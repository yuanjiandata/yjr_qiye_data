import csv, gzip
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evidence"
INPUT_HEAD = "edcf8f84c99298372ffa0dcf88facb12f7a31e37"
NOW = datetime.now(timezone(timedelta(hours=8))).replace(microsecond=0).isoformat()

with gzip.open(E / "W2_UNRESOLVED_QUEUE.csv.gz", "rt", encoding="utf-8-sig", newline="") as f:
    queue = list(csv.DictReader(f))[480:540]
assert len(queue) == 60
assert [int(r["queue_order"]) for r in queue] == list(range(481, 541))
assert all(r["province"] == "江苏" and r["priority"] == "P1_IDENTITY" for r in queue)

JS_TITLE = "江苏省工商业联合会第十二届常务委员会组成人员名单（2026年9月，共计120人）"
JS_URL = "https://www.jssh.org.cn/zzjg/fzxfhz/"
JS_DATE = "2026-09"

# Latest official roster roles for this deterministic queue slice.
FED_VICE = {485, 493, 495, 509, 514, 518, 520, 528, 538}
FED_AND_CHAMBER_VICE = {489, 540}
CHAMBER_VICE = {481, 487, 497, 508, 512, 515, 519, 522, 531, 533, 536, 539}
STANDING = {
    482,483,484,486,488,490,491,492,494,496,498,499,500,502,503,504,505,506,
    511,513,516,521,523,525,527,530,532,535,537
}
assert len(FED_VICE | FED_AND_CHAMBER_VICE | CHAMBER_VICE | STANDING) == 52

UNRESOLVED = {
    501: "张惠扬",
    507: "陈军",
    517: "周洁",
    524: "查艳",
}

SPECIAL = {
    510: {
        "name": "陈湘珍",
        "org": "盐城市人民政府台湾事务办公室",
        "title": "主任",
        "evidence_type": "government_official",
        "grade": "A",
        "evidence_title": "盐城市台协会召开换届大会 赖元皇连任会长",
        "url": "https://www.jsstb.gov.cn/yancheng/202601/t20260108_12745165.htm",
        "date": "2026-01-08",
        "bridge": "https://www.jssh.org.cn/xwzx/yw/202311/t20231113_217297.html",
        "note": "2023 Jiangsu federation evidence identifies the source person as 盐城市委统战部副部长、市工商联党组书记; 2026 Jiangsu Taiwan Affairs Office evidence identifies 陈湘珍 as 盐城市台办主任. Province + role history closes identity without a name-only match.",
    },
    529: {
        "name": "施勇",
        "org": "中共淮安市委统战部 / 淮安市社会主义学院",
        "title": "常务副部长 / 院长",
        "evidence_type": "government_official",
        "grade": "A",
        "evidence_title": "民盟淮安市委会2026年度盟务工作会议召开",
        "url": "https://www.jstz.gov.cn/a/20260411/177639529943.shtml",
        "date": "2026-04-11",
        "bridge": "https://www.jstz.gov.cn/a/20240923/1727406256514.shtml",
        "note": "2024 Jiangsu United Front evidence identifies the source person as 淮安市委统战部常务副部长、市社会主义学院院长、市工商联党组书记; 2026 evidence keeps the first two roles, while later federation evidence names a different 市工商联党组书记. The stale federation post is not carried forward.",
    },
    534: {
        "name": "顾万峰",
        "org": "中共江苏省委统战部",
        "title": "常务副部长",
        "evidence_type": "government_official",
        "grade": "A",
        "evidence_title": "省委统战部召开2026年离退休干部迎新春座谈会",
        "url": "https://www.jstz.gov.cn/a/20260210/1770689661221.shtml",
        "date": "2026-02-10",
        "bridge": "https://www.jstz.gov.cn/a/20230209/167592865682.shtml",
        "note": "2023 Jiangsu United Front evidence identifies 顾万峰 as 省委统战部副部长、省工商联党组书记; 2026 official evidence identifies him as 省委统战部常务副部长. The latest Sep-2026 federation roster names different current federation leadership, so the stale federation role is not retained.",
    },
}

