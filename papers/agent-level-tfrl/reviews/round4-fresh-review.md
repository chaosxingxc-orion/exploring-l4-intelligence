# Peer Review — Round 2 (FRESH panel, new angles, blind to prior rounds)

> Run wf_be2e7d7e-7a1, 2026-07-01. Different adversaries (Lean-purist, deployment-realist, coherence-critic, contribution-skeptic, eval-statistician). Meta-chair classified findings against the resolution ledger.


## Chair: clean_round=False, verdict=major revision, 13 NEW critical/major + 11 minor


The revised paper's core -- a clean Gibbs-tilting theory (OSA-1 spread bound, OSA-2 additivity + qstar_product 'isolation adds nothing', the new strict-positivity lemma) plus an honestly reported paralinguistic negative -- survives and is internally consistent in the body (Sections 5/7/10). No NEW finding invalidates that core, and no finding is fatal-and-unfixable, so the verdict is major revision, not reject. However the round is NOT clean: thirteen NEW major findings remain. The dominant class is incomplete propagation of the round-1 reframe into the most-read sections: the abstract/intro/C1-C2/appendix still carry the retracted 'realized spread' term, the OSA-3 'stability tax' pillar (with a false 'bounds the tax' claim -- the deficit is unbounded above), the C2 promise of convergence 'conditions' the body says are open, an unqualified 'verifiable-reward acceptance gate', and a false 'Pinsker discharged on paper' claim; plus a literal wrong-direction KL slip (beta*KL(q*||q0)) in the appendix proof of the flagship new lemma. These are individually fixable but, for a paper whose selling point is calibrated honesty, the most-read sections are currently the least accurate. Two methodological NEW findings have more teeth: the headline emotion negative is reported by seed-vote-counting (2/5) rather than the across-seed CI, which from the paper's own numbers spans zero -- the honest statement is 'null', not 'fragile' (and this strengthens the paper); and the Phase-1 controls do not rule out the evidence-accumulation confound, leaving the compounding slope attributable to acoustic-data quantity. The deepest concern, raised independently by the deployment and novelty reviewers, is that the flagship system's novel axis (cross-session paralinguistics) has no specified mechanism to beat the pre-registered strong baseline and Phase-2 pre-registers a null there, so C4 'worth building' is unsupported and the paper risks reducing to a (valuable) theory + honest-negative + benchmark note. Remaining NEW items -- 'agentic recovery' contradicting qstar_product, the 'Not Model Class' title undercut by the paper's own model-class-switch remedy, the tautological '0 regressions' rerank metric, under-specified SLURP/MInDS provenance, an unpinned baseline update rule, uncosted human calibration contradicting the label-free premise, and the embedding-probe negative over-generalized to the untested generative policy -- are concrete and addressable. Recommend major revision: sync front matter to body, fix the KL direction, report the across-seed emotion CI, add an evidence-matched benchmark control, and either specify a paralinguistic winning mechanism or demote the system to a probe rig.


### NEW critical/major (not already resolved/scoped)


**[MAJOR] F1-kl-direction** (fix-in-lean) @ main.tex line 1351 (appendix, OSA-suite paragraph, justification of gain_pos_of_nonconstant)
  
  The appendix justification of the flagship new lemma gain_pos_of_nonconstant writes the master identity in the wrong (asymmetric) KL direction: 'the master identity gain = beta * KL(q* || q0)'. KL is asymmetric; the correct identity is gain = beta * KL(q0 || q*), as the main text (line 493) and the cited Lean lemma F_sub_eq_beta_mul_kl (line 1268, F(q*)-F(q) = beta * sum q log(q/q*), at q=q0) both state. Only the appendix flipped it.
  
  *Fix:* Change KL{q*}{q0} to KL{q0}{q*} at line 1351 so it reads gain = beta * KL(q0 || q*), matching F_sub_eq_beta_mul_kl (p=q0, r=q*) and kl_pos_of_ne (which requires r=q*>0). Grep the appendix for every KL{..}{..} to confirm no other direction slip.
  
  *Why new:* The strict-positivity theorem was added in round 1 (ledger), but the KL-direction typo in its written proof is a new, literal mathematical error introduced by that addition, not previously flagged. For a paper marketing calibrated formal honesty, an asymmetry slip in the headline lemma's exposition is a real defect a measure-theory reader will catch immediately.

