# Decision Log — 2026-08 卷

> 条目按原序保存（新在上）；追加与分卷规则见 [[Decision-Log]]。

### 2026-08-03（续89）· owner 两项裁决（E 盘唯一离线介质/--require-installed 默认）+ 整改四轮对抗自检收敛

#### Context

owner 答复续88 遗留问题并指示对整改工作本身做多轮对抗式自检。

#### Decision

①E 盘为唯一存储介质：`SPEECHRL_DATA_DIR/program-archives/` 下的四个 git bundle 即默认且唯一
离线副本（GitHub cold-backup 远端并存），不再另设第二介质。②`--require-installed` 采纳为主
开发机默认（写入两份客户端指南）。③对抗自检四轮收敛：R1 机械反证扫描修 10 处活动面残留
（4 处旧安装指令、3 处 gates 清单缺新门、CONTRIBUTING 2 处旧口径、实验台账缺 shared code
revision 列），历史 integrity 收据与旧日志条目按 append-only 判不改；R2 独立数据重验全过
（574/574 resolution 对镜像逐 blob 比中、claim-ledger 17/17 URI 可解析并修 1 处行号粘连、
SNAPSHOT 13/13 三方一致、4/4 bundle sha256+verify+final-pin）；R3 故障注入 8/8 fail-closed
（临时 worktree：计数漂移/决策记录篡改/删 resolution 行/无 waiver UNRESOLVED/未登记目录/
namespace 漂移/缺 checkout）；R4 语义终审+全量验收绿。

#### Consequences

续88 遗留 owner 项全部关闭；剩余延期项仅 T5 的 LEGACY_W_ERA 物理收缩（R0 后）与 study 远程
CI 首跑（push 授权后）。详单：`docs/checks/program-architecture/2026-08-03-post-reorg-remediation/`
（Addendum）。

### 2026-08-03（续88）· 重整后架构复核整改 T0–T5 落地（真相对齐/574 冷备解析/工程地板）

#### Context

目录重整落地后，复核提案 `PROGRAM-DIRECTORY-POST-MIGRATION-REVIEW-V1`（specs/2026-08-03）判
`CONDITIONAL_ACCEPT_WITH_REMEDIATION`：主架构正确，但 HOT 文档与实际目录冲突（P0-1）、574 条
legacy 资产全 unresolved 而 gate 仍 PASS（P0-2）、study 依赖/测试/lockfile/CI/license 缺失
（P1-1/1-2）、checker 浅层存在性检查（P1-3）、W1 snapshot 记录十件实为十三件（P1-4）。逐项
对仓核验属实后按 user 指示执行整改。

#### Decision

T0–T5 全部落地（伞仓 commit 5fa2249/e85ac82/989ae98 + 本笔；study 仓 4ceaba9/5dd1822/
ac75a61）。要点：①HOT 三页/两份旧 spec/owner 合同（dated Amendment 1）/common README 对齐现
状；②新 retired-repository-registry + 四态 resolver，574 项全 `COLD_BACKUP_RESOLVED`
（`remote@commit:path`+blob），`UNRESOLVED>0` 无 waiver 即 gate FAIL；四仓离线 git bundle 落
`SPEECHRL_DATA_DIR/program-archives/`（SHA-256 入 registry）；claim ledger 18 处死路径升级
git+https URI；③study 落 42 项无模型 contract tests（信息边界/OBS-SUPPLY 分离/exposure
schema/FrozenCoreGate fail-closed/快照隔离/治理对齐/入口拒绝）+真实 config 骨架+uv.lock+CI+
私有阶段 LICENSE/NOTICE；④common 依赖按 YAGNI 判 `DEFERRED_UNTIL_FIRST_CONSUMPTION`（首次消
费时精确 umbrella commit pin；实验记录增 `shared code revision` 绑定）；⑤registry v2（
default_branch/package_name/created_at/experiment_namespace/decision_record_blob）+ checker 补
四盲点（真 Git 校验/`--require-installed` origin+branch/跨源计数与 frontmatter 断言）；
⑥snapshot 记录统一为十三件逐文件 provenance，tombstone 走 append-only Addendum 2；common
首次 OWNERSHIP 审计落 `common/OWNERSHIP.md`。

#### Consequences

