---
title: "Speech-aware evidence acquisition R0 independent review assessment"
date: "2026-08-05"
artifact_type: "INDEPENDENT_AI_DOCTORAL_SUPERVISOR_AND_SENIOR_ENGINEER_ADVISORY_REVIEW"
campaign: "speech-aware-evidence-acquisition-r0-review"
round: "independent-review-2026-08-05"
umbrella_commit_reviewed: "047cf39dcbb7b8cde56757d69eb63a98c9f86de0"
study_commit_reviewed: "b0635aa9736d2cbf3a581fc9295110172672c833"
reviewer_context: "Codex primary agent; four-round adversarial analysis; no delegated subagents; model-free inspection and verification only"
verdict: "R0_REPAIR__R1_MODEL_FACING_EXECUTION_WITHHELD_PENDING_P0_CLOSURE_AND_R0_SMOKE"
human_signature_claimed: false
owner_authority_claimed: false
model_touch_performed: false
repository_modified_by_reviewer: true
modification_scope: "this review report and its campaign index only"
---

# Speech-aware evidence acquisition：R0 独立评审 assessment

## 0. 结论先行

本次复核不接受“R0 已有效完成”“R0 承诺功能全部落地”或“五轮对抗归零”这三个强表述。

能够由现有证据支持的最强表述是：

> **R0.2 的 model-free 工程骨架已经基本搭建；在本次复核时点，D1–D4、split receipt、模型与
> llama.cpp runtime receipt 均与当前磁盘事实一致。但 R0.1 readiness 尚未收口，R0.3
> `SAEA-E-001` 真实模型 smoke 尚未执行，且 gate、split、carrier/media、attempt budget 与正式
> artifact chain 存在可复现的 fail-closed 缺口。R0 整体应判为 `REPAIR`，不能判为 `PASS`。**

本报告建议在 P0 缺口关闭并完成 R0.3 之前，暂缓正式 R1 model-facing reproduction。该建议是
AI reviewer advisory，不替代 owner 决策，也不撤销已有 owner GO；它只指出当前工程证据不足以
安全消费该授权。

精确 verdict：

`R0_REPAIR__R1_MODEL_FACING_EXECUTION_WITHHELD_PENDING_P0_CLOSURE_AND_R0_SMOKE`

## 1. 审查对象、边界与不作出的主张

### 1.1 审查对象

本次审查绑定以下版本：

- umbrella：`047cf39dcbb7b8cde56757d69eb63a98c9f86de0`；
- study：`b0635aa9736d2cbf3a581fc9295110172672c833`；
- study branch：`master`，审查开始与结束时均与 `origin/master` 对齐；
- 两个 worktree 在审查开始和结束时均为 clean。

承诺来源按效力与细化关系读取：

1. `wiki/experiments/speech-aware-evidence-acquisition/2026-08-04-owner-consolidated-execution-contract.md`；
2. `docs/superpowers/specs/2026-08-02-speech-aware-evidence-acquisition-stage2a-entry.md`；
3. `docs/superpowers/specs/2026-08-05-speech-aware-evidence-acquisition-stage2-discovery-slice1-design.md`；
4. `docs/superpowers/plans/2026-08-05-speech-aware-evidence-acquisition-r0-vertical-slice.md`；
5. study `docs/engineering.md`、R0 smoke runbook、代码、配置、测试和 receipts；
6. umbrella HOT/current 状态与 study experiment index。

### 1.2 审查边界

本次只做 model-free 审查。没有启动或调用 Qwen3-Omni，没有执行 `SAEA-E-001`，没有读取任何
confirmatory 结果，没有新增 exposure row，没有运行 R1/X probe，也没有修改 study 代码、配置、
receipt、数据或 Wiki current truth。

本次评审不判断研究方法是否有效、是否优于 prior、是否创新，也不产生 paper candidate。R0 的合同
目标本来就只是 wiring 与 measurement integrity；优越性和创新性不能由 R0 推出。

## 2. 评审标尺：R0 不是一个单点

2026-08-05 discovery-slice design 已把 R0 分成三个不同出口：

- **R0.1：** model-free readiness memo 与 innovation ledger 脚手架；出口是 owner 拍板 R1；
- **R0.2：** model-free 工程基线；出口是全测试通过、双仓 gate 通过；
- **R0.3：** 首次真实模型 smoke `SAEA-E-001`；出口是 trace 完整、预算吻合、hash 齐全。

