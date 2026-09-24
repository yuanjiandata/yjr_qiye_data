#!/usr/bin/env python3
"""Deterministic validator for FC-EXEC-2515 W3-BATCH-0071."""
import csv, gzip, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
E=ROOT/"projects"/"fc-exec-2515"/"evidence"
START,END=4201,4260
EXPECTED_RESULTS_SHA256="3612ba4015a14f0ab00778801af524b955f163c0fab6d85ec260687ecaf4e1a7"
EXPECTED_RESEARCH_SHA256="116646b596e24e3722ea31e47250fa5fdf870bd63c107e69f1d22bfead6d7130"
GX_ANCHOR="https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_gx/202309/t20230914_316460.html"
NX_ANCHOR="https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_nx/202207/t20220719_102110.html"
SOURCE_MAP={4201: ('W3-BATCH-0068', 4122), 4202: ('W3-BATCH-0069', 4091), 4203: ('W3-BATCH-0069', 4134), 4204: ('W3-BATCH-0069', 4123), 4205: ('W3-BATCH-0069', 4112), 4206: ('W3-BATCH-0069', 4124), 4207: ('W3-BATCH-0069', 4135), 4208: ('W3-BATCH-0069', 4100), 4209: ('W3-BATCH-0069', 4087), 4210: ('W3-BATCH-0069', 4092), 4211: ('W3-BATCH-0069', 4136), 4212: ('W3-BATCH-0069', 4097), 4213: ('W3-BATCH-0069', 4125), 4214: ('W3-BATCH-0069', 4106), 4215: ('W3-BATCH-0069', 4098), 4216: ('W3-BATCH-0068', 4080), 4217: ('W3-BATCH-0069', 4126), 4218: ('W3-BATCH-0069', 4088), 4219: ('W3-BATCH-0069', 4127), 4220: ('W3-BATCH-0070', 4152), 4221: ('W3-BATCH-0070', 4153), 4222: ('W3-BATCH-0069', 4103), 4223: ('W3-BATCH-0068', 4072), 4224: ('W3-BATCH-0070', 4144), 4225: ('W3-BATCH-0069', 4085), 4226: ('W3-BATCH-0069', 4082), 4227: ('W3-BATCH-0069', 4137), 4228: ('W3-BATCH-0069', 4138), 4229: ('W3-BATCH-0070', 4154), 4230: ('W3-BATCH-0069', 4104), 4231: ('W3-BATCH-0069', 4093), 4232: ('W3-BATCH-0069', 4101), 4233: ('W3-BATCH-0069', 4139), 4234: ('W3-BATCH-0069', 4105), 4235: ('W3-BATCH-0069', 4081), 4236: ('W3-BATCH-0068', 4073), 4237: ('W3-BATCH-0069', 4140), 4238: ('W3-BATCH-0069', 4108), 4239: ('W3-BATCH-0069', 4090)}
GX_CONFIRMED={4202: ('梧州市工商业联合会', '主席', 'B', 'https://www.chinanews.com/gn/2026/02-04/10565925.shtml'), 4203: ('深圳市锦绣前程人才服务集团有限公司', '董事长', 'B', 'https://www.chinanews.com/cj/2026/03-09/10583901.shtml'), 4205: ('崇左市工商业联合会', '党组书记', 'B', 'https://finance.sina.com.cn/wm/2026-05-23/doc-inhywcxs5487324.shtml'), 4209: ('柳州市工商业联合会', '主席', 'A', 'https://www.lztz.gov.cn/gzsx/202604/t20260427_3745336.html'), 4211: ('广西扬翔集团股份有限公司', '董事长', 'B', 'https://gx.people.com.cn/n2/2026/0202/c179464-41490892.html'), 4218: ('柳州市工商业联合会', '党组书记', 'A', 'https://lztz.gov.cn/gzsx/202607/t20260715_3773529.html'), 4222: ('百色市工商业联合会', '主席', 'B', 'https://www.sohu.com/a/996544127_121106875'), 4223: ('广西壮族自治区工商业联合会', '主席', 'A', 'https://www.acfic.org.cn/gdgslgz/gx/bjgslgz/202601/t20260114_323788.html'), 4236: ('广西壮族自治区工商业联合会', '党组成员、副主席', 'A', 'https://wap.acfic.org.cn/gdgslgz_14277/202605/t20260526_326371.html')}
GX_GENERIC='OFFICIAL_2023_GUANGXI_IDENTITY_ANCHOR_BUT_NO_SUFFICIENT_CURRENT_2026_BRIDGED_ORG_TITLE_EVIDENCE'
GX_SPECIAL={4210: 'CURRENT_2026_WUZHOU_TRADE_UNION_ROLE_HIT_WITHOUT_SAFE_SOURCE_PERSON_IDENTITY_BRIDGE', 4213: 'CURRENT_2026_SAME_NAME_HITS_WITHOUT_SAFE_SOURCE_PERSON_IDENTITY_BRIDGE', 4230: 'CURRENT_2026_BAISE_MARKET_REGULATOR_ROLE_HIT_WITHOUT_SAFE_SOURCE_PERSON_IDENTITY_BRIDGE'}
NX_CONFIRMED={4245: ('宁夏宝丰集团有限公司', '董事长', 'B', 'https://finance.sina.com.cn/hy/hyjz/2026-06-24/doc-inienicz8353295.shtml'), 4247: ('百瑞源枸杞股份有限公司', '董事长', 'B', 'https://www.sohu.com/a/1015558543_121959073'), 4248: ('石嘴山银行股份有限公司', '党委书记、董事长', 'A', 'https://www.szsccb.com/szsccb/2026-02/04/article_2026020414553391780.html'), 4252: ('宁夏麦尔乐食品股份有限公司', '董事长', 'A', 'https://www.fujian.gov.cn/xwdt/fjyw/202608/t20260829_7206379.htm'), 4256: ('智慧宫国际文化传播集团有限公司', '董事长', 'A', 'https://www.swu.edu.cn/info/1197/28158.htm'), 4259: ('宁夏厚生记食品有限公司', '董事长', 'B', 'https://www.sohu.com/a/1015558543_121959073'), 4260: ('宁夏骏华月牙湖农牧科技股份有限公司', '董事长、总经理兼信息披露事务负责人', 'A', 'https://www.csrc.gov.cn/ningxia/c104434/c7649173/content.shtml')}
NX_NO_CURRENT={4240: ("A","https://news.sina.com.cn/c/2025-10-02/doc-infsnqmq6293749.shtml")}
NX_REASONS={4241: 'CURRENT_2026_GSL_PARTY_SECRETARY_CHANGED_AND_NO_SAFE_CURRENT_ROLE_FOUND_FOR_SOURCE_PERSON', 4242: 'OFFICIAL_2022_NINGXIA_IDENTITY_ANCHOR_BUT_NO_SUFFICIENT_CURRENT_2026_BRIDGED_ORG_TITLE_EVIDENCE', 4243: 'OFFICIAL_2022_NINGXIA_IDENTITY_ANCHOR_BUT_NO_SUFFICIENT_CURRENT_2026_BRIDGED_ORG_TITLE_EVIDENCE', 4244: 'CURRENT_2026_ZHONGWEI_VICE_MAYOR_SAME_NAME_HIT_WITHOUT_SAFE_SOURCE_PERSON_IDENTITY_BRIDGE', 4246: 'OLDER_WUZHONG_INSTRUMENT_ROLE_EVIDENCE_FOUND_BUT_NO_SUFFICIENT_CURRENT_2026_CONFIRMATION', 4249: 'OLDER_IPO_ROLE_EVIDENCE_FOUND_BUT_NO_SUFFICIENT_CURRENT_2026_CONFIRMATION', 4250: 'CURRENT_2025_COMPANY_CHAIRMAN_EVIDENCE_FOUND_BUT_NO_SUFFICIENT_CURRENT_2026_CONFIRMATION', 4251: 'OFFICIAL_2022_NINGXIA_IDENTITY_ANCHOR_BUT_NO_SUFFICIENT_CURRENT_2026_BRIDGED_ORG_TITLE_EVIDENCE', 4253: 'CURRENT_2026_COMPANY_LEGAL_REPRESENTATIVE_EVIDENCE_FOUND_BUT_CURRENT_CHAIRMAN_TITLE_NOT_ESTABLISHED', 4254: 'CURRENT_2026_COMPANY_LEGAL_REPRESENTATIVE_CONTEXT_FOUND_BUT_CURRENT_CHAIRMAN_TITLE_NOT_ESTABLISHED', 4255: 'CURRENT_COMPANY_IDENTITY_CONTEXT_FOUND_BUT_NO_SUFFICIENT_CURRENT_2026_TITLE_EVIDENCE', 4257: 'CURRENT_2026_NINGXIA_ENTREPRENEURS_ASSOCIATION_ROLE_HIT_WITHOUT_SAFE_SOURCE_PERSON_IDENTITY_BRIDGE', 4258: 'OFFICIAL_2022_NINGXIA_IDENTITY_ANCHOR_BUT_NO_SUFFICIENT_CURRENT_2026_BRIDGED_ORG_TITLE_EVIDENCE'}
OUTCOME_FIELDS=("current_organization","current_title","current_verification_status","evidence_grade","evidence_url","unresolved_reason")

