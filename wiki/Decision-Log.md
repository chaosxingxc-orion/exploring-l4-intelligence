# Decision Log

> Append-only, lightweight ADRs — the team's durable **memory**. Newest on top. One entry per
> decision: date · what we decided · why · consequences. Humans and AIs both append here (see
> [[AI-Collaboration]]), then publish with `scripts/wiki-sync.sh`.

---

### 2026-07-09 · 三锚点增量再定级 + Q1/Q2 决策单 + Stage-1 双轨闭环战役设计（A2 再定级生效；三条方法论要求立规；分工硬化）

**Decision.** Owner 复提三锚点（A1 speech-key/异构-value 组织、A2 "已证外接优于 rollout"、A3 数据
底座）要求批判性反思，并开出 Q1（统一 vs 特化嵌入器，emotion2vec/codec 是否纳入）/Q2（ASR 困难
样本记忆、SLU intent 整段、slot 片段的粒度组织）两个设计问题。本日裁定：① **A2 接受 07-08 再定级
提案**——诚实表述 = 已证 rollout read-out 上界 + Stage-2 定理目标（τ*>0 邻域收敛 + N* 预算）+
方向性经验证据，不再声称"已证明"；② **三条方法论要求立规**：理论必须辅以小规模数据验证并跑
debate-verify-improve loop、理论必须 survey 充足且以 Lean 保证收敛/一致性并显式提取假设与约束项、
数据验证必须覆盖全部本地数据集（无 silent cap）；③ **分工硬化（三次重申）**：Fable 5 零 legwork
（协调/评价/指导），技术验证+方案调研 → Opus，代码 → Sonnet。产出三文档：
[[2026-07-09-three-anchors-delta-regrade]]、[[2026-07-09-q1q2-embedder-granularity-decision-memo]]、
[[2026-07-09-stage1-dual-track-campaign]]。

**Evidence.** 三路代码/文档盘点（勘误：误用 Sonnet 执行，owner 当日纠正分工）→ **20 项承重判定经
6 个 Opus 对抗验证束逐条复核：16 CONFIRMED / 3 PARTIAL / 1 REFUTED**。新发现要点：泄露 verdict
只写不查（kb_poc 实际构建并检索过 LEAKAGE 源）；持久 KB 从未被任何真实实验使用；registry "built"
虚标 4 项；T8 结构性同池复用仍在（字符串 scrub 残留 1.7%）；**"同基座"经复核软化为部分成立**
（REFUTED 我方原判"唯一 importer"——speechrl_common 被 7 个 m 系/repro 脚本真实使用；Hydra+
Qwen2-Audio 名义路径仍是无映射 stub）；unpinned revision 10/28；W1 reproduce 字段 23/25 因 D→E
迁移过期；Lean 台账 6.1–6.7 全确认（唯一 sorry=BestOfN:90、三定理前件假设、收敛全为
squeeze-over-assumed、"跨界"两定理 FRAMING-ONLY、over-confidence 仅 docstring、Reachability 唯一
实质 few-shot 定理是**上限**方向）。E 盘机器盘存：**39 数据集/18 模型在盘、零无主目录、嵌入器
候选池 12/12 全齐**（owner 纠正："17"只是 lock 28 的建议纳入子集，覆盖底数必须以盘存为准）。

**Consequences.** 战役结构 P1 收口三文档 → **P2 owner 讨论门**（调研 §7 八项议程 + 3 新裁决位：
lock 增补扩至 gap 数据集 / "同基座"消解方向 / 复现加固优先级；**不冻结不开跑**）→ P3 前置工程
（Sonnet；P0 = retrieve 侧强制 verdict 门 + kb_snapshot 接入一切新跑）→ P4 理论轨（Opus survey +
Lean：τ*>0 门控注入定理、N* 落地、Beirami sorry 清欠、dual-track binding 升级为测试）⟷ P5 数据轨
（覆盖矩阵：26 纳入 / 13 显式排除各带理由；loader 7 有 ~19 缺）→ P6 辩论 loop（干涸判据 = 一轮无
新分歧）→ P7 记录。"自以为满足信息约束/工程声称但实际未达成"清单 6→9 条。memory 更新两条（分工
硬约束、双轨 loop 方法论）。下一步 = P2 讨论门。

### 2026-07-09 · 数据根从 D 盘迁到 E 盘（speechrl-data）

**Decision.** 把 `speechrl-data/`（模型 + 数据集 + repos + manifests + _repro，共 ~651 GB）整体从
`D:\chao_workspace\exploring-l4-intelligence\speechrl-data`（WSL `/mnt/d/…`）迁到
`E:\chao_workspace\exploring-l4-intelligence\speechrl-data`（WSL `/mnt/e/…`）。仓库/代码仍留在 D 盘。
迁移方式：robocopy 复制 → 校验文件数/字节数一致 → 删除 D 源。`SPEECHRL_DATA_DIR` 从"逐次内联传参"
改为在 WSL `~/.bashrc` 固化为 E 盘路径，运行时自动命中。

**What changed.** 唯一硬编码 D 盘*数据*路径的脚本 `scripts/data/fetch-qwen3-omni-gguf.sh` 改为 honor
`SPEECHRL_DATA_DIR`（默认回退改到 E 盘）；`CLAUDE.md`/`AGENTS.md`/`README(_CN)`/`docs/data.md`/
`docs/setup.md`/`wiki/Data-and-Assets.md` 的数据位置声明 D→E、~440→~650 GB。其余脚本/配置本就走
`${SPEECHRL_DATA_DIR:-<repo>/speechrl-data}`，无需改动。历史 dated 记录（append-only）不改写。KB 早已
在 E 盘（`SPEECHRL_KB_DIR=E:/speechrl-knowledge`），不受影响。

**Why.** D 盘吃紧（迁移前 D 已用 890 GB / 剩 515 GB），E 盘 3.8 TB 空闲；把大体量只读资产迁到 E 腾出
D 盘，并与既有 E 盘 KB 约定一致。仓库留在 D 以保持 `common/src` 等代码路径不变（如 `m5_selector_rescore_dev.py`
内的 `sys.path` 绝对路径）。

---

### 2026-07-08 · 三个技术锚点的批判性审计（A2 再定级提案）+ 语音向量化 survey-first 决定

**Decision.** Owner 提出三个技术锚点并要求对抗性审计。两路独立审计（W1 逐行 + wiki/proofs 盘点，
判定全部核到 path:line/commit）结论：**A1（speech-key/异构-value KB）设计夯实、验证未夯实**——唯一
端到端验证是 logmel 冒烟键恒等往返，CLAP/omni-embed 未建过真库，omni-embed loader 实际未接通，且
CLAP（audio-event 模型）与内容型主任务族可能错配；**A2（"外接能力源优于 rollout 已理论证明"）不成立**
——已证的是 rollout read-out 上界 + τ→0 假设下的 squeeze，"外接跨越边界"两定理是自评 FRAMING-ONLY
的平凡 ∃ 见证，over-confidence 只是经验注解非定理，且 clean 经验证据（T8 null + 24% 采纳率）反对朴素
版主张——**再定级提案：A2 = 已证 rollout 上界 + Stage-2 定理目标（τ*>0 邻域收敛 + N* 预算）+ 方向性
证据**；**A3（数据+脚本底座）最扎实但有五刺**（T7 boundary 标签误导→已加 errata、verbatim-only 泄露
审计盲区、item-id 冻结未接入 T 跑、"同基座"与 Hydra stub 脱节、目标 regime 无外部 baseline）。
"自以为满足信息约束而未达成"清单 6 条入 `2026-07-08-three-anchors-critical-audit.md`。

**Owner 三点指示**：(1) 审计先记录并同步；(2) **survey-first、规划后置**——充分调研 2025-01 之后的
语音向量化（speech2vec 类）方案、与 owner 讨论后才做实验规划，本轮不锁嵌入器/实验设计；Stage-1 最高
优先 = **数据集覆盖度**（所有小规模数据集完成验证，产出覆盖最广的数据方案+实验型技术方案统一表）；
(3) 提交并同步远端，代码与研究进度一致。**模型分工确立**：Fable 只做编排/判据冻结/对抗把关/综合，
调研委托 Opus 代理群（8 维度 finder + 对抗验证 workflow 已启动），代码实现委托 Sonnet（本日完成
kb_audit latent bug 修复 + T7 errata）。配套产出：`2026-07-08-dataset-coverage-inventory.md`
（28/28 数据集逐条盘点，17 纳入/11 显式排除带理由，lock↔kb_registry 双向对齐）。

**Why it matters.** 这是对研究地基的一次系统性"自查自纠"：把最强声称（A2"已证明"）按 committed
tree 的实际内容降回诚实位置，把信息边界的"标签合规但信息违规"活例（T7）钉进勘误，并在选型前立起
"充分调研 → owner 讨论 → 再规划"的顺序纪律。Q1/Q2（统一 vs 特化嵌入器、任务粒度组织）的候选方案
空间已写入审计文档 §6，待 2025+ 调研矩阵到位后与 owner 讨论定夺。

**（同日后续）调研完成。** 8-finder Opus workflow + 40 条对抗验证（34 CONFIRMED/6 PARTIAL/
0 REFUTED）收官，主文档 `2026-07-08-speech2vec-survey-2025plus.md`（附录 dims-1-4 / dims-5-8 入
`survey/`）。七条主发现：**CLAP 词汇内容键失效硬确证**（LibriSpeech R@1 0.1% vs GLAP 93.8%、
AISHELL-2 98.5%）；**frozen-omni 隐态可检索性获外部支持**（LCO-Omni 无音频对比训练登 MAEB 榜一，
利好 W4）；无单模型全任务族最优 → 指向「内容主键+speaker/emotion 特化键」2–3 键架构，与 W4
"单空间多读出"构成待裁决竞争假设 H-a/H-b；codec token 作键=空白+劣势；语音无成熟 late-interaction
→ slot 走两级检索；ASR 困难样本记忆先例强（BR-ASR 200k 词规模化✅）且"frozen omni 自身嵌入作键"
确认为文献空白；omni-embed-nemotron 官方 API 确诊 loader 错因（非对称 encode_document/encode_query），
但其音频零样本弱+NC license → 主键候选地位动摇。8 项 owner 讨论议程见主文档 §7——**选型与 T11
规划留待讨论，不预执行**。

**（同日后续 2）下载底座就位 + 两项 owner 裁定。** 按"Opus 出清单、Sonnet 写脚本、Fable 驱动调试、
调通即停交 owner 手动下载"的分工完成：模型清单 `docs/models.candidates.json` + 数据集缺口清单
`docs/datasets.gap-candidates.json`（G1 说话人/G2 zh-ASR/G3 zh-SER，P1≈44GB 补齐全部缺口；否决
3D-Speaker 191GB/WenetSpeech/CASIA/VoxCeleb 全量），配套 `fetch-candidate-models.sh` /
`fetch-candidate-datasets.sh`——六条源路径（hf-mirror Xet-safe 单连接 aria2、ModelScope、GitHub
release、OpenSLR 多连接+CN 镜像回退、HF 数据集、manual）全部实测调通，调试抓出 3 个真 bug（nargs
--include 覆盖、grep -c 双零、--only 被层级过滤吞）。GGUF 核查（Opus）：**LCO-7B 有社区 GGUF**
（marksverdhei，Q8_0 8.1GB+mmproj 2.5GB，--pooling last）；e5-omni-7B 全网无 GGUF、自转有
modal_temp.pt 校准风险。**Owner 裁定：① 重型模型入默认下载清单（一次做对）；② e5-omni-7B 整体
移出参考范围（删除条目）**。最终模型清单 12 项 ≈28GB；omni 嵌入对决候选收敛为 LCO-3B/7B GGUF
（llama.cpp 栈内）+ 本地已有 omni-embed-nemotron-3b（对照）。

### 2026-07-06 (later) · Omni-agentic 综述战役收官 → 契约相对主论点 + 收敛定理 + 7 方向到 K 终闸
**Result.** 战役 A0→D4 全部完成、到达 owner 终闸(K/T9,不自动进 Stage-2)。产出:框架 D0 + 14-lane/~120-
系统综述(D1,3 遍文献核查硬化)+ 正式论文 D2 + **五人格严格评审 D3(全 sound-with-corrections)+ 全面修订 +
re-review 判 cleared-for-owner** + 问题定义 D4。少量实验论证:p6 感知-delta、GAP-1 正向搜索、E10/E10b/T2/T3/
T5/T6。理论证明:`InfoBoundary`+`AgenticElements`(定义性)+ **`BestOfNConvergence`(收敛,约束项=去相关误差
τ→0;受约束收敛/无约束不收敛的对偶,填 CLAUDE.md 要求的收敛半)**,全 sorry-free、全库 green(8560 jobs)。

**评审把主论点从过强改到诚实(契约相对)。** 原"冻结模型只有 new-info 要素能跨越"被五人格一致判过强:项目
canonical 本就把 **decoding / reward-guided decoding 列为 in-scope** 训练无关杠杆,故 **contrastive decoding
(合约内解码律改动,信息无关)也能抬 ceiling**。修订后:**Claim A(要素=唯一新信息载体,成立)/ Claim B(只有
要素能抬 ceiling,假)** 分离;**使用方式(对固定生成律的选择/编排)受 oracle@N 界**——能把 greedy 抬向 oracle、
但抬不过;跨越需要**要素 ① 或 合约内生成律改动 ③**。给了要素的**可操作判据**(是否引入模型推理输入里没有的
条件比特)。另修正两处过度断言:2505.24347 是**单冻结 GPT-4o 自检、缺 oracle 对照 → 未决(GAP-6)**,非
"化为要素";p6 "validates" 是我记录在案的过度伸张老毛病 → 降为"方向一致但不充分,自产 ASR 混淆,SQuAD-only/
VocalBench-zero 的形态反而利于混淆解释,强外部 ASR 对照是前置条件"。

