#!/usr/bin/env python3
import csv, gzip, pathlib, datetime, re, subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]; E=ROOT/'evidence'
INPUT_HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT.parents[1],text=True).strip()
assert INPUT_HEAD=='35302277b720b2c448d016c73dff2d1137d127f9', INPUT_HEAD
NOW=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).replace(microsecond=0).isoformat()
with gzip.open(E/'W2_UNRESOLVED_QUEUE.csv.gz','rt',encoding='utf-8-sig',newline='') as f: allq=list(csv.DictReader(f))
rows=allq[780:840]
assert len(rows)==60 and [int(r['queue_order']) for r in rows]==list(range(781,841))
assert {r['province'] for r in rows}=={'浙江'} and {r['priority'] for r in rows}=={'P1_IDENTITY'}
LIVE='https://www.zjfic.org.cn/col/col1620079/index.html'
HIST='https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_zj/202209/t20220919_313059.html'
# Live current Zhejiang federation/chamber leadership. Source rows are independently retained; no person_id merge.
live_fed={'李书福','宋汉平','张天任','张晓平','陈仲尼','陈建成','林俊波'}
live_ch={'励行根','吴淑英','余震','张亚波','张林松','陈保华','邵法平'}
live_dual=set()
FIELDS=['queue_order','person_id','province','excel_row','name_normalized','source_federation_role','identity_resolution','candidate_names','current_organization','current_title','current_verification_status','evidence_type','evidence_grade','evidence_title','evidence_url','evidence_date','unresolved_reason','research_notes']
special={}
def add(q,org,title,grade,url,date,etype,etitle,notes): special[q]=(org,title,grade,url,date,etype,etitle,notes)
add(782,'浙江龙盛集团股份有限公司','董事长、总经理','B','https://finance.sina.com.cn/stock/aiassist/ggxc/2026-04-11/doc-inhucmsy7464509.shtml','2026-04-11','authoritative_media','浙江龙盛2025年报高管信息','ACFIC 2022 Zhejiang standing-committee roster anchors 阮伟祥; 2026 annual-report-based current evidence supplies the company role. Name+province+federation+enterprise context closes identity; not a name-only assignment.')
add(789,'浙江耀厦控股集团有限公司','总裁','B','https://www.sohu.com/a/996280352_121106994','2026-03-13','authoritative_media','新生代杭商热议全国两会精神（四）','Current Hangzhou merchant material identifies 李建滨 simultaneously as 杭州市总商会副会长 and 浙江耀厦控股集团有限公司总裁, providing federation/chamber+enterprise context for the Zhejiang source identity.')
add(791,'中哲控股集团有限公司 / 广西河池化工股份有限公司','董事长 / 董事长','B','https://finance.sina.com.cn/stock/aiassist/ggbd/2026-02-26/doc-inhpaaih2056617.shtml','2026-02-26','authoritative_media','河化股份聘任杨和荣为董事长及非独立董事','2026 listed-company-announcement coverage states 杨和荣 has served as 中哲控股董事长 since 2006 and was appointed 河化股份董事长 in Feb-2026. Zhejiang/Ningbo enterprise context plus the historical federation roster safely bridges identity.')
add(797,'恒逸石化股份有限公司','董事长、总裁','B','https://finance.sina.com.cn/wm/2026-04-16/doc-inhuryeq4086832.shtml','2026-04-16','authoritative_media','恒逸石化2025年年度报告解读','2026 annual-report-based coverage explicitly gives 邱奕博 as current 恒逸石化董事长兼总裁; historical Zhejiang federation identity and enterprise context are consistent.')
add(801,'浙江野马电池股份有限公司','总经理','B','https://stock.stockstar.com/IG2026052000022007.shtml','2026-05-20','authoritative_media','野马电池2025年年度报告解读','2026 annual-report-based evidence states 余谷峰 is 野马电池总经理. The uncommon name, Zhejiang enterprise context and historical federation roster provide a safe identity bridge.')
add(804,'万凯新材料股份有限公司','董事长','B','https://finance.sina.com.cn/stock/aigc/gdhjy/2026-04-21/doc-inhvheyy6217237.shtml','2026-04-21','authoritative_media','万凯新材2026年第一次临时股东会董事会换届','2026 company-meeting/announcement coverage identifies 沈志刚 as the serving chairman who presided over the meeting; historical Zhejiang federation identity plus Zhejiang enterprise history closes the bridge.')
add(808,'宁波激智科技股份有限公司','董事长','B','https://www.rmzxw.com.cn/c/2026-07-30/3955155.shtml','2026-07-30','authoritative_media','让“全球合伙人”加速集聚','People\'s CPPCC reporting identifies 张彦 as 浙江省政协委员、宁波市侨联兼职副主席、激智科技董事长. Combined with the Zhejiang federation source context, this is not a name-only hit.')
add(814,'太平鸟集团有限公司','董事长','B','https://www.eeo.com.cn/2026/0605/904315.shtml','2026-06-05','authoritative_media','开出“诊断单”后，太平鸟用三年完成一场大手术','2026 Economic Observer reporting repeatedly identifies 张江平 as 太平鸟集团董事长; Ningbo/Zhejiang enterprise and public-representative context closes identity to the federation source row.')
add(819,'泰昌集团有限公司','董事长、总裁','B','https://news.66wz.com/system/2026/08/21/105825502.shtml','2026-08-21','authoritative_media','温州市“追光”思政课首次走进民企','Current Wenzhou Daily/66wz reporting explicitly identifies 张鹏飞 as 泰昌集团董事长兼总裁; Zhejiang/Wenzhou business context and the historical federation roster safely bridge identity.')
add(824,'方远集团','党委书记、总裁','B','https://finance.sina.com.cn/jjxw/2026-01-18/doc-inhhttqp3404385.shtml','2026-01-18','authoritative_media','代表委员热议“好房子、好小区、好社区、好城区建设”','2026 Zhejiang public reporting identifies 陈志军 as 省政协委员、方远集团党委书记、总裁. A separate current provincial federation article also identifies 陈志军 as a 工商联界别委员, providing non-name-only identity context.')
add(828,'宁波市工商业联合会 / 宁波市台州商会','副主席 / 会长','A','https://nbsczsh.com/','2026-08-04','formal_association_official','宁波市工商联商协会秘书处综合能力提升培训','Current Ningbo chamber-official material identifies 陈春明 as 宁波市工商联副主席、市台州商会会长. The federation/chamber context directly bridges the historical Zhejiang provincial federation row.')
add(832,'中国民主建国会浙江省委员会','副主任委员','A','https://www.hzmj.org.cn/XueXiXuanChuan/20263524928354.html','2026-05-11','formal_association_official','纪念“五一口号”发布78周年暨全省民建爱国主义教育基地联盟活动','Current 民建杭州 official material lists 陈越孟 among 民建浙江省委会副主委. Historical Zhejiang federation identity plus same-province public-role context closes identity safely.')
# Current federation/chamber assignments resolved by the live provincial leadership page.
# All other rows were individually/targetedly checked and remain unresolved rather than guessed.
results=[]
for r in rows:
    q=int(r['queue_order']); name=r['name_normalized']
    out={'queue_order':r['queue_order'],'person_id':r['person_id'],'province':r['province'],'excel_row':r['excel_row'],'name_normalized':name,'source_federation_role':r['federation_role'],'candidate_names':name}
    if q in special:
        org,title,grade,url,date,etype,etitle,notes=special[q]
        out.update(identity_resolution='CURRENT_ROLE_CONFIRMED_WITH_CONTEXT_BRIDGE',current_organization=org,current_title=title,current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type=etype,evidence_grade=grade,evidence_title=etitle,evidence_url=url,evidence_date=date,unresolved_reason='',research_notes=notes)
    elif name in live_fed:
        out.update(identity_resolution='CURRENT_ROLE_CONFIRMED_BY_LIVE_OFFICIAL_PROVINCIAL_LEADERSHIP_PAGE',current_organization='浙江省工商业联合会',current_title='副主席',current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type='federation_official',evidence_grade='A',evidence_title='浙江省工商业联合会（浙江省商会）商会领导',evidence_url=LIVE,evidence_date='2026-09-20',unresolved_reason='',research_notes='Live official provincial federation page directly names the person and current role; mapping uses name+province+federation context and preserves the source person_id.')
    elif name in live_ch:
        out.update(identity_resolution='CURRENT_ROLE_CONFIRMED_BY_LIVE_OFFICIAL_PROVINCIAL_LEADERSHIP_PAGE',current_organization='浙江省商会',current_title='副会长',current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type='federation_official',evidence_grade='A',evidence_title='浙江省工商业联合会（浙江省商会）商会领导',evidence_url=LIVE,evidence_date='2026-09-20',unresolved_reason='',research_notes='Live official provincial chamber page directly names the person as current vice-chair; source person_id remains distinct.')
    elif name=='林建良':
        out.update(identity_resolution='CURRENT_ROLE_CONFIRMED_BY_LIVE_OFFICIAL_PROVINCIAL_LEADERSHIP_PAGE',current_organization='浙江省工商业联合会',current_title='党组成员、一级巡视员',current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type='federation_official',evidence_grade='A',evidence_title='浙江省工商业联合会（浙江省商会）商会领导',evidence_url=LIVE,evidence_date='2026-09-20',unresolved_reason='',research_notes='Live official provincial leadership page lists 林建良 as 浙江省工商联党组成员、一级巡视员; the older deputy-chair/chamber title is not carried forward.')
    elif name=='宋立':
        out.update(identity_resolution='CURRENT_ROLE_CONFIRMED_BY_LIVE_OFFICIAL_PROVINCIAL_LEADERSHIP_PAGE',current_organization='浙江省工商业联合会 / 浙江省商会',current_title='党组成员、秘书长 / 秘书长',current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type='federation_official',evidence_grade='A',evidence_title='浙江省工商业联合会（浙江省商会）商会领导',evidence_url=LIVE,evidence_date='2026-09-20',unresolved_reason='',research_notes='Live official provincial page directly confirms current secretary-general roles.')
    else:
        out.update(identity_resolution='HISTORICAL_SOURCE_IDENTITY_CURRENT_ROLE_UNRESOLVED',current_organization='',current_title='',current_verification_status='UNRESOLVED_CURRENT_ORG_TITLE',evidence_type='targeted_public_current_verification',evidence_grade='A',evidence_title='ACFIC Zhejiang 2022 standing-committee identity + 2026 targeted current verification',evidence_url=HIST,evidence_date='2026-09-20',unresolved_reason=f'{name} is confirmed in the official 2022 Zhejiang federation standing-committee roster, but targeted current public research did not establish a sufficiently specific, current organization/title with a safe identity bridge.',research_notes='Current public sources were searched using federation/province/business context. No current organization/title is asserted where only a same-name or stale role could be found.')
    results.append(out)
