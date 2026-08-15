---
check_id: "SAEA-DATA-ACQUISITION-WAVE2-2026-08-15"
status: "PASS_ACQUISITION_AND_REGISTRATION_ONLY"
authority: "dataset acquisition, on-disk re-verification, integrity verification and canonical-lock registration only"
---

# Speech-aware 数据获取 wave 2 收据（2026-08-15）

## 裁定

**PASS。** 三项既有持有（SLURP、SLUE-SQA-5、Spoken-SQuAD）按推荐 variant 原地复核完成，字节与
lock 指纹逐项对齐，未重新下载、未删除任何本地数据；三项新资产（HALAS、SlideASR-Bench、
SQuAD v1.1 dev 重建参考）已获取、逐文件校验并登记进 canonical lock。

本收据只关闭**数据身份与字节门**。模型触达、API 调用、实验执行、Stage-2A 执行授权与任何
paper-scale 工作均不在本收据范围，本次任务也未触碰 GPU / llama-server / study 仓
`studies/speech-aware-evidence-acquisition`。

资产身份、状态、许可、边界与验证字段的**唯一 live source**是 `docs/datasets.lock.json`。
本文件是 2026-08-15 的审计快照，不得反向成为第二份状态表。

## 一、三项既有持有的原地复核（未重新下载）

| 资产 | lock key | 复核结论 |
|---|---|---|
| SLURP | `slurp` | **verified-complete**。持有的是**上游原始 variant**（pinned `pswietojanski/slurp` checkout + Zenodo 4274930 音频发布），是 HF `qmeeus/slurp` 重打包的超集 |
| SLUE-SQA-5 | `slue-sqa-5` | **verified-complete**。`verified_test` 与 `test` 两个目标 split 早已在盘 |
| Spoken-SQuAD | `spoken-squad` | **verified-complete**（test 集）；**原始完整问题表缺失**，需 SQuAD v1.1 dev 重建 |

### SLURP

Git HEAD `8eb16545762be97ace75334109d73824217311f1`，与 lock revision 一致。

- 真实语音 `slurp_real`：72,395 个 FLAC / 3,911,348,301 bytes；
- 合成语音 `slurp_synth`：69,257 个 FLAC / 2,837,310,779 bytes；
- 连同两个 tar.gz 与两份下载日志共 141,656 files / 13,507,477,690 bytes，
  与 lock 的 `files` / `size_bytes` **逐字节相等**；
- 真实音频引用闭合：train/devel/test.jsonl 引用的 72,395 个唯一 recording 与盘上 72,395 个文件
  **一一对应**（0 缺失、0 未引用）；
- **slot 标注存在**：`repos/slurp/dataset/slurp/{train,devel,test,train_synthetic}.jsonl` 每条 utterance
  带 `entities`（span + type）与 `sentence_annotation`，标注数分别为 11,367 / 2,022 / 2,823 / 14,623；
- **per-recording `ent_wer` 存在**：`recordings[]` 每项含 `file`、`wer`、`ent_wer`、`status`；
- real + synth 音频合计 6,748,659,080 bytes（≈6.75 GB），与 HF `qmeeus/slurp` 重打包体量吻合，
  故不需要另取该 variant。

### SLUE-SQA-5

Revision `e2989c55a53593a8e39b8f8ebdb47ccaccbe484a`；上游 pinned file list 301 files /
118,074,483,514 bytes，与盘上完全一致，partial marker 为 0。

| split | shards | rows | bytes |
|---|---|---|---|
| `verified_test` | 3 | 408 | 866,778,007 |
| `test` | 14 | 2,382 | 5,677,818,113 |
| `validation` | 12 | 1,939 | 4,623,616,828 |
| `train` | 270 | 46,186 | 106,906,260,175 |

合计 50,915 rows，与 lock `expected_payload.rows` 一致。列含 `question_audio`、`document_audio`、
`raw_question_text`、`raw_document_text`、`normalized_*`、`word2time`、`answer_spans`——
要求的 `document_audio` 与 `raw_document_text` 字段齐备。

`train`（106.9 GB）在本任务开始前（2026-08-03）就已完整落盘，因此"不要拉 train"的指示在本轮
**没有产生任何获取动作**；同时删除本地数据不在本次授权内，故保持原样。

### Spoken-SQuAD

