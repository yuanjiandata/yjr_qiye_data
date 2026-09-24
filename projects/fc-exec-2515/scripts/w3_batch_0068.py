#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0068."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=4021,4080
EXPECTED_RESULTS_SHA256="84f7fcd77b09cee71e8809cd53705de441c77c39bc4b4cc92bbfa8d440caa58e"
EXPECTED_RESEARCH_SHA256="ad8569b69afd42ac5853259b7a2efae2a92ad8b8691ec6c188f68f0a9d8cadd2"
INNER_MONGOLIA_ANCHOR="https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_nm/202209/t20220919_313060.html"
GUANGXI_ANCHOR="https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_gx/202309/t20230914_316460.html"
SOURCE_MAP={4021: ('W3-BATCH-0066', 3924, 'ANG-1670'), 4022: ('W3-BATCH-0064', 3810, 'ANG-1701'), 4023: ('W3-BATCH-0064', 3832, 'ANG-1723'), 4024: ('W3-BATCH-0066', 3925, 'ANG-1724'), 4025: ('W3-BATCH-0064', 3833, 'ANG-1739'), 4026: ('W3-BATCH-0066', 3926, 'ANG-1737'), 4027: ('W3-BATCH-0066', 3927, 'ANG-1738'), 4028: ('W3-BATCH-0066', 3928, 'ANG-1740'), 4029: ('W3-BATCH-0064', 3834, 'ANG-1717'), 4030: ('W3-BATCH-0066', 3929, 'ANG-1662'), 4031: ('W3-BATCH-0064', 3814, 'ANG-1705'), 4032: ('W3-BATCH-0066', 3930, 'ANG-1702'), 4033: ('W3-BATCH-0066', 3931, 'ANG-1741'), 4034: ('W3-BATCH-0066', 3932, 'ANG-1725'), 4035: ('W3-BATCH-0066', 3933, 'ANG-1736'), 4036: ('W3-BATCH-0066', 3934, 'ANG-1744')}
FRESH_ORDERS=set(range(4037,4081))
CONFIRMED_ORDERS={4064, 4066, 4037, 4039, 4072, 4073, 4044, 4045, 4047, 4022, 4023, 4025, 4058, 4029, 4063}
FRESH_EXPECTED={4037: ('广西壮族自治区工商业联合会', '主席', 'A', 'https://www.acfic.org.cn/gdgslgz/gx/bjgslgz/202601/t20260114_323788.html'), 4039: ('广西壮族自治区工商业联合会', '党组成员、副主席', 'A', 'https://wap.acfic.org.cn/gdgslgz_14277/202605/t20260526_326371.html'), 4044: ('澳门广西工商业联合会', '主席', 'A', 'https://www.lztz.gov.cn/gzsx/202604/t20260427_3745336.html'), 4045: ('广西力源宝科技有限公司', '董事长', 'B', 'https://gx.people.com.cn/n2/2026/0204/c179464-41493167.html'), 4047: ('双英集团股份有限公司', '董事长', 'B', 'https://www.gxnews.com.cn/staticpages/20260310/newgx69afbcf4-21917525.shtml'), 4058: ('广西华控投资集团有限公司', '董事长', 'B', 'https://gx.people.com.cn/n2/2026/0206/c179409-41494930.html'), 4063: ('来宾东糖集团', '党委书记', 'B', 'https://news.gxnews.com.cn/staticpages/20260714/newgx6a559c64-21969711.shtml'), 4064: ('深圳市锦绣前程人才服务集团有限公司', '董事长', 'B', 'https://www.chinanews.com/cj/2026/03-09/10583901.shtml'), 4066: ('广西扬翔集团股份有限公司', '董事长', 'B', 'https://gx.people.com.cn/n2/2026/0202/c179464-41490892.html'), 4072: ('广西壮族自治区工商业联合会', '主席', 'A', 'https://www.acfic.org.cn/gdgslgz/gx/bjgslgz/202601/t20260114_323788.html'), 4073: ('广西壮族自治区工商业联合会', '党组成员、副主席', 'A', 'https://wap.acfic.org.cn/gdgslgz_14277/202605/t20260526_326371.html')}
OUTCOME_FIELDS=("current_organization","current_title","current_verification_status","evidence_grade","evidence_url","unresolved_reason")

