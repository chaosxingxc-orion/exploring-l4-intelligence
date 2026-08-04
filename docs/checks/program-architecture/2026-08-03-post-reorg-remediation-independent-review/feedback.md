---
title: "工程目录重整整改：独立复核反馈"
review_id: "PROGRAM-DIRECTORY-POST-MIGRATION-INDEPENDENT-REVIEW-2026-08-03"
date: "2026-08-03"
addressed_to: "research engineering team and Fable5"
reviewed_umbrella_commit: "75406d4d74b63192cbcbf4177b91b4f1d06557c7"
reviewed_study_commit: "ac75a61104a994d77a259b9aa0f8a5e8f51dee66"
reviewed_umbrella_remote_commit: "772e6ed15ac0006ddd34e0600b6f994230692eb8"
reviewed_study_remote_commit: "53d9283d92059e7561c60a2b402af7bd5af074b8"
verdict: "LOCAL_REMEDIATION_VERIFIED__FULL_GOVERNANCE_CLOSURE_WITHHELD"
model_touch_authority: "WITHHELD_UNTIL_G0_G1_CLOSE"
document_role: "RELEASE_SCOPED_INDEPENDENT_CHECK_FEEDBACK"
---

# 工程目录重整整改：独立复核反馈

## 1. 给工程团队的结论

本轮整改的主体是有效的：目录边界、当前真相、study registry、历史资产绑定、W1 snapshot
provenance、study 最低工程骨架与 common ownership 均已从“建议”变为实际提交。**不需要回滚目录架构，
也不需要把 study 并回伞仓。**

但本次独立复核不能签发“治理面完全关闭”，当前正式判定为：

`LOCAL_REMEDIATION_VERIFIED__FULL_GOVERNANCE_CLOSURE_WITHHELD`

原因不是整改内容整体失效，而是两个宣称为 fail-closed 的门仍可被结构合法但事实虚假的收据穿透，
并且伞仓与 study 的整改提交尚未推送到远端。D1–D4 的无模型 E0 工作可以继续；首次模型触达、
`R0 engineering foundation ready` 签发以及正式实验记录生成继续 withheld。

本反馈只审查工程治理与可复现性，不裁决创新性、方法学或实验有效性。

## 2. 已独立确认完成的部分

| 交易 | 判定 | 独立证据 |
|---|---|---|
| T0 truth alignment | PASS | HOT、Project Thesis、Experiment Assets、registry v2、owner amendment 与当前目录一致 |
| T1 legacy data repair | DATA PASS | 574/574 条当前 resolution 可从离线 bundle 还原并验证五元绑定；0 unresolved、0 waiver |
| T2 minimum study baseline | LOCAL PASS | 42 项 study 测试通过；lockfile、CI、真实 config、LICENSE/NOTICE 和构建产物存在 |
| T3 shared-code ruling | PASS | 当前无 `speechrl_common` 消费，因此不声明依赖；首次消费时精确 pin 的政策已落盘 |
| T4 snapshot correction | PASS | 13/13 文件、来源 commit、SHA-256、quarantine 状态一致；wheel/sdist 均不包含 snapshot |
| T5 common ownership | PASS WITH DEFERRED SHRINK | module-level ownership 已登记；`LEGACY_W_ERA` 物理收缩按提案延至 R0 后 |

独立执行结果：

```text
umbrella gates:
  code graph                                      PASS (21 trusted nodes)
  study workspace --require-installed             PASS
  legacy asset resolution                         PASS (574 cold-backup resolved)
  AI context surface                              PASS
  AI context manifest                             PASS

tests:
  scripts/checks                                  136 passed, 2 skipped, 190 subtests passed
  common/tests                                    21 passed, 1 skipped
  study tests                                     42 passed

artifacts:
  study sdist + wheel                             built successfully
  W1 snapshot entries in sdist/wheel              0 / 0
  four offline bundles                            SHA-256 PASS; git bundle verify PASS
  four cold-backup remote tips                    match frozen final commits
  574-entry bundle-backed five-tuple audit        PASS (one expected non-final historical commit)
```

两个 Git worktree 在复核结束时均为 clean。

## 3. 必须关闭的治理缺陷

### G0 — BLOCKER：模型触达门接受不存在的模型文件

位置：study
`src/audio_aware_evidence_acquisition/contracts.py::FrozenCoreGate.assert_model_touch_allowed`。

当前 gate 只验证：

- `llama_cpp_build_commit` 看起来像 7–40 位十六进制字符串；
- `gguf_files` 非空；
- 每项包含非空 path 和 64 位十六进制 SHA-256 字符串。