Revision `b55aab98726d0eab95eeef1ee9992a0532b3226e`；上游 pinned file list 23 files /
3,403,613,158 bytes，与盘上完全一致，partial marker 为 0。21 个 test shard 共 5,351 rows，
列只有 `context`（音频）/`instruction`（问题文本）/`answer`，**没有 question_id**。

lock 中 legacy 指纹 `files: 25` / `size_bytes: 3403615926` 比 payload 多 2 个文件、2,768 bytes，
来源是下载器留下的 `.hfd/last_download_command`（162 B）与 `.hfd/repo_metadata.json`（2,606 B）。
为保持历史指纹可复现，该记录**不做改动**，只在 lock amendment 中写明对账。

**原始完整问题表结论：缺失。** 该镜像只保留作者删除后幸存的问题，因此本轮补取 SQuAD v1.1 dev
作为重建参考（见下）。

## 二、两项新获取 + 一项重建参考

### HALAS（`halas`，newly-downloaded）

Revision `317cef3a10d1097edc37e8eb1c007f415e3d0c55`；6 files / 7,186,701 bytes；6 个文件全部做了
**固定 revision 远端字节 vs 本地字节的 SHA-256 比对，全部一致**；partial marker 0。

- `HALAS_dataset.csv` 3,611 行 × 41 列（`train.csv` 2,866 / `test.csv` 745）；
- 列含 `audio_id`、`e22_reference_text`、`corrected_reference_text`，以及 9 个 ASR 系统各自的
  `*_prediction` / `*_label` / `*_hallucination_text` / `*_hallucination_json`（span 级）；
- 载体连接：`audio_id` 形如 `<segment_index>_<earnings22_call_stem>.wav`，涉及 125 个
  Earnings-22 call，与本仓 governed `earnings22-original` 的 125 个 media stem **125/125 全匹配**；
  标注覆盖音频 2.8467 小时。

**许可：上游 dataset card 逐字写作 `unknown`**（`cardData.license == "unknown"`，HF tag
`license:unknown`），无 SPDX 标识、无 LICENSE 文件、无条款正文。lock 条目已带
`license_note: UNRESOLVED_FOR_PUBLICATION` 与 `claim_limit`：仅限本地研究使用；再分发、派生发布
与任何 Stage-3 发表用途在上游条款书面澄清前**一律阻断**。

### SlideASR-Bench（`slideasr-bench`，newly-downloaded）

Revision `6f05006aeca495af24a5ff080a75c3884f1915ca`，license `mit`；16,939 files /
10,836,763,656 bytes；0 缺失、0 尺寸不符、0 partial marker；**16,934 个 LFS 对象逐个 SHA-256 与上游
OID 比对，0 失败**；5 个非 LFS 文件记录固定 revision 原始字节 SHA-256。

上游**不按 split 分目录**：`SlideASR-S/audio/` 一棵树同时服务 `test.jsonl` 与 `train.jsonl`，因此
pin 的单位是固定 revision 的整仓，"只要 test"在**消费层**而非下载层强制。

| 单位 | 行数 | 音频 | 时长 | entity_list |
|---|---|---|---|---|
| `test.jsonl`（消费） | 2,054 | 2,130,709,552 B，0 缺失 | 18.4950 h | 13,895 项（每行 5–12） |
| `train.jsonl`（不消费） | 6,413 | — | 67.2922 h | 44,240 项 |

音频总计 8,467 个 WAV / 9,883,054,910 bytes（English 4,819、Mandarin 3,648）；
slide 图片 8,467 个 / 940,766,287 bytes。

**边界（已写入 lock `consumption_boundary`）**：本 study 只读 test split 的 `audio/**` 人声 WAV 与
每条样本的 `entity_list` 文本；8,467 张 slide 图片仅为整仓字节闭包而 pin，**任何 loader / reward /
trace 都不读取**；`train.jsonl` 同样不消费，以维持 discovery / confirmatory 隔离。

### SQuAD v1.1 dev（`squad-v11-dev`，newly-downloaded，重建参考）

官方 `rajpurkar.github.io/SQuAD-explorer/dataset/dev-v1.1.json`；4,854,279 bytes；
SHA-256 `95aa6a52d5d6a735563366753ca50492a658031da74f301ac5238b03966972c9`；
`version` 1.1；48 篇文章 / 2,067 段 / 10,570 问题（10,533 个唯一问题文本）。

