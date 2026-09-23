#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0049."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=2881,2940
EXPECTED_RESULTS_SHA256="9638968c923e46dab018363d882fb31fa80f54e534e3f8c2ce0b0de0ca06e7dc"
EXPECTED_RESEARCH_SHA256="cfb33d1f41db347d0eadf06d39ddcde5e2316334ef5bc7021e6d55ac7b79430f"
CONFIRMED={2913: ('德阳市工商业联合会', '主席', 'A'), 2915: ('资阳市工商业联合会', '主席', 'A'), 2917: ('凉山州工商业联合会', '党组书记', 'C'), 2921: ('遂宁市工商业联合会', '主席、总商会会长', 'A'), 2923: ('凉山州工商业联合会', '主席', 'B'), 2936: ('宜宾市工商业联合会', '党组书记', 'A'), 2934: ('四川省工商业联合会', '党组成员、副主席', 'B')}

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rb=(E/"W3_BATCH_0049_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0049_RESEARCH.tsv").read_bytes()
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
    assert Counter(r["province"] for r in queue)==Counter({"四川":60})
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":53,"CURRENT_ORG_TITLE_CONFIRMED":7})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":57,"B":2,"C":1})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":53,"CONFIRMED":7})
    assert sum(r["mode"]=="FRESH_WEB_RESEARCH" for r in research)==48
    assert sum(r["mode"]=="REUSE_SEALED_CONFIRMED" for r in research)==1
    assert sum(r["mode"]=="REUSE_SEALED_UNRESOLVED" for r in research)==11
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
        assert expected_start==2941
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0049"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0049_RESULTS.csv"
        assert int(last["queue_start"])==2881 and int(last["queue_end"])==2940
    print("PASS W3-BATCH-0049 rows=60 confirmed=7 unresolved=53 grades=A57/B2/C1 logical_end=2940")

if __name__=="__main__":
    main()
