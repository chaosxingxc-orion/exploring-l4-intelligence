#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v4.2 package conformance checker (internal consistency check).

Loads a machine-readable rule manifest (docs/checks/v42-rules.yaml) and checks
the v4.2 "converged & locked" proposal package -- the proposal + its
accompanying response letter -- plus the claim ledger, emitting one JSON verdict
per rule.

Dependencies: Python 3 standard library + PyYAML only.

This is a MACHINE-ASSISTED INTERNAL SECOND PASS. It is NOT independent oversight
and NOT an external peer review. It verifies document-package self-consistency
against the ledger and the owner-ruling discipline; it certifies nothing about
scientific validity.

Usage:
    python scripts/checks/v42_conformance.py \
        --manifest docs/checks/v42-rules.yaml \
        --root . \
        --output docs/checks/v42-conformance-output.json

Exit code: 0 if every rule PASSES, 1 if any rule FAILS (or errors), 2 on a
usage/loading error.
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import sys

try:
    import yaml
except Exception as exc:  # pragma: no cover
    sys.stderr.write("FATAL: PyYAML is required (pip install pyyaml): %s\n" % exc)
    sys.exit(2)


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def read_lines(path):
    """Return list of lines (no trailing newline), 0-indexed. Line N of the file
    is lines[N-1]."""
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read().split("\n")


def line_has_any(line, markers):
    """Substring match; case-insensitive for ASCII, verbatim for CJK."""
    low = line.lower()
    for m in markers:
        if m in line or m.lower() in low:
            return True
    return False


def window_text(lines, idx0, radius):
    """Join lines within +/- radius of 0-indexed idx0."""
    lo = max(0, idx0 - radius)
    hi = min(len(lines), idx0 + radius + 1)
    return "\n".join(lines[lo:hi])


def excerpt(line, limit=180):
    s = line.strip()
    return s if len(s) <= limit else s[:limit] + " ..."


def region_after_marker(lines, markers):
    """Return the 0-indexed start line of the first heading line whose text
    contains one of the markers, or None."""
    for i, line in enumerate(lines):
        if line.lstrip().startswith("#") and line_has_any(line, markers):
            return i
    return None


def is_heading(line):
    return line.lstrip().startswith("#")


# --------------------------------------------------------------------------- #
# per-target compiled view
# --------------------------------------------------------------------------- #
class Doc(object):
    def __init__(self, name, relpath, root):
        self.name = name
        self.relpath = relpath
        self.abspath = os.path.join(root, relpath)
        self.exists = os.path.isfile(self.abspath)
        self.lines = read_lines(self.abspath) if self.exists else []
        self.appendix_d_start = None  # set by checker after config load
        self.appendix_a_start = None
        self.legend_lines = set()     # 0-indexed set of legend/definition lines

    def in_appendix_d(self, idx0):
        return self.appendix_d_start is not None and idx0 >= self.appendix_d_start


