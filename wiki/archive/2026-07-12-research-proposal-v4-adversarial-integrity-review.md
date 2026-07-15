# 2026-07-12 — Research Proposal v4 对抗式方法学与研究诚信审查

> **审查对象**：`wiki/2026-07-13-research-proposal-v4-external-review.md`，以及截至本审查时可见的 W1 M1 在途实现、权威 claim ledger、项目 thesis/status、历史审查回复与 Git 时间线。  
> **审查日期**：2026-07-12（Asia/Singapore）。  
> **审查性质**：只读、独立、敌意测试式复核；不是对 v4 的批准，也不是对作者主观意图的推断。  
> **证据词汇**：`FACT` = 可由当前文档/代码/工件直接核验；`INFERENCE` = 由事实推出的审查判断；`UNKNOWN` = 当前证据不足。  
> **纪律**：本报告没有改动 v4、代码、账本、实验工件或团队正在进行的工作；只新增本 dated review。

---

## 0. 一句话裁决

**REJECT / NO-GO：v4 当前不能签字、不能进入 Stage 2、不能消费 eligibility 或 confirmatory split，也不能被称为“已通过外部评审”。**

团队对上一轮错误对象、伪 holdout、缩窄 multiplicity、Coverage 定理命名和内部 AI QA 口径，确实做了若干真实整改；但 v4 同时引入或保留了四个足以单独否决方案的结构性问题：

1. S3 的“节省调用”成功门按其自身成本定义**数学上不可达**；
2. 旗舰 `qwen3-omni-own` 隐状态检索键与“严格闭源 API 黑盒契约”**直接冲突**；
3. RDU 主系统目前是 frozen speech-RAG/orchestration，缺少项目 thesis 所要求的 reward-guided inference-time operator，不能自动继承“training-free RL”身份；
4. 权威证据账本与正文发生 post-notice 冲突：`C-MINDS-V2` 被从 `directional` 升成 `valid`，不存在的 `C-KEEP` 被当成已入账证据，`invalid` 的 `C-T7` 又被软性回收到正向理论动机。

此外，正在实现的代码暴露出新的错误对象风险、中文 agreement 指标实现错误、未实机验证即标 `supported`、公开可预测的“custodian”方案，以及 unit tests 与科学有效性之间的巨大覆盖空洞。

**FFP 裁决**：当前没有足够证据认定 fabrication、falsification 或 plagiarism；不得把严重方法学错误直接写成“造假已成立”。但是，已经出现可确认的 questionable research practices（QRP）和数个应进入独立 research-integrity inquiry 的条件式触发器。特别是，同类证据升级在明确审查告知后再次发生，不能再无条件解释为普通疏忽。

---

## 1. 本轮如何做多轮对抗式评审

本轮不是一次性通读，而是按四个相互攻击的 reviewer 角色执行：

### Round A — 方案内部一致性攻击

逐条检查 headline、接口契约、假设、成本、统计族、成功门、签字门和理论结论是否能同时为真。该轮发现 S3 不可达、黑盒契约自相矛盾、`MAX=15` 不是原子检验族、need-label 的 `iff` 不成立、理论下界缺必要条件。

### Round B — 实现与工件反证

不接受“文档已定义”的自证，而是检查在途代码、测试 seam、manifest、claim ledger、Git 状态和时间线。该轮发现 pseudo-question 默认读取 query/transcript 而非 corpus value、K2 中文使用 word-WER、跨模态 `supported` 仅由 stub test 验证、确定性抽样允许公开 seed 覆盖和重复覆盖写入。

### Round C — 文献与新颖性攻击

用最接近的 speech/audio RAG、adaptive retrieval、query expansion、retriever–generator interaction 与 trained speech-biasing 工作反证空白和机制叙事。该轮确认 v4 漏掉 WavRAG、VoxRAG、PlanRAG-Audio 和系统性 adaptive-RAG benchmark；RDU 的系统级组织本身不能据此主张空白。

### Round D — 研究诚信 hostile meta-review

把每个问题分类为 honest error、方法学缺陷、QRP 或潜在 FFP 调查触发器，并专门寻找负结果删除、事后换指标、证据洗回、非独立复现冒充独立、可预测 holdout 冒充盲法等模式。结论不是“已造假”，而是：**当前保存负结果的行为降低了 fabrication/falsification 的怀疑；最危险的模式是保留 caveat 的同时，在醒目标签、机制故事和系统 headline 中选择性升级证据。**

四轮审查结论一致：**v4 不具备 Stage-2 readiness。**

---

## 2. 对团队回复的逐项判决

