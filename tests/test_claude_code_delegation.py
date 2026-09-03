import json
import stat
from types import SimpleNamespace

import pytest

from tools.delegate_tool import (
    _claude_code_enabled,
    _claude_code_settings,
    _resolve_claude_code_auth,
    _resolve_claude_code_cwd,
)
from hermes_cli.config import validate_config_structure


def test_claude_code_lane_requires_both_config_gates():
    assert not _claude_code_enabled({})
    assert not _claude_code_enabled({"backend": "claude-code-cli"})
    assert not _claude_code_enabled(
        {"backend": "hermes", "claude_code": {"enabled": True}}
    )
    assert _claude_code_enabled(
        {"backend": "claude-code-cli", "claude_code": {"enabled": True}}
    )


def test_auth_uses_oauth_env_or_managed_store_only(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setattr("tools.delegate_tool._claude_code_keychain_available", lambda: False)
    monkeypatch.delenv("CLAUDE_CODE_OAUTH_TOKEN", raising=False)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "api-key-is-not-allowed")
    assert _resolve_claude_code_auth() is None

    credentials = tmp_path / ".claude" / ".credentials.json"
    credentials.parent.mkdir()
    credentials.write_text(json.dumps({"apiKey": "not-an-oauth-credential"}))
    assert _resolve_claude_code_auth() is None

    monkeypatch.setenv("CLAUDE_CODE_OAUTH_TOKEN", "oauth-token")
    assert _resolve_claude_code_auth() == "oauth_env"

    monkeypatch.delenv("CLAUDE_CODE_OAUTH_TOKEN")
    credentials.write_text(json.dumps({"oauthAccount": {"accountUuid": "opaque"}}))
    assert _resolve_claude_code_auth() == "managed_store"

    (tmp_path / ".claude" / "settings.json").write_text(
        json.dumps({"apiKeyHelper": "/usr/local/bin/not-approved"})
    )
    monkeypatch.setenv("CLAUDE_CODE_OAUTH_TOKEN", "oauth-token")
    assert _resolve_claude_code_auth() is None


def test_trusted_cwd_requires_existing_root_and_rejects_escape(tmp_path):
    root = tmp_path / "project"
    root.mkdir()
    child = root / "src"
    child.mkdir()
    assert _resolve_claude_code_cwd({"cwd_roots": [str(root)]}, str(child)) == str(child)

    with pytest.raises(ValueError):
        _resolve_claude_code_cwd({"cwd_roots": []}, str(child))
    with pytest.raises(ValueError):
        _resolve_claude_code_cwd({"cwd_roots": [str(root)]}, str(tmp_path))

    outside = tmp_path / "outside"
    outside.mkdir()
    link = root / "link"
    link.symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError):
        _resolve_claude_code_cwd({"cwd_roots": [str(root)]}, str(link))

    root_link = tmp_path / "project-link"
    root_link.symlink_to(root, target_is_directory=True)
    with pytest.raises(ValueError):
        _resolve_claude_code_cwd({"cwd_roots": [str(root_link)]}, str(child))


def test_delegate_task_uses_cli_lane_without_building_hermes_child(tmp_path, monkeypatch):
    from agent.external_cli_client import CLIResult
    from tools import delegate_tool

    root = tmp_path / "project"
    root.mkdir()
    cfg = {
        "backend": "claude-code-cli",
        "claude_code": {
            "enabled": True,
            "command": "claude",
            "args": [],
            "cwd_roots": [str(root)],
            "allowed_tools": ["Read"],
            "permission_mode": "dontAsk",
            "output_format": "stream-json",
            "max_turns": 2,
            "timeout_seconds": 5,
            "max_concurrent": 1,
            "no_session_persistence": True,
        },
        "max_concurrent_children": 1,
        "max_spawn_depth": 1,
    }
    calls = []

    class FakeClient:
        def __init__(self, **kwargs):
            calls.append(kwargs)

        def run(self):
            return CLIResult(
                status="completed",
                summary="cli result",
                model="claude-test",
                num_turns=2,
            )

    monkeypatch.setattr(delegate_tool, "_load_config", lambda: cfg)
    monkeypatch.setattr(delegate_tool, "_resolve_claude_code_auth", lambda: "managed_store")
    monkeypatch.setattr(delegate_tool, "_resolve_workspace_hint", lambda parent: str(root))
    monkeypatch.setattr(delegate_tool, "ExternalCLIClient", FakeClient, raising=False)
    monkeypatch.setattr(
        delegate_tool,
        "_build_child_agent",
        lambda **kwargs: pytest.fail("Hermes child must not be built for CLI backend"),
    )

    response = delegate_tool.delegate_task(
        goal="inspect the project",
        parent_agent=SimpleNamespace(_delegate_depth=0, session_id="parent"),
    )

    payload = json.loads(response)
    assert payload["results"][0]["backend"] == "claude-code-cli"
    assert payload["results"][0]["summary"] == "cli result"
    assert calls[0]["cwd"] == str(root)
    assert calls[0]["prompt"] == "inspect the project"


