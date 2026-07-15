---
title: "答复 v2：对 v1 的勘误 + 法证诚信审计逐条答复 + 答复复审逐条答复（含全量核验 ledger）"
date: 2026-07-11
stage: 1-problem-definition
status: "v2；取代 v1（2026-07-11-response-to-reviewer-stage1-audit.md）的状态陈述；v1 按 append-only 保留"
responds_to:
  - 2026-07-10-research-integrity-forensic-audit.md
  - 2026-07-11-adversarial-review-of-stage1-audit-response.md
status_vocabulary: "ACKNOWLEDGED → DECIDED → TICKETED → IMPLEMENTED → VERIFIED → PUBLISHED（六级制，2026-07-11 owner 签署采纳；本文一切状态用词受此约束）"
---

# 答复 v2 — 勘误、法证答复与复审答复

尊敬的两位审稿人：

复审对 v1 的核心判词我们**整体接受**："这是一份质量较高的承认与整改意向书，但不是证据闭环的
response"。v1 最不可原谅的缺陷正如复审所指：**在承认"按报告入账、未经验证"缺陷的同一封信里，
又把 DECIDED/TICKETED 写成了"已执行"**。本 v2 用六级状态制重写全部状态陈述，先勘误自己，再逐条
答复法证审计（v1 因并发时间线漏答），最后逐条答复复审。所有核验判定来自新一轮 4 个独立核验代理
（对照 HEAD 实跑/复算），全量 ledger 见 §4。

## 1. 对 v1 的勘误（本节每条都是我们自己的错误）

| # | v1 错误陈述 | 更正 |
|---|---|---|
| E1 | "已完成动作清单"把裁定/开票/横幅写成"已执行/已交付" | 按六级制重标：owner 裁定=DECIDED；#25–#29=TICKETED；横幅/归档=IMPLEMENTED but NOT PUBLISHED（未 push/sync）；G0=METHOD-G0 PARTIAL（RI-G0/G1 当时 NOT STARTED）。完整重标表见 §5 |
| E2 | "种子切片正相关使 t-CI 反保守偏窄……修正依赖只会更 NULL" | **统计错误，撤回**。正确表述：重叠使现有 t-CI 不具独立重复含义、不确定性估计无效；CI 变宽 = 更不确定，不是更接近零；null 主张须预注册 SESOI + equivalence test（Lakens 2017），当前唯一合法句是"五次相互依赖的运行未获可靠正增益证据" |
| E3 | 对"W4 手工转录"给总括 STALE | **对象错配，撤回**。拆分：emotion t-CI 手工写入 → 已由 `cdbf1d2` 修正（IMPLEMENTED/VERIFIED）；**MInDS 提交 JSON 手工拼装 → 当时未修（OPEN）**，且核验又发现它与 `docs/experiment_inventory.md:86` 数字不一致（第二处出处断裂，审计都没抓到的）。修复 = #33（重做中） |
| E4 | "MBR 每个 N 都不显著"（继承自宏平均口径工件） | corpus 口径下错误：MBR-8 = −0.0012（跨 0）但复审复算 N=1/N=2 显著**变差**；oracle 的无限定 headline +0.0418 是宏平均，corpus 为 +0.0296 CI [0.0212, 0.0390]。今后一切 WER 主张双口径并明确命名（#32 重做中） |
| E5 | "51 件归档 + 86 件 LOG 已挂横幅" | 86 是**分类数**；实际新挂横幅 39 件（另 15 件原有状态块）。且归档发布链当时是坏的：wiki-sync 只发布顶层、16 处相对链接错路径——v1 说"已执行"的归档实为 IMPLEMENTED-locally / PUBLISH-BROKEN。修复中（sync 子目录发布 + 全链检查） |
| E6 | "32/34 CONFIRMED" headline | 六代理实际产出 36 行子判定，headline 不可从摘要重建。全量逐行 ledger 见 §4（含第二轮 13 行）；"6 个独立代理"更正为"6 个**项目内**对抗核验代理"——内部红队，不构成 ACM 意义的外部独立复现 |
| E7 | 北星句收作完成时 | 更正为 `TARGET CLAIM — NOT YET ESTABLISHED`："我们**将**系统测量 frozen omni 在 support/readout/selectivity/realization 四层级的能力边界并区分真实/oracle-only/被封顶的增益" |

