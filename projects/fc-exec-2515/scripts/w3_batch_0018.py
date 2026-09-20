#!/usr/bin/env python3
import csv, gzip, pathlib, datetime, re, subprocess, glob
ROOT=pathlib.Path(__file__).resolve().parents[1]; E=ROOT/'evidence'; REPO=ROOT.parents[1]
INPUT_HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
assert INPUT_HEAD=='7f01f67213e48af96c1e896921d60d3f4466b378', INPUT_HEAD
NOW=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).replace(microsecond=0).isoformat()
with gzip.open(E/'W2_UNRESOLVED_QUEUE.csv.gz','rt',encoding='utf-8-sig',newline='') as f: allq=list(csv.DictReader(f))
rows=allq[1020:1080]
assert len(rows)==60 and [int(r['queue_order']) for r in rows]==list(range(1021,1081))
assert sum(r['province']=='浙江' for r in rows)==22 and sum(r['province']=='安徽' for r in rows)==38
assert {r['priority'] for r in rows}=={'P1_IDENTITY'}

ZJ_LIVE='https://www.zjfic.org.cn/col/col1620079/index.html'
ZJ_HIST='https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_zj/202209/t20220919_313059.html'
AH_LIVE='https://www.ahgcc.cn/Survey/'
AH_HIST='https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_ah/202208/t20220802_312829.html'
TAIER='https://www.taiergroup.com/'
GAOJUN_CONFLICT='https://www.sohu.com/a/1035630526_100126234'
VERIFY_DATE='2026-09-20'

# Load all already sealed W3 result rows. For Zhejiang cross-listed rows, reuse is permitted only
# when exact normalized name + province + the repository ambiguity_group_id all agree.
prior_results={}
for fn in sorted(glob.glob(str(E/'W3_BATCH_*_RESULTS.csv'))):
    if fn.endswith('W3_BATCH_0018_RESULTS.csv'): continue
    with open(fn,'r',encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f): prior_results[int(r['queue_order'])]=r

def latest_prior(target):
    candidates=[r for r in allq if int(r['queue_order'])<1021 and r['province']==target['province'] and r['name_normalized']==target['name_normalized'] and r['ambiguity_group_id']==target['ambiguity_group_id'] and int(r['queue_order']) in prior_results]
    assert candidates, target
    p=max(candidates,key=lambda r:int(r['queue_order']))
    return p, prior_results[int(p['queue_order'])]

zj_fed_vp={'屠红燕','傅利泉','鲁伟鼎','赖梅松'}
zj_ch_vp={'黄军民','蒋晓萌','谢识才','詹洪良','潘建清'}
zj_expected_unresolved={'龚浩强','梁斌','董伟国','董凌宇','蒋文标','潘云峰'}

# Current Anhui roles copied from the live official 安徽省工商联（总商会） leadership surface.
# For entrepreneurs we store the enterprise role as current organization/title while preserving the
# source federation role in source_federation_role and the federation context in evidence provenance.
ah_current={
 '王翠凤':('安徽省工商业联合会 / 安徽省总商会','主席 / 会长'),
 '聂磊':('安徽省工商业联合会 / 安徽省总商会','副主席 / 副会长'),
 '李增流':('安徽省工商业联合会 / 安徽省总商会','党组成员、副主席兼秘书长 / 副会长'),
 '王光平':('安徽光太实业集团','总裁'),
 '尤加林':('安徽加林集团','董事长'),
 '施卫东':('安徽德力日用玻璃股份有限公司','董事长'),
 '徐进':('安徽口子酒业股份有限公司','董事长'),
 '徐珍玉':('安徽朗坤物联网有限公司','董事长'),
 '潘保春':('合肥荣事达电子电器集团有限公司','董事长'),
 '余竹云':('中环控股集团有限公司','董事长'),
 '卢立新':('安徽共生物流科技有限公司','董事长'),
 '李健':('安徽宣酒集团股份有限公司','董事长、党委副书记'),
 '吴成月':('安徽长安开元投资集团','董事长'),
 '高晓谋':('安徽中天石化股份有限公司','董事长'),
 '薛颖':('安徽工艺贸易进出口有限公司','投资人、董事'),
 '朱圣杰':('安徽人和节能科技有限责任公司','董事长'),
 '徐玉美':('安徽国邦实业集团','董事长'),
 '姚和平':('安徽安利材料科技股份有限公司','党委书记、董事长、总经理'),
 '冯雷':('合肥维天运通信息科技股份有限公司','董事长'),
 '李万军':('安徽智飞龙科马生物制药有限公司','董事长'),
 '刘庆峰':('科大讯飞股份有限公司','董事长'),
 '程振朔':('安徽新远科技股份有限公司','董事长'),
 '王磊':('安徽桃花源工贸集团 / 安徽桃花源实业有限公司','执行董事 / 董事长'),
 '陈冬梅':('合肥华泰集团股份有限公司','董事长'),
 '丁超毅':('安徽绿桐科技有限公司','董事长'),
 '王正前':('合肥安达创展科技股份有限公司','董事长、总经理'),
 '卢育发':('安徽天柱绿色能源科技有限公司','总经理'),
 '吕彬':('安徽瓦大现代农业科技有限公司','董事长'),
 '刘伟':('宏晶微电子科技股份有限公司','董事长'),
 '何仿':('合肥京东方医院','院长'),
 '沈君':('安徽致君利再生科技有限公司','董事长'),
}
assert len(ah_current)==31
ah_absent_unresolved={'胡春华','高维民','尹正龙','周勇','林巨广'}

