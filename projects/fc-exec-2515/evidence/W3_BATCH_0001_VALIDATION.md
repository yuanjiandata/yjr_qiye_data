# W3-BATCH-0001 Validation

## Result

**PASS**

This batch processed exactly queue orders **1–60**, the maximum allowed batch size for W3.

## Why this batch is identity-first

All 60 selected queue rows are `P0_NAME_REPAIR` records. Their canonical `person_id` is currently attached to a malformed physical source row: a split name fragment, a shifted boundary, or a compound row containing multiple people. Writing a current organization/title onto those canonical IDs before repairing the identity boundary would risk cross-person contamination.

Therefore this Gate performed the prerequisite W3 evidence work: re-read the deterministic W2 queue; inspected adjacent source rows; checked the corresponding official ACFIC provincial committee rosters; recorded evidence-backed identity candidates/fragment relationships; made zero unsupported current organization/title claims; and marked every touched row with `DEFERRED_CANONICAL_IDENTITY_REPAIR_REQUIRED`.

These 60 rows are now processed for the W3 active queue and are carried as structural identity conflicts for later canonical split/merge resolution. They must not be silently treated as verified current employment records.

## Evidence coverage

- Zhejiang: 22 rows — ACFIC official roster dated 2022-09-19.
- Anhui: 27 rows — ACFIC official roster dated 2022-08-12.
- Henan: 11 rows — ACFIC official roster dated 2022-08-29.
- A-grade identity evidence: **60/60**
- Explicit unresolved current org/title reason: **60/60**
- Current organization/title confirmations: **0**
- Unsupported current-title claims: **0**

## Deterministic checks

- queue orders are unique and exactly 1–60;
- person IDs are unique across touched rows;
- all rows have A-grade official federation evidence;
- all rows have a non-empty unresolved reason;
- current organization and current title fields are blank for all 60 rows;
- no identity was inferred from name alone;
- next deterministic queue order is 61.

## Next Gate

`W3-BATCH-0002`, starting at queue order 61.
