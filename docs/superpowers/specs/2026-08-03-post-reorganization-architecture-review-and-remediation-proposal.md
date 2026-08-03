---
title: "工程目录重整后架构复核与整改提案"
proposal_id: "PROGRAM-DIRECTORY-POST-MIGRATION-REVIEW-V1"
date: "2026-08-03"
addressed_to: "research engineering team, Fable5, and the research owner"
reviewed_umbrella_commit: "772e6ed15ac0006ddd34e0600b6f994230692eb8"
reviewed_study_commit: "53d9283d92059e7561c60a2b402af7bd5af074b8"
proposal_status: "PROPOSED_FOR_TEAM_REVIEW"
overall_assessment: "CONDITIONAL_ACCEPT_WITH_REMEDIATION"
execution_authority: "DOCUMENTATION_AND_GOVERNANCE_PROPOSAL_ONLY"
model_execution_effect: "NO_NEW_AUTHORITY"
---

# 工程目录重整后架构复核与整改提案

## 1. 给团队的结论

这次重整的**主架构选择是正确的**：伞仓承担 Stage‑1、研究治理、共享资产和实验索引；正式研究对象
使用语义名称建立独立 Git 仓；R/W 编号不再充当工程身份；W1–W4 本地 checkout 已退出活动工作区。
不建议推倒重来，也不建议把 study 重新并回伞仓。

但目前只能评为 `CONDITIONAL_ACCEPT_WITH_REMEDIATION`。目录的物理边界已经整理好，治理真相、历史
资产解析、独立构建能力和自动检查尚未同步完成。若现在直接进入模型触达，实验可以运行，却不能保证
另一台机器能从两个仓的提交记录重建同一环境，也不能保证历史证据引用仍可解析。

建议：**D1–D4 的无模型 E0 工作可以继续；首次模型触达和 R0 结果生成前，必须关闭本文 P0/P1 项。**
这不是重新讨论研究方向，也不涉及创新性或方法学裁决，只是让已经选择的目录架构真正可复现、可审计。

## 2. 本次复核看到的正确部分

1. 伞仓与 `studies/audio-aware-evidence-acquisition/` 都是干净 Git worktree；study 有独立 `.git`，
   `origin` 与 registry URL 一致，远程 `master` 为同一提交 `53d9283d...`。
2. 伞仓通过 `studies/*/` 忽略 study 内容，只跟踪 `studies/README.md` 与 `studies/registry.json`。
3. `projects/` 已从活动目录消失；W1–W4 远端以 cold backup 形式保留，四个 `master` HEAD 与 retirement
   tombstone 登记一致。
4. `Research-Objective.md`、study registry、experiment index 和 owner execution contract 已把首个
   study 路由到语义名称，且没有把 R2 写进仓名、包名和实验命名空间。
5. 现行 umbrella 四门全部通过：code graph、study workspace、AI context surface、AI context manifest；
   `common/tests` 为 21 passed、1 skipped；W1 snapshot 的 13 项 SHA‑256 全部核验通过。

这些结果说明不需要改变“两类仓 + 三个资产平面”的方向。问题在于现有检查主要验证结构存在，尚未
验证跨文件语义一致、远程依赖可重建和 study 是否拥有最低可执行质量门。

## 3. 缺陷与严重度

