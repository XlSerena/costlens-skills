#!/usr/bin/env python3
"""Lightweight check: SKILL.md descriptions cover self-test trigger phrases."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

# phrase snippet → skill folder name
CASES = [
    ("cycle-to-date", "cycle-total-to-daily"),
    ("cycle total", "cycle-total-to-daily"),
    ("entry point", "spend-entry-inventory"),
    ("team", "spend-attribution"),
    ("dedup", "spend-alerts"),
    ("alert", "spend-alerts"),
    ("reconcil", "spend-reconciliation"),
]


def read_desc(skill_dir: Path) -> str:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return ""
    block = m.group(1)
    # flatten yaml-ish description
    return block.lower()


def main() -> int:
    errors: list[str] = []
    descs: dict[str, str] = {}
    for d in sorted(SKILLS.iterdir()):
        if d.is_dir() and (d / "SKILL.md").exists():
            descs[d.name] = read_desc(d)

    for needle, skill in CASES:
        blob = descs.get(skill, "")
        if needle not in blob and needle not in (SKILLS / skill / "SKILL.md").read_text(encoding="utf-8").lower():
            errors.append(f"{skill}: missing trigger cue {needle!r}")

    # ensure when-not / anti-rationalization present
    for skill in descs:
        body = (SKILLS / skill / "SKILL.md").read_text(encoding="utf-8")
        if "## When not to use" not in body:
            errors.append(f"{skill}: missing When not to use")
        if "## Anti-rationalization" not in body:
            errors.append(f"{skill}: missing Anti-rationalization")

    if errors:
        print("FAIL", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print("OK — trigger cues + when-not + anti-rationalization present")
    for skill in sorted(descs):
        print(f"  · {skill}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
