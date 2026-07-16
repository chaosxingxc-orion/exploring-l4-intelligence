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

## dated correction #3（2026-07-16,amendment-3 整改批 @37da7f3——收官就绪度评审 G5 闭合钉定）

背景：v3 收官就绪度评审裁定 correction #2 所钉对象集已被 `691150a`/`705b69a` 策略改写
实质取代（G5「bundle 唯一钉定失效」）;owner 四裁决（续59）触发 amendment-3 整改批,一次性
落盘后以 `37da7f3` 钉定现行全件。原哈希保留不改写。**本 correction 起,签署对象 = 下表
所列 @37da7f3 的不可变集合。**

| # | path | git blob @37da7f3 | 相对 correction #2 |
|---|---|---|---|
| 1 | `wiki/2026-07-15-system-first-research-proposal-v3-consolidated.md` | `30e50c048a2c` | 变更（errata-2 八项） |
| 2 | `wiki/survey/2026-07-15-system-first-survey-protocol-v1.md` | `3133ffb76e03` | 变更（A3 折入,v1+amendments 1–3,51 查询/74 种子口径） |
| 3 | `wiki/survey/2026-07-15-sf-protocol-amendment-1.md` | `cfbf1ac326a8` | 含 691150a 期 amendment-2 增补行（本批未动） |
| 3b | `wiki/survey/2026-07-16-sf-protocol-amendment-3.md` | `061c1437b489` | **新增**（A3-1..A3-12 独立日期件） |
| 4 | `wiki/survey/2026-07-15-sf-seed-manifest.jsonl` | `7eaefcc923e4` | 变更（批次2 +14 = **74 条**,initial_tag 字段） |
| 5 | `wiki/survey/2026-07-15-sf-seed-manifest-report.md` | `35148a9ae6f2` | 变更（批次2 附注+机器分布） |
| 6 | `wiki/survey/2026-07-15-sf-queries.jsonl` | `c56ca22629a2` | 变更（**51 行** = 48 原批字节前缀不变 + 3 增补） |
| 7 | `scripts/survey/sf_query_compiler.py` | `9508ef9eccdc` | 变更（sfqc-1.0.0/1.1.0 分层+增补注册表+防混入守卫） |
| 8 | `docs/checks/2026-07-15-sf-queries-static-validation.md` | `7d62a77847e7` | 未变（历史件,链条职能由 8b 取代） |
| 8b | `docs/checks/2026-07-16-sf-queries-static-validation-rerun.md` | `460c3a113d73` | **新增**（13/13 检查+前缀哈希+终态链条补记） |
| 9 | `wiki/survey/2026-07-15-sf-secondary-routes.md` | `249da3c7c15e` | 未变（退役留档） |
| 9b | `wiki/survey/2026-07-16-sf-t1-proceedings-routes.md` | `9bb2f3d3a8ac` | **新增**（50 route 实例化,§6 自检 7/7） |
| 10 | `wiki/survey/2026-07-15-sf-blank-templates.md` | `7129ed06d394` | 变更（**REC-1..REC-7**,A3-5 schema 传播） |
| 11 | `wiki/survey/2026-07-15-gate-s1-own-library-sweep.md` | `8cf7b46e79be` | 未变 |
| 12 | `docs/checks/2026-07-15-proposal-v3-hostile-review-lenses.md` | `5d5e55162b69` | 变更（LATE_RECONSTRUCTED_REVIEW_SUMMARY 补盖,A3-12） |
| + | `wiki/survey/README.md`（token 登记面,随包） | `7e77aaba5039` | 变更（A3 token 块+venue_tier 语义原位修订） |
| + | `wiki/2026-07-15-system-first-research-proposal-v3-stage1a-closeout-readiness-review.md` | `7bf0f83654e2` | **新增**（触发评审件,provenance） |

敌意环：双镜头（Opus ①计数一致性②G1–G6 闭合）R1 = 1 MAJOR+4 MINOR+2 NIT → 修复 → R2 窄幅
机器复检清零 → `A3_BATCH_LOOP_CONVERGED@37da7f3`。**attestation（更正后复签）**：联网检索
查询执行数 = 0。**下一动作**：本 correction 提交后,重新申请 Gate S1 search-design 窄幅复核
（范围 = G1–G6 闭合与本表一致性）。

## dated correction #4（2026-07-16——博导复审 WITHHOLD 六项整改批 @f3ab138,取代 correction #3 集合为现行签署对象）

