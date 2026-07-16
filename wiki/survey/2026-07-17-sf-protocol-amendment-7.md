---
amendment_id: "SF-PROTO-AMENDMENT-7"
date: 2026-07-17
scope: "执行期合同——调研退出机制 E1–E3 / 全文强制细则 / agent-era 优先级操作化 / 引文校准实验登记"
gate_relation: "**非 gate 阻断项**:本修正案约束 mapping 执行与 Stage-1A close,不新增签署前义务;评审复核本件只需确认其不与已签对象冲突——不要求按其内容延长 survey-ready gate（评审 §12 反无限延长条款,我方主动遵守）"
owner_ruling: "2026-07-17:①退出看核心论文集引用链路完备性,不靠泛泛扫描;②「一篇都没引（交集为空）」= 基本无关;③backward 引文从论文原文自取,forward 用学术索引类工具;④发现新论文仍需检索算法——三层架构 owner 确认"
---

# Amendment-7：执行期合同（退出机制 / 全文纪律 / 时代优先级）

## §1 调研退出机制（Stage-1A close 的机器可判定收敛条件）

**架构（owner 确认的三层分工）**：发现层 = 冻结查询检索（BFS，61 条 + 版本化增补）；
相关性廉价筛 + 退出判据 = 引文链闭包（DFS/饱和层）；两层互补不互替——跨社区平行谱系
在结构上引不到核心集（Seg-Agent/DVD 类），必须由查询层兜住；核心集本身由查询层先发现，
闭包才有正确起点。

**退出 = 三条件合取（全部机器可查，逐轮饱和表落盘）**：

- **E1（BFS 干涸）**：全部冻结 mapping 查询执行完毕且命中筛查清零（REC-0 全量落账，
  flow 五计数机器导出）。
- **E2（引文闭包收敛）**：对每篇核心论文（= claim-bearing D2 工作），backward 参考文献
  （**从存档全文离线抽取**——可回放，不依赖外部索引）与 forward 被引（协议 §5 既注册的
  SS/OpenAlex 发现层；OpenAlex 为主、Semantic Scholar 为辅，快照日期逐次钉定）逐层筛查；
  **连续 K=2 轮闭包扩张新增 INCLUDED = 0** 即收敛。边过滤沿用协议 §5 五层防爆
  （方法谱系边+对比边）。
- **E3（哨兵清零）**：全部登记哨兵 + 评审后供反例经四分法归位，0 UNRESOLVED。

**引用交集廉价筛（owner 规则的落地形态）**：候选论文参考文献与核心集**交集为空 ⇒ 降级轻筛**
（题录/摘要级快裁）；据此 EXCLUDED 必须登记
`reason_code OTHER:NO_CORE_CITATION_OVERLAP` + 一句理由——**可审计可证伪，绝不静默丢弃**；
词项匹配但零交集的候选积累入 vocabulary-drift 观察队列（§4）。本规则**不得**用作发现层的
唯一入口（Seg-Agent/DVD 反例：跨社区相关工作预期零交集）。

**退出报告**：逐轮饱和表（每轮 新增命中/新增 INCLUDED/闭包边数/剩余队列），PRISMA-S 兼容；
Stage-1A close 签署以 E1∧E2∧E3 + 饱和表为证据，**评审不得以「再供一篇反例」无限延长**（新
反例走四分法归位与 dated amendment，不重开退出判据）。

## §2 全文强制细则（owner 裁决⑤操作化）

1. **义务面**：INCLUDED / 核心集 / 哨兵 = 强制全文双份（PDF + e-print 源码）；e-print 为
   E2 backward 抽取的正典输入。FETCH 即登记（不登记不算读过——四层知识模型纪律）。
2. **存储与台账**：数据盘 `$SPEECHRL_DATA_DIR/survey-fulltext/<id>/`（永不进 git）；git 只进
   append-only 台账 `wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl`（URL/UTC/HTTP/字节/
   sha256/存储路径/访问类）。采集器 = `scripts/survey/sf_fulltext_fetch.py`
   （export 端点、≥3s 限速、指数退避）。
3. **已执行（如实计数）**：26 哨兵全文双份采集入台账——截至 stage-1 提交 **44/52 renditions
   落盘**（余 8 件〔6 e-print + 2 PDF〕遭区域 TLS 拦截多轮瞬断，逐行失败留痕，重试进行中）；
   **执行首步义务**：补齐余件 + 92 种子全文批量采集 + SF-L9 四篇 DOI 经典的官方源获取
   （不可得 = REMOVED_UNOBTAINABLE 如实移除）。
4. 非 arXiv 工作沿用协议 §2 免费官方源救援 + `survey-backups/` 既有正典，本节不改动之。

## §3 agent-era 优先级操作化（owner 时代裁决）

1. **队列排序**：§4bis 排序键的「时新性↓」升为威胁度之后第二键；2025+ 工作先于前时代工作
   深读。
2. **前 2025 工作默认谱系/基础层地位**：D2 深读仅当 ①方法占据相关 或 ②在 2025+ 仍被持续
   引用（forward 引文存活度 = 「概念是否被淘汰」的机器判据，E2 数据顺带产出）。
3. **held-out 时代约束**已机器化（runner 强制 v1≥2025-01）。
4. **边界**：检索窗口/冻结前缀/种子存量不动；时代先验不进 study_quality（先验≠证据，与
   venue_tier 零证据权重同构）。

## §4 已登记的执行期观察义务

1. **Seg-Agent 引文校准实验**（本批预注册并已执行——自愿提前，非前置义务）：从其 e-print
   抽取参考文献，与存量论文集（92 种子 ∪ 26 哨兵，并集 99）求交——**预注册预测：交集 = ∅**
   （跨社区谱系引 SAM/SoM 系）。**结果 = PREDICTION_CONFIRMED**（30 个被引 arXiv ID × 99
   存量 = 空交集，`docs/checks/2026-07-17-sf-citation-calibration-segagent.json`）——
   「引用交集筛不能当唯一发现入口」的实证登记件成立，§1 规则维持；结果件随批入 bundle
   作为已完成证据（本修正案其余义务均为执行期，不因此新增签署前义务）。
2. **vocabulary-drift 观察队列**：执行期逐批登记「词项匹配但类目被挡」与「他渠道发现但
   61 查询零命中」的在对象工作；累计到 3 例同轴即触发受控道增补评估（appended/versioned，
   不改前缀）。
3. **execution-early 队列**（评审 §7 表 + 本批核验）：WorldEvolver 2606.30639 /
   PolarMem 2602.00415 / AudioGenie 2505.22053 / Dopamine-Audiobook 2504.11002（四篇
   FULLY_TRAINING_FREE，ID 前置核验通过）——BFS 首轮优先精读；
   **MemoPilot 2606.08656 = TF-Strict 直接威胁样本**（冻结 player + multi-turn GRPO 训练
   外部 memory updater，abstract 级坐实 TRAINS_EXTERNAL）→ 入 direct boundary/threat 队列，
   双人抽取纪律适用。
