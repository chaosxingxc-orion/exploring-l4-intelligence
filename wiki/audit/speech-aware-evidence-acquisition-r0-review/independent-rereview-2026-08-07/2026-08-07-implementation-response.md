---
title: "Implementation response to the 2026-08-07 script-engineering rereview"
date: "2026-08-07"
artifact_type: "IMPLEMENTATION_TEAM_RESPONSE"
campaign: "speech-aware-evidence-acquisition-r0-review"
round: "independent-rereview-2026-08-07"
responds_to: "2026-08-07-saea-r0-script-engineering-review-assessment.md"
verdict_disposition: "ACCEPTED IN FULL"
owner_authority_claimed: false
model_touch_performed: false
---

# 实施方回应：R0 脚本工程独立复评

## 1. 处置：全盘接受

verdict `R0_OVERALL_INCOMPLETE__R0_2_REPAIR_REQUIRED_FOR_BROKEN_OPERATOR_PATH__R1_MODEL_FACING_EXECUTION_WITHHELD`
被全盘接受。三条阻塞项与两条非阻塞项均由本方**独立复现确认**（不采信、先验证）：

| 发现 | 本方复现结果 |
|---|---|
| B1 官方 CLI 入口不可执行 | 确认。`python -m ...core.driver --help` → "is a package and cannot be directly executed"；`__main__.py` 不存在；`pyproject.toml` 无 console script。连带 `scripts/evaluate.sh --outputs` 也在 dispatch 处即死，**根本到不了 scorer** |
| B2 runbook 与 CLI 不自洽 | 确认。runbook 中 `attempt_id`、`session-receipt`、`tracking-uri` 出现次数**均为 0**，而三者都是代码要求的 |
| B3 R0 整体未完成 | 确认。R0.1 仍为 `(fill)` 模板、innovation ledger 为空、R0.3 未授权未执行 |
| N1 lint 未全绿 | 确认。`ruff check src` 报 F841（`contracts/ledger.py:135`），而 `docs/engineering.md` 当时写着 "src clean" |
| N2 状态叙事漂移 | 确认。HOT 页 `last_refresh` 停在 2026-08-05 且仍称 repair 在分支上 |

## 2. 根因：同一条根因在同一天复发两次

第一次复发即 B1 本身。2026-08-05 的修复战役已把根因写入 spec：**测试写自实现，不写自合同**。
712 个测试直接 `import` 并调用 `driver_main([...])`，CI 的入口测试只跑 `--help`/无参分支（在 bash 内
提前退出，从未 dispatch 到 Python），于是"文档里写的那条命令"从未被任何测试执行过。库很强，
打包后的官方命令不可用。

**第二次复发发生在修复 B1 的过程中。** 新增的 subprocess 测试用 `sys.executable` 启子进程，而子进程
**不继承** `sys.dont_write_bytecode`，于是往冻结的 `scoring/` 包写入 `.pyc`，触发本项目自己加的
`__pycache__` 拒绝闸，导致其后 16 个依赖 gate 的测试连锁失败。控制面复跑发现；实施 agent 未发现的
原因是其 shell 里预先 `export PYTHONDONTWRITEBYTECODE=1`，**恰好掩盖了该缺陷**——这是"评估环境本身
被污染"的又一实例。

记录这一点不是自责表演，而是给下一轮复核方的判据：**本项目每一波修复的缺陷引入率不为零**，
应据此判断成熟度，而非只看最终绿灯。

## 3. 已完成的整改（复评 §10 第 1–5 项）

分支 `r0-operator-path`（study），提交 `f32d60d` + `81fbf32`：

1. **可执行入口恢复**：新增 `core/driver/__main__.py`，并在 `pyproject.toml` 注册 `saea-driver`
   console script。`python -m speech_aware_evidence_acquisition.core.driver --help` 与
   `saea-driver --help` 在 Windows 与 WSL2 均 exit 0。
2. **subprocess 级测试**：新增 `tests/contract/test_cli_module_dispatch.py`，真实 spawn 验证
   module 与 console-script 两种 dispatch、`score --outputs` 确实进入 scorer、`evaluate.sh` 确实
   进入 Python。已用"移除 `__main__.py` 后 4 个测试挂 3 个、复原后全绿"证明其具备判别力。
3. **薄入口**：`saea-driver smoke` 生成含 fresh `attempt_id` 的 plan、建立并持久化 session receipt、
   执行 run、以显式 `--tracking-uri` finalize，并打印 manifest / scores / ledger / MLflow id 位置。
   它只编排既有受管步骤，**不绕过任何 gate**；`--dry-run` 仅供测试，绝不触达真实模型。
4. **runbook 同步**：补齐 `attempt_id`、`--session-receipt`、session 创建命令、`--tracking-uri`，
   以及"失败后必须换 fresh attempt_id + fresh run dir"的操作说明。
5. **lint 与 CI**：F841 已修，`ruff check src` 干净；CI contracts job 扩展为验证真实
   module/console dispatch，而非只测 bash 内的 help 分支。
6. **字节码泄漏回归**（本方在复核中发现并追加）：所有测试子进程强制 `-B`/
   `PYTHONDONTWRITEBYTECODE=1`；conftest 改为**每个测试后**清理 `scoring/__pycache__`，使套件顺序
   无关；新增"CLI dispatch 后该目录必须不存在"的回归测试。

### 验证（控制面亲自复跑，非转述）

- Windows 全量套件连跑两次：**702 passed / 26 skipped，零失败**，两次跑完
  `scoring/__pycache__` 均不存在；
- WSL2 全量：**720 passed / 8 skipped**；
- `ruff check src` 干净；WARM gate dry-run 仍 `GATE OPEN`、exit 0。

## 4. 未做与不能做的部分（§10 第 6–8 项）

- **R0.1 readiness**：仍为空模板。填写需要对四条 prior 线做逐轴可运行性核查（model-free），
  但**R1 基线由 owner 拍板**，实施方不得自选。等待 owner 指令。
- **R0.3 SAEA-E-001**：owner 授权未给出，**未执行、无模型触达、exposure ledger 无新行**。
  runbook 现已可复制执行，但执行仍需授权。
- **HOT current truth**：已按 N2 更正——`last_refresh` 改为 2026-08-07，端点 token 改为
  `…STAGE2A_R0_INCOMPLETE__R1_WITHHELD`，正文写明 repair 已并入 master、R0 overall 为 INCOMPLETE、
  R0.1 空模板、R0.3 未授权。

## 5. 对复评两项判断的明确附议

- **"不要在首次真实 smoke 前继续增加防御性模块与抽象层"**：接受。本方在完成 R0.3 之前不再扩展
  基础设施。
- **"fixed-retrieval 命名要克制"**：接受并记录——当前 arm 是"固定 query + 预取 context 的输入形状"，
  不是检索器；未来任何检索质量主张必须另有真实检索过程与 recall/precision 证据。

## 6. 尚未提交的部分

`r0-operator-path` 分支尚未合入 master、未推送。是否合入与推送由 owner 决定。
