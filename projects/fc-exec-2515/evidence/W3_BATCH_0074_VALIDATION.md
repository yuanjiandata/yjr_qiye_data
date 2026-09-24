# W3-BATCH-0074 Validation

**Project:** FC-EXEC-2515-01  
**Gate:** W3-BATCH-0074  
**Result:** PASS

## Deterministic checks

- Input repository truth: `main` = `8e0dea7fea770e629a18e382e2a3f6beca907b40`; latest sealed gate was W3-BATCH-0073 and W3-BATCH-0074 was the sole READY gate.
- Google Drive source inputs were re-read. SHA-256 matched the repository-frozen values:
  - `名单汇总表_final.xlsx` = `86ada49718551b560cbb1385a5cd776db271b894d773bd7e643093e583648f3b`
  - `名单汇总表_补全单位.xlsx` = `136998b03210bd5144be16df3e964c64cae94581170268bc00764a041f596316`
- Queue coverage is exact and contiguous: 4381-4440, 60 rows, no duplicates or omissions.
- Provinces: 宁夏 36, 新疆 16, 北京 8.
- Prior SEALED/PASS reuse: 36 rows. Each reuse is constrained by exact `province + name_normalized + ambiguity_group_id`.
- Fresh public-evidence research: 15 rows. One literal `暂未公开` source placeholder was reviewed without inventing a person identity.
- Same-batch reuse: 8 rows, each constrained by the same exact identity-group tuple.
- Priority transition: 52 P1 rows were processed, closing P1 at 4331/4331; 8 P2 rows were processed.
- Result statuses: 19 `CURRENT_ORG_TITLE_CONFIRMED`, 41 explicit `UNRESOLVED_CURRENT_ORG_TITLE`, 0 unsupported title claims.
- Evidence grades: A=50, B=8, C=2.
- Confirmed rows all contain organization, title, and provenance URL. Unresolved rows all contain an explicit reason.
- Public hits that lacked a safe source-person identity bridge were preserved as unresolved; no name-only identity inference was used.
- Result SHA-256: `73f64e981ccc193aca9bf121b6ff4844590daf50968a4f9f478024c665dac375`.
- Research TSV.GZ SHA-256: `d955d212e19db841307db98758ee1cd57a86ed5e2ded391014bf054dadb90b23`.
- Segmented store appends ordinal 47 for both ledger and overlay, preserving continuous logical coverage through queue 4440.
- Control state advances only to W3-BATCH-0075 READY at queue 4441. Macro lifecycle remains ACTIVE and blocker remains null.

## Gate decision

PASS / SEALED.
