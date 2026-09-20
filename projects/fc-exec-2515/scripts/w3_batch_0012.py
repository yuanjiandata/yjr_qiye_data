import csv, gzip, re
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evidence"
INPUT_HEAD = "fc942efc87ec6d6321943ee1c2340f32cb07aa11"
NOW = datetime.now(timezone(timedelta(hours=8))).replace(microsecond=0).isoformat()

with gzip.open(E / "W2_UNRESOLVED_QUEUE.csv.gz", "rt", encoding="utf-8-sig", newline="") as f:
    queue = list(csv.DictReader(f))[660:720]
assert len(queue) == 60
assert [int(r["queue_order"]) for r in queue] == list(range(661, 721))
assert all(r["priority"] == "P1_IDENTITY" for r in queue)
assert sum(r["province"] == "江苏" for r in queue) == 40
assert sum(r["province"] == "浙江" for r in queue) == 20

JS_STANDING_TITLE = "江苏省工商业联合会第十二届常务委员会组成人员名单（2026年9月，共计120人）"
JS_STANDING_URL = "https://www.jssh.org.cn/zzjg/fzxfhz/"
JS_EXEC_TITLE = "江苏省工商业联合会第十二届执行委员会委员名单（2026年9月，共计337名）"
JS_EXEC_URL = "https://www.jssh.org.cn/zzjg/czwmd/"
ZJ_HISTORY_TITLE = "浙江省工商业联合会第十二次代表大会召开"
ZJ_HISTORY_URL = "https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_zj/202208/t20220822_312896.html"
JS_STANDING = {"秦玉锦","顾明华","钱晓春","殷平","高飞","高晓东","郭宏新","唐成杰","唐冠玉","龚育才","康往东","董力源","蒋学明","蒋承志","傅志伟","潘骏","潘卫国","戴凌云"}
JS_CHAMBER_VICE = {"袁永刚","钱京","徐云飞","徐浩宇","曹明拓","梁勤","梁泽泉","缪文彬","薛驰"}
JS_FED_VICE = {"徐翔","殷爱国","崔根良","蒋立","蒋东良","缪汉根"}
JS_BOTH = {"徐志军"}
assert len(JS_STANDING | JS_CHAMBER_VICE | JS_FED_VICE | JS_BOTH) == 34

SPECIAL = {
    663: dict(name="顾万峰", org="中共江苏省委统战部", title="常务副部长", etype="government_official", grade="A", etitle="省委统战部召开部务会（扩大）会议暨理论学习中心组学习会", url="https://www.jstz.gov.cn/a/20260909/1788956713411.shtml", date="2026-09-09", bridge="https://www.jstz.gov.cn/a/20230209/167592865682.shtml", note="Historical Jiangsu United Front evidence anchors 顾万峰 as the former 省委统战部副部长、省工商联党组书记; Sep-2026 official evidence identifies the same person as 省委统战部常务副部长. The stale federation title is not carried forward."),
    673: dict(name="奚爱国", org="中国国民党革命委员会江苏省委员会", title="副主委", etype="formal_association_official", grade="A", etitle="民革江苏省委会十二届十八次常委会会议暨理论学习中心组学习会在南京召开", url="https://www.minge.gov.cn/n1/2026/0803/c415693-40773119.html", date="2026-08-03", bridge="https://www.acfic.org.cn/gdgslgz/js/bjgslgz/202202/t20220221_280128.html", note="ACFIC federation-history evidence anchors 奚爱国 as the Jiangsu source person; Aug-2026 民革中央 official evidence confirms his current 民革江苏省委会副主委 role."),
    680: dict(name="黄一新", org="南京钢铁集团有限公司", title="党委书记、董事长", etype="enterprise_official", grade="A", etitle="南钢开展高温慰问送清凉活动", url="https://njsteel.com.cn/BrandCulture/ShowContentDetail1?contentId=5a311549-fddb-4437-9603-0f569a8c70a2&currentCCId=f35ca146-6316-4688-9824-1c5e298808ac&index=2&parentCCId=5844302e-49e9-48b0-9c3b-eba00217a532", date="2026-08-17", bridge="https://www.acfic.org.cn/gdgslgz/js/bjgslgz/202310/t20231024_280668.html", note="ACFIC history links 黄一新 to 南钢 in the Jiangsu federation context; the enterprise's Aug-2026 official page confirms the same organization-role pair."),
}

