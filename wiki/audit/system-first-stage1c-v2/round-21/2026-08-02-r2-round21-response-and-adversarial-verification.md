---
title: "R2 round-21 逐项回应与对抗核验：19/19 引文属实（零虚构零定性错、三轮最净）、5/5 发表态声明属实（滞后方在我方）、6 MAJOR 全采（两处半采）、owner 三裁决（续87）"
date: "2026-08-02"
artifact_type: "RESPONSE"
campaign: "system-first-stage1c-v2"
round: "round-21"
response_target: "wiki/audit/system-first-stage1c-v2/round-21/2026-08-02-r2-v19-multiround-adversarial-doctoral-supervisor-review.md"
review_target: "proposals/2026-07-29-r2-coreview-draft.md @ ab221c4 blob c4a9e8f4（sha256 f2504017…/225218 字节三项逐位亲验一致——评审对象=对抗自检环收敛终态）"
verification_channels: "①blob/正文指控=主会话亲验（git ls-tree+sha256 复算+逐锚 sed：§3.3 L645-648 RQ1 冲突、K0 L1077-1080 自承、模块行 L206、L241 时间线、§6.2 L918 简写、K-NB L1143-1148 判死式、红线 L120-123 全部坐实）；②19 件引文+5 项发表态=隔离 Opus 代理一手 WebFetch/官方页/PDF 取证；③本地覆盖=隔离 Sonnet 代理三线扫描（MAIN §10+正文/ledger/d2-entries）"
citation_verdict: "19/19 真实、零虚构、零定性错（唯一瑕疵=以'近音干扰'转述 'confusing entities'，合理外推）；发表态声明 5/5 属实——WavRAG=ACL 2025 正式（2025.acl-long.613）、DeRAGEC=Findings ACL 2025 正式（2025.findings-acl.786）、Speech-Hands=2026.acl-long.1997（pp.43124-43142）、Audiopedia=ICASSP 2025 DOI 10.1109/ICASSP49660.2025.10889814（302 解析实测）——四条滞后在我方记录；LongAudio-RAG 题名项对我方不成立（§10 行已用 v5 现行题名+现行一作，R3 监督面板本地 PDF 核过）"
local_coverage: "19 件中 9 件全库真缺席（wang21b/Retrieve-and-Copy/Whispering LLaMA/2025.emnlp-main.1052/johnson24/yang25n/VoxRAG/2025.naacl-short.51/CCFQA）；3 件同源异形（DeRAGEC/WavRAG anthology 形态未在册、TARS=库内 Wang 2026 之方法名）；8 件已三线闭环"
acceptance: "MAJOR-1/2/3/5/6 采；MAJOR-4 大部采——控制器定义取 owner 红线权威口径（续87①）、'删 RL 身份'支路不采（续82③，与 round-20 方案 A 同型拒绝）；MAJOR-1 关闭选项按 owner 裁决取选项 2（析因，续87③）"
owner_rulings: "Decision-Log 续87（①红线零训练/新模型必 frozen+控制器非模型 ②结论向量=既有评价体系 RQ 级延伸 ③RQ0 选项 2 析因）"
authority_effect: "RESPONSE_ONLY_NO_EXECUTION_GRANT"
exposure: "隔离代理对 19 件论文官方页/arXiv API/DOI 解析的 WebFetch/WebSearch（引文与发表态核验，owner 指示范围内）；零模型/指标/研究数据集执行；继承既有 exposure"
---

# R2 round-21 逐项回应与对抗核验

## §1 核验方法

三通道同 round-19/20 协议。blob 绑定=精确三项（git blob `c4a9e8f4` @ `ab221c4`、sha256
`f250401740fd…6965`、225218 字节），评审对象即 v19 对抗自检环收敛终态、无版本漂移。
评审边界纪律满分：frontmatter `novelty_scope: OUT_OF_SCOPE`、正文重申不判首创/占位/
prior-difference、明示不要求数值阈值（留 Stage-2A power 输入）、开题许可≠Stage-2A 授权。

## §2 引文核验：19/19 真实、零定性错；发表态 5/5 属实（滞后方在我方）

隔离一手核验全部通过（本轮为 round-19 以来引文卫生最佳轮：2 错→3 修正→0 错）。要点：

1. **四件发表态升级属实、错在我方记录**：WavRAG（2025.acl-long.613=arXiv 2502.14727
   同源，八作者/读数一致）、DeRAGEC（2025.findings-acl.786，其 arXiv comments 自述
   "ACL2025 Findings"）、Speech-Hands（2026.acl-long.1997，pp.43124-43142）、Audiopedia
   （ICASSP DOI 解析 302 实测活跃）。四条按"主链接指向本地在册形态"合同处置：抓取正式
   形态入库后切换主链接与状态栏。
