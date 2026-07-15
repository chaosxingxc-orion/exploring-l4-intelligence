---
title: "过夜整改报告：全实验清白重做 + RI 机器化 + 工程/统计地基（owner 晨会材料）"
date: 2026-07-11
stage: 1-problem-definition / remediation
status: "写至 ASR v2 出数前；ASR 结果落地后补最终节。状态词受六级制约束。"
---

# 2026-07-11 · 过夜整改报告（晨会材料）

> Owner 睡前指令："把所有的实验都完整的修一遍，解决不了的问题先记录下来。"
> 本报告按六级状态制（ACKNOWLEDGED→DECIDED→TICKETED→IMPLEMENTED→VERIFIED→PUBLISHED）陈述。
> **每一项 VERIFIED 都有独立 Opus 复核记录**；未验的一律不写成完成。

## 1. 实验清白重做（G5 三件套 + 工程/统计地基）

### #33 MInDS 清白重做 — VERIFIED，已入库（W4 `9ead4d4`）

**科学结论改写**：清白因子分解（card 池 126 / eval 437 不相交、3 独立 support draw、2×2 因子）：
naive 0.712；**instruction-only（真 zero-shot）0.467 = 显著回归 −0.245 [−0.286, −0.201]**；
cards-only 0.958（+0.246）；instruction+cards 0.973（+0.262）。**旧 "+0.126 policy 增益"完全由
card 因子驱动且是 transductive 的**；纯指令叠加效应仅 +0.015。Opus 复核：切分逐字节独立重建、
全部数字 1e-9 复算、provenance hash 对真。caveat：脚本化语料表面重叠贡献 card 优势的 ~3%（已
记录）；7 个 delta 未做多重比较校正（morning item）。Ledger：C-MINDS-V2（supersedes C-MINDS-POLICY）。

### #34 CREMA-D 清白重做 — VERIFIED，已入库（W4 `d04bb89`）

**情感故事第三次修订（这次是干净版）**：speaker-grouped GroupKFold(5)、全语料 7442 clips /
91 speakers、内层分组选层（零泄漏，Opus 验证）、cluster(=speaker) bootstrap：**attentive-stats
池化增益真实但小——pooled +0.0270 CI [+0.0141, +0.0401]（排除 0），且整体落在预注册 SESOI 0.05
之内（"bounded below SESOI"）**。两个 fold 单独显著。与 v2 NULL 的方向差异经 Opus 对抗检查
= 功效/设计（v2 各 seed 均值 +0.037 本就为正，n=300 切片无功效），非 bug。旧 +0.097 维持
oracle-选层假象定性。**speaker 重述**：冻结工件纯算术重读——2/3 种子 CI 排除 chance（高于），
**"表示无 speaker 信息 / never written / measured-zero readout" 措辞全部废止**（三处 wiki 已挂
更正）。Ledger：C-W4-EMO-GROUPED、C-W4-PARA-RESTATED。

### #32 ASR best-of-N 清白重做 — IMPLEMENTED + 在跑（结果待补）

- v2 脚本（不动冻结 v1）：**seed 四分离**（cohort/noise/greedy/pool）、双口径并报（corpus WER 带
  S/D/I/N 计数 + 明确命名的 macro）、条件族 {clean, snr5}、selector 全家桶（oracle 只作上界 /
  MBR / random / 长度启发式 / logprob 置信——logprobs 实测可用）、层级 bootstrap、脚本原子写 +
  全套 provenance（llama.cpp build 与 /props 实时互证）。
- **实现中抓到 v1 的真 bug**：v1 的 MBR 用非对称 WER 当距离（除以伪参考词数），会被退化短候选
  拉偏——v1 的 MBR null 部分可能是实现偏差；v2 改为方向不变的原始词级编辑距离（合成池验证）。
- **运行事故与修复（记录在案）**：第一次全量在 utterance ~10 处遭 llama-server prompt-cache
  livelock（同一 task 无限重复 "need to evaluate at least 1 token… n_past" 警告；best-of-N 的
  同音频前缀 25×/utt 恰好触发该边界）。修复：per-request 超时 (10,180)s + 单次重试 + utterance
  级断点续跑（.partial.jsonl）+ 两道中止护栏 + **--cache-ram 0**（活体 args 硬校验）重启。
  第二次尝试 18:31Z 起跑，task 推进正常。代价：关缓存后吞吐下降（预期）。
- 结果与 Opus 复核 → 见本报告末节（出数后补）。

### #25 Phase-A 工程必修 — VERIFIED，已入库（W1 `28f0a38`）

