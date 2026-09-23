#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0060."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=3541,3600
EXPECTED_RESULTS_SHA256="22375b0b3dfe7b8b1fc1252cb8877906040401b46fbf226ed13ca7c4ee774852"
EXPECTED_RESEARCH_SHA256="746c810dce09bbc1407f345a8a1f9a6e52e4cbf4e7993794003f1c4e74ab3ee1"
IDENTITY_ANCHOR="https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_gs/202207/t20220719_312778.html"
SOURCE_MAP={"3541": 3467, "3542": 3456, "3543": 3468, "3544": 3469, "3545": 3470, "3546": 3471, "3547": 3460, "3548": 3472, "3549": 3473, "3550": 3445, "3551": 3447, "3552": 3474, "3553": 3448, "3554": 3458, "3555": 3475, "3556": 3443, "3557": 3476, "3558": 3477, "3559": 3444, "3560": 3478, "3561": 3479, "3562": 3451, "3563": 3480, "3564": 3481, "3565": 3482, "3566": 3483, "3567": 3484, "3568": 3485, "3569": 3486, "3570": 3487, "3571": 3488, "3572": 3452, "3573": 3489, "3574": 3455, "3575": 3490, "3576": 3491, "3577": 3492, "3578": 3493, "3579": 3494, "3580": 3495, "3581": 3496, "3582": 3497, "3583": 3498, "3584": 3499, "3585": 3500, "3586": 3501, "3587": 3502, "3588": 3462, "3589": 3446, "3590": 3503, "3591": 3504, "3592": 3505, "3593": 3506, "3594": 3507, "3595": 3508, "3596": 3509, "3597": 3510, "3598": 3442, "3599": 3511, "3600": 3512}
CONFIRMED_SOURCE_ORDERS={3444,3445,3447,3452,3455,3460,3462,3485,3490,3507}

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rb=(E/"W3_BATCH_0060_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0060_RESEARCH.tsv.gz").read_bytes()
    assert hashlib.sha256(rb).hexdigest()==EXPECTED_RESULTS_SHA256
    assert hashlib.sha256(qb).hexdigest()==EXPECTED_RESEARCH_SHA256
    results=list(csv.DictReader(rb.decode("utf-8-sig").splitlines()))
    research=list(csv.DictReader(gzip.decompress(qb).decode("utf-8-sig").splitlines(),delimiter="\t"))
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
    assert Counter(r["province"] for r in queue)==Counter({"甘肃":60})
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":50,"CURRENT_ORG_TITLE_CONFIRMED":10})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":53,"B":7})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":50,"CONFIRMED":10})
    assert Counter(r["mode"] for r in research)==Counter({"REUSE_SEALED_UNRESOLVED":50,"REUSE_SEALED_CONFIRMED":10})
    assert Counter(r["source_gate"] for r in research)==Counter({"W3-BATCH-0058":28,"W3-BATCH-0059":32})
    for q,r in zip(queue,research):
        qo=int(q["queue_order"]); src=int(r["source_queue_order"])
        assert int(SOURCE_MAP[str(qo)] if str(qo) in SOURCE_MAP else SOURCE_MAP[qo])==src
        assert q["ambiguity_group_id"]==r["ambiguity_group_id"]
        assert q["province"]=="甘肃"
        assert q["name_normalized"]==r["name_normalized"]
        assert r["identity_anchor_url"]==IDENTITY_ANCHOR
        assert r["source_gate"]==("W3-BATCH-0058" if src<=3480 else "W3-BATCH-0059")
    for r in results:
        assert "NAME_ONLY" not in r["identity_resolution"]
        assert r["identity_resolution"].startswith("REUSED_SEALED_EVIDENCE_")
        if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED":
            assert r["current_organization"] and r["current_title"] and r["evidence_url"] and not r["unresolved_reason"]
        else:
            assert not r["current_organization"] and not r["current_title"] and not r["evidence_url"] and r["unresolved_reason"]
    assert {int(r["source_queue_order"]) for r in research if r["decision"]=="CONFIRMED"}==CONFIRMED_SOURCE_ORDERS
    idx=list(csv.DictReader((E/"W3_SEGMENT_INDEX.csv").open("r",encoding="utf-8-sig",newline="")))
    for kind in ("ledger","overlay"):
        entries=sorted((r for r in idx if r["kind"]==kind),key=lambda r:int(r["ordinal"]))
        expected_start=1
        for e in entries:
            start,end,count=map(int,(e["queue_start"],e["queue_end"],e["row_count"]))
            assert start==expected_start,(kind,expected_start,start)
            assert end-start+1==count
            expected_start=end+1
        assert expected_start==3601
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0060"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0060_RESULTS.csv"
        assert int(last["queue_start"])==3541 and int(last["queue_end"])==3600
    print("PASS W3-BATCH-0060 rows=60 confirmed=10 unresolved=50 grades=A53/B7/C0 logical_end=3600")

if __name__=="__main__":
    main()
