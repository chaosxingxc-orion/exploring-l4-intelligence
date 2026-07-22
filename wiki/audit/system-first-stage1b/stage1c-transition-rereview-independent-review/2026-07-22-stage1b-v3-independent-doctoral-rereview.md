---
transaction: "INDEPENDENT_DOCTORAL_STAGE_TRANSITION_REREVIEW"
review_date: "2026-07-22"
review_target: "wiki/audit/system-first-stage1b/stage1c-transition-rereview-request/2026-07-22-stage1b-v3-speech-prior-remediation-and-stage1c-rereview-proposal.md"
target_sha256: "08de0816e05f0679ea8ed319078d8011f2528ae83aa227fa0804406454ea8bbd"
claimed_release_commit: "626914a963637354642116b938eb9ab745a099c8"
resolved_release_commit: "626914adb460d827fa02d8272ac5c406201dfa82"
review_status: "WITHHOLD_WITH_BOUNDED_DEFECTS"
stage1c_problem_comparison_authority: "WITHHOLD_PENDING_P0_REPAIR"
stage1c_rubric_and_asset_reconciliation_preparation: "ALLOW"
model_api_dataset_metric_reproduction_prototype_authority: "WITHHOLD"
novelty_verdict: "NOT_REQUESTED_AND_NOT_PERMITTED"
---

# Stage-1B v3 → Stage-1C 独立严格复审：语音/多模态先行研究与资产闭环

> 审查角色：严格外部审稿人 / 博士生导师  
> 审查对象：上列固定 proposal 及其声称的 v3 scientific release  
> 审查方法：项目既有论文集、CURRENT bibliography、registry、冻结 Git blobs 与本地资产优先；外部检索只核验已知关键论文的身份与研究角色  
> 写入纪律：本报告是新的独立 AUDIT 交易件；未修改 proposal、release、CURRENT、registry、资产锁、脚本或研究代码

## 0. 最终裁决

```text
CURRENT_STAGE                              = STAGE_1B_LATE_CLOSEOUT_AND_TRANSITION_REREVIEW
STAGE_1A                                  = CLOSED
STAGE_1B_DISCOVERY_FLOW                    = PASS_WITH_DISCLOSED_OPEN_SURFACES
STAGE_1B_V3_LISTED_ARTIFACT_REPLAY         = PASS_AT_RESOLVED_COMMIT_45_OF_45
DECLARED_FULL_RELEASE_COMMIT_IDENTITY       = FAIL
STAGE_1B_SPEECH_SUPPLEMENT_32_PDF_LOCK      = PASS_32_OF_32
STAGE_1B_81_WORK_DEPTH_ACCOUNTING           = FAIL_7_FALSE_FULLTEXT_LABELS
SPEECH_OMNI_PRIOR_RECONCILIATION            = FAIL_BOUNDED_SOURCE_SELECTION
CITATION_IDENTITY_AND_PAGE_PROVENANCE       = PARTIAL_PASS
REWARD_GUIDED_VS_ORCHESTRATION_SEPARATION   = INCOMPLETE
RELATED_CODE_LOCAL_LOCK                     = FAIL
DATASET_ASSET_GLOBAL_LOCK                   = FAIL_STALE_AND_INCOMPLETE
STAGE_1C_RUBRIC_PREPARATION                 = ALLOW
STAGE_1C_FORMAL_PROBLEM_COMPARISON          = WITHHOLD
MODEL_OR_REPRODUCTION_EXECUTION              = WITHHOLD
ACADEMIC_FRAUD_EVIDENCE                     = NOT_ESTABLISHED
REMEDIATION_SCOPE                           = TARGETED_RECONCILIATION_ONLY
NEW_BROAD_D0_SURVEY                         = NOT_REQUIRED
```

**正式结论：`WITHHOLD_WITH_BOUNDED_DEFECTS`。目前不能签署 Stage-1C 正式启动。**

这不是因为 20,727 条 D0 仍然不够多，也不是要求团队继续无边界扩充 survey。v3 已经实质关闭了上一轮的几个主要问题：45 个列入 release 的对象可重放，32 条语音/omni supplement 可比较，AudioGenie-Reasoner、VoiceAgentRAG、EVA-Bench、JarvisBench 等已经进入 synthesis，H5 仍被正确隔离，且没有执行模型实验。

