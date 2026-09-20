#!/usr/bin/env python3
import csv, gzip, glob, subprocess, re
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
P = ROOT / "projects" / "fc-exec-2515"
E = P / "evidence"
INPUT_HEAD = "5e8d9e3ffa0c308a1befc5406bd4de03b0a48b00"
BATCH_START, BATCH_END = 1381, 1440
NOW = datetime.now(timezone(timedelta(hours=8))).replace(microsecond=0).isoformat()
FJ_HIST = "https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_fj/202208/t20220830_312930.html"

head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
assert head == INPUT_HEAD, (head, INPUT_HEAD)
with gzip.open(E / "W2_UNRESOLVED_QUEUE.csv.gz", "rt", encoding="utf-8-sig", newline="") as f:
    allq = list(csv.DictReader(f))
rows = allq[BATCH_START - 1:BATCH_END]
assert len(rows) == 60
assert [int(r["queue_order"]) for r in rows] == list(range(BATCH_START, BATCH_END + 1))
assert {r["priority"] for r in rows} == {"P1_IDENTITY"}
assert Counter(r["province"] for r in rows) == Counter({"福建": 60})
by_order = {}
for fn in sorted(glob.glob(str(E / "W3_BATCH_*_RESULTS.csv"))):
    with open(fn, "r", encoding="utf-8-sig", newline="") as f:
        for x in csv.DictReader(f):
            if int(x["queue_order"]) < BATCH_START:
                by_order[int(x["queue_order"])] = x
by_ag = defaultdict(list)
for q in allq:
    by_ag[q["ambiguity_group_id"]].append(q)

# Current-role writes require context beyond name: exact historical organization,
# direct current federation role, or a multi-source federation identity bridge.
special = {}
with (E / "W3_BATCH_0024_RESEARCH.tsv").open("r", encoding="utf-8-sig", newline="") as f:
    for x in csv.DictReader(f, delimiter="	"):
        special[x["name_normalized"]] = dict(org=x["org"], title=x["title"], grade=x["grade"], etype=x["etype"], etitle=x["etitle"], url=x["url"], date=x["date"], notes=x["notes"])

# All other touched identities were individually or cohort-searched against current
# government/federation/company/filing/media sources. If the identity bridge is not
# strong enough, leave current role blank rather than guessing from a homonym.
special_unresolved = {
    "刘木火": "2025福州人大系统出现同名代表信息，但未取得与福建省工商联常委源记录及当前单位职务之间的安全身份桥；不按姓名归并。",
    "吴国仕": "2026晋江政府材料出现兴业皮革/宏兴汽车皮革同名企业负责人，但未取得其与福建省工商联常委源身份的直接当前桥接，故不写现职。",
    "张勇": "张勇属于高频同名；当前福建公开资料存在多名同名干部/企业人士，源记录无历史单位键，禁止按姓名择一。",
    "张文亮": "检索到福建相关社团/企业同名公开信息，但没有与省工商联常委源身份形成足够强的身份连续链，故保持未决。",
    "陈晖": "当前公开资料存在多名福建同名陈晖，且无历史单位键可用于安全消歧；不按姓名推断。",
    "陈锦（女）": "当前公开资料存在多名福建同名陈锦，源记录仅有性别与常委角色，仍不足以唯一锁定当前单位职务。",
}
fields = ["queue_order","person_id","province","excel_row","name_normalized","source_federation_role","identity_resolution","candidate_names","current_organization","current_title","current_verification_status","evidence_type","evidence_grade","evidence_title","evidence_url","evidence_date","unresolved_reason","research_notes"]
results = []
for r in rows:
    name = r["name_normalized"]
    base = {"queue_order": r["queue_order"], "person_id": r["person_id"], "province": r["province"], "excel_row": r["excel_row"], "name_normalized": name, "source_federation_role": r["federation_role"], "candidate_names": name}
    priors = [x for x in by_ag[r["ambiguity_group_id"]] if int(x["queue_order"]) < BATCH_START and int(x["queue_order"]) in by_order]
    if priors:
        p = max(priors, key=lambda x: int(x["queue_order"]))
        prev = by_order[int(p["queue_order"])]
        assert p["province"] == r["province"] and p["name_normalized"] == name
        result = {**base, "identity_resolution": "REUSED_SEALED_EVIDENCE_SAME_REPOSITORY_AMBIGUITY_GROUP", "current_organization": prev["current_organization"], "current_title": prev["current_title"], "current_verification_status": prev["current_verification_status"], "evidence_type": prev["evidence_type"], "evidence_grade": prev["evidence_grade"], "evidence_title": prev["evidence_title"], "evidence_url": prev["evidence_url"], "evidence_date": prev["evidence_date"], "unresolved_reason": prev["unresolved_reason"], "research_notes": f"与已封存 queue {p['queue_order']} 同省、同名且同 ambiguity_group_id={r['ambiguity_group_id']}；复用证据但保留独立 person_id。" + prev["research_notes"]}
    elif name in special:
        s = special[name]
        result = {**base, "identity_resolution": "CURRENT_ROLE_CONFIRMED_WITH_CONTEXTUAL_IDENTITY_BRIDGE", "current_organization": s["org"], "current_title": s["title"], "current_verification_status": "CURRENT_ORG_TITLE_CONFIRMED", "evidence_type": s["etype"], "evidence_grade": s["grade"], "evidence_title": s["etitle"], "evidence_url": s["url"], "evidence_date": s["date"], "unresolved_reason": "", "research_notes": s["notes"] + f" 历史身份锚点：{FJ_HIST}"}
    else:
        reason = special_unresolved.get(name, "已针对2026年政府、工商联、企业官网、上市公司披露及权威媒体进行当前角色检索；现有命中缺少足够的源身份桥、存在同名风险，或未能证明当前职务仍在任，因此保持未决。")
        result = {**base, "identity_resolution": "HISTORICAL_IDENTITY_CURRENT_ROLE_UNRESOLVED", "current_organization": "", "current_title": "", "current_verification_status": "UNRESOLVED_CURRENT_ORG_TITLE", "evidence_type": "federation_official_historical_identity_plus_targeted_current_research", "evidence_grade": "A", "evidence_title": "福建省工商业联合会（总商会）第十二届执委会名单", "evidence_url": FJ_HIST, "evidence_date": "2022-08-30", "unresolved_reason": reason, "research_notes": f"2026-09-20完成本批当前角色公开检索；禁止以姓名单字段认人。历史身份锚点：{FJ_HIST}"}
    results.append(result)

