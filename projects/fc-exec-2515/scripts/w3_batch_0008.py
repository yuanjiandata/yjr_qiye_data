import csv, gzip
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evidence"
INPUT_HEAD = "a6ce82ac4806e9eeba2e7e6b197ae2c2cd63f5ff"
NOW = datetime.now(timezone(timedelta(hours=8))).replace(microsecond=0).isoformat()

with gzip.open(E / "W2_UNRESOLVED_QUEUE.csv.gz", "rt", encoding="utf-8-sig", newline="") as f:
    queue = list(csv.DictReader(f))[420:480]
assert [int(r["queue_order"]) for r in queue] == list(range(421, 481))
assert len(queue) == 60
assert all(r["province"] == "江苏" and r["priority"] == "P1_IDENTITY" for r in queue)

JS_TITLE = "江苏省工商业联合会第十二届常务委员会组成人员名单（2026年7月，共计121人）"
JS_URL = "https://www.jssh.org.cn/zzjg/fzxfhz/"
JS_EXEC_URL = "https://www.jssh.org.cn/sjb/bjczw/"
JS_DATE = "2026-07"

VICE_Q = set(range(421, 443)) | {448, 457, 464, 465, 474, 479}
STANDING_Q = {444,445,446,447,449,451,453,454,455,456,458,459,460,461,462,463,467,468,469,470,471,472,473}
UNRESOLVED = {450:"王红卫", 475:"孙振东", 476:"李建"}
SPECIAL = {
    452: ("王益冰","苏州市司法局","党组书记、局长","苏州市司法局领导信息",
          "https://sfj.suzhou.gov.cn/sfj/sfjldxx/202110/883a7d4b88954ba5943930fea4f87b6e.shtml","2026-07-21",
          "Official 2022 Jiangsu federation recommendation evidence identifies 王益冰 (1972-04) as 苏州市委统战部副部长、市工商联党组书记: https://www.jssh.org.cn/sjb/tzgg/202210/t20221014_214987.html. Current Suzhou Justice Bureau leadership evidence closes the role change without name-only inference."),
    477: ("李兰翔","盐城市人民政府","副市长","盐城市政协九届六十七次主席会议召开",
          "https://wap.yancheng.gov.cn/art/2026/9/4/art_49_4451545.html","2026-09-04",
          "ACFIC 2023 evidence identifies 李兰翔 as 江苏省政协副秘书长、省工商联副主席: https://www.acfic.org.cn/gdgslgz/js/bjgslgz/202304/t20230426_280633.html. Current Yancheng government evidence identifies her as 副市长; stale federation role is not carried forward."),
    478: ("李厚林","扬州市政协","经济科技委员会主任","企业敢说话 部门真回应——江苏扬州市政协“扬企有话讲”政企协商平台汇众智解难题",
          "https://www.cppcc.gov.cn/zxww/2026/04/20/ARTI1776648774943124.shtml","2026-04-20",
          "Jiangsu United Front/Yangzhou 2025 evidence identifies 李厚林 as 扬州市委统战部副部长、市工商联党组书记: https://www.jstz.gov.cn/a/20250317/1742175919732.shtml. Current CPPCC evidence identifies him as 扬州市政协经济科技委员会主任; identity is bridged by role history, not name alone."),
}
FIELDS = [
    "queue_order","person_id","province","excel_row","source_fragment","federation_role",
    "identity_resolution","candidate_names","repair_notes","evidence_type","evidence_grade",
    "evidence_title","evidence_url","evidence_date","current_organization","current_title",
    "current_verification_status","unresolved_reason",
]
results = []
for r in queue:
    q, name = int(r["queue_order"]), r["name_normalized"]
    out = {"queue_order":str(q),"person_id":r["person_id"],"province":r["province"],
           "excel_row":r["excel_row"],"source_fragment":name,"federation_role":r["federation_role"],
           "candidate_names":name,"current_organization":"","current_title":"","unresolved_reason":""}
    if q in SPECIAL:
        exp, org, title, etitle, url, edate, note = SPECIAL[q]
        assert name == exp
        out.update(identity_resolution="CURRENT_ROLE_CONFIRMED_WITH_ROLE_HISTORY_BRIDGE", repair_notes=note,
                   evidence_type="government_official", evidence_grade="A", evidence_title=etitle,
                   evidence_url=url, evidence_date=edate, current_organization=org, current_title=title,
                   current_verification_status="CURRENT_ORG_TITLE_CONFIRMED")
    elif q in UNRESOLVED:
        assert name == UNRESOLVED[q]
        if name == "王红卫":
            reason = "Absent from the latest July-2026 Jiangsu standing-committee roster and latest published executive roster. A current Jiangsu High Court official with the same name is a documented Tianjin-transferred jurist, so that homonym was explicitly rejected; no safe identity bridge to the source person was found."
        else:
            reason = f"{name} is absent from the latest July-2026 Jiangsu standing-committee roster and latest published executive roster; targeted public search found no current role that can be linked without name-only inference."
        out.update(identity_resolution="HISTORICAL_SOURCE_IDENTITY_CURRENT_ROLE_UNRESOLVED",
                   repair_notes=f"Checked current official roster {JS_URL} and latest published executive roster {JS_EXEC_URL}; stale 常委 was not carried forward.",
                   evidence_type="federation_official", evidence_grade="A", evidence_title=JS_TITLE,
                   evidence_url=JS_URL, evidence_date=JS_DATE,
                   current_verification_status="UNRESOLVED_CURRENT_ORG_TITLE", unresolved_reason=reason)
    else:
        if q in VICE_Q:
            org, title = "江苏省总商会", "副会长"
        elif q == 443:
            org, title = "江苏省工商业联合会 / 江苏省总商会", "副主席 / 副会长（兼）"
        elif q == 466:
            assert name == "刘聪"; org, title = "江苏省工商业联合会 / 江苏省总商会", "主席 / 会长"
        elif q == 480:
            assert name == "李晓林"; org, title = "江苏省工商业联合会 / 江苏省总商会", "副主席 / 副会长（兼）"
        else:
            assert q in STANDING_Q, (q, name); org, title = "江苏省工商业联合会", "常务委员"
        out.update(identity_resolution="CURRENT_ROLE_CONFIRMED_BY_LATEST_OFFICIAL_PROVINCIAL_ROSTER",
                   repair_notes="Name + province + source federation role reconcile to the official July-2026 Jiangsu standing-committee roster; higher current roles supersede stale source labels. No identity or employer was inferred from name alone.",
                   evidence_type="federation_official", evidence_grade="A", evidence_title=JS_TITLE,
                   evidence_url=JS_URL, evidence_date=JS_DATE, current_organization=org, current_title=title,
                   current_verification_status="CURRENT_ORG_TITLE_CONFIRMED")
    results.append(out)

