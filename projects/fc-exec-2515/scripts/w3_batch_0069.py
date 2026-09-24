#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0069."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=4081,4140
EXPECTED_RESULTS_SHA256="dbdffd75df0758c3ffdd9754cb1f41aa8a47efc28a99dc46278ebf6b981d392d"
EXPECTED_RESEARCH_SHA256="da07da114f0a9863c3e8e1ac6b8b3065bc825897a81feba088b25f6399d00534"
GUANGXI_ANCHOR="https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_gx/202309/t20230914_316460.html"
SOURCE_MAP={4113: 4043, 4114: 4044, 4115: 4045, 4116: 4046, 4117: 4047, 4118: 4048, 4119: 4049, 4120: 4050, 4121: 4051, 4122: 4052, 4123: 4053, 4124: 4054, 4125: 4055, 4126: 4056, 4127: 4057, 4128: 4058, 4129: 4059, 4130: 4060, 4131: 4061, 4132: 4062, 4133: 4063, 4134: 4064, 4135: 4065, 4136: 4066, 4137: 4067, 4138: 4068, 4139: 4069, 4140: 4070}
FRESH_ORDERS=set(range(4081,4113))
FRESH_EXPECTED={4087: ('柳州市工商业联合会', '主席', 'A', 'https://www.lztz.gov.cn/gzsx/202604/t20260427_3745336.html'), 4088: ('柳州市工商业联合会', '党组书记', 'A', 'https://lztz.gov.cn/gzsx/202607/t20260715_3773529.html'), 4089: ('桂林市工商业联合会', '主席', 'B', 'https://finance.sina.com.cn/wm/2026-05-23/doc-inhywcxs5487324.shtml'), 4091: ('梧州市工商业联合会', '主席', 'B', 'https://www.chinanews.com/gn/2026/02-04/10565925.shtml'), 4103: ('百色市工商业联合会', '主席', 'B', 'https://www.sohu.com/a/996544127_121106875'), 4107: ('河池市工商业联合会', '主席', 'B', 'https://finance.sina.com.cn/wm/2026-04-25/doc-inhvsuvi0888104.shtml'), 4109: ('来宾市工商业联合会', '主席', 'B', 'https://finance.sina.com.cn/jjxw/2026-07-31/doc-iniktkau9218193.shtml'), 4112: ('崇左市工商业联合会', '党组书记', 'B', 'https://finance.sina.com.cn/wm/2026-05-23/doc-inhywcxs5487324.shtml')}
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
    rb=(E/"W3_BATCH_0069_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0069_RESEARCH.tsv.gz").read_bytes()
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
    assert Counter(r["province"] for r in queue)==Counter({"广西":60})
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":45,"CURRENT_ORG_TITLE_CONFIRMED":15})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":48,"B":12})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":45,"CONFIRMED":15})
    assert Counter(r["mode"] for r in research)==Counter({"FRESH_WEB_RESEARCH":32,"REUSE_SEALED_UNRESOLVED":21,"REUSE_SEALED_CONFIRMED":7})
    src=load_results("W3-BATCH-0068")
    for q,res,rr in zip(queue,results,research):
        qo=int(q["queue_order"])
        assert rr["identity_anchor_url"]==GUANGXI_ANCHOR
        assert "NAME_ONLY" not in res["identity_resolution"]
        if qo in SOURCE_MAP:
            sq=SOURCE_MAP[qo]
            assert rr["source_gate"]=="W3-BATCH-0068" and int(rr["source_queue_order"])==sq
            assert not rr["search_query"]
            source_q=all_queue[sq-1]
            assert source_q["province"]==q["province"]
            assert source_q["name_normalized"]==q["name_normalized"]
            assert source_q["ambiguity_group_id"]==q["ambiguity_group_id"]
            for field in OUTCOME_FIELDS:
                assert res[field]==src[sq][field],(qo,field,res[field],src[sq][field])
        else:
            assert qo in FRESH_ORDERS and rr["mode"]=="FRESH_WEB_RESEARCH"
            assert not rr["source_gate"] and not rr["source_queue_order"] and rr["search_query"]
            if qo in FRESH_EXPECTED:
                org,title,grade,url=FRESH_EXPECTED[qo]
                assert (res["current_organization"],res["current_title"],res["evidence_grade"],res["evidence_url"])==(org,title,grade,url)
                assert res["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED"
            else:
                assert res["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE"
                assert not res["current_organization"] and not res["current_title"] and not res["evidence_url"] and res["unresolved_reason"]
        confirmed=res["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED"
        assert rr["decision"]==("CONFIRMED" if confirmed else "UNRESOLVED")
        if confirmed:
            assert res["current_organization"] and res["current_title"] and res["evidence_url"] and not res["unresolved_reason"]
        else:
            assert not res["current_organization"] and not res["current_title"] and not res["evidence_url"] and res["unresolved_reason"]
    idx=list(csv.DictReader((E/"W3_SEGMENT_INDEX.csv").open("r",encoding="utf-8-sig",newline="")))
    for kind in ("ledger","overlay"):
        entries=sorted((r for r in idx if r["kind"]==kind),key=lambda r:int(r["ordinal"]))
        expected_start=1
        for e in entries:
            start,end,count=map(int,(e["queue_start"],e["queue_end"],e["row_count"]))
            assert start==expected_start,(kind,expected_start,start)
            assert end-start+1==count
            expected_start=end+1
        assert expected_start==4141
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0069"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0069_RESULTS.csv"
        assert int(last["queue_start"])==4081 and int(last["queue_end"])==4140
    print("PASS W3-BATCH-0069 rows=60 confirmed=15 unresolved=45 grades=A48/B12/C0 logical_end=4140")

if __name__=="__main__":
    main()
