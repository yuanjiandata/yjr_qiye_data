#!/usr/bin/env python3
import csv
import gzip
import subprocess
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
P = ROOT / "projects" / "fc-exec-2515"
E = P / "evidence"
INPUT_HEAD = "8a5dc82dd8ef8001e12b57db7438e5515262d056"
BATCH_START, BATCH_END = 1081, 1140
VERIFY_DATE = "2026-09-20"
NOW = datetime.now(timezone(timedelta(hours=8))).replace(microsecond=0).isoformat()
AH_LIVE = "https://www.ahgcc.cn/Survey/"
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

# Live 安徽省工商联（总商会） leadership surface, freshly checked 2026-09-20.
# These are direct current organization/title statements on the official federation page.
ah_live = {
    "王光平": ("安徽光太实业集团", "总裁"),
    "徐进": ("安徽口子酒业股份有限公司", "董事长"),
    "徐珍玉": ("安徽朗坤物联网有限公司", "董事长"),
    "余竹云": ("中环控股集团有限公司", "董事长"),
    "卢立新": ("安徽共生物流科技有限公司", "董事长"),
    "李健": ("安徽宣酒集团股份有限公司", "董事长、党委副书记"),
    "朱圣杰": ("安徽人和节能科技有限责任公司", "董事长"),
    "冯雷": ("合肥维天运通信息科技股份有限公司", "董事长"),
    "徐玉美": ("安徽国邦实业集团", "董事长"),
    "李万军": ("安徽智飞龙科马生物制药有限公司", "董事长"),
    "姚和平": ("安徽安利材料科技股份有限公司", "党委书记、董事长、总经理"),
    "刘庆峰": ("科大讯飞股份有限公司", "董事长"),
    "陈冬梅": ("合肥华泰集团股份有限公司", "董事长"),
    "丁超毅": ("安徽绿桐科技有限公司", "董事长"),
    "王正前": ("合肥安达创展科技股份有限公司", "董事长、总经理"),
    "卢育发": ("安徽天柱绿色能源科技有限公司", "总经理"),
    "吕彬": ("安徽瓦大现代农业科技有限公司", "董事长"),
    "朱玉荣": ("安徽文香信息技术有限公司", "董事长"),
    "刘伟": ("宏晶微电子科技股份有限公司", "董事长"),
    "何仿": ("合肥京东方医院", "院长"),
    "沈君": ("安徽致君利再生科技有限公司", "董事长"),
    "周伊凡": ("安徽富煌建设有限责任公司", "董事、总经理；兼合肥富煌君达高科信息技术有限公司董事长"),
    "臧牧": ("安徽皖仪科技股份有限公司", "董事长兼总经理"),
    "潘斌": ("安徽环新集团股份有限公司", "总经理助理；兼安徽环新创业投资管理有限公司董事长"),
    "潘道伟": ("三只松鼠股份有限公司", "党委书记、行政总经理"),
}

