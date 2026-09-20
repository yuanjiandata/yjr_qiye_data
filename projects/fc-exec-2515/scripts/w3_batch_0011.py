import csv, gzip
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evidence"
INPUT_HEAD = "981f994de8aee7729ce0e801bff2ce009cd3903c"
NOW = datetime.now(timezone(timedelta(hours=8))).replace(microsecond=0).isoformat()

with gzip.open(E / "W2_UNRESOLVED_QUEUE.csv.gz", "rt", encoding="utf-8-sig", newline="") as f:
    queue = list(csv.DictReader(f))[600:660]
assert len(queue) == 60
assert [int(r["queue_order"]) for r in queue] == list(range(601, 661))
assert all(r["province"] == "江苏" and r["priority"] == "P1_IDENTITY" for r in queue)

JS_STANDING_TITLE = "江苏省工商业联合会第十二届常务委员会组成人员名单（2026年9月，共计120人）"
JS_STANDING_URL = "https://www.jssh.org.cn/zzjg/fzxfhz/"
JS_EXEC_TITLE = "江苏省工商业联合会第十二届执行委员会委员名单（2026年7月，共计338名）"
JS_EXEC_URL = "https://www.jssh.org.cn/zzjg/czwmd/"

FED_VICE = {"李晓林", "肖伟", "吴卫东", "吴培服", "沈彬", "陈建华", "周江", "周立成", "周海江", "昝圣达"}
CHAMBER_VICE = {"孙力斌", "李晓冬", "李海斌", "吴毅", "张丽", "陈惠", "邵丹薇", "周荣", "周立宸", "单建华", "宫长义"}
STANDING = {
    "许岗", "李焕军", "李瑞华", "杨永岗", "吴强", "吴芸", "吴亚军", "吴志祥", "吴建发", "何海平",
    "张相阳", "张家炯", "张斯纬", "张黎明", "陆云芳", "陆永华", "陆建新", "陈扬", "陈锦鹏", "林雅杰",
    "周俊", "郑红卫", "赵峰", "郦海星", "俞雷", "姜道志"
}
DIRECT_NAMES = FED_VICE | CHAMBER_VICE | STANDING
assert len(DIRECT_NAMES) == 47

SPECIAL = {
    605: dict(
        name="李兰翔", org="盐城市人民政府", title="副市长", etype="government_official",
        etitle="市政协九届六十七次主席会议召开", url="https://wap.yancheng.gov.cn/art/2026/9/4/art_49_4451545.html", date="2026-09-04",
        bridge="https://www.acfic.org.cn/gdgslgz/js/bjgslgz/202304/t20230426_280633.html",
        note="ACFIC role-history evidence anchors 李兰翔 in the Jiangsu federation source identity; Sep-2026 Yancheng government evidence identifies the same person as 副市长. The stale federation role is not carried forward."
    ),
    606: dict(
        name="李厚林", org="扬州市政协", title="经济科技委员会主任", etype="government_official",
        etitle="企业敢说话 部门真回应——江苏扬州市政协‘扬企有话讲’政企协商平台汇众智解难题",
        url="https://www.cppcc.gov.cn/zxww/2026/04/20/ARTI1776648774943124.shtml", date="2026-04-20",
        bridge="https://www.jstz.gov.cn/a/20250317/1742175919732.shtml",
        note="Yangzhou United Front history anchors 李厚林 as the prior 市工商联党组书记; 2026 CPPCC evidence identifies him as 扬州市政协经济科技委员会主任. Role history, not name-only matching, closes identity."
    ),
    639: dict(
        name="陈湘珍", org="盐城市人民政府台湾事务办公室", title="主任", etype="government_official",
        etitle="盐城市台协会召开换届大会 赖元皇连任会长", url="https://www.jsstb.gov.cn/yancheng/202601/t20260108_12745165.htm", date="2026-01-08",
        bridge="https://www.jssh.org.cn/xwzx/yw/202311/t20231113_217297.html",
        note="Historical Jiangsu federation evidence anchors 陈湘珍 as 盐城市委统战部副部长、市工商联党组书记; 2026 Jiangsu Taiwan Affairs evidence identifies her as 盐城市台办主任. Province + role history closes identity."
    ),
    658: dict(
        name="施勇", org="中共淮安市委统战部 / 淮安市社会主义学院", title="常务副部长 / 院长", etype="government_official",
        etitle="民盟淮安市委会2026年度盟务工作会议召开", url="https://www.jstz.gov.cn/a/20260411/177639529943.shtml", date="2026-04-11",
        bridge="https://www.jstz.gov.cn/a/20240923/1727406256514.shtml",
        note="Historical Huai'an United Front evidence anchors the source person; Apr-2026 Jiangsu United Front evidence confirms 施勇 as 淮安市委统战部常务副部长、市社会主义学院院长. The former federation post is not carried forward."
    ),
}

