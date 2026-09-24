#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0070."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=4141,4200
EXPECTED_RESULTS_SHA256="52183f2f954bb4d2ecbdf2bc704baef195246a34dec3bfb74143133b505e119f"
EXPECTED_RESEARCH_SHA256="24f7415fe2863360cb649b351ce8e68999b629945b49578c3087f127dfbf10cc"
GUANGXI_ANCHOR="https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_gx/202309/t20230914_316460.html"
SOURCE_MAP={4155: ('0068', 4058), 4158: ('0068', 4043), 4161: ('0068', 4041), 4162: ('0068', 4044), 4163: ('0068', 4045), 4164: ('0068', 4059), 4165: ('0069', 4095), 4166: ('0068', 4038), 4167: ('0068', 4040), 4168: ('0069', 4107), 4169: ('0069', 4109), 4170: ('0069', 4094), 4171: ('0068', 4046), 4172: ('0069', 4083), 4175: ('0068', 4076), 4176: ('0068', 4060), 4177: ('0068', 4079), 4179: ('0068', 4047), 4181: ('0069', 4102), 4182: ('0068', 4061), 4183: ('0069', 4110), 4184: ('0069', 4084), 4185: ('0068', 4074), 4186: ('0069', 4111), 4187: ('0069', 4096), 4189: ('0069', 4086), 4190: ('0068', 4062), 4191: ('0068', 4078), 4192: ('0068', 4048), 4193: ('0068', 4049), 4194: ('0068', 4049), 4195: ('0068', 4050), 4196: ('0068', 4051), 4197: ('0069', 4099), 4198: ('0069', 4089), 4199: ('0068', 4063)}
WITHIN_MAP={4156: 4145, 4157: 4141, 4159: 4146, 4160: 4147, 4173: 4149, 4174: 4148, 4178: 4150, 4180: 4142, 4188: 4143, 4200: 4151}
FRESH_ORDERS=set(range(4141,4155))
FRESH_EXPECTED={4143: ('广西兆和种业有限公司', '总经理', 'B', 'https://nxy.gxu.edu.cn/info/1077/5791.htm'), 4146: ('广西巴马丽琅饮料有限公司', '董事长', 'B', 'https://me.gxu.edu.cn/info/1051/5136.htm'), 4147: ('广西浙江商会', '会长', 'B', 'https://finance.sina.com.cn/wm/2026-05-23/doc-inhywcxs5487324.shtml'), 4149: ('广西金福农业有限公司', '总裁', 'B', 'https://www.rmzxw.com.cn/c/2026-02-26/3873912.shtml'), 4150: ('迈越科技股份有限公司', '董事长', 'B', 'https://www.gxjtc.edu.cn/info/1050/11179.htm'), 4151: ('广西广东商会', '会长', 'A', 'https://stgsl.shantou.gov.cn/stgsl/hyhwxx/202602/29f94aac464b45eb92773b89cf2b646a.shtml')}
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
    rb=(E/"W3_BATCH_0070_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0070_RESEARCH.tsv.gz").read_bytes()
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
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":40,"CURRENT_ORG_TITLE_CONFIRMED":20})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":43,"B":17})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":40,"CONFIRMED":20})
    assert Counter(r["mode"] for r in research)==Counter({"FRESH_WEB_RESEARCH":14,"REUSE_SEALED_UNRESOLVED":28,"REUSE_SEALED_CONFIRMED":8,"REUSE_CURRENT_BATCH_CONFIRMED":6,"REUSE_CURRENT_BATCH_UNRESOLVED":4})
    prior_cache={}
    result_map={int(r["queue_order"]):r for r in results}
    for q,res,rr in zip(queue,results,research):
        qo=int(q["queue_order"])
        assert rr["identity_anchor_url"]==GUANGXI_ANCHOR
        assert "NAME_ONLY" not in res["identity_resolution"]
        if qo in SOURCE_MAP:
            gate_short,sq=SOURCE_MAP[qo]
            gate="W3-BATCH-"+gate_short
            assert rr["source_gate"]==gate and int(rr["source_queue_order"])==sq
            assert not rr["search_query"]
            source_q=all_queue[sq-1]
            assert source_q["province"]==q["province"]
            assert source_q["name_normalized"]==q["name_normalized"]
            assert source_q["ambiguity_group_id"]==q["ambiguity_group_id"]
            src=prior_cache.setdefault(gate,load_results(gate))
            for field in OUTCOME_FIELDS:
                assert res[field]==src[sq][field],(qo,field,res[field],src[sq][field])
        elif qo in WITHIN_MAP:
            sq=WITHIN_MAP[qo]
            assert rr["source_gate"]=="W3-BATCH-0070" and int(rr["source_queue_order"])==sq
            assert not rr["search_query"]
            source_q=all_queue[sq-1]
            assert source_q["province"]==q["province"]
            assert source_q["name_normalized"]==q["name_normalized"]
            assert source_q["ambiguity_group_id"]==q["ambiguity_group_id"]
            for field in OUTCOME_FIELDS:
                assert res[field]==result_map[sq][field],(qo,field,res[field],result_map[sq][field])
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
        assert expected_start==4201
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0070"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0070_RESULTS.csv"
        assert int(last["queue_start"])==4141 and int(last["queue_end"])==4200
    print("PASS W3-BATCH-0070 rows=60 confirmed=20 unresolved=40 grades=A43/B17/C0 logical_end=4200")

if __name__=="__main__":
    main()
