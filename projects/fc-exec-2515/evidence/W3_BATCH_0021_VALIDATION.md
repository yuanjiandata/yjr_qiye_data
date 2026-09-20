# W3-BATCH-0021 Validation

- Gate: `W3-BATCH-0021`
- Queue orders: `1201-1260`
- Touched rows: **60** (`安徽 34`, `福建 26`)
- Priority: `P1_IDENTITY` 60
- Evidence coverage: **60/60**
- Evidence grades: **A=51, B=9, C=0**
- Current organization + title confirmed: **40**
- Explicit current-role unresolved: **20**
- Unsupported current-title claims: **0**
- Cumulative evidence ledger: **1260 rows**, queue `1-1260` contiguous, no duplicate queue order
- Cumulative verification overlay: **1260 rows**, queue `1-1260` contiguous, no duplicate queue order

## Identity / recency controls

- 34 安徽 rows are repository-encoded cross-list identities and reuse already sealed evidence only when `ambiguity_group_id + province + normalized name` all match; each source row retains its own `person_id`.
- All 26 福建 first-occurrence identities were researched against current public government/federation/enterprise/filing or authoritative-media evidence, with the 2022 official 福建省工商联 roster used only as the historical identity anchor.
- 20 福建 rows obtained a safe current-role closure; six (林湫、郑辉、郑玉琳、施天佑、洪杰、傅芬芳) remain explicit unresolved because the current identity bridge was not strong enough or the legal-entity/role chain changed.
- Stale source roles were not carried forward: 黄世霖 is refreshed from old 宁德时代副董事长 to current 福建时代星云科技有限公司董事长; 蔡劲军 is refreshed to current 火炬电子董事长; 邹剑寒 is refreshed to current 奥佳华董事长、总经理.
- No current organization/title is assigned from a name-only hit.

**PASS**
