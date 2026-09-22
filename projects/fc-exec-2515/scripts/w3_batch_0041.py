#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0041."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=2401,2460
EXPECTED_RESULTS_RAW_SHA256="83442766167ec90a516ba682e32b50693e60ebe2a84212ed0dc07b76d28ef632"
EXPECTED_RESULTS_GZIP_SHA256="702d035845e4a1054e509b8f4eb8d3a813e6e87d93c32a485a7e47c42bdeaff8"
EXPECTED_RESEARCH_RAW_SHA256="c8e495c16bd207f1dec636959b9c7c7fe0cfc3798e38dc8f1be1acab3aec872f"
EXPECTED_RESEARCH_GZIP_SHA256="5641e9edee639ff36c3a221c538bf3da0eb3029d4c1f8751440b294abe4b706d"
EXPECTED_PERSON_IDS=['FC2515-P19-R0242', 'FC2515-P19-R0246', 'FC2515-P19-R0251', 'FC2515-P19-R0253', 'FC2515-P19-R0255', 'FC2515-P19-R0258', 'FC2515-P19-R0262', 'FC2515-P19-R0263', 'FC2515-P19-R0265', 'FC2515-P19-R0271', 'FC2515-P19-R0274', 'FC2515-P19-R0276', 'FC2515-P19-R0279', 'FC2515-P19-R0280', 'FC2515-P19-R0281', 'FC2515-P19-R0282', 'FC2515-P19-R0284', 'FC2515-P19-R0285', 'FC2515-P19-R0288', 'FC2515-P19-R0296', 'FC2515-P19-R0297', 'FC2515-P19-R0299', 'FC2515-P19-R0300', 'FC2515-P19-R0307', 'FC2515-P19-R0310', 'FC2515-P19-R0313', 'FC2515-P19-R0315', 'FC2515-P19-R0319', 'FC2515-P19-R0322', 'FC2515-P19-R0327', 'FC2515-P19-R0329', 'FC2515-P19-R0330', 'FC2515-P19-R0333', 'FC2515-P19-R0336', 'FC2515-P19-R0337', 'FC2515-P19-R0340', 'FC2515-P19-R0345', 'FC2515-P19-R0349', 'FC2515-P19-R0352', 'FC2515-P19-R0353', 'FC2515-P19-R0356', 'FC2515-P19-R0360', 'FC2515-P19-R0363', 'FC2515-P19-R0364', 'FC2515-P19-R0367', 'FC2515-P19-R0371', 'FC2515-P19-R0373', 'FC2515-P19-R0374', 'FC2515-P19-R0382', 'FC2515-P19-R0385', 'FC2515-P19-R0387', 'FC2515-P19-R0388', 'FC2515-P19-R0391', 'FC2515-P19-R0397', 'FC2515-P19-R0398', 'FC2515-P19-R0399', 'FC2515-P19-R0400', 'FC2515-P19-R0404', 'FC2515-P19-R0405', 'FC2515-P19-R0410']
EXPECTED_NAMES=['陈志列', '赵心竹', '覃九三', '朱自琴', '言登峰', '郑文强', '董凡', '马学沛', '刘文华', '欧先涛', '黄俊辉', '叶远璋', '李德', '李连柱', '吴启超', '吴艳芬', '张伟明', '陈翀', '林治平', '张红伟', '陈宏海', '周细妹', '凌福传', '徐耀目', '缪国乐', '何坤皇', '罗桂芳', '廖平元', '刘远程', '张琳', '陈涛', '贺妙忠', '魏海勇', '陈志胜', '陈宝家', '彭晋谦', '白宝鲲', '吴丰礼', '陈国良', '陈健民', '袁斌', '李维', '张瑞', '张燕航', '郭丛枢', '万国江', '朱英杰', '李茜', '黄达昌', '曾锦俊', '李积回', '张辉雄', '洪家虎', '陈宇', '陈弘祖', '陈宇驰', '林水栖', '王明旺', '支勇', '陈高文']
EXPECTED_CONFIRMED=[2401, 2406, 2407, 2414, 2428, 2438, 2444, 2451, 2457, 2458]
EXPECTED_FRESH=list(range(START,END+1))

def read_gz(path, delimiter=","):
    b=path.read_bytes()
    raw=gzip.decompress(b)
    rows=list(csv.DictReader(raw.decode("utf-8-sig").splitlines(),delimiter=delimiter))
    return b,raw,rows

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rb,rr,results=read_gz(E/"W3_BATCH_0041_RESULTS.csv.gz")
    qb,qr,research=read_gz(E/"W3_BATCH_0041_RESEARCH.tsv.gz","\t")

    assert hashlib.sha256(rr).hexdigest()==EXPECTED_RESULTS_RAW_SHA256
    assert hashlib.sha256(rb).hexdigest()==EXPECTED_RESULTS_GZIP_SHA256
    assert hashlib.sha256(qr).hexdigest()==EXPECTED_RESEARCH_RAW_SHA256
    assert hashlib.sha256(qb).hexdigest()==EXPECTED_RESEARCH_GZIP_SHA256

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
    assert Counter(r["province"] for r in queue)==Counter({"广东":60})
    assert all(r["identity_anchor_url"].startswith("https://www.acfic.org.cn/") for r in results)
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":50,"CURRENT_ORG_TITLE_CONFIRMED":10})
    assert [int(r["queue_order"]) for r in results if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED"]==EXPECTED_CONFIRMED
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":55,"B":5})
    assert all(not r["identity_resolution"].startswith("REUSED_SEALED_EVIDENCE_") for r in results)
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":50,"CONFIRMED":10})
    assert all(r["web_query"] and r["identity_anchor_url"] and r["research_note"] for r in research)

    for r in results:
        assert "NAME_ONLY" not in r["identity_resolution"]
        if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED":
            assert r["current_organization"] and r["current_title"] and r["evidence_url"] and not r["unresolved_reason"]
        else:
            assert not r["current_organization"] and not r["current_title"] and r["unresolved_reason"]

    idx=list(csv.DictReader((E/"W3_SEGMENT_INDEX.csv").open("r",encoding="utf-8-sig",newline="")))
    for kind in ("ledger","overlay"):
        entries=sorted((r for r in idx if r["kind"]==kind),key=lambda r:int(r["ordinal"]))
        expected_start=1
        for e in entries:
            start,end,count=map(int,(e["queue_start"],e["queue_end"],e["row_count"]))
            assert start==expected_start,(kind,expected_start,start)
            assert end-start+1==count
            expected_start=end+1
        assert expected_start==2461
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0041"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0041_RESULTS.csv.gz"
        assert int(last["queue_start"])==2401 and int(last["queue_end"])==2460
    print("PASS W3-BATCH-0041 rows=60 confirmed=10 unresolved=50 grades=A55/B5 logical_end=2460")

if __name__=="__main__":
    main()
