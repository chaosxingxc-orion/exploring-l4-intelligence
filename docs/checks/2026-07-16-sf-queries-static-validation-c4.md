# sf-queries 静态验证（correction #4 版,2026-07-16）

**链条（C4-6 后现行终态）**：协议 md（sha256 `a0b2a0171a4e60177c923c7597176843ed07bab72c71d7e4139cade43daf54e9`）
→ 编译器 `scripts/survey/sf_query_compiler.py`（sfqc-1.0.0/1.1.0/**1.2.0** 三层,sha256
`94e76681a040131e83b6980130159f00d0856c68fe9ce9baa5ca4cc0fe657668`）
→ `wiki/survey/2026-07-15-sf-queries.jsonl` **53 行**（sha256
`75a59b2bf5ca621c8d044befdd711d4a4a82ef768948808d79ad1ce6278be740`）。

**append-only 证明**：
- 前 51 行 sha256 = `4e40658010d89833878e1f353a4975db5f86a52547f0fd10adbf093cf054a5e9`
- 提交前 HEAD 全文件 sha256 = `4e40658010d89833878e1f353a4975db5f86a52547f0fd10adbf093cf054a5e9`
- 两者逐字节一致：**True**（51 行原批零改写;SF-L10-Q1/Q2 追加于末尾,标 sfqc-1.2.0）

**编译器静态验证**：13/13 PASS（`python scripts/survey/sf_query_compiler.py` 可复跑;
row_count=53 / 唯一性 / 零占位符 / 括号引号平衡 / 运算符大写 / 日期良构 / 每 lane 计数
{L1:8,L2:6,L3:7,L4:6,L5:6,L6:6,L7:6,L8:6,L10:2} / 类目映射 / 例外规则 / 行哈希自洽 /
版本分层 / 输出顺序）。

**SF-L10 语义**：cs.SE+cs.HC 受控类目道(C4-6);道名跳过 SF-L9(已被基础谱系道占用,收词纪律)。
本文件取代 `2026-07-16-sf-queries-static-validation-rerun.md` 的链条职能（该件保留为 51 条
时期历史终态）。