签署对象自本 correction 起 = **@f3ab138 钉定的下表 25 件不可变集合**（correction #3 的 17 件
集合保留为历史钉定;后续任何变更走新 dated correction）。逐件 git blob（`git ls-tree f3ab138`
机器输出,short 12 位）：

| # | path | blob | 变更说明 |
|---|---|---|---|
| 1 | `wiki/survey/2026-07-15-system-first-survey-protocol-v1.md` | `93ccd1ff1b7a` | 变更（C4-2 tier 零证据权重折入/§4 计数 53/SF-L10 块/§6 七维+命名统一） |
| 2 | `wiki/survey/2026-07-15-sf-protocol-amendment-1.md` | `cfbf1ac326a8` | 未变 |
| 3 | `wiki/survey/2026-07-16-sf-protocol-amendment-3.md` | `061c1437b489` | 未变 |
| 3b | `wiki/survey/2026-07-16-sf-protocol-amendment-4.md` | `f44202048c24` | **新增**（C4-1..C4-6 对照+ID_DEREFERENCE 注册+编码深度纪律+两组合成验收案例+工件复跑清单） |
| 4 | `wiki/survey/2026-07-15-sf-seed-manifest.jsonl` | `cbd05401ff4b` | 变更（批次3 +13 = **87 条**,74 行前缀字节不变;入册前置=ID 核验 14/14 HIT） |
| 5 | `wiki/survey/2026-07-15-sf-seed-manifest-report.md` | `17ca7ec40c4c` | 变更（批次3 节） |
| 6 | `wiki/survey/2026-07-15-sf-queries.jsonl` | `d31fc0a66fde` | 变更（**53 行** = 51 行前缀字节不变〔前缀 sha256 `4e40658010d8…`〕+ SF-L10-Q1/Q2,sfqc-1.2.0） |
| 7 | `scripts/survey/sf_query_compiler.py` | `d3a4d800ae15` | 变更（三层版本 sfqc-1.0.0/1.1.0/1.2.0,ADDITION_LANES 注册表+守卫） |
| 8 | `docs/checks/2026-07-16-sf-queries-static-validation-c4.md` | `f89b894561af` | **新增**（C4 终态链条:协议→编译器→53 行 jsonl,前缀证明;13/13） |
| 9 | `wiki/survey/2026-07-16-sf-t1-proceedings-routes.md` | `9bb2f3d3a8ac` | 未变（保留为散文历史;机器正典移交 9b/9c） |
| 9b | `wiki/survey/2026-07-16-sf-t1-routes.jsonl` | `207acc5d1ac3` | **新增**（C4-3:50 条逐行序列化,exact URL/显式状态/判断依据/词表 hash 钉定/执行期字段占位） |
| 9c | `wiki/survey/2026-07-16-sf-t1-wordlist-v1.json` | `ee4e2d9750c2` | **新增**（词表机器正典:raw 73/有效 71,双侧归一化正典,合并对显式登记） |
| 9d | `scripts/survey/sf_t1_routes_validate.py` + `docs/checks/2026-07-16-sf-t1-routes-validation.json` | `c00d75175368` / `c717560d582d` | **新增**（仓内只读 validator + 持久化输出 **12/12 PASS**） |
| 10 | `wiki/survey/2026-07-15-sf-blank-templates.md` | `92943382e3a9` | 变更（**REC-0 工作级主账新增**;REC-1 派生行 C4-5 字段;REC-2 七维/proximity 统一/真枚举/evidence_grade 移出/coding_depth） |
| 10b | `scripts/survey/sf_child_query_split.py` + `scripts/survey/sf_child_query_replay_test.py` + `docs/checks/2026-07-16-sf-child-query-replay-test.json` | `6b64918eb7db` / `671b63a7e97d` / `6ad59559bef1` | **新增**（C4-5 拆分规范实现 + 离线合成 replay test **9/9 PASS**） |
| 11 | `wiki/survey/2026-07-16-sf-id-dereference-log.jsonl` | `515ed499c1c7` | **新增**（C4-6a:ID_DEREFERENCE 逐次留痕,21 次访问 14/14 目标 HIT 零幻觉） |
| 11b | `wiki/survey/2026-07-16-sf-sentinel-data.json` + `scripts/survey/sf_sentinel_recall_test.py` + `docs/checks/2026-07-16-sf-sentinel-recall.json` | `982cdd921e32` / `6f18b659a373` / `5f69e74cdfce` | **新增**（C4-6b:离线 recall **9 HIT + 5 EXPLAINED_MISS 零 unexplained**;AgentEval 经 SF-L10 转 HIT） |
| 12 | `wiki/survey/2026-07-16-gate-s1-correction-4-response.md` | `300225e906b5` | **新增**（C4-1 分层回应信:完成性更正表/§14 自评/双向合同/owner 改判披露） |
| + | `wiki/survey/README.md`（token 登记面） | `1be06b3f8e88` | 变更（T2_UNREVIEWED/T2_PROMOTED/T1_DEMOTED 退役标注;C4 新 token 登记） |
| + | `wiki/2026-07-16-gate-s1-rereview-application-stage1a-doctoral-review.md` | `092e389e4e07` | **新增**（触发评审件,provenance） |

