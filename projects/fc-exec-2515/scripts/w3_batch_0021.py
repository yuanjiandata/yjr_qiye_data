#!/usr/bin/env python3
import csv, gzip, glob, subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
P = ROOT / "projects" / "fc-exec-2515"
E = P / "evidence"
INPUT_HEAD = "da90d9648560196eb9819dd40894fbf01aa30a4b"
BATCH_START, BATCH_END = 1201, 1260
VERIFY_DATE = "2026-09-20"
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
assert Counter(r["province"] for r in rows) == Counter({"安徽": 34, "福建": 26})

# Sealed evidence may be reused only for repository-encoded cross-list identities:
# same ambiguity_group_id + province + normalized name. person_id remains independent.
by_order = {}
for fn in sorted(glob.glob(str(E / "W3_BATCH_*_RESULTS.csv"))):
    with open(fn, "r", encoding="utf-8-sig", newline="") as f:
        for x in csv.DictReader(f):
            if int(x["queue_order"]) < BATCH_START:
                by_order[int(x["queue_order"])] = x
by_ag = defaultdict(list)
for q in allq:
    by_ag[q["ambiguity_group_id"]].append(q)

# Fresh Fujian current-role closures. Each has either a current source that itself
# names the federation role, or a repository historical-organization key plus a
# current official/enterprise source. No name-only identity assignment is allowed.
special = {
    "王光远": dict(org="福建省工商业联合会", title="主席（兼福建省政协副主席）", grade="A", etype="federation_official_current_role", etitle="福建：税商联动筑牢民企合规经营防线", url="https://wap.acfic.org.cn/gdgslgz_14277/202607/t20260701_327276.html", date="2026-07-01", notes="全国工商联2026-07官方稿直接写明福建省政协副主席、省工商联主席王光远；与2022福建省工商联十二届主席身份连续闭合。"),
    "陈晞": dict(org="福建省工商业联合会", title="党组书记（兼中共福建省委统战部副部长）", grade="A", etype="federation_official_current_role", etitle="福建：省工商联重点民营企业建立完善中国特色现代企业制度培训班暨一企一策调研服务座谈交流活动举行", url="https://www.acfic.org.cn/gdgslgz/fj/bjgslgz/202608/t20260806_330299.html", date="2026-08-06", notes="全国工商联2026-08官方稿直接写明省委统战部副部长、省工商联党组书记陈晞；不沿用源表较早常务副主席标签。"),
    "陈飚": dict(org="福建省工商业联合会", title="党组成员、副主席", grade="A", etype="federation_official_current_role", etitle="福建：省工商联重点民营企业建立完善中国特色现代企业制度培训班暨一企一策调研服务座谈交流活动举行", url="https://www.acfic.org.cn/gdgslgz/fj/bjgslgz/202608/t20260806_330299.html", date="2026-08-06", notes="全国工商联2026-08官方稿直接写明省工商联党组成员、副主席陈飚。"),
    "林龙金": dict(org="福建省工商业联合会", title="副主席", grade="A", etype="federation_official_current_role", etitle="福建：税商联动筑牢民企合规经营防线", url="https://wap.acfic.org.cn/gdgslgz_14277/202607/t20260701_327276.html", date="2026-07-01", notes="全国工商联2026-07官方稿直接写明福建省工商联副主席林龙金。"),
    "余建": dict(org="福建省工商业联合会", title="党组成员、副主席", grade="B", etype="formal_association_current_role", etitle="福建省工商联党组成员、副主席余建出席相关活动", url="https://www.mszz.cn/cccu/shdt/171096.html", date="2026-02-06", notes="2026-02商会公开材料写明福建省工商联党组成员、副主席余建；与福建省发改委2025官方活动中的同职务形成连续性。"),
    "叶善青": dict(org="福建省工商业联合会", title="党组成员、副主席", grade="A", etype="federation_official_current_role", etitle="福建：省工商联重点民营企业建立完善中国特色现代企业制度培训班暨一企一策调研服务座谈交流活动举行", url="https://www.acfic.org.cn/gdgslgz/fj/bjgslgz/202608/t20260806_330299.html", date="2026-08-06", notes="全国工商联2026-08官方稿直接写明省工商联党组成员、副主席叶善青。"),
    "许清流": dict(org="福建省工商业联合会", title="副主席", grade="A", etype="cppcc_official_current_federation_role", etitle="全国政协委员许清流相关履职报道", url="https://www.cppcc.gov.cn/zxww/2026/02/03/ARTI1770082659959132.shtml", date="2026-02-03", notes="全国政协官网2026-02明确许清流为全国政协委员、福建省工商联副主席，直接闭合源身份；企业职务未用低等级来源覆盖。"),
    "吴华新": dict(org="永荣控股集团有限公司", title="董事长", grade="A", etype="enterprise_official_current_role_with_historical_org_bridge", etitle="永荣控股集团2026企业新闻", url="https://www.eversun-chn.com/news-detail/2061356007639293952.html", date="2026-06-01", notes="源记录已含永荣控股历史组织键；永荣控股2026企业官网明确董事长吴华新，结合2022省工商联副主席官方名册闭合身份，不以姓名单字段匹配。"),
    "吴凯庭": dict(org="厦门盈趣科技股份有限公司", title="董事", grade="A", etype="enterprise_official_current_role_with_historical_org_bridge", etitle="盈趣科技十五五开新局：持续加码科技创新投入", url="https://www.intretech.com.cn/Ne_d_gci_19_id_236.html", date="2026-03-02", notes="源记录已有盈趣科技/万利达历史组织键；盈趣科技2026企业官网明确吴凯庭董事参会，结合2022省工商联副主席名册闭合。"),
    "吴荣照": dict(org="鸿星尔克集团", title="党委书记、董事长", grade="A", etype="government_official_current_role_with_historical_org_bridge", etitle="鸿星尔克吴荣照：深耕践行晋江经验 做强国民运动品牌", url="https://www.jinjiang.gov.cn/xxgk/jjyw/202605/t20260507_3289419.htm", date="2026-05-07", notes="源记录已有鸿星尔克历史组织键；晋江市政府2026-05直接写明鸿星尔克集团党委书记、董事长吴荣照。"),
    "邹剑寒": dict(org="奥佳华智能健康科技集团股份有限公司", title="董事长、总经理", grade="B", etype="current_listed_company_announcement_reporting_with_historical_org_bridge", etitle="奥佳华：邹剑寒当选董事长并任总经理", url="https://cj.sina.com.cn/articles/view/7935425109/1d8fcfa5502001llwi", date="2026-09-16", notes="源记录已有奥佳华董事长历史组织键；2026-09公司换届公告报道明确邹剑寒当选董事长并获聘总经理，结合2022省工商联副主席名册闭合。"),
    "张轩松": dict(org="永辉超市股份有限公司", title="董事长", grade="A", etype="enterprise_official_current_role_with_historical_org_bridge", etitle="张轩松：在AI浪潮中凸显人才价值", url="https://www.yonghui.com.cn/html/web/latestnews/meitijujiao/2031273524945752066.html", date="2026-03-10", notes="源记录已有永辉集团历史组织键；永辉官网2026-03明确全国政协委员、永辉超市董事长张轩松，结合2022省工商联副主席名册闭合。"),
    "林孝发": dict(org="九牧集团", title="党委书记、董事长", grade="A", etype="government_official_current_role_with_historical_org_bridge", etitle="福建省工信系统全国两会代表委员履职报道", url="https://gxt.fujian.gov.cn/zwgk/xw/hydt/snhydt/202603/t20260309_7107501.htm", date="2026-03-09", notes="源记录已有九牧集团董事长历史组织键；福建省工信厅2026-03明确林孝发为九牧集团党委书记、董事长。"),
    "林国镜": dict(org="福建大东海实业集团有限公司", title="董事长", grade="B", etype="authoritative_media_current_role_with_historical_org_bridge", etitle="福建省优秀民营企业家拟表彰对象公示", url="https://news.xmnn.cn/fjxw/202608/t20260816_445282.html", date="2026-08-17", notes="源记录已有福建大东海集团董事长历史组织键；2026-08福建日报来源公示列林国镜为福建大东海实业集团有限公司董事长。"),
    "林治良": dict(org="福州市工商业联合会", title="主席（兼福州市政协副主席）", grade="A", etype="federation_official_current_role", etitle="福建：中国福州国际招商月民企专场招商对接会召开", url="https://www.acfic.org.cn/gdgslgz/fj/bjgslgz/202605/t20260525_326343.html", date="2026-05-25", notes="全国工商联2026-05官方稿直接写明福州市政协副主席、市工商联主席林治良；与2022省工商联副主席源身份形成工商联系统连续链。"),
    "周少雄": dict(org="福建七匹狼实业股份有限公司", title="董事长", grade="B", etype="authoritative_financial_media_current_role_with_historical_org_bridge", etitle="七匹狼董事长周少雄：当前品牌状态是稳中有进 结构优化", url="https://www.stcn.com/article/detail/3781618.html", date="2026-04-22", notes="源记录已有七匹狼实业董事长历史组织键；证券时报网2026-04当前采访明确周少雄为七匹狼董事长。"),
    "黄世霖": dict(org="福建时代星云科技有限公司", title="董事长", grade="A", etype="government_portal_current_role_with_federation_identity", etitle="人工智能+如何补齐短板？福建省政协专题议政性常委会献良策", url="https://www.digitalchina.gov.cn/2026/xwzx/szkx/202606/t20260618_5335915.htm", date="2026-06-18", notes="数字中国建设峰会政府门户2026-06直接写明福建省政协常委、省工商联副主席、福建时代星云科技有限公司董事长黄世霖；并纠正源表已过时的宁德时代副董事长职务。"),
    "曹晖": dict(org="福耀玻璃工业集团股份有限公司", title="董事长", grade="A", etype="federation_official_current_role_and_enterprise", etitle="福建：让民营经济的广袤森林更加郁郁葱葱", url="https://wap.acfic.org.cn/gdgslgz_14277/202607/t20260714_327529.html", date="2026-07-14", notes="全国工商联2026-07官方稿同段直接写明福建省工商联副主席、省民营企业商会会长、福耀集团董事长曹晖。"),
    "蔡劲军": dict(org="福建火炬电子科技股份有限公司", title="董事长", grade="B", etype="authoritative_media_current_role_with_federation_identity", etitle="教育科技人才发展如何一体推进？福建省政协探寻更优实践路径", url="https://finance.sina.com.cn/roll/2026-09-05/doc-iniqupts5096447.shtml", date="2026-09-05", notes="新华社2026-09报道直接写明福建省政协常委、福建省工商联副主席、福建火炬电子科技股份有限公司董事长蔡劲军，身份与现职同时闭合。"),
    "蔡金钗": dict(org="福建盼盼食品集团", title="总裁", grade="B", etype="authoritative_media_current_role_with_federation_identity", etitle="泉州公安：破获经济犯罪案件570余起", url="https://www.cnr.cn/fj/yw/20260514/t20260514_527619461.shtml", date="2026-05-14", notes="央广网2026-05同段直接写明十四届全国人大代表、福建省工商联副主席、福建盼盼食品集团总裁蔡金钗。"),
}

