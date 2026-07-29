---
artifact_id: "SF-STAGE1C-R2-COREVIEW-V2"
role: "R2 开题报告底稿 v2（模板 v2 首例）：跨域知识演进综述 → 本域批判分析 → 共通性 → 实验建议"
status: "CONDITIONAL_GO_STANDALONE_PENDING_V3_CHECKLIST (owner 2026-07-29, Decision-Log 续77); v3 整改中"
template: "2026-07-29-direction-coreview-template.md (V2)"
review: "wiki/audit/system-first-stage1c-v2/round-03/2026-07-29-r2-doctoral-supervisor-coreview.md (MAJOR_REVISION)"
evidence_cut: "2026-07-29"
supersedes: "V1（同文件 git 历史）"
execution_authority: "STAGE2A_WITHHELD"
---

# R2 开题报告 v2：音频驱动的外部知识获取

## §1 元信息与证据可回溯

- ID：R2；主维度 D1 知识（外部知识获取）。前版 V1 与更早的执行者草稿
  `R2-audio-native-knowledge-acquisition.md` 的证据事实全部继承。
- 证据底座三层（承重深度递减，引用纪律见 §6）：
  1. **深读层**（有 dossier 逐篇条目）：AudioRAG 2602.10656、Omni-DeepSearch 2605.08762、
     VoiceAgentRAG 2603.02206（d1/d4 dossier）及 d6 donor 条目（ToolGate 2606.03054、FOVEA
     2605.01345、Calibrate-Then-Act 2602.16699、VOI-search 2605.05701、PRA 2604.09482、
     Decocted 2604.04373、MemRL 2601.03192、AdaCompute 2604.14853、WebThinker 2504.21776、
     Reflexion 2303.11366 等）。
  2. **登记未深读层**（本地 PDF+hash，无逐篇条目；只作机制定位，不引数字）：
     2605.13277、2605.15019、2604.25122、2508.21475、2605.05185、2605.16481、2605.14906、
     2605.10848。
  3. **本轮补抓层**（2026-07-29 按 owner 授权 known-ID fetch+登记 31 篇；深度=机制级定位，
     标 `PENDING_DEEP_READ`，不引承重数字）：见 §2 各节点 id 与 §6 枚举。
- **时效规则（owner 2026-07-29）**：2024-01 之前的论文不参考，例外仅数据集提供方与算法
  原理支撑。本稿引用集中的 pre-2024 例外：RAG 2005.11401、DPR 2004.04906、Self-RAG
  2310.11511、ROME 2202.05262（算法原理）；OK-VQA 1906.00067、A-OKVQA 2206.01718
  （数据集）；ReAct 2210.03629、Reflexion 2303.11366（原理，深读层既有）。本轮同批抓取的
  其余 pre-2024 节点（REALM/kNN-LM/RETRO/Atlas/FLARE/IRCoT/Self-Ask/DSP/Toolformer/
  WebGPT/MuRAG/RA-CM3 共 12 篇）仅入 ledger 存档，不进引用集。
- 全部承重引用可回溯 `wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl`（sha256+本地路径）。

## §2 业内实践演进综述（文本 → 视觉多模态 → 语音）

### §2.1 文本模型 + 知识：三轴演进（主体 2024→2026）

**原理基座（pre-2024，仅按 owner 时效例外引入）**：运行时检索拼接原理（RAG 2005.11401：
冻结生成器+可换外部库）、稠密检索原理（DPR 2004.04906：文档入 embedding 空间、近邻即
检索）、自适应触发原理（Self-RAG 2310.11511：模型自决"是否检索/是否可信"）、参数知识
可定位原理（ROME 2202.05262：事实在权重中有结构但难更新——外部知识必要性的原理依据）、
工具交错与语言化反馈原理（ReAct 2210.03629、Reflexion 2303.11366，本地深读层）。此外的
pre-2024 谱系（预训练耦合库、解码期数据库、交错检索原型、浏览式工具化等）按 07-29 时效
裁决不再逐篇参考。

