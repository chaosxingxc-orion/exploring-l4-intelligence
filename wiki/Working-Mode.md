# Working Mode

This is a multi-repository workspace. Commit every change to the repository that owns it.

## Ownership

- Umbrella governance, Wiki, `common/`, `docs/`, `scripts/`, `studies/README.md` and
  `studies/registry.json` → umbrella repo.
- W1–W4 code/config/README → the corresponding independent repo under `projects/<work>/`.
- Admitted study code/config/README → its independent semantically named repo under
  `studies/<semantic-study>/`.
- Models, datasets and large/raw outputs → `SPEECHRL_DATA_DIR`, never Git.
- Run tracking → local MLflow; the Wiki pins run IDs and asset hashes.

Do not create an engineering repo from a conditional candidate. Repository creation requires a semantic
identity, owner GO and an execution contract. Candidate IDs remain survey/audit provenance.

## Git and checks

Existing umbrella and W1–W4 repos use `master`; each admitted study records its own branch policy.
Branch non-trivial changes and keep a commit/PR within one repository. Preserve LF normalization and the
lazy-import boundary in `common/`. Run `pytest common/tests`, the owning repository's tests, and the
relevant umbrella gate.

Never create remotes, push, or publish the Wiki without explicit authorization. The repository Wiki
source is authoritative; the web Wiki is a mirror.

## Research flow

Each study advances independently from survey through validation. Once one study enters engineering,
survey of the next candidate may proceed in parallel. Record durable state in [[Research-Objective]],
experiment assets in [[Experiment-Assets]], and detailed placement/lifecycle rules in
[[AI-Collaboration]].

---

## 中文

这是多仓工作区，改动必须提交到拥有它的仓：治理、Wiki、共享设施和 study 登记表属于伞仓；W1–W4
代码属于各自 `projects/` 仓；正式研究代码属于各自 `studies/` 独立仓；大型数据、权重和原始输出只放
`SPEECHRL_DATA_DIR`，运行由 MLflow 跟踪并从 Wiki 绑定 ID/hash。

条件候选不得提前建工程仓。只有具体语义名称、owner GO 和执行合同都冻结后才能建仓。每个 study 独立
推进；一个进入工程后，可以并行调研下一个候选。未经明确授权不得创建远程仓、push 或发布 Wiki。