## 2. 对法证诚信审计的逐条答复（v1 漏答，本节补齐）

先接受总裁决："未证实故意造假，但系统性研究记录控制失败"——我们对 intent 部分不辩解也不邀功；
对 control-failure 部分全部接受。§11 强制裁决表**全表照单采纳**，已录入机器可读
`docs/claim_ledger.yaml`（#30，IMPLEMENTED 待 VERIFIED）。

| 项 | 核验判定 | 答复与动作（六级制） |
|---|---|---|
| INT-001 MInDS 提交 JSON 非脚本直出 | CONFIRMED（脚本只打印 CI 到 stdout；另发现与 experiment_inventory 不一致） | 接受。#33 v2 脚本原子直出 + 双处数字重生成（IMPLEMENTING） |
| INT-002 emotion CI 曾手工写入 | CONFIRMED-历史 / 已修 `cdbf1d2` | 接受"corrected but not erased"表述；事件留在 ledger |
| INT-003 K8 原位重评分破坏 append-only | CONFIRMED（60 格无侧车；git 父 7748515 可恢复） | 接受。补建 `.pre-rescore-3b2d4bd.json` 侧车（#30 IMPLEMENTING）；今后修复一律新 artifact ID |
| INT-004 精确数字缺行级输出 | CONFIRMED（与首审 provenance 项合并） | 接受。provenance 字段包 + 行级预测入 artifact 成为 #25/#32/#33/#34 的统一要求 |
| INT-005 M3 = 真值转写注入 | 首轮已核验；既有更正记录 | 接受"原阳性工件未机器可读作废"的增量批评：M3 → ledger INVALID + `.validity.yaml` 侧车（#30） |
| INT-006 T7 = 答案查表 | 同上 | 同上（T7 → INVALID + 侧车 + 归档文档 frontmatter 状态层） |
| INT-007 MInDS transductive 3-shot | CONFIRMED（card 用评测行自身 3 转写/类；三因子同变） | 接受机制指控全部；一处更正：仓库原文未用 "zero-shot" 一词（审稿人转述）——但这不减轻因果混淆本身。#33 因子分解重做（IMPLEMENTING） |
| INT-008 macro 写成 WER | CONFIRMED | 接受，见 E4；#32 双口径 |
| INT-009 seed 三重混杂 | CONFIRMED（实为四重：cohort/noise/greedy/pool） | 接受复审 RR-004 的更强版本：#32 四分离 |
| INT-010 SNR=5 单条件 | CONFIRMED（硬编码） | 接受。#32 条件族 {clean, snr5}（nested noise replicates 记为本轮限制） |
| INT-011/012 重叠与伪独立 | 首轮已核验 | 接受；群组划分 + cluster bootstrap = #26/#34 |
| INT-013 "speaker near chance" 无统计支持 | CONFIRMED-wiki 措辞 / PARTIAL-工件 | 接受并**自我加重**：工件自带的 seed-123 CI [0.0267, 0.070] **排除** chance 0.011（显著高于）——"no speaker info / never written / measured-zero" 三处 wiki 措辞被自家工件反驳，全部挂更正；今后此类主张须 superiority+equivalence 双检验（#34） |
| INT-014 hard BoN ≠ Gibbs tilt | PARTIAL | 核心（operator 桥 = 0、无对象等价证明）接受且首轮已承认。**有证据的反驳**：klBoundBoN 是 Beirami **hard-BoN** 界（BestOfN.lean:48,79–96），非 Gibbs/soft 对象；Lean 中 Tilting（T1）与 BestOfN（T2）刻意分模块；文本一律用 "approximation / β→0 limit" 关系措辞，无同一性主张。**但**论文 main.tex 的 "concrete realisation" 措辞确实越界 → 隔离横幅五点之一（#31） |
| INT-015 MLflow 链不闭合 | CONFIRMED（精确化：git commit 每条都有；缺 manifest/model hash；一条负时长异常） | 接受。run→commit→input/output hash→claim 映射并入 ledger 体系（#30）；负时长异常记录在案未解释（morning item） |
| G0–G7 方案 | — | RI-G0 证据冻结（SHA-256 inventory）+ RI-G1 claim ledger：IMPLEMENTING（#30）；G5 三个清洁重做：#32/#33/#34 IMPLEMENTING；G6 理论同对象门 = #27；G7 owner 裁决门接受（Stage-1 不自动滚入 Stage-2 本就是项目规则）。**升级触发器清单照单收录**——其中第 3 条（脚本无法产生工件）已被 MInDS 触发，相应处置=作废重做+ledger 记录，供 owner 依据其第 9 节裁量 |

