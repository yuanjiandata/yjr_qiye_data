#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0047."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=2761,2820
EXPECTED_RESULTS_SHA256="a6bad54f9a9cc92e08266a89acba142d7b7e89389f33b51e609e8fafa665ff09"
EXPECTED_RESEARCH_SHA256="932a99d0248010499c6f36643d2e434d391067d7acdb2d3f53fd97f814650325"
CONFIRMED={2762: ('海口市工商业联合会', '党组书记', 'B'), 2769: ('海南省工商业联合会', '党组成员、专职秘书长', 'B'), 2771: ('海南广陵高科实业有限公司', '董事长', 'B'), 2772: ('四川省工商业联合会', '主席', 'B'), 2774: ('四川省工商业联合会', '一级巡视员', 'B'), 2776: ('四川省工商业联合会', '党组成员、副主席', 'B'), 2777: ('四川省工商业联合会', '党组成员、副主席', 'A'), 2778: ('通威集团', '董事局主席', 'A'), 2779: ('四川启阳汽车集团有限公司', '董事长', 'B'), 2783: ('四川铁骑力士实业有限公司', '董事长', 'C'), 2786: ('超宇集团有限公司', '董事长', 'C'), 2787: ('中诚投建工集团有限公司', '董事长', 'C'), 2793: ('海天集团', '董事长', 'B'), 2794: ('四川金象赛瑞化工股份有限公司', '总裁', 'B'), 2796: ('四川省工商业联合会', '副主席', 'B'), 2797: ('域上和美集团', '董事长', 'B'), 2798: ('四川省工商业联合会', '党组成员、副主席', 'B'), 2799: ('四川省工商业联合会', '主席', 'B'), 2818: ('星瑞集团', '董事长兼总裁', 'B')}

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rb=(E/"W3_BATCH_0047_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0047_RESEARCH.tsv").read_bytes()
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
    assert Counter(r["province"] for r in queue)==Counter({"海南":11,"四川":49})
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":41,"CURRENT_ORG_TITLE_CONFIRMED":19})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":43,"B":14,"C":3})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":41,"CONFIRMED":19})
    assert sum(r["mode"]=="FRESH_WEB_RESEARCH" for r in research)==49
    assert sum(r["mode"]=="REUSE_SEALED_CONFIRMED" for r in research)==3
    assert sum(r["mode"]=="REUSE_SEALED_UNRESOLVED" for r in research)==8
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
        assert expected_start==2821
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0047"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0047_RESULTS.csv"
        assert int(last["queue_start"])==2761 and int(last["queue_end"])==2820
    print("PASS W3-BATCH-0047 rows=60 confirmed=19 unresolved=41 grades=A43/B14/C3 logical_end=2820")

if __name__=="__main__":
    main()
