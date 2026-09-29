#!/usr/bin/env python3
import csv, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
W=ROOT/"work"; E=ROOT/"evidence"
inp=W/"W3_BATCH_0083_INPUT.csv"; res=E/"W3_BATCH_0083_RESULTS.csv"; research=E/"W3_BATCH_0083_RESEARCH_RECOVERY.tsv"
with inp.open(encoding="utf-8",newline="") as f: ir=list(csv.DictReader(f))
with res.open(encoding="utf-8",newline="") as f: rr=list(csv.DictReader(f))
with research.open(encoding="utf-8",newline="") as f: tr=list(csv.DictReader(f,delimiter="\t"))
assert len(ir)==len(rr)==len(tr)==60
assert [int(x["queue_order"]) for x in ir]==list(range(4921,4981))
assert [int(x["queue_order"]) for x in rr]==list(range(4921,4981))
assert [int(x["queue_order"]) for x in tr]==list(range(4921,4981))
assert hashlib.sha256(inp.read_bytes()).hexdigest()=="ea7029eb6d6b07cbd05034a0e73f688bcdd95c0ea27614d663829922e4af2388"
assert sum(x["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED" for x in rr)==15
assert sum(x["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE" for x in rr)==45
assert all((x["current_organization"] and x["current_title"] and x["evidence_url"]) or x["unresolved_reason"] for x in rr)
print("W3-BATCH-0083 PERSISTENCE_RECOVERY PASS")
