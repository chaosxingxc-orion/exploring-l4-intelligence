# Discrepancy register

Seeded 2026-07-13 (ticket #38 item 4, v4.2 doctoral review §6 P0_INTEGRITY_FREEZE `required_artifacts`) by `scripts/checks/build_registers.py`. Append-only in spirit: add a new dated entry to re-adjudicate, never silently delete a prior one.

## Known record-inconsistencies (from the 2026-07-13 v4.2 doctoral review)

Source: `wiki/2026-07-13-v42-doctoral-adversarial-integrity-review.md` §1 (可复核事实) and §4 M-8.

1. **Stale "4 errors" text** — v4.2 §13.4 stated the standard entry had "现有 4 errors" as of that snapshot; the review's own real run reported `PYTHONPATH=src pytest -q` → **143 passed, 3 warnings, 167.10s, 0 errors** at commit `159b525`. The "4 errors" text was stale/outdated at publish time.
2. **"Converged (2 rounds, 0 residual)" wording scope** — commit `159b5258`'s subject line uses "converged"/"0 residual" language while the SAME proposal snapshot lists undelivered items (K-trajectory harness, live cross-modal smoke, corpus lock, REPRODUCE.md, full SAP numbers, operator-linked theory) — the review judges this "更像发布快照协调失败，而不是有利方向的数据造假" (a release-snapshot coordination failure, not favorable-direction fabrication) but it still means "converged"/"locked" must not be read as an M1-closure claim.
3. **Chronology: date-vs-commit** — the root proposal's frontmatter date is 2026-07-12, but its FIRST git commit timestamp is 2026-07-13 01:42:28 +08:00 — insufficient alone to prove backdating, but an unexplained release-record vs. file-date mismatch the review flags as needing a `created_at`/`released_at` dual-timestamp fix going forward.

## This run's live-checked facts (never assumed stale)

- **generated_at (UTC)**: 2026-07-13T03:25:43Z
- **umbrella git SHA**: `aaff7d519cb5f48629044681d17974a70387997b` (dirty=True)
- **W1 git SHA**: `159b5258f2d1d0cb2fec1b0e81dbb5876148e350` (dirty=True)
- **W1 standard entry**: NOT re-run by this script this time (skipped (--no-live-pytest)) — see `docs/integrity/release_manifest.json` (built separately by `scripts/checks/build_release_manifest.py`) for the authoritative, dedicated standard-entry result.

## Open items (not yet adjudicated)

- **P0_INTEGRITY_FREEZE is NOT yet PASS (honest-audit, Decision-Log 续28).** Two of the four required registers are partial: `prior_exposure_registry.json` still lists prompt-template and metric-family enumeration as OUTSTANDING (`manual_completion_todo[0]/[1]`), and `experiment_attempt_registry.jsonl` is a shallow filename+mtime scan that does NOT capture the config-selection trajectory (every tried prompt/weight/threshold/K/embedder + abandonment reason) that P0/M-6 require. The required `append_only_erratum_for_v42.md` is not yet on disk. Any remediation report MUST present P0 as INCOMPLETE, not PASS, until these are enumerated. Authoritative machine-readable status: `prior_exposure_registry.json` -> `p0_gate_status`.
- Whether the root-repo first-commit-timestamp-vs-frontmatter-date gap (item 3 above) recurs in any LATER release snapshot — needs a `created_at`/`released_at` field added to future proposal frontmatter and checked mechanically, not just narrated here once.
- Any NEW discrepancy this script's future re-runs surface between this file's last-recorded facts and the live-checked facts at that later run — append, do not overwrite, the "This run's live-checked facts" section above.


## 2026-07-13 追加（#39 收尾，协调者）

- **docs/checks/v42-conformance-report.md（人读叙事版）已陈旧**：正文仍记 "12/12 PASS / rules-2026-07-12"，而活体机读输出（`v42-conformance-output.json`）已是 **22/22 PASS / rules v42-remediation/rules-2026-07-13**。处置：本文件为准绳时以机读 JSON 为权威；叙事版顶部已加更新注记（见该文件），完整重写排入下一次发布周期。
- **#39 敌意环第 3 轮"kb_embed.py/build_full_corpus.py 违规编辑"判定为误报**：该两文件的未提交改动是提速修复代理（模型缓存 + device 旗标 + 子批量，协调者已独立验证：断点余弦 1.0、测试绿）的合法成果，与 #39 工作流无关；按序提交中。
