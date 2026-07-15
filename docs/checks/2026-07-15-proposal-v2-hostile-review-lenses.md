# system-first proposal v2（送审版）敌意内审环原始工件（R1 双镜头 + R2 收敛复检）

（环设计说明：按 v1 环教训（docs/checks/2026-07-15-proposal-v1-hostile-review-lenses.md 末节）
新增「机制叙述 vs 原文」与「自库覆盖率」两镜头。CONVERGED = 环内判定（一轮零新发现），
不等于外部评审通过。）

## 镜头 1（事实/指针/评审转述准确性,Opus）——1 MAJOR + 4 MINOR

- **[MAJOR]** §0.2-2「AWM/ExpeL 不在我方库中,系你的净新贡献」失真：严评 P0-LIT-1 定性
  「已出现在团队历史 survey」成立——`2026-07-04-stage1-3w-crossdomain-comparisons.md:419`
  与 JitRL 同句点名 ExpeL/AWM；survey/README θ2 段列 AWM。窄读（census v2 内 grep 0 命中）
  可辩护,但「净新贡献」比「不在 census v2」强,被自库文件证伪——正是严评所警的
  selective-omission 观感;错误由续50 继承。
- [MINOR] §11 ⑥ locator 枚举漏 equation（严评原文四元）;其余七项转写逐项忠实。
- [MINOR] §0.3「Checkpoint A–E 全部并入 §11」对 E 过度陈述（E 属工程纪律,落 §8）。
- [MINOR] §1「九行合同」实为八行（north_star_metric 删除后 S0 = 8 字段）。
- [MINOR] §0.2-3「四镜头」与归档件「R1 三镜头+R2 复检」措辞漂移。
- PASS：§0.3 处置表对两评审的转述忠实（撤回清单五项/两标签/Gate S1 状态串/改名建议归属/
  诚信裁定）;严评四行 delta 更正转写忠实;P0-LIT-1 五篇与机制族 arXiv 编号逐一相符;
  「见 v1 §N」指针全部有效,「表内 15 项」实数准确;S0/census/ledger/round-2 数字与状态全部
  核实;续48/续50 引用相符;无新增未披露承诺。

## 镜头 2（术语纪律 + 自库覆盖率 + 机制叙述残留,Opus）——2 MAJOR + 2 MINOR

- **[M1 MAJOR]**（与镜头 1 交叉证实）AWM/ExpeL 自库覆盖失实——同一「检索失效」失败模式在
  同批次内复发;续48 的 census-v2 口径裁决可辩护,v2 的无限定「我方库」+「净新贡献」措辞与
  广义「查自库」新规矛盾。
- **[M2 MAJOR]** mandatory seeds 全集遗漏自库 neighbor-matrix Section B 的 DIRECT 占据者：
  training-free-grpo 2510.08191（北极星最直接机制近邻,v1/v2 全文零出现）/
  inference-time-reward-hacking 2506.19248（Goodhart 检测选择概念占据者）/
  walking-through-uncertainty 2604.25591（冻结 Qwen2.5-Omni selective-prediction DIRECT）/
  scaling-auditory 2503.23395（自评最紧 omni 机制占据者,仅散文提及未列名）——列名种子缺失
  ⇒ citation chaining 不以其为锚。中量候选另列六条。
- [m MINOR] 评审来源流程 token（PROVISIONAL_STAGE1A_TAXONOMY 等）有 gloss/出处但未登记,
  与本件援引收词纪律拒绝改名的做法不对称。
- [m MINOR] 字面「首个」一处（版本序用法,实质合规但会命中机检）。
- PASS：撤回口径零出现（~93/305/12/12/I4 whitespace/全局 NO_DIRECT_MATCH/「唯一主问题=ρ」/
  A-SEL 全部 grep=0）;C 码未复活;四行 delta 让步性表述+TO_VERIFY_FULLTEXT 无过度乐观残留;
  TF-Strict 全文一致无放宽;无实质「首个」宣称。

## R1 合并与修复（协调者逐项亲验）

2 独立 MAJOR + 6 MINOR。修复：①AWM/ExpeL 改四要件限定口径（census v2 grep 0 命中 + 广义
自库 07-04 踪迹 + 不作「评审净新」+ 注明更正续50）;②§4 补 4 条自库反扫列名种子（各带定位句）
+ 系统性自库反扫协议步骤 + 6 条中量候选;③equation 补回;④Checkpoint E 归属改 §8;⑤八行;
⑥「R1 三镜头+R2 复检（四代理）」;⑦README 补登五流程 token;⑧「第一份送审版」。

## R2 收敛复检（Opus,独立）——CONVERGED

8/8 FIXED（行级证据齐,四新种子 ID 独立命中 neighbor-matrix-v2;AWM/ExpeL 四要件的自库文件
行号独立核验;「九行」「首个」残留 grep=0）+ 新鲜扫描零新发现（§4 种子段 ⟷ §11「§4 全集」
回指一致;表格/blockquote 结构完好）。
