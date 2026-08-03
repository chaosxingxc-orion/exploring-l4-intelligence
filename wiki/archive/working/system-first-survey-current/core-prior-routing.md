# Core-prior routing at the Stage-1A gate

## Scope and decision boundary

This note closes only the Stage-1A identity, full-text, and survey-routing question raised by the
independent working-brief review. It is **not** an innovation matrix and makes no claim that the
program is novel, non-novel, better, or worse than these systems. The four items were supplied by the
reviewer and dereferenced by known identifier, so `query_recall_credit=false`; they are not evidence
that systematic discovery is complete.

Stage-1A asks whether each work is uniquely identified, locally reproducible as evidence, routed to
the correct survey lane, and represented by the protocol. Stage-1B will code and map method-path
proximity. Stage-1C may form candidate problem/gap hypotheses and select a problem. Reproduction and
technical-approach innovation converge only in Stage-2A.

## Hash-bound routing facts

| Work | Frozen local evidence | Stage-1A factual classification | Stage-1B coverage obligation | Deferred decision |
|---|---|---|---|---|
| Omni-Decision, arXiv:2607.11433 | PDF SHA-256 `132a11f78e1b85bda53af8edc24c9c9a4100a75644b7ce4f42f72ece4d1f374b`; eprint SHA-256 `75e3b9e94ffafdaa3433f6d6c3b6d3a7e9c9bdd0d849e436d28987e5e358ff2c` | P1 direct neighbor; `DEEPLY_READ`. PDF p1 calls it a training-free evidence-state system; p5 defines planner action selection and `can_advance`; p9 says it does not replace budget-aware action selection. | Code explicit evidence state, action lifecycle, validation/repair, stopping, information access, and budget reporting under RQ-SYS/RQ-SAFE/RQ-MEASURE-MAP. | No Stage-1A novelty verdict. Map proximity in Stage-1B; decide reproduction priority and approach only after Stage-1C selection. |
| AOP-Agent, arXiv:2605.28192 | PDF SHA-256 `bc09e0b8df4fe0e81dced64c71491ab5e1e748346ffc6d8f6b1a04659b85b9e3`; eprint SHA-256 `9bb03eee1129f0330ef0c2457966ae899a55d7772ae346fc2653b89bb9a1be4c` | P1 direct neighbor; `DEEPLY_READ`. PDF p1 states no additional training; p4 describes hierarchical omni-modal memory and an observe–reflect–replan loop whose reflector chooses whether more observation is needed; p9 records a non-streaming memory limitation. | Code memory topology, temporal granularity, observation/tool actions, multi-agent decision rights, state transitions, stopping, and modality-specificity under RQ-SYS/RQ-OMNI. | No Stage-1A novelty verdict. Map proximity in Stage-1B; decide reproduction priority and approach only after Stage-1C selection. |
| Light-Omni, arXiv:2607.05511 | PDF SHA-256 `676c77f205d6fee07350283679bcb3ca54712d45d590b67fa20b53442a62d257`; eprint SHA-256 `d71ec53d5075491c80d032cc73f91bef6c807359a09008414be4f0df0f9ecccb` | P2 trained/white-box boundary comparator; `BOUNDARY_COMPARATOR`, nonblocking. PDF p5 introduces learnable soft prompts; the full text reports trained adapters/joint optimization. | Retain in the trained-comparator and H5 modality-specificity strata; do not enter it into a training-free direct-method denominator. | Comparative effectiveness and any transferable technical choice are post-mapping questions. |
| LatentOmni, arXiv:2605.22012 | PDF SHA-256 `4cac09b2f7d06796a2d397fbfb903b583e8da7e1c89da6e70be6e9297f9da033`; eprint SHA-256 `cecc35f9f078a79805f62a06e055ad026acd9ad55dd3e40cf94e017b659e7a6a` | P2 trained/white-box boundary comparator; `BOUNDARY_COMPARATOR`, nonblocking. PDF p5 specifies supervised fine-tuning and p6 reports 750 fine-tuning steps. | Retain in the trained-comparator and H5 modality-specificity strata; do not enter it into a training-free direct-method denominator. | Comparative effectiveness and any transferable technical choice are post-mapping questions. |

The byte identities and storage locations are canonical in
`wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl`; bibliographic identity and routing are canonical in
`data/official-metadata-receipts-v1.jsonl` and `data/reviewer-known-items-v3.json`. This note explains
those records and is not a second numeric or identity canon.

## Gate consequence

The reviewer-known omission is repaired without adding duplicate seeds: each arXiv identity resolves
to one existing-corpus work node. Omni-Decision and AOP-Agent are now direct opening references;
Light-Omni and LatentOmni are explicit trained boundary comparators. Nothing in this routing closes
H5, authorizes Stage-1B, or pre-commits a Stage-2 method.