| 项目 | 判决 | 严格解释 |
|---|---:|---|
| 承认旧 `squtr`/vocalbench 错误对象并停止 140 格 | **PARTIAL ACCEPT** | 叫停和保留错误记录是真整改；但 `C-PHASEA` 仍是 `invalid`，新 q2q builder 的默认值路径又可能把 query 当 evidence，错误对象风险尚未封死。 |
| 将旧 locked TEST 永久降级为 exposed-dev-like | **ACCEPT** | 当前回复没有继续把它称为 untouched；这是上一轮要求的实质满足。 |
| ASR Holm 完整家族更正 | **ACCEPT** | 团队承认 16 格完整家族不显著，也没有再称独立复现。 |
| MInDS 5 个 unique contrasts 修复 | **PARTIAL ACCEPT** | 机械重复问题已修；但证据仍是 Stage-1 `directional`、composite candidate-card treatment，不能升级成 valid 或“标准知识卡 schema 已证”。 |
| content hash / refuse-overwrite / archive | **PARTIAL ACCEPT** | 这些是必要的机械 provenance 防线；clean-checkout reproduction、真实 corpus value 抽检、跨模态实跑和外部复算仍未关闭。 |
| Coverage theorem 降级 | **PARTIAL ACCEPT** | 不再把静态恒等式冒充系统收敛，是进步；但 operator-linked Lean theorem 仍为 0，v4 新下界本身也不成立。 |
| 内部 AI QA 改名 | **PARTIAL ACCEPT** | 文案有所纠正；RI-6 未完成，11/11 内部复算仍不能成为 independent reproduction。 |
| 新 confirmatory custody | **REJECT** | 固定公开 seed + 仓库内确定性脚本只保证可复算，不保证开发者在冻结前无法知道或挑选 ID；它不是独立 custodian。 |
| `MAX=15` 与五轮 alpha spending | **PARTIAL / IMPLEMENTATION REJECT** | 固定分母与跨轮预算意识是进步；但 15 行不等于实际 elementary hypotheses，五轮修改系统也不应包装成同一个冻结研究。 |
| `C-MINDS-V2 = valid` | **REJECT** | 与权威 ledger 直接冲突，且混淆 composite treatment 与 delivery/schema 机制。 |
| `C-KEEP directional, 24%` | **REJECT** | 当前 ledger 中没有 `C-KEEP`；“以后追溯并 mint”不能使它今天成为证据。 |
| `C-T7` 作为 recall-first motivator | **REJECT AS EVIDENCE** | 可作为失败史保留，不能从 invalid/leaked 结果中回收效应方向来支撑正向机制。 |
| v4 作为“external review”或 clean verdict | **REJECT** | 文件只有 audience/标题，没有外部 reviewer 的具名裁决和签字；内部 checker 不能自证外审通过。 |
| 当前 M1 在途工作 | **LIMITED GO** | 只允许 exposed DEV、synthetic、dry-run、单元测试、corpus/value/provenance 修复；禁止 confirmatory 消费和任何证据升级。 |

---

## 3. 四个 FUNDAMENTAL 阻断项

### F-1. S3 的成本成功门不是“困难”，而是无解

**FACT**：v4 要求 triggered two-pass 相对 always-retrieval 减少至少 30% 的调用，同时保持效果等价。v4 又定义：

- triggered：先做 `m=5` 次采样；未触发时总成本 5 次生成，触发时再生成一次，总成本 6；
- always retrieval：一次初始生成 + 一次带知识生成，总成本 2；
- never retrieval：1 次。

在途 `two_pass_runner.py` 与该定义一致：`run_pass1` 调 `generate_fn` 共 `m=5` 次，触发后 `run_pass2` 再调一次。

若触发概率为 \(p\)，triggered 平均生成次数为

\[
C_{trigger}=5+p\ge 5.
\]

相对 always retrieval 降低 30% 要求

\[
5+p \le 0.7\times 2 = 1.4,
\]

没有任何 \(p\in[0,1]\) 能满足。即使作者误写成“成本不超过 always 的 130%”，也要求 \(5+p\le2.6\)，仍无解。

**INFERENCE**：这不是一个可证伪的科学假设，而是定义上必败的 gate。若实验最终报告“节省 ≥30%”，则必然发生了分母替换、漏记四次 completion、把 batch HTTP request 冒充一次 generation pass，或事后改变成本定义。

**必须修复**：

1. 选择真正廉价的一次性 trigger（retrieval-score、单次 confidence、外部小模型或无 LLM 信号）；或
2. 保留 `m=5`，但把研究问题改为“更高计算成本下是否位于 accuracy–latency/token/$ frontier”，不得再写节省调用；
3. 三臂严格匹配采样/选择预算，否则 triggered 的五样本 medoid 与 always/never 的单样本输出混杂；
4. 成本必须同时报告 completion 数、input/output tokens、wall-clock latency、GPU-seconds 与货币成本。

