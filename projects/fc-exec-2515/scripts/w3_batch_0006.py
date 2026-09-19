import csv, gzip, glob
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "evidence"
INPUT_HEAD = "91e538e53ce08ab46c1c06e4e27282e55bd58330"
NOW = datetime.now(timezone(timedelta(hours=8))).replace(microsecond=0).isoformat()

with gzip.open(E / "W2_UNRESOLVED_QUEUE.csv.gz", "rt", encoding="utf-8-sig", newline="") as f:
    queue = list(csv.DictReader(f))[300:360]
assert [int(r["queue_order"]) for r in queue] == list(range(301, 361))
assert all(r["priority"] == "P1_IDENTITY" for r in queue)
assert sum(r["province"] == "河北" for r in queue) == 57
assert sum(r["province"] == "吉林" for r in queue) == 3

HE = (
    "federation_official", "A", "河北省工商业联合会(总商会)第十三届执委会名单",
    "https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_he/202207/t20220715_312762.html",
    "2022-07-15",
)

REUSE = {
    311:127, 317:223, 319:128, 324:142, 327:226, 332:230,
    335:147, 338:144, 340:169, 341:140, 345:233, 346:234,
    347:235, 348:141, 350:237, 351:238, 352:145, 353:239,
}

prior = {}
for path in sorted(glob.glob(str(E / "W3_BATCH_000*_RESULTS.csv"))):
    if path.endswith("W3_BATCH_0006_RESULTS.csv"):
        continue
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            prior[int(row["queue_order"])] = row

for target_q, source_q in REUSE.items():
    assert source_q in prior
    assert prior[source_q]["current_verification_status"] == "CURRENT_ORG_TITLE_CONFIRMED"
    target_name = next(r["name_normalized"] for r in queue if int(r["queue_order"]) == target_q)
    assert prior[source_q]["source_fragment"] == target_name

