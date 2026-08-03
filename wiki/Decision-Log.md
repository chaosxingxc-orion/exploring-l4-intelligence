# Decision Log

> Append-only, lightweight ADRs — the team's durable **memory**. Entries live in **monthly
> volumes**; append a new decision to the current month's volume (date · what we decided · why ·
> consequences), never rewrite old entries. Load volumes by targeted `rg` only — never broadly.
> Full discipline: [[AI-Collaboration]].

## 按月分卷 · Monthly volumes

- [[Decision-Log-2026-08]] — **当前追加卷**：owner GO 与建仓、Lean/W1–W4/调研包三场退役、
  运行节奏与公共职能宪章、架构重构
- [[Decision-Log-2026-07]] — 主体卷（93 条续N + 早期条目）：Stage-1A/1B/1C 全部战役裁决、
  记录体系去噪、评审整改链（续15–82）
- [[Decision-Log-2026-06]] — 起源卷：续1–14、免训练知识激活重定向、W4 旗舰期、种子决策

## 按研究对象划分 · By research object

- **audio-aware evidence acquisition（R2 provenance，现役 study）**：开题评审与整改链＝
  续76–87（07 卷末段 + 08 卷）；GO/建仓/数据线/执行合同＝08 卷 08-03 各条；实验期决策此后
  记 08 卷并在 `wiki/experiments/audio-aware-evidence-acquisition/` 留台账指针。
- **R1（已日落）**：授权补正与日落＝续76（07 卷）；context/ICL 证据链归档于
  `wiki/archive/working/stage1c-portfolio/`。
- **R3–R9（候选，OWNER_UNVERIFIED）**：候选定义＝续76–78 附带裁决（07 卷）；提案档案在
  `wiki/archive/working/stage1c-portfolio/proposals/`。
- **Stage-1A/1B 调研战役（已封存）**：续44–75（07 卷主体）；封存 ADR＝08 卷「调研包整体封存」。
- **W1–W5 时代（已退役）**：06 卷全部 + 07 卷早期条目；退役与冷备份 ADR＝08 卷。
- **程序级治理**：三阶段方法论（07 卷 07-04）、知识四层与记录规约（续44–58，07 卷）、
  架构与公共职能宪章（08 卷）。

## 追加规则 · Append rule

新决策写入当月卷（当前=[[Decision-Log-2026-08]]），新在上；跨月时新建
`Decision-Log-<year>-<month>.md` 并在上表加一行、更新「当前追加卷」标注。R 相关决策同时在
「按研究对象划分」对应行补一个指针。本页只维护索引，不承载条目。