因此，“R0.2 engineering baseline delivered”和“R0 complete”不是同一句话。当前 HOT 页已使用较
窄的“R0 engineering baseline delivered；smoke/R1 next”措辞，但同页又写“五轮对抗 review zero
defects”。前半句可保留；后半句被本次可复现 findings 推翻。

本报告使用四级判定：

- `PASS`：承诺有实际执行证据，且未发现反例；
- `PARTIAL`：主要结构存在，但正式配置、产物或端到端证据缺失；
- `NOT_RUN`：只有 runbook 或假实现，没有真实执行；
- `REPAIR`：存在会破坏研究边界、测量完整性或预算记账的可复现缺口。

## 3. 四轮对抗式审查方法

### Round 1：承诺—证据映射

逐项把 owner contract、Stage-2A entry contract、R0.1/R0.2/R0.3 design 和实现计划映射到当前
代码、配置、receipt、测试、runbook 与 experiment ledger。目标是区分：

- 文件或接口“存在”；
- 合成测试“能跑”；
- 正式配置“可实例化”；
- 真实运行“已证明”；
- 研究完整性“机器不可绕过”。

### Round 2：正向验证

运行全测试、构建、umbrella gates、真实 receipt dry-run，并从当前数据重新生成 D1–D4 以及三类
split 的内存表示，与 committed artifacts 比较。目标是确认当前工作树和磁盘事实是否真的健康。

### Round 3：恶意但类型合法的反例攻击

使用临时目录和 synthetic gate world，不修改仓库，构造以下攻击：

1. exposure 行写 Earnings21，但 plan 使用 `fsd50k`；
2. split IDs 被替换，receipt 仍保留旧 identity hash；
3. media path 使用数据根目录之外的绝对路径；
4. 同一 exposure 行与同一 plan 重复开 gate；
5. Earnings21 plan 下提交 `fsd50k` payload。

每个攻击都要求代码实际接受，而不是只做静态猜测。

### Round 4：反驳性复核

对每个 finding 重新回答两个问题：

1. 它证明当前数据已经污染了吗？
2. 它是否只是明确允许的 R1/X 延期，而不是 R0 缺口？

结论是：当前 D1–D4 和 split **没有污染**；X1/X3/X4 policy、oracle 的具体 upper-bound 算法和
论文级统计明确属于后续阶段，不应错算为 R0 defect。保留下来的 P0/P1 findings 都直接作用于
R0 已承诺的 gate、wiring、measurement integrity、预算或正式产物链。

## 4. 正向证据：已经完成且值得保留的部分

### 4.1 测试、构建与 workspace gates

- WSL2 `Ubuntu-24.04`、Python 3.12、`~/.venvs/speechrl`：`234 passed in 4.15s`；
- Python sdist 和 wheel 构建成功；
- umbrella `code_graph_check.py`：PASS，24 trusted nodes；
- `study_workspace_check.py`：PASS；
- `paper_workspace_check.py`：PASS，paper zero state；
- `ai_context_surface_check.py`：PASS；
- `build_ai_context_manifest.py --check`：PASS；
- secret pattern scan未发现明显 API key 或 `sk-...` 泄漏。

测试数量和 contract surface 都明显超过目录骨架阶段。Registry、loader、D2 field allowlist、
ExecutionPlan、receipt rehash、runtime library exact-set、trace namespace、config collision、scoring
freeze、snapshot quarantine 和 model-free entrypoint 都有直接测试。

### 4.2 真实 receipt dry-run

在真实 `SPEECHRL_DATA_DIR` 和 `/home/chao` runtime root 上执行：

```bash
cd /mnt/d/chao_workspace/exploring-l4-intelligence/studies/speech-aware-evidence-acquisition
source ~/.venvs/speechrl/bin/activate
export SPEECHRL_DATA_DIR=/mnt/e/chao_workspace/exploring-l4-intelligence/speechrl-data
export LLAMA_RUNTIME_ROOT=/home/chao
bash scripts/reproduce.sh
```

结果：gate dry-run PASS，约 161.2 秒。模型 GGUF、mmproj、`llama-server`、`build/bin` runtime files、
E0 closure 和 scoring freeze 在该时点均与 receipt/lock 匹配。没有加载模型；该 dry-run 不授权后续
调用。

