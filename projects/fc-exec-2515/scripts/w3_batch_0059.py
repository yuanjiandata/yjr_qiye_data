#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0059."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=3481,3540
EXPECTED_RESULTS_SHA256="7f4a93c472a2ce0321fd439e63bd84d223007137609a00f89864e05c812b5c60"
EXPECTED_RESEARCH_SHA256="0365725601df0fd3d389519144e2d13e3950eb408a679218f0f97becf2f834b0"
GANSU_ANCHOR="https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_gs/202207/t20220719_312778.html"

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rb=(E/"W3_BATCH_0059_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0059_RESEARCH.tsv.gz").read_bytes()
    assert hashlib.sha256(rb).hexdigest()==EXPECTED_RESULTS_SHA256
    assert hashlib.sha256(qb).hexdigest()==EXPECTED_RESEARCH_SHA256
    results=list(csv.DictReader(rb.decode("utf-8-sig").splitlines()))
    research=list(csv.DictReader(gzip.decompress(qb).decode("utf-8-sig").splitlines(),delimiter="\t"))
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
    assert Counter(r["province"] for r in queue)==Counter({"甘肃":60})
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":53,"CURRENT_ORG_TITLE_CONFIRMED":7})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":54,"B":6})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":53,"CONFIRMED":7})
    assert Counter(r["mode"] for r in research)==Counter({"FRESH_WEB_RESEARCH":55,"REUSE_SEALED_UNRESOLVED":3,"REUSE_SEALED_CONFIRMED":2})
    for r in research[:55]:
        assert not r["source_gate"] and not r["source_queue_order"]
        assert r["mode"]=="FRESH_WEB_RESEARCH"
        assert r["identity_anchor_url"]==GANSU_ANCHOR
    expected_reuse=[("3536","3463","REUSE_SEALED_CONFIRMED"),("3537","3464","REUSE_SEALED_UNRESOLVED"),("3538","3465","REUSE_SEALED_UNRESOLVED"),("3539","3454","REUSE_SEALED_CONFIRMED"),("3540","3466","REUSE_SEALED_UNRESOLVED")]
    for r,(qo,src,mode) in zip(research[55:],expected_reuse):
        assert r["queue_order"]==qo
        assert r["source_gate"]=="W3-BATCH-0058"
        assert r["source_queue_order"]==src
        assert r["mode"]==mode
        assert r["identity_anchor_url"]==GANSU_ANCHOR
    for q,r in zip(queue,research):
        assert q["ambiguity_group_id"]==r["ambiguity_group_id"]
        assert q["name_normalized"]==r["name_normalized"]
    for r in results:
        assert "NAME_ONLY" not in r["identity_resolution"]
        if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED":
            assert r["current_organization"] and r["current_title"] and r["evidence_url"] and not r["unresolved_reason"]
        else:
            assert not r["current_organization"] and not r["current_title"] and not r["evidence_url"] and r["unresolved_reason"]
    assert {int(r["queue_order"]) for r in results if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED"}=={3485,3490,3507,3515,3527,3536,3539}
    idx=list(csv.DictReader((E/"W3_SEGMENT_INDEX.csv").open("r",encoding="utf-8-sig",newline="")))
    for kind in ("ledger","overlay"):
        entries=sorted((r for r in idx if r["kind"]==kind),key=lambda r:int(r["ordinal"]))
        expected_start=1
        for e in entries:
            start,end,count=map(int,(e["queue_start"],e["queue_end"],e["row_count"]))
            assert start==expected_start,(kind,expected_start,start)
            assert end-start+1==count
            expected_start=end+1
        assert expected_start==3541
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0059"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0059_RESULTS.csv"
        assert int(last["queue_start"])==3481 and int(last["queue_end"])==3540
    print("PASS W3-BATCH-0059 rows=60 confirmed=7 unresolved=53 grades=A54/B6/C0 logical_end=3540")

if __name__=="__main__":
    main()