NO_CURRENT = {
    655: dict(
        name="钟雨", etype="listed_company_filing", grade="A",
        etitle="江苏洋河酒厂股份有限公司公告编号2026-003：关于公司总裁退休离任暨聘任总裁的公告",
        url="https://static.cninfo.com.cn/finalpage/2026-01-24/1224948902.PDF", date="2026-01-24",
        bridge="https://www.jstz.gov.cn/a/20250910/1757484098614.shtml",
        note="2025 Jiangsu United Front evidence anchors 钟雨 to 洋河股份. The Jan-24-2026 CNINFO listed-company filing states he retired, resigned all company roles, and after resignation holds no other role in the company or controlled subsidiaries. No replacement employer/title is inferred."
    )
}

UNRESOLVED = {
    603: "孙振东 is absent from the current Jul-2026 Jiangsu executive roster and Sep-2026 standing-committee roster. Targeted fresh public search did not establish a present organization/title with province + federation/history linkage; name-only hits were rejected.",
    604: "李建 is absent from the current Jul-2026 Jiangsu executive roster and Sep-2026 standing-committee roster. The name is highly non-unique (including unrelated current federation figures outside Jiangsu); no safe Jiangsu source-identity bridge closes a present organization/title.",
    624: "Source row 364 is one of two exact-value duplicate candidates in repository group EDG-0001 (张飞/江苏/执委). The current Jul-2026 official roster distinguishes 张飞（淮） and 张飞（盐）, while the Sep-2026 standing roster includes only 张飞（淮）. Assigning either current identity to this person_id would be arbitrary, so the row remains unresolved.",
    625: "Source row 365 is one of two exact-value duplicate candidates in repository group EDG-0001 (张飞/江苏/执委). The current Jul-2026 official roster distinguishes 张飞（淮） and 张飞（盐）, while the Sep-2026 standing roster includes only 张飞（淮）. Assigning either current identity to this person_id would be arbitrary, so the row remains unresolved.",
    630: "张惠扬 is absent from the current Jul-2026 Jiangsu executive roster and Sep-2026 standing roster. Public evidence confirms the former 淮安市政协副主席/市工商联主席 role ended, but no sufficiently current authoritative evidence establishes a replacement present organization/title.",
    636: "陈军 is absent from the current Jiangsu federation rosters. 2026 public search returns multiple unrelated Jiangsu people with this common name (including finance and listed-company executives); none can be safely bridged to the source person from province + federation context, so no current role is assigned.",
    646: "周洁 is absent from the current Jul-2026 executive roster and Sep-2026 standing roster. Targeted current public search did not yield a present organization/title that can be linked with federation/history context rather than name alone.",
    653: "查艳 is absent from the current Jul-2026 executive roster and Sep-2026 standing roster. Older official material anchors her former 常州市委统战部副部长、市工商联党组书记 identity, but current public evidence found in this gate does not safely establish a present organization/title; membership in a 2026 local people's congress presidium is not treated as an employment title."
}
assert set(UNRESOLVED) == {603,604,624,625,630,636,646,653}

