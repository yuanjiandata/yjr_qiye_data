#!/usr/bin/env python3
import csv, gzip, hashlib, io, json, re, sys, unicodedata, zipfile
from collections import Counter, defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

SOURCE_FILE_ID = "1jlNP_ENJzQgBsMgZ2bwR6ZoiUdNZhqzR"
SOURCE_TITLE = "名单汇总表_final.xlsx"
EXPECTED_SHA256 = "86ada49718551b560cbb1385a5cd776db271b894d773bd7e643093e583648f3b"
SHEET_ORDER = ["北京","上海","天津","重庆","河北","山西","辽宁","吉林","黑龙江","江苏","浙江","安徽","福建","江西","山东","河南","湖北","湖南","广东","海南","四川","贵州","云南","陕西","甘肃","青海","内蒙古","广西","宁夏","新疆","西藏"]
ETHNICITIES = ["汉族","蒙古族","回族","藏族","维吾尔族","苗族","彝族","壮族","布依族","朝鲜族","满族","侗族","瑶族","白族","土家族","哈尼族","哈萨克族","傣族","黎族","傈僳族","佤族","畲族","高山族","拉祜族","水族","东乡族","纳西族","景颇族","柯尔克孜族","土族","达斡尔族","仫佬族","羌族","布朗族","撒拉族","毛南族","仡佬族","锡伯族","阿昌族","普米族","塔吉克族","怒族","乌孜别克族","俄罗斯族","鄂温克族","德昂族","保安族","裕固族","京族","塔塔尔族","独龙族","鄂伦春族","赫哲族","门巴族","珞巴族","基诺族"]
ETH_SHORT = [x[:-1] for x in ETHNICITIES]
ROLE_TOKENS = ["兼职副主席","专职副主席","常务副主席","兼职副会长","专职副会长","二级巡视员","副主席","副会长","秘书长","主席","常委","执委","会长","委员"]
NS = {"m":"http://schemas.openxmlformats.org/spreadsheetml/2006/main","r":"http://schemas.openxmlformats.org/officeDocument/2006/relationships","pr":"http://schemas.openxmlformats.org/package/2006/relationships"}

def norm(x):
    if x is None: return ""
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", str(x).replace("\u00a0", " "))).strip()

def col_index(ref):
    letters = re.match(r"([A-Z]+)", ref).group(1)
    n=0
    for ch in letters: n=n*26+ord(ch)-64
    return n-1

def read_xlsx(path):
    out=[]
    with zipfile.ZipFile(path) as z:
        shared=[]
        if "xl/sharedStrings.xml" in z.namelist():
            root=ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall("m:si",NS):
                shared.append("".join(t.text or "" for t in si.iterfind(".//m:t",NS)))
        wb=ET.fromstring(z.read("xl/workbook.xml"))
        rels=ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        relmap={r.attrib["Id"]:r.attrib["Target"] for r in rels.findall("pr:Relationship",NS)}
        sheets=[]
        for sh in wb.find("m:sheets",NS):
            name=sh.attrib["name"]; rid=sh.attrib["{%s}id"%NS["r"]]; target=relmap[rid]
            xp=target.lstrip("/") if target.startswith("/") else "xl/"+target.lstrip("/")
            sheets.append((name,xp))
        assert [x[0] for x in sheets] == SHEET_ORDER, [x[0] for x in sheets]
        for si,(name,xp) in enumerate(sheets):
            root=ET.fromstring(z.read(xp)); dim=root.find("m:dimension",NS); max_row=1
            if dim is not None:
                m=re.search(r"(\d+)$",dim.attrib.get("ref","")); max_row=int(m.group(1)) if m else 1
            rowdict={}; sd=root.find("m:sheetData",NS)
            if sd is not None:
                for row in sd.findall("m:row",NS):
                    rn=int(row.attrib["r"]); vals=[None,None,None,None]
                    for c in row.findall("m:c",NS):
                        ci=col_index(c.attrib["r"])
                        if ci>3: continue
                        t=c.attrib.get("t"); v=c.find("m:v",NS)
                        if t=="inlineStr":
                            isel=c.find("m:is",NS); val="" if isel is None else "".join(tn.text or "" for tn in isel.iterfind(".//m:t",NS))
                        elif v is None: val=None
                        elif t=="s": val=shared[int(v.text)]
                        else: val=v.text
                        vals[ci]=val
                    rowdict[rn]=vals
            for rn in range(2,max_row+1): out.append((si,name,rn,*rowdict.get(rn,[None,None,None,None])))
    return out

