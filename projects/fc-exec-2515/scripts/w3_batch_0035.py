#!/usr/bin/env python3
"""Deterministic validation for FC-EXEC-2515 W3-BATCH-0035."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=2041,2100
EXPECTED_RESULTS_RAW_SHA256="aefc1b7f63d802c386b0f9d0d62c6a20411282575fc3b67032725f2a32158382"
EXPECTED_RESULTS_GZIP_SHA256="2e85a32849eed26b449aee50b6bac8ae96f8f3a014063a263aade89706c21e84"
EXPECTED_RESEARCH_RAW_SHA256="dbfac53e2a0ef5ba68b3e895b5aa312b830fc62c3c9c5a9f4cb22fb9d1d07350"
EXPECTED_RESEARCH_GZIP_SHA256="e8b969d9098704220d89dda26fe900257db4a9fe491017a71fb6f74ed9b127a7"
EXPECTED_PERSON_IDS=['FC2515-P17-R0174', 'FC2515-P17-R0175', 'FC2515-P17-R0176', 'FC2515-P17-R0177', 'FC2515-P17-R0178', 'FC2515-P17-R0179', 'FC2515-P17-R0180', 'FC2515-P17-R0183', 'FC2515-P17-R0185', 'FC2515-P17-R0189', 'FC2515-P17-R0193', 'FC2515-P17-R0194', 'FC2515-P17-R0195', 'FC2515-P17-R0200', 'FC2515-P17-R0201', 'FC2515-P17-R0203', 'FC2515-P17-R0206', 'FC2515-P17-R0208', 'FC2515-P17-R0215', 'FC2515-P17-R0217', 'FC2515-P17-R0225', 'FC2515-P17-R0226', 'FC2515-P17-R0228', 'FC2515-P17-R0231', 'FC2515-P17-R0234', 'FC2515-P17-R0237', 'FC2515-P17-R0239', 'FC2515-P17-R0240', 'FC2515-P17-R0245', 'FC2515-P17-R0248', 'FC2515-P17-R0250', 'FC2515-P17-R0252', 'FC2515-P17-R0259', 'FC2515-P17-R0260', 'FC2515-P17-R0262', 'FC2515-P17-R0265', 'FC2515-P17-R0266', 'FC2515-P17-R0267', 'FC2515-P17-R0269', 'FC2515-P17-R0271', 'FC2515-P17-R0276', 'FC2515-P17-R0278', 'FC2515-P17-R0279', 'FC2515-P17-R0281', 'FC2515-P17-R0287', 'FC2515-P17-R0288', 'FC2515-P17-R0289', 'FC2515-P17-R0291', 'FC2515-P17-R0292', 'FC2515-P17-R0293', 'FC2515-P17-R0294', 'FC2515-P17-R0295', 'FC2515-P17-R0296', 'FC2515-P17-R0297', 'FC2515-P17-R0298', 'FC2515-P17-R0301', 'FC2515-P17-R0303', 'FC2515-P17-R0304', 'FC2515-P17-R0308', 'FC2515-P17-R0310']
EXPECTED_NAMES=['蔡燕美', '廖军', '廖森', '谭旭明', '戴辉', '魏琼', '蹇宏', '马林武', '王旭', '王静', '王仁宗', '王书会', '王永蓬', '王国华', '王忠标', '王栎栎', '王继刚', '王楠波', '方朝晖', '尹洪涛', '叶杰', '田萍', '冉建波', '付诚', '代德明', '邝远平', '兰坤', '匡玲', '任习东', '邬剑刚', '刘玲', '刘萌', '刘长云', '刘长来', '刘世琴', '刘红艳', '刘丽君', '刘国梁', '刘金成', '刘顺妮', '关晓斌', '江勇', '许俐', '许开华', '孙应安', '孙桃香', '苏鸣', '李达', '李刚', '李进', '李进', '李果', '李俊', '李俊', '李勇', '李健', '李万军', '李万清', '李文帅', '李文喜']
EXPECTED_CONFIRMED=[2047, 2051, 2052, 2053, 2054, 2056, 2058, 2065, 2069, 2070, 2073, 2074, 2082, 2084, 2085, 2096, 2098, 2100]

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rgz=(E/"W3_BATCH_0035_RESULTS.csv.gz").read_bytes()
    qgz=(E/"W3_BATCH_0035_RESEARCH.tsv.gz").read_bytes()
    assert hashlib.sha256(rgz).hexdigest()==EXPECTED_RESULTS_GZIP_SHA256
    assert hashlib.sha256(qgz).hexdigest()==EXPECTED_RESEARCH_GZIP_SHA256
    raw=gzip.decompress(rgz); research_raw=gzip.decompress(qgz)
    assert hashlib.sha256(raw).hexdigest()==EXPECTED_RESULTS_RAW_SHA256
    assert hashlib.sha256(research_raw).hexdigest()==EXPECTED_RESEARCH_RAW_SHA256
    results=list(csv.DictReader(raw.decode("utf-8-sig").splitlines()))
    research=list(csv.DictReader(research_raw.decode("utf-8-sig").splitlines(),delimiter="\t"))
    expected=list(range(START,END+1))
    assert len(queue)==len(results)==len(research)==60
    assert [int(r["queue_order"]) for r in queue]==expected
    assert [int(r["queue_order"]) for r in results]==expected
    assert [int(r["queue_order"]) for r in research]==expected
    assert [r["person_id"] for r in queue]==EXPECTED_PERSON_IDS
    assert [r["person_id"] for r in results]==EXPECTED_PERSON_IDS
    assert [r["name_normalized"] for r in queue]==EXPECTED_NAMES
    assert [r["name_normalized"] for r in results]==EXPECTED_NAMES
    assert {r["priority"] for r in queue}=={"P1_IDENTITY"}
    assert Counter(r["province"] for r in queue)==Counter({"湖北":60})
    assert {int(r["queue_order"]) for r in results if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED"}==set(EXPECTED_CONFIRMED)
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":42,"CURRENT_ORG_TITLE_CONFIRMED":18})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":60})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":42,"CONFIRMED":18})
    assert all(r["evidence_url"] or r["unresolved_reason"] for r in results)
    for r in results:
        assert "NAME_ONLY" not in r["identity_resolution"]
        if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED":
            assert r["current_organization"] and r["current_title"] and r["evidence_url"] and not r["unresolved_reason"]
        else:
            assert not r["current_organization"] and not r["current_title"] and r["unresolved_reason"]
    with (E/"W3_SEGMENT_INDEX.csv").open("r",encoding="utf-8-sig",newline="") as f:
        idx=list(csv.DictReader(f))
    expected_segments=[(1,1620),(1621,1680),(1681,1740),(1741,1800),(1801,1860),(1861,1920),(1921,1980),(1981,2040),(2041,2100)]
    for kind in ("ledger","overlay"):
        seg=[r for r in idx if r["kind"]==kind]
        seg.sort(key=lambda r:int(r["ordinal"]))
        assert [(int(r["queue_start"]),int(r["queue_end"])) for r in seg]==expected_segments
        assert sum(int(r["row_count"]) for r in seg)==2100
    print("PASS W3-BATCH-0035 next=2101")

if __name__=="__main__":
    main()
