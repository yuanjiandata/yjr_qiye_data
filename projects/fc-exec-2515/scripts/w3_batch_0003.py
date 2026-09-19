import csv, gzip
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evidence"
INPUT_HEAD = "97aa202d82f44096594d105d4cafe01068b7e094"
NOW = "2026-09-20T01:56:34+08:00"

with gzip.open(E / "W2_UNRESOLVED_QUEUE.csv.gz", "rt", encoding="utf-8-sig", newline="") as f:
    queue = list(csv.DictReader(f))[120:180]
assert [int(r["queue_order"]) for r in queue] == list(range(121, 181))
assert all(r["priority"] == "P1_IDENTITY" for r in queue)

HE = ("federation_official", "A", "河北省工商业联合会(总商会)第十三届执委会名单",
      "https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_he/202207/t20220715_312762.html", "2022-07-15")
CQ = ("federation_official", "A", "重庆市工商业联合会（总商会）第六届执委会名单",
      "https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_cq/202207/t20220715_312763.html", "2022-07-15")

# q: resolution, type, grade, evidence title, url, date, org, title, note
C = {
121:("CROSS_ROLE_IDENTITY_SUPPORTED","government_official","A","南川区民营经济代表人士热议民营企业座谈会","https://www.cqtzb.gov.cn/web/article/1415775604187615232/web/content_1415775604187615232.html","2025-03-03","重庆南商投资（集团）有限公司","董事长","Same Chongqing federation member is explicitly tied to the enterprise role by Chongqing United Front source."),
124:("CURRENT_PUBLIC_ROLE_IDENTIFIED","federation_official","A","2026年度全国“百城千校万企促就业”行动在石启动","https://wap.acfic.org.cn/qlyw_13743/202603/t20260329_325280.html","2026-03-29","河北省工商业联合会","主席","Current provincial federation role confirmed by ACFIC."),
125:("CURRENT_PUBLIC_ROLE_IDENTIFIED","government_official","A","省工商联深入学习贯彻习近平总书记在雄安新区考察时的重要讲话精神 发挥桥梁纽带作用 营造更优市场环境","https://www.hbtzb.gov.cn/system/2026/03/30/030379294.shtml","2026-03-30","河北省工商业联合会","党组书记、常务副主席","Current provincial federation role confirmed by Hebei United Front."),
126:("CURRENT_PUBLIC_ROLE_IDENTIFIED","government_official","A","保定市工商联召开第十八次代表大会","https://www.baoding.gov.cn/content-173-538815.html","2026-03-26","河北省工商业联合会","一级巡视员","Current provincial federation role confirmed by Baoding government source."),
127:("CURRENT_PUBLIC_ROLE_IDENTIFIED","federation_official","A","河北：2025年省工商联工作会议在石家庄召开","https://www.acfic.org.cn/gdgslgz/hb/bjgslgz/202503/t20250307_252646.html","2025-03-07","河北省工商业联合会","副主席","Current provincial federation role confirmed by ACFIC."),128:("CURRENT_PUBLIC_ROLE_IDENTIFIED","government_official","A","雄安新区总商会高质量发展大会圆满召开","https://www.xiongan.gov.cn/20260122/60b24034dae34f7e89df3f3d274a13f7/c.html","2026-01-22","河北省工商业联合会","党组成员、副主席","Current provincial federation role confirmed by China Xiong'an government source."),
130:("CROSS_SOURCE_IDENTITY_BY_FEDERATION_CONTEXT","federation_official","A","河北：民营经济人士理想信念报告会举办","https://wap.acfic.org.cn/gdgslgz_14277/202509/t20250915_321374.html","2025-09-15","石家庄以岭药业股份有限公司","董事长","ACFIC Hebei federation event identifies 吴相君 as the enterprise chairman; province and federation context disambiguate the roster member."),
132:("CURRENT_ENTERPRISE_ROLE_IDENTIFIED","federation_official","A","河北省工商联聚焦提振发展信心、推动政策落实听取企业家意见建议","https://www.acfic.org.cn/ztzlhz/myqyzth2025/myqyzth2025_xxgc/202502/t20250228_313701.html","2025-02-28","河北叁陆伍网络科技集团有限公司","董事长","ACFIC explicitly identifies 于树中 as 河北省工商联副主席 and enterprise chairman."),
135:("CURRENT_ENTERPRISE_ROLE_IDENTIFIED","authoritative_media","B","冀南钢铁集团董事长王树华，参加全国民营经济人士形势政策座谈会","https://finance.sina.com.cn/roll/2025-07-21/doc-infheqea8318974.shtml","2025-07-21","冀南钢铁集团有限公司","党委书记、董事长","Authoritative media identifies the same 河北省工商联副主席 with current enterprise role."),
140:("CURRENT_ENTERPRISE_ROLE_IDENTIFIED","listed_company_filing","A","中红普林医疗用品股份有限公司2025年年度报告全文","https://disc.static.szse.cn/download/disc/disk03/finalpage/2026-04-27/8a9f5ea0-0d7d-458b-9a49-4ddc5cd8a54b.PDF","2026-04-27","中红普林医疗用品股份有限公司","董事长","Listed-company annual report explicitly states 桑树军 is 河北省工商联副主席 and has served as company chairman since 2012."),
141:("CURRENT_ENTERPRISE_ROLE_IDENTIFIED","authoritative_media","B","江苏神通的前世今生：韩力掌舵七年布局新兴赛道","https://www.sohu.com/a/1070086390_122014422","2026-08-31","江苏神通阀门股份有限公司","董事长","Fresh corporate-profile reporting identifies 韩力 as company chairman and 河北省工商联副主席."),
142:("CROSS_SOURCE_IDENTITY_BY_FEDERATION_CONTEXT","federation_official","A","河北：民营经济人士理想信念报告会举办","https://wap.acfic.org.cn/gdgslgz_14277/202509/t20250915_321374.html","2025-09-15","北京以东科技有限公司","董事长","ACFIC Hebei federation event identifies 孟宪明 as enterprise chairman; federation and province context disambiguate identity."),
143:("CURRENT_ENTERPRISE_ROLE_IDENTIFIED","enterprise_official","A","米亚林董事长受邀出席全国工商联和邮储银行举办的民营企业走进邮储活动","https://www.sunhola.cn/newsd-108471.html","2025-04-24","首衡集团","董事长","Enterprise official source explicitly identifies 米亚林 as 河北省工商联副主席 and group chairman."),
144:("CURRENT_ENTERPRISE_ROLE_IDENTIFIED","authoritative_media","B","倪海琼代表—— 创新实干推动产业升级","https://finance.eastmoney.com/a/202603083665262811.html","2026-03-08","河北奥润顺达窗业有限公司","总裁","Economic Daily reporting explicitly identifies 倪海琼 as 河北省工商联副主席 and company president."),
145:("CURRENT_ENTERPRISE_ROLE_IDENTIFIED","authoritative_media","B","AI中国 我代言丨詹国海：打造京津冀绿色石化统一监管服务圈","https://heb.hebccw.cn/system/2026/03/04/102158454.shtml","2026-03-04","河北鑫海控股集团有限公司","董事长","Hebei authoritative media explicitly identifies 詹国海 as 河北省工商联副主席 and group chairman."),
147:("CURRENT_ENTERPRISE_ROLE_IDENTIFIED","authoritative_media","B","养元饮品的前世今生：姚奎章掌舵近二十载打造双轮格局","https://m.sohu.com/a/1068091023_122014422","2026-08-27","河北养元智汇饮品股份有限公司","董事长","Fresh company-profile reporting identifies 姚奎章 as current chairman and 河北省工商联副主席."),
152:("CURRENT_ENTERPRISE_ROLE_IDENTIFIED","federation_official","A","河北省工商联聚焦提振发展信心、推动政策落实听取企业家意见建议","https://www.acfic.org.cn/ztzlhz/myqyzth2025/myqyzth2025_xxgc/202502/t20250228_313701.html","2025-02-28","石家庄四药有限公司","董事长","ACFIC explicitly identifies 苏学军 as 河北省总商会副会长 and enterprise chairman."),
169:("CURRENT_ENTERPRISE_ROLE_IDENTIFIED","government_official","A","河北3人获“优秀中国特色社会主义事业建设者”称号","https://gxt.hebei.gov.cn/hbgyhxxht/xwzx32/snxw40/2025073109151955704/index.html","2025-07-31","河北普阳钢铁有限公司","董事长","Hebei industry authority explicitly identifies 郭龙鑫 as 河北省总商会副会长 and company chairman."),
}

