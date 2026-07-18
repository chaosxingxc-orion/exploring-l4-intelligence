---
artifact_id: "INHERITED-PRIOR-EXPOSURE-UNION-2026-07-18-02"
title: "INHERITED_PRIOR_EXPOSURE union v2——四仓（W1–W4 + umbrella）历史研究模型触碰事件登记"
date: 2026-07-18
supersession: "v2（同日 dated supersession,v5 复审 P0-1 整改）:v1 的「全量登记」称谓撤回——v1 只覆盖 W1+umbrella 且 frontmatter 自载 W4 缺口,『全量』与已知缺口不能同真;v2 = W4 全量考古并入 + W2/W3 零实验核验 + 仓外边界 owner attestation;v1 表体原样保留于 §1"
authority: "阶段正典 v2 四字段记账之 legacy_experiments 字段的正典载体（owner 裁决② 2026-07-18:历史实验不删除、不降格、不假装未发生）"
method: "W1+umbrella:考古代理扫 Decision-Log 2497 行 + _repro/ 464 结果件（抽查 6/6）;W4:考古代理两轮扫描收敛（一轮:inventory 261 行全文/14 个 _repro JSON/git 全历史 52 commit/Hydra 日志/changelog 标题索引,子代理三失二〔由一手证据补齐〕;二轮:changelog 4172 行全通读 + 59 运行事件中转表交叉核对,计数与分型精化）;主执行方法证抽查:inventory 87/95 行逐字吻合、三件 _repro 在盘、claim_ledger.yaml 悬空引用坐实（untracked 且不在盘）;W2/W3:experiments/data 仅 .gitkeep、各 2 提交（零实验骨架,主执行方直验）"
discipline: "「模型触碰」= 研究模型的推理/评测/嵌入计算（含 smoke/单 item/失败但已处理数据);LOAD-ONLY/加载失败单列不计入;无证据的传闻不列;UNCERTAIN 如实标注;粒度异构（W1 事件级/W4 组-行级/legacy LOW）如实分层,不强行归一。本 union 是后续 held-out/预注册/验证集设计必须显式排除或分层处理的暴露面;所有历史数字维持 PRE-METHODOLOGY_DIRECTIONAL_EVIDENCE 等级"
summary_scoped: "计数〔按本件表行机器可数,粒度异构不作单一总数聚合〕:W1+umbrella = 27 事件（§1）;W4 ≈70 事件（§4;二轮考古收敛:changelog 59 运行事件折叠为族 + CREMA 簇 6 + legacy 簇 6 + _repro 簇 7;LOAD/FAIL 单列不计入）;W2/W3 = 0;**去重注记:§1 事件 #1–7（omni-embed CREMA/MInDS 探针,取自 wiki 归档摘要）与 §4 组 D/R 同战役同源——W4 为原生仓,细化以 §4 为准,项目级唯一事件面按两表并集去此重叠**。distinct 研究模型:W1 侧 ~11 + W4 侧 8（实际对数据推理:omni-embed-nemotron-3b/jina omni-small/Gemma-4-E4B/Gemma-4-12B/Qwen3-Omni GGUF〔1 item+超时〕/Voxtral Mini 3B/DeepSeek-OpenAI 兼容 API 验证器/Qwen3-ASR〔legacy 路由〕;LOAD-ONLY 单列）,跨仓重叠 = qwen3-omni 与 omni-embed 同源战役。W4 侧数据集 14 个（CREMA-D/MInDS-14 与 W1 侧同源重叠;新增:SLURP、FLEURS、Spoken-SQuAD、HeySQuAD、URO-Bench mini、CoVoST2〔含 val 1758 + locked test 1695〕、AISHELL-1(63)、WenetSpeech-Wu(21)、Chinese synthetic RAG;LibriSpeech 仅 loader 无运行不计入）"
selection_contamination: "W4 侧选择决策污染面（二轮考古分型）:**触发新模型推理的选择运行 = 5 条**（CoVoST2 val1758 选 boundary-card→locked test/V2 指令 sweep 接受-拒绝/URO 3×3 grid 5-seed/CoVoST2 E4B selection-locked/HeySQuAD train60 accept）+ **离线选择器决策**（SLURP formal selector +0.045 selection-locked、MInDS formal selector〔负,fallback〕、URO task-level selector、margin/same-family 门等——复用既有输出但同属污染面）——**两类合计 ≥11 处选择决策**（首轮 IDs:S4/S16/V2sweep/SEL1/SEL2/SEL2b/V3/F1/F2/F6/F7/C8）,held-out/验证集设计对涉及数据集×split 必须显式排除或分层;SEL2-seed42 = 选择-过拟合已识别未部署（selected_not_validated）"
integrity_negative_declaration: "已读一手证据中未发现 test-item gold 进入 selector/reward/prompt/检索/候选构造的泄漏;全部 oracle 行显式标注为上界/干净文本基线非部署数字;确证的两起信息问题 = R3 transductive exemplar 污染（已 superseded #33）与 R2 oracle-layer-selection artifact（已更正为 null）——完整链条 §4.4 并列保留"
out_of_repo_attestation: "owner attestation（TEAM_ATTESTATION 级,不称机器证明）:四仓之外无未入仓的研究模型运行面;W4 legacy `omni_embedding/` 原始 artifact 不在仓内（gitignored）,其 sanitized 摘要以 dialect_route_table.md 等为准,granularity=LOW 如实标注"
---

