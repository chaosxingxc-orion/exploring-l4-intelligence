---
title: "R2 round-20 逐项回应与对抗核验：14/14 引文属实（零定性错、3 处小修正）、6 MAJOR 采 4 半采 2、MAJOR-3 取方案 B（续82③）"
date: "2026-08-01"
artifact_type: "RESPONSE"
campaign: "system-first-stage1c-v2"
round: "round-20"
response_target: "wiki/audit/system-first-stage1c-v2/round-20/2026-08-01-r2-v18-multiround-adversarial-doctoral-supervisor-review.md"
review_target: "proposals/2026-07-29-r2-coreview-draft.md @ eea6695 blob e837886a（工作树逐字节亲验一致）"
verification_channels: "①blob/正文指控=主会话亲验（git hash-object+逐行 grep：档 B 张力 L555 vs L842/856、USE 输出 L234、value 非实验轴 L551、'被证伪' L813 全部坐实）；②14 件引文=隔离 Opus 代理一手 WebFetch/ISCA/Anthology/arXiv；③本地覆盖=隔离 Sonnet 代理双目录扫描"
citation_verdict: "14/14 真实存在、零虚构、零定性错误；3 处修正见 §2"
acceptance: "MAJOR-1/2/4/6 采（各带修正注）；MAJOR-3 半采——方案 A 不采（撞续82③ TFRL 身份保留）、取方案 B（有限时域序贯决策合同正式化，恰为续82③ 自身要求）；MAJOR-5 半采——效率取比较性 estimand（每有效实体修正边际成本，不进主判据，续82② 效果优先维持）+可靠性护栏采"
owner_rulings: "Decision-Log 续86"
authority_effect: "RESPONSE_ONLY_NO_EXECUTION_GRANT"
exposure: "隔离代理对 14 件论文官方页/arXiv API 的 WebFetch/WebSearch（引文核验，owner 指示范围内）；零模型/指标/研究数据集执行；继承既有 exposure"
---

# R2 round-20 逐项回应与对抗核验

## §1 核验方法

三通道同 round-19 协议：blob 绑定亲验（`e837886a` @ `eea6695`=v18 终态一致）；14 件引文
隔离一手核验；本地登记面双目录扫描。评审边界遵守情况良好：frontmatter 明文
`novelty_review_in_scope: false`、正文重申不评新颖性/不要求 prior-difference、结论明示
"不是 NO-GO"、round-19 五项判基本/部分关闭——与续85① 一致。

## §2 引文核验：14/14 真实、零定性错、3 处修正

全部 14 件 URL/作者/年份/发表处一致（含 TED-EL"Li et al."、Audiopedia"Penamakuri
et al."、iKnow-audio"Olvera et al."、MoshiRAG"Chien et al."逐一比中；MCR-Bench 名称
经官方 repo 核实属 2025.emnlp-main.246，注意该名不在其摘要、仅在正文/repo）。三处修正：

1. **评审清单第 15 件 "Failing Forward"（2025.findings-acl.125）= DARAG 的正式发表版**
   ——本项目已有其 arXiv 版（2410.13198）全量 D2；评审将其列为 fresh-search 新件属
   重复计数（非虚构）。D2 条目已有 anthology 交叉注。
2. **Siskos 之 anthology 条目（2025.findings-emnlp.768）= 库内 arXiv 2509.19567 同一件
   的正式版**（六作者/三载体/17%与 24.1% 读数全同、arXiv v2 自注 EMNLP 2025 录用）；
   我方 D2 已交叉登记该 anthology id。
3. **CTC-Assisted LLM-Based Contextual ASR（2411.06437）发表处低报**：评审记"2024
   预印本"，实为 **SLT 2024** 正式发表（arXiv comment 在案；作者 Yang et al.）。

