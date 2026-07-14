# 2026-07-09 · 三锚点增量再定级（对 2026-07-08 审计的 delta，Opus 复核台账齐备）

> **性质**：Stage-1 append-only 再定级文档。Owner 2026-07-09 复提三锚点并追问"是否夯实、
> 是否还有'自以为满足信息约束实则未达成'"——本文是对 `2026-07-08-three-anchors-critical-audit.md`
> 的**增量复审**，不重做、不改写。
> **方法**：三路代码/文档盘点（勘误：误用 Sonnet 执行，owner 当日纠正分工——技术验证归 Opus；
> 盘点结论全部再经复核）→ **20 项承重判定 × 6 个 Opus 对抗验证束逐条复核：16 CONFIRMED /
> 3 PARTIAL / 1 REFUTED**（台账见 §2，PARTIAL/REFUTED 修正已内联）→ E 盘机器盘存（39 数据集/
> 18 模型）→ Fable 综合。
> **Owner 本日两项裁定**：① **A2 接受再定级**（07-08 提案生效）；② 追加三条方法论要求
> （理论⟷数据 loop / survey+Lean+假设提取 / 数据全覆盖）→ 落为
> `2026-07-09-stage1-dual-track-campaign.md`。

## 1. 07-08 记分卡逐项状态

### A1（speech-key/异构-value 组织形式）——五洞

| # | 07-08 判定 | 本日状态 |
|---|---|---|
| 1 | 唯一端到端验证是 logmel 恒等往返，零语义证据 | **OPEN**（数据轨检索质量测评 = 唯一出路；嵌入器候选池 18 模型已全部在盘） |
| 2 | omni-embed loader 未接通 | **OPEN**（官方非对称 API 已确诊，修复排入战役 P3；NC license 已降对照） |
| 3 | CLAP 与内容任务错配存疑 | **CLOSED（问题已定死）**：F1 硬确证 R@1 0.1% vs GLAP 93.8/98.5 → CLAP 降为声音事件域 + 负对照 |
| 4 | value 只覆盖 knowledge 粒度 | **OPEN → 方案已立**（Q2 备忘录三粒度方案 + schema 演进需求，P3 工程票） |
| 5 | kb_audit latent bug + KB 工件不入库 | **半 CLOSED**（bug 修复 a517bdd 复核确认）；KB 工件版本化仍 OPEN |

### A2（"理论已证外接优于 rollout"）

**CLOSED（表述层）**：owner 2026-07-09 裁定接受再定级——A2 的诚实表述 =
**已证 rollout read-out 上界（机器检查）+ Stage-2 定理目标（τ*>0 邻域收敛 + N* 预算）+
方向性经验证据（交付形式 > 注入内容）。不是已证结果。**
定理层 **OPEN**：τ*>0 门控注入定理、N* 落地 best-of-N 算子、Beirami sorry 清欠——进战役 P4
理论轨工作单。

### A3（数据+脚本底座）——五刺

| # | 07-08 判定 | 本日状态 |
|---|---|---|
| 1 | T7 boundary 标签误导 | **CLOSED**（errata 落库 a517bdd，复核确认） |
| 2 | 泄露审计 verbatim-only（残留 1.7%） | **OPEN**（复核确认 `t8_clean_rag_rerun.json:8` post_scrub=0.017） |
| 3 | item-id 冻结未接入 T 跑 | **OPEN**（战役 P3 **P0 优先级**：kb_snapshot 强制接入一切新跑） |
| 4 | "同基座"声称与仓库脱节 | **OPEN 但判定软化**（见 N5——复核驳倒了"唯一 importer"，同基座是"部分成立"） |
| 5 | 目标 regime 无外部 baseline | **OPEN**（Stage-2 前置；文献对照 BR-ASR/kNN-Whisper 系仅作协议参照） |

## 2. 本轮新增发现（20 项 Opus 复核台账）

### A1 侧新增（复核束 V1，全 CONFIRMED）

