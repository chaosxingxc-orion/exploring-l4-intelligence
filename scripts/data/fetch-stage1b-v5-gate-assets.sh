#!/usr/bin/env bash
# Fetch only the bounded, public Stage-1B v5 gate assets through the unified downloader.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${SPEECHRL_WORKSPACE:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
export SPEECHRL_LOCKFILE="$WORKSPACE/docs/stage1b-v5-gate-assets.lock.json"

exec bash "$SCRIPT_DIR/fetch-data.sh" "$@"
