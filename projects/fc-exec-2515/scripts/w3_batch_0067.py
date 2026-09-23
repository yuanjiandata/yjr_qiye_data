#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0067."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=3961,4020
EXPECTED_RESULTS_SHA256="1b82efaeed45b5029ff65b5d054524a02fd7412231ef1006b4c2ab2dcca6ae4f"
EXPECTED_RESEARCH_SHA256="65a43594eed2bff5c413feee6a7ba83e7a96f2e8e4953c8fe4e2a66d5d48d75b"
INNER_MONGOLIA_ANCHOR="https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_nm/202209/t20220919_313060.html"
SOURCE_MAP={
    3961: ('W3-BATCH-0065', 3880, 'ANG-1720'),
    3962: ('W3-BATCH-0065', 3881, 'ANG-1696'),
    3963: ('W3-BATCH-0065', 3882, 'ANG-1690'),
    3964: ('W3-BATCH-0065', 3883, 'ANG-1695'),
    3965: ('W3-BATCH-0065', 3884, 'ANG-1693'),
    3966: ('W3-BATCH-0064', 3817, 'ANG-1689'),
    3967: ('W3-BATCH-0064', 3818, 'ANG-1688'),
    3968: ('W3-BATCH-0065', 3885, 'ANG-1691'),
    3969: ('W3-BATCH-0064', 3819, 'ANG-1694'),
    3970: ('W3-BATCH-0065', 3886, 'ANG-1692'),
    3971: ('W3-BATCH-0065', 3887, 'ANG-1697'),
    3972: ('W3-BATCH-0065', 3888, 'ANG-1698'),
    3973: ('W3-BATCH-0064', 3820, 'ANG-1655'),
    3974: ('W3-BATCH-0065', 3889, 'ANG-1654'),
    3975: ('W3-BATCH-0064', 3821, 'ANG-1656'),
    3976: ('W3-BATCH-0064', 3822, 'ANG-1673'),
    3977: ('W3-BATCH-0065', 3890, 'ANG-1667'),
    3978: ('W3-BATCH-0065', 3891, 'ANG-1668'),
    3979: ('W3-BATCH-0064', 3823, 'ANG-1684'),
    3980: ('W3-BATCH-0065', 3892, 'ANG-1680'),
    3981: ('W3-BATCH-0064', 3824, 'ANG-1678'),
    3982: ('W3-BATCH-0065', 3893, 'ANG-1675'),
    3983: ('W3-BATCH-0065', 3894, 'ANG-1682'),
    3984: ('W3-BATCH-0065', 3895, 'ANG-1676'),
    3985: ('W3-BATCH-0064', 3825, 'ANG-1679'),
    3986: ('W3-BATCH-0065', 3896, 'ANG-1677'),
    3987: ('W3-BATCH-0065', 3897, 'ANG-1683'),
    3988: ('W3-BATCH-0065', 3898, 'ANG-1674'),
    3989: ('W3-BATCH-0065', 3899, 'ANG-1681'),
    3990: ('W3-BATCH-0065', 3900, 'ANG-1734'),
    3991: ('W3-BATCH-0066', 3901, 'ANG-1700'),
    3992: ('W3-BATCH-0064', 3826, 'ANG-1699'),
    3993: ('W3-BATCH-0066', 3902, 'ANG-1661'),
    3994: ('W3-BATCH-0064', 3827, 'ANG-1657'),
    3995: ('W3-BATCH-0064', 3812, 'ANG-1669'),
    3996: ('W3-BATCH-0066', 3903, 'ANG-1727'),
    3997: ('W3-BATCH-0066', 3904, 'ANG-1726'),
    3998: ('W3-BATCH-0066', 3905, 'ANG-1721'),
    3999: ('W3-BATCH-0066', 3906, 'ANG-1719'),
    4000: ('W3-BATCH-0066', 3907, 'ANG-1685'),
    4001: ('W3-BATCH-0066', 3908, 'ANG-1658'),
    4002: ('W3-BATCH-0066', 3909, 'ANG-1659'),
    4003: ('W3-BATCH-0066', 3910, 'ANG-1660'),
    4004: ('W3-BATCH-0066', 3911, 'ANG-1729'),
    4005: ('W3-BATCH-0066', 3912, 'ANG-1703'),
    4006: ('W3-BATCH-0064', 3828, 'ANG-1648'),
    4007: ('W3-BATCH-0066', 3913, 'ANG-1728'),
    4008: ('W3-BATCH-0066', 3914, 'ANG-1663'),
    4009: ('W3-BATCH-0066', 3915, 'ANG-1716'),
    4010: ('W3-BATCH-0066', 3916, 'ANG-1718'),
    4011: ('W3-BATCH-0066', 3917, 'ANG-1743'),
    4012: ('W3-BATCH-0066', 3918, 'ANG-1730'),
    4013: ('W3-BATCH-0064', 3829, 'ANG-1731'),
    4014: ('W3-BATCH-0064', 3830, 'ANG-1732'),
    4015: ('W3-BATCH-0064', 3831, 'ANG-1733'),
    4016: ('W3-BATCH-0066', 3919, 'ANG-1735'),
    4017: ('W3-BATCH-0066', 3920, 'ANG-1745'),
    4018: ('W3-BATCH-0066', 3921, 'ANG-1722'),
    4019: ('W3-BATCH-0066', 3922, 'ANG-1686'),
    4020: ('W3-BATCH-0066', 3923, 'ANG-1671')
}
CONFIRMED_ORDERS={3969, 3972, 3973, 3975, 3976, 3978, 3979, 4011, 3981, 4015, 3992, 3962, 3966}
OUTCOME_FIELDS=("current_organization","current_title","current_verification_status","evidence_grade","evidence_url","unresolved_reason")

