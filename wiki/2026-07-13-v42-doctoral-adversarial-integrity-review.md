---
title: "v4.2 博导级对抗审查：科学有效性、当前工程兑现度与研究诚信风险"
date: 2026-07-13
stage: 1-problem-definition
reviewed_object: "2026-07-12-research-proposal-v42-external-review.md"
reviewed_root_commit: "628621a59d61f9ead918ea62787252728d3221fd"
reviewed_w1_commit: "159b5258f2d1d0cb2fec1b0e81dbb5876148e350"
evidence_cutoff: "2026-07-13T07:59:38+08:00"
review_mode: "doctoral hostile review + research-integrity audit + code/artifact verification + literature survey"
verdict: "MAJOR RECONSTRUCTION；NO-GO for M3/M4；不得称 locked/converged/confirmatory-ready"
integrity_verdict: "FFP_NOT_ESTABLISHED；QRP_RISK_HIGH；INDEPENDENT_AUDIT_REQUIRED"
source_preservation: "本轮未修改 proposal、response、代码、数据、实验工件或状态文档；仅新增本日期审查报告"
---

# v4.2 博导级对抗审查

## 0. 一句话结论

**v4.2 比 v4/v4.1 有真实、重要且可验证的进步，但仍不是“收敛与锁定版”，也不是可签署的确证协议。** 它已经把若干旧错误诚实写进正文，却在至少九个 load-bearing 位置仍把“已披露的缺陷”误当成“可接受的设计”。当前正确裁决是：

- 可继续作为 **Stage-1 讨论稿与工程整改清单**；
- **不得进入 M3/M4，不得把公开固定测试称为强确证，不得宣称 M1 已闭合**；
- 在独立审计、语料锁、抽样隔离、estimand 修复与多候选池方差纳入之前，任何正结果只能是 development / fixed-public-benchmark evidence；
- 目前**没有足够证据认定 fabrication/falsification/plagiarism（FFP）**，但存在高密度 QRP、记录不一致与可被利用的选择性通道；如团队在已知这些通道后仍以“强确证、已收敛、零残余”对外报告，性质将从设计缺陷升级为潜在 falsification 风险。

## 1. 审查范围与可复核事实

本轮审查了：

1. v4.2 proposal 全文、附录 A 原子族、缺口表与签字位；
2. 回信 v5、claim ledger、v4.2 internal consistency checker 及其规则清单；
3. W1 的 `159b525` 工程提交，包括 full-corpus builder、五轴审计、deterministic draw、provenance 与测试；
4. 当前磁盘中的 FiQA/`squtr` full-corpus checkpoint；
5. 当前 Lean 文本与 proposal 对理论交付状态的自述；
6. 与 adaptive holdout、随机运行方差、小簇推断、BoN reward hacking、speech/audio RAG、self-consistent error、benchmark contamination 和研究不端定义有关的原始论文或官方规范。

可复核事实：

- 根仓 proposal 首次进入 Git 的时间为 **2026-07-13 01:42:28 +08:00**；文件 frontmatter 日期为 2026-07-12。这不足以证明倒签，但发布记录与文件日期不一致，后续必须增加 `created_at` / `released_at` 双时间字段。
- W1 标准入口实测：`PYTHONPATH=src pytest -q`，**143 passed，3 warnings，167.10 s**。所以 v4.2 §13.4 仍写“现有 4 errors”在发布快照上已经过时。
- v4.2 checker 实测 **12/12 PASS**；但其规则仅覆盖禁用词、必要短语、文件存在、ledger 引用与原子数，不检查统计有效性、语料官方性、抽样隔离、真实实验、理论对象或工程状态。
- 截止 2026-07-13 07:59:38 +08:00，full-corpus checkpoint 为 **29,000 / 57,638 docs，向量形状 `(29000, 1024)`**；构建尚未完成，且 `docs/datasets.lock.json` 尚无 FiQA/squtr corpus lock。
- v4.2 七项签字全部为“待定”；proposal 自己也承认 K-trajectory harness、live cross-modal smoke、corpus lock、REPRODUCE.md、完整 SAP 数值和 operator-linked theory 未交付。

因此，**测试绿是真进步；M1 闭合、科学收敛和确证就绪则不是事实。**

