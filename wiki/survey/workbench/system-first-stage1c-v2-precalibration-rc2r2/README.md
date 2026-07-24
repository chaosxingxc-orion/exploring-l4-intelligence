# Stage-1C v2 Agentic RC2R2

RC2R2 是 RC2R1 的不可变后继，只修复独立复审指出的 frozen-provenance 缺陷。它不改写
RC2/RC2R1，不分发 coder，不计算 agreement，也不执行 320-work mapping、研究模型、指标、
论文复现或 prototype。

当前状态：`AGENTIC_RC2R2_CODER_READY_NOT_DISTRIBUTED`。

## 信任链

1. `frozen-package-contract-v1.json` 固定 calibration、source、distribution、response schema、
   delivery-receipt schema、prepared intake、paper-scoped rendition map、共享 bundle 和 prompt
   的精确 SHA-256。
2. 该 frozen contract 自身的 SHA-256 作为字面常量编译进 agreement v4；调用者不能用另一套
   内部自洽 artifacts 替换它。
3. runtime intake 只可填入 coder、transaction、process、model 和 receipt 绑定；其静态投影
   必须与 frozen prepared intake 完全一致。
4. 每名 coder 的 delivery receipt 记录实际收到的 8 个 artifact 的 bytes/hash、共享 bundle、
   prompt 和 receipt 自身 digest；agreement 在读取 response 前先验证整条链。
5. source locator 的 rendition 必须属于 frozen source manifest 中同一篇论文，禁止伪造或跨论文
   rendition。

## 分发边界

coder-visible 内容仅为 response schema、source manifest、assignment、blind packet、中性
codebook、中性 claim view、agreement rules 和 prompt。身份、receipt、readiness、selection rationale、
origin links 和 prior labels 均不进入共享内容包。字符串豁免按完整 JSON path，而不是字段叶名。

只有新的独立复审给出
`ACCEPT_AGENTIC_RC2R2_METHOD_CONTRACT_FOR_CODER_INTAKE` 后，既有 owner continuation 授权
才允许开始两名隔离 model coder 的 N=56 分发。owner adjudication、mapping 签名、portfolio
签名、Stage-2A 和 push 仍是独立人工门。
