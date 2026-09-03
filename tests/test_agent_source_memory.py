import json
from pathlib import Path

from agent.agent_source_memory import (
    read_agent_source_outcomes,
    record_agent_source_outcome_for_agent,
    record_agent_source_outcome,
)
from agent.memory_manager import MemoryManager
from agent.memory_provider import MemoryProvider


class RecordingProvider(MemoryProvider):
    def __init__(self):
        self.outcomes = []

    @property
    def name(self):
        return "recording"

    def is_available(self):
        return True

    def initialize(self, session_id, **kwargs):
        pass

    def get_tool_schemas(self):
        return []

    def on_agent_source_outcome(self, outcome):
        self.outcomes.append(outcome)


def test_persists_redacted_outcome_in_decision_memory(tmp_path):
    path = tmp_path / "backlog" / "decision-memory.json"

    result = record_agent_source_outcome(
        store_path=path,
        intended_route="hermes",
        actual_agent_source="hermes",
        request_class="bounded_coordination",
        completion_status="completed",
        outcome_quality="high",
        prompt="private prompt with API_KEY=do-not-store",
        session_id="session-123",
    )

    assert result["actual_agent_source"] == "hermes"
    assert result["prompt_sha"]
    stored = json.loads(path.read_text())
    record = stored["records"][-1]
    assert record["timestamp"] == record["ts"]
    assert record["expected"] == "hermes"
    assert record["observed"] == "hermes"
    assert record["prompt_class"] == "bounded_coordination"
    assert record["completion_status"] == "completed"
    assert record["outcome_quality"] == "high"
    assert record["redacted"] is True
    assert "private prompt" not in path.read_text()
    assert "API_KEY" not in path.read_text()


def test_memory_manager_forwards_outcome_to_provider(tmp_path):
    provider = RecordingProvider()
    manager = MemoryManager()
    manager.add_provider(provider)

    outcome = record_agent_source_outcome(
        store_path=tmp_path / "decision-memory.json",
        intended_route="hermes",
        actual_agent_source="codex_native",
        request_class="repo_implementation",
        completion_status="completed",
        outcome_quality="fallback_success",
        memory_manager=manager,
    )

    assert provider.outcomes == [outcome]
    assert outcome["actual_agent_source"] == "codex_native"


def test_record_keeps_routing_telemetry_aliases_and_explicit_fallback(tmp_path):
    outcome = record_agent_source_outcome(
        store_path=tmp_path / "decision-memory.json",
        intended_route="hermes",
        actual_agent_source="hermes",
        fallback=True,
        request_class="bounded_coordination",
        completion_status="completed",
        outcome_quality="fallback_success",
    )

    assert outcome["route_intent"] == "hermes"
    assert outcome["agent_source"] == "hermes"
    assert outcome["request_count"] == 1
    assert outcome["fallback"] is True


def test_memory_observer_cannot_mutate_durable_record(tmp_path):
    class MutatingObserver:
        def on_agent_source_outcome(self, outcome):
            outcome["prompt"] = "secret prompt injected by observer"

    path = tmp_path / "decision-memory.json"
    outcome = record_agent_source_outcome(
        store_path=path,
        memory_manager=MutatingObserver(),
        intended_route="hermes",
        actual_agent_source="hermes",
        request_class="bounded_coordination",
        completion_status="completed",
        outcome_quality="high",
    )

    assert "prompt" not in outcome
    assert "secret prompt" not in path.read_text()


def test_persistence_failures_are_non_fatal(tmp_path):
    # A directory is not a writable JSON file, so the persistence path fails.
    result = record_agent_source_outcome(
        store_path=tmp_path,
        intended_route="hermes",
        actual_agent_source="hermes",
        request_class="bounded_coordination",
        completion_status="failed",
        outcome_quality="low",
    )

    assert result is None


def test_disabled_persistence_does_not_write(tmp_path):
    path = tmp_path / "decision-memory.json"

    result = record_agent_source_outcome(
        store_path=path,
        enabled=False,
        intended_route="hermes",
        actual_agent_source="hermes",
        request_class="bounded_coordination",
        completion_status="completed",
        outcome_quality="high",
    )

    assert result is None
    assert not path.exists()


def test_future_reads_filter_intended_and_actual_sources(tmp_path):
    path = tmp_path / "decision-memory.json"
    for actual in ("hermes", "codex_native"):
        record_agent_source_outcome(
            store_path=path,
            intended_route="hermes",
            actual_agent_source=actual,
            request_class="bounded_coordination",
            completion_status="completed",
            outcome_quality="high" if actual == "hermes" else "fallback_success",
        )

    records = read_agent_source_outcomes(
        path,
        intended_route="hermes",
        actual_agent_source="codex_native",
        request_class="bounded_coordination",
    )

    assert len(records) == 1
    assert records[0]["intended_route"] == "hermes"
    assert records[0]["actual_agent_source"] == "codex_native"


