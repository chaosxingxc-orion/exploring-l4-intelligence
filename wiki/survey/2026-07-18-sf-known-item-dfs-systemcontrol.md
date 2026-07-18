---
artifact_id: "SF-KNOWN-ITEM-DFS-SYSTEMCONTROL-2026-07-18-01"
title: "known-item 保证队列 8 项之 system-control 13 轴 DFS 深读（v4 复审 P0-3/P0-4 整改;owner 裁决③④）"
date: 2026-07-18
method: "两个隔离深读代理（Opus）逐篇全文 PDF 精读;schema = amendment-9 §3 的 system-control 13 轴 + 负结果 + 与本项目关系（仅事实差异,禁创新定性——owner 裁决④仍生效）;全文正典:5 arXiv 双 rendition 入 fulltext ledger,3 ACL 官方源救援入 survey-backups（sha256 于 v4-review 访问台账）"
verification: "主执行方承重引文抽查:批 A 6/6 逐字命中（其一为 PDF 抽取粘连词假阴性后复核命中）;批 B 5/5 命中（其一为连字换行变体复核命中）——合计 11/11;抽查只声称抽中项定位质量。〔dated correction 2026-07-18(v6 复审):①Agentic Coding 记录中 PDR 段的信号语义以 coding-v4 为准——vanilla PDR = random-K 随机采样无选择信号（TeX 一手:'For random-K, we follow PDR and randomly sample K previous summaries';select-K 才经 RTV）,本文批 A 散文对 PDR/RTV 未分变体处以此更正;②Team-of-Thoughts 信号分期裁决 = 离线校准标量 + 推理期合成内定性评估,无部署期独立 reward（P1-1）——『orchestrator 聚合(画像)』表述维持,reward 归类以 coding-v4 为准〕"
recall_note: "65 查询离线召回（正典 matcher）:ATLAS 5 命中(SF-L2-Q1/L13-Q1/L13-Q3/L14-Q1/L15-Q1)/AutoTTS=SF-L2-Q1/AgenticCoding=SF-L2-Q1/TeamOfThoughts=零命中/ToolGate=零命中;ACL 3 项非 arXiv 走官方源;known-item 身份与零命中反例身份并存,不加 seed、不称召回修复"
loadbearing_facts: "〔dated correction 2026-07-18(v5 复审 P0-2/引用审计):本字段的自由文本身份汇总被 identity taxonomy v1 机器重编码取代——正典 = wiki/survey/2026-07-18-sf-known-item-coding-v2.json + docs/checks/2026-07-18-sf-identity-taxonomy-test.json(9 method path,占据合取机器重算;『非 reward-model 引导』类散文口径撤回——llm_judge∈reward 集合);ATLAS 88.9% 补条件 = GPQA-Diamond 单基准 Fig 7a 有可定义正确多数收敛点的轨迹子集,非跨基准总体;正文各篇逐轴事实记录维持不改写〕①八项中零项含 speech/audio〔已检视集合〕;④Agentic Coding 的选择显式不触 gold=read-out-only 实证参照;⑤ATLAS 自适应停机+stateful 直接合成 = decision-rights/停止轴的最强组件先验"
---

# known-item 8 项 system-control 13 轴 DFS

## 批次 A（ATLAS / AutoTTS / Agentic Coding / Team of Thoughts）

## 2606.01667 ATLAS: Agentic Test-time Learning-to-Allocate Scaling

### 方法一段
一个 LLM orchestrator 端到端拥有 test-time scaling 的控制回路,通过唯一动作 `explore`(派发一个全新独立 solver 求解原题)反复决定「继续取证 vs 停机合成」。每个 explorer 只见原题、从零求解,返回结构化候选 `(answer, reasoning, approach, confidence)`;只有 orchestrator 跨调用累积证据池(p3 "only the orchestrator accumulates evidence across calls")。停机后 orchestrator 基于完整 Thought/Action/Observation 轨迹直接合成终答(称 "stateful evidence management")。动作空间可扩展:ATLAS-MM 增加 solver 选择维度、ATLAS-MI 增加定向指令维度;正交超参 explore-effort(Low/Med/High)调节停机阈值。骨干 = Claude Sonnet 4.6,零训练、纯 prompt/SDK。

