#!/usr/bin/env python3
"""Deterministic validation for FC-EXEC-2515 W3-BATCH-0032."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=1861,1920
EXPECTED_RESULTS_RAW_SHA256="d76486ab1e7fdc4e2a0c65382f241809737f245557b28ffb68786e4af71a7661"
EXPECTED_RESULTS_GZIP_SHA256="49cdc2afea8a33272d18183c7d7a0e2dfe482d09c459ee22444d4c27936cf2ed"
EXPECTED_RESEARCH_RAW_SHA256="514cc8d6239182084cc593ba35074d22de40f4e435ec25c18a9a68ab381d6792"
EXPECTED_RESEARCH_GZIP_SHA256="ca020910b7425736ec953d35baf13ddd459d3a1a01a2f820a1bee6766acb1a9c"
EXPECTED_CONFIRMED=set(list(range(1871,1904))+list(range(1905,1916))+[1919,1920])

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rgz=(E/"W3_BATCH_0032_RESULTS.csv.gz").read_bytes()
    qgz=(E/"W3_BATCH_0032_RESEARCH.tsv.gz").read_bytes()
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
    assert Counter(r["province"] for r in queue)==Counter({"河南":8,"湖北":52})
    assert [r["person_id"] for r in queue]==[r["person_id"] for r in results]
    assert len({r["person_id"] for r in results})==60
    for r in results:
        assert r["evidence_url"] or r["unresolved_reason"]
        assert r["evidence_grade"]=="A"
        q=int(r["queue_order"])
        if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED":
            assert q in EXPECTED_CONFIRMED
            assert r["current_organization"] and r["current_title"] and r["evidence_url"] and not r["unresolved_reason"]
        else:
            assert q not in EXPECTED_CONFIRMED
            assert r["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE"
            assert not r["current_organization"] and not r["current_title"] and r["unresolved_reason"]
    assert Counter(r["current_verification_status"] for r in results)==Counter(
        {"CURRENT_ORG_TITLE_CONFIRMED":46,"UNRESOLVED_CURRENT_ORG_TITLE":14})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":60})
    with (E/"W3_SEGMENT_INDEX.csv").open("r",encoding="utf-8-sig",newline="") as f:
        idx=list(csv.DictReader(f))
    expected_segments=[(1,1620),(1621,1680),(1681,1740),(1741,1800),(1801,1860),(1861,1920)]
    for kind in ("ledger","overlay"):
        seg=[r for r in idx if r["kind"]==kind]
        seg.sort(key=lambda r:int(r["ordinal"]))
        assert [(int(r["queue_start"]),int(r["queue_end"])) for r in seg]==expected_segments
    print("PASS W3-BATCH-0032 next=1921")

if __name__=="__main__":
    main()
