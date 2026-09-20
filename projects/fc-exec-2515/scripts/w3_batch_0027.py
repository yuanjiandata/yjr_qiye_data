#!/usr/bin/env python3
import csv, gzip, glob, subprocess, re
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
P = ROOT / 'projects' / 'fc-exec-2515'
E = P / 'evidence'
INPUT_HEAD = '3d6bb8f7bd4e2504f2a4a941e39b9651c3b8bf88'
BATCH_START, BATCH_END = 1561, 1620
NOW = datetime.now(timezone(timedelta(hours=8))).replace(microsecond=0).isoformat()
FJ_HIST = 'https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_fj/202208/t20220830_312930.html'

head = subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip()
assert head == INPUT_HEAD, (head, INPUT_HEAD)
with gzip.open(E/'W2_UNRESOLVED_QUEUE.csv.gz','rt',encoding='utf-8-sig',newline='') as f:
    allq=list(csv.DictReader(f))
rows=allq[BATCH_START-1:BATCH_END]
assert len(rows)==60 and [int(r['queue_order']) for r in rows]==list(range(BATCH_START,BATCH_END+1))
assert {r['priority'] for r in rows}=={'P1_IDENTITY'}
assert Counter(r['province'] for r in rows)==Counter({'福建':60})

with gzip.open(E/'W2_MASTER_ROSTER.csv.gz','rt',encoding='utf-8-sig',newline='') as f:
    master={r['person_id']:r for r in csv.DictReader(f)}
by_order={}
for fn in sorted(glob.glob(str(E/'W3_BATCH_*_RESULTS.csv'))):
    with open(fn,'r',encoding='utf-8-sig',newline='') as f:
        for x in csv.DictReader(f):
            if int(x['queue_order'])<BATCH_START: by_order[int(x['queue_order'])]=x
by_ag=defaultdict(list)
for q in allq: by_ag[q['ambiguity_group_id']].append(q)
research={}
with (E/'W3_BATCH_0027_RESEARCH.tsv').open('r',encoding='utf-8-sig',newline='') as f:
    for x in csv.DictReader(f,delimiter='\t'): research[x['queue_order']]=x

fresh=[]
for r in rows:
    qual=master[r['person_id']]['annotation_other']
    priors=[x for x in by_ag[r['ambiguity_group_id']] if int(x['queue_order'])<BATCH_START and int(x['queue_order']) in by_order and x['province']==r['province'] and x['name_normalized']==r['name_normalized'] and master[x['person_id']]['annotation_other']==qual]
    if not priors: fresh.append(r['queue_order'])
assert fresh==['1574','1575'], fresh
assert set(research)==set(fresh)

