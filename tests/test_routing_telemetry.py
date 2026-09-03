import json
import sys
from types import SimpleNamespace

from agent import routing_telemetry


def test_metrics_capture_selection_fallback_and_failed_outcome(tmp_path, monkeypatch):
    events_path = tmp_path / "routing-events.jsonl"
    monkeypatch.setattr(routing_telemetry, "_events_path", lambda: events_path)
    routing_telemetry.reset_metrics_for_tests()

    routing_telemetry.record_routing_decision(
        request_id="request-hermes",
        route_intent="hermes",
        selected_agent_source="hermes",
        task_shape="bounded_coordination",
    )
    routing_telemetry.record_routing_outcome(
        request_id="request-hermes",
        selected_agent_source="hermes",
        outcome="completed",
        outcome_quality="good",
    )
    routing_telemetry.record_routing_decision(
        request_id="request-fallback",
        route_intent="hermes",
        selected_agent_source="default_fallback",
        fallback=True,
        fallback_reason="unavailable",
        task_shape="bounded_coordination",
    )
    routing_telemetry.record_routing_outcome(
        request_id="request-fallback",
        selected_agent_source="default_fallback",
        outcome="failed",
        outcome_quality="poor",
    )

    metrics = routing_telemetry.get_routing_metrics(events_path)

    assert metrics["decisions_total"] == 2
    assert metrics["hermes_selections_total"] == 1
    assert metrics["fallbacks_total"] == 1
    assert metrics["outcomes_total"] == 2
    assert metrics["outcome_quality_known_total"] == 2
    assert metrics["outcome_quality_good_total"] == 1
    assert metrics["selection_rate"] == 0.5
    assert metrics["fallback_rate"] == 0.5
    assert metrics["outcome_quality_rate"] == 0.5
    assert {event["event"] for event in _read_events(events_path)} == {
        "routing_decision",
        "routing_outcome",
    }


def test_telemetry_failure_does_not_break_routing(monkeypatch):
    def fail(*args, **kwargs):
        raise OSError("telemetry unavailable")

    monkeypatch.setattr(routing_telemetry, "_write_event", fail)
    assert routing_telemetry.record_routing_decision(
        request_id="request-safe",
        route_intent="hermes",
        selected_agent_source="hermes",
    ) is None
    assert routing_telemetry.record_routing_outcome(
        request_id="request-safe",
        selected_agent_source="hermes",
        outcome="completed",
    ) is None


def test_normalize_outcome_marks_failed_path_as_poor():
    assert routing_telemetry.normalize_outcome("error") == ("failed", "poor")
    assert routing_telemetry.normalize_outcome("timeout") == ("timeout", "poor")
    assert routing_telemetry.normalize_outcome("completed") == ("completed", "unknown")


def test_decision_context_adapter_preserves_task_shape_and_fallback():
    event = routing_telemetry.record_routing_decision_from_context(
        {
            "route": "hermes",
            "intended_route": "hermes",
            "classification": "hermes_positive",
            "task_shape_label": "bounded_coordination",
        },
        request_id="request-context",
    )

    assert event is not None
    assert event["route_intent"] == "hermes"
    assert event["selected_agent_source"] == "hermes"
    assert event["task_shape"] == "bounded_coordination"
    assert event["fallback"] is False


def test_delegate_child_emits_terminal_outcome_for_success_and_failure(tmp_path, monkeypatch):
    from tools import delegate_tool

    events_path = tmp_path / "routing-events.jsonl"
    monkeypatch.setattr(routing_telemetry, "_events_path", lambda: events_path)
    routing_telemetry.reset_metrics_for_tests()

    class FakeChild:
        tool_progress_callback = None
        _credential_pool = None
        _delegate_depth = 1
        _delegate_role = "leaf"
        _routing_request_id = "child-success"
        _routing_selected_source = "hermes"
        session_prompt_tokens = 0
        session_completion_tokens = 0
        session_estimated_cost_usd = 0.0

        def get_activity_summary(self):
            return {"api_call_count": 1, "current_tool": None, "max_iterations": 1}

        def run_conversation(self, **kwargs):
            return {"final_response": "done", "completed": True, "interrupted": False, "api_calls": 1}

        def close(self):
            return None

    parent = SimpleNamespace(session_id="parent")
    success = delegate_tool._run_single_child(0, "success", FakeChild(), parent)
    assert success["status"] == "completed"

    failed_child = FakeChild()
    failed_child._routing_request_id = "child-failure"
    failed_child.run_conversation = lambda **kwargs: {
        "final_response": "", "completed": False, "interrupted": False, "api_calls": 1
    }
    failed = delegate_tool._run_single_child(1, "failure", failed_child, parent)
    assert failed["status"] == "failed"

    metrics = routing_telemetry.get_routing_metrics(events_path)
    assert metrics["outcomes_total"] == 2
    assert metrics["outcome_quality_good_total"] == 1
    assert metrics["outcome_quality_rate"] == 0.5