首次模型触达前的硬门（T0–T3）全部关闭；验收收据
`docs/checks/program-architecture/2026-08-03-post-reorg-remediation/`。E0（D1–D4）继续为下一
步；模型触达仍需 E0 closure + runtime receipt（合同不变）。旧 proposal 仅存历史理由；当前操作
只从 architecture/合同/HOT 三页进入。遗留决定权在 owner：cold backup 是否另设第二离线介质、
`--require-installed` 是否纳入主开发机默认习惯。

### 2026-08-02（续87）· round-21 三裁决（红线零训练/结论向量/RQ0 析因）+ v20 整改授权

#### Context

round-21（GPT-5.6 四轮隔离审查@v19 blob `c4a9e8f4`，即对抗自检环收敛终态 `ab221c4`）判
MAJOR_REVISION：6 项全报告层、非 NO-GO、边界纪律满分（novelty 双向出域、不要求数值阈值
与执行、明示开题许可≠Stage-2A 授权）。三通道对抗核验：blob 绑定三项逐位一致；**19/19
引文真实零虚构零定性错**（三轮以来最干净：r19 两错→r20 三修正→r21 零错）；**五项发表
态声明 5/5 属实且滞后方在我方**——WavRAG 实为 ACL 2025（2025.acl-long.613）、DeRAGEC
实有 Findings ACL 2025 正式件（2025.findings-acl.786）、Speech-Hands 已有正式条目
（2026.acl-long.1997）、Audiopedia 已有 ICASSP 2025 DOI（10.1109/ICASSP49660.2025.
10889814）；LongAudio-RAG 题名变更项对我方不成立（§10 行已用现行题名+现行一作）。本地
覆盖：19 件中 9 件全库真缺席（语音实体检索/链接谱系 2021/2023 两件、Whispering LLaMA、
Generative Annotation 2025.emnlp-main.1052、长音频策略控制 2024/2025 两件、VoxRAG、
NAACL 2025 表示分析、CCFQA AAAI 2026）。正文指控锚全数亲验坐实：§3.3 L645-648 仍把
schema/版本/出处钉为 O-config 实验对象（v19 收窄未传播到旧节——六轮自检环逃逸，教训
入新镜头）、K0 条款自承正读数不可分离、同录音索引 ORG/OBS 双标、§6.2 简写回漂、L241
"音频域 2026 起步"时间线不可维持、K-NB 全称主张反证逻辑低估。

#### Decision（owner 三裁决，2026-08-02 会话）

①**红线权威口径（MAJOR-4 控制器分叉）**：本轮**不训练任何模型参数**；可引入新模型但
一律 frozen（已发布检查点）。落地=档 B 控制器**不是模型**：外置、非神经、无梯度，有限
决策常量 dev 期 reward-guided 标定、test 冻结种子重放；K-RL 身份按续82③ 保留为"策略
选择/标定"而非"模型训练"；评审"删 RL 身份"支路不采（与 round-20 方案 A 同型拒绝）。
②**总答案=结论向量**：废单一"机制成立"总标签，改 RQ0–RQ4b 逐问结论、遵循既有评价
体系（"五类结论不得互相替代"之 RQ 级延伸）、多载体综合评估不合成单标签（续83① 三支柱
相容）。③**RQ0 取选项 2**：保留分型承诺（观察不足/参数知识不足/可由外证纠正/何时不应
引知），补 OBS×外部证据 2×2 析因（无增强/仅观测增强/仅真外证/双开）+预注册错误分型，
使观察不足、外证不足、交互各有 estimand；闭卷参数化召回探针承接"参数知识激活"辨识面。
④其余六 MAJOR 按 Fable 对抗分析采/半采：M-2 四处跨层漂移全修（含 OBS-INDEX 方案）、
M-3 十一判据三态真值表化+K-NB 全称反证逻辑（任一承重对手经正式反向检验证优→全称主张
REFUTED）、M-5 载体族 discovery/confirmatory split+INCONCLUSIVE_BASELINE_NOT_READY
出口+最小确认路径资源上界（可行性规划信息、非成本门——续82② 不冲突）、M-6 文献九件
收编+四件发表态升级+L2 拆线+时间线修正+发表态权重分层。⑤自检环基线延续并**新增两
镜头**：旧节-新卡传播全扫（收窄条款对全文旧表述的传播检查）、发表态定期复核（arXiv
件逐个查 anthology/DOI 升级）。

#### Consequences

round-21 评审件落审计层+回应信；v20 整改开工（十项签字门全采）；文献批=9 件新 fetch+
4 件正式形态升级+2 件 D2（wang21b 域外拒绝=准入邻近、Generative Annotation=RQ1/RQ3
最贴）；评审 §7 问题树表=代拟采结构、措辞随 v20 由 owner 签；复审窄面=问题树+五层归属+
三态判据+RQ4a/档 B+direct-field map+最小确认路径。

