#!/usr/bin/env python3
import csv, gzip, pathlib, datetime, re, subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]; E=ROOT/'evidence'
INPUT_HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT.parents[1],text=True).strip()
assert INPUT_HEAD=='9138a4410a2723bf83bf133be782ccc37bd4edec', INPUT_HEAD
NOW=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).replace(microsecond=0).isoformat()
with gzip.open(E/'W2_UNRESOLVED_QUEUE.csv.gz','rt',encoding='utf-8-sig',newline='') as f: allq=list(csv.DictReader(f))
rows=allq[720:780]
assert len(rows)==60 and [int(r['queue_order']) for r in rows]==list(range(721,781))
assert {r['province'] for r in rows}=={'浙江'} and {r['priority'] for r in rows}=={'P1_IDENTITY'}
LIVE='https://www.zjfic.org.cn/col/col1620079/index.html'
live_fed={'胡季强','陈仲尼','王达武','叶辽宁','王世民','王黎红','冯仁强'}
live_ch={'励行根','王振滔','潘建清','仇建平','邵法平','蒋晓萌','余震','庄伟意','陈保华','陶晓莺','高兴江','田宁','张林松','陈频','詹洪良','张亚波','刘启宏','胡兴荣','方毅','黄军民'}
live_dual={'元成茂','林建良'}
FIELDS=['queue_order','person_id','province','excel_row','name_normalized','source_federation_role','identity_resolution','candidate_names','current_organization','current_title','current_verification_status','evidence_type','evidence_grade','evidence_title','evidence_url','evidence_date','unresolved_reason','research_notes']
special={}
def add(q,org,title,grade,url,date,etype,etitle,notes): special[q]=(org,title,grade,url,date,etype,etitle,notes)
add(725,'中共浙江省委金融委员会办公室 / 中共浙江省委金融工作委员会','常务副主任 / 常务副书记','A','https://sjrb.zj.gov.cn/art/2026/3/19/art_1370340_58717113.html','2026-03-19','government_official','浙江省委金融办公开活动材料','2022 ACFIC Zhejiang election roster anchors 徐国龙; 2026 Zhejiang financial-office evidence supplies the current role.')
add(726,'浙商研究中心','副主任','A','https://www.ctsec.com/company/detail/9317507','2026-03-27','enterprise_official','财通证券公开材料','2022 ACFIC Zhejiang election roster anchors 蔡晓春; current role is refreshed from 2026 evidence rather than carrying the old federation title.')
add(727,'浙江省农业农村厅','副厅长','A','https://cnrri.caas.cn/bsdt/607b21a0282747a28403d60661cc5233.htm','2026-06-10','government_official','中国水稻研究所公开活动材料','2022 ACFIC Zhejiang election roster anchors 徐燕峰; 2026 official material confirms the current role.')
add(752,'贝达药业股份有限公司','董事长','B','https://www.qxzh.zj.cn/art/2026/3/19/art_1228998548_58937010.html','2026-03-19','authoritative_media','丁列明：加快发展生物医药新兴支柱产业','2026 Zhejiang public material identifies 丁列明 as 全国政协委员、杭州市工商联副主席、贝达药业董事长, providing province+federation+enterprise identity context.')
add(753,'浙江亚厦装饰股份有限公司','董事长','A','https://static.cninfo.com.cn/finalpage/2026-04-28/1225218703.PDF','2026-04-28','listed_company_filing','浙江亚厦装饰股份有限公司2025年年度报告','The 2026-filed annual report itself states 丁泽成 is 浙江省工商联常务委员会委员 and current 亚厦股份董事长.')
add(758,'西子清洁能源装备制造股份有限公司','董事长','A','https://www.xizice.com/news/831.html','2026-01-26','enterprise_official','王克飞董事长荣获科创之星','Enterprise-official evidence confirms 王克飞 as current 西子洁能董事长; Zhejiang entrepreneur-association context separately identifies him as 浙江省工商联常委, avoiding a name-only match.')
add(760,'富通集团有限公司','董事长','B','https://www.cwc.net.cn/tradeleads/show-8401.html','2026-03-11','authoritative_media','富通集团董事长王建沂相关公开材料','Reuses already sealed q701 current-role evidence only after the same Zhejiang federation source identity is closed; distinct person_id is preserved.')
add(761,'广宇集团股份有限公司','董事长','B','https://www.sohu.com/a/1019929094_115377','2026-05-08','authoritative_media','广宇集团2026年投资者网上集体接待日通知','The Zhejiang federation changeover context links 王轶磊 to 广宇集团; 2026 filing-based coverage confirms his current chair role.')
add(769,'长江精工钢结构（集团）股份有限公司','董事长、总裁','A','https://static.cninfo.com.cn/finalpage/2026-04-18/1225120796.PDF','2026-04-18','listed_company_filing','长江精工钢结构（集团）股份有限公司2025年年度报告','The 2026-filed annual report explicitly states 方朝阳 is 浙江省工商联第十二届常委 and current company 董事长兼总裁.')
add(776,'浙江富钢集团有限公司','董事长','A','https://www.fusteel.cn/news/company_news/article_288.html','2026-01-06','enterprise_official','富钢集团2026年公开材料','Recent Zhejiang public evidence identifies 朱柏荣 as 浙江省工商联常委、浙江富钢集团董事长; 2026 enterprise-official evidence confirms the chair role remains current.')
add(779,'新凤鸣集团股份有限公司','董事长','A','https://big5.sse.com.cn/site/cht/www.sse.com.cn/disclosure/listedinfo/announcement/c/new/2026-04-17/603225_20260417_PPC6.pdf','2026-04-17','stock_exchange','新凤鸣集团股份有限公司第六届董事会第四十九次会议决议公告','2026 public company materials identify 庄耀中 in the Zhejiang federation cohort; SSE April-2026 filing directly confirms current chairman authority. Current title is conservatively limited to 董事长.')
unresolved={
730:('A',LIVE,'吕晓峰 is anchored by the 2022 ACFIC Zhejiang election roster but is absent from the live 2026 provincial federation leadership page; no safe replacement current role was established.'),
754:('B','https://www.zjfic.org.cn/','王炜 is a high-frequency name; targeted Zhejiang/federation searches did not provide enough disambiguating keys for a current organization/title.'),
755:('B','https://www.zjfic.org.cn/','王文胜 is a high-frequency name; current web hits did not supply federation/province/organization-history linkage sufficient for a safe assignment.'),
759:('B','https://news.sina.com.cn/sx/2026-04-19/detail-inhuznpc9299936.shtml','A 2026 report names a 宁波市工商联党组书记王建云, but the source row explicitly records 王建云(女) and no reliable bridge proves identity; the same-name role is rejected.'),
763:('A','https://static.cninfo.com.cn/finalpage/2026-04-29/1225230252.PDF','A 2026 filing confirms a 王敏良 in current 仙鹤股份 leadership, but no sufficiently strong federation-history bridge ties that public identity to this source 浙江省工商联常委 row.'),
768:('A','https://static.cninfo.com.cn/finalpage/2026-04-22/1225141427.PDF','A 2026 filing confirms current 方能斌 corporate roles, but searched evidence did not safely bridge that identity to this source 浙江省工商联常委 row.'),
773:('B','https://www.zjfic.org.cn/','Targeted searches for 吕粱 in Zhejiang federation/business context did not establish a sufficiently specific current organization/title.'),
774:('A',LIVE,'Cross-listed 吕晓峰 source row remains a distinct person_id. He is absent from the live 2026 leadership page and no safe replacement current role was established.'),
775:('A','https://static.cninfo.com.cn/finalpage/2026-04-21/1225130397.PDF','A 2026 filing confirms a 朱立科 as 浙江一鸣食品董事长、总经理, but searched evidence did not explicitly bridge that public identity to this provincial-federation standing-committee source row.'),
777:('B','https://www.zjfic.org.cn/','Targeted searches for 朱铁成 in Zhejiang federation/business context did not establish a sufficiently specific current organization/title.')}
results=[]
for r in rows:
    q=int(r['queue_order']); name=r['name_normalized']
    out={'queue_order':r['queue_order'],'person_id':r['person_id'],'province':r['province'],'excel_row':r['excel_row'],'name_normalized':name,'source_federation_role':r['federation_role'],'candidate_names':name}
    if q in special:
        org,title,grade,url,date,etype,etitle,notes=special[q]
        out.update(identity_resolution='CURRENT_ROLE_CONFIRMED_WITH_CONTEXT_BRIDGE',current_organization=org,current_title=title,current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type=etype,evidence_grade=grade,evidence_title=etitle,evidence_url=url,evidence_date=date,unresolved_reason='',research_notes=notes)
    elif q in unresolved:
        grade,url,reason=unresolved[q]
        out.update(identity_resolution='HISTORICAL_SOURCE_IDENTITY_CURRENT_ROLE_UNRESOLVED',current_organization='',current_title='',current_verification_status='UNRESOLVED_CURRENT_ORG_TITLE',evidence_type='targeted_public_current_verification',evidence_grade=grade,evidence_title='Zhejiang current-role targeted verification',evidence_url=url,evidence_date='2026-09-20',unresolved_reason=reason,research_notes='Public current evidence was reviewed; no current organization/title is asserted without a sufficient identity bridge.')
    elif name in live_fed:
        out.update(identity_resolution='CURRENT_ROLE_CONFIRMED_BY_LIVE_OFFICIAL_PROVINCIAL_LEADERSHIP_PAGE',current_organization='浙江省工商业联合会',current_title='副主席',current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type='federation_official',evidence_grade='A',evidence_title='浙江省工商业联合会（浙江省商会）商会领导',evidence_url=LIVE,evidence_date='2026-09-20',unresolved_reason='',research_notes='Live official provincial federation page directly names the person and current role; source mapping uses name+province+federation context and preserves distinct person_id values.')
    elif name in live_ch:
        out.update(identity_resolution='CURRENT_ROLE_CONFIRMED_BY_LIVE_OFFICIAL_PROVINCIAL_LEADERSHIP_PAGE',current_organization='浙江省商会',current_title='副会长',current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type='federation_official',evidence_grade='A',evidence_title='浙江省工商业联合会（浙江省商会）商会领导',evidence_url=LIVE,evidence_date='2026-09-20',unresolved_reason='',research_notes='Live official provincial chamber page directly names the person as current vice-chair; distinct source person_id is preserved.')
    elif name in live_dual:
        out.update(identity_resolution='CURRENT_ROLE_CONFIRMED_BY_LIVE_OFFICIAL_PROVINCIAL_LEADERSHIP_PAGE',current_organization='浙江省工商业联合会 / 浙江省商会',current_title='党组成员、副主席 / 副会长',current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type='federation_official',evidence_grade='A',evidence_title='浙江省工商业联合会（浙江省商会）商会领导',evidence_url=LIVE,evidence_date='2026-09-20',unresolved_reason='',research_notes='Live official page supersedes the stale source role and directly gives current federation/chamber roles.')
    elif name=='宋立':
        out.update(identity_resolution='CURRENT_ROLE_CONFIRMED_BY_LIVE_OFFICIAL_PROVINCIAL_LEADERSHIP_PAGE',current_organization='浙江省工商业联合会 / 浙江省商会',current_title='党组成员、秘书长 / 秘书长',current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type='federation_official',evidence_grade='A',evidence_title='浙江省工商业联合会（浙江省商会）商会领导',evidence_url=LIVE,evidence_date='2026-09-20',unresolved_reason='',research_notes='Live official page directly confirms current secretary-general roles.')
    else: raise AssertionError((q,name,'no disposition'))
    results.append(out)
