# 2026-07-09 · 理论方案覆盖调研（覆盖阶段材料——只铺全景，不做收敛）

> **性质**：Stage-1 理论方案覆盖调研主文档，落实 owner 三条方法论要求之②（理论要有充足 survey、
> Lean 保证收敛/一致性、显式提取假设与约束项）。**方法**：6 维 Opus web finder（post-2025 侧重，
> text/VLM 域同权重）+ 24 条承重 claims 逐条 Opus 对抗验证（**16 CONFIRMED / 8 PARTIAL /
> 0 REFUTED**；PARTIAL 修正已内联，见 §5）。**产出**：147 claims、**27 个可 Lean 化定理目标候选**、
> 6 组文献空白（= 我们的生态位）。全部候选**不排序不裁剪**——收敛留待 owner 收敛门。
> 明细附录：`survey/2026-07-09-theory-scheme-coverage-appendix.md`（147 claims 全表 + 逐候选
> Lean 可行性）。原始 JSON：session scratchpad `coverage/theory-finder-*.json`。

## 1. 六维要点（全部经验证 gate；标注★ = 对我们最承重）

**D1 kNN 门控理论（21 claims）**
- ★ **TARG（arXiv:2511.09803，training-free 检索门控 SOTA）"Usefulness Calibration" 直接假设
  τ* 存在**（检索有益 ⟺ U>τ*），据此得对 Always/Never-RAG 的支配——**假设了我们要证的东西**：
  把它变成定理（T-B）就是文献缺的那一步。
- ★ 门控信号有现成操作化谱系：Drozdov 2022 按"查询-最近键距离"分桶调 λ（检索质量门，+4% ppl）；
  He 2021 用 base 模型置信度/熵/n-gram 频率训练 retrieve/skip 门（省 50% 检索持平精度）；
  Adaptive kNN-MT 的 Meta-k（k=0=忽略检索）；NEST 的闭式 min-max 距离比→sigmoid 门。
- ★ 负半证据充分：kNN-LM 开放生成不增益（58% token 变差、检索分布熵随生成长度**增长更快**——
  exposure-biased 查询上检索更不可靠）；**Long-Tail Crisis（arXiv:2503.22426）给出频率条件化的
  when-to-retrieve 边界**（低频 token 上 kNN 概率反低于 base——检索恰在最需要处失效）。
- kNN-LM 增益的三成分分解（表示变化 ~55%/近似检索正则化/温度）——协议设计须控这些混淆。

**D2 RAG 理论（25 claims）**
- ★ **RAG-as-noisy-ICL（arXiv:2506.03100）**：RAG 有 ICL 没有的**内在误差天花板**（n→∞ 偏置项
  不消失）+ 存在最优检索数 n*（Proposition 2）——N* 与 τ* 的直接文献先例，含精确形式。
- ★ C-RAG：conformal 保证下的检索生成风险上界（τ/召回下界的 certified 形式先例）。
- ★ **ClashEval 给出 α 的经验函数形**：模型先验答案的 token 概率与 RAG 采纳率呈**一致负线性**
  ——参数固执不是常数而是状态依赖函数，可直接测。
- Adaptive-Chameleon/Stubborn-Sloth：连贯反证据可说服 vs 确认偏误顽固——α 的两态刻画。

**D3 BoN 过优化 / N*（24 claims）**
- ★ **Beirami Theorem 3.1 的精确形式已核**：KL(BoN‖ref) ≤ log n − (n−1)/n 是**上界非等式**、
  前件=奖励唯一性假设——**我们 BestOfN.lean:90 的 sorry 可按此原文处置**（证明或钉为显式引用假设）。
- ★ Inference-Time Reward Hacking（arXiv:2506.19248）：**内部最优 N* 存在性定理**（TP2 + 严格增
  评分下 hacking 不可避免且有内点最优）+ HedgeTune 求根算法 + Best-of-Poisson 连续预算旋钮——
  N* 落地 best-of-N 算子的全套先例。
- ★ Soft-BoN 以 O(1/n) 显式常数收敛到 tilt 最优（温度=信赖域半径）——与 Tilting.lean 直接接轨。
- 过选择偏差（max-order-statistic bias，"More Test-Time Compute Can Hurt"）+ Optimizer's Curse
  ——N* 负半的两个独立锚。

