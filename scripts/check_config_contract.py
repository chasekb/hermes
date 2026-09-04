#!/usr/bin/env python3
"""Fail-closed, secret-safe validation of a Hermes YAML configuration."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, NoReturn

import yaml


class ContractError(Exception):
    """A deterministic configuration contract failure."""

    def __init__(self, code: str, detail: str) -> None:
        super().__init__(detail)
        self.code = code
        self.detail = detail


ABSOLUTE_PATH = re.compile(r"(?:^|[ =\"'])(?:[A-Za-z]:[\\/]|/Users/|/home/|/opt/|/var/|/tmp/|/root/)")
VARIABLE_REFERENCE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?::\?[^}]*)?\}")
MALFORMED_REFERENCE = re.compile(r"\$\{[^}]*\}")
DB_READ_ONLY = re.compile(r"(?:^|[\s;])(?:export\s+)?DB_READ_ONLY\s*=\s*(?:true|True|TRUE)(?:\s|;|$)")


def fail(code: str, detail: str) -> NoReturn:
    raise ContractError(code, detail)


def get_path(config: dict[str, Any], path: tuple[str, ...]) -> Any:
    value: Any = config
    for key in path:
        if not isinstance(value, dict) or key not in value:
            fail("CONTRACT_MISSING", ".".join(path))
        value = value[key]
    return value


def iter_strings(value: Any, path: str = "config") -> list[tuple[str, str]]:
    if isinstance(value, dict):
        result: list[tuple[str, str]] = []
        for key, child in value.items():
            result.extend(iter_strings(child, f"{path}.{key}"))
        return result
    if isinstance(value, list):
        result = []
        for index, child in enumerate(value):
            result.extend(iter_strings(child, f"{path}[{index}]"))
        return result
    return [(path, value)] if isinstance(value, str) else []


def check_paths(config: dict[str, Any]) -> None:
    for path, value in iter_strings(config):
        if not ABSOLUTE_PATH.search(value):
            continue
        fail("CONTRACT_ABSOLUTE_PATH", path)


def check_targets(config: dict[str, Any]) -> None:
    hooks = config.get("hooks")
    if not isinstance(hooks, dict) or not hooks:
        fail("CONTRACT_HOOK_TARGET", "hooks must declare targets")
    for event, entries in hooks.items():
        if not isinstance(entries, list) or not entries:
            fail("CONTRACT_HOOK_TARGET", f"hooks.{event} must declare targets")
        for index, entry in enumerate(entries):
            if not isinstance(entry, dict) or not isinstance(entry.get("command"), str) or not entry["command"].strip():
                fail("CONTRACT_HOOK_TARGET", f"hooks.{event}[{index}].command")
            command = entry["command"]
            if "${HERMES_HOME}" not in command and "${HERMES_PROJECT_ROOT" not in command:
                fail("CONTRACT_HOOK_TARGET", f"hooks.{event}[{index}].command is not an explicit portable target")
            for reference in MALFORMED_REFERENCE.findall(command):
                if not VARIABLE_REFERENCE.fullmatch(reference):
                    fail("CONTRACT_HOOK_TARGET", f"hooks.{event}[{index}].command has malformed variable")
    servers = config.get("mcp_servers")
    if not isinstance(servers, dict) or not servers:
        fail("CONTRACT_MCP_TARGET", "mcp_servers must declare at least one target")
    for name, server in servers.items():
        if (
            not isinstance(server, dict)
            or not isinstance(server.get("command"), str)
            or not server["command"].strip()
            or not isinstance(server.get("args"), list)
            or not server["args"]
        ):
            fail("CONTRACT_MCP_TARGET", f"mcp_servers.{name}.command")
        if name in {"filesystem", "sqlite"} and not any(
            isinstance(arg, str) and "${HERMES_HOME}" in arg for arg in server["args"]
        ):
            fail("CONTRACT_MCP_TARGET", f"mcp_servers.{name} missing explicit HERMES_HOME target")
        if name.startswith("postgres-") and not any(
            isinstance(arg, str) and "${HERMES_PROJECT_ROOT:?" in arg for arg in server["args"]
        ):
            fail("CONTRACT_MCP_TARGET", f"mcp_servers.{name} missing explicit project-root target")


def merge_overlay(base: dict[str, Any], overlay: dict[str, Any], source: Path) -> dict[str, Any]:
    """Apply a mapping overlay with explicit, deterministic deep-merge semantics."""
    if not overlay or any(key not in base for key in overlay):
        fail("CONTRACT_OVERLAY", f"{source} must override known configuration sections")

    def merge(left: Any, right: Any) -> Any:
        if isinstance(left, dict) and isinstance(right, dict):
            result = dict(left)
            for key, value in right.items():
                result[key] = merge(result[key], value) if key in result else value
            return result
        return right

    return merge(base, overlay)


def check_safety(config: dict[str, Any]) -> None:
    if get_path(config, ("security", "redact_secrets")) is not True:
        fail("CONTRACT_SECURITY", "security.redact_secrets")
    if get_path(config, ("security", "tirith_fail_open")) is not False:
        fail("CONTRACT_SECURITY", "security.tirith_fail_open")
    if get_path(config, ("approvals", "mode")) != "manual":
        fail("CONTRACT_APPROVALS", "approvals.mode")
    for path, value in iter_strings(config):
        if "DB_READ_ONLY" in value and not DB_READ_ONLY.search(value):
            fail("CONTRACT_DB_READ_ONLY", path)


def load_config(path: Path) -> dict[str, Any]:
    data: Any = None
    try:
        with path.open(encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
    except (OSError, yaml.YAMLError):
        fail("CONTRACT_YAML_PARSE", "configuration could not be parsed")
    if not isinstance(data, dict):
        fail("CONTRACT_YAML_SHAPE", "top-level YAML value must be a mapping")
    return data


def load_overlays(config: dict[str, Any], paths: list[Path]) -> dict[str, Any]:
    merged = config
    for path in paths:
        if not path.is_file():
            fail("CONTRACT_OVERLAY", f"explicit overlay input is missing: {path}")
        merged = merge_overlay(merged, load_config(path), path)
    return merged


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("config.yaml"))
    parser.add_argument("--overlay", action="append", type=Path, default=[])
    args = parser.parse_args()
    try:
        config = load_overlays(load_config(args.config), args.overlay)
        check_paths(config)
        check_targets(config)
        check_safety(config)
    except ContractError as error:
        print(f"config-contract-failed: {error.code}", file=sys.stderr)
        return 1
    print("config-contract-ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
