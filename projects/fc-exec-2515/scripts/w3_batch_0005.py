import csv, gzip, glob
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evidence"
INPUT_HEAD = "ae2818b476cf0bab94685b059491dfe6a192fd87"
NOW = datetime.now(timezone(timedelta(hours=8))).replace(microsecond=0).isoformat()

with gzip.open(E / "W2_UNRESOLVED_QUEUE.csv.gz", "rt", encoding="utf-8-sig", newline="") as f:
    queue = list(csv.DictReader(f))[240:300]
assert [int(r["queue_order"]) for r in queue] == list(range(241, 301))
assert all(r["priority"] == "P1_IDENTITY" for r in queue)
assert all(r["province"] == "河北" for r in queue)

HE = (
    "federation_official", "A", "河北省工商业联合会(总商会)第十三届执委会名单",
    "https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_he/202207/t20220715_312762.html",
    "2022-07-15",
)

# Current-role evidence already sealed for another row of the same Hebei federation person.
# Reuse is allowed only for explicitly mapped queue pairs after checking that the same official
# Hebei roster cross-lists that name under both the earlier federation role and 执委.
REUSE = {
    242: 132, 255: 183, 256: 135, 264: 189, 274: 126, 277: 197, 282: 143,
    284: 152, 287: 125, 290: 206, 294: 209, 298: 124, 299: 130,
}

prior = {}
for path in sorted(glob.glob(str(E / "W3_BATCH_000*_RESULTS.csv"))):
    if path.endswith("W3_BATCH_0005_RESULTS.csv"):
        continue
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            prior[int(row["queue_order"])] = row
for target_q, source_q in REUSE.items():
    assert source_q in prior
    assert prior[source_q]["current_verification_status"] == "CURRENT_ORG_TITLE_CONFIRMED"
    target_name = next(r["name_normalized"] for r in queue if int(r["queue_order"]) == target_q)
    assert prior[source_q]["source_fragment"] == target_name

# q: resolution, evidence_type, grade, title, url, date, org, role, note
FRESH = {
    246: (
        "CURRENT_ENTERPRISE_ROLE_IDENTIFIED", "enterprise_official", "A",
        "复盘耕耘路 聚力启新程 | 河北省互感器技术创新中心2026年度会议圆满召开",
        "https://www.snkgroup.cn/news/detail/70", "2026-07-11",
        "申科科技集团有限公司", "董事长",
        "Official Hebei federation roster anchors 王力崇 as the Hebei executive member; the enterprise official page identifies the same uncommon-name person as current group chairman.",
    ),
    247: (
        "CURRENT_PUBLIC_ROLE_IDENTIFIED", "authoritative_media", "B",
        "省政府新闻办“‘十四五’高质量发展河北答卷”系列主题新闻发布会 河北省人民政府国有资产监督管理委员会专场文字实录",
        "https://hebfb.hebccw.cn/system/2025/11/12/102122445.shtml", "2025-11-12",
        "河北省人民政府国有资产监督管理委员会", "二级巡视员、规划处处长",
        "Hebei federation roster anchors 王大玮 in the province; the provincial policy publicity platform explicitly identifies his current SASAC role and planning-department post.",
    ),
    252: (
        "CURRENT_ENTERPRISE_ROLE_IDENTIFIED", "enterprise_official", "A",
        "中国旭阳集团举行2025年度业绩发布会：底部反转，盈利走强",
        "https://www.risun.com/news/details_294_10121.html", "2026-04-13",
        "河北旭阳能源有限公司", "董事长（兼中国旭阳集团副总裁）",
        "Hebei federation roster anchors 王英其; China Risun official coverage explicitly identifies him as group vice president and Hebei Risun chairman.",
    ),
    253: (
        "CURRENT_ENTERPRISE_ROLE_IDENTIFIED", "listed_company_filing", "A",
        "厚普清洁能源（集团）股份有限公司第六届董事会第二次会议决议公告",
        "https://static.cninfo.com.cn/finalpage/2026-08-05/1225458411.PDF", "2026-08-05",
        "厚普清洁能源（集团）股份有限公司", "董事长",
        "Hebei federation roster anchors 王季文; the August 2026 listed-company filing states the board meeting was chaired by company chairman 王季文.",
    ),
    262: (
        "CURRENT_ENTERPRISE_ROLE_IDENTIFIED", "authoritative_media", "B",
        "“河北王”换帅！老白干酒进入“王占刚时代”",
        "https://finance.eastmoney.com/a/202605203743368323.html", "2026-05-20",
        "河北山庄集团", "董事长",
        "Hebei federation roster anchors 尤文武; China Business Journal coverage reports him as 河北山庄集团董事长 while describing the group’s 2025-2026 operating performance.",
    ),
    265: (
        "CURRENT_ENTERPRISE_ROLE_IDENTIFIED", "federation_official", "A",
        "晨光生物科技集团股份有限公司董事长卢庆国：在千百次萃取中精益求精",
        "https://www.acfic.org.cn/myjjzs/qyjjy/202508/t20250818_319805.html", "2025-08-18",
        "晨光生物科技集团股份有限公司", "董事长",
        "ACFIC enterprise-profile coverage identifies 卢庆国 as current Morninglight Bio chairman; the Hebei federation roster supplies the provincial executive identity anchor.",
    ),
    268: (
        "CURRENT_ENTERPRISE_ROLE_IDENTIFIED", "government_official", "A",
        "河北代表委员议国是·特别关注｜“链”上发力，京津冀协同发展动能澎湃",
        "https://www.lf.gov.cn/Item/146020.aspx", "2025-03-04",
        "秦皇岛兴龙科技集团", "董事长",
        "Hebei federation roster anchors 田纯刚; Langfang municipal-government republication of Hebei Government content identifies him as a national legislator and Xinglong Technology Group chairman.",
    ),
    279: (
        "CURRENT_PUBLIC_ROLE_IDENTIFIED", "authoritative_media", "B",
        "河北省商标品牌协会第三届五次理事会在衡水市召开",
        "https://www.hbjjrb.cn/system/2026/01/19/102145436.shtml", "2026-01-19",
        "衡水市工商业联合会", "主席",
        "Hebei federation roster anchors 刘宏志; 2026 Hebei Economic Daily coverage explicitly identifies him as 衡水市工商联主席.",
    ),
    293: (
        "CURRENT_ENTERPRISE_ROLE_IDENTIFIED", "authoritative_media", "B",
        "李鹏亮代表：打造“冀酒IP” 赋能冀酒振兴",
        "https://he.people.com.cn/n2/2026/0127/c192235-41484894.html", "2026-01-27",
        "河北邯郸丛台酒业股份有限公司", "党委书记、总经理",
        "Hebei federation roster anchors 李鹏亮; People.cn Hebei identifies him as a provincial legislator and the company party secretary/general manager.",
    ),
}

