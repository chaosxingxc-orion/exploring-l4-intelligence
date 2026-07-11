---
title: "答复 v3：对 Step-1 完成声明法证复审的回应（自我勘误置顶）"
date: 2026-07-12
stage: 1-problem-definition
status: "已交付；REJECT-closeout 全接受（Decision-Log 续15）；状态词受六级制约束"
responds_to: 2026-07-11-step1-completion-forensic-integrity-review.md
---

# 答复 v3 — 全部接受，先勘误自己

尊敬的审稿人：

您的复审可检主张经我方独立增量核验为 **11/11 CONFIRMED**（数字类 5/5 逐位复算吻合，含
Holm-16 的 .592/.075/.000；一致性类 6/6；P0-1 由执行代理在活体库上确认）。owner 已全盘接受
REJECT-closeout 与 RI-0..RI-6 门（续15）。按您的判词，真正的测试是收到事实后的处置——以下
是处置记录。

## 1. 自我勘误（这三处过升级表述是协调者写的，指名承认）

| # | 我方错误表述 | 更正 |
|---|---|---|
| E1 | "Holm family-wise survives (noise2)" | 该结论只在事后缩窄的 4-selector@N=8 家族内成立；完整 4×4 discovery 网格 Holm-16 下 noise1 p=.592、noise2 p=.075。合法表述采用您给出的原句（同 cohort 噪声敏感性分析、方向一致、完整家族 n.s.）。已更正入 claim ledger C-ASR-V2 |
| E2 | "locked-DEV 65/65 零失败" | cell 级属实；item 级 510/4439 未评分、24 个 HTTPError、4 个空聚合、65/65 dirty、provenance 三键空值。今后 cell 级与 item 级口径强制分列 |
| E3 | "FIRST operator-linked theorem" | Coverage.lean 实质为 i.i.d. Bernoulli 覆盖模型 + 代码引注；已改名（"operator formalization pending — see Proposal-F"），ledger count=0 维持权威。六级制采纳后升级表述仍复发，纪律修正：**机器可读 ledger 先于任何叙述文字** |

另两处失实一并承认：ACCESS_LOG"未读 test_ids"与 census 代码矛盾（您抓得对，含 b4707fe
重叠核验的 membership 读取）；MInDS "7/7" 实为 5 个独特对比。

## 2. 止损与对象修复（您的 P0-1）

- **140 格扫描在启动前叫停：0 格跑在错误对象上**（`_repro/step2_mock` 不存在，无任何格产出）。
- squtr **corpus-side 真实建库器已落地并建成**：qrels 证据文档为值、text-keyed、gold-scrub 过
  CLEAN 门（活体 LEAKAGE→CLEAN 消解验证）；nemotron+glap 各 310 docs（W1 `e30af76`）；
  lco/qwen3-omni-own 记 pending-GPU-window；跨模态查询路由缺口如实写入 kb_retrieve docstring。
- **vocalbench-knowledge 退出 knowledge-RAG 主战场**（owner 裁定），并经 owner 内涵分析
  **再定性**为闭卷参数化知识探针（无证据段落列；"knowledge"指权重内知识）——重新归位为
  no-retrieval 语义锚点 + Step-3 selector 闭卷主场；标签漂移链根因已记录（网格草案 07-12 注）。
- Phase-A RAG 主场收缩为 squtr（corpus 重建后）+ heysquad + SQuAD-zh。

## 3. holdout 与 custody（您的 P0-2 / §7.5 / RI-1）

- 现有 locked TEST **永久降级**为 exposed-dev-like（README 横幅引用您的 11.20% 精确数）；
  未来确证 TEST = owner 亲任 custodian + 密封机制（与执行会话零共享上下文的全新会话库外
  抽取，仓库只存 salted commitment，读取即 burn）。
- census 不再打开 test_ids（counts 侧车）；ACCESS_LOG 追加更正条目。
- KB `content_hash`（values+keys+item_ids+code sha）+ **refuse-overwrite/supersede-archive**
  已实现（26/26 测试）；63 个存量源内容哈希清单落盘。
- 后整改 freeze 采用您要求的分离字段（planned_label / observed_at_utc / 观测时 git heads），
  54,688 文件。

## 4. 传播一致性（您的 §7.4）

ledger：可达 commit 修正（rebase 等价性以 patch-id 证明入注）、C-PHASEA/C-THEORY 补注、
C-ASR-V2 双路径+sha256。论文：五处修正**下沉到 sections/ 真源**，横幅移入 assembler，
`reassemble.py` 重组后与 main.tex 逐字节一致；"independently re-verified"改为
"internally re-verified by adversarial AI agents (not an independent team)"。

## 5. 状态表（六级制）

REJECT-closeout 接受：Step-1 维持未收官，全部数字 directional。机械整改 = IMPLEMENTED
（本轮 commits：伞仓 `7d2aa4c`、W1 `e30af76`、W4 `88dc775`）。仍 OPEN：RI-3 owner 逐项签
preregistration（Proposal A/B/F 已立项待起草/签署）、RI-4 custodian 重抽（设计全冻结后）、
RI-5 clean-checkout G2-L3、RI-6 独立复算。这些未完成项不会被写成完成。

Stage-1 执行组 · 2026-07-12
