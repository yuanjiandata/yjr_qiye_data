# W3-BATCH-0068 Validation

- Gate: `W3-BATCH-0068`
- Parent HEAD: `6c48f2955c21faa6e375ca0169c6b2c5b0206a22`
- Queue slice: `4021-4080` (60 rows)
- Province: 内蒙古 16 / 广西 44
- Priority: P1_IDENTITY 60
- Google Drive membership SHA-256: `86ada49718551b560cbb1385a5cd776db271b894d773bd7e643093e583648f3b` — PASS
- Google Drive supplement SHA-256: `136998b03210bd5144be16df3e964c64cae94581170268bc00764a041f596316` — PASS
- Prior SEALED/PASS exact-group reuse: 16
- Fresh public-evidence research: 44
- Result: confirmed 15 / unresolved 45
- Evidence grades: A=52 / B=8 / C=0
- Unsupported current-title claims: 0
- Segment continuity after append: 1-4080, no gap / no overlap

For 内蒙古, all 16 rows had an earlier SEALED/PASS row in the same exact `ambiguity_group_id + province + normalized_name` identity group, so the gate reused those outcomes with explicit source-gate/source-queue provenance.

For 广西, the nationwide federation's official 13th executive-committee roster was used as the source-person identity anchor and every one of the 44 rows received a fresh current-web research pass. Current organization/title was closed only where 2026 evidence provided sufficient province/role/business context beyond a bare name match. Examples closed in this gate include 眭国华, 蔡家东, 邓永源, 邓秀汕, 杨英, 丁文博, 林伟民, 周文皓, and 莫金枝. Rows without a safe current identity bridge remain explicit unresolved. 韦永山 remains unresolved for September-current status because the 2026-05-29 disciplinary announcement supplies a then-current union role but no later post-investigation role confirmation was found.

## Deterministic acceptance

PASS. Every touched row is either backed by an exact sealed-evidence reuse chain or by a fresh public-evidence research record with an official federation identity anchor and explicit decision. Frozen source hashes match repository truth, no unsupported current-title claim was introduced, and the segmented ledger/overlay advances contiguously to queue order 4080.
