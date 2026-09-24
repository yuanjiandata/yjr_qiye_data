#!/usr/bin/env python3
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

GATE="W3-BATCH-0074"
START,END=4381,4440
EXPECTED_RESULTS_SHA="73f64e981ccc193aca9bf121b6ff4844590daf50968a4f9f478024c665dac375"
EXPECTED_RESEARCH_SHA="d955d212e19db841307db98758ee1cd57a86ed5e2ded391014bf054dadb90b23"
PRIOR_MAP={4381: 4305, 4382: 4306, 4383: 4307, 4384: 4308, 4385: 4309, 4386: 4310, 4387: 4311, 4388: 4312, 4389: 4313, 4390: 4314, 4391: 4315, 4392: 4316, 4393: 4317, 4394: 4318, 4395: 4319, 4396: 4320, 4397: 4321, 4398: 4322, 4399: 4323, 4400: 4324, 4401: 4325, 4402: 4326, 4403: 4327, 4404: 4328, 4405: 4329, 4406: 4330, 4407: 4331, 4408: 4332, 4409: 4333, 4410: 4334, 4411: 4335, 4412: 4336, 4413: 4337, 4414: 4338, 4415: 4339, 4416: 4340}
SAME_BATCH_MAP={4425: 4424, 4426: 4417, 4427: 4418, 4428: 4419, 4429: 4420, 4430: 4421, 4431: 4422, 4432: 4423}

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
    assert Counter(r["province"] for r in touched)==Counter({"宁夏":36,"新疆":16,"北京":8})
    assert Counter(r["priority"] for r in touched)==Counter({"P1_IDENTITY":52,"P2_ORG_TITLE_LOOKUP":8})

    results=read_csv(ev/"W3_BATCH_0074_RESULTS.csv")
    assert [int(r["queue_order"]) for r in results]==list(range(START,END+1))
    assert len({r["person_id"] for r in results})==60
    for qr,rr in zip(touched,results):
        assert rr["person_id"]==qr["person_id"]
        assert rr["province"]==qr["province"]
        assert rr["excel_row"]==qr["excel_row"]

    status_counts=Counter(r["current_verification_status"] for r in results)
    grade_counts=Counter(r["evidence_grade"] for r in results)
    assert status_counts==Counter({"CURRENT_ORG_TITLE_CONFIRMED":19,"UNRESOLVED_CURRENT_ORG_TITLE":41})
    assert grade_counts==Counter({"A":50,"B":8,"C":2})
    for r in results:
        if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED":
            assert r["current_organization"] and r["current_title"] and r["evidence_url"]
            assert not r["unresolved_reason"]
        else:
            assert not r["current_organization"] and not r["current_title"]
            assert r["unresolved_reason"]

    assert sha256(ev/"W3_BATCH_0074_RESULTS.csv")==EXPECTED_RESULTS_SHA
    assert sha256(ev/"W3_BATCH_0074_RESEARCH.tsv.gz")==EXPECTED_RESEARCH_SHA
    with gzip.open(ev/"W3_BATCH_0074_RESEARCH.tsv.gz","rt",encoding="utf-8-sig",newline="") as f:
        research=list(csv.DictReader(f,delimiter="\t"))
    assert [int(r["queue_order"]) for r in research]==list(range(START,END+1))
    assert Counter(r["mode"] for r in research)==Counter({
        "REUSE_PRIOR_SEALED":36,
        "FRESH_PUBLIC_RESEARCH":15,
        "SOURCE_PLACEHOLDER_REVIEW":1,
        "REUSE_SAME_BATCH_EXACT_GROUP":8,
    })

    prev72={int(r["queue_order"]):r for r in read_csv(ev/"W3_BATCH_0072_RESULTS.csv")}
    prev73={int(r["queue_order"]):r for r in read_csv(ev/"W3_BATCH_0073_RESULTS.csv")}
    for q,sq in PRIOR_MAP.items():
        qr=qmap[q]; sr=qmap[sq]
        assert (qr["province"],qr["name_normalized"],qr["ambiguity_group_id"]) == (sr["province"],sr["name_normalized"],sr["ambiguity_group_id"])
        src=(prev72 if sq<=4320 else prev73)[sq]
        rr=results[q-START]
        assert rr["current_organization"]==src["current_organization"]
        assert rr["current_title"]==src["current_title"]
        assert rr["current_verification_status"]==src["current_verification_status"]
        assert rr["evidence_grade"]==src["evidence_grade"]
        assert rr["evidence_url"]==src["evidence_url"]
        assert rr["unresolved_reason"]==src["unresolved_reason"]

    rmap={int(r["queue_order"]):r for r in results}
    for q,sq in SAME_BATCH_MAP.items():
        qr=qmap[q]; sr=qmap[sq]
        assert (qr["province"],qr["name_normalized"],qr["ambiguity_group_id"]) == (sr["province"],sr["name_normalized"],sr["ambiguity_group_id"])
        for k in ("current_organization","current_title","current_verification_status","evidence_grade","evidence_url","unresolved_reason"):
            assert rmap[q][k]==rmap[sq][k]

    idx=read_csv(ev/"W3_SEGMENT_INDEX.csv")
    new=[r for r in idx if r["ordinal"]=="47"]
    assert len(new)==2 and {r["kind"] for r in new}=={"ledger","overlay"}
    assert all(r["queue_start"]=="4381" and r["queue_end"]=="4440" and r["row_count"]=="60" and r["base_or_parent_gate"]==GATE for r in new)

    status=(root/"STATUS.yaml").read_text(encoding="utf-8")
    current=(root/"CURRENT.yaml").read_text(encoding="utf-8")
    assert "code: W3-BATCH-0074" in status and "code: W3-BATCH-0075" in status
    assert "current_gate: W3-BATCH-0075" in current and "work_cursor: 4440" in current
    assert "P1_IDENTITY:\n      initial: 4331\n      processed: 4331\n      remaining: 0" in current
    assert "unsupported_current_title_claims: 0" in status and "unsupported_current_title_claims: 0" in current
    print("PASS",GATE)

if __name__=="__main__":
    main()