with open(E / "W3_BATCH_0008_RESULTS.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n"); w.writeheader(); w.writerows(results)
LEDGER_FIELDS = ["queue_order","person_id","province","excel_row","candidate_names","evidence_type","evidence_grade","evidence_title","evidence_url","evidence_date","current_verification_status","unresolved_reason"]
OVERLAY_FIELDS = ["queue_order","person_id","province","excel_row","identity_resolution","candidate_names","current_organization","current_title","current_verification_status","evidence_grade","evidence_url","unresolved_reason"]
def append_rows(path, fields, rows):
    with open(path, "r", encoding="utf-8-sig", newline="") as f: old = list(csv.DictReader(f))
    last = int(old[-1]["queue_order"])
    if last == 480: return
    assert last == 420, (path, last)
    with open(path, "a", encoding="utf-8", newline="") as f:
        csv.DictWriter(f, fieldnames=fields, extrasaction="ignore", lineterminator="\n").writerows(rows)
append_rows(E / "W3_EVIDENCE_LEDGER.csv", LEDGER_FIELDS, results)
append_rows(E / "W3_VERIFICATION_OVERLAY.csv", OVERLAY_FIELDS, results)

confirmed = sum(r["current_verification_status"] == "CURRENT_ORG_TITLE_CONFIRMED" for r in results)
unresolved = 60 - confirmed
a_count = sum(r["evidence_grade"] == "A" for r in results)
b_count = sum(r["evidence_grade"] == "B" for r in results)
assert (confirmed, unresolved, a_count, b_count) == (57, 3, 60, 0)
assert all(r["evidence_url"] and r["evidence_title"] for r in results)
assert {int(r["queue_order"]) for r in results if r["current_verification_status"] != "CURRENT_ORG_TITLE_CONFIRMED"} == set(UNRESOLVED)
for p in [E / "W3_EVIDENCE_LEDGER.csv", E / "W3_VERIFICATION_OVERLAY.csv"]:
    with open(p, "r", encoding="utf-8-sig", newline="") as f: rows = list(csv.DictReader(f))
    assert len(rows) == 480 and [int(x["queue_order"]) for x in rows] == list(range(1, 481))

(E / "W3_BATCH_0008_METRICS.yaml").write_text(f"""schema: fc2515-w3-batch-metrics-v1
project_id: FC-EXEC-2515-01
gate: W3-BATCH-0008
status: PASS
queue_range: [421, 480]
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
  processed_queue_rows: 480
  actionable_queue_remaining: 10164
  next_queue_order: 481
  p0_processed: 101
  p0_remaining: 0
  p1_processed: 379
  p1_remaining: 3952
next_gate: W3-BATCH-0009
""", encoding="utf-8")
(E / "W3_BATCH_0008_VALIDATION.md").write_text(f"""# W3-BATCH-0008 Validation

Result: **PASS**

- Deterministic queue slice: 421–480 exactly, 60 江苏 P1_IDENTITY rows.
- Every touched row has public evidence or an explicit unresolved-current-role reason; unsupported current-title claims: 0.
- Current-state anchor: Jiangsu federation official roster labeled `2026年7月，共计121人`.
- 54 rows are directly present in that current roster; higher current roles supersede stale source labels. 徐志军 is now 副主席/省总商会副会长（兼）, not the old 秘书长 label.
- Three additional stale identities were closed with role-history bridges plus current official evidence: 王益冰→苏州市司法局党组书记、局长; 李兰翔→盐城市副市长; 李厚林→扬州市政协经济科技委员会主任.
- Three rows remain unresolved: 王红卫、孙振东、李建. They are absent from the current standing-committee roster and latest published executive roster; targeted search did not safely close identity/current role. The 江苏高院王红卫 homonym was explicitly rejected.
- Evidence grades: A={a_count}, B={b_count}, C=0; confirmed={confirmed}/60; unresolved={unresolved}/60.
- Cumulative evidence ledger and overlay each reconcile to 480 rows with queue_order 1..480 and no gaps.

Next deterministic gate: `W3-BATCH-0009`, starting queue_order 481.
""", encoding="utf-8")

