---
check_id: "R2-STAGE2A-DATA-ACQUISITION-2026-08-02"
status: "PASS_D0__D1_D4_NOT_EVALUATED"
authority: "dataset acquisition, local derivation, integrity verification and canonical-lock consolidation only"
---

# R2 Stage-2A 数据获取与 D0 闭包收据

## 裁定

**D0 PASS。** Earnings21、Earnings22、ConEC 已按固定 Git revision 落到
`SPEECHRL_DATA_DIR`，Earnings 音频与元数据数量/时长和官方说明一致，复制前后逐文件
SHA-256 一致，Earnings22 不再含原始 LFS pointer。该裁定只关闭数据身份与字节门；D1-D4、
模型/API 调用、实验与 Stage-2 执行授权均不在本收据范围。

当前资产身份、状态、许可、阻塞原因与验证字段的**唯一 live source**是
`docs/datasets.lock.json`。本文件是 2026-08-02 的审计快照，不得反向成为第二份状态表。

## 核心闭包证据

| 资产 | 固定身份 | 本地核验 |
|---|---|---|
| Earnings21 | Rev `c05ab6fd8b4b627d123c922a22a39e993dd37635` | 676 files，875,886,792 bytes；44 calls；141,348.532 s（39.2635 h） |
| Earnings22 | 同一 Rev commit | 527 regular files，1,993,169,787 bytes；125 main calls；428,021 s（118.8947 h）；30 个 subset symlinks |
| ConEC | `88440713d8b80dc4f19b225f6480237e78c379de` | 514 files，370,772,197 bytes |

Earnings21/22 的共享 payload 清单含 1,203 个 regular files，清单 SHA-256 为
`5d2071f974302ce77a08b64247ac90f3ad0b2ddab4d7d0eae442bfd22c4f8088`。30 个符号链接的独立
清单 SHA-256 为 `8a96b36225049f67e0cc3a7fa0c5983ddd18a7a9c1cd24707173584470c88970`。
两份清单位于数据根的 `manifests/r2-stage2a-fetch/`，不进入 Git。

上游 Rev 仓库的 `.gitattributes` 未覆盖 Earnings22 的 125 个根 MP3，导致常规
`git lfs pull` 留下文本 pointer。本地获取链补充 repo-local attribute，逐一按 pointer 的
SHA-256 OID 和 size materialize；最终 `remaining_pointers=0`。`subset10` 的 10 条链接是主音频的
投影，不重复计为独立 call。

## 本轮其它结果

- 完成：PRISM、Rare5k reconstruction、BuzzWord、TED-EL annotations、ATCO2-1h、
  Eka-Medical、LibriSQA。
- 可续传但非阻塞：SQA-5 为 4/301 files、821,867,405/118,074,483,514 bytes；
  ContextASR-Bench 为 6/35 files、104,823,821/96,662,324,651 bytes。
- Rare5k 从本地 LibriSpeech train-960 的公开协议重建为 83,949 个 rare words，和论文约
  209.2k 不一致；缺失 tokenizer/normalization 原工件，因此 lock 明确标为 reconstruction。
- 原 E 盘不完整 Earnings clone 已可恢复地移至数据根
  `manifests/r2-stage2a-fetch/earnings21-22-partial-preclosure-20260802`，未做不可恢复删除。
- 复制后哈希与 Git identity 复核通过后，删除了 `/home/chao/speechrl-downloads/earnings21-22`
  的 5.3 GB 重复 ext4 staging copy；完整 E 盘 governed copy 与上游固定 revision 均可恢复该内容。

## 离线核验

- canonical lock：104 assets；86 `COMPLETE`、3 `PARTIAL`、6 `MISSING`、9 `BLOCKED`；
- `r2-core --full --fail-on-drift`：3/3 `COMPLETE`，drift=0；
- 全量 inventory、单元测试、Python 编译、shell 语法和 diff whitespace gate 的最终结果见
  同目录 `asset-acquisition-receipt.json`；
- `sf_current_package_check.py --check` 的 trusted-code-graph 差异来自本任务开始前已有的
  staged/current-package 变更，不属于数据闭包，未在本任务中改写或掩盖。

下一步只做 D1-D4：跨层 sample mapping、信息可用时间/泄漏约束、评测定义，以及 10 个固定样本的
无模型 loader/provenance smoke；二级大数据下载不得继续阻塞 Stage-2A 收敛。
