"""Read-only GitHub acceptance evidence for Kanban completions.

The adapter is deliberately worker-side and fail-closed: a completion that
claims a published PR is not persisted until GitHub confirms the same PR,
commit/check data, and terminal workflow run twice.  GitHub reads are made
through the ``gh`` CLI so workers and coordinators share the configured
credential resolution without copying credential contents into the process.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import time
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Sequence
from urllib.parse import urlparse


_MAX_API_ATTEMPTS = 3
_RETRY_DELAY_SECONDS = 0.05
_PR_PATH_RE = re.compile(r"^/([^/]+)/([^/]+)/pull/(\d+)/?$")
_SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")
_MERGED_MODE = "merged_pr"
_EXACT_WORKFLOW_MODE = "exact_sha_workflow_run"


@dataclass(frozen=True)
class GitHubAcceptanceError(ValueError):
    """Sanitized, machine-readable failure from an acceptance phase."""

    phase: str
    code: str
    detail: str

    def __str__(self) -> str:
        return f"GitHub acceptance evidence unavailable or incomplete ({self.phase}:{self.code})"


Runner = Callable[[Sequence[str], Mapping[str, str], str | None], tuple[int, str, str]]


def _default_runner(
    argv: Sequence[str], env: Mapping[str, str], cwd: str | None
) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(
            list(argv),
            cwd=cwd,
            env=dict(env),
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        # Do not retain command output or exception text: it may contain auth
        # or host details from a helper process.
        return 124, "", type(exc).__name__
    return proc.returncode, proc.stdout, proc.stderr


def _parse_pr_url(value: Any) -> tuple[str, str, int]:
    if not isinstance(value, str) or not value.strip():
        raise GitHubAcceptanceError("input", "published_pr_invalid", "missing URL")
    parsed = urlparse(value.strip())
    if parsed.scheme != "https" or parsed.netloc.lower() != "github.com":
        raise GitHubAcceptanceError("input", "published_pr_invalid", "unsupported URL")
    match = _PR_PATH_RE.fullmatch(parsed.path)
    if not match:
        raise GitHubAcceptanceError("input", "published_pr_invalid", "unsupported URL")
    return match.group(1), match.group(2), int(match.group(3))


def _sha(value: Any, field: str) -> str:
    if not isinstance(value, str) or not _SHA_RE.fullmatch(value):
        raise GitHubAcceptanceError("input", f"{field}_invalid", "invalid SHA")
    return value.lower()


def _request_json(
    endpoint: str,
    *,
    env: Mapping[str, str],
    cwd: str | None,
    runner: Runner,
) -> Any:
    argv = ("gh", "api", "--hostname", "github.com", endpoint)
    last_code = "request_failed"
    for attempt in range(_MAX_API_ATTEMPTS):
        returncode, stdout, _stderr = runner(argv, env, cwd)
        if returncode == 0:
            try:
                return json.loads(stdout)
            except (TypeError, json.JSONDecodeError):
                last_code = "invalid_response"
        else:
            last_code = "request_failed"
        if attempt + 1 < _MAX_API_ATTEMPTS:
            time.sleep(_RETRY_DELAY_SECONDS * (attempt + 1))
    raise GitHubAcceptanceError("github_read", last_code, "read-only API request failed")


def _snapshot(
    owner: str,
    repo: str,
    number: int,
    *,
    expected: Mapping[str, Any],
    env: Mapping[str, str],
    cwd: str | None,
    runner: Runner,
) -> dict[str, Any]:
    prefix = f"repos/{owner}/{repo}"
    pr = _request_json(f"{prefix}/pulls/{number}", env=env, cwd=cwd, runner=runner)
    if not isinstance(pr, dict):
        raise GitHubAcceptanceError("pr_read", "invalid_response", "pull request response invalid")
    mode = expected.get("acceptance_mode")
    if mode is None:
        # Legacy metadata remains merged-PR mode, but an incomplete merged
        # claim cannot silently become exact-SHA mode.
        mode = _MERGED_MODE if expected.get("merge_sha") else None
    if mode not in {_MERGED_MODE, _EXACT_WORKFLOW_MODE}:
        raise GitHubAcceptanceError("input", "acceptance_mode_invalid", "unsupported acceptance mode")
    if mode == _EXACT_WORKFLOW_MODE:
        if pr.get("state") not in {"open", "closed"}:
            raise GitHubAcceptanceError("pr_read", "state_invalid", "pull request state invalid")
    elif pr.get("state") != "closed" or not pr.get("merged_at"):
        raise GitHubAcceptanceError("pr_read", "not_merged", "pull request is not merged")
    repository = pr.get("base", {}).get("repo", {}).get("full_name")
    if not isinstance(repository, str) or repository.lower() != f"{owner}/{repo}".lower():
        raise GitHubAcceptanceError("pr_read", "repository_mismatch", "pull request repository changed")
    if pr.get("number") is not None and pr.get("number") != number:
        raise GitHubAcceptanceError("pr_read", "number_mismatch", "pull request number changed")
    head = _sha(pr.get("head", {}).get("sha"), "pr_head_sha")
    declared_sha = expected.get("exact_sha") if mode == _EXACT_WORKFLOW_MODE else expected.get(
        "pr_head_sha", expected.get("head_sha")
    )
    if head != _sha(declared_sha, "exact_sha" if mode == _EXACT_WORKFLOW_MODE else "pr_head_sha"):
        raise GitHubAcceptanceError("pr_read", "head_mismatch", "published PR head changed")
    merge = None
    if mode == _MERGED_MODE:
        merge = _sha(pr.get("merge_commit_sha"), "merge_sha")
        if merge != _sha(expected.get("merge_sha"), "merge_sha"):
            raise GitHubAcceptanceError("pr_read", "merge_mismatch", "published PR merge changed")

    checks = _request_json(
        f"{prefix}/commits/{head}/check-runs?per_page=100",
        env=env,
        cwd=cwd,
        runner=runner,
    )
    if not isinstance(checks, dict) or not isinstance(checks.get("check_runs"), list):
        raise GitHubAcceptanceError("checks_read", "invalid_response", "check-runs response invalid")
    check_map = {
        str(item.get("name")): item.get("conclusion")
        for item in checks["check_runs"]
        if isinstance(item, dict) and item.get("name")
    }
    required = expected.get("required_checks")
    if not isinstance(required, list) or not required:
        raise GitHubAcceptanceError("input", "required_checks_invalid", "required checks missing")
    observed_checks: list[dict[str, Any]] = []
    for item in required:
        name = item.get("name") if isinstance(item, dict) else item
        if not isinstance(name, str) or not name or check_map.get(name) != "success":
            raise GitHubAcceptanceError("checks_read", "required_check_failed", "required check not successful")
        observed_checks.append({"name": name, "conclusion": "success"})

    terminal = expected.get("terminal_run")
    if not isinstance(terminal, dict) or not terminal.get("id"):
        raise GitHubAcceptanceError("input", "terminal_run_invalid", "terminal run missing")
    run_id = str(terminal["id"])
    run = _request_json(
        f"{prefix}/actions/runs/{run_id}", env=env, cwd=cwd, runner=runner
    )
    if not isinstance(run, dict) or run.get("head_sha") != head:
        raise GitHubAcceptanceError("run_read", "head_mismatch", "terminal run head changed")
    if mode == _EXACT_WORKFLOW_MODE and run.get("event") != "workflow_dispatch":
        raise GitHubAcceptanceError("run_read", "event_mismatch", "terminal run is not workflow_dispatch")
    if run.get("status") != "completed" or run.get("conclusion") != "success":
        raise GitHubAcceptanceError("run_read", "run_not_successful", "terminal run is not successful")
    jobs = _request_json(
        f"{prefix}/actions/runs/{run_id}/jobs?per_page=100",
        env=env,
        cwd=cwd,
        runner=runner,
    )
    job_rows = jobs.get("jobs") if isinstance(jobs, dict) else None
    if not isinstance(job_rows, list) or not job_rows or any(
        not isinstance(job, dict) or job.get("conclusion") != "success" for job in job_rows
    ):
        raise GitHubAcceptanceError("run_read", "job_not_successful", "terminal run has incomplete jobs")
    return {
        "acceptance_mode": mode,
        "published_pr": expected["published_pr"],
        "pr_state": pr["state"],
        "pr_repository": repository,
        "pr_number": number,
        "pr_head_sha": head,
        "merge_sha": merge,
        "required_checks": observed_checks,
        "terminal_run": {
            "id": terminal["id"],
            "head_sha": head,
            "event": run["event"],
            "status": run["status"],
            "conclusion": run["conclusion"],
            "jobs": [
                {"id": job.get("id"), "name": job.get("name"), "conclusion": "success"}
                for job in job_rows
                if isinstance(job, dict)
            ],
        },
    }


def validate_published_pr(
    metadata: Mapping[str, Any],
    *,
    env: Mapping[str, str] | None = None,
    cwd: str | None = None,
    runner: Runner | None = None,
) -> dict[str, Any]:
    """Validate and return sanitized, two-read GitHub acceptance evidence."""
    if not isinstance(metadata, Mapping) or "published_pr" not in metadata:
        return dict(metadata)
    owner, repo, number = _parse_pr_url(metadata["published_pr"])
    expected = dict(metadata)
    mode = expected.get("acceptance_mode")
    if mode not in {None, _MERGED_MODE, _EXACT_WORKFLOW_MODE}:
        raise GitHubAcceptanceError("input", "acceptance_mode_invalid", "unsupported acceptance mode")
    if mode is None and not expected.get("merge_sha"):
        raise GitHubAcceptanceError("input", "acceptance_mode_invalid", "acceptance mode required")
    if mode == _EXACT_WORKFLOW_MODE:
        _sha(expected.get("exact_sha"), "exact_sha")
    runtime_env = dict(os.environ if env is None else env)
    read = runner or _default_runner
    first = _snapshot(owner, repo, number, expected=expected, env=runtime_env, cwd=cwd, runner=read)
    second = _snapshot(owner, repo, number, expected=expected, env=runtime_env, cwd=cwd, runner=read)
    if first != second:
        raise GitHubAcceptanceError("consistency", "second_read_mismatch", "GitHub readback changed")
    enriched = dict(metadata)
    enriched["github_acceptance"] = first
    return enriched
