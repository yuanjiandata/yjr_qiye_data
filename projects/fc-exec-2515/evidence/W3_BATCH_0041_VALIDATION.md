# W3-BATCH-0041 Validation

- Gate: `W3-BATCH-0041`
- Queue orders: `2401-2460`
- Touched rows: **60** (`广东 60`)
- Priority: `P1_IDENTITY` 60
- Fresh source identities researched: **60**
- Prior sealed evidence reused: **0**
- Evidence coverage: **60/60**
- Evidence grades: **A=55, B=5, C=0**
- Current organization + title confirmed: **10**
- No-current-role confirmed: **0**
- Explicit current-role unresolved: **50**
- Unsupported current-title claims: **0**
- Prior sealed logical ledger/overlay: **2400 rows**, queue `1-2400`, PASS at W3-BATCH-0040
- Appended result segment: **60 rows**, queue `2401-2460`
- Logical cumulative ledger after append: **2460 rows**, queue `1-2460` contiguous, no gap/overlap
- Logical cumulative overlay after append: **2460 rows**, queue `1-2460` contiguous, no gap/overlap

## Source-input control

- Google Drive membership baseline `名单汇总表_final.xlsx` was re-read as source input only.
- Local SHA-256 recheck: `86ada49718551b560cbb1385a5cd776db271b894d773bd7e643093e583648f3b` — exact match to repository-frozen source hash.
- Google Drive supplement `名单汇总表_补全单位.xlsx` was also re-read.
- Local SHA-256 recheck: `136998b03210bd5144be16df3e964c64cae94581170268bc00764a041f596316` — exact match to repository truth.
- W1/W2 deterministic ordering was reconstructed from the frozen workbook and repository normalization/queue rules; queue `2401-2460` is exactly the next 60 Guangdong `P1_IDENTITY` records.
- No Google Drive artifact was used as control-state authority.

## Evidence / identity controls

- All 60 source rows are anchored to the official 全国工商联 `广东省工商联第十三届执委会名单` (`2022-09-19`).
- Fresh exact-name + 广东省工商联 + 2026 current-role research was performed for all **60** source identities.
- **陈志列**: 2026-01 Guangdong United Front material directly identifies `广东省工商联主席` and `研祥高科技控股集团董事局主席`.
- **郑文强**: 2026 current materials bridge `广东省工商联合会常委` → `横琴工商联主席` → `珠海市新东升集团有限公司董事长`; current company/title is accepted only through that two-source role bridge.
- **董凡**: 2026 material directly identifies `广东省工商联副主席、珠海市工商联主席、健帆生物科技集团股份有限公司董事长、总裁`.
- **李连柱**: 汕头市工商联 2026-04 official material directly identifies `省工商联副主席、佛山市工商联主席、尚品宅配集团董事长`.
- **廖平元**: 2026 Guangdong two-sessions reporting directly identifies `省工商联副主席、梅州市工商联主席、广东嘉元科技股份有限公司董事长`.
- **吴丰礼**: 2026 current reporting/announcement evidence identifies `广东省工商联常委` and `广东拓斯达科技股份有限公司董事长兼总裁`.
- **张燕航**: 中山市工商联 current leadership page directly identifies `广东省工商联第十三届执委会副会长` and `广东毅马集团有限公司董事长`.
- **李积回**: 阳江市政府 2026-04 official material directly identifies `广东省总商会副会长、阳江十八子集团有限公司董事、总经理`.
- **林水栖**: 2026 two-sessions reporting directly identifies `广东省工商联副主席、广东金岭糖业集团有限公司董事长`.
- **王明旺**: 2026 material identifies `省总商会副会长、茂名市工商联主席、欣旺达创始人`; the result deliberately records `创始人` rather than carrying forward historical chairman/general-manager roles.
- **刘文华** stays unresolved because current public results contain materially different same-name identities (including a federation official and a university president).
- **陈涛** stays unresolved because current high-profile same-name government results do not safely bridge to this source federation identity.
- **黄达昌、覃九三、马学沛、叶远璋、吴启超、万国江** and other plausible company/current-role hits remain unresolved where no safe source-identity bridge was found.
- No current organization/title field is populated on an unresolved row.
- No identity was inferred from name alone.

## Deterministic hashes

- results raw SHA-256: `83442766167ec90a516ba682e32b50693e60ebe2a84212ed0dc07b76d28ef632`
- results gzip SHA-256: `702d035845e4a1054e509b8f4eb8d3a813e6e87d93c32a485a7e47c42bdeaff8`
- research raw SHA-256: `c8e495c16bd207f1dec636959b9c7c7fe0cfc3798e38dc8f1be1acab3aec872f`
- research gzip SHA-256: `5641e9edee639ff36c3a221c538bf3da0eb3029d4c1f8751440b294abe4b706d`

**PASS**