fresh_unresolved = {
    "林湫": "已检索到2026年南平市副市长/市工商联主席相关公开报道，但本轮未取得足够强的官方跨来源身份桥，把该现职与源记录中的福建省工商联副主席身份安全闭合，故不按姓名直接挂接。",
    "郑辉": "针对2026年福建工商联、政府、企业公开资料检索，未找到可同时闭合源省工商联副主席身份与当前单位职务的高可信证据。",
    "郑玉琳": "针对2026年福建工商联、政府、企业公开资料检索，未找到可同时闭合源省工商联副主席身份与当前单位职务的高可信证据。",
    "施天佑": "可检索到2026年百宏实业控股联席主席同名信息，但源表组织为福建百宏聚纤科技实业有限公司，当前法律实体/职务链未获得足够官方桥接，故不冒进归并。",
    "洪杰": "三棵树企业官网可确认2026年董事长兼总裁洪杰，但源记录缺少历史组织键，尚无当前官方材料同时写明其福建省工商联副主席身份，避免仅凭姓名+省份挂接。",
    "傅芬芳": "2026年上市公司年报资料支持圣农发展董事、总经理傅芬芳，源表则为福建圣农实业有限公司董事长；本轮未取得当前省工商联身份与新职务的直接桥接，保留未决。",
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
        result = {**base, "identity_resolution": "REUSED_SEALED_EVIDENCE_SAME_REPOSITORY_AMBIGUITY_GROUP", "current_organization": prev["current_organization"], "current_title": prev["current_title"], "current_verification_status": prev["current_verification_status"], "evidence_type": prev["evidence_type"], "evidence_grade": prev["evidence_grade"], "evidence_title": prev["evidence_title"], "evidence_url": prev["evidence_url"], "evidence_date": prev["evidence_date"], "unresolved_reason": prev["unresolved_reason"], "research_notes": "与已封存 queue {} 同省、同名且同 ambiguity_group_id={}；复用其证据但保留独立 person_id，不做姓名合并。".format(p["queue_order"], r["ambiguity_group_id"]) + prev["research_notes"]}
    elif name in special:
        s = special[name]
        result = {**base, "identity_resolution": "CURRENT_ROLE_CONFIRMED_WITH_CONTEXTUAL_IDENTITY_BRIDGE", "current_organization": s["org"], "current_title": s["title"], "current_verification_status": "CURRENT_ORG_TITLE_CONFIRMED", "evidence_type": s["etype"], "evidence_grade": s["grade"], "evidence_title": s["etitle"], "evidence_url": s["url"], "evidence_date": s["date"], "unresolved_reason": "", "research_notes": s["notes"] + f" 历史身份锚点：{FJ_HIST}"}
    else:
        assert r["province"] == "福建" and name in fresh_unresolved, (r["queue_order"], name)
        result = {**base, "identity_resolution": "HISTORICAL_IDENTITY_CURRENT_ROLE_UNRESOLVED", "current_organization": "", "current_title": "", "current_verification_status": "UNRESOLVED_CURRENT_ORG_TITLE", "evidence_type": "federation_official_historical_identity_plus_targeted_current_research", "evidence_grade": "A", "evidence_title": "福建省工商业联合会（总商会）第十二届执委会名单", "evidence_url": FJ_HIST, "evidence_date": "2022-08-30", "unresolved_reason": fresh_unresolved[name], "research_notes": f"2026-09-20已针对政府、全国工商联、企业官网、上市公司/权威媒体进行当前角色检索；因身份桥或时效性不足保持未决。历史身份锚点：{FJ_HIST}"}
    results.append(result)

out = E / "W3_BATCH_0021_RESULTS.csv"
with out.open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(results)

# Append cumulative evidence ledger and verification overlay.
ledger_path = E / "W3_EVIDENCE_LEDGER.csv"
with ledger_path.open("r", encoding="utf-8-sig", newline="") as f:
    old_ledger = list(csv.DictReader(f)); ledger_fields = list(old_ledger[0].keys())
assert len(old_ledger) == 1200
new_ledger = old_ledger + [{k: {"queue_order": x["queue_order"], "person_id": x["person_id"], "province": x["province"], "excel_row": x["excel_row"], "candidate_names": x["candidate_names"], "evidence_type": x["evidence_type"], "evidence_grade": x["evidence_grade"], "evidence_title": x["evidence_title"], "evidence_url": x["evidence_url"], "evidence_date": x["evidence_date"], "current_verification_status": x["current_verification_status"], "unresolved_reason": x["unresolved_reason"]}.get(k, "") for k in ledger_fields} for x in results]
with ledger_path.open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=ledger_fields); w.writeheader(); w.writerows(new_ledger)