**组织形式（2024→2026）**：平铺 chunk 向量库 → **图/层次索引**（GraphRAG 2404.16130 社区
摘要图、HippoRAG 2405.14831 海马体式索引、LightRAG 2410.05779 双层图检索：组织开始携带
跨文档结构）→ **agentic/演化记忆**（A-MEM 2502.12110；MemRL 2601.03192 三元组库
{intent, experience, utility-Q} 且只更新真正进过上下文的记忆；Decocted 2604.04373 经验
蒸馏优于原始经验、检索相关性↑而任务性能非单调）；稀疏/稠密对照仍活跃（Pi-Serini
2605.10848：调好的 BM25+足够深度即可暴露高证据召回）。
**轴结论**：组织从"静态外挂"走到"带效用记账、可演化的库"，库的价值被逐条测量。

**供给形式（2024→2026）**：检索质量评估器决定纠正动作（CRAG 2401.15884）→ **agentic
深搜**（Search-o1 2501.05366、Search-R1 2503.09516、DeepResearcher 2504.03160、WebThinker
2504.21776 分层委派+报告工具）→ **被定价/被校准的获取**（Calibrate-Then-Act 2602.16699：
校准先验后闭式判 "retrieve iff p_ret·γ≥p_da"，并示证"无条件检索是默认失效模式"；
VOI-search 2605.05701：value-per-budget 归一+双硬预算；PRA 2604.09482：margin-shift VoI
只在证据能移动评估器后验时判需检索；AdaCompute 2604.14853：Lagrange 单价精确命中平均
预算）。
**轴结论**：供给决策从"总是检索"演进到"何时检索、检索多少都是被打分、被定价的决策"——
2026 文本域的活跃前沿。

**使用形式（2024→2026）**：拼接 grounding → **admission/仲裁**（PRA 打分器与策略分离防
污染；Decocted 证明上下文信息增益可为负 I(Y;C|X)<0——"更相关≠更好"）→ 证据态写作
（WebThinker draft/check/edit）。
**轴结论**：末端问题已收敛为 **stop / admission / 预算**——恰是 reward-guided 控制面问题。

### §2.2 视觉多模态 + 知识：三轴演进（主体 2024→2026）

**数据集基座（pre-2024，按时效例外引入）**：OK-VQA 1906.00067 / A-OKVQA 2206.01718 定义
"图像之外的知识是否必要"这一问题并提供沿用至今的 knowledge-VQA 基准。其余 pre-2024 多
模态 RAG 谱系按时效裁决不逐篇参考。

**组织形式（2024→2026）**：实体/wiki 文档库（Wiki-LLaVA 2404.15406、EchoSight
2407.12735）→ 多粒度证据（2605.15019 element/scene 两级）→ **在线构建的层次视觉记忆**
（2605.16481；2605.14906 给出组织代价函数：长上下文随长度退化 vs 记忆体在存储压缩中丢
视觉保真度）。

**供给形式（2024→2026）**：**多模态搜索 agent**（MMSearch 2409.12959 第一代基准 →
MMSearch-Plus 2508.21475 provenance-aware → OpenSearch-VL 2605.05185）→ **被门控/被定价
的获取**（ToolGate 2606.03054：pre-call gate 在输出进上下文之前决定执行/跳过，15,782 次
标注调用给出基率 11.8% helpful / 9.9% harmful / 78.3% unchanged——获取不免费且多半惰性；
FOVEA 2605.01345：序贯贝叶斯实验设计选观察，Information Cliff 证明贪心可证不足；
MementoGUI 2605.18652：检索刷新本身被门控；cotomi 2605.03231：lazy observation 按需揭示
且预取与轮内获取不可加）→ **regime 边界**（2606.28864：额外测试时算力对推理型任务有利、
对纯感知任务有害）。

**使用形式（2024→2026）**：知识 grounding → **utility-vs-relevance 证据选择**
（2605.13277）→ 归因指标（2605.15019 attribution precision/unsupported-claim）→
**四臂协议成为标准**（M3-VQA 2604.25122：no-evidence / gold-evidence / heuristic /
agentic + 证据链可溯源）→ forced-answer 四分类探针（ToolGate）。

**轴结论**：视觉域已把"获取要定价、证据要审计、oracle/gold-evidence 臂是标准协议"变成
共同实践——这些臂和探针正是语音域实验里缺席的东西。

### §2.3 语音多模态：处于演进史的哪个阶段

本地读集（cut 2026-07-29）内，语音域的知识工作分三条线：

