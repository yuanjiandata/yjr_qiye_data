#!/usr/bin/env python3
import csv, gzip, hashlib, os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evidence"
RESULTS = E / "W3_BATCH_0077_RESULTS.csv"
RESEARCH = E / "W3_BATCH_0077_RESEARCH.tsv.gz"
INDEX = E / "W3_SEGMENT_INDEX.csv"

EXPECTED_RESULTS_SHA = "e6e68b2da2c767b8e4dbca0386243f677c8845f6f8316f16e00637d348482426"
EXPECTED_RESEARCH_SHA = "d81ae211e955091c4956eef0b40a583eae47463efbb0be22b9df8b6311c3402a"
EXPECTED_MEMBERSHIP_SHA = "86ada49718551b560cbb1385a5cd776db271b894d773bd7e643093e583648f3b"
EXPECTED_SUPPLEMENT_SHA = "136998b03210bd5144be16df3e964c64cae94581170268bc00764a041f596316"

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1<<20), b""):
            h.update(chunk)
    return h.hexdigest()

with open(RESULTS, encoding="utf-8", newline="") as f:
    rows=list(csv.DictReader(f))
assert len(rows)==60
orders=[int(r["queue_order"]) for r in rows]
assert orders==list(range(4561,4621))
assert all(r["province"]=="北京" for r in rows)
assert sum(r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED" for r in rows)==2
assert sum(r["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE" for r in rows)==58
assert sum(r["current_verification_status"]=="NO_CURRENT_ROLE_CONFIRMED" for r in rows)==0
assert all(r["evidence_grade"]=="A" for r in rows)
for r in rows:
    if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED":
        assert r["current_organization"] and r["current_title"] and r["evidence_url"]
        assert not r["unresolved_reason"]
    else:
        assert not r["current_organization"] and not r["current_title"]
        assert r["unresolved_reason"]
assert sha256(RESULTS)==EXPECTED_RESULTS_SHA

with gzip.open(RESEARCH, "rt", encoding="utf-8", newline="") as f:
    rr=list(csv.DictReader(f, delimiter="\t"))
assert len(rr)==60
assert [int(r["queue_order"]) for r in rr]==list(range(4561,4621))
assert all(r["mode"]=="FRESH_PUBLIC_RESEARCH" for r in rr)
assert all(r["source_person_anchor_url"] and r["search_query"] for r in rr)
for r in rr:
    if r["decision"]=="CURRENT_ORG_TITLE_CONFIRMED":
        assert r["current_evidence_url"] and r["identity_bridge_url"]
assert sha256(RESEARCH)==EXPECTED_RESEARCH_SHA

idx=INDEX.read_text(encoding="utf-8")
assert "ledger,50,projects/fc-exec-2515/evidence/W3_BATCH_0077_RESULTS.csv,4561,4620,60,result_segment,ledger,W3-BATCH-0077" in idx
assert "overlay,50,projects/fc-exec-2515/evidence/W3_BATCH_0077_RESULTS.csv,4561,4620,60,result_segment,overlay,W3-BATCH-0077" in idx

membership=os.environ.get("FC2515_MEMBERSHIP_XLSX")
supplement=os.environ.get("FC2515_SUPPLEMENT_XLSX")
if membership:
    assert sha256(membership)==EXPECTED_MEMBERSHIP_SHA
if supplement:
    assert sha256(supplement)==EXPECTED_SUPPLEMENT_SHA

print("W3-BATCH-0077 PASS")
