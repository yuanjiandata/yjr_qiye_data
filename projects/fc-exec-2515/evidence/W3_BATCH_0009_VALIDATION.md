# W3-BATCH-0009 Validation

Result: **PASS**

- Deterministic queue slice: 481–540 exactly, 60 江苏 P1_IDENTITY rows.
- Every touched row has public evidence or an explicit unresolved-current-role reason; unsupported current-title claims: 0.
- Current-state anchor: Jiangsu federation official roster labeled `2026年9月，共计120人`, superseding the July roster used by the prior batch.
- 52 rows are directly present in that latest roster and receive their current federation/chamber role from the official page.
- Three stale federation identities are closed by role-history bridge plus current A-grade official evidence: 陈湘珍→盐城市台办主任; 施勇→淮安市委统战部常务副部长/市社会主义学院院长; 顾万峰→江苏省委统战部常务副部长.
- 钟雨 is separately resolved as `NO_CURRENT_ROLE_CONFIRMED`: 2025 official Jiangsu evidence identifies him as 洋河党委副书记、总裁, while the reproduced listed-company announcement 2026-003 states that he retired and resigned all company roles and would hold no role in the company or controlled subsidiaries. No new employer/title is inferred.
- Four rows remain unresolved: 张惠扬、陈军、周洁、查艳. They are absent from the Sep-2026 roster and targeted search did not safely close a present role without name-only inference.
- Evidence grades: A=59, B=1, C=0; current organization/title confirmed=55/60; no-current-role confirmed=1/60; unresolved=4/60.
- Cumulative evidence ledger and verification overlay each reconcile to 540 rows with queue_order 1..540 and no gaps or duplicate queue orders.

Next deterministic gate: `W3-BATCH-0010`, starting queue_order 541.