def test_conversation_entrypoint_emits_route_and_terminal_outcome(tmp_path, monkeypatch):
    from agent import conversation_loop

    events_path = tmp_path / "routing-events.jsonl"
    monkeypatch.setattr(routing_telemetry, "_events_path", lambda: events_path)
    routing_telemetry.reset_metrics_for_tests()
    monkeypatch.setattr(
        conversation_loop,
        "_run_conversation",
        lambda agent, user_message, *args, **kwargs: {
            "final_response": "done",
            "completed": True,
            "interrupted": False,
        },
    )

    result = conversation_loop.run_conversation(
        SimpleNamespace(
            session_id="session-entrypoint",
            provider="openrouter",
            api_mode="chat_completions",
        ),
        "bounded coordination request",
        task_id="request-entrypoint",
    )

    assert result["completed"] is True
    events = _read_events(events_path)
    assert [event["event"] for event in events] == [
        "routing_decision",
        "routing_outcome",
    ]
    assert events[0]["selected_agent_source"] == "hermes"
    assert events[1]["outcome"] == "completed"
    assert events[1]["outcome_quality"] == "good"


def test_conversation_entrypoint_emits_task_shape_routing_context(tmp_path, monkeypatch):
    from agent import conversation_loop

    events_path = tmp_path / "routing-events.jsonl"
    monkeypatch.setattr(routing_telemetry, "_events_path", lambda: events_path)
    routing_telemetry.reset_metrics_for_tests()
    monkeypatch.setattr(
        conversation_loop,
        "_run_conversation",
        lambda agent, user_message, *args, **kwargs: {
            "final_response": "delegated",
            "completed": True,
            "interrupted": False,
        },
    )

    conversation_loop.run_conversation(
        SimpleNamespace(
            session_id="session-shaped",
            provider="openrouter",
            api_mode="chat_completions",
        ),
        "Decompose this bounded workflow and coordinate dependencies in parallel.",
        task_id="request-shaped",
    )

    event = _read_events(events_path)[0]
    assert event["route_intent"] == "hermes"
    assert event["selected_agent_source"] == "hermes"
    assert event["task_shape"] == "bounded_coordination"
    assert event["classification"] == "hermes_positive"
    assert "decomposition" in event["matched_signals"]
    assert "dependency_coordination" in event["matched_signals"]


def test_production_conversation_entrypoint_smoke_routes_bounded_coordination_to_hermes(
    tmp_path, monkeypatch
):
    """A realistic turn must complete through Hermes with runtime evidence."""
    from agent import conversation_loop

    events_path = tmp_path / "routing-events.jsonl"
    monkeypatch.setattr(routing_telemetry, "_events_path", lambda: events_path)
    routing_telemetry.reset_metrics_for_tests()

    memory_records = []

    class MemoryRecorder:
        @staticmethod
        def record_agent_source_outcome(**kwargs):
            memory_records.append(kwargs)

    monkeypatch.setitem(sys.modules, "agent.agent_source_memory", MemoryRecorder)
    monkeypatch.setattr(
        conversation_loop,
        "_run_conversation",
        lambda agent, user_message, *args, **kwargs: {
            "final_response": "All bounded child checks completed.",
            "completed": True,
            "interrupted": False,
        },
    )

    prompt = (
        "Decompose this bounded coordination workflow into two child tasks, run "
        "independent checks in parallel, then coordinate dependencies for the "
        "final fan-in. Keep execution within this test's scope."
    )
    result = conversation_loop.run_conversation(
        SimpleNamespace(
            session_id="session-e2e-routing",
            provider="openrouter",
            api_mode="chat_completions",
        ),
        prompt,
        task_id="request-e2e-routing",
    )

    assert result["completed"] is True
    assert result["final_response"]
    events = _read_events(events_path)
    decision, outcome = events
    assert decision["selected_agent_source"] == "hermes"
    assert decision["route_intent"] == "hermes"
    assert decision["task_shape"] == "bounded_coordination"
    assert decision["fallback"] is False
    assert "decomposition" in decision["matched_signals"]
    assert "dependency_coordination" in decision["matched_signals"]
    assert outcome["selected_agent_source"] == "hermes"
    assert outcome["outcome"] == "completed"
    assert outcome["outcome_quality"] == "good"
    assert routing_telemetry.get_routing_metrics(events_path)["fallbacks_total"] == 0
    assert memory_records and memory_records[0]["actual_agent_source"] == "hermes"
    assert memory_records[0]["completion_status"] == "completed"