### 2026-08-01（续86）· round-20 六项 MAJOR 处置（方案 B 序贯合同/三态判定/效率 estimand/文档拆分）+ v19 整改授权

#### Context

round-20（GPT-5.6 多轮隔离审查@v18 blob `e837886a`）判 MAJOR_REVISION：6 项全报告层、
边界纪律良好（novelty 双向出域明文、非 NO-GO、round-19 五项判基本关闭）。三通道对抗
核验：14/14 引文真实零定性错（引文卫生三轮持续改善）；三处修正=Failing Forward 即
DARAG 正式版（已全量 D2、评审重复计数）、Siskos anthology 条目=库内件正式版（已交叉
登记）、CTC-Assisted 实为 SLT 2024 正式发表；对全项目全新十件（TED-EL/Audiopedia/
iKnow-audio/Xiang/MCR-Bench/CopyNE/Adaptive-CB/CTC-Assisted/N-best T5/HypR）——其中
TED-EL/Audiopedia 将"语音实体→外部知识"谱系时间线自 2026 前移至 2024，v18 L4 时间线
失真指控成立。正文指控四条文本锚亲验坐实（档 B 在线更新张力 L555 vs L842/856、USE
输出交叉 L234、value 非实验轴 L551、"被证伪"措辞 L813）。

#### Decision（owner 裁决，2026-08-01 会话）

①**MAJOR-3 取方案 B、不采方案 A**：档 B 改写为有限时域序贯决策合同（状态/转移/horizon/
可观测反馈/离线 credit assignment/策略 dev 学 test 冻结种子重放），"contextual bandit"
一词退役——TFRL 身份与 K-RL 判据保留（续82③ 重申；方案 B 恰为续82③"按 MDP/bandit
对象正式化"的落地）。②**效率维度**：以既有"每有效实体修正边际成本"升为效率比较性
estimand（描述性、不进主判据——续82② 效果优先维持）；可靠性护栏（worst-group 非劣+
correct→wrong 上界）入 K-NB 成立侧护栏族。③**文档拆分与最小主线**：治理史/环记录移
AUDIT sidecar、主报告=科学叙事+参考文献表；最小开题主线冻结按"排序非收窄"口径——
三支柱全数保留为条件扩展承诺（续83① 相容）。④其余全采：RQ 卡片化（RQ1 收窄/RQ2 升
SRC-sel 主实验/RQ3 收窄准入/RQ4 拆 4a/4b/总问题级决策表）、三态判定语义全格网
（SUPPORTED/REFUTED_OR_NEGLIGIBLE/INCONCLUSIVE）、§1.7 十件补录+L4 三分+时间线修正、
标准参考文献表。⑤对抗自检基线要求延续（续85④ 口径：隔离上下文+重新搜索+监督核验、
至零轮）。

#### Consequences

round-20 二件（评审+回应）落审计层；十件 fetch+五件 D2（TED-EL/Audiopedia/iKnow-audio/
Xiang/MCR-Bench——iKnow 按声学类别 tagging 限定收编）+五件登记级+DARAG 交叉注；v19
起草+签字表 V3；完成后送"问题树+直接语音/音频现状+统计/控制合同"窄面复审。本条不授予
Stage-2A、模型/API 调用、指标运行、研究数据集获取、原型或 push/wiki 发布权限。

### 2026-08-01（续85）· round-19 边界纠偏生效（开题只审问题与现状）+ TFRL 身份维持 + v18 重构授权 + 对抗自检基线要求

#### Context

round-18 零 MAJOR 后进入签字就绪，round-19（GPT-5.6 多轮隔离审查）初版以新颖性尺度判
7 MAJOR；owner 与评审方在提交前协同纠偏为「边界纠偏版」：`novelty_review_in_scope:
false`、5 MAJOR 全部为报告层要求（SESOI/power/数据 hash/后端保真明示移 Stage-2A）。
三通道对抗核验（blob 亲验/20 件引文隔离一手核验/本地读集扫描）：20/20 引文真实零虚构；
PlanRAG-Audio、GRGA、ATIR、MARS 四件 2026 新近邻定性准确（GRGA 逐字 training-free+
POMDP；ATIR 自述训练 retriever；MARS 选择对象=对话历史）——§3.3「语音域读集内全部缺席」
不可维持；2 件评审定性错误（AgenticASR「intent routing」串自同作者 2605.29430；G-SPIN
「entity description/世界知识」串自 DANCER）；MAJOR-2 经核实为提案自身词典内部不一致
（§1.3 重听=观测重表达、准入=使用形式 vs §6.3 全装进「知识接口查询族」）。

