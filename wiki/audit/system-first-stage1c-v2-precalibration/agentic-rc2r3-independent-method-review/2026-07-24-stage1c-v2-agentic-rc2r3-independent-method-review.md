---
title: "Stage-1C v2 Agentic RC2R3 independent method review"
date: "2026-07-24"
artifact_type: "INDEPENDENT_AI_DOCTORAL_SUPERVISOR_ADVISORY_REVIEW"
campaign: "system-first-stage1c-v2-precalibration"
round: "agentic-rc2r3-independent-method-review"
reviewed_commit: "ee12a3a79bd578df996c44c4bdb2dbc709e2f616"
reviewed_manifest: "wiki/survey/workbench/system-first-stage1c-v2-precalibration-rc2r3/review-package-manifest-rc2r3.json"
reviewer_context: "fresh no-fork gpt-5.6-sol; interrupted once only to stop optional long replay, then resumed same isolated context"
verdict: "ACCEPT_AGENTIC_RC2R3_METHOD_CONTRACT_FOR_CODER_INTAKE"
human_signature_claimed: false
owner_authority_claimed: false
repository_modified_by_reviewer: false
---

# AI 博士导师方法顾问审查

审查对象仅为提交 `ee12a3a79bd578df996c44c4bdb2dbc709e2f616` 及其 commit-bound RC2R3
manifest。本审查不是人类签名、owner 裁决、coder 产出或执行授权；未修改仓库，未调用研究
模型、基准、复现或原型。

## 1. 提交与清单完整性

- manifest 自身为 7,858 bytes，SHA-256 为
  `02c5c68ffd1464601ebdbca9a09295d0e2a5d4fa6b3e740abc58763b3afdd944`。
- 声明、实际及唯一路径数均为 30。
- 30/30 artifact 均直接从该提交 Git blob bytes 重算；每项长度及 SHA-256 全部匹配，无缺失、
  重复或 working-tree 替代。
- frozen contract blob SHA-256 为
  `5c7b864adbde92c66d2230437fa5a09d1a6c5da5c9939afb4a7132279c2e8696`，与 manifest、contract
  report 及 agreement engine 编译常量一致。
- 八件 coder-visible artifact 逐件 blob 长度/摘要均与 distribution manifest 一致；按固定名称、
  NUL、八字节大端长度及原始 bytes 重算的 bundle digest 为
  `03674710223ad3c457e6568bdc83b66c1491abd84dd4e6d2c16495065e3ead64`。独立 prompt digest 为
  `88fca5a601bc49b946e2c29fcac35ba212dec38af5625c312a964535201aaa8e`。

## 2. 前驱不可变性

- RC2R2 提交 `9652d98eade798903be6c5d007591d2602a2f5c3` 是目标提交祖先。
- RC2R2 workbench 子树在前驱和目标提交中的 tree id 均为
  `c6ada0a6e33458825902c01cf1deeb9020da803e`。
- RC2R2 manifest 内嵌的 30 项 artifact 在前驱中全部匹配声明摘要，且目标提交中的对应 bytes 与
  前驱逐字节相同。
- RC2R3 的 11 项 `-inherited` artifact 与 RC2R2 对应 blob id 全部相同；RC2R2 builder、
  agreement-v4 及其更早运行时依赖也未改写。
- RC2R2 审查交易是追加到新的 audit 路径，而非改写 RC2R2 包。

## 3. 冻结阈值闭包

闭包成立：

- `AGREEMENT_MINIMUM = 0.85` 同时进入 builder、agreement engine、agreement contract、runtime
  intake 与 frozen root。
- `compute_agreement()` 虽保留兼容性参数，但在任何 provenance 或 metric 计算前调用
  `_validate_minimum()`；布尔值及任何不等于 `0.85` 的值均失败。
- static validation 再次核对 frozen contract、runtime intake 中的 `agreement_minimum` 和编译
  frozen hash。
- 实际 metric 调用直接传入模块常量，而非 caller 参数。
- 对抗测试覆盖 `0.01`、`0.84`、`0.86`、`1.0`，并验证拒绝发生在 metrics 前。

因此公开 RC2R3 agreement API 不能通过普通 runtime 参数降低或替换阈值。

## 4. Receiver-byte receipt 闭包

闭包成立：

- receipt builder 强制接收精确八件 `dict[str, bytes]` 及独立的 prompt `bytes`；缺件、多件、
  非 bytes、任一 artifact 单字节变化或 prompt 单字节变化均拒绝。
