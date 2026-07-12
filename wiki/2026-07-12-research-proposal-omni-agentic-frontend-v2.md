---
title: "Research Proposal v2（效果优先版）：Omni Agentic System 的前端多模态知识体系"
date: 2026-07-12
stage: "1-problem-definition → 申请进入 Stage-2 预注册"
status: "DRAFT v2 — owner 批判性修正后重构（研究对象=系统；效果=最终裁判）；未签署，签署前零实验"
supersedes: 2026-07-12-research-proposal-RDU-frontend-knowledge-v1.md
panel_response: "v1 敌对评审团 5 FUNDAMENTAL + 12 MAJOR 全部处置（§9 映射表）"
---

# Omni Agentic System 的前端多模态知识体系：以业务效果为裁判的检索·发现·使用

## 0. v2 与 v1 的本质差异（owner 修正记录）

v1 的错误：把研究对象收窄到模型本体（frozen-key 纯度），并把主问题设计成"两头可发表"。
owner 裁定（2026-07-12）：①研究对象 = **omni agentic system**——冻结 omni 为核心组件，
**知识子系统与核心系统解耦、允许异构**（组件以"冻结使用 + 效果最优"选型，不背模型纯度包袱）；
②**效果是唯一最终裁判**——主问题必须设计成去赢；系统效果不达标的后果是回炉迭代（预算界定），
"负结果也是贡献"的表述**禁止用于主问题**，仅保留给次级科学点；③frozen-key sufficiency 降级为
次级科学点 S1（组件选型依据 + 激活叙事证据）。

## 1. 主问题（唯一，效果口径）

> 以冻结 Qwen3-Omni-30B 为核心的 omni agentic system，加装前端多模态知识子系统（检索-发现-
> 使用三段，组件异构、全部冻结使用），能否在知识依赖型语音任务上，对**强基线**（调优闭卷
> prompt 与 long-context 全塞入，取两者最优）取得 **≥10% 相对**、全家族校正后统计可靠、
> 边界清白的业务效果提升？

- **成功语义**：达标 → 系统主张成立，对外效果故事 = "零训练前端追平/超越需专训检索器的
  pipeline"（trained-frozen 对照臂支撑，见 §3-S1）；
- **失败语义**：不达标 → 进入系统设计迭代循环（§8 预算界定的 pivot 规则），**不以负结果
  自我安慰**；只有耗尽预注册迭代预算仍不达标时，才由 owner 决定是否转向边界性结论。
- 合规口径：组件"冻结使用"= 我方不训练任何参数；上游预训练组件（含 trained-frozen 检索器）
  照 LLMLingua-2 先例标注，不作为 training-free-by-construction 证据。

## 2. 系统架构与组件选型自由度

```
语音输入 → [发现：何时/需何类知识（两遍管线，见 S3）]
        → [检索：异构键空间（S1 对比后选型）× 检索策略]
        → [使用：递送形式（card/2-turn/flat）+ 信任标定]
        → 冻结 omni 核心生成 → 业务效果
```

知识子系统候选组件（全冻结使用）：键/查询嵌入 = qwen3-omni-own（2048d 活体已验）/ GLAP /
omni-embed-nemotron（trained-frozen 对照）/ 专化侧翼（实体粒度）；own-ASR→文本检索 = 无音频键
的级联替代。**选型由 dev 效果决定并如实报告**——系统不押注任一组件。

## 3. 假设结构：一个主效果假设 + 四个次级科学点

- **H-sys（primary）**：§1 原文。判定于确证层（custodian 单通道）。
- **S1（frozen-key sufficiency，降级后的 v1 主问题）**：omni-own 键 vs 专化冻结 vs
  trained-frozen（nemotron）的检索质量（squtr 原生 R@k/nDCG）与端到端贡献对比。价值 =
  组件选型依据 + "激活"叙事证据；**系统成败不押于此**。若 omni-own 不足，系统换用更强冻结
  组件继续（负结果仅记录为 S1 边界，不阻塞 H-sys）。
