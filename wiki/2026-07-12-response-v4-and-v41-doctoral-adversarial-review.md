# 2026-07-12 — 对 v4 审查回复与 v4.1 的博导级对抗复审

> **直接审查对象**：`wiki/2026-07-12-response-v4-to-adversarial-integrity-review.md`。  
> **必要连带对象**：该回复指定的 `wiki/2026-07-12-research-proposal-v41-external-review.md`、`docs/checks/v41-conformance-report.md`、W1 commit `48502ca`（票 #37）、当前外部 KB 工件、claim ledger、Project Thesis、Per-Work-Status、Decision Log 与 G0 记录。  
> **审查日期**：2026-07-12，Asia/Singapore。  
> **身份**：严格期刊审稿人 + 博士生导师 + research-integrity hostile reviewer。  
> **边界**：只读取证，只新增本报告；没有修改团队回复、v4.1、代码、账本、实验工件或状态页。  
> **证据标签**：`FACT` 为文件/代码/工件/实跑直接证据；`INFERENCE` 为审稿判断；`UNKNOWN` 为当前无法证实。

---

## 0. 总裁决

### 0.1 对回复态度与整改诚意的裁决

**ACCEPT WITH SERIOUS RESERVATIONS。**

这封回复比 v4 更诚实，也不是纯粹的“同意审稿人式表演”。以下整改有真实代码、工件或文本证据：

- `C-MINDS-V2` 已改回 directional/composite，`C-KEEP` 已改 unverified，`C-T7` 已退出正向动机；
- `SQuAD-zh=0.925` 的数据集身份错配已更正；
- K2 中文 agreement 已从 word-WER 改成 CER，并增加中文 minimal-pair tests；
- GLAP 与 Nemotron 的 cross-modal 状态均已从 `supported` 降为 `pending-live-verification`；
- 旧 squtr query-valued sources 已在本机归档；
- pseudo-question builder 已限制为 corpus records/source；
- 新 build manifest 增加 provenance 字段，旧 KB 增加 sidecar；
- W1 #37 已提交，当前 W1 worktree clean；
- v4.1 明确仍待外审与 owner 签字，没有宣称已进入 Stage 2。

这些事实显著降低“团队收到批评后继续掩盖”的怀疑。

但是，回复把四件不同的事混成了“已处置”：

1. **承认问题**；
2. **在 proposal 中写下未来修复**；
3. **代码机械实现某个 guard**；
4. **科学与确认性治理真正闭合**。

本轮复核证明，许多条目只达到 1–3，没有达到 4。

### 0.2 对 v4.1 的裁决

**MAJOR RECONSTRUCTION / REJECT FOR STAGE 2。**

v4.1 相比 v4 有实质进步，但仍有五个可以单独阻止 Stage 2 的 FUNDAMENTAL：

1. 固定公开 seed 与可预测 confirmatory IDs 仍被保留；“披露局限”不能把它变成确认性 holdout；
2. “一版一轮 + per-version α”没有控制跨版本反复试验的 program-level Type-I error；
3. squtr 310-doc mini-corpus 由 test qrels 的全部正例文档 + 200 distractors 构建，违反“KB 与评估标注独立构建”；
4. selector 的“可验证 reward”实际是 self-consistency、同权重异 prompt verifier 和 verbal confidence 等 proxy，未验证 correctness，也未定义真效用与代理奖励的区分；
5. S3 与 selector 对照仍存在严重预算混杂：5/6-call triggered 与 2-call always 比效果；K-path selector 又声称与 K=1 single-RDU“严格等预算”。

### 0.3 对正在处理的 M1/#37 的裁决

**PARTIAL PASS，M1 NOT GREEN。**

代码修复包是真实的，但 M1 仍未满足 v4.1 自己的 entry criteria：

- real cross-modal live smoke 未执行；
- §4 rewrite–retrieve–deliver–answer K-trajectory selector harness 尚未实现；
- deterministic draw 不强制 group-disjoint，也不强制完整 exposure exclusions；
- squtr 仍允许在 corpus source 缺失时回落到旧 4-field source name；
- 标准 `pytest` 全仓收集失败；
- external KB 的旧 provenance sidecar 含 guess/assumption，不是 build-time provenance；
- no confirmatory/eligibility manifests 或 holdout-supply proof 已交付。

### 0.4 研究诚信裁决

**NO FFP FINDING；QRP RISK REMAINS HIGH；INDEPENDENT OVERSIGHT REQUIRED。**

当前没有优势证据证明 fabrication、falsification 或 plagiarism。团队保存旧失败、承认 QRP、归档错误 KB、公开测试失败边界，是反对 FFP 定罪的重要证据。

但仍有新的 QRP/治理风险：

- 用“independent conformance checker”称呼同一 AI 工作流内、还能直接改信件的检查者；
- 承诺 checker code/rule manifest/output JSON/environment，实际只提交一份人工式 Markdown；
- conformance report 宣告 `RELEASE-READY`，却漏掉多处直接矛盾；
- 把“零学术欺诈”写成抽样治理标准，但它不是可操作、可验证的防偏差机制；
- 将事实错误责任归到“定稿协调 AI”，容易稀释作者与 owner 的最终责任。

