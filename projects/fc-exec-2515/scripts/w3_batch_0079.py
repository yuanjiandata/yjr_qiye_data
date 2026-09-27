#!/usr/bin/env python3
import csv,gzip,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"evidence"
RESULTS=E/"W3_BATCH_0079_RESULTS.csv"
RESEARCH=E/"W3_BATCH_0079_RESEARCH.tsv.gz"
INDEX=E/"W3_SEGMENT_INDEX.csv"
def sha256(p):
 h=hashlib.sha256()
 with open(p,"rb") as f:
  for c in iter(lambda:f.read(1<<20),b""): h.update(c)
 return h.hexdigest()
with open(RESULTS,encoding="utf-8",newline="") as f: rows=list(csv.DictReader(f))
assert len(rows)==60
assert [int(r["queue_order"]) for r in rows]==list(range(4681,4741))
assert [int(r["excel_row"]) for r in rows]==list(range(254,314))
assert all(r["province"]=="北京" for r in rows)
assert all(r["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE" for r in rows)
assert all(r["evidence_grade"]=="A" for r in rows)
assert all(not r["current_organization"] and not r["current_title"] and r["unresolved_reason"] for r in rows)
assert sha256(RESULTS)=="a4deda6129f4807edf8564037e55a1655644fc5dae1f890165bf7652fbb596be"
with gzip.open(RESEARCH,"rt",encoding="utf-8",newline="") as f: rr=list(csv.DictReader(f,delimiter="\t"))
assert len(rr)==60
assert [int(r["queue_order"]) for r in rr]==list(range(4681,4741))
assert all(r["mode"]=="FRESH_PUBLIC_RESEARCH" and r["source_person_anchor_url"] and r["search_query"] for r in rr)
assert sha256(RESEARCH)=="fca0959a027766a974b506447d57fe34c93488b6b63dd6466944af6ec923a243"
idx=INDEX.read_text(encoding="utf-8")
assert "ledger,52,projects/fc-exec-2515/evidence/W3_BATCH_0079_RESULTS.csv,4681,4740,60,result_segment,ledger,W3-BATCH-0079" in idx
assert "overlay,52,projects/fc-exec-2515/evidence/W3_BATCH_0079_RESULTS.csv,4681,4740,60,result_segment,overlay,W3-BATCH-0079" in idx
print("W3-BATCH-0079 PASS")
