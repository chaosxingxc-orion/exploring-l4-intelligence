---
report_id: SF-SEED-MANIFEST-REPORT-2026-07-15-01
title: "Gate S1 检索协议 seed_manifest.jsonl 生成报告"
date: 2026-07-15
manifest_file: "2026-07-15-sf-seed-manifest.jsonl"
method: "零外部查询——仅枚举本报告§1五个来源文件内已明文列出的条目，逐 arXiv ID 去重，无 web/API 检索"
---

# Gate S1 检索协议 seed_manifest.jsonl 生成报告

## §1 来源与条数（去重前，逐来源枚举）

| # | 来源 | 文件:定位 | 条数（原始枚举） |
|---|---|---|---|
| 1 | proposal v1 §4 最近邻表（15 行） | `2026-07-15-system-first-research-proposal-v1.md` §4表 | 15 |
| 2 | proposal v1 §4 表末「登记说明」评审补充机制族 | `2026-07-15-system-first-research-proposal-v1.md` §4表末登记说明 | 10 |
| 3 | proposal v2 §4 自库反扫四条 | `2026-07-15-system-first-research-proposal-v2.md` §4 | 4 |
| 4 | Gate S1 自库反扫 STRONG 15 条表 | `2026-07-15-gate-s1-own-library-sweep.md` STRONG表 | 15 |
| 5 | 检索协议 v1 §3④ v2 评审 delta-scan 新增 7 条 | `2026-07-15-system-first-survey-protocol-v1.md` §3④ | 7 |
| — | **原始枚举合计** | | **51** |

## §2 去重结果

**逐 arXiv ID 交叉核对（5 个来源两两比对）：零 ID 级重复。** 51 条原始枚举 = 51 条唯一种子，
去重未删除任何条目。已用脚本核验（PowerShell `ConvertFrom-Json` 逐行解析 + ID 去重计数）：
51 行、51 unique id、dupes 列表为空。

### 冲突清单（ID 级重复）

无。五个来源在本次任务限定的枚举范围内彼此不共享任何 arXiv ID。

### 非重复但值得记录的「近撞」（不计入冲突，仅登记供协调者知悉）

- **ACE (2510.04618)**：出现在来源 5（评审 delta-scan，本次列为种子）；同一 ID 在
  `2026-07-15-gate-s1-own-library-sweep.md` 的 **MEDIUM** 桶（非 STRONG 15，本次任务范围外）
  也有记录，且该文件自身注明"自反扫 MEDIUM 升列名"——即 ACE 从自库反扫的 MEDIUM 层被评审
  delta-scan 独立点名后升格为列名种子。因 MEDIUM 桶不在本次任务枚举范围（任务只要求 STRONG
  15 条），未造成 ID 级重复，但两个来源指向同一篇文献这一事实值得记录。
- **协议自身计数不自洽（供协调者核正典用）**：`2026-07-15-system-first-survey-protocol-v1.md`
  frontmatter/§3 声称"57 列名种子快照"，其正文四个子项之和为
  15（①）+16（②）+15（③）+7（④）=**53**，与其自称的 57 已有 4 条内部不一致；而本次任务
  按明文枚举实际可取得的②「评审补充机制族」arXiv ID 只有 **10 条**（AWM/ExpeL/Self-Refine/
  CRITIC/TPO/HuggingGPT/AudioGPT/DSPy/TextGrad/TTRL），非协议声称的 16 条——即 15+10+15+7=47，
  加上来源 3（proposal v2 §4 自库反扫四条，不在协议 §3 的①–④四项计数内，是另一批"送审前"
  种子）=51，与本报告的正典数吻合。**协议文档的「57」「16」两个数字均需按本 manifest 修正**
  （或者协议作者需要说明②的另外 6 条题录出自何处、以及 57 与 53 的 4 条差额出自何处——本次
  任务未做该项考证,仅如实登记差异供协调者核实)。**〔已闭合：协议 §3 已按本报告重构为五分类
  15+10+4+15+7=51,「57/16」更正入协议正文——本段为修复前登记,保留作 lineage。〕**

## §3 最终唯一种子总数（正典）

**51**

（脚本核验：51 行 JSONL、51 个唯一 `id`、0 重复。此数取代协议文档中"57 列名种子"的自述，
按本 manifest 的枚举范围与逐 ID 去重结果为准。）

## §4 各来源条数（去重后 = 去重前，因无重复）

| source 字段值 | 条数 | 对应来源 |
|---|---|---|
| reviewer点名 | 18 | 来源1的 AS_CITED_BY_REVIEW 8 行 + 来源2 评审补充机制族 10 项 |
| 自库继承 | 7 | 来源1的 RETAINED_RECORDS@census-v2 6 行 + CoVer（ROUND2_PREREGISTERED_TARGET） |
| 自库反扫 | 19 | 来源3 自库反扫四条 4 + 来源4 STRONG 15 |
| 评审delta-scan | 7 | 来源5 v2 评审 delta-scan 新增 7 条 |
| **合计** | **51** | |

