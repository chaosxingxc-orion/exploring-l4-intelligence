---
artifact_id: SF-T1-ROUTES-2026-07-16-01
title: "T1 十会 proceedings 题录发现道——50 条 route manifest（A2-7 实例化,amendment-3 A3-3）"
date: 2026-07-16
status: "FROZEN_PENDING_SIGNOFF——纸面冻结件;全部 entry/status 为冻结时静态知识判断,执行首步逐条核验,差异走版本化增补（不改写本件）"
attestation: "本件编制过程零联网访问——未打开任何 proceedings 页面、未执行任何题录扫描;联网检索查询执行数 = 0"
replaces: "对 v3 收官就绪度评审 G3「A2-7 仍是 prose promise」的闭合件"
---

# T1 十会 proceedings 题录发现道：route manifest

## §1 语义与边界

- **性质 = 发现层,题目级**（A2-7）：扫描 venue-year proceedings 题录 → 冻结词表过滤 →
  命中回 arXiv 题名解析或免费官方源救援（amendment-3 A3-1）。**不是检索查询**,不产出承重
  证据;承重仍走全文强制（A2-9）。
- **route ID** = `SF-T1R-{VENUE}-{YEAR}`;venue 代码 = ACL / EMNLP / NEURIPS / ICML / ICLR /
  CVPR / ICCV / MM / ICASSP / IS（INTERSPEECH）。10 会 × 2022–2026 = **50 条 route**（含
  不举办/未出版占位,见 §2 状态列——「50」是 ID 空间,可执行数以状态列机器计数为准）。
- **执行记录** = 每 route 一份 REC-7 日志（模板见 `2026-07-15-sf-blank-templates.md`）;
  raw 题录列表存 `$SPEECHRL_DATA_DIR/survey-backups/t1-routes/`（永不进 git）,sha256 入日志。

## §2 50 条 route 状态表（冻结 @2026-07-16;状态语义见表下注）

| route_id | 入口（静态知识,执行首步核验） | access | status |
|---|---|---|---|
| SF-T1R-ACL-2022..2026 | `aclanthology.org/events/acl-{year}/`（Long+Short+Findings 三 track） | FREE_OA | 2022–2025 READY;2026 NOT_YET_PUBLISHED（会期 07/08,§5bis 增量扫描承接） |
| SF-T1R-EMNLP-2022..2026 | `aclanthology.org/events/emnlp-{year}/`（Main+Findings） | FREE_OA | 2022–2025 READY;2026 NOT_YET_PUBLISHED（会期 11/12） |
| SF-T1R-NEURIPS-2022..2026 | `papers.nips.cc/paper_files/paper/{year}`（Main+Datasets&Benchmarks） | FREE_OA | 2022–2025 READY;2026 NOT_YET_PUBLISHED（会期 12） |
| SF-T1R-ICML-2022..2026 | `proceedings.mlr.press`（2022=v162;2023=v202;2024=v235;2025/2026 卷号 ENTRY_TO_RESOLVE——执行时按 PMLR 索引页解析并登记） | FREE_OA | 2022–2025 READY;2026 NOT_YET_PUBLISHED（会期 07,PMLR 上线滞后） |
| SF-T1R-ICLR-2022..2026 | `openreview.net`（venue id `ICLR.cc/{year}/Conference`,accepted 全清单;OpenReview 分页规则已冻结于协议内审 R2） | FREE_OA | 2022–2026 全 READY（2026 会期 04/05 已过） |
| SF-T1R-CVPR-2022..2026 | `openaccess.thecvf.com/CVPR{year}`（Main Conference） | FREE_OA | 2022–2026 全 READY（2026 会期 06 已过;CVF 上线核验于执行首步） |
| SF-T1R-ICCV-2023,2025 | `openaccess.thecvf.com/ICCV{year}` | FREE_OA | 2023/2025 READY;**2022/2024/2026 = NOT_HELD（ICCV 奇数年举办,3 条占位 route 不可执行）** |
| SF-T1R-MM-2022..2026 | `dl.acm.org/conference/mm` 各年 proceedings TOC（题录浏览免费） | TOC_FREE_FULLTEXT_PAYWALLED | 2022–2025 READY;2026 NOT_YET_PUBLISHED（会期 10） |
| SF-T1R-ICASSP-2022..2026 | IEEE Xplore ICASSP {year} proceedings TOC（题录浏览免费） | TOC_FREE_FULLTEXT_PAYWALLED | 2022–2026 全 READY（2026 会期 04/05 已过） |
| SF-T1R-IS-2022..2026 | `isca-archive.org` INTERSPEECH {year} | FREE_OA | 2022–2025 READY;2026 NOT_YET_PUBLISHED（会期 08/09） |

