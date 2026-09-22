#!/usr/bin/env python3
"""Deterministic validation for FC-EXEC-2515 W3-BATCH-0028."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=1621,1680
EXPECTED_RESULTS_SHA256="159d306698dcfe6c8914d7ef0d8e2c81626f44effd11504472612191a8decd1e"

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    raw=gzip.open(E/"W3_BATCH_0028_RESULTS.csv.gz","rb").read()
    assert hashlib.sha256(raw).hexdigest()==EXPECTED_RESULTS_SHA256
    results=list(csv.DictReader(raw.decode("utf-8-sig").splitlines()))
    assert len(queue)==len(results)==60
    expected=list(range(START,END+1))
    assert [int(r["queue_order"]) for r in queue]==expected
    assert [int(r["queue_order"]) for r in results]==expected
    assert {r["priority"] for r in queue}=={"P1_IDENTITY"}
    assert Counter(r["province"] for r in queue)==Counter({"河南":29,"福建":25,"江西":4,"山东":2})
    assert [r["person_id"] for r in queue]==[r["person_id"] for r in results]
    assert len({r["person_id"] for r in results})==60
    for r in results:
        if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED":
            assert r["current_organization"] and r["current_title"] and r["evidence_url"]
            assert not r["unresolved_reason"]
        else:
            assert r["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE"
            assert not r["current_organization"] and not r["current_title"] and r["unresolved_reason"]
    assert Counter(r["current_verification_status"] for r in results)==Counter(
        {"UNRESOLVED_CURRENT_ORG_TITLE":32,"CURRENT_ORG_TITLE_CONFIRMED":28})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":42,"B":18})
    print("PASS W3-BATCH-0028 next=1681")

if __name__=="__main__":
    main()
