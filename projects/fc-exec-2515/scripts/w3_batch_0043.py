#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0043."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=2521,2580
EXPECTED_RESULTS_SHA256="1f10d91def44635901deec270abfdb052745935b4da635b611a9072232387abc"
EXPECTED_RESEARCH_SHA256="420dd56d896a79418d860f396b8f8470edb941a2b683504459c5e973fc1e02e7"
EXPECTED_PERSON_IDS=['FC2515-P19-R0559', 'FC2515-P19-R0560', 'FC2515-P19-R0564', 'FC2515-P19-R0565', 'FC2515-P19-R0566', 'FC2515-P19-R0569', 'FC2515-P19-R0570', 'FC2515-P19-R0572', 'FC2515-P19-R0573', 'FC2515-P19-R0574', 'FC2515-P19-R0580', 'FC2515-P19-R0581', 'FC2515-P19-R0584', 'FC2515-P19-R0585', 'FC2515-P19-R0586', 'FC2515-P19-R0589', 'FC2515-P19-R0591', 'FC2515-P19-R0596', 'FC2515-P19-R0597', 'FC2515-P19-R0600', 'FC2515-P19-R0601', 'FC2515-P19-R0603', 'FC2515-P19-R0614', 'FC2515-P19-R0618', 'FC2515-P19-R0621', 'FC2515-P20-R0002', 'FC2515-P20-R0004', 'FC2515-P20-R0005', 'FC2515-P20-R0006', 'FC2515-P20-R0007', 'FC2515-P20-R0009', 'FC2515-P20-R0010', 'FC2515-P20-R0011', 'FC2515-P20-R0012', 'FC2515-P20-R0013', 'FC2515-P20-R0014', 'FC2515-P20-R0015', 'FC2515-P20-R0016', 'FC2515-P20-R0017', 'FC2515-P20-R0018', 'FC2515-P20-R0019', 'FC2515-P20-R0020', 'FC2515-P20-R0021', 'FC2515-P20-R0022', 'FC2515-P20-R0023', 'FC2515-P20-R0024', 'FC2515-P20-R0025', 'FC2515-P20-R0027', 'FC2515-P20-R0028', 'FC2515-P20-R0029', 'FC2515-P20-R0030', 'FC2515-P20-R0031', 'FC2515-P20-R0032', 'FC2515-P20-R0033', 'FC2515-P20-R0034', 'FC2515-P20-R0035', 'FC2515-P20-R0036', 'FC2515-P20-R0037', 'FC2515-P20-R0038', 'FC2515-P20-R0039']
EXPECTED_NAMES=['潘康虎', '戴汝新', '马少福', '王来春', '王诗增', '列海权', '吕耀华', '刘晋嵩', '刘根森', '许凌', '吴芳华', '吴学明', '张莹', '张耀华', '陈丹丹', '周厚立', '郑林栋', '彭少衍', '曾智明', '廖伊曼', '霍启山', '戴进杰', '贺建东', '崔家荣', '吴胜丰', '任清华', '林胜', '黄琅', '林峰', '龙丁敏', '陈益智', '刘文民', '刘文军', '吴汉陵', '王大富', '黄召华', '张跃光', '朱鼎健', '潘永强', '伍苏国', '李建炜', '杨坤', '李玮', '王勇', '黄海', '胡祥', '许方瑜', '杨莹', '戴扬', '李辉', '刘景萍', '赵树华', '桂金德', '沈琦雅', '宋军', '刘明东', '邢丹丹', '陈杰', '庄炳聪', '徐心敬']
EXPECTED_AMBIGUITY_GROUP_IDS=['ANG-1020', 'ANG-0983', 'ANG-1086', 'ANG-1026', 'ANG-1030', 'ANG-0935', 'ANG-0945', 'ANG-0938', 'ANG-0939', 'ANG-1048', 'ANG-0956', 'ANG-0950', 'ANG-0975', 'ANG-0974', 'ANG-1066', 'ANG-0957', 'ANG-1060', 'ANG-0978', 'ANG-0988', 'ANG-0964', 'ANG-1084', 'ANG-0984', 'ANG-1053', 'ANG-0962', 'ANG-0954', 'ANG-1102', 'ANG-1143', 'ANG-1191', 'ANG-1140', 'ANG-1193', 'ANG-1182', 'ANG-1107', 'ANG-1106', 'ANG-1112', 'ANG-1152', 'ANG-1189', 'ANG-1122', 'ANG-1127', 'ANG-1150', 'ANG-1103', 'ANG-1131', 'ANG-1137', 'ANG-1132', 'ANG-1151', 'ANG-1190', 'ANG-1162', 'ANG-1165', 'ANG-1139', 'ANG-1126', 'ANG-1135', 'ANG-1109', 'ANG-1167', 'ANG-1146', 'ANG-1149', 'ANG-1115', 'ANG-1108', 'ANG-1169', 'ANG-1179', 'ANG-1116', 'ANG-1124']
EXPECTED_CONFIRMED=[2524, 2525, 2535, 2536, 2539, 2546, 2547, 2549, 2550, 2552, 2553, 2556, 2557, 2561, 2563, 2564, 2565, 2569, 2570, 2571, 2577]
EXPECTED_GRADES={"A":49,"B":11}

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rb=(E/"W3_BATCH_0043_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0043_RESEARCH.tsv").read_bytes()
    assert hashlib.sha256(rb).hexdigest()==EXPECTED_RESULTS_SHA256
    assert hashlib.sha256(qb).hexdigest()==EXPECTED_RESEARCH_SHA256
    results=list(csv.DictReader(rb.decode("utf-8-sig").splitlines()))
    research=list(csv.DictReader(qb.decode("utf-8-sig").splitlines(),delimiter="\t"))
    expected=list(range(START,END+1))
    assert len(queue)==len(results)==len(research)==60
    assert [int(r["queue_order"]) for r in queue]==expected
    assert [int(r["queue_order"]) for r in results]==expected
    assert [int(r["queue_order"]) for r in research]==expected
    assert [r["person_id"] for r in queue]==EXPECTED_PERSON_IDS
    assert [r["person_id"] for r in results]==EXPECTED_PERSON_IDS
    assert [r["name_normalized"] for r in queue]==EXPECTED_NAMES
    assert [r["name_normalized"] for r in research]==EXPECTED_NAMES
    assert [r["ambiguity_group_id"] for r in queue]==EXPECTED_AMBIGUITY_GROUP_IDS
    assert [r["ambiguity_group_id"] for r in research]==EXPECTED_AMBIGUITY_GROUP_IDS
    assert {r["priority"] for r in queue}=={"P1_IDENTITY"}
    assert Counter(r["province"] for r in queue)==Counter({"广东":25,"海南":35})
    assert [int(r["queue_order"]) for r in results if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED"]==EXPECTED_CONFIRMED
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":39,"CURRENT_ORG_TITLE_CONFIRMED":21})
    assert Counter(r["evidence_grade"] for r in results)==Counter(EXPECTED_GRADES)
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":39,"CONFIRMED":21})
    assert all(r["identity_anchor_url"].startswith("https://www.acfic.org.cn/") for r in research)
    assert sum(r["mode"]=="FRESH_RESEARCH" for r in research)==35
    assert sum(r["mode"].startswith("REUSE_") for r in research)==25
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
        assert expected_start==2581
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0043"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0043_RESULTS.csv"
        assert int(last["queue_start"])==2521 and int(last["queue_end"])==2580
    print("PASS W3-BATCH-0043 rows=60 confirmed=21 unresolved=39 grades=A49/B11 logical_end=2580")

if __name__=="__main__":
    main()
