---
proposal_id: "R8"
title: "条件自适应的可靠能力控制"
dimension: "D5 cross-cutting reliability"
status: "workbench proposal; owner review pending; Stage-2A vertical-slice component"
execution_authority: "WITHHELD"
---

# R8 — 条件自适应的可靠能力控制

## Proposal 摘要

本研究让 R1-R7 的能力增益在 acoustic condition、task 和 core/service version 变化时保持可重复、低尾部
回归和可诊断。Controller 根据 reward error、agreement、margin、cost 与 condition 决定是否替换 incumbent、
是否继续预算以及调用哪个 action family。Reliability 的目标是**可靠实现能力提升**，不是把系统改写成
低 coverage 的 abstention engine。

Headroom、reward admissibility、hacking、rollback 和 abstention 在此作为诊断/门禁。主结果仍是 task
utility 的 lower confidence bound、worst-group 与净翻转。

## 1. 研究问题与假设

- `H1 condition calibration`：condition-specific reward error/margin 比 global threshold 更能预测真实非回归。
- `H2 useful guard`：incumbent gate 降低 correct→wrong 和 worst-group loss，同时保留足够 coverage 与净能力增益。
- `H3 robustness`：在 judge swap、prompt permutation、selection pressure 和 held-out acoustic strata 下，
  policy 的增益符号保持稳定或能被可靠 rollback。
- `H4 capability not abstention`：加入 guard 后的 unconditional task utility 仍超过强基线；只改善 selective risk
  而无净能力收益不满足主张。

## 2. 语音评估证据与 donor

| 证据 | 可借信号/失败模式 | 限制 |
|---|---|---|
| `SPEECH_NEAREST_PRIOR` AudioProcessBench (2606.09925) | reference-free step critic；majority 常优于 BoN；强生成器自评有大 SelfGap | critic skill 不等于 selection utility |
| `SPEECH_NEAREST_PRIOR` AudioJudge | 多方面 LAM judge、pairwise/pointwise、人类相关性与位置/冗长偏置 | system-level correlation 不保证逐实例替换安全 |
| `SPEECH_NEAREST_PRIOR` SpeakerSleuth | text-over-acoustic bias、speaker consistency 失败 | benchmark label 只作离线评估 |
| `SPEECH_NEAREST_PRIOR` ParaPairAudioBench、S2S/voice-agent judge studies | paralinguistic/对话 judge reliability 载体 | 不能替代主任务能力评测 |
| `SPEECH_NEAREST_PRIOR` Omni-RRM / S²ER | audio-capable reward、pairwise semantic equivalence | trained RM 与 protocol drift；需独立校准 |
| `CROSS_DOMAIN_METHOD_DONOR` Best-of-Poisson/HedgeTune、Scaling Flaws、SpecBench | selection-pressure 曲线、hacking threshold、validation-test gap | true reward calibration 与 i.i.d. pool 假设常不满足 speech loop |
| `CROSS_DOMAIN_METHOD_DONOR` CITE/Weaver/CORA/MARS | finite calibration、anytime-valid test、execute/abstain/stop | 只借统计合同，效果不迁移 |

## 3. Reliability controller

### 3.1 Condition-indexed error ledger

在隔离 calibration split 上估计每个 `(signal, action, condition, core revision)` 的 pairwise error、ranking
fidelity、tie/position/self bias 与 uncertainty。Condition 至少含 task、clean/noise/reverb、language/accent、
duration 和 core/service version。样本不足的 bucket 必须回退 pooled empirical policy，不能伪造精细保证。

### 3.2 Conservative decision rule

对 incumbent `i` 与 candidate `j`：

```text
accept j only if estimated_margin(j,i) >= threshold(c,a)
and provenance/gold/cost guards pass
otherwise keep i or allocate one bounded diagnostic action
```