overlay_path = E / "W3_VERIFICATION_OVERLAY.csv"
with overlay_path.open("r", encoding="utf-8-sig", newline="") as f:
    old_overlay = list(csv.DictReader(f)); overlay_fields = list(old_overlay[0].keys())
assert len(old_overlay) == 1200
new_overlay = old_overlay + [{k: {"queue_order": x["queue_order"], "person_id": x["person_id"], "province": x["province"], "excel_row": x["excel_row"], "identity_resolution": x["identity_resolution"], "candidate_names": x["candidate_names"], "current_organization": x["current_organization"], "current_title": x["current_title"], "current_verification_status": x["current_verification_status"], "evidence_grade": x["evidence_grade"], "evidence_url": x["evidence_url"], "unresolved_reason": x["unresolved_reason"]}.get(k, "") for k in overlay_fields} for x in results]
with overlay_path.open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=overlay_fields); w.writeheader(); w.writerows(new_overlay)

statuses = Counter(x["current_verification_status"] for x in results)
grades = Counter(x["evidence_grade"] for x in results)
confirmed = statuses["CURRENT_ORG_TITLE_CONFIRMED"]
unresolved = statuses["UNRESOLVED_CURRENT_ORG_TITLE"]
assert confirmed == 40 and unresolved == 20, (confirmed, unresolved)
assert grades == Counter({"A": 51, "B": 9}), grades
assert len(new_ledger) == 1260 and len(new_overlay) == 1260
assert [int(x["queue_order"]) for x in new_ledger] == list(range(1, 1261))
assert [int(x["queue_order"]) for x in new_overlay] == list(range(1, 1261))
assert len({x["queue_order"] for x in new_ledger}) == 1260
assert len({x["queue_order"] for x in new_overlay}) == 1260
assert all((x["evidence_url"] or x["unresolved_reason"]) for x in results)
assert all(not (x["current_verification_status"] == "CURRENT_ORG_TITLE_CONFIRMED" and (not x["current_organization"] or not x["current_title"] or not x["evidence_url"])) for x in results)
assert all(not (x["identity_resolution"].startswith("CURRENT_ROLE_CONFIRMED") and x["name_normalized"] in fresh_unresolved) for x in results)

