#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0062."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=3661,3720
EXPECTED_RESULTS_SHA256="1f767056a6da35ba1c684f3bb9ea4ec2b5ee661ec008531e60302160fc4f7747"
EXPECTED_RESEARCH_SHA256="498e9a16d27cf9e46bfa5432a8880f00d60fe11399c0bac57388e9ad533b07da"
GANSU_ANCHOR="https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_gs/202207/t20220719_312778.html"
QINGHAI_ANCHOR="https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_qh/202207/t20220719_312776.html"
SOURCE_MAP={
    3661: ("W3-BATCH-0058",3463,"ANG-1489"),
    3662: ("W3-BATCH-0059",3527,"ANG-1583"),
    3663: ("W3-BATCH-0059",3499,"ANG-1491"),
    3664: ("W3-BATCH-0059",3482,"ANG-1545"),
    3665: ("W3-BATCH-0059",3490,"ANG-1537"),
}
CONFIRMED_ORDERS={3661,3662,3665,3666,3680,3714}

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rb=(E/"W3_BATCH_0062_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0062_RESEARCH.tsv.gz").read_bytes()
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
    assert Counter(r["province"] for r in queue)==Counter({"甘肃":5,"青海":55})
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":54,"CURRENT_ORG_TITLE_CONFIRMED":6})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":56,"B":4})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":54,"CONFIRMED":6})
    assert Counter(r["mode"] for r in research)==Counter({"FRESH_WEB_RESEARCH":55,"REUSE_SEALED_CONFIRMED":3,"REUSE_SEALED_UNRESOLVED":2})
    for q,r in zip(queue,research):
        qo=int(q["queue_order"])
        if qo in SOURCE_MAP:
            sg,sq,g=SOURCE_MAP[qo]
            assert r["source_gate"]==sg and int(r["source_queue_order"])==sq
            assert q["ambiguity_group_id"]==r["ambiguity_group_id"]==g
            assert r["identity_anchor_url"]==GANSU_ANCHOR
        else:
            assert r["mode"]=="FRESH_WEB_RESEARCH"
            assert not r["source_gate"] and not r["source_queue_order"]
            assert r["identity_anchor_url"]==QINGHAI_ANCHOR
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
        assert expected_start==3721
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0062"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0062_RESULTS.csv"
        assert int(last["queue_start"])==3661 and int(last["queue_end"])==3720
    print("PASS W3-BATCH-0062 rows=60 confirmed=6 unresolved=54 grades=A56/B4/C0 logical_end=3720")

if __name__=="__main__":
    main()
