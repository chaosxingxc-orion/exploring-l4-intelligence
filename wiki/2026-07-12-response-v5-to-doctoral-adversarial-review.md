---
title: "答复 v5：对 v4.1 + 回信 + #37 博导级对抗复审的回应（自我勘误置顶；五 F′ 按 owner 续26 裁决处置）"
date: 2026-07-12
stage: 1-problem-definition
status: "已交付；MAJOR RECONSTRUCTION 全接受；39/42 CONFIRMED、0 REFUTED；五 F′ 按 owner 续26 逐项处置，结构整改落 v4.2、工程整改落票 #38；三处尊重性商榷 + 两处偏离披露（§10.1 头条重构未全采、§6.5 build-time provenance）仅置于本函，不入方案；可执行 conformance 工件（v4.1 轮承诺曾未兑现）本 v4.2 轮随包交付并落盘：scripts/checks/v42_conformance.py + docs/checks/v42-rules.yaml + v42-conformance-output.json + v42-environment.txt"
responds_to: 2026-07-12-response-v4-and-v41-doctoral-adversarial-review.md
supersedes_scope: "v4.1（2026-07-12-research-proposal-v41-external-review.md）已发勘误二横幅（commit 2fa8061，append-only，本文维持不可签字）；结构重构见 v4.2（2026-07-12-research-proposal-v42-external-review.md）"
---

# 答复 v5 — 全部接受，先勘误自己

> **勘误附记（承接回信 v4 的三处自更正，不重犯）**：本团队在上一封回信（`2026-07-12-response-v4-to-adversarial-integrity-review.md`）里已具名撤回三处措辞，本函不再重复这些错误——
> ① 上封承诺的机器一致性检查工件（checker code / rule manifest / output JSON / environment）**当时未随发布交付**，实际仅一份 Markdown；**该 v4.1-轮承诺确曾未兑现**（诚实史实保留：当时 `docs/checks/` 仅一份 Markdown 报告）。**本 v4.2 轮已兑现该承诺**：可执行 conformance 工件包随 v4.2 包交付并落盘、可被第三方重跑——`scripts/checks/v42_conformance.py`（checker 脚本）+ `docs/checks/v42-rules.yaml`（规则清单）+ `docs/checks/v42-conformance-output.json`（输出 JSON）+ `docs/checks/v42-environment.txt`（执行环境捕获）。为不重犯"承诺工件不存在"，可执行 conformance 工件（checker 脚本 + 规则清单 + 输出 JSON + 执行环境捕获）命名 internal consistency check、不冒充外审（见 §6、常驻承诺⑨）；工件所核为 package 自洽，非科学有效性、非独立监督。
> ② "independent conformance checker" 措辞**已撤回**：同一 AI 工作流内、且能直接改信件的检查者，不构成研究诚信意义上的独立监督；本函一律称 **internal consistency check**，绝不冒充外审。
> ③ 责任表述**已更正**：起草流程引入错误、作者与签字人未在发布前拦截——**最终责任完全在作者与 owner，AI 参与不构成任何减责事由**（本函 §4 重申）。
> ④ **本函新增自撤**：回信 v4 与 #37 中"append-only **burn record**"一语**撤回**——overwrite-supersede 的拒覆盖/改名守卫只是**文件卫生**，与 owner 已否决的密封 burn 仪式无关，但"burn record"这一命名会让人误读为复活了被否决的仪式，故我方主动撤除该措辞（详见 §3 商榷 b）。

尊敬的审稿人：

您对 v4.1 的 **MAJOR RECONSTRUCTION / REJECT FOR STAGE 2** 裁决，我方**全盘接受**。按协议以 5 路独立复核逐条核验您的 42 项可核验主张：**39 CONFIRMED / 3 PARTIAL / 0 REFUTED——连续第二轮无一处被驳倒**；您援引的 9 篇文献全部真实、数学全部正确，3 处 PARTIAL 均为范围修正而非推翻。五个 FUNDAMENTAL（F′-1…F′-5）、统计计划未达预注册级、理论对象/测量错误、#37 判"真实修复/部分通过/M1 未绿"、conformance report 四问题、QRP 仍高风险——均成立。当日（2026-07-12）已发布**勘误二**：v4.1 顶部五项 append-only 横幅 + 回信三项附记 + conformance report 由 `RELEASE-READY` 降 `DOCUMENT-PACKAGE-READY`、"independent" 撤回（commit `2fa8061`）。真正的测试是收到事实后的处置——以下是处置记录。