1. **检索表征线**（解决"音频能否直接作 query/索引单元"）：SpeechDPR 2401.13463（端到端
   口语 passage 检索，蒸馏自 UASR+文本稠密检索）→ SpeechRAG 2412.16500（语音 adapter 接
   冻结 LLM 检索器，绕过 ASR 从文本 query 检索音频段）→ WavRAG 2502.14727（原始音频直接
   embedding 入库、音频-文本混合知识库+CoT）。三篇对应文本域 **2020–2022 的
   DPR→RAG 段位**：组织形式=稠密库（首次含音频模态），供给=单跳检索拼接，使用=无条件
   grounding。
2. **agentic 获取线**（2026）：AudioRAG、Omni-DeepSearch——对应文本域 **2025 的
   Search-o1/WebThinker 段位**（AudioRAG 即 WebThinker 的音频移植），但**尚未进入 2026
   文本域的"定价/校准"段位**：供给决策全部是 LLM 自由生成 + 硬编码预算常数，无一处
   scalar reward 充当推理期控制器（T1 场级事实：37 行音频/omni 语料内为零，读集内）。
3. **基础设施线**：VoiceAgentRAG——跨轮预取/缓存，纯文本 KB，无答案质量轴。

**定位结论**：语音域在组织轴停在"向量库/无组织"（图/层次/演化记忆全缺），在供给轴停在
"pre-pricing agentic"（校准触发、VoI 定价、预算再分配全缺），在使用轴停在"无条件接纳"
（admission 门、四臂协议、oracle 行、abstention/coverage 全缺）。**文本域 2023–2026 的
整个"自适应→定价"跃迁，语音域尚未发生——这就是 R2 的台阶所在。**

## §3 本域文献与数据集批判性分析

### §3.1 逐篇方法分析（DFS 四问，深读层）

| 论文 | 方法 | 局限 | 改进空间 | 可借鉴 |
|---|---|---|---|---|
| AudioRAG | 文本 controller（Qwen3-8B）Think-Call-Answer 环调度 frozen omni audio tool + Google Search；omni 降级为可查询观察源 | 无 need gate/成本记账/hop 记录/显式 stop；wrapper 自身把 type-D 无效答案变多（无限循环）；+9.2pt 无工具消融不可归因 | 调度与停止无 reward 约束——公开缺口 | 500 题、GPT-4o judge 三次平均、A/B/C/D 错误分类学 |
| Omni-DeepSearch | 冻结模型自持 query/工具/重试/放弃；三工具每步一 query；预算=固定档 (X,Y)；video 两阶段 verify-then-densify | 每步必搜（禁用内部知识）；停止=预算耗尽或自声明；UNKNOWN token 存在但零 coverage 分析；无成本记账；无 no-tool 直读行 | 预算饱和+over-search 自证（见 §3.2）而无逐实例调度器——台阶由作者自己给出 | 640 题官方资产、三判官协议、subgroup/预算/oracle 三消融报告法 |
| VoiceAgentRAG | Slow Thinker 预测 3–5 后续话题异步预取 + Fast Talker 缓存优先；document-embedding 建索引（prediction-query embedding 版本语义错误命中——全文最锋利工程教训） | 无真实语音、无答案质量指标；75% 头条混淆三机制无消融；单次运行 | 对 R2 能力问题无台阶 | cache/latency 报告法（归 R9） |

### §3.2 数据集批判性四问

**AudioRAG-500**：
- 合理？**中**。两道过滤（Question Validity + Answer Correctness）设计合理，但过滤器与
  错误判官都见 gold audio attribute，且 80% 条目由 GPT-4o 从八个公开数据集（MMAU/CinePile/
  MNSC/FMA/Jazznet/MusicNet/iNaturalist/CHEER）的元数据生成——检索侧污染未处理。
- 代表性？**中**。音源跨 sound/music/speech，但无难度/条件分层。
- 新标准基线？**否**。n=500 无 CI、无 split、无工具消融、无检索质量测量。
- 它对比了什么？Table 2：六个裸模型（Qwen2.5-Omni 32.2 / AF3 28.8 / Audio-Reasoner 20.2 /
  Baichuan-Omni 24.4 / **Qwen3-Omni 37.0** / Gemini-2.5-Flash 45.0）+ 两个 agentic 臂
  （Qwen2.5-Omni+Qwen3-8B 39.5；**Qwen3-Omni+Qwen3-8B 46.2**）。

**Omni-DeepSearch-640**：
- 合理？**高（三者最严）**。音频 QC + 四道 GPT-5 过滤（含纯问题推理过滤、first-hop 实体
  泄漏过滤、视觉必要性过滤）+ 人工唯一性复核；一个非根节点绑定近期新闻抗参数捷径；
  Wikipedia 知识图谱路径 k≥5。
