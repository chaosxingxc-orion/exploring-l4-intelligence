---
title: "R2 开题报告 v16.1：博导视角正式开题签字审查（概念闭合、实验可证伪性与 Earnings21/ConEC 载体审计）"
date: "2026-08-01"
artifact_type: "REVIEW"
campaign: "system-first-stage1c-v2"
round: "round-16"
review_target: "wiki/survey/workbench/stage1c-portfolio/proposals/2026-07-29-r2-coreview-draft.md"
review_target_commit: "c8cfd1808a102231b643e94895d7ec6f6d4b7773"
review_target_git_blob: "edb38a2f64cb91f63ec5631cd3e3af1569b3aca3"
review_target_blob_sha256: "0eaa05117f59cc15a1f906ff52fef4604dc35d9d310fb909b27d01c19f4cd92c"
review_target_size: "99,728 bytes; 967 lines; Git blob bytes"
responds_to: "round-15/2026-08-01-r2-v16-doctoral-supervisor-coreview.md + v16.1 pre-signature remediation"
verdict: "MAJOR_REVISION_REQUIRED_BEFORE_FORMAL_OPENING"
major_count: 1
formal_opening_authorized: false
permission_note_issued: false
authority_effect: "REVIEW_ONLY_NO_OWNER_DECISION_NO_EXECUTION_GRANT"
human_signature_claimed: false
model_or_metric_execution_authorized: false
stage2a_authorized: false
novelty_verdict: "NOT_ISSUED"
---

# R2 v16.1 博导签字审查：总体框架已经成立，但主载体的直接先例与数据分割合同仍有一处阻断性缺口

## 一、裁决摘要

**裁决：`MAJOR_REVISION_REQUIRED_BEFORE_FORMAL_OPENING`；1 项 MAJOR，5 组收尾项。暂不出具
“允许正式开题” notes。**

这不是对研究方向的否定，也不要求推倒重来。与早期版本相比，v16.1 已经把最重要的逻辑骨架
搭起来了：

1. **知识组织、知识供给、知识使用已经被定义为三个互斥的系统对象**，不再只是三个相近说法；
2. **黑盒模型为什么需要外部知识**已经从“模型不知道事实”的泛论，收敛为“错误声学假设会生成
   相关但全错的证据链”这一语音特有因果机制；
3. 组织层、供给层、使用层和控制层都有对应的实验臂、反事实对照与击杀判据；
4. 有效性、合理性、可靠性、效率已分层评价，且没有用一个不可解释的总分把它们揉在一起；
5. 能力上界、发音库机制核、TFRL/RL 身份都被写成可失败的技术假设，而不是开题时预先宣布成立。

因此，**课题本身值得做，技术问题也具有博士研究价值**。本轮不签字的原因只有一个，但它会同时
改变知识源、开发/测试隔离、最近基线和增量主张：提案选择 Earnings21 作为主载体，却遗漏了直接
建立在 Earnings-21/22 上的 ConEC，以及与之相连的 Earnings21 contextual-biasing 基线谱系。
在补上这一组先例之前，“十二件近邻无占据”“官方 split”“最强 incumbent”三项陈述均不能视为
闭合。

---

## 二、对开题核心逻辑的逐项审查

| 审查问题 | 结论 | 博导意见 |
|---|---|---|
| 研究对象是否清楚 | **通过** | §1.3 已用“被改变的系统对象”划分组织/供给/使用，并把采集门与准入门分开；这个定义可作为全篇术语法。 |
| 黑盒模型为何需要知识 | **通过** | §1.2 的“误听实体 → 错 query → 相关但错误的证据互相加强”是语音域特有、可实验化的因果链；动态事实、私域事实和出处审计构成第二类必要性。 |
| 各模块是否有针对性改进 | **基本通过** | 发音库解决声学候选生成，世界知识 rescore 解决同音身份裁决，面 key/value 解决组织，门控环解决供给与使用，TFRL 解决任务化配置；不是同一技术换名重复。 |
| 是否能评价“引入知识有效” | **通过** | §6.5 的 paired `delta_E`、实体准确率、任务效用、wrong→correct/correct→wrong、CI 与 SESOI 足够构成效果判断。 |
| 是否能评价“引入知识合理” | **通过但依赖载体修复** | 触发/准入混淆矩阵、oracle headroom、证据 removal/swap、unsupported claim、under-call/no-op 能区分“碰巧答对”与“知识真正起作用”；但知识来源与时间边界必须先锁死。 |
| 是否能评价知识使用效率 | **方法上通过，主张上受限** | 九维资源向量、P95、每实体修正成本和摊销口径合理；既然正文坚持“效果优先、成本不进主判据”，就只能声称“效率被完整记录”，不能在没有等预算曲线或 Pareto 优势时声称“更高效”。 |
| 技术点是否值得验证 | **是** | 黑盒声学候选 × 世界知识显式裁决 × 选择性重听/搜索，是高风险但有明确失败出口的系统假设；组织优化与 contextual bandit 也有价值，但必须分别赢过等预算 random search 和离线档 A。 |
| 当前是否可正式开题 | **否** | 主载体最近先例和 dev/test 合同尚未闭合；见 MAJOR-1。 |

