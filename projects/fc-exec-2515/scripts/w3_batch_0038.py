#!/usr/bin/env python3
"""Deterministic validation for FC-EXEC-2515 W3-BATCH-0038."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=2221,2280
EXPECTED_RESULTS_RAW_SHA256="672f07e1a3c4be5ffc9eda0ab8d8812631e19c35df7324b87dd4d2ad329509e0"
EXPECTED_RESULTS_GZIP_SHA256="09cf9ff2fbb4c430c6a0cf12b8dcba8ca30ba5aa194b28cd089f29794deacaa9"
EXPECTED_RESEARCH_RAW_SHA256="69a859695aeed84f0cba900fba6448041b63e5edb2ba4252e5e143f43a52b13d"
EXPECTED_RESEARCH_GZIP_SHA256="f94f8a5326739d0e51cf3e5ed379747224ca04053caecf53b36366ad6ef769a0"
EXPECTED_PERSON_IDS=['FC2515-P19-R0030', 'FC2515-P19-R0031', 'FC2515-P19-R0032', 'FC2515-P19-R0033', 'FC2515-P19-R0034', 'FC2515-P19-R0035', 'FC2515-P19-R0036', 'FC2515-P19-R0037', 'FC2515-P19-R0038', 'FC2515-P19-R0039', 'FC2515-P19-R0040', 'FC2515-P19-R0041', 'FC2515-P19-R0042', 'FC2515-P19-R0043', 'FC2515-P19-R0044', 'FC2515-P19-R0045', 'FC2515-P19-R0046', 'FC2515-P19-R0047', 'FC2515-P19-R0048', 'FC2515-P19-R0049', 'FC2515-P19-R0051', 'FC2515-P19-R0052', 'FC2515-P19-R0053', 'FC2515-P19-R0054', 'FC2515-P19-R0055', 'FC2515-P19-R0056', 'FC2515-P19-R0057', 'FC2515-P19-R0058', 'FC2515-P19-R0059', 'FC2515-P19-R0060', 'FC2515-P19-R0061', 'FC2515-P19-R0062', 'FC2515-P19-R0063', 'FC2515-P19-R0064', 'FC2515-P19-R0065', 'FC2515-P19-R0066', 'FC2515-P19-R0067', 'FC2515-P19-R0068', 'FC2515-P19-R0069', 'FC2515-P19-R0070', 'FC2515-P19-R0071', 'FC2515-P19-R0072', 'FC2515-P19-R0073', 'FC2515-P19-R0074', 'FC2515-P19-R0075', 'FC2515-P19-R0076', 'FC2515-P19-R0077', 'FC2515-P19-R0078', 'FC2515-P19-R0079', 'FC2515-P19-R0080', 'FC2515-P19-R0081', 'FC2515-P19-R0082', 'FC2515-P19-R0083', 'FC2515-P19-R0084', 'FC2515-P19-R0085', 'FC2515-P19-R0086', 'FC2515-P19-R0087', 'FC2515-P19-R0088', 'FC2515-P19-R0089', 'FC2515-P19-R0090']
EXPECTED_NAMES=['王明旺', '冯日光', '吕耀华', '李红', '李立勉', '李积回', '吴木棠', '吴胜丰', '张红伟', '张宏斌', '张燕航', '陈翀', '陈东平', '陈宏海', '陈继山', '郭清海', '黄俊辉', '彭晋谦', '蔡仲光', '关向明', '殷民', '卢小周', '王永辉', '王锐祥', '丘育华', '苏展航', '杜兰', '吴丹琳', '陈镇雄', '幸运', '谢萌', '薛华', '魏国华', '李勇', '励建炬', '吴宪', '张春华', '覃九三', '朱自琴', '言登峰', '郑文强', '马学沛', '刘文华', '欧先涛', '叶远璋', '李德', '吴启超', '吴艳芬', '张伟明', '林治平', '周细妹', '凌福传', '徐耀目', '缪国乐', '何坤皇', '罗桂芳', '刘远程', '张琳', '贺妙忠', '魏海勇']
EXPECTED_CONFIRMED=[2221, 2222, 2224, 2226, 2240, 2253]

def main():
    rgz=(E/"W3_BATCH_0038_RESULTS.csv.gz").read_bytes()
    qgz=(E/"W3_BATCH_0038_RESEARCH.tsv.gz").read_bytes()
    assert hashlib.sha256(rgz).hexdigest()==EXPECTED_RESULTS_GZIP_SHA256
    assert hashlib.sha256(qgz).hexdigest()==EXPECTED_RESEARCH_GZIP_SHA256
    raw=gzip.decompress(rgz); research_raw=gzip.decompress(qgz)
    assert hashlib.sha256(raw).hexdigest()==EXPECTED_RESULTS_RAW_SHA256
    assert hashlib.sha256(research_raw).hexdigest()==EXPECTED_RESEARCH_RAW_SHA256
    results=list(csv.DictReader(raw.decode("utf-8-sig").splitlines()))
    research=list(csv.DictReader(research_raw.decode("utf-8-sig").splitlines(),delimiter="\t"))
    expected=list(range(START,END+1))
    assert len(results)==len(research)==60
    assert [int(r["queue_order"]) for r in results]==expected
    assert [int(r["queue_order"]) for r in research]==expected
    assert [r["person_id"] for r in results]==EXPECTED_PERSON_IDS
    assert [r["name_normalized"] for r in results]==EXPECTED_NAMES
    assert len(set(EXPECTED_PERSON_IDS))==60
    assert Counter(r["province"] for r in results)==Counter({"广东":60})
    assert {int(r["queue_order"]) for r in results if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED"}==set(EXPECTED_CONFIRMED)
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":54,"CURRENT_ORG_TITLE_CONFIRMED":6})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":60})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":54,"CONFIRMED":6})
    assert all(r["evidence_url"] or r["unresolved_reason"] for r in results)
    for r in results:
        assert "NAME_ONLY" not in r["identity_resolution"]
        if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED":
            assert r["current_organization"] and r["current_title"] and r["evidence_url"] and not r["unresolved_reason"]
        else:
            assert not r["current_organization"] and not r["current_title"] and r["unresolved_reason"]
    with (E/"W3_SEGMENT_INDEX.csv").open("r",encoding="utf-8-sig",newline="") as f:
        idx=list(csv.DictReader(f))
    expected_segments=[(1,1620),(1621,1680),(1681,1740),(1741,1800),(1801,1860),(1861,1920),(1921,1980),(1981,2040),(2041,2100),(2101,2160),(2161,2220),(2221,2280)]
    for kind in ("ledger","overlay"):
        seg=[r for r in idx if r["kind"]==kind]
        seg.sort(key=lambda r:int(r["ordinal"]))
        assert [(int(r["queue_start"]),int(r["queue_end"])) for r in seg]==expected_segments
        assert sum(int(r["row_count"]) for r in seg)==2280
    print("PASS W3-BATCH-0038 next=2281")

if __name__=="__main__":
    main()
