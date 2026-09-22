#!/usr/bin/env python3
"""Deterministic validation for FC-EXEC-2515 W3-BATCH-0029."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=1681,1740
EXPECTED_RESULTS_SHA256="9167d2db944582487f25927ceb6ecad668ea61ebd16d2feaa69b97c741087ac1"
EXPECTED_RESEARCH_SHA256="a5d842e14fb7247905f38f533f4e2b0c3be76ef2ee026d3b5a1c957c8d6f5514"

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    raw=gzip.open(E/"W3_BATCH_0029_RESULTS.csv.gz","rb").read()
    research_raw=gzip.open(E/"W3_BATCH_0029_RESEARCH.tsv.gz","rb").read()
    assert hashlib.sha256(raw).hexdigest()==EXPECTED_RESULTS_SHA256
    assert hashlib.sha256(research_raw).hexdigest()==EXPECTED_RESEARCH_SHA256
    results=list(csv.DictReader(raw.decode("utf-8-sig").splitlines()))
    research=list(csv.DictReader(research_raw.decode("utf-8-sig").splitlines(),delimiter="\t"))
    assert len(queue)==len(results)==60
    assert len(research)==52
    expected=list(range(START,END+1))
    assert [int(r["queue_order"]) for r in queue]==expected
    assert [int(r["queue_order"]) for r in results]==expected
    assert {r["priority"] for r in queue}=={"P1_IDENTITY"}
    assert Counter(r["province"] for r in queue)==Counter({"河南":60})
    assert [r["person_id"] for r in queue]==[r["person_id"] for r in results]
    assert len({r["person_id"] for r in results})==60
    for r in results:
        if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED":
            assert r["current_organization"] and r["current_title"] and r["evidence_url"]
            assert not r["unresolved_reason"]
        else:
            assert r["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE"
            assert not r["current_organization"] and not r["current_title"] and r["unresolved_reason"]
        assert r["evidence_grade"] in {"A","B"}
    assert Counter(r["current_verification_status"] for r in results)==Counter(
        {"UNRESOLVED_CURRENT_ORG_TITLE":39,"CURRENT_ORG_TITLE_CONFIRMED":21})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":49,"B":11})
    with (E/"W3_SEGMENT_INDEX.csv").open("r",encoding="utf-8-sig",newline="") as f:
        idx=list(csv.DictReader(f))
    for kind in ("ledger","overlay"):
        seg=[r for r in idx if r["kind"]==kind]
        seg.sort(key=lambda r:int(r["ordinal"]))
        assert [(int(r["queue_start"]),int(r["queue_end"])) for r in seg]==[(1,1620),(1621,1680),(1681,1740)]
    print("PASS W3-BATCH-0029 next=1741")

if __name__=="__main__":
    main()
