import csv, gzip
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / 'evidence'
INPUT_HEAD = '5a510ef785118199b42b0b0444fb16f1481db647'
NOW = datetime.now(timezone(timedelta(hours=8))).replace(microsecond=0).isoformat()

with gzip.open(E/'W2_UNRESOLVED_QUEUE.csv.gz','rt',encoding='utf-8-sig',newline='') as f:
    queue=list(csv.DictReader(f))[180:240]
assert [int(r['queue_order']) for r in queue] == list(range(181,241))
assert all(r['priority']=='P1_IDENTITY' for r in queue)
assert all(r['province']=='河北' for r in queue)

HE=('federation_official','A','河北省工商业联合会(总商会)第十三届执委会名单',
    'https://www.acfic.org.cn/ztzlhz/2022gslhj/2022gslhj_he/202207/t20220715_312762.html','2022-07-15')

# q: resolution, evidence_type, grade, title, url, date, org, role, note
C={
183:('CURRENT_PUBLIC_ROLE_IDENTIFIED','authoritative_media','B','邢台市工商联赴深穗开展考察交流','https://www.hebjjrb.cn/system/2026/03/29/102166537.shtml','2026-03-30','中国人民政治协商会议河北省邢台市委员会','副主席','Fresh 2026 report identifies 王建江 as 邢台市政协副主席 and separately names 张鹏 as the current city federation chair; this avoids carrying forward the pre-election federation title.'),
189:('CURRENT_ENTERPRISE_ROLE_IDENTIFIED','authoritative_media','B','全国“两优一先”风采录丨“航天铸镜人”卢勇：匠心攻坚，守护航天安全','https://cpc.people.com.cn/n1/2026/0709/c462314-40756868.html','2026-07-09','秦皇岛星箭特种玻璃有限公司','党支部书记、董事长','Xinhua/People report gives a fresh enterprise role for 卢勇; Hebei federation roster supplies the provincial federation identity context.'),
197:('CURRENT_ENTERPRISE_ROLE_IDENTIFIED','federation_official','A','执委名单','https://www.acfic.org.cn/lqfw/zzjs/zwdwjs/202506/t20250617_309772.html','2025-06-17','河北千喜鹤饮食股份有限公司','董事长','ACFIC national executive roster directly lists 刘延云 with the company and chairman role, providing federation-context identity and employment in one A-grade source.'),
206:('CURRENT_PUBLIC_ROLE_IDENTIFIED','authoritative_media','B','河北省“数字工商联”推进会在石家庄裕华区举行','https://www.sohu.com/a/1027817999_121196328','2026-05-26','河北省工商业联合会','党组成员、秘书长','2026 event coverage explicitly identifies 河北省工商联党组成员、秘书长李明辉; federation context prevents a name-only match.'),
209:('CURRENT_ENTERPRISE_ROLE_IDENTIFIED','federation_official','A','思想引领凝聚“向心力”，精准服务提升“获得感”——河北省工商联十三届四次执委会议为迈向“十五五”新征程擘画蓝图','https://www.acfic.org.cn/gdgslgz/hb/bjgslgz/202512/t20251209_323112.html','2025-12-09','河北华密新材科技股份有限公司','董事长','ACFIC explicitly identifies 河北省工商联常委李藏稳 as company chairman in the current provincial-federation context.'),
223:('CURRENT_ASSOCIATION_ROLE_IDENTIFIED','authoritative_media','B','2025第十届中国能源终端站发展大会圆满落幕——金联创推出加油站智慧大脑服务','https://jyz.315i.com/news/4573.html','2025-04-23','河北省石油业商会','会长','Industry-event coverage explicitly identifies 陈金端 as 河北省石油业商会会长; Hebei federation roster anchors the source identity.'),
226:('CURRENT_ENTERPRISE_ROLE_IDENTIFIED','authoritative_media','B','河北金融与民间资本商会 多位企业家积极参会履职共献发展良策','https://www.hebjjrb.cn/system/2026/01/29/102149295.shtml','2026-01-30','河北源达信息技术股份有限公司','董事长','2026 Hebei Economic Daily coverage identifies 郝旭 as both chamber president and company chairman, giving strong regional identity context.'),
230:('CURRENT_PUBLIC_ROLE_IDENTIFIED','government_official','A','北京外交人员综合服务有限公司考察团来衡考察洽谈','https://www.hebeiql.org.cn/system/2026/04/03/030379954.shtml','2026-04-03','中共衡水市委统一战线工作部 / 衡水市工商业联合会','副部长 / 党组书记','Hebei provincial federation of returned overseas Chinese official page identifies 姜丙刚 with both current United Front and federation roles.'),
233:('CURRENT_ENTERPRISE_ROLE_IDENTIFIED','federation_official','A','思想引领凝聚“向心力”，精准服务提升“获得感”——河北省工商联十三届四次执委会议为迈向“十五五”新征程擘画蓝图','https://www.acfic.org.cn/gdgslgz/hb/bjgslgz/202512/t20251209_323112.html','2025-12-09','邯郸盛卓集团','董事长','ACFIC explicitly identifies 河北省工商联常委葛超众 as 邯郸盛卓集团董事长.'),
234:('CURRENT_PUBLIC_ROLE_IDENTIFIED','government_official','A','中共承德市委举行民主协商会','https://www.chengde.gov.cn/art/2026/2/5/art_360_1103368.html','2026-02-05','承德市工商业联合会','主席','Chengde government official page names 市工商联主席董旭明 in a 2026 municipal consultation meeting.'),
235:('CURRENT_ENTERPRISE_ROLE_IDENTIFIED','federation_official','A','思想引领凝聚“向心力”，精准服务提升“获得感”——河北省工商联十三届四次执委会议为迈向“十五五”新征程擘画蓝图','https://www.acfic.org.cn/gdgslgz/hb/bjgslgz/202512/t20251209_323112.html','2025-12-09','河北锦宝石循环资源开发集团','董事长','ACFIC provincial executive meeting coverage directly identifies 董香文 as group chairman.'),
237:('CURRENT_ENTERPRISE_ROLE_IDENTIFIED','authoritative_media','B','港华能源与晶澳达成战略合作，携手共筑光储智新标杆','https://finance.sina.com.cn/stock/relnews/cn/2026-06-04/doc-iniahhrm2359257.shtml','2026-06-04','晶澳太阳能科技股份有限公司','董事、储能事业部董事长','Fresh 2026 company-sourced report identifies 靳军辉 as JA Solar director and storage business chairman; roster and prior federation context disambiguate the person.'),
238:('CURRENT_PUBLIC_ROLE_IDENTIFIED','authoritative_media','B','唐山市政协十三届六次会议第二次全体会议发言摘登','https://tangshan.huanbohainews.com.cn/2026-02/08/content_50502159.html','2026-02-08','唐山市工商业联合会','主席','Tangshan Daily coverage explicitly identifies 市政协副主席、市工商联主席甄德恩 in 2026.'),
239:('CURRENT_ENTERPRISE_ROLE_IDENTIFIED','authoritative_media','B','立中集团：关于聘任公司终身名誉董事长、终身名誉董事的公告','https://www.cfi.net.cn/p20260703002817.html','2026-07-03','立中四通轻合金集团股份有限公司','终身名誉董事','Published board-resolution text records the July 2026 appointment of founder 臧立国 as lifetime honorary director; Hebei roster provides federation identity context.'),
}