### 2.1 三种“形式”现在应如何理解

建议 fable5 后续所有章节都服从下面这条边界，不再按组件名字分类：

```text
组织形式（knowledge representation / storage）
  = 知识以何种单元、schema、索引、版本、出处、时间快照存在

供给形式（knowledge acquisition / routing）
  = 针对当前假设，何时取、从哪里取、用什么 query、取多少、何时停止

使用形式（knowledge integration / decision）
  = 已取回候选如何准入、融合、冲突裁决、归因、拒用、触发重听或最终作答
```

同一实体词表可以有一种组织形式，却有多种供给形式；同一批已取回证据也可以有多种使用形式。
所以实验归因必须遵守 §6.2 已提出的单层替换纪律：一次只改变 ORG、SUPPLY、USE、OPT 中的一层。

### 2.2 为什么在把模型当黑盒时仍要引入知识

提案现在给出了三条成立理由，其中第一条最有研究辨识度：

- **感知假设并不等于事实身份。** 黑盒模型把声音映射为一个文本/语义假设；实体同音、口音和
  长尾词会使局部声学证据不足。继续围绕错误假设检索，会获得“内部一致、外部有出处、但锚错
  实体”的证据链。
- **参数知识有时间与权限边界。** 训练截止之后的事实、企业私域材料、会话参与者名单和需审计
  出处的信息，不能靠扩大黑盒参数规模保证获得。
- **黑盒限制反而要求把控制与证据外显。** 不能读取或修改内部状态时，候选生成、证据来源、
  调用决策、拒用理由和成本必须在模型外形成可复放合同。

需要避免的错误表述是“模型不够聪明，所以给它知识”。可检验的表述应是：**在预注册实例分布
上，外部知识相对裸核存在正 oracle headroom；门控系统能在不使用 test gold 的条件下实现其中
一部分，并且收益可由知识层反事实消融归因。**

### 2.3 如何判断有效、合理和高效

三者不是同一个问题：

| 评价面 | 必须回答的问题 | 最低充分证据 |
|---|---|---|
| 有效性 | 加知识后任务是否更好 | paired `delta_E`、SESOI、置信区间、实体/任务主指标、最强对手比较 |
| 合理性 | 好转是否由正确知识、正确时机、正确使用造成 | oracle headroom、触发与准入 gold、source/temporal validity、removal/swap、错误迁移、污染与盲从读数 |
| 可靠性 | 是否只在平均数上好看 | worst-group、口音/实体类型分层、correct→wrong、coverage-quality、seed/run 方差 |
| 效率 | 相同效果花多少资源，或相同资源得到多少效果 | 等预算响应曲线、九维增量成本、均值/P95、每纠正实体成本、离线构建摊销、Pareto 前沿 |

不建议把九维成本压成一个未经预注册权重的标量“效率分”。如果未来要使用“efficient”作为论文
主张，至少满足以下一项：同预算效果优于对手；同效果成本低于对手；或在预注册资源维度上形成
Pareto 改进。否则只报告成本，不下效率优越结论。

---

## 三、阻断性问题

### MAJOR-1：Earnings21 的直接 contextual-ASR 载体谱系缺席，导致知识源、数据隔离和最强基线同时未闭合

#### 3.1 遗漏的不是普通相关工作

当前 §5.1 把“Earnings21 官方全集〔官方 split〕”冻结为主载体，§8 的最近邻矩阵和 §9 的 45 件
证据底座却均未出现下列三件直接先例：

