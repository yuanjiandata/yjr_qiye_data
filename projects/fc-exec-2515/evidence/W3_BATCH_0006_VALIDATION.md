# W3-BATCH-0006 Validation

Result: **PASS**

- Deterministic queue slice: 301–360 exactly, 60 rows; 57 河北 + 3 吉林, all P1_IDENTITY.
- Every touched row has public evidence or an explicit unresolved-current-role reason.
- No current organization/title was assigned from a name-only hit.
- 18 current-role results reuse prior sealed evidence only where the same Hebei official federation roster cross-lists the identical person under an earlier role and 执委; person_ids remain separate.
- Fresh current-role evidence was added for 张志祥、周超男、霍占利、魏立华、魏海金、李维斗、唐庆会、吕兵.
- 吉林 rows use 2026 public evidence for current provincial federation leadership; no stale carry-forward was used.
- Evidence grades in batch: A=48, B=12; C=0.
- Current organization + title confirmed: 26/60.
- Current-role unresolved: 34/60; unresolved organization/title fields remain blank rather than guessed.
- Cumulative W3 evidence ledger reconciles to 360 rows with queue_order 1..360 and no gaps.
- Unsupported current-title claims: 0.

Next deterministic gate: `W3-BATCH-0007`, starting queue_order 361.
