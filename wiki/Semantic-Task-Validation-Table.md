# Semantic-Task Validation Table (Stage-1 directional worth-investment checks)

> **We are in Stage 1 (theoretical / problem validation).** Per the CLAUDE.md methodology, the
> experiments below are **small-sample, simple, directional** — each is a cheap "is this direction
> worth investing in?" check on a K2-selected candidate problem, **not** a large-scale Stage-2
> validation. Sample sizes are deliberately small (≈50–150 items); a positive directional signal is
> what justifies the later Stage-2 investment (a fresh Research-Proposal-Template instance with powered
> n, frozen criteria, full controls). A null/weak directional signal is an equally valid outcome that
> argues *against* investing further in that problem.
>
> **Purpose.** The maintainable master table of our flagged speech **semantic** tasks (ASR/ST · SLU ·
> Spoken-QA/audio-reasoning · Speech-Agentic), each with its **validation set** (a small slice),
> **validation goal** (which yardstick quantity / candidate problem it probes), and **validation
> scheme** (the cheap directional procedure). Candidate problems: **CP-1** (H_prompt − H_fix), **CP-3**
> (ρ(ASR)), **CP-8** (calibration + PMI on the SLU/MCQ surface), **CP-4** (voice-agent pass@k). Record:
> [[2026-07-04-stage1-problem-definition]] (K2-resolved), [[2026-07-04-sufficiency-yardstick-memo]],
> [[2026-07-04-stage1-semantic-tfrl-survey]].
>
> **Maintenance rule.** The **Result** column is filled from committed `_repro/*.json` artifacts; every
> in-house number carries a grade tag — at Stage 1 that is `[directional | small-n | not
> significance-bearing]`. A directional result never confirms/establishes anything; it only signals
> whether Stage-2 investment is warranted. On-disk facts from the 2026-07-04 dataset profile.

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
| **librispeech** | `test.other` 2,939 · `test.clean` 2,620 · `validation.other` 2,864 · `validation.clean` 2,703 (parquet, audio bytes) | WER (`asr_reward`) | **CP-3**, CP-1(ASR), CP-2 | ρ(ASR): what fraction of oracle headroom a label-free selector harvests; H_prompt−H_fix on ASR | CP-3 (**GPU, modern selectors** — NOT n-gram/n-best rescoring): regenerate pools **with per-token logprobs**, then compare **self-certainty** (omni token-confidence), a **frozen-LLM reranker/judge** (the omni or a modern text LLM scoring candidates), and consensus/MBR vs the pool oracle. CP-1: K-instruction scored search, oracle-over-K vs fixed, on a fresh `test.other` slice + random-instruction control | **needs llama-server (GPU)** | — |
| **covost2** | `dev`/`test` per pair (e.g. `es_en` test) — TSV | BLEU/chrF (`bleu`/`chrf`) | CP-1(ST), CP-2 | H_prompt−H_fix on ST | (deferred) | **BLOCKED — audio absent** (needs Common Voice, not in frozen set); no source-sentence column | — |
| **fleurs-r** | 12 langs · `test.tsv` (~264/lang) | WER/CER; LID acc | CP-1(ST/LID) | H_prompt−H_fix on ST/LID | (deferred) | **BLOCKED — audio tarred**, 2 incomplete `.aria2`; no translation column (ST needs cross-lang pairing) | — |

## 2. SLU (intent / slot)

| Dataset | 验证集 (split · n) | Verifiable reward | Serves | 验证目标 | 验证方案 | Status | Result |
|---|---|---|---|---|---|---|---|
| **minds14** | en-US n=150 (E1); full `all/train` 8,168 available | intent accuracy; `intent_class` 14 ClassLabels | **CP-1(SLU)**, CP-8 | H_prompt−H_fix on intent | E1 (done): 8 task-def × 1 vs 1 fixed × 8, matched budget 8 | ✅ E1 done | **H_prompt−H_fix = +0.000** (CI [−0.02,+0.02]); greedy=majority **0.953** (near-saturated), oracle_fix=prompt 0.980; b2-share (vs random-label floor) +0.013 (CI [0.0,+0.033]); best instr = the fixed one 143/150. `[directional, n=150]`. **Read: prompt-space ≈ nil on easy intent; surface near-ceiling.** `_repro/cp1_slu_hprompt_minds14.json` |
| **slurp** | `test` 2,974 · `devel` 2,033 (jsonl + FLAC real/synth) | intent acc/F1 (`intent`) + **slot-F1** (from `entities`) | CP-1(SLU), CP-8 | H_prompt−H_fix on intent+slot | as minds14, plus slot-F1 arm | **Ready — needs slot-F1 reward** | — |
| **speech-massive** | `validation` 24,396 (12 langs × 2,033); `train_115` few-shot | intent acc/F1 (`intent_str` string) + slot-F1 (`labels`/`annot_utt`) | CP-1(SLU), CP-8 | H_prompt−H_fix on multilingual intent+slot | as minds14 (string label, no map needed) | **Ready (eval-only, NC license)** | — |

