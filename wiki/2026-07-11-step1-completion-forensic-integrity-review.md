# 2026-07-11 Step-1 完成声明法证复审与研究诚信裁决

> **审查日期：** 2026-07-11（Asia/Singapore）  
> **审查阶段：** Stage 1 / Problem Definition  
> **审查性质：** hostile forensic re-review；只读核验；不是对个人动机的裁判  
> **代码快照：** umbrella `d8ab92350ce29966afeb7e45b58240bcc551381e`；W1 `47e490d2f5517e15803aec0ffbb15ef86221ebec`；W4 `f154886c26d93ddc259f88c74d6f425aa19efe8e`  
> **写入边界：** 本轮未修改研究代码、原始工件、claim ledger、实验记录或团队回复；只新增本审查报告。W1 原有 dirty 文件 `scripts/knowledge/kb_embed.py` 保持原状。  
> **总裁决：** **REJECT STEP-1 CLOSEOUT；保持 STOP-THE-LINE。允许继续明确标注为 exploratory 的 DEV 工程诊断；不允许进入现有 locked TEST、Phase-B、论文解禁或确认性主张。**

---

## 0. 一页裁决

这轮整改不是“完全无效”。团队真实修复了多项严重错误：撤销了 M3/T7 泄漏阳性，承认旧 MInDS `+0.126` 的 transductive/card 混淆，修正 ASR macro/corpus WER 与种子耦合，采用 speaker-grouped CREMA 评估，保留了负结果、失败项和 wav-cache 事故，并增加了 claim ledger、row-level artifact 与 clean-provenance rerun。这些行为与“系统性凭空造数、删除所有负结果”的假设不相符。

但是，**“做了大量纠错”不能推出“Step-1 已经科学闭环”**。本轮仍存在五个足以否决 closeout 的 P0 问题：

1. Proposal-R 的核心 Phase-A `squtr` / `vocalbench-knowledge` 实际没有构造所声称的 external-knowledge passage；当前 KB value 是问题/query 本身。
2. 所谓 locked TEST 的 ID 明文提交在 Git 中，64/65 个数据集还含旧暴露测试样本，无法证明 untouched/blinded。
3. ASR 的“Holm family-wise survives”只对事后缩窄的 `4 selectors @ N=8` 家族成立；按实际 discovery grid 的 `4×4=16` 比较，noise2 logprob@8 也不显著。
4. 65 个 locked-DEV artifact 全部 `git_dirty=true`，且缺 manifest、dataset revision、engine/model hash；其中有 24 个 item errors 和 4 个 scoreless cells。
5. Proposal-R 仍是未签署 DRAFT，G2-L3 未完成，load-bearing `kb_embed.py` 仍 dirty；协调者放行 DEV 不能替代 owner preregistration/sign-off。

### 学术欺诈裁决

- **fabrication（捏造数据）：未发现直接证据。**
- **falsification（篡改/遗漏使研究记录失真）：尚不足以作出成立认定。**
- **plagiarism：本轮未见相关证据，亦非本轮核心范围。**
- **严重 QRP、错误对象、统计包装、provenance failure、假性 held-out：已经确认。**
- **是否可以宣告“没有欺诈”：不可以。** 当前证据只支持 `NO FFP FINDING / INTENT UNDETERMINED`，不支持给团队作无条件洗清。

