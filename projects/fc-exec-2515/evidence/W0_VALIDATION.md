# W0-SOURCE-FREEZE Validation

## INPUT

- Repository truth at run start: `main@b76689042d992ce15ecac9da9c8125db93364ff8`
- Google Drive root: `2515各省工商联` (`15PUQLLT9IXVQOeTvyFPop4e4EgUbIm8i`)
- Frozen raw membership workbook: `名单汇总表_final.xlsx` (`1jlNP_ENJzQgBsMgZ2bwR6ZoiUdNZhqzR`)
- Workbook SHA-256: `86ada49718551b560cbb1385a5cd776db271b894d773bd7e643093e583648f3b`

## WORK

1. Read repository `STATUS.yaml`, `CURRENT.yaml`, and `PROJECT_MANIFEST.yaml`.
2. Inventoried Drive root plus `各省` and `各省独立`.
3. Parsed every physical row after the header across all 31 sheets of the frozen membership workbook.
4. Preserved source identity by the deterministic locator: `file_id + sheet + excel_row`.
5. Computed per-sheet row-stream SHA-256 hashes and row counts.
6. Classified `各省` files as enrichment/reference inputs rather than the membership baseline.

## VALIDATION

- Province-level sheets: **31**
- Physical rows after headers: **10,762**
- Non-empty rows: **10,744**
- Rows with a non-empty name: **10,743**
- Blank rows retained by source row number: **18**
- Non-empty row without a name: **1** — `西藏!3`, raw role value `不需要`
- Named-populated province sheets: **30**
- `西藏` named rows: **0**
- `各省` folder child items: **34**
- Canonical province final files in `各省`: **28**
- Canonical province files absent from `各省`: **黑龙江、云南、西藏**
- Fallback files present in `各省独立`: **黑龙江.xlsx、云南.xlsx**
- No standalone Tibet file was found in `各省独立`.

The 31-sheet frozen workbook accounts for all province-level scopes. Missing/placeholder conditions are explicit; no rows were silently dropped. Per-sheet hashes are recorded in `W0_BASELINE.csv`.

## RESULT

**PASS / SEALED**

W0 source truth is frozen. Downstream transforms must not use a stale chat count or the directory name `2515` as the population count.

## NEXT_GATE

`W1-PERSON-NORMALIZE`
