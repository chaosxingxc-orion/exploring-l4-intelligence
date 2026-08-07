---
title: "Speech-aware evidence acquisition R0 script-engineering independent rereview assessment"
date: "2026-08-07"
artifact_type: "INDEPENDENT_AI_DOCTORAL_SUPERVISOR_AND_SCRIPT_ENGINEERING_ADVISORY_REREVIEW"
campaign: "speech-aware-evidence-acquisition-r0-review"
round: "independent-rereview-2026-08-07"
umbrella_commit_reviewed: "0c4ea0607cae27e4c4a3e23000ffaa7339350395"
study_commit_reviewed: "8aa85847e510bfbd43eeeb4ef09d8d3b63b1cbf9"
reviewer_context: "Codex primary agent; five-round adversarial analysis; no delegated subagents; model-free inspection and verification only"
review_rubric: "trusted-operator, single-machine, serial research scripts; judge simplicity, repeatable capability, recoverable rerun, and ability to complete the job; do not require production robustness or completeness"
verdict: "R0_OVERALL_INCOMPLETE__R0_2_REPAIR_REQUIRED_FOR_BROKEN_OPERATOR_PATH__R1_MODEL_FACING_EXECUTION_WITHHELD"
human_signature_claimed: false
owner_authority_claimed: false
model_touch_performed: false
repository_modified_by_reviewer: true
modification_scope: "this rereview report and its campaign index only"
git_blob: "PENDING_FIRST_COMMIT"
---

# Speech-aware evidence acquisition：R0 独立复评 assessment

## 0. 结论先行

本次复评不接受“R0 已有效完成”的总体结论。更准确的判断是：

> **R0.2 的库级工程底座和 model-free 合成执行链已经基本搭成，前次 P0/P1 信任边界问题也大体得到实质修复；但当前正式 CLI 和 R0 smoke runbook 不能按文档完成一次真实 run/score/finalize，因此 R0.2 尚需一次很小但阻塞性的 operator-path repair。R0.1 仍是空模板，R0.3 未获授权、未执行，所以 R0 整体明确未完成。**

精确 verdict：
`R0_OVERALL_INCOMPLETE__R0_2_REPAIR_REQUIRED_FOR_BROKEN_OPERATOR_PATH__R1_MODEL_FACING_EXECUTION_WITHHELD`

这不是对研究方向的否定，也不是要求把研究脚本改造成生产系统。相反，本报告采用 owner 明确给出的轻量标尺：单机、串行、可信操作者；工程要简洁，能力可重复，能够完成工作即可。在这个更宽松的标尺下，真正阻塞结论的不是并发、签名、WORM、分布式事务或极端篡改，而是**官方写出的命令今天就不能执行到工作结果**。

## 1. 本次到底评什么

### 1.1 R0 不是一个单点

生效设计把 R0 分成三个出口：

- **R0.1**：model-free readiness memo 与 innovation ledger；出口是 owner 选定 R1 基线。
- **R0.2**：model-free 工程基线；出口是测试通过、双仓 gate 绿，并有可操作的统一执行路径。
- **R0.3**：真实模型 smoke `SAEA-E-001`；出口是 trace 完整、计划与实际用量吻合、hash/产物齐全。

因此，“R0.2 写了很多代码”和“R0 完成”不是同一件事；“单元测试能直接调用 `main()`”与“操作者按 runbook 能跑通”也不是同一件事。

### 1.2 明确排除的生产级要求

以下项目不进入本次否决依据：

- 多进程并发消费同一 run quota 的竞态；本评审只要求串行运行，并将“禁止并发跑同一 run”视为操作边界。
- run bundle 的外部真实性证明，以及 GGUF 快路径无法识别保留 size/mtime/file-id 的原位换字节；owner 已于 2026-08-07 接受为 R0 边界。
- entity/QA scorer adapter；owner 已明确移出 R0。
- 全局首切片数值预算帽；2026-08-06 amendment 已废止，只有逐 run 自洽、预登记和一次性 attempt 仍有效。
- 自动扩缩容、高可用、跨机恢复、恶意操作者防护、复杂重试框架。

这些排除项保证本报告没有用“生产完备性”惩罚一个脚本化研究工程。

## 2. 五轮对抗式分析

### Round 1：承诺—实现映射

把 owner contract、Stage-2A entry、discovery-slice design、vertical-slice plan 逐项映射到 study 的代码、配置、测试、runbook 和研究产物。重点区分五种状态：接口存在、合成测试通过、正式配置可实例化、操作者入口可执行、真实模型结果已产生。