JS_UNRESOLVED = {
    676: "郭东升 is absent from both the Sep-2026 Jiangsu standing-committee roster and the updated Sep-2026 executive roster. Earlier 2026 federation-role material is superseded by the newer official composition pages, and no post-change current organization/title was safely established.",
    681: "黄东峰 appeared in the Jul-2026 Jiangsu executive roster but is absent from the updated Sep-2026 337-member executive roster and Sep standing roster. The July status is therefore not carried forward and no separate current role was safely established.",
    694: "熊杰 is absent from both the Sep-2026 Jiangsu standing-committee roster and the updated Sep-2026 executive roster. March-2026 material still used the former federation role, but newer official composition evidence no longer supports it; no post-change current role was safely established.",
}
ZJ_LEADERS_TITLE = "浙江省工商业联合会（浙江省商会）领导｜商会领导"
ZJ_LEADERS_URL = "https://www.zjfic.org.cn/col/col1620079/index.html"
ZJ = {
    701: dict(name="王建沂", org="富通集团有限公司", title="董事长", etype="official_conference_material", grade="B", etitle="两会声音｜全国人大代表、富通集团董事长王建沂：为‘法治中国’建设尽职尽责、贡献绵薄之力", url="https://www.cwc.net.cn/tradeleads/show-8401.html", date="2026-03-11", note="The 2022 ACFIC election roster anchors 王建沂 as the Zhejiang federation source person; the Mar-2026 item, sourced from 富通集团, confirms his current 富通集团董事长 role."),
    702: dict(name="徐国龙", org="中共浙江省委金融委员会办公室 / 中共浙江省委金融工作委员会", title="常务副主任 / 常务副书记", etype="government_official", grade="A", etitle="全省地方金融系统党建工作暨党风廉政建设会议召开", url="https://sjrb.zj.gov.cn/art/2026/3/19/art_1370340_58717113.html", date="2026-03-19", note="The 2022 ACFIC roster anchors the former federation identity; Mar-2026 Zhejiang financial-office evidence confirms the same person in his current financial-system role."),
    703: dict(name="蔡晓春", org="浙商研究中心", title="副主任", etype="enterprise_official", grade="A", etitle="凤凰成长计划圆满结课 浙商齐聚财通共话发展新篇", url="https://www.ctsec.com/company/detail/9317507", date="2026-03-27", note="The 2022 ACFIC roster anchors 蔡晓春; 2026 enterprise-official material explicitly describes him as 浙商研究中心副主任 and 浙江省工商联原党组副书记、一级巡视员, so the stale federation vice-chair label is not carried forward."),
    704: dict(name="徐燕峰", org="浙江省农业农村厅", title="副厅长", etype="government_official", grade="A", etitle="浙江省农业农村厅副厅长徐燕峰来中国水稻研究所调研交流", url="https://cnrri.caas.cn/bsdt/607b21a0282747a28403d60661cc5233.htm", date="2026-06-10", note="The 2022 ACFIC roster anchors 徐燕峰 as the Zhejiang source person; Jun-2026 China Rice Research Institute official evidence confirms her current 浙江省农业农村厅副厅长 role."),
    705: dict(name="元成茂", org="浙江省工商业联合会 / 浙江省商会", title="党组成员、副主席 / 副会长", etype="federation_official", grade="A", etitle=ZJ_LEADERS_TITLE, url=ZJ_LEADERS_URL, date="2026-09", note="The live Zhejiang federation leadership page reflects the post-source current leadership. 元成茂 is currently listed as 党组成员、副主席 and 浙江省商会副会长; the current page, not the historical source label alone, is used."),
    706: dict(name="林建良", org="浙江省工商业联合会 / 浙江省商会", title="党组成员、副主席 / 副会长", etype="federation_official", grade="A", etitle=ZJ_LEADERS_TITLE, url=ZJ_LEADERS_URL, date="2026-09", note="The live Zhejiang federation leadership page currently lists 林建良 as 党组成员、副主席 and 浙江省商会副会长; the current page is used as authority."),
}