sp = ROOT / "STATUS.yaml"
s = sp.read_text(encoding="utf-8")
s = s.replace("code: W3-BATCH-0007\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS", "code: W3-BATCH-0008\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS", 1)
s = s.replace("code: W3-BATCH-0008\n  phase: W3-EVIDENCE-ENRICH\n  status: READY", "code: W3-BATCH-0009\n  phase: W3-EVIDENCE-ENRICH\n  status: READY", 1)
for a, b in {
    "  batches_sealed: 7":"  batches_sealed: 8",
    "  processed_queue_rows: 420":"  processed_queue_rows: 480",
    "  next_queue_order: 421":"  next_queue_order: 481",
    "  actionable_queue_remaining: 10224":"  actionable_queue_remaining: 10164",
    "    processed: 319\n    remaining: 4012":"    processed: 379\n    remaining: 3952",
    "  identity_evidence_rows: 420":"  identity_evidence_rows: 480",
    "  current_org_title_confirmed_rows: 147":"  current_org_title_confirmed_rows: 204",
    "  current_org_title_unresolved_rows: 172":"  current_org_title_unresolved_rows: 175",
}.items():
    assert a in s, a
    s = s.replace(a, b, 1)
anchor = "  w3_batch_0007_validation: projects/fc-exec-2515/evidence/W3_BATCH_0007_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv"
rep = "  w3_batch_0007_validation: projects/fc-exec-2515/evidence/W3_BATCH_0007_VALIDATION.md\n  w3_batch_0008_results: projects/fc-exec-2515/evidence/W3_BATCH_0008_RESULTS.csv\n  w3_batch_0008_metrics: projects/fc-exec-2515/evidence/W3_BATCH_0008_METRICS.yaml\n  w3_batch_0008_validation: projects/fc-exec-2515/evidence/W3_BATCH_0008_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv"
assert anchor in s
sp.write_text(s.replace(anchor, rep, 1), encoding="utf-8")

cp = ROOT / "CURRENT.yaml"
c = cp.read_text(encoding="utf-8")
for a, b in {
    "current_gate: W3-BATCH-0008":"current_gate: W3-BATCH-0009",
    "work_cursor: 420":"work_cursor: 480",
    "verified_records: 147":"verified_records: 204",
    "unresolved_records: 10497":"unresolved_records: 10440",
    "last_input_head: 79603b7c559d0da203a0babc68608fe0b68a55e1":f"last_input_head: {INPUT_HEAD}",
    "  processed: 420":"  processed: 480",
    "  actionable_remaining: 10224":"  actionable_remaining: 10164",
    "  next_queue_order: 421":"  next_queue_order: 481",
    "      processed: 319\n      remaining: 4012":"      processed: 379\n      remaining: 3952",
}.items():
    assert a in c, a
    c = c.replace(a, b, 1)
lines = c.splitlines()
for i, line in enumerate(lines):
    if line.startswith("last_evidence_at:"):
        lines[i] = f"last_evidence_at: {NOW}"
        break
c = "\n".join(lines) + "\n"
batch = f"""
w3_batch_0008:
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
c = c.replace("\nnotes:\n", batch + "\nnotes:\n", 1)
needle = "  - Next deterministic queue order is 421.\n"
assert needle in c
notes = """  - Next deterministic queue order is 421.
  - W3-BATCH-0008 processed queue orders 421-480 exactly, all 江苏 P1 identity/current-role rows.
  - 57 rows received current organization/title confirmation; 3 remain explicitly unresolved (王红卫、孙振东、李建) because current evidence could not safely close identity/current role.
  - The July-2026 Jiangsu official roster was authoritative for current federation/chamber roles; stale source labels were not mechanically carried forward.
  - 王益冰、李兰翔、李厚林 were updated through role-history bridges plus current official sources; the 江苏高院王红卫 homonym was explicitly rejected rather than name-matched.
  - Next deterministic queue order is 481.
"""
c = c.replace(needle, notes, 1)
cp.write_text(c, encoding="utf-8")
assert "code: W3-BATCH-0009" in sp.read_text(encoding="utf-8")
assert "current_gate: W3-BATCH-0009" in cp.read_text(encoding="utf-8")
print({"gate":"W3-BATCH-0008","confirmed":confirmed,"unresolved":unresolved,
       "A":a_count,"B":b_count,"next":481,"now":NOW})
