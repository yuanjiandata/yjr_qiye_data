#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0064."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=3781,3840
EXPECTED_RESULTS_SHA256="59a1bfddb19e338d9be198d6865d257e542e868cad93e19b0c08e0aff149e079"
EXPECTED_RESEARCH_SHA256="31e254cfd8a140fbe0cab8739394dc22b7e6a7a475027dffb8b9c236072cdbe0"
QINGHAI_ANCHOR="https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_qh/202207/t20220719_312776.html"
INNER_MONGOLIA_ANCHOR="https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_nm/202209/t20220919_313060.html"
SOURCE_MAP={3781: (3722, 'ANG-1603'), 3782: (3723, 'ANG-1602'), 3783: (3724, 'ANG-1599'), 3784: (3725, 'ANG-1600'), 3785: (3726, 'ANG-1601'), 3786: (3727, 'ANG-1634'), 3787: (3728, 'ANG-1633'), 3788: (3729, 'ANG-1626'), 3789: (3730, 'ANG-1627'), 3790: (3731, 'ANG-1631'), 3791: (3732, 'ANG-1593'), 3792: (3733, 'ANG-1590'), 3793: (3734, 'ANG-1591'), 3794: (3735, 'ANG-1592'), 3795: (3736, 'ANG-1630'), 3796: (3737, 'ANG-1632'), 3797: (3738, 'ANG-1615'), 3798: (3739, 'ANG-1629'), 3799: (3740, 'ANG-1604'), 3800: (3741, 'ANG-1594'), 3801: (3742, 'ANG-1597'), 3802: (3743, 'ANG-1636'), 3803: (3744, 'ANG-1624'), 3804: (3745, 'ANG-1642'), 3805: (3746, 'ANG-1635'), 3806: (3747, 'ANG-1643'), 3807: (3748, 'ANG-1628'), 3808: (3749, 'ANG-1605')}
FRESH_ORDERS=set(range(3809,3841))
CONFIRMED_ORDERS={3790, 3802, 3809, 3810, 3811, 3813, 3815, 3816, 3817, 3819, 3820, 3821, 3822, 3823, 3824, 3826, 3831, 3832, 3833, 3834}

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rb=(E/"W3_BATCH_0064_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0064_RESEARCH.tsv.gz").read_bytes()
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
    assert Counter(r["province"] for r in queue)==Counter({"青海":28,"内蒙古":32})
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":40,"CURRENT_ORG_TITLE_CONFIRMED":20})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":46,"B":12,"C":2})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":40,"CONFIRMED":20})
    assert Counter(r["mode"] for r in research)==Counter({"FRESH_WEB_RESEARCH":32,"REUSE_SEALED_CONFIRMED":2,"REUSE_SEALED_UNRESOLVED":26})
    for q,r in zip(queue,research):
        qo=int(q["queue_order"])
        if qo in SOURCE_MAP:
            sq,g=SOURCE_MAP[qo]
            assert r["identity_anchor_url"]==QINGHAI_ANCHOR
            assert r["source_gate"]=="W3-BATCH-0063" and int(r["source_queue_order"])==sq
            assert q["ambiguity_group_id"]==r["ambiguity_group_id"]==g
            assert r["mode"] in ("REUSE_SEALED_CONFIRMED","REUSE_SEALED_UNRESOLVED")
            assert not r["search_query"]
        else:
            assert qo in FRESH_ORDERS
            assert r["identity_anchor_url"]==INNER_MONGOLIA_ANCHOR
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
        assert expected_start==3841
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0064"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0064_RESULTS.csv"
        assert int(last["queue_start"])==3781 and int(last["queue_end"])==3840
    print("PASS W3-BATCH-0064 rows=60 confirmed=20 unresolved=40 grades=A46/B12/C2 logical_end=3840")

if __name__=="__main__":
    main()
