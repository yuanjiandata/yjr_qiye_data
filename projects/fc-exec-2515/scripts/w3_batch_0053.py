#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0053."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=3121,3180
EXPECTED_RESULTS_SHA256="f786b1ff04694be566e766c28e5beed5f1818c465632a9f553793831c11eca33"
EXPECTED_RESEARCH_SHA256="327d93d4f97d310a5fb1670e5c8b3d26699985adcde2f71af5f3c82b3d0eae00"
CONFIRMED={
3124: ('贵州省工商业联合会', '秘书长', 'A'),
3125: ('贵州省工商业联合会', '主席', 'A'),
3129: ('贵州省总工会', '党组成员、副主席', 'B'),
3130: ('贵州省工商业联合会', '副主席', 'C'),
3131: ('贵州省工商业联合会', '秘书长', 'A'),
3135: ('世纪恒通科技股份有限公司', '董事、总经理', 'B'),
3137: ('贵州省工商业联合会', '主席', 'A'),
3141: ('贵州省总工会', '党组成员、副主席', 'B'),
3142: ('贵州省工商业联合会', '副主席', 'C'),
3145: ('云南省工商业联合会', '主席', 'A'),
3146: ('云南省工商业联合会', '党组书记', 'A'),
3148: ('云南省工商业联合会', '副主席、机关（非公）党委书记', 'A'),
3149: ('云南省工商业联合会', '副主席', 'A'),
3150: ('云南省工商业联合会', '党组成员、副主席', 'B'),
3152: ('云南省工商业联合会', '副主席', 'A'),
3153: ('云南省工商业联合会', '副主席', 'A'),
3155: ('云南省工商业联合会', '副主席', 'A'),
3157: ('云南省工商业联合会', '副主席', 'A'),
3158: ('云南省工商业联合会', '副主席', 'A'),
3162: ('云南省工商业联合会', '副主席', 'A'),
3169: ('云南省工商业联合会', '党组书记', 'A'),
3171: ('云南省工商业联合会', '副主席、机关（非公）党委书记', 'A'),
3172: ('云南省工商业联合会', '副主席', 'A'),
3173: ('云南省工商业联合会', '党组成员、副主席', 'B'),
3175: ('云南省总商会', '副会长', 'A'),
3177: ('云南省总商会', '副会长', 'A'),
3179: ('云南省总商会', '副会长', 'A'),
3180: ('云南省总商会', '副会长', 'A'),
}

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rb=(E/"W3_BATCH_0053_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0053_RESEARCH.tsv").read_bytes()
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
    assert Counter(r["province"] for r in queue)==Counter({"贵州":24,"云南":36})
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":32,"CURRENT_ORG_TITLE_CONFIRMED":28})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":53,"B":5,"C":2})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":32,"CONFIRMED":28})
    assert sum(r["mode"]=="FRESH_WEB_RESEARCH" for r in research)==50
    assert sum(r["mode"]=="REUSE_SEALED_CONFIRMED" for r in research)==7
    assert sum(r["mode"]=="REUSE_SEALED_UNRESOLVED" for r in research)==3
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
    for q in (3121,3122,3123,3127,3128,3132,3134,3136,3139,3140,3143,3144):
        assert byq[q]["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE"
    assert byq[3124]["current_organization"]=="贵州省工商业联合会"
    assert byq[3146]["current_title"]=="党组书记"
    assert byq[3149]["current_organization"]=="云南省工商业联合会"
    idx=list(csv.DictReader((E/"W3_SEGMENT_INDEX.csv").open("r",encoding="utf-8-sig",newline="")))
    for kind in ("ledger","overlay"):
        entries=sorted((r for r in idx if r["kind"]==kind),key=lambda r:int(r["ordinal"]))
        expected_start=1
        for e in entries:
            start,end,count=map(int,(e["queue_start"],e["queue_end"],e["row_count"]))
            assert start==expected_start,(kind,expected_start,start)
            assert end-start+1==count
            expected_start=end+1
        assert expected_start==3181
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0053"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0053_RESULTS.csv"
        assert int(last["queue_start"])==3121 and int(last["queue_end"])==3180
    print("PASS W3-BATCH-0053 rows=60 confirmed=28 unresolved=32 grades=A53/B5/C2 logical_end=3180")

if __name__=="__main__":
    main()