fields=['queue_order','person_id','province','excel_row','name_normalized','source_federation_role','identity_resolution','candidate_names','current_organization','current_title','current_verification_status','evidence_type','evidence_grade','evidence_title','evidence_url','evidence_date','unresolved_reason','research_notes']
results=[]
for r in rows:
    name=r['name_normalized']; qo=r['queue_order']; qual=master[r['person_id']]['annotation_other']
    base={'queue_order':qo,'person_id':r['person_id'],'province':r['province'],'excel_row':r['excel_row'],'name_normalized':name,'source_federation_role':r['federation_role'],'candidate_names':name}
    priors=[x for x in by_ag[r['ambiguity_group_id']] if int(x['queue_order'])<BATCH_START and int(x['queue_order']) in by_order and x['province']==r['province'] and x['name_normalized']==name and master[x['person_id']]['annotation_other']==qual]
    if priors:
        p=max(priors,key=lambda x:int(x['queue_order'])); prev=by_order[int(p['queue_order'])]
        result={**base,'identity_resolution':'REUSED_SEALED_EVIDENCE_SAME_REPOSITORY_AMBIGUITY_GROUP_AND_REGION','current_organization':prev['current_organization'],'current_title':prev['current_title'],'current_verification_status':prev['current_verification_status'],'evidence_type':prev['evidence_type'],'evidence_grade':prev['evidence_grade'],'evidence_title':prev['evidence_title'],'evidence_url':prev['evidence_url'],'evidence_date':prev['evidence_date'],'unresolved_reason':prev['unresolved_reason'],'research_notes':f"与已封存 queue {p['queue_order']} 同省、同名、同 ambiguity_group_id={r['ambiguity_group_id']} 且 region_qualifier={qual or '<blank>'} 一致；复用证据但保留独立 person_id。"+prev['research_notes']}
    else:
        s=research[qo]
        assert s['person_id']==r['person_id'] and s['name_normalized']==name and s['region_qualifier']==qual
        if s['decision']=='CONFIRMED':
            result={**base,'identity_resolution':'CURRENT_ROLE_CONFIRMED_WITH_REGION_AND_CONTEXTUAL_IDENTITY_BRIDGE','current_organization':s['org'],'current_title':s['title'],'current_verification_status':'CURRENT_ORG_TITLE_CONFIRMED','evidence_type':s['etype'],'evidence_grade':s['grade'],'evidence_title':s['etitle'],'evidence_url':s['url'],'evidence_date':s['date'],'unresolved_reason':'','research_notes':s['notes']+' supporting_url='+s['supporting_url']+' 历史省工商联身份锚点：'+FJ_HIST}
        else:
            result={**base,'identity_resolution':'REGION_QUALIFIED_IDENTITY_CURRENT_ROLE_UNRESOLVED','current_organization':'','current_title':'','current_verification_status':'UNRESOLVED_CURRENT_ORG_TITLE','evidence_type':s['etype'],'evidence_grade':s['grade'],'evidence_title':s['etitle'],'evidence_url':s['url'],'evidence_date':s['date'],'unresolved_reason':s['reason'],'research_notes':s['notes']+' candidate_or_supporting_url='+s['supporting_url']}
        assert s['decision'] in {'CONFIRMED','UNRESOLVED'}
    results.append(result)

out=E/'W3_BATCH_0027_RESULTS.csv'
with out.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n'); w.writeheader(); w.writerows(results)
ledger_path=E/'W3_EVIDENCE_LEDGER.csv'
with ledger_path.open('r',encoding='utf-8-sig',newline='') as f:
    old_ledger=list(csv.DictReader(f)); ledger_fields=list(old_ledger[0].keys())
assert len(old_ledger)==1560
with ledger_path.open('a',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=ledger_fields,lineterminator='\n')
    for x in results:
        d={'queue_order':x['queue_order'],'person_id':x['person_id'],'province':x['province'],'excel_row':x['excel_row'],'candidate_names':x['candidate_names'],'evidence_type':x['evidence_type'],'evidence_grade':x['evidence_grade'],'evidence_title':x['evidence_title'],'evidence_url':x['evidence_url'],'evidence_date':x['evidence_date'],'current_verification_status':x['current_verification_status'],'unresolved_reason':x['unresolved_reason']}; w.writerow({k:d.get(k,'') for k in ledger_fields})
overlay_path=E/'W3_VERIFICATION_OVERLAY.csv'
with overlay_path.open('r',encoding='utf-8-sig',newline='') as f:
    old_overlay=list(csv.DictReader(f)); overlay_fields=list(old_overlay[0].keys())
assert len(old_overlay)==1560
with overlay_path.open('a',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=overlay_fields,lineterminator='\n')
    for x in results:
        d={'queue_order':x['queue_order'],'person_id':x['person_id'],'province':x['province'],'excel_row':x['excel_row'],'identity_resolution':x['identity_resolution'],'candidate_names':x['candidate_names'],'current_organization':x['current_organization'],'current_title':x['current_title'],'current_verification_status':x['current_verification_status'],'evidence_grade':x['evidence_grade'],'evidence_url':x['evidence_url'],'unresolved_reason':x['unresolved_reason']}; w.writerow({k:d.get(k,'') for k in overlay_fields})

