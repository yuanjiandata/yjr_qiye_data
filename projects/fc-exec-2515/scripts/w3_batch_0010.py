import csv, gzip
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evidence"
INPUT_HEAD = "565a50b46904107791766d627ae21a8c0af433ae"
NOW = datetime.now(timezone(timedelta(hours=8))).replace(microsecond=0).isoformat()
with gzip.open(E / "W2_UNRESOLVED_QUEUE.csv.gz", "rt", encoding="utf-8-sig", newline="") as f:
    queue = list(csv.DictReader(f))[540:600]
assert len(queue) == 60
assert [int(r["queue_order"]) for r in queue] == list(range(541, 601))
assert all(r["province"] == "江苏" and r["priority"] == "P1_IDENTITY" for r in queue)

JS_TITLE = "江苏省工商业联合会第十二届常务委员会组成人员名单（2026年9月，共计120人）"
JS_URL = "https://www.jssh.org.cn/zzjg/fzxfhz/"
JS_EXEC_TITLE = "江苏省工商业联合会第十二届执行委员会委员名单（2026年7月，共计338名）"
JS_EXEC_URL = "https://www.jssh.org.cn/zzjg/czwmd/"
FED_CHAIR = {594}
FED_VICE = {543,555,560,561,567}
CHAMBER_VICE = {541,553,557,558,566,570,576,585,592,593}
SPECIAL_Q = {544,551,552,580}
UNRESOLVED_Q = {547,565,578}
DIRECT = set(range(541,601)) - SPECIAL_Q - UNRESOLVED_Q
assert len(DIRECT) == 53
SPECIAL = {
544: dict(name="奚爱国", org="中国国民党革命委员会江苏省委员会", title="副主委", etype="formal_association_official", etitle="民革江苏省委会十二届十八次常委会会议暨理论学习中心组学习会在南京召开", url="https://www.minge.gov.cn/n1/2026/0803/c415693-40773119.html", date="2026-08-03", bridge="https://www.acfic.org.cn/gdgslgz/js/bjgslgz/202202/t20220221_280128.html", note="Repository source anchors 奚爱国 in Jiangsu federation context; 2022 ACFIC evidence identifies the same rare-name Jiangsu person as 泰州市政协副主席、市工商联主席, and the 2026 民革中央 official page identifies 奚爱国 as 民革江苏省委会副主委. Province + federation-history bridge avoids a name-only match."),
551: dict(name="黄一新", org="南京钢铁集团有限公司", title="党委书记、董事长", etype="enterprise_official", etitle="南钢开展高温慰问送清凉活动", url="https://njsteel.com.cn/BrandCulture/ShowContentDetail1?contentId=5a311549-fddb-4437-9603-0f569a8c70a2&currentCCId=f35ca146-6316-4688-9824-1c5e298808ac&index=2&parentCCId=5844302e-49e9-48b0-9c3b-eba00217a532", date="2026-08-17", bridge="https://www.acfic.org.cn/gdgslgz/js/bjgslgz/202310/t20231024_280668.html", note="Repository source anchors 黄一新 as a Jiangsu federation standing-committee member; ACFIC's 2023 Nanjing federation report identifies 黄一新 as 南钢党委书记、董事长, and the enterprise's Aug-2026 official page confirms the same organization-role pair. Province + federation context + historical organization closes identity without name-only assignment."),
552: dict(name="黄东峰", org="江苏省工商业联合会", title="执行委员会委员", etype="federation_official", etitle=JS_EXEC_TITLE, url=JS_EXEC_URL, date="2026-07", bridge="", note="The current official Jiangsu executive-committee roster includes 黄东峰 while the newer Sep-2026 standing-committee roster no longer lists him as a standing member. The stale 常委 label is not carried forward; current federation status is recorded only as 执行委员会委员."),
580: dict(name="王益冰", org="苏州市司法局", title="党组书记、局长", etype="government_official", etitle="全城寻访新就业群体学法守法之‘星’", url="https://sfj.suzhou.gov.cn/sfj/szsyfzs/202609/4295e4a7ea4348099d70883a7a4f8df9.shtml", date="2026-09-18", bridge="https://www.jssh.org.cn/xwzx/sxdt/202203/t20220317_211704.html", note="2022 Jiangsu federation evidence identifies 王益冰 as 苏州市委统战部副部长、市工商联党组书记. A Sep-18-2026 Suzhou Justice Bureau official article identifies 王益冰 as 党组书记、局长. The role-history bridge closes identity without name-only inference."),
}
UNRESOLVED = {
547: "郭东升 is absent from both the latest Sep-2026 Jiangsu standing-committee roster and the current Jul-2026 executive roster. Public material as late as May 2026 still called him 江苏省工商联党组成员、副主席, but that is superseded by newer official composition pages; no post-change current organization/title could be safely established.",
565: "熊杰 is absent from both the latest Sep-2026 Jiangsu standing-committee roster and the current Jul-2026 executive roster. March 2026 public material still called him 江苏省工商联党组成员、副主席, but newer official composition pages no longer support that role; no post-change current organization/title could be safely established.",
578: "王红卫 is absent from the latest Sep-2026 standing-committee roster and Jul-2026 executive roster. A current Jiangsu High Court official with the same name is a documented Tianjin-transferred jurist and is a rejected homonym; no province/federation/organization bridge safely links another current role to the source person.",
}
FIELDS=["queue_order","person_id","province","excel_row","source_fragment","federation_role","identity_resolution","candidate_names","repair_notes","evidence_type","evidence_grade","evidence_title","evidence_url","evidence_date","current_organization","current_title","current_verification_status","unresolved_reason"]
results=[]
for r in queue:
    q=int(r["queue_order"]); name=r["name_normalized"]
    out={"queue_order":str(q),"person_id":r["person_id"],"province":r["province"],"excel_row":r["excel_row"],"source_fragment":name,"federation_role":r["federation_role"],"candidate_names":name,"current_organization":"","current_title":"","unresolved_reason":""}
    if q in SPECIAL:
        x=SPECIAL[q]; assert name==x["name"]
        res="CURRENT_ROLE_CONFIRMED_WITH_ROLE_HISTORY_BRIDGE" if x["bridge"] else "CURRENT_ROLE_CONFIRMED_BY_CURRENT_OFFICIAL_EXECUTIVE_ROSTER"
        note=x["note"] + ((" Historical bridge: "+x["bridge"]) if x["bridge"] else "")
        out.update(identity_resolution=res,repair_notes=note,evidence_type=x["etype"],evidence_grade="A",evidence_title=x["etitle"],evidence_url=x["url"],evidence_date=x["date"],current_organization=x["org"],current_title=x["title"],current_verification_status="CURRENT_ORG_TITLE_CONFIRMED")
    elif q in UNRESOLVED_Q:
        out.update(identity_resolution="HISTORICAL_SOURCE_IDENTITY_CURRENT_ROLE_UNRESOLVED",repair_notes="Checked newest Jiangsu federation standing/executive rosters and targeted fresh public evidence; stale titles were not carried forward and same-name hits were rejected unless identity closed.",evidence_type="federation_official",evidence_grade="A",evidence_title=JS_TITLE,evidence_url=JS_URL,evidence_date="2026-09",current_verification_status="UNRESOLVED_CURRENT_ORG_TITLE",unresolved_reason=UNRESOLVED[q])
    else:
        assert q in DIRECT
        if q in FED_CHAIR: org,title="江苏省工商业联合会 / 江苏省总商会","主席 / 会长"
        elif q in FED_VICE: org,title="江苏省工商业联合会","副主席"
        elif q in CHAMBER_VICE: org,title="江苏省总商会","副会长"
        else: org,title="江苏省工商业联合会","常务委员"
        out.update(identity_resolution="CURRENT_ROLE_CONFIRMED_BY_LATEST_OFFICIAL_PROVINCIAL_ROSTER",repair_notes="Name + 江苏 source scope + federation role reconcile to the official Sep-2026 standing-committee roster. Current higher roles supersede stale labels; no name-only inference.",evidence_type="federation_official",evidence_grade="A",evidence_title=JS_TITLE,evidence_url=JS_URL,evidence_date="2026-09",current_organization=org,current_title=title,current_verification_status="CURRENT_ORG_TITLE_CONFIRMED")
    results.append(out)
