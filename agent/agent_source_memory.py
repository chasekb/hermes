"""Durable, privacy-safe records for agent-source routing outcomes.

Routing records use the same compact shape as ``backlog/decision-memory.json``
(the ``expected``/``observed``/``outcome``/``recommendation`` fields), while
also exposing explicit fields for routing analysis.  Prompt text is never
stored; callers may provide it only to derive a SHA-256 comparison key.

This module is deliberately independent from a particular memory provider.
The routing path can use it when the built-in memory is enabled, and the
MemoryManager hook lets configured providers observe the same record.  All
persistence is best effort: a broken or unavailable memory store must never
make an otherwise successful request fail.
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import os
import re
import tempfile
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional

logger = logging.getLogger(__name__)

try:
    import fcntl
except ImportError:  # pragma: no cover - Windows uses an atomic replace without locking.
    fcntl = None

_STORE_VERSION = 1
_DEFAULT_DESCRIPTION = (
    "Durable decision-memory store for Hermes backlog, workflow, skill, and hook reviews."
)
_MAX_LABEL_LENGTH = 96
_SAFE_LABEL_RE = re.compile(r"[^A-Za-z0-9_.:/@+-]+")
_SECRET_LABEL_RE = re.compile(
    r"(?:api[_-]?key|access[_-]?token|secret|password|credential|private[_-]?key)",
    re.IGNORECASE,
)
_ROUTING_SIGNALS = frozenset(
    {
        "decomposition",
        "bounded_scope",
        "dependency_coordination",
        "explicit_orchestration",
        "needs_parallel_children",
        "coding_task",
    }
)
_ROUTE_SOURCES = frozenset(
    {"hermes", "codex_native", "claude_code_cli", "default_fallback", "unknown"}
)
_ROUTING_CLASSIFICATIONS = frozenset(
    {"explicit", "hermes_positive", "codex_native", "ambiguous", "fallback"}
)
_ROUTING_PRECEDENCE = frozenset(
    {
        "explicit_directive",
        "hermes_task_shape",
        "codex_native_task_shape",
        "safe_default",
        # Compatibility with early task-shape router integrations.
        "task_shape",
    }
)
_ROUTING_VERSIONS = frozenset({"task-shape-v1"})
_TASK_SHAPE_KEYS = _ROUTING_SIGNALS | {"coordination_signals"}
_FALLBACK_REASONS = frozenset(
    {
        "fallback",
        "hermes_unavailable",
        "unavailable",
        "error",
        "timeout",
        "invalid",
        "auth",
        "billing",
        "rate_limit",
        "overloaded",
        "server_error",
        "context_overflow",
        "provider_policy_blocked",
    }
)


def _is_truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "on", "enabled"}


def _optional_bool(value: Any) -> Optional[bool]:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "on", "enabled"}:
        return True
    if normalized in {"0", "false", "no", "off", "disabled"}:
        return False
    return bool(value)


def _safe_label(value: Any, default: str = "unknown") -> str:
    """Return a bounded label, never arbitrary prompt or credential content."""
    if value is None:
        return default
    value = str(value).strip()
    if not value or _SECRET_LABEL_RE.search(value):
        return "redacted"
    value = _SAFE_LABEL_RE.sub("_", value).strip("_")
    if not value:
        return default
    return value[:_MAX_LABEL_LENGTH]


def _safe_route(value: Any) -> str:
    """Keep agent-source labels within the routing telemetry vocabulary."""
    normalized = str(value or "").strip().lower()
    return normalized if normalized in _ROUTE_SOURCES else "unknown"


def _safe_session_id(value: Any) -> str:
    """Keep session provenance useful without accepting free-form text."""
    return _safe_label(value, default="")


def _prompt_digest(prompt: Any = None, prompt_sha: Any = None) -> str:
    """Return a stable digest without persisting the supplied prompt."""
    if prompt_sha:
        candidate = str(prompt_sha).strip().lower()
        if re.fullmatch(r"[0-9a-f]{64}", candidate):
            return candidate
        return hashlib.sha256(candidate.encode("utf-8", "replace")).hexdigest()
    if prompt is None:
        return ""
    return hashlib.sha256(str(prompt).encode("utf-8", "replace")).hexdigest()


def _safe_quality(value: Any) -> Any:
    if isinstance(value, bool):
        return bool(value)
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if math.isfinite(float(value)):
            return value
    normalized = str(value or "").strip().lower()
    if normalized in {"good", "poor", "high", "low", "fallback_success", "unknown"}:
        return normalized
    return "unknown"


def _safe_status(value: Any) -> str:
    """Keep completion labels categorical instead of persisting error text."""
    normalized = str(value or "").strip().lower()
    if normalized in {
        "completed",
        "complete",
        "success",
        "succeeded",
        "passed",
        "pass",
        "failed",
        "failure",
        "error",
        "timeout",
        "interrupted",
        "unknown",
    }:
        return normalized
    return "unknown"


def _default_store_path() -> Path:
    from hermes_constants import get_hermes_home

    return get_hermes_home() / "backlog" / "decision-memory.json"


def _load_store(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {
            "version": _STORE_VERSION,
            "description": _DEFAULT_DESCRIPTION,
            "updated_at": "",
            "records": [],
        }
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("decision-memory store must contain a JSON object")
    records = data.get("records")
    if records is None:
        data["records"] = []
    elif not isinstance(records, list):
        raise ValueError("decision-memory records must be a JSON array")
    return data


def _write_store(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = path.with_name(path.name + ".lock")
    with lock_path.open("a+", encoding="utf-8") as lock:
        if fcntl is not None:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        try:
            # Read again while holding the lock so concurrent routing requests
            # append rather than overwrite each other.
            current = _load_store(path)
            current.setdefault("records", []).extend(data.get("records", []))
            current["version"] = current.get("version", _STORE_VERSION)
            current["description"] = current.get("description", _DEFAULT_DESCRIPTION)
            current["updated_at"] = datetime.now(timezone.utc).isoformat()
            fd, temp_name = tempfile.mkstemp(
                prefix=path.name + ".", suffix=".tmp", dir=str(path.parent)
            )
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as output:
                    json.dump(current, output, indent=2, ensure_ascii=False)
                    output.write("\n")
                    output.flush()
                    os.fsync(output.fileno())
                os.replace(temp_name, path)
            finally:
                if os.path.exists(temp_name):
                    os.unlink(temp_name)
        finally:
            if fcntl is not None:
                fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def build_agent_source_outcome(
    *,
    intended_route: Any = None,
    actual_agent_source: Any = None,
    request_class: Any = None,
    completion_status: Any = None,
    outcome_quality: Any = None,
    routing_context: Optional[Mapping[str, Any]] = None,
    prompt: Any = None,
    prompt_sha: Any = None,
    session_id: Any = None,
    fallback_reason: Any = None,
    fallback: Optional[bool] = None,
    timestamp: Optional[str] = None,
) -> Dict[str, Any]:
    """Build a compact decision-memory-compatible routing record.

    ``prompt`` is accepted solely to compute ``prompt_sha`` and is never
    copied into the returned record.  Labels are bounded and credential-like
    values are replaced with ``redacted``.
    """
    context = routing_context if isinstance(routing_context, Mapping) else {}
    intended = _safe_route(
        intended_route
        if intended_route is not None
        else context.get("expected_agent_source", context.get("intended_route", context.get("route")))
    )
    actual = _safe_route(actual_agent_source)
    if request_class is not None:
        request_kind = _safe_label(request_class)
    else:
        context_request_kind = str(context.get("task_shape_label") or "").strip().lower()
        request_kind = (
            context_request_kind
            if context_request_kind in {"bounded_coordination", "single_task", "unknown"}
            else "unknown"
        )
    status = _safe_status(completion_status)
    quality = _safe_quality(outcome_quality)
    digest = _prompt_digest(prompt, prompt_sha)
    # A source mismatch is always a fallback, even if an upstream result
    # omitted the flag or incorrectly reported ``False``.
    is_fallback = bool(fallback) if fallback is not None else False
    is_fallback = is_fallback or intended != actual
    succeeded = status.lower() in {"completed", "complete", "success", "succeeded", "passed", "pass"}
    recorded_at = timestamp or datetime.now(timezone.utc).isoformat()
    record: Dict[str, Any] = {
        # Keep both spellings: existing decision-memory records use ``ts``,
        # while the record_eval helper validates the more explicit name.
        "ts": recorded_at,
        "timestamp": recorded_at,
        "subject_type": "agent_source_routing",
        "subject_id": digest or f"{request_kind}:{actual}",
        "expected": intended,
        "observed": actual,
        # Aliases shared with routing telemetry.  Keep the explicit names
        # below as the durable memory contract, while allowing telemetry
        # consumers to query this record without a translation step.
        "route_intent": intended,
        "agent_source": actual,
        "outcome": "pass" if succeeded else "fail",
        "recommendation": quality,
        "evidence": [f"agent_source:{actual}", f"request_class:{request_kind}"],
        # Match the existing decision-memory redaction marker and retain a
        # more specific marker for prompt-derived provenance.
        "risk_flags": ["secret_redacted", "prompt_redacted"],
        "redacted": True,
        "prompt_class": request_kind,
        "prompt_sha": digest,
        "intended_route": intended,
        "actual_agent_source": actual,
        "request_class": request_kind,
        "completion_status": status,
        "outcome_quality": quality,
        "fallback": is_fallback,
        "request_count": 1,
        "success": succeeded,
        "lanes": [intended, actual],
        "reviewers": [],
    }
    # Preserve only the router's bounded, structured decision context.  This
    # supports later analysis without retaining prompt text or request prose.
    allowed_context_values = {
        "routing_version": _ROUTING_VERSIONS,
        "classification": _ROUTING_CLASSIFICATIONS,
        "precedence": _ROUTING_PRECEDENCE,
        "task_shape_label": {"bounded_coordination", "single_task", "unknown"},
    }
    for key, allowed in allowed_context_values.items():
        value = str(context.get(key) or "").strip().lower()
        if value in allowed:
            record[key] = value
    if isinstance(context.get("matched_signals"), (list, tuple)):
        record["matched_signals"] = [
            str(signal).strip().lower()
            for signal in context["matched_signals"][:20]
            if str(signal).strip().lower() in _ROUTING_SIGNALS
        ]
    if isinstance(context.get("signal_scores"), Mapping):
        record["signal_scores"] = {
            str(name).strip().lower(): int(score)
            for name, score in list(context["signal_scores"].items())[:20]
            if str(name).strip().lower() in _ROUTING_SIGNALS
            and isinstance(score, (int, float))
            and not isinstance(score, bool)
        }
    if isinstance(context.get("task_shape"), Mapping):
        record["task_shape"] = {
            str(name).strip().lower(): bool(value)
            for name, value in list(context["task_shape"].items())[:20]
            if str(name).strip().lower() in _TASK_SHAPE_KEYS
            and isinstance(value, (bool, int))
        }
    safe_session = _safe_session_id(session_id)
    if safe_session:
        record["session_id"] = safe_session
    safe_reason = _safe_label(fallback_reason, default="").lower()
    if safe_reason in _FALLBACK_REASONS:
        record["fallback_reason"] = safe_reason
    return record


def _notify_memory_manager(memory_manager: Any, record: Dict[str, Any]) -> None:
    if memory_manager is None:
        return
    try:
        callback = getattr(memory_manager, "on_agent_source_outcome", None)
        if callback is not None:
            callback(record)
    except Exception as exc:  # pragma: no cover - exercised through failure injection.
        logger.debug("memory provider routing-outcome hook failed: %s", exc)


def record_agent_source_outcome(
    *,
    intended_route: Any = None,
    actual_agent_source: Any = None,
    request_class: Any = None,
    completion_status: Any = None,
    outcome_quality: Any = None,
    store_path: Optional[Path | str] = None,
    enabled: bool = True,
    memory_manager: Any = None,
    agent: Any = None,
    prompt: Any = None,
    prompt_sha: Any = None,
    session_id: Any = None,
    fallback_reason: Any = None,
    fallback: Optional[bool] = None,
    routing_context: Optional[Mapping[str, Any]] = None,
) -> Optional[Dict[str, Any]]:
    """Persist one routing outcome and return its sanitized record.

    Persistence and provider callbacks are best effort.  ``None`` means that
    persistence was disabled or the store could not be written; callers should
    continue serving the request in either case.
    """
    if agent is not None:
        memory_manager = memory_manager or getattr(agent, "_memory_manager", None)
        if session_id is None:
            session_id = getattr(agent, "session_id", None)
        if enabled is True:
            configured = getattr(agent, "_routing_outcomes_enabled", None)
            if configured is None:
                configured = (
                    getattr(agent, "_memory_enabled", False)
                    or getattr(agent, "_user_profile_enabled", False)
                    or memory_manager is not None
                )
            enabled = _is_truthy(configured)
    if not enabled:
        return None

    record = build_agent_source_outcome(
        intended_route=intended_route,
        actual_agent_source=actual_agent_source,
        request_class=request_class,
        completion_status=completion_status,
        outcome_quality=outcome_quality,
        prompt=prompt,
        prompt_sha=prompt_sha,
        session_id=session_id,
        fallback_reason=fallback_reason,
        fallback=fallback,
        routing_context=routing_context,
    )
    # Provider hooks are observers.  Give them a deep copy so a buggy or
    # legacy provider cannot mutate the sanitized record that is written to
    # the durable store (or inject data into it after redaction).
    _notify_memory_manager(memory_manager, deepcopy(record))
    try:
        _write_store(Path(store_path).expanduser() if store_path else _default_store_path(), {"records": [record]})
    except Exception as exc:
        logger.debug("agent-source outcome persistence unavailable: %s", exc)
        return None
    return record


def _agent_routing_context(agent: Any) -> Dict[str, Any]:
    """Extract structured routing context without retaining arbitrary state."""
    for attribute in ("_routing_decision", "routing_decision", "_route_decision"):
        decision = getattr(agent, attribute, None)
        if decision is None:
            continue
        try:
            context_builder = getattr(decision, "telemetry_context", None)
            if callable(context_builder):
                context = context_builder()
            else:
                context = decision
            if isinstance(context, Mapping):
                return dict(context)
        except Exception as exc:
            logger.debug("routing decision context unavailable: %s", exc)
    for attribute in ("_routing_context", "routing_context"):
        context = getattr(agent, attribute, None)
        if isinstance(context, Mapping):
            return dict(context)
    return {}


def _first_value(source: Mapping[str, Any], keys: Iterable[str]) -> Any:
    for key in keys:
        value = source.get(key)
        if value is not None and value != "":
            return value
    return None


def record_agent_source_outcome_for_agent(
    agent: Any,
    prompt: Any,
    result: Optional[Mapping[str, Any]],
    *,
    store_path: Optional[Path | str] = None,
) -> Optional[Dict[str, Any]]:
    """Record one completed ``AIAgent.run_conversation`` result.

    The conversation wrapper uses this adapter so every returned route result
    gets the same durable record, including early failures and fallback
    results.  Only allowlisted routing context is copied by
    :func:`build_agent_source_outcome`; the prompt is used for its digest only.
    This function is fail-open because it runs after the user request.
    """
    try:
        result_map = result if isinstance(result, Mapping) else {}
        context = _agent_routing_context(agent)
        result_context = result_map.get("routing_context")
        if isinstance(result_context, Mapping):
            context = {**context, **result_context}

        intended = _first_value(
            result_map,
            ("intended_route", "route_intent", "expected_agent_source"),
        )
        if intended is None:
            intended = _first_value(
                context,
                ("intended_route", "route_intent", "expected_agent_source", "route"),
            )
        if intended is None:
            intended = _first_value(agent.__dict__ if hasattr(agent, "__dict__") else {},
                                    ("_intended_route", "intended_route", "_route_intent"))

        actual = _first_value(
            result_map,
            ("actual_agent_source", "agent_source", "source"),
        )
        if actual is None:
            actual = _first_value(context, ("actual_agent_source", "agent_source", "source"))
        if actual is None:
            actual = _first_value(agent.__dict__ if hasattr(agent, "__dict__") else {},
                                 ("_actual_agent_source", "actual_agent_source", "agent_source"))
        if actual is None:
            actual = "codex_native" if getattr(agent, "api_mode", "") == "codex_app_server" else "hermes"
        if intended is None:
            # A plain AIAgent turn has no route policy to compare against;
            # treat its observed source as the intended source rather than
            # manufacturing a fallback event for an un-routed request.
            intended = actual

        request_class = _first_value(result_map, ("request_class", "prompt_class", "task_shape_label"))
        if request_class is None:
            request_class = _first_value(context, ("request_class", "prompt_class", "task_shape_label", "classification"))
        if request_class is None:
            request_class = _first_value(agent.__dict__ if hasattr(agent, "__dict__") else {},
                                         ("_request_class", "request_class", "task_shape_label"))

        if _first_value(result_map, ("completion_status",)) is not None:
            completion_status = _first_value(result_map, ("completion_status",))
        elif result_map.get("interrupted"):
            completion_status = "interrupted"
        elif result_map.get("completed") is True:
            completion_status = "completed"
        else:
            completion_status = "failed"

        fallback = _optional_bool(result_map.get("fallback"))
        fallback_detected = (fallback is True) or intended != actual
        fallback_reason = _first_value(result_map, ("fallback_reason",))
        if fallback_reason is None:
            fallback_reason = _first_value(context, ("fallback_reason",))
        if fallback_reason is None and fallback_detected:
            fallback_reason = "fallback"

        quality = _first_value(result_map, ("outcome_quality", "quality"))
        if quality is None:
            quality = _first_value(context, ("outcome_quality", "quality"))
        if quality is None:
            quality = "high" if result_map.get("completed") is True and not fallback_detected else (
                "fallback_success" if result_map.get("completed") is True else "low"
            )

        return record_agent_source_outcome(
            intended_route=intended,
            actual_agent_source=actual,
            request_class=request_class,
            completion_status=completion_status,
            outcome_quality=quality,
            store_path=store_path,
            memory_manager=getattr(agent, "_memory_manager", None),
            agent=agent,
            prompt=prompt,
            session_id=getattr(agent, "session_id", None),
            fallback_reason=fallback_reason,
            fallback=fallback,
            routing_context=context,
        )
    except Exception as exc:
        logger.debug("agent-source outcome adapter failed: %s", exc)
        return None


def read_agent_source_outcomes(
    store_path: Optional[Path | str] = None,
    *,
    intended_route: Optional[str] = None,
    actual_agent_source: Optional[str] = None,
    request_class: Optional[str] = None,
    limit: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """Read routing records for later intended-versus-actual comparisons."""
    try:
        data = _load_store(Path(store_path).expanduser() if store_path else _default_store_path())
    except Exception as exc:
        logger.debug("agent-source outcome query unavailable: %s", exc)
        return []
    records: Iterable[Dict[str, Any]] = (
        item for item in data.get("records", []) if isinstance(item, dict)
    )
    if intended_route is not None:
        records = (
            item
            for item in records
            if item.get("intended_route", item.get("route_intent")) == intended_route
        )
    if actual_agent_source is not None:
        records = (
            item
            for item in records
            if item.get("actual_agent_source", item.get("agent_source")) == actual_agent_source
        )
    if request_class is not None:
        records = (
            item
            for item in records
            if item.get("request_class", item.get("prompt_class")) == request_class
        )
    result = list(records)
    if limit is not None:
        requested = max(0, int(limit))
        result = result[-requested:] if requested else []
    return result


__all__ = [
    "build_agent_source_outcome",
    "record_agent_source_outcome",
    "record_agent_source_outcome_for_agent",
    "read_agent_source_outcomes",
]
