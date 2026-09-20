#!/usr/bin/env python3
import csv, gzip, glob, subprocess, re
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
P = ROOT / "projects" / "fc-exec-2515"
E = P / "evidence"
INPUT_HEAD = "922c09a0ebb4a3356c12765b7aa1435d10050809"
BATCH_START, BATCH_END = 1261, 1320
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
special = {
    "付文辉": dict(org="宁德思客琦智能装备科技股份有限公司", title="董事长兼总经理", grade="B", etype="authoritative_media_current_role_with_historical_org_bridge", etitle="宁德师范学院第十一期闽东大讲堂开讲", url="https://m.edu.k618.cn/gaoxiao/202609/t20260915_20059213.html", date="2026-09-15", notes="源记录已有思客琦历史组织键；2026-09公开活动明确付文辉为思客琦董事长兼总经理。"),
    "华祥斌": dict(org="福建德尔科技股份有限公司", title="法定代表人", grade="B", etype="authoritative_media_current_legal_role_with_historical_org_bridge", etitle="再度冲击IPO！福建德尔启动上市辅导", url="https://www.bbtnews.com.cn/2026/0129/583479.shtml", date="2026-01-29", notes="源记录已有福建德尔历史组织键；2026-01上市辅导备案报道援引证监会材料明确法定代表人为华祥斌。"),
    "许阳阳": dict(org="达利食品集团", title="总裁", grade="B", etype="authoritative_media_current_role_with_historical_org_bridge", etitle="达利食品集团总裁许阳阳：向世界传递中国饮食文化与价值力量", url="https://fj.people.com.cn/n2/2026/0907/c181466-41689258.html", date="2026-09-07", notes="源记录已有达利食品集团历史组织键；人民网福建2026-09直接写明现任总裁许阳阳。"),
    "许明金": dict(org="香缤集团", title="董事局主席", grade="B", etype="authoritative_media_current_role_with_federation_context", etitle="全国政协委员许明金：加强深港合作", url="https://finance.sina.com.cn/jjxw/2026-03-09/doc-inhqknrq6988047.shtml", date="2026-03-09", notes="中国经营报报道同时写明全国政协委员、广东省福建商会会长、香缤集团董事局主席许明金；与福建省总商会历史副会长身份形成跨商会身份桥。"),
    "吴体芳": dict(org="德艺文化创意集团股份有限公司", title="董事长", grade="B", etype="authoritative_financial_media_current_role_with_historical_org_bridge", etitle="德艺文创控股股东及董事长吴体芳相关当前披露", url="https://finance.sina.com.cn/stock/aigc/zjchg/2026-03-25/doc-inhsffcv9663756.shtml", date="2026-03-25", notes="源记录已有德艺文化创意历史组织键；2026-03当前披露明确吴体芳为控股股东、实际控制人、董事长。"),
    "柯希平": dict(org="厦门恒兴集团有限公司", title="董事长", grade="A", etype="government_official_current_role_with_historical_org_bridge", etitle="柯希平：向新而行为企发声", url="https://www.fujian.gov.cn/zwgk/ztzl/sxzygwzxsgzx/flsxkmh/202602/t20260228_7102764.htm", date="2026-02-28", notes="源记录已有恒兴集团历史组织键；福建省政府2026-02直接写明全国政协委员、厦门恒兴集团董事长柯希平。"),
    "施锦珊": dict(org="鑫桥联合融资租赁有限公司", title="总裁", grade="B", etype="formal_association_current_role_and_federation_identity", etitle="中国服务贸易协会融资租赁专业委员会成立大会", url="https://www.sina.cn/news/detail/5283550779148572.html", date="2026-04-03", notes="2026-04北京福建企业总商会认证材料同时写明福建省工商联（总商会）副会长、鑫桥联合融资租赁有限公司总裁施锦珊。"),
    "黄丹青": dict(org="融汇（福建）集团有限公司", title="总裁", grade="B", etype="authoritative_media_current_role_and_federation_identity", etitle="左海会客厅｜黄丹青：让东西方艺术在家门口对话", url="https://news.fznews.com.cn/fzyw/20260418/3FXj14Xq31.shtml", date="2026-04-18", notes="福州日报2026-04同段明确福建省总商会兼职副会长、融汇（福建）集团有限公司总裁黄丹青，身份与现职直接闭合。"),
    "黄铁明": dict(org="福建祥鑫股份有限公司", title="党委书记、董事长", grade="A", etype="government_official_current_role_with_historical_org_bridge", etitle="祝贺！福建12位企业家获评全国优秀企业家", url="https://fgw.fujian.gov.cn/ztzl/ssxsdmyjjqszl/gzjz/202603/t20260312_7109264.htm", date="2026-03-12", notes="源记录已有福建祥鑫历史组织键；福建省发改委2026-03明确黄铁明为福建祥鑫股份有限公司党委书记、董事长。"),
    "章高路": dict(org="安井食品集团股份有限公司", title="联席董事长、执行董事", grade="B", etype="current_listed_company_board_reporting_with_historical_org_bridge", etitle="安井食品完成董事会换届", url="https://finance.sina.com.cn/roll/2026-05-22/doc-inhysxpa5565846.shtml", date="2026-05-22", notes="源记录已有安井食品历史组织键；2026-05董事会换届公告报道明确章高路当选联席董事长，新一届董事会任期至2029年。"),
    "蒋志鹏": dict(org="福建弦德集团有限公司", title="董事长", grade="B", etype="authoritative_financial_media_current_role_with_historical_org_bridge", etitle="全国政协委员蒋志鹏相关履职报道", url="https://finance.sina.com.cn/roll/2026-03-11/doc-inhqpxkf5924021.shtml", date="2026-03-11", notes="源记录为福建弦德投资董事长；上海证券报2026-03明确全国政协委员、福建弦德集团有限公司董事长蒋志鹏，地域与集团身份连续闭合。"),
    "傅天龙": dict(org="福建春伦集团有限公司", title="董事长", grade="B", etype="authoritative_media_current_role_with_historical_org_bridge", etitle="标准为翼 茶香致远——春伦集团以标准化赋能福州茉莉花茶产业腾飞", url="https://www.fjdaily.com/app/content/2026-01/26/content_3856506.html", date="2026-01-26", notes="源记录已有春伦集团历史组织键；福建日报2026-01直接写明福建春伦集团有限公司董事长傅天龙。"),
    "谢伟东": dict(org="三明市海斯福化工有限责任公司", title="董事长", grade="A", etype="enterprise_official_current_role_with_historical_org_bridge", etitle="喜报！海斯福荣获三明市两项荣誉", url="https://www.hexafluo.com/article-47215-75876.html", date="2026-02-25", notes="源记录已有海斯福历史组织键；海斯福官网2026-02明确谢伟东现为董事长，刷新源表旧总经理职务。"),
    "谢秉昆": dict(org="福建坤彩材料科技股份有限公司", title="董事长", grade="B", etype="authoritative_financial_media_current_role_with_historical_org_bridge", etitle="V观财报｜坤彩科技被责令改正 董事长谢秉昆等遭警示函", url="https://finance.sina.com.cn/tech/roll/2026-01-16/doc-inhhpfkr5380057.shtml", date="2026-01-16", notes="源记录已有坤彩科技董事长历史组织键；2026-01中新经纬经新浪财经报道明确谢秉昆为公司董事长，2026-08公司业绩说明会材料继续出现其董事长身份。"),
    "赖世贤": dict(org="安踏集团", title="执行董事、联席CEO（兼代理安踏品牌CEO）", grade="B", etype="authoritative_financial_media_current_role_with_historical_org_bridge", etitle="800亿晋江鞋王，主业换帅", url="https://m.21jingji.com/article/20260716/herald/d9f92d48ce316def7548946b7f746c9f.html", date="2026-07-16", notes="源记录已有安踏集团历史组织键；安踏集团向21世纪商业评论确认赖世贤现为执行董事、联席CEO，并自2026-07代理安踏品牌CEO。"),
    "魏成生": dict(org="均和（厦门）控股有限公司", title="总裁", grade="B", etype="federation_context_current_role", etitle="福建省工商联系统热议全省优化营商环境大会精神", url="https://www.sohu.com/a/974018973_121106994", date="2026-01-15", notes="2026工商联系统公开材料同段写明福建省总商会副会长、福建省高科技商会会长、均和（厦门）控股有限公司总裁魏成生。"),
    "施文彪": dict(org="福建省工商业联合会", title="党组成员、秘书长", grade="B", etype="current_federation_role_reporting", etitle="第二届侨商供采大会在福州举行", url="https://www.52hrtt.com/ec/n/w/info/G1770704445352", date="2026-03-02", notes="2026-03活动公开材料直接写明福建省工商联党组成员、秘书长施文彪，与源记录专职秘书长身份直接连续。"),
    "王书传": dict(org="信和新材料股份有限公司", title="党支部书记、总经理", grade="A", etype="government_official_current_role_with_federation_identity_bridge", etitle="王书传：攻关核心技术，做强海洋装备福建造", url="https://www.fujian.gov.cn/zwgk/ztzl/2026lh/lhhsy/wysy/202601/t20260129_7086555.htm", date="2026-01-29", notes="福建省政府2026-01明确省政协委员、信和新材料党支部书记兼总经理王书传；信和公开材料已明确同一企业王书传为福建省工商联常委，和2022官方常委名册共同闭合身份。"),
}

