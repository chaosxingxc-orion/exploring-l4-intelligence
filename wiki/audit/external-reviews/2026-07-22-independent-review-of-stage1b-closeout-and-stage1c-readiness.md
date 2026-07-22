# 2026-07-22 Stage-1B 收口与 Stage-1C 准入独立审查报告

> 审查身份：严格外部审稿人 / 博士生导师视角  
> 审查日期：2026-07-22  
> 审查对象：当前研究目标、有效 survey 协议与状态、Stage-1B frozen-D0 closeout、论文注册表视图、post-Stage-1B refinement，以及复现环境/知识库交接计划  
> 审查边界：本报告只审查阶段、survey 科学闭环、引用与遗漏风险、研究范围和 Stage-1C 准入；不要求元数据篡改防御、恶意输入鲁棒性，也不授权模型调用、数据集指标实验、smoke、复现或原型  
> 写入纪律：本报告是独立审查件；未改动研究团队任何现有源文件或交付物

## 0. 一页结论

```text
CURRENT_STAGE                         = STAGE_1B_LATE_EXECUTION_AND_CLOSEOUT
STAGE_1A_GATE                         = PASSED_AND_SUPERSEDED_BY_STAGE_1B_EXECUTION
FROZEN_D0_ARXIV_IDENTITY_EXHAUSTION   = PASS
FULL_SYSTEMATIC_MAPPING_CLOSEOUT      = INCOMPLETE
CITATION_IDENTITY_AND_ROLE_ROUTING    = GENERALLY_ADEQUATE
SPECIFIC_NEW_P0_OMISSION_FOUND        = NO_IN_BOUNDED_EXTERNAL_CROSS_CHECK
T1_VENUE_ROUTE_COVERAGE               = INCOMPLETE
DELTA_RECALL_REMAINDER                = INCOMPLETE
H5_LOAD_BEARING_USE                   = WITHHOLD
STAGE_1C_ELIGIBLE_INPUT_PACKAGE       = NOT_YET_DELIVERED
STAGE_1C_FORMAL_START                 = WITHHOLD
STAGE_1C_PREPARATORY_FORMATTING       = ALLOW
MODEL_SMOKE_OR_REPRODUCTION           = PROHIBITED_AT_CURRENT_GATE
ACADEMIC_FRAUD_EVIDENCE               = NOT_ESTABLISHED
RESEARCH_GOVERNANCE_RISK              = HIGH_UNTIL_RECORD_AND_SYNTHESIS_CLOSE
```

总评：团队已经完成了一个规模可观、边界声明相对克制的 frozen-D0 发现与摘要筛选工程，不能再把它视为 Stage-1A，也不应继续无限扩张 arXiv 广搜。然而，“20,727/20,727 D0 identity 已处理”只证明一个冻结检索池的发现闭合，不等于 Stage-1B 系统映射闭合，更不等于可以直接进入复现。当前仍缺四个承重条件：T1 路由与增量召回余项闭合、协议规定的最终映射表、可供 Stage-1C 使用的正反证据输入包、以及可引用的冻结发布快照。H5 还不能进入 gap 论证。

因此，本轮结论不是要求团队继续大规模搜索，而是要求进行一次**短、硬、不可绕过的 Stage-1B 收口**。四项收口完成并独立签字后，应立即进入 Stage-1C；此前不得执行已经拟议的模型 smoke 或冻结复现对象。

## 1. 本次审查所冻结的证据快照

由于当前 Stage-1B 交付物主要处于未提交 working tree，本报告不能用 Git blob 宣称其为已发布证据。为使本次意见至少可回指，本报告按审查时可见字节记录如下：

