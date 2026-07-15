---
protocol_id: PROBE-PROTO-2026-07-14-01
title: Stage-1B 四探针预注册协议 v1（owner 签批件——签批后才开机）
date: 2026-07-14
stage: Stage-1B（directional prototyping；owner 续40 裁决 1B 先行、四探针全包）
status: DRAFT_FOR_OWNER_SIGNOFF — 签批前零 GPU 运行
prerequisites_met: "C1/C4 = CENSUS_COMPLETE（Research-Objective open item 6；工件仍名 *-draft，owner 终验并入本协议 §7 签批动作）；身份合同+same-selector contract = FROZEN（续41，commit dce5c79，blob sha256 1338f6b16f5409022b0a8193c5e71729dcf65ba78f1fa41b3645e642efc208b1）"
discipline: "廉价小样、单次触碰、全部尝试（含失败）入登记、信息边界守卫、directional-only/hypothesis-grade、不做显著性结论、负结果一等公民；探针不改变任何 survey 结论等级"
generated_by: "Claude Fable 5 主会话（基于冻结合同 §1–§7 起草）"
signoff: { owner: PENDING, date: null }
---

# Stage-1B 四探针预注册协议 v1

> 所有探针打在**冻结后的**身份合同判据上（续41）。任何协议偏离须在执行前登记修订，
> 执行后发现的偏离入负结果/异常表——不得静默。

## 0. 共享设定（全探针一致）

- **模型**：Qwen3-Omni-30B GGUF via 常驻 `llama-server`（`-ngl 28`、`input_audio` 路径——既有
  可用配置）；SER 备选 = 盘内锁内 nemotron3-nano-omni（若 30B 对 SER 提示不稳，登记后切换；
  **锁外模型一律禁用**——Qwen2-Audio 不在冻结资产内亦不在盘上，不作备选）。
- **池共享（硬规定）**：**四探针共用同一批池。** P-α 池在登记为 **c0=裸 prompt** 的供给下生成
  （H(c) 是供给条件量——池的 c 必须登记）；P-β/P-γ 直接对 P-α 池打分；P-δ 的 c0 腿=P-α 池，
  **全协议仅 P-δ 的 c1 新增一次生成**。
- **池几何（合同 §7）**：每 **(item, 供给 c)** 组合单次生成 K=16 候选（temperature/采样参数运行
  前登记入 attempt registry），**单次触碰**：同一 (item, c) 不重采、不重跑（失败标 FAILED 保留在分母）。
- **格（cells）**：C-ASR = LibriSpeech test-other 子集（shifted 一侧）；C-SER = CREMA-D 子集；
  C-AU = **mmau-mini（锁内资产）**子集。每格 n=60–100 items（预算内取上限；n 运行前冻结并登记）。
- **信息边界（合同 §7）**：test-item gold **只**在事后评估 U 时使用；不进入 prompt、池构造、
  任何打分信号 S、检索或候选处理。打分信号的输入模态与来源按合同 §7 登记轴逐一登记。
- **登记**：每次运行（含失败/中止）追加 `docs/integrity/experiment_attempt_registry.jsonl`
  扩展段；原始输出存 `speechrl-data/_repro/1b-probes/`（E 盘,运行后更新 e-drive 登记册）。
- **环境纪律**（既有教训）：GPU 启动前查 `pgrep`+gpu_session 锁与并发会话；detached 跑法=写 .sh
  后 `wsl bash <path>`,`python -u`,`HF_HUB_OFFLINE=1`;kill 从 .sh 内按路径执行。
- **报告纪律**：ρ cellwise-only,四量并列（rho_greedy/rho_pool/delta_mbr/regret）;头空过小标
  `HEADROOM_TOO_SMALL` 只报绝对量;全部数字 directional-only。
- **预声明切点（防事后弹性;均为方向性判读阈,非显著性检验）**：HEADROOM_TOO_SMALL = 头空
  绝对量 C-ASR <1.0 WER 点、C-SER/C-AU <3pp;「选择高度一致」= 选择重合率 >90%;「shuffle 不
  改变选择」= 翻转率 <10%;「H(c) 明显为正」= 超过对应 HEADROOM_TOO_SMALL 切点。

## 1. P-α 头空测量（服务：全部候选的存在性前提）

- **测什么**：每格 U_greedy（beam/greedy 默认输出）、E[U_pool]、U_oracle（池内按 U 最优）→ H(c)。
- **判读（directional）**：≥1 格 H(c) 明显为正 → 选择器纲领有对象；**全格 H(c)≈0 → 停线上报
  owner**（这不杀单一身份,而是动摇整个 selector 方向——escalate,勿自行解释）。
- **产出**：每格 (U_greedy, E[U_pool], U_oracle, H) + 分布草图；n、K、解码参数如实登记。

## 2. P-β MBR 基线（服务：I1 杀手作为我们自己的锚）