**Verdict(Stage-1,呈交 K).** **构建方案**:冻结文本脑 + 可换 new-info 要素(freeze-and-bolt-on;omni 的非
commodity 价值=感知>转写 + 音频键记忆/知识;全双工出局=需改基座);能力只来自新要素或合约内解码改动;验证叉
(verifier-as-tool 有效、as-role 弱)。**推荐研究方向(排序,rubric 先冻结)**:**GAP-6**(oracle 对照的自检=能
否证伪主论点的决定性最便宜实验,先跑)· **GAP-3**(omni 去相关 verifier,已有收敛理论,W1/W4 对齐)· **GAP-1**
(voice-agent best-of-N 抵 pass^k——旗舰但部分已知答案的工程 demo)· 外加 **GAP-7**(合约内解码抬 ceiling,评审
新浮出的信息无关杠杆)。**架构分叉(omni 传感器 vs 大脑)**:survey 证据偏 sensor-split,但感知-delta 前置条件
未立(p6 未决)——**留 owner 在 T9 定**。**Why it matters**:第 4 次(也最系统的)过度伸张纠正,靠的是五人格
盲审的独立视角 + 项目自身 canonical 的字面——把一个漂亮但过强的主张,收敛成一个诚实、契约相对、可证伪的
Stage-1 结论。分支未推送、wiki 待同步。

### 2026-07-06 · Owner 修正 2026-07-03 关闭：重开完整 omni agentic 系统 + 立「要素-用法」框架 + 开正式综述战役
**Decision.** Owner **行使 2026-07-03 NO-GO 关闭决定 §9 明确保留的「owner-level amendment」路径**
（`wiki/2026-07-03-omni-agentic-tfrl-go-no-go-decision.md`：re-open 需外生 r1–r3，且记录注明「in-house
后继证据无外生重开路径→flagged for owner-level amendment」），**主动修正该关闭，重开完整 omni agentic
系统**（含被关闭的**跨会话累积** skills/memory/routing），以 Q1 结论（[[2026-07-05-Q1-conclusion-corrected]]：
ICL 不足 → 需 new-info 记忆）为依据。**Append-only：不改 2026-07-03 记录**；此后引用该关闭须并引本条修正。

**框架（Owner 四轮 Socratic 精修 × 我们的定理，收敛为「要素-用法分类学」）。** Owner 起初提三支柱（能力/
skills、知识脊柱、记忆），问「还有哪些盲区」。经四轮精修定为**三轴**+一个主论点：
- **轴① 要素（≈闭集，唯一 new-info 载体）**：model · 系统/用户 prompt · connector 三型{skills/tools ·
  knowledge · memory}。Owner 三支柱 = 三个 connector 型要素。
- **轴② 使用方式**（角色/编排/多智能体/路由——规划、校验-as-role 在此）：**对同一冻结模型的花式用法 =
  read-out 类 = 被 T8 `InfoBoundary` oracle 上界卡死、越不过知识 gap**（E10/E10b 已实测：同权重+critic
  prompt 的双系统 verifier 从不超过 majority）。
- **轴③ 约束/质量**：感知保真（model 质量）、实时/全双工（**基座**属性）、对齐（横切）。
- **主论点**：**对冻结模型，agentic 杠杆只能来自新增 new-info 要素（能算/取新事实的工具、外部知识、带外部
  内容的记忆、真正互补的另一个模型），不能来自对同一模型的花式使用方式。** Owner 原三要素恰是正确的
  new-info 载体；我最初误列的四「盲区」被正确归位为轴②/轴③。校验分叉：as-role（弱，E10 已否）vs as-tool
  （外部 checker/executor = 轴①真要素）。

**Owner 两挑战择出「我们的研究前沿」。** ①驱动规划/控制的模型**不必是多模态**——可用文本 LLM API（DeepSeek
V4 Pro 类）；⇒ 控制/编排是 **commodity**（且独立更强模型本身即 new-info 互补要素），非我们的 omni 研究点。
三种 new-info 精确分工：文本 LLM 加推理+世界知识（受转写所限）、omni 加**感知（>转写）**、记忆/知识加外部
存储。**M3 教训在此咬住**：omni 只喂转写 = ASR→text-LLM、丢了音频。②**omni 不适合作全双工基座**（现有含
Qwen3-Omni 是回合制/半双工；全双工需双流基座 = 改基座 = 违反冻结主旨，Owner 明确当前不动基座）⇒ 全双工/
实时**剔出研究范围**（仅作 survey landscape）。**⇒ 我们真正的研究前沿 = 两个 omni 特有的 new-info 要素：
(i) omni 作富感知要素（训练无关激活、暴露 >转写的 delta；M3 教训升为核心问题）；(ii) 音频-理解为键的
记忆/知识 connector（Q1b）。** 架构分叉（omni-传感器 vs omni-大脑 vs 混合）**Owner 定：不预锁，survey 扫清、
T9 定夺**。

**战役（Owner 三决策 2026-07-06）**：正式综述论文 + 五人格严格评审（对标 171-ref 语义综述）；语音/omni 为主
（VLM/GUI 仅跨域参照）；覆盖 2025-01→今主要多模态/语音 agent 系统的**构建 + 评测**，锚在我们盘上那批**已拥有
但从未跑过**的 agentic 基准（tau2/eva/soulx-duplug/audiomc/voiceassistant-eval）。交付 A0→D0 框架→D1 survey
Workflow→D2 论文→D3 评审→D4 问题定义 v2→K 终闸选题（不自动进 Stage-2）。计划 `academic-skill-workflow-*.md`。

**Why.** 关闭当初封的是「在冻结契约下、靠自设机制立即建跨会话 agent」；如今**问题先行**（Q1 已证 ICL 不足、
只有 new-info 越过知识 gap）+ **要素-用法框架**给了它一个良构的问题定义骨架。修正是程序合规的（走 §9 预留
路径）、留痕的（本条 append）、且 Stage-1 的（survey/论证为核心，选题仍归 T9 终闸）。分支未推送、wiki 待同步。

### 2026-07-05 (later) · 修正战役：信息边界准则立起 → 合法杠杆重测 → Q1 结论订正（M3 撤回后重建）
**Decision / 背景.** 主人指出一个**低级但根本**的错误：M3（注入 golden 转写）是**信息边界越界**——"如果我都有
了 text ground truth，为什么还需要音频输入？"若有转写就不需要 omni 模型（改用 ASR→text-LLM，否定了 omni
的初衷）。这是与早先声学 oracle 造假同类的错误，且**统计纪律没抓到它**——靠的是主人的任务定义/模态边界视角。
遂**先立准则、再重测、后订正**（全程 Stage-1 方向性；每个杠杆过 [[Information-Boundary-Guard]]）。

**做了什么（全部 boundary-clean）.**
- **G0** 立 [[Information-Boundary-Guard]]（4 问：部署有此输入？尊重音频-only？无测项泄漏？真能力 vs 喂答案），
  **撤回 M3/Q1b 锁**（[[2026-07-05-A-realization-conclusion]] 挂撤回横幅），重评旧实验（P2/E8/E10/E10b 保留，
  M3 撤回，E7 重做）。
- **T1** [[2026-07-05-task-definition-rubric]]：回到最原始任务定义，逐族列"真实部署输入 / 合法杠杆 / 越界线"
  （SQA-音频内容[mmau 给文本问题] vs SQA-音频问题[转写=泄漏=M3]）；跨族 R-input/R-reward（**可部署奖励**：
  自一致/置信/规则/工具成功——WER/对金标准准确率**不是**可部署奖励）/R-fewshot 规则。
- **T2** 正确的"任务定义 few-shot"（audio+文本 how-to-handle+train 推理示范，测项音频-only）：**仍不超过 plain**
  （mmau −0.075 n.s.；vocalbench −0.175 SIG−；SQuAD ±0）。示范确带真任务信号（C−b1 SQuAD +0.10 SIG+）但被多模态
  few-shot 格式成本抵消。**补上了"E7 设计错误 → Q1a 未定"的缺口**：正确设计下 Q1a 仍成立。产物 `_repro/t2_taskdef_fewshot.json`。
- **T5** [[2026-07-05-t5-headroom-composition]]：仅用模型自身样本（P2 greedy vs oracle@8）拆 headroom = **内部实现
  gap**（oracle−greedy，E10/E10b 证内部选择拿不到）+ **能力/知识 gap**（1−oracle，无一样本正确→需外部信号）；
  知识 gap 在知识问答最大——**vocalbench-zh 42.7%**，即记忆系统的目标市场。
- **T8** `proofs/tfrl/TfrlProofs/InfoBoundary.lean`（sorry-free，全库 green）：形式化 read-out vs new-info。
  read-out 选择器（best-of-N/自一致/E10 双系统）**只可能选中自己的样本**→ 上界=oracle@N（`readout_acc_le_oracle`），
  知识 gap 是**整个 read-out 类的不可约误差下界**（`readout_error_ge_gap`）；只有改变采样分布的 new-info 杠杆能越过
  （`newinfo_can_cross_gap`）。收敛半部接 `BlindSpot.avg_regret_tendsto_zero`（frac=gap）。
- **#37** [[2026-07-05-W4-value-reassessment]]：旗舰 W4 是 **read-out 杠杆**（重组自身 embedding、不引入新信息）→
  受 oracle 上界约束、碰不到知识 gap；但它改善记忆的**检索键**（更解耦=更好的键）→ 与 new-info 记忆**互补而非替代**。
- **T6 Step 1**（主人明确优先方向"step by step 尝试…压缩/检索/使用三策略最核心"）：统一**压缩键**可行性探针——
  键=模型自产的音频内容压缩摘要（可部署、仅作索引，非注入金标准，绝非 M3）。产物 `_repro/t6_compression_feasibility.json`。

**Verdict（订正后，Stage-1 方向性；[[2026-07-05-Q1-conclusion-corrected]]）.**
- **Q1a：ICL/指令优化不足**——三个合法 read-out 杠杆（T2 few-shot、E8 提示优化、E10/E10b 双系统）全部不过；
  read-out 上界是被证明的墙（T8）；击败它的知识 gap 实测高达 ~43%（T5）。
- **Q1b：需要超越-ICL 的系统，且必须是 new-info 杠杆 = 多模态外部知识记忆**——因为它是唯一能越过知识 gap 的类
  （T8），而该 gap 真实且大（T5）。**不是**自奖励（E10 已否）、**不是**转写注入（M3 撤回）、**不是**跨会话累积
  agent（7/03 关闭围栏）。其 training-free 可实现性是下一步方向性探针（T6），**建/不建的裁决是主人 Stage-1 检查点
  （T9）——本结论不自动滚入 Stage-2**。