assert len(results)==60
confirmed=sum(r['current_verification_status']=='CURRENT_ORG_TITLE_CONFIRMED' for r in results); unres=60-confirmed
a_grade=sum(r['evidence_grade']=='A' for r in results); b_grade=sum(r['evidence_grade']=='B' for r in results)
assert (confirmed,unres,a_grade,b_grade)==(28,32,50,10),(confirmed,unres,a_grade,b_grade)
assert all(r['evidence_url'] and r['unresolved_reason'] if r['current_verification_status'].startswith('UNRESOLVED') else r['evidence_url'] for r in results)
with open(E/'W3_BATCH_0014_RESULTS.csv','w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator='\n'); w.writeheader(); w.writerows(results)
LEDGER_FIELDS=['queue_order','person_id','province','excel_row','candidate_names','evidence_type','evidence_grade','evidence_title','evidence_url','evidence_date','current_verification_status','unresolved_reason']
OVERLAY_FIELDS=['queue_order','person_id','province','excel_row','identity_resolution','candidate_names','current_organization','current_title','current_verification_status','evidence_grade','evidence_url','unresolved_reason']
def append_rows(path,fields):
    with open(path,'r',encoding='utf-8-sig',newline='') as f: old=list(csv.DictReader(f))
    last=int(old[-1]['queue_order'])
    if last==840: return
    assert last==780,(path,last)
    with open(path,'a',encoding='utf-8',newline='') as f: csv.DictWriter(f,fieldnames=fields,extrasaction='ignore',lineterminator='\n').writerows(results)
append_rows(E/'W3_EVIDENCE_LEDGER.csv',LEDGER_FIELDS); append_rows(E/'W3_VERIFICATION_OVERLAY.csv',OVERLAY_FIELDS)
for p in [E/'W3_EVIDENCE_LEDGER.csv',E/'W3_VERIFICATION_OVERLAY.csv']:
    with open(p,'r',encoding='utf-8-sig',newline='') as f: rr=list(csv.DictReader(f))
    orders=[int(x['queue_order']) for x in rr]
    assert len(rr)==840 and orders==list(range(1,841)) and len(set(orders))==840
(E/'W3_BATCH_0014_METRICS.yaml').write_text(f'''schema: fc2515-w3-batch-metrics-v1
project_id: FC-EXEC-2515-01
gate: W3-BATCH-0014
status: PASS
queue_range: [781, 840]
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
  processed_queue_rows: 840
  actionable_queue_remaining: 9804
  next_queue_order: 841
  p1_processed: 739
  p1_remaining: 3592
next_gate: W3-BATCH-0015
''',encoding='utf-8')
validation=f'''# W3-BATCH-0014 Validation

Result: **PASS**

- Deterministic queue slice: 781–840 exactly, 60 浙江 P1_IDENTITY rows; no rows outside this repository-defined gate were touched.
- Every touched row has public evidence or an explicit unresolved-current-role reason; unsupported current-title claims: 0.
- Live Zhejiang federation/chamber leadership directly closes 16 current-role rows; repeated source appearances preserve distinct person_id values.
- 12 additional current roles were closed only with context bridges from 2026 public evidence, including 阮伟祥、李建滨、杨和荣、邱奕博、余谷峰、沈志刚、张彦、张江平、张鹏飞、陈志军、陈春明、陈越孟.
- 32 rows remain explicit current-role unresolved cases. Same-name, stale or weakly bridged hits were rejected rather than promoted to claims.
- Evidence grades: A={a_grade}, B={b_grade}, C=0; current organization/title confirmed={confirmed}/60; unresolved={unres}/60.
- No current organization/title was assigned from a name-only hit.
- Cumulative evidence ledger and verification overlay each reconcile to 840 rows with queue_order 1..840, no gaps or duplicates.

Next deterministic gate: `W3-BATCH-0015`, starting queue_order 841.
'''
(E/'W3_BATCH_0014_VALIDATION.md').write_text(validation,encoding='utf-8')
sp=ROOT/'STATUS.yaml'; s=sp.read_text(encoding='utf-8')
def sub1(text,a,b):
    assert a in text,a
    return text.replace(a,b,1)
s=sub1(s,'code: W3-BATCH-0013\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS','code: W3-BATCH-0014\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS')
s=sub1(s,'code: W3-BATCH-0014\n  phase: W3-EVIDENCE-ENRICH\n  status: READY','code: W3-BATCH-0015\n  phase: W3-EVIDENCE-ENRICH\n  status: READY')
for a,b in [('  batches_sealed: 13','  batches_sealed: 14'),('  processed_queue_rows: 780','  processed_queue_rows: 840'),('  next_queue_order: 781','  next_queue_order: 841'),('  actionable_queue_remaining: 9864','  actionable_queue_remaining: 9804'),('  identity_evidence_rows: 780','  identity_evidence_rows: 840'),('  current_org_title_confirmed_rows: 473','  current_org_title_confirmed_rows: 501'),('  current_org_title_unresolved_rows: 204','  current_org_title_unresolved_rows: 236')]: s=sub1(s,a,b)
s=sub1(s,'    processed: 679\n    remaining: 3652','    processed: 739\n    remaining: 3592')
anchor='  w3_batch_0013_validation: projects/fc-exec-2515/evidence/W3_BATCH_0013_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv'
rep='  w3_batch_0013_validation: projects/fc-exec-2515/evidence/W3_BATCH_0013_VALIDATION.md\n  w3_batch_0014_results: projects/fc-exec-2515/evidence/W3_BATCH_0014_RESULTS.csv\n  w3_batch_0014_metrics: projects/fc-exec-2515/evidence/W3_BATCH_0014_METRICS.yaml\n  w3_batch_0014_validation: projects/fc-exec-2515/evidence/W3_BATCH_0014_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv'
s=sub1(s,anchor,rep); sp.write_text(s,encoding='utf-8')
cp=ROOT/'CURRENT.yaml'; c=cp.read_text(encoding='utf-8')
c=sub1(c,'current_gate: W3-BATCH-0014','current_gate: W3-BATCH-0015')
c=sub1(c,'work_cursor: 780','work_cursor: 840')
c=sub1(c,'verified_records: 475','verified_records: 503')
c=sub1(c,'unresolved_records: 10169','unresolved_records: 10141')
c=sub1(c,'  processed: 780','  processed: 840')
c=sub1(c,'  actionable_remaining: 9864','  actionable_remaining: 9804')
c=sub1(c,'  next_queue_order: 781','  next_queue_order: 841')
c=sub1(c,'      processed: 679\n      remaining: 3652','      processed: 739\n      remaining: 3592')
c=sub1(c,'last_input_head: 9138a4410a2723bf83bf133be782ccc37bd4edec',f'last_input_head: {INPUT_HEAD}')
c,n=re.subn(r'last_evidence_at: .*',f'last_evidence_at: {NOW}',c,count=1); assert n==1
section=f'''\nw3_batch_0014:
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
notes=f'''  - W3-BATCH-0014 processed queue orders 781-840 exactly, all 60 浙江 P1 identity/current-role rows.
  - {confirmed} rows received current organization/title confirmation; {unres} remain explicit unresolved where current evidence was stale, ambiguous, or insufficiently linked to the source identity.
  - The live Zhejiang federation/chamber leadership page directly closed 16 current roles; a further 12 were closed only with contextual current evidence and historical federation identity anchors.
  - Strong 2026 closures include 阮伟祥、杨和荣、邱奕博、余谷峰、沈志刚、张彦、张江平、张鹏飞、陈志军、陈春明、陈越孟; no name-only assignment was permitted.
  - Same-name or weakly bridged hits for the remaining rows were preserved as unresolved rather than guessed.
  - Evidence grades are A={a_grade}, B={b_grade}, C=0; unsupported current-title claims=0.
  - Next deterministic queue order is 841.
'''
c=c.rstrip()+'\n'+notes; cp.write_text(c,encoding='utf-8')
st=sp.read_text(encoding='utf-8'); ct=cp.read_text(encoding='utf-8')
assert 'latest_gate:\n  code: W3-BATCH-0014' in st and 'next_gate:\n  code: W3-BATCH-0015' in st
assert 'current_gate: W3-BATCH-0015' in ct and 'work_cursor: 840' in ct and 'next_queue_order: 841' in ct
print(f'PASS W3-BATCH-0014 confirmed={confirmed} unresolved={unres} A={a_grade} B={b_grade} now={NOW}')
