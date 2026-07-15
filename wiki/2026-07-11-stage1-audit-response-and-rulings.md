---
title: "Stage-1 对抗审计的核验、答复与 owner 裁定（G0 claim tree）"
date: 2026-07-11
stage: 1-problem-definition
status: "owner 已裁定（四项全签）；本文 = G0 gate 交付物"
responds-to: "2026-07-10-stage1-adversarial-research-audit.md"
---

# 2026-07-11 · 审计答复与裁定（G0）

> **性质**：对外部审计（`2026-07-10-stage1-adversarial-research-audit.md`，Codex 会话出具）的
> 逐条核验、批判性答复与 owner 裁定记录。核验 = 6 个 Opus 对抗核验代理对照当前 HEAD 逐条重验
> （实跑 dry-run、重算重叠率、逐行读 Lean）。**本文同时是审计 G0 gate 要求的 claim tree 签署页。**

## 1. 核验结论：审计事实层面几乎全对

34 项事实性主张核验结果：**32 CONFIRMED / 1 STALE / 1 PARTIAL / 0 REFUTED**。

| 主张簇 | 判定 | 要点 |
|---|---|---|
| Step-2 Phase-A 不可执行（R2-P0） | 7/7 CONFIRMED，整体可执行性 REFUTED | 无 `--execute` 路径；runner/builder source 命名 4 vs 3 字段错配；`qwen3-omni-hidden` vs `qwen3-omni-own` token 错配；6 臂 PLAN ONLY；kb_batch_build 只建单 utt 键单 value。**比审计更糟**：`_query_embedder` 的 auto 回退使 GLAP/LCO/MERaLiON/qwen3-omni-own 查询全落 CLAP（512-d 打 1024/2048-d 索引）——**连 ref-config 锚点格都检索不通** |
| W1 best-of-N（R2-P1） | 6/6 CONFIRMED | oracle +0.0418 CI 不跨 0 vs MBR +0.0037 CI 跨 0（n.s.）；宏平均 WER 非 corpus WER；种子混杂数据/生成方差；**多样性坍塌：8 池均 4.19 个不同候选、14.6% 八条全同**；单一采样配置；音频路径上游实验性无 parity check |
| W4 CREMA-D（R1） | 6 CONFIRMED + 1 STALE | 自定判据 `A_t(e_t)>A_t(e_t')` 未过而文档写 "thesis holds"；content=12 句固定句 ID（精确复算 12 句码）；切分 91/91 说话人、827/827 (speaker,sentence) 对全跨；5 种子切片重叠 16.0–21.3%（精确复算吻合）。STALE：手工转录 headline——07-01 `cdbf1d2` 已修为脚本原子产出 |
| Lean 定理域（R3-P0） | 8/8 CONFIRMED | 每条定理的承重前提（单调有界/δ>0/τ_n→0/reach 上界）均为外部假设；operator-linked 定理数=0；`beirami_thm_3_1` 为具名公理非形式化成果；sorry=0 属实。docstring 均自我披露——诚实，但"系统收敛已被 Lean 证明"不可对外表述 |
| KB 泄漏门盲区（R2-P1） | 4/4 CONFIRMED | 纯规范化子串匹配；build_one 用建库池自身 gold 自审（无 eval-gold 参数）；runner 不按 `from_item_id` 排除自身条目（result JSON 边界声明是散文非机器不变量）；source/eval 池分离仅为约定 |
| 出处/测试/调研覆盖 | 3 CONFIRMED + 1 PARTIAL | 273 个结果 JSON 均缺 git SHA/模型 hash/引擎 SHA/manifest hash；调研核验率 20/62、20/64 精确吻合（partial 率 20%/40%）；Locatello/Hewitt–Liang/Voita–Titov 全库仅出现于审计文档本身。PARTIAL：审计漏计 `test_kb_gate.py`（4 条实质执法测试，但 pytest 收集不到——"测试体系不足"论点反而成立） |

## 2. 审计错/过时/不公之处（批判性平衡，4 项）

1. **"偏离旗舰、擅开战役"不公**：三步走战役是 owner 2026-07-08/09 明令（Decision-Log 续2–续10），非漂移。但其底层观点成立——四个研究对象在文档中共享同一 headline、两套"现行计划"（07-04 CP-1/3/8/4 vs 07-09 三步走）并行未对账。本次以 G0 裁定 + 归档解决。
2. **低估测试面**：`test_kb_gate.py` 存在且实质（漏检项：审计）。
3. **W4 原子写出指控 STALE**：`cdbf1d2`（07-01）已修，审计快照旧。
4. **审计 136 格 vs 台账 140 格**：核验后**审计读码正确，错的是我们的 Decision-Log 续10 台账**（35 臂/140 格从未落进代码；RAPTOR-lite 臂未实现）。台账失实根因：网格草案 §6.7"工程前置①–⑤已全部完成"按代理完工报告入账、未经 E2E 门验证——**簿记纪律缺陷，本文承认并由 G2 门（全臂 E2E green 才准冻结/宣称完成）根治**。

