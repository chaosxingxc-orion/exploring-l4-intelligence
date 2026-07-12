# v4.1 Release Conformance Report (internal consistency check)

> **Nature.** This is a machine-assisted **internal consistency check**, executed by an independent
> conformance checker prior to release of the v4.1 package. It is **NOT an external peer review** and
> does not constitute owner sign-off. It verifies that the v4.1 proposal and its accompanying response
> letter conform to (a) the authoritative claim ledger, (b) the owner rulings in Decision-Log 续24, and
> (c) the four FUNDAMENTAL / numbered dispositions of the v4 adversarial integrity review.

- **Report date:** 2026-07-12 (Asia/Singapore)
- **Checker:** independent conformance checker (Opus, read-mostly; one mechanical fix applied — see §Fixes)
- **Rule-list version:** `v41-conformance/rules-2026-07-12` — derived verbatim from Decision-Log 续24
  (R1–R4), the standing rules carried from prior rounds (eligibility-headline scope, reference-freshness
  ≥2025-01, milestone-gate DAG, ledger-conformant-citations-only), and the six numbered CHECKS in the
  release brief.

---

## (a) Inputs and SHA-256 (as reviewed / as released)

Computed via PowerShell `Get-FileHash -Algorithm SHA256`. The response letter hash is the **post-fix
(released)** version — one mechanical fix was applied during this check (§Fixes).

| # | File | SHA-256 |
|---|------|---------|
| 1 | `wiki/2026-07-12-research-proposal-v41-external-review.md` (v4.1) | `10CC5F23AD120EEF8846B560B07B51E6ECF61CDB8FB309EF08F1440DE42286E0` |
| 2 | `wiki/Project-Thesis.md` | `0604F15357C080CF8BE519CB16A92DB1A3F08B8E031EAAE38E1F3D9C30566B5B` |
| 3 | `wiki/Per-Work-Status.md` | `6AA8B963A078E238EFE082D0376113FBA799B181B1E8B0A7DEB5138ACF31732B` |
| 4 | `wiki/2026-07-12-response-v4-to-adversarial-integrity-review.md` (letter, post-fix) | `88CA75EDC4251CEED3E30097FEC682F37FC8E1C1E3C0688CCE186B3FBE3BDAEE` |
| 5 | `docs/claim_ledger.yaml` | `C7A29949A2EF5C493E9359E67605F345110CA8E4095DA5DD524B9FEF8C4DB73D` |
| 6 | `wiki/Decision-Log.md` | `B016E4EC5004765E18313980ADC3279F64786B443E499B43AED2E8675E744E5E` |
| 7 | `wiki/2026-07-12-research-proposal-v4-adversarial-integrity-review.md` (review) | `2F06E88ADC9A5CFC4F221F7E413F9DFD50244549C1DBF1F19FA013A8F8C25903` |

---

## (c) Per-check verdicts

### CHECK 1 — LEDGER CONFORMANCE — **PASS**