但本轮发现四个必须先修复的结构问题：

1. proposal、HOT/CURRENT router 与 audit index 声称的完整 commit SHA 不存在；短前缀实际解析到另一个完整 SHA；
2. 81-work coverage 中 7 条被写成 `FULLTEXT_ROUTED`，但其冻结来源明确记录 `local_fulltext=false` / abstract review，本地也没有对应 PDF；
3. “四来源 81 篇闭合”只证明这四个来源内部的路由完整，未与项目已有 seed manifest、CURRENT bibliography 和 226-work registry 做 known-prior reconciliation；Speech-Copilot、AudioGPT、EchoChain、From Text to Voice 以及若干 speech reward/evaluator 先行工作因此仍在承重结构之外；
4. `docs/datasets.lock.json` 不再是当前磁盘的完整快照。锁表的 28 个数据集和 3 个模型都存在，但实盘有 39 个数据目录和 20 个模型目录；与 Stage-1C 可行性直接相关的 `audio2tool` 已在盘上却未锁定，其他多个关键 benchmark 仍未下载或未形成 exact-identity lock。

这四项都会影响 Stage-1C 的 common-rubric 比较，尤其是 nearest prior、evaluator coverage 和 local feasibility。修复后无需再开大规模 discovery，可进行一次窄复审。

## 1. 当前阶段判定

当前不是 Stage-1A，也不是 Stage-1C 已开始，而是：

> **Stage-1B late closeout / fixed-release transition re-review pending。**

依据如下：

- `wiki/Research-Objective.md` 明示当前为 `Stage-1B late execution and closeout`，Stage-1C 仍待独立签字；
- D0、delta、T1、citation surface、mapping release 和 unranked eligible inputs 均已经形成；
- proposal 只申请 Stage-1C problem comparison，不申请 novelty、模型、API、数据指标、复现或 prototype 权限；
- v3 manifest 已生成并进入 Git，但其 reviewer-facing 完整 commit 身份写错；
- Stage-1C 所需的 local-feasibility 资产视图仍不可信，因此尚不能开始正式比较和选择。

允许团队在本轮后准备 Stage-1C rubric、修复资产清单、整理候选卡模板；不得把这些准备活动写成 Stage-1C 已签署，更不得触碰模型或运行数据集指标。

## 2. 多轮对抗式审查

### Round A：发布对象身份与重放

#### A1. 45 个 manifest 条目本身通过

对实际可解析 commit `626914adb460d827fa02d8272ac5c406201dfa82`，逐项读取 37 个 Git blob；对 8 个 external assets 读取冻结路径，并核对 manifest 记录的 bytes 与 SHA-256：

```text
manifest entries     = 45
Git artifacts        = 37
external artifacts   = 8
missing              = 0
byte mismatch        = 0
SHA-256 mismatch     = 0
```

定向运行：

```text
python -m pytest -q \
  scripts/survey/test_sf_stage1b_evidence_release_contract.py \
  scripts/survey/test_sf_stage1b_release_manifest.py

29 passed, 3 subtests passed
```

因此，不能指控团队伪造了 45 项重放结果，也不能说 release 只是未提交 worktree 的拼装。

#### A2. reviewer-facing 完整 SHA 失败

proposal front matter 和正文声称：

```text
626914a963637354642116b938eb9ab745a099c8
```

Git 结果：

```text
git rev-parse 626914a
=> 626914adb460d827fa02d8272ac5c406201dfa82

git cat-file / show 626914a963637354642116b938eb9ab745a099c8
=> bad object / not a valid commit
```

错误长 SHA 还出现在：

- `wiki/Research-Objective.md`；
- `wiki/survey/current/status.md`；
- `wiki/survey/current/README.md`；
- `wiki/audit/system-first-stage1b/INDEX.md`；
- 本次 re-review proposal。

manifest 采用 `CONTAINING_GIT_COMMIT` 模式，因此短前缀所指向的 release 内容仍可重放；但 reviewer 被正式要求签署的是一个不存在的完整对象。**短 SHA 可解析不能替代 reviewer-facing full SHA 的固定身份。** 这是 release identity P0，而不是纯排版错误。

