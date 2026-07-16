---
title: "Gate S1 Correction #4：Stage-1A survey 执行前博士生导师式对抗复审"
date: 2026-07-16
review_role: "严格外部审稿人 / 博士生导师"
review_stage: "Stage-1A 内部的 survey-ready gate；首条系统检索执行之前"
review_target: "wiki/survey/2026-07-16-gate-s1-correction-4-response.md"
target_commit: "5cde3e36ddaf178f7e115ca5fbec7d27a69ce01c"
target_git_blob: "300225e906b531e1488ac57f518ac6b8363497d4"
target_worktree_sha256: "E0DF79B3E2607D499D3630A1DC8CCF8AA238BFCA5F21BC9FAECA1DC93792AD46"
verdict: "WITHHOLD SIGNATURE — CORRECTION #4A / PRE-LAUNCH INTEGRATION FIX REQUIRED"
integrity_verdict: "FFP NOT ESTABLISHED；MATERIAL QRP REMAINS"
---

# Gate S1 Correction #4：Stage-1A survey 执行前博士生导师式对抗复审

## 0. 一页裁决

**总裁决：暂不签署 search-design gate，不允许执行首条系统检索查询。**

Correction #4 不是无效工作。相反，团队已经完成若干可核验的实质整改：50 条 route 已逐行机器化，
87 条 seed 与 53 条 query 的计数可重数，25 件 correction bundle 在冻结提交上 25/25 完整，四个现有
重放程序在项目规定的 WSL2 / Python 3.12 环境中均成功并与冻结输出逐字节一致。这些应被明确承认。

但是，当前回复把“局部脚本可以重复产生同一输出”上升成“全部 P0 闭合、双合同全绿、可以签署”，
证据并不支持。至少仍有五个会直接影响 survey 可执行性或审计真实性的阻断项：

1. 签署协议和 README 仍同时保留 74/87、REC-1..REC-7/REC-0..REC-7、amendments 1–3/1–4、
   51/53 等互相冲突口径；签署包本身没有形成单一可执行合同。
2. child-query splitter 不能读取真实冻结 query 行，并且声称 `YEAR→MONTH→DAY`，实现却从 ROOT
   直接拆 MONTH；9/9 PASS 只证明一个人为构造的三个月样例自洽。
3. amendment-4 承诺的 REC-0/REC-2/D2 validator 不存在；目前只有模板和三条合成示例，无法强制
   “承重 claim 必须回指 D2”、NA 类型、纳排理由、双人 threat 编码等合同。
4. route validator 只查结构不查事实；`SF-T1R-ACL-2026` 在 2026-07-16 仍被标成
   `NOT_YET_PUBLISHED`，但 ACL 2026 已于 7 月 2–7 日举行且 ACL Anthology 已发布 2026 卷。
5. sentinel test 把任意自由文本解释都当作 `EXPLAINED_MISS`，因此不可证伪；同时 query 类目仍没有
   `cs.MM` 和 `cs.MA`，已存在与 omni agentic system 高度相邻而会从该缝隙漏掉的论文。

**诚信裁决：没有证据足以认定 fabrication、falsification 或 plagiarism，也没有发现偷偷运行模型
实验的证据；因此不得指控“学术欺诈已成立”。** 但 G3 的历史完成态夸张已由团队自己承认，本次又
出现“全部绿灯”与实际工件不一致、联网访问总量表述不完整、已知文献从旧日志向新 seed 丢失等问题，
构成应被正式记录的 material questionable research practices（QRP）。如果在收到本报告后仍用同一
口径申请签署，性质将从疏漏升级为明知证据不足仍作完成态陈述。

## 1. 阶段校准：不是“Stage-1A 尚未开始”

本复审采用仓内正典阶段定义：当前是 **Stage-1A 收官准备末段的 survey-ready gate**。问题界定、
检索协议、seed/query/route 冻结、记录合同和签署准备，本身都属于 Stage-1A 工作；尚未正式开始的是
Stage-1A 的系统 mapping 执行，而不是 Stage-1A 整体。

因此本报告只审查：

