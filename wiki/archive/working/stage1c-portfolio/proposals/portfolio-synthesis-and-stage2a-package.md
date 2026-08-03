---
artifact_id: "SF-CAPABILITY-PROPOSALS-PORTFOLIO-REVIEW-V1"
role: "portfolio synthesis and next-step recommendation"
authority: "workbench draft; owner review pending"
execution_authority: "STAGE2A_WITHHELD"
---

# Portfolio 评审摘要与 Stage-2A 建议

## 1. 总判断

九条方向中，最短且能直接检验项目北极星的研究闭环是：

> 在同一 frozen speech/omni API core 上，R5 用 evidence state 保留 direct incumbent，R6 用 black-box
> reward 决定是否执行 branch/repair/stop，R8 只在 condition-aware margin 足够时接受 revised answer；检验其
> 是否在 MMAU/MMAR 上超过 strong structured prompt、best fixed action 和 terminal-only rerank。

这一闭环同时满足五条统一约束：不改模型；目标是可靠能力提升；提升来自系统级 in-context state/action；
Lean 只审计不变量和条件蕴含；安全/abstain/hacking 只作 guard/stress，不替代主能力结果。

## 2. 方向优先级矩阵

| 方向 | 科学价值 | 当前语音证据 | 实验就绪度 | 首轮主要风险 | 决策 |
|---|---|---|---|---|---|
| R5 evidence-state architecture | 高：定义研究对象和作答权 | 较强，且有 wrapper 回归反例 | 高 | structured prompt 已足够 | Stage-2A 核心 |
| R6 within-instance control | 高：区分 TFRL 与 terminal rerank | 中等，speech 多为退化/手工形态 | 中高 | reward 不具 action fidelity | Stage-2A 核心 |
| R8 reliable control | 高：把平均增益变为可部署结论 | 强 evaluator/failure 证据 | 中高 | coverage 塌缩或误差界不稳 | Stage-2A 核心 |
| R1 multi-source context ceiling/construction | 高：分解 demo 与 query view 的条件化能力 | vanilla SICL、demo retrieval、query transform 各自证据强，联合问题未闭合 | 中；split fence 待审计 | 重复已有 ICL/检索或 demo pool 泄漏 | Stage-2B 首扩展 |
| R4 skill lifecycle | 高：固定工具库中的信用与组合 | 强选择/工具证据 | 中 | 输出验证可能比选择更重要 | Stage-2B 并行扩展 |
| R3 acoustic-keyed memory | 中高：speech-native 条件状态 | 直接跨实例证据薄 | 中低 | key 无判别力、污染/泄漏 | Stage-2C |
| R7 cross-instance evolution | 高但依赖强 | 直接 speech occupancy 不足 | 低至中 | retrospective illusion/漂移 | R3/R6 成立后 |
| R2 external knowledge | 任务条件性高 | 有 AudioRAG/DeepSearch carrier | 中 | waveform-sufficient 任务无意义 | 只在需外部事实时 |
| R9 integration | 高但不是首实验 | 多系统近邻 | 依赖前八项 | 组件相消、成本掩盖 | 最后集成 |

## 3. 建议的研究论文/里程碑打包

### Milestone A — Reliable black-box context control

绑定 R5+R6+R8。最小贡献问题：`step-wise reward control` 是否在 incumbent-preserving evidence-state 中
超过 strong fixed/terminal-only baselines，并对声学条件保持正 LCB。无此结果，不扩系统。

### Milestone B — Expanding the useful action space

绑定 R1+R4。R1 先独立测量 demonstration + query-view 菜单内经验上界、交互和 selection opportunity，
只有异质性成立后才测试训练自由 constructor；R4 再增加 executable skill 并做信用归因。R1 不以成本作为
研究目标，R4/系统集成仍遵守共享成本合同。

### Milestone C — Persistent system evolution

绑定 R3+R7。先证明 acoustic key 预测 contribution，再开放跨实例 update；只接受 time-ordered future
utility，不接受 shuffled retrospective best。