### Round 2：正向可执行验证

在指定 WSL2/Python 3.12 环境、当前 clean commit 上执行测试、构建、runtime gate 和 umbrella gates，确认底层不是纸面实现。

### Round 3：可信操作者照抄 runbook

不构造恶意输入，只按官方文档寻找最短路径：生成 plan、准备 session、执行 run、score、finalize、写 MLflow/ledger。这里发现的是正常使用即触发的断点，而非边界攻击。

### Round 4：研究主张反证

检查是否已有真实模型输出、readiness-qualified prior、联合指标表、wiring memo，防止把“测量设施具备”偷换成“方法有效”或“既定研究目标达成”。

### Round 5：反驳与降级

逐条尝试用“这是 R1/X 延期项”“这是 owner 接受边界”“这是生产级要求”反驳 finding。被成功反驳的项目从缺陷中移除；最终保留的阻塞项都直接作用于 R0 已承诺的脚本执行能力。

## 3. 正向证据：已经做对的部分

### 3.1 当前提交的验证结果

| 检查 | 当前结果 | 解释 |
|---|---:|---|
| study `pytest -q` | `712 passed, 8 skipped`，24.89s | 库级、contract、合成路径覆盖广，model-free |
| `python -m build` | PASS | sdist 与 wheel 成功构建 |
| `scripts/reproduce.sh` | PASS，exit 0 | 当前磁盘 receipts/runtime/E0 gate 可打开；无模型调用 |
| 重复 `scripts/reproduce.sh` | PASS，约 1.6s | 缓存热后可稳定重复执行同一 model-free 核验能力 |
| umbrella `code_graph_check.py` | PASS | 24 trusted nodes |
| `study_workspace_check.py` | PASS | study 与 experiment routing 一致 |
| `legacy_asset_resolution_check.py --verify-bundles` | PASS | 574 bindings、4 bundle hashes、0 unresolved |
| paper/workspace/context/manifest gates | 全 PASS | 伞仓治理面当前可通过 |
| `ruff check src` | FAIL，1 个 F841 | `contracts/ledger.py:135` 未使用变量；不影响能力，但当前 CI lint job 会红 |

### 3.2 工程能力中可判 PASS 的部分

- deterministic carrier loader、split receipt 与 live recomputation 已实现并有真实资产门禁。
- frozen-core adapter、payload/media/evidence/reference identity、session/attempt、四轴 trace、run bundle、finalizer 和成本采样均有实质代码与大量正反测试。
- bare-core、fixed legal context、mismatched evidence 和 fixed-retrieval 三种 D2 payload 形状在正确 carrier 配对下可经 fake transport 完成合成 run。
- mismatched evidence 是确定性 derangement，不依赖随机漂移。
- oracle 的 R0.2 合同本来就定义为“runtime 一律拒绝、具体上界随首次 probe 冻结”；当前 `OracleEvidenceError` 符合该接口，不应被误判成 R0.2 缺失。
- fixed-retrieval 的 vertical-slice 工程计划只承诺“预取证据 + query 字段”的固定 payload 形状，并未承诺 R0 内实现检索引擎；当前实现与该窄合同一致。后续论文中不得把它表述成已经验证了检索质量。
- MLflow 全 bundle 上传和 machine-derived ledger row 的库函数与测试已存在。

前次 review 指出的 split 自信任、carrier/media 未绑定、attempt 复用、session 身份、bundle 闭包等核心问题，当前未再发现同等级的串行使用反例。修复是实质性的，不应因为下面的入口回归而被一笔抹掉。

## 4. 阻塞性 findings

### B1 — 官方 driver 模块入口在当前提交不可执行

**严重度：Blocking；归属：R0.2 operator path。**

R0 repair 把原来的 `core/driver.py` 重构成 `core/driver/` package。`core/driver/__init__.py` 虽然保留了：

```python
if __name__ == "__main__":
    sys.exit(main())
```

但 `python -m some.package` 只查找 `some/package/__main__.py`，不会把 package 的 `__init__.py` 当作模块入口。当前 package 没有 `__main__.py`，`pyproject.toml` 也没有 `[project.scripts]` console entry。

实测：

```text
$ python -m speech_aware_evidence_acquisition.core.driver --help
No module named speech_aware_evidence_acquisition.core.driver.__main__;
'speech_aware_evidence_acquisition.core.driver' is a package and cannot be directly executed
```

直接后果：

