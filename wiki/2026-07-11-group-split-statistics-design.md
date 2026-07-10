# Group-split + cluster-bootstrap statistical foundation for W1 baselines (design)

- **Date:** 2026-07-11
- **Stage:** 1 (problem-definition; directional-only evidence discipline applies)
- **Status:** **DESIGN — NOT IMPLEMENTED.** No code changed by this document. This is the
  build spec for ticket #26; implementation is a separate Sonnet task after owner sign-off.
- **Scope:** W1 repo `projects/speech-mllm-training-free-rl`, the Stage-1 baseline grid
  (`scripts/baselines/`, `scripts/loaders/`, `_repro/baselines/`).
- **Owner action required before implementation:** (a) approve the new locked-test seed +
  access-control convention; (b) approve the rerun scope (cell count below); (c) confirm that
  the previously-exposed id lists are accepted as permanently non-locked.

---

## 0. Why this exists — the four verified audit findings

Two external audits (verified against the code in this session) established:

1. **Item-id-disjoint dev/test is insufficient.** The split unit must be the *group*
   (speaker / session / dialogue / source-question-family / clip / template), matched to each
   task family. Item-level disjointness lets two utterances of the same speaker — or two QA
   pairs over the same audio clip, or the same source question rendered in two accents — land
   on opposite sides of the split, so "test" is not independent of "dev".

2. **The existing redraw tooling reuses deterministic seeds.** `scripts/baselines/redraw.py`
   + `scripts/loaders/_common.py:draw_disjoint` draw `test` with `seed_test = TEST_SEED`
   (`20261705`) and `dev` with `seed_dev = DEV_SEED` (`20260705`) — the *same* seeds the grid
   already ran under. The redraw makes dev/test mutually disjoint, but the resulting test id
   sets are computed from the already-seen `TEST_SEED` permutation of the same pools, so the
   40/64 "new" test cells are **not a fresh, never-observed holdout** (Dwork et al.
   reusable-holdout problem: a holdout is only valid until it informs a decision; these ids
   have already driven arm/threshold/prompt choices). `_repro/redraw_manifest.json` and every
   existing test cell in `_repro/baselines/` are therefore **permanently non-locked**.

3. **Per-item bootstrap must become cluster bootstrap.** The current
   `run_baseline.paired_bootstrap` resamples individual items i.i.d. (line 517-530). Under
   intra-group correlation (same speaker, same clip, same passage), i.i.d. item resampling
   underestimates the variance → CIs too narrow, false "significant" gaps. The resampling unit
   must be the group.

4. **"65 格" conflated dataset keys with result cells.** The redraw census found **65
   overlapping dataset keys** (52 wave-1 + 13 wave-2). Those 65 keys map to **234 clean result
   cells** (`key × split × backbone`), not 65 — see §4. (The ticket's "~241" is this quantity;
   the exact count from the on-disk cells is 234.)

---

## 1. Group-metadata inventory (Task 1)

### 1.1 Per-task-family grouping rule (from the audit)

| K-type(s) | Task family | Group unit (in priority order) |
|---|---|---|
| K1, K2 | content / ASR (en, zh) | **speaker** → book/chapter → recording family (noise-augmented copies of one recording share a group) |
| K3 | multilingual LID(+gender) | **speaker** / recording (the *language* is the label, so it can never be the group) |
| K4 | SER | **speaker** or **session/dialogue** |
| K5 | speaker-attribute probe | **speaker** (the attribute is the label; must split by speaker id) |
| K6, K7 | SLU intent / slot | **template / intent-surface (scenario)** or **speaker** |
| K8 | spoken verifiable QA / MCQ | **same source-text question's variants** (TTS / human / rephrased / multi-accent) → **source passage / clip** (many QA per one clip/passage) → template/topic |
| K9 | native spoken-query retrieval | **query** (clean + SNR-augmented renderings of one query share a group) |
| K10 | spoken tool-calling | **scenario seed / query template** (one query rendered by many speakers) or tool |
| K11 | rule-verifiable / refusal | instruction-type (only relevant once scored; both current K11 cells are unscored or stubbed) |

### 1.2 Availability classes

Every result cell stores `per_item = [{item_id, instr, reply, score, detail}]` **only** — no
`meta`, so **group labels are NOT persisted in the result JSONs today** (verified). Group
recovery therefore falls into four classes:

- **G-FIELD** — group unit already lives in the loader's `meta` or `gold` dict (usable at
  rerun with zero loader change; for a *rescore* of an existing cell it requires re-invoking
  the loader to recover the field, since per_item dropped it).
- **G-ID** — group derivable by parsing the existing `item_id` string alone (no loader change;
  a pure string helper works even on the archived result JSONs).
