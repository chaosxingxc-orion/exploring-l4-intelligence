---
artifact_id: "SF-STAGE1C-R2-SIGNATURE-SHEET-V4"
role: "R2 开题签字表：一页纸签字依据（正文可长、签字对象不可歧义）——随 v20 交付（round-21 整改版：RQ0 析因、结论向量、十二判据三态真值表、K-NB 全称反证、RQ4a 拆分、控制器权威定义、载体族双 split、最小确认路径）"
companion_of: "2026-07-29-r2-coreview-draft.md (V20)"
date: "2026-08-02"
status: "DRAFT_FOR_OWNER_SIGNATURE_REVIEW; owner 未签"
supersedes: "V3（companion_of V19）及更早——本表为签字对象的唯一现行版"
---

# R2 开题签字表（一页）

**总研究问题（一句话）**：在核心 speech/omni 模型冻结、内部状态不可依赖的条件下，如何
围绕语音任务构造可组织（ORG）、可选择供给（SUPPLY）、可审慎使用（USE）的外部知识控制
系统，并分别评价知识引入的必要性、有效性、合理性、可靠性与效率？
**递进子问题（承诺面=实验可识别面）**：RQ0 必要性与错误分型（识别面=**OBS×外证 2×2
析因**+预注册错误分型，各分量独立 estimand）／RQ1 组织——本轮主问题=key/索引/切片/面
（value/schema/版本/出处=工程合同+后续分支）／RQ2 供给——本轮主实验=供给源选择
（K-SUP）／RQ3 使用——本轮主问题=证据准入（融合/冲突/引用/拒答=后续分支）／RQ4a-1
双源按样本动作选择（等预算析因识别）／RQ4a-2 序贯策略与优化器身份／RQ4b 系统评价。
**总答案=RQ0–RQ4b 结论向量**（各按其判据独立三态、多载体综合、不合成单一总标签——
既有"五类结论不得互相替代"之 RQ 级延伸）。技术模块=
RQ 的候选方案；WP 总表+RQ 卡片表+总问题级治理路由表+模块唯一映射表=正文 §1.0。
**谱系定位（描述性；本阶段对新颖性双向出域——不作首创主张、不必证明交集无占据，
边界裁定在案）**：RECOVER 已实现 API-only/training-free/文本侧外显 rescore；长音频线已有
结构化多流库与多维图上的 training-free 规划检索（PlanRAG-Audio/GRGA，知识源封闭于同
录音、无准入门）；R2 方法差异锚=按样本**双源信息获取动作选择**（门控选择性重解析+外部
检索调度）与真假证据准入的耦合（正文 §1.7 五线地图+§8 二十一件矩阵）。

**主假设（可独立证伪；RQ 对应——H-SUPPLY/H-CONTROL 分量/H-USE/H-SYS 四条+前置 H0 与
H-ORG 括注）**
- **H-SUPPLY（RQ2，供给源价值主实验）**：逐源供给（slides/财报稿/参会者）优于等表长
  合并对照——判据 K-SUP（三态判读；判定载体=NB 主载体 SRC-sel 臂；含总 WER 对合并
  对照非劣之成立侧否决条件）。
- **H-CONTROL 之双源选择分量（RQ4a-1，音频特有机制主张）**：读取音频不确定性信号的调度
  （A4b）优于不读取者（A4a）——判据 K1b（三重合取：A4b−A4a paired delta 下置信界>0
  ∧ β 向量联合与零可区分 ∧ A4b 胜过 serial-composition 无条件双源串行固定臂；判定载体
  =NB 主载体）；序贯策略（档B−档A）=K-RL、档A 方法位=K-OPT。
- **H-USE（RQ3，知识使用）**：同证据集下显式准入优于无条件拼接（融合/冲突处理=后续支线），且降低
  correct→wrong——判据 K4（A3−A2）。
- **H-SYS（系统级整体读数；配置族最佳效果主张——全称"预注册配置族内最佳已测系统效果"，
  非模型/任务上界；高风险假设非前提）**：主张臂（运行时无专用ASR前端）在主载体上对**全部
  入判组（含⓪无上下文强专用 ASR）×两主指标合取**成立，**且过 §7 K-NB 成立侧护栏族四条**
  （总 WER 对自身裸核非劣/worst-group 非劣/correct→wrong 上界/abstain 带宽——防"修好
  实体毁掉整句"）——判据 K-NB（dev 选定臂；全称主张反证逻辑=任一 mandatory 对手经预注册反向检验证优
  即判死；mandatory baseline set 预注册冻结不可事后缩减、对手不可运行记
  INCONCLUSIVE_BASELINE_NOT_READY；SPLIT_GROUP/SPLIT_READING=未获支持出口非反证）；
  trained 上界对照不及则改判"增强"。
  （前置 H0/RQ0：gold-evidence〔A1′ masked 口径〕相对裸核存在超 SESOI 的 oracle
  headroom——判据 K0〔OBS×外证 2×2 析因之外证主效应；OBS 主效应/交互并行报告〕，
  否则供给/使用杠杆不评；A1 gold-entity=OBS 侧读数不入 H0。
  H-ORG/RQ1=O-config 三臂，判据 K5，判死权仅 K5-t。）

