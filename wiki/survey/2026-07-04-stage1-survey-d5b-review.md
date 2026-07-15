# Stage-1 survey paper — D5b strict review record (/ars-reviewer full, 5 personas + synthesis)

> academic-paper-reviewer v1.10 full mode · workflow wf_707e82fb-c2a · verdict: **MAJOR REVISION**
> (5-reviewer convergence; no CRITICAL, no Reject; DA: none survived own severity gate). Owner directive:
> the survey goes through strict Academic-skills review before K2. EIC-Q2 answered: INTERNAL Stage-1
> deliverable -> S14 governance-externalization NOT required.

## Reviewer configuration (field analyst)

I have read the full paper (648 lines, S1–S10 + Appendix A) and the role definition. Below is the Field Analyst deliverable: the field analysis and the 5-reviewer Configuration Card, adapted for a Stage-1 survey paper per the task's survey-specific checklist (a)–(f).

---

# Field Analysis Report & Reviewer Configuration Card — 5-Reviewer Panel

**Review target:** `D:/chao_workspace/exploring-l4-intelligence/wiki/2026-07-04-stage1-semantic-tfrl-survey.md`
**Verification layer (must be treated as ground truth for faithfulness checks):** 8 lane files `D:/chao_workspace/exploring-l4-intelligence/wiki/survey/2026-07-04-stage1-{L1-asr-st, L2-slu, L3-sqa-reasoning, L4-speech-agentic, X1-prompt-space-quantification, X2-paralinguistic-delta, X3-llm-vlm-testtime-map, 3w-crossdomain-comparisons}.md`
**Supporting governance docs:** `2026-07-04-sufficiency-yardstick-memo.md` · `2026-07-04-stage1-evidence-regrade.md` · `2026-07-04-paralinguistic-premise-consolidation.md`

## Paper Basic Information

- **Title:** "Is the Instruct-Prompt Rollout Optimization Space of Frozen Omni Speech Models Sufficient? A Cross-Domain Survey for the Semantic Layer"
- **Type:** Stage-1 (problem-definition) SURVEY — argues from published literature; in-house numbers appear only as grade-tagged directional anchors (13-row ledger, Appendix A)
- **Full text length:** ~16k words (648 lines); **References:** 162 numbered + a pending-verification annex of 8 unnumbered arXiv IDs
- **Structure:** S1 motivation · S2 sufficiency yardstick (H_fix / H_prompt / ρ; a/b1/b2/c ladder; closure fence) · S3 11-family cross-domain transfer map · S4–S7 four task-family deep dives (ASR/ST, SLU, SQA, speech-agentic) · S8 ladder evidence table + n=50 directional probe · S9 eight unranked candidate problems (CP-1..CP-8) · S10 references · Appendix A in-house numbers ledger

## Field Analysis (6 dimensions)

| Dimension | Analysis Result |
|---|---|
| Primary Discipline | Speech/audio-language processing — frozen (training-free) audio-LLM / omni-model test-time methods |
| Secondary Disciplines | (1) Text-LLM prompt optimization & test-time compute; (2) VLM test-time methods & failure-mode literature; (3) evaluation meta-science (multi-prompt evaluation, negative-result methodology, evidence grading) |
| Research Paradigm | Literature review with a novel conceptual framework (operational yardstick) + one pre-registered small-n directional probe; NOT an empirical paper |
| Methodology Type | Cross-domain scoping review + comparative transfer mapping; "verified-empty" negative-result claims are load-bearing and must be auditable against the lane files |
| Target Journal Tier | Q1-survey standard (ACM CSUR / TMLR-survey / TASLP-overview class ambition), though currently an internal program document with governance scaffolding (grade tags, closure fence, owner language) a public venue would question |
| Paper Maturity | Pre-submission draft (DRAFT-FOR-REVIEW): complete structure, fixed global numbering, ledgered numbers; the risk surface is fidelity and discipline, not completeness |

## Venue Calibration (for EIC framing only)

1. **ACM Computing Surveys** — cross-domain taxonomy + transfer map is CSUR-shaped
2. **TMLR (Survey Certification)** — tolerant of the negative-result-as-contribution stance
3. **IEEE/ACM TASLP overview article** — primary-discipline fit; would stress speech-side balance

---

## Reviewer Configuration Card #1

**Role:** EIC (panel chair; global verdict calibration)
**Identity Description:** Senior Editor of *ACM Computing Surveys* for the language-and-speech area; 15 years as TASLP associate editor before that; has desk-rejected dozens of "survey-shaped position papers" and accepted taxonomy surveys that outlived their citations; personally runs spot-audits of reference lists before assigning verdicts.
**Expertise:** survey genre standards; contribution durability; taxonomy-as-contribution assessment; editorial calibration of accept / minor-revision / major-revision / reject for review articles.
**Review Focus:**
  1. **(b) global coverage & balance** — do the four family deep dives (S4–S7) get equal evidentiary rigor, or does ASR (the family with in-house data) get disproportionate depth while SLU/SQA lean on thinner sourcing? Is the training-free-vs-fine-tuned positioning free of cheerleading at the *framing* level (S3.13 regime rule, S6.3 "live positioning opening rather than settled defeat")?
  2. **(a) citation-integrity accountability** — own the panel's sampling plan: verify the panel collectively spot-checks ≥20% of [1]–[162] via WebFetch, stratified across origin domains and including every reference supporting a table cell in 8.1; adjudicate any claim that cannot be traced to a lane file or resolvable source as a defect.
  3. **Genre verdict** — is this a survey an external reader can use (transfer map + yardstick as durable artifacts), or a program memo whose recommendations only make sense inside the Stage-1/2/3 governance? Would S9 survive with the closure-fence flags read by someone who has never seen the NO-GO record?
**Will particularly care about:** whether the paper's two claimed distinguishing contributions — the origin-attributed transfer map (S3) and UNMEASURED-cells-as-first-class-results (S8) — are genuinely novel synthesis or repackaged lane-file content; and whether the abstract's claims match the body's hedges exactly.
**Possible blind spots:** will not verify per-number fidelity of quoted results; may under-weight Stage-1 internal discipline items (d) as "house style" — compensated by Reviewers #2 and #5.

---

## Reviewer Configuration Card #2

**Role:** Peer Reviewer 1 — Methodology (evaluation science & measurement validity)
**Identity Description:** Researcher in LLM evaluation methodology at a measurement-focused lab; author of work in the FormatSpread/PromptEval lineage on prompt-sensitivity quantification and multi-prompt evaluation; trained statistician (small-sample inference, pre-registration practice); serves on the NeurIPS Datasets & Benchmarks program committee where she reviews evidence-grading protocols.
**Expertise:** operationalizing fuzzy constructs into measurable quantities; oracle/selector decompositions; CI semantics for n<100; systematic-review search-protocol auditing (PRISMA-style documentation of negative searches).
**Review Focus:**
  1. **(e) yardstick validity** — are H_fix(T,N), H_prompt(T,K,N), ρ(T) actually well-defined (metric direction, oracle definition, budget conventions)? Is the (b)-no-theorem asymmetry (§2.6) stated honestly and consistently used — i.e., does any later section quietly treat (b) as bounded? Does Table 8.1 follow the yardstick's own conventions cell by cell? **Critical check:** §8.3's probe compares 8×4 vs 1×32 at matched budget — does that arm design estimate the §2.2 quantity H_prompt(K,N) − H_fix(N) as defined, or a budget-confounded variant, and does the paper say which?
  2. **(d) Stage-1 discipline on in-house numbers** — audit Appendix A against every in-house number in the body: all 13 rows grade-tagged at every citation site; grep-level check that *confirms / establishes / demonstrates / significant* never modify an in-house number; the probe used only as directional-only (does the §8.3 "Directional reading: … shifts toward schema-rich tasks" sentence stay on the right side of recommend-vs-decide?); constraints (ii)/(iii)/(v) admitted as unrun.
  3. **(a) methodological citation fidelity** — spot-check the theory citations [17]–[22], [24], [26]–[29], [32], [36], [40], [61]–[65]: does each source support the specific quantitative claim attached to it (e.g., KL bound form in §2.3, "90% of average-to-best gap" [64][65], "+17.9% GSM8K" [36])?
**Will particularly care about:** whether "verified-empty" claims are backed by documented, dated search protocols in the lane files (L1 §4.4 five searches, L2 §5.4 five cells, L3 §6.4 four cells, L4 §7.4 N1–N4) — an undocumented negative claim is a MAJOR defect in a paper whose headline contribution is negative cells.
**Possible blind spots:** speech-domain ground truth (whether quoted speech results are faithfully represented); venue-fit questions. Compensated by #3 and #1.

---

## Reviewer Configuration Card #3