def test_safe_default_classification_is_not_counted_as_provider_fallback(tmp_path, monkeypatch):
    from agent import conversation_loop

    events_path = tmp_path / "routing-events.jsonl"
    monkeypatch.setattr(routing_telemetry, "_events_path", lambda: events_path)
    routing_telemetry.reset_metrics_for_tests()
    monkeypatch.setattr(
        conversation_loop,
        "_run_conversation",
        lambda agent, user_message, *args, **kwargs: {
            "final_response": "hello",
            "completed": True,
            "interrupted": False,
        },
    )

    conversation_loop.run_conversation(
        SimpleNamespace(
            session_id="session-default",
            provider="openrouter",
            api_mode="chat_completions",
        ),
        "Hello there.",
        task_id="request-default",
    )

    event = _read_events(events_path)[0]
    assert event["classification"] == "fallback"
    assert event["selected_agent_source"] == "hermes"
    assert event["fallback"] is False
    assert routing_telemetry.get_routing_metrics(events_path)["fallback_rate"] == 0.0


def test_conversation_entrypoint_records_failed_exception_without_masking_it(tmp_path, monkeypatch):
    from agent import conversation_loop

    events_path = tmp_path / "routing-events.jsonl"
    monkeypatch.setattr(routing_telemetry, "_events_path", lambda: events_path)
    routing_telemetry.reset_metrics_for_tests()

    def fail(*args, **kwargs):
        raise RuntimeError("provider failed")

    monkeypatch.setattr(conversation_loop, "_run_conversation", fail)

    try:
        conversation_loop.run_conversation(
            SimpleNamespace(
                session_id="session-failure",
                provider="openai-codex",
                api_mode="codex_responses",
            ),
            "request",
            task_id="request-failure",
        )
    except RuntimeError as exc:
        assert str(exc) == "provider failed"
    else:
        raise AssertionError("conversation failure was swallowed")

    events = _read_events(events_path)
    assert events[0]["selected_agent_source"] == "codex_native"
    assert events[1]["outcome"] == "failed"
    assert events[1]["outcome_quality"] == "poor"


def test_fallback_selection_records_actual_codex_native_source(tmp_path, monkeypatch):
    from agent import chat_completion_helpers
    from agent.error_classifier import FailoverReason

    events_path = tmp_path / "routing-events.jsonl"
    monkeypatch.setattr(routing_telemetry, "_events_path", lambda: events_path)
    routing_telemetry.reset_metrics_for_tests()

    chat_completion_helpers._record_fallback_selection(
        SimpleNamespace(
            provider="openai-codex",
            model="gpt-5.3-codex",
            session_id="session-fallback",
        ),
        reason=FailoverReason.rate_limit,
        fallback_index=0,
    )

    event = _read_events(events_path)[0]
    assert event["event"] == "routing_decision"
    assert event["route_intent"] == "codex_native"
    assert event["selected_agent_source"] == "codex_native"
    assert event["fallback"] is True
    assert event["fallback_reason"] == "rate_limit"


def test_codex_native_fallback_keeps_codex_native_route_intent(tmp_path, monkeypatch):
    from agent import chat_completion_helpers
    from agent.error_classifier import FailoverReason

    events_path = tmp_path / "routing-events.jsonl"
    monkeypatch.setattr(routing_telemetry, "_events_path", lambda: events_path)
    routing_telemetry.reset_metrics_for_tests()

    chat_completion_helpers._record_fallback_selection(
        SimpleNamespace(
            provider="openai-codex",
            model="gpt-5.3-codex",
            session_id="session-codex-fallback",
            _primary_runtime={"provider": "openai-codex", "api_mode": "codex_responses"},
        ),
        reason=FailoverReason.rate_limit,
        fallback_index=0,
    )

    event = _read_events(events_path)[0]
    assert event["route_intent"] == "codex_native"
    assert event["selected_agent_source"] == "codex_native"
    assert event["fallback"] is True


def _read_events(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line]
