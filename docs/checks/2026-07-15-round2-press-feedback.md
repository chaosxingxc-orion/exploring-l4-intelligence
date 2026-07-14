# Gate-B PRESS 2015 同行评审反馈件

**评审对象**：`wiki/survey/2026-07-15-round2-protocol-v2-instantiated.md`（SURVEY-PROTO-2026-07-15-01，21 lanes / 82 exact query strings，`queries_executed: 0`）
**评审基准**：PRESS 2015 六要素，适配 web/arXiv/scholarly 检索（非 MEDLINE）
**评审性质**：READ-ONLY 预执行敌意预检；无文件写入
**总裁定**：**PRESS_REVISE**（定向修订；全部修复零 GPU、首条查询前完成）
**归档注**：本件由协调者自评审代理返回全文转录归档（原任务输出文件被系统回收）；转录日 2026-07-15。

机械计数核验：18 检索型 lane × 4 = 72，+ L-CHASE 10 = **82** ✓；lane 21 ✓。82 条中 **36 条为文本检索式**、**46 条为 CITATION_BACKWARD/FORWARD 种子指令**。

## 逐要素裁定

### 1. TRANSLATION —— ISSUES
- **L-DIS-A 避开自造术语 → PASS（明确确认）**：仅用标准名（best-of-N/verifier-guided/test-time scaling/self-consistency/coverage/upper bound/oracle），未现 headroom/realization-rate/rho/supply 自造词；带 speech audio 域限定。
- **L-DIS-C 部分覆盖，ISSUES**：覆盖 prompt/context selection、instruction optimization、demonstration selection、in-context example、RAG context ranking；**缺** retrieval-augmented generation 全称、ICL/in-context learning、exemplar selection。**域粒度错配**：两条 keyword 纯文本域，与其 ASR forward-chase（2509.19567 contextual-biasing supply-ladder）不一致。
- **L-SAT-7 最硬 ISSUES**：三语 mega-query（中/西/德混在单条）在 web 引擎上近零召回——多语 lane 的唯一多语查询翻译失效。

### 2. BOOLEAN/PROXIMITY —— ISSUES
- 好：全部词袋短语，无不支持算子的静默依赖。
- 缺陷 A：§3 宣称 IEEE/ISCA 走 `site:` 查询，但 82 条中无一条含 `site:`。
- 缺陷 B：复合专名（best-of-N/AIR-Bench/URO-Bench/Spoken-SQuAD/pass@k）未加 exact-phrase 引号。

### 3. SUBJECT HEADINGS 等效 —— ISSUES
- arXiv 分类过滤全缺（无 cat:eess.AS/cs.SD/cs.CL）。
- IEEE Xplore 进了 §3 表但未进任何 lane engines——ICASSP/TASLP 名义覆盖、操作零覆盖。

### 4. TEXT WORDS —— ISSUES（top-10 缺失变体）
1. `BoN`/`best-of-n`（跨 5 lane，最高杠杆）；2. `re-ranking` 连字号变体；3. `speech recognition`/`automatic speech recognition` 全称；4. **BBAudio 完全未搜**（L-SAT-3 verbatim_target 有、查询无——承重漏检）；5. `PRM`/`ORM` 缩写；6. 数据集去连字号变体（MINDS14/AIR Bench/UROBench）；7. `retrieval-augmented generation` 全称 + `ICL` + `exemplar selection`；8. `SER` 缩写 + emotion classification；9. `selective classification`；10. `inference-time scaling`。⚠ 裸缩写 `TTS` 严禁入查询（text-to-speech 灾难性歧义；现仅注释使用，保持）。

### 5. SPELLING/SYNTAX —— PASS
21 个 arXiv ID 全部格式合法且角色交叉自洽（2026 未来 id 无法核存在性，格式与内部引用一致）；无坏引号。小 nit：德语 `Spracherkennung`（识别）应为 `Emotionserkennung`（情感识别）；`Qwen-Audio` vs `Qwen2-Audio` 系不同代真实模型非拼写错。

### 6. LIMITS/FILTERS —— ISSUES
- date_range `{from: null, to: 2026-07-15}` 合理，无排除性过滤；languages 默认 en + awaiting_classification 合理。
- **L-SAT-7 multilingual 在所列引擎不可实现**：关键洞见——「非英文 SER」的论文本身是英文、发英文 venue；正确写法=英文检索式点名目标语言 + 可选分语言母语查询。

## §13 可追溯性 vs 复审 §8.2 十缺陷 —— PASS（带 2 保留）
十条映射全部指向真实章节、无虚假声称。保留 A：IEEE 名义覆盖无 lane 路由（缺陷 4 对表成立、对操作不成立）；保留 B：§14 preflight 未把 ROUND2-G6（P0-R8 validator）列为阻断前置（复审 §8.3 明列六门全绿才发首条查询）。

## 修复清单（按后果排序）
| 优先级 | 修复项 |
|---|---|
| HIGH-1 | L-SAT-7 mega-query 拆分：英文点名目标语言 + 可选分语言母语查询（德语用 Emotionserkennung） |
| HIGH-2 | arXiv cat 过滤变体 + IEEE `site:ieeexplore.ieee.org` 实际路由（L-SAT-1/6） |
| MOD-3 | 十项 text-word 变体补齐（BBAudio 承重项优先） |
| MOD-4 | L-DIS-C 加音频接地供给选择查询（contextual biasing…ASR…supply） |
| MINOR-5 | §14 preflight 增列 ROUND2-G6 为阻断前置 |
| MINOR-6 | L-CHASE ernez23a 补 Crossref DOI 解析步 |
| MINOR-7 | 复合专名 exact-phrase 引号 + Qwen 模型代次消歧注 |

## 总裁定
```
1_translation: ISSUES · 2_boolean: ISSUES · 3_headings: ISSUES · 4_text_words: ISSUES ·
5_spelling: PASS · 6_limits: ISSUES
TRACEABILITY: PASS_WITH_2_CAVEATS
OVERALL: PRESS_REVISE
```
骨架强（82 条内联无推迟、三 disconfirming lane 齐备、停止规则机械化、第二审三类强制、十缺陷映射诚实）；HIGH/MOD 修完 + MINOR 兜齐后即可交独立 reviewer 做 search-design 签署。全部修复零 GPU、零查询执行。
