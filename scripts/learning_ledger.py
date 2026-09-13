#!/usr/bin/env python3
"""Maintain a local, append-only experiment ledger for explicit skill learning."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
VALID_DECISIONS = {"continue", "adjust", "stop"}
REQUIRED_EVENT_FIELDS = {
    "date",
    "experiment",
    "hypothesis",
    "expected_signal",
    "observed_signal",
    "evidence",
    "decision",
    "lesson",
    "tags",
}


def new_ledger() -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "purpose": "User-owned evidence for improving future recommendations",
        "events": [],
    }


def _nonempty_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def validate_event(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("event JSON must be an object")

    missing = sorted(REQUIRED_EVENT_FIELDS - set(payload))
    if missing:
        raise ValueError("missing event fields: " + ", ".join(missing))

    normalized = {
        field: _nonempty_text(payload[field], field)
        for field in [
            "date",
            "experiment",
            "hypothesis",
            "expected_signal",
            "evidence",
            "decision",
            "lesson",
        ]
    }

    try:
        date.fromisoformat(normalized["date"])
    except ValueError as exc:
        raise ValueError("date must use YYYY-MM-DD") from exc

    if normalized["decision"] not in VALID_DECISIONS:
        raise ValueError("decision must be continue, adjust, or stop")

    signal = payload["observed_signal"]
    if isinstance(signal, bool) or not isinstance(signal, int) or not -2 <= signal <= 2:
        raise ValueError("observed_signal must be an integer from -2 to 2")
    normalized["observed_signal"] = signal

    tags = payload["tags"]
    if not isinstance(tags, list) or not all(isinstance(tag, str) and tag.strip() for tag in tags):
        raise ValueError("tags must be a list of non-empty strings")
    normalized["tags"] = sorted({tag.strip().lower() for tag in tags})

    canonical = json.dumps(normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    normalized["event_id"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]
    return normalized


def validate_ledger(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("ledger JSON must be an object")
    if payload.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"schema_version must be {SCHEMA_VERSION}")
    events = payload.get("events")
    if not isinstance(events, list):
        raise ValueError("events must be a list")

    normalized = new_ledger()
    seen: set[str] = set()
    for raw in events:
        event = validate_event(raw)
        supplied_id = raw.get("event_id") if isinstance(raw, dict) else None
        if supplied_id is not None and supplied_id != event["event_id"]:
            raise ValueError("event_id does not match event content")
        if event["event_id"] in seen:
            raise ValueError(f"duplicate event: {event['event_id']}")
        seen.add(event["event_id"])
        normalized["events"].append(event)
    return normalized


def append_event(ledger: dict[str, Any], raw_event: dict[str, Any]) -> dict[str, Any]:
    normalized = validate_ledger(ledger)
    event = validate_event(raw_event)
    if any(existing["event_id"] == event["event_id"] for existing in normalized["events"]):
        raise ValueError(f"duplicate event: {event['event_id']}")
    updated = copy.deepcopy(normalized)
    updated["events"].append(event)
    return updated


def summarize(ledger: dict[str, Any]) -> dict[str, Any]:
    normalized = validate_ledger(ledger)
    events = normalized["events"]
    decisions = Counter(event["decision"] for event in events)
    tags = Counter(tag for event in events for tag in event["tags"])
    ordered = sorted(events, key=lambda event: (event["date"], event["event_id"]))
    return {
        "event_count": len(events),
        "net_observed_signal": sum(event["observed_signal"] for event in events),
        "decision_counts": dict(sorted(decisions.items())),
        "recurring_tags": [
            {"tag": tag, "events": count}
            for tag, count in sorted(tags.items(), key=lambda pair: (-pair[1], pair[0]))
            if count >= 2
        ],
        "recent_lessons": [event["lesson"] for event in ordered[-3:]],
        "notice": (
            "Directional signals summarize experiments; inspect raw evidence before changing a recommendation."
        ),
    }


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        with temporary.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        temporary.replace(path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _emit(payload: dict[str, Any], compact: bool) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=None if compact else 2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compact", action="store_true", help="emit compact JSON")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="create a new ledger without overwriting")
    init_parser.add_argument("ledger", type=Path)

    add_parser = subparsers.add_parser("add", help="append one event from a JSON file")
    add_parser.add_argument("ledger", type=Path)
    add_parser.add_argument("event", type=Path)

    summary_parser = subparsers.add_parser("summary", help="summarize existing evidence")
    summary_parser.add_argument("ledger", type=Path)

    args = parser.parse_args()

    try:
        if args.command == "init":
            if args.ledger.exists():
                raise ValueError(f"refusing to overwrite existing ledger: {args.ledger}")
            ledger = new_ledger()
            _write_json_atomic(args.ledger, ledger)
            _emit(ledger, args.compact)
        elif args.command == "add":
            ledger = append_event(_read_json(args.ledger), _read_json(args.event))
            _write_json_atomic(args.ledger, ledger)
            _emit(ledger, args.compact)
        else:
            _emit(summarize(_read_json(args.ledger)), args.compact)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
