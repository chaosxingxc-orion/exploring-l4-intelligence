# Speech-aware evidence acquisition: Stage-2 discovery 首切片探索结构设计

## Status

本件在 2026-08-02 入场合同(`docs/superpowers/specs/2026-08-02-speech-aware-evidence-acquisition-stage2a-entry.md`)
与 2026-08-04 合并执行合同
(`wiki/experiments/speech-aware-evidence-acquisition/2026-08-04-owner-consolidated-execution-contract.md`)
框架**之内**细化 discovery 首切片的探索结构;不修改任何合同冻结值(边界、预算帽、执行
profile、E0→R0→R1→X 顺序)。E0 与 runtime receipt 已于 2026-08-04 关闭并经 gate dry-run
验证(study 仓 `docs/receipts/`)。

```yaml
record_kind: stage2-discovery-slice-design
date: 2026-08-05
study: speech-aware-evidence-acquisition
scope: discovery slice 1 (E0 closed; R0 + R1 + X1-X3)
decided_by: owner in-session answers, 2026-08-05
amends_contracts: none
```

## 决定记录(owner 会话内拍板,2026-08-05)

1. paper candidate 的主张类型**先不定,由 discovery 证据决定**;
2. 首切片薄探测覆盖 **X1–X3**;X4(reward-guided vs 固定策略)与 X5(次级载体迁移)因依赖
   前三点结果顺延第二切片(届时预算续期需 dated amendment);
3. R1 基线**先出按轴 readiness 对比备忘再由 owner 拍板**,不预设首选;
4. 切片内部**重叠推进**:model-free 的 readiness 备忘与 R0 工程布线并行;
5. 每个验证点**内嵌该轴最强可运行论文方法作为复现 arm**(矩阵结构,见 §1);
6. 本设计**不做预算分配**;首切片总帽由合并合同 §6 冻结,逐 run 用量在各自
   `ExecutionPlan` 中申报并经 exposure 预登记。

## §1 组织维度:验证点为骨架,论文复现为对照列

Stage-2 探索不按"论文复现"与"技术验证点"二选一,而是矩阵结构:

- **行(骨架)**:合同 X 序列的单轴验证点。首切片做 X1(OBS)、X2(ORG/SUPPLY)、
  X3(USE)三个最小因子实验;
- **列(校准与对照)**:R1 对一条最强同任务/同载体/同边界 prior 做全协议端到端复现,
  回答"我们的测量管线可信吗";同时每个验证点的因子表内嵌该轴最强可运行论文方法作为
  必跑 arm,回答"现有方法在我们的边界上做到什么程度、在哪里失败"。

论文复现因此不是一次性校准动作,而是贯穿每个验证点的对照列,同时是创新点的证据来源(§6)。

## §2 验证内容:三个可证伪假设与 arm 集

每点都是"其余轴冻结、只动一个轴"的最小因子实验;三门
(effectiveness / reasonableness / efficiency)齐报;gold/reference/test annotation/
future turn 永不进入 runtime;oracle evidence 只作上界接口,不进正式 runtime。

- **X1(OBS)** 假设:对实体密集片段的重解析(重转写/多假设/置信度定位)降低实体误听,
  且不恶化整体 WER。arm 集:bare core / prior 复现 arm(API 边界内可行的已发表做法,
  由 readiness 备忘确定具体篇目)/ 本仓 OBS 变体。判定指标:entity recall/F1、
  entity-WER、correct-to-wrong 转移。
- **X2(ORG/SUPPLY,OBS 冻结)** 假设:合法证据(ConEC supplementary contexts)的组织
  与供给方式(粒度/数量/顺序)改变证据可及性,提高 wrong-to-correct 且不增加
  correct-to-wrong。arm 集:no-context / ConEC 论文 context 注入方法原样复现 /
  本仓组织化 supply 变体 / random-mismatched 负对照。
- **X3(USE,供给冻结)** 假设:证据准入/核验控制在供给含错误证据时降低 correct-to-wrong
  回归。arm 集:no-verification / 已发表纠错或证据核验做法(RECOVER 式 1-best correction
  或 QA 核验线,由 readiness 备忘确定)/ 本仓准入-核验控制;供给中含受控污染证据。

## §3 载体与 split 分配

- **discovery** = `earnings21-original` + `conec` contexts(ConEC 上下文挂在 Earnings21
  上;R1 复现与 X2 直接使用);
- **dev** = Earnings22 upstream-curated subset10(E0 D4 已作为 dev 曝光;继续承担
  smoke/调试);
- **confirmatory** = `earnings22-original` 去除 subset10 的剩余部分:保持未读,首切片
  一律不触碰;任何 confirmatory 读取前先在实验台账与 exposure ledger 登记冻结的
  split identity hash 并标记 consumed(合并合同 §7)。

## §4 判定与晋级规则(读结果前预注册)

每个薄探收口时判为三态之一:

- **PROMOTE**:增益真实、单轴可归因、负对照干净;
- **PARK**:无增益或不可归因;
- **REPAIR**:测量或布线问题,修复后可重跑(不计入轴结论)。

第二切片深挖轴的入选判据:该轴 PROMOTE **且**候选创新点台账(§6)中已有针对该轴的可证伪
delta 主张。全 PARK 则出 narrow/stop memo。零/负结果是合法的切片完成形态。判定规则在读取
任何 confirmatory 结果前冻结;首切片只使用 discovery 与 dev split。

