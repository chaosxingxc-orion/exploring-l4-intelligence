# 2026-07-08 · 三个技术锚点的批判性审计（Stage-1 反思，append-only 再定级）

> **性质**：Stage-1 论证文档。对 owner 于 2026-07-08 提出的三个技术锚点做对抗性审计——
> 逐锚点核对"声称 vs 记录在案的证据"，并清点"自以为满足信息约束但实际未达成"的情形。
> **证据基础**：两路独立代码/文档审计（W1 仓库逐行核查 + umbrella wiki/proofs 盘点），
> 所有判定核对到 path:line 或 commit。本文档只做再定级与勘误，不改写任何历史记录。

## 0. 三个锚点（owner 表述）

- **A1（知识组织形式）**：多模态知识以「语音向量为 key、异构信息源为 value」组织。
- **A2（理论锚点）**：已从理论上证明——扩展 frozen 模型能力边界最有效的方式不是 rollout
  （over-confidence 问题），而是外接能力源动态加载 few-shot 知识/能力。
- **A3（实验底座）**：锁定一组本地已下载、可复现、无信息泄露的数据集与脚本，
  且与后期大规模实验工程同基座。

## 1. A1 判定：**设计夯实，验证未夯实（半夯实）**

**成立的部分。** 设计 owner-LOCKED（`wiki/2026-07-05-omni-multimodal-memory-design.md`）且与
声称一致：key = 统一压缩语音嵌入、value = 异构外部知识 dict。工程管道成形并已入 W1 版本控制
（`scripts/knowledge/`：kb_schema/build/index/retrieve/audit/snapshot，commit b97d12c），
query-space 正确性修复真实（commit 0c74d17：查询侧 embedder 从 manifest 回读 build-time
embedder，杜绝 key/query 空间错配；`auto` 不再静默降级）。检索 = FAISS IndexFlatIP 上 L2 归一
cosine top-k，键/查询归一化一致（`kb_index.py:36-52`）。

**未夯实的部分（五个洞）。**

1. **唯一端到端验证是 logmel-stats 冒烟键的恒等往返**（`kb_poc.py:54-75`：同一音频既做 key 又做
   query，self-retrieval@1=1.0）——验证的是持久化管道，**不是语义检索质量**。CLAP / omni-embed
   从未建过真库、查过真库（无 committed 证据）。"组织形式有效"目前是零语义证据状态。
2. **omni-embed-nemotron-3b 路径实际未接通**：`kb_embed.py:60-70` 把 wav *路径*喂给
   `SentenceTransformer.encode`（期望文本），docstring 自注 "loader wiring is model-specific"。
   名义上的 Stage-2 键是纸面的。
3. **唯一接通的真嵌入器 CLAP（`laion/clap-htsat-unfused`）是 audio-event 模型**，对语音词汇内容
   的表达能力存疑——而主任务族（spoken-QA/SLU）恰是内容型。key 空间与任务族可能系统性错配
   （→ 2025+ 语音向量化调研的先决问题，见 §5）。
4. **Value 只覆盖 knowledge 粒度**（`kb_schema.py:33`：transcript/translation/labels/intent/
   answer/text-fact/other-modal 的原始字符串）。按已锁定的能力分类学
   （`wiki/2026-07-06-capability-taxonomy-knowledge-skill-memory.md`），instance-recall
   **memory** 与 task-template **skill** 两个粒度未触及——ASR 困难样本记忆正属前者。
5. **历史包袱已在记录中自纠但须持续注意**：该设计曾被误标为 "memory"（2026-07-06 分类学再定级）；
   其最初经验支撑（T7 RAG 增益）因泄露作废，boundary-clean 重跑为 null（见 §3）。
   另有 latent bug：`kb_audit.audit_source` 引用已不存在的 `KnowledgeEntry`/`entries.jsonl`
   schema（`kb_audit.py:71-81`，本日修复中）；KB 工件本体（E:\speechrl-knowledge）不在版本控制。

## 2. A2 判定：**未夯实——"从理论上证明了"不成立（三锚点中最大缺口）**

**真正已证的（sorry-free，除 `BestOfN.lean:90` 一处披露的 Beirami sorry）：**
- **read-out 上界**：`InfoBoundary.lean` 的 `readout_acc_le_oracle` / `readout_error_ge_gap`
  —— rollout/选择不能超出自身样本、在知识缺口上必然失败。这是"rollout 有上限"的合法内核。
- `realized_gap_le_two_tau`（`Realization.lean`）：泛型 argmax 失配 2τ 界（对任何 selector 成立，
  不特指 rollout，也不建模 calibration）。
- `BestOfNConvergence.lean` / `Iterate.lean`：**τ→0 / δ>0 假设下**的受约束收敛 squeeze 与
  无约束不收敛对偶。