NO_CURRENT_ROLE = {
    526: {
        "name": "钟雨",
        "evidence_type": "authoritative_media_official_filing_reproduction",
        "grade": "B",
        "evidence_title": "江苏洋河酒厂股份有限公司公告编号2026-003：关于公司总裁退休离任暨聘任总裁的公告（指定媒体全文转载）",
        "url": "https://finance.sina.com.cn/roll/2026-01-24/doc-inhiiucf6014952.shtml",
        "date": "2026-01-24",
        "bridge": "https://www.jstz.gov.cn/a/20250910/1757484098614.shtml",
        "note": "2025 Jiangsu United Front evidence identifies 江苏洋河酒厂股份有限公司党委副书记、总裁钟雨, closing the source identity with province/organization context. The reproduced listed-company filing states he retired and resigned all company roles, and would hold no other role in the company or controlled subsidiaries. No replacement current employer/title is inferred.",
    }
}

FIELDS = [
    "queue_order","person_id","province","excel_row","source_fragment","federation_role",
    "identity_resolution","candidate_names","repair_notes","evidence_type","evidence_grade",
    "evidence_title","evidence_url","evidence_date","current_organization","current_title",
    "current_verification_status","unresolved_reason",
]
results = []
for r in queue:
    q = int(r["queue_order"])
    name = r["name_normalized"]
    out = {
        "queue_order": str(q), "person_id": r["person_id"], "province": r["province"],
        "excel_row": r["excel_row"], "source_fragment": name, "federation_role": r["federation_role"],
        "candidate_names": name, "current_organization": "", "current_title": "", "unresolved_reason": ""
    }
    if q in SPECIAL:
        x = SPECIAL[q]
        assert name == x["name"]
        out.update(
            identity_resolution="CURRENT_ROLE_CONFIRMED_WITH_ROLE_HISTORY_BRIDGE",
            repair_notes=x["note"] + " Historical bridge: " + x["bridge"],
            evidence_type=x["evidence_type"], evidence_grade=x["grade"], evidence_title=x["evidence_title"],
            evidence_url=x["url"], evidence_date=x["date"], current_organization=x["org"],
            current_title=x["title"], current_verification_status="CURRENT_ORG_TITLE_CONFIRMED",
        )
    elif q in NO_CURRENT_ROLE:
        x = NO_CURRENT_ROLE[q]
        assert name == x["name"]
        out.update(
            identity_resolution="CURRENT_EMPLOYMENT_TERMINATION_CONFIRMED_WITH_ROLE_HISTORY_BRIDGE",
            repair_notes=x["note"] + " Historical bridge: " + x["bridge"],
            evidence_type=x["evidence_type"], evidence_grade=x["grade"], evidence_title=x["evidence_title"],
            evidence_url=x["url"], evidence_date=x["date"],
            current_verification_status="NO_CURRENT_ROLE_CONFIRMED",
        )
    elif q in UNRESOLVED:
        assert name == UNRESOLVED[q]
        reasons = {
            501: "张惠扬 is absent from the Sep-2026 Jiangsu standing-committee roster. Strong older evidence identifies him as 淮安市政协副主席、市工商联主席, but later official leadership/federation materials no longer support that as current; no safe current role was found.",
            507: "陈军 is absent from the Sep-2026 Jiangsu standing-committee roster. The name is highly non-unique and targeted public search returned multiple unrelated current identities; no province/federation/organization bridge safely closes a current role.",
            517: "周洁 is absent from the Sep-2026 Jiangsu standing-committee roster. Targeted public search did not produce a current organization/title that could be linked with province + federation-role context rather than name alone.",
            524: "查艳 is absent from the Sep-2026 Jiangsu standing-committee roster. Historical federation materials support the source identity, but no sufficiently current public evidence safely closes a present organization/title.",
        }
        out.update(
            identity_resolution="HISTORICAL_SOURCE_IDENTITY_CURRENT_ROLE_UNRESOLVED",
            repair_notes="Checked the latest official Sep-2026 Jiangsu federation roster; the stale 常委 label was not carried forward. No employer/title was assigned from a name-only search hit.",
            evidence_type="federation_official", evidence_grade="A", evidence_title=JS_TITLE,
            evidence_url=JS_URL, evidence_date=JS_DATE,
            current_verification_status="UNRESOLVED_CURRENT_ORG_TITLE", unresolved_reason=reasons[q],
        )
    else:
        assert q in FED_VICE | FED_AND_CHAMBER_VICE | CHAMBER_VICE | STANDING, (q, name)
        if q in FED_AND_CHAMBER_VICE:
            org, title = "江苏省工商业联合会 / 江苏省总商会", "副主席 / 副会长（兼）"
        elif q in FED_VICE:
            org, title = "江苏省工商业联合会", "副主席"
        elif q in CHAMBER_VICE:
            org, title = "江苏省总商会", "副会长"
        else:
            org, title = "江苏省工商业联合会", "常务委员"
        out.update(
            identity_resolution="CURRENT_ROLE_CONFIRMED_BY_LATEST_OFFICIAL_PROVINCIAL_ROSTER",
            repair_notes="Name + 江苏 source scope + federation role reconcile to the official Sep-2026 Jiangsu standing-committee roster. Current higher roles supersede stale source labels; no identity or employer was inferred from name alone.",
            evidence_type="federation_official", evidence_grade="A", evidence_title=JS_TITLE,
            evidence_url=JS_URL, evidence_date=JS_DATE, current_organization=org, current_title=title,
            current_verification_status="CURRENT_ORG_TITLE_CONFIRMED",
        )
    results.append(out)