#### Decision（owner 裁决，2026-08-01 会话）

①**开题审查边界**：本阶段只审「研究问题是否讲清、学界现状是否讲准」，新颖性判决双向
出域——既不作占据/首创判决，也不在正文写「无人做/全部缺席/唯一空位」类排他句；纠偏版
为 round-19 唯一操作版，初版以 sidecar 留痕（会话转录级重建、无裁决效力）。
②**v18 重构授权**：采纠偏版骨架——一句话总问题+RQ0–RQ4、现状改五条研究线、唯一词典
贯穿（OBS/CONTROL 独立于知识三形式）、模块→RQ→形式→变量→判据→失败出口唯一映射表、
三阶段改 WP1–3；三支柱维持（续83① 不变——重排非收窄，无一支柱退场）。
③**TFRL 身份维持**（重申续82③）：纠偏版 MAJOR-5 之「TFRL/bandit 不应在开题阶段成为
必须证明的身份主张」条款不采；档 B 身份主张与 K-RL 判据保留，定位为 WP2/WP3 内的方法
身份主张而非总研究问题。
④**对抗自检基线要求**：v18 及后续每个发布件必须过多轮对抗式自检环，且必须含**隔离上下文
面板、重新搜索（fresh literature search）与监督核验（对承重表述抽查一手源）**三类镜头，
至一轮零新发现方可送审。

#### Consequences

round-19 三件（纠偏版评审/初版 sidecar/回应件）落审计层并登记 blob；新近邻收编义务落地：
全文 ledger +19 行（PlanRAG-Audio、GRGA、ATIR、MARS=arXiv 2508.01166、AgenticASR、
G-SPIN、FineCoS、CB-Whisper、Liu-Trie、Chan 2023、DANCER、Modica、Wang 2026、Pundak=
ISCA 通道），四件 D2 深读+两件纠错定性件（TCR）起草中，Interactive ASR 2605.29430 自
stage1b registry 路由入 R2 读集；v18 起草+签字表 companion 同步随后；AgenticASR/G-SPIN
入任何矩阵/正文必须按 TCR 纠错定性、不得继承评审行描述。本条不授予 Stage-2A、模型/API
调用、指标运行、研究数据集获取、原型或 push/wiki 发布权限。

### 2026-08-01（续84）· 主载体数据包定为「Earnings21+ConEC 层」（round-16 MAJOR-1 整改路线 A）

#### Context

round-16（GPT-5.6 签字审查，对 v16.1 blob edb38a2f）判 MAJOR_REVISION：唯一 MAJOR=主载体
Earnings21 的直接 contextual-ASR 谱系（Fox 2022 偏置词表/ConEC 2024 真实上下文层/Huang
2024 训练式改进）全部缺席证据底座，连载体源论文（Del Rio 2021）亦未登记；且 v16.1 所写
「官方 split」经核验为事实错误（Earnings-21=纯评测集、无官方三分）。三路一手核验确认：
评审承重引用（ConEC）逐字属实；Fox 词表为 oracle 派生（ConEC 自评"too simple"）且其 ASP
组件为训练件；**Huang 2024 的「trained upper bound」刻画错误**（其自表总 WER 10.40 不敌
training-free shallow fusion 10.29，真上界=ConEC oracle 行 9.69）；补读后「API-only×
training-free×双源动作选择×外显世界知识 rescore」合取仍无占据。ConEC oracle 余量
（B-WER 24.84→18.72）为 K-NB 战场提供强于 Siskos 轴的 headroom 一手数。

#### Decision（owner 裁决）

主载体数据包按整改路线 **A** 执行：**主载体=「Earnings21 音频/评测集 + ConEC
version-pinned 上下文与修订转写层」**；dev/标定=Earnings-22+ConEC 层（其官方协议：
Earnings-21 只作 evaluation）；reference 采 ConEC 修订版（实体纠错），与原始版数字对照处
如实双报。路线 B（排除 ConEC 层）不采。

#### Consequences