| ID | 严重度 | 缺陷 | 直接后果 |
|---|---|---|---|
| P0-1 | BLOCKER | HOT/管理文档与实际目录互相冲突 | AI 或团队可能把已获批 study 当成未获批，或继续向已删除 `projects/` 路由工作 |
| P0-2 | BLOCKER | 574 条 legacy experiment asset 全部为 `unresolved`，但 workspace gate 仍 PASS | 历史 claim 看似存在，实际路径不可解析；审计链断裂 |
| P1-1 | MAJOR | study 的独立性只成立在 Git 层，不成立在构建/依赖层 | 单独 clone study 无法按声明重建环境；`../../common` 是未锁定的隐式依赖 |
| P1-2 | MAJOR | study 没有任何测试、lockfile、CI 或 license/notice | `pytest` 输出 `no tests ran`；远程仓目前只有目录骨架，不能作为 R0 fail-closed 基线 |
| P1-3 | MAJOR | registry/workspace checker 只做浅层存在性检查 | 假 `.git`、错误 origin、缺失已登记 checkout、Wiki/registry 状态漂移都可能漏检 |
| P1-4 | MAJOR | W1 snapshot 的数量、来源 commit、远端状态与迁移记录不一致 | 13 个文件被写成“十个”；新增 3 项没有同等粒度的 adoption 登记，来源叙述自相矛盾 |
| P2-1 | MINOR | `common/` 的身份仍停留在“四个 work repo 的共享库” | 已退役 W/W4 术语继续塑造新 study；模块是否真为跨 study 共用没有可机检证据 |
| P2-2 | MINOR | 已实施的旧 proposal/spec 仍以 `WITHHELD`/未建仓/保留 projects 的口吻留在 active specs | 后续协作者可能误用过期实施说明，而不是现行 architecture/contract |

## 4. P0-1：统一当前真相

### 4.1 证据

- `wiki/Research-Objective.md` 与 `studies/registry.json`：1 个 study 已获 owner GO，当前为 Stage‑2A E0。
- `wiki/Experiment-Assets.md`：仍写“Admitted study repositories: 0”、等待 execution contract，且写
  W1–W4 仍位于 `projects/`。
- `wiki/Project-Thesis.md`：repository table 仍把 W1–W4 的已删除本地路径列为当前 repository classes。
- `docs/superpowers/specs/2026-08-02-study-repositories-and-experiment-assets.md`：仍写“keep W1–W4 in
  projects”和“create no nested study repository yet”。
- `docs/superpowers/specs/2026-08-02-fable5-study-directory-reorganization-proposal.md`：仍为
  `PROPOSED_FOR_REVIEW`、`remote_repository_creation: WITHHELD`，目标树仍含 `projects/`。

### 4.2 修改建议

在一个 umbrella truth-alignment transaction 中完成：

1. 把 `wiki/Experiment-Assets.md` 更新为：1 个 admitted study、owner GO 已签、E0 进行中、W1–W4
   本地退役、远端 cold backup；删除“573 live / 1 history-only”等旧统计。
2. 把 `wiki/Project-Thesis.md` 的 repository table 改为三类：umbrella、admitted studies、retired
   cold-backup provenance。W1–W4 不再以活动路径出现。
3. 将两份 2026-08-02 architecture proposal 标记为 `IMPLEMENTED_AND_SUPERSEDED_2026-08-03`，正文顶部
   指向 `docs/architecture.md`、owner contract 和本提案。保留历史设计理由，但不得继续充当当前操作说明。
4. owner contract 中“回滚后 W1–W4 不受影响”的句子不应原地改写；新增 dated amendment，澄清本地仓已
   退役，回滚只影响 study 与 umbrella registry，不会恢复旧 worktree。
5. 更新 `common/README.md` 的“四个 works / W4 flagship / each work repo”旧语义。
6. 重建 AI context manifest，并新增跨源事实断言：registry study count、Experiment‑Assets count、HOT
   endpoint、study index frontmatter 必须一致。

## 5. P0-2：让 legacy evidence 从“存在清单”变成“可解析资产”

### 5.1 证据

`docs/integrity/experiment-asset-inventory.json` 当前记录：

```text
recorded_entries = 574
worktree_present = 0
history_only = 0
unresolved = 574
```

这是删除本地 W1 后的真实结果，但 `study_workspace_check.py` 只比较“生成结果是否和文件一致”，没有把
非零 unresolved 当成失败，因此仍报告 PASS。与此同时，`docs/claim_ledger.yaml` 和
`docs/corpus.lock.json` 仍包含大量 `projects/...` 路径和已失效的本地复现命令。

