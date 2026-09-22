#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0040."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=2341,2400
EXPECTED_RESULTS_RAW_SHA256="861fdff4a7a64d2c9bdfbd1f7c2c536f7d306f0eef533edc4de8b11ebfa03ff4"
EXPECTED_RESULTS_GZIP_SHA256="4983821f11ca35a8d6d6d172b1289f3a31fadba28cb36a4dc990cfc77372cb27"
EXPECTED_RESEARCH_RAW_SHA256="1cd8916de29e543ee565415883bcd317f2fe495a7ffdf6fa9d8d27fc3c811272"
EXPECTED_RESEARCH_GZIP_SHA256="5603578e2f43b9a56967d66fa52db46bfc6106685b5562debc9fe729d62c0b5e"
EXPECTED_PERSON_IDS=['FC2515-P19-R0151', 'FC2515-P19-R0152', 'FC2515-P19-R0153', 'FC2515-P19-R0154', 'FC2515-P19-R0155', 'FC2515-P19-R0156', 'FC2515-P19-R0157', 'FC2515-P19-R0158', 'FC2515-P19-R0159', 'FC2515-P19-R0160', 'FC2515-P19-R0161', 'FC2515-P19-R0162', 'FC2515-P19-R0163', 'FC2515-P19-R0164', 'FC2515-P19-R0165', 'FC2515-P19-R0166', 'FC2515-P19-R0167', 'FC2515-P19-R0168', 'FC2515-P19-R0169', 'FC2515-P19-R0170', 'FC2515-P19-R0171', 'FC2515-P19-R0172', 'FC2515-P19-R0173', 'FC2515-P19-R0174', 'FC2515-P19-R0175', 'FC2515-P19-R0176', 'FC2515-P19-R0177', 'FC2515-P19-R0178', 'FC2515-P19-R0179', 'FC2515-P19-R0180', 'FC2515-P19-R0181', 'FC2515-P19-R0182', 'FC2515-P19-R0184', 'FC2515-P19-R0185', 'FC2515-P19-R0186', 'FC2515-P19-R0187', 'FC2515-P19-R0188', 'FC2515-P19-R0189', 'FC2515-P19-R0190', 'FC2515-P19-R0193', 'FC2515-P19-R0194', 'FC2515-P19-R0195', 'FC2515-P19-R0198', 'FC2515-P19-R0202', 'FC2515-P19-R0204', 'FC2515-P19-R0205', 'FC2515-P19-R0208', 'FC2515-P19-R0209', 'FC2515-P19-R0214', 'FC2515-P19-R0218', 'FC2515-P19-R0219', 'FC2515-P19-R0222', 'FC2515-P19-R0225', 'FC2515-P19-R0226', 'FC2515-P19-R0227', 'FC2515-P19-R0228', 'FC2515-P19-R0233', 'FC2515-P19-R0235', 'FC2515-P19-R0236', 'FC2515-P19-R0239']
EXPECTED_NAMES=['曹宇勇', '龚武', '崔夏宇', '梁志远', '彭林', '彭国远', '程悦', '曾建新', '赖志光', '蔡文贞', '蔡永忠', '潘康虎', '戴汝新', '马少福', '王诗增', '列海权', '刘晋嵩', '刘根森', '许凌', '吴芳华', '吴学明', '张莹', '张耀华', '陈丹丹', '周厚立', '郑林栋', '彭少衍', '廖伊曼', '霍启山', '戴进杰', '贺建东', '崔家荣', '殷民', '卢小周', '冯日光', '关向明', '李红', '张宏斌', '陈丽文', '王永辉', '王锐祥', '丘育华', '江南', '苏展航', '杜兰', '吴丹琳', '陈镇雄', '幸运', '胡德兆', '黄健慧', '梁耀铭', '谢萌', '薛华', '魏国华', '王岚', '王文银', '李勇', '励建炬', '吴宪', '张春华']
EXPECTED_CONFIRMED=[2349, 2355, 2364, 2365, 2375, 2376, 2377, 2379, 2391, 2394]
EXPECTED_FRESH=list(range(2341,2373))

def read_gz(path, delimiter=","):
    b=path.read_bytes()
    raw=gzip.decompress(b)
    rows=list(csv.DictReader(raw.decode("utf-8-sig").splitlines(),delimiter=delimiter))
    return b,raw,rows

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        queue=list(csv.DictReader(f))[START-1:END]
    rb,rr,results=read_gz(E/"W3_BATCH_0040_RESULTS.csv.gz")
    qb,qr,research=read_gz(E/"W3_BATCH_0040_RESEARCH.tsv.gz","\t")

    assert hashlib.sha256(rr).hexdigest()==EXPECTED_RESULTS_RAW_SHA256
    assert hashlib.sha256(rb).hexdigest()==EXPECTED_RESULTS_GZIP_SHA256
    assert hashlib.sha256(qr).hexdigest()==EXPECTED_RESEARCH_RAW_SHA256
    assert hashlib.sha256(qb).hexdigest()==EXPECTED_RESEARCH_GZIP_SHA256

    expected=list(range(START,END+1))
    assert len(queue)==len(results)==60
    assert [int(r["queue_order"]) for r in queue]==expected
    assert [int(r["queue_order"]) for r in results]==expected
    assert [r["person_id"] for r in queue]==EXPECTED_PERSON_IDS
    assert [r["person_id"] for r in results]==EXPECTED_PERSON_IDS
    assert [r["name_normalized"] for r in queue]==EXPECTED_NAMES
    assert [r["name_normalized"] for r in results]==EXPECTED_NAMES
    assert {r["priority"] for r in queue}=={"P1_IDENTITY"}
    assert Counter(r["province"] for r in queue)==Counter({"广东":60})
    assert all(r["identity_anchor_url"].startswith("https://www.acfic.org.cn/") for r in results)
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":50,"CURRENT_ORG_TITLE_CONFIRMED":10})
    assert [int(r["queue_order"]) for r in results if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED"]==EXPECTED_CONFIRMED
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":57,"B":3})
    reused=[r for r in results if r["identity_resolution"].startswith("REUSED_SEALED_EVIDENCE_")]
    fresh=[r for r in results if not r["identity_resolution"].startswith("REUSED_SEALED_EVIDENCE_")]
    assert len(reused)==28 and len(fresh)==32
    assert [int(r["queue_order"]) for r in fresh]==EXPECTED_FRESH
    assert len(research)==32
    assert [int(r["queue_order"]) for r in research]==EXPECTED_FRESH
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":28,"CONFIRMED":4})
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
        assert expected_start==2401
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0040"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0040_RESULTS.csv.gz"
        assert int(last["queue_start"])==2341 and int(last["queue_end"])==2400
    print("PASS W3-BATCH-0040 rows=60 confirmed=10 unresolved=50 grades=A57/B3 logical_end=2400")

if __name__=="__main__":
    main()
