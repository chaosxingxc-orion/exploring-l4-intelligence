# Stage-1C v2 Agentic RC2R3 运行时完整性修复说明

## 结论

RC2R3 只修复 RC2R2 独立复审指出的三项缺陷，不改变 N=56、论文编码语义或研究范围。
当前状态是 `CODER_READY_NOT_DISTRIBUTED`，不是校准完成，也不是 320-work mapping 已获授权。

## 三项修复

第一，agreement threshold 被编译冻结为 `0.85`。所有 paper-level critical fields、对象分割和
对象内部 critical fields 都使用同一个不可覆盖常量。调用方传入 `0.84`、`0.86` 或其他值会在
计算任何一致率之前失败，零正例仍为 `NOT_CALIBRATED`，不能被平均值掩盖。

第二，delivery receipt 不再从 distribution manifest 抄写期望值。收件端必须把实际收到的八个
artifact 原始 bytes 和 prompt bytes 交给 builder；builder 重新计算逐文件长度、SHA256、按固定顺序
组合的 bundle digest 和 prompt SHA256。缺文件、多文件、非 bytes、单字节变化或 prompt 与
`coder_prompt` artifact 不同，均不产生 receipt。receipt 还绑定 coder、transaction、process、task
和模型身份。这里严格表述为“受控 builder 观察到的本地字节证明”，不冒充第三方数字签名。

第三，leak scanner 在授权判断阶段使用 `(key, value)` 与 `(index, value)` 的 typed segments，
只有真正数组路径下的身份字段可以豁免。`items[0]`、`items.0`、`items/0` 等字面 key 不会伪装成
数组索引；blind packet 对意外顶层 key 也 fail closed。

## 不变边界

- RC2、RC2R1、RC2R2 及其复审不可改写；
- Duplex 专用模型路线继续排除；
- 参考、借鉴和复现的语义合同不变；
- 当前没有 coder distribution、agreement、owner adjudication、研究模型调用、benchmark、复现、
  prototype、novelty verdict、320-work mapping、Stage-2A 或 push；
- 只有 fresh independent reviewer 返回精确
  `ACCEPT_AGENTIC_RC2R3_METHOD_CONTRACT_FOR_CODER_INTAKE` 后，既有授权才允许 N=56 分发。

后续若校准输出完成，必须先冻结 A/B 原始响应，再计算 pre-adjudication agreement，并把所有承重
分歧交 owner 裁决；320-work mapping 仍需 `SIGN_STAGE1C_V2_EXPERIMENT_MAPPING`。
