---
title: "Implementation response to the R0 independent review"
date: "2026-08-05"
artifact_type: "IMPLEMENTATION_TEAM_RESPONSE"
campaign: "speech-aware-evidence-acquisition-r0-review"
round: "independent-review-2026-08-05"
responds_to: "2026-08-05-saea-r0-independent-review-assessment.md"
verdict_received: "R0_REPAIR__R1_MODEL_FACING_EXECUTION_WITHHELD_PENDING_P0_CLOSURE_AND_R0_SMOKE"
verdict_disposition: "ACCEPTED IN FULL"
owner_authority_claimed: false
model_touch_performed: false
---

# 实施方回应：R0 独立评审

## 1. 处置：全盘接受

评审 verdict 被**全盘接受**。本方没有对任何 P0/P1 发现提出异议；相反，全部发现经本方独立复核后
**逐条确认属实**，其中数条的证据比评审所述更强。

复核方法（不采信、只验证）：控制面逐条读码 + 两个独立验证 agent 用真实
`FrozenCoreGate` / `FrozenCoreAdapter` / `LlamaServerTransport` 在临时目录中跑通探针。

| 评审发现 | 本方复核结论 | 补强证据 |
|---|---|---|
| P0-1 split 收据自证、运行时不验证 | 确认 | 篡改 dev ids 保留旧 hash，`load_split` 静默返回 |
| P0-2 carrier/payload/media 未值级绑定 | 确认 | `fsd50k` **本就在真实 umbrella lock 的 asset_catalog 中**，无需篡改即过门；绝对 media 路径读到 data root 外文件并 base64 送出 |
| P0-3 receipt-pinned 磁盘 runtime ≠ 实际响应 server | 确认 | 无 PID/argv/socket 任何绑定，endpoint 无 localhost 限制 |
| P0-4 同一 exposure 额度可重复消费 | 确认 | 同一 plan + 同一行连开两次成功；两个 adapter 各自从零计数；`src/` 中无任何代码写回 `consumed=yes` |
| P1-1 产物链无哈希闭包 | 确认 | 改 outputs.text 保留旧 `response_sha256` 仍正常计分 |
| P1-5 CI 仍执行 pre-R0 语义 | 确认 | 实测 `reproduce.sh` exit 1 / `evaluate.sh` exit 2 → job 必挂；且该 job 从不安装包 |
| P2 文档漂移 | 确认 | README 仍列已删除包；baseline README 承诺 YAML 而 composer 只读 JSON |

**"五轮对抗归零"结论作废。** 正确表述为："内部 review waves 完成；独立 R0 评审返回 REPAIR。"

## 2. 根因（本方分析，非评审要求）

1. **威胁模型同源**：五轮 reviewer 的治理不变量清单由实施方从 diff 推导，只覆盖文件治理
   （冻结面、禁用数据集、无模型触达、无提交字节），未覆盖运行期信任边界。审查者在被审查者的
   世界观内攻击，故全部 held。
2. **验证锚点错位**：任务级评审对照"计划中的 authoritative code block"，计划本身缺检查时全链
   无人能发现。独立评审从**合同**做承诺-证据矩阵，才看见"承诺 measurement integrity、交付
   wiring"。
3. **自证 artifact 当已验证**：哈希了能哈希的东西，未把哈希绑定到实际发生的事。
4. **预算是进程内存计数而非持久化事务**。
5. **结论措辞越界**：把"这些攻击未发现缺陷"说成"零缺陷"。

## 3. 方法变更（写入修复计划并已执行）

- 修复计划**不给权威代码块**，只给**不变量 + 必须从 ACCEPT 翻转为 REJECT 的探针**；
- 评审对照不变量与探针结果，不对照字面代码；
- 每轮修复后**攻击修复本身**——本次因此连续揪出同类递进缺陷（见 §4）；
- 结论只能表述为"以下攻击面在 N 轮中未被攻破"，并附攻击清单。

