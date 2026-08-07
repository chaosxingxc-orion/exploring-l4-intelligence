---
title: "R0 repair submission package for fresh independent rereview"
date: "2026-08-05"
artifact_type: "IMPLEMENTATION_TEAM_SUBMISSION"
campaign: "speech-aware-evidence-acquisition-r0-review"
round: "independent-review-2026-08-05"
responds_to: "2026-08-05-saea-r0-independent-review-assessment.md §12"
study_commit_submitted: "7b90762f9acbbc59179fb6fb7e1ec96866e8ffbe"
study_branch: "r0-repair"
model_touch_performed: false
owner_authority_claimed: false
---

# R0 修复提交包（供新一轮独立复核）

> **状态：FINAL（2026-08-07）。** 提交 commit：study `62baab9`。经**五轮**外部视角对抗终审
> （每轮由不同复核方自合同独立推导威胁模型，均未使用实施方清单），第五轮返回
> `ZERO_DEFECTS_CONFIRMED`（Critical/Important 层面零发现），其唯一 Minor 与一条改进建议已在
> `62baab9` 关闭。前四轮的全部发现见 §11 趋势表——**该表是本包最重要的成熟度证据**，请勿只看
> 最后一轮的绿灯。

按评审 §12 的最小提交包清单组织。**本件只记录实施方控制面亲自验证过的事实**；子代理报告中未经复核
的表述不进入本件（本轮已出现过一份报告声称存在、实际不存在的测试，故采用此纪律）。

## 1. 修复后的 exact study commit

- study：`7b90762f9acbbc59179fb6fb7e1ec96866e8ffbe`（分支 `r0-repair`，自 R0 基线 `b0635aa` 起 21 个提交）
- umbrella：`28d6736`（治理更正 + 本回应文档；`b0635aa` 时代的 "zero defects" 表述已撤回）
- 两仓工作树在提交时点 clean。

## 2. finding → 闭合矩阵

| 评审 finding | 关闭方式 | 关键机制 |
|---|---|---|
| P0-1 split 收据自证 | T1 | `core/split_receipt.py`：严格解析（schema/精确键集/count/前缀/唯一/互斥）+ **从 ids 重算 identity_hash** + **与当前 loader 实时重算逐位比对**；`run_experiment` 只接受 `VerifiedSplit` |
| P0-2 carrier/payload/media 未绑定 | T2 + T3 | gate：speech profile 白名单 + general-audio 拒绝名单（从 E0 配置读取）+ exposure 行载体列**分词精确匹配**；adapter：payload↔plan↔split↔loader 值级绑定；媒体路径规范化 + carrier root 禁闭，adapter 与 transport **两条独立防线** |
| P0-3 磁盘 runtime ≠ 响应 server | T5（三轮） | localhost 限定；session receipt 绑定二进制哈希 + **进程映像**（`/proc/<pid>/exe` / `QueryFullProcessImageNameW`）+ **套接字所有权（按 family+地址+端口）**；**逐次发送复验** |
| P0-4 额度可重复消费 | T4 | `(run_id, attempt_id)` 以 `O_EXCL` 原子占用（create+write 原子化）；用量**发送前**落盘；无 attach/resume；slice 上限取登记与实际的保守上界 |
| P1-1 产物链无闭包 | T6（两轮） | `saea-run-manifest-v1` 绑定 study commit/配置/协议/plan+attempt/split/session/各产物哈希/实际成本/终态；`verify_bundle` 从字节重算；计分只经 manifest；ABORTED 也必落可审计 manifest |
| P1-2 MLflow/台账非事务 | T6 | `finalize` 校验 → 计分 → 写 scores → 上传（含 raw trace）→ **由已验证 manifest 派生**台账行；人工填写与 manifest 冲突即拒 |
| P1-3 控制/scorer 只有结构 | T8 | 三条控制的正式 JSON config + `earnings21-discovery` 数据片段（与冻结收据一致）；`scorers` 写入片段；`cost` scorer 注册；**entity/QA 未伪造适配器**，记入待决 |
| P1-4 效率记账不全 | T7 | GPU 秒/峰值显存（可注入采样器，设备可 pin，缺失记 `NOT_AVAILABLE`+原因）、CPU 秒、gate 时延、证据字节（供给/采纳分列）、tool calls、失败 attempt 成本 |
| P1-5 CI 为 pre-R0 语义 | T9 | CI 改为真实语义并**先装包**；新增 lint 门（active tree，隔离快照排除）；文档去除 pre-R0 残留、显式 `NOT_CONFIGURED` |
| P2 文档漂移 | T9 + T8 | README 树与真实包一致（含 `contracts.py`、`resources.py`）；baseline README 改 JSON 且不再宣称无条件可运行；YAML 片段的非 composer 身份写明 |