v17 整改：三件谱系 D2+矩阵行（Huang 2024 按更正后口径入表、Fox 词表带 oracle 出身警示、
ConEC baseline 可跑性风险入义务）；载体源论文与 Earnings25 登记（后者排除裁定：ASR-only
无上下文层）；「官方 split」纠错+数据隔离合同+知识时态/污染协议+同载体基线阶梯；round-16
MINOR-1..5 关闭；一页纸签字表交付；两条新线索（Contextual Earnings-22 2604.07354/
ProfASR-Bench 2512.23686）入补扫义务。本条不授予 Stage-2A、模型/API 调用、指标运行、
数据集获取（研究数据）、原型或 push/wiki 发布权限。

### 2026-08-01（续83）· 三支柱维持（收敛权在 Stage-2 基线实验）+ 克隆边界升红线第四条 + round-14 复审发起授权

#### Context

v15 完成 D2 登记批（十篇近邻 D2+ledger，`dc9ab84`）并经七轮对抗内审收敛至零发现。内审
博导镜头提出裁定级建议：锁定单一主问题、另两支柱降为声明式后续工作（"三篇论文体量"指控）。
该建议属研究对象定义权，上交 owner。另 round-12 OBS-1（克隆边界是否升 §0 红线第四条）
悬置至今；v15 已将克隆机制如实重述（零样本克隆传音色、发音变体来自显式 G2P/音变模型）。

#### Decision（owner 两裁决）

①**三支柱维持，拒绝开题期收窄**：研究方向允许失败——研究内容与方向的收敛发生在 Stage-2
的大量基线实验对比中，不在开题（零实验状态）预判收敛；三支柱+整合载体条款（系统作为整体
在一个载体上运行与归因）+判据族失败出口即为收敛机制本身。②**克隆边界升 §0 红线第四条**：
enrollment 仅限当前会话内当事说话人任务音频、不跨会话留存、克隆输出仅用于内部 key 合成
比对、永不生成对外播放语音、不涉第三方 PII 合成（§2.4 五项边界升格为红线，round-12 OBS-1
就此关闭）。随后发起 round-14 复审（隔离评审、审计层落件）。

#### Consequences

v15 补红线第四条（§0/§1.4 同步）并在处置建议最强反方补"三篇论文体量"应答（收敛权在
Stage-2 实验+整合载体条款）；round-12 OBS-1 关闭、遗留 owner 落笔项清零；round-14 复审
对象=含本裁决落地后的 v15。本条不授予 Stage-2A、模型/API 调用、指标运行、数据集获取、
原型或 push/wiki 发布权限。


## 早期条目（紧凑格式）

**2026-08-02 · 研究方向改为局部流水线，以语义 study 独立建仓，Wiki 统一管理实验资产：**
**Context：** 当前活跃资产把 W1 写成主程序载体，并把 R1–R9 候选分析隐含成未来工程分解；同时把
R3–R9 共审绑定为首个 Stage‑2 的全局前置。Owner 明确指出：R1 正是“计划研究但论证后日落”的实例，
说明候选编号不是工程身份；首个条件 GO 方向完成自身调研后应独立进入工程，同时并行调研下一候选。
**Decision：** R1–R9 只保留为 Stage‑1C 调研/审计 provenance。一个独立研究对象只有在关闭自身充分
调研、owner GO 与执行合同后，才按具体语义名称创建独立 GitHub 仓；本地统一置于 umbrella 的
`studies/<semantic-slug>/`，但由自身 Git 管理。R1 在入场前日落，不建空仓。W1–W4 保留为独立 work
repos，不再承载主程序或默认拥有新 study。Stage 按方向独立记账：一个 study 工程期间可并行调研下一个
候选，完成所有候选调研不是全局 Stage‑2 前置。umbrella Wiki 是实验生命周期与资产图的管理平面；study
repo 管代码/配置/测试，`SPEECHRL_DATA_DIR` 与 MLflow 管大型资产和运行数据。
**Consequences：** 新增 umbrella-owned `studies/README.md`/`registry.json`，但只登记已获
`OWNER_GO_AND_EXECUTION_CONTRACT` 的 study；当前为 0。首个计划对象以“audio-aware evidence
acquisition”为工作语义名，仍需关闭 v3 清单和执行合同，未授权远程建仓或实验。新增
[[Experiment-Assets]]；旧 574-row W1 attempt inventory 保持历史字节，刷新索引得 573 live、1 Git-history-
only、0 unresolved。当前 HOT/CURRENT、repo/working/onboarding 资产同步原位更新。
**Supersedes：** 取代 W1=primary-program carrier、候选编号=工程目录、R3–R9 全量共审=首个 study 工程
统一前置、R5+R6+R8=所有 Stage‑2 唯一入口的说法；不改变 TF-Strict/API-only 北极星，也不产生模型/API、
下载、metric、prototype、remote repo、push 或 Wiki publication 权限。失效条件：owner 改变 repo ownership、
study admission gate、实验资产权威边界，或批准首个语义 study 的执行合同。