**[MAJOR] F2-frontmatter-desync** (reframe) @ Abstract main.tex line 182; C1 line 211; appendix status table lines 1219-1220, 1307; vs §5 line 612, §10 line 1054
  
  The revision's honest hedges were applied in the body but not propagated to the most-read sections, producing direct internal contradictions and two substantive misstatements: (a) OSA-3 is named 'the stability tax'/third pillar in abstract (182), C1 (211) and appendix table (1219-1220) but §5 (612) says 'exactly two load-bearing results' and §10 (1054) demotes it; moreover 'OSA-3 bounds the rollout-stability tax' is mathematically false, since rollout_deficit = beta*KL(q||q*) is an unbounded-above deficit, not a bounded tax. (b) Abstract (182)/C1 (211) claim Hoeffding AND Pinsker are 'discharged on paper,' but only Hoeffding is (lem:hoeffding); Pinsker is consumed as the undischarged hypothesis hPinsker (1307) and proved nowhere, and the documented best-of-N sorry (1297) is omitted from the abstract/C1.
  
  *Fix:* Sync front matter to the body: drop 'OSA-3 (the stability tax)' and 'bounds the rollout-stability tax' (replace with 'a static, nonnegative rollout-deficit corollary; finite-time convergence open'); state in the abstract/C1 'Hoeffding is discharged on paper; Pinsker and the Beirami order-statistics bound are consumed as named hypotheses, the latter the single documented sorry (klBoN_le_klBoundBoN_TODO)' (the rem:honesty text already exists -- promote it).
  
  *Why new:* The ledger demoted OSA-3 and qualified the machine-checked claim in the body, but the reviewers show that fix is incomplete: the abstract, contribution list, and appendix table still carry the retracted framing, and the abstract makes a false 'Pinsker discharged on paper' claim. Insufficient propagation of an applied fix, plus a new substantive misstatement (no tax bound exists), not a re-raise of a settled item.

**[MAJOR] F3-realized-spread-term** (reframe) @ Abstract main.tex line 182 / intro / line 723 / line 885 / line 1145 / line 1195 vs rem:ceiling line 535-541
  
  The load-bearing thesis word 'realized reward spread' is retained in the abstract (182), intro, feasibility (723), plan (885), conclusion (1145) and appendix (1195), while rem:ceiling (535-541) explicitly states 'there is no separate realized spread to speak of, and we drop that adjective ... avoid calling spread realized.' Substantively the certified OSA-1 bound uses the global RANGE (spread^2/8beta), not a 'realized'/variance quantity; the variance refinement Var_q0(R)/(2beta) is only a remark, not a theorem.
  
  *Fix:* Delete 'realized' globally (or define an explicit effective support so it has a referent); state the thesis as 'governed by the reward range (and, to leading order, Var_q0(R))', and make the abstract say plainly the certified ceiling is range-based with the variance term a remark.
  
  *Why new:* rem:ceiling (the body fix) was added in round 1, but the term it retracts is still the headline word everywhere else, including the thesis statement. The reviewers show the body's own retraction is contradicted by the unrevised front matter -- a new coherence defect, not the settled title change.

