---
title: "Experiment index: speech-aware evidence acquisition"
study_slug: "speech-aware-evidence-acquisition"
study_repo: "https://github.com/chaosxingxc-orion/speech-aware-evidence-acquisition.git"
local_checkout: "studies/speech-aware-evidence-acquisition"
decision_record: "wiki/experiments/speech-aware-evidence-acquisition/2026-08-04-owner-consolidated-execution-contract.md"
experiment_id_namespace: "SAEA-E-<nnn>"
source_candidate_provenance: "R2 (system-first-stage1c-v2; provenance only)"
domain: "speech-only; general/environmental audio excluded"
---

# Experiment index: speech-aware evidence acquisition

本页是该 study 的实验生命周期控制面。有效研究对象是冻结 speech-capable omni 核上的
**speech-aware evidence acquisition**；音频文件只是 speech signal 的载体，FSD50K、AudioSet、
ESC-50 等 general-audio 数据不得进入本台账的实验。

## 当前权威路由

- **当前唯一自包含有效合同**（registry pin 指向本件）：
  [2026-08-04-owner-consolidated-execution-contract.md](2026-08-04-owner-consolidated-execution-contract.md)
- Study 仓边界采用（execution-scope guard + 指南路由，续92）：study commit
  `6c4b37e9ff90becde3df934fa2b87e136f1354eb`
- 历史来源记录（事实继承、不回写；blob 见合并合同 §9）：
  [2026-08-04-owner-stage3-boundary-and-paper-gate-contract.md](2026-08-04-owner-stage3-boundary-and-paper-gate-contract.md)、
  [2026-08-04-owner-speech-domain-scope-and-identity-contract.md](2026-08-04-owner-speech-domain-scope-and-identity-contract.md)、
  [2026-08-03-owner-go-and-execution-contract.md](2026-08-03-owner-go-and-execution-contract.md)
- Stage-2A 入场序列：
  `docs/superpowers/specs/2026-08-02-speech-aware-evidence-acquisition-stage2a-entry.md`
- 数据范围、实验角色与保留政策：
  [2026-08-04-speech-domain-dataset-scope-and-retention-plan.md](2026-08-04-speech-domain-dataset-scope-and-retention-plan.md)
- 数据身份/下载状态唯一事实源：`docs/datasets.lock.json`
- D0 获取收据：`docs/checks/speech-aware-evidence-acquisition/2026-08-02-acquisition/`
- 模型/工具 exposure：study 仓 `docs/exposure-ledger.md`
- Stage-1C 历史证据：`wiki/archive/working/stage1c-portfolio/2026-08-03-archive-digest.md`

## 登记要求

每条正式实验必须解析到：`experiment_id`、study commit、shared-code revision、config hash、
protocol hash、model revision、dataset revision、**split role（discovery|confirmatory|dev）、
split identity hash、consumed 标记**、MLflow run、artifact location、artifact hashes、
result summary、deviations 与 decision。大字节位于 `SPEECHRL_DATA_DIR` 或 MLflow；Wiki 只登记 URI、
版本和 hash。confirmatory 样本一经读取即在本台账落 `consumed=yes`（2026-08-03 程序可见性纪律；
consolidated contract §7）；exposure 事件同步记入 study 仓 `docs/exposure-ledger.md`，继承
exposure 单调不减。

每条记录还必须声明：

- speech task 和 carrier；
- `OBS / ORG / SUPPLY / USE` 中本次实际改变的轴；
- runtime 可见字段与禁止字段检查；
- effectiveness、reasonableness 与 efficiency 三类结果；
- general-audio 数据未被加载的确认。

## Ledger

| experiment_id | date | speech task/carrier | changed axes | study commit | shared code revision | config hash | protocol hash | model rev | dataset rev | split role | split identity hash | consumed | MLflow run | artifact location | artifact hashes | effectiveness | reasonableness | efficiency | deviations | decision |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

尚无正式实验。首条记录前必须关闭 E0 D1–D4，并落 llama.cpp build 与 GGUF hash 的 runtime receipt。
