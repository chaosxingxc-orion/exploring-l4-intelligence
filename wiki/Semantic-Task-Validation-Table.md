# Semantic-Task Validation Table (Stage-2 living document)

> **Purpose.** The maintainable master table of our flagged speech **semantic** tasks (ASR/ST · SLU ·
> Spoken-QA/audio-reasoning · Speech-Agentic), each with its **validation set**, **validation goal**,
> and **validation scheme** — the engineering anchor for the Stage-2 experiments on the K2-selected
> problems **CP-1** (quantify H_prompt − H_fix), **CP-3** (measure ρ(ASR)), **CP-8** (calibration + PMI
> on the SLU/MCQ surface), **CP-4** (voice-agent pass@k). See the Stage-1 record:
> [[2026-07-04-stage1-problem-definition]] (K2-resolved), [[2026-07-04-sufficiency-yardstick-memo]]
> (the H_fix / H_prompt / ρ yardstick), [[2026-07-04-stage1-semantic-tfrl-survey]] (the reviewed survey).
>
> **Maintenance rule.** This table is updated as experiments run: the **Result** column is filled from
> committed `_repro/*.json` artifacts, and every in-house number carries its grade tag
> (`[directional]` small-n → `[scoped]` → validated). On-disk facts (splits, counts, fields) come from
> the 2026-07-04 dataset profile; re-profile with `scripts/profile_semantic_datasets.py` if the
> frozen set changes.

## 0. The yardstick quantities each experiment measures (validation goals, defined once)

Per task family T (survey §2.2): **H_fix(T,N)** = oracle-over-sampling headroom under one fixed
instruction (does q₀ hold high-reward mass? — condition **a**). **H_prompt(T,K,N)** = oracle headroom
over K instructions × N rollouts; **H_prompt − H_fix** = the prompt-space contribution (condition
**b**, split **b1** format vs **b2** genuine accuracy). **ρ(T)** = fraction of oracle headroom a
label-free selector realizes (condition **c**). **Δ_BM** = the matched-budget diversity contrast the
Stage-1 probe measured (≠ H_prompt − H_fix). CP mapping: **CP-1** measures H_prompt − H_fix; **CP-3**
measures ρ; **CP-8** measures the b2/c share attributable to scoring-surface bias; **CP-4** measures
pass@k (H_fix) + reward-realized ρ on agent rollouts.

---

## 1. ASR / ST

| Dataset | 验证集 (split · n) | Verifiable reward | Serves | 验证目标 | 验证方案 | Status | Result |
|---|---|---|---|---|---|---|---|
| **librispeech** | `test.other` 2,939 · `test.clean` 2,620 · `validation.other` 2,864 · `validation.clean` 2,703 (parquet, audio bytes) | WER (`asr_reward`) | **CP-3**, CP-1(ASR), CP-2 | ρ(ASR): what fraction of oracle headroom a label-free selector harvests; H_prompt−H_fix on ASR | CP-3: re-score the committed C1 pools (`_repro/asr_bon_llamacpp_snr5.json`, 144 utts × 8) with self-certainty + frozen-LM PLL-MBR utility + overlap-MBR vs pool oracle — **CPU, no generation**. CP-1: K-instruction scored search, oracle-over-K vs fixed, on a fresh `test.other` slice + random-instruction control | **CP-3 ready (on-disk pools)**; CP-1 needs llama-server | — |
| **covost2** | `dev`/`test` per pair (e.g. `es_en` test) — TSV | BLEU/chrF (`bleu`/`chrf`) | CP-1(ST), CP-2 | H_prompt−H_fix on ST | (deferred) | **BLOCKED — audio absent** (needs Common Voice, not in frozen set); no source-sentence column | — |
| **fleurs-r** | 12 langs · `test.tsv` (~264/lang) | WER/CER; LID acc | CP-1(ST/LID) | H_prompt−H_fix on ST/LID | (deferred) | **BLOCKED — audio tarred**, 2 incomplete `.aria2`; no translation column (ST needs cross-lang pairing) | — |

## 2. SLU (intent / slot)