**[MAJOR] F4-agentic-recovery-contradicts-qstarproduct** (reframe) @ §9 main.tex line 887; §10 lines 980, 996; abstract/intro 'agentic decomposition is empirically supported for content/intent'
  
  The phrase 'agentic recovery'/'agentic decomposition empirically supported for content/intent' (§9 line 887, §10 lines 980/996, abstract framing) is incoherent under the revised thesis: the content/intent evidence is labeled 'Single-model only' (tab:opB), and qstar_product proves the isolated/agentic optimum EQUALS the monolithic optimum. So the agent 'recovers' nothing a single model could not. Calling single-model best-of-N gains evidence for an 'agentic-recovery move' conflates 'reward spread is high on one model' with 'agentic decomposition adds gain,' which the paper's own theorem forbids.
  
  *Fix:* Replace 'agentic recovery' with theory-licensed language: 'single-model verifiable selection yields high-spread gain for content/intent; whether agentic decomposition adds anything beyond the monolithic single-model optimum is untested and, by qstar_product, can only come from introducing genuinely new non-degenerate per-block rewards.' State plainly the content/intent gain is single-model, not agentic.
  
  *Why new:* The OSA-2 reframe (isolation adds nothing) was applied to §5/§10, but the residual 'agentic recovery' terminology -- a leftover from the old 'agent recovers gain the single model can't' framing -- directly contradicts the very theorem the reframe introduced. The reviewer shows the reframe is not fully internalized in the discussion/plan.

**[MAJOR] F5-title-not-model-class** (reframe) @ Title main.tex lines 169-171; remedy lines 730, 824, 894; spread def line 537; tab:opB vs tab:cremad-matrix
  
  The (newly chosen) title slogan 'Governed by Reward Spread, Not Model Class' is undercut by the paper's own central finding and remedy: realized spread is the range of R over supp(q0), and q0 is induced by the frozen model, so spread is a joint property of (model, action-space, reward). The paper's resolution of the paralinguistic null is precisely to SWITCH model class (omni embedding -> ECAPA/SER) because the omni model affords near-zero speaker spread. That is 'model class governs spread,' the opposite of the slogan. Separately, no controlled experiment holds reward and action space fixed and varies model capability; every comparison (flat conditioning vs Operator-B) changes both the action space and the reward.
  
  *Fix:* Narrow the slogan to what is supported, e.g. 'Governed by Reward Spread, Not Search Cleverness or Agent Class,' and add a scope sentence early stating spread is model-induced (different model classes realize different spreads for the same reward -- which is exactly why the paralinguistic fix is a model-class switch). Either run the missing equal-spread/varied-capability control or drop the universal 'Not Model Class' claim.
  
  *Why new:* The ledger applied the title change as the round-1 fix; two reviewers independently show the new title is itself contradicted by the paper's own model-class-switch remedy and is unsupported by any controlled comparison. Per the ledger rule, this is a demonstration that the applied fix (the new title/thesis framing) is wrong/insufficient.

**[MAJOR] F6-emotion-vote-counting-not-CI** (re-run-experiment) @ tab:emotion-multiseed main.tex lines 771-788; mirrored abstract 182, intro 213, plan 887, discussion 991, conclusion 1165
  
  The integrated multi-seed emotion result is summarized by an across-seed mean+std and a seed-vote count ('paired CI excludes 0 in only 2/5 seeds') but never by the correct across-seed CI / one-sample test on the mean. From the paper's own per-seed deltas {+0.097,-0.053,+0.083,-0.007,+0.063}: SE=0.064/sqrt(5)=0.029, t4=1.28, p~0.27, 95% CI ~ [-0.043,+0.116], spanning zero. The honest statement is 'no significant emotion gain at the across-seed level (null),' not 'fragile / helps on some splits,' which implies a real-but-unstable effect. Seed-vote-counting over underpowered per-seed tests is a known anti-pattern.
  
  *Fix:* Report the across-seed CI on the mean paired delta (one-sample t or seed-level bootstrap): mean +0.037, 95% CI ~ [-0.04,+0.12], not significantly different from 0. Demote '2/5 seeds significant' to a footnote and change 'fragile' to 'no significant emotion gain at the across-seed level' wherever the result is summarized.
  
  *Why new:* The ledger's fix was 'emotion re-run multi-seed (fragile 2/5) and reported honestly.' The reviewer shows the inference METHOD of that fix is statistically wrong: the headline robustness statistic is a vote count, and the cleanest statistic (across-seed mean CI, which spans zero) is the one omitted -- so the applied fix is insufficient and its prose ('fragile') overstates a result that is null. (The fix actually strengthens the paper's negative thesis.)