def load_results(gate):
    p=E/(gate.replace("-","_")+"_RESULTS.csv")
    if not p.exists():
        p=E/(gate.replace("-","_")+"_RESULTS.csv.gz")
    if p.suffix==".gz":
        with gzip.open(p,"rt",encoding="utf-8-sig",newline="") as f:
            return {int(r["queue_order"]):r for r in csv.DictReader(f)}
    with p.open("r",encoding="utf-8-sig",newline="") as f:
        return {int(r["queue_order"]):r for r in csv.DictReader(f)}

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        all_queue=list(csv.DictReader(f))
    queue=all_queue[START-1:END]
    rb=(E/"W3_BATCH_0068_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0068_RESEARCH.tsv.gz").read_bytes()
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
    assert Counter(r["province"] for r in queue)==Counter({"内蒙古":16,"广西":44})
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":45,"CURRENT_ORG_TITLE_CONFIRMED":15})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":52,"B":8})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":45,"CONFIRMED":15})
    assert Counter(r["mode"] for r in research)==Counter({"FRESH_WEB_RESEARCH":44,"REUSE_SEALED_UNRESOLVED":12,"REUSE_SEALED_CONFIRMED":4})
    source_cache={}
    for q,res,rr in zip(queue,results,research):
        qo=int(q["queue_order"])
        assert "NAME_ONLY" not in res["identity_resolution"]
        if qo in SOURCE_MAP:
            sg,sq,g=SOURCE_MAP[qo]
            assert rr["identity_anchor_url"]==INNER_MONGOLIA_ANCHOR
            assert rr["source_gate"]==sg and int(rr["source_queue_order"])==sq
            assert q["ambiguity_group_id"]==rr["ambiguity_group_id"]==g
            assert not rr["search_query"]
            source_q=all_queue[sq-1]
            assert source_q["province"]==q["province"]
            assert source_q["name_normalized"]==q["name_normalized"]
            assert source_q["ambiguity_group_id"]==q["ambiguity_group_id"]
            if sg not in source_cache:
                source_cache[sg]=load_results(sg)
            src=source_cache[sg][sq]
            for field in OUTCOME_FIELDS:
                assert res[field]==src[field],(qo,field,res[field],src[field])
        else:
            assert qo in FRESH_ORDERS
            assert rr["identity_anchor_url"]==GUANGXI_ANCHOR
            assert rr["mode"]=="FRESH_WEB_RESEARCH"
            assert not rr["source_gate"] and not rr["source_queue_order"]
            assert rr["search_query"]
            if qo in FRESH_EXPECTED:
                org,title,grade,url=FRESH_EXPECTED[qo]
                assert (res["current_organization"],res["current_title"],res["evidence_grade"],res["evidence_url"])==(org,title,grade,url)
            else:
                assert res["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE"
                assert not res["current_organization"] and not res["current_title"] and not res["evidence_url"] and res["unresolved_reason"]
        confirmed=res["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED"
        assert rr["decision"]==("CONFIRMED" if confirmed else "UNRESOLVED")
        if confirmed:
            assert res["current_organization"] and res["current_title"] and res["evidence_url"] and not res["unresolved_reason"]
        else:
            assert not res["current_organization"] and not res["current_title"] and not res["evidence_url"] and res["unresolved_reason"]
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
        assert expected_start==4081
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0068"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0068_RESULTS.csv"
        assert int(last["queue_start"])==4021 and int(last["queue_end"])==4080
    print("PASS W3-BATCH-0068 rows=60 confirmed=15 unresolved=45 grades=A52/B8/C0 logical_end=4080")

if __name__=="__main__":
    main()