- `gain_product`（孤立组合无增益）、`too_improbable_unreachable`（条件化重加权上限）。

**没有证的：**
- "外接能力源可跨越能力边界"对应的 `newinfo_can_cross_gap`（`InfoBoundary.lean`）与
  `external_element_can_escape`（`AgenticElements.lean`）是 `Fin 1 → Bool` 上的平凡 ∃ 见证，
  **仓库自评 FRAMING-ONLY / tautology**（`wiki/2026-07-07-knowledge-proof-honest-accounting-
  and-feasibility.md` §1.1；定理 docstring 明令 "Do not cite it as evidence that knowledge
  injection works"）。
- 收敛定理的 load-bearing 前件 τ→0 是**假设不是推导**——honest-accounting §1.2 的原话是
  "convergence-by-assumed-bound, not convergence of a real system"，且经验上 τ 大
  （反事实采纳率仅 ~24%），定理对部署系统 vacuous。
- **over-confidence 从头到尾只是 τ 的经验注解**（`Realization.lean` docstring），不是定理，
  更没有"rollout 因 over-confidence 而次优于外接源"的任何形式化比较。

**记录内已两次收回强形式**：(a) "只有外接元素能抬 ceiling" 经五人格评审降为契约相对
（对比解码等合约内杠杆也能，Decision-Log 2026-07-06 later）；(b) `gain_product` 曾被过度
泛化为"agent 组合无用"（Q1 评审勘误）。文档夸大有前科（"C1/C2 all green" 曾被收回、
commit 8298846 假声称 verified）——**一切 "Lean-locked" 声称必须对 committed tree 核验**。

**经验面同样不支持朴素版 A2**：boundary-clean 后外部知识注入的增益为 null
（T8 clean_H0 = −0.066, CI [−0.167, 0.033]），frozen 模型 parametric stubbornness 显著；
幸存的正向线索是**交付形式**（T10：2-turn tool 使反事实采纳 0.175→0.35）与
**感知-delta**（p6：SQuAD-zh +0.283 SIG，但 3 数据集仅 1 显著、无多重比较校正）。

**再定级提案（呈 owner 确认）**：A2 的诚实表述是——
> 已证 rollout 的 read-out 上界（机器检查）＋ 一个 **Stage-2 定理目标**
> （τ*>0 邻域收敛 + N* 预算约束，honest-accounting §2.4 判 FEASIBLE）＋
> 方向性经验证据（交付形式 > 注入内容本身）。**不是已证结果。**

## 3. A3 判定：**三锚点中最扎实，但有五根刺**

**成立的部分。** 28 数据集 + 6 模型 frozen lock（`docs/datasets.lock.json`，revision-pinned，
~441 GB），单一下载器 `scripts/data/fetch-data.sh`，候选集分离（datasets.candidates.json 不入
lock）。全部 T 系列脚本共用 llama.cpp server + Qwen3-Omni-30B Q8 GGUF + 共享 p2 harness
（数据切片与打分跨实验一致）；结果 JSON 落库且全带 `1-directional` 标签；泄露护栏是**机器实现**
（`kb_audit.audit_texts` + `scrub_golds`，build 时自动跑并写入 manifest），且**抓住过真泄露**
（T7 → t7_leakage_audit 量化 → T8 清洗归零）。`wiki/Information-Boundary-Guard.md` 在 umbrella
wiki 中存在（W1 代码的跨仓库引用有效）。

**五根刺：**

1. **T7 结果 JSON 的 boundary 字段写 "answers never injected"，而注入的 context 段落内含 gold
   answer**（answer_in_own_KB≈1.0）——gold *字段*确实没注入，但 gold *字符串*就在注入文本里。
   标签误导，属"自以为满足信息约束但实际未达成"的活例（→ 本日已加 errata sibling 注记，
   原 JSON 按 append-only 纪律不改）。
2. **泄露审计只查 verbatim/substring 重叠**（NFKC-lower-alnum 后子串匹配，`kb_audit.py:21-52`）
   ——paraphrase/部分重构/可推答案检不出；T8 清洗后残留 1.7%。护栏是必要非充分。
3. **item-id 冻结（kb_snapshot）只有 kb_poc 在用**；T0/T7–T10/p6 全靠 seed + parquet 行序
   permutation，行序一变即漂移，committed 结果无 sample_manifest。可复现性是"弱意义"的。
4. **"同基座"声称与仓库现实脱节**：真实证据全部来自 Qwen3-Omni-30B GGUF + llama.cpp 栈；
   仓库名义 scale-up 路径（Hydra `src/training_free_rl/main.py` stub + configs）指向
   **Qwen2-Audio-7B + GRPO + librispeech**，两者之间无映射文档。KB 侧倒有扩展路径
   （`scripts/knowledge/DESIGN.md` §4：flat→HNSW→IVF-PQ/托管库）。