**[MAJOR] F7-evidence-accumulation-confound** (re-run-experiment) @ §9 main.tex line 911 (leakage control), line 909 (novel-query split), line 928/957 (M5 compounding vs single-shot)
  
  The Phase-1 leakage controls (raw embeddings only, novel-query split) do not rule out the evidence-accumulation confound: across sessions the agent accumulates strictly MORE per-speaker audio, and more enrollment audio trivially raises speaker-verification and affect-readout accuracy, so a positive compounding slope is the expected consequence of data quantity, not of any self-evolution. The 'compounding vs single-shot baseline (empty memory)' contrast (M5) is confounded because the single-shot baseline sees only the current session; only the vs-classic contrast controls it, and only if the ECAPA+dictionary baseline is fed the IDENTICAL accumulated audio -- which the plan does not state.
  
  *Fix:* Add a fixed-audio-budget / evidence-matched control: hold total per-speaker audio (or number of enrolled utterances) constant across episode index so the slope cannot be driven by accumulation; and specify that the classic baseline receives the same accumulated per-speaker evidence as the agent. Demote the vs-single-shot contrast, which cannot separate self-evolution from accumulation.
  
  *Why new:* The leakage/novel-query controls are the round-1 benchmark-hardening fixes in the ledger. The reviewer shows they are insufficient against a specific, likely-dominant confound they do not touch (acoustic-evidence quantity), so the headline compounding result remains attributable to audio accumulation rather than agentic intelligence.

**[MAJOR] F8-tautological-rerank-metric** (reframe) @ tab:opB main.tex line 805 ('+ conservative rerank 0.715 0.845 (0 regressions)') and line 791
  
  URO '+ conservative rerank: 0.715 -> 0.845 (0 regressions)' reports a tautology in place of a CI. A conservative rerank that switches a candidate only when the verifiable reward improves cannot, by construction, regress on that reward -- '0 regressions' is guaranteed definitionally, not measured -- yet it is presented as evidence of a clean +0.130 gain.
  
  *Fix:* Replace '(0 regressions)' with a paired-bootstrap CI on the per-item delta for the rerank step, state explicitly that zero regressions is a structural property of an improve-only selector (not a finding), and if the rerank reward differs from the eval metric report regressions on the EVAL metric (where they are possible).
  
  *Why new:* Not in the ledger. A specific tautological-metric defect in the current table -- exactly the 'manufacture apparent robustness' pattern the revision claims to avoid -- distinct from the scoped multi-seed re-run.

**[MAJOR] F9-provenance-underspecified** (re-run-experiment) @ tab:opB main.tex lines 793-808 and reconciliation paragraph line 791; sample-size statement line 745
  
  The SLURP/MInDS provenance reconciliation is honestly disclosed but the numeric mapping is under-specified: the SLURP baseline silently moves 0.522->0.550 and the 'after' 0.894->0.880 with the selection rule unstated; tab:opB shows TWO MInDS rows with different baselines (0.883 and 0.852) under a caption claiming 'one reconciled baseline per task'; MInDS +0.089 is the only entry with no CI; and n for SLURP and URO is never given (only CREMA-D and MInDS n stated).
  
  *Fix:* State the exact selection rule and dataset slice yielding each baseline/after pair; give n for SLURP and URO; give a CI for MInDS +0.089 or remove it; present a single canonical MInDS row (alternative in appendix) or rename the caption to 'primary + alternative configuration.'
  
  *Why new:* Not in the ledger. The reconciliation paragraph was added round 1, but a disclosure that names a conflict without resolving which number is canonical (and contradicts its own 'one reconciled baseline per task' caption) is still under-specified and not reproducible.

