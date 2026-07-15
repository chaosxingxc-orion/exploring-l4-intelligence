# Gate S1 送签 bundle manifest（S1-E6——全部配套工件唯一钉定）

（钉定基准 commit = **aa6e660**;哈希正典 = git blob（LF 规范化,核验
`git show aa6e660:<path> | sha256sum` 或 `git rev-parse aa6e660:<path>`）。本 manifest 自身
在后续 commit 中提交,其 blob 由该 commit 的工件清单外部可查——自指钉定不可能,如实声明。
任何单项更正走 dated correction 新条目,不覆盖历史哈希。）

| # | 角色 | path | git blob @aa6e660 |
|---|---|---|---|
| 1 | 科学提案（整体评审对象,含 errata 修订记录） | `wiki/2026-07-15-system-first-research-proposal-v3-consolidated.md` | `15f46eff37f2245f93a15e0b59ccefe67b7ba407` |
| 2 | 检索协议 v1+amendment-1（签署对象本体） | `wiki/survey/2026-07-15-system-first-survey-protocol-v1.md` | `2d55529357833dd4c88de526feaa4d67f6562486` |
| 3 | amendment-1 变更记录（取代关系与理由） | `wiki/survey/2026-07-15-sf-protocol-amendment-1.md` | `ed620b6826d07fcda2d375420254ecf49b3fe4a6` |
| 4 | seed manifest（60 条,快照 51+增量批次1） | `wiki/survey/2026-07-15-sf-seed-manifest.jsonl` | `1255fcfde89861d693cf75cd4f4b87758016beae` |
| 5 | manifest 生成报告（含裁决附注与增量附注） | `wiki/survey/2026-07-15-sf-seed-manifest-report.md` | `6c83dc51e9ce03f80716646deb3d0eccf3e343cb` |
| 6 | 编译冻结查询（48 行,S1-E2） | `wiki/survey/2026-07-15-sf-queries.jsonl` | `c87a23016d7f8c28e19bc707535f56e388eff803` |
| 7 | 离线编译器（纯 stdlib,零网络） | `scripts/survey/sf_query_compiler.py` | `97938e39c9825257d8e4c49f3a9d70fe4cd91d87` |
| 8 | 静态验证报告（S1-E8,联网查询数=0） | `docs/checks/2026-07-15-sf-queries-static-validation.md` | `42b2a902360cfeca815c8024707535db70200719` |
| 9 | 副源路线 manifest（16 条,S1-E4） | `wiki/survey/2026-07-15-sf-secondary-routes.md` | `901b1a54123238c737cf52e4259c147ec38beec7` |
| 10 | 空白记录模板 T1–T6 | `wiki/survey/2026-07-15-sf-blank-templates.md` | `a787059feb0552ce46005043a341ae9e6ff2220d` |
| 11 | 自库反扫工件（种子来源之一） | `wiki/survey/2026-07-15-gate-s1-own-library-sweep.md` | `8cf7b46e79bedb70284eefee2272afc0081b98c3` |
| 12 | v3 内审报告归档（S1-E7,含迟归档说明） | `docs/checks/2026-07-15-proposal-v3-hostile-review-lenses.md` | `b2cbc1567a9567082dfeed221b17d82c6af4b370` |
| — | 协议内审归档（前轮,续53） | `docs/checks/2026-07-15-gate-s1-protocol-hostile-review-lenses.md` | 见 806064d 批次（本 commit 未改,blob 沿用） |

**S1-E1..E8 自验状态**：E1 ✓（#1 修订记录节）/ E2 ✓（#6+#7,字节可复现）/ E3 ✓（协议 §4
类目冻结+溢出规则）/ E4 ✓（#9,可回放分级）/ E5 ✓（#4 增量批次1:直接威胁+基础谱系,SF-L9）/
E6 ✓（本件）/ E7 ✓（#12,迟归档如实说明）/ E8 ✓（#8,query 执行数=0）。
**attestation**：截至本 manifest 落笔,联网检索查询执行数 = 0。

## dated correction #1（2026-07-15,续55 签署级亲验复核）

复核方式 = 不沿抄提交信息、逐项按工件重验（12/12 blob 重算一致;编译器离线复跑 blob 复现
`c87a2301`;P0-A..D 逐 checkbox 对照）。发现唯一残留：**P0-C 末项「每篇最可能推翻的 RQ」
字段缺失**——修复 = 协议 §6 增 `most_threatened_rq` + T2 模板同步 + amendment-1 A1-9 行
（commit `1c4c26a`）。上表 #2/#3/#10 三件以更正后 blob 为准,原 @aa6e660 哈希保留不改写;
其余九件未动（blob 同 aa6e660）：

| # | path | git blob @1c4c26a |
|---|---|---|
| 2 | `wiki/survey/2026-07-15-system-first-survey-protocol-v1.md` | `f135373d49544ee9af577e39775d9aa3a1d2d92d` |
| 3 | `wiki/survey/2026-07-15-sf-protocol-amendment-1.md` | `c6a97969076a258d7fc5599a6025115f19a94632` |
| 10 | `wiki/survey/2026-07-15-sf-blank-templates.md` | `1763c793248f28acb50051637e8123de69a2760a` |

**attestation（更正后复签）**：截至本更正落笔,联网检索查询执行数 = 0。
## dated correction #2（2026-07-15,中断恢复后的整改包敌意环收敛）

背景：会话中断期间,恢复后的整改包敌意环（R1 七镜头,审 @aa6e660 态）发现 4 MAJOR + 10 MINOR
——其一（most_threatened_rq）已由 correction #1 先行闭合;其余 13 项于 `8f76a16` 闭合,R2 窄幅
复检 13/13 FIXED + 3 新残留于 `d2fab2d` 清零（grep 终验 0/0/0）,环收敛。要点：§3 schema 五值
enum+SF-L9、A1-1 敏感性计数机器重数 16→19/18+eess.IV 补裁决、§9/T1 每页一行 schema 取代 cap
语义、批次1 后现值分布节（Σ=89,机器解析）、v3 三处陈旧计数+假「唯一 scope_pending」更正。
受影响工件以 `d2fab2d` blob 为准,原哈希保留不改写：

| # | path | git blob @d2fab2d |
|---|---|---|
| 1 | `wiki/2026-07-15-system-first-research-proposal-v3-consolidated.md` | `10185474788c` |
| 2 | `wiki/survey/2026-07-15-system-first-survey-protocol-v1.md` | `775fb7615a8b` |
| 3 | `wiki/survey/2026-07-15-sf-protocol-amendment-1.md` | `081ed1c12b8e` |
| 5 | `wiki/survey/2026-07-15-sf-seed-manifest-report.md` | `445ce34d3c8b` |
| 8 | `docs/checks/2026-07-15-sf-queries-static-validation.md` | `7d62a77847e7` |
| 9 | `wiki/survey/2026-07-15-sf-secondary-routes.md` | `5307737a303f` |
| 10 | `wiki/survey/2026-07-15-sf-blank-templates.md` | `a94f231aed9c` |
| 12 | `docs/checks/2026-07-15-proposal-v3-hostile-review-lenses.md` | `ecdbd6ace953` |
| + | `wiki/survey/README.md`（token 登记面,随包） | `dbf6f5eb0000` |

未变件：#4 manifest（`1255fcfd`——批次1 后未再动）/ #6 queries.jsonl（`c87a2301`,编译产物
全程稳定）/ #7 compiler / #11 sweep。**attestation（更正后复签）**：联网检索查询执行数 = 0。
