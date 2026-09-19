# W2-EXISTING-ABSORB Validation

## INPUT
- W1 canonical roster: **10,644** person records.
- Existing consolidated source: `名单汇总表_补全单位.xlsx` (`10Zc9caTUy4eJITc802cisKSCQhuOJsEp`), SHA-256 `136998b03210bd5144be16df3e964c64cae94581170268bc00764a041f596316`.
- Frozen baseline source values already carried by W1 from `名单汇总表_final.xlsx`.
- Province-level source folder remains upstream provenance inventory; this gate uses the consolidated 31-sheet workbooks to avoid duplicating the same derivative rows.

## WORK
- Preserved all W1 person IDs and source-row provenance.
- Preferred already-separated organization/title values from the frozen final workbook.
- Filled missing values from the 31-sheet supplement only through deterministic province + canonical federation role + normalized-name matching.
- For duplicated keys, absorption occurs only when W1 and supplement group cardinality is identical, preserving source order; mismatched groups are not guessed.
- Split combined supplement values only when a recognized title suffix is explicitly separated by whitespace; otherwise preserved the whole source value as organization rather than inventing a title.
- Classified only obvious federation staff and enterprise/entrepreneur candidates. No person is marked confirmed entrepreneur in W2.
- Generated a deterministic unresolved/current-verification queue for W3.

## VALIDATION
- Output records: **10644 / 10,644**, unique person IDs **10644**.
- Records with non-placeholder organization absorbed: **507**.
- Records with title absorbed: **177**.
- Evidence ledger rows: **507**, all with source file ID/file/sheet/row provenance.
- Entrepreneur candidates from existing source only: **418**; confirmed entrepreneurs: **0**.
- Unresolved/current identity queue rows: **10644**, all with explicit reason and deterministic priority/order.
- Source-name anomalies remain unresolved; same-name groups are not merged or externally resolved in this gate.

## RESULT
**PASS / SEALED** — existing source values are absorbed without unsupported identity or current-employment claims.

## NEXT_GATE
`W3-EVIDENCE-ENRICH`