### system-control 13 轴
1. **核心身份**:单核在场但角色二分——orchestrator + explorer 均为 LLM 调用;权重/结构均不改(p14 "delegated controller with two roles: an orchestrator and an explorer")。跨族可换(Qwen/Gemma/GPT-5.2,vLLM 本地服务)。
2. **访问级别**:API-only 文本/结构化输出;explorer 返回摘要字段非全轨迹(p10);无 logits/hidden。
3. **全系统训练范围**:全冻结、零训练——"no external rule, scoring function, or learned controller in the loop"(p2/p3,逐字核验命中);verifier 无(orchestrator 自评);reward model 仅作对照 baseline 不入主方法。
4. **控制时域**:多步轨迹级(explore-or-stop 循环,budget T=8;ATLAS-MM T=20)。
5. **decision rights**:orchestrator 凭 in-context 候选池评估独占 explore/stop 决策;判据=独立 solver 异途同归 + 信息增益是否值回成本(p4)。
6. **状态/记忆**:orchestrator 累积候选池并保留完整 T/A/O 轨迹;explorer 无状态(条件独立)。无跨会话记忆。
7. **工具**:唯一工具 `explore`=派发新 solver(p14);候选作 Observation 入 orchestrator 上下文;可选 `integrate`(ablation)。
8. **反馈/奖励**:label-free,共识+自报 confidence;无 learned reward;「多数纠正」与「少数提取」并存(p17 "Reasoning quality overrides vote count")。
9. **候选生成与选择**:K 池=N 独立候选;selector=orchestrator 直接合成(非打分器);等 K 基线在场(LLM Selection 固定 8-explore、Majority Voting、Reward reranking,p8 Table 7)。
10. **停止/预算**:核心贡献=自适应 early-stop;explore-effort 三档;88.9% 轨迹恰在收敛点停机(p8)。
11. **终态合成**:orchestrator 直接合成;独立 integrator 更贵且无增益(p6 Table 4b)。
12. **信息边界**:explorer 仅见题面,test gold 隔离;Grading 用 gold 但仅评估、排除于回路(p15)。
13. **模态/任务**:HLE-Verified/LiveCodeBench/GPQA-Diamond/BabyVision(视觉)。**无 speech/audio**。

### 负结果与适用条件
独立 integrator 3/4 基准降或平(仅增成本);关 extended thinking GPQA −1pp;引用负结果:naive parallel scaling 非普遍有益、symmetric debate 无超越 majority 的增益;适用条件:orchestrator 只需 in-context 读候选轨迹并决策,跨族均正增益,prompt 为 benchmark-agnostic。

### 与本项目关系
**component-prior**(兼 boundary-comparator)。近同构骨架:冻结核心+零训练+orchestrator 决定 gather-more/stop/synthesize+label-free——自适应停机与 stateful 合成可直接作组件先验;关键差异:(a) 共识/合成非 **reward 引导**;(b) orchestrator 自身即第二个强 LLM,非单一冻结 speech/omni 弱核;(c) **无 speech/audio**。

## 2605.08083 LLMs Improving LLMs: Agentic Discovery for Test-Time Scaling (AutoTTS)

### 方法一段
把 TTS 策略设计重构为「环境驱动的自动发现」:构造离线回放 MDP 环境(预采集基座 N 条推理轨迹+probe 信号),explorer LLM(Claude Code)多轮编辑代码提出候选 controller,在离线回放上零 LLM 调用地廉价评估,读 accuracy-cost 曲线+执行轨迹反馈跨轮精炼;beta 参数化把 controller 收敛为单标量 β 防过拟合。基座(Qwen3 0.6–8B)全程冻结,产物是代码 controller,held-out(AIME25/HMMT25)评估;全发现 $39.9/160 分钟。