W1–W4 cold-backup remotes 在本次复核中仍可访问，且 `master` 与 tombstone 的 final HEAD 一致。因此
这里不是证据已经丢失，而是**解析器没有理解 retired remote authority**。

### 5.2 修改建议

1. 新建 `docs/integrity/retired-repository-registry.json`，每个退役仓至少登记：
   `repo_id`、remote URL、final branch/commit、retention policy、verified_at、tombstone、local state。
2. 将 legacy resolver 从两态扩展为四态：
   `WORKTREE_PRESENT`、`LOCAL_GIT_HISTORY`、`COLD_BACKUP_RESOLVED`、`UNRESOLVED`。
   `projects/<repo>/<path>` 应解析成 `remote@final_commit:path`，而不是直接判 unresolved。
3. 生成 `docs/integrity/legacy-asset-resolution.json`：574 条逐项绑定 remote、commit、path 和可选 blob
   hash。目标是 `unresolved = 0`；确实无法恢复的条目必须有 owner waiver 和原因，不能静默通过。
4. 给 `study_workspace_check.py` 增加 fail-closed 规则：`UNRESOLVED > 0` 即失败，除非每项都有带日期
   waiver；cold backup 的 branch HEAD 漂移不影响已冻结 commit，但定期验证 commit 可获取。
5. `docs/claim_ledger.yaml` 不必把 574 条内容复制回来；把死路径升级为 resolution key 或
   `git+https://...@commit#path=` URI。`docs/corpus.lock.json` 的再生成命令必须指向仍可获取的 commit/
   snapshot，或明确标为 retired/non-runnable。
6. 为避免 GitHub 成为唯一备份，建议在 `SPEECHRL_DATA_DIR/program-archives/` 保存四个 `git bundle`，
   并在 umbrella manifest 登记 bundle SHA‑256。bundle 不进入 Git。

## 6. P1-1：修复独立 study 的依赖合同

### 6.1 证据

study `pyproject.toml` 没有 runtime/dev dependencies，也没有声明 `speechrl-common`；但 README、AGENTS
和 migration manifest 都要求：

```bash
uv pip install -e ../../common -e .
```

这意味着它只能在当前伞仓相邻目录布局中工作，且每次安装消费的是 umbrella `common/` 当前 worktree，
没有 commit pin。独立 Git 历史无法单独解释一个实验使用了哪一版 common。

### 6.2 修改建议

短期建议采用“**远程精确 pin + 本地 editable override**”：

1. 在 study `pyproject.toml` 声明实际使用的依赖与 dev extra；在首次真正 import `speechrl_common` 前，
   将其绑定到 umbrella 的精确 commit/subdirectory，生成并提交 `uv.lock`。
2. `../../common` 只作为开发 override；CI 和 release reproduction 必须从锁定 commit 安装。
3. 每个 experiment record 增加 `shared_code_revision`，即使 study commit 不变也能识别 common 漂移。
4. 当前 study 源码尚未 import `speechrl_common`，所以也可以在 R0 前先删除“ACTIVE dependency”声明；
   真正消费第一个模块时再以精确 pin 加入，避免提前依赖整个 legacy-rich common 包。
5. 当至少两个 admitted study 真正消费同一能力后，再决定把 `common/` 抽成独立版本化仓/包；现在不为
   追求形式独立而再创建一个无人复用的仓。

## 7. P1-2：把 study 骨架变成最低可执行工程基线

### 7.1 证据

- `pytest` 在规定的 WSL2 Python 3.12 环境中没有收集到任何测试。
- `configs/*` 与 `tests/*` 只有 `.gitkeep`。
- `scripts/reproduce.sh` 和 `scripts/evaluate.sh` 只打印“R0 slice not delivered”并退出 2。
- 没有 `uv.lock`、CI workflow、`LICENSE` 或 third-party notice。

在 E0 期间这些 placeholder 可以存在，但不能被称为已经完成的 engineering foundation，更不能在首次
模型调用后才补测试，因为届时信息边界与 trace 合同已经可能被错误实现。