- **测什么**：同一批池（P-α 池）上 MBR 的 rho_greedy/rho_pool/delta_mbr/regret。**成对效用预注册**：
  C-ASR = 1−WER 两两互评（与文献 BLEU 口径的差异注明）；C-SER = 候选标签多数票一致率（两两同标=1
  异标=0）；C-AU = 候选答案两两一致率（选择题精确匹配）。此三定义属 §7 冻结参数,非执行层小参数。
- **判读**：能否在 C-ASR 重现文献量级（LibriSpeech ~31%,注意 ReazonSpeech ~9% 的数据依赖——
  台账 #2）;偏离本身就是 I4 供给依赖性的方向性素材。
- **边界**：MBR 是基线不是研究对象;此处不比较"我们的方法"（尚无）。

## 3. P-γ 同核自有信号（服务：strict-I2 生死条件,合同 §3 kill-if）

- **开机前置（0 成本 smoke,不通过不开机）**：以 1 item 验证「音频条件下对**给定** continuation
  取全序列 logprob」在 llama-server 现有端点可行（已验证的只是音频**生成**路径,echo-logprob 打分
  从未 smoke 过）;不可行则登记替代实现（如逐 token 强制解码取分）后方可开机。
- **测什么**：(a) 同核 audio-conditioned 似然对 **P-α 池**打分;(b) 外部纯文本 scorer（文本 LM
  困惑度）同池打分;(c) **shuffle-audio 对照**：打乱音频后同核信号是否仍选同一候选。
- **判读（严格对齐合同 §3 冻结判据,kill/pivot 不互换）**：shuffle 翻转率 <10%（不改变选择）→
  **kill 方向**（文本流畅度伪装）;δ_corr 方向≈0（同核与外部选择重合 >90%）→ **kill 方向**
  （同核信号无独立价值）;同核信号无效**而**外部 scorer 有效 → **pivot 方向**（坍缩回 I1）;
  二者分离且同核兑现为正 → 存活方向。
- **产出**：选择重合率、各自 rho（四量）、shuffle 对照翻转率。

## 4. P-δ 供给对比（服务：I4 供给条件化前提,合同 §5）

- **测什么**：在 C-ASR + C-AU 两格,对比两种供给 c：c0=P-α 池（裸 prompt）vs c1=加一种既有供给
  （检索上下文或任务指令增强,运行前择一登记——c1 是全协议唯一新增生成）;各自重测 H(c) 与 MBR 兑现。
- **C-T7 防线（若 c1 选检索,不可豁免）**：开机前产出机检边界审计工件（检索库与全部测试 item 的
  gold 零交集证据,C3 式,入 docs/checks/）——前科：+0.517 检索供给佐证因 C-T7 泄漏判 INVALID。
  c1 选型本身不回签,该审计**不得豁免**。
- **判读**：H(c0) vs H(c1) 或 ρ(c0) vs ρ(c1) 出现方向性移动 → I4 的「兑现面随供给变形」前提
  有对象;不动 → I4 供给轴前提存疑（进 Stage-1C 决策材料,不自动 kill——供给设计问责,
  headroom 归因纪律）。
- **边界**：c1 只用 read-out 类供给（读出既有能力）,禁 new-info 类（注入题目新信息——信息边界）。

## 5. 预算与工期

- GPU：单卡 5090 本地;估 [K=16 × (60–100 items) × 3 格 × (1 生成 + 2 打分道)] + [P-δ c1 侧：
  2 格 × (60–100 items) × K=16 生成 + 头空/MBR 打分] ≈ 数天墙钟（llama-server 常驻,音频输入
  吞吐为主导）;探针间串行、道内批处理。
- 全部为一次性预算;超预算 → 停下登记,不追加不重跑。

## 6. 探针不能做的事（预登记禁区）

不做显著性检验;不做跨任务 ρ 平均;不把任何探针数字写成结论级（全部 hypothesis-grade,
供 Stage-1C 决策包 v2 作方向材料）;不因结果难看而换格/换供给重试（换=新修订,须再签批）;
不自动滚入任何 proceed/kill 裁决——三结局判据的裁决人是 owner（Stage-1C）。

## 7. Owner 签批

```text
签批语义：① 批准按本协议开机执行 P-α/β/γ/δ;协议参数（K=16、格、n 范围、池共享、MBR 效用定义、
预声明切点、判读框架）冻结,执行层小参数（采样温度、具体 n、c1 选型）运行前登记即可,不再回签
（c1 若选检索,C-T7 边界审计工件不得豁免）;② 同一动作完成 C1/C4 census 终验
（docs/integrity/2026-07-14-c{1,4}-*-census-draft.md 转正式）。
签批不构成：对探针结果的任何预先背书;结果解读权在 Stage-1C 决策包 v2。
owner: ____________   date: ____________
```