**2026-08-03 · Owner GO：audio-aware evidence acquisition 建独立仓入工程，数据线并入语义路径：**
**Context：** round-22 已给 `FORMAL_OPENING_APPROVED`（执行仍 withheld）；目录重整提案经评审通过并由
Fable5 返回 ACCEPT_WITH_AMENDMENTS；数据侧 D0 已闭（E21/E22/ConEC 固定 revision + canonical lock）。
**Decision：** owner 签发 `OWNER_GO_AND_EXECUTION_CONTRACT`。创建私有仓
`chaosxingxc-orion/audio-aware-evidence-acquisition`（master），checkout 至
`studies/audio-aware-evidence-acquisition/` 并登记 registry；冻结字段（runtime=llama.cpp+Qwen3-Omni-30B
GGUF、载体三键、mandatory 缩减集、R0 预算带 ≤3000 调用/≤40 GPU 时/付费 API=0、exposure 四字段台账）
落 `wiki/experiments/audio-aware-evidence-acquisition/2026-08-03-owner-go-and-execution-contract.md`，
未逐字段指定者按 Fable5 建议值 DEFAULT 生效、可带日期 amendment 修改。数据采集收据路径由
`docs/checks/r2-stage2a-data/` 语义化为 `docs/checks/audio-aware-evidence-acquisition/`。
**Consequences：** registry 首条 lifecycle=engineering；实验台账 `wiki/experiments/<slug>/README.md` 建立
（ID 空间 AAEA-E-<nnn>）；工程 session 主场移至 study checkout；E0（D1–D4）+runtime 收据是首次模型触达
的 fail-closed 前置；survey delta lane 与程序簿记留伞仓。
**Supersedes：** 取代「registry 当前为 0、未授权远程建仓」的上一条现状；失效条件：owner 撤回/修订执行
合同或 STOP_THE_LINE 触发。

**2026-08-03 · Stage‑1B 程序级 Lean 形式层退役；公式证明按 study 在 Stage‑2 重构：**
**Context：** owner 复盘判定 Stage‑1B 存在过量设计——本应用于详细分析的阶段过度投入了原理研究与公式
讨论；程序级通用形式层（`proofs/tfrl` 23 个 Lean 源、`scripts/lean_axiom_gate.sh` 门禁、
`docs/checks/lean-axiom-gate/` 收据）不再承载当前研究。
**Decision：** 统一删除上述三件（Git 历史保留字节）；形式证明推迟到 Stage‑2，由各获准研究对象在自己
的 study 仓内按自身主张分别重构——不同研究对象应有不同的公式证明，不再维护程序级通用证明库。
**Consequences：** CLAUDE/AGENTS 门禁句与 `wiki/Research-Objective.md` formal 节原位更新；
`wiki/survey/current/research-directions.md` 各方向的「Lean 义务」保留（其语义=per-study Stage‑2 义务，
与本裁决一致）；Stage‑1B v5 调研映射与 H5 `WITHHOLD_NON_LOAD_BEARING` 不受影响。
**Supersedes：** 取代「Lean proofs live in proofs/tfrl + axiom gate 在册」的现状描述。失效条件：owner
重启程序级形式层。

**2026-08-03 · W1–W4 历史 work 仓退役删除（本地即刻、远端待 token 授权）：**
**Context：** owner 裁定 `projects/` 下四个 work 仓是历史工作产物（W1 legacy 探针线、W2/W3 支撑骨架、
W4 已另行重定位），研究主线已由 admitted study 承载。
**Decision：** 本地与云端全部删除。删除前保全：study 仓迁移清单登记的十个 W1 候选文件按
copy-and-verify 快照入 `reference/w1-snapshot/`（源 commit `7ed41f62`、SHA-256 清单、未整合状态）；
四仓终态 HEAD 与 W2/W3 未提交 config 微调存墓碑
`wiki/archive/program/w1-w4-retirement/2026-08-03-w1-w4-retirement-tombstone.md`。本地删除即刻执行
（W1 目录留空壳至会话结束）；远端删除因 gh token 缺 `delete_repo` scope 待 owner 授权后执行。
**Consequences：** CLAUDE/AGENTS 表与命令区、CONTRIBUTING 仓类、Per-Work-Status 四节墓碑化原位更新；
legacy 574 行 attempt inventory 保持历史字节、解析面按设计转 unresolved；scratch 空目录与 hf_probe*
残留同日清除。
**Supersedes：** 取代「W1–W4 保留为独立 work repos」的架构描述（2026-08-02 条目相应部分）。失效条件：
owner 决定恢复某一 work 仓（从远端 re-clone，若远端已删则不可恢复）。