## 2. 多轮对抗式评审

### Round 1 — 最强善意解释（steelman）

团队这轮至少做对了七件事：

1. 不再把 qrels-conditioned 310-doc 库包装成合法确证语料；
2. 明确 U/Û，撤回把一致性信号称为 verifiable reward；
3. 把 K=1 降为低成本基线，并为 selector 增加 equal-K random/MBR；
4. 承认公开固定种子只提供 replayability，不提供 blindness；
5. 把多个旧正结果降为 directional/invalid，并保留失败史；
6. 把泛化边界缩到 headroom-qualified responder cohort，并承认 Q-B 只有单集；
7. 实际修复标准 pytest，开始真实 full-corpus embedding，而不是只写计划。

这些改动说明团队具备自我纠错能力，也解释了为何本报告**不支持直接作 FFP 指控**。

### Round 2 — 方法学攻击（即使所有人完全诚实，结论是否仍会错）

答案仍是“会”。最严重的误差来源不是作者主观诚信，而是设计本身：

- 主张“10% 相对错误下降”，实际检验冻结 dev 基线换算的绝对 margin；proposal 已承认 confirmatory baseline error 较高时会 anti-conservative。
- 只对一次已实现 K-pool 做 item/group bootstrap；生成随机性没有进入 sampling distribution。
- focus 是根据 eligibility headroom 选出的 responder；两个所谓 replication 只是 no-harm，不是正效应复制。
- long-context / own-ASR / strongest RDU ladder 没有进入六个 primary 原子，无法证明收益来自 RDU 设计而不是“多给知识”。
- effective clusters 可能只有 20–45，却要估计 Holm 后约 0.008 的尾部；“BCa 或 bootstrap-t 二选一”仍没有经过设计特定模拟。

### Round 3 — 恶意研究者攻击（如果有人想让结果看起来更好，现制度能否阻止）

不能。无需伪造任何一条数据，仍可利用以下通道获得有利结果：

1. 公开 pool + 公开 seed 可在冻结配置前算出 confirmatory IDs；
2. eligibility/dev 可不带 group manifest，导致同 speaker/session 跨 split；
3. partial group manifest 的缺失 ID 静默退化为 singleton；
4. confirmatory manifest 仍可 `force_supersede`；
5. exclusion paths“非空”即可过门，但代码不能证明它覆盖了**全部** prior exposures；
6. `corpus_mode="full"` 字符串即可让 `query_independent_corpus` PASS；
7. 单次 K-pool 可能碰巧有利；random comparator 自身再加一层随机噪声；
8. 固定绝对 margin 可在 confirmatory baseline error 较高时放松“10% 相对”要求；
9. Q-A 只需一个 responder focus 有正效应，其余两个数据集只需“不明显变坏”；
10. internal checker 12/12 PASS 可被不熟悉范围的人误读为科学有效性通过。

这组攻击说明当前体系是 **transparent but not tamper-resistant, reproducible but not selection-blind**。

### Round 4 — 反向辩护（什么证据足以排除不当操纵）

团队若要反驳上述怀疑，不能再用更多散文，需要交付：

- 冻结前全部人员/AI 的 dataset、query、prompt、metric、seed 暴露清单；
- 由独立方保管的最终 item IDs 或冻结后一次性外部评分；
- group manifest 100% coverage 证明及四 split 的 group-disjoint proof；
- raw candidate pools、server logs、随机种子、解析前输出、失败运行与重试记录；
- 配置选择轨迹：所有尝试过的 prompt、权重、阈值、K、embedder 与放弃理由；
- 至少两名不参与开发者的复跑与签名差异报告；
- 预注册 simulation notebook，证明拟用检验在实际 cluster/ICC/missingness/seed variance 下控制 Type-I。

在这些证据出现前，合理结论是“未证实操纵，也未建立足以排除选择性操纵的制度”。

### Round 5 — 博士论文价值攻击

