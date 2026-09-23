#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0066."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=3901,3960
EXPECTED_RESULTS_SHA256="0d22f02241acd5fb4a341c3ce3a427611e8260c6290573a0f5b2d95ef83b606d"
EXPECTED_RESEARCH_SHA256="eb818025a22431fa025e5c1bc319e03e70494461e53f4340553403126ae3ca35"
INNER_MONGOLIA_ANCHOR="https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_nm/202209/t20220919_313060.html"
SOURCE_MAP={3901: ('W3-BATCH-0065', 3853, 'ANG-1700'), 3917: ('W3-BATCH-0065', 3854, 'ANG-1743'), 3923: ('W3-BATCH-0065', 3855, 'ANG-1671'), 3929: ('W3-BATCH-0065', 3856, 'ANG-1662'), 3930: ('W3-BATCH-0065', 3857, 'ANG-1702'), 3931: ('W3-BATCH-0065', 3858, 'ANG-1741'), 3935: ('W3-BATCH-0065', 3859, 'ANG-1646'), 3936: ('W3-BATCH-0065', 3860, 'ANG-1644'), 3937: ('W3-BATCH-0065', 3861, 'ANG-1742'), 3938: ('W3-BATCH-0065', 3862, 'ANG-1672'), 3939: ('W3-BATCH-0064', 3815, 'ANG-1713'), 3940: ('W3-BATCH-0065', 3863, 'ANG-1714'), 3941: ('W3-BATCH-0065', 3864, 'ANG-1709'), 3942: ('W3-BATCH-0065', 3865, 'ANG-1708'), 3943: ('W3-BATCH-0065', 3866, 'ANG-1706'), 3944: ('W3-BATCH-0065', 3867, 'ANG-1707'), 3945: ('W3-BATCH-0065', 3868, 'ANG-1712'), 3946: ('W3-BATCH-0064', 3816, 'ANG-1710'), 3947: ('W3-BATCH-0065', 3869, 'ANG-1711'), 3948: ('W3-BATCH-0065', 3870, 'ANG-1647'), 3949: ('W3-BATCH-0064', 3813, 'ANG-1653'), 3950: ('W3-BATCH-0064', 3811, 'ANG-1715'), 3951: ('W3-BATCH-0065', 3871, 'ANG-1645'), 3952: ('W3-BATCH-0065', 3872, 'ANG-1652'), 3953: ('W3-BATCH-0065', 3873, 'ANG-1704'), 3954: ('W3-BATCH-0065', 3874, 'ANG-1687'), 3955: ('W3-BATCH-0065', 3875, 'ANG-1650'), 3956: ('W3-BATCH-0065', 3876, 'ANG-1651'), 3957: ('W3-BATCH-0065', 3877, 'ANG-1649'), 3958: ('W3-BATCH-0064', 3809, 'ANG-1666'), 3959: ('W3-BATCH-0065', 3878, 'ANG-1665'), 3960: ('W3-BATCH-0065', 3879, 'ANG-1664')}
FRESH_ORDERS=set(range(START,END+1))-set(SOURCE_MAP)
CONFIRMED_ORDERS={3939, 3946, 3949, 3917, 3950, 3951, 3958}

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rb=(E/"W3_BATCH_0066_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0066_RESEARCH.tsv.gz").read_bytes()
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
    assert Counter(r["mode"] for r in research)==Counter({"FRESH_WEB_RESEARCH":28,"REUSE_SEALED_UNRESOLVED":25,"REUSE_SEALED_CONFIRMED":7})
    for q,r in zip(queue,research):
        qo=int(q["queue_order"])
        assert r["identity_anchor_url"]==INNER_MONGOLIA_ANCHOR
        if qo in SOURCE_MAP:
            sg,sq,g=SOURCE_MAP[qo]
            assert r["source_gate"]==sg and int(r["source_queue_order"])==sq
            assert q["ambiguity_group_id"]==r["ambiguity_group_id"]==g
            assert r["mode"] in ("REUSE_SEALED_UNRESOLVED","REUSE_SEALED_CONFIRMED")
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
        assert expected_start==3961
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0066"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0066_RESULTS.csv"
        assert int(last["queue_start"])==3901 and int(last["queue_end"])==3960
    print("PASS W3-BATCH-0066 rows=60 confirmed=7 unresolved=53 grades=A56/B4/C0 logical_end=3960")

if __name__=="__main__":
    main()
