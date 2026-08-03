# Current Survey Status

- Gate: direction-local pipeline; endpoint
  `DIRECTION_LOCAL_PIPELINE__R1_SUNSET__AUDIO_AWARE_EVIDENCE_ACQUISITION_FORMAL_OPENING_APPROVED__STAGE2A_EXECUTION_CONTRACT_PENDING`.
- Owner rulings (2026-07-27/28): core = Qwen3-Omni-30B via the local llama.cpp lane; ASR mainline =
  general ASR; this stage performs analysis/synthesis only and holds no execution authority; datasets and
  metrics are reused from reference papers or official benchmark protocols as the working default.
- Owner direction-viability criterion (2026-07-29, Decision-Log 续76): a research direction needs
  sufficient survey plus either in-domain prior work serving as a methodological comparison baseline, or
  cross-domain-informed design where the field is empty; both compare with incumbent SOTA on a task.
- R1 sunset is owner-confirmed (2026-07-29): `NO_GO_AS_STANDALONE_DIRECTION__SUNSET_BEFORE_STAGE2` —
  R1 lacked standalone direction potential, proposing only baseline exploration content. Its paper-derived
  datasets, baselines and metrics remain a reusable evidence package; no Stage-2B slot.
- Audio-aware evidence acquisition (source-candidate R2) is now
  `PASS_STAGE1C_FORMAL_OPENING` after the stage-aligned v20 multiround review on 2026-08-02. This closes
  problem selection and permits the Stage‑2A handoff; innovation/final method remain undecided. Red lines =
  no parameter modification, task-trained model or additional answering LLM; frozen tool-grade components
  are allowed (续78). AudioRAG/Omni-DeepSearch/VoiceAgentRAG are in-domain prior; official data has no
  negative class, so need detection cannot be evaluated without new labels.
- R3–R9 remain owner-unverified (`OWNER_UNVERIFIED`), but they are later candidate analyses rather than
  a global prerequisite for the first admitted study.
- Owner architecture ruling (2026-08-02): candidate IDs remain audit provenance. Only a GO plus execution
  contract creates a semantically named independent repo under `studies/`; R1 gets no repo. Engineering
  one study may overlap survey of the next candidate.
- Executor-proposed rulings C/D/E remain owner-unsigned; where they conflict with the 2026-07-29
  criterion, the criterion prevails.
- C1 reliability is a shared measure, not the primary problem; fixed-pool headroom gates no new context.
- Immutable evidence: Stage‑1B v5 `38fb9435d0c35e226ad62b16015a6dbee054e6c2`; 320-work union unchanged.
- R1 agreement remains `FAIL`. R2R1 passed 22 focused tests but remains
  `RETIRED_WITHOUT_DISTRIBUTION_OR_INDEPENDENT_ACCEPTANCE`; no calibration-validity claim follows.
- H5 remains withheld and non-load-bearing; no cross-modality effectiveness conclusion enters the portfolio.
- Data state: D0 is closed for Earnings21, Earnings22 and ConEC at pinned revisions; model-free D1–D4
  alignment, leakage, scoring and ten-sample trace checks remain open.
- Exposure: literature search/fetch/full-text and PDF-table review plus authorized dataset acquisition
  occurred; no model/API execution, metric run, reproduction or prototype occurred.
- Withheld: further unapproved data/model acquisition, model/API calls, metric runs, reproduction,
  prototypes, remote study-repo creation, Stage‑2 execution, push and Wiki publication.
- Next action: close D1–D4, freeze the Stage‑2A contract and request `OWNER_GO_AND_EXECUTION_CONTRACT`;
  after engineering begins, survey the next candidate in parallel.
