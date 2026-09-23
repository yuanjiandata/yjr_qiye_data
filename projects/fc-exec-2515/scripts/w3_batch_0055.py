#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0055."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=3241,3300
EXPECTED_RESULTS_SHA256="9a0902f236c6f19c920de685315e3ef1e95ba1e12caaefa81355f36c61dee628"
EXPECTED_RESEARCH_SHA256="22948333c7d3b99d52200cdd8601cf52f06c50a73e539d0924486a8a1d5a0a93"
CONFIRMED={
    3248: ('普洱市工商业联合会（总商会）', '主席（会长）', 'B'),
    3260: ('云南省总商会', '副会长', 'A'),
    3261: ('云南省工商业联合会（总商会）', '副会长', 'B'),
    3262: ('云南省工商业联合会', '副主席', 'A'),
    3265: ('云南省工商业联合会（总商会）', '副会长', 'B'),
    3273: ('云南省工商业联合会', '副主席、机关（非公）党委书记', 'A'),
    3277: ('云南省总商会', '副会长', 'A'),
    3278: ('云南省总商会', '副会长', 'A'),
    3293: ('云南省工商业联合会', '主席', 'A'),
    3295: ('昆明理工恒达科技股份有限公司', '董事长', 'B'),
    3298: ('云南省工商业联合会', '副主席', 'B'),
    3299: ('云南省工商业联合会', '党组成员、副主席', 'B'),
    3300: ('云南人民电力电气有限公司', '董事长', 'B'),
}

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rb=(E/"W3_BATCH_0055_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0055_RESEARCH.tsv").read_bytes()
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
    assert Counter(r["mode"] for r in research)==Counter({"FRESH_WEB_RESEARCH":39,"REUSE_SEALED_CONFIRMED":10,"REUSE_SEALED_UNRESOLVED":11})
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
    assert byq[3245]["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE"
    assert byq[3254]["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE"
    assert byq[3264]["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE"
    assert byq[3300]["current_organization"]=="云南人民电力电气有限公司"
    idx=list(csv.DictReader((E/"W3_SEGMENT_INDEX.csv").open("r",encoding="utf-8-sig",newline="")))
    for kind in ("ledger","overlay"):
        entries=sorted((r for r in idx if r["kind"]==kind),key=lambda r:int(r["ordinal"]))
        expected_start=1
        for e in entries:
            start,end,count=map(int,(e["queue_start"],e["queue_end"],e["row_count"]))
            assert start==expected_start,(kind,expected_start,start)
            assert end-start+1==count
            expected_start=end+1
        assert expected_start==3301
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0055"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0055_RESULTS.csv"
        assert int(last["queue_start"])==3241 and int(last["queue_end"])==3300
    print("PASS W3-BATCH-0055 rows=60 confirmed=13 unresolved=47 grades=A53/B7/C0 logical_end=3300")

if __name__=="__main__":
    main()