### system-control 13 轴
1. **核心身份**:双模型分离——冻结基座 solver+explorer LLM 写代码;**权重全不改**,产物=代码非权重(p12 与 TTT-Discover/ThetaEvolve 的权重更新路线明确对照)。
2. **访问级别**:文本/答案级;controller 观测=活跃分支/深度/probe 中间答案/剩余预算;非 logits。
3. **全系统训练范围**:基座 frozen;controller 经代码搜索合成(非梯度);**但发现目标用搜索集 gold**(`1{ŷ=y}−γC`)→权重意义 training-free、**标签监督的离线发现**。
4. **控制时域**:双时域——离线元发现(5 轮)+推理时分支级管理(branch/continue/probe/prune/stop)。
5. **decision rights**:分层——元层 explorer 依轨迹+acc/cost 重写代码;对象层代码 controller 依状态选 admissible action。
6. **状态/记忆**:发现 history 跨轮复用;推理时每题重置。
7. **工具**:离线回放环境;probe=零成本读预采集中间答案(p4)。
8. **反馈/奖励**:发现奖励=accuracy−γ·cost(**用 gold**)+执行轨迹反馈;推理时 controller label-free。
9. **候选生成与选择**:每(model,problem)预采 128 轨迹;selector=controller 终态共识型 Agg;等 K 基线 SC@64/ASC/ESC/Parallel-Probe。
10. **停止/预算**:controller 自适应 width×depth 分配+停/剪;β 调 acc-cost。
11. **终态合成**:确定性 Agg 聚合。
12. **信息边界**:held-out "never used during discovery or selection"(逐字核验命中)——test gold 隔离干净;**但 controller 是标签监督搜索产物**(需带标签搜索集=new-info 依赖)。
13. **模态/任务**:数学(AIME/HMMT)+GPQA 泛化;**无 speech/audio**,纯文本。

### 负结果与适用条件
去 beta 参数化→过拟合(held-out 53.1→49.0);去执行轨迹→更差且更贵(标量反馈不足);初始 controller 压 token→acc 崩;适用条件:须可建离线回放环境+带标签搜索集。

### 与本项目关系
**component-prior**(兼 boundary-comparator)。「离线回放廉价评估控制策略」方法论高度可移植(预采集冻结 speech/omni 核心 K 池后零重跑试 selector/controller);关键差异:(a) **标签监督离线发现**(TF-Strict/label-free 边界反例);(b) 共识 Agg 非 reward-guided;(c) 无 speech;(d) 创新在发现方法非部署 controller。

## 2604.16529 Scaling Test-Time Compute for Agentic Coding

### 方法一段
面向长程 agentic coding(每尝试=动作/观测/报错交织长轨迹),核心论点「表示」瓶颈:每条 rollout 用同一冻结模型摘要成结构化摘要(保假设/进展/失败模式)。以摘要为接口两维扩展:并行=Recursive Tournament Voting(RTV,N 条独立 rollout→摘要→G=2 两两小组 V=8 投票锦标赛递归淘汰,**不触 gold/测例**);顺序=Parallel-Distill-Refine(PDR,iter-1 新 rollout 条件于 iter-0 蒸馏选出的 K 摘要)。5 冻结前沿模型+mini-SWE-agent/Terminus 脚手架,零训练。

