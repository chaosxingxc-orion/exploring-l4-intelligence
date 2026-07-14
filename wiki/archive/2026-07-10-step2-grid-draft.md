# 2026-07-10 · Step-2 网格草案（冻结会材料——2a 调研 × 2b 底账合并，不预执行）

> **2026-07-11 更正（append-only，正文保持原样）**：①§6.7 "工程前置①–⑤已全部完成"经核验不实——Phase-A
> 当前不可执行（无 --execute 路径、runner/builder source 命名 4vs3 字段错配、qwen3-omni-hidden vs
> qwen3-omni-own token 错配、query embedder auto 回退 CLAP 致 ref-config 亦检索不通、6 臂 PLAN ONLY、
> kb_batch_build 仅单 utt 键单 value），修复=工程票 #25，G2 门（全臂 E2E green）后方可开跑；②计数对齐：
> 续10 裁定 35 臂/140 格（RAPTOR-lite 入列），代码现为 34/136，以裁定为准、#25 对齐代码；③§6.8 重抽
> 签字位已由续10 裁决为全量重抽（非开放问题）；④本网格开跑前置另受 2026-07-11 stop-the-line 约束，详见
> [[2026-07-11-stage1-audit-response-and-rulings]]。

> **2026-07-11 补正（#28 全量核验）**：§2 递送维的 LLMLingua-2 应称**冻结预训练压缩器**（其压缩器为
> 上游 LLM 蒸馏训练的 token 分类器，非 training-free by construction——training-free 的是原版
> LLMLingua）；臂不变（我方冻结使用、不训练），但任何写作不得把 LLMLingua-2 作为 training-free
> 论题证据（step2a-d3-7 更正，详见 [[2026-07-11-survey-full-verification]]）。

> **2026-07-12 再定性（owner 内涵裁定）**：vocalbench-knowledge 退出 RAG 主战场≠废弃——其内涵是
> **闭卷参数化知识探针**（口语短事实 QA，盘上无证据段落；轴名 knowledge 指模型权重内知识，非外挂库）。
> 误编根因=标签漂移链：调研标其为 KB-retrieval **SOURCE** 候选（库源），网格误滑为检索**测试床**。
> 重新归位三角色：①Proposal-R no-retrieval 对照的语义锚点（RAG 增益−闭卷增益=外部知识净贡献）；
> ②Step-3 selector 主场之一（闭卷知识激活，无 KB，最贴"激活预训练知识"旗舰叙事）；③语音通道
> 知识存取差探针。Phase-A RAG 主场收缩为 squtr（corpus-side 重建后）+ heysquad + SQuAD-zh。

> **性质**：Step-2（omni agentic system mock 基线锁定与方案对比）的冻结会输入。合并
> 2a 调研（105 网格候选，`2026-07-09-step2a-mmknowledge-survey.md`）与 2b 方案空间底账
> （三步设计 §2b），落成可执行网格 + **预注册削减规则**。mock 口径 = owner 已裁定的
> **严格无 RL**（固定管线；组织×加载的方案空间本身是被对比对象，方案内参数 dev 定、test 锁）。
> H-b 前提已解除（30B 音频 embedding 活体 WORKS，dim 2048 双模态同空间）。
> **签字位见 §6；不冻结不开跑。**

## 1. 参照配置（ref-config，边际扫描的锚点）

`{向量模型=GLAP · key=单utterance键 · value=knowledge-passage · 检索=dense top-3 cosine ·
查询=音频直查 · 递送=flat in-prompt · 基座=Qwen3-Omni-30B}`——每一维的"业界默认"，
所有边际扫描固定其余维于此。

## 2. 维度枚举（合并后终版）

- **向量模型（8）**：GLAP / LCO-3B / LCO-7B / **Qwen3-Omni 自身隐态**（H-b，已解锁）/ SENSE /
  MERaLiON-SE2 / CLAP（负对照）/ omni-embed-nemotron（NC 对照）。
- **key 组织（4）**：单 utt 键 / 多粒度键（utt+词级，M2R 双尺度）/ H-a 2–3 键空间（内容+
  speaker+emotion，特化侧翼裁决）/ H-b 单空间多读出。
- **value 组织（4+2 对照）**：knowledge-passage / memory-instance / exemplar（grain 标注，
  schema 已支持）；+低成本结构对照臂二选一（RAPTOR-lite 或 HippoRAG-lite——2a D2 证据，
  只跑主裁决场 1-2 集）；+audio+text 混合 value（2a D1 候选）。
- **检索策略（7）**：dense top-k∈{1,3,5} / 固定阈值截断 / hybrid BM25+dense RRF（squtr 文本
  语料侧）/ **retrieve-then-select 固定版**（2a：Hearing-More 先例）/ 两级检索（slot 默认）/
  固定深度 IRCoT 2 跳（M 裁决臂）/ 长上下文 stuffing（无检索对照）。
- **查询构造（4）**：音频直查（同空间）/ 自身 ASR 转写→文本键（跨空间，部署合规）/ 非对称
  encode_query / HyDE 单发（M 裁决臂）。
