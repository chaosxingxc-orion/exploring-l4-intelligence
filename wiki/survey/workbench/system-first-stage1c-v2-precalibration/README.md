# Stage-1C v2 Agentic pre-calibration workbench

状态：`AGENTIC_RC2_CODER_READY_NOT_DISTRIBUTED`

本目录是首次提交前原位修正后的 RC2。它落实 owner 的最新范围裁决：专用 Duplex
模型任务不进入研究、复现或 branch 路线；Stage-1C 聚焦 frozen-core agentic 技术演进。
Stage-1B v5 与 320-work union 不改写，RC1 继续作为已审历史对象。首次提交前发现的
coder-visible 标签泄漏已原位闭合；owner 已授权一次本地 no-push commit 与 commit-bound
独立方法复审提交，coder 仍未分发。

## 当前合同

- N=56 仍为 38 个已签 overlay + 18 个 purposive sentinel；
- FDB-v2 因已签 overlay 仅保留为 `OUT_OF_SCOPE_SPECIALIZED_SYSTEM` 盲校准边界；
- FDB-v3 已从 sentinel 移除，由 Active Perception Agent（2512.23646）替换；
- Audio MultiChallenge 仅为 `INSTRUMENT_SUPPORT_REFERENCE_ONLY`；
- AudioGenie-Reasoner 是直接方法首要候选，AudioToolAgent 是 task-matched nearest prior，
  Audio2Tool 是本地 instrument；三者均未被提升为 reproduction anchor；
- 共享协议只冻结接口：
  `observation → external state → signal/evaluator → decision right → action/tool → feedback → update/repair/stop`；
- knowledge、skill、memory 是能力资产，training-free RL 与 multimodal agent system 是控制与承载维度；
- 每个 experiment cell 只能指定一个 `primary_intervention_axis`，防止系统组合收益被重复归因。

## 活跃入口

- `stage1c-v2-precalibration-contract-rc2-zh.md`：范围、输入、输出与门序；
- `codebook-v2.md`：含具名边界裁决的 reviewer-only 完整编码手册；
- `coder-codebook-v2.json`：不含论文具名预期标签的 coder-visible 中性编码规则；
- `calibration-response-schema-v2.json`：唯一 coder response schema；
- `schema-bundle-v2.json`：未来 full mapping 的强类型对象合同与 specialized-system branch gate；
- `calibration-source-byte-manifest-v2.json`：56 篇精确 source bytes、revision、SHA-256 与 receipt；
- `calibration-manifest-v2.json`：reviewer-only 的 38+18 样本身份、选择理由与替换记录；
- `calibration-assignment-manifest-v2.json`：隐藏抽样角色与选择理由的 coder-visible assignment；
- `calibration-blind-packet-v2.json`：label-hidden paper/object blank responses；
- `claim-template-registry-v2.json`：reviewer-only 的 13 个 synthesis templates 与 prior links；
- `claim-template-coder-view-v2.json`：移除 origin/link 的 coder-visible 中性 template view；
- `agreement-contract-v2.json`：paper/object exact agreement 与停止规则；
- `coder-transaction-contract-v2.json`：coder、隔离、暴露与 human adjudicator 前置条件；
- `reproduction-readiness-v2.json`：已知 agentic 候选、instrument、validation carrier 和 K/S/M analogues 的只读闭合；
- `calibration-distribution-manifest-v2.json`：只列 coder-visible 共享内容的待分发输入字节；
- `review-package-manifest-rc2.json`：独立复审 exact manifest。

## 已完成的方法修正

1. `agentic_scope` 使用封闭枚举记录 scope、loop、core dependency、K/S/M assets 与 control role；
2. `DIRECT_AGENTIC` 必须至少具备 `DECIDE + ACT_OR_TOOL`，依赖专用模型或 trained controller
   的工作不能通过直接 agentic gate；
3. agentic fields 与 cell 级 primary intervention 已进入 agreement critical paths；
4. full-mapping paper audit 明确 specialized-system exclusion 不能成为 `CORE_MEMBER` 或 branch primary；
5. 56 篇仍共用一个 paper/object response，非实证工作不伪造 experiment cells；
6. 已知候选统一登记 official source、revision、license、protocol、entrypoint、access、evaluator、
   local state、专用模型依赖、最强 blocker、deviation ledger 与 rejection condition；
7. readiness 全部 fail closed：资产齐全不等于已复现，也不等于 anchor。
8. coder distribution 采用固定 allowlist、递归 forbidden-key/known-label scanner 与单一 shared-content
   bundle hash；两名 coder 的内容必须 byte-identical，身份与提交 receipt 在包外单独绑定。

## 仍关闭的门

- packet 尚未分发，coder A/B 与 human/domain-expert adjudicator 未绑定；
- coder prompt 尚未冻结，agreement 与 adjudication 均未计算；
- 320-work mapping 尚未取得校准后新的 `SIGN_STAGE1C_V2_EXPERIMENT_MAPPING`；
- 没有运行研究模型、API、benchmark metric、reproduction 或 prototype；
- 没有 family/branch selection、项目 novelty verdict 或 Stage-2A 权限；
- 已取得 `AUTHORIZE_STAGE1C_V2_AGENTIC_RC2_REVIEW_SUBMISSION`，但它不授权 push 或 coder 分发；
- 下一动作是创建获批的本地 commit（不 push），再提交 commit-bound exact RC2 package 做独立方法复审。