| 文件 | 字节数 | SHA-256 |
|---|---:|---|
| `wiki/Research-Objective.md` | 5,064 | `44e99edf7daf125159b5a89e9807eee6b6683480c5600a6a83c18a86695b98d9` |
| `wiki/Project-Thesis.md` | 6,524 | `5aafddb9d32d085462f619e739cb3d1f8b47740d39d88b0cfc6b38f99e7f9623` |
| `wiki/survey/current/status.md` | 4,056 | `7e90a58b9d9cc6efa7af2656226028ae45ad2e00624cbfac6037d2ef50e9c905` |
| `wiki/survey/current/protocol.md` | 63,244 | `16d04d0b83cf4bf667e6418b5e3edd1a42c51809358c66696a009ffa5f002bda` |
| `wiki/survey/workbench/system-first-stage1b/2026-07-22-final-exhaustive-research-closeout.md` | 8,320 | `1b64b8bb1ed50c1880e0ce081e328a6e6d54476af425e68169f884d4b365e9f3` |
| `wiki/survey/registry/views/stage1b-bounded-exhaustive-2026-07-22.json` | 144,993 | `8e3fcc5348afc4ff3425afac0da5fc6abb11aa33306fa74943c4d82ed4ed9e59` |
| `wiki/survey/workbench/system-first-post-stage1b-refinement/2026-07-22-local-fulltext-secondary-filter-v4.md` | 5,685 | `e63c3d066d5f54832ca0d15b58ccd2a6c4a45f31dd912bc7619282d1ad342987` |
| `docs/superpowers/plans/2026-07-22-stage1b-to-reproduction-environment-and-knowledge-base.md` | 5,206 | `6c6d1a6f57f9b2855f9292765319b311605c3650d8a4033ca24a8dec915d220e` |

审查时 umbrella `HEAD` 为 `c01fba751b56588ed2f62cb6d01f6c25f3e95539`。上述 current 文件为 modified，Stage-1B workbench、registry view、post-stage1b refinement 和交接计划为 untracked。换言之，当前材料可以作为工作证据被审查，但尚不能作为不可变、可复核的正式 Stage-1B release 被引用。

这不是形式主义问题。若研究团队在 Stage-1C 选题后再反向修改 Stage-1B 编码或 roster，外部观察者将无法区分“合理纠错”与“为选定课题回填证据”。先冻结证据，再作选题，是防止选择性报告的必要因果顺序。

## 2. 当前究竟处于哪个阶段

### 2.1 不是 Stage-1A

Stage-1A 已完成 search-design 的身份、路由和协议准入，独立复审对 `c01fba7` 给出 `SIGN`，owner 随后授权 Stage-1B 执行。团队已经实际执行 65 条冻结 arXiv 查询、形成 20,727-ID D0、完成 20,727/20,727 摘要级处理、取得 319 篇全文并形成 226 篇保留 roster。仅从暴露事实看，Stage-1B 已经实质启动且接近末段。

### 2.2 也还不是 Stage-1C

项目自己的有效协议明确规定：

- Stage-1B 负责 method-path 事实、占位、接近度、负证据和复现准备度映射；
- Stage-1B 不创建或排序最终 3–5 张 candidate cards，也不冻结 reproduction list；
- Stage-1C 才负责候选 problem/gap-hypothesis cards、排序、owner 选题与 reproduction-list freeze；
- Stage-2A 才以复现为第一步收敛技术方案。

当前仅完成了 discovery/screening 主干及局部全文二次过滤，尚未交付 Stage-1B 规定的完整 synthesis。因此准确阶段应写作：

> **Stage-1B late execution and closeout：发现池已闭合，系统映射与发布闭环尚未闭合。**

### 2.3 必须停止混用的三个“闭合”

| 闭合层级 | 当前状态 | 能证明什么 | 不能证明什么 |
|---|---|---|---|
| frozen-D0 identity exhaustion | PASS | 冻结的 20,727 个 arXiv ID 均有摘要级处置记录 | 不能证明 venue、引用链或新论文宇宙闭合 |
| full-text/registry processing | PARTIAL PASS | 319 篇全文、226 篇 roster 已形成；局部有页级证据 | 不能替代跨 method-path 的最终 occupancy、kill 和 sensitivity synthesis |
| Stage-1B scientific/release closeout | FAIL/INCOMPLETE | 尚无可放行证明 | 不能据此开始 Stage-1C 正式选题，更不能直接进入 Stage-2A 复现 |

