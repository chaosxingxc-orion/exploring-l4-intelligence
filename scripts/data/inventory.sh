#!/usr/bin/env bash
# Delegating shim -> scripts/data/fetch-assets.sh inventory "$@" (logic merged 2026-07-29; see fetch-assets.sh header + README).
exec bash "$(dirname "$0")/fetch-assets.sh" inventory "$@"