def test_router_context_is_persisted_without_prompt_text(tmp_path):
    path = tmp_path / "decision-memory.json"
    result = record_agent_source_outcome(
        store_path=path,
        routing_context={
            "expected_agent_source": "hermes",
            "task_shape_label": "bounded_coordination",
            "classification": "hermes_positive",
            "precedence": "task_shape",
            "reason": "coordination shape",
            "matched_signals": ["decomposition", "dependency_coordination"],
            "signal_scores": {"decomposition": 1, "dependency_coordination": 1},
            "task_shape": {"coordination_signals": 2},
        },
        actual_agent_source="hermes",
        completion_status="completed",
        outcome_quality="high",
        prompt="do not persist this request body",
    )

    assert result["expected"] == "hermes"
    assert result["request_class"] == "bounded_coordination"
    assert result["classification"] == "hermes_positive"
    assert result["task_shape"]["coordination_signals"] is True
    assert "do not persist" not in json.dumps(result)


def test_untrusted_router_explanation_is_not_persisted(tmp_path):
    result = record_agent_source_outcome(
        store_path=tmp_path / "decision-memory.json",
        routing_context={
            "expected_agent_source": "hermes",
            "task_shape_label": "bounded_coordination",
            "reason": "private prompt text must not become an explanation",
            "matched_signals": ["private prompt text"],
        },
        actual_agent_source="hermes",
        completion_status="completed",
        outcome_quality="high",
    )

    encoded = json.dumps(result)
    assert "private prompt text" not in encoded


class OutcomeAgent:
    _routing_outcomes_enabled = True
    _memory_enabled = False
    _user_profile_enabled = False
    session_id = "session-42"
    _memory_manager = None


def test_agent_turn_outcome_uses_router_context_and_result(tmp_path):
    result = record_agent_source_outcome_for_agent(
        OutcomeAgent(),
        "private coordination request",
        {
            "completed": True,
            "failed": False,
            "provider": "openai-codex",
            "agent_source": "hermes",
            "outcome_quality": "high",
            "routing_context": {
                "expected_agent_source": "hermes",
                "task_shape_label": "bounded_coordination",
                "classification": "hermes_positive",
            },
        },
        store_path=tmp_path / "decision-memory.json",
    )

    assert result["intended_route"] == "hermes"
    assert result["actual_agent_source"] == "hermes"
    assert result["request_class"] == "bounded_coordination"
    assert result["completion_status"] == "completed"
    assert "private coordination request" not in json.dumps(result)


def test_agent_turn_fallback_records_actual_source(tmp_path):
    result = record_agent_source_outcome_for_agent(
        OutcomeAgent(),
        "private fallback request",
        {
            "completed": True,
            "failed": False,
            "agent_source": "codex_native",
            "fallback": True,
            "fallback_reason": "hermes unavailable",
            "routing_context": {
                "expected_agent_source": "hermes",
                "task_shape_label": "bounded_coordination",
            },
        },
        store_path=tmp_path / "decision-memory.json",
    )

    assert result["intended_route"] == "hermes"
    assert result["actual_agent_source"] == "codex_native"
    assert result["fallback"] is True
    assert result["fallback_reason"] == "hermes_unavailable"


def test_agent_turn_memory_unavailable_is_fail_open(tmp_path):
    class BrokenMemoryAgent(OutcomeAgent):
        _routing_outcomes_enabled = True

    result = record_agent_source_outcome_for_agent(
        BrokenMemoryAgent(),
        "request containing no durable prompt text",
        {"completed": False, "failed": True},
        store_path=tmp_path,
    )

    assert result is None


def test_agent_run_conversation_persists_returned_outcome(monkeypatch, tmp_path):
    import agent.agent_source_memory as source_memory
    from run_agent import AIAgent

    agent = OutcomeAgent()
    agent.api_mode = "chat_completions"
    agent.provider = "openai-codex"
    agent.model = "test-model"
    agent._route_decision = {
        "expected_agent_source": "hermes",
        "task_shape_label": "bounded_coordination",
    }

    monkeypatch.setattr(
        "agent.conversation_loop.run_conversation",
        lambda *args, **kwargs: {
            "final_response": "done",
            "completed": True,
            "failed": False,
            "actual_agent_source": "hermes",
        },
    )
    monkeypatch.setattr(
        source_memory,
        "_default_store_path",
        lambda: tmp_path / "decision-memory.json",
    )

    result = AIAgent.run_conversation(agent, "private request")

    assert result["final_response"] == "done"
    records = read_agent_source_outcomes(tmp_path / "decision-memory.json")
    assert len(records) == 1
    assert records[0]["intended_route"] == "hermes"
    assert records[0]["actual_agent_source"] == "hermes"


def test_agent_run_conversation_ignores_recorder_failure(monkeypatch):
    from agent import agent_source_memory as source_memory
    from run_agent import AIAgent

    agent = OutcomeAgent()
    monkeypatch.setattr(
        "agent.conversation_loop.run_conversation",
        lambda *args, **kwargs: {"final_response": "still works", "completed": True},
    )

    def fail_to_record(*args, **kwargs):
        raise RuntimeError("memory backend unavailable")

    monkeypatch.setattr(source_memory, "record_agent_source_outcome_for_agent", fail_to_record)

    result = AIAgent.run_conversation(agent, "request")

    assert result["final_response"] == "still works"


def test_agent_turn_without_route_intent_is_not_marked_as_fallback(tmp_path):
    result = record_agent_source_outcome_for_agent(
        OutcomeAgent(),
        "request without an explicit routing decision",
        {"completed": True},
        store_path=tmp_path / "decision-memory.json",
    )

    assert result["intended_route"] == "hermes"
    assert result["actual_agent_source"] == "hermes"
    assert result["fallback"] is False
