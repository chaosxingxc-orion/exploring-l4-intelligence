---
title: 对团队 Stage-1 审计回复的复审：承认成立，但整改闭环不成立
date: 2026-07-11
stage: Stage 1 — response-to-reviewer adjudication
responds_to: 2026-07-11-response-to-reviewer-stage1-audit.md
companion: 2026-07-11-stage1-audit-response-and-rulings.md
reviewed_commit: 641bb655e12ebc47332aa86eb5b9b1dba198fb69
review_mode: read-only, three-lane adversarial verification
verdict: RESPONSE PARTIALLY ACCEPTED; REMEDIATION CLOSURE REJECTED; STOP-THE-LINE REMAINS
publication_readiness: RED
intent_finding: none; no inference of fabrication or deliberate deception
non_actions: no team source/config/result/response file modified; this report only
---

# 对团队 Stage-1 审计回复的复审：承认成立，但整改闭环不成立

> **最终裁决：这是一份质量较高的“承认问题与整改意向书”，但不是一份证据闭环的 response-to-reviewer。**
> 团队确实暂停了新 GPU 运行，准确承认了 Phase-A 不可执行、W4 判据未过、CREMA-D 切分污染、
> Lean 定理与实际 operator 脱节、结果 JSON 缺 provenance 等问题；这些是实质进步。然而，回复把
> `承认/裁定/开票/写横幅/未来门控` 多次写成 `已执行/已完成/已交付`，而现有论文、代码、工件、
> machine-readable validity、Wiki 发布链和独立 held-out 仍没有闭环。更严重的是，回复保留了已经被
> corpus-WER 复算推翻的 ASR 描述，完全漏答 MInDS 的 zero-shot/transductive 问题，并新增了
> “CI 变宽会更 NULL”这一错误统计解释。

因此：**接受治理层面的 acknowledgement；拒绝解除 STOP-THE-LINE；拒绝将 #25–#29 或 G0 claim tree
计作已完成科研整改。**

本文只新增本复审报告，没有修改团队回复、rulings、Decision Log、论文、代码、配置或实验结果。

## 0. 审查快照与时间线说明

审查开始时，团队回复和治理改动仍在工作树中。审查过程中，团队于 2026-07-11 00:29 +08:00 将整批
改动提交为：

```text
641bb655e12ebc47332aa86eb5b9b1dba198fb69
docs(wiki): audit governance — external audit verified (32/34 CONFIRMED),
owner G0 rulings + stop-the-line, reviewer response letter,
51 process docs archived + 8 drift fixes
```

本报告以该 commit 为最新快照，**不再保留“回复尚未提交”这一已经过时的指控**。但截至复审取证时：

- 当前分支仍比 `origin/research/stage1-directional-validation` ahead 1；该 commit 尚未推送。
- `.wiki-tmp` 仍停在 `24ac48e`，2026-07-11 回复尚未同步到共享 GitHub Wiki。
- W1 仍有一个 dirty AISHELL 验证工件；W4 工作树 clean，意味着相关 MInDS/CREMA 修复没有发生。
- 论文 `papers/agent-level-tfrl/main.tex` 未随治理 commit 修改。
- 四个 work repo 没有与 #25–#29 对应的新实现 commit。

所以“本地有 commit”可以解决持久性的一部分，却不能证明远端共享、论文传播、代码实现或实验闭环。

## 1. 复审方法

本次使用三个相互攻击的只读审查通道：

1. **统计与实验设计红队**：复算 ASR corpus-WER/N 曲线，检查 seed、CREMA、MInDS 与 65 个 overlap。
2. **artifact/provenance 红队**：检查 claim→script→raw→summary→paper、Git/MLflow/hash、撤回传播和 Wiki 发布。
3. **敌对元审稿人**：专门寻找偷换问题、把计划写成完成、以 owner/Stage-1/append-only 免责、以及 G0 不可证伪。

主审另外独立检查了最新 commit、各 repo 状态、相关脚本、论文原文、Wiki sync 行为和链接解析。

裁决词含义：

| 裁决 | 含义 |
|---|---|
| `ACCEPT` | 回复陈述与当前证据一致，且该窄项确已实现 |
| `PARTIAL` | 方向/承认正确，但实现、统计或传播未闭环 |
| `REJECT` | 回复陈述被当前文件、复算或状态直接反证 |
| `OPEN` | 是合理 future work，但不得写成已执行 |

## 2. 总体评分表

