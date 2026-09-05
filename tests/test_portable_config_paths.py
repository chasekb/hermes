"""Static coverage for the portable workflow configuration contract."""

from pathlib import Path
import os
import importlib.util
import shutil
import subprocess

import pytest
import yaml


ROOT = Path(__file__).parents[1]


def _contract_checker():
    spec = importlib.util.spec_from_file_location(
        "check_config_contract", ROOT / "scripts/check_config_contract.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
    assert any("${HERMES_POSTGRES_" in value for value in commands)


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


def test_missing_postgres_env_is_explicitly_fail_closed() -> None:
    servers = _config()["mcp_servers"]
    postgres = [servers[name] for name in servers if name.startswith("postgres-")]
    assert len(postgres) == 4
    for server in postgres:
        wrapper = server["args"][-1]
        assert "set -euo pipefail" in wrapper
        assert ': "${HERMES_POSTGRES_' in wrapper
        assert 'source "$HERMES_POSTGRES_' in wrapper
        assert "export DB_READ_ONLY=true" in wrapper


def test_missing_postgres_env_prevents_mcp_launch(tmp_path: Path) -> None:
    servers = _config()["mcp_servers"]
    sentinel = tmp_path / "npx-launched"
    fake_npx = tmp_path / "npx"
    fake_npx.write_text(f"#!/bin/sh\ntouch {sentinel}\n", encoding="utf-8")
    fake_npx.chmod(0o755)

    for name, server in servers.items():
        if not name.startswith("postgres-"):
            continue
        wrapper = server["args"][-1]
        env_name = next(
            line.split("HERMES_", 1)[1].split("_ENV", 1)[0]
            for line in wrapper.splitlines()
            if line.strip().startswith(": \"${HERMES_")
        )
        variable = f"HERMES_{env_name}_ENV"
        result = subprocess.run(
            [shutil.which("bash") or "/bin/bash", "-lc", wrapper],
            env={
                "PATH": str(tmp_path) + os.pathsep + os.environ["PATH"],
                variable: str(tmp_path / "missing.env"),
            },
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode != 0, name
        assert not sentinel.exists(), name


def test_local_state_paths_are_profile_relative() -> None:
    servers = _config()["mcp_servers"]
    assert "${HERMES_HOME}/hermes-agent" in servers["filesystem"]["args"]
    assert "${HERMES_HOME}/state.db" in servers["sqlite"]["args"]


def test_linux_and_macos_target_fixtures_fail_closed() -> None:
    checker = _contract_checker()
    fixtures = [
        ROOT / "tests/fixtures/config_contract/linux/missing-hook-target.yaml",
        ROOT / "tests/fixtures/config_contract/linux/malformed-overlay.yaml",
        ROOT / "tests/fixtures/config_contract/macos/missing-mcp-target.yaml",
        ROOT / "tests/fixtures/config_contract/macos/unresolved-overlay.yaml",
    ]
    for fixture in fixtures:
        with pytest.raises(checker.ContractError):
            checker.check_targets(checker.load_config(fixture))


def test_missing_overlay_input_is_not_treated_as_parse_only() -> None:
    checker = _contract_checker()
    with pytest.raises(checker.ContractError, match="explicit overlay input is missing"):
        checker.load_overlays({}, [ROOT / "tests/fixtures/config_contract/macos/not-present.yaml"])
