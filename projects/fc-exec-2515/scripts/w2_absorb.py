#!/usr/bin/env python3
import csv,gzip,hashlib,io,json,re,sys,unicodedata,zipfile
from collections import Counter,defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

SUPPLEMENT_ID='10Zc9caTUy4eJITc802cisKSCQhuOJsEp'
SUPPLEMENT_TITLE='名单汇总表_补全单位.xlsx'
SUPPLEMENT_SHA='136998b03210bd5144be16df3e964c64cae94581170268bc00764a041f596316'
SHEET_ORDER=['北京','上海','天津','重庆','河北','山西','辽宁','吉林','黑龙江','江苏','浙江','安徽','福建','江西','山东','河南','湖北','湖南','广东','海南','四川','贵州','云南','陕西','甘肃','青海','内蒙古','广西','宁夏','新疆','西藏']
ROLE_TOKENS=['兼职副主席','专职副主席','常务副主席','兼职副会长','专职副会长','二级巡视员','副主席','副会长','秘书长','主席','常委','执委','会长','委员']
PLACEHOLDERS={'','暂未公开','未公开','不详','待核实','无','暂无','未知','企业家'}
ORG_COMPANY_RE=re.compile(r'(有限责任公司|股份有限公司|有限公司|集团(?:股份)?有限公司|集团|公司|银行|证券|保险|基金|控股|实业|投资|资本|科技|制造|能源|医药|药业|电器|地产|置业|商贸|物流|航空|网络|信息|传媒|食品|汽车|矿业|化工|建设|工程)')
EXEC_RE=re.compile(r'(董事局主席|董事长|副董事长|CEO|首席执行官|总裁|总经理|创始人|联合创始人|执行董事|首席合伙人|合伙人|实际控制人|法定代表人)')
TITLE_TOKENS=['董事长、首席执行官兼总裁','首席合伙人、董事长','董事长、首席执行官','联席CEO、执行董事','副董事长、总裁','董事长兼总经理','董事长兼总裁','董事局主席','党委书记','常务副主席','首席执行官','执行董事','董事长','副董事长','总裁','总经理','CEO','创始人','合伙人','主席','副主席','副会长','会长','秘书长']
NS={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','pr':'http://schemas.openxmlformats.org/package/2006/relationships'}

def norm(x):
    if x is None:return ''
    return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',str(x).replace('\u00a0',' '))).strip()

def simple_name(x):
    t=norm(x)
    t=re.sub(r'[（(][^（）()]*[）)]','',t)
    return re.sub(r'[\s()（）]','',t).strip()

def canon_role(raw):
    t=norm(raw); hits=[]
    for tok in ROLE_TOKENS:
        i=t.find(tok)
        if i>=0:hits.append((i,-len(tok),tok))
    return sorted(hits)[0][2] if hits else t

def col_index(ref):
    letters=re.match(r'([A-Z]+)',ref).group(1); n=0
    for ch in letters:n=n*26+ord(ch)-64
    return n-1

def read_xlsx(path):
    out={}
    with zipfile.ZipFile(path) as z:
        shared=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            root=ET.fromstring(z.read('xl/sharedStrings.xml'))
            for si in root.findall('m:si',NS):shared.append(''.join(t.text or '' for t in si.iterfind('.//m:t',NS)))
        wb=ET.fromstring(z.read('xl/workbook.xml')); rels=ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        relmap={r.attrib['Id']:r.attrib['Target'] for r in rels.findall('pr:Relationship',NS)}
        for sh in wb.find('m:sheets',NS):
            name=sh.attrib['name']; rid=sh.attrib['{%s}id'%NS['r']]; target=relmap[rid]
            xp=target.lstrip('/') if target.startswith('/') else 'xl/'+target.lstrip('/')
            root=ET.fromstring(z.read(xp)); rows=[]; sd=root.find('m:sheetData',NS)
            if sd is not None:
                for row in sd.findall('m:row',NS):
                    rn=int(row.attrib['r']); vals=['','','','']
                    for c in row.findall('m:c',NS):
                        ci=col_index(c.attrib['r'])
                        if ci>3:continue
                        t=c.attrib.get('t'); v=c.find('m:v',NS)
                        if t=='inlineStr':
                            isel=c.find('m:is',NS); val='' if isel is None else ''.join(tn.text or '' for tn in isel.iterfind('.//m:t',NS))
                        elif v is None:val=''
                        elif t=='s':val=shared[int(v.text)]
                        else:val=v.text or ''
                        vals[ci]=norm(val)
                    rows.append((rn,*vals))
            out[name]=rows
    return out

def split_combined(value):
    v=norm(value)
    if v in PLACEHOLDERS:return '','','EMPTY_OR_PLACEHOLDER'
    # Prefer a rightmost whitespace boundary whose suffix contains a recognized title token.
    parts=v.split(' ')
    for i in range(1,len(parts)):
        org=' '.join(parts[:i]).strip(); tail=' '.join(parts[i:]).strip()
        if org and any(tok in tail for tok in TITLE_TOKENS):return org,tail,'SPLIT_TITLE_SUFFIX'
    # Some source strings concatenate title with enterprise name; keep whole value as organization instead of guessing.
    return v,'','UNSPLIT_SOURCE_VALUE'

def std_org(v):
    t=norm(v)
    return t.replace('（','(').replace('）',')')

def csv_bytes(rows,fields):
    s=io.StringIO(newline=''); w=csv.DictWriter(s,fieldnames=fields,lineterminator='\n'); w.writeheader()
    for r in rows:w.writerow({k:r.get(k,'') for k in fields})
    return s.getvalue().encode('utf-8')

def gzwrite(path,data):path.write_bytes(gzip.compress(data,compresslevel=9,mtime=0))
def sha(b):return hashlib.sha256(b).hexdigest()

def main():
    root=Path(sys.argv[1]); supplement=Path(sys.argv[2]); ev=root/'evidence'; ev.mkdir(parents=True,exist_ok=True)
    assert sha(supplement.read_bytes())==SUPPLEMENT_SHA
    roster=list(csv.DictReader(gzip.open(ev/'W1_MASTER_PERSON_ROSTER.csv.gz','rt',encoding='utf-8-sig',newline='')))
    assert len(roster)==10644 and len({r['person_id'] for r in roster})==10644
    pidx={p:i for i,p in enumerate(SHEET_ORDER)}
    supp=read_xlsx(supplement); assert list(supp.keys())==SHEET_ORDER
    # Build deterministic supplement groups by province+canonical role+simple name.
    sg=defaultdict(list)
    for prov,rows in supp.items():
        for rn,role,name,unit,extra in rows:
            if rn==1 or not norm(name):continue
            key=(prov,canon_role(role),simple_name(name))
            sg[key].append({'row':rn,'role_raw':norm(role),'name_raw':norm(name),'unit_raw':norm(unit),'extra_raw':norm(extra)})
    wg=defaultdict(list)
    for r in roster:wg[(r['province'],r['federation_role'],r['name_normalized'])].append(r)
    for v in wg.values():v.sort(key=lambda x:int(x['excel_row']))
    # Deterministic mapping only: unique key or exact same group cardinality with source order preserved.
    smap={}; match_stats=Counter()
    for key,wrows in wg.items():
        srows=sg.get(key,[])
        if len(wrows)==1 and len(srows)==1:
            smap[wrows[0]['person_id']]=srows[0]; match_stats['UNIQUE_KEY_MATCH']+=1
        elif len(wrows)>0 and len(wrows)==len(srows):
            for wr,sr in zip(wrows,srows):smap[wr['person_id']]=sr
            match_stats['ORDERED_EQUAL_CARDINALITY_MATCH']+=len(wrows)
        elif srows:
            match_stats['AMBIGUOUS_GROUP_NOT_ABSORBED']+=len(wrows)
    output=[]; ledger=[]; unresolved=[]; class_counts=Counter(); method_counts=Counter(); source_counts=Counter()
    for r in roster:
        final_unit=norm(r.get('unit_raw')); final_title=norm(r.get('extra_raw'))
        has_final=bool(final_unit and final_unit not in PLACEHOLDERS)
        org=title=''; source_id=source_file=source_sheet=source_row=''; method=''; splitq=''; source_value=''
        if has_final:
            org=final_unit; title=final_title; method='FINAL_SEPARATE_FIELDS'; splitq='SEPARATE_FIELDS'; source_id=r['source_file_id']; source_file=r['source_file']; source_sheet=r['source_sheet']; source_row=r['excel_row']; source_value=' | '.join(x for x in [final_unit,final_title] if x)
        else:
            sr=smap.get(r['person_id'])
            if sr and norm(sr['unit_raw']) not in PLACEHOLDERS:
                org,title,splitq=split_combined(sr['unit_raw']); method='SUPPLEMENT_COMBINED_FIELD'; source_id=SUPPLEMENT_ID; source_file=SUPPLEMENT_TITLE; source_sheet=r['province']; source_row=str(sr['row']); source_value=sr['unit_raw']
        org_std=std_org(org)
        person_type='unclassified'; entrepreneur='UNKNOWN'
        if org_std and re.search(r'(工商业联合会|工商联|总商会)',org_std):person_type='federation_staff'; entrepreneur='NO'
        elif org_std and ORG_COMPANY_RE.search(org_std) and (EXEC_RE.search(title) or EXEC_RE.search(source_value)):
            person_type='entrepreneur_candidate'; entrepreneur='CANDIDATE'
        elif org_std and ORG_COMPANY_RE.search(org_std):person_type='enterprise_affiliated_candidate'; entrepreneur='CANDIDATE'
        elif not org_std and r['federation_role'].startswith('专职'):person_type='federation_staff_candidate'; entrepreneur='UNKNOWN'
        class_counts[person_type]+=1
        status='SOURCE_ONLY_NEEDS_CURRENT_VERIFICATION' if org_std else 'UNRESOLVED_NO_EXISTING_ORGANIZATION'
        reason=''
        if r['name_quality'].startswith('SOURCE_'):
            status='UNRESOLVED_SOURCE_NAME_ANOMALY'; reason=r['name_quality']
        elif not org_std:reason='NO_NONPLACEHOLDER_ORGANIZATION_IN_EXISTING_SOURCES'
        elif r.get('ambiguity_group_id'):reason='SAME_NAME_GROUP_REQUIRES_EXTERNAL_IDENTITY_CONFIRMATION'
        row=dict(r)
        row.update({'person_type':person_type,'entrepreneur_flag':entrepreneur,'current_organization':org_std,'current_title':norm(title),'organization_standard_name':org_std,'group_or_brand':'','ownership_type':'','industry':'','listed_status':'','ticker':'','employment_status':'','source_1':source_id,'source_2':'','source_date':'','evidence_grade':'SOURCE_EXISTING_ONLY','verification_status':status,'existing_source_file':source_file,'existing_source_sheet':source_sheet,'existing_source_row':source_row,'absorption_method':method,'split_quality':splitq,'unresolved_reason':reason})
        output.append(row)
        if method:
            method_counts[method]+=1; source_counts[source_file]+=1
            ledger.append({'person_id':r['person_id'],'province':r['province'],'name_normalized':r['name_normalized'],'federation_role':r['federation_role'],'organization':org_std,'title':norm(title),'source_file_id':source_id,'source_file':source_file,'source_sheet':source_sheet,'source_row':source_row,'source_value_raw':source_value,'absorption_method':method,'split_quality':splitq,'evidence_grade':'SOURCE_EXISTING_ONLY','current_verification_required':'YES'})
        # W2 contains no current web verification, so every canonical person must enter W3.
        # Priority only determines deterministic processing order.
        if r['name_quality'].startswith('SOURCE_'):
            qpriority='P0_NAME_REPAIR'; qreason=reason or r['name_quality']
        elif r.get('ambiguity_group_id'):
            qpriority='P1_IDENTITY'; qreason=reason or 'SAME_NAME_GROUP_REQUIRES_EXTERNAL_IDENTITY_CONFIRMATION'
        elif not org_std:
            qpriority='P2_ORG_TITLE_LOOKUP'; qreason=reason or 'NO_NONPLACEHOLDER_ORGANIZATION_IN_EXISTING_SOURCES'
        else:
            qpriority='P3_CURRENT_VERIFY'; qreason='EXISTING_SOURCE_REQUIRES_CURRENT_WEB_VERIFICATION'
        unresolved.append({'queue_order':0,'person_id':r['person_id'],'province':r['province'],'excel_row':r['excel_row'],'name_normalized':r['name_normalized'],'federation_role':r['federation_role'],'name_quality':r['name_quality'],'ambiguity_group_id':r.get('ambiguity_group_id',''),'current_organization':org_std,'current_title':norm(title),'reason':qreason,'priority':qpriority})
    unresolved.sort(key=lambda x:({'P0_NAME_REPAIR':0,'P1_IDENTITY':1,'P2_ORG_TITLE_LOOKUP':2,'P3_CURRENT_VERIFY':3}[x['priority']],pidx[x['province']],int(x['excel_row'])))
    for i,x in enumerate(unresolved,1):x['queue_order']=i
    assert len(output)==10644 and len({x['person_id'] for x in output})==10644
    assert all(output[i]['person_id']==roster[i]['person_id'] for i in range(len(roster)))
    # Every absorbed row has provenance; every unresolved row has a reason.
    assert all(x['source_file_id'] and x['source_file'] and x['source_row'] for x in ledger)
    assert all(x['reason'] for x in unresolved)
    fields=list(output[0].keys()); bmaster=csv_bytes(output,fields); bledger=csv_bytes(ledger,list(ledger[0].keys()) if ledger else ['person_id']); bunres=csv_bytes(unresolved,list(unresolved[0].keys()) if unresolved else ['queue_order'])
    gzwrite(ev/'W2_MASTER_ROSTER.csv.gz',bmaster); gzwrite(ev/'W2_EVIDENCE_LEDGER.csv.gz',bledger); gzwrite(ev/'W2_UNRESOLVED_QUEUE.csv.gz',bunres)
    actual_org=sum(bool(x['current_organization']) for x in output); actual_title=sum(bool(x['current_title']) for x in output); cand=sum(x['entrepreneur_flag']=='CANDIDATE' for x in output)
    metrics=['schema: fc-exec-w2-metrics-v1','project_id: FC-EXEC-2515-01','input:',f'  w1_person_records: {len(roster)}',f'  supplement_file_id: {SUPPLEMENT_ID}',f'  supplement_sha256: {SUPPLEMENT_SHA}','matching:']
    for k,v in sorted(match_stats.items()):metrics.append(f'  {k}: {v}')
    metrics += ['absorption:']+[f'  {k}: {v}' for k,v in sorted(method_counts.items())]
    metrics += [f'  records_with_organization: {actual_org}',f'  records_with_title: {actual_title}',f'  evidence_ledger_rows: {len(ledger)}',f'  unresolved_queue_rows: {len(unresolved)}',f'  entrepreneur_candidate_rows: {cand}','person_type_counts:']+[f'  {json.dumps(k,ensure_ascii=False)}: {v}' for k,v in class_counts.most_common()]
    metrics += ['artifacts:',f'  W2_MASTER_ROSTER.csv.gz: {sha((ev/"W2_MASTER_ROSTER.csv.gz").read_bytes())}',f'  W2_EVIDENCE_LEDGER.csv.gz: {sha((ev/"W2_EVIDENCE_LEDGER.csv.gz").read_bytes())}',f'  W2_UNRESOLVED_QUEUE.csv.gz: {sha((ev/"W2_UNRESOLVED_QUEUE.csv.gz").read_bytes())}']
    (ev/'W2_METRICS.yaml').write_text('\n'.join(metrics)+'\n',encoding='utf-8')
    validation=f'''# W2-EXISTING-ABSORB Validation\n\n## INPUT\n- W1 canonical roster: **10,644** person records.\n- Existing consolidated source: `{SUPPLEMENT_TITLE}` (`{SUPPLEMENT_ID}`), SHA-256 `{SUPPLEMENT_SHA}`.\n- Frozen baseline source values already carried by W1 from `名单汇总表_final.xlsx`.\n- Province-level source folder remains upstream provenance inventory; this gate uses the consolidated 31-sheet workbooks to avoid duplicating the same derivative rows.\n\n## WORK\n- Preserved all W1 person IDs and source-row provenance.\n- Preferred already-separated organization/title values from the frozen final workbook.\n- Filled missing values from the 31-sheet supplement only through deterministic province + canonical federation role + normalized-name matching.\n- For duplicated keys, absorption occurs only when W1 and supplement group cardinality is identical, preserving source order; mismatched groups are not guessed.\n- Split combined supplement values only when a recognized title suffix is explicitly separated by whitespace; otherwise preserved the whole source value as organization rather than inventing a title.\n- Classified only obvious federation staff and enterprise/entrepreneur candidates. No person is marked confirmed entrepreneur in W2.\n- Generated a deterministic unresolved/current-verification queue for W3.\n\n## VALIDATION\n- Output records: **{len(output)} / 10,644**, unique person IDs **{len(set(x['person_id'] for x in output))}**.\n- Records with non-placeholder organization absorbed: **{actual_org}**.\n- Records with title absorbed: **{actual_title}**.\n- Evidence ledger rows: **{len(ledger)}**, all with source file ID/file/sheet/row provenance.\n- Entrepreneur candidates from existing source only: **{cand}**; confirmed entrepreneurs: **0**.\n- Unresolved/current identity queue rows: **{len(unresolved)}**, all with explicit reason and deterministic priority/order.\n- Source-name anomalies remain unresolved; same-name groups are not merged or externally resolved in this gate.\n\n## RESULT\n**PASS / SEALED** — existing source values are absorbed without unsupported identity or current-employment claims.\n\n## NEXT_GATE\n`W3-EVIDENCE-ENRICH`\n'''
    (ev/'W2_VALIDATION.md').write_text(validation,encoding='utf-8')
    manifest={'W2_MASTER_ROSTER.csv.gz':(len(output),sha((ev/'W2_MASTER_ROSTER.csv.gz').read_bytes())),'W2_EVIDENCE_LEDGER.csv.gz':(len(ledger),sha((ev/'W2_EVIDENCE_LEDGER.csv.gz').read_bytes())),'W2_UNRESOLVED_QUEUE.csv.gz':(len(unresolved),sha((ev/'W2_UNRESOLVED_QUEUE.csv.gz').read_bytes()))}
    am=['schema: fc-exec-w2-artifact-manifest-v1','files:']
    for k,(n,h) in manifest.items():am += [f'  {k}:',f'    rows: {n}',f'    stored_sha256: {h}']
    (ev/'W2_ARTIFACT_MANIFEST.yaml').write_text('\n'.join(am)+'\n',encoding='utf-8')
    print(json.dumps({'records':len(output),'org':actual_org,'title':actual_title,'ledger':len(ledger),'unresolved':len(unresolved),'entrepreneur_candidates':cand,'methods':method_counts,'matches':match_stats},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