speech/audio RAG 已有直接竞争线：WavRAG 原生音频检索、VoxRAG transcription-free spoken QA、PlanRAG-Audio 的规划式检索，以及 contextual ASR 的 RECAST。故“冻结模型 + RAG + 多样本选择”本身不足以成为博士级新颖性。[WavRAG](https://aclanthology.org/2025.acl-long.613/)、[VoxRAG](https://aclanthology.org/2025.magmar-1.3/)、[PlanRAG-Audio](https://aclanthology.org/2026.findings-acl.1304/)、[RECAST](https://aclanthology.org/2025.findings-emnlp.203/)

本工作真正可能守住的贡献只能是以下合取之一：

- 严格黑盒、全语料下，RDU **超过 strongest long-context 与 own-ASR cascade**；
- label-free selector 在 equal-K 下跨数据集稳定超过 random/MBR，并量化实现 oracle headroom 的比例；
- 对 imperfect proxy 的 over-optimization 给出可测、可证、与 Python 同对象的 pessimistic/abstaining selector；
- 给出公开语音 benchmark 上 q2q 生成桥接的污染审计与跨模态因果分解。

v4.2 当前没有把任何一个上述条件设成足够强的 load-bearing gate，所以博士价值仍未建立。

## 3. FUNDAMENTAL findings

### F-1：主 estimand 与检验对象不一致，且团队已知其可能偏松

**证据**：§3.1/§9.3/附录 A 把主 estimand 写为“相对错误率下降”，但用冻结 dev bare error 生成固定 `SESOI_abs`；同时承认 confirmatory bare error 更高时对“10% 相对”主张 anti-conservative。

**裁决**：不可接受。敏感性分析不能挽救 primary estimand mismatch。一个已知可能偏松的 surrogate 不能作为同一 headline 的确证检验。

**必须二选一**：

1. headline 改成“绝对错误率下降超过预注册固定 margin”，并停止写“10% 相对”；或
2. 直接检验 aggregate paired relative error reduction，联合重采样分子与分母，并为近零分母和 baseline drift 预注册处理。

**关闭证据**：模拟覆盖率 + machine-readable estimand + analysis code golden test 三者一致。

### F-2：所谓 pre-M2 SESOI 冻结在时间上已不可能成立

**证据**：签字位仍待定，但项目已经有 C-ASR-V2 selector battery、MBR/random/logprob 等 dev 结果；正文又要求 Q-B SESOI 在“任何 selector dev 观测前”冻结。

**裁决**：不能通过重新命名当前阶段抹去已知信息。SESOI 现在设定只能称 **post-observation but externally justified**，不能称 blind/pre-observation。

**修复**：建立完整 prior-exposure register；由未接触效应值的独立统计人员根据外部 utility/文献设定 SESOI；若做不到，则用一套真正新数据作确证，现有公开数据永久留作 development。

### F-3：public deterministic evaluation 不能保留强 confirmatory 等级

§9.8 已准确承认 public seed、public pool 使 final IDs 在配置冻结前可知，却在 §13.3 保留 M4 confirmatory 等级。这个推论不成立。

单一最终版本只控制“重复开火”类 Type-I，不控制同一版本内对已知 final items 的自适应选择。adaptive holdout 文献明确指出，复用或适应性地选择分析会对 holdout 本身过拟合。[Dwork et al., NeurIPS 2015](https://proceedings.neurips.cc/paper/2015/hash/bad5f33780c42f2588878a9d07405083-Abstract.html)

**硬裁决**：

- 第三方冻结后一次性评分进入 M4，才可使用 confirmatory；或
- owner 拒绝独立评分，则名称必须降为 `preregistered fixed-public-benchmark evaluation`，证据等级不高于强 development / quasi-confirmatory。

“发表前届时再定”太晚，因为 M4 的科学解释已在当时形成。

### F-4：单次 K-generation 条件推断遗漏了方法本身的随机性

附录 A 明确承认 CI 仅条件于一次 K-pool，并把多 pool 设为“可选”。对一个以随机采样产生候选的 selector，这不是可选局限，而是 estimand 的组成部分。

RL 评测文献已经反复说明少量随机运行会造成严重统计不确定性；不能用只重采样 task items 的 CI 代替算法运行方差。[Henderson et al.](https://arxiv.org/abs/1709.06560)、[Agarwal et al., NeurIPS 2021](https://proceedings.neurips.cc/paper/2021/hash/f514cec81cb148559cf475e7426eed5e-Abstract.html)

**修复**：每个 item/group 至少 3–5 个独立 K-pool seeds；外层重采样 group，内层重采样 generation replicate；同时报告 conditional-on-pool 与 marginal-over-generation 两个 estimand。若预算不允许，只能把结论严格限定为该固定 pool，不能主张部署期 selector superiority。

### F-5：Q-A 没有 load-bearing strongest-baseline gate

§3.1 说复杂度阶梯“并列裁定”，但附录 A 六原子与 §13.2 合成逻辑中没有 long-context、own-ASR cascade 或 RDU-vs-strongest 的 primary 原子。

这意味着系统可以只因“给了更多知识”击败 bare core，即使 RDU 不优于简单全塞或 ASR-text RAG，仍通过 headline。对已有 WavRAG/PlanRAG/RECAST 文献背景，这不足以证明研究设计贡献。

**修复**：增加或替换为 `H_RDU_VS_STRONGEST`；strongest baseline 在 dev 中按预注册规则从 long-context、own-ASR text-RAG、frozen trained retriever 中选出；RDU 必须在预算/上下文长度明确的可比条件下越过 SESOI。若担心 m 增大，应删去弱价值原子，而不是把关键归因降为散文。

### F-6：full-corpus audit 目前由模式字符串自证，不符合 proposal 自己的门

当前实现中：

- `query_independent_corpus = PASS iff corpus_mode == "full"`；
- builder 调用 `revision=None`；
- 未断言 `doc_count==57,638`；
- 未与预注册 upstream revision/checksum/content hash 比对；
- `docs/datasets.lock.json` 没有 FiQA/squtr corpus lock。

因此一个不完整、替换过或错误来源的 `corpus.jsonl` 仍可被标成 query-independent。当前 29,000-doc checkpoint 证明真实构建在进行，但不证明 officialness 或完整性。

**修复**：在 embedding 前先验证 upstream archive revision/hash；在完成时验证 ordered doc-ID hash、content hash、doc count；所有不匹配 fail-closed；audit 读取证据工件，不读取调用者布尔值或 mode 名称。

### F-7：`answer_presence_expected` 的代码语义与 open-corpus 任务定义相反

proposal 正确指出：合法开放语料中答案 span 自然出现不是泄漏；泄漏是 test qrels/answers 决定 corpus/index/prompt/candidates。当前 builder 却把 downstream `eval_golds` 交给 `scrub=True`，并以 scrub 后 CLEAN 判断该轴 PASS。

这会删除合法证据，改变研究任务，且把“答案存在是预期”实现成“答案必须被清除”。

**修复**：

- open-corpus：不 scrub 合法答案；审计 build inputs 与 qrels/query/answer 路径、doc-selection independence；
- per-item injected context：单独 fail；
- `answer_presence_expected` 只报告描述性 overlap，不作为删除内容的理由；
- 用含合法 answer span 的正向 golden test 和 per-item injected context 的负向 golden test。

### F-8：group-aware draw 仍有三条可利用的隔离漏洞

当前代码：

1. eligibility/exploration 缺 group manifest 只 warning；
2. group manifest 缺失 item 时静默 `gid=iid` singleton；
3. confirmatory 只要求 exclusion manifest path 列表非空，无法证明它是 exposure union 全集；`force_supersede` 对 confirmatory 仍可用。

此外，manifest 没有 group-manifest hash 与明确 exclusion-definition hash。代码头部还保留“fixed seed equally tamper-evident”的错误表述，与 v4.2 对 blindness 的承认冲突。

**修复**：四 split 全部 hard-require 100% group coverage；missing group ID 即 error；按 group union 排除而不只按 item ID；exposure registry 枚举所有 prior manifests 并由状态机验证齐全；confirmatory 禁 `force_supersede`；写入 group/pool/exclusion/code hashes。

### F-9：一次性 M4 状态机在正文内部自相矛盾

§9.5、§13.2 与 DAG 写 M4 fail 后终局；但 §13.3 的 M5 又写“不达标→development 迭代或 owner 复盘”。这给“失败后迭代”留下文本授权口。

**修复**：用 machine-readable state machine：

```yaml
states: [M1, M2, M3, M4_UNFIRED, M4_PASS, M4_FAIL_FINAL]
allowed_transitions:
  M2: [M2, M3]
  M3: [M2, M4_UNFIRED]
  M4_UNFIRED: [M4_PASS, M4_FAIL_FINAL]
  M4_PASS: []
  M4_FAIL_FINAL: []
```

任何新数据复制必须是新 program ID，不能复用原 family、seed 或 confirmatory label。

### F-10：理论“正确命名”已有进步，但仍没有博士级 load-bearing theorem

v4.2 §10.2 已诚实承认 `U(τ*)−U(τhat)≤2ε` 是 generic argmax mismatch，不是收敛。真正第二定理依赖 `ε_n→0`，但尚未定义：

- n 是 verifier samples、calibration items，还是候选池 K；
- Û_n 如何更新；
- 对 adaptive candidate set 的 uniform high-probability bound 如何获得；
- dataset/core shift 下 ε 如何保持；
- Python selector 与 Lean 对象的逐例一致性。

如果只假设 `ε_n→0` 再推出 regret→0，理论价值接近把结论写入前提。BoN 文献真正困难处在 imperfect reward 与 coverage/tail/over-optimization 的约束，而非二行 argmax bound。[Huang et al., 2025](https://arxiv.org/abs/2503.21878)

**修复**：证明 finite-sample `ε(n,δ,complexity)`，再推出 regret bound；或实现 uncertainty set / pessimistic selector，使约束对应工程算法。否则删除“理论贡献”，仅把 Lean lemma 作为实现审计。

## 4. MAJOR findings

### M-1：两个 no-harm 原子不是正向复制

团队自己承认 non-inferiority 下受益和平凡无害都可通过。因此“1 个正效应 focus + 2 个 no-harm”不能称多数据集效果复制。至少一个预定外部数据集必须通过正向 SESOI，或把 headline 明确改成单数据集 case study。

### M-2：Q-B 只有单数据集，不能支撑一般 TFRL 身份价值

“算法身份”可以由定义成立，但“selector 有科学价值”不能靠一个 responder focus。至少要求一个不同任务族或不同核心的正向 equal-K replication；否则只能说“在 `<FOCUS>` 上观测到 selector effect”。

### M-3：random comparator 应使用条件期望，不应再抽一次幸运 random index

给定同一 K-pool，random-pick 的条件期望真效用就是 K 个候选 U 的均值。用一次 seeded random pick 会给 comparator 添加无意义 Monte Carlo 方差。primary 可直接比较 selector U 与 pool mean-U；另保留随机实际抽取作部署模拟。

### M-4：同权重异 prompt 不能承担“跨源”独立性

proposal 已承认它不是 weight-independent，但仍把它纳入核心 proxy。Self-consistent error 文献显示同一模型可稳定重复相同错误，改 prompt 不能被预设为独立证据；相关工作反而使用 cross-model probe。[Too Consistent to Detect](https://aclanthology.org/2025.emnlp-main.238/)

要求预注册 error-correlation/conditional mutual information；达不到阈值则删除该信号或换独立模型。CISC 也指出跨问题 calibration 与同题排序能力不同，v4.2 的 within-question 诊断方向正确，但必须真实测量后才能进入 selector。[CISC](https://aclanthology.org/2025.findings-acl.1030/)

### M-5：小簇尾部推断仍未被证成

BCa/bootstrap-t 比 naïve percentile 更合理，但 20–45 clusters、非均衡 group、离散 endpoint、Holm 极端尾部下仍需 simulation。经典研究显示少簇时标准方法可能过度拒绝，wild cluster bootstrap-t 可改善但也依赖设计条件。[Cameron, Gelbach & Miller, 2008](https://doi.org/10.1162/rest.90.3.414)

要求至少比较：studentized cluster bootstrap、wild cluster bootstrap、cluster-level randomization/sign-flip（若其 exchangeability 条件成立）；以 Type-I、coverage、power 决定最终方法，而不是凭方法名称选择。

### M-6：配置选择自由度远大于当前 multiplicity 账本

modality × form × delivery × selector weights × K × threshold × embedder × prompts 的 dev winner 被称为 `best_frozen_rdu`。独立 test 可以保护 final test，但 public IDs 又破坏了这一保护。必须输出完整 search space、所有尝试结果与 selection rule，避免只保存赢家。

### M-7：q2q 还有“预训练记忆回生 test query”盲点

即使 build script 不读取 query 文件，生成 q2q 的公开预训练模型可能在训练中见过 benchmark queries，并从文档回生高度相似问题。LLM benchmark contamination 可跨表面转换或语言边界，不能只做 exact path audit。[Yao et al., EMNLP 2024](https://aclanthology.org/2024.emnlp-main.990/)、[Balloccu et al., EACL 2024](https://aclanthology.org/2024.eacl-long.5/)

要求在规则冻结后做 exact/fuzzy/semantic query-overlap audit，报告分布而非事后按结果调阈值；q2q 与 raw-doc/q2a 必须同时保留。

### M-8：工程提交与发布文字没有事务一致

W1 `159b525` 在 root `628621a` 前已使标准测试 143 passed，但 v4.2 同次发布仍写“现有 4 errors”。反过来，commit subject 写“converged（2 rounds, 0 residual）”，而同一 proposal 明列 K-harness、live smoke、lock、REPRODUCE、完整 audit 等未完成。

这更像发布快照协调失败，而不是有利方向的数据造假；但它足以否决“lock/converged”。今后 release manifest 必须列各 repo SHA，并由脚本从该 SHA fresh checkout 重建状态表。

### M-9：conformance checker 通过不等于 proposal 自洽

12 条规则未检查 F-1 至 F-10 中任何核心问题。checker 的 scope disclaimer 是诚实的，但“12/12 PASS”不应出现在没有相邻限定语的管理汇报中。应新增 semantic rules，并把人工/独立审查结果与机械 lint 分栏。

## 5. 研究诚信裁决

### 5.1 为什么现在不能指控“学术欺诈已成立”

按 ORI 定义，research misconduct 主要指 fabrication、falsification 或 plagiarism；还需显著偏离规范，并达到故意、明知或鲁莽等证明门槛。诚实错误和意见差异不自动构成 misconduct。[ORI 定义](https://ori.hhs.gov/definition-research-misconduct)、[ORI Federal Policy](https://ori.hhs.gov/content/chapter-2-research-misconduct-federal-policies)

本轮看到的反证包括：

- 团队公开撤回旧措辞与旧 invalid claims；
- proposal 明列大量未交付项和 contested owner ruling；
- pytest 结果可真实复跑；
- full-corpus checkpoint 确实存在并在构建；
- 没发现凭空编造的 confirmatory result，因为当前根本还没有 M4 结果。

因此当前 FFP 裁决必须是 **NOT ESTABLISHED**，不能越权写成“有罪”。

### 5.2 为什么仍必须按高风险完整性事件处理

以下组合达到 QRP-HIGH：

- 过去已有 gold/transductive/object-mismatch 假增益史；
- 公开 final IDs 可预测；
- 关键门由调用者 flag 自证；
- 数据随机性被条件化掉；
- 记录与提交状态不一致；
- 独立监督被 owner 明确推迟；
- 标题/commit 使用“锁定、收敛、零残余”，证据却尚未闭合。

若这些问题在知情后仍被省略，或把不利 runs / seeds / configs 排除而不披露，可能触及 falsification 中“改变或省略数据/结果，使研究记录不能准确反映研究”的风险边界。现在应做的是保全证据、独立审计和纠偏，而不是先给个人定罪。

## 6. 严格改进计划（给研究团队 AI 的可执行规格）

### P0 — 立即执行，继续任何 data-sensitive dev 前

```yaml
gate_id: P0_INTEGRITY_FREEZE
allowed_work:
  - corpus embedding and non-data-sensitive engineering
  - unit tests and documentation of prior exposure
forbidden_work:
  - selector weight/SESOI/threshold tuning on any known final items
  - M3 signature
  - M4 execution
required_artifacts:
  - prior_exposure_registry.json
  - experiment_attempt_registry.jsonl
  - discrepancy_register.md
  - release_manifest.json
  - append_only_erratum_for_v42.md
pass_conditions:
  - all existing datasets, groups, prompts, outputs, seeds and metrics exposures enumerated
  - v4.2 labeled DRAFT / NOT LOCKED / NOT PREREGISTERED
  - independent reviewer receives read-only artifact snapshot
```

### P1 — 语料、KB 与 provenance

```yaml
gate_id: P1_CORPUS_INDEPENDENCE
requirements:
  - upstream dataset revision + archive sha256 + public doc_count pinned
  - local ordered_doc_id_hash + normalized_content_hash pinned
  - builder asserts every registered value before embedding and before persist
  - qrels/query/answer files absent from build-input manifest
  - q2q input manifest contains corpus documents only
  - open-corpus answer spans are not scrubbed
  - per-item injected gold context hard-fails
  - five audit axes derived from evidence, never from mode strings/booleans alone
  - incomplete checkpoint cannot be persisted as full source
tests:
  - altered corpus under corpus_mode=full must fail
  - 57,637 and 57,639 docs must fail
  - legal answer-containing document must remain unchanged
  - injected per-item gold context must fail
  - qrels path alias/symlink in build inputs must fail
closure_evidence:
  - fresh full build report with hashes, count, upstream anchor and retrieval smoke
```

### P2 — 抽样隔离与 custody

```yaml
gate_id: P2_SPLIT_AND_CUSTODY
requirements:
  - group_manifest coverage == 100% for all four splits
  - missing/duplicate/unknown group key == hard error
  - exclusions operate on complete group union
  - canonical exposure registry proves all previous manifests included
  - manifest contains pool_hash, group_hash, exclusion_hash, code_sha
  - confirmatory write is create-once; force_supersede forbidden
  - M4 IDs unavailable to developers until code/config/SAP freeze
alternatives:
  blinded_confirmatory:
    - third_party_one_shot_scoring
  public_mode:
    - downgrade label to fixed-public-benchmark evaluation
```

### P3 — SAP 重写

```yaml
gate_id: P3_STATISTICAL_PREREGISTRATION
primary_system_atoms:
  - RDU_vs_bare_on_focus
  - RDU_vs_strongest_practical_baseline_on_focus
  - positive_effect_replication_on_predeclared_second_dataset
primary_selector_atoms:
  - selector_vs_pool_mean_random_expectation_equal_K
  - selector_vs_MBR_equal_K
  - selector_positive_replication_on_second_dataset_or_core
mandatory_design:
  generation_replicates_per_group: ">=3; target 5 after power/cost simulation"
  outer_resampling_unit: group
  inner_variation: independent_K_pool_seed
  report_both:
    - conditional_on_pool_effect
    - marginal_over_generation_effect
estimand_rule:
  - either test relative error reduction directly
  - or rename claim to fixed absolute improvement
  - never use an anti-conservative surrogate under a relative headline
method_selection:
  - simulate actual cluster sizes, ICC, discreteness, missingness and seed variance
  - compare studentized cluster bootstrap, wild cluster bootstrap and valid randomization alternatives
  - freeze method before final data
SESOI_rule:
  - disclose all previous effect observations
  - derive from utility/external literature, not observed winner
  - if blindness impossible, require fresh external confirmatory data
```

### P4 — selector 与 Goodhart 探索

```yaml
gate_id: P4_SELECTOR_VALIDITY
diagnostics:
  - within-question pairwise ranking accuracy/AUROC with cluster CI
  - self-consistent-error subset sensitivity
  - true-U vs proxy-Uhat curve across K and pool seeds
  - proxy error correlation across prompt/model sources
  - abstention/selective-risk curve
required_baselines:
  - pool mean random expectation
  - MBR with frozen distance normalization
  - verbal confidence only
  - self-consistency only
  - independent-model score if license/budget permits
  - pessimistic lower-confidence selector
failure_routes:
  - proxy uninformative: publish negative mechanism result; do not relabel selector success
  - U declines while Uhat rises: freeze N below pre-registered turning-point rule or use pessimistic selector
```

### P5 — 理论轨

```yaml
gate_id: P5_THEORY_DUAL_TRACK
must_define:
  - stochastic process indexed by n
  - how Uhat_n is estimated/updated
  - finite-sample epsilon(n, delta, complexity)
  - candidate-set adaptivity and distribution-shift assumptions
must_prove:
  - unconstrained counterexample for the same Python selector
  - constrained finite-sample correctness/regret
  - convergence under a measurable epsilon_n_to_zero mechanism
  - failure when the key constraint is violated
conformance:
  - Python-Lean golden cases including ties, early stopping, K cap and abstention
fallback:
  - if only generic 2epsilon lemma remains, classify as verification infrastructure, not novel theory
```

### P6 — 独立复核与发布

```yaml
gate_id: P6_INDEPENDENT_REVIEW
reviewers:
  - statistics reviewer not involved in model/config development
  - data/provenance reviewer with read-only raw artifact access
  - reproduction reviewer running from clean checkout
required_outputs:
  - signed discrepancy disposition table
  - fresh-checkout reproduction log
  - raw-to-table trace for every headline number
  - all negative/failed runs index
  - final claim-to-evidence matrix
promotion_rule:
  Stage_1_to_Stage_2: owner decision after P0-P3 design gates, not after a favorable result
  M4: only after P0-P6 applicable pre-run gates pass
```

## 7. 建议新增的 proposal 探索方向

这些方向不是“多做几个 ablation”，而是能把当前普通 RAG+BoN 方案提升成可守研究贡献的候选：

1. **Pessimistic selector**：不选最高 Û，而选 `LCB(U)=Û−uncertainty`; 检验其是否消除 K 增大时的 reward hacking。该方向与近期 BoN 理论直接对话。
2. **Abstaining selector**：当 top-1/top-2 proxy gap 或跨源一致不足时退回 greedy/MBR；主指标改为 risk–coverage 曲线。
3. **Generation-robust realization**：把“oracle 头空实现率”定义为跨 K-pool seeds 的期望与下分位数，而不是单池 rho。
4. **Contamination-resistant q2q**：比较 raw-doc、q2q、a2a，并将 test-query semantic overlap 作为预注册诊断；研究 form bridge 的收益是否来自 benchmark question 回生。
5. **Cross-model error decorrelation**：系统测量同模型异 prompt、不同模型、不同模态 verifier 的错误相关，而不是预设“cross-source”。
6. **Budget-normalized frontier**：报告质量–延迟–token–检索调用四维 frontier；不设商业成功门，但必须阻止靠无限 K 赢。
7. **真正的强基线因果分解**：bare → long-context → own-ASR text-RAG → native audio retrieval → full RDU → RDU+selector，每级都有固定新增资源与可解释净增益。
8. **跨集 selector transfer**：在 dataset A 标定 proxy 权重，零调参迁移到 dataset B/core B；这比在 responder focus 内调优更能建立 training-free selector 的一般价值。

## 8. 最终决策表

| 项目 | 当前裁决 | 允许的下一步 | 禁止事项 |
|---|---|---|---|
| Stage-1 问题定义 | 可继续讨论，但未锁定 | 按 P0–P3 重构 | 自动滚入 Stage-2 |
| M1 工程 | PARTIAL | 完成 full corpus、lock、live smoke、K harness、sampling gates | 宣称 M1 green |
| v4.2 SAP | REJECT | 重写 estimand、replication、seed variance、strong baseline | M3 签字 |
| public deterministic eval | replayable only | 第三方评分或降级证据名称 | 称 blinded confirmatory |
| selector/TFRL | hypothesis-grade | equal-K、多 pool、多集复制 | 单池单集泛化 |
| theory | baseline lemma only | 有限样本 ε 与同对象收敛 | 称 convergence delivered |
| integrity | FFP 未成立；QRP 高风险 | 独立审计、证据保全、差异登记 | 无证据定罪或无审计放行 |
| publication | NO-GO | 先完成独立复核与新数据确证 | 用当前 directional/invalid 结果作头条 |

## 9. 给 owner 的最短决策建议

请不要在“相信团队”与“指控造假”之间二选一。正确治理动作是：

1. **不认定 FFP，但立刻启动独立完整性审计；**
2. **允许 full-corpus 等非数据敏感工程继续，暂停所有会改变 SESOI、selector、prompt 和 final config 的 data-sensitive 决策；**
3. **把 v4.2 降为 draft，撤销“收敛与锁定”管理含义；**
4. **若 owner 坚持公开固定 final IDs，就主动放弃强 confirmatory 名称；**
5. **只有当 RDU 超过 strongest baseline、selector 跨 pool/跨集成立、语料与抽样门机器闭合时，才讨论 Stage-2。**

这是对团队最严厉、也最公平的结论：**现有记录尚不足以证明造假，但已经足以证明不能再靠内部自述、命名收敛和单次可复跑来换取科学可信度。**