| 维度 | 裁决 | 说明 |
|---|---|---|
| 面对批评的诚实程度 | `ACCEPT` | 没有否认 Phase-A、W4、理论和 provenance 的核心缺陷 |
| stop-the-line 当前是否生效 | `ACCEPT` | 检查时 GPU/相关进程为空；没有发现 Phase-A/Step-3 新运行 |
| Phase-A 不可执行诊断 | `ACCEPT` | 回复列出的 execute、token、dimension、PLAN ONLY 等缺陷与代码一致 |
| Phase-A 已修复 | `REJECT` | 无对应实现 commit；#25 是计划，不是修复 |
| W4 claim 降级方向 | `PARTIAL` | Per-Work 局部改正，但 Project-Thesis、Architecture、feasibility 文档和 AGENTS/README 仍保留旧叙事 |
| ASR 统计回复 | `REJECT` | 保留错误 headline、错误 seed 解释和错误 all-N MBR 结论 |
| CREMA 统计回复 | `PARTIAL/REJECT` | 污染识别正确；“更宽 CI 更 NULL”错误；代码与工件未改 |
| MInDS 回复 | `REJECT` | zero-shot、transductive、generator mismatch 均未正面回应 |
| artifact provenance | `REJECT` | 只承认缺字段；没有 evidence freeze、hash manifest 或 claim ledger |
| invalid/superseded 治理 | `REJECT` | 人类横幅存在，机器状态仍冲突，原 JSON 仍是肯定式阳性 |
| Wiki 归档方案 | `REJECT` | sync 不发布子目录；已造成 broken links；远端将删除归档页 |
| 理论裁决方向 | `PARTIAL` | 承认 operator-linked=0 正确；现行论文仍把 hard BoN 写成 Gibbs tilt 实现 |
| G0 primary question | `PARTIAL` | 战略聚焦有价值，但仍把五个机制绑成一个问题，ρ 未定义稳健 |
| #25–#29 执行状态 | `OPEN` | 票号只有散文引用，没有仓库可核验 ticket schema/acceptance evidence |
| publication readiness | `RED` | 论文和研究记录不得解除隔离 |

## 3. 团队回复中真正正确、应保留的部分

### 3.1 正确接受 STOP-THE-LINE

团队没有为“先把 GPU 跑起来再修”辩护，而是暂停 Phase-A、Step-3 和 redraw rerun。检查时没有相关
WSL/GPU 进程，W4 也没有新结果 commit。这是当前回复中最可靠的执行事实。

但“当前停跑”不等于已经建立持久门禁。后续必须由可执行 gate 阻止启动，而不是靠回复中的文字承诺。

### 3.2 正确承认 Phase-A 比审计描述更糟

回复没有淡化以下问题：

- 无 `--execute` 路径；
- 6 臂为 PLAN ONLY / `NotImplementedError`；
- runner/builder source schema 不一致；
- registry token 不一致；
- query embedder auto fallback 造成真实 embedding space/dimension 错配；
- 批量 builder 没有驱动声称的多粒度结构。

把原“工程前置已完成”明确记为簿记失实也是必要动作。问题只在于：回复随后又把创建 #25 和声明
“G2 将是硬规则”列进“已完成动作”，重复了相同的完成状态混淆。

### 3.3 正确降级 W4 的科学主张

接受 `diagonal_dominant=False`、matched>mismatched 判据未过，并把当前证据降为 L0/L1，而不是 L2/L3，
是正确的科学裁决。未来采用 speaker-grouped split、真实 transcript/WER、EER/minDCF、不同 backbone，
方向也合理。

但是“裁定废止”与“所有对外文本已废止”不是一回事。后者仍被活跃真源直接反证，见 RR-009。

### 3.4 正确承认理论的条件性

团队明确承认：

- operator-linked theorem 数量为 0；
- monotone/δ/τ/reach 是外部假设；
- Beirami 结果以 named axiom 引入，不是本项目在 Lean 中证明；
- `sorry=0` 不等于系统收敛已经证明。

这是正确的理论卫生。coverage、selector regret、biased-proxy negative、Python/Lean parity 也都是值得做的
proposal。但它们目前仍是 #27 future work。

### 3.5 正确区分战略 pivot 与原计划失效

Owner 有权改变研究方向；选择 W1 machinery 优先、W4 延后，并不天然构成 misconduct。团队也正确承认
旧计划与新计划没有及时对账，造成双重“现行计划”。

需要修正的是措辞：owner 授权能使 pivot 合法，不能使结果已知后的新问题自动变成 pre-specified。
正确标签是 `LEGITIMATE POST-HOC STRATEGIC PIVOT`，而不是继承旧 preregistration 的 confirmatory 身份。

## 4. 根本范围错位：回复没有回应最新研究诚信审查

配套 rulings 的 frontmatter 明确写：

```yaml
responds-to: 2026-07-10-stage1-adversarial-research-audit.md
```

也就是说，这封信主要回应较早的方法学/问题定义审计。与此同时，commit `641bb655` 还纳入了后续的
`2026-07-10-research-integrity-forensic-audit.md`，但回复没有建立对它的逐项映射。

这很可能是并发时间线造成的，而不是故意回避；但在当前 HEAD 中会产生危险假象：一份写着
“32 CONFIRMED / G0 已完成 / 已交付”的回复与一份要求 evidence freeze、claim ledger、MInDS 作废、
ASR corpus 重算的法证报告同时存在，后续 AI 很容易错误推断“后者也已经关闭”。

