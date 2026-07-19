---
amendment_id: "SF-PROTO-AMENDMENT-10"
date: 2026-07-18
scope: "v5 复审整改合同——exposure union v2（四仓）/ identity taxonomy v1 冻结 / known-item coding v2 / v5 增补矩阵 / 量词扫描检查 / Stage-1B 首批 reviewer-known 队列 / owner 重申登记"
owner_ruling: "2026-07-18 五裁决:①W4 四仓考古批准;②taxonomy 十字段采纳,「是否 reward-guided」降派生字段,按 method path 重编码;③v5 矩阵/自包含/引用修正;④Round E 十项入 Stage-1B 首批;⑤owner 重申原文:「重申：Stage-1B 全程不得运行研究模型或 smoke」"
---

# Amendment-10：v5 复审整改合同

## §1 exposure union v2（P0-1）

四仓（W1–W4+umbrella）考古完成,「全量」称谓撤回重立为四仓 scoped 计数（W1+umbrella 27 事件
/ W4 ≈70 事件〔二轮收敛,changelog 4172 行全通读,8 推理研究模型/14 数据集/选择决策污染面
≥11 处〕/ W2·W3 零实验直验;粒度异构不聚合;同源战役去重注记）;W4 诚信更正链（MInDS
手工 JSON 事故八步时间线、R2 oracle-artifact、SEL2-seed42 选择-过拟合）**并列入账**;评审
点名七族全部映射零排除;仓外边界 = owner attestation。**union v2 前冻结的 fresh/held-out
切分无效;≥11 条选择运行数据集×split = 最高优先隔离面**。新发现主动披露：W4
superseded-note 所引 `docs/claim_ledger.yaml` 悬空（untracked 且不在盘）——登记 W4 侧待修
簿记项。正典 = `wiki/2026-07-18-inherited-prior-exposure-union.md`。

## §2 identity taxonomy v1 冻结（P0-2）

机器可读 schema（`wiki/survey/2026-07-18-sf-identity-taxonomy-v1.json`）：十字段 + score_type
七枚举 + 三派生字段（is_reward_guided / is_all_system_training_free /
is_project_strict_identity——后者含 dev-label 选型轴）+ 冲突规则（dev-gold 永不报 test
泄漏;mixed-path 论文按 method path 分行;占据量词必须机器重算合取）。known-item 8 项重编码
= `2026-07-18-sf-known-item-coding-v2.json`（9 method path,DeepVerifier 双路径分行）;合同
测试 = `scripts/survey/sf_identity_taxonomy_test.py`（V1–V5:字段/枚举/四反例单测/负控自证
可失败/占据合取机器重算持久化,5/5 PASS）。**机器重算正典**（散文量词唯一来源,
`docs/checks/2026-07-18-sf-identity-taxonomy-test.json`）：speech/audio = 0/9;
training-free∧reward-guided∧K 池 = 3/9（Selective TTS/Team of Thoughts/Agentic Coding）;
strict-identity∧reward-guided∧K 池 = 1/9（Agentic Coding）;原「零项」句已撤回。

## §3 v5 矩阵与引用（P0-3 / P1-1）

v5 增补矩阵（`2026-07-18-sf-v5-claim-evidence-matrix.md`,scope=v5 新数字与量词,零 orphan）;
v5 自包含参考文献 28 条（ACL 作者自官方 citation 元数据补齐）;ATLAS 88.9% 补 GPQA-Diamond/
Fig 7a 条件;known-item DFS 件 dated correction（自由文本身份汇总由 taxonomy 重编码取代）。

## §4 量词扫描检查（本方流程改进,内审环第六轮教训的可执行化）

`scripts/survey/sf_quantifier_scan.py`：reviewer-facing 件中的量词 token（见脚本 TOKEN
定义〔SCOPED〕）无同行集合限定语即 FAIL;内嵌负例自测（oracle 可失败证明）。纳入发布前检查单（与敌意内审环
能力包络镜头并列）。

## §5 Stage-1B 首批 reviewer-known 队列（P1-2;owner 裁决④）

v5 复审 Round E 十项以 `REVIEWER_KNOWN_ITEM` 登记（v5 附录 A 第二表 = 正典:5 arXiv 附我方
复现命中留痕〔CATTS=L2-Q1/AgentBench=L2-Q1+L12-Q3/PiCSAR=L5-Q1/SamplingForQuality=EBD=
L2-Q4+L5-Q1〕;5 ACL 附 T1-ACL-2026 路由保证）;执行首轮**先按 taxonomy v1 编码再入正常
BFS/DFS 排序**;不动 65 条冻结查询,不冒充 query recall 成果。空位措辞纪律（P1-3）：mapping
收敛前只允许「已检视集合中未见/待检验候选空位/组件轴占据表」三型句。

## §6 owner 重申登记（逐字）

owner 2026-07-18：「**重申：Stage-1B 全程不得运行研究模型或 smoke**」。