## 3. Owner 裁定（2026-07-11，四项全签）

1. **接受 stop-the-line**：Phase-A、Step-3 新 GPU 批跑、65 格重抽重跑波全部暂停；已完成 Step-1 数字保留 hypothesis-grade 不回滚；先 G0（本文）→ 工程/统计地基 → G2（全臂 E2E green）再开跑。
2. **G0 主问题 = 当前战役**（见 §4 claim tree）：W1 收窄问题为 primary；W4 按审计 §7.1 重定义为独立旗舰线（正负可发表），不与 W1 共享 headline；W2/W3 维持 trained-comparison 定位。
3. **主张与术语改述包全收**：① W4 弃 disentanglement 措辞，降级 L0/L1（readout availability / suppression / selective-readout limits）；② W1 headline = "oracle headroom 真实，deployable selector 未实现"；③ 论文面主术语 = **weight-frozen reward-guided inference-time optimization/search**，内部保留 TFRL 缩写、对外首处给非标准定义并与 test-time-RL 区分。
4. **wiki 治理标准方案**：新建 `wiki/archive/`（收 8 SUPERSEDED + 43 已收官 survey 战役件）；86 件 LOG 原地加机器可查横幅；4 处 CANON 即刻修漂移；此后**每次战役收官即归档**为固定动作。

## 4. G0 claim tree（签署版）

**Primary question（唯一）**：
> 在冻结 Qwen3-Omni-30B、清白 KB、部署合规查询的条件下，speech-keyed 知识组织 × 检索 × 递送
> 与 label-free selector，能把 oracle candidate/retrieval headroom 实现出多大比例？

- **Primary estimand**：ρ = (R_selector − R_greedy) / (R_oracle − R_greedy)，cluster bootstrap CI（cluster = speaker/session/question-family），同报绝对任务 delta 与 GPU cost；oracle 分母 ≤0 的 item/集单独处理，禁止无限/负 ρ。
- **Secondary estimands**：检索质量（R@k/MRR/nDCG）与端到端增益分离归因；H-a vs H-b 按任务族判报；递送形式杠杆（2-turn 工具递送 vs flat）；采纳率 α；effective-N/语义多样性。
- **必带对照**：no-retrieval / random retrieval / oracle retrieval / long-context stuffing / gold-transcript（仅上界）/ own-ASR cascade。
- **Kill criteria（预注册）**：
  - random retrieval ≈ best arm，或 oracle retrieval 无增益 → 停止优化 retrieval（机制不在此）；
  - deployable selector 的 ρ CI 在两个独立 test surface 上均不高于 0 → 结论定为 "support exists, realization fails"，照常发表；
  - 仅单模型/单 runtime 有效 → 降级 case study。
- **不再追逐（当前证据下不做的主张）**："training-free RL disentangles frozen omni embeddings"；从 oracle 数字外推 deployable gain；agent-convergence 宏大主张；L4 三层叙事共享同一 headline。
- **支线挂账（不抢 headline）**：W4 §7.1（frozen omni 表示的可读性/可选择性/极限，H1–H4 预注册，fresh proposal 后启动）；理论轨 operator-linked 重写（coverage 定理 (1−p*)^N、可估 τ 的 selector regret、exp-weights 有限时界、负结果、no-universal-N*、`#print axioms` 白名单 CI）。

## 5. 修复计划（审计 Phase 0–7 → 执行票）

| 审计阶段 | 我方执行票 | 承接 |
|---|---|---|
| Phase 0 真源统一 | 本文 + 归档执行 + 4 处 CANON 修漂移 + Decision-Log 续11 | Fable+Sonnet，即刻 |
| Phase 2 工程必修 | #25：execute 路径、命名统一、禁 auto、真多粒度/H-a/H-b/RAPTOR-lite/audio+text、eval-manifest ∩=∅ 机器不变量、own-item 排除、语义泄漏辅审、测试矩阵（golden fixtures/property tests/fake-model E2E）、provenance 字段、原子写出、35 臂/140 格对齐 | Sonnet |
| Phase 2 统计地基 | #26：65 集组元数据盘点 → group split 设计 → cluster bootstrap → 重抽波修订后放行（#23 解除条件） | Opus 设计 + Sonnet 实现 |
| Phase 6 理论重写 | #27：operator-linked 定理批次（上列 6 项） | Opus/Lean |
| Phase 7 调研补课 | #28：其余 ~86 条 load-bearing claims 全量核验 + 补 probing 基础文献（Locatello/Hewitt–Liang/Voita–Titov/probe capacity）入 W4 链 | Opus 波次 |
| W4 重定义 | #29：fresh Research-Proposal-Template（§7.1 问法 + H1–H4 + speaker-grouped 切分）| owner 排期后启动 |

Phase 3/4/5（W4 claim-ladder 实验、W1 selector-realization 实验、Step-2 RAG 受控重启）在 #25/#26 落地后按三步走结构重排，**test 面在所有臂选定前锁死**。