FIELDS=['queue_order','person_id','province','excel_row','source_fragment','federation_role','identity_resolution','candidate_names','repair_notes','evidence_type','evidence_grade','evidence_title','evidence_url','evidence_date','current_organization','current_title','current_verification_status','unresolved_reason']
results=[]
for r in queue:
    q=int(r['queue_order']); name=r['name_normalized']
    out={'queue_order':str(q),'person_id':r['person_id'],'province':r['province'],'excel_row':r['excel_row'],'source_fragment':name,'federation_role':r['federation_role'],'candidate_names':name,'current_organization':'','current_title':'','unresolved_reason':''}
    if q in C:
        res,typ,grade,etitle,url,edate,org,title,note=C[q]
        out.update(identity_resolution=res,repair_notes=note,evidence_type=typ,evidence_grade=grade,evidence_title=etitle,evidence_url=url,evidence_date=edate,current_organization=org,current_title=title,current_verification_status='CURRENT_ORG_TITLE_CONFIRMED')
    else:
        typ,grade,etitle,url,edate=HE
        out.update(identity_resolution='IDENTITY_ONLY_OFFICIAL_ROSTER',repair_notes='Identity retained from official Hebei federation roster; current organization/title intentionally left unresolved.',evidence_type=typ,evidence_grade=grade,evidence_title=etitle,evidence_url=url,evidence_date=edate,current_verification_status='UNRESOLVED_CURRENT_ORG_TITLE',unresolved_reason='Official Hebei federation roster confirms this source identity/role, but this batch did not find sufficiently current and specific public evidence to assign a current organization/title without risking a name-only match.')
    results.append(out)

