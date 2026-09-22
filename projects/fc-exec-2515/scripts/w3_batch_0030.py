#!/usr/bin/env python3
"""Deterministic validation for FC-EXEC-2515 W3-BATCH-0030."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=1741,1800
EXPECTED_RESULTS_RAW_SHA256="f772b98fd014369d64249a9065b3fa5170e37e38bae8b9d58233190eefb4de16"
EXPECTED_RESULTS_GZIP_SHA256="0355eb2b3f1a30334501463cb50c3b2fe31b846cadda7fce7b4254e12c6c7362"
EXPECTED_RESEARCH_RAW_SHA256="f61a3e495b14442576f62c29d26a59f74e9f04eece73ab287289ef8078bd6018"
EXPECTED_RESEARCH_GZIP_SHA256="1073fa353c5378ac0e9d14687ba16eb15a76bf781691cbaa44e1d002b13d829e"

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rgz=(E/"W3_BATCH_0030_RESULTS.csv.gz").read_bytes()
    qgz=(E/"W3_BATCH_0030_RESEARCH.tsv.gz").read_bytes()
    assert hashlib.sha256(rgz).hexdigest()==EXPECTED_RESULTS_GZIP_SHA256
    assert hashlib.sha256(qgz).hexdigest()==EXPECTED_RESEARCH_GZIP_SHA256
    raw=gzip.decompress(rgz); research_raw=gzip.decompress(qgz)
    assert hashlib.sha256(raw).hexdigest()==EXPECTED_RESULTS_RAW_SHA256
    assert hashlib.sha256(research_raw).hexdigest()==EXPECTED_RESEARCH_RAW_SHA256
    results=list(csv.DictReader(raw.decode("utf-8-sig").splitlines()))
    research=list(csv.DictReader(research_raw.decode("utf-8-sig").splitlines(),delimiter="\t"))
    assert len(queue)==len(results)==len(research)==60
    expected=list(range(START,END+1))
    assert [int(r["queue_order"]) for r in queue]==expected
    assert [int(r["queue_order"]) for r in results]==expected
    assert [int(r["queue_order"]) for r in research]==expected
    assert {r["priority"] for r in queue}=={"P1_IDENTITY"}
    assert Counter(r["province"] for r in queue)==Counter({"河南":60})
    assert [r["person_id"] for r in queue]==[r["person_id"] for r in results]
    assert len({r["person_id"] for r in results})==60
    for r in results:
        assert r["evidence_url"] or r["unresolved_reason"]
        assert r["evidence_grade"] in {"A","B"}
        if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED":
            assert r["current_organization"] and r["current_title"] and r["evidence_url"] and not r["unresolved_reason"]
        else:
            assert r["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE"
            assert not r["current_organization"] and not r["current_title"] and r["unresolved_reason"]
    assert Counter(r["current_verification_status"] for r in results)==Counter(
        {"UNRESOLVED_CURRENT_ORG_TITLE":42,"CURRENT_ORG_TITLE_CONFIRMED":18})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":49,"B":11})
    with (E/"W3_SEGMENT_INDEX.csv").open("r",encoding="utf-8-sig",newline="") as f:
        idx=list(csv.DictReader(f))
    for kind in ("ledger","overlay"):
        seg=[r for r in idx if r["kind"]==kind]
        seg.sort(key=lambda r:int(r["ordinal"]))
        assert [(int(r["queue_start"]),int(r["queue_end"])) for r in seg]==[
            (1,1620),(1621,1680),(1681,1740),(1741,1800)]
    print("PASS W3-BATCH-0030 next=1801")

if __name__=="__main__":
    main()