**D4 校准 / τ 形式化（22 claims）**
- ★ over-confidence 从 docstring 到定理的路径存在：**CDL（Hu&Wu，FOCS 2024）**——校准决策损失
  对全部有界决策任务的最大可改进量；**Chow 规则**——c(x)=P(correct|x) 校准 ⟹ 按 c 排序/门限
  是风险-覆盖 Bayes 最优；Confidence Gate Theorem——选择精度单调 ⟺ 无反转区。
  组合起来即"**miscalibration ⇒ 选择次优有界**"的形式化骨架（注意 §5 PARTIAL 修正：现成文献
  没有直接的"错校准⇒排序次优"定理，需要我们自己组装——这正是空白）。
- RLHF/推理模型系统性过自信（verbalized confidence 聚 0.8–1.0，知识密集任务 ECE~0.30）——
  τ 大的经验事实在文献里是稳固的（归属修正见 §5）。

**D5 多系统去相关 / δ_corr（25 claims）**
- ★ 单 frozen 模型自我验证塌缩（Stechly/Kambhampati：GPT-4 自批评性能崩、外部 sound verifier
  恢复）+ **信息论上限：生成器-评估器错误相关时自评几乎不提供正确性证据**（迭代自批评放大置信
  不加信息）——E10/E10b 实测的文献同侪。
- ★ **Sharpening（Huang et al.）**：自改进可行 ⟺ 判别能力严格超过生成能力（正生成-验证 gap）
  ——两系统方案的正半条件（§5 修正：精确形式是"gap>0 时可证有效"而非"仅当"）。
- ★ Weak-verifier 聚合达近 oracle 的显式前件 = **条件独立**（Weaver）；ensemble 的
  bias-variance-**diversity** 精确分解（Bregman 族）——δ_corr 作约束项的两个数学母体。
- 生成-验证 gap 随生成器变强而**缩小**（强生成器产出更难检出的错误）——δ_corr 不是静态常数。

**D6 ICL 可达性 / R（30 claims）**
- ★ few-shot 的"能改什么"边界文献充分：任务识别 vs 任务学习二分（识别不随 shot 数涨）；
  gold 标签基本不必要（Min et al.）；**翻转标签覆盖先验是规模涌现能力**；**few-shot 覆盖
  预训练偏置无效、many-shot（数百-数千）有效**（Agarwal 2024）——R 是 shot 数的增函数且有
  低 shot 平台，与我们 Reachability.lean 上限定理同向且给出增长形。
- ★ ICL-as-implicit-Bayes（Xie et al.）+ PAC-ICL（Wies et al.）——R 的形式化母体（先验支撑
  内可识别 ⟹ 可达）。
- ★ **delivery-form 作为新约束项候选**：finder 提出 delivery_form_reach_monotonicity 定理候选
  （flat vs 多轮/工具递送的 reach 单调性）——与 T10 经验发现（2-turn 递送使采纳 0.175→0.35）
  互为表里。softmax bottleneck 结构性 floor——上下文无关的不可达域。

## 2. 27 个定理目标候选 × 约束项（全列，不排序；旗舰标注为 finder 自评）

| 约束项 | 定理候选（出处维度） |
|---|---|
| **τ\***（门控半径） | T-A oracle 半径门逐点支配（D1）；**T-B 门限门 Bayes 最优 + 支配 Always/Never——证 TARG 之假设**（D1）；T-C 有限库估计误差 floor（D1）；T-D 频率条件化门（D1）；Gated-injection radius τ*（D2）；Sufficiency-gated abstention conformal 收敛（D2） |
| **N\***（预算上限） | **Finite-outcome BoN KL 界——清欠 Beirami sorry**（D3）；内点最优 N* 存在性/单峰（D3）；**BoN 过优化预算上限 under 有界奖励估计误差（D5，独立成条，与 D3 内点最优同锚 2506.19248）**；BoN Over-Selection Cap（D4）；N* for reward-guided KB selection（D2）；重尾灾难负半强化（D3） |
| **δ_corr**（去相关） | **δ_corr error-floor dichotomy（D5 旗舰）**；Two-system decorrelation lifts selection floor（D3 旗舰）；Two-System Decorrelation Floor（D4，弱先例版）；Generation-verification gap gate（D5）；Debate honest-win under stability（D5，自评 STRETCH） |
| **τ**（估计误差） | Noisy-Selector Argmax Preservation（D4）；Calibration⇔Selection Optimality——over-confidence 定理化（D4）；T-E 奖励引导门收敛到 τ*（D1） |
| **R**（可达界） | reach_budget_from_bounded_evidence——R(k) 接地（D6）；**reachable_bestofN_converges_with_recall_floor——补 Reachability 缺的收敛半边**（D6）；softmax bottleneck 结构 floor（D6） |
| **α**（采纳） | Confidence-gated arbitration minimax 最优（D2）；（α 函数形先例 = ClashEval 负线性，测量对象） |
| **组合/迭代** | Iterative/agentic RAG 在 KL 信赖域收缩下收敛（D2）；Consensus/MBR recall floor 有限集中（D3） |
| **新约束项候选** | **delivery-form**：delivery_form_reach_monotonicity（D6）——若采纳，台账从 7 项扩为 8 项 |

