#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0058."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=3421,3480
EXPECTED_RESULTS_SHA256="30fc844c248f905cc2df98fd8b8887cfd7720a13aadbd990fcdfdcfaea39b036"
EXPECTED_RESEARCH_SHA256="d6331a6a3c3e0583361cedd2cded93a69775624f4ec2126513eff919e41f4363"
YUNNAN_ANCHOR="https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_yn/202309/t20230914_316462.html"
SHAANXI_ANCHOR="https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_sn/202207/t20220727_312822.html"
GANSU_ANCHOR="https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_gs/202207/t20220719_312778.html"

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rb=(E/"W3_BATCH_0058_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0058_RESEARCH.tsv.gz").read_bytes()
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
    assert Counter(r["province"] for r in queue)==Counter({"云南":16,"陕西":4,"甘肃":40})
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":42,"CURRENT_ORG_TITLE_CONFIRMED":18})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":49,"B":11})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":42,"CONFIRMED":18})
    assert Counter(r["mode"] for r in research)==Counter({"FRESH_WEB_RESEARCH":44,"REUSE_SEALED_UNRESOLVED":11,"REUSE_SEALED_CONFIRMED":5})
    for i,r in enumerate(research[:16],start=3301):
        assert r["source_gate"]=="W3-BATCH-0056"
        assert int(r["source_queue_order"])==i
        assert r["identity_anchor_url"]==YUNNAN_ANCHOR
    for r in research[16:20]:
        assert not r["source_gate"] and not r["source_queue_order"]
        assert r["mode"]=="FRESH_WEB_RESEARCH"
        assert r["identity_anchor_url"]==SHAANXI_ANCHOR
    for r in research[20:]:
        assert not r["source_gate"] and not r["source_queue_order"]
        assert r["mode"]=="FRESH_WEB_RESEARCH"
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
    idx=list(csv.DictReader((E/"W3_SEGMENT_INDEX.csv").open("r",encoding="utf-8-sig",newline="")))
    for kind in ("ledger","overlay"):
        entries=sorted((r for r in idx if r["kind"]==kind),key=lambda r:int(r["ordinal"]))
        expected_start=1
        for e in entries:
            start,end,count=map(int,(e["queue_start"],e["queue_end"],e["row_count"]))
            assert start==expected_start,(kind,expected_start,start)
            assert end-start+1==count
            expected_start=end+1
        assert expected_start==3481
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0058"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0058_RESULTS.csv"
        assert int(last["queue_start"])==3421 and int(last["queue_end"])==3480
    print("PASS W3-BATCH-0058 rows=60 confirmed=18 unresolved=42 grades=A49/B11/C0 logical_end=3480")

if __name__=="__main__":
    main()
