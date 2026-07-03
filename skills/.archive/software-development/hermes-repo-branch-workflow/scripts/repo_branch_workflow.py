#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class BranchState:
    repo_root: Path
    branch: str
    status_header: str
    ahead: int = 0
    behind: int = 0
    dirty_files: list[str] = None  # type: ignore[assignment]

    @property
    def dirty(self) -> bool:
        return bool(self.dirty_files)

    @property
    def status(self) -> str:
        if self.dirty:
            return "dirty"
        if self.ahead and self.behind:
            return "ahead-behind"
        if self.ahead:
            return "ahead"
        if self.behind:
            return "behind"
        return "clean"

    def recommendation(self) -> str:
        if self.dirty:
            if self.branch == "main":
                return "Commit or move the work to a per-machine branch before switching computers."
            return "Commit the work before switching computers, or keep it isolated on this branch until it is ready."
        if self.behind and not self.ahead:
            if self.branch == "main":
                return "Fetch and fast-forward main from origin before continuing."
            return "Fetch origin and rebase this branch onto origin/main before new edits."
        if self.ahead and not self.behind:
            return "Push this branch so the other machine can pick it up cleanly."
        if self.ahead and self.behind:
            return "Fetch origin, reconcile this branch with origin/main, then push after the history is clean."
        return "Safe to switch machines or start a new task on this branch."


def run_git(args: list[str], cwd: Optional[Path] = None) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def find_repo_root(start: Path) -> Path:
    try:
        return Path(run_git(["rev-parse", "--show-toplevel"], cwd=start))
    except subprocess.CalledProcessError as exc:
        raise SystemExit("not inside a git repository") from exc


def parse_status_header(header: str) -> tuple[int, int]:
    ahead = behind = 0
    match = re.search(r"ahead (\d+)", header)
    if match:
        ahead = int(match.group(1))
    match = re.search(r"behind (\d+)", header)
    if match:
        behind = int(match.group(1))
    return ahead, behind


def collect_state(repo_root: Path) -> BranchState:
    status_lines = run_git(["status", "--short", "--branch"], cwd=repo_root).splitlines()
    if not status_lines:
        raise SystemExit("unexpected empty git status output")

    header = status_lines[0]
    branch = run_git(["branch", "--show-current"], cwd=repo_root) or "HEAD"
    ahead, behind = parse_status_header(header)
    dirty_files = [line[3:] if len(line) > 3 else line for line in status_lines[1:]]
    return BranchState(
        repo_root=repo_root,
        branch=branch,
        status_header=header,
        ahead=ahead,
        behind=behind,
        dirty_files=dirty_files,
    )


def build_payload(state: BranchState) -> dict:
    return {
        "repo_root": str(state.repo_root),
        "branch": state.branch,
        "status": state.status,
        "ahead": state.ahead,
        "behind": state.behind,
        "dirty_files": state.dirty_files,
        "recommendation": state.recommendation(),
        "status_header": state.status_header,
    }


def format_human(state: BranchState) -> str:
    lines = [
        f"Repo: {state.repo_root}",
        f"Branch: {state.branch}",
        f"Status: {state.status}",
        f"Ahead: {state.ahead}",
        f"Behind: {state.behind}",
        f"Recommended next step: {state.recommendation()}",
    ]
    if state.dirty_files:
        lines.append("Dirty files:")
        lines.extend(f"  - {item}" for item in state.dirty_files)
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Report the safe next step for the Hermes branch workflow.")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of human-readable text")
    parser.add_argument("--cwd", type=Path, default=Path.cwd(), help="directory to inspect")
    args = parser.parse_args()

    repo_root = find_repo_root(args.cwd)
    state = collect_state(repo_root)
    payload = build_payload(state)

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(format_human(state))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
