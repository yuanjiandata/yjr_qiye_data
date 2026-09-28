#!/usr/bin/env python3
import csv,gzip,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"evidence"; W=ROOT/"work"
RESULTS=E/"W3_BATCH_0082_RESULTS.csv"; RESEARCH=E/"W3_BATCH_0082_RESEARCH.tsv.gz"
INPUT=W/"W3_BATCH_0082_INPUT.csv"; INDEX=E/"W3_SEGMENT_INDEX.csv"
def sha256(p):
 h=hashlib.sha256()
 with open(p,"rb") as f:
  for c in iter(lambda:f.read(1<<20),b""): h.update(c)
 return h.hexdigest()
with open(INPUT,encoding="utf-8",newline="") as f: ir=list(csv.DictReader(f))
assert len(ir)==60
assert [int(r["queue_order"]) for r in ir]==list(range(4861,4921))
assert all(r["province"]=="上海" for r in ir)
assert sha256(INPUT)=="22cc932a7e4cb536e43834f977185dd261cd2a5371d4f28b84a1ea9f079430d1"
with open(RESULTS,encoding="utf-8",newline="") as f: rows=list(csv.DictReader(f))
assert len(rows)==60
assert [int(r["queue_order"]) for r in rows]==list(range(4861,4921))
assert sum(r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED" for r in rows)==9
assert sum(r["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE" for r in rows)==51
assert all(r["evidence_grade"]=="A" for r in rows)
assert all((r["current_organization"] and r["current_title"]) or r["unresolved_reason"] for r in rows)
assert sha256(RESULTS)=="8f993804dbdff40add1c7a60397dce9a4903455c0422d11c25bc4b63903d1070"
with gzip.open(RESEARCH,"rt",encoding="utf-8",newline="") as f: rr=list(csv.DictReader(f,delimiter="\t"))
assert len(rr)==60
assert [int(r["queue_order"]) for r in rr]==list(range(4861,4921))
assert all(r["mode"]=="FRESH_PUBLIC_RESEARCH" and r["source_person_anchor_url"] and r["search_query"] for r in rr)
assert sha256(RESEARCH)=="86c702b760ed83d32cb14d724df56297e2f688489cb91ac9df333fe25d255d48"
idx=INDEX.read_text(encoding="utf-8")
assert "ledger,55,projects/fc-exec-2515/evidence/W3_BATCH_0082_RESULTS.csv,4861,4920,60,result_segment,ledger,W3-BATCH-0082" in idx
assert "overlay,55,projects/fc-exec-2515/evidence/W3_BATCH_0082_RESULTS.csv,4861,4920,60,result_segment,overlay,W3-BATCH-0082" in idx
print("W3-BATCH-0082 PASS")