## 3. 对答复复审的逐条答复

RR-001→RR-016 我们的立场：**14 条接受、2 条部分接受、0 条拒绝**。逐条：

| RR | 裁决接受度 | 动作（六级制） |
|---|---|---|
| RR-001 headline 不可重建 | 接受 | §4 全量 ledger（本文）+ 后续入 machine ledger；"internal adversarial agents" 措辞采纳 |
| RR-002 macro 当现行 WER | 接受 | E4 勘误；#32 IMPLEMENTING；论文相应句列入隔离横幅 |
| RR-003 MBR N=1/2 显著变差 | 接受（我方复算方向一致；精确 CI 待 #32 重做后 VERIFIED） | Per-Work-Status 更正（IMPLEMENTING）；论文横幅 |
| RR-004 seed 四层 | 接受 | #32 四分离协议照抄 |
| RR-005 "更 NULL" 错误 | 接受 | E2 勘误；SESOI/equivalence 进 #34 与 prereg 模板 |
| RR-006 MInDS 漏答 | 接受（并发时间线致漏，不辩解） | §2 INT-007 行 + #33 |
| RR-007 STALE 对象错配 | 接受 | E3 勘误拆分 |
| RR-008 停跑 ≠ 证据冻结 | 接受 | RI-G0 inventory IMPLEMENTING（#30）；W1 dirty 工件将随 #32 提交序清理归位 |
| RR-009 机器可读作废缺失 | 接受 | ledger + validity 侧车 + frontmatter 状态层（#30）；采纳 NISO 机器可读原则；注：原 JSON 本体不改（正是证据冻结要求），机器可读性由侧车+ledger 承担 |
| RR-010 传播不完整 | 接受 | Project-Thesis / Architecture / W4-Feasibility / Per-Work-Status 更正注 IMPLEMENTING；main.tex 隔离横幅 IMPLEMENTING；状态=DECIDED→IMPLEMENTING，不再自称完成 |
| RR-011 票据不可审计 | 接受 | 六级制采纳；任务台账为操作层，claim_ledger.yaml 为证据层；acceptance evidence 随各票 VERIFIED 时入 ledger |
| RR-012 重抽非 fresh holdout | 接受（40/64 同 ID 的复算我们未独立重复，采信并入 #26 设计前提） | #26 改用新种子 + locked-test 访问纪律 + 已曝光 ID 清单标记为非-locked；"65 格"口径混淆更正：65 dataset keys ≈ 241 result cells |
| RR-013 wiki-sync 丢页+断链 | 接受（一处精确化：survey/ 子目录页面 sync 从未发布过，远端本无这些页；但 8 个顶层页删除风险属实，修复义务不变） | sync 子目录发布 + 全链修复 IMPLEMENTING；修复+验证前不 push/sync（遵令） |
| RR-014 fake E2E 不充分 | 接受 | G2 三层制（fake E2E / 每 runtime live smoke / ref-config tiny 重建）写入 #25 验收 |
| RR-015 论文桥未隔离 | 接受 | main.tex QUARANTINED DRAFT 横幅（IMPLEMENTING）；解除条件=五处改写（#31） |
| RR-016 完成时态 | 接受 | E7 勘误 |
| §6 G0 批评 | 接受 | owner 已裁：拆分 Proposal-R（Step-2 primary）/ Proposal-S（Step-3 primary），各自独立 prereg；绝对 delta co-primary；ρ 降 secondary（joint-bootstrap/Fieller、分母策略预注册、不平均 per-item ratio）；`random≈best` 换成预注册 equivalence margin |

