#!/usr/bin/env python3
"""Validate the checked-in Hermes config portability and safety contract."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config.yaml"
ALLOWLIST_PATH = ROOT / "shell-hooks-allowlist.json"
HOST_PATH_RE = re.compile(r"/(?:Users|home)/[A-Za-z0-9_.-]+")
HOOK_TEMPLATE = "${HERMES_HOME}/agent-hooks/hook_router.py"


def fail(message: str) -> None:
    raise SystemExit(f"config portability check failed: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> None:
    config_text = CONFIG_PATH.read_text(encoding="utf-8")
    require(not HOST_PATH_RE.search(config_text), "host-specific absolute path found in config.yaml")
    require(config_text.count(f"command: {HOOK_TEMPLATE}") == 24, "all 24 hooks must use the portable router template")
    for expected in (
        "allow_private_urls: false",
        "redact_secrets: true",
        "tirith_fail_open: false",
        "mode: manual",
        "cron_mode: deny",
        "- ${HERMES_HOME}/hermes-agent",
        "- ${HERMES_HOME}/state.db",
    ):
        require(expected in config_text, f"missing safety or path contract: {expected}")

    mcp_text = config_text[config_text.index("mcp_servers:"):]
    mcp_blocks = {
        block.split(":", 1)[0].strip(): block
        for block in re.split(r"\n  (?=postgres-)", mcp_text)
    }
    for name in ("postgres-db", "postgres-metabase", "postgres-trade", "postgres-cohida"):
        command = mcp_blocks.get(name, "")
        require("set -euo pipefail" in command, f"{name} must fail closed")
        require("DB_READ_ONLY=true" in command, f"{name} must remain read-only")
        require("source \"$HERMES_POSTGRES_" in command, f"{name} must source an explicit local env variable")

    allowlist = json.loads(ALLOWLIST_PATH.read_text(encoding="utf-8"))
    require(
        allowlist.get("approvals")
        and all(item.get("command") == HOOK_TEMPLATE for item in allowlist["approvals"]),
        "hook allowlist must use the portable router template",
    )
    print("config-portability-ok")


if __name__ == "__main__":
    main()