metrics = f'''schema: fc-exec-2515-w3-batch-metrics-v1
project_id: FC-EXEC-2515-01
gate: W3-BATCH-0021
status: SEALED
validation: PASS
touched_rows: 60
anhui_rows: 34
fujian_rows: 26
p1_identity_rows: 60
evidence_backed_rows: 60
a_grade_rows: {grades['A']}
b_grade_rows: {grades['B']}
c_grade_rows: 0
current_org_title_confirmed_rows: {confirmed}
current_org_title_unresolved_rows: {unresolved}
unsupported_current_title_claims: 0
queue_start: 1201
queue_end: 1260
next_queue_order: 1261
verified_at: {NOW}
input_head: {INPUT_HEAD}
'''
(E / "W3_BATCH_0021_METRICS.yaml").write_text(metrics, encoding="utf-8")
validation = f'''# W3-BATCH-0021 Validation

- Gate: `W3-BATCH-0021`
- Queue orders: `1201-1260`
- Touched rows: **60** (`安徽 34`, `福建 26`)
- Priority: `P1_IDENTITY` 60
- Evidence coverage: **60/60**
- Evidence grades: **A={grades['A']}, B={grades['B']}, C=0**
- Current organization + title confirmed: **{confirmed}**
- Explicit current-role unresolved: **{unresolved}**
- Unsupported current-title claims: **0**
- Cumulative evidence ledger: **1260 rows**, queue `1-1260` contiguous, no duplicate queue order
- Cumulative verification overlay: **1260 rows**, queue `1-1260` contiguous, no duplicate queue order

## Identity / recency controls

- 34 安徽 rows are repository-encoded cross-list identities and reuse already sealed evidence only when `ambiguity_group_id + province + normalized name` all match; each source row retains its own `person_id`.
- All 26 福建 first-occurrence identities were researched against current public government/federation/enterprise/filing or authoritative-media evidence, with the 2022 official 福建省工商联 roster used only as the historical identity anchor.
- 20 福建 rows obtained a safe current-role closure; six (林湫、郑辉、郑玉琳、施天佑、洪杰、傅芬芳) remain explicit unresolved because the current identity bridge was not strong enough or the legal-entity/role chain changed.
- Stale source roles were not carried forward: 黄世霖 is refreshed from old 宁德时代副董事长 to current 福建时代星云科技有限公司董事长; 蔡劲军 is refreshed to current 火炬电子董事长; 邹剑寒 is refreshed to current 奥佳华董事长、总经理.
- No current organization/title is assigned from a name-only hit.

**PASS**
'''
(E / "W3_BATCH_0021_VALIDATION.md").write_text(validation, encoding="utf-8")

