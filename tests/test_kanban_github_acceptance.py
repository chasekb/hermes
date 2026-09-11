from __future__ import annotations

import json

from hermes_cli.kanban_github import validate_published_pr


PR_URL = "https://github.com/chasekb/trade/pull/63"
HEAD = "c525217404ccfffce91128725f36a1881be290b6"
MERGE = "d" * 40


def test_acceptance_retries_first_read_and_preserves_evidence():
    metadata = {
        "published_pr": PR_URL,
        "pr_head_sha": HEAD,
        "merge_sha": MERGE,
        "required_checks": [{"name": "verification"}],
        "terminal_run": {"id": 34584147928},
    }
    pr = {
        "state": "closed",
        "merged_at": "2026-09-11T00:00:00Z",
        "head": {"sha": HEAD},
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
