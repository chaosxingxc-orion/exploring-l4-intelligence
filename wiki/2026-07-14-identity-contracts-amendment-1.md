---
amendment_id: CONTRACT-AMEND-2026-07-14-01
title: 身份合同修正案 №1 —— δ_corr 拆名、strict-I2 kill-if 重写、UMBRELLA 算子范围更正、签字块拆分
date: 2026-07-14
amends: "wiki/2026-07-14-identity-contracts-v1.md（FROZEN@dce5c79，sha256(git blob)=1338f6b16f5409022b0a8193c5e71729dcf65ba78f1fa41b3645e642efc208b1）——正文条款一字不改；§8 日志按其自身规则追加一行；生效以 owner 重签为准"
trigger: "第三轮博导复审（收档 a06a498）§6.3 / §9.2 / §9.7：δ_corr 同名异义（理论=误差去相关；合同/探针=选择重合>90%）使 strict-I2 kill-if 在数学与构念上不可执行；same-selector contract 对 UMBRELLA 的『环内每一步』覆盖无定义对象；C1/C4 终验与探针授权混签"
status: EFFECTIVE — owner 于 2026-07-14 以两次独立 AskUserQuestion 裁决分栏签署（§E 主签 + §D Integrity gate 各自落笔，未混栏）；治理性签署，非审计签署
posthoc_log_entry: "已按合同 §8 规则同步登记：变更=判据修正（kill-if 可执行化），触发=第三轮复审，novelty 判定不变"
generated_by: "Claude Fable 5 主会话（依复审 §6.3 拆名清单起草；构念论证引 JudgeBoN within-prompt 教训）"
signoff: { owner: PENDING_RESIGN, date: null }
---

# 身份合同修正案 №1

## A. δ_corr 拆名（修正合同 §3 与术语歧义）

**问题**：`δ_corr` 同一符号承载了三套语义——理论文档 TH2a（2026-07-05）的
「可达误差去相关，δ_corr→0 时收敛至 oracle」；v4.2 整改的「实测误差相关/条件互信息」；
合同/探针把它操作化为「同核与外部**选择重合** >90% ⇒ δ_corr≈0 ⇒ kill」。
复审判定第三种是构念替换：**两个 scorer 可以 100% 同选且全对，也可以 100% 同选且全错**——
选择重合推不出误差相关，更推不出独立价值缺失。

**拆名（自本修正案起强制）**：

```text
selection_overlap    = P(argmax S_same == argmax S_ext)          —— 仅描述量，不得作 kill 判据
error_corr           = φ相关( 1[sel_same 错], 1[sel_ext 错] )     —— 在有头空的 item 上计算
conditional_error_mi = I(E_same; E_ext | item 难度/头空分层)      —— 探针样本量下仅作描述
complementary_gain   = U(best router/combiner) − max(U_same, U_ext)   —— 含组合器形态,非仅二选一
```

**符号裁定**：理论符号 `δ_corr` 保留 TH2a 原义 = **残余误差相关**（越小越接近 oracle 收敛），
其经验估计对象 = `error_corr`。「选择重合」永久移出 δ_corr 语义。术语表同步登记。

## B. strict-I2 kill-if 重写（替换合同 §3 原 kill-if **两条**——两个独立测试，不合取）

**测试一（替换原第一条「shuffle 音频不改变选择」的 winner-flip 操作化）——音频接地检验**：

```text
kill/pivot 方向（独立成立即触发）：matched controls（correct / item-permuted / silence 或
masked / 同说话人同长度 hard-negative audio）下，同核 score 的 delta、rank correlation、
winner margin 与最终 U 均无系统响应 → 该信号对音频无因果依赖 = I1 类文本流畅度选择器，
strict-I2 的音频接地前提不成立（坍缩方向,不必等测试二）。单一 shuffle winner-flip 率作废。
```

**测试二（替换原第二条「δ_corr≈0」的选择重合操作化）——独立价值检验**：

```text
kill 方向成立需同时满足：
  ① 高同错：有头空 item 上 error_corr 高（同核与外部在同一批 item 上一起错）；
  ② 无互补：complementary_gain ≈ 0（连 best router/combiner 都无法从二者组合中获益）。
仅 selection_overlap 高：不构成任何 kill 证据（描述量）。
```

**强制报告清单（每次运行，缺一即不完整——JudgeBoN within-prompt 教训的落地：以
Recovery/PCS 等终端决策量收口，不以 aggregate agreement 收口）**：双 selector 各自的
Recovery / PCS / rho / regret；双者间 rank correlation；2×2 四格计数（A错B对 / A对B错 /
都错 / 都对）；selection_overlap（描述）；router 上界与 complementary_gain。