- 代表性？**中偏高**。15 类覆盖检索目标×音频内容两维；仅 640 题、YouTube 开放域，作者
  自述未覆盖噪声/多语。
- 新标准基线？**接近但未成立**，四个阻断项：仅一个 `train` split；无冻结检索快照（结果随
  时间漂移）；无 no-tool 直读行；温度 0 单样本、每格 4 题量级——统计分辨率撑不起排名功能。
  **可作方向性主载体**。
- 它对比了什么？12 个模型统一 pipeline 横比（Gemini-3-Pro 43.44 最强；最佳开源 Mimo-V2.5
  11.72；**本项目核 Qwen3-Omni-30B Thinking 仅 6.56**——本地复现空间巨大）；预算消融
  **(5,1)=29.06 → (10,3)=43.44 → (15,5)=44.06**，且第三档强烈非均匀（IMAGE 38.75→50.00、
  SPEECH 55.00→70.83 上升；VIDEO 36.88→31.25、AMBIENT 36.67→20.83 下降）；App.A.6 给出
  完整 over-search 轨迹：正确证据第 3 轮已到手，预算有余继续扩展假设、累积语义合理干扰项，
  "(10,3) 停下答对，(15,5) 耗尽预算答错"；oracle 分解 entity-only 33.76 / 端到端 43.44 /
  gold-entity 50.00（完美实体后仍有约 50 点 headroom 落在查询构造/检索/验证上）。
- 补充（检索表征线数据集，本轮登记未深读，只记在案不判定）：SpeechDPR/SpeechRAG/WavRAG
  各有口语 QA/检索评测资产，属组织轴选项，深读后再过四问。

**VoiceAgentRAG-200**：
- 合理？**低（作为能力基线）**：合成 12 文档 KB 为可复现性刻意选择。代表性？**低**：
  scripted 文本轮次、单一 CRM 域。新标准基线？**否**：无答案质量轴。它对比了什么？
  仅 Traditional RAG 一个基线（hit rate 75%、110.4ms→0.35ms、316×）。
- 处置：仅作 R9 latency/cache 参考。

### §3.3 readiness 表

| 资产 | 本地 | lock | split | 评测依赖 | 缺口 |
|---|---|---|---|---|---|
| Omni-DeepSearch-640 | 有（`LOCAL_CANDIDATE_UNFROZEN`） | 未入 | 官方仅 `train` | 三 LLM judge（外部 API） | 无检索快照/负类/dev-test |
| AudioRAG-500 | 未落盘 | 未入 | 论文未给 | GPT-4o judge（外部 API） | 无 frozen web corpus/工具消融 |
| VoiceAgentRAG-200 | 未落盘 | 未入 | scripted | — | 无语音/答案质量轴 |
| 检索表征线三篇资产 | 论文已登记，数据集未盘点 | 未入 | 待深读 | 待深读 | 组织轴选项，非首切片 |

## §4 技术方法共通性分析

### §4.1 三篇的共同结构（读集内断言，cut 07-29）

1. **组织轴：无人拥有可复放的知识组织**——两篇 benchmark 用开放 live web（无快照/文档 ID/
   轨迹落盘），第三篇有索引却是纯文本合成 KB。语音域至今没有"持久、可复放、按声学条件
   组织"的知识形态。
2. **供给轴：每个采集决策=LLM 自由生成，每个数量=硬编码常数**（无界 hops / 固定 (X,Y) /
   n=3–5、τ=0.40）。读集内无 scalar reward 充当推理期控制器。
3. **使用轴：检索结果无条件进上下文**，无 admission、无跨供给共识，无人测"这次采集是否
   改变了答案"。
4. **停止权是三篇共同的、已被自己论文实证的失效面**（AudioRAG type-D 增多；Omni-DeepSearch
   A.6 over-search 轨迹；VoiceAgentRAG 无停止概念）——且可在它们已发布的指标上直接测量，
   不需要发明新指标。
5. **abstain 实质缺席**（UNKNOWN token 存在但零 coverage 分析）。
6. **跨实例/跨轮知识复用为零**（每题冷启；TTL 300s 即死；作者自提 pre-warming 而不实现）。

### §4.2 跨域已成熟、语音域缺席的机制位（改进空间来源）