# All other touched identities were individually or cohort-searched against current
# government/federation/company/filing/media sources. If the identity bridge is not
# strong enough, leave current role blank rather than guessing from a homonym.
special_unresolved = {
    "方华玉": "2026福建日报报道写明华峰华锦有限公司董事长方华玉，但源组织为福建华峰新材料有限公司；未取得两法律实体与源身份的当前官方桥接，故不强行迁移。",
    "吴有林": "2026最新公司披露报道区分吴有林为时任董事长/总经理、苏明城为当前董事长；未找到吴有林安全可写的现任单位职务。",
    "张桂潮": "2026上市公司报道明确张桂潮已于2025-09离任福龙马董事及高级管理职务；未找到可验证的替代现任单位职务，且不将离任单一公司推断为无任何现职。",
    "王文礼": "当前福建公开资料存在至少两名同名王文礼（八马茶业董事长、福建税务系统干部等），源记录无单位键，禁止按姓名择一归并。",
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

out = E / "W3_BATCH_0022_RESULTS.csv"
with out.open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n"); w.writeheader(); w.writerows(results)
ledger_path = E / "W3_EVIDENCE_LEDGER.csv"
with ledger_path.open("r", encoding="utf-8-sig", newline="") as f:
    old_ledger = list(csv.DictReader(f)); ledger_fields = list(old_ledger[0].keys())
assert len(old_ledger) == 1260
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
assert len(old_overlay) == 1260
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
assert confirmed == 20 and unresolved == 40, (confirmed, unresolved)
assert grades == Counter({"A": 46, "B": 14}), grades
assert len(new_ledger) == 1320 and len(new_overlay) == 1320
assert [int(x["queue_order"]) for x in new_ledger] == list(range(1, 1321))
assert [int(x["queue_order"]) for x in new_overlay] == list(range(1, 1321))
assert len({x["queue_order"] for x in new_ledger}) == 1320
assert len({x["queue_order"] for x in new_overlay}) == 1320
assert all((x["evidence_url"] or x["unresolved_reason"]) for x in results)
assert all(not (x["current_verification_status"] == "CURRENT_ORG_TITLE_CONFIRMED" and (not x["current_organization"] or not x["current_title"] or not x["evidence_url"])) for x in results)
assert all(not (x["current_verification_status"] == "UNRESOLVED_CURRENT_ORG_TITLE" and (x["current_organization"] or x["current_title"] or not x["unresolved_reason"])) for x in results)
metrics = f'''schema: fc-exec-2515-w3-batch-metrics-v1
project_id: FC-EXEC-2515-01
gate: W3-BATCH-0022
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
queue_start: 1261
queue_end: 1320
next_queue_order: 1321
verified_at: {NOW}
input_head: {INPUT_HEAD}
'''
(E / "W3_BATCH_0022_METRICS.yaml").write_text(metrics, encoding="utf-8")
validation = f'''# W3-BATCH-0022 Validation

- Gate: `W3-BATCH-0022`
- Queue orders: `1261-1320`
- Touched rows: **60** (`福建 60`)
- Priority: `P1_IDENTITY` 60
- Evidence coverage: **60/60**
- Evidence grades: **A={grades['A']}, B={grades['B']}, C=0**
- Current organization + title confirmed: **{confirmed}**
- Explicit current-role unresolved: **{unresolved}**
- Unsupported current-title claims: **0**
- Cumulative evidence ledger: **1320 rows**, queue `1-1320` contiguous, no duplicate queue order
- Cumulative verification overlay: **1320 rows**, queue `1-1320` contiguous, no duplicate queue order

## Identity / recency controls

- Two cross-listed 福建 rows (王光远、叶善青) reuse sealed evidence only because repository `ambiguity_group_id + province + normalized name` match; each row keeps its independent `person_id`.
- The other 58 rows were freshly reviewed against current public government/federation/company/filing or authoritative-media evidence; 18 obtained safe current-role closure and 40 remain explicit unresolved.
- Source roles were refreshed rather than copied: 许阳阳 is current 达利食品集团总裁; 谢伟东 is current 海斯福董事长; 章高路 is current 安井食品联席董事长、执行董事; 赖世贤 is current 安踏集团执行董事、联席CEO并代理安踏品牌CEO.
- 王文礼 has multiple current Fujian homonyms and remains unresolved. 方华玉、吴有林、张桂潮 likewise remain unresolved where legal-entity continuity, current incumbency, or replacement role could not be safely proven.
- No current organization/title is assigned from a name-only hit.

**PASS**
'''
(E / "W3_BATCH_0022_VALIDATION.md").write_text(validation, encoding="utf-8")
status_path = P / "STATUS.yaml"
s = status_path.read_text(encoding="utf-8")
for a,b in {
    "code: W3-BATCH-0021\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED": "code: W3-BATCH-0022\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED",
    "code: W3-BATCH-0022\n  phase: W3-EVIDENCE-ENRICH\n  status: READY": "code: W3-BATCH-0023\n  phase: W3-EVIDENCE-ENRICH\n  status: READY",
    "batches_sealed: 21": "batches_sealed: 22",
    "processed_queue_rows: 1260": "processed_queue_rows: 1320",
    "next_queue_order: 1261": "next_queue_order: 1321",
    "actionable_queue_remaining: 9384": "actionable_queue_remaining: 9324",
    "processed: 1159": "processed: 1219",
    "remaining: 3172": "remaining: 3112",
    "identity_evidence_rows: 1260": "identity_evidence_rows: 1320",
    "current_org_title_confirmed_rows: 767": "current_org_title_confirmed_rows: 787",
    "current_org_title_unresolved_rows: 390": "current_org_title_unresolved_rows: 430",
}.items():
    assert a in s, a
    s = s.replace(a,b,1)
anchor = "  w3_batch_0021_validation: projects/fc-exec-2515/evidence/W3_BATCH_0021_VALIDATION.md\n"
assert anchor in s
s = s.replace(anchor, anchor + "  w3_batch_0022_results: projects/fc-exec-2515/evidence/W3_BATCH_0022_RESULTS.csv\n  w3_batch_0022_metrics: projects/fc-exec-2515/evidence/W3_BATCH_0022_METRICS.yaml\n  w3_batch_0022_validation: projects/fc-exec-2515/evidence/W3_BATCH_0022_VALIDATION.md\n", 1)
status_path.write_text(s, encoding="utf-8")

current_path = P / "CURRENT.yaml"
c = current_path.read_text(encoding="utf-8")
for a,b in {
    "current_gate: W3-BATCH-0022": "current_gate: W3-BATCH-0023",
    "work_cursor: 1260": "work_cursor: 1320",
    "verified_records: 769": "verified_records: 789",
    "unresolved_records: 9875": "unresolved_records: 9855",
    "processed: 1260": "processed: 1320",
    "actionable_remaining: 9384": "actionable_remaining: 9324",
    "next_queue_order: 1261": "next_queue_order: 1321",
    "processed: 1159": "processed: 1219",
    "remaining: 3172": "remaining: 3112",
}.items():
    assert a in c, a
    c = c.replace(a,b,1)
assert "last_input_head: da90d9648560196eb9819dd40894fbf01aa30a4b" in c
c = c.replace("last_input_head: da90d9648560196eb9819dd40894fbf01aa30a4b", f"last_input_head: {INPUT_HEAD}", 1)
c = re.sub(r"last_evidence_at: .*", f"last_evidence_at: {NOW}", c, count=1)
batch_block = f'''\nw3_batch_0022:\n  status: SEALED\n  validation: PASS\n  touched_rows: 60\n  fujian_rows: 60\n  p1_identity_rows: 60\n  evidence_backed_rows: 60\n  a_grade_rows: {grades['A']}\n  b_grade_rows: {grades['B']}\n  c_grade_rows: 0\n  current_org_title_confirmed_rows: {confirmed}\n  current_org_title_unresolved_rows: {unresolved}\n  unsupported_current_title_claims: 0\n\n'''
assert "notes:\n" in c
c = c.replace("notes:\n", batch_block + "notes:\n", 1)
c = c.rstrip() + f'''\n  - W3-BATCH-0022 processed queue orders 1261-1320 exactly, all 60 福建 P1 identity/current-role rows.\n  - {confirmed} rows received current organization/title confirmation; {unresolved} remain explicit unresolved; unsupported current-title claims remain zero.\n  - 王光远、叶善青 reused sealed evidence only through exact repository ambiguity_group_id + normalized name + province match; each source record retains its independent person_id.\n  - The other 58 rows received fresh current-web review: 18 were safely closed and 40 remain unresolved rather than inferred from name.\n  - Current-role refreshes include 许阳阳→达利食品集团总裁、谢伟东→海斯福董事长、章高路→安井食品联席董事长/执行董事、赖世贤→安踏集团执行董事/联席CEO并代理安踏品牌CEO.\n  - 王文礼 homonyms were explicitly rejected; 方华玉、吴有林、张桂潮 remain unresolved where legal-entity continuity or current replacement role is not safely proven.\n  - Evidence grades are A={grades['A']}, B={grades['B']}, C=0; next deterministic queue order is 1321.\n'''
current_path.write_text(c, encoding="utf-8")
print(f"PASS W3-BATCH-0022 confirmed={confirmed} unresolved={unresolved} grades={dict(grades)} next=1321")