## §5 verification_level 分布

| verification_level | 条数 | 判定依据 |
|---|---|---|
| 题录AS_GIVEN | 22 | AS_CITED_BY_REVIEW（无 TO_VERIFY_FULLTEXT 标注）8 行中的 4 行 + 评审补充机制族 10 + CoVer 1 + 评审delta-scan 7 |
| 题录AS_GIVEN\|delta待全文核验 | 4 | 来源1 表中标注 TO_VERIFY_FULLTEXT 的 4 行：Reflexion / LATS / Voyager / LLM-as-Verifier |
| census在库(题录+) | 21 | 来源1 RETAINED_RECORDS@census-v2 6 行 + 来源4 STRONG 15（自库反扫"仓内已知"，按同一 token 语义类推） |
| 摘要级 | 4 | 来源3 四条（proposal v2 称"均在我方 neighbor-matrix/sota-cards v2"，已有摘要级描述但全文核验前生效，非题录、未达全文） |
| **合计** | **51** | |

**〔本表为协调者裁决前快照;裁决后现值（见底部附注）：census在库(题录+)=22 / 摘要级=3
——scaling-auditory 改判所致,manifest 为正典。〕**

注：来源4（STRONG 15）在其原文件中并未使用 RETAINED_RECORDS@census-v2 这个字面 token，
而是文件自述"两类『仓内已知』都被本次反扫检回"——本报告按语义等价类推为
`census在库(题录+)`，这是本次生成中唯一一处非字面 token 匹配的推断，如实标注供协调者复核。

## §6 scope_pending 分布

`Y`：仅 1 条 —— **training-free-grpo (2510.08191)**（proposal v2 明文："TF-Strict 归属待核"，
因其外设经 ground-truth 多轮学习 token prior，冻结核心是否满足 TF-Strict 待核）。
`N`：其余 50 条（含 walking-through-uncertainty / scaling-auditory / inference-time-reward-hacking
——三者均为「直接占据」判定，非 TF 归属待核类；IRO 2506.17828 本身不在本次五来源枚举范围内，
未产生第二个 Y）。

## §7 lanes 分配统计（八 lane，条目可 1–3 个 lane，总计数 74 = ΣLanes——此 74 系**快照51
期的 lane 重数和**,与现行种子条数 74 数字撞脸纯属巧合;批次2 后现行 lane 和 = 111,见增量
批次2 附注）

| lane | 主题 | 命中条数 |
|---|---|---|
| SF-L1 | reasoning+acting 环境反馈 | 7 |
| SF-L2 | test-time agent feedback/control | 12 |
| SF-L3 | multimodal/omni tool agents | 13 |
| SF-L4 | external memory/skill acquisition | 7 |
| SF-L5 | training-free verification/control | 17 |
| SF-L6 | black-box/API-only 优化 | 10 |
| SF-L7 | reward hacking/Goodhart | 2 |
| SF-L8 | 等预算评测/trajectory credit | 6 |
| **合计（含多 lane 重复计数）** | | **74** |

**〔本表为协调者裁决前快照;裁决后机器实测（见底部附注）：L1=8/L2=13/L3=13/L4=7/L5=17/L6=9/
L7=3/L8=6,Σ=76。〕**

**"(lane 待协调者核)" 标注条数：10（初稿误记 12——manifest 机器 grep=10,名单即下列 10 个）**
——LATS / CoVer / TTRL / Large-Language-Monkeys(Brown) /
Speech-Copilot / walking-through-uncertainty / scaling-auditory / Omni-Decision /
Effective-Feedback-Compute / ACE，均为多主题交叉或资源轴描述语言类条目，lane 归属判断依据
不够单一，已在 manifest 逐行 rationale 末尾加注，供协调者裁定。

## §8 已知限制（如实声明）

- 本 manifest 严格限定于任务指定的五个来源文件中**明文列出**的条目；未执行任何新的
  arXiv/Semantic Scholar/OpenAlex 查询，未做 backward/forward citation chaining（那是协议
  §5 签署后才执行的动作）。
- lane 分配为协调者层面的主题判断（非算法/评审机制产出），标注"(lane 待协调者核)"的 10
  条（初稿误记 12）建议由协调者在协议执行前复核；未标注的条目视为合理置信但仍可在协议执行中修订
  （taxonomy 版本化，协议 §10）。
- verification_level 中 21 条（裁决后 22——scaling-auditory 改判,见 §5 现值注）"census在库(题录+)"对来源4（STRONG 15）是语义类推而非字面
  token 匹配（详见 §5 注）；来源3 的"摘要级"判定亦为推断（该文件未使用五级证据分级中的
  字面 token）。这两处推断已在本报告中显式标注,不构成静默判定。

---

## 协调者裁决附注（2026-07-15,逐行亲验后）