assert len(results)==60 and [int(x["queue_order"]) for x in results]==list(range(541,601))
assert len({x["person_id"] for x in results})==60
assert all(x["evidence_url"] and x["evidence_title"] and x["evidence_grade"]=="A" for x in results)
assert all(x["unresolved_reason"] for x in results if x["current_verification_status"]=="UNRESOLVED_CURRENT_ORG_TITLE")
assert all(x["current_organization"] and x["current_title"] for x in results if x["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED")
confirmed=sum(x["current_verification_status"]=="CURRENT_ORG_TITLE_CONFIRMED" for x in results); unresolved=60-confirmed
assert (confirmed,unresolved)==(57,3)
with open(E/"W3_BATCH_0010_RESULTS.csv","w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator="\n"); w.writeheader(); w.writerows(results)
LEDGER_FIELDS=["queue_order","person_id","province","excel_row","candidate_names","evidence_type","evidence_grade","evidence_title","evidence_url","evidence_date","current_verification_status","unresolved_reason"]
OVERLAY_FIELDS=["queue_order","person_id","province","excel_row","identity_resolution","candidate_names","current_organization","current_title","current_verification_status","evidence_grade","evidence_url","unresolved_reason"]
def append_rows(path,fields):
    with open(path,"r",encoding="utf-8-sig",newline="") as f: old=list(csv.DictReader(f))
    last=int(old[-1]["queue_order"])
    if last==600: return
    assert last==540,(path,last)
    with open(path,"a",encoding="utf-8",newline="") as f: csv.DictWriter(f,fieldnames=fields,extrasaction="ignore",lineterminator="\n").writerows(results)
append_rows(E/"W3_EVIDENCE_LEDGER.csv",LEDGER_FIELDS)
append_rows(E/"W3_VERIFICATION_OVERLAY.csv",OVERLAY_FIELDS)
for p in [E/"W3_EVIDENCE_LEDGER.csv",E/"W3_VERIFICATION_OVERLAY.csv"]:
    with open(p,"r",encoding="utf-8-sig",newline="") as f: rr=list(csv.DictReader(f))
    assert len(rr)==600 and [int(x["queue_order"]) for x in rr]==list(range(1,601))
(E/"W3_BATCH_0010_METRICS.yaml").write_text(f'''schema: fc2515-w3-batch-metrics-v1
project_id: FC-EXEC-2515-01
gate: W3-BATCH-0010
status: PASS
queue_range: [541, 600]
batch_rows: 60
p1_identity_rows: 60
evidence_backed_rows: 60
a_grade_rows: 60
b_grade_rows: 0
structural_deferred_rows: 0
current_org_title_confirmed_rows: {confirmed}
current_org_title_unresolved_rows: {unresolved}
unsupported_current_title_claims: 0
post_batch:
  processed_queue_rows: 600
  actionable_queue_remaining: 10044
  next_queue_order: 601
  p0_processed: 101
  p0_remaining: 0
  p1_processed: 499
  p1_remaining: 3832
next_gate: W3-BATCH-0011
''',encoding="utf-8")
(E/"W3_BATCH_0010_VALIDATION.md").write_text(f'''# W3-BATCH-0010 Validation

Result: **PASS**

- Deterministic queue slice: 541–600 exactly, 60 江苏 P1_IDENTITY rows.
- Every touched row has public evidence or an explicit unresolved-current-role reason; unsupported current-title claims: 0.
- 53 rows are directly present in the official Jiangsu standing-committee roster labeled `2026年9月，共计120人` and receive current federation/chamber roles from that latest roster.
- Four additional current roles are safely closed without name-only inference: 奚爱国 via ACFIC federation-history + 2026 民革中央 official role; 黄一新 via ACFIC historical organization + Aug-2026 南钢 official role; 黄东峰 via the current Jul-2026 Jiangsu federation executive roster; 王益冰 via prior Jiangsu federation identity bridge + Sep-18-2026 Suzhou Justice Bureau official evidence.
- Three rows remain unresolved: 郭东升、熊杰、王红卫. The first two had early-2026 federation roles but are absent from newer official composition pages; 王红卫 has a known unrelated current homonym, which remains explicitly rejected.
- Evidence grades: A=60, B=0, C=0; current organization/title confirmed={confirmed}/60; unresolved={unresolved}/60.
- Cumulative evidence ledger and verification overlay each reconcile to 600 rows with queue_order 1..600 and no gaps or duplicate queue orders.

Next deterministic gate: `W3-BATCH-0011`, starting queue_order 601.
''',encoding="utf-8")
sp=ROOT/"STATUS.yaml"; s=sp.read_text(encoding="utf-8")
repls={
"code: W3-BATCH-0009\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS":"code: W3-BATCH-0010\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS",
"code: W3-BATCH-0010\n  phase: W3-EVIDENCE-ENRICH\n  status: READY":"code: W3-BATCH-0011\n  phase: W3-EVIDENCE-ENRICH\n  status: READY",
"  batches_sealed: 9":"  batches_sealed: 10","  processed_queue_rows: 540":"  processed_queue_rows: 600","  next_queue_order: 541":"  next_queue_order: 601","  actionable_queue_remaining: 10104":"  actionable_queue_remaining: 10044","    processed: 439\n    remaining: 3892":"    processed: 499\n    remaining: 3832","  identity_evidence_rows: 540":"  identity_evidence_rows: 600","  current_org_title_confirmed_rows: 259":"  current_org_title_confirmed_rows: 316","  current_org_title_unresolved_rows: 179":"  current_org_title_unresolved_rows: 182"}
for a,b in repls.items(): assert a in s,a; s=s.replace(a,b,1)
anchor="  w3_batch_0009_validation: projects/fc-exec-2515/evidence/W3_BATCH_0009_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv"
rep="  w3_batch_0009_validation: projects/fc-exec-2515/evidence/W3_BATCH_0009_VALIDATION.md\n  w3_batch_0010_results: projects/fc-exec-2515/evidence/W3_BATCH_0010_RESULTS.csv\n  w3_batch_0010_metrics: projects/fc-exec-2515/evidence/W3_BATCH_0010_METRICS.yaml\n  w3_batch_0010_validation: projects/fc-exec-2515/evidence/W3_BATCH_0010_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv"
assert anchor in s; sp.write_text(s.replace(anchor,rep,1),encoding="utf-8")
cp=ROOT/"CURRENT.yaml"; c=cp.read_text(encoding="utf-8")
repls={
"current_gate: W3-BATCH-0010":"current_gate: W3-BATCH-0011","work_cursor: 540":"work_cursor: 600","verified_records: 260":"verified_records: 317","unresolved_records: 10384":"unresolved_records: 10327","last_evidence_at: 2026-09-20T07:53:42+08:00":f"last_evidence_at: {NOW}","last_input_head: edcf8f84c99298372ffa0dcf88facb12f7a31e37":f"last_input_head: {INPUT_HEAD}","  processed: 540":"  processed: 600","  actionable_remaining: 10104":"  actionable_remaining: 10044","  next_queue_order: 541":"  next_queue_order: 601","      processed: 439\n      remaining: 3892":"      processed: 499\n      remaining: 3832"}
for a,b in repls.items(): assert a in c,a; c=c.replace(a,b,1)
section=f'''\nw3_batch_0010:
  status: SEALED
  validation: PASS
  touched_rows: 60
  p1_identity_rows: 60
  evidence_backed_rows: 60
  a_grade_rows: 60
  b_grade_rows: 0
  current_org_title_confirmed_rows: {confirmed}
  current_org_title_unresolved_rows: {unresolved}
  unsupported_current_title_claims: 0
\n'''
assert "\nnotes:\n" in c; c=c.replace("\nnotes:\n","\n"+section+"notes:\n",1)
notes_anchor="  - Next deterministic queue order is 541.\n"
notes_add="""  - W3-BATCH-0010 processed queue orders 541-600 exactly, all 江苏 P1 identity/current-role rows.
  - 53 rows were refreshed directly from the live Sep-2026 Jiangsu standing-committee roster; stale source roles were replaced by the current federation/chamber role.
  - Four additional identities were safely bridged to current roles: 奚爱国、黄一新、黄东峰、王益冰; public current claims are backed by federation/party/enterprise/government official evidence and are not name-only assignments.
  - 郭东升、熊杰、王红卫 remain explicit current-role unresolved cases because newer composition evidence removed/superseded older roles or a known homonym prevented safe linkage.
  - Next deterministic queue order is 601.
"""
assert notes_anchor in c; cp.write_text(c.replace(notes_anchor,notes_anchor+notes_add,1),encoding="utf-8")
assert "latest_gate:\n  code: W3-BATCH-0010" in sp.read_text(encoding="utf-8")
assert "next_gate:\n  code: W3-BATCH-0011" in sp.read_text(encoding="utf-8")
ct=cp.read_text(encoding="utf-8")
assert "current_gate: W3-BATCH-0011" in ct and "work_cursor: 600" in ct
assert "next_queue_order: 601" in ct and "processed: 600" in ct
print(f"PASS W3-BATCH-0010 confirmed={confirmed} unresolved={unresolved} A=60 now={NOW}")
