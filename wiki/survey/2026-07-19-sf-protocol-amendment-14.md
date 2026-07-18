---
artifact_id: "SF-PROTOCOL-AMENDMENT-14-2026-07-19-01"
title: "Amendment 14 — v8 复审(WITHHOLD,3 Gate MAJOR)整改合同:信号实例身份/承重证据完备/跨平台重放"
date: 2026-07-19
review_ref: "wiki/2026-07-19-system-first-research-proposal-v8-stage1a-doctoral-review.md（審 v8@a4ed640,blob 8761914971）"
owner_ruling: "2026-07-19「好」——全盘 ACCEPT,按 P0-A→B→C+P1 执行;pypdf 依赖接受;release binding 对 v9 起生效"
stage_account: "current_activity_stage = Stage-1A survey-ready gate（尾门）;new_model_touches_since_gate_freeze = 0（起算 af96a89）;cumulative_model_touches = 非零;legacy_experiments = INHERITED_PRIOR_EXPOSURE;本批 discovery_queries_executed = 0"
---

# Amendment 14：v8 复审整改合同

## §1 Gate MAJOR-1 — 信号实例身份（P0-A,已闭合）

**缺陷（评审三反例,我方全部亲手复现）**：行级扁平 signal 字段把多信号系统平均成一个信号——
①行级 lifecycle 与边 lifecycle 矛盾不被拦截（11/11 照绿）;②终局 reward + 另一在线非 reward
信号的边被拼接成 candidate=True（异信号拼接）;③`reward_guided_selection` 不查 lifecycle
（offline_calibration + scored_select 也 True）。根本原因是**数据模型表达力缺口**,非单纯检查
缺口。

**修复（taxonomy v5 + sidecar schema v2 + coding v6,单写链保持）**：
- `signals[].signal_id` 一等实例（form/source/lifecycle/uses/evidence 逐信号）;每条
  control edge 引用 signal_id 且 `signal_use ∈ 该信号.uses`;edge 可选 lifecycle 字段若在
  必须等于所引信号（失配 = validator 红,派生不计——评审验收例 1）;
- **派生全部存在量词化**：`rq = sequential ∧ ∃ 同一信号 s(reward(s) ∧ 有效 LIVE 边引用 s)`;
  `is_reward_guided = ∃ s: reward(s)`;`rgs = 池真实∧policy∈{scored,tournament}∧
  selection_object≠none∧∃ reward 信号 s 含 select|prune`——离线校准信号永不入选;
- **多信号系统如实拆分（评审验收例 5）**：AutoTTS = s_state（在线状态观测,form=none,驱动
  branch/stop 边——落实上轮裁决代理的相位合并观察）+ s_consensus（终态 Agg）;Selective TTS
  = s_stage_judge（在线 prune→branch）+ s_final_judger（终态 select,无前向边）;PDR random-K
  = 零信号行;新增 enum `state_observation`;
- 验收 A1–A7 + killer K1–K7 全绿;评审的异信号拼接构造现判 rq=False。

## §2 Gate MAJOR-2 — 承重证据完备性（P0-B,已闭合）

**缺陷（评审两假绿,我方复现;其一为十轮最重）**：reconciliation 只验「已填证据不自相矛盾」;
翻转 open-sft `control_horizon`（headline 5/11→4/11）与 `p9999` 假页码均 11/11 全绿;固定
数字与生成输出无对账。

**修复**：
- **required-evidence 合同**：15 个承重字段（七 strict 位+visibility/topology/modality/
  horizon/rights/pool/policy）逐行强制证据条目,三类:canon/tex 逐字引文（机器核验）、
  pdf_page（页码∈页数范围+页内 anchor,pypdf）、**absence adjudication**（负命题:结构化
  note+已检视 scope;机器地板=存在性+值绑定,语义真值由裁决哈希连带绑定）;缺条目=字段
  unknown/not_adjudicated,**绝不默认 False 参与 strict 合取**（strict 位三态化）;
- **裁决行哈希绑定（本批最强单防线）**：`adjudication_row_sha256` = 行内容（除裁决字段）
  规范化 JSON 的 sha256;reconciliation 重算比对——**裁决后任何行变更（含单独 horizon 翻转、
  值+证据双翻转）即裁决失效,fail-closed**;
- **locator 真解析**：pN token 必须 ≤ 钉定 PDF 页数（`p9999` 死于 page-out-of-range）,
  邻接 ASCII anchor 于 N±1 页文本内检索;canon/tex 引文核验保持;
- **敏感面突变集（内审环第十层镜头:突变从派生公式敏感面推导,不从上轮评审清单继承）**：
  13 类,在**模拟盖章副本**上跑且断言盖章基线为净（反空洞第二代——脏基线会让任何突变
  空洞变红）;评审三精确反例全部由指定检测器拦截（horizon/双翻转→行哈希;p9999→页码范围;
  lifecycle 失配→validator）;
- **release binding**：`sf_release_binding_check.py`——日期送审件带机器可读 binding 块,
  headline 数字与持久化测试输出逐键对账,负 fixture 自测;对 v9/回应信起生效。

## §3 Gate MAJOR-3 — 正典环境重放（P0-C,已闭合）