`final-exhaustive-research-closeout` 的正文确实限定为“frozen D0 only”，这是正确的；但文件标题中的 `final exhaustive`、状态页中的 next action、以及下游已冻结的复现卡组合起来，会给读者造成 Stage-1B 全部结束的错误印象。建议以后使用 `frozen-D0-exhaustion-closeout`，避免把检索池闭合命名成研究阶段闭合。

## 3. 对现有交付物的严格评价

### 3.1 做得正确且应保留的部分

1. **分母意识明显改善。** 团队清楚区分 20,602 个系统轮次 D0 ID、125 个 D0 内 targeted/registry ID，以及 99 个 D0 外定向 ID，没有用 D0 外论文虚增 20,727 的完成度。
2. **“未发现”的适用域较克制。** closeout 明确只声称 frozen D0 exhaustion，没有声称 literature universe closure 或“业内不存在”。
3. **论文角色分层基本合理。** core、instrument、transfer、negative/boundary 分开，训练过的 reward/evaluator instrument 没有被悄悄计入 frozen-system method denominator。
4. **本地全文优先是正确的。** 451 份本地 PDF 的二次过滤、页级定位、模型内部访问与训练依赖排除，优于只依赖标题/摘要作技术接近度判断。
5. **负证据得到保留。** 126 条 negative/boundary 和 43 条 instrument 没有被当成“无用论文”删除，这对于后续构造 kill criterion 与反例非常重要。
6. **没有越权执行模型。** 当前记录仍为 research model/smoke = 0、dataset metric/prototype = 0。知识库和 no-model 环境准备本身不构成实验越界。

这些优点足以说明团队并非“什么都没做完”。问题在于，它们是高质量的原料和过程证据，还不是协议约定的最终科学产品。

### 3.2 P0：把 D0 耗尽当成 systematic mapping 完成，逻辑不成立

协议 §8 要求 Stage-1B 顺序包含：执行冻结查询、扫描已注册 T1 routes、REC-0/BFS/DFS/citation closure、全文与 sidecar、独立协调/裁决，最后才派生表格和发布。

当前状态页却同时承认：

- delta recall 只尝试了 4/65，因 SSL EOF/429/503 与超时中断；
- 50 条 T1 routes 在 REC-7 深度仍未执行；
- H5 coder B 与第三方裁决未完成；
- record-layer construction PASS，但 release 仍 BLOCKED。

所以 `D0 remaining = 0` 只能支持“冻结 arXiv 集合内无未处理 identity”，不能支持“检索策略的所有预注册召回路径完成”。这是本轮最核心的结构性漏洞。

### 3.3 P0：协议要求的 Stage-1B 最终输出并不存在

有效协议 §9 明确要求至少交付：

- coverage/kill matrix；
- system-control occupancy 与 sensitivity tables；
- SOTA/method cards；
- updated census/ledger 与 saturation/flow report；
- direct-prior proximity 与 reproduction-readiness evidence；
- eligible Stage-1C inputs。

而每个 eligible Stage-1C input 必须同时具有：

- supporting evidence；
- contradicting evidence；
- single-observation kill criterion；
- unresolved alternatives；
- method limitations；
- improvement space 与 research value。

本次检查中，`wiki/survey/current/tables/` 只有 `opening-guarantees.md`。226-record registry view 是重要底座，但其主视图仍以 instrument、speech task match、negative falsifier、open transfer 等浅层路由数组为主，不能替代上述 claim-level 合成。post-Stage-1B refinement 自己也承认，contradicting evidence、kill criteria、data replacement feasibility 和 reproduction scope 尚待补足；但它随后提出由这一步直接产生 3–5 张 Stage-1C cards，也出现了轻微的职责越界。正确产物应是未排序的 eligible inputs，最终 3–5 张 cards 必须留给 Stage-1C。

因此：**团队有 roster，没有完成 map；有候选论文，没有完成 gap-eligible evidence bundle。**

### 3.4 P0：Stage-1B 证据仍主要未提交，正式准入无法追溯

当前正式 HEAD 仍是 Stage-1A search-design 签字所绑定的 `c01fba7`，但 Stage-1B 的主要结果位于 modified/untracked working tree。若现在开始 Stage-1C，将出现严重的时间顺序歧义：究竟是先看见证据再选题，还是选题后仍可调整证据集合？