ZJ_UNRESOLVED = {
    707: "吕晓峰 is anchored by the 2022 ACFIC Zhejiang election roster, but he is absent from the live Zhejiang federation leadership page and targeted 2026 searches did not establish a sufficiently current replacement organization/title. Older 2023 federation/浙商总会 roles were not carried forward.",
}
ZJ_CURRENT_VICE = {"李书福","张天任","王世民","冯仁强","宋汉平","林俊波","鲁伟鼎","徐爱华","赖梅松","屠红燕","陈建成","张晓平","宗馥莉"}
assert len(ZJ_CURRENT_VICE) == 13

FIELDS=["queue_order","person_id","province","excel_row","source_fragment","federation_role","identity_resolution","candidate_names","repair_notes","evidence_type","evidence_grade","evidence_title","evidence_url","evidence_date","current_organization","current_title","current_verification_status","unresolved_reason"]
results=[]
for r in queue:
    q=int(r["queue_order"]); name=r["name_normalized"]
    out={"queue_order":str(q),"person_id":r["person_id"],"province":r["province"],"excel_row":r["excel_row"],"source_fragment":name,"federation_role":r["federation_role"],"candidate_names":name,"current_organization":"","current_title":"","unresolved_reason":""}
    if q in SPECIAL:
        x=SPECIAL[q]; assert name==x["name"]
        out.update(identity_resolution="CURRENT_ROLE_CONFIRMED_WITH_ROLE_HISTORY_BRIDGE",repair_notes=x["note"]+" Historical bridge: "+x["bridge"],evidence_type=x["etype"],evidence_grade=x["grade"],evidence_title=x["etitle"],evidence_url=x["url"],evidence_date=x["date"],current_organization=x["org"],current_title=x["title"],current_verification_status="CURRENT_ORG_TITLE_CONFIRMED")
    elif q in JS_UNRESOLVED:
        out.update(identity_resolution="HISTORICAL_SOURCE_IDENTITY_CURRENT_ROLE_UNRESOLVED",repair_notes="Checked the live Sep-2026 Jiangsu standing and executive composition pages plus targeted fresh public evidence. Older current-role claims were not carried across a newer composition change.",evidence_type="federation_official",evidence_grade="A",evidence_title=JS_EXEC_TITLE,evidence_url=JS_EXEC_URL,evidence_date="2026-09",current_verification_status="UNRESOLVED_CURRENT_ORG_TITLE",unresolved_reason=JS_UNRESOLVED[q])
    elif r["province"] == "江苏":
        if name in JS_STANDING: org,title="江苏省工商业联合会","常务委员"
        elif name in JS_CHAMBER_VICE: org,title="江苏省总商会","副会长"
        elif name in JS_FED_VICE: org,title="江苏省工商业联合会","副主席"
        elif name in JS_BOTH: org,title="江苏省工商业联合会 / 江苏省总商会","副主席 / 副会长（兼）"
        else: raise AssertionError((q,name))
        out.update(identity_resolution="CURRENT_ROLE_CONFIRMED_BY_LATEST_OFFICIAL_PROVINCIAL_ROSTER",repair_notes="Name + Jiangsu source scope + federation-role history reconcile to the live Sep-2026 official standing roster. Current higher federation/chamber role supersedes the stale source 执委 label; no name-only inference.",evidence_type="federation_official",evidence_grade="A",evidence_title=JS_STANDING_TITLE,evidence_url=JS_STANDING_URL,evidence_date="2026-09",current_organization=org,current_title=title,current_verification_status="CURRENT_ORG_TITLE_CONFIRMED")
    elif q in ZJ:
        x=ZJ[q]; assert name==x["name"]
        out.update(identity_resolution="CURRENT_ROLE_CONFIRMED_WITH_ROLE_HISTORY_BRIDGE",repair_notes=x["note"]+" Historical identity anchor: "+ZJ_HISTORY_URL,evidence_type=x["etype"],evidence_grade=x["grade"],evidence_title=x["etitle"],evidence_url=x["url"],evidence_date=x["date"],current_organization=x["org"],current_title=x["title"],current_verification_status="CURRENT_ORG_TITLE_CONFIRMED")
    elif q in ZJ_UNRESOLVED:
        out.update(identity_resolution="HISTORICAL_SOURCE_IDENTITY_CURRENT_ROLE_UNRESOLVED",repair_notes="The 2022 ACFIC election roster anchors the source identity. The live Zhejiang federation leadership page and targeted 2026 public search were then checked; no name-only current-role assignment was permitted.",evidence_type="federation_official",evidence_grade="A",evidence_title=ZJ_LEADERS_TITLE,evidence_url=ZJ_LEADERS_URL,evidence_date="2026-09",current_verification_status="UNRESOLVED_CURRENT_ORG_TITLE",unresolved_reason=ZJ_UNRESOLVED[q])
    elif r["province"] == "浙江" and name in ZJ_CURRENT_VICE:
        out.update(identity_resolution="CURRENT_ROLE_CONFIRMED_BY_LIVE_OFFICIAL_PROVINCIAL_LEADERSHIP_PAGE",repair_notes="The 2022 ACFIC election roster anchors the source identity; the live Zhejiang federation leadership page reflects the current post-source leadership and still lists this person as a 浙江省工商联副主席. Only the current federation role is written here; enterprise titles on the page are deferred where fresher company evidence may differ.",evidence_type="federation_official",evidence_grade="A",evidence_title=ZJ_LEADERS_TITLE,evidence_url=ZJ_LEADERS_URL,evidence_date="2026-09",current_organization="浙江省工商业联合会",current_title="副主席",current_verification_status="CURRENT_ORG_TITLE_CONFIRMED")
    else:
        raise AssertionError((q,name,r["province"]))
    results.append(out)