系统性 adaptive-RAG 评估已经表明，效率经常被复杂管线忽略，而且较轻的不确定性方法可能在效率/自知性上胜过复杂 pipeline；v4 不能只以 FLARE/Self-RAG 家谱代替强效率基准：[Adaptive Retrieval Without Self-Knowledge, ACL 2025](https://aclanthology.org/2025.acl-long.319/)。

### F-2. 旗舰检索键违反唯一黑盒接口契约

**FACT**：v4 把可迁移系统接口锁为“音频/文本输入、文本输出、允许多次采样”，明确不依赖 hidden state/logit/logprob 等白盒能力；但旗舰检索键又是 `qwen3-omni-own` 的 2048d hidden-state audio embedding。

**FACT**：Qwen3-Omni 官方公开的生成使用面是多模态输入和文本/音频输出，没有把 2048d 内部隐藏态规定为通用 closed chat API 的输出：[Qwen3-Omni official repository](https://github.com/QwenLM/Qwen3-Omni)。当前 W1 实现也把 `qwen3-omni-own` 的 cross-modal audio query 标成 `pending-GPU-window`，而非已完成的通用黑盒路径。

**INFERENCE**：本地 llama-server 或自定义 harness 能抽 hidden state，并不能支持“任意闭源 API 可迁移”。当前文案把“本地白盒诊断能力”和“部署 API 契约”合并成了一个旗舰臂。

**必须二选一**：

- **严格黑盒主张**：主臂只允许 own-ASR→text retrieval，或一个明确独立、冻结、部署可获得的 audio/text embedder；核心 hidden state 仅作白盒诊断，不参与 portable headline；
- **本地白盒主张**：承认需要内部 embedding endpoint，删除 closed-API/any-core portability headline，并列出实现依赖。

### F-3. RDU 尚不是仓库定义的 training-free RL

**FACT**：权威 Project Thesis 要求在推理时以可验证 reward 搜索/选择模型行为。v4 的 load-bearing RDU 是 query expansion、retrieval、triggering 和 prompt delivery；reward 层被降为基础设施，而且不用于输出重排作为研究主张。

**INFERENCE**：这是一个可能有价值的 fully-frozen speech-RAG/agentic orchestration 研究，但不是因为“没有训练”就自动成为 RL。把所有 inference-time orchestration 都称为 RL 会使项目主张失去可证伪边界。

**整改路径**：

- 路径 A：把该工作独立命名为 `training-free / fully-frozen speech RAG`，与 TFRL 主线分轨；
- 路径 B：定义真实算子：对同一输入生成 \(K\) 个 query rewrite/retrieval/card/answer trajectory，以部署可得且预注册的 reward 选择；与等预算随机选择、MBR 和单次 RDU 对照；形式化 action、policy、reward、update/selection operator 与 stopping rule。

路径 B 还必须使 Lean theorem 与 Python 执行的是同一算子，而不是给 RAG 系统附上一个无关的静态不等式。

### F-4. 方案身份与项目 canonical thesis 发生漂移

**FACT**：Project Thesis 仍把 W4 的 frozen omni embedding disentanglement 定为旗舰；Per-Work-Status 仍反映此前 W4/W1 定位。v4 却把 W1 风格 RDU 知识系统变为新的主问题。

**INFERENCE**：改变方向本身不违规，但目前没有清晰的 owner-ratified supersession/new-work identity。若直接把 v4 当作原 thesis 的自然延续，读者会无法判断是 pivot、W1 子研究、W4 替代品还是新 work。

**必须修复**：Stage-2 签字前由 owner 明确选择：保留原旗舰、建立并行新 work、或正式 supersede；同时更新 thesis、per-work status、claim scope 和论文身份。未作选择前只能称 Stage-1 proposal exploration。

---

## 4. 正在处理的 M1 工作：实现级漏洞

### I-1. pseudo-question builder 可能重复“错误对象”事故

**FACT**：`build_pseudo_question_source(dataset_loader_key, value_spec="text")` 从 generic dataset registry 取 row，然后 `_extract_value(row, "text")` 读取 loader 的 `row["text"]`。同文件注释已承认，对 registry dataset，`value_spec='text'` 可能是 QUERY/transcript。

**FACT**：真实 `squtr` loader 的 query 与 corpus evidence 是两个不同对象。当前测试注册的是 fake dataset，其中 `meta.text` 恰好被构造成 evidence，因此没有覆盖真实 `squtr` 语义。

**INFERENCE**：若以默认接口在 `squtr` 上执行 q2q，系统可能从评估 query 合成 pseudo-questions，并把 query 当 value；这正是上一轮 P0-1 错误对象的变体。content hash 和 refuse-overwrite 只能稳定地保存错误对象，不能证明对象正确。

**必须修复**：pseudo-question builder 必须接收已经审计的 corpus-document records/source manifest，不得重新从 generic query loader 猜 value；加入 real-squtr semantic test，断言每个 value 来自 qrels 指向的 corpus document，并断言 query text、gold answer、transcript 不被用作 corpus evidence。

这里需要区分“孤立 builder 的局部对象”与“可运行实验臂”：当前 isolated q2q builder 在输入确为 evidence passage 时，确实构造 `key = pseudo-question`、`value = same evidence passage`，这一局部语义是正确的；但代码自己声明尚未接入 `run_mock`/Phase-A，测试又全是 fake rows。与此同时，`run_mock.py` 的 `source_name_for` 仍指向旧 `squtr__<embedder>__<key_org>__<value_org>` active source。磁盘上新建的两个 310-document corpus 库虽为真实 evidence docs，实际消费路由并未切换；旧 active source 的 value 仍可见 query 本身且被标为 `CLEAN`。因此“新 corpus 已建”不等于旧错误对象已从实验闭环消失。

### I-2. K2 中文 agreement 实现错误

**FACT**：`two_pass_runner.py` 把 K2 映射到 `_wer`，调用 `jiwer.wer`；normalization 没有把中文拆为字符。注释声称“char-wise”，实现却是 word-WER。

本轮只读验证得到：

```text
你好世界 vs 你好世间: two_pass_wer = 1.0, CER = 0.25
今天天气很好 vs 今天天气真好: two_pass_wer = 1.0, CER = 0.166666...
```

**INFERENCE**：大多数非完全相同的中文句子会被视为一个整词替换，agreement trigger 将严重失真。项目现有通用 `metrics.py` 已正确使用 `jiwer.cer`，说明这是 two-pass 新路径的局部回归。

**必须修复**：K2 明确调用 CER，加入中文 minimal-pair、插入/删除/替换、标点/NFKC 测试；不得仅测试英文 `hello world`。

### I-3. `supported` 不是实机证据

**FACT**：`omni-embed-nemotron` 被状态表标为 `supported`，实现注释又承认 audio query 对 `encode_query({"audio": ...})` 尚未 live verify。测试通过 stubbed embedding 检查路由和排序，不启动真实模型，也不检查真实 audio→text embedding 的维度与语义。

**INFERENCE**：contract test 只能证明“若底层返回向量，路由能继续”，不能证明官方模型实际接受该输入或跨模态检索有效。

**必须修复**：状态降为 `pending-live-verification`；满足以下 gate 后才可升 `supported`：真实模型加载、真实 wav query、text corpus embedding、维度一致、非 NaN、已知正例 top-k、负例排序与批/单一致性。

### I-4. q2q 的“同分布”只桥接形式，没有桥接模态

音频问题与文本伪问题都采用 question discourse form，不等于分布相同。必须把设计拆成：

- modality bridge：native audio key vs own-ASR text key；
- form bridge：raw document/q2a vs doc2query/q2q vs HyDE/a2a；
- delivery：flat vs equal-content card。

至少做 `2 × 3 × 2` 的受控设计或合理的层级 gate，才能区分是 modality alignment、query/document asymmetry，还是 delivery schema 在起作用。

### I-5. 默认 text embedder 与音频 query 缺少合法桥

**FACT**：pseudo-question 默认 text embedder `auto` 可能退化到 MiniLM 或 TF-IDF。它们能嵌入 pseudo-question 文本，却不能直接嵌入原始音频 query。

**INFERENCE**：q2q 索引可构建不代表可被 audio query 检索。必须为每个 key arm 冻结 query path；`auto` fallback 不得静默改变研究对象。

### I-6. 当前 tests 验证了软件契约，没有验证科学契约

本轮在 WSL2/Python 3.12 环境复跑：

```text
pytest scripts/baselines/test_deterministic_draw.py \
       scripts/baselines/test_two_pass_runner.py \
       scripts/knowledge/test_pseudo_question.py -q
44 passed in 0.88s

python -u scripts/knowledge/test_kb_gate.py
all checks PASS
```

这是正面工程信号，但这些测试大量使用 fake generator/embedder/dataset，未验证：

- 真实 `squtr` corpus/value 对象；
- 真实 Qwen/Nemotron cross-modal API；
- 中文 CER；
- confirmatory custody 的不可预知性；
- equal-budget scientific comparison；
- retrieval need label 的构念效度；
- hidden-state 路径的 closed-API compatibility。

因此，**“tests pass”只能支持 plumbing readiness，不能支持 scientific readiness。**

### I-7. M1 不是 clean-checkout 可重建状态

**FACT**：审查时 W1 HEAD 为 `e30af76`（2026-07-12 01:37 +08:00），但 M1 在途实现位于工作树：7 个 modified、7 个 untracked。`deterministic_draw.py`、`two_pass_runner.py`、`knowledge_card.py` 及其测试、pseudo-question 测试均未提交。

**INFERENCE**：这符合“团队正在实现”的事实，却不符合任何“已提交入库、clean-checkout 重建绿、M1 completed”的口径。未提交实现生成的 artifact 也无法仅凭 manifest 回溯到唯一代码状态。

**必须修复**：在任何批量实验前，冻结代码 commit；clean checkout 执行 unit/integration/real-model smoke；artifact 记录 code SHA、dirty=false、engine build、dataset/model revision、manifest hash。现有 dirty-tree 结果只能为 DEV evidence。

### I-8. 基线表存在数据集身份错配与 provenance 空洞

**FACT**：v4 把 `SQuAD-zh` baseline 写成 `0.925 (n=40)`；实际名为 `SQuAD-zh` 的 locked artifact 是 `0.85 [0.725, 0.95]`，`0.925` 属另一个 `uro-bench-SQuAD-zh` 工件。被引用的 locked baselines 还记录 `git_dirty=true`，且 engine build、dataset revision、manifest hash 为空。

**INFERENCE**：这是可定位的数据集标签错配，不足以单独证明故意伪造，但会直接改变 eligibility/headroom 讨论，必须更正。当前 baseline 可保留为 directional inventory，不能升级为 confirmatory provenance。

### I-9. KB 的 `CLEAN` 与 content hash 覆盖仍不完整

**FACT**：外部 knowledge root 的 65 个 active sources 中，只有两个新 squtr corpus source 带新 `content_hash`；其余大多数旧 source 没有。两个新 source 的构建时间对应未提交工作状态，而 manifest 没有完整存储 hash 所依赖的 code SHA/dirty flag、embedder revision、quantization、normalization 和 index parameters。现有 evidence freeze 也不覆盖 E: 盘 KB 本体。

**INFERENCE**：`CLEAN` 当前主要表示 scrub/audit 状态，不等于对象正确、代码可复现或整个 index lineage 已冻结。必须避免把一个布尔标签扩写为完整 provenance certificate。

---

## 5. 统计设计与因果解释漏洞

### S-1. `MAX=15` 行数不等于 15 个 elementary hypotheses

一行中包含多个 dataset、endpoint、retriever、winner、list length、threshold 和 interaction。若每个格子产生 p 值，Holm-15 会低估 multiplicity；若每行只产生一个联合 p 值，v4 又没有冻结联合统计量、聚合权重和成功语义。

**整改**：发布机器可读 atomic manifest：

```yaml
- hypothesis_id: H_SYS_SQUTR_PRIMARY
  dataset: squtr
  endpoint: normalized_error
  contrast: best_frozen_rdu_vs_bare_core
  selection_rule: frozen_before_eligibility
  statistic: paired_mean_difference
  p_value_method: paired_randomization
  family: primary_confirmatory_v1
  multiplicity: holm
  missingness: fail_closed
```

每个 `dataset × endpoint × contrast` 只能有一个最终裁决算法。若要用 max-T，必须冻结 joint resampling 单位和 dependence structure；不得在看到结果后从 Holm 切到 max-T。

### S-2. eligibility gate 改写了目标总体

用 baseline < 0.85 和 oracle headroom 下界筛选数据集，即使预注册，也会把 headline 从“知识依赖型语音任务”改成“已知有足够 headroom 的 responder datasets”。固定 multiplicity 分母不能恢复外部效度。

**整改**：科学问题先验固定一个 focus dataset 和两个 replication datasets；oracle headroom 只作机制诊断或 futility rule，不作为把不利数据集移出主张总体的资格筛选。若保留筛选，headline 必须明确写 `headroom-qualified datasets only`。

### S-3. H5 的 15%→10% fallback 是观察驱动的移动门槛

在 dev 首格 <12% 时降低目标，不因“事先写出来”就成为业务 SESOI。SESOI 应由用户价值、错误成本、延迟/费用预算决定，而不是由早期效果看起来能否达到决定。

**整改**：签字前固定一个外部可解释阈值；12% 可作为工程 futility/route decision，但不得修改“有意义效果”的定义。

### S-4. 10% 相对错误下降没有业务依据

相对错误下降在不同 baseline 下对应完全不同的绝对收益。v4 没有 stakeholder utility、错误类型权重、SLA、延迟/token/$ budget 或部署容量模型。

**整改**：在 prereg 中同时冻结绝对变化、相对变化、关键错误类型、成本预算和 no-harm gate；若无法给业务依据，就诚实称 conventional scientific threshold，不称 business effect。

### S-5. 固定效应汇总异质任务会掩盖失败

QA EM/F1、intent/slot error、ASR B-WER 并不因为都写成 relative error 就共享同一效应。k=3–4 时 DerSimonian–Laird 也不稳定。

**整改**：一个焦点场景为 primary；其他数据集做 replication/no-harm。若必须汇总，使用预先定义的 hierarchical model、报告 heterogeneity，并要求至少两个预定任务族方向一致，而不是让大样本任务吞掉失败任务。

### S-6. 五个 confirmatory rounds 不是同一个 confirmatory study

每次失败后修改系统，即使使用每轮 \(\alpha=.01\)，也改变了 intervention 和 estimand。fresh holdout 只能控制一部分过拟合，不会让五个不同版本变成一个冻结研究。

**整改**：一个版本只允许一轮 confirmatory。失败后重新做 Stage-2 proposal/prereg/version；旧轮永久保留并进入 cumulative evidence。不得只发表第一个成功版本。

### S-7. holdout supply 必须在签字前证明

v4 把 supply table 延后到 M2，但没有足够 mutually exclusive group holdouts 就无法承诺五轮。必须先证明每个 dataset 的 group cardinality、exclusion、disjointness、power 和不可预知 custody，再决定研究规模。

---

## 6. 构念、机制和理论漏洞

### C-1. `oracle injection changes outcome iff retrieval is needed` 不成立

至少存在四种 potential-outcome 状态：

| Bare \(Y_0\) | Oracle \(Y_1\) | 解释 |
|---:|---:|---|
| 0 | 1 | oracle-benefiter |
| 1 | 0 | oracle-harmed |
| 1 | 1 | 指标不变，不能推出“不需要知识” |
| 0 | 0 | non-responder，不能推出“不需要知识” |

单次随机输出还把 treatment effect 与 sampling noise 混合。这里测到的是 `oracle-treatment responsiveness`，不是 ground-truth retrieval need。

**整改**：以重复采样估计 \(P(Y_1-Y_0>0)\)，报告四层；真正 need label 应来自任务/corpus annotation 或独立人工 rubric。oracle/gold 只能用于离线诊断，不能调完 gate 后再冒充 deployable label。

### C-2. L3 的加法“归因恒等式”不是恒等式

retrieval miss、mismatch 和 non-adoption 可能重叠并交互；把三者直接相加会双计数。generator 在错误证据下的行为也不是固定 distractor cost。

**整改**：

- 设计顺序 counterfactual interventions：oracle retrieval、oracle relevance ordering、oracle delivery、oracle adoption；或
- 使用预注册的 mediation/Shapley decomposition；或
- 将其降格为 descriptive failure taxonomy，不再写 `≈ total gap` 的机制恒等式。

### C-3. “标准知识卡”效应没有被现有证据隔离

`C-MINDS-V2` 是带 label/schema/boundary/examples 的 composite candidate-card treatment，并且 ledger 记录了 card text 与 eval transcript overlap。它不能证明 source tag、relevance signal、usage directive 这个 schema 本身是主导杠杆。

**整改**：S2 必须 equal-content A/B：完全相同事实、示例、token budget 和位置，只改变 schema/turn structure。C-MINDS 只能作为带 overlap caveat 的 directional motivation。

### C-4. 理论正下界缺少必要条件

v4 声称 recall ≥ \(r_0\)、干扰代价有界、\(\Delta_{deliver}>0\) 可推出

\[
r_0\Delta_{deliver}-(1-precision)c_{distractor}\ge0.
\]

这在数学上不成立；还必须显式假设

\[
r_0\Delta_{deliver}\ge(1-precision)c_{distractor}.
\]

而且 precision/recall 的条件分母不同，相关性和 adoption interaction 未定义。当前式子把要证明的结论放进隐藏假设，近乎循环论证。

**整改**：先定义 item-level utility、FP/FN/adoption 事件和概率空间；证明 unconstrained operator failure，再证明同一 Python operator 在明确约束下的 correctness 与 convergence/rate；提供 sorry-free Lean 和 Python↔Lean conformance。若做不到，应删除 theory contribution，只保留可检验的经验诊断式。

### C-5. “零结构改动”术语错误

RDU 明显新增了检索、触发、card、两遍生成和 KB 等系统结构。准确表述应是：

> no base-model weight or base-model architecture changes; external system components are added.

继续写“不改任何结构，把核心搭成系统”会误导读者。

### C-6. S4 混合了外部知识、任务 schema 和 contextual biasing

SLURP intent/slot schema、热词表、QA corpus 和一般外部知识不是同一构念。B-WER hotword biasing 可以是很好的独立研究，但不能不加区分地成为“知识增强”共同机制证据。

**整改**：至少分为 factual external knowledge、task ontology/schema、contextual entity memory 三类，分别定义合法 KB、泄漏边界、成功指标和可迁移主张。

---

## 7. 文献 survey 后的新颖性与遗漏判断

v4 的主要文献问题不是“引用数量少”，而是没有比较最接近的系统，因此创新边界被放大。

### 必须进入 novelty matrix 的最近邻

- [WavRAG, ACL 2025](https://aclanthology.org/2025.acl-long.613/)：原生 audio retrieval 与 text/audio hybrid KB；
- [VoxRAG, MAGMaR 2025](https://aclanthology.org/2025.magmar-1.3/)：模块化、无需转写的 spoken-QA RAG，CLAP + FAISS；
- [PlanRAG-Audio, Findings ACL 2026](https://aclanthology.org/2026.findings-acl.1304/)：规划所需 modality/time span 并从结构化 text/audio DB 检索，与 Discover–Retrieve–Use 的系统叙事非常接近；
- [Adaptive Retrieval Without Self-Knowledge, ACL 2025](https://aclanthology.org/2025.acl-long.319/)：35 个 adaptive retrieval 方法的统一效率/性能评估；
- [BR-ASR](https://arxiv.org/abs/2505.19179)：trained speech-bias retrieval 近邻，必须作为“训练能买到什么”的对照；
- [RECAST, Findings EMNLP 2025](https://aclanthology.org/2025.findings-emnlp.203/)：对 decoder states 做 contrastively trained retrieval，说明强近邻往往依赖训练/内部状态；
- [HyDE](https://arxiv.org/abs/2212.10496)：论文明确承认 hypothetical documents 可含 false details，其有效性依赖 dense bottleneck 过滤；不能只引用“a2a matching”而忽略 hallucination 风险；
- [RAG-E](https://arxiv.org/abs/2601.21803) 与 [Decomposing Retrieval Failure](https://arxiv.org/abs/2602.17981)：retriever–generator interaction/misalignment 说明失败因素不是简单加法恒等式。

### 可守住的新颖性边界

当前 survey 不能支持“RDU 系统组织是空白”或“自然兼容任何闭源 API”。更可信且可检验的空白是：

> 在严格 text-in/audio-in/text-out 黑盒契约、所有组件冻结、知识库与评估标注独立构建的条件下，speech query 的 modality bridge 与生成式 form bridge（doc2query/HyDE）各自贡献多少，它们何时优于 own-ASR→text 和最强简单 RAG？

这是一个较窄但清楚的 frozen speech-RAG 问题。若要保留 TFRL 身份，必须另加 reward-guided selection operator，而不是依赖命名。

---

## 8. 证据账本、时间线与研究诚信判断

### E-1. 已确认的账本冲突

1. `C-MINDS-V2`：ledger 为 `directional`，v4 却写 `valid`；
2. `C-KEEP`：ledger 无该条目，v4 却给出 24% 和 directional 身份；
3. `C-T7`：ledger 为 `invalid` 且禁止作正证据，v4 仍以其方向支撑 recall-first；
4. v4 自己声明只有 `valid/directional` 可引用，却违反自己的规则。

这不是措辞美学，而是证据治理失败。

### E-2. “CLEAN-FOR-REVIEW”不可追溯

对应 commit 的可见变更主要是 proposal 文档，未发现与该 verdict 同步冻结的 checker report、规则版本、输入清单和输出 hash。更重要的是，本轮发现的内部矛盾足以反证它不是 scientific clean certificate。

**整改**：以后 checker verdict 必须附：checker code commit、rule manifest、输入文件 hash、输出 JSON、失败项、执行环境；并把它命名为 internal consistency check，不得等同 external review。

### E-3. 公开确定性 seed 不是 custodian

**FACT**：新脚本支持 CLI `--seed`；manifest 可写入指定目录；固定 seed 与候选池公开时，开发者能在 arm freeze 前算出 confirmatory IDs。Git 只能记录最终提交的 seed，不能证明此前没试过其他 seed。重复运行还可覆盖同名 manifest。

**INFERENCE**：确定性保证 reproducibility，不保证 blindness、unpredictability 或 independence。pairwise disjoint 也不等于未被适应性设计消费。

**必须修复**：

- 使用未参与设计/实现/运行的独立 custodian；
- 在 arm、analysis code、eligibility rules 全冻结后才产生不可预测 randomness；
- 可用 external commit–reveal、离线 secret seed 或加密 ID manifest；
- repo 在解盲前只保存 salted commitment 与 group counts，不保存可推导 ID；
- 禁止任意 `--seed` 覆盖 confirmatory mode，重抽必须 fail-closed 且留下 append-only burn record。

[Reusable Holdout](https://pubmed.ncbi.nlm.nih.gov/26250683/) 的核心问题正是 adaptive reuse 会让 holdout 过拟合；可复算抽样并不能消除开发者提前知道样本后的适应性选择。OSF registration 的价值也在于形成不可修改的 time-stamped frozen record，而不是在本地文件上写“preregistered”标签：[OSF Registrations](https://help.osf.io/article/330-welcome-to-registrations)。

### E-4. 未来日期破坏时间先后证据

**FACT**：本审查时区日期为 2026-07-12；v4 文件及部分 Decision Log/seed 注释写 2026-07-13，但 Git commit 时间为 2026-07-12。所有签字仍为 pending，而 M1 实现已经开始。

**INFERENCE**：未来日期可能只是预制明日文档，不足以证明欺诈；但它使“发生在数据之前”“已外审”“已冻结”的时间顺序不可依赖。如果后续把 07-13 文档称为在 07-12 实现之前完成的 preregistration，将构成虚假 chronology。

**整改**：使用真实 `created_at`、`frozen_at`、`signed_at`、timezone、commit hash 和 immutable registration URI；文件名日期不能替代时间戳。已经写出的 M1 设计决定必须登记为 prior exposure，不得追溯性包装为 pre-data choice。

---

## 9. FFP、QRP 与 honest error 的严格区分

美国 ORI 将 research misconduct 限定为 fabrication、falsification、plagiarism，并要求显著偏离共同实践、故意/明知/鲁莽以及优势证据；诚实错误和意见分歧不属于 research misconduct：[ORI definition](https://ori.hhs.gov/definition-research-misconduct)。本报告依此作如下分类。

### 当前未发现足够证据成立的事项

- **Fabrication**：未发现凭空制造不存在的样本或运行；
- **Falsification**：未发现足以证明作者故意篡改/删除数据或操纵工件；
- **Plagiarism**：本轮没有相关信号，也不是审查中心；
- **全面隐藏负结果**：旧失败、NULL、invalid claim 和审查记录总体仍保留，这是反对“已系统性造假”判断的重要证据。

### 当前可以确认的 QRP / 严重治理缺陷

- 在已知 ledger 状态下升级 `C-MINDS-V2`；
- 用不存在的 `C-KEEP` 支撑主设计；
- 将 composite treatment 叙述为被隔离的 schema/delivery mechanism；
- 从 invalid/leaked `C-T7` 软性回收方向；
- 以 owner/公开 seed 代替独立 custodian；
- 把 15 个章节行当作 15 个统计假设；
- 在签字前实施设计承诺，却保留将来“预注册”语言；
- 把未 live-verified 路由标为 supported；
- 以内部 QA/checker 接近替代外部复现/评审。

### 为什么“再次发生”提高了严重度

首次错误对象、holdout 概念误解、Holm-4 和 Coverage 命名，可以在团队主动保存记录、叫停实验的背景下暂按 honest/sloppy error 解释。但在审查已经明确告知“directional 不得升级、invalid 不得作正证据、custodian 必须独立”之后，同类行为又在 v4 出现。此时仍不能直接推断主观故意，但已经达到**鲁莽证据治理风险**，需要独立人员介入，而不是继续由同一 AI/team 自审闭环。

### 需要正式 integrity inquiry 的条件式触发器

下列任一项一旦发生，应立即启动独立调查；调查触发不等于 FFP 已定罪：

1. 在收到本报告后仍对外称 `C-MINDS-V2 valid`、`C-KEEP minted` 或把 `C-T7` 当正证据；
2. 在“黑盒 API”主臂秘密使用 hidden state、logprob、gold transcript、eval passage ID 或人工标签；
3. 用 eval query/answer/transcript 生成 q2q/HyDE/carrier key/KB，再声称 corpus-independent；
4. 成本表故意漏掉 `m=5` completions，或把 batch request 当成一次生成；
5. 看到结果后缩小 atomic family、切换 Holm/max-T、改变 SESOI/eligibility，且不登记 deviation；
6. 把公开可预测 seed 抽出的样本称为 blinded/independent/fresh；
7. 五轮中只报告第一个正结果，未保留失败轮或未执行 alpha-spending；
8. 使用训练过的 projection/retriever，却仍声称 training-free-by-construction；
9. 把 2026-07-13 的 future-dated 文件追溯性称为 2026-07-12 实现之前的 preregistration；
10. 把当前 review copy 称为具名外部 reviewer 已批准。

---

## 10. 建议替代 proposal

### Proposal A — 先做一个可守住的 fully-frozen speech-RAG 研究

**主问题**：

> 在预先冻结、与评估 query/answer/transcript 独立构建的外部 corpus，以及只暴露 audio/text input 和 text output 的黑盒契约下，全部组件冻结的 speech-RAG 是否能在一个预定焦点数据集上，相对裸核心、own-ASR→BM25/dense、always-retrieval 和最强训练型 retriever reference，取得预先定义且成本可接受的错误下降？在控制 modality bridge 后，doc2query/HyDE 的 form bridge 是否仍提供独立增益？

**最小实验设计**：

1. 一个 focus dataset + 两个 replication datasets；不得依据看到的 baseline/headroom 把任务移出 headline；
2. 主臂严格黑盒；core hidden-state retrieval 只能作为 local-white-box diagnostic；
3. 因子分解：`native-audio vs own-ASR-text` × `raw-doc vs q2q vs HyDE` × `flat vs equal-content-card`；
4. retrieval endpoint 与 end-to-end endpoint 分开；
5. strong baselines 与 RDU 匹配 corpus access、tokens、samples、latency 和调参预算；
6. `standard-card vs flat` 内容、示例、位置和 token 完全相同；
7. 只做一轮 confirmatory；修改系统后必须新 study/new prereg；
8. 主结论限定在实际验证的 core/API/dataset，不写“任意闭源 API 天然可迁移”。

### Proposal B — 若必须保留 TFRL 身份

在 Proposal A 上增加独立的 reward-guided operator：

> 生成 \(K\) 个可部署的 rewrite–retrieve–deliver–answer trajectories；用只依赖黑盒输出和冻结 KB 的可验证 reward 选择；在等预算下对比随机选择、MBR、自一致 medoid 和单次 RDU。

必须冻结：action space、reward、tie-break、budget \(N^*\)、stopping rule、error bound、trust constraint；Lean 证明与 Python selector 对同一对象做 correctness、unconstrained failure 和 constrained convergence/rate。

### Proposal C — 将 S4 独立成 contextual biasing 研究

热词 B-WER 与 general QA-RAG 的构念差异太大。建议独立研究：

> 在不给 gold hotword set 的 deployable 条件下，冻结模型如何从大候选表中检索并使用 entity context；相对 no-context、oracle-list、trained bias retriever 的 B-WER/latency frontier 如何？

这样可以避免用热词结果为一般知识推理背书。

---

## 11. 重开 Stage-2 的强制 checkpoint

以下全部满足前维持 STOP-THE-LINE；不是任选清单。

### P0 — 证据与时间线

- [ ] 发布 v4 勘误：`C-MINDS-V2` 改回 directional/composite；删除 valid 和“已证主导机制”；
- [ ] `C-KEEP` 在正式 artifact provenance + ledger mint 前改为 unverified，数字不得进入 load-bearing rationale；
- [ ] `C-T7` 只保留为失败史；
- [ ] 用真实时间戳更正 future-dated chronology；
- [ ] 把已经实现的 M1 choices 登记为 pre-freeze prior exposure；
- [ ] 明确 v4 是 RAG 新 work、W1 子研究、W4 pivot 或 thesis supersession。

### P1 — 科学对象与接口

- [ ] 选择 strict-black-box 或 local-white-box，禁止混写；
- [ ] pseudo-question 只从 corpus-document source manifest 构建；
- [ ] 50 个随机 value 由独立人员逐项核验 corpus provenance；
- [ ] 明确 audio query 到每个 text-key embedder 的合法 bridge；
- [ ] 真实跨模态模型 live test 完成前状态不得为 supported；
- [ ] q2q/a2a 不再称“同分布”，改为待检验的 form-bridge hypothesis。

### P2 — S3 与成本

- [ ] 删除不可达的 30% call-reduction gate，或改用一次廉价 trigger；
- [ ] always/never/triggered 三臂匹配采样和选择预算；
- [ ] completion、token、latency、GPU-second、$ 全量计费；
- [ ] 中文 K2 使用 CER 并通过 minimal-pair tests；
- [ ] need label 改为 potential-outcome/independent task annotation。

### P3 — 统计冻结

- [ ] 展开 atomic `dataset × endpoint × contrast` hypothesis manifest；
- [ ] 每个 hypothesis 只有一个最终 p-value 与 correction route；
- [ ] focus dataset/replications 在数据前固定；
- [ ] SESOI 由 utility/cost 解释，不随 dev 效果降低；
- [ ] power 与 holdout supply 在签字前完成；
- [ ] 一版本一轮 confirmatory；后续轮为独立 study。

### P4 — Custody 与复现

- [ ] custodian 未参与设计、实现和运行；
- [ ] freeze 后才产生不可预测 seed，repo 解盲前不含可推导 IDs；
- [ ] confirmatory mode 禁止 `--seed` 任意覆盖和 silent overwrite；
- [ ] clean checkout 一键重建 KB/index/metrics；
- [ ] 由真正独立人员完成 clean reproduction；
- [ ] claim ledger、proposal、paper source、README/status 同步，不允许只修最醒目文档。

### P5 — 理论与项目身份

- [ ] 若称 TFRL，明确 reward-guided inference-time operator；否则改名 frozen speech-RAG；
- [ ] Lean correctness + unconstrained failure + constrained convergence/rate；
- [ ] Python↔Lean conformance test；
- [ ] owner、stat reviewer、integrity reviewer、external reviewer 具名签字和 immutable timestamps；
- [ ] 当前 review copy 不得充当自己的 external approval。

---

## 12. 允许继续与立即停止的边界

### 允许继续

- exposed DEV 上的工程搭架；
- synthetic/fake-data unit tests；
- corpus-side value、content hash、archive/refuse-overwrite、retrieval metric 修复；
- 中文 CER、budget accounting、real-model smoke；
- preregistration 草案、novelty matrix 和真正外部审查；
- 不接触 eligibility/confirmatory IDs 的 dry-run。

### 立即停止

- eligibility 或 confirmatory split 的任何消费；
- Phase-B/Stage-2 确认性运行；
- 把 M1 输出写成证据；
- 使用 `valid`、independent reproduction、externally reviewed、untouched、blinded、confirmatory 等升级词；
- 把 ≥10% 写成已观察结果；
- 在未更正成本公式前运行 S3 大规模实验；
- 在未修正 corpus-object interface 前为 `squtr` 批量生成 pseudo-questions；
- 在未明确 work identity 前让 v4 取代 canonical thesis。

---

## 13. 最终审查意见

团队不是“什么都没改”。叫停错误运行、保留负结果、降级旧 holdout、承认 Holm 完整家族、修复重复 contrasts、加强 artifact hash，都是可信的正面动作，也使当前证据不足以支持“已经系统性造假”的指控。

但是，v4 仍然不是可签字 proposal。它把一个尚未证明属于 TFRL 的 speech-RAG 系统写成主线，把白盒 hidden embedding 放进黑盒 headline，把 mathematically impossible 的成本门写成成功标准，并在已经收到审查告知后再次升级证据标签。正在进行的实现也只证明 plumbing 在前进，尚未证明研究对象、指标和 custody 正确。

因此本轮的严格结论是：

> **上一轮回复：部分正确、部分真实整改；v4 科学方案：拒绝；M1 工程：仅限 DEV-only；Stage 2：关闭；FFP：未证实；QRP：已确认；独立诚信监督：现在必要。**

任何后续 AI 都不应把本报告简化为“再补几个 baseline 即可”。重开需要同时修复：研究身份、接口契约、对象 provenance、成本可达性、原子统计族、holdout custody、证据账本和理论—工程同对象。