# Deterministic gate validation before any repository state mutation.
assert len(results) == 60
assert [int(r["queue_order"]) for r in results] == list(range(481, 541))
assert len({r["person_id"] for r in results}) == 60
assert all(r["evidence_url"] and r["evidence_title"] and r["evidence_grade"] in {"A","B"} for r in results)
assert all(r["unresolved_reason"] for r in results if r["current_verification_status"] == "UNRESOLVED_CURRENT_ORG_TITLE")
assert all(r["current_organization"] and r["current_title"] for r in results if r["current_verification_status"] == "CURRENT_ORG_TITLE_CONFIRMED")
assert all(not r["current_organization"] and not r["current_title"] for r in results if r["current_verification_status"] == "NO_CURRENT_ROLE_CONFIRMED")
confirmed = sum(r["current_verification_status"] == "CURRENT_ORG_TITLE_CONFIRMED" for r in results)
unresolved = sum(r["current_verification_status"] == "UNRESOLVED_CURRENT_ORG_TITLE" for r in results)
no_role = sum(r["current_verification_status"] == "NO_CURRENT_ROLE_CONFIRMED" for r in results)
a_count = sum(r["evidence_grade"] == "A" for r in results)
b_count = sum(r["evidence_grade"] == "B" for r in results)
assert (confirmed, unresolved, no_role, a_count, b_count) == (55, 4, 1, 59, 1)
assert {int(r["queue_order"]) for r in results if r["current_verification_status"] == "UNRESOLVED_CURRENT_ORG_TITLE"} == set(UNRESOLVED)
assert {int(r["queue_order"]) for r in results if r["current_verification_status"] == "NO_CURRENT_ROLE_CONFIRMED"} == set(NO_CURRENT_ROLE)

with open(E / "W3_BATCH_0009_RESULTS.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n"); w.writeheader(); w.writerows(results)

LEDGER_FIELDS = ["queue_order","person_id","province","excel_row","candidate_names","evidence_type","evidence_grade","evidence_title","evidence_url","evidence_date","current_verification_status","unresolved_reason"]
OVERLAY_FIELDS = ["queue_order","person_id","province","excel_row","identity_resolution","candidate_names","current_organization","current_title","current_verification_status","evidence_grade","evidence_url","unresolved_reason"]

def append_rows(path, fields, rows):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        old = list(csv.DictReader(f))
    last = int(old[-1]["queue_order"])
    if last == 540:
        return
    assert last == 480, (path, last)
    with open(path, "a", encoding="utf-8", newline="") as f:
        csv.DictWriter(f, fieldnames=fields, extrasaction="ignore", lineterminator="\n").writerows(rows)

append_rows(E / "W3_EVIDENCE_LEDGER.csv", LEDGER_FIELDS, results)
append_rows(E / "W3_VERIFICATION_OVERLAY.csv", OVERLAY_FIELDS, results)

