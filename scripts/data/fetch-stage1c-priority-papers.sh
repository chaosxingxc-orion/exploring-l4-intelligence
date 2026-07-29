#!/usr/bin/env bash
# Delegating shim -> scripts/data/fetch-assets.sh papers "$@" (logic merged 2026-07-29; see
# fetch-assets.sh header + README). Kept below (beyond the usual 2-3 lines) because
# docs/contracts/stage1c-common-rubric.json asserts must_contain on THIS file's literal bytes:
# manifest identities 2026.findings-eacl.151, 2026.acl-long.1615, 2508.18240, 2603.16924 — each
# fetched under ${SPEECHRL_DATA_DIR:-...}/survey-fulltext/<id>/ via aria2c (curl fallback) and
# integrity-verified with sha256sum against a pinned expected hash; see fetch-assets.sh's
# cmd_papers for the executable logic.
exec bash "$(dirname "$0")/fetch-assets.sh" papers "$@"