## §5 执行顺序(重叠推进)

- **并行 A(model-free)**:按轴的 prior readiness 清单——对合同 §4 候选线
  (ConEC/contextual ASR、RECOVER 式 1-best correction、Siskos 实体消解、
  FlexCTC/TurboBias 偏置线)及 readiness 调研中新识别的同边界方法,逐条记录 runnable
  revision、许可、API 边界兼容性、scorer 对齐方式、不可运行原因。三类结局都有用:
  可运行的进对应验证点当复现 arm;最强最近的一条由 owner 拍板为 R1 全协议复现对象;
  边界内不可运行的(预期含需 logit 访问的偏置线)按
  `INCONCLUSIVE_BASELINE_NOT_READY` 语义留档为结构性缺口证据(§6 来源 3)。
- **并行 B**:R0 工程布线(入场合同七项交付:deterministic loader、frozen-core
  adapter、四轴 trace、scorer adapters、三个工程控制、负对照与 oracle 上界接口、
  MLflow/台账连接与成本记账)。R0 只验证 wiring 与 measurement integrity。
- **汇合后串行**:owner 拍板 R1 基线 → R1 复现 → X1 → X2 → X3 → 三门联合表 +
  go/narrow/repair/stop memo,首切片收口。

模型触达顺序仍严格为 E0(已闭)→ R0 → R1 → X;每次触达携带合法 `ExecutionPlan` 并先在
study 仓 `docs/exposure-ledger.md` 预登记,由 `contracts.FrozenCoreGate` fail-closed 执行。

## §6 创新点发现机制

创新点从三个受控来源产生,全部落入 study 仓 `docs/innovation-candidates.md`
(append-only 候选创新点台账,每条带证据指针:receipt/台账行/memo 路径):

1. **复现失败模式**:每个验证点收口时出 gap memo——prior 方法在哪些实体、哪些条件下
   失败,是否引入 correct-to-wrong,失败可否归因到轴。创新主张的标准形式:
   "prior P 在本边界上有失败模式 F,轴控制 C 消除 F"——天然可证伪、自带 baseline。
2. **合同预登记的三个能力缺口**(可访问性、时效/专名、可验证性):每个验证点结果回填
   该缺口被 prior 覆盖的程度。
3. **结构性边界缺口**:readiness 备忘中被判 NOT_READY 的方法线,证明该能力在 API-only
   冻结核上尚无已发表可行方案;本仓外部控制面若达到其效果即是边界内首个可行方案。

台账为 Stage-2B 服务:合格 paper candidate(改进主张 + 零假设 + 机制 + baseline 收据 +
未读 confirmatory 声明)只能从台账中已有可证伪 delta 主张的轴产生。

## §7 Stage-2 分解(2026-08-05 补充;对齐 Stage-1A/1B/1C 拆法)

模型触达只发生在 2A-R0.3、2A-R1、2A-X、2B-深挖四处,每处独立 `ExecutionPlan` 预算与
exposure 行;其余全部 model-free。

- **2A-E0** 闭合(已于 2026-08-04 关闭):D1–D4 收据 + runtime receipt + gate dry-run。
- **2A-R0.1** 脚手架+备忘(model-free):readiness 按轴清单 + 创新点台账;出口 = owner
  拍板 R1 基线。
- **2A-R0.2** 工程基线(model-free,假 transport 测试):**两层结构**——Layer 1 可复用
  基础工程(单一 `core/` 包:统一注册表、统一驱动器 `run_experiment()`、五个抽象缝:
  载体/split、证据源、传输、评分适配、执行策略;治理层 contracts/gate/D2 arm 形状/冻结
  scoring 不抽象不留缝);Layer 2 配置化实验(每个实验 = 四片 config + 至多一个新注册
  组件 + 预注册)。出口 = 全测试通过、双仓 gate 绿。
- **2A-R0.3** smoke(首次模型触达,SAEA-E-001,dev subset10,~12 调用):出口 = trace
  完整、预算吻合、哈希齐(wiring 备忘,非结果主张)。
- **2A-R1** 复现校准(模型触达,discovery split):选定 prior 全协议复现;出口 = 指标落
  在可解释偏差带内,或 `INCONCLUSIVE_BASELINE_NOT_READY` 留档。
- **2A-X1–X3** 薄探测(模型触达,各含 prior 复现 arm):每点因子表 + gap memo + 台账
  条目;出口 = 每点 PROMOTE / PARK / REPAIR(§4)。
- **2A 收口**(model-free):三门联合表 + go/narrow/repair/stop memo。
- **2B-深挖**(模型触达;预算需 dated amendment):PROMOTE 轴第二切片 + X4/X5。
- **2B-资格化 → 冻结**(model-free):改进主张 + 零假设 + 机制 + baseline 收据 +
  实验/统计设计 + 未读 confirmatory 声明 → qualified paper candidate,study 终点;
  零/负结果合法。
- **Stage-3**:不在本仓;`OWNER_GO_AND_PAPER_EXECUTION_CONTRACT` 晋级 `papers/<slug>`。

## 失效条件

owner 修改主张类型决定、验证点覆盖、split 分配或晋级判据时,本件按
`wiki/AI-Collaboration.md` 就地取代并保留日期记录;stop-the-line 触发器沿用入场合同。
