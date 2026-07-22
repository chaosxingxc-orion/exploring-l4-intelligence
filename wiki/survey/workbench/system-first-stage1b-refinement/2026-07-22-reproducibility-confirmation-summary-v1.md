# Reproducibility confirmation summary (2026-07-22)

> **Priority status: RESOURCE AUDIT ONLY.** The availability findings remain evidence, but the active
> reproduction routing is superseded by the speech/omni-agent root in
> [`2026-07-22-speech-omni-agent-reproduction-routing-v2.md`](2026-07-22-speech-omni-agent-reproduction-routing-v2.md).
> Do not turn text-only or visual-only A/B rows into dataset, baseline, or reproduction work.

## Outcome

This is the final summary page for the post-Stage-1B secondary-confirmation pass. The denominator is
the **67** papers routed by v4 to `MANUAL_REVIEW_ACCESS_AMBIGUOUS`; the three already page-audited
direct candidates are reported separately and are not added to that denominator.

| Overall result | Count | Meaning |
|---|---:|---|
| A — executable reproduction | 28 | Method, data, and a local/API baseline are available now; high cost is disclosed but is not treated as absence. |
| B — conditional reproduction | 23 | The paper can be rebuilt or approximated, but code, an exact model endpoint, a dataset step, or substantial environment work is missing. |
| C — exact reproduction blocked | 11 | A load-bearing dataset, trace corpus, proprietary environment, or training artifact is unavailable. |
| N — not a reproduction target | 5 | Survey/review only; useful as an instrument or bibliography, not as an experiment to reproduce. |

Thus **51/67** are reproducible at least conditionally, but this is an artifact-readiness statement,
not a Stage-1C problem choice or novelty verdict. The 67 complete one-by-one reports are in
[`2026-07-22-manual-confirmation-67-v1.md`](2026-07-22-manual-confirmation-67-v1.md).

## Three-axis contract

- **Technique** asks whether the method can be implemented without guessing a load-bearing component.
- **Data** asks whether the exact evaluation/training resource is local or can currently be obtained
  under a stated public or controlled-access route. Merely naming a dataset is not enough.
- **Baseline** asks whether at least one meaningful comparator can run locally or through an external
  API. A retired historical model version is marked conditional even when a modern replacement exists.
- Symbols: `YES` = available; `PARTIAL` = obtainable/rebuildable with a disclosed condition;
  `NO` = unavailable load-bearing resource; `N/A` = no experimental target.

Reproducibility and project fit are independent. Papers that train or modify model weights can receive
an A while remaining outside the frozen-black-box execution lane.

## Direct-method reproduction queue

The three direct candidates already audited in v4 remain separate:

| Paper | Technique | Data | Baseline | Current action |
|---|---|---|---|---|
| `2510.02995` [AudioToolAgent](https://arxiv.org/abs/2510.02995) | YES; [released orchestration code](https://github.com/GLJS/AudioToolAgent) | YES; local MMAR and compatible MMAU subset, with public download paths | YES; local/open and API configurations | **First reproduction target** once execution authority is granted. |
| `2509.16971` [AudioGenie-Reasoner](https://arxiv.org/abs/2509.16971) | PARTIAL; method is specified, but no live author repository was found | YES; MMAU-mini and MMAR are local | YES; open/API audio models | Clean-room backup; do not claim exact reproduction. |
| `2606.07264` [VISA](https://arxiv.org/abs/2606.07264) | PARTIAL; frozen-expert routing and disagreement resolution are described, no author code found | YES; MMAR is local | YES; open experts/API backbone can be substituted | Clean-room backup and architecture comparator. |

Two current-state changes affect the queue:

1. `2505.22053` [AudioGenie](https://arxiv.org/abs/2505.22053) should be restored from v4's data-access
   downgrade to **conditional direct**: the [author repository](https://github.com/ryysayhi/AudioGenie)
   and [MA-Bench](https://huggingface.co/datasets/ryysayhi/MA-Bench) are now public, although MA-Bench
   has not been fetched into the frozen local data lock.
2. `2606.15141` [EChO-Agent](https://arxiv.org/abs/2606.15141) moves from the 67-paper ambiguous queue to **conditional direct**. Its
   Tool → Evidence → Reason → Verify pipeline is training-free and fully specified; MMAR is local and
   YAMNet, Whisper, SpeechBrain SER, Essentia, DeepSeek, and Qwen3-Omni are obtainable. No author
   orchestration repository was found, so the first implementation must be called a clean-room replica.

`2605.28192` [AOP-Agent](https://arxiv.org/abs/2605.28192) is a high-value direct-like watch item, not a runnable first target: the method is
training-free and uses open Omni-LLMs, but neither MOV-Bench nor an author code release was found in the
current audit.

## Superseded resource-based execution order

This ordering is retained only as provenance and must not be executed. The v2 modality-first queue is
the authority. No model load, smoke test, metric run, or prototype was performed in this audit.

1. **Artifact-only preflight:** clone AudioToolAgent; fetch/checksum MA-Bench for AudioGenie; freeze
   exact licenses, commit hashes, model IDs, API versions, and expected GPU/API cost.
2. **First exact baseline:** AudioToolAgent on the locally available MMAR slice, preserving the paper's
   baseline configuration and a same-backbone no-tool control.
3. **First clean-room control:** EChO-Agent on the same MMAR slice. Implement only the four published
   stages and label every inferred engineering choice.
4. **Generic control-plane transfers:** Reflexion, LATS, Tree Search for Language Model Agents, CoPS,
   EET, A-MapReduce, and Team of Thoughts. These are reproducible but require a speech/omni adapter.
5. **Keep out of the direct lane:** eSpark, SPEAR, OmniVerifier, Fission-GRPO, T3, GIFT, OmniAgent,
   DeepTool, and other weight-updating/model-internal methods. They are comparators or boundary cases.

## Material live-resource corrections

| Paper/resource | Paper-time or v4 impression | Verified state on 2026-07-22 |
|---|---|---|
| Reflexion | paper URL used the old `noahshinn024` path | Repository is live at `https://github.com/noahshinn/reflexion`. |
| AudioGenie / MA-Bench | MA-Bench was not in the local lock and was treated as unavailable | Code and the MA-Bench release are public; local fetch is still pending. |
| OmniVerifier / ViVerBench | project artifacts were unclear | GitHub contains inference, evaluation, training, and TTS code; ViVerBench is a 3.59k-row Apache-2.0 Hugging Face dataset. |
| MEG semantic reconstruction | no URL in the decoding paper | The underlying 10-hour Donders dataset and preprocessing code are downloadable under the RU-DI-HD-1.0 human-data agreement. |
| GeoToken | repository link exists | Repository is live but explicitly says components/documentation will be updated; treat as incomplete. |
| MATTRL | repository link exists | Repository is essentially README-only in this audit; do not equate URL reachability with code availability. |

## Evidence and limitations

- Every one of the 67 local PDFs was read through page-level extracted evidence for method, data,
  baseline, and artifact claims. Representative pages for EChO-Agent, AOP-Agent, the MEG work, and the
  Turkish hate-speech work were rendered and visually inspected to guard against extraction errors.
- Online checks were limited to author/project pages, GitHub, Hugging Face, arXiv/OpenReview, and
  primary dataset hosts. “No repository found” means no author-linked or exact-title release was found
  by this bounded audit; it is not a proof that no private or newly created repository exists.
- External evidence digest:
  `SPEECHRL_DATA_DIR/survey-fulltext-secondary-analysis/2026-07-22-repro-confirmation-v1/evidence-digest.json`.
  The earlier naive HTTP-probe output was discarded because several hosts returned local SSL EOF
  errors; the paper reports and live primary-source checks are the resource authority.
- This pass authorizes documentation and mapping only. It does not execute Stage-2 reproduction or
  make a novelty/gap claim.
