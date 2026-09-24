# W3-BATCH-0076 Validation

**Project:** FC-EXEC-2515-01  
**Gate:** W3-BATCH-0076  
**Result:** PASS

## Deterministic checks

- Input repository truth: `main` = `58950d59d1faa739feff77395ffc0673e055615f`; latest sealed gate was W3-BATCH-0075 and W3-BATCH-0076 was the sole READY gate.
- Google Drive source inputs were re-read. SHA-256 matched the repository-frozen values:
  - `名单汇总表_final.xlsx` = `86ada49718551b560cbb1385a5cd776db271b894d773bd7e643093e583648f3b`
  - `名单汇总表_补全单位.xlsx` = `136998b03210bd5144be16df3e964c64cae94581170268bc00764a041f596316`
- Queue coverage is exact and contiguous: 4501-4560, 60 rows, no duplicates or omissions.
- Province and priority: 北京 60; all 60 are `P2_ORG_TITLE_LOOKUP`.
- Fresh public-evidence research: 60 rows. The official ACFIC Beijing 15th executive-committee roster anchors every source person; current public evidence was evaluated row by row.
- Result statuses: 9 `CURRENT_ORG_TITLE_CONFIRMED`, 0 `NO_CURRENT_ROLE_CONFIRMED`, 51 explicit `UNRESOLVED_CURRENT_ORG_TITLE`.
- Current organization/title confirmations closed: 梁雪青、林航、林余存、马春秀、沈鹏、宋玫、许泽玮、易月明、张剑辉.
- Evidence grades: A=57, B=3, C=0.
- Confirmed rows contain organization, title, current provenance URL, and a safe identity bridge. Unresolved rows contain an explicit reason.
- Current same-name hits, current roles without a safe source-person bridge, and stale/insufficient public evidence were preserved as unresolved; no name-only identity inference was used.
- Unsupported current-title claims remain zero.
- Result SHA-256: `22f3213ca47d6f0a37357d6cd754721298e62009bd497a7dd20ac306c1f2d64b`.
- Research TSV.GZ SHA-256: `effec1ce5696869ce99498716677cdcaaaf2b4006069155ffe90467faeb0321e`.
- Segmented store appends ordinal 49 for both ledger and overlay, preserving continuous logical coverage through queue 4560.
- Control state advances only to W3-BATCH-0077 READY at queue 4561. Macro lifecycle remains ACTIVE and blocker remains null.

## Gate decision

PASS / SEALED.