FIELDS = [
    "queue_order", "person_id", "province", "excel_row", "source_fragment", "federation_role",
    "identity_resolution", "candidate_names", "repair_notes", "evidence_type", "evidence_grade",
    "evidence_title", "evidence_url", "evidence_date", "current_organization", "current_title",
    "current_verification_status", "unresolved_reason",
]
results = []
for r in queue:
    q = int(r["queue_order"])
    name = r["name_normalized"]
    out = {
        "queue_order": str(q), "person_id": r["person_id"], "province": r["province"],
        "excel_row": r["excel_row"], "source_fragment": name, "federation_role": r["federation_role"],
        "candidate_names": name, "current_organization": "", "current_title": "", "unresolved_reason": "",
    }
    if q in REUSE:
        src = prior[REUSE[q]]
        out.update(
            identity_resolution="CURRENT_ROLE_REUSED_WITH_OFFICIAL_ROSTER_CROSSLIST",
            repair_notes=(
                f"Same 河北 person is cross-listed in the official provincial federation roster under the earlier role and 执委; "
                f"reused sealed current-role evidence from W3 queue {REUSE[q]} without merging person_ids. " + src["repair_notes"]
            ),
            evidence_type=src["evidence_type"], evidence_grade=src["evidence_grade"],
            evidence_title=src["evidence_title"], evidence_url=src["evidence_url"], evidence_date=src["evidence_date"],
            current_organization=src["current_organization"], current_title=src["current_title"],
            current_verification_status="CURRENT_ORG_TITLE_CONFIRMED",
        )
    elif q in FRESH:
        res, typ, grade, etitle, url, edate, org, title, note = FRESH[q]
        out.update(
            identity_resolution=res, repair_notes=note, evidence_type=typ, evidence_grade=grade,
            evidence_title=etitle, evidence_url=url, evidence_date=edate,
            current_organization=org, current_title=title,
            current_verification_status="CURRENT_ORG_TITLE_CONFIRMED",
        )
    else:
        typ, grade, etitle, url, edate = HE
        out.update(
            identity_resolution="IDENTITY_ONLY_OFFICIAL_ROSTER",
            repair_notes="Identity retained from official Hebei federation roster; current organization/title intentionally left unresolved.",
            evidence_type=typ, evidence_grade=grade, evidence_title=etitle, evidence_url=url, evidence_date=edate,
            current_verification_status="UNRESOLVED_CURRENT_ORG_TITLE",
            unresolved_reason=(
                "Official Hebei federation roster confirms this source identity/role, but this batch did not find sufficiently "
                "current and specific public evidence to assign a current organization/title without risking a name-only match."
            ),
        )
    results.append(out)