必须把两组 gate 改名：

- `METHOD-G0`：问题定义与 claim tree；团队目前只部分完成这一项。
- `RI-G0`：研究诚信 evidence freeze；当前未完成。
- `RI-G1`：机器可读 claim/validity ledger；当前未完成。

在没有该命名隔离前，任何“G0 done”都是歧义状态。

## 5. 逐项敌对裁决

### RR-001：`32 CONFIRMED / 1 STALE / 1 PARTIAL` 不可从摘要表重建

**回复主张：** 6 个独立代理核验 34 项，32/1/1/0。

**直接问题：** 配套表显式写出的簇内数量为：

```text
7 + 6 + (6+1) + 8 + 4 + (3+1) = 36
```

这不必然证明 headline 34 是错的，因为簇间可能有重叠；但没有 34-row ledger 时，任何第三方都无法知道
哪些项目重复、哪个是 STALE、哪个是 PARTIAL。`130 次工具调用`也没有命令、输出、hash 或 agent transcript
与 claim ID 的绑定。

此外，“6 个同一项目内 AI 代理”是有价值的内部红队，不等于外部独立复现。ACM 的 Results Reproduced
要求由作者之外的人或团队取得主要结果；内部多代理一致性不能替代这一点。
[ACM Artifact Review and Badging](https://www.acm.org/publications/policies/artifact-review-and-badging-current)

**裁决：** `PARTIAL`。

**整改：** 发布 34-row ledger：`AUDIT_CLAIM_ID / exact source / command / output hash / verdict / reviewer / overlap_group`，
并用脚本自动重算 headline count。

### RR-002：ASR 接受 macro/corpus 区别，却继续把 macro 数值当现行 WER

**回复主张：** oracle `+0.0418`、MBR `+0.0037` 与审计一致；以后 macro 与 corpus 并报。

**复算事实：** 对同一 144 行、2496 reference words：

| 方法 | macro utterance-WER | corpus WER | corpus-WER 对 greedy 改善 |
|---|---:|---:|---:|
| Greedy | 0.11834 | 231/2496 = 0.092548 | — |
| Oracle-8 | 0.07650 | 157/2496 = 0.062901 | +0.029647 |
| MBR-8 | 0.11466 | 234/2496 = 0.093750 | -0.001202 |

所以 oracle 条件性 headroom 仍存在，但 `+0.0418` 不是未加限定的标准 corpus WER 改善；MBR 点估计在
corpus 口径下略差。

当前论文仍多次写：

- `0.118→0.077 / +0.042` 作为 WER；
- “three generation seeds”；
- CI reflects pool-generation variance；
- MBR `+0.004`。

回复中“今后并报”是正确计划，却没有修 artifact generator、paper 或 headline，不能算 closure。

**裁决：** `REJECT current result wording; ACCEPT corrected oracle direction only`。

### RR-003：MBR 并非“每个 N 都不显著”

corpus-WER 下：

- N=1 MBR 改善 `-0.01162`，bootstrap CI 约 `[-0.0219,-0.0019]`，显著变差；
- N=2 MBR 改善 `-0.01002`，CI 约 `[-0.0183,-0.0019]`，显著变差；
- N=4/N=8 才是区间跨 0。

因此回复和现行论文的 “MBR non-significant at every N” 是错误事实。它没有救回 selector；相反，它让
“低 N 下 deployable selector 可能有害”成为必须报告的结果。

**裁决：** `REJECT`。

### RR-004：seed 修复方案仍漏掉 noise 与 greedy 两层

回复正确承认当前 seed 同时驱动 utterance 与 generation，并提出 fixed utterance × repeated pool seed。
但实际代码中的同一个 `s` 同时决定：

1. utterance permutation/cohort；
2. additive-noise realization；
3. greedy seed；
4. pool seeds。

只拆 item×pool 仍不能识别 generation variance。

**裁决：** `PARTIAL`。

**最低协议：** 显式冻结 `cohort_seed / noise_seed / greedy_seed / pool_seed`；在同一 cohort、同一 noise
realization 上 crossed ≥5 pool seeds，另设 nested noise replicates；speaker/chapter 层级重采样。

### RR-005：CREMA 污染识别正确，但“修正只会更 NULL”是新错误

回复正确复算了 speaker/sentence 全跨和 16.0%–21.3% test overlap。但以下句子错误：

> 种子切片正相关使 t-CI 反保守偏窄；修正依赖只会更 NULL。

问题有三层：

1. 只有 overlap 不能证明五个 delta 的实际协方差为正；缺 row predictions 时无法估计。
2. 即使有效样本数下降导致 CI 变宽，结论也是“不确定性更大”，不是“更接近零”。
3. 未拒绝零效应不等于证明等价或无效；要支持“实质无效”，必须预注册 SESOI 并做 equivalence test。

等价检验正是为了给“没有有意义效应”提供正面证据，而不是把普通 p>0.05 当作 null 证明。
[Lakens, Equivalence Tests: A Practical Primer](https://pmc.ncbi.nlm.nih.gov/articles/PMC5502906/)

当前唯一合法句子是：

> 在五次相互依赖的现有运行上，没有得到可靠正增益证据；现有跨 seed t-CI 不具独立重复含义。

**裁决：** 污染诊断 `ACCEPT`；统计解释 `REJECT`；修复状态 `OPEN`。

### RR-006：MInDS 完全漏答，0.984 不能叫 zero-shot

回复与配套 rulings 没有正面裁定 MInDS 的最新问题。当前代码仍然：

- 默认每类 3 个 examples；
- 从待评估的同一 rows 构建 candidate cards；
- 再在这些 rows 上评估；
- 42/182 条是直接 support，另有一条 query 与 support 文本重复。

排除 42 个直接 support 后，policy 与 raw-schema 的差仍存在，因此这不是“假数”；但它只能描述为：

> 固定、由评估集构建的 3-shot/class transductive support-card 条件下的分类差异。

它不能叫 zero-shot、held-out generalization、reward-guided RL，也不能把 +0.126 归因于 card 单一因素。
现行论文仍多次称其 zero-shot，回复没有纠正。

**裁决：** `REJECT`。

### RR-007：用 emotion 的 `cdbf1d2` 判定 W4 provenance “STALE”是对象错配

较早审计明确写的是：

> W4 **MInDS committed summary** 不是 reproducer 直接写出的文件。

回复却用 commit `cdbf1d2` 反驳整个 W4 手工转录问题。该 commit 实际只修改：

```text
_repro/emotion_pool_paired_v2.json
scripts/pool_method_probe_paired.py
```

它成功修复了 **emotion headline t-CI** 的脚本产出，是一个应接受的窄项；它没有修改 MInDS。
当前 `repro_minds14_toolintent.py` 仍只在 E 盘写三个 `report_*.json` 并 print CI，不生成提交的
`_repro/minds14_toolintent_paired.json`，也没有 reducer/transformation log。

**裁决：**

- Emotion generator current state：`ACCEPT`；
- Historical hand-insertion incident：`CONFIRMED, corrected but not erased`；
- MInDS generator mismatch：`CONFIRMED / OPEN`；
- 回复的总括 `STALE`：`REJECT`。

### RR-008：STOP-THE-LINE 不是 evidence freeze

团队当前确实停跑，但没有完成研究诚信审查要求的证据冻结：

- 无 `_repro`/E 盘 raw/MLflow/cache/model/runtime 的统一 SHA-256 inventory；
- 无 Git bundle/全部 refs 保存记录；
- 无 run ID→commit→input hash→output hash→claim 映射；
- W1 仍有 dirty AISHELL artifact；
- MLflow 负时长异常仍未解释。

停跑防止新 GPU 结果继续堆积；evidence freeze 则防止现有证据被善意清理、覆盖或失去来源。两者不可互换。

**裁决：** operational hold `ACCEPT`；RI-G0 evidence freeze `REJECT`。

### RR-009：机器可读撤回仍失败

现状：

- M3 文档 `status` 已承认 partial retraction，但同一 frontmatter 的 `verdict` 仍写
  `Q1b YES / LOCKED by M3 / +22.4%`。
- 归档 T7 的 frontmatter `status` 仍写 `Boundary-clean`，其后才有 Markdown `SUPERSEDED` 横幅。
- 原始 `m3_crossmodal.json`、`t7_rag_gate_probe.json` 没有 `validity: INVALID`、`superseded_by`。
- 全仓没有实际 claim ledger；相应 schema 只存在于法证审计报告的 proposal 代码块。

“人类在正文中能找到撤回”不等于“AI 默认不会继续使用旧阳性”。NISO 对撤回传播的建议明确要求状态
既能被人识别，也能被机器读取。[NISO RP-45-2024 CREC](https://www.niso.org/publications/rp-45-2024-crec)

**裁决：** `REJECT`。

### RR-010：外部主张并未全部废止，现行论文仍传播旧结论

回复把下列事项列为“已执行”：W4 弃 disentanglement、W1 headline 改述、对外术语替换。

但当前 active 文档仍包括：

- `wiki/Project-Thesis.md`：W4 training-free RL disentanglement 仍是核心 thesis；
- `wiki/Architecture.md`：W4 仍写 disentangle frozen embeddings；
- `wiki/W4-Training-Free-RL-Feasibility.md`：仍写 `The thesis holds`；
- `wiki/Per-Work-Status.md`：标题仍为 speech disentanglement，且写 MBR all-N n.s.；
- `papers/agent-level-tfrl/main.tex`：仍写 genuine training-free RL、hard BoN 是 Gibbs tilt 的 concrete
  realisation、三 generation seeds、macro-WER headline、MInDS zero-shot。

因此更准确状态是：

```text
OWNER DECISION: DONE
PROPAGATION INTO ACTIVE CANON/PAPER: NOT DONE
```

**裁决：** `PARTIAL/REJECT completed wording`。

### RR-011：#23–#29 是不可审计的散文票据，不是完成证据

全仓搜索显示 #25–#29 的执行定义只出现在回复、rulings 与 Decision Log。没有稳定 ticket artifact、状态、
acceptance test、evidence commit、reviewer 或 verified_at。它们也可能存在于外部任务系统，但回复没有给
可访问链接或 namespace。

至少要区分六种状态：

```text
ACKNOWLEDGED → DECIDED → TICKETED → IMPLEMENTED → VERIFIED → PUBLISHED
```

创建 #25 只能算 `TICKETED`；写“G2 将成为硬规则”只能算 `DECIDED`；只有代码、测试、artifact 与独立
复核均存在时才能算 `VERIFIED`。

**裁决：** #25–#29 全部 `OPEN/TICKETED`，不能出现在“已完成科学整改”清单。

### RR-012：`65 格重跑`再次混淆 dataset key 与 result cell

`redraw_manifest.json` 有 65 个 dataset keys。但当前与这些 keys 匹配的 baseline JSON 至少有 241 个
dev/test result cells；因此“65 格”不是仓库惯用的 `dataset×backbone×split` cell 口径。

更严重的是，重抽工具沿用旧 deterministic test seed/test-first 逻辑。独立比较当前可解析 test artifacts：

- 64 个可比 dataset keys 中，至少 40 个的 planned new-test IDs 与现有旧 test 完全相同；
- 至少 81 个当前 test result cells 使用的 IDs 与 planned test 完全相同。

所以这套 redraw 可以修复 dev/test item overlap，却不能创造“从未被看过”的 locked test。公开 manifest
也意味着这些 IDs 已经进入团队知识。

反复自适应使用 holdout 会导致对 holdout 本身过拟合；仅重新命名或重新锁定已看过的数据不能恢复
独立性。[Dwork et al., Generalization in Adaptive Data Analysis and Holdout Reuse](https://proceedings.neurips.cc/paper/2015/hash/bad5f33780c42f2588878a9d07405083-Abstract.html)

**裁决：** stop rerun `ACCEPT`；当前 redraw 作为 fresh locked-test `REJECT`。

### RR-013：Wiki 归档方案会让共享 Wiki 丢页，并已产生断链

commit 将 51 个页面移入 `wiki/archive/`。但是 `scripts/wiki-sync.sh` 明确：

```bash
find "$WORK_DIR" -maxdepth 1 -name '*.md' -delete
for f in "$SRC_DIR"/*.md; do
    cp "$f" "$WORK_DIR/"
done
```

它只发布顶层 `wiki/*.md`，完全忽略 `wiki/archive/**`。一旦同步：

- 51 个所谓 archived pages 不会进入 GitHub Wiki；
- 远端旧顶层页面会被删除；
- 它们不是“共享可访问归档”，只剩普通 Git 历史/本地子目录。

链接检查还发现：

- `wiki/survey/README.md` 新增的 16 个 `archive/survey/...` 相对链接全部解析到不存在的
  `wiki/survey/archive/...`；正确路径至少应从 `../archive/...` 开始。
- 6 个被移动页面仍被顶层 Wiki 文件以 19 个 `[[Page]]` 链接引用，包括
  `Validation-Experiment-Matrix`、T7、Research-Question-Framing 等。

回复宣称“51 件归档 + 86 件 LOG 横幅”。当前精确 marker 统计只有 39 个 `**LOG**` 文件；若 86 是
分类数而非实际加横幅数，回复应提供分类 ledger，而不能写成“86 件已加机器横幅”。

**裁决：** `REJECT`。归档 commit 在修复 sync 和 link checker 前不应推送/发布。

### RR-014：fake-model E2E 不能单独根治真实 runtime 问题

回复把“全臂 fake-model E2E green”设为 G2 证据。Fake E2E 很重要，但这次故障包含真实维度、registry
返回名、embedding API 和 llama.cpp audio semantics；完全错误的 real runtime 可以在 fake 上全绿。

G2 必须三层：

1. unit/fake E2E；
2. 每个真实 embedder/runtime 的 1–3 item live integration smoke；
3. 冻结 ref-config 的真实 tiny end-to-end reconstruction，summary 可从 row output 重建。

三层全绿才允许大网格。

**裁决：** current G2 design `PARTIAL`。

### RR-015：理论问题被接受，但当前 paper bridge 仍未隔离

回复正确承认 ordinary hard BoN 没有 operator-linked Lean proof，却没有修改或 quarantine 当前 paper。
论文仍称 hard BoN 是 Gibbs tilt 的 concrete realisation/β→0 tilt，并用 Gibbs identity 组织实验叙事。

普通 BoN 的输出 policy 是 order-statistics induced distribution；有限候选集上 softmax 的 β→0 argmax
不等于分布层面固定 β 的 Gibbs tilt。相关理论文献正是分别推导 BoN policy 与 soft-BoN/tilted policy，
不是把二者直接视为同一对象。
[Beirami et al., 2024](https://arxiv.org/abs/2401.01879)、
[Soft Best-of-N, 2025](https://arxiv.org/abs/2505.03156)

**裁决：** acknowledgement `ACCEPT`；theory remediation `OPEN`；current paper claim `REJECT`。

### RR-016：“北星句”把未来目标写成完成时

回复收下的句子是：

> 我们系统测量了……并证明哪些增益是真实的……

但当前 W4 判据未过、Phase-A 不可执行、MBR 无 deployable gain、locked test 不新鲜、operator-linked
theorem 为 0。它只能写成：

> `TARGET CLAIM — NOT YET ESTABLISHED`：我们将系统测量……并区分……

否则又一次把 proposal 写成 result。

**裁决：** `REJECT completed tense`。

## 6. 对新 G0 primary question 的严格审查

团队签署的问题是：

> speech-keyed 知识组织 × 检索 × 递送 + label-free selector 能把 oracle headroom 实现出多大比例 ρ？

### 6.1 值得肯定的地方

- 明确冻结模型与部署边界；
- 明确区分 oracle 和 deployable selector；
- 接受负结果也可发表；
- 同时报告绝对 delta、cost、retrieval metric；
- 纳入 no/random/oracle retrieval 和 own-ASR controls；
- 设有机制 kill 分支，不再把所有 null 都解释成继续扩张的理由。

### 6.2 为什么仍不能判 G0 fully delivered

它把至少五个可独立失败的对象绑在一起：

1. knowledge organization；
2. speech-key retrieval；
3. context delivery；
4. candidate generation；
5. label-free selection。

任一组合差异都可能来自 prompt 长度、query quality、candidate support、retrieval recall 或 selector，
无法成为单一机制论文的 primary contrast。它还没有冻结 primary task/dataset、arm、cluster、SESOI、
power、multiplicity family、两个 test surfaces 的身份和访问控制。

`random retrieval ≈ best` 中的 `≈` 也不是统计规则；必须有预注册 equivalence margin。没有 margin，
“未显著不同”不能触发等价判断。

### 6.3 ρ 是高风险 ratio estimand

当前定义：

```text
ρ = (R_selector − R_greedy) / (R_oracle − R_greedy)
```

必须先解决：

- WER 是 lower-is-better；应定义统一 utility（如 `U=-WER`）或改进方向。
- ρ 应是 aggregate improvements 的 ratio，不能平均 per-item ratios。
- 分母接近 0 或 CI 跨 0 时 ratio 会爆炸、反号或产生无界区间。
- 把 denominator≤0 items 排除会条件化在有利 headroom 上，造成向上偏差。
- numerator 与 denominator 必须在同一 pool、同一预算、同一 cluster bootstrap draw 中联合计算。
- 必须同时把 absolute deployable delta 设为 co-primary；ρ 不能替代可部署绝对效果。

Ratio CI 在分母接近零时需要 Fieller 或适当 joint-bootstrap 处理，普通对称 CI/先筛分母并不可靠。
[Franz, Ratios: A Short Guide to Confidence Limits and Proper Use](https://arxiv.org/abs/0710.2024)

### 6.4 推荐的真正单问题版本

团队应在以下两者中选一个 primary，不要再次共享 headline：

#### Proposal-S：Selector realization（推荐给 W1）

> 在固定 frozen Qwen3-Omni、固定 untouched ASR cohort、固定 noise strata 与固定候选预算下，
> 一个只使用部署时可得信号的 label-free selector，是否在 corpus WER 上稳定优于 greedy、random pick
> 和等预算 MBR/ROVER/置信度 baseline，并实现预注册比例的 oracle pool headroom？

Primary：absolute corpus-WER delta；ρ 只作 secondary。检索和知识组织不进入这篇 primary experiment。

#### Proposal-R：Retrieval causality（推荐给 Step-2）

> 在 frozen generator、audio-only/own-ASR query、source/eval disjoint 且 answer-scrubbed KB 下，
> speech-keyed retrieval 相对 no-retrieval 和 random retrieval 是否带来预注册的 end-to-end 改善，
> 且 oracle retrieval 是否证明瓶颈确实在 retrieval？

Primary：end-to-end task delta；retrieval R@k 和 reader conditional accuracy 为机制分解。selector 固定，
不在同一 primary claim 中优化。

如果 owner 坚持端到端组合，则必须把它定位成 system evaluation，而不是单一机制发现；并用 factorial
或 sequential mediation 拆分 organization/retrieval/delivery/selection。

## 7. 当前工作应如何重新标记

### 7.1 回复文本的状态词必须重写

建议把“已完成动作清单”拆为：

| 当前项目 | 正确状态 |
|---|---|
| stop-the-line | `IMPLEMENTED / CURRENTLY OBSERVED` |
| owner G0 decision | `DECIDED` |
| response/rulings local commit | `COMMITTED LOCALLY / NOT PUSHED / NOT WIKI-SYNCED` |
| W4 claim downgrade | `DECIDED / PARTIALLY PROPAGATED` |
| #25–#29 | `TICKETED OR PROPOSED / NOT IMPLEMENTED` |
| Phase-A engineering | `BLOCKED / NOT EXECUTABLE` |
| group-aware redraw | `DESIGNED / NOT IMPLEMENTED` |
| ASR metric correction | `IDENTIFIED / NOT PROPAGATED` |
| theory rewrite | `OPEN` |
| claim ledger/evidence freeze | `NOT STARTED OR NOT EVIDENCED` |

### 7.2 必须撤销或更正的回复原句

1. `全部动作已执行` → `owner 已裁定；传播和实现未完成`。
2. `W4 手工转录问题 STALE` → 分成 emotion-corrected 与 MInDS-open 两项。
3. `MBR non-significant at every N` → 报 corpus 曲线，N1/N2 显著变差。
4. `修正依赖只会更 NULL` → `依赖使现有不确定性估计无效，方向需 grouped rerun`。
5. `zero-shot MInDS` → `transductive 3-shot/class fixed-support result`。
6. `G0 已交付` → `METHOD-G0 partial；RI-G0/RI-G1 not delivered`。
7. `6 independent agents` → `6 internal adversarial agents`，除非有真正外部独立复核。
8. `已入库` → 在 push/wiki-sync 前写 `local commit only`。

## 8. 重新开放实验的硬门

### Gate A — 立即门：研究记录隔离

- 冻结 `_repro`、E 盘 raw、MLflow、cache、model/runtime 与环境 hash inventory。
- 建立 machine-readable claim ledger；M3/T7 必须默认解析为 INVALID。
- 当前 paper 标 `QUARANTINED DRAFT`，直到 macro/corpus、seed、MInDS、BoN/Gibbs 全部修正。
- 修复 Wiki 归档发布策略和所有 broken links，再 push/sync `641bb655` 的后继 commit。

### Gate B — 统计门

- ASR generator 同时输出 S/D/I/N、corpus WER 与明确命名的 macro utterance-WER。
- seed 四分离，speaker/chapter hierarchical bootstrap。
- CREMA speaker-disjoint/nested group split；提交 row predictions；如声称 null，预注册 SESOI/equivalence。
- MInDS support/dev/test 严格分离，zero-shot arm 无 examples，factorial ablation 与多 support draws。
- 所有旧 overlap result cells 机器标记 INVALID/SUPERSEDED；不得只按 65 keys 估算工作量。

层级数据不能把子观测当独立单位；cluster/hierarchical resampling 应匹配实验单位和依赖结构。
[Saravanan et al., Hierarchical Bootstrap](https://pmc.ncbi.nlm.nih.gov/articles/PMC7906290/)

### Gate C — 工程门

- #25–#29 进入真实 ticket schema并有 acceptance tests/evidence commit。
- fake E2E + 每个 real runtime live smoke + tiny ref-config reconstruction 全绿。
- cited reproducer 必须直接产生 committed summary；MInDS 先修。
- result JSON 包含 commit/dirty/model/runtime/data/manifest/env/run/output hashes。

### Gate D — G0/G1 科学门

- 只选 Proposal-S 或 Proposal-R 之一为 primary。
- 冻结 task/dataset/arm/cluster/metric/MCID/power/multiplicity。
- final test 必须此前未被用于方向、prompt、arm 或阈值选择，并由访问日志证明。
- success、futility、equivalence 三种门分别定义，不能用一个“不显著”同时承担三种含义。

### Gate E — 独立复核门

- 非整改作者/非同上下文 AI 独立复算主表。
- 34-row audit ledger 与 headline 自动对账。
- Wiki/source relative link checker 与远端 Wiki link checker 均为 0 broken。
- 只有在 artifact 可执行、完整且能重建论文主结果后，才允许写“整改已验证”。

## 9. 给团队 AI 的机器可读裁决

```yaml
review_id: RESPONSE-REVIEW-2026-07-11
reviewed_response: 2026-07-11-response-to-reviewer-stage1-audit.md
reviewed_commit: 641bb655e12ebc47332aa86eb5b9b1dba198fb69
global_verdict: RESPONSE_PARTIALLY_ACCEPTED_REMEDIATION_CLOSURE_REJECTED
stop_the_line: REMAINS_IN_FORCE
publication_readiness: RED
intent:
  fabrication: NOT_ALLEGED
  deliberate_deception: NOT_ESTABLISHED
accepted:
  - operational_stop_the_line
  - phase_a_not_executable_diagnosis
  - w4_claim_downgrade_direction
  - operator_linked_theorem_count_zero
  - provenance_fields_missing_diagnosis
partial:
  - local_commit_exists_but_not_pushed_or_wiki_synced
  - w4_claim_propagation
  - seed_redesign
  - group_aware_redraw_plan
  - method_g0_claim_tree
rejected:
  - asr_unqualified_macro_wer_headline
  - mbr_non_significant_at_every_n
  - crema_wider_ci_means_more_null
  - minds_zero_shot_label
  - minds_generator_issue_marked_stale
  - machine_readable_invalidity_complete
  - wiki_archive_complete_and_link_safe
  - ticket_creation_equals_remediation_execution
  - hard_bon_equals_lean_proven_gibbs_operator
  - all_external_claims_already_propagated
integrity_gates:
  RI_G0_evidence_freeze: NOT_DONE
  RI_G1_claim_ledger: NOT_DONE
  RI_G2_independent_reproduction: NOT_DONE
method_gates:
  METHOD_G0_single_question: PARTIAL
  METHOD_G1_preregistration: NOT_DONE
  METHOD_G2_executable_real_runtime: NOT_DONE
prohibited_until_reopened:
  - new_phase_a_or_step3_gpu_runs
  - publication_claim_upgrade
  - cite_m3_or_t7_as_positive
  - call_minds_zero_shot_or_reward_guided_rl
  - call_three_asr_blocks_generation_seed_replications
  - report_macro_utterance_wer_as_unqualified_wer
  - claim_current_wiki_archive_is_shared_and_link_safe
next_review_requires:
  - pushed_commit_and_wiki_sync_or_explicit_local_only_status
  - evidence_freeze_manifest
  - machine_readable_claim_ledger
  - corrected_paper_or_quarantined_draft
  - corrected_asr_stats_and_seed_protocol
  - corrected_crema_and_minds_protocols
  - real_ticket_acceptance_evidence
  - wiki_sync_and_link_tests
  - one_primary_question_with_frozen_success_futility_equivalence_gates
```

## 10. 外部方法学校准

本复审在前一份法证报告的多源 survey 基础上，重点复核了团队回复新增的四类问题：

- **artifact 的“存在”与“验证”不同。** Functional artifact 至少应 documented、consistent、complete、
  exercisable；Results Reproduced 需要作者之外的团队取得主要结果。
  [ACM Artifact Review and Badging](https://www.acm.org/publications/policies/artifact-review-and-badging-current)
- **撤回必须机器可读。** 只在正文加横幅不足以防止自动系统继续使用旧阳性。
  [NISO RP-45-2024 CREC](https://www.niso.org/publications/rp-45-2024-crec)
- **自适应 holdout 复用会过拟合。** 已看过的 test manifest 不能通过重新锁定恢复 untouched 地位。
  [Dwork et al., 2015](https://proceedings.neurips.cc/paper/2015/hash/bad5f33780c42f2588878a9d07405083-Abstract.html)
- **未显著不等于等价。** 要支持实质无效，需要 SESOI 和 equivalence test。
  [Lakens, 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5502906/)
- **ratio estimand 在小分母下不稳定。** ρ 需要联合推断和明确的 denominator policy。
  [Franz, 2007](https://arxiv.org/abs/0710.2024)
- **层级数据要匹配 cluster 单位。** 逐 clip/row bootstrap 不能自动覆盖 speaker/session 依赖。
  [Saravanan et al., 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7906290/)
- **BoN 与 Gibbs/soft-BoN 不能只凭极限直觉等同。**
  [Beirami et al., 2024](https://arxiv.org/abs/2401.01879)、
  [Soft Best-of-N, 2025](https://arxiv.org/abs/2505.03156)
- **representation probe 不能自动证明 disentanglement。** 需要控制 probe capacity、nuisance、
  counterfactual 与 identifiability。
  [Locatello et al., 2019](https://proceedings.mlr.press/v97/locatello19a.html)、
  [Hewitt & Liang, 2019](https://aclanthology.org/D19-1275/)、
  [Voita & Titov, 2020](https://aclanthology.org/2020.emnlp-main.14/)

## 11. 最终判词

团队回复不是无价值的公关文本。它保留负结果、公开承认簿记失实、暂停运行并接受大量不利裁决，说明
项目具备自我纠错意愿。严厉复审应承认这一点。

但科学审查评价的是证据状态，不是态度。当前最准确的状态是：

> **ACKNOWLEDGEMENT ACCEPTED; IMPLEMENTATION MOSTLY OPEN; STATISTICAL RESPONSE PARTLY WRONG;
> INTEGRITY REMEDIATION NOT CLOSED.**

尤其不能接受的，是回复刚刚承认“按代理完工报告入账、未经 E2E 验证”的系统缺陷，却又把新一轮的
agent consensus、散文票号、未传播的 owner 裁定和 future gates 写成“全部动作已执行”。这不证明故意
欺骗，却证明完成状态治理仍未被真正修复。

因此，直到 evidence freeze、claim ledger、ASR/CREMA/MInDS 纠正、Wiki 发布链、real-runtime E2E、
fresh locked test 和单一 primary proposal 全部有可核验凭据之前，STOP-THE-LINE 必须继续，论文维持 RED。
