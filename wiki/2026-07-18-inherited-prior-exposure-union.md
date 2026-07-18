---
artifact_id: "INHERITED-PRIOR-EXPOSURE-UNION-2026-07-18-01"
title: "INHERITED_PRIOR_EXPOSURE union——项目历史研究模型触碰事件全量登记"
date: 2026-07-18
authority: "阶段正典 v2 四字段记账之 legacy_experiments 字段的正典载体（owner 裁决② 2026-07-18:历史实验不删除、不降格、不假装未发生）"
method: "档案考古代理（Opus）扫 Decision-Log 全文（2497 行,2026-06-22→07-13 实验条目精读+12 类关键词全文 grep）+ W1 _repro/ 全部结果件 meta + baselines 464 件文件名聚合 + wiki/archive/;主执行方抽查 6/6 证据指针在案、baselines 计数精确吻合"
discipline: "「模型触碰」= 研究模型的推理/评测/嵌入计算（含 smoke/单 item/失败但已处理数据);纯下载/校验/加载失败单列不计入;无证据的传闻不列;UNCERTAIN 如实标注。本 union 是后续 held-out/预注册/验证集设计必须显式排除或分层处理的暴露面;所有历史数字维持 PRE-METHODOLOGY_DIRECTIONAL_EVIDENCE 等级（阶段正典 v2 墓碑透镜）"
summary: "27 个 exposure 事件 / ~11 个 distinct 模型 / 数据集并集 = CREMA-D、MINDS-14(+zh)、LibriSpeech(含 test.other/稀有实体切片)、MMAU-mini、SQuAD-zh、OpenbookQA-zh、vocalbench-*、spoken-squad、big-bench-audio、heysquad、squtr(含全语料 31000/57638 文档侧) + Wave-1 基线网格 ~72 键全集(aishell-1/seed-tts-eval/thchs-30/air-bench-*/mmar/mmsu/audiocaps-qa/uro-bench-*/voicebench-*/meld/esd/fleurs-r/slurp/speech-massive-* 等,完整键名 = _repro/baselines/ 与 wave1_results.md)"
known_gap: "W4 仓（speech-mllm-omni-embedding-rl,gitignored 独立仓）未在本扫描面——可能存在额外 omni-embed 检索/rerank 触碰,标 UNCERTAIN 待另行考古（登记为本件已知缺口,不销账）"
---

# INHERITED_PRIOR_EXPOSURE union

## §1 exposure 事件表（27 件,按日期升序;逐件带证据指针）

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
| 24 | 07-11 | qwen3-omni-30b GGUF | ASR best-of-N v2（clean 重做+selector 电池） | LibriSpeech test.other n=96,pool=8×3 seeds | logprob-conf = 唯一 CI 排零 selector | _repro/asr_bon_v2_*.json;DL 续13 |
| 25 | 07-11 | 30B（+omni-embed 池化侧,规模 UNCERTAIN） | MInDS v2 真 zero-shot;CREMA 多 fold-seed | MInDS-14;CREMA-D | MInDS 反降 0.245（旧增益系 card+transductive);CREMA sub-SESOI | DL 续13/14 |
| 26 | 07-13 | qwen3-omni-30b GGUF | CP-1 SLU H_prompt−H_fix | MInDS-14 n=150 | 头空~0.027;H_prompt−H_fix=0.0 | _repro/cp1_slu_hprompt_minds14.json |
| 27 | ~07-11 起 PARKED | GLAP | squtr 全语料嵌入构建（corpus 侧） | **31000/57638 docs 已嵌后封存** | 无最终指标 | commit 64d697c;DL 续26/27 |

## §2 失败加载/未触碰数据（experiment_attempt,不计入 union）

minicpm-o-4.5（两轮加载失败）/ moss-audio-8b（打包缺陷）/ qwen3-omni HF-int4+vLLM 路
（失败,后由 GGUF 路成功=事件 8 起）/ nemotron 生成底座（EXEMPT）/ Qwen2-Audio（stub,从未
实跑）。

## §3 对后续设计的强制约束

1. **held-out/预注册**：任何未来评测切片必须对照本表做 exposure 检查——已暴露 item 集
   （尤其 LibriSpeech 144+36+50+96、MMAU-mini 150、各 n=150 切片、Wave-1 dev40/test60 全
   网格）**显式排除或分层降级**,不得混作 fresh。
2. **等级**：本表全部数字 = PRE-METHODOLOGY_DIRECTIONAL_EVIDENCE / hypothesis-grade,永不
   自动升级;引用必须带本件指针。
3. **已知缺口**：W4 仓未扫（frontmatter known_gap）;发现新历史触碰 → append 本表并注日期,
   不改写既有行。
