# Stage-1C v2 Agentic RC2R1 方法合同

RC2R1 是已提交 RC2 的追加修复版本，不改写 RC2。修复范围严格限定为独立复审指出的两类
P0 与两项 P1：agreement intake、逐字段 gate、BORROW/REPRODUCE 语义约束、两篇 ACL 来源
receipt 和 coder-visible 全元数据泄漏扫描。

Agreement 只有在两份响应都满足以下条件后才能计算：精确 56 篇、canonical ID 集完全一致、
response schema 和 completed-response 语义检查通过、packet/source/bundle/prompt 绑定一致，且
coder、transaction、process 三者均相互独立。对象层先计算 segmentation，再对每个 critical
field path 单独计算 exact agreement。任何 `NOT_CALIBRATED` 或低于 0.85 的承重门都使 overall
失败，不能由其他高一致率字段稀释。

参考、借鉴和复现严格分开：REFERENCE 不迁移协议；BORROW_PROTOCOL 必须给出 source→target
变量翻译和拒绝观测；REPRODUCTION_CANDIDATE 必须闭合任务、数据版本与 split、官方代码版本、
入口、access、许可、evaluator、local state 和 locator。仅有本地资产不能自动成为 anchor。

当前状态只允许形成 exact independent-review package。独立复审 ACCEPT 后，才能按 owner 已
记录的连续授权绑定两个隔离 model coders；两份原始结果冻结前不得计算 agreement。Owner 的
人工裁决、post-calibration mapping 签名和最终 portfolio 签名均不可由本合同替代。

本合同不运行研究模型、benchmark metric、论文复现或 prototype，不给出 novelty verdict，
不 push。
