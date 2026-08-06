#!/usr/bin/env python3
"""Verify synthetic CostLens fixtures against expected ledger / alerts / recon."""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYN = ROOT / "fixtures" / "synthetic"
SNAP_DIR = SYN / "snapshots"
EXP = SYN / "expected"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def derive_dailies(snapshot_files: list[Path]) -> tuple[list[dict], list[str]]:
    """Return (daily rows, aborted batch ids)."""
    # prior cumulative per (person_key, cycle_id)
    prior: dict[tuple[str, str], int] = {}
    rows: list[dict] = []
    aborted: list[str] = []

    files = sorted(snapshot_files, key=lambda p: p.name)
    for path in files:
        batch = load_json(path)
        batch_id = batch["batch_id"]
        date = batch["date"]
        entry_point = batch["entry_point"]

        if batch.get("expect_abort"):
            # Any missing cycle_id ⇒ abort entire batch
            if any("cycle_id" not in s for s in batch["snapshots"]):
                aborted.append(batch_id)
                continue
            raise AssertionError(f"{path}: expect_abort set but cycle_ids present")

        for s in batch["snapshots"]:
            if "cycle_id" not in s or s["cycle_id"] in (None, ""):
                aborted.append(batch_id)
                break
        else:
            for s in batch["snapshots"]:
                person = s["person_key"]
                cycle = s["cycle_id"]
                total = int(s["cycle_total_cents"])
                key = (person, cycle)
                if key not in prior:
                    daily = total
                else:
                    daily = total - prior[key]
                prior[key] = total
                rows.append(
                    {
                        "date": date,
                        "person_key": person,
                        "cycle_id": cycle,
                        "spend_cents": daily,
                        "entry_point": entry_point,
                        "source_batch_id": batch_id,
                    }
                )
            continue
        # aborted via break
        continue

    return rows, aborted


def row_key(r: dict) -> tuple:
    return (r["date"], r["person_key"], r["cycle_id"], int(r["spend_cents"]))


def main() -> int:
    errors: list[str] = []

    snaps = list(SNAP_DIR.glob("*.json"))
    if not snaps:
        errors.append("no snapshot files")
        print_errors(errors)
        return 1

    derived, aborted = derive_dailies(snaps)
    expected_ledger = load_json(EXP / "daily_ledger.json")
    expected_rows = expected_ledger["rows"]

    der_set = {row_key(r) for r in derived}
    exp_set = {
        (r["date"], r["person_key"], r["cycle_id"], int(r["spend_cents"]))
        for r in expected_rows
    }

    if der_set != exp_set:
        missing = exp_set - der_set
        extra = der_set - exp_set
        if missing:
            errors.append(f"daily ledger missing rows: {sorted(missing)[:5]}…")
        if extra:
            errors.append(f"daily ledger unexpected rows: {sorted(extra)[:5]}…")

    # Reconciliation
    recon = load_json(EXP / "reconciliation.json")
    tol = int(recon.get("rounding_tolerance_cents", 0))
    sums: dict[tuple[str, str], int] = defaultdict(int)
    for r in derived:
        sums[(r["cycle_id"], r["person_key"])] += int(r["spend_cents"])

    for cycle in recon["cycles"]:
        cid = cycle["cycle_id"]
        for person, latest in cycle["latest_totals_cents"].items():
            got = sums.get((cid, person), None)
            if got is None:
                errors.append(f"recon missing dailies for {person} cycle {cid}")
            elif abs(got - int(latest)) > tol:
                errors.append(
                    f"recon mismatch {person} cycle {cid}: sum(dailies)={got} latest={latest}"
                )

    for batch_id in recon["abort_batches"]:
        if batch_id not in aborted:
            errors.append(f"expected abort of {batch_id}, got aborted={aborted}")

    # Attribution: unassigned must appear in derived spend
    attr = load_json(SYN / "attribution.json")
    mapped = {m["person_key"] for m in attr["mappings"]}
    unassigned = set(recon["unassigned_person_keys"])
    spenders = {r["person_key"] for r in derived}
    for person in unassigned:
        if person not in spenders:
            errors.append(f"unassigned {person} dropped from ledger")
        if person in mapped:
            errors.append(f"{person} listed unassigned but mapped")

    # Alerts dedupe
    alerts = load_json(EXP / "alerts.json")
    threshold = int(alerts["threshold_person_daily_cents"])
    version = alerts["threshold_version"]
    fired: set[str] = set()
    for r in derived:
        if int(r["spend_cents"]) >= threshold:
            key = f"{r['date']}|{r['person_key']}|daily_spend|{version}"
            fired.add(key)
    # Simulate replay: adding same keys again must not grow set
    replay = set(fired)
    for r in derived:
        if int(r["spend_cents"]) >= threshold:
            key = f"{r['date']}|{r['person_key']}|daily_spend|{version}"
            replay.add(key)
    if replay != fired:
        errors.append("alert dedupe failed on replay")
    expected_keys = set(alerts["expected_alert_keys"])
    if not expected_keys.issubset(fired):
        errors.append(f"missing alert keys: {expected_keys - fired}")
    # Fixture intends only the listed keys for this threshold story
    if fired != expected_keys:
        errors.append(f"alert key set mismatch: got={sorted(fired)} expected={sorted(expected_keys)}")

    if errors:
        print_errors(errors)
        return 1

    print("OK — fixtures match cycle→daily, reconciliation, abort, attribution, alerts")
    print(f"  daily rows: {len(derived)}")
    print(f"  aborted batches: {aborted}")
    print(f"  alert keys: {sorted(fired)}")
    return 0


def print_errors(errors: list[str]) -> None:
    print("FAIL — fixture verification", file=sys.stderr)
    for e in errors:
        print(f"  - {e}", file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