pivot-if 不变（只有外部 scorer 有效 → 坍缩回 I1）。**P-γ 处置**：其判读框架由本节替换；
探针能否称「conditional complementarity 探针」取决于 Gate C 是否完成复审 §9.2-A 的全部定义
（generator context / verifier context / 输出 score / 长度归一 / candidate formatting /
是否要求模型判断「音频是否支持该答案」）——**若最终实现仅为 likelihood 打分，探针强制命名
`same-core likelihood baseline`，不得称 strict-I2 独立信号**。

## C. same-selector contract 范围更正（替换合同 §7 适用范围段）

原文（作废）：「UMBRELLA 的环内每一步选择动作仍受本表约束」。

**更正**：same-selector contract 只覆盖**池内选择算子**（I1 / bare-I2 / strict-I2 / I3 / I4）。
UMBRELLA 的 agentic 环是**不同的算子对象**（含生成、扩池、工具调用阶段——按 P0-R7 分类法与
池内选择禁混写）；其 action-proposal 结构留待 Stage-1C dossier 单独冻结，其核心保留问题=
**等预算下 advantage-guided loop vs 一次性 BoN/MBR/rerank 的判别**（复审 Proposal E 采纳）。
不得以「仍受约束」一句把不同算子并成同一对象。

## D. 签字块拆分（修正探针协议 §7 的混签；复审 §9.7）

原探针协议把「C1/C4 census 终验」与「探针开机授权」并入同一签字动作——前置未终验却标
prerequisites_met，构成循环。拆为两个独立 exact-hash 块：

```text
【Integrity gate —— 独立签字栏,owner 须在本栏单独落笔（可与 §E 同时进行,但不由 §E 代签）】
owner 确认：C1 = CENSUS_COMPLETE_WITH_REGISTERED_PERMANENT_GAP（config-selection 轨迹永久缺口,
1B 起由探针尝试登记前瞻关闭）；C4 = CENSUS_COMPLETE（29 行台账）。
对象（sha256(git blob bytes) @ HEAD a09ae94,核验命令 git show <commit>:<path> | sha256sum）：
  docs/integrity/2026-07-14-c1-attempt-census-draft.md
    = a3999861674b500e40c4cd24b5f49c1a88c4882c3b6e37d8e35484bb4a663a25
  docs/integrity/2026-07-14-c4-negative-results-census-draft.md
    = 4ae58ae3f320f3407fa3b25960ce6c02879b7f304ec2d5c4aa13fc040e05c5ec
owner: 已签——2026-07-14，AskUserQuestion 第二栏独立裁决（「终验签收」）；C1/C4 就此正式关闭，
Stage-1B 诚信前置满足（探针开机另需 Gate C Protocol gate）

【Protocol gate —— 留待 Gate C，冻结 run manifest 后单独签】
对象 = 探针协议 v2 + frozen run manifest 的 exact hash。冻结项 = 复审 §9.5/9.6 全部前置项
（item IDs/seeds/温度/c1/解析规则/dev-split 替换）**加 §9.2-A 全部定义**（generator/verifier
context、score、长度归一、formatting、audio-support 判断）。本修正案不构成该授权。
owner: PENDING_GATE_C
```

**随本修正案生效的 supersession 声明**：探针协议 v1（`2026-07-14-1b-probe-protocol-v1.md`）整体
标记 SUPERSEDED——其 frontmatter `prerequisites_met` 行与 §7「签批同时完成 C1/C4 终验」混签语义
作废（协议 v2 于 Gate C 重写）；C1/C4 两份 census addenda 中「owner 于 1B-0 探针协议签批时终验」
句由本节 Integrity gate 取代（append-only：此句即 dated 更正，原文件不改）。

## E. Owner 重签块（本修正案生效开关）

```text
重签语义：仅生效 A–D 条款文本；合同 v1 其余条款不变；§8 post-hoc 日志已同步登记本次变更。
C1/C4 终验不由本栏承载——owner 须在 §D 的 Integrity gate 栏单独落笔（两栏可同时签,各自独立）。
Protocol gate 仍留 Gate C。
owner: 已签——2026-07-14，AskUserQuestion 第一栏独立裁决（「重签生效」）；A–D 条款即时生效，
合同 §8 日志行转正，探针协议 v1 正式作废（v2 于 Gate C 重写）
```
