---
title: "Gate S0 — Program Identity（研究纲领身份签字页）"
date: 2026-07-15
status: "SIGNED_VIA_SESSION_DIRECTIVE (2026-07-15) — owner 在读完本页修订版全文后以明确会话指令签署（授权原文逐字存 Decision-Log 续48）：确认身份三行 + 勾选 TF-Strict。区别于「问答≠签署」歧义：本次是 owner 对本页文本本身的、知情的、显式签署指令；owner 可随时亲笔补签。修订史：签署前按 owner 意见删 north_star_metric 行（身份层不立法指标）、supersedes 移出合同区（08ed2fd/2f7bd22）"
review_lineage: "v2 博导评审 Gate S0 要求（2026-07-15-stage1a-research-proposal-doctoral-adversarial-review-v2-owner-clarified.md §8）"
---

# Gate S0：研究纲领身份（一页）

```text
primary_object        = 面向冻结黑盒 omni foundation model 的外部 reward-guided agentic system
                        （外部控制平面：观察/供给构造 · 状态与外部记忆 · 工具/检索 · 候选生成 ·
                          评估 · 选择 · 预算/风险/停止 · 溯源与信息边界守卫）
north_star_method     = training-free reward-guided external control——reward/advantage 决定下一步
                        动作；固定池内选择是其退化特例
selector / evaluator  = supporting components——既有 selector 线全部工件（合同/台账/协议）降级为
                        组件 dossier，效力不变
resource_posture      = 全力摸高（当前：预算不设 cap、照实记录）→ 持续整合 → 成本压降；
                        等预算类判据 = PHASE-3_TOOL 延后启用
black_box_contract    = 严格黑盒 headline：核心方法不得要求 weights / gradients / hidden states /
                        attention / 保证可得的 logprobs；本地 llama.cpp 部署 = 低成本校验环节
                        （GRAY_BOX_DIAGNOSTIC，永不承重）
training_free_scope   = （TF-Strict/TF-Core 系 v2 评审拟的代号；人话正名如下括注）
                        ☐ TF-Strict =「全系统零训练」：核心模型和我们造的全部外部组件
                          （evaluator/controller/router）都没有任何可训练参数，适应只靠上下文/
                          记忆/搜索/规则/非参数统计——与「只通过外部系统优化」一致，草案推荐
                        ☐ TF-Core =「仅核心冻结」：核心冻结，但允许训练外部小组件（如小 reward
                          model/router）；此时 headline 必须改名 frozen-core agent optimization，
                          不得裸称 training-free
core_structure_policy = 核心模型权重与内部架构冻结；外部系统结构显式设计并版本化
                        （旧「不改结构」措辞据此修正，消除字面自相矛盾）
innovation_status     = 系统级创新 = owner 选择的创新假设；system-first survey 占据核查完成前，
                        不得宣称任何「首个」
```

**度量说明（非合同条款）**：具体指标绑定任务×数据集，在各研究的协议中定义、Stage-2 预注册时
冻结——**身份层不立法指标**（owner 2026-07-15：过早在身份层定指标，正是把指标误立为研究对象
的倒置风险源）。可测处保留「相对冻结模型自身天花板记账」的报告纪律（headroom 归因，见热层
硬约束），仅此而已。

**簿记效果（非合同条款，签署即自动生效）**：本页取代「唯一主问题 = ρ 实现率」（G0 2026-07-11）
与 Project-Thesis 2026-07-12 取代说明（selector-first primary）——旧裁决正式退役、不得再作现状
引用。（记录此项的原因：本次方向漂移的根源之一就是旧裁决从未退役、被后续会话反复再引用。）

**签署（两项分立）：**

- [x] 身份三行（primary_object / north_star_method / selector 降级）确认
- [x] training_free_scope 勾选：**TF-Strict ☑** / TF-Core ☐

owner 签署：**via 会话指令 2026-07-15**（授权原文逐字存 Decision-Log 续48；亲笔补签位保留：
签名：__________________ 日期：__________）