7 项 P0 全部真修复（Opus 实跑验证）：`--execute`+驱动器落地；命名 4 字段统一；`qwen3-omni-own`
token 归一；**auto→CLAP 回退击毙**（manifest 记 token、查询强制同 embedder、维度断言、负测试）；
6 个 PLAN-ONLY 臂全部真实现；kb_batch_build 驱动多粒度/H-a/H-b/RAPTOR-lite/audio+text；
eval_manifest ∩=∅ 机器不变量 + own-item 双重排除 + retrieved passages 全记录；泄漏审计加 n-gram
+ 嵌入相似辅助层；**dry-run 35 臂/140 格 = 台账对齐**；fake E2E 35/35 PASS、kb_gate 16/16。
残留（诚实记录）：G2 第 2/3 层未跑（KB 源批量构建、真 embedder live smoke、真 server 契约、
heysquad CLEAN 门）；struct-lite 暂 alias raptor-lite；FIXED_THRESHOLD=0.5 占位待签。

### #26 统计地基 — 设计 VERIFIED-by-review 交付 + 核心机件 IMPLEMENTED（W1 `33ff3c1`）

设计文档（`2026-07-11-group-split-statistics-design.md`）：76 键全分类（G-FIELD/G-ID/G-SOURCE/
G-NONE 逐键引证）；烧毁种子清单 + 新 LOCKED_TEST_SEED 提案 + 访问纪律；**诚实计数**：264 有效格、
重叠键对应 234 格（"65 格"是键/格混淆）。核心机件已实现并测试（34/34）：cluster bootstrap /
Holm / max-T / DerSimonian-Laird（stats.py）、group_key_of（20 数据集）、draw_disjoint_grouped、
per_item 落 group_id。**留给 owner 的 5 个裁决位**：重跑范围、粗粒度 SER 处理、legacy loader
改动、访问控制硬度、种子批准（设计文档 §5）。

## 2. RI 机器化与发布链（第二、三份审稿的核心诉求）

- **RI-G0 证据冻结**：`_repro/evidence_freeze_20260711.json`（16,972 文件 / 6.28 GB 全哈希、0 错）
  + WSL mlruns 补充清单（509 文件）。
- **RI-G1 claim ledger**：`docs/claim_ledger.yaml` 15 条机器可读裁决（M3/T7 默认 INVALID + validity
  侧车 + frontmatter 状态层；MInDS/CREMA 新裁决已录）。
- **K8 原位重评分补救**：60 个 pre-rescore 侧车（自真父提交 `c9ee7d1`——规格里写的 7748515 是错的，
  执行代理双验证后纠正）。
- **重抽验证格的原位覆写已回滚**：disjoint 结果移至新 artifact ID，已提交原件恢复（RI-G0 规则）。
- **发布链**：wiki-sync 改为全树发布（此前只发顶层——归档 51 页会丢、远端 8 旧页会被删）；
  18 处断链归零；论文 main.tex 挂 QUARANTINED DRAFT 横幅（5 处已证错误主张列名，解除=#31）；
  Project-Thesis / Architecture / W4-Feasibility / Per-Work-Status 传播更正注全部落位。
- **答复 v2**（`2026-07-11-response-v2-erratum-and-forensic-reply.md`）：对 v1 自身 7 处错误的勘误
  （含"更 NULL"统计错误、STALE 总括、"已执行"时态）+ 法证审计逐条答复 + 复审 16 条逐条答复 +
  49 行核验 ledger。

## 3. 解决不了/未做完的问题清单（owner 晨会）

1. **ASR v2 结果待落**（在跑；若第二次尝试再卡，livelock 证据已存档，改用 -np 4 -c 16384 配置重试
   是下一个旋钮）。
2. **#26 五个设计裁决位**（上述）——裁决后才能生成新锁定 manifest 并放行 ~234 格重跑（#23）。
3. **MInDS 7 个 delta 的多重比较校正**未做（stats.py 的 Holm/max-T 已备，接线即可）。
4. **噪声嵌套重复**（nested noise replicates）本轮未做——单噪声实现/条件，已在工件 limitations 记录。
5. **MLflow 负时长异常**（run 2c61b2f1，−1486ms）未解释。
6. **struct-lite 臂**暂为 raptor-lite 别名（HippoRAG-lite 未建）；FIXED_THRESHOLD=0.5 待签。
7. **G2 第 2/3 层**（Phase-A 真 runtime 三层绿的后两层）未跑——#24 的开跑前置。
8. **#27 理论重写 / #28 调研 86 条全量核验 / #29 W4 fresh proposal / #31 论文改写**：TICKETED，
   未动工（非实验类，按你晨会排期）。
9. **#33/#34 的 provenance git_dirty=true**：脚本运行时未提交所致；提交后各花 ~5 分钟 GPU 可出
   干净 provenance 版（可选）。
10. **push + wiki-sync**：等 ASR 终格入库后一次性执行（发布链已修好；若晨会前 ASR 未收尾，
    现有 commit 也可先推——待你示下或我按"全部收尾后推"的既定序执行）。

