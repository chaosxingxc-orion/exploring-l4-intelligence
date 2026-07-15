# system-first proposal v1 敌意内审环原始工件（R1 三镜头 + R2 收敛复检）

（归档目的：外审严评缺陷 6 指出「内部 R2 CONVERGED 无可回放评审原始工件」——本文件为四个
Opus 代理报告的逐字归档。审查基线 = proposal v1 提交前工作树（R1）/ 修复后工作树（R2），
最终定稿 commit 见 git 历史。CONVERGED 为环内判定 = 一轮零新发现，不等于外部评审通过。）

## 镜头 A（授权合规,Opus）——结论：0 MAJOR + 2 MINOR

- 检查项 1（v2 §11 十一节次序完整按序）：PASS。
- 检查项 2（七句禁句含语义等价变体）：PASS——五句被提案显式反驳。
- 检查项 3（五合同 kill test+降级后果、v2 §3 承重项）：**[MINOR]** agentic 合同遗漏 v2 §3.4
  第六项「等预算下与 one-shot selector 可区分」（大体被 kill-agentic 吸收；建议以结构匹配表述
  补回并与 §5 owner 偏离显式挂钩）。其余齐备。
- 检查项 4（「首个」类宣称）：PASS。
- 检查项 5（P0-SYS-1..7 处置）：**[MINOR]** P0-SYS-2（正典陈旧）无处置/遗留声明——实况为
  已由续46 重写+续48 S0 签署关闭，但提案未披露；建议补一行。其余六项均有处置。
- 检查项 6（owner 授权偏离披露）：PASS——§1/§5/§11 三处显式披露。

## 镜头 B（事实与指针核验,Opus）——结论：1 MAJOR + 五类核验全过

- **[MAJOR]** CoVer (2602.12281) 状态 token `RETAINED_RECORD@census-v2` 无据——
  `paper_works.jsonl`（实测 95 行）grep 2602.12281 = 0 命中；其真实登记在
  `round2_new_targets.jsonl`：title_verification=AS_GIVEN_BY_REVIEW、零执行——与提案自身
  「round-2 零执行」口径自相矛盾。对比：IAD 标同 token 正确（census 1 命中）。建议改标。
- PASS：census v2=95 works（实测）；ledger v2=62 行（实测）；round-2=21 lanes/105 零执行；
  574 历史工件；commit 锚 dce5c79/0a5e108/28ad858 与热层一致。
- PASS：S0=SIGNED_VIA_SESSION_DIRECTIVE+TF-Strict，提案如实披露；RESP-02 现行有效；
  scaling-auditory token 与热层一致。
- PASS：全部文件指针真实存在。
- PASS：十条 arXiv 编号与 v2 评审逐一完全一致。
- PASS：owner 裁决转述（三阶段/身份层不立法指标/TF-Strict/黑盒+本地校验）与续45–48 一致，
  无过度引申；探针映射如实标「推荐案、对齐待 owner」。

## 镜头 C（术语与证据纪律,Opus）——结论：2 MAJOR + 3 MINOR

- **[M-1 MAJOR]** 自造 C-BB/C-TF/C-RL/C-AG/C-OM 五码未登记（全仓 grep 零先例），且把
  「C」命名空间扩成第三家族（诚信核查 C1–C5 vs 论文贡献 C1–C3 同名异构前科在案）。建议
  弃码用描述名，或登记+拆名警示。
- **[M-2 MAJOR]** CoVer 误标（与镜头 B 交叉证实），且与自认现行有效的 RESP-02 §3.3
  「2602.12281 尚未入台账（P1 首批）」直接矛盾。
- [m-3 MINOR] 新 token（AS_CITED_BY_REVIEW/TRAINED_COMPARATOR/RETAINED_RECORD@census-v2）
  首现有定义（不违规）但未登记；RETAINED_RECORD 单数与 RESP-02 正名 RETAINED_RECORDS 复数
  有形漂移。
- [m-4 MINOR]「95 works」缺 94 记录簇→95 works 的溯源注记。
- [m-5 MINOR]「Proposal E」无出处限定语（墓碑表警示存在死「方案 A」同名族）。
- PASS：死代号复活（A-SEL/旧 δ_corr 操作化/「唯一主问题=ρ」）零出现；证据等级纪律贯穿；
  已撤回口径（~93/305/P0 八项/12/12/I4 whitespace/全局 NO_DIRECT_MATCH）全部避开；
  TF-Strict 语义全文一致无放宽。

## R1 合并与修复（协调者逐项亲验）

合并 = 2 独立 MAJOR（CoVer 误标〔B+C 交叉〕；自造 C 码）+ 5 MINOR。修复：五合同弃短代号改
描述名；CoVer 改 ROUND2_PREREGISTERED_TARGET（token 现场定义并登记 L3 库入口）；agentic 合同
补第六条件（结构匹配表述）；§11 补 P0-SYS-2 已处置披露；token 复数对齐 + 四 token 登记
wiki/survey/README.md；census 计数带溯源 @28ad858；Proposal E 加限定语。

## R2 收敛复检（Opus,独立）——结论：CONVERGED

7/7 FIXED（逐项行级引文核验：CoVer 行+token 定义 ✓；C 码全文 grep 清零+描述名/kill 名+撞名
理由句 ✓；agentic 第六条件 ✓；§11 第④点 ✓；RETAINED_RECORDS 全文复数一致〔含 frontmatter〕✓；
两处 census 溯源 ✓；README 登记块四 token ✓）+ 新鲜扫描（表格列数/代码块闭合/措辞矛盾/断链）
零新发现。

## 环后外审勘误（后置登记）

同日外审严评另发现环未覆盖的四项（本环镜头只查了 token/指针/合规，未查**机制叙述与论文实际
内容的相符性**、未查**自库覆盖率**）：①Reflexion/LATS/Voyager/LLM-as-Verifier delta 行过度
乐观;②自库 5 条强近邻遗漏（census 在库未检回）;③CONVERGED 措辞需环内限定;④本归档文件此前
缺失。全部已修。**环设计教训：增加「机制叙述 vs 原文」与「自库覆盖率」两个镜头。**