with open(E / "W3_BATCH_0005_RESULTS.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
    w.writeheader(); w.writerows(results)

LEDGER_FIELDS = ["queue_order", "person_id", "province", "excel_row", "candidate_names", "evidence_type", "evidence_grade", "evidence_title", "evidence_url", "evidence_date", "current_verification_status", "unresolved_reason"]
OVERLAY_FIELDS = ["queue_order", "person_id", "province", "excel_row", "identity_resolution", "candidate_names", "current_organization", "current_title", "current_verification_status", "evidence_grade", "evidence_url", "unresolved_reason"]

def append_rows(path, fields, rows):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        old = list(csv.DictReader(f))
    last = int(old[-1]["queue_order"])
    if last == 300:
        return
    assert last == 240, (path, last)
    with open(path, "a", encoding="utf-8", newline="") as f:
        csv.DictWriter(f, fieldnames=fields, extrasaction="ignore", lineterminator="\n").writerows(rows)

append_rows(E / "W3_EVIDENCE_LEDGER.csv", LEDGER_FIELDS, results)
append_rows(E / "W3_VERIFICATION_OVERLAY.csv", OVERLAY_FIELDS, results)

confirmed = sum(r["current_verification_status"] == "CURRENT_ORG_TITLE_CONFIRMED" for r in results)
unresolved = 60 - confirmed
a_count = sum(r["evidence_grade"] == "A" for r in results)
b_count = sum(r["evidence_grade"] == "B" for r in results)
assert confirmed == 22 and unresolved == 38
assert a_count == 52 and b_count == 8
assert all(r["evidence_url"] and r["evidence_title"] for r in results)
assert all(
    (r["current_organization"] and r["current_title"])
    if r["current_verification_status"] == "CURRENT_ORG_TITLE_CONFIRMED"
    else bool(r["unresolved_reason"])
    for r in results
)
with open(E / "W3_EVIDENCE_LEDGER.csv", "r", encoding="utf-8-sig", newline="") as f:
    led = list(csv.DictReader(f))
assert len(led) == 300 and [int(x["queue_order"]) for x in led] == list(range(1, 301))

(E / "W3_BATCH_0005_METRICS.yaml").write_text(f"""schema: fc2515-w3-batch-metrics-v1
project_id: FC-EXEC-2515-01
gate: W3-BATCH-0005
status: PASS
queue_range: [241, 300]
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
  processed_queue_rows: 300
  actionable_queue_remaining: 10344
  next_queue_order: 301
  p0_processed: 101
  p0_remaining: 0
  p1_processed: 199
  p1_remaining: 4132
next_gate: W3-BATCH-0006
""", encoding="utf-8")

(E / "W3_BATCH_0005_VALIDATION.md").write_text(f"""# W3-BATCH-0005 Validation

Result: **PASS**

- Deterministic queue slice: 241–300 exactly, 60 rows, all P1_IDENTITY / 河北.
- Every touched row has public evidence or an explicit unresolved-current-role reason.
- Official Hebei ACFIC roster remains the identity anchor for all 60 rows; no name-only person merge was performed.
- 13 current-role results reuse already sealed evidence only where the same name is cross-listed by the same official Hebei roster under the earlier federation role and 执委; the source person_ids remain separate.
- 9 additional current roles were verified from fresh public sources, including enterprise official, listed-company filing, government/federation official and authoritative-media evidence.
- Evidence grades in batch: A={a_count}, B={b_count}; C=0.
- Current organization + title confirmed: {confirmed}/60.
- Current-role unresolved: {unresolved}/60; unresolved organization/title fields remain blank rather than guessed.
- Fresh 2026 evidence confirms 王力崇、王英其、王季文、尤文武、刘宏志 and 李鹏亮; other verified current roles include 王大玮、卢庆国 and 田纯刚.
- Common-name rows such as 王勇、王志民 and 刘清 remain unresolved because no safe current-role linkage was found in this batch.
- Cumulative W3 evidence ledger reconciles to 300 rows with queue_order 1..300 and no gaps.
- Unsupported current-title claims: 0.

Next deterministic gate: `W3-BATCH-0006`, starting queue_order 301.
""", encoding="utf-8")

sp = ROOT / "STATUS.yaml"
s = sp.read_text(encoding="utf-8")
s = s.replace("code: W3-BATCH-0004\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS", "code: W3-BATCH-0005\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS", 1)
s = s.replace("code: W3-BATCH-0005\n  phase: W3-EVIDENCE-ENRICH\n  status: READY", "code: W3-BATCH-0006\n  phase: W3-EVIDENCE-ENRICH\n  status: READY", 1)
for a, b in {
    "  batches_sealed: 4": "  batches_sealed: 5",
    "  processed_queue_rows: 240": "  processed_queue_rows: 300",
    "  next_queue_order: 241": "  next_queue_order: 301",
    "  actionable_queue_remaining: 10404": "  actionable_queue_remaining: 10344",
    "    processed: 139\n    remaining: 4192": "    processed: 199\n    remaining: 4132",
    "  identity_evidence_rows: 240": "  identity_evidence_rows: 300",
    "  current_org_title_confirmed_rows: 45": "  current_org_title_confirmed_rows: 67",
    "  current_org_title_unresolved_rows: 94": "  current_org_title_unresolved_rows: 132",
}.items():
    assert a in s, a
    s = s.replace(a, b, 1)
anchor = "  w3_batch_0004_validation: projects/fc-exec-2515/evidence/W3_BATCH_0004_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv"
rep = "  w3_batch_0004_validation: projects/fc-exec-2515/evidence/W3_BATCH_0004_VALIDATION.md\n  w3_batch_0005_results: projects/fc-exec-2515/evidence/W3_BATCH_0005_RESULTS.csv\n  w3_batch_0005_metrics: projects/fc-exec-2515/evidence/W3_BATCH_0005_METRICS.yaml\n  w3_batch_0005_validation: projects/fc-exec-2515/evidence/W3_BATCH_0005_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv"
assert anchor in s
s = s.replace(anchor, rep, 1)
sp.write_text(s, encoding="utf-8")

cp = ROOT / "CURRENT.yaml"
c = cp.read_text(encoding="utf-8")
c = c.replace("current_gate: W3-BATCH-0005", "current_gate: W3-BATCH-0006", 1).replace("work_cursor: 240", "work_cursor: 300", 1)
for a, b in {
    "verified_records: 45": "verified_records: 67",
    "unresolved_records: 10599": "unresolved_records: 10577",
    "last_input_head: 5a510ef785118199b42b0b0444fb16f1481db647": f"last_input_head: {INPUT_HEAD}",
    "  processed: 240": "  processed: 300",
    "  actionable_remaining: 10404": "  actionable_remaining: 10344",
    "  next_queue_order: 241": "  next_queue_order: 301",
    "      processed: 139\n      remaining: 4192": "      processed: 199\n      remaining: 4132",
}.items():
    assert a in c, a
    c = c.replace(a, b, 1)
# Replace timestamp regardless of previous exact value.
lines = c.splitlines()
for i, line in enumerate(lines):
    if line.startswith("last_evidence_at:"):
        lines[i] = f"last_evidence_at: {NOW}"
        break
c = "\n".join(lines) + "\n"
b5 = f"""
w3_batch_0005:
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
"""
assert "\nnotes:\n" in c
c = c.replace("\nnotes:\n", b5 + "\nnotes:\n", 1)
needle = "  - Next deterministic queue order is 241.\n"
notes = """  - Next deterministic queue order is 241.
  - W3-BATCH-0005 processed queue orders 241-300 exactly, all 河北 P1 identity/current-role rows.
  - 22 rows received current organization/title confirmation; 38 remain explicitly unresolved where current evidence was insufficiently specific.
  - Thirteen confirmations reuse prior sealed current-role evidence only after same-roster cross-list identity closure; no person_id merge was performed.
  - Fresh current-role evidence was added for 王力崇、王大玮、王英其、王季文、尤文武、卢庆国、田纯刚、刘宏志、李鹏亮; 孙清良 remains unresolved because the freshest strong title evidence found was not recent enough for a current-title claim.
  - No current organization/title was assigned from a name-only hit; high-frequency names remain unresolved without cross-source context.
  - Next deterministic queue order is 301.
"""
assert needle in c
c = c.replace(needle, notes, 1)
cp.write_text(c, encoding="utf-8")

assert "code: W3-BATCH-0006" in sp.read_text(encoding="utf-8")
assert "current_gate: W3-BATCH-0006" in cp.read_text(encoding="utf-8")
print({"gate": "W3-BATCH-0005", "confirmed": confirmed, "unresolved": unresolved, "A": a_count, "B": b_count, "ledger_rows": len(led), "next": 301, "now": NOW})
