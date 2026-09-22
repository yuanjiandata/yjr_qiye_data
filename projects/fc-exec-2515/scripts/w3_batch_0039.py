#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0039."""
import csv, gzip, hashlib
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[3]
E = ROOT / "projects" / "fc-exec-2515" / "evidence"
START, END = 2281, 2340
EXPECTED_RESULTS_RAW_SHA256 = "987b23815619510381b6d888ff060e900866421200fe173e4bd3417d653614c3"
EXPECTED_RESULTS_GZIP_SHA256 = "7e924f98f2d176de3ab58e81f4e1fa078baaa31af73d8569d26b0e2018c2f5ff"
EXPECTED_RESEARCH_RAW_SHA256 = "6a8e385fae98641ceb7b3215884d4d5b413e2cf76970ed602eada6c750bff142"
EXPECTED_RESEARCH_GZIP_SHA256 = "b404fb0f6a5c81238b048f490e43f7c7e0445a3e4b169775baba1fad33fe23ac"
EXPECTED_NAMES = ['陈志胜', '陈宝家', '白宝鲲', '吴丰礼', '陈国良', '陈健民', '袁斌', '李维', '张瑞', '郭丛枢', '朱英杰', '李茜', '黄达昌', '曾锦俊', '张辉雄', '洪家虎', '陈宇', '陈弘祖', '陈宇驰', '支勇', '陈高文', '梁友尧', '孔令炬', '蔡光辉', '梁智威', '潘开广', '陈素玉', '黄锋伟', '林少光', '黄敏', '彭康良', '黄立坚', '王庆安', '王理宗', '刘学伟', '刘骏立', '许珊', '许志鸿', '阮永刚', '麦德添', '李婧', '李志珍', '李苏华', '李继新', '杨璋胜', '吴伟斌', '吴振鑫', '张炜', '陆荣政', '陈满新', '林松泉', '林梅峰', '郑小振', '赵莉瑜', '胡刚锋', '姚永红', '黄沃', '黄仕坤', '黄志云', '黄国洪']
EXPECTED_IDS = ['FC2515-P19-R0091', 'FC2515-P19-R0092', 'FC2515-P19-R0093', 'FC2515-P19-R0094', 'FC2515-P19-R0095', 'FC2515-P19-R0096', 'FC2515-P19-R0097', 'FC2515-P19-R0098', 'FC2515-P19-R0099', 'FC2515-P19-R0100', 'FC2515-P19-R0101', 'FC2515-P19-R0102', 'FC2515-P19-R0103', 'FC2515-P19-R0104', 'FC2515-P19-R0105', 'FC2515-P19-R0106', 'FC2515-P19-R0107', 'FC2515-P19-R0108', 'FC2515-P19-R0109', 'FC2515-P19-R0110', 'FC2515-P19-R0111', 'FC2515-P19-R0112', 'FC2515-P19-R0113', 'FC2515-P19-R0114', 'FC2515-P19-R0115', 'FC2515-P19-R0116', 'FC2515-P19-R0117', 'FC2515-P19-R0118', 'FC2515-P19-R0119', 'FC2515-P19-R0120', 'FC2515-P19-R0121', 'FC2515-P19-R0122', 'FC2515-P19-R0123', 'FC2515-P19-R0124', 'FC2515-P19-R0125', 'FC2515-P19-R0126', 'FC2515-P19-R0127', 'FC2515-P19-R0128', 'FC2515-P19-R0129', 'FC2515-P19-R0130', 'FC2515-P19-R0131', 'FC2515-P19-R0132', 'FC2515-P19-R0133', 'FC2515-P19-R0134', 'FC2515-P19-R0135', 'FC2515-P19-R0136', 'FC2515-P19-R0137', 'FC2515-P19-R0138', 'FC2515-P19-R0139', 'FC2515-P19-R0140', 'FC2515-P19-R0141', 'FC2515-P19-R0142', 'FC2515-P19-R0143', 'FC2515-P19-R0144', 'FC2515-P19-R0145', 'FC2515-P19-R0146', 'FC2515-P19-R0147', 'FC2515-P19-R0148', 'FC2515-P19-R0149', 'FC2515-P19-R0150']
EXPECTED_CONFIRMED = [2284, 2293, 2296, 2304, 2314, 2321, 2330]