status_path = P / "STATUS.yaml"
s = status_path.read_text(encoding="utf-8")
for a,b in {
    "code: W3-BATCH-0020\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED": "code: W3-BATCH-0021\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED",
    "code: W3-BATCH-0021\n  phase: W3-EVIDENCE-ENRICH\n  status: READY": "code: W3-BATCH-0022\n  phase: W3-EVIDENCE-ENRICH\n  status: READY",
    "batches_sealed: 20": "batches_sealed: 21",
    "processed_queue_rows: 1200": "processed_queue_rows: 1260",
    "next_queue_order: 1201": "next_queue_order: 1261",
    "actionable_queue_remaining: 9444": "actionable_queue_remaining: 9384",
    "processed: 1099": "processed: 1159",
    "remaining: 3232": "remaining: 3172",
    "identity_evidence_rows: 1200": "identity_evidence_rows: 1260",
    "current_org_title_confirmed_rows: 727": "current_org_title_confirmed_rows: 767",
    "current_org_title_unresolved_rows: 370": "current_org_title_unresolved_rows: 390",
}.items():
    assert a in s, a
    s = s.replace(a,b,1)
anchor = "  w3_batch_0020_validation: projects/fc-exec-2515/evidence/W3_BATCH_0020_VALIDATION.md\n"
assert anchor in s
s = s.replace(anchor, anchor + "  w3_batch_0021_results: projects/fc-exec-2515/evidence/W3_BATCH_0021_RESULTS.csv\n  w3_batch_0021_metrics: projects/fc-exec-2515/evidence/W3_BATCH_0021_METRICS.yaml\n  w3_batch_0021_validation: projects/fc-exec-2515/evidence/W3_BATCH_0021_VALIDATION.md\n",1)
status_path.write_text(s, encoding="utf-8")

