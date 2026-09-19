# W3-BATCH-0007 Validation

Result: **PASS**

- Deterministic queue slice: 361–420 exactly, 60 rows; 7 吉林 + 53 江苏, all P1_IDENTITY.
- Every touched row has public evidence or an explicit unresolved-current-role reason.
- Latest repository-defined source identities were reconciled against public current evidence; no identity was inferred from name alone.
- The official Jiangsu federation page is currently labeled `2026年7月，共计121人` and was used as the current-state authority for Jiangsu federation/chamber roles.
- 47/53 Jiangsu rows are present in that latest official roster and received a current federation/chamber organization + title; 6 rows (郭东升 x2, 熊杰 x2, 顾万峰, 李兰翔) remain unresolved because the stale source role is not supported by the latest official roster.
- 顾万峰 was not carried forward as 常务副主席: the July 2026 official roster names 刘军 as current 常务副主席.
- 吉林 current roles were refreshed with 2026 evidence; 李维斗、唐庆会、吕兵 reuse prior sealed current evidence, while 徐朝春、李武华 use fresh 2026 sources and source-role cross-listing without person_id merge.
- Evidence grades in batch: A=55, B=5; C=0.
- Current organization + title confirmed: 54/60.
- Current-role unresolved: 6/60; unresolved organization/title fields remain blank rather than guessed.
- Cumulative W3 evidence ledger and verification overlay each reconcile to 420 rows with queue_order 1..420 and no gaps.
- Unsupported current-title claims: 0.

Next deterministic gate: `W3-BATCH-0008`, starting queue_order 421.