# Current-role closures that require an explicit historical federation identity bridge.
special = {
    "徐善水": {
        "org": "安徽集友新材料股份有限公司", "title": "董事长、总裁",
        "grade": "A", "etype": "stock_exchange_filing_with_historical_federation_identity_bridge",
        "etitle": "安徽集友新材料股份有限公司2026年股东会材料",
        "url": "https://big5.sse.com.cn/site/cht/www.sse.com.cn/disclosure/listedinfo/announcement/c/new/2026-04-03/603429_20260403_90XW.pdf",
        "date": "2026-04-03",
        "notes": "2022全国工商联安徽换届名册锚定安徽省总商会副会长/常委身份；上交所2026披露明确徐善水现任董事长、总裁。",
    },
    "朱有为": {
        "org": "马鞍山锐生工贸有限公司", "title": "总经理",
        "grade": "A", "etype": "federation_official_current_role_with_historical_identity_bridge",
        "etitle": "含山县工商联：马鞍山市无为商会来含开展考察交流活动",
        "url": "https://www.ahgcc.cn/News/show/277765.html", "date": "2026-07-06",
        "notes": "安徽省工商联2026-07官方稿明确朱有为为马鞍山锐生工贸有限公司总经理，并给出马鞍山市总商会副会长、无为商会会长上下文；与2022省工商联常委身份闭合。",
    },
    "孙四平": {
        "org": "芜湖市工商业联合会", "title": "主席",
        "grade": "A", "etype": "government_official_current_federation_role_with_historical_identity_bridge",
        "etitle": "中共芜湖市委召开党外人士座谈会",
        "url": "https://whsggj.wuhu.gov.cn/xwzx/szyw/8953646.html", "date": "2026-09-01",
        "notes": "2026-09芜湖政府系统报道明确市工商联主席孙四平；2022安徽省工商联常委名册提供省级身份锚点。",
    },
    "李颖": {
        "org": "安徽省工商业联合会", "title": "对外联络处处长、一级调研员",
        "grade": "A", "etype": "federation_official_current_staff_role_with_same_federation_identity_bridge",
        "etitle": "于军赴上海市工商联开展深化对口合作工作",
        "url": "https://www.ahgcc.cn/News/show/274199.html", "date": "2025-11-14",
        "notes": "安徽省工商联官方稿直接写明李颖现任对外联络处处长、一级调研员；与同一省工商联系统历史常委记录闭合，同名外部命中不采纳。",
    },
    "杨乐": {
        "org": "安徽金禾实业股份有限公司", "title": "董事长",
        "grade": "A", "etype": "stock_exchange_filing_with_historical_federation_identity_bridge",
        "etitle": "金禾实业第七届董事会第八次会议决议公告",
        "url": "https://disc.static.szse.cn/disc/disk03/finalpage/2026-06-27/758c0175-f145-4638-adbe-cade38b6bf77.PDF", "date": "2026-06-27",
        "notes": "2022安徽省工商联常委名册提供身份锚点；深交所2026-06公告明确会议由董事长杨乐主持，且公司为安徽金禾实业股份有限公司。",
    },
    "吴涛": {
        "org": "淮南市工商业联合会", "title": "党组书记",
        "grade": "A", "etype": "government_official_role_with_historical_federation_identity_bridge",
        "etitle": "市审计局召开市工商联党组书记吴涛、主席杜本硕同志任期经济责任审计进点见面会",
        "url": "https://sjj.huainan.gov.cn/xwzx/jgdt/551844389.html", "date": "2025-10-31",
        "notes": "淮南市审计局官方任期审计稿明确吴涛为市工商联党组书记；结合2022安徽省工商联常委名册，不从其他同名记录推断。针对2026公开信息未发现权威更替证据。",
    },
    "杜本硕": {
        "org": "淮南市工商业联合会", "title": "主席",
        "grade": "A", "etype": "government_official_role_with_historical_federation_identity_bridge",
        "etitle": "市审计局召开市工商联党组书记吴涛、主席杜本硕同志任期经济责任审计进点见面会",
        "url": "https://sjj.huainan.gov.cn/xwzx/jgdt/551844389.html", "date": "2025-10-31",
        "notes": "淮南市审计局官方任期审计稿明确杜本硕为市工商联主席；2022安徽省工商联常委名册为身份锚点。2026检察系统同名命中无身份桥，明确排除而不串人。",
    },
    "邵迪": {
        "org": "宿州市工商业联合会", "title": "主席（宿州市政协副主席）",
        "grade": "A", "etype": "federation_official_current_local_role_with_historical_identity_bridge",
        "etitle": "宿州市工商联赴沪杭招商考察 深化产业对接与商会联动",
        "url": "https://www.ahgcc.cn/News/show/277629.html", "date": "2026-06-26",
        "notes": "安徽省工商联2026-06官方稿明确邵迪为宿州市政协副主席、市工商联主席；2022省工商联常委名册含邵迪（女），身份上下文一致。",
    },
    "胡守斌": {
        "org": "中国人民政治协商会议淮北市委员会", "title": "副主席（兼致公党淮北市委会主委）",
        "grade": "A", "etype": "government_official_current_role_plus_local_federation_history_bridge",
        "etitle": "淮北市召开药械行业协会一届六次会员代表大会",
        "url": "https://amr.huaibei.gov.cn/gszx/gskx/58021245.html", "date": "2026-03-03",
        "notes": "2024淮北理工学院公开稿明确同一胡守斌当时为淮北市政协副主席、工商联主席，建立工商联身份桥；2026淮北市市场监管局更新其现职为市政协副主席、致公党市委会主委，不机械沿用旧工商联主席。",
    },
    "姚亚妹": {
        "org": "合肥市工商业联合会", "title": "主席（合肥市人大常委会副主任）",
        "grade": "B", "etype": "authoritative_media_current_role_plus_government_federation_history_bridge",
        "etitle": "全市民营经济统战工作暨民营企业家座谈会召开",
        "url": "https://www.sohu.com/a/1029559957_121106832", "date": "2026-05-29",
        "notes": "2024合肥市瑶海区政府稿明确姚亚妹为市政协副主席、工商联主席，形成身份桥；2026合肥会议报道更新为市人大常委会副主任、市工商联主席。当前职务来源为权威会议转发稿，保守定B。",
    },
    "邰紫鹏": {
        "org": "泰尔重工股份有限公司", "title": "党委书记、董事长",
        "grade": "A", "etype": "enterprise_official_current_role_with_federation_identity_bridge",
        "etitle": "泰尔重工2026当前官网新闻/党委换届",
        "url": "https://www.taiergroup.com/", "date": VERIFY_DATE,
        "notes": "泰尔重工官网2026当前页面及5月/6月企业新闻明确邰紫鹏为党委书记、董事长；2022省工商联常委/副会长身份提供桥接。旧省工商联页面的总经理表述不再沿用。",
    },
}

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
    elif name in ah_live:
        org, title = ah_live[name]
        result = {**base,
            "identity_resolution": "CURRENT_ROLE_CONFIRMED_BY_LIVE_OFFICIAL_ANHUI_LEADERSHIP_PAGE",
            "current_organization": org, "current_title": title,
            "current_verification_status": "CURRENT_ORG_TITLE_CONFIRMED",
            "evidence_type": "federation_official_live_current_role",
            "evidence_grade": "A", "evidence_title": "安徽省工商联（总商会）现任领导/商会概况",
            "evidence_url": AH_LIVE, "evidence_date": VERIFY_DATE,
            "unresolved_reason": "",
            "research_notes": "2026-09-20重新核验安徽省工商联（总商会）官方现任领导页面；页面直接把该工商联身份与当前企业/机构职务关联。历史2022执行委员会名册仅作身份锚点。",
        }
    else:
        result = {**base,
            "identity_resolution": "HISTORICAL_IDENTITY_CURRENT_ROLE_UNRESOLVED",
            "current_organization": "", "current_title": "",
            "current_verification_status": "UNRESOLVED_CURRENT_ORG_TITLE",
            "evidence_type": "federation_official_historical_identity_plus_targeted_current_research",
            "evidence_grade": "A", "evidence_title": "安徽省工商联第十二届执行委员会名单",
            "evidence_url": AH_HIST, "evidence_date": VERIFY_DATE,
            "unresolved_reason": "2022官方安徽省工商联名册可确认源身份；本轮针对2026公开网页、政府/工商联/企业/交易所信息检索，未找到足以在不依赖姓名单字段的前提下安全闭合的当前单位+职务。",
            "research_notes": "保持未决；同名命中、旧职务或缺少工商联身份桥的候选均未写入。",
        }
    results.append(result)