## 4. ASR v2 终格

### snr5 条件 — VERIFIED（Opus ACCEPT-with-notes：42/42 聚合格精确复算、288/288 选择逻辑复现、0 跳过 0 重试）

n=96、pool_seeds [1,2,3]×8、N∈{1,2,4,8}。@N=8（corpus / macro WER；Δ=对 greedy 改善）：

| selector | corpus | macro | corpus Δ 95% CI | 判定 |
|---|---|---|---|---|
| greedy（temp0 基线） | 0.0973 | 0.1113 | — | — |
| oracle@8（上界，不可部署） | 0.0636 | 0.0760 | +0.0336 [0.0235, 0.0453] | SIG |
| **logprob 置信@8（可部署）** | **0.0891** | 0.1049 | **+0.0081 [0.0005, 0.0161]** | **SIG（仅 corpus，边缘）** |
| MBR@8（修复后对称编辑距离） | 0.0924 | 0.1065 | +0.0048 [−0.0023, 0.0121] | ns |
| random@8 | 0.1033 | 0.1205 | −0.0060 [−0.0159, 0.0040] | ns |
| length@8 | 0.1086 | 0.1235 | −0.0116 [−0.0264, 0.0022] | ns |

**读法（严格口径）**：① oracle headroom 复现且更稳（+0.0336）；② **首个过 CI 的 deployable
selector**——logprob@8 实现 ≈24% 的 oracle headroom（ρ≈0.24），但仅 corpus 口径、CI 下界 ~5e-4，
**Stage-1 directional，禁止读作稳健部署增益**（G4 纪律：不以单个边缘 CI 定论；multiplicity
未校正）；③ 修复后的 MBR 转正向但 ns（v1 的 MBR null 部分归因于其非对称距离 bug 的说法不成立
——修好后仍 ns，v1 结论方向侥幸无恙）；④ random/length 为负对照，行为如预期。
多样性：4.58 unique/8、16.3% 全同池（与 v1 同量级——坍塌是采样配置属性，非实现差异）。

### clean 条件 — VERIFIED（Opus ACCEPT：42/42 聚合格精确复算；同 cohort sha 跨条件一致=纯噪声差分设计确认）

@N=8（greedy corpus 0.0579）：

| selector | corpus | corpus Δ 95% CI | macro Δ 95% CI | 判定 |
|---|---|---|---|---|
| oracle@8（上界） | 0.0357 | +0.0223 [0.0136, 0.0316] | +0.0254 [0.0133, 0.0397] | SIG（上界） |
| **logprob 置信@8** | **0.0486** | **+0.0094 [0.0034, 0.0165]** | **+0.0134 [0.0045, 0.0247]** | **SIG（双口径）** |
| MBR@8 | 0.0559 | +0.0021 [−0.0021, 0.0068] | +0.0055 [−0.0012, 0.0144] | ns |
| random@8 | 0.0678 | −0.0098 [−0.0190, −0.0017] | −0.0161 | 显著回归 |
| length@8 | 0.1004 | −0.0426 [−0.0571, −0.0290] | −0.0592 | 严重回归 |

### 终节结论（Stage-1 directional，双条件合读）

1. **oracle headroom 在两条件均复现**（snr5 +0.0336 / clean +0.0223，相对降幅 ~35%/~38%）——
   support 真实，且比 v1 的宏平均口径更稳。
2. **过夜最重要的新信号：logprob 置信是两个条件下唯一 CI 排除 0 的 deployable selector**
   （clean 双口径显著；实现 oracle headroom 的 ~24%/~42%）。项目的诚实 headline 从
   "support exists, realization fails" 更新为 **"support exists; a simple confidence selector
   realizes a small but replicated fraction of it"** —— 仍禁止读作稳健部署增益
   （单模型/单 runtime、multiplicity 未校正、snr5 侧 CI 下界边缘），这恰是 Proposal-S
   （Step-3 primary）powered 验证要回答的问题。
3. MBR（修好非对称 bug 后）两条件均正向但 ns——v1 的 MBR null 结论方向无恙但机理解释需修订；
   random/length 负对照行为正常（length 在 clean 上严重反向）。
4. 运行事故记录：第一次尝试 llama-server prompt-cache livelock（best-of-N 同前缀 25×/utt
   触发 n_past 边界）——超时/断点/护栏/--cache-ram 0 修复后双条件 192/192 utt 零跳过零重试。
   llama.cpp 该边界已入 gotcha 台账（best-of-N 场景暂用 cache-ram 0，吞吐代价 ~45-66s/utt）。

全部 ledger 裁决：C-ASR-V2 / C-MINDS-V2 / C-W4-EMO-GROUPED / C-W4-PARA-RESTATED（docs/claim_ledger.yaml，16 条）。
