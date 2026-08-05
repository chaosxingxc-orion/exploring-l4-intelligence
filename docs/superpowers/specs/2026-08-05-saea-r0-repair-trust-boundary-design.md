# SAEA R0 修复设计：信任边界与 run transaction 闭合

## Status

回应独立评审 `wiki/audit/speech-aware-evidence-acquisition-r0-review/independent-review-2026-08-05/`
（verdict `R0_REPAIR__R1_MODEL_FACING_EXECUTION_WITHHELD_PENDING_P0_CLOSURE_AND_R0_SMOKE`）。
所有 P0/P1 声明经本方独立复核**全部确认**（控制面代码核读 + 两个验证 agent 的可执行探针，
证据见 study `.superpowers/sdd/r0-repair/verification.md`）。本件冻结修复范围与验收判据；
不修改 owner 合同，不扩大到 R1/X/2B 范围。

```yaml
record_kind: r0-repair-design
date: 2026-08-05
study: speech-aware-evidence-acquisition
reviewed_study_commit: b0635aa9736d2cbf3a581fc9295110172672c833
reviewed_umbrella_commit: 047cf39dcbb7b8cde56757d69eb63a98c9f86de0
verdict_accepted: true
```

## §1 根因（决定修复方式，不只是补洞）

1. **威胁模型同源。** 前五轮对抗的"治理不变量"清单由实施方自己从 diff 推导：覆盖文件治理
   （冻结面、禁用数据集、无模型触达、无提交字节），完全未覆盖**运行期信任边界**——收据是否
   自洽、payload 值是否与 plan 一致、回答请求的进程是否即被 pin 的那个。审查者在被审查者的
   世界观内攻击，故全部 held。
2. **验证锚点错位。** 任务级评审对照"计划中的 authoritative code block"，逐字一致即 PASS。
   当计划本身缺一条检查，链上无人能发现。独立评审从**合同**做承诺-证据矩阵，才暴露
   "承诺 measurement integrity、交付 wiring"。
3. **自证 artifact 被当作已验证 artifact。** 系统性模式：哈希了能哈希的东西，未把哈希绑定到
   实际发生的事（splits.json 自证；runtime receipt 只证磁盘不证 server；outputs.text 与其自身
   response hash 无关系）。
4. **预算是进程内存计数而非持久化事务。** exposure ledger 被设计为"人写的审计记录"，无
   attempt 语义、无一次性消费、无失败成本落盘。
5. **结论措辞越界。** "这些攻击未发现缺陷"被表述为"零缺陷"。

### 由根因导出的方法变更（本次修复必须遵守）

- 计划**不再给 authoritative code block**：给**不变量 + 回归探针**，实现由执行者推导，评审对照
  不变量而非字面代码；
- 每个修复任务必须携带一个**从 ACCEPT 变 REJECT** 的可执行探针；
- 终审威胁模型来自**合同承诺**与**外部输入信任边界**，由独立视角生成，不复用实施方清单；
- 结论只能表述为"以下攻击面在 X 轮中未被攻破"，附攻击清单。

## §2 修复范围与不在范围

**在范围（P0）：** split 收据真实性、carrier/media/payload 值级绑定、runtime session 身份、
一次性 attempt 预算。
**在范围（P1）：** run bundle 哈希闭包与 finalizer、三条工程控制的正式 config、scorer seam
端到端、成本记账补全、CI 与文档对齐。
**不在范围（合法延期，评审亦确认）：** X1/X3/X4 policy、oracle 具体算法、confirmatory 大规模
验证、paper-scale 与 manuscript。

**冻结面调整（显式声明）：** `contracts.py` 此前"不可改"是 R0 实施计划的自设约束，非 owner 合同
条款；gate 加固必须修改它。E0 收据不覆盖 `contracts.py`（D3 只冻结 `scoring/`），修改后必须
重跑 receipt 校验与全部 contract 测试。`scoring/`、`e0/`、既有 `docs/receipts/*.json`、
`docs/exposure-ledger.md` 仍不可改。

## §3 必须成立的不变量（验收判据）

