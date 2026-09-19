# W3-BATCH-0008 Validation

Result: **PASS**

- Deterministic queue slice: 421–480 exactly, 60 江苏 P1_IDENTITY rows.
- Every touched row has public evidence or an explicit unresolved-current-role reason; unsupported current-title claims: 0.
- Current-state anchor: Jiangsu federation official roster labeled `2026年7月，共计121人`.
- 54 rows are directly present in that current roster; higher current roles supersede stale source labels. 徐志军 is now 副主席/省总商会副会长（兼）, not the old 秘书长 label.
- Three additional stale identities were closed with role-history bridges plus current official evidence: 王益冰→苏州市司法局党组书记、局长; 李兰翔→盐城市副市长; 李厚林→扬州市政协经济科技委员会主任.
- Three rows remain unresolved: 王红卫、孙振东、李建. They are absent from the current standing-committee roster and latest published executive roster; targeted search did not safely close identity/current role. The 江苏高院王红卫 homonym was explicitly rejected.
- Evidence grades: A=60, B=0, C=0; confirmed=57/60; unresolved=3/60.
- Cumulative evidence ledger and overlay each reconcile to 480 rows with queue_order 1..480 and no gaps.

Next deterministic gate: `W3-BATCH-0009`, starting queue_order 481.