### 7.2 修改建议

首次模型触达前至少交付以下**无模型 contract tests**：

1. registry、owner contract、experiment index、study origin 和 package identity 相互一致；
2. 三个 carrier lock key 与模型 lock key存在，loader 不把数据字节写进 Git；
3. gold/reference transcript/test annotation/future turn 字段在 runtime request schema 中 fail-closed；
4. OBS 与 SUPPLY trace 字段分离，request/response/tool/cost 均可序列化并 hash；
5. exposure ledger schema 可校验，模型入口在 E0/runtime receipt 缺失时必须拒绝；
6. `reference/w1-snapshot/` 不在 package discovery/import path 中；
7. `reproduce.sh`/`evaluate.sh` 的 pre-E0 拒绝行为本身有测试，而不是只靠人工阅读。

同时：

- 用最小实际 YAML/schema/README 取代 config `.gitkeep`；
- 提交 `uv.lock`，增加 `python -m build` 和 `pytest` CI；
- 明确私有阶段的 license policy，并为 W1 snapshot 添加来源 license/NOTICE；
- 质量门要求“至少收集一个测试且全部通过”，避免 `no tests ran` 被 CI 误当成成功。

## 8. P1-3：升级 registry 与 workspace checker

当前 checker 做到了 slug、路径、字段集合、decision/index 文件存在和“未登记目录不得出现”，但仍有
四个盲点：

1. registered study 不安装时不会失败；只检查 `installed - registered`，不检查反向差集；
2. `.git` 只检查路径存在，不验证它是真 Git 仓；
3. 不验证 nested repo 的 `origin`、branch、remote HEAD 是否匹配 registry；
4. 不解析 experiment index frontmatter，也不检查 Experiment‑Assets 中的 admitted count/state。

建议 registry schema v2 增加稳定身份字段：`default_branch`、`package_name`、`created_at`、
`experiment_namespace`、decision-record Git blob。不要把每个实验 commit 放进 registry；实验 commit
仍属于 Wiki ledger。

建议 checker 增加两种模式：

- 默认模式：允许未 checkout 的 private study，但验证 registry、Wiki、decision、remote identity；
- `--require-installed`：供主开发机使用，要求所有 lifecycle=`engineering|validation` 的 study 已安装，
  `git rev-parse` 成功、origin 匹配、branch policy 合法。

另在每个 study 仓配置自己的 CI；umbrella `code_graph_check.py` 只覆盖 umbrella 的 20 个 trusted nodes，
不应被理解为已经验证 nested study code。

## 9. P1-4：修复 W1 snapshot provenance

当前 snapshot 的 SHA‑256 是完整的，13/13 均通过；问题在记录层：

- migration manifest 与 retirement tombstone 写“十个文件”；实际为 13 个；
- `repro_asr_best_of_n_v2.py`、`repro_asr_best_of_n_llamacpp.py` 和 `gpu_session.sh` 来自不同历史 commit，
  没有进入与其他候选同粒度的表格；
- snapshot 文档仍写 remote 被删除，而 tombstone addendum 和现场验证确认 remote 被保留；
- 两个 legacy runner 内含硬编码 `/mnt/d/.../common/src`，目前因未集成而无害，但不得原样晋升到 `src/`。

建议：

1. 将 snapshot manifest 改为每文件一行：原 repo、原路径、source commit、SHA‑256、license、当前状态、
   adoption target；数量统一为 13。
2. 统一措辞为“local checkout retired; remote retained as cold backup”。
3. 将 13 项状态设为 `QUARANTINED_REFERENCE_NOT_EXECUTABLE`；任何进入 `src/` 的文件必须新增 dated
   adoption row、去除绝对路径、补测试并重新 hash。
4. 增加静态检查，禁止生产源码 import `reference.w1-snapshot` 或把 reference 目录加入 `sys.path`。

## 10. P2：收缩 common 与清理过期说明

`common/` 可以继续留在 umbrella，但应重新做一次 module-level ownership audit：