2. **LongAudio-RAG 题名项对我方不成立**：2602.14612 曾名 "LongAudio-RAG:…"（v1，一作
   Vakada），现名 "Event-Grounded Question Answering over Long Audio via Structured
   Retrieval"（v5，一作 Hegde、框架改称 LA-RAG）——我方 §10 行即 v5 现行题名+现行一作
   （R3 监督面板本地 PDF 一手核）；如实注记，无需改动。
3. **同源身份三则**：评审 #7=库内 Siskos（2509.19567）；#19 "TARS"=库内 "Wang 2026"
   （2026.acl-long.857）之方法名（摘要逐字 "we introduce TARS"，一作 Chaoren Wang）——
   两称谓同篇、引用统一为 "Wang et al. 2026 (TARS)"；GRGA 为模型名非题名（引用注意）。
4. 9 件全库真缺席经双路确认（web 存在性+本地三线零命中）——收编义务见 §4。

## §3 六项 MAJOR 逐项回应

**MAJOR-1（RQ0 承诺>可识别+决策表不消费全部 RQ）——采；关闭选项按 owner 取选项 2
（续87③）。** K0 条款自承 NB 载体正读数不能分离外部新信息与潜在知识激发（L1077-1080
亲验）。v20 动作：RQ0 保留分型承诺+OBS×外部证据 2×2 析因（A0/仅观测增强/仅真外证 A1′/
双开）+预注册错误分型（负类/观测型/知识型/交互），各分量独立 estimand；闭卷参数化召回
探针承接"参数知识激活"面；总答案改**结论向量**（owner 裁决②：RQ0–RQ4b 逐问结论、既有
"五类结论不得互相替代"之 RQ 级延伸、多载体综合不合成单标签）。

**MAJOR-2（词典清楚、归属漂移四处）——采，四锚全数亲验坐实。** 最重一处=§3.3
L645-648 仍把外部知识域"版本/出处/冲突/abstain schema"钉为"O-config 臂的实验问题"、
与 RQ1 卡片收窄正面冲突（v19 收窄未传播到旧节——本方六轮自检环逃逸，如实承认，教训
=新增"旧节-新卡传播全扫"镜头）。v20 动作：§3.3 对齐 RQ1 卡（schema/版本/出处=工程
合同+后续分支）；同录音索引取 **OBS-INDEX** 方案（只检验观测组织与访问效率、不承担
外部知识 ORG 结论——与 §1.3 自有裁定"存量化不改变层归属"一致，L4a 线标签同步改）；
RQ3 模块统一名"证据准入"（融合/冲突/引用/拒答=后续支线）；ABSTAIN 固定为终结动作层、
USE 只评其正确性；§6.2 L918 简写补"触发/停止之裁决行为归 CONTROL"限定。

**MAJOR-3（三态真值表+K-NB 全称反证）——采。** 真值表=编辑规范化：语义已由三态总则
+局部阀覆盖（本方环内多轮以此拒报同类候选），但签署级文档不能靠"全局重释条款"扛住
分析脚本/预注册/执行者/答辩委员四方歧义——此理由压倒既有拒报立场，认账。v20 动作：
十一条主判据逐条改显式三行真值表（SUPPORTED=LCB 越 SESOI；REFUTED_OR_NEGLIGIBLE=UCB
不超可忽略界或预注册等效/ROPE/反向非劣成立；INCONCLUSIVE=其余）；合取命题明写"全部
分量支持才成立、任一承重分量被正式反证则推翻、仅未获支持则不确定"；**K-NB 保留全称
主张+正确反证逻辑**（任一承重对手经正式反向检验证优→全称主张 REFUTED——现行
SPLIT_GROUP 回 owner 对反证力的低估修正；SPLIT_GROUP 保留给"未获支持非反证"格）。

**MAJOR-4（RQ4a 拆分+档 B 合同+TF-Strict 控制器）——大部采；控制器定义取 owner 红线
权威口径（续87①）、"删 RL 身份"支路不采（续82③）。** v20 动作：RQ4a 拆 4a-1（双源
按样本动作选择）/4a-2（序贯策略/优化器身份）；4a-1 建等预算析因（SUPPLY-only/OBS-only/
无条件串行/双源自适应，固定动作可用性、信息量与调用预算，以 interaction 识别选择价值
——RQ0 析因〔续87③〕同构复用设计件）；档 B 合同补齐入正文（C_t 候选证据区入状态、
初始态/动作合法域/观测随机性/终止态/horizon/episode return/策略类/离线 credit
assignment/行为策略/随机种子/覆盖条件）；**控制器权威定义**：外置、非神经、无梯度之
序贯策略（规则/表格/线性打分类），有限决策常量 dev 期 reward-guided 标定、test 冻结
种子重放——本轮零模型参数训练、一切模型（含新引入）frozen 检查点（红线第一二条权威
口径，owner 落笔）；档 A/档 B 共享动作空间/horizon/信息/调参预算之合同同批冻结。