**状态语义**：`READY` = 冻结时判断 proceedings 已出版、入口已知;`NOT_YET_PUBLISHED` = 会期未到
或 proceedings 未上线——执行期按 §5bis 增量扫描机制复查（复查事件入 REC-7,不改本表）;
`NOT_HELD` = 该 venue-year 不存在,route 占位不可执行;`ENTRY_TO_RESOLVE` = 入口模式已知、
具体卷号/URL 执行时确定性解析并登记。**access 语义**：`FREE_OA` = 题录与全文皆免费官方开放
获取;`TOC_FREE_FULLTEXT_PAYWALLED` = 题录扫描免费可行,全文回链 arXiv,无 arXiv/免费官方版
→ `REMOVED_PAYWALLED_UNOBTAINABLE`（A3-1 计数移除记账）。

**track 界定（冻结）**：只扫正会 track（上表括注);workshop/demo/industry/tutorial 不扫
（与 venue_tier 语义一致——T3 论文若经其他道发现,按 A3-2 相关性裁决,不由本道供给）。

## §3 题录过滤词表 v1（冻结;命中规则 = A 组任一 ∨〔B 组任一 ∧ C 组任一〕）

- **归一化**：题名 lowercase → Unicode NFKC → `[-_/]`→空格 → 连续空格折一;词表项按
  **词边界整词/整短语**匹配（显式枚举,零通配符——沿用协议「星号陷阱零命中」纪律）。
- **A 组（单独命中即选入）**：agent · agents · agentic · multi-agent · multiagent ·
  tool use · tool-use · tool using · tool calling · function calling · orchestration ·
  orchestrator · orchestrate · workflow · workflows · test-time · inference-time ·
  training-free · tuning-free · gradient-free · reward-guided · reward guided · verifier ·
  verifiers · self-correction · self-correct · self-refine · self-refinement ·
  self-verification · llm-as-a-judge · llm-as-judge · best-of-n · reward hacking ·
  overoptimization · over-optimization · black-box optimization · compound ai system ·
  compound ai systems · copilot
- **B 组（模态/模型词）**：llm · llms · large language model · language model · foundation
  model · multimodal · multi-modal · omni · audio · speech · auditory · spoken · voice ·
  vision-language · vlm · mllm · audio-language · speech-language
- **C 组（机制词,须与 B 组合取）**：memory · skill · skills · planning · planner · search ·
  feedback · reward · verification · self-evaluation · reflection · judge · routing ·
  stopping · abstention · assistant
- **过包容声明**：本词表刻意偏召回——题录命中只进入 BFS 题录级编码,过包容代价 = 筛读时间,
  欠包容代价 = 占据盲区;欠包容由 48 条查询与引文图兜底。词表修订走版本化增补（v2、v3…,
  旧版保留,REC-7 记录所用版本号）。

## §4 题名 → 全文解析流程（冻结）

1. **arXiv 归一化精确匹配**（题名归一化后 exact）→ 命中即回 arXiv 钉版本;
2. 失败 → **模糊匹配候选**（token-set Jaccard ≥ 0.90 或编辑距离比 ≥ 0.92)→ 逐条人工裁决,
   `match_method=fuzzy_adjudicated` 留痕;
3. 仍无 → **免费官方源救援**（A3-1:venue-native ID/DOI + 本地备份 + sha256）;
4. 付费且无任何免费版本 → `REMOVED_PAYWALLED_UNOBTAINABLE`(ID+题名+venue 入 flow report,
   计数披露义务绑定一切占据类结论);
5. 全部解析事件入 REC-7 `resolution[]`,零无记录筛选（修正案 E 同款纪律）。

## §5 停止与计数

- 每 route 停止条件 = 该 venue-year 题录**全量扫描一遍**（题录数、命中数、解析分布全记录);
- route 级计数五元组 `{n_titles_total, n_matched, n_resolved_arxiv, n_rescued_oa,
  n_paywalled_removed}` 由 REC-7 机器汇总——**禁止口算**;
- 全部 50 route 的执行前置条件与 51 条查询相同（reviewer 签署 + owner 批准 + P0-R8 复跑）,
  签署前零扫描（本件 attestation 见 frontmatter）。

## §6 纸面良构性自检（2026-07-16,机器验证——非独立外部验证,独立核验归窄幅复核）

敌意环镜头2 MINOR-4 闭合件。python 机器检查（脚本证据在 Decision-Log 续59 批次会话记录）：
venue 代码恰 10 个且与 §2 表一致 = PASS;年份界 2022–2026、无越界年份 = PASS;NOT_HELD 恰
3 条（ICCV 偶数年）= PASS;词表 73 项（A=39/B=18/C=16）逐项零通配符 = PASS;五计数字段
（n_titles_total/n_matched/n_resolved_arxiv/n_rescued_oa/n_paywalled_removed）齐备 = PASS;
attestation 存在 = PASS;A∨(B∧C) 命中规则声明存在 = PASS。7/7 全过。