statuses=Counter(x['current_verification_status'] for x in results); grades=Counter(x['evidence_grade'] for x in results)
confirmed=statuses['CURRENT_ORG_TITLE_CONFIRMED']; unresolved=statuses['UNRESOLVED_CURRENT_ORG_TITLE']; no_role=statuses['NO_CURRENT_ROLE_CONFIRMED']
assert confirmed+unresolved+no_role==60
assert all(x['evidence_url'] or x['unresolved_reason'] for x in results)
assert all(not (x['current_verification_status']=='CURRENT_ORG_TITLE_CONFIRMED' and (not x['current_organization'] or not x['current_title'] or not x['evidence_url'])) for x in results)
assert all(not (x['current_verification_status']=='UNRESOLVED_CURRENT_ORG_TITLE' and (x['current_organization'] or x['current_title'] or not x['unresolved_reason'])) for x in results)
for path in [ledger_path,overlay_path]:
    with path.open('r',encoding='utf-8-sig',newline='') as f: z=list(csv.DictReader(f))
    assert len(z)==1620 and [int(x['queue_order']) for x in z]==list(range(1,1621)) and len({x['queue_order'] for x in z})==1620

metrics=f'''schema: fc-exec-2515-w3-batch-metrics-v1\nproject_id: FC-EXEC-2515-01\ngate: W3-BATCH-0027\nstatus: SEALED\nvalidation: PASS\ntouched_rows: 60\nfujian_rows: 60\np1_identity_rows: 60\nevidence_backed_rows: 60\na_grade_rows: {grades['A']}\nb_grade_rows: {grades['B']}\nc_grade_rows: {grades['C']}\ncurrent_org_title_confirmed_rows: {confirmed}\nno_current_role_confirmed_rows: {no_role}\ncurrent_org_title_unresolved_rows: {unresolved}\nunsupported_current_title_claims: 0\nqueue_start: 1561\nqueue_end: 1620\nnext_queue_order: 1621\nverified_at: {NOW}\ninput_head: {INPUT_HEAD}\n'''
(E/'W3_BATCH_0027_METRICS.yaml').write_text(metrics,encoding='utf-8')
validation=f'''# W3-BATCH-0027 Validation\n\n- Gate: `W3-BATCH-0027`\n- Queue orders: `1561-1620`\n- Touched rows: **60** (`福建 60`)\n- Priority: `P1_IDENTITY` 60\n- Evidence coverage: **60/60**\n- Evidence grades: **A={grades['A']}, B={grades['B']}, C={grades['C']}**\n- Current organization + title confirmed: **{confirmed}**\n- No-current-role confirmed: **{no_role}**\n- Explicit current-role unresolved: **{unresolved}**\n- Unsupported current-title claims: **0**\n- Cumulative evidence ledger: **1620 rows**, queue `1-1620` contiguous, no duplicate queue order\n- Cumulative verification overlay: **1620 rows**, queue `1-1620` contiguous, no duplicate queue order\n\n## Identity / recency controls\n\n- 58 cross-listed 福建 rows reused sealed evidence only after exact repository `ambiguity_group_id + province + normalized name + region qualifier` match; every source row retains an independent `person_id`.\n- The only two fresh rows are distinct source records both named 林锦云 but explicitly qualified by the official federation roster and repository source as `干部` and `企业家`; they were researched separately and never merged by name.\n- `林锦云(企业家)` safely closes to **福建闽宁情商贸有限公司董事长**: 2026-07-18 福州市政府 material states the company/title and continuous 闽宁创业履历, and 2026-06-20 福建省政府 independently corroborates the same company/title.\n- `林锦云(干部)` remains unresolved: the official federation roster proves this is a separate source identity, while current authority searches did not produce a safe current cadre identity bridge.\n\n**PASS**\n'''
(E/'W3_BATCH_0027_VALIDATION.md').write_text(validation,encoding='utf-8')