**2026-08-03 · W1–W4 远端保留冷备份；程序运行节奏定型（Stage‑1 伞仓 / Stage‑2 开仓 / 数据模型公共职能）：**
**Context：** 同日稍早退役条目将远端删除记为待 `delete_repo` token 授权。owner 随后裁定远端不删。
**Decision：** ①四个 work 仓远端保留为**冷备份**，仅从伞仓解除链接（活跃面零引用，URL 只存墓碑）；
本地删除维持。②运行节奏定型：每个新研究课题的 Stage‑1（详细讨论、调研、论证）在伞仓完成；完成
Stage‑1 进入 Stage‑2 时开独立 study 仓，此后全部工作在该 study 自己的工作目录完成。伞仓长期保留
**数据与模型下载职能**（`docs/datasets.lock.json` + `scripts/data/`，数据/模型是各 studies 的公共
资产）；除此之外各 studies 的 Stage‑1 都在伞仓完成。
**Consequences：** 墓碑追加当日 addendum；Per-Work-Status/CLAUDE/AGENTS 措辞由「删除待授权」改
「冷备份」；不再需要 `delete_repo` scope；CLAUDE/AGENTS Repository 节补运行节奏句。
**Supersedes：** 同日退役条目中「远端删除待 token 授权」部分；运行节奏为 2026-08-02 架构条目的
操作化细则。失效条件：owner 决定真删远端或恢复某 work 仓。

**2026-08-03 · 伞仓公共职能定型：数据三层拆分、「发表即晋升」管线，不设污染档案：**
**Context：** 目录重整与 W1–W4 退役后，owner 与 Fable5 就伞仓公共职能完成四轮辩论（基线记录拆分、
载体消耗账、切分归属、发表结晶）。
**Decision：** ①数据三层拆分：数据集本体=gold truth 不变量（伞仓 lock）；使用方案（split/采样/
prompt/协议/加载内容）=study 私有；伞仓**不设**「载体污染/消耗」档案。②发表即晋升：study 的
切分/采样随论文发表结晶为**新数据集**晋升入伞仓——构建方式（可复现派生脚本入 `scripts/data/`）
+数据留档（样本身份/hash 入 lock）+provenance（源数据集、来源 study/论文、当时角色）。先例=
Rare5k（`derive_rare5k.py`+lock reconstruction 条目）。③程序级可见性两句纪律：写侧=confirmatory
消耗的实验台账行必须显式带 split 身份 hash 与「已消耗」标记；读侧=新 study 的 Stage‑1 载体选型
必须扫描既有 study 实验台账+exposure 台账，给出带范围的继承 exposure 声明（四字段纪律的点名
适用）。④伞仓公共职能终表：数据+模型下载、基线身份档案（身份/readiness/exact-revision pin；
运行读数归 study；档案文件待 R1 复现队列冻结时落）、各 study 的 Stage‑1 讨论调研场、文献调研
基建（ledger/registry/fetch 管线）、运行时 pin 档案、治理与门禁。⑤重访触发器：当第二个 study
与既有 study 实际共用载体时，把「按载体聚合视图」做成只读推导检查（从台账推导，不另存真值）。
**Consequences：** 不新建任何档案文件；实验台账行格式自 R2 首条正式记录起补 split-hash 与消耗
标记列。
**Supersedes：** 细化本日「运行节奏」条目的数据职能部分。失效条件：owner 调整公共职能表。