1. **Fox & Delworth, Interspeech 2022**：直接为 Earnings21 发布 contextual biasing lists，
   比较 shallow fusion，并提出 alternate-spelling prediction；这与 §2.3 的发音/异拼候选机制及
   K-XOVER 的 in-context/biasing 对手直接重叠。
2. **ConEC, LREC-COLING 2024**：直接在 Earnings-21/22 音频上补充真实 slides、earnings release、
   参会者姓名与机构，提供修订 transcript、entity 信息和公开 shallow-fusion baseline；它不是
   “另一个数据集”，而是当前主载体的上下文知识层。
3. **Huang et al., Interspeech 2024**：在 ConEC 上报告 early context injection + text perturbation
   的训练式 contextual-ASR 改进；虽不满足 R2 的 API-only/training-free 边界，却是必须正面登记的
   trained upper bound。

ConEC 还明确写出协议：**Earnings-21 作 evaluation set；Earnings-22 或其他不含 Earnings-21 的
数据可用于 training/development。** 这与当前 §3.4“dev 上标定、冻结后进 test”、§6.3“禁 test
gold”是相容的，但与 §5.1 模糊的“官方 split/官方全集”并不等价。Earnings21 本身是 evaluation/test
corpus，不应被写成仿佛已有可供 TFRL 调参的官方 train/dev/test 三分。

#### 3.2 为什么该遗漏足以阻止签字

它会改变至少五个开题合同：

- **知识组织**：真实知识可以直接来自每场财报的 slides、release、participants，而不是待定的
  “知识源拉实体清单”；组织单元、覆盖率、噪声和 distractor 都有现成公共载体。
- **知识供给**：ConEC 的 per-call list 与全局/动态检索是不同供给制度，必须成为实验轴，而不能
  混成一个“有知识”臂。
- **知识使用**：零训练 shallow fusion、prompt/context injection、世界知识显式 rescore、选择性
  重听是不同使用机制；当前 incumbent 分组缺少同载体的最近基线。
- **数据隔离**：若在 Earnings21 全集上调 `tau/alpha/beta/gamma/delta`、词典规模或 prompt，再在
  同一全集报告最终效果，会违反提案自己的 test-gold 禁令。
- **独立性量词**：§8 的“十二件近邻无一同时满足……”只对已读十二件成立；直接先例未入矩阵时，
  该证据宇宙不能支撑签字阶段的“最近邻已闭合”。

此外，ConEC 对原始 Earnings21 transcript 作过实体纠错并发布 replacement files。开题合同必须
说明最终 reference 使用原始版还是 ConEC 修订版；否则不同基线的 WER/实体指标不可比。

#### 3.3 必须完成的整改

建议采用下面的最小修复路线，不重开 owner 已确认的“主载体=Earnings21”选择：

1. **补三件 D2 源核和近邻矩阵行**：Fox 2022、ConEC 2024、Huang 2024；逐项记录训练态、信息
   访问边界、知识来源、注入位置、公开实现、载体和指标，不只补 bibliography。
2. **把主载体实例化为明确的数据包**：推荐写成“Earnings21 audio/evaluation set + ConEC
   version-pinned context/transcript layer”；若坚持原始 Earnings21，必须逐条解释为什么排除 ConEC
   context 与修订 reference，并把 ConEC 作为同载体强对照。
3. **冻结开发/测试合同**：Earnings21 全集只作最终 evaluation；档 A、档 B 离线 reward、阈值、
   prompt、知识规模和 stopping rule 的标定使用 Earnings22/ConEC 或另一个预注册且与 Earnings21
   不重叠的开发集。若另行切分 Earnings21，则必须放弃“官方全集最终测试”的说法，并按 call/company
   分组防止实体与公司泄漏。
4. **增加同载体基线阶梯**：no-context；ConEC real-context shallow fusion；ConEC oracle；Fox
   bias list + alternate spelling；Huang trained neural biasing upper bound；Siskos 自动上下文发现；
   frozen omni 裸核；R2 主张臂。不同信息边界分组报告，不得把 trained 上界伪装成同边界对手。
5. **冻结知识时态与污染协议**：每场 call 的资料需记录来源、版本/hash、`available_at`、相对
   `call_start` 的可用性；把“当时可得真实上下文”“事后可得资料”“从 gold transcript 构造的
   oracle”分成三臂。实时 web 不得检回测试 transcript 或其派生页面后仍算非 oracle。
6. **重算 K-NB/K-XOVER 的对手与归因**：明确收益来自知识覆盖、候选生成、供给调度、准入，还是
   世界知识 rescore；ConEC 已提供的上下文不得被当作 R2 独有构造贡献。

