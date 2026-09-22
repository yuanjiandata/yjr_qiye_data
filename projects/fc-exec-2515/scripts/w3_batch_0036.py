#!/usr/bin/env python3
"""Deterministic validation for FC-EXEC-2515 W3-BATCH-0036."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=2101,2160
EXPECTED_RESULTS_RAW_SHA256="cf87ffb824d5d831e636eb2737d95034549f3207d8bc751a966d6927b744085d"
EXPECTED_RESULTS_GZIP_SHA256="2a708c540683f0e2ee84c10cf1b9f6efda749ba74b61093a6652f230233c99ef"
EXPECTED_RESEARCH_RAW_SHA256="a0f5f86951b00da65fbe42953fb24632d94e602ef6e381e301ad888e754a9aaf"
EXPECTED_RESEARCH_GZIP_SHA256="8bef99e7894bbda5e806719d3d771afa9c9ada69e7471d889ff1effbf25cc3ec"
EXPECTED_PERSON_IDS=['FC2515-P17-R0311', 'FC2515-P17-R0315', 'FC2515-P17-R0318', 'FC2515-P17-R0319', 'FC2515-P17-R0324', 'FC2515-P17-R0325', 'FC2515-P17-R0326', 'FC2515-P17-R0327', 'FC2515-P17-R0329', 'FC2515-P17-R0330', 'FC2515-P17-R0333', 'FC2515-P17-R0337', 'FC2515-P17-R0338', 'FC2515-P17-R0343', 'FC2515-P17-R0346', 'FC2515-P17-R0347', 'FC2515-P17-R0348', 'FC2515-P17-R0349', 'FC2515-P17-R0350', 'FC2515-P17-R0355', 'FC2515-P17-R0357', 'FC2515-P17-R0363', 'FC2515-P17-R0364', 'FC2515-P17-R0366', 'FC2515-P17-R0371', 'FC2515-P17-R0374', 'FC2515-P17-R0375', 'FC2515-P17-R0378', 'FC2515-P17-R0385', 'FC2515-P17-R0406', 'FC2515-P17-R0411', 'FC2515-P17-R0412', 'FC2515-P17-R0415', 'FC2515-P17-R0416', 'FC2515-P17-R0417', 'FC2515-P17-R0419', 'FC2515-P17-R0428', 'FC2515-P17-R0429', 'FC2515-P17-R0431', 'FC2515-P17-R0432', 'FC2515-P17-R0436', 'FC2515-P17-R0439', 'FC2515-P17-R0441', 'FC2515-P17-R0442', 'FC2515-P17-R0449', 'FC2515-P17-R0452', 'FC2515-P17-R0458', 'FC2515-P17-R0460', 'FC2515-P17-R0463', 'FC2515-P17-R0465', 'FC2515-P17-R0466', 'FC2515-P17-R0470', 'FC2515-P17-R0471', 'FC2515-P17-R0474', 'FC2515-P17-R0479', 'FC2515-P17-R0487', 'FC2515-P17-R0492', 'FC2515-P17-R0493', 'FC2515-P17-R0494', 'FC2515-P17-R0497']
EXPECTED_NAMES=['李玉保', '李兴东', '李树锋', '李彩云', '杨帆', '杨帆', '杨华', '杨明', '杨义华', '杨义祖', '杨红才', '肖旭', '肖凯旋', '吴天延', '吴宇星', '吴俊峰', '吴智勇', '何中林', '何建刚', '邹贤城', '库尔班江•泰吾克力', '宋伟锋', '宋昵荔', '宋嘉桓', '张卫元', '张文明', '张文旗', '张平安', '陈军', '陈纯星', '陈莉莉', '陈晓林', '陈继承', '陈鸿杰', '陈新云', '范双涛', '罗振林', '罗绪军', '金波', '金海', '周志专', '周锦平', '郑强', '郑大斌', '赵世运', '赵林平', '胡秀容', '胡勇政', '胡爱娣', '胡越高', '柯碧松', '段卫昌', '段东宁', '施江昆', '秦德平', '夏锡汉', '徐志新', '徐劲松', '徐国胜', '徐凌峰']
EXPECTED_CONFIRMED=[2104, 2113, 2117, 2118, 2121, 2127, 2129, 2130, 2131, 2132, 2136, 2138, 2140, 2141, 2148, 2149, 2151, 2152, 2157, 2159]

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rgz=(E/"W3_BATCH_0036_RESULTS.csv.gz").read_bytes()
    qgz=(E/"W3_BATCH_0036_RESEARCH.tsv.gz").read_bytes()
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
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":40,"CURRENT_ORG_TITLE_CONFIRMED":20})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":59,"B":1})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":40,"CONFIRMED":20})
    assert all(r["evidence_url"] or r["unresolved_reason"] for r in results)
    for r in results:
        assert "NAME_ONLY" not in r["identity_resolution"]
        if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED":
            assert r["current_organization"] and r["current_title"] and r["evidence_url"] and not r["unresolved_reason"]
        else:
            assert not r["current_organization"] and not r["current_title"] and r["unresolved_reason"]
    with (E/"W3_SEGMENT_INDEX.csv").open("r",encoding="utf-8-sig",newline="") as f:
        idx=list(csv.DictReader(f))
    expected_segments=[(1,1620),(1621,1680),(1681,1740),(1741,1800),(1801,1860),(1861,1920),(1921,1980),(1981,2040),(2041,2100),(2101,2160)]
    for kind in ("ledger","overlay"):
        seg=[r for r in idx if r["kind"]==kind]
        seg.sort(key=lambda r:int(r["ordinal"]))
        assert [(int(r["queue_start"]),int(r["queue_end"])) for r in seg]==expected_segments
        assert sum(int(r["row_count"]) for r in seg)==2160
    print("PASS W3-BATCH-0036 next=2161")

if __name__=="__main__":
    main()
