---
artifact_id: "SF-STAGE1C-R2-SIGNATURE-SHEET-V1"
role: "R2 开题签字表：一页纸签字依据（正文可长、签字对象不可歧义）——随 v17 交付"
companion_of: "2026-07-29-r2-coreview-draft.md (V17)"
date: "2026-08-01"
status: "DRAFT_FOR_OWNER_SIGNATURE_REVIEW; owner 未签"
---

# R2 开题签字表（一页）

**研究问题（一句话）**：在 API-only 冻结 omni 核上，外置知识系统（实体发音库+世界知识+
面 key 联邦+T2 库）经门控查询-裁决环调度，能否在实体/知识密集语音任务上以 training-free
方式取得超过"专用 ASR+biasing/GER"管线的任务效果上界，并将收益归因到组织/供给/使用三层？

**三条主假设（可独立证伪）**
- **H-SUPPLY（音频特有供给，最核心独立性主张）**：读取音频不确定性信号的调度（A4b）优于
  不读取者（A4a），且降低错误实体引发的错误检索链——判据 K1b（合取：paired delta 下置信
  界>0 ∧ β 权重与零可区分）。
- **H-USE（知识使用）**：同证据集下显式准入/冲突处理优于无条件拼接，且降低 correct→wrong
  ——判据 K4（A3−A2）。
- **H-SYS（能力上界，高风险假设非前提）**：主张臂（运行时 ASR-free）在主载体上对入判组
  paired delta 下置信界>0——判据 K-NB；trained 上界对照不及则改判"增强"。
  （前置 H0：gold entity/evidence 相对裸核存在超 SESOI 的 oracle headroom，否则不进主实验。）

**三形式→模块映射**：组织 ORG=知识以何单元/schema/索引/版本/出处存在（knowledge builder；
判据 K5）；供给 SUPPLY=何时取/从哪取/取多少/何时停（controller/retriever；K1a/K1b/K2）；
使用 USE=已取回证据的准入/融合/冲突/拒用（admission/arbitration；K4）；优化 OPT=dev
reward→冻结配置（档 A）/contextual bandit 策略（档 B；K-RL）。主实验一次只改一层。

**载体（身份已冻结；数值预注册=Stage-2A 第零步）**
- 主载体数据包=**Earnings21 音频/评测集+ConEC version-pinned 上下文与修订转写层**（真实
  slides/财报稿/参会者名单；reference 采 ConEC 修订版、对照处双报；实体子切片承接官方
  24 类标注）。**dev/标定=Earnings-22+ConEC 层**（Earnings-21 只作 evaluation；全部可调项
  dev 侧冻结；按 call/company 分组防泄漏）。
- 复制载体=TED-LIUM3；诊断集=PRISM 词典协议（全合成）；组④对照=LibriSpeech+Rare5k
  （实体子切片单独报数）。

**最强基线（六组信息边界+同载体阶梯）**：①朴素族（Double Metaphone 级强实现钉死/KBBS）
②in-context 词典注入（DICT-SCALE 规模扫描）③白盒参照上界（PRISM/WCTC，不入对手集）
④trained 上界（RECAST/BR-ASR@LS+Rare5k；另：Huang24f@ConEC=同载体训练对手、非上界、
不可运行、**不入④**）⑤retrieval-GER（对照钉原载体侧）⑥黑盒上下文发现（Siskos 重实现后入判）；同载体
阶梯：no-context→ConEC 真实上下文 shallow fusion→ConEC oracle（9.69；稀有词 WER 余量约
6pp；总 WER 本载体 READOUT_ONLY——偏置杠杆天花板≈0.7 点+强核零上下文已越 oracle）
→Fox 词表（诊断级、test-gold 派生不进 controller）→裸核→主张臂；另设 serial-composition/always/never/random-matched-cost
/ASR-dump 固定对照族。

**主判据与 kill criteria**：主判据=效果绝对提升（paired delta+CI+SESOI+多重性校正；效率
九维记账不进主判据）。判死/降级出口全数预注册：K1a（调度不敌固定档→判死）、K1b（双源
独立性合取不成→MERGE 路由）、K-NB（能力上界判死/改判"增强"）、K-PS（发音库降工程件）、
K-XOVER（价值窗口判空→改挂语音学检索+rescore）、K4/K5/K2/K3/K-Gate/K-RL；灵敏度前置四条
+判别力三分+§5.3 四级回退梯——判死永不在无分辨力载体上宣布。

**数据隔离与知识时态**：test gold 永不进 controller；Earnings21 只作最终 evaluation；每场
call 资料记录来源/hash/available_at，"当时可得/事后可得/gold oracle"三臂分立；检索快照
冻结、复放合同全程 trace。

**权限边界**：红线四条（不改参数/不新训模型/不新增代答 LLM/克隆边界——enrollment 仅会话
内当事人、不留存、不对外播放、不涉第三方 PII）；本签字仅授权开题成立性；Stage-2A 执行
（模型/API/数据/指标）另需 authorization（义务清单全列于 §9）。

**owner 签字栏**：＿＿＿＿（结论/日期/Decision-Log 条目号）
