# Gate S1 系统性自库反扫结果（mandatory seeds 候选）

（协议步骤工件：零外部查询——仅扫仓内 12 个文件〔neighbor-matrix v2 / sota-cards v2 /
canonical-census-v2 / scout-ledger r1+r2 / round2_new_targets / X3 test-time map / L4
speech-agentic / 3w-crossdomain / 归档 agent-convergence·memory·skills〕。执行 = Opus 代理,
2026-07-15;协调者注：代理报 paper_works "96 行"系行计数方式差异,正典计数维持 95 works
@28ad858 不变。候选总数 ~76 distinct IDs：STRONG 15 / MEDIUM 23 / WEAK ~38〔9 桶〕。）

## STRONG（列名 mandatory seeds,协议 §3 已采）

| ID | 名称 | 出处 | 一句话性质 |
|---|---|---|---|
| 2408.03314 | Scaling LLM Test-Time Compute Optimally (Snell) | round2_new_targets + X3 + 3w | compute-optimal TTS 奠基作,round-2 已自标 promote |
| 2407.21787 | Large Language Monkeys (Brown) | neighbor-v2 L7 + census + X3/3w | coverage-vs-K 对数线性律——ρ/oracle 分裂的文本域孪生 |
| 2203.11171 | Self-Consistency (Wang) | scout1 + X3/3w | 无标签共识选择正典源头 |
| 2305.20050 | Let's Verify Step by Step (Lightman) | scout1 + X3 | 过程奖励验证正典（PRM） |
| 2110.14168 | Training Verifiers (Cobbe) | X3 | 结果验证器正典（ORM,6B+verifier 胜 175B） |
| 2402.08115 | Self-Verification Limitations (Stechly) | X3 | 无 sound verifier 时自验证失败——label-free selector 成立边界 |
| 2402.01694 | ARGS: Alignment as Reward-Guided Search | X3 | 冻结 LLM 解码时奖励制导搜索——研究对象的文本祖先 |
| 2309.07124 | RAIN: Align without Finetuning | X3 | 自评+回退,零训练权重冻结 test-time 对齐 |
| 2310.01798 | LLMs Cannot Self-Correct Yet (Huang) | X3 + 3w | 内在自纠退化/oracle 假象——对照纪律来源 |
| 2407.01502 | AI Agents That Matter (Kapoor) | 3w | 成本受控 agent 评测正典——simple retry Pareto 压制 Reflexion/LATS |
| 2506.12928 | Scaling Test-time Compute for LLM Agents | L4 C07 | BoN over agent rollouts + list-wise verification（轨迹选择） |
| 2406.12045 | tau-bench (Sierra) | L4 C02 | 可验证奖励 tool-agent 环境正典 |
| 2407.09886 | Speech-Copilot (Kuan/Lee) | L4 C09 | LLM 编排语音工具+程序生成,training-free——语音原生 agent seed |
| 2507.19457 | GEPA: Reflective Prompt Evolution | X3 + 3w + skills | 反射式 prompt 进化等预算胜 GRPO——黑盒优化最强证据 |
| 2309.03409 | OPRO: LLMs as Optimizers | X3 + 3w | LLM-as-optimizer,prompt-space headroom 量化正典 |

## MEDIUM（协议执行时裁决,23 条）

2311.17311 USC / 2408.15240 GenRM / 2506.07982 tau2-bench / 2407.01489 Agentless /
2502.18581 Self-Certainty BoN / 2510.04618 ACE / 2304.03442 Generative Agents /
2402.06147 DeAL / 2509.21749 Thinking with Sound / 2603.13686 tau-Voice /
2411.17451 VL-RewardBench / 2310.02743 RM-Ensembles-Overopt / 2503.21878 Is-BoN-Best /
2501.19393 s1 / 2605.05716 Cross-Component Interference / 2508.19828 Memory-R1 /
2506.23049 AURA / 2505.17656 Too-Consistent-to-Detect / 2509.17995 Variation-in-Verification /
2505.11730 VG-Search / 2605.10991 Test-Time Personalization / 2512.02008 Art-of-Scaling-TTC /
2606.02981 Predicting-Inference-Gains（threatens I4,在案）

## WEAK（9 桶,lane 查询自然覆盖——桶名+代表,全清单见本文件 git 版原始代理输出）

Prompt-opt（APE/FormatSpread 等）· MM-verifier（VisualPRM/VisVM）· Agent-arch
（AFlow/AgentSquare/SWE-agent/OSWorld/UGround）· BoN/MBR 理论（soft-BoN/hard-BoN-KL/MBR-conv/
GSI/CarBoN/Twisted-SMC/BoN-smoothing——SURVEY-B 已继承,soft-BoN 最接近升 MEDIUM）· 语音-agent
基准（VoiceAgentBench/FDB-v3/EchoChain/Audio2Tool/From-Text-to-Voice/AudioMC）· Agent-记忆系统
（MemoryBank/A-MEM/HippoRAG/Zep/Mem0/MemoryOS）· Skill-库（SkillsBench/CoEvoSkills/SkillRouter/
CREATOR/CRAFT）· 语音-奖励模型（WavReward/GSRM/ParaS2S,多 trained,positioning 用）·
跨域 VLA（RoboMonkey）

## 关键结论（进协议依据）

- 正典缺口最刺眼处 = test-time-scaling/verification 祖先链（列了 TTRL/MAV 却无
  Snell/Monkeys/Self-Consistency/Lightman/Cobbe）与 reward-guided decoding 文本祖先
  （ARGS/RAIN）——已全部入列名种子。
- round2_new_targets 中被 review 自标「promote to matrix-level」的 6 条,除已列名 2 条外其余
  5 条均已入 STRONG/MEDIUM。
- STRONG 中 Monkeys/Snell/GenRM 已在 v2 矩阵但未作 seed;其余 STRONG 仅存于归档调研件——
  两类「仓内已知」都被本次反扫检回。
