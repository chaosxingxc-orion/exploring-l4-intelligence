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