| # | 机制 | 跨域出处 | 语音域状态 |
|---|---|---|---|
| M1 | pre-call admission gate（证据进上下文前拒绝） | ToolGate（11.8/9.9/78.3 基率；prompt 级怀疑无效） | 三篇皆无 |
| M2 | value-per-budget + 双硬预算 | VOI-search（中预算有时胜高预算） | 只有全局固定档 |
| M3 | 校准先验决定是否检索 | Calibrate-Then-Act（closed-form；"always acquire 是默认失效模式"） | 不可测（benchmark 无负类）——正是 V1 判死 H1 的原因 |
| M4 | margin-shift VoI 免人工负类标签 | PRA（\|Δm\|>ε 才判需检索） | 无；黑箱可行性待评估（PRA 用 logit，API-only 不保证） |
| M5 | forced-answer 四分类探针（离线标签构造） | ToolGate | 仅 Audio-Maestro 事后诊断（41.6–43.5% 工具改动方向是错的），从不进决策 |
| M6 | "更相关≠更好"/负信息增益 | Decocted | AudioRAG 从不检查检索页是否含答案 |
| M7 | oracle/headroom 行 | 视觉 FOVEA selector ablation；四臂协议 | 唯一 oracle 行=Omni-DeepSearch entity 分解；D1 读集六篇 `oracle_if_published` 全 NONE |
| M8 | 按类别/实例再分配固定总预算 | AdaCompute（Lagrange 单价+二分） | Omni-DeepSearch 自证最优预算随类别而异却统一封顶 |

（M9 跨轮复用/write-gate 归 R3、M10 图组织双缺须先补文本证据、M11 regime 边界语音侧已有
同形数据、M12 稀疏/稠密对照零——记录在案，不入首批杠杆。）

### §4.3 与文本/视觉谱系的对应

语音 agentic 线正处在文本域 2025 段位；文本域 2026 年已给出四条"定价/校准"路线（CTA/
VOI-search/PRA/AdaCompute），视觉域已给出门控与四臂协议（ToolGate/M3-VQA）。**这些机制的
"形状"可借（协议/状态表示/统计量），效果不跨模态外推（H5 withheld）。**

## §5 实验建议

**数据集**：主载体 Omni-DeepSearch-640（构造纪律最严 + 唯一自带 oracle 行 + 预算消融即
现成对照臂；执行合同须解决：本地资产冻结入 lock、按 task_category 分层预注册 dev/test
切分——只切分不重标、judge 协议复现方案）。次载体 AudioRAG-500（错误分类学 + 跨任务
方向一致性检验）。放弃 VoiceAgentRAG（无答案质量轴，仅存 R9 参考）。检索表征线资产深读
后再议（组织轴选项）。

**基线方法**（(a) 型落实）：
- 须复现（项目核 Qwen3-Omni-30B，官方协议）：**no-tool direct 行（论文缺失，本项目补上
  即是贡献）**、固定预算三档 (5,1)/(10,3)/(15,5)、AudioRAG raw + agentic pipeline 两臂。
  注意本核在 Omni-DeepSearch 论文里仅 6.56（Thinking）——先复现该数字再谈改进。
- 只引用：Gemini/MiMo 等他核数字（不改写为本项目结果）。
- 对照臂：random-matched-cost 调度（AdaCompute 空对照形状）、MementoGUI 式 random
  episodic 臂（若引入任何缓存）。

**改进/提升空间**（每条已过 read-out/new-info 判别：只用部署时可得信号——中间答案一致性、
检索-音频实体 corroboration、预算消耗；不用 test gold、不用隐藏状态）：
1. **主杠杆 L1：reward-guided 检索预算/停止调度**（M2+M8）：逐实例决定继续搜/换 query/停，
   等总预算下对抗最优固定档。依据=论文自证的饱和曲线+over-search 轨迹+类别非均匀性。
2. **次杠杆 L2：pre-call admission 门**（M1+M6）：检索证据进上下文前的接纳决策，用
   AudioRAG A/B/C/D 分类学测 Knowledge-error 下降与 type-D 不增。
3. **候选 L3：margin-shift 式免负类 need 信号**（M4）：先做黑箱可行性评估（API-only 无
   保证 logprob），可行则补上 V1 判死的 need-detection 的替代路径；不可行则弃。
4. **交付物 L4：oracle/headroom 行**（M7）：复用官方 golden_path 构造 gold-entity 臂，
   产出语音域缺席的标准协议行本身即贡献。