当能支持 uniform bound 时，`threshold ≥ 2ε_c`；不能支持时使用 empirical LCB policy，并明确不称形式保证。
Abstain 只在任务协议允许且不会替代主 capability 统计时报告；unconditional utility 与 coverage-quality 同时给出。

### 3.3 Selection-pressure audit

对 candidate/action budget 做逐级 sweep，报告 `Peak / Final / Degradation`，监测 proxy reward 持续上升而
true task utility 下降。Judge swap、prompt order、candidate order、same-family/self-eval、adversarial acoustic
condition 与 held-out condition 都是强制 stress tests。

## 4. 实验设计

### 4.1 Stage-2A binding

与 R5/R6 共用 frozen core、MMAU Test-mini + MMAR、同短 horizon action menu。Calibration/test 完全隔离；
R8 不增加新能力动作，只决定是否执行/接纳/停止，使可靠性贡献可归因。

### 4.2 Arms

`always revise`、`always incumbent`、`global margin`、`hand threshold`、`consensus-only`、`judge-only`、
`condition-adaptive empirical gate`、`2ε-certified subset where supported`、`offline oracle gate`。另与 R6
无 gate 的 controller 对比。

### 4.3 Outcomes

Primary：unconditional task utility paired delta/LCB 与 worst-group delta。共同报告 correct→wrong、
wrong→correct、tail loss、seed variance、coverage、selective risk、calibration error、ranking/AUC、threshold
coverage、cost-quality frontier、selection-pressure degradation 和 rollback rate。

### 4.4 Reliability gates

- reward-vs-gold rank monotonicity与 per-prompt AUC；
- tie rate、大差距 tie、position/order bias、repeated-scoring Kendall’s W；
- SelfGap / same-family bias；
- semantic-equivalence merge/split error；
- condition-wise sample sufficiency；
- judge/proxy swap 后决策一致性。

## 5. Lean 与数学建议

现有 `RuntimeReliability` 允许的结论：若 incumbent 和 candidate 的估计效用均与真实效用相差不超过 `ε`，
且 estimated margin 至少 `2ε`，则真实非回归；严格超过则真实提升。Lean 不证明 `ε` 在真实 evaluator、
新 acoustic condition 或新 core version 上成立。

建议把全局 ε 扩展为候选相关误差：若 `|e_i|≤ε_i(c)`、`|e_j|≤ε_j(c)`，安全阈值是
`ε_i(c)+ε_j(c)`。对 finite calibration 可研究 PAC/conformal 或 anytime-valid confidence sequence，但必须
单列 exchangeability、coverage 与 repeated-selection 假设。对 adaptive trajectory，Best-of-Poisson 的固定
i.i.d. pool unimodality 只能作为待检验 hypothesis。

## 6. 击杀与重路由

- proxy 在 held-out condition 上无法给出稳定 ranking/error 证据：不得宣称形式可靠性，只保留 empirical policy。
- guard coverage 近零：判为不实用；不以低 risk 覆盖主能力失败。
- unconditional utility 不超过 best fixed：R8 只能作为风险报告，不是 capability contribution。
- selection pressure 下 true utility 明显下降：冻结 budget/threshold 到 peak 前并记录 hacking；无法定位则 rollback。
- condition buckets 太稀：合并分桶或仅报告观察性结果，不给伪精确门槛。
- judge swap 使结论翻转：结论限定到 pinned judge，不能称稳健。

## 7. 路线与预期贡献

Stage-2A 先估 empirical error/flip profile，再启用 conservative gate；只有覆盖率与增益同时达标才尝试
`2ε` 支持的 certified subset。预期贡献是 speech control 的 condition-indexed reliability protocol、能力与
覆盖联合报告、selection-pressure/hacking 曲线，以及形式定理到 executable trace 的 conformance 桥。

## 8. Provenance

语音 evaluator 事实来自 D5/T3 及本地 evaluator fulltexts；统计与 hacking 设计来自 D6 donor lane；Lean
结论来自 `RuntimeReliability.lean`。所有保证均保持条件化措辞。
