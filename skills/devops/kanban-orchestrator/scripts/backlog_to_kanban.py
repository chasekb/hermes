#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Materialize Hermes backlog items into a Kanban-ready bridge payload.")
    parser.add_argument("--backlog", type=Path, default=DEFAULT_BACKLOG)
    parser.add_argument("--statuses", default="accepted,ready")
    parser.add_argument("--include-blocked", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args()

    backlog = load_backlog(args.backlog)
    statuses = {s.strip().lower() for s in args.statuses.split(",") if s.strip()}
    cards = [to_card(item, args.backlog) for item in eligible_items(backlog, statuses, args.include_blocked)]
    if args.limit > 0:
        cards = cards[:args.limit]

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