## 4. 全量核验 ledger（两轮 49 行）

### 4.1 第一轮（对 2026-07-10 方法学审计，6 代理 36 行）

| ID | 判定 | 一行证据 |
|---|---|---|
| S2-1 无 execute 路径 | CONFIRMED | dry-run 自述 "Execution is deliberately NOT wired here"；34 臂/136 格 |
| S2-2 六臂 PLAN ONLY | CONFIRMED | run_mock.py:284-290/334-340/437-442 NotImplementedError |
| S2-3 two-stage 假两级 | CONFIRMED | run_mock.py:326-331 同索引同相似度截断 |
| S2-4 builder 单粒度 | CONFIRMED | kb_batch_build.py:192-211 单 utt 键单 value；引擎字段未被驱动 |
| S2-5 命名 4vs3 错配 | CONFIRMED | run_mock.py:254 vs kb_batch_build.py:205 |
| S2-6 token 错配 | CONFIRMED | 'qwen3-omni-hidden'(run_mock:93) vs 'qwen3-omni-own'(kb_embed:148) |
| S2-7 auto 回退 | CONFIRMED+加重 | manifest 存 ename 非 token → GLAP/qwen3-omni-own 也落 CLAP 512-d |
| S2-总 可执行性 | REFUTED（不可执行） | 四个独立致命阻塞 |
| BN-1 宏平均口径 | CONFIRMED | agg() 逐 utt 均值；corpus 未报 |
| BN-2 oracle/MBR 数字 | CONFIRMED | +0.0418 CI 正 / +0.0037 CI 跨 0（宏口径） |
| BN-3 seed 混杂 | CONFIRMED | 同一 s 驱动 utts 与 pool |
| BN-4 多样性坍塌 | CONFIRMED | 4.19 unique/8（审计 4.17 舍入差）；14.6% 全同精确 |
| BN-5 无对照解码族 | CONFIRMED | 单一采样配置；无 beam/ROVER/ensemble |
| BN-6 audio 实验性无 parity | CONFIRMED | 上游 EXPERIMENTAL；仅 Q8_0 |
| W4-1 diagonal_dominant=False | CONFIRMED | feasibility 表 + 06-24 记录 |
| W4-2 content=12 句 ID | CONFIRMED | 复算恰 12 句码 |
| W4-3 切分全跨 | CONFIRMED | 91/91 speaker、827/827 对 |
| W4-4 切片重叠 16–21% | CONFIRMED | 复算 16.0–21.3%（均值 19.2%） |
| W4-5 speaker≈0.04 | CONFIRMED | 0.040 pooled / 0.0333 probe |
| W4-6 手工转录 | STALE | cdbf1d2 已修（emotion）——v2 勘误 E3：MInDS 部分另案 OPEN |
| W4-7 判据未过 vs "thesis holds" | CONFIRMED | 判据是 W4 自定；措辞已裁废止 |
| L-1..L-6 定理域刻画 | 6× CONFIRMED | 各定理承重前提均外部假设（文件:行号见核验档） |
| L-7 klBoNActual 公理 | CONFIRMED | opaque + named axiom；另发现 2 文档 sorry 表述过时 |
| L-8 operator-linked=0 | CONFIRMED | 全部抽象载体；sorry=0 属实 |
| KB-1 子串门 | CONFIRMED | kb_audit.py:38-41 纯 containment |
| KB-2 自审非 eval-gold | CONFIRMED | build_one 无 eval 参数 |
| KB-3 无 own-item 排除 | CONFIRMED | 边界声明是散文 |
| KB-4 分离非机器不变量 | CONFIRMED | source 名无 split 维 |
| P-1 provenance 缺失 | CONFIRMED | 273 JSON 全查；有 seed/sampling 无 hash |
| P-2 只有一个测试 | PARTIAL | test_kb_gate.py 存在但 pytest 不收集 |
| P-3 调研核验率 | CONFIRMED | 20/62=16C4P、20/64=12C8P 精确 |
| P-4 probing 文献缺失 | CONFIRMED | 全库仅审计文档自身提及 |