def par_balance(t):
    t=norm(t); return t.count("(")-t.count(")")

def is_cont_fragment(name):
    t=norm(name)
    if ")" not in t: return False
    close=t.find(")")
    if t[close+1:].strip(): return False
    prefix=t[:close].strip(" (")
    if prefix in ("女","男") or prefix in ETH_SHORT or prefix in ETHNICITIES: return True
    return "工商联" in prefix and bool(re.search(r"(书记|部长|主席|主任|副主席|副部长)$",prefix))

def is_marker_name(name):
    t=norm(name)
    return bool(re.fullmatch(r"\(?(?:共)?\d+人\)?",t)) or t=="(排序)"

def repair_parens(t):
    t=norm(t); notes=[]; o=t.count("("); c=t.count(")")
    if o>c:
        t += ")"*(o-c); notes.append("appended_missing_close_paren")
    elif c>o:
        for _ in range(c-o):
            i=t.find(")")
            if i>=0: t=t[:i]+t[i+1:]; notes.append("removed_unmatched_close_paren")
    return t,notes

def parse_name(payload):
    repaired,notes=repair_parens(payload); gender=""; ethnicity=""; others=[]
    for m in re.finditer(r"\(([^()]*)\)",repaired):
        val=m.group(1).strip(); gv="女" if "女" in val else ("男" if "男" in val else ""); ev=""
        for e in ETHNICITIES:
            if e in val or e[:-1] in val: ev=e; break
        if gv or ev:
            if gv and not gender: gender=gv
            if ev and not ethnicity: ethnicity=ev
            residue=val
            if gv: residue=residue.replace(gv,"")
            if ev: residue=residue.replace(ev,"").replace(ev[:-1],"")
            if residue.strip(): others.append(residue.strip())
        else: others.append(val)
    base=re.sub(r"\([^()]*\)","",repaired); base=re.sub(r"[()]","",base); base=re.sub(r"\s+","",base).strip()
    return base,gender,ethnicity,";".join(x for x in others if x),notes

def canon_role(raw):
    t=norm(raw); hits=[]
    for tok in ROLE_TOKENS:
        i=t.find(tok)
        if i>=0: hits.append((i,-len(tok),tok))
    return sorted(hits)[0][2] if hits else t

def is_compound(province,payload,base):
    if province=="安徽":
        if len(base)>=5: return True
        m=re.search(r"\((?:女|男|[^)]*族)\)",norm(payload))
        if m and norm(payload)[m.end():].strip(): return True
    if province=="河南" and len(base)>=5: return True
    if province=="广东" and len(base)>=5 and len(re.findall(r"\((?:女|男)\)",norm(payload)))>=2: return True
    return False

def csv_bytes(rows,fields):
    s=io.StringIO(newline=""); w=csv.DictWriter(s,fieldnames=fields,lineterminator="\n"); w.writeheader()
    for row in rows: w.writerow({k:row.get(k,"") for k in fields})
    return s.getvalue().encode("utf-8")

def write_gz(path,data): path.write_bytes(gzip.compress(data,compresslevel=9,mtime=0))
def sha(data): return hashlib.sha256(data).hexdigest()

