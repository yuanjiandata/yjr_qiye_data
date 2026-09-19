# W1-PERSON-NORMALIZE Validation

## INPUT
- Repo truth at run start: `main@8f1139a125266a042c05eba9b8e106a713836dcb`
- Frozen source workbook: `名单汇总表_final.xlsx` (`1jlNP_ENJzQgBsMgZ2bwR6ZoiUdNZhqzR`)
- SHA-256: `86ada49718551b560cbb1385a5cd776db271b894d773bd7e643093e583648f3b`

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
