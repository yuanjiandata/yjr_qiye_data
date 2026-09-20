#!/usr/bin/env python3
import csv, gzip, glob, subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
P = ROOT / "projects" / "fc-exec-2515"
E = P / "evidence"
INPUT_HEAD = "6c190cdb77530ca81234a7242d3b34bf61650219"
BATCH_START, BATCH_END = 1141, 1200
VERIFY_DATE = "2026-09-20"
NOW = datetime.now(timezone(timedelta(hours=8))).replace(microsecond=0).isoformat()
AH_HIST = "https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_ah/202208/t20220812_312855.html"

head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
assert head == INPUT_HEAD, (head, INPUT_HEAD)
with gzip.open(E / "W2_UNRESOLVED_QUEUE.csv.gz", "rt", encoding="utf-8-sig", newline="") as f:
    allq = list(csv.DictReader(f))
rows = allq[BATCH_START - 1:BATCH_END]
assert len(rows) == 60
assert [int(r["queue_order"]) for r in rows] == list(range(BATCH_START, BATCH_END + 1))
assert {r["priority"] for r in rows} == {"P1_IDENTITY"}
assert {r["province"] for r in rows} == {"安徽"}

# Load already sealed result rows so cross-listed source records can reuse evidence
# only when repository ambiguity_group_id + province + normalized name all match.
by_order = {}
for fn in sorted(glob.glob(str(E / "W3_BATCH_*_RESULTS.csv"))):
    with open(fn, "r", encoding="utf-8-sig", newline="") as f:
        for x in csv.DictReader(f):
            if int(x["queue_order"]) < BATCH_START:
                by_order[int(x["queue_order"])] = x
by_ag = defaultdict(list)
for q in allq:
    by_ag[q["ambiguity_group_id"]].append(q)
special = {
    "曹金栋": {
        "org": "中共安庆市委统一战线工作部",
        "title": "副部长（兼安庆市党外知识分子联谊会常务副会长）",
        "grade": "A",
        "etype": "government_party_official_current_role_with_federation_identity_bridge",
        "etitle": "市党外知识分子联谊会召开三届三次理事会会议",
        "url": "https://www.aqtz.gov.cn/html/news/1005/16196.html",
        "date": "2026-05-12",
        "notes": "安庆统一战线2026-05官方稿明确曹金栋现任市委统战部副部长；2025-11同一官方站点明确其同时任市工商联党组书记，形成源工商联身份到当前角色的连续桥接。",
    },
    "韩东成": {
        "org": "安徽省东超科技有限公司",
        "title": "董事长",
        "grade": "B",
        "etype": "authoritative_media_current_role_with_federation_enterprise_identity_bridge",
        "etitle": "韩东成代表：推动空中成像技术服务千行百业",
        "url": "https://ah.people.com.cn/n2/2026/0420/c227131-41557224.html",
        "date": "2026-04-20",
        "notes": "人民网安徽2026-04明确韩东成为安徽省东超科技有限公司董事长；安徽省工商联2024官方企业稿明确同名东超科技创始人、董事长兼总经理，形成企业+工商联语境身份桥，不以姓名单字段认人。",
    },
    "程景梁": {
        "org": "黄山市工商业联合会",
        "title": "主席",
        "grade": "B",
        "etype": "authoritative_media_current_federation_role_with_government_continuity_bridge",
        "etitle": "安徽省皖北经济发展合作商会十五周年庆",
        "url": "https://www.ahcaijing.com/html/2026/hefei_0207/614500.html",
        "date": "2026-02-07",
        "notes": "2026-02安徽财经网明确程景梁为黄山市工商联主席；黄山市政府2025-12官方党外人士座谈会亦明确其市工商联主席身份，且源记录为安徽省工商联常委，角色链连续。",
    },
}

