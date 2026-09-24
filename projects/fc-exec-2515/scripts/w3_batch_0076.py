#!/usr/bin/env python3
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

GATE="W3-BATCH-0076"
START,END=4501,4560
EXPECTED_RESULTS_SHA="22f3213ca47d6f0a37357d6cd754721298e62009bd497a7dd20ac306c1f2d64b"
EXPECTED_RESEARCH_SHA="effec1ce5696869ce99498716677cdcaaaf2b4006069155ffe90467faeb0321e"

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def read_csv(path):
    with open(path,"r",encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def main():
    root=Path(__file__).resolve().parents[1]
    ev=root/"evidence"
    with gzip.open(ev/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))
    qmap={int(r["queue_order"]):r for r in queue}
    touched=[qmap[q] for q in range(START,END+1)]
    assert len(touched)==60
    assert Counter(r["province"] for r in touched)==Counter({"北京":60})
    assert Counter(r["priority"] for r in touched)==Counter({"P2_ORG_TITLE_LOOKUP":60})

    results=read_csv(ev/"W3_BATCH_0076_RESULTS.csv")
    assert [int(r["queue_order"]) for r in results]==list(range(START,END+1))
    assert len({r["person_id"] for r in results})==60
    for qr,rr in zip(touched,results):
        assert rr["person_id"]==qr["person_id"]
        assert rr["province"]==qr["province"]
        assert rr["excel_row"]==qr["excel_row"]

    status_counts=Counter(r["current_verification_status"] for r in results)
    grade_counts=Counter(r["evidence_grade"] for r in results)
    assert status_counts==Counter({"CURRENT_ORG_TITLE_CONFIRMED":9,"UNRESOLVED_CURRENT_ORG_TITLE":51})
    assert grade_counts==Counter({"A":57,"B":3})
    for r in results:
        status=r["current_verification_status"]
        if status=="CURRENT_ORG_TITLE_CONFIRMED":
            assert r["current_organization"] and r["current_title"] and r["evidence_url"]
            assert not r["unresolved_reason"]
        else:
            assert not r["current_organization"] and not r["current_title"]
            assert r["unresolved_reason"]

    assert sha256(ev/"W3_BATCH_0076_RESULTS.csv")==EXPECTED_RESULTS_SHA
    assert sha256(ev/"W3_BATCH_0076_RESEARCH.tsv.gz")==EXPECTED_RESEARCH_SHA
    with gzip.open(ev/"W3_BATCH_0076_RESEARCH.tsv.gz","rt",encoding="utf-8-sig",newline="") as f:
        research=list(csv.DictReader(f,delimiter="\t"))
    assert [int(r["queue_order"]) for r in research]==list(range(START,END+1))
    assert Counter(r["mode"] for r in research)==Counter({"FRESH_PUBLIC_RESEARCH":60})
    rmap={int(r["queue_order"]):r for r in research}
    for q in range(START,END+1):
        assert rmap[q]["source_person_anchor_url"]
        assert rmap[q]["search_query"]
    for q in [4508, 4509, 4511, 4518, 4523, 4526, 4546, 4549, 4556]:
        assert rmap[q]["current_evidence_url"] and rmap[q]["identity_bridge_url"]

    idx=read_csv(ev/"W3_SEGMENT_INDEX.csv")
    new=[r for r in idx if r["ordinal"]=="49"]
    assert len(new)==2 and {r["kind"] for r in new}=={"ledger","overlay"}
    assert all(r["queue_start"]=="4501" and r["queue_end"]=="4560" and r["row_count"]=="60" and r["base_or_parent_gate"]==GATE for r in new)

    status=(root/"STATUS.yaml").read_text(encoding="utf-8")
    current=(root/"CURRENT.yaml").read_text(encoding="utf-8")
    assert "code: W3-BATCH-0076" in status and "code: W3-BATCH-0077" in status
    assert "current_gate: W3-BATCH-0077" in current and "work_cursor: 4560" in current
    assert "P2_ORG_TITLE_LOOKUP:\n      initial: 6045\n      processed: 128\n      remaining: 5917" in current
    assert "unsupported_current_title_claims: 0" in status and "unsupported_current_title_claims: 0" in current
    print("PASS",GATE)

if __name__=="__main__":
    main()