- **I1 split 真实性：** 任何模型触达前，splits 收据必须通过严格解析（schema、精确键集、
  每 split 的 carrier/role/count/ids 排序唯一且前缀一致、identity_hash 由 ids 重算相等、
  同载体 split 之间互斥），并与**当前 loader 实时重算**结果逐位相等；不一致一律 fail closed。
- **I2 载体范围：** plan carrier 必须属于本 study 的 speech 载体白名单（由 umbrella lock 的
  profile 推导）且不在 general-audio 拒绝名单；exposure 行的载体列必须被解析并与 plan 一致。
- **I3 payload 值级绑定：** adapter 必须核验 `payload.carrier_lock_key == plan.carrier_lock_key`、
  `speech_ref == f"{carrier}/{sample_id}"`、`sample_id ∈ 冻结 split ids`、`audio_seconds` 与
  loader 事实一致。
- **I4 媒体禁闭：** `media_relpath` 只接受规范化 POSIX 相对路径；解析后必须位于该 carrier 的
  `local_subdir` 之内；绝对路径、盘符、反斜杠、`..`、symlink 逃逸一律拒绝（adapter 与 transport
  双层）。
- **I5 server 身份：** endpoint 仅限本机；每次 run 必须存在 session receipt，绑定二进制哈希、
  PID、argv、端口与 model/mmproj 路径；无 session receipt 或身份不符则拒绝触达。
- **I6 一次性 attempt：** `(run_id, attempt_id)` 为不可复用主键，gate 以原子独占方式开启；
  实际用量在**发送前**持久化，失败不丢；重试必须新 attempt；slice 上限对"登记预留"与
  "实际用量"取保守上界。
- **I7 产物闭包：** 每个 attempt 产出 run manifest，绑定 study commit、config/protocol/plan/split
  身份、exposure 行与 attempt id、outputs/raw trace/trace manifest/scores/session receipt 的哈希、
  实际成本与终态；scorer 必须经 manifest 入口并先完成全链校验（response hash 对应 text、
  sample 集合等于冻结 split、无重复）。
- **I8 记账完整：** calls/tokens/latency/audio 之外，补 GPU/CPU/峰值显存实测、证据字节、
  失败 attempt 成本；无法实测项必须显式记为 deviation 并提请 owner 处置，不得静默省略。
- **I9 CI 真实性：** CI 反映当前 R0 语义；clean-clone job 先安装包；active tree lint 设门；
  五个探针成为常驻回归；coverage/type-check 若未配置须显式标注 `NOT_CONFIGURED`。

## §4 常驻回归探针（必须从 ACCEPT 变 REJECT）

| # | 攻击 | 当前 | 修复后 |
|---|---|---|---|
| P1 | exposure 行为 earnings21，plan carrier=`fsd50k` | ACCEPT | REJECT |
| P2 | 收据 ids 被替换、identity_hash 保留旧值 | ACCEPT | REJECT |
| P3 | data root 外绝对 media 路径 | READ/SEND | REJECT |
| P4 | 同一 exposure 行/plan 重复开门、计数归零 | ACCEPT×2 | 第二次 REJECT |
| P5 | earnings21 plan 下提交 `fsd50k` payload | ACCEPT | REJECT |

## §5 交付顺序

H1 split 闭合 → H2 载体/媒体/payload 绑定 → H4 attempt 记账 → H3 session 身份 →
H5 bundle+finalizer → H6 config/scorer/成本 → H7 CI/文档 → 全新独立视角终审 → 提交 fresh
rereview 包。R0.3 smoke 与 R1 在终审通过且 owner 处置到位前不启动。

## §6 需要 owner 处置的项（不得由实施方自行解释）

1. entity/QA scorer adapter 是否属于 R0 交付（其参考层格式尚未冻结），或明确移出并接受；
2. GPU/CPU/VRAM 记账：本设计选择**实测采样**而非延期，若采样在本机不可得，需 owner 接受
   deviation；
3. R0.3 `SAEA-E-001` 执行授权与 attempt 预注册。

## 失效条件

owner 修改上述范围、判据或授权时就地取代本件并保留日期记录。