上述问题不等于欺诈，但不能再由同一 team/AI 自证关闭。

---

## 1. 多轮 hostile review 的结论

### Round A — 回复是否真的逐项关闭上一轮意见

结论：**四处证据勘误基本关闭；custody、统计跨版本控制、科学对照、理论对象只部分关闭。** 回复中的 `37 CONFIRMED / 5 PARTIAL / 0 REFUTED` 只能说明团队接受了审查，不能证明 42 项已经闭合。

### Round B — v4.1 内部逻辑反证

发现：

- “业务效果为裁判”与“10% 只是惯例科学阈值，不称 business effect”冲突；
- “不可预测 custody 是签字门”与“固定公开 seed、拒绝 unpredictability machinery”冲突；
- “single RDU K=1”与“所有对照严格匹配同一 K 预算”冲突；
- “每个 dataset×endpoint×contrast 一个原子”与 secondary family 只给 S1–S4 摘要、未展开 R@k/end-to-end 等多个 endpoint 冲突；
- “同一 R 符号”同时表示 proxy reward、task utility、selector performance 和 oracle utility，理论对象未定义清楚。

### Round C — 代码/工件反证

发现：

- #37 包含真实修复；
- deterministic draw 仍是 item-id 抽样，group key 不存在于 manifest/算法；
- `exclusion_lists` 是 optional caller input，confirmatory 模式不 fail-closed；
- 固定 seed `721003303` 与 pool 一公开，confirmatory IDs 在 arm freeze 前完全可计算；
- `force_supersede` 仍允许更换 pool/exclusions 后重抽；local JSONL 不是不可篡改日志；
- squtr corpus 由 qrels 决定正例集合；`CLEAN` audit 实际 `n_golds=0`；
- `run_mock.source_name_for` 在新 corpus 不存在时仍回落到旧错误对象名字；
- full pytest 仍红。

### Round D — 文献与理论反证

发现：

- self-consistency/verbal confidence 是有用 uncertainty proxy，但文献同时明确存在 self-consistent errors、overconfidence 与 within-question calibration 特殊性；不能直接叫 verifiable correctness reward；
- Best-of-N 在 imperfect reward 下会随 N 增大发生 reward hacking，有限预算本身不等于收敛；
- 多版本确认性试验属于 online/sequential multiple testing，必须控制 program-level error；每版重新注册不会重置 Type-I error；
- WavRAG、VoxRAG、PlanRAG-Audio 已把 audio-RAG/system organization 的 novelty 空间压得很窄，v4.1 的真正创新必须由 selector 的净增益和严格因果分解支撑。

### Round E — 研究诚信 hostile meta-review

发现：没有看到删除负结果或伪造运行；但“self-certification inflation”仍存在——用 `independent`、`RELEASE-READY`、`zero fraud` 和 `全部处置` 等标签，超过实际工件所能支持的程度。

---

## 2. 回复逐项裁决矩阵

