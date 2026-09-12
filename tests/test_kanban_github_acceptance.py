from __future__ import annotations

import json

from hermes_cli.kanban_github import validate_published_pr


PR_URL = "https://github.com/chasekb/trade/pull/63"
HEAD = "c525217404ccfffce91128725f36a1881be290b6"
MERGE = "d" * 40


def test_acceptance_retries_first_read_and_preserves_evidence():
    metadata = {
        "acceptance_mode": "merged_pr",
        "published_pr": PR_URL,
        "pr_head_sha": HEAD,
        "merge_sha": MERGE,
        "required_checks": [{"name": "verification"}],
        "terminal_run": {"id": 34584147928},
    }
    pr = {
        "state": "closed",
        "number": 63,
        "merged_at": "2026-09-11T00:00:00Z",
        "head": {"sha": HEAD},
        "base": {"repo": {"full_name": "chasekb/trade"}},
        "merge_commit_sha": MERGE,
    }
    checks = {"check_runs": [{"name": "verification", "conclusion": "success"}]}
    run = {"head_sha": HEAD, "status": "completed", "conclusion": "success"}
    jobs = {"jobs": [{"id": 1, "name": "verification", "conclusion": "success"}]}
    responses = [
        (1, "", "temporary GitHub failure"),
        *[(0, json.dumps(value), "") for value in (pr, checks, run, jobs) * 2],
    ]
    calls = []

    def runner(argv, env, cwd):
        calls.append((tuple(argv), dict(env), cwd))
        return responses.pop(0)

    enriched = validate_published_pr(metadata, env={"GH_TOKEN": "redacted"}, runner=runner)

    assert enriched["published_pr"] == PR_URL
    assert enriched["github_acceptance"]["pr_head_sha"] == HEAD
    assert enriched["github_acceptance"]["merge_sha"] == MERGE
    assert enriched["github_acceptance"]["terminal_run"]["id"] == 34584147928
    assert len(calls) == 9
    assert all(call[0][:4] == ("gh", "api", "--hostname", "github.com") for call in calls)
    assert all(call[1] == {"GH_TOKEN": "redacted"} for call in calls)


def test_kanban_complete_uses_verified_metadata_before_transition(monkeypatch):
    import tools.kanban_tools as kanban_tools

    captured = {}

    class FakeRun:
        id = 7

    class FakeConn:
        def close(self):
            pass

    class FakeDb:
        class HallucinatedCardsError(ValueError):
            phantom = []

        @staticmethod
        def complete_task(conn, tid, **kwargs):
            captured.update(kwargs)
            return True

        @staticmethod
        def latest_run(conn, tid):
            return FakeRun()

    monkeypatch.setenv("HERMES_KANBAN_TASK", "t_worker")
    monkeypatch.setattr(kanban_tools, "_connect", lambda board=None: (FakeDb, FakeConn()))
    monkeypatch.setattr(
        kanban_tools,
        "validate_published_pr",
        lambda metadata, **kwargs: {**metadata, "github_acceptance": {"verified": True}},
    )

    result = kanban_tools._handle_complete(
        {
            "task_id": "t_worker",
            "summary": "verified",
            "metadata": {"published_pr": PR_URL},
        }
    )

    assert json.loads(result)["ok"] is True
    assert captured["metadata"]["github_acceptance"] == {"verified": True}


def _exact_metadata():
    return {
        "acceptance_mode": "exact_sha_workflow_run",
        "published_pr": PR_URL,
        "exact_sha": HEAD,
        "required_checks": [{"name": "verification"}],
        "terminal_run": {"id": 34584147928},
    }


def _exact_responses(*, run_sha=HEAD, jobs=None, state="open", check_conclusion="success"):
    pr = {
        "state": state,
        "number": 63,
        "head": {"sha": HEAD},
        "base": {"repo": {"full_name": "chasekb/trade"}},
    }
    checks = {"check_runs": [{"name": "verification", "conclusion": check_conclusion}]}
    run = {
        "head_sha": run_sha,
        "event": "workflow_dispatch",
        "status": "completed",
        "conclusion": "success",
    }
    job_rows = jobs if jobs is not None else [{"id": 1, "name": "verification", "conclusion": "success"}]
    return [
        (0, json.dumps(value), "")
        for value in (pr, checks, run, {"jobs": job_rows}) * 2
    ]


