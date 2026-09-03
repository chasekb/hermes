"""Deterministic task-shape routing for Hermes and Codex-native lanes.

The router deliberately uses two layers of evidence:

* explicit lane directives (for example, ``use the Codex-native lane``), and
* task-shape signals (coordination, scope, dependencies, parallel child work,
  and coding/editing intent).

It is intentionally a pure module.  Callers can route first and then attach
runtime facts such as the actual agent source and completion outcome through
:meth:`RoutingDecision.telemetry_context`.  No prompt text is retained in the
returned context.

Precedence, from strongest to weakest:

1. An explicit Hermes/Codex-native directive.
2. A Hermes coordination shape (at least two coordination signals).
3. A focused coding/editing shape.
4. A safe Codex-native default.  Weak, underspecified requests are marked
   ``ambiguous``; requests with no routing evidence are marked ``fallback``.

The default is conservative: a request only enters the Hermes lane when its
shape demonstrates coordination work, rather than merely mentioning a
coordination word.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional, Tuple

ROUTE_HERMES = "hermes"
ROUTE_CODEX_NATIVE = "codex_native"
ROUTING_VERSION = "task-shape-v1"

# Canonical signal names are part of the telemetry contract.  Keep these
# stable even if individual regexes gain additional synonyms.
_SIGNAL_NAMES = (
    "decomposition",
    "bounded_scope",
    "dependency_coordination",
    "explicit_orchestration",
    "needs_parallel_children",
    "coding_task",
)

_SIGNAL_PATTERNS: Mapping[str, Tuple[Tuple[str, str], ...]] = {
    "decomposition": (
        ("decompose", r"\bdecompos(?:e|ed|ition|ing)\b"),
        ("split", r"\bsplit\b"),
        ("subtasks", r"\bsubtasks?\b"),
        ("break into", r"\bbreak\s+(?:this\s+)?(?:work|task)?\s*into\b"),
        ("step by step", r"\bstep[- ]by[- ]step\b"),
    ),
    "bounded_scope": (
        ("bounded", r"\bbounded\b"),
        ("time-boxed", r"\btime[- ]box(?:ed)?\b"),
        ("limited scope", r"\blimited\s+(?:to|scope)\b"),
        ("focused", r"\bfocused\b"),
        ("one file", r"\bone\s+(?:file|module)\b"),
        ("acceptance criteria", r"\bacceptance\s+criteria\b"),
        ("within scope", r"\bwithin\s+(?:the\s+)?scope\b"),
    ),
    "dependency_coordination": (
        ("dependency", r"\bdependenc(?:y|ies)\b"),
        ("depends on", r"\bdepends?\s+on\b"),
        ("after completion", r"\bafter\s+(?:the\s+)?(?:task|step|child|work)\b[^.]{0,80}\bcomplete"),
        ("coordinate", r"\bcoordinat(?:e|ion|ing|ed)\b"),
        ("fan-in", r"\bfan[- ]in\b"),
        ("blocked by", r"\bblocked\s+by\b"),
    ),
    "explicit_orchestration": (
        ("orchestrate", r"\borchestrat(?:e|ion|ing|ed|or)\b"),
        ("workflow", r"\bworkflow\b"),
        ("parent child", r"\bparent[- ]child\b"),
        ("kanban", r"\bkanban\b"),
        ("supervise", r"\bsupervis(?:e|ion|ing|ed)\b"),
    ),
    "needs_parallel_children": (
        ("parallel", r"\bparallel(?:ly)?\b"),
        ("concurrently", r"\bconcurren(?:t|tly)\b"),
        ("in parallel", r"\bin\s+parallel\b"),
        ("child workers", r"\bchild\s+(?:agents?|workers?)\b"),
        ("multiple agents", r"\bmultiple\s+agents?\b"),
        ("fan-out", r"\bfan[- ]out\b"),
    ),
    "coding_task": (
        ("implement", r"\bimplement(?:ation|ing|ed)?\b"),
        ("fix", r"\bfix(?:es|ed|ing)?\b"),
        ("refactor", r"\brefactor(?:ing|ed)?\b"),
        ("patch", r"\bpatch(?:es|ed|ing)?\b"),
        ("edit", r"\bedit(?:s|ed|ing)?\b"),
        ("regression test", r"\bregression\s+test\b"),
        ("repository", r"\brepositor(?:y|ies)\b"),
        ("source file", r"\bsource\s+file\b"),
        ("function", r"\bfunction\b"),
    ),
}

# Weak intent is useful for distinguishing an underspecified request from a
# pure fallback without changing the selected safe default.
_AMBIGUOUS_PATTERNS: Tuple[re.Pattern[str], ...] = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\breview\b",
        r"\bsuggest\b",
        r"\bcompare\b",
        r"\bapproach\b",
        r"\bimprovements?\b",
        r"\bhelp\b",
    )
)

_EXPLICIT_HERMES = re.compile(
    r"\b(?:use|choose|select|route|send|run|keep|stay\s+on)\s+(?:the\s+)?(?:hermes(?:[- ]native)?|hermes\s+agent)\b",
    re.IGNORECASE,
)
_EXPLICIT_CODEX = re.compile(
    r"\b(?:use|choose|select|route|send|run|keep|stay\s+on)\s+(?:the\s+)?(?:codex(?:[- ]native)?|codex\s+cli)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class TaskShape:
    """The privacy-safe shape extracted from a request.

    ``matches`` is retained only in memory for human/debug inspection and is
    not included in :meth:`to_dict`; it contains canonical vocabulary labels,
    never prompt excerpts.
    """

    decomposition: bool = False
    bounded_scope: bool = False
    dependency_coordination: bool = False
    explicit_orchestration: bool = False
    needs_parallel_children: bool = False
    coding_task: bool = False
    matches: Mapping[str, Tuple[str, ...]] = field(default_factory=dict, repr=False)

    @property
    def coordination_signals(self) -> int:
        """Count independent coordination/task-shape dimensions."""
        return sum(
            bool(getattr(self, name))
            for name in (
                "decomposition",
                "bounded_scope",
                "dependency_coordination",
                "explicit_orchestration",
                "needs_parallel_children",
            )
        )

    @property
    def has_coordination_shape(self) -> bool:
        """Whether enough independent signals justify Hermes coordination."""
        return self.coordination_signals >= 2

    def to_dict(self) -> Dict[str, Any]:
        """Return the stable, JSON-safe task-shape representation."""
        return {
            "bounded_scope": self.bounded_scope,
            "coding_task": self.coding_task,
            "dependency_coordination": self.dependency_coordination,
            "explicit_orchestration": self.explicit_orchestration,
            "needs_parallel_children": self.needs_parallel_children,
            "decomposition": self.decomposition,
            "coordination_signals": self.coordination_signals,
        }


@dataclass(frozen=True)
class RoutingDecision:
    """A route plus explainable, privacy-safe decision context."""

    route: str
    task_shape: TaskShape
    classification: str
    precedence: str
    reason: str
    matched_signals: Tuple[str, ...] = ()
    signal_scores: Mapping[str, int] = field(default_factory=dict)
    fallback_route: str = ROUTE_CODEX_NATIVE

    @property
    def intended_route(self) -> str:
        """Alias used by decision-memory records."""
        return self.route

    @property
    def agent_source(self) -> str:
        """The selected source before runtime fallback is observed."""
        return self.route

    @property
    def task_shape_label(self) -> str:
        """Map the detailed shape to the telemetry module's low-cardinality label."""
        if self.task_shape.has_coordination_shape:
            return "bounded_coordination"
        if self.task_shape.coding_task:
            return "single_task"
        return "unknown"

    def telemetry_context(
        self,
        *,
        actual_agent_source: Optional[str] = None,
        completion_status: Optional[str] = None,
        outcome_quality: Any = None,
        fallback_reason: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Build a stable context for logs, metrics, and memory persistence.

        Runtime callers should pass observed values after execution.  The
        optional fields are omitted when unknown, allowing this same seam to
        be used at selection time and completion time.
        """
        context: Dict[str, Any] = {
            "routing_version": ROUTING_VERSION,
            "route": self.route,
            "intended_route": self.intended_route,
            "expected_agent_source": self.intended_route,
            "classification": self.classification,
            "precedence": self.precedence,
            "reason": self.reason,
            "matched_signals": list(self.matched_signals),
            "signal_scores": dict(self.signal_scores),
            "task_shape": self.task_shape.to_dict(),
            "task_shape_label": self.task_shape_label,
            "fallback_route": self.fallback_route,
        }
        if actual_agent_source is not None:
            context["actual_agent_source"] = str(actual_agent_source)
        if completion_status is not None:
            context["completion_status"] = str(completion_status)
        if outcome_quality is not None:
            context["outcome_quality"] = outcome_quality
        if fallback_reason is not None:
            context["fallback_reason"] = str(fallback_reason)
        return context


def _score_signals(prompt: str) -> Tuple[Dict[str, int], Dict[str, Tuple[str, ...]]]:
    scores: Dict[str, int] = {}
    matches: Dict[str, Tuple[str, ...]] = {}
    for name in _SIGNAL_NAMES:
        labels = tuple(
            label
            for label, pattern in _SIGNAL_PATTERNS[name]
            if re.search(pattern, prompt, re.IGNORECASE)
        )
        scores[name] = len(labels)
        if labels:
            matches[name] = labels
    return scores, matches


def classify_task_shape(prompt: str) -> TaskShape:
    """Extract deterministic task-shape signals without retaining prompt text."""
    text = str(prompt or "")
    scores, matches = _score_signals(text)
    return TaskShape(
        decomposition=scores["decomposition"] > 0,
        bounded_scope=scores["bounded_scope"] > 0,
        dependency_coordination=scores["dependency_coordination"] > 0,
        explicit_orchestration=scores["explicit_orchestration"] > 0,
        needs_parallel_children=scores["needs_parallel_children"] > 0,
        coding_task=scores["coding_task"] > 0,
        matches=matches,
    )


def _is_ambiguous(text: str, shape: TaskShape) -> bool:
    if any(pattern.search(text) for pattern in _AMBIGUOUS_PATTERNS):
        return True
    # Mixed intent without enough coordination evidence is ambiguous even
    # when neither side contains an explicit directive.
    return shape.coding_task and shape.coordination_signals == 1


def route_task(prompt: str, *, default_route: str = ROUTE_CODEX_NATIVE) -> RoutingDecision:
    """Select Hermes or Codex-native using explicit and task-shape evidence.

    ``default_route`` is constrained to the two supported lanes.  It exists
    for callers that already have a configured safe default, while the normal
    Hermes default remains Codex-native for backwards-compatible behavior.
    """
    if default_route not in {ROUTE_HERMES, ROUTE_CODEX_NATIVE}:
        raise ValueError(
            f"default_route must be {ROUTE_HERMES!r} or {ROUTE_CODEX_NATIVE!r}"
        )

    text = str(prompt or "")
    shape = classify_task_shape(text)
    scores = {name: 0 for name in _SIGNAL_NAMES}
    scores.update({name: len(labels) for name, labels in shape.matches.items()})
    matched = tuple(name for name in _SIGNAL_NAMES if scores[name] > 0)

    explicit_hermes = bool(_EXPLICIT_HERMES.search(text))
    explicit_codex = bool(_EXPLICIT_CODEX.search(text))
    if explicit_hermes or explicit_codex:
        route = ROUTE_HERMES if explicit_hermes and not explicit_codex else ROUTE_CODEX_NATIVE
        # If both directives occur, Codex-native is the safer deterministic
        # choice: it is the narrower execution lane and avoids fan-out.
        return RoutingDecision(
            route=route,
            task_shape=shape,
            classification="explicit",
            precedence="explicit_directive",
            reason=(
                "explicit Hermes directive"
                if route == ROUTE_HERMES
                else "explicit Codex-native directive"
            ),
            matched_signals=matched,
            signal_scores=scores,
            fallback_route=default_route,
        )

    if shape.has_coordination_shape:
        return RoutingDecision(
            route=ROUTE_HERMES,
            task_shape=shape,
            classification="hermes_positive",
            precedence="hermes_task_shape",
            reason="multiple coordination signals",
            matched_signals=matched,
            signal_scores=scores,
            fallback_route=default_route,
        )

    if shape.coding_task:
        return RoutingDecision(
            route=ROUTE_CODEX_NATIVE,
            task_shape=shape,
            classification="codex_native",
            precedence="codex_native_task_shape",
            reason="focused coding or repository work",
            matched_signals=matched,
            signal_scores=scores,
            fallback_route=default_route,
        )

    if _is_ambiguous(text, shape):
        return RoutingDecision(
            route=default_route,
            task_shape=shape,
            classification="ambiguous",
            precedence="safe_default",
            reason="insufficient task-shape evidence",
            matched_signals=matched,
            signal_scores=scores,
            fallback_route=default_route,
        )

    return RoutingDecision(
        route=default_route,
        task_shape=shape,
        classification="fallback",
        precedence="safe_default",
        reason="no routing signals",
        matched_signals=matched,
        signal_scores=scores,
        fallback_route=default_route,
    )


# Compatibility-friendly names for callers integrating the seam.
select_agent = route_task
classify_prompt = classify_task_shape

__all__ = [
    "ROUTE_CODEX_NATIVE",
    "ROUTE_HERMES",
    "ROUTING_VERSION",
    "RoutingDecision",
    "TaskShape",
    "classify_prompt",
    "classify_task_shape",
    "route_task",
    "select_agent",
]
