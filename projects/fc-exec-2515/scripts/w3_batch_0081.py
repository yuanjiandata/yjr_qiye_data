#!/usr/bin/env python3
import csv,gzip,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"evidence"
W=ROOT/"work"
RESULTS=E/"W3_BATCH_0081_RESULTS.csv"
RESEARCH=E/"W3_BATCH_0081_RESEARCH.tsv.gz"
INPUT=W/"W3_BATCH_0081_INPUT.csv"
INDEX=E/"W3_SEGMENT_INDEX.csv"
def sha256(p):
 h=hashlib.sha256()
 with open(p,"rb") as f:
  for c in iter(lambda:f.read(1<<20),b""): h.update(c)
 return h.hexdigest()
with open(INPUT,encoding="utf-8",newline="") as f: ir=list(csv.DictReader(f))
assert len(ir)==60
assert [int(r["queue_order"]) for r in ir]==list(range(4801,4861))
assert all(r["province"]=="上海" for r in ir)
assert sha256(INPUT)=="e21a2ab631b5e0cafa3e6c03161d626aaa228a5d1437883b3ff0d9fd85b895b1"
with open(RESULTS,encoding="utf-8",newline="") as f: rows=list(csv.DictReader(f))
assert len(rows)==60
assert [int(r["queue_order"]) for r in rows]==list(range(4801,4861))
assert sum(r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED" for r in rows)==5
assert sum(r["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE" for r in rows)==55
assert all(r["evidence_grade"]=="A" for r in rows)
assert all((r["current_organization"] and r["current_title"]) or r["unresolved_reason"] for r in rows)
assert sha256(RESULTS)=="5735649193ff9652a527b87bf6d752f6cf377d84ff50f6c6c8ee50d8d18db02f"
with gzip.open(RESEARCH,"rt",encoding="utf-8",newline="") as f: rr=list(csv.DictReader(f,delimiter="\t"))
assert len(rr)==60
assert [int(r["queue_order"]) for r in rr]==list(range(4801,4861))
assert all(r["mode"]=="FRESH_PUBLIC_RESEARCH" and r["source_person_anchor_url"] and r["search_query"] for r in rr)
assert sha256(RESEARCH)=="5c50c9ff091419988ab2a71f41fdc57aec3830a058388115c00de970378d59e6"
idx=INDEX.read_text(encoding="utf-8")
assert "ledger,54,projects/fc-exec-2515/evidence/W3_BATCH_0081_RESULTS.csv,4801,4860,60,result_segment,ledger,W3-BATCH-0081" in idx
assert "overlay,54,projects/fc-exec-2515/evidence/W3_BATCH_0081_RESULTS.csv,4801,4860,60,result_segment,overlay,W3-BATCH-0081" in idx
print("W3-BATCH-0081 PASS")
