# Home · Knowledge Base

The shared knowledge base & "memory" for **exploring-l4-intelligence**. Humans and their AI
assistants get one consistent understanding here. The source lives in the repo's `wiki/` folder and
is synced to this Wiki via `scripts/wiki-sync.sh`.

> The canonical entry point is the repo **root README**; this Wiki is its extended knowledge base.
> The project's north star is [[Project-Thesis]] — training-free RL to activate pretrained knowledge.

## Pages

- [[Project-Thesis]] — the research thesis / north star (**read first**)
- [[Research-Objective]] — current stage, blockers, next action (**read second**)
- [[Architecture]] — repo model & shared library
- [[Environment-and-Setup]] — WSL2 / CUDA / py3.12 venv / verl
- [[Inference-Engine-Choice]] — local 30B on 24 GB: llama.cpp (proven) vs vLLM (deferred to W2), measured evidence
- [[Working-Mode]] — cross-repo conventions
- [[Per-Work-Status]] — per-work status (changes most often)
- [[Data-and-Assets]] — models & datasets
- [[AI-Collaboration]] — how AIs use the Wiki as shared memory
- [[Onboarding]] — zero-to-first-run
- [[Decision-Log]] — decisions & learnings (append-only memory)

## How to use this Wiki

Before starting, read this page and [[Per-Work-Status]]; record notable decisions/learnings to
[[Decision-Log]]; publish from the repo with `bash scripts/wiki-sync.sh`.

---

## 中文

**exploring-l4-intelligence** 的团队共享知识库与"记忆"。人和各自的 AI 协作者都从这里取得对项目的一致
理解。源文件在仓库的 `wiki/` 目录，用 `scripts/wiki-sync.sh` 同步到本 Wiki。

> 仓库的**权威入口是根目录 README**；本 Wiki 是它的延伸知识库。

**页面**：[[Project-Thesis]] 研究主旨/北极星（**先读**）· [[Research-Objective]] 当前阶段与下一步
（**次读**）·
[[Architecture]] 架构与共享库 · [[Environment-and-Setup]] 环境搭建 · [[Inference-Engine-Choice]]
本地 30B 推理引擎取舍（llama.cpp 已验证 / vLLM 留待 W2）· [[Working-Mode]]
协作约定 · [[Per-Work-Status]] 各工作进度（最常更新）· [[Data-and-Assets]] 模型与数据 ·
[[AI-Collaboration]] AI 如何把 Wiki 当共享记忆 · [[Onboarding]] 从零跑通 · [[Decision-Log]]
决策与经验（追加式记忆）。

**怎么用**：开工前先读本页和 [[Per-Work-Status]]；有重要决策/经验写回 [[Decision-Log]]；改完在仓库里
运行 `bash scripts/wiki-sync.sh` 发布。
