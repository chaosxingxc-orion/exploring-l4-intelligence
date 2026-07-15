# C1 — Attempt Census (registry vs raw-run set difference) — DRAFT

DRAFT — single-pass AI census (C1/C4), coordinator verification pending; generated 2026-07-14

Scope of this census: umbrella repo `D:/chao_workspace/exploring-l4-intelligence/`
(`docs/`, `wiki/`, `scripts/`), the W1 repo
`projects/speech-mllm-training-free-rl/` (its own git repo: `_repro/`, `docs/`, `configs/`,
`scripts/`, git log), and the Windows-visible data root
`E:/chao_workspace/exploring-l4-intelligence/speechrl-data/` (directory listing only; no binaries read).

Method: file inventory + `git log` + `grep`. No runs executed. Evidence is single-pass; every
unknown is marked UNKNOWN rather than guessed.

---

## Headline finding

**A registry EXISTS — this is NOT a "no registry at all" case — but it is INCOMPLETE by its own
declaration on the dimension C1 exists to cover.** The attempt registry
(`docs/integrity/experiment_attempt_registry.jsonl`, 574 rows) is a **disk-scan of the git-tracked
W1 `_repro/` subtree only**, enriched per-row with `status`/`claim_id`/`inferred`. By the project's
own machine-readable admission (`prior_exposure_registry.json` → `manual_completion_todo[0]` and
`p0_gate_status`), the **config-selection trajectory** — every tried-and-abandoned
prompt/weight/threshold/K/embedder sweep and its abandonment reason — is **only partially recoverable
from disk** and otherwise lives in session logs / human recall. Separately, the **entire E:-drive raw-run
working tree** (`speechrl-data/_repro/`, ~79 top-level entries incl. wavs, run logs, checkpoints, the
halted GLAP full-corpus build) is **outside the registry's scan scope (0 rows reference it)**. The gate
`P0_INTEGRITY_FREEZE` is self-certified **NOT_PASS**.

Net: a reviewer can reconstruct the **committed cell set and its claim mapping**, but **cannot**
reconstruct **what was tried and dropped** (the QRP/multiplicity-relevant dimension) or the raw
generation artifacts behind the committed numbers.

---

## 1. Registry inventory (what exists)

| # | Registry / ledger | Path | Kind | Coverage / caveat |
|---|---|---|---|---|
| R1 | Experiment attempt registry | `docs/integrity/experiment_attempt_registry.jsonl` | 574 JSONL rows, one per on-disk artifact | Filename+mtime scan of **W1 `_repro/` only**, enriched `status`/`claim_id`/`inferred`/`content_hint`. `purpose_note` repeatedly says "not machine-parsed further". Does NOT capture config-selection trajectory. |
| R2 | Prior-exposure registry | `docs/integrity/prior_exposure_registry.json` | keyed JSON | `datasets_touched`, `effect_sizes_observed`, `prompt_templates_enumerated`, `metric_families_enumerated`, `dev_exposure_events`, `manual_completion_todo`, `p0_gate_status`. `n_repro_artifacts_scanned=574`. |
| R3 | Claim ledger | `docs/claim_ledger.yaml` | 16 claim entries | Authoritative narrative→claim resolution; per-claim `status` ∈ {valid, directional, "null", invalid, unverified} + `invalid_reason`/`superseded_by`. Cites some artifacts OUTSIDE the R1 scan scope (W4 repo — see §3). |
| R4 | Discrepancy register | `docs/integrity/discrepancy_register.md` | append-only prose | Records manifest-staleness + P0-NOT_PASS status; itself states R1 is "a shallow filename+mtime scan that does NOT capture the config-selection trajectory". |
| R5 | Release manifest | `docs/integrity/release_manifest.json` | JSON | Per-repo SHA+dirty+live pytest/checker; a publish-transaction record, not an attempt ledger. |
| R6 | Remediation evidence | `docs/integrity/remediation_evidence.yaml` | JSON/YAML | finding→fix→checker-rule map (v4.2 review). |
| R7 | Append-only erratum | `docs/integrity/append_only_erratum_for_v42.md` | prose | v4.2 proposal errata. |
| R8 | Record policy + attestations | `docs/integrity/record-policy-and-attestations.md` | prose | hot/cold policy + post-commit `(path,commit,blob-hash)` triples. |
| G  | Generator | `scripts/checks/build_registers.py` | script | Builds R1+R2 (present on disk). |

