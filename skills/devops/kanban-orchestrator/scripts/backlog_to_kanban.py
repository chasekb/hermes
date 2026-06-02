#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_BACKLOG = Path(os.environ.get("HERMES_HOME", str(Path.home() / ".hermes"))) / "backlog" / "backlog.json"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_backlog(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def eligible_items(backlog: dict, statuses: set[str], include_blocked: bool) -> list[dict]:
    items = []
    for item in backlog.get("items", []):
        status = str(item.get("status", "")).lower()
        if statuses and status not in statuses:
            continue
        if not include_blocked and status == "blocked":
            continue
        items.append(item)
    return items


def to_card(item: dict, backlog_path: Path) -> dict:
    deps = item.get("dependencies") or []
    if isinstance(deps, str):
        deps = [deps]
    return {
        "backlog_id": item.get("id"),
        "title": item.get("title", ""),
        "summary": item.get("summary", ""),
        "scope": item.get("scope", ""),
        "tenant": item.get("tenant", ""),
        "priority": item.get("priority", ""),
        "status": item.get("status", ""),
        "dependencies": deps,
        "execution_criteria": item.get("execution_criteria", []),
        "closeout_criteria": item.get("closeout_criteria", []),
        "notes": item.get("notes", []),
        "links": item.get("links", []),
        "backlog_path": str(backlog_path),
        "generated_at": now(),
    }


def render_markdown(cards: list[dict]) -> str:
    if not cards:
        return "No backlog items matched the filter."
    lines = []
    for card in cards:
        lines.append(f"- [{card['backlog_id']}] {card['title']} ({card['status']})")
        if card.get("summary"):
            lines.append(f"  - Summary: {card['summary']}")
        if card.get("dependencies"):
            lines.append(f"  - Dependencies: {', '.join(card['dependencies'])}")
        if card.get("execution_criteria"):
            lines.append("  - Execution criteria:")
            for criterion in card["execution_criteria"]:
                lines.append(f"    - {criterion}")
        if card.get("closeout_criteria"):
            lines.append("  - Closeout criteria:")
            for criterion in card["closeout_criteria"]:
                lines.append(f"    - {criterion}")
    return "\n".join(lines)


def render_body(card: dict) -> str:
    lines = [
        f"Backlog ID: {card['backlog_id']}",
        f"Source backlog: {card['backlog_path']}",
        f"Backlog status: {card['status']}",
        f"Scope: {card['scope'] or '~/.hermes'}",
        f"Tenant: {card['tenant'] or 'default'}",
        f"Priority: {card['priority'] or 'n/a'}",
        "",
        f"Summary: {card['summary'] or '(no summary provided)'}",
        "",
        "Execution criteria:",
    ]
    if card.get("execution_criteria"):
        lines.extend(f"- {criterion}" for criterion in card["execution_criteria"])
    else:
        lines.append("- (none recorded)")
    lines.extend([
        "",
        "Closeout criteria:",
    ])
    if card.get("closeout_criteria"):
        lines.extend(f"- {criterion}" for criterion in card["closeout_criteria"])
    else:
        lines.append("- (none recorded)")
    if card.get("dependencies"):
        lines.extend(["", "Dependencies:"])
        lines.extend(f"- {dependency}" for dependency in card["dependencies"])
    if card.get("notes"):
        lines.extend(["", "Notes:"])
        lines.extend(f"- {note}" for note in card["notes"])
    if card.get("links"):
        lines.extend(["", "Links:"])
        lines.extend(f"- {link}" for link in card["links"])
    lines.extend([
        "",
        f"Generated at: {card['generated_at']}",
        "",
        "Bridge contract:",
        "- Treat the backlog item as the durable spec.",
        "- Use Kanban as the execution surface.",
        "- Write completion evidence back to the backlog item during closeout.",
    ])
    return "\n".join(lines)


