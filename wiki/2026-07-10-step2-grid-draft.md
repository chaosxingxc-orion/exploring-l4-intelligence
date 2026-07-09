# 2026-07-10 · Step-2 网格草案（冻结会材料——2a 调研 × 2b 底账合并，不预执行）

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
- **基座（2）**：Qwen3-Omni-30B / MERaLiON-2-3B（双 GGUF 定稿）。

## 3. 预注册削减规则（全因子 ≈8×4×6×7×4×6×2 天文数字 → 三阶段）

**Phase A 边际扫描（主裁决场，dev n=40）**：每维逐臂扫、其余维钉 ref-config。
臂数 = 8+4+6+7+4+6 = 35 配置 × 4 数据集 × 1 基座（qwen3 先行）≈ **140 dev 格**。
向量模型维在 squtr 上额外跑 R@1/R@10/nDCG@10（原生 qrels，检索质量与端到端并行出数）。

**Phase B 赢家组合 + 交互对角（dev→test 双切片）**：每维 top-1/top-2 组成 ≤6 个组合配置 +
已证一阶杠杆交互（递送×查询构造、key×检索策略）≤6 对角格 → **≤12 配置 × 4 集 × 2 基座 ×
dev/test ≈ 192 格**；test 只跑 Phase B（防 dev 过拟合，Stage-1 版防泄漏纪律）。

**Phase C 特化侧翼（各任务族主场，dev n=40 / test n=60 赢家）**：
K4 SER（E2V-S/e2v+/Dasheng/CLSP/WavLM ×5 vs H-b 读出，crema-d+esd+csemotions）；
K5 SID（ERes2NetV2/CAM++/ReDimNet/WavLM-L ×4 + cn-celeb1 试验对 EER）；
K1/K2 困难样本记忆（memory-grain：librispeech train池→test、aishell-1 同构；utt 键 vs
utt+词级；SenseVoice-S zh 声学键探针）；K6/K7（两级检索 vs 整句 exemplar，slurp+speech-massive
+minds14）；K10（audio2tool 工具注册表检索）。≈ **120 格**。

**总预算 ≈ 450 格**（每格 n=40-60、~2-6 min GPU）≈ **2-3 个 GPU 日**，分波与 step-1 波 2/3
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
HippoRAG-lite；audio+text 混合 value 是否入列）；3. 三阶段削减规则与 ~450 格预算（§3）；
4. test 只跑 Phase B 赢家的防过拟合纪律；5. H-a/H-b 判定按任务族分报（§4）；6. Phase A 先行
基座=qwen3 单基座（省一半，MERaLiON 在 Phase B 补入）；7. 工程前置清单（§5）排期确认。