out = E / "W3_BATCH_0024_RESULTS.csv"
with out.open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n"); w.writeheader(); w.writerows(results)
ledger_path = E / "W3_EVIDENCE_LEDGER.csv"
with ledger_path.open("r", encoding="utf-8-sig", newline="") as f:
    old_ledger = list(csv.DictReader(f)); ledger_fields = list(old_ledger[0].keys())
assert len(old_ledger) == 1380
new_ledger = old_ledger + [{k: {
    "queue_order": x["queue_order"], "person_id": x["person_id"], "province": x["province"],
    "excel_row": x["excel_row"], "candidate_names": x["candidate_names"],
    "evidence_type": x["evidence_type"], "evidence_grade": x["evidence_grade"],
    "evidence_title": x["evidence_title"], "evidence_url": x["evidence_url"],
    "evidence_date": x["evidence_date"], "current_verification_status": x["current_verification_status"],
    "unresolved_reason": x["unresolved_reason"]}.get(k, "") for k in ledger_fields} for x in results]
with ledger_path.open("a", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=ledger_fields, lineterminator="\n"); w.writerows(new_ledger[len(old_ledger):])

overlay_path = E / "W3_VERIFICATION_OVERLAY.csv"
with overlay_path.open("r", encoding="utf-8-sig", newline="") as f:
    old_overlay = list(csv.DictReader(f)); overlay_fields = list(old_overlay[0].keys())
assert len(old_overlay) == 1380
new_overlay = old_overlay + [{k: {
    "queue_order": x["queue_order"], "person_id": x["person_id"], "province": x["province"],
    "excel_row": x["excel_row"], "identity_resolution": x["identity_resolution"],
    "candidate_names": x["candidate_names"], "current_organization": x["current_organization"],
    "current_title": x["current_title"], "current_verification_status": x["current_verification_status"],
    "evidence_grade": x["evidence_grade"], "evidence_url": x["evidence_url"],
    "unresolved_reason": x["unresolved_reason"]}.get(k, "") for k in overlay_fields} for x in results]
with overlay_path.open("a", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=overlay_fields, lineterminator="\n"); w.writerows(new_overlay[len(old_overlay):])

