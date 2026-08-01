---
artifact_id: "SF-STAGE1C-R2-SIGNATURE-SHEET-V2"
role: "R2 开题签字表：一页纸签字依据（正文可长、签字对象不可歧义）——随 v18 交付（round-19 边界纠偏整改版）"
companion_of: "2026-07-29-r2-coreview-draft.md (V18)"
date: "2026-08-01"
status: "DRAFT_FOR_OWNER_SIGNATURE_REVIEW; owner 未签"
supersedes: "V1（companion_of V17.1；其「独立性承重」段按续85① 新颖性双向出域改为谱系定位段——本表为签字对象的唯一现行版）"
---

# R2 开题签字表（一页）

**总研究问题（一句话）**：在核心 speech/omni 模型冻结、内部状态不可依赖的条件下，如何
围绕语音任务构造可组织（ORG）、可选择供给（SUPPLY）、可审慎使用（USE）的外部知识控制
系统，并分别评价知识引入的必要性、有效性、合理性、可靠性与效率？
**递进子问题**：RQ0 必要性与边界（观测不足≠知识缺口）／RQ1 组织／RQ2 供给（含声学不
确定性下的双源比价）／RQ3 使用（准入/冲突/拒答）／RQ4 控制与评价。技术模块=RQ 的候选
方案；模块→RQ→层→变量→对照→判据→失败出口唯一映射表=正文 §1.0。
**谱系定位（描述性；本阶段对新颖性双向出域——不作首创主张、不必证明交集无占据，
边界裁定在案）**：RECOVER 已实现 API-only/training-free/文本侧外显 rescore；长音频线已有
结构化多流库与多维图上的 training-free 规划检索（PlanRAG-Audio/GRGA，知识源封闭于同
录音、无准入门）；R2 方法差异锚=按样本**双源信息获取动作选择**（门控选择性重解析+外部
检索调度）与真假证据准入的耦合（正文 §1.7 五线地图+§8 二十一件矩阵）。

**三条主假设（可独立证伪；RQ 对应）**
- **H-SUPPLY（RQ2，音频特有供给，最核心机制主张）**：读取音频不确定性信号的调度（A4b）
  优于不读取者（A4a），且降低错误实体引发的错误检索链——判据 K1b（合取：paired delta
  下置信界>0 ∧ β 权重与零可区分）。
- **H-USE（RQ3，知识使用）**：同证据集下显式准入/冲突处理优于无条件拼接，且降低
  correct→wrong——判据 K4（A3−A2）。
- **H-SYS（系统级整体读数；配置族最佳效果主张——全称"预注册配置族内最佳已测系统效果"，
  非模型/任务上界；高风险假设非前提）**：主张臂（运行时无专用ASR前端）在主载体上对入判组
  paired delta 下置信界>0——判据 K-NB；trained 上界对照不及则改判"增强"。
  （前置 H0/RQ0：gold-evidence〔A1′ masked 口径〕相对裸核存在超 SESOI 的 oracle
  headroom——判据 K0，否则供给/使用杠杆不评；A1 gold-entity=OBS 侧读数不入 H0。
  H-ORG/RQ1=O-config 三臂，判据 K5，判死权仅 K5-t。）

**三形式+两横切轨→模块映射（唯一词典，正文 §1.3）**：ORG=知识以何单元/schema/索引/
版本/出处存在（knowledge builder；K5）；SUPPLY=何时取/从哪取/取多少/何时停（controller/
retriever；K1a/K1b/K2）；USE=已取回证据的准入/融合/冲突/拒用（admission/arbitration；
K4）；**OBS**=重听/重切/多假设（观测重处理，非知识形式——`RE_RESOLVE/RE_SLICE` 属此轨）；
**CONTROL/OPT**=dev reward→冻结配置（档 A）/contextual bandit 运行期策略（档 B；K-RL，
方法身份承载——owner 裁定在案）。主实验一次只改一层；工作包 WP1 组织（RQ0/RQ1）/WP2 供给与控制
（RQ2/RQ4）/WP3 使用与评价（RQ3/RQ4），最低学术产出与失败出口见 §1.0 总表。