assert len(results)==60 and [int(x["queue_order"]) for x in results]==list(range(661,721))
assert len({x["person_id"] for x in results})==60
assert all(x["evidence_url"] and x["evidence_title"] and x["evidence_grade"] in {"A","B"} for x in results)
assert all(x["unresolved_reason"] for x in results if x["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE")
assert all(x["current_organization"] and x["current_title"] for x in results if x["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED")
confirmed=sum(x["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED" for x in results)
unresolved=sum(x["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE" for x in results)
a_grade=sum(x["evidence_grade"]=="A" for x in results)
b_grade=sum(x["evidence_grade"]=="B" for x in results)
assert (confirmed,unresolved,a_grade,b_grade)==(56,4,59,1), (confirmed,unresolved,a_grade,b_grade)
with open(E/"W3_BATCH_0012_RESULTS.csv","w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator="\n"); w.writeheader(); w.writerows(results)

LEDGER_FIELDS=["queue_order","person_id","province","excel_row","candidate_names","evidence_type","evidence_grade","evidence_title","evidence_url","evidence_date","current_verification_status","unresolved_reason"]
OVERLAY_FIELDS=["queue_order","person_id","province","excel_row","identity_resolution","candidate_names","current_organization","current_title","current_verification_status","evidence_grade","evidence_url","unresolved_reason"]
def append_rows(path,fields):
    with open(path,"r",encoding="utf-8-sig",newline="") as f: old=list(csv.DictReader(f))
    last=int(old[-1]["queue_order"])
    if last==720: return
    assert last==660,(path,last)
    with open(path,"a",encoding="utf-8",newline="") as f:
        csv.DictWriter(f,fieldnames=fields,extrasaction="ignore",lineterminator="\n").writerows(results)
append_rows(E/"W3_EVIDENCE_LEDGER.csv",LEDGER_FIELDS)
append_rows(E/"W3_VERIFICATION_OVERLAY.csv",OVERLAY_FIELDS)
for p in [E/"W3_EVIDENCE_LEDGER.csv",E/"W3_VERIFICATION_OVERLAY.csv"]:
    with open(p,"r",encoding="utf-8-sig",newline="") as f: rr=list(csv.DictReader(f))
    assert len(rr)==720 and [int(x["queue_order"]) for x in rr]==list(range(1,721))
    assert len({int(x["queue_order"]) for x in rr})==720

(E/"W3_BATCH_0012_METRICS.yaml").write_text(f'''schema: fc2515-w3-batch-metrics-v1
project_id: FC-EXEC-2515-01
gate: W3-BATCH-0012
status: PASS
queue_range: [661, 720]
batch_rows: 60
p1_identity_rows: 60
evidence_backed_rows: 60
a_grade_rows: {a_grade}
b_grade_rows: {b_grade}
structural_deferred_rows: 0
current_org_title_confirmed_rows: {confirmed}
no_current_role_confirmed_rows: 0
current_org_title_unresolved_rows: {unresolved}
unsupported_current_title_claims: 0
post_batch:
  processed_queue_rows: 720
  actionable_queue_remaining: 9924
  next_queue_order: 721
  p0_processed: 101
  p0_remaining: 0
  p1_processed: 619
  p1_remaining: 3712
next_gate: W3-BATCH-0013
''',encoding="utf-8")
(E/"W3_BATCH_0012_VALIDATION.md").write_text(f'''# W3-BATCH-0012 Validation

Result: **PASS**

- Deterministic queue slice: 661–720 exactly, 40 江苏 + 20 浙江 P1_IDENTITY rows.
- Every touched row has public evidence or an explicit unresolved-current-role reason; unsupported current-title claims: 0.
- 江苏: 34 rows are closed directly from the live Sep-2026 official standing roster; 顾万峰、奚爱国、黄一新 are closed through role-history bridges plus current official evidence. 郭东升、黄东峰、熊杰 remain unresolved because the newer Sep-2026 standing/executive composition no longer supports the earlier role and no post-change current role was safely established.
- 浙江: the 2022 ACFIC election roster is used only as the historical identity anchor. Current claims are refreshed from 2026 evidence. 王建沂、徐国龙、蔡晓春、徐燕峰 are bridged to current non-federation roles; 元成茂、林建良 are updated to the live federation leadership page; 李书福 through 宗馥莉 are retained as current 浙江省工商联副主席 only where the live official leadership page still lists them. 吕晓峰 remains unresolved because he is no longer on the live leadership page and no sufficiently current replacement role was established.
- Evidence grades: A={a_grade}, B={b_grade}, C=0; current organization/title confirmed={confirmed}/60; unresolved={unresolved}/60.
- No identity was assigned from a name-only hit. Province + federation history + current official context (or explicit organization-history bridge) is required for every current-role write.
- Cumulative evidence ledger and verification overlay each reconcile to 720 rows with queue_order 1..720, no gaps and no duplicate queue orders.

Next deterministic gate: `W3-BATCH-0013`, starting queue_order 721.
''',encoding="utf-8")

sp=ROOT/"STATUS.yaml"; s=sp.read_text(encoding="utf-8")
repls={
"code: W3-BATCH-0011\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS":"code: W3-BATCH-0012\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS",
"code: W3-BATCH-0012\n  phase: W3-EVIDENCE-ENRICH\n  status: READY":"code: W3-BATCH-0013\n  phase: W3-EVIDENCE-ENRICH\n  status: READY",
"  batches_sealed: 11":"  batches_sealed: 12",
"  processed_queue_rows: 660":"  processed_queue_rows: 720",
"  next_queue_order: 661":"  next_queue_order: 721",
"  actionable_queue_remaining: 9984":"  actionable_queue_remaining: 9924",
"    processed: 559\n    remaining: 3772":"    processed: 619\n    remaining: 3712",
"  identity_evidence_rows: 660":"  identity_evidence_rows: 720",
"  current_org_title_confirmed_rows: 367":"  current_org_title_confirmed_rows: 423",
"  current_org_title_unresolved_rows: 190":"  current_org_title_unresolved_rows: 194"}
for a,b in repls.items(): assert a in s,a; s=s.replace(a,b,1)
anchor="  w3_batch_0011_validation: projects/fc-exec-2515/evidence/W3_BATCH_0011_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv"
rep="  w3_batch_0011_validation: projects/fc-exec-2515/evidence/W3_BATCH_0011_VALIDATION.md\n  w3_batch_0012_results: projects/fc-exec-2515/evidence/W3_BATCH_0012_RESULTS.csv\n  w3_batch_0012_metrics: projects/fc-exec-2515/evidence/W3_BATCH_0012_METRICS.yaml\n  w3_batch_0012_validation: projects/fc-exec-2515/evidence/W3_BATCH_0012_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv"
assert anchor in s; sp.write_text(s.replace(anchor,rep,1),encoding="utf-8")

cp=ROOT/"CURRENT.yaml"; c=cp.read_text(encoding="utf-8")
repls={
"current_gate: W3-BATCH-0012":"current_gate: W3-BATCH-0013",
"work_cursor: 660":"work_cursor: 720",
"verified_records: 369":"verified_records: 425",
"unresolved_records: 10275":"unresolved_records: 10219",
"last_input_head: 981f994de8aee7729ce0e801bff2ce009cd3903c":f"last_input_head: {INPUT_HEAD}",
"  processed: 660":"  processed: 720",
"  actionable_remaining: 9984":"  actionable_remaining: 9924",
"  next_queue_order: 661":"  next_queue_order: 721",
"      processed: 559\n      remaining: 3772":"      processed: 619\n      remaining: 3712"}
for a,b in repls.items(): assert a in c,a; c=c.replace(a,b,1)
c,n=re.subn(r"last_evidence_at: .*",f"last_evidence_at: {NOW}",c,count=1); assert n==1
section=f'''\nw3_batch_0012:
  status: SEALED
  validation: PASS
  touched_rows: 60
  p1_identity_rows: 60
  evidence_backed_rows: 60
  a_grade_rows: {a_grade}
  b_grade_rows: {b_grade}
  current_org_title_confirmed_rows: {confirmed}
  current_org_title_unresolved_rows: {unresolved}
  unsupported_current_title_claims: 0
\n'''
assert "\nnotes:\n" in c; c=c.replace("\nnotes:\n","\n"+section+"notes:\n",1)
notes_anchor="  - Next deterministic queue order is 661.\n"
notes_add="""  - W3-BATCH-0012 processed queue orders 661-720 exactly: 40 江苏 + 20 浙江 P1 identity/current-role rows.
  - 56 rows received current organization/title confirmation; 4 remain explicit unresolved current-role cases (郭东升、黄东峰、熊杰、吕晓峰).
  - Jiangsu used the live Sep-2026 standing/executive composition as current-state authority; the Jul-2026 黄东峰 executive status was not carried forward after the updated Sep list removed it.
  - Zhejiang used the 2022 ACFIC election roster only as a historical identity anchor and refreshed current roles from 2026 evidence; the live provincial leadership page supersedes stale source titles and confirms the current vice-chair cohort from 李书福 through 宗馥莉.
  - No current organization/title was assigned from a name-only hit; evidence grades are A=59, B=1, C=0.
  - Next deterministic queue order is 721.
"""
assert notes_anchor in c; cp.write_text(c.replace(notes_anchor,notes_anchor+notes_add,1),encoding="utf-8")

st=sp.read_text(encoding="utf-8"); ct=cp.read_text(encoding="utf-8")
assert "latest_gate:\n  code: W3-BATCH-0012" in st
assert "next_gate:\n  code: W3-BATCH-0013" in st
assert "current_gate: W3-BATCH-0013" in ct and "work_cursor: 720" in ct
assert "next_queue_order: 721" in ct and "processed: 720" in ct
assert "verified_records: 425" in ct and "unresolved_records: 10219" in ct
print(f"PASS W3-BATCH-0012 confirmed={confirmed} unresolved={unresolved} A={a_grade} B={b_grade} now={NOW}")
