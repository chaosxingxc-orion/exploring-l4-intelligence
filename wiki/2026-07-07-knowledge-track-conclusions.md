---
title: "知识轨 Stage-1 结论 —— 多模态语音知识的组织形态 / 应用方式 / training-free RL 的作用与收敛"
date: 2026-07-07
stage: 1-argumentation + directional-experiment + theory(Lean)
status: "Stage-1 结论。论据 = 调研(argumentation)+ 冻结 Qwen3-Omni 上的 directional 实验(n≤60,paired-bootstrap CI,不定论)+ Lean sorry-free 收敛证明。任何 Stage-2 由 owner K/T9 gate。"
---

# 知识轨结论(回答三问)

> 🚨 **重大 caveat(2026-07-07,泄漏审计后):经验骨架被污染,Q1/Q2 的经验支撑作废、待边界干净重跑。** T7 的 KB 逐条含 ground truth(audit:answer_in_own_KB=1.0、in_topk=0.90),且检索 query 用了问题文本(部署应为音频)——H0/inject_k 增益几乎全是"查答案"而非知识辅助推理。**清白幸存:③ 的 Lean 收敛证明(纯理论)+ 调研/taxonomy。** ①② 的"RAG 大幅有效/flat-RAG 最优"**在清白重跑([[2026-07-07-T8-clean-rag-rerun]]:音频 query + 答案擦除)完成前不成立**。下文①②按此降级阅读。

> 取向:效果优先、非概念新。全程 boundary-clean、directional-only、不伪造。证据链:调研 [[2026-07-07-agentic-rag-landscape-omni-applicability]]/[[survey/2026-07-06-knowledge-backbone]] · 映射 [[2026-07-07-tfrl-baseline-effect-map]] · 有效性探针 [[2026-07-07-T0-consumption-validity-probe]] · 实验 [[2026-07-07-T7-rag-gate-experiment]] · 理论 `proofs/tfrl TfrlProofs/Realization.lean`(sorry-free)。

## 证据摘要(先摆事实)
| 来源 | 关键数(directional) | 含义 |
|---|---|---|
| T0 探针 | inject 正确参考 B=0.75–0.78,救回~42%;错配 C<A | 冻结 omni **能**消费注入知识但不完美;喂错会拖累 |
| T7 实验(heysquad,n=60) | base 0.283 → inject-all 0.767 → oracle 0.80;**H0=+0.517 CI[.38,.65]** | **知识 gap 大且 RAG 可关闭;omni 消费稳健** |
| T7 实验 | **gate−inject_k = −0.134 CI[−.23,−.05]**;检索 hit@5=0.90,门控保 gold 仅 0.73 | **精度门控掉点**:模型对干扰鲁棒,门控牺牲召回 |
| 调研 | CB-RAG 唯一干净训练无关语音正例;audio-native KG=空 cell;检索器是"要训练"的瓶颈 | 消费训练无关容易,检索/组织才是难点 |
| Lean | `selector_tendsto_oracle`(τ→0⇒oracle),sorry-free | 奖励引导选择的收敛,τ=承重约束 |

---

## 问① 多模态语音知识目前最优的组织形态?

**结论:对一个冻结的强 omni 做知识-QA,最优组织形态是"文本 passage 检索、以文本段注入"(flat/passage RAG),而不是(此刻)LLM-Wiki / GraphRAG / audio-native-KG。** 论据:
- **plain passage-RAG 已把冻结 omni 抬 0.283→0.80(T7),且模型对干扰 passage 鲁棒** → KG/层级/精排这些"更结构化"的组织在强模型 + 好长上下文下**边际收益小**;T7 的激进精度门控反而 −0.134。
- **LLM-Wiki / GraphRAG** 的价值在**多跳/全局 sensemaking**(T1 landscape),对**单跳知识-QA**冻结 omni 用不上;**audio-native KG 是空 cell(未建)**,且 audio-native 检索**要训练**(WavRAG/SpeechRAG),违反训练无关。
- **绑定约束是检索召回 + 文本投递**:把对的 passage 拿进上下文(召回)、以**文本**呈现(冻结 omni 最干净的消费路径)。检索器保持**现成/off-the-shelf**(omni 训练无关地消费它)。
- **诚实边界:** 上述基于**干净检索 + 单跳**;**ASR-噪声 query / 多跳 / 副语言键控** regime 可能更需要富组织(本轮未测)——这是 LLM-Wiki/KG 的 Stage-2 空间,不是一阶的赢法。