- **N1 泄露"门"只写不查**：`kb_build.py:84,89-107,124` 无论 audit verdict 一律持久化（verdict
  仅进 provenance `:104`）；`kb_retrieve.py:51-74` 零 verdict 读取；**kb_poc.py:54-58 实际构建过
  scrub=False 的 LEAKAGE 源并在 :70-71 加载检索**。README `:62-65` "automatic gate, not human
  discipline" 作为代码声称为假。
- **N2 持久 KB 从未被真实实验使用**：kb_* import 全部限于 scripts/knowledge/ 内；`build_source`
  仅 kb_poc 两处调用；T0/T7–T10 用脚本内 MiniLM+TF-IDF 检索器（`t7_rag_gate_probe.py:79-92`）。
- **N3 registry "built" 虚标**：`kb_registry.py:48-53` 四个数据集标 built（定义 `:11`"至少建过
  一次"），E 盘持久库实际只有 heysquad_poc/_clean 两个 PoC 源。
- **N4 schema 无 span**：`kb_schema.py:36-54` 无 span/offset/segment 字段；key_audio_ref 整文件路径。

### 实验纪律侧新增（复核束 V2，全 CONFIRMED）

- **N6 T8 结构泄露模式仍在**：`t8_clean_rag_rerun.py:48-54` KB 池与评测项同池、无 item-id 排除；
  唯一缓解是 gold 字符串 scrub `:37-43`；且 `:70` 的 asr_hit 把自身 ctx 计入 topk 命中、`:69,76`
  oracle_scrub 注入自身（已擦除）段落。"清白"清的是字符串不是结构。
- **N7 T9/T10 无 CI**：两脚本零 bootstrap（对照：t7/t8/p6 都有）；headline 数字 0.237 与
  0.175→0.35 无区间。复测时必须补。
- **N8 T0 gold 注入 = 合规披露的 ceiling probe**（`t0_consumption_probe.py:11,19-21`）——非隐藏
  泄露，但引用其数字必须带 ceiling 标签。

### A3 侧新增（复核束 V4/V5）

- **N9 zh-ASR/SID/zh-SER 全部不在 lock**（V4 4.1 ✅）：aishell-1/thchs-30/cn-celeb1/cn-celeb2/
  voxceleb1-test/esd/csemotions/m3ed 均仅在 gap-candidates.json。
- **N10 lock 元数据 bug**（4.2 ✅）：aime24/25/26 与 seed-tts-eval 误标 `task:"asr"`
  （`datasets.lock.json:490,507,524,541`）。
- **N11 unpinned revision = 10/28**（4.3 PARTIAL 修正口径，原报 ~6）：librispeech/covost2/minds14/
  air-bench/voicebench/tau2-bench/seed-tts-eval/aime×3 + GGUF 模型条目 `:572`。
- **N12 SID 仅 crema-d 91 人代用**（4.4 ✅）：VoxCeleb 已删（`data.md:93-94`）。
- **N13 llama.cpp 无 SHA 钉扎**（5.1 ✅）：`env-setup.sh:54` shallow clone 无 commit/tag。
- **N14 无 Python 依赖 lockfile**（5.2 ✅）：无 uv.lock/requirements；pyproject 主要依赖无版本约束。
- **N15 采样参数缺口（5.3 PARTIAL——原判定部分被驳）**：修正后的事实是——server launch flags
  **已**共提交（`repro_asr_best_of_n_llamacpp.py:20` 完整命令；`-ngl 28`/port 记录在 _repro JSON
  model 字段），非 T 系脚本也设过 top_p；**真实残留缺口** = `-c 8192`、top_k、repeat_penalty
  不逐结果机器记录，T/p 族脚本只显式 seed+temperature+max_tokens。
- **N16 reproduce 字段过期 23/25**（5.4 ✅）：D→E 迁移 commit dcb97f0 只改 umbrella，W1 的
  `SPEECHRL_DATA_DIR=<repo>/speechrl-data` 字符串未更新，按字面执行解析不到数据。
- **N17 GGUF 仅文件名钉扎**（5.5 ✅）。

### "同基座"判定修正（复核束 V3——**含 1 项 REFUTED**）