- runbook 的 `...core.driver run` 不可执行；
- `scripts/evaluate.sh --manifest ...` 和 `--outputs ...` 都不可执行；
- runbook 的 `...core.driver finalize` 不可执行；
- 因此正式 run、权威 scoring、finalize/ledger/MLflow 链在 operator 层同时断开。

测试没有发现它，是因为 unit tests 直接 import 并调用 `driver_main([...])`；CI 的入口测试只测 `evaluate.sh --help` 和无参数分支，这两条路径在 shell 内提前退出，从未真正 dispatch 到 Python module。现有 712 项测试证明内部函数很强，但不能证明打包后的官方命令可用。

这是本次最明确的“工程实现有遗漏”：不是缺生产健壮性，而是缺少两三行 `__main__.py` 或一个 console script，再加一个 subprocess smoke test。

### B2 — R0 smoke runbook 与当前 CLI/plan 合同不自洽

**严重度：Blocking；归属：R0.2→R0.3 交接。**

即使补上 B1，照抄 `docs/runbooks/2026-08-05-r0-smoke.md` 仍不能完成 smoke：

1. runbook 声称 plan values 可“verbatim”实例化，但清单没有 `attempt_id`。`ExecutionPlan.validate()` 为兼容 E0 dry-run 允许其缺省；真正 model path 会在 `FrozenCoreAdapter` 构造时明确拒绝空 `attempt_id`。
2. `driver run` 当前要求 `--session-receipt`，runbook 命令没有这个参数。
3. runbook 只要求一个已运行的 llama-server，没有给出如何调用受支持的 `start_session(...)` 并持久化 receipt 的脚本或命令。可信操作者需要自己阅读 Python API、拼接参数，无法从 runbook 闭环。
4. runbook 把 finalize 描述为“score + upload + machine-derived ledger row”，但命令只传 `--manifest`。代码只有在显式提供 `--tracking-uri` 时才调用 `log_bundle`；按 runbook 执行会跳过 MLflow 上传，`mlflow_run_id` 为 `None`。
5. protocol hash、speech seconds、attempt directory、session receipt、tracking URI 分散在多处，由操作者手工拼装。单项都能理解，但整体并不是一个简洁、可重复的研究脚本入口。

这说明 R0.2 的内部组件虽然齐，**工程方案在最后一公里没有完成集成**。R0.3 目前尚无授权，所以“没有真实执行”不是实现者越权；但 runbook 在授权到来后仍无法工作，是当前就可以且应该修复的工程问题。

### B3 — R0.1 与 R0.3 尚未完成，不能把 R0.2 交付等同于 R0 完成

**严重度：Stage verdict blocker；归属：R0 overall。**

- `docs/readiness/2026-08-05-prior-readiness-memo.md` 仍是 `TEMPLATE`，OBS、ORG/SUPPLY、USE、OVERALL 全为 `(fill)`。
- `docs/innovation-candidates.md` 仍为 `(no entries yet)`。
- owner 尚未选择 R1 baseline。
- `docs/runbooks/2026-08-05-r0-smoke.md` 明示 `NOT EXECUTED`。
- owner decision 记录明示 SAEA-E-001 authority 仍未授予、没有 model touch。
- 没有真实 trace/bundle/scores/MLflow run/wiring-integrity memo，也没有 effectiveness/reasonableness/efficiency 联合表。

因此：R0.1 = `NOT_DONE`，R0.3 = `NOT_AUTHORIZED_NOT_RUN`，R0 overall 必须为 `INCOMPLETE`。这是阶段事实，不应包装为工程质量批评，也不应通过无授权模型调用来“补证”。

## 5. 非阻塞但必须如实记录的问题

### N1 — 当前 CI 并非全绿

`ruff check src` 在 `src/speech_aware_evidence_acquisition/contracts/ledger.py:135` 报 F841：`n = len(line)` 未使用。修复成本极低，不影响能力；但 study `docs/engineering.md` 仍写“src clean”，repair submission 的“zero defects”也不能覆盖当前事实。

### N2 — current/audit 状态叙事已有漂移

- `wiki/Research-Objective.md` 的 `last_refresh` 仍是 2026-08-05，仍称 repair 在 `r0-repair` 分支进行；实际 repair 已合入 study `master`。
- repair submission 的 front matter、正文 banner 和当前提交分别指向不同 study commit；它只能作为历史 submission，不能替代本次对 `8aa8584...` 的复评。
- campaign index 仍把已提交的 repair submission 标成 `PENDING_FIRST_COMMIT`；本次只按原 index 指令把它补为实际 blob，不改旧 audit artifact bytes。

这些是治理面清理项，不影响底层程序运行，但会让后来 reviewer 错判“现在到底在哪一步”。

