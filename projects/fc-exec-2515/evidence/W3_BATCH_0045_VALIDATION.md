# FC-EXEC-2515 W3-BATCH-0045 Validation

- Gate: `W3-BATCH-0045`
- Queue range: `2641-2700`
- Rows touched: `60`
- Provinces: 海南 `60`
- Priority: `P1_IDENTITY` only
- Result: **PASS**

## Deterministic checks

- Repository truth was read first at input HEAD `15d4e784f2ba0707e7cc480d7c0e67d69b078a98`: `W3-BATCH-0044` is `SEALED/PASS` and `W3-BATCH-0045` is the sole `READY` NORMAL gate.
- Queue order is exactly contiguous `2641..2700`.
- Person IDs, normalized names, provinces and ambiguity-group IDs match the deterministic W2 queue slice reconstructed from the frozen source contract.
- Google Drive membership source SHA-256 rechecked: `86ada49718551b560cbb1385a5cd776db271b894d773bd7e643093e583648f3b`.
- Google Drive supplement source SHA-256 rechecked: `136998b03210bd5144be16df3e964c64cae94581170268bc00764a041f596316`.
- Every touched row has either a supported current organization/title claim or an explicit unresolved reason.
- No result uses name-only identity inference.
- `35` rows reuse only prior `SEALED/PASS` outcomes under exact `ambiguity_group_id + province + normalized_name`; distinct `person_id` values remain distinct.
- `25` rows received fresh public-evidence research after official ACFIC Hainan ninth executive-committee identity anchoring.
- Fresh current-role confirmations are limited to four rows with an additional identity bridge: 林明宁、周勤富、钟宇光、符曜. Other fresh rows without a sufficient current identity bridge remain explicitly unresolved.
- The two source rows named 王斌 remain separate and unresolved; no same-name collapse is performed.
- Confirmed current organization/title rows: `18`.
- Explicit unresolved rows: `42`.
- Evidence grades: `A=50`, `B=10`, `C=0`.
- Unsupported current-title claims: `0`.
- Segmented ledger/overlay logical coverage after this gate: `1-2700`, no gap and no overlap.
- Results SHA-256: `6c2f45567d33741a59ec4cf8759c912a3b8380597fe7b546a189be7cc1e75b38`.
- Research SHA-256: `f1703897e4c4a08fc1652fa623948dbcbc749a9404a12eb3766f3337bc558f34`.

## Outcome

`W3-BATCH-0045` is deterministically sealed. The next valid NORMAL gate is `W3-BATCH-0046`, beginning at queue order `2701`.
