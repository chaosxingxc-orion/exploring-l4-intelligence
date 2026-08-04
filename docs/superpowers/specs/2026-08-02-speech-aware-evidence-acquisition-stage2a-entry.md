# Speech-aware evidence acquisition: Stage-2A engineering entry contract

## Status

Stage-1C 于 2026-08-02 获 `PASS_STAGE1C_FORMAL_OPENING`，owner 于 2026-08-03 签发 GO，并于
2026-08-04 将对象收窄为 speech-only、完成语义身份迁移。当前冻结值以
`wiki/experiments/speech-aware-evidence-acquisition/2026-08-04-owner-speech-domain-scope-and-identity-contract.md`
为准；本件规定 E0→R0→R1→X 的工程顺序。

```yaml
semantic_research_object: speech-aware evidence acquisition
source_candidate_provenance: R2
stage1c_decision: PASS_STAGE1C_FORMAL_OPENING
authorization: OWNER_GO_AND_EXECUTION_CONTRACT
authorization_record: wiki/experiments/speech-aware-evidence-acquisition/2026-08-04-owner-speech-domain-scope-and-identity-contract.md
domain: speech-only
general_audio: excluded_from_study_but_retained_locally
novelty_status: NOT_YET_DETERMINED
method_status: EXPLORATION_SPACE_ONLY
repository_slug: speech-aware-evidence-acquisition
repository_url: https://github.com/chaosxingxc-orion/speech-aware-evidence-acquisition.git
experiment_index: wiki/experiments/speech-aware-evidence-acquisition/README.md
```

## Purpose

Stage-2A 的首要任务不是继续扩大论文和数据清单，而是把 research question 变成可执行、可归因、
可复核的 speech-domain 实验。先证明载体身份、信息边界、scorer、trace 与 closest-prior 路径可运行，
再测试外部控制平面的候选机制。创新性和最终技术方法仍由 Stage-2A/2B 证据决定。

## Immutable boundary

- 冻结 Qwen3-Omni 核只经 API-shaped boundary 访问；不修改参数、结构或声学训练范式。
- 无 task-trained model，无第二个具有最终答案权的 LLM。
- 范围只含 speech signal 与语言任务；general/environmental audio 数据不得进入任何 arm。
- gold answer、reference transcript、test annotation、future turn 不得进入 runtime。
- `OBS`、`ORG`、`SUPPLY`、`USE` 分开 trace；外部响应、工具动作、请求与派生物均可版本化和哈希。
- discovery 与 confirmatory 隔离；confirmatory 规则在读取结果前冻结。

## Research axes

1. `OBS`：从 speech signal 形成的转写、实体与片段观察；
2. `ORG`：知识的粒度、结构、索引、来源和时间组织；
3. `SUPPLY`：证据选择、数量、顺序、模板与供给时机；
4. `USE`：证据准入、核验、拒绝、再查询、停止和最终采用。

一次机制实验只能把预注册的轴视作 intervention；其余轴必须冻结或纳入完整 factorial。只报“加知识
前后总分”不能支撑机制结论。

## Entry sequence

### E0 — model-free closure

1. 对 `earnings21-original`、`earnings22-original`、`conec` 做跨层 sample/segment identity；
2. 固化每个 arm 的 runtime visible fields 和 leakage checks；
3. 固化 WER/entity/QA scorer、normalization、correct-to-wrong 与 wrong-to-correct；
4. 生成十样本 loader/provenance/四轴 trace 收据；
5. 核验 license/redistribution，数据身份只引用 `docs/datasets.lock.json`；
6. 明确检查 FSD50K、AudioSet、ESC-50 未进入依赖图或测试发现路径。

### R0 — reproduction-zero vertical slice

- 一个 discovery carrier 和一个未读 confirmatory carrier；
- deterministic loader、frozen-core adapter、四轴 trace 与 scorer adapters；
- bare core、固定合法 context、固定 retrieval/context 三个工程控制；
- random/mismatched evidence 负对照和 oracle-evidence 上界接口（oracle 不进入正式 runtime）；
- MLflow 与 umbrella experiment index 的 URI/hash 连接；
- 调用、token、latency、GPU/CPU、speech-audio seconds 与证据 bytes 记账。

R0 只验证 wiring 与 measurement integrity，不构成优越性或创新性证据。

### R1 — closest/strongest-prior reproduction

优先在相同 speech task、carrier 与 information boundary 下冻结 ConEC/contextual ASR、RECOVER-style
correction、实体消解和 contextual-biasing 候选。首次 run 前记录 exact runnable revision、prompt、
scorer 与不可运行原因。冻结 mandatory baseline 失败时报告 `INCONCLUSIVE_BASELINE_NOT_READY`。

### X — directional exploration

在至少一个 closest-prior 可信复现之后，按最小可辨识顺序测试：

1. `OBS` 是否减少实体误听；
2. 在 OBS 冻结时，`ORG/SUPPLY` 是否提高合法证据可访问性；
3. 在供给冻结时，`USE` 是否降低错误证据造成的 correct-to-wrong；
4. reward-guided next action 是否优于固定一次检索/固定 rerank；
5. 增益是否在 secondary speech carriers 上保留，而不是只适配 Earnings。

## Evaluation gates

| Gate | 必须回答 |
|---|---|
| Effectiveness | 任务/实体/QA 指标是否提高，分布和尾部是否稳定？ |
| Reasonableness | 增益来自哪一轴？证据是否相关、有来源、无 gold 泄漏？是否增加 correct-to-wrong？ |
| Efficiency | 增益对应多少调用、token、latency、GPU/CPU、speech seconds 和 evidence bytes？是否位于 Pareto 前沿？ |

## First two-week deliverable

- E0 四门与 runtime receipt；
- core carrier 的 end-to-end discovery/confirmatory 路径；
- bare/fixed-context/random-evidence/oracle-bound controls；
- 一个 readiness-qualified closest-prior smoke/reproduction attempt；
- 一张 effectiveness/reasonableness/efficiency 联合表；
- 下一切片的 go/narrow/repair/stop memo。

遇到信息泄漏、样本身份漂移、scorer 不一致、许可问题、runtime pin 不可复现或未处理的同边界更强
runnable prior 时立即 stop-the-line。

## Literature and data delta policy

文献采用每周有界 delta lane。新工作默认只更新 prior/threat queue；只有推翻研究问题、载体合法性、
信息边界或可复现合同时才重开 Stage-1。新论文提到数据集不自动产生下载义务；只有被一个预注册实验、
baseline 或诊断问题消费，且小于 1 TB、公开可得、许可可接受时才进入 acquisition proposal。
