"""Fail-open observability for agent routing decisions.

Routing telemetry is deliberately small and dependency-free.  It emits one
bounded JSON record when a route is selected and one when that route reaches a
terminal outcome.  Records contain only low-cardinality labels and one-way
hashes of correlation identifiers; prompts, model responses, credentials, and
paths are never persisted.

Metric definitions
------------------
* ``decisions_total`` is the denominator for selection and fallback rates.
* ``hermes_selections_total`` counts decisions whose selected source is
  ``hermes``.
* ``fallbacks_total`` counts decisions that selected ``default_fallback``.
* ``outcome_quality_rate`` is good outcomes divided by outcomes with a known
  quality label.  Unknown/interrupted outcomes are excluded from this
  denominator, rather than being silently treated as successful.

Telemetry is best effort.  A broken home directory, logger, or file must never
change routing behavior, so all public record functions return ``None`` after a
telemetry error.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

logger = logging.getLogger(__name__)

EVENT_SCHEMA_VERSION = 1
EVENTS_ENV_VAR = "HERMES_ROUTING_EVENTS_PATH"
DISABLE_ENV_VAR = "HERMES_ROUTING_TELEMETRY"

SOURCE_HERMES = "hermes"
SOURCE_CODEX_NATIVE = "codex_native"
SOURCE_CLAUDE_CODE = "claude_code_cli"
SOURCE_DEFAULT_FALLBACK = "default_fallback"
ROUTE_SOURCES = frozenset({
    SOURCE_HERMES, SOURCE_CODEX_NATIVE, SOURCE_CLAUDE_CODE, SOURCE_DEFAULT_FALLBACK,
})
ROUTE_INTENTS = frozenset({SOURCE_HERMES, SOURCE_CODEX_NATIVE, SOURCE_CLAUDE_CODE, "default"})
OUTCOMES = frozenset({"completed", "failed", "timeout", "interrupted"})
QUALITY_VALUES = frozenset({"good", "poor", "unknown"})
TASK_SHAPES = frozenset({"bounded_coordination", "single_task", "unknown"})
ROUTING_CLASSIFICATIONS = frozenset({
    "explicit", "hermes_positive", "codex_native", "ambiguous", "fallback",
})
ROUTING_PRECEDENCE = frozenset({
    "explicit_directive", "hermes_task_shape", "codex_native_task_shape", "safe_default",
})
ROUTING_SIGNALS = frozenset({
    "decomposition", "bounded_scope", "dependency_coordination",
    "explicit_orchestration", "needs_parallel_children", "coding_task",
})
FALLBACK_REASONS = frozenset({
    "", "unavailable", "error", "timeout", "invalid",
    "auth", "auth_permanent", "billing", "rate_limit", "overloaded",
    "server_error", "context_overflow", "payload_too_large",
    "image_too_large", "multimodal_tool_content_unsupported",
    "model_not_found", "provider_policy_blocked", "format_error",
    "thinking_signature", "long_context_tier",
    "oauth_long_context_beta_forbidden", "llama_cpp_grammar_pattern",
    "unknown",
})

# Stable names for dashboards and log-based metric extraction.
METRIC_NAMES = {
    "decisions_total": "hermes_routing_decisions_total",
    "hermes_selections_total": "hermes_routing_selections_total",
    "fallbacks_total": "hermes_routing_fallbacks_total",
    "outcomes_total": "hermes_routing_outcomes_total",
    "outcome_quality_known_total": "hermes_routing_outcome_quality_known_total",
    "outcome_quality_good_total": "hermes_routing_outcome_quality_good_total",
    "selection_rate": "hermes_routing_selection_rate",
    "fallback_rate": "hermes_routing_fallback_rate",
    "outcome_quality_rate": "hermes_routing_outcome_quality_rate",
}

_METRICS_LOCK = threading.Lock()
_METRICS = {
    "decisions_total": 0,
    "hermes_selections_total": 0,
    "fallbacks_total": 0,
    "outcomes_total": 0,
    "outcome_quality_known_total": 0,
    "outcome_quality_good_total": 0,
}


def _events_path() -> Path:
    configured = os.environ.get(EVENTS_ENV_VAR, "").strip()
    if configured:
        return Path(configured).expanduser()
    try:
        from hermes_constants import get_hermes_home

        home = get_hermes_home()
    except Exception:
        home = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
    return Path(home) / "logs" / "routing-events.jsonl"


def _enabled() -> bool:
    value = os.environ.get(DISABLE_ENV_VAR, "1").strip().lower()
    return value not in {"0", "false", "no", "off"}


def _hash_identifier(value: Optional[str]) -> str:
    if not value:
        return ""
    return hashlib.sha256(str(value).encode("utf-8", "replace")).hexdigest()[:16]


def _label(value: Any, allowed: frozenset[str], default: str) -> str:
    normalized = str(value or "").strip().lower()
    return normalized if normalized in allowed else default


def _write_event(event: Dict[str, Any]) -> None:
    """Write one event and log the same bounded JSON for live evidence."""
    path = _events_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(event, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(encoded + "\n")
    logger.info("hermes.routing %s", encoded)


def _emit(event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if not _enabled():
        return None
    try:
        _write_event(event)
    except Exception:
        # Observability is never on the routing critical path.
        logger.debug("Routing telemetry unavailable", exc_info=True)
        return None
    with _METRICS_LOCK:
        if event["event"] == "routing_decision":
            _METRICS["decisions_total"] += 1
            if event["selected_agent_source"] == SOURCE_HERMES:
                _METRICS["hermes_selections_total"] += 1
            if event["fallback"]:
                _METRICS["fallbacks_total"] += 1
        elif event["event"] == "routing_outcome":
            _METRICS["outcomes_total"] += 1
            if event["outcome_quality"] in {"good", "poor"}:
                _METRICS["outcome_quality_known_total"] += 1
            if event["outcome_quality"] == "good":
                _METRICS["outcome_quality_good_total"] += 1
    return event


def record_routing_decision(
    *,
    request_id: Optional[str],
    route_intent: str,
    selected_agent_source: str,
    fallback: bool = False,
    fallback_reason: str = "",
    task_shape: str = "unknown",
    session_id: Optional[str] = None,
    routing_context: Optional[Dict[str, Any]] = None,
) -> Optional[Dict[str, Any]]:
    """Record a route selection using privacy-safe, stable labels."""
    source = _label(selected_agent_source, ROUTE_SOURCES, SOURCE_DEFAULT_FALLBACK)
    event = {
        "schema_version": EVENT_SCHEMA_VERSION,
        "event": "routing_decision",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": _hash_identifier(request_id),
        "session_id": _hash_identifier(session_id),
        "route_intent": _label(route_intent, ROUTE_INTENTS, "default"),
        "selected_agent_source": source,
        "fallback": bool(fallback or source == SOURCE_DEFAULT_FALLBACK),
        "fallback_reason": _label(
            fallback_reason,
            FALLBACK_REASONS,
            "other",
        ),
        "task_shape": _label(task_shape, TASK_SHAPES, "unknown"),
    }
    # Copy only the router's bounded vocabulary.  In particular, never copy
    # ``reason`` or prompt-derived strings into the event record.
    context = routing_context if isinstance(routing_context, dict) else {}
    classification = context.get("classification")
    if classification in ROUTING_CLASSIFICATIONS:
        event["classification"] = classification
    precedence = context.get("precedence")
    if precedence in ROUTING_PRECEDENCE:
        event["precedence"] = precedence
    version = context.get("routing_version")
    if version == "task-shape-v1":
        event["routing_version"] = version
    if isinstance(context.get("matched_signals"), (list, tuple)):
        event["matched_signals"] = [
            signal for signal in context["matched_signals"][:20]
            if signal in ROUTING_SIGNALS
        ]
    if isinstance(context.get("signal_scores"), dict):
        event["signal_scores"] = {
            signal: int(score)
            for signal, score in list(context["signal_scores"].items())[:20]
            if signal in ROUTING_SIGNALS
            and isinstance(score, (int, float))
            and not isinstance(score, bool)
        }
    if isinstance(context.get("task_shape"), dict):
        event["task_shape_details"] = {
            key: bool(value)
            for key, value in list(context["task_shape"].items())[:20]
            if (key in ROUTING_SIGNALS or key == "coordination_signals")
            and isinstance(value, (bool, int))
        }
    return _emit(event)


def normalize_outcome(outcome: str, quality: Optional[str] = None) -> Tuple[str, str]:
    """Normalize runtime statuses into the outcome and quality vocabulary."""
    normalized = str(outcome or "").strip().lower()
    if normalized in {"success", "complete", "completed", "ok"}:
        normalized = "completed"
    elif normalized in {"error", "failure", "failed"}:
        normalized = "failed"
    elif normalized not in {"timeout", "interrupted"}:
        normalized = "failed"
    quality_label = _label(quality, QUALITY_VALUES, "unknown")
    if quality_label == "unknown" and normalized in {"failed", "timeout"}:
        quality_label = "poor"
    return normalized, quality_label


def record_routing_outcome(
    *,
    request_id: Optional[str],
    selected_agent_source: str,
    outcome: str,
    outcome_quality: Optional[str] = None,
    session_id: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Record a terminal route outcome; failures are intentionally fail-open."""
    normalized_outcome, quality = normalize_outcome(outcome, outcome_quality)
    event = {
        "schema_version": EVENT_SCHEMA_VERSION,
        "event": "routing_outcome",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": _hash_identifier(request_id),
        "session_id": _hash_identifier(session_id),
        "selected_agent_source": _label(selected_agent_source, ROUTE_SOURCES, SOURCE_DEFAULT_FALLBACK),
        "outcome": normalized_outcome,
        "outcome_quality": quality,
    }
    return _emit(event)


