#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Identity taxonomy v5 contract test (v8 doctoral review Gate MAJOR-1/-2/-3).

Deltas vs the v4 test (retained for audit of the v4-era claims):

MAJOR-1 — signal-instance identity: rows carry signals[] with signal_id;
  every control edge references one; is_rq_sys/is_reward_guided/
  reward_guided_selection are existentials over the SAME signal instance.
  Acceptance A1 (edge/signal lifecycle mismatch fails), A2 (different-signal
  splice is NOT rq), A5 (multi-signal rows keep per-signal identity),
  A6/A7 (rgs same-signal, offline calibration never qualifies).

MAJOR-2 — completeness, not just consistency: required-evidence contract per
  derived claim (positive canon/tex quote, pdf page-range+anchor, or absence
  adjudication with scope); tri-state strict bits (unknown never defaults to
  False); adjudication_row_sha256 binds the adjudication to row content so ANY
  post-adjudication change (incl. a lone horizon flip or a value+evidence
  double-flip) fails closed; PDF page tokens must be inside the pinned PDF's
  page range (p9999 dies); mutation set derived from the derivation's
  sensitivity surface, each must produce NEW failures beyond baseline.

MAJOR-3 — cross-platform replay: every registered asset path resolves through
  scripts/survey/sf_asset_path.py so Windows and WSL2 Ubuntu-24.04 read the
  same bytes and produce the same verdict.