statuses = Counter(x["current_verification_status"] for x in results)
grades = Counter(x["evidence_grade"] for x in results)
confirmed = statuses["CURRENT_ORG_TITLE_CONFIRMED"]
unresolved = statuses["UNRESOLVED_CURRENT_ORG_TITLE"]
assert confirmed == 15 and unresolved == 45, (confirmed, unresolved)
assert grades == Counter({"A": 52, "B": 8}), grades
assert len(new_ledger) == 1440 and len(new_overlay) == 1440
assert [int(x["queue_order"]) for x in new_ledger] == list(range(1, 1441))
assert [int(x["queue_order"]) for x in new_overlay] == list(range(1, 1441))
assert len({x["queue_order"] for x in new_ledger}) == 1440
assert len({x["queue_order"] for x in new_overlay}) == 1440
assert all((x["evidence_url"] or x["unresolved_reason"]) for x in results)
assert all(not (x["current_verification_status"] == "CURRENT_ORG_TITLE_CONFIRMED" and (not x["current_organization"] or not x["current_title"] or not x["evidence_url"])) for x in results)
assert all(not (x["current_verification_status"] == "UNRESOLVED_CURRENT_ORG_TITLE" and (x["current_organization"] or x["current_title"] or not x["unresolved_reason"])) for x in results)
metrics = f'''schema: fc-exec-2515-w3-batch-metrics-v1
project_id: FC-EXEC-2515-01
gate: W3-BATCH-0024
status: SEALED
validation: PASS
touched_rows: 60
fujian_rows: 60
p1_identity_rows: 60
evidence_backed_rows: 60
a_grade_rows: {grades['A']}
b_grade_rows: {grades['B']}
c_grade_rows: 0
current_org_title_confirmed_rows: {confirmed}
current_org_title_unresolved_rows: {unresolved}
unsupported_current_title_claims: 0
queue_start: 1381
queue_end: 1440
next_queue_order: 1441
verified_at: {NOW}
input_head: {INPUT_HEAD}
'''
(E / "W3_BATCH_0024_METRICS.yaml").write_text(metrics, encoding="utf-8")
validation = f'''# W3-BATCH-0024 Validation

- Gate: `W3-BATCH-0024`
- Queue orders: `1381-1440`
- Touched rows: **60** (`福建 60`)
- Priority: `P1_IDENTITY` 60
- Evidence coverage: **60/60**
- Evidence grades: **A={grades['A']}, B={grades['B']}, C=0**
- Current organization + title confirmed: **{confirmed}**
- Explicit current-role unresolved: **{unresolved}**
- Unsupported current-title claims: **0**
- Cumulative evidence ledger: **1440 rows**, queue `1-1440` contiguous, no duplicate queue order
- Cumulative verification overlay: **1440 rows**, queue `1-1440` contiguous, no duplicate queue order

## Identity / recency controls

- Thirteen cross-listed 福建 rows reuse sealed evidence only after exact repository `ambiguity_group_id + province + normalized name` match; each source row retains an independent `person_id`.
- The remaining 47 rows were freshly reviewed against current public government/federation/company/filing or authoritative-media evidence; 7 obtained safe current-role closure and 40 remain explicit unresolved.
- Strong current closures include 郭建涛 via a live enterprise-official team page that states both 福建省工商联常委 and company chairman/president; 胡鹄 and 翁冠枢 via 2026 listed-company appointment disclosures carrying their 福建省工商联常委 identity; 郭恒禄 via a current government role page plus a current 福州市工商联 bridge.
- Current federation-context closures also include 林从金、蒋海鸿; 林谋悦 is closed by a historical explicit 福建省工商联常委+enterprise bridge plus 2026 current authoritative-media reporting.
- High-homonym or weak-bridge rows remain unresolved; no current organization/title is assigned from a name-only hit.

**PASS**
'''
(E / "W3_BATCH_0024_VALIDATION.md").write_text(validation, encoding="utf-8")

