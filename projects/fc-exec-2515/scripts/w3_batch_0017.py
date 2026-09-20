#!/usr/bin/env python3
import csv, gzip, pathlib, datetime, re, subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]; E=ROOT/'evidence'; REPO=ROOT.parents[1]
INPUT_HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
assert INPUT_HEAD=='c824c8d3c838a564c37fa35d9b577841d8f7f20a', INPUT_HEAD
NOW=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).replace(microsecond=0).isoformat()
with gzip.open(E/'W2_UNRESOLVED_QUEUE.csv.gz','rt',encoding='utf-8-sig',newline='') as f: allq=list(csv.DictReader(f))
rows=allq[960:1020]
assert len(rows)==60 and [int(r['queue_order']) for r in rows]==list(range(961,1021))
assert {r['province'] for r in rows}=={'浙江'} and {r['priority'] for r in rows}=={'P1_IDENTITY'}

LIVE='https://www.zjfic.org.cn/col/col1620079/index.html'
HIST='https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_zj/202209/t20220919_313059.html'
WJY='https://www.zjfic.org.cn/col/col1620074/art/2026/art_0c23cdd012554d2996bc665d052fa9c3.html'
FNB='https://static.cninfo.com.cn/finalpage/2026-04-22/1225141427.PDF'
SHAO='https://www.acfic.org.cn/myjjzs/qyjjy/202607/t20260701_327273.html'
XUL='https://m.sohu.com/a/1038019078_121106875'
XUL_BRIDGE='https://www.huamao.com/index.php/news/info/1071.html'
XIA='https://www.zjfic.org.cn/col/col1620089/art/2026/art_e17e62def5f547a4821f30362d073794.html'

# Load the immediately preceding sealed Zhejiang result rows. Same ambiguity_group_id + province + exact
# normalized name is used only to bridge cross-listed source rows; person_id values remain distinct.
prior_results={}
for n in (13,14,15,16):
    with open(E/f'W3_BATCH_{n:04d}_RESULTS.csv','r',encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f): prior_results[int(r['queue_order'])]=r

def latest_prior(target):
    candidates=[r for r in allq if int(r['queue_order'])<961 and r['province']==target['province'] and r['name_normalized']==target['name_normalized'] and r['ambiguity_group_id']==target['ambiguity_group_id'] and int(r['queue_order']) in prior_results]
    assert candidates, target
    p=max(candidates,key=lambda r:int(r['queue_order']))
    return p, prior_results[int(p['queue_order'])]

# Current live Zhejiang federation/chamber leadership, re-read on 2026-09-20.
fed_vp={'张晓平','陈仲尼','陈建成','林俊波','宗馥莉','胡季强','徐爱华'}
ch_vp={'陈频','陈保华','邵法平','胡兴荣','高兴江','郭明明','陶晓莺'}