sp=P/'STATUS.yaml'; s=sp.read_text(encoding='utf-8')
repls={
'code: W3-BATCH-0026\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED':'code: W3-BATCH-0027\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED',
'code: W3-BATCH-0027\n  phase: W3-EVIDENCE-ENRICH\n  status: READY':'code: W3-BATCH-0028\n  phase: W3-EVIDENCE-ENRICH\n  status: READY',
'batches_sealed: 26':'batches_sealed: 27','processed_queue_rows: 1560':'processed_queue_rows: 1620','next_queue_order: 1561':'next_queue_order: 1621','actionable_queue_remaining: 9084':'actionable_queue_remaining: 9024','processed: 1459':'processed: 1519','remaining: 2872':'remaining: 2812','identity_evidence_rows: 1560':'identity_evidence_rows: 1620','current_org_title_confirmed_rows: 862':f'current_org_title_confirmed_rows: {862+confirmed}','current_org_title_unresolved_rows: 595':f'current_org_title_unresolved_rows: {595+unresolved}','no_current_role_confirmed_rows: 2':f'no_current_role_confirmed_rows: {2+no_role}'}
for a,b in repls.items(): assert a in s,a; s=s.replace(a,b,1)
anchor='  w3_batch_0026_validation: projects/fc-exec-2515/evidence/W3_BATCH_0026_VALIDATION.md\n'; assert anchor in s
s=s.replace(anchor,anchor+'  w3_batch_0027_research: projects/fc-exec-2515/evidence/W3_BATCH_0027_RESEARCH.tsv\n  w3_batch_0027_results: projects/fc-exec-2515/evidence/W3_BATCH_0027_RESULTS.csv\n  w3_batch_0027_metrics: projects/fc-exec-2515/evidence/W3_BATCH_0027_METRICS.yaml\n  w3_batch_0027_validation: projects/fc-exec-2515/evidence/W3_BATCH_0027_VALIDATION.md\n',1); sp.write_text(s,encoding='utf-8')

cp=P/'CURRENT.yaml'; c=cp.read_text(encoding='utf-8'); verified_add=confirmed+no_role
repls={'current_gate: W3-BATCH-0027':'current_gate: W3-BATCH-0028','work_cursor: 1560':'work_cursor: 1620','verified_records: 864':f'verified_records: {864+verified_add}','unresolved_records: 9780':f'unresolved_records: {9780-verified_add}','processed: 1560':'processed: 1620','actionable_remaining: 9084':'actionable_remaining: 9024','next_queue_order: 1561':'next_queue_order: 1621','processed: 1459':'processed: 1519','remaining: 2872':'remaining: 2812','last_input_head: f8d4d5ee6f7509d1f5e9b6522f774e5e97ea119e':f'last_input_head: {INPUT_HEAD}'}
for a,b in repls.items(): assert a in c,a; c=c.replace(a,b,1)
c=re.sub(r'last_evidence_at: .*',f'last_evidence_at: {NOW}',c,count=1)
block=f'''\nw3_batch_0027:\n  status: SEALED\n  validation: PASS\n  touched_rows: 60\n  fujian_rows: 60\n  p1_identity_rows: 60\n  evidence_backed_rows: 60\n  a_grade_rows: {grades['A']}\n  b_grade_rows: {grades['B']}\n  c_grade_rows: {grades['C']}\n  current_org_title_confirmed_rows: {confirmed}\n  no_current_role_confirmed_rows: {no_role}\n  current_org_title_unresolved_rows: {unresolved}\n  unsupported_current_title_claims: 0\n\n'''; assert 'notes:\n' in c; c=c.replace('notes:\n',block+'notes:\n',1)
c=c.rstrip()+f'''\n  - W3-BATCH-0027 processed queue orders 1561-1620 exactly, all 60 福建 P1 identity/current-role rows.\n  - {confirmed} rows received current organization/title confirmation; {unresolved} remain explicit unresolved; {no_role} have no-current-role confirmation; unsupported current-title claims remain zero.\n  - 58 rows reused prior sealed evidence only through exact repository ambiguity_group_id + province + normalized name + region qualifier match; independent person_id values are retained.\n  - The two fresh same-name records 林锦云(干部) and 林锦云(企业家) were researched separately. 林锦云(企业家) safely closes to 福建闽宁情商贸有限公司董事长 via 2026 福州市政府 current evidence plus 福建省政府 corroboration; 林锦云(干部) remains unresolved because the official roster marks it as a distinct source identity and no safe current cadre bridge was found.\n  - Evidence grades are A={grades['A']}, B={grades['B']}, C={grades['C']}; next deterministic queue order is 1621.\n'''; cp.write_text(c,encoding='utf-8')
print('PASS W3-BATCH-0027',dict(statuses),dict(grades),'fresh',fresh,'next=1621')