本地覆盖分层：对全项目全新 **10 件**（TED-EL/Audiopedia/iKnow-audio/Xiang/MCR-Bench/
CopyNE/Adaptive-CB/CTC-Assisted/N-best T5/HypR）；已在案 4 件（ContextASR-Bench ledger
1351–1352+矩阵/义务位——评审对其位置的描述准确；DARAG=Failing Forward；Siskos 双形态；
MoshiRAG/DeRAGEC/Voice Memory 摘要级）。同姓氏碰撞风险注记（三个不同 Wang 一作）已录，
收编时按年份/venue 消歧。

## §3 六项 MAJOR 逐项回应

**MAJOR-1（RQ 承诺面＞实验识别面）——采。** 四条文本锚全部亲验坐实：value 合同"非实验
轴"（551 行）vs RQ1 承诺；USE 行输出"答案/拒答"与终结动作正典交叉（234 行）；H-SUPPLY
主差分（A4b−A4a）识别对象实为 CONTROL 层对比；RQ4 兜载五判据。v19 动作：RQ 卡片化
（构念→主操纵→同层对照→判定载体→estimand→三态结论→失败后范围）；RQ1 收窄至
key/index/切片/面组织（value/schema/版本/出处降后续分支+工程合同）；RQ2 升 SRC-sel
（供给源选择）为主实验并赋独立判据、A4b−A4a 归 RQ4a/CONTROL；RQ3 收窄为证据准入；
RQ4 拆 4a（CONTROL/OPT）/4b（系统评价）；补总问题级决策表。

**MAJOR-2（直接线缺席+权重失衡）——采，带三点修正（§2）。** 10 件新线经双路核验属实，
其中 TED-EL（2024）/Audiopedia（2024-12）将"语音实体→外部知识"谱系时间线自 2026 前移
至 2024——v18 L4 外部世界知识支的时间线失真指控成立。v19 动作：§1.7 重写（L4 拆三类
信息边界：同录音内/外部音频库/外部世界知识；补入十件并按各自限定收编——iKnow-audio
限定声学类别 tagging 非语音/ASR；ContextASR-Bench 升 L1 主线）；每线固定六问模板；
donor 节加跨域启发定位注；统一 literature cut=2026-08-01；新增标准参考文献表（作者/
题名/venue/年份/DOI-URL/发表态分列）。

**MAJOR-3（档 B 非 contextual bandit+在线 reward 不可观测）——半采：方案 A 不采、取
方案 B。** 指控本体属实且经亲验（555 行"允许在交互中更新" vs 842 行"实际回报仅离线
标定不进在线决策"+856 行 ε-greedy/UCB——在线更新信号无定义；动作改写 H_t/E_t=序贯
结构）。但方案 A（删 K-RL 身份）与 Decision-Log 续82③（TFRL 身份保留、档 B=身份承载、
须按 MDP/bandit 对象正式化）正面冲突——**方案 B 恰为续82③ 自身的落地要求**。v19 动作：
档 B 改写为**有限时域序贯决策合同**（状态/动作/转移/horizon/可观测反馈/奖励延迟/离线
credit assignment/TF-Strict 兼容边界=策略 dev 期学习、test 冻结种子重放——零 test 期
学习，与红线相容）；"contextual bandit"一词退役（治理史原文不动）；K-RL 判据保留、
对象改称序贯策略。

**MAJOR-4（判死语义混"未证正效应"与"证明无效"）——采。** 自证文本锚亲验（813 行
"被证伪"压在 LCB≤0 型读数上）。v19 动作：§7 增三态判定总则（SUPPORTED／
REFUTED_OR_NEGLIGIBLE〔须过预注册等效性/ROPE/非劣反向检验方可判死〕／INCONCLUSIVE
〔含样本不足/区间过宽/载体无分辨力——SPLIT/PENDING 阀族归入此态〕），全格网主判据
统一语义；"被证伪"类措辞同批修正。数值阈值照旧 §9 预注册。