- **S2（递送主效应）**：预注册单一对比 = 递送主效应（card+2-turn 合并最优 vs flat）−
  键模态主效应，联合 CI（panel #5 修复：不再用"≥ 任意维度"的病态定义）。
- **S3（发现段·两遍管线）**：触发式检索作为**独立 two-pass pipeline**（第一遍生成量取不确定
  度→决定检索→第二遍生成），**在 mock 口径之外**运行（panel #2 修复：不违反
  assert_no_adaptive_logic 不变量）；定位 = active-retrieval（FLARE/Self-RAG 谱系，引注）向
  冻结 omni 的迁移；双门判定：增益差 TOST（margin 预注册）+ 调用降幅 ≥30% superiority
  （panel #14 修复）。
- **S4（实体粒度实例）**：热词管线中**可部署列表 = 从 eval 前冻结的热词库经音频键检索的产出**
  （panel #3 修复：真词保证入列的列表降为 oracle 上界臂，不可部署标注）；B-WER 主指标以
  检索产出为条件计算；检索召回/同音精度（H5a）单独报告；测试床 = is21_deep_bias /
  AISHELL-NER / SLURP（附录 A 协议）。

## 4. 实验设计

### 4.1 数据与基线（覆盖纪律：多集轻采样 dev n=40）

主场 squtr / heysquad / SQuAD-zh + 闭卷锚点 vocalbench-knowledge + S4 测试床。
**强基线族**（被超越对象，dev 调优后冻结）：①调优闭卷 prompt；②long-context 全塞入
（相关语料直接进上下文）；③own-ASR 级联检索（无音频键的传统路线）。closed-book 锚点改为
**within-item 配对对比**（同一音频，KB 供给 vs 保留——panel #9 修复）。

### 4.2 臂预算（探索层 dev only）

系统配置搜索 ≈ 键空间(4) × 递送(3) + 检索策略微调（出信号维度追加）≈ 12-16 格/集 +
基线族 3 + 对照臂 4（random/oracle-retrieval、gold-transcript 上界、no-retrieval）
≈ **20-23 格 × 4 集 ≈ 90 格** + S3 两遍管线 8 格 + S4 测试床 ~24 格。每臂按**生成遍数**
计价（two-pass 臂 ×2），开跑前实测 1 真格标定 wall-clock（panel #15 修复）。

### 4.3 统计（panel #4/#11/#13 修复）

- **单尺度**：一律相对改善百分比为主尺度；**per-dataset SESOI 数值表**（预注册附表：各集
  基线水平 → 10% 相对换算的绝对值）；主判定 = 相对尺度单门；
- **家族全枚举**：每个假设一个预声明家族（H-sys：最优配置 vs 3 基线 = 3 比较；S1：3 键空间
  两两 = 3；S2：1；S3：2；S4：列表长度扫描 {2,5,10,50} = 4 + 主对比 1；闭卷锚点 1）——
  **合计 15 项，全表进 Holm/max-T**，"显著"必注家族；
- **交互模型预注册**（panel #13）：键×递送交互 CI 宽度门控主效应解读；H-sys 赢家按格级
  估计选择；
- cluster bootstrap（group_key；无组集如实回退）；跨集固定效应为主、DL 仅作参考
  （panel 驳回项 R1-m1 的处置）。

### 4.4 探索/确证防火墙（panel #6/#7/#12 修复）

- **探索层不触发任何 kill**（panel #12）：探索层输出 = 配置排序 + Phase-B 协议草案；
- **确证层**：owner 签 Phase-B 后，custodian 加固版抽取——**先公布 hash{抽取脚本, 候选 ID
  全集, 种子规则}入库，种子取自公共信标（如比特币区块哈希/NIST beacon），全新会话仅接收已
  承诺脚本执行**（panel #6 修复：抽取不可被协调者引导）；确证池组不相交于
  union(dev+旧test+65曝光清单)（panel #7），无组键数据集不入确证层或先补组键；