- survey 是否能按同一合同开始并回放；
- 检索宇宙是否存在已知、可修复的结构性盲区；
- screening/coding/claim lineage 是否已有最低可执行约束；
- 回复中的完成态和诚信陈述是否与证据相符。

本报告**不要求**：模型调用、benchmark 结果、selector/evaluator 对比、预算 cap、SESOI 冻结、
Stage-2 因果验证或论文级结果。任何模型触碰仍应等到 Stage-1B 获得明确放行。修复本报告列出的
survey 工件不构成 Stage-1B 实验。

## 2. 审查方法、冻结证据与三轮对抗复核

### 2.1 冻结对象

- 审查时 HEAD：`5cde3e36ddaf178f7e115ca5fbec7d27a69ce01c`。
- 目标回复 git blob：`300225e906b531e1488ac57f518ac6b8363497d4`。
- 目标回复工作树 SHA-256：
  `E0DF79B3E2607D499D3630A1DC8CCF8AA238BFCA5F21BC9FAECA1DC93792AD46`。
- correction #4 实质工件提交：`f3ab138`；bundle manifest 固定提交：`5cde3e3`。
- 独立重数：87 seed / 87 唯一，53 query / 53 唯一，50 route / 50 唯一，14 sentinel。
- bundle 独立核验：25/25 `PASS_AND_UNCHANGED`。

### 2.2 对抗轮次

| 轮次 | 主要问题 | 结论 |
|---|---|---|
| A：claim–artifact 对照 | 每一个“已修复/全绿”是否有持久工件与正确口径 | 发现协议、README、sentinel 报告仍有陈旧正典，REC validator 缺失 |
| B：replay + integration | 工件是否只在合成样例中通过，真实冻结输入能否接入 | 四个既有 replay 可逐字节复现；child splitter 对真实行 `KeyError: query_sha256`，且 YEAR 层未实现 |
| C：coverage + integrity | 检索宇宙、引用依据、事实状态和诚信口径是否经得起外部核验 | 发现 cs.MM/cs.MA 盲区、直接近邻遗漏、ACL 2026 状态错误、联网访问总量少报 |

三轮均产生新发现，故团队所称“语义敌意复审零残留”不能作为外部签署依据。本审查也不冒充三名
独立人类审稿人；它是同一外部审查者用三组相互对抗的验收目标完成的复核。

### 2.3 WSL2 故障与重放环境

初次重放被 `Wsl/Service/CreateInstance/MountDisk/HCS/E_ACCESSDENIED` 阻断。诊断确认 VHD 存在、
D: 为健康 NTFS、文件可由当前用户读写、Defender Controlled Folder Access 关闭；但 VHD owner 为
`BUILTIN\Administrators`，当前未提升用户无法更新安全描述符。把
`D:\wsl\Ubuntu-24.04\ext4.vhdx` owner 恢复为发行版所属用户 `CHAO\35686` 后，WSL 启动时成功自动
加入新的 `NT VIRTUAL MACHINE\<GUID>` ACE，直接验证了根因链。

修复后环境核验：Ubuntu 24.04、Linux 6.6.87.2 WSL2、root ext4 `rw`、系统与 speechrl venv 均为
Python 3.12.3、RTX 5090 可见、D:/E: 工作与数据挂载均正常。随后在 `f3ab138` 的临时 git archive
中使用 `~/.venvs/speechrl` 重放，未改团队工作树：

- route validator：PASS，输出 byte-identical；
- child replay：PASS，输出 byte-identical；
- query compiler：PASS，53 行输出 byte-identical；
- sentinel replay：PASS，输出 byte-identical。

这组结果证明“冻结程序是确定性的”，但不证明其语义合同正确、真实输入能接上、route 外部事实正确，
也不证明 sentinel 具有有效召回诊断能力。

## 3. 对 Correction #4 六项整改的逐项裁决

