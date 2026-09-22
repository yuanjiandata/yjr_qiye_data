#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0044."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=2581,2640
EXPECTED_RESULTS_SHA256="d1c01e1fbb263f9c5bc9405259cb0fc668b448124ebea8e7241fdeb2f7cdc6a5"
EXPECTED_RESEARCH_SHA256="0bd2878b831df750c53274c733629d876abc79d1f88a3eac38a363f693057295"

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rb=(E/"W3_BATCH_0044_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0044_RESEARCH.tsv").read_bytes()
    assert hashlib.sha256(rb).hexdigest()==EXPECTED_RESULTS_SHA256
    assert hashlib.sha256(qb).hexdigest()==EXPECTED_RESEARCH_SHA256
    results=list(csv.DictReader(rb.decode("utf-8-sig").splitlines()))
    research=list(csv.DictReader(qb.decode("utf-8-sig").splitlines(),delimiter="\t"))
    expected=list(range(START,END+1))
    assert len(queue)==len(results)==len(research)==60
    assert [int(r["queue_order"]) for r in queue]==expected
    assert [int(r["queue_order"]) for r in results]==expected
    assert [int(r["queue_order"]) for r in research]==expected
    assert [r["person_id"] for r in results]==[r["person_id"] for r in queue]
    assert [r["person_id"] for r in research]==[r["person_id"] for r in queue]
    assert [r["name_normalized"] for r in research]==[r["name_normalized"] for r in queue]
    assert [r["ambiguity_group_id"] for r in research]==[r["ambiguity_group_id"] for r in queue]
    assert [r["province"] for r in results]==[r["province"] for r in queue]
    assert [int(r["excel_row"]) for r in results]==[int(r["excel_row"]) for r in queue]
    assert {r["priority"] for r in queue}=={"P1_IDENTITY"}
    assert Counter(r["province"] for r in queue)==Counter({"海南":60})
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":47,"CURRENT_ORG_TITLE_CONFIRMED":13})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":52,"B":8})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":47,"CONFIRMED":13})
    assert all(r["identity_anchor_url"].startswith("https://www.acfic.org.cn/") for r in research)
    assert sum(r["mode"]=="FRESH_RESEARCH" for r in research)==36
    assert sum(r["mode"].startswith("REUSE_") for r in research)==24
    assert sum(r["mode"]=="REUSE_SEALED_CONFIRMED" for r in research)==11
    assert sum(r["mode"]=="REUSE_SEALED_UNRESOLVED" for r in research)==13
    for r in results:
        assert "NAME_ONLY" not in r["identity_resolution"]
        if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED":
            assert r["current_organization"] and r["current_title"] and r["evidence_url"] and not r["unresolved_reason"]
        else:
            assert not r["current_organization"] and not r["current_title"] and r["unresolved_reason"]
    idx=list(csv.DictReader((E/"W3_SEGMENT_INDEX.csv").open("r",encoding="utf-8-sig",newline="")))
    for kind in ("ledger","overlay"):
        entries=sorted((r for r in idx if r["kind"]==kind),key=lambda r:int(r["ordinal"]))
        expected_start=1
        for e in entries:
            start,end,count=map(int,(e["queue_start"],e["queue_end"],e["row_count"]))
            assert start==expected_start,(kind,expected_start,start)
            assert end-start+1==count
            expected_start=end+1
        assert expected_start==2641
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0044"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0044_RESULTS.csv"
        assert int(last["queue_start"])==2581 and int(last["queue_end"])==2640
    print("PASS W3-BATCH-0044 rows=60 confirmed=13 unresolved=47 grades=A52/B8 logical_end=2640")

if __name__=="__main__":
    main()
