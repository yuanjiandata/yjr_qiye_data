#!/usr/bin/env python3
import csv,gzip,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"evidence"
W=ROOT/"work"
RESULTS=E/"W3_BATCH_0080_RESULTS.csv"
RESEARCH=E/"W3_BATCH_0080_RESEARCH.tsv.gz"
INPUT=W/"W3_BATCH_0080_INPUT.csv"
INDEX=E/"W3_SEGMENT_INDEX.csv"
def sha256(p):
 h=hashlib.sha256()
 with open(p,"rb") as f:
  for c in iter(lambda:f.read(1<<20),b""): h.update(c)
 return h.hexdigest()
with open(INPUT,encoding="utf-8",newline="") as f: ir=list(csv.DictReader(f))
assert len(ir)==60
assert [int(r["queue_order"]) for r in ir]==list(range(4741,4801))
assert sha256(INPUT)=="0bc2dd3224714c4155a1cde25a74089f5b35a44e2e2ae69a9a782db2234f87ce"
with open(RESULTS,encoding="utf-8",newline="") as f: rows=list(csv.DictReader(f))
assert len(rows)==60
assert [int(r["queue_order"]) for r in rows]==list(range(4741,4801))
assert sum(r["province"]=="北京" for r in rows)==28
assert sum(r["province"]=="上海" for r in rows)==32
assert sum(r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED" for r in rows)==3
assert sum(r["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE" for r in rows)==57
assert sum(r["evidence_grade"]=="A" for r in rows)==58
assert sum(r["evidence_grade"]=="B" for r in rows)==2
assert all((r["current_organization"] and r["current_title"]) or r["unresolved_reason"] for r in rows)
assert sha256(RESULTS)=="f6702431b1571301647fcc2cee6565e689faceaa093ce2ef3b85eeddd335def9"
with gzip.open(RESEARCH,"rt",encoding="utf-8",newline="") as f: rr=list(csv.DictReader(f,delimiter="\t"))
assert len(rr)==60
assert [int(r["queue_order"]) for r in rr]==list(range(4741,4801))
assert all(r["mode"]=="FRESH_PUBLIC_RESEARCH" and r["source_person_anchor_url"] and r["search_query"] for r in rr)
assert sha256(RESEARCH)=="1cceaf3da73d5523880ff21ca8c6dfb7a9bb4d5a84d371a3b0b936e9fde0a98b"
idx=INDEX.read_text(encoding="utf-8")
assert "ledger,53,projects/fc-exec-2515/evidence/W3_BATCH_0080_RESULTS.csv,4741,4800,60,result_segment,ledger,W3-BATCH-0080" in idx
assert "overlay,53,projects/fc-exec-2515/evidence/W3_BATCH_0080_RESULTS.csv,4741,4800,60,result_segment,overlay,W3-BATCH-0080" in idx
print("W3-BATCH-0080 PASS")
