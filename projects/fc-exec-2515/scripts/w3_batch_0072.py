#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0072."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=4261,4320
EXPECTED_RESULTS_SHA256="23bbcdbb74df2249a866a534231d4076e17990f8145b1e108a5c612ddcff1719"
EXPECTED_RESEARCH_SHA256="a283fdb51163558d0784b0dd671467f1a6be4ac7f18bfce444dfd2db2ec6004f"
NX_ANCHOR="https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_nx/202207/t20220719_102110.html"
SOURCE_MAP={4269: 4246, 4278: 4243, 4280: 4254, 4285: 4250, 4287: 4259, 4289: 4249, 4293: 4255, 4298: 4258, 4299: 4240, 4303: 4248, 4304: 4256, 4310: 4242, 4314: 4241, 4317: 4253, 4320: 4247, 4315: 4263}

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        all_queue=list(csv.DictReader(f))
    queue=all_queue[START-1:END]
    rb=(E/"W3_BATCH_0072_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0072_RESEARCH.tsv.gz").read_bytes()
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
    assert Counter(r["province"] for r in queue)==Counter({"宁夏":60})
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":49,"CURRENT_ORG_TITLE_CONFIRMED":10,"NO_CURRENT_ROLE_CONFIRMED":1})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":53,"B":7})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":49,"CONFIRMED":10,"NO_CURRENT_ROLE_CONFIRMED":1})
    assert Counter(r["mode"] for r in research)==Counter({"FRESH_WEB_RESEARCH":44,"REUSE_SEALED_UNRESOLVED":10,"REUSE_SEALED_CONFIRMED":4,"REUSE_SEALED_NO_CURRENT_ROLE":1,"REUSE_SAME_BATCH_CONFIRMED":1})
    for q,res,rr in zip(queue,results,research):
        qo=int(q["queue_order"])
        assert "NAME_ONLY" not in res["identity_resolution"]
        assert rr["identity_anchor_url"]==NX_ANCHOR
        if qo in SOURCE_MAP:
            sq=SOURCE_MAP[qo]
            source_q=all_queue[sq-1]
            assert source_q["province"]==q["province"]=="宁夏"
            assert source_q["name_normalized"]==q["name_normalized"]
            assert source_q["ambiguity_group_id"]==q["ambiguity_group_id"]
            assert int(rr["source_queue_order"])==sq
            if qo==4315:
                assert rr["source_gate"]=="W3-BATCH-0072"
                assert rr["mode"]=="REUSE_SAME_BATCH_CONFIRMED"
            else:
                assert rr["source_gate"]=="W3-BATCH-0071"
                assert rr["mode"].startswith("REUSE_SEALED_")
            assert not rr["search_query"]
        else:
            assert rr["mode"]=="FRESH_WEB_RESEARCH"
            assert not rr["source_gate"] and not rr["source_queue_order"]
            assert rr["search_query"]
        status=res["current_verification_status"]
        if status=="CURRENT_ORG_TITLE_CONFIRMED":
            assert res["current_organization"] and res["current_title"] and res["evidence_url"] and not res["unresolved_reason"]
            assert rr["decision"]=="CONFIRMED"
        elif status=="NO_CURRENT_ROLE_CONFIRMED":
            assert not res["current_organization"] and not res["current_title"] and res["evidence_url"] and not res["unresolved_reason"]
            assert rr["decision"]=="NO_CURRENT_ROLE_CONFIRMED"
        else:
            assert not res["current_organization"] and not res["current_title"] and not res["evidence_url"] and res["unresolved_reason"]
            assert rr["decision"]=="UNRESOLVED"
    idx=list(csv.DictReader((E/"W3_SEGMENT_INDEX.csv").open("r",encoding="utf-8-sig",newline="")))
    for kind in ("ledger","overlay"):
        entries=sorted((r for r in idx if r["kind"]==kind),key=lambda r:int(r["ordinal"]))
        expected_start=1
        for e in entries:
            start,end,count=map(int,(e["queue_start"],e["queue_end"],e["row_count"]))
            assert start==expected_start,(kind,expected_start,start)
            assert end-start+1==count
            expected_start=end+1
        assert expected_start==4321
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0072"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0072_RESULTS.csv"
        assert int(last["queue_start"])==4261 and int(last["queue_end"])==4320
    print("PASS W3-BATCH-0072 rows=60 current=10 no_current=1 unresolved=49 grades=A53/B7/C0 logical_end=4320")

if __name__=="__main__":
    main()