def read_gz_csv(path, delimiter=","):
    b = path.read_bytes()
    raw = gzip.decompress(b)
    text = raw.decode("utf-8-sig")
    rows = list(csv.DictReader(text.splitlines(), delimiter=delimiter))
    return b, raw, rows

def main():
    rp = E / "W3_BATCH_0039_RESULTS.csv.gz"
    qp = E / "W3_BATCH_0039_RESEARCH.tsv.gz"
    rb, rr, rows = read_gz_csv(rp)
    qb, qr, research = read_gz_csv(qp, "\t")
    assert hashlib.sha256(rr).hexdigest() == EXPECTED_RESULTS_RAW_SHA256
    assert hashlib.sha256(rb).hexdigest() == EXPECTED_RESULTS_GZIP_SHA256
    assert hashlib.sha256(qr).hexdigest() == EXPECTED_RESEARCH_RAW_SHA256
    assert hashlib.sha256(qb).hexdigest() == EXPECTED_RESEARCH_GZIP_SHA256
    assert len(rows) == 60
    assert [int(r["queue_order"]) for r in rows] == list(range(START, END+1))
    assert [r["person_id"] for r in rows] == EXPECTED_IDS
    assert [r["name_normalized"] for r in rows] == EXPECTED_NAMES
    assert all(r["province"] == "广东" and r["federation_role"] == "常委" for r in rows)
    assert all(r["identity_anchor_url"].startswith("https://www.acfic.org.cn/") for r in rows)
    confirmed = [int(r["queue_order"]) for r in rows if r["current_verification_status"] == "CURRENT_ORG_TITLE_CONFIRMED"]
    unresolved = [r for r in rows if r["current_verification_status"] == "UNRESOLVED_CURRENT_ORG_TITLE"]
    assert confirmed == EXPECTED_CONFIRMED
    assert len(unresolved) == 53
    assert all(r["current_organization"] and r["current_title"] and r["evidence_url"] for r in rows if r["current_verification_status"] == "CURRENT_ORG_TITLE_CONFIRMED")
    assert all(not r["current_organization"] and not r["current_title"] and r["unresolved_reason"] for r in unresolved)
    assert Counter(r["evidence_grade"] for r in rows) == Counter({"A":57,"B":3})
    assert len(research) == 60
    assert [int(r["queue_order"]) for r in research] == list(range(START, END+1))
    assert Counter(r["decision"] for r in research) == Counter({"CONFIRMED":7,"UNRESOLVED":53})
    assert all(r["web_query"] and r["identity_anchor_url"] and r["research_note"] for r in research)

    # Metadata-continuity check: prior prefix was SEALED/PASS through 2280; this index
    # must append exactly one 2281-2340 segment for each logical projection.
    idx = list(csv.DictReader((E / "W3_SEGMENT_INDEX.csv").open("r", encoding="utf-8-sig", newline="")))
    for kind in ("ledger","overlay"):
        entries = sorted((r for r in idx if r["kind"] == kind), key=lambda r:int(r["ordinal"]))
        expected = 1
        for e in entries:
            start,end,count=map(int,(e["queue_start"],e["queue_end"],e["row_count"]))
            assert start == expected, (kind, expected, start)
            assert end-start+1 == count
            expected = end+1
        assert expected == 2341
        last = entries[-1]
        assert last["base_or_parent_gate"] == "W3-BATCH-0039"
        assert last["path"] == "projects/fc-exec-2515/evidence/W3_BATCH_0039_RESULTS.csv.gz"
        assert int(last["queue_start"]) == 2281 and int(last["queue_end"]) == 2340
    print("PASS W3-BATCH-0039 rows=60 confirmed=7 unresolved=53 grades=A57/B3 logical_end=2340")

if __name__ == "__main__":
    main()
