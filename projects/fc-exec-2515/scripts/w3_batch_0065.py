#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0065."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=3841,3900
EXPECTED_RESULTS_SHA256="cbdfe3a9fc4b90e274c71cea5c6eccac9c0a6a9dc29ecdfeff42669c4bf20cab"
EXPECTED_RESEARCH_SHA256="ce30bb83a7195959e0df59e73d144659ce03a868209e58709c9b4a2a52a75806"
INNER_MONGOLIA_ANCHOR="https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_nm/202209/t20220919_313060.html"
SOURCE_MAP={3859: (3835, 'ANG-1646'), 3860: (3836, 'ANG-1644'), 3861: (3837, 'ANG-1742'), 3867: (3838, 'ANG-1707'), 3868: (3839, 'ANG-1712'), 3870: (3840, 'ANG-1647')}
FRESH_ORDERS=set(range(START,END+1))-set(SOURCE_MAP)
CONFIRMED_ORDERS={3888, 3891, 3847, 3848, 3881, 3854, 3871}

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rb=(E/"W3_BATCH_0065_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0065_RESEARCH.tsv.gz").read_bytes()
    assert hashlib.sha256(rb).hexdigest()==EXPECTED_RESULTS_SHA256
    assert hashlib.sha256(qb).hexdigest()==EXPECTED_RESEARCH_SHA256
    results=list(csv.DictReader(rb.decode("utf-8").splitlines()))
    research=list(csv.DictReader(gzip.decompress(qb).decode("utf-8").splitlines(),delimiter="\t"))
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
    assert Counter(r["province"] for r in queue)==Counter({"内蒙古":60})
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":53,"CURRENT_ORG_TITLE_CONFIRMED":7})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":56,"B":4})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":53,"CONFIRMED":7})
    assert Counter(r["mode"] for r in research)==Counter({"FRESH_WEB_RESEARCH":54,"REUSE_SEALED_UNRESOLVED":6})
    for q,r in zip(queue,research):
        qo=int(q["queue_order"])
        assert r["identity_anchor_url"]==INNER_MONGOLIA_ANCHOR
        if qo in SOURCE_MAP:
            sq,g=SOURCE_MAP[qo]
            assert r["source_gate"]=="W3-BATCH-0064" and int(r["source_queue_order"])==sq
            assert q["ambiguity_group_id"]==r["ambiguity_group_id"]==g
            assert r["mode"]=="REUSE_SEALED_UNRESOLVED"
            assert not r["search_query"]
        else:
            assert qo in FRESH_ORDERS
            assert r["mode"]=="FRESH_WEB_RESEARCH"
            assert not r["source_gate"] and not r["source_queue_order"]
            assert r["search_query"]
    for r in results:
        assert "NAME_ONLY" not in r["identity_resolution"]
        if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED":
            assert r["current_organization"] and r["current_title"] and r["evidence_url"] and not r["unresolved_reason"]
        else:
            assert not r["current_organization"] and not r["current_title"] and not r["evidence_url"] and r["unresolved_reason"]
    assert {int(r["queue_order"]) for r in results if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED"}==CONFIRMED_ORDERS
    idx=list(csv.DictReader((E/"W3_SEGMENT_INDEX.csv").open("r",encoding="utf-8-sig",newline="")))
    for kind in ("ledger","overlay"):
        entries=sorted((r for r in idx if r["kind"]==kind),key=lambda r:int(r["ordinal"]))
        expected_start=1
        for e in entries:
            start,end,count=map(int,(e["queue_start"],e["queue_end"],e["row_count"]))
            assert start==expected_start,(kind,expected_start,start)
            assert end-start+1==count
            expected_start=end+1
        assert expected_start==3901
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0065"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0065_RESULTS.csv"
        assert int(last["queue_start"])==3841 and int(last["queue_end"])==3900
    print("PASS W3-BATCH-0065 rows=60 confirmed=7 unresolved=53 grades=A56/B4/C0 logical_end=3900")

if __name__=="__main__":
    main()