它不验证文件存在、文件位于受控资产根、实际字节 SHA-256/size 与收据一致，也不把收据绑定到
`docs/datasets.lock.json` 中冻结的模型键。独立反例使用
`/definitely/does/not/exist/model.gguf` 和伪造的 64 位摘要，当前 gate 仍返回允许。

这意味着“缺少收据时拒绝”已经实现，但“收据不能伪造”尚未实现；因此不得据此打开首次模型触达。

#### 要求的修复

1. 为 E0 closure receipt 与 runtime receipt 建立显式 schema/version/study identity。
2. runtime receipt 必须绑定模型 lock key、受控资产根下的 canonical relative path、bytes 和 SHA-256。
3. gate 从 `SPEECHRL_DATA_DIR`/canonical lock 解析文件，拒绝绝对路径、`..`、路径逃逸、重复项和额外模型文件。
4. gate 重新读取文件并计算 size/SHA-256；不得只检查字符串格式。
5. llama.cpp build commit 必须由可验证 runtime/build receipt 提供，而不是任意十六进制字符串。
6. E0 receipt 的 D1–D4 不应只有四个 `CLOSED` 字符串；每项至少绑定对应 artifact/receipt hash。
7. 新增反例测试：不存在文件、错 hash、错 size、路径逃逸、重复文件、错 lock key、伪造 build commit、
   D1–D4 artifact hash 漂移。

#### G0 验收

```text
不存在的模型路径                       必须拒绝
模型字节或 size 漂移                    必须拒绝
receipt 与 datasets.lock 模型键不一致   必须拒绝
合法 E0 + runtime + 两个冻结模型文件    才能允许
```

### G1 — MAJOR：legacy 默认 validator 不证明 commit/path/blob/URI 的语义绑定

位置：umbrella `scripts/checks/legacy_asset_resolution_check.py`。

当前 574 条数据本身经独立 bundle 复验全部正确；问题在持续门禁。默认 validator 只检查 commit/blob
的格式和 URI 中是否出现 commit，不检查：

- `path == registered legacy prefix + repo_path`；
- URI remote 是否等于对应 retired repository 的 registered remote；
- URI path 是否等于 `repo_path`；
- `git_blob` 是否真的等于该 retired repo 的 `commit:repo_path`。

独立 fault injection 在临时副本中同时把首条记录的 `git_blob` 改为 40 个零、remote 改为
`example.invalid`、URI path 改为错误路径，现行 `load_and_validate_resolution` 仍然 PASS。

#### 要求的修复

1. 默认结构门增加上述 path/remote/URI 三个 exact-equality 断言。
2. 增加离线 `--verify-bundles` 模式，从 registry 的 bundle path 重新校验 bundle SHA-256，并证明
   每项 `commit:repo_path -> git_blob`。
3. primary-dev-machine 的标准 gate 必须启用 `--verify-bundles`；CI 可使用受信缓存的 bundle/mirror，
   不得依赖网络 branch tip 作为历史 blob authority。
4. 为 `git_blob`、URI remote、URI path、commit 不可达、bundle hash 漂移分别加入负向测试。
5. `study_workspace_check.py` 可继续消费 resolution summary，但完整 acceptance 必须同时运行语义 validator。

#### G1 验收

```text
python scripts/checks/legacy_asset_resolution_check.py --verify-bundles

expected:
  574 bindings verified
  0 unresolved
  0 waived
  4 bundle hashes verified
  any one-field tamper => nonzero exit
```

### G2 — RELEASE BLOCKER：本地提交尚未进入远端

复核时状态：

```text
umbrella local  75406d4d74b63192cbcbf4177b91b4f1d06557c7
umbrella remote 772e6ed15ac0006ddd34e0600b6f994230692eb8
                 local ahead by 5 commits

study local     ac75a61104a994d77a259b9aa0f8a5e8f51dee66
study remote    53d9283d92059e7561c60a2b402af7bd5af074b8
                 local ahead by 3 commits
```

因此目前只能证明本机 checkout 可复现，不能证明团队从 GitHub clean clone 可重建；study CI 也尚未在
GitHub 实际执行。推送属于受保护操作，必须在 owner 明确授权后进行。

#### G2 验收

1. G0/G1 修复及测试先分别提交到所属仓。
2. 获得明确 push 授权后推送伞仓与 study。
3. `git ls-remote` 的 branch tip 必须等于本地审定 commit。
4. study GitHub CI 的 test 与 clean-clone-reproduction jobs 全绿。
5. 在新的 release-scoped check 目录登记最终两个远端 commit 与 CI run URL/ID。