### 4.3 D1–D4 与 split 的独立实时重算

忽略 artifacts 中仅反映生成日期的 `generated` 字段后：

| Artifact | 独立重算结果 |
|---|---|
| `d1-identity.json` | MATCH |
| `d2-leakage.json` | MATCH |
| `d3-scoring.json` | MATCH |
| `d4-trace.json` | MATCH |
| discovery split | MATCH，44 samples |
| dev split | MATCH，10 samples |
| confirmatory split | MATCH，115 samples |

这组证据非常重要：findings 指向的是**未来执行时的持续保证不足**，而不是当前 receipt 已经虚假。

### 4.4 可保留的核心架构

以下设计不需要推倒重来：

- 单一 `core/` foundation package；
- 一个通用 `Registry`、五个 seam；
- 一个共享 `run_experiment()` driver；
- D2 三种 arm 的 exact field set；
- `FrozenCoreAdapter` 作为模型请求 choke point；
- discovery/dev/confirmatory 的显式角色；
- scoring-side reference 隔离；
- raw trace 拒绝写入 Git worktree；
- model-free receipt verification；
- R1/X 通过新增 config 或注册组件扩展，而不是复制 runner。

评审建议是 harden 现有骨架，而不是另起一套框架。

## 5. 承诺—实现—证据矩阵

| R0 承诺 | 当前实现 | 证据强度 | 判定 |
|---|---|---|---|
| 单一 core/、统一 registry、统一 driver | 已实现并被合成端到端测试覆盖 | 高 | `PASS` |
| deterministic Earnings loader | E21/E22 loader 已实现；当前实时数据一致 | 高 | `PASS` |
| discovery/dev/confirmatory split freeze | receipt 与当前数据一致；运行时不重算且可篡改 | 中 | `REPAIR` |
| gate-bound frozen-core adapter | receipt/预算/allowlist 有实现；plan/config/payload/server 未全绑定 | 中 | `REPAIR` |
| OBS/ORG/SUPPLY/USE trace | fake transport 路径已验证；真实 trace 未生成 | 中 | `PARTIAL` |
| bare core | 正式 JSON 配置存在 | 高 | `PASS`（model-free wiring） |
| fixed legal context | 代码与合成 driver test 存在；无正式 config/run | 中低 | `PARTIAL` |
| fixed retrieval/context | payload builder unit test；无正式 config/driver smoke | 低 | `PARTIAL` |
| random/mismatched evidence | deterministic rotated mismatch 实现并测试；无正式 config | 中 | `PARTIAL` |
| oracle upper-bound interface | runtime 明确拒绝，符合“不得进正式 runtime”；具体计算后置 | 中 | `PASS`（仅接口承诺） |
| scorer adapters | frozen WER/entity/QA/transitions 底层存在；registry 只有 ASR WER | 中 | `PARTIAL` |
| MLflow + umbrella ledger linkage | helper 与 renderer 存在；没有可执行的端到端 transaction | 低 | `PARTIAL` |
| calls/tokens/latency/audio/evidence/GPU/CPU accounting | calls/audio/latency/tokens 部分完成；其余未闭环 | 中低 | `PARTIAL` |
| R0.1 readiness exit | memo 仍为 TEMPLATE，owner 未拍板 R1 | 无完成证据 | `NOT_RUN` |
| R0.3 SAEA-E-001 | runbook 存在，experiment ledger 为空 | 无执行证据 | `NOT_RUN` |

## 6. P0 findings：进入 R1 前必须关闭

### P0-1：split receipt 是自述事实，运行时不验证其真实性

**位置：** study `core/driver.py::load_split()`。

当前函数读取 `docs/receipts/splits.json` 后：

- 不检查 `saea-splits-v1` schema；
- 不检查 split exact keys；
- 不检查 count 与 IDs 数量一致；
- 不检查 carrier-prefixed ID 的 prefix；
- 通过 `split('/', 1)[1]` 丢弃 prefix；
- 不从 IDs 重算 `identity_hash`；
- 不检查 receipt `carrier_lock_key`；
- 不从当前 loader/asset identity 重算 split。

driver 随后只比较 `plan.split_identity_hash == receipt.identity_hash`。因此 receipt 的 IDs 和 hash 可
同时失去关系，而 plan/driver 仍认为它们一致。