**MAJOR-5（pilot/confirmatory+基线出口+最小路径）——采。** K0/K4 判定载体=先导 vs
§6.6"先导不得充当确认性证据"张力属实。v20 动作："先导数据集"改称载体族（carrier
family）并预划互不重叠 discovery/confirmatory split（按源音频/speaker/company/entity
去泄漏；阈值/标注规则/prompt 于 discovery 定、正式裁决于 confirmatory 出）；mandatory
baseline set 冻结（版本/信息边界/调参预算/readiness gate、不可事后缩减），任一
mandatory 对手不可运行→K-NB 记 `INCONCLUSIVE_BASELINE_NOT_READY`（不移出入判集）；
新增最小确认路径（单主载体+必需基线+主指标族+确认样本量 power 输入+调用/GPU/存储/
标注人月上界〔声明不确定度的可行性规划估计、非成本判据——续82② 效果优先不受触〕
+stop/go 顺序；面联邦/个性化/档 B/多载体复制/基线全迁移=条件扩展、互不为前置）。

**MAJOR-6（直接线遗漏+发表态权重）——采。** 9 件真缺席+时间线修正坐实（johnson24=
Interspeech 2024 deep-Q 跳读策略、yang25n=Interspeech 2025 training-free 双维 chunking
——L241"agentic 控制范式（音频域 2026 起步）"不可维持）。v20 动作：L2 拆
`acoustic/speech-key memory` 与 `speech entity retrieval/linking/disambiguation` 两支
（2021 wang21b/2023 Retrieve-and-Copy/2024 TED-EL 成线）；L3 补 acoustic-key→candidate
→admission 轴（Whispering LLaMA/Generative Annotation/DeRAGEC/RECOVER 同轴四态表）；
L4a 时间线修正+johnson24/yang25n 入线；L5 补 NAACL 2025 表示分析+CCFQA 正式层；统一
变量列六问模板覆盖新增件；发表态分层加权（正式同行评议/已录用/纯预印本/benchmark/
跨域 donor）；四件正式形态升级+主链接切换（先抓正式件入库、维持"主链接指本地在册"
合同）；DeRAGEC 升全文 D2（证据等级与发表态正交之口径向评审说明，义务本在案）。

## §4 v20 承诺清单（对应评审 §8 十项签字门）

- [ ] RQ0 析因（选项 2，续87③）+错误分型预注册；总答案=结论向量（续87②）；
- [ ] OBS-INDEX 单列；RQ1 §3.3 对齐；RQ3 全篇统一"证据准入"；ABSTAIN 层固定；
- [ ] 十一判据三态真值表；K-NB 全称反证逻辑+mandatory 集+BASELINE_NOT_READY 出口；
- [ ] RQ4a 拆 4a-1/4a-2+等预算析因；档 B 合同补齐；控制器权威定义（续87①）；
- [ ] 载体族 discovery/confirmatory split；最小确认路径（资源上界=规划估计）；
- [ ] 直接线九件收编+L2 拆线+时间线修正+发表态分层+四件正式形态升级；
- [ ] 效率比率定义（净/毛修正、零/负分母、correct-to-wrong 抵扣、索引摊销、区间估计）。

v20 交付后按续85④/续87⑤ 跑多轮隔离对抗自检环（新增旧节-新卡传播全扫+发表态复核两
镜头）至零轮，再送"问题树+五层归属+三态判据+RQ4a/档 B+direct-field map+最小确认路径"
窄面复审。

## §5 评审代拟与边界事项

§7 问题树表=评审代拟、owner 未签——结构经续87② 采纳（结论向量）、逐格措辞随 v20 由
owner 签。评审自身边界纪律满分（对比记录：本轮引文卫生三轮最佳），无越权执行要求。
本方元教训入档：六轮自检环收敛后仍被外审找到六项实 MAJOR——非环失效而是镜头覆盖差
（本方概念镜头聚焦 v19 新表、旧节残句逃逸；本方重搜按缺口面、外审按谱系纵深+发表态
——两查询族缺失），续87⑤ 两新镜头即此修复。