def test_exact_sha_workflow_dispatch_accepts_open_pr():
    responses = _exact_responses()
    enriched = validate_published_pr(_exact_metadata(), runner=lambda *args: responses.pop(0))
    assert enriched["github_acceptance"]["acceptance_mode"] == "exact_sha_workflow_run"
    assert enriched["github_acceptance"]["merge_sha"] is None


def test_exact_sha_rejects_mismatched_run_sha():
    responses = _exact_responses(run_sha="e" * 40)
    try:
        validate_published_pr(_exact_metadata(), runner=lambda *args: responses.pop(0))
    except ValueError as exc:
        assert "run_read:head_mismatch" in str(exc)
    else:
        raise AssertionError("mismatched workflow run SHA was accepted")


def test_exact_sha_rejects_failed_job():
    responses = _exact_responses(jobs=[{"id": 1, "name": "verification", "conclusion": "failure"}])
    try:
        validate_published_pr(_exact_metadata(), runner=lambda *args: responses.pop(0))
    except ValueError as exc:
        assert "run_read:job_not_successful" in str(exc)
    else:
        raise AssertionError("failed workflow job was accepted")


def test_exact_sha_rejects_missing_acceptance_mode():
    metadata = _exact_metadata()
    metadata.pop("acceptance_mode")
    try:
        validate_published_pr(metadata, runner=lambda *args: (0, "{}", ""))
    except ValueError as exc:
        assert "input:acceptance_mode_invalid" in str(exc)
    else:
        raise AssertionError("exact-SHA metadata without a mode was accepted")


def test_exact_sha_rejects_inconsistent_second_read():
    responses = _exact_responses()
    responses[4] = (0, json.dumps({"state": "closed", "head": {"sha": HEAD}, "base": {"repo": {"full_name": "chasekb/trade"}}}), "")
    try:
        validate_published_pr(_exact_metadata(), runner=lambda *args: responses.pop(0))
    except ValueError as exc:
        assert "pr_read:not_merged" in str(exc)
    else:
        raise AssertionError("inconsistent second read was accepted")


def test_kanban_complete_exact_mode_uses_real_validator_before_db(monkeypatch):
    import tools.kanban_tools as kanban_tools

    import hermes_cli.kanban_github as github

    captured = {}

    class FakeRun:
        id = 8

    class FakeConn:
        def close(self):
            pass

    class FakeDb:
        class HallucinatedCardsError(ValueError):
            phantom = []

        @staticmethod
        def complete_task(conn, tid, **kwargs):
            captured.update(kwargs)
            return True

        @staticmethod
        def latest_run(conn, tid):
            return FakeRun()

    responses = [(1, "", "transient")] + _exact_responses()
    monkeypatch.setattr(github, "_default_runner", lambda *args: responses.pop(0))
    monkeypatch.setenv("HERMES_KANBAN_TASK", "t_worker")
    monkeypatch.setattr(kanban_tools, "_connect", lambda board=None: (FakeDb, FakeConn()))

    result = kanban_tools._handle_complete(
        {
            "task_id": "t_worker",
            "summary": "verified exact workflow",
            "metadata": _exact_metadata(),
        }
    )

    assert json.loads(result)["ok"] is True
    assert captured["metadata"]["github_acceptance"]["pr_state"] == "open"


def test_kanban_complete_rejects_exact_evidence_before_db_mutation(monkeypatch):
    import tools.kanban_tools as kanban_tools

    import hermes_cli.kanban_github as github

    responses = _exact_responses(run_sha="e" * 40)
    monkeypatch.setattr(github, "_default_runner", lambda *args: responses.pop(0))
    monkeypatch.setenv("HERMES_KANBAN_TASK", "t_worker")

    def unexpected_db_connect(board=None):
        raise AssertionError("DB connection attempted after rejected GitHub evidence")

    monkeypatch.setattr(kanban_tools, "_connect", unexpected_db_connect)
    result = kanban_tools._handle_complete(
        {
            "task_id": "t_worker",
            "summary": "should remain in flight",
            "metadata": _exact_metadata(),
        }
    )

    assert json.loads(result)["ok"] is False
    assert "GitHub acceptance evidence unavailable" in result