def test_unavailable_cli_auth_preserves_result_schema(monkeypatch, tmp_path):
    from tools import delegate_tool

    cfg = {
        "backend": "claude-code-cli",
        "claude_code": {
            "enabled": True,
            "cwd_roots": [str(tmp_path)],
            "allowed_tools": ["Read"],
        },
    }
    monkeypatch.setattr(delegate_tool, "_load_config", lambda: cfg)
    monkeypatch.setattr(delegate_tool, "_resolve_claude_code_auth", lambda: None)
    response = delegate_tool.delegate_task(
        goal="inspect the project",
        parent_agent=SimpleNamespace(_delegate_depth=0, session_id="parent", cwd=str(tmp_path)),
    )
    result = json.loads(response)["results"][0]
    assert result["status"] == "auth_unavailable"
    assert result["tokens"]["source"] == "unavailable"
    assert result["cost_status"] == "unavailable"
    assert "api_calls" in result


def test_delegate_task_runs_project_scoped_cli_end_to_end(tmp_path, monkeypatch):
    from tools import delegate_tool

    root = tmp_path / "project"
    root.mkdir()
    command = tmp_path / "fake-claude"
    command.write_text(
        "#!/bin/sh\n"
        "cat >/dev/null\n"
        "printf '%s\\n' '{\"type\":\"system\",\"model\":\"fake\"}'\n"
        "printf '%s\\n' '{\"type\":\"result\",\"subtype\":\"success\",\"result\":\"done\"}'\n"
    )
    command.chmod(command.stat().st_mode | stat.S_IXUSR)
    cfg = {
        "backend": "claude-code-cli",
        "claude_code": {
            "enabled": True,
            "command": str(command),
            "cwd_roots": [str(root)],
            "allowed_tools": ["Read"],
            "permission_mode": "dontAsk",
            "max_turns": 2,
            "timeout_seconds": 5,
            "max_concurrent": 1,
            "no_session_persistence": True,
        },
        "max_concurrent_children": 1,
        "max_spawn_depth": 1,
    }
    monkeypatch.setattr(delegate_tool, "_load_config", lambda: cfg)
    monkeypatch.setattr(delegate_tool, "_claude_code_keychain_available", lambda: False)
    monkeypatch.setenv("CLAUDE_CODE_OAUTH_TOKEN", "test-token")

    response = delegate_tool.delegate_task(
        goal="inspect the project",
        parent_agent=SimpleNamespace(
            _delegate_depth=0,
            session_id="parent",
            terminal_cwd=str(root),
        ),
    )

    result = json.loads(response)["results"][0]
    assert result["status"] == "completed"
    assert result["summary"] == "done"
    assert result["backend"] == "claude-code-cli"


@pytest.mark.parametrize(
    "key,value",
    [
        ("max_turns", 201),
        ("timeout_seconds", 901),
        ("input_max_bytes", 10 * 1024 * 1024 + 1),
        ("stdout_max_bytes", 8 * 1024 * 1024 + 1),
        ("stderr_max_bytes", 256 * 1024 + 1),
        ("max_concurrent", 9),
        ("max_budget_usd", -1),
    ],
)
def test_claude_code_settings_reject_values_above_safety_ceilings(key, value):
    settings = {
        "enabled": True,
        "allowed_tools": ["Read"],
        key: value,
    }
    with pytest.raises(ValueError, match=key):
        _claude_code_settings({"claude_code": settings})


def test_claude_code_settings_reject_unsafe_args_and_protocol_values():
    base = {"enabled": True, "allowed_tools": ["Read"]}
    with pytest.raises(ValueError, match="controlled flag"):
        _claude_code_settings(
            {"claude_code": {**base, "args": ["--bare"]}}
        )
    with pytest.raises(ValueError, match="output_format"):
        _claude_code_settings(
            {"claude_code": {**base, "output_format": "text"}}
        )


def test_config_validation_reports_unsafe_claude_code_settings():
    issues = validate_config_structure(
        {
            "delegation": {
                "backend": "claude-code-cli",
                "claude_code": {
                    "enabled": True,
                    "allowed_tools": [],
                    "timeout_seconds": 901,
                },
            }
        }
    )
    messages = "\n".join(issue.message for issue in issues)
    assert "delegation.claude_code" in messages
    assert "allowed_tools" in messages
    assert "timeout_seconds" in messages
