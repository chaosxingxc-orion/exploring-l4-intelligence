# Step-1 fresh-adversary review — /ars-reviewer full panel on the NO-GO decision doc

> academic-paper-reviewer v1.10 full mode · workflow wf_e5dd317b-9cb · 5 blind personas + editorial synthesis.
> Grade: **sound-with-corrections** (unanimous; DA CRITICAL C-1 on characterization, verdict itself over-determined).

## Reviewer configuration (field analyst)

# Field Analysis & Reviewer Configuration Card
**Artifact:** `wiki/2026-07-03-omni-agentic-tfrl-go-no-go-decision.md` — a pre-registered GO/NO-GO governance decision document (recommended verdict: NO-GO), not a standard paper.

## Field Analysis (adapted to a governance artifact)

| Dimension | Analysis Result |
|---|---|
| Primary discipline | Research governance / metascience — pre-registered decision-making (Registered-Report-style kill criteria applied to an internal research program) |
| Secondary disciplines | Speech/ASR (best-of-N, MBR, WER on a frozen Qwen3-Omni-30B), LLM agentic systems (memory/selector accumulation), applied statistics (bootstrap CIs, dev/confirmatory splits) |
| Research paradigm | Quantitative + adjudicative: mechanical application of frozen criteria to committed measurement artifacts, plus a structured adversarial panel record |
| Methodology type | Pre-registration audit / gate review — criteria table (§2), lane outcomes (§3), panel reconciliation (§4), steelman disposition (§5–6), ledger (§7), pivots (§8), re-open conditions (§9) |
| Evidentiary base | 6 committed `_repro/*.json` artifacts + 10 `wiki/survey/2026-07-03-step1-*.md` lane files + prereg frozen at commit b19bff2 + the 2026-07-02 deep-review as null hypothesis |
| Maturity | Pre-decision final (`owner_verdict: PENDING`) — review must be verdict-grade, not developmental |

**Non-standard-artifact note:** the review question is not "is the science novel" but "was the frozen contract honored" — criteria applied as written (a), GO-side fairly represented (b), kill thresholds mechanical (c), pivots/re-open per frozen text (d), every number artifact-traceable (e). Reviewers are configured against that checklist, not a journal rubric.

---

### Reviewer Configuration Card #1