Persists docs/checks/2026-07-19-sf-identity-taxonomy-v5-test.json
"""
import copy
import glob
import gzip
import hashlib
import io
import json
import os
import re
import sys
import tarfile

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sf_coding_generator import render  # noqa: E402
from sf_asset_path import resolve_asset_path  # noqa: E402

TAX = os.path.join(REPO, "wiki", "survey", "2026-07-19-sf-identity-taxonomy-v5.json")
CODING = os.path.join(REPO, "wiki", "survey", "2026-07-19-sf-known-item-coding-v6.json")
SIDECAR_DIR = os.path.join(REPO, "wiki", "survey", "sidecars")
INDEP = os.path.join(REPO, "wiki", "survey", "2026-07-18-sf-independent-counterexamples-v1.json")
INDEP2 = os.path.join(REPO, "wiki", "survey", "2026-07-19-sf-independent-counterexamples-v2.json")
INDEP3 = os.path.join(REPO, "wiki", "survey", "2026-07-19-sf-independent-counterexamples-v3.json")
OUT = os.path.join(REPO, "docs", "checks", "2026-07-19-sf-identity-taxonomy-v5-test.json")

_tax = json.load(io.open(TAX, encoding="utf-8"))
E = _tax["enums"]
ENUMS_ROW = {k: set(E[k]) for k in ("core_topology", "core_native_modality", "core_io_modality",
                                    "control_horizon", "selection_object", "terminal_operator",
                                    "selection_policy")}
VIS = set(E["internal_visibility"])
SIG_FORM = set(E["signal_form"])
SIG_SRC = set(E["signal_source"])
SIG_LC = set(E["signal_lifecycle"])
ADJ_STATUS = set(E["adjudication_status"])
SIGNAL_USE = set(_tax["signal_use"])
RIGHTS = set(_tax["decision_rights"])
REWARD_FORMS = set(_tax["reward_forms"])
ALLOWED = {k: set(v) for k, v in _tax["allowed_relations"].items()}
REWARD_USES = {"select", "prune", "revise", "route", "retry", "branch", "tool_call", "memory_write",
               "supply", "stop_budget", "execute_skip_gate"}
STRICT_BITS = ["core_weight_update", "external_component_weight_update",
               "controller_program_or_config_optimized_on_labels", "human_or_dev_label_model_selection",
               "deployment_label_access", "test_item_gold_access", "inference_external_new_information"]
REQ_FIELDS = STRICT_BITS + ["internal_visibility", "core_topology", "core_native_modality",
                            "control_horizon", "decision_rights", "candidate_pool_exists",
                            "selection_policy"]
LINEAGE = ["paper_work_id", "fulltext_ref", "canonical_record_id", "source_locator", "coder",
           "semantic_adjudicator"]
ADJ_EXCLUDE = {"semantic_adjudicator", "adjudication_status", "adjudication_row_sha256",
               "adjudication_provenance"}
TERMINAL_EDGE_RIGHTS = {"synthesize", "stop"}
QUOTE_PAT = re.compile(r"(canon|tex):\s*'([^']+)'")
PAGE_TOKEN = re.compile(r"p(\d+)(?:\s+([A-Za-z][A-Za-z0-9_-]{2,}))?")


def adapt(r):
    """Legacy flat fixture/CE rows -> signals form (real v6 rows pass through)."""
    if "signals" in r:
        return r
    r = dict(r)
    if r.get("signal_form") and r.get("signal_form") != "none":
        s = {"signal_id": "s1", "form": r["signal_form"], "source": r.get("signal_source", "none"),
             "lifecycle": r.get("signal_lifecycle", "none"), "uses": r.get("signal_use", []),
             "evidence": "fixture"}
        r["signals"] = [s]
        edges = []
        for e in r.get("control_edges", []):
            e = dict(e)
            e.setdefault("signal_id", "s1")
            edges.append(e)
        r["control_edges"] = edges
    else:
        r["signals"] = []
        r.setdefault("control_edges", [])
    return r


def sig_is_reward(s):
    return (s.get("lifecycle") in {"online_step", "terminal"}
            and s.get("form") in REWARD_FORMS
            and bool(set(s.get("uses", [])) & REWARD_USES))


def valid_live_edges(r):
    sigs = {s.get("signal_id"): s for s in r.get("signals", [])}
    out = []
    for e in r.get("control_edges", []):
        s = sigs.get(e.get("signal_id"))
        if s is None:
            continue
        if e.get("signal_use") not in s.get("uses", []):
            continue
        if e.get("decision_right") not in r.get("decision_rights", []):
            continue
        if e.get("decision_right") not in ALLOWED.get(e.get("signal_use"), ()):
            continue
        if not e.get("source_locator") or not e.get("edge_semantics"):
            continue
        if e.get("signal_lifecycle") and e["signal_lifecycle"] != s.get("lifecycle"):
            continue  # A1: mismatched edge is invalid (validator also flags it)
        lc = s.get("lifecycle")
        if lc == "online_step" or (lc == "terminal" and e["decision_right"] in TERMINAL_EDGE_RIGHTS):
            out.append((e, s))
    return out


def derive(r, topology_policy=("single_core", "single_core_multi_call")):
    r = adapt(r)
    strict = (all(r.get(b) is False for b in STRICT_BITS)
              and r.get("internal_visibility") == "api_only")
    signals = r.get("signals", [])
    reward = any(sig_is_reward(s) for s in signals)
    s0 = (strict and r.get("core_topology") in topology_policy
          and r.get("core_native_modality") in {"audio_native", "omni_native"})
    live = valid_live_edges(r)
    # CE-v3 patch (isolated non-implementer refutation __fixture__cross_use_
    # synth_splice): the same-signal tightening carried down to USE granularity
    # — the live edge's OWN signal_use must itself be a reward use; an inert
    # reward-qualifying use elsewhere on the signal cannot promote a pure
    # synthesis edge into reward-guided control.
    rq = (r.get("control_horizon") == "sequential"
          and any(sig_is_reward(s) and e.get("signal_use") in REWARD_USES
                  for e, s in live))
    rgs = (r.get("candidate_pool_exists") is True
           and r.get("selection_policy") in {"scored_select", "tournament_select"}
           and r.get("selection_object") != "none"
           and any(sig_is_reward(s) and ({"select", "prune"} & set(s.get("uses", [])))
                   for s in signals))
    facts = {"data_access_strict_bits": strict, "is_reward_guided": reward,
             "is_s0_core_compatible": s0, "is_rq_sys_control_compatible": rq,
             "is_project_method_candidate": s0 and rq, "reward_guided_selection": rgs,
             "n_valid_live_edges": len(live), "n_signals": len(signals)}
    if len(signals) == 1:
        facts["signal_form"] = signals[0].get("form")
        facts["signal_source"] = signals[0].get("source")
        facts["signal_lifecycle"] = signals[0].get("lifecycle")
    return facts


ALIAS = {"is_project_identity_candidate": "is_project_method_candidate"}


def run_expectations(cases, rows, label, policy=("single_core", "single_core_multi_call")):
    by_id = {r["method_path_id"]: r for r in rows}
    failures = []
    for pid, spec in cases.items():
        r = spec.get("row") or by_id.get(pid)
        if r is None:
            failures.append(f"{label}:{pid}: row missing")
            continue
        facts = dict(adapt(r))
        facts.update(derive(r, policy))
        for k, v in spec["expect"].items():
            k2 = ALIAS.get(k, k)
            if facts.get(k2) != v:
                failures.append(f"{label}:{pid}: expect {k2}={v}, got {facts.get(k2)}")
    return failures


def base_row(**kw):
    r = {"method_path_id": "__fixture__", "paper_work_id": "__fx__", "core_topology": "single_core",
         "core_native_modality": "text_only", "internal_visibility": "api_only",
         "core_io_modality": "text_in_text_out", "core_weight_update": False,
         "external_component_weight_update": False, "controller_program_or_config_optimized_on_labels": False,
         "human_or_dev_label_model_selection": False, "deployment_label_access": False,
         "test_item_gold_access": False, "inference_external_new_information": False,
         "signal_form": "none", "signal_source": "none", "signal_lifecycle": "none", "signal_use": [],
         "control_horizon": "terminal", "decision_rights": [], "control_edges": [],
         "selection_object": "none", "terminal_operator": "none",
         "explicit_candidate_pool_selection": False, "candidate_pool_exists": False,
         "selection_policy": "none", "includes_speech_audio": False, "adjudication_required": False}
    r.update(kw)
    return r


def fx_edge(u, d, lc=None):
    e = {"signal_use": u, "decision_right": d, "source_locator": "fixture-locator",
         "edge_semantics": "fixture edge"}
    if lc:
        e["signal_lifecycle"] = lc
    return e


def row_hash(mp):
    core = {k: v for k, v in mp.items() if k not in ADJ_EXCLUDE}
    blob = json.dumps(core, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def validate(rows):
    bad = []
    for r in rows:
        pid = r.get("method_path_id", "?")
        for f, dom in ENUMS_ROW.items():
            if r.get(f) not in dom:
                bad.append(f"{pid}:{f}")
        if r.get("internal_visibility") not in VIS:
            bad.append(f"{pid}:internal_visibility")
        for b in STRICT_BITS:
            if r.get(b) not in (True, False, "unknown"):
                bad.append(f"{pid}:{b}")
        for f in ("explicit_candidate_pool_selection", "includes_speech_audio", "adjudication_required"):
            if not isinstance(r.get(f), bool):
                bad.append(f"{pid}:{f}")
        for f in LINEAGE:
            if not r.get(f):
                bad.append(f"{pid}:lineage:{f}")
        if r.get("candidate_pool_exists") not in (True, False, "unknown"):
            bad.append(f"{pid}:candidate_pool_exists")
        if r.get("adjudication_status") not in ADJ_STATUS:
            bad.append(f"{pid}:adjudication_status")
        if not set(r.get("decision_rights", [])) <= RIGHTS:
            bad.append(f"{pid}:rights")
        if r.get("explicit_candidate_pool_selection") != (r.get("selection_object") != "none"):
            bad.append(f"{pid}:pool-consistency")
        if r.get("candidate_pool_exists") is False and r.get("selection_policy") != "none":
            bad.append(f"{pid}:policy-without-pool")
        sigs = {}
        for s in r.get("signals", []):
            sid = s.get("signal_id")
            if not sid or sid in sigs:
                bad.append(f"{pid}:signal-id")
            sigs[sid] = s
            if s.get("form") not in SIG_FORM or s.get("source") not in SIG_SRC or s.get("lifecycle") not in SIG_LC:
                bad.append(f"{pid}:signal-enums:{sid}")
            if not set(s.get("uses", [])) <= SIGNAL_USE or not s.get("evidence"):
                bad.append(f"{pid}:signal-uses/evidence:{sid}")
        for e in r.get("control_edges", []):
            if not (isinstance(e, dict) and e.get("signal_id") and e.get("signal_use")
                    and e.get("decision_right") and e.get("source_locator") and e.get("edge_semantics")):
                bad.append(f"{pid}:edge-shape")
                continue
            s = sigs.get(e["signal_id"])
            if s is None:
                bad.append(f"{pid}:edge-unknown-signal:{e['signal_id']}")
                continue
            # v9-review P0-A: the edge structural contract is ENFORCED, never
            # silently skipped (E1) — an inconsistent edge fails the row.
            if e.get("signal_lifecycle") and e["signal_lifecycle"] != s.get("lifecycle"):
                bad.append(f"{pid}:edge-signal-lifecycle-mismatch:{e['signal_id']}")
            if e.get("signal_use") not in s.get("uses", []):
                bad.append(f"{pid}:edge-use-not-in-signal:{e['signal_id']}:{e.get('signal_use')}")
            if e.get("decision_right") not in r.get("decision_rights", []):
                bad.append(f"{pid}:edge-right-not-in-row:{e.get('decision_right')}")
            if e.get("decision_right") not in ALLOWED.get(e.get("signal_use"), ()):
                bad.append(f"{pid}:edge-relation-not-whitelisted:{e.get('signal_use')}->{e.get('decision_right')}")
    ids = [r.get("method_path_id") for r in rows]
    if len(ids) != len(set(ids)):
        bad.append("duplicate-method-path-id")
    return bad


# ---------- reconciliation ----------

def load_sidecar_docs():
    paths = sorted(glob.glob(os.path.join(SIDECAR_DIR, "*.sidecar.json")))
    return [(os.path.basename(p), json.load(io.open(p, encoding="utf-8"))) for p in paths]


def ledger_index(rel):
    p = os.path.join(REPO, rel.replace("/", os.sep))
    if not os.path.exists(p):
        return None
    idx = []
    for l in io.open(p, encoding="utf-8"):
        if not l.strip():
            continue
        x = json.loads(l)
        xid = x.get("arxiv_id") or x.get("id")
        kind = x.get("kind") or ("pdf" if str(x.get("url", "")).endswith(".pdf") else None)
        idx.append({"id": xid, "kind": kind, "sha256": x.get("sha256"), "stored_at": x.get("stored_at")})
    return idx


def canon_sections(path):
    text = io.open(os.path.join(REPO, path.replace("/", os.sep)), encoding="utf-8").read()
    sections, cur_key, cur = {}, None, []
    for line in text.splitlines():
        m = re.match(r"^##\s+(\S+)", line)
        if m and not line.startswith("###"):
            if cur_key:
                sections[cur_key] = "\n".join(cur)
            cur_key, cur = m.group(1), [line]
        elif cur_key:
            cur.append(line)
    if cur_key:
        sections[cur_key] = "\n".join(cur)
    return sections


def _norm(s):
    s = re.sub(r"\\[a-zA-Z]+", " ", s)
    return re.sub(r"\s+", " ", re.sub(r"[\\${}~]", "", s)).strip().lower()


_tex_cache = {}
_pdf_cache = {}


def tex_text(stored_at):
    key = stored_at
    if key in _tex_cache:
        return _tex_cache[key]
    p = resolve_asset_path(stored_at).replace("/", os.sep)
    text = ""
    if os.path.exists(p):
        try:
            with tarfile.open(p, "r:gz") as tf:
                for m in tf.getmembers():
                    if m.name.endswith(".tex"):
                        text += tf.extractfile(m).read().decode("utf-8", errors="replace")
        except tarfile.ReadError:
            with gzip.open(p, "rb") as f:
                text = f.read().decode("utf-8", errors="replace")
    _tex_cache[key] = _norm(text)
    return _tex_cache[key]


def pdf_reader(stored_at):
    key = stored_at
    if key in _pdf_cache:
        return _pdf_cache[key]
    p = resolve_asset_path(stored_at).replace("/", os.sep)
    reader = None
    if os.path.exists(p):
        try:
            import pypdf
            reader = pypdf.PdfReader(p)
        except Exception:
            reader = None
    _pdf_cache[key] = reader
    return reader


def _anchor_on_pages(reader, n, anchor):
    npages = len(reader.pages)
    for i in range(max(0, n - 2), min(npages, n + 1)):
        try:
            if anchor.lower() in (reader.pages[i].extract_text() or "").lower():
                return True
        except Exception:
            pass
    return False


def check_page_tokens(locator, reader, pid, what, fails):
    """Every pN token must be within the pinned PDF's page range AND carry a
    non-empty ASCII anchor found on pages N-1..N+1 (v9-review E3: an in-range
    page number alone is not a resolved locator)."""
    for m in PAGE_TOKEN.finditer(locator or ""):
        n = int(m.group(1))
        anchor = m.group(2)
        if not anchor:
            fails.append(f"{pid}:{what}:page-token-without-anchor:p{n}")
            continue
        if reader is None:
            fails.append(f"{pid}:{what}:pdf-unreadable-for-page-check")
            return
        npages = len(reader.pages)
        if not (1 <= n <= npages):
            fails.append(f"{pid}:{what}:page-out-of-range:p{n}/{npages}")
            continue
        if not _anchor_on_pages(reader, n, anchor):
            fails.append(f"{pid}:{what}:page-anchor-missing:p{n}:{anchor}")


def check_quotes(locator, section_text, tex_norm, pid, what, fails):
    quotes = QUOTE_PAT.findall(locator or "")
    for kind, q in quotes:
        if kind == "canon":
            if not (section_text and q in section_text):
                fails.append(f"{pid}:{what}:canon-quote-missing:'{q[:30]}'")
        else:
            if not (tex_norm and _norm(q) in tex_norm):
                fails.append(f"{pid}:{what}:tex-quote-missing:'{q[:30]}'")
    if not quotes and not PAGE_TOKEN.search(locator or ""):
        fails.append(f"{pid}:{what}:locator-unverifiable:'{(locator or '')[:30]}'")


def check_evidence_entry(fe, expected, field, section_text, tex_norm, reader, pid, fails):
    fv = fe.get("value")
    same = (set(expected) == set(fv)) if isinstance(expected, list) and isinstance(fv, list) \
        else (expected == fv)
    if not same:
        fails.append(f"{pid}:evidence-value-mismatch:{field}")
    kind = fe.get("kind")
    if kind == "canon":
        q = fe.get("quote", "")
        if not (section_text and q in section_text):
            fails.append(f"{pid}:evidence-quote-missing:{field}")
    elif kind == "tex":
        q = fe.get("quote", "")
        if not (tex_norm and _norm(q) in tex_norm):
            fails.append(f"{pid}:evidence-tex-quote-missing:{field}")
    elif kind == "pdf_page":
        # v9-review §4.4: declared-but-unimplemented kind is now implemented:
        # page within pinned PDF range + anchor found on pages N-1..N+1.
        n, anchor = fe.get("page"), fe.get("anchor")
        if not (isinstance(n, int) and anchor):
            fails.append(f"{pid}:pdf-page-entry-incomplete:{field}")
        elif reader is None:
            fails.append(f"{pid}:pdf-page-unreadable:{field}")
        elif not (1 <= n <= len(reader.pages)):
            fails.append(f"{pid}:pdf-page-out-of-range:{field}:p{n}/{len(reader.pages)}")
        elif not _anchor_on_pages(reader, n, anchor):
            fails.append(f"{pid}:pdf-page-anchor-missing:{field}:p{n}:{anchor}")
    elif kind == "absence":
        if not fe.get("note") or not fe.get("scope"):
            fails.append(f"{pid}:absence-entry-incomplete:{field}")
    else:
        fails.append(f"{pid}:evidence-kind-invalid:{field}")


def reconcile(sidecars, coding_text):
    fails = []
    try:
        expected = render(sidecars)
    except SystemExit as e:
        return [f"generator:{e}"]
    if coding_text != expected:
        fails.append("single-write:coding-not-byte-identical-to-generator-output")
    ledgers, sections_cache = {}, {}
    for name, sc in sidecars:
        wid = sc.get("paper_work_id")
        ft = sc.get("fulltext", {})
        lref = ft.get("ledger")
        if lref not in ledgers:
            ledgers[lref] = ledger_index(lref) if lref else None
        idx = ledgers[lref]
        row_hit = None
        if idx is None:
            fails.append(f"{wid}:ledger-missing:{lref}")
        else:
            row_hit = next((x for x in idx if x["id"] == ft.get("id") and x["kind"] == ft.get("kind")
                            and x["sha256"] == ft.get("sha256") and x["sha256"]), None)
            if row_hit is None:
                fails.append(f"{wid}:ledger-row-binding-failed:id+kind+sha256")
        if ft.get("id") != wid:
            fails.append(f"{wid}:fulltext-id-mismatch:{ft.get('id')}")
        cfile, _, anchor = (sc.get("canonical_record_id") or "").partition("#")
        if cfile not in sections_cache:
            try:
                sections_cache[cfile] = canon_sections(cfile)
            except FileNotFoundError:
                sections_cache[cfile] = None
        secs = sections_cache[cfile]
        section_text = None
        if secs is None:
            fails.append(f"{wid}:canon-file-missing:{cfile}")
        elif anchor not in secs:
            fails.append(f"{wid}:canon-heading-unresolved:#{anchor}")
        else:
            section_text = secs[anchor]
        if anchor != wid:
            fails.append(f"{wid}:anchor-vs-work-id:{anchor}")
        tex_norm = ""
        reader = None
        if row_hit and row_hit.get("stored_at"):
            if ft.get("kind") == "eprint":
                tex_norm = tex_text(row_hit["stored_at"])
                if not tex_norm:
                    fails.append(f"{wid}:eprint-unreadable:{row_hit['stored_at']}")
            elif ft.get("kind") == "pdf":
                reader = pdf_reader(row_hit["stored_at"])
        for mp in sc.get("method_paths", []):
            pid = mp.get("method_path_id", "?")
            if not pid.startswith(wid + "#"):
                fails.append(f"{pid}:method-path-prefix-vs-work-id:{wid}")
            check_quotes(mp.get("source_locator"), section_text, tex_norm, pid, "row-locator", fails)
            check_page_tokens(mp.get("source_locator"), reader, pid, "row-locator", fails)
            sig_ids = set()
            for s in mp.get("signals", []):
                sid = s.get("signal_id")
                sig_ids.add(sid)
                check_quotes(s.get("evidence"), section_text, tex_norm, pid, f"signal:{sid}", fails)
                check_page_tokens(s.get("evidence"), reader, pid, f"signal:{sid}", fails)
                # v9-review P0-B: signal-level field binding — form/lifecycle/
                # uses must each declare which evidence supports which value.
                sce = s.get("claim_evidence") or {}
                for key in ("form", "lifecycle", "uses"):
                    fe = sce.get(key)
                    if fe is None:
                        fails.append(f"{pid}:signal-evidence-missing:{sid}:{key}")
                        continue
                    check_evidence_entry(fe, s.get(key), f"signal:{sid}:{key}",
                                         section_text, tex_norm, reader, pid, fails)
            for e in mp.get("control_edges", []):
                if e.get("signal_id") not in sig_ids:
                    fails.append(f"{pid}:edge-references-unknown-signal:{e.get('signal_id')}")
                check_quotes(e.get("source_locator"), section_text, tex_norm, pid, "edge-locator", fails)
                check_page_tokens(e.get("source_locator"), reader, pid, "edge-locator", fails)
            ce = mp.get("claim_evidence") or {}
            for field in REQ_FIELDS:
                fe = ce.get(field)
                if fe is None:
                    fails.append(f"{pid}:required-evidence-missing:{field}")
                    continue
                check_evidence_entry(fe, mp.get(field), field, section_text, tex_norm,
                                     reader, pid, fails)
            coder = mp.get("coder") or sc.get("coder")
            adj = mp.get("semantic_adjudicator")
            if coder in (None, "", "W1") or adj in (None, "", "W1"):
                fails.append(f"{pid}:actor-id-invalid")
            if mp.get("load_bearing"):
                if mp.get("adjudication_status") != "adjudicated_agree":
                    fails.append(f"{pid}:load-bearing-not-adjudicated:{mp.get('adjudication_status')}")
                elif mp.get("adjudication_row_sha256") != row_hash(mp):
                    fails.append(f"{pid}:adjudication-row-hash-mismatch (post-adjudication change)")
                if coder == adj:
                    fails.append(f"{pid}:coder==adjudicator on load-bearing row")
    return fails


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    coding_text = io.open(CODING, encoding="utf-8").read()
    rows = json.loads(coding_text)["rows"]
    sidecars = load_sidecar_docs()
    checks = []

    def check(cid, desc, ok, detail=""):
        checks.append({"id": cid, "check": desc, "result": "PASS" if ok else "FAIL", "detail": str(detail)})

    bad = validate(rows)
    check("V1", f"通用 validator(signals/edges/三态位/无硬编码行数;{len(rows)} 行/{len(sidecars)} sidecar)",
          not bad, f"{bad[:6]}")

    unk1 = derive(base_row(core_native_modality="unknown"))
    unk2 = derive(base_row(core_native_modality="omni_native", core_weight_update="unknown"))
    check("V2", "unknown 不满足合取(含 strict 位三态:unknown 不默认 False)",
          unk1["is_project_method_candidate"] is False
          and unk2["data_access_strict_bits"] is False and unk2["is_s0_core_compatible"] is False)

    k1 = base_row(core_native_modality="audio_native")
    k2 = base_row(core_native_modality="omni_native", signal_form="verifiable_outcome",
                  signal_source="environment", signal_lifecycle="online_step",
                  signal_use=["tool_call", "stop_budget"], control_horizon="sequential",
                  decision_rights=["tool_call", "stop"],
                  control_edges=[fx_edge("tool_call", "tool_call"), fx_edge("stop_budget", "stop")])
    k3 = base_row(signal_form="verifiable_outcome", signal_source="environment",
                  signal_lifecycle="online_step", signal_use=["retry", "stop_budget"],
                  control_horizon="sequential", decision_rights=["retry", "stop"],
                  control_edges=[fx_edge("retry", "retry")])
    k4 = base_row(signal_form="scalar_score", signal_source="llm_judge", signal_lifecycle="online_step",
                  signal_use=["select"], control_horizon="sequential", decision_rights=["memory_write"])
    k5 = base_row(signal_form="scalar_score", signal_source="llm_judge", signal_lifecycle="online_step",
                  signal_use=["select"], control_horizon="sequential", decision_rights=["memory_write"],
                  control_edges=[fx_edge("select", "memory_write")])
    k6 = base_row(signal_form="pairwise_comparison", signal_source="llm_judge", signal_lifecycle="terminal",
                  signal_use=["select"], control_horizon="sequential", decision_rights=["memory_write"])
    k7 = base_row(core_native_modality="omni_native", signal_form="pairwise_comparison",
                  signal_source="llm_judge", signal_lifecycle="terminal", signal_use=["select"],
                  control_horizon="sequential", decision_rights=["branch"],
                  control_edges=[fx_edge("select", "branch")])
    d = {k: derive(v) for k, v in dict(k1=k1, k2=k2, k3=k3, k4=k4, k5=k5, k6=k6, k7=k7).items()}
    check("V3", "killers K1–K7(K7=terminal 边前向权经白名单走私必假)",
          (d["k1"]["is_s0_core_compatible"] and not d["k1"]["is_project_method_candidate"]
           and d["k2"]["is_rq_sys_control_compatible"] and d["k2"]["is_project_method_candidate"]
           and d["k3"]["is_reward_guided"]
           and not d["k4"]["is_rq_sys_control_compatible"]
           and not d["k5"]["is_rq_sys_control_compatible"]
           and not d["k6"]["is_rq_sys_control_compatible"]
           and not d["k7"]["is_rq_sys_control_compatible"] and d["k7"]["is_reward_guided"]),
          {k: v["is_rq_sys_control_compatible"] for k, v in d.items()})

    # A1–A7 acceptance (v8-review §4.5)
    a1_row = base_row(signal_form="scalar_score", signal_source="llm_judge",
                      signal_lifecycle="online_step", signal_use=["revise"],
                      control_horizon="sequential", decision_rights=["retry"],
                      control_edges=[fx_edge("revise", "retry", "terminal")])  # mismatched edge lifecycle
    a1_derive = derive(a1_row)
    a1_val = validate([dict(adapt(a1_row), load_bearing=False, adjudication_status="adjudicated_agree",
                            fulltext_ref="x", canonical_record_id="x", source_locator="x",
                            coder="fx", semantic_adjudicator="fx2")])
    a2 = base_row(core_native_modality="omni_native",
                  signals=[{"signal_id": "s_reward", "form": "scalar_score", "source": "llm_judge",
                            "lifecycle": "terminal", "uses": ["select"], "evidence": "fixture"},
                           {"signal_id": "s_route", "form": "text_critique", "source": "llm_judge",
                            "lifecycle": "online_step", "uses": ["route"], "evidence": "fixture"}],
                  control_horizon="sequential", decision_rights=["tool_call"],
                  control_edges=[{"signal_id": "s_route", "signal_use": "route",
                                  "decision_right": "tool_call", "source_locator": "fixture-locator",
                                  "edge_semantics": "route signal controls tool call"}])
    d2 = derive(a2)
    a3 = derive(base_row(signal_form="scalar_score", signal_source="llm_judge",
                         signal_lifecycle="online_step", signal_use=["revise"],
                         control_horizon="sequential", decision_rights=["retry"],
                         control_edges=[fx_edge("revise", "retry")]))
    a4 = derive(base_row(signal_form="pairwise_comparison", signal_source="llm_judge",
                         signal_lifecycle="terminal", signal_use=["select", "prune"],
                         control_horizon="sequential", decision_rights=["stop"],
                         control_edges=[fx_edge("prune", "stop")]))
    a6_bad = derive(base_row(signal_form="scalar_score", signal_source="llm_judge",
                             signal_lifecycle="online_step", signal_use=["revise"],
                             selection_object="candidate_output",
                             explicit_candidate_pool_selection=True,
                             candidate_pool_exists=True, selection_policy="scored_select"))
    a7 = derive(base_row(signal_form="scalar_score", signal_source="llm_judge",
                         signal_lifecycle="offline_calibration", signal_use=["select"],
                         selection_object="candidate_output",
                         explicit_candidate_pool_selection=True,
                         candidate_pool_exists=True, selection_policy="scored_select"))
    check("V3a", "验收 A1(边/信号 lifecycle 失配=validator 红+派生不计)/A2(异信号拼接≠rq)/"
          "A3 正控/A4(terminal reward 边只达 stop|synthesize)/A6(rgs 需同信号 select|prune)/"
          "A7(offline calibration 永不 rgs)",
          (any("lifecycle-mismatch" in b for b in a1_val) and a1_derive["is_rq_sys_control_compatible"] is False
           and d2["is_reward_guided"] and not d2["is_rq_sys_control_compatible"]
           and not d2["is_project_method_candidate"]
           and a3["is_rq_sys_control_compatible"]
           and a4["is_rq_sys_control_compatible"]
           and not a6_bad["reward_guided_selection"]
           and not a7["reward_guided_selection"] and not a7["is_reward_guided"]),
          f"A2 reward={d2['is_reward_guided']} rq={d2['is_rq_sys_control_compatible']}")

    author_cases = {
        "2604.16529#pdr-random-k": {"expect": {"is_reward_guided": False, "n_signals": 0,
                                               "candidate_pool_exists": True, "reward_guided_selection": False}},
        "2604.16529#rtv": {"expect": {"is_reward_guided": True, "is_rq_sys_control_compatible": False,
                                      "reward_guided_selection": True}},
        "2604.16529#rtv-pdr-pipeline": {"expect": {"is_reward_guided": True, "is_rq_sys_control_compatible": True}},
        "2602.16485#calibrated-orchestration": {"expect": {"is_reward_guided": False,
                                                            "is_rq_sys_control_compatible": False}},
        "2606.03054#trained-gate": {"expect": {"signal_form": "binary_gate", "is_reward_guided": False,
                                               "is_rq_sys_control_compatible": False, "n_valid_live_edges": 1}},
        "2606.01667#agentic-orchestration": {"expect": {"is_reward_guided": False,
                                                         "is_rq_sys_control_compatible": False,
                                                         "n_valid_live_edges": 3}},
        "2605.08083#discovered-controller": {"expect": {"is_reward_guided": False, "n_signals": 2,
                                                         "is_rq_sys_control_compatible": False,
                                                         "n_valid_live_edges": 2}},
        "2026.findings-acl.1724#pipeline": {"expect": {"is_reward_guided": True, "n_signals": 2,
                                                        "is_rq_sys_control_compatible": True,
                                                        "data_access_strict_bits": False}},
        "2026.findings-acl.1243#closed-prompt-only": {"expect": {"is_rq_sys_control_compatible": True}},
        "2026.findings-acl.1243#open-sft-variant": {"expect": {"is_rq_sys_control_compatible": True,
                                                                "core_native_modality": "text_only"}},
        "2026.findings-acl.511#prm-guided-search": {"expect": {"is_rq_sys_control_compatible": True}},
    }
    f3 = run_expectations(author_cases, rows, "author")
    check("V3b", "作者反例集(多信号身份 A5:AutoTTS 双相位/STTS 双 judge 在案)", not f3, f"{f3}")

    mut1 = copy.deepcopy(rows)
    for r in mut1:
        if r["method_path_id"] == "2026.findings-acl.1724#pipeline":
            for s in r["signals"]:
                s["form"] = "consensus_vote"
    mut2 = copy.deepcopy(rows)
    for r in mut2:
        if r["method_path_id"] == "2604.16529#pdr-random-k":
            r["signals"] = [{"signal_id": "s_bad", "form": "pairwise_comparison", "source": "llm_judge",
                            "lifecycle": "online_step", "uses": ["prune", "supply"], "evidence": "x"}]
    check("V4", "负控:STTS 信号改名必须红;PDR 错码信号回填必须红",
          bool(run_expectations(author_cases, mut1, "author"))
          and bool(run_expectations(author_cases, mut2, "author")))

    f5all, n_ce = [], 0
    for pth in (INDEP, INDEP2, INDEP3):
        if os.path.exists(pth):
            indep = json.load(io.open(pth, encoding="utf-8"))
            f5all += run_expectations(indep["cases"], rows, os.path.basename(pth))
            n_ce += len(indep["cases"])
    check("V5", f"独立语义反例 x{n_ce}(v1+v2+v3,legacy 经 adapter)", n_ce > 0 and not f5all, f"{f5all[:6]}")

    atlas = next(r for r in rows if r["method_path_id"] == "2606.01667#agentic-orchestration")
    atlas_omni = dict(atlas, core_native_modality="omni_native")
    sens_a = derive(atlas_omni, ("single_core", "single_core_multi_call"))["is_s0_core_compatible"]
    sens_b = derive(atlas_omni, ("single_core",))["is_s0_core_compatible"]
    check("V5b", "CE-1b 拓扑蕴含敏感列非空洞", sens_a is True and sens_b is False, f"A={sens_a} strict={sens_b}")

    def occupancy(policy, rws):
        dd = [dict(adapt(r), **derive(r, policy)) for r in rws]
        works = sorted({r["paper_work_id"] for r in dd})
        n, w = len(dd), len(works)
        by_obj = {}
        for r in dd:
            if r["data_access_strict_bits"] and r["is_reward_guided"] and r["explicit_candidate_pool_selection"]:
                by_obj.setdefault(r["selection_object"], []).append(r["method_path_id"])
        def dual(paths):
            uw = sorted({next(r["paper_work_id"] for r in dd if r["method_path_id"] == p) for p in paths})
            return {"method_paths": sorted(paths), "n_paths": f"{len(paths)}/{n}",
                    "unique_works": uw, "n_works": f"{len(uw)}/{w}"}
        return {
            "n_method_paths": n, "n_unique_works": w,
            "is_reward_guided": dual([r["method_path_id"] for r in dd if r["is_reward_guided"]]),
            "is_rq_sys_control_compatible": dual([r["method_path_id"] for r in dd if r["is_rq_sys_control_compatible"]]),
            "is_s0_core_compatible": dual([r["method_path_id"] for r in dd if r["is_s0_core_compatible"]]),
            "is_project_method_candidate": dual([r["method_path_id"] for r in dd if r["is_project_method_candidate"]]),
            "strict_AND_reward_AND_pool_BY_selection_object(mechanism)": {k: dual(v) for k, v in sorted(by_obj.items())},
            "reward_guided_selection": dual([r["method_path_id"] for r in dd if r["reward_guided_selection"]]),
            "learned_rm_prm_AND_pool": dual([r["method_path_id"] for r in dd
                                             if any(s.get("source") == "learned_rm_prm" for s in r.get("signals", []))
                                             and r["explicit_candidate_pool_selection"]]),
            "core_native_audio_or_omni": dual([r["method_path_id"] for r in dd
                                               if r["core_native_modality"] in ("audio_native", "omni_native")]),
        }

    occ = {"policy_A": occupancy(("single_core", "single_core_multi_call"), rows),
           "sensitivity_strict_topology": occupancy(("single_core",), rows)}
    occ2 = {"policy_A": occupancy(("single_core", "single_core_multi_call"), rows),
            "sensitivity_strict_topology": occupancy(("single_core",), rows)}
    n_rows, n_works = len(rows), len({r["paper_work_id"] for r in rows})
    check("V6", "occupancy 真断言:重算两次同构;分母=len(rows)/unique(paper_work_id);双政策持久化",
          (occ == occ2 and occ["policy_A"]["n_method_paths"] == n_rows
           and occ["policy_A"]["n_unique_works"] == n_works
           and occ["policy_A"]["is_reward_guided"]["n_paths"].endswith(f"/{n_rows}")),
          f"paths={n_rows} works={n_works}")

    f7 = reconcile(sidecars, coding_text)
    check("V7", "真 reconciliation:单写字节等同/ledger 同行绑定(路径经 resolver)/节标题解析/"
          "canon|tex 引文+PDF 页码范围/签名与边证据/required-evidence 完备/actor+裁决行哈希", not f7, f"{f7[:8]}")

    # The mutation harness runs on a SIM-ADJUDICATED copy: every row stamped
    # adjudicated_agree with its row-hash, so post-adjudication-change classes
    # (horizon flip, double-flip) are exercised. Its baseline must be CLEAN —
    # a dirty harness baseline would make every mutation vacuously "red".
    stamped = copy.deepcopy(sidecars)
    for _, sc in stamped:
        for mp in sc["method_paths"]:
            mp["semantic_adjudicator"] = "sim-adj:harness"
            mp["adjudication_status"] = "adjudicated_agree"
            mp["adjudication_row_sha256"] = row_hash(mp)
    stamped_coding = render(stamped)
    harness_baseline = set(reconcile(stamped, stamped_coding))
    baseline_val = set(validate(json.loads(stamped_coding)["rows"]))
    mut_results = {}

    def mutate(tag, fn_sc=None, fn_coding=None, expect_kind=None, restamp=False):
        """restamp=True simulates the NEW-ROW flow (v9-review Round C): the
        error enters BEFORE adjudication and the row hash is legitimately
        recomputed — catches must come from validator/evidence contracts,
        never from the row hash."""
        scs = copy.deepcopy(stamped)
        ct = stamped_coding
        if fn_sc:
            fn_sc(scs)
            if restamp:
                for _, sc in scs:
                    for mp in sc["method_paths"]:
                        mp["adjudication_row_sha256"] = row_hash(mp)
            ct = render(scs) if fn_coding is None else ct
        if fn_coding:
            ct = fn_coding(ct)
        new_recon = set(reconcile(scs, ct)) - harness_baseline
        new_val = set(validate(json.loads(ct)["rows"])) - baseline_val
        new = new_recon | new_val
        mut_results[tag] = sorted(new)[:3]
        ok = bool(new)
        if expect_kind:
            ok = ok and any(expect_kind in f for f in new)
        return ok

    def sc_of(scs, wid):
        return next(sc for _, sc in scs if sc["paper_work_id"] == wid)

    def mut_wrong_work(scs):
        sc = sc_of(scs, "2606.01667")
        sc["paper_work_id"] = "bogus-work"
        sc["fulltext"]["id"] = "bogus-work"

    def mut_horizon(scs):
        sc_of(scs, "2026.findings-acl.1243")["method_paths"][1]["control_horizon"] = "terminal"

    def mut_horizon_double_flip(scs):
        mp = sc_of(scs, "2026.findings-acl.1243")["method_paths"][1]
        mp["control_horizon"] = "terminal"
        mp["claim_evidence"]["control_horizon"]["value"] = "terminal"

    def mut_fake_page(scs):
        mp = sc_of(scs, "2606.01667")["method_paths"][0]
        mp["source_locator"] = "canon: '独占 explore/stop 决策' (p9999 explore)"

    def mut_lifecycle(scs):
        mp = sc_of(scs, "2026.findings-acl.1243")["method_paths"][1]
        mp["control_edges"][0]["signal_lifecycle"] = "terminal"

    def mut_signal_identity(scs):
        mp = sc_of(scs, "2026.findings-acl.511")["method_paths"][0]
        mp["control_edges"][0]["signal_id"] = "s_ghost"

    def mut_wrong_right(scs):
        mp = sc_of(scs, "2026.findings-acl.1724")["method_paths"][0]
        mp["decision_rights"] = ["memory_write"]

    def mut_wrong_policy(scs):
        mp = sc_of(scs, "2604.16529")["method_paths"][1]
        mp["selection_policy"] = "scored_select"

    def mut_wrong_modality(scs):
        sc_of(scs, "2606.01667")["method_paths"][0]["core_native_modality"] = "text_only"

    def mut_wrong_sha(scs):
        sc_of(scs, "2606.01667")["fulltext"]["sha256"] = "0" * 64

    def mut_wrong_kind(scs):
        sc_of(scs, "2606.01667")["fulltext"]["kind"] = "eprint"

    def mut_nonsense(scs):
        sc_of(scs, "2606.01667")["method_paths"][0]["source_locator"] = "nonsense"

    def mut_e1_edge_use(scs):
        mp = sc_of(scs, "2026.findings-acl.1724")["method_paths"][0]
        mp["control_edges"][0]["signal_use"] = "select"

    def mut_e2_signal_evidence_page(scs):
        sc_of(scs, "2606.01667")["method_paths"][0]["signals"][0]["evidence"] = "p9999"

    def mut_e3_bare_page(scs):
        sc_of(scs, "2606.01667")["method_paths"][0]["source_locator"] = "p1"

    def mut_e4_signal_form(scs):
        sc_of(scs, "2026.findings-acl.1724")["method_paths"][0]["signals"][0]["form"] = "text_critique"

    m_ok = not harness_baseline and all([
        mutate("E1_edge_use_flip", mut_e1_edge_use, restamp=True,
               expect_kind="edge-use-not-in-signal"),
        mutate("E2_signal_evidence_p9999", mut_e2_signal_evidence_page, restamp=True,
               expect_kind="page"),
        mutate("E3_bare_in_range_page", mut_e3_bare_page, restamp=True,
               expect_kind="page-token-without-anchor"),
        mutate("E4_signal_form_flip", mut_e4_signal_form, restamp=True,
               expect_kind="evidence-value-mismatch"),
        mutate("wrong_horizon", mut_horizon, expect_kind="row-hash"),
        mutate("double_flip_horizon_plus_evidence", mut_horizon_double_flip, expect_kind="row-hash"),
        mutate("fake_page_p9999", mut_fake_page, expect_kind="page-out-of-range"),
        mutate("edge_signal_lifecycle_mismatch", mut_lifecycle, expect_kind="lifecycle-mismatch"),
        mutate("edge_signal_identity_mismatch", mut_signal_identity),
        mutate("wrong_decision_right", mut_wrong_right),
        mutate("wrong_selection_policy", mut_wrong_policy),
        mutate("wrong_work", mut_wrong_work),
        mutate("wrong_modality", mut_wrong_modality),
        mutate("wrong_sha", mut_wrong_sha),
        mutate("wrong_kind", mut_wrong_kind),
        mutate("nonsense_locator", mut_nonsense),
        mutate("coding_hand_edit", fn_coding=lambda ct: ct.replace(
            '"control_horizon": "sequential"', '"control_horizon": "terminal"', 1)),
    ])
    check("V8", "敏感面突变集 17 类全 fail-closed(模拟盖章副本+基线必须净;E1–E4 走新行流程"
          "restamp——拦截必须来自 validator/证据合同而非行哈希)",
          m_ok, {"harness_baseline": sorted(harness_baseline)[:3], **mut_results})

    fixture12 = base_row(method_path_id="__fx12__#path", paper_work_id="__fx12__",
                         signal_form="scalar_score", signal_source="llm_judge",
                         signal_lifecycle="online_step", signal_use=["revise"],
                         control_horizon="sequential", decision_rights=["retry"],
                         control_edges=[fx_edge("revise", "retry")])
    occ12 = occupancy(("single_core", "single_core_multi_call"), rows + [adapt(fixture12)])
    dup_bad = validate(rows + [dict(rows[0])])
    # v9-review P0-A acceptance: a GENERIC new 12th row (no per-ID author
    # expectation anywhere) with an E1-style inconsistent edge must be
    # rejected by the general validator alone.
    good12 = dict(adapt(fixture12), load_bearing=False,
                  adjudication_status="adjudicated_agree",
                  fulltext_ref="fx", canonical_record_id="fx", source_locator="fx",
                  coder="fx-coder", semantic_adjudicator="fx-adj")
    bad12 = copy.deepcopy(good12)
    bad12["control_edges"][0]["signal_use"] = "select"  # not in signal's uses
    v_good = [b for b in validate([good12]) if "lineage" not in b]
    v_bad = validate([bad12])
    check("V9", "扩容:第12行→分母自动 /12;重复被拒;通用第12行无逐ID期望——好行净/E1式坏边行被"
          "validator 单独拒绝",
          occ12["n_method_paths"] == n_rows + 1
          and occ12["is_reward_guided"]["n_paths"].endswith(f"/{n_rows + 1}")
          and "duplicate-method-path-id" in dup_bad
          and not v_good
          and any("edge-use-not-in-signal" in b for b in v_bad),
          f"good12={v_good[:2]} bad12={[b for b in v_bad if 'edge-use' in b][:1]}")

    n_pass = sum(1 for c in checks if c["result"] == "PASS")
    report = {"artifact_id": "SF-IDENTITY-TAXONOMY-V5-TEST-2026-07-19-01",
              "inputs": {"taxonomy": os.path.relpath(TAX, REPO).replace("\\", "/"),
                         "coding": os.path.relpath(CODING, REPO).replace("\\", "/"),
                         "sidecars": [n for n, _ in sidecars]},
              "platform": {"os": os.name, "python": sys.version.split()[0]},
              "topology_policy": "A(frozen) + strict-topology sensitivity dual-computed",
              "checks": checks, "occupancy": occ, "mutation_results": mut_results,
              "summary": f"{n_pass}/{len(checks)} PASS",
              "verdict": "PASS" if n_pass == len(checks) else "FAIL"}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    payload = (json.dumps(report, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    with open(OUT, "wb") as f:
        f.write(payload)
    # v9-review P2: platform-stamped copy so neither platform's run overwrites
    # the other's evidence; sf_dual_platform_check.py asserts equality.
    with open(OUT.replace(".json", f".{os.name}.json"), "wb") as f:
        f.write(payload)
    print(json.dumps({"summary": report["summary"], "verdict": report["verdict"],
                      "platform": report["platform"],
                      "policy_A_key_numbers": {
                          "reward_guided": occ["policy_A"]["is_reward_guided"]["n_paths"],
                          "rq_sys_compatible": occ["policy_A"]["is_rq_sys_control_compatible"]["n_paths"]
                          + " (works " + occ["policy_A"]["is_rq_sys_control_compatible"]["n_works"] + ")",
                          "method_candidate": occ["policy_A"]["is_project_method_candidate"]["n_paths"],
                          "reward_guided_selection": occ["policy_A"]["reward_guided_selection"]["n_paths"],
                          "strict_reward_pool": {k: v["n_paths"] + " (works " + v["n_works"] + ")"
                                                 for k, v in occ["policy_A"]["strict_AND_reward_AND_pool_BY_selection_object(mechanism)"].items()}}},
                     ensure_ascii=False, indent=1))
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