## 4. 非阻断但应在最终关闭事务中清理的事项

### G3.1 整改提案状态未收束

`docs/superpowers/specs/2026-08-03-post-reorganization-architecture-review-and-remediation-proposal.md`
仍写 `PROPOSED_FOR_TEAM_REVIEW` 与 `CONDITIONAL_ACCEPT_WITH_REMEDIATION`，而团队收据已经写明接受并实施。

建议在 spec 顶部标为 `IMPLEMENTED_WITH_RESIDUAL_GATES` 并指向本反馈；G0–G2 全部关闭后再标为
`IMPLEMENTED_AND_CLOSED`。不要把原始设计正文删掉。

### G3.2 旧 Stage-2A handoff 仍像现行入口

`docs/superpowers/specs/2026-08-02-fable5-verdict-and-stage2a-handoff-package.md` 仍写 study 未创建，
并保留 `uv pip install -e ../../common -e .`。该文件应加醒目的
`IMPLEMENTED_AND_SUPERSEDED_2026-08-03` banner，路由到当前 owner contract、Stage-2A entry contract、
study README 和本反馈；历史正文保留不改。

### G3.3 不回写旧 check report

既有
`docs/checks/program-architecture/2026-08-03-post-reorg-remediation/report.md`
末尾写“outputs below”，但没有附最终输出表。该报告已经被提交并引用，应按 check-report immutable
纪律保留原字节。不要原地修补；在 G0–G2 关闭后创建新的 final-closure release 目录，并在那里给出
完整最终输出。

### G3.4 packaging 维护

setuptools 已提示 `project.license = { file = "LICENSE" }` 将于 2027-02-18 后不再支持。按当前
PyPA metadata 改为 SPDX expression/license-files 即可；不阻断 E0。

## 5. 建议实施顺序

| 顺序 | 所属仓 | 动作 | 完成后允许什么 |
|---|---|---|---|
| F1 | study | 修复 G0，补收据 schema、真实文件/lock/build 绑定和负向测试 | 仅具备申请模型触达复核的条件 |
| F2 | umbrella | 修复 G1，增加 exact binding 与 bundle-backed validator/fault tests | 历史资产持续治理闭环 |
| F3 | umbrella | 处理 G3 文档状态；生成新 manifest/检查结果 | 当前入口无歧义 |
| F4 | both | 全量本地验收，分别提交 | 形成待发布 commit |
| F5 | both | 获得明确授权后推送、等待远端 CI | 团队级 clean-clone 可复现 |
| F6 | umbrella | 新建 final-closure check report，owner/team 签发 | `R0 engineering foundation ready` |

F1 与 F2 可以并行；F3 不应改写旧 check report。不得为了尽快关闭而把 G0/G1 降级为人工检查。

## 6. 最终复验清单

### Umbrella

```text
python scripts/checks/code_graph_check.py
python scripts/checks/study_workspace_check.py --require-installed
python scripts/checks/legacy_asset_resolution_check.py --verify-bundles
python scripts/checks/ai_context_surface_check.py
python scripts/checks/build_ai_context_manifest.py --check
python -m pytest scripts/checks -q
pytest common/tests -q
```

### Study

```text
uv sync --frozen
python -m build
pytest -q
```

额外要求：

- 至少保存一次 G0 的伪造 receipt 被拒绝的测试输出；
- 至少保存一次 G1 的 blob/URI/path fault injection 被拒绝的测试输出；
- wheel/sdist 中 W1 snapshot entries 仍为 0；
- 两个 worktree clean；
- 本地 HEAD、远端 branch tip 与 final closure report 三者一致；
- owner contract、Research Objective、Experiment Assets 与 study experiment index 仍保持
  Stage-2A E0、D1–D4 pending/closing 的真实状态，不提前写实验结果或方法结论。

## 7. 当前执行裁决

```text
continue_model_free_E0_D1_D4: ALLOWED
create_or_claim_formal_experiment_result: WITHHELD
first_model_touch: WITHHELD_UNTIL_G0_G1_CLOSE_AND_RUNTIME_RECEIPTS_REVIEWED
R0_engineering_foundation_ready_signoff: WITHHELD_UNTIL_G0_G1_G2_CLOSE
innovation_or_methodology_verdict: OUT_OF_SCOPE_AT_THIS_STAGE
directory_architecture_rollback: NOT_RECOMMENDED
```

请工程团队针对 G0、G1、G2 返回逐项 closure evidence；下一轮只复核这些 residual gates 与由其触发的
必要文档更新，不重新开启目录架构讨论，也不扩大到新的论文扫描或方法设计。