### N3 — 串行是当前能力边界

同一 run 的并发 attempt 不作为本次否决项。当前结论只对单机串行操作者成立；在文档中加一句“同一 run 不得并发执行”即可。除非未来运行方式改变，不建议为此引入锁服务或数据库。

## 6. 承诺完成度矩阵

| R0 承诺 | 判定 | 证据与限制 |
|---|---|---|
| E0 D1–D4 + runtime gate | PASS | 当前真实资产 dry-run 打开，umbrella gates 全绿 |
| discovery/confirmatory carrier loader 与 split | PASS（model-free path） | 两 carrier loader/receipt 存在；confirmatory 结果按合同仍未读 |
| frozen-core adapter | PASS（库级/合成） | fake transport 与大量 contract tests 通过；真实 CLI 尚未到达它 |
| OBS/ORG/SUPPLY/USE traces | PASS（库级/合成） | trace/bundle verification 有测试；真实 R0.3 trace 不存在 |
| ASR WER + cost scorer adapters | PASS | owner 已把 entity/QA adapter 移出 R0 |
| bare / fixed context / fixed retrieval | PASS（窄工程合同） | 正确 carrier 配对可合成跑通；fixed retrieval 是固定 query+预取证据 payload，不是检索器 |
| mismatched evidence negative control | PASS | deterministic derangement，有端到端 fake-transport 证据 |
| oracle upper-bound interface | PASS（接口） | runtime 明确拒绝；实际上界算法/结果留到首个使用 probe |
| run bundle / score / finalize | PARTIAL / BLOCKED | 库函数通过；官方 `python -m ...driver` 入口不可执行 |
| MLflow + umbrella ledger linkage | PARTIAL | 库函数存在；runbook finalize 未传 tracking URI，未有真实产物 |
| calls/tokens/latency/GPU/CPU/audio/evidence bytes | PASS（实现与合成） | 真实 R0.3 数值尚无；GPU/CPU scope按当前 sampler 设计解释 |
| R0.1 readiness + innovation ledger | NOT DONE | 仍为空模板，owner 未选 R1 |
| R0.3 SAEA-E-001 smoke | NOT AUTHORIZED / NOT RUN | 不应越权执行；runbook 还需先修 |
| first-slice joint table + decision memo | NOT DONE | 依赖后续 R1/X 实验，不是 R0.2 已完成证据 |

## 7. “能力幂等、工程简洁”的专项判断

### 7.1 能力可重复性

底层重复性是好的：配置 hash、split identity、receipt、确定性 mismatch、bundle hash 和 gate 都有清楚约束；`reproduce.sh` 在缓存热后可快速重复成功。合成 run 也显示相同输入能进入同一逻辑路径。

但 operator 层尚不能称为幂等或易重跑：同一 attempt 按治理要求必须一次性，失败后要人工同时更换 `attempt_id`、run directory、exposure 记录和若干路径。这里不应取消一次性语义，而应由一个薄 wrapper 自动生成 fresh attempt 并打印所有产物位置。理想语义是“同一个实验意图可安全重试”，不是“强行复用同一个 attempt”。

### 7.2 工程简洁性

当前 study 约有 84 个 `src` Python 文件、12,961 行源码，以及 41 个测试文件、12,802 行测试。文件拆分降低了单文件长度，但并未降低操作者认知成本；一个 R0 smoke 仍要求跨 plan、ledger、session、driver、evaluate、finalize、tracking 多层手工操作。

代码量本身不是缺陷，已写且有用的安全约束也无需为了“简洁”大删。真正需要简化的是**外部操作面**：内部可以有 84 个文件，操作者应只需要一个明确入口。当前恰好相反——内部抽象完整，入口断了。后续不要继续扩展基础设施，先让一条 happy path 真实跑通。

## 8. 博导视角的研究判定

1. **目前不能判断方法有效。** 没有真实模型结果，Effectiveness、Reasonableness、Efficiency 三门都没有观测值。
2. **目前能判断测量设计方向合理。** 四轴分离、负对照、合法 evidence boundary、wrong-to-correct/correct-to-wrong、成本记账构成了可信的研究骨架。
3. **readiness 是当前科学阻塞。** closest prior 尚未完成逐轴可运行性判定，R1 对象未选；在这之前谈创新优势或进入 X1/X2/X3 都缺校准锚。
4. **R0.3 只证明 wiring。** 即使 smoke 成功，也只能证明模型请求、trace、score、bundle、cost、MLflow 的链条工作，不能证明研究假设成立。
5. **固定检索命名要克制。** 当前 arm 是“固定 query 与预取 context 的输入形状”；未来若要声称 retrieval 改进，必须另有真实检索/选择过程和 recall/precision 证据。