| 回复主张/处置 | 裁决 | 证据与原因 |
|---|---:|---|
| 全盘接受 REJECT/NO-GO | **ACCEPT** | v4.1 与状态页都明确 Stage 2 关闭、签字待定。 |
| E1–E4 四处勘误 | **ACCEPT** | ledger 标签、C-KEEP、C-T7、SQuAD-zh 均已实质更正。 |
| claim-ledger 机器门已建立 | **PARTIAL/REJECT AS DELIVERED** | 只有 Markdown conformance report；未找到 checker code、独立 rule manifest、output JSON 或 environment artifact。 |
| F-1 成本门已关闭 | **PARTIAL** | 不可能的 30% gate 已删除；但 S3 的效果比较仍被计算预算严重混杂。 |
| F-2 黑盒契约已关闭 | **PARTIAL ACCEPT** | core hidden state 已降诊断；独立 frozen embedder 是合理外挂。但 real audio→text cross-modal route 未 live verify，Nemotron 许可限制商业价值。 |
| F-3 已恢复真正 TFRL | **PARTIAL/REJECT** | 有 action/policy/selector 草案，但 reward 是未经正确性验证的 proxy；实现与 Lean 同对象尚不存在。更准确叫 reward-model-guided inference-time search target。 |
| F-4 身份漂移已关闭 | **ACCEPT WITH NOTE** | G0 确有 owner 裁定，canonical docs 已更新；此前问题更准确是传播失败。新 v4.1 七项签字仍全部待定。 |
| I-1 pseudo-question 对象修复 | **PARTIAL** | builder 入口更安全，旧源本机已归档；但 run_mock 仍可 fallback 到 legacy name，corpus 本身又是 qrels-conditioned。 |
| I-2 K2 CER | **ACCEPT** | 代码与中文 tests 已修。 |
| I-3 supported 降级 | **ACCEPT** | GLAP/Nemotron 均为 pending-live-verification；真实 live gate 脚本存在但未运行。 |
| I-4 modality×form×delivery 因子化 | **ACCEPT AS DESIGN** | 文案已正确降为 form-bridge hypothesis；尚未执行。 |
| I-5 禁 auto | **PARTIAL ACCEPT** | pseudo-question path 加了 hard error/escape hatch；全系统所有 fallback 仍需 inventory。 |
| I-6 tests 只支持 plumbing | **ACCEPT** | 回复表述正确；后续却又在 commit 中写 all suites green，入口定义不一致。 |
| I-7 clean checkout | **PARTIAL** | W1 当前 clean 且 #37 已提交；但标准 full pytest 红、real smoke 与 K-trajectory harness 缺失。 |
| I-8 baseline mismatch | **ACCEPT** | 0.85/0.925 已拆开。 |
| I-9 provenance 补全 | **PARTIAL** | 新 schema 增字段；旧 KB sidecar 明写 revision guess、normalization assumed、build-time SHA 缺失，不能升级为完整 provenance。 |
| S-1 m=7 原子族 | **PARTIAL/REJECT FOR PREREG** | primary 模板有 7 atoms，但 datasets/SESOI/α/no-harm margins/p-values 未定；secondary family 仍非原子展开。 |
| S-2 headline 限定 headroom-qualified | **METHOD ACCEPT / SCIENCE WEAK** | 限定诚实，但总体成为 responder-selected tasks；不可再泛化为知识依赖语音任务。 |
| S-3 SESOI 不移动 | **ACCEPT** | 15→10 fallback 已移出成功门。 |
| S-4 不称 business effect | **REJECT AS CONSISTENCY** | §9.3 这样写，但标题、§2.2 和多处仍写“业务效果”。 |
| S-5 不池化异质任务 | **ACCEPT AS DESIGN** | focus + replication/no-harm 方向正确；no-harm margin 尚未定义。 |
| S-6 一版一轮 | **PARTIAL** | 版本内清楚；跨版本重复检验没有 program-level alpha control。 |
| S-7 holdout supply gate | **PARTIAL** | supply 仍待证明；proposal 同时要求“不可预测 custody”又拒绝不可预测机制。 |
| C-1 responsiveness 四状态 | **ACCEPT AS DESIGN** | 构念命名已纠正；重复采样次数/estimand 仍待冻结。 |
| C-2 taxonomy 非恒等式 | **ACCEPT** | 机械加法已撤。 |
| C-3 equal-content A/B | **ACCEPT AS DESIGN** | 正确隔离 schema，但需要 tokenization/position equality audit。 |
| C-4 理论必要条件 | **REJECT AS FORMAL CLAIM** | 当前式子不是一般必要条件，变量分母/条件事件不同，measurement slots 也不对应。 |
| C-5 零核心结构措辞 | **ACCEPT** | 已修。 |
| C-6 三构念拆分 | **ACCEPT AS DESIGN** | QA/schema/entity 不再冒充共同机制。 |
| 文献最近邻补齐 | **PARTIAL ACCEPT** | 六个关键近邻已入矩阵；novelty 仍需更精确 comparison，不可只写“对方缺什么”。 |
| E-3 custody 作为已披露局限 | **REJECT FOR CONFIRMATORY USE** | 披露偏差不会消除偏差；若坚持该路线，只能把结果降为 open/exploratory reproduction。 |
| E-4 chronology | **ACCEPT** | v4.1/回复日期已与实际日期一致；仍需真实 created/frozen/signed timestamps。 |
| QRP 由独立监督关闭 | **NOT YET DELIVERED** | 当前 conformance checker 仍是内部 AI 检查，不满足独立诚信监督。 |

---

## 3. 五个仍然成立的 FUNDAMENTAL

### F′-1. Owner 可以拒绝 custodian，但不能靠裁决改变统计事实

**FACT**：回复明确承认固定 seed 不提供 blindness/unpredictability，却仍选择它作为 confirmatory 抽样方案；v4.1 §9.5 同时要求签字前证明“不可预测 custody”。

这是直接自相矛盾。固定 seed 常量与候选 pool 一公开，任何人无需打开 manifest 就能重算 confirmatory IDs。所谓“manifest commit before arm selection”不能阻止开发者：

- 在提交 manifest 前计算 IDs；
- 根据已知 IDs 选择 prompt、arm、KB 或 dataset；
- 尝试不同 pool definition/exclusion set；
- 只提交最终看起来合理的一套输入。

W1 `deterministic_draw.py` 的注释称固定 seed 与旧方案“equally tamper-evident”，这个说法不成立。确定性提供 **replayability**，不提供 **selection blindness**。