| 项目 | 团队完成态 | 外部裁决 | 理由 |
|---|---|---|---|
| C4-1 / 历史失配更正 | 已闭合 | **基本通过，附诚信保留** | 能区分 G3 完成态夸张与其余设计深化是合理的；但当前“全部绿灯”再次超出证据 |
| C4-2 / venue tier 与质量 | 已闭合 | **设计方向通过，执行合同未闭合** | venue tier 零证据权重、七维质量评价合理；Decision-Log supersession 自相矛盾且无 validator |
| C4-3 / 50 routes | 12/12 PASS | **结构通过，事实状态未通过** | 50 行和枚举可重放；ACL 2026 status 已被官方页面反证，validator 只做静态结构检查 |
| C4-4 / REC-0 lineage | 已闭合 | **不通过** | REC-0 模板与三条 synthetic case 已落盘，但 promised validator 不存在，无法强制 lineage |
| C4-5 / child query replay | 9/9 PASS | **不通过** | synthetic determinism 成立；真实 frozen row 无 `query_sha256`，并且缺 YEAR splitter |
| C4-6 / 类目盲区与 sentinel | 已闭合 | **部分通过** | cs.SE/cs.HC 补洞有效；测试不可证伪、输入计数仍写 51，cs.MM/cs.MA 仍漏 |

### 3.1 C4-1：更正值得接受，但不能用“唯一一次夸张”提前封案

回复明确收回了此前关于 50 route 已逐条实例化和机器验证的错误完成态，这是必要且正确的科研记录
动作。把 G2 的政策偏离、G4/G6 的深度不足和 G3 的完成态夸张区分开，也比把所有问题统称“造假”
更严谨。

问题在于回复第 70–78 行再次把多项尚无可执行证据的事项全部标成 ✅。因此“G3 是本轮唯一完成态
夸张”只能描述此前轮次，不能描述当前 correction #4 的自评。外部裁决必须以本次实际证据重新计算。

### 3.2 C4-2：方法方向正确，但引用和正典需纠正