**关闭标准**：完成上述协议级修订和源核即可复审；不要求在开题前运行模型或给出正结果。若补读
后仍能维持“API-only + training-free + 双源动作选择 + 显式世界知识 rescore”的合取空位，可继续
保留为待验主张；若不能，应主动收窄，不得靠信息边界措辞绕过最近先例。

---

## 四、非阻断性收尾项

### MINOR-1：`serial-composition` 仍没有判据和载体绑定

§6.2 已赋予它“门控调度器不胜则调度增量被证伪”的后果，但 §7 K1a 未具名纳入比较族，§5.1
整合载体清单也未纳入。把它写入 K1a 的固定策略族，并指定 NB 或另一个调度载体；否则删去判死
措辞，只保留诊断臂。此项承接 round-15 MINOR-2。

### MINOR-2：两件近邻的证据等级/信息边界回写仍未完成

- Zhang 行的 `training-free` 应保留摘要级 `PROBABLE`，不能写成无条件确认；“无条件管线”应改为
  “摘要级未见按样本动作决策”。
- Wang 行应具名 DSTC11/MultiWOZ 2.1、测试集策划的 14k 闭世界实体池、TTS train/真人 test，
  并把 top-10 + 固定阈值列入门先例；先导集若从评测 gold 策划候选库也要同样声明。

此项承接 round-15 MINOR-3/4；它不改变主张，但关系到引用诚实与外推边界。

### MINOR-3：“噪声耐受属于核的训练分布”假设需要有效裁决者

当前把它交给 A2/A3，但 A2/A3 的主载体与生成该假设的实体词表注入 regime 不一致，K4 又可能
返回 `PENDING_CARRIER_FORM`。应把它挂到 NB 主载体的 K-Gate/K1b 预检，或明确 A2/A3@NB 与备用
裁决路径。此项承接 round-15 MINOR-5。

### MINOR-4：版本与签字面需要收口

当前 Git 内容是 v16.1，但 frontmatter 仍写 v16、round-14 待复审，§9 仍写“其余六 MINOR 与五
OBS”，与实际已关闭 MINOR-1/6/7/8 不一致。定稿时同步 artifact id/status/review chain，并交付
一页纸签字表：一句研究问题、三主假设、组织/供给/使用映射、主/复制/诊断载体、最强基线、主判据、
kill criteria、数据隔离和权限边界。正文可以长，签字对象不能含糊。

### MINOR-5：登记 2026 年最新同域评测载体 Earnings25

Earnings25（2026-07-26）提供约 498 小时 full-call test 和 46 小时 industry-balanced segmented
test，以及 speaker role、industry、call structure 元数据。它当前没有替代 Earnings21/ConEC
实体知识载体的充分理由，但应作为最新外部复制/规模与行业分层候选完成一次纳入或排除裁定。
该项不阻断开题，因为它不是当前机制的直接上下文先例。

---

## 五、技术价值与范围判断

### 5.1 值得做的技术点

1. **声学多假设与世界知识的双源裁决**：值得做。它把“检索更多”改成“先保留感知不确定性，
   再用独立世界约束裁决身份”，可直接测量错误传播是否被截断。
2. **选择性重听/搜索的外显标量门**：值得做。最强证据不是 agent 形式新颖，而是它能否胜过
   always/never、matched-cost、serial-composition 和同预算固定策略。
3. **多面 key/value 组织**：有条件值得做。只有在含副语言/说话人/事件/时间面的载体上，并且
   K5-r 显示检索余量后，才可能形成博士贡献；在纯实体 ASR 载体上不应强行承重。
4. **TFRL 两档身份**：设计合理。档 A 是 derivative-free 配置优化，档 B 才承载 contextual-bandit
   的 RL 身份；赢不过 random search 或档 A 时主动降级命名，是正确的科学纪律。
5. **omni 知识系统超过专用 ASR+biasing/GER 的能力上界**：可以作为高风险假设，不可作为开题
   前提。当前 K-NB 的降级出口合理；ConEC 修复后应在同载体最强基线上接受正面检验。

### 5.2 范围风险

三支柱共同构成一套系统论文的逻辑是成立的，但博士执行时必须由 Stage-2A 基线把承重轴收窄。
建议保持如下优先级：