def main():
    src=Path(sys.argv[1]); root=Path(sys.argv[2]); ev=root/"evidence"; ev.mkdir(parents=True,exist_ok=True)
    assert sha(src.read_bytes())==EXPECTED_SHA256
    rows=read_xlsx(src); assert len(rows)==10762
    by=defaultdict(list)
    for r in rows: by[r[1]].append(r)
    continuations=[]
    for sn,rr in by.items():
        prev=None
        for r in rr:
            if prev and par_balance(prev[4])>0 and is_cont_fragment(r[4]) and norm(r[3])==norm(prev[3]) and norm(r[5])==norm(prev[5]): continuations.append((prev,r))
            prev=r
    assert len(continuations)==90
    cont_rows={(b[1],b[2]) for a,b in continuations}; cont_prev={(a[1],a[2]) for a,b in continuations}
    prev_for={(b[1],b[2]):(a[1],a[2]) for a,b in continuations}; frag={(a[1],a[2]):norm(b[4]) for a,b in continuations}
    marker_named={(r[1],r[2]) for r in rows if is_marker_name(r[4])}; assert len(marker_named)==9
    pidx={sn:i+1 for i,sn in enumerate(SHEET_ORDER)}; records=[]
    for r in rows:
        si,sn,er,role,name,unit,extra=r; nonempty=any(norm(v) for v in r[3:])
        if not nonempty or (sn,er) in cont_rows or (sn,er) in marker_named or not norm(name): continue
        payload=norm(name)+frag.get((sn,er),""); base,gender,eth,other,notes=parse_name(payload); quality="OK"
        if len(base)<=1: quality="SOURCE_SPLIT_OR_TRUNCATED"
        elif is_compound(sn,payload,base): quality="SOURCE_COMPOUND_OR_SHIFTED"
        elif notes or ((sn,er) in cont_prev and not (sn=="湖南" and er==3)): quality="MALFORMED_PAREN_REPAIRED"
        pid=f"FC2515-P{pidx[sn]:02d}-R{er:04d}"
        records.append({"person_id":pid,"province":sn,"source_file_id":SOURCE_FILE_ID,"source_file":SOURCE_TITLE,"source_sheet":sn,"excel_row":er,"source_row_id":f"{SOURCE_FILE_ID}:{sn}:{er}","name_raw":norm(name),"payload_name_raw":payload,"name_normalized":base,"gender":gender,"ethnicity":eth,"annotation_other":other,"role_raw":norm(role),"federation_role":canon_role(role),"unit_raw":norm(unit),"extra_raw":norm(extra),"name_quality":quality,"exact_value_group_id":"","ambiguity_group_id":"","normalization_notes":";".join(notes+(["structural_annotation_continuation_joined"] if (sn,er) in cont_prev else []))})
    assert len(records)==10644 and len({r["person_id"] for r in records})==10644
    reliable=[r for r in records if r["name_quality"] in ("OK","MALFORMED_PAREN_REPAIRED")]
    exact=defaultdict(list)
    for r in reliable: exact[(r["province"],r["name_raw"],r["role_raw"],r["unit_raw"],r["extra_raw"])].append(r)
    exact_groups=[v for v in exact.values() if len(v)>1]; exact_groups.sort(key=lambda v:(pidx[v[0]["province"]],v[0]["excel_row"]))
    for i,v in enumerate(exact_groups,1):
        gid=f"EDG-{i:04d}"
        for r in v: r["exact_value_group_id"]=gid
    same=defaultdict(list)
    for r in reliable: same[(r["province"],r["name_normalized"])].append(r)
    same_groups=[v for v in same.values() if len(v)>1]; same_groups.sort(key=lambda v:(pidx[v[0]["province"]],v[0]["name_normalized"],v[0]["excel_row"]))
    for i,v in enumerate(same_groups,1):
        gid=f"ANG-{i:04d}"
        for r in v: r["ambiguity_group_id"]=gid
    assert len(exact_groups)==9 and sum(map(len,exact_groups))==18
    assert len(same_groups)==1913 and sum(map(len,same_groups))==4331
    recmap={(r["province"],r["excel_row"]):r for r in records}; rowmap=[]
    for r in rows:
        si,sn,er,role,name,unit,extra=r; nonempty=any(norm(v) for v in r[3:]); rt="BLANK"; pid=co=q=notes=""; payload=norm(name)
        if nonempty:
            if (sn,er) in cont_rows:
                rt="ANNOTATION_CONTINUATION"; pr=recmap[prev_for[(sn,er)]]; pid=pr["person_id"]; co=f"{SOURCE_FILE_ID}:{prev_for[(sn,er)][0]}:{prev_for[(sn,er)][1]}"; q="STRUCTURAL_CONTINUATION"; notes="joined_to_preceding_source_person"
            elif (sn,er) in marker_named or not norm(name): rt="NON_PERSON_MARKER"; notes="embedded_count_sort_or_nonperson_marker"
            else:
                rt="PERSON"; pr=recmap[(sn,er)]; pid=pr["person_id"]; q=pr["name_quality"]; notes=pr["normalization_notes"]; payload=pr["payload_name_raw"]
        rowmap.append({"source_row_id":f"{SOURCE_FILE_ID}:{sn}:{er}","source_file_id":SOURCE_FILE_ID,"source_file":SOURCE_TITLE,"province":sn,"excel_row":er,"row_type":rt,"role_raw":norm(role),"name_raw":norm(name),"unit_raw":norm(unit),"extra_raw":norm(extra),"payload_name_raw":payload,"canonical_person_id":pid,"continuation_of_source_row_id":co,"name_quality":q,"normalization_notes":notes})
    assert Counter(x["row_type"] for x in rowmap)==Counter({"PERSON":10644,"ANNOTATION_CONTINUATION":90,"BLANK":18,"NON_PERSON_MARKER":10})
    review=[]
    for v in exact_groups:
        gid=v[0]["exact_value_group_id"]
        for r in v: review.append({"review_type":"EXACT_VALUE_DUPLICATE_CANDIDATE","review_group_id":gid,"group_size":len(v),"person_id":r["person_id"],"province":r["province"],"excel_row":r["excel_row"],"name_raw":r["name_raw"],"name_normalized":r["name_normalized"],"role_raw":r["role_raw"],"federation_role":r["federation_role"],"unit_raw":r["unit_raw"],"review_reason":"identical raw name + raw federation role + unit + extra within province; no automatic merge"})
    for v in same_groups:
        gid=v[0]["ambiguity_group_id"]
        for r in v: review.append({"review_type":"SAME_NAME_REVIEW","review_group_id":gid,"group_size":len(v),"person_id":r["person_id"],"province":r["province"],"excel_row":r["excel_row"],"name_raw":r["name_raw"],"name_normalized":r["name_normalized"],"role_raw":r["role_raw"],"federation_role":r["federation_role"],"unit_raw":r["unit_raw"],"review_reason":"same normalized name occurs multiple times within province; identity not merged from name alone"})
    exceptions=[x for x in rowmap if x["row_type"] in ("ANNOTATION_CONTINUATION","NON_PERSON_MARKER") or x["name_quality"] not in ("","OK")]
    blobs={"W1_MASTER_PERSON_ROSTER.csv":csv_bytes(records,list(records[0].keys())),"W1_SOURCE_ROW_MAP.csv":csv_bytes(rowmap,list(rowmap[0].keys())),"W1_DUPLICATE_REVIEW.csv":csv_bytes(review,list(review[0].keys())),"W1_NORMALIZATION_EXCEPTIONS.csv":csv_bytes(exceptions,list(rowmap[0].keys()))}
    for name,data in blobs.items():
        if name=="W1_NORMALIZATION_EXCEPTIONS.csv": (ev/name).write_bytes(data)
        else: write_gz(ev/(name+".gz"),data)
    quality=Counter(r["name_quality"] for r in records); severe=Counter(r["province"] for r in records if r["name_quality"].startswith("SOURCE_")); roles=Counter(r["federation_role"] for r in records); genders=Counter(r["gender"] for r in records if r["gender"]); eths=Counter(r["ethnicity"] for r in records if r["ethnicity"])
    assert quality==Counter({"OK":10448,"MALFORMED_PAREN_REPAIRED":95,"SOURCE_SPLIT_OR_TRUNCATED":70,"SOURCE_COMPOUND_OR_SHIFTED":31})
    assert severe==Counter({"河南":51,"安徽":27,"浙江":22,"广东":1})
    artifact_meta={}
    for name,data in blobs.items():
        stored=ev/name if name=="W1_NORMALIZATION_EXCEPTIONS.csv" else ev/(name+".gz")
        count=len(records) if name.startswith("W1_MASTER") else len(rowmap) if name.startswith("W1_SOURCE") else len(review) if name.startswith("W1_DUPLICATE") else len(exceptions)
        artifact_meta[stored.name]={"rows":count,"uncompressed_sha256":sha(data),"stored_sha256":sha(stored.read_bytes()),"stored_bytes":stored.stat().st_size}
    rules="""schema: fc-exec-w1-normalization-rules-v1
source_file_id: 1jlNP_ENJzQgBsMgZ2bwR6ZoiUdNZhqzR
source_locator: file_id + source_sheet + excel_row
unicode: NFKC
whitespace: trim_and_collapse
person_id: FC2515-P<sheet_order_2d>-R<excel_row_4d>
name_policy:
  gender: extract parenthetical 女/男
  ethnicity: extract recognized PRC ethnicity annotation
  other_parenthetical: preserve in annotation_other
  structural_continuation: attach deterministic closing annotation fragment to preceding same-role/same-unit row
  severe_corruption: preserve raw text and flag; never guess repaired identity
role_policy:
  method: earliest explicit recognized federation role token; longest token wins at same position
identity_policy:
  name_only_auto_merge: forbidden
  exact_duplicate: review candidate only
  same_normalized_name_within_province: ambiguity review only
"""
    (ev/"W1_NORMALIZATION_RULES.yaml").write_text(rules,encoding="utf-8")
    ml=["schema: fc-exec-w1-metrics-v1","project_id: FC-EXEC-2515-01","input:",f"  source_file_id: {SOURCE_FILE_ID}","  physical_rows_after_header: 10762","  nonempty_rows: 10744","  named_rows: 10743","classification:","  person_source_records: 10644","  annotation_continuation_rows: 90","  non_person_marker_rows: 10","  blank_rows: 18","name_quality:"]
    for k in ["OK","MALFORMED_PAREN_REPAIRED","SOURCE_SPLIT_OR_TRUNCATED","SOURCE_COMPOUND_OR_SHIFTED"]: ml.append(f"  {k}: {quality[k]}")
    ml += ["severe_source_name_exceptions_by_province:"]+[f"  {k}: {v}" for k,v in sorted(severe.items(),key=lambda x:pidx[x[0]])]
    ml += ["identity_review:",f"  exact_value_duplicate_candidate_groups: {len(exact_groups)}",f"  exact_value_duplicate_candidate_rows: {sum(map(len,exact_groups))}",f"  same_name_review_groups: {len(same_groups)}",f"  same_name_review_rows: {sum(map(len,same_groups))}","  name_only_auto_merges: 0","gender_counts:"]+[f"  {k}: {v}" for k,v in sorted(genders.items())]
    ml += [f"ethnicity_nonempty_count: {sum(eths.values())}","role_counts:"]+[f"  {json.dumps(k,ensure_ascii=False)}: {v}" for k,v in roles.most_common()]
    ml += ["artifacts:"]
    for k,v in artifact_meta.items(): ml += [f"  {k}:",f"    rows: {v['rows']}",f"    uncompressed_sha256: {v['uncompressed_sha256']}",f"    stored_sha256: {v['stored_sha256']}",f"    stored_bytes: {v['stored_bytes']}"]
    (ev/"W1_METRICS.yaml").write_text("\n".join(ml)+"\n",encoding="utf-8")
    am=["schema: fc-exec-w1-artifact-manifest-v1","compression: gzip_mtime_0","files:"]
    for k,v in artifact_meta.items(): am += [f"  {k}:",f"    rows: {v['rows']}",f"    stored_sha256: {v['stored_sha256']}",f"    uncompressed_sha256: {v['uncompressed_sha256']}"]
    am += ["read_note: compressed CSV artifacts are deterministic gzip; fetch path as base64 and gunzip"]
    (ev/"W1_ARTIFACT_MANIFEST.yaml").write_text("\n".join(am)+"\n",encoding="utf-8")
    validation=f"""# W1-PERSON-NORMALIZE Validation

## INPUT
- Repo truth at run start: `main@8f1139a125266a042c05eba9b8e106a713836dcb`
- Frozen source workbook: `{SOURCE_TITLE}` (`{SOURCE_FILE_ID}`)
- SHA-256: `{EXPECTED_SHA256}`

## WORK
- Preserved all physical source rows and deterministic `file_id + sheet + excel_row` locators.
- Normalized Unicode/whitespace, gender, ethnicity, other annotations, and federation roles.
- Rejoined 90 deterministic annotation-continuation rows without inventing identities.
- Assigned 10,644 stable source-row-based `person_id` values.
- Flagged source corruption rather than guessing repaired names.
- Generated exact-duplicate candidates and same-name ambiguity groups; no name-only automatic merges were performed.

## VALIDATION
- Physical source rows: **10,762** = 10,644 PERSON + 90 ANNOTATION_CONTINUATION + 10 NON_PERSON_MARKER + 18 BLANK.
- Named source rows: **10,743** = 10,644 PERSON + 90 continuation + 9 named markers.
- Stable person IDs: **10,644 / 10,644 unique**.
- Name quality: OK **10,448**; malformed-parenthesis repaired **95**; split/truncated source **70**; compound/shifted source **31**.
- Severe source-name exceptions: **101** (河南 51 / 安徽 27 / 浙江 22 / 广东 1).
- Exact-value duplicate candidate groups: **9** / 18 rows.
- Same-normalized-name review groups: **1,913** / 4,331 rows.
- Name-only automatic merges: **0**.

## RESULT
**PASS / SEALED**

## NEXT_GATE
`W2-EXISTING-ABSORB`
"""
    (ev/"W1_VALIDATION.md").write_text(validation,encoding="utf-8")
    print(json.dumps({"person_records":len(records),"row_types":dict(Counter(x["row_type"] for x in rowmap)),"name_quality":dict(quality),"severe":dict(severe),"exact_groups":len(exact_groups),"same_name_groups":len(same_groups),"review_rows":len(review),"exceptions":len(exceptions),"artifacts":artifact_meta},ensure_ascii=False,indent=2))

if __name__=="__main__": main()