### system-control 13 轴
1. **核心身份**:单一冻结前沿 LLM/次运行——同一模型兼 rollout/摘要/比较投票三角色;权重不改;跨 5 模型可换。
2. **访问级别**:API-only 文本;pass/fail 仅评估 oracle 不入方法;无 logits。
3. **全系统训练范围**:**全冻结零训练**;选择显式 label-free——"without access to any ground-truth outcomes, test cases or test samples"(逐字核验命中,PDF 抽取粘连词)。
4. **控制时域**:多步轨迹级+跨迭代(iter0→iter1)+并行种群;调度固定常数(N=16,T=2,K=4,G=2,V=8)。
5. **decision rights**:**固定调度非自适应**;唯一决策=RTV 组内比较投票+PDR 选 K 摘要;无自适应停机(与 ATLAS 关键分野)。
6. **状态/记忆**:跨迭代状态=选中 K 摘要作精炼上下文;每迭代环境重置;摘要=可复用表示。
7. **工具**:**真实工具环境**(bash/terminal 读文件改代码执行,报错入上下文)——四篇唯一真外部工具。
8. **反馈/奖励**:LLM 对摘要的比较投票(self-eval/共识,label-free);无 reward model。
9. **候选生成与选择**:K 池=16 并行 rollout;selector=RTV;pass@N 仅 oracle 上界;摘要作比较基质优于原轨迹(Finding 1)。
10. **停止/预算**:固定预算,无自适应 early-stop;iter1 步数约减半为涌现结果非决策。
11. **终态合成**:**选优非合成**(final RTV 返回 top-1 原样)。
12. **信息边界**:四篇最干净 read-out-only——选择全程无 gold/测例/测样。
13. **模态/任务**:SWE-Bench Verified/Terminal-Bench v2;编码单域。**无 speech/audio**。

### 负结果与适用条件
摘要>原始长轨迹(末轮尤甚);递归小组>flat 大组,V≈8 后收益递减;多先验(K=4)>单先验,select-K>random-K;iter1 通过率随精炼上下文质量单调(0/4→近零,4/4→97-99%,garbage-in-garbage-out);GPT-5-0825 增益但绝对最低(受基座能力约束);适用条件:长程 rollout/binary 任务/rollout 间残余多样性/前沿模型。

### 与本项目关系
**component-prior**(强 boundary-comparator 价值)。四篇中最贴合「K 池+label-free selector」:RTV=可直接借鉴的 selector,PDR=供给侧 c 机制,其「选择不触 gold」正是 read-out-only 理想的实证参照;关键差异:(a) LLM 自比较/共识非 reward 打分;(b) 编码域无 speech;(c) 强前沿 LLM 真工具使用非文本输出冻结弱核;(d) 固定调度。

## 2602.16485 Team of Thoughts: Efficient Test-time Scaling through Orchestrated Tool Calling

### 方法一段
异构多智能体框架:7 个不同后训练模型族当「专门化工具」,中心 orchestrator 经原生 tool-calling 动态调用最合适子集(默认 k=2)。两组件:Orchestrator Calibration(**带标签校准集**实测各候选「聚合工具输出」准确率选最佳协调者——协调力与规模解耦)与 Agent Self-Assessment(每工具 agent 在校准集上**给 ground truth** 自审生成能力画像)。推理时画像喂 orchestrator,依匹配度选择性激活、评估、聚合(GMM 混合概念化)。全冻结、无梯度。

### system-control 13 轴
1. **核心身份**:**联邦/异构**——7 族;orchestrator=其一;权重不改。
2. **访问级别**:API-only 文本;条件于工具**离散响应**非连续分布;无 logits。
3. **全系统训练范围**:无梯度训练,**但 calibration 与 self-assessment 用 ground truth**("its own reasoning trajectories, and the ground truth",逐字核验命中)→冻结权重、标签监督的离线配置。
4. **控制时域**:单响应为主,可迭代工具调用。
5. **decision rights**:orchestrator 凭画像+校准决定激活哪些工具/评估/聚合(Selection/Evaluation/Aggregation 三功能)。
6. **状态/记忆**:全局上下文 Z 追加工具输出;能力画像预计算、跨 query 持久(静态先验)。
7. **工具**:工具=其它 LLM,原生 tool-calling;**只回终答优于含轨迹**(AIME25 pass@1 95.33→78.67)。
8. **反馈/奖励**:校准准确率(**gold**)选 orchestrator+生成画像;推理时靠画像匹配;**非 label-free**。
9. **候选生成与选择**:K 池=激活的 k 个工具候选(k=2);selector=orchestrator 聚合;等 K 基线+Theoretical Limit oracle 在场。
10. **停止/预算**:选择性激活=预算分配;无自适应停机。
11. **终态合成**:orchestrator 聚合/合成。
12. **信息边界**:test gold 经交叉校准隔离("50% of AIME2025 serves as the calibration set for AIME2024",逐字核验命中);**但系统依赖带标签校准数据=new-info(标签依赖)**。
13. **模态/任务**:数学+代码;**无 speech/audio**。