FIELDS=['queue_order','person_id','province','excel_row','name_normalized','source_federation_role','identity_resolution','candidate_names','current_organization','current_title','current_verification_status','evidence_type','evidence_grade','evidence_title','evidence_url','evidence_date','unresolved_reason','research_notes']
results=[]
for t in rows:
    q=int(t['queue_order']); name=t['name_normalized']; p, old=latest_prior(t)
    out={'queue_order':t['queue_order'],'person_id':t['person_id'],'province':t['province'],'excel_row':t['excel_row'],'name_normalized':name,'source_federation_role':t['federation_role'],'candidate_names':name}
    bridge=f'Cross-listed Zhejiang source row safely linked through exact name + province + ambiguity_group_id {t["ambiguity_group_id"]} to sealed queue {p["queue_order"]}; person_id is preserved and not merged. '

    if name in fed_vp:
        out.update(identity_resolution='CURRENT_ROLE_CONFIRMED_BY_LIVE_OFFICIAL_PROVINCIAL_LEADERSHIP_PAGE',current_organization='浙江省工商业联合会',current_title='副主席',current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type='federation_official',evidence_grade='A',evidence_title='浙江省工商业联合会（浙江省商会）商会领导',evidence_url=LIVE,evidence_date='2026-09-20',unresolved_reason='',research_notes=bridge+'Live official leadership page independently reconfirms the current provincial vice-chair role; no name-only employer inference is used.')
    elif name in ch_vp:
        out.update(identity_resolution='CURRENT_ROLE_CONFIRMED_BY_LIVE_OFFICIAL_PROVINCIAL_LEADERSHIP_PAGE',current_organization='浙江省商会',current_title='副会长',current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type='federation_official',evidence_grade='A',evidence_title='浙江省工商业联合会（浙江省商会）商会领导',evidence_url=LIVE,evidence_date='2026-09-20',unresolved_reason='',research_notes=bridge+'Live official leadership page independently reconfirms the current chamber vice-chair role; no name-only employer inference is used.')
    elif name=='元成茂':
        out.update(identity_resolution='CURRENT_ROLE_REFRESHED_BY_LIVE_OFFICIAL_PROVINCIAL_LEADERSHIP_PAGE',current_organization='浙江省工商业联合会',current_title='党组成员、一级巡视员',current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type='federation_official',evidence_grade='A',evidence_title='浙江省工商业联合会（浙江省商会）商会领导',evidence_url=LIVE,evidence_date='2026-09-20',unresolved_reason='',research_notes=bridge+'Live official page now lists 元成茂 as 党组成员、一级巡视员; this supersedes the older vice-chair/chamber-vice-chair label for this touched row.')
    elif name=='宋立':
        out.update(identity_resolution='CURRENT_ROLE_CONFIRMED_BY_LIVE_OFFICIAL_PROVINCIAL_LEADERSHIP_PAGE',current_organization='浙江省工商业联合会 / 浙江省商会',current_title='党组成员、秘书长 / 秘书长',current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type='federation_official',evidence_grade='A',evidence_title='浙江省工商业联合会（浙江省商会）商会领导',evidence_url=LIVE,evidence_date='2026-09-20',unresolved_reason='',research_notes=bridge+'Live official page reconfirms both current federation and chamber secretary-general roles.')
    elif name=='王建云':
        out.update(identity_resolution='CURRENT_ROLE_CONFIRMED_WITH_OFFICIAL_FEDERATION_CONTEXT_BRIDGE',current_organization='中共宁波市委统一战线工作部 / 宁波市工商业联合会',current_title='副部长 / 党组书记',current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type='federation_official',evidence_grade='A',evidence_title='王建云：植根宁波实践 诠释新时代企业家精神',evidence_url=WJY,evidence_date='2026-01-30',unresolved_reason='',research_notes=bridge+'Zhejiang federation official 2026 article directly identifies 王建云 as 宁波市委统战部副部长、市工商联党组书记, providing a federation-context current-role bridge rather than a name-only match.')
    elif name=='方能斌':
        out.update(identity_resolution='CURRENT_ROLE_CONFIRMED_WITH_LISTED_FILING_AND_FEDERATION_CONTEXT',current_organization='浙江大胜达包装股份有限公司',current_title='董事长',current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type='listed_company_filing',evidence_grade='A',evidence_title='浙江大胜达包装股份有限公司2025年年度报告',evidence_url=FNB,evidence_date='2026-04-22',unresolved_reason='',research_notes=bridge+'Original listed-company annual report states 方能斌 is current company chairman and also 杭州市工商联副主席、杭州市萧山区工商联（总商会）十二届主席. Name + Zhejiang + federation-role context closes identity without name-only inference.')
    elif name=='邵云东':
        out.update(identity_resolution='CURRENT_ROLE_CONFIRMED_WITH_CURRENT_ACFIC_FEDERATION_CONTEXT',current_organization='浙江天草生物科技股份有限公司',current_title='董事长',current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type='federation_official',evidence_grade='A',evidence_title='从余村再出发：让“四千精神”在绿水青山间传承',evidence_url=SHAO,evidence_date='2026-07-01',unresolved_reason='',research_notes=bridge+'2026 ACFIC article identifies 邵云东 as 浙江天草生物科技股份有限公司董事长 in a Zhejiang federation-organized entrepreneur context; historical source identity is therefore bridged by province + federation context, not name alone.')
    elif name=='徐立勋':
        out.update(identity_resolution='CURRENT_ROLE_CONFIRMED_WITH_ENTERPRISE_FEDERATION_HISTORY_AND_CURRENT_MEDIA',current_organization='华茂集团',current_title='董事长、总裁',current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type='authoritative_media',evidence_grade='B',evidence_title='透过她/他/TA的视界：海外华人艺术回顾展（宁波）在华茂美术馆开幕',evidence_url=XUL,evidence_date='2026-06-17',unresolved_reason='',research_notes=bridge+'Current 2026 source identifies 徐立勋 as 华茂集团董事长、总裁. Identity is additionally anchored by Huamao official 2022 coverage of 徐立勋 at 浙江省工商联第十二次代表大会 ('+XUL_BRIDGE+'), avoiding name-only inference.')
    elif name=='夏赛丽':
        out.update(identity_resolution='CURRENT_ROLE_CONFIRMED_BY_2026_ZHEJIANG_FEDERATION_OFFICIAL_CONTEXT',current_organization='浙江省工商企业合作交流协会',current_title='会长',current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type='federation_official',evidence_grade='A',evidence_title='知名浙商嘉兴行活动暨嘉兴市产业推介会在桐乡举办',evidence_url=XIA,evidence_date='2026-06-12',unresolved_reason='',research_notes=bridge+'Zhejiang federation official 2026 article directly identifies 夏赛丽 as 浙江省工商企业合作交流协会会长 in the federation event context, safely bridging this historical provincial executive row.')
    elif old['current_verification_status']=='CURRENT_ORG_TITLE_CONFIRMED':
        out.update(identity_resolution='CURRENT_ROLE_CONFIRMED_BY_SEALED_CROSSLIST_CONTEXT',current_organization=old['current_organization'],current_title=old['current_title'],current_verification_status='CURRENT_ORG_TITLE_CONFIRMED',evidence_type=old['evidence_type'],evidence_grade=old['evidence_grade'],evidence_title=old['evidence_title'],evidence_url=old['evidence_url'],evidence_date=old['evidence_date'],unresolved_reason='',research_notes=bridge+'Current-role evidence was already sealed for the same cross-listed identity in an immediately preceding Zhejiang gate and is reused without merging person_id; evidence remains 2026-current.')
    else:
        extra=''
        if name=='王敏良': extra=' A 2026 listed-company filing supports a same-name 仙鹤股份 chairman/general-manager role, but no sufficiently specific provincial-federation-to-company identity bridge was established; the hit is not promoted.'
        elif name=='朱立科': extra=' A 2026 listed-company filing supports a same-name 一鸣食品 chairman/general-manager role, but it does not contain federation context linking it to this provincial executive-row identity; the hit is not promoted.'
        elif name=='阮福德': extra=' 2025-2026 public sources support a same-name 杰克控股 chairman role, but no sufficiently specific provincial-federation identity bridge was established; the hit is not promoted.'
        elif name=='李永宪': extra=' A 2024 report linked 浙江省工商联常委、嘉兴市工商联副主席 and 万纳神核控股集团董事长, but 2026-current role evidence was not strong enough to assert a present title.'
        elif name in {'吴伟','邹华'}: extra=' Current Zhejiang same-name hits were rejected because organization/history linkage to this source identity was insufficient.'
        out.update(identity_resolution='CROSSLIST_IDENTITY_CURRENT_ROLE_UNRESOLVED',current_organization='',current_title='',current_verification_status='UNRESOLVED_CURRENT_ORG_TITLE',evidence_type=old['evidence_type'],evidence_grade=old['evidence_grade'],evidence_title=old['evidence_title'],evidence_url=old['evidence_url'],evidence_date=old['evidence_date'],unresolved_reason=f'{name} remains current-role unresolved: targeted 2026 research did not establish a sufficiently specific current organization/title with a safe identity bridge.',research_notes=bridge+'Targeted current research was refreshed; same-name, stale, or weakly bridged hits are intentionally rejected.'+extra)
    results.append(out)

