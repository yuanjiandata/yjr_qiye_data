import csv, gzip, glob
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evidence"
INPUT_HEAD = "79603b7c559d0da203a0babc68608fe0b68a55e1"
NOW = datetime.now(timezone(timedelta(hours=8))).replace(microsecond=0).isoformat()

with gzip.open(E / "W2_UNRESOLVED_QUEUE.csv.gz", "rt", encoding="utf-8-sig", newline="") as f:
    queue = list(csv.DictReader(f))[360:420]
assert [int(r["queue_order"]) for r in queue] == list(range(361, 421))
assert all(r["priority"] == "P1_IDENTITY" for r in queue)
assert sum(r["province"] == "吉林" for r in queue) == 7
assert sum(r["province"] == "江苏" for r in queue) == 53

JS = (
    "federation_official", "A", "江苏省工商业联合会第十二届常务委员会组成人员名单（2026年7月，共计121人）",
    "https://www.jssh.org.cn/zzjg/fzxfhz/", "2026-07",
)
JS_SOURCE = JS[3]
JS_UNRESOLVED = {373:"郭东升", 374:"熊杰", 399:"顾万峰", 401:"郭东升", 402:"熊杰", 404:"李兰翔"}

JS_ROLES = {
    "刘聪": ("江苏省工商业联合会 / 江苏省总商会", "主席 / 会长"),
    "周海江": ("江苏省工商业联合会", "副主席"),
    "沈彬": ("江苏省工商业联合会", "副主席"),
    "崔根良": ("江苏省工商业联合会", "副主席"),
    "李晓林": ("江苏省工商业联合会 / 江苏省总商会", "副主席 / 副会长（兼）"),
    "吴卫东": ("江苏省工商业联合会 / 江苏省总商会", "副主席 / 副会长（兼）"),
    "陈建华": ("江苏省工商业联合会", "副主席"),
    "缪汉根": ("江苏省工商业联合会", "副主席"),
    "肖伟": ("江苏省工商业联合会", "副主席"),
    "蒋立": ("江苏省工商业联合会", "副主席"),
    "周江": ("江苏省工商业联合会", "副主席"),
    "昝圣达": ("江苏省工商业联合会", "副主席"),
    "殷爱国": ("江苏省工商业联合会", "副主席"),
    "蒋东良": ("江苏省工商业联合会", "副主席"),
    "周立成": ("江苏省工商业联合会", "副主席"),
    "徐翔": ("江苏省工商业联合会", "副主席"),
    "吴培服": ("江苏省工商业联合会", "副主席"),
    "孙力斌": ("江苏省总商会", "副会长"),
    "周荣": ("江苏省总商会", "副会长"),
    "周立宸": ("江苏省总商会", "副会长"),
    "单建华": ("江苏省总商会", "副会长"),
    "宫长义": ("江苏省总商会", "副会长"),
    "袁永刚": ("江苏省总商会", "副会长"),
    "缪文彬": ("江苏省总商会", "副会长"),
    "薛驰": ("江苏省总商会", "副会长"),
    "王卫": ("江苏省总商会", "副会长"),
    "王燕清": ("江苏省总商会", "副会长"),
    "朱钰峰": ("江苏省总商会", "副会长"),
}

prior = {}
for path in sorted(glob.glob(str(E / "W3_BATCH_000*_RESULTS.csv"))):
    if path.endswith("W3_BATCH_0007_RESULTS.csv"):
        continue
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            prior[int(row["queue_order"])] = row

PREV_REUSE = {363:358, 364:359, 365:360}
for target_q, source_q in PREV_REUSE.items():
    assert source_q in prior
    assert prior[source_q]["current_verification_status"] == "CURRENT_ORG_TITLE_CONFIRMED"
    target_name = next(r["name_normalized"] for r in queue if int(r["queue_order"]) == target_q)
    assert prior[source_q]["source_fragment"] == target_name

