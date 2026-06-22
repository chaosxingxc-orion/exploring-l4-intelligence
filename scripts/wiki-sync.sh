#!/usr/bin/env bash
# Sync wiki/ (the source of truth) -> the GitHub Wiki repo (<repo>.wiki.git).
#
# Usage:
#   bash scripts/wiki-sync.sh            # publish: clone/pull wiki, copy wiki/*.md, commit, push
#   bash scripts/wiki-sync.sh --dry-run  # clone/pull + show the diff, do NOT commit or push
#
# Notes:
#   - Edit pages in wiki/*.md (reviewed via normal git/PRs); this script mirrors them to the wiki.
#   - wiki/README.md is repo-facing meta and is NOT published as a wiki page.
#   - The wiki remote is derived from `origin`: .../repo(.git) -> .../repo.wiki.git
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

# Clone an existing wiki, refresh it, or first-time-init an empty one via push.
FRESH=0
if [[ -d "$WORK_DIR/.git" ]]; then
  git -C "$WORK_DIR" pull --ff-only || true
elif git clone "$WIKI_URL" "$WORK_DIR" 2>/dev/null; then
  :   # cloned an existing, initialized wiki
else
  echo "Wiki not cloneable yet — attempting first-time init via push."
  echo "(If the push fails: enable Settings -> Features -> Wikis, create the first page"
  echo " once in the web UI to initialize the repo, then re-run this script.)"
  rm -rf "$WORK_DIR"; mkdir -p "$WORK_DIR"
  git -C "$WORK_DIR" init -q
  git -C "$WORK_DIR" remote add origin "$WIKI_URL"
  git -C "$WORK_DIR" checkout -q -B master
  FRESH=1
fi

# Mirror top-level *.md from source (except README.md), pruning pages dropped from source.
find "$WORK_DIR" -maxdepth 1 -name '*.md' -delete
for f in "$SRC_DIR"/*.md; do
  base="$(basename "$f")"
  [[ "$base" == "README.md" ]] && continue
  cp "$f" "$WORK_DIR/"
done

cd "$WORK_DIR"
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