assert len(results)==60
confirmed=sum(r['current_verification_status']=='CURRENT_ORG_TITLE_CONFIRMED' for r in results); unres=60-confirmed
a_grade=sum(r['evidence_grade']=='A' for r in results); b_grade=sum(r['evidence_grade']=='B' for r in results)
assert (confirmed,unres,a_grade,b_grade)==(50,10,52,8),(confirmed,unres,a_grade,b_grade)
assert all(r['evidence_url'] for r in results)
with open(E/'W3_BATCH_0013_RESULTS.csv','w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator='\n'); w.writeheader(); w.writerows(results)
LEDGER_FIELDS=['queue_order','person_id','province','excel_row','candidate_names','evidence_type','evidence_grade','evidence_title','evidence_url','evidence_date','current_verification_status','unresolved_reason']
OVERLAY_FIELDS=['queue_order','person_id','province','excel_row','identity_resolution','candidate_names','current_organization','current_title','current_verification_status','evidence_grade','evidence_url','unresolved_reason']
def append_rows(path,fields):
    with open(path,'r',encoding='utf-8-sig',newline='') as f: old=list(csv.DictReader(f))
    last=int(old[-1]['queue_order'])
    if last==780: return
    assert last==720,(path,last)
    with open(path,'a',encoding='utf-8',newline='') as f: csv.DictWriter(f,fieldnames=fields,extrasaction='ignore',lineterminator='\n').writerows(results)
append_rows(E/'W3_EVIDENCE_LEDGER.csv',LEDGER_FIELDS); append_rows(E/'W3_VERIFICATION_OVERLAY.csv',OVERLAY_FIELDS)
for p in [E/'W3_EVIDENCE_LEDGER.csv',E/'W3_VERIFICATION_OVERLAY.csv']:
    with open(p,'r',encoding='utf-8-sig',newline='') as f: rr=list(csv.DictReader(f))
    orders=[int(x['queue_order']) for x in rr]
    assert len(rr)==780 and orders==list(range(1,781)) and len(set(orders))==780
(E/'W3_BATCH_0013_METRICS.yaml').write_text(f'''schema: fc2515-w3-batch-metrics-v1
project_id: FC-EXEC-2515-01
gate: W3-BATCH-0013
status: PASS
queue_range: [721, 780]
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
  processed_queue_rows: 780
  actionable_queue_remaining: 9864
  next_queue_order: 781
  p1_processed: 679
  p1_remaining: 3652
next_gate: W3-BATCH-0014
''',encoding='utf-8')
validation=f'''# W3-BATCH-0013 Validation

Result: **PASS**

- Deterministic queue slice: 721–780 exactly, 60 浙江 P1_IDENTITY rows; no rows outside this repository-defined gate were touched.
- Every touched row has public evidence or an explicit unresolved-current-role reason; unsupported current-title claims: 0.
- Live Zhejiang federation/chamber leadership is current-state authority for 39 rows in this slice; cross-listed source rows retain distinct person_id values.
- Already-sealed role-history bridges are safely reused for 徐国龙、蔡晓春、徐燕峰、王建沂 only after Zhejiang federation identity closure.
- Fresh safe closures include 丁列明、丁泽成、王克飞、王轶磊、方朝阳、朱柏荣、庄耀中.
- 10 rows remain explicit unresolved current-role cases; plausible corporate roles were not assigned when identity-to-source-row linkage was insufficient.
- Evidence grades: A={a_grade}, B={b_grade}, C=0; current organization/title confirmed={confirmed}/60; unresolved={unres}/60.
- No current organization/title was assigned from a name-only hit.
- Cumulative evidence ledger and verification overlay each reconcile to 780 rows with queue_order 1..780, no gaps or duplicates.

Next deterministic gate: `W3-BATCH-0014`, starting queue_order 781.
'''
(E/'W3_BATCH_0013_VALIDATION.md').write_text(validation,encoding='utf-8')
sp=ROOT/'STATUS.yaml'; s=sp.read_text(encoding='utf-8')
def sub1(text,a,b):
    assert a in text,a
    return text.replace(a,b,1)
s=sub1(s,'code: W3-BATCH-0012\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS','code: W3-BATCH-0013\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS')
s=sub1(s,'code: W3-BATCH-0013\n  phase: W3-EVIDENCE-ENRICH\n  status: READY','code: W3-BATCH-0014\n  phase: W3-EVIDENCE-ENRICH\n  status: READY')
for a,b in [('  batches_sealed: 12','  batches_sealed: 13'),('  processed_queue_rows: 720','  processed_queue_rows: 780'),('  next_queue_order: 721','  next_queue_order: 781'),('  actionable_queue_remaining: 9924','  actionable_queue_remaining: 9864'),('  identity_evidence_rows: 720','  identity_evidence_rows: 780'),('  current_org_title_confirmed_rows: 423','  current_org_title_confirmed_rows: 473'),('  current_org_title_unresolved_rows: 194','  current_org_title_unresolved_rows: 204')]: s=sub1(s,a,b)
s=sub1(s,'    processed: 619\n    remaining: 3712','    processed: 679\n    remaining: 3652')
anchor='  w3_batch_0012_validation: projects/fc-exec-2515/evidence/W3_BATCH_0012_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv'
rep='  w3_batch_0012_validation: projects/fc-exec-2515/evidence/W3_BATCH_0012_VALIDATION.md\n  w3_batch_0013_results: projects/fc-exec-2515/evidence/W3_BATCH_0013_RESULTS.csv\n  w3_batch_0013_metrics: projects/fc-exec-2515/evidence/W3_BATCH_0013_METRICS.yaml\n  w3_batch_0013_validation: projects/fc-exec-2515/evidence/W3_BATCH_0013_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv'
s=sub1(s,anchor,rep); sp.write_text(s,encoding='utf-8')
cp=ROOT/'CURRENT.yaml'
c=cp.read_text(encoding='utf-8')
c=sub1(c,'current_gate: W3-BATCH-0013','current_gate: W3-BATCH-0014')
c=sub1(c,'work_cursor: 720','work_cursor: 780')
c=sub1(c,'verified_records: 425','verified_records: 475')
c=sub1(c,'unresolved_records: 10219','unresolved_records: 10169')
c=sub1(c,'  processed: 720','  processed: 780')
c=sub1(c,'  actionable_remaining: 9924','  actionable_remaining: 9864')
c=sub1(c,'  next_queue_order: 721','  next_queue_order: 781')
c=sub1(c,'      processed: 619\n      remaining: 3712','      processed: 679\n      remaining: 3652')
c=sub1(c,'last_input_head: fc942efc87ec6d6321943ee1c2340f32cb07aa11',f'last_input_head: {INPUT_HEAD}')
c,n=re.subn(r'last_evidence_at: .*',f'last_evidence_at: {NOW}',c,count=1)
assert n==1
section=f'''\nw3_batch_0013:
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
notes=f'''  - W3-BATCH-0013 processed queue orders 721-780 exactly, all 60 浙江 P1 identity/current-role rows.
  - {confirmed} rows received current organization/title confirmation; {unres} remain explicit unresolved because identity-to-current-role linkage was not strong enough for a safe write.
  - The live Zhejiang federation/chamber leadership page supplied authoritative current federation/chamber roles; cross-listed rows preserve distinct person_id values.
  - Fresh high-confidence closures include 丁泽成 and 方朝阳 from 2026-filed listed-company reports that explicitly state both 浙江省工商联常委 identity and current company roles; additional safe bridges closed 丁列明、王克飞、王轶磊、朱柏荣、庄耀中.
  - Plausible current corporate roles for 王敏良、方能斌、朱立科 were deliberately not assigned because public evidence did not safely bridge them to the source federation row. 王建云 homonym/gender ambiguity was explicitly rejected.
  - No current organization/title was assigned from a name-only hit; evidence grades are A={a_grade}, B={b_grade}, C=0.
  - Next deterministic queue order is 781.
'''
c=c.rstrip()+'\n'+notes
cp.write_text(c,encoding='utf-8')
st=sp.read_text(encoding='utf-8'); ct=cp.read_text(encoding='utf-8')
assert 'latest_gate:\n  code: W3-BATCH-0013' in st and 'next_gate:\n  code: W3-BATCH-0014' in st
assert 'current_gate: W3-BATCH-0014' in ct and 'work_cursor: 780' in ct
assert 'next_queue_order: 781' in ct and 'verified_records: 475' in ct and 'unresolved_records: 10169' in ct
print(f'PASS W3-BATCH-0013 confirmed={confirmed} unresolved={unres} A={a_grade} B={b_grade} now={NOW}')