fields = [
    "queue_order","person_id","province","excel_row","name_normalized","source_federation_role",
    "identity_resolution","candidate_names","current_organization","current_title",
    "current_verification_status","evidence_type","evidence_grade","evidence_title","evidence_url",
    "evidence_date","unresolved_reason","research_notes",
]
out = E / "W3_BATCH_0019_RESULTS.csv"
with out.open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(results)

# Append deterministic ledger + overlay.
ledger_path = E / "W3_EVIDENCE_LEDGER.csv"
with ledger_path.open("r", encoding="utf-8-sig", newline="") as f:
    old_ledger = list(csv.DictReader(f)); ledger_fields = list(old_ledger[0].keys())
assert len(old_ledger) == 1080
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
assert len(old_overlay) == 1080
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
assert confirmed == 37 and unresolved == 23, (confirmed, unresolved)
assert grades == Counter({"A": 59, "B": 1}), grades
assert len(new_ledger) == 1140 and len(new_overlay) == 1140
assert [int(x["queue_order"]) for x in new_ledger] == list(range(1, 1141))
assert [int(x["queue_order"]) for x in new_overlay] == list(range(1, 1141))
assert len({x["queue_order"] for x in new_ledger}) == 1140
assert len({x["queue_order"] for x in new_overlay}) == 1140
assert all((x["evidence_url"] or x["unresolved_reason"]) for x in results)
assert all(not (x["current_verification_status"] == "CURRENT_ORG_TITLE_CONFIRMED" and (not x["current_organization"] or not x["current_title"] or not x["evidence_url"])) for x in results)

