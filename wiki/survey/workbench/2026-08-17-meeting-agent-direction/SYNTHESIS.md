# Synthesis — meeting-minutes-agent go/no-go (coordinator verdict for the owner)

Date 2026-08-17. Inputs: local-audit.md (`f995191`), datasets.md/methods.md (`eeda182`), the
task-dataset expansion scan (`b179634`), and the 2026-08-17 acquisition receipts (`1677b07`).
This synthesis is the decision package; the three reports are the evidence.

## 1. Data feasibility — CLOSES

Local tonight: AMI with genuinely minutes-shaped gold (142 abstractive summaries with
abstract/actions/decisions/problems sections + summlink evidence grounding; 109 meetings
full-stack; annotation zips extracted), earnings21+ConEC as the glossary-mechanism substrate
(RTTM speaker turns 44/44, per-call ~790-term glossaries, participant names with affiliations),
ContextASR-Dialogue EN (5,273 speaker-attributed episodes, TTS).

Three cheap acquisitions close every named gap: **MeetingQA** (<50 MB) converts held AMI audio
into deterministic extractive meeting QA (human 84.6 vs model 57.3 F1 — measurable headroom);
**ICSI** (~9 GB, CC BY 4.0, NOT LDC-gated) makes every AMI result two-corpus and adds
summary+entity gold; **QMSum** (<100 MB) adds a query-focused layer over both. Optional
expansions: MeetingBank bounded subset (professional minutes + agenda/roster as metadata),
NOTSOFAR-1 (modern attribution substrate), M3-SLU (speaker-attributed QA; release UNVERIFIED).
Residual gaps and their handling: coreference gold — de-scope as a named function, measure
attribution through QA instead; per-speaker channels — mixdown-only accepted (ICSI adds
far-field channels).

## 2. Academic space — OPEN BUT CLOSING FAST

Four targeted searches: nobody publishes an episode-local, self-built glossary re-injected into
a frozen model. The three nearest priors define the claim boundary: EGTA (2607.17766, one month
old — offline external-document memory + logit bias; we are incremental self-built + prompt-only),
Zero-Shot Context-Aware ASR (2511.18774 — the warning: naive self-injection degrades WER 15.79
→ 29.01, so the abstract/normalise/dedupe/gate step IS the contribution and the naive arm is a
mandatory control), CTC-Assisted (2411.06437 — pass-1 filters a gold list, never creates one:
"list provenance is the whole of our contribution"). Must-address-in-writing: Audio-Mind
(2605.28480, "conditional evidence acquisition … bounded external evidence" phrasing) and
Dixtral (trained baseline). External validation of the entity-centric thesis: BFCL v4's
published failure mode ("models fail to correctly handle entity dictation") and M3-SLU's
headline ("capture what was said but fail to identify who said it").

Engineering shape: cascade dominates decisively (no AutoMin submission has ever consumed audio;
end-to-end walls at meeting length; our core caps at ~40 min/instance) — chunking is forced, and
the glossary is precisely the cross-chunk state carrier: the method and the constraint are the
same story. Evaluation: judge-free headline stack exists (MeetEval tcpWER/cpWER/ORC-WER with
cpWER−ORC-WER as the isolated speaker-confusion cost; MeetingQA F1; ROUGE legacy-row only;
LLM-judging fenced behind human calibration).

## 3. Program fit — RULED

Standalone topic (owner 2026-08-17): merges interleaved listening/spelling/revising; NOT
knowledge-injection framing (SAEA continues on non-meeting carriers); speaker-dimension state is
core and episode-local; only cross-meeting persistence is memory-gated. Repository scaffold
stands at `papers/meeting-minutes-agent` (PROVISIONAL).

## 4. Recommendation — OPEN (GO), with a scoped charter

Claim surface at open: (i) the episode-local self-built glossary loop, provenance-anchored,
prompt-only, with the naive-reinjection arm as a registered control; (ii) speaker-attributed
minutes + meeting QA on AMI+ICSI(+MeetingQA), judge-free headline metrics. De-scoped at open:
coreference as a named deliverable (folded into QA-measured attribution); cross-meeting memory
(future studies). First actions on GO: registry status PROVISIONAL→ACTIVE; acquisitions
MeetingQA+ICSI+QMSum (phase-2 acquisition agent); first design records (glossary-loop
preregistration with EGTA/2511.18774 positioning, chunking design, evaluation tier stack).

SAEA-side consequences already applied from the same evidence: spec corrections (SLURP resolved;
librisqa rejected for zero knowledge-coupling), and the SAEA acquisition candidates (SpokenWOZ,
WearVox, SpokenNativQA, SD-QA, AudioBench scoped) proceed independently of this decision.