JILIN_FRESH = {
    361: ("authoritative_media", "B", "吉林省陕西商会第三届换届选举大会圆满召开",
          "https://news.cnjiwang.com/jwyc/202605/4051609.html", "2026-05-31",
          "吉林省工商业联合会", "副主席",
          "Current 2026 China Jilin Network coverage explicitly identifies 徐朝春 as 吉林省工商联副主席. The 2022 provincial federation election roster cross-lists him as provincial federation vice-chair and provincial chamber vice-chair, so the two source-role rows are the same identity without merging person_ids."),
    362: ("authoritative_media", "B", "吉林省光彩事业促进会第三次会员代表大会隆重召开 步长制药赵菁当选促进会副会长",
          "https://finance.sina.com.cn/roll/2026-09-18/doc-inisfprh8538016.shtml", "2026-09-18",
          "吉林省工商业联合会", "副主席",
          "Fresh 2026-09-18 International Financial News coverage explicitly identifies 李武华 as 吉林省工商联副主席. The 2022 provincial federation election roster cross-lists him as provincial federation vice-chair and provincial chamber vice-chair, so the two source-role rows are the same identity without merging person_ids."),
}
JILIN_CROSS = {366:361, 367:362}

FIELDS = [
    "queue_order","person_id","province","excel_row","source_fragment","federation_role",
    "identity_resolution","candidate_names","repair_notes","evidence_type","evidence_grade",
    "evidence_title","evidence_url","evidence_date","current_organization","current_title",
    "current_verification_status","unresolved_reason",
]
results = []
by_q = {}
for r in queue:
    q = int(r["queue_order"])
    name = r["name_normalized"]
    out = {
        "queue_order":str(q),"person_id":r["person_id"],"province":r["province"],
        "excel_row":r["excel_row"],"source_fragment":name,"federation_role":r["federation_role"],
        "candidate_names":name,"current_organization":"","current_title":"","unresolved_reason":"",
    }
    if q in PREV_REUSE:
        src = prior[PREV_REUSE[q]]
        out.update(
            identity_resolution="CURRENT_ROLE_REUSED_WITH_PROVINCIAL_ROLE_CROSSLIST",
            repair_notes=f"Same 吉林 federation leader is cross-listed under federation/chamber roles; reused sealed current-role evidence from W3 queue {PREV_REUSE[q]} without merging person_ids. " + src["repair_notes"],
            evidence_type=src["evidence_type"], evidence_grade=src["evidence_grade"],
            evidence_title=src["evidence_title"], evidence_url=src["evidence_url"], evidence_date=src["evidence_date"],
            current_organization=src["current_organization"], current_title=src["current_title"],
            current_verification_status="CURRENT_ORG_TITLE_CONFIRMED",
        )
    elif q in JILIN_FRESH:
        typ, grade, etitle, url, edate, org, title, note = JILIN_FRESH[q]
        out.update(
            identity_resolution="CURRENT_PUBLIC_ROLE_IDENTIFIED",
            repair_notes=note, evidence_type=typ, evidence_grade=grade,
            evidence_title=etitle, evidence_url=url, evidence_date=edate,
            current_organization=org, current_title=title,
            current_verification_status="CURRENT_ORG_TITLE_CONFIRMED",
        )
    elif q in JILIN_CROSS:
        src = by_q[JILIN_CROSS[q]]
        assert src["source_fragment"] == name
        out.update(
            identity_resolution="CURRENT_ROLE_REUSED_WITH_PROVINCIAL_ROLE_CROSSLIST",
            repair_notes=f"Same 吉林 federation leader is cross-listed in the source under federation and chamber roles; reused the same-batch current-role evidence from queue {JILIN_CROSS[q]} without merging person_ids. " + src["repair_notes"],
            evidence_type=src["evidence_type"], evidence_grade=src["evidence_grade"],
            evidence_title=src["evidence_title"], evidence_url=src["evidence_url"], evidence_date=src["evidence_date"],
            current_organization=src["current_organization"], current_title=src["current_title"],
            current_verification_status="CURRENT_ORG_TITLE_CONFIRMED",
        )
    elif r["province"] == "江苏":
        typ, grade, etitle, url, edate = JS
        if q in JS_UNRESOLVED:
            assert JS_UNRESOLVED[q] == name
            if name == "顾万峰":
                reason = "The source carries the former 常务副主席 role, but the latest official July 2026 Jiangsu federation leadership roster names 刘军 as current 常务副主席; no sufficiently current authoritative evidence safely establishes 顾万峰's present organization/title."
            else:
                reason = f"{name} appears in the older source role but is absent from the latest official July 2026 Jiangsu federation standing-committee/leadership roster; targeted current-role search did not produce sufficiently fresh authoritative evidence to assign a present organization/title safely."
            out.update(
                identity_resolution="HISTORICAL_IDENTITY_ANCHORED_CURRENT_ROLE_UNRESOLVED",
                repair_notes="Latest official Jiangsu federation roster was used as the current-state authority; stale source role was not carried forward.",
                evidence_type=typ, evidence_grade=grade, evidence_title=etitle, evidence_url=url, evidence_date=edate,
                current_verification_status="UNRESOLVED_CURRENT_ORG_TITLE", unresolved_reason=reason,
            )
        else:
            assert name in JS_ROLES, (q, name)
            org, title = JS_ROLES[name]
            out.update(
                identity_resolution="CURRENT_ROLE_CONFIRMED_BY_LATEST_OFFICIAL_PROVINCIAL_ROSTER",
                repair_notes="Name + province + federation/chamber role match the latest official July 2026 Jiangsu provincial federation standing-committee roster; no name-only employer inference was used.",
                evidence_type=typ, evidence_grade=grade, evidence_title=etitle, evidence_url=url, evidence_date=edate,
                current_organization=org, current_title=title,
                current_verification_status="CURRENT_ORG_TITLE_CONFIRMED",
            )
    else:
        raise AssertionError((q, r["province"], name))
    results.append(out)
    by_q[q] = out