**研究问题一句话**：在 Omni-DeepSearch-640（官方协议、等总预算）上，训练无关的
reward-guided 检索调度与 admission 门能否相对最优固定预算基线带来可靠 accuracy 提升并
降低 over-search 失败。

**数字击杀阈值**（提案默认，`TBD_AT_AUTHORIZATION`）：
- K1：等预算 L1 vs 最优固定档，paired delta 95% 下置信界 ≤0 或点估计 <**+2.0pt** → 杀
  独立方向，回落 MERGE。
- K2：L1 未把 over-search 型错误相对减少 ≥**30%**（等 accuracy）→ 调度杠杆判死，仅留 L2
  作 R5/R8 组件。
- K3：收益在 AudioRAG-500 上符号翻转 → 降级为单 benchmark 现象。
- K4：L2 未把 Knowledge-error 降低且 type-D 不增 → admission 门判死。

**管辖界线**（判据均匀适用）：R2 立项研究的是**检索这一 action family 的专用调度与证据
取舍**；R6 管跨方向通用轨迹控制、R8 管阈值可靠性，R2 产出可被其消费。与 V1 相同的对抗
论证保留：若"用到 controller 即越界"成立则 R5/R6/R8 同死——该判据不可选择性适用。

## §6 边界与暴露声明

- API-only；test gold 永不进 controller；数据/指标复用官方口径；不自建数据、不重标、不补
  检索快照；H5 withheld——跨域只借形状不承载效果。
- **本轮 exposure（2026-07-29）**：① known-ID fulltext fetch+登记 31 篇，全部 pdf+eprint
  双 rendition 落盘 E: 并追加 ledger 行；其中进入引用集 19 篇（post-2024：2401.15884/
  2401.13463/2404.16130/2404.15406/2405.14831/2407.12735/2409.12959/2410.05779/2412.16500/
  2501.05366/2502.14727/2503.09516/2504.03160；pre-2024 例外：2005.11401/2004.04906/
  2310.11511/2202.05262/1906.00067/2206.01718），其余 12 篇 pre-2024（2002.08909/1911.00172/
  2112.04426/2208.03299/2305.06983/2212.10509/2210.03350/2212.14024/2302.04761/2112.09332/
  2210.02928/2211.12561）按 owner 时效裁决仅存档不引用；② 3 次 web 检索仅用于解析语音线
  三篇的精确 arXiv id（题名→id，非主题发现）；③ 零模型/API 执行、零指标运行、零数据集
  下载、零复现、零原型。
- 补抓层引用纪律：本稿只用其**机制级定位**（标准共识事实），不引其论文内数字；任何数字
  承重前须补逐篇深读条目。

## §7 处置建议与 owner 裁定

**执行者建议：`GO_STANDALONE_AS_RETRIEVAL_SCHEDULING`**。演进分析强化了 V1 的判断：语音域
缺的不是又一个检索 pipeline，而是文本/视觉域已经完成的"获取被定价、证据被审计"跃迁——
这个跃迁在语音域是空位，且三篇论文自己的数据已经给出了对照臂和失效证据。

**最强反方**（继承 V1 §7）：管辖论证（query/hop/stop 属 R6、预算可靠性属 R8）→ 应 MERGE。
回应同 V1：该论证依赖 owner 未签的「裁决 C」，且判据须均匀适用。真正裁定点=portfolio
归属：**选项 A** 独立方向（本稿 §5 全案）；**选项 B** MERGE（§5 的 L1→R6、L2→R5/R8、
K1-K4 原样搬运，Stage-2D 撤销）。两案实验内容几乎相同。

**owner 裁定栏**：`CONDITIONAL_GO_STANDALONE_PENDING_V3_CHECKLIST` / 2026-07-29 / Decision-Log
续77。三项配套裁决：①检索 trace-logging 放行（pin 服务/日期/参数、逐次落盘返回 hash、共享查询
跨臂复用）；②生效条件=v3 关闭博导评审 §十四 全部清单（proposal 级/authorization 级分层）；
③主张对象=北极星 system-level capability，红线=模型参数不可修改、不得新增一个模型（续78 细化：
只禁为任务新训练模型与新增 LLM 代答；embedding 检索器/frozen judge 属工具级冻结组件可用，最终
作答权在冻结核）。v3 以评审 §十 的音频特有机制为主研究问题重写。