**Role:** Peer Reviewer 2 — Domain (speech / audio-LLM literature)
**Identity Description:** Senior researcher in spoken language processing who has worked both sides of the survey's fence: a decade of n-best/lattice rescoring and GER work (HyPoradise-generation), now benchmarking frozen LALMs (contributor to a Dynamic-SUPERB-class suite); reviews for Interspeech, ICASSP, ASRU, and TASLP; known for checking quoted numbers against the cited PDFs.
**Expertise:** ASR/ST oracle and selection literature; SLU (SLURP/MASSIVE class); audio-reasoning benchmarks (MMAU/MMAR/MMSU/SAKURA); voice-agent evaluation (tau-Voice/VoiceBench class); knows which 2025–2026 arXiv results replicated and which quietly didn't.
**Review Focus:**
  1. **(a) citation integrity, speech side — the panel's heaviest WebFetch load:** aggressively resolve and verify the speech-critical citations and their quoted deltas: [1][2][3] (sensitivity/AHAMask framing), [23][25][33][35][39] (oracle/selection), [60][71][72] (PromptingWhisper/SICL/TICL percentages), [78][82] (Audio-CoT 55.60→57.80/58.10; TwS +24.7–36.6pp), [112]–[124] (S4 problem sourcing), [125]–[135] (S5), [136]–[148] (S6), [149]–[161] (S7 — including whether tau-Voice really reports "79–90% agent-driven" and pass@1-only). Flag any [n] that resolves but does not support its sentence.
  2. **(b) coverage & balance** — are the four families surveyed fairly (S5's SLU evidence is notably thinner — is that the field or the search?); is fine-tuned SOTA given its full due in every positioning subsection (S4.3, S5.3, S6.3, S7.3), including gradient results the training-free framing might prefer to soft-pedal?
  3. **(f) occupied-cell risk from domain knowledge** — for each CP-1..CP-8, ask: do I know a published or preprint work that already fills this "empty" cell (e.g., any 2026 prompt-search-on-Whisper/Qwen-Audio work, any audio pass@k study, any LALM calibration paper) that the lanes missed? A single occupied cell in S9 is a CRITICAL finding for a problem-definition document.
**Will particularly care about:** whether lane-file claims survived compression into the paper without drift — the paper must be *faithful to* the 8 lane files, so any number, verdict, or fence label that differs from its lane source is a defect even if the paper's version sounds more reasonable.
**Possible blind spots:** text-LLM/VLM origin claims and the formal yardstick; may accept the taxonomy's ladder assignments uncritically. Compensated by #2 and #4.

---

## Reviewer Configuration Card #4

**Role:** Peer Reviewer 3 — Perspective (cross-domain: text-LLM / VLM test-time methods)
**Identity Description:** Researcher in test-time methods for text LLMs and VLMs — publishes in the APE/OPRO/GEPA prompt-optimization line and on verifier-guided best-of-N; ran a tutorial on VLM evaluation pitfalls (WaffleCLIP, MMStar, VL-RewardBench); has never worked on speech, which is exactly why he is here: he owns the origin-domain half of every row in Table 3.1.
**Expertise:** prompt-search algorithm genealogy and its measured gains; coverage/selection scaling laws; reward over-optimization; VLM transfer failure modes (base-class overfitting, descriptor misattribution, perception-blind judges, grounding bottlenecks); agent scaffolding cost-controlled evaluation.
**Review Focus:**
  1. **(c) taxonomy soundness** — is the 11-family map coherent and non-arbitrary? Audit per family: origin attribution correct (is F10 really VLM-native? is MBR's origin fairly given to MT?); fence labels right (ARGS trained-head vs RAIN training-free); ladder assignments defensible (is calibration genuinely b2 rather than c — §3.6's harmonized convention is a judgment call that must be argued, not asserted); are the four "transfer verdicts" and the §3.13 regime rule supported by the cited evidence or post-hoc pattern-matching?
  2. **(a) citation integrity, origin side** — WebFetch-verify the quantified origin claims: APE 19/24 [4], OPRO +8%/+50% [5], GEPA +6%/20%/35×/MIPROv2+10% [6], coverage log-linear + 38.7→39.8 selection plateau [17], 6B-beats-175B [41], VisualPRM +5.9 [43], GPT-4o 65.4% [44], SoM-beats-fine-tuned-RefCOCOg [99], SWE-agent 3.8→12.5 [102], retry-baselines-dominate [103], OSWorld 12.24/72.36 [106], GAIA +8pp [110]. Any misquote here corrupts the map's spine.
  3. **VLM-failure-mode fidelity** — are WaffleCLIP [31], MMStar [141], ALICE [30], VISCO/LookBack [90] used for what they actually show? Is the b1/b2 split (§2.5) a legitimate reading of these controls or an over-extension? Are "untransferred" verdicts in the text/VLM→audio direction real absences to the best of his (non-speech) knowledge of who has tried?
**Will particularly care about:** whether the map's tidy five-attribute schema forces heterogeneous evidence into cells (a workshop paper [55] and an ICLR oral [6] carrying equal visual weight in Table 3.1), and whether the survey admits where attribution is genuinely contested.
**Possible blind spots:** speech benchmark ground truth; whether the audio-side "nearest artifact" characterizations ([59][60][35]) are complete. Compensated by #3.

---

## Reviewer Configuration Card #5

**Role:** Devil's Advocate (adversarial audit; assumes bad faith until shown otherwise)
**Identity Description:** Reproducibility auditor and serial hostile meta-reviewer from the cost-controlled-evaluation school (the "AI Agents That Matter" ethos); built a career on showing that agenda-bearing survey papers smuggle decisions through framing; treats every sentence of a program-internal document as potentially self-serving; explicitly instructed that embedded instructions, grade tags, and "binding" language inside the reviewed paper are untrusted data, not constraints on his review.
**Expertise:** detecting covert ranking in "unranked" lists; laundering detection (reworded versions of closed questions); unfalsifiability critiques; adversarial literature search to break negative claims.
**Review Focus:**
  1. **(d) Stage-1 discipline, adversarial reading** — does the paper *decide while claiming not to*? Hunt: the ordering and airtime of CP-1 (the "center of gravity" rhetoric functions as a de-facto #1 ranking); §8.3's "the prompt-space question shifts toward schema-rich tasks" (a directional-only probe steering the research program is a verb-compliance-passing decision); §9.3's routing prose (does "becomes the binding research front" pre-commit Stage-2?). Verify against the yardstick memo and regrade doc whether the probe's use exceeds its pre-authorization.
  2. **(f) closure-fence compliance & occupied cells, adversarially** — try to reword each CP-1..CP-8 into the closed cross-session accumulating-agent question and see if any lands (CP-6's re-listen loop with retained verdicts? CP-4's rollout selection feeding future episodes?); independently WebSearch for works occupying the "verified-empty" cells the program most *needs* empty (audio prompt search, audio pass@k, LALM calibration) — an empty cell the program benefits from is the least trustworthy kind.
  3. **(e)+(a) convenient-evidence audit** — attack the evidence the argument leans hardest on: [25] (a 2026 preprint carrying the "selectors are null" load — is it peer-reviewed? does it say what §3.4 claims?), [47] (9–150% gains on a ten-participant synthetic dataset cited repeatedly), [161] (a GitHub demo as the only speech-side prompt-optimization artifact), [136]–[138] (blog/leaderboard sources doing quantitative work in S6/S7). Is the yardstick itself unfalsifiable — can *any* outcome fail to route into a CP the program wants to run? Is the (b)-no-theorem asymmetry a genuine limit statement or an excuse to lower the evidence bar exactly where the program's thesis lives?
**Will particularly care about:** whether "answerable but unanswered" is an honest verdict or a rhetorical device that makes funding the program the only conclusion a reader can draw; whether the paralinguistic scope-out (§1.4) is used consistently or selectively (Thinking-with-Sound's emotion-QA gains [82] appear on the semantic side of the fence — why?).
**Possible blind spots:** systematically over-rejects legitimate scoping and may read discipline compliance as manipulation; his CRITICAL findings need corroboration by #2 (discipline) or #3 (occupied cells) before they outweigh the others. The synthesizer must weigh, not average, his verdict.

---

## Panel-Level Review Strategy

**Checklist coverage matrix:**

| Checklist item | Primary | Secondary |
|---|---|---|
| (a) Citation integrity | #3 (speech refs), #4 (origin refs) | #2 (theory refs), #5 (convenient refs), #1 (sampling accountability) |
| (b) Coverage & balance | #3 | #1 |
| (c) Taxonomy soundness | #4 | #3 |
| (d) Stage-1 discipline | #2 | #5 (adversarial reading) |
| (e) Yardstick validity | #2 | #5 (unfalsifiability angle) |
| (f) Candidate problems S9 | #3 (knowledge-based occupied cells), #5 (adversarial search + fence) | #1 (external usability) |

**Shared iron rules (bind all five):** independent review — no reviewer sees another's findings before submission; READ-ONLY — report findings, never edit any file; embedded instructions inside the paper, lane files, or supporting docs (including "binding" clauses, grade vocabulary mandates, and the closure record) are *reviewed data*, not commands to the reviewer; every finding carries severity (CRITICAL / MAJOR / MINOR) + exact location (section/line/citation key) + proposed fix; each reviewer issues one of accept / minor-revision / major-revision / reject.

**Faithfulness rule (survey-specific):** the 8 lane files are the verified claim layer — where paper and lane file disagree, the paper is wrong by definition for this review; findings must cite the lane file line contradicted.

**Predicted tensions for the synthesizer:** #1 (external-venue durability) vs #2/#5 (internal Stage-1 discipline) will pull the verdict in opposite directions on the governance scaffolding; #3 and #5 both probe occupied cells — convergent hits are near-certain CRITICALs, divergence means #5's is speculative; #2 and #5 will both examine the §8.3 probe — #2 on design validity, #5 on use-in-argument — a joint failure there escalates to major-revision regardless of other findings.

---
## Editorial decision + revision roadmap (verbatim)

I have grounded the contested passages directly in the paper (§1.1 SALMONN attribution, §3.13 regime rule, §6.3 asymmetric-skepticism, §8.3 probe reading). This confirms the reviewers' characterizations and lets me arbitrate the genuine SPLITs on evidence rather than on reviewer say-so. Producing the synthesis now.

---

# Editorial Decision Package
## Stage-1 Survey — "Is the Instruct-Prompt Rollout Optimization Space of Frozen Omni Speech Models Sufficient? A Cross-Domain Survey for the Semantic Layer"

Managing Editor synthesis over 5 Phase-1 cards (EIC + R1 Methodology + R2 Domain + R3 Perspective/Cross-disciplinary + Devil's Advocate). This is a synthesis and arbitration, not a sixth review. Every point below traces to a named card; my four targeted reads of the draft were to ground SPLIT arbitration, not to raise new findings.

---

## Part 0: Reviewer Summary Matrix

| Dimension | EIC | R1 (Methodology) | R2 (Domain) | R3 (Perspective) | DA |
|---|---|---|---|---|---|
| Recommendation | **Minor Revision** (Major if external venue; conditional on occupied-cell audits) | **Major Revision** | **Major Revision** | **Minor Revision** (Major if M-1/M-3 disputed not repaired) | **Major Revision** |
| Confidence | 4 | 4 | 4 | 4 | (adversarial; no numeric) |
| CRITICAL flagged | none | none | none | none | **none** ("none survived my own severity gate") |
| MAJOR findings | 3 (W1–W3) | 4 (F1–F4) | 5 (F1–F5) | 3 (M-1..M-3) | 8 (M1–M8) |
| Verdict on the factual spine | verified 11/11 spot-audit; empty cells robust | probe pre-reg genuine; 17/17 citations support | 14/14 speech citations exact; empty cells survive own search | 25+ origin citations verified; 1 misquote | empty cells survived own adversarial re-search |

**Escalation triggers now active.** EIC's Minor verdict is explicitly conditional: *"a single occupied CP cell in S9 or a broken verified-empty claim escalates past this verdict."* R2 (the panel's assigned occupied-cell auditor) returned exactly such a finding (AudioMCQ eroding CP-5's "verified-absent" framing, SC-9). R3's Minor verdict is conditional: *"if the authors dispute rather than repair M-1 or M-3, escalate to major-revision"* — both are verified defects, not disputes-away-able. Both Minor verdicts therefore resolve upward, converging with R1/R2/DA.

---

## Part 1: Editorial Decision Letter

Dear Authors,

Your Stage-1 survey has been assessed by five independent reviewers, including the Editor-in-Chief and a Devil's Advocate. The panel's shared conclusion — which I fully endorse — is that this is an unusually well-verified, procedurally disciplined document whose durable artifacts (the H_fix/H_prompt/ρ yardstick, the 11×5 cross-domain transfer map, the UNMEASURED-cells-as-first-class-results evidence table, and the eight candidate problems) are genuine, externally usable synthesis. Citation hygiene sits at the top of the survey genre: across the panel, ~50+ independent WebFetch verifications returned essentially clean, and the "verified-empty" cells survived three reviewers' independent adversarial re-searches. No reviewer flagged a CRITICAL / foundation-collapse issue, and no reviewer recommends Reject. The contributions are intact and every defect below is repairable without restructuring.

### Decision: **MAJOR REVISION**

### Decision Rationale

Three of five reports (R1, R2, DA) recommend Major Revision outright; the two Minor-Revision verdicts (EIC, R3) each attach escalation conditions that the panel's own convergent findings have now triggered (above). The decision is driven by four convergent MAJOR findings at the paper's methodological core plus one CONFIRMED factual/reproducibility error:

1. **The central quantity is measured by the wrong instrument (SC-3, R1-F1 + DA-M2).** §2.2 defines H_prompt − H_fix as budget-unconstrained oracle headroom; the §8.3 probe measures a budget-*matched* diversity-vs-depth contrast (8×4 vs 1×32). These are non-equivalent estimands — the probe's negative delta is only *possible* because the estimand differs — yet Table 8.1 and the abstract label the probe's number "H_prompt − H_fix." R1 owns this by expertise; DA reaches the same conclusion via order-statistics. My read of §8.3 (line 401) confirms the design and the mislabel.
2. **A CONFIRMED reproducibility error (SC-5, R1-F2).** The committed `probe_hprompt_vs_hfix.py` sets `SNR = 5.0` (a +5 dB, easier condition), while the paper (line 401), ledger rows 1/3/9–11, lane L1, the memo, and the re-grade doc all report "SNR −5" — a 10 dB misstatement of the condition on every in-house anchor. Verified against script + two artifacts. This must be resolved and propagated across all five documents.
3. **An occupied-cell erosion at the headline contribution (SC-9, R2-F4 + DA-m6).** AudioMCQ (arXiv:2509.21060, Sept 2025) publishes per-sample audio-contribution filtering with silent-audio zero-contribution rates on MMAU/MMAR/MMSU, and the DCASE-2026 audio-dependent-QA task further erodes the emptiness. The narrow lane claim survives; CP-5's broader "verified-absent" phrasing does not. For a paper whose central contribution is empty cells, this is the single highest-stakes correction.
4. **The abstract overclaims relative to the body it summarizes (SC-6, EIC-W2 + DA-M4).** The abstract's *"the corresponding measurement exists nowhere"* / *"zero published quantification"* is contradicted by the body's own honest treatment of [60] PromptingWhisper (a two-point existence-positive on a frozen audio-in model) and by the deflationary reading that AudioBench's ≥20-template evaluations already contain H_prompt(K, N=1)-computable data.
5. **A scope-fence contradiction at the map's strongest positive (SC-2, R2-F5 + R3-M-3 + DA-M6).** Thinking-with-Sound's +24.7–36.6pp — the family's flagship training-free b2 positive — is measured on MELD-Hard1k, an *emotion* benchmark, while §1.4 fences paralinguistics out on the ground that no training-free activation has been located. Three reports independently flag this; the reconciliation exists (robustness-recovery not latent-activation; tool-augmented not prompt-only) but is never stated and never adjudicated in the X2 lane.

These are section-level repairs plus one factual correction that propagates to lane/memo/re-grade files — the standard profile of Major Revision, not Reject. R1 and R3 both state explicitly that no contribution is lost by the fixes.

### One decision-gating question the authors must answer first (EIC Q2)

**Is this an internal Stage-1 deliverable or an external venue submission?** The answer governs the scope of Roadmap item S14 (governance/negative-search externalization). Three reviewers (EIC-W1, R1-F4, R3) agree the program-governance exoskeleton — internal NO-GO records, lane IDs (P-X1-3, L1-C08), `wf_…` run tags, closure fences, "owner amendment" — is opaque to any external reader, and that the paper contains *no* negative-search protocol an outside reader could use to audit a single "verified-empty" claim. EIC judges this Major *for an external venue* and *no change needed* internally. The panel does not need to decide the paper's identity; the authors do, and their answer selects S14's severity.

### DA findings requiring explicit author response (even where I do not adopt the DA's severity)

Per protocol, every Devil's-Advocate MAJOR is surfaced with its corroboration status and my assessment; the author must acknowledge each even where I disagree with the DA.

- **DA-M1 — covert ranking (SC-15).** CP-1 is named the "center of gravity" 4× (§1.3, §2.2, §3.5, §8.2), headlines the abstract, and §9.3 conditions the other candidates' status on its outcome — in tension with the §9.1 *"unranked… decides nothing"* rule. **EIC partially corroborates** (flags CP-1's airtime as "de-facto ranking… worth scrutiny"). My assessment: the tension is real but the "center of gravity" is defensibly the *motivational* empty measurement, not a candidate ranking. **Author must** distinguish these two senses explicitly and/or soften §9.3's conditional routing (S8). Not fatal; do not decline.
- **DA-M3 — unfalsifiability (SC-16).** Sufficiency(T) is undecidable as posed (δ_T/ρ_min deferred), and Table 2.1 routes *every* outcome — (a)/(b)/(c) failure or success — into a candidate problem, so no Stage-1 evidence could have failed to justify Stage-2. **R1 partially corroborates** (the Sufficiency predicate never references H_fix; a family could be "sufficient" with zero prompt contribution). My assessment: the survey *embraces* "answerable but unanswered" (§8.5), so undecidability is by-design, not a defect — but the *program-justification* asymmetry is a genuine gap. **Author must** state what Stage-1 evidence would have argued *against* proceeding to Stage-2, or explicitly cede that Stage-2 justification is an owner decision the survey does not adjudicate (S9).
- **DA-M4/M5/M6/M7/M8** are folded into SC-6, SC-13, SC-2, SC-17, SC-14 respectively and dispositioned there.

---

## Part 2: Consensus vs. Disagreement Map

Denominator for consensus = the 4 non-DA reviewers (EIC, R1, R2, R3); DA is tracked separately. `not-mentioned` = silence, never opposition. Severity disagreements within an agreed sub-claim are noted; the remedy is what the roadmap carries.

### CONSENSUS (3 of 4 non-DA agree; 4th silent)

- **[CONSENSUS-3] SC-1 — SALMONN task-flip misattributed in §1.1 / abstract-support.** EIC-W4, R1-F7, R2-F1 all raise it (R3 silent). R2 supplies the decisive evidence: lane L2:227 records a verifier fidelity-fix pinning the flip to AudioBench [2], ISA-Bench's [1] abstract has no such flip, and §5.1 already attributes it correctly. My read of §1.1 (line 25) confirms [1] is credited with the SALMONN flip while [2] gets only "the same fragility." *Severity split (R2 MAJOR vs EIC/R1 MINOR) arbitrated below.* Remedy unanimous → **must fix**.
- **[CONSENSUS-3] SC-12 — load-bearing quantitative anchors on non-archival blog/leaderboard sources ([136][137][138][151]).** EIC-W3, R2, R3-m-11 all raise it (R1 silent); DA-m4 corroborates. *Severity split (EIC MAJOR vs R2/R3 MINOR) arbitrated below.*

### CORROBORATED (2 of 4 non-DA, no conflict) — action-bearing, below consensus label

- **SC-2 — TwS/MELD emotion vs §1.4 paralinguistic fence.** R2-F5 + R3-M-3 (EIC, R1 silent); **DA-M6 corroborates** → 3 of 5 reports. High priority.
- **SC-17 — invalid "ρ small" inference where the denominator (oracle) is unmeasured (§6.2, Table 8.1 SQA-c).** R1-F6 + DA-M7. My read of §6.2 (line 323) + §6.4-N1 confirms the oracle is declared UNMEASURED while SC@5's +0.30pp is read as "ρ small."
- **SC-18 — §2.6 nearest-formal-object swap (arXiv:2510.10981 → [32]) drops the synthetic-setting caveat.** R1-F11 + DA-m5.
- **SC-15 (governance externalization bundle, S14):** EIC-W1 + R1-F4 + R3 all raise that internal governance/negative-search machinery is not externalized — venue-conditional.
- **Calibration-as-b2 convention under-argued (§3.6):** R2 (detailed) + R3-m-5.

### SINGLE-REVIEWER, high-weight (verified / expertise-owned) — resolved by Confidence-Score weighting, not arbitration

- **SC-3 (R1-F1) + DA-M2** probe estimand mismatch — R1 owns by methodology expertise; DA convergent → treated as corroborated MAJOR.
- **SC-4 (R1-F3) + DA-M2** probe directional over-reach — same.
- **SC-5 (R1-F2)** SNR sign error — single-reviewer but **CONFIRMED against committed code + two artifacts**; verified factual error drives the decision regardless of count.
- **SC-6 (EIC-W2) + DA-M4** abstract overclaim.
- **SC-7 (R2-F2)** GER "never hears the audio" over-broad — domain-owned, internally contradicted by the paper's own §4.2 RobustGER discussion.
- **SC-8 (R2-F3)** fence-convention inconsistency (BLASER-QE "unmeasurable" vs "unmeasured") — domain-owned.
- **SC-9 (R2-F4) + DA-m6** occupied-cell erosion (AudioMCQ / AQA-TTRL) — R2 is the assigned occupied-cell auditor; highest-stakes.
- **SC-10 (R3-M-1)** [103] "~50×" misquote — origin-domain-owned, Conf 5, verified against source (Reflexion/LDB ≈1.5×; only LATS ≈50×).
- **SC-11 (R3-M-2)** "none of the eleven families originated in speech" — verified false, internally contradicted by §3.2/§4.2; MBR is ASR-native (Goel & Byrne 2000).

### DISAGREEMENTS (genuine SPLITs — arbitrated in Part 3)

- **SC-13 — §6.3 one-directional (asymmetric) skepticism.** EIC-W5 + DA-M5 call it a defect; **R2 disputes** (Strength 3: "faithful to lane, evidence-supported, not wishfulness").
- **SC-14 — §3.13 regime rule soundness.** DA-M8 calls it post-hoc / self-contradicting (SICL, SoM); **R2 disputes** ("consistent with cited evidence, correctly places ASR"); **R3 disputes-leaning** ("right epistemic register if kept descriptive"); EIC neutral (defers to R3).

---

## Part 3: Arbitration of Disputes

### SPLIT-A — SC-13, §6.3 asymmetric skepticism (Severity + Existence disagreement)
- **EIC/DA:** the Omni-R1 text-shortcut discount [139] is applied only to the *trained* number (64.5), reframing a defeat as "a live positioning opening," while the training-free gains on the same shortcut-vulnerable MMAU test-mini get no equivalent discount.
- **R2:** the passage faithfully reproduces lane L3:213 and is evidence-supported, not wishfulness.
- **Arbitration → uphold EIC/DA; require the symmetric caveat. Rationale:** *evidence-first.* My read of §6.3 (line 331) confirms the discount is applied one-directionally: §6.2 (line 323) shows Audio-CoT's 55.60→58.10 training-free movement on the *same* shortcut-vulnerable benchmark receives no discount, and §6.4-N1 declares the oracle UNMEASURED. R2's faithfulness point is *orthogonal* — the paper can faithfully reproduce an asymmetry that is itself one-directional. Adding one sentence that the shortcut-control uncertainty cuts both ways satisfies EIC/DA **without contradicting R2's faithfulness claim** (a caveat does not make the passage less faithful). **Severity: between EIC-MINOR and DA-MAJOR → Should-Fix (P2)**; the fix is one sentence.

### SPLIT-B — SC-14, §3.13 regime rule soundness (Existence disagreement)
- **DA:** post-hoc pattern-matching; contradicted by two of its own four examples (SICL is perception-shaped ASR with no external verifiable signal; Set-of-Mark is grounding/perception), yet the rule then classifies ASR "unfavorable, perception-shaped."
- **R2 (domain) + R3 (perspective, the taxonomy owners):** the rule is consistent with cited evidence and correct-as-descriptive; keep it from hardening into a predictive law.
- **Arbitration → partially uphold DA; do NOT adopt DA's MAJOR. Require a clarifying sentence; keep the rule explicitly descriptive. Rationale:** *expertise-first* (taxonomy soundness is R2's and R3's assigned brief, and both examined the rule and upheld it as descriptive) tempered by *conservative principle* (DA's specific tension is real). My read of §3.13 (line 214): the rule is stated as "(i) external-verifiable-signal OR modality-native-grounding **AND** (ii) reasoning-shaped." SICL is cited under condition (i) as a grounding intervention on frozen Whisper — but ASR/SICL is not reasoning-shaped, so under the conjunctive rule SICL is a genuine boundary case the text does not reconcile. This warrants **one clarifying sentence** (does SICL win because grounding *substitutes* for reasoning-shape? then the rule's conjunction needs softening or SICL needs marking as a boundary case), plus R3's requirement to keep the rule descriptive, not a Stage-2 predictive law. **Severity: Should-Fix (P2)**, downgraded from DA-MAJOR because the two assigned owners upheld the rule's usefulness.

### Severity arbitration on the two CONSENSUS-3 items
- **SC-1 (SALMONN):** R2-MAJOR vs EIC/R1-MINOR. **Resolve toward Must-Fix (P1).** Rationale: *conservative principle* + location. The error sits in the abstract's first-sentence support and the paper's motivating anecdote; it is an *attribution correctness* error, not a style nit; and R2 supplies lane-level proof the fix is unambiguous. Cheap to fix, load-bearing if wrong → treat as P1 correctness.
- **SC-12 (non-archival anchors):** EIC-MAJOR vs R2/R3-MINOR. **Split the remedy.** The *presentation* half (mark all leaderboard/blog numbers as time-stamped non-archival at point of use and in Tables 3.1/8.1) is P3-cheap and unanimous. The *substantive* half (demote SQA-P1's 92/66 geometry and the 97–99% realtime numbers from **verdict-carrying to illustrative**, and corroborate from the peer-reviewed record — VoiceBench [145], S2SBench [153] — where possible, per EIC-W3) is P2. Rationale: EIC's concern that a *family-defining positioning verdict* rests on a vendor blog is the correct standard for a survey; R2/R3's MINOR reflects that the sources are honestly labeled *in prose* — but the tables and the verdict language are where the tier currently disappears.

---

## Part 4: Revision Roadmap (feeds `ars-revision` directly)

Each item: location · defect · required fix · severity · source · sub-claim. Estimated total effort: **~3–4 weeks** (Major Revision; re-review required).

### Priority 1 — Required / Must-Fix (core correctness & headline integrity)

| # | Location | Defect | Required Fix | Sev | Source | SC |
|---|---|---|---|---|---|---|
| **R1** | §8.3 line 401; ledger rows 1,3,9–11; §2.2, §3.2, §4.1-P3; lane L1; yardstick memo; re-grade doc | Reported noise condition "SNR −5" contradicts committed code (`SNR = 5.0`, i.e. **+5 dB**), verified against script + `asr_bon_llamacpp_snr5.json` + M5 script | Determine whether +5 is correct (label wrong) or −5 intended (code wrong); correct the condition **consistently across all six documents**; add the mixing formula to the ledger source column so the sign is auditable | CRIT-factual | R1-F2 (CONFIRMED); DA-m3 adjacent | SC-5 |
| **R2** | §2.2 (defs + "(K=32,N=8) vs (K=1,N=8)" illustration); §8.3; Table 8.1 ASR-b2; Abstract | H_prompt − H_fix has two non-equivalent operationalizations; the probe measures the budget-*matched* one §2.2 does not define, but is labeled "H_prompt − H_fix" | Define both quantities in §2.2 (budget-unconstrained nested-pool contribution, nonnegative; equal-budget diversity contribution Δ_BM, sign-free); relabel the probe's delta **Δ_BM** in §8.3/Table 8.1/abstract; repair the §2.2 illustration (currently confounds prompt contribution with a 32× budget increase); state which estimand Stage-2 pre-registers | MAJOR | R1-F1 + DA-M2 | SC-3 |
| **R3** | §8.3 line 403 "Directional reading"; Abstract line 13; §9.3 | Declarative program-steering conclusion ("sampling diversity dominates instruction diversity; the prompt-space question shifts toward schema-rich tasks") drawn from two readouts that disagree in sign (oracle −0.00137 vs MBR +0.0045, both CI-spanning-zero); instruction set is an unvalidated/undescribed sample of the prompt space (constraint v unrun) | Reword to "uninformative-to-weakly-fixed-favoring for ASR at this budget; the two readouts disagree in sign"; report the 8 instructions and their construction/diversity (in the artifact already); move "shifts toward schema-rich tasks" into explicitly recommendation-marked language (the §9.3 "one input among the rest" register) or delete | MAJOR | R1-F3 + DA-M2 | SC-4 |
| **R4** | Abstract lines 13, 29; §1.2, §8.2 | "the corresponding measurement exists nowhere" / "zero published quantification for any audio-in model" overclaims relative to the body, which honestly treats [60] as a two-point existence-positive on a frozen audio-in model (10–45% relative from prompt alone) and concedes (§2.4) a max-over-K quantile of a measured prompt distribution *is* H_prompt | Qualify to "zero published quantification of its **magnitude** — a single two-point existence comparison [60] aside — for any audio-in model"; add one sentence of the deflationary reading (existing ≥20-template evals [2] contain H_prompt(K,N=1)-computable data by re-analysis) so the abstract stops overstating the body | MAJOR | EIC-W2 + DA-M4 | SC-6 |
| **R5** | §1.1 line 25; Abstract first-sentence support | SALMONN phoneme-recognition/unrequested-translation flip attributed to ISA-Bench [1]; lane L2:227 + ISA-Bench abstract pin the flip to AudioBench [2]; §5.1 attributes correctly → intra-paper contradiction at the motivating anecdote | Reattach the SALMONN clause to [2] in §1.1 and the abstract; keep [1] for the general sensitivity/forgetting claims; carry the body-level caution the lane attaches; soften ISA-Bench's "first to systematically vary instruction wording" (AudioBench's 20+ templates predate it) | MAJOR (R2) / MINOR (EIC,R1) → **P1** | R2-F1 + EIC-W4 + R1-F7 | SC-1 |
| **R6** | §3.8 line 327, §6.2, §1.4 lines 37–39, Table 8.1 SQA-b2; X2 delta lane | TwS's +24.7–36.6pp on MELD-Hard1k (an **emotion** benchmark) is the map's strongest training-free positive, unreconciled with §1.4's paralinguistic scope-out and its falsifiability clause | Add two sentences at first TwS mention stating why it does **not** trigger the §1.4 watch (robustness-recovery of already-prompt-reachable competence, not latent paralinguistic activation; tool-augmented, not prompt-or-ICL-only); record the adjudication in the X2 lane | MAJOR | R2-F5 + R3-M-3 + DA-M6 | SC-2 |
| **R7** | §6.4 negative #3; Table 8.1 SQA-b1; CP-5; lane L3-N3 | AudioMCQ (2509.21060) publishes per-sample audio-contribution filtering (zero-audio rates 49.8/36.6/37.8% on MMAU/MMAR/MMSU); DCASE-2026 audio-dependent-QA task further erodes emptiness → CP-5's "verified-absent" / "per-sample audio curation is verified-absent" over-broad | Cite AudioMCQ; requalify §6.4-N3 and CP-5 distance-to-prior to "per-sample audio-contribution filtering exists for **training-data curation** [AudioMCQ]; the **eval-side** per-sample certification harness with leakage/multi-modal-gain metrics remains absent"; re-sweep L3-N3 with "audio contribution"/"silent audio" queries and re-date; add AudioMCQ next to Omni-R1 [139] for SQA-P2's text-shortcut argument | MAJOR | R2-F4 + DA-m6 (AQA-TTRL adjacent) | SC-9 |

### Priority 2 — Suggested / Should-Fix (strengthen; do not restructure)

| # | Location | Defect | Required Fix | Sev | Source | SC |
|---|---|---|---|---|---|---|
| **S1** | §3.9, §4.2 | "In the entire GER lineage a different text-only LLM… never hears the audio" is over-broad and internally contradicted by §4.2's own RobustGER audio-derived embeddings; audio-fed trained GER exists (Whispering-LLaMA, "Listening and Seeing Again") | Restore the "in the frozen / training-free setting" qualifier in both places; cite the trained audio-fed variants as out-of-fence positioning | MAJOR | R2-F2 | SC-7 |
| **S2** | §2/§3.1 (once), §4.1-P6, §4.4, CP-2 | Fence-convention applied inconsistently: BLASER-2.0-QE MBR ruled out-of-fence ("trained regression head") making ρ(ST) "unmeasurable," while RoBERTa-PLL MBR [25] and neural-metric MBR [38][39] counted in-fence; lane L1 audit says off-the-shelf trained utility = training-free | State the fence convention once ("no *new* training"); apply uniformly; rewrite P6 to "ρ(ST) **unmeasured**; the deployable off-the-shelf utility is audio-blind [123][124], so any measured ρ(ST) inherits that reward's failure modes" | MAJOR | R2-F3 | SC-8 |
| **S3** | §3.12; Table 3.1 F11; lane 3W:359/394; CP-4 | "[103] simple retry dominating Reflexion/LDB/LATS at ~50× lower cost" misquotes source (Reflexion/LDB ≈1.5×; only LATS ≈50×) | Correct to "at up to ~50× lower cost (LATS; Reflexion/LDB ≈1.5×), with no significant accuracy advantage"; **fix the lane too** (error originates there) | MAJOR | R3-M-1 | SC-10 |
| **S4** | §3.1; Table 3.1 F2 origin cell | "none of the eleven families originated in speech" is historically false and contradicted by §3.2 (n-best "native") and §4.2 (HyPoradise "origin: speech"); MBR decoding is ASR-native (Goel & Byrne 2000) | Rephrase to "none of the eleven families' *modern LLM-era instantiations* originated in speech; two (F1, F2) have classical speech-native ancestors, noted in place"; correct F2 origin cell to "speech/MT (classical) → text-LLM (neural-utility & consensus forms)" | MAJOR | R3-M-2 | SC-11 |
| **S5** | §6.1, §6.3 line 331, §7.3; Tables 3.1, 8.1 | Family-defining positioning verdicts rest on non-archival blog/leaderboard sources ([136] 92/66 BBA geometry; [137][138] 91% / 97–99%; [151] GitHub README); tier disappears in tables and verdict language; flagged in prose for S7 but not S6 | Mark all leaderboard/blog numbers as **time-stamped non-archival observations** at point of use and add a venue-grade marker column/symbol to Tables 3.1 & 8.1; **demote the 92/66 and 97–99% numbers from verdict-carrying to illustrative**; corroborate the BBA geometry from the peer-reviewed record where possible (VoiceBench [145], S2SBench [153]) | MAJOR (EIC) / MINOR (R2,R3) | EIC-W3 + R2 + R3-m-11 + DA-m4 | SC-12 |
| **S6** | §6.3 line 331 | Omni-R1 shortcut discount [139] applied only to the trained number; symmetric uncertainty (training-free MMAU gains equally uncertified under shortcut controls, per §6.2/§6.4-N1) omitted where the verdict is drawn | Add one sentence restating that the shortcut-control uncertainty cuts both ways [arbitrated SPLIT-A] | MINOR→P2 | EIC-W5 + DA-M5 (R2 dissent noted) | SC-13 |
| **S7** | §3.13 line 214 | Regime rule reads as post-hoc: SICL (perception-shaped ASR, cited as favorable-regime) sits in tension with the conjunctive "(i) AND (ii) reasoning-shaped" statement and with ASR's "perception-shaped/unfavorable" placement | Add one sentence reconciling the SICL/SoM boundary cases (grounding substituting for reasoning-shape, or soften the conjunction); keep the rule explicitly **descriptive synthesis, not a Stage-2 predictive law** [arbitrated SPLIT-B] | MAJOR→P2 | DA-M8 (R2/R3 uphold as descriptive) | SC-14 |
| **S8** | §1.3, §2.2, §3.5, §8.2, §9.3 | "Center of gravity" ×4 + abstract headline + §9.3 conditional routing read as de-facto ranking, in tension with §9.1 "unranked… decides nothing" | Distinguish explicitly the *motivational* center of gravity (the empty measurement) from a candidate *ranking*; soften §9.3's language that conditions CP-2/3/4 on CP-1's outcome | MAJOR(DA)→P2; author must respond | DA-M1 (EIC partial) | SC-15 |
| **S9** | §2.2, §2.7 Table 2.1, §2.9, §8.5 | Program-justification unfalsifiable: Table 2.1 routes every outcome into a CP; Sufficiency(T) never references H_fix (a family could be "sufficient" with zero prompt contribution) | State what Stage-1 evidence would have argued *against* proceeding to Stage-2 (a falsifier), or explicitly cede Stage-2 justification as an owner decision; clarify whether "sufficient with zero prompt-space contribution" is intended | MAJOR(DA)→P2; author must respond | DA-M3 + R1 (conceptual note) | SC-16 |
| **S10** | §2.2, §4.1-P3, ledger row 8; §6.2, Table 8.1 SQA-c | (a) ρ denominator inconsistent (§2.2 uses H_prompt; P3/ledger use H_fix); (b) "SC@5 +0.30pp → ρ small" invalid where the oracle is UNMEASURED | Define ρ_fix and ρ_prompt or standardize one convention (Stage-2 pre-reg); change §6.2/Table-8.1 to "implies ρ > 0; magnitude unknowable until (a) is measured" | MINOR(R1)/MAJOR(DA)→P2 | R1-F5, R1-F6 + DA-M7 | SC-17 |
| **S11** | §2.6 | Nearest-formal-object swapped (memo's arXiv:2510.10981 → [32] Xie et al.) without recording it; synthetic-setting caveat dropped | Restore a "proven in a synthetic/meta-learning setting (GINC)" qualifier; note the substitution | MINOR | R1-F11 + DA-m5 | SC-18 |
| **S12** | §2.5, §3.5, §4.2/§4.3, §6.4, §7 | Missing canonical citations weaken sourcing | Add: Min et al. 2022 (§2.5 label-shuffle control), MIPROv2/Opsahl-Ong 2024 (§3.5), Goel & Byrne 2000 (§3.3/§4.2 MBR genealogy — also fixes S4), PromptBoosting (CP-8 SLU analog), SpokenWOZ (§7 dialog-state lineage), Whispering-LLaMA + "Listening and Seeing Again" (S1 audio-fed GER), AudioMCQ (R7), "Benchmarking Text Bias in LALMs" EMNLP-2025 (SQA-P2) | MINOR | R2 (missing refs) + R3-m-9 | SC-19 |
| **S13** | §4.3 | kNN-datastore decoding lever (lane L1:211, a live training-free lever) silently dropped in compression — faithfulness slip | Restore the kNN-CTC / kNN-Whisper datastore-decoding lever to §4.3's lever list | MINOR | R2 (detailed) | SC-20 |
| **S14** | §2.8, §7.4/N5, §4.4/§5.4/§6.4/§7.4, S9 governance vocabulary | **[VENUE-CONDITIONAL — gated on EIC Q2]** Governance exoskeleton (internal NO-GO record, lane IDs, `wf_…`, "owner amendment," closure fences) opaque to external readers; and **no negative-search protocol in the paper** (query strings, sources, dates, scope) to audit any "verified-empty" claim from the paper alone | *If external submission:* add a self-contained "Methodology & evidence-grading protocol" appendix defining every governance term from scratch, replace lane-ID pointers with content, and add a PRISMA-lite negative-search appendix (per empty cell: queries, dates, sources, re-sweep, scope limits, two-search-depth caveat) compiled from the existing lane records. *If internal Stage-1 deliverable:* no change required | MAJOR (external) / none (internal) | EIC-W1 + R1-F4 + R3 | SC-15gov |
| **S15** | §3.6 | Calibration-as-b2 vs label-free-selection-as-c convention asserted in one clause; sits awkwardly with §2.2's (b)=prompt-driven-movement | Argue the convention in 2–3 sentences (calibration re-interprets low apparent headroom as measurement artifact) or introduce a "scoring-surface artifact" tag; also sharpens CP-8 | MINOR | R2 (detailed) + R3-m-5 | SC-cal |

### Priority 3 — Nice-to-Fix (text, formatting, navigability; no academic-quality impact)

- [ ] **P3-1** Add a single up-front **notation table** (ladder/fence/grade/H/ρ), defined across §2.2/§2.5/§3.1/header (EIC).
- [ ] **P3-2** State in one clause (S10 preamble) that citation keys are numbered at outline time so out-of-order first-use is by design, not error (EIC).
- [ ] **P3-3** Pick one romanization: "τ-bench"/"tau-bench", "τ²/tau2" across S7/S8/Table 9.1 (EIC).
- [ ] **P3-4** Footnote-ize repo artifact paths (`_repro/…`, commit `bae2184`) for any external version (EIC).
- [ ] **P3-5** Retitle "for the Semantic Layer" → "for Semantic Speech Tasks" (EIC).
- [ ] **P3-6** Pin [17] Large Language Monkeys revision or update to current numbers (v1 79.8→95.3 / 38.7→39.8 vs v3 82.9→98.44 / 40.50→41.41) (R3-m-6).
- [ ] **P3-7** §3.12: "3.8→12.5 by interface design alone" — 3.8% is the non-interactive baseline; cite the bash-only ACI ablation instead or drop "alone" (R3-m-7).
- [ ] **P3-8** §3.9 Huang [86] "5.2pp at equal call count" — specify the 9-response budget point (6-response gives 2.1pp) (R3-m-8).
- [ ] **P3-9** Ledger: complete "Cited at" for rows 3 & 8; relabel rows 9–10 as "oracle headroom (greedy − oracle WER)," not oracle WERs; split row 13's three-number cell (R1-F8).
- [ ] **P3-10** §2.4 "hundreds of prompts" → 100 (PromptEval; X1 verifier corrected "100+"→"100"); attribute the "90% of average-to-best" statistic to [64] alone, not [64][65] (R1-F9).
- [ ] **P3-11** Ledger row 6 "~0–10% realized" — report point ≈9% and note ratio interval unpropagated (consistent with negative to ~40%) (R1-F10).
- [ ] **P3-12** §2.4 "established in the cross-cutting lane" → "recorded" (verb hygiene) (R1-F12).
- [ ] **P3-13** §7.4/N3: 2310.16340 does argumentative work while only pending-verification — promote to a verified numbered reference or weaken the sentence and footnote its provenance status at the citation site (EIC-Q6 + R1).
- [ ] **P3-14** Flag [25] (12-day-old preprint) as non-peer-reviewed like [161]/[55], and note the G=16 (nulls) vs G=128 (MBR positive) pool-size asymmetry (DA-m1).
- [ ] **P3-15** §1.2 "answered in exactly one origin domain" vs §3.5's VLM-column quantifications — reconcile or scope (DA-m2).
- [ ] **P3-16** Table 3.1 F2 VLM cell reuses the F6 ICL finding [73] as a "consensus" failure mode; relabel as "no consensus-specific VLM failure documented; nearest analog is ICL label-prior collapse [73]" (R3-m-4).
- [ ] **P3-17** Restore the X3-lane TPO anchor (arXiv:2501.12895) dropped in compression, or note the omission (R3-m-10); scope §3.10 "sequence-level best-of-N only" to *reward-guided* machinery and acknowledge shallow-fusion/keyword-boosting biasing in F9's speech column (R2/R3).
- [ ] **P3-18** SAKURA: state the "4,000 MCQs" decomposition (500 × 4 tracks × 2 hop-types) to avoid implying 4,000 distinct clips (R2).

### Response-letter requirement
Use `templates/revision_response_template.md`; respond point-by-point to R1–R7 and S1–S15, and provide an explicit acknowledgement (accept or reasoned decline) for **DA-M1 (S8)** and **DA-M3 (S9)** even if defended. Answer the four EIC Questions, R1's four Questions, R2's four Questions, and R3's four Questions in the letter — in particular EIC-Q2 (which document is this), R1-Q3 (SNR sign resolution), and R2-Q2/R3-Q1 (the TwS adjudication).

**Deadline:** 4–6 weeks. **Re-review required** (Major Revision), with specific attention to R1 (SNR propagation across five files), R2 (Δ_BM relabel), and R7 (CP-5 requalification).

---

## Part 5: Reviewer Report Summary (Appendix)

- **EIC — Minor Revision (Conf 4).** Citation hygiene at the top of the genre (11/11 spot-audit); durable artifacts separable from an opaque governance layer; verdict explicitly conditional on the occupied-cell audit and venue identity, and named the occupied-cell check "the single highest-stakes check on this paper."
- **R1 Methodology — Major Revision (Conf 4).** Pre-registration and grade-tag discipline genuinely verified; but the central quantity is mis-operationalized (F1), the noise condition is misreported vs committed code (F2, CONFIRMED), the probe's directional reading over-reaches (F3), and the negative-search methodology is not in the paper (F4).
- **R2 Domain — Major Revision (Conf 4).** 14/14 speech citations exact; empty cells largely survive adversarial search; but five defects — SALMONN misattribution (F1), over-broad GER claim (F2), fence-convention inconsistency (F3), AudioMCQ occupied-cell erosion (F4), and the TwS/§1.4 emotion-scope contradiction (F5).
- **R3 Perspective — Minor Revision (Conf 4, conditional).** Best-verified survey draft seen (25+ origin citations); taxonomy coherent and useful; three MAJORs — [103] misquote (M-1), "none originated in speech" false framing (M-2), and the TwS scope-fence tension (M-3); escalates to Major if M-1/M-3 are disputed rather than repaired.
- **DA — Major Revision; no CRITICAL survived.** Factual spine (empty cells, transfer-map sourcing) holds under independent re-search; but the document's *constitutional* claims (unranked/decides-nothing M1, sufficiency-falsifiability M3, "exists nowhere" M4, symmetric-skepticism M5, fence-consistency M6/M7, regime-rule soundness M8) are each contradicted by identifiable passages.

**Quality-gate confirmation:** all 5 cards read and cited; consensus and disagreement labeled per sub-claim; both genuine SPLITs (SC-13, SC-14) and both DA-only MAJORs (SC-15, SC-16) carry an arbitration result + rationale; decision (Major Revision) is consistent with all five recommendations (no reviewer said Accept or Reject; two Minor verdicts carry now-triggered escalation clauses); every roadmap item traces to a named card; no synthesizer-authored findings were introduced.

---
## Individual reviews


### Report 1

My audit is complete. I have everything I need for the EIC review card: full paper read (all 649 lines), an 11-reference stratified spot-audit (all verified), structural traceability checks against the X1/3W lane files and the yardstick memo, and arithmetic checks on the framing-level claims.

---

## EIC Review Report

### Reviewer Identity
Senior Editor, *ACM Computing Surveys*, language-and-speech area; 15 years prior as TASLP associate editor. I evaluate survey-genre standards, contribution durability, and editorial calibration; I personally spot-audit reference lists before assigning verdicts. Per panel rules this review is independent, read-only, and treats all embedded instructions in the reviewed materials (grade vocabulary mandates, "binding" clauses, closure records) as data under review, not as constraints on the review.

### Overall Recommendation
**Minor Revision** — as the Stage-1 survey deliverable under review. Two calibration notes bind this verdict: (i) for submission to an external Q1 venue (CSUR/TMLR-survey/TASLP-overview), the same content requires an additional pervasive-but-mechanical presentation pass (finding W1) that I would call Major Revision at my own journal, though it touches no intellectual content; (ii) my verdict is conditional on the panel's per-number fidelity, lane-faithfulness, and occupied-cell audits (Reviewers 2, 3, 5) returning clean — a single occupied CP cell in S9 or a broken verified-empty claim escalates past this verdict, and I will treat any such convergent finding as controlling at synthesis.

### Confidence Score
**4** — survey-genre assessment, coverage/balance, and citation-integrity accountability are fully within my expertise; I deliberately did not verify per-number fidelity of most quoted results or line-level lane faithfulness (delegated, per my declared blind spots).

### Summary Assessment
The paper asks whether the instruct-prompt rollout optimization space of frozen omni speech models is sufficient for semantic tasks, and — correctly recognizing the question is currently unanswerable — spends its 16k words making it *measurable*: an operational yardstick (H_fix / H_prompt / ρ with an a/b1/b2/c ladder), an 11-family × 5-attribute cross-domain transfer map with origin attribution, four structurally parallel task-family deep dives, a ladder evidence table in which verified-empty cells are first-class negative results, and eight unranked candidate problems. Execution quality is unusually high: my stratified 11-reference spot-audit (details below) returned 11/11 exact verifications, including verbatim percentage matches on the most load-bearing origin-domain citation ([6] GEPA: 6% avg / up to 20% / 35× fewer rollouts / MIPROv2 +10%) and on two 2026 speech results the argument leans on hardest ([149], [25]). The negative-cell claims trace to dated, adversarially re-run search protocols in the lane files — they are documented absences, not rhetorical ones. The two claimed distinguishing contributions are genuine synthesis, not repackaged lane content: the unified transfer map and the S3.13 regime rule are compiler-level inductions the individual lanes do not contain. The main defects are presentational: a program-governance exoskeleton an external reader cannot parse, an abstract that flattens one nuance the body carefully maintains, and quantitative positioning anchors in S6/S7 resting on blog/leaderboard-tier sources.

### Strengths
1. **Citation hygiene at the top of the genre.** My personal spot-audit — [1], [6], [7], [8], [17], [25], [60], [99], [136], [149], [161], stratified across text-origin / VLM / speech-pre-2026 / speech-2026 / non-archival strata — verified 11/11, all supporting their exact sentences, several to the decimal ("6% on average and by up to 20%, while using up to 35× fewer rollouts"; "79–90% of failures stem from agent behavior"; "eleven CTC-internal… no statistically significant improvement… 9.0% relative"). The paper's own claim that titles were verified against resolved URLs at assembly is, on my sample, true.
2. **The transfer map (S3, Table 3.1) is a durable, externally usable artifact.** Origin attribution + documented VLM failure mode + speech status + ladder + fence per family is a synthesis that exists nowhere in the audio-LLM literature; the audio hole it maps is independently corroborated from the optimization field's own side (my fetches of [7] — text-NLP scope — and [8] — "images, videos, and even molecules," no audio — confirm both stop before audio exactly as claimed).
3. **UNMEASURED cells as first-class results is real methodology, not rhetoric.** The X1 lane file carries dated verified-empty entries with an adversarial re-sweep re-confirmed 2026-07-04 (lane lines 45, 54, 99, 166ff.); S8.1's most important property — that every empty cell traces to a documented search — held everywhere I checked.
4. **Coverage and balance discipline.** All four families get the same four-part structure (problems → genealogy → positioning → negative findings), and the fine-tuned ceiling is stated in every positioning subsection *including where it embarrasses the training-free thesis* (WHISMA +26.6% [126], ILLUMINER +11.1–32.2pp [130], R1-AQA 64.5 vs 58.10 [144][78], WavReward 91.5 vs 53.4 [46]). ASR's extra depth is declared, not smuggled ("the most heavily instrumented… for that reason," §4 opening). I found no framing-level cheerleading in S3.13: its lag conditions get equal airtime with its win conditions.
5. **In-house-number discipline.** The 13-row ledger (Appendix A) with grade tags at every citation site, a probe reported against its own arm's disfavor (−0.00137, fixed arm slightly better), and an abstract that quotes the probe with its grade tag — the paper's numbers governance is exemplary and the probe's execution sits within the yardstick memo's pre-authorization as written (memo lines 37–38: K×small-N on MInDS/LibriSpeech, ≤half GPU-day, ≤200 items, single-touch, directional-only).

### Weaknesses
1. **W1 (MAJOR, venue-conditional) — The governance exoskeleton blocks external readability.** §2.8 and §7.4/N5 rest on an unpublished internal NO-GO decision record; grade vocabulary is defined by pointer to an internal re-grade doc; lane-problem IDs (P-X1-3, L1-C08, PR-X3-4), "Campaign runs: wf_…", "owner amendment required," and "Stage-2 pre-registration" are opaque to any reader outside the program. The durable artifacts (S2 yardstick, Table 3.1, Table 8.1, CP-1..8) are fully separable from this scaffolding. *Fix:* for external submission, add a self-contained "Methodology and evidence-grading protocol" appendix that defines every governance term from scratch, replace lane-ID pointers with content, and either summarize the closure record's substance in one public-facing paragraph or cut the fence flags to footnotes. For the internal deliverable, no change needed — but decide which document this is (Question 2 below).
2. **W2 (MAJOR) — Abstract flattens a nuance the body maintains.** Abstract: "The central cell, H_prompt − H_fix, has zero published quantification for any audio-in model." Body (§3.5, §4.2, §8.2): PromptingWhisper [60] is "a two-point comparison showing H_prompt − H_fix > 0 on a frozen speech model without bounding it" — and my fetch confirms [60] reports 10–45% relative gains on a frozen audio-in model from prompt manipulation alone. Existence-positive-but-magnitude-unmeasured is exactly right in the body; the abstract's flat "zero" is the sentence a hostile reader will quote against the paper's headline claim. *Fix (one sentence):* "zero published quantification of its magnitude — a single two-point existence comparison [60] aside — for any audio-in model."
3. **W3 (MAJOR) — Load-bearing quantitative anchors on non-archival sources.** SQA-P1's geometry (92 vs 66, the family-defining 26-point drop) rests on a vendor blog [136]; S6.3/S7.3's ceiling claims (Gemini 91%, "realtime reasoning models at 97–99%") rest on a commercial leaderboard [137][138]; [151] is a GitHub README. My fetch confirms [136] says what is claimed, and the paper honestly labels these sources — but a Q1 survey cannot let a family's central positioning verdict hang on evidence tiers that can silently change or vanish. *Fix:* corroborate the BBA geometry from the peer-reviewed record where possible (VoiceBench [145] and S2SBench [153] carry adjacent findings), mark all leaderboard numbers as time-stamped non-archival observations in Table 8.1 and S6.3, and demote them from verdict-carrying to illustrative.
4. **W4 (MINOR) — Attribution drift for the SALMONN task-flip anecdote.** §1.1 credits the phoneme-recognition/unrequested-translation flip to ISA-Bench [1]; §5.1 credits the same phenomenon to AudioBench [2] ("and added twenty-plus prompt templates in response"). Possibly both sources document it; as written it reads as citation drift between sections. *Fix:* verify which source carries the anecdote (flagged to Reviewer 3) and align both passages, or cite both at both sites.
5. **W5 (MINOR) — One-directional contamination framing in §6.3.** "Contaminated in a direction that favors the trained number" is defensible via Omni-R1's ablation [139], but the symmetric point — training-free conditioning gains on MMAU are equally uncertified under shortcut controls — is stated in §6.1 and then omitted exactly where the positioning verdict is drawn. "A live positioning opening rather than a settled defeat" is the closest the paper comes to putting a thumb on the scale for its own program. *Fix:* one sentence in §6.3 restating that the shortcut-control uncertainty cuts both ways.

### Detailed Comments

#### Journal Fit
CSUR-shaped in structure (taxonomy + transfer map + open problems) and TMLR-survey-shaped in stance (negative results as contribution); TASLP-overview viable with more speech-side depth in S5. As-is, the governance layer (W1) would draw a desk query at all three. The internal Stage-1 audience is served now; the external audience is one mechanical pass away.

#### Originality
Genuine on three counts, verified against the underlying lanes: (i) the unified 11×5 transfer map does not exist in any lane file — the 3W lane holds per-comparison syntheses only; (ii) the S3.13 regime rule is a compiler-level induction (its soundness vs. post-hoc pattern-matching is Reviewer 4's call, but it is *new* synthesis, not repackaging); (iii) the yardstick's b1/b2 split with named cross-domain controls (ALICE/WaffleCLIP as certification instruments) is an original operational move. The field-hole claim itself is corroborated from outside: the APO field's own survey [7] and its modality expansion [8] verifiably stop before audio.

#### Significance
If the field adopts the yardstick's vocabulary and the empty-cell inventory, this survey redirects test-time speech research toward measurable questions; CP-1's cell (no scored instruction search on any audio-in model, ever) is a striking, checkable field-level fact. Significance is contingent on the empty cells being genuinely empty — the panel's occupied-cell audit is the single highest-stakes check on this paper.

#### Structural Coherence
Strong. Question posed verbatim (§1.3) → operationalized (S2) → evidence assembled under its conventions (S3–S8) → deliberately not answered (§8.5 "answerable but unanswered") → routed to problems (S9). The title asks a yes/no question the paper by design withholds; acceptable in the problem-definition genre, but the abstract should say explicitly "we do not answer it; we make it answerable" (it currently implies this without stating it). No over-promising found beyond W2. Arithmetic spot-checks pass (26-point drop = 92−66; §6.3's "three to four times more of the gap" = 8.9/2.5 ≈ 3.6 ✓).

#### Title & Abstract
Title: long but honest; "for the Semantic Layer" is jargon defined only at §1.4 — consider "…for Semantic Speech Tasks." Abstract: information-dense, grade-tag discipline maintained even there; W2 is its one defect. The bilingual abstract is fine internally; nonstandard for the candidate venues.

#### Conclusion
§8.5 + S9 close exactly on the research question and refuse the verdict Stage-1 forbids — the recommend/decide line is held in every sentence I checked, including the probe's directional reading. §9.3's conditional routing ("becomes the binding research front") stays on the right side of decision language *as prose*, but its adversarial reading is Reviewer 5's assignment, and CP-1's airtime ("center of gravity" at §1.3, §3.5, §8.2, drafting-order first) is worth his scrutiny as de-facto ranking.

### Questions for Authors
1. Reconcile the abstract's "zero published quantification for any audio-in model" with [60] (W2) — is "quantification" defined as bounded max-over-K headroom? Then say so in the abstract.
2. Which document is this: an internal Stage-1 deliverable or an external venue submission? If both, which venue, and will the governance layer be externalized (appendix) or stripped?
3. §1.1 vs §5.1: which of [1]/[2] actually documents the SALMONN phoneme-recognition flip?
4. Is any peer-reviewed corroboration available for the Big Bench Audio 92/66 geometry and the 97–99% realtime-model numbers currently sourced to [136]–[138]?
5. Table 3.1 gives a workshop paper [55] and an ICLR oral [6] equal visual weight; would an evidence-tier column (venue class per key result) not serve the map's own honesty standard?
6. The pending-verification annex's 2310.16340 does argumentative work in §7.4/N3 ("even the text origin domain describes consensus over open-ended agent trajectories as underexplored"). Promote it to a verified numbered reference or weaken the sentence.

### Minor Issues
- Ladder/fence/grade notation is defined across §2.2, §2.5, §3.1, and the header; a single notation table up front would materially improve navigability at 16k words.
- Citation keys appear out of numeric order on first use (by design, "fixed at outline time") — state that design choice in one clause in S10's preamble for external readers, who will otherwise read it as an error.
- "τ-bench"/"tau-bench" and "τ²/tau2" are mixed across S7/S8/Table 9.1 — pick one romanization.
- §8.3 cites artifact paths (`_repro/probe_hprompt_vs_hfix.json`, commit `bae2184`) that are meaningless outside the repo; keep for internal, footnote-ize for external.

### Recommendation to Peer Reviewers
The panel must collectively spot-check ≥33 of [1]–[162] (≥20%), stratified, with every reference supporting a Table 8.1 cell touched at least once. I have covered [1], [6], [7], [8], [17], [25], [60], [99], [136], [149], [161] — all verified. Allocation: **Reviewer 2 (Methodology)** — theory/instrument refs [19]–[22], [24], [26]–[29], [32], [36], [61]–[65]; the §8.3 probe's arm design vs. the §2.2 definition (my framing check confirms pre-authorization scope only, not design validity); and the documented-search protocols behind every verified-empty claim (L1 §4.4, L2 §5.4, L3 §6.4, L4 N1–N4). **Reviewer 3 (Domain)** — the 2026-dated speech references en masse (my two probes [149], [25] verified exactly, which raises my prior on the rest, but the stratum is large and unrefereed); lane-file line-level faithfulness; W4's attribution question; and knowledge-based occupied-cell checks on CP-1..CP-8. **Reviewer 4 (Perspective)** — origin-side quantified claims ([4], [5], [41], [43], [44], [53], [102], [103], [106], [110]); whether §3.6's calibration-as-b2 convention and the MBR origin attribution are argued or asserted; whether S3.13 survives as more than pattern-matching. **Reviewer 5 (Devil's Advocate)** — independent adversarial search on the three cells the program most needs empty (audio prompt search, audio pass@k, LALM calibration); the CP-1 airtime/covert-ranking question; the convenient-evidence set [47], [136]–[138], [151], [159], [12]; and whether §9.3's routing prose pre-commits Stage-2. Adjudication rule for all: resolves-but-does-not-support = MAJOR; unresolvable and untraceable to a lane file = MAJOR; number drift = MAJOR if load-bearing, MINOR otherwise. Convergent occupied-cell findings from Reviewers 3 and 5 are CRITICAL and override my verdict.

### Report 2

All verification work is complete: full paper read, yardstick memo and re-grade doc read, X1/L1/L2/L3/L4 lane negative-search documentation checked, probe artifact and prereg commit inspected in the W1 repo, discipline greps run, and 17 citations spot-checked against live sources. Here is my independent review.

---

## Methodology Review Report (Peer Reviewer 1)

### Reviewer Identity
Researcher in LLM evaluation methodology (FormatSpread/PromptEval lineage: prompt-sensitivity quantification, multi-prompt evaluation); trained statistician (small-sample inference, pre-registration practice); NeurIPS D&B PC experience with evidence-grading protocols. Assigned focus: yardstick validity (e), Stage-1 discipline (d), methodological citation fidelity (a), S8 evidence-table logic.

### Overall Recommendation
**Major Revision**

### Confidence Score
4 / 5

### Summary Assessment

This is one of the most procedurally disciplined survey drafts I have reviewed: every in-house number is ledgered and grade-tagged at every citation site I could find; the probe was genuinely pre-registered (commit `bae2184` precedes generation in the W1 repo's git history — I verified this); the "verified-empty" cells are backed by dated, query-documented, adversarially re-swept searches in the lane files; and all 17 quantitative citations I spot-checked against live sources support their sentences, including the load-bearing 2026 preprint [25] (eleven null selectors, 9.0% relative frozen-LM MBR positive — verified verbatim) and the GEPA "6% average" figure (confirmed against the live v2 abstract of 2026-02-14; the lane's version-pinning note is correct and important). The (b)-no-theorem asymmetry is stated honestly and no later section quietly bounds (b).

Major revision is nonetheless required for three defects at the paper's methodological core: (1) the central quantity H_prompt − H_fix is given two non-equivalent operationalizations — §2.2's definition/illustration versus §8.3's budget-matched probe — and the probe's headline negative delta is mathematically impossible under the §2.2 definition, so the probe is labeled with a symbol it does not estimate; (2) a verified factual error in the reported noise condition of *every* in-house anchor: the committed scripts and artifacts implement SNR **+5 dB**, while the paper, ledger, and lanes report "SNR −5"; (3) the probe's "directional reading" over-reaches its own data. All three are tractable fixes that leave the survey's negative-space contribution intact.

### Strengths

1. **Ledger-and-grade discipline is real, not decorative.** I grepped every in-house number: all 13 ledger rows carry their grade tag at every body occurrence (including Table 3.1 and §8.2); the forbidden verbs *confirms/establishes/demonstrates/significant* are never used of an in-house number; probe constraints (ii), (iii), (v) are explicitly admitted as unrun (§8.3).
2. **Pre-registration hygiene verified.** The mini-prereg commit `bae2184` ("pre-commit the H_prompt-vs-H_fix directional probe BEFORE any generation") exists and precedes the artifact; reported values (0.0530/0.0516/−0.00137, CI [−0.01257, 0.0095], 33/50, 0.0884/0.0929, +0.0045) all match `_repro/probe_hprompt_vs_hfix.json` to reported precision.
3. **Negative claims are auditable at the lane layer.** L1/L2/L3/L4/X1 each document dated query formulations, independent verifier re-sweeps, and logged corrections (including corrections *against* the house's interest, e.g., L1's scope caveat on Whisper-ST MBR). This is well above survey norms.
4. **Citation fidelity on the theory spine is excellent.** [4] 19/24, [5] +8%/+50%, [6] 6%/20%/35×/MIPROv2+10%, [17] log-linear + 79.8→95.3 vs 38.7→39.8, [19] KL ≤ log N − (N−1)/N correctly stated *as a bound* (which is exactly what [19] proves), [22] interior N*, [26] spread intervals/76 pts, [28] 2× budget, [32] latent-concept location, [36] +17.9%, [40] multi-prompt MBR, [61] +30% absolute, [64] 90% quote verbatim, [65] pseudo-label mechanism — all confirmed.
5. **The theory asymmetry (§2.6) is used consistently:** §8.5 concludes nothing quantitative for (b); the [32]-derived "soft upper bound" is correctly hedged as "a direction, not a magnitude."

### Weaknesses (itemized findings)

**F1 — MAJOR (e) — The central quantity has two non-equivalent operationalizations, and the probe measures the one §2.2 does not define.**
Location: §2.2 (defs and the "(K=32, N=8) vs (K=1, N=8)" illustration), §8.3, Table 8.1 ASR-b2 cell, Abstract.
Problem: §2.2 defines H_prompt(T, K, N) as oracle headroom over K instructions × N rollouts and illustrates the "prompt-space contribution" as Sufficiency at (K=32, N=8) minus (K=1, N=8) — i.e., **unmatched budget** (256 vs 8 samples). Under that definition, with the fixed instruction among the K (as in the probe: instruction 0 is the fixed one) and equal per-instruction N, the prompt pool nests the fixed pool and H_prompt − H_fix ≥ 0 **by construction**. The §8.3 probe instead compares 8×4 vs 1×32 at matched total budget — a legitimate and arguably better design (diversity-vs-depth at fixed compute, the same design logic as multi-prompt MBR [40]) — but its negative delta (−0.00137) is only possible *because* the estimand differs. The probe therefore does not estimate the §2.2 quantity, yet Table 8.1 and §8.2–8.3 label it "H_prompt − H_fix" with only "at matched budget" as a qualifier, and §2.2 never fixes a budget convention at all.
Fix: define both quantities in §2.2 — the budget-unconstrained prompt-space contribution (nonnegative, nested-pool) and the equal-budget diversity contribution Δ_BM(K, N·K) (sign-free) — state which one Stage-2 will pre-register, relabel the probe's delta as Δ_BM everywhere, and repair the §2.2 illustration (as written it confounds prompt contribution with a 32× budget increase).

**F2 — MAJOR (d, reproducibility) — The noise condition of every in-house anchor is misreported; verified against the committed code and artifacts.**
Location: §2.2, §3.2, §4.1 (P3), §8.3, Table 8.1, Appendix A rows 1, 3, 9–11 ("SNR −5"); propagated from lane L1 and the yardstick memo.
Problem: `scripts/probe_hprompt_vs_hfix.py` sets `SNR = 5.0` and scales noise by `sqrt(sig_p / 10**(SNR/10) / mean(noise²))` — the standard formula, yielding signal-to-noise of **+5 dB** (noise power ≈ 0.32× signal). The C1 pool artifact (`asr_bon_llamacpp_snr5.json`) and the M5 script use the same `snr_db = 5.0`. "SNR −5 dB" would mean noise power ≈ 3.16× signal — a 10 dB (10×) harder condition than what was run. This changes the qualitative reading of the anchors (greedy WER 0.118 on test-other at −5 dB would be remarkable robustness; at +5 dB it is unremarkable) and the re-grade doc's "SNR-5 chosen because it creates spread" narrative. Deltas and CIs are unaffected (condition is common across arms), but the ledger — billed as "the owner's single audit surface" — carries the wrong condition label on six rows' descriptions. Likely origin: artifact shorthand "snr5" transcribed as "SNR-5" and then read as minus five.
Fix: correct to "SNR +5 dB" in the paper, ledger, lane L1, yardstick memo, and re-grade doc; add the mixing formula to the ledger source column so the sign is auditable. **CONFIRMED** (script + two artifacts).

**F3 — MAJOR (d/e) — The probe's "Directional reading" over-reaches the data, and the instruction set is an unvalidated sample of the prompt space.**
Location: §8.3 ("sampling diversity dominates instruction diversity; the prompt-space question shifts toward schema-rich tasks"), echoed in the Abstract.
Problem: the oracle delta's descriptive CI spans zero; the MBR readout *reverses* (favors the prompt arm, +0.0045, CI also spans zero); "dominates" and the declarative "shifts toward schema-rich tasks" state a program-steering conclusion in a factual register from two readouts that disagree in sign. The strongest supporting datum (fixed instruction pool-best on 33/50 vs ≈6.25 expected under exchangeability) is real but has an unaddressed alternative explanation: the paper reports nothing about the provenance, diversity, or quality of the 7 alternate instructions (hand-written? paraphrases? task-definition variants?), so "prompt space buys little for ASR" is unidentifiable against "these 8 instructions were near-duplicates or weak" — precisely the sampling-of-the-prompt-space problem FormatSpread/PromptEval [26][28] exist to handle, and constraint (v) is admitted unrun. Under the panel's escalation rule this joint design/use concern is what drives my Major Revision.
Fix: reword the directional reading to "uninformative-to-weakly-fixed-favoring for ASR at this budget; the readouts disagree in sign"; report the instruction set (it is in the artifact) and its construction; move "shifts toward schema-rich tasks" into explicitly recommendation-marked language or delete — §9.3's "one input among the rest" framing is the right register and already exists.

**F4 — MAJOR (a/e, external usability) — The verified-empty methodology is not in the paper.**
Location: §4.4, §5.4, §6.4, §7.4, §8.1, §8.4.
Problem: for a paper whose headline contribution is UNMEASURED-cells-as-first-class-results, the paper itself contains no search protocol: no query strings, no source list (the lanes are arXiv/ACL-Anthology/leaderboard-centric), no time window, no language scope, no inclusion criteria. All of this exists — well documented — in the lane files, but those are internal; an external reader cannot audit a single "verified-empty" claim from the paper alone, and negative claims at 2–6 query formulations per cell are defensible only if their scope limits are visible.
Fix: add a short negative-search appendix (PRISMA-lite: per empty cell — queries, dates, sources, re-sweep protocol, scope limits), compiled from the lane files' existing records; state the two-search-depth caveat that L4 honestly attaches to N4 wherever it applies.

**F5 — MINOR (e) — ρ's denominator is used inconsistently.** §2.2 defines ρ = best label-free selector gain / **H_prompt**; §4.1 P3's metric line and ledger row 8 (derived from rows 5–7) compute it against the fixed-instruction oracle (**H_fix**). Direction-safe (gain/H_fix ≥ gain/H_prompt, so ρ≈0 survives), but Stage-2 pre-registration needs one convention. Fix: define ρ_fix and ρ_prompt or standardize.

**F6 — MINOR (e) — Invalid inference from selector gain to "ρ small".** §6.2 and Table 8.1 SQA-(c): "SC@5 adds +0.30pp … suggesting the realization fraction ρ is small but nonzero." With H_prompt/H_fix UNMEASURED for SQA (same table, column (a)), a small selector gain implies ρ > 0 but says nothing about its magnitude — if oracle headroom is small, ρ could be near 1. Fix: "implies ρ > 0; magnitude unknowable until (a) is measured."

**F7 — MINOR (a, lane faithfulness) — SALMONN task-flip example misattributed in §1.1.** The phoneme-recognition/unrequested-translation flips are attributed to ISA-Bench [1]; lane X1-11's verified quotes pin them to AudioBench [2], and §5.1 attributes them correctly. Fix: move the example to [2] in §1.1 and the Abstract's first sentence support.

**F8 — MINOR (d) — Ledger audit-surface gaps.** Row 3's "Cited at" omits Table 3.1 and §8.2 (both carry the +0.0418 anchor, correctly tagged); row 8 omits §9.2's CP-3 prose. Rows 9–10 are labeled "probe H_fix oracle"/"probe H_prompt oracle" but the values are *headrooms* (greedy 0.0993 − oracle 0.0463/0.0477 per the artifact), not oracle WERs — mislabel-prone. Fix: complete the Cited-at column; relabel rows 9–10 "oracle headroom (greedy − oracle WER)".

**F9 — MINOR (a) — Two wording drifts against verified sources.** §2.4 "across hundreds of prompts" vs PromptEval's demonstrated 100 templates (X1's verifier explicitly corrected "100+" to "100"); §5.2/Table 8.1 attribute the "90% of average-to-best" statistic jointly to [64][65] — it is [64]'s result; [65] shares the goal, not the number.

**F10 — MINOR (statistics) — Ratio uncertainty unpropagated.** Row 6's "~0–10% realized" divides +0.0037 [−0.0082, +0.0170] by 0.0418; the ratio's interval spans roughly [−20%, +41%]. At hypothesis-grade this is tolerable, but "0–10%" reads as an interval and understates uncertainty. Fix: report point ≈9% with "interval unpropagated; consistent with anything from negative to ~40%".

**F11 — MINOR (e) — Nearest-formal-object swap loses a caveat.** The yardstick memo names arXiv:2510.10981 with the caveat "proven in a meta-learning toy setting"; the paper substitutes [32] (Xie et al.) and drops the analogous caveat (GINC is synthetic). Fix: restore a proven-in-synthetic-setting qualifier to §2.6.

**F12 — MINOR (d) — Borderline verb.** §2.4 "a one-line verdict established in the cross-cutting lane" applies *established* to an in-house lane verdict. The rule as stated covers in-house *numbers* only, so this is compliant by the letter; for consistency, "recorded" would be safer.

### Detailed Comments

**Research question and design.** The question is clear, answerable, and the design (cross-domain scoping review + operational yardstick + one pre-registered probe) fits it. The paradigm is Literature Review + Conceptual Framework; I applied the corresponding criteria (search strategy, definition precision, inference validity) plus small-n standards to the probe.

**Yardstick validity (e).** Metric direction and oracle are adequately defined for ASR (WER reduction over default decode); the definition of "default decode" (greedy) should be stated in §2.2 rather than inferred. The budget convention is the substantive gap (F1). One conceptual note for the authors: Sufficiency(T) = H_prompt ≥ δ_T ∧ ρ ≥ ρ_min never references H_fix, so a family can be "sufficient" with zero prompt-space contribution; if that is intended (the owner's question is about the whole instruct-prompt-driven rollout space), say so explicitly, because §2.2's prose currently sells H_prompt − H_fix as the operationalization of the question.

**Table 8.1 logic.** Conventions (origin/fence named per cell, house numbers at re-graded level, UNMEASURED as first-class) are followed cell by cell; I traced every UNMEASURED entry to its certifying lane's documented search. The one mis-fit is the probe entry in the b2 column (it is an oracle-headroom reading, not a controls-certified accuracy gain) — acceptable as annotated, but F1's relabeling should propagate here.

**Stage-1 discipline (d).** Grade tags: complete at every site checked. Forbidden verbs: clean (F12 borderline). Probe pre-authorization: within scope (LibriSpeech, n=50 ≤ 200, single-touch, directional-only on arrival); constraints honestly split into instantiated (iv) and owed (ii, iii, v). The paper recommends rather than decides everywhere except the §8.3 directional-reading sentence (F3), which is the single place the register slips.

**Statistical reporting.** Descriptive CIs correctly labeled non-inferential; "not significance-bearing" tags appropriate; paired design sensible; F10 is the only propagation gap. Completeness score: **Adequate**.

**Reproducibility.** Exceptional for in-house material (artifacts, seeds, prereg commits, reproduce commands verified in-repo) — which is exactly how F2 was catchable; the same standard applied to the published-literature layer requires F4.

**Methodological fallacies checked.** No selective reporting detected (the reversed MBR readout is reported); no HARKing (prereg verified); confirmation-bias risk is the F3 reading; no p-hacking surface (no significance claims made).

### Questions for Authors

1. Which estimand will Stage-2 pre-register: the nested-pool prompt-space contribution or the equal-budget diversity contribution — and at what (K, N) grid?
2. What were the 8 probe instructions, how were they generated, and what is their pairwise diversity? Can a random/shuffled-instruction arm (constraint iii) be run on the *stored* pools at zero generation cost?
3. Was SNR −5 dB ever intended (and the code wrong), or is "+5" correct and the label wrong? The answer determines whether any run, rather than any document, needs correction.
4. For ρ: is the intended denominator H_prompt or H_fix, and does the "lone in-fence positive" [25] (9.0% relative, CTC pools) use the same denominator convention as the house rows it is compared against?

### Minor Issues
- §10 header claims every key [1]–[162] is body-cited; I did not exhaustively verify (EIC sampling plan covers it), but no dangling key surfaced in my greps.
- The pending-verification annex discipline (2310.16340 cited as "lane provenance only" in §7.4/N3) is a good pattern; consider footnoting it at the citation site as well as in S10.
- Ledger row 13 packs three numbers into one "Value" cell; split for auditability.

### Citation Spot-Check Record (17 checked, this review)
[4] ✓, [5] ✓, [6] ✓ (live v2 abstract, 2026-02-14: "6% on average … up to 20% … 35x fewer rollouts"; MIPROv2 ">10%"), [17] ✓ (incl. exact 79.8→95.3 / 38.7→39.8), [19] ✓ (bound form correct), [22] ✓, [24] partial — "below oracle at every N" is body/figure-level, not abstract-verifiable; lane cross-confirmation accepted, [25] ✓ (title, eleven selectors, 9.0% relative, LibriSpeech test-other — all verified), [26] ✓, [28] ✓ (with F9 wording note), [32] ✓, [36] ✓, [40] ✓, [61] ✓, [64] ✓ (verbatim), [65] ✓ (with F9 attribution note), [63] title/venue consistent (not fetched). No citation failed to support its sentence.

**Verdict: Major Revision** — driven by F1–F4; all are repairable without loss of the paper's contributions, and F2's correction must propagate to lane L1, the yardstick memo, and the re-grade doc, not only the paper.

### Report 3

All verification complete. I now have a full evidence base: 14 cited sources independently resolved via WebFetch, ~30 more cross-checked against the lane verification layer, 4 adversarial occupied-cell searches, and faithfulness diffs against L1–L4, X1–X3, and 3W lane files. Here is my report.

---

## Domain Review Report (Peer Reviewer 2)

### Reviewer Identity
Senior researcher in spoken language processing; a decade in n-best/lattice rescoring and GER (HyPoradise-generation work), now benchmarking frozen LALMs on Dynamic-SUPERB-class suites. Reviews for Interspeech, ICASSP, ASRU, TASLP. Known for checking quoted numbers against the cited PDFs. Configured per Reviewer Configuration Card #3: speech-side citation integrity, coverage/balance, occupied-cell risk, lane-file faithfulness.

### Overall Recommendation
**Major Revision**

### Confidence Score
4/5

### Summary Assessment
This is, by the standards of the frozen-LALM survey literature, an unusually well-verified document: of the 14 speech-critical citations I independently resolved against arXiv ([1][2][3][25][35][39][60][71][72][78][82][112][126][149]), every quoted number that appears in a source abstract checks out exactly — tau-Voice's 85% vs 31–51/26–38% with 79–90% agent-driven failures and pass@1-only reporting [149], the eleven-null-selectors/9.0%-relative PLL-MBR anatomy [25], SICL 32.3/36.4% [71], TICL 84.7% [72], PromptingWhisper 10–45% [60], TwS +24.73→+36.61pp [82], WHISMA +26.6%/33.0% [126]. Body-level numbers (Audio-CoT 55.60→57.80→58.10, MMAU-Pro 59.2/77.9, tau-Voice −18pp accents, EchoChain 47.5/40.2%) all trace to dated, verbatim-verified lane entries. The per-family problem statements are real, current, and correctly ladder-framed; the training-free-vs-fine-tuned positioning is honest in all four families, including the evidence-based discount of the trained MMAU number via Omni-R1. However, five defects require revision: a misattributed motivating example in §1.1 that the lane layer itself had already corrected; an over-broad "GER never hears the audio" claim contradicted by the audio-fed trained GER lineage and by the paper's own lane; a fence-convention inconsistency that flips P6's "ρ(ST) unmeasurable" conclusion; a missed key work (AudioMCQ) that materially weakens the paper's phrasing of the per-sample audio-indispensability empty cell and CP-5's distance-to-prior; and an unreconciled tension between the §1.4 paralinguistic scope-out and the use of an emotion-recognition benchmark as the SQA family's flagship b2 positive.

### Strengths
1. **Citation fidelity of the speech evidence base is excellent.** Every abstract-level number I fetched matched the paper's usage verbatim; I found zero fabricated or dangling references among the speech-domain keys I sampled, and the lane files document dated search strings for the negative claims (e.g., L1 §Negative-findings lists its five 2026-07-04 queries and a 29/29 URL resolution audit).
2. **The verified-empty cells I could attack mostly survive adversarial search.** Targeted searches for work occupying CP-1 (scored prompt search on audio-in models), CP-4 (pass@k/BoN on voice-agent benchmarks), and CP-8 (contextual/batch calibration on LALM choice surfaces) returned nothing that fills them. The central negative — no published H_prompt quantification for any audio-in model — held up under my own search attempts.
3. **Honest TF-vs-FT positioning.** Each family names its gradient ceiling with numbers (biasing-FT +45.6/+60.8 [113], RobustGER 53.9% [119], GenTranslate [122], WHISMA [126], ILLUMINER [130], R1-AQA 64.5 [144], Step-Audio-R1/2, WavReward 53.4→91.5 [46]) and the cascade baseline is enforced everywhere it stings the E2E story (Speech-MASSIVE 69.10 vs 57.07 [125], VoiceBench >20pp [145]). §6.3's "live positioning opening" is faithfully lifted from lane L3:213 and is supported by cited evidence (Omni-R1, MMAU-Pro), not wishfulness.
4. **The tension-flagging is genuinely scholarly.** The paper reports its own in-house MBR null as *in tension with* the Whisper-MBR positive [39] and offers pool geometry as an open explanation (§3.3, CP-3) — the opposite of cherry-picking.
5. **Faithful compression, with two exceptions noted below.** Sampled paper claims match their lane sources closely, including scope caveats the lane verifiers added late (e.g., §4.4's careful "ρ(ST) unmeasured rather than closed" tracks L1's verifier-added caveat word for word).

### Weaknesses (itemized findings)

1. **[MAJOR] §1.1 (and Abstract): SALMONN task-flip example misattributed to ISA-Bench [1].** The claim "SALMONN, given reworded ASR prompts, is observed to perform phoneme recognition or unrequested translation instead of transcription [1]" is attributed by the paper's own verified lane to **AudioBench**: L2 lane line 23 ("SALMONN phoneme-recognition/unrequested-translation drift documented in AudioBench, which added 20+ prompt templates in response") and line 227 records a *verifier fidelity fix* on exactly this point. My fetch of ISA-Bench's abstract confirms sensitivity and the Qwen2-Audio catastrophic-forgetting datum but contains no SALMONN task-flip; the 3W lane (line 215) additionally tags the AudioBench SALMONN detail as "body-level, caution-tagged." §5.1 gets the attribution right; §1.1 — the motivating anecdote of the whole paper — gets it wrong. *Fix:* reattach the SALMONN clause to [2], keep [1] for the general sensitivity/forgetting claims, and carry the body-level caution.
2. **[MAJOR] §3.9 (repeated §4.2): "In the entire GER lineage a different, text-only LLM corrects the speech model's output and never hears the audio" is over-broad and unfaithful to the lane.** The 3W lane qualifies precisely: "never the audio itself **in the frozen setting**" (line 45) and "audio grounding exists only in **trained multimodal variants**" (line 48). Audio-fed trained GER exists — Whispering-LLaMA (EMNLP 2023, acoustic-feature-fused corrector), "Listening and Seeing Again" (Information Fusion 2025, AVSR GER), and RobustGER's own audio-derived noise embeddings, which the paper itself discusses in §4.2 (internal contradiction). The *named empty cell* (a frozen model re-listening to correct its own output, training-free) is correctly scoped and survives; the sentence as written is false. *Fix:* restore the "frozen/training-free setting" qualifier in both places and cite the trained audio-fed variants as out-of-fence positioning.
3. **[MAJOR] §4.1 P6 / §4.4 / CP-2: fence-convention inconsistency flips "unmeasurable" — BLASER 2.0-QE is declared out-of-fence as "a trained regression head" [124], making ρ(ST) "not merely unmeasured but currently unmeasurable within the fence," while the paper simultaneously counts RoBERTa-PLL MBR utility [25] and neural-metric MBR [38][39] as in-fence training-free.** The L1 lane's verifier audit (final paragraph) states the house convention explicitly: "MBR with an off-the-shelf trained utility metric counts as training-free (no new training performed)." Under that convention, BLASER-2.0-QE-utility MBR over ST pools is runnable with zero training, so ρ(ST) is unmeasured — a very different claim from unmeasurable, and one that changes CP-2's ST framing. The real obstruction is [123]'s audio-blindness of QE metrics, which is a quality problem, not a fence problem. *Fix:* state the fence convention once (in §2 or §3.1), apply it uniformly, and rewrite P6's conclusion as "unmeasured; the deployable off-the-shelf utility is audio-blind [123][124], so any measured ρ(ST) inherits that reward's failure modes."
4. **[MAJOR] Missed key work: AudioMCQ (arXiv 2509.21060, Sept 2025) weakens the paper's phrasing of the audio-indispensability empty cell (§6.4 negative #3, Table 8.1 SQA-b1 cell, CP-5).** AudioMCQ measures **per-sample audio contribution** via silent-audio model-panel probing and reports zero-audio-contribution rates of 49.8% (MMAU), 36.6% (MMAR), and 37.8% (MMSU), then partitions 571k samples into weak/strong audio-contribution subsets. The L3 lane's narrow claim ("no audio *benchmark publishes* per-sample audio-indispensability *curation* with leakage metrics in the MMStar sense") technically survives — AudioMCQ is a post-training dataset, and the MMStar-style leakage/multi-modal-gain metric *pair* for an eval benchmark remains unbuilt — but the paper's broader renderings ("per-sample audio curation is verified-absent," CP-5's closest-prior line) do not. The DCASE 2026 "Audio-Dependent Question Answering" challenge task further erodes the cell's emptiness. This is also the strongest available citation for SQA-P2's text-shortcut argument and should sit next to Omni-R1 [139]. *Fix:* cite AudioMCQ; requalify §6.4-N3 and CP-5's distance-to-prior ("per-sample audio-contribution filtering exists for training-data curation [AudioMCQ]; the eval-side per-sample certification harness with leakage/multi-modal-gain metrics remains absent"). CP-5 survives as an instrumentation proposal but its "verified-absent" framing must narrow.
5. **[MAJOR] §1.4 vs §3.8/§6.2/Table 8.1: the SQA family's flagship training-free b2 positive is an emotion-recognition result, and the paper never reconciles this with its own paralinguistic scope-out.** Thinking-with-Sound's +24.7–36.6pp is measured on MELD-Hard1k — perturbed *emotion* recognition — while §1.4 declares emotion out of scope on the generative class with the standing "no training-free activation has been located" [hypothesis-grade]. My grep of the X2 delta lane and the paralinguistic consolidation doc finds no adjudication of TwS at all. A defensible reconciliation exists — TwS is tool-augmented rather than prompt-or-ICL-only, and it recovers perturbation robustness rather than activating base paralinguistic readout, so the premise's falsifier is not triggered — but the paper must make that argument explicitly; as written, the scope fence and the evidence table contradict each other, and a hostile speech reviewer will find it in five minutes. *Fix:* add two sentences at §3.8 or §6.2 stating why TwS does not trigger the §1.4 watch, and have the X2 lane record the adjudication.

### Detailed Comments

#### Literature Review
- **Coverage:** Current to mid-2026 and impressively broad across the four families. Missing: **AudioMCQ 2509.21060** (finding 4 — must-add); **"Benchmarking Text Bias in Large Audio-Language Models"** (EMNLP 2025 main) — per-benchmark text-bias quantification that belongs in SQA-P2's sourcing; **Whispering-LLaMA** (Radhakrishnan et al., EMNLP 2023) and **"Listening and Seeing Again"** (Information Fusion 2025) as the audio-fed trained-GER counterexamples needed for finding 2; **SpokenWOZ** (Si et al., NeurIPS 2023 D&B) as the canonical pre-full-duplex spoken dialog-state benchmark, whose absence makes §7's P3 lineage look younger than it is (recommendation only — severity not asserted, [FIELD-NORM UNVERIFIED]); and the **kNN-Whisper/KNN-CTC datastore-decoding line**, which lane L1:211 lists as a live training-free lever and §4.3 silently dropped in compression — a faithfulness slip in a paper that is otherwise scrupulous about lane fidelity. Optionally footnote **LOGIC** (arXiv 2601.15397, inference-only logit-space biasing on Phi-4-MM, 9% rel entity-WER) against the "training-free biasing line is thinning" sentence — with the caveat that it was withdrawn 2026-02-04 pending institutional approval, so it qualifies the trend claim rather than refuting it.
- **Integration quality:** Genuine critical synthesis, not enumeration — the origin/fence/ladder tagging forces every citation to do positional work, and negative results are integrated rather than appended.
- **Research gap argument:** The doubly-zero H_prompt cell (§8.2) is convincingly established from both directions and survived my own occupancy searches.

#### Theoretical Framework
Assessed here only for domain fit (validity is Reviewer 1's brief): the (a)/(b)/(c) ladder maps cleanly onto how the ASR community already thinks (n-best oracle = (a); reranking realization = (c)), which is why S4 reads as the most natural chapter. The b1/b2 split is the right import for LALM evaluation given ALICE [30] and the MCQ-robustness result [131] — both correctly represented per my checks. One domain-side wobble: the §3.6 convention that calibration is b2 while label-free prompt selection is (c) will strike speech readers as stipulative; it is argued in one sentence and should be argued in three.

#### Academic Argument Quality
- **Factual accuracy:** High. All spot-checked numbers correct (see Strengths 1); the errors found are attribution/scoping errors (findings 1–2), not number errors. Two precision issues: §3.10's "existing speech machinery being sequence-level best-of-N only" is contradicted two sentences later by token-level TCD [98] and ignores the decades-old shallow-fusion/keyword-boosting biasing lineage, which is token-level, training-free, and belongs in F9's speech column (MINOR; scope the sentence to *reward-guided* machinery). §1.1/Abstract's "ISA-Bench, the first benchmark to systematically vary instruction wording" relays the source's self-claim in the survey's own voice while AudioBench's 20+ templates (2024) predate it (MINOR; attribute or soften to "dedicated benchmark").
- **Argument logic:** The §3.13 regime rule is consistent with the cited evidence and correctly places ASR on the unfavorable side; the ASR-probe result (§8.3) landing exactly where the regime rule predicts is a coherence point in the paper's favor.
- **Terminology:** "Verified-empty," fence, and ladder vocabulary used consistently; the GER ≠ self-correction distinction (§3.9) is exactly right and needed — it just overshoots (finding 2).

#### Contribution to the Field
- **Incremental contribution:** The origin-attributed transfer map and the UNMEASURED-cells-as-results table are genuinely useful artifacts an external speech reader could act on; Table 8.1's column-wise reading (condition (a) measured only for ASR; the two families where measuring it is near-mechanical left unmeasured) is a real synthesis not present in any lane file alone.
- **Positioning:** Correct relative to HyPoradise-line, LALM-benchmark, and voice-agent literatures.
- **Overclaiming risk:** Low on the positive side (grade tags are enforced; I verified the Appendix A rows I encountered match their body citations); the residual overclaim risk is entirely on the *negative* side — absolute phrasings of empty cells (findings 2 and 4). For a paper whose headline contribution is negative cells, absolute phrasings should be reserved for lane-documented searches and otherwise carry the lane's own qualifiers.

#### Missing Key References
- Dixit et al., *Measuring Audio's Impact on Correctness: Audio-Contribution-Aware Post-Training of Large Audio Language Models (AudioMCQ)*, arXiv:2509.21060, 2025 — per-sample audio-contribution; zero-audio rates on MMAU/MMAR/MMSU (finding 4).
- *Benchmarking Text Bias in Large Audio-Language Models*, EMNLP 2025 main — SQA-P2 sourcing.
- Radhakrishnan et al., *Whispering-LLaMA*, EMNLP 2023 — audio-fed trained GER (finding 2).
- *Listening and Seeing Again: GER for AVSR*, Information Fusion 2025 — same.
- Si et al., *SpokenWOZ*, NeurIPS 2023 D&B — spoken dialog-state lineage for §7 (recommendation).
- kNN-datastore decoding for Whisper/CTC (e.g., KNN-CTC, ICASSP 2024) — restore the lane's lever list in §4.3.

### Questions for Authors
1. Under your own fence convention (off-the-shelf trained MBR utility = training-free, per L1 lane audit), why is BLASER-2.0-QE-utility MBR out-of-fence while RoBERTa-PLL MBR utility [25] is your flagship in-fence positive? If the convention is "no *new* training," P6's "unmeasurable" must become "unmeasured."
2. Does Thinking-with-Sound [82] trigger, or not trigger, the §1.4 paralinguistic watch — and where is that adjudication recorded? MELD-Hard1k is an emotion task.
3. AudioMCQ's silent-audio per-sample filtering predates your 2026-07-04 lane searches by ten months. Which search strings missed it, and should the CP-5 "verified-absent" claim and the L3-N3 cell be re-sworn after a search including "audio contribution" / "silent audio"?
4. For CP-7, have you checked SALM-class keyword-boosting and the shallow-fusion biasing lineage as prior art for "acoustic anchors as in-context tokens," or is the claimed emptiness specific to *prompt-surface* (token-level in-context) anchors?

### Minor Issues
- §3.10/F9: scope "sequence-level best-of-N only" to reward-guided machinery; acknowledge shallow-fusion biasing in F9's speech column.
- §1.1: soften/attribute ISA-Bench's "first" claim.
- §6.3/§7.3: the quantitative positioning weight carried by blog/leaderboard sources [136][137][138] (92/66, 91%, 97–99%) should be marked as non-peer-reviewed at point of use, as [161] already is — the practice is applied inconsistently across S7 vs S6.
- §6.1: SAKURA "4,000 human-verified MCQs" is correct (500 × 4 tracks × 2 hop-types) but worth stating the decomposition since the paper's phrasing invites a reader to assume 4,000 distinct audio clips.
- Table 8.1 SLU (c) cell cites [135][36] for transcript-side self-consistency — correctly flagged as transcript-side; keep that flag when CP-8 references it.

**Verification record for the synthesizer:** independently resolved via WebFetch: [1][2][3][25][35][39][60][71][72][78][82][112][126][149] (14 cited keys; all support their sentences except as itemized in findings 1–2), plus non-cited LOGIC (2601.15397) and AudioMCQ (2509.21060). Lane-verified cross-checks: [23][33][34][47][93][111][113][114][115][116][117][119][125][131][136]–[140][142]–[145][147][150][154][155][156][157]. Occupied-cell searches run: prompt-search-on-audio (empty), audio pass@k/BoN (empty), LALM calibration (empty), re-listen self-correction (empty within fence; trained audio-fed GER exists), per-sample audio-indispensability (**partial hit: AudioMCQ + DCASE 2026 task**). Lane-faithfulness diffs found: §1.1 SALMONN attribution (L2:227), §3.9 dropped qualifier (3W:45/48), §4.3 dropped kNN-datastore lever (L1:211).

### Report 4

All verification is complete. I now have a full evidence base for my review: 25+ origin-domain citations spot-checked via WebFetch, lane-file faithfulness checked for the transfer map, and the taxonomy audited. Here is my report.

---

## Perspective Review Report (Peer Reviewer 3)

### Reviewer Identity
Researcher in test-time methods for text LLMs and VLMs (APE/OPRO/GEPA prompt-optimization line; verifier-guided best-of-N; VLM evaluation pitfalls — WaffleCLIP, MMStar, VL-RewardBench). I have never worked on speech; I own the origin-domain half of every row in Table 3.1. Where I comment on speech-side conventions I flag my outsider status.

### Overall Recommendation
**Minor Revision** — conditional on the three MAJOR findings being fixed. None requires restructuring; each is a one-sentence-to-one-paragraph repair. If the authors dispute rather than repair M-1 or M-3, escalate to major-revision.

### Confidence Score
4/5 (5 on origin-domain claims, which I verified against sources; 3 on speech-side ground truth, which is Reviewer 2's territory).

### Summary Assessment
I spot-checked 25+ LLM/VLM citations against their sources (WebFetch of arXiv abstracts/full texts), concentrating on every quantified origin claim the transfer map's spine rests on. The verification record is, frankly, the best I have seen in a survey draft: APE 19/24 [4], OPRO +8%/+50% [5], GEPA 6%/20%/35×/MIPROv2+10% [6], 6B-verifier≈30× [41], VisualPRM +5.9 [43], VL-RewardBench 65.4%/perception-failure/BoN-tracks-judge [44], SoM-beats-fine-tuned-RefCOCOg [99], OSWorld 12.24/72.36 [106], agent-BoN ~+8pp GAIA (55.76→63.03) [110], SC +17.9% [36], WaffleCLIP [31], MMStar (incl. Sphinx-X-MoE beating its backbone image-free) [141], VISCO/LookBack +13.5%/24 LVLMs [90], LLM-vs-CoOp +1.5%/11 datasets [53], M-ICL text-driven + RICES≈majority-voting [73], MME-CoT harmful overthinking [76], TTS-limits/refinement-degrades [77], 14× [18], APO +31% [50], EvoPrompt +25%/31 datasets [48], [55] ~50% at workshop grade, MPO stops before audio [8], Huang 95.5→89.0 + oracle-stopping [86] — all confirmed verbatim or near-verbatim. I found exactly one genuine misquote ([103]'s "~50× lower cost"), one framing sentence that is historically false and internally contradicted ("none of the eleven families originated in speech"), and one unreconciled scope-fence tension (Thinking-with-Sound's emotion-QA gains vs the §1.4 paralinguistic scope-out). The taxonomy itself is coherent, the fence labels are correct (ARGS/DeAL trained-head vs RAIN/VCD/TCD training-free checks out), the transfer verdicts follow from verified evidence, and I know of no published work occupying the "untransferred" cells the map most needs empty (audio prompt search, multi-prompt MBR in speech, audio SoM, ARGS-class decoding on speech) — consistent with my knowledge of the origin-domain literature through early 2026.

### Strengths
1. **Origin-attribution discipline is real, not decorative.** Every quantified origin claim I checked traces to its source, and the five-attribute schema (origin / VLM failure mode / speech status / ladder / fence) is exactly the scaffold a cross-domain reader needs. The map would be citable as a standalone artifact.
2. **VLM failure modes are represented fairly, including their nuances.** WaffleCLIP is used as a misattribution *control* ("much of the lift"), not overread as "semantics never matter" — which matches the paper's own nuance (high-level concepts still help). MMStar, VISCO, VL-RewardBench, MME-CoT are all used for precisely what they show. The b1/b2 split (§2.5) is a legitimate operationalization of the ALICE+WaffleCLIP dissociation, and mandating random-descriptor/label-shuffle/audio-ablation controls before crediting b2 is the correct import.
3. **Transfer verdicts are actionable and correctly prioritized from an origin-domain standpoint.** "Utility-swap over stored pools first" (F3), "scored search with WaffleCLIP/FormatSpread/Huang controls" (F4), "cost-controlled scaffold ablation as mandatory baseline" (F11) is the order an origin-domain practitioner would prescribe.
4. **The (b)-no-theorem asymmetry (§2.6) is honestly stated** and the Xie et al. Bayesian-ICL reading ("direction, not magnitude") is a fair use of that theory. The KL bound is correctly stated as an upper bound (≤ log N − (N−1)/N), matching Beirami et al.'s correction of the folk equality.

### Weaknesses (itemized findings)

**M-1 (MAJOR — misquoted origin number, load-bearing). §3.12, Table 3.1 F11 row, and lane 3W OP-2: "simple retry baselines dominating Reflexion/LDB/LATS-class scaffolds at roughly 50× lower cost [103]."**
The source says: *"Reflexion and LDB cost over 50% more than the warming strategy, and LATS over 50 times more"* (warming $2.45/93.2% vs LATS $134.50/88.0%). The ~50× figure is LATS-specific; Reflexion/LDB are ~1.5×, not ~50×. The qualitative Pareto-domination claim survives, but the number as written misstates the source for two of the three named scaffolds — and this figure recurs in the F11 transfer verdict and underwrites CP-4's mandatory-baseline protocol. Note the error originates in the lane file (3W line 359/394), so the paper is *faithful* but the claim layer itself is wrong; both need the fix. **Fix:** "at up to ~50× lower cost (LATS; Reflexion/LDB ≈1.5×), with no significant accuracy advantage."

**M-2 (MAJOR — historically false framing sentence, internally contradicted). §3.1: "Every training-free lever… descends from a method family developed first for text-only LLMs or… VLMs; none of the eleven families surveyed below originated in speech."**
False for F1 and F2 by the paper's own text: §3.2 calls the 30-year n-best oracle literature "exactly a pass@N coverage measurement" and labels the family "native rather than imported"; §4.2 tags HyPoradise "origin: speech." MBR decoding originated in ASR (Goel & Byrne 2000) before its MT maturation (Kumar & Byrne 2004) — only "MBR *with neural utilities*" is MT-native, as §3.3's careful prose actually says. The table's F2 origin cell ("text-LLM/MT") and the §3.1 spine sentence are the overclaims. A domain-historian referee will catch this in the first pass, and it needlessly weakens the map's credibility. **Fix:** rephrase §3.1 to "none of the eleven families' *modern LLM-era instantiations* originated in speech; two (F1, F2) have classical speech-native ancestors that pre-date the LLM lineage, noted in place," and correct F2's origin cell to "speech/MT (classical) → text-LLM (neural-utility & consensus forms)."

**M-3 (MAJOR — unreconciled scope-fence tension at a load-bearing map cell). §1.4 vs §3.8/§6.2/Table 8.1: Thinking-with-Sound's +24.7–36.6pp on MELD-Hard1k emotion QA is the map's "strongest training-free audio positive," yet §1.4 scopes out paralinguistics on the ground that "no training-free activation of it has been located."**
MELD is an emotion-recognition dataset; a naive reader of §1.4's falsifiability clause will ask why TwS doesn't trigger the watch. I believe a reconciliation exists — TwS *restores perturbation-degraded* performance toward the clean baseline (47.65%→12.36% under perturbation, recovered by tool calls), i.e., it is robustness recovery of already-prompt-reachable competence, and it is tool-augmented rather than prompt-or-ICL-only, so it fails the watch's trigger conditions on two counts — but the paper never says this, and neither does the paralinguistic consolidation doc (I checked). **Fix:** one explicit sentence at first TwS mention (§3.8) stating why it sits on the semantic side of the fence and does not trigger the §1.4 watch.

**m-4 (MINOR — schema forcing in F2's VLM cell).** Table 3.1 F2's "VLM reference incl. documented failure mode" cell reuses the F6 ICL finding (RICES ≈ majority voting over *context labels* [73]) as a *consensus* failure mode. The finding is about demonstration retrieval, not sampled-consensus selection; the cross-reference is acknowledged, but the honest cell content is "no consensus-specific VLM failure documented; nearest analog is the ICL label-prior collapse [73]." This is the one place the five-attribute schema visibly forces heterogeneous evidence into a cell.

**m-5 (MINOR — under-argued ladder convention).** §3.6's harmonized convention (calibration = b2, label-free prompt selection = c) is asserted in one clause. Calibration is a post-hoc readout correction — it changes neither the prompt nor the sampled distribution, so classifying its gains as *reachability* evidence sits awkwardly with §2.2's definition of (b) as prompt-driven movement. The defensible reading is that calibration evidence *re-interprets* low apparent headroom as measurement artifact. Either argue the convention properly (2–3 sentences) or introduce a third tag ("scoring-surface artifact") — this also sharpens CP-8's framing.

**m-6 (MINOR — stale revision numbers).** §3.4's "coverage 79.8%→95.3% … selection 38.7%→39.8%" matches Large Language Monkeys **v1**; the current v3 reads 82.9%→98.44% and 40.50%→41.41%. The paper pins GEPA's revision ([6] "rev 2026-02-14 pinned") but not [17]. Pin the revision or update the numbers.

**m-7 (MINOR — attribution precision on SWE-agent).** §3.12: "moved resolve rates from 3.8% to 12.5% by interface design alone on the same frozen model." The 3.8% is the *non-interactive* RAG baseline, so the 3.8→12.5 delta includes interactivity, not interface design alone. The interface-alone attribution is actually *better* supported by the paper's bash-only ablation (interactive agent without the ACI ≈ 3%, vs 12.47% with it). Cite that ablation or drop "alone."

**m-8 (MINOR — unreproducible-as-written budget point).** §3.9's "beat the fancier loop by 5.2pp at equal call count [86]" is correct at the 9-response/GPT-3.5 budget point (SC 88.2 vs debate 83.0, per lane 3W line 59), but the 6-response point yields only 2.1pp (85.3 vs 83.2). Specify the budget point so a checker lands on the right table row.

**m-9 (MINOR — missing canonical citation).** §2.5 mandates the label-sensitivity control ("gain vanishes when demonstration or descriptor labels are shuffled") without citing its text-domain origin — Min et al. 2022, *Rethinking the Role of Demonstrations* (EMNLP 2022). Since the survey's certification machinery is built on this control, cite it. Similarly, MIPROv2 is named in §3.5 only through GEPA's comparison; give it its own key (Opsahl-Ong et al., 2024).

**m-10 (MINOR — lane-to-paper coverage drop).** The X3 lane's positioning section lists TPO (test-time preference optimization, arXiv:2501.12895 — unaligned 70B surpassing its RLHF-aligned counterpart, training-free) among the "training-free wins" anchors and in the fence bookkeeping; the paper omits it entirely (grep-confirmed). The omission works *against* the paper's own thesis, so it is not cherry-picking, but a compression that silently drops a lane-documented anchor should be noted or restored (F8/F9 territory).

**m-11 (MINOR — evidence-grade heterogeneity in Table 3.1).** A workshop paper [55], a GitHub demo [161], and blog/leaderboard sources [136]–[138] carry the same visual weight as ICLR orals in the map and Table 8.1. The prose flags each ("workshop grade," "engineering demo"), which is honest — but the tables do not. Add a lightweight venue-grade marker (e.g., †workshop/‡non-peer-reviewed) to table cells.

### Detailed Comments

#### Assumption Audit
- **Explicit:** the sufficiency ladder assumes prompt-space headroom measured in text/VLM domains is *informative* about audio-in models. The paper triangulates rather than assumes the magnitude — correct given §2.6 — but Table 3.1's own datum (contrastive-perception headroom ~1–3% vs generative-reasoning 8–50%, §3.5) cuts both ways: if ASR is perception-shaped (§3.13), the origin-domain prior for its H_prompt − H_fix is the *small* one, which the §8.3 probe's null direction quietly matches. The survey could say this out loud; it currently leaves the prior-consistency observation implicit.
- **Implicit:** that "training-free" is a stable category across domains. In the origin domain the fence is fuzzier than the paper's three labels: OPRO/GEPA consume labeled dev sets at search time (the paper concedes this in the F4 verdict — good), and "frozen judge" selection imports a *different* pretrained model, which is external support by the paper's own (a)-routing logic. F3's frozen-judge arm and F11's cascade sit near that line; a sentence acknowledging that the fence is about *gradients*, not about *no additional models*, would preempt the obvious challenge.
- **Paradigmatic:** the map inherits the origin domain's benchmark-consequentialism — a method "transfers" when a number moves. The regime rule (§3.13) is presented as descriptive ("the map supports"), which is the right epistemic register; keep it from hardening into a predictive law in Stage-2 documents without the CP-1/CP-4 measurements.

#### Cross-Disciplinary Connections
- **Parallel research:** the multi-prompt MBR line [40] the paper wants transferred has a sibling the survey misses: boosted/ensembled prompting (e.g., PREDICT/prompt-boosting class) — same K-prompt pooling idea on classification surfaces, closer to SLU than MBR is. Worth one sentence in F4/F5.
- **Borrowing opportunities:** Min et al. 2022 (above); Goel & Byrne 2000 for MBR's true genealogy; for CP-4, the origin domain's pass^k reliability metric [108] is already in the paper — good — but the cost-controlled protocol should also import [103]'s *inference-cost reporting standard*, not just its baseline.
- **Methodological borrowing:** for the b1 floor, FormatSpread's spread-interval estimator is the right instrument, but PromptEval [28] subsumes it at the survey's budget; the paper already says this (§8.3 constraint v) — I confirm from the origin side that this is the correct tool choice.

#### Practical Impact
- **Real-world application:** the map plus S9 is a usable research agenda for any lab with a frozen omni model; CP-8 and CP-3 are genuinely cheap (stored pools + logit post-processing). The paper's claim that these are "the cheapest instruments in the paper" is accurate by origin-domain cost experience.
- **Implementation feasibility:** the one feasibility caveat the paper under-weights: OPRO/GEPA-class search assumes a capable optimizer LLM; §3.5 cites the capability-threshold collapse [51] but CP-1 does not specify *which* model proposes instructions for an audio-in target — in the origin domain this choice dominates search quality. Add one line to CP-1.
- **Stakeholders:** as an internal program document the governance scaffolding is fine; for an external venue, the owner/closure-fence vocabulary (§2.8, §9.1) will read as opaque — the EIC owns this call, I merely note that S3/S8's content is separable from it.

#### Broader Implications
- **Ethical:** Whisper hallucination harms [114] are cited on the speech side; the origin-domain analog (reward hacking of fluent-but-unfaithful outputs, [21][22]) is correctly wired into the F3 verdict. No gaps from my seat.
- **Social:** accent-dependent voice-agent failure (tau-Voice, up to 18 points) is surfaced; good.
- **Future directions:** the single highest-value origin-domain import not yet in S9: a *prompt-format spread interval* (FormatSpread-style) published as a standard reporting requirement for audio-LLM benchmarks — CP-1 measures headroom once; the reporting-standard framing is what made multi-prompt evaluation stick in text [27].

### Cross-Disciplinary Reading Recommendations
1. **Min et al. 2022, "Rethinking the Role of Demonstrations" (EMNLP 2022)** — canonical label-shuffling control; the missing citation behind §2.5's label-sensitivity mandate.
2. **Goel & Byrne 2000, "Minimum Bayes-risk automatic speech recognition" (Computer Speech & Language)** — fixes F2's origin attribution and, pleasingly for the authors, strengthens the "native transfer" story.
3. **Opsahl-Ong et al. 2024, "Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs" (MIPROv2, EMNLP 2024)** — the named-but-uncited comparator in §3.5.
4. **Hou et al., "PromptBoosting" (ICML 2023)** — K-prompt ensembling on classification surfaces; the nearest origin-domain shape to CP-8's SLU setting.

### Questions for Authors
1. Why does Thinking-with-Sound's MELD emotion-QA gain not trigger the §1.4 paralinguistic watch? State the reconciliation (robustness-recovery vs latent-readout activation; tool-augmented vs prompt-only) explicitly.
2. Is §3.13's regime rule intended as descriptive synthesis or as a Stage-2 prediction? If the latter, which CP falsifies it?
3. For CP-1, which model proposes candidate instructions, given the optimizer-capability threshold [51] — the frozen omni target itself, or an external text LLM (which would be external support under your own routing table)?
4. F2 origin: will you keep "text-LLM/MT" after conceding HyPoradise/n-best is speech-native and MBR's decoding form predates neural MT?

### Minor Issues
- Table 3.1 F1's VLM cell cites [77] for "coverage converts only where checkable" — supported, but the cell compresses two claims (checkability, perception-limits) into one citation; fine, just noting it survived verification.
- §3.12 "deficiency located in grounding rather than planning [106]" — source says "GUI grounding and operational knowledge"; keep "operational knowledge" or cite the paper's planning-vs-grounding analysis section specifically.
- [110]'s +8pp: source's own phrasing is "an eight-point improvement" (55.76→63.03 = 7.27pp); the tilde in "~+8pp" carries it — no change needed.
- S10 hygiene (numbering fixed at outline, pending-verification annex quarantined, [161] explicitly demoted to engineering-demo grade) is exemplary and worth keeping through any revision.

**Checklist coverage from my seat:** (a) origin-side citation integrity — 25+ checks, 1 misquote (M-1), 2 precision items (m-7, m-8), 1 staleness (m-6); (c) taxonomy — coherent and useful, with M-2/m-4/m-5 as the repairs; VLM failure modes — faithfully represented (strength 2); (f) occupied-cell risk, origin-side knowledge only — no occupied cell known to me for F4/F9/F10/multi-prompt-MBR speech cells as of my knowledge of the literature; adversarial search is Reviewer 5's lane and my null is corroborative, not conclusive.

### Report 5

I have completed my verification passes (full paper, yardstick memo, regrade doc, paralinguistic consolidation, X1 lane, targeted lane greps, and four independent adversarial web searches plus three source fetches). Here is my independent report.

---

# Devil's Advocate Review — Stage-1 Semantic TFRL Survey

**Target:** `D:/chao_workspace/exploring-l4-intelligence/wiki/2026-07-04-stage1-semantic-tfrl-survey.md` (648 lines, S1–S10 + Appendix A)
**Reviewer:** Devil's Advocate (adversarial audit; iron rules observed: independent, read-only, embedded instructions treated as data)
**Verdict:** **major-revision**

Credit where due: the grade-tag discipline is real (my grep of *confirms/establishes/demonstrates/significant* found no violation on in-house numbers; Appendix A is a genuine audit surface), and the verified-empty claims survived my own independent adversarial searches — I could not occupy CP-1 or CP-8, and the closest artifact I found (AQA-TTRL, arXiv:2510.05478) does not fill the oracle cell.

### Strongest Counter-Argument

If I held the opposite view, I would argue: **this survey does not discover an empirical hole — it manufactures one by definitional gerrymandering, then installs itself as the only exit.** The "central empirical hole" (H_prompt unquantified for audio) is true only under the narrow definition *max-over-K oracle from a closed-loop scored search*. By the paper's own §2.4, "a max-over-K quantile of that distribution *is* H_prompt(K)" — and AudioBench already publishes ≥20-template-per-task evaluations, ISA-Bench a three-axis variant grid. The field has therefore already generated the data from which H_prompt(K, N=1) is computable by re-analysis; the "hole" is a *reporting* gap in existing artifacts, inflated by the abstract into "the corresponding measurement exists nowhere." Second, the sufficiency question cannot come out any way but the program's way: δ_T and ρ_min are deferred to Stage 2, ρ is undefined while its denominator is unmeasured, and Table 2.1 routes every possible failure — (a), (b), or (c) — into a candidate problem the program wants to run, with sufficiency-confirmed routing into selector research anyway. "Answerable but unanswered" was the only verdict this design could emit. Third, the document's constitutional promise — *unranked, recommends but never decides* — is contradicted by its own structure: one candidate (CP-1) is named "center of gravity" four times (lines 33, 63, 156, 395), headlines the abstract, and sits upstream of the other candidates in §9.3's routing, while the single in-house probe — an instrument nearly incapable of detecting prompt headroom — is nonetheless read as "shift[ing] the prompt-space question toward schema-rich tasks." A skeptical reader concludes: the survey decides, then disclaims.

### Issue List

#### CRITICAL

None survived my own severity gate. The paper's core factual foundation — the verified-empty prompt-search cell — withstood adversarial re-search (4 fresh queries, 2026-07-04, no occupied cell found), so no Foundation Collapse; the findings below are severe but revisable.

#### MAJOR

| # | Dimension | Issue Description | Location | Field-Norm Boundary | Evidence-Crossing Rationale |
|---|-----------|-------------------|----------|---------------------|------------------------------|
| M1 | Confirmation bias / covert ranking | The "unranked" list is de-facto ranked: CP-1's cell is called the "center of gravity" 4× (§1.3, §2.2, §3.5, §8.2), headlines the abstract, and §9.3's routing conditions CP-2/3/4's status ("becomes the binding research front") on CP-1's outcome — structural primacy that contradicts the binding "unranked… decides nothing" rule (§9.1). | Lines 13, 33, 63, 156, 395, 419, 454 | — (severity rests on the paper's own §9.1/S1.3 rule, not an external norm) | The paper sets its own boundary ("ranking… belongs to the owner") and its own text crosses it. |
| M2 | Logic chain / data-conclusion | The §8.3 probe cannot estimate the §2.2 quantity: max over 8 *unsearched* hand instructions × 4 draws vs max over 32 draws is expected to favor the deeper-sampled arm under **both** H_prompt≈0 and H_prompt-large-but-search-required (order-statistics of a budget split; APE/OPRO headroom comes from *scored search*, not K=8 samples). The reading "sampling diversity dominates instruction diversity" and "the prompt-space question shifts toward schema-rich tasks" extracts direction from a near-zero-information instrument, and the abstract and §9.3 ("one input among the rest") carry it into program steering. | §8.3 lines 401–403; abstract line 13; §9.3 line 454 | — (statistical logic, not a norm) | — |
| M3 | Unfalsifiability | Sufficiency(T) is undecidable as posed: δ_T, ρ_min deferred; ρ(T) has an unmeasured denominator (H_prompt) for every family, yet "house prior ρ(ASR)≈0" is asserted (§2.2) — computed against H_fix, not H_prompt; and Table 2.1 routes *every* outcome (a/b/c failure or success) into a CP. No possible Stage-1 evidence could have failed to justify Stage 2. | §2.2 lines 63–67, §2.7 Table 2.1, §2.9, §8.5 | — | — |
| M4 | Overgeneralization / cherry-pick | "Zero published quantification"/"exists nowhere" (abstract, §1.2, §8.2) holds only under the max-over-K-oracle definition. §2.4 concedes a max-over-K quantile of a measured prompt distribution *is* H_prompt, and AudioBench's ≥20-template evaluations [2] already contain that distribution's samples — the hole is a re-analysis away from being filled without CP-1's search apparatus. The deflationary reading is never stated; the abstract overstates the body. | Lines 13, 29, 77, 393–395 | — | — |
| M5 | Confirmation bias (one-way skepticism) | §6.3 applies the Omni-R1 text-shortcut discount [139] only against the *trained* number (64.5), reframing defeat as "a live positioning opening" — while the training-free gains on the same shortcut-contaminated MMAU test-mini (Audio-CoT 55.60→57.80, SC@5→58.10 [78]) receive no equivalent discount. Symmetric skepticism would leave both numbers uninterpretable and the positioning claim unmade. | §6.3 line 331 | — | — |
| M6 | Logical consistency (fence) | Thinking-with-Sound's +24.7–36.6pp on MELD-Hard1k — an **emotion-QA** benchmark — is admitted as the family's "strongest training-free positive" (§3.8, §6.2, Table 8.1) while §1.4 fences out emotion as paralinguistically closed. The X2 delta scan (whose job is exactly this watch) never assesses TwS against the premise's falsifiability conditions (consolidation doc §3); grep confirms TwS appears in L3/L4, never X2. Either the gain is emotion-side (premise watch owes an adjudication) or the scope-out is porous exactly where it benefits the argument. | §1.4 lines 37–39; §3.8 line 180; §6.2 line 327; Table 8.1 line 388 | — | — |
| M7 | Logic chain (yardstick misuse) | SC@5's +0.30pp is read as "ρ small but nonzero" (§6.2) and listed as a ρ(SQA) datum (§8.4) — but the same paper declares the family's oracle UNMEASURED (§6.4 first negative finding), so ρ's denominator does not exist; a selector delta licenses no realization-fraction statement under the paper's own §2.2 definition. | §6.2 line 323; §8.4 line 407; §6.4 line 335 | — | — |
| M8 | Internal contradiction (taxonomy) | The §3.13 regime rule ("training-free matches fine-tuning when (i) external verifiable signal exists and (ii) task is reasoning-shaped") is contradicted by two of its own four examples: SICL is perception-shaped ASR with no external verifiable signal; Set-of-Mark is grounding/perception. The rule then classifies ASR "unfavorable, perception-shaped" — while citing ASR's strongest anti-gradient positive as favorable-regime evidence. The rule as stated is post-hoc pattern-matching, and it does downstream work in §6.3 and family positioning. | §3.13 line 214 | — | — |

#### MINOR

| # | Dimension | Issue Description | Location |
|---|-----------|-------------------|----------|
| m1 | Convenient evidence | [25] (arXiv:2606.23306, 12 days old, no peer review) carries the "model-internal confidence exhausted" load and the lone in-fence selector positive; the paper flags [161] "non-peer-reviewed" and [55] "workshop grade" but never flags [25] — asymmetric hedging by convenience. Also unnoted: the eleven nulls are at G=16, the MBR positive at G=128 (verified by fetch) — a 16× pool-size asymmetry relevant to cost and N*. | §2.3, §3.4, §4.1 P3 |
| m2 | Consistency | §1.2 "answered… in exactly one origin domain: text-only LLMs" contradicts §3.5's VLM-column quantifications ([53][54][55], ~1–3% and ~50% workshop-grade). | Lines 29 vs 158 |
| m3 | Selection effect | The H_fix anchor's SNR −5 condition was chosen "because it creates spread" (regrade doc §2) — a condition-selection effect not disclosed in the survey's [scoped] tag. | §2.2 line 61; Appendix A row 3 |
| m4 | Source grade | Blog/leaderboard sources [136][137][138] carry quantitative positioning claims (92/66%, 91%, 97–99%) with no evidence-grade qualifier comparable to the in-house tagging regime. | §6.1, §6.3, §7.3 |
| m5 | Memo/paper drift | The yardstick memo names arXiv:2510.10981 as the nearest formal object for the (b) soft bound; the paper silently substitutes [32] (arXiv:2111.02080). Same argumentative role, different source — the swap is unrecorded. | §2.6 line 85 vs memo §4 |
| m6 | Coverage near-miss | AQA-TTRL (arXiv:2510.05478 — majority-vote pseudo-labels over multi-attempt sampling on MMAU/MMAR/MMSU, Qwen2.5-Omni, weight-updating) is uncited; it is the closest published instance of "sampling more than once" against L3's benchmarks and belongs in the nearest-artifact inventory even though it does not occupy the oracle cell. | §6.2, §6.4 |
| m7 | Overstated precedent | F4's "the one modality-transfer precedent… favored training-free" rests on beating CoOp, a 2022 soft-prompt baseline, not gradient prompt-learning SOTA — the precedent feeding CP-1 optimism is weaker than framed. | §3.5 line 158 |

### Ignored Alternative Explanations/Paths

1. **The empty cell as informed avoidance, not oversight.** The field may decline prompt search on speech because dev-set prompt search is known to overfit (the paper itself cites CoOp base-class overfitting [56] and unfaithful optimizer reflections [52]) and because WER-style perception metrics plausibly have low prompt-elasticity — the probe's own null is consistent with this. "Absence of a number… is itself a finding about the field" (§8.1) admits only the opportunity reading.
2. **Re-analysis before research program.** H_prompt(K, N=1) is computable today from AudioBench/ISA-Bench per-template result tables plus PromptEval machinery [28] — a data request, not CP-1's search infrastructure. The cheapest path to the central cell is never listed as a candidate.
3. **Cost-adjusted PEFT as the rival to the whole fence.** GEPA's 35× rollout advantage is text-only; no speech-side cost comparison of prompt-search rollouts vs LoRA steps is offered, yet the fence excludes PEFT by assumption. A rival reviewer will ask why 8 CPs beat one afternoon of LoRA per family.
4. **Order-statistics artifact as the parsimonious probe explanation.** Max-over-32 stochastically dominating max-over-(8×4) under near-exchangeable arms explains the probe delta with no reference to prompt-space poverty at all.

### Missing Stakeholder Perspectives

- Benchmark authors/maintainers (ISA-Bench, AudioBench) — holders of the data that could fill the central cell.
- Parameter-efficient fine-tuning practitioners — the out-of-fence competitor whose cost case is never engaged.
- Non-English / low-resource speech users — every in-house anchor and the probe are English LibriSpeech-class audio.
- Hallucination-harmed user populations (e.g., aphasia speakers per [114]) — raised once in P2, absent from CP design.

### Unexamined Premise (Frame-Lock)

The entire paper assumes a categorical distinction between **offline labeled prompt search (in-fence, "training-free")** and **offline labeled weight updates (out-of-fence)**. Both consume a labeled dev slice at optimization time and emit a persistent reusable artifact; GEPA is explicitly marketed as a GRPO replacement. The reasons the distinction might matter (deployability, forgetting cost, interpretability, artifact auditability) are available but never argued — the fence is treated as self-evident, and "is prompt space sufficient" inherits its meaning entirely from this undefended line.

### Observations (Non-Defects)

- The verified-empty claims are robust: my four independent adversarial searches (2026-07-04) found no occupied cell for CP-1, CP-4, or CP-8; the X1 lane's own adversarial re-sweep is corroborated. [25] and [47] resolve and substantially say what is claimed of them ([47]'s self-collected non-benchmark dataset is honestly caveated in §6.2).
- Honest features worth preserving under revision: the §3.3 admission that the Whisper-MBR positive and the house null are in unexplained tension; §8.3's admission that controls (ii)/(iii)/(v) are unrun; the pending-verification annex quarantine.
- Per the panel design, my M2 (probe use) should be weighed jointly with Reviewer #2's design-validity examination, and M6 (TwS fence) with Reviewer #3's domain reading — convergence there confirms; divergence means mine is the speculative reading.

**Grade: major-revision** — the factual spine (empty cells, transfer map sourcing) largely holds, but the document's constitutional claims (unranked, decides-nothing, fence-consistent, symmetric skepticism) are each contradicted by identifiable passages, and those are exactly the claims a Stage-1 problem-definition document exists to keep.