## 3. 五探针回归（评审 §10.3 的表，修复后）

| Probe | 修复前 | 修复后 | 常驻回归位置 |
|---|---|---|---|
| P1 exposure=earnings21 + plan `fsd50k` | ACCEPT | **REJECT** | `tests/contract/test_carrier_scope.py` |
| P2 收据 ids 换、hash 留旧 | ACCEPT | **REJECT** | `tests/unit/test_split_receipt.py`（含真实同载体 ID 互换与互斥首发探针） |
| P3 data root 外绝对 media 路径 | READ/SEND | **REJECT**（adapter 与 transport 各自独立） | `tests/unit/test_frozen_core_adapter.py`、`test_llama_server_transport.py` |
| P4 同一额度重复开门 | ACCEPT×2 | **REJECT**（第二次） | `tests/contract/test_attempt_accounting.py` |
| P5 earnings21 plan + `fsd50k` payload | ACCEPT | **REJECT** | `tests/unit/test_frozen_core_adapter.py` |

修复过程中由复核自身新发现并已关闭的同类攻击（均为常驻回归）：伪造 session 收据用任意活进程 PID；
第二个同 pinned 二进制实例 + 伪造端口；`host` 参数收下未用导致 v4/v6 错配（P 监听 `::1`、Q 应答
`127.0.0.1`）；清空 raw trace 跳过 outputs↔trace 校验；脏树下成功 run 无 manifest 且 attempt 永久
OPENED；真实四片 config 组合实际不可运行；`scorers` 从未被任何片段设置。

## 4. 双 OS 全测试（控制面亲自复跑于提交 commit）

- Windows：**696 passed / 24 skipped**（提交 commit `62baab9`，控制面亲自复跑）
- WSL2 Ubuntu-24.04：**712 passed / 8 skipped**
- 受体收据合同：`tests/contract/test_real_receipts.py` 4 passed（两平台）

**已知环境敏感性（主动披露）**：`tests/unit/test_session.py` 与 `test_llama_server_transport.py`
会真实 spawn 子进程并绑定本机套接字。修复期间一个子代理在**多代理并发高负载**窗口内观察到该两文件
出现超时类失败（10 failed / 14 errors），控制面随后在同一 commit 上连续 5 次复跑（3 次聚焦 + 2 次全量）
**无法复现**，WSL 侧同样全绿。判断为负载相关的测试脆弱性而非产品缺陷，但复核方在高负载环境重跑时
可能重现；相关测试已内置 spawn 重试与超时放宽。

## 5. 真实 gate dry-run（model-free）

WSL2，`SPEECHRL_DATA_DIR` + `LLAMA_RUNTIME_ROOT=/home/chao`：`bash scripts/reproduce.sh` →
`GATE OPEN (dry run)`，exit 0。**冷路径 2m25s**（全量逐文件哈希 34.7GB GGUF + 全部 `build/bin`
运行库）；**热路径 0.98s**（廉价身份比对；运行库与启动器仍全量）。`--full` 强制全量仍为 2m23s。
热路径证明的是"文件的路径/大小/mtime/inode 与记录一致且运行库字节未变"，**不证明** GGUF 字节
未被同尺寸同 mtime 地原地替换（§8.5）。

## 6. D1–D4 与 split 实时重算

D1–D4 收据自 E0 关闭起未改（`docs/receipts/*.json` 在整个修复窗口 zero diff，已用 `git diff --stat`
路径限定确认）。split 的实时重算现在是**运行时强制**（T1），不再是一次性生成：任何模型触达前，
收据必须与当前 loader 重算结果逐位一致。

## 7. 环境完整性事件（主动披露）

修复期间一个并发子代理把共享 Python 环境的 editable 安装指向了自己的临时 worktree，导致一段时间内
"测试通过"的证据可能来自别处代码。控制面发现后核实导入路径已指回本仓并独立复跑全套件，数字与上报
一致。此后所有关键结论均由控制面独立复跑后采信。**建议复核方将"评估环境本身是否被污染"纳入检查项。**