RESULT_FIELDS = ["queue_order","person_id","province","excel_row","source_fragment","federation_role","identity_resolution","candidate_names","repair_notes","evidence_type","evidence_grade","evidence_title","evidence_url","evidence_date","current_organization","current_title","current_verification_status","unresolved_reason"]
results=[]
for r in queue:
    q=int(r["queue_order"]); name=r["name_normalized"]
    out={"queue_order":str(q),"person_id":r["person_id"],"province":r["province"],"excel_row":r["excel_row"],
         "source_fragment":name,"federation_role":r["federation_role"],"candidate_names":name,
         "current_organization":"","current_title":"","unresolved_reason":""}
    if q in C:
        res,typ,grade,etitle,url,edate,org,title,note=C[q]
        out.update(identity_resolution=res,repair_notes=note,evidence_type=typ,evidence_grade=grade,
                   evidence_title=etitle,evidence_url=url,evidence_date=edate,current_organization=org,
                   current_title=title,current_verification_status="CURRENT_ORG_TITLE_CONFIRMED")
    else:
        typ,grade,etitle,url,edate = CQ if q in (122,123) else HE
        candidates=name
        resolution="IDENTITY_ONLY_OFFICIAL_ROSTER"
        reason="Official federation roster confirms this source identity/role, but no sufficiently current and specific A/B employer-title evidence was found in this batch; name-only matches were rejected."
        note="Identity retained from official federation roster; current employment intentionally left unresolved."
        if q==122:
            note="Cross-role Chongqing roster evidence supports 乔澍 identity; no current employer/title is safely attributable."
        if q==123:
            candidates="王敏（女）|王敏（MBA）（女）"; resolution="AMBIGUOUS_SAME_NAME_OFFICIAL_ROSTER"
            note="Chongqing official roster contains two distinct 王敏 entries; this source row lacks enough qualifier to safely attribute a current employer."
            reason="Same-name ambiguity remains between official-roster entries 王敏（女） and 王敏（MBA）（女）; current employment is not assigned by name alone."
        out.update(identity_resolution=resolution,candidate_names=candidates,repair_notes=note,evidence_type=typ,
                   evidence_grade=grade,evidence_title=etitle,evidence_url=url,evidence_date=edate,
                   current_verification_status="UNRESOLVED_CURRENT_ORG_TITLE",unresolved_reason=reason)
    results.append(out)

