#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0052."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=3061,3120
EXPECTED_RESULTS_SHA256="e309904a9e9a2faae7b5a214c70c20eeeceb12993e05a616e5e849cf0ce0ad46"
EXPECTED_RESEARCH_SHA256="6fcf315e8b275a26793017281ae74e0c88e6f688e7245e3224300687440181f1"
CONFIRMED={
3063: ('海天集团', '董事长', 'B'),
3069: ('德阳市工商业联合会', '主席', 'A'),
3071: ('中诚投建工集团有限公司', '董事长', 'C'),
3072: ('资阳市工商业联合会', '主席', 'A'),
3073: ('四川金象赛瑞化工股份有限公司', '总裁', 'B'),
3075: ('四川省工商业联合会', '主席', 'B'),
3077: ('凉山州工商业联合会', '党组书记', 'C'),
3082: ('遂宁市工商业联合会', '主席、总商会会长', 'A'),
3084: ('凉山州工商业联合会', '主席', 'B'),
3095: ('四川省工商业联合会', '党组成员、副主席', 'B'),
3097: ('宜宾市工商业联合会', '党组书记', 'A'),
3102: ('泸州市工商业联合会', '主席、总商会会长', 'A'),
3105: ('四川铁骑力士实业有限公司', '董事长', 'C'),
3106: ('成都市工商业联合会', '党组书记', 'A'),
3110: ('四川家福来实业集团有限公司', '总经理', 'C'),
3111: ('四川省工商业联合会', '常委', 'C'),
3115: ('贵州省工商业联合会', '主席', 'A'),
3117: ('贵州省总工会', '党组成员、副主席', 'B'),
3118: ('贵州省工商业联合会', '副主席', 'C'),
3120: ('世纪恒通科技股份有限公司', '董事、总经理', 'B'),
}

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rb=(E/"W3_BATCH_0052_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0052_RESEARCH.tsv").read_bytes()
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
    assert Counter(r["province"] for r in queue)==Counter({"四川":54,"贵州":6})
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":40,"CURRENT_ORG_TITLE_CONFIRMED":20})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":47,"B":7,"C":6})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":40,"CONFIRMED":20})
    assert sum(r["mode"]=="FRESH_WEB_RESEARCH" for r in research)==6
    assert sum(r["mode"]=="REUSE_SEALED_CONFIRMED" for r in research)==16
    assert sum(r["mode"]=="REUSE_SEALED_UNRESOLVED" for r in research)==38
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
    assert byq[3116]["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE"
    assert byq[3119]["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE"
    assert byq[3117]["current_organization"]=="贵州省总工会"
    assert byq[3120]["current_organization"]=="世纪恒通科技股份有限公司"
    idx=list(csv.DictReader((E/"W3_SEGMENT_INDEX.csv").open("r",encoding="utf-8-sig",newline="")))
    for kind in ("ledger","overlay"):
        entries=sorted((r for r in idx if r["kind"]==kind),key=lambda r:int(r["ordinal"]))
        expected_start=1
        for e in entries:
            start,end,count=map(int,(e["queue_start"],e["queue_end"],e["row_count"]))
            assert start==expected_start,(kind,expected_start,start)
            assert end-start+1==count
            expected_start=end+1
        assert expected_start==3121
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0052"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0052_RESULTS.csv"
        assert int(last["queue_start"])==3061 and int(last["queue_end"])==3120
    print("PASS W3-BATCH-0052 rows=60 confirmed=20 unresolved=40 grades=A47/B7/C6 logical_end=3120")

if __name__=="__main__":
    main()
