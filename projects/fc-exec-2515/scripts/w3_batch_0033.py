#!/usr/bin/env python3
"""Deterministic validation for FC-EXEC-2515 W3-BATCH-0033."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=1921,1980
EXPECTED_RESULTS_RAW_SHA256="fcd73bb66b1e44865c8f7ec5a9515077045e251efc802bfb9eb0a36cd0b848cb"
EXPECTED_RESULTS_GZIP_SHA256="6290e2d867d4210bdef4b75042d8f27e29590f93945ef51013d531b94f074620"
EXPECTED_RESEARCH_RAW_SHA256="fc0e87a03825a944fab42a546a6d9b2d6fd649548fd48888c5ebef0942ffc640"
EXPECTED_RESEARCH_GZIP_SHA256="2791f6e8b51b75df5ef7ad9fb96272c84ee418cc615c45ab41d0b22c652b0823"
EXPECTED_CONFIRMED={1921, 1922, 1924, 1926, 1933, 1934, 1937, 1938, 1940, 1941, 1942, 1943, 1950, 1951, 1959, 1961, 1963, 1971, 1973, 1976, 1977, 1980}

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rgz=(E/"W3_BATCH_0033_RESULTS.csv.gz").read_bytes()
    qgz=(E/"W3_BATCH_0033_RESEARCH.tsv.gz").read_bytes()
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
    assert Counter(r["province"] for r in queue)==Counter({"湖北":60})
    assert [r["person_id"] for r in queue]==[r["person_id"] for r in results]
    assert len({r["person_id"] for r in results})==60
    assert {int(r["queue_order"]) for r in results if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED"}==EXPECTED_CONFIRMED
    for r in results:
        assert r["evidence_url"] or r["unresolved_reason"]
        assert r["evidence_grade"] in {"A","B"}
        assert "NAME_ONLY" not in r["identity_resolution"]
        if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED":
            assert r["current_organization"] and r["current_title"] and r["evidence_url"] and not r["unresolved_reason"]
        else:
            assert r["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE"
            assert not r["current_organization"] and not r["current_title"] and r["unresolved_reason"]
    assert Counter(r["current_verification_status"] for r in results)==Counter(
        {"UNRESOLVED_CURRENT_ORG_TITLE":38,"CURRENT_ORG_TITLE_CONFIRMED":22})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":56,"B":4})
    with (E/"W3_SEGMENT_INDEX.csv").open("r",encoding="utf-8-sig",newline="") as f:
        idx=list(csv.DictReader(f))
    expected_segments=[(1,1620),(1621,1680),(1681,1740),(1741,1800),(1801,1860),(1861,1920),(1921,1980)]
    for kind in ("ledger","overlay"):
        seg=[r for r in idx if r["kind"]==kind]
        seg.sort(key=lambda r:int(r["ordinal"]))
        assert [(int(r["queue_start"]),int(r["queue_end"])) for r in seg]==expected_segments
    print("PASS W3-BATCH-0033 next=1981")

if __name__=="__main__":
    main()
