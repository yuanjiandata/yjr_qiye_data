# W3-BATCH-0083 Persistence Recovery Validation

- Exact queue coverage: `4921-4980`, 60 Shanghai P2 rows.
- INPUT was deterministically regenerated with the repository W1/W2 algorithms and frozen Drive inputs; SHA-256 matches the pre-failure target exactly: `ea7029eb6d6b07cbd05034a0e73f688bcdd95c0ea27614d663829922e4af2388`.
- Prior business outcome preserved: **15 CURRENT_ORG_TITLE_CONFIRMED / 45 UNRESOLVED_CURRENT_ORG_TITLE / 0 no-current / 0 unsupported claims**.
- The 45 unresolved rows were not re-searched.
- Targeted recovery was limited to the 15 previously confirmed queue orders: `4923,4929,4935,4937,4938,4944,4948,4952,4954,4963,4968,4969,4972,4974,4975`.
- Historical pre-failure RESULTS/RESEARCH SHA-256 values remain provenance targets only; their exact byte streams were never durably persisted, so the recovery bundle does not claim byte identity with them.
- Prior aggregate evidence grade A=54/B=6 is retained as historical business truth; missing prior per-row grade placement for unresolved rows is not invented.
- Shared CURRENT/STATUS/PROJECT_MANIFEST/W3_SEGMENT_INDEX projections are intentionally not rewritten because CONTROL V3 makes them non-blocking.

Result: **PASS / SEALED / PERSISTENCE_RECOVERY**.

Next gate: `W3-BATCH-0084`, queue order `4981`.
