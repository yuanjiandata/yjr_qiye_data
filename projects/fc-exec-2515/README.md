# FC-EXEC-2515-01

31省工商联执委全名单企业任职核验工程。

## 目标

以 Google Drive「2515各省工商联」中的31省名单为输入，逐人核验当前单位与当前单位职务，并重点识别企业家，最终形成可追溯的人员主表、企业家表、省份统计、冲突/未核验表和证据台账。

## RGAC 运行纪律

- Repository main HEAD 是项目状态真源。
- Google Drive 是原始输入源，不是状态控制面。
- 每次自动运行最多完成一个完整 Gate。
- 每次运行先读取本目录 STATUS / CURRENT / PROJECT_MANIFEST。
- 若 prompt 与仓库状态冲突，以仓库为准。
- Gate PASS 才允许提交并推进 next_gate。
- W3/W4/W5 是可重复批次 Gate，按确定性队列向前推进。
- 不使用 Make、飞书、外部 Spreadsheet 作为控制状态。
- 遇到真正的人类决策门、高风险/不可逆行为或宏项目完成则停止自动续跑。

## 当前入口

W0-SOURCE-FREEZE