def load_results(gate):
    p=E/(gate.replace("-","_")+"_RESULTS.csv")
    with p.open("r",encoding="utf-8-sig",newline="") as f:
        return {int(r["queue_order"]):r for r in csv.DictReader(f)}

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        all_queue=list(csv.DictReader(f))
    queue=all_queue[START-1:END]
    rb=(E/"W3_BATCH_0067_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0067_RESEARCH.tsv.gz").read_bytes()
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
    assert Counter(r["province"] for r in queue)==Counter({"内蒙古":60})
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":47,"CURRENT_ORG_TITLE_CONFIRMED":13})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":50,"B":8,"C":2})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":47,"CONFIRMED":13})
    assert Counter(r["mode"] for r in research)==Counter({"REUSE_SEALED_UNRESOLVED":47,"REUSE_SEALED_CONFIRMED":13})
    source_cache={}
    for q,res,rr in zip(queue,results,research):
        qo=int(q["queue_order"])
        sg,sq,g=SOURCE_MAP[qo]
        assert rr["identity_anchor_url"]==INNER_MONGOLIA_ANCHOR
        assert rr["source_gate"]==sg and int(rr["source_queue_order"])==sq
        assert rr["ambiguity_group_id"]==q["ambiguity_group_id"]==g
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
        confirmed=res["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED"
        assert rr["decision"]==("CONFIRMED" if confirmed else "UNRESOLVED")
        assert rr["mode"]==("REUSE_SEALED_CONFIRMED" if confirmed else "REUSE_SEALED_UNRESOLVED")
        expected_prefix="REUSED_SEALED_EVIDENCE_C:" if confirmed else "REUSED_SEALED_EVIDENCE_U:"
        assert res["identity_resolution"].startswith(expected_prefix)
        assert f":{sq}:{g}" in res["identity_resolution"]
        assert "NAME_ONLY" not in res["identity_resolution"]
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
        assert expected_start==4021
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0067"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0067_RESULTS.csv"
        assert int(last["queue_start"])==3961 and int(last["queue_end"])==4020
    print("PASS W3-BATCH-0067 rows=60 confirmed=13 unresolved=47 grades=A50/B8/C2 logical_end=4020")

if __name__=="__main__":
    main()
