# `wiki/` — source for the GitHub Wiki

This folder is the **source of truth** for the GitHub Wiki. Edit Markdown here (reviewed via normal
git/PRs), then publish with `bash scripts/wiki-sync.sh`, which pushes to
`exploring-l4-intelligence.wiki.git`. **Don't edit only on the web Wiki** — it will drift from here.

**Conventions**

- GitHub-wiki filename rules: `Home.md` is the landing page; page titles use hyphens
  (`Working-Mode.md` → "Working Mode"); `_Sidebar.md` / `_Footer.md` are special navigation files.
- Cross-link pages with `[[Page-Name]]`.
- Bilingual & grouped: an English block first, then a `## 中文` block — never line-by-line
  interleaving, and never duplicate code/commands/tables.

**Pages**: `Home`, `Architecture`, `Environment-and-Setup`, `Working-Mode`, `Per-Work-Status`,
`Data-and-Assets`, `AI-Collaboration`, `Onboarding`, `Decision-Log` (+ `_Sidebar`, `_Footer`).

---

## 中文

这个目录是 GitHub Wiki 的**源文件（source of truth）**。在这里改 Markdown、走正常的 git / PR 评审，
然后运行 `bash scripts/wiki-sync.sh` 推送到 `exploring-l4-intelligence.wiki.git`。**不要只在网页版
Wiki 上改**，否则会和这里不同步。

约定：GitHub-wiki 文件名规则（`Home.md` 是首页；标题用连字符；`_Sidebar.md` / `_Footer.md` 是导航
文件）；页面间用 `[[Page-Name]]` 互链；双语分块——先英文整块，再 `## 中文` 整块，不逐行交替，也不重复
代码/命令/表格。