### 负结果与适用条件
含完整推理轨迹降协调性能(95.33→78.67);k≥8 崩(82→60%,长上下文不解);|E|>50 选择过载;协调力与规模解耦(235B 当 orchestrator 仅 26.67%);适用条件:异构专长互异+带标签校准+小 k。

### 与本项目关系
**boundary-comparator**(兼 component-prior)。orchestrator 选择性激活与「只回终答」负结果可借鉴;边界价值最大——**gold 标签离线画像/选择**直接违反严格 label-free/read-out-only;差异:(a) 标签监督配置;(b) 异构联邦非单核;(c) 画像匹配非 reward 引导;(d) 无 speech。

### 批次 A 横向小结（事实,非结论）

| 维度 | ATLAS | AutoTTS | Agentic Coding | Team-of-Thoughts |
|---|---|---|---|---|
| 训练/标签 | 零训练、label-free | 零权重更新,发现用 gold | 零训练、**显式 label-free** | 零梯度,校准/自审用 gold |
| 控制器 | 自适应 agentic(停机=核心贡献) | 离线发现的代码 controller | **固定调度** | orchestrator 选择性激活 |
| 选择信号 | orchestrator 共识/合成 | 答案共识 Agg | LLM 比较投票(RTV) | orchestrator 聚合(画像) |
| 终态 | 直接合成 | 确定性 Agg | **选优 top-1** | 直接合成 |
| speech/audio | 无(视觉) | 无 | 无 | 无 |
| 角色 | component-prior | component-prior | component-prior | boundary-comparator |

四篇**均无 speech/audio、均非 reward-model 引导**;Agentic Coding 的 label-free 选择纪律、AutoTTS 的离线回放评估方法论、ATLAS 的自适应停机+stateful 合成 = 三个最可移植组件先验;Team-of-Thoughts 与 AutoTTS 发现阶段的 gold 依赖 = TF-Strict/read-out-only 边界的两个反例对照。

## 批次 B（ToolGate / DeepVerifier / Selective TTS / DREAM）

〔主执行方引文抽查:5/5 命中——ToolGate『decoding log probabilities, or tool outputs』
逐字 +『All VLM weights are frozen…only the lightweight Tool-Gate classifier is trained』
（连字换行变体核实）+『cross-domain gate is trained only on out-of-domain VQA sources』
（两变体皆 trained 的直接证据）;Selective TTS『lack sufficient data to train robust reward
models』;DeepVerifier『prone to the same set of failures in different roll-outs』;DREAM
基线表含 REBASE/MAJ 对照〕

## 2606.03054 ToolGate: Token-Efficient Pre-Call Control for Tool-Augmented Vision-Language Agents

### 方法一段
冻结 ReAct 式 VLM（Qwen3-VL-30B/235B-FP8）推理中提议感知类工具调用（OCR/检测/分割/裁剪/深度）;每个被提议调用执行**之前**,外部轻量控制器读轨迹前缀文本+待执行调用,输出 execute/skip;skip 则回填固定 no-op 消息。控制器 = 冻结 MiniLM 句向量+9 维结构特征→L2 逻辑回归,"does not access hidden states, image features, decoding log probabilities, or tool outputs",不改 VLM/prompt/工具栈。token 成本降至基线 64–69%、每回合执行调用 2.73→1.02;matched-domain 训练时 30B 再 +1.65。