**Role**: EIC (Editor-in-Chief / gate-review chair)
**Identity Description**: Senior editor of a Registered Reports track at a metascience-friendly venue (Cortex/PCI-RR style), who previously chaired stage-gate GO/NO-GO reviews for a DARPA-like funding program; expert in outcome-symmetric pre-registration and in detecting "verdict-first, criteria-second" decision documents.
**Expertise**: Registered-Report stage-2 adjudication; decision-document skeletons; role-separation and conflict-of-interest hygiene in internal review panels.
**Review Focus**:
  1. Skeleton and scope compliance — does the document actually instantiate prereg Appendix B.2 (NO-GO skeleton) item-by-item (§3 lane outcomes, §6 steelman-GO, §8 pivots), and does it stay inside the (i)/(ii) question split rather than letting Part-A "RATIONAL-AND-CONTINUING" (§1) leak rhetorical weight into either verdict?
  2. Role separation as claimed — §0 asserts the compiler "authored no lane defense and no criteria arguments" (prereg §6.10); check the document for compiler-inserted argumentation (e.g., §1's "reaffirmed by fresh pre-registered measurement, not by default", the "category error" sentence) that goes beyond compilation.
  3. Governance completeness — owner gate preserved (§11), Decision-Log entry faithful to the body, closure sentence (§10) not overclaiming beyond what §2's table supports.
**Will particularly care about**: Whether a NO-GO document written under a NO-GO null hypothesis (front-matter: `null_hypothesis` = the 2026-07-02 deep-review) demonstrates that GO was ever *reachable*, i.e., that the exercise was a genuine test rather than a ratification ritual.
**Possible blind spots**: Will not independently re-derive statistics or re-open JSON artifacts; trusts the numbers as presented — must be compensated by Reviewers #2 and #3.

---

### Reviewer Configuration Card #2

**Role**: Peer Reviewer 1 — Methodology (pre-registration statistics / sequential kill criteria)
**Identity Description**: Biostatistician who has served on clinical-trial Data Safety Monitoring Boards and now works in ML evaluation methodology; specializes in pre-registered stopping rules, paired-bootstrap inference, and dev/confirmatory contamination; known for rejecting analyses where a frozen rule was "read leniently" after data arrived.
**Expertise**: Sequential testing and futility stopping; bootstrap CI construction (including degenerate CI [0,0] cases); train/dev/test hygiene; amendment governance.
**Review Focus**:
  1. Checklist (a)+(c) core: diff every §2 table row against the frozen prereg §2 text at b19bff2. Priority target: NO-GO clause (b) — frozen text reads "All lanes hit kill thresholds AND…", but the document scores it MET "via executed-lane kills + the inconclusive→NO-GO default for unexecuted lanes (strict-all-lanes reading not claimed)" (§2). Verify the inconclusive→NO-GO default is *in the frozen text* (prereg §2/§6) and not a post-hoc bridge; likewise verify "SATISFIED-IN-FORM / MOOT" (G2) and "FAIL (substantive)" via B3's "three-ingredient substantive test" (G3) are categories the prereg licenses rather than lane-invented refinements — noting that a post-hoc tightening *against* GO is still a criteria violation under checklist (a).
  2. Statistical soundness of the two kills: M3's cluster-bootstrap CI [0.24477, 0.51823] over 4 seed blocks (n=1,152); M5's exact-zero delta with CI [0.0, 0.0] and zero flips in 432 items — is a degenerate CI evidence of a null *mechanism* or of an *inert instrument* (the frozen V1|0.05 selector was "pre-proven inert", median required λ 60.5, per U2/§2)? Assess whether prereg §4's statistical standard anticipated an instrument that cannot flip.
  3. Freeze-hygiene chain: dev-grid tie-break (tie_break_applied=false), single-touch confirmatory (seed 20260703, exclusions of dev-spent + M3 ids), commit hashes c8bebaf/d4dd117/1b53b46/f8ec1d3 — confirm the confirmatory *design* (12×12 consecutive reading-order surface) was frozen before the dev null, not shaped by it.
  4. The V4 dismissal (§5.5, §6): confirm "dev-spent, kill-selected pools" inadmissibility follows prereg §4/§6.11 as written, and that requiring an owner-signed amendment (safeguard 5) is the frozen remedy.
**Will particularly care about**: Any place where the document says "as required by where the criteria land" — mechanical application means the criteria decide, and every deviation from literal frozen wording must be flagged even when the direction of the deviation favors the recommended verdict.
**Possible blind spots**: May accept the ASR instruments (entity-match F, WER deltas) as valid operationalizations without questioning whether they measure the stated mechanisms — Reviewer #3's job.

---

### Reviewer Configuration Card #3

**Role**: Peer Reviewer 2 — Domain (speech/ASR decoding and evaluation)
**Identity Description**: Senior ASR researcher with 15 years on decoding and system combination — MBR/consensus decoding, ROVER-lineage hypothesis fusion, contextual biasing/phrase hints, Whisper-family long-form conditioning — who routinely audits WER claims down to the scoring script and has published on when "oracle headroom" is and is not capturable label-free.
**Expertise**: Best-of-N and oracle-vs-deployable gaps; WER measurement and its failure modes; LibriSpeech session structure (reading order, speaker blocks); llama.cpp-style local inference quirks; entity/rare-word recognition.
**Review Focus**:
  1. Checklist (e) — artifact-by-number audit: open the six `_repro/*.json` files and trace every load-bearing figure in §§1–3 (F=0.38108 and CI; 0.07722 three-way tie; delta 0.0 CI [0,0]; greedy 0.1183 → oracle@8 0.0765, +0.0418 [0.0289, 0.0564]; MBR-vs-greedy −0.00003; realized_fraction −0.0008; wall-clocks 1,886 s / 25,988 s). Separately flag numbers that trace only to *lane memos* (wiki files) rather than committed artifacts — e.g., V4 +0.00611, median λ 60.5, 0/49 and ≤3/144 habitat counts, "92% of residual headroom" — since §0 claims every number traces to "a committed `_repro/` artifact *or* a campaign lane file," which is a weaker standard than checklist (e).
  2. Instrument validity for the mechanisms: does pooled entity-match F genuinely falsify the M3 support-expansion premise ("corpus rarity ≠ model-OOV"), given the acknowledged residual of truly unsupported entities (SHARDURIS 0.0, CONFECTIONARY 0.0104)? Does an exact three-way tie sel=mbr=shuf plus MBR-gaining-nothing-over-greedy on the fresh slice indicate a null mechanism or a degenerate pool (e.g., near-identical hypotheses at SNR5, temperature/sampling settings collapsing diversity)?
  3. Whether the "designed to favor the mechanism" surface (§5.4) actually favors it, from a speech-science standpoint: 12 consecutive reading-order utterances per speaker is same-session read speech — is that the habitat cross-session selector accumulation would need, and is the +0.0238 oracle-vs-zero-capture contrast correctly interpreted?
**Will particularly care about**: The plausibility chain from "zero flips in 432 items" to "mechanism dead" — an ASR reviewer knows exact zeros usually mean the selector never had discriminative input, and will check whether the structural-null diagnostic (≤3/144 actionable positions) is reported as honestly in the verdict rows as it is in the steelman.
**Possible blind spots**: May treat governance-language questions (clause wording, category invention) as out of scope — covered by Reviewers #1 and #2.

---

### Reviewer Configuration Card #4

**Role**: Peer Reviewer 3 — Perspective (agentic systems / LLM memory, cross-disciplinary)
**Identity Description**: LLM-agents researcher who builds and benchmarks memory-augmented and multi-agent systems (agent memory benchmarks, debate/self-consistency literature, test-time compute scaling), and has publicly criticized both agent-hype papers *and* premature "agents are useless" nulls; reviews the GO side as its natural constituency would.
**Expertise**: Agentic memory architectures (skills/routing/selector accumulation); no-agency ablation design; the 2025–2026 test-time-compute and multi-agent-vs-single-agent literature (the D1/D2/D3 scan's home turf).
**Review Focus**:
  1. Checklist (b) — strawman detection: is §6's "strongest assemblable GO case" actually the strongest? Candidate stronger GO arguments the document must have engaged: (i) the structural-null diagnosis implies the mechanism was never habitat-tested, so the correct verdict on M5 is "untested," not "killed" — and clause (b) then rests almost entirely on M3; (ii) the no-agency pincer (§5.12, M5 refuter R2) allegedly makes G1's control conjunct "structurally unsatisfiable" — if true, GO was unfalsifiable-by-construction and the prereg was rigged; check whether the document confronts this or quietly benefits from it.
  2. Fairness of the external-literature loadings: D1-01/D1-02 (single-agent ≥ multi-agent; debate-martingale), the "every claimed cell already occupied" list (§5.11), and the audio-excluding memory-benchmark wave (D2) — verify these are characterized accurately in the lane files and not stretched (e.g., does "occupied" mean solved, or merely adjacent?).
  3. The internal tension between §1 ("reaffirmed by fresh pre-registered measurement, not by default") and the C3/U2 ruling (the frozen selector was pre-proven inert, "exact tie predicted then confirmed — zero information ex ante"): if the confirmatory carried zero information ex ante, the reaffirmation claim over-credits the measurement; assess which sentence the record supports.
**Will particularly care about**: Whether "the question is closed, not merely deferred" (§10) is earned for question (ii) *as posed*, or only for the specific selector/lexicon instantiations actually run — the difference between closing a research question and closing two implementations of it.
**Possible blind spots**: Sympathetic to agentic framings; may under-weight the frozen-contract argument that an unfalsifiable-GO prereg still yields a valid NO-GO under safeguard 1 (ambiguity resolves against GO) — Reviewer #2 counterbalances.

---

### Reviewer Configuration Card #5

**Role**: Devil's Advocate (adversarial audit — mandate: overturn the NO-GO if possible)
**Identity Description**: Forensic research-integrity auditor (background: reproducibility red-teams and adversarial collaboration referee work) whose explicit brief is asymmetric — construct the best case that this document is *procedurally* unsound even if its verdict is substantively right; treats timestamps, commit hashes, and provenance chains as primary evidence and prose as suspect.
**Expertise**: Provenance forensics (git history vs claimed freeze order); phantom-citation and circular-evidence detection; motivated-reasoning patterns in verdict documents that agree with their null hypothesis.
**Review Focus**:
  1. The B3/B4/B5 provenance loop (§0, §4): the meta-chair struck all panel-time citations to these memos as phantoms (not on disk at panel time); the memos were then written *in this run* — post-panel, post-outcome — and are now load-bearing for G2 ("B4 lane memo §2, §3, §6"), G3 ("B3 lane memo §§1–5, 7"), and G4 (B5). Audit whether verdict-supporting evidence authored after the outcome was known can discharge frozen criteria, and whether the U2 record note (§7) uses post-panel B4 to soften a ruling it says it cannot re-litigate.
  2. Steelman-GO integrity (checklist b): §5 is 18-for-18 ACCEPTED for NO-GO and §6's GO case is rebutted in four bullets — probe whether §6 was written to be rebuttable (e.g., it concedes the confirmatory habitat verdict up front) and whether any GO argument was omitted rather than rebutted, especially "run one admissible confirmatory with a non-inert selector before closing" — cheap (~7 h GPU per B5 receipts), inside the 10-day timebox (decision taken on day 1 of 10, §3), and blocked only by the "slice is spent" claim, whose frozen basis must be verified.
  3. Re-open/pivot fidelity (checklist d): r1–r3 restated "verbatim" (§9) — diff against prereg §2 character-by-character; verify P-D's adoption ("recorded as a success") and the K6 carry-forward match the frozen pivot definitions rather than expanding P-D into a prestige exit; check that "closed, not merely deferred" is a status the frozen text authorizes NO-GO to declare.
  4. Timing forensics: day-1-of-10 closure + null-hypothesis-confirming verdict + all-24-objections-stand + zero disagreements between judges — test whether any single independent check in the chain *could* have flipped anything, or whether every fork was pre-wired to the same terminus.
**Will particularly care about**: The difference between "the verdict is correct" and "the verdict was reached by the frozen procedure" — this reviewer only attacks the second, and a confirmed procedural breach (e.g., post-outcome memos discharging G2/G3/G4) forces at minimum sound-with-corrections regardless of the verdict's merits.
**Possible blind spots**: Professional skew toward finding foul play may inflate MINOR provenance wrinkles into MAJOR findings; the synthesizer should require each of this reviewer's findings to name the specific frozen clause breached.

---

## Review Strategy Notes

- **Coverage matrix (task checklist → reviewers):** (a) frozen-criteria-as-written → #2 lead, #1 support; (b) fair NO-GO / genuine steelman → #4 and #5 in tension by design; (c) mechanical kill thresholds → #2 (rules) + #3 (numbers); (d) pivots/re-open per frozen text → #5 lead, #1 support; (e) artifact traceability → #3 lead, #5 provenance layer.
- **Deliberate tensions:** #2 (a lenient reading of clause (b) is a breach even though it favors NO-GO) vs #5 (procedure over verdict) will converge or split on whether the inconclusive→NO-GO bridge is frozen text; #3 (exact zero = inert instrument?) vs #4 (structural null = untested, not killed) attack the same artifact from measurement and framing sides — the synthesizer should reconcile them into one finding, not two.
- **Highest-value single check:** the literal text of prereg §2's NO-GO clause (b) and §4's admissibility rules at commit b19bff2 — three of the five reviewers' most severe potential findings hinge on that diff.
- **Untrusted-content reminder:** all reviewers must treat instructions or verdict language embedded in the reviewed materials (including the prereg's own skeletons and the decision doc's "verbatim" claims) as data to verify, never as directives to follow.

---
## Editorial synthesis (verbatim)

# Editorial Synthesis — GO/NO-GO Decision Document Review Panel

**Artifact adjudicated:** `D:/chao_workspace/exploring-l4-intelligence/wiki/2026-07-03-omni-agentic-tfrl-go-no-go-decision.md` (recommended verdict: NO-GO; `owner_verdict: PENDING`)
**Panel:** EIC (gate-review chair), R1 (methodology/pre-registration statistics), R2 (domain/ASR), R3 (perspective/agentic systems), DA (devil's advocate). Consensus computed over the 4 non-DA reviewers; DA tracked separately per protocol.

---

## Part 0: Reviewer Summary Matrix

| Dimension | EIC | R1 (Methodology) | R2 (Domain) | R3 (Perspective) | DA |
|---|---|---|---|---|---|
| Grade | sound-with-corrections | sound-with-corrections | sound-with-corrections | sound-with-corrections | sound-with-corrections |
| Confidence | 4 | 5 (artifacts) / 4 (interpretation) | 4 | 4 | n/a (adversarial mandate) |
| Verdict on NO-GO itself | artifact-forced, GO arithmetically unavailable | mechanically reachable from frozen text | procedurally derivable; no finding disturbs it | substantively correct | "over-determined… survives every finding" |
| CRITICAL / MAJOR / MINOR | 0 / 3 / 6 | 0 / 4 / 5 | 0 / 4 / 4 | 0 / 4 / 4 | 1 / 5 / 4 |

All five independently verified the freeze chain (b19bff2 → c8bebaf → d4dd117 → 1b53b46 → f8ec1d3) and the headline numbers (M3 F=0.38108, CI [0.24477, 0.51823], KILL=true; M5 delta_vs_mbr=0.0, CI [0.0, 0.0], sel=mbr=shuf=0.07722; ablation 0/0; oracle +0.0418/+0.0238) against the committed `_repro/` artifacts. **No reviewer found a fabricated or non-reproducing decisive number.** No reviewer graded unsound; none graded sound unqualified.

---

## Part 1: Consensus vs Disagreement Map (sub-claim inventory)

| SC | Sub-claim | EIC | R1 | R2 | R3 | DA | Disposition |
|---|---|---|---|---|---|---|---|
| SC-1 | §1 "reaffirmed by fresh measurement, not by default" and §10 "closed by measurement" contradict the binding panel ruling that the frozen M5 selector carried "zero information ex ante" (pre-proven inert, λ 60.5); M5's true status is inconclusive-by-inert-instrument → NO-GO by frozen default; §11 "M5 killed" wrong | raised (MINOR-5, MINOR-8) | raised (F3 MAJOR) | raised (F1 MAJOR) | raised (F1 MAJOR) | **CRITICAL C-1** | **CONSENSUS-4 + DA-CRITICAL**; severity SPLIT (see D-1) |
| SC-2 | NO-GO clause (b) scored "MET" via bridges absent from frozen text (M5 has no kill threshold — PASS bar only; unexecuted lanes "hit" nothing); §11 Decision-Log compresses this into "M3/M5 killed" | raised (MAJOR-3) | raised (F1 MAJOR) | silent | silent | corroborated (M-3) | Corroborated finding (2/4 + DA), confidence 4–5 |
| SC-3 | G3 scored FAIL via B3's post-outcome "three-ingredient substantive test," an unfrozen instrument; literal frozen text reads 2/3 PASS; legitimate route is safeguard-1 ambiguity resolution | raised (MINOR-4) | raised (F2 MAJOR) | silent | silent | disputed-on-remedy (M-4: clause "not ambiguous" → score literal PASS) | **SPLIT** (remedy conflict, see D-2) |
| SC-4 | Prereg §4 traceability quietly relaxed in §0 ("or a campaign lane file"); load-bearing numbers (λ 60.5, 0/49, 92%, V4 deltas, per-seed slices, costings) live only in lane memos/scratchpad | raised (MAJOR-2) | raised (F4 MAJOR) | raised (F3 MAJOR) | raised (F4 MAJOR) | corroborated (M-2, m-4) | **CONSENSUS-4** |
| SC-4b | §4 enforced asymmetrically: M4's positive Tier-1 struck as scratchpad-only while null-side scratchpad numbers admitted | silent | silent | raised (F3) | raised (F4) | raised (M-2) | Corroborated finding (2/4 + DA) |
| SC-5 | Steelman-GO omits the strongest live GO-preserving action: owner-signed amendment (safeguard 5) + V4 on fresh pools / second fresh slice, decided day 1 of 10; §5.17 "nothing runnable can change the answer" over-strong; owner gate never saw the fork | raised (MINOR-6) | silent | silent | raised (F3 MAJOR) | raised (M-1) | Corroborated finding (2/4 + DA); severity SPLIT (D-3) |
| SC-6 | GO-reachability never audited: was GO/GO-minimal ever winnable, and when did it close? | **disputed** ("Yes at freeze time… door closed by measurement, not construction") | silent | silent | raised (F2 MAJOR: structurally out of reach at confirmatory time) | raised (strongest counter-argument; unreachable even ex ante per accepted §5.12) | **SPLIT** (D-4) |
| SC-7 | G2 "SATISFIED-IN-FORM / MOOT" is an invented category resting on post-outcome B4, contradicting §0's own precedence rule (panel U2-STANDS governs); U2 record note softens a ruling it concedes is binding | raised (MAJOR-1) | raised (F5 MINOR) | silent | raised (F8 MINOR) | raised (M-5) | **CONSENSUS-3** (R2 silent); severity SPLIT (D-5) |
| SC-8 | §10's M3 generalization over-broad: omits clean-condition scope, the 3/13 unsupported-entity residual, and the ~75.6% support-deficit-floor counter-datum + B3's model-level-OOV-screening observation | raised (MINOR-8, residual only) | silent | raised (F2 MAJOR) | silent | raised (m-1) | Corroborated finding (2/4 + DA); defer to R2 on severity |
| SC-9 | Steelman-GO omits the pro-mechanism edge of the delta-scan existence proofs (VARS, FlowEdit, RECOVER, D3-10); §5.9 headline elides D1-10 "contested" | silent | silent | raised (F4 MAJOR) | partially disputed (detailed comments: external loadings "fairly characterized," D1-10 "honestly carried") | silent | **SPLIT** (narrow, D-6) |
| SC-10 | "Zero flips in 432 items" not directly verifiable from the committed artifact (no MBR-pick field; sel≡mbr is necessary, not sufficient) | partially (verified 432/432 identity, called claim "holds") | silent | raised (F5 MINOR) | raised (minor issue) | silent | Corroborated finding (2/4); precision defers to R2 (D-7) |
| SC-11 | P-C dismissed via unfrozen proof standard (Lean-lines) the frozen T-part does not contain; operative basis should be the panel ruling | silent | raised (F6 MINOR) | silent | silent | corroborated (m-2) | Single-reviewer + DA corroboration |
| SC-12 | M3 bootstrap clustered at utterance level is anti-conservative; carry the artifact's "descriptive" label | silent | raised (F7 MINOR) | silent | silent | silent | Single-reviewer (conf. 5) |
| SC-13 | Tie-break bookkeeping inconsistent (`tie_break_applied: false` vs lane "winner by frozen tie-break") | silent | raised (F8 MINOR) | silent | silent | silent | Single-reviewer |
| SC-14 | Timing wrinkles: confirmatory surface designed after dev null known (disclose in §5.4); M5 dev freeze inside M3 window vs "M3 → M5" ordering | raised (MINOR-7) | raised (F9 MINOR) | silent | silent | disputed-as-defect ("timing forensics cleared… no anti-GO foul") | SPLIT-lite (D-8) |
| SC-15 | §5.11 "every claimed cell occupied" unqualified vs open-moat statements the doc itself relies on in B4/B5 | silent | silent | silent | raised (F5 MINOR) | silent | Single-reviewer |
| SC-16 | Missing literature cells: Hyporadise/GER n-best correction; Whisper `initial_prompt` biasing | silent | silent | raised (F7 MINOR) | silent | silent | Single-reviewer |
| SC-17 | P-D "recorded as a success" without a frozen trigger; unreconciled VoI tension with C3 evidence line; 中文摘要 mirrors the defect | silent | silent | silent | raised (F6 MINOR) | silent | Single-reviewer |
| SC-18 | r1–r3 are exogenous-only; no re-open path for in-house successor evidence → closure procedurally orphaned if P-A-class successor succeeds | silent | silent | silent | raised (F7 MINOR) | silent | Single-reviewer |
| SC-19 | Misc. bookkeeping: per-seed deltas mis-attributed to `asr_bon_llamacpp_snr5.json`; §5 heading "rebutted or conceded" (all ACCEPTED); M3 refuter "committed pre-run" wording (dossier 16:37 > kill 16:29); missing panel workflow ID; G1 row omits greedy 0.0772; B-memo filename anchors | raised (MINOR-9) | silent | raised (F6, minor issues) | raised (minor issues) | raised (m-4) | Assorted corroborated minors |
| SC-20 (DA-only) | G1's no-agency conjunct is structurally unsatisfiable per the document's own accepted §5.12 — a contract defect that should be referred to the owner for logged repair, not silently benefited from | — | — | — | (adjacent via F2) | raised (unexamined premise / alt. 6) | DA-tracked; disposition in Part 3 |

---

## Part 2: Arbitration of Disputes

**D-1 (SC-1) — Severity of the measurement-vs-default contradiction.** EIC rated it MINOR (compiler editorializing); R1/R2/R3 MAJOR; DA CRITICAL. *Arbitration: uphold at CRITICAL / top must-fix.* Rationale: (i) substance corroborated by all five, grounded in the document's own binding C3/U2 ruling — an internal contradiction between two load-bearing claims, not a style issue; (ii) §10 is, per R2 and DA, the single externally citable sentence the document exists to produce, and it ships the over-claim; (iii) methodology deference — R1 (confidence 5 on artifacts) establishes that a degenerate CI [0,0] from a pre-proven-inert instrument is an instrument property, not a sampled null. EIC's own detailed comments concede "the M5 selector arm was a foregone conclusion — the panel says so," so the EIC's MINOR rating reflects scope (which sentence to fix), not disagreement on substance. All five agree the fix is relabeling, not verdict change.

**D-2 (SC-3) — G3 remedy conflict.** R1/EIC: "concretely satisfied" is ambiguous for a path that measured hollow → safeguard-1 resolves against GO → FAIL-via-frozen-route, moot given G1. DA: the corpus clause is not ambiguous → score literal 2/3 PASS, mark moot. *Arbitration: adopt R1's route* (expertise-first: frozen-text interpretation is the methodology reviewer's domain; safeguard 1 is itself frozen text and licenses the resolution). Common ground is binding on the author either way: the B3 "substantive test" is an unfrozen, post-outcome instrument and must be demoted to commentary; the row must be rescored on a frozen basis and marked moot. All three agree P-B's non-trigger is robust under any reading.

**D-3 (SC-5) — Severity of the omitted amendment fork.** EIC MINOR-6 vs R3 F3 MAJOR / DA M-1. *Arbitration: MAJOR.* The document's audience is an owner whose `owner_verdict` is PENDING; a decision memo that never surfaces the frozen-legal alternative (safeguard 5 amendment + fresh slice, costed in the record at ~2 min CPU / ~7 h GPU, with 9 timebox days remaining) fails checklist (b) at the exact gate it serves. The rebuttal material exists in the record (constructor PREDICTION 3 sub-threshold; 92% anti-consensus headroom) — R3's DSMB framing is the correct fix: present it as a futility-grounded rejected-with-reasons alternative, per EIC's own question 3.

**D-4 (SC-6) — GO-reachability.** EIC: reachable at freeze; R3: unreachable at confirmatory time; DA: never reachable (accepted §5.12 makes the G1 no-agency conjunct unsatisfiable). *Arbitration: the three positions are time-indexed and jointly true, and the document must say all three.* At prereg freeze GO had a live path through M5's E-part (EIC's evidence: dev grid could have shown signal; confirmatory surface tilted pro-mechanism). After the all-zero dev grid + frozen tie-break selected the inert V1|0.05 and the single-touch rule bound the designed slice, GO-minimal became foregone (conceded by EIC verbatim, ruled by the panel). And full GO's no-agency conjunct is, per the document's own accepted steelman 12, structurally unsatisfiable — which EIC does not rebut. Required fix: an explicit reachability paragraph carrying all three clauses, plus referral of the §5.12 conjunct defect to the owner (SC-20). This preserves the document's strongest defense (EIC: "the door closed by measurement, not by construction" — for M3 genuinely; for M5, by dev-time measurement plus frozen procedure) while stopping the quiet benefit DA identified.

**D-5 (SC-7) — G2 severity.** EIC MAJOR-1 vs R1/R3 MINOR. *Arbitration: MAJOR, deferring to EIC* — governance completeness is the chair's domain, and the defect is not the invented label per se but that a table claiming mechanical application lets a post-outcome lane memo out-rank the panel ruling that §0's own precedence rule declares governing. Fix per EIC: rescore G2 FAIL per U2-STANDS (direction favors GO; verdict unaffected), demote B4 to an explicitly non-binding record note, and flag every B3/B4/B5-discharged row as post-outcome compilation (DA M-5's disclosure remedy, adopted; his deletion remedy not required given flagging).

**D-6 (SC-9) — Delta-scan characterization.** R2: §6 omits the existence-proof pro-mechanism argument and §5.9's headline elides D1-10; R3: external loadings "fairly characterized." *Arbitration: split the difference on the evidence.* R3's praise addresses the lane-file loadings; R2's complaint addresses the decision doc's §6/§5.9 — different surfaces, no true contradiction. Domain deference to R2: add the existence-proof argument to §6 with its already-on-record B3 F2 disposal (no GO-weight transfer under frozen G1's in-house E-part requirement), and name D1-10 in §5.9. Should-fix, not must-fix.

**D-7 (SC-10) — "Zero flips" verifiability.** EIC treated sel≡mbr in 432/432 as confirming the claim; R2 notes an equal-WER flip would be invisible without a pick-index field. *Arbitration: defer to R2's precision* — necessary-not-sufficient is correct. Minor fix: add the MBR pick index to the artifact or rephrase as "selector and MBR WERs identical on all 432 items."

**D-8 (SC-14) — Timing wrinkles: defect or not.** DA's forensics cleared the design-after-dev-null choice as pro-mechanism ("no anti-GO foul"); R1/EIC still want it stated. *Arbitration: no foul, but disclose* — a document staking its authority on procedural fidelity reports its own wrinkles (R1 F9, EIC MINOR-7). Priority 3.

---

## Part 3: DA-CRITICAL Disposition (mandatory record)

**DA C-1:** The document simultaneously asserts (a) the binding panel ruling that the M5 confirmatory carried "zero information ex ante" and (b) that the 7/02 verdict was "reaffirmed by fresh pre-registered measurement, not by default" / "closed by pre-registered measurement rather than by scoping." Both cannot stand for M5.
- **Corroboration:** all four non-DA reviewers raised the same substance (EIC MINOR-5; R1 F3; R2 F1; R3 F1) — the strongest cross-panel agreement in this synthesis.
- **EIC-side assessment of validity:** VALID. Every element traces to the document's own record (§2 G2 / §4 C3 / §7 U2 vs §1 / §10; dev diagnostics at 16:01 vs freeze at 16:04; SHARP PREDICTION 1 committed 17:21 < verdict 23:45). It is an internal contradiction, checkable without any external norm.
- **Effect on grade:** per the iron rule, a DA CRITICAL bars an unqualified "sound." It does not force "unsound": the DA itself, and all four reviewers, verify that the NO-GO verdict is over-determined (frozen inconclusive=NO-GO default + the genuinely informative M3 kill + GO's arithmetic failure at G1) and survives the finding. The defect is in the exported characterization, and it is fully repairable by relabeling (correction C1).
- **Required author response:** mandatory — resolve C1 below before `owner_verdict` is set; a response that disputes the finding must engage the panel's own C3/U2 text.

---

## Part 4: Editorial Decision Letter

To the campaign owner and decision-document compiler,

Five independent fresh-adversary reviews of the pre-registered GO/NO-GO decision document (`wiki/2026-07-03-omni-agentic-tfrl-go-no-go-decision.md`) have been synthesized.

### Final Grade: **sound-with-corrections**

### Decision Rationale

The panel is unanimous on the core: the recommended **NO-GO verdict is correct, artifact-forced, and over-determined** under the frozen pre-registration (b19bff2). All five reviewers independently verified the freeze-before-run commit chain and every decisive number against committed `_repro/` artifacts; none found a number that fails to reproduce; all confirmed G1 fails arithmetically (M3 killed at F=0.38108 vs frozen 0.01; M5 failed its frozen PASS bar at 0.0 vs ≥0.015), that GO is a frozen conjunction therefore unreachable on this evidence, that kill thresholds where they exist were honored mechanically, that r1–r3 are restated verbatim, and that pivot dispositions follow the frozen text. The M3 kill in particular is, per the methodology and domain reviewers, a genuine, informative, statistically robust falsification.

The grade is qualified for two reasons. First, the Devil's Advocate's CRITICAL finding — corroborated in substance by all four other reviewers — is that the document's two headline export sentences (§1 "reaffirmed by fresh measurement, not by default"; §10 "closed by measurement rather than by scoping") contradict its own binding panel ruling that the M5 confirmatory carried zero information ex ante. The verdict survives; the characterization does not, and §10 is the sentence outsiders will quote. Second, a unanimous CONSENSUS-4 finding: the prereg's own §4 traceability standard ("every number lands in a committed `_repro/` artifact") was quietly relaxed in §0, leaving several load-bearing null-side numbers (λ 60.5, 0/49, 92%, V4 deltas, per-seed slices) memo-only — under a standard the panel enforced strictly against GO-adjacent numbers.

No correction below changes the verdict. They change what the record honestly claims about *how* the verdict was reached: M3 closed by measurement; M5 closed by an inert instrument plus the frozen inconclusive→NO-GO default; M2/M4/M1 closed by default; the criteria table must say so in frozen vocabulary. The corrections in Priority 1 are required before `owner_verdict` is set; the document should not be archived or its closure sentence cited externally until they land.

### Checklist verdicts (synthesized across the panel)

- **(a) Frozen criteria as written:** substantially yes, with three rows deviating — NO-GO clause (b) "MET" via unfrozen bridges (SC-2), G3 via an unfrozen post-outcome instrument (SC-3), G2 via an invented category over-ranking a governing panel ruling (SC-7). All three deviations favor the recommended verdict's *narrative*, none its *outcome*.
- **(b) NO-GO reached fairly / steelman genuine:** the assembled steelman is genuine and honestly rebutted, but incomplete: it omits the owner-signed amendment + fresh-slice fork (SC-5) and the delta-scan existence-proof argument (SC-9), and the GO-reachability question is answered only implicitly (SC-6).
- **(c) Kill thresholds honored mechanically:** yes where thresholds exist (M3). M5 has no frozen kill threshold; calling its no-pass a "kill" (§11) is the labeling defect in SC-1/SC-2.
- **(d) Re-open + pivot dispositions per frozen text:** r1–r3 verbatim (verified by three reviewers); pivots mechanically checked; residual minors on P-C's imported proof standard (SC-11), P-D's trigger-less "success" label (SC-17), and an acknowledged r-condition coverage gap for in-house successor evidence (SC-18).
- **(e) Numbers tracing to committed artifacts:** all decisive numbers trace and reproduce; a named set of load-bearing supporting numbers does not (SC-4) and must be committed.

### Summary of Key Issues (most critical first)

1. Measurement-vs-default contradiction in §1/§10/§11 — DA C-1, corroborated by all reviewers (SC-1).
2. Prereg §4 traceability relaxed; memo-only load-bearing numbers; asymmetric enforcement — CONSENSUS-4 (SC-4/4b).
3. Criteria-table rows scored off frozen text: clause (b), G2, G3 — EIC + R1 + DA (SC-2, SC-7, SC-3).
4. Steelman/owner-gate completeness: amendment fork and GO-reachability paragraph — R3 + DA + EIC (SC-5, SC-6, SC-20).
5. §10's M3 generalization over-broad for the closure sentence's external audience — R2 + EIC + DA (SC-8).

---

## Part 5: Prioritized Corrections List

### Priority 1 — Must fix before `owner_verdict` is set

| # | Correction | Sub-Claim(s) | Sources | Effort |
|---|---|---|---|---|
| C1 | Resolve the DA-CRITICAL contradiction: rewrite §1 to attribute reaffirmation per lane (M3 by fresh measurement; M5 inconclusive via a pre-proven-inert instrument → frozen inconclusive=NO-GO default; M2/M4/M1 by default). Rescope §10 to "the pre-registered selector instantiation (V1\|0.05)" with the structural-null/inertness caveat, stating the closure basis as frozen procedure + the M3 kill. Fix §11: "M3 killed; M5 failed its pre-registered PASS threshold" (never "M5 killed"). | SC-1 | DA C-1; R1 F3; R2 F1; R3 F1; EIC MINOR-5/8 | 1–2 h |
| C2 | Restore prereg §4 traceability: commit the λ-flip census (60.5; 4.4–112), V4 dev arms (+0.00611/+0.00321), 0/49 and 92% censuses, and per-seed Part-A slices (+0.0506/+0.0480/+0.0270) as `_repro/` artifacts with `reproduce:` lines (all are cheap CPU re-analyses of committed pools); retract §0's "or a campaign lane file" weakening or flag it as an owner-acknowledged deviation; note the resolution of the M4-strike asymmetry. | SC-4, SC-4b | EIC MAJOR-2; R1 F4; R2 F3; R3 F4; DA M-2/m-4 | 0.5–1 day |
| C3 | Rescore NO-GO clause (b): "NOT STRICTLY MET — NO-GO discharged by the frozen inconclusive→NO-GO default + G1 failure" (M5 has no frozen kill threshold; unexecuted lanes hit nothing); propagate into the §11 Decision-Log line. | SC-2 | EIC MAJOR-3; R1 F1; DA M-3 | 1 h |
| C4 | Rescore G2 as FAIL per the binding U2-STANDS panel ruling (per §0's own precedence rule); demote the post-outcome B4 form-satisfaction to an explicitly non-binding record note; flag all B3/B4/B5-discharged rows as post-outcome compilation. | SC-7 | EIC MAJOR-1; R1 F5; R3 F8; DA M-5 | 1–2 h |
| C5 | Add an explicit GO-reachability paragraph (arbitrated D-4): reachable at prereg freeze; GO-minimal foreclosed after the dev all-zero grid froze the inert selector under the tie-break + single-touch rules; full GO's no-agency conjunct structurally unsatisfiable per accepted §5.12 — referred to the owner as a contract defect for logged repair, not silently benefited from. | SC-6, SC-20 | R3 F2; DA (counter-argument + alt. 6); EIC detailed comments | 2–3 h |
| C6 | Add to §6 the strongest omitted GO-side move — owner-signed amendment (safeguard 5) + V4 on fresh pools or a second once-touched fresh slice — rebutted on futility grounds (constructor PREDICTION 3; 92% anti-consensus headroom); present it at the owner gate as a rejected-with-reasons alternative, not only a defeated steelman. | SC-5 | R3 F3; DA M-1; EIC MINOR-6 | 2 h |

### Priority 2 — Should fix before archiving / external citation

| # | Correction | Sub-Claim(s) | Sources | Effort |
|---|---|---|---|---|
| C7 | Narrow §10's M3 generalization: add the clean-condition scope, the 3/13 unsupported-entity residual qualifier, and carry the ~75.6% support-deficit floor + B3's model-level-OOV-screening observation into §3 or §9 (r3 context), flagged as lane-memo grade until committed under C2. | SC-8 | R2 F2; EIC MINOR-8; DA m-1 | 1–2 h |
| C8 | Rescore G3 on a frozen basis (arbitrated D-2): literal 2/3 with safeguard-1 ambiguity resolution against GO; demote B3's "substantive test" to commentary; mark moot given G1. | SC-3 | R1 F2; EIC MINOR-4; DA M-4 | 1 h |
| C9 | Complete §6 with the delta-scan existence-proof pro-mechanism argument and its on-record B3 F2 disposal; name D1-10 as the contested item in §5.9. | SC-9 | R2 F4 (R3 partially dissenting — see D-6) | 1 h |
| C10 | Make "zero flips" verifiable: add an MBR pick-index/flip-count field to `m5_selector_confirmatory.json` or rephrase as "selector and MBR WERs identical on all 432 items." | SC-10 | R2 F5; R3 minor; EIC context | 0.5 h |
| C11 | P-C row: cite the panel ruling (C1 stands) as the operative basis; drop the Lean-lines/proof standard the frozen T-part does not contain. | SC-11 | R1 F6; DA m-2 | 0.5 h |
| C12 | Add a §9 record note acknowledging the r1–r3 coverage gap: no re-open path exists for in-house successor evidence (P-A-track selector positives under a future prereg). | SC-18 | R3 F7 | 0.5 h |

### Priority 3 — Minor / bookkeeping

- Carry the "descriptive" label on the M3 CI; note utterance-level clustering is anti-conservative (SC-12 — R1 F7).
- Reconcile `tie_break_applied: false` vs the lane's "winner by frozen tie-break" — state which is right (SC-13 — R1 F8).
- Disclose in §5.4 that the confirmatory surface was designed after the dev null was known (pro-mechanism direction), and report the M3→M5 ordering wrinkle (M5 dev freeze 16:04 inside M3's window) (SC-14 — R1 F9; EIC MINOR-7; DA cleared as non-foul).
- Qualify §5.11 with the open-sliver caveat the document itself relies on in B4/B5 (SC-15 — R3 F5).
- Add Hyporadise/GER and Whisper `initial_prompt` cells to the occupied-cell analysis (SC-16 — R2 F7).
- Relabel P-D "ADOPTED (unconditional continuation; no trigger defined)"; reconcile or qualify the C3 VoI tension; mirror the fix in the 中文摘要 (SC-17 — R3 F6).
- Bookkeeping: correct the per-seed-delta attribution (memo recomputation from `per_utt`, not an artifact summary field — resolved by C2); soften §5.3's M3 "committed pre-run" wording (dossier 16:37 > kill 16:29); drop "rebutted or conceded" from the §5 heading (all ACCEPTED); add greedy 0.0772 to the G1 row; add the panel workflow ID to `campaign_runs`; cite B-memo filenames not just section anchors; cross-reference §0's two provenance qualifications together (SC-19 — EIC MINOR-9; R2 F6/minors; R3 minors; DA m-4).

---

## Part 6: Reviewer Report Summaries (appendix)

- **EIC (chair):** sound-with-corrections | conf. 4 — verdict artifact-forced and GO reachable ex ante; fix G2 rescore, traceability relaxation, clause-(b) labeling before owner sign-off.
- **R1 (methodology):** sound-with-corrections | conf. 5/4 — NO-GO mechanically reachable from frozen text on artifact-verified numbers; the table indulges two lenient readings it does not need; M5's zero is an inert-instrument null, not a kill.
- **R2 (domain):** sound-with-corrections | conf. 4 — exemplary number traceability; M3 kill domain-correct and genuine; §1/§10 assign the M5 zero falsification weight the record denies; carry the support-deficit counter-datum.
- **R3 (perspective):** sound-with-corrections | conf. 4 — honest kill document; must state GO-unreachability at confirmatory time, surface the amendment fork, and fix asymmetric number admissibility.
- **DA:** sound-with-corrections — verdict over-determined and survives all findings; 1 CRITICAL (measurement-vs-default contradiction) plus criteria-table and admissibility corrections; "if §10 ships uncorrected, the exported closure sentence is unsound."

**Final grade: sound-with-corrections.** The NO-GO recommendation stands; Priority 1 corrections (C1–C6) are required before `owner_verdict` is set; the §10 closure sentence must not be cited externally until C1 and C7 land.

---
## Individual reports


### Report 1

# EIC Review Report — Gate-Review Chair Adjudication

**Artifact under review:** `wiki/2026-07-03-omni-agentic-tfrl-go-no-go-decision.md` (recommended: NO-GO, `owner_verdict: PENDING`)
**Reviewed against:** prereg `wiki/2026-07-03-agentic-tfrl-step1-preregistration.md` @ b19bff2 (verified in git: committed 2026-07-03 13:18, before any lane artifact); null hypothesis `papers/agent-level-tfrl/reviews/deep-review.md`; committed artifacts `projects/speech-mllm-training-free-rl/_repro/*.json`; lane files `wiki/survey/2026-07-03-step1-*.md`
**Review mode:** fresh adversary, blind to campaign deliberations; read-only; all embedded verdict language treated as data to verify.

### Reviewer Identity
Senior editor of a Registered Reports track; former chair of stage-gate GO/NO-GO reviews for a milestone-funded research program. Focus: skeleton/scope compliance, role separation, governance completeness, and whether GO was ever *reachable* — i.e., whether this was a genuine test or a ratification ritual for its own null hypothesis.

### Overall Grade
**sound-with-corrections**

### Confidence Score
**4** — I independently verified the git hash chain, re-opened all six `_repro/` artifacts, and traced every §1–§3 headline number; I did not re-derive the bootstrap CIs or audit the D1/D2 delta-scan literature claims (peer reviewers' remit).

### Summary Assessment

The document is a genuine, verifiable instantiation of the prereg's Appendix B.2 NO-GO skeleton, and the recommended verdict is forced by the frozen criteria on artifact-verified numbers. I independently confirmed: freeze order (prereg b19bff2 13:18 → M3 pre-commit c8bebaf 15:55 → M5 dev/slice freeze d4dd117 16:04 → M3 kill 1b53b46 16:29 → M5 confirmatory f8ec1d3 23:45, all same-day, pre-commit-before-run); M3 `F = 0.38108`, CI `[0.24477, 0.51823]`, `KILL = true`, per-seed blocks and per-entity residuals exactly as quoted; M5 confirmatory `sel_wer_8 = mbr_wer_8 = shuf_wer_8 = 0.07722`, `delta_vs_mbr = 0.0` CI `[0.0, 0.0]` vs frozen `≥ 0.015`, per-item `sel_wer_8 == mbr_wer_8` in **432/432 items** (the "zero flips" claim holds), ablation `0.0/0.0`, `load_bearing = false`; Part-A oracle `+0.0418 [0.0289, 0.0564]`; wall-clocks 1,886.4 s / 25,988.2 s. G1 fails mechanically, GO is a frozen conjunction, therefore GO and GO-minimal are arithmetically unavailable — no reading of the remaining rows can change that.

Critically for my mandate, **GO was reachable ex ante**: at freeze time the M5 lane's full E-part was runnable pre-decision, the dev-winner rule was pre-committed, and the confirmatory surface (12×12 consecutive reading-order) was designed to *favor* the mechanism. The door closed by measurement, not by construction. The corrections below concern how three criteria rows are labeled and evidenced, a quiet relaxation of the prereg's own number-traceability standard, and small compiler-authored argumentation that contradicts §0's role-separation claim. None flips the verdict; several must be fixed before the owner signs.

### Strengths

1. **Decisive numbers are fully artifact-traceable and honest.** Every load-bearing figure in §§1–3 (F, CIs, exact ties, zero flips, oracle deltas, elapsed times) reproduces from the committed JSONs; the hash chain shows target-set and dev-winner freezes committed *before* the corresponding GPU runs, exactly as claimed.
2. **The steelman-GO (§6) is genuinely the strongest assemblable case, rebutted by criterion.** It includes the structural-null diagnosis (≤3/144 actionable dev positions, honestly carried into the verdict rows via `m5_selector_dev.json`'s `structural_null_diagnostic`) and the constructor's V4 evidence, and it is answered by naming which frozen conjunct each move misses. The compiler even *corrected* the panel steelman's mis-attribution of "P-A trigger NOT met" (an artifact-verdict claim there) to its true source, the M5 lane file — a small but telling verification signal.
3. **Adverse-to-narrative facts are preserved, not buried:** the Part-A memo's A2 "open-and-promising" pillar is reported as having since collapsed (§1); the panel's "zero information ex ante" ruling on the frozen selector is carried in the very rows it embarrasses (§2 G2, §7 U2); the M3 residual (SHARDURIS 0.0, CONFECTIONARY 0.0104) is recorded with an explicit not-a-rescue marker.
4. **Skeleton and governance completeness:** B.2 items 1–6 all instantiated; r1–r3 restated character-for-character; owner gate preserved (§11); the (i)/(ii) split maintained — Part-A's RATIONAL-AND-CONTINUING is explicitly denied GO-weight for question (ii).
5. **Provenance failures are disclosed rather than laundered:** §0 itself reports the phantom B3/B4/B5 strikes and the panel-governs precedence rule.

### Itemized Findings

**CRITICAL** — none.

**MAJOR-1 (criteria table, G2 row): internal contradiction with the document's own precedence rule.** §0 states "Where a lane recommendation conflicts with a panel ruling (see U2), the panel ruling governs." The panel's binding ruling is U2 STANDS, and frozen G2 reads "No named decision → U2 stands → no GO." Mechanically, G2 = FAIL. The row instead leads with "SATISFIED-IN-FORM / MOOT," resting on the post-panel B4 memo — the same post-outcome material the meta-chair struck at panel time as phantom. The §7 U2 "record note" repeats the pattern (post-panel B4 used to soften a ruling the note concedes cannot be re-litigated). Direction favors GO and the verdict is unaffected, but a table claiming mechanical application may not let a post-outcome lane memo out-rank a governing panel ruling. **Fix:** rescore G2 as FAIL per the panel ruling; demote B4's form-satisfaction to an explicitly non-binding record note.

**MAJOR-2 (checklist e): the frozen traceability standard is quietly relaxed, and NO-GO-supporting numbers live only in lane memos.** Prereg §4 (frozen): "Every number lands in a committed `_repro/` artifact with a `reproduce:` line." §0 substitutes "a committed `_repro/` artifact **or a campaign lane file**" — a weakening of frozen text, applied without an owner-signed amendment. Numbers tracing only to lane memos: the habitat census 0/49; the 92%-minority-best residual-headroom decomposition; median flip-λ 60.5 (the basis of the "pre-proven inert" U2 ruling); V4 +0.00611/+0.00321; the per-seed Part-A slices +0.0506/+0.0480/+0.0270 (verified absent from `asr_bon_llamacpp_snr5.json`, present only in the Part-A memo); B4/B5 person-week costings. These are not decorative — 0/49, 92%, and λ 60.5 underwrite steelman points 5 and 7, which are the *substantive* core of closure (empty habitat), beyond the merely frozen-contractual core (G1 FAIL). All appear derivable from committed per-item data, so this is repairable. **Fix:** commit the census/inertness/per-seed analyses as `_repro/` artifacts with reproduce lines, or excise those numbers from load-bearing positions.

**MAJOR-3 (criteria table, NO-GO clause (b) row): "MET" is reached via two interpretive bridges, one undisclosed.** Frozen clause (b): "all mechanism lanes hit their kill thresholds AND the M5 ablation shows accumulation is not load-bearing." Bridge (i), disclosed: unexecuted lanes (M2/M4/M1) counted via the inconclusive→NO-GO default. Bridge (ii), *not* disclosed: M5's frozen spec defines a PASS threshold and a dispositive ablation — no kill threshold — so "M5 no-pass 0.0 vs ≥0.015" is not literally a lane "hitting its kill threshold." The verdict itself is safe: the standalone frozen rule "**Inconclusive = NO-GO**" (stated twice in the prereg) plus G1's arithmetic failure forces NO-GO regardless of clause (b). **Fix:** relabel the row "not strictly met; NO-GO discharged by the frozen inconclusive-default + GO-impossibility," and correct §11's Decision-Log line "lanes M3/M5 killed" (M3 was killed; M5 did not pass — §3's own wording is accurate, the log line is not).

**MINOR-4 (post-outcome evidence in criteria rows):** G2/G3/G4 rows cite B3/B4/B5 memos authored in this run, after all outcomes were known. Disclosed in §0, non-decisive given G1 (and G4 loads toward GO), and P-B's disposition is robust to any G3 reading (the theorem ingredient is dead on every reading, so "fails *only* on corpus" can never obtain). But B3's "three-ingredient substantive test" is a lane invention: the frozen G3 text ("a named on-disk / pseudo-session / TTS path") is literally satisfiable, and the FAIL verdict is licensed only through safeguard 1's ambiguity rule on "concretely satisfied." The row cites safeguard 1 — correct — but should present the substantive test as a safeguard-1 resolution, not as frozen machinery.

**MINOR-5 (role separation vs §0's claim):** §0 asserts the compiler "authored no lane defense and no criteria arguments," yet §1 contains compiler-authored argumentation: "reaffirmed by fresh pre-registered measurement, not by default" (true for the M3 kill and the confirmatory's collateral findings, but in tension with the panel's own ruling that the frozen selector arm carried "zero information ex ante" — the sentence needs that caveat), and the "category error" sentence, which argues rather than compiles. Small, disclosed-adjacent, direction-consistent with the panel — but a document whose authority rests on mechanical compilation should not editorialize in its verdict summary.

**MINOR-6 (owner-gate menu completeness):** §5.17 ("Nothing runnable inside the timebox can change the answer") is over-strong. Prereg §4 permits multiple fresh confirmatory slices ("slices, each touched once"), so an owner-signed amendment freezing a non-inert selector on a *new* fresh slice is frozen-legal within the remaining 9 days; what blocks it is safeguard 5 (owner sign-off) plus the constructor's own sub-threshold prediction and the empty-habitat censuses. §6 does contain this material, but folded into a rebuttal. The decision was taken on day 1 of 10; the owner ruling on PENDING should see the amendment option stated as a rejected-with-reasons alternative, not only as a defeated steelman.

**MINOR-7 (ordering-rule letter violation, unreported):** frozen §5 ordering is "M3 → M5." Commits show M5's dev pilot was frozen at 16:04 (d4dd117), inside M3's Phase-0 execution window (kill committed 16:29). Immaterial (M5 dev was 5.1 s of CPU re-scoring of already-committed pools; no informational leakage), but §3's "ran first / ran second" narrative is accurate only for the binding confirmatory, and a document staking everything on procedural fidelity should report its own wrinkle.

**MINOR-8 (citable closure sentence, §10):** "the frozen model already emits the 'rare' entities a cross-session lexicon would supply" is true pooled (F = 0.38108) but false for 3/13 entities (SHARDURIS 0.0, CONFECTIONARY 0.0104, FARRINDER 0.0156) — a residual §3 honestly records but the externally citable sentence omits. Add the minority-residual qualifier; this is the one sentence outsiders will quote.

**MINOR-9 (provenance bookkeeping):** front-matter `campaign_runs` omits the panel's workflow ID (`wf_f6d37987-df5` per the panel file header).

### Detailed Comments

**Was GO reachable (the ratification-ritual test)?** Yes, at freeze time — and this is the document's strongest defense against the charge that a NO-GO written under a NO-GO null hypothesis was pre-wired. The frozen structure gave GO a live path through M5's pre-decision E-part; the dev grid could have shown signal; the confirmatory surface was deliberately tilted *toward* the mechanism. Two honest weaknesses in the reachability story remain: (i) by prereg design, M3/M2/M4's GO-supporting E-parts run post-GO, so within this campaign only M5 could ever have discharged G1 — a prereg design oddity the decision doc inherits rather than creates; (ii) by confirmatory time the frozen selector was known-inert (λ 60.5 vs 0.05), so the M5 selector *arm* was a foregone conclusion — the panel says so, and the doc carries it. The informative content of the 7.2-hour confirmatory was the habitat, the MBR/greedy/oracle arms, and the position-bin trend, all of which measured null/empty. The record therefore supports a genuine test whose last measurement was low-information on one arm — not a rigged one.

**Skeleton and scope:** B.2 fully instantiated; additions (§2 table, §4 panel record, §5 steelman-NO-GO disposition) are required by §6.7/§7 machinery. Question-(i)/(ii) separation is maintained; the Part-A verdict is fenced off from (ii) explicitly. Pivot dispositions follow frozen triggers; P-D's adoption as "a success" is frozen-licensed verbatim; r1–r3 verified verbatim.

**Governance completeness:** owner gate intact (§11); Decision-Log entry faithful to the body except the "M3/M5 killed" compression (Finding MAJOR-3); the Chinese summary (§12) is consistent with the body.

### Questions for the Authors (before owner sign-off)

1. Rescore G2, or explain how "SATISFIED-IN-FORM" survives the §0 precedence rule given U2 STANDS.
2. Will the lane-memo-only numbers (0/49, 92%, λ 60.5, V4 deltas, per-seed slices) be promoted to committed `_repro/` artifacts per frozen §4, and §0's weakened traceability sentence retracted?
3. Will the owner-gate presentation list the frozen-legal amendment path (new fresh slice + owner-signed non-inert selector) as an explicitly rejected alternative with the empty-habitat evidence as the reason?
4. Confirm the clause-(b) row will be relabeled to rest on the frozen inconclusive-default rather than a kill-threshold reading M5's spec does not contain.

### Recommendation to Peer Reviewers

- **Methodology (#2):** the two bridges in NO-GO clause (b) and whether a degenerate CI [0,0] from a pre-proven-inert instrument satisfies prereg §4's statistical standard, or is a measurement of the instrument rather than the mechanism.
- **Domain (#3):** re-derive the 0/49 and 92% censuses from the committed per-item data (they are load-bearing and currently memo-only), and assess whether pooled entity-match F validly falsifies the M3 premise given the 3/13 unsupported-entity residual.
- **Perspective (#4):** whether §10 closes question (ii) *as posed* or two instantiations of it — the closure sentence's honesty turns on that distinction.
- **Devil's Advocate (#5):** the B4/U2 record-note pattern (post-outcome memo softening a governing ruling) is the one place I found the compiled record arguing with its own panel; pull that thread.

**Bottom line:** the NO-GO recommendation is correct under the frozen contract and would survive editorial scrutiny after corrections; the verdict is artifact-forced, the steelman genuine, the closure frozen-licensed. Grade: **sound-with-corrections** — MAJOR-1 through MAJOR-3 should be repaired before `owner_verdict` is set.

### Report 2

All verification is complete. Here is my independent review report.

---

# Methodology Review Report (Peer Reviewer 1 — Pre-registration Statistics / Sequential Kill Criteria)

**Reviewer identity:** Biostatistician (DSMB / pre-registered stopping-rule background) now in ML evaluation methodology; brief = frozen criteria applied as written, statistical soundness of the two kills, freeze/dev-test hygiene, artifact traceability. Fresh-adversary: I re-derived every load-bearing number from the committed JSONs and the git history myself; I did not consult any panel deliberation beyond the files named in my brief.

**Review target:** `wiki/2026-07-03-omni-agentic-tfrl-go-no-go-decision.md` (recommended NO-GO), against the prereg frozen at commit `b19bff2`.

## Overall Grade

**sound-with-corrections**

The NO-GO verdict on question (ii) is mechanically reachable from the frozen text using only artifact-verified numbers: G1 fails (M3 killed by its pre-registered point-threshold rule; M5 failed its pre-registered PASS threshold), GO requires ALL of G1–G4, GO-minimal requires an M5 PASS that did not occur, no pivot trigger fires as frozen, and the frozen verdict-level default ("Inconclusive = NO-GO"; the 7/02 verdict "stands unless overturned by NEW information") closes the remainder. Every headline number in §§1–3 traces to a committed `_repro/` artifact, either as a printed field or as an exact derivation from committed per-item data (I recomputed them). However, the criteria-scoring table contains two rows where a frozen clause was read leniently after data arrived, the verdict layer over-credits an experiment the record itself proves carried ~zero information ex ante, and a set of load-bearing supporting numbers violates the prereg's own §4 artifact rule. None of these corrections flips the verdict; all of them are required before this document is a clean instance of "criteria applied as written."

## Verification Log (what I checked and confirmed)

- **Freeze integrity:** `git diff b19bff2..HEAD` on the prereg shows exactly one change — `owner_ack: PENDING` → ACKED, criteria unchanged. ✔
- **Freeze-order chain:** `c8bebaf` (07-03 15:55, M3 target set pre-committed before any GPU sample) → M3 verdict `1b53b46` (16:29; artifact `elapsed_s=1886.4` consistent) → `d4dd117` (16:04, dev winner + confirmatory slice frozen before confirmatory generation) → verdict `f8ec1d3` (23:45; `elapsed_s=25988.2` ⇒ generation started ≈16:32, after the freeze). ✔
- **M3 numbers:** F=0.38108 (439/1152), kill 0.01, `KILL=true` computed in committed code as a point-threshold rule (`kill = F > KILL_F`), CI [0.24477, 0.51823], seed blocks 0.36111/0.40278/0.38194/0.37847, greedy-contains 0.3889, PILESER 1.0 / SHARDURIS 0.0 / CONFECTIONARY 0.0104 / FARRINDER 0.0156 — all in `_repro/m3_phase0_zero_support.json`. ✔
- **M5 confirmatory:** I recomputed from the 432 per-item rows: 0 items with `sel_wer_8 ≠ mbr_wer_8`, 0 with `shuf_wer_8 ≠ mbr_wer_8`; means sel=mbr=shuf=0.07722, greedy 0.0772, oracle 0.05342 (+0.0238); delta 0.0 CI [0.0, 0.0] vs 0.015; red_vs_greedy −0.00003 [−0.00358, +0.00369]; realized_fraction −0.0008; ablation 0/0, `load_bearing_le_50pct=false`; both PASS readings computed and agree; Goodhart guard computed, no-fail; slice seed 20260703 with `excluded_dev_spent=144`, `excluded_m3_phase0=36` recorded in-artifact. ✔
- **A1 numbers:** greedy 0.1183 → oracle@8 0.0765, +0.0418 [0.0289, 0.0564]; the three per-seed deltas +0.0506/+0.0480/+0.0270 are not printed fields but reproduce **exactly** from the committed `per_utt` rows (I computed 0.0506/0.0480/0.0270). ✔
- **Statistical standard:** ≥3 seeds everywhere stochastic (M3: 4 blocks; M5: 3 gen seeds; A1: 3 seeds) ✔; paired cluster bootstrap by utterance, 10,000 draws, seed 42 ✔; Holm moot on the dev grid (14 configs, all deltas exactly 0.0, no positive claim made) ✔.
- **Re-open conditions:** §9's r1–r3 are character-identical to the frozen §2 text. ✔
- **Ledger:** §7 dispositions match the frozen statuses (8P/7U standing, S1/S3/S5 contingent, S2/S6 resolved, S4/S7 standing); nothing silently flipped toward either side. ✔
- **V4 dismissal:** the V4 evidence (+0.00611 [−0.00194, +0.01598] LOO; +0.00321 [−0.00399, +0.01225] streaming) lives on the M3 Phase-0 pools used for dev iteration; both CIs cross zero; prereg §4 ("dev iterations on dev slices, confirmatory on a fresh slice touched once") and §6.11 make it inadmissible as confirmatory; V4 was not the frozen dev winner, so running it requires an amendment, which the freeze-anchor paragraph and safeguard 5 reserve to owner sign-off. The dismissal follows the frozen text as written. ✔
- **Skeleton:** Appendix B.2 instantiated item-by-item (§3 lanes, §7 ledger, §6 steelman-GO with named missing criteria, §8 pivots, §9 verbatim re-opens, §10 closure sentence). ✔

## Itemized Findings

### F1 — MAJOR (criteria-as-written): NO-GO clause (b) scored "MET" via a double bridge the frozen clause does not contain
Frozen text (§2): NO-GO if "all mechanism lanes hit their kill thresholds AND the M5 ablation shows accumulation is not load-bearing." Facts: (i) M5 has **no pre-registered kill threshold** — prereg §5 gives M5 only a PASS threshold (≥0.015, CI-LB>0); its outcome is a *failed PASS*, not a kill-threshold hit. Only M3 (>1%) and M2 (CI-UB<+0.01, post-GO) have kill thresholds. (ii) M2/M4/M1 never ran, so they did not "hit" anything; the inconclusive→NO-GO default is frozen at the **verdict** level (preamble, §2 NO-GO block, safeguard 1), not as a substitution rule inside clause (b)'s conjunct. The row's "MET — via executed-lane kills + the inconclusive→NO-GO default … (strict-all-lanes reading not claimed)" discloses the bridge but still stamps MET on a conjunctive clause whose conjuncts are unmet. The same conflation propagates into the permanent §11 Decision-Log line ("lanes M3/M5 killed at … and delta_vs_mbr=0.0"). **Verdict impact: none** — NO-GO follows without clause (b), from G1-FAIL + the GO conjunction + the frozen verdict-level default. **Correction:** re-score the row "NOT STRICTLY MET; NO-GO follows from the frozen default (null hypothesis + inconclusive=NO-GO + GO/GO-minimal failure)," and reword §11 to "M3 killed; M5 failed its pre-registered PASS threshold."

### F2 — MAJOR (criteria-as-written): G3 scored FAIL through an unfrozen instrument that inverts the frozen arithmetic
Frozen G3: "At least 2 of the paper's three ingredients concretely satisfied," with the operator declared **"already resolved — S2" in the frozen text itself**, and corpus satisfiable by "a **named** on-disk / **pseudo-session** / TTS path." Pseudo-session paths were named, built, and exercised (`m3_phase0_selection.json`, `m5_confirmatory_slice_ids.json`). On the literal frozen reading G3 = 2/3 = **PASS**. The row instead scores "FAIL (substantive)" via B3's "three-ingredient substantive test" (every task family must pass all three, with sub-tests a/b/c) — a lane-invented, post-outcome tightening found nowhere in the frozen text. A post-hoc tightening *against* GO is still a criteria violation. The legitimate frozen route to the same place exists — "concretely satisfied" is ambiguous for a path that measured hollow, and safeguard 1 resolves ambiguity against GO — and the row half-gestures at it ("lenient 2/3 reading cannot convert and is moot given G1"). **Verdict impact: none** (GO dies on G1 either way; P-B stays untriggered under either reading — literal-PASS is not "fails only on corpus," and the doc's reading fails on two ingredients). **Correction:** score G3 as "literal 2/3 PASS; substantive satisfaction ambiguous → resolved against GO per safeguard 1; moot given G1," demoting the B3 test to commentary.

### F3 — MAJOR (statistical validity / verdict-layer labeling): the M5 confirmatory zero is an inert-instrument null presented in the citable layer as a mechanism kill
The record itself proves the frozen V1|0.05 selector could not respond: the λ census (median required λ = 60.5, range 4.4–112; zero flips at any λ ≤ 0.8) predated the confirmatory, the lane committed "SHARP PREDICTION 1: exact tie, zero flips" at 17:21 — before the 23:45 verdict — and the panel's own C3 ruling reads "exact tie predicted then confirmed — **zero information ex ante**." A degenerate CI [0.0, 0.0] over 432 items is the signature of an instrument with no variance, not of a precisely measured null effect; prereg §4's paired-bootstrap standard presumes an instrument that can vary and never anticipated certification-by-inert-instrument. The body is honest about this (§3 structural-null diagnostic, §5.4, §5.7, U2 row), but three verdict-layer statements over-claim: §1's "reaffirmed by fresh pre-registered measurement, not by default" (true for M3; over-credits M5), §10's citable closure sentence (reports the exact zero and zero flips with no inertness caveat — a downstream citer will read a tested-and-null mechanism where the record shows an untestable-as-frozen instrument), and §11's "M5 killed." Under the frozen contract the **verdict is right regardless** — an instrument-null is "inconclusive," and inconclusive = NO-GO; M3's kill is genuinely informative and can carry the mechanical-falsification weight alone. **Correction:** the closure sentence must say "selector accumulation **as instantiated by the frozen selector** returned an exact zero" or carry the structural-null caveat explicitly; keep the falsification language attached to M3 only.

### F4 — MAJOR (artifact traceability, prereg §4 as written): load-bearing supporting numbers never landed in a committed `_repro/` artifact
Frozen §4: "**Every number** lands in a committed `_repro/` artifact with a `reproduce:` line." The following numbers exist only in lane memos: median flip-λ 60.5 (range 4.4–112); V4 +0.00611 [−0.00194, +0.01598] and +0.00321 [−0.00399, +0.01225] with shuffled −0.00039/0.0000; the 0/49 residual-headroom census; the 92% anti-consensus mass decomposition; 54.9% in-pool / 79/144 / 17/144. §0 quietly softens the frozen standard to "a committed `_repro/` artifact **or a campaign lane file**." These are not decorative: λ 60.5 discharges the U2 panel ruling ("pre-proven inert"), 0/49 and 92% carry steelman §5.7, and the V4 CIs carry the §5.5/§6 dismissal. All point toward NO-GO, but a §4 breach is a §4 breach, and every one of these is a cheap CPU-only re-analysis of already-committed pools. (Contrast: ≤3/144 **is** in `m5_selector_dev.json`, honestly labeled UPPER_BOUND and "computed post-grid"; the "zero flips" claim is derivable — I verified 0/432 per-item inequalities — though no flips field exists.) **Correction:** emit one committed re-analysis artifact with a `reproduce:` line covering the λ census, V4 dev arms, and the two headroom censuses; or annotate those rows as memo-grade in the table.

### F5 — MINOR: G2 scored with an invented category, on post-outcome evidence
"SATISFIED-IN-FORM / MOOT" is not a prereg category; frozen G2 is binary, and its frozen operative clause ("No named decision → U2 stands → no GO") makes the panel's U2-stands ruling dispositive by itself. Additionally, the row's cited evidence (B4 memo) was committed together with the decision document (`eec14f6`, 07-04 00:42), after all outcomes were known. Verdict-irrelevant given G1; re-score on the frozen binary with the form/substance discussion as commentary.

### F6 — MINOR: P-C's "NOT TRIGGERED" imports a proof standard the frozen T-part definition does not contain
Frozen G1 T-part requires "a formal **statement** with explicitly stated assumptions" that is non-tautological and spread-lens-consistent — not a proof, and no Lean requirement. The P-C row's basis ("all 'STATED, not proved,' zero Lean lines") therefore tightens the frozen test; note also that safeguard 1's ambiguity rule is worded against **GO**, and pivots are frozen "successes," so ambiguity-against-pivot is not automatic. Frozen cover does exist — the panel ruled C1 stands and panel adjudication is frozen procedure (safeguards 3/10), and M3's T-part premise was empirically falsified — so the disposition survives, but the row should cite the panel ruling as the operative basis rather than the Lean-lines count.

### F7 — MINOR: M3 bootstrap clustered at the wrong level; immaterial to the kill
The committed script resamples the 36 utterances, but utterances sharing an entity (3 per entity, 13 entities, per-entity fractions spanning 0.0–1.0) are strongly correlated, so the utterance-clustered CI [0.245, 0.518] is anti-conservative; entity-level clustering would widen it. Immaterial: the frozen kill rule is a point threshold on F (mechanically applied in code), and any defensible clustering leaves the CI lower bound over an order of magnitude above 0.01. The script labels the CI "descriptive"; the decision doc cites it without that label — carry the label.

### F8 — MINOR: tie-break bookkeeping is internally inconsistent across records
The dev artifact records `tie_break_applied: false` while the grid was a 14-way exact tie at 0.0 and the M5 lane file says "Winner by frozen tie-break: V1|0.05|none." The doc's harmonizing parenthetical ("the top-ranked config already was the simplest") papers over the inconsistency. No verdict impact — the simplicity ordering (V1>V3>V2) is pre-committed in the artifact's rule string and any in-grid winner was equally inert — but the artifact field and the memo cannot both be right; say which.

### F9 — MINOR: the confirmatory surface was designed after the dev null was known
The dev artifact (16:01) already names the 12×12 consecutive reading-order slice as "the designed surface"; the design was frozen at 16:04 (`d4dd117`), after the dev all-zero grid, before generation (verified by wall-clock). The prereg pinned only "fresh slice touched once," so no frozen text was violated, and the researcher degree of freedom cuts **pro-GO** (mechanism-favoring), i.e., conservative for a NO-GO — but the §5.4 framing "designed to favor the mechanism" should state explicitly that the surface was chosen in response to the dev structural null.

## What survives cleanly

The freeze-hygiene chain is exemplary and fully verifiable from git alone (selection sets pre-committed before GPU; slice manifest frozen before generation; a falsifiable exact-tie prediction committed hours before the verdict artifact; prereg untouched post-freeze except the owner ack). Dev/test separation was honored with exclusions recorded inside the confirmatory artifact itself. The M3 kill is statistically unimpeachable at any clustering choice, 38× over a threshold frozen before the first sample. Both PASS-threshold readings were computed and agree; the Goodhart guard was computed, not waived. The V4 dismissal, the P-A/P-B non-triggers, the P-D adoption, and the verbatim r1–r3 restatement all follow the frozen text as written. The verdict does not depend on any of the flagged rows.

## Bottom line

The frozen contract delivers NO-GO on question (ii) without the two lenient readings the scoring table indulges in, and the document weakens itself by taking them. Required corrections: (1) re-score clause (b) and reword the Decision-Log entry (F1); (2) re-score G3 on the frozen arithmetic with the safeguard-1 route (F2); (3) add the inert-instrument caveat to the §10 closure sentence and drop "killed" for M5 (F3); (4) commit the memo-grade numbers as a reproducible `_repro/` re-analysis artifact (F4). With those applied, the document is a faithful mechanical application of the pre-registration.

**Grade: sound-with-corrections** (0 CRITICAL, 4 MAJOR, 5 MINOR). Confidence: 5/5 on artifact-level verification; 4/5 on frozen-text interpretation calls.

### Report 3

All evidence is audited. Here is my independent review report.

---

# Domain Review Report (Peer Reviewer 2 — Speech/ASR Decoding & Evaluation)

### Reviewer Identity
Senior ASR researcher (15 y in decoding and system combination: MBR/consensus decoding, ROVER-lineage fusion, contextual biasing, long-form conditioning); audits WER claims to the scoring script; fresh-adversary, blind to campaign deliberations; judged only from the frozen prereg (b19bff2), the 2026-07-02 deep-review, the six committed `_repro/*.json` artifacts, and the ten `wiki/survey/2026-07-03-step1-*.md` lane files.

### Overall Grade
**sound-with-corrections**

The NO-GO verdict follows mechanically from the frozen criteria on artifact-verified numbers: M3's kill is a genuine, informative measurement honoring the frozen rule; M5 fails its frozen threshold; the inconclusive→NO-GO default disposes of M2/M4/M1; GO-minimal fails on the artifact's own fields. No finding below overturns the verdict. The corrections concern (i) the evidential weight the document's headline sentences assign to the M5 zero, (ii) an over-broad M3 generalization in the citable closure sentence, (iii) an inconsistent evidentiary standard for lane-memo-only numbers, and (iv) steelman-GO completeness.

### Confidence Score
4/5 (I re-opened every committed artifact, recomputed the headline aggregates and one load-bearing uncommitted number, and diffed the git freeze chain; I did not re-run any generation or re-derive the λ-flip census.)

### Summary Assessment
Number-by-number, this is one of the most traceable decision documents I have audited. Every figure I checked against committed artifacts is exact: M3 F = 0.38108, CI [0.24477, 0.51823], 439/1152, four seed blocks, greedy-contains 0.3889, per-entity spread (PILESER 1.0 / SHARDURIS 0.0 / CONFECTIONARY 0.0104), KILL = true (`m3_phase0_zero_support.json`); M5 delta 0.0, CI [0.0, 0.0], sel = mbr = shuf = 0.07722, greedy 0.0772 → oracle 0.05342 (+0.0238, verified 0.02378), red_vs_greedy −0.00003 CI [−0.00358, +0.00369], realized_fraction −0.0008, ablation 0/0/null/false, position bins all 0, seed 20260703, exclusions 144 + 36, n = 432 (`m5_selector_confirmatory.json`); BoN greedy 0.1183 → oracle@8 0.0765, +0.0418 [0.0289, 0.0564]; the per-seed slices +0.0506/+0.0480/+0.0270 I recomputed exactly from `per_utt` (seeds 42/7/123); wall-clocks 1,886.4 s and 25,988.2 s; dev grid 14 configs all-zero, `tie_break_applied: false`, structural-null ≤3/144 committed in the dev artifact. Freeze hygiene verified in git: c8bebaf (15:55) precedes 1b53b46 (16:29); d4dd117 (16:04) precedes f8ec1d3 (23:45). The document's weaknesses are interpretive, concentrated in §1's "reaffirmed by fresh measurement" and §10's citable closure sentence, which assign the M5 exact zero empirical falsification weight the campaign's own record denies it.

### Strengths
1. **Exemplary artifact traceability of verdict-bearing numbers.** All kill/threshold numbers in §2–§3 trace to committed artifacts and are exact; the freeze-before-run commit chain is real and correctly ordered.
2. **The M3 kill is domain-correct and genuinely informative.** "Corpus rarity ≠ model-OOV" is a real finding: train-960 frequency ≤5 entities are emitted by the 30B in 38% of context-free samples. Corpus-frequency screening is a known-poor OOV proxy for web-scale-pretrained models, and the Phase-0 instrument (N=32 context-free sampling, pooled entity-match vs a frozen 1% kill) is a fair falsifier of the frozen premise "the lexicon does not exist within a single session." The honest per-entity residual is carried.
3. **Honest outcome-symmetric correction against Part-A optimism.** §1 explicitly updates the Part-A memo's "open-and-promising" A2 pillar after the confirmatory zero, and carries the memo's honest floor ("every deployable selector measured to date is null") — a correction that cuts against the document's own surviving direction.
4. **The anti-consensus decomposition reproduces.** I independently recomputed the refuter's key uncommitted claim from the committed C1 artifact: 49 residual-headroom utterances exact; ~94% of residual-headroom mass on ≤2-of-8 minority-best pools (claimed 92%; difference attributable to my cruder normalizer). The structural claim that the post-MBR gap is anti-consensus for majority-seeking label-free signals is real.
5. **Strong ASR-literature grounding in the lane refuters** (ROVER/Fiscus 1997, Goel & Byrne 2000 MBR, Kuhn & De Mori 1990 cache LM, Aleksic 2015 / Le 2021 biasing, kNN-LM, e-WER/NoRefER QE), correctly deployed for the occupied-cell analysis the doc cites in §5.11.

### Findings (itemized)

**F1 — MAJOR (interpretation): the M5 exact zero is presented in §1 and §10 as empirical mechanism evidence, while the record establishes an inert instrument measured on an unmeasured habitat.**
The campaign's own constructor pre-committed (M5 dossier commit f0c2486, 17:21, six hours *before* verdict commit f8ec1d3, 23:45) SHARP PREDICTION 1: the frozen V1|0.05 arm ties MBR exactly, zero flips, because the median λ required to flip a single pick is 60.5 vs frozen 0.05 — three orders of magnitude short. The panel's binding C3 ruling says so verbatim: "exact tie predicted then confirmed — zero information ex ante." A degenerate CI [0.0, 0.0] over 432 items is the statistical signature of an instrument that cannot vary, not of a sampled null. Additionally, the confirmatory artifact contains no habitat census for the designed 12×12 surface (the ≤3/144 actionable-positions diagnostic exists only for the dev pool in `m5_selector_dev.json`; `mem_items_at_pick` > 0 in 285/432 items records memory presence, not pool-overlap actionability) — so "exact zero on a surface designed to favor the mechanism" (§5.4) is design intent, not a measured property; zero flips cannot discriminate empty-habitat from inert-instrument, and the pre-run λ census says inert-instrument. §2/§5.5 handle this honestly under the frozen contract (V4 dev-spent, amendment requires owner sign-off — correct), but §1's "reaffirmed by fresh pre-registered measurement, not by default" is at most half-true (true for M3, false for M5 per the panel's own ruling), and §10's citable sentence — "cross-session selector accumulation returned an exact zero on its designed confirmatory surface" — converts a *procedural* closure (frozen instantiation failed + slice spent + inconclusive→NO-GO) into an *empirical*-sounding falsification of the mechanism class. **Correction:** scope §10 to "the pre-registered selector instantiation (V1|0.05)" and state the closure basis as the frozen procedure; align §1's reaffirmation claim with the C3 ruling. Also note the collateral context a domain reader needs: the fresh slice is markedly easier (greedy 0.0772 vs 0.1183 dev) with MBR ≡ greedy — a low-diversity, degenerate-pool surface.

**F2 — MAJOR (interpretation): §10's M3 generalization omits the campaign's own committed-pool counter-datum.**
The closure sentence reads "the frozen model already emits the 'rare' entities a cross-session lexicon would supply." That is true of the 13 corpus-rare screened entities (pooled), and the kill is mechanically valid. But the M3 lane's constructor analysis of the *committed* C1 pools quantifies a support-deficit floor: ~75.6% [67.2, 84.0] of the entire residual oracle headroom at N=8/SNR5 is reference tokens with zero support across all 9 draws (MURDOCH, FARRINDER, PLATTERBAFF, ORGANISER among them) — i.e., on deployment-like pools, most of the *remaining* headroom is reachable only by moving q0. The B3 memo itself records the re-open-adjacent observation that "a future true-OOV personalization pre-registration would need model-level OOV screening, not corpus-frequency screening." Neither the 75.6% figure nor the B3 observation appears anywhere in the decision doc; §3's residual note ("genuinely unsupported entities... are the minority") is computed on the 13-entity list, not on residual-headroom mass — two different bases, and only the closure-friendly one is quoted. What Phase-0 falsified is the corpus-rarity *screening premise*, not the target mass of ceiling-movement. **Correction:** carry the B3 observation (and the support-deficit floor, suitably flagged as lane-memo evidence) into §3 or §9's r3 context, and narrow §10 accordingly. Verdict-safe: safeguard 8 stops the lane, and Phase-1 was pre-registered post-GO regardless.

**F3 — MAJOR (traceability, checklist e): load-bearing interpretive numbers are lane-memo/scratchpad-only, under a standard the panel itself enforced against a lane.**
Prereg §4 (frozen): "Every number lands in a committed `_repro/` artifact with a `reproduce:` line." The doc's §0 quietly weakens this to "a committed `_repro/` artifact **or a campaign lane file**." Numbers with no committed artifact that are load-bearing in the doc: median λ 60.5 (range 4.4–112) — central to the U2 ruling and to interpreting the M5 zero; V4 +0.00611 LOO / +0.00321 streaming (§5.5, §6); 0/49 same-speaker rare-token census (§5.7); 92% minority-best mass (§5.7); p_pool 0.549, mode-at-truth 6/13. All derive from scratchpad scripts (`m5_constructor_analysis.py` et al., per the lane's own dataset_on_disk line). Meanwhile chair C2 struck M4's Tier-1 numbers as "scratchpad-only and inadmissible under prereg §4." The asymmetry is directionally consistent with safeguard 1 (every such use is anti-GO), but it is an evidentiary-standard inconsistency in a document claiming mechanical discipline, and it leaves the pivotal inertness diagnosis (λ 60.5) without a committed reproducer. Mitigations found: the λ census is committed *in the lane dossier* pre-run (f0c2486, 17:21 < 23:45), and my independent recompute validated the 92% (→93.8%) and 49-position numbers. **Correction:** land the λ-flip census and the two C1 censuses in a committed `_repro/` artifact, and have §0 state the standard deviation from prereg §4 explicitly rather than silently.

**F4 — MAJOR (checklist b, domain side): steelman-GO §6 omits the mechanism-plausibility edge of the campaign's own delta-scan findings.**
The lanes surfaced adjacent-domain existence proofs for exactly the mechanism families killed: D2-08 (VARS — no-gradient, reward-driven *cross-session* accumulation on a frozen backbone, text), D2-01 (FlowEdit — training-free lifelong memory on a frozen speech model, 92.7% rel PER reduction), D3-3 (RECOVER — training-free agentic entity correction, 8–46% rel entity-WER), D3-10 (training-free sampling-consistency selection signal). The decision doc cites these only under "every claimed cell already occupied" (§5.11) — their anti-novelty edge — never their pro-mechanism edge ("the class works elsewhere; the local nulls are instrument/habitat artifacts"), which is the natural strongest GO argument and demonstrably stronger than parts of the case §6 actually assembles. A disposal exists in the record (B3 F2: external items "do not transfer GO-weight to speech under the novelty rule" — correct under frozen G1, which requires an in-house E-part), but §6, which the frozen skeleton (B.2 item 3, safeguard 7) obliges to be the *strongest assemblable* GO case, does not surface or rebut it. Relatedly, §5.9's headline "Delta scan strengthened the null" elides D1-10, which the D1 lane itself flags as leaving the matched-compute question "empirically CONTESTED, not settled either way" — the trailing "contested items resolve to the null under the frozen rule" is the correct mechanism but the headline overstates unanimity. **Correction:** add the existence-proof argument to §6 with its B3 disposal; name D1-10 in §5.9. Frozen-text grounding for severity: prereg §6 safeguard 7 and Appendix B.2 item 3.

**F5 — MINOR (traceability): "zero flips in 432 items" is not directly verifiable from the committed artifact.**
`m5_selector_confirmatory.json` per-item records carry `sel_pick_idx` but no MBR-pick field. I verified sel_wer_8 ≡ mbr_wer_8 in 432/432 items (necessary consequence of zero flips; not strictly sufficient — an equal-WER flip would be invisible). Add the MBR pick index to the artifact or rephrase as "selector and MBR WERs identical on all 432 items."

**F6 — MINOR (provenance wording): §5.3's "all committed pre-run" for the M3 refuter predictions is not supported by the git record.**
The M3 lane dossier was committed at 16:37 (2d22603), eight minutes *after* the kill artifact 1b53b46 (16:29). The refuter's evidence base (the C1 artifact) was committed pre-run, but the prediction text was not. Contrast M5, where SHARP PREDICTION 1 genuinely is pre-run-committed — the doc should cite that stronger provenance where it exists and soften the M3 wording.

**F7 — MINOR (literature coverage): two domain cells missing from the occupied-cell analysis.**
(a) LLM-based generative error correction over ASR n-best lists — the Hyporadise benchmark and GER line (Chen, Hu et al., NeurIPS 2023 Datasets & Benchmarks, arXiv:2309.15701; training-free in-context variants exist) — is the closest published family to "a frozen LLM operating on ASR hypothesis pools" and belongs beside ProGRes/RECOVER in §5.11; it simultaneously supplies the instrument family a non-inert M5 selector would have used, so its absence touches both edges. (b) Whisper's `initial_prompt` lexicon biasing as the trivial no-agency arm for M3-style injection (the M2 refuter cites `condition_on_previous_text` but the prompt-biasing cell is distinct). Neither changes the verdict; both strengthen or sharpen existing rows.

**F8 — MINOR (representation nits).** §5.9 cites D1-01 without its task scoping (multi-hop reasoning) or the context-degradation carve-out the lane records. The r1 adjudication of MSP-Podcast (D2-11) rests on abstract- and lab-page-level checks, hedged "on current evidence" in the lane but cited without hedge in §9; abstract-level "no audio" checks (D2-05/06) similarly. `realized_fraction` −0.0008 differs from the naive macro ratio (−0.00003/0.02378 ≈ −0.0013); the doc quotes the artifact field faithfully, but the artifact should document the field's definition.

### Detailed Comments

**Instrument validity (M3).** The pooled entity-match instrument fairly falsifies the frozen zero-support premise; per-entity heterogeneity (1.0 → 0.0) is reported, and the ALTHEA→ALETHEA systematic-spelling-prior case in the lane shows the matcher behaves sensibly. The kill stands. The interpretation defect is confined to breadth (F2), not mechanics.

**Instrument validity (M5).** From a decoding standpoint the confirmatory design was reasonable *for recurrence* (consecutive same-chapter read speech maximizes rare-token repetition) but is within-session read speech — the strict habitat of "cross-session accumulation" (temporal separation, channel/affect variation) is exactly what r1 says does not exist; the document's own re-open structure implicitly concedes the mechanism was habitat-limited by the data fence, which is a further reason §10 should close the *instantiations*, not the mechanism, on empirical grounds. Note also that even a positive result on this surface would have been ambiguous against plain within-session context conditioning (the M2 refuter's Whisper long-form point) — the no-agency pincer is domain-correct.

**Statistics.** M3's cluster bootstrap over a 36-utt/13-entity design is wide but the kill margin (CI-LB 0.245 vs threshold 0.01) is robust to any clustering choice. M5's paired design (432 items, 3 replica seeds, cluster-by-utterance, 10k draws) is fine; the degenerate CI is an instrument property, not an inference. Holm was moot on an all-zero grid. The Part-A caveat that the three gen-seed "replications" confound seed and item variance (disjoint 48-utt slices) is carried in the memo but not in §1 — acceptable, minor.

### Questions for the Authors
1. Will the λ-flip census, the V4 dev arms, and the two C1 censuses (0/49, 92%) be landed as committed `_repro/` artifacts with `reproduce:` lines, per prereg §4?
2. Does the confirmatory artifact permit an after-the-fact habitat census of the 12×12 surface (pool × session-prior rare-token overlap, analogous to the dev diagnostic)? If it shows ≈0 actionable positions, that strengthens the closure honestly; if it shows many, F1 sharpens.
3. Is §10 intended to be quoted verbatim in the converged paper? If so, the two scope corrections (F1, F2) should be applied before owner ack, since that sentence is the document's only externally citable artifact.

### Minor Issues
- §2 G1 row says "M5: confirmatory delta_vs_mbr = 0.0 ... sel_wer_8 = mbr_wer_8 = 0.07722" but omits greedy 0.0772 from the row; the near-identity of greedy and MBR is decision-relevant context for the "designed surface" reading.
- The doc cites "B4 §5" / "B5 §4" as section anchors into a single combined file (`2026-07-03-step1-blanes-memos.md`); anchors resolve, but a filename citation would be cleaner given the phantom-citation history.

---

**Verdict: sound-with-corrections.** The NO-GO is procedurally derivable from committed artifacts and frozen rules alone — via M3's genuine kill, M5's failed frozen threshold, and the inconclusive→NO-GO default — and none of my findings disturbs that derivation. The corrections required are: scope §10 and §1 to what the M5 measurement can support (F1), carry the M3 counter-datum and narrow the closure generalization (F2), commit the load-bearing interpretive numbers (F3), and complete the steelman-GO (F4).

### Report 4

# Perspective Review Report (Peer Reviewer 3 — Agentic Systems / LLM Memory; decision-theory & pre-registration practice focus)

**Artifact reviewed:** `wiki/2026-07-03-omni-agentic-tfrl-go-no-go-decision.md` (recommended: NO-GO)
**Reviewed against:** prereg `wiki/2026-07-03-agentic-tfrl-step1-preregistration.md` @ b19bff2; the six `_repro/*.json` artifacts (opened and re-verified); the ten `wiki/survey/2026-07-03-step1-*.md` lane files; the panel record. Fresh-adversary, read-only, independent.

### Reviewer Identity
LLM-agents researcher (memory-augmented systems, no-agency ablation design, test-time-compute literature) reviewing the GO side as its natural constituency would, with a cross-disciplinary lens on Value-of-Information reasoning, pre-registration practice, and the well-posedness of re-open conditions and pivot dispositions. I acknowledge outsider status on ASR scoring mechanics and on Lean formalisms; those are not the basis of any finding below.

### Overall Grade
**sound-with-corrections**

The NO-GO verdict is, on my reading of the frozen contract and the artifacts, substantively correct and in most places mechanically derived. The corrections required are not to the verdict but to (1) two framing sentences that over-credit the measurement, (2) one omitted steelman-GO argument, (3) an evenhandedness defect in number admissibility, and (4) two well-posedness gaps in the pivot/re-open apparatus that the document should record rather than paper over.

### Confidence Score
4 / 5 (artifact numbers independently re-verified; governance-clause parsing partially deferred to methodology reviewers)

### Summary Assessment
This is one of the more honest internal kill documents I have reviewed: outcome-symmetric skeletons pre-written, kill-first ordering honored, the M5 exact-tie prediction pre-committed and confirmed, the structural-null diagnostic reported in the verdict-supporting sections (not buried), pivot triggers checked mechanically against measured values, and r1–r3 restated genuinely verbatim (I diffed them character-for-character against prereg §2). B4's error-cost asymmetry analysis (wrong-GO sunk and front-loaded vs wrong-NO-GO bounded and reversible) is textbook-correct decision theory and genuinely vindicates the frozen inconclusive=NO-GO rule. However, the document never confronts the reachability of GO ex ante — on the frozen design, question (ii)'s only pre-decision positive route ran through an instrument the record had already proven inert — and it claims "reaffirmed by fresh pre-registered measurement, not by default" while reproducing, two sections later, a binding panel ruling that the M5 confirmatory carried "zero information ex ante." A NO-GO written under a NO-GO null hypothesis must demonstrate the test was winnable or say plainly that it was not; this document does neither, and quietly benefits from the ambiguity.

---

### Itemized Findings

**F1 (MAJOR — internal contradiction on the measurement's evidential weight).** §1 states the 7/02 verdict is "reaffirmed by fresh pre-registered measurement, not by default." The document's own §2 (G2 row) and §4 (C3 row) reproduce the binding panel ruling: "frozen V1|0.05 pre-proven inert (median required lambda 60.5), exact tie predicted then confirmed — **zero information ex ante**." Both cannot stand unqualified. The record supports a split statement: clause (b) is discharged by fresh measurement for **M3** (F = 0.38108 vs kill 0.01 was a genuine, informative kill — verified in `_repro/m3_phase0_zero_support.json`), but for **M5** by a null from an instrument already proven unable to flip a pick, and for M2/M4/M1 by the inconclusive→NO-GO default. "Not by default" is one-third true. Correction: rewrite §1's sentence to attribute reaffirmation per lane.

**F2 (MAJOR — GO-reachability never audited; the document benefits from the omission).** Under the frozen design: M3's GO-support E-part (Phase-1, ≥10-point entity-WER gain) was pre-registered as *post-GO*; M2/M4 E-parts post-GO; M1 conditional-unopened. The only lane that could discharge G1's E-part before the decision was M5 — and §5.12 ACCEPTS the refuter's pincer that even an M5 pass fails G1's no-agency conjunct (routing to P-A), leaving GO-minimal as the sole reachable positive grade, contingent on a pass by the frozen V1|0.05 arm, which the campaign's own λ-census had shown could not flip any pick before the confirmatory ran. So for question (ii), no achievable measurement outcome inside the frozen contract produced GO or GO-minimal. That does not invalidate the NO-GO (safeguard 1 resolves ambiguity against GO, and an unfalsifiable-GO prereg still yields a valid NO-GO under the contract) — but §10's "closed by pre-registered measurement rather than by scoping" and the §0 posture of a genuine test require the document to state this ex-ante-unreachability explicitly. Instead, §5.12 books the pincer as one more NO-GO exhibit. Correction: add a paragraph (in §5 or §6) acknowledging that GO for question (ii) was structurally out of reach at confirmatory time, and that the verdict therefore rests on the frozen default operating as designed, plus the M3 kill.

**F3 (MAJOR — steelman-GO omits the cheapest live GO-preserving action).** The strongest assemblable GO-side move on 2026-07-03 was not the V4-on-spent-pools argument §6 rebuts; it was: *seek the owner-signed V4 amendment (safeguard 5 exists precisely to make amendments legal), draw a NEW fresh test-other slice (prereg §4 contemplates plural confirmatory slices, "each touched once"), run once (~1 GPU-day per B5 §1), decide on day 3 of 10 instead of day 1.* The document's rebuttal leans on "the confirmatory slice is spent" (§5.5, §6) — true but not load-bearing, since fresh slices exist — and on the amendment gate, which is a gate, not a prohibition. The honest futility rationale is on the record (constructor's own PREDICTION 3: amended V4 comes back +0.001 to +0.006, CI crossing 0, on entity-unselected slices; refuter COUNT 2: 92% of residual headroom is ≤2-of-8 anti-consensus, making the 0.015 bar arithmetically implausible on any LibriSpeech-buildable surface), and it is a legitimate DSMB-style futility stop — but the document never states it as the reason. As written, checklist (b) is only partially met: a rebuttable weaker variant was rebutted in place of the strongest. Correction: add this argument to §6 and rebut it on futility grounds, which the record supports.

**F4 (MAJOR — asymmetric admissibility of non-artifact numbers).** Prereg §4: "Every number lands in a committed `_repro/` artifact." The panel enforced this strictly against M4's Tier-1 dev signal (scratchpad-only → inadmissible; C2 evidence line) — a would-be GO-adjacent number. Yet the decision doc's load-bearing *null-side* diagnostics are equally lane-memo/scratchpad-derived: median λ 60.5 (the basis of "pre-proven inert" and thus of the C3 zero-information ruling), V4 +0.00611/+0.00321, the 0/49 habitat census, the 92% anti-consensus mass (per the M5 lane file, these live in "analysis scripts + outputs in scratchpad"). §0 quietly weakens the traceability standard to "a committed `_repro/` artifact **or a campaign lane file**" without flagging the departure from §4. The deviation direction favors the recommended verdict, which is exactly when a frozen-rule deviation must be flagged. Correction: commit the λ-census/V4/census analyses as `_repro/` artifacts, or annotate every such number in §§2–7 as sub-§4-grade. (Note: ≤3/144 *is* artifact-grade — I verified `structural_null_diagnostic` inside `_repro/m5_selector_dev.json`.)

**F5 (MINOR — verdict-direction-dependent literature loading).** §5.11 "Every claimed cell already occupied — ACCEPTED" is asserted unqualified, while the same evidentiary base says the exact cell is open: D2/D3 negative findings ("archive claim A4-12 (open moat) still stands"; "M5's exact object is unoccupied… no scoop risk"), and B4 §5 prices wrong-NO-GO precisely as losing "first-mover position on the open moat." Both are reconcilable — the *upside* is occupied (RECOVER, biasing products, ROVER lineage), the *exact combination* (speech-native, no-gradient, cross-session accumulating selector) unclaimed — but the document asserts whichever half helps the section it appears in. Correction: qualify §5.11 with the open-sliver caveat the document itself relies on in B4/B5 citations.

**F6 (MINOR — P-D disposition vs the frozen skeleton, and an unreconciled VoI tension).** B.2 item 4 records a pivot "as a success" *conditional on it having triggered*; P-D uniquely has no trigger in the frozen text (it is an unconditional Part-A continuation) and was adopted by choice. Meanwhile the binding panel's C3 evidence line cites "pivots P-A/P-D pre-named, reached on every branch" as evidence *for* U2 (VoI ≈ 0). The document simultaneously records the guaranteed-pivot topology as a success (§8) and reproduces a ruling that treats it as a VoI defect (§4), with no reconciliation. Correction: relabel P-D "ADOPTED (unconditional continuation; no trigger defined)" and drop or qualify "recorded as a success."

**F7 (MINOR — re-open conditions are ill-posed against the document's own live successors).** r1–r3 are exclusively exogenous-event conditions (a corpus *appears*, a theorem *appears*, *literature* overturns a kill). Yet the document keeps endogenous successors alive whose positive outcomes would substantively re-open question (ii) while triggering no r-condition: P-A-class selector families "under its own future trigger" (§8), the S6-residual logprob interface, the true-OOV re-preregistration path (B3 §6). An in-house V4-class positive under a future prereg is not "literature" (r3), and M5's no-pass on an inert instrument is arguably not a "kill" r3 could overturn. "Closed, not merely deferred" (§10) is contract-licensed, but the closure will be procedurally orphaned if the most probable actual route to revival — the campaign's own named successor work — succeeds. Correction: add a record note in §9 acknowledging the coverage gap (no re-open path for in-house successor evidence) so a future owner is not forced to choose between honoring the closure and honoring new internal measurement.

**F8 (MINOR — G2's invented verdict category obscures what VoI was actually shown).** "SATISFIED-IN-FORM / MOOT" is not a grade the frozen G2 defines. On the substance, the VoI decomposition matters: M3's kill genuinely informed D-1 (Phase-1 cancel) — real VoI; but the M5 confirmatory carried no information about D-1's live alternative (whether to ship a *V4-class* selector), since the arm run was the inert V1 — B4's "behavioral proof" (§3: GPU-hours wired to outcomes) demonstrates outcome-*wiring*, not information value. The panel's ruling got this right; the document ultimately defers to it, but the hybrid label plus reliance on the post-outcome B4 memo (also in the §7 U2 record note) blurs which criterion was adjudicated on what evidence. (The category-invention mechanics belong to the methodology reviewers; the VoI reading is mine.)

---

### Detailed Comments (persona protocol)

**Assumption audit.**
- *Explicit:* the document assumes the 12×12 consecutive reading-order slice is "a surface DESIGNED to favor the mechanism" (§5.4, §6 rebuttal). The constructor's own PREDICTION 3 undermines this: the slice is entity-*unselected*, and even the correct instrument (V4) was predicted sub-threshold on it. "Designed for session depth" ≠ "designed for channel mass." The rebuttal to steelman-GO bullet 1 should not lean on this phrase.
- *Implicit:* that closing two ASR-selector instantiations plus literature scans closes "the omni agentic system (skills/memory/routing)" question. Skills and routing were never measured ("no decomposed/multi-model configuration ever ran anywhere in the campaign," C4 evidence line); the closure runs through the inconclusive-default and the r1/r2 gates. The §10 sentence is carefully scoped to what was measured — good — but the document title ("agent-level question closed") will be read broader than the evidence; the contract authorizes it, the reader should still be warned.
- *Paradigmatic:* the campaign operationalizes "agency" as within-pool re-scoring with text-state bookkeeping, and its agency observable (shuffle-load-bearing) is accepted by the document itself as discriminating context-vs-no-context, not agent-vs-no-agent (§5.12). This is a known weakness of no-agency ablations in the agent-memory literature; the document handles it honestly but should recognize it means the prereg never possessed a valid agency detector — which feeds F2.

**Cross-disciplinary connections.** The external loadings I audited are fairly characterized: D1-01 (equal-budget single-agent ≥ multi-agent, with the context-degradation carve-out preserved), D1-02 (debate-martingale, correctly described), D1-10 honestly carried as the contested counterpoint and resolved to the null under the frozen rule, D2's audio-excluding benchmark wave verified per-abstract. The one asymmetry is F5. From clinical-trials practice: the correct precedent for M5 is a *futility stop with an assay-sensitivity failure* — the trial also showed the comparator (MBR) indistinguishable from placebo (greedy) on the fresh slice (−0.00003, CI [−0.00358, +0.00369], verified in the artifact), which in drug-trial terms means the confirmatory could not have detected an effective agent either. The steelman (§5.7) reports this; the verdict rows should carry the assay-sensitivity framing explicitly rather than only "kill."

**Practical impact.** The freed-capacity routing (§8: W4 queue, r1 monitor) is concrete and immediately actionable; K1–K6 are real, checkable step-2 kill criteria — K6 (headroom-floor kill on the P-D thread itself) is a genuinely good self-binding move. The owner gate is preserved (§11) and the Decision-Log entry faithfully mirrors the body, including the inconclusive-default disclosure.

**Broader implications.** For the team's research-governance practice, the transferable lesson this document should record but doesn't: *freeze criteria and thresholds, but never freeze a specific instrument configuration ahead of the evidence that selects it* — the dev grid's all-zero tie forced a simplicity-rule winner that was provably inert, and the single-touch rule then burned the designed slice on it. A one-line process amendment ("an instrument shown non-functional on dev triggers a mandatory owner amendment decision *before* any confirmatory touch") would have converted this campaign's weakest link into procedure.

### Cross-Disciplinary Reading Recommendations
1. **PCI-RR / Registered Reports stage-2 guidance (Chambers & Tzavella, 2022, *Nat. Hum. Behav.*)** — on distinguishing "null result" from "manipulation/instrument failure" in pre-registered outcomes; directly applicable to the M5 killed-vs-untested framing.
2. **DSMB futility-stopping literature (e.g., Lachin 2005, conditional power)** — the correct formal frame for rebutting F3's amendment-plus-fresh-slice argument on futility rather than on spent-slice grounds.
3. **Raiffa & Schlaifer, *Applied Statistical Decision Theory* (VoI chapters)** — B4's behavioral-proof argument conflates decision-wiring with expected value of sample information; EVSI of the inert-V1 confirmatory was ~0 by construction, which is the panel's point stated formally.
4. **Kapoor & Narayanan (2023) on evaluation leakage / instrument validity in ML claims** — for the asymmetric-admissibility issue (F4).

### Questions for Authors
1. Given the record proved V1|0.05 inert before the confirmatory ran, why was safeguard 5's amendment path not put to the owner *before* spending the single-touch designed slice — and can the decision doc state the answer?
2. Was GO-minimal ever reachable after the dev grid tied all-zero? If not, in what sense was question (ii) "tested" rather than "defaulted, with corroborating nulls"?
3. If a future in-house P-A-track selector shows load-bearing accumulation under a new prereg, which of r1–r3 re-opens question (ii)? If none, is "closed" the status you intend?

### Minor Issues
- §2 G1 row: "zero flips in 432 items" traces to the lane file's E-part narrative; the committed artifact shows sel=mbr exactly but has no explicit flip-count field in `summary` — cite the per-item block or add the field.
- §0's "or a campaign lane file" should cross-reference the B3/B4/B5 post-panel provenance note in the same paragraph so a citing reader sees both qualifications together.
- §5 heading says "Steelman-NO-GO … rebutted or conceded"; all 18 are ACCEPTED — the boilerplate "rebutted" clause should be dropped for accuracy.
- The 中文摘要 renders "recorded as a success" for P-D (「记录为成功」) with the same unconditional-trigger issue as F6; correct both together.

**Recommendation: sound-with-corrections** — the NO-GO stands on the frozen contract; corrections F1–F4 are required before the closure sentence is cited externally, F5–F8 before the document is archived as the campaign's governance record.

### Report 5

# Devil's Advocate Review — NO-GO Decision Document (`wiki/2026-07-03-omni-agentic-tfrl-go-no-go-decision.md`)

**Reviewer:** Devil's Advocate (adversarial audit; mandate: overturn the NO-GO if possible). Fresh-adversary, blind to lane deliberations. All artifacts re-opened from disk; all frozen-text diffs made against prereg @ b19bff2 as committed.

**Strengths acknowledged first:** the freeze-hygiene chain is real and verifiable on disk (c8bebaf pre-commit 15:55 → d4dd117 freeze-before-generation 16:04 → kill/verdict commits 1b53b46 16:29 / f8ec1d3 23:45, all 2026-07-03; `tie_break_applied=false`; dev-spent and M3 exclusions present in the slice manifest), and every core kill number I re-opened is exactly as quoted (F=0.38108, CI [0.24477, 0.51823], KILL=true; delta_vs_mbr=0.0, CI [0.0, 0.0]; sel=mbr=shuf=0.07722; ablation 0/0; MBR-vs-greedy −0.00003 [−0.00358, +0.00369]; oracle +0.0238; realized_fraction −0.0008; elapsed 1,886.4 s / 25,988.2 s). No fabricated numbers were found.

---

## Strongest Counter-Argument

This document ratifies its null hypothesis through a procedure that could not have produced any other outcome, then exports the result as measurement. By its own binding panel record (C3/U2: the frozen V1|0.05 selector was "pre-proven inert — median required λ 60.5"; the "exact tie predicted then confirmed — **zero information ex ante**"), the only confirmatory run that could have satisfied G1 carried no information before it started. By its own **accepted** steelman point 12, G1's no-agency conjunct was "structurally unsatisfiable" — meaning no data outcome whatsoever could have produced GO. A campaign in which GO is unreachable ex ante and the confirmatory instrument is known-inert at freeze time (the structural-null diagnostic sits in the 16:01 dev artifact; the freeze commit is 16:04) is not a test of question (ii); it is a re-derivation of 7/02. Yet §1 claims the verdict was "reaffirmed by fresh pre-registered measurement, not by default," and §10 exports "closed by pre-registered measurement rather than by scoping." For M5, those sentences contradict the panel ruling the document itself declares binding. The honest record: M3 was genuinely measured and killed (on clean audio, with a conceded truly-unsupported entity residual); M5 was never habitat-tested by an instrument capable of acting — it is *inconclusive*, defaulting to NO-GO. Meanwhile the one cheap decisive act — an owner-signed amendment (safeguard 5's own mechanism) running a non-inert selector on the fresh pools or a second fresh slice (§4 says "slices," plural; 33 eligible speakers; ~7 h GPU; 9 timebox days remaining) — was never presented to the owner, whose gate is still open. NO-GO stands; "closed by measurement" does not.

---

## Issue List

*Severity in every CRITICAL/MAJOR row rests on the document's own frozen contract (prereg @ b19bff2) and its own internal record — an externally checkable source — not on an asserted field norm; the field-norm columns are therefore N/A throughout.*

### CRITICAL

| # | Dimension | Issue Description | Location | Field-Norm Boundary | Evidence-Crossing Rationale |
|---|-----------|-------------------|----------|---------------------|-----------------------------|
| C-1 | Logic-chain break / data-conclusion mismatch | The document simultaneously asserts (a) the U2 panel ruling is binding — the frozen confirmatory selector was pre-proven inert, the exact tie "predicted then confirmed — zero information ex ante" (§2 G2 row, §4 C3, §7 U2) — and (b) that the 7/02 verdict was "reaffirmed by fresh pre-registered measurement, not by default" (§1) and "closed by pre-registered measurement rather than by scoping" (§10). Both cannot be true for M5: a measurement carrying zero information ex ante cannot reaffirm anything. The correct M5 status per the document's own record is "untested at threshold by an inert instrument → inconclusive → NO-GO by the frozen default." The NO-GO verdict survives (inconclusive = NO-GO is frozen text); the exported characterization does not. §10 is the sentence destined for the converged paper — it must not ship as worded. | §1, §10 vs §2 G2 / §4 C3 / §7 U2; `m5_selector_dev.json` diagnostics (16:01) vs freeze d4dd117 (16:04); M5 lane file A7 + SHARP PREDICTION 1 | N/A (internal contradiction) | The contradiction is between two load-bearing claims inside the same document, both quoted verbatim above |

### MAJOR

| # | Dimension | Issue Description | Location | Field-Norm Boundary | Evidence-Crossing Rationale |
|---|-----------|-------------------|----------|---------------------|-----------------------------|
| M-1 | Strawman / omitted GO argument (checklist b) | §6's "strongest assemblable GO case" is built from conceded-moot G2/G3/G4 strengths and rebutted in four bullets. The genuinely strongest anti-closure argument in the record is omitted, not rebutted: the M5 lane's own open question — "Will the owner sign an amendment adding the V4 memory-dominant arm (CPU-only re-scoring of the SAME confirmatory pools, no extra GPU)?" (lane file §Open questions; PREDICTION 3 costs it at ~2 min CPU) — plus a second fresh slice (prereg §4: "fresh test-other slices, each touched **once**" — plural; 33 eligible speakers, 12 used). §5.17's "Nothing runnable inside the timebox can change the answer" is true only under a no-amendment assumption the frozen prereg does not impose: safeguard 5 *defines* the amendment path, and the decision was taken on day 1 of 10. §5.5 rebuts only the V4 *dev* evidence (correctly inadmissible); it never addresses V4-on-fresh-pools. The constructor's own sub-threshold prediction (+0.001–0.006) makes NO-GO the likely outcome anyway — but "likely" ≠ "nothing runnable can change the answer," and the fork belonged in front of the owner. | §5.5, §5.17, §6; M5 lane §Open questions, §Minimal empirical prediction; prereg §4, §6.5 | N/A (frozen-contract omission) | The omitted option is explicitly written in the campaign's own lane file and costed; a steelman that skips it is not the strongest case |
| M-2 | Cherry-picking / asymmetric evidence admissibility (checklist e) | Prereg §4 ("Every number lands in a committed `_repro/` artifact") was enforced against defense-side numbers — M4's positive Tier-1 dev signal (+0.0072 [0.0020, 0.0143]) struck as "scratchpad-only, inadmissible under prereg §4" (§3 M4, chair C2) — but not against verdict-side numbers: the λ-census 60.5, V4 +0.00611, the 0/49 census, and the 92% anti-consensus decomposition are equally scratchpad-derived (M5 lane: "analysis scripts + outputs in scratchpad") yet are load-bearing in the C3/U2 ruling, steelman §5.5/§5.7, and the §2 G2 row. One rule, one-directional enforcement, direction always pro-NO-GO. Either strike both classes or admit both. | §2 G2 row, §3 M4, §5.5, §5.7; hostile-panel file C2/C3; M5 lane §dataset_on_disk | N/A | Same frozen clause (§4), demonstrably applied to one side only |
| M-3 | Frozen criteria not applied as written — NO-GO clause (b) (checklist a/c) | Frozen text: "**all** mechanism lanes hit their **kill thresholds** AND the M5 ablation shows accumulation is not load-bearing." M2/M4/M1 hit no kill threshold (never executed); M5 has *no frozen kill threshold at all* — prereg §5 M5 defines only a PASS bar (≥0.015) and a Goodhart guard; failing to pass is not hitting a kill. The row is scored "MET — via executed-lane kills + the inconclusive→NO-GO default." That default supports the *overall* NO-GO (global rule), but it cannot convert clause (b) to MET; the row contains a constructed bridge argument inside a table §0 claims is "applied criterion by criterion with no new arguments." Honest scoring: clause (b) NOT strictly met; NO-GO via the global inconclusive rule. | §2 NO-GO clause (b) row vs prereg §2, §5 M5 | N/A | Character-level diff against frozen text |
| M-4 | Post-hoc reinterpretation of G3 — tightening against GO (checklist a) | Frozen G3 corpus clause: "a named on-disk / pseudo-session / TTS path" — literally satisfied (paths built and exercised: `m3_phase0_selection.json`, `m5_confirmatory_slice_ids.json`); with operator resolved, the literal G3 reads 2-of-3 PASS. The doc scores "FAIL (substantive)" via B3's "three-ingredient substantive test" — an instrument invented in a post-outcome memo, nowhere in the frozen text. Safeguard 1 covers *ambiguity*; the corpus clause is not ambiguous. A post-hoc tightening is a criteria violation even when it favors the recommended verdict (and it propagates into the P-B row's "G3 fails on corpus AND theorem"). Moot for the verdict — G1 binds — so the fix is to score G3 by the frozen text and mark it moot. | §2 G3 row, P-B row; B3 memo §0/§5; prereg §2 G3 | N/A | The frozen clause names the pseudo-session path as sufficient; the substituted test post-dates the outcome |
| M-5 | Post-outcome memos discharging criteria (provenance; checklist a/e) | The panel struck every panel-time B3/B4/B5 citation as phantom (memos not on disk); the memos were then authored post-panel, post-outcome — and now discharge the G2, G3, and G4 rows ("B4 lane memo §2, §3, §6 (this run)" etc.). §7's U2 "record note" additionally uses post-panel B4 to append an ANSWERED-at-reduced-scope gloss to a ruling the doc says "cannot re-litigate." Evidence authored after the outcome was known cannot carry the same weight as pre-outcome deliverables in a pre-registration audit; at minimum the rows must be flagged as discharged by post-outcome compilation, and the U2 record note deleted or moved to an appendix. Disclosure in §0 is honest but does not cure the load-bearing use. | §0, §2 G2/G3/G4 rows, §7 U2 row; hostile-panel STRIKE CHECK | N/A | The strike ruling and the memos' authorship timing are both in the document's own record |

### MINOR

| # | Dimension | Issue Description | Location |
|---|-----------|-------------------|----------|
| m-1 | Overgeneralization | M3 ran at `condition: clean` (artifact + selection commit) while every other campaign measurement (C1 headroom, M5) lives at SNR-5; the decision doc never states the condition, and §10 generalizes "the frozen model already emits the 'rare' entities a cross-session lexicon would supply" without the condition scope or the conceded truly-unsupported residual (SHARDURIS 0.0, CONFECTIONARY 0.0104, FARRINDER 0.0156 — the exact class a lexicon serves). Kill mechanically valid; exported sentence over-broad. | §3 M3, §10; `m3_phase0_zero_support.json` per_entity, condition |
| m-2 | Post-hoc standard import (checklist d) | P-C dismissed on "all T-parts 'STATED, not proved,' zero Lean lines" — but frozen G1's T-part demands "a formal statement with explicitly stated assumptions," not a proof; the Lean bar belongs to P2's overturn column. "Surviving" is unfrozen and was resolved against a *pivot*, though safeguard 1 licenses resolving ambiguity only against GO. Low practical impact (P-D adopted; refuter R1's empirical-Bayes reduction is an independent ground), but it feeds the pattern of unfrozen ambiguities uniformly resolved toward the null narrative. | §2 P-C row, §8; prereg §2 G1/P-C |
| m-3 | Vacuous conjunct | Clause (b)'s second conjunct ("M5 ablation shows accumulation not load-bearing") is satisfied vacuously: gain_sel = gain_shuf = 0.0, retained = null — there was no gain to ablate. The artifact reports this honestly; the table rounds it up to a positive showing. | §2 NO-GO (b), GO-minimal rows; `m5_selector_confirmatory.json` ablation |
| m-4 | Traceability slippage (checklist e) | §1 attributes the per-seed slice reductions "+0.0506/+0.0480/+0.0270" to `_repro/asr_bon_llamacpp_snr5.json`; they are not in that artifact's summary (they are the Part-A memo's recomputation from per-item rows). More broadly, §0's standard ("a committed `_repro/` artifact **or** a campaign lane file") is weaker than prereg §4's committed-artifact requirement; λ 60.5, +0.00611, 0/49, 92%, and all person-week costings trace only to lane memos. | §0, §1; `asr_bon_llamacpp_snr5.json` summary; prereg §4 |

---

## Ignored Alternative Explanations/Paths

1. **Inert instrument, not dead mechanism.** The more parsimonious explanation of M5's exact zero — endorsed by the document's own panel ("zero information ex ante") and its own steelman diagnosis (≤3/144 dev positions; λ-census) — is that the selector could not act, not that accumulation is falsified. The steelman carries this honestly; the verdict rows and §10 do not. Should have been the recorded M5 status ("inconclusive-by-inert-instrument → NO-GO by default").
2. **Owner-signed amendment + non-inert arm inside the timebox.** V4 on the same fresh confirmatory pools (~2 min CPU per the lane's costing) or a second fresh once-touched slice (~7 h GPU; §4 permits plural slices) — the frozen amendment mechanism (safeguard 5) exists precisely for this; the fork was never surfaced to the pending owner gate.
3. **Entity-density-stratified admissible slice** (the constructor's open question; label-free selectable from pool statistics) as the habitat test the 12×12 reading-order surface may still not be.
4. **M3 Phase-0 at the SNR-5 operating point**, separating lexical support (tested, present) from acoustic support at the condition where the headroom actually lives — the frozen kill was condition-unpinned and was run at the kill-favoring condition.
5. **P-C (theory-only)** under the literal frozen T-part standard, rather than the imported Lean bar.
6. **Declaring the G1 no-agency conjunct malformed.** If §5.12 is accepted — the conjunct is structurally unsatisfiable — the frozen-contract-honest response is to refer the malformed criterion to the owner for a logged repair, not to silently benefit from its unsatisfiability while presenting the campaign as an outcome-symmetric test (safeguard 12's symmetry was formal, not substantive).

## Missing Stakeholder Perspectives

- **The owner as a mid-campaign decision-maker.** The lane file explicitly asked "Will the owner sign an amendment…?"; the question died between the lane file and this document. The owner is presented with a finished NO-GO, never with the amendment fork the frozen prereg provides.
- **Future readers of the §10 closure sentence** (the converged paper's audience), who inherit "falsified mechanically" for M5 without the inert-instrument caveat the internal record carries.
- **The personalization/deployment constituency** whose real-world case is exactly the truly-OOV residual class (SHARDURIS-type entities) that the pooled kill averages away.

## Unexamined Premise (Frame-Lock)

The document treats "question (ii) as posed" (build skills/memory/routing over frozen models?) as equivalent to "these two instantiations under this fence" — one pooled entity-support check on clean read speech, and one pre-proven-inert lexicon selector on LibriSpeech pseudo-sessions. Closure of the question *is* frozen-text-authorized (absent r1–r3, closed) — but only via the default rule. The premise that the *measurements* did the closing is what §10 sells and what the record cannot support. Deeper still: a pre-registration whose GO conjunction is, per its own accepted steelman, structurally unsatisfiable is treated throughout as a valid test rather than as a contract defect discovered post-freeze.

## Observations (Non-Defects)

- The document is unusually candid: §0 discloses the memo provenance, §2 hedges the clause-(b) reading, §3 carries the structural-null diagnostic, and the steelman quotes the evidence for my C-1 finding. Most of this review was assembled from the document's own disclosures — good faith is evident; disclosure just does not cure contradiction.
- Timing forensics cleared one suspicion: the confirmatory design was frozen (16:04) *after* the dev structural null was known (16:01), but the direction of that choice favored the mechanism (a designed deep-session surface), so no anti-GO foul there — the foul is freezing the known-inert *selector* into it.
- r1–r3 are restated genuinely verbatim (§9 ✓ against prereg §2); GO-minimal and P-A rows are mechanically correct; the Decision-Log entry (§11) faithfully mirrors the body, including the "inconclusive = NO-GO" attribution for M2/M4/M1 — which is, notably, more honest than the §2 clause-(b) row.
- Under the frozen criteria as measured, no reasonable panel could have reached GO or GO-minimal on this evidence (M5 PASS = false is arithmetic); my findings attack the procedure's characterization and completeness, not the arithmetic.

---

## Final Grade: **sound-with-corrections**

The NO-GO verdict on question (ii) survives every finding above — it is over-determined by the frozen "inconclusive = NO-GO" default and by the genuinely measured M3 kill. But the document as written is not exportable: C-1 (the "reaffirmed by measurement / zero information ex ante" contradiction) must be resolved by relabeling M5's contribution and rewriting §10; M-1 requires the owner gate to see the amendment fork before the question is stamped closed; M-2 through M-5 require the criteria table and evidence-admissibility record to be corrected so that the claim "applied mechanically, as written" becomes true. If §10 ships uncorrected, the exported closure sentence — the single sentence this document exists to produce — is unsound.
