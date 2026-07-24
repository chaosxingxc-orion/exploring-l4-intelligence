# Agentic RC2R2 calibration codebook v4

本版继承 RC2R1 v3 的 paper labels、experiment objects、agentic scope、reference/borrow/reproduce
语义与逐字段 agreement gates，不改变研究分类。

新增的 provenance 规则如下：

- coder 必须保留 packet 中的 `paper_id`、`packet_item_id` 与 `source_manifest_id`；
- 每个 source locator 的 `rendition_id` 必须来自该论文在 source manifest 中的 primary 或
  alternate rendition；同一 manifest 内另一篇论文的 rendition 也不合法；
- `BORROW_PROTOCOL` 仍要求 source→speech/omni variables、保留的决策结构、locator、拒绝条件
  与可观察拒绝证据；
- `REPRODUCTION_CANDIDATE` 仍要求 task、dataset/revision/split、official repo/pinned revision、
  entrypoint、access、license/terms、evaluator/ground truth、local state 与 locator 全闭合；
- `REFERENCE` 不得暗含 transfer 或 reproduction evidence；
- 所有 56 份 response 必须在任何 agreement 或 adjudication 可见之前冻结。

delivery receipt 不是论文编码内容。它由 orchestration 层在分发/提交时生成，并绑定实际收到的
共享字节；coder 不得手工改写 frozen package contract 或 receipt digest。