**Referenced-but-ABSENT registry (unevidenced pointer):** `prior_exposure_registry.json`
`manual_completion_todo[3]` points at
`scripts/baselines/_repro/draws/exposure_registry.json` (deterministic_draw.py's F-8(b) draw
registry) and states **"no `draws/` directory exists yet on disk."** So one registry is named in the
integrity apparatus but has no backing artifacts (expected: no real eligibility/exploration/
confirmatory draws have been taken yet).

**MLflow store:** CLAUDE.md says the local MLflow file store (`mlruns`) lives on **WSL ext4**
`~/speechrl-data/mlruns` — **not Windows-visible**; not found under E:. Whether it holds run records is
**UNKNOWN** from this vantage. Flag for coordinator (needs a WSL-side `ls`).

---

## 2. Raw-run artifact inventory (what actually exists on disk)

### 2a. REGISTERED group — W1 `_repro/` (git-tracked, D:)
`projects/speech-mllm-training-free-rl/_repro/` — this IS the R1 scan target. Row-status distribution
(R1, 574 rows):

| status | rows |
|---|---|
| baseline-cell | 265 |
| superseded-variant | 126 |
| holdout-manifest (test_ids present; not opened by scan) | 66 |
| locked-dev-cell | 65 |
| probe-or-analysis-artifact | 36 |
| broken-variant | 8 |
| notes/doc | 6 |
| validity-annotation | 2 |

claim_id tagging (R1): C-BASELINES 464, C-ASR-V2 8, C-T7 2, C-M3 2, C-THEORY 1, C-ASR-ORACLE 1;
`inferred=false` 495 / `inferred=true` 79. On-disk this maps to `_repro/baselines/` (464 files),
`_repro/LOCKED_HOLDOUT/` (66 manifests + logs), ~40 top-level analysis JSONs, README. **Registry ≈ this
tree, 1:1.** This group is reconstructable.

### 2b. UNREGISTERED group — E:-drive raw working tree
`E:/…/speechrl-data/_repro/` — **~79 top-level entries (27 subdirs + 52 files); 0 referenced by R1**
(`grep -c` for speechrl-data / /mnt/e / full_corpus / phase_a_agent / *_wavs in R1 = **0**). Contents
(names + rough character; sizes not read for binaries):

- **Raw generation inputs (wav pools), 15 dirs:** `asr_bon_v2_other_{clean,snr5,snr5_ns20260713}_wavs`,
  `librispeech_other_{clean,snr5,}_wavs`, `cp1_{minds14,mmau,mmau_mmaudit}_wavs`, `m3_phase0_wavs`,
  `minds14_{en-US,enus,v2}_wavs`, `loader_wavs`, `p2_wavs`.
- **Run logs (raw):** `asr_bon_v2_full_run{,2}.log`, `asr_bon_v2_noise2_run.log`, `asr_run.log`,
  `vllm_probe.log`, `wave1.log`, `wave2.log`, `locked_rerun_dev.log`.
- **Log subdirs:** `wave1_logs/` (8), `wave2_logs/` (4), `wave3_logs/` (4), `redraw_logs/` (2),
  `locked_rerun_logs/` (2).
- **Build/checkpoint dirs:** `full_corpus_checkpoints/` (only `full_corpus__fiqa__glap.npz`, ~127 MB —
  the HALTED GLAP full-corpus build), `full_corpus_logs/` (empty), `phase_a_agent/`
  (`cpu_builds.log`, `fix_builds.log`, `*_report.json`, done-markers), `step0_evidence/`
  (`embed_server.log`, `vllm_attempt.log`, `resp_mm.json`, `resp_txt.json`),
  `minds14_v2_query_cache/`, `m5_confirmatory_wavs_snr5/`, `probe_hpf_wavs_snr5/`.