研究结论：方向与实验骨架值得继续，但 R0 尚未产生任何支持“能力提升”或“研究目标已达成”的证据。

## 9. 资深脚本工程师视角的判定

1. 内部架构已经超过“能写脚本”的最低线，关键身份和产物绑定扎实。
2. 712 项测试仍漏掉官方命令不可执行，说明测试分层失衡：大量内部不变量被验证，最短 operator smoke 却没有。
3. runbook 与 CLI 在一次重构后发生漂移，且 CI 只测 help/no-args；这是典型的“组件正确、产品路径坏掉”。
4. 不需要引入新框架。一个 `__main__.py`、一个真实 subprocess test、一个薄 smoke wrapper 和一份同步 runbook 足以关闭主要工程问题。
5. 在完成首次真实 smoke 前，不建议继续增加防御性模块、抽象层或新 scorer；先验证现有底座能完成工作。

工程结论：基础组件多数可用，但交付面尚未达到“脚本能把工作做完”。R0.2 应判 `REPAIR_REQUIRED`，而不是重新设计。

## 10. 最小整改清单

按依赖顺序，只做下面这些即可申请下一次复核：

1. **恢复一个真实 CLI 入口。** 增加 `core/driver/__main__.py` 调用 `main()`，或在 `pyproject.toml` 注册 `saea-driver`；二选一，不要重复造层。
2. **增加两个 subprocess 级测试。** 至少验证安装后的 `python -m ...core.driver --help` 能成功 dispatch，以及 `scripts/evaluate.sh --outputs <synthetic>` 确实进入 scorer，而不是只测 shell 的 help 分支。
3. **把 smoke 收敛成一个薄入口。** 推荐 `scripts/r0-smoke.sh` 或一个 CLI `smoke` 子命令：生成/校验 plan（含 fresh `attempt_id`）、启动并写 session receipt、执行 run、finalize 时显式传 local MLflow URI、最后打印 manifest/scores/ledger/MLflow id。无需做通用 workflow engine。
4. **同步 runbook。** 补齐 `attempt_id`、`--session-receipt`、session 创建命令、`--tracking-uri`、失败后 fresh attempt 的唯一操作；确保文档命令可复制执行。
5. **修掉 lint 单点并扩 CI。** 删除未使用的 `n`，让 `ruff check src` 恢复 0；CI 必须覆盖真实 module/console dispatch。
6. **完成 R0.1。** 填 readiness memo、记录不可运行 prior、由 owner 选 R1；不需要模型调用。
7. **获得 owner 授权后执行一次 R0.3。** 只跑约定 subset10，产出完整 bundle、score、成本、MLflow 与 wiring memo。不要借机扩大实验规模。
8. **最后更新 HOT current truth。** 把 repair 已合并、fresh review 结论、R0.1/R0.3 当前状态写回 `wiki/Research-Objective.md`。

复核门只需要看到：CLI subprocess 通过、runbook dry instantiation 无缺字段、lint 通过、R0.1 已闭合，以及 owner 授权后的 SAEA-E-001 产物。无需追加生产级 hardening。

## 11. 最终回答

### R0 承诺的功能是否有效完成？

**没有整体完成。** 多数 R0.2 库级功能已有效实现，但正式命令入口和 runbook 不能把这些组件串成一次可执行工作；R0.1、R0.3 均未完成。

### 是否完成既定目标？

**没有。** 当前完成的是大部分 measurement/wiring foundation，不是 readiness、真实 smoke，更不是方法有效性或研究假设验证。

### 在研究课题的工程基座上，是否完成了所有工程方案？

**组件层接近完成，交付层未完成。** loader、gate、adapter、trace、bundle、scorer、tracking library 大多已落地；官方 CLI、session/plan/run/finalize/MLflow 的一条简洁 happy path 没有闭环。

### 工程实现是否有遗漏或漏洞？

**有三个与当前脚本目标直接相关的遗漏：** package 重构后缺可执行入口；runbook 缺 attempt/session 必需项；MLflow finalize 文档与实际参数不一致。另有一个低成本 lint 回归和若干 current/audit 叙事漂移。并发、外部真实性和极端篡改问题已按本次标尺排除，不作为整改要求。

本报告是 AI reviewer advisory，不替代 owner 签字，不授予 model touch，也不改变现有 exposure/Stage-3 stop line。