5. **目标 regime 无外部可比 baseline**：38-work 对齐综述判
   `{audio-native ∩ training-free ∩ local-mapped}` = EMPTY——"可复现"的是自家脚本，
   "可比较"的对象尚不存在，clean fact-gap testbed 是 Stage-2 前置。

**其他勘误**：p6 感知-delta 三数据集无多重比较校正（3 中 1 显著，SIG 判读应保守）；
T9/T10 反事实 A′ 取自测试集 gold 池（轻度标签空间泄露，不影响其 boundary-clean 判定但应记录）。

## 4. "自以为满足信息约束但实际未达成"清单（合并去重）

| # | 情形 | 位置 | 状态 |
|---|---|---|---|
| 1 | T7 boundary 标签宣称无答案注入，注入 context 实含 gold | `_repro/t7_rag_gate_probe.json` | errata 注记（本日） |
| 2 | 泄露审计 verbatim-only，paraphrase 盲区（实测残留 1.7%） | `kb_audit.py:21-52` | 记录在案，改进待定 |
| 3 | 可复现性依赖 parquet 行序而非 item-id manifest | T0/T7–T10/p6 全部 | 今后跑法必须走 kb_snapshot |
| 4 | p6 无多重比较校正即报 SIG | `_repro/p6_perception_delta.json` | 判读降级为"方向性" |
| 5 | 反事实 A′ 取自测试集 gold 池 | t9/t10 | 记录在案，低危 |
| 6 | "同基座"声称无工程映射支撑 | Hydra stub vs T 脚本 | 待 scale-up 规划时消解 |

## 5. Owner 决定（2026-07-08）与下一步

1. **本审计先记录并同步**（本文档 + Decision-Log + wiki-sync）。
2. **充分调研先行、规划后置**：先充分调研 **2025-01 之后**的语音向量化（speech2vec 类）方案
   并与 owner 展开讨论，之后才做实验规划——本轮不锁定嵌入器清单/实验设计。
   调研已以多代理 workflow 启动（8 维度 Opus finder + 对抗验证），产出
   `wiki/2026-07-08-speech2vec-survey-2025plus.md`（候选矩阵 ≠ 选型）。
3. **实验目标（调研+讨论后落实）**：Stage-1 最高优先 = **数据集覆盖度**——所有小规模数据集
   完成验证，产出覆盖最广的**数据方案 + 实验型技术方案**（每种任务情形 → 表征×粒度×
   检索/使用方式的统一方案表）。
4. **模型分工**：Fable 总编排/判据冻结/对抗把关/综合；调研委托 Opus；代码实现委托 Sonnet。
5. 一致性小修复本日执行：kb_audit latent bug、T7 errata（W1 repo，各归各仓库提交）；
   omni-embed loader 修复推迟到嵌入器选型讨论后按官方用法一并做。

## 6. 对两个设计问题的初步立场（讨论材料，待调研验证，非结论）

- **Q1（统一 vs 任务特化嵌入器）**："统一主键 + 证据驱动的特化例外"。key 空间定义"相似"的
  语义，各任务等价类不同（内容同/说话人异 ↔ 情感同/内容异 ↔ 意图同/措辞异），单一空间难以
  处处最优；但 W4 论题本身 = frozen omni 嵌入的任务条件化解缠读出，项目内生答案是"一个空间、
  多读出"。emotion2vec/speech codec 等特化表征的候选角色：对照上界 baseline + verifier 信号，
  除非实测证明作键显著更好（effect-over-novelty）。**先决实证问题 = CLAP 键对内容型任务的
  错配风险**，由调研 + 后续检索质量测评定夺。
- **Q2（粒度）**：按 knowledge/skill/memory 分类学组织——ASR 困难样本 = **memory 粒度**
  （key=声学嵌入，value=(音频引用, 校正转写, 错误模式)；来源仅 train/dev/历史流量；部署侧
  "困难"判定只能用可部署信号如多采样不一致/熵）；SLU intent = utterance 级 key（value 中
  标签定义=knowledge 与历史实例=memory 分开存）；SLU slot = segment 粒度（候选：两级检索——
  utterance 级检回带槽位标注的相似整句作 few-shot、span 定位交给 frozen 模型 ICL；
  多向量/late-interaction 与 frame 级列为后备）。KB schema 演进方向：`key_granularity` 字段 +
  父子多键 + value 的 grain 标签。以上均为**候选方案空间**，待 2025+ 调研矩阵到位后与 owner
  讨论定夺。
