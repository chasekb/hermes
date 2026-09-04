"""Static coverage for the portable workflow configuration contract."""

from pathlib import Path
import os

import yaml


ROOT = Path(__file__).parents[1]


def _config() -> dict:
    with (ROOT / "config.yaml").open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def test_hooks_and_mcp_paths_use_portable_variables() -> None:
    config = _config()
    hooks = config["hooks"]
    mcp = config["mcp_servers"]

    commands = [entry["command"] for entries in hooks.values() for entry in entries]
    commands.extend(
        arg
        for server in mcp.values()
        for arg in server.get("args", [])
        if isinstance(arg, str)
    )
    assert commands
    assert all("/Users/bernardchase" not in value for value in commands)
    assert any("${HERMES_HOME}" in value for value in commands)
    assert any("${HERMES_PROJECT_ROOT" in value for value in commands)


def test_hook_path_resolves_from_profile_home_without_shell_execution() -> None:
    command = _config()["hooks"]["pre_tool_call"][0]["command"]
    previous = os.environ.get("HERMES_HOME")
    try:
        os.environ["HERMES_HOME"] = "/tmp/hermes-profile"
        assert os.path.expandvars(command) == (
            "/tmp/hermes-profile/agent-hooks/hook_router.py"
        )
    finally:
        if previous is None:
            os.environ.pop("HERMES_HOME", None)
        else:
            os.environ["HERMES_HOME"] = previous


def test_missing_project_root_is_explicitly_fail_closed() -> None:
    servers = _config()["mcp_servers"]
    postgres = [servers[name] for name in servers if name.startswith("postgres-")]
    assert len(postgres) == 4
    for server in postgres:
        wrapper = server["args"][-1]
        assert '${HERMES_PROJECT_ROOT:?HERMES_PROJECT_ROOT must be set}' in wrapper
        assert "export DB_READ_ONLY=true" in wrapper


def test_local_state_paths_are_profile_relative() -> None:
    servers = _config()["mcp_servers"]
    assert "${HERMES_HOME}/hermes-agent" in servers["filesystem"]["args"]
    assert "${HERMES_HOME}/state.db" in servers["sqlite"]["args"]