这不等于存在造假，但它制造了事后选择和回填的条件。Stage-1C 之前必须形成一个 commit/manifest-bound、hash-frozen 的 Stage-1B release，且 reviewer 能从该快照重建 roster、关键表和缺失项。

### 3.5 P1：H5 不能一边作为北极星核心维度，一边在选题时被默默绕过

团队已正确标注 `H5_LOAD_BEARING_USE=WITHHOLD`。问题不是 H5 阻止所有非 H5 mapping，而是：如果 Stage-1C 的 gap card 涉及 black-box frozen access、外设控制、内部状态依赖或训练自由边界，H5 很可能直接改变某些论文能否进入核心分母。

准入时只能二选一：

1. 完成独立 coder B、agreement 和第三方 disagreement adjudication，使 H5 可承重；或
2. 明确把所有 H5 相关结论排除在本轮 Stage-1C 候选空间之外，并在每张输入包上标注该缺口。

由于项目北极星本身以 frozen/black-box 外设优化为核心，本审查建议采用第一条。第二条虽然形式上可行，但会把最关键的研究边界排除，导致 Stage-1C 选题失真。

### 3.6 P1：局部 refinement 很有价值，但命名和状态路由容易造成“分析后移”

`post-stage1b-refinement` 实际上仍在做 Stage-1B 必需的全文分类、直接候选纠错与接近度证据整理。只要 Stage-1B 的 eligible inputs 尚未形成，这些工作就不是“Stage-1B 之后”的附加优化，而是 Stage-1B 收口的一部分。

建议在正式 closeout 中吸收其承重结论，不要让 Stage-1C 被迫引用一个名义上 post-stage、实际上尚未发布的 mutable workbench。

## 4. 引用是否合理

### 4.1 总体结论

引用身份、稳定链接和大类角色路由总体达到 Stage-1B 的工作标准；对“论文讲了什么”的若干关键表述与官方摘要一致。但是，**引用数量充足不等于引用结构已经支持 gap claim**。当前主要缺口不是 bibliography identity，而是从 paper-level facts 到 claim-level support/contradiction/kill 的可审计聚合。

### 4.2 几个承重近邻的外部抽查