**MAJOR-5（成本账本≠效率评价；可靠性未入成立条件）——半采。** 效率：续82② 效果优先
维持、matched-cost 门不设——取评审选项 2 的最小形态：以 §6.5 既有"**每有效实体修正
边际成本**"升为效率维度的比较性 estimand（描述性报告、**不进主判据**）；五段链 Cost 段
措辞同步。可靠性：采——K-NB 成立侧护栏族扩展（总 WER 之外增 worst-group 非劣与
correct→wrong 上界，护栏型=携成立侧否决权不携判死权、SPLIT_READING 出口；abstain 不得
人为压 coverage 之条款已在 §6.5、上升为护栏注）。

**MAJOR-6（文档角色混载+计划过载）——采。** 196KB/审计史占尾部大半，确与仓内"一份
文档一个角色"规范冲突（其中 R1–R23 对抗环记录为 v18 自检批产物，如实承认）。v19 动作：
治理史/版本记录/环记录移 AUDIT sidecar（短链接引用）、主报告=科学叙事+参考文献；依赖
有向执行表（能力门→载体门→最小核心实验→条件分支→独立复制，逐段输入/产出/停止条件/
资源量级/收缩范围）；先导 150–200 题定位为构念/流程/方差先导、确认性判据用 power 定的
冻结扩展集（§5.4 全量层义务既有、明示分工）；**最小开题主线冻结按"排序非收窄"口径**
（RQ0 门→ORG 同层比较→SUPPLY 主实验→USE 准入→系统级效果/可靠性/成本画像；个性化/
面联邦/档 B/基线重实现=条件扩展——三支柱全数保留为承诺内容，与续83① 相容）。

## §4 评审代拟与边界事项

§6 问题树（含总问题改写与 RQ4a/4b 拆分）=评审代拟、owner 未签——实质方向与 v18 一致、
经续86 采纳骨架、措辞随 v19 由 owner 签；donor 压缩要求与 round-10"恢复说理散文"历史
要求相反（评审间分歧、非 owner 裁决冲突）——按 MAJOR-6 角色分离逻辑调和（主文定位注+
细节保留）。评审自身边界纪律良好，无越权执行要求。

## §5 v19 承诺清单（对应评审 §7 八项签字门）

- [ ] RQ 承诺面与主操纵/主判据一一对应（RQ 卡片化）；
- [ ] 三形式操作归因互斥（触发/USE 输出/router 主层三处修正）；
- [ ] §1.7 补十件直接工作+L4 三分+时间线修正；
- [ ] 标准参考文献表+统一 literature cut；
- [ ] 档 B 有限时域序贯决策合同（方案 B，续82③）；
- [ ] 三态判定语义全格网；
- [ ] 效率比较性 estimand（不进主判据）+可靠性护栏入成立侧；
- [ ] 主报告瘦身（审计史移 sidecar）+依赖执行表+先导/确认分工+最小主线（排序非收窄）。

v19 交付后按续85④/续86 基线跑多轮隔离对抗自检环（隔离上下文+重新搜索+监督核验，至
零轮）再送"问题树+直接语音/音频现状+统计/控制合同"窄面复审。

---

**更正附注（2026-08-02，追加不改写；载体=D2 条目 2026-08-01-d2-2025-emnlp-main-246）**：
两处。①§2 首段括注"注意该名不在其摘要、仅在正文/repo"有误——该句转引自隔离 web
核验代理；本地 D2 三路核（Anthology PDF p.4878/arXiv PDF/eprint LaTeX `abstract` 环境，
sha256 复算一致）证实 **MCR-Bench 名称在其 PDF 摘要第三句出现**；著录摘要字段（abs 页/
Anthology 网页）离线未核、为上游断言最可能来源，只作可能性登记。②该篇标题存在双形态：
排版/正文标题 "…Benchmarking Text Bias…under Cross-Modal Inconsistencies" 与著录标题
"…Revealing Text Bias…"（arXiv PDF /Title 元数据），引用须按 D2 合同双列不混用。web
表征被本地全文证伪属监督镜头有效实例；引文真实性判定（14/14 属实）不受影响。