敌意环：机械镜头（四脚本复跑/全 JSON 解析/模板块良构/计数交叉/前缀证明）+ 语义镜头
（跨件引用/口径残留）R1 = 1 finding（编译器 docstring 旧口径 51/48+3）→ 修复 → R2 复检
清零,`C4_BATCH_LOOP_CONVERGED@f3ab138`。**attestation**：联网检索查询执行数 = 0 维持;
ID_DEREFERENCE 访问类已注册并逐次留痕（amendment-4 §1）。**下一动作**：本 correction 提交后,
以回应信为封面请 reviewer 按复审 §14 十一项清单窄幅复核（双向合同:全过即签）。

## dated correction #4A（2026-07-16,博导复审 8 项 P0——钉定基准 commit = **af96a89**）

（触发 = 《Correction #4 执行前博导式对抗复审》WITHHOLD;owner 三裁决 = Decision-Log 续62。
哈希正典 = git blob,核验 `git rev-parse af96a89:<path>`。31 件 + fixtures 树;状态动词自本批
起由 `sf_package_summary.py` 机器推导——本表「变更/新增」仅描述文件事实,完成态见机器清单。）

| # | path | git blob @af96a89 | 变更说明 |
|---|---|---|---|
| 1 | `wiki/survey/2026-07-15-system-first-survey-protocol-v1.md` | `6d6adf6c2dbf` | 变更（P0-R1 口径统一:92 种子/55 查询/REC-0..7/amendments 1–5;§4 增 SF-L11 受控道） |
| 2 | `wiki/survey/2026-07-16-sf-protocol-amendment-5.md` | `f4e118051ee7` | **新增**（C4A 合同全文:P0 对照/splitter 合同/validator V1–V13/SF-L11+四分法/route 裁定表/双计数/机械化动词） |
| 3 | `wiki/survey/2026-07-15-sf-seed-manifest.jsonl` | `7cf761347223` | 变更（批次4 +5 = **92 条**,87 行前缀字节不变;TF-TTCL 转录失败 provenance 在案） |
| 4 | `wiki/survey/2026-07-15-sf-seed-manifest-report.md` | `011ec5aae6d2` | 变更（HISTORICAL_SUPERSEDED 范围标注——快照 51 审计件,现行正典=manifest+机器重数） |
| 5 | `wiki/survey/2026-07-15-sf-queries.jsonl` | `4cfd3b9063f0` | 变更（**55 行** = 53 行前缀字节不变 + SF-L11-Q1/Q2,sfqc-1.3.0） |
| 6 | `scripts/survey/sf_query_compiler.py` | `a869f816ed74` | 变更（四层版本,ADDITION_LANE_VERSIONS 表;SF-L11 = cs.MM/cs.MA） |
| 7 | `scripts/survey/sf_child_query_split.py` | `21422f672ca5` | 变更（P0-R2:`_year_windows` 实装/`parent_from_frozen_row` 适配器/`remaining_after`/`assert_unique_ids`;两类哈希机器分离） |
| 8 | `scripts/survey/sf_child_query_replay_test.py` + `docs/checks/2026-07-16-sf-child-query-replay-test.json` | `e8129113af14` / `ce71ae27af41` | 变更（三层合同期望:首 overflow=SPLIT_YEAR,**10/10 PASS**） |
| 9 | `scripts/survey/sf_child_query_realrow_dryrun.py` + `docs/checks/2026-07-16-sf-child-query-realrow-dryrun.json` | `e9b4201a51bb` / `91378a4f9691` | **新增**（P0-R2 核心验收:55/55 真实冻结行入规范函数,负例硬错误,**17/17 PASS**） |
| 10 | `scripts/survey/sf_record_validator.py` + `scripts/survey/sf_record_validator_test.py` + `docs/checks/2026-07-16-sf-record-validator-test.json` | `f7a7c55812e9` / `4e4326163af3` / `2b1b7c53651e` | **新增**（P0-R3:V1–V13 实装;负例子进程非零退出,**16/16 PASS**） |
| 10b | `wiki/survey/fixtures-c4a/`（15 件） | tree `d930f3c17184` | **新增**（正例 1 + 故意破坏负例 14;逐件 sha256 另钉于 record-validator-test 输出 fixture_sha256 段） |
| 11 | `wiki/survey/2026-07-16-sf-t1-routes-v2.jsonl` + `scripts/survey/sf_t1_routes_v2_gen.py` | `8e0a5d3ebcee` / `739be87e5c82` | **新增**（P0-R4 supersession:ACL-2026→READY〔唯一状态改判〕/ICML-2025 入口→v267〔唯一入口改判〕/逐行 status_audit_c4a;v1 保留不改写） |
| 11b | `scripts/survey/sf_t1_routes_validate.py` + `docs/checks/2026-07-16-sf-t1-routes-validation.json` | `cf5be69345eb` / `3efef48872c1` | 变更（active 输入自动取 v2,**12/12 PASS**） |
| 11c | `scripts/survey/sf_t1_routes_status_audit.py` + `docs/checks/2026-07-16-sf-t1-routes-status-audit.json` + `scripts/survey/probe_hosts_c4a.sh` | `694064a4a56c` / `6494ede500fd` / `aae93eff0a6f` | **新增**（当日外部审计证据件:39 URL 探针 200×28/404×3/403×1/CONN_FAIL×7,失败码逐行留痕;与结构 validator 分立） |
| 12 | `wiki/survey/2026-07-16-sf-sentinel-data.json` + `scripts/survey/sf_sentinel_recall_test.py` + `docs/checks/2026-07-16-sf-sentinel-recall.json` | `d5b09fd62ba6` / `79a16a3061f0` / `63b3d300a3b3` | 变更（P0-R5 四分法:21 哨兵 QUERY_HIT×14/SEED×7/**UNRESOLVED×0**;两 held-out 纯查询召回,VQQA×5 验证 SF-L11;coverage_note 仅注释） |
| 13 | `scripts/survey/sf_package_summary.py` + `docs/checks/2026-07-16-sf-package-summary.json` | `6d985c84662b` / `55a66d9df0e8` | **新增**（机械化状态动词 + stale-token 扫描 + 机器重数;八项全 PASS） |
| 14 | `wiki/survey/2026-07-15-sf-blank-templates.md` | `4334a7ef72ea` | 变更（split_level 增 YEAR;NA 类型稳定对象;INCLUDED⇒reason_code=null;validator 实装引用） |
| 15 | `wiki/survey/README.md` | `8b8faa70e8b1` | 变更（REC-0..REC-7 编号纪律更新） |
| 16 | `wiki/survey/2026-07-16-sf-access-log-c4a-review-verification.jsonl` | `483538082912` | **新增**（26 行 append-only:评审引文核验 7/7 HIT + verbatim 摘要 7 + venue 状态 3+8;新 access class 如实披露待追认→amendment-5 §6 已注册） |
| 17 | `wiki/survey/2026-07-16-gate-s1-correction-4a-response.md` | `96886f96c8f3` | **新增**（回应信:核验先行/完成态收回/两点分层陈述/机器清单/owner 三裁决/P0-R8 申请） |
| 18 | `wiki/2026-07-16-gate-s1-correction-4-prelaunch-doctoral-review.md` | `028dfc1b20a3` | **新增**（触发评审件入库,provenance） |
| 19 | `wiki/Decision-Log.md` | `6f179510f1cb` | 变更（**续62**:owner 三裁决 + P0-R7 token 退役语义澄清 dated supersession） |
| 20 | `wiki/Research-Objective.md` | `a0b80eea994d` | 变更（热层 last_refresh + gate 状态段更新至 correction #4A） |

敌意环（C4A）：机械镜头（compiler+五脚本 WSL venv 复跑全 PASS/前缀 53 字节证明/append-only
diff 核验 queries+2 seeds+5）+ 语义镜头（跨件数字口径交叉核对）R1 = 1 finding（「47 探针」
应为 39 URL 探针——amendment-5/回应信两处）→ 修复 → R2 复检清零。**attestation**：
`discovery_queries_executed = 0` 维持;双计数正典 = amendment-5 §6。**下一动作**：以回应信为
封面请 reviewer 执行 P0-R8 窄幅复核（双向合同维持:0 新 MAJOR/0 新 MINOR + 旧项 evidence
locator 可重放即签署）。

## dated correction #4B（2026-07-17,P0-R8 再复审 3 MAJOR + 2 MINOR 整改批——钉定基准 commit = 待 stage-2 追加）

（触发 = 《Gate S1 P0-R8 窄幅博士生导师式对抗复审》WITHHOLD;owner 四点裁决 = Decision-Log
续63。哈希正典 = git blob,两段提交制:本段（stage-1）钉路径与机器基数,blob 钉定表由 stage-2
提交追加于本段末——**基数机器对账取代手数**（P0-R8 的 31-vs-33 教训）。计数语义:`files` =
下表逐件枚举的非树成员;`fixtures` = `wiki/survey/fixtures-c4b/` 树内 json 件数;`atom_xml` =
atom 树内件数;**本表「变更/新增」行 ∪ 两树 = 本批 git 变更集**（「不变」行为字节级确定性
重生成一致件,不入 diff）。）

MACHINE_COUNT: files=36 fixtures=26 atom_xml=26

| # | path | 变更说明 |
|---|---|---|
| 1 | `wiki/survey/2026-07-15-system-first-survey-protocol-v1.md` | 变更（§4 增 SF-L12/SF-L13 受控道各 Q1..Q3;正典口径 61 查询,历史口径链「55」入 C4A 段） |
| 2 | `wiki/survey/2026-07-15-sf-queries.jsonl` | 变更（**61 行** = 55 行前缀字节不变 + L12/L13 各三行,sfqc-1.4.0;prefix55 哈希钉于 canon） |
| 3 | `wiki/survey/2026-07-16-sf-sentinel-data.json` | 变更（**26 哨兵** = 21 + TimeLogic/Seg-Agent/2602.21497/2505.18079/2605.11374;`abstract`→`source_normalized_abstract`;逐条 atom provenance;VQQA/MAR3 P0-3.2 声称更正） |
| 4 | `wiki/survey/2026-07-17-sf-t1-routes-v3.jsonl` | **新增**（dated supersession:ICASSP-2023..2026 evidence_tier A→C 更正,自查披露 amendment-6 §3.8;v2 不改写） |
| 5 | `wiki/survey/2026-07-17-sf-canon.json` | **新增**（P0-1.1 期望值单一正典:92/61/50/26/5+前缀哈希+类目并集+版本分层+producer 清单+禁词表） |
| 6 | `wiki/survey/2026-07-17-sf-protocol-amendment-6.md` | **新增**（C4B gate 整改合同全文:P0-1..P0-4+owner 裁决登记+访问类注册） |
| 7 | `wiki/survey/2026-07-17-sf-protocol-amendment-7.md` | **新增**（执行期合同:退出机制 E1–E3/全文强制细则/时代优先级/校准实验登记——**非 gate 阻断项**） |
| 8 | `wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl` | **新增**（26 哨兵全文双份采集台账,append-only;正文存数据盘不进 git） |
| 9 | `wiki/survey/2026-07-17-sf-access-log-c4b.jsonl` | **新增**（本批联网活动双计数总账:1 header + 12 seq 行,代理检索词逐字登记;discovery=0） |
| 10 | `wiki/survey/2026-07-17-gate-s1-correction-4b-response.md` | **新增**（回应信+P0-R9 申请:核验先行/全盘接受/两处措辞精确重述/复跑表） |
| 11 | `scripts/survey/sf_query_compiler.py` | 变更（ADDITION_LANES 增 L12/L13 各 [1,2,3],sfqc-1.4.0;61/61 静态验证） |
| 12 | `scripts/survey/sf_record_validator.py` | 变更（**v2:V1–V15**——双向一一 lineage/V14 种子联结 fail-closed/内层 schema 枚举正典/V15 单正典位/后缀与类型稳健,P0-2 全项） |
| 13 | `scripts/survey/sf_record_validator_test.py` | 变更（v2:fixtures-c4b 子进程级 26/26） |
| 14 | `scripts/survey/sf_fixtures_c4b_gen.py` | **新增**（负例生成器:25 个命名 mutation 函数 = 负例文档;含评审三组对抗 fixture） |
| 15 | `scripts/survey/sf_sentinel_recall_test.py` | 变更（source_normalized_abstract/atom 哈希核验/BOUNDARY_REG 强校验/held-out era≥2025 机器强制/routes v3 优先） |
| 16 | `scripts/survey/sf_package_summary.py` | 变更（**v2 fail-closed**:canon 精确计数/前缀哈希/八 producer 隔离重跑字节比对/collector 降格 EVIDENCE_PRESENT/manifest MACHINE_COUNT 对账/occurrence 级豁免/缺文件=FAIL,P0-1 全项） |
| 17 | `scripts/survey/sf_package_summary_test.py` | **新增**（P0-1.5 mutation harness:基线绿+7 变异全非零退出+P0-4.3 boundary 一正一负） |
| 18 | `scripts/survey/sf_t1_routes_adjudication_validate.py` | **新增**（P0-1.3 独立裁定层:R1–R7 逐 route 对齐,50×50） |
| 19 | `scripts/survey/sf_t1_routes_v3_gen.py` | **新增**（v3 生成器:四行 tier 更正+record_sha256 重算,更正注记内嵌） |
| 20 | `scripts/survey/sf_t1_routes_validate.py` | 变更（active 输入 v3 优先） |
| 21 | `scripts/survey/sf_atom_provenance_fetch.py` | **新增**（raw Atom 采集器:export 端点/≥3s/退避/append-only 台账） |
| 22 | `scripts/survey/sf_fulltext_fetch.py` | **新增**（全文双份采集器:PDF+e-print→数据盘,台账入 git;含 /mnt/<drive> 路径翻译防误落盘） |
| 22b | `scripts/survey/sf_citation_calibration.py` | **新增**（amendment-7 §4.1 预注册校准实验:Seg-Agent 参考文献 × 存量论文集求交,离线确定性） |
| 23 | `docs/checks/2026-07-16-sf-package-summary.json` | 变更（v2 门禁输出:13 项清单,含 EVIDENCE_PRESENT 语义与 counts expected/got 并列） |
| 24 | `docs/checks/2026-07-16-sf-record-validator-test.json` | 变更（26/26,fixture sha256 逐件钉定） |
| 25 | `docs/checks/2026-07-16-sf-sentinel-recall.json` | 变更（26 哨兵:QUERY_HIT 23/SEED 3/UNRESOLVED 0;held-out 5 全纯查询召回） |
| 26 | `docs/checks/2026-07-16-sf-child-query-replay-test.json` | 不变（61 行输入下重生成字节一致——确定性旁证） |
| 27 | `docs/checks/2026-07-16-sf-child-query-realrow-dryrun.json` | 变更（**61/61** 真实冻结行零 KeyError,17/17） |
| 28 | `docs/checks/2026-07-16-sf-t1-routes-validation.json` | 变更（输入切 v3,12/12） |
| 29 | `docs/checks/2026-07-16-sf-t1-routes-adjudication.json` | **新增**（PASS,0 violations;曾于 v2 输入下抓到 4 条 tier 失实——触发 v3） |
| 30 | `docs/checks/2026-07-17-sf-package-summary-mutations.json` | **新增**（harness 输出:基线+7 变异+boundary 对） |
| 31 | `docs/checks/2026-07-17-sf-citation-calibration-segagent.json` | **新增**（amendment-7 §4.1 预注册校准实验结果） |
| 32 | `docs/survey-provenance/atom-ledger.jsonl` | **新增**（27 行:26 成功+1 次 TLS 瞬断如实留痕） |
| 33 | `wiki/2026-07-16-gate-s1-p0r8-rereview-doctoral-review.md` | **新增**（触发评审件入库,provenance） |
| 34 | `wiki/Decision-Log.md` | 变更（**续63**:owner 四点裁决 + C4B 整改批登记,append-only） |
| 35 | `wiki/Research-Objective.md` | 变更（热层 last_refresh + gate 状态段更新至 correction #4B） |
| 树A | `wiki/survey/fixtures-c4b/`（26 件 = 1 正例 + 25 负例） | **新增**（逐件 sha256 钉于 record-validator-test 输出 fixture_sha256 段） |
| 树B | `docs/survey-provenance/atom/`（26 件 raw Atom XML） | **新增**（逐件 sha256 钉于 sentinel 数据 atom_sha256 字段 + atom-ledger 逐行） |

（stage-2 blob 钉定表追加于此段末;核验 `git rev-parse <stage-1 commit>:<path>`。）