### system-control 13 轴（要点）
1. **核心身份**:单一冻结 VLM 核;控制平面外挂 **trained** 逻辑回归。2. **访问级别**:部署期纯文本+结构元数据（黑盒）;logits 仅离线打标探针用。3. **训练范围（关键）**:核 frozen;控制器 **supervised-trained**——**无 zero-shot 未训练变体,cross-domain 与 in-domain 两种都是训练过的分类器**（区别只在训练数据域）;标签源=forced-answer 探针+终局正确性（**离线用 gold**）。4. 控制时域:轨迹内逐工具调用级。5. **decision rights**:仅对已提议调用 execute/skip——"ToolGate does not choose which tool to call",无 retry/branch/终止权。6. 状态:逐调用近无状态（前缀左截断 1500 字符）。7. 工具:六感知工具,VLM 决定调哪个、门决定是否执行。8. 反馈:训练用 wrong→right 翻转代理标签（离线 gold）;部署无奖励。9. **无 K 池无终答 selector**（逐调用二值门,非 best-of-N）。10. 停止/预算:本质即 execute-skip 成本控制,τ 单调调节。11. 终态合成:无。12. 信息边界:部署期无 test gold（干净）;gold 仅离线标签/诊断。13. 模态:视觉 VQA 多基准,**无 speech/audio**。

### 负结果与适用条件
235B in-domain 门**反降 1.32 分**（execute-positive 稀疏时匹配域未必好）;更重输入信号（图像特征/logprob）**不**改善部署 trade-off;**prompt 自调节失败**（VoI 自报降到 60.0 且反增工具量）——「外部控制器优于让模型自调节」;tool-only 已是强基线（低效多为 per-tool 系统先验）;代理标签保守非真 VoI。

### 与本项目关系
**component-prior**。「外部黑盒纯文本控制器 + execute/skip 成本门 + 外部控制优于自调节」= 预算/工具授权轴直接先例;差异:(a) 控制器监督训练（违 TF-Strict）;(b) 视觉非 speech/omni;(c) 逐调用二值门非 K 池 reward 引导选择。

## 2026.findings-acl.1243 DeepVerifier（Inference-Time Scaling of Verification）

### 方法一段
策略型深度研究智能体（DRA,主实验 Claude-3.7-Sonnet）产出答案+轨迹;DeepVerifier 三模块流水线:分解 agent 把轨迹压成分步摘要、按自动构建的 DRA 失败分类法（5 大类 13 子类）定位可疑点、提 ≤3 个可外部核验 yes/no 追问;验证 agent（可 web 搜索/截屏/代码执行）逐一从外部证据作答;judge 综合打 1–4 分,≤2 判错→纠错反馈回喂重试,循环至接受或上限。主实验闭源零训练,GAIA +8–11%;另发布 DeepVerifier-4K（4,646 SFT 对)微调 Qwen3-8B 得开源变体。

### system-control 13 轴（要点）
1. 核心身份:多智能体（策略 DRA+分解/验证/judge 三子 agent),主实验权重不动。2. 访问级别:API 文本。3. **训练范围（审计）**:主实验**整系统 frozen/prompt-only**（"without additional training"）——verifier 能力来自强闭源模型+人工分类法 rubric;**开源变体对策略主干 SFT**（两路径分立记录）;分类法由人工标注 555 error points 离线构建。4. 控制时域:多步轨迹+跨轮迭代（≤10 轮,3–4 轮见顶）。5. decision rights:judge 判 accept/reject;分解 agent 决定查什么（gather-more）;reject→反馈驱动 retry;终止=接受或上限。6. 状态:跨轮携带轨迹+追问答案+反馈,分步摘要作压缩状态。7. 工具:验证 agent 用 web/截屏/代码。8. 反馈:**rubric-based outcome 验证器**（agent-as-judge,1–4 分),靠 verification asymmetry+外部证据;**推理期 label-free**。9. **序贯精修非 K 池**——明确对比 BoN"prone to the same set of failures in different roll-outs"。10. 停止:验证器接受即停或达上限;≤3 追问有界核验成本。11. 终态:被接受的答案。12. 信息边界:推理期不用 test gold,但验证 agent**检索新外部证据（web = new-info 获取）**;离线分类法/SFT/元评估用 gold。13. 模态:web-research 多模态（GAIA/XBench/BrowseComp）,**无 speech/audio**。

### 负结果与适用条件
弱模型→反馈质量退化;精度**早峰后回落**（correct→incorrect 迁移跨轮持续,过度迭代有害）;去验证模块→高精度低召回;去分解→继承原 agent 同类错;部分子集增益有限（GPT-4.1 仅 +2–3%）;成本/延迟上升。