FIELDS=["queue_order","person_id","province","excel_row","source_fragment","federation_role","identity_resolution","candidate_names","repair_notes","evidence_type","evidence_grade","evidence_title","evidence_url","evidence_date","current_organization","current_title","current_verification_status","unresolved_reason"]
results=[]
for r in queue:
    q=int(r["queue_order"]); name=r["name_normalized"]
    out={"queue_order":str(q),"person_id":r["person_id"],"province":r["province"],"excel_row":r["excel_row"],"source_fragment":name,"federation_role":r["federation_role"],"candidate_names":name,"current_organization":"","current_title":"","unresolved_reason":""}
    if q in SPECIAL:
        x=SPECIAL[q]; assert name==x["name"]
        out.update(identity_resolution="CURRENT_ROLE_CONFIRMED_WITH_ROLE_HISTORY_BRIDGE",repair_notes=x["note"]+" Historical bridge: "+x["bridge"],evidence_type=x["etype"],evidence_grade="A",evidence_title=x["etitle"],evidence_url=x["url"],evidence_date=x["date"],current_organization=x["org"],current_title=x["title"],current_verification_status="CURRENT_ORG_TITLE_CONFIRMED")
    elif q in NO_CURRENT:
        x=NO_CURRENT[q]; assert name==x["name"]
        out.update(identity_resolution="CURRENT_EMPLOYMENT_TERMINATION_CONFIRMED_WITH_ROLE_HISTORY_BRIDGE",repair_notes=x["note"]+" Historical bridge: "+x["bridge"],evidence_type=x["etype"],evidence_grade=x["grade"],evidence_title=x["etitle"],evidence_url=x["url"],evidence_date=x["date"],current_verification_status="NO_CURRENT_ROLE_CONFIRMED")
    elif q in UNRESOLVED:
        out.update(identity_resolution="HISTORICAL_SOURCE_IDENTITY_CURRENT_ROLE_UNRESOLVED",repair_notes="Checked the current Jul-2026 Jiangsu executive roster, the current Sep-2026 standing roster, repository duplicate/ambiguity state, and targeted fresh public evidence. No name-only employer/title assignment was permitted.",evidence_type="federation_official",evidence_grade="A",evidence_title=JS_EXEC_TITLE,evidence_url=JS_EXEC_URL,evidence_date="2026-07",current_verification_status="UNRESOLVED_CURRENT_ORG_TITLE",unresolved_reason=UNRESOLVED[q])
    else:
        assert name in DIRECT_NAMES, (q,name)
        if name in FED_VICE:
            org,title="江苏省工商业联合会 / 江苏省总商会","副主席 / 副会长（兼）" if name in {"李晓林","吴卫东"} else "副主席"
        elif name in CHAMBER_VICE:
            org,title="江苏省总商会","副会长"
        else:
            org,title="江苏省工商业联合会","常务委员"
        out.update(identity_resolution="CURRENT_ROLE_CONFIRMED_BY_LATEST_OFFICIAL_PROVINCIAL_ROSTER",repair_notes="Name + 江苏 source scope + federation-role history reconcile to the official Sep-2026 standing-committee roster. A current higher federation/chamber role supersedes the stale source 执委 label; no name-only inference.",evidence_type="federation_official",evidence_grade="A",evidence_title=JS_STANDING_TITLE,evidence_url=JS_STANDING_URL,evidence_date="2026-09",current_organization=org,current_title=title,current_verification_status="CURRENT_ORG_TITLE_CONFIRMED")
    results.append(out)