- **N5**：原判定"main.py 是 speechrl_common 唯一 importer" **REFUTED**——`repro_asr_best_of_n
  [_llamacpp].py`、`m3_phase0_zero_support.py`、`m5_memo_censuses.py`、`m5_selector_confirmatory.py`、
  `m5_selector_rescore_dev.py`、`probe_hprompt_vs_hfix.py` 共 7 个脚本真实使用共享库的
  reward/decode。3.2 PARTIAL：具名 model 字段的 14 个 JSON 全部指向 qwen3-omni GGUF（无一
  Qwen2-Audio），但 14/28 无 model 字段、字符串不统一。3.3 ✅：T/p 族的真实共享底座是 p2_baselines。
  **修正后判定**："同基座"= **部分成立**——W1 best-of-N/选择器线与共享库真实同基座；知识轨
  T/p 族走独立 p2 harness；Hydra+Qwen2-Audio 名义 scale-up 路径仍是无映射 stub。消解方向见
  Q1/Q2 备忘录裁决位 +10。

### 理论侧（复核束 V6，6.1–6.7 全 CONFIRMED）

唯一实质 sorry `BestOfN.lean:90`；`kl_best_of_n_le`/`regret_O_sqrt_log`/`gain_le_of_hoeffding`
三定理把硬内容作前件假设（`:= hBeirami` 式）；三个收敛定理全部 squeeze_zero 套外部假设的
τ→0/frac→0；"外接跨界"两定理为自标 FRAMING-ONLY 的平凡见证；over-confidence 仅 docstring；
Iterate.lean 已入库入 import（d79b387，此前"未提交却称 green"史实成立）；
**`too_improbable_unreachable` 方向是给 few-shot 重加权设上限**——设计含义见 Q1/Q2 备忘录 §3。

## 3. "自以为满足信息约束/工程声称但实际未达成"清单（6 → 9）

| # | 情形 | 位置 | 状态 |
|---|---|---|---|
| 1–6 | （07-08 原六条） | 见 `2026-07-08-three-anchors-critical-audit.md` §4 | 1 号已 errata；3 号进 P3 P0 |
| 7 | README "automatic gate" 声称 vs verdict 只写不查、泄露源可建可查 | `scripts/knowledge/README.md:62-65` vs `kb_build.py:104`/`kb_retrieve.py` | **P3 P0 修复项** |
| 8 | registry "built" 声称 vs 持久库仅两个 PoC 源 | `kb_registry.py:48-53` | P3 修正 |
| 9 | T8 "boundary-clean" 声称 vs 结构性同池复用 + 字符串级审计（残留 1.7%） | `t8_clean_rag_rerun.py:48-54` | 判读维持 null 结论有效（泄露只会虚增增益，null 更稳），但"clean"标签今后须写"string-scrubbed, structure-shared" |

## 4. 三锚点一句话判定（更新版）

- **A1**：设计成立、工程底座真实**但从未被证据使用过**、语义有效性零证据——嵌入器候选池已全部
  在盘，数据轨检索质量测评是唯一能把 A1 从"设计"变"结果"的动作。
- **A2**：表述已按 owner 裁定再定级；理论实体 = 1 个已证上界族 + 3 个条件性收敛 + 2 个 FRAMING
  见证 + 1 个反方向上限定理——**τ*>0 门控定理是把"外接"从主张变定理的正道**（战役 P4）。
- **A3**：底座诚实纪律好于典型研究代码（append-only errata、结果随脚本入库、directional 标签），
  但四个词各需降格——"锁定"（39 盘存中 11 个候选未入 lock）、"无泄露"（两起史实 + 结构复用仍在）、
  "同基座"（部分成立）、"可复现"（方向性近似，非 bit 级）。修复全部排入战役 P3，带优先级。

## 5. 底数核定（E 盘机器盘存，2026-07-09）

39 数据集在盘（lock 28 全 COMPLETE + gap 7 + WS-D 4；m3ed/slue-sqa-5/esc-50/fsd50k/mlc-slm/
full-duplex-v3 不在盘各有由）；18 模型在盘（lock 6 + 候选 12 全齐）；零无主目录。
**覆盖矩阵以 39 为底数**（owner 纠正："17"只是 07-08 对 lock 28 的建议纳入子集）——
见 `2026-07-09-stage1-dual-track-campaign.md` §2。
