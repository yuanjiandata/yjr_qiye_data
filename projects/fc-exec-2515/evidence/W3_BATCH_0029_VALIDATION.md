# W3-BATCH-0029 Validation

- Gate: `W3-BATCH-0029`
- Input repository HEAD: `77576645e241d19a14303f01b62923d5b0f1b00e`
- Queue orders: `1681-1740`
- Touched rows: **60** (`河南 60`)
- Priority: `P1_IDENTITY` **60/60**
- Distinct source identities researched: **52**
- Same-batch exact ambiguity-group reuse rows: **8**
- Evidence or explicit unresolved reason: **60/60**
- Evidence grades: **A=49, B=11, C=0**
- Current organization + title confirmed: **21**
- Explicit current-role unresolved: **39**
- No-current-role confirmed: **0**
- Unsupported current-title claims: **0**

## Deterministic source / queue controls

- Google Drive `名单汇总表_final.xlsx` re-read SHA-256 = `86ada49718551b560cbb1385a5cd776db271b894d773bd7e643093e583648f3b`, exactly matching repository `STATUS.yaml`.
- Google Drive `名单汇总表_补全单位.xlsx` re-read SHA-256 = `136998b03210bd5144be16df3e964c64cae94581170268bc00764a041f596316`, exactly matching repository `STATUS.yaml`.
- W1 normalization was independently reproduced from the frozen source: canonical persons `10644`, severe source-name exceptions `101`, same-name ambiguity groups `1913`, ambiguity-member rows `4331`.
- Therefore the earliest deterministic P1 range after sealed cursor 1680 is exactly `1681-1740`, all 河南.
- The 2022 全国工商联河南换届名单 is used only as the historical/source identity anchor. Current organization/title claims require a newer public source plus province/federation/organization/gender context; no name-only assignment is permitted.
- Eight later source rows in this batch reuse an earlier result in the same batch only when `province + normalized name + ambiguity_group_id` are identical; every `person_id` remains distinct.

## Current-role controls

Safe current closures include 石从亮、平本强、乔松涛、刘文新、李静敏、张付峰、薛亚辉、马文超、王爽、王幸福、王若飞、王新奇、李本磊、李圆方、连建伟、吴鹏斐. Repeated source rows for 石从亮、平本强、乔松涛、刘文新、李静敏 reuse those same-batch conclusions without merging source identities.

Fail-closed examples:
- 郭伟 source identity is explicitly female; current male homonym hits were rejected.
- 刘硕 has a plausible 2026 listed-company hit, but no safe bridge to the 河南省工商联常委 source identity, so no current role is written.
- 任平、王永利 source records carry female qualifiers; ambiguous current same-name hits without a reliable gender/source bridge are rejected.
- 陈占亭 has historical/2025 secretary-general evidence but the provincial federation leadership changed in 2026; absent a sufficiently current direct role source, the record remains unresolved.
- 李芳、张传兵、郭启文 have strong older role evidence but insufficiently fresh 2026 proof for current-role promotion in this Gate.
- 宋占锋 has a current 浙江河南商会 homonym hit but no safe bridge to the 河南省工商联常委 source identity.

## Repository-native cumulative store

The sealed base remains immutable at queue `1-1620`; result segments remain append-only:

- sealed base: `1-1620`
- `W3_BATCH_0028_RESULTS.csv.gz`: `1621-1680`
- `W3_BATCH_0029_RESULTS.csv.gz`: `1681-1740`
- logical cumulative range: **1-1740, contiguous, no overlap/gap**

`W3_SEGMENT_INDEX.csv` remains the cumulative storage authority and `w3_segmented_store.py` projects result segments into logical ledger/overlay schemas.

## Hashes

- queue snapshot SHA-256: `fa8b33ced6857457aa00ff4dac3b12e6119bab9fde9961d66032437cefed9248`
- uncompressed results SHA-256: `9167d2db944582487f25927ceb6ecad668ea61ebd16d2feaa69b97c741087ac1`
- compressed results SHA-256: `d2d78f3928aee4f268fbec51a41a2aae3db112b77b592b8f9d16d3907da3bf9a`
- uncompressed research SHA-256: `a5d842e14fb7247905f38f533f4e2b0c3be76ef2ee026d3b5a1c957c8d6f5514`
- compressed research SHA-256: `948d2ec9fc583d503830b69984f7aa1518358d11d27d066e447772cfed472d9a`

**PASS**