将 `venue_tier` 降为发现排序元数据、让承重性由工作级质量和 claim locator 决定，是正确改进。
对于 Stage-1A 的 systematic mapping，也不应机械要求所有 INCLUDED 论文都完成论文级风险偏倚
评估：systematic map 的首要目的在于结构化研究区，而 systematic review 更强调证据综合与强度。
[Petersen 等人的 mapping guidelines](https://www.sciencedirect.com/science/article/abs/pii/S0950584915000646)
明确区分了两者目标。

但 amendment-4 §2 第 46 行把“PRISMA 系质量评估惯例”当成 `code-on-use` 的方法学依据并不严谨。
PRISMA 2020 首先是**报告规范**，不是替代 review 方法学或决定质量评估对象的规则；
[PRISMA 2020 官方说明](https://www.prisma-statement.org/prisma-2020)提供 checklist 与 flow diagram，
[PRISMA-S](https://link.springer.com/article/10.1186/s13643-020-01542-z)要求把检索组件完整报告到可复现，
而 systematic map 的筛选—编码—评估流更适合参考
[ROSES map flow](https://www.roses-reporting.com/flow-diagram)。建议把依据改写为“本项目为 mapping，D1
负责分类，D2 负责所有承重与 direct-threat 工作；PRISMA-S/ROSES 仅约束透明报告与 flow”。

另有正典冲突：Decision-Log 续61 Decision 称 `T2_UNREVIEWED` 退役、venue tier 零证据权重；同一
条目的 Supersedes 又称 `T1_DEMOTED/T2_PROMOTED` 继续有效，而 README/amendment 又称相关 override
机制退役。必须新增 dated supersession，说明这些字段究竟是“历史审计标签”还是“仍影响证据权重”；
不得让同一标签同时承担两个语义。

### 3.3 C4-3：route 数据结构有明显进步，但结构 PASS 不能替代事实核验

独立确认：50 route ID 唯一；状态分布为 41 READY、6 NOT_YET_PUBLISHED、3 NOT_HELD；35 条 exact
URL、12 条 ENTRY_TO_RESOLVE、3 条 N/A；12 项静态 validator 可逐字节重放。

然而 `SF-T1R-ACL-2026` 的 `status_basis` 仍称“会期 2026-07/08 未到”。官方
[ACL 2026 program](https://2026.aclweb.org/program/)列出的主会日期为 7 月 5–7 日，且
[ACL Anthology 的 2026 venue 页](https://aclanthology.org/venues/acl/)已经列出 ACL 2026 六个 volume。
所以在冻结日 7 月 16 日，`NOT_YET_PUBLISHED` 是错误事实。该错误并未使 JSON schema 失效，却证明
12/12 PASS 仅是结构性检查，不是 route readiness 证明。

类似地，ICML 2025 仍为 `ENTRY_TO_RESOLVE`，但官方
[PMLR volume 267](https://proceedings.mlr.press/v267/)已有确定入口。这项可在 P0-R8 首次联网状态门
中解析，不必因此重做整个 route 设计；但签署前必须让 frozen status 与复核时点一致。

### 3.4 C4-4：REC-0 是正确方向，但“模板存在”不等于“lineage 可执行”

`2026-07-15-sf-blank-templates.md` 已新增 REC-0，并覆盖 source hits、dedup、screening stage、decision、
reason、人员、版本和 REC-2 back-reference。三条 synthetic case 也覆盖了双源合并、摘要排除和全文
不可得。这些设计本身值得保留。

阻断点是 amendment-4 §2 明确承诺 validator 会强制：

- 承重 claim 只能回指 `coding_depth:"D2"` 的 REC-2 行；
- NA 必须携带理由；
- 不能无痕留空。

仓内 `scripts/survey/` 只有 query、route、child 和 sentinel 五个脚本，没有 record/ledger validator、
JSON Schema 或 negative fixtures。当前没有任何机器约束可阻止 INCLUDED 行缺 REC-2、DIRECT_THREAT
停在 D1、claim 回指 D0、重复 canonical_id、枚举漂移或空字符串。

此外，D1 允许把本应为 object 的整个 block 直接替换成字符串 `"NA:<理由>"`，造成同字段异类型；
REC-0 模板把 `reason_code` 写成必选字符串模板，合成 INCLUDED case 却使用 `null`。这些都说明目前是
可读草案，不是机器合同。建议使用类型稳定的对象，例如 `{"status":"NA","reason":"..."}`，并用
schema/validator 固定 included/excluded 的条件必填规则。

### 3.5 C4-5：9/9 PASS 只覆盖了自造输入，没有覆盖真实接口

`sf_child_query_split.py` 第 6 行宣称超过 2000 时按 `YEAR→MONTH→DAY` 拆分；第 116 行实际执行
`ROOT/YEAR→MONTH`、`MONTH→DAY`，仓内没有 `_year_windows`。冻结查询跨 2022–2026，真实 root overflow
的第一步会直接产生几十个月份，而不是协议所称的年度层。

更严重的是 `_child_record` 和 root builder 都强取 `parent["query_sha256"]`，而 53 条 frozen query
只有 `record_sha256`。将第一条真实 JSONL 行传给 splitter 会得到 `KeyError: 'query_sha256'`。仓内也
没有 executor/adapter 把 compiler 输出转为 splitter 输入。

现有 test 自造了一个含 `query_sha256`、只跨 2024-01 至 2024-03 的 parent，所以既不会发现真实 schema
不匹配，也无法发现 YEAR 层缺失。它确实证明同样 synthetic parent + oracle 会产生同样 bytes，但不能
支持“执行器必须调用、派生查询已可精确重放”的完成态。

### 3.6 C4-6：已补一个真实盲区，但 sentinel 判据不能衡量 recall

SF-L10 加入 cs.SE/cs.HC，能够恢复主类目只有 cs.SE 的 AgentEval，这项修复有针对性。14 个已知 ID
的存在性核验也都可由日志追踪。

但现有 sentinel gate 是“每篇必须 HIT 或有 explanation”；`EXPLAINED_MISS` 只需自由文本说明，任何
漏检都能事后解释为合理，因此测试理论上几乎不会失败。更合理的结果域应为：

- `QUERY_HIT`：冻结 query 的词项与类目确定命中；
- `SEED_GUARANTEED`：不依赖 query，由 manifest 精确 ID 保底；
- `EXACT_ROUTE_GUARANTEED`：由明确 venue route 保底；
- `UNRESOLVED_MISS`：以上均不成立，必须触发设计修订或接受并登记覆盖边界。

此外脚本和报告仍写“51 rows, frozen”，实际为 53。当前 query 类目集合只有 cs.AI、cs.CL、cs.CV、
cs.HC、cs.LG、cs.RO、cs.SD、cs.SE、eess.AS，缺少直接相关的 cs.MM 与 cs.MA。不是要求无边界地增加
所有 arXiv 类目，而是要求对已经观察到的反例作受控补救。

## 4. 文献与引用审计

### 4.1 已纳入引用的总体评价

Correction #4 针对上一轮点名的 14 个 arXiv ID 做 known-ID dereference，日志中的最终题名、类目和
存在性与原始页面一致；包括此前待核的 VideoAgent。该动作是存在性/元数据核验，不是执行预注册
discovery query，也不构成 Stage-1B 实验。

但“ID 都存在”只解决 citation hallucination，不解决 coverage。以下遗漏不要求团队立刻写结论，
而是要求在首条系统检索前把已知的直接威胁/边界案例放入 seed 或 held-out sentinel，避免明知遗漏后
仍宣称检索设计可签署。

### 4.2 P0：签署前必须进入 seed / threat queue 的直接近邻

1. **Agentic Monte Carlo: Simulating Reinforcement Learning for Black-Box Agents**
   ([arXiv:2606.05296](https://arxiv.org/abs/2606.05296))。它把固定黑盒 LLM agent 作为 trajectory prior，
   用 SMC 在 test time 采样并报告超过 prompting 与 GRPO；标题和问题身份都直接威胁项目北极星。
   但其 value function 是学习得到的，必须分别编码“核心冻结”与“外部组件训练”，不能粗暴归入 TFStrict。
2. **Training-Free Test-Time Contrastive Learning for LLMs**
   ([arXiv:2604.13552](https://arxiv.org/abs/2604.13552))。冻结 LLM、Explore–Reflect–Steer、多代理轨迹、
   跨实例文本规则存储，直接覆盖 external control plane 与 persistence。更严重的是该 ID 已在
   `2026-07-14-search-query-log.jsonl` 第 241 行被团队发现，却没有进入当前 87 seed；这是知识组织/转录
   失败，不是外部搜索未发现。
3. **Test-Time Learning with an Evolving Library (EvoLib)**
   ([arXiv:2605.14477](https://arxiv.org/abs/2605.14477))。不更新参数、不用外部监督、跨实例维护技能和
   reflective insight library，直接挑战 persistence、memory/skill update 与“训练”边界。
4. **Mapping Smarter, Not Harder**
   ([arXiv:2510.14900](https://arxiv.org/abs/2510.14900))。自称无标签、无模型更新的 test-time RL，却在
   推理时发 targeted web search 获取新证据；这是 `read-out` 与 `new-info` 信息边界的理想反例，必须
   作为边界论文编码，不能只按作者标题归为同类。
5. **MAR3** ([arXiv:2603.27706](https://arxiv.org/abs/2603.27706))。training-free、多 agent、audio-visual
   recognition/reasoning/reflection，主类目仅 cs.MM，且已接收 ACM MM 2026。它既是 omni component
   近邻，也是当前类目盲区的确定反例。

### 4.3 P1：执行早期优先精读，不作为无限扩张签署包的理由

- **Useful Memories Become Faulty When Continuously Updated by LLMs**
  ([arXiv:2605.12978](https://arxiv.org/abs/2605.12978))：连续 consolidation 可使性能跌破 no-memory，
  是停止规则、负结果和可回滚 memory 的关键安全证据。
- **VQQA** ([arXiv:2603.12310](https://arxiv.org/abs/2603.12310))：黑盒自然语言接口、多代理 VLM critique
  作为 semantic gradients、闭环 prompt optimization，并带 cs.MA；是 multimodal external control
  plane 的直接组件近邻。

上述列表是本轮已查明的有限修订集，不是要求团队在签署前穷尽未来所有论文。修复后仍可按协议执行
snowballing 和版本化增补；Stage-1A 的价值就是先建立可追溯的广覆盖，而不是提前用预算 cap 强制收敛。

## 5. 诚信与疑似学术欺诈审计

### 5.1 没有被证实的事项

- 未发现伪造论文、伪造 route 行数、篡改重放输出或捏造 bundle hash。
- 87/53/50/14 数字均可从机器工件重数，25 件 bundle 可按 manifest 复核。
- 未发现 2026-07-16 前后运行模型、benchmark 或 Stage-1B 原型实验的证据。
- W1/W4 子仓干净且最近提交早于本次 gate；W2/W3 的工作树变化只是把 `~/...` 改为
  `${oc.env:HOME}/...` 的配置路径卫生，不是实验结果。

因此本报告不建议启动 fabrication/falsification/plagiarism 调查，也不应对个人作“造假者”定性。

### 5.2 已成立或仍存在的 QRP

1. **历史完成态夸张：已成立并已承认。** G3 过去把范围模板称作 50 条逐条 route 与机器验证。
2. **当前 premature closure：仍存在。** C4-4/C4-5/C4-6 未达到自称验收条件却全部标绿。
3. **claim–evidence mismatch：仍存在。** 合成 replay PASS 被表述成真实执行链闭合；结构 validator
   PASS 被表述成 route readiness。
4. **provenance 不完整：仍存在。** 回复 frontmatter 称 21 次 ID_DEREFERENCE “逐次留痕”，但 log
   header 明示在 canonical pass 前还有约 25 次同类访问未逐次记录。准确口径应是“21 次 canonical
   logged access + 约 25 次先前聚合披露；discovery query=0”，总访问约 46，而不是 21。
5. **知识转录失败：成立。** TF-TTCL 已在旧 search log 被发现，却从新 seed/census 消失；说明“读过
   即登记、提炼入正典”的组织链尚未可靠运行。

“联网检索查询执行数=0”在窄义 discovery-query 口径下仍然成立；known-ID dereference 不应被伪装成
零网络活动，也不应被错误升级成已执行 survey query。应同时报告两种计数，消除语义套利空间。

### 5.3 复发后的升级条件

本轮仍按“可整改 QRP”处理。若团队在收到明确反例、schema mismatch 和 validator 缺失证据后，仍在
下一份回复中声称这些项目“全部闭合/零残留”而不更正，则应升级为 formal research-integrity concern，
要求独立人员重放与 owner 书面确认。升级依据是明知后的重复失实陈述，而不是当前代码 bug 本身。

## 6. 是否超越 Stage-1A 范畴

**没有发现实质 Stage-1B 越界。** 当前新增工件是 query/seed/route/schema/replay 与文献核验，均属于
Stage-1A survey 方法准备。known-ID 页面访问、离线 compiler/replay、修复 WSL2 也不是模型实验。

需要继续禁止的超前动作：

- 未签署前执行 53 条 discovery query 或 T1 venue scan；
- 未获 Stage-1B release 前触碰模型、跑数据集、报告模型效果或选择器收益；
- 在 Stage-1A 把某个 controller、memory 或 multi-agent 机制写成已确定技术路线；
- 提前设置第三阶段资源压降用的预算 cap，反过来限制当前广度探索。

允许且应继续做的工作：修复 survey 合同、补直接 seed、做离线 schema/negative fixture、准备配置化
实验接口的**规范**（dataset/model/inference/evaluator 作为可配置抽象），但不实际发起模型推理。

## 7. Correction #4A：最小、严格、可验收的整改计划

以下均为首条 survey 查询前的 P0；不是新研究 proposal，也不是要求完成论文。

### P0-R1：把签署对象统一成一个正典合同

修订或以 dated amendment 明确 supersede：

- protocol title、§3、§6、§12；
- survey README 的模板编号说明；
- sentinel script/report 的 51-row 字符串；
- 签署包 manifest 与 bundle hash。

统一口径必须是：87 seeds、53 queries、50 machine routes、REC-0..REC-7、amendments 1–4、machine JSONL
route + validator，而不是旧的 74 / REC-1..REC-7 / amendments 1–3 / routes.md。历史数字可保留在明确标注
`HISTORICAL_SUPERSEDED` 的审计段，不得继续出现在当前签署清单。

**验收：**一条脚本从 machine artifacts 重数并生成 package summary；对 active-signature sections 做
stale-token scan，旧口径零命中；新 bundle manifest 逐件按 git blob 校验。

### P0-R2：修复 child splitter 的真实输入合同

必须二选一并在协议、实现、测试中完全一致：

1. 真正实现 ROOT→YEAR→MONTH→DAY，包括 `_year_windows`；或
2. 明确把协议改为 MONTH→DAY，并说明为什么跨多年 root 直接拆月仍满足 API/恢复约束。

同时让 splitter 直接接受 frozen query row。可在 compiler vNext 增加 `query_sha256`，也可由 adapter 对
`decoded_search_query` 计算并校验；但 `record_sha256` 与 query-string hash 不得混用。补一个不联网的
executor dry-run，读取 `2026-07-15-sf-queries.jsonl` 的真实行并调用同一 normative function。

**负测试必须至少包括：**缺 submittedDate、缺/错 hash、跨 2022–2026 overflow、month overflow、single-day
overflow、闭区间边界、重复 child ID、恢复点续跑。**验收：**真实行不再 KeyError；若保留三层合同，
第一 overflow event 必须是 `SPLIT_YEAR`；两次运行 bytes/hash 一致。

### P0-R3：交付 REC-0/REC-2/claim-lineage validator

新增可执行 schema 与 validator，不得只给 Markdown 示例。至少强制：

- 每个 canonical work 唯一 REC-0；每个 source hit 有可解析回指；
- INCLUDED 必须有 REC-2 backref，EXCLUDED/UNOBTAINABLE 必须有 reason code/text；
- `topic_relevance=core`、`DIRECT_THREAT` 或被任何报告 claim 引用的工作必须 D2；
- D2 必须全字段、七维 study_quality 与 locator；承重 claim 只能回指 D2；
- NA 使用类型稳定结构并有 reason，禁止空字符串伪装完成；
- threat 双人编码和分歧裁决字段满足预注册规则；
- flow 数字从 REC-0 自动导出，不能手填另一套数字。

提供 positive fixtures 和故意破坏的 negative fixtures；负例必须真的使 validator 非零退出。将 validator、
fixtures、固定输出纳入 correction bundle。

### P0-R4：执行 P0-R8 route 状态复核，而不把静态 validator 当联网真值

在签署前逐条 revalidate 50 route 的 status/entry，记录 URL、UTC 时间、HTTP/解析结果和 snapshot/hash。
至少把 ACL 2026 改为 READY；解析已有官方入口的 ICML 2025。结构 validator 与 external-status audit 分开
报告：前者证明 schema，后者证明冻结时点事实。

**验收：**所有 READY/NOT_YET/NOT_HELD 都有当日证据；entry URL 可解析或有明确失败码；状态统计由
manifest 自动生成；差异以 dated amendment supersede，不静默改写历史证据。

### P0-R5：把 sentinel 从“可解释即过”改为可证伪测试

- 使用 `QUERY_HIT / SEED_GUARANTEED / EXACT_ROUTE_GUARANTEED / UNRESOLVED_MISS` 四分法；
- explanation 只能作为注释，不能把 `UNRESOLVED_MISS` 自动变 PASS；
- 保留一组未参与 query 设计的 held-out sentinels，防止循环验收；
- 为 cs.MM/cs.MA 做受控 lane 或明确的 seed/venue rescue，并用 MAR3/VQQA 验证；
- 把 §4.2 的五篇直接近邻加入 seed/threat queue，把 §4.3 两篇列为 execution-early priority；
- 对 TF-TTCL 登记“旧日志已发现但未转录”的 provenance，不能假装本轮首次发现。

**验收：**任何一篇四种救援均不成立时测试失败；报告输入计数从 JSONL 自动读取为 53；类别和 seed
rescue 的责任边界可由机器输出解释。

### P0-R6：更正网络访问与零查询 attestation

采用不含糊的双计数：

- `discovery_queries_executed = 0`；
- `id_dereference_accesses = 21 canonical logged + approximately 25 prior aggregate-disclosed`。

未来每次 access 自发生时写 append-only event；transport retry 也有 parent attempt ID。不得再用“21 次均逐次
留痕”覆盖 header 已承认的未逐次记录访问。

### P0-R7：消除 Decision-Log 的 supersession 矛盾

新增 dated 条目明确：`T1_DEMOTED/T2_PROMOTED/T2_UNREVIEWED/quality_override` 哪些完全退役，哪些仅作为
历史 provenance 保留，哪些仍影响排序但绝不影响 evidence weight。旧 Decision-Log 不改写；新条目必须
逐条列明 supersedes 对象和理由。

### P0-R8：再做一次真正独立的窄幅签署复核

复核输入必须是新 correction #4A commit + git blob manifest，而不是当前工作树口头状态。最低验收集：

1. machine counts/package consistency；
2. 四个旧 replay + child real-row integration/negative tests；
3. REC/claim validator positive + negative tests；
4. route live-status audit；
5. sentinel holdout outcome；
6. network attestation reconciliation；
7. source target 与历史审计件未被回写。

只有一轮窄幅复核出现 **0 个新 MAJOR、0 个新 MINOR，且所有旧项有可重放 evidence locator**，reviewer
才可签署。签署后仍需 owner 批准，且首条 query 执行时应生成 REC-1 事件；签署本身不背书 novelty 或
科学效果。

## 8. Stage-1A 之后值得保留的 proposal 检查点（非本 gate 阻断项）

这些是 survey 应组织出的方向，不是现在跑实验：

1. **黑盒核心与外部训练组件分离。** AMC/MemoPilot 类工作会冻结核心却训练 value/updater；分别报告
   `core_frozen`、`external_component_trained`、`method_specific_training`，避免用“training-free”一词混洗。
2. **read-out 与 new-info 分离。** 自采样/verifier/环境反馈和 test-time web search 不属于同一种能力
   来源；任何提升都要标明信息从哪里进入系统。
3. **within-item 与 across-item persistence 分离。** EvoLib、TF-TTCL、JitRL 与 memory consolidation
   需要按状态寿命、更新对象、回滚和污染传播组织，而不是都叫 memory。
4. **system-level omni 与 component-level multimodality 分离。** MAR3/VQQA 可证明多模态组件邻近，
   但不自动证明 omni agentic system 身份；必须沿核心可见观察、工具 I/O、行动模态和因果 grounding 编码。
5. **负证据与停止规则。** memory 退化、verifier 偏差、单日 API overflow、无 headroom 的 null 都应进入
   同一 failure/stopping taxonomy，防止只积累正结果。
6. **Stage-1B 配置化工程准备。** 可以先定义 dataset/model/inference/evaluator/control-plane 的配置合同和
   dry-run schema；真正模型运行必须等 release。每个实验写定制代码会破坏后续横向比较，应把差异收敛到
   config 与插件接口，但这不是本次 survey 签署的前置开发任务。

## 9. 给研究团队 AI 的无歧义执行摘要

不要把本报告理解为“重做 proposal”“立刻跑更多模型”或“无限加论文”。下一步只有 Correction #4A：

1. 修 active signature package 的陈旧口径；
2. 让 child splitter 读取真实 query row，并统一 YEAR/MONTH/DAY 语义；
3. 实现 REC-0/REC-2/claim validator 和负测试；
4. 复核 50 route 的当日外部事实，修 ACL 2026；
5. 把 sentinel 改成不可由自由解释自动过关，并补本轮有限 direct seeds；
6. 更正网络访问双计数与 Decision-Log supersession；
7. 以新 commit/blob bundle 申请窄幅复审。

在此之前：**reviewer signature = WITHHELD；discovery query 继续为 0；模型触碰继续为 0。**

在完成这些之后：若窄幅复审零新发现，应签署 Stage-1A mapping execution gate，而不是继续人为添加预算
限制或要求 Stage-2 结果。