### 与本项目关系
**component-prior**。「rubric 引导 label-free 验证器+核验分解成可核验子问+迭代反馈带早停」= reward/停止轴先例;差异:(a) 序贯精修非 K 池选择;(b) 控制平面是重 LLM agent 且**检索 new-info**;(c) web-research 非 speech/omni;(d) 开源变体 SFT（TF 边界）。

## 2026.findings-acl.1724 Scaling Unverifiable Rewards（Selective TTS）

### 方法一段
多智能体数据分析流水线（剖析→可视化〔生成执行绘图代码+chart-judger 滤废图〕→洞见→judger 核验;生成 Qwen2.5-VL-32B,judge GPT-4o/4.1-nano）。终局质量不可验证→设计 easy/moderate/harsh 三档 LLM-as-Judge,用人类专家配对偏好**选出**与人最一致的 harsh judger（Kendall τ=0.55）作 pseudo-ground-truth。Selective TTS = 过程维分阶段剪枝:每阶段 stage-local LLM 评估器排序、按剪枝比 α 裁候选,**固定预算**（LLM 调用数）下把算力从单轮宽度重分配到更多轮探索;61.64→65.86、方差降。

### system-control 13 轴（要点）
1. 核心身份:多智能体异构双主干,权重全不动。2. 访问级别:text/API,judge 为 VLM 读图表+文本。3. **训练范围**:**全系统零训练**——所有 agent 与 judge 均 prompt-based frozen（明确因"lack sufficient data to train robust reward models"弃训练路线）;人类对齐仅用于**选 judger（选择非训练）**——**八篇中最接近 TF-Strict**。4. 控制时域:多阶段流水线+固定预算多轮。5. decision rights:stage-local 评估器决定逐阶段剪枝（α 控选择性）;预算控制器决定再起多少 run。6. 状态:流水线中间工件传递,run 间独立。7. 工具:绘图代码执行+报错回溯。8. 反馈:**LLM-as-Judge（不可验证奖励,无 rule/gold）**;harsh judger 因 τ=0.55 被选作 pseudo-GT;**部署 label-free**——**镜像本项目 label-free proxy S / 无 U 场景**。9. **显式 K 池**（各阶段 bs=5,至 k³ 候选）+stage-local 剪枝+终 judger 选优;**α=0 全展开=等 K 基线在场**+random pruning+final-stage-only(≈BoN) 对照。10. **停止/预算 = 核心贡献**:固定预算+剪枝重分配（O(pv·n³) 有推导;α=0.6 最优）。11. 终态:judger 排序最高者,选优非融合。12. 信息边界:不可验证任务**根本无 gold 可泄**;人工标注仅离线选 judger（干净）。13. 模态:图表/数据科学视觉,**无 speech/audio**。

### 负结果与适用条件
α=0.8（≈各阶段 best-of-N）**退化**（stage-local 评估器与终 judger 未对齐→过剪）;random pruning 显著更差（增益来自有引导剪枝）;final-stage-only(≈BoN) 落后完整版（**早阶段剪枝才是关键**）;**高质量报告上 judge-人类对齐崩**（top 段 τ=−0.15——顶部人也难分）;整体 τ=0.55 本身不完美。

### 与本项目关系
**component-prior（八篇中机制层面最贴近）**。「全系统零训练+label-free LLM-judge 对 K 池选优+固定预算分阶段剪枝+人对齐选 judger」= selector/预算/label-free proxy 轴最强设计先例;差异:(a) 多异构核生成流水线非单一冻结 speech 核;(b) 奖励主观不可验证（无 U 真值/oracle headroom 框架）;(c) 选择在过程剪枝非事后 K 池。

## 2026.findings-acl.511 DREAM（Reward-Guided Dual-Phase Adaptive Inference）