**可复现反例：**临时 receipt 中把 dev IDs 改为
`earnings22-original/CONFIRMATORY-LIKE-ID`，保留旧的 `aaaa...` hash 和 `split_role=dev`；
`load_split()` 返回新 ID、旧 hash、dev role，没有拒绝。

**研究风险：** confirmatory ID 可以被重标为 dev；ledger 与 protocol 仍携带旧 hash；“未读
confirmatory”声明可能在没有显式异常的情况下失真。

**必需修复：** model-touch 前对 receipt 做 exact-schema 校验、重算 IDs hash、验证 prefix/count/
carrier/role，并从当前合法 loader 重算可允许的 split membership。split receipt 本身还必须被一个
不能与它同时自我改写的 commit/blob 或 release manifest 绑定。

### P0-2：carrier、payload 与 media path 没有形成一条值级绑定链

**位置：** `contracts.FrozenCoreGate`、`core.model.FrozenCoreAdapter`、
`core.model.LlamaServerTransport`。

当前 gate 对 exposure 行只绑定：profile、split role、split identity hash、`consumed=no` 和三个预算
数值。它不解析或核对 exposure 行的 `speech carrier + split`。随后对 plan carrier 只检查“名称存在于
umbrella lock”，而不是“属于该 study 的 speech-only allowlist”。

adapter 对 payload 只检查字段名 exact-set、decoding key allowlist、information-boundary key 与预算；
不检查：

- `payload.carrier_lock_key == plan.carrier_lock_key`；
- `speech_ref` 与 carrier/sample 一致；
- sample 属于 plan split；
- `media_relpath` 属于该 carrier lock 的 `local_subdir`；
- task instruction 与 frozen config 一致。

transport 直接计算 `self._data_root / payload["media_relpath"]`。Python `Path` 在右侧为绝对路径时会
丢弃左侧 root，所以绝对 media path 可读取 `SPEECHRL_DATA_DIR` 之外的任意现有文件。

**已复现：**

1. exposure 行声明 Earnings21，gate 接受 `plan.carrier_lock_key=fsd50k`；
2. Earnings21 plan 下 adapter 接受 `carrier_lock_key=fsd50k` 的 payload；
3. transport 读取并发送了 data root 外的绝对 `.mp3` 文件。

**研究风险：** speech-only/general-audio exclusion、carrier attribution、processed speech seconds 与
dataset revision 都可失真；还存在本地文件越界读取风险。

**必需修复：** gate 使用 study-specific carrier allowlist；exposure 行必须绑定 carrier；adapter 必须
逐值绑定 plan/config/split/sample/payload；所有路径用 `resolve(strict=True)` 后验证
`is_relative_to(carrier_root)`，拒绝绝对路径、drive prefix、反斜杠、`..`、symlink escape 与 prefix
不匹配。

### P0-3：receipt-pinned 磁盘 runtime 不等于实际响应 server

**位置：** `FrozenCoreGate.assert_model_touch_allowed()`、`FrozenCoreAdapter.__init__()`、
`LlamaServerTransport` 和 model config。

gate 正确重哈希了磁盘上的 model/runtime files，但 driver 不启动该二进制，也不证明当前 HTTP
endpoint 由它提供。现有流程是：

1. 重哈希 `/home/chao/llama.cpp/build/bin` 和 GGUF；
2. 构造一个指向 config `base_url` 的 HTTP client；
3. 向 `/v1/chat/completions` 发请求。

中间没有 PID、executable inode/hash、command line、listening socket、loaded GGUF、server startup
receipt 或 endpoint locality 的绑定。config `base_url` 也没有 localhost allowlist。

**研究风险：** gate 可以在本地 receipt 全真时，把请求发给另一个本地进程、远程服务、另一模型或
错误模型配置；正式记录却仍会继承 receipt-pinned Qwen3-Omni 身份。

**必需修复：**首选由同一 driver 在 gate 后立即启动 receipt-pinned binary，并记录 PID、binary
hash、argv、model/mmproj canonical paths、port、startup output 与 shutdown state。若必须使用 resident
server，则需要受控 supervisor 提供可验证 session receipt，且 endpoint 必须限制为本机受管 socket。

### P0-4：同一 exposure reservation 可重复消费

**位置：** `FrozenCoreGate._require_exposure_preregistration()` 与 adapter per-process counters。

