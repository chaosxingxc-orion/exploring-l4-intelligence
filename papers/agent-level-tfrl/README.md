# Training-Free RL on Frozen Omni Speech Models (converged single-model paper)

The converged paper: *Training-Free RL on Frozen Omni Speech Models: Reward-Guided Best-of-N, a
Paralinguistic Probe, and a Reward-Spread Lens.*

**History (why the directory is named `agent-level-tfrl`).** This started as the W5 agent-level
proposal ("…Recovers in Context-Isolated Agent Systems", 42 pp, OSA-1/2/3). On 2026-07-02 a
three-axis hostile review (`reviews/deep-review.md`) killed that framing (the `qstar_product`
theorem is a tautology; purpose VoI≈0; the cross-session benchmark unbuildable on frozen data), and
the owner collapsed it — via the POMDP trajectory logged in `reviews/pomdp-restructure-log.md` —
into an honest single-model paper that then **converged after four fresh hostile rounds**
(`reviews/deep-round1..4.md`; 0 surviving fundamental/major). See Decision-Log 2026-07-02.

## The converged contributions
- **C1** — genuine reward-driven best-of-N on a frozen Qwen3-Omni-30B (Q8_0 GGUF, llama.cpp,
  24 GB laptop GPU): multi-seed (n=144) oracle-WER headroom **+0.042 [0.029, 0.056] at N=8**,
  significant from N=4; deployable label-free MBR **non-significant at every N** — an honest
  realized-vs-headroom gap. Artifact: W1 repo `_repro/asr_bon_llamacpp_snr5.json`.
- **C2** — honest frozen-encoder probing (a distinct operator, explicitly *not* RL): content ≈1.0,
  speaker ≈ chance, emotion NULL across seeds.
- **C3** — a reward-spread lens giving sign + ceiling only (`gain = β·KL ≤ spread²/8β`), two
  sorry-free Lean lemmas; the N-curve is order statistics.

The agent-level question is **deferred, not disproved** (§Future work; `sections/04-related-b.tex`
§3.4): re-opening it requires a cross-session corpus, a locally-driven generative operator (now
resolved via llama.cpp), and a genuinely new non-separable irreducibility result. The 2026-07-03
rationality campaign (`wiki/2026-07-03-agentic-tfrl-step1-preregistration.md`) adjudicates exactly
that question.

## Files
- `main.tex` — the converged paper (assembled; self-contained preamble).
- `references.bib` — adversarially-verified sources (auto-generated; do not hand-edit keys).
- `sections/*.tex` — per-section sources `\input` by the assembler into `main.tex`.
- `build.sh` — build the PDF with a pinned PATH (avoids WSL Windows-PATH interop issues).
- `_build/gen_bib.py`, `_build/assemble.py` — deterministic generators.
- `reviews/` — BOTH review chains: the proposal-era rounds 1–4 (`round*-review.md`, `ledger.md`)
  and the collapse chain (`deep-review.md`, `pomdp-restructure-log.md`, `deep-round1..4.md`).

## Build (WSL2 + TinyTeX)
```bash
bash papers/agent-level-tfrl/build.sh   # pdflatex ×3 + bibtex -> main.pdf
python3 papers/agent-level-tfrl/_build/gen_bib.py     # regenerate references.bib
python3 papers/agent-level-tfrl/_build/assemble.py    # sections/*.tex -> main.tex
```

## Status
CONVERGED (2026-07-02, merged via PR #2): four fresh hostile rounds ended fundamental → major →
major → minor with 0 surviving fundamental/major; an integrity reviewer reproduced every C1 number
against the committed artifact. Every number in the paper traces to a committed reproducible
artifact (best-of-N in the W1 repo; probes in the W4 repo).
