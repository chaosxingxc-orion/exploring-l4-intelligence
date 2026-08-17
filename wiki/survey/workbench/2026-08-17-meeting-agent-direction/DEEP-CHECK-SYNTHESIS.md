# Deep-check synthesis — meeting-minutes-agent scheme (coordinator verdict)

Date 2026-08-17 (night). Input: the six-agent adversarial workflow (3 deep-reading clusters over
the primary priors fetched in full text; 3 adversaries: topic-soundness / literature-positioning
/ methodology). Full structured output: workflow run `wf_d6404f0b-867` journal. Score: 2 FATAL,
24 MAJOR, 7 minor. This synthesis is the operative verdict; every adopted change below is
REGISTERED — the L4 preregistration and E-track implementations must conform.

## 1. The two FATALs and their resolution

**F1 (both adversaries, convergent): the meeting-domain glossary-GAIN claim has no valid
substrate today.** AMI is entity-poor by our own census (0.22% proper-name tokens); earnings
calls are not meetings; MeetingBank has entity mass but its references are Speechmatics ASR
output and its "minutes" are per-bill Legistar descriptions — no verbatim transcript gold.
RESOLUTION (adopted): (a) the core claim is re-scoped to **"episode-local self-built glossary
for entity-dense long-form speech"**, with meetings as the attribution/long-form-structure
domain; (b) a registered **substrate decision gate** precedes G3/G5: an ICSI entity census (ICSI
ships NE gold) + the MeetingBank re-census, against a pre-declared density floor (≥10 distinct
proper-name terms/episode AND repeat payoff ≥0.4, anchored to EGTA's ~10-terms/doc operating
point) plus a reference-adequacy requirement (verbatim transcript gold for any WER-family
claim); (c) MeetingBank's valid surfaces are summarization/QA/segmentation only.

## 2. Corrections of record (fix before L4; workbench methods.md carries two verified errors)

1. **EGTA is NOT frozen**: Qwen3-Omni-30B-A3B with trained LoRA (r=16, 220K chunk examples;
   only the audio encoder frozen) plus a decoder logit-bias channel (B=2). The methods.md
   "Frozen? Yes (no fine-tuning)" row is false and must be fixed.
2. **No EGTA-R-alone number exists anywhere in EGTA** (all headline tables are RG or G-only).
   The methods.md claim that "its ablation separates our channel from theirs" cites a
   nonexistent result. Corrected positioning: the prompt-only channel's standalone contribution
   is UNQUANTIFIED in the literature — our G2 prompt-only arm is the **first quantified
   prompt-only term-injection result on this model family**, and that is a claim anchor.
3. **The 2511.18774 "naive trap" is mischaracterized in our docs**: the degradation
   (15.79→29.01 avg) is an AUXILIARY model's first pass injected into Whisper's |PREV| token,
   condition-dependent (CV15 IMPROVED 15.55→10.40; MGB2 collapsed 16.02→47.61),
   mechanism plausibly Whisper-specific. On Qwen3-Omni the naive arm is an open measurement;
   prereg must not presuppose its direction. Its "multi-speaker dialogue" trigger and its
   self-prefixing result (12.27 best variant — restructured self-derived supply works) are the
   honest citations.
4. **Gating per se is occupied ground** (EGTA Algorithm 1 + activation audits + shuffled-memory
   control). Our anchor is the CONJUNCTION: term table manufactured from the episode's own
   errorful first pass + incremental cross-chunk carry + construction-time gate + truly-frozen
   API-only prompt-level core. Provenance alone is a footnote (BabelDOC + self-prefixing).
5. **Audio-Mind phrasing purge**: no claim sentence may use "conditional evidence acquisition"
   / "bounded external evidence"; differentiate on: self-built episode-local state vs external
   tools; long-form meeting carry (their stated Limitation); no second LLM; WER/attribution
   claim surface.
6. **MeetingBank license**: declared cc-by-nc-sa-4.0 on both HF channels — the owner's
   undeclared-default never triggers here; ShareAlike binds released derived subsets.

## 3. Registered design changes (adopted into the workplan)

1. **G2.0 kill-gate smoke** (flies FIRST): oracle-supply keyword arm on the earnings substrate
   with a pre-declared minimum keyword-F movement — below it, the prompt channel is declared
   inert for this core and the topic re-scopes before further spend. (No published evidence
   shows a truly frozen core consumes prompt glossaries zero-shot; CTC-Assisted trained it in.)
