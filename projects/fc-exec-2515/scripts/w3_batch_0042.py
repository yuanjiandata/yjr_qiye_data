#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0042."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=2461,2520
EXPECTED_RESULTS_SHA256="47e6ed83f9d20100c483f81c05e570b2a8210a8311afe6e7e9e871bed363aa40"
EXPECTED_RESEARCH_SHA256="a75ab0bf2752643ef76d1c6f03c2162f94d9192680cf14581741f6e9083554fa"
EXPECTED_PERSON_IDS=['FC2515-P19-R0413', 'FC2515-P19-R0416', 'FC2515-P19-R0421', 'FC2515-P19-R0424', 'FC2515-P19-R0429', 'FC2515-P19-R0432', 'FC2515-P19-R0433', 'FC2515-P19-R0435', 'FC2515-P19-R0439', 'FC2515-P19-R0440', 'FC2515-P19-R0446', 'FC2515-P19-R0448', 'FC2515-P19-R0449', 'FC2515-P19-R0450', 'FC2515-P19-R0455', 'FC2515-P19-R0456', 'FC2515-P19-R0457', 'FC2515-P19-R0458', 'FC2515-P19-R0459', 'FC2515-P19-R0466', 'FC2515-P19-R0467', 'FC2515-P19-R0468', 'FC2515-P19-R0470', 'FC2515-P19-R0471', 'FC2515-P19-R0474', 'FC2515-P19-R0475', 'FC2515-P19-R0476', 'FC2515-P19-R0477', 'FC2515-P19-R0479', 'FC2515-P19-R0482', 'FC2515-P19-R0483', 'FC2515-P19-R0484', 'FC2515-P19-R0486', 'FC2515-P19-R0490', 'FC2515-P19-R0497', 'FC2515-P19-R0500', 'FC2515-P19-R0503', 'FC2515-P19-R0510', 'FC2515-P19-R0512', 'FC2515-P19-R0515', 'FC2515-P19-R0516', 'FC2515-P19-R0518', 'FC2515-P19-R0521', 'FC2515-P19-R0522', 'FC2515-P19-R0525', 'FC2515-P19-R0529', 'FC2515-P19-R0531', 'FC2515-P19-R0532', 'FC2515-P19-R0533', 'FC2515-P19-R0536', 'FC2515-P19-R0537', 'FC2515-P19-R0538', 'FC2515-P19-R0540', 'FC2515-P19-R0541', 'FC2515-P19-R0543', 'FC2515-P19-R0546', 'FC2515-P19-R0549', 'FC2515-P19-R0552', 'FC2515-P19-R0553', 'FC2515-P19-R0554']
EXPECTED_NAMES=['梁友尧', '孔令炬', '何小鹏', '蔡光辉', '梁智威', '蔡仲光', '潘开广', '李立勉', '陈素玉', '黄锋伟', '林少光', '郭清海', '黄敏', '彭康良', '黄立坚', '温志芬', '王庆安', '王理宗', '王福亮', '刘学伟', '刘骏立', '许珊', '许志鸿', '阮永刚', '麦德添', '李婧', '李志珍', '李苏华', '李继新', '杨璋胜', '吴木棠', '吴伟斌', '吴振鑫', '张炜', '陆荣政', '陈东平', '陈宏海', '陈满新', '林松泉', '林梅峰', '郁亮', '郑小振', '赵莉瑜', '胡刚锋', '姚永红', '黄沃', '黄仕坤', '黄志云', '黄国洪', '曹宇勇', '龚武', '崔夏宇', '梁志远', '彭林', '彭国远', '程悦', '曾建新', '赖志光', '蔡文贞', '蔡永忠']
EXPECTED_AMBIGUITY_GROUPS=['ANG-1011', 'ANG-0960', 'ANG-0931', 'ANG-1041', 'ANG-1013', 'ANG-1040', 'ANG-1021', 'ANG-0997', 'ANG-1079', 'ANG-1099', 'ANG-1006', 'ANG-1062', 'ANG-1095', 'ANG-0979', 'ANG-1097', 'ANG-1019', 'ANG-1023', 'ANG-1028', 'ANG-1029', 'ANG-0936', 'ANG-0941', 'ANG-1050', 'ANG-1049', 'ANG-1063', 'ANG-1089', 'ANG-0993', 'ANG-0995', 'ANG-1001', 'ANG-0999', 'ANG-1005', 'ANG-0953', 'ANG-0948', 'ANG-0952', 'ANG-0969', 'ANG-1064', 'ANG-1065', 'ANG-1072', 'ANG-1078', 'ANG-1007', 'ANG-1008', 'ANG-1057', 'ANG-1058', 'ANG-1056', 'ANG-1036', 'ANG-0959', 'ANG-1096', 'ANG-1090', 'ANG-1094', 'ANG-1093', 'ANG-0986', 'ANG-1100', 'ANG-0961', 'ANG-1012', 'ANG-0981', 'ANG-0977', 'ANG-1033', 'ANG-0987', 'ANG-1054', 'ANG-1042', 'ANG-1043']
EXPECTED_CONFIRMED=[2463, 2464, 2476, 2478, 2486, 2498, 2518]

def read_plain(path, delimiter=","):
    b=path.read_bytes()
    rows=list(csv.DictReader(b.decode("utf-8-sig").splitlines(),delimiter=delimiter))
    return b,rows

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rb,results=read_plain(E/"W3_BATCH_0042_RESULTS.csv")
    qb,research=read_plain(E/"W3_BATCH_0042_RESEARCH.tsv","\t")
    assert hashlib.sha256(rb).hexdigest()==EXPECTED_RESULTS_SHA256
    assert hashlib.sha256(qb).hexdigest()==EXPECTED_RESEARCH_SHA256
    expected=list(range(START,END+1))
    assert len(queue)==len(results)==len(research)==60
    assert [int(r["queue_order"]) for r in queue]==expected
    assert [int(r["queue_order"]) for r in results]==expected
    assert [int(r["queue_order"]) for r in research]==expected
    assert [r["person_id"] for r in queue]==EXPECTED_PERSON_IDS
    assert [r["person_id"] for r in results]==EXPECTED_PERSON_IDS
    assert [r["person_id"] for r in research]==EXPECTED_PERSON_IDS
    assert [r["name_normalized"] for r in queue]==EXPECTED_NAMES
    assert [r["name_normalized"] for r in research]==EXPECTED_NAMES
    assert [r["ambiguity_group_id"] for r in queue]==EXPECTED_AMBIGUITY_GROUPS
    assert [r["ambiguity_group_id"] for r in research]==EXPECTED_AMBIGUITY_GROUPS
    assert {r["priority"] for r in queue}=={"P1_IDENTITY"}
    assert Counter(r["province"] for r in queue)==Counter({"广东":60})
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":53,"CURRENT_ORG_TITLE_CONFIRMED":7})
    assert [int(r["queue_order"]) for r in results if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED"]==EXPECTED_CONFIRMED
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":58,"B":2})
    assert all(r["identity_resolution"].startswith("REUSED_SEALED_EVIDENCE_") for r in results)
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":53,"CONFIRMED":7})
    assert all(r["prior_sealed_gate"] and r["prior_sealed_queue"] for r in research)
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
        assert expected_start==2521
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0042"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0042_RESULTS.csv"
        assert int(last["queue_start"])==2461 and int(last["queue_end"])==2520
    print("PASS W3-BATCH-0042 rows=60 confirmed=7 unresolved=53 grades=A58/B2 logical_end=2520")

if __name__=="__main__":
    main()