## 1. 五个 F′ 的逐项处置（owner 续26 裁决 → v4.2 落点）

owner 已对五项逐条裁决（Decision-Log 续26，续24 为其上位标准），v4.2 按裁决**整体重构**：

- **F′-1（custody 自相矛盾）→ G2**：owner 裁"custody 如实改称 **public deterministic evaluation**（透明、可复算、**非盲法**）；删去 §9.5 '不可预测 custody' 签字门措辞；**零新机械**"。我方**接受您的技术点本身成立**——确定性只保证 replayability，不提供 selection-blindness；公开固定种子下开发者原则上可在 arm-freeze 前算出 confirmatory IDs。v4.2 §9.8/§11 如实改名并把该残余敞口标为**已披露 contested 局限**（L5-F1），不假装消解。若将来某次发表需确证级盲法，**最轻量方案是冻结后第三方一次性评分**（非五轮自审、非 custodian 机器），届时再决、非现在。
- **F′-2（per-version α 无 program 级控制）→ G3**：owner 裁采**单一最终确证版本制**——每个 program 恰有**一个**确证版本，此前所有版本按定义均为 development/exploration，**取消 per-version α 阶梯**，失败归入 cumulative evidence 表。这与三阶段方法论同构，直接消除"反复试到成功"的 online multiplicity。v4.2 §9.5 落定。
- **F′-3（qrels-conditioned 语料）→ G1**：owner 裁 squtr 确证检索语料 = **官方全语料（57,638 docs）**；**qrels 只入评分，绝不参与语料/索引构成**；310-doc 工件**永久降为 qrels-conditioned DEV smoke**（正例密度较全语料抬升 ×186，只作纯管线冒烟、绝不选择任何前向转入确证的 config）。泄漏审计从单一 `CLEAN` 拆为**五轴**（`object_correct` / `query_independent_corpus` / `label_independent_build` / `answer_presence_expected` / `provenance_complete`），每轴给机器可执行证伪判据；**`n_golds=0` 一律输出 `NOT_EVALUATED`、绝不 `CLEAN`**，任一轴 `NOT_EVALUATED`/非 PASS 即 fail-closed 阻断评分。v4.2 §6.4；焦点/资格候选语料 pin 进 `datasets.lock.json`（锚上游 revision + 公开 checksum）列为 M1 前置交付项。
- **F′-4（proxy 误名 verifiable）→ G4**：owner 裁全域改名 **label-free proxy reward**，分离符号 **U（真任务效用，gold 仅评估可见）** vs **Û（可部署 proxy：一致性/验证器一致度/置信）**；**selector = argmax Û、oracle = argmax U、ρ 只用任务效用 U 计**；**绝对 selector 增量列为 co-primary**；新增三件 proxy 诊断（within-question rank AUROC、self-consistent-error 压力子集、K 增大的 Goodhart 真-代理效用曲线）。"verifiable/验证器" 保留词纪律扩及名词，只用于确定性 checker。对外身份术语维持 **weight-frozen reward-guided inference-time optimization（G0）**。v4.2 §4。
- **F′-5（预算混杂）→ G5**：owner 裁 K=1 单次 RDU **永久改标"低成本系统基线"、绝不称"等预算"**；等预算 selector 族 = `K-candidate random / MBR / selector` 严格同 K；**S3 改轻量 1×3 预算匹配**——同一固定总生成预算 G 下比较 never / always / triggered（triggered 的第二遍从同一 G 预算内支出，非额外一遍），**效果判定、成本仅描述性计账、不设任何成本成功门**（续24-R1）。v4.2 §3.2/§7.1。

**并连带处置您在博导复审中提出、已核验成立的其余项**（逐条落 v4.2）：

