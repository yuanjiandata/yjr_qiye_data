#!/usr/bin/env python3
"""Deterministic validation for FC-EXEC-2515 W3-BATCH-0037."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=2161,2220
EXPECTED_RESULTS_RAW_SHA256="0b635f7ca9828c37479f52a4592996faeba0653d0fb25820963cf1c7c26f4973"
EXPECTED_RESULTS_GZIP_SHA256="4351ddbd47ac0a7762b877dc94b9cb3f933e53fdfb1b670f5585f5d0b6a6ba11"
EXPECTED_RESEARCH_RAW_SHA256="aad62f6df4c68fe67de2ce92d7bd8ce848b828a0d5feddde16eb8c6e90ff8cfb"
EXPECTED_RESEARCH_GZIP_SHA256="1a93846cee909719c70f2818752885d872611eb3e3fef3f75f60f1b571f7e42e"
EXPECTED_PERSON_IDS=['FC2515-P17-R0501', 'FC2515-P17-R0506', 'FC2515-P17-R0509', 'FC2515-P17-R0511', 'FC2515-P17-R0512', 'FC2515-P17-R0513', 'FC2515-P17-R0517', 'FC2515-P17-R0519', 'FC2515-P17-R0522', 'FC2515-P17-R0532', 'FC2515-P17-R0535', 'FC2515-P17-R0537', 'FC2515-P17-R0546', 'FC2515-P17-R0547', 'FC2515-P17-R0550', 'FC2515-P17-R0551', 'FC2515-P17-R0554', 'FC2515-P17-R0560', 'FC2515-P17-R0561', 'FC2515-P17-R0566', 'FC2515-P17-R0567', 'FC2515-P17-R0568', 'FC2515-P17-R0572', 'FC2515-P17-R0573', 'FC2515-P17-R0574', 'FC2515-P17-R0575', 'FC2515-P17-R0576', 'FC2515-P17-R0579', 'FC2515-P17-R0586', 'FC2515-P17-R0589', 'FC2515-P17-R0592', 'FC2515-P18-R0054', 'FC2515-P18-R0099', 'FC2515-P18-R0174', 'FC2515-P18-R0175', 'FC2515-P19-R0002', 'FC2515-P19-R0003', 'FC2515-P19-R0004', 'FC2515-P19-R0005', 'FC2515-P19-R0006', 'FC2515-P19-R0007', 'FC2515-P19-R0009', 'FC2515-P19-R0010', 'FC2515-P19-R0011', 'FC2515-P19-R0012', 'FC2515-P19-R0013', 'FC2515-P19-R0014', 'FC2515-P19-R0016', 'FC2515-P19-R0017', 'FC2515-P19-R0018', 'FC2515-P19-R0019', 'FC2515-P19-R0020', 'FC2515-P19-R0021', 'FC2515-P19-R0022', 'FC2515-P19-R0023', 'FC2515-P19-R0024', 'FC2515-P19-R0025', 'FC2515-P19-R0027', 'FC2515-P19-R0028', 'FC2515-P19-R0029']
EXPECTED_NAMES=['高林', '唐万金', '浦海龙', '黄立', '黄红', '黄晖', '黄卓仁', '黄金杯', '梅秀娟', '章力', '商春利', '阎志', '喻鹏', '程坷', '程阿罗', '程春生', '储震', '温欣艳', '游林', '谢清伦', '谢耀煌', '赖春临', '蔡花', '蔡开云', '蔡燕美', '廖军', '廖森', '谭旭明', '戴辉', '魏琼', '蹇宏', '陈夕林', '陈夕林', '刘洋', '刘洋', '陈志列', '陈丽文', '冯日光', '张宏斌', '陈继山', '李红', '王文银', '王福亮', '江南', '李连柱', '何小鹏', '陈涛', '林水栖', '郁亮', '赵心竹', '胡德兆', '黄健慧', '梁耀铭', '董凡', '曾智明', '温志芬', '廖平元', '万国江', '王岚', '王来春']
EXPECTED_CONFIRMED=[2161, 2162, 2164, 2172, 2173, 2174, 2175, 2176, 2179, 2181, 2182, 2184, 2191, 2196, 2197, 2198, 2201, 2206, 2207, 2213, 2214, 2215, 2216, 2220]

def main():
    rgz=(E/"W3_BATCH_0037_RESULTS.csv.gz").read_bytes()
    qgz=(E/"W3_BATCH_0037_RESEARCH.tsv.gz").read_bytes()
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
    assert Counter(r["province"] for r in results)==Counter({"湖北":31,"湖南":4,"广东":25})
    assert {int(r["queue_order"]) for r in results if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED"}==set(EXPECTED_CONFIRMED)
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":36,"CURRENT_ORG_TITLE_CONFIRMED":24})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":60})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":36,"CONFIRMED":24})
    assert all(r["evidence_url"] or r["unresolved_reason"] for r in results)
    for r in results:
        assert "NAME_ONLY" not in r["identity_resolution"]
        if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED":
            assert r["current_organization"] and r["current_title"] and r["evidence_url"] and not r["unresolved_reason"]
        else:
            assert not r["current_organization"] and not r["current_title"] and r["unresolved_reason"]
    with (E/"W3_SEGMENT_INDEX.csv").open("r",encoding="utf-8-sig",newline="") as f:
        idx=list(csv.DictReader(f))
    expected_segments=[(1,1620),(1621,1680),(1681,1740),(1741,1800),(1801,1860),(1861,1920),(1921,1980),(1981,2040),(2041,2100),(2101,2160),(2161,2220)]
    for kind in ("ledger","overlay"):
        seg=[r for r in idx if r["kind"]==kind]
        seg.sort(key=lambda r:int(r["ordinal"]))
        assert [(int(r["queue_start"]),int(r["queue_end"])) for r in seg]==expected_segments
        assert sum(int(r["row_count"]) for r in seg)==2220
    print("PASS W3-BATCH-0037 next=2221")

if __name__=="__main__":
    main()
