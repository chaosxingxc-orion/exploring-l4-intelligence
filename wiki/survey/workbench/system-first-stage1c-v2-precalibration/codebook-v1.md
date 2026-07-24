# Stage-1C v2 calibration codebook v1

## Coding unit

Paper 是 audit unit；run cell 是实验运行配置；observation 是 cell 上的单个 metric/evaluator 结果；claim 是
scope-bound proposition；family membership 是经过兼容性判断的关系，不是论文主题标签。

## Required paper fields

- `paper_disposition`：`EMPIRICAL_LOAD_BEARING / EMPIRICAL_RELATION_ONLY /
  NON_EMPIRICAL_EVIDENCE_NODE / BOUNDARY_OR_FALSIFIER / EXCLUDE_WITH_REASON`；
- `paper_role`：`DIRECT_PATH / COMPONENT_PATH / INSTRUMENT / NEGATIVE_OR_FALSIFIER / BOUNDARY /
  REFERENCE_ONLY`；
- `problem_nodes`：目标失败，可多标签，但必须标 primary/secondary 或 `UNROUTED`；
- `intervention_axes`：D0-D4，可多标签；不能替代 problem node；
- `mm_level`：MM0 文本、MM1 多模态任务、MM2 多模态资产、MM3 同运行 matched modality-necessity；
- `reference_borrow_reproduce`：三分合同；
- `source_locators`：所有承重事实必须有全文 locator。

## Run-cell boundary

以下任何一项实质变化都创建新 cell：dataset revision/split/slice、preprocessing/input、core revision/access、
prompt/system topology、K/S/M asset/version、persistence、tool权限、intervention/decision rights、reward-next-action
effect、budget/horizon 或 seed/aggregation contract。

Accuracy、WER、MOS、task success、latency、cost、harm 等多个 observations 不复制 cell。

## Paired comparison

- `EXACT_PAIRED`：除声明 intervention 外所有 comparability keys 一致；
- `PARTIALLY_MATCHED`：存在已知混杂，只允许带不确定性的并列；
- `UNPAIRED_PARALLEL`：不得计算跨论文 effect；
- `NOT_A_COMPARISON`：单一描述或无 baseline。

## Dataset graph

Lineage：`SAME_REVISION / DERIVED_FROM / SUBSET_OF / TRANSLATED_FROM / AUDIO_RENDERING_OF /
REANNOTATED_FROM / SPLIT_OF`，必须有来源证据。

Non-lineage relation：`INDEPENDENT_SAME_TASK / CROSS_DATASET_VALIDATION / DISTRIBUTION_SHIFT_TEST /
PROTOCOL_ANALOGUE`。语义相似不得编码为 lineage。

## Claim coding

先判断论文报告 claim 还是 cross-paper synthesis。Claim scope 必须包含 problem/outcome、task、dataset
revision/split、model、access、input、intervention、budget/horizon、evaluator。Scope 不兼容时不得因文字相似
强行合并；scope 兼容且命题等价时只保留一个 canonical claim ID。

Paper-to-claim relation：`SUPPORT / INSTRUMENT_SUPPORT / BOUNDARY_OR_FALSIFIER / CONTRADICTION`。

## Family coding

Calibration 阶段不得创建正式 family。只判断 candidate membership compatibility：

- target problem 是否相同；
- outcome semantics 是否兼容；
- environment/access 是否兼容；
- baseline→intervention comparison 是否可解释。

只有后续 mapping 才能形成 `CORE_MEMBER / VALIDATION_MEMBER / TRANSFER_ANALOGUE / FALSIFIER /
INSTRUMENT_SUPPORT`。八个 protocol templates 不构成 family。

## Critical disagreements

以下分歧必须逐条 adjudicate，不能被总体 agreement 掩盖：reproduction anchor、dataset lineage、MM3、
EXACT_PAIRED、CORE_MEMBER compatibility、claim merge/split、trained/gray-box/TF-Strict access。

Coder 不得根据年份、论文数量或主题新颖度推断重要性、方向排名或 novelty。