- `audio/io`、data-root、轻量 tracking 等若确实是 program infrastructure，可保留；
- `omni_embed`、`disentanglement`、W4 probe 等只有退役 work 消费的模块，应标记 legacy、迁出活动 API，
  或等待真实新消费者后再恢复；
- 新能力只有两个 admitted study 实际消费后才能晋升 shared；
- 建议新增 `common/OWNERSHIP.md`，逐模块记录 consumer study、owner、stability 和 deprecation 状态。

旧 proposal/spec 不必删除。历史理由有价值，但必须用 frontmatter/tombstone 明确其实施状态；当前操作只
从 `docs/architecture.md`、`wiki/Research-Objective.md`、`wiki/Experiment-Assets.md` 和 owner contract
进入。

## 11. 建议的实施交易顺序

| 交易 | 所属仓 | 内容 | 是否阻断模型触达 |
|---|---|---|---|
| T0 truth alignment | umbrella | 修正 Experiment‑Assets、Project‑Thesis、active spec 状态、common README，重建 manifests | 是 |
| T1 legacy resolution | umbrella | retired repo registry、remote-aware resolver、574 项 resolution、claim/lock 路由、checker fail-closed | 是 |
| T2 minimum study gate | study | dependencies/lock、contract tests、CI、license/NOTICE、真实 config skeleton | 是 |
| T3 dependency pin | study + umbrella | 精确 common revision；experiment ledger 增加 shared-code pin | 是 |
| T4 snapshot correction | study + umbrella tombstone/amendment | 13 项逐文件 provenance、remote 状态和 quarantine rule | R0 前完成 |
| T5 common module audit | umbrella | consumer/ownership/deprecation 清单与模块收缩 | 可在 R0 后、X 前完成 |

跨仓不能假装原子 commit。协调顺序应为：先让被引用 authority 在所属仓提交并取得 commit/blob，再让消费
仓 pin 它，最后由 umbrella Wiki ledger 记录 study commit。不得在两个仓都写“latest”。

## 12. 验收标准

### Umbrella

```text
python scripts/checks/code_graph_check.py
python scripts/checks/study_workspace_check.py --require-installed
python scripts/checks/legacy_asset_resolution_check.py
python scripts/checks/ai_context_surface_check.py
python scripts/checks/build_ai_context_manifest.py --check
pytest common/tests
```

要求：current truth 无冲突；legacy `UNRESOLVED=0`；installed study origin/branch 与 registry 一致；AI
manifest green；common 每个活动模块有 consumer/owner 状态。

### Study

```text
uv sync --frozen
python -m build
pytest -q
```

要求：测试收集数大于 0；无模型 contract tests 全绿；E0/runtime receipt 缺失时模型入口 fail-closed；
snapshot 不可 import；lockfile 与依赖 pin 已提交；CI 在干净 clone 中复现。

### 文档与审计

- registry、Research‑Objective、Experiment‑Assets、experiment index 对 admitted count/state 一致；
- owner contract 不被原地改写，退役后的澄清走 dated amendment；
- 两份旧 proposal 明示 superseded/implemented；
- D1–D4 继续登记为 E0，无任何创新性、方法有效性或实验结果主张。

## 13. 请求团队裁决

请团队逐项回复：

1. 是否接受总体裁决 `CONDITIONAL_ACCEPT_WITH_REMEDIATION`？
2. 是否同意 T0–T3 为首次模型触达前的硬门？
3. legacy cold backup 是否同时制作离线 `git bundle`，还是只依赖 GitHub private remotes？
4. `common` 短期采用精确 umbrella commit pin，还是在第二个 study 出现前暂不依赖？
5. 谁负责 umbrella T0/T1，谁负责 study T2/T3/T4？

建议团队批准本整改提案后，先执行 T0 与 T1；Fable5 在 study 仓并行执行 T2–T4。完成后再由一次
post-remediation review 签发“R0 engineering foundation ready”，而不是把目录存在等同于工程基建完成。