- **G-SOURCE** — the grouping field exists in the raw corpus but the loader does **not** expose
  it in `meta`/`gold`/`item_id` → needs a loader meta-field addition (code change).
- **G-NONE** — no grouping unit exists at any grain finer than the whole dataset → honest
  fallback to item-level, flagged in output.

### 1.3 Inventory table (all grid dataset keys)

Meta field names cited are from the loaders read this session. "id-parse" gives the substring
of the observed `item_id` that carries the group.

#### K1 / K2 — content ASR

| dataset key | group unit | class | evidence (field / id-parse) |
|---|---|---|---|
| `librispeech` | speaker (or chapter) | **G-FIELD** | `meta["speaker_id"]`, `meta["chapter_id"]`; id `6829-68771-0001` = spk-chap-utt |
| `aishell-1` | speaker | **G-ID** (→G-SOURCE to make explicit) | id `BAC009S0769W0185`; speaker = `S0769` substring. Loader exposes no speaker field today |
| `thchs-30` | speaker (reader) | **G-ID** | id `D7_841`; reader = `D7` prefix (also sentence `841` shared across readers = 2nd candidate group) |
| `seed-tts-eval-en/-zh` | speaker | **G-NONE** | id = bare `filename` (e.g. `10002287-00000094`); no verified speaker column. Filename-prefix grouping is a **guess** — do not claim speaker-disjoint |
| `voicebench-sd-qa` (K1 stratifier) | **source question** (same Q, 11 accents) | **G-ID** | id `sd-qa/{dialect}#{j}`; the `#j` index is the same question across dialects — the exact "same source question rendered differently" case. `meta["dialect"]` also present |
| `uro-bench-Repeat`, `uro-bench-Repeat-zh` | — (echo) | **G-NONE** | id = int; distinct echo utterances, no family field |

#### K3 — LID

| dataset key | group unit | class | evidence |
|---|---|---|---|
| `fleurs-r` | speaker/recording | **G-NONE** | 7-col FLEURS tsv has `id, filename, raw, transcription, phonemic, num_samples, gender` — **no speaker id**. `gold["gender"]`/`lang` present but language is the label. Honest caveat: cannot build a speaker-disjoint split from this mirror |

#### K4 — SER

| dataset key | group unit | class | evidence |
|---|---|---|---|
| `crema-d` | speaker (~91) | **G-FIELD** | `gold["spk"]` (also `gold["sent"]`, 12 shared sentences); id `crema-d/1002_MTI_NEU_XX` |
| `meld` | dialogue | **G-FIELD** | `meta["dialogue_id"]` (+`speaker`, `utterance_id`); id `meld/test/dia5_utt8` |
| `esd` | speaker (10 zh) | **G-FIELD** | `gold["spk"]`. **Leakage caveat:** current self-split holds out the last 20 % of each *(speaker, emotion)* block → same speaker on both sides. Group-disjoint needs whole-speaker holdout; only 10 speakers (coarse — see §2.4) |
| `csemotions` | speaker (10) | **G-FIELD** (id-positional) | `gold["speaker"]` (`female001`…). id `csemotions/shard0_row74` is positional — speaker NOT in id, so a rescore of an existing cell must re-load. 10 speakers (coarse) |
| `uro-bench-UnderEmotion-en/-zh` | — | **G-NONE** | id = int; `meta` has `language`, `target_text` only. TTS emotional utterances, no speaker field |
| `vocalbench-emotion` | — | **G-NONE** | id = `Qid`; `meta` has `question`, `score`. No speaker |

#### K5 — speaker-attribute (and the excluded SID pair)

| dataset key | group unit | class | evidence |
|---|---|---|---|
| `speech-massive-de-DE-attr`, `-fr-FR-attr` | **speaker** | **G-SOURCE** | source parquet carries `speaker_id` (loader docstring) but `_COLUMNS` reads only `speaker_sex`/`speaker_age` (the labels) + `scenario_str`/`utt`. **Must add `speaker_id`** or a speaker-disjoint split is impossible |
| `cn-celeb1` *(K5-excluded SID)* | speaker / session | G-FIELD | `gold["speaker_id"]`, `meta["session"]` — not on the scored grid, listed for completeness |
| `voxceleb1-test-split` *(K5-excluded SID)* | speaker / video-session | G-FIELD/G-ID | `gold` = speaker_id; id `id10270+5r0dWxy17C8+00001` encodes speaker + video |

#### K6 / K7 — SLU intent / slot

