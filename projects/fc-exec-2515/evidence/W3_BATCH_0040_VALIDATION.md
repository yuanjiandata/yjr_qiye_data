# W3-BATCH-0040 Validation

- Gate: `W3-BATCH-0040`
- Queue orders: `2341-2400`
- Touched rows: **60** (`广东 60`)
- Priority: `P1_IDENTITY` 60
- Fresh source identities researched: **32**
- Prior sealed evidence reused under exact repository ambiguity-group controls: **28**
- Evidence coverage: **60/60**
- Evidence grades: **A=57, B=3, C=0**
- Current organization + title confirmed: **10**
- No-current-role confirmed: **0**
- Explicit current-role unresolved: **50**
- Unsupported current-title claims: **0**
- Prior sealed logical ledger/overlay: **2340 rows**, queue `1-2340`, PASS at W3-BATCH-0039
- Appended result segment: **60 rows**, queue `2341-2400`
- Logical cumulative ledger after append: **2400 rows**, queue `1-2400` contiguous, no gap/overlap
- Logical cumulative overlay after append: **2400 rows**, queue `1-2400` contiguous, no gap/overlap

## Source-input control

- Google Drive membership baseline `名单汇总表_final.xlsx` was re-read as source input only.
- Local SHA-256 recheck: `86ada49718551b560cbb1385a5cd776db271b894d773bd7e643093e583648f3b` — exact match to repository-frozen source hash.
- Google Drive supplement `名单汇总表_补全单位.xlsx` was also re-read; local SHA-256 `136998b03210bd5144be16df3e964c64cae94581170268bc00764a041f596316` exactly matches repository truth.
- W1/W2 deterministic ordering was reconstructed from the frozen workbook and repository normalization/queue rules; queue `2341-2400` is exactly the next 60 Guangdong `P1_IDENTITY` records.
- No Google Drive artifact was used as control-state authority.

## Evidence / identity controls

- All 60 source rows are anchored to the official 全国工商联 `广东省工商联第十三届执委会名单`, with the广东省委统战部 official candidate roster used as an additional role/category identity surface.
- Fresh exact-name + 广东 + current-role searches were performed for the first **32** identities. The remaining **28** rows reuse SEALED/PASS outcomes only under exact `ambiguity_group_id + province + normalized name + blank region qualifier` controls; each source row retains its own `person_id`.
- **赖志光** is closed by the live 广东东升控股集团 enterprise leadership page, which states both his current `广东东升控股集团有限公司总裁` role and `广东省工商联常委` social duty.
- **王诗增** is closed by 2025 material explicitly identifying `广东省工商联常委、广东省福建商会理事长`, plus the Guangdong Fujian Chamber's 2026 official site confirming he remains `理事长`.
- **陈丹丹** is closed by 2026 广东两会 reporting directly identifying her as `广东省工商联常委、香港中国商会创会会长`.
- **周厚立** uses a 2024 direct identity bridge (`广东省工商联常委 + 中怡国际控股有限公司主席`) only for identity continuity; the current-title assertion comes from a 2026 report continuing to identify him as `中怡国际控股有限公司主席`.
- Reused current-role confirmations were rechecked against current primary sources for **冯日光、关向明、李红、陈丽文、梁耀铭、魏国华**.
- **陈丽文** is deliberately updated to her current 2026 government role `中共广东省委港澳工作办公室（广东省人民政府港澳事务办公室）主任`; the historical工商联 role is not carried forward as a current title.
- Plausible same-name/current-role hits for `蔡文贞、蔡永忠、马少福、廖伊曼、霍启山` and others were not promoted where the current source did not safely bridge back to the exact source identity.
- No current organization/title field is populated on an unresolved row.
- No identity was inferred from name alone.

## Deterministic hashes

- results raw SHA-256: `861fdff4a7a64d2c9bdfbd1f7c2c536f7d306f0eef533edc4de8b11ebfa03ff4`
- results gzip SHA-256: `4983821f11ca35a8d6d6d172b1289f3a31fadba28cb36a4dc990cfc77372cb27`
- research raw SHA-256: `1cd8916de29e543ee565415883bcd317f2fe495a7ffdf6fa9d8d27fc3c811272`
- research gzip SHA-256: `5603578e2f43b9a56967d66fa52db46bfc6106685b5562debc9fe729d62c0b5e`

**PASS**