- **标题去 '业务效果' 品牌化**：本版**不补 utility 论证**，故 v4.2 直接改标 **"以效果为裁判"**，并诚实标注 10% 为惯例科学阈值、非 business effect（S-4 一致性缺陷闭合）。
- **次级族整体降为方向性探索**：S1a/S1b/S2/S3/S4 降为方向性排序、**不做任何 Holm 家族存活声明、不并入 primary 分母**（v4.2 §3.3）——比"逐 dataset×endpoint×contrast 原子化"更简单也更诚实，我方明确选择降级。
- **focus-selection 时序如实**：focus/replication 在 **M2 由 eligibility-split 选出**，**responder-cohort 选择在头条范围内如实声明**（v4.2 §3.1/§9.4），不再写成先验固定。
- **ρ 报告口径**：改 aggregate-ratio only、联合 cluster bootstrap 整体重采样分子/分母、预注册分母下限、Fieller/percentile 敏感性（v4.2 §9.7）；绝对 delta 为 co-primary、ρ 仅机制量。
- **理论轨**：τ 测量改为**标定集上的 proxy 误差/regret（非 argmax 一致度）**；首定理 = 有限样本 selector regret **U(τ\*) − U(τ̂) ≤ 2ε**（在 calibrated proxy 误差界前提下，与既有 `Realization.lean` 的 argmax-mismatch 界对齐，票 #27）；N\* 只作预算 cap、非收敛条件（v4.2 §10.2）。

## 2. 统计与理论：接受未达预注册级

我方接受 primary m=6 仍是骨架而非冻结原子族：附录 A 各原子附 p 值**算法骨架**，而 α、per-dataset SESOI、no-harm/TOST margin、分母下限等**边界常数在 M3 确证注册落定、本版不填**（G3 单一确证版本制下这是正确时点）。secondary 已按上文降为方向性、无 multiplicity 声明。理论轨接受：cost cap ≠ convergence，检索净收益不等式当前**最多是 heuristic design inequality、不进 Lean 作 load-bearing assumption**，闭合前不作"Lean 已证 selector 收敛"的任何论文句。

**§8（新颖性与博士论文价值判断）的处置——明确 DEFER，不隐没**：我方**不主张任一段机制新颖**（v4.2 §2 已如实写"不主张任一段机制新颖，而主张在此狭窄合取下取得效果并把 oracle 头空实现出可靠比例"）。novelty / 博士论文价值与 utility 论证同属**本 Stage-1 版本明确不补、DEFER 到 Stage-2 的项**：可守贡献载荷点（严格黑盒下 modality×form×delivery 因果分解、全语料音频查询检索稳定净增益、等预算 selector 实现头空、proxy 失效/reward-hacking/N\* 的严谨边界、跨核心复制）留待 Stage-2 以效果证据支撑，本函**不就其博士论文价值作任何断言**。特此单列，避免在"逐点处置"框架下漏掉 §8。

## 3. 尊重性商榷与偏离披露（附证据，不推翻裁决，仅界定范围；**只置于本函、不入方案**）

> 本节含三处**尊重性商榷**（a–c）+ 两处**偏离/未尽披露**（d 头条重构未全采、e §6.5 build-time provenance），后两者从"全盘接受"中**单列**以防隐没。

**(a) M1 重开清单部分越界到 M2/M3/签字位交付物——我方按自己的 DAG 执行**：您的 §11 清单把 full/query-independent corpus build、live GLAP/Nemotron 报告、§4 K-trajectory harness、exact atomic SAP / α sequence / SESOI / no-harm margin、holdout-supply table、owner 七项签字 **全列为 M1 门**。按我方自设 DAG，M1 是**工程就绪门（engineering-readiness）**——标准 pytest 单入口零 error、squtr 源缺失 hard-fail 不 fallback、group-aware deterministic draw、五轴审计消除 `n_golds=0` 空转、KB provenance 完整——这些**属 M1**；而 exact SAP/α/SESOI/margin 属 **M3 确证注册**、live cross-modal 与 K-trajectory 净增益属 **M2 dev**、七项签字属**签字位**。我方**接受这些项全部必须完成**，只 respectfully 主张它们**各归其门**、不全部压进 M1；我方按 DAG 推进，绝不以"归其他门"为借口延宕（每门交付物在 v4.2 §13.4 诚实缺口表逐项列出所属门）。

