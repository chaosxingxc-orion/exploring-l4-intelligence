#!/usr/bin/env bash
set -euo pipefail

# Exact-ID Stage-1C paper acquisition. Full texts stay outside Git.
DATA_ROOT="${SPEECHRL_DATA_DIR:-/mnt/e/chao_workspace/exploring-l4-intelligence/speechrl-data}"

ASSETS=(
  "2026.findings-eacl.151|pdf|https://aclanthology.org/2026.findings-eacl.151.pdf|da6a78305f6f62dcf38a88b4f2d3a9be93001c3d5591ee621dae6463cffc153c"
  "2026.acl-long.1615|pdf|https://aclanthology.org/2026.acl-long.1615.pdf|081805a63ca2ef8fa04b1378d6aa2cda86b904d3cf9ccd5f0d496593df86a6b1"
  "2508.18240|pdf|https://arxiv.org/pdf/2508.18240|e5f0b89106fc1471cb0cd96e3c0a5d93067eb4a857558484b74bd1b9231b3e95"
  "2508.18240|eprint|https://arxiv.org/e-print/2508.18240|b1b7446ab39129154a027d92c8238be359ad0941bdae9af466576117c01ad7c7"
  "2603.16924|pdf|https://arxiv.org/pdf/2603.16924|66421173cd988f1e83c49a395cbb37ec186b779c30171976c566e698c2c0480b"
  "2603.16924|eprint|https://arxiv.org/e-print/2603.16924|157982078e822089cd7c5f279b0dbd1cd9038df3f38ff9de053bbb3297db53fd"
)

if [[ "${1:-}" == "--list" ]]; then
  printf '%s\n' "${ASSETS[@]}"
  exit 0
fi

for row in "${ASSETS[@]}"; do
  IFS='|' read -r identity kind url expected_sha <<<"$row"
  destination_dir="$DATA_ROOT/survey-fulltext/$identity"
  destination="$destination_dir/$identity.$kind"
  mkdir -p "$destination_dir"

  if [[ -s "$destination" ]]; then
    actual_sha="$(sha256sum "$destination" | awk '{print $1}')"
    if [[ "$actual_sha" == "$expected_sha" ]]; then
      printf '[SKIP] %s %s hash verified\n' "$identity" "$kind"
      continue
    fi
    printf '[FAIL] existing file hash mismatch: %s\n' "$destination" >&2
    exit 1
  fi

  temporary="$destination.part.$$"
  if command -v aria2c >/dev/null 2>&1; then
    aria2c -x 8 -s 8 --file-allocation=none --allow-overwrite=true \
      --dir="$destination_dir" --out="$(basename "$temporary")" "$url"
  else
    curl -L --fail --silent --show-error --max-time 300 -o "$temporary" "$url"
  fi

  actual_sha="$(sha256sum "$temporary" | awk '{print $1}')"
  if [[ "$actual_sha" != "$expected_sha" ]]; then
    rm -f -- "$temporary"
    printf '[FAIL] downloaded hash mismatch: %s %s\n' "$identity" "$kind" >&2
    exit 1
  fi
  mv -- "$temporary" "$destination"
  printf '[OK] %s %s\n' "$identity" "$kind"
done