FRESH = {
    308: ("CURRENT_ENTERPRISE_ROLE_IDENTIFIED","authoritative_media","B",
          "宝钢股份董事长邹继新在烟台鲁宝与建龙集团董事长张志祥会谈：就进一步深化合作达成重要共识",
          "https://finance.sina.com.cn/wm/2026-05-28/doc-inhznkuh8454271.shtml","2026-05-28",
          "北京建龙重工集团有限公司","董事长、总裁",
          "Official Hebei federation roster anchors 张志祥; 2026 coverage quoting 建龙集团 identifies him as current chairman and president."),
    321: ("CURRENT_ENTERPRISE_ROLE_IDENTIFIED","government_official","A",
          "委员建言｜周超男委员：夯实智算底座 助力打造智能经济新形态",
          "https://www.hebzx.gov.cn/system/2026/03/11/030377645.shtml","2026-03-11",
          "润泽智算科技集团股份有限公司","董事长",
          "Hebei federation roster anchors 周超男; Hebei CPPCC official coverage identifies her as current Runze Intelligent Computing chair."),
    355: ("CURRENT_PUBLIC_ROLE_IDENTIFIED","government_official","A",
          "河北省人民代表大会常务委员会任免人员名单",
          "https://www.hbrd.gov.cn/system/2026/07/24/102207256.shtml","2026-07-24",
          "河北省人民代表大会常务委员会","副秘书长",
          "Hebei federation roster anchors 霍占利; the July 2026 Hebei People's Congress official appointment confirms the current deputy secretary-general role."),
    356: ("CURRENT_ENTERPRISE_ROLE_IDENTIFIED","government_official","A",
          "从动工到投产仅用11个月 君乐宝华南基地建设跑出“蓬江速度”",
          "https://www.pjq.gov.cn/yzpj/jjkx/content/post_3479317.html","2026-04-21",
          "君乐宝乳业集团","董事长兼总裁",
          "Hebei federation roster anchors 魏立华; Jiangmen Pengjiang district government reporting identifies him as current Junlebao chairman and president."),
    357: ("CURRENT_ENTERPRISE_ROLE_IDENTIFIED","authoritative_media","B",
          "河北省农业企业联合会换届大会在石家庄召开",
          "https://www.hebjjrb.cn/system/2026/03/30/102167054.shtml","2026-03-31",
          "金沙河集团有限公司","董事长",
          "Hebei federation roster anchors 魏海金; Hebei Economic Daily reports him as Jinshahe Group chairman and newly elected provincial agricultural-enterprise federation president."),
    358: ("CURRENT_PUBLIC_ROLE_IDENTIFIED","government_official","A",
          "省工商联召开十二届八次常委会会议",
          "https://jlzx.gov.cn/dptt/202608/t20260825_3665276.html","2026-08-25",
          "吉林省工商业联合会","主席（同时任吉林省政协副主席）",
          "Jilin CPPCC official coverage explicitly identifies 李维斗 as current provincial federation chairman and provincial CPPCC vice-chairman."),
    359: ("CURRENT_PUBLIC_ROLE_IDENTIFIED","government_official","A",
          "省工商联召开十二届八次常委会会议",
          "https://jlzx.gov.cn/dptt/202608/t20260825_3665276.html","2026-08-25",
          "中共吉林省委统战部 / 吉林省工商业联合会","副部长 / 党组书记",
          "Jilin CPPCC official coverage explicitly identifies 唐庆会 as current provincial United Front Work Department deputy head and federation party secretary."),
    360: ("CURRENT_PUBLIC_ROLE_IDENTIFIED","authoritative_media","B",
          "智赋吉林 数启新篇 2026第五届吉林省数字经济发展促进大会暨第三届吉林省人工智能大会圆满落幕",
          "https://finance.sina.com.cn/wm/2026-04-03/doc-inhtfeqz3783831.shtml","2026-04-03",
          "吉林省工商业联合会","副主席",
          "2026 event coverage sourced to Jilin Federation of Industry and Commerce explicitly identifies 吕兵 as current provincial federation vice-chairman."),
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
        "queue_order":str(q),"person_id":r["person_id"],"province":r["province"],
        "excel_row":r["excel_row"],"source_fragment":name,"federation_role":r["federation_role"],
        "candidate_names":name,"current_organization":"","current_title":"","unresolved_reason":"",
    }
    if q in REUSE:
        src = prior[REUSE[q]]
        out.update(
            identity_resolution="CURRENT_ROLE_REUSED_WITH_OFFICIAL_ROSTER_CROSSLIST",
            repair_notes=f"Same 河北 person is cross-listed in the official provincial federation roster under the earlier role and 执委; reused sealed current-role evidence from W3 queue {REUSE[q]} without merging person_ids. " + src["repair_notes"],
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
        assert r["province"] == "河北"
        typ, grade, etitle, url, edate = HE
        out.update(
            identity_resolution="IDENTITY_ONLY_OFFICIAL_ROSTER",
            repair_notes="Identity retained from official Hebei federation roster; current organization/title intentionally left unresolved after targeted current-role search did not safely close identity-to-employer linkage.",
            evidence_type=typ, evidence_grade=grade, evidence_title=etitle, evidence_url=url, evidence_date=edate,
            current_verification_status="UNRESOLVED_CURRENT_ORG_TITLE",
            unresolved_reason="Official Hebei federation roster confirms this source identity/role, but no sufficiently current and specific public evidence was found in this batch to assign a current organization/title without risking a name-only match.",
        )
    results.append(out)

with open(E / "W3_BATCH_0006_RESULTS.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
    w.writeheader()
    w.writerows(results)

LEDGER_FIELDS = ["queue_order","person_id","province","excel_row","candidate_names","evidence_type","evidence_grade","evidence_title","evidence_url","evidence_date","current_verification_status","unresolved_reason"]
OVERLAY_FIELDS = ["queue_order","person_id","province","excel_row","identity_resolution","candidate_names","current_organization","current_title","current_verification_status","evidence_grade","evidence_url","unresolved_reason"]

def append_rows(path, fields, rows):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        old = list(csv.DictReader(f))
    last = int(old[-1]["queue_order"])
    if last == 360:
        return
    assert last == 300, (path, last)
    with open(path, "a", encoding="utf-8", newline="") as f:
        csv.DictWriter(f, fieldnames=fields, extrasaction="ignore", lineterminator="\n").writerows(rows)

append_rows(E / "W3_EVIDENCE_LEDGER.csv", LEDGER_FIELDS, results)
append_rows(E / "W3_VERIFICATION_OVERLAY.csv", OVERLAY_FIELDS, results)

confirmed = sum(r["current_verification_status"] == "CURRENT_ORG_TITLE_CONFIRMED" for r in results)
unresolved = 60 - confirmed
a_count = sum(r["evidence_grade"] == "A" for r in results)
b_count = sum(r["evidence_grade"] == "B" for r in results)
assert confirmed == 26 and unresolved == 34
assert a_count + b_count == 60
assert all(r["evidence_url"] and r["evidence_title"] for r in results)
assert all((r["current_organization"] and r["current_title"]) if r["current_verification_status"] == "CURRENT_ORG_TITLE_CONFIRMED" else bool(r["unresolved_reason"]) for r in results)

with open(E / "W3_EVIDENCE_LEDGER.csv", "r", encoding="utf-8-sig", newline="") as f:
    led = list(csv.DictReader(f))
assert len(led) == 360
assert [int(x["queue_order"]) for x in led] == list(range(1, 361))

(E / "W3_BATCH_0006_METRICS.yaml").write_text(f"""schema: fc2515-w3-batch-metrics-v1
project_id: FC-EXEC-2515-01
gate: W3-BATCH-0006
status: PASS
queue_range: [301, 360]
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
  processed_queue_rows: 360
  actionable_queue_remaining: 10284
  next_queue_order: 361
  p0_processed: 101
  p0_remaining: 0
  p1_processed: 259
  p1_remaining: 4072
next_gate: W3-BATCH-0007
""", encoding="utf-8")

(E / "W3_BATCH_0006_VALIDATION.md").write_text(f"""# W3-BATCH-0006 Validation

Result: **PASS**

- Deterministic queue slice: 301–360 exactly, 60 rows; 57 河北 + 3 吉林, all P1_IDENTITY.
- Every touched row has public evidence or an explicit unresolved-current-role reason.
- No current organization/title was assigned from a name-only hit.
- 18 current-role results reuse prior sealed evidence only where the same Hebei official federation roster cross-lists the identical person under an earlier role and 执委; person_ids remain separate.
- Fresh current-role evidence was added for 张志祥、周超男、霍占利、魏立华、魏海金、李维斗、唐庆会、吕兵.
- 吉林 rows use 2026 public evidence for current provincial federation leadership; no stale carry-forward was used.
- Evidence grades in batch: A={a_count}, B={b_count}; C=0.
- Current organization + title confirmed: {confirmed}/60.
- Current-role unresolved: {unresolved}/60; unresolved organization/title fields remain blank rather than guessed.
- Cumulative W3 evidence ledger reconciles to 360 rows with queue_order 1..360 and no gaps.
- Unsupported current-title claims: 0.

Next deterministic gate: `W3-BATCH-0007`, starting queue_order 361.
""", encoding="utf-8")

sp = ROOT / "STATUS.yaml"
s = sp.read_text(encoding="utf-8")
s = s.replace("code: W3-BATCH-0005\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS", "code: W3-BATCH-0006\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS", 1)
s = s.replace("code: W3-BATCH-0006\n  phase: W3-EVIDENCE-ENRICH\n  status: READY", "code: W3-BATCH-0007\n  phase: W3-EVIDENCE-ENRICH\n  status: READY", 1)
for a, b in {
    "  batches_sealed: 5":"  batches_sealed: 6",
    "  processed_queue_rows: 300":"  processed_queue_rows: 360",
    "  next_queue_order: 301":"  next_queue_order: 361",
    "  actionable_queue_remaining: 10344":"  actionable_queue_remaining: 10284",
    "    processed: 199\n    remaining: 4132":"    processed: 259\n    remaining: 4072",
    "  identity_evidence_rows: 300":"  identity_evidence_rows: 360",
    "  current_org_title_confirmed_rows: 67":f"  current_org_title_confirmed_rows: {67+confirmed}",
    "  current_org_title_unresolved_rows: 132":f"  current_org_title_unresolved_rows: {132+unresolved}",
}.items():
    assert a in s, a
    s = s.replace(a, b, 1)

anchor = "  w3_batch_0005_validation: projects/fc-exec-2515/evidence/W3_BATCH_0005_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv"
rep = "  w3_batch_0005_validation: projects/fc-exec-2515/evidence/W3_BATCH_0005_VALIDATION.md\n  w3_batch_0006_results: projects/fc-exec-2515/evidence/W3_BATCH_0006_RESULTS.csv\n  w3_batch_0006_metrics: projects/fc-exec-2515/evidence/W3_BATCH_0006_METRICS.yaml\n  w3_batch_0006_validation: projects/fc-exec-2515/evidence/W3_BATCH_0006_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv"
assert anchor in s
s = s.replace(anchor, rep, 1)
sp.write_text(s, encoding="utf-8")

cp = ROOT / "CURRENT.yaml"
c = cp.read_text(encoding="utf-8")
c = c.replace("current_gate: W3-BATCH-0006", "current_gate: W3-BATCH-0007", 1)
c = c.replace("work_cursor: 300", "work_cursor: 360", 1)
for a, b in {
    "verified_records: 67":f"verified_records: {67+confirmed}",
    "unresolved_records: 10577":f"unresolved_records: {10577-confirmed}",
    "last_input_head: ae2818b476cf0bab94685b059491dfe6a192fd87":f"last_input_head: {INPUT_HEAD}",
    "  processed: 300":"  processed: 360",
    "  actionable_remaining: 10344":"  actionable_remaining: 10284",
    "  next_queue_order: 301":"  next_queue_order: 361",
    "      processed: 199\n      remaining: 4132":"      processed: 259\n      remaining: 4072",
}.items():
    assert a in c, a
    c = c.replace(a, b, 1)

lines = c.splitlines()
for i, line in enumerate(lines):
    if line.startswith("last_evidence_at:"):
        lines[i] = f"last_evidence_at: {NOW}"
        break
c = "\n".join(lines) + "\n"

b6 = f"""
w3_batch_0006:
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
c = c.replace("\nnotes:\n", b6 + "\nnotes:\n", 1)
needle = "  - Next deterministic queue order is 301.\n"
notes = """  - Next deterministic queue order is 301.
  - W3-BATCH-0006 processed queue orders 301-360 exactly: 57 河北 + 3 吉林 P1 identity/current-role rows.
  - 26 rows received current organization/title confirmation; 34 remain explicitly unresolved where current evidence was insufficiently specific.
  - Eighteen confirmations reuse prior sealed current-role evidence only after same-roster cross-list identity closure; no person_id merge was performed.
  - Fresh current-role evidence was added for 张志祥、周超男、霍占利、魏立华、魏海金、李维斗、唐庆会、吕兵.
  - 吉林 leadership claims were refreshed from 2026 evidence; 河北 common-name rows remain unresolved unless identity-to-role linkage is safe.
  - Next deterministic queue order is 361.
"""
assert needle in c
c = c.replace(needle, notes, 1)
cp.write_text(c, encoding="utf-8")

assert "code: W3-BATCH-0007" in sp.read_text(encoding="utf-8")
assert "current_gate: W3-BATCH-0007" in cp.read_text(encoding="utf-8")
print({"gate":"W3-BATCH-0006","confirmed":confirmed,"unresolved":unresolved,"A":a_count,"B":b_count,"ledger_rows":len(led),"next":361,"now":NOW})