| dataset key | group unit | class | evidence |
|---|---|---|---|
| `slurp`, `slurp-slot` | intent-surface (scenario) / speaker | **G-FIELD** (scenario) / **G-SOURCE** (speaker) | `gold["scenario"]` (18 scenarios) present; SLURP `usrid` speaker is in the jsonl but not loaded. `meta["recording_file"]` = `audio-<session>…` carries session. id = int `slurp_id` |
| `speech-massive-de-DE`, `-fr-FR` (K6) | intent/scenario / speaker | **G-FIELD** (scenario) / **G-SOURCE** (speaker) | `meta["scenario_str"]`, `gold["intent_str"]`; speaker_id must be added (see K5) |
| `speech-massive-de-DE-slot`, `-fr-FR-slot` (K7) | same as above | G-FIELD / G-SOURCE | same loader/fields |
| `minds14-zh` *(LEGACY, K6)* | intent / speaker | **G-SOURCE** | p2_baselines loader, positional id, no group field exposed |

#### K8 — spoken QA / MCQ (the bulk)

| dataset key | group unit | class | evidence |
|---|---|---|---|
| `voicebench-bbh` | BBH subtask (~27 templates) | **G-ID** | id `bbh_web_of_lies_218`; subtask = prefix before final `_<n>` |
| `voicebench-mmsu-spoken` | MMLU source doc / domain | **G-FIELD** | `meta["src"]` (upstream MMLU source), `meta["domain"]`; id `mmsu-spoken/health/6062` |
| `mmsu` | task_name (47) / category | **G-FIELD** | `meta["task_name"]`, `meta["category"]`; id `accent_identification_<uuid>` (task_name = prefix) — topical family, not per-clip |
| `heysquad` | SQuAD passage | **G-FIELD → G-SOURCE** | `meta["context"]` = the passage (many spoken Qs per passage). Hash `context` → group, or add explicit `passage_id`. **Note the T7 leakage warning on `context`** — group derivation reads it but must not inject it |
| `air-bench-foundation-sound-aqa-avqa`, `-sound-aqa-clothoaqa`, `-music-aqa` | **audio clip** (many QA per clip) | **G-SOURCE** | 1000 QA over 351 clips (clothoaqa); 814 over 797 (music_avqa). Clip = `Path(row["path"]).stem`, resolvable but **not** a meta field. id `Sound_AQA:clothoaqa:14934` = per-QA uniq_id, clip absent → must add `meta["clip_id"]` |
| `air-bench-foundation-*` classification (`acoustic-scene-cochlscene`, `-tut2017`, `music-genre-fma`, `-mtj-jamendo`, `music-instruments-nsynth`, `-mtj-jamendo`, `music-midi-pitch-nsynth`, `-velocity-nsynth`, `music-mood-mtj-jamendo`, `audio-grounding`) | clip = item (1:1) | **G-NONE (item = clip)** | one clip → one label; item-level bootstrap is already clip-correct, no sub-item leakage |
| `air-bench-foundation-speech-grounding` | — | env-blocked | never produced a real cell (`NeedsAirBenchFoundationAudio`) |
| `voicebench-openbookqa` | OpenBookQA core fact | **G-NONE (→G-SOURCE)** | positional id; the science "fact"/book id is not exposed |
| `mmar` | topical category | **G-NONE** (coarse category only) | `meta["category"]`, `sub_category`, `language`; each is a distinct audio+Q, no fine family |
| `audiocaps-qa` | — | **G-NONE** | heterogeneous env sound, "no stratification field" (loader docstring); id positional |
| `uro-bench-{SQuAD-zh, OpenbookQA-zh, Gsm8kEval, GaokaoEval, HSK5-zh, APE-zh, MLC, MLC-zh, MLCpro-en, MLCpro-zh, TruthfulEval}` | — | **G-NONE** | id = int; distinct TTS-rendered questions, no family field |
| `uro-bench-MuChoEval-en` | source audio (maybe) | **G-NONE (→G-SOURCE)** | `meta["from_audio"]` may indicate multiple Qs per source clip — add + verify before claiming a group |
| `voiceassistant-listening-{general,music,sound,speech}`, `voiceassistant-speaking-reasoning` | category / sound-clip | **G-FIELD** (category) | `meta["category1"]`, `category2`; listening/* also have `meta["sound_audio_wav"]` (the asked-about clip) → finer clip group is G-SOURCE |
| `vocalbench-knowledge` | topic / source | **G-FIELD** | `meta["topic"]`, `meta["source"]` |
| `vocalbench-reasoning` | category / source | **G-FIELD** | `meta["category"]`, `meta["source"]` |
| `vocalbench-multi-round` | category | **G-FIELD** | `meta["category"]` |
| `SQuAD-zh`, `spoken-squad` *(LEGACY)* | SQuAD passage (title) | **G-SOURCE** | positional id (`SQuAD-zh#0`); p2 loader exposes no `title`/`context` id — many Qs per passage, must add |
| `mmau-mini`, `vocalbench-zh`, `big-bench-audio`, `OpenbookQA-zh` *(LEGACY)* | clip / fact / — | **G-SOURCE / G-NONE** | p2_baselines positional ids; source family ids not exposed (mmau audio_id, OpenBookQA fact, BBA scenario) |

#### K9 / K10 / K11

| dataset key | group unit | class | evidence |
|---|---|---|---|
| `squtr` (K9) | **query** (clean+SNR share) | **G-ID** | id `{subset}|{noise_level}|{qid}`; qid shared across noise levels = "noise-augmented versions same group". Score is `None` at Step-1 (diagnostic) → bootstrap moot until real R@k |
| `audio2tool` (K10) | **query template / scenario seed** | **G-SOURCE** (query_idx) / **G-FIELD** (tool_name) | source has `query_idx`, `speaker_id`, `speaker_idx` (one query, many speakers); loader exposes `meta["tool_name"]`, `meta["domain"]` only. id `tier1_direct|77` = per-item id. Add `query_idx` for the true scenario group |
| `voicebench-advbench` (K11) | — | **G-NONE** | refusal probe; id positional; no family (item-level) |
| `voicebench-ifeval` (K11) | instruction-type | G-FIELD (moot) | `meta["instruction_id_list"]`; score is `None` (no checker ported) → no bootstrap yet |

### 1.4 Datasets that CANNOT produce a group-disjoint split → fallback

| situation | datasets | fallback |
|---|---|---|
| **No group field at any grain** | `seed-tts-eval-{en,zh}`, `fleurs-r`, `uro-bench` echo/QA subsets, `voicebench-openbookqa`, `audiocaps-qa`, `mmar`, `voicebench-advbench`, most legacy QA | **item-level disjoint split + item-level bootstrap**, cell **flagged** `split_unit="item"`, `bootstrap_unit="item"` in output. Honest caveat printed: "no group metadata; intra-group correlation not controlled." |
| **Clip = item already (1:1)** | air-bench classification subsets (scene/genre/instrument/midi/mood/grounding) | item-level bootstrap **is** clip-level; no caveat needed beyond noting group≡item |
| **Few groups (< ~8 clusters)** | `esd` (10 spk), `csemotions` (10 spk), single-locale SLU by speaker | group-disjoint **is** possible but coarse: a 60/40 split over 10 speakers = ~6 test / ~4 dev speakers. Options: (a) accept coarse group-disjoint with a **wide-CI caveat** (cluster bootstrap with 10 clusters is honest but low-power); (b) fall back to item-level, flagged. Design default: **(a)**, because item-level would overstate significance. `draw_disjoint_grouped` reports `n_groups` so the caveat is data-driven. |
| **Single-speaker corpus** | none confirmed on the grid; `seed-tts-eval` is the closest (speaker unknown, treated as no-group) | if a genuinely single-speaker ASR corpus is ever added, a speaker split is undefined → fall back to book/recording group, else item-level flagged |

---

## 2. Redraw v2 design (Task 2)

### 2.1 New locked seeds (distinct from every burned seed)

Burned seeds found in the repo this session (must **not** be reused for the locked holdout):
`20260705` (`SLICE_SEED`=`DEV_SEED`=`POOL_RECONSTRUCTION_SEED`), `20261705`
(`TEST_SEED`=`SLICE_SEED+1000`), `20260711` (`COHORT_SEED`), `20260712` (`NOISE_SEED`).

Propose three **new, never-used** constants (deliberately non-date so they can't collide with a
future dated seed), in a new `scripts/baselines/locked_split.py`:

```python
# scripts/baselines/locked_split.py  (NEW — design only)
LOCKED_TEST_SEED   = 611_741_209   # group-shuffle seed for the TEST draw — NEVER used before
LOCKED_DEV_SEED    = 611_741_213   # group-shuffle seed for the DEV draw (from the test remainder)
LOCKED_SPLIT_TAG   = "grouplock-v2-20260711"   # stamped into every manifest + result cell
```

Rationale for a fresh test seed (finding #2): the locked holdout is only a real holdout if its
membership has **never informed a decision**. `20261705` has already selected arms/prompts, so
any redraw from it is contaminated regardless of disjointness. A brand-new seed + a brand-new
draw procedure (group-aware, below) severs that link.

### 2.2 Group-aware disjoint draw (`draw_disjoint_grouped`)

New function beside `draw_disjoint` in `_common.py` (old one kept for backward replay of the
non-locked cells). Signature and contract:

```python
def draw_disjoint_grouped(
    group_of: dict[str, str],     # item_id -> group_id  (item_id its own group if G-NONE)
    n_test: int = 60, n_dev: int = 40,
    seed_test: int = LOCKED_TEST_SEED, seed_dev: int = LOCKED_DEV_SEED,
) -> dict:
    """Group-disjoint (test, dev) draw. ALL items of a group land on the SAME side.
    Test drawn FIRST from the full group set; dev drawn from the remaining groups."""
```

Algorithm (numpy-only, deterministic):
1. Invert `group_of` → `groups: {group_id: [item_ids]}`; sort group ids (stable order).
2. `rng_test = default_rng(seed_test)`; permute the group-id list; **greedily add whole
   groups** to `test` until the *item* count first reaches `n_test` (accept the overshoot from
   the last group rather than splitting it — never split a group).
3. Remove the chosen test groups; `rng_dev = default_rng(seed_dev)` permutes the remaining
   groups; greedily fill `dev` to `n_dev` items the same way.
4. Return `{test_ids, dev_ids, test_groups, dev_groups, n_groups_total, n_test, n_dev,
   group_disjoint_verified: test_groups ∩ dev_groups == ∅, shortfall}`.
5. **Small-pool / few-group handling:** if whole groups can't hit `n_test+n_dev`, allocate
   groups proportionally (mirrors `draw_disjoint`'s 60/40 rule) and record `shortfall`; if a
   single group already exceeds `n_test`, flag `oversized_group` (the cell is then effectively
   one-cluster → item-level bootstrap, caveat).

The per-dataset `group_of` map comes from a new **`group_key_of(dataset_key, row)`** dispatch
(§2.5) — the single place the §1.3 rules become code. For G-NONE datasets, `group_of[item_id]
= item_id` (every item its own singleton group), so the *same* function yields item-level
splits for them with no special-casing.

### 2.3 Test-first, access-controlled locked manifest

Write the frozen test membership to a **separate, access-controlled location** distinct from
the working tree the runner/eval reads:

```
_repro/LOCKED_HOLDOUT/                       (NEW dir; git-tracked but access-gated by convention)
  <dataset_key>__test.locked.json            one file per key: {split_tag, seed, group_ids, item_ids, sha256}
  ACCESS_LOG.md                              append-only: who/when/why each locked file was opened
  README.md                                  the rules below
```

**Access-control convention (process, not filesystem ACL — this box has no per-file ACL):**
- The locked test manifest may be read by **exactly one** consumer: the final scoring pass that
  produces the confirmatory number. **No** arm selection, prompt search, threshold tuning,
  N\*-budget choice, or reward-model calibration may read any file under `LOCKED_HOLDOUT/`.
- Enforcement hooks (design): (a) `run_baseline.py` refuses `--slice locked` unless invoked
  with `--confirmatory` (a flag that also stamps the result cell `locked_holdout_touched:true`
  and appends to `ACCESS_LOG.md`); (b) a pre-commit / CI check greps that no tuning script
  imports `locked_split.load_locked_test`; (c) dev-side tuning uses **only** the dev manifest
  (`_repro/baselines_dev_locked/…`), never the locked dir.
- **Dev manifest is separate and freely readable** (tuning happens on dev). Only *test* is
  locked.

**Permanently non-locked (finding #2), stated explicitly in `README.md` and every downstream
report:** the current `_repro/redraw_manifest.json`, every `baselines-<key>-disjoint-{dev,test}`
kb_snapshot, and all 264 existing `_repro/baselines/*.json` cells are **exposed** and can never
be re-designated as the locked holdout. The locked holdout is *only* the freshly group-drawn
`LOCKED_TEST_SEED` sets in `LOCKED_HOLDOUT/`.

### 2.4 Draw order and reproducibility

Per dataset key: reconstruct the full pool ids exactly as `redraw.py` does today
(`run_baseline._load_rows(..., n=None, seed=POOL_RECONSTRUCTION_SEED)` under the audio-stub
context — reuse verbatim), build `group_of` via `group_key_of`, then `draw_disjoint_grouped`.
Freeze the **test** file under `LOCKED_HOLDOUT/` and the **dev** file under
`_repro/baselines_dev_locked/` as new kb_snapshots
(`baselines-<key>-grouplock-{dev,test}`) — never overwriting the old `-disjoint-*` names.

### 2.5 `group_key_of(dataset_key, row)` — the dispatch (pure-runner, no loader change for most)

One function in a new `scripts/baselines/grouping.py`, implementing §1.3. Sketch of the
non-trivial branches (rest default to `row["meta"]["item_id"]` = singleton):

```python
def group_key_of(dataset_key, row):
    meta, gold, iid = row["meta"], row.get("gold"), row["meta"]["item_id"]
    # G-ID (parse existing item_id — works on archived cells too)
    if dataset_key == "aishell-1":            return iid[6:11]                  # 'S0769'
    if dataset_key == "thchs-30":             return iid.split("_")[0]          # 'D7'
    if dataset_key == "librispeech":          return iid.split("-")[0]          # speaker
    if dataset_key == "voicebench-bbh":       return iid.rsplit("_", 1)[0]      # 'bbh_web_of_lies'
    if dataset_key == "voicebench-sd-qa":     return iid.split("#")[-1]         # question index
    if dataset_key == "squtr":                return iid.split("|")[-1]         # qid across noise
    # G-FIELD
    if dataset_key == "crema-d":              return gold["spk"]
    if dataset_key == "esd":                  return gold["spk"]
    if dataset_key == "csemotions":           return gold["speaker"]
    if dataset_key == "meld":                 return str(meta["dialogue_id"])
    if dataset_key == "voicebench-mmsu-spoken": return meta.get("src") or meta["domain"]
    if dataset_key == "mmsu":                 return meta["task_name"]
    if dataset_key.startswith("vocalbench-") and dataset_key != "vocalbench-emotion":
        return meta.get("source") or meta.get("topic") or meta.get("category") or iid
    if dataset_key.startswith("voiceassistant-"): return f'{meta["category1"]}/{meta["category2"]}'
    if dataset_key in ("slurp","slurp-slot"): return gold["scenario"]
    if dataset_key.startswith("speech-massive"): return meta.get("scenario_str", iid)
    if dataset_key == "heysquad":             return _stable_hash(meta["context"])   # passage
    # G-SOURCE (requires the loader meta additions in §3 before these resolve)
    if dataset_key.startswith("air-bench-foundation-") and dataset_key.endswith(("-aqa","-avqa","-clothoaqa","-music-aqa")):
        return meta.get("clip_id", iid)       # clip_id added by loader change
    if dataset_key == "audio2tool":           return meta.get("query_idx", iid)
    return iid                                 # G-NONE → singleton (item-level split+bootstrap)
```

At **rerun** time `run_baseline._run_item` additionally persists
`"group_id": group_key_of(dataset_key, row)` into each per_item entry, so future analyses read
the group directly from the cell (closing finding #3's gap that per_item drops meta).

---

## 3. Cluster bootstrap + multiplicity + hierarchical aggregation (Task 3)

All numpy-only; no scipy/statsmodels (preserves the lazy-import + dependency-light discipline).
Reference implementation to reuse/replace: `run_baseline.paired_bootstrap` (the existing i.i.d.
item bootstrap) and `p6_perception_delta.py:boot` — the design generalizes their resample loop
from items to clusters.

### 3.1 Paired cluster bootstrap (replaces `paired_bootstrap`)

```python
def cluster_bootstrap_ci(scores, groups, nboot=10000, seed=LOCKED_TEST_SEED):
    """95% CI on the mean, resampling GROUPS (not items) with replacement.
    scores: list[float|None]; groups: list[group_id] aligned to scores.
    Falls back to item-level (each item its own group) when groups is None/all-unique,
    and the returned dict flags bootstrap_unit accordingly."""
    # 1. drop None; bucket item indices by group_id -> clusters = list[np.ndarray]
    # 2. for b in range(nboot):
    #        pick len(clusters) clusters WITH replacement;
    #        concat their item scores; record the mean
    # 3. return [q2.5, q97.5], plus n_clusters, bootstrap_unit
```

Key properties:
- **Resample unit = cluster.** Draw `K` clusters with replacement (K = number of clusters),
  pool their member items, take the mean. This propagates intra-cluster correlation into the
  CI width — the whole point of finding #3.
- **Paired** across two arms (baseline vs training-free-RL arm) by using the **same cluster
  resample indices** for both arms in each bootstrap iteration, then recording the *difference*
  of means → a CI on Δ that cancels the shared cluster-draw noise (this is the actual "paired"
  part the old name only gestured at). API: `paired_cluster_delta_ci(scores_a, scores_b,
  groups, ...)`.
- **Fallback flagged:** when `group_key_of` returned singletons (G-NONE), `n_clusters ==
  n_items` and the result carries `"bootstrap_unit": "item"` + a caveat string; otherwise
  `"cluster"`. Output never silently mixes the two.
- **Aggregate block change** (`run_one`, line ~629): `aggregate` gains
  `{"ci95_cluster": ..., "n_clusters": ..., "bootstrap_unit": ...}` alongside the legacy
  `"ci95"` (kept for continuity of the exposed cells).

### 3.2 Within-arm-family multiplicity: Holm / max-T

When an arm family compares many datasets/subsets at once (e.g. the K8 uro-bench family, or
one training-free-RL variant across all cells), control the family-wise error:

- **Holm–Bonferroni** (default, distribution-free): compute a per-comparison bootstrap p-value
  (`p = 2 · min(fraction of paired-Δ bootstrap replicates ≤ 0, ≥ 0)`), sort ascending, reject
  `p_(i)` while `p_(i) ≤ α / (m − i + 1)`. Pure numpy, no dependency.
- **max-T (bootstrap step-down)** for correlated tests (preferred when the same clusters recur
  across comparisons — e.g. multi-accent sd-qa): in each bootstrap iteration resample clusters
  **once**, recompute the studentized Δ statistic for *every* comparison, track the
  **maximum** |t| across the family; the max-T null distribution gives simultaneously-valid
  adjusted p-values that respect the empirical correlation (tighter than Holm when tests are
  positively dependent). Implemented as one extra reduction inside the existing cluster-bootstrap
  loop — negligible cost.
- Output: `adjusted_p`, `reject_at_0.05`, and the method tag per comparison. Design default:
  report **both** Holm and max-T; flag any disagreement.

### 3.3 Hierarchical (random-effects) cross-dataset aggregation

To combine per-dataset Δ effects into a family-level or grid-level headline **without** letting
a large dataset dominate or pretending datasets are one pool:

- **Two-level random-effects (DerSimonian–Laird), numpy-only.** Inputs: per-dataset Δ̂_k and its
  cluster-bootstrap variance v_k (square of half-CI-width / 1.96). Estimate between-dataset
  heterogeneity τ² by DL, then the pooled effect is the inverse-variance weighted mean with
  weights `w_k = 1/(v_k + τ²)`; its CI uses `1/Σw_k`. Report τ² and I² (heterogeneity) so a
  high-variance grid isn't summarized as a single deceptively-tight number.
- **Cluster-of-clusters bootstrap alternative** (when v_k is unreliable for small `n_clusters`):
  a nested bootstrap — outer loop resamples **datasets**, inner loop resamples **clusters**
  within each — giving a fully nonparametric grid-level CI. More faithful for the coarse-group
  SER cells (§1.4). Design default: **DL random-effects** for the headline (cheap, standard),
  **nested bootstrap** as the robustness check.
- These live in a new `scripts/baselines/stats.py`; `summarize_wave1.py` calls them to add a
  "random-effects pooled Δ (95 % CI, τ², I²)" row per K-family instead of / alongside the
  current purely-per-cell table.

### 3.4 What stays the same

`metrics.py` scorers are untouched (they already return per-item `{score, detail}`); the change
is entirely in the *aggregation* layer (`run_one`'s aggregate block + new `stats.py` + the
summarizer). The per-item score semantics, K-type dispatch, and label sets do not change.

---

## 4. Work estimate (Task 4)

### 4.1 Loader meta-field additions (code changes) vs pure-runner changes

**Pure-runner (no loader touched)** — these resolve via G-ID/G-FIELD in `group_key_of`:
`librispeech, aishell-1, thchs-30, voicebench-sd-qa, voicebench-bbh, voicebench-mmsu-spoken,
mmsu, crema-d, meld, esd, csemotions, slurp, slurp-slot, speech-massive-*(scenario grouping),
vocalbench-{knowledge,reasoning,multi-round}, voiceassistant-*, squtr, heysquad(hash context)`.
(~30 keys covered with zero loader edits.)

**Loader meta-field additions required (G-SOURCE)** — one edit each:

| loader file | add to `meta` | unlocks keys |
|---|---|---|
| `speech_massive.py` | `speaker_id` (add to `_COLUMNS` + meta) | de-DE, fr-FR, ×(intent/slot/attr) = 6 grid keys — enables speaker grouping (scenario grouping already works without this) |
| `air_bench_foundation.py` | `clip_id = Path(row["path"]).stem` | 3 AQA keys (sound-aqa-avqa, -clothoaqa, music-aqa) |
| `audio2tool.py` | `query_idx` (+ optional `speaker_id`) | audio2tool (K10) |
| `slurp.py` | `speaker_id` from jsonl `usrid` (only if speaker grouping wanted; scenario works already) | slurp, slurp-slot (optional) |
| `heysquad.py` | explicit `passage_id` (optional; `_stable_hash(context)` works without) | heysquad (optional) |
| `p2_baselines.py` (legacy) | source-family id (SQuAD `title`; mmau `audio_id`; OpenBookQA fact; BBA scenario) | SQuAD-zh, spoken-squad, mmau-mini, OpenbookQA-zh, vocalbench-zh, big-bench-audio — legacy loaders, larger edit |

**G-NONE (no loader change possible, item-level fallback + flag):** `seed-tts-eval-{en,zh},
fleurs-r, uro-bench-* (all subsets), voicebench-openbookqa, voicebench-advbench, audiocaps-qa,
mmar, vocalbench-emotion, minds14-zh`. (~30 keys run item-level, honestly flagged.)

**New runner/stats modules (the bulk of the work, all pure-runner):**
`locked_split.py`, `grouping.py` (`group_key_of`), `_common.draw_disjoint_grouped`,
`stats.py` (cluster bootstrap, paired Δ, Holm, max-T, DL random-effects, nested bootstrap),
`run_baseline` edits (persist `group_id`; `--slice locked/--confirmatory`; new aggregate keys),
`summarize_wave1.py` edits (random-effects rows, bootstrap-unit column),
`_repro/LOCKED_HOLDOUT/` + access-log + CI grep guard.

### 4.2 Honest cell count for the eventual rerun

From the on-disk cells (verified this session):

| quantity | count |
|---|---|
| total **clean** result cells (`key × backbone × split`) | **264** (152 qwen3 + 112 meralion; 76 unique keys) |
| cells whose key is one of the 65 dev/test-overlap keys (the ticket's "~241") | **234** (130 qwen3 + 104 meralion) |
| the "65 格" figure taken literally as cells | wrong — 65 is **keys**, not cells |

Under the group-split redesign the rerun scope is **larger** than the 234, because item-disjoint
≠ group-disjoint and the locked-test seed is fresh — so every *scored* cell that admits a group
or item split must be re-generated:

- **Full both-backbone group-lock rerun:** ≈ **264 cells** (the whole clean grid), minus a
  handful that produce no bootstrappable metric today (`squtr` K9 diagnostic = None,
  `voicebench-ifeval` stubbed = None → split still frozen but no CI). Net **~260 scored cells**.
- **qwen3-only rerun (the wave-2 precedent, if the owner scopes meralion out):** ≈ **152 cells**.
- **Minimal "fix only the overlapped keys" rerun:** **234 cells** — but this is *not*
  sufficient, because the 30 non-overlap clean cells (11 keys: `librispeech, fleurs-r,
  csemotions, esd, meld, seed-tts-eval-zh, audio2tool, voicebench-advbench, voicebench-ifeval,
  voicebench-mmsu-spoken, air-bench-foundation-speech-grounding`) are only *item*-disjoint, so
  they still need a group-disjoint redraw under the new rule.

**Recommended scope:** full group-lock rerun of the **~260 scored cells** (both backbones) so
the locked holdout is uniform across the grid; if compute-bound, qwen3-only (~150 scored) as a
Stage-1 directional pass, meralion deferred to the confirmatory step. Either way this is a
**one-touch generation pass per cell** (no per-item tuning), matching the existing wave
throughput.

### 4.3 Effort summary

- **~6 new modules** (`locked_split`, `grouping`, `stats`, manifest dir + guards) — the
  statistical core, pure-runner.
- **~6 loader edits** (1-3 lines each except the legacy `p2_baselines` cluster), all additive
  meta fields, none changing existing scoring.
- **2 aggregation-site edits** (`run_baseline.run_one`, `summarize_wave1`).
- **1 GPU rerun** of ~150-260 cells (single-touch generation), gated on owner scope + seed
  sign-off.

---

## 5. Open questions for the owner

1. **Rerun scope:** full 264/~260-cell both-backbone group-lock, or qwen3-only ~150 for a
   Stage-1 directional pass with meralion deferred?
2. **Coarse-group SER** (`esd`/`csemotions`, 10 speakers): accept coarse group-disjoint +
   wide-CI caveat (design default), or item-level fallback?
3. **G-SOURCE legacy loaders** (`SQuAD-zh`, `spoken-squad`, `mmau-mini`, …): worth the
   `p2_baselines.py` edit to expose passage/clip ids, or run them item-level and flag?
4. **Access-control enforcement:** is the process convention + CI grep guard sufficient, or is a
   harder mechanism (separate repo / encrypted manifest) wanted for the locked test dir?
5. Confirm the proposed `LOCKED_TEST_SEED = 611_741_209` (and siblings) are acceptable as the
   one-time locked seeds.

---

*Append-only record. Stage-1 evidence remains hypothesis-grade; this is a design, not a result —
no numbers here are experimental findings. Implementation and any rerun are separate,
owner-gated steps.*
