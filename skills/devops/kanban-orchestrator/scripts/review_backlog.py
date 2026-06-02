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


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def item_age_days(item: dict) -> int:
    raw = item.get("updated_at") or item.get("created_at")
    if not raw:
        return 0
    dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    delta = datetime.now(timezone.utc) - dt
    return max(delta.days, 0)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a weekly or stale-item review for the Hermes backlog.")
    parser.add_argument("--backlog", type=Path, default=DEFAULT_BACKLOG)
    parser.add_argument("--mode", choices=("weekly", "stale"), default="weekly")
    parser.add_argument("--stale-days", type=int, default=14)
    args = parser.parse_args()

    backlog = load_json(args.backlog)
    items = backlog.get("items", [])
    lines = [f"# Hermes backlog {args.mode} review", ""]
    lines.append(f"Source: {args.backlog}")
    lines.append(f"Generated at: {now()}")
    lines.append("")

    if args.mode == "weekly":
        lines.append("## Ready / accepted items")
        for item in items:
            if str(item.get("status", "")).lower() in {"accepted", "ready", "in_progress", "blocked"}:
                lines.append(f"- [{item.get('id')}] {item.get('title')} ({item.get('status')})")
        lines.append("")
        lines.append("## Proposed / triaged items")
        for item in items:
            if str(item.get("status", "")).lower() in {"proposed", "triaged"}:
                lines.append(f"- [{item.get('id')}] {item.get('title')} ({item.get('status')})")
    else:
        lines.append(f"## Items older than {args.stale_days} days")
        for item in items:
            if item_age_days(item) >= args.stale_days and str(item.get("status", "")).lower() not in {"done", "closed", "archived"}:
                lines.append(f"- [{item.get('id')}] {item.get('title')} ({item.get('status')}) - age {item_age_days(item)}d")

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
