# Stage-1B 定向锚点论文扫描 RC1

状态：`UNSIGNED_STAGE1B_OVERLAY_AWAITING_INDEPENDENT_REVIEW`

本工作台落实 owner 指令“先进行详细的论文扫描，并且填充到 Stage‑1B 中，之后再进行分析”。
它是一个独立的 Stage‑1B 派生证据层，不重写已冻结的 Stage‑1B v5，也不修改已经完成博士生导师评审的
capability-delta RC1 字节。

## 结果摘要

- 全文扫描 26 篇；24 篇通过定向纳入门，2 篇保留为 `SCANNED_NOT_PROMOTED`。
- 每篇扫描对象均绑定 arXiv PDF、e-print 和版面文本，共 78 个外部文件；PDF/e-print 的 52 个
  rendition 同时与全局 full-text ledger 对账。
- 24 个纳入记录分别编码问题轴、干预轴、知识/技能/记忆/系统/控制主方向、MM0-MM3 证据级别、
  论文实验设置、可借鉴内容、最强边界或反证以及精确全文 locator。
- `REFERENCE_CONTEXT`、`BORROWED_PROTOCOL_ANALOGUE` 与 `REPRODUCTION_ANCHOR` 被严格分开。
  本次没有任何工作满足已闭合复现锚点；复现锚点数为 0。
- 计数保持三层可辨：CURRENT 继承并集 282；本定向增量独立叠加为 306；与未签名的 14 篇
  capability delta 合并后是 320 个候选身份。320 不是签名 release，也不是 Stage‑1C 输入分母。

## 阅读入口

1. [`targeted-anchor-scan-contract.md`](targeted-anchor-scan-contract.md)：扫描、纳入、证据和权限合同；
2. [`targeted-anchor-map.md`](targeted-anchor-map.md)：24 篇纳入工作与 2 篇未纳入工作的中文事实地图；
3. [`targeted-anchor-scan-records-v1.json`](targeted-anchor-scan-records-v1.json)：逐篇机器可读记录；
4. [`review-package-manifest.json`](review-package-manifest.json)：RC1 文件、字节数与 SHA-256；
5. `docs/checks/stage1b-targeted-anchor-scan/2026-07-24-rc1/`：外部全文绑定、canonical census
   和合同检查结果；
6. `wiki/survey/registry/stage1b-targeted-anchor-scan-2026-07-24-papers.jsonl`：24 条长期 registry
   派生记录。

## 本次实际做了什么

- 从语音/omni 的多轮对话、主动感知、奖励与解码出发，补查视觉多模态智能体和文本智能体中的
  知识、技能、记忆、test-time control 和系统实验协议；
- 读取论文全文，而不是用标题、摘要或搜索片段作承重证据；
- 对 Audio MultiChallenge、VISUALSKILL、Temporal Contrastive Decoding 和
  Utility-Oriented Visual Evidence Selection 的关键表格/arm/access 信息进行了 PDF 页面视觉复核；
- 只登记论文报告的实验事实与项目可用关系，不聚合跨论文分数，不判断项目 novelty，不选择研究方向。

## 未完成与待授权事项

本 RC 请求独立 verdict：`SIGN_STAGE1B_TARGETED_ANCHOR_SCAN_RELEASE`。该 token 尚未签发。

在签名之前，24 条记录不得进入 Stage‑1C 承重输入。即使以后签名，也仍需单独完成数据、代码、
loader、评价器、许可、版本和 access closure，才能把某个 `reproduction_candidate_status` 升级为
真正的 reproduction anchor。研究方向分析、实验 family/branch 形成、模型或 benchmark 执行继续暂停。