**缺陷（评审复放,我方在 `wsl -d Ubuntu-24.04`+Python 3.12.3 精确复现）**：台账存 Windows
`E:/...` 路径,WSL 不可解析→eprint-unreadable→10/11。

**修复**：`scripts/survey/sf_asset_path.py` 单一 canonical resolver（盘符 ↔ `/mnt/<d>/`
双向,六用例自测）;TeX/PDF 读取全部经 resolver。**验收留痕**：Windows（3.14.3）与 WSL2
Ubuntu-24.04（3.12.3）同 commit 同 sidecar 字节 → 同 verdict、同 occupancy、generator
字节等同、非 pending 失败两端均 NONE;测试输出携 platform 字段。

## §4 P1 — 开局文献补齐（已闭合;六篇 6/6 反幻觉核验,access log 在案）

开局表 v3（新日期件,v1/v2 字节不动）：表 A +Reinforced Agent（2604.27233,RQ-SYS 直接近邻,
reviewer 优化态必须拆 path）、+TF-TTCL（2026.findings-acl.1482/2604.13552——**诚信登记:
correction-4 已登记「转录失败」事故第二次复发,「看过但遗忘」类第五例,按评审前令登记
provenance 不称首次发现**）;表 D +Training-Free GRPO（2510.08191,名称碰撞高危边界:
multi-epoch gold 蒸馏 token prior ≠ TF-Strict,仓内 v2 复审定性在案）;新表 E = P2 首批
发现/筛选队列（TRACE/LWE/Min-Seek,各带首批检查点）。全部带角色/去重 ID/预期 route/边界
假设（评审 P1 验收四要素）。

## §5 措辞降级与内审环升级（评审 §9.2）

**dated correction**：v8 中「真 reconciliation」「七类突变 fail-closed」「评审三重语义破坏
已全被拦截」三类陈述相对其检查覆盖为**超额保证**（horizon 假绿/p9999/WSL 10-11 三事实
在案）——v8 为钉定审计件不改字节,更正以本节为正典;整改期措辞采评审给定表述:「当前实现
已验证单写真源、部分字段锚点和既定 mutation 集;尚未证明所有承重语义或跨环境 fail-closed」
——本批完成后的新真值一律以 v5 测试持久化输出与本 amendment 逐项验收为措辞来源（禁止散文自数）。
**内审环第十层镜头**：突变集必须从派生公式敏感面推导（每个能改 headline 的字段都有
突变+证据合同）,不得从上轮评审清单继承——已实现为 V8 的 13 类敏感面集合+模拟盖章反空洞。

## §6 独立再裁决与 CE-v3（结果并入）

**再裁决（隔离 Opus 双代理,schema v2 全 11 行）**：批 A **6 AGREE / 0 DISAGREE**、批 B
**5 AGREE / 0 DISAGREE**——迁移零异议通过;双代理交叉确认「无任何跨信号拼接残留」:每条边
绑定真正行使控制的信号,两个多信号案例被反向正确处理（STTS 真实拆分 vs DREAM 真实不拆——
单一 PRM 真承担三用途）;absence 条目共 8 条全部判 honest scope。七条非致改观察全部登记入
sidecar `adjudication_provenance`（ATLAS rights 引文覆盖 2/3+consensus 复合简化/AutoTTS
probe 保守省略/ToT lifecycle 可辩/DeepVerifier 拓扑-模态惯例接地/open 变体 api_only 引文
出处——均不改任何派生值）。

**CE-v3（非实现者攻击,六案）**：**再次击穿初版 v5 派生**（EXPECTED_TO_FAIL 如实交付）:
**信号内跨用途拼接**——rq 只查边所属信号的信号级 reward 性,不查边自身用途;惰性 prune 用途
+纯 synthesize 边可伪造 rq=True。**当日补丁（第十一层收紧:same-signal 约束下推到用途
粒度）**:`rq 要求 LIVE 边自身的 signal_use ∈ reward_uses`——经核对不破坏任何现有正例
（全部真 rq 行的活边用途本就是 select/prune/revise/stop_budget）;killer 合同增 **A8**。
其余五案为回归哨兵（重叠用途下仅非 reward 信号有活边/rgs 跨信号拼接/池 unknown 三态/
strict 位 unknown 沉没 candidate 而 rq 保真/ATLAS synthesize-over-pool 非 rgs）,当前实现
全部通过并入合同测试 V5。

## §7 门禁现值（收口实测）

- v5 合同测试:**12/12 PASS 双端**——Windows(nt,Python 3.14.3)与 WSL2 Ubuntu-24.04
  (posix,Python 3.12.3)同 verdict、同 occupancy、generator 字节等同（持久化快照 =
  正典环境 posix 运行,含 platform 字段）;
- 机器数字（重算,edge+use 双粒度背书,数值不变）:reward 6/11、rq_sys 5/11（4/8）、
  candidate 0/11、轨迹 2/11（1/8）、reward_guided_selection 4/11;
- 独立反例累计 v1+v2+v3 = 17 案全并入 V5;裁决 11/11 `adjudicated_agree` 带行哈希;
- immutability / 量词 lint / release binding / 单写字节等同:全绿留痕;
- systematic query = 0;research-model/smoke = 0。
