# W3-BATCH-0028 Validation

- Gate: `W3-BATCH-0028`
- Input repository HEAD: `2e5e817fd854cd6816fef9e03848d33ec37a2afd`
- Queue orders: `1621-1680`
- Touched rows: **60** (`福建 25 / 江西 4 / 山东 2 / 河南 29`)
- Priority: `P1_IDENTITY` **60/60**
- Evidence or explicit unresolved reason: **60/60**
- Evidence grades: **A=42, B=18, C=0**
- Current organization + title confirmed: **28**
- Explicit current-role unresolved: **32**
- No-current-role confirmed: **0**
- Unsupported current-title claims: **0**

## Deterministic queue / identity controls

- The two frozen Google Drive inputs were re-read and their SHA-256 values matched repository `STATUS.yaml`.
- W1/W2 queue derivation reproduced exactly: `P0=101 / P1=4331 / P2=6045 / P3=167`; this Gate is the earliest unresolved deterministic range `1621-1680`.
- 25 福建 records reused already sealed evidence only after exact `ambiguity_group_id + province + normalized name + region qualifier` match; every source `person_id` remains distinct.
- 江西 `1646/1649` are literal source-label anomalies (`名单:`), not invented people. The two `万红梅` records remain distinct and unresolved.
- 山东 official roster contains two separate `王琳` vice-chair source records; they remain distinct and unresolved.
- 河南 confirmations require source/federation identity context plus current public evidence. Name-only hits were rejected, including conflicting `赵志军` candidates and unbridged `马文超` / `姜明` hits.
- 秦英林 was refreshed to `牧原食品股份有限公司 / 终身荣誉董事长`; the superseded `董事长/总裁` role was not carried forward after the 2026-06 transition.
- 薛景霞 was refreshed from the actual 2026-05 Beijing University HSBC Business School source as `河南康利达投资集团 / 董事长`; the source does not support narrowing that current claim to `康利达装饰股份有限公司`.

## Repository-native cumulative store

The W3 base ledger/overlay sealed by `W3-BATCH-0027` remains immutable at queue `1-1620`. Starting with this Gate, append-only result segments are indexed by `W3_SEGMENT_INDEX.csv`; `w3_segmented_store.py` projects each result segment into the logical ledger and overlay schemas.

- sealed base: `1-1620`
- `W3_BATCH_0028_RESULTS.csv.gz`: `1621-1680`
- logical cumulative range: **1-1680, contiguous, no overlap/gap**

This avoids any dependency on Remote Desktop or large-file server-side append while preserving deterministic repository truth.

## Hashes

- queue snapshot SHA-256: `b83487b20a0c9b3e7e2e624b4c2e1db1e64627901ffeb0f0693d50a6db4f40af`
- uncompressed results SHA-256: `159d306698dcfe6c8914d7ef0d8e2c81626f44effd11504472612191a8decd1e`
- compressed results SHA-256: `b4e78a78607a502d7248851f72f71aa4043df6896fd83bbf592ea29b841be620`
- uncompressed research SHA-256: `ce2e4306993406bc01c4a02ac4845d6f68803085f00da84f673157c6cfedadff`
- compressed research SHA-256: `bbd9d7330b0df47b46b6a58f4c104922bb62d77ebc44f2363910340b831d9864`

**PASS**
