# POMDP restructure log — collapse W5 to an honest single-model training-free-RL-for-speech paper

> A **partially-observed decision process**. The true state s* ("the honest paper this becomes") is hidden. We hold a
> **belief b**, take the highest-information **action**, record the **observation**, **update** the belief, and
> **roll back** when an observation invalidates a prior step. Newest trajectory entry on top of the log.

## Setup
- **Trigger.** A deep 3-axis adversarial review (principle / purpose / feasibility) reached a conclusive verdict:
  the agent-level / L4 framing does not survive; most flaws are not fixable by revision. Owner: collapse to an honest
  single-model paper (Option A), executed as a POMDP.
- **Termination.** A fresh hostile panel on the restructured paper raises no surviving fundamental challenge; paper
  compiles clean; belief stabilizes. Cap 3 hostile rounds.

## Belief state b (current)
- **b.positive_spine (P≈0.7, UNVERIFIED):** single-model verifiable-reward best-of-N / reranking gives real
  content/intent gains. **BLOCKER:** the paper's opB numbers (SLURP +0.330, URO +0.335, MInDS +0.132) may have been
  produced by a remote DeepSeek API or precomputed scores, not a local frozen model (feasibility S2). → Step 1 probes.
- **b.negative (P≈0.9):** paralinguistics is a negative on the frozen omni content embedding (speaker≈chance, emotion
  null). → Step 2 firms it across models incl. a classic ECAPA reference.
- **b.theory (P≈0.6 cut / 0.4 demote):** the OSA theory is tautology-where-proven; likely cut or demoted to a
  one-paragraph honest lens. → Step 3 decides, informed by whether it does explanatory work.
- **b.agent_program:** cross-session benchmark + agent system + OSA-2/3 → future work (data frozen, stack unbuilt).
- **b.env:** local assets sufficient for Option A (4 generative bases + omni-embed bi-encoder + abundant
  content/intent/QA/paralinguistic sets); only a cross-session corpus is missing (future-work only).

## Trajectory (newest on top)
### t2 — Step 1 CLOSE (MInDS re-run) → belief correction (a rollback of my own suspicion)
- **action:** bounded GPU re-run of `repro_minds14_toolintent.py` (frozen omni-embed bi-encoder, MInDS-14 en-US,
  n=182, seed 42, 3 arms + paired bootstrap).
- **observation o2:** naive=0.720, raw-schema=**0.857**, policy=**0.984**; **policy vs raw-schema = +0.126
  [+0.077,+0.181] SIG** (24 fixes, 1 reg); policy vs naive = +0.264 [+0.198,+0.335] SIG. Artifact committed:
  `_repro/minds14_toolintent_paired.json` + reproduce command.
- **belief correction:** the provenance agent's suspicion that MInDS 0.984 was "MRR misread as Acc@1 0.972" is
  **WRONG** — the policy arm's Acc@1 really is 0.984, and the paper's `0.852→0.984 (+0.132)` is essentially the
  reproduced `0.857→0.984 (+0.126)`. So I **roll back** my planned "cut/replace the MInDS number" action: the NUMBER
  is real and now reproducible-with-a-committed-artifact. What remains genuinely wrong is only (a) the **mechanism**
  attribution (bi-encoder selection, not generative best-of-N) and (b) the **baseline label** ("raw-schema arm
  0.857", not "bare intent-name 0.550"). This is the POMDP paying off: probing corrected a belief I would have
  wrongly acted on.
- **positive-spine status:** SOLID — MInDS is a real, local, frozen-model, verifiable-reward SELECTION gain with a
  committed paired-CI artifact. Sufficient to anchor the collapsed paper's positive result.
- **positioning risk (for Step 4/5):** the collapsed thesis ("frozen-model verifiable selection for speech intent")
  sits near W1's territory (best-of-N/reranking) — the paper must state how it differs (omni-embed encoder + the
  paralinguistic negative + the spread lens, on SLU/intent, not W1's ASR best-of-N). Note for the hostile panel.
- **action chosen next:** Step 2 — signal probe (firm the paralinguistic negative across omni-embed + a classic
  ECAPA reference), then Step 3 (theory's fate).

### t1 — Step 1 OBSERVATION (provenance trace) → belief update
- **observation o1 (forensic, cited):** the three content/intent numbers are produced by the **frozen omni-embed
  bi-encoder** doing cosine retrieval over static text candidate-cards under a verifiable reward
  (`evaluation/tool_intent.py:237,247,258`; `SentenceTransformer(omni-embed-nemotron-3b)`; grep for any local
  generation primitive = **0 matches**). So they are **LOCAL-FROZEN** and honestly keepable — BUT:
  1. **Mis-attributed.** The paper sells them as "generative candidates … Operator-B (Z_B) … best-of-N"
     (`07-feasibility.tex:74`, table caption `:78`, Z_B defined as the thinker–talker `:11`). Reality = a frozen
     **bi-encoder (Operator-A-class) selection over hand-authored cards**, not a generative policy, not best-of-N
     decoding. → must re-word, not cut.
  2. **URO `+0.130` rerank IS remote DeepSeek** (`uro_qa_low_margin_rerank.py:343-344`) — cut or re-run local.
     (The URO `+0.335` base retrieval is local and keepable; the remote step is a separate bracketed rerank.)
  3. **MInDS `0.852→0.984 (+0.132)` is unbacked** by any committed artifact and looks like MRR 0.984 misread as
     Acc@1 0.972; artifact-backed gain is **+0.089 (0.883→0.972)**. → correct or cut.
  4. **No committed score file** for any of the three (only `_repro/emotion_pool_paired_v2.json`, the null). Numbers
     live only as prose in `docs/`. → not reproducible until re-run + committed.
- **belief update:**
  - b.positive_spine: **CONFIRMED real + local**, P≈0.9 — but it is *frozen-bi-encoder verifiable SELECTION*
    (embedding-candidate reranking), **not** generative best-of-N. The "two-operator (embedding vs generative)"
    framing is moot: the reproducible local results are all Operator-A-class selection; the generative operator was
    never run locally. → the collapsed paper's thesis becomes **"training-free RL as verifiable-reward selection on a
    single frozen speech model."**
  - NEW substantive defects to fix in Step 4: (a) re-attribute all three (bi-encoder selection, not generative
    best-of-N); (b) cut the remote-DeepSeek URO rerank from any all-local claim; (c) replace MInDS +0.132 with the
    artifact-backed +0.089; (d) commit reproducible score artifacts.
- **action chosen (closes Step 1):** a **bounded GPU re-run** of the bi-encoder content/intent selection on SLURP +
  MInDS (the clean tasks) to (i) regenerate committed score JSONs + reproduce commands, and (ii) resolve the MInDS
  number honestly from the artifact. Then Step 2 (signal probe) firms the negative.

### t0 — INIT
- **belief:** b0 as above (from the 3-axis diagnosis, archived in `reviews/deep-review.md`).
- **action chosen:** Step 1 — provenance pilot (highest information value: it gates whether Option A has a positive
  empirical spine or must slide toward a negative-results paper).
- **observation:** o1 above.