Every claim-ledger citation in v4.1 and the letter matches ledger status exactly. Note: the tokens
`C-1..C-6` in v4.1 (lines 118, 150, 218, 220, 222, 234, 286, 320, 407, 486, 488) and in the letter
(§2) are **review-finding IDs** (the review's construct findings C-1..C-6), not ledger claim IDs — they
carry no ledger status obligation. `CTC-WS` (v4.1 line 69) is a biasing-technique name (false-positive
on the `C-…` regex), not a claim ID.

| Ledger claim | Ledger status | v4.1 / letter treatment | Verdict |
|---|---|---|---|
| C-MINDS-V2 | directional | v4.1 §1.4 L56 (+0.246/+0.262/−0.245 [−.286,−.201] with ~3% / +3/107 overlap caveat), §8.2 L236 "不作『标准卡 schema 已证』"; letter E1 "改回 directional". **Never called valid.** Numbers match ledger to the digit. | PASS |
| C-KEEP (nonexistent) | no ledger entry | v4.1 §1.4 L57 "原 C-KEEP 不存在…unverified、待 mint、不作设计依据"; letter E2 "降 unverified". Explicitly flagged nonexistent; 24% adoption number never used as evidence. | PASS |
| C-T7 | invalid | v4.1 L61 (discipline: only in appendix D, invalid, "绝不作 §7 动机"), L345 (P1 failure-mode prevention, invalid), L509 (appendix D failure history); letter E3 "引用作废". Never a motivator/positive evidence. | PASS |
| C-ASR-V2 | directional | v4.1 §1.4 L58 (clean +0.0094 [.0034,.0165], snr5 +0.0081 [.0005,.0161]; "全家族 Holm 校正后两条件均不存活"; "已退出系统设计"). Numbers match ledger; correctly not upgraded. | PASS |
| C-BASELINES | directional | v4.1 §1.4 L59, §9.1 L248 "directional inventory, git_dirty=true, engine/revision/hash 空". | PASS |
| C-M3 / C-PHASEA / C-MINDS-POLICY | invalid | v4.1 §11 L345 (P1/P2/P3 prevention) + appendix D L509; all labeled invalid, failure-history only. | PASS |
| C-MINDS-2TURN | (nonexistent) | grep of v4.1 + letter: **absent**. | PASS |
| HB-16 / HB-23 (letter §4a) | survey-anchor refs (not in ledger) | Used only to argue BR-ASR/RECAST/HyDE were previously cited; they anchor real literature, not empirical result-claims. Not ledger-tracked; no status obligation. | PASS (noted) |

Baseline evidence discipline holds: SQuAD-zh locked = **0.85 [0.725,0.95]** and uro-bench-SQuAD-zh =
**0.925** are listed separately (v4.1 §9.1 L253–254), matching the ruling.

### CHECK 2 — RULING CONFORMANCE (R1–R4) — **PASS**

- **R1 (no cost success gate; correct cost accounting).** No cost-based success gate anywhere. `30%` /
  `Pareto` / `调用降幅` appear only in (i) appendix D L513 (documenting the **removed** gate: "S3 成本类
  成功门…数学不可达，R1 撤除") and (ii) letter §3 F-1 L74–75 (describing the removal). Active text is the
  opposite: §3.3 L117 "不设任何成本成功门（R1）", §7.1 L210 "成本不进任何成功门、不作 Pareto 支配主张".
  Cost accounting is present and **arithmetically correct**: §7.1 L212 "触发 item = m+1 = **6** 遍（m=5）；
  未触发 = **5**；恒检索 = **2**/item；从不 = **1**" — verbatim to R1; also input+output tokens / wall-clock
  latency / GPU-seconds; efficiency optimization explicitly deferred (§7.1 L214). Letter §3 F-1 L76 repeats
  the same arithmetic. **PASS.**
- **R2 (strict black-box core; independent-embedder speech-vector flagship; hidden state diagnostic-only;
  W4 untouched).** Flagship retrieval key = independent frozen embedder speech vector, GLAP / omni-embed-
  nemotron, framed as an external system component (§5.2 L162, §5.3 L168–169). Core 2048d hidden state is
  a white-box DIAGNOSTIC arm "排除于一切 portable/deployable 头条主张" (§5.3 L171). own-ASR→text kept as
  modality-bridge arm (§5.3 L170). W4 narrative explicitly untouched (§5.3 note L174; §12 L359). **PASS.**
- **R3 (operator fully specified + equal-budget controls + ρ = G0).** §4 specifies action space (§4.1),
  frozen-sampling policy (§4.1), deployable output-side verifiable reward (§4.2: self-consistency /
  verifier-agreement δ_corr / elicited confidence), selection rule argmax (§4.3), stopping rule + budget
  cap N* (§4.3), and ρ = (R_selector − R_greedy)/(R_oracle − R_greedy) (§3.2 L109). Equal-budget controls
  named: **random selection / MBR medoid / single-pass RDU (K=1)** with matched K budget (§4.3 L145). ρ
  restores owner-signed G0 (§3.2). Lean #27 bound to the same operator, unconstrained-failure +
  constrained-convergence under τ and N* (§4.4, §10.2). **PASS.**
- **R4 (no custodian/commit-reveal/burn; tutorial-reproduction standard).** Every occurrence of
  `custodian` / `commit–reveal` / `burn` is in the REJECTION/abandoned context: §11 L341 "拒绝审查者的
  『全部锁死』路线（独立 custodian、commit–reveal、burn 记录一并否决，含最小 commit–reveal 变体）";
  §12/appendix-D echoes; §14 sign-off L410 "不采用 custodian/commit-reveal/burn"; letter §5 L109 quotes
  the owner rejection verbatim. Tutorial-grade reproducibility present: §11 L341 "① tutorial 级可复现…②
  零数据集泄漏…③ 零学术欺诈" + REPRODUCE.md contract + deterministic script + fixed seeds (续21-B①).
  **PASS.**

### CHECK 3 — REVIEW COVERAGE — **PASS** (all CONFIRMED findings disposed)

Every numbered review finding maps to a v4.1 section, an engineering ticket (#37, explicit deferral for
implementation-level items), or an explicit acknowledgement. No CONFIRMED finding is left without a
disposition.

| Finding | Review verdict | Disposition (v4.1 / ticket) | OK |
|---|---|---|---|
| F-1 cost gate unsolvable | CONFIRMED | §7.1/§9.3 whole cost-gate family removed; descriptive accounting | ✓ |
| F-2 hidden-state key vs black-box | CONFIRMED | §5.2/§5.3 independent-embedder key; hidden state → diagnostic | ✓ |
| F-3 RDU not yet TFRL | CONFIRMED | §4 operator + §3.2 ρ restored (Path B) | ✓ |
| F-4 identity drift | CONFIRMED | §12 transactional lineage refresh (Thesis/Per-Work-Status/proposal/letter) | ✓ |
| I-1 pseudo-Q wrong-object risk | PARTIAL | §6 corpus-manifest input; impl → #37 | ✓ |
| I-2 K2 word-WER on Chinese | CONFIRMED | §7 CER (中文 CER); impl → #37 | ✓ |
| I-3 `supported` not live | CONFIRMED | §5.3 nemotron; status → #37 pending-live-verification | ✓ |
| I-4 q2q form≠modality | CONFIRMED | §6.2 form-bridge HYPOTHESIS; modality×form×delivery factoring | ✓ |
| I-5 default text embedder no audio bridge | CONFIRMED | §5.2 frozen query path; `auto` ban → #37 | ✓ |
| I-6 tests verify plumbing not science | CONFIRMED | letter I-6 "tests pass = plumbing readiness only" | ✓ |
| I-7 M1 not clean-checkout | CONFIRMED | §9.8 / M1 gate: freeze commit, git_dirty=false | ✓ |
| I-8 baseline id mismatch + empty provenance | CONFIRMED | §9.1 SQuAD-zh 0.85; uro-bench single-row; directional inventory | ✓ |
| I-9 CLEAN/content_hash coverage | CONFIRMED | §9.8; KB manifest provenance fields → #37 | ✓ |
| S-1 MAX=15 ≠ 15 atoms | CONFIRMED | §9.5 + appendix A atomic manifest, primary m=7 | ✓ |
| S-2 eligibility rewrites population | CONFIRMED | §9.4 headline scoped to headroom-qualified | ✓ |
| S-3 SESOI moving threshold | CONFIRMED | §9.3 15%→10% fallback removed; engineering futility only | ✓ |
| S-4 10% no business basis | CONFIRMED | §9.3 labeled "conventional scientific threshold", not business | ✓ |
| S-5 fixed-effect pooling hides failure | CONFIRMED | §3.1/§9.5 focus primary + replication no-harm, no heterogeneous pooling | ✓ |
| S-6 5 rounds ≠ 1 confirmatory | CONFIRMED | §9.5 one-version-one-round, new registered version on failure | ✓ |
| S-7 holdout supply pre-sign | PARTIAL | §9.5 α=0.01 equal-split removed → per-version α; holdout-supply sign-off gate retained | ✓ |
| C-1 oracle-iff-need false | CONFIRMED | §7.2 L1 renamed responsiveness, four potential-outcome states P(Y₁−Y₀>0) | ✓ |
| C-2 L3 additive identity false | CONFIRMED | §7.2 descriptive taxonomy; sequential counterfactual/Shapley | ✓ |
| C-3 standard-card effect unisolated | CONFIRMED | §8.2 equal-content A/B (vary schema/turn only) | ✓ |
| C-4 theory lower bound missing necessary cond. | CONFIRMED | §10.2 r₀·Δ_deliver ≥ (1−precision)·c_distractor as MEASURED assumption | ✓ |
| C-5 "零结构改动" terminology | CONFIRMED | throughout: "零权重、零核心结构改动；外挂系统组件另加" | ✓ |
| C-6 S4 mixes three constructs | CONFIRMED | §9.6 three-construct split (factual / schema / entity biasing) | ✓ |
| §7 literature nearest-neighbours | PARTIAL | §2.1 novelty matrix (6 new + 3 already-cited neighbours) | ✓ |
| E-1/E-2 ledger conflict / CLEAN untraceable | CONFIRMED | §1 errata (letter) + §11 checker artifact | ✓ |
| E-3 public seed ≠ custodian | CONFIRMED | §11 disclosed custody limitation (per R4 rejection of custodian machinery) | ✓ |
| E-4 future-date breaks chronology | CONFIRMED | v4.1 + letter dated 2026-07-12 (matches Git day); M1 decisions = prior exposure | ✓ |
| §9 QRP (recurrence) | CONFIRMED | §1 machine gate + independent integrity oversight | ✓ |

### CHECK 4 — MATH — **PASS**

- **Primary confirmatory family size.** Appendix A lists exactly **7** primary atoms: H_SYS_FOCUS,
  H_SYS_REP1, H_SYS_REP2, H_SEL_RHO_FOCUS, H_SEL_VS_RANDOM, H_SEL_VS_MBR, H_SEL_VS_SINGLE. §9.5 decomposes
  it as 1 focus system-effect + 2 replication no-harm + 1 selector ρ + 3 equal-budget controls = **7**;
  Holm within family, m=7. Manifest count == prose count == 7. ✓
- **Cost accounting.** m=5 ⇒ triggered = m+1 = **6**; untriggered = **5**; always-retrieval = **2**;
  never = **1** (§7.1 L212). Consistent with R1 and with the review's F-1 model (per-item-type costs;
  the review's population-average 5+p is a different, compatible quantity). ✓
- **Baseline numbers vs locked artifacts.** SQuAD-zh = 0.85 [0.725,0.95] (§9.1) and uro-bench-SQuAD-zh =
  0.925 (§9.1) match the ruling and are kept as distinct artifacts. ✓
- **FWER arithmetic.** No numeric FWER computation is asserted in v4.1 (correction = Holm within the m=7
  family; per-version α declared at registration; secondary S1–S4 family carries its own multiplicity and
  is excluded from the primary denominator). Nothing to recompute; no arithmetic error. ✓
- **Removed-gate arithmetic (appendix D).** The documented-as-removed S3 gate (5+p ≤ 0.7×2 = 1.4,
  unsolvable ∀p∈[0,1]) is correctly characterized as mathematically unreachable. ✓

### CHECK 5 — CROSS-DOC CONSISTENCY — **PASS**

| Axis | v4.1 | Thesis | Per-Work-Status | Letter | Consistent |
|---|---|---|---|---|---|
| Work identity | §12: W1 primary study (RDU + selector); W4 separate, untouched | supersession note: W1 carries primary study; W4 separate, repositioned per G0 | board + notes: W1 now carries primary study; W4 repositioned per G0 | §4/F-4: W1 identity refresh, W4 untouched | ✓ |
| Primary metric | ρ = (R_selector − R_greedy)/(R_oracle − R_greedy) (§3.2) + ≥10% scoped headline (§3.1) | ρ (G0) | ρ realization rate | ρ (F-3 note) | ✓ |
| Headline scope | headroom-qualified knowledge-dependent speech tasks (§9.4) | — | — | ④ headroom-qualified | ✓ |
| Custody standard | tutorial-grade reproducibility; no custodian/commit-reveal/burn (§11, §14) | — | — | §5 same (owner ruling quoted) | ✓ |
| Status | v4.1 pending external review + owner signature (not passed) | "pending external review + owner signature" | "v4.1 drafted, awaiting external review + owner signature" | §7 sign-off gate open | ✓ |

### CHECK 6 — SELF-CONTAINMENT — **PASS** (after one fix)

- **v4.1:** no workflow IDs, no model names (Opus/Sonnet/Fable), no orchestration references. The only
  "代理" token is §11 L343 "由独立 checker 代理执行" — a description of the claim-ledger-governance
  consistency-check mechanism (this very report), self-explanatory to an external reader and publicly
  committed to in the letter §7. Acceptable; not internal scaffolding. The "5 路独立复核" descriptor
  (frontmatter L9) is a verification-rigor count, not an agent/workflow reference. **PASS.**
- **Letter:** contained one internal workflow-orchestration ID `wf_1cb25cee-1f8` (§ intro, L15) — a
  scaffolding leak with no external meaning. **Fixed** (§Fixes). The remaining "协调层 / 定稿协调 AI"
  naming is retained deliberately: the reviewer-response protocol requires owning bookkeeping failures
  by name, so identifying the responsible coordination layer is accountability, not scaffolding.
  **PASS after fix.**

---

## Fixes applied (small mechanical only)

1. **Letter self-containment (CHECK 6).** Removed the internal workflow-orchestration ID
   `wf_1cb25cee-1f8` and the "5 路…复核代理" scaffolding phrasing from the letter intro (L14–15).
   Changed `按协议以 5 路独立复核代理对您 42 项可核验主张逐条核验（workflow `wf_1cb25cee-1f8`）：37
   CONFIRMED…` → `按协议以独立复核对您 42 项可核验主张逐条核验：37 CONFIRMED…`. Meaning preserved
   (independent claim-by-claim verification, 37/42 CONFIRMED / 0 REFUTED). The letter SHA-256 in §(a) is
   the post-fix value.

No structural problems were found; no BLOCKED items.

---

## (d) Overall verdict

**RELEASE-READY.**

All six checks PASS. Ledger conformance is exact (no nonexistent claim ID cited as evidence; C-T7 confined
to failure-history/discipline context; C-MINDS-V2 never called valid; C-KEEP/24% flagged unverified).
Owner rulings R1–R4 are faithfully implemented (cost gate removed with correct m+1=6 accounting;
independent-embedder speech-vector flagship with hidden-state demoted to diagnostic; fully specified
reward-guided operator with equal-budget controls and ρ = G0; tutorial-grade reproducibility replacing all
lock-everything ceremony). Every CONFIRMED review finding has a v4.1 section, ticket-#37 deferral, or
explicit acknowledgement. Math (family m=7, baselines 0.85 / 0.925, cost arithmetic) recomputes correctly.
The four canon documents state a single, consistent work identity, primary metric, headline scope, and
custody standard. Self-containment holds after removing one internal workflow-ID leak from the letter.

> This internal consistency check is not an external review and confers no owner sign-off; the §14 owner
> signatures, the holdout-supply proof, M1 clean-checkout green, and the real cross-modal live smoke
> remain the STOP-THE-LINE gates before Stage-2.
