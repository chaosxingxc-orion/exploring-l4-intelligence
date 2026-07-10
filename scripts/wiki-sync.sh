#!/usr/bin/env bash
# Sync wiki/ (the source of truth) -> the GitHub Wiki repo (<repo>.wiki.git).
#
# Usage:
#   bash scripts/wiki-sync.sh            # publish: clone/pull wiki, copy wiki/**/*.md, commit, push
#   bash scripts/wiki-sync.sh --dry-run  # clone/pull + show the diff, do NOT commit or push
#
# Notes:
#   - Edit pages in wiki/**/*.md (reviewed via normal git/PRs); this script mirrors them to the wiki.
#   - wiki/README.md (top-level only) is repo-facing meta and is NOT published as a wiki page.
#     Subdirectory README.md files (e.g. wiki/survey/README.md) ARE real index pages and DO publish.
#   - The wiki remote is derived from `origin`: .../repo(.git) -> .../repo.wiki.git
#
# 2026-07-11 (RR-013 remediation): this script previously only mirrored TOP-LEVEL
# wiki/*.md (`find -maxdepth 1 ...; for f in "$SRC_DIR"/*.md`). That silently
# dropped every subdirectory from the published wiki — wiki/survey/ (the active
# Step-2 survey index + working docs) and wiki/archive/survey/<campaign>/ (51
# pages archived out of the top level on 2026-07-11) never reached the GitHub
# Wiki. Worse: because $WORK_DIR is always a *fresh* clone that gets fully
# repopulated from $SRC_DIR each run, and the old deletion phase also only
# looked at maxdepth 1, a sync run right after the 2026-07-11 archive move would
# have deleted the wiki-remote copies of the 8 pages relocated out of the top
# level with nothing at any depth to replace them — silent data loss on the
# published wiki. Fixed: mirror the full *.md tree (preserving subpaths) and
# prune stale pages at any depth (excluding .git) before repopulating.
set -euo pipefail

DRY_RUN=0
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=1

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC_DIR="$REPO_ROOT/wiki"
WORK_DIR="$REPO_ROOT/.wiki-tmp"   # gitignored working clone of the wiki repo

[[ -d "$SRC_DIR" ]] || { echo "ERROR: wiki source dir not found: $SRC_DIR" >&2; exit 1; }

ORIGIN="$(git -C "$REPO_ROOT" remote get-url origin)"
WIKI_URL="${ORIGIN%.git}.wiki.git"
echo "Wiki remote: $WIKI_URL"

# Always start from a clean working clone (avoids stale-state wedging across runs).
rm -rf "$WORK_DIR"
FRESH=0
if git clone "$WIKI_URL" "$WORK_DIR" 2>/dev/null; then
  :   # cloned an existing, initialized wiki
else
  echo "Wiki not cloneable yet — attempting first-time init via push."
  echo "(If the push fails with 'Repository not found': enable Settings -> Features -> Wikis,"
  echo " then create the first page once in the web UI to initialize the repo, and re-run.)"
  mkdir -p "$WORK_DIR"
  git -C "$WORK_DIR" init -q
  git -C "$WORK_DIR" remote add origin "$WIKI_URL"
  git -C "$WORK_DIR" checkout -q -B master
  FRESH=1
fi

# Mirror the FULL *.md tree from source (except top-level README.md), preserving
# subpaths (survey/, archive/, archive/survey/<campaign>/, ...), and pruning any
# stale page at any depth that was dropped from source. $WORK_DIR is always a
# fresh clone (see above), so this delete+repopulate pair fully reproduces
# $SRC_DIR's tree in the wiki working copy on every run.
find "$WORK_DIR" -name '*.md' -not -path "$WORK_DIR/.git/*" -delete
while IFS= read -r -d '' f; do
  rel="${f#"$SRC_DIR"/}"
  [[ "$rel" == "README.md" ]] && continue   # top-level README.md only: repo-facing meta, not a page
  dest="$WORK_DIR/$rel"
  mkdir -p "$(dirname "$dest")"
  cp "$f" "$dest"
done < <(find "$SRC_DIR" -name '*.md' -print0)

cd "$WORK_DIR"
# This is a throwaway clone: borrow the umbrella's commit identity and pin line endings
# (the wiki repo has no .gitattributes, so avoid LF->CRLF churn).
git config user.name  "$(git -C "$REPO_ROOT" config user.name  2>/dev/null || echo 'wiki-sync')"
git config user.email "$(git -C "$REPO_ROOT" config user.email 2>/dev/null || echo 'wiki-sync@local')"
git config core.autocrlf false

if [[ -z "$(git status --porcelain)" ]]; then
  echo "Wiki already up to date — nothing to sync."
  exit 0
fi

echo "----- changes -----"
git --no-pager diff --stat || true
git status --porcelain

if [[ "$DRY_RUN" == "1" ]]; then
  echo "[dry-run] not committing or pushing."
  exit 0
fi

git add -A
git commit -m "Sync wiki from repo wiki/ ($(git -C "$REPO_ROOT" rev-parse --short HEAD))"
if [[ "$FRESH" == "1" ]]; then
  git push -u origin master
else
  git push
fi
echo "Wiki published: ${ORIGIN%.git}/wiki"
