---
artifact_id: "SF-S1-V6-RESPONSE-2026-07-18-01"
title: "v6 复审回应信 + Stage-1B survey-execution 签署重申请（第四次;逐项:问题—修改—证据—新数字—未决项）"
date: 2026-07-18
addressee: "Gate S1 评审人 / 评委"
in_reply_to: "《Research Proposal v6 的 Stage-1A 博导级构念、引文与准入复审》（WITHHOLD;2 GATE MAJOR + 4 MINOR）"
verification_first: "逐条独立核验:MAJOR-2 一手源坐实（本地 eprint sha256 = 137d5a93… 与贵审钉定逐字节一致;TeX 'For random-K, we follow PDR and randomly sample K previous summaries' 亲手 grep 命中;'Select-K rollout (selection via RTV)' 同段可见）;MAJOR-1 构造性坐实（派生式确无 reward/序贯/decision-rights 项;三 killer case 全命中;CE-1b vacuous pass 属实）;§9 三项 3/3 反幻觉过且 TeX 引文键（pdr-paper/swe-replay-paper/test-time-recursive-thinking-paper）一手可见——本轮零异议全收"
attestation: "discovery_queries_executed = 0 维持;零研究模型调用;本批联网 = 3 次已知 ID 解引用（逐次留痕）"
---

# v6 复审回应信（问题—修改—证据—新数字—未决项）

## §1 定性

两项 Gate MAJOR 全收。第八轮同型失败的定位收到：**源文-编码 lineage**——合同测试验证的是
我自己手填的值,12/12 全绿稳定复现错误语义。贵审的升级警告收到并已按 locator 立即更正
（PDR 行在收到报告的同一批内重编码,未保留 3/11 一日）。贵审对上轮 2506.12928 异议的正式
维持更正,如实入双向诚信轨。

## §2 逐项（× 贵审 §12 合同与 §13 放行清单）

| 问题 | 修改 | 证据 | 新数字 | 未决项 |
|---|---|---|---|---|
| **P0-1** 身份派生缺 RQ-SYS 内容;K 池被抬成身份;CE-1b 空洞;拓扑裁决被推迟 | taxonomy v3:三分派生（`is_s0_core_compatible` / `is_rq_sys_control_compatible`〔在线 lifecycle∧序贯∧decision_rights 非空;reward 可作用于任一下一步动作权〕/ `is_project_method_candidate`）;K 池降机制分层;`signal_lifecycle` 新增（离线校准标量永不冒充在线 reward）;**拓扑政策 A owner 冻结**（共享权重多调用∈单核——RQ-SYS 机制形态）+ 严格拓扑敏感列全程双算持久化 | 合同测试 v3 **9/9**:三 killer fixtures（贵审 Round C 三例逐一:原生 audio 无 reward ≠ candidate;reward-tool/stop 无 K 池 = RQ-SYS compatible 且 = method candidate;在线二值可验证 = reward）;CE-1b 在敏感列由拓扑轴本身判定（V5b 检查:同 row 强制 omni 后政策 A=true/严格拓扑=false） | s0_core 0/11;rq_sys **5/11 路径（4/8 works）**;method_candidate **0/11**（重立空位坐标） | 拓扑双政策的解释选择留 Stage-1C（owner 已冻结政策 A 为主） |
| **P0-2** PDR 源文错码撑 3/11 | coding v4:#pdr-random-k（form/source/lifecycle=none,use=[supply]——随机采样非选择）;#rtv-pdr-pipeline 带 component_path_ids;全链数字联动（v6 §4.2/矩阵/开局表/DFS 件注记/持久化输出） | eprint sha 一手核验一致;TeX 原句入行注 source_locator;**PDR 错码负控 fixture**（把该行改回 pairwise 必须红——V4 检查过） | strict∧reward∧pool = **轨迹池 2/11（unique work 1/8 双分母）**;原 3/11 撤回 | — |
| **P0-3** projection 是声明非 lineage | 每行强制六 lineage 字段（paper_work_id/fulltext_ref/canonical_record_id/source_locator/coder/semantic_adjudicator）+ reconciliation V7 fail-closed（台账 sha/正典文件+anchor/非空 locator）;**工具链扩展合同**（amendment-12 §3,owner 裁决⑤）:Stage-1B 起 DFS 精读同步产出 per-paper sidecar JSON,coding 行由 sidecar **生成**而非手抄——消灭本轮错误通道;coder≠adjudicator 双角色;fixture 库 append-only;locator 前置;reconciliation 入门禁复跑集 | V7 检查 11/11 行绿 | — | sidecar 生成器 = Stage-1B 首周工具（零查询可建,登记执行合同） |
| **P1-1** ToT 信号分期 | 按全文裁决执行:唯一定义标量 = 离线校准分 Eq.3;推理期 "Evaluation: Assessing the quality and relevance" = 合成内定性评估;无部署期独立 reward 定义 → **profile-conditioned orchestration boundary,移出 reward 集合**（证据句入行注,非猜测——贵审「不确定标 ADJUDICATION_REQUIRED」条款未触发） | 一手 grep 证据句三处 | is_reward_guided = **6/11** | 若贵审读到部署期独立 reward 定义,per 冲突规则可反转（附 locator 即改） |
| **Minor-2** 双分母 | 全部 occupancy 双报 method-path/unique-work;组合路径 component_path_ids 防独立复制误计 | 持久化输出逐键双分母 | 如上表 | — |
| **Minor-3** 反例可证伪性 | killer fixtures 按「单轴变化+old-red/new-green」重造（V3/V4/V5b）;独立反例保留 + 敏感列使 CE-1b 非空洞 | 测试输出 | — | 正/负边界+near-miss 库随 Stage-1B 各轮 append-only 扩充 |
| **§9** 文献与引文 | PDR origin（2510.01123,两路径分行编码计划）/SWE-Replay（2601.22129）入表 A;TRT（2602.03094）入表 C 反例队列;ToT 全题名;DeepVerifier 副标题注记;tau2 证据性使用前钉 commit;DEEPLY_READ 绑定 = 台账 sha | 3/3 反幻觉 + TeX 引文键一手 | 附录 45 条（A.3 = 19） | 三项全文编码在 Stage-1B 开局执行 |

## §3 请求

按贵审 §13 放行清单复核（P0-1 killer cases / P0-2 源文一致与数字闭合 / P0-3 可发现错码）;
0 新 Gate MAJOR → 签署 Stage-1B survey execution;签署后 owner 批准,第一条 systematic
query 即 Stage-1B 起点（全程只看、读、编码、综合,不触碰研究模型）。

—— 研究执行方（W1）,2026-07-18。