**Why it matters.** 这是本弧线第 4 次过度伸张的纠正，且最深：前几次靠统计纪律（CI、E10b、M3 smoke 崩塌）抓住，
这次**只有任务定义/模态边界视角能抓**。准则现已成文（G0），成为一切杠杆的前置闸。分支未推送、wiki 待同步。
**Decision.** Owner reframe (2026-07-05): rather than *select* the good answer post-hoc (the (c) wall),
test whether **adjusting the conditioning A makes the good answer modal (greedy)**, training-free, on the
non-saturated zh+en surfaces, against a frozen relative +10% bar (prereg
[[2026-07-05-stage1-A-realization-prereg]]). **Ran:** P2 baselines (n=150; 4 non-sat surfaces, oracle-δ
+0.11…+0.28) → E7 multimodal few-shot ICL (owner's key lever), E8 in-fence prompt-opt, E10 generator/
verifier two context-differentiated systems (n=24–30). **Theory (machine-checked, full TfrlProofs builds
8570 jobs, sorry-free):** TH2a `BlindSpot` (two-system realization → oracle as blind-spot fraction → 0) +
TH2 `Reachability` (the (b) mode-shift + the (b)-cap — the "(b) has no theorem" gap now filled).

**Result / verdict (DIRECTIONAL NULL, Stage-1).** Under the frozen +10% bar **no in-fence lever realizes
the oracle-δ**: E7 never lifts greedy (and its ±0.033 deltas sit inside temp-0 decode noise), E8 +0.0%
(but it was a 4-candidate pick, not real OPRO/GEPA), E10 sub-threshold (SQuAD +5.6%, big-bench +8.3%). But
this **does not close Q1 or establish the agentic branch**, because it is under-powered (n=24, no CIs) AND
under-scoped — the decisive in-fence instruments (real OPRO/GEPA, M3 cross-modal injection, full
shot-curve, and an **on-surface self-selection control**) were never run. Returned to owner with those as
mandatory Stage-2 preconditions; no auto-rollover.

**Update — E10b de-confounder (n=40 + paired-bootstrap CIs) turns the null into a CLEAR verdict.** The
review's CRITICAL confound (no on-surface self-selection control) was then run: the two-system verifier
**never beats on-surface majority self-selection** (ver−maj = −0.075/−0.025/+0.000 on mmau/SQuAD-zh/
big-bench, all CIs cross/below 0; worse on mmau), so the "two-system positive seed" is **refuted**. Clear
answer now: **Q1a ICL is insufficient** — every cheap in-fence lever (prompt/few-shot/prompt-opt/
self-selection/two-system verifier) fails the +10% bar; **Q1b an omni agentic system is warranted ONLY if
it injects a genuinely new independent-of-M signal** (M3 cross-modal / new reward / W4 embedding) — the
internal-composition/self-verification route is refuted (E10b) and forbidden by `gain_product`. Two
Stage-2 tests remain to lock it: (a) real OPRO/GEPA (last cheap in-fence lever); (b) M3/W4 (first
new-signal lever). Artifact `_repro/e10b_control.json`.

**Update — M3 (first new-independent-signal probe, n=60 + CIs): MODEST/BORDERLINE, not locked.** Injecting
an independent ground-truth text transcript alongside the audio gives vocalbench-zh +20% (CI[0.0, 0.2],
lower bound at 0) and SQuAD-zh +4% (n.s.) — the **only** lever to show any positive, weakly supporting the
new-signal direction but not robustly confirmed. (A sharp lesson: the n=3 smoke showed SQuAD "+50%" — pure
noise, inverted at n=60; do not narrativize smokes.) So the new-signal/agentic direction is theory-supported
+ weakly-empirically-supported, **not yet earned**; Stage-2 = powered-n M3, W4 (independent-knowledge
signal), and OPRO/GEPA. Artifact `_repro/m3_crossmodal.json`.

**LOCK — powered M3 (n=150 + CIs) settles Q1b.** Re-run at n=150: vocalbench-zh **+22.4% SIGNIFICANT**
(CI[0.04, 0.16] excludes 0, clears the +10% bar); SQuAD-zh +7.7% n.s. So injecting a new independent-of-M
signal (a ground-truth transcript) **robustly realizes headroom that every internal ICL/selection/
verification lever could not** — the only lever in either phase to clear the bar with a CI excluding 0.
Interpretable: the transcript recovers **audio-perception loss** (benefit largest where audio-only is weak).
**Locked answer: Q1a ICL insufficient (robust); Q1b YES — design an omni agentic system as a
new-independent-signal injector** (internal composition/self-verification refuted by E10b + forbidden by
`gain_product`; new-signal route demonstrated by M3; theory-consistent with TH2a's shared-knowledge floor).
The branch (2.2/new-signal) is decided; Stage-2 **engineers** the produced signal (ASR self-transcription /
retrieval / **W4 omni-embedding** as the independent-knowledge signal, #37) and formally closes OPRO/GEPA.
**Meta-lesson (reaffirmed hard this session): I over-reached toward agentic 3× — each caught by the strict
review, the frozen +10% bar, paired-bootstrap CIs, the E10b de-confounder, and the M3 n=3→n=150 noise
collapse. The locked answer survived all of them.**

**RETRACTION (2026-07-05, owner — a 4th over-reach, deeper than the others).** The "M3 locks Q1b" above is
**WITHDRAWN.** M3 fed the audio PLUS **the test item's ground-truth text transcript** — an
**information-boundary violation**: deployment's omni input is *audio only*; a golden transcript doesn't
exist there, and if it did the omni model is pointless (you'd use a text LLM + ASR — negating the whole
premise). So M3's +22.4% is **input leakage**, same class as the retracted acoustic-oracle fraud — not a
valid lever. **Q1a STANDS** (no *valid* internal lever — few-shot/prompt/self-selection/two-system — realizes
the oracle-δ). **Q1b is REOPENED.** The legitimate path: a **multimodal MEMORY system** injecting *external*
knowledge keyed by the input, never the test transcript (design: [[2026-07-05-omni-multimodal-memory-design]]).
**Corrective (G0):** codified the **information-boundary guard** (every lever must pass: deployment has this
input? respects audio-only modality? no test-item leakage? real capability vs fed-answer). Re-graded: KEEP
P2/E8/E10/E10b (valid — own samples/prompt/label-free selection); RETRACT M3 (leakage); REDO E7 (few-shot
mis-designed: gave only the answer, not the task-handling pattern → T2). **Deeper meta-lesson: statistical
discipline (CIs, controls, review) did NOT catch this one — it took the owner's task-definition /
modality-boundary lens. Metric-chasing that leaks information the real task lacks is the classic multimodal
error; the guard now makes it a pre-flight check on every experiment.**

**Why (the strict review, again).** A 3-persona blind panel (methodology / devil's-advocate / EIC+formal)
returned **MAJOR REVISION** and was right — the v1 verdict over-reached toward agentic (same failure mode
as Phase-1). It caught: (i) **TH2 `Reachability.lean` did NOT compile** (Mathlib `div_lt_div_iff` rename)
— I'd falsely claimed it "machine-checked"; fixed to green (`lt_div_iff₀`/`div_lt_iff₀`). (ii) A **post-hoc
ρ≥0.3 threshold** (not in the prereg) manufactured "E10 clears"; under the frozen +10% bar E10 clears
nothing. (iii) The **"two-system > self-selection" causal claim is confounded** — E4's self-selection ≈0
was on MMAU; E10's positives on SQuAD-zh/big-bench-audio (zero overlap, no on-surface control), and on
MMAU the verifier was *worse* than greedy. (iv) E10 is a **branch-2.1 verifier/MBR selector**, not
"agentic" — its weak signal argues 2.1 is under-tested, not for 2.2. **Consequences.** The honest value of
this phase is a precisely-scoped directional null + the two machine-checked theorems + a pinned Stage-2
precondition list — NOT a build recommendation. Artifacts: conclusion (v2)
[[2026-07-05-A-realization-conclusion]], review [[2026-07-05-A-realization-review-synthesis]],
`_repro/{p2_baselines,e7_fewshot,e8_promptopt,e10_verifier,dec_synthesis}.json`,
`proofs/tfrl/TfrlProofs/{BlindSpot,Reachability}.lean`. **Lesson reaffirmed:** small-n directional
evidence + a preferred prior (agentic/2.2) reliably produces over-reach; the frozen bar + adversarial
review are what keep the conclusion honest.

### 2026-07-05 · Stage-1 Q1 directional finding (ICL-sufficiency for frozen-omni TFRL) — locked, strict-reviewed, then CORRECTED for over-reach; theory machine-checked in Lean
**Decision.** Executed the owner's `/goal`: run the planned Stage-1 experiments with full validation, lock
the research in paper form, prove the theory in Lean, and answer Q1 (is ICL sufficient for training-free RL
on a frozen omni's semantic layer; if not, design an omni agentic system?). **Experiments (all n=150,
frozen Qwen3-Omni-30B Q8_0 GGUF via llama.cpp, grade `[directional | single-touch | not
significance-bearing]`, artifacts in W1 `_repro/`):** E1 SLU text-prompt H_prompt−H_fix=+0.000; E3 SQA-MCQ
+0.020 n.s. with H_fix support +0.133; E4 (c)-realization — no cheap self-referential selector beats
majority (self-cert ρ=0.0, majority/conf-vote ρ=−0.047, self-judge ρ=0.143 n.s.); E6′ multimodal-b with a
FBank/MFCC feature-invariance audit. **Theory (machine-checked, `proofs/tfrl`, full TfrlProofs builds
sorry-free against Mathlib v4.31.0 bar the documented Beirami sorry):** new `Realization.lean` — C4 bound
`R(oracle)−R(selector) ≤ 2τ` + convergence theorem `realized_tendsto_oracle` (τ→0 ⇒ realized→oracle);
plus `gain_product`/`qstar_product` (context-isolated separable-reward agent composition is inert).
**Then ran a 4-persona strict review (methodology / domain / devil's-advocate / EIC+formal, blind, grounded
in the artifacts + Lean).** Decision: **MAJOR REVISION** — and the review was RIGHT.

**Why (what the review caught, and we corrected).** The v1 verdict ("ICL insufficient → build an agentic
system", VERDICT-LOCKED) over-reached on three counts: (i) **category error** — it conflated "cheap current
instruments don't harvest" with "the space is insufficient", when the text leg used *un-optimized*
hand-authored prompts (not the OPRO/GEPA optimized search — the survey's "central empty cell", unrun) and
the (c) leg used only *cheap self-referential* selectors (omitting the trained-verifier/MBR class the survey
says is the only in-fence winner); (ii) **its one affirmative result was an artifact** — E6′'s multimodal
+0.060 is 100% speed-driven (recomputed independently: oracle{original,trim}=0.640=greedy → **+0.000**),
because the time-averaged log-mel gate is length-robust by construction and can't see the temporal leakage
that ±10% speed introduces; (iii) it **locked a program decision on Stage-1 n=150 evidence**, which
CLAUDE.md says "can settle nothing." Formal nits too (an `iff` the theorem proves only forward; the
`spread²/8β` cap is hypothesis-gated like Beirami; `gain_product` over-generalized to license agent-building
when it only forbids *isolated* stacking and is silent on a non-isolated τ-reducing verifier).

**Corrected finding (v2, DIRECTIONAL — returned to owner, NOT a branch decision).** Real latent oracle
headroom exists (sampling +0.13) so the frozen model is not the bottleneck; but the *cheap/naive* ICL
levers fail to convert it — naive text-prompt diversity inert, cheap self-referential selection
under-harvests. **"The ICL optimization space is insufficient" is NOT established**, because the decisive
stronger in-fence instruments were not run (optimized prompt search; trained-verifier/MBR selector; M3
cross-modal injection; ≥2nd non-saturated surface). **The open problem is (c) realization.** The
omni-agentic question stays **open and is not forced by `gain_product`** (it forbids only naive isolated
stacking, not a non-isolated verifier — the very (c)-lever); both branch 2.1 (stronger in-fence selector /
optimized prompt search) and 2.2 (reward/verification expansion, behind the 7/03 closure fence, with a
C1–C4 convergence proof) are live and under-tested. **Consequences.** Number-tracing + Lean judged
exemplary/honest by the panel; the value of this campaign is a *corrected, precisely-scoped* directional
signal + a machine-checked realization theory + a documented next-probe list — not a program pivot. Artifacts:
conclusion [[2026-07-04-Q1-conclusion-ICL-sufficiency-omni]] (v2), review [[2026-07-05-Q1-conclusion-review-synthesis]],
framing [[Research-Question-Framing]], theory [[Theory-Convergence-and-Constraints]]. W1 commits (E1/E3/E4/E6′
`_repro/`); umbrella commits (Realization.lean + wiki). **Owner discussion selects the next probe; no
automatic rollover to Stage-2.**

### 2026-07-04 · Three-stage research methodology codified; Stage-1 problem-definition campaign for the semantic layer closes with a strict-reviewed survey and an owner-selected problem set
**Decision.** The owner judged the research insufficiently grounded and installed a **three-stage
methodology** (1 Problem-definition: survey-grounded argumentation, small-n only directional; 2
Solution-validation: large-sample pre-registered; 3 Publication) now in CLAUDE.md/AGENTS.md
(byte-mirrored). Under Stage 1, we ran a problem-definition campaign on the question: *from the ICL
perspective, is the instruct-prompt rollout optimization space of a frozen omni speech model
sufficient for the SEMANTIC layer (ASR/SLU/SQA/agentic)?* At the closing checkpoint (K2) the owner
selected **CP-1, CP-3, CP-8, and CP-4** to advance to Stage 2. Full record:
[[2026-07-04-stage1-problem-definition]] (K2-resolved), [[2026-07-04-stage1-semantic-tfrl-survey]]
(the reviewed survey), [[2026-07-04-sufficiency-yardstick-memo]], [[2026-07-04-stage1-evidence-regrade]].
**Why.** The prior arc was thesis→operator→mechanism driven, never problem-driven; the C1 pipeline
used one fixed instruction, so the owner's prompt-space question was never measured in-house. Stage 1
fixes the problem before spending Stage-2 sample budget.
**Consequences.** (1) **The honest Stage-1 answer:** sufficiency cannot be settled at Stage 1 — the
central cell (the *magnitude* of H_prompt − H_fix) is unmeasured for every audio-in model (in-house
zero; the text-domain APE/OPRO/GEPA quantification has no audio analog; PromptingWhisper is a
two-point existence-positive that bounds nothing). An operational yardstick (H_fix / H_prompt / ρ;
b1/b2 split; failure-routing) converts the question into ranked problems. (2) **Evidence re-graded**
under the Stage-1 lens: the NO-GO campaign's M3/M5 kills drop to `directional`; MInDS +0.126 and the
C1 headroom to `scoped`; the vector-class paralinguistic negatives stay `settled` — consolidated as
the premise that focuses research on the semantic layer (resolves the 2026-06-23 OPEN as full
semantic focus). (3) **A rigor chain executed with Academic-skills + Workflow (~40 agents):** 33
literature-anchored problems + 101 verified claims + a cross-domain (LLM/VLM/speech) transfer map;
one budget-matched directional probe [n=50] read Δ_BM ≈ 0 on ASR (a real error caught in review: it
measures Δ_BM, not H_prompt − H_fix); a 16k-word survey (171 refs) that passed a **/ars-reviewer
5-persona strict review** — MAJOR REVISION (no CRITICAL), 7 P1 + 14 P2 applied, re-review
all-P1-resolved (it also caught a confirmed SNR-sign error, +5 dB not −5, fixed across six docs).
(4) **Stage 2 opens with a fresh Research-Proposal-Template instance** per problem; suggested
cost-ordering CP-3 → CP-1(SLU/SQA)+CP-8 → CP-4; cross-session variants stay behind the r1–r3 closure
fence. Branch `research/stage1-problem-definition`, PR to master.

### 2026-07-04 · Step-1 rationality campaign ratified NO-GO — the agent-level question is CLOSED (pre-registered, measurement-backed, owner-gated)
**Decision.** The owner ratified the campaign's recommended **NO-GO** on question (ii) — *build an omni
agentic system (skills/memory/routing over frozen models) to extend training-free RL* — and declined the
elective safeguard-5 V4-amendment fork (rejected-with-reasons on futility grounds). The 2026-07-02
verdict stands, now upheld by the campaign's own pre-registered instruments, not review argument alone.
Question (i) — single-model TFRL as a direction — is **RATIONAL-AND-CONTINUING** via pivot **P-D**
(condition-mapping of the real C1 headroom). Full record: [[2026-07-03-omni-agentic-tfrl-go-no-go-decision]]
(owner_verdict stamped), pre-registration [[2026-07-03-agentic-tfrl-step1-preregistration]] (freeze b19bff2).
**Why.** Criteria frozen BEFORE analysis; null hypothesis = the 7/02 verdict; inconclusive = NO-GO. G1
failed arithmetically: **M3** (support expansion) was killed by its own Phase-0 zero-support check —
pooled entity-match **F = 0.38108 vs the frozen 0.01 kill threshold** (38×; train-960h rarity ≠ model-OOV:
the 30B's pretraining already emits the "rare" book entities); **M5** (selector accumulation) failed its
PASS bar with an exact zero (sel = MBR = 0.07722 on the designed 12×12 confirmatory surface) — with the
honest caveat that the frozen V1|0.05 selector was **pre-proven inert** (median flip-λ 60.5), so the M5 arm
closes by the frozen inconclusive→NO-GO default, *not* by empirical falsification of the mechanism class;
M2/M4 design-only and M1 unopened → default. Collateral finding: on the fresh slice MBR gains nothing over
greedy while oracle headroom is real (+0.0238) — deployable label-free capture ≈ 0%.
**Consequences.** (1) **Rigor chain:** 22-item objection ledger → 3 delta-scan lanes (33 verified claims;
re-open conditions r1/r2 re-verified EMPTY on decision day) → 4 blind constructor/refuter mechanism pairs →
2 pre-registered pilots with freeze-before-run commits (b19bff2→c8bebaf→d4dd117→1b53b46→f8ec1d3→d874585) →
6-charge hostile panel (both blind judges: all six stand) → mechanical synthesis + integrity check →
**/ars-reviewer 5-persona fresh-adversary panel: unanimous sound-with-corrections**, all 12 corrections
applied (per-lane reaffirmation attribution, GO-reachability statement, the elective amendment fork
surfaced at the gate), 12/12 memo censuses reproduced into `_repro/m5_memo_censuses.json`. (2) **The
converged paper's "deferred, not disproved" question now has a citable closure sentence** (decision doc
§10). (3) WF-2 (omni-agentic-system survey) NOT launched. Freed capacity → the W4 post-NULL queue + P-D;
a zero-cost standing r1 monitor (re-run the D2 negative-finding searches periodically). (4) Re-open only
on r1 (public cross-session same-speaker corpus) / r2 (peer-reviewed non-separable decomposition bound) /
r3 (a lane kill overturned by literature); an acknowledged coverage gap — no re-open path for in-house
successor evidence — is recorded for owner-level amendment if ever desired. (5) Campaign mechanics:
Workflow orchestration + academic-research-skills (research_architect / report_compiler / /ars-reviewer),
~100 agents, ~1 day wall-clock, ~9 h GPU, all on the single 24 GB 5090. Branch
`research/agentic-rationality-step1`, PR to master.

### 2026-07-03 · Publication closed out; assets/docs reconciled to reality; inference-engine decision recorded
**Decision.** Closed every dangling item from the W5 arc in one pass. (1) **Publication:** PR #2 (the
whole 6/26→7/02 arc) was merged by the owner on 2026-07-02; today the local master was fast-forwarded,
the wiki synced — which **removed the stale, mis-attributed 2026-06-25 "Operator-B best-of-N" draft
from the public wiki** (it described the int4/HF path, placeholders unfilled) — and the merged branch
deleted. (2) **Toolchain committed** (`87154b9`): env-setup Phase 5 (bitsandbytes + cmake/ninja +
llama.cpp CUDA build, sm_120), the file-selective GGUF fetch script, and
`speechrl_common.models.generative_omni` (a committed W1 script imported it while it sat untracked);
`main.bbl` rebuilt to the converged round-4 source (`5f5cfce`); the failed vLLM runner
(`repro_asr_best_of_n_vllm.py`), the stale 6/25 draft, and the 6/25 TODO note retired. (3) **Lockfile:**
the Qwen3-Omni GGUF (Q8_0 + bf16 mmproj, 32.3G) added as the **6th frozen model** — new source kind
`hf-manual` (file-selective; the whole-repo pull >110 GB is deliberately avoided), dispatch added to
`fetch-data.sh`, regen-stable mappings to `gen-lockfile.py`; totals 408.7G→441.0G. (4) **Docs corrected
to reality** (~13 files): the real WSL distro is **`Ubuntu-24.04`** (the machine's default `Ubuntu` is
WSL1 — no GPU), the real data root is the **repo-root `speechrl-data/` on the Windows drive**
(`/mnt/d/…`; ext4 `~/speechrl-data` holds only `mlruns`), totals ~410→~440 GB. (5) New
[[Inference-Engine-Choice]] records the measured engine decision (llama.cpp proven — produced W1
`f9d111a`; vLLM/transformers version pairing deferred to W2); [[Per-Work-Status]] refreshed (W1 genuine
best-of-N, the emotion NULL correction, the converged cross-work paper).
**Why.** No dangling state: every number's engine and model must be reproducible from the frozen
manifest, and operating docs must match the measured environment — the 6/26 "R1 unprovisioned" verdict
came from probing the wrong distro and the wrong data path.
**Consequences.** This corrects the 2026-07-02 entry's closing status: the branch IS pushed/merged and
the wiki IS synced. The lockfile is authoritative including the GGUF, and a regeneration now reproduces
its entry. Deliberately deferred: the vLLM version pairing (W2), and the open research moves — the
label-free selector for the realized-vs-headroom gap, the pre-registered H1/H2/H3 pilots (env now
unblocked), W4's post-NULL experiment queue — which await prioritization.

### 2026-07-02 · Deep principle/purpose/feasibility review collapses W5, then a REAL best-of-N (llama.cpp) earns it back — converged as an honest single-model paper
**Decision.** The owner judged the prior review still too shallow (syntax/semantic, not **原理/目的/可行**), and asked
for a genuinely adversarial review run as a **POMDP** (step-by-step, partial observation, iterate + roll back). Three
independent hostile expert reads (principle · purpose · feasibility) reached a conclusive verdict: **the agent-level /
L4 framing does not survive** (the OSA theory is tautology-where-proven — `qstar_product` = `exp(a+b)=exp(a)exp(b)`,
smoking gun in `OptSpace-notes.md` — and unmodellable/untested where interesting; the purpose is self-refuting with
VoI≈0; the cross-session benchmark data is frozen-absent and the stack unbuilt). Owner chose **Option A: collapse to
an honest single-model paper.**
**Why.** Follow the evidence even to restructuring; the direction itself was challengeable; substance over prose;
bounded local GPU pilots authorized.
**Consequences (the POMDP trajectory, full log in `papers/agent-level-tfrl/reviews/pomdp-restructure-log.md`).**
(1) **A forensic provenance pilot** found the paper's content/intent "Operator-B best-of-N" numbers were actually a
frozen **bi-encoder cosine retrieval** — a real mis-attribution the earlier 4-round review missed — and re-ran MInDS
to a committed paired-CI artifact. (2) Collapsed 57→21 pp; committed a precise **paralinguistic negative** probe
(speaker 3×-chance, emotion 2.4×-chance, null training-free gain). (3) **A fresh hostile panel then found a
fundamental flaw even in the collapse:** the omni-embed "selection" never used the reward (argmax cosine, not
reward-driven) — so it was *not* training-free RL at all. (4) Owner chose **Path B: earn the RL claim with a real
best-of-N.** The HF/vLLM int4 loader wall was hit; owner steer **"run the 30B via llama.cpp"** unblocked it.
(5) **Genuine training-free RL, executed:** Qwen3-Omni-30B-A3B (Q8_0 GGUF, llama.cpp, resident server, `-ngl 28` on a
24 GB laptop 5090) samples N transcripts per LibriSpeech-test-other+snr5 utterance; a verifiable WER reward selects.
**Multi-seed (3 generation seeds pooled, n=144): oracle-WER best-of-N headroom +0.042 [0.029,0.056] at N=8,
significant from N=4 (N=1<greedy — the honest order-statistics climb); deployable label-free MBR non-significant at
every N** — a real reward-driven headroom + an honest realized-vs-headroom gap. (6) Reframed the paper: **C1** = this
genuine best-of-N; **C2** = honest frozen-encoder probing (distinct operator, not RL); **C3** = a reward-spread lens
giving only the *sign + ceiling* (the N-curve is order statistics), two `sorry`-free Lean lemmas. (7) **Four fresh
hostile rounds on the reframed paper converged: fundamental → major → major → minor, 0 surviving fundamental/major;**
an integrity reviewer reproduced every C1 number against the committed artifact to the digit. **Verdict: CONVERGED.**
Every number backed by a committed reproducible artifact (best-of-N in the W1 repo; probes in the W4 repo). New tool
capability proven: **llama.cpp drives Qwen3-Omni-30B audio ASR + best-of-N on the 24 GB laptop GPU** (audio flagged
experimental upstream). Commits: W1 `b7b4b0d`/`cd6aa92`/`f9d111a`; umbrella `dff7628`→`20a6a31`→`b03c091`→`67b377d`→
(round-4). Branch `docs/research-proposal-template-and-first-proposal`, not pushed; wiki not synced.

### 2026-07-01 · W5 proposal hardened by a rigorous FOUR-ROUND fresh-adversary review (substance-only fixes; converged at the pre-registered cap)
**Decision.** The owner judged the first review pass (the entry below) **not rigorous** — one revision cycle, same
reviewers primed on their own lists, a meta-reviewer that once returned placeholder output, and several items
patched *in prose*. We re-ran the review as a **multi-round adversarial loop** with a hard discipline: **fresh
reviewers each round** (blind to prior rounds and to the resolution ledger), a **meta-chair** holding the only
ledger and reporting solely *genuinely new* critical/major, **fix in substance not prose** (strengthen via
Lean/GPU-experiment/citation — or cut), and **loop until a clean round, cap 4**.
**Why.** A proposal that stakes its credibility on machine-checked honesty must survive independent attack, not a
single self-consistent pass; prose hedging is not a resolution.
**Consequences.** (1) **Four rounds ran; the defect class shrank monotonically and terminated at the cap:**
R1 (6 critical + 11 major — the *structural* over-claim: the "single-model inert → agent **recovers**" thesis was
**unsupported by the theorems** — `qstar_product` proves the isolated optimum *equals* the monolithic one — and
**contradicted by our own data**; whole paper reframed, title changed, system demoted to a **testbed**) →
R2 (13 major — the reframe hadn't propagated to the most-read sections; KL-direction, front-matter, emotion
statistic all re-synced) → R3 (0 critical, 4 major — β-convention in Related Work, the Lean status-table `sorry`
location, the PLDA-calibrated falsifier, proposal framing) → **R4/cap** (0 critical, 7 major — all
internal-consistency / fidelity / **artifact-integrity**: C1's Pinsker/Beirami/Hoeffding mapping, pre-correction
Lean docstrings, the affect baseline upgraded to a classical online CPD, a per-factor win criterion, a byte-verbatim
appendix signature, and — caught by a blind auditor — the committed emotion t-CI being **hand-inserted rather than
script-emitted**). Every round's panel certified, from R1 on, that **no theorem is wrong and no proof is broken**.
(2) **Substance, not prose, throughout.** New sorry-free Lean lemmas `gain_pos_of_nonconstant` / `kl_pos_of_ne`
(strict Gibbs) added in R1 and re-verified after each Lean edit (`lake build`, 8559 jobs, sorry-free bar the one
documented Beirami `sorry`). The load-bearing emotion result was **re-run on the RTX 5090** and turned out to be a
**NULL** (across-seed 95% t-CI **[−0.043, +0.116]** spans 0), not the originally-claimed +0.097 (a single-seed
oracle-test-layer artifact) — an honest scientific correction; in R4 the reproducer was fixed to *emit* that t-CI
and re-run so the committed JSON is genuinely script-produced. (3) **The thesis is now honest and precisely scoped:**
theory (gain governed by reward *spread*, not search effort or agent wrapping — the isolation result is an
*accounting identity*), a scoped paralinguistic **NULL**, single-model best-of-N content/intent gains explicitly
*not* evidence for the agentic claim, and a testbed + pre-registered falsification plan whose central question —
does agentic decomposition add anything beyond a frozen single model — is **disclosed as open** (a *proposal*, not
an executed result). 57 pp, compiles clean (0 undefined). Six review archives + a resolution `ledger.md` under
`papers/agent-level-tfrl/reviews/`. Commits: umbrella `70b5aef` (R3), `c2481b4` (R4); W4 `dd6e8d3` (re-run artifact).
Branch `docs/research-proposal-template-and-first-proposal`, not pushed.

### 2026-07-01 · W5 agent-level proposal written as a peer-reviewed LaTeX paper (42 pp, 217 refs, 5-role review → minor revision)
**Decision.** Consolidated the W5 agent-level arc into a rigorous, English, NeurIPS-style **LaTeX research
proposal** at `papers/agent-level-tfrl/` (`main.tex` + `references.bib` + modular `sections/`), compiled to a
42-page `main.pdf` on a user-space TinyTeX install in WSL2. It folds together the optimization-space-adequacy
theory (OSA-1/2/3, machine-checked in `proofs/tfrl/TfrlProofs/OptSpace.lean`), the convergence analysis, the
feasibility case (open moat + two-omni component pairing + the verifiable-reward acceptance gate), preliminary
in-house results, the self-evolving omni speech-agent system design, and the staged research plan. Drafted via a
parallel section-writer workflow; bibliography (217 adversarially-verified sources) generated deterministically.
**Why.** The owner asked for a paper-grade, peer-review-ready write-up (≥30k tokens, full citations + detailed
proofs + why/how) produced with multi-role adversarial review and a review→revise→re-review loop.
**Consequences.** (1) **Peer-review loop ran to its target.** A 5-role panel (theory-critic · statistician ·
speech-domain · reproducibility-auditor · novelty/red-teamer) + area chair returned **major revision** in round 1
— the math was verified correct on disk (Lean pins, one documented sorry) but the prose over-claimed. A
per-section revision workflow applied the must-fix items (OSA-2 downgraded to *conditional* additivity + an
explicit Phase-2 spread-floor **conjecture**; the dual-use key-agreement reward **reclassified as a surrogate**,
not verifiable per the paper's own definition; "asymptotically inert" → "gain bounded by realized reward spread";
"machine-checked" **qualified** to the sorry-free qualitative core vs the conditional quantitative bounds;
convergence reframed as a **design principle**, finite-time guarantee open; single-seed / winner's-curse /
contamination caveats; citation softening). Round 2: **all five reviewers moved to minor revision**, gating items
resolved; residual M8/title fixes then applied. Reviews archived under `papers/agent-level-tfrl/reviews/`.
(2) The paper is **honest by construction**: novelty framed as domain-transfer (mechanism not novel), the one Lean
`sorry` + the isolated Hoeffding lemma disclosed, agentic recovery (OSA-2) explicitly *not yet measured* (Phase-2).
(3) Reproducible build shipped (`build.sh`, `_build/` generators). (4) **Survey-first still honored** — Project-Thesis
and the W4 H1/H2/H3 untouched; this is a proposal, not a thesis change. (5) Branch
`docs/research-proposal-template-and-first-proposal`, not pushed.

### 2026-06-30 · Agent-level direction (survey-first POMDP): GO verdict + the optimization-space theorem machine-checked in Lean
**Decision.** Pursued the owner's strategic pivot — *is the L4-evolution space agent-system-level no-gradient RL
(skills+memory) rather than single-model output search?* — as a **survey-first POMDP** (Belief-State + Trajectory
in [[2026-06-30-agent-level-synthesis]]). **S1** (decisive probe, 41 verified claims) returned **GO** at
commit-degree *add-new-layer*, scope *speech-grounded*: agent-level self-improvement **compounds**
(Voyager/ExpeL/AWM/JitRL), the `q*` objective **extends** to agent actions (JitRL closed form), the two omni
classes map to **memory(embedding)/policy(generative)**, and the **training-free self-improving SPEECH-agent moat
is open** — but the *mechanism* is not novel, so it's a new layer, not a thesis reframe. Then formalized the
owner's **optimization-space-adequacy** hypothesis in Lean (`proofs/tfrl/TfrlProofs/OptSpace.lean`, extends
T1/T3): **OSA-1** flat/degenerate space ⇒ zero gain (recovers T3) + quantitative `gain ≤ spread²/(8β)`; **OSA-2**
context-isolated agents ⇒ **additive** gain; **OSA-3** rollout deficit + credit-assigned tilt = global optimum.
`lake build` **green, sorry-free**. Grounded by a convergence survey (θ2, 43 claims / 54 sources,
[[2026-06-30-survey-agent-convergence]]): proven *finite-N* convergence lives at the **output** level; the agent
level has only JitRL's *asymptotic* consistency under a **trust-region/slow-drift** precondition — the trust
region being the hinge between naive non-convergence and credit-assigned convergence.
**Why.** Owner: optimizing a single model's instruct/output is too small a space; bring it into an agent system
(context isolation + skills/memory) to enlarge the optimization space — but then rollout-stability/convergence
needs algorithm-level care. Prove this formally and survey the latest open-source training-free-RL convergence.
**Consequences.** (1) **Survey-first honored:** [[Project-Thesis]] and the W4 proposal's H1/H2/H3 are **unchanged**;
the GO + commit-degree is a deferred decision for the owner. (2) The optimization-space hypothesis is now a
**machine-checked theorem suite** (axis B8 resolved). (3) Two survey rounds archived under `wiki/survey/` with
real verifiable links (S1 + θ2 convergence). (4) Lean toolchain provisioned on this machine (elan + mathlib
cache); the W4 proposal's empirical/GPU track stays blocked on R1. (5) Branch
`docs/research-proposal-template-and-first-proposal`, not pushed.

### 2026-06-26 · First research proposal authored as a POMDP step-by-step build; Step-2 survey archived (93 verified sources)
**Decision.** Authored the first proposal on the new [[Research-Proposal-Template]] —
[[2026-06-26-training-free-rl-for-speech-omni-research-proposal]] — for the owner's idea: *how far can
training-free RL activate pretrained omni-model capabilities across the two model classes (vector/embedding vs
thinker-talker/generative), with in-context conditioning (explicit task definition + few-shot) as the lever.*
Built it explicitly as a **partially-observed decision process (POMDP)** — a live Belief-State table + a
Trajectory log, each step a committable/rollbackable action ordered by value-of-information — rather than
one-shot. Ran the **Step-2 survey** as a 5-lane multi-agent workflow (`wf_d76b4901-23c`) with per-lane
adversarial source verification; archived **80 verified claims / 93 real http-linked sources** under
`wiki/survey/` (index `survey/README.md`). Pre-registered the proposal to **v1.0** (§1 hypotheses, §2 per-family
δ/α + go/kill/pivot + mandatory controls, §5(T) theory, §6 risks all FROZEN before any pilot).
**Why.** First real exercise of the template; the owner asked for broad capability coverage (sampled dev/test),
thorough survey + reproduction with a technical-principle/scheme emphasis, local models only (Qwen3-Omni-30B-A3B
via llama.cpp), and a step-by-step iterative build.
**Consequences.** (1) **Central falsifiable claim H1** — model-class asymmetry of ICL activation: reward-selected
in-context conditioning activates an under-exposed capability on the generative class but not the vector class
(label-free contrastive bi-encoder) — plus H2 (presence map + activation order content/intent ≥ emotion ≥
speaker) and H3 (task-def vs demos vs instruction richness; label-sensitivity as the cross-class diagnostic).
(2) **Step-1 feasibility probe → R1 blocker:** the WSL compute env on this machine is **unprovisioned** (no GPU /
CUDA / uv / `~/.venvs/speechrl`, `~/speechrl-data/{models,datasets,repos}` empty, no llama.cpp; only system
py3.14) — so the **empirical track (feasibility round-trip + all pilots) is BLOCKED-pending-provisioning**; the
prior experiments ran on another host. llama.cpp's Qwen3-Omni audio path itself IS supported (libmtmd, verified).
(3) **Survey refined H1 (partial rollback):** on the generative class naive few-shot demos mostly fix *format*
not task accuracy (ALICE, arXiv:2603.20433), audio LLMs "read not listen" (VoxParadox, 2605.27772), and speaker
resists even on (B) (2603.10827) — so the lever is **explicit task-definition + reward selection**, not raw
demos; added §6 controls (random-reward null, cross-model sign-consistency, acoustic-grounding). The survey also
**corrected an in-house citation** — LEACE is arXiv:2306.03819 (the feasibility doc's `2104.01767` is
WhiteningBERT). (4) v1.0 is **pre-registered and compute-ready**; only the empirical track remains, gated on
provisioning. (5) Survey synthesis agent hit a transient 401 mid-run; synthesized in-loop from the verified lanes.

### 2026-06-26 · Research Proposal Template rewritten: pre-registration form with a two-tier theory/effectiveness gate
**Decision.** Reviewed the lightweight `Research Proposal Template` (multi-agent workflow: 6 review
dimensions + adversarial synthesis, grounded in the NeurIPS reproducibility checklist / Registered
Reports / ACM artifact badging / Gorman-&-Bedrick / Kapoor-&-Narayanan AND our own W4 docs) and
rewrote it into a **portable (project-agnostic) 9-section pre-registration form**, delivered as
**paired monolingual EN / 中文 docs** (`Research-Proposal-Template.md` + `Research-Proposal-Template_CN.md`,
cross-linked, per the repo's README/CONTRIBUTING `_CN` convention). Its core is repo-independent; the
W1–W4 framing, repo wikilinks, lockfile/tracker, and wiki-sync hooks live only in a clearly-**optional**
"wiring into a project knowledge base" footer: front-matter →
falsifiable hypothesis → pre-registered success/kill/pivot criteria → survey & positioning →
reproduced results (baseline + method pilot, with a Repro Manifest, locked-test/anti-gaming guards,
and an operational 三方检测 definition) → two-tier theory/effectiveness gate → risks/ethics/data-
governance → decision & outcome → AI-tools-&-verification table. Renamed the file to the dashed
wikilink convention ([[Research-Proposal-Template]]) and linked it from the sidebar.
**Why.** The template's rigor bar was right but lived *implicitly*, so it depended on the reader and
eroded across works. Two self-inflicted flaws: (1) old requirement #3 demanded a mathematical proof
of *effectiveness* — a category error for an empirical thesis that contradicts our own feasibility
doc ([[W4-Training-Free-RL-Feasibility]]: the operator is proved; the P/L/S effectiveness conditions
are "to verify empirically"); (2) section order (Reproduced Results before the proposal) + no
pre-registered kill-criteria invited HARKing (author the hypothesis after seeing the numbers).
**Consequences.** (1) Requirement #3 is now a **two-tier gate** — (T) operator convergence/
well-posedness (a written justification with stated assumptions suffices; Lean only for finitary
theorems) and (E) a pre-registered *empirical* effectiveness criterion; effectiveness is measured,
never proven. (2) The falsifiable hypothesis + success/kill/pivot criteria are committed **before**
the pilot. (3) New required fields lift existing team practice into the form: Repro Manifest,
locked-test-set / selection≠metric / full-sweep guards, paired-bootstrap-CI stats, a logged
independent 三方检测 (a different teammate **or** an AI agent, from a clean checkout), a 3-line
ethics/licensing field (voiceprints = biometric, SER = affective), and an AI-output verification
table (anti-hallucination). (4) Over-engineering deliberately rejected to keep it a tight fill-in
form: ACM badge tiers, a formal in-principle sign-off gate, full datasheets/model-cards per study,
an NSF budget section, blanket multiple-comparison correction. **Not yet published** — run
`scripts/wiki-sync.sh` to publish to the GitHub Wiki.

### 2026-06-25 · Cross-team synthesis closes the goal: SLU/Spoken-QA/SER gains, independently reproduced
**Decision.** After pushing the 2026-06-24 work, discovered the collaborator ("codex" team) had pushed a
large frozen-model **policy-surface** Operator-B line to the W4 remote (CoVoST2/FLEURS translation,
HeySQuAD/URO QA, SLURP/MInDS tool-intent, AISHELL/Wu routing + `docs/lean/` guardrail proofs). Rebased our
loader commit cleanly on top (W4 `452bd8b`), then **synthesised both teams' evidence into one goal
close-out** ([[2026-06-25-cross-team-synthesis-semantic-tasks-tfrl-feasibility]]) and **independently
reproduced** the recognized-source MInDS-14 SLU gain on GPU.
**Why.** The owner goal asks for feasible sample-level training-free-RL gains on mainstream semantic
tasks (ASR/SLU/Spoken-Agentic) + Lean convergence + *adversarial* proof the gains are real. The
collaborator's policy-surface (instruction/wrapper/route/rerank selection over a frozen omni model) is
Operator-B training-free RL at the interface granularity — the same `argmax_z E[R(z)]` our Lean T1/T4
formalize — so the two lines compose into the goal rather than competing.
**Consequences.** (1) **Goal MET.** Frozen-model, paired-CI, recognized-source gains: SLU SLURP
0.550→0.880 (+0.330), MInDS-14 0.883→0.972 (+0.089); Spoken-QA URO 0.380→0.715 (+0.335) + conservative
rerank →0.845 (0 regr); emotion/SER +0.097 (our Operator A). (2) **Independent reproduction** on our GPU
(`speechrl-data/_repro_minds14_toolintent.py`, our `data_minds14` loader + the collaborator's
`evaluation.tool_intent`, seed 42, n=182): raw-schema 0.852 → policy **0.984**, Δ+0.132 CI [0.082, 0.187],
1 regression — same sign/significance as their +0.089, confirming realness. (3) **Convergence** backed by
our `proofs/tfrl` T1–T6 + their `docs/lean/conservative_rerank_gate.lean` (no-regression iff accepted
overrides correct) which composes with T1/T4. (4) **One blocked leg:** token-level generative best-of-N
(our 5 local generators incompatible with transformers-4.57/vllm-0.14) — mathematically validated,
empirically deferred to a stack bump; the collaborator's policy-surface Operator-B uses the frozen
*embedding* model, so the Operator-B goal leg is met at selection/rerank granularity. Large-scale still
deferred (validation-only): gated on the emotion-gain significance upgrade, a larger HeySQuAD locked test,
and the generator-stack fix.

### 2026-06-24 · Training-free RL validation run (waves 0–4): emotion gain + Lean convergence + Operator-B blocker
**Decision.** Ran the validation-only wave suite on the rebuilt GPU env (RTX 5090). Validated training-free
RL **Operator A** (frozen omni-embed disentanglement) across factor families and **proved the convergence
theory in Lean 4**; archived everything to the wiki ([[2026-06-24-tfrl-validation-run-log]] + 3 dated
per-experiment docs with 5-role adversarial challenges).
**Why.** Owner goal: feasible sample-level training-free-RL gains on mainstream semantic tasks, with Lean
math-convergence proof and adversarial validation of the gains.
**Consequences.** Results: (1) **emotion/SER gain Δ+0.097** (mean→attentive pooling @L16) — a real
training-free Operator-A gain (scoped: CI-separation marginal at test=300, queue dev-selection+paired
bootstrap). (2) content exposed (~1.0), intent present-but-not-steerable (~0.25, no pooling gain),
speaker suppressed (~0.04) — consistent with the disentanglement thesis. (3) **Lean** `proofs/tfrl/`:
T1 tilting, T3 flat-reward no-go, T4 plurality, T5 MBR-SLLN, T6 regret-O(√log N) **proved sorry-free**;
T2 KL-bound proved modulo one order-statistics `sorry` (`lake build` 8566 jobs). (4) **Operator-B
generative best-of-N (ASR/SLU/agentic) BLOCKED** — all 4 downloaded generators incompatible with
transformers-4.57/vllm-0.14 (minicpm-o-4.5: vllm only 2.6 + audio-encoder bug; qwen3-omni: needs newer
transformers processor; moss-audio: no modeling code). Fix: bump transformers/vllm or use a
Qwen2.5-Omni/Qwen2-Audio checkpoint. New reusable code: `common/rl/decode.py`, `data_minds14/librispeech`,
generalized `eval_harness`, intent/lid conditionings; env-setup gap fixed (sentence-transformers/sklearn/
sacrebleu). Large-scale deferred pending the emotion-gain significance upgrade + the Operator-B stack fix.

### 2026-06-24 · Dataset set frozen to a lockfile; downloads unified into one script
**Decision.** Froze the dataset/model set to exactly what is on disk and recorded it in a single
committed manifest, `docs/datasets.lock.json` (28 datasets + 5 models + 7 ref repos, each with its
source id and a pinned revision — HF/git commit shas where recoverable, ModelScope `master` else,
content-fingerprinted as a fallback), generated by `scripts/data/gen-lockfile.py`. Replaced the split
download path (umbrella `scripts/data/*` + the W1 `wave0_fetch.sh` engine + one-off
`fetch-semantic-modelscope.sh`/`fetch-semantic-manual.sh` + `campaigns/`) with **one self-contained,
lockfile-driven downloader**, `scripts/data/fetch-data.sh`, that any collaborator runs to reproduce the
identical set. It preflight-checks its dependencies and offers `--install-deps` (lightweight: hf +
modelscope CLIs + aria2) alongside the full `scripts/env-setup.sh`. Deleted the placeholder/partial
stubs (`voxceleb`, `cvss`, `speech-commands`, `minds14-xtreme_s`) and removed `voxceleb` from the
registry. Reconciled docs to reality: `fleurs` → `fleurs-r`, real per-dataset HF sources, and the
total `~281 GB` → `~410 GB` across all 13 places it appeared.
**Why.** The on-disk set had drifted far past the docs (a semantic-task campaign added ~17 datasets
that only `wiki/Speech-Semantic-Task-Datasets.md` knew about), and the download logic was fragmented
across two repos — so collaborating teams could not reliably reproduce the same data. A single manifest
+ a single downloader makes the set explicit, version-pinned, and reproducible cross-team; pinning HF
commits removes "latest drift" between teams.
**Consequences.** `docs/datasets.lock.json` is now the source of truth; change the set only by
regenerating it deliberately. `wave0_fetch.sh` (W1) is retired and its README/Per-Work-Status updated.
SLURP audio lives at `repos/slurp/scripts/audio/{slurp_real,slurp_synth}` (Zenodo 4274930), linked from
`datasets/slurp`. `seed-tts-eval` + `aime24/25/26` are kept but flagged `modelscope-manual` (their
evalscope ids weren't recoverable from disk — fetch manually). `env-setup.sh` now also installs the
download CLIs; `wsl-setup.sh` installs `aria2`. Speaker-ID is exercised via CREMA-D now that VoxCeleb
is gone. `DatasetSpec` gained a `revision` field. Publish via `scripts/wiki-sync.sh`.

### 2026-06-23 · Catalog extended — recent (2024-2026) speech-agentic + speech-retrieval datasets
**Decision.** Extended [[Speech-Semantic-Task-Datasets]] with two web-verified recency batches (workflow
`wf_b4eb417e-fe1`, 11 agents, 55 candidates → 12 core, **0 hallucinated**): (a) **speech-agentic
2024-2026** — VoiceAssistant-Eval, VocalBench-zh, Audio-MultiChallenge, SoulX-Duplug-Eval (bilingual
full-duplex), EVA-Bench, tau2-bench(voice); (b) **speech-retrieval** (the bi-encoder's *native* eval
surface) — MAEB + MSEB/SVQ (primary), FLEURS-Retrieval, SLUE-SQA-5, WavCaps, SpeechBrown. Both fetch
scripts updated with the OPEN sets.
**Why.** The flagship is a frozen retrieval bi-encoder, so MTEB/MSEB-style audio-embedding benchmarks
(MAEB, SVQ) are the most *direct* way to score it; the agentic batch fills the generative/behavioural axis.
**Consequences.** ModelScope reality persists — only `evalscope/tau2-bench-data` is hosted there; the rest
are hf-mirror-only. Flags: VoiceAgentBench / RealTalk-CN **gated**; WavCaps academic-only + 820 GB (out of
script); SpeechBrown synthetic-TTS (verify id). MAEB (arXiv 2602.16008) ≠ MSEB (arXiv 2602.07143) despite
similar names. Next: run **MAEB + MSEB/SVQ on omni-embed-nemotron-3b** as the semantic-eval starter.

### 2026-06-23 · Pivot toward semantic tasks (omni-embed is semantic-specialized) + public dataset catalog
**Decision.** The flagship omni-**embedding** (`omni-embed-nemotron-3b`, contrastive InfoNCE bi-encoder →
one pooled 2048-d vector) is **semantically specialized** (content ≈1.00, language/intent strong, emotion
≈0.40, speaker ≈0.04), so we lean onto the semantic axis it is *measured*-strong on: **SLU / Spoken-QA /
Speech-Translation / speech-agentic**, and curate a verified public dataset set for it (new
[[Speech-Semantic-Task-Datasets]]). Adversarial caveats kept on the record: "only semantic" overstates
(partial emotion retained); the verdict is scoped to the embedding/retrieval class, **not** generative
omni; this is *complementary* to the disentanglement thesis (content/language were always Operator-A
native), not a reversal. OPEN: full pivot vs. a second track (affects breadth-vs-Spoken-QA-depth in the
starter set).
**Why.** [[Paralinguistic-Suppression-Survey]] established that fine speaker-ID is destroyed and emotion
only partially recoverable in the pooled vector; the high-fidelity, native axis is semantic. Playing to
that measured strength is the highest-confidence near-term use of the frozen embedding.
**Consequences.** New [[Speech-Semantic-Task-Datasets]] (16 core datasets across 4 families;
adversarially link-checked — **0 hallucinated, 0 gated**; license/source flags recorded). New umbrella
scripts `scripts/data/fetch-semantic-modelscope.sh` + `fetch-semantic-manual.sh` (`--list`/`--dry-run`,
user runs them). **ModelScope reality (web-verified):** only VoiceBench (`lmms-lab/voicebench`) + FLEURS
(`pengzhendong/fleurs`, already local) are on ModelScope; everything else goes via hf-mirror or direct
(SLURP→Zenodo 4274930, STOP→dl.fbaipublicfiles.com/stop). Minimal starter = VoiceBench + HeySQuAD (2 new
fetches; CoVoST2/FLEURS/MINDS-14 already local). Next: a semantic-eval harness (retrieval/probe +
generative readout) on the starter set — the positive complement to the survey's speaker/emotion negatives.

### 2026-06-23 · Paralinguistic-suppression survey (D2) + pooling-method probe (D3) — emotion routing upgraded to "Operator A with a richer readout"
**Decision.** Two converging results refine the per-factor routing. **(D3, own run)** a weight-free
pooling-METHOD sweep (`scripts/pool_method_probe.py` + `layer_probe.extract_pooled`; CREMA-D, seeds 42
& 7) shows **mean = std = stats** (no gain), while a **weight-free attentive-statistics pool at mid-layer
L16 modestly lifts emotion** (0.40 → 0.51 seed-42 CI-separated, → 0.45 seed-7 CIs overlap) and **speaker
stays floored (≤0.067) across every method × layer × seed**. **(D2, 77-agent 3-vote-verified survey,
`wf_6694eca5-de9`)** the assertion "omni models lose paralinguistics at pooling" is **right in direction,
too strong in mechanism, and sharply per-factor**: paralinguistics is **suppressed/unread at the
pooled-vector + decoder readout, not destroyed** (final-layer probes still 3–55× chance); the single
masked-mean vector is **near-degenerate** (per-frame outputs cos~0.98 to the LLM mean token), so the big
emotion lever is an **ordered-trajectory / multi-vector readout** (C-Gate 16.8→77.7%, +61pp) not a smarter
single vector; **fine-grained speaker-ID is never written to the output** and is recovered **only** by an
external speaker encoder (ECAPA-LLM 1.03% EER) or a disentangled codec — both non-training-free. Net:
**emotion → Operator A is viable but needs a richer readout (multi-vector/trajectory/layer/generative)
before B; speaker → Operator B / external-channel (the natural boundary of the training-free thesis).**
Full evidence + citations: [[Paralinguistic-Suppression-Survey]].
**Why.** D3 supplies the **mean-vs-stats-vs-attentive ablation the literature lacks** (the two dedicated
layer-wise omni studies use mean pooling only); its modest single-vector emotion gain + floored speaker
match D2's mechanism exactly. D2 corrects the earlier "emotion → B or accept ~0.40" by separating *info
present-but-unread* (emotion, fix the readout) from *info never written* (speaker, fix the source).
**Consequences.** New durable [[Paralinguistic-Suppression-Survey]] (D1 injection mechanism verified:
51-token sequence in, pooled 2048-d out; D2 C1–C5 verdicts + 6-class fix taxonomy; D3 table). New W4 code:
`layer_probe.extract_pooled` (mean/std/stats/attentive, weight-free) + `scripts/pool_method_probe.py`
(MLflow `2c61b2f1` seed42, `21453cb1` seed7). [[Per-Work-Status]] emotion verdict updated. Next
experiments: (1) strict same-audio SSL baseline (emotion2vec/WavLM/ECAPA on the CREMA-D split), (2) a
multi-vector / ordered-trajectory emotion readout, (3) emotion2vec-fusion (emotion analogue of ECAPA-LLM),
(4) the W1→W4 RL-on-speaker bridge (PALLM-style, proposed-only in the literature).

### 2026-06-23 · Model-understanding phase (1.2.1) — ICL tested; per-factor verdict now evidence-backed
**Decision.** After understanding the model thoroughly and **measuring in-context learning** (the lever
1.1.1 omitted), the per-factor operator decision is upgraded from provisional to evidence-backed:
**content → Operator A** (~1.0); **emotion → Operator B** or accept a ~0.40 ceiling; **speaker →
Operator B**; **language → provisional A** (mechanism validated, test on FLEURS). Few-shot is
structurally and mechanically supported but **not a useful label-conditioned activation lever** for the
suppressed factors. See [[Omni-Embed-Model-Dossier]] and [[2026-06-23-omni-embed-speech-disentanglement-1.2.1]].
**Why.** Probes (frozen, training-free) established: native text-query retrieval recovers content (0.99)
but not emotion (0.27 < 0.36 probe); in-context demos strongly move the query representation
(move=0.336) yet are label-insensitive (0.047) and **few-shot demos reduce emotion accuracy**
(0.217→0.150). So no weight-free Operator-A lever (instruction, layer, pooling, native retrieval, ICL)
exceeds ~0.40 for emotion, and speaker is ~chance across all 37 layers — the contrastive Whisper-ASR
backbone has discarded it. This is the rigorous version of the 1.1.1 conclusion (which was withdrawn for
not testing ICL).
**Consequences.** New durable [[Omni-Embed-Model-Dossier]] (architecture + I/O contract + token
mechanics + few-shot verdict). New W4 diagnostic code: `io_contract.py`, `icl_forward.py`,
`scripts/diag/*`; `embed_queries` in `common`. Next: 1.3 Operator B (generative `lm_head` readout) for
emotion/speaker; 1.4 content/language fan-out. Also fixed an infinite derangement-loop bug in the P7
control (had hung for hours) — model forwards are ~0.11s.

### 2026-06-22 · F.1 finding (PROVISIONAL) — single-instruction + layer/pooling don't recover speaker; ICL untested
**Decision.** From the CREMA-D layer/pooling sweep (weight-free Operator A, *single-instruction*
conditioning): **speaker stays at chance (~0.03) across all 37 Thinker layers AND audio-token pooling**;
**emotion plateaus at ~0.40**. **Important correction (per review):** this is a *weak* intervention —
it does not exploit the model's strongest weight-free lever, **in-context learning / activation heads**
(native text-query cross-modal retrieval, few-shot demonstrations with target-token pooling, rich
activation prompts). So the negative falsifies only "single-instruction + architectural axes," **not**
"training-free activation." The earlier "speaker/emotion are Operator-B-mandatory" claim is **withdrawn
and downgraded to provisional (A(ICL)→B)**, pending experiment 1.2. content remains a clean Operator-A
win (~1.0). See report `2026-06-22-omni-embed-speech-disentanglement-1.1.1` and
[[W4-Training-Free-RL-Feasibility]] §0.1.
**Why.** A single short instruction has little leverage over ~50 content-oriented audio tokens under
mean pooling, and the model was contrastively trained with only `query:`/`passage:` prompts (weak
instruction-following) — but its Qwen2.5-Omni backbone has strong ICL, which reshapes the actual
forward pass and was not tested. Whether ICL survived the retrieval LoRA tuning is an empirical
question, not an assumption.
**Consequences.** Next: **experiment 1.2** — activation heads / ICL (text-query zero-shot + few-shot
with target-token pooling) for speaker/emotion BEFORE any Operator-B claim; then Operator B only for
factors that stay flat under ICL; then content/language fan-out. New W4 code so far: `layer_probe.py`
(mid-layer / audio-token pooling) + `scripts/layer_sweep.py`, `scripts/audio_pool_probe.py`.

### 2026-06-22 · W4 per-factor operator decision (from the algorithm-survey workflow)
**Decision.** Use **Operator A** (embedding-layer inference-time search: instruction/pooling/layer/
projector + verifiable-reward argmax) for **content** and **language**; **Operator B** (generative
Qwen2.5-Omni best-of-N/MBR, frozen weights, GRPO update dropped) for **emotion**; **hybrid** for
**speaker** (A's layer/pooling/LEACE-RLACE projector search, with B readout if the recovered probe
margin is too low). Any consensus/B path must gate the per-class plurality separatrix on a held-out
calibration set; prefer verifiable rewards over majority-vote pseudo-rewards everywhere a ground-truth
signal exists. Full analysis + sources: [[W4-Training-Free-RL-Feasibility]] §0/§4/§5.
**Why.** A multi-agent survey (11 agents, arXiv-cited, mostly self-verified) established: (a) Operator
A has real inference-time DoF on a vector-output model (instruction deltas up to ~55pp; closed-form
LEACE/RLACE/whitening projections); (b) the binding risk is weak steerability, fixed by reward-guided
selection; (c) omni-embed-nemotron-3b's Whisper-ASR backbone + contrastive mean-pooling **suppress
speaker/emotion** in the pooled vector (raw emotion probe ~31%), so those factors need layer/pooling
recovery or the generative readout; (d) consensus pseudo-rewards are Condorcet-fragile on near-chance
paralinguistic factors.
**Consequences.** The CREMA-D proof (E.4) tests the falsifiable cross-probe inequality
`A_t(e_t) > A_t(e_{t'})` per factor with non-target factors held fixed; a flat row for emotion/speaker
is a valid negative result (factor below the frozen model's separatrix), not a failure. The W4
`rl/embed_search` config implements Operator A first; Operator B is a future switch behind the same
interface.

### 2026-06-22 · Re-center the umbrella on training-free knowledge activation; W4 becomes flagship
**Decision.** Frame the whole series around one thesis: use training-free RL (no weight or structure
change) to *activate* the cross-modal, multi-granularity task knowledge an omni/multimodal LLM absorbed
in pretraining, lifting out-of-box performance on speech tasks. Promote **W4** (omni-embedding speech
disentanglement) to the flagship first work; keep **W1** as the mature training-free *pattern* reference
whose reward/eval machinery W4 reuses. No git repo or package is renamed — repositioning is by docs,
ordering, and a Role column. The flagship's first proof runs on CREMA-D (speaker + emotion on the same
audio). See [[Project-Thesis]] and [[W4-Training-Free-RL-Feasibility]].
**Why.** The docs stated the series only generically; the real thesis was unwritten, "disentanglement"
appeared nowhere, and omni-embed was listed as an asset with no motivation. Disentangling a frozen omni
model purely by reward activation is the strongest, most novel claim, and W1's existing training-free
machinery is exactly the shared foundation it needs.
**Consequences.** New canonical page `wiki/Project-Thesis.md`; four-work table reordered W4-first with a
Role column across README(_CN)/CLAUDE/AGENTS/docs/wiki; `common/` gains an omni-embedding loader +
embedding/probe/disentanglement reward & metric modules + an eval/probing harness (lazy imports
preserved); registry adds VoxCeleb/MELD/CREMA-D/CoVoST2/FLEURS/MINDS14/SLURP. The earlier "W1 first"
seed decision is superseded (W1 stays the pattern reference). W4-specific code/configs/README live in
W4's own repo.

### 2026-06-22 · Establish the README + Wiki knowledge base
**Decision.** Make the root README the single canonical onboarding doc (English `README.md` + 中文
`README_CN.md`), and stand up this Wiki (sourced from `wiki/`, synced by `scripts/wiki-sync.sh`) as
shared team memory. Sync `CLAUDE.md`/`AGENTS.md` to point here.
**Why.** Knowledge was scattered across per-tool files and people's heads; humans and their AIs need
one consistent understanding.
**Consequences.** Edit wiki content in `wiki/`, not the web Wiki; record notable decisions here.

### (template) · <short title>
**Decision.** …  **Why.** …  **Consequences.** …

---

## Seed decisions (context already baked into the repo)

- **WSL2-only compute.** RTX 5090 (Blackwell sm_120) lacks stable native-Windows torch wheels;
  verl/vLLM/flash-attn are Linux-only. All training runs in WSL2.
- **Python pinned to 3.12.** System Python 3.14 is too new for ML wheels.
- **Four separate work repos under one umbrella.** Independent history/issues per work, shared code
  via editable `common/`. Keeps each paper's repo publishable on its own.
- **Data never in git.** ~410 GB lives in `speechrl-data/` (WSL ext4); `.gitignore` guards it.
- **verl for RL; Qwen2-Audio as default base** (swappable via `models/` + config).
- **W1 first.** Training-free RL is the most mature work and the reference pattern for W2–W4.
  *(Superseded 2026-06-22: W4 is now the flagship first study; W1 remains the training-free pattern reference.)*

---

## 中文

> 追加式的轻量 ADR——团队的持久**记忆**。最新在最上。每条：日期 · 决定了什么 · 为什么 · 影响。人和 AI
> 都往这里追加（见 [[AI-Collaboration]]），再用 `scripts/wiki-sync.sh` 发布。

**条目格式：** 日期 · 标题；**决定**……**为什么**……**影响**……（英文区已有 2026-06-22 的两条与模板）。

**2026-07-04 · 固化三阶段研究方法论；语义层 Stage-1 问题定义战役以严审综述 + owner 选定题集收官：**
Owner 判定研究合理性不足，确立**三阶段方法论**（①问题定义：survey 支撑的论证、小样本仅方向性；
②方案验证：大样本预注册；③论文发表）并写入 CLAUDE.md/AGENTS.md（逐字节镜像）。Stage-1 就问题
"ICL 视角下冻结 omni 语音模型 instruct-prompt rollout 的优化空间对**语义层**（ASR/SLU/SQA/agentic）
是否足够"开展问题定义战役；收题检查点（K2）owner 选定 **CP-1、CP-3、CP-8、CP-4** 推进 Stage-2。
**诚实的 Stage-1 答案**：充分性 Stage-1 无法定论——核心格（H_prompt − H_fix 的量级）在所有音频
输入模型上无人测过（in-house 为零；文本域 APE/OPRO/GEPA 量化无音频对应；PromptingWhisper 仅两点
存在性正例、定不了界）。可操作标尺（H_fix/H_prompt/ρ、b1/b2 拆分、失败路由）把问题转成排名候选。
证据经 Stage-1 视角再定级：NO-GO 战役的 M3/M5 击杀降为 directional，MInDS +0.126 与 C1 headroom 为
scoped，向量类副语言负结果维持 settled（夯实为聚焦语义层的前提，收口 6/23 OPEN 为全转向）。
用 Academic-skills + Workflow（~40 agents）执行严谨链：33 个文献锚定问题 + 101 条已验证 claim +
跨域（LLM/VLM/speech）迁移地图；一个等预算定向探针 [n=50] 在 ASR 读出 Δ_BM≈0（审查抓出真实操作化
错误：测的是 Δ_BM 非 H_prompt−H_fix）；16k 词综述（171 引用）过 **/ars-reviewer 五人格严审**——
MAJOR REVISION（无 CRITICAL），7 P1+14 P2 全修，re-review 判 all-P1-resolved（并抓出确证的 SNR
符号错误 +5dB 非 −5，跨六文档订正）。Stage-2 每问题以新 Research-Proposal-Template 实例开始；
建议成本排序 CP-3 → CP-1(SLU/SQA)+CP-8 → CP-4；跨会话变体留在 r1–r3 关闭围栏后。分支
`research/stage1-problem-definition`，PR 待合并。

**2026-07-04 · 第一步合理性战役裁定 NO-GO——agent 级问题关闭（预注册、测量支撑、owner 终审）：**
Owner 批准战役推荐的 **NO-GO**（问题 ii：是否构建 omni agentic 系统扩展免训练 RL），并放弃了可选的
safeguard-5 V4 修正案岔路（以徒劳性理由被记录否决）。7/02 判定成立——这次由战役自己的预注册仪器支撑，
而非仅靠审稿论证。问题 i（单模型 TFRL 方向）**理性且继续**，经由 P-D（C1 真实 headroom 的条件刻画）。
判据先于分析冻结（b19bff2；零假设=7/02 判定；不确定即 NO-GO）：G1 算术性失败——**M3** 被自己的
Phase-0 零支撑检查击杀（F=0.38108 超冻结杀线 0.01 达 38 倍：语料罕见 ≠ 模型 OOV）；**M5** 未过 PASS 线
（设计表面上精确零：sel=MBR=0.07722），并诚实标注冻结选择器 V1|0.05 事前已被证明惰性（翻转 λ 中位 60.5）
——故 M5 按「不确定→冻结默认」关闭，而非对机制类的经验证伪；M2/M4 仅设计、M1 未开 → 默认。附带发现：
新切片上 MBR 对 greedy 零增益而 oracle headroom 真实（+0.0238）——可部署无标签捕获率 ≈0%。
严谨链：22 条反对台账 → 3 增量扫描车道（33 条已验证 claim；r1/r2 决定日复核为空）→ 4 对盲构造/反驳 →
2 个冻结先于运行的预注册 pilot → 六指控控辩合议庭（双盲法官全部 stands）→ 机械合成+完整性核查 →
**/ars-reviewer 五人盲审一致 sound-with-corrections**、12 项修正全部落实、12/12 备忘数字复现入
`_repro/m5_memo_censuses.json`。收敛论文的 "deferred, not disproved" 问题获得可引用的关闭句（决策文档
§10）。WF-2 不启动；算力转向 W4 队列 + P-D；r1 零成本常设监测。重开仅凭 r1/r2/r3（并记录一处覆盖缺口：
族内后继证据无重开路径，如需修补属 owner 级修正）。战役机制：Workflow 编排 + academic-research-skills
（~100 agents、约 1 天、~9h GPU、单卡 24GB 5090）。分支 `research/agentic-rationality-step1`，PR 待合并。

**2026-07-03 · 发布线收口；资产/文档对齐现实；推理引擎决策入档：** PR #2（6/26→7/02 全弧线）主人已于
7/02 合入；本日快进本地 master、同步 wiki（并**从公开 wiki 清除了 6/25 那份占位未填、归因已被推翻的
「Operator-B best-of-N」草稿**）、删除已合并分支。工具链入库（`87154b9`：env-setup Phase 5 的
llama.cpp CUDA 构建、按文件取 GGUF 的脚本、补上 W1 已提交脚本断链依赖的 `generative_omni`）；
`main.bbl` 重建至收敛版（`5f5cfce`）；实测跑不通的 vLLM 脚本与过期草稿/TODO 退役。**GGUF 入 lockfile
成为第 6 个冻结模型**（新来源类型 `hf-manual`，按文件取、刻意避开 >110 GB 全仓拉取；`fetch-data.sh`
分发 + `gen-lockfile.py` 映射同步；总量 408.7G→441.0G）。**文档对齐现实**（约 13 个文件）：真实发行版
是 `Ubuntu-24.04`（默认 `Ubuntu` 为 WSL1、无 GPU）、真实数据根在仓库根 `speechrl-data/`（WSL 侧
`/mnt/d/…`；ext4 `~/speechrl-data` 只放 `mlruns`）、总量 ~410→~440 GB。新增 [[Inference-Engine-Choice]]
（llama.cpp 已验证、vLLM 版本配对留待 W2）；[[Per-Work-Status]] 刷新。本条订正 7/02 条目的收尾状态：
分支已推送合入、wiki 已同步。留待排期的研究项：无标签选择器（收窄 realized-vs-headroom 差距）、
预注册 H1/H2/H3 pilot（环境已解封）、W4 NULL 后的实验队列。

**2026-07-02 · 原理/目的/可行三轴深审把 W5「坍缩」，再用真实 best-of-N（llama.cpp）挣回，收敛为一篇诚实的单模型论文：**
主人判定此前审查仍偏语法语义、未触及**原理/目的/可行**，要求以 **POMDP**（分步、局部观测、迭代+回滚）方式做真正的对抗式审查。
三份独立敌对专家阅审一致结论：**agent-level/L4 框架不成立**（OSA 理论「证到的是同义反复」——`qstar_product` 即
`exp(a+b)=exp(a)exp(b)`，`OptSpace-notes.md` 留有把该定理写成相反主张的铁证；有趣处则不可建模、未验证；目的自我否定、
信息价值≈0；跨会话基准所需数据在冻结集里根本不存在、技术栈未搭）。主人选 **A：坍缩为诚实的单模型论文。跟着证据走。**
**影响（POMDP 轨迹，完整日志见 `papers/agent-level-tfrl/reviews/pomdp-restructure-log.md`）：**（1）取证式溯源发现论文里的
content/intent「生成式 best-of-N」其实是**冻结双编码器的余弦检索**——一处此前四轮审查漏掉的**错误归因**，并重跑 MInDS 落一份带
配对 CI 的可复现产物。（2）57→21 页；提交精确的**副语言负结果**探针（说话人 3×随机、情感 2.4×随机、免训练增益为 null）。
（3）**新一轮敌对审查发现坍缩后仍有根本缺陷**：omni-embed 的「选择」根本没用到奖励（argmax 余弦，非奖励驱动）——**根本不是
training-free RL**。（4）主人选 **B：用真实 best-of-N 挣回 RL 主线**。撞上 HF/vLLM 的 int4 加载墙；主人一句**「30B 用 llama.cpp
跑」**破局。（5）**真正的 training-free RL 落地**：Qwen3-Omni-30B（Q8_0 GGUF、llama.cpp 常驻服务、24GB 笔记本 5090 上 -ngl 28）
对 LibriSpeech test-other+snr5 每条采样 N 个转写、用可验证 WER 奖励选择。**多种子（3 个生成种子合并，n=144）：oracle best-of-N
在 N=8 headroom +0.042 [0.029,0.056]、N≥4 显著（N=1<greedy——诚实的序统计爬升）；可部署的无标签 MBR 在每个 N 都不显著**——真实的
奖励驱动 headroom + 诚实的「已实现 vs 上界」差距。（6）重构：**C1**=该真实 best-of-N；**C2**=诚实的冻结编码器探针（不同算子、非
RL）；**C3**=只给「符号+上界」的奖励离散度透镜（N-曲线归为序统计），两条 `sorry`-free Lean 引理。（7）**对重构后论文再做四轮新敌对
审查并收敛：根本→重大→重大→次要，无幸存的根本/重大问题**；一位完整性审稿人把每个 C1 数字逐位复现于已提交产物。**判定：收敛。**
每个数字都有已提交可复现产物（best-of-N 在 W1 仓、探针在 W4 仓）。新证明的工具能力：**llama.cpp 能在 24GB 笔记本 GPU 上驱动
Qwen3-Omni-30B 做语音 ASR + best-of-N**（音频输入上游标注为实验性）。分支未推送、wiki 未同步。

**2026-07-01 · W5 提案经四轮「新对手」对抗式审查加固（只改实质、不改措辞；在预设上限收敛）：** 主人判定首轮
审查不够严格（只一轮、审稿人复用且被自己的清单诱导、meta 曾返回占位输出、部分问题只在措辞上打补丁）。遂重做
为**多轮对抗式审查**：每轮**全新审稿人**（对此前各轮与「决议台账」双盲），一位**主审**独持台账、只报**真正新增**
的 critical/major，**只在实质上修复**（用 Lean/GPU 实验/引用核验加强，或直接删除），**循环至干净一轮、上限 4 轮**。
**为什么**：一份以「机器可验证的诚实」立信的提案，必须扛住独立攻击，而非一次自洽通过；措辞对冲不算解决。
**影响**：四轮跑满、缺陷等级单调收敛并在上限终止——R1（6 critical+11 major：结构性夸大——「单模型惰性→智能体**恢复**」
的论点**不被定理支持**，`qstar_product` 证明隔离最优=单体最优，且被自有数据反驳；全文重构、改标题、系统降级为
**测试床**）→ R2（13 major：重构未传导到最常读章节；KL 方向、前言、情感统计量全部重同步）→ R3（0 critical、4 major：
相关工作的 β 约定、Lean 状态表 `sorry` 位置、PLDA 标定的证伪器、提案定位）→ **R4/上限**（0 critical、7 major：全为
内部一致性/保真/**产物完整性**——C1 的 Pinsker/Beirami/Hoeffding 归属、Lean 旧注释、情感基线升级为经典在线变点检测、
按因子独立的判胜、逐字节一致的附录签名，以及被盲审发现的：已提交的情感 t-CI 是**手工填入而非脚本产出**）。自 R1 起
每轮都确认**无定理错误、无证明破损**。旗舰情感结果在 5090 上**重跑为 NULL**（跨种子 95% t-CI **[−0.043,+0.116]** 跨 0），
诚实修正了原 +0.097（单种子 oracle 选层假象）；R4 修好复现脚本使其**产出**该 t-CI 并重跑，令 JSON 真由脚本生成。论文
现为诚实且精确限定的「理论(增益由奖励**离散度**决定，而非搜索力度或智能体包装；隔离结论是**会计恒等式**) + 有界的
副语言 NULL + 测试床与预注册证伪计划」，其核心问题（智能体分解相对冻结单模型是否有增益）**明示为开放**——是**提案**
而非已执行结果。57 页、编译零未定义。六份审查存档 + `ledger.md` 决议台账于 `papers/agent-level-tfrl/reviews/`。提交：
伞仓 `70b5aef`(R3)、`c2481b4`(R4)；W4 `dd6e8d3`(重跑产物)。分支 `docs/research-proposal-template-and-first-proposal`，未推送。

**2026-06-22 · 把系列重定到「免训练知识激活」主旨，W4 升为旗舰：** 全系列围绕一个主旨——用免训练 RL
（不改权重/结构）激活 omni/多模态 LLM 预训练中习得的跨模态多粒度任务知识，提升语音任务开箱表现。把
**W4**（omni 嵌入语音解耦）升为旗舰首发工作，**W1** 保持为成熟的免训练「范式」参考、其奖励/评测机制被
W4 复用；不改任何仓/包名，仅靠文档、排序与「角色」列重定位；首个验证在 CREMA-D（同音频的说话人+情感）。
下方「先做 W1」的初始决策被本条取代。详见 [[Project-Thesis]]。

**已固化在仓库里的初始决策：** 仅用 WSL2 算力（RTX 5090 无稳定原生 Windows torch；verl/vLLM 仅 Linux）；
Python 锁 3.12（系统 3.14 太新）；一个伞仓下四个独立工作仓库（各自历史/issue，靠可编辑 `common/` 共享
代码）；数据绝不进 git（≈410 GB 在 `speechrl-data/`，`.gitignore` 兜底）；RL 用 verl、基座默认
Qwen2-Audio（可换）；**先做 W1**（免训练 RL 最成熟，是 W2–W4 的参考范式）。

**2026-07-07 · 知识轨（冻结 omni + 外挂多模态知识 + training-free RL）Stage-1 执行 + 结论（T0–T8）：**
先做了**概念对齐**（知识≠技能≠记忆,按缺失粒度分;之前把"外部知识注入"错标成"记忆",已 dated re-grade,见
[[2026-07-06-capability-taxonomy-knowledge-skill-memory]]）。取向锁定**效果优先、非概念新**。调研（agentic-RAG 横向对比 +
2025-相似原理扫描）发现机制在文本域已存在（RTTC/AdaRewriter/TARG）→ **不追净新**,只在冻结 Qwen3-Omni 上抬基线。
**关键结果（directional,n≤60,paired-bootstrap CI）：** T0 探针——冻结 omni **能**消费注入知识但不完美（错配会拖累）;
**T7 实验（heysquad RAG）——H0=+0.517 CI[.38,.65]：base 0.283→oracle 0.80,冻结 omni 有巨大知识 gap 且极善消费检索来的
外部知识（RAG 大幅有效）；但选定的 R1 精度门控被证伪（gate−inject_k=−0.134 CI[−.23,−.05]）——模型对干扰 passage 鲁棒,
门控牺牲召回反掉点,约束是召回而非精度。** **Lean（T5）：** 创建了 `TfrlProofs/Realization.lean`（sorry-free,全库绿）——
`selector_tendsto_oracle`：奖励引导选择器在估计误差 τ→0 时收敛到 oracle（C4,realized≥oracle−2τ）。**注意：`Theory-Convergence`
文档此前声称的 Realization.lean/C4/InfoBoundary 实际盘上不存在（文档夸大）,本轮才真正落地 selection 收敛。**
**理论⟷实验闭环：** T7 的 R1 失败恰是该定理前提被违反（TF-IDF 相关性代理 τ 太大、丢 gold）→ 定理正确指出"成立与否由奖励代理 τ 决定"。
**三问结论**（[[2026-07-07-knowledge-track-conclusions]]）：①最优组织=**冻结 omni 单跳下的文本-passage RAG**（非 LLM-Wiki/KG,
后者留多跳 Stage-2；audio-native KG 空 cell 且检索器要训练）；②应用=**召回优先的文本注入**、边界干净（外部知识非答案）；
③TFRL **收敛已证（τ→0⇒oracle）**,但干净单跳下准确率杠杆近饱和 → 有效价值重定向到**效率（何时检索）与受压 regime（ASR 噪声/多跳）**。
全程 directional-only、boundary-clean、不伪造；记忆/技能轨保持 park。Stage-2 由 owner K/T9 gate。产物：`wiki/2026-07-0{6,7}-*`、
`~/tfrl_proofs/TfrlProofs/Realization.lean`；未 wiki-sync、未 push。

**2026-07-07（更正/续）· 清白重跑推翻 T7 正结果（E0–E6）：** owner 抓出 T7 三处硬伤（覆盖不足 / 检索 query 用 gold 文本越界 / **KB 逐条含 ground truth**，审计 answer_in_own_KB=1.0）。**清白重跑（audio-ASR query + 答案擦除 + 残留 0.017，n=60）：clean_H0=−0.066 CI[−.17,.03]（null）、lookup=+0.516——表面 RAG 增益 100% 是查答案；答案擦除后外部知识零增益。** E0：盘上无干净"事实-gap+外部KB"测试床（OpenbookQA 饱和+无 fact-book）。**结论（[[2026-07-07-E6-final-conclusions-clean]]，无泄漏前提）：①无法断言任何形态增强冻结 omni，RAG=待超越基线且增强价值未清白证实，前提=先构造事实-gap 基准；②检索加载机制可行但清白收益是查答案；③TFRL 收敛已 Lean 证明（τ→0⇒oracle），准确率空间因缺干净测试床暂无可测对象，近期干净可测的是效率（何时检索）。** 幸存清白:Lean/调研/taxonomy；作废:T7 及旧结论正向主张（已挂横幅）。directional、未 sync、未 push。

**2026-07-07（完成）· 清白 E2/E5 + Lean C1/C2 + agentic 触点,收口三问:** hook 指出上一版三处未完成（测试床阻塞 / 覆盖不足 / Lean 只 C4）→ 本轮真做完。**(点3 Lean)** `Iterate.lean`（sorry-free,全库绿）交付 **C1 单调有界收敛 + C2 预算 N*≤(M−x₀)/δ + 无约束发散负结果**（补齐 C4 之外的迭代收敛）。**(点1 清白 E2/E5)** 反事实利用率（CF,无泄漏,3 集）：冻结 omni 冲突时只 **24%** 采纳外部知识(参数固执,SQuAD 上 keep-参数 0.70);答案擦除增强 **null**(T8);**proto-agentic 2 轮工具递送使采纳翻倍 0.175→0.35(t10)——递送形式是清白训练无关杠杆(E5 清白目标,取代已证伪的 R1 精度门控)**。**(点2 覆盖)** semantic 4 集 + proto-agentic;full-agentic 记为离线不可行(需模拟器/DB-env/o4-mini rubric)。**三问清白结论([[2026-07-07-E6-final-conclusions-clean]])：①存储结构(RAG/LLMWiki/KG) under-determined,一阶清白信号在"递送/交互形式"(agentic 工具递送 > flat);②使用=agentic 递送 + 信任校准,检索加载必要不充分;③TFRL 优化空间在"递送-形式选择 + 信任校准"两轴(非精度门控/推理增强),收敛已 Lean 证明(C1/C2/C4,τ/N*)。** 最重要负向机制发现 = **参数固执限制 RAG 修正参数错误**。全程 boundary-clean、directional、未 sync、未 push。