def main():
    with gzip.open(E/"W2_UNRESOLVED_QUEUE.csv.gz","rt",encoding="utf-8-sig",newline="") as f:
        all_queue=list(csv.DictReader(f))
    queue=all_queue[START-1:END]
    rb=(E/"W3_BATCH_0071_RESULTS.csv").read_bytes()
    qb=(E/"W3_BATCH_0071_RESEARCH.tsv.gz").read_bytes()
    assert hashlib.sha256(rb).hexdigest()==EXPECTED_RESULTS_SHA256
    assert hashlib.sha256(qb).hexdigest()==EXPECTED_RESEARCH_SHA256
    results=list(csv.DictReader(rb.decode("utf-8").splitlines()))
    research=list(csv.DictReader(gzip.decompress(qb).decode("utf-8").splitlines(),delimiter="\t"))
    expected=list(range(START,END+1))
    assert len(queue)==len(results)==len(research)==60
    assert [int(r["queue_order"]) for r in queue]==expected
    assert [int(r["queue_order"]) for r in results]==expected
    assert [int(r["queue_order"]) for r in research]==expected
    assert [r["person_id"] for r in results]==[r["person_id"] for r in queue]
    assert [r["person_id"] for r in research]==[r["person_id"] for r in queue]
    assert [r["name_normalized"] for r in research]==[r["name_normalized"] for r in queue]
    assert [r["ambiguity_group_id"] for r in research]==[r["ambiguity_group_id"] for r in queue]
    assert [r["province"] for r in results]==[r["province"] for r in queue]
    assert [int(r["excel_row"]) for r in results]==[int(r["excel_row"]) for r in queue]
    assert {r["priority"] for r in queue}=={"P1_IDENTITY"}
    assert Counter(r["province"] for r in queue)==Counter({"广西":39,"宁夏":21})
    assert Counter(r["current_verification_status"] for r in results)==Counter({"UNRESOLVED_CURRENT_ORG_TITLE":43,"CURRENT_ORG_TITLE_CONFIRMED":16,"NO_CURRENT_ROLE_CONFIRMED":1})
    assert Counter(r["evidence_grade"] for r in results)==Counter({"A":52,"B":8})
    assert Counter(r["decision"] for r in research)==Counter({"UNRESOLVED":43,"CONFIRMED":16,"NO_CURRENT_ROLE_CONFIRMED":1})
    assert Counter(r["mode"] for r in research)==Counter({"FRESH_WEB_RESEARCH":21,"REUSE_SEALED_UNRESOLVED":30,"REUSE_SEALED_CONFIRMED":9})
    result_map={int(r["queue_order"]):r for r in results}
    for q,res,rr in zip(queue,results,research):
        qo=int(q["queue_order"])
        assert "NAME_ONLY" not in res["identity_resolution"]
        if qo <= 4239:
            assert qo in SOURCE_MAP
            gate,sq=SOURCE_MAP[qo]
            assert rr["identity_anchor_url"]==GX_ANCHOR
            assert rr["source_gate"]==gate and int(rr["source_queue_order"])==sq
            assert not rr["search_query"]
            source_q=all_queue[sq-1]
            assert source_q["province"]==q["province"]=="广西"
            assert source_q["name_normalized"]==q["name_normalized"]
            assert source_q["ambiguity_group_id"]==q["ambiguity_group_id"]
            if qo in GX_CONFIRMED:
                org,title,grade,url=GX_CONFIRMED[qo]
                assert (res["current_organization"],res["current_title"],res["current_verification_status"],res["evidence_grade"],res["evidence_url"],res["unresolved_reason"]) == (org,title,"CURRENT_ORG_TITLE_CONFIRMED",grade,url,"")
                assert rr["mode"]=="REUSE_SEALED_CONFIRMED" and rr["decision"]=="CONFIRMED"
            else:
                reason=GX_SPECIAL.get(qo,GX_GENERIC)
                assert (res["current_organization"],res["current_title"],res["current_verification_status"],res["evidence_grade"],res["evidence_url"],res["unresolved_reason"]) == ("","","UNRESOLVED_CURRENT_ORG_TITLE","A","",reason)
                assert rr["mode"]=="REUSE_SEALED_UNRESOLVED" and rr["decision"]=="UNRESOLVED"
        else:
            assert rr["identity_anchor_url"]==NX_ANCHOR
            assert rr["mode"]=="FRESH_WEB_RESEARCH"
            assert not rr["source_gate"] and not rr["source_queue_order"] and rr["search_query"]
            if qo in NX_CONFIRMED:
                org,title,grade,url=NX_CONFIRMED[qo]
                assert (res["current_organization"],res["current_title"],res["current_verification_status"],res["evidence_grade"],res["evidence_url"],res["unresolved_reason"]) == (org,title,"CURRENT_ORG_TITLE_CONFIRMED",grade,url,"")
                assert rr["decision"]=="CONFIRMED" and rr["evidence_url"]==url
            elif qo in NX_NO_CURRENT:
                grade,url=NX_NO_CURRENT[qo]
                assert (res["current_organization"],res["current_title"],res["current_verification_status"],res["evidence_grade"],res["evidence_url"],res["unresolved_reason"]) == ("","","NO_CURRENT_ROLE_CONFIRMED",grade,url,"")
                assert rr["decision"]=="NO_CURRENT_ROLE_CONFIRMED" and rr["evidence_url"]==url
            else:
                reason=NX_REASONS[qo]
                assert (res["current_organization"],res["current_title"],res["current_verification_status"],res["evidence_grade"],res["evidence_url"],res["unresolved_reason"]) == ("","","UNRESOLVED_CURRENT_ORG_TITLE","A","",reason)
                assert rr["decision"]=="UNRESOLVED"
        status=res["current_verification_status"]
        if status=="CURRENT_ORG_TITLE_CONFIRMED":
            assert res["current_organization"] and res["current_title"] and res["evidence_url"] and not res["unresolved_reason"]
        elif status=="NO_CURRENT_ROLE_CONFIRMED":
            assert not res["current_organization"] and not res["current_title"] and res["evidence_url"] and not res["unresolved_reason"]
        else:
            assert not res["current_organization"] and not res["current_title"] and not res["evidence_url"] and res["unresolved_reason"]
    idx=list(csv.DictReader((E/"W3_SEGMENT_INDEX.csv").open("r",encoding="utf-8-sig",newline="")))
    for kind in ("ledger","overlay"):
        entries=sorted((r for r in idx if r["kind"]==kind),key=lambda r:int(r["ordinal"]))
        expected_start=1
        for e in entries:
            start,end,count=map(int,(e["queue_start"],e["queue_end"],e["row_count"]))
            assert start==expected_start,(kind,expected_start,start)
            assert end-start+1==count
            expected_start=end+1
        assert expected_start==4261
        last=entries[-1]
        assert last["base_or_parent_gate"]=="W3-BATCH-0071"
        assert last["path"]=="projects/fc-exec-2515/evidence/W3_BATCH_0071_RESULTS.csv"
        assert int(last["queue_start"])==4201 and int(last["queue_end"])==4260
    print("PASS W3-BATCH-0071 rows=60 current=16 no_current=1 unresolved=43 grades=A52/B8/C0 logical_end=4260")

if __name__=="__main__":
    main()