| Dataset | 验证集 (split · n) | Verifiable reward | Serves | 验证目标 | 验证方案 | Status | Result |
|---|---|---|---|---|---|---|---|
| **minds14** | `all/train` 8,168 → self-split (seed-frozen dev/test); en-US subset ~563 | intent accuracy / macro-F1 (`classification_accuracy`/`macro_f1`); `intent_class` int ClassLabel (14 intents) | **CP-1(SLU)**, CP-8 | H_prompt−H_fix on intent (the probe-favored schema-rich surface; MInDS +0.126 [scoped] is the in-house precedent); CP-8: b2/c share from calibration | CP-1: K task-definition prompts × N, oracle-over-K intent-acc vs fixed + random-instruction control (b1 floor). CP-8: contextual/Batch calibration on the 14-way choice surface, calibrated-vs-raw acc + distractor-rephrase variance | **Ready** (loader + reward to write) | — |
| **slurp** | `test` 2,974 · `devel` 2,033 (jsonl + FLAC real/synth) | intent acc/F1 (`intent`) + **slot-F1** (from `entities`) | CP-1(SLU), CP-8 | H_prompt−H_fix on intent+slot | as minds14, plus slot-F1 arm | **Ready — needs slot-F1 reward** | — |
| **speech-massive** | `validation` 24,396 (12 langs × 2,033); `train_115` few-shot | intent acc/F1 (`intent_str` string) + slot-F1 (`labels`/`annot_utt`) | CP-1(SLU), CP-8 | H_prompt−H_fix on multilingual intent+slot | as minds14 (string label, no map needed) | **Ready (eval-only, NC license)** | — |

## 3. Spoken-QA / audio reasoning (MCQ & extractive)

| Dataset | 验证集 (split · n) | Verifiable reward | Serves | 验证目标 | 验证方案 | Status | Result |
|---|---|---|---|---|---|---|---|
| **mmau-mini** | `test_mini` 1,000 (parquet, audio bytes + `choices` + `answer`) | MCQ accuracy (match to `answer` text) | **CP-1(SQA)**, CP-8, CP-5 | H_prompt−H_fix on MCQ; CP-8: scoring-surface-bias share | CP-1: K instructions × N, oracle-over-K MCQ-acc vs fixed. CP-8: PMI/calibration over the option set, calibrated-vs-raw acc | **Ready** | — |
| **big-bench-audio** | 1,000 (mp3 + `metadata.jsonl`, closed-set `official_answer`) | accuracy (normalized EM, 21-value closed set) | CP-1(SQA) | H_prompt−H_fix on spoken-only reasoning | CP-1 as mmau; spoken-only (model must listen — a natural acoustic-grounding surface) | **Ready** | — |
| **vocalbench** | `knowledge` 2,000 · `reasoning` 1,000 · `robust` 3,600 (parquet audio; **labels in `json/`**) | QA accuracy (from `json/ Answer`) | CP-1(SQA), CP-8 | H_prompt−H_fix; robustness split for acoustic grounding | CP-1 on knowledge/reasoning; robust subset for b2/noise controls | **Ready — read `json/` for labels** | — |
| **heysquad** | `validation` 4,158 (parquet; spoken question + text `context` + gold spans) | extractive-QA EM / token-F1 (SQuAD-2) | CP-1(SQA) | H_prompt−H_fix on extractive spoken-QA | K instructions × N, oracle-over-K EM/F1 vs fixed | **Ready — needs QA-EM/F1 reward** | — |
| **spoken-squad** | `test` 5,351 (parquet; spoken passage in `context`, question in `instruction`) | QA EM / token-F1 | CP-1(SQA) | H_prompt−H_fix on spoken-document QA | as heysquad (note inverted fields: audio = passage) | **Ready — needs QA-EM/F1 reward** | — |
| **mmsu** | (MCQ labels intended) | MCQ accuracy | CP-1(SQA), CP-8 | — | — | **BLOCKED — label parquet not downloaded** (only audio on disk; `data/train-*.parquet` missing; lockfile "COMPLETE" is audio-fingerprint only) | — |
| **mmar** | `MMAR-meta.json` 1,000 (`choices`+`answer`) | MCQ accuracy | CP-1(SQA) | — | — | **BLOCKED — audio tarred** (2.98 GB `mmar-audio.tar.gz` not extracted) | — |

## 4. Speech-Agentic