#### A3. 本轮判定

```text
LISTED_ARTIFACT_INTEGRITY = PASS
REVIEW_OBJECT_IDENTITY    = FAIL
```

只有在新的 dated correction / superseding transaction 中明确给出真实完整 SHA，并让 HOT/CURRENT/audit router 一致指向它，独立签字才有对象。

### Round B：引用、全文深度与语音/多模态覆盖

#### B1. 32 条 supplement 的引用质量明显改善

v3 的 32 条 supplement 已实现：

- 32/32 唯一 arXiv identity；
- 32/32 reviewer-facing author/year/stable link；
- 32/32 本地 PDF 存在；
- 32/32 PDF SHA-256 与 supplement 一致；
- 32/32 有页码和文本 anchor；
- role 分离为 23 direct、8 instrument、1 boundary；
- paper-reported metrics 明确未被写成项目复现结果。

就 **32 条被选为承重条目的自包含引用** 而言，本轮可给 `PASS`。这些引用足以支持“论文里报告了何种系统路径”的 Stage-1B 编码，但不能支持“该方法在本项目环境中有效”的实验性结论。

#### B2. 81-work coverage 的全文深度有 7 条内部矛盾

coverage 统计声称：

```text
FULLTEXT_ROUTED = 70
ABSTRACT_ROUTED = 11
```

对 coverage、fulltext ledger、冻结 `rescue-audit.jsonl` 和实盘 PDF 交叉核对后：

- 63 条 `FULLTEXT_ROUTED` 可在本地找到对应 PDF；
- 7 条没有 fulltext ledger 成功行，也没有本地 PDF；
- 其冻结来源记录明确包含 `local_fulltext=false`，review level 是 `ABSTRACT_MANUAL`、`ABSTRACT_AND_ARTIFACT` 或 `LEXICAL_GATE_ACCOUNTED`。

错误标成 `FULLTEXT_ROUTED` 的 7 条是：

| arXiv ID | title | coverage role | 冻结来源的真实深度 |
|---|---|---|---|
| 2505.17862 | Daily-Omni | `H5_HELD` | abstract / no local fulltext |
| 2507.22898 | VOICE stroke assessment | `BOUNDARY_COMPARATOR` | abstract / no local fulltext |
| 2510.11098 | VCB Bench | `MEASUREMENT_INSTRUMENT` | abstract + artifact check / no local fulltext |
| 2601.06235 | AI glasses voice-agent system | `BOUNDARY_COMPARATOR` | abstract / no local fulltext |
| 2602.00675 | JANUS | `BOUNDARY_COMPARATOR` | abstract / no local fulltext |
| 2603.23625 | voice-enabled smart speaker for care homes | `BOUNDARY_COMPARATOR` | abstract / no local fulltext |
| 2606.13049 | Y-BotFrame | `BOUNDARY_COMPARATOR` | abstract / no local fulltext |

这些条目当前都不是 23 条 direct supplement 方法，因此不需要扩大到新的方法精读。最小修复是：能取得 PDF 就 hash-bind；否则诚实改为 `ABSTRACT_ROUTED`，并禁止其承担 page-level claim。**不能继续把“人工看过摘要并做角色判断”写成“fulltext routed”。**

#### B3. “81 篇完整”是来源内完整，不是项目已知先行研究完整

proposal 对其限制写得相对诚实：81 篇只来自四个来源，且不主张 literature-universe closure。问题不在这句话本身，而在于它随后把“required typical identities”固定成了同一内部列表，再用测试证明该列表完整。这是一个循环式 gate：

```text
内部选择四个来源
  -> 从四个来源生成 required identities
  -> 测试 required identities 全部出现
  -> 得出 typical identities 已完整
```

它无法发现项目自己已经登记、但没进入四来源并集的已知先行工作。

本地交叉核对结果：