exposure ledger 的 discovery/dev 行按合同保持 `consumed=no`；gate 没有一次性 nonce、attempt id、
open/actualized 状态或原子消费操作。同一 plan 和同一行可多次通过 gate。每个新 adapter 又把 calls 和
audio counters 重置为零。

**已复现：**同一真实 synthetic gate、同一 plan、同一 exposure row 连续两次打开成功。

**研究风险：**一个登记为 12 calls 的 plan 可在多个进程或 fresh attempt 目录重复执行，每次获得
新的 12-call 预算。ledger slice total 不变，真实 exposure 和 GPU/audio 使用量持续增长。失败
transport 的 attempt 虽在内存计数，但 run abort 后没有强制 actualization。

**必需修复：** exposure 以 `(run_id, attempt_id)` 为不可复用主键；gate open 必须产生一次性 nonce
或原子 `RESERVED -> OPENED` 转移；每次 transport attempt 在发送前持久化 actual usage，失败也不能
丢；fresh attempt 必须有新登记，slice total 由 reservations 与 actuals 的保守上界共同约束。

## 7. P1 findings：R0.3 前应关闭

### P1-1：正式 outputs、trace、score 与 ledger 之间没有完整哈希闭包

driver outputs row 包含 request/response hash，但 scorer 只读取 `carrier_lock_key`、`sample_id` 和
`text`；它不验证：

- response hash 是否对应 text；
- request id 是否存在于 trace；
- outputs sample set 是否等于 frozen split；
- 是否有重复 sample；
- run/config/protocol/model/dataset identity；
- trace manifest 是否对应 raw trace；
- outputs 文件自身的 hash。

因此修改 outputs text、保留旧 response hash，仍会被正常计分。

`TraceSink` 生成 raw `trace.jsonl` 和一个 record-hash manifest，但 `core.tracking.log_run()` 只上传
outputs 与 trace manifest，不上传 raw trace，也不上传 scoring artifact。`RunResult` 只返回
trace-manifest hash，没有 outputs hash、raw-trace hash 或 scores hash。

**必需修复：**每个 attempt 生成原子 run manifest，至少绑定：study commit、shared-code revision、
config/protocol/model/dataset/split identity、ExecutionPlan、exposure row/attempt id、outputs hash、raw
trace hash、trace manifest hash、score artifact hash、actual cost、failure state 与 MLflow artifact URI。
scorer 必须从该 manifest 进入并先完成全链校验。

### P1-2：MLflow 和 umbrella ledger linkage 只是 helper，不是可复现 transaction

runbook 第 3–4 步写“score；log to MLflow；render ledger row”，但：

- driver CLI 结束时只打印 run id 与 cost；
- `evaluate.sh` 只把 aggregate 打到 stdout，不生成 frozen score artifact；
- `log_run()` 需要仍在内存中的 `RunResult`、`ComposedConfig`、`ExecutionPlan`；
- 没有 CLI 从已结束 run 重建这些对象并完成验证；
- `ledger_row()` 只格式化调用者提供的 21 个字符串，不能从已验证 run manifest 派生事实。

这不足以证明“MLflow 与 umbrella experiment index 的 URI/hash 连接”已完成。

**必需修复：**提供单一 `finalize` 命令，验证 attempt bundle，执行 scoring，写 score artifact，上传
完整 MLflow artifacts，输出机器生成的 ledger row/JSON，并拒绝人工给出的冲突字段。

### P1-3：三条工程控制与 scorer adapter 只完成了结构面

正式 config fragment 目前只有 `configs/baseline/bare-core.json`。`fixed-legal-context` 在 synthetic
driver test 中可运行；`fixed-retrieval` 只有 payload-builder unit test。两者都没有正式 config、
ExecutionPlan/runbook 实例或 artifact schema。mismatched evidence 有 decorator，但无正式 config。

scoring package 已冻结 WER、entity、QA 与 transitions 底层函数，但统一 `SCORERS` registry 只注册
`asr-wer`。没有 entity/QA outputs adapter、evidence metric adapter 或 cost scorer。README 所称
“registered task, entity, evidence and cost metrics”强于事实。

这不要求提前实现 X1/X3/X4 policy；那些明确属于后续阶段。R0 需要补的是合同已点名的三条工程
控制的可配置实例与 scorer seam 的基本端到端消费能力。

### P1-4：效率记账只完成了 calls/audio/latency/tokens 子集

