---
amendment_id: "SF-PROTO-AMENDMENT-9"
date: 2026-07-18
scope: "v4 博导复审整改合同——阶段正典 supersession 登记 / exposure union / system-control occupancy schema / known-item 保证队列 / claim-evidence 证据模式纪律 / Stage-2A 复现先行合同草案"
owner_ruling: "2026-07-18 五裁决:①阶段重定义按评审方案走 dated supersession（1B=mapping 执行禁研究模型含 smoke;方向性原型→Stage-2A 复现先行）②历史实验全量登记 INHERITED_PRIOR_EXPOSURE ③已知项保证性 DFS 队列（不动 65 条冻结查询）④system-control occupancy schema 采纳,selector 表降组件表 ⑤Stage-2A 复现先行合同接受为 1C 冻结草案"
gate_relation: "本修正案 = v4 复审 P0-1..P0-4/P1-1..P1-3 的整改载体;签署对象 = 更正后 v4 + 本件 + 九项门禁重绿"
---

# Amendment-9：v4 复审整改合同

## §1 阶段正典 supersession（P0-1;owner 裁决①）

正典已改：`wiki/Research-Methodology.md` §研究流程阶段（2026-07-18 dated supersession,含
墓碑——旧「1B=方向性原型」语义废止,方向性原型/小样/smoke 自此属 Stage-2A;07-16「survey
执行=1A」裁决之目的由新表继承并加强）。CLAUDE.md/AGENTS.md 指针已镜像。**owner 已签署：
Stage-1B（mapping 执行）全程不得运行研究模型或 smoke。**

**四字段 exposure 记账（任何阶段声明强制）**：`current_activity_stage` /
`new_model_touches_since_gate_freeze`（附起算 commit）/ `cumulative_model_touches` /
`legacy_experiments = INHERITED_PRIOR_EXPOSURE`。exposure union 正典 =
`wiki/2026-07-18-inherited-prior-exposure-union.md`（历史实验逐事件登记:模型/数据/指标/
证据指针;不删除、不降格、不归零;后续 held-out/预注册设计必须显式排除或分层）。

## §2 claim-evidence 证据模式纪律（P0-2）

五值互斥枚举,每个承重 claim 必标其一：

- `MACHINE_RECOMPUTED_LOCAL`——本地数据/工件可由命令重新计算;
- `MACHINE_REPLAYED_STRUCTURE`——结构/计数/哈希/matcher/validator 可重放（九项门禁属此级,
  **不覆盖外部论文数字**）;
- `SOURCE_REPORTED_TRACEABLE`——数字来自论文,可定位页/表/图,未独立复验;
- `REVIEWER_INFERENCE`——跨论文综合或身份判断;
- `TEAM_ATTESTATION`——签字承诺（如「未执行未登记的查询/模型调用」——日志在场性不能机器
  证明完整性,措辞永不称「机器证明」）。

v4 承重数字全量矩阵 = `wiki/survey/2026-07-18-sf-v4-claim-evidence-matrix.md`。「全部承重
数字可机器复跑」类无限定句**永久禁用**——完成态语言必须与所引验证机制的能力包络相等
（敌意内审环新增「能力包络」镜头,与 mutation 镜头并列强制）。

## §3 system-control occupancy schema（P0-3;owner 裁决④）

空位/占据判断的编码轴自本件起 = **系统控制 13 轴**（selector 四轴表降为组件表）：

1. 核心身份（单一冻结核心/专家联邦/双模型;权重与结构是否改动）
2. 访问级别（API-only/文本输出/logits/hidden-state/梯度）
3. 全系统训练范围（核心/控制器/verifier/memory updater 各自 trained 或 frozen——TF-Strict 四事实字段）
4. 控制时域（单步解码级/单响应级/多步轨迹级/跨会话级）
5. decision rights（gather-more/retry/branch/tool-call 授权/终止——谁在什么信息下决定下一步）
6. 状态/记忆（有无跨步状态;读写规则;跨 rollout 复用）
7. 工具（有无;调用由谁决策;工具输出如何入上下文）
8. 反馈/奖励来源（rule/consensus/self-eval/外部模型/learned evaluator;label-free 与否）
9. 候选生成与选择（有无 K 池;selector 类型;等 K 基线在场性）
10. 停止/预算（early-stop/budget 分配/execute-skip 门控）
11. 终态合成（直接选优/合成器/多候选融合）
12. 信息边界（read-out/new-info;test-item gold 隔离）
13. 模态/任务范围（含 speech/audio 与否;单任务/多任务/omni）