按 [ORI 的正式定义](https://ori.hhs.gov/definition-research-misconduct)，fabrication 是编造数据或结果，falsification 包括操纵过程或改变/遗漏数据使研究记录不能准确反映研究，诚实错误与意见差异不自动构成 misconduct。因此，本报告严格区分“结论无效或误导”与“已证明故意造假”。

**但是：** 团队在收到本报告后若仍把 query-KB 写成 knowledge retrieval、把公开 test IDs 写成 untouched holdout、把内部 AI QA 写成 independent replication、把 Holm4 写成完整 discovery family 校正，或覆盖旧 KB 而继续用不含内容的 build hash 证明“没有变化”，则不再是单纯的无知错误，应升级正式 falsification inquiry。

---

## 1. 审查方法：三轮对抗式复核

本轮不是只读团队总结，而是对 committed row-level artifacts、代码路径、Git/dirty state、统计摘要和跨文档传播进行反向验证。

### Round A — 数值与工件复算

- 从 ASR `per_utt` 的 S/D/I/N 重建 corpus WER、selector×N 点估计与 bootstrap p 值。
- 从 CREMA 逐 clip correct 字段复算四个 fold-seed 的效应。
- 从 MInDS hits 重算四个 factorial arms、删除 exact-text overlap 后的效应、support-draw 分布。
- 对 65 个 locked-DEV JSON 核对 manifest IDs、重复、error、scoreless、aggregate 与 provenance。

### Round B — 红队边界与 chain-of-custody

- 追踪 `squtr`、`vocalbench-knowledge` 从 loader 到 `values.jsonl` 的真实 value 语义。
- 检查 KB 原位覆盖、build hash 覆盖范围、freeze 时间字段和派生 JSON 生成器。
- 比较 locked TEST 与旧 exposed TEST 的 membership overlap，并检查 ACCESS_LOG 是否能证明未读。
- 检查 ledger 中 commit/hash/reviewer ID 是否可达、可追踪。

### Round C — hostile meta-review

- 将“已修复”与“已验证”逐项分离。
- 将 discovery、robustness check、computational reproduction、independent replication 分离。
- 按 Stage-1 规则重新分级：小样本数字只能是 directional，不得自动升级为 Stage-2 evidence。
- 按研究诚信定义分别判断事实失实、QRP、正式调查触发器与 FFP 证据。

这里的多代理审阅仍然只是**内部对抗 QA**，不是独立研究团队复现。National Academies 将“同一数据与代码得到一致计算结果”称为 reproducibility，而“针对同一科学问题、用新数据得到一致结果”称为 replicability；二者不能互换（见 [NASEM reproducibility/replicability brief](https://nap.nationalacademies.org/resource/25303/Combined%20Reproducibility%20Brief%20vs2.pdf)）。

---

## 2. P0-1：Phase-A 的核心对象不是所声称的 knowledge retrieval

这是本轮最严重的新发现。它不是“指标还需优化”，而是**研究对象错了**。

### 2.1 `squtr` 的 knowledge-passage 实际是 query/question

当前文件：

`E:\speechrl-knowledge\knowledge_base\squtr__glap__single-utt__knowledge-passage\values.jsonl`

其中 value 是 FiQA query，例如：

`Tax implications of holding EWU ...?`

它不是 qrels 指向的 corpus document，也不是 external knowledge passage。代码路径解释了为什么：

- `kb_batch_build.py:159-173` 中 `value_spec="text"` 取 `row.meta.text`；
- `squtr.py:163-167, 189-195` 明确说明标准 loader 的 `meta.text` 是 query text，`gold` 只是 doc-id qrels；
- 真正的 qrels corpus 构造只在 `plan_squtr_mini_corpus()` 中出现，而该函数在 `kb_batch_build.py:114-139` 明确写着 **PLAN MODE ONLY / nothing persisted**；
- real `build_one()` 在 `kb_batch_build.py:478-513` 仍遍历 query rows，并把 `_extract_value(r, value_spec)` 交给 KB。

因此，当前系统至多研究“speech query → similar stored query”的检索或 ICL，不是 Proposal-R 所定义的“answer-scrubbed external knowledge retrieval”。后续即使产生正增益，也不能据此解释为模型利用了外部知识。

### 2.2 `vocalbench-knowledge` 也把 question 当作 fact

当前文件：

`E:\speechrl-knowledge\knowledge_base\vocalbench-knowledge__qwen3-omni-own__single-utt__knowledge-passage\values.jsonl`

首条 value 是：

`What is the name of the currency used in Switzerland?`

这是问题文本，不是答案、事实或 evidence passage；但 source 名仍写 `knowledge-passage`，manifest 的 `value_type` 仍写 `text-fact`。这种标签与内容不一致会使下游 AI、审稿人和分析脚本误判实验真正操纵了什么。

### 2.3 KB 能被原位覆盖，build hash 又不覆盖内容

日志显示 SQuAD/vocalbench 曾用 `value_spec=gold` 构建，随后又用 `text` / `question` 原位重建。旧 KB 没有不可变归档。

`kb_schema.py:163-166` 的 `build_hash` 只哈希：

`dataset|revision|key_modality|value_type|embedder|build_seed|n_entries`

它不包含 `keys.npy`、`values.jsonl`、input item IDs 或生成代码 commit。因此 SQuAD value 内容发生改变后，hash 仍可保持 `7b6ee5af64fa723b`。`kb_build.py` 又会直接覆盖 source 目录内的 index、values 和 manifest。

**裁决：** 当前 build hash 不是 content hash，也不能承担 chain-of-custody。任何基于现有 KB 的 Phase-A 结果都无法仅凭该 hash 证明自己用了哪一版内容。

**强制修复：** Phase-A 保持阻断；先建立真正 corpus-side source、content-addressed source version、inputs/values/keys SHA-256、refuse-overwrite、old-version archive 和 source/eval disjoint proof。`squtr` primary 还必须先实现 native qrels retrieval metric，而不是 `score=None` 的 generative placeholder。

---

## 3. P0-2：locked TEST 已失去严格 holdout 资格

### 3.1 测试 ID 明文提交，访问控制只是 honor system

`projects/speech-mllm-training-free-rl/_repro/LOCKED_HOLDOUT/*.json` 直接包含 `test_ids`。任何有仓库读取权限的人或 AI 都可以无痕读取；Git 不能记录“谁看过文件”。ACCESS_LOG 不能证明未访问。

更具体地：

- `locked_rerun_cells.py` 会加载整个 manifest，并访问 `test_ids` 字段求长度；
- ACCESS_LOG 却写 `test_ids NOT read (only len counts via census)`，这是字面自相矛盾；
- commit `b4707fe` 声称独立复算 SQuAD overlap 0.60，这必然使用了 test membership，但没有相应 access-log 条目；
- 本次外部审计也能直接读到这些 ID，这恰好证明所谓单消费者隔离并不存在。

### 3.2 新 seed 不等于新证据

65 个 test manifests 中：

- 64/65 与旧 exposed test IDs 有非零重叠；
- 总重叠 `741 / 6614 = 11.20%`；
- 7 个数据集 overlap ≥ 50%；最高达 89.47%、80.85%、65.45%、60%；
- `squtr` overlap 为 25%；
- 只有 23/65 是真正 group-disjoint，42/65 是明确标注的 item-level fallback。

团队保留 overlap 字段是正面的透明行为，因此这里更像对 holdout 概念理解错误，而非已经证明的隐瞒。但“fresh seed”“fresh manifest”不能使已看过、已打分、可能影响过设计的 items 恢复为 untouched evidence。

Dwork 等人的 adaptive data analysis 工作强调，分析流程在看过结果后会适应数据，传统有效性依赖于先固定 procedure；holdout 的价值来自隔离，而不是文件名叫 locked（[Science 2015](https://pubmed.ncbi.nlm.nih.gov/26250683/)，[NeurIPS 2015](https://proceedings.neurips.cc/paper/2015/file/bad5f33780c42f2588878a9d07405083-Paper.pdf)）。

**裁决：** 当前 TEST 可被称为“新冻结的混合测试清单”，不能称 untouched、blinded、single-consumer 或 independent confirmatory holdout。

**强制修复：** 等所有模型、指标、controls、SESOI、analysis code 和 winner protocol 冻结后，由独立 custodian 在仓库外重新抽取 test；仓库只存 salted commitment/hash 和统计量，不存明文 ID。现有 test 永久降级为 exposed DEV-like set，不得重新包装。

---

## 4. P0-3：ASR 的数值可复算，但 multiplicity 叙事被缩窄

### 4.1 成立的事实

从三个 ASR v2 工件的逐 utterance S/D/I/N 可精确重建 corpus WER 与 selector×N 点估计。noise1/noise2 使用同一 96 utterance cohort，但 greedy 只 43/96 相同，完整 candidate pool 只 12/96 相同，说明 noise2 不是整批缓存复用。缓存 bug 在采集前被发现并留下记录，这是支持诚信修复的证据。

在固定 `N=8`、仅四个 deployable selectors 的家族内，团队的数值可复算：

| 条件 | logprob@8 raw p | Holm4 |
|---|---:|---:|
| noise1 | .037 | .148 |
| noise2 | .005 | .015 |

### 4.2 未成立的“family-wise 已解决”

实际 discovery grid 查看了 `4 deployable selectors × 4 N = 16` 个 corpus-WER 比较/condition。按同一 bootstrap p 值和 Holm step-down 重新校正：

| 条件 | logprob@8 raw p | Holm16 |
|---|---:|---:|
| clean | .000 | .000 |
| noise1 | .037 | **.592** |
| noise2 | .005 | **.075** |

若把 clean/noise1/noise2 的 48 个比较视为一个 discovery family，noise1/noise2 的 adjusted p 分别约为 1.0 和 .21。

Holm 方法对一个明确列出的 fixed family 控制 FWER；它不会替研究者决定哪些已经看过的 hypotheses 可以事后移出 family。Holm 原始方法处理的是一组被检验的 hypotheses，而非仅保留看起来最有希望的子集（见 [Holm 1979 原文索引](https://www.scienceopen.com/book?vid=2288c405-e825-4f16-9e92-97d5c305afbf)）。

noise2 在第一轮后才采集，因此可把 `logprob@8` 视为预先选定 endpoint；但它仍使用同一 96 条 utterances，只变化噪声 realization，不是独立 dataset replication。合法表述应为：

> 在同一 cohort 的第二噪声敏感性分析中，预先选定的 logprob@8 方向一致；对固定 N=8 的四 selector 家族，noise2 通过 Holm，而完整 discovery grid 未通过。该证据仍为 Stage-1 directional，不是独立复现或 deployable win。

**裁决：** “evidence real”“Holm family-wise survives”若无 family 定义就是过度升级；当前尚不能证明团队为显著性故意缩小 family，但这是 formal integrity review 的合理关注点。

---

## 5. P0-4：locked-DEV 确实运行了，但“65/65 零失败/已验证”不成立

机械核验结果：

- 65/65 JSON 存在；共 4,439 rows；item IDs 与 dev manifests 一致；无 test ID 混入；aggregate 基本可复算。
- 但只有 3,929 条 scored，510 条 score=None；有 24 个 item-level HTTPError；4 个 cells 的 aggregate mean 为 null。
- 65/65 `git_dirty=true`。
- 65/65 缺 `manifest_hash`、`dataset_revision`、`engine_build_id`；也缺足以锁定模型的 SHA-256。
- 15 个 checkpoint-recovered cells 没有形成可独立审计的 clean-run provenance 包。

因此，“65/65”只能表示 65 个 cell 都产生了一个输出文件、cell-level driver 没有整体退出，不能无修饰地写“零失败”“全链通过”“publication-grade verified”。

此外，primary `squtr` 仍是 0/40 scored；现有 baseline 明确将它视作 diagnostic-only。这与 Proposal-R 需要的 end-to-end primary metric 直接冲突。

**强制修复：** 所有 Phase-A load-bearing code 必须先提交到 clean commit；每个 artifact 必须记录 code SHA + dirty=false、model/runtime hash、dataset revision、manifest hash、KB content hash、input/output hashes、完整错误数与 scoreless 口径。clean checkout 重新跑 G2-L3 reference config 与 controls 后，DEV 才能作为 exploratory map。

---

## 6. P0-5：unsigned DRAFT、协调者默认值与未完成 G2 不能组成 preregistration

`wiki/2026-07-11-proposal-R-prereg-draft.md` 明确写着：

- `DRAFT — owner signature required`；
- Phase-A 140-cell 与 Phase-B blocked；
- owner sign-off checklist 仍未勾选；
- primary metric、power、locked params、runtime control gate 均要求预先决策。

但 Decision Log 后续由协调者把推荐默认值当成冻结值并放行 Phase-A DEV。DEV 探索本身不是禁止行为；问题在于**不能把可否决的协调者默认值反称为 owner-signed preregistration**。

OSF 对 preregistration 的核心定义是：在 data collection/analysis 开始前，保存 time-stamped、read-only 的研究计划；unsigned、仍可改写的 DRAFT 不是这一含义上的注册（[OSF registrations guidance](https://help.osf.io/article/330-welcome-to-registrations)）。

同时，W1 的 `scripts/knowledge/kb_embed.py` 仍有未提交的 load-bearing 修复，涉及 16 kHz resampling、llama `/embeddings` payload 与 CLAP API；首轮 CPU build 是 41 ok / 7 fail，四个 sense arms blocked，G2-L3 未完成。

**裁决：** Phase-A 可在明确标注 `exploratory engineering diagnostic` 的前提下继续准备，但本轮不能称 preregistered、frozen、G2-green 或 Step-1 complete。

---

## 7. 其他重大统计与传播漏洞

### 7.1 MInDS：大 card treatment 成立，但不是“examples 的已隔离因果效应”

成立部分：126 card pool 与 437 eval row 分离；去掉 12 个 exact-text overlap 后，cards−naive 仍约 `+.2463`，主效应不是由这 12 条直接重复驱动。三个 support draws 的 card gain 约 `+.236` 至 `+.254`。

未成立部分：

- 三个 support draws 共用同一批 437 eval rows；CI 只 bootstrap eval item，未重采 support pool/draw，不能覆盖 support-selection variance。
- card factor 同时加入 label、schema、boundary note 和 positive examples；它隔离的是 composite card treatment，不是 examples 单一机制。
- `minds14_v2_multiplicity.json` 的 7 行包含两对完全重复 comparison，实际只有 5 个 unique contrasts。“7/7”会制造证据数量感。
- multiplicity JSON 没有 committed generator、reproduce command、input hashes 或 code commit。

允许主张：`composite candidate-card representation strongly improves retrieval classification in this split`。禁止主张：`examples alone causally explain the effect`、`7 independent findings`、`zero-shot RL gain`。

### 7.2 CREMA：4 fold seeds 是 split robustness，不是 4 次 replication

四个 fold seeds 重复使用同一 7,442 clips、91 speakers、同一模型与同一 pooling pair；预测在 seeds 间约 79%–82% 相同。效应 `+2.7` 至 `+4.3pp` 可复算，说明方向对 fold assignment 较稳定。

但 cluster bootstrap 只重采已经生成的 OOF predictions，没有在每个 replicate 中重切 outer/inner folds、重做 layer selection 和训练，因此没有传播 selection/training variance。SESOI=.05 也是在先前同一数据结果已知后才“分析前固定”，不能称独立 preregistered margin。四个 seeds 中有一个 CI 上界超过 .05，故“practically equivalent to no effect”也不对所有 folds 稳健。

允许主张：`same-corpus grouped-CV conditional effect is small and split-direction-stable`。禁止主张：`4 independent replications`、`external generalization`、`speaker-free/disentangled`。

### 7.3 Lean coverage theorem 没有关闭理论—实现鸿沟

`Coverage.lean` 对定义好的实函数 `missProb(p,N)=(1-p)^N` 证明幂/乘积恒等、随 N 单调及 sample-complexity bound。这是正确而有用的数学模型，但它没有形式化：

- Python `best_of_n`/argmax、tie handling 或 WER 实现；
- candidate generator 的概率空间；
- seeded PRNG draws 的独立性与同分布性；
- Python/Lean conformance；
- 实际 selector 的 convergence；
- unconstrained failure 与 constrained convergence。

`missProb_eq_prod` 证明常数幂等于有限乘积，不是对工程随机过程“独立性”的证明。`coverage_bridge.py` 双方都算 `p=1/4,N=3` 得到 27/64，只是数值 parity vector，不是实现等价证明。

因此可以称“i.i.d. Bernoulli oracle-coverage model 的第一组 axiom-clean lemmas”，不能称“actual implemented operator theorem”或“selector convergence proof”。这也与 ledger 仍写 `operator-linked theorems=0`、paper 写 count=0 的状态互相冲突。

### 7.4 claim ledger、paper 与 source sections 仍不一致

- authoritative ledger 仍将 `C-PHASEA` 标为 invalid，无 successor，但 Decision Log 已放行 DEV。
- `C-THEORY` 仍写 operator-linked count=0，而 Decision Log 声称 FIRST operator-linked theorem。
- W4 ledger 使用 history rewrite 前、当前分支/remote 不可达的 `9ead4d4` / `d04bb89`；可达 commit 是 `56b8a9c` / `40d34c2`。
- verifier IDs `a2bf4e5`、`a5e4997`、`ad9b3d7`、`abef730` 在仓库中不可追踪。
- `C-ASR-V2` artifact 使用字面 brace 路径，普通机器消费者无法直接解析，ledger 又没有 artifact SHA-256。
- paper 仍写 `all results independently re-verified`；内部 Opus/Codex agents 不是独立团队。
- paper/README/section sources 仍传播旧 CREMA negative、旧 speaker “near chance”与旧 ASR headline；只改 assembled `main.tex` 也会在再次 assemble 时发生回退。
- 新 `Coverage.lean` 已加入后，paper 仍写 operator-linked theorem count=0。

论文目前仍有 quarantine banner，这是正确处理；在这些传播冲突清零前不得解禁。

### 7.5 evidence freeze 不是整改后完整 freeze

现有 freeze 能证明当时一批文件的 hash，但：

- `generated_at` 是用户手填标签，与文件实际写入/commit 时间不一致，不能作为取证时钟；
- 整改后新增的大量 W1/W4/KB artifacts 没有 post-remediation freeze；
- KB 的可变外部目录与内容 hash 不在有效 custody 中。

应把 `planned_label`、`observed_at_utc`、`commit_at_utc` 分开，且对 repo、external KB、raw artifacts、mlruns 生成同一审查批次的 Merkle/content manifest。

---

## 8. 欺诈风险矩阵

| 问题 | 已确认事实 | 当前分类 | 是否已证明故意 |
|---|---|---|---|
| 凭空编造数据 | 主要点估计可由 row-level artifacts 复算 | 未发现 fabrication | 否 |
| 篡改逐项结果 | 负结果、error、NULL、cache 事故仍保留 | 未发现直接 falsification | 否 |
| 删除不利结果 | length harm、MInDS regression、blocked arms 均可见 | 暂无证据 | 否 |
| 错误研究对象 | query/question 被标成 knowledge-passage | **严重对象错配/QRP** | 动机不明 |
| 多重检验 | family 缩为 Holm4@N8 | **选择性统计表述风险** | 动机不明 |
| 伪重复 | CREMA fold seeds、同 cohort noise draws 被近似写成 replication | **报告失实风险** | 动机不明 |
| holdout | IDs 明文提交、旧 test overlap、access log 不完备 | **假性 held-out 已确认** | 动机不明 |
| provenance | dirty artifacts、无 generator、不可达 commit、可变 KB hash | **严重 custody failure** | 动机不明 |
| 独立复现 | 内部 AI verifier 被称 independent | **不准确研究记录** | 动机不明 |
| 完成状态 | unsigned DRAFT/G2 open 却称 release/closeout | **状态夸大** | 动机不明 |

### 为什么目前不直接认定欺诈

以下证据反对“正在系统捏造”的强结论：

- ASR、CREMA、MInDS 主要数值可由逐项记录复算；
- W4 clean-provenance rerun 的科学结果与原 artifact 一致；
- ASR repo artifact 与 E 盘副本 hash 一致；
- locked-DEV IDs 与 manifests 一致，未发现整份 payload 重复或 test ID 混入；
- 错误、NULL、负效应与 blocked arms 没有被统一清除；
- wav-cache 假复现是在正式收集前被发现、修复并写入记录；
- overlap 字段被保留而非删除。

这些证据支持“内部纠错是真实的”，但不能抵消前述设计和报告失效。

### 正式调查升级触发器

收到本报告后若出现任何一项，应由非项目成员的 research integrity officer/custodian 启动正式 inquiry：

1. 仍把 `squtr` query-KB 或 vocalbench question-KB 报成 external knowledge passage。
2. 仍把现有 test 称为 untouched、never-read、single-consumer 或 independent holdout。
3. 仍把 Holm4@N8 报成完整 discovery grid 的 FWER correction。
4. 仍把四个 CREMA fold seeds 报成四次独立 replication。
5. 仍把 MInDS composite card treatment 写成 examples 单因素的已隔离因果效应。
6. 删除、覆盖或不披露旧 KB、24 errors、scoreless cells、blocked arms、overlap 或 harmful selectors。
7. 无法提供两个派生 JSON 的生成器，或 clean rerun 与已报摘要不一致且没有解释。
8. 用 dirty code 继续生成结论性 artifact，却不保存 exact diff/environment。
9. 在 test IDs/labels 已见后重画 split、改 primary metric、改 SESOI 或改 success rule，却仍称 preregistered。
10. 继续把内部 AI 验证写成独立人类/独立团队 reproduction。

---

## 9. 强制整改计划与验收证据

### Gate RI-0 — 立即冻结错误升级（现在）

**动作：** 保持 paper quarantine；禁止 Phase-B/现有 TEST；Phase-A 只能叫 DEV exploratory engineering；保存当前 repo、外部 KB、logs、artifacts 的只读副本。

**验收：** owner 签署一条不可变 decision record，明确 `NO CLOSEOUT / NO CONFIRMATORY CLAIM / NO CURRENT TEST`；指定一个未参与设计与运行的 integrity custodian。

### Gate RI-1 — 重建证据链（24–72 小时）

**动作：**

1. 为 ASR noise replication、MInDS multiplicity、CREMA fold seeds 提交唯一可执行 generator。
2. generator 原子地产生 raw rows + summary；summary 只从 raw rows 生成。
3. 每个 artifact 记录 input SHA-256、code commit、dirty flag、model/runtime hash、dataset revision、manifest hash、command、environment lock。
4. external KB 改为 immutable versioned source；build hash 覆盖 keys、values、input IDs、build config 和 code SHA。
5. 禁止原位覆盖；修复版产生新 source ID，旧版进入 INVALID ledger 而不是消失。

**验收：** clean checkout 一键重建摘要，byte-identical 或数值容差由 prereg 预定义；第三方能在不询问作者的情况下重跑。

### Gate RI-2 — 修复真正的研究对象（72 小时–1 周）

**动作：**

- `squtr` 使用 qrels corpus documents 作为 VALUE；query audio 只作为 query side。
- `vocalbench-knowledge` 明确找到 external evidence/fact；若数据集没有 passage，则退出 knowledge-RAG primary，不得用 question 伪装。
- `SQuAD/heysquad` 建立 answer-scrubbed context、source/eval group-disjoint、gold-overlap audit。
- 对每个 source 输出 20 条人工可读 sample、value-semantic unit test、oracle retrieval sanity check、random retrieval negative control。

**验收：** custodian 随机抽 50 个 values，确认它们是 evidence passages 而非 query/answer leakage；native qrels R@k/nDCG 可计算；`squtr` 不再 score=None。

### Gate RI-3 — 重新完成 preregistration

owner 必须逐项签署：

- 单一 primary question；
- dataset 与 primary metric；
- exact treatment/control arms；
- selector、N、condition、metric 的完整 multiplicity family；
- SESOI 与 equivalence rule；
- power/cluster-count decision；
- missing/error/scoreless policy；
- stop/pivot/kill rules；
- Phase-A/Phase-B 边界；
- independent custodian 与 TEST access protocol。

**验收：** time-stamped read-only registration 在任何新 data analysis 前完成；之后所有偏离进入 append-only deviation log。

### Gate RI-4 — 重新旋转 confirmatory TEST

**动作：** 在所有设计冻结后，由 custodian 从未用于旧 test/dev/diagnostic 的 groups/items 中抽取；如果数据集无法提供未暴露样本，则换 dataset 或外部 corpus，不得假装还有 holdout。

**验收：** repo 只存 commitment；test IDs/labels 不对开发团队开放；单次执行产生 signed report；读取即 burn，失败也不得重抽。

### Gate RI-5 — clean G2-L3 与 exploratory Phase-A

**动作：** 提交 `kb_embed.py` 修复；clean checkout 跑 primary、replication 与全部 mechanism controls；逐 cell 报 errors/NULL/shortfall，不用“65/65”掩盖 item failure。

**验收：** `git_dirty=false`；primary squtr 得到有效 native metric；KB semantics correct；所有 controls 使用同一 frozen code/config；Phase-A 结果只用于选择 Phase-B protocol，不升级 evidence grade。

### Gate RI-6 — 独立复算与传播一致性

**动作：** 未参与设计的人从 clean checkout 独立复算 ASR、MInDS、CREMA 和 Phase-A；同步 ledger、paper source sections、assembled main、README、status wiki。

**验收：** 每个 headline claim 只有一个 claim ID，能追到 artifact hash、generator、input hash 和 verifier report；禁止 `independent` 一词，除非 verifier 真正独立于设计/运行团队。

---

## 10. 下一轮 proposal：不仅挑错，还要回答什么值得研究

Stage 1 的目标是选对问题，不是急着把每个小跑都包装成结果。下面六个方向应成为 owner discussion 的候选 proposal；它们彼此竞争，不能全部自动进入 Stage 2。

### Proposal A — 语音直接检索是否真的优于 own-ASR cascade？

**问题：** 当 KB 是真实 evidence corpus 时，audio-direct embedding 相比 frozen model 自己的 ASR→text retrieval，是否在噪声/口音/语言转换下提供可重复增益？

**关键 controls：** gold transcript upper bound、own-ASR cascade、audio-direct、random retrieval、oracle qrels retrieval、no retrieval、scrubbed vs unscrubbed KB。

**检查点：** retrieval R@k/nDCG 与 end-to-end answer score 同时报；若 oracle retrieval 不提升 answer score，则瓶颈不在 retrieval；若 audio-direct 不优于 own-ASR，旗舰“omni embedding activation”方向应降级。

### Proposal B — deployable selector 的增益是否跨 cohort/model/corpus？

**问题：** logprob-confidence 的小幅 ASR gain 是真正可部署规律，还是 Qwen3-Omni×LibriSpeech×特定 runtime 的偶然条件效应？

**设计：** 预先固定 `N=8 logprob` 单 endpoint；新 utterance groups；至少另一 speech corpus、另一语言/口音、另一 runtime/backbone；把 oracle 只当 headroom。

**检查点：** paired cluster CI、SESOI、calibration、error-type S/D/I、pool collapse rate、compute/latency cost。若只在 clean 或单模型成立，不得称通用 TFRL。

### Proposal C — reward/proxy misalignment 与 over-optimization budget

**问题：** 随 N 增大，logprob/MBR/length 等 proxy 何时开始偏离真实 WER/semantic reward？

**设计：** 预注册 N curve、proxy-vs-oracle rank correlation、best-of-N collapse、harm rate；加入 N* budget cap 与 stop rule。

**价值：** 这比只报 oracle headroom 更接近“training-free optimization”真正的风险和理论约束，也能连接 over-optimization 与 reward hacking 文献。

### Proposal D — MInDS card effect 的机制拆解

**问题：** 大效应来自 label semantics、schema、boundary instruction、positive examples，还是 encoder 对固定模板的表面匹配？

**因子：** label-only；schema/no-example；schema+boundary/no-example；examples-only；full cards；paraphrased templates；speaker/template/session-disjoint split。

**检查点：** support draw 作为上层随机因素做 hierarchical bootstrap；跨模板/跨语言验证；若 paraphrase 后效应崩塌，则应解释为 template retrieval，不是 latent task knowledge activation。

### Proposal E — paralinguistic readout 的小效应是否跨 corpus？

**问题：** CREMA 的 +2.7–4.3pp 是同 corpus selection bias，还是 frozen content embedding 中可利用的有限情感信息？

**设计：** 方法选择只在 discovery corpus；锁定 pooling/layer 后在新 emotion corpus 做 external test；speaker/session fully disjoint；报告 speaker leakage、emotion accuracy、calibration、domain shift。

**检查点：** 不把 fold seeds 当 replication；SESOI 在外部数据前冻结；如跨 corpus 不成立，结论应是 corpus-specific probe。

### Proposal F — 真正 operator-linked 的约束与收敛理论

**问题：** 对与代码同一对象的 selector/update rule，何种 KL trust region、N* cap、reward-error bound、slow-drift 条件能保证 constrained process 收敛，而 unconstrained process 为什么失败？

**最低理论门槛：**

1. Lean 中定义 candidate distribution、selector、ties、iteration/operator；
2. 证明工程 rule 的 correctness；
3. 构造 unconstrained non-convergence/counterexample；
4. 加入明确约束并证明 convergence/rate；
5. 建立 executable conformance tests，而不是只让 Python/Lean 计算同一手工分数。

Coverage lemma 可以保留为前置基础，但不能代替这个 proposal。

---

## 11. 给后续 AI 审查者的机器可执行规则

后续 AI 不得只读取 Decision Log 的“PASS/完成”字样，必须执行以下判定：

```yaml
review_decision:
  step1_closeout: REJECT
  stop_the_line: true
  dev_engineering_allowed: true
  confirmatory_test_allowed: false
  paper_release_allowed: false
  ffps_finding:
    fabrication: NOT_FOUND
    falsification: NOT_ESTABLISHED
    plagiarism: OUT_OF_SCOPE_NO_SIGNAL
    intent: UNDETERMINED
  confirmed_risks:
    - wrong_experimental_object
    - pseudo_locked_holdout
    - post_hoc_multiplicity_family_narrowing
    - dirty_unreproducible_artifacts
    - mutable_kb_without_content_hash
    - unsigned_preregistration
    - pseudo_replication
    - internal_ai_mislabeled_independent
    - cross_document_claim_drift
  required_before_reopen:
    - immutable_content_addressed_kb
    - real_corpus_side_squtr
    - frozen_native_primary_metric
    - clean_g2_l3
    - owner_signed_read_only_preregistration
    - externally_custodied_fresh_holdout
    - committed_atomic_analysis_generators
    - independent_clean_checkout_reproduction
```

若团队回复只提供新的 summary markdown、commit message 或 AI “PASS”，而不提供上述验收物，状态不得升级。

---

## 12. 最终结论

这一轮比上一轮诚实，也更接近一个可审查的研究工程：团队承认并保留了多项错误，主要数字能够从逐项工件复算，未出现足以直接认定 fabricated data 的证据。

但严格结论仍然是：

> **这是一次有价值的内部整改，不是 Step-1 科学收官。当前已经确认错误研究对象、失效的 holdout、缩窄的 multiplicity family、dirty provenance、未签 preregistration、伪重复和跨文档漂移。没有直接证据证明学术欺诈，但已经有充分理由维持停线、要求独立研究诚信核查，并禁止任何 confirmatory/independent/untouched/knowledge-retrieval 的升级表述。**

真正的诚信测试不在于团队是否曾犯错，而在于：收到这些可复核事实后，是否会把错误对象重建、把现有 test 作废、把统计家族完整公开、保存失败与旧版本，并让独立 custodian 在 clean、冻结、不可适应的流程中重新验证。
