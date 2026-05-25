#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home() / ".hermes"
LOG_PATH = HOME / "agent-hooks" / "hook-events.jsonl"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

DANGEROUS_TERMINAL_PATTERNS = [
    re.compile(r"(?i)\brm\s+-rf\s+/$"),
    re.compile(r"(?i)\brm\s+-rf\s+/\s*$"),
    re.compile(r"(?i)\bmkfs\.[a-z0-9_\-]+\b"),
    re.compile(r"(?i)\bdd\s+if=.*\s+of=/dev/"),
    re.compile(r"(?i)\b(poweroff|reboot|shutdown|halt)\b"),
    re.compile(r"(?i):\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;\s*:"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_preview(value, limit: int = 240) -> str:
    try:
        text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    except Exception:
        text = repr(value)
    text = text.replace("\n", " ")
    return text[:limit]


def log_event(payload: dict) -> None:
    record = {
        "ts": utc_now(),
        "event": payload.get("hook_event_name"),
        "tool": payload.get("tool_name"),
        "session_id": payload.get("session_id") or payload.get("task_id") or "",
        "cwd": payload.get("cwd") or "",
        "preview": safe_preview(payload.get("tool_input") if "tool_input" in payload else payload.get("extra")),
    }
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def terminal_command(payload: dict) -> str:
    tool_input = payload.get("tool_input")
    if isinstance(tool_input, dict):
        return str(tool_input.get("command", "") or "")
    if isinstance(tool_input, str):
        return tool_input
    extra = payload.get("extra") or {}
    if isinstance(extra, dict):
        maybe = extra.get("command") or extra.get("cmd")
        if maybe:
            return str(maybe)
    return ""


def git_context(cwd: str) -> str | None:
    if not cwd:
        return None
    try:
        branch = subprocess.run(
            ["git", "-C", cwd, "branch", "--show-current"],
            capture_output=True,
            text=True,
            timeout=2,
        )
        status = subprocess.run(
            ["git", "-C", cwd, "status", "--short", "--branch"],
            capture_output=True,
            text=True,
            timeout=2,
        )
    except Exception:
        return None
    parts = []
    if branch.returncode == 0:
        b = branch.stdout.strip()
        if b:
            parts.append(f"git branch: {b}")
    if status.returncode == 0:
        s = status.stdout.strip()
        if s:
            parts.append("git status:\n" + s)
    return "\n".join(parts) or None


def notify_approval(description: str, command: str) -> None:
    title = "Hermes needs approval"
    body = f"{description}: {command[:120]}" if description else command[:120]

    def esc(s: str) -> str:
        return s.replace("\\", "\\\\").replace('"', '\\"')

    try:
        subprocess.run(
            [
                "osascript",
                "-e",
                f'display notification "{esc(body)}" with title "{esc(title)}"',
            ],
            check=False,
            capture_output=True,
            text=True,
        )
    except Exception:
        pass


def main() -> int:
    raw = sys.stdin.read()
    payload = {}
    if raw.strip():
        try:
            payload = json.loads(raw)
        except Exception:
            payload = {"raw": raw}

    event = payload.get("hook_event_name", "")
    log_event(payload)

    if event == "pre_tool_call":
        tool = payload.get("tool_name", "")
        if tool == "terminal":
            cmd = terminal_command(payload)
            if cmd and any(p.search(cmd) for p in DANGEROUS_TERMINAL_PATTERNS):
                print(
                    json.dumps(
                        {
                            "action": "block",
                            "message": "Blocked by Hermes hook: destructive terminal command.",
                        }
                    )
                )
                return 0
        return 0

    if event == "pre_llm_call":
        cwd = payload.get("cwd") or os.getcwd()
        pieces = [f"Local context: cwd={cwd}"]
        gc = git_context(cwd)
        if gc:
            pieces.append(gc)
        context = "\n\n".join(pieces)
        if context.strip():
            print(json.dumps({"context": context}))
        return 0

    if event == "pre_approval_request":
        extra = payload.get("extra") or {}
        if not isinstance(extra, dict):
            extra = {}
        notify_approval(str(extra.get("description", "") or ""), str(extra.get("command", "") or ""))
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