# --------------------------------------------------------------------------- #
# checker
# --------------------------------------------------------------------------- #
class Checker(object):
    def __init__(self, manifest, root):
        self.manifest = manifest
        self.root = root
        self.vocab = manifest.get("vocab", {})
        self.appendix_d_markers = manifest.get("appendix_d_markers", ["附录 D"])
        self.appendix_a_markers = manifest.get("appendix_a_markers", ["附录 A"])
        self.legend_markers = manifest.get("legend_markers", [])
        self.docs = {}
        for name, relpath in manifest.get("targets", {}).items():
            d = Doc(name, relpath, root)
            d.appendix_d_start = region_after_marker(d.lines, self.appendix_d_markers)
            d.appendix_a_start = region_after_marker(d.lines, self.appendix_a_markers)
            for i, line in enumerate(d.lines):
                if line_has_any(line, self.legend_markers):
                    d.legend_lines.add(i)
            self.docs[name] = d

    def vocab_of(self, key_or_list):
        """Resolve a marker list that may be given inline or as a vocab key."""
        if isinstance(key_or_list, list):
            return key_or_list
        return self.vocab.get(key_or_list, [])

    def target_docs(self, rule):
        out = []
        for name in rule.get("applies_to", []):
            d = self.docs.get(name)
            if d is not None:
                out.append(d)
        return out

    # -- rule dispatch ------------------------------------------------------ #
    def run_rule(self, rule):
        t = rule.get("type")
        handler = getattr(self, "_rule_" + t, None)
        if handler is None:
            return self._result(rule, "ERROR", violations=[
                {"reason": "no handler for rule type '%s'" % t}])
        try:
            return handler(rule)
        except Exception as exc:  # keep one bad rule from killing the run
            import traceback
            return self._result(rule, "ERROR", violations=[
                {"reason": "handler exception: %s" % exc,
                 "traceback": traceback.format_exc().splitlines()[-3:]}])

    def _result(self, rule, verdict, violations=None, notes=None, extra=None):
        violations = violations or []
        r = {
            "id": rule.get("id"),
            "type": rule.get("type"),
            "applies_to": rule.get("applies_to", []),
            "verdict": verdict,
            "n_violations": len(violations),
            "violations": violations,
        }
        if notes:
            r["notes"] = notes
        if extra:
            r.update(extra)
        return r

    # -- banned_phrase ------------------------------------------------------ #
    def _rule_banned_phrase(self, rule):
        pats = [re.compile(p, re.IGNORECASE) for p in rule.get("patterns", [])]
        allow_appendix = rule.get("allow_in_appendix_d", False)
        allow_key = rule.get("allow_if_line_has")
        allow_markers = self.vocab_of(allow_key) if allow_key else []
        violations = []
        checked = 0
        for d in self.target_docs(rule):
            for i, line in enumerate(d.lines):
                for pat in pats:
                    if pat.search(line):
                        checked += 1
                        if allow_appendix and d.in_appendix_d(i):
                            continue
                        if allow_markers and line_has_any(line, allow_markers):
                            continue
                        violations.append({
                            "file": d.relpath, "line": i + 1,
                            "match": pat.pattern, "excerpt": excerpt(line),
                            "reason": "banned phrase without an allowed context",
                        })
        return self._result(rule, "PASS" if not violations else "FAIL", violations,
                            notes="matched-occurrences=%d (allowed ones excluded)" % checked)

    # -- banned_phrase_in_titles -------------------------------------------- #
    def _rule_banned_phrase_in_titles(self, rule):
        pats = [re.compile(p, re.IGNORECASE) for p in rule.get("patterns", [])]
        allow_key = rule.get("allow_if_line_has")
        allow_markers = self.vocab_of(allow_key) if allow_key else []
        violations = []
        checked = 0
        for d in self.target_docs(rule):
            # frontmatter title: field + heading lines
            in_frontmatter = False
            for i, line in enumerate(d.lines):
                stripped = line.strip()
                if i == 0 and stripped == "---":
                    in_frontmatter = True
                    continue
                if in_frontmatter and stripped == "---":
                    in_frontmatter = False
                    continue
                is_title_line = is_heading(line) or (
                    in_frontmatter and re.match(r'^\s*title\s*:', line))
                if not is_title_line:
                    continue
                for pat in pats:
                    if pat.search(line):
                        checked += 1
                        if allow_markers and line_has_any(line, allow_markers):
                            continue
                        violations.append({
                            "file": d.relpath, "line": i + 1,
                            "match": pat.pattern, "excerpt": excerpt(line),
                            "reason": "banned phrase in a title/heading line without negation",
                        })
        return self._result(rule, "PASS" if not violations else "FAIL", violations,
                            notes="title-line matches=%d" % checked)

    # -- proximity (equal-budget near K=1) ---------------------------------- #
    def _rule_proximity(self, rule):
        anchors = [re.compile(p, re.IGNORECASE) for p in rule.get("anchor_patterns", [])]
        nears = [re.compile(p, re.IGNORECASE) for p in rule.get("near_patterns", [])]
        window = int(rule.get("window", 3))
        req_key = rule.get("require_line_has")
        req_markers = self.vocab_of(req_key) if req_key else []
        violations = []
        cooccur = 0
        for d in self.target_docs(rule):
            n = len(d.lines)
            for i, line in enumerate(d.lines):
                if not any(a.search(line) for a in anchors):
                    continue
                # is a near-pattern within +/- window lines?
                lo = max(0, i - window)
                hi = min(n, i + window + 1)
                near_hit = None
                for j in range(lo, hi):
                    if any(nb.search(d.lines[j]) for nb in nears):
                        near_hit = j
                        break
                if near_hit is None:
                    continue
                cooccur += 1
                win = window_text(d.lines, i, window)
                if req_markers and line_has_any(win, req_markers):
                    continue
                violations.append({
                    "file": d.relpath, "line": i + 1,
                    "near_line": near_hit + 1,
                    "excerpt": excerpt(line),
                    "reason": "anchor within %d lines of near-pattern lacks a "
                              "separation/negation marker in-window" % window,
                })
        return self._result(rule, "PASS" if not violations else "FAIL", violations,
                            notes="anchor-near co-occurrences=%d (separated ones excluded)" % cooccur)

    # -- future_date -------------------------------------------------------- #
    def _rule_future_date(self, rule):
        threshold = rule.get("threshold", "2026-07-13")
        ty, tm, td = [int(x) for x in threshold.split("-")]
        thr = (ty, tm, td)
        dash = re.compile(r'(?<!\d)(20\d\d)-(\d{2})-(\d{2})(?!\d)')
        cjk = re.compile(r'(20\d\d)\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日')
        violations = []
        scanned = 0
        for d in self.target_docs(rule):
            for i, line in enumerate(d.lines):
                for m in list(dash.finditer(line)) + list(cjk.finditer(line)):
                    y, mo, dy = int(m.group(1)), int(m.group(2)), int(m.group(3))
                    if mo < 1 or mo > 12 or dy < 1 or dy > 31:
                        continue  # not a real calendar date
                    scanned += 1
                    if (y, mo, dy) >= thr:
                        violations.append({
                            "file": d.relpath, "line": i + 1,
                            "date": "%04d-%02d-%02d" % (y, mo, dy),
                            "excerpt": excerpt(line),
                            "reason": "calendar date on/after threshold %s" % threshold,
                        })
        return self._result(rule, "PASS" if not violations else "FAIL", violations,
                            notes="calendar-dates scanned=%d threshold=%s" % (scanned, threshold))

    # -- required_phrase ---------------------------------------------------- #
    def _rule_required_phrase(self, rule):
        pats = [re.compile(p, re.IGNORECASE) for p in rule.get("patterns", [])]
        min_count = int(rule.get("min_count", 1))
        also_any = rule.get("must_also_have_any", [])
        violations = []
        found_total = 0
        details = {}
        for d in self.target_docs(rule):
            cnt = 0
            for line in d.lines:
                for pat in pats:
                    cnt += len(pat.findall(line))
            details[d.relpath] = cnt
            found_total += cnt
        if found_total < min_count:
            violations.append({
                "reason": "required phrase found %d time(s) across %s, need >= %d"
                          % (found_total, list(details.keys()), min_count),
                "patterns": rule.get("patterns", []),
            })
        if also_any and found_total >= min_count:
            # require the companion token somewhere in the same docs
            comp_ok = False
            for d in self.target_docs(rule):
                if any(line_has_any(line, also_any) for line in d.lines):
                    comp_ok = True
                    break
            if not comp_ok:
                violations.append({
                    "reason": "companion token %s not present" % also_any})
        return self._result(rule, "PASS" if not violations else "FAIL", violations,
                            notes="per-file counts=%s" % json.dumps(details, ensure_ascii=False))

    # -- ledger_citation ---------------------------------------------------- #
    def _rule_ledger_citation(self, rule):
        # load ledger
        ledger_doc = self.docs.get("ledger")
        if ledger_doc is None or not ledger_doc.exists:
            return self._result(rule, "ERROR", violations=[
                {"reason": "ledger target not available"}])
        with open(ledger_doc.abspath, "r", encoding="utf-8") as fh:
            entries = yaml.safe_load(fh)
        ledger = {}
        for e in (entries or []):
            if isinstance(e, dict) and "claim_id" in e:
                ledger[str(e["claim_id"]).strip()] = str(e.get("status", "")).strip()

        id_re = re.compile(rule["id_regex"])
        dwin = int(rule.get("directional_window", 2))
        iwin = int(rule.get("invalid_window", 1))
        dmark = self.vocab_of(rule.get("directional_markers", "directional_markers"))
        imark = self.vocab_of(rule.get("invalid_markers", "invalid_markers"))
        nmark = self.vocab_of(rule.get("nonexistent_markers", "nonexistent_markers"))

        violations = []
        citations = {}  # id -> list of (docname, line1, idx0)
        for name in rule.get("applies_to", []):
            d = self.docs.get(name)
            if d is None:
                continue
            for i, line in enumerate(d.lines):
                for m in id_re.finditer(line):
                    cid = m.group(0)
                    citations.setdefault(cid, []).append((d, i))

        cited_ids = sorted(citations.keys())
        directional_checked = []
        invalid_checked = []
        existence_checked = []

        for cid in cited_ids:
            occ = citations[cid]
            status = ledger.get(cid)

            # (1) existence
            if status is None:
                # allowed only if EVERY... at least one occurrence flags nonexistent
                flagged = False
                for d, i in occ:
                    if line_has_any(window_text(d.lines, i, 1), nmark):
                        flagged = True
                        break
                existence_checked.append(cid)
                if not flagged:
                    violations.append({
                        "claim_id": cid, "kind": "existence",
                        "file": occ[0][0].relpath, "line": occ[0][1] + 1,
                        "excerpt": excerpt(occ[0][0].lines[occ[0][1]]),
                        "reason": "cited ledger-form id not in ledger and not flagged nonexistent",
                    })
                continue

            # (2) directional label discipline
            if status == "directional":
                for d, i in occ:
                    if i in d.legend_lines or d.in_appendix_d(i):
                        continue
                    if not line_has_any(window_text(d.lines, i, dwin), dmark):
                        violations.append({
                            "claim_id": cid, "kind": "directional_label",
                            "file": d.relpath, "line": i + 1,
                            "excerpt": excerpt(d.lines[i]),
                            "reason": "directional claim cited without a Stage-1/"
                                      "directional label within +/-%d lines" % dwin,
                        })
                directional_checked.append(cid)

            # (3) invalid -> appendix-D / legend / explicit failure-context only
            if status == "invalid":
                for d, i in occ:
                    if d.in_appendix_d(i) or i in d.legend_lines:
                        continue
                    if not line_has_any(window_text(d.lines, i, iwin), imark):
                        violations.append({
                            "claim_id": cid, "kind": "invalid_location",
                            "file": d.relpath, "line": i + 1,
                            "excerpt": excerpt(d.lines[i]),
                            "reason": "invalid claim cited outside the failure-history "
                                      "appendix and without an invalid/failure/prevention marker",
                        })
                invalid_checked.append(cid)

        notes = ("ledger_entries=%d; cited_ids=%s; directional_checked=%s; "
                 "invalid_checked=%s; nonledger_checked=%s"
                 % (len(ledger), cited_ids, directional_checked,
                    invalid_checked, existence_checked))
        extra = {"cited_ids": cited_ids,
                 "cited_status": {c: ledger.get(c, "NOT_IN_LEDGER") for c in cited_ids}}
        return self._result(rule, "PASS" if not violations else "FAIL",
                            violations, notes=notes, extra=extra)

    # -- file_exists -------------------------------------------------------- #
    def _rule_file_exists(self, rule):
        violations = []
        checked = []
        for item in rule.get("must_exist", []):
            relpath = item["path"] if isinstance(item, dict) else item
            src = item.get("source", "") if isinstance(item, dict) else ""
            abspath = os.path.join(self.root, relpath)
            ok = os.path.exists(abspath)
            checked.append({"path": relpath, "exists": ok, "source": src})
            if not ok:
                violations.append({
                    "path": relpath, "source": src,
                    "reason": "letter claims this artifact exists, but it is missing",
                })
        return self._result(rule, "PASS" if not violations else "FAIL", violations,
                            notes="paths checked=%d" % len(checked),
                            extra={"paths": checked})

    # -- appendix_atom_count ------------------------------------------------ #
    def _rule_appendix_atom_count(self, rule):
        d = self.docs.get(rule["applies_to"][0])
        # resolve appendix markers robustly: a literal list is used as-is; a
        # string may reference vocab; fall back to the top-level appendix_a_markers.
        am = rule.get("appendix_markers")
        if isinstance(am, list):
            markers = am
        elif isinstance(am, str):
            markers = self.vocab.get(am) or self.appendix_a_markers
        else:
            markers = self.appendix_a_markers
        start = region_after_marker(d.lines, markers)
        if start is None:
            return self._result(rule, "ERROR", violations=[
                {"reason": "appendix-A heading not found"}])

        fence_lang = rule.get("fence_lang", "yaml")
        atoms_key = rule.get("atoms_key", "atoms")

        # find the first ```<lang> ... ``` fenced block after the appendix heading
        block, fstart, fend = self._extract_fenced_block(d.lines, start, fence_lang)
        atom_count = None
        method = None
        if block is not None:
            try:
                parsed = yaml.safe_load(block)
                if isinstance(parsed, dict) and isinstance(parsed.get(atoms_key), list):
                    atom_count = len(parsed[atoms_key])
                    method = "yaml_parse"
            except Exception:
                atom_count = None
        if atom_count is None and block is not None:
            # fallback: count '- hypothesis_id:' entries
            atom_count = len(re.findall(r'^\s*-\s*hypothesis_id\s*:', block, re.M))
            method = "regex_hypothesis_id"

        # prose m= claims (whole doc)
        m_re = re.compile(rule.get("m_regex", r'm\s*=\s*(\d+)'))
        m_values = sorted(set(int(x) for line in d.lines for x in m_re.findall(line)))

        # family atom-count prose claims
        fam_values = []
        fam_res = [re.compile(p) for p in rule.get("family_atom_regexes", [])]
        for line in d.lines:
            for pat in fam_res:
                for x in pat.findall(line):
                    fam_values.append(int(x))
        fam_values = sorted(set(fam_values))

        violations = []
        all_prose = sorted(set(m_values + fam_values))
        if atom_count is None:
            violations.append({"reason": "could not determine appendix-A atom count"})
        else:
            for v in all_prose:
                if v != atom_count:
                    violations.append({
                        "reason": "prose claim %d != appendix-A atom count %d" % (v, atom_count),
                    })
            if not all_prose:
                violations.append({"reason": "no prose m= / family atom-count claim found to cross-check"})

        notes = ("atom_count=%s (via %s, block lines %s-%s); m_values=%s; "
                 "family_atom_values=%s" % (atom_count, method,
                 (fstart + 1) if fstart is not None else None,
                 (fend + 1) if fend is not None else None,
                 m_values, fam_values))
        return self._result(rule, "PASS" if not violations else "FAIL", violations,
                            notes=notes,
                            extra={"atom_count": atom_count, "count_method": method,
                                   "m_values": m_values, "family_atom_values": fam_values})

    @staticmethod
    def _extract_fenced_block(lines, start_idx0, lang):
        """Return (block_text, fence_start_idx0, fence_end_idx0) for the first
        ```<lang> fenced block at or after start_idx0."""
        open_pat = re.compile(r'^\s*```+\s*' + re.escape(lang) + r'\s*$')
        close_pat = re.compile(r'^\s*```+\s*$')
        i = start_idx0
        n = len(lines)
        while i < n:
            if open_pat.match(lines[i]):
                j = i + 1
                buf = []
                while j < n and not close_pat.match(lines[j]):
                    buf.append(lines[j])
                    j += 1
                return "\n".join(buf), i, (j if j < n else n - 1)
            i += 1
        return None, None, None


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main(argv=None):
    ap = argparse.ArgumentParser(description="v4.2 package conformance checker")
    ap.add_argument("--manifest", default="docs/checks/v42-rules.yaml")
    ap.add_argument("--root", default=".", help="umbrella repo root")
    ap.add_argument("--output", default=None, help="write JSON here (also printed)")
    args = ap.parse_args(argv)

    root = os.path.abspath(args.root)
    manifest_path = args.manifest if os.path.isabs(args.manifest) \
        else os.path.join(root, args.manifest)
    if not os.path.isfile(manifest_path):
        sys.stderr.write("FATAL: manifest not found: %s\n" % manifest_path)
        return 2
    with open(manifest_path, "r", encoding="utf-8") as fh:
        manifest = yaml.safe_load(fh)

    checker = Checker(manifest, root)

    # input hashes (targets + manifest)
    inputs = {}
    mrel = os.path.relpath(manifest_path, root).replace("\\", "/")
    inputs[mrel] = {
        "sha256": sha256_of(manifest_path),
        "exists": True,
        "role": "rule_manifest",
    }
    for name, d in checker.docs.items():
        inputs[d.relpath] = {
            "sha256": sha256_of(d.abspath) if d.exists else None,
            "exists": d.exists,
            "role": name,
            "lines": len(d.lines),
            "appendix_d_start_line": (d.appendix_d_start + 1) if d.appendix_d_start is not None else None,
            "appendix_a_start_line": (d.appendix_a_start + 1) if d.appendix_a_start is not None else None,
        }

    results = [checker.run_rule(r) for r in manifest.get("rules", [])]
    passed = [r["id"] for r in results if r["verdict"] == "PASS"]
    failed = [r["id"] for r in results if r["verdict"] != "PASS"]

    if not failed:
        overall = "DOCUMENT PACKAGE READY FOR EXTERNAL REVIEW"
    else:
        overall = "BLOCKED(%s)" % ",".join(failed)

    report = {
        "meta": {
            "tool": "scripts/checks/v42_conformance.py",
            "rules_version": manifest.get("rules_version"),
            "manifest": mrel,
            "root": root.replace("\\", "/"),
            "run_utc": datetime.datetime.now(datetime.timezone.utc)
                        .strftime("%Y-%m-%dT%H:%M:%SZ"),
            "self_scope": ("machine-assisted internal consistency check (second "
                           "pass); NOT independent oversight; NOT external peer "
                           "review; certifies package self-consistency only, not "
                           "scientific validity"),
            "inputs": inputs,
        },
        "rules": results,
        "summary": {
            "total": len(results),
            "passed": len(passed),
            "failed": len(failed),
            "passed_ids": passed,
            "failed_ids": failed,
            "overall_verdict": overall,
        },
    }

    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        outp = args.output if os.path.isabs(args.output) else os.path.join(root, args.output)
        with open(outp, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    sys.stdout.write(text + "\n")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