def normalize_priority(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    match = re.fullmatch(r"P(\d+)", text, flags=re.IGNORECASE)
    if match:
        return match.group(1)
    if re.fullmatch(r"\d+", text):
        return text
    return None


def parse_create_output(raw: str) -> dict:
    text = raw.strip()
    if not text:
        return {"raw": raw}
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"(?:task[_\s-]?id|id)[:=]\s*([A-Za-z0-9._:-]+)", text)
        return {"raw": raw, "task_id": match.group(1) if match else None}
    if isinstance(parsed, dict):
        task_id = parsed.get("task_id") or parsed.get("id")
        if task_id is None and isinstance(parsed.get("task"), dict):
            task_id = parsed["task"].get("id") or parsed["task"].get("task_id")
        parsed["task_id"] = task_id
        return parsed
    if isinstance(parsed, list) and parsed:
        first = parsed[0]
        if isinstance(first, dict):
            task_id = first.get("task_id") or first.get("id")
            first["task_id"] = task_id
            return {"items": parsed, "task_id": task_id}
    return {"parsed": parsed}


def apply_to_kanban(card: dict, args: argparse.Namespace) -> dict:
    if not args.board:
        raise SystemExit("--board is required when using --apply")

    title = f"[{card['backlog_id']}] {card['title']}"
    idempotency_key = f"backlog:{args.board}:{card['backlog_id']}"
    cmd = [
        "hermes",
        "kanban",
        "--board",
        args.board,
        "create",
        title,
        "--body",
        render_body(card),
        "--tenant",
        args.tenant or card.get("tenant") or "default",
        "--idempotency-key",
        idempotency_key,
        "--created-by",
        args.created_by,
        "--triage",
        "--json",
    ]
    priority = normalize_priority(args.priority or card.get("priority"))
    if priority is not None:
        cmd.extend(["--priority", priority])
    if args.assignee:
        cmd.extend(["--assignee", args.assignee])
    if args.workspace:
        cmd.extend(["--workspace", args.workspace])
    if args.max_runtime:
        cmd.extend(["--max-runtime", args.max_runtime])
    if args.skill:
        for skill in args.skill:
            cmd.extend(["--skill", skill])
    if args.max_retries is not None:
        cmd.extend(["--max-retries", str(args.max_retries)])
    if args.branch:
        cmd.extend(["--branch", args.branch])
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return {
        "backlog_id": card["backlog_id"],
        "title": card["title"],
        "command": cmd,
        "result": parse_create_output(proc.stdout),
        "stderr": proc.stderr.strip(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Materialize Hermes backlog items into a Kanban-ready bridge payload.")
    parser.add_argument("--backlog", type=Path, default=DEFAULT_BACKLOG)
    parser.add_argument("--statuses", default="proposed,triaged,accepted,ready")
    parser.add_argument("--include-blocked", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--apply", action="store_true", help="Create Kanban tasks for the selected backlog items.")
    parser.add_argument("--board", help="Kanban board slug to target when applying.")
    parser.add_argument("--tenant", help="Override the tenant namespace used when creating tasks.")
    parser.add_argument("--assignee", help="Assignee to set on created Kanban tasks.")
    parser.add_argument("--workspace", help="Workspace mode for created Kanban tasks.")
    parser.add_argument("--priority", help="Override priority when creating Kanban tasks.")
    parser.add_argument("--created-by", default="backlog-bridge", help="Recorded author for created Kanban tasks.")
    parser.add_argument("--max-runtime", help="Optional runtime cap passed through to Kanban create.")
    parser.add_argument("--max-retries", type=int, help="Optional retry cap passed through to Kanban create.")
    parser.add_argument("--branch", help="Optional branch name passed through to Kanban create.")
    parser.add_argument("--skill", action="append", help="Optional worker skill to force-load when creating tasks.")
    args = parser.parse_args()

    backlog = load_backlog(args.backlog)
    statuses = {s.strip().lower() for s in args.statuses.split(",") if s.strip()}
    cards = [to_card(item, args.backlog) for item in eligible_items(backlog, statuses, args.include_blocked)]
    if args.limit > 0:
        cards = cards[:args.limit]

    if args.apply:
        if not args.board:
            parser.error("--board is required when using --apply")
        results = [apply_to_kanban(card, args) for card in cards]
        print(json.dumps({
            "source_backlog": str(args.backlog),
            "board": args.board,
            "apply": True,
            "count": len(results),
            "generated_at": now(),
            "results": results,
        }, indent=2, sort_keys=True))
        return 0

    if args.format == "markdown":
        print(render_markdown(cards))
        return 0

    print(json.dumps({
        "source_backlog": str(args.backlog),
        "count": len(cards),
        "generated_at": now(),
        "cards": cards,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
