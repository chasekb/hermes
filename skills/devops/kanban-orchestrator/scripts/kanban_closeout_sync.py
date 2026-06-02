#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_BACKLOG = Path(os.environ.get("HERMES_HOME", str(Path.home() / ".hermes"))) / "backlog" / "backlog.json"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json_atomic(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=str(path.parent)) as tmp:
        json.dump(data, tmp, indent=2, sort_keys=True)
        tmp.write("\n")
        tmp_path = Path(tmp.name)
    tmp_path.replace(path)


def find_item(backlog: dict, item_id: str) -> dict:
    for item in backlog.get("items", []):
        if str(item.get("id")) == item_id:
            return item
    raise SystemExit(f"backlog item not found: {item_id}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply Kanban closeout evidence back into the Hermes backlog store.")
    parser.add_argument("--backlog", type=Path, default=DEFAULT_BACKLOG)
    parser.add_argument("--item-id", required=True)
    parser.add_argument("--status", choices=("done", "closed", "blocked"), required=True)
    parser.add_argument("--summary", default="")
    parser.add_argument("--evidence", default="")
    parser.add_argument("--evidence-file", type=Path)
    parser.add_argument("--allow-empty-evidence", action="store_true")
    args = parser.parse_args()

    backlog = load_json(args.backlog)
    item = find_item(backlog, args.item_id)
    previous_status = item.get("status")

    evidence = args.evidence.strip()
    if args.evidence_file:
        evidence = args.evidence_file.read_text(encoding="utf-8").strip()

    if args.status in {"done", "closed"} and not evidence and not args.allow_empty_evidence:
        raise SystemExit("closeout evidence is required for done/closed unless --allow-empty-evidence is set")

    item["status"] = args.status
    item["updated_at"] = now()
    item.setdefault("evidence", [])
    if evidence:
        item["evidence"].append({"timestamp": now(), "text": evidence})
    if args.summary:
        item.setdefault("history", []).append({
            "timestamp": now(),
            "from": previous_status,
            "to": args.status,
            "summary": args.summary,
        })
    else:
        item.setdefault("history", []).append({
            "timestamp": now(),
            "from": previous_status,
            "to": args.status,
        })
    backlog.setdefault("history", []).append({
        "timestamp": now(),
        "item_id": args.item_id,
        "from": previous_status,
        "to": args.status,
        "summary": args.summary,
    })

    save_json_atomic(args.backlog, backlog)
    print(json.dumps({
        "backlog": str(args.backlog),
        "item_id": args.item_id,
        "previous_status": previous_status,
        "new_status": args.status,
        "updated_at": item.get("updated_at"),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
