---
title: "Precheck Provenance 更正（append-only）— evidence/artifact snapshot 拆分 + canonical hash"
date: 2026-07-13
corrects: "wiki/2026-07-13-reviewer-precheck-survey-design-and-record-closure.md（原文不改动）"
mandated_by: "预检博导审查 W1-ASEL precheck doctoral review §7 / P0-REC-1（snapshot 回归）"
author: "协调者本人"
---

# Precheck Provenance 更正

## 缺陷（reviewer 坐实，我复核属实）

被审 precheck 文件 frontmatter 仅用单一 `snapshot:` 字段写
`umbrella HEAD 0afad68 / W1 a532da0`，把**证据快照**（文件描述的仓库状态）与**工件快照**
（文件自身的提交）混在一起——正是团队此前已修过、本轮又复现的同类歧义（R6-M2 类）。
说明 closure checker 尚未覆盖这条不变量。

## 正确的三元组（canonical hash = git blob 字节）

```yaml
provenance:
  evidence_snapshot:            # precheck 正文所描述的仓库状态（full 40-char SHA，canonical）
    umbrella_commit: 0afad686a7274643fb127ed8a07a99a132ffd3e1
    w1_commit: a532da06296681b3bbb30446a6fa285ca5bed508
  artifact_snapshot:            # precheck 文件自身
    path: wiki/2026-07-13-reviewer-precheck-survey-design-and-record-closure.md
    umbrella_commit: aad1f6d4feb6d762402aa8cbfb314c81397e352d
    sha256_git_blob: 8a1ec913517d60fa5e3d738b4473eb6c8e26c4f36275f52a5e809e33e0f3fa40
```

（工件 blob 哈希独立复核命令：`git show aad1f6d:wiki/2026-07-13-reviewer-precheck-survey-design-and-record-closure.md | sha256sum` = `8a1ec913…` — 与 reviewer 记录一致。）

## checker 不变量补登（防复发）

发布任何"呈 reviewer / 呈 owner"的记录类文件时，frontmatter 必须**分列** `evidence_snapshot`
与 `artifact_snapshot`，且工件快照带 canonical git-blob 哈希——单一 `snapshot` 字段自此禁止用于
双重语义。此约定登记入哈希正典条目谱系（CLAUDE.md/AGENTS.md 术语表）。