## 8. 明确的残余边界（不得被过度信任）

1. **bundle 是自洽性检查，不是真实性证明**：拥有 run 目录写权限者可伪造完全自洽、可 finalize 的
   bundle（复核方已构造成功）。原始响应字节不留存、链条无外部锚（无签名、无 write-once 存储）。
2. **check→send 竞态**：进程身份与套接字所有权在用户态校验，与实际发送之间存在窄窗口；loopback TCP
   无内核级连接认证可彻底关闭。
3. **GPU 采样**：设备级而非进程级；尾部不足一个采样间隔的时间未计入（有界低估）；无 `nvidia-smi`
   时记 `NOT_AVAILABLE` + 原因。
4. **entity/QA scorer 未注册**：参考层格式需 owner 输入，见 `docs/owner-decisions-pending.md`。
5. **GGUF 热路径**：同尺寸同 mtime 的原地字节替换检测不到（owner 2026-08-06 批准的取舍，
   由一条专门测试锁定为已知事实，而非散文承诺）。
6. **`config_hash` 与 `scorers`** 目前只做形状校验，未从真实 config 片段字节重算——
   **未被当作"已验证"字段冒充**，记于 `docs/owner-decisions-pending.md`。
7. **`earnings22-original` 无证据身份覆盖**（D1 未冻结其证据层）：为其配置证据源时 fail-closed
   拒绝，非静默豁免。

## 9. 尚未做的事

- R0.3 `SAEA-E-001` **未执行**；exposure ledger 无新行；无任何模型触达。
- R0.1 readiness 备忘仍为模板，owner 未拍板 R1 基线。
- 提交包未 push（本地 commit；发布需 owner 授权）。

## 10. 五轮外部终审趋势（成熟度证据）

| 轮次 | Critical | Important | Minor | 其中"上一波修复自己引入的" |
|---|---|---|---|---|
| r1 | 0 | 4 | 5 | — |
| r2 | **1** | 5 | 4 | 1 |
| r3 | 0 | 3 | 2 | **2** |
| r4 | 0 | 1 | 3 | 0 |
| r5 | 0 | **0** | 1 | 0 |

严重度、数量与"修复引入新缺陷"的比率三条曲线同时下降。**实施方明确不主张"零缺陷"**——
可主张的最强表述是：五轮独立推导的威胁模型攻击下，最后一轮在 Critical/Important 层面未被攻破。

一个应当被记录的教训：三条身份轨（媒体 r2、参考 r3、证据 r4）本属同一类遗漏，却分三轮才补全。
当为某类资产加上"验证而非信任"的轨时，必须立即枚举全部同类资产。

## 11. 本轮 owner 指令带来的合同/设计变更（2026-08-06/07）

1. **数值预算帽废止**（signed amendment：`wiki/audit/speech-aware-evidence-acquisition-r0-review/2026-08-06-owner-amendment-retire-first-slice-budget-caps.md`）：
   P0-4 的一次性消费部分仍关闭；数值上限部分由 owner 主动收窄合同义务，**不得再作为缺陷上报**。
2. **GGUF 验证放宽**（owner 批准）：全量哈希改为廉价身份（size/mtime_ns/st_ino/st_dev）比对 +
   变更/显式/每进程首次触达时全量。冷 2m25s → 热 0.85s。残余弱点"同尺寸同 mtime 原地替换"
   由一条专门测试锁定。运行库与启动器仍永远全量。
3. **代码规模与抽象整改**（owner 指令）：最大文件 1806 → ≤320 行，平均 134；载体布局知识收敛为
   `CarrierDescriptor`，新增载体 = 一个描述符 + 一次 loader 注册，并由"合成第三载体"测试证明。
   合同冻结常量（general-audio 拒绝名单、载体 profile 白名单、执行 profile、Stage-3 门）
   **刻意未配置化**——可配置即可绕过。
   重构安全性经独立验证：139 个搬移函数中 119 个 AST 完全一致，其余 22 个逐一核对；
   **无任何拒绝规则丢失**；每个再导出解析到被验证的同一对象。

## 12. 提请 owner 处置

1. entity/QA scorer 是否属 R0 交付范围；
2. §8.1 与 §8.2 两项残余边界是否接受为 R0 边界；
3. R0.3 执行授权与 attempt 预注册；
4. 是否将本包推送到远端以供复核方拉取。