[Dwork et al.](https://proceedings.neurips.cc/paper_files/paper/2015/hash/bad5f33780c42f2588878a9d07405083-Abstract.html) 明确指出适应性重复使用/响应 holdout 会使其过拟合；需要限制 analyst 对 holdout 的信息通道，而不是只让抽样可复算。

**博导裁决**：

- 若 owner 坚持不用独立 custodian/benchmark server/secret seed，则必须把该层称为 **public deterministic evaluation**，不是 blinded/fresh confirmatory；
- 可以发表，但证据等级应降为 exploratory/transparent reproduction；
- 若论文需要 confirmatory claim，最轻量方案不是“复杂工程”，而是第三方一次性评分或 benchmark server；这比五轮自审成本更低。

### F′-2. “per-version α”没有解决反复试到成功

v4.1 写“一版本一轮；失败后新注册版本；每版 α 在注册时声明”。这只解决版本内透明度，没有控制整个研究计划反复提出相似系统并测试同一 headline 的错误率。

若每个版本都用 α=.05、试验近似独立，五个版本至少一个假阳性的概率是：

\[
1-(1-.05)^5 \approx 22.6\%.
\]

版本数继续增加时趋近 1。重新注册不会让统计历史清零。[Online FWER](https://pubmed.ncbi.nlm.nih.gov/33413033/) 的研究对象正是未知未来长度的连续假设流，要求对整条序列控制错误率。

**必须选择一种**：

1. program-level alpha spending/online FWER；
2. 一个 final confirmatory version，此前所有版本均为 development；
3. 每次成功后必须在全新外部 dataset/core 上独立复制，第一成功版本只算 discovery；
4. 放弃显著性成功门，做完整 cumulative evidence/likelihood/Bayesian updating，并不宣称单次确认。

当前“旧轮永久保留”是透明性要求，不是 Type-I control。

### F′-3. squtr mini-corpus 使用 test qrels 构建，违背 KB 独立性

这是本轮最严重的新实现发现。

**FACT**：官方 fiqa corpus 有 57,638 文档。当前 `build_squtr_corpus_source`：

1. 先选择 test queries；
2. 从 test qrels 取出所有相关 doc IDs；
3. 把这些 gold docs 全部放入 KB；
4. 只再采样 200 个 distractors。

当前工件为 310 docs，其中 110 是 qrels-positive docs。正例文档占比约：

\[
110/310 \approx 35.5\%.
\]

若在完整 corpus 中，同样 110 个正例只占约：

\[
110/57638 \approx 0.19\%.
\]

也就是候选池的正例密度被提高约 186 倍。这个 mini-corpus 可以作为明确标注的 controlled retrieval smoke，却不能作为“KB 与评估标注独立构建”的 confirmatory corpus，更不能承担 squtr 主场的原生检索难度。

**FACT**：manifest `pool_split="test"`、note 写 `n_gold_docs=110`；leakage audit 却是 `n_golds=0` 并给 `CLEAN`。这是一个**真空审计通过**：没有检查任何 gold string，也没有检查 qrels-dependent corpus selection。

这里还暴露了概念混乱：在正规 open-corpus QA/IR 中，相关文档包含答案是任务定义，不应把答案从合法证据中 scrub 掉；真正的泄漏是**用 test qrels/answers 决定 corpus 构成、索引、prompt 或候选范围**。

**必须修复**：

- confirmatory retrieval 使用官方完整 57,638-doc corpus；或用与 qrels 完全无关的 query-independent 固定 subset；
- qrels 只用于评分，不得用于构建 candidate corpus；
- 把 `CLEAN` 拆成至少：`object_correct`、`query_independent_corpus`、`label_independent_build`、`answer_presence_expected`、`provenance_complete`；
- `n_golds=0` 不得输出 `CLEAN`，应输出 `NOT_EVALUATED`；
- 当前 310-doc 工件永久标 `qrels-conditioned controlled mini-corpus`，不得用于 headline。

### F′-4. proxy reward 被误称为 verifiable reward

v4.1 §4 的三种 reward：

- candidate answers 的 self-consistency；
- 同一权重、不同 system prompt 的 verifier agreement；
- 模型 verbalized confidence。

它们都不读取 gold，也不执行确定性 correctness checker。它们是 **label-free proxy reward / uncertainty signal**，不是通常 RLVR 语境中的 verifiable reward。RLVR 的典型 verifier 是数学 exact-answer、程序单测或规则验证；即使这种 verifier 也可能被 gaming，更不用说同模型自评。

[Too Consistent to Detect](https://aclanthology.org/2025.emnlp-main.238/) 证明错误可以跨随机采样保持稳定，而且多类 detector 对 self-consistent errors 明显困难。[CISC](https://aclanthology.org/2025.findings-acl.1030/) 确实表明 confidence-weighted consistency 可能有用，但同一论文也指出标准 calibration 对同题候选排序可能很差，最 calibrated 的方法甚至可能最不适合 within-question selection。[Best-of-N inference-time alignment](https://arxiv.org/abs/2503.21878) 进一步表明 imperfect reward 下扩大 N 会产生 reward hacking。

**必须改名并重新定义**：

- 真任务效用写作 \(U(\tau)\)；
- 部署 proxy 写作 \(\hat U(\tau)\)；
- oracle 选择 \(\arg\max U\)；
- deployable selector 选择 \(\arg\max \hat U\)；
- ρ 用 task utility/metric，不用 proxy score；
- “verifiable”仅保留给规则/单测/exact-match 等确定性验证器；当前主线叫 proxy-reward-guided search。

若 selector 不能在两个独立数据面稳定优于 random/MBR，它仍是一个有价值的负结果，但不能靠“TFRL”命名获得科学贡献。

### F′-5. unequal-budget comparison 仍破坏因果解释

#### S3

triggered 每 item 用 5 或 6 次生成，always retrieval 只用 2 次。即使删除成本成功门，比较效果仍无法回答“触发策略是否更好”，因为 triggered 同时获得更多 sampling/consensus compute。

删除成本门只避免了数学不可能，并没有消除 treatment confounding。

#### Selector

v4.1 同时写：

- selector/random/MBR/single RDU 严格匹配同一 K；
- single RDU 定义为 K=1。

K=1 与 K>1 不可能在 generation budget 上严格相同。若为 single RDU 也生成 K 次再只取第一个，它不再是通常意义的 K=1 成本臂；若只调用一次，就不是 equal-budget control。

**正确设计**：

- `K-candidate generator + selector`、`K-candidate random`、`K-candidate MBR` 为真正等预算 selector family；
- `single RDU K=1` 作为 low-cost system baseline，不能标 equal-budget；
- S3 做 `sample budget (1 vs 5) × retrieval policy (always vs triggered vs never)` factorial，或改用 single-pass cheap trigger；
- headline 同时报 effect 与 compute，不能在标题称“业务效果”却把成本推迟到后期。

---

## 4. 统计计划仍未达到 preregistration 等级

### 4.1 primary m=7 是模板，不是冻结原子族

附录 A 的 7 atoms 是比 v4 好的骨架，但仍有 `<FOCUS>/<REP1>/<REP2>`、per-version α、per-dataset SESOI、no-harm margin、K、N*、reward weights 和 exact p-value algorithm 未填。

`paired_cluster_bootstrap_mean_diff` 是统计/CI 过程，不自动产生可供 Holm 使用的唯一 p 值。必须明确：

- null 与方向；
- bootstrap p-value 或 randomization p-value 算法；
- studentized/non-studentized；
- cluster resampling unit；
- CI 与 Holm-adjusted decision 的优先关系；
- `relative reduction ≥10%` 与 `CI lower > SESOI` 是否同一 null；
- replication no-harm 的 margin；
- 七项是否全部通过才成功，还是 gatekeeping hierarchy。

### 4.2 secondary family 仍未原子化

`S1a: R@k + end-to-end` 已经至少两个 endpoints；S1b 有多个 embedders；S4 有三个 constructs；S3 同时写 TOST/优越性。附录只给摘要，不是 `dataset × endpoint × contrast` manifest。

因此 S-1 只能判 primary skeleton partial-closed，不能写“multiplicity 已关闭”。

### 4.3 focus selection 与 eligibility 的时间逻辑矛盾

manifest 写 `selection_rule: frozen_before_eligibility`，但 datasets 直到 M2 eligibility 后才命名，且 M2 同时包含全臂 dev 排序、资格判定和原子族定稿。

需要冻结明确顺序：

1. 候选 datasets；
2. dataset-selection rule；
3. eligibility IDs 与 analysis；
4. focus/rep identities；
5. dev configuration selection；
6. confirmatory registration。

若 focus 是根据 observed headroom 最大者选择，confirmatory inference 必须承认 responder selection；不能写成 focus 先验固定。

### 4.4 ρ 是不稳定比值，定义仍不足

\[
\rho=\frac{R_{selector}-R_{greedy}}{R_{oracle}-R_{greedy}}
\]

需要明确是 ratio of aggregate means，还是 mean of item-level ratios。后者会在小/零 denominator 爆炸；前者仍有 ratio-estimator 偏差和不对称 CI。

建议：

- primary 报 absolute selector delta；
- ρ 为 co-primary/secondary mechanistic metric；
- 只计算 aggregate ratio，不平均 item ratios；
- 用 paired cluster bootstrap 对整个 numerator/denominator 联合重采样；
- 预注册 denominator floor 与 undefined handling；
- 做 Fieller/percentile bootstrap sensitivity；
- 不因 denominator 小而删除不利 datasets。

---

## 5. 理论轨仍存在对象和测量错误

### 5.1 τ 的测量槽不支持 uniform error bound

v4.1 把 τ 的测量写成“selector vs oracle 一致度”。argmax agreement 不是

\[
\sup_{\tau}|\hat U(\tau)-U(\tau)|\le \epsilon
\]

的证据。两个 reward 可以 argmax 一致但数值误差巨大，也可以 argmax 不一致但 regret 极小。

正确测量应保存每个 candidate 的 proxy score 与 true task utility，在独立 calibration data 上建立 high-probability error/regret bound，并验证跨 dataset/core shift。若只能测 rank agreement，就应证明 rank-based finite-sample guarantee，不得偷换成 uniform error。

### 5.2 N* 只是预算 cap，不是收敛条件

有限 K 让算法停止，不意味着它随迭代“收敛到正确对象”。在当前一次性 finite candidate selection 中，最自然理论是 finite-sample regret/selection error，不是 dynamical convergence。

若要证明 convergence，必须有明确定义的 sequence：随着 verifier samples、calibration data 或 computation budget 增长，\(\hat U_n\) 如何更新、误差为何趋零、candidate space 如何变化。否则“有 N* 所以收敛”只是有限性。

### 5.3 检索-递送不等式不是一般必要条件

\[
r_0\Delta_{deliver}\ge(1-precision)c_{distractor}
\]

只有在非常特殊的事件定义、共同分母、独立性和单候选条件下才能作为期望净收益条件。一般系统还需要：

- knowledge-needed prevalence；
- trigger rate；
- recall conditional on need；
- false-positive retrieval rate；
- top-k 中相关/不相关证据数量；
- adoption probability conditional on evidence quality；
- benefit/harm 的 item heterogeneity 与 interaction。

此外：

- `precision` 的 measurement slot 却指向 S4 同音 precision，不能代表 QA retrieval precision；
- `Δ_deliver = oracle retrieval vs bare` 混合“证据可得性”和“递送形式”，不是纯 delivery effect；
- relevant document 包含 answer 是合法检索目标，不能用字符串 scrub 近似边界。

该式目前最多是 heuristic design inequality，不能叫已识别的 necessary condition，更不能直接进 Lean 作为 load-bearing assumption。

### 5.4 现有 Lean 不等于 #27 已完成

仓库已有 `Realization.lean` 的 generic argmax mismatch bound 和 `Iterate.lean` 的一般单调有界序列结果；这些是可复用基础。但 §4 K-trajectory implementation 尚不存在，Python↔Lean conformance 也未交付。v4.1 对此保持“待完成”是诚实的；任何 checker 不得因章节写得完整就判 operator-linked theory closed。

---

## 6. #37 工程审计：哪些真修了，哪些仍没修

### 6.1 真正完成的工程修复

W1 commit `48502ca` 是 1,954 additions / 144 deletions 的实质包，不是空提交。确认：

- CER implementation 与中文 tests；
- legacy squtr archive script，并在本机 E: knowledge root 归档 16 个旧 sources；
- GLAP/Nemotron status downgrade；
- real cross-modal verification script；
- corpus-only pseudo-question entry；
- manifest provenance schema + backfill sidecars；
- confirmatory seed override hard-error；
- overwrite refusal与 draw log；
- W1 worktree 当前 clean。

### 6.2 `run_mock` 仍保留错误对象 fallback

`source_name_for` 只有在新 corpus manifest 存在时才返回新 source；否则回到旧四字段名字。测试甚至把这个 fallback 当成 PASS。

这意味着：

- 本机归档有效；
- clean checkout/另一机器若仍有旧 source，代码仍可能消费旧错误对象；
- 新 corpus 缺失时没有 fail-closed。

**必须改为**：squtr 非 dry-run 一律 hard-require corpus source；不存在就报 P0 object error，绝不回落 legacy。

### 6.3 deterministic draw 不满足自己宣称的 group-disjoint firewall

算法只接收 item IDs：没有 group map/group hash/group-disjoint verification。`exclusion_lists` 还是 optional；confirmatory caller 可以不传 eligibility/dev/exposure union。

必须：

- confirmatory mode 要求 group manifest；
- 按 group 抽样，不按 item 抽样；
- 自动加载并强制排除所有 prior exposure manifests；
- 缺一个 manifest 即 fail-closed；
- manifest 记录 group IDs 与 overlap proof；
- 禁止在同一 public seed 下随意改变 pool/exclusion definition。

### 6.4 append-only JSONL 不是 tamper-evident ledger

本地文件以普通写权限存在，可以删改。它是 useful audit trail，不是防篡改证明。Git commit、signed hash 或外部 append-only store 才能提高 tamper evidence。

### 6.5 provenance sidecar 明确不是 build-time provenance

例如当前 squtr GLAP sidecar 写：

- `code_git_sha_at_backfill = 20d45a8`，不是实际 build-time SHA；
- `embedder_revision_guess`；
- `normalization_assumed`；
- recomputed hash 与 manifest hash 不同，注释称可能只是 SHA 输入不同。

这种诚实 sidecar 有取证价值，但不能被描述为“旧工件 provenance 已补全”。旧 KB 要么重建，要么永久保持 `legacy/incomplete-provenance`。

### 6.6 测试状态不是“all suites green”

本轮 fresh run：

```text
targeted pytest including test_phase_a_e2e.py:
82 passed, 4 errors

PYTHONPATH=src pytest -q:
124 passed, 4 errors
```

四个 error 都因 `test_phase_a_e2e.py` 的 `test_*` 函数要求不存在的 `results` fixture。该文件以独立脚本运行时确实得到 `PHASE_A_E2E_TEST_PASS`。

因此准确表述是：

> custom script entry passes; standard pytest collection is broken.

M1 的 clean-checkout gate 必须冻结唯一标准命令，并让标准 pytest 通过；不能让 commit message 的“all suites green”依赖未披露的入口选择。

### 6.7 real science path 仍未运行

- `live_verify_crossmodal.py` 明确未跑；
- `_repro` 中没有新的 live cross-modal report；
- q2q tests 仍主要使用 fake generator/embedder；
- §4 trajectory selector 没有对应新 harness；
- 当前 active squtr corpus 是 label-conditioned mini-corpus。

所以 #37 证明 remediation plumbing 前进，不证明 M1 science-ready。

---

## 7. conformance report 为什么不能作为独立关闭证据

`docs/checks/v41-conformance-report.md` 正确声明它不是外部评审，这是优点。但它仍有四个问题。

### 7.1 承诺工件不存在

回复承诺：checker code commit + rule manifest + input hash + output JSON + failures + environment。当前 `docs/checks/` 只有一个 Markdown report。repo 中未找到：

- checker source；
- executable rule manifest；
- raw JSON output；
- environment capture。

因此“机器一致性检查已冻结”不成立，只能称 machine-assisted manual report。

### 7.2 “independent”定义不成立

checker 是 Opus AI、属于同一工作流，并对 response letter 直接施加 mechanical fix。它可以是 useful second pass，但没有人员/团队独立、数据隔离、决策隔离或利益冲突标准，不能承担 research-integrity independence。

### 7.3 `RELEASE-READY` 范围过宽

如果只是“文档包可发给外审”，可以说 `DOCUMENT PACKAGE READY FOR EXTERNAL REVIEW`。`RELEASE-READY` 容易被后续 AI 读成方案可执行/科学已清白，尤其 v4 历史上已经发生 `CLEAN-FOR-REVIEW` 误导。

### 7.4 checker 漏掉的直接矛盾

- business effect 标题 vs conventional threshold；
- unpredictable custody gate vs public predictable seed；
- owner rejects burn vs #37/回复又要求 append-only burn-like supersession record；
- equal-budget vs K=1；
- group-disjoint proposal vs item-only draw implementation；
- secondary family 未原子化；
- qrels-conditioned corpus vs evaluation-independent KB；
- standard pytest red。

因此六个 PASS 只能证明检查规则太窄，不能证明科学一致性。

---

## 8. 新颖性与博士论文价值判断

v4.1 加入 WavRAG、VoxRAG、PlanRAG-Audio 是必要进步：

- [WavRAG](https://aclanthology.org/2025.acl-long.613/) 已做 native audio retrieval 与 text/audio hybrid KB，并报告相对 ASR-text pipeline 的速度优势；
- [VoxRAG](https://aclanthology.org/2025.magmar-1.3/) 已用 CLAP+FAISS 做 transcription-free spoken QA，虽 retrieval/answer quality 仍弱；
- [PlanRAG-Audio](https://aclanthology.org/2026.findings-acl.1304/) 已做 planning + structured text/audio retrieval，并把效率作为核心结果。

因此，单说“audio RAG + planning/RDU + frozen components”不足以构成博士级贡献。可守的贡献必须来自：

1. strict core-black-box 下的 modality×form×delivery 因果分解；
2. q2q/HyDE 对 full-corpus audio-query retrieval 的稳定净增益；
3. proxy selector 在等预算下稳定实现 oracle headroom；
4. proxy failure、self-consistent error、reward hacking 和 N* 的严谨边界；
5. 跨 core/dataset replication。

如果 selector 最终不优于 MBR/random，这仍可是一篇好负结果论文；但需要把“为什么 label-free proxy 无法实现 headroom”作为中心，而不是继续扩大系统包装。

---

## 9. 对“学术欺诈”风险的精确判断

### 9.1 当前不能指控 FFP

没有看到：

- 凭空生成不存在的 raw results；
- 删除失败工件后只留正结果；
- 修改 per-item rows 以匹配 headline；
- 抄袭来源。

代码和历史反而保留了不少不利证据。

### 9.2 当前确认的 QRP/治理问题

- qrels-conditioned mini-corpus 被称为 evaluation-independent KB；
- `n_golds=0` 的 vacuous audit 输出 `CLEAN`；
- 内部 AI checker 被称 independent；
- 承诺的 checker artifacts 未交付；
- “业务效果”标签在无 utility/cost 门时残留；
- per-version α 忽略 repeated-study multiplicity；
- same K/equal budget 口径不可能同时成立；
- custom script green 被概括为 all suites green；
- 作者责任部分转嫁给“协调 AI”。

### 9.3 作者责任不能转交给 AI

AI 可以解释错误产生路径，但论文作者、PI/owner 和签字人对最终文本、代码、统计与工件负全部责任。正确措辞应是：

> The drafting workflow introduced the error; the authors failed to catch it before release and retain full responsibility.

“AI 写的”不能成为减责事由。

### 9.4 正式调查触发器

以下任一发生，应冻结相关 claim 并启动独立 inquiry；不是预先定罪：

1. 当前 310-doc qrels-conditioned corpus 被用于 confirmatory headline，却称 full/independent corpus；
2. 把 `n_golds=0 CLEAN` 当成无泄漏证明；
3. 公开固定 seed 的 IDs 被称 blinded/unpredictable/fresh；
4. 多版本中只报告成功版，不报告 program-level alpha/cumulative failures；
5. 把 self-consistency/verbal confidence 写成确定性 correctness verifier；
6. 用 5/6-call triggered 对 2-call always 的优势归因于 trigger；
7. 把 K=1 single RDU 写成与 K>1 selector 等预算；
8. conformance report 继续声称存在实际上没有的 checker code/JSON/rule artifacts；
9. standard pytest 红却对外写 clean-checkout all-green；
10. 在 real live smoke 之前把 cross-modal 状态升级 supported。

---

## 10. 建议的 v4.2 重构方案

### 10.1 把研究问题收成两个真正独立的 confirmatory questions

**Q-A：System effect**

> 在 full/query-independent corpus、严格 core-black-box、所有外部组件冻结使用的条件下，RDU 相对 bare、long-context、own-ASR→text strong RAG 是否有净增益？

**Q-B：Selector effect**

> 给定完全相同的 K trajectories，\(\hat U\)-selector 是否优于 random、MBR 和预注册 confidence baselines，并实现正的 absolute utility delta 与稳定 ρ？

Q-A 不能只以 bare core 为 load-bearing；Q-B 不能混入 K=1 cost baseline。

### 10.2 重新定义 reward

```text
U(trajectory)      = confirmatory task utility, gold available only for evaluation
U_hat(trajectory)  = deployable proxy: consistency / verifier / confidence
selector           = argmax U_hat
oracle             = argmax U
regret             = U(oracle) - U(selector)
rho                = aggregate selector gain / aggregate oracle gain
```

把“verifiable”从 proxy 中删除。对 proxy 做：

- within-question ranking AUROC/pairwise accuracy；
- calibration/Brier/ECE 仅作不同问题层；
- self-consistent-error stress subset；
- cross-model verifier 与 same-model-different-prompt 分开；
- K 扩大时 true utility 与 proxy utility 的 Goodhart curve。

### 10.3 重建 squtr 测试床

- focus confirmatory 使用 full fiqa 57,638 corpus；
- 允许 q2q 离线生成，但只从完整 corpus 文档生成；
- q2q generator 不见 test queries/qrels；
- qrels 只在 scoring process 读取；
- 当前 310-doc mini-corpus只作 DEV smoke；
- retrieval 报 Recall@k/nDCG/MRR，端到端另报；
- corpus build hash 与 q2q generation hash 分开。

### 10.4 重新设计 S3

最小 factorial：

| Sampling budget | Never | Always retrieval | Triggered retrieval |
|---:|---:|---:|---:|
| 1 | ✓ | ✓ | cheap one-pass gate only |
| 5 | ✓ | ✓ | ✓ |

这样才能估计 retrieval-policy main effect、sampling main effect 和 interaction。若 triggered 必须先 5 samples，则其公平对照是 5-sample always/never，不是 2-call always。

### 10.5 统计与 custody

- focus dataset 在 eligibility 前先验固定；若必须筛 responder，headline 只限 responder cohort；
- 完整展开 primary + secondary atoms；
- 预注册 no-harm/TOST margins、p-value algorithms、gatekeeping success logic；
- 一个 final confirmatory version，或 program-level online FWER；
- public deterministic evaluation 与 blinded confirmatory 二选一，禁止混称；
- 最低成本 confirmatory 方案：外部人员/benchmark server 在 code+analysis freeze 后一次性评分；
- absolute delta 为 co-primary，ρ 为 mechanism metric；
- 全部历史版本进 cumulative table。

### 10.6 理论轨

第一阶段只证明 finite-sample selector regret：

\[
U(\tau^*)-U(\hat\tau)\le 2\epsilon
\]

前提是独立 calibration set 给出可核验的 uniform/high-prob proxy error bound。之后再研究随 verifier samples 增长的 convergence。不要把 cost cap 当 convergence。

检索系统的净收益理论应从事件级 utility model 推导，而不是直接使用 `recall×delivery − (1−precision)×cost`。

---

## 11. M1 重开所需检查点

全部满足前，M1 仍是 DEV-only：

- [ ] `PYTHONPATH=src pytest -q` 标准入口零 error；
- [ ] squtr source missing 时 hard-fail，不 fallback legacy；
- [ ] full/query-independent corpus build；
- [ ] `CLEAN` audit 拆分并消除 `n_golds=0` vacuous pass；
- [ ] group-aware deterministic draw；
- [ ] confirmatory 自动加载完整 exposure union，缺失 fail-closed；
- [ ] true live GLAP/Nemotron audio→text retrieval report；
- [ ] §4 K-trajectory harness 与 equal-K random/MBR selector；
- [ ] K=1 baseline 不再标 equal-budget；
- [ ] real q2q 2-doc smoke + full-corpus scaling estimate；
- [ ] old KB 重建或永久 incomplete-provenance；
- [ ] holdout-supply table 与真实 custody choice；
- [ ] exact atomic SAP、alpha sequence、SESOI、no-harm/TOST margins；
- [ ] owner 七项签字和真正独立 reviewer 裁决。

---

## 12. 最终导师意见

如果这是我的博士生，我会给出这样的评价：

> 你们这次学会了公开承认错误，也做出了不少真实修复，这是研究能力的进步；但你们仍然过早地把“文档写得完整”当成“科学对象已经闭合”，把 owner 的资源偏好当成统计学有效性，把 proxy agreement 当成 verifiable reward，把可复算抽样当成盲法，把 qrels-conditioned mini-corpus 当成独立知识库。博士论文最危险的不是负结果，而是用越来越复杂的治理术语掩盖一个尚未被正确识别的实验对象。

因此最终裁决为：

> **回复诚意：基本接受；四处勘误：接受；#37 工程：部分通过；v4.1：重大重构；M1：未绿；Stage 2：继续关闭；FFP：未发现；QRP：仍高风险；独立监督：强制。**

下一步不应再增加系统组件或写更宏大的 narrative。先完成三件事：

1. 把 qrels-conditioned corpus 改成 full/query-independent corpus；
2. 把 \(U\) 与 \(\hat U\) 分开，并做真正等 K selector 实验；
3. 在 custody 和 program-level alpha 上做一个可以被外部统计审稿人接受的选择。

这三件事不关闭，任何大规模 GPU 运行都只是更昂贵地放大当前设计偏差。
