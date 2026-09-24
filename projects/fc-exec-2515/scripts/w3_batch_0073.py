#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0073."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=4321,4380
EXPECTED_RESULTS_SHA256="4a9327918c218729239a05590238bdc0cc0f746d18b9a3d6bca00fce573075ed"
EXPECTED_RESEARCH_SHA256="0f545e6e034d2da01f5963bfced8ac806b5d77684cb264d850c60ae355aca3d1"
NX_ANCHOR="https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_nx/202207/t20220719_102110.html"
SOURCE_MAP={4325: 4251, 4326: 4264, 4327: 4262, 4328: 4245, 4332: 4261, 4334: 4260, 4335: 4252, 4336: 4244, 4337: 4257, 4341: 4265, 4342: 4266, 4343: 4267, 4344: 4268, 4345: 4269, 4346: 4270, 4347: 4271, 4348: 4272, 4349: 4273, 4350: 4274, 4351: 4275, 4352: 4276, 4353: 4277, 4354: 4278, 4355: 4279, 4356: 4280, 4357: 4281, 4358: 4282, 4359: 4283, 4360: 4284, 4361: 4285, 4362: 4286, 4363: 4287, 4364: 4288, 4365: 4289, 4366: 4290, 4367: 4291, 4368: 4292, 4369: 4293, 4370: 4294, 4371: 4295, 4372: 4296, 4373: 4297, 4374: 4298, 4375: 4299, 4376: 4300, 4377: 4301, 4378: 4302, 4379: 4303, 4380: 4304}
FRESH={4321, 4322, 4323, 4324, 4329, 4330, 4331, 4333, 4338, 4339, 4340}

def read_results(path):
    with path.open("r",encoding="utf-8-sig",newline="") as f:
        return {int(r["queue_order"]):r for r in csv.DictReader(f)}

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        all_queue=list(csv.DictReader(f))
    queue=all_queue[START-1:END]
    rb=(E/"W3_BATCH_0073_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0073_RESEARCH.tsv.gz").read_bytes()
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
    assert Counter(r["province"] for r in queue)==Counter({"宁夏":60})
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":50,"CURRENT_ORG_TITLE_CONFIRMED":9,"NO_CURRENT_ROLE_CONFIRMED":1})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":56,"B":4})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":50,"CONFIRMED":9,"NO_CURRENT_ROLE_CONFIRMED":1})
    assert Counter(r["mode"] for r in research)==Counter({"REUSE_SEALED_UNRESOLVED":39,"FRESH_WEB_RESEARCH":11,"REUSE_SEALED_CONFIRMED":9,"REUSE_SEALED_NO_CURRENT_ROLE":1})
    assert set(SOURCE_MAP)==set(expected)-FRESH
    prior={}
    for gate in ("0071","0072"):
        prior.update(read_results(E/f"W3_BATCH_{gate}_RESULTS.csv"))
    for q,res,rr in zip(queue,results,research):
        qo=int(q["queue_order"])
        assert "NAME_ONLY" not in res["identity_resolution"]
        assert rr["identity_anchor_url"]==NX_ANCHOR
        if qo in SOURCE_MAP:
            sq=SOURCE_MAP[qo]
            source_q=all_queue[sq-1]
            assert source_q["province"]==q["province"]=="宁夏"
            assert source_q["name_normalized"]==q["name_normalized"]
            assert source_q["ambiguity_group_id"]==q["ambiguity_group_id"]
            assert int(rr["source_queue_order"])==sq
            expected_gate="W3-BATCH-0071" if sq<=4260 else "W3-BATCH-0072"
            assert rr["source_gate"]==expected_gate
            assert rr["mode"].startswith("REUSE_SEALED_")
            assert not rr["search_query"]
            src=prior[sq]
            for field in ("current_organization","current_title","current_verification_status","evidence_grade","evidence_url","unresolved_reason"):
                assert res[field]==src[field], (qo,sq,field,res[field],src[field])
        else:
            assert qo in FRESH
            assert rr["mode"]=="FRESH_WEB_RESEARCH"
            assert not rr["source_gate"] and not rr["source_queue_order"]
            assert rr["search_query"]
            assert res["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE"
            assert res["evidence_grade"]=="A"
            assert not res["current_organization"] and not res["current_title"] and not res["evidence_url"]
            assert res["unresolved_reason"]
        status=res["current_verification_status"]
        if status=="CURRENT_ORG_TITLE_CONFIRMED":
            assert res["current_organization"] and res["current_title"] and res["evidence_url"] and not res["unresolved_reason"]
            assert rr["decision"]=="CONFIRMED"
        elif status=="NO_CURRENT_ROLE_CONFIRMED":
            assert not res["current_organization"] and not res["current_title"] and res["evidence_url"] and not res["unresolved_reason"]
            assert rr["decision"]=="NO_CURRENT_ROLE_CONFIRMED"
        else:
            assert not res["current_organization"] and not res["current_title"] and not res["evidence_url"] and res["unresolved_reason"]
            assert rr["decision"]=="UNRESOLVED"
    idx=list(csv.DictReader((E/"W3_SEGMENT_INDEX.csv").open("r",encoding="utf-8-sig",newline="")))
    for kind in ("ledger","overlay"):
        entries=sorted((r for r in idx if r["kind"]==kind),key=lambda r:int(r["ordinal"]))
        expected_start=1
        for e in entries:
            start,end,count=map(int,(e["queue_start"],e["queue_end"],e["row_count"]))
            assert start==expected_start,(kind,expected_start,start)
            assert end-start+1==count
            expected_start=end+1
        assert expected_start==4381
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0073"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0073_RESULTS.csv"
        assert int(last["queue_start"])==4321 and int(last["queue_end"])==4380
    print("PASS W3-BATCH-0073 rows=60 current=9 no_current=1 unresolved=50 grades=A56/B4/C0 logical_end=4380")

if __name__=="__main__":
    main()