## 4. 修复实施（study 分支 `r0-repair`）

| 任务 | 不变量 | 内容 |
|---|---|---|
| T1 | I1 | 严格收据解析 + 与 loader **实时重算**比对；8 探针 |
| T2 | I2 | speech 载体 profile 白名单 + general-audio 拒绝名单（从 E0 配置读取以尊重冻结的"源码不得出现禁用名"不变量）+ exposure 行载体列**精确分词**绑定 |
| T3 | I3/I4 | payload↔plan↔split↔loader 值级绑定；媒体禁闭（adapter 与 transport 两条独立防线，拒绝绝对/盘符/反斜杠/穿越/符号链接与 junction 逃逸） |
| T4 | I6 | `(run_id, attempt_id)` 以 `O_EXCL` 原子占用；用量发送前落盘；无 attach/resume；slice 上限取登记与实际的保守上界 |
| T5 | I5 | localhost 限定 + session receipt 绑定二进制哈希/PID/**进程映像**/**套接字所有权（地址感知）**；逐次发送复验 |
| T6 | I7 | `saea-run-manifest-v1` 全链哈希闭包 + finalizer；计分只经 manifest；ABORTED 也必落可审计 manifest |
| T7 | I8 | GPU 秒/峰值显存（可注入采样器，缺失即 `NOT_AVAILABLE` 附原因）、CPU 秒、gate 时延、证据字节、tool calls、失败 attempt 成本 |
| T8 | — | 三条工程控制的正式 JSON config + `cost` scorer；entity/QA **不伪造适配器**，记入 owner 待决 |
| T9 | I9 | CI 改为真实 R0 语义并先装包；lint 门（active tree，隔离快照排除）；文档去除 pre-R0 残留声明，`coverage`/`type-check` 显式 `NOT_CONFIGURED` |

**递进式对抗的实证价值**：T5 连修三轮——绑定进程映像后，评审跑第二个同样的二进制即绕过；
绑定套接字所有权后，评审发现 `host` 参数收下未用（P 监听 `[::1]`、Q 监听 `127.0.0.1`，收据声称
P 却由 Q 应答，端到端实测）。同一不变量的前两轮修复都只堵住了被演示的那条路径，而非那一类。

## 5. 明确的残余边界（不得被过度信任）

1. **bundle 是自洽性检查，不是真实性证明**：拥有 run 目录写权限者可伪造一份完全自洽、可
   finalize 的 bundle（复核方已构造成功）。原始响应字节不留存，链条无外部锚（无签名、无
   write-once 存储）。已写入模块文档与 `docs/engineering.md`。
2. **check→send 竞态**：进程身份与套接字所有权在用户态校验，与实际发送之间存在窄窗口；
   llama-server 无内核级连接认证（loopback TCP 无 mTLS/SO_PEERCRED 等价物）可彻底关闭。
3. **entity/QA scorer 未注册**：参考层格式需 owner 定夺，见 study `docs/owner-decisions-pending.md`。
4. **GPU/VRAM** 在无 `nvidia-smi` 环境记为 `NOT_AVAILABLE` 附原因，非静默省略。

## 6. 提请 owner 处置

1. entity/QA scorer 是否属 R0 交付（参考层格式冻结需要 owner 输入）；
2. §5.1/§5.2 两项残余边界是否接受为 R0 范围边界；
3. R0.3 `SAEA-E-001` 执行授权与 attempt 预注册——**在新一轮独立复核通过前不启动**。

## 7. 下一步

按评审 §12 组装 fresh-rereview 提交包（修复后 commit、finding→code/test 闭合矩阵、五探针回归、
双 OS 全测试、真实 gate dry-run、D1–D4/split 实时重算、session/attempt 负测试、合成 run bundle +
finalizer dry-run、clean worktree 与 remote 绑定、owner 处置项）。R1 model-facing execution 维持
withheld。