with open(E/"W3_BATCH_0003_RESULTS.csv","w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=RESULT_FIELDS,lineterminator="\n"); w.writeheader(); w.writerows(results)

LEDGER_FIELDS=["queue_order","person_id","province","excel_row","candidate_names","evidence_type","evidence_grade","evidence_title","evidence_url","evidence_date","current_verification_status","unresolved_reason"]
OVERLAY_FIELDS=["queue_order","person_id","province","excel_row","identity_resolution","candidate_names","current_organization","current_title","current_verification_status","evidence_grade","evidence_url","unresolved_reason"]

def append_rows(path, fields, rows):
    with open(path,"r",encoding="utf-8-sig",newline="") as f: old=list(csv.DictReader(f))
    last=int(old[-1]["queue_order"])
    if last==180: return
    assert last==120, (path,last)
    with open(path,"a",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore",lineterminator="\n")
        w.writerows(rows)

append_rows(E/"W3_EVIDENCE_LEDGER.csv", LEDGER_FIELDS, results)
append_rows(E/"W3_VERIFICATION_OVERLAY.csv", OVERLAY_FIELDS, results)

confirmed=sum(r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED" for r in results)
unresolved=60-confirmed
a_count=sum(r["evidence_grade"]=="A" for r in results)
b_count=sum(r["evidence_grade"]=="B" for r in results)
assert confirmed==18 and unresolved==42
assert a_count==55 and b_count==5
assert all(r["evidence_url"] and r["evidence_title"] for r in results)
assert all((r["current_organization"] and r["current_title"]) if r["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED" else bool(r["unresolved_reason"]) for r in results)

with open(E/"W3_EVIDENCE_LEDGER.csv","r",encoding="utf-8-sig",newline="") as f: led=list(csv.DictReader(f))
assert len(led)==180 and [int(x["queue_order"]) for x in led]==list(range(1,181))

metrics=f'''schema: fc2515-w3-batch-metrics-v1
project_id: FC-EXEC-2515-01
gate: W3-BATCH-0003
status: PASS
queue_range: [121, 180]
batch_rows: 60
p1_identity_rows: 60
evidence_backed_rows: 60
a_grade_rows: {a_count}
b_grade_rows: {b_count}
structural_deferred_rows: 0
current_org_title_confirmed_rows: {confirmed}
current_org_title_unresolved_rows: {unresolved}
unsupported_current_title_claims: 0
post_batch:
  processed_queue_rows: 180
  actionable_queue_remaining: 10464
  next_queue_order: 181
  p0_processed: 101
  p0_remaining: 0
  p1_processed: 79
  p1_remaining: 4252
next_gate: W3-BATCH-0004
'''
(E/"W3_BATCH_0003_METRICS.yaml").write_text(metrics,encoding="utf-8")

validation=f'''# W3-BATCH-0003 Validation

Result: **PASS**

- Deterministic queue slice: 121–180 exactly, 60 rows, all P1_IDENTITY.
- Every touched row has public evidence or an explicit unresolved-current-role reason.
- Evidence grades in batch: A={a_count}, B={b_count}; C=0.
- Current organization + title confirmed: {confirmed}/60.
- Current-role unresolved: {unresolved}/60; unresolved values remain blank rather than guessed.
- 重庆 李云强 cross-role identity reused prior government evidence; 乔澍 remains unresolved.
- 重庆 王敏 ambiguity is preserved because the official roster contains two distinct 王敏 entries.
- 河北 leadership identities are anchored to the ACFIC official XIII executive roster.
- Current enterprise assignments are written only where current evidence plus federation/province context disambiguates identity.
- Common-name 河北常委 rows 173–180 remain unresolved rather than name-matched to unrelated people.
- Cumulative W3 evidence ledger reconciles to 180 rows with queue_order 1..180 and no gaps.
- Unsupported current-title claims: 0.

Next deterministic gate: `W3-BATCH-0004`, starting queue_order 181.
'''
(E/"W3_BATCH_0003_VALIDATION.md").write_text(validation,encoding="utf-8")

status_path=ROOT/"STATUS.yaml"
s=status_path.read_text(encoding="utf-8")
assert "code: W3-BATCH-0003\n  phase: W3-EVIDENCE-ENRICH\n  status: READY" in s
s=s.replace("code: W3-BATCH-0002\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS","code: W3-BATCH-0003\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS",1)
s=s.replace("code: W3-BATCH-0003\n  phase: W3-EVIDENCE-ENRICH\n  status: READY","code: W3-BATCH-0004\n  phase: W3-EVIDENCE-ENRICH\n  status: READY",1)

repls={
"  batches_sealed: 2":"  batches_sealed: 3",
"  processed_queue_rows: 120":"  processed_queue_rows: 180",
"  next_queue_order: 121":"  next_queue_order: 181",
"  actionable_queue_remaining: 10524":"  actionable_queue_remaining: 10464",
"    processed: 19\n    remaining: 4312":"    processed: 79\n    remaining: 4252",
"  identity_evidence_rows: 120":"  identity_evidence_rows: 180",
"  current_org_title_confirmed_rows: 13":"  current_org_title_confirmed_rows: 31",
"  current_org_title_unresolved_rows: 6":"  current_org_title_unresolved_rows: 48",
}
for a,b in repls.items():
    assert a in s, a
    s=s.replace(a,b,1)
artifact_anchor="  w3_batch_0002_validation: projects/fc-exec-2515/evidence/W3_BATCH_0002_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv"
artifact_new="  w3_batch_0002_validation: projects/fc-exec-2515/evidence/W3_BATCH_0002_VALIDATION.md\n  w3_batch_0003_results: projects/fc-exec-2515/evidence/W3_BATCH_0003_RESULTS.csv\n  w3_batch_0003_metrics: projects/fc-exec-2515/evidence/W3_BATCH_0003_METRICS.yaml\n  w3_batch_0003_validation: projects/fc-exec-2515/evidence/W3_BATCH_0003_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv"
assert artifact_anchor in s
s=s.replace(artifact_anchor,artifact_new,1)
status_path.write_text(s,encoding="utf-8")

current_path=ROOT/"CURRENT.yaml"
c=current_path.read_text(encoding="utf-8")
assert "current_gate: W3-BATCH-0003" in c
c=c.replace("current_gate: W3-BATCH-0003","current_gate: W3-BATCH-0004",1)
c=c.replace("work_cursor: 120","work_cursor: 180",1)

crepls={
"verified_records: 13":"verified_records: 31",
"unresolved_records: 10631":"unresolved_records: 10613",
"last_evidence_at: '2026-09-20T00:46:56+08:00'":f"last_evidence_at: '{NOW}'",
"last_input_head: d658bd5c9a024595882b59490cdaa87337e7c8b8":f"last_input_head: {INPUT_HEAD}",
"  processed: 120":"  processed: 180",
"  actionable_remaining: 10524":"  actionable_remaining: 10464",
"  next_queue_order: 121":"  next_queue_order: 181",
"      processed: 19\n      remaining: 4312":"      processed: 79\n      remaining: 4252",
}
for a,b in crepls.items():
    assert a in c, a
    c=c.replace(a,b,1)
anchor="\nnotes:\n"
batch3=f'''\nw3_batch_0003:
  status: SEALED
  validation: PASS
  touched_rows: 60
  p1_identity_rows: 60
  evidence_backed_rows: 60
  a_grade_rows: {a_count}
  b_grade_rows: {b_count}
  current_org_title_confirmed_rows: {confirmed}
  current_org_title_unresolved_rows: {unresolved}
  unsupported_current_title_claims: 0
'''
assert anchor in c
c=c.replace(anchor,batch3+anchor,1)

note_anchor="  - Next deterministic queue order is 121.\n"
new_notes="""  - Next deterministic queue order is 121.
  - W3-BATCH-0003 processed queue orders 121-180 exactly, all P1 identity/current-role rows.
  - 18 rows received current organization/title confirmation; 42 remain explicitly unresolved where current evidence was insufficiently specific.
  - 河北 identities were anchored to the official ACFIC XIII executive roster; enterprise roles were only written with corroborating current evidence and federation/province context.
  - 重庆 王敏 remains ambiguous between two official-roster identities; no name-only employer assignment was made.
  - Next deterministic queue order is 181.
"""
assert note_anchor in c
c=c.replace(note_anchor,new_notes,1)
current_path.write_text(c,encoding="utf-8")

# Final deterministic state assertions.
assert "code: W3-BATCH-0004" in status_path.read_text(encoding="utf-8")
assert "current_gate: W3-BATCH-0004" in current_path.read_text(encoding="utf-8")
print({"gate":"W3-BATCH-0003","confirmed":confirmed,"unresolved":unresolved,"A":a_count,"B":b_count,"ledger_rows":len(led),"next":181})