# INHERITED_PRIOR_EXPOSURE union v2

## §1 W1 + umbrella 侧 exposure 事件表（27 件,按日期升序;逐件带证据指针;v1 原表保留——事件 #1–7 与 §4 组 D/R 同源,见 frontmatter 去重注记）

| # | 日期 | 模型 | 触碰类型 | 数据集与规模 | 产出指标 | 证据指针 |
|---|---|---|---|---|---|---|
| 1 | 06-22 | omni-embed-nemotron-3b | 冻结嵌入+kNN 探针,37 层/池化 sweep | CREMA-D dev600/test300 | content≈0.99/emotion 0.36–0.40/speaker≈chance | archive/2026-06-22-omni-embed-speech-disentanglement-1.1.1.md |
| 2 | 06-23 | omni-embed-nemotron-3b | Operator-A pooling sweep（D3） | CREMA-D seeds 42&7 | attentive@L16 情感 0.40→0.51/0.45 | DL 06-23;MLflow 2c61b2f1/21453cb1 |
| 3 | 06-23 | omni-embed-nemotron-3b | ICL/few-shot 探针（1.2.1） | CREMA-D | 情感 few-shot 0.217→0.150（负结果） | DL 06-23 1.2.1 条 |
| 4 | 06-24 | omni-embed-nemotron-3b | Wave 0.2 复现 | CREMA-D | 三因子先验复测确认 | archive/2026-06-24-tfrl-validation-run-log.md |
| 5 | 06-24 | omni-embed-nemotron-3b | Wave 1 语言+意图 kNN | MINDS-14 en-US dev280/test257 | 意图 0.25≫chance,不可 steer | 同上 §Wave1 |
| 6 | 06-24 | omni-embed-nemotron-3b | Wave 1b 情感 pooling gain | CREMA-D | attn@L16 +0.097 | archive/2026-06-24-emotion-pooling-…-gain.md |
| 7 | 06-24 | omni-embed-nemotron-3b | Wave 1c 意图 pooling sweep | MINDS-14 | Δ=−0.058（pooling 伤意图,负结果） | 同上 §Wave1c |
| 8 | 07-02 | qwen3-omni-30b Q8_0 GGUF | 真 best-of-N/MBR/oracle ASR | LibriSpeech n=144,pool=8,SNR5 | oracle 头空 +0.042[0.029,0.056]@N=8;MBR ns | _repro/asr_bon_llamacpp_snr5.json |
| 9 | 07-03 | qwen3-omni-30b GGUF | M3 phase-0 zero-support 探针 | LibriSpeech 稀有实体 36 utts×32 samples | match 0.381[0.245,0.518] | _repro/m3_phase0_zero_support.json |
| 10 | 07-03 | qwen3-omni-30b GGUF | M5 selector confirmatory | LibriSpeech n=144/12 speakers | selector red_vs_mbr≈0（null） | _repro/m5_selector_confirmatory.json |
| 11 | 07-04 | qwen3-omni-30b GGUF | CP-1 SQA H_prompt−H_fix | MMAU-mini n=150 | oracle 头空~0.15;H_prompt−H_fix=0.02 | _repro/cp1_sqa_hprompt_mmau.json |
| 12 | 07-04 | qwen3-omni-30b GGUF | CP-3 label-free selector 兑现 | MMAU-mini n=150 | 头空 0.14;majority/self-certainty ρ≈0 | _repro/cp3_selector_realization_mmau.json |
| 13 | 07-04 | qwen3-omni-30b GGUF | CP-1 声学条件化审计 | MMAU-mini n=150 | variants 0.587–0.653 | _repro/cp1_multimodal_feature_audited_mmau.json |
| 14 | 07-04 | qwen3-omni-30b GGUF | H_prompt vs H_fix 探针 | LibriSpeech n=50（排除既暴露 ids） | directional-only | _repro/probe_hprompt_vs_hfix.json |
| 15 | 07-05 | qwen3-omni-30b GGUF | P2 oracle 头空扫描 best-of-8 | 7 集各 n=150 | bba 0.28/SQuAD-zh 0.14/MMAU 0.147… | _repro/p2_baselines.json |
| 16 | 07-05 | qwen3-omni-30b GGUF | E7 few-shot/E8 prompt-opt/E10(+b) verifier | 4 集 n=24–40 | 全 lever rel_gain≈0（null） | _repro/e7/e8/e10/e10b/dec_synthesis.json |
| 17 | 07-05 | qwen3-omni-30b GGUF | M3 cross-modal（真转写注入） | SQuAD-zh/vocalbench-zh 各 n=150 | +0.06/+0.10（gold-注入边界告警在案） | _repro/m3_crossmodal.json |
| 18 | 07-05 | qwen3-omni-30b GGUF | T2/T3/T6 | MMAU/vocalbench-zh/SQuAD-zh n=25–90 | T2/T3 n.s.;T6 P@k 0.62 | _repro/t2/t3/t6_*.json |
| 19 | 07-06 | qwen3-omni-30b GGUF | P6 perception-delta 两臂 | 3 集各 n=60 | SQuAD-zh +0.283 SIG | _repro/p6_perception_delta.json |
| 20 | 07-07 | qwen3-omni-30b GGUF | T0/T7/T8/T9/T10（RAG-gate/反事实/2-turn 工具） | bba/vocalbench-zh/SQuAD-zh n=34–60;KB 403 passages | T7 H0 0.517;T9 CF-follow 0.237;T10 0.175→0.35 | _repro/t0/t7/t8/t9/t10_*.json + t7_errata.md |
| 21 | 07-09→10 | qwen3-omni-30b + MERaLiON-2 双 GGUF | **Wave-1 冻结基线网格**（最大单一 exposure） | 224 格核心（56 集×2 底座×dev40/test60);实盘 464 结果件,qwen ~72 键/meralion ~56 键 | 全表 = wave1_results.md | _repro/wave1_results.md + _repro/baselines/*.json;DL 续5/6 |
| 22 | 07-09 | 30B + MERaLiON-2-3B | Step-0 活体 smoke | 少量 smoke item（bba×dev n=40 单格） | embedding HTTP200 dim2048;转写命中 | DL 续4/5 |
| 23 | 07-10→12 | GLAP/LCO-3B/LCO-7B/30B own-embed/MERaLiON-SE2/CLAP/composite(ERes2NetV2+Emotion2Vec) | KB 建库音频嵌入 + 10 CPU 嵌入器冒烟 | 4 集每源 n=50–180;glap 2704/llama-embed 720/… | 63 源 CLEAN | _repro/kb_content_inventory_20260712.json;DL 续14 |
| 24 | 07-11 | qwen3-omni-30b GGUF | ASR best-of-N v2（clean 重做+selector 电池） | LibriSpeech test.other n=96,pool=8×3 seeds | logprob-conf = 该 selector 电池中仅有的 CI 排零 deployable selector | _repro/asr_bon_v2_*.json;DL 续13 |
| 25 | 07-11 | 30B（+omni-embed 池化侧,规模 UNCERTAIN） | MInDS v2 真 zero-shot;CREMA 多 fold-seed | MInDS-14;CREMA-D | MInDS 反降 0.245（旧增益系 card+transductive);CREMA sub-SESOI | DL 续13/14 |
| 26 | 07-13 | qwen3-omni-30b GGUF | CP-1 SLU H_prompt−H_fix | MInDS-14 n=150 | 头空~0.027;H_prompt−H_fix=0.0 | _repro/cp1_slu_hprompt_minds14.json |
| 27 | ~07-11 起 PARKED | GLAP | squtr 全语料嵌入构建（corpus 侧） | **31000/57638 docs 已嵌后封存** | 无最终指标 | commit 64d697c;DL 续26/27 |

## §2 失败加载/未触碰数据（experiment_attempt,不计入 union）

minicpm-o-4.5（两轮加载失败）/ moss-audio-8b（打包缺陷）/ qwen3-omni HF-int4+vLLM 路
（失败,后由 GGUF 路成功=事件 8 起）/ nemotron 生成底座（EXEMPT）/ Qwen2-Audio（stub,从未
实跑）。

## §3 对后续设计的强制约束

1. **held-out/预注册**：任何未来评测切片必须对照本件全表（§1+§4）做 exposure 检查——已
   暴露 item 集（W1 侧:LibriSpeech 144+36+50+96、MMAU-mini 150、各 n=150 切片、Wave-1
   dev40/test60 全网格;W4 侧:**CoVoST2 val 1758+locked test 1695**、HeySQuAD val200/422、
   URO 200、SLURP 500、MInDS 180/437、CREMA-D dev600/test300、FLEURS、Spoken-SQuAD、
   AISHELL-63、WenetSpeech-Wu 21）**显式排除或分层降级**,不得混作 fresh;frontmatter
   selection_contamination 列出的 ≥11 条选择运行的数据集×split 为最高优先隔离面。**本 v2
   完成前冻结的任何 fresh/held-out 切分无效（v5 复审 Round B 裁定);自 v2 起解除该冻结**。
2. **等级**：本表全部数字 = PRE-METHODOLOGY_DIRECTIONAL_EVIDENCE / hypothesis-grade,永不
   自动升级;引用必须带本件指针。
3. **缺口状态（v2 更新）**：W4 全仓历史考古完成（§4;残余 UNCERTAIN 项逐条列于 §5,含 legacy
   granularity=LOW 与 verifier 实名未钉）;W2/W3 零实验直验;仓外边界 = owner attestation
   （frontmatter）。发现新历史触碰 → append 本表并注日期,不改写既有行。

## §4 W4 仓（speech-mllm-omni-embedding-rl）exposure 补全（v2;考古代理全历史扫描,主执行方法证抽查）

仓范围：初始 52adeca（2026-06-07）→ HEAD 88dc775（2026-07-12,早于 gate 冻结 af96a89——
new_touches_since_freeze=0 签字不受影响）。型缩写：EMB=嵌入/检索,GEN=生成,RRK=rerank/
verifier,RTE=路由,PRB=探针,MEM=memory-use,SMK=smoke,LOAD=纯加载,FAIL=失败已处理。

### §4.1 事件行（按群组;「选择」列=是否用于选参/选 exemplar/选阈值/selection-locked）

**群组 L — legacy 归档（≤06-23;原始 artifact 不在仓内,granularity=LOW）**：
L1 AISHELL-1 test63 路由诊断（ASR 0.952/omni 0.762/RRF 0.937,负控）;L2 WenetSpeech-Wu
test21 路由（omni-primary +0.571 CI[0.381,0.762] 12/0）;L3 Chinese synthetic RAG 30/120/600
定性诊断;L4 audio-tower LoRA RAG600（**改权重,本线外,仅备案**）;L5 音频 codec 探索
（EnCodec/DAC/Mimi,边界项）;L6 ASR-mediated text 路线叙述。证据 = dialect_route_table.md
+ changelog 索引;UNCERTAIN 如 §5。

**群组 D — CREMA-D 解耦+模型理解探针（omni-embed-nemotron-3b,06-22..24;与 §1 事件 #1–7
同战役同源）**：D1–D3 双因子/content/层-池探针（speaker 不可恢复,emotion 天花板 ~0.40）;
D4 Hydra smoke×8;D5 P0–P7 契约探针;D6 pooling 轴;D7 泛化 harness + MInDS loader
（LibriSpeech 仅 loader 无运行,不计入）。证据 = commits db84a7a/923ad1d/ee146b4/a5a6c85/
9f1a6b9/452bd8b + outputs/ 日志。

**群组 S — 语义冻结基准（06-23..24）**：S1/S1b FLEURS 60（饱和;v2 literal boundary 选择）;
S2 FLEURS en→fr 57;S3 Spoken-SQuAD smoke;S4 HeySQuAD train60（**选择;train 正 val 反转的
accept-gate 教训**）;S5 HeySQuAD final-answer 60;S6 tool/intent 基线;S7/S8 URO 200
（card +0.335 CI[0.265,0.405]）;S9 URO rerank（0.715→0.845,26/0）;S10 HeySQuAD rerank
60;S11 SLURP 500 schema（0.522→0.894）;S12 MInDS 180 schema（0.856→0.972）;S13/S14/S15
FLEURS/CoVoST2 60/200 card;**S16 CoVoST2 ar→en val 1758 选 boundary-card → locked test
1695:0.635→0.753 +0.117 CI[0.099,0.138]（选择,规范 val/test 分离,最大规模真运行）**;
S17 margin gate 1695。

**群组 H/SEL — HeySQuAD 扩量+V2 sweep+任务级选择器（06-25..26）**：H1 val-100;**H2
answerable val-200（raw 0.900/policy_grounding 0.875——train60 正结果被推翻）**;
**V2sweep 五族任务条件指令（选择;含评审点名 HeySQuAD V2 109:0.917→0.899 负）**;H3
bad-case 修复;**SEL1 URO 任务级选择器（选择-locked,+0.0875 7/0）**;**SEL2 URO 3×3 grid
5-seed（选择-locked;seed42 selected_not_validated = 选择-过拟合已识别未部署）**;SEL2b
taxonomy 5-seed;V3 margin-gated gate75。

**群组 F — 选择器/verifier 正式化（07-01..02）**：F1 SLURP same-family gate 5-seed（选择）;
**F2 SLURP 500 formal selector（选择-locked;locked 0.620→0.665 +0.045 CI[0.010,0.080]
11/2——评审点名项,inventory:95 逐字核verified）**;F3 SLURP low-margin verifier（0.550→
0.676/0.690,0 reg）;**F4 MInDS 180 low-margin verifier（0.883→0.956 +0.072 13/0——评审
点名项）**;F5 CoVoST2 ar/zh 200 verifier;**F6 MInDS formal selector（选择-locked,负——
raw fallback,评审点名项）**;F7 CoVoST2 任务级选择器 5-seed（no_stable_policy,严格无泄漏
行为）。

**群组 C — 跨模型/后端**：C1 jina omni-small CoVoST2 zh 200（media-path 0.845;dict
payload=接口误用 sanity）;**C2 jina URO/MInDS/SLURP/CoVoST2 系统侧 card（SLURP 0.502→
0.772 +0.270——评审点名 Jina 项）**;C3 jina 指令/tuple 5-seed（全 raw fallback）;C4
AutoRound-Int4 Qwen3-Omni vLLM（**LOAD-ONLY**）;C5/C5b Qwen3-Omni GGUF（LOAD-ONLY/失败
smoke）;C6–C8 Gemma-4-E4B 生成 V3 smoke→matrix→CoVoST2 selection/locked（C8 选择）;C9/C10
memory-use smoke/V0;C11 Gemma-4-12B 后端诊断（N=49 −0.306,负）;C12/C12b Voxtral Mini 3B
（N=60 Acc 0.617 欠功效/12 行 smoke 日期 UNCERTAIN）;C13 Qwen3-Omni chat 候选选择
（timeout 2/2,FAIL 单列）。

**群组 M — omni agentic memory-use（Gemma-4-E4B + omni-embed,07-01..03）**：M1 稳定性/
压测;M2 query-audio 门（+0.127 over text-only）;M3 HeySQuAD val-200 检索→use/packed
（0.280→0.595）;M4 Spoken-SQuAD test-200 transfer;M5 MInDS query-signal 审计;M6 CoVoST2
order 控制+multivote gate;M7 URO 8 族 final-task use（7/8 族改进 26/0）;M8 HeySQuAD 422
补充;M9 evidence-order shuffle 控制。

**群组 R — _repro 可复现件/诚信整改（07-01..12）**：R1 paralinguistic 负探针（诚实 null）;
**R2 emotion pooling paired v2（across-seed NULL;单-seed +0.097 = oracle-layer-selection
artifact,已更正）**;**R3 MInDS paired 182 手工 JSON（SUPERSEDED #33,transductive 污染）**;
R4 speaker restatement;**R5 GroupKFold 说话人分组重做（+0.0270 CI[0.0141,0.0401]
bounded<SESOI;speaker-free 主张 retired #34）**;**R6 MInDS v2 clean factorial（126/437
disjoint;instruction_only 回归 −0.245;残余 ~3% 表面重叠已披露）**;R7→R8 multiplicity
7/7→**5 独特对比 5/5 survive**（superseded-note 在案）。

### §4.2 评审点名七族核查（全部映射,零排除）

SLURP 500 formal selector→F2（+F1/F3/S11/C2）;MInDS formal selector+low-margin verifier→
F6（负）+F4（+S12/M5/R3/R6 事故链）;URO-Bench 200 多 selector→SEL1/SEL2/SEL2b/V3/M7
（+C2）;HeySQuAD 200/109→H2+V2sweep-109（+S4/S5/S10/M3/M8/M9）;CoVoST2 1758/1695→S16
（+S17/F5/C1/C3）;Jina 跨模型→C1/C2/C3;WenetSpeech-Wu 路由→L2（+L1 负控）。

### §4.3 MInDS-14 事故完整时间线（诚信更正链,并列保留）

①06-24 干净 180 行审计（0.856→0.972）→ ②06-25 提交 repro 脚本 → ③07-01 提交**手工组装**
182 行 JSON（0.857/+0.126）→ ④法证审计三宗：**JSON 手工组装**（脚本只写 WAV+manifest,无
结果 JSON 写出——考古代理逐行核实）、**数值不匹配**（JSON 0.857/+0.126 vs inventory
0.852/+0.132,两数并列保留——主执行方 inventory:87 逐字核verified）、**transductive 污染**
（42/182 eval 行即 card exemplar）→ ⑤07-11 SUPERSEDED #33,旧件 append-only 冻结 →
⑥07-11 clean redo（126/437 disjoint;instruction_only −0.245;~3% 表面重叠披露;v2 脚本
原子写单一 writer 亲验）→ ⑦harden（fold-seed 4/4）→ ⑧07-12 multiplicity 更正 7→5 独特
对比,5/5 survive（88dc775）。**新发现（本考古,主执行方核实）**：superseded-note 引用的
`docs/claim_ledger.yaml` **untracked 且不在盘 = 悬空引用**——登记为 W4 侧待修簿记项
（主动披露,随回应信报评审）。

### §4.4 其他更正/污染事件（并列保留）

R2 oracle-layer artifact→R5 分组重做（speaker-free retired #34）;SEL2-seed42 选择-过拟合
（selected_not_validated,未部署）;R1/R4 paralinguistic 诚实 null;S4→H2 train-正-val-负
accept-gate 教训。

## §5 W4 扫描覆盖声明（置信度如实）

**HIGH（一手通读;二轮收敛）**：inventory 261 行全文/14 个 _repro JSON/旧 MInDS JSON 全文+
superseded note/git 全历史 52 commit/outputs Hydra 日志/8 个 docs 汇总件/3 个模型卡/
**changelog 4172 行全通读**（59 运行事件,其子代理中转表交叉核对）/法证四项（旧脚本无 JSON
写出、v2 原子写、claim_ledger 悬空、legacy 目录不在仓——主执行方另抽查 inventory 87/95 行
逐字、三件 _repro 在盘、claim_ledger 连盘上不存在）。**MEDIUM（残余低概率遗漏面,如实标注）**：
project_status(103KB)/decisions(60KB)/benchmark_plan(76KB) 正文未逐行——若其中存在未被
changelog/inventory 索引的孤立小 smoke,存在低概率遗漏。
**UNCERTAIN（逐条,宁多列不编）**：①外部 LLM verifier 实名（DeepSeek vs OpenAI-兼容未钉）;
②M3/M4/M8 生成器身份（几乎确定 Gemma-4-E4B）;③LibriSpeech 仅 loader 不计入;④C5b/C12b
回溯 smoke 日期;⑤legacy L3–L6 无日期无离散指标;⑥本表 ≈68 行 vs changelog 子代理独立计数
59 = 拆分粒度差异非矛盾（其 59 行表本体经主会话中转恢复,已交叉参照）;⑦AMI/LibriSQA 仅
计划未跑。