## 问② 多模态知识应该如何被 omni agentic system 应用?

**结论:按(口语)query 检索外部 passage,以文本注入冻结 omni 的上下文,让其 in-context 消费——冻结 2026 omni 对此稳健(0.28→0.80),能容忍干扰 passage。** 应用原则:
- **召回优先、非精度门控:** 把对的 passage 拿进 top-k;**不要**激进门控/丢弃(模型能处理干扰;门控牺牲召回反掉点,T7)。
- **文本投递:** 检索知识以文本段注入(冻结 omni 最干净的消费;audio-native 键控要训练)。
- **边界:** 注入**外部知识、绝不注入答案**([[Information-Boundary-Guard]],M3 泄漏教训)。
- **omni 的特有角色(语音):** (a) 理解口语 query 以驱动检索、(b) 消费文本知识回答口语问题——**音频通道对 query/感知重要,知识本身是模态无关的文本**。

## 问③ training-free RL 如何发挥作用并收敛?

**作用(被证据重定向):** TFRL = 对 RAG 回路决策点的推理期奖励引导选择。但 **T7 证明:在强、干扰鲁棒的 omni + 干净检索下,"利用优化(门控)"的准确率空间很小,精度门控甚至掉点**。故 TFRL 的有效作用点**不是滤干扰**,而是:
- **(a) 效率**:奖励引导的**何时/多少检索**——base 已对 0.283 项答对,对这些检索是浪费;when-gate 可在**同等准确率下降低检索率/延迟**(语音场景的关键轴);
- **(b) 受压 regime**:ASR-噪声 query / 多跳,检索+利用未饱和处(Stage-2 活口)。

**收敛(机器验证,T5 `TfrlProofs/Realization.lean`,sorry-free):** 奖励引导选择器(best-of-N / 按估计奖励 R̂ 的采纳排序)在**奖励估计误差 τ = sup|R̂−R| → 0 时收敛到 oracle**:
- `selector_ge_ref_sub_two_tau`:realized ≥ oracle − 2τ(correctness);
- `selector_tendsto_oracle`:τ→0 ⇒ realized → oracle(convergence,squeeze)。
- **τ 是承重约束(C4):** 无界 τ(无约束)时 realized 可任意低于 oracle → 2τ 间隙正是"有界估计器"买来的。两段(无约束发散/有约束收敛)结构满足理论轨。

**理论⟷实验的闭环(螺旋回报):** **T7 里 R1 门控失败,恰是该定理前提被违反**——TF-IDF 相关性代理 R̂ 的 τ 太大(错排、丢 gold),选择器没逼近 oracle,故门控掉点。**定理正确地指出:奖励引导选择能否帮上忙,由奖励代理质量 τ 决定。** ⇒ TFRL 要收敛到 oracle,须**要么把 τ 做小**(更好的相关性/去相关验证器),**要么把杠杆挪到存在小-τ 可验证奖励的决策点**(如基于模型置信的 when-gate)。

---

## 一句话总纲
**冻结的 2026 omni 已经能稳健消费外挂文本知识:知识轨的一阶赢法是"召回优先的文本-passage RAG",不是更花哨的组织;training-free RL 的收敛已被证明(τ→0⇒oracle),但其准确率杠杆在干净单跳下近饱和——真正的 TFRL 价值在"效率(何时检索)"与"受压 regime(噪声/多跳)",且成立与否由奖励代理的 τ 决定。** 这是一个**开源可复现、抬升现有 RAG 基线阈值**的诚实起点,而非营销式净新。

## 后置(owner / Stage-2)
- 重定向后的首个 Stage-2 验证:**when-gate 效率**(同准确率、更低检索率/延迟)或**ASR-噪声 query regime** 的利用增益;并把 τ(相关性/验证器质量)作为可控变量。
- 富组织(LLM-Wiki/GraphRAG/audio-native-KG)留给**多跳/全局**任务的 Stage-2。
- Lean:C1(KL 信赖域)/C2(N* 预算)迭代收敛可在 `Realization.lean` 之上继续(当前已交付 C4 selection 收敛)。
