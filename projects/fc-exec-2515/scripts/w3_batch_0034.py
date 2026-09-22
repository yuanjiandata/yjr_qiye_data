#!/usr/bin/env python3
"""Deterministic validation for FC-EXEC-2515 W3-BATCH-0034."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=1981,2040
EXPECTED_RESULTS_RAW_SHA256="2b4ba95b7822a8e5b2837977e121ccec3e99e9bcea3d4e6538a3b96003de66db"
EXPECTED_RESULTS_GZIP_SHA256="1d1eb5f6db6c7e06b279de121ba3932153597fa7f7b61a6be0a6c6ae20326f99"
EXPECTED_RESEARCH_RAW_SHA256="22dc2c55c2fc5c32b35a4a0c258b0e91938e9f874f8d2e2f0262dc2d906c3a6c"
EXPECTED_RESEARCH_GZIP_SHA256="237aa1e95be81bd23f149f5c2359505ebd403e478d8069acf55420bd93e899f1"
EXPECTED_PERSON_IDS=['FC2515-P17-R0114', 'FC2515-P17-R0115', 'FC2515-P17-R0116', 'FC2515-P17-R0117', 'FC2515-P17-R0118', 'FC2515-P17-R0119', 'FC2515-P17-R0120', 'FC2515-P17-R0121', 'FC2515-P17-R0122', 'FC2515-P17-R0123', 'FC2515-P17-R0124', 'FC2515-P17-R0125', 'FC2515-P17-R0126', 'FC2515-P17-R0127', 'FC2515-P17-R0128', 'FC2515-P17-R0129', 'FC2515-P17-R0130', 'FC2515-P17-R0131', 'FC2515-P17-R0132', 'FC2515-P17-R0133', 'FC2515-P17-R0134', 'FC2515-P17-R0135', 'FC2515-P17-R0136', 'FC2515-P17-R0137', 'FC2515-P17-R0138', 'FC2515-P17-R0139', 'FC2515-P17-R0140', 'FC2515-P17-R0141', 'FC2515-P17-R0142', 'FC2515-P17-R0143', 'FC2515-P17-R0144', 'FC2515-P17-R0145', 'FC2515-P17-R0146', 'FC2515-P17-R0147', 'FC2515-P17-R0148', 'FC2515-P17-R0149', 'FC2515-P17-R0150', 'FC2515-P17-R0151', 'FC2515-P17-R0152', 'FC2515-P17-R0153', 'FC2515-P17-R0154', 'FC2515-P17-R0155', 'FC2515-P17-R0156', 'FC2515-P17-R0157', 'FC2515-P17-R0158', 'FC2515-P17-R0159', 'FC2515-P17-R0160', 'FC2515-P17-R0161', 'FC2515-P17-R0162', 'FC2515-P17-R0163', 'FC2515-P17-R0164', 'FC2515-P17-R0165', 'FC2515-P17-R0166', 'FC2515-P17-R0167', 'FC2515-P17-R0168', 'FC2515-P17-R0169', 'FC2515-P17-R0170', 'FC2515-P17-R0171', 'FC2515-P17-R0172', 'FC2515-P17-R0173']
EXPECTED_NAMES=['宋伟锋', '宋昵荔', '宋嘉桓', '张卫元', '张文明', '张文旗', '张平安', '陈军', '陈纯星', '陈莉莉', '陈晓林', '陈继承', '陈鸿杰', '陈新云', '范双涛', '罗振林', '罗绪军', '金波', '金海', '周志专', '周锦平', '郑强', '郑大斌', '赵世运', '赵林平', '胡秀容', '胡爱娣', '胡越高', '柯碧松', '段卫昌', '段东宁', '施江昆', '秦德平', '夏锡汉', '徐志新', '徐劲松', '徐国胜', '徐凌峰', '高林', '浦海龙', '黄立', '黄红', '黄晖', '黄卓仁', '黄金杯', '梅秀娟', '章力', '商春利', '阎志', '喻鹏', '程阿罗', '程春生', '储震', '温欣艳', '游林', '谢清伦', '谢耀煌', '赖春临', '蔡花', '蔡开云']
EXPECTED_CONFIRMED=[1986, 1988, 1989, 1990, 1991, 1995, 1997, 1999, 2000, 2007, 2009, 2010, 2015, 2017, 2019, 2021, 2029, 2030, 2031, 2032, 2035, 2037, 2038, 2040]

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rgz=(E/"W3_BATCH_0034_RESULTS.csv.gz").read_bytes()
    qgz=(E/"W3_BATCH_0034_RESEARCH.tsv.gz").read_bytes()
    assert hashlib.sha256(rgz).hexdigest()==EXPECTED_RESULTS_GZIP_SHA256
    assert hashlib.sha256(qgz).hexdigest()==EXPECTED_RESEARCH_GZIP_SHA256
    raw=gzip.decompress(rgz); research_raw=gzip.decompress(qgz)
    assert hashlib.sha256(raw).hexdigest()==EXPECTED_RESULTS_RAW_SHA256
    assert hashlib.sha256(research_raw).hexdigest()==EXPECTED_RESEARCH_RAW_SHA256
    results=list(csv.DictReader(raw.decode("utf-8-sig").splitlines()))
    research=list(csv.DictReader(research_raw.decode("utf-8-sig").splitlines(),delimiter="\t"))
    expected=list(range(START,END+1))
    assert len(queue)==len(results)==60
    assert len(research)==39
    assert [int(r["queue_order"]) for r in queue]==expected
    assert [int(r["queue_order"]) for r in results]==expected
    assert [r["person_id"] for r in queue]==EXPECTED_PERSON_IDS
    assert [r["person_id"] for r in results]==EXPECTED_PERSON_IDS
    assert [r["name_normalized"] for r in queue]==EXPECTED_NAMES
    assert [r["name_normalized"] for r in results]==EXPECTED_NAMES
    assert {r["priority"] for r in queue}=={"P1_IDENTITY"}
    assert Counter(r["province"] for r in queue)==Counter({"湖北":60})
    assert {int(r["queue_order"]) for r in results if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED"}==set(EXPECTED_CONFIRMED)
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":36,"CURRENT_ORG_TITLE_CONFIRMED":24})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":59,"B":1})
    assert all(r["evidence_url"] or r["unresolved_reason"] for r in results)
    for r in results:
        assert "NAME_ONLY" not in r["identity_resolution"]
        if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED":
            assert r["current_organization"] and r["current_title"] and r["evidence_url"] and not r["unresolved_reason"]
        else:
            assert not r["current_organization"] and not r["current_title"] and r["unresolved_reason"]
    fresh=[r for r in results if not r["identity_resolution"].startswith("REUSED_SEALED_EVIDENCE_")]
    assert [r["queue_order"] for r in fresh]==[r["queue_order"] for r in research]
    with (E/"W3_SEGMENT_INDEX.csv").open("r",encoding="utf-8-sig",newline="") as f:
        idx=list(csv.DictReader(f))
    expected_segments=[(1,1620),(1621,1680),(1681,1740),(1741,1800),(1801,1860),(1861,1920),(1921,1980),(1981,2040)]
    for kind in ("ledger","overlay"):
        seg=[r for r in idx if r["kind"]==kind]
        seg.sort(key=lambda r:int(r["ordinal"]))
        assert [(int(r["queue_start"]),int(r["queue_end"])) for r in seg]==expected_segments
        assert sum(int(r["row_count"]) for r in seg)==2040
    print("PASS W3-BATCH-0034 next=2041")

if __name__=="__main__":
    main()