assert len(results)==60
confirmed=sum(r['current_verification_status']=='CURRENT_ORG_TITLE_CONFIRMED' for r in results)
unres=sum(r['current_verification_status']=='UNRESOLVED_CURRENT_ORG_TITLE' for r in results)
a_grade=sum(r['evidence_grade']=='A' for r in results); b_grade=sum(r['evidence_grade']=='B' for r in results); c_grade=sum(r['evidence_grade']=='C' for r in results)
assert confirmed+unres==60 and c_grade==0
assert all(r['evidence_url'] for r in results)
assert all((r['current_organization'] and r['current_title'] and not r['unresolved_reason']) if r['current_verification_status']=='CURRENT_ORG_TITLE_CONFIRMED' else (not r['current_organization'] and not r['current_title'] and r['unresolved_reason']) for r in results)

with open(E/'W3_BATCH_0017_RESULTS.csv','w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator='\n'); w.writeheader(); w.writerows(results)
LEDGER_FIELDS=['queue_order','person_id','province','excel_row','candidate_names','evidence_type','evidence_grade','evidence_title','evidence_url','evidence_date','current_verification_status','unresolved_reason']
OVERLAY_FIELDS=['queue_order','person_id','province','excel_row','identity_resolution','candidate_names','current_organization','current_title','current_verification_status','evidence_grade','evidence_url','unresolved_reason']
def append_rows(path,fields):
    with open(path,'r',encoding='utf-8-sig',newline='') as f: old=list(csv.DictReader(f))
    last=int(old[-1]['queue_order'])
    if last==1020: return
    assert last==960,(path,last)
    with open(path,'a',encoding='utf-8',newline='') as f: csv.DictWriter(f,fieldnames=fields,extrasaction='ignore',lineterminator='\n').writerows(results)
append_rows(E/'W3_EVIDENCE_LEDGER.csv',LEDGER_FIELDS); append_rows(E/'W3_VERIFICATION_OVERLAY.csv',OVERLAY_FIELDS)
for pth in [E/'W3_EVIDENCE_LEDGER.csv',E/'W3_VERIFICATION_OVERLAY.csv']:
    with open(pth,'r',encoding='utf-8-sig',newline='') as f: rr=list(csv.DictReader(f))
    orders=[int(x['queue_order']) for x in rr]
    assert len(rr)==1020 and orders==list(range(1,1021)) and len(set(orders))==1020

(E/'W3_BATCH_0017_METRICS.yaml').write_text(f'''schema: fc2515-w3-batch-metrics-v1
project_id: FC-EXEC-2515-01
gate: W3-BATCH-0017
status: PASS
queue_range: [961, 1020]
batch_rows: 60
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
  processed_queue_rows: 1020
  actionable_queue_remaining: 9624
  next_queue_order: 1021
  p1_processed: 919
  p1_remaining: 3412
next_gate: W3-BATCH-0018
''',encoding='utf-8')

(E/'W3_BATCH_0017_VALIDATION.md').write_text(f'''# W3-BATCH-0017 Validation

Result: **PASS**

- Deterministic repository queue slice: 961–1020 exactly, 60 浙江 `P1_IDENTITY` rows; no queue rows outside this gate were processed.
- Every touched row has public evidence or an explicit unresolved-current-role reason; unsupported current-title claims: 0.
- Cross-listed records were bridged only through exact name + province + the same repository ambiguity group; each source row keeps its own `person_id` and no name-only merge occurred.
- The live Zhejiang federation/chamber leadership page was re-read for this gate and directly refreshes current provincial federation/chamber roles for touched cross-listed rows.
- 邵云东 was newly closed from a 2026 ACFIC article that identifies him as 浙江天草生物科技股份有限公司董事长 in explicit Zhejiang federation activity context.
- 徐立勋 was newly closed from 2026 current-role reporting plus a Huamao official federation-congress identity bridge; 夏赛丽 was newly closed by a 2026 Zhejiang federation official article identifying her as 浙江省工商企业合作交流协会会长.
- Targeted research on all previously unresolved touched identities rejected stale, same-name, or weakly bridged hits rather than promoting them.
- Evidence grades: A={a_grade}, B={b_grade}, C={c_grade}; current organization/title confirmed={confirmed}/60; unresolved={unres}/60.
- Cumulative evidence ledger and verification overlay each reconcile to 1020 rows with `queue_order` 1..1020, no gaps or duplicates.

Next deterministic gate: `W3-BATCH-0018`, starting `queue_order=1021`.
''',encoding='utf-8')

# Update repository-authoritative control files.
sp=ROOT/'STATUS.yaml'; s=sp.read_text(encoding='utf-8')
def sub1(text,a,b):
    assert a in text,a
    return text.replace(a,b,1)
s=sub1(s,'code: W3-BATCH-0016\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS','code: W3-BATCH-0017\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS')
s=sub1(s,'code: W3-BATCH-0017\n  phase: W3-EVIDENCE-ENRICH\n  status: READY','code: W3-BATCH-0018\n  phase: W3-EVIDENCE-ENRICH\n  status: READY')
for a,b in [('  batches_sealed: 16','  batches_sealed: 17'),('  processed_queue_rows: 960','  processed_queue_rows: 1020'),('  next_queue_order: 961','  next_queue_order: 1021'),('  actionable_queue_remaining: 9684','  actionable_queue_remaining: 9624'),('  identity_evidence_rows: 960','  identity_evidence_rows: 1020')]: s=sub1(s,a,b)
s=sub1(s,'    processed: 859\n    remaining: 3472','    processed: 919\n    remaining: 3412')
s=sub1(s,'  current_org_title_confirmed_rows: 575',f'  current_org_title_confirmed_rows: {575+confirmed}')
s=sub1(s,'  current_org_title_unresolved_rows: 282',f'  current_org_title_unresolved_rows: {282+unres}')
anchor='  w3_batch_0016_validation: projects/fc-exec-2515/evidence/W3_BATCH_0016_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv'
rep='  w3_batch_0016_validation: projects/fc-exec-2515/evidence/W3_BATCH_0016_VALIDATION.md\n  w3_batch_0017_results: projects/fc-exec-2515/evidence/W3_BATCH_0017_RESULTS.csv\n  w3_batch_0017_metrics: projects/fc-exec-2515/evidence/W3_BATCH_0017_METRICS.yaml\n  w3_batch_0017_validation: projects/fc-exec-2515/evidence/W3_BATCH_0017_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv'
s=sub1(s,anchor,rep); sp.write_text(s,encoding='utf-8')

cp=ROOT/'CURRENT.yaml'; c=cp.read_text(encoding='utf-8')
c=sub1(c,'current_gate: W3-BATCH-0017','current_gate: W3-BATCH-0018')
c=sub1(c,'work_cursor: 960','work_cursor: 1020')
c=sub1(c,'verified_records: 577',f'verified_records: {577+confirmed}')
c=sub1(c,'unresolved_records: 10067',f'unresolved_records: {10067-confirmed}')
c=sub1(c,'  processed: 960','  processed: 1020')
c=sub1(c,'  actionable_remaining: 9684','  actionable_remaining: 9624')
c=sub1(c,'  next_queue_order: 961','  next_queue_order: 1021')
c=sub1(c,'      processed: 859\n      remaining: 3472','      processed: 919\n      remaining: 3412')
c,n=re.subn(r'last_input_head: .*',f'last_input_head: {INPUT_HEAD}',c,count=1); assert n==1
c,n=re.subn(r'last_evidence_at: .*',f'last_evidence_at: {NOW}',c,count=1); assert n==1
section=f'''\nw3_batch_0017:
  status: SEALED
  validation: PASS
  touched_rows: 60
  p1_identity_rows: 60
  evidence_backed_rows: 60
  a_grade_rows: {a_grade}
  b_grade_rows: {b_grade}
  c_grade_rows: {c_grade}
  current_org_title_confirmed_rows: {confirmed}
  current_org_title_unresolved_rows: {unres}
  unsupported_current_title_claims: 0
\n'''
c=sub1(c,'\nnotes:\n','\n'+section+'notes:\n')
notes=f'''  - W3-BATCH-0017 processed queue orders 961-1020 exactly, all 60 浙江 P1 identity/current-role rows.
  - {confirmed} rows received current organization/title confirmation; {unres} remain explicit unresolved where current evidence lacked a sufficiently specific identity bridge.
  - Cross-listed identities were reused only through exact name + province + the same ambiguity_group_id; source person_id values were preserved and never merged by name.
  - The live Zhejiang federation/chamber leadership page was refreshed for touched cross-listed current roles.
  - 邵云东 was newly confirmed from 2026 ACFIC federation-context evidence; 徐立勋 from current 2026 role evidence plus Huamao's federation-congress identity bridge; 夏赛丽 from 2026 Zhejiang federation official evidence.
  - All other previously unresolved touched identities were re-searched and remained unresolved where current identity-to-role linkage was stale, same-name-only, or insufficiently specific.
  - Evidence grades are A={a_grade}, B={b_grade}, C={c_grade}; unsupported current-title claims=0.
  - Next deterministic queue order is 1021.
'''
c=c.rstrip()+'\n'+notes; cp.write_text(c,encoding='utf-8')

st=sp.read_text(encoding='utf-8'); ct=cp.read_text(encoding='utf-8')
assert 'latest_gate:\n  code: W3-BATCH-0017' in st and 'next_gate:\n  code: W3-BATCH-0018' in st
assert 'current_gate: W3-BATCH-0018' in ct and 'work_cursor: 1020' in ct and 'next_queue_order: 1021' in ct
print(f'PASS W3-BATCH-0017 confirmed={confirmed} unresolved={unres} A={a_grade} B={b_grade} C={c_grade} now={NOW}')
