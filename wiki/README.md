# `wiki/` — source for the GitHub Wiki

This folder is the **source of truth** for the GitHub Wiki. Edit Markdown here (reviewed via normal
git/PRs), then publish with `bash scripts/wiki-sync.sh`, which pushes to
`exploring-l4-intelligence.wiki.git`. **Don't edit only on the web Wiki** — it will drift from here.

**Conventions**

- GitHub-wiki filename rules: `Home.md` is the landing page; page titles use hyphens
  (`Working-Mode.md` → "Working Mode"); `_Sidebar.md` / `_Footer.md` are special navigation files.
- Cross-link pages with `[[Page-Name]]`.
- English only. Every page is authored in English; the former bilingual block convention was
  retired on 2026-08-15 in favour of the program's English-only first principle, and
  `scripts/checks/ai_context_surface_check.py` now fails closed on any CJK character in an
  active page.

**Pages**: `Home`, `Architecture`, `Environment-and-Setup`, `Working-Mode`, `Per-Work-Status`,
`Data-and-Assets`, `AI-Collaboration`, `Onboarding`, `Decision-Log` (+ `_Sidebar`, `_Footer`).