adapter `cost_summary()` 当前输出：calls、audio seconds、latency、prompt tokens、completion tokens。
缺少：

- 实际 GPU-hours；
- 实际 CPU-hours；
- 峰值显存；
- supplied/admitted evidence bytes 的 run aggregate；
- tool calls；
- gate/setup latency；
- failed attempt cost。

`planned_gpu_hours` 只在 plan/ledger 中作为登记上限，运行中没有计时或中止机制。设计计划把
GPU/CPU 直接采样延至 R1，但 owner entry contract 已把它列入 R0 accounting。若团队坚持此延期，
应由 owner 明确接受范围缩减或记录 deviation，不能由 implementation plan 单方面把合同义务解释掉。

### P1-5：CI 仍执行 pre-R0 语义，当前 workflow 会失败

`.github/workflows/ci.yml` 的 `clean-clone-reproduction` job 仍名为“Pre-R0 entrypoints must refuse”，
期望：

```bash
bash scripts/reproduce.sh; r1=$?
bash scripts/evaluate.sh; r2=$?
test "$r1" -eq 2 && test "$r2" -eq 2
```

当前 R0 `reproduce.sh` 已变成 receipt verify。在本地去掉 `SPEECHRL_DATA_DIR` 后，实际结果是：

- `reproduce.sh`：exit 1；
- `evaluate.sh` 无参数：exit 2。

因此该 job 的 final `test` 必然失败。GitHub clean job 还没有先 `uv sync`，在真正 clean runner 上可能
更早因 src-layout package 未安装而 exit 1。

**必需修复：**更新 job 为当前 R0 语义；将纯 clean-clone contract tests 与需要私有 assets/runtime
的 machine-bound gate 分开。CI 应至少加入 active-source lint；type-check/coverage 若暂不设门，应在
quality report 中明确为 `NOT_CONFIGURED`，不能写成零缺陷。

## 8. P2 findings：不阻塞 R0.3，但应在同一修复波清理

1. README layout 仍列出已经删除的 `models/`、`evidence/`、`tracing/`、`experiments/` 目录；
2. baseline README 说新 baseline 落为 YAML，但 config composer 只读取 JSON；
3. `ruff check .` 报 16 项：12 项在 quarantined W1 snapshot，4 项在 active source/tests；
4. 没有配置 pyright/mypy，当前环境也未安装 pyright；
5. 没有 pytest coverage 插件，不能给出覆盖率百分比；
6. wheel 构建成功，但没有对非 editable 安装后的 config/repo-root 行为做 smoke；构建成功不等于
   wheel 可作为独立 runtime artifact。

quarantined snapshot 不应机械格式化或改写；lint 应排除该目录并对 active tree 单独设门。

## 9. 博导视角：是否完成了既定研究目标

### 9.1 尚未完成 R0 的认识论目标

R0 不需要证明性能提升，但必须证明“测到的东西确实来自声明的模型、样本、split、arm 和 scorer”。
当前模型、split、carrier、attempt 与 artifacts 的绑定存在断点，所以 measurement integrity 还没有
成立。234 个测试说明局部实现有纪律，不等于正式实验事实可归因。

### 9.2 目前没有任何 effectiveness/reasonableness/efficiency 结果

experiment index 明确仍无正式实验；`SAEA-E-001` 未执行。因此下列问题全部尚未获得数据：

- llama.cpp 当前 build 是否接受所构造的 Qwen3-Omni audio chat payload；
- real response shape 是否与 transport parser 一致；
- 十个 dev samples 是否逐个产生完整 OBS/USE/request/response/cost trace；
- bare-core outputs 是否能被 frozen scorer 完整消费；
- MLflow 与 umbrella ledger 是否能无人工重写地闭环；
- 实际成本是否处于登记预算；
- failure/retry 路径是否保留 exposure 与 partial artifacts。

所以不能说“R0 功能有效完成”。最多能说“model-free skeleton 在合成环境中功能成立”。

### 9.3 readiness 未完成意味着 R1 选择没有审查依据

readiness memo 仍为模板，OBS、ORG/SUPPLY、USE 三段均未填，OVERALL 排名与 owner decision 为空。
这不是 R0.2 core defect，但它使 R0.1 尚未完成，也意味着正式 R1 对象尚未按合同冻结。不能因为
工程代码可运行就自行选择一个方便的 prior。

