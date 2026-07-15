#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/checks/build_registers.py — P0 integrity registers (2026-07-13, ticket #38 item 4,
v4.2 doctoral review §6 P0_INTEGRITY_FREEZE "required_artifacts": prior_exposure_registry.json,
experiment_attempt_registry.jsonl, discrepancy_register.md).

Generates THREE machine-collected registers (this script does NOT generate
release_manifest.json — see the sibling scripts/checks/build_release_manifest.py for that):

  (i)   docs/integrity/prior_exposure_registry.json — everything OBSERVED so far: datasets/splits
        touched (from W1's _repro/ artifact filenames), models touched, effect sizes already on
        record (from docs/claim_ledger.yaml), and a flagged subset specifically covering the
        C-ASR-V2 selector battery (owner ruling, Decision-Log: "prior-exposure register discloses
        all previously observed effect sizes incl. C-ASR-V2 battery"). Machine-collected WHERE
        POSSIBLE — an explicit, honest `manual_completion_todo` list names exactly what this script
        CANNOT auto-derive (prompt template text, exact metric-family definitions per artifact,
        etc.) rather than silently omitting it or pretending it was checked.

  (ii)  docs/integrity/experiment_attempt_registry.jsonl — one JSON line per known run artifact
        under W1's `_repro/` tree: path, mtime (best-effort "when"), and a best-effort `purpose`
        string (derived from the filename's own naming convention — NOT a human-verified
        description; flagged as such).

  (iii) docs/integrity/discrepancy_register.md — seeded with the KNOWN record-inconsistencies the
        2026-07-13 v4.2 doctoral review already names (stale "4 errors" text, converged-wording
        scope, chronology date-vs-commit — review §1/§4 M-8), plus this run's OWN live-checked
        facts (so the register never silently goes stale relative to whoever last ran it).

Usage (WSL venv; PyYAML required for claim_ledger.yaml):
    python scripts/checks/build_registers.py --umbrella-root . \\
        --w1-root projects/speech-mllm-training-free-rl --out-dir docs/integrity
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys

try:
    import yaml
except Exception as exc:  # pragma: no cover
    sys.stderr.write("FATAL: PyYAML is required (pip install pyyaml): %s\n" % exc)
    sys.exit(2)


def _utc_now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _mtime_utc(path: str) -> str:
    ts = os.path.getmtime(path)
    return datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git_sha_of(repo_root: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=repo_root, text=True
        ).strip()
    except Exception as exc:  # pragma: no cover
        return "UNKNOWN (%s)" % exc


def git_dirty_of(repo_root: str) -> bool | None:
    try:
        out = subprocess.check_output(["git", "status", "--porcelain"], cwd=repo_root, text=True)
        return bool(out.strip())
    except Exception:  # pragma: no cover
        return None


# --------------------------------------------------------------------------------------------- #
# _repro/ artifact scan (feeds BOTH experiment_attempt_registry.jsonl and
# prior_exposure_registry.json's datasets/models-touched summary)
# --------------------------------------------------------------------------------------------- #

# <dataset>__<model>__<split>[.suffix...].json — the naming convention scripts/baselines' runner
# scripts (run_baseline.py etc.) actually use for per-(dataset, model, split) result artifacts.
_TRIPLE_RE = re.compile(r"^(?P<dataset>.+?)__(?P<model>[^_].*?)__(?P<split>dev|test|train)\b")

_SKIP_DIR_NAMES = {"__pycache__", ".git"}


def _iter_repro_files(w1_root: str):
    repro = os.path.join(w1_root, "_repro")
    if not os.path.isdir(repro):
        return
    for dirpath, dirnames, filenames in os.walk(repro):
        dirnames[:] = [d for d in dirnames if d not in _SKIP_DIR_NAMES]
        for fn in sorted(filenames):
            yield os.path.join(dirpath, fn)


def _best_effort_purpose(relpath: str, fn: str) -> dict:
    """Filename-derived, best-effort ONLY -- never a human-verified description. Returns
    {dataset, model, split, purpose_note} with whichever fields the naming convention yields
    (None for the rest)."""
    m = _TRIPLE_RE.match(fn)
    if m:
        return {
            "dataset": m.group("dataset"), "model": m.group("model"), "split": m.group("split"),
            "purpose_note": "per-(dataset,model,split) result artifact (filename convention)",
        }
    stem = re.sub(r"\.(json|jsonl|md|yaml)$", "", fn, flags=re.IGNORECASE)
    return {
        "dataset": None, "model": None, "split": None,
        "purpose_note": "mnemonic filename '%s' -- not machine-parsed further (see "
                         "manual_completion_todo)" % stem,
    }


def scan_repro_artifacts(w1_root: str) -> list[dict]:
    out = []
    for abspath in _iter_repro_files(w1_root):
        relpath = os.path.relpath(abspath, w1_root).replace("\\", "/")
        fn = os.path.basename(abspath)
        meta = _best_effort_purpose(relpath, fn)
        try:
            size = os.path.getsize(abspath)
        except OSError:
            size = None
        out.append({
            "path": "projects/speech-mllm-training-free-rl/" + relpath,
            "mtime_utc": _mtime_utc(abspath),
            "size_bytes": size,
            **meta,
        })
    return out


# --------------------------------------------------------------------------------------------- #
# claim_ledger.yaml scan (effect sizes already on record)
# --------------------------------------------------------------------------------------------- #

_SELECTOR_KEYWORDS = ("selector", "mbr", "logprob", "length", "c-asr-v2", "asr_bon_v2",
                      "best-of-n", "bon", "oracle")


def load_claim_ledger(umbrella_root: str) -> list[dict]:
    path = os.path.join(umbrella_root, "docs", "claim_ledger.yaml")
    if not os.path.isfile(path):
        return []
    with open(path, "r", encoding="utf-8") as fh:
        entries = yaml.safe_load(fh)
    return [e for e in (entries or []) if isinstance(e, dict) and "claim_id" in e]


def _excerpt(text, limit=400) -> str:
    if not text:
        return ""
    s = " ".join(str(text).split())
    return s if len(s) <= limit else s[:limit] + " ..."


def summarize_effect_sizes(ledger_entries: list[dict]) -> list[dict]:
    out = []
    for e in ledger_entries:
        out.append({
            "claim_id": e.get("claim_id"),
            "status": e.get("status"),
            "stage": e.get("stage"),
            "artifact": e.get("artifact"),
            "metric_definition": _excerpt(e.get("metric_definition"), 300),
            "note_excerpt": _excerpt(e.get("note"), 500),
            "superseded_by": e.get("superseded_by"),
        })
    return out


def flag_selector_battery_observations(ledger_entries: list[dict]) -> list[dict]:
    """Owner ruling (Decision-Log 续28): 'prior-exposure register discloses all previously
    observed effect sizes incl. C-ASR-V2 battery' -- entries whose claim_text/note/metric_definition
    mention selector-battery-adjacent terms (MBR/logprob/length/C-ASR-V2/best-of-N/oracle)."""
    out = []
    for e in ledger_entries:
        haystack = " ".join([
            str(e.get("claim_id", "")), str(e.get("claim_text", "")),
            str(e.get("metric_definition", "")), str(e.get("note", "")),
        ]).lower()
        if any(k in haystack for k in _SELECTOR_KEYWORDS):
            out.append({
                "claim_id": e.get("claim_id"), "status": e.get("status"),
                "claim_text_excerpt": _excerpt(e.get("claim_text"), 300),
                "note_excerpt": _excerpt(e.get("note"), 500),
            })
    return out


# --------------------------------------------------------------------------------------------- #
# datasets/models-touched summary (from the _repro/ scan)
# --------------------------------------------------------------------------------------------- #

def summarize_datasets_touched(artifacts: list[dict]) -> dict:
    by_dataset: dict[str, dict] = {}
    for a in artifacts:
        ds = a.get("dataset")
        if not ds:
            continue
        entry = by_dataset.setdefault(ds, {"splits_touched": set(), "models_touched": set(),
                                            "n_artifacts": 0, "example_artifacts": []})
        entry["n_artifacts"] += 1
        if a.get("split"):
            entry["splits_touched"].add(a["split"])
        if a.get("model"):
            entry["models_touched"].add(a["model"])
        if len(entry["example_artifacts"]) < 3:
            entry["example_artifacts"].append(a["path"])
    return {
        ds: {
            "splits_touched": sorted(v["splits_touched"]),
            "models_touched": sorted(v["models_touched"]),
            "n_artifacts": v["n_artifacts"],
            "example_artifacts": v["example_artifacts"],
        }
        for ds, v in sorted(by_dataset.items())
    }


# --------------------------------------------------------------------------------------------- #
# 2026-07-13 enrichment (ticket #38 P0 flesh-out): prompt-template enumeration, metric-family
# enumeration, C-ASR-V2 selector-comparator effect extraction, and a dev-exposure event ledger.
# Everything below is machine-collected from files ON DISK; whatever genuinely cannot be
# auto-derived stays in MANUAL_COMPLETION_TODO. Resolves manual_completion_todo[0]/[1] of the
# earlier stub for the parts that ARE recoverable from disk.
# --------------------------------------------------------------------------------------------- #

_TEMPLATE_DEF_RE = re.compile(r"^def (?P<name>k\d+_[a-z0-9_]+)\(", re.MULTILINE)


def enumerate_prompt_templates(w1_root: str) -> dict:
    """Machine-derive the DISTINCT prompt-template families from scripts/baselines/templates.py
    (the named per-K-type builder functions the baseline runner dispatches through
    build_instruction()). Free-form/inline dev prompts NOT registered there stay in
    manual_completion_todo."""
    rel = "scripts/baselines/templates.py"
    path = os.path.join(w1_root, rel)
    out = {
        "source_evidence": "projects/speech-mllm-training-free-rl/" + rel,
        "dispatcher": "build_instruction(dataset_key,row) -> k_type_of(dataset_key) -> kN_* builder",
        "template_functions": [],
        "n_template_functions": 0,
        "note": ("The NAMED per-K-type prompt builders actually used by the baseline runner. "
                 "Inline/free-form prompts (run_baseline.py / run_mock.py ad-hoc strings, "
                 "kb_batch_build.py pseudo-question generator) are NOT captured here -- see "
                 "manual_completion_todo."),
    }
    if not os.path.isfile(path):
        out["note"] = "templates.py NOT FOUND at %s" % rel
        return out
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    names = sorted(set(_TEMPLATE_DEF_RE.findall(text)))
    out["template_functions"] = names
    out["n_template_functions"] = len(names)
    return out


def enumerate_metric_families(w1_root: str) -> dict:
    """Machine-derive distinct metric families actually computed, by OPENING every baseline result
    artifact and reading its own recorded `k_type`, `stage`, and `aggregate` metric keys. Resolves
    manual_completion_todo[1] for the baseline grid (the artifacts that record metric keys)."""
    import collections
    base = os.path.join(w1_root, "_repro", "baselines")
    k_types: "collections.Counter[str]" = collections.Counter()
    agg_keys: "collections.Counter[str]" = collections.Counter()
    stages: "collections.Counter[str]" = collections.Counter()
    n = 0
    n_err = 0
    if os.path.isdir(base):
        for fn in sorted(os.listdir(base)):
            if not fn.endswith(".json"):
                continue
            try:
                with open(os.path.join(base, fn), "r", encoding="utf-8") as fh:
                    d = json.load(fh)
            except Exception:
                n_err += 1
                continue
            if not isinstance(d, dict):
                continue
            n += 1
            if d.get("k_type"):
                k_types[str(d["k_type"])] += 1
            if d.get("stage"):
                stages[str(d["stage"])] += 1
            agg = d.get("aggregate")
            if isinstance(agg, dict):
                for k in agg.keys():
                    agg_keys[str(k)] += 1
    return {
        "source_evidence": ("projects/speech-mllm-training-free-rl/_repro/baselines/*.json "
                            "(each artifact's own k_type/stage/aggregate keys)"),
        "n_baseline_artifacts_read": n,
        "n_read_errors": n_err,
        "k_type_taxonomy": dict(sorted(k_types.items())),
        "aggregate_metric_keys": dict(sorted(agg_keys.items())),
        "stages_observed": dict(sorted(stages.items())),
        "note": ("k_type = the K1-K11 metric-type taxonomy (K1/K2 ASR-WER, K3 LID/gender, K4 SER, "
                 "K5 attribute, K6 intent-acc, K7 slot-F1, K8 MCQ/QA-acc, K9 closed-book, K10 "
                 "tool-call, K11 passthrough/probe). aggregate_metric_keys are the scored statistics "
                 "stored per cell. Non-baseline artifacts (asr_bon, selector, probe) record bespoke "
                 "schemas covered under c_asr_v2_selector_comparator_effects / effect_sizes_observed."),
    }


_ASR_V2_CONDITION_FILES = {
    "snr5": "_repro/asr_bon_v2_snr5.json",
    "clean": "_repro/asr_bon_v2_clean.json",
}
_ASR_V2_SELECTORS = ["oracle", "logprob", "mbr", "random", "length"]


def extract_c_asr_v2_selector_effects(w1_root: str) -> dict:
    """Machine-extract the C-ASR-V2 selector battery's per-selector corpus-WER effects at the
    deployment endpoint N=8 (owner ruling 续28②: prior-exposure register discloses ALL previously
    observed effect sizes incl. the C-ASR-V2 battery). realized_fraction = logprob_delta /
    oracle_delta per condition -- the ~24%/~42%-of-oracle-headroom headline."""
    out = {
        "source_evidence": ["projects/speech-mllm-training-free-rl/" + v
                            for v in _ASR_V2_CONDITION_FILES.values()],
        "claim_id": "C-ASR-V2",
        "endpoint": ("N=8 (deployment endpoint); each selector vs greedy decode; corpus-WER delta "
                     ">0 = improvement; hierarchical bootstrap (utterance x pool-seed) CI95"),
        "conditions": {},
        "headline_realized_fraction_of_oracle_headroom": {},
        "multiplicity_caveat": ("Full discovery-grid Holm correction (4 deployable selectors x 4 N = "
                                "16 corpus-WER comparisons/condition) survives in NEITHER condition; "
                                "the fixed-N=8 4-selector family survives in noise2 only. logprob is "
                                "the SOLE selector whose corpus-WER CI excludes 0 in BOTH conditions, "
                                "but the signal is marginal -- Stage-1 directional, NOT a deployable "
                                "win. MBR positive but ns in both; random and length are significant "
                                "REGRESSIONS on clean. See claim_ledger C-ASR-V2 "
                                "hardening_update_correction_2026_07_12."),
    }
    for cond, rel in _ASR_V2_CONDITION_FILES.items():
        p = os.path.join(w1_root, rel)
        if not os.path.isfile(p):
            out["conditions"][cond] = {"error": "artifact not found: %s" % rel}
            continue
        try:
            with open(p, "r", encoding="utf-8") as fh:
                d = json.load(fh)
        except Exception as exc:  # pragma: no cover
            out["conditions"][cond] = {"error": "load failed: %s" % exc}
            continue
        sel8 = (((d.get("summary") or {}).get("selectors") or {}).get("8") or {})
        rows = {}
        for name in _ASR_V2_SELECTORS:
            s = sel8.get(name)
            if not isinstance(s, dict):
                continue
            rows[name] = {
                "corpus_delta_vs_greedy_mean": s.get("corpus_delta_vs_greedy_mean"),
                "corpus_delta_vs_greedy_ci95": s.get("corpus_delta_vs_greedy_ci95"),
                "corpus_sig": s.get("corpus_sig"),
                "macro_sig": s.get("macro_sig"),
            }
        out["conditions"][cond] = {"selectors_at_N8": rows}
        try:
            orc = rows["oracle"]["corpus_delta_vs_greedy_mean"]
            lp = rows["logprob"]["corpus_delta_vs_greedy_mean"]
            if orc:
                out["headline_realized_fraction_of_oracle_headroom"][cond] = round(lp / orc, 4)
        except Exception:  # pragma: no cover
            pass
    return out


_OVERLAP_RE = re.compile(r"(\d+\.\d+)\s*%\s*overlap", re.IGNORECASE)


def enumerate_dev_exposure_events(w1_root: str, artifacts: list[dict]) -> list[dict]:
    """Structured ledger of the DISTINCT dev-exposure events already on disk under _repro/. Each
    event names source_evidence path(s). This scan deliberately does NOT open the LOCKED_HOLDOUT
    per-dataset id lists (test_ids/dev_ids) -- that is a GOVERNED access (ACCESS_LOG.md); only file
    metadata + the README downgrade banner text are read."""
    events = []
    locked_cells = sorted(a["path"] for a in artifacts
                          if "/baselines/" in a["path"] and a["path"].endswith(".locked.json"))
    events.append({
        "event_id": "locked_dev_baseline_rerun",
        "what": "group-aware locked-DEV baseline rerun; per-(dataset,model,split=dev) scored cells",
        "magnitude": ("%d *.locked.json dev cells (ALL 65 dataset keys; test half single-consumer "
                      "reserved)" % len(locked_cells)),
        "date": "2026-07-11",
        "claim_id": "C-BASELINES",
        "n_source_artifacts": len(locked_cells),
        "source_evidence": (["projects/speech-mllm-training-free-rl/_repro/LOCKED_HOLDOUT/ACCESS_LOG.md"]
                            + locked_cells[:3]),
    })
    readme = os.path.join(w1_root, "_repro", "LOCKED_HOLDOUT", "README.md")
    overlap = None
    if os.path.isfile(readme):
        with open(readme, "r", encoding="utf-8") as fh:
            m = _OVERLAP_RE.search(fh.read())
            if m:
                overlap = m.group(1) + "%"
    events.append({
        "event_id": "locked_holdout_permanent_downgrade",
        "what": ("65 LOCKED_HOLDOUT manifests permanently downgraded to exposed-dev-like (plaintext "
                 "test_ids + confirmed old-test overlap + honor-system access already happened)"),
        "magnitude": ("old-test overlap = %s (README banner); 65 manifests downgraded"
                      % (overlap or "see README (figure not auto-parsed)")),
        "date": "2026-07-12",
        "claim_id": None,
        "source_evidence": [
            "projects/speech-mllm-training-free-rl/_repro/LOCKED_HOLDOUT/README.md",
            "projects/speech-mllm-training-free-rl/_repro/LOCKED_HOLDOUT/ACCESS_LOG.md",
        ],
        "note": "This scan does NOT open the per-dataset test_ids/dev_ids lists (governed access).",
    })
    asr = sorted(a["path"] for a in artifacts if os.path.basename(a["path"]).startswith("asr_bon"))
    events.append({
        "event_id": "asr_best_of_n_family",
        "what": ("ASR best-of-N / selector-battery exposures (llama.cpp Qwen3-Omni-30B, {clean,snr5}, "
                 "oracle/logprob/mbr/random/length x N in {1,2,4,8})"),
        "magnitude": ("see c_asr_v2_selector_comparator_effects (realized fraction ~24%/~42% of "
                      "oracle headroom; logprob sole selector with both-condition CI excluding 0)"),
        "date": "2026-07-02..2026-07-11",
        "claim_id": "C-ASR-V2",
        "source_evidence": asr,
    })
    selart = sorted(a["path"] for a in artifacts if os.path.basename(a["path"]) in {
        "m5_selector_dev.json", "m5_selector_confirmatory.json",
        "cp3_selector_realization_mmau.json", "coverage_bridge_v1.json"})
    if selart:
        events.append({
            "event_id": "selector_dev_and_confirmatory_slices",
            "what": ("MMAU selector realization + m5 selector dev/confirmatory slices (rho "
                     "oracle-headroom realization exposure)"),
            "magnitude": "selector-realization + confirmatory slice artifacts present on disk",
            "date": "2026-07-03..2026-07-04",
            "claim_id": "C-ASR-V2",
            "source_evidence": selart,
        })
    probe = sorted(a["path"] for a in artifacts if os.path.basename(a["path"]) in {
        "m3_crossmodal.json", "t7_rag_gate_probe.json", "cp1_multimodal_feature_audited_mmau.json",
        "cp1_slu_hprompt_minds14.json", "cp1_sqa_hprompt_mmau.json"})
    if probe:
        events.append({
            "event_id": "cross_modal_and_rag_probe_exposures",
            "what": ("cross-modal injection (C-M3, RETRACTED/leaked) + RAG-gate probe (C-T7, "
                     "RETRACTED/leaked) + hprompt cp1 dev exposures -- kept for failure-history "
                     "provenance; do NOT cite as positive"),
            "magnitude": "retracted/invalid (information-boundary violations)",
            "date": "2026-07-04..2026-07-07",
            "claim_id": ["C-M3", "C-T7"],
            "source_evidence": probe,
        })
    return events


# --- experiment_attempt_registry.jsonl per-row enrichment (beyond the shallow filename scan) --- #

_W1_PREFIX = "projects/speech-mllm-training-free-rl/"
_CLAIM_BY_STEM_PREFIX = [
    ("asr_bon_v2", "C-ASR-V2"),
    ("asr_bon_llamacpp", "C-ASR-ORACLE"),  # artifact also backs C-ASR-MBR / C-ASR-SEEDS
    ("m3_crossmodal", "C-M3"),
    ("t7_rag_gate", "C-T7"),
    ("m5_selector", "C-ASR-V2"),
    ("cp3_selector", "C-ASR-V2"),
    ("coverage_bridge", "C-THEORY"),
]
_PEEK_MAX_BYTES = 260000


def _content_hint(abspath: str) -> str | None:
    """Bounded content peek for small JSON artifacts: returns a short 'key=value' hint and lets the
    caller flag inferred=False (purpose confirmed from content, not merely guessed from filename)."""
    try:
        if not abspath.endswith(".json") or os.path.getsize(abspath) > _PEEK_MAX_BYTES:
            return None
        with open(abspath, "r", encoding="utf-8") as fh:
            d = json.load(fh)
    except Exception:
        return None
    if not isinstance(d, dict):
        return None
    for key in ("problem", "stage", "note", "title"):
        if key in d and isinstance(d[key], (str, int, float)):
            return "%s=%s" % (key, str(d[key])[:80])
    summ = d.get("summary")
    if isinstance(summ, dict):
        for key in ("problem", "task", "condition"):
            if key in summ:
                return "summary.%s=%s" % (key, str(summ[key])[:80])
    return "top_keys=" + ",".join(list(d.keys())[:6])


def _enrich_attempt(entry: dict, w1_root: str) -> dict:
    path = entry["path"]
    fn = os.path.basename(path)
    stem = re.sub(r"\.(json|jsonl|md|yaml)$", "", fn, flags=re.IGNORECASE)
    inferred = True
    if "/LOCKED_HOLDOUT/" in path and fn.endswith(".json"):
        status = "holdout-manifest (test_ids present; id lists NOT opened by this scan)"
        if entry.get("dataset") is None:
            entry["dataset"] = stem
    elif entry.get("dataset") and ".locked." in fn:
        status, inferred = "locked-dev-cell", False
    elif entry.get("dataset") and any(s in fn for s in (
            ".pre-lockedrerun", ".pre-rescore", ".disjoint-validation")):
        status, inferred = "superseded-variant", False
    elif entry.get("dataset") and ".broken" in fn:
        status, inferred = "broken-variant", False
    elif entry.get("dataset"):
        status, inferred = "baseline-cell", False
    elif fn.endswith(".md"):
        status = "notes/doc"
    elif fn.endswith(".yaml"):
        status = "validity-annotation"
    else:
        status = "probe-or-analysis-artifact"
    claim_id = None
    for pref, cid in _CLAIM_BY_STEM_PREFIX:
        if stem.startswith(pref):
            claim_id = cid
            break
    if claim_id is None and entry.get("dataset") and "/baselines/" in path:
        claim_id = "C-BASELINES"
    hint = None
    if entry.get("dataset") is None and "/LOCKED_HOLDOUT/" not in path and path.startswith(_W1_PREFIX):
        hint = _content_hint(os.path.join(w1_root, path[len(_W1_PREFIX):]))
        if hint:
            inferred = False
    entry["status"] = status
    entry["inferred"] = inferred
    entry["claim_id"] = claim_id
    if hint:
        entry["content_hint"] = hint
    return entry


MANUAL_COMPLETION_TODO = [
    "CONFIG-SELECTION TRAJECTORY (v4.2 review M-6): the full search space actually explored (every "
    "tried modality/form/delivery/selector-weight/K/threshold/embedder/PROMPT and its abandonment "
    "reason) is only PARTIALLY on disk. Named prompt-template families are now enumerated "
    "(prompt_templates_enumerated) and the baseline metric taxonomy is enumerated "
    "(metric_families_enumerated), but ad-hoc dev prompts and abandoned weight/threshold/K sweeps "
    "NOT persisted to _repro/ cannot be auto-derived -- they must be reconstructed from session "
    "logs / human recall. THIS is the load-bearing OUTSTANDING item for P0.",
    "INLINE/FREE-FORM PROMPTS outside scripts/baselines/templates.py (run_baseline.py / run_mock.py "
    "ad-hoc strings; kb_batch_build.py pseudo-question generator) are not captured by the "
    "named-function enumeration and need a manual sweep.",
    "Confirm whether any dataset/split pair was ALSO touched by a process OUTSIDE _repro/ entirely "
    "(ad-hoc notebooks, since-deleted scripts, a sibling session's uncommitted local files) -- this "
    "scan is limited to what is currently ON DISK under _repro/.",
    "Reconcile scripts/baselines/_repro/draws/exposure_registry.json (deterministic_draw.py's own "
    "F-8(b) registry) against this file once the sampling-isolation track produces real eligibility/"
    "exploration/confirmatory draws -- no draws/ directory exists yet on disk.",
]


P0_GATE_STATUS = {
    "gate_id": "P0_INTEGRITY_FREEZE",
    "pass_conditions_met": False,
    "certification": ("NOT_PASS (honest-audit, Decision-Log 续28④). The four required_artifacts now "
                      "exist AND the two registers are substantially fleshed out: prompt-template + "
                      "metric-family enumeration and the C-ASR-V2 selector-battery effect sizes are "
                      "now machine-collected, and experiment_attempt_registry.jsonl now carries "
                      "per-row status/claim_id/inferred flags. Gate STILL NOT PASS: the "
                      "config-selection trajectory (M-6) is only partially recoverable from disk, "
                      "and the independent read-only reviewer snapshot (pass_conditions[2]) is a "
                      "process step this file cannot self-certify."),
    "resolved_this_round_2026_07_13": [
        "prompt-template enumeration -> prompt_templates_enumerated (kN_* builders from templates.py).",
        "metric-family enumeration -> metric_families_enumerated (K1-K11 taxonomy + aggregate keys, "
        "machine-read from every baseline artifact).",
        "C-ASR-V2 selector battery magnitudes disclosed explicitly -> "
        "c_asr_v2_selector_comparator_effects (realized fraction ~24%/~42%; MBR/random/length "
        "results at N=8, machine-extracted from the artifacts).",
        "experiment_attempt_registry.jsonl enriched beyond the shallow filename+mtime scan "
        "(status / claim_id / inferred / content_hint per row).",
        "dev-exposure events enumerated -> dev_exposure_events (locked-dev rerun, LOCKED_HOLDOUT "
        "downgrade, asr best-of-N family, selector slices, retracted cross-modal/RAG probes).",
        "append_only_erratum_for_v42.md created on disk (fourth P0 artifact).",
    ],
    "unmet_pass_conditions": [
        "CONFIG-SELECTION TRAJECTORY (M-6) not fully enumerable: abandoned prompt/weight/threshold/K/"
        "embedder sweeps not persisted to _repro/ cannot be auto-derived (manual_completion_todo[0]).",
        "pass_conditions[2] 'independent reviewer receives read-only artifact snapshot' is a process "
        "step, not certified by this file.",
    ],
    "honest_audit_note": ("Independent-honest-audit stance adopted at Stage-1 (Decision-Log 续28④): "
                          "this gate is reported by its TRUE state. Any remediation report for "
                          "external-reviewer sign-off MUST present P0 as INCOMPLETE (not PASS) "
                          "until the config-selection trajectory (M-6) is enumerated and an "
                          "independent reviewer receives the read-only snapshot."),
}


def build_prior_exposure_registry(umbrella_root: str, w1_root: str) -> dict:
    artifacts = scan_repro_artifacts(w1_root)
    ledger = load_claim_ledger(umbrella_root)
    return {
        "_comment": ("P0 integrity register (2026-07-13, v4.2 doctoral review §6 "
                     "P0_INTEGRITY_FREEZE) -- everything OBSERVED so far, machine-collected WHERE "
                     "POSSIBLE from W1's _repro/ artifact tree, docs/claim_ledger.yaml, "
                     "scripts/baselines/templates.py, and the C-ASR-V2 artifacts. 2026-07-13 "
                     "flesh-out (ticket #38): prompt-template + metric-family enumeration, C-ASR-V2 "
                     "selector-comparator effect sizes, and a dev-exposure event ledger added. See "
                     "manual_completion_todo for what still cannot be auto-derived."),
        "generated_at": _utc_now(),
        "generated_by": "scripts/checks/build_registers.py",
        "umbrella_git_sha": git_sha_of(umbrella_root),
        "w1_git_sha": git_sha_of(w1_root),
        "n_repro_artifacts_scanned": len(artifacts),
        "datasets_touched": summarize_datasets_touched(artifacts),
        "n_claim_ledger_entries": len(ledger),
        "effect_sizes_observed": summarize_effect_sizes(ledger),
        "selector_battery_observations_c_asr_v2_family": flag_selector_battery_observations(ledger),
        "c_asr_v2_selector_comparator_effects": extract_c_asr_v2_selector_effects(w1_root),
        "prompt_templates_enumerated": enumerate_prompt_templates(w1_root),
        "metric_families_enumerated": enumerate_metric_families(w1_root),
        "dev_exposure_events": enumerate_dev_exposure_events(w1_root, artifacts),
        "manual_completion_todo": MANUAL_COMPLETION_TODO,
        "p0_gate_status": P0_GATE_STATUS,
    }


def build_experiment_attempt_registry(w1_root: str) -> list[dict]:
    return [_enrich_attempt(r, w1_root) for r in scan_repro_artifacts(w1_root)]


# --------------------------------------------------------------------------------------------- #
# discrepancy register (seeded from the review's own §1/§4 findings + this run's live checks)
# --------------------------------------------------------------------------------------------- #

def _run_standard_pytest_w1(w1_root: str) -> dict:
    """Best-effort: run PYTHONPATH=src pytest -q inside W1 and capture the summary line -- used to
    live-check the 'stale 4-errors text' discrepancy against the CURRENT state (never assumed)."""
    env = dict(os.environ)
    env["PYTHONPATH"] = os.path.join(w1_root, "src")
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-q"], cwd=w1_root, env=env,
            capture_output=True, text=True, timeout=1800,
        )
        tail = "\n".join(proc.stdout.strip().splitlines()[-5:])
        return {"ran": True, "returncode": proc.returncode, "summary_tail": tail}
    except Exception as exc:  # pragma: no cover
        return {"ran": False, "reason": str(exc)}


def build_discrepancy_register_md(umbrella_root: str, w1_root: str, *, run_pytest: bool) -> str:
    live_pytest = _run_standard_pytest_w1(w1_root) if run_pytest else {"ran": False, "reason": "skipped (--no-live-pytest)"}
    lines = []
    lines.append("# Discrepancy register")
    lines.append("")
    lines.append("Seeded 2026-07-13 (ticket #38 item 4, v4.2 doctoral review §6 P0_INTEGRITY_FREEZE"
                  " `required_artifacts`) by `scripts/checks/build_registers.py`. Append-only in"
                  " spirit: add a new dated entry to re-adjudicate, never silently delete a prior"
                  " one.")
    lines.append("")
    lines.append("## Known record-inconsistencies (from the 2026-07-13 v4.2 doctoral review)")
    lines.append("")
    lines.append("Source: `wiki/2026-07-13-v42-doctoral-adversarial-integrity-review.md` §1 "
                  "(可复核事实) and §4 M-8.")
    lines.append("")
    lines.append("1. **Stale \"4 errors\" text** — v4.2 §13.4 stated the standard entry had "
                  "\"现有 4 errors\" as of that snapshot; the review's own real run reported "
                  "`PYTHONPATH=src pytest -q` → **143 passed, 3 warnings, 167.10s, 0 errors** "
                  "at commit `159b525`. The \"4 errors\" text was stale/outdated at publish time.")
    lines.append("2. **\"Converged (2 rounds, 0 residual)\" wording scope** — commit `159b5258`'s "
                  "subject line uses \"converged\"/\"0 residual\" language while the SAME proposal "
                  "snapshot lists undelivered items (K-trajectory harness, live cross-modal smoke, "
                  "corpus lock, REPRODUCE.md, full SAP numbers, operator-linked theory) — the review "
                  "judges this \"更像发布快照协调失败，而不是有利方向的数据造假\" (a release-snapshot "
                  "coordination failure, not favorable-direction fabrication) but it still means "
                  "\"converged\"/\"locked\" must not be read as an M1-closure claim.")
    lines.append("3. **Chronology: date-vs-commit** — the root proposal's frontmatter date is "
                  "2026-07-12, but its FIRST git commit timestamp is 2026-07-13 01:42:28 +08:00 — "
                  "insufficient alone to prove backdating, but an unexplained release-record vs. "
                  "file-date mismatch the review flags as needing a `created_at`/`released_at` "
                  "dual-timestamp fix going forward.")
    lines.append("")
    lines.append("## This run's live-checked facts (never assumed stale)")
    lines.append("")
    lines.append("- **generated_at (UTC)**: %s" % _utc_now())
    lines.append("- **umbrella git SHA**: `%s` (dirty=%s)"
                  % (git_sha_of(umbrella_root), git_dirty_of(umbrella_root)))
    lines.append("- **W1 git SHA**: `%s` (dirty=%s)"
                  % (git_sha_of(w1_root), git_dirty_of(w1_root)))
    if live_pytest.get("ran"):
        lines.append("- **W1 standard entry (`PYTHONPATH=src pytest -q`) THIS RUN**: returncode=%d"
                      % live_pytest["returncode"])
        lines.append("  ```")
        lines.append("  " + live_pytest["summary_tail"].replace("\n", "\n  "))
        lines.append("  ```")
    else:
        lines.append("- **W1 standard entry**: NOT re-run by this script this time (%s) — see "
                      "`docs/integrity/release_manifest.json` (built separately by "
                      "`scripts/checks/build_release_manifest.py`) for the authoritative, "
                      "dedicated standard-entry result." % live_pytest.get("reason"))
    lines.append("")
    lines.append("## Open items (not yet adjudicated)")
    lines.append("")
    lines.append("- **P0_INTEGRITY_FREEZE is NOT yet PASS (honest-audit, Decision-Log 续28).** Two "
                  "of the four required registers are partial: `prior_exposure_registry.json` still "
                  "lists prompt-template and metric-family enumeration as OUTSTANDING "
                  "(`manual_completion_todo[0]/[1]`), and `experiment_attempt_registry.jsonl` is a "
                  "shallow filename+mtime scan that does NOT capture the config-selection trajectory "
                  "(every tried prompt/weight/threshold/K/embedder + abandonment reason) that "
                  "P0/M-6 require. The required `append_only_erratum_for_v42.md` is not yet on disk. "
                  "Any remediation report MUST present P0 as INCOMPLETE, not PASS, until these are "
                  "enumerated. Authoritative machine-readable status: "
                  "`prior_exposure_registry.json` -> `p0_gate_status`.")
    lines.append("- Whether the root-repo first-commit-timestamp-vs-frontmatter-date gap (item 3 "
                  "above) recurs in any LATER release snapshot — needs a `created_at`/`released_at` "
                  "field added to future proposal frontmatter and checked mechanically, not just "
                  "narrated here once.")
    lines.append("- Any NEW discrepancy this script's future re-runs surface between this file's "
                  "last-recorded facts and the live-checked facts at that later run — append, do "
                  "not overwrite, the \"This run's live-checked facts\" section above.")
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--umbrella-root", default=".")
    ap.add_argument("--w1-root", default="projects/speech-mllm-training-free-rl")
    ap.add_argument("--out-dir", default="docs/integrity")
    ap.add_argument("--no-live-pytest", action="store_true",
                     help="skip re-running W1's standard pytest entry inside this script (it is "
                          "run once, authoritatively, by build_release_manifest.py instead)")
    ap.add_argument("--registers-only", action="store_true",
                     help="write ONLY prior_exposure_registry.json + experiment_attempt_registry.jsonl; "
                          "do NOT (re)write discrepancy_register.md (used when that file is owned / "
                          "hand-edited by a concurrent process). Implies --no-live-pytest.")
    args = ap.parse_args()

    umbrella_root = os.path.abspath(args.umbrella_root)
    w1_root = args.w1_root if os.path.isabs(args.w1_root) else os.path.join(umbrella_root, args.w1_root)
    out_dir = args.out_dir if os.path.isabs(args.out_dir) else os.path.join(umbrella_root, args.out_dir)
    os.makedirs(out_dir, exist_ok=True)

    prior_exposure = build_prior_exposure_registry(umbrella_root, w1_root)
    p1 = os.path.join(out_dir, "prior_exposure_registry.json")
    with open(p1, "w", encoding="utf-8") as fh:
        json.dump(prior_exposure, fh, ensure_ascii=False, indent=2, sort_keys=False)
        fh.write("\n")

    attempts = build_experiment_attempt_registry(w1_root)
    p2 = os.path.join(out_dir, "experiment_attempt_registry.jsonl")
    with open(p2, "w", encoding="utf-8") as fh:
        for entry in attempts:
            fh.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")

    if args.registers_only:
        p3 = "SKIPPED (--registers-only; discrepancy_register.md left untouched)"
    else:
        discrepancy_md = build_discrepancy_register_md(
            umbrella_root, w1_root, run_pytest=not args.no_live_pytest)
        p3 = os.path.join(out_dir, "discrepancy_register.md")
        with open(p3, "w", encoding="utf-8") as fh:
            fh.write(discrepancy_md)

    print(json.dumps({
        "prior_exposure_registry": p1,
        "experiment_attempt_registry": p2,
        "n_experiment_attempts": len(attempts),
        "discrepancy_register": p3,
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