重建可行性实测：Spoken-SQuAD test 的 5,335 个唯一问题文本 **5,335/5,335 全部**能在 SQuAD v1.1 dev
中找到；dev 中有 **5,198** 个问题在该镜像里不存在——即作者按"答案被 ASR 噪声破坏"删除的部分。
由于镜像不带 `question_id`，重建的 join key 只能是**逐字问题文本**，这一点已写入 lock。

## 三、Lock 变更

- 新增三条 `asset_catalog` 记录：`halas`、`slideasr-bench`、`squad-v11-dev`（catalog 107 → 110）；
- 三条既有记录（`slurp`、`slue-sqa-5`、`spoken-squad`）的 identity / revision / size 字段
  **一律未改**，只在 `amendments` 追加 2026-08-15 的复核与对账条目；
- `profiles.speech-aware-secondary` 描述加入 SlideASR-Bench；
  `profiles.speech-aware-annotations` 重述为"只承载标注、不带语音字节"的 overlay profile
  （TED-EL + HALAS + SQuAD v1.1 dev）；
- 顶层 `generated` 更新为本轮说明。

## 四、离线核验

| 检查 | 结果 |
|---|---|
| `asset_lock.py validate` | `OK 110 assets` |
| `inventory.sh --fail-on-drift`（全目录） | `BLOCKED=11 COMPLETE=99 MISSING=0 PARTIAL=0 drift=0` |
| `inventory.sh --profile speech-aware-secondary --full --fail-on-drift` | `COMPLETE=4 drift=0` |
| `inventory.sh --profile speech-aware-annotations --full --fail-on-drift` | `COMPLETE=3 drift=0` |
| `inventory.sh --profile speech-aware-core --full --fail-on-drift` | `COMPLETE=3 drift=0` |
| `pytest scripts/data/test_asset_lock.py` | `7 passed` |
| `scripts/checks/code_graph_check.py` | `PASS (24 trusted nodes)` |
| `scripts/checks/ai_context_surface_check.py` | 本任务中段运行为 `PASS (0 failures)`；收尾复跑为 `FAIL (1)`，唯一失败项 `new-audit-artifact-outside-audit-root: wiki/experiments/speech-aware-evidence-acquisition/2026-08-15-owner-amendment-dual-track-agentic.md` 来自并行会话提交 `402cffb`，与本次数据变更无关，未在本任务中改写或掩盖 |
| `scripts/checks/legacy_asset_resolution_check.py` | `PASS (COLD_BACKUP_RESOLVED=574, UNRESOLVED=0)` |
| `scripts/checks/build_ai_context_manifest.py --check` | `PASS` |
| `scripts/checks/study_workspace_check.py` | `PASS` |
| `scripts/checks/paper_workspace_check.py` | `PASS` |

## 五、非阻塞观察（本轮不处置）

1. **SLURP 音频在盘上共有三份物理副本。** governed 路径
   `repos/slurp/scripts/audio`（141,656 files / 13,507,477,690 B）之外，`datasets/slurp` 顶层还有一份
   完整副本，其下 `datasets/slurp/audio/` 又有一份，`datasets/slurp` 子树合计 283,312 files /
   27,014,955,380 B。经 PowerShell 复核，这些路径**都不是** symlink / junction / hardlink
   （`LinkType` 为空，`fsutil hardlink list` 只列出自身），即 27.0 GB 是真实重复占用。
   legacy `fetch_slurp` 原意是建 `datasets/slurp -> repos/slurp/scripts/audio` 的软链，实际落成了拷贝。
   删除不在本次授权内，故只记录，未处置。
2. **SLUE-SQA-5 `train` 106.9 GB 已在盘。** 本轮未拉取、未删除；若后续要压缩占用，需要单独的
   owner 处置授权。
3. **并行会话在本任务运行期间向伞仓落了两个提交**：`6a42d1d`（survey ledger 回填，正是本任务开始时
   工作树里那处无关改动）与 `402cffb`（owner dual-track 记录 + 两份 survey note）。二者都未触碰
   `docs/datasets.lock.json`；本任务的 lock diff 相对 HEAD 恰为 86 insertions / 3 deletions，
   无冲突、无覆盖。`402cffb` 是收尾 `ai_context_surface_check` 唯一失败项的来源，属于该会话的范围，
   本任务未改写。
