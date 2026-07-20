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
case "$#" in
  0) ;;
  1)
    if [[ "$1" == "--dry-run" ]]; then
      DRY_RUN=1
    else
      echo "ERROR: unsupported argument; expected no arguments or exact --dry-run" >&2
      exit 2
    fi
    ;;
  *)
    echo "ERROR: unsupported arguments; expected no arguments or exact --dry-run" >&2
    exit 2
    ;;
esac

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC_DIR="$REPO_ROOT/wiki"
WORK_DIR="$REPO_ROOT/.wiki-tmp"   # gitignored working clone of the wiki repo

[[ "$WORK_DIR" == "$REPO_ROOT/.wiki-tmp" && "$REPO_ROOT" == /* ]] || {
  echo "ERROR: unsafe wiki temporary path: $WORK_DIR" >&2
  exit 1
}

cleanup_work_dir() {
  rm -rf -- "$WORK_DIR"
}

if [[ "$DRY_RUN" == "1" ]]; then
  trap cleanup_work_dir EXIT
fi

[[ -d "$SRC_DIR" ]] || { echo "ERROR: wiki source dir not found: $SRC_DIR" >&2; exit 1; }

REPO_GIT_ARGS=()
DOT_GIT="$REPO_ROOT/.git"
if [[ -d "$DOT_GIT" ]]; then
  REPO_GIT_ARGS=(-C "$REPO_ROOT")
elif [[ -f "$DOT_GIT" ]]; then
  mapfile -t GIT_POINTER_LINES < "$DOT_GIT"
  [[ "${#GIT_POINTER_LINES[@]}" == "1" ]] || {
    echo "ERROR: malformed linked-worktree .git pointer" >&2
    exit 1
  }
  GIT_POINTER="${GIT_POINTER_LINES[0]%$'\r'}"
  [[ "$GIT_POINTER" == "gitdir: "* ]] || {
    echo "ERROR: malformed linked-worktree .git pointer" >&2
    exit 1
  }
  GIT_DIR_PATH="${GIT_POINTER#gitdir: }"
  if [[ "$GIT_DIR_PATH" =~ ^([A-Za-z]):[\\/](.*)$ && -d "/mnt/${BASH_REMATCH[1],,}" ]]; then
    GIT_DIR_PATH="/mnt/${BASH_REMATCH[1],,}/${BASH_REMATCH[2]//\\//}"
  elif [[ "$GIT_DIR_PATH" != /* && ! "$GIT_DIR_PATH" =~ ^[A-Za-z]:[\\/] ]]; then
    GIT_DIR_PATH="$REPO_ROOT/$GIT_DIR_PATH"
  fi
  [[ -d "$GIT_DIR_PATH" ]] || {
    echo "ERROR: linked-worktree gitdir not found: $GIT_DIR_PATH" >&2
    exit 1
  }
  GIT_DIR_PATH="$(cd "$GIT_DIR_PATH" && pwd -P)"
  REPO_GIT_ARGS=(--git-dir="$GIT_DIR_PATH" --work-tree="$REPO_ROOT")
else
  echo "ERROR: repository metadata not found: $DOT_GIT" >&2
  exit 1
fi

repo_git() {
  command git "${REPO_GIT_ARGS[@]}" "$@"
}

ORIGIN="$(repo_git remote get-url origin)"
WIKI_URL="${ORIGIN%.git}.wiki.git"
echo "Wiki remote: $WIKI_URL"

# Always start from a clean working clone (avoids stale-state wedging across runs).
cleanup_work_dir
FRESH=0
CLONE_ERR=""
if CLONE_ERR="$(git clone "$WIKI_URL" "$WORK_DIR" 2>&1)"; then
  :   # cloned an existing, initialized wiki
elif ! grep -qiE 'repository .*not found|not found' <<<"$CLONE_ERR"; then
  # 2026-07-15: a transient network/TLS failure used to be misread as "wiki not
  # initialized", sending the script down the fresh-init path whose push is then
  # rejected by the existing remote. Fail fast instead; only a genuine
  # repository-not-found takes the first-time-init path below.
  echo "ERROR: wiki clone failed (network?): $CLONE_ERR" >&2
  exit 1
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
git config user.name  "$(repo_git config user.name  2>/dev/null || echo 'wiki-sync')"
git config user.email "$(repo_git config user.email 2>/dev/null || echo 'wiki-sync@local')"
git config core.autocrlf false

if [[ -z "$(git status --porcelain)" ]]; then
  echo "Wiki already up to date — nothing to sync."
  if [[ "$DRY_RUN" == "1" ]]; then
    echo "[dry-run] not committing or pushing."
  fi
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
git commit -m "Sync wiki from repo wiki/ ($(repo_git rev-parse --short HEAD))"
if [[ "$FRESH" == "1" ]]; then
  git push -u origin master
else
  git push
fi
echo "Wiki published: ${ORIGIN%.git}/wiki"