### 9.4 不应把合法延期误判为遗漏

以下工作不属于本次 P0/P1：

- X1 re-resolution policy；
- X3 verification loop；
- X4 reward-guided next-action policy；
- oracle evidence 的具体计算方法；
- confirmatory 大规模验证；
- paper-scale implementation、最终 superiority claim 和 manuscript。

它们应继续按 R1/X/2B/Stage-3 顺序推进，不能为了“补齐 R0”而提前实现。

## 10. 资深工程师视角：是否完成了研究课题工程基座

### 10.1 已完成的是 architecture skeleton

代码已经从“目录骨架”进入“可测试基础设施”：职责拆分合理，stdlib-only gate 易于审计，真实资产与
Git 分离，冻结 scoring source，config 无 override semantics，trace 轴命名空间和 fresh-directory
规则都有价值。这些是可继续建设的基础。

### 10.2 未完成的是 trust boundary 与 run transaction

一个研究工程基座的最低要求不是“正常路径能跑”，而是：

> 给定一个正式 run id，任何人都能证明它只读取了注册 split 的合法 speech samples，由 receipt-pinned
> server/model 产生，请求、响应、trace、score、成本和 ledger 是同一个不可拆分 transaction；失败和
> 重试不能抹掉 exposure 或复用预算。

当前实现尚未满足这个定义。缺口集中在边界绑定与 transaction finalization，并非业务算法复杂度。

### 10.3 “五轮对抗归零”不可保留

本次五个攻击均被实际接受，而不是理论担忧：

| Probe | 当前结果 | 应有结果 |
|---|---|---|
| exposure Earnings21、plan `fsd50k` | ACCEPT | REJECT |
| split IDs 改变、hash 保持旧值 | ACCEPT | REJECT |
| data root 外绝对 media path | READ/SEND | REJECT |
| 同一 exposure 行重复开门 | ACCEPT × 2 | 第二次 REJECT |
| Earnings21 plan、`fsd50k` payload | ACCEPT | REJECT |

因此后续 current truth 应把“zero defects”改为“内部 review waves completed；independent R0 review
returned REPAIR”，直至 fresh rereview 接受。该 current-state 修改需要 owner/team 在修复事务中按
`wiki/AI-Collaboration.md` 完成；本 advisory report 不直接改 HOT 页。

## 11. 建议的有界修复计划

### H1 — Split and carrier closure（P0）

- 新建严格 `FrozenSplitReceipt` parser；
- exact keys/schema/count/prefix/hash/carrier/role 全检；
- gate 时用 loader 重算 dev/discovery membership；
- study carrier allowlist 与 general-audio denylist 双保险；
- exposure carrier、plan carrier、config carrier、payload carrier 四向相等；
- 增加 confirmatory ID 注入、stale hash、wrong prefix、duplicate ID、mixed carrier 测试。

### H2 — Media confinement and payload binding（P0）

- `media_relpath` 只允许规范化 POSIX relative path；
- resolve 后必须位于 lock entry `local_subdir`；
- 拒绝绝对路径、drive、backslash、traversal、symlink escape；
- payload sample 必须属于 frozen split；
- `speech_ref`、sample id、carrier、audio seconds 与 loader fact 一致；
- adapter 接受由 driver 构造的不可变 typed request，不接受任意 mapping。

### H3 — Runtime session attestation（P0）

- driver/supervisor 启动 receipt-pinned server；
- bind PID、binary hash、argv、model/mmproj paths、port 与 startup receipt；
- endpoint localhost-only；
- server health response 记录 build/model identity；
- run manifest 写入 session receipt hash；
- 测试 wrong process、wrong model、remote URL、port hijack 和 stale resident server。

### H4 — One-time attempt accounting（P0）

- 引入 `attempt_id`；
- exposure row/receipt 状态机：REGISTERED → OPENED → FINALIZED/ABORTED；
- gate nonce 单次使用；
- request 发送前持久化 actual calls/audio；
- failure trace 与 partial manifest 必须落盘；
- retry 使用新 attempt registration，不共享 per-process budget；
- slice cap 对 registered reserve 与 actual usage 取保守值。

### H5 — Atomic run bundle and finalizer（P1）

