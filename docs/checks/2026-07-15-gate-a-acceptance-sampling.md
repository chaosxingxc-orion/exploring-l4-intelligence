# Gate-A 独立抽样验收报告

> **归档事故重建注（2026-07-15）**：本文件首次提交（b1af8c6）时因任务输出文件被系统回收而为
> 0 字节空文件——commit 信息先于证据字节存在，属「提交信息不实」类事故，协调者据会话内代理返回
> 全文重建于此并如实登记。重建内容与 b1af8c6 提交信息所引结论一致；reviewer 可要求重跑抽样以
> 消除重建环节（抽样规则确定性：paper_works.jsonl 0-based 行 3,12,21,30,39,48,57,66,75,84）。

**抽样评审员立场**：未参与生成这些工件的独立代理，只读核验；census 字段以 arXiv abs 页 /
ACL Anthology / WebSearch 实时网络返回为准。

## 层一 — 10 篇 census 抽样（行 3,12,21,30,39,48,57,66,75,84 = W-0004/13/22/31/40/49/58/67/76/85）

| Work | ID | 结论 | 依据摘要 |
|---|---|---|---|
| W-0004 | 2503.22712 | CONFIRMED | 题名、4 作者（Zijun Jia/Jinsong Yu/Hongyu Long/Diyin Tang）、2025、v4=2025-05-07 全对 |
| W-0013 | 1805.04604 | CONFIRMED | Confidence Modeling for Neural Semantic Parsing、Dong/Quirk/Lapata、v1=2018-05-11 |
| W-0022 | 2205.00978 | CONFIRMED | 7 作者含带音标名、v1=2022-05-02 |
| W-0031 | 2603.19615 | CONFIRMED | CAF-Score、Insung Lee 等 5 人、v1=2026-03-20（本轮 WebFetch 实取确认） |
| W-0040 | 2603.12520 | CONFIRMED | 单作者 Eddie Landesberg、v1=2026-03-12 |
| W-0049 | 2510.02611 | CONFIRMED | Wu/Mirhoseini/Tambe、v1=2025-10-02 |
| W-0058 | 2020.acl-main.503 | CONFIRMED | Kamath/Jia/Liang、ACL 2020、venue-native id + DOI 正确 |
| W-0067 | 2601.18510 | CONFIRMED | Just-In-Time RL、8 作者、v3=2026-06-08 |
| W-0076 | 2606.04680 | CONFIRMED | Read What You Hear、6 作者、v1=2026-06-03 |
| W-0085 | 2606.04730 | CONFIRMED | KIT IWSLT 2026、8 作者（Ugan…Waibel）、v1=2026-06-03 |

**层一：10/10 CONFIRMED，受核 5 字段零错误。** 两点非受核字段旁注（不触发扩检）：W-0058 notes
「no arXiv preprint」不完整（实存 arXiv 2006.09462，canonical_id 本身正确）；W-0067 venue
「ICML 2026 (Spotlight)」在 abs 页无佐证来源。

## 层二 — 全部 17 条 MATERIAL/CRITICAL（15 MATERIAL + 2 CRITICAL，数量与预期一致）

逐条核验内部自洽性并复算算术：CL2-0001/0002/0008/0009/0010/0011/0014/0015/0016/0018/0021/
0034/0058/0059/0061 = **COHERENT**（含 ρ=0.009/0.029=31%、14.29/27.04=52.8%、33.5%/38.4%/7.7%
WERR 等复算通过）。两条 CRITICAL 对论文方向核验：

- **CL2-0060 / ProGRes 2409.00217**：WebFetch 确认摘要原文 "dynamically expand the n-best…
  with new hypotheses generated"、purely zero-shot、WER 5–25% → 确为 candidate-expansion（池外），
  推翻 kill-I1 DIRECT 池内占位标签的纠正方向 **RIGHT**。
- **CL2-0062 / TAP-GER 2309.15649**：确认摘要 "achieve error rates below the N-best oracle level"、
  生成式纠错产新文本 → 确为池外生成，纠正方向 **RIGHT**（载荷数字 8.72/9.78/8.41/29.56/11.87
  内部一致；表内值本轮经摘要佐证方向，未再全文重取）。

**层二：17/17 COHERENT，2/2 CRITICAL 方向 RIGHT，无 DEFECT。**

## 层三 — 全部 ABSTRACT_ONLY/UNREACHABLE 且 KILL/OCCUPANCY 的承重行（7 行）

CL2-0009（80%=置信度下修纠正）、CL2-0010（收窄为 rho_pool 并自陈仅摘要级）、CL2-0021（限定
训练模型、非 frozen-omni）、CL2-0025（Reflexion 仅文本域机制占据）、CL2-0026（Training-Free
GRPO 同）、CL2-0027（限定 text-agentic）、CL2-0029（谨慎区分 SYSTEM 占据 vs selection OBJECT）
——**7/7 verdict 均未超出摘要可支撑范围，无 DEFECT。**

## 总裁定

三层各自零同类错误 → 无需强制全层扩检。**ACCEPTANCE_PASS**。
需扩展全层复检的层：无。发现的受核字段错误：无（仅上列两处非受核字段小瑕疵供修订参考）。
