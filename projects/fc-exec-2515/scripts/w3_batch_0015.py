#!/usr/bin/env python3
import csv, gzip, pathlib, datetime, re, subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]; E=ROOT/'evidence'
INPUT_HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT.parents[1],text=True).strip()
assert INPUT_HEAD=='462b748b1a8624029971a6d982563dc564690009', INPUT_HEAD
NOW=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).replace(microsecond=0).isoformat()
with gzip.open(E/'W2_UNRESOLVED_QUEUE.csv.gz','rt',encoding='utf-8-sig',newline='') as f: allq=list(csv.DictReader(f))
rows=allq[840:900]
assert len(rows)==60 and [int(r['queue_order']) for r in rows]==list(range(841,901))
assert {r['province'] for r in rows}=={'浙江'} and {r['priority'] for r in rows}=={'P1_IDENTITY'}
LIVE='https://www.zjfic.org.cn/col/col1620079/index.html'
HIST='https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_zj/202209/t20220919_313059.html'
# Current live Zhejiang federation/chamber leadership. Source rows stay independent; no person_id merge.
live_fed={'宗馥莉','胡季强','徐爱华','屠红燕','傅利泉','鲁伟鼎','赖梅松'}
live_ch={'胡兴荣','高兴江','郭明明','陶晓莺','黄军民','蒋晓萌','谢识才','詹洪良','潘建清'}
FIELDS=['queue_order','person_id','province','excel_row','name_normalized','source_federation_role','identity_resolution','candidate_names','current_organization','current_title','current_verification_status','evidence_type','evidence_grade','evidence_title','evidence_url','evidence_date','unresolved_reason','research_notes']
special={}
def add(q,org,title,grade,url,date,etype,etitle,notes): special[q]=(org,title,grade,url,date,etype,etitle,notes)
add(841,'中共台州市委统一战线工作部 / 台州市工商业联合会','副部长 / 党组书记','A','https://www.zjfic.org.cn/col/col1620074/art/2026/art_e1c07b54f3a54f1a8bf67757b9d81f62.html','2026-03-30','federation_official','林福江：弘扬垦荒精神 赓续“五大”血脉 以台州民营经济的硬核力量勇当先行者','Current Zhejiang federation official article directly identifies 林福江 as 台州市委统战部副部长、市工商联党组书记; historical provincial standing-committee identity supplies the role-history anchor.')
add(847,'浙江通力传动科技股份有限公司','董事长','A','https://chinajob.mohrss.gov.cn/c/2026-09-02/588686.shtml','2026-09-02','government_official','浙江温州：瑞安着力破解“企业缺人、学生缺练”矛盾','MOHRSS China Employment Network current report directly names 项建忠 as 浙江通力传动科技股份有限公司董事长. Name+Zhejiang/Wenzhou organization-region+historical federation context closes identity.')
add(848,'荣盛石化股份有限公司','总经理','A','https://www.cnrspc.com/newsinfo/10952850.html','2026-01-19','enterprise_official','加拿大总理卡尼会见荣盛石化总经理项炯炯','Current company-official article directly identifies 项炯炯 as 荣盛石化总经理; uncommon name, Zhejiang company region and historical provincial federation context close identity without name-only inference.')
add(852,'浙江新和成股份有限公司','副董事长、总裁','A','https://www.suihua.gov.cn/sh/bdyw/202601/c12_225871.shtml','2026-01-29','government_official','韩雪松陈立军会见浙江新和成股份有限公司胡柏剡一行','Current municipal-government report explicitly identifies 胡柏剡 as 浙江新和成股份有限公司副董事长、总裁; Zhejiang enterprise context and historical federation identity align.')
add(853,'德力西集团有限公司','总裁','A','https://www.delixi.com/xwzx/16502','2026-01-28','enterprise_official','圆满收官“十四五” | 德力西集团召开2025年度总结表彰大会','DeLiXi official 2026 annual meeting article repeatedly identifies 胡煜鐄 as 集团总裁; historical Zhejiang federation identity and enterprise region context close identity.')
add(854,'正泰集团股份有限公司','总裁助理','B','https://www.wzbc.edu.cn/Art/Art_46/Art_46_137976.aspx','2026-04-11','official_conference_material','我校组织校友企业家参与“问道名企”活动 南存辉、王文、葛益平授课','Current institutional conference report identifies 南君侠 simultaneously as 全国温州商会总会新生代温商工作委员会会长、正泰集团总裁助理, providing chamber+enterprise context rather than a name-only match.')
add(855,'珀莱雅化妆品股份有限公司','董事长','B','https://finance.sina.com.cn/roll/2026-06-18/doc-inicwaim5280101.shtml','2026-06-18','authoritative_media','直击股东会｜珀莱雅董事长侯军呈：光靠自有品牌无法十年内跻身全球化妆品行业前十','Daily Economic News coverage of the 2025 annual shareholder meeting explicitly identifies 侯军呈 as 珀莱雅股份董事长; Zhejiang listed-company and historical federation context close identity.')
add(856,'东阳市源泰实业投资合伙企业（有限合伙）','执行事务合伙人','B','https://finance.sina.com.cn/stock/zqgd/2026-02-11/doc-inhmnaif4623692.shtml','2026-02-11','authoritative_media','东望时代拟1.94亿关联收购科冠聚合物51%股权','Listed-company announcement coverage states 东望时代关联交易对方源泰实业的执行事务合伙人为俞蘠 and also identifies his control of 野风集团/野风创投/野风控股; Dongyang/Zhejiang business context anchors the historical federation identity.')
add(858,'浙江佐力药业股份有限公司','董事长','A','https://static.cninfo.com.cn/finalpage/2026-08-28/1225516989.PDF','2026-08-28','listed_company_filing','浙江佐力药业股份有限公司第八届董事会第十八次会议决议公告','Original CNINFO filing states the 2026-08-26 board meeting was chaired by 董事长俞有强; historical Zhejiang federation identity and Zhejiang listed-company context close identity.')
add(865,'中共浙江省委金融委员会办公室 / 中共浙江省委金融工作委员会','常务副主任 / 常务副书记','A','https://sjrb.zj.gov.cn/art/2026/3/19/art_1370340_58717113.html','2026-03-19','government_official','全省地方金融系统党建工作暨党风廉政建设会议召开','Zhejiang provincial financial-office official report explicitly identifies 徐国龙 as 省委金融办常务副主任、省委金融工委常务副书记; province+public-role context bridges the historical federation identity.')
add(867,'浙江省农业农村厅','副厅长','A','https://cnrri.caas.cn/bsdt/607b21a0282747a28403d60661cc5233.htm','2026-06-10','government_official','浙江省农业农村厅副厅长徐燕峰来中国水稻研究所调研交流','Chinese Academy of Agricultural Sciences institute official report explicitly identifies 徐燕峰 as 浙江省农业农村厅副厅长; Zhejiang public-role context bridges the historical federation identity.')
add(870,'赛石集团有限公司','董事长','B','https://xsc.zjgsu.edu.cn/2026/0918/c5478a231415/page.htm','2026-07-06','official_conference_material','浙江工商大学“卓越辅导员”项目简介','Current Zhejiang Gongshang University material identifies alumnus 郭柏峰 as 赛石集团董事长; uncommon name+Zhejiang institution/business context and historical federation identity provide a safe bridge.')
add(876,'湖州市市场监督管理局','党委书记、局长','B','https://news.10jqka.com.cn/20260417/c676087482.shtml','2026-04-17','authoritative_media','市市场监管局举办“青蓝学堂”首期活动 局长寄语年轻干部实干担当','Current report from 湖州市场监管消息 identifies 黄骆意 as 市市场监管局党委书记、局长; historical public reporting had identified the same Zhejiang official as 湖州市工商联党组书记、常务副主席, supplying a role-history bridge.')
add(878,'杭州市市场监督管理局','党委书记、局长','B','https://www.cfsn.cn/news/detail/2277/356916.html','2026-07-10','authoritative_media','浙江省市场监管局党委书记、局长谢小云带队赴杭州检查市场监管领域防汛防台工作','Current China Food Safety Network report names 麻承荣 as 杭州市市场监管局党委书记、局长. Distinctive name+Hangzhou/Zhejiang public-sector context and historical federation identity close the bridge.')
add(879,'伟星集团有限公司','董事长兼总裁','A','https://static.cninfo.com.cn/finalpage/2026-04-17/1225112913.PDF','2026-04-17','listed_company_filing','浙江伟星实业发展股份有限公司2025年度报告','Original CNINFO annual report explicitly states 章卡鹏 is 伟星集团董事长兼总裁 and also 浙江省工商联常委, directly closing both source identity and current enterprise role in one filing.')
add(882,'福建省浙江商会','会长','B','https://www.52hrtt.com/fj/n/w/info/G1770706409747','2026-03-22','authoritative_media','福建省浙江衢州商会换届庆典圆满举行','Current event report explicitly identifies 福建浙江商会会长董加余; Zhejiang-chamber context plus the uncommon name and historical Zhejiang provincial federation identity close the bridge.')
add(890,'浙江联润建设工程有限公司','董事长','B','https://www.sohu.com/a/1036162239_121106994','2026-06-13','official_conference_material','衢州市南孔儒商促进会第一次会员大会圆满举行','Current federation-attended conference report identifies 谢招修 as 浙江联润建设工程有限公司董事长 and newly elected association chair; Quzhou/Zhejiang federation context safely bridges identity.')
add(892,'浙江省华夏民生与公益研究院','院长','B','https://www.sohu.com/a/1011072996_121106994','2026-04-17','official_conference_material','“侨兴浙江・青蓝接力”浙江省侨助共富暨“侨青入乡”现场推进活动在湖州安吉成功举办','Current Zhejiang provincial united-front event material identifies 赖惠能 as 浙江省华夏民生与公益研究院院长; same-province public-role context plus historical federation identity avoids name-only inference.')
add(894,'浙商研究中心','副主任','A','https://www.ctsec.com/company/detail/9317507','2026-03-27','enterprise_official','凤凰成长计划圆满结课 浙商齐聚财通共话发展新篇','财通证券 official current article identifies 蔡晓春 as 浙商研究中心副主任 and explicitly notes he is former 浙江省工商联党组副书记、一级巡视员, directly providing the role-history bridge.')
add(897,'贝达药业股份有限公司','董事长','A','https://bettapharma.com/News/show/id/2826','2026-03-03','enterprise_official','带着“创新盼”与“娘家情” 全国政协委员丁列明再赴“春日之约”','Betta Pharma official current material identifies 丁列明 as company chairman/current national CPPCC member; Zhejiang biopharma and historical federation context close identity.')
add(898,'浙江亚厦装饰股份有限公司','董事长','A','https://static.cninfo.com.cn/finalpage/2026-04-28/1225218703.PDF','2026-04-28','listed_company_filing','浙江亚厦装饰股份有限公司2025年年度报告','Original CNINFO annual report lists 丁泽成 as current chairman; the same filing also records his public roles and Zhejiang context, and this evidence was already sealed for the same source identity in W3-BATCH-0013.')
results=[]
for r in rows:
    q=int(r['queue_order']); name=r['name_normalized']
    out={'queue_order':r['queue_order'],'person_id':r['person_id'],'province':r['province'],'excel_row':r['excel_row'],'name_normalized':name,'source_federation_role':r['federation_role'],'candidate_names':name}
    if q in special:
        org,title,grade,url,date,etype,etitle,notes=special[q]
        out.update(identity_resolution='CURRENT_ROLE_CONFIRMED_WITH_CONTEXT_BRIDGE',current_organization=org,current_title=title,current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type=etype,evidence_grade=grade,evidence_title=etitle,evidence_url=url,evidence_date=date,unresolved_reason='',research_notes=notes)
    elif name in live_fed:
        out.update(identity_resolution='CURRENT_ROLE_CONFIRMED_BY_LIVE_OFFICIAL_PROVINCIAL_LEADERSHIP_PAGE',current_organization='浙江省工商业联合会',current_title='副主席',current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type='federation_official',evidence_grade='A',evidence_title='浙江省工商业联合会（浙江省商会）商会领导',evidence_url=LIVE,evidence_date='2026-09-20',unresolved_reason='',research_notes='Live official Zhejiang federation leadership page directly names this current vice-chair. Mapping uses name+province+federation context and preserves the source person_id.')
    elif name in live_ch:
        out.update(identity_resolution='CURRENT_ROLE_CONFIRMED_BY_LIVE_OFFICIAL_PROVINCIAL_LEADERSHIP_PAGE',current_organization='浙江省商会',current_title='副会长',current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type='federation_official',evidence_grade='A',evidence_title='浙江省工商业联合会（浙江省商会）商会领导',evidence_url=LIVE,evidence_date='2026-09-20',unresolved_reason='',research_notes='Live official Zhejiang chamber leadership page directly names this current vice-chair. Mapping uses name+province+federation context and preserves the source person_id.')
    else:
        # Targeted current searches were performed for each remaining row. Stale/name-only/region-mismatched hits are not promoted.
        extra=''
        if name=='袁海波': extra=' A current Hong Kong listed-company executive with the same name was rejected because region/history did not bridge to the Zhejiang federation identity.'
        if name=='王文胜': extra=' A current Shandong enterprise same-name hit was rejected because region/history did not bridge to the Zhejiang federation identity.'
        if name=='潘云峰': extra=' A 2026 Zhejiang vocational-education public-role hit was not promoted because the source-row identity lacked enough organization-history linkage.'
        out.update(identity_resolution='HISTORICAL_SOURCE_IDENTITY_CURRENT_ROLE_UNRESOLVED',current_organization='',current_title='',current_verification_status='UNRESOLVED_CURRENT_ORG_TITLE',evidence_type='targeted_public_current_verification',evidence_grade='A',evidence_title='ACFIC Zhejiang 2022 standing-committee/executive identity + 2026 targeted current verification',evidence_url=HIST,evidence_date='2026-09-20',unresolved_reason=f'{name} is confirmed in the official 2022 Zhejiang federation roster, but targeted 2026 public research did not establish a sufficiently specific current organization/title with a safe identity bridge.',research_notes='Current public sources were searched using federation/province/business/public-role context. No current organization/title is asserted where only a same-name, stale, or region-mismatched hit could be found.'+extra)
    results.append(out)
