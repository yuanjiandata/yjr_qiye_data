#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0046."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=2701,2760
EXPECTED_RESULTS_SHA256="8e14595ba0e3139846c6453dd9daec1564c8f0def4375134605c11114edde86d"
EXPECTED_RESEARCH_SHA256="467c5f136b16beaf61a105276dabf94cb68fff973d643f472f434e5b36ff24a9"
CONFIRMED={2706: ('海南一龄医疗产业发展有限公司', '董事长', 'B'), 2707: ('海南金盘智能科技股份有限公司', '董事、高级副总裁', 'B'), 2713: ('海南省湖南商会', '会长', 'B'), 2725: ('海南金畅现代物流中心有限公司', '董事长', 'A'), 2738: ('海南省工商业联合会', '党组书记', 'A'), 2739: ('海南省工商业联合会', '党组成员、专职副主席', 'B'), 2740: ('海南传味文昌鸡产业股份有限公司', '董事长', 'B'), 2741: ('三亚市工商业联合会', '党组书记', 'A'), 2744: ('海南勤富食品股份有限公司', '董事长', 'B'), 2747: ('海南椰国食品有限公司', '总经理', 'A'), 2756: ('海南海丰渔业发展集团有限公司', '总经理', 'A'), 2759: ('海南信联盛融资担保有限公司', '董事长', 'B')}

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rb=(E/"W3_BATCH_0046_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0046_RESEARCH.tsv").read_bytes()
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
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":48,"CURRENT_ORG_TITLE_CONFIRMED":12})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":53,"B":7})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":48,"CONFIRMED":12})
    assert sum(r["mode"]=="REUSE_SEALED_CONFIRMED" for r in research)==12
    assert sum(r["mode"]=="REUSE_SEALED_UNRESOLVED" for r in research)==48
    assert all(r["identity_anchor_url"].startswith("https://www.acfic.org.cn/") for r in research)
    byq={int(r["queue_order"]):r for r in results}
    for q,(org,title,grade) in CONFIRMED.items():
        r=byq[q]
        assert r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED"
        assert (r["current_organization"],r["current_title"],r["evidence_grade"])==(org,title,grade)
        assert r["evidence_url"]
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
        assert expected_start==2761
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0046"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0046_RESULTS.csv"
        assert int(last["queue_start"])==2701 and int(last["queue_end"])==2760
    print("PASS W3-BATCH-0046 rows=60 confirmed=12 unresolved=48 grades=A53/B7 logical_end=2760")

if __name__=="__main__":
    main()