new_unresolved = {
    "殷金宝": "检索到天津银行系统同名历史人物，但地域、履历和生存状态均与安徽省工商联源身份不一致，明确排除；未发现可安全桥接的安徽当前角色。",
    "曹建": "可确认2023年亳州市委统战部副部长、市工商联党组书记历史身份，但未找到足够新的2026权威现职证据，故不延续旧职。",
    "梁万标": "检索到安徽省京港物流有限公司及商协会同名现职信息，但未找到能把该身份与安徽省工商联常委源记录安全连接的独立桥接证据。",
    "梁红群": "2026公开资料明确阜阳市妇联党组书记、主席梁红群，但缺少将该现职身份与安徽省工商联常委源记录安全闭合的跨来源桥接，故不按姓名直接挂接。",
    "彭友": "2026上市公司相关公开信息支持芯瑞达董事长彭友仍在任，但本轮未找到把安徽省工商联常委源记录与该上市公司身份直接闭合的独立工商联/企业桥接证据。",
    "韩家林": "可找到2024芜湖市委统战部副部长、市工商联党组书记历史证据，但未找到足够新的2026权威现职材料，故不机械沿用旧职。",
    "戴正刚": "全国工商联2024材料确认安徽正刚新能源科技有限公司董事长戴正刚并处于安徽省工商联常执委企业家语境，但缺少2026足够新的权威现职证据，保留未决。",
}
fields = [
    "queue_order","person_id","province","excel_row","name_normalized","source_federation_role",
    "identity_resolution","candidate_names","current_organization","current_title",
    "current_verification_status","evidence_type","evidence_grade","evidence_title","evidence_url",
    "evidence_date","unresolved_reason","research_notes",
]
results = []
for r in rows:
    name = r["name_normalized"]
    base = {
        "queue_order": r["queue_order"], "person_id": r["person_id"], "province": r["province"],
        "excel_row": r["excel_row"], "name_normalized": name,
        "source_federation_role": r["federation_role"], "candidate_names": name,
    }
    if name in special:
        s = special[name]
        result = {**base,
            "identity_resolution": "CURRENT_ROLE_CONFIRMED_WITH_CONTEXTUAL_IDENTITY_BRIDGE",
            "current_organization": s["org"], "current_title": s["title"],
            "current_verification_status": "CURRENT_ORG_TITLE_CONFIRMED",
            "evidence_type": s["etype"], "evidence_grade": s["grade"],
            "evidence_title": s["etitle"], "evidence_url": s["url"], "evidence_date": s["date"],
            "unresolved_reason": "", "research_notes": s["notes"],
        }
    else:
        priors = [x for x in by_ag[r["ambiguity_group_id"]]
                  if int(x["queue_order"]) < BATCH_START and int(x["queue_order"]) in by_order]
        if priors:
            p = max(priors, key=lambda x: int(x["queue_order"]))
            prev = by_order[int(p["queue_order"])]
            assert p["province"] == r["province"] and p["name_normalized"] == name
            result = {**base,
                "identity_resolution": "REUSED_SEALED_EVIDENCE_SAME_REPOSITORY_AMBIGUITY_GROUP",
                "current_organization": prev["current_organization"], "current_title": prev["current_title"],
                "current_verification_status": prev["current_verification_status"],
                "evidence_type": prev["evidence_type"], "evidence_grade": prev["evidence_grade"],
                "evidence_title": prev["evidence_title"], "evidence_url": prev["evidence_url"],
                "evidence_date": prev["evidence_date"], "unresolved_reason": prev["unresolved_reason"],
                "research_notes": f"与已封存 queue {p['queue_order']} 同省、同名且同 ambiguity_group_id={r['ambiguity_group_id']}；复用其证据但保留独立 person_id，不做姓名合并。" + prev["research_notes"],
            }
        else:
            reason = new_unresolved.get(name, "针对当前公开政府、工商联、企业及媒体资料进行检索，未找到能在不依赖姓名单字段的前提下安全闭合的当前单位+职务。")
            result = {**base,
                "identity_resolution": "HISTORICAL_IDENTITY_CURRENT_ROLE_UNRESOLVED",
                "current_organization": "", "current_title": "",
                "current_verification_status": "UNRESOLVED_CURRENT_ORG_TITLE",
                "evidence_type": "federation_official_historical_identity_plus_targeted_current_research",
                "evidence_grade": "A", "evidence_title": "安徽省工商联第十二届执行委员会名单",
                "evidence_url": AH_HIST, "evidence_date": VERIFY_DATE,
                "unresolved_reason": reason,
                "research_notes": "保持未决；同名命中、旧职务或缺少工商联身份桥的候选均未写入。",
            }
    results.append(result)