**载体（身份已冻结；数值预注册=Stage-2A 第零步）**
- 主载体数据包=**Earnings21 音频/评测集+ConEC version-pinned 上下文与修订转写层**（真实
  slides/财报稿/参会者名单；reference 采 ConEC 修订版、对照处双报；实体子切片承接官方
  24 类标注）。**dev/标定=Earnings-22+ConEC 层**（Earnings-21 只作 evaluation；全部可调项
  dev 侧冻结；按 call/company 分组防泄漏）。主载体为分布内载体：直接支持"选择性上下文
  增强与动作选择"结论；参数外知识时态结论待后 cutoff/私域第二载体（义务在案）。
- 复制载体=TED-LIUM3；诊断集=PRISM 词典协议（全合成）；组④对照=LibriSpeech+Rare5k
  （实体子切片单独报数）。

**最强基线（六组信息边界+同载体阶梯）**：①朴素族（Double Metaphone 级强实现钉死/KBBS)
②in-context 词典注入（DICT-SCALE 规模扫描）③白盒参照上界（PRISM/WCTC，不入对手集）
④trained 上界（RECAST/BR-ASR@LS+Rare5k；另：Huang24f@ConEC=同载体训练对手、非上界、
不可运行、**不入④**）⑤retrieval-GER（对照钉原载体侧）⑥黑盒上下文发现（Siskos 重实现后入判）；同载体
阶梯：no-context→ConEC 真实上下文 shallow fusion→ConEC oracle（9.69；稀有词 WER 余量约
6pp；总 WER 本载体 READOUT_ONLY——偏置杠杆天花板≈0.7 点+强核零上下文已越 oracle）
→Fox 词表（诊断级、test-gold 派生不进 controller）→RECOVER 1-Best（TF 黑盒后处理强制
对照臂、重实现后入判）→裸核→主张臂；另设 serial-composition/always/never/random-matched-cost
/ASR-dump 固定对照族。

**主判据与 kill criteria**：主判据=效果绝对提升（paired delta+CI+SESOI+多重性校正；效率
九维记账不进主判据）。判死/降级出口全数预注册：K0（必要性：A1′−A0 无 headroom→供给/使用杠杆不评）、K1a
（调度不敌固定档→判死）、K1b（双源独立性合取不成→MERGE 路由；判定载体=NB 主载体）、
K-NB（配置族最佳效果判死/改判"增强"；对手含⓪无上下文强专用 ASR）、K-PS（发音库降
工程件）、K-XOVER（价值窗口判空→改挂语音学检索+rescore）、K-OPT（档 A 不赢等预算随机
搜索→不立方法主张）、K4（判定载体=先导多 claim 子层）/K5/K2/K3/K-Gate/K-RL；
灵敏度前置五条（含本核余量下限与查询/检索两级 headroom 分账）+判别力三分+§5.3 四级
回退梯——判死永不在无分辨力载体上宣布。评价按 Need→Access→Use→Outcome→Cost 五段链
组织（§1.0），有效性/合理性/可靠性/效率四类结论不得互相替代。

**数据隔离与知识时态**：test gold 永不进 controller；Earnings21 只作最终 evaluation；每场
call 资料记录来源/hash/available_at，"当时可得/事后可得/gold oracle"三臂分立；检索快照
冻结、复放合同全程 trace。

**权限边界**：红线四条（不改参数/不新训模型/不新增代答 LLM/克隆边界——enrollment 仅会话
内当事人、不留存、不对外播放、不涉第三方 PII）；本签字仅授权开题成立性；Stage-2A 执行
（模型/API/数据/指标）另需 authorization（义务清单全列于 §9）。

**owner 签字栏**：＿＿＿＿（结论/日期/Decision-Log 条目号）