FIELDS=['queue_order','person_id','province','excel_row','name_normalized','source_federation_role','identity_resolution','candidate_names','current_organization','current_title','current_verification_status','evidence_type','evidence_grade','evidence_title','evidence_url','evidence_date','unresolved_reason','research_notes']
results=[]
for t in rows:
    q=int(t['queue_order']); name=t['name_normalized']
    out={'queue_order':t['queue_order'],'person_id':t['person_id'],'province':t['province'],'excel_row':t['excel_row'],'name_normalized':name,'source_federation_role':t['federation_role'],'candidate_names':name}
    if t['province']=='浙江':
        p,old=latest_prior(t)
        bridge=f'Cross-listed Zhejiang row linked only through exact name + province + ambiguity_group_id {t["ambiguity_group_id"]} to sealed queue {p["queue_order"]}; person_id remains distinct. '
        if name in zj_fed_vp:
            out.update(identity_resolution='CURRENT_ROLE_CONFIRMED_BY_LIVE_OFFICIAL_PROVINCIAL_LEADERSHIP_PAGE',current_organization='浙江省工商业联合会',current_title='副主席',current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type='federation_official',evidence_grade='A',evidence_title='浙江省工商业联合会（浙江省商会）商会领导',evidence_url=ZJ_LIVE,evidence_date=VERIFY_DATE,unresolved_reason='',research_notes=bridge+'Live official Zhejiang leadership page was re-read in this gate and independently reconfirms the current provincial vice-chair role.')
        elif name in zj_ch_vp:
            out.update(identity_resolution='CURRENT_ROLE_CONFIRMED_BY_LIVE_OFFICIAL_PROVINCIAL_LEADERSHIP_PAGE',current_organization='浙江省商会',current_title='副会长',current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type='federation_official',evidence_grade='A',evidence_title='浙江省工商业联合会（浙江省商会）商会领导',evidence_url=ZJ_LIVE,evidence_date=VERIFY_DATE,unresolved_reason='',research_notes=bridge+'Live official Zhejiang leadership page was re-read in this gate and independently reconfirms the current chamber vice-chair role.')
        elif old['current_verification_status']=='CURRENT_ORG_TITLE_CONFIRMED':
            out.update(identity_resolution='CURRENT_ROLE_CONFIRMED_BY_SEALED_CROSSLIST_CONTEXT',current_organization=old['current_organization'],current_title=old['current_title'],current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type=old['evidence_type'],evidence_grade=old['evidence_grade'],evidence_title=old['evidence_title'],evidence_url=old['evidence_url'],evidence_date=old['evidence_date'],unresolved_reason='',research_notes=bridge+'The already sealed current-role evidence remains 2026-current; targeted refresh found no contradictory identity/title evidence. No name-only inference was used.')
        else:
            assert name in zj_expected_unresolved
            out.update(identity_resolution='CROSSLIST_IDENTITY_CURRENT_ROLE_UNRESOLVED',current_organization='',current_title='',current_verification_status='UNRESOLVED_CURRENT_ORG_TITLE',evidence_type='targeted_public_current_verification',evidence_grade='A',evidence_title='ACFIC Zhejiang 2022 identity anchor + 2026 targeted current verification',evidence_url=ZJ_HIST,evidence_date=VERIFY_DATE,unresolved_reason=f'{name} remains current-role unresolved: refreshed public research did not establish a sufficiently specific current organization/title with a safe identity bridge.',research_notes=bridge+'Same-name, stale, or weakly bridged current hits were rejected; historical A-grade federation identity is preserved without inventing a current employer/title.')
    else:
        assert t['province']=='安徽'
        hist=f'ACFIC 2022 Anhui election roster anchors {name} to this exact provincial federation role ({t["federation_role"]}). '
        if name in ah_current:
            org,title=ah_current[name]
            out.update(identity_resolution='CURRENT_ROLE_CONFIRMED_BY_LIVE_OFFICIAL_ANHUI_LEADERSHIP_PAGE',current_organization=org,current_title=title,current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type='federation_official',evidence_grade='A',evidence_title='安徽省工商业联合会（总商会）现任领导',evidence_url=AH_LIVE,evidence_date=VERIFY_DATE,unresolved_reason='',research_notes=hist+'The live official Anhui federation/chamber leadership surface directly lists this person together with the current federation role and the stored current organization/title; identity is therefore closed by federation context, not name alone.')
        elif name=='邰紫鹏':
            out.update(identity_resolution='CURRENT_ROLE_REFRESHED_BY_ENTERPRISE_OFFICIAL_WITH_FEDERATION_IDENTITY_BRIDGE',current_organization='泰尔重工股份有限公司',current_title='党委书记、董事长',current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type='enterprise_official',evidence_grade='A',evidence_title='泰尔重工官网新闻中心：邰紫鹏现任党委书记、董事长',evidence_url=TAIER,evidence_date=VERIFY_DATE,unresolved_reason='',research_notes=hist+'The live Anhui federation surface independently links the same identity to 泰尔重工, while the current enterprise official site refreshes the company title to 党委书记、董事长, superseding the older 总经理 wording on the federation page.')
        elif name=='高君':
            out.update(identity_resolution='CURRENT_ROLE_CONFLICT_UNRESOLVED',current_organization='',current_title='',current_verification_status='UNRESOLVED_CURRENT_ORG_TITLE',evidence_type='federation_official',evidence_grade='A',evidence_title='安徽省工商联现任领导页 + 2026 current-role conflict review',evidence_url=AH_LIVE,evidence_date=VERIFY_DATE,unresolved_reason='高君 current-role status is conflict-held: the official Anhui federation surface still lists him as 省总商会副会长、宝业集团安徽有限公司总经理, while June 2026 reporting says he was taken measures and had lost contact; no current organization/title is asserted until the conflict is cleared.',research_notes=hist+'Current official federation listing was preserved as evidence but not promoted into current fields because later public reporting creates a material status conflict. Conflict reference: '+GAOJUN_CONFLICT)
        else:
            assert name in ah_absent_unresolved, name
            out.update(identity_resolution='HISTORICAL_IDENTITY_CURRENT_ROLE_UNRESOLVED',current_organization='',current_title='',current_verification_status='UNRESOLVED_CURRENT_ORG_TITLE',evidence_type='targeted_public_current_verification',evidence_grade='A',evidence_title='ACFIC Anhui 2022 election identity + 2026 official-leadership/current-role verification',evidence_url=AH_HIST,evidence_date=VERIFY_DATE,unresolved_reason=f'{name} remains current-role unresolved: the historical federation identity is verified, but the current official Anhui leadership surface no longer lists the name and targeted current research did not safely establish a replacement organization/title.',research_notes=hist+'Absence from the current leadership surface is not treated as proof of no current role; no name-only replacement match is promoted.')
    results.append(out)