## §4 known-item 保证性 DFS 队列（P0-4;owner 裁决③）

**不动 65 条冻结查询**;以下工作以 `REVIEWER_KNOWN_ITEM`（评审供给）身份获得 Stage-1B 开局
**保证性 DFS 入口**（登记 exposure provenance;零命中者保留零命中反例身份,不加 seed 后
声称召回修复;drift 队列 3 例阈值自此只管**未知**漂移）：

| 工作 | 身份注记 | 65 查询离线召回（我方复现） |
|---|---|---|
| ATLAS 2606.01667 | system-control 直接近邻 | 5 命中（SF-L2-Q1/L13-Q1/L13-Q3/**L14-Q1/L15-Q1**——C4C 方法占位轴有效） |
| AutoTTS 2605.08083 | controller synthesis 近邻 | SF-L2-Q1 |
| Agentic Coding TTC 2604.16529 | 长轨迹 memory/reuse 组件 prior | SF-L2-Q1 |
| Team of Thoughts 2602.16485 | 多模型联邦边界对照（评审供给,同表其余七项） | **零命中**（text-domain,模态连词挡;零命中身份 = 我方 matcher 复现的主动补充披露〔评审未测此项召回〕） |
| ToolGate 2606.03054 | **TRAINED_COMPARATOR**（摘要逐字:"learned controller"+"matched-domain trajectory training"）+ decision-rights/停止 prior | **零命中**（gating 词族,drift 队列 1/3 身份保留） |
| DeepVerifier 2026.findings-acl.1243 | rubric outcome verifier,"without any additional training"(abs 级);verifier 能力来源待全文审计 | 非 arXiv,官方源救援已双份落盘 |
| Selective TTS 2026.findings-acl.1724 | reward-guided 多阶段 pipeline/judge drift prior | 非 arXiv,同上 |
| Dual-Phase Adaptive Inference 2026.findings-acl.511 | reward 驱动预算/early-stop prior | 非 arXiv,同上 |

全部 8 项全文已入库（5 arXiv 双份入 fulltext ledger;3 ACL 官方 PDF 入 survey-backups,
sha256 留痕）;13 轴 DFS 记录 = `wiki/survey/2026-07-18-sf-known-item-dfs-systemcontrol.md`。
**carry-forward 纪律（P1-3）**：Stage-1B 每轮产出 known-item carry-forward ledger（旧 survey
direct neighbor/当前命中/引文新增/零命中已知项四列账）——归档不是遗忘许可（ATLAS 07-03
在案未迁移 = 第二例 carriage failure,与 2512.11109/X3 同型）。

## §5 Stage-2A 复现先行合同（草案;owner 裁决⑤——Stage-1C 冻结,现无执行力）

按 v4 复审 §6 六条全文接受为草案：复现选择理由（最近 system prior/最强组件基线/一个负结果
comparator 三选）→ 复现合同（原设置/版本钉定/容忍区间/不可复现退出条件）→ 配置化工程合同
（禁每实验一条定制主流程）→ 复现先于改进 → 证据隔离（复现/开发/验证集分离,exposure union
从验证集排除或显式降级）→ 资源纪律（不设 cap 但全记账,与三阶段资源姿态一致）。优先复现
对象 = Stage-1B mapping 后决定（候选池至少含 ATLAS/AutoTTS 类系统控制、MLLM Orchestration
类免训编排、majority/BoN/Selective-TTS 类强组件基线）。

## §6 双向证据综合纪律（P1-1）

「支持而非削弱」类单向措辞废止;candidate problem card 强制四行：`supporting evidence` /
`contradicting evidence` / `single-observation kill criterion` /
`unresolved alternative explanation`。v4 §3.2 已按「异质案例共同提示」+三栏改写。

## §7 引用自包含（P1-2）

reviewer-facing 件必须带 reference appendix（作者/年份/稳定链接）、数字页/表/图 locator、
非连续引文以拼接引标注;「一致成立/主导/封顶」限定为「在该论文报告的模型/任务/设置内」;
「11/12 引文抽查」只声称抽中项定位质量。v4 更正版已执行。