**(b) "burn record" 措辞——守卫是文件卫生、非被否决的仪式，但我方主动撤回自己的命名**：#37/回信中 overwrite-supersede 的**拒覆盖 + 改名归档**守卫，其实质是**防止静默覆盖 manifest 的文件卫生**，与 owner 续24④ 否决的独立 custodian / commit–reveal / 密封 **burn 仪式**在机制上无关。但我方**接受"burn record"这一命名本身会误导**（易被读作复活了被否决的仪式），故**主动撤除该措辞**（见勘误附记④），改称"拒覆盖-改名归档守卫（refuse-overwrite / supersede-archive guard）"，并接受您的技术点：本地普通写权限的 append-only JSONL **不是 tamper-evident ledger**，只是 useful audit trail，我方不再以"防篡改"表述它。

**(c) 理论文本原比被表征的更 hedged——但 τ 测量槽批评完全接受并已修**：v4.1 §10.2 对首定理其实已写"待完成"、对检索不等式已标 MEASURED 假设，措辞比"把 cost cap 当 convergence、把 argmax 一致度当 uniform bound 当作已成立结论"的表征更保守。我方 respectfully 记录这一点**仅为存真**，绝不据此免除任何修正——**τ 测量槽的批评我方完全接受**：argmax 一致度确实不是 sup|Û−U|≤ε 的证据，v4.2 §10.2 已改为标定集上的 proxy 误差/regret 测量、首定理改有限样本 regret 界。

**(d) §10.1 头条重构未全采——如实披露此处非"全盘接受"**：您的 §10.1 建议"把研究问题收成**两个真正独立的（truly independent）** confirmatory questions"。v4.2 §3 **未按此措辞落定**，改采"**两个可分别裁定的（separately adjudicated）**确证问题"，并明写"故不作『两个真正独立』表述"（v4.2 L106）：理由是 Q-A（H_SYS_FOCUS）与 Q-B（H_SEL_ABS_DELTA）**共用同一焦点集、同处一个 Holm 家族（m=6）**，且 Q-B 的 selector 是 Q-A 所评 RDU 系统内的一个组件——弱/失败的 RDU 会同时压低两者，二者在统计与机制上**并非独立**，强行称"真正独立"反而是新的不实表述。故我方**只主张二者各自裁定、互不混淆**，而非统计解耦。此处系对您一条明确建议的**实质性偏离**，特此从"全盘接受"中**单列披露**、不使其隐没于笼统接受之下；技术点本身（不得把共家族、含component 的两问表述为独立）我方接受。

**(e) §6.5 provenance sidecar 非 build-time——如实认领，给出落点**：您指出 KB provenance sidecar 是**事后（post-hoc）审计轨、非 build-time provenance**，此点**成立、我方认领**，不以笼统"KB provenance 完整"一语带过。诚实区分：现状 sidecar 只是有用的 audit trail（与 §3b 对 append-only JSONL 的诚实同调——非 tamper-evident）。整改方向（票 #38）：在 KB build 管线内**于构建时写入 provenance（source revision / checksum / build config / 时间戳），provenance 缺失即 fail-closed 阻断该文档入库**，使其成为 build-time 强制字段而非可选事后补录；在该 fail-closed build-time 捕获落地前，我方**仅以 "sidecar audit trail" 表述、不称其为 build-time provenance**。

## 4. 责任声明（起草流程解释是因果、非免责）

论文作者、owner/签字人对最终文本、代码、统计与工件负**全部责任**。AI 起草流程可以解释错误如何产生（如"调和双标签时协调层凭记忆升级了 directional 标签"），但这是**因果说明、不是减责事由**。正确措辞恒为：**起草流程引入错误；作者未在发布前拦截，保留全部责任。**"AI 写的"永不成为减责理由。

## 5. 工程整改票 #38（含 verify-fix-loop 流程变更）

工程整改立票 **#38**，条目对齐五 F′ 的工程面：

