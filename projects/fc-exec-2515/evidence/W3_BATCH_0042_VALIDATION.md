# W3-BATCH-0042 Validation

- Gate: `W3-BATCH-0042`
- Queue orders: `2461-2520`
- Touched rows: **60** (`广东 60`)
- Priority: `P1_IDENTITY` 60
- Fresh identity research rows: **0**
- Prior SEALED/PASS evidence reused under exact repository ambiguity-group controls: **60**
- Current-source rechecks on reused confirmed rows: **7**
- Evidence coverage: **60/60**
- Evidence grades: **A=58, B=2, C=0**
- Current organization + title confirmed: **7**
- No-current-role confirmed: **0**
- Explicit current-role unresolved: **53**
- Unsupported current-title claims: **0**
- Prior sealed logical ledger/overlay: **2460 rows**, queue `1-2460`, PASS at W3-BATCH-0041
- Appended result segment: **60 rows**, queue `2461-2520`
- Logical cumulative ledger after append: **2520 rows**, queue `1-2520` contiguous, no gap/overlap
- Logical cumulative overlay after append: **2520 rows**, queue `1-2520` contiguous, no gap/overlap
- Gate segment storage: plain UTF-8 CSV/TSV; the repository segmented-store reader natively supports non-gzip segments.

## Source-input control

- Google Drive membership baseline `名单汇总表_final.xlsx` was re-read as source input only.
- Local SHA-256 recheck: `86ada49718551b560cbb1385a5cd776db271b894d773bd7e643093e583648f3b` — exact match to repository-frozen source hash.
- Google Drive supplement `名单汇总表_补全单位.xlsx` was re-read as source input only.
- Local SHA-256 recheck: `136998b03210bd5144be16df3e964c64cae94581170268bc00764a041f596316` — exact match to repository-frozen source hash.
- W1/W2 deterministic ordering was reconstructed from the frozen source workbook and repository normalization/queue rules. Queue `2461-2520` is exactly the next 60 Guangdong `P1_IDENTITY` records.
- Google Drive is not used as control-state authority.

## Evidence / identity controls

- All 60 source rows are present in the official 全国工商联 `广东省工商联第十三届执委会名单`.
- Every touched row belongs to an ambiguity group whose same Guangdong normalized-name identity already has a SEALED/PASS W3 outcome. Reuse is permitted only on exact `ambiguity_group_id + province + normalized_name` equality; every source row retains its independent `person_id`.
- No identity or current role is inferred from name alone.
- Prior unresolved outcomes remain unresolved rather than being promoted from same-name or organization-only hits.
- Seven prior confirmed outcomes received a current-source recheck:
  - **何小鹏** — 2026-09-01 小鹏集团 official material identifies him as `小鹏集团董事长兼CEO`.
  - **蔡光辉** — 2026-07-01 汕头市工商联 official material identifies him as `广东省澄海商会会长`.
  - **温志芬** — 2026-01-27 新兴县政府 material identifies him as `全国工商联副主席、温氏股份董事长`; current organization/title recorded as `温氏食品集团股份有限公司 / 董事长`.
  - **王理宗** — 2026-03-06 广东政协 material identifies him as `广东高科技产业商会会长`.
  - **李婧** — 2026-01-25 南方网 material directly identifies `广东省工商联常委、肇庆市工商联副主席、广东高登铝业集团执行总裁`; retained at B grade.
  - **陈满新** — 2026-01-08 current local-federation-context reporting identifies `东莞市工商联（总商会）副主席、东莞市青年企业家联合会会长、东莞市瀚森投资集团有限公司总裁`; retained at B grade.
  - **赖志光** — 2026-06-22 粤港澳大湾区门户 material identifies `客青会会长、广东东升控股集团有限公司总裁`.
- A separate 2026 same-name `李婧` hit without this exact federation/enterprise bridge was not used to alter the sealed identity.
- No current organization/title field is populated on an unresolved row.

## Deterministic hashes

- results SHA-256: `47e6ed83f9d20100c483f81c05e570b2a8210a8311afe6e7e9e871bed363aa40`
- research SHA-256: `a75ab0bf2752643ef76d1c6f03c2162f94d9192680cf14581741f6e9083554fa`

**PASS**
