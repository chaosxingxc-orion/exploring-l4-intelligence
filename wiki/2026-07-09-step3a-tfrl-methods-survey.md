# 2026-07-09 · Step-3a 调研：training-free RL 可实施方案矩阵（覆盖材料——不预选臂）

> **性质**：Stage-1 Step-3 前置调研（owner 定纲"TFRL 充分调研"项）。**方法**：5 维 Opus web
> finder + 20 条承重验证（**12 CONFIRMED / 8 PARTIAL / 0 REFUTED**，修正见 §4）。
> **产出**：92 claims、**~90 个可实施候选**（每个带 lever_class × our-stack 成本 × 理论钩子），
> 理论钩子覆盖：τ×80 · N*×43 · τ*×34 · recall×31 · δ_corr×30 · R×26 · α×20——与 27 定理候选
> 台账天然双向绑定。**臂选择留 step-3 kickoff owner 门**。
> 原始档：`survey/2026-07-09-step3a-d{1..5}-*.json` + `-verifications.json`。

## 1. 五维要点（★ = 与我们栈/理论契合度最高）

**D1 选择/top-N（16 候选）**：★Self-certainty+Borda（免奖励模型；**修正：全词表对均匀分布的
KL，非 top-k 均值 logprob**——llama-server 只出 top-k logprobs → 近似有效性是 P3 核查项）；
★**RCS 嵌入质心选择**（Fréchet 均值，+2–7% over 多数票；**直接复用我们 CPU 驻留的 faiss 嵌入
器作独立效用 = 天然 δ_corr**）；★MBR-ROVER（ASR 形态，4–8 样本即起效，编辑距离效用≡ROVER）；
GER/H2T 重写（输出可超全部输入假设 = R 扩展）；USC（同模型自选 = **低 δ_corr 对照基线**）；
Integrative Decoding；CISC/排名投票；语义熵聚类选择；Soft-BoN（防过优化）。

**D2 验证器重排/跨模型验证（17 候选）**：★ASR 跨系统一致性验证器（cross-WER，非 Whisper
ensemble 素材，L-M 成本）；★弱验证器无监督聚合（FUSE/Weaver 线，条件独立前件）；isotonic
dev 校准层（L 成本，τ 测量的现成工具）；conformal 风险控制选择门；pairwise 淘汰赛；
budget-aware 验证器分级（便宜先行、不确定升级）；悲观 BoN 上限（N* 护栏的工程版）；
**ICR 注意力聚合重排 = BLOCKED**（llama-server 不暴露 per-head attention——栈边界钉死）。

**D3 训练无关自适应门控（18 候选）**：★TARG margin/熵检索门（L）；★多信号融合门（熵+margin+
一致性+检索相似度；**修正：原文并非我们所述的融合配方，实现须按修正版**）；CoCoA token 级
上下文-参数仲裁；ClashEval 先验概率门；SUGAR 语义熵深度门；UAB 重采样预算门；UCCI isotonic
校准；conformal 弃答门。**空白确认：语音原生门控几乎不存在**（唯一音频信号是 dLLM-ASR 置信
早退）——文本门控在 omni 上的迁移有效性 = 我们的实验空位。

**D4 推理时搜索（23 候选）**：rStar 式 MCTS+互鉴别、MCTS-RAG（检索决策入搜索）、Search-o1
（不确定时检索+文中推理）、LATS（T10 多轮作搜索空间）、REBASE、★DeepConf（logprob 置信门+
在线早停，**token 省至 ~15%** = N* 的数据驱动实例化，L-M 成本）、自适应 N 停止、RSD 两级升级
（便宜通道→omni 验证）、CRITIC 可验证奖励迭代精修（T10 精修环）。**栈边界：无分支 KV 句柄
——树搜索按全重解码计成本**（prompt-cache 摊薄共享前缀）。

**D5 RL-trained 对照类定位（18 条）**：Search-R1/R1-Searcher/ReSearch/s3/DynamicRAG 全部映射
到对应 training-free 杠杆；**关键定位数字（修正版）**：Search-R1 较 RAG 基线 +41%（7B）/+20%
（3B）——这是 RL 训练买到的上限参照，我们的论题是 training-free 能吃到其中多少。多篇论文
自带 prompt-only 基线数 = 我们预期增益的文献锚。

## 2. 杠杆类 × 理论钩子（臂设计的骨架）

| lever_class | 数量 | 主理论钩子 | step-3b 的角色 |
|---|---|---|---|
| selection/top-N | ~22 | τ、N* | N-sweep 主臂族（oracle/MBR/RCS/self-certainty/USC） |
| gating | ~25 | **τ\***、N*、α | 门控曲线主臂族（TARG/多信号/ClashEval/conformal/DeepConf） |
| reranking | ~13 | τ、R | 候选重排与 GER 重写 |
| cross-model-verify | ~11 | **δ_corr** | MERaLiON-2 + ASR-ensemble 验证器臂 |
| search | ~11 | N*、R | 高成本档（预算允许时的 T10 搜索空间） |
| comparison-class | ~8 | — | RL-trained 定位参照（不实施） |

## 3. 栈边界（load-bearing，臂设计硬约束）

1. llama-server 暴露 top-k logprobs，**不暴露全词表分布** → self-certainty 需 top-k 近似
   有效性核查（P3 检查项）；
2. **不暴露 per-head attention** → ICR/CoRe/ReAttn 注意力重排全线 BLOCKED（对照类记录）；
3. **无分支 KV 句柄** → 树搜索成本 = 全重解码 ×分支数（prompt-cache 摊共享前缀）；
4. 单卡 24GB 被 30B 常驻占满 → 跨模型验证走分时（MERaLiON-2 3B 可考虑 CPU 推理小规模）或
   ASR-ensemble（sherpa-onnx CPU 即可）。

## 4. 承重验证 PARTIAL 修正（8/20，实现时必须按修正版）

1. MBR-ASR 增益非"~20–35%"区间——高度条件依赖（原文无此汇总区间）；
2. **self-certainty = 全词表对均匀的 KL**（非 top-k logprob 均值）；
3. 多信号门控融合配方与原文不符——按修正版实现；
4. MBR 效用膨胀是引用的先验知识而非该文发现；
5. 一处双论文混引已拆分归位；
6. self-certainty 公式重申（同 2）；
7. T7 数字引用（0.283/0.767/0.800/0.633 与"约束是召回非精度"）确认无误；
8. Search-R1 定位数=+41%/+20% over RAG 基线（非我们初记的表述）。

## 5. 与两条既有线的合并点

- **27 定理候选台账**：D1-D4 候选的 theory_hook 直接指向 τ*/N*/δ_corr 定理目标——3c Lean
  首批定理的"工程对应物"就位（dual-track binding 的素材）；
- **2a 的 out-of-mock 14 项**：与本表 gating/search 类合并去重后构成 step-3b 臂候选全集。
**本文不选臂；step-3 kickoff 时与 owner 按（理论钩子覆盖 × 成本 × 栈可行性）定臂。**
