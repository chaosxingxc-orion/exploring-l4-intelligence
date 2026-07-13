# v4.2 提案 append-only 勘误记录（2026-07-13 整改轮）

- **日期**：2026-07-13
- **勘误对象**：`wiki/2026-07-12-research-proposal-v42-external-review.md`（v4.2 提案）
- **触发来源**：`wiki/2026-07-13-v42-doctoral-adversarial-integrity-review.md` §3（F-1..F-10）+ §4（M-1..M-9）的博导级对抗完整性审查
- **owner 裁决**：`wiki/Decision-Log.md` 续28（五项裁决）/ 续29（阶段纪律再纠偏）/ 续30（裁撤 #35）
- **机读处置表**：`docs/integrity/remediation_evidence.yaml`（本轮 finding→fix→证据→checker 规则映射）
- **完整性口径（保持）**：FFP NOT ESTABLISHED；QRP 高风险；独立诚实审计已在 Stage-1 采纳（续28④）。本勘误既非 commit，亦非外部盖章。

## 1. 本轮已受理的审查发现与一句话处置

处置标签：**就地修复**（fixed-in-place）/ **门禁待办**（gated-at-M2/M3，Stage-1 不操作化）/ **owner 裁定**（引注）。

| # | 发现 | 处置 |
|---|---|---|
| F-1 | 主 estimand 与检验对象错配（相对 vs 固定绝对，surrogate 偏松） | 门禁@M3；owner 裁定续29：10% 相对=目标/门禁而非当前操作对象，SAP 附录改标"确证协议草案" |
| F-2 | pre-M2 SESOI 冻结不能再称盲法 | 就地修复：改标 post-observation but externally justified + 撤回盲法措辞；owner 裁定续28② |
| F-3 | 公开确定性评测不得保留强 confirmatory 级 | 门禁@M3：等级标签推迟至 M3 签字，此前不作 confirmatory 宣称；owner 裁定续28① |
| F-4 | 单次 K 池条件推断遗漏生成随机性 | 门禁@M2→M3：§13.4 新增 generation-robust ρ 缺口行（跨 K 池种子期望+下分位） |
| F-5 | 缺 RDU-vs-strongest 承载原子 | 就地登记：`H_RDU_VS_STRONGEST` 具名注册为显式 contested/deferred；m=6 依续29 冻结不变 |
| F-6 | 全语料审计靠模式字符串自证 | 部分就地修复：`docs/corpus.lock.json` + `verify_corpus_lock` fail-closed + 审计轴测试；上游 revision/checksum pin 余为 M1 缺口 |
| F-7 | `answer_presence_expected` scrub 语义反转 | owner 裁定续28：潜伏雷非现行害（生产路径未传 eval_golds、scrub 空转、无数据受损）；修复 tracked@M1 |
| F-8 | "fixed seed equally tamper-evident" 措辞错误 | 就地修复：`deterministic_draw.py` 头改"replayable, not selection-blind"；回信 v5 撤回 tamper-evident |
| F-9 | 一次性 M4 状态机正文自相矛盾 | 门禁@M3（机读状态机推迟）；文档侧 M5 加限定语（见 §2.5） |
| F-10 | 无博士级承载定理（仅 generic argmax-mismatch） | 门禁@M2/理论轨：须有限样本 ε(n,δ,complexity)+算子对齐，否则降级为验证基建 |
| M-1 | 两个 no-harm 原子非正向复制 | 门禁@M3：headline 明确 scoped 为单 focus |
| M-2 | Q-B 单数据集不足承载一般 TFRL 价值 | 门禁@M3：跨集/跨核心正向 equal-K 复制推迟 |
| M-3 | random 对照应用条件期望 pool-mean | 门禁@M3：§13.4 缺口行改比 selector U vs pool-mean；实际抽取仅留作部署模拟 |
| M-4 | 同权重异 prompt 非跨源独立 | 门禁@M2：selector 纳入前须 MEASURED δ_corr（error-correlation/CMI） |
| M-5 | 小簇尾部推断未证成 | 门禁@M2：BCa/studentized/wild-cluster/randomization 经模拟按 Type-I/coverage/power 选 |
| M-6 | 配置多重性账本不全 | 门禁@M2：`experiment_attempt_registry.jsonl` 已增行级 status/claim/inferred；完整 config-selection trajectory 仍 OUTSTANDING（见先验暴露登记册 manual_completion_todo[0]） |
| M-7 | q2q 预训练回生 test query 污染盲点 | 门禁@M2：冻结后 exact/fuzzy/semantic query-overlap 审计推迟 |
| M-8 | 发布快照与仓库状态非事务一致 | 就地修复：见 §2.6（陈旧"4 errors"更正 + release_manifest 机械化） |
| M-9 | checker 通过≠proposal 自洽 | 就地修复机制：新增语义规则 + scope disclaimer；人工/独立审查与机械 lint 分栏 |

## 2. 文档侧记录变更（changes of record）

1. **estimand 角色互换（F-1）**：10% 相对错误率下降由"当前阶段操作对象"改标为"北极星目标/未来门禁验收标准"；确证统计附录整体标"确证协议草案（M3 冻结生效，Stage-1 无操作效力）"（续29）。
2. **generation-robust ρ + pool-mean 对照（F-4 / M-3）**：§13.4 新增两条诚实缺口行——ρ oracle-头空实现率定义为跨 K 池种子的期望+下分位、外层重采样 group/内层重采样 generation replicate；primary equal-budget random 对照改比 selector U vs pool 均值 U 的条件期望。二者均门禁@M2–M3，本版不操作化。
3. **`H_RDU_VS_STRONGEST` 原子（F-5）**：具名注册为显式 contested/deferred（非静默降为散文/丢弃）；m=6 primary family 依续29 冻结不变；promotion 或弱原子置换决定推迟至 M3。
4. **SESOI post-observation-externally-justified 重标（F-2）**：Q-B 两支 SESOI（abs/sup）改标"post-observation but externally justified"，明确撤回 blindness/pre-observation 措辞；全部先验效应观测（含 C-ASR-V2 selector 电池）在 `docs/integrity/prior_exposure_registry.json` 全量公开。
5. **M5 限定语（F-9）**：M5 表述加限定——M4 FAIL 为终局，任何后续复制须为**新 program ID**，不得复用原 family/seed/confirmatory 标签；机读状态机推迟至 M3。
6. **陈旧"4 errors"更正（M-8）**：§13.4 gap 表由旧快照"现有 4 errors"更正为活体标准入口 `PYTHONPATH=src pytest -q` = **159 passed / 0 errors**（旧快照标注为陈旧）；`docs/integrity/release_manifest.json` 机械化记录各 repo SHA+dirty+活体 pytest+活体 checker，防发布快照再度失真（discrepancy register item 1/2）。

## 3. 记录纪律（footer）

本文件为 **append-only 勘误记录**：仅以**新增 dated 条目**更新，绝不改写或删除既有条目。任何后续整改轮次追加于本文件下方，并注明日期、对象 SHA 与新处置。