def record_routing_decision_from_context(
    context: Dict[str, Any],
    *,
    request_id: Optional[str],
    session_id: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Persist a :meth:`RoutingDecision.telemetry_context` selection.

    Keeping this adapter here means routing stays a pure decision function and
    callers do not need to duplicate the stable field mapping. Unknown or
    malformed context values reduce to safe default labels.
    """
    context = context if isinstance(context, dict) else {}
    intended = context.get("intended_route") or context.get("route") or "default"
    actual = context.get("actual_agent_source") or intended
    return record_routing_decision(
        request_id=request_id,
        session_id=session_id,
        route_intent=str(intended),
        selected_agent_source=str(actual),
        # ``classification`` describes how the policy reached its safe
        # default; it is not evidence that a provider failover occurred.
        # Count only an actual intended/observed lane mismatch or the explicit
        # default-fallback source in the fallback-rate denominator.
        fallback=actual != intended or actual == SOURCE_DEFAULT_FALLBACK,
        fallback_reason=str(context.get("fallback_reason") or ""),
        task_shape=str(context.get("task_shape_label") or "unknown"),
        routing_context=context,
    )


def record_routing_outcome_from_context(
    context: Dict[str, Any],
    *,
    request_id: Optional[str],
    session_id: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Persist observed completion fields from a routing context."""
    context = context if isinstance(context, dict) else {}
    return record_routing_outcome(
        request_id=request_id,
        session_id=session_id,
        selected_agent_source=str(
            context.get("actual_agent_source")
            or context.get("route")
            or SOURCE_DEFAULT_FALLBACK
        ),
        outcome=str(context.get("completion_status") or "failed"),
        outcome_quality=context.get("outcome_quality"),
    )


def get_routing_metrics(path: Optional[Path] = None) -> Dict[str, Any]:
    """Aggregate persisted events into rates suitable for runtime evidence."""
    counts = dict(_METRICS)
    by_source: Dict[str, Dict[str, int]] = {source: {"decisions": 0, "outcomes": 0} for source in ROUTE_SOURCES}
    events_path = Path(path) if path is not None else _events_path()
    try:
        with events_path.open("r", encoding="utf-8") as handle:
            counts = {key: 0 for key in counts}
            for line in handle:
                try:
                    event = json.loads(line)
                except (TypeError, ValueError):
                    continue
                source = event.get("selected_agent_source")
                if source not in by_source:
                    continue
                if event.get("event") == "routing_decision":
                    counts["decisions_total"] += 1
                    by_source[source]["decisions"] += 1
                    if source == SOURCE_HERMES:
                        counts["hermes_selections_total"] += 1
                    if event.get("fallback"):
                        counts["fallbacks_total"] += 1
                elif event.get("event") == "routing_outcome":
                    counts["outcomes_total"] += 1
                    by_source[source]["outcomes"] += 1
                    quality = event.get("outcome_quality")
                    if quality in {"good", "poor"}:
                        counts["outcome_quality_known_total"] += 1
                    if quality == "good":
                        counts["outcome_quality_good_total"] += 1
    except (FileNotFoundError, OSError):
        pass

    decisions = counts["decisions_total"]
    known = counts["outcome_quality_known_total"]
    return {
        **counts,
        "metric_names": dict(METRIC_NAMES),
        "selection_rate": _ratio(counts["hermes_selections_total"], decisions),
        "fallback_rate": _ratio(counts["fallbacks_total"], decisions),
        "outcome_quality_rate": _ratio(counts["outcome_quality_good_total"], known),
        "by_source": by_source,
    }


def _ratio(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 6) if denominator else 0.0


def reset_metrics_for_tests() -> None:
    """Reset process-local counters; persisted event files are never deleted."""
    with _METRICS_LOCK:
        for key in _METRICS:
            _METRICS[key] = 0