**2026-08-03 · Stage‑1 调研包整体封存：CURRENT 类退役、主门禁退役、横切保护移交：**
**Context：** owner 裁定调研包「整体清理掉」；独立批判代理复核出 14 项风险（三条 KEEP→DELETE
断边、campaign 索引硬编码载体、搬运合法性、.gitattributes 行尾陷阱、文献收件地址在归档区等），
执行方案按其修订。
**Decision：** ①`wiki/survey/current/`（158 件）与门禁绑定散件保 blob 归档至
`wiki/archive/working/system-first-survey-current/` 与同级 campaign 目录；official-metadata 库
（118 件+回执）迁入 REGISTRY 文献公共层 `wiki/survey/registry/`。②主门禁
`sf_current_package_check` 及 current 层引擎群退役（10 模块+7 测试）；保留审计不可变检查、
声明式合同引擎、文献抓取管线与 bibliography 库件。③横切保护移交新件：
`scripts/checks/code_graph_check.py`（受信代码图三方相等+未跟踪代码禁令+软链拒绝）与
`scripts/checks/atomic_write.py`。④**正典澄清（安全移动门语义）**：不可变审计记录中的
`wiki/survey/current/...` 路径与 spec 引用是**溯源指针而非活指针**，由封存 digest 的强规格映射表
（旧路径|新路径|blob）与检查器内的前缀重定位（`CURRENT_LAYER_RELOCATION`）解析，不构成
inbound-reference 搬运阻断；commit-pinned `git show <sha>:<path>` 取回不受影响。⑤七类分类法
降为六类：CURRENT 类成员归零后从分类器、政策常量与本表移除；ARCHIVE 准入判据由「被 CURRENT
取代」改为「**闭合**（完成、被取代或废弃）且无活跃依赖」。
**Consequences：** 伞仓门禁=code_graph/study_workspace/ai_context_surface/build_manifest --check
四道；ai-context 活跃条目 20→11；oracle 测试面同 commit 重钉（surface 120 绿、全仓 199 绿、审计
111 件不可变 PASS）；campaign 索引生成器随 stage1a 战役闭合退役，既有 INDEX 冻结为史料。
**Supersedes：** 「sf_current_package_check 是伞仓真门禁」的表述与 CURRENT 类的一切现行语义。
失效条件：owner 重启程序级调研包制度。

**2026-08-04 · 现役 study 收窄为 speech-only，并完成语义身份、远端仓与数据绑定迁移：**
**Context：** owner 复核 R2 数据清单后指出，当前研究聚焦 speech domain；过去文献扫描把 speech
音频载体与 general/environmental audio 任务混为一谈，并出现“论文新增数据集即自动下载/实验”的
范围膨胀。同时，FSD50K、AudioSet 等资产已耗时完成下载，owner 明确要求保留本地字节而非删除。
**Decision：** ①有效研究对象由 `audio-aware evidence acquisition` 收窄并重命名为
`speech-aware evidence acquisition`，远端改名
`chaosxingxc-orion/speech-aware-evidence-acquisition`，本地 checkout、Wiki experiment/check 目录、
Python package 与实验 namespace 统一为 speech-aware / `SAEA-E`。②研究范围只含 ASR、实体、
contextual biasing、spoken QA、会议语音等 speech/spoken-language 任务；speech 的 WAV/MP3 输入仍是
合法载体，排除的是 general-audio task，不是所有音频文件。③ Stage‑2 数据绑定：Earnings21/22+
ConEC 为 core，SLUE-SQA-5、ContextASR-Bench、AMI 为 secondary speech；FSD50K、AudioSet、ESC-50
保持本地 `COMPLETE`，转为 `retained-cross-domain`，不得进入本 study 的实验、baseline 或结论。
④ profile 从候选号 `r2-*` 迁移为 admitted study 的 `speech-aware-*` 语义名。⑤有效合同明确分离
OBS、知识组织 ORG、证据供给 SUPPLY、知识使用 USE，并冻结 effectiveness、reasonableness、
efficiency 三类评价；新增论文只有被具体预注册实验/baseline 消费时才产生下载提案。
**Consequences：** 2026-08-03 原 GO 合同与正式开题审计件保留当时事实；当前自包含权威改为
`wiki/experiments/speech-aware-evidence-acquisition/2026-08-04-owner-speech-domain-scope-and-identity-contract.md`。
不删除 `SPEECHRL_DATA_DIR` 中任何已验证资产；Stage‑2A 立即转向 E0→R0，不再以新增下载阻塞工程。
**Supersedes：** 取代 2026-08-03 GO 条目中的旧 semantic identity、路径、远端、`AAEA-E` 及过宽
audio-domain 表述；GO、预算与 fail-closed 授权继续有效。失效条件：owner 另行修改 study domain、
身份或数据保留政策。
