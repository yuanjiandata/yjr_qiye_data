#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0061."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=3601,3660
EXPECTED_RESULTS_SHA256="7b206adabe20b3ecdfcc4df2689de27f36eb6f409435be4b05b5d2570001d0ba"
EXPECTED_RESEARCH_SHA256="7c9dc187fd3cb15a5b3e3203f043287d2132def9cf3099624399f39d010f167e"
IDENTITY_ANCHOR="https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_gs/202207/t20220719_312778.html"
SOURCE_MAP={3601: ('W3-BATCH-0059', 3457, 'ANG-1541'), 3602: ('W3-BATCH-0059', 3513, 'ANG-1512'), 3603: ('W3-BATCH-0059', 3514, 'ANG-1515'), 3604: ('W3-BATCH-0059', 3515, 'ANG-1514'), 3605: ('W3-BATCH-0059', 3516, 'ANG-1571'), 3606: ('W3-BATCH-0058', 3461, 'ANG-1570'), 3607: ('W3-BATCH-0059', 3517, 'ANG-1503'), 3608: ('W3-BATCH-0058', 3453, 'ANG-1505'), 3609: ('W3-BATCH-0059', 3518, 'ANG-1504'), 3610: ('W3-BATCH-0059', 3519, 'ANG-1528'), 3611: ('W3-BATCH-0059', 3520, 'ANG-1564'), 3612: ('W3-BATCH-0059', 3521, 'ANG-1565'), 3613: ('W3-BATCH-0059', 3522, 'ANG-1496'), 3614: ('W3-BATCH-0059', 3523, 'ANG-1497'), 3615: ('W3-BATCH-0058', 3450, 'ANG-1507'), 3616: ('W3-BATCH-0059', 3524, 'ANG-1492'), 3617: ('W3-BATCH-0059', 3525, 'ANG-1527'), 3618: ('W3-BATCH-0058', 3441, 'ANG-1569'), 3619: ('W3-BATCH-0059', 3526, 'ANG-1506'), 3620: ('W3-BATCH-0059', 3527, 'ANG-1583'), 3622: ('W3-BATCH-0059', 3528, 'ANG-1529'), 3623: ('W3-BATCH-0059', 3529, 'ANG-1542'), 3624: ('W3-BATCH-0059', 3530, 'ANG-1577'), 3625: ('W3-BATCH-0059', 3531, 'ANG-1576'), 3626: ('W3-BATCH-0058', 3459, 'ANG-1579'), 3627: ('W3-BATCH-0059', 3532, 'ANG-1578'), 3628: ('W3-BATCH-0058', 3449, 'ANG-1582'), 3629: ('W3-BATCH-0059', 3533, 'ANG-1559'), 3630: ('W3-BATCH-0059', 3534, 'ANG-1572'), 3631: ('W3-BATCH-0059', 3535, 'ANG-1560'), 3632: ('W3-BATCH-0058', 3441, 'ANG-1569'), 3633: ('W3-BATCH-0058', 3444, 'ANG-1532'), 3635: ('W3-BATCH-0058', 3445, 'ANG-1543'), 3636: ('W3-BATCH-0058', 3446, 'ANG-1523'), 3637: ('W3-BATCH-0058', 3462, 'ANG-1510'), 3638: ('W3-BATCH-0058', 3447, 'ANG-1513'), 3639: ('W3-BATCH-0058', 3448, 'ANG-1498'), 3640: ('W3-BATCH-0058', 3449, 'ANG-1582'), 3641: ('W3-BATCH-0058', 3450, 'ANG-1507'), 3642: ('W3-BATCH-0058', 3451, 'ANG-1495'), 3643: ('W3-BATCH-0058', 3452, 'ANG-1536'), 3644: ('W3-BATCH-0058', 3453, 'ANG-1505'), 3645: ('W3-BATCH-0058', 3454, 'ANG-1581'), 3646: ('W3-BATCH-0058', 3455, 'ANG-1535'), 3647: ('W3-BATCH-0058', 3456, 'ANG-1547'), 3648: ('W3-BATCH-0059', 3457, 'ANG-1541'), 3649: ('W3-BATCH-0058', 3458, 'ANG-1555'), 3650: ('W3-BATCH-0058', 3459, 'ANG-1579'), 3651: ('W3-BATCH-0058', 3460, 'ANG-1550'), 3652: ('W3-BATCH-0058', 3461, 'ANG-1570'), 3653: ('W3-BATCH-0059', 3519, 'ANG-1528'), 3654: ('W3-BATCH-0059', 3506, 'ANG-1518'), 3655: ('W3-BATCH-0059', 3483, 'ANG-1508'), 3656: ('W3-BATCH-0058', 3470, 'ANG-1554'), 3657: ('W3-BATCH-0059', 3515, 'ANG-1514'), 3658: ('W3-BATCH-0059', 3507, 'ANG-1521'), 3659: ('W3-BATCH-0059', 3517, 'ANG-1503'), 3660: ('W3-BATCH-0059', 3522, 'ANG-1496')}
FRESH_ORDERS={3621,3634}
CONFIRMED_ORDERS={3604, 3606, 3608, 3618, 3620, 3626, 3632, 3633, 3635, 3637, 3638, 3643, 3644, 3645, 3646, 3650, 3651, 3652, 3657, 3658}

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rb=(E/"W3_BATCH_0061_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0061_RESEARCH.tsv.gz").read_bytes()
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
    assert Counter(r["province"] for r in queue)==Counter({"甘肃":60})
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":40,"CURRENT_ORG_TITLE_CONFIRMED":20})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":46,"B":14})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":40,"CONFIRMED":20})
    assert Counter(r["mode"] for r in research)==Counter({"REUSE_SEALED_UNRESOLVED":38,"REUSE_SEALED_CONFIRMED":20,"FRESH_WEB_RESEARCH":2})
    for q,r in zip(queue,research):
        qo=int(q["queue_order"])
        assert r["identity_anchor_url"]==IDENTITY_ANCHOR
        if qo in FRESH_ORDERS:
            assert r["mode"]=="FRESH_WEB_RESEARCH"
            assert not r["source_gate"] and not r["source_queue_order"]
            assert r["ambiguity_group_id"]=="ANG-1516"
            assert r["decision"]=="UNRESOLVED"
        else:
            sg,sq,g=SOURCE_MAP[qo]
            assert r["source_gate"]==sg and int(r["source_queue_order"])==sq
            assert r["ambiguity_group_id"]==g
            assert q["ambiguity_group_id"]==g
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
        assert expected_start==3661
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0061"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0061_RESULTS.csv"
        assert int(last["queue_start"])==3601 and int(last["queue_end"])==3660
    print("PASS W3-BATCH-0061 rows=60 confirmed=20 unresolved=40 grades=A46/B14/C0 logical_end=3660")

if __name__=="__main__":
    main()