- **计数正典确认**：51 条唯一种子（零 ID 重复）——协议/热层的「57」「16」系协调者算术口径,
  已按本枚举更正（协议 §3 快照构成重构为五分类 15+10+4+15+7=51）。
- **lane 裁决**（10 条挂标全部处置——初稿两处误记 12,机器 grep=10;3 条修改）：walking-through-uncertainty 补 SF-L7
  （selective-prediction/弃权属停止-弃权轴）;Large-Language-Monkeys 补 SF-L2
  （repeated-sampling 即 test-time scaling 主场）;Speech-Copilot 的 SF-L6 改 SF-L1
  （编排属行动轴,非黑盒优化）;其余确认原分配。
- **核验级修正 1 条**：scaling-auditory 2503.23395 由「摘要级」改「census在库(题录+)」
  （census v2 既往 grep 1 命中）。
- 修正后 lane 命中分布（机器重数,grep 实测）：L1=8, L2=13, L3=13, L4=7, L5=17, L6=9, L7=3, L8=6（Σ=76）。〔初稿附注曾口算 L2=14/L6=8,当场机器重数更正——教训再证:分布数一律 grep,不口算。〕

## 增量批次1 附注（2026-07-15,amendment-1 / §5bis 机制首次使用）

manifest 追加 9 行（不改旧行）：v3 外审 delta 5 条（OmniAgent/CMA-Harness/UCT-ToolCreator
〔scope_pending=Y,第二例〕/ConMem/Argos）+ 基础谱系 4 条（SF-L9 专用,DOI 题录）。
**现行总数 = 60**（机器 wc 实测;快照 51 数字在上文各处保留作 lineage,现行计数以 60 为准）。
scope_pending 现为 2 条（training-free-grpo + UCT-ToolCreator）。

## 增量批次1 后现值分布（机器 grep/解析,内审 MINOR-5 闭合——上文各表与「现值」字样一律读作
「快照51裁决后值」,批次1 后现值以本节为准）

- lane 分布（60 行）：L1=8 / L2=14 / L3=16 / L4=10 / L5=18 / L6=10 / L7=3 / L8=6 / **L9=4**,Σ=89。
- verification_level（60 行）：题录AS_GIVEN=31 / 题录AS_GIVEN|delta待全文核验=4 /
  census在库(题录+)=22 / 摘要级=3。
- source（60 行）：reviewer点名=18 / 自库继承=7 / 自库反扫=19 / 评审delta-scan=12 /
  **评审点名-基础谱系=4**（第五值,协议 §3 schema 已同步登记）。
- scope_pending=Y：2（training-free-grpo 2510.08191 + UCT-ToolCreator 2602.01983）。

## 增量批次2 附注（2026-07-16,amendment-3 A3-7 / §5bis 机制第二次使用）

manifest 追加 **14 行**（不改旧行）,来源 = v3 收官就绪度评审 §4 delta scan
（`2026-07-15-system-first-research-proposal-v3-stage1a-closeout-readiness-review.md`,
source 字段沿用「评审delta-scan」枚举值）：系统结构自动设计与 reward/feedback 搜索 6 条
（AFlow / ADAS / GPTSwarm / RAP / ToT / PromptAgent）+ 通用 agentic system 3 条
（Magentic-One / Agent-S / AutoGen）+ 多模态组合/主动感知/工具闭环 5 条
（Chameleon / Socratic-Models / AVIS / Visual-Sketchpad / VideoAgent-2026）。

- **新字段 `initial_tag[]`**（amendment-3 A3-7 登记,仅批次2 起使用,旧行不补——多值枚举
  DIRECT_THREAT / TRAINED_COMPARATOR / METHOD_LINEAGE / COMPONENT_ANALOGY;初判定性仅管
  阅读优先级,不预判最终纳排结论）。批次2 分布（机器计数）：TRAINED_COMPARATOR=4 /
  METHOD_LINEAGE=8 / COMPONENT_ANALOGY=3 / DIRECT_THREAT=3（多值可叠）。
- **存在性待核**：VideoAgent-2026（2606.23327）ID 在协调者知识范围外——执行首步核验,
  不可解析标 UNRESOLVED（沿用②机制族处置）;Socratic-Models（2204.00598）在默认检索窗前,
  任何查询不可召回,靠列名进入。
- **现行总数 = 74**（机器实测:74 行、74 唯一 id、零重复——追加脚本带重复守卫断言）。
- 批次2 后现值分布（机器 grep/解析）：lane L1=12 / L2=17 / L3=22 / L4=12 / L5=18 / L6=16 /
  L7=3 / L8=6 / L9=5,Σ=111;verification_level 题录AS_GIVEN=45 / 题录AS_GIVEN|delta待全文
  核验=4 / census在库(题录+)=22 / 摘要级=3;source reviewer点名=18 / 自库继承=7 / 自库反扫=19 /
  评审delta-scan=26 / 评审点名-基础谱系=4;scope_pending=Y 维持 2。