out = E / "W3_BATCH_0020_RESULTS.csv"
with out.open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(results)
# Append cumulative evidence ledger and verification overlay.
ledger_path = E / "W3_EVIDENCE_LEDGER.csv"
with ledger_path.open("r", encoding="utf-8-sig", newline="") as f:
    old_ledger = list(csv.DictReader(f)); ledger_fields = list(old_ledger[0].keys())
assert len(old_ledger) == 1140
new_ledger = old_ledger + [{k: {
    "queue_order": x["queue_order"], "person_id": x["person_id"], "province": x["province"],
    "excel_row": x["excel_row"], "candidate_names": x["candidate_names"], "evidence_type": x["evidence_type"],
    "evidence_grade": x["evidence_grade"], "evidence_title": x["evidence_title"], "evidence_url": x["evidence_url"],
    "evidence_date": x["evidence_date"], "current_verification_status": x["current_verification_status"],
    "unresolved_reason": x["unresolved_reason"],
}.get(k, "") for k in ledger_fields} for x in results]
with ledger_path.open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=ledger_fields); w.writeheader(); w.writerows(new_ledger)

overlay_path = E / "W3_VERIFICATION_OVERLAY.csv"
with overlay_path.open("r", encoding="utf-8-sig", newline="") as f:
    old_overlay = list(csv.DictReader(f)); overlay_fields = list(old_overlay[0].keys())
assert len(old_overlay) == 1140
new_overlay = old_overlay + [{k: {
    "queue_order": x["queue_order"], "person_id": x["person_id"], "province": x["province"],
    "excel_row": x["excel_row"], "identity_resolution": x["identity_resolution"],
    "candidate_names": x["candidate_names"], "current_organization": x["current_organization"],
    "current_title": x["current_title"], "current_verification_status": x["current_verification_status"],
    "evidence_grade": x["evidence_grade"], "evidence_url": x["evidence_url"],
    "unresolved_reason": x["unresolved_reason"],
}.get(k, "") for k in overlay_fields} for x in results]
with overlay_path.open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=overlay_fields); w.writeheader(); w.writerows(new_overlay)

statuses = Counter(x["current_verification_status"] for x in results)
grades = Counter(x["evidence_grade"] for x in results)
confirmed = statuses["CURRENT_ORG_TITLE_CONFIRMED"]
unresolved = statuses["UNRESOLVED_CURRENT_ORG_TITLE"]
assert confirmed == 33 and unresolved == 27, (confirmed, unresolved)
assert grades == Counter({"A": 58, "B": 2}), grades
assert len(new_ledger) == 1200 and len(new_overlay) == 1200
assert [int(x["queue_order"]) for x in new_ledger] == list(range(1, 1201))
assert [int(x["queue_order"]) for x in new_overlay] == list(range(1, 1201))
assert len({x["queue_order"] for x in new_ledger}) == 1200
assert len({x["queue_order"] for x in new_overlay}) == 1200
assert all((x["evidence_url"] or x["unresolved_reason"]) for x in results)
assert all(not (x["current_verification_status"] == "CURRENT_ORG_TITLE_CONFIRMED" and (not x["current_organization"] or not x["current_title"] or not x["evidence_url"])) for x in results)
metrics = f'''schema: fc-exec-2515-w3-batch-metrics-v1
project_id: FC-EXEC-2515-01
gate: W3-BATCH-0020
status: SEALED
validation: PASS
touched_rows: 60
anhui_rows: 60
p1_identity_rows: 60
evidence_backed_rows: 60
a_grade_rows: {grades['A']}
b_grade_rows: {grades['B']}
c_grade_rows: 0
current_org_title_confirmed_rows: {confirmed}
current_org_title_unresolved_rows: {unresolved}
unsupported_current_title_claims: 0
queue_start: 1141
queue_end: 1200
next_queue_order: 1201
verified_at: {NOW}
input_head: {INPUT_HEAD}
'''
(E / "W3_BATCH_0020_METRICS.yaml").write_text(metrics, encoding="utf-8")