assert len(results)==60
confirmed=sum(r['current_verification_status']=='CURRENT_ORG_TITLE_CONFIRMED' for r in results); unres=60-confirmed
a_grade=sum(r['evidence_grade']=='A' for r in results); b_grade=sum(r['evidence_grade']=='B' for r in results)
assert (confirmed,unres,a_grade,b_grade)==(37,23,51,9),(confirmed,unres,a_grade,b_grade)
assert all(r['evidence_url'] for r in results)
assert all((r['current_organization'] and r['current_title']) if r['current_verification_status']=='CURRENT_ORG_TITLE_CONFIRMED' else r['unresolved_reason'] for r in results)
with open(E/'W3_BATCH_0015_RESULTS.csv','w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator='\n'); w.writeheader(); w.writerows(results)
LEDGER_FIELDS=['queue_order','person_id','province','excel_row','candidate_names','evidence_type','evidence_grade','evidence_title','evidence_url','evidence_date','current_verification_status','unresolved_reason']
OVERLAY_FIELDS=['queue_order','person_id','province','excel_row','identity_resolution','candidate_names','current_organization','current_title','current_verification_status','evidence_grade','evidence_url','unresolved_reason']
def append_rows(path,fields):
    with open(path,'r',encoding='utf-8-sig',newline='') as f: old=list(csv.DictReader(f))
    last=int(old[-1]['queue_order'])
    if last==900: return
    assert last==840,(path,last)
    with open(path,'a',encoding='utf-8',newline='') as f: csv.DictWriter(f,fieldnames=fields,extrasaction='ignore',lineterminator='\n').writerows(results)
append_rows(E/'W3_EVIDENCE_LEDGER.csv',LEDGER_FIELDS); append_rows(E/'W3_VERIFICATION_OVERLAY.csv',OVERLAY_FIELDS)
for p in [E/'W3_EVIDENCE_LEDGER.csv',E/'W3_VERIFICATION_OVERLAY.csv']:
    with open(p,'r',encoding='utf-8-sig',newline='') as f: rr=list(csv.DictReader(f))
    orders=[int(x['queue_order']) for x in rr]
    assert len(rr)==900 and orders==list(range(1,901)) and len(set(orders))==900
(E/'W3_BATCH_0015_METRICS.yaml').write_text(f'''schema: fc2515-w3-batch-metrics-v1
project_id: FC-EXEC-2515-01
gate: W3-BATCH-0015
status: PASS
queue_range: [841, 900]
batch_rows: 60
p1_identity_rows: 60
evidence_backed_rows: 60
a_grade_rows: {a_grade}
b_grade_rows: {b_grade}
structural_deferred_rows: 0
current_org_title_confirmed_rows: {confirmed}
no_current_role_confirmed_rows: 0
current_org_title_unresolved_rows: {unres}
unsupported_current_title_claims: 0
post_batch:
  processed_queue_rows: 900
  actionable_queue_remaining: 9744
  next_queue_order: 901
  p1_processed: 799
  p1_remaining: 3532
next_gate: W3-BATCH-0016
''',encoding='utf-8')
(E/'W3_BATCH_0015_VALIDATION.md').write_text(f'''# W3-BATCH-0015 Validation

Result: **PASS**

- Deterministic queue slice: 841–900 exactly, 60 浙江 P1_IDENTITY rows; no rows outside this repository-defined gate were touched.
- Every touched row has public evidence or an explicit unresolved-current-role reason; unsupported current-title claims: 0.
- Live Zhejiang federation/chamber leadership directly closes 16 current roles; repeated source appearances preserve distinct `person_id` values.
- 21 additional current roles were closed only with context bridges from current public evidence. Strong A-grade examples include 林福江、项建忠、项炯炯、胡柏剡、胡煜鐄、俞有强、徐国龙、徐燕峰、章卡鹏、蔡晓春、丁列明、丁泽成.
- 23 rows remain explicit current-role unresolved cases. Same-name, stale, weakly bridged, or region-mismatched hits were rejected rather than promoted to claims.
- Evidence grades: A={a_grade}, B={b_grade}, C=0; current organization/title confirmed={confirmed}/60; unresolved={unres}/60.
- No current organization/title was assigned from a name-only hit.
- Cumulative evidence ledger and verification overlay each reconcile to 900 rows with queue_order 1..900, no gaps or duplicates.

Next deterministic gate: `W3-BATCH-0016`, starting queue_order 901.
''',encoding='utf-8')
sp=ROOT/'STATUS.yaml'; s=sp.read_text(encoding='utf-8')
def sub1(text,a,b):
    assert a in text,a
    return text.replace(a,b,1)
s=sub1(s,'code: W3-BATCH-0014\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS','code: W3-BATCH-0015\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS')
s=sub1(s,'code: W3-BATCH-0015\n  phase: W3-EVIDENCE-ENRICH\n  status: READY','code: W3-BATCH-0016\n  phase: W3-EVIDENCE-ENRICH\n  status: READY')
for a,b in [('  batches_sealed: 14','  batches_sealed: 15'),('  processed_queue_rows: 840','  processed_queue_rows: 900'),('  next_queue_order: 841','  next_queue_order: 901'),('  actionable_queue_remaining: 9804','  actionable_queue_remaining: 9744'),('  identity_evidence_rows: 840','  identity_evidence_rows: 900'),('  current_org_title_confirmed_rows: 501','  current_org_title_confirmed_rows: 538'),('  current_org_title_unresolved_rows: 236','  current_org_title_unresolved_rows: 259')]: s=sub1(s,a,b)
s=sub1(s,'    processed: 739\n    remaining: 3592','    processed: 799\n    remaining: 3532')
anchor='  w3_batch_0014_validation: projects/fc-exec-2515/evidence/W3_BATCH_0014_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv'
rep='  w3_batch_0014_validation: projects/fc-exec-2515/evidence/W3_BATCH_0014_VALIDATION.md\n  w3_batch_0015_results: projects/fc-exec-2515/evidence/W3_BATCH_0015_RESULTS.csv\n  w3_batch_0015_metrics: projects/fc-exec-2515/evidence/W3_BATCH_0015_METRICS.yaml\n  w3_batch_0015_validation: projects/fc-exec-2515/evidence/W3_BATCH_0015_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv'
s=sub1(s,anchor,rep); sp.write_text(s,encoding='utf-8')
cp=ROOT/'CURRENT.yaml'; c=cp.read_text(encoding='utf-8')
c=sub1(c,'current_gate: W3-BATCH-0015','current_gate: W3-BATCH-0016')
c=sub1(c,'work_cursor: 840','work_cursor: 900')
c=sub1(c,'verified_records: 503','verified_records: 540')
c=sub1(c,'unresolved_records: 10141','unresolved_records: 10104')
c=sub1(c,'  processed: 840','  processed: 900')
c=sub1(c,'  actionable_remaining: 9804','  actionable_remaining: 9744')
c=sub1(c,'  next_queue_order: 841','  next_queue_order: 901')
c=sub1(c,'      processed: 739\n      remaining: 3592','      processed: 799\n      remaining: 3532')
c,n=re.subn(r'last_input_head: .*',f'last_input_head: {INPUT_HEAD}',c,count=1); assert n==1
c,n=re.subn(r'last_evidence_at: .*',f'last_evidence_at: {NOW}',c,count=1); assert n==1
section=f'''\nw3_batch_0015:
  status: SEALED
  validation: PASS
  touched_rows: 60
  p1_identity_rows: 60
  evidence_backed_rows: 60
  a_grade_rows: {a_grade}
  b_grade_rows: {b_grade}
  current_org_title_confirmed_rows: {confirmed}
  current_org_title_unresolved_rows: {unres}
  unsupported_current_title_claims: 0
\n'''
c=sub1(c,'\nnotes:\n','\n'+section+'notes:\n')
notes=f'''  - W3-BATCH-0015 processed queue orders 841-900 exactly, all 60 浙江 P1 identity/current-role rows.
  - {confirmed} rows received current organization/title confirmation; {unres} remain explicit unresolved where current evidence was stale, ambiguous, region-mismatched, or insufficiently linked to the source identity.
  - The live Zhejiang federation/chamber leadership page directly closed 16 current roles; a further 21 were closed only with contextual current evidence and historical federation identity anchors.
  - Strong current closures include 林福江、项建忠、项炯炯、胡柏剡、胡煜鐄、俞有强、徐国龙、徐燕峰、章卡鹏、蔡晓春、丁列明、丁泽成; no name-only assignment was permitted.
  - Same-name/weakly bridged hits including 袁海波、潘云峰、王炜、王文胜 were preserved as unresolved rather than guessed.
  - Evidence grades are A={a_grade}, B={b_grade}, C=0; unsupported current-title claims=0.
  - Next deterministic queue order is 901.
'''
c=c.rstrip()+'\n'+notes; cp.write_text(c,encoding='utf-8')
st=sp.read_text(encoding='utf-8'); ct=cp.read_text(encoding='utf-8')
assert 'latest_gate:\n  code: W3-BATCH-0015' in st and 'next_gate:\n  code: W3-BATCH-0016' in st
assert 'current_gate: W3-BATCH-0016' in ct and 'work_cursor: 900' in ct and 'next_queue_order: 901' in ct
print(f'PASS W3-BATCH-0015 confirmed={confirmed} unresolved={unres} A={a_grade} B={b_grade} now={NOW}')
