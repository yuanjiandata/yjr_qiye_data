#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0054."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=3181,3240
EXPECTED_RESULTS_SHA256="3af29d8d847c54d31d67baa407230221280458f662e2731ca0dcaeff1dee24de"
EXPECTED_RESEARCH_SHA256="32e56c783612155567d2535fa09dbf1ddf858b8476880d6dd2e5fb7c67ad12dd"
CONFIRMED={
    3181: ('云南省工商业联合会（总商会）', '企业家副主席（副会长）', 'B'),
    3183: ('云南省总商会', '副会长', 'A'),
    3184: ('云南省总商会', '副会长', 'A'),
    3185: ('昆明温州总商会', '会长', 'A'),
    3186: ('云南大益茶业集团有限公司', '轮值总裁', 'B'),
    3189: ('昆明理工恒达科技股份有限公司', '董事长', 'B'),
    3190: ('云南省工商业联合会（总商会）', '副会长', 'B'),
    3192: ('云南省总商会', '副会长', 'A'),
    3194: ('云南省工商业联合会', '副主席', 'B'),
    3196: ('云南省工商业联合会', '党组成员、副主席', 'B'),
    3200: ('云南省工商业联合会（总商会）', '企业家副主席（副会长）', 'B'),
    3203: ('昆明温州总商会', '会长', 'A'),
    3206: ('云南省工商业联合会', '副主席', 'A'),
    3214: ('云南省工商业联合会（总商会）', '企业家副主席（副会长）', 'B'),
    3216: ('云南省工商业联合会', '副主席', 'A'),
    3217: ('云南省工商业联合会', '副主席', 'A'),
    3218: ('云南省工商业联合会', '副主席', 'A'),
    3222: ('云南省总商会', '副会长', 'A'),
    3228: ('云南省总商会', '副会长', 'A'),
    3229: ('云南省工商业联合会（总商会）', '副会长', 'B'),
    3230: ('云南省工商业联合会', '副主席', 'A'),
    3235: ('云南省工商业联合会', '副主席', 'A'),
    3239: ('云南省总商会', '副会长', 'A')
}

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rb=(E/"W3_BATCH_0054_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0054_RESEARCH.tsv").read_bytes()
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
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":37,"CURRENT_ORG_TITLE_CONFIRMED":23})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":51,"B":9})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":37,"CONFIRMED":23})
    assert sum(r["mode"]=="FRESH_WEB_RESEARCH" for r in research)==45
    assert sum(r["mode"]=="REUSE_SEALED_CONFIRMED" for r in research)==9
    assert sum(r["mode"]=="REUSE_SEALED_UNRESOLVED" for r in research)==5
    assert sum(r["mode"]=="CURRENT_SOURCE_RECHECK_CONFIRMED" for r in research)==1
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
    assert byq[3181]["current_title"]=="企业家副主席（副会长）"
    assert byq[3185]["current_organization"]=="昆明温州总商会"
    assert byq[3186]["current_title"]=="轮值总裁"
    assert byq[3189]["current_organization"]=="昆明理工恒达科技股份有限公司"
    assert byq[3229]["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED"
    idx=list(csv.DictReader((E/"W3_SEGMENT_INDEX.csv").open("r",encoding="utf-8-sig",newline="")))
    for kind in ("ledger","overlay"):
        entries=sorted((r for r in idx if r["kind"]==kind),key=lambda r:int(r["ordinal"]))
        expected_start=1
        for e in entries:
            start,end,count=map(int,(e["queue_start"],e["queue_end"],e["row_count"]))
            assert start==expected_start,(kind,expected_start,start)
            assert end-start+1==count
            expected_start=end+1
        assert expected_start==3241
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0054"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0054_RESULTS.csv"
        assert int(last["queue_start"])==3181 and int(last["queue_end"])==3240
    print("PASS W3-BATCH-0054 rows=60 confirmed=23 unresolved=37 grades=A51/B9/C0 logical_end=3240")

if __name__=="__main__":
    main()