with open(E/'W3_BATCH_0004_RESULTS.csv','w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator='\n'); w.writeheader(); w.writerows(results)

LEDGER_FIELDS=['queue_order','person_id','province','excel_row','candidate_names','evidence_type','evidence_grade','evidence_title','evidence_url','evidence_date','current_verification_status','unresolved_reason']
OVERLAY_FIELDS=['queue_order','person_id','province','excel_row','identity_resolution','candidate_names','current_organization','current_title','current_verification_status','evidence_grade','evidence_url','unresolved_reason']

def append_rows(path, fields, rows):
    with open(path,'r',encoding='utf-8-sig',newline='') as f: old=list(csv.DictReader(f))
    last=int(old[-1]['queue_order'])
    if last==240: return
    assert last==180, (path,last)
    with open(path,'a',encoding='utf-8',newline='') as f:
        csv.DictWriter(f,fieldnames=fields,extrasaction='ignore',lineterminator='\n').writerows(rows)

append_rows(E/'W3_EVIDENCE_LEDGER.csv',LEDGER_FIELDS,results)
append_rows(E/'W3_VERIFICATION_OVERLAY.csv',OVERLAY_FIELDS,results)

confirmed=sum(r['current_verification_status']=='CURRENT_ORG_TITLE_CONFIRMED' for r in results)
unresolved=60-confirmed
a_count=sum(r['evidence_grade']=='A' for r in results)
b_count=sum(r['evidence_grade']=='B' for r in results)
assert confirmed==14 and unresolved==46
assert a_count==52 and b_count==8
assert all(r['evidence_url'] and r['evidence_title'] for r in results)
assert all((r['current_organization'] and r['current_title']) if r['current_verification_status']=='CURRENT_ORG_TITLE_CONFIRMED' else bool(r['unresolved_reason']) for r in results)
with open(E/'W3_EVIDENCE_LEDGER.csv','r',encoding='utf-8-sig',newline='') as f: led=list(csv.DictReader(f))
assert len(led)==240 and [int(x['queue_order']) for x in led]==list(range(1,241))

(E/'W3_BATCH_0004_METRICS.yaml').write_text(f'''schema: fc2515-w3-batch-metrics-v1
project_id: FC-EXEC-2515-01
gate: W3-BATCH-0004
status: PASS
queue_range: [181, 240]
batch_rows: 60
p1_identity_rows: 60
evidence_backed_rows: 60
a_grade_rows: {a_count}
b_grade_rows: {b_count}
structural_deferred_rows: 0
current_org_title_confirmed_rows: {confirmed}
current_org_title_unresolved_rows: {unresolved}
unsupported_current_title_claims: 0
post_batch:
  processed_queue_rows: 240
  actionable_queue_remaining: 10404
  next_queue_order: 241
  p0_processed: 101
  p0_remaining: 0
  p1_processed: 139
  p1_remaining: 4192
next_gate: W3-BATCH-0005
''',encoding='utf-8')

(E/'W3_BATCH_0004_VALIDATION.md').write_text(f'''# W3-BATCH-0004 Validation

Result: **PASS**

- Deterministic queue slice: 181–240 exactly, 60 rows, all P1_IDENTITY / 河北.
- Every touched row has public evidence or an explicit unresolved-current-role reason.
- Official Hebei ACFIC roster remains the identity anchor; external employment/public-role evidence is only assigned where province/federation/person context closes identity.
- Evidence grades in batch: A={a_count}, B={b_count}; C=0.
- Current organization + title confirmed: {confirmed}/60.
- Current-role unresolved: {unresolved}/60; unresolved organization/title fields remain blank rather than guessed.
- 王建江 was not left on his 2025 federation-chair title: 2026 evidence shows 张鹏 as current 邢台市工商联主席 and 王建江 as 邢台市政协副主席.
- Fresh 2026 evidence confirms current roles for 卢勇、郝旭、姜丙刚、董旭明、靳军辉、甄德恩、臧立国; official federation evidence confirms 刘延云、李藏稳、葛超众、董香文.
- High-frequency/common-name rows without a safe cross-source identity link remain unresolved rather than name-matched.
- Cumulative W3 evidence ledger reconciles to 240 rows with queue_order 1..240 and no gaps.
- Unsupported current-title claims: 0.

Next deterministic gate: `W3-BATCH-0005`, starting queue_order 241.
''',encoding='utf-8')

sp=ROOT/'STATUS.yaml'; s=sp.read_text(encoding='utf-8')
s=s.replace('code: W3-BATCH-0003\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS','code: W3-BATCH-0004\n  phase: W3-EVIDENCE-ENRICH\n  status: SEALED\n  validation: PASS',1)
s=s.replace('code: W3-BATCH-0004\n  phase: W3-EVIDENCE-ENRICH\n  status: READY','code: W3-BATCH-0005\n  phase: W3-EVIDENCE-ENRICH\n  status: READY',1)
for a,b in {
'  batches_sealed: 3':'  batches_sealed: 4','  processed_queue_rows: 180':'  processed_queue_rows: 240','  next_queue_order: 181':'  next_queue_order: 241','  actionable_queue_remaining: 10464':'  actionable_queue_remaining: 10404','    processed: 79\n    remaining: 4252':'    processed: 139\n    remaining: 4192','  identity_evidence_rows: 180':'  identity_evidence_rows: 240','  current_org_title_confirmed_rows: 31':'  current_org_title_confirmed_rows: 45','  current_org_title_unresolved_rows: 48':'  current_org_title_unresolved_rows: 94'}.items():
    assert a in s,a; s=s.replace(a,b,1)
anchor='  w3_batch_0003_validation: projects/fc-exec-2515/evidence/W3_BATCH_0003_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv'
rep='  w3_batch_0003_validation: projects/fc-exec-2515/evidence/W3_BATCH_0003_VALIDATION.md\n  w3_batch_0004_results: projects/fc-exec-2515/evidence/W3_BATCH_0004_RESULTS.csv\n  w3_batch_0004_metrics: projects/fc-exec-2515/evidence/W3_BATCH_0004_METRICS.yaml\n  w3_batch_0004_validation: projects/fc-exec-2515/evidence/W3_BATCH_0004_VALIDATION.md\n  w3_verification_overlay: projects/fc-exec-2515/evidence/W3_VERIFICATION_OVERLAY.csv'
assert anchor in s; s=s.replace(anchor,rep,1); sp.write_text(s,encoding='utf-8')

cp=ROOT/'CURRENT.yaml'; c=cp.read_text(encoding='utf-8')
c=c.replace('current_gate: W3-BATCH-0004','current_gate: W3-BATCH-0005',1).replace('work_cursor: 180','work_cursor: 240',1)
for a,b in {
'verified_records: 31':'verified_records: 45','unresolved_records: 10613':'unresolved_records: 10599',"last_evidence_at: '2026-09-20T01:56:34+08:00'":f"last_evidence_at: '{NOW}'",'last_input_head: 97aa202d82f440965882b59490cdaa87337e7c094':'last_input_head: 97aa202d82f440965882b59490cdaa87337e7c094',
'last_input_head: 97aa202d82f44096594d105d4cafe01068b7e094':f'last_input_head: {INPUT_HEAD}','  processed: 180':'  processed: 240','  actionable_remaining: 10464':'  actionable_remaining: 10404','  next_queue_order: 181':'  next_queue_order: 241','      processed: 79\n      remaining: 4252':'      processed: 139\n      remaining: 4192'}.items():
    if a==b: continue
    assert a in c,a; c=c.replace(a,b,1)
b4=f'''\nw3_batch_0004:\n  status: SEALED\n  validation: PASS\n  touched_rows: 60\n  p1_identity_rows: 60\n  evidence_backed_rows: 60\n  a_grade_rows: {a_count}\n  b_grade_rows: {b_count}\n  current_org_title_confirmed_rows: {confirmed}\n  current_org_title_unresolved_rows: {unresolved}\n  unsupported_current_title_claims: 0\n'''
assert '\nnotes:\n' in c; c=c.replace('\nnotes:\n',b4+'\nnotes:\n',1)
needle='  - Next deterministic queue order is 181.\n'
notes='''  - Next deterministic queue order is 181.\n  - W3-BATCH-0004 processed queue orders 181-240 exactly, all 河北 P1 identity/current-role rows.\n  - 14 rows received current organization/title confirmation; 46 remain explicitly unresolved where evidence was insufficiently current or specific.\n  - The 2026 邢台工商联换届 was honored: 王建江 is retained as 邢台市政协副主席 rather than incorrectly carrying forward the former federation-chair role.\n  - No current organization/title was assigned from a name-only hit; common-name records remain unresolved unless federation/province/person context closed identity.\n  - Next deterministic queue order is 241.\n'''
assert needle in c; c=c.replace(needle,notes,1); cp.write_text(c,encoding='utf-8')

assert 'code: W3-BATCH-0005' in sp.read_text(encoding='utf-8')
assert 'current_gate: W3-BATCH-0005' in cp.read_text(encoding='utf-8')
print({'gate':'W3-BATCH-0004','confirmed':confirmed,'unresolved':unresolved,'A':a_count,'B':b_count,'ledger_rows':len(led),'next':241,'now':NOW})