**三形式+两横切轨→模块映射（唯一词典，正文 §1.3）**：ORG=知识以何单元/索引/切片/面存在（knowledge builder；K5——schema/版本/出处=工程合同+后续分支、本轮非实验对象）；SUPPLY=供给源与候选证据之变量面（本轮主实验=供给源选择、判据=K-SUP；何时取/取多少=条件参数、触发/停止裁决归 CONTROL）；USE=已取回证据之准入/拒用（admission；K4——融合/冲突/引用=后续支线）；**OBS**=重听/重切/多假设（观测
重处理，非知识形式——`RE_RESOLVE/RE_SLICE` 属此轨）；**CONTROL/OPT**=在各轨动作与配置
间选择（router 主层判据=K1a/K1b/K2）＋dev reward→冻结配置（档 A；K-OPT）/有限时域序贯
决策策略（档 B——dev 学 test 冻结种子重放、"contextual bandit"旧称退役；K-RL，方法
身份承载——owner 裁定在案）。
主实验一次只改一层；工作包 WP1 组织（RQ0/RQ1）/WP2 供给与控制（RQ2/RQ4a）/WP3 使用与
评价（RQ3/RQ4b），最低学术产出与失败出口见 §1.0 总表。

**载体（身份已冻结；数值预注册=Stage-2A 第零步）**
- 主载体数据包=**Earnings21 音频/评测集+ConEC version-pinned 上下文与修订转写层**（真实
  slides/财报稿/参会者名单；reference 采 ConEC 修订版、对照处双报；实体子切片承接官方
  24 类标注）。**dev/标定=Earnings-22+ConEC 层**（Earnings-21 只作 evaluation；全部可调项
  dev 侧冻结；按 call/company 分组防泄漏）。主载体为分布内载体：直接支持"选择性上下文
  增强与动作选择"结论；参数外知识时态结论待后 cutoff/私域第二载体（义务在案）。
- 复制载体=TED-LIUM3；诊断集=PRISM 词典协议（全合成）；组④对照=LibriSpeech+Rare5k
  （实体子切片单独报数）；自建载体族=discovery/confirmatory 双 split（阈值/prompt/标注
  规则于 discovery 调定、K0/K4 正式判定唯出 confirmatory；按源音频/说话人/主题去泄漏）。

**最强基线（⓪–⑥七组信息边界+同载体阶梯）**：⓪无上下文强专用 ASR（Whisper-large 级，
入判组）①朴素族（Double Metaphone 级强实现钉死/KBBS)
②in-context 词典注入（DICT-SCALE 规模扫描）③白盒参照上界（PRISM/WCTC，不入对手集）
④trained 上界（RECAST/BR-ASR@LS+Rare5k；另：Huang24f@ConEC=同载体训练对手、非上界、
不可运行、**不入④**）⑤retrieval-GER（对照钉原载体侧）⑥黑盒上下文发现（Siskos 重实现后入判）；同载体
阶梯：no-context→ConEC 真实上下文 shallow fusion→ConEC oracle（9.69；稀有词 WER 余量约
6pp；总 WER 本载体 READOUT_ONLY——偏置杠杆天花板≈0.7 点+强核零上下文已越 oracle）
→Fox 词表（诊断级、test-gold 派生不进 controller）→RECOVER 1-Best（TF 黑盒后处理强制
对照臂、重实现后入判）→裸核→主张臂；另设 serial-composition/always/never/random-matched-cost
/ASR-dump 固定对照族。

**主判据与判定判据（本段为摘要口径、判据细则与出口一律以正文 §7 条款为准；三态总则：
SUPPORTED／REFUTED_OR_NEGLIGIBLE〔判死须过预注册反向
等效/非劣检验、"未证正效应"不构成判死〕／INCONCLUSIVE〔SPLIT/PENDING 族归入〕）**：
主判据=效果绝对提升（paired delta+CI+SESOI+多重性校正；效率之比较性 estimand=每有效
实体修正边际成本、不进主判据）。判死/降级出口全数预注册：K0（必要性：A1′−A0 无
headroom→该载体供给/使用杠杆不评）、K-SUP（供给源选择，RQ2 主判据）、K1a
（调度不敌固定档→判死）、K1b（合取命题：全部分量支持才成立、任一承重分量被正式反证则推翻→MERGE 路由、仅未获
支持=不确定；判定载体=NB 主载体）、
K-NB（配置族最佳效果判死/改判"增强"；对手含⓪无上下文强专用 ASR）、K-PS（发音库降
工程件）、K-XOVER（价值窗口判空→**该载体**回退梯；改挂另有二充分条件=§2.3 中止规则
或窗口存在∧子消融①为负，全局生效受 §7 灵敏度前置检定）、K-OPT（档 A 不赢等预算随机
搜索→不立方法主张）、K4（判定载体=载体族 confirmatory split 多 claim 子层）/K5/K2/K3/K-Gate/K-RL；
灵敏度前置五条（含本核余量下限与查询/检索两级 headroom 分账）+判别力三分+§5.3 四级
回退梯——判死永不在无分辨力载体上宣布。评价按 Need→Access→Use→Outcome→Cost 五段链
组织（§1.0），必要性/有效性/合理性/可靠性/效率五类结论不得互相替代。

**数据隔离与知识时态**：test gold 永不进 controller；Earnings21 只作最终 evaluation；每场
call 资料记录来源/hash/available_at，"当时可得/事后可得/gold oracle"三臂分立；检索快照
冻结、复放合同全程 trace。

**权限边界**：红线四条（不改参数/不新训模型〔权威口径：本轮零模型参数训练、新引入模型
一律 frozen 已发布检查点；外置控制器=非模型——无梯度、有限决策常量 dev 标定 test 冻结，
不属此列〕/不新增代答 LLM/克隆边界——enrollment 仅会话内当事人、不留存、不对外播放、
不涉第三方 PII）；本签字仅授权开题成立性；Stage-2A 执行
（模型/API/数据/指标）另需 authorization（义务清单全列于 §9）。

**owner 签字栏**：＿＿＿＿（结论/日期/Decision-Log 条目号）
