#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0057."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=3361,3420
EXPECTED_RESULTS_SHA256="253434989e69864867bb9571d4f16064271ceee7c4ef2c4811735572a54115da"
EXPECTED_RESEARCH_SHA256="94cafbbcac6b526e9ae8c4405f67c5e49fd0d8d4c2d1f8d09412809d45f07f27"
EXPECTED_SOURCE_GATE="W3-BATCH-0055"
IDENTITY_ANCHOR="https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_yn/202309/t20230914_316462.html"

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rb=(E/"W3_BATCH_0057_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0057_RESEARCH.tsv").read_bytes()
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
    assert Counter(r["province"] for r in queue)==Counter({"云南":60})
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":47,"CURRENT_ORG_TITLE_CONFIRMED":13})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":53,"B":7})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":47,"CONFIRMED":13})
    assert Counter(r["mode"] for r in research)==Counter({"REUSE_SEALED_UNRESOLVED":47,"REUSE_SEALED_CONFIRMED":13})
    assert all(r["source_gate"]==EXPECTED_SOURCE_GATE for r in research)
    assert [int(r["source_queue_order"]) for r in research]==list(range(3241,3301))
    assert all(r["identity_anchor_url"]==IDENTITY_ANCHOR for r in research)
    for q,r in zip(queue,research):
        assert q["ambiguity_group_id"]==r["ambiguity_group_id"]
        assert q["province"]=="云南"
        assert q["name_normalized"]==r["name_normalized"]
    for r in results:
        assert "NAME_ONLY" not in r["identity_resolution"]
        assert r["identity_resolution"].startswith("REUSED_SEALED_EVIDENCE_")
        if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED":
            assert r["current_organization"] and r["current_title"] and r["evidence_url"] and not r["unresolved_reason"]
        else:
            assert not r["current_organization"] and not r["current_title"] and not r["evidence_url"] and r["unresolved_reason"]
    idx=list(csv.DictReader((E/"W3_SEGMENT_INDEX.csv").open("r",encoding="utf-8-sig",newline="")))
    for kind in ("ledger","overlay"):
        entries=sorted((r for r in idx if r["kind"]==kind),key=lambda r:int(r["ordinal"]))
        expected_start=1
        for e in entries:
            start,end,count=map(int,(e["queue_start"],e["queue_end"],e["row_count"]))
            assert start==expected_start,(kind,expected_start,start)
            assert end-start+1==count
            expected_start=end+1
        assert expected_start==3421
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0057"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0057_RESULTS.csv"
        assert int(last["queue_start"])==3361 and int(last["queue_end"])==3420
    print("PASS W3-BATCH-0057 rows=60 confirmed=13 unresolved=47 grades=A53/B7/C0 logical_end=3420")

if __name__=="__main__":
    main()