- outputs、raw trace、trace manifest、scores、cost、config、plan 全部 hash；
- `finalize` CLI 执行校验、scoring、MLflow upload 和 ledger rendering；
- scorer 拒绝重复/缺失/额外 samples，验证 response hash 与 trace linkage；
- MLflow 上传 raw trace 和 score artifact；
- ledger row 只能从 verified manifest 派生；
- aborted attempt 生成可审计但不可冒充 completed 的 bundle。

### H6 — R0 config/scorer/cost completion（P1）

- 为 fixed legal context、fixed retrieval 和 mismatched evidence 增加正式 JSON fragments；
- 增加至少一个 fixed-retrieval synthetic driver test；
- 为 entity/QA 增加 outputs adapters，或明确从 R0 contract 移出并获 owner 接受；
- cost aggregate 加 evidence bytes 与 failure attempts；
- GPU/CPU/VRAM 使用要么实测，要么形成明确 deviation/owner acceptance；
- 保持 X policies 和 oracle computation 后置，不扩大修复范围。

### H7 — CI and documentation alignment（P1/P2）

- 替换 pre-R0 clean-clone job；
- CI 对 active source 做 lint，排除 immutable/quarantined snapshot；
- 新增本报告五个 regression tests；
- 增加 installed-wheel 或明确 repo-checkout-only contract test；
- 修复 README layout、JSON/YAML 漂移；
- quality report 把 coverage/type-check 明确写为 PASS/FAIL/NOT_CONFIGURED。

### H8 — R0.3 owner-visible smoke（最后一步）

P0/P1 修复、测试和 fresh review 通过后：

1. 填写并冻结合法 ExecutionPlan 与 attempt registration；
2. 执行 `SAEA-E-001` dev subset10；
3. 验证十样本完整 trace、sample set、hash、server identity 和 actual cost；
4. 运行 finalizer，生成 MLflow run 与 umbrella ledger row；
5. 写 wiring-integrity memo；
6. 若任何边界/score/hash/预算失败，判 `REPAIR`，不进入 R1；
7. 全部通过后，才签发 `R0_COMPLETE__R1_ENTRY_ELIGIBLE`，并由 owner 依据 readiness memo 选择 R1。

## 12. Fresh rereview 的最小提交包

下一轮不需要重审 Stage-1 文献或重跑 W1 legacy inventory。工程团队应提交一个有界、commit-bound
的 R0 repair package，至少包含：

1. 修复后的 exact study commit；
2. P0/P1 finding → code/test/receipt 的 closure matrix；
3. 本报告五个 probe 的 regression tests；
4. WSL2 全测试、build、active lint 输出；
5. 真实 gate dry-run 输出及耗时；
6. D1–D4/split 实时重算结果；
7. runtime-session attestation 负测试；
8. one-time attempt/budget 负测试；
9. synthetic complete run bundle + finalizer + MLflow/ledger dry-run；
10. clean worktree 与 study commit/remote binding；
11. owner 对 GPU/CPU accounting scope 和 R0.3 执行的明确处置；
12. 若申请执行 smoke，预注册 exposure row 与尚未使用的 attempt id。

fresh reviewer 的接受条件不是“所有测试通过”这一句话，而是：每个 P0 反例必须从 ACCEPT 变为
REJECT，正式 run bundle 必须能从原始 artifact bytes 独立重建其 identity 与 hash closure。

## 13. 最终判定

### 博导判定

R0 尚未完成既定目标。当前没有真实模型 wiring 证据，也没有正式 effectiveness、reasonableness、
efficiency 结果；measurement integrity 仍被 split/carrier/server/artifact chain 缺口阻断。不得把
R0.2 skeleton 当成研究结果，更不得据此宣称方法有效或创新。

### 资深工程师判定

工程骨架有保留价值，局部质量明显达标，当前 receipts 真实；但 trust boundary 和 formal run
transaction 尚未闭合。所有工程方案没有全部完成，尤其是 split authenticity、carrier/media
confinement、actual server identity、one-time attempt budget、artifact finalization、正式 control
configs、scorer adapters、成本记账和 CI。

### Advisory verdict

`R0_REPAIR__R1_MODEL_FACING_EXECUTION_WITHHELD_PENDING_P0_CLOSURE_AND_R0_SMOKE`

该 verdict 不声称 owner authority。owner 可以选择接受、修改或驳回；在没有新的 owner 处置前，本
报告只建议工程团队按 H1–H8 做有界修复，并在 fresh independent rereview 通过后执行 R0.3。