- builder 从传入原始 bytes 重算逐件长度/SHA-256、顺序 bundle digest 和 prompt digest，并要求
  独立 prompt bytes 与 `coder_prompt` artifact bytes 完全相同。
- receipt 自摘要覆盖 coder slot、coder id、transaction、process、task、model、distribution
  identity、实际 byte 摘要和时间字段。
- runtime binding 对 A/B receipt 与外部 binding 的 coder/transaction/process/task/model 逐字段
  交叉核对。
- agreement engine 验证严格 receipt schema、自摘要、八件有序 artifact rows、bundle/prompt
  摘要以及 intake 中 receipt id/digest/received hashes。
- 测试覆盖 receipt 重签后的 coder、task、distribution、bundle、prompt、逐件 artifact 及 intake
  binding 篡改。

合同也准确限定证明强度：receipt 仅证明受控 builder 所观察到的本地 bytes，不宣称 provider 数字
签名、人类独立证明或不可伪造的第三方身份认证。此限制与当前 intake 威胁模型一致。

## 5. Typed path 与严格形状闭包

闭包成立：

- 授权判断使用不可混淆的 `("key", value)` 与 `("index", value)` segments；通配只允许匹配
  index kind。
- JSON Pointer 转义仅用于决定之后的显示，不参与 allowlist 判断。
- 真正 `items` 数组下的身份字段可获豁免；文字 key `items[0]`、`items.0`、`items/0`、
  `items~10` 等不能伪装成数组索引。
- blind packet 顶层 key 集合被精确冻结，任何额外 key fail closed。
- 对抗测试同时验证 forbidden value 扫描与严格顶层形状拒绝，并覆盖 bracket、dot、slash 和
  pointer-escape spellings。

未发现 RC2R2 的结构路径 alias 可在 RC2R3 中复现。

## 6. Coder blindness、方法门禁与权限边界

- coder-visible bundle 精确限制为八项；codebook 与 prompt 明示仅使用供给 bytes、禁止
  repository、network discovery 和另一 coder 输出。
- inherited blind packet、source、assignment、codebook、prompt 与 RC2R2 blob 相同，RC2R3 未
  加入 paper label 或预期答案。
- transaction contract 将两个 coder 限定为不同模型配置、fresh/no-fork、独立
  process/workspace，并明确不宣称 provider independence 或 human inter-rater independence。
- coder slots、adjudicator、task identities 和 exposure declarations 均尚未赋值；distribution
  manifests 保持 `distribution_authorized=false`。
- agreement 要求两份 raw output 先冻结；承重分歧仍交 owner adjudication。
- artifact 一致记录：没有 coder distribution、agreement、研究模型调用、benchmark、复现、
  prototype、novelty verdict、full mapping、Stage-2A 或 push 授权/完成主张。
- 本次接收仅能打开既有授权下的 N=56 coder intake；不产生 mapping、adjudication、research
  execution、Stage-2A、portfolio 或 push 权限。

## 7. 测试、覆盖率与平台证据

- 测试源码含 18 个 RC2R3 adversarial tests，三类原缺陷均被直接攻击，并覆盖 compiled root、
  static projection、N=56、receipt identities、response validation、coder leakage 与 authority gates。
- 在目标提交的 clean working tree、禁用 bytecode 写入条件下，本次 Windows Python 3.14.3 复验
  通过 18/18 RC2R3 tests；更宽的 RC2 系列 discovery 通过 80/80，复验后工作树仍无修改。
- commit-bound summary 记录 branch-aware coverage：agreement 88%、builder 84%、combined 86%，
  均高于 80% 门槛；并记录 Windows 3.14 与 WSL2 Ubuntu-24.04 / Python 3.12 均 PASS、frozen hash
  相同。
- 本次没有再次运行 WSL 或覆盖率工具；平台与覆盖率百分比因此属于已检查的 commit-bound
  evidence，而不是本审查重新生成的测量。后续交易仍宜保存精确命令、cwd、解释器路径、coverage
  分母和 post-write diff exit code。这是证据可复验性的改进建议，不削弱已由代码、对抗测试和独立
  blob 重算闭合的三项运行时缺陷。

综合判断：未发现阻止 coder intake 的具体、可复现、边界明确的方法合同缺陷；接收不延伸任何被
保留的执行或 owner 权限。

`ACCEPT_AGENTIC_RC2R3_METHOD_CONTRACT_FOR_CODER_INTAKE`
