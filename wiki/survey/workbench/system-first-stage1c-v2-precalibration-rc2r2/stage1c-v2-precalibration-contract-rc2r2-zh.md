# Stage-1C v2 Agentic RC2R2 frozen-provenance 合同

## 修复目标

RC2R1 已经闭合 N=56 完整性、逐 critical path agreement、结构化参考/借鉴/复现约束和 ACL
来源 receipt，但独立复审证明：调用者仍可替换整套内部自洽的 56-item universe、使用同 `$id`
的松 schema、引用伪造/跨论文 rendition，并用不透明 receipt ID 冒充实际分发。因此 RC2R1
不得进入 coder intake。

RC2R2 只修复上述 provenance 链，不引入新论文、实验族或技术判断。

## 静态信任根

`frozen_package_contract` 固定以下对象的 exact JSON bytes SHA-256：

- calibration manifest；
- source-byte manifest；
- coder distribution manifest；
- response schema；
- delivery-receipt schema；
- prepared agreement intake 的静态投影；
- paper→allowed renditions 映射；
- canonical-ID 顺序、共享 content bundle 与 coder prompt。

frozen contract 的 digest 以字面常量编译到 agreement v4。agreement 首先比较该常量，然后才
读取其余 artifacts。这样攻击者即便同步替换所有输入及其相互引用，也不能制造第二个可接受的
信任根。

## 运行时闭合

运行时 intake 只能绑定两个固定 slot：A=`gpt-5.6-sol`，B=`gpt-5.6-terra`。coder ID、
transaction ID 和 process ID 两两不同；两份 response 必须精确覆盖 frozen 56 IDs 与 packet
bindings。

每个 delivery receipt 必须包含实际收到的 bundle hash、prompt hash，以及 8 个 coder-visible
artifact 的名称、bytes 和 SHA-256。receipt 对排除自身 digest 字段后的 exact JSON bytes 哈希，
runtime slot 再绑定 receipt ID 与 digest。任意缺失、替换、错 slot 或自哈希不一致均在 agreement
计算前 fail closed。

## 证据边界

source manifest 为每篇论文固定 primary/alternate renditions 的 ID、bytes 与 hash。completed
response 中的每个 locator 必须引用该篇论文自身的 rendition；仅“在同一 manifest 中存在”不足以
通过。

泄漏扫描仍递归覆盖 coder bundle，但身份值豁免改为完整 JSON-path allowlist。例如真实 source
title 仅在 `blind_packet.items[*].title` 可豁免；`auxiliary_metadata.title` 不因同名叶字段获得
豁免。

## 当前权力状态

本合同只达到 `AGENTIC_RC2R2_CODER_READY_NOT_DISTRIBUTED`。当前事实仍为：零 coder 分发、
零 agreement、零研究模型调用、零 benchmark metric、零论文复现、零 prototype、零 novelty
verdict、零 full mapping 签名和零 push。

下一门是 commit-bound fresh independent review。只有获得精确 ACCEPT，才可按既有 owner
continuation 授权执行 N=56 双模型隔离校准；分歧裁决仍必须交 owner。