with open(E / "W3_BATCH_0007_RESULTS.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
    w.writeheader(); w.writerows(results)
LEDGER_FIELDS = ["queue_order","person_id","province","excel_row","candidate_names","evidence_type","evidence_grade","evidence_title","evidence_url","evidence_date","current_verification_status","unresolved_reason"]
OVERLAY_FIELDS = ["queue_order","person_id","province","excel_row","identity_resolution","candidate_names","current_organization","current_title","current_verification_status","evidence_grade","evidence_url","unresolved_reason"]

def append_rows(path, fields, rows):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        old = list(csv.DictReader(f))
    last = int(old[-1]["queue_order"])
    if last == 420:
        return
    assert last == 360, (path, last)
    with open(path, "a", encoding="utf-8", newline="") as f:
        csv.DictWriter(f, fieldnames=fields, extrasaction="ignore", lineterminator="\n").writerows(rows)

append_rows(E / "W3_EVIDENCE_LEDGER.csv", LEDGER_FIELDS, results)
append_rows(E / "W3_VERIFICATION_OVERLAY.csv", OVERLAY_FIELDS, results)

confirmed = sum(r["current_verification_status"] == "CURRENT_ORG_TITLE_CONFIRMED" for r in results)
unresolved = 60 - confirmed
a_count = sum(r["evidence_grade"] == "A" for r in results)
b_count = sum(r["evidence_grade"] == "B" for r in results)
assert confirmed == 54 and unresolved == 6, (confirmed, unresolved)
assert a_count + b_count == 60
assert all(r["evidence_url"] and r["evidence_title"] for r in results)
assert all((r["current_organization"] and r["current_title"] and not r["unresolved_reason"]) if r["current_verification_status"] == "CURRENT_ORG_TITLE_CONFIRMED" else (not r["current_organization"] and not r["current_title"] and bool(r["unresolved_reason"])) for r in results)
assert {int(r["queue_order"]) for r in results if r["current_verification_status"] != "CURRENT_ORG_TITLE_CONFIRMED"} == set(JS_UNRESOLVED)
with open(E / "W3_EVIDENCE_LEDGER.csv", "r", encoding="utf-8-sig", newline="") as f:
    led = list(csv.DictReader(f))
with open(E / "W3_VERIFICATION_OVERLAY.csv", "r", encoding="utf-8-sig", newline="") as f:
    ov = list(csv.DictReader(f))
assert len(led) == 420 and len(ov) == 420
assert [int(x["queue_order"]) for x in led] == list(range(1, 421))
assert [int(x["queue_order"]) for x in ov] == list(range(1, 421))

(E / "W3_BATCH_0007_METRICS.yaml").write_text(f"""schema: fc2515-w3-batch-metrics-v1
project_id: FC-EXEC-2515-01
gate: W3-BATCH-0007
status: PASS
queue_range: [361, 420]
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
  processed_queue_rows: 420
  actionable_queue_remaining: 10224
  next_queue_order: 421
  p0_processed: 101
  p0_remaining: 0
  p1_processed: 319
  p1_remaining: 4012
next_gate: W3-BATCH-0008
""", encoding="utf-8")
(E / "W3_BATCH_0007_VALIDATION.md").write_text(f"""# W3-BATCH-0007 Validation

Result: **PASS**

- Deterministic queue slice: 361–420 exactly, 60 rows; 7 吉林 + 53 江苏, all P1_IDENTITY.
- Every touched row has public evidence or an explicit unresolved-current-role reason.
- Latest repository-defined source identities were reconciled against public current evidence; no identity was inferred from name alone.
- The official Jiangsu federation page is currently labeled `2026年7月，共计121人` and was used as the current-state authority for Jiangsu federation/chamber roles.
- 47/53 Jiangsu rows are present in that latest official roster and received a current federation/chamber organization + title; 6 rows (郭东升 x2, 熊杰 x2, 顾万峰, 李兰翔) remain unresolved because the stale source role is not supported by the latest official roster.
- 顾万峰 was not carried forward as 常务副主席: the July 2026 official roster names 刘军 as current 常务副主席.
- 吉林 current roles were refreshed with 2026 evidence; 李维斗、唐庆会、吕兵 reuse prior sealed current evidence, while 徐朝春、李武华 use fresh 2026 sources and source-role cross-listing without person_id merge.
- Evidence grades in batch: A={a_count}, B={b_count}; C=0.
- Current organization + title confirmed: {confirmed}/60.
- Current-role unresolved: {unresolved}/60; unresolved organization/title fields remain blank rather than guessed.
- Cumulative W3 evidence ledger and verification overlay each reconcile to 420 rows with queue_order 1..420 and no gaps.
- Unsupported current-title claims: 0.

Next deterministic gate: `W3-BATCH-0008`, starting queue_order 421.
""", encoding="utf-8")

sp = ROOT / "STATUS.yaml"
s = sp.read_text(encoding="utf-8")
s = s.replace("code: W3-BATCH-0006\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS", "code: W3-BATCH-0007\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS", 1)
s = s.replace("code: W3-BATCH-0007\n  phase: W3-EVIDENCE-ENRICH\n  status: READY", "code: W3-BATCH-0008\n  phase: W3-EVIDENCE-ENRICH\n  status: READY", 1)
for a, b in {
    "  batches_sealed: 6":"  batches_sealed: 7",
    "  processed_queue_rows: 360":"  processed_queue_rows: 420",
    "  next_queue_order: 361":"  next_queue_order: 421",
    "  actionable_queue_remaining: 10284":"  actionable_queue_remaining: 10224",
    "    processed: 259\n    remaining: 4072":"    processed: 319\n    remaining: 4012",
    "  identity_evidence_rows: 360":"  identity_evidence_rows: 420",
    "  current_org_title_confirmed_rows: 93":f"  current_org_title_confirmed_rows: {93+confirmed}",
    "  current_org_title_unresolved_rows: 166":f"  current_org_title_unresolved_rows: {166+unresolved}",
}.items():
    assert a in s, a
    s = s.replace(a, b, 1)
anchor = "  w3_batch_0006_validation: projects/fc-exec-2515/evidence/W3_BATCH_0006_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv"
rep = "  w3_batch_0006_validation: projects/fc-exec-2515/evidence/W3_BATCH_0006_VALIDATION.md\n  w3_batch_0007_results: projects/fc-exec-2515/evidence/W3_BATCH_0007_RESULTS.csv\n  w3_batch_0007_metrics: projects/fc-exec-2515/evidence/W3_BATCH_0007_METRICS.yaml\n  w3_batch_0007_validation: projects/fc-exec-2515/evidence/W3_BATCH_0007_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv"
assert anchor in s
s = s.replace(anchor, rep, 1)
sp.write_text(s, encoding="utf-8")

cp = ROOT / "CURRENT.yaml"
c = cp.read_text(encoding="utf-8")
c = c.replace("current_gate: W3-BATCH-0007", "current_gate: W3-BATCH-0008", 1)
c = c.replace("work_cursor: 360", "work_cursor: 420", 1)
for a, b in {
    "verified_records: 93":f"verified_records: {93+confirmed}",
    "unresolved_records: 10551":f"unresolved_records: {10551-confirmed}",
    "last_input_head: 91e538e53ce08ab46c1c06e4e27282e55bd58330":f"last_input_head: {INPUT_HEAD}",
    "  processed: 360":"  processed: 420",
    "  actionable_remaining: 10284":"  actionable_remaining: 10224",
    "  next_queue_order: 361":"  next_queue_order: 421",
    "      processed: 259\n      remaining: 4072":"      processed: 319\n      remaining: 4012",
}.items():
    assert a in c, a
    c = c.replace(a, b, 1)
lines = c.splitlines()
for i, line in enumerate(lines):
    if line.startswith("last_evidence_at:"):
        lines[i] = f"last_evidence_at: {NOW}"
        break
c = "\n".join(lines) + "\n"
b7 = f"""
w3_batch_0007:
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
c = c.replace("\nnotes:\n", b7 + "\nnotes:\n", 1)
needle = "  - Next deterministic queue order is 361.\n"
notes = f"""  - Next deterministic queue order is 361.
  - W3-BATCH-0007 processed queue orders 361-420 exactly: 7 吉林 + 53 江苏 P1 identity/current-role rows.
  - {confirmed} rows received current organization/title confirmation; {unresolved} remain explicitly unresolved where latest current evidence contradicts or no longer supports the stale source role.
  - The live Jiangsu federation official roster is labeled July 2026 and supersedes the older source list for current federation/chamber-role claims.
  - 郭东升、熊杰、顾万峰、李兰翔 source roles were not carried forward when unsupported by the latest Jiangsu official roster; 顾万峰 in particular was not retained as 常务副主席 because the current roster names 刘军.
  - 吉林 leadership claims were refreshed from 2026 evidence; cross-listed source rows reuse evidence without person_id merge.
  - Next deterministic queue order is 421.
"""
assert needle in c
c = c.replace(needle, notes, 1)
cp.write_text(c, encoding="utf-8")

assert "code: W3-BATCH-0008" in sp.read_text(encoding="utf-8")
assert "current_gate: W3-BATCH-0008" in cp.read_text(encoding="utf-8")
print({"gate":"W3-BATCH-0007","confirmed":confirmed,"unresolved":unresolved,"A":a_count,"B":b_count,"ledger_rows":len(led),"next":421,"now":NOW})
