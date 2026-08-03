# W1–W4 work-repository retirement tombstone (2026-08-03)

Owner ruling 2026-08-03: the four historical work repositories under `projects/` are historical
residue; delete local and remote. This record preserves final identities and the two uncommitted
diffs destroyed with the checkouts. Rescued adoption candidates live in the admitted study repo at
`reference/w1-snapshot/` (ten files, SHA-256 manifest, source commit `7ed41f62`).

## Final repository states

| Work | Repository | Final HEAD (master) | Local deletion | Remote deletion |
|---|---|---|---|---|
| W1 | `https://github.com/chaosxingxc-orion/speech-mllm-training-free-rl.git` | `7ed41f62e3f33f9f16d0fbbe2d13725ace62502f` | 2026-08-03 | pending `delete_repo` token grant |
| W2 | `https://github.com/chaosxingxc-orion/speech-mllm-efficient-rl-alignment.git` | `766bbc92e2d1152b341a2bcceca043a1d764126e` | 2026-08-03 | pending `delete_repo` token grant |
| W3 | `https://github.com/chaosxingxc-orion/speech-mllm-multitask-rl.git` | `931806c82bba12157a499bc6cbdab5af9077a858` | 2026-08-03 | pending `delete_repo` token grant |
| W4 | `https://github.com/chaosxingxc-orion/speech-mllm-omni-embedding-rl.git` | `0f587c6e915f567c1d09ecec6f109ae9c5795bf4` | 2026-08-03 | pending `delete_repo` token grant |

All four repositories had zero unpushed commits at deletion time; every committed byte remains on
the remote until the pending remote deletion executes.

## Uncommitted changes destroyed with the checkouts

W2 and W3 each carried the same two-hunk `configs/config.yaml` working-tree edit (never committed):
the three path defaults `data_dir`/`ckpt_dir`/`mlflow_dir` changed their fallback from
`~/speechrl-data/...` to `${oc.env:HOME}/speechrl-data/...`. W1 and W4 working trees were clean.

## Surviving evidence

- Stage‑1B v5 `38fb9435d0c35e226ad62b16015a6dbee054e6c2` and its 320-work union (wiki survey layer).
- Legacy experiment-attempt inventory `docs/integrity/experiment_attempt_registry.jsonl` (574 rows,
  historical bytes preserved; worktree/history resolution now reports them unresolved by design).
- The ten rescued W1 candidate files in the study repo's `reference/w1-snapshot/`.
- The umbrella-side probe/eval evidence in `wiki/` audit and archive layers.