for p in [E / "W3_EVIDENCE_LEDGER.csv", E / "W3_VERIFICATION_OVERLAY.csv"]:
    with open(p, "r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 540
    assert [int(x["queue_order"]) for x in rows] == list(range(1, 541))
    assert len({x["queue_order"] for x in rows}) == 540

(E / "W3_BATCH_0009_METRICS.yaml").write_text(f"""schema: fc2515-w3-batch-metrics-v1
project_id: FC-EXEC-2515-01
gate: W3-BATCH-0009
status: PASS
queue_range: [481, 540]
batch_rows: 60
p1_identity_rows: 60
evidence_backed_rows: 60
a_grade_rows: {a_count}
b_grade_rows: {b_count}
structural_deferred_rows: 0
current_org_title_confirmed_rows: {confirmed}
no_current_role_confirmed_rows: {no_role}
current_org_title_unresolved_rows: {unresolved}
unsupported_current_title_claims: 0
post_batch:
  processed_queue_rows: 540
  actionable_queue_remaining: 10104
  next_queue_order: 541
  p0_processed: 101
  p0_remaining: 0
  p1_processed: 439
  p1_remaining: 3892
next_gate: W3-BATCH-0010
""", encoding="utf-8")

(E / "W3_BATCH_0009_VALIDATION.md").write_text(f"""# W3-BATCH-0009 Validation

Result: **PASS**

- Deterministic queue slice: 481–540 exactly, 60 江苏 P1_IDENTITY rows.
- Every touched row has public evidence or an explicit unresolved-current-role reason; unsupported current-title claims: 0.
- Current-state anchor: Jiangsu federation official roster labeled `2026年9月，共计120人`, superseding the July roster used by the prior batch.
- 52 rows are directly present in that latest roster and receive their current federation/chamber role from the official page.
- Three stale federation identities are closed by role-history bridge plus current A-grade official evidence: 陈湘珍→盐城市台办主任; 施勇→淮安市委统战部常务副部长/市社会主义学院院长; 顾万峰→江苏省委统战部常务副部长.
- 钟雨 is separately resolved as `NO_CURRENT_ROLE_CONFIRMED`: 2025 official Jiangsu evidence identifies him as 洋河党委副书记、总裁, while the reproduced listed-company announcement 2026-003 states that he retired and resigned all company roles and would hold no role in the company or controlled subsidiaries. No new employer/title is inferred.
- Four rows remain unresolved: 张惠扬、陈军、周洁、查艳. They are absent from the Sep-2026 roster and targeted search did not safely close a present role without name-only inference.
- Evidence grades: A={a_count}, B={b_count}, C=0; current organization/title confirmed={confirmed}/60; no-current-role confirmed={no_role}/60; unresolved={unresolved}/60.
- Cumulative evidence ledger and verification overlay each reconcile to 540 rows with queue_order 1..540 and no gaps or duplicate queue orders.

Next deterministic gate: `W3-BATCH-0010`, starting queue_order 541.
""", encoding="utf-8")

# Update repository state truth only after deterministic evidence validation passes.
sp = ROOT / "STATUS.yaml"
s = sp.read_text(encoding="utf-8")
repls = {
    "code: W3-BATCH-0008\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS": "code: W3-BATCH-0009\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS",
    "code: W3-BATCH-0009\n  phase: W3-EVIDENCE-ENRICH\n  status: READY": "code: W3-BATCH-0010\n  phase: W3-EVIDENCE-ENRICH\n  status: READY",
    "  batches_sealed: 8": "  batches_sealed: 9",
    "  processed_queue_rows: 480": "  processed_queue_rows: 540",
    "  next_queue_order: 481": "  next_queue_order: 541",
    "  actionable_queue_remaining: 10164": "  actionable_queue_remaining: 10104",
    "    processed: 379\n    remaining: 3952": "    processed: 439\n    remaining: 3892",
    "  identity_evidence_rows: 480": "  identity_evidence_rows: 540",
    "  current_org_title_confirmed_rows: 204": "  current_org_title_confirmed_rows: 259",
    "  current_org_title_unresolved_rows: 175": "  current_org_title_unresolved_rows: 179\n  no_current_role_confirmed_rows: 1",
}
for a,b in repls.items():
    assert a in s, a
    s = s.replace(a,b,1)
anchor = "  w3_batch_0008_validation: projects/fc-exec-2515/evidence/W3_BATCH_0008_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv"
rep = "  w3_batch_0008_validation: projects/fc-exec-2515/evidence/W3_BATCH_0008_VALIDATION.md\n  w3_batch_0009_results: projects/fc-exec-2515/evidence/W3_BATCH_0009_RESULTS.csv\n  w3_batch_0009_metrics: projects/fc-exec-2515/evidence/W3_BATCH_0009_METRICS.yaml\n  w3_batch_0009_validation: projects/fc-exec-2515/evidence/W3_BATCH_0009_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv"
assert anchor in s
sp.write_text(s.replace(anchor,rep,1), encoding="utf-8")

cp = ROOT / "CURRENT.yaml"
c = cp.read_text(encoding="utf-8")
for a,b in {
    "current_gate: W3-BATCH-0009": "current_gate: W3-BATCH-0010",
    "work_cursor: 480": "work_cursor: 540",
    "verified_records: 204": "verified_records: 260",
    "unresolved_records: 10440": "unresolved_records: 10384",
    "last_evidence_at: 2026-09-20T06:50:33+08:00": f"last_evidence_at: {NOW}",
    "last_input_head: a6ce82ac4806e9eeba2e7e6b197ae2c2cd63f5ff": f"last_input_head: {INPUT_HEAD}",
    "  processed: 480": "  processed: 540",
    "  actionable_remaining: 10164": "  actionable_remaining: 10104",
    "  next_queue_order: 481": "  next_queue_order: 541",
    "      processed: 379\n      remaining: 3952": "      processed: 439\n      remaining: 3892",
}.items():
    assert a in c, a
    c = c.replace(a,b,1)

section = f"""
w3_batch_0009:
  status: SEALED
  validation: PASS
  touched_rows: 60
  p1_identity_rows: 60
  evidence_backed_rows: 60
  a_grade_rows: {a_count}
  b_grade_rows: {b_count}
  current_org_title_confirmed_rows: {confirmed}
  no_current_role_confirmed_rows: {no_role}
  current_org_title_unresolved_rows: {unresolved}
  unsupported_current_title_claims: 0

"""
assert "\nnotes:\n" in c
c = c.replace("\nnotes:\n", "\n" + section + "notes:\n", 1)
notes_anchor = "  - Next deterministic queue order is 481.\n"
notes_add = """  - W3-BATCH-0009 processed queue orders 481-540 exactly, all 江苏 P1 identity/current-role rows.
  - The live Jiangsu federation roster advanced again to September 2026 (120 members), and this newer roster superseded July labels for current federation/chamber roles.
  - 55 rows received current organization/title confirmation: 52 directly from the latest roster plus 陈湘珍、施勇、顾万峰 via historical identity bridges and current official-role evidence.
  - 钟雨 is evidence-resolved as NO_CURRENT_ROLE_CONFIRMED after listed-company announcement 2026-003 documented retirement and resignation from all company roles; no replacement employer/title was invented.
  - 张惠扬、陈军、周洁、查艳 remain explicit current-role unresolved cases; name-only search hits were rejected.
  - Next deterministic queue order is 541.
"""
assert notes_anchor in c
c = c.replace(notes_anchor, notes_anchor + notes_add, 1)
cp.write_text(c, encoding="utf-8")

# Final deterministic read-back validation of all state artifacts.
assert "latest_gate:\n  code: W3-BATCH-0009" in sp.read_text(encoding="utf-8")
assert "next_gate:\n  code: W3-BATCH-0010" in sp.read_text(encoding="utf-8")
ct = cp.read_text(encoding="utf-8")
assert "current_gate: W3-BATCH-0010" in ct and "work_cursor: 540" in ct
assert "next_queue_order: 541" in ct and "processed: 540" in ct
print(f"PASS W3-BATCH-0009 confirmed={confirmed} no_current_role={no_role} unresolved={unresolved} A={a_count} B={b_count} now={NOW}")