## 3. Spoken-QA / audio reasoning (MCQ & extractive)

| Dataset | 验证集 (split · n) | Verifiable reward | Serves | 验证目标 | 验证方案 | Status | Result |
|---|---|---|---|---|---|---|---|
| **mmau-mini** | n=150 (E3, E4, E6′); full `test_mini` 1,000 | MCQ accuracy | **CP-1(SQA)**, **CP-3(ρ)**, CP-1(multimodal-b), CP-8, CP-5 | H_prompt−H_fix on MCQ (E3); ρ realization (E4); multimodal-conditioning (b) (E6′) | E3: 8 task-def × 1 vs 1 fixed × 8, budget 8. E4: modern label-free selectors on the SAME slice's pools. E6′: FBank-invariance-audited acoustic conditioning | ✅ E3 + E4 + E6′ done | **E3:** greedy=majority **0.640**; **H_fix = +0.133** (oracle 0.773 — support REAL) but **H_prompt−H_fix = +0.020** (n.s.). **E4 (ρ):** greedy 0.633, oracle 0.773 (**headroom +0.140**); self-certainty **ρ=0.0**, majority/conf-vote **ρ=−0.047**, LLM-judge **ρ=0.143 n.s.** — **no label-free selector significantly beats majority**. **E6′ (multimodal b) — CORRECTED post-review:** apparent H_mm=+0.060 is a **speed-driven artifact** — recompute {original,trim}=0.640=greedy → **+0.000**; the time-averaged mel gate can't see temporal leakage (±10% speed passes at 0.993). **No valid multimodal gain established**; M2/M3 untested. `[directional, n=150]`. **Read (v2, strict-reviewed): (a) support REAL (sampling +0.13, one measurement); (b) NAIVE text-prompt inert (optimized search unrun); (c) CHEAP self-referential selection under-harvests (trained-verifier class untested; best self-judge ρ=0.143 under-powered positive). "Space insufficient" NOT established — open problem is (c) realization.** `_repro/cp1_sqa_hprompt_mmau.json`, `_repro/cp3_selector_realization_mmau.json`, `_repro/cp1_multimodal_feature_audited_mmau.json`. See [[2026-07-05-Q1-conclusion-review-synthesis]] |
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

## 6. Execution order (small directional GPU checks on the frozen omni; modern selectors only)

> **Methodology note (owner steer, 2026-07-04).** (a) **Stage 1 = small samples.** Each check uses a
> small slice (≈50–150), simple design, just enough to see whether the direction shows a signal worth
> a Stage-2 investment — no large-n runs here. (b) **GPU + modern models.** Checks run on the frozen
> omni (llama.cpp Qwen3-Omni-30B) and modern LLM selectors; **no n-gram / n-best LM rescoring** (that
> classical path is off-thesis and was reverted). "Cheapest first" means smallest slice / reuse of
> generations, never a fallback to traditional CPU methods.

1. **CP-1 SLU arm on MInDS-14** — K task-definition instructions × N on the frozen omni; oracle-over-K
   intent accuracy vs the fixed instruction, + a random-instruction control (b1 floor). The
   probe-favored schema-rich surface with the +0.126 [scoped] in-house precedent. **First experiment.**
2. **CP-8 calibration on MInDS-14 intent** — contextual/Batch calibration + PMI over the 14-way choice
   surface; calibrated-vs-raw accuracy and distractor-rephrase variance. Reuses arm-1 generations.
3. **CP-1 SQA arm on mmau-mini / big-bench-audio** — MCQ oracle-over-K on the frozen omni.
4. **CP-3 selector anatomy** — regenerate ASR pools **with per-token logprobs**; compare self-certainty,
   a frozen-LLM reranker/judge, and consensus/MBR vs oracle. (Modern selectors; supersedes the reverted
   n-gram attempt.)
5. **CP-4 pass@k on voicebench verifiable subtasks** — N-rollout agent harness, last.

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