def _run_completion_with_real_validator(monkeypatch, responses, metadata):
    import tools.kanban_tools as kanban_tools
    import hermes_cli.kanban_github as github

    calls = []

    class FakeRun:
        id = 9

    class FakeConn:
        def close(self):
            pass

    class FakeDb:
        class HallucinatedCardsError(ValueError):
            phantom = []

        @staticmethod
        def complete_task(conn, tid, **kwargs):
            calls.append((tid, kwargs))
            return True

        @staticmethod
        def latest_run(conn, tid):
            return FakeRun()

    monkeypatch.setenv("HERMES_KANBAN_TASK", "t_worker")
    monkeypatch.setattr(github, "_default_runner", lambda *args: responses.pop(0))
    monkeypatch.setattr(kanban_tools, "_connect", lambda board=None: (FakeDb, FakeConn()))
    result = kanban_tools._handle_complete(
        {
            "task_id": "t_worker",
            "summary": "boundary evidence",
            "metadata": metadata,
        }
    )
    return json.loads(result), calls


def test_kanban_complete_rejects_failed_job_before_db_transition(monkeypatch):
    result, calls = _run_completion_with_real_validator(
        monkeypatch,
        _exact_responses(jobs=[{"id": 1, "name": "verification", "conclusion": "failure"}]),
        _exact_metadata(),
    )
    assert result["ok"] is False
    assert calls == []


def test_kanban_complete_rejects_pending_run_before_db_transition(monkeypatch):
    responses = _exact_responses()
    responses[2] = (
        0,
        json.dumps(
            {
                "head_sha": HEAD,
                "event": "workflow_dispatch",
                "status": "in_progress",
                "conclusion": None,
            }
        ),
        "",
    )
    result, calls = _run_completion_with_real_validator(
        monkeypatch, responses, _exact_metadata()
    )
    assert result["ok"] is False
    assert calls == []


def test_kanban_complete_rejects_inconsistent_second_read_before_db_transition(monkeypatch):
    responses = _exact_responses()
    responses[4] = (
        0,
        json.dumps(
            {
                "state": "closed",
                "number": 63,
                "head": {"sha": HEAD},
                "base": {"repo": {"full_name": "chasekb/trade"}},
            }
        ),
        "",
    )
    result, calls = _run_completion_with_real_validator(
        monkeypatch, responses, _exact_metadata()
    )
    assert result["ok"] is False
    assert calls == []


def test_kanban_complete_accepts_unchanged_merged_pr_before_db_transition(monkeypatch):
    metadata = {
        "acceptance_mode": "merged_pr",
        "published_pr": PR_URL,
        "pr_head_sha": HEAD,
        "merge_sha": MERGE,
        "required_checks": [{"name": "verification"}],
        "terminal_run": {"id": 34584147928},
    }
    pr = {
        "state": "closed",
        "number": 63,
        "merged_at": "2026-09-11T00:00:00Z",
        "head": {"sha": HEAD},
        "base": {"repo": {"full_name": "chasekb/trade"}},
        "merge_commit_sha": MERGE,
    }
    checks = {"check_runs": [{"name": "verification", "conclusion": "success"}]}
    run = {
        "head_sha": HEAD,
        "status": "completed",
        "conclusion": "success",
        "event": "push",
    }
    jobs = {"jobs": [{"id": 1, "name": "verification", "conclusion": "success"}]}
    responses = [
        (0, json.dumps(value), "")
        for value in (pr, checks, run, jobs) * 2
    ]
    result, calls = _run_completion_with_real_validator(monkeypatch, responses, metadata)
    assert result["ok"] is True
    assert len(calls) == 1
    assert calls[0][1]["metadata"]["github_acceptance"]["merge_sha"] == MERGE
