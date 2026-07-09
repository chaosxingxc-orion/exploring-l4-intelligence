# 2026-07-09 · Stage-1 实验战役设计：三步走（owner 定纲并批准）

> **性质**：Stage-1 实验设计记录（owner 2026-07-09 定纲、逐项裁定后批准执行）。
> 配套：覆盖三文档（model-matrix / dataset-taxonomy / theory-scheme-coverage）、
> 双轨战役设计书、Q1/Q2 备忘录。**每步开跑前判据冻结（prereg），每步收尾对模型/数据集
> 两张全覆盖台账销号。**

## Owner 三步定纲（原文大意）

1. **Step 1 基线锁定**：数据集 × 模型 × 评测方案的基线锁定；模型必须 GPU 驱动。
2. **Step 2 omni agentic system mock 基线锁定与方案对比**：数据集 × 多模态知识向量模型 ×
   知识组织方案 × 加载/检索方案 × 基座模型；模型必须 GPU 驱动。
3. **Step 3**：TFRL 技术方案充分调研；在 step 2 锁定前提下 top-N 效果基线锁定与方案对比；
   基于 lean skills 从数学论证分析多模态协同是否需要改进；多轮验证论证是否改进基线。

## Owner 逐项裁定（2026-07-09）

- 底座阵容 = **四底座 + 下 MERaLiON-2**（Qwen3-Omni GGUF 主 / minicpm-o / moss-audio /
  MERaLiON-2 GGUF，license 先核）；nemotron-nano 不许静默暂缓 → Step 0 限时跑通尝试，
  不通带证据豁免。
- **qwen3-omni HF int4 删除**（同模型 GGUF 已可驱动，留一份即可）。
- Step 1 = **三波推进**（波 1：K8+K9 闭卷+K1/K2；波 2：K4–K7；波 3：K10/K11+长尾）。
- Step 2 mock = **严格无 RL**（无奖励选择/无自适应门控/无 top-N——全部是 step 3 增量，
  delta 归因干净）；"固定"≠"单一"，组织×加载的方案空间本身是被对比对象。
- **模型与数据集均须全覆盖台账**：22/22 模型、45 集逐一有实验位或显式带证据豁免，
  每步收尾销号（台账全文见计划档案与本目录 coverage 文档；关键变化：mmsu 元数据已补
  → 从排除翻回 K8 纳入；cn-celeb2 已解压入 K5 池；ST 任务族空格留 step-1 冻结会裁决）。

## 三步结构（要点）

**Step 0 前置（≤1 天）**：MERaLiON license+下载+冒烟；HF 双底座活体冒烟；gpu_session.sh
分时协议（llama-server 启停序列化+会话锁+空闲断言）；30B GGUF embedding 导出 GPU 验证
（H-b 前提）；nemotron NVFP4 限时尝试；删 HF int4 + lock 注记；meld ffmpeg 与 air-bench
补取两项解堵。

**Step 1 基线锁定**：29 纳入集（dev40/test60 冻结）× 4(+1) 底座 × K1–K11 类型化可验证
奖励；greedy + 固定模板 + 显式采样参数；squtr 跑闭卷 floor（RAG delta 对照臂）；结果入
`_repro/baselines/`，每波 Opus 抽验 + 基线表 wiki。

**Step 2 mock agentic**：
- **2a 前置调研**（与 step 1 并行）：多模态知识组织/加载 2025-01+ 学术实践，4 维 Opus
  finder→adversarial-verify（多模态 RAG 系统 / 组织结构先例 / 加载检索策略 / agentic 原语
  与编排），产出候选矩阵供冻结会。
- **2b 方案空间底账**：8 个 agentic 操作原语（mock 固定版 vs step-3 自适应版标注）；
  key 侧组织 4 种（单 utt 键 / 多粒度键 / H-a 2–3 键空间 / H-b 单空间多读出）× value 侧
  4 种（knowledge / memory / exemplar / 结构化变体 LLM-Wiki+KG 低成本对照臂）；检索 5 种 ×
  查询构造 3 种（golden 转写查禁止）× 递送 4 种（已证一阶杠杆，全枚举）× 位置/压缩。
- **2c 网格**：主裁决场（squtr+heysquad-scrubbed+SQuAD-zh+vocalbench-knowledge）全因子
  （预注册削减：每维扫边际、交互项跑主对角+已证一阶杠杆组合）；特化侧翼按任务族；
  泄露纪律（verdict==CLEAN 强制门 + item-id 结构分离 + Information-Boundary-Guard）。
  **H-a vs H-b 与组织×加载最优方案在此裁决** → owner 门锁定 = step 3 分母。

**Step 3**：3a TFRL 方案调研（Opus，post-2025，产出可实施候选表）→ 3b top-N 基线与方案
对比（N-sweep × 选择器组 {oracle/MBR/置信度/跨模型验证器三路/自适应门控}，对比 step-2 与
step-1 双分母，paired CI 多种子；顺带产出 N*/τ/α/δ_corr/门控曲线全部约束项测量）→
3c Lean 论证（T-B 门限门 Bayes 最优 / N* 内点最优落地 / δ_corr floor / Beirami 清欠；
负半=mock 缺陷、正半=约束下改进——直接回答"多模态协同是否需要改进"）→ 3d 多轮
debate-verify-improve loop 至干涸 → **最终交付："TFRL 是否改进基线"论证结论 + Stage-2 候选**。

## 风险与对策（摘）

GPU 分时单点 → gpu_session 排程+波次化；网格爆炸 → 预注册削减入档；HF 底座/MERaLiON/
30B embedding 任一不通 → 降臂+证据豁免（Step 0 先验）；API 断连 → workflow resume（已演练）。
