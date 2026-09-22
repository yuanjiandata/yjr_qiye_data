#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0045."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=2641,2700
EXPECTED_RESULTS_SHA256="6c2f45567d33741a59ec4cf8759c912a3b8380597fe7b546a189be7cc1e75b38"
EXPECTED_RESEARCH_SHA256="f1703897e4c4a08fc1652fa623948dbcbc749a9404a12eb3766f3337bc558f34"
FRESH_CONFIRMED={
    2646: ("三亚市工商业联合会","党组书记","A"),
    2649: ("海南勤富食品股份有限公司","董事长","B"),
    2652: ("海南椰国食品有限公司","总经理","A"),
    2667: ("海口市工商业联合会","党组书记","B"),
}

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rb=(E/"W3_BATCH_0045_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0045_RESEARCH.tsv").read_bytes()
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
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":42,"CURRENT_ORG_TITLE_CONFIRMED":18})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":50,"B":10})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":42,"CONFIRMED":18})
    assert all(r["identity_anchor_url"].startswith("https://www.acfic.org.cn/") for r in research)
    assert sum(r["mode"]=="FRESH_RESEARCH" for r in research)==25
    assert sum(r["mode"].startswith("REUSE_") for r in research)==35
    assert sum(r["mode"]=="REUSE_SEALED_CONFIRMED" for r in research)==14
    assert sum(r["mode"]=="REUSE_SEALED_UNRESOLVED" for r in research)==21
    byq={int(r["queue_order"]):r for r in results}
    for q,(org,title,grade) in FRESH_CONFIRMED.items():
        r=byq[q]
        assert r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED"
        assert (r["current_organization"],r["current_title"],r["evidence_grade"])==(org,title,grade)
        assert r["evidence_url"]
    assert byq[2679]["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE"
    assert byq[2680]["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE"
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
        assert expected_start==2701
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0045"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0045_RESULTS.csv"
        assert int(last["queue_start"])==2641 and int(last["queue_end"])==2700
    print("PASS W3-BATCH-0045 rows=60 confirmed=18 unresolved=42 grades=A50/B10 logical_end=2700")

if __name__=="__main__":
    main()