```text
P0  主载体与最强基线可比性（ConEC/Earnings21 合同）
P1  双源门控是否有独立增益（A4b−A4a、K1b）
P2  发音库是否存在相对简单 G2P/in-context 的价值窗口（K-PS/K-XOVER）
P3  组织优化与 contextual bandit 是否产生额外论文贡献（K5/K-RL）
```

P1 或 P2 任一成立即可形成较清楚的技术主线；P3 不应在前两者无效时靠增加系统复杂度救方向。

---

## 六、给 fable5 的复审验收清单

下一版回复应逐项提供定位证据：

- [ ] Fox 2022、ConEC 2024、Huang 2024 三件 D2 源核与更新后的最近邻矩阵；
- [ ] Earnings21/ConEC 数据包版本、reference 版本、知识来源与时间可用性合同；
- [ ] 与 Earnings21 完全隔离的 dev/calibration 来源，及所有可调项清单；
- [ ] ConEC/Fox/Huang/Siskos 与 R2 的同载体、分信息边界基线阶梯；
- [ ] 更新后的 ORG/SUPPLY/USE 单层归因表及 K-NB/K-XOVER 绑定；
- [ ] round-15 遗留 MINOR-2..5 的关闭证据；
- [ ] 一页纸签字表与 v16.1/下一版本的元数据同步；
- [ ] Earnings25 的纳入/排除说明。

复审只需审上述差分，不再重开已通过的研究对象定义、效果优先裁定、红线、三支柱保留和现有
击杀框架。若 MAJOR-1 被实质关闭且没有新近邻改变合取占据判断，可进入零 MAJOR 签字轮。

---

## 七、正式开题与权限结论

**本轮不出具允许开题 notes。** 原因不是实验尚未跑——开题本来允许结果未知——而是主实验的
知识载体与数据隔离尚未定义到可复现、可比较、无 test 泄漏的程度，且最近的同载体先例没有进入
证据矩阵。

本件不授予 Stage-2A、模型/API 调用、数据获取、指标运行、复现、原型、push 或 wiki 发布权限；
不修改 owner 已有裁定。`formal_opening_authorized: false` 只表示本轮博导审查意见为暂缓签字，
不冒充自然人导师或 owner 的法律/行政签署。

---

## 八、本轮重点核验的一手来源

1. Del Rio et al. 2021, **Earnings-21: A Practical Benchmark for ASR in the Wild**：
   https://www.isca-archive.org/interspeech_2021/delrio21_interspeech.html
2. Fox & Delworth 2022, **Improving Contextual Recognition of Rare Words with an Alternate Spelling
   Prediction Model**：https://www.isca-archive.org/interspeech_2022/fox22_interspeech.html
3. Huang et al. 2024, **ConEC: Earnings Call Dataset with Real-world Contexts for Benchmarking
   Contextual Speech Recognition**：https://aclanthology.org/2024.lrec-main.328/
4. ConEC 官方数据/代码仓库：https://github.com/huangruizhe/ConEC
5. Huang et al. 2024, **Improving Neural Biasing for Contextual Speech Recognition by Early Context
   Injection and Text Perturbation**：https://www.isca-archive.org/interspeech_2024/huang24f_interspeech.html
6. Siskos et al. 2025, **Retrieval Augmented Generation based context discovery for ASR**：
   https://aclanthology.org/2025.findings-emnlp.768/
7. Jiang et al. 2026, **Earnings25: A Comprehensive 500-Hour Speech Benchmark for Finance**：
   https://arxiv.org/abs/2607.23813

以上新增核验均为论文/数据集官方页面、ACL/ISCA 论文或作者官方仓库；技术判断未依赖二手博客。
本轮还对提案已有 45 件 D2/D1 证据目录和 round-15 遗留项作本地交叉核验，但不在此重复其完整
书目。

---

## 九、评审边界与 exposure

本轮执行：只读本地提案、round-15 评审、D2/D1 目录与 Git 元数据；通过 ACL Anthology、ISCA
Archive、arXiv 和作者官方 GitHub 对上述直接先例做一手核验；新增本评审文件一件。

本轮未运行研究模型、未调用项目模型/API、未下载或处理数据集、未运行指标、未复现论文、未制作
原型、未修改提案、未改写既有审计件、未 commit、未 push、未发布 wiki。

本审查是 AI 生成的学术评议，不声称自然人博导签字；后续应由 owner/真实导师依据修订稿作正式
行政与学术授权。