assert len(results)==60
confirmed=sum(r['current_verification_status']=='CURRENT_ORG_TITLE_CONFIRMED' for r in results)
unres=sum(r['current_verification_status']=='UNRESOLVED_CURRENT_ORG_TITLE' for r in results)
a_grade=sum(r['evidence_grade']=='A' for r in results); b_grade=sum(r['evidence_grade']=='B' for r in results); c_grade=sum(r['evidence_grade']=='C' for r in results)
assert (confirmed,unres,a_grade,b_grade,c_grade)==(48,12,55,5,0),(confirmed,unres,a_grade,b_grade,c_grade)
assert all(r['evidence_url'] for r in results)
assert all((r['current_organization'] and r['current_title'] and not r['unresolved_reason']) if r['current_verification_status']=='CURRENT_ORG_TITLE_CONFIRMED' else (not r['current_organization'] and not r['current_title'] and r['unresolved_reason']) for r in results)

with open(E/'W3_BATCH_0018_RESULTS.csv','w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator='\n'); w.writeheader(); w.writerows(results)
LEDGER_FIELDS=['queue_order','person_id','province','excel_row','candidate_names','evidence_type','evidence_grade','evidence_title','evidence_url','evidence_date','current_verification_status','unresolved_reason']
OVERLAY_FIELDS=['queue_order','person_id','province','excel_row','identity_resolution','candidate_names','current_organization','current_title','current_verification_status','evidence_grade','evidence_url','unresolved_reason']
def append_rows(path,fields):
    with open(path,'r',encoding='utf-8-sig',newline='') as f: old=list(csv.DictReader(f))
    last=int(old[-1]['queue_order'])
    if last==1080: return
    assert last==1020,(path,last)
    with open(path,'a',encoding='utf-8',newline='') as f: csv.DictWriter(f,fieldnames=fields,extrasaction='ignore',lineterminator='\n').writerows(results)
append_rows(E/'W3_EVIDENCE_LEDGER.csv',LEDGER_FIELDS); append_rows(E/'W3_VERIFICATION_OVERLAY.csv',OVERLAY_FIELDS)
for pth in [E/'W3_EVIDENCE_LEDGER.csv',E/'W3_VERIFICATION_OVERLAY.csv']:
    with open(pth,'r',encoding='utf-8-sig',newline='') as f: rr=list(csv.DictReader(f))
    orders=[int(x['queue_order']) for x in rr]
    assert len(rr)==1080 and orders==list(range(1,1081)) and len(set(orders))==1080

(E/'W3_BATCH_0018_METRICS.yaml').write_text(f'''schema: fc2515-w3-batch-metrics-v1
project_id: FC-EXEC-2515-01
gate: W3-BATCH-0018
status: PASS
queue_range: [1021, 1080]
batch_rows: 60
zhejiang_rows: 22
anhui_rows: 38
p1_identity_rows: 60
evidence_backed_rows: 60
a_grade_rows: {a_grade}
b_grade_rows: {b_grade}
c_grade_rows: {c_grade}
structural_deferred_rows: 0
current_org_title_confirmed_rows: {confirmed}
no_current_role_confirmed_rows: 0
current_org_title_unresolved_rows: {unres}
unsupported_current_title_claims: 0
post_batch:
  processed_queue_rows: 1080
  actionable_queue_remaining: 9564
  next_queue_order: 1081
  p1_processed: 979
  p1_remaining: 3352
next_gate: W3-BATCH-0019
''',encoding='utf-8')

(E/'W3_BATCH_0018_VALIDATION.md').write_text(f'''# W3-BATCH-0018 Validation

Result: **PASS**

- Deterministic repository queue slice: 1021–1080 exactly, 60 `P1_IDENTITY` rows (浙江 22, 安徽 38); no rows outside this gate were processed.
- Every touched row has public evidence or an explicit unresolved-current-role reason; unsupported current-title claims: 0.
- Zhejiang cross-listed rows were bridged only through exact name + province + the same repository ambiguity group; each source row retains its own `person_id`.
- Zhejiang's live official federation/chamber leadership page was re-read and directly reconfirmed touched current leadership roles; other sealed 2026 evidence was reused only after exact cross-list identity closure.
- Anhui's official current leadership surface was read as the primary current-state authority for touched provincial federation/chamber identities and directly provides enterprise roles for the confirmed entrepreneur records.
- Historical 安徽 identities absent from the current official leadership surface (胡春华、高维民、尹正龙、周勇、林巨广) remain explicit unresolved rather than being name-matched to unrelated people.
- 高君 is held unresolved because current official federation listing conflicts with later June-2026 public status reporting; no current title is asserted pending conflict clearing.
- 邰紫鹏 is refreshed to 泰尔重工党委书记、董事长 using current enterprise-official evidence; the older 总经理 wording is not propagated.
- Evidence grades: A={a_grade}, B={b_grade}, C={c_grade}; current organization/title confirmed={confirmed}/60; unresolved={unres}/60.
- Cumulative evidence ledger and verification overlay each reconcile to 1080 rows with `queue_order` 1..1080, no gaps or duplicates.

Next deterministic gate: `W3-BATCH-0019`, starting `queue_order=1081`.
''',encoding='utf-8')

# Repository-authoritative control state update.
def sub1(text,a,b):
    assert a in text,a
    return text.replace(a,b,1)
sp=ROOT/'STATUS.yaml'; s=sp.read_text(encoding='utf-8')
s=sub1(s,'code: W3-BATCH-0017\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS','code: W3-BATCH-0018\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS')
s=sub1(s,'code: W3-BATCH-0018\n  phase: W3-EVIDENCE-ENRICH\n  status: READY','code: W3-BATCH-0019\n  phase: W3-EVIDENCE-ENRICH\n  status: READY')
for a,b in [('  batches_sealed: 17','  batches_sealed: 18'),('  processed_queue_rows: 1020','  processed_queue_rows: 1080'),('  next_queue_order: 1021','  next_queue_order: 1081'),('  actionable_queue_remaining: 9624','  actionable_queue_remaining: 9564'),('  identity_evidence_rows: 1020','  identity_evidence_rows: 1080')]: s=sub1(s,a,b)
s=sub1(s,'    processed: 919\n    remaining: 3412','    processed: 979\n    remaining: 3352')
s=sub1(s,'  current_org_title_confirmed_rows: 609','  current_org_title_confirmed_rows: 657')
s=sub1(s,'  current_org_title_unresolved_rows: 308','  current_org_title_unresolved_rows: 320')
anchor='  w3_batch_0017_validation: projects/fc-exec-2515/evidence/W3_BATCH_0017_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv'
rep='  w3_batch_0017_validation: projects/fc-exec-2515/evidence/W3_BATCH_0017_VALIDATION.md\n  w3_batch_0018_results: projects/fc-exec-2515/evidence/W3_BATCH_0018_RESULTS.csv\n  w3_batch_0018_metrics: projects/fc-exec-2515/evidence/W3_BATCH_0018_METRICS.yaml\n  w3_batch_0018_validation: projects/fc-exec-2515/evidence/W3_BATCH_0018_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv'
s=sub1(s,anchor,rep); sp.write_text(s,encoding='utf-8')

cp=ROOT/'CURRENT.yaml'; c=cp.read_text(encoding='utf-8')
c=sub1(c,'current_gate: W3-BATCH-0018','current_gate: W3-BATCH-0019')
c=sub1(c,'work_cursor: 1020','work_cursor: 1080')
c=sub1(c,'verified_records: 611','verified_records: 659')
c=sub1(c,'unresolved_records: 10033','unresolved_records: 9985')
c=sub1(c,'  processed: 1020','  processed: 1080')
c=sub1(c,'  actionable_remaining: 9624','  actionable_remaining: 9564')
c=sub1(c,'  next_queue_order: 1021','  next_queue_order: 1081')
c=sub1(c,'      processed: 919\n      remaining: 3412','      processed: 979\n      remaining: 3352')
c,n=re.subn(r'last_input_head: .*',f'last_input_head: {INPUT_HEAD}',c,count=1); assert n==1
c,n=re.subn(r'last_evidence_at: .*',f'last_evidence_at: {NOW}',c,count=1); assert n==1
section=f'''\nw3_batch_0018:\n  status: SEALED\n  validation: PASS\n  touched_rows: 60\n  zhejiang_rows: 22\n  anhui_rows: 38\n  p1_identity_rows: 60\n  evidence_backed_rows: 60\n  a_grade_rows: {a_grade}\n  b_grade_rows: {b_grade}\n  c_grade_rows: {c_grade}\n  current_org_title_confirmed_rows: {confirmed}\n  current_org_title_unresolved_rows: {unres}\n  unsupported_current_title_claims: 0\n\n'''
c=sub1(c,'\nnotes:\n','\n'+section+'notes:\n')
notes=f'''  - W3-BATCH-0018 processed queue orders 1021-1080 exactly: 22 Zhejiang and 38 Anhui P1 identity/current-role rows.\n  - {confirmed} rows received current organization/title confirmation; {unres} remain explicit unresolved with no unsupported current-title claims.\n  - Zhejiang cross-listed identities were reused only through exact name + province + the same ambiguity_group_id; person_id values remain source-row distinct.\n  - Anhui current roles were grounded primarily in the live official 安徽省工商联（总商会） leadership surface, which directly links federation identities to current enterprise roles.\n  - 胡春华、高维民、尹正龙、周勇、林巨广 were not on the current Anhui official leadership surface and remain unresolved; absence was not converted into a no-current-role claim.\n  - 高君 is conflict-held rather than promoted because official federation listing and later 2026 status reporting diverge.\n  - 邰紫鹏 was refreshed from older 总经理 wording to current enterprise-official 党委书记、董事长 evidence.\n  - Evidence grades are A={a_grade}, B={b_grade}, C={c_grade}; next deterministic queue order is 1081.\n'''
c=c.rstrip()+'\n'+notes; cp.write_text(c,encoding='utf-8')

st=sp.read_text(encoding='utf-8'); ct=cp.read_text(encoding='utf-8')
assert 'latest_gate:\n  code: W3-BATCH-0018' in st and 'next_gate:\n  code: W3-BATCH-0019' in st
assert 'current_gate: W3-BATCH-0019' in ct and 'work_cursor: 1080' in ct and 'next_queue_order: 1081' in ct
print(f'PASS W3-BATCH-0018 confirmed={confirmed} unresolved={unres} A={a_grade} B={b_grade} C={c_grade} now={NOW}')