2. **G2 full arm matrix** (registered before flight): zero | naive-raw | scrambled-raw
   (de-sequentialization control) | uniform-ungated glossary (gate control; EGTA A.6 shows
   un-gated hurts even with clean lists) | gated glossary | deranged glossary (EGTA
   shuffled-memory template, cited as such) | oracle ceiling (labeled) | **no-carry**
   (chunk-local glossary, state reset per boundary; carry-delta is a named line with a kill
   criterion: carry-delta ≤ 0 kills the cross-chunk-carry claim, falling back to the
   construction-time-gate claim) | **single-pass** (for ≤40-min episodes: no chunking at all;
   chunked+glossary must at least recover the measured chunking cost — the AutoMin 2025 lesson:
   long-context GPT-4o 7.74 beat every bespoke system's 4.55) | **provenance factorization**:
   speech-derived-only vs metadata-only vs combined glossaries (metadata-only doubles as the
   EGTA-analogue baseline; the provenance claim is licensed only if speech-only adds measurably
   over metadata-only). E4 glossary entries carry per-term provenance tags.
3. **Leakage tiers, machine-enforced in E4**: Tier-M0 = artifacts co-shipped with the audio as
   meeting materials (agendas, slides, press releases) — runtime-admissible; Tier-M1 =
   annotation/reference-derived artifacts (earnings oracle/bias lists, ConEC corrected
   references, speaker-metadata name maps, Contextual-E22 GPT-5-over-gold lists, AMI
   roles/seen_type) — ceiling/diagnostic only. Fail-closed before any model contact.
4. **Metrics pins (E5)**: PRIMARY confusion cost = tcpWER − tcORC-WER at collar 5 s on
   identical per-speaker streams (cpWER − ORC-WER demoted to literature-comparable secondary
   with the reordering-inflates-ORC caveat); machine check that the pipeline emits real
   per-segment timestamps (anti-gaming); glossary-induced-substitution diagnostic on every
   glossary arm (kill: induced substitutions ≥ entity true-positive gains ⇒ net-harmful);
   EGTA's unsupported-activation-rate audit adopted as a Tier-0 diagnostic; MeetingQA scoring =
   macro-F1 + IoU with empty-string abstention and a hashed normalization layer.
5. **MeetingQA headroom language retired** until G1 measures the frozen-core zero-shot floor
   (57.3 is a 2023 fine-tuned DeBERTa, not an LLM floor; the human 84.6 is a 250-question
   estimate; the gap is dominated by abstention and multi-span, which the glossary does not
   touch).
6. **Power discipline**: after G1, per-meeting bootstrap CIs and per-metric MDEs from zero-arm
   variance; paired per-meeting permutation tests; deltas below MDE are reported as null. Kill:
   AMI-dev MDE > 2 cpWER points retires AMI as a gain substrate (NOTSOFAR-1's own indictment of
   18/16-session sets).
7. **AMI role registry**: frozen overlap matrix across the ASR partition, seen_type convention,
   MeetingQA's 80:10:10 split, and M3-SLU's AMI-derived instances; every meeting gets exactly
   one role (glossary-discovery / ASR-eval / QA-eval), machine-checked fail-closed; straddling
   M3-SLU instances quarantined.
8. **Falsifiability in L4**: H1 (on entity-dense episodes, gated self-built glossary beats
   zero AND naive AND scrambled AND uniform arms on keyword-F/entity-WER, prompt-only, truly
   frozen) and H2 (content supply moves entity metrics but not attribution; roster supply moves
   the confusion cost — the M3-SLU dissociation) stated verbatim, with kill patterns bound to
   pre-declared consequences (halt / re-scope / negative-result publication).
9. **Window-invariant claim restatement**: "compact, gated, self-derived supply beats raw
   self-derived context at equal or lower token cost, even when the raw context fits the
   window" — so the contribution survives cores with longer windows; cross-chunk carry is the
   long-form special case, tested where length genuinely binds.

## 4. What the check CONFIRMED (unchanged)

The conjunction is unoccupied (verified against full paper texts); audio-grounded QMSum is
unprecedented; M3-SLU quantifies the attribution gap on this core family; the judge-free
headline reflex and the G3 census-driven reframe were sound; E1/E2/E5 architecture stands.