assert len(results)==60 and [int(x["queue_order"]) for x in results]==list(range(601,661))
assert len({x["person_id"] for x in results})==60
assert all(x["evidence_url"] and x["evidence_title"] and x["evidence_grade"]=="A" for x in results)
assert all(x["unresolved_reason"] for x in results if x["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE")
assert all(x["current_organization"] and x["current_title"] for x in results if x["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED")
confirmed=sum(x["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED" for x in results)
no_role=sum(x["current_verification_status"]=="NO_CURRENT_ROLE_CONFIRMED" for x in results)
unresolved=sum(x["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE" for x in results)
assert (confirmed,no_role,unresolved)==(51,1,8)

with open(E/"W3_BATCH_0011_RESULTS.csv","w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator="\n"); w.writeheader(); w.writerows(results)
LEDGER_FIELDS=["queue_order","person_id","province","excel_row","candidate_names","evidence_type","evidence_grade","evidence_title","evidence_url","evidence_date","current_verification_status","unresolved_reason"]
OVERLAY_FIELDS=["queue_order","person_id","province","excel_row","identity_resolution","candidate_names","current_organization","current_title","current_verification_status","evidence_grade","evidence_url","unresolved_reason"]
def append_rows(path,fields):
    with open(path,"r",encoding="utf-8-sig",newline="") as f: old=list(csv.DictReader(f))
    last=int(old[-1]["queue_order"])
    if last==660: return
    assert last==600,(path,last)
    with open(path,"a",encoding="utf-8",newline="") as f: csv.DictWriter(f,fieldnames=fields,extrasaction="ignore",lineterminator="\n").writerows(results)
append_rows(E/"W3_EVIDENCE_LEDGER.csv",LEDGER_FIELDS)
append_rows(E/"W3_VERIFICATION_OVERLAY.csv",OVERLAY_FIELDS)
for p in [E/"W3_EVIDENCE_LEDGER.csv",E/"W3_VERIFICATION_OVERLAY.csv"]:
    with open(p,"r",encoding="utf-8-sig",newline="") as f: rr=list(csv.DictReader(f))
    assert len(rr)==660 and [int(x["queue_order"]) for x in rr]==list(range(1,661))
    assert len({int(x["queue_order"]) for x in rr})==660

(E/"W3_BATCH_0011_METRICS.yaml").write_text(f'''schema: fc2515-w3-batch-metrics-v1
project_id: FC-EXEC-2515-01
gate: W3-BATCH-0011
status: PASS
queue_range: [601, 660]
batch_rows: 60
p1_identity_rows: 60
evidence_backed_rows: 60
a_grade_rows: 60
b_grade_rows: 0
structural_deferred_rows: 0
current_org_title_confirmed_rows: {confirmed}
no_current_role_confirmed_rows: {no_role}
current_org_title_unresolved_rows: {unresolved}
unsupported_current_title_claims: 0
post_batch:
  processed_queue_rows: 660
  actionable_queue_remaining: 9984
  next_queue_order: 661
  p0_processed: 101
  p0_remaining: 0
  p1_processed: 559
  p1_remaining: 3772
next_gate: W3-BATCH-0012
''',encoding="utf-8")

(E/"W3_BATCH_0011_VALIDATION.md").write_text(f'''# W3-BATCH-0011 Validation

Result: **PASS**

- Deterministic queue slice: 601–660 exactly, 60 江苏 P1_IDENTITY rows.
- Every touched row has public evidence or an explicit unresolved-current-role reason; unsupported current-title claims: 0.
- 47 rows are closed from the live official Jiangsu standing-committee roster labeled `2026年9月，共计120人`, with higher current federation/chamber roles preferred over stale source `执委` labels.
- Four additional current roles are safely closed through role-history bridges: 李兰翔→盐城市副市长, 李厚林→扬州市政协经济科技委员会主任, 陈湘珍→盐城市台办主任, 施勇→淮安市委统战部常务副部长/市社会主义学院院长.
- 钟雨 is evidence-resolved as `NO_CURRENT_ROLE_CONFIRMED` using the original CNINFO listed-company filing (公告编号 2026-003), which records retirement and resignation from all 洋河股份/company-subsidiary roles.
- Eight rows remain explicit current-role unresolved: 孙振东、李建、张飞×2、张惠扬、陈军、周洁、查艳. The two 张飞 rows are repository exact-value duplicate candidates (EDG-0001); the current official roster distinguishes 淮/盐 identities, so person_id-level assignment would be arbitrary and is not made.
- Evidence grades: A=60, B=0, C=0; current organization/title confirmed={confirmed}/60; no-current-role confirmed={no_role}/60; unresolved={unresolved}/60.
- Cumulative evidence ledger and verification overlay each reconcile to 660 rows with queue_order 1..660, no gaps and no duplicate queue orders.

Next deterministic gate: `W3-BATCH-0012`, starting queue_order 661.
''',encoding="utf-8")

sp=ROOT/"STATUS.yaml"; s=sp.read_text(encoding="utf-8")
repls={
"code: W3-BATCH-0010\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS":"code: W3-BATCH-0011\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS",
"code: W3-BATCH-0011\n  phase: W3-EVIDENCE-ENRICH\n  status: READY":"code: W3-BATCH-0012\n  phase: W3-EVIDENCE-ENRICH\n  status: READY",
"  batches_sealed: 10":"  batches_sealed: 11",
"  processed_queue_rows: 600":"  processed_queue_rows: 660",
"  next_queue_order: 601":"  next_queue_order: 661",
"  actionable_queue_remaining: 10044":"  actionable_queue_remaining: 9984",
"    processed: 499\n    remaining: 3832":"    processed: 559\n    remaining: 3772",
"  identity_evidence_rows: 600":"  identity_evidence_rows: 660",
"  current_org_title_confirmed_rows: 316":"  current_org_title_confirmed_rows: 367",
"  current_org_title_unresolved_rows: 182":"  current_org_title_unresolved_rows: 190",
"  no_current_role_confirmed_rows: 1":"  no_current_role_confirmed_rows: 2"}
for a,b in repls.items(): assert a in s,a; s=s.replace(a,b,1)
anchor="  w3_batch_0010_validation: projects/fc-exec-2515/evidence/W3_BATCH_0010_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv"
rep="  w3_batch_0010_validation: projects/fc-exec-2515/evidence/W3_BATCH_0010_VALIDATION.md\n  w3_batch_0011_results: projects/fc-exec-2515/evidence/W3_BATCH_0011_RESULTS.csv\n  w3_batch_0011_metrics: projects/fc-exec-2515/evidence/W3_BATCH_0011_METRICS.yaml\n  w3_batch_0011_validation: projects/fc-exec-2515/evidence/W3_BATCH_0011_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv"
assert anchor in s; sp.write_text(s.replace(anchor,rep,1),encoding="utf-8")

cp=ROOT/"CURRENT.yaml"; c=cp.read_text(encoding="utf-8")
repls={
"current_gate: W3-BATCH-0011":"current_gate: W3-BATCH-0012",
"work_cursor: 600":"work_cursor: 660",
"verified_records: 317":"verified_records: 369",
"unresolved_records: 10327":"unresolved_records: 10275",
"last_input_head: 565a50b46904107791766d627ae21a8c0af433ae":f"last_input_head: {INPUT_HEAD}",
"  processed: 600":"  processed: 660",
"  actionable_remaining: 10044":"  actionable_remaining: 9984",
"  next_queue_order: 601":"  next_queue_order: 661",
"      processed: 499\n      remaining: 3832":"      processed: 559\n      remaining: 3772"}
for a,b in repls.items(): assert a in c,a; c=c.replace(a,b,1)
# replace dynamic evidence timestamp without relying on exact prior run wall clock
import re
c,n=re.subn(r"last_evidence_at: .*",f"last_evidence_at: {NOW}",c,count=1); assert n==1
section=f'''\nw3_batch_0011:
  status: SEALED
  validation: PASS
  touched_rows: 60
  p1_identity_rows: 60
  evidence_backed_rows: 60
  a_grade_rows: 60
  b_grade_rows: 0
  current_org_title_confirmed_rows: {confirmed}
  no_current_role_confirmed_rows: {no_role}
  current_org_title_unresolved_rows: {unresolved}
  unsupported_current_title_claims: 0
\n'''
assert "\nnotes:\n" in c; c=c.replace("\nnotes:\n","\n"+section+"notes:\n",1)
notes_anchor="  - Next deterministic queue order is 601.\n"
notes_add="""  - W3-BATCH-0011 processed queue orders 601-660 exactly, all 江苏 P1 identity/current-role rows.
  - 47 rows were refreshed from the live Sep-2026 Jiangsu standing-committee roster; current higher federation/chamber roles supersede stale 执委 labels.
  - Four non-roster current roles were safely bridged for 李兰翔、李厚林、陈湘珍、施勇; 钟雨 is resolved as no-current-role from the original CNINFO filing 2026-003.
  - 孙振东、李建、张飞×2、张惠扬、陈军、周洁、查艳 remain explicit unresolved current-role cases; the two 张飞 source rows are exact-value duplicate candidates and were not arbitrarily mapped to the current 淮/盐 homonyms.
  - Next deterministic queue order is 661.
"""
assert notes_anchor in c; cp.write_text(c.replace(notes_anchor,notes_anchor+notes_add,1),encoding="utf-8")

assert "latest_gate:\n  code: W3-BATCH-0011" in sp.read_text(encoding="utf-8")
assert "next_gate:\n  code: W3-BATCH-0012" in sp.read_text(encoding="utf-8")
ct=cp.read_text(encoding="utf-8")
assert "current_gate: W3-BATCH-0012" in ct and "work_cursor: 660" in ct
assert "next_queue_order: 661" in ct and "processed: 660" in ct
print(f"PASS W3-BATCH-0011 confirmed={confirmed} no_role={no_role} unresolved={unresolved} A=60 now={NOW}")