- **递送（6）**：flat / 结构化参考注（grain 角色标记）/ **2-turn 工具递送**（T10 一阶杠杆）/
  system-prompt 注入 / 相关性边缘重排（lost-in-the-middle，L）/ LLMLingua-2 压缩注入（M 裁决臂）。
- **基座（1）**：Qwen3-Omni-30B（**2026-07-10 修订**：owner 裁定主模型单一化——波 1 论证
  MERaLiON 不具备主模型能力，从底座除名；其文件保留为 **step-3 封闭形态验证器候选**，去留由
  step-3 验证臂实验裁决）。

## 3. 预注册削减规则（全因子 ≈8×4×6×7×4×6×2 天文数字 → 三阶段）

**Phase A 边际扫描（主裁决场，dev n=40）**：每维逐臂扫、其余维钉 ref-config。
臂数 = 34 配置（8+4+5+7+4+6；value_org 实为 5 个可枚举 token——"4+2 对照"中结构对照臂二选一
后只余 1 个附加臂，runner 基建 dry-run 已核实计数）× 4 数据集 × 1 基座（qwen3 先行）
= **136 dev 格 ≈ 4.8h**（runner dry-run 实估）。
向量模型维在 squtr 上额外跑 R@1/R@10/nDCG@10（原生 qrels，检索质量与端到端并行出数）。

**Phase B 赢家组合 + 交互对角（dev→test 双切片）**：每维 top-1/top-2 组成 ≤6 个组合配置 +
已证一阶杠杆交互（递送×查询构造、key×检索策略）≤6 对角格 → **≤12 配置 × 4 集 × 1 基座 ×
dev/test ≈ 96 格**（2026-07-10 单底座修订）；test 只跑 Phase B（防 dev 过拟合）。

**Phase C 特化侧翼（各任务族主场，dev n=40 / test n=60 赢家）**：
K4 SER（E2V-S/e2v+/Dasheng/CLSP/WavLM ×5 vs H-b 读出，crema-d+esd+csemotions）；
K5 SID（ERes2NetV2/CAM++/ReDimNet/WavLM-L ×4 + cn-celeb1 试验对 EER）；
K1/K2 困难样本记忆（memory-grain：librispeech train池→test、aishell-1 同构；utt 键 vs
utt+词级；SenseVoice-S zh 声学键探针）；K6/K7（两级检索 vs 整句 exemplar，slurp+speech-massive
+minds14）；K10（audio2tool 工具注册表检索）。≈ **120 格**。

**总预算 ≈ 330 格**（单底座修订后）（每格 n=40-60、~2-6 min GPU）≈ **2-3 个 GPU 日**，分波与 step-1 波 2/3
交错排程。嵌入库构建（每向量模型 × 每数据集池）走 llama-server 空窗批抽（gpu_session 排程）。

## 4. 裁决口径

- **H-a vs H-b**：主裁决场（内容任务）+ K4/K5（副语言）同切片同协议对决；H-b 臂 = 自身隐态
  （30B embedding server 配置已验证）与 LCO 变体；判定 directional（paired-bootstrap CI），
  按任务族分别报告（预期："内容强副语言弱"的部分成立形态，survey F2/W4 证据先验）。
- **组织×加载最优方案**：每任务族报告 top 配置 + 对 ref-config 的 delta CI —— 即 owner Q1/Q2
  的实证答案、step-3 的分母。
- **泄露纪律**：每 KB source 过 kb_build（CLEAN 强制门）；KB 池与评测 item-id 结构分离；
  heysquad 走 scrub；查询构造臂全部过 Information-Boundary-Guard（golden 转写查禁止）。

## 5. 工程前置（step-2 专属，Sonnet 票）

① KB schema 演进落地：key_granularity + 父子 span 键 + value grain 标签（备忘录已定需求）；
② 嵌入库批构建管线（8 向量模型 loader 统一接口 + 每数据集池的 build_source + verdict 门）；
③ squtr mini-corpus builder 接入（loader 已有 build_mini_corpus）；④ mock 管线 runner
（run_baseline 的检索增强扩展：retrieve→inject→generate，复用波 1 全部机制）；
⑤ 30B embedding server 模式与生成模式的 gpu_session 分时排程（同一模型两种 serve 配置）。

## 6. 冻结会签字位

1. ref-config 认可（§1）；2. 维度枚举与对照臂取舍（§2——结构对照臂二选一：RAPTOR-lite vs
HippoRAG-lite 之择、audio+text 混合 value 是否入列）；3. 三阶段削减规则与 **~330 格**预算
（§3，单底座修订版）；4. test 只跑 Phase B 赢家的防过拟合纪律；5. H-a/H-b 判定按任务族分报
（§4）；6. ~~Phase A 单基座先行~~（**已被 2026-07-10 主模型单一化裁定取代**：全程 qwen3
单底座）；7. 工程前置清单（§5）排期确认（①-⑤ 已全部完成，签字即可开跑）。
另附波 1 caveat 裁决位：8. dev/test 是否为 Phase-B 做不相交重抽（波 1 量化 52/56 集重叠）；
9. containment-EM 弱指标维持或加语义辅助臂。
