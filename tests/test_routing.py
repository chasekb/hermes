import json

from agent.routing import (
    ROUTE_CODEX_NATIVE,
    ROUTE_HERMES,
    RoutingDecision,
    classify_task_shape,
    route_task,
)


def test_bounded_parallel_dependency_work_routes_to_hermes():
    decision = route_task(
        "Decompose this bounded migration into three child tasks, run independent "
        "checks in parallel, and coordinate dependencies before the final fan-in."
    )

    assert decision.route == ROUTE_HERMES
    assert decision.task_shape.coordination_signals >= 2
    assert decision.task_shape.needs_parallel_children is True
    assert "task_shape" in decision.telemetry_context()


def test_explicit_hermes_directive_is_honored():
    decision = route_task("Use the Hermes lane for this bounded workflow.")

    assert decision.route == ROUTE_HERMES
    assert decision.classification == "explicit"
    assert decision.precedence == "explicit_directive"


def test_single_repo_edit_routes_to_codex_native():
    decision = route_task(
        "Fix the null check in src/parser.py, add a focused regression test, and "
        "return the patch."
    )

    assert decision.route == ROUTE_CODEX_NATIVE
    assert decision.task_shape.coding_task is True
    assert decision.task_shape.coordination_signals == 1


def test_explicit_directive_wins_over_conflicting_task_shape():
    decision = route_task(
        "Use the Codex-native lane only. Even though this needs decomposition and "
        "parallel child workers, keep it in Codex."
    )

    assert decision.route == ROUTE_CODEX_NATIVE
    assert decision.precedence == "explicit_directive"
    assert decision.task_shape.needs_parallel_children is True


def test_ambiguous_prompt_uses_deterministic_codex_fallback():
    decision = route_task("Review the deployment approach and suggest improvements.")

    assert decision.route == ROUTE_CODEX_NATIVE
    assert decision.classification == "ambiguous"
    assert decision.precedence == "safe_default"
    assert decision.telemetry_context()["classification"] == "ambiguous"


def test_no_signal_prompt_is_marked_fallback():
    decision = route_task("Tell me a short joke about databases.")

    assert decision.route == ROUTE_CODEX_NATIVE
    assert decision.classification == "fallback"
    assert decision.reason == "no routing signals"


def test_task_shape_exposes_stable_signal_names():
    shape = classify_task_shape(
        "Orchestrate a bounded workflow: split the work, then run child tasks "
        "after their dependencies complete."
    )

    assert shape.to_dict() == {
        "bounded_scope": True,
        "coding_task": False,
        "dependency_coordination": True,
        "explicit_orchestration": True,
        "needs_parallel_children": False,
        "decomposition": True,
        "coordination_signals": 4,
    }


def test_decision_context_is_json_safe_and_contains_match_details():
    context = route_task("Implement a focused parser fix in one file.").telemetry_context()

    assert isinstance(context, dict)
    assert context["route"] == ROUTE_CODEX_NATIVE
    assert context["matched_signals"]
    assert context["signal_scores"]["coding_task"] >= 1
    assert isinstance(context["task_shape"], dict)
    json.dumps(context)
    assert isinstance(RoutingDecision, type)


def test_decision_context_accepts_observed_outcome_fields():
    context = route_task("Decompose this bounded workflow and coordinate dependencies.").telemetry_context(
        actual_agent_source="default_fallback",
        completion_status="timeout",
        outcome_quality="poor",
        fallback_reason="timeout",
    )

    assert context["intended_route"] == ROUTE_HERMES
    assert context["expected_agent_source"] == ROUTE_HERMES
    assert context["actual_agent_source"] == "default_fallback"
    assert context["completion_status"] == "timeout"
    assert context["outcome_quality"] == "poor"
    assert context["fallback_reason"] == "timeout"
    assert context["task_shape_label"] == "bounded_coordination"
    assert route_task("Decompose this bounded workflow and coordinate dependencies.").task_shape_label == "bounded_coordination"