metrics = f'''schema: fc-exec-2515-w3-batch-metrics-v1\nproject_id: FC-EXEC-2515-01\ngate: W3-BATCH-0019\nstatus: SEALED\nvalidation: PASS\ntouched_rows: 60\nanhui_rows: 60\np1_identity_rows: 60\nevidence_backed_rows: 60\na_grade_rows: {grades['A']}\nb_grade_rows: {grades['B']}\nc_grade_rows: 0\ncurrent_org_title_confirmed_rows: {confirmed}\ncurrent_org_title_unresolved_rows: {unresolved}\nunsupported_current_title_claims: 0\nqueue_start: 1081\nqueue_end: 1140\nnext_queue_order: 1141\nverified_at: {NOW}\ninput_head: {INPUT_HEAD}\n'''
(E / "W3_BATCH_0019_METRICS.yaml").write_text(metrics, encoding="utf-8")

validation = f'''# W3-BATCH-0019 Validation\n\n- Gate: `W3-BATCH-0019`\n- Queue orders: `1081-1140`\n- Touched rows: **60** (`安徽 60`)\n- Priority: `P1_IDENTITY` 60\n- Evidence coverage: **60/60**\n- Evidence grades: **A={grades['A']}, B={grades['B']}, C=0**\n- Current organization + title confirmed: **{confirmed}**\n- Explicit current-role unresolved: **{unresolved}**\n- Unsupported current-title claims: **0**\n- Cumulative evidence ledger: **1140 rows**, queue `1-1140` contiguous, no duplicate queue order\n- Cumulative verification overlay: **1140 rows**, queue `1-1140` contiguous, no duplicate queue order\n\n## Identity / recency controls\n\n- The 2022 ACFIC 安徽 execution roster is used only as an identity/history anchor, never as present-tense employment authority.\n- The live 安徽省工商联（总商会） leadership page was freshly checked on {VERIFY_DATE}; direct current claims are written only where that page links the person to a current enterprise/organization role.\n- Additional current-role closures use public government, federation, enterprise, or stock-exchange evidence plus a federation-history bridge.\n- Same-name-only hits are rejected. Known examples include the 2026 procurator-system `杜本硕` hit, which is not linked to the source federation identity.\n- `胡守斌` is refreshed to current 淮北市政协/致公党 role rather than mechanically carrying forward the older 工商联主席 role.\n- `邰紫鹏` remains refreshed to 泰尔重工党委书记、董事长 from current enterprise evidence, superseding stale 总经理 wording.\n- All remaining rows carry an explicit unresolved reason; no employer/title was guessed.\n\n**PASS**\n'''
(E / "W3_BATCH_0019_VALIDATION.md").write_text(validation, encoding="utf-8")

status_path = P / "STATUS.yaml"
s = status_path.read_text(encoding="utf-8")
repls = {
    "code: W3-BATCH-0018": "code: W3-BATCH-0019",
    "code: W3-BATCH-0019\n  phase: W3-EVIDENCE-ENRICH\n  status: READY": "code: W3-BATCH-0020\n  phase: W3-EVIDENCE-ENRICH\n  status: READY",
    "batches_sealed: 18": "batches_sealed: 19",
    "processed_queue_rows: 1080": "processed_queue_rows: 1140",
    "next_queue_order: 1081": "next_queue_order: 1141",
    "actionable_queue_remaining: 9564": "actionable_queue_remaining: 9504",
    "processed: 979": "processed: 1039",
    "remaining: 3352": "remaining: 3292",
    "identity_evidence_rows: 1080": "identity_evidence_rows: 1140",
    "current_org_title_confirmed_rows: 657": "current_org_title_confirmed_rows: 694",
    "current_org_title_unresolved_rows: 320": "current_org_title_unresolved_rows: 343",
}
for a,b in repls.items():
    assert a in s, a
    s = s.replace(a,b,1)