| Dataset | 验证集 (split · n) | Verifiable reward | Serves | 验证目标 | 验证方案 | Status | Result |
|---|---|---|---|---|---|---|---|
| **voicebench** | verifiable subtasks: `openbookqa` 455 · `mmsu` ~3,574 · `bbh` 1,000 · `sd-qa` 6,083 · `ifeval` 345 (parquet) | MCQ/QA acc (`reference`); IFEval rule-check | **CP-4**, CP-1(SQA) | pass@k (H_fix) + ρ on voice-QA; H_prompt−H_fix | CP-4: sample N answers, pass@k + reference-reward best-of-N on the 4 verifiable subtasks. MCQ options are inside the `prompt` string (parse) | **Ready (openbookqa/mmsu/bbh/sd-qa)**; ifeval needs a rule-checker | — |
| **voiceassistant-eval** | listening: general 799/music 600/sound 394/speech 899; viewing 900 (parquet, `ref_answers`) | accuracy vs `ref_answers` | CP-4, CP-1(SQA) | pass@k + ρ on listening/viewing | CP-4 as voicebench; speaking track (S2S) deferred (needs TTS+judge) | **Ready (listening/viewing)** | — |
| **uro-bench** | verifiable subtasks: `Gsm8kEval` 582 · `OpenbookQA-zh` 189 · `Repeat` 252 · `SQuAD-zh` 153 (parquet, `target_text`) | subtask-specific (Gsm8k EM, OQA acc, Repeat WER, SQuAD-zh F1) | CP-4 | pass@k + ρ on the verifiable URO tracks | CP-4 on the 4 clean-metric tracks; 40-track metric map for the rest | **Ready (verifiable subset)** | — |
| **tau2-bench** | airline 50 · retail 114 · telecom 114 (JSON specs + `db.json`) | task-success / DB-state (`evaluation_criteria`) | CP-4 | pass@k + DB-state ρ on tool-use agent | (deferred) needs the tau2 simulator harness | **BLOCKED — no audio** (text tool-use; voice variant needs TTS) | — |

---

## 5. Engineering checklist (prerequisites, tracked here)

**Loaders to write** (none exist — `common/data/` has only registry specs): one thin loader per ready
dataset returning `(audio_or_path, reference, meta)`; mirror the parquet-bytes pattern already used in
`scripts/repro_asr_best_of_n.py::load_utts`.

**Reward fns to add to `speechrl_common.rl`** (present: WER/ASR, exact-match, classification-accuracy,
macro-F1, BLEU, chrF, EER):
- `slot_f1` (SLURP entities / Speech-MASSIVE `labels`) — for the SLU slot arm;
- `qa_em` + `qa_token_f1` (SQuAD-style, with `is_impossible` handling) — HeySQuAD, Spoken-SQuAD;
- `ifeval_check` (rule-based instruction-following) — VoiceBench/VA `ifeval`;
- tau2 DB-state scorer + LLM-judge/refusal-rate — deferred with CP-4's harder subtasks.

**Provisioning to unblock** (not on the critical path; CP-3/CP-1-SLU/CP-1-SQA proceed without them):
extract `mmar-audio.tar.gz` + fleurs-r tars (finish 2 `.aria2`); fetch mmsu `data/*.parquet` (labels);
covost2 audio needs Common Voice (out of frozen set — a lockfile-expansion decision); tau2 voice needs TTS.

## 6. Execution order (cost-first, per the K2 suggested sequencing)

1. **CP-3 selector anatomy on the committed C1 librispeech pools** — CPU-only re-scoring, no generation,
   directly tests the house `ρ(ASR) ≈ 0` prior with self-certainty + frozen-LM PLL-MBR + overlap-MBR.
   *First experiment; cheapest genuine measurement.*
2. **CP-8 calibration on MInDS-14 intent** — inference-only, schema-rich surface the probe favored.
3. **CP-1 SLU arm on MInDS-14** — K-instruction scored search (the probe-favored family; +0.126 precedent).
4. **CP-1 SQA arm on mmau-mini / big-bench-audio** — MCQ oracle-over-K.
5. **CP-4 pass@k on voicebench verifiable subtasks** — heavier rollout harness, last.

Each experiment: a mini-prereg committed before generation, a `_repro/*.json` artifact with a
`reproduce:` line, paired-bootstrap CIs, and the **Result** column above back-filled with the graded number.

## 7. 中文摘要

本表是语音**语义**任务(ASR/ST · SLU · 口语问答/音频推理 · 语音智能体)的可维护主表,每任务给出
**验证集**(盘上切分+规模)、**验证目标**(充分性标尺量:H_fix/H_prompt/ρ,映射到 K2 选定的
CP-1/CP-3/CP-8/CP-4)与**验证方案**(采样/指令/选择器/指标/预算)。盘上 11 个数据集音频+标签齐全可
立即用;5 个受阻(covost2 无音频、fleurs-r/mmar 音频未解压、mmsu 标签未下、tau2 无音频)。执行按
成本优先:先 CP-3 在已提交的 C1 池上纯 CPU 重打分,再 CP-8 校准、CP-1 的 SLU/SQA 臂、最后 CP-4。
每个实验落 `_repro/` 产物并回填"Result"列,in-house 数字带分级标签。工程前置(loader、缺失奖励、
数据解压)见 §5。
