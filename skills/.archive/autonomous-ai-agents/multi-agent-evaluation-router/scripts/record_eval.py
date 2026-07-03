#!/usr/bin/env python3
"""Append a compact multi-agent evaluation record to backlog/decision-memory.json.

Usage:
  python record_eval.py --record-json '{...}'
  cat record.json | python record_eval.py
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
STORE = ROOT / "backlog" / "decision-memory.json"


def _load_store() -> dict[str, Any]:
    if STORE.exists():
        return json.loads(STORE.read_text())
    return {"version": 1, "description": "Durable decision-memory store for Hermes backlog, workflow, skill, and hook reviews.", "updated_at": "", "records": []}


def _write_store(data: dict[str, Any]) -> None:
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    STORE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record-json", help="JSON record to append; if omitted, read from stdin")
    args = parser.parse_args()
    raw = args.record_json
    if raw is None:
        import sys
        raw = sys.stdin.read().strip()
    if not raw:
        raise SystemExit("no record JSON supplied")
    record = json.loads(raw)
    if not isinstance(record, dict):
        raise SystemExit("record must be a JSON object")
    required = ["timestamp", "prompt_class", "prompt_sha", "lanes", "reviewers", "recommendation"]
    missing = [key for key in required if key not in record]
    if missing:
        raise SystemExit(f"missing required keys: {', '.join(missing)}")
    store = _load_store()
    store.setdefault("records", []).append(record)
    _write_store(store)
    print(json.dumps({"path": str(STORE), "records": len(store["records"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