## 3. 文献空白 = 我们的生态位（六 finder 汇总，全部为"确认不存在"）

1. **任何门控规则的收敛证明不存在**——TARG 假设 τ*、Drozdov/Meta-k/NEST 全是启发式；
   "证明门限门最优并给收敛"是空白正中。
2. **δ_corr 参数化的选择定理不存在**——去相关思想散见（Weaver 条件独立、ensemble diversity
   分解），但没有"以相关系数为显式约束项的两系统选择收敛界"。
3. **(τ 校准误差) × (N* 过选择) × (α 门控采纳) 的统一收敛界不存在**。
4. 校准⇒选择排序最优的直接定理不存在（CDL/Chow/选择性预测是组件，组装是我们的活）。
5. 迭代 agentic RAG 的收敛性只有 KL 信赖域候选形，无成品。
6. speech/audio 域上述全部空白平方级放大（理论文献几乎全在 text）。

## 4. 与既有 Lean 台账的接口（战役 P4 工作单的文献锚）

- **Beirami sorry（BestOfN.lean:90）**：Theorem 3.1 原文已核（上界+奖励唯一性前件）→ 按原文
  证明或钉为显式引用假设，两条路都有据。
- **τ→0 假设病根**：D1 T-C/T-E + D2 τ* 定理候选给出"τ*>0 邻域"的正确形式——不再假设消失，
  改证"门控下收敛到 oracle−f(τ*) 邻域"。
- **over-confidence docstring → 定理**：CDL + Chow + Confidence-Gate 三组件组装（D4）。
- **Reachability.lean 上限定理的收敛半边**：reachable_bestofN_converges_with_recall_floor（D6）。
- **`gain_le_of_hoeffding`/`regret_O_sqrt_log` 前件假设**：Soft-BoN O(1/n) 显式常数收敛（D3）
  提供可消化的替代形式。

## 5. 对抗验证 PARTIAL 修正（8/24，引用时必须用修正版）

1. Long-Tail Crisis：">90% 邻居污染"数字过强——原文为最近邻多数不含目标 token（方向成立）。
2. "Why kNN-LM works" 作者归属：Xu/Alon/Neubig（非 Khandelwal/Jurafsky）。
3. **"错校准⇒选择排序次优"无现成定理**——headline 撤回，改为组件组装目标（正中空白 §3.4）。
4. Reward-hacking 定理前件是 **strict TP2**（严格 MLR），非无条件"严格增"。
5. UQ survey（2503.15850）是方法学综述，具体数字（ECE~0.30 等）须溯源到其引用的原始实验文献。
6. Sharpening 精确形式："正生成-验证 gap 时可证有效"，非"仅当"（必要性未证）。
7. 生成-验证 gap 论文：强生成器⇒TNR 急降/TPR 稳（方向确认，表述微调）。
8. 相关错误自评：精确表述为"相关时自评仅提供弱/有界证据"（非零证据）。

## 6. 状态与下一步

覆盖三路（模型/数据/理论）之理论路完成。全部 27 候选进收敛门材料；门后按 owner 裁定冻结
Lean 工作单（战役 P4）并与数据轨测量落点（P5）双向绑定。**本文不做选型。**