anchor = "  w3_batch_0018_validation: projects/fc-exec-2515/evidence/W3_BATCH_0018_VALIDATION.md\n"
assert anchor in s
s = s.replace(anchor, anchor + "  w3_batch_0019_results: projects/fc-exec-2515/evidence/W3_BATCH_0019_RESULTS.csv\n  w3_batch_0019_metrics: projects/fc-exec-2515/evidence/W3_BATCH_0019_METRICS.yaml\n  w3_batch_0019_validation: projects/fc-exec-2515/evidence/W3_BATCH_0019_VALIDATION.md\n", 1)
status_path.write_text(s, encoding="utf-8")

current_path = P / "CURRENT.yaml"
c = current_path.read_text(encoding="utf-8")
crepls = {
    "current_gate: W3-BATCH-0019": "current_gate: W3-BATCH-0020",
    "work_cursor: 1080": "work_cursor: 1140",
    "verified_records: 659": "verified_records: 696",
    "unresolved_records: 9985": "unresolved_records: 9948",
    "processed: 1080": "processed: 1140",
    "actionable_remaining: 9564": "actionable_remaining: 9504",
    "next_queue_order: 1081": "next_queue_order: 1141",
    "processed: 979": "processed: 1039",
    "remaining: 3352": "remaining: 3292",
}
for a,b in crepls.items():
    assert a in c, a
    c = c.replace(a,b,1)
# last_input_head means HEAD consumed to produce this gate, not the post-commit SHA.
c = c.replace("last_input_head: 7f01f67213e48af96c1e896921d60d3f4466b378", f"last_input_head: {INPUT_HEAD}", 1)
c = c.replace("last_evidence_at: 2026-09-20T16:52:10+08:00", f"last_evidence_at: {NOW}", 1)
batch_block = f'''\nw3_batch_0019:\n  status: SEALED\n  validation: PASS\n  touched_rows: 60\n  anhui_rows: 60\n  p1_identity_rows: 60\n  evidence_backed_rows: 60\n  a_grade_rows: {grades['A']}\n  b_grade_rows: {grades['B']}\n  c_grade_rows: 0\n  current_org_title_confirmed_rows: {confirmed}\n  current_org_title_unresolved_rows: {unresolved}\n  unsupported_current_title_claims: 0\n\n'''
notes_anchor = "notes:\n"
assert notes_anchor in c
c = c.replace(notes_anchor, batch_block + notes_anchor, 1)
notes_tail = f'''  - W3-BATCH-0019 processed queue orders 1081-1140 exactly, all 60 安徽 P1 identity/current-role rows.\n  - {confirmed} rows received current organization/title confirmation; {unresolved} remain explicit unresolved with no unsupported current-title claims.\n  - The live 安徽省工商联（总商会） leadership surface directly closed current enterprise/organization roles for 26 touched source rows, including the duplicate 周伊凡 source rows without merging person_id values.\n  - Fresh contextual closures include 徐善水、朱有为、孙四平、李颖、杨乐、吴涛、杜本硕、邵迪、胡守斌、姚亚妹; each required a federation-history/context bridge and current public evidence.\n  - 胡守斌 was refreshed from the older 工商联主席 role to current 淮北市政协副主席/致公党市委会主委; 邰紫鹏 remains current 泰尔重工党委书记、董事长.\n  - Same-name-only and weakly bridged hits were rejected; the 2026 procurator-system 杜本硕 hit was not linked to the source identity.\n  - Evidence grades are A={grades['A']}, B={grades['B']}, C=0; next deterministic queue order is 1141.\n'''
c = c.rstrip() + "\n" + notes_tail
current_path.write_text(c, encoding="utf-8")

print(f"PASS W3-BATCH-0019 confirmed={confirmed} unresolved={unresolved} grades={dict(grades)} next=1141")