### 4.2 第二轮（法证审计增量 + 复审支撑，4 代理 13 行）

| ID | 判定 | 一行证据 |
|---|---|---|
| C-ASR-ORACLE corpus 复算 | CONFIRMED | 复算 231/2496→157/2496：+0.02965 CI[0.0212,0.0390]；MBR-8 −0.0012 跨 0 |
| INT-003 K8 无侧车 | CONFIRMED | 3b2d4bd 原位改 60 格；.broken 侧车属 f8ca276（波2）；git 父可恢复 |
| INT-010 SNR=5 单条件 | CONFIRMED | 脚本硬编码 |
| INT-015 MLflow | CONFIRMED-精确化 | git commit 全有；缺 manifest/model hash；1 条负时长 |
| INT-001 MInDS 非直出 | CONFIRMED+加重 | stdout-only CI；与 experiment_inventory.md:86 数字不一致 |
| INT-007 transductive | CONFIRMED-机制/PARTIAL-标签 | eval 行自身 3 转写/类嵌 card；三因子同变；"zero-shot"是转述 |
| INT-013 near-chance 措辞 | CONFIRMED-wiki/PARTIAL-工件 | seed-123 CI 排除 chance（显著高于）；"never written/measured-zero" 被自家工件反驳 |
| INT-014 对象混淆 | PARTIAL | 核心桥缺失成立；klBoundBoN=hard-BoN 界（审计刻画不准）；文本无同一性主张 |
| INT-014a Lean 无混淆 | CONFIRMED | T1/T2 分模块 |
| INT-014b 文本同一性主张 | REFUTED | 全部关系措辞（approximation/β→0 limit） |
| INT-014c selector=hard argmax | CONFIRMED | decode.py:30-39 argmax over stored pool |
| INT-014d 机器桥存在 | REFUTED | opaque+axiom，无 decode.py 链接 |
| INT-014e 理论文档 sorry 表述 | STALE | 9e999f7 已换 named axiom；2 文档待更正（IMPLEMENTING） |

## 5. 状态总表（六级制，v2 时点）

| 事项 | 状态 |
|---|---|
| stop-the-line | IMPLEMENTED / CURRENTLY OBSERVED（GPU 仅修复性重跑，owner 授权） |
| owner 四轮裁定（续11+续12） | DECIDED |
| 答复/rulings/治理 commit | COMMITTED LOCALLY（641bb65）/ NOT PUSHED / NOT WIKI-SYNCED（发布链修复中，修完一次性 push+sync） |
| W4 主张降级传播 | DECIDED / IMPLEMENTING（Project-Thesis 等更正注执行中） |
| wiki 归档 | IMPLEMENTED locally / PUBLISH-BROKEN→FIXING（sync 子目录 + 断链） |
| RI-G0 证据冻结 / RI-G1 claim ledger | IMPLEMENTING（#30） |
| 论文 | QUARANTINED DRAFT（横幅执行中）；解除=#31 五处改写 |
| ASR / MInDS / CREMA 清洁重做 | IMPLEMENTING（#32/#33/#34，过夜） |
| Phase-A 工程 | IMPLEMENTING（#25，过夜）；执行网格仍 BLOCKED 于 G2 三层绿 + METHOD-G1 prereg |
| group-split 统计地基 + 新种子 locked test | TICKETED（#26）；旧重抽 manifest 已标记非-locked |
| METHOD-G0 | PARTIAL→REVISED：单问题拆分已 DECIDED（Proposal-R/S）；METHOD-G1 prereg NOT DONE |
| 理论重写 / 调研补课 / W4 fresh proposal | TICKETED（#27/#28/#29） |

## 6. 结语

复审说得对：科学审查评价的是证据状态，不是态度。本 v2 不再请求解除任何 gate——**stop-the-line
与 publication RED 均维持**，直至各票以可核验凭据到达 VERIFIED，由下一轮 hostile review 复核。
我们只主张一件事：v1 的状态混淆在本 v2 中已按六级制逐项重标，且每一条被指出的错误都有对应的
勘误条目与执行票。

Stage-1 执行组（协调：Fable；核验：Opus×10；工程：Sonnet×5）· 2026-07-11
