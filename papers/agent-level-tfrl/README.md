# Agent-Level Training-Free RL — Research Proposal (W5)

A peer-review-grade research proposal: *Training-Free Reinforcement Learning Has a Vanishing
Optimization Space on Single Models but Recovers in Context-Isolated Agent Systems — Theory and a
Self-Evolving Omni Speech Agent.*

Consolidates the W5 agent-level arc: the **optimization-space-adequacy** theory (OSA-1/2/3,
machine-checked in `proofs/tfrl/TfrlProofs/OptSpace.lean`), the convergence analysis, the feasibility
case (open moat + the two-omni component pairing + the verifiable-reward acceptance gate), preliminary
in-house results, the self-evolving omni speech-agent system design, and the research plan. Built from
the adversarially-verified survey rounds archived under `wiki/survey/`.

## Files
- `main.tex` — the paper (NeurIPS-approximating, self-contained preamble; ~37 pages).
- `references.bib` — 217 adversarially-verified sources (auto-generated; do not hand-edit keys).
- `sections/*.tex` — per-section sources `\input` by the assembler into `main.tex`.
- `build.sh` — build the PDF with a pinned PATH (avoids WSL Windows-PATH interop issues).
- `_build/gen_bib.py`, `_build/assemble.py` — deterministic generators (bib from the source list;
  `main.tex` from `sections/` + the shared preamble/macros).

## Build (WSL2 + TinyTeX)
```bash
bash papers/agent-level-tfrl/build.sh   # 3× pdflatex + bibtex -> main.pdf
```
Requires a TeX distribution (TinyTeX user-space install is sufficient). The build pins
`PATH=$HOME/.TinyTeX/bin/x86_64-linux:/usr/bin:/bin`.

## Regenerate (after editing sections or the source list)
```bash
python3 papers/agent-level-tfrl/_build/gen_bib.py     # -> references.bib
python3 papers/agent-level-tfrl/_build/assemble.py    # sections/*.tex -> main.tex
bash    papers/agent-level-tfrl/build.sh
```

## Status
Compiles clean: **42 pages**, all 217 citations + all cross-references resolve, 0 LaTeX errors,
~43k-token source. The theory section + appendix transcribe the Lean theorems faithfully (the one
documented order-statistics `sorry` in the best-of-N KL bound and the isolated Hoeffding lemma are
flagged as explicit assumptions, never overclaimed).

**Peer review (`reviews/`).** A 5-role adversarial panel (theory-critic · statistician ·
speech-domain · reproducibility-auditor · novelty/red-teamer) + area chair reviewed the paper.
Round 1: **major revision** (correct math, but prose over-claimed). A per-section revision applied
the must-fix items (OSA-2 downgraded to conditional additivity + a Phase-2 spread-floor conjecture;
the dual-use key-agreement reward reclassified as a surrogate, not a verifiable reward; "machine-
checked" qualified to the sorry-free qualitative core vs the conditional quantitative bounds;
convergence reframed as a design principle with the finite-time guarantee open; single-seed /
winner's-curse / contamination caveats on the preliminary results; citation softening). Round 2:
all five reviewers moved to **minor revision** with the gating items resolved; the remaining
residuals were then applied. See `reviews/round1-review.md` and `reviews/round2-rereview.md`.
