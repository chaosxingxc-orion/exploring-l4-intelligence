# MD 与脚本整编战役 spec（2026-07-29）

## Authority

owner 2026-07-29 指令（逐义）：包括 wiki 内文件、CLAUDE.md、AGENTS.md 和工程内 md 及相关脚本
都做清理。**md 看内容**：与当前工作无直接关系的直接移除；弱关系的摘要后归档；只保留强关系。
**脚本判断是否必须使用**：不是必须的都删除；必须使用的再分析能否用模板+配置优化、降低脚本
数量、转化为配置文件。追加裁决：**「一句话，应删尽删！」**——边界件默认删除（台账保恢复），
仅门禁绑定或 R2–R9 重审证据承重的保留。

当前工作定义（判级基准）：Stage-1C R2–R9 开题报告式协同重审（07-29 判据与模板）→ Stage-2A
R5+R6+R8 纵向切片（核=Qwen3-Omni-30B via llama.cpp，ASR 主线=通用 ASR）。

## 处置规则

- MD：STRONG 保留（current 加载面、活跃 proposals/模板、dossier/T1-T3 证据、HOT 正典、
  README/CONTRIBUTING、门禁引用件）；WEAK 先写 2-4 行摘要汇入本役 digest 再删除入台账；
  NONE 直接删除入台账。CLAUDE.md/AGENTS.md 不删，做节级瘦身（镜像同步、≤12KB）。
- 脚本：MUST_GATE（10 条门禁及其 import 闭包）/ MUST_INFRA（env/data/wiki-sync/train/eval 入口）/
  MUST_PYTEST（守活跃不变量）保留；其余 NOT_MUST 删除入台账。MUST 群出模板+配置收敛方案
  （引擎+声明式配置），实施与否由 owner 在方案上裁定。
- `wiki/audit/**`、`wiki/archive/**` 一字不动。已注册 AUDIT 工件若需删除，走 registry sunset
  数组（path/git_blob/last_commit，历史可达校验），沿用 07-28 机制。

## 机制

- 本役审计目录：`wiki/audit/md-script-consolidation-2026-07-29/`——`sunset-ledger.jsonl`
  （沿用 07-28 行 schema，decided_by=owner-2026-07-29）+ `sunset-digest.md`（WEAK 摘要与
  各链终局）。上一役 143 件脚本无台账欠账在本役 ledger 以
  `reason_class=SUNSET_TOOLING_BACKFILL` 回填。
- 每波收尾：涉 current 层则同 commit 重盖 manifest + ai-context manifest + package 回执；
  每波 `sf_current_package_check.py --check` PASS 后 commit+push。
- 波次：A=umbrella wiki+docs MD；B=根 MD 与 CLAUDE/AGENTS 瘦身；C=工程仓 MD（各仓独立
  commit）；D=脚本删除+143 回填；E=配置化方案（文档，交 owner 裁定后另行实施）。
- **scripts/tools/（owner 2026-07-29 裁决）**：设常驻目录存放日常反复使用的工程工具。现存
  fetch/登记线（sf_fulltext_fetch、sf_fulltext_ledger_status、sf_official_metadata_fetch、
  sf_atom_provenance_fetch）迁入；被删发现道工具若 R2-R9 重审确需，从台账恢复点按需恢复到
  此目录。迁移不动 10 条门禁绑定脚本的路径（code_graph 稳定性优先）；门禁外的日用工具才
  进 tools/。

## 验证

每波删除后：门禁 10 条 PASS、加载面无悬空、被删件抽样 `git show` 可恢复。盘点输入：两路
Opus 判级报告（MD 判级 / 脚本必用性+配置化），主会话逐表复核后执行。