current_path = P / "CURRENT.yaml"
c = current_path.read_text(encoding="utf-8")
for a,b in {
    "current_gate: W3-BATCH-0021": "current_gate: W3-BATCH-0022",
    "work_cursor: 1200": "work_cursor: 1260",
    "verified_records: 729": "verified_records: 769",
    "unresolved_records: 9915": "unresolved_records: 9875",
    "processed: 1200": "processed: 1260",
    "actionable_remaining: 9444": "actionable_remaining: 9384",
    "next_queue_order: 1201": "next_queue_order: 1261",
    "processed: 1099": "processed: 1159",
    "remaining: 3232": "remaining: 3172",
}.items():
    assert a in c, a
    c = c.replace(a,b,1)
assert "last_input_head: 6c190cdb77530ca81234a7242d3b34bf61650219" in c
c = c.replace("last_input_head: 6c190cdb77530ca81234a7242d3b34bf61650219", f"last_input_head: {INPUT_HEAD}",1)
import re
c = re.sub(r"last_evidence_at: .*", f"last_evidence_at: {NOW}", c, count=1)
batch_block = f'''\nw3_batch_0021:\n  status: SEALED\n  validation: PASS\n  touched_rows: 60\n  anhui_rows: 34\n  fujian_rows: 26\n  p1_identity_rows: 60\n  evidence_backed_rows: 60\n  a_grade_rows: {grades['A']}\n  b_grade_rows: {grades['B']}\n  c_grade_rows: 0\n  current_org_title_confirmed_rows: {confirmed}\n  current_org_title_unresolved_rows: {unresolved}\n  unsupported_current_title_claims: 0\n\n'''
assert "notes:\n" in c
c = c.replace("notes:\n", batch_block + "notes:\n",1)
c = c.rstrip() + f'''\n  - W3-BATCH-0021 processed queue orders 1201-1260 exactly: 34 安徽 + 26 福建 P1 identity/current-role rows.\n  - {confirmed} rows received current organization/title confirmation; {unresolved} remain explicit unresolved; unsupported current-title claims remain zero.\n  - 34 安徽 cross-list rows reused sealed evidence only when repository ambiguity_group_id + normalized name + province matched; every source row retains an independent person_id.\n  - All 26 福建 first-occurrence identities received fresh public-web research. Twenty were safely closed with current federation/government/enterprise/authoritative evidence; six remain unresolved rather than inferred by name.\n  - 黄世霖 was corrected from stale 宁德时代副董事长 to current 福建时代星云科技有限公司董事长; 蔡劲军 and 邹剑寒 were likewise refreshed to current corporate roles.\n  - Evidence grades are A={grades['A']}, B={grades['B']}, C=0; next deterministic queue order is 1261.\n'''
current_path.write_text(c, encoding="utf-8")
print(f"PASS W3-BATCH-0021 confirmed={confirmed} unresolved={unresolved} grades={dict(grades)} next=1261")