**[MAJOR] F10-baseline-update-rule-unpinned** (cut-or-scope) @ §9 main.tex line 905 ('Primary baseline') and M5 line 957
  
  The primary paralinguistic baseline -- 'a speaker-keyed dictionary that stores per-speaker affect/role state' -- does not fix its accumulation/update rule (last-write-wins vs running centroid vs online change detection). A strong baseline (running centroid + drift detector) likely closes the M5 gap; a weak one (last-write-wins) makes any agent win meaningless. The plan asserts the baseline is 'deliberately strong' but pins no update logic, leaving a degree of freedom that can manufacture or erase the headline effect post hoc.
  
  *Fix:* Pre-register the baseline's exact accumulation/update/delete logic (e.g., per-speaker running ECAPA centroid with k-shot enrollment, SER majority-with-decay, explicit change-detection threshold) in the locked artifact, and justify it as the strongest simple pipeline a practitioner would deploy.
  
  *Why new:* The ledger added the ECAPA+SER baseline (benchmark hardening). The reviewers show the baseline as specified is incomplete: its informativeness for the load-bearing M5 paired-bootstrap contrast is undefined until the update rule is frozen -- a residual researcher degree of freedom the round-1 fix did not close.

**[MAJOR] F11-system-novel-axis-unbeatable** (cut-or-scope) @ §8 main.tex lines 824, 866, 879; §9 lines 887, 905, 926-928 (Phase-2 asymmetric pre-registration); §10 line 980
  
  The system's novel axis (the cross-session paralinguistic loop) has no specified mechanism to beat the pre-registered strong baseline: the paper concedes the omni embedding is at chance on speaker (so the paralinguistic store IS ECAPA/SER, the baseline's store), the policy only verbalizes a decision determined by retrieved ECAPA/SER state, and skills can never be admitted on paralinguistics (verifiable-only gate, line 866). Phase-2 then pre-registers a NULL on paralinguistics. So the 'self-evolving omni speech agent' reduces, on its differentiating axis, to drift-prone memory curation over the same encoder the 50-line baseline reads -- and the predicted-success axis (content/intent compounding) is conceded non-novel memory-RAG. C4's 'worth building' is unsupported by any hypothesized winning mechanism.
  
  *Fix:* Either (a) write down a concrete paralinguistic query class and the mathematical reason agentic state beats a strong dictionary (e.g., Bayesian multi-session speaker-evidence integration under genuine channel variation single-enrollment ECAPA misses) and add an ablation isolating that mechanism (curated graph vs running-centroid dictionary, same front end); or (b) honestly demote the system from a flagship 'worth building now' contribution to a minimal probe rig whose purpose is the negative result + benchmark, building only what those require.
  
  *Why new:* Not in the ledger. The round-1 changes (teethed baseline, demoted OSA-3, honest Phase-2 null) sharpen the problem rather than resolve it: M5 is a pre-registered falsifier for the flagship claim with no proposed path to passing, which two reviewers independently flag as a system-contribution concern the revision created rather than answered.

**[MAJOR] F12-calibration-contradicts-labelfree** (reframe) @ §8 main.tex line 847 (decouplings 1 and 2), line 859 (KL does not stop the Goodhart fixed point)
  
  The cross-session paralinguistic loop's only safeguard against the conceded self-reinforcing Goodhart fixed point includes 'periodic calibration against held-out human-labeled probes' (line 847). This covertly reintroduces ongoing deployment-time human supervision, contradicting the 'no oracle at deployment / label-free' premise the rest of the system rests on, and is entirely uncosted; if such labels are available per deployment population they could simply relabel the store directly. The companion safeguard ('sibling extractor where possible') shares the ECAPA family's systematic channel bias, so the 'independent pass' is either correlated (no real check) or just noisy.
  
  *Fix:* Cost the calibration loop explicitly (human labels per deployment population, per drift event, per new speaker) and compare to periodically re-reading the encoder; replace 'sibling extractor where possible' with a committed, genuinely independent reward extractor and report its empirical agreement-with-truth, or drop the decoupling claim. Add a deployment-without-calibration ablation to expose the drift the safeguards are meant to prevent.
  
  *Why new:* Not in the ledger. The system honestly names the gate a self-consistency gate (round-1 honesty), but the specific internal contradiction -- that its anti-drift safeguard requires an ongoing, uncosted human-label stream at deployment, violating the system's own label-free premise -- is newly surfaced and undercuts the deployment story.