- **Standalone artifacts:** `Realization.lean`, `librispeech_train960_tokfreq.json`,
  `report_{naive,policy,rawschema}.json`, `minds14_*_manifest.jsonl`, pip-freeze snapshots.

### 2c. UNREGISTERED group — E:-drive top-level logs
`E:/…/speechrl-data/`: `_llama_server*.log` (incl. `_llama_server_meralion.log` ~345 MB),
`_llama_server_qwen3_embed.log`, `wave0_*.log` (5), `_aishell-hf.log`, `_openslr-driver.log`,
`_download-all.log`, `_hf-complete.log`, plus `_explore_*.py`/`_probe_*.py` one-off scripts. These are
serving/fetch logs (arguably data-plumbing, not experiments) — but they are run artifacts and **none is
indexed anywhere**.

### 2d. UNREGISTERED group — E:-drive fetch logs
`E:/…/speechrl-data/logs/` — 6 airbench fetch logs + `airbench_tail_complete.sh`. Data-fetch, unindexed.

### 2e. OUT-OF-SCOPE but claim-cited — W4 repo outputs (D:)
`projects/speech-mllm-omni-embedding-rl/outputs/{2026-06-22,2026-06-24}/…` exist and are **cited by
`claim_ledger.yaml` C-W4-DISENTANGLE** (`.../eval_harness.py`, `.../main.log`) yet are **NOT scanned by
R1** (R1 only walks W1's `_repro/`). So the ledger reaches artifacts the attempt census does not cover.

---

## 3. Set difference (both directions)

### 3a. Raw artifacts WITH NO registry entry (unregistered attempts)
1. **Entire E:-drive raw-run tree** (§2b–2d): wav pools, wave/asr/locked run logs, `phase_a_agent`
   builds, `step0_evidence`, `full_corpus_checkpoints` (halted GLAP build), llama-server logs. **0 of
   these appear in R1/R2.** By design R1 scans only the committed D: subtree; the raw evidence behind
   the committed numbers is not indexed.
2. **Config-selection trajectory** — abandoned prompt/weight/threshold/K/embedder sweeps and their
   abandonment reasons. **Not on disk anywhere in a machine-parsable form**; R2 flags it as the
   "load-bearing OUTSTANDING item for P0", reconstructable only from session logs / human recall.
3. **W4 repo outputs** (§2e) — cited by the claim ledger, outside R1's walk.
4. **Any process that touched a dataset/split OUTSIDE `_repro/`** (ad-hoc notebooks, since-deleted
   scripts, a sibling session's uncommitted local files). R2 `manual_completion_todo[2]` explicitly
   lists this as unconfirmed. **UNKNOWN.**

### 3b. Registry entries WITH NO artifact (unevidenced claims)
1. **`scripts/baselines/_repro/draws/exposure_registry.json`** — named in R2's todo but the `draws/`
   directory **does not exist** (no draws taken yet). A referenced registry with no backing artifacts.
2. R1 itself is a scan OF the disk, so it has **no dangling row→missing-file entries** by construction
   (every row is a file that was present at scan time, commit `56364eb`/W1 `ab1c680`). Coordinator note:
   R1 was generated at an EARLIER snapshot than current HEADs (umbrella now `93e0bcf`), so a re-scan
   could surface newly-added or removed files not in the frozen 574. **Not re-run here.**
3. The claim ledger's W4 citations (§2e) are evidenced (files exist) but sit outside the census
   boundary — a scope gap, not a missing artifact.

---

## 4. Verdict — what a reviewer can / cannot reconstruct

**CAN reconstruct** (evidence present + indexed):
- The committed baseline/selector/holdout **cell set** (574 artifacts, each with `status` + `claim_id`).
- The **claim→status resolution** for the 16 headline claims (`claim_ledger.yaml`): 6 invalid, 2 null,
  1 unverified, 7 directional.
- The **named prompt-template families** and **metric-family taxonomy** (R2), the **C-ASR-V2 selector
  effect sizes** (~24%/~42% realized fraction at N=8), and the **dev-exposure event** list.

**CANNOT reconstruct** (the load-bearing gaps):
- The **config-selection trajectory** — the full explored search space and every abandonment reason
  (R2 `manual_completion_todo[0]`; this is the M-6 gap and the reason `p0_gate_status.pass=false`).
- The **raw generation artifacts** on E: (wavs, per-run logs, `full_corpus` checkpoints, serving
  logs) — present on disk but **not indexed by any register**, so not discoverable from the repo alone.
- Whether **any out-of-`_repro/` process** touched eval data (UNKNOWN).
- **MLflow** run contents (WSL-only; not Windows-visible; UNKNOWN).

**Bottom line for C1:** the registry apparatus is real and non-trivial for the *committed* surface, but
the attempt census is **incomplete-by-design on the dimension it is meant to close** (tried-and-dropped
configs) and **blind to the entire raw-run tree on E:**. The project already self-reports this as
`P0_INTEGRITY_FREEZE = NOT_PASS`; this census concurs and adds the E:-drive scope gap as a second,
separately-recorded blind spot.

---

## 5. Counts (for the coordinator)

- Registries found: **3 primary** (R1 attempt, R2 prior-exposure, R3 claim-ledger) + **5 supporting**
  integrity registers (R4–R8); **1 referenced-but-absent** (`draws/exposure_registry.json`).
- Raw artifact groups: **1 registered** (W1 `_repro/`, 574 rows) vs **≥4 unregistered groups**
  (E: `_repro/` ~79 entries; E: top-level serving logs; E: `logs/` fetch logs; W4 outputs cited but
  unscanned) + **1 UNKNOWN** (WSL MLflow).
- Unregistered attempts (set-diff 3a): **4 classes** (E: raw tree; config-selection trajectory;
  W4 outputs; out-of-`_repro` unknowns).
- Unevidenced registry pointers (set-diff 3b): **1** (`draws/exposure_registry.json` absent);
  R1 rows all backed (at frozen snapshot).

---

## 6. Provenance of this draft
- Evidence snapshot: umbrella HEAD `93e0bcf` (working tree read 2026-07-14); W1 HEAD `a532da0`.
  NOTE: R1/R2 were generated at an older snapshot (umbrella `56364eb`, W1 `ab1c680`) — a re-scan at
  current HEAD was NOT performed by this census.
- Data root: `E:/…/speechrl-data/` (Windows-visible), directory listings only.
- Method limits: single-pass; no runs; binaries not opened; WSL ext4 (`~/speechrl-data/mlruns`,
  `~/.venvs`) not inspected.

---

## Coordinator spot-check addendum（2026-07-14，主会话亲验）

- **MLflow UNKNOWN 已解决**：WSL `~/speechrl-data/mlruns` 存在，2.3 MB，2 个 experiment
  （500168843308197976 / 741139080879565390）——小体量，登记为已发现。
- **registry 对 E 盘零引用**：亲验 grep = 0 命中，坐实本普查 headline。
- **E 盘运行树 + W4 outputs 已补登**：`docs/integrity/2026-07-14-edrive-run-inventory.jsonl`
  （376 行聚合登记：`_repro`/`logs` 深度≤2，大目录记 n_files/total_bytes 摘要行，含 W4 Hydra 运行目录与
  data-root 服务日志；目的=可发现性登记，非全文件清单）。
- **闭环形态：C1 = CENSUS_COMPLETE_WITH_REGISTERED_PERMANENT_GAP**——config-selection 轨迹
  （被弃用的 prompt/K/阈值/embedder 尝试及其原因）历史不可重建，按禁补造纪律登记为**永久缺口**
  （类比 RAW_EVENT_UNAVAILABLE）；自 Stage-1B 起由探针协议的尝试登记机制**前瞻性关闭**。
- 本普查 = 单遍 AI + 协调者抽查（mlruns/零引用/文件在场三项）；**owner 于 1B-0 探针协议签批时终验**。