### 方法一段
在冻结推理 LLM（Qwen2.5-Math-1.5B/DeepSeekMath-7B/LLaMA-3-8B）上做树搜索,把每推理步拆 plan 相位与 execution 相位分别独立搜索（各采 N 候选、PRM 打分留 top-n）;自适应预算双阈值——≥n 候选超高阈值提前停,全低于低阈值补采 m。**奖励模型是微调件**（数学=微调 Qwen2.5-32B,代码=微调 Qwen2.5-Coder-7B;rollout 派生标签 ~400k/数据集）。GSM8K/MATH/AMC23+HumanEval/MBPP 上改善精度-效率前沿。

### system-control 13 轴（要点）
1. **核心身份:双模型**——冻结策略 LLM+**trained PRM**（分立微调模型）。2. 访问级别:PRM 读文本输出 +/− token logit 作奖励（其自身 logit）;对生成器文本级。3. **训练范围**:策略核 frozen;**PRM=TRAINED**（TF-Strict 边界:选择器的奖励模型被微调）。4. 控制时域:多步树/beam,每步拆 plan+exec 子相位。5. decision rights:搜索算法+PRM 决定留哪些 plan/exec、预算（早停/补采）。6. 状态:beam 轨迹内状态。7. 工具:代码任务用可见测试执行（通过率=执行奖励）;数学无工具。8. 反馈:**learned PRM**（rollout 标签离线用 gold）;推理期无 gold。9. **K 池+PRM selector**;基线=majority vote/beam/REBASE,等预算前沿比较。10. **停止/预算=核心**:双阈值早停+补采,预算从易步挪难步（GSM8K ~80% 步早停/MATH ~5%）。11. 终态:累积奖励最高轨迹。12. 信息边界:PRM 训练离线 gold（标准监督);推理期干净;代码用可见测试（任务规格非隐藏 gold）。13. 模态:**纯文本** math/code,**无 speech/audio/vision**。

### 负结果与适用条件
自适应预算在 MATH 增益边际（步难度均匀时重分配收益甚微——**只在步难度差异大时有效**）;**分开的 plan/exec RM ≈ 单一共享 RM**（分离无收益）;LLM critic 仅边际→移除;奖励打分便宜（FLOP-rew < 1/10 FLOP-gen）。

### 与本项目关系
**component-prior**。「对冻结生成器做 reward 引导 K 池搜索+自适应预算/早停」= 本项目 selector/预算轴最直接的 reward-guided 先例;差异:(a) **PRM 微调**（违全系统零训练——正是 VeGAS 类『测试时不改 policy ≠ 全系统 training-free』边界的又一例);(b) 纯文本非 speech/omni;(c) 过程级树搜索干预非黑盒输出事后选择。

---

## 全八项跨批小结（事实,非结论;创新定性属 owner,未锁定）

1. **模态普查**:八项**零项含 speech/audio**（与七篇威胁集普查一致——speech/omni 在 system-control 文献中的缺位持续成立,仍待 Stage-1B mapping 全语料确认）。
2. **训练范围轴普查**:全系统零训练且 label-free 部署 = ATLAS、Agentic Coding、Selective TTS 三项;AutoTTS/Team-of-Thoughts 离线依赖 gold（发现/校准);ToolGate/DREAM 外挂控制器/PRM 被监督训练;DeepVerifier 主实验零训练、开源变体 SFT。**「冻结核心 ≠ 全系统 TF-Strict」在八项中五次实证**。
3. **reward-guided 轴**:唯一「trained-PRM 引导 K 池搜索」= DREAM（trained comparator);**零项做「training-free reward 信号引导冻结核 K 池选择」**——共识/自评/比较/画像是主流选择信号。
4. **decision-rights/停止轴最强先验**:ATLAS 自适应停机、DREAM 双阈值预算、Selective TTS 固定预算剪枝重分配、ToolGate execute-skip 门、DeepVerifier 验证器早停——五种停止/预算机制互补,全部可作 Stage-2A 组件候选。
5. **反例对照价值**:「外部控制器优于模型自调节」（ToolGate prompt 自调节失败）与「stage-local 评估器与终 judger 失配则过剪退化」（Selective TTS α=0.8）= 外部控制平面设计的两条实证约束。