- [AudioToolAgent](https://arxiv.org/abs/2510.02995) 确实使用中央 LLM 协调多个音频语言模型工具、处理冲突，并报告 MMAU/MMAR/MMAU-Pro 结果；将其置于 direct/reproduction-readiness 队列是合理的。
- [EChO-Agent](https://arxiv.org/abs/2606.15141) 的官方摘要明确给出 planning、tool execution、evidence integration、answer verification 流程，并在 MMAR 上评估；它应被视为音频证据链编排的重要直接近邻，而不只是泛化 agent 引用。
- [AOP-Agent](https://arxiv.org/abs/2605.28192) 明确在无需额外训练的条件下使用 hierarchical omni-modal memory 与 observe-reflect-replan loop；它对“omni active perception + external control”构成高接近度证据，但任务对象为长视频音视多跳推理，不能直接外推到所有 speech agentic tasks。
- [Omni-Decision](https://arxiv.org/abs/2607.11433) 明确是 training-free evidence-state system，覆盖 acquisition、validation、repair 和 stopping；它是 system-control/evidence-state 维度的重要开放近邻。其 OmniGAIA/WorldSense 结果不能直接证明 speech/omni 语音任务上的效果。
- [$\tau$-Voice](https://arxiv.org/abs/2603.13686) 是 full-duplex grounded voice-agent benchmark，覆盖 278 个任务并区分任务完成与交互质量；将其作为 evaluation instrument 而不是 frozen control mechanism 是正确的。

这些抽查支持团队的主要角色判断，同时也说明 Stage-1C 必须按“系统控制路径 × 任务/模态 × 冻结访问契约”做 cellwise 比较，不能用“都是 agent”或“都是 training-free”合并成一个宽泛创新叙事。

### 4.3 当前引用仍需修正的方式

1. 每一项性能数字必须回到 PDF 页码、表格或图号；abstract/网页链接只能证明身份和摘要级主张。
2. 对 `state of the art`、`consistent improvement`、`dominant`、`ceiling` 等词必须绑定论文自己的模型、split、metric 和对照条件。
3. `repo exists`、`code will be available`、`open source`、`locally reproducible` 是四个不同命题，不能互相代替。
4. 相同论文可能同时提供 method、instrument 和 boundary facets，但 occupancy 的分析单位必须是 method path，不能通过多角色重复计数。
5. 任何 “no direct match” 结论都必须同时披露 D0、D0 外 targeted、T1 未执行、delta 未完成、不可获得全文与 H5 withheld 的数量。

## 5. 是否遗漏了相关论文

### 5.1 可以给出的严格答案

本次基于现有论文全集优先、再用官方 arXiv 页面作定向外部抽查，**没有发现一个可被证实为团队完全遗漏的、显然应进入 P0 direct-prior 的新论文身份**。外部抽查触及的 AudioToolAgent、EChO-Agent、AOP-Agent、Omni-Decision、$\tau$-Voice 等均已在团队语料或当前路由中出现。

但不能因此写“没有遗漏”。当前最多可以写：

> 在审查时已冻结的 D0、已注册 targeted/registry 文献与已检查的外部关键身份中，未发现新的明确 P0 identity omission；T1 venue routes 与 delta recall 尚未闭合，因此跨 venue 和增量召回遗漏风险仍未消除。

### 5.2 当前真正需要补的不是再来一轮无边界大搜

应优先补齐以下结构性召回路径：

1. 执行协议内已注册但未执行的 50 条 T1 routes；
2. 对 65 条 delta 中未完成的 61 条作一次有界重试，或逐条记录不可执行原因、时间窗和影响评估；
3. 对 direct/core 候选做 backward/forward citation closure，尤其检查其引用与被引中的非 arXiv venue 版本；
4. 对同一 work 的 arXiv、conference、journal、project page 与 repository 做 work-level 合并，避免“venue 版本缺失”被误判为“论文遗漏”；
5. 之后停止广搜。新增论文只按 date-bounded delta 或由 Stage-1C 候选卡触发的定向补证进入。

这是一项收尾工作，不是新的大规模 survey campaign。

## 6. 是否存在超越当前阶段的探索

### 6.1 尚未发生的越界

没有证据显示团队已经运行 research model、dataset metric、smoke、headroom test、复现或 prototype。构建元数据知识库、固定环境身份、检查本地模型/数据是否存在、做 no-model 配置 dry gate，均可作为 Stage-1B 到 Stage-1C 的基础设施准备。

### 6.2 已经发生的计划层越界

交接计划 Phase 4 明确要求 `choose reproduction slices`，并称第一张 comparator-first ASR reproduction card 已 `frozen`。这与当前协议直接冲突：Stage-1B 不冻结 reproduction list，Stage-1C 在候选 gap 排序和 owner 选题之后才冻结它。

状态页又把下一步写成在获得新授权后比较 Audio-Mind、AudioToolAgent 与 no-tool，并 smoke Agent-Omni/AURA/Agentic-ASR。这不是 Stage-1B 的下一个科学动作，而是 Stage-2A 的候选动作。即便另行取得“模型调用授权”，也不能用执行授权替代阶段准入；权限充分不代表科学顺序正确。

应作如下状态修正，而不是删除既有计划：

- 已有 reproduction priority 只能标记为 `PROVISIONAL_INPUT / NOT_STAGE_FROZEN`；
- 当前 next action 改为 Stage-1B 收口与 Stage-1C eligible-input synthesis；
- Stage-1C 完成 owner problem selection 后，再决定哪些论文构成最近邻复现集；
- Stage-2A 才执行第一项 reproduction，且先复现最近邻，再引入新机制。

## 7. 学术诚信与造假风险评估

### 7.1 本轮没有足够证据指控学术欺诈

未发现伪造论文身份、捏造实验结果、篡改模型指标、虚构独立 coder、抄袭或把 model run 冒充为未运行。相反，团队主动披露了 50 条 T1 未执行、delta 4/65、H5 withheld、release blocked、model/smoke = 0，以及 D0-only 的适用域。这些披露与蓄意隐瞒并不一致。

因此，严谨结论必须是：**没有建立 fabrication、falsification 或 plagiarism 的证据。** 不能因为阶段管理混乱就直接指控造假。

### 7.2 但当前状态具有高选择性报告风险

以下行为若不纠正，会在未来形成与学术不端难以区分的记录条件：

- 在 T1 和 delta 未闭合时使用 `final/exhaustive` 形成过强的外部印象；
- 在缺少 occupancy/kill/contradiction synthesis 时直接挑选复现对象；
- Stage-1B 主要证据保持未提交状态，让选题后改写原始编码成为可能；
- H5 未完成却让涉及 black-box/frozen 边界的 gap claim 承重；
- 把 “repository URL 可达” 写成 “可复现”，或把论文报告值写成团队复算值。

这些目前是**治理缺陷和可疑实践风险**，不是已证实欺诈。最有效的防线不是继续增加对抗性脚本，而是严格执行“证据冻结先于选题、反证与 kill criterion 先于 gap claim、复现先于新方案”的顺序。

## 8. Stage-1C 的最小放行条件

以下四项是 Stage-1C 正式启动前的 P0 gate。它们应在现有论文集内完成，不再扩张 frozen D0，也不运行模型。

### Gate C1：冻结可引用的 Stage-1B release

必须交付：

- 一个 commit-bound release manifest，绑定 protocol、query/T1 route inventory、D0、handled ledger、226-record roster、全文 sidecars、mapping outputs、H5 状态与 unresolved counts；
- 每项生成物的 raw hash 与 producer/version；
- working-tree 与 release bytes 一致的证明；
- 明确声明 correction 只能通过 dated supersession 进入。

通过标准：独立审查者可以从一个固定 commit 定位本轮所有承重输入，不依赖未跟踪 workbench。

### Gate C2：关闭召回余项，而非继续大搜

必须交付：

- 50/50 T1 route dispositions；
- delta 65/65 的执行结果，或对未执行项给出逐项 `WAIVED_UNAVAILABLE`、重试证据、时间窗和影响分析；
- direct/core 的 citation-closure ledger；
- 一个范围严格的 recall limitation statement。

通过标准：不得再把未执行写成 zero hit；允许存在有证据的不可执行项，但不能无声消失。

### Gate C3：交付协议规定的映射产物

必须交付：

- coverage/kill matrix；
- system-control method-path occupancy table；
- 按 task/modality/access contract 分层的 sensitivity table；
- instruments、negative priors 与 boundary/comparator 分表；
- saturation/flow 与 direct-prior proximity/repro-readiness 表；
- 每张表完整给出 population、work/path denominator、缺失、不可获得和冲突数量。

通过标准：所有 headline 数字都能回到 registry/sidecar；同一 work 的多 facets 不造成方法分母重复计数。

### Gate C4：形成 Stage-1C eligible inputs，并完成 H5 决策

Stage-1B 应提交一个覆盖所有仍具合理可能性的、**未排序的 eligible-input 集合**，但不得在此阶段压缩成最终 3–5 张卡、排序或选定课题。每个输入包至少包括：

1. 明确定义的 problem/gap hypothesis；
2. system-level direct evidence；
3. component/transfer evidence；
4. strongest contradicting evidence；
5. 单个可观察结果即可推翻该 gap 的 kill criterion；
6. 未排除的替代理由；
7. 适用 task/modality/access contract；
8. 可替代数据、最近邻复现对象与可测 evaluator；
9. 预期研究价值与“不做”的理由；
10. H5 可承重状态。

H5 需完成独立 coder B 与裁决；若团队坚持暂不完成，则所有依赖 H5 的输入包必须标记 `INELIGIBLE_FOR_STAGE_1C_SELECTION`。

### 独立准入签字

四项全部满足后，由独立 reviewer 对固定 commit 给出：

```text
STAGE_1B_DISCOVERY_CLOSE              = PASS
STAGE_1B_MAPPING_CLOSE                = PASS
STAGE_1B_RECORD_RELEASE               = PASS
STAGE_1C_ELIGIBLE_INPUTS              = PASS
STAGE_1C_FORMAL_START                 = SIGN
MODEL_OR_REPRODUCTION_EXECUTION       = STILL_WITHHOLD
```

Stage-1C 启动签字仍不等于 Stage-2A 模型执行授权。

## 9. 可供 Stage-1C 组织、但本轮不得提前排序的探索轴

下面不是预选结论，只是把现有论文集组织成可审查的 gap-input families，防止团队在 Stage-1C 只围绕某一篇喜欢的论文做事后叙事：

1. **Evidence-state control：** frozen omni/speech 系统是否缺少可检查的证据状态、冲突、依赖、repair 和 stopping 的统一外部控制面？主要反证来自 Omni-Decision、EChO-Agent、AOP-Agent。
2. **Tool/agent arbitration：** black-box 多模型、多工具或多模态专家之间的 routing、conflict resolution 与 credit/evaluator 是否仍缺统一任务合同？主要反证来自 AudioToolAgent、VISA 与已有 mixture/router priors。
3. **Budget/stop/repair policy：** 在没有梯度、隐藏状态和可靠 logprob 时，外部系统能否用 reward/evaluator 信号决定继续、停止、重试、换工具或回滚？必须把已有 budget forcing、VAD stop policy、test-time search 和 negative results 纳入反证。
4. **Evaluator/reward reliability：** 跨 speech/audio/omni 任务的外部 reward 是否具备可校准性、抗分布漂移性和与任务成功的一致性？需要 instruments 与 negative priors，而不能把 evaluator 本身误当成 control innovation。
5. **Interactive/full-duplex system objective：** 静态 QA 上的 inference-time control 是否能转移到 full-duplex、policy-grounded、environment-interacting voice agent？$\tau$-Voice、VoiceAgentBench、EVA-Bench 等首先是测量与问题界定证据，不是方法成功证据。

Stage-1C 应用统一量表比较这些轴：directness、contradictory coverage、falsifiability、local data/model feasibility、nearest-prior reproducibility、system-first value。只有 owner 在看到完整正反证据后才能选题。

## 10. 给研究团队 AI 的强制执行指令

```text
DO NOT broaden frozen-D0 arXiv scanning.
DO NOT run a research model, smoke, dataset metric, reproduction, or prototype.
DO NOT call the current working-tree package a released Stage-1B closeout.
DO NOT use H5 in occupancy, headline, gap, or Stage-1C selection before coder-B/adjudication.
DO NOT freeze or rank the reproduction list in Stage-1B.
DO NOT convert repository availability into a reproducibility claim.

DO execute or explicitly waive all 50 registered T1 routes.
DO close or scope all 65 delta rows; 4/65 is not completion.
DO generate the required coverage/kill, occupancy, sensitivity, flow, proximity, and readiness tables.
DO create an unranked Stage-1C eligible-input set with support, contradiction, kill criteria,
   unresolved alternatives, limitations, feasibility, and value.
DO freeze the exact Stage-1B evidence package in a commit-bound manifest before Stage-1C selection.
DO request one independent stage-transition review against those fixed bytes.
```

## 11. 最终裁定

### 对 Stage-1B 工作质量

`MAJOR REMEDIATION, BOUNDED CLOSEOUT ONLY`。

团队已经完成足以停止大规模广搜的 corpus work；继续堆论文的边际价值低于把已有论文集组织成可证伪的 method-path map。当前最需要的不是更多代码健壮性，也不是更多 PDF，而是把已有 226-record roster 和 451-PDF 本地池转化为协议要求的科学结构。

### 对 Stage-1C

`FORMAL START = WITHHOLD`。

理由不是 Stage-1B 研究量不足，而是 Stage-1B 的召回余项、claim-level synthesis、H5 承重边界和不可变发布证据尚未同时闭合。允许团队立即准备 Stage-1C 表格模板和输入包框架；不允许排序候选问题、owner 正式选题或冻结复现列表。

一旦 Gate C1–C4 完成并对固定 commit 独立签字，结论应快速转为 `SIGN`，无需再开新一轮无边界 survey。随后 Stage-1C 只做问题选择和复现列表冻结；模型/数据实验继续留给 Stage-2A。