- 单通道单次消费、读取即 burn 沿用。

## 5. 边界与 custody

v1 §5 全部保留，外加：content_hash 扩展至**嵌入器 SHA+revision+量化+归一化配置与索引参数**
（键==查询嵌入器 fail-closed 断言）（panel #8 修复）；S4 列表构造 = 检索产出（§3-S4）。

## 6. reward 信号层（δ_corr 处置：panel #17）

信号表（logprob/熵、外部冻结 LM 评分、自一致性）仅供发现段触发与使用段标定。
**δ_corr 定位选择"借用基础设施"**：引 ROVER（Fiscus 1997）谱系作为跨源误差互补的经典依据，
从我方定理约束清单中移除（不作为本提案的理论贡献主张）。

## 7. 理论轨（与系统同对象）

形式化对象改为**系统算子**：两遍管线的触发规则（S3）与检索-递送复合算子的正确性；召回下限
约束下的效果保证形式；无约束反例（过严门控）。Coverage.lean 保留为 i.i.d. 前置。

## 8. 停止/pivot 规则（效果优先版）

1. 确证层 H-sys 达标 → 系统主张成立，进入 Stage-3 评估；
2. 确证层不达标 → **系统迭代循环**：分析瓶颈段（检索/发现/使用分解归因）→ 修订组件/协议 →
   重新探索；**预算 cap = Stage-2 内最多 2 轮迭代**（每轮需 owner 批准），耗尽后 owner 复盘
   决定转向；
3. oracle-retrieval 无增益的集 → 该集退出主场（瓶颈不在知识供给）；
4. 次级科学点（S1-S4）各自如实报告，正负皆入 ledger，不影响 H-sys 判定路径。

## 9. Panel 17 项处置映射

F1→§0/§1（主问题重构为效果口径，owner 裁定）；F2→§3-S3（两遍管线出 mock 口径+引 FLARE/
Self-RAG）；F3→§3-S4（列表=检索产出）；F4→§4.3（单尺度+SESOI 数值表）；F5→§3-S2（单一预注册
对比）；M6→§4.4（信标种子+承诺脚本）；M7→§4.4（确证池组不相交于全部曝光集）；M8→§5
（content_hash 扩展）；M9→§4.1（within-item 锚点）；M10→§10（Week-1 现实化）；M11→§4.3
（15 项全家族表）；M12→§4.4/§8（探索层无 kill）；M13→§4.3（交互模型）；M14→§3-S3（双门）；
M15→§4.2（按遍计价+先实测）；M16→附录 A（logit_bias/GBNF 仅探索标注）；M17→§6（δ_corr 借用
定位）。噪音 5 项按主席驳回意见处置（2-turn 更名"两轮 prompt 递送"等）。

## 10. 时间线（现实化）

Week 1：own-ASR 级联臂 + 文本键系统配置先行（今日可跑技术栈）∥ 并行建：跨模态路由、S4
偏置协议、两遍管线；1 真格成本标定 → 探索层分两批（先 text-key 批，后 audio-key 批）；
Week 2：三段归因分析 + Phase-B 协议（预命名赢家 ≤3 + 基线族 + 对照）+ S1 报告；
Week 3：owner 签 Phase-B → custodian 信标抽取 → 单通道确证 → H-sys 判定。

## 11. Owner / Reviewer 签字位

1. §1 主问题措辞与强基线族构成；2. 10% 相对门槛与 per-dataset SESOI 表；3. §3 次级科学点
取舍；4. §4.2 臂预算；5. §4.3 家族表（15 项）；6. custodian 信标协议；7. §8 迭代预算
（2 轮 cap）；8. S4 偏置协议；9. 时间线。

## 附录 A/B：沿用 v1（S4 协议按 §3-S4 修订：检索产出列表；oracle 列表臂标注）。
