---
title: "E0 — 测试床有效性 + KB 可得性(知识轨完整实验)"
date: 2026-07-07
stage: 1-directional
status: "E0 结论。boundary-clean。directional。"
---

> **LOG** — Stage-1 过程记录（hypothesis-grade），非现行真源；现行结论以 [[Decision-Log]] 与 [[Per-Work-Status]] 为准。

# E0 结论 —— 干净知识-RAG 测试床不在盘上,须构造

**核实过程:**
- **OpenbookQA-zh(唯一"理论上零构造干净"候选):盘上只有 QA parquet(id/source_wav/source_text=题+选项/target_text=答案),无 fact-book**;全盘 `find *fact* / *openbook*book*` 无命中。且 OpenbookQA-zh 在 **P2 基线饱和(greedy 0.973)** → 无知识 gap → 即便补事实也无 RAG 提升空间。
- **reading-comp 擦除诊断(bgpeaild9,audio-ASR query,擦除答案;40/60 partial,final 待):** base 0.25 · raw(不擦=泄漏)0.775 · **scrub(擦除=清白)0.20(< base)** · oracle_scrub 0.275 · asr_hit@k 0.82 · scrub_leak 0.03。→ **lookup 成分 = raw−scrub = +0.575;清白增益 ≈ 0(略负)。** 即 T7 的"RAG 增益"100% 是查答案;答案擦除后外部知识对冻结 omni **零推理增强**。
- 其余非饱和集(big-bench-audio 推理 / mmau 感知 / vocalbench-zh)是**推理/感知 gap 而非知识 gap**,且**无配套外部 KB**。

**结论(诚实):**
1. **盘上没有任何数据集能"零构造、边界干净地"测试"外部知识辅助冻结 omni 推理"。** reading-comp=查答案(擦除→null);OpenbookQA=饱和+无事实;其余=推理/感知 gap+无 KB;agentic=非知识检索轴。
2. **干净的知识-增强测试 = 绑定前提缺失**:需构造"事实-gap 口语 QA(omni 因缺事实而错)+ 边界干净外部 KB(不含答案)"。离线无现成来源(HF_HUB_OFFLINE;OpenbookQA 英文 fact-book 与 zh QA 不匹配)。
3. reading-comp 的清白结果本身是**有价值的负结论**:在冻结强 omni 上,把 passage(去掉答案后)当"知识"注入**不提升**——阅读理解式 RAG 的收益是"含答案"而非"知识辅助"。

**对 E1–E6 的影响:** E2 的"干净 H0"在现有数据(reading-comp)上=NULL;真正的知识-增强 headroom 须先 E1/E4 **构造**测试床才能测。TFRL 的**准确率**优化空间因此暂**无干净可测对象**;可干净测的 TFRL 价值转向**效率(何时检索)**(reward=模型置信,非 gold)。这些进入 E6 的诚实结论。