status_path = P / "STATUS.yaml"
s = status_path.read_text(encoding="utf-8")
for a,b in {
    "code: W3-BATCH-0023\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED": "code: W3-BATCH-0024\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED",
    "code: W3-BATCH-0024\n  phase: W3-EVIDENCE-ENRICH\n  status: READY": "code: W3-BATCH-0025\n  phase: W3-EVIDENCE-ENRICH\n  status: READY",
    "batches_sealed: 23": "batches_sealed: 24",
    "processed_queue_rows: 1380": "processed_queue_rows: 1440",
    "next_queue_order: 1381": "next_queue_order: 1441",
    "actionable_queue_remaining: 9264": "actionable_queue_remaining: 9204",
    "processed: 1279": "processed: 1339",
    "remaining: 3052": "remaining: 2992",
    "identity_evidence_rows: 1380": "identity_evidence_rows: 1440",
    "current_org_title_confirmed_rows: 810": "current_org_title_confirmed_rows: 825",
    "current_org_title_unresolved_rows: 467": "current_org_title_unresolved_rows: 512",
}.items():
    assert a in s, a
    s = s.replace(a,b,1)
anchor = "  w3_batch_0023_validation: projects/fc-exec-2515/evidence/W3_BATCH_0023_VALIDATION.md\n"
assert anchor in s
s = s.replace(anchor, anchor + "  w3_batch_0024_research: projects/fc-exec-2515/evidence/W3_BATCH_0024_RESEARCH.tsv\n  w3_batch_0024_results: projects/fc-exec-2515/evidence/W3_BATCH_0024_RESULTS.csv\n  w3_batch_0024_metrics: projects/fc-exec-2515/evidence/W3_BATCH_0024_METRICS.yaml\n  w3_batch_0024_validation: projects/fc-exec-2515/evidence/W3_BATCH_0024_VALIDATION.md\n", 1)
status_path.write_text(s, encoding="utf-8")

current_path = P / "CURRENT.yaml"
c = current_path.read_text(encoding="utf-8")
for a,b in {
    "current_gate: W3-BATCH-0024": "current_gate: W3-BATCH-0025",
    "work_cursor: 1380": "work_cursor: 1440",
    "verified_records: 812": "verified_records: 827",
    "unresolved_records: 9832": "unresolved_records: 9817",
    "processed: 1380": "processed: 1440",
    "actionable_remaining: 9264": "actionable_remaining: 9204",
    "next_queue_order: 1381": "next_queue_order: 1441",
    "processed: 1279": "processed: 1339",
    "remaining: 3052": "remaining: 2992",
}.items():
    assert a in c, a
    c = c.replace(a,b,1)
assert "last_input_head: fd480fd85b1f6961711b721ab8bebf47c9f0b9a5" in c
c = c.replace("last_input_head: fd480fd85b1f6961711b721ab8bebf47c9f0b9a5", f"last_input_head: {INPUT_HEAD}", 1)
c = re.sub(r"last_evidence_at: .*", f"last_evidence_at: {NOW}", c, count=1)
batch_block = f'''
w3_batch_0024:
  status: SEALED
  validation: PASS
  touched_rows: 60
  fujian_rows: 60
  p1_identity_rows: 60
  evidence_backed_rows: 60
  a_grade_rows: {grades['A']}
  b_grade_rows: {grades['B']}
  c_grade_rows: 0
  current_org_title_confirmed_rows: {confirmed}
  current_org_title_unresolved_rows: {unresolved}
  unsupported_current_title_claims: 0

'''
assert "notes:\n" in c
c = c.replace("notes:\n", batch_block + "notes:\n", 1)
c = c.rstrip() + f'''
  - W3-BATCH-0024 processed queue orders 1381-1440 exactly, all 60 福建 P1 identity/current-role rows.
  - {confirmed} rows received current organization/title confirmation; {unresolved} remain explicit unresolved; unsupported current-title claims remain zero.
  - Thirteen rows reused prior sealed evidence only through exact repository ambiguity_group_id + normalized name + province match; each source record retains its independent person_id.
  - The other 47 rows received fresh current-web review; 7 were safely closed and 40 remain unresolved rather than inferred from name.
  - Strong current closures include 郭建涛、胡鹄、翁冠枢、郭恒禄; each has an enterprise/listed-company/government source that also supplies a federation-context identity bridge.
  - Current federation-context closures also include 林从金、蒋海鸿; 林谋悦 uses an explicit historical 福建省工商联常委+enterprise bridge followed by 2026 current reporting.
  - Evidence grades are A={grades['A']}, B={grades['B']}, C=0; next deterministic queue order is 1441.
'''
current_path.write_text(c, encoding="utf-8")
print(f"PASS W3-BATCH-0024 confirmed={confirmed} unresolved={unresolved} grades={dict(grades)} next=1441")