validation = f'''# W3-BATCH-0020 Validation

- Gate: `W3-BATCH-0020`
- Queue orders: `1141-1200`
- Touched rows: **60** (`安徽 60`)
- Priority: `P1_IDENTITY` 60
- Evidence coverage: **60/60**
- Evidence grades: **A={grades['A']}, B={grades['B']}, C=0**
- Current organization + title confirmed: **{confirmed}**
- Explicit current-role unresolved: **{unresolved}**
- Unsupported current-title claims: **0**
- Cumulative evidence ledger: **1200 rows**, queue `1-1200` contiguous, no duplicate queue order
- Cumulative verification overlay: **1200 rows**, queue `1-1200` contiguous, no duplicate queue order

## Identity / recency controls

- 50 touched rows are cross-list records whose identity linkage is already encoded by the repository's `ambiguity_group_id`; evidence is reused only when normalized name + province + ambiguity group all match. Each source row keeps its own `person_id`.
- Reused current-role claims remain backed by already sealed public official/enterprise/exchange evidence checked during the immediately preceding 安徽 batches; no name-only merge is performed.
- Fresh public-web research was performed for all 10 first-occurrence identities in this gate. Only 曹金栋、韩东成、程景梁 obtained a sufficiently safe current-role bridge; the other seven remain explicit unresolved cases.
- 曹金栋 is refreshed to the 2026 current role `安庆市委统战部副部长`; the 2025 official page linking him to `市工商联党组书记` supplies the federation identity bridge.
- 韩东成 is linked to current `安徽省东超科技有限公司董事长` through current authoritative media plus an 安徽省工商联 enterprise-profile bridge.
- 程景梁 is linked to current `黄山市工商联主席` through 2026 reporting plus a 2025 黄山市政府 official continuity record.
- 殷金宝、曹建、梁万标、梁红群、彭友、韩家林、戴正刚 remain unresolved where current evidence or identity bridging was insufficient; known same-name/historical hits were not promoted.

**PASS**
'''
(E / "W3_BATCH_0020_VALIDATION.md").write_text(validation, encoding="utf-8")
status_path = P / "STATUS.yaml"
s = status_path.read_text(encoding="utf-8")
repls = {
    "code: W3-BATCH-0019": "code: W3-BATCH-0020",
    "code: W3-BATCH-0020\n  phase: W3-EVIDENCE-ENRICH\n  status: READY": "code: W3-BATCH-0021\n  phase: W3-EVIDENCE-ENRICH\n  status: READY",
    "batches_sealed: 19": "batches_sealed: 20",
    "processed_queue_rows: 1140": "processed_queue_rows: 1200",
    "next_queue_order: 1141": "next_queue_order: 1201",
    "actionable_queue_remaining: 9504": "actionable_queue_remaining: 9444",
    "processed: 1039": "processed: 1099",
    "remaining: 3292": "remaining: 3232",
    "identity_evidence_rows: 1140": "identity_evidence_rows: 1200",
    "current_org_title_confirmed_rows: 694": "current_org_title_confirmed_rows: 727",
    "current_org_title_unresolved_rows: 343": "current_org_title_unresolved_rows: 370",
}
for a, b in repls.items():
    assert a in s, a
    s = s.replace(a, b, 1)
anchor = "  w3_batch_0019_validation: projects/fc-exec-2515/evidence/W3_BATCH_0019_VALIDATION.md\n"
assert anchor in s
s = s.replace(anchor, anchor + "  w3_batch_0020_results: projects/fc-exec-2515/evidence/W3_BATCH_0020_RESULTS.csv\n  w3_batch_0020_metrics: projects/fc-exec-2515/evidence/W3_BATCH_0020_METRICS.yaml\n  w3_batch_0020_validation: projects/fc-exec-2515/evidence/W3_BATCH_0020_VALIDATION.md\n", 1)
status_path.write_text(s, encoding="utf-8")

current_path = P / "CURRENT.yaml"
c = current_path.read_text(encoding="utf-8")
crepls = {
    "current_gate: W3-BATCH-0020": "current_gate: W3-BATCH-0021",
    "work_cursor: 1140": "work_cursor: 1200",
    "verified_records: 696": "verified_records: 729",
    "unresolved_records: 9948": "unresolved_records: 9915",
    "processed: 1140": "processed: 1200",
    "actionable_remaining: 9504": "actionable_remaining: 9444",
    "next_queue_order: 1141": "next_queue_order: 1201",
    "processed: 1039": "processed: 1099",
    "remaining: 3292": "remaining: 3232",
}
for a, b in crepls.items():
    assert a in c, a
    c = c.replace(a, b, 1)
c = c.replace("last_input_head: 8a5dc82dd8ef8001e12b57db7438e5515262d056", f"last_input_head: {INPUT_HEAD}", 1)
c = c.replace("last_evidence_at: 2026-09-20T17:52:33+08:00", f"last_evidence_at: {NOW}", 1)
batch_block = f'''\nw3_batch_0020:\n  status: SEALED\n  validation: PASS\n  touched_rows: 60\n  anhui_rows: 60\n  p1_identity_rows: 60\n  evidence_backed_rows: 60\n  a_grade_rows: {grades['A']}\n  b_grade_rows: {grades['B']}\n  c_grade_rows: 0\n  current_org_title_confirmed_rows: {confirmed}\n  current_org_title_unresolved_rows: {unresolved}\n  unsupported_current_title_claims: 0\n\n'''
notes_anchor = "notes:\n"
assert notes_anchor in c
c = c.replace(notes_anchor, batch_block + notes_anchor, 1)
notes_tail = f'''  - W3-BATCH-0020 processed queue orders 1141-1200 exactly, all 60 安徽 P1 identity/current-role rows.\n  - {confirmed} rows received current organization/title confirmation; {unresolved} remain explicit unresolved with no unsupported current-title claims.\n  - 50 cross-list rows reused sealed evidence only when repository ambiguity_group_id + normalized name + province matched; each source row retains its independent person_id.\n  - Fresh research covered all 10 first-occurrence identities; only 曹金栋、韩东成、程景梁 received safe current-role closure.\n  - 曹金栋 is current 安庆市委统战部副部长 via 2026 official evidence and a 2025 市工商联党组书记 bridge; 韩东成 is current 东超科技董事长; 程景梁 is current 黄山市工商联主席.\n  - 殷金宝、曹建、梁万标、梁红群、彭友、韩家林、戴正刚 remain unresolved where recency or identity linkage was insufficient.\n  - Evidence grades are A={grades['A']}, B={grades['B']}, C=0; next deterministic queue order is 1201.\n'''
c = c.rstrip() + "\n" + notes_tail
current_path.write_text(c, encoding="utf-8")

print(f"PASS W3-BATCH-0020 confirmed={confirmed} unresolved={unresolved} grades={dict(grades)} next=1201")
