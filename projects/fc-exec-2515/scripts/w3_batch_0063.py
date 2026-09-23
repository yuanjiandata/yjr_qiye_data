#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0063."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=3721,3780
EXPECTED_RESULTS_SHA256="433cc5e5839596de3dc4920d27163c9ebbd2bcac3141b0b4dc542f7f2b4f0ac9"
EXPECTED_RESEARCH_SHA256="ed1c0b1a6db4976a9e9009cf5149803b14e3fd378dac135b928686cdd5cfd405"
QINGHAI_ANCHOR="https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_qh/202207/t20220719_312776.html"
SOURCE_MAP={
    3723: (3685, 'ANG-1602'),
    3727: (3689, 'ANG-1634'),
    3728: (3669, 'ANG-1633'),
    3729: (3682, 'ANG-1626'),
    3730: (3670, 'ANG-1627'),
    3734: (3677, 'ANG-1591'),
    3740: (3676, 'ANG-1604'),
    3743: (3680, 'ANG-1636'),
    3746: (3690, 'ANG-1635'),
    3747: (3681, 'ANG-1643'),
    3748: (3679, 'ANG-1628'),
    3750: (3691, 'ANG-1585'),
    3751: (3692, 'ANG-1607'),
    3752: (3693, 'ANG-1606'),
    3753: (3694, 'ANG-1640'),
    3754: (3686, 'ANG-1637'),
    3755: (3696, 'ANG-1641'),
    3756: (3668, 'ANG-1638'),
    3757: (3688, 'ANG-1639'),
    3758: (3699, 'ANG-1621'),
    3759: (3700, 'ANG-1619'),
    3760: (3701, 'ANG-1618'),
    3761: (3702, 'ANG-1620'),
    3762: (3703, 'ANG-1622'),
    3763: (3684, 'ANG-1617'),
    3764: (3678, 'ANG-1596'),
    3765: (3706, 'ANG-1623'),
    3766: (3707, 'ANG-1587'),
    3767: (3708, 'ANG-1598'),
    3768: (3709, 'ANG-1586'),
    3769: (3667, 'ANG-1588'),
    3770: (3711, 'ANG-1589'),
    3771: (3712, 'ANG-1616'),
    3772: (3671, 'ANG-1625'),
    3773: (3666, 'ANG-1613'),
    3774: (3715, 'ANG-1608'),
    3775: (3716, 'ANG-1611'),
    3776: (3717, 'ANG-1610'),
    3777: (3718, 'ANG-1612'),
    3778: (3683, 'ANG-1609'),
    3779: (3720, 'ANG-1614')
}
FRESH_ORDERS={3721, 3722, 3724, 3725, 3726, 3731, 3732, 3733, 3735, 3736, 3737, 3738, 3739, 3741, 3742, 3744, 3745, 3749, 3780}
CONFIRMED_ORDERS={3721,3731,3743,3773,3780}

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rb=(E/"W3_BATCH_0063_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0063_RESEARCH.tsv.gz").read_bytes()
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
    assert Counter(r["province"] for r in queue)==Counter({"青海":60})
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":55,"CURRENT_ORG_TITLE_CONFIRMED":5})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":56,"B":4})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":55,"CONFIRMED":5})
    assert Counter(r["mode"] for r in research)==Counter({"FRESH_WEB_RESEARCH":19,"REUSE_SEALED_CONFIRMED":2,"REUSE_SEALED_UNRESOLVED":39})
    for q,r in zip(queue,research):
        qo=int(q["queue_order"])
        assert r["identity_anchor_url"]==QINGHAI_ANCHOR
        if qo in SOURCE_MAP:
            sq,g=SOURCE_MAP[qo]
            assert r["source_gate"]=="W3-BATCH-0062" and int(r["source_queue_order"])==sq
            assert q["ambiguity_group_id"]==r["ambiguity_group_id"]==g
            assert r["mode"] in ("REUSE_SEALED_CONFIRMED","REUSE_SEALED_UNRESOLVED")
        else:
            assert qo in FRESH_ORDERS
            assert r["mode"]=="FRESH_WEB_RESEARCH"
            assert not r["source_gate"] and not r["source_queue_order"]
            assert r["search_query"]
    for r in results:
        assert "NAME_ONLY" not in r["identity_resolution"]
        if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED":
            assert r["current_organization"] and r["current_title"] and r["evidence_url"] and not r["unresolved_reason"]
        else:
            assert not r["current_organization"] and not r["current_title"] and not r["evidence_url"] and r["unresolved_reason"]
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
        assert expected_start==3781
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0063"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0063_RESULTS.csv"
        assert int(last["queue_start"])==3721 and int(last["queue_end"])==3780
    print("PASS W3-BATCH-0063 rows=60 confirmed=5 unresolved=55 grades=A56/B4/C0 logical_end=3780")

if __name__=="__main__":
    main()