### Milestone D — Knowledge extension and integration

R2 只用于 external-fact-required carrier；R9 对已存活组件做 factorial integration 与 speech-native 外部验证。

## 4. Stage-2A 待冻结执行合同

### 4.1 Objective

实现并评估 `incumbent-preserving reward-guided context controller`，动作限制为：

```text
keep incumbent
structured re-prompt
same-observation resample
one cross-observation branch
one bounded repair
stop
```

### 4.2 Core 与 data

- 建议 core：Qwen2.5-Omni-7B，经冻结 inference API；exact repository/revision/weight hash、serving stack、
  generation config 与 system prompt = `TBD_AT_AUTHORIZATION`。
- 数据：MMAU Test-mini + MMAR；先解析 T2 的 `metadata_only` 与任何本地 pin 叙述冲突，再冻结 dataset
  revision、split、file hash、license、contamination/exposure。
- 不在 Stage-2A 接入 live retrieval、persistent memory、动态 skill induction 或 full-duplex。

### 4.3 Runtime reward

依次采用：deterministic option/format checks；counts-only consensus；hypothesis-vs-hypothesis semantic
equivalence；可选 frozen cross-family judge 的 pairwise margin。Test gold 与 gold CoT 由 mechanical fence 隔离。
Judge 只有在校准/重复性/位置偏置/SelfGap 检查通过后才能掌舵。

### 4.4 Baselines

`direct`、`strong structured prompt`、`random matched-cost`、`same-observation majority/MBR`、`best fixed
action`、`full fixed chain`、`terminal-only rerank`、`step-wise controller`、`offline executed-pool oracle`。

### 4.5 统计与门槛

授权包必须填入：

- Primary task utility 与预注册 SESOI；
- paired CI/LCB 方法、seeds/replicates 和 multiple-comparison rule；
- correct→wrong、worst-group、coverage 与 cost tolerance；
- action/core/judge hard budgets；
- condition buckets 与最小样本量；
- reward calibration split 与 test gold fence；
- stop/rollback threshold；
- 数据、core、prompt、代码和环境 hashes。

### 4.6 Lean/conformance gate

在研究运行前至少编译并测试：state/action types、bounded termination、incumbent recoverability、gold
boundary、provenance preservation、`2ε` margin theorem，以及 executable trace 到 Lean operator 的正/负例
映射。若 conformance 未关闭，只允许说“formal model 已编译”，不能说实际实现被证明可靠或收敛。

## 5. Stage-2A 成功、失败与重路由

### Success

Step-wise controller 相对 direct、structured prompt、best fixed 和 terminal-only 均达到预注册 SESOI/LCB，
且 correct→wrong、worst-group、coverage 与成本不越界。随后才授权 R1/R4 扩 action space。

### Partial

- Candidate oracle 有 headroom、controller 无 recovery：优先修 reward/R8，不扩 action。
- Structured prompt 有增益、adaptive 无额外值：保留固定 prompt，关闭 R6 动态主张。
- 平均正但 condition 尾部负：先做 R8 condition gate，再决定是否扩展。
- 只有某类 demonstration/query-view context 有效：转 R1 机制研究；不把总收益归给 R6。

### Abort

需要模型内部量；gold 进入环；数据/许可/version/hash 不闭合；同成本不超过强固定基线；可靠阈值覆盖率
近零；效应低于 SESOI；收益由未匹配调用量解释。Abort 不等于否定 system-level ICL，只否定当前合同。

## 6. Owner review 决策点

若接受本 portfolio，下一次 owner 决策只需回答：

1. 是否将 `R5+R6+R8` 定为唯一 Stage-2A vertical slice；
2. 是否允许进入**合同冻结与资产核验**，而不是直接运行；
3. exact core service 与 MMAU/MMAR 资产冲突解决后，是否签发
   `AUTHORIZE_STAGE2A_CAPABILITY_CONTROL_VERTICAL_SLICE`。

本文件本身不签发该授权。
