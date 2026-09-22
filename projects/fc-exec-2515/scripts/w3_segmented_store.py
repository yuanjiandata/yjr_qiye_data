#!/usr/bin/env python3
"""Read and validate logical W3 cumulative stores (sealed base + append-only result segments)."""
import csv, gzip
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
E = ROOT / "projects" / "fc-exec-2515" / "evidence"
INDEX = E / "W3_SEGMENT_INDEX.csv"

LEDGER_FIELDS = [
    "queue_order","person_id","province","excel_row","candidate_names","evidence_type",
    "evidence_grade","evidence_title","evidence_url","evidence_date",
    "current_verification_status","unresolved_reason",
]
OVERLAY_FIELDS = [
    "queue_order","person_id","province","excel_row","identity_resolution","candidate_names",
    "current_organization","current_title","current_verification_status","evidence_grade",
    "evidence_url","unresolved_reason",
]

def _read(path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def _project(rows, projection):
    if projection == "native":
        return rows
    fields = LEDGER_FIELDS if projection == "ledger" else OVERLAY_FIELDS
    return [{k:r.get(k,"") for k in fields} for r in rows]

def load_kind(kind):
    with INDEX.open("r", encoding="utf-8-sig", newline="") as f:
        entries=[r for r in csv.DictReader(f) if r["kind"] == kind]
    entries.sort(key=lambda r:int(r["ordinal"]))
    out=[]; expected=1
    for e in entries:
        start,end,count=map(int,(e["queue_start"],e["queue_end"],e["row_count"]))
        assert start == expected, (kind,"gap_or_overlap",expected,start)
        rows=_project(_read(ROOT/e["path"]),e["projection"])
        assert len(rows)==count
        assert [int(r["queue_order"]) for r in rows] == list(range(start,end+1))
        out.extend(rows); expected=end+1
    assert len({r["queue_order"] for r in out}) == len(out)
    return out

def main():
    ledger=load_kind("ledger")
    overlay=load_kind("overlay")
    assert len(ledger)==len(overlay)
    assert [r["queue_order"] for r in ledger] == [r["queue_order"] for r in overlay]
    assert [r["person_id"] for r in ledger] == [r["person_id"] for r in overlay]
    print(f"PASS W3 segmented store rows={len(ledger)} end={ledger[-1]['queue_order']}")

if __name__ == "__main__":
    main()