**[MAJOR] F13-negative-overgeneralized-to-policy** (cut-or-scope) @ §7 main.tex lines 745-769; §10 lines 1028-1039 ('hidden precondition violated'); C3 line 213
  
  The paralinguistic negative is established on exactly ONE content bi-encoder (omni-embed-nemotron-3b) via a linear/kNN probe, where near-chance 91-way speaker ID is near-definitional (content embeddings are not speaker encoders -- that is why ECAPA exists). The negative is then generalized to 'frozen omni models do not afford paralinguistic per-block rewards' and to Conjecture-1 refutation for 'paralinguistic factors' broadly, but the generative Operator-B policy -- the actual proposed paralinguistic actor -- is never tested for paralinguistics; only the Operator-A embedding probe is. The negative therefore does not bound the proposed policy.
  
  *Fix:* Either broaden the negative to multiple frozen omni models including generative-omni paralinguistic decoding on power-adequate, decontaminated sets, or scope the claim precisely to 'one content bi-encoder's linear-probe geometry' and stop generalizing the embedding-probe null to the generative Operator-B policy or to 'frozen omni models' as a class.
  
  *Why new:* The ledger reports the emotion re-run and demotes the two-omni embedding-memory claim, but the reviewers show the negative's SCOPE is over-stated: it is a single-encoder, near-definitional probe result presented as a general statement about frozen-omni paralinguistic capability, and the proposed generative policy is never tested -- a scope defect the round-1 honesty pass did not bound.


### Re-raised but already addressed (chair rebuttal)

- OSA-2 / qstar_product being a 'null presented as structural contribution' (Rev4.7): the isolation-adds-nothing reframe IS the applied honest fix in the ledger; calling it self-canceling is a significance re-litigation of a settled reframe.
- gain_pos_of_nonconstant is a 'trivial one-line Mathlib corollary' (Rev4.1): the new strict-positivity theorem was the round-1 substance fix; triviality is a significance judgment on a settled addition (the genuine NEW issue is the KL-direction typo in its proof, F1).
- Op-B content/intent numbers are single-seed (Rev4.4, Rev5.2): the multi-seed re-run + committed artifacts are EXPLICITLY scoped as future work with teeth in the ledger. (The distinct, not-scoped defects in the current tables -- tautological rerank F8, provenance under-spec F9 -- and the abstract still headlining +0.330/+0.335 without a single-seed caveat are the residual items; the re-run itself is scoped.)
- Lean machine-checks trivia / quantitative bounds consumed as hypotheses (Rev4.9): qualified machine-checked claim is in the ledger; the genuine residual is only the false 'Pinsker discharged on paper' wording, captured in F2.
- Emotion fragile result reported (Rev5.1 base): the multi-seed re-run is in the ledger; the NEW item is the wrong inference method (vote-counting vs across-seed CI), captured as F6.
- Family-(B) model-dependent / circular emotion reward (Rev4.10): the label-derived vs model-dependent reward split (rem:rewardfamilies) is the applied round-1 fix.
- Contamination of CREMA-D / public benchmarks (parts of Rev4.5): contamination caveats and the Phase-0 contamination screen are already in the paper and the ledger's benchmark hardening.
- Deployment-time gap for paralinguistics / self-consistency gate (Rev2.1, Rev3.4 in part): §8 already concedes the paralinguistic loop degenerates to a self-consistency gate; the residual NEW item is only the unqualified abstract wording 'verifiable-reward acceptance gate,' folded into F2.