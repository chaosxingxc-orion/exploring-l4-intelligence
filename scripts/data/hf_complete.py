#!/usr/bin/env python3
"""Diff an HF dataset repo against a local directory and emit an aria2c input list for the gaps.

Why this exists: HuggingFace migrated many repos to the **Xet** content-addressed backend, whose
presigned CDN URLs are *byte-range-locked* (the `Policy` carries a `ByteRange` condition). aria2c's
multi-connection range-splitting (`-x>1` / `split>1`) then requests ranges the signature doesn't
authorize -> HTTP 403 on nearly every chunk. The fix is to fetch each file with a SINGLE connection
(no range split) and get throughput from **file-level** parallelism (`aria2c -j`). This tool writes a
list in exactly that shape (`split=1`, `max-connection-per-server=1` per entry).

It also makes completeness *verifiable*: a file counts as present only if it exists locally AND its
size matches the repo's metadata, so truncated/partial files are re-listed as gaps. Run it again after
downloading to prove 0 gaps remain.

Usage:  python hf_complete.py <repo_id> <dest_dir> <out_list>   [repo_type defaults to 'dataset']
Metadata listing goes through $HF_ENDPOINT (hf-mirror.com by default), which proxies the HF *API*
fine — only the Xet *CAS* download is unreachable from CN, which is why aria2c (not the python client)
does the actual fetch. Prints one machine-readable SUMMARY line to stderr.
"""
import os
import sys
from huggingface_hub import HfApi

repo, dest, out_list = sys.argv[1], sys.argv[2], sys.argv[3]
repo_type = sys.argv[4] if len(sys.argv) > 4 else "dataset"
endpoint = os.environ.get("HF_ENDPOINT", "https://hf-mirror.com")
api = HfApi(endpoint=endpoint)

total = have = 0
total_bytes = have_bytes = miss_bytes = 0
missing = []  # (path, size)
try:
    for e in api.list_repo_tree(repo, repo_type=repo_type, recursive=True):
        size = getattr(e, "size", None)
        if size is None:              # RepoFolder -> skip
            continue
        total += 1
        total_bytes += size
        local = os.path.join(dest, e.path)
        try:
            ok = os.path.getsize(local) == size
        except OSError:
            ok = False
        if ok:
            have += 1
            have_bytes += size
        else:
            missing.append((e.path, size))
            miss_bytes += size
except Exception as ex:               # noqa: BLE001 — surface any listing failure to the caller
    sys.stderr.write(f"SUMMARY repo={repo} ERROR list_repo_tree: {ex}\n")
    sys.exit(3)

with open(out_list, "w", encoding="utf-8") as f:
    for path, _ in missing:
        url = f"{endpoint}/datasets/{repo}/resolve/main/{path}" if repo_type == "dataset" \
            else f"{endpoint}/{repo}/resolve/main/{path}"
        d = os.path.dirname(path)
        f.write(url + "\n")
        if d:
            f.write(f"  dir={d}\n")
        f.write(f"  out={os.path.basename(path)}\n")
        f.write("  split=1\n  max-connection-per-server=1\n")

sys.stderr.write(
    f"SUMMARY repo={repo} total_files={total} total_GB={total_bytes/1e9:.2f} "
    f"have={have} missing={len(missing)} missing_GB={miss_bytes/1e9:.2f}\n"
)
