#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Seg-Agent citation-calibration experiment (amendment-7 §4.1, pre-registered).

Question: does Seg-Agent 2605.12953 — a HIGH-confidence in-object paper that the
frozen queries initially missed — cite ANY paper in our current stock (92 seeds
∪ 26 sentinels)? Pre-registered prediction: intersection = ∅ (cross-community
lineage cites the SAM/SoM family), which would be the empirical exhibit that the
owner's citation-overlap screen must remain an EXIT/relevance layer and can
never be the sole DISCOVERY channel (exit mechanism E2 vs BFS separation).

Method (offline, deterministic given the archived e-print):
  1. read the archived e-print (tar.gz / gzipped TeX) from the fulltext store;
  2. extract every .bbl/.bib/.tex member and collect bibliography text
     (\\bibitem blocks + @entries);
  3. regex-harvest arXiv IDs (NNNN.NNNNN with optional version);
  4. intersect with seed-manifest IDs ∪ sentinel IDs.

Run from repo root:
  python scripts/survey/sf_citation_calibration.py [--eprint PATH]
Persists docs/checks/2026-07-17-sf-citation-calibration-segagent.json. Exit 0
iff the experiment RAN (either verdict); exit 1 only on missing/unreadable input.
"""
import gzip
import io
import json
import os
import re
import sys
import tarfile

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGET = "2605.12953"
SEEDS = os.path.join(REPO, "wiki", "survey", "2026-07-15-sf-seed-manifest.jsonl")
SENTINELS = os.path.join(REPO, "wiki", "survey", "2026-07-16-sf-sentinel-data.json")
OUT = os.path.join(REPO, "docs", "checks",
                   "2026-07-17-sf-citation-calibration-segagent.json")
ARXIV_ID_RE = re.compile(r"\b(\d{4}\.\d{4,5})(?:v\d+)?\b")


def _normalize_data_root(p):
    """SPEECHRL_DATA_DIR is persisted as a WSL path (/mnt/e/...). Under Windows
    Python it arrives either verbatim or MSYS-mangled to
    <git-root>/mnt/e/... — both forms are translated to E:/..."""
    m = re.search(r"[/\\]mnt[/\\]([a-z])[/\\](.*)$", p or "")
    return f"{m.group(1).upper()}:/{m.group(2)}" if m else p


DEFAULT_EPRINT = os.path.join(
    _normalize_data_root(os.environ.get(
        "SPEECHRL_DATA_DIR",
        "E:/chao_workspace/exploring-l4-intelligence/speechrl-data")),
    "survey-fulltext", TARGET, f"{TARGET}.eprint")


def extract_text_members(blob):
    """Return {name: text} for every .tex/.bbl/.bib member of a tar.gz or a
    single gzipped file."""
    members = {}
    try:
        with tarfile.open(fileobj=io.BytesIO(blob), mode="r:*") as tf:
            for m in tf.getmembers():
                if m.isfile() and re.search(r"\.(tex|bbl|bib)$", m.name, re.I):
                    members[m.name] = tf.extractfile(m).read().decode(
                        "utf-8", errors="replace")
        return members
    except tarfile.TarError:
        pass
    try:
        members["(gzipped-single-file)"] = gzip.decompress(blob).decode(
            "utf-8", errors="replace")
    except OSError:
        members["(raw-bytes-as-text)"] = blob.decode("utf-8", errors="replace")
    return members


def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = dict(zip(argv[1::2], argv[2::2]))
    eprint_path = args.get("--eprint", DEFAULT_EPRINT)
    if not os.path.exists(eprint_path):
        print(f"calibration: INPUT_MISSING ({eprint_path}) — fetch the e-print first "
              "(sf_fulltext_fetch.py)")
        return 1
    blob = open(eprint_path, "rb").read()
    members = extract_text_members(blob)
    bib_text = "\n".join(t for n, t in sorted(members.items())
                         if re.search(r"\.(bbl|bib)$", n, re.I))
    scope = "bbl/bib members"
    if not bib_text.strip():
        bib_text = "\n".join(t for t in members.values())
        scope = "all text members (no bbl/bib found)"
    n_bibitems = len(re.findall(r"\\bibitem", bib_text)) + len(
        re.findall(r"@\w+\s*\{", bib_text))
    cited_ids = sorted(set(ARXIV_ID_RE.findall(bib_text)) - {TARGET})

    seed_ids = {json.loads(l)["id"] for l in open(SEEDS, encoding="utf-8") if l.strip()}
    sentinel_ids = set(json.load(open(SENTINELS, encoding="utf-8"))["papers"].keys())
    stock = seed_ids | sentinel_ids
    overlap = sorted(set(cited_ids) & stock)

    prediction_confirmed = (len(overlap) == 0)
    report = {
        "artifact_id": "SF-CITATION-CALIBRATION-SEGAGENT-2026-07-17-01",
        "experiment": "amendment-7 §4.1（预注册:交集=∅）",
        "target": TARGET,
        "eprint_sha256_ref": "wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl",
        "extraction_scope": scope,
        "n_text_members": len(members),
        "n_bibliography_entries_approx": n_bibitems,
        "n_arxiv_ids_cited": len(cited_ids),
        "arxiv_ids_cited": cited_ids,
        "stock_size": {"seeds": len(seed_ids), "sentinels": len(sentinel_ids),
                       "union": len(stock)},
        "overlap_with_stock": overlap,
        "prediction": "intersection = ∅（跨社区谱系引 SAM/SoM 系）",
        "verdict": ("PREDICTION_CONFIRMED — 引用交集筛不可作唯一发现入口的实证登记件"
                    if prediction_confirmed else
                    "PREDICTION_REFUTED — 按 amendment-7 §4.1 修正 §1 规则并登记"),
        "rule_consequence": "维持:交集为空⇒降级轻筛(登记后排除),发现层仍由冻结查询承载"
                            if prediction_confirmed else
                            "需 owner 复核:交集非空说明引用筛比预期更有召回力",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write((json.dumps(report, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    print(f"calibration: {report['verdict']}")
    print(f"  cited arXiv ids: {len(cited_ids)}; overlap with stock({len(stock)}): {overlap}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
