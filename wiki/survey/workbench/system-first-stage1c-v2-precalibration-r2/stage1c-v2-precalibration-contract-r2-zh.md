# Stage-1C v2 Agentic 校准 R2 方法合同（送审稿）

## 1. 本轮解决什么问题

R1 的失败不是一个可以靠 owner 裁决抹平的普通分歧。它暴露了两个结构性问题：第一，coder
自由书写 `object_match_key`，导致语义上可能对应的对象在结构上完全无法比较；第二，字段一致率只在
已匹配对象中计算，使 unmatched 对象把字段分母变成零。与此同时，旧 reproduction schema 要盲
coder 报告其无权看到的本地资产状态，造成 mandatory positive 在结构上不可表达。

R2 是 owner 授权的唯一一次有界 consolidation。它保持 N=56、38 overlays、18 sentinels、全部
source bytes 和 R1 raw evidence 不变，不通过替换样本或补发预期标签提高一致率。

## 2. 对象身份与一致率

Raw response schema 已删除所有对象的 `object_match_key`。Coder 只提供语义字段、局部引用 ID 和
source locator。编译器根据冻结 rendition SHA256、anchor type、规范化 coordinate 生成 source
anchor，再解析 dataset/run/observation/comparison/edge 之间的引用，最后生成确定性 segmentation
signature。不存在 fuzzy matching、语义后配对或 adjudication 后重写身份。

Agreement 对每个 paper × object type 使用 compiled-key 的精确并集。Unmatched 对象不仅使
segmentation 失败，也在每个适用 critical field 中各占一个 disagreement denominator。只有双方对
该类都输出零对象时才是 `NOT_CALIBRATED`。这直接关闭了 R1 的“零匹配 → 零字段分母”漏洞。

## 3. 抽取完整性

`EMPIRICAL_EXTRACTABLE` 必须含 material run cells、observations 和 dataset nodes。运行条件变化
建立新 cell，同一运行的多指标留在 observations。能够闭合 baseline/intervention 和 comparability
key 时必须建立 paired comparison；否则必须给 typed absence reason。Dataset lineage/relation 必须
有来源证据，任务相似不得冒充血缘。对象 locator 不能只指向 title 或 abstract。

## 4. 参考、借鉴、论文可复现支持与本地 anchor

R2 把五个概念拆开：

- `REFERENCE` 不迁移协议和结果；
- `BORROW_PROTOCOL` 必须包含 source→speech/omni 翻译、保留的决策结构和可观测拒绝条件；
- `paper_reproduction_support` 只记录论文 bytes 中可见的 task/data/repo/entrypoint/access/terms/
  evaluator，可以 `OPEN_WITH_BLOCKERS`；
- `REPRODUCTION_CANDIDATE` 必须有无 blocker 的 `CLOSED_PAPER_SUPPORT`；
- reviewer-only `local_reproduction_readiness` 才记录本地 checkout、资产、loader 和许可状态。

Calibration 不得产生 `REPRODUCTION_ANCHOR`。Anchor 还需要 paper support、本地闭合和后续 100%
复核，三者不能由“仓库存在”自动推导。

## 5. Mandatory positive preflight

Reviewer-only ledger 在不向 coder 泄漏预期标签的前提下证明：TRACE 第 3 页支持 `SUBSET_OF` 与
`REANNOTATED_FROM` 两条 dataset edges；AudioToolAgent 第 1 页明确给出官方 repo、任务与评测
载体，能够生成一条 `OPEN_WITH_BLOCKERS` 的 paper support。Exact R2 schema 对两类均可表达，
preflight 为 PASS；N=56 没有变化。

## 6. 仍然关闭的权限

当前状态是 `AGENTIC_CALIBRATION_R2_METHOD_READY_NOT_DISTRIBUTED`。只有新的独立 reviewer 对
commit-bound exact manifest 返回
`ACCEPT_AGENTIC_CALIBRATION_R2_METHOD_CONTRACT_FOR_CODER_INTAKE`，才能启动两个全新隔离
Sol/Terra 上下文的唯一一次完整 N=56 recode。

本合同不授权 320-work mapping、owner adjudication、研究模型、benchmark metric、论文复现、
prototype、novelty verdict、Stage-2A 或 push。R2 若任一已校准 critical gate 低于 0.85，或 mandatory
class 仍为 `NOT_CALIBRATED`，必须停止并回到独立方法复审。