- `wiki/survey/current/bibliography.md` 有 75 条 arXiv 记录；仅 16 条进入 81-work coverage，59 条在其外；
- 这 59 条并非都应进入 speech-agent supplement，但其中存在直接影响当前三个非 H5 bundles 的条目；
- 226-work registry 中有 76 条 `speech_primary_object=true`，只有 9 条进入 81-work coverage；同样不能把其余 67 条全部视为遗漏，但至少需要对 direct/system/reward/interactive 相关子集做 reconciliation；
- 早期 seed manifest 已登记 AudioGPT、MM-ReAct、HuggingGPT 和 Speech-Copilot，但它们没有进入 v3 81-work coverage 或 32-row reference appendix。

至少下列 known priors 必须被定向处置：

| known prior | 为什么必须可见 | 对当前 bundle 的影响 | 最低要求 |
|---|---|---|---|
| [Speech-Copilot](https://arxiv.org/abs/2407.09886) | training-free、LLM 程序生成、模块化语音工具编排的直接先行系统 | tool/orchestration；也约束“omni agent system”历史定位 | D2；进入 direct 或明确 boundary，并与 AudioToolAgent 比较 |
| [AudioGPT](https://arxiv.org/abs/2304.12995) | 早期 ChatGPT + 音频 foundation models + ASR/TTS 的经典复合系统 | 约束 multi-model federation / orchestration 的历史起点 | 至少 D1/D2 role route；不能从系统 genealogy 消失 |
| [MM-ReAct](https://arxiv.org/abs/2303.11381) | 中央 LLM 编排多模态专家的典型 origin-domain system | 约束“omni agent”与既有 multimodal tool-agent 的差分 | 作为非语音 origin boundary 进入统一 genealogy |
| [EchoChain](https://arxiv.org/abs/2604.16456) | 专门测量中断后的 state update reasoning，且有 paired half-duplex control | 直接改变 interactive/full-duplex 的 failure taxonomy 与 instrument set | D2 instrument route；进入 interactive bundle |
| [From Text to Voice](https://arxiv.org/abs/2605.15104) | 把可验证 text tool benchmark 转成配对 audio evaluation，并保留 gold annotations | 提供成本较低、可验证的 voice-tool evaluation route | 已有本地 PDF，应进入 instrument comparison |
| AuTAgent 2602.13685 | 当前 registry 已有 D2，学习型 tool gate 是 training-dependent close boundary | 约束 training-free tool selection 与 learned routing 的边界 | 从 registry 定向纳入 81 reconciliation；不得继续遗漏 |
| [WavReward](https://arxiv.org/abs/2505.09558) | speech-input reward evaluator，覆盖 spoken dialogue IQ/EQ | evaluator/reward reliability 的训练型上界与 artifact-risk boundary | 至少 D1/D2 boundary route |
| [SDiaReward](https://arxiv.org/abs/2603.14889) | multi-turn speech episode preference reward，覆盖 modality/colloquialness | evaluator scope、episode-level preference 与 shift risk | 至少 D1/D2 boundary route |
| [GSRM](https://arxiv.org/abs/2602.13891) | reasoning-centric speech reward model，使用大规模 human ratings | speech reward 的训练型对照与自然度维度边界 | 至少 D1/D2 boundary route |

这里不要求把所有 trained reward models 纳入 23 条 training-free direct occupancy。相反，应把它们放进 `MEASUREMENT_INSTRUMENT` 或 `TRAINED_BOUNDARY`，明确它们能测什么、为什么不能作为 TF-Strict 方法。

#### B4. 引用结论

```text
32_ROW_SELF_CONTAINED_REFERENCES    = PASS
32_ROW_LOCAL_PDF_AND_PAGE_ANCHORS   = PASS
81_WORK_SOURCE_INTERNAL_ROUTING     = PASS
81_WORK_DEPTH_SEMANTICS             = FAIL
KNOWN_PRIOR_RECONCILIATION          = FAIL
LITERATURE_UNIVERSE_CLOSURE         = NOT_CLAIMED_AND_NOT_REQUIRED
```

### Round C：研究范畴与分类学

#### C1. 没有实验越界

本轮未发现模型加载、API 调用、数据集指标、smoke、复现或 prototype 运行。proposal 对 Stage-1B / Stage-1C / Stage-2A / Stage-2B 的边界总体正确：

- Stage-1B 负责 method paths、proximity、contradictions、instruments 和 reproducibility conditions；
- Stage-1C 比较并选择问题；
- Stage-2A 才先复现 nearest prior，再收敛技术方案；
- Stage-2B 验证干预与失败条件。

因此，本轮问题不是“实验提前跑了”，而是“选题输入的证据和本地可行性状态还没有完全对齐”。

#### C2. `DIRECT_CONTROL_METHOD` 仍然过宽

23 条 direct 中混合了至少三种不同事物：

1. **外部系统编排**：i-Code Studio、FAM-HRI、Langbar、Enterprise Realtime Voice Agent 等；
2. **反馈/验证驱动的循环**：AudioGenie-Reasoner、Interactive ASR、EChO-Agent、Omni-Decision 等；
3. **工具/证据调用但无独立 reward/evaluator**：AudioToolAgent、Audio-Maestro、Agent-Omni 等。

这三类都可以是 `system-first` 的直接先行工作，但不能因为都有 `signal -> action edge` 就被读成“training-free RL 已有 23 个直接先行方法”。当前 proposal 没有明确做出这种 novelty 声称，因此尚未越界；然而 Stage-1C 若以 `direct count=23` 推断 reward-guided controller 的拥挤度，会产生概念污染。

最小分类修复不是重写 32 条 schema，而是增加一个正交字段或派生表：

```text
control_basis = {
  EXTERNAL_ORCHESTRATION_ONLY,
  STATE_OR_EVENT_GATED,
  EVALUATOR_OR_VERIFIER_GATED,
  REWARD_GUIDED_SELECTION,
  TRAINED_POLICY_BOUNDARY,
  MEASUREMENT_ONLY
}
```

并为每条给出：`reward/evaluator identity`、`whether signal changes next action`、`whether policy/config was optimized on labels`、`whether any weights change`。这样才能把“第一创新点：omni agentic system”和“北极星：training-free reward-guided optimization”同时保住，而不是互相替代。

#### C3. H5 处理正确

Daily-Omni 仍为 `H5_HELD`，evidence-state 和 specialist tool/agent arbitration 两个 H5-dependent bundles 仍不可选。没有 coder-B 却冒充双人一致性，也没有把 H5 偷渡进 occupancy。此项通过。

### Round D：本地论文、代码和数据资产

#### D1. 必须区分四种“本地”

```text
paper identity locked
paper PDF locally hash-bound
author code repository locally commit-pinned
benchmark/dataset locally revision/content-pinned
```

v3 主要完成了前两项，不能把它写成后两项也完成。

#### D2. 论文全文状态

```text
32-row load-bearing supplement PDFs  = 32/32 local and hash-matched
81-work rows labelled FULLTEXT       = 70
verified local PDFs among those 70   = 63
false FULLTEXT labels                = 7
explicit ABSTRACT_ROUTED exclusions = 11
```

所以“32 条承重论文全文已锁定”成立；“81 篇相关工作全文全部已下载”不成立。

#### D3. 代码仓状态

实盘 `speechrl-data/repos/` 顶层只有少量历史仓：AudioGenie-Reasoner、JitRL、mbr-for-asr、TPO、TTRL、slue-toolkit、slurp、instruction_following_eval，以及 `stage1b/Diffusion-ASR`。它不是 32 条 supplement 的 code-repository mirror。

因此：

- 多数 direct systems 的 author repository 未本地 clone/commit-pin；
- 226-work registry 中 `OPEN_SOURCE_VERIFIED=68` 只表示远端可核验，不等于本地存在；
- 本轮不能声称“相关代码已经全部下载并锁定”。

Stage-1C 不需要预先 clone 全部仓库。它需要对每个候选 bundle 的 nearest prior 给出 `REMOTE_VERIFIED / LOCAL_UNPINNED / LOCAL_COMMIT_PINNED / UNAVAILABLE`，并在选题前确认至少一条可进入 Stage-2A 的 reproduction route。

#### D4. 数据/模型锁与实盘不一致

`docs/datasets.lock.json` 当前声称：

```text
locked datasets = 28
locked models   = 3
total bytes     = 409,103,904,696
total GiB       = 381.008
```

存在性核对证明 28/28 数据集路径和 3/3 模型路径都存在。但双向盘点得到：

```text
disk dataset top-level directories = 39
disk model top-level directories   = 20
disk datasets bytes                = 652,848,697,386  (608.013 GiB)
disk models bytes                  = 110,181,716,329  (102.615 GiB)
disk datasets + models             = 710.628 GiB
whole speechrl-data root           = 813,171,448,994  (757.325 GiB)
unlisted dataset/model directories = about 325.009 GiB
```

未进入 lock 的 12 个数据目录：

```text
aishell-1
audio2tool
audiocaps-qa
auditorybench-plusplus
cn-celeb1
cn-celeb2
csemotions
esd
slurp
squtr
thchs-30
voxceleb1-test-split
```

未进入 lock 的 17 个模型目录：

```text
campplus-zh
clap-htsat-unfused
clsp
dasheng
emotion2vec-plus-large
emotion2vec-s
eres2netv2-zh
glap
lco-embedding-omni-3b-gguf
lco-embedding-omni-7b-gguf
meralion-2-gguf
meralion-speech-encoder-2
redimnet-b6
sense
sensevoice-small
wavlm-base-plus
wavlm-large
```

这不自动说明文件损坏；它说明 `datasets.lock.json` 是旧 baseline snapshot，而不是当前数据盘的完整 inventory。文件头仍称其为 “exact local snapshot”，因此当前语义不成立。

本报告只做了目录存在性、文件数和聚合字节盘点；没有为了审稿而重新 hash 约 757 GiB。修复也不应要求恶意元数据测试，而应先恢复结构性资产分类。

#### D5. 当前三个非 H5 bundles 的关键数据状态

| instrument / environment | 当前本地状态 | 审查结论 |
|---|---|---|
| VoiceAgentBench | 没有 exact `VoiceAgentBench` 本地数据/仓锁；现有 `voicebench` 是 `lmms-lab/voicebench`，不能凭名称混同 | 未锁定 |
| tau-Voice | 有 `tau2-bench`，但没有 exact tau-Voice voice extension 资产锁 | 父基座在，本体未锁定 |
| Full-Duplex-Bench v3 | 仍在 `docs/datasets.candidates.json`，未发现对应本地目录 | 未下载/未锁定 |
| Audio2Tool | 本地目录存在，约 9.755 GiB，但仍只在 candidates 文件，未进入 frozen lock | 已下载但未冻结 |
| Omni-DeepSearch | 未发现 exact 本地数据锁 | 未锁定 |
| EVA-Bench | `ServiceNow-AI/eva` 已在 lock，状态 `COMPLETE` | 已锁定，但仍需确认 Stage-1C 所需 split/task contract |
| IHBench | 未发现 exact 本地数据锁 | 未锁定 |
| LALM audio-judge reliability | supplement 自己披露 production recordings 私有、部分 adversarial audio 待发布 | 无法声称完整本地复现 |
| MMAR / MMAU-mini | 已锁定并存在 | 可支持静态 audio-reasoning feasibility，不等于 voice-agent/full-duplex feasibility |
| SoulX-Duplug | 已锁定并存在 | 可支持 turn-taking 邻近测量，不能自动替代 tau-Voice/FDB-v3 |

因此，对用户问题的直接回答是：**相关论文的 32 条承重 PDF 已下载；相关代码没有全部下载；相关数据集也没有全部下载；整个资产盘没有被当前 lock 完整覆盖。**

Stage-1C 不应以“把所有论文的数据都下载完”为前置条件。正确门槛是：资产状态必须真实、可区分，候选比较不得把 `remote public`、`local unpinned`、`local locked` 和 `private/unavailable` 混在一起。

## 3. 三个 `ELIGIBLE_NON_H5` bundles 的逐项审查

| bundle | v3 改进 | 当前承重缺口 | 本轮状态 |
|---|---|---|---|
| Budget / stop / repair | AudioGenie-Reasoner、Interactive/Agentic ASR、EChO、Omni-Decision 已进入；repair harm 和 noisy stop 已披露 | 需要用 `control_basis` 区分 verifier-gated 与一般 orchestration；nearest-prior code/data feasibility 未锁 | `CONDITIONALLY_ELIGIBLE_AFTER_P0` |
| Evaluator / reward reliability | 8 个 speech instruments 和 LALM-judge reliability 已严格编码 | WavReward、SDiaReward、GSRM、Omni-RRM/Omni-Reward 等训练型直接边界未在 81 reconciliation；数据可用性表不完整 | `WITHHOLD_UNTIL_TARGETED_RECONCILIATION` |
| Interactive / full-duplex | VoiceAgentRAG、Unit Agent、Pepper、tau-Voice、FDB-v3、EVA、IHBench 已可见 | EchoChain 和 From Text to Voice 缺失；exact local assets 只有部分存在；tau2/VoiceBench 名称近似可能被误当 exact benchmark | `WITHHOLD_UNTIL_TARGETED_RECONCILIATION` |

这张表不是在 Stage-1B 排名三个问题，而是在判断它们是否已具备被同一 rubric 公平比较的资格。

## 4. 学术诚信判断

本轮没有发现：

- 伪造论文；
- 伪造模型实验或指标；
- 捏造 45/45 manifest hash replay；
- 伪造 coder-B；
- 把 paper-reported metrics 冒充 project reproduction；
- 抄袭证据。

因此不能把现有问题直接定性为 academic fraud。

但存在三类实质性研究诚信风险：

1. **固定对象身份失真**：正式 full SHA 不存在；
2. **证据深度高报**：7 条摘要级证据写成 `FULLTEXT_ROUTED`；
3. **选择性综合风险**：项目早已登记的关键先行工作未进入四来源 81-work 承重面，而机器 gate 又只检查内部 required list。

目前更符合“版本/证据整合失败与选择性综合风险”，尚无证据证明主观欺诈。团队收到本报告后若仍继续使用错误 full SHA、继续称 70 条 fulltext、或在不披露上述 known priors 的情况下排名选题，风险性质将显著升级。

## 5. 最小整改计划

### P0-R1：修复唯一可签署的 release identity

必须：

1. 以新的 dated correction / superseding release 明确写入真实完整 SHA；
2. `git rev-parse <declared-full-sha>` 必须返回同一 40 位值；
3. proposal replacement、Research-Objective、CURRENT status/README 和 audit index 必须一致；
4. 重新对 45 项做一次 blob/external hash replay；
5. 不得修改本次或此前已经登记的 audit bytes，只能新建 correction/response。

验收：

```text
DECLARED_FULL_SHA_EXISTS = true
DECLARED_FULL_SHA_EQUALS_RELEASE_OBJECT = true
MANIFEST_REPLAY = 45/45, zero mismatch
```

### P0-R2：修复 81-work evidence-depth accounting

必须对 7 条冲突记录逐项二选一：

- 下载 PDF、记录 URL/bytes/SHA/local path/page anchor，再保留 `FULLTEXT_ROUTED`；或
- 改为 `ABSTRACT_ROUTED`，禁止承担 page-level conclusion。

checker 应增加正向语义检查，而不是恶意鲁棒性测试：

```text
if depth == FULLTEXT_ROUTED:
    require successful PDF ledger row
    require local path exists
    require local SHA == recorded SHA
```

### P0-R3：做一次 known-prior reconciliation，不重开 broad D0

输入集合只需取并集：

```text
v3 four-source 81 list
+ Stage-1A seed manifest
+ CURRENT bibliography speech/omni/direct/reward/interactive subset
+ retained registry speech_primary direct/instrument/boundary subset
```

优先处理本报告 B3 表的条目。每条只需输出：identity、role、depth、为何影响哪个 bundle、是否进入 strict supplement、若不进入则理由。不要把 59 条 bibliography 外部项或 67 条 registry speech-primary 外部项全部强制深读。

验收：

```text
Speech-Copilot   = routed
AudioGPT         = routed
MM-ReAct         = routed as origin boundary
EchoChain        = routed
From Text to Voice = routed
AuTAgent         = reconciled from registry
speech reward-model boundary set = explicitly routed
```

### P0-R4：恢复资产事实层，不要求把所有资产都下载完

不要简单把 757 GiB 全部塞进一个新 lock。应至少分三层：

1. `FROZEN_BASELINE`：当前 28 datasets + 3 models，保留原快照语义；
2. `LOCAL_CANDIDATE_UNFROZEN`：本地新增的 12 dataset dirs、17 model dirs，记录 path/files/bytes/source/revision 状态；
3. `SURVEY_AND_REPRO_AUXILIARY`：survey corpus、repos、logs、临时 repro 资产，不混入 dataset/model 总数。

对 Stage-1C 三个候选 bundles 再建立小型 acquisition matrix：

```text
paper_pdf_status
author_repo_status + commit
dataset_status + exact upstream identity/revision
license/access
local path
files/bytes or content fingerprint
stage2 reproduction blocker
```

必须特别纠正：

- `audio2tool = LOCAL_UNFROZEN`，不是 `CANDIDATE_NOT_ON_DISK`；
- `voicebench != VoiceAgentBench`；
- `tau2-bench != tau-Voice`；
- `EVA-Bench = LOCAL_LOCKED`；
- Full-Duplex-Bench v3、IHBench、Omni-DeepSearch 等按真实状态写 `REMOTE_ONLY/MISSING/UNVERIFIED`。

### P1-R5：增加 reward-guided 正交分类

在不改动 Stage-1B 方法内容的前提下，为 23 direct rows 生成 `control_basis` 派生表，防止 system orchestration 被当成 reward-guided control。

验收：每条都能回答：

1. 什么信号进入 controller；
2. 是否有 evaluator/reward；
3. 该信号是否改变下一动作；
4. 是否存在 label-optimized controller/config；
5. core 或外部组件是否更新权重。

### P1-R6：重写 Stage-1C common-rubric 的可行性输入

三个非 H5 bundles 都必须使用同一组字段：

```text
scientific importance
system-first relevance
nearest direct prior
strongest inspected-set contradiction
single-observation kill
reward/evaluator observability
exact local dataset status
exact local code status
Stage-2A reproduction path
known unavailability/private blockers
```

完成 P0 后可立即窄复审；无需再跑 20,727-work D0、T1 broad scan 或模型实验。

## 6. 给研究团队 AI 的严格执行指令

```text
DO NOT modify any registered reviewer request or prior review.
DO NOT treat the invalid 40-character SHA as a harmless short-hash alias.
DO NOT call the 81-work set complete outside its four declared sources.
DO NOT call a row FULLTEXT_ROUTED without local PDF bytes and a matching hash.
DO NOT equate DIRECT_CONTROL_METHOD with reward-guided training-free RL.
DO NOT equate voicebench with VoiceAgentBench.
DO NOT equate tau2-bench with tau-Voice.
DO NOT describe docs/datasets.lock.json as the current exact disk snapshot.
DO NOT download every possible benchmark merely to make counts look complete.
DO NOT run a model, metric, smoke, reproduction, or prototype.
DO NOT rank or select the three non-H5 bundles before the P0 reconciliation.

DO issue a dated correction with one resolvable full release SHA.
DO repair or downgrade the seven false FULLTEXT labels.
DO reconcile the bounded known-prior set listed in this report.
DO separate orchestration, evaluator-gated control, reward-guided selection, and trained boundaries.
DO publish an honest baseline/candidate/auxiliary asset inventory.
DO give each Stage-1C candidate an exact paper/code/data availability state.
DO request one narrow independent re-review after P0-R1 through P0-R4 pass.
```

## 7. 可复审后的预期裁决

若 P0-R1 至 P0-R4 完成，H5 继续 withheld，且 targeted reconciliation 没有推翻三个非 H5 bundles 的资格，下一轮应预期：

```text
STAGE_1B_DISCOVERY_FLOW          = PASS
STAGE_1B_MAPPING_CLOSE           = PASS
STAGE_1B_RECORD_RELEASE          = PASS
STAGE_1C_FORMAL_PROBLEM_COMPARE = SIGN
MODEL_OR_REPRODUCTION_EXECUTION  = WITHHOLD
NOVELTY_VERDICT                  = DEFER_TO_REPRODUCTION_FIRST_STAGE_2
```

当前真正缺的不是更多论文数量，而是把**已经知道的关键先行工作、证据深度和实盘资产状态**对齐到同一个可签署对象。这个修复范围有限，但在完成前直接进入 Stage-1C，会让“本地可行性”和“nearest prior proximity”两项评分从一开始就失真。