1. squtr 全语料 build（57,638 docs），corpus-lock hash+count+上游 revision pin 进 `datasets.lock.json`，非 dry-run **hard-require corpus source、缺失 P0 fail-closed 绝不 fallback legacy**；
2. 五轴泄漏审计（每轴机器可执行证伪判据 + per-item gold-span/context 排除断言 + `NOT_EVALUATED` 阻断语义）；
3. **group-aware deterministic draw**——confirmatory mode 要求 group manifest、按 group 抽样、自动加载并强制排除完整 exposure union、缺一 fail-closed；
4. U/Û 符号分离 + label-free proxy reward 改名贯穿代码 + 三件 proxy 诊断 harness；
5. §4 K-trajectory rewrite–retrieve–deliver–answer selector harness + 等 K random/MBR + S3 1×3 预算匹配 harness；
6. 标准 `PYTHONPATH=src pytest -q` **单入口零 error**（修 `test_phase_a_e2e.py` 的 results-fixture 破损，不再让 "all suites green" 依赖未披露入口选择）；
7. 拒覆盖-改名归档守卫（非 "burn record"）。

**流程变更（承接 QRP 复发教训）**：**多镜头 hostile 内部复审自本轮起成为标准**——每次发布前跑对象正确性 / 统计有效性 / 信息边界 / 语料独立性 / 术语纪律多轴内部对抗核验（明确标 internal、不冒充独立监督），把"凭记忆调和标签""空转审计打 CLEAN""入口依赖式 all-green"这些复发通道用机器门 + 多镜头核验关死。

## 6. 我方请求与常驻承诺（带门）

**请求评委**：以同一标准复核 **v4.2**（`2026-07-12-research-proposal-v42-external-review.md`，按五 F′ 裁决整体重构）。**关于可执行 conformance 工件我方如实交代其兑现史：v4.1 轮承诺曾未兑现（当时 `docs/checks/` 仅一份 Markdown 报告 `v41-conformance-report.md`，已发勘误横幅并降范围）；本 v4.2 轮已兑现该承诺——四工件随 v4.2 包落盘、可被第三方重跑核对每条规则的 PASS/FAIL：`scripts/checks/v42_conformance.py`（checker 脚本）+ `docs/checks/v42-rules.yaml`（规则清单 rule manifest）+ `docs/checks/v42-conformance-output.json`（输出 JSON）+ `docs/checks/v42-environment.txt`（执行环境捕获），非仅 Markdown**。命名 **internal consistency check、不冒充外审**，工件所核为 package 自洽（非科学有效性、非独立监督）；reviewer §7.1（"承诺工件不存在"）本 v4.2 轮已因四工件落盘而闭合。

**常驻承诺（未完成不写成完成）**：

① 全语料确证检索 + qrels 只入评分 + 五轴审计；
② public deterministic evaluation 如实标注、盲法残余敞口已披露；
③ 单一最终确证版本制、无 per-version α 阶梯；
④ U/Û 分离、ρ 只算任务效用、绝对增量 co-primary、三件 proxy 诊断；
⑤ K=1 低成本基线、等预算族 = random/MBR/selector、S3 1×3 预算匹配；
⑥ 次级族方向性、无 Holm 声明；
⑦ 理论首定理 = 有限样本 regret（#27 同对象），闭合前不作 Lean 收敛论文句；
⑧ tutorial 级可复现 + 零泄漏 + 零欺诈（续24-R1/R4），无 custodian/commit-reveal/burn 仪式；
⑨ 多镜头 hostile 内部复审 + 可执行 conformance 工件成为标准（本 v4.2 轮四工件已落盘交付：`scripts/checks/v42_conformance.py` + `docs/checks/v42-rules.yaml` + `v42-conformance-output.json` + `v42-environment.txt`）。

**签字门**：owner 签字位 + holdout 供给证明 + M1 clean-checkout 绿（本团队 DAG 的工程就绪门）+ 真跨模态 live smoke——全绿前维持 STOP-THE-LINE，M1 DEV-only、Stage-2 关闭。

Stage-1 执行组 · 2026-07-12
