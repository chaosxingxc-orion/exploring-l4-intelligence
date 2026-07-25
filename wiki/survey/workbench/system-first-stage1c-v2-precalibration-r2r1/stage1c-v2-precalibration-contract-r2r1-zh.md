# Stage-1C v2 Agentic 校准 R2R1 方法合同

## 1. 本轮目的

R2R1 只修复 R2 独立复审复现的三项承重缺陷，不重新设计校准、不更换论文，也不扩大研究
范围。输入仍是同一组 N=56：38 篇 overlays、18 篇 sentinels，以及完全相同的冻结 source
renditions。R1 的两份原始编码和 agreement、R2 的方法包都保持不可改写。

当前状态是 `AGENTIC_CALIBRATION_R2R1_METHOD_READY_NOT_DISTRIBUTED`。这表示方法合同已准备，
不表示 reviewer 已接受，更不表示 coder 可以开始工作。

## 2. 缺陷一：对象 ID 与引用必须强类型

R2 的编译器虽然生成了 `OBJ-*` identity，但把所有 coder-local ID 放在一个可覆盖的全局
map 中。两个对象复用同一 local ID 时，后写对象可能静默改变引用目标。

R2R1 的规则是：

1. 每种对象各自拥有独立 map；
2. 同一对象类型内的 local ID 在写入 map 前检查唯一性；
3. compatibility decision 必须同时填写 `target_object_type` 和 `target_object_id`；
4. 引用只允许在声明的 typed map 中解析，禁止跨类型 fallback；
5. 未声明、重复或无法唯一解析的引用在 agreement 前直接拒绝整个 response。

这允许 dataset node 与 run cell 偶然使用相同字符串，却不会把 dataset 引用解析为 run
cell。最终比较 identity 仍由冻结 source rendition、typed locator、对象类型和语义签名共同
生成，coder 不能填写 `object_match_key`。

## 3. 缺陷二：复现候选只能由肯定闭合的论文证据产生

论文可见的 reproduction support 拆成十项事实：task、dataset、dataset revision、split、
official repo、pinned revision、entrypoint、model access、license/terms、evaluator/ground truth。
每项事实必须编码为 `OBSERVED_IN_SOURCE`、`NOT_STATED_IN_SOURCE`、
`AMBIGUOUS_IN_SOURCE` 或 `NOT_APPLICABLE_IN_SOURCE`。

只有十项全部是 `OBSERVED_IN_SOURCE`、值不是占位符、access 不含糊、revision 是不可移动的
pin、blockers 为空时，才允许 `CLOSED_PAPER_SUPPORT`。`main`、`master`、`HEAD`、`latest`
等移动引用不能冒充 pinned revision。`REPRODUCTION_CANDIDATE` 至少需要一条这样的 closed
support。只要有一项未观察到，就必须是 `OPEN_WITH_BLOCKERS`，并记录至少一个 blocker。

这些规则只判断论文侧协议是否闭合。本地代码或数据存在仍只是 reviewer-only readiness，
不能自动升级为 reproduction anchor。

## 4. 缺陷三：agreement 必须绑定真正冻结的响应字节

R2 的 delivery receipt 绑定了输入包，却没有绑定 coder 实际提交的 response bytes。R2R1
增加独立 submission receipt：每名 coder 的 56 条 response 必须按 canonical paper order
组成一个 canonical UTF-8 JSON array。receiver 在冻结前检查：

- N=56、paper ID 顺序和唯一性；
- response ID 唯一性；
- coder、transaction、packet 和 source-manifest binding；
- schema 与完整语义合同；
- 原始 byte length 与 SHA-256。

两份 submission receipt 的 ID、receipt SHA、response SHA、byte length 和 paper-ID digest
进入 runtime intake；它们再与静态 frozen-package hash 共同生成 `frozen_response_root`。
Agreement v7 只接受 A/B 两份原始 bytes，并在任何 response 编译或 metric 之前重新计算并
比较 delivery receipt、submission receipt、response digest 和 frozen root。冻结后的任意
字节变化都会失败；冻结前的合法变化会生成新的 digest 和 receipt，不会与旧冻结状态混淆。

## 5. 不变项与后续门

- 0.85 gate 不变；union-object denominator 与 both-zero-only `NOT_CALIBRATED` 规则不变。
- coder-visible bundle 仍为八项，不包含 readiness、预期标签、submission receipt 或 reviewer
  positive-support ledger。
- Duplex specialized-system exclusion、零 reproduction anchor 和零研究执行保持不变。
- R2R1 必须先形成 commit-bound exact manifest，再由新的 no-fork 独立 reviewer 复审。
- 只有 `ACCEPT_AGENTIC_CALIBRATION_R2R1_METHOD_CONTRACT_FOR_CODER_INTAKE` 才能开启此前已授权
  的一次同 N=56 Sol/Terra recode。
- coder distribution、agreement、owner adjudication、320-work mapping、Stage-2A 和 push 都不
  由本合同自动触发。
