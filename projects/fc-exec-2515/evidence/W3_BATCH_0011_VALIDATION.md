# W3-BATCH-0011 Validation

Result: **PASS**

- Deterministic queue slice: 601–660 exactly, 60 江苏 P1_IDENTITY rows.
- Every touched row has public evidence or an explicit unresolved-current-role reason; unsupported current-title claims: 0.
- 47 rows are closed from the live official Jiangsu standing-committee roster labeled `2026年9月，共计120人`, with higher current federation/chamber roles preferred over stale source `执委` labels.
- Four additional current roles are safely closed through role-history bridges: 李兰翔→盐城市副市长, 李厚林→扬州市政协经济科技委员会主任, 陈湘珍→盐城市台办主任, 施勇→淮安市委统战部常务副部长/市社会主义学院院长.
- 钟雨 is evidence-resolved as `NO_CURRENT_ROLE_CONFIRMED` using the original CNINFO listed-company filing (公告编号 2026-003), which records retirement and resignation from all 洋河股份/company-subsidiary roles.
- Eight rows remain explicit current-role unresolved: 孙振东、李建、张飞×2、张惠扬、陈军、周洁、查艳. The two 张飞 rows are repository exact-value duplicate candidates (EDG-0001); the current official roster distinguishes 淮/盐 identities, so person_id-level assignment would be arbitrary and is not made.
- Evidence grades: A=60, B=0, C=0; current organization/title confirmed=51/60; no-current-role confirmed=1/60; unresolved=8/60.
- Cumulative evidence ledger and verification overlay each reconcile to 660 rows with queue_order 1..660, no gaps and no duplicate queue orders.

Next deterministic gate: `W3-BATCH-0012`, starting queue_order 661.
