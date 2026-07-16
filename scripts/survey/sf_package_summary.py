#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fail-closed machine package summary, v2 (correction #4B / P0-1).

The C4A summary was a real script whose oracle was weaker than its prose: it
checked uniqueness where the claim said canonical counts, trusted persisted
verdict fields a human could hand-write, upgraded "50 collector rows" into an
audit PASS, and let one historical marker exempt a whole line (doctoral
re-review #4A MAJOR-1 — all four holes reproduced by mutation). v2 closes them:

  1. EXACT canonical counts, prefix hashes, category sets and compiler-version
     tiers are enforced against ONE pinned canon file
     (wiki/survey/2026-07-17-sf-canon.json); any deviation = non-zero exit.
  2. Every deterministic producer is RE-RUN as a subprocess and its fresh
     output bytes must equal the persisted evidence bytes — a hand-edited or
     stale evidence file can no longer inherit a green light. On mismatch the
     persisted bytes are restored and the item FAILs.
  3. The route status-audit collector is reported as EVIDENCE_PRESENT only;
     adjudication is a separate deterministic validator
     (sf_t1_routes_adjudication_validate.py) with its own re-run + verdict.
  4. The active signature surface is machine-derived from the bundle-manifest
     #4B section (MACHINE_COUNT reconciliation kills the 31-vs-33 class of
     error); the stale-token scan exempts ONLY fenced historical blocks or
     〔HIST:...〕-wrapped occurrences — a marker on the same line no longer
     shields other tokens; a missing active file FAILs (never skipped).

Run from repo root:  python scripts/survey/sf_package_summary.py
Persists docs/checks/2026-07-16-sf-package-summary.json. Exit 0 iff all green.
Negative harness: scripts/survey/sf_package_summary_test.py (P0-1.5).
"""
import glob
import hashlib
import json
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CANON_PATH = os.path.join(REPO, "wiki", "survey", "2026-07-17-sf-canon.json")
OUT = os.path.join(REPO, "docs", "checks", "2026-07-16-sf-package-summary.json")
HIST_WRAP_RE = re.compile(r"〔HIST:[^〕]*〕")


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def read_bytes(path):
    with open(path, "rb") as f:
        return f.read()


def jsonl_rows(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if not os.path.exists(CANON_PATH):
        print("package summary: FAIL (canon file missing — nothing to enforce against)")
        return 1
    canon = json.loads(read_bytes(CANON_PATH).decode("utf-8"))
    checklist = []

    def item(name, evidence, status, detail):
        checklist.append({"item": name, "evidence": evidence,
                          "status": status, "detail": detail})

    # ---- 1. exact canonical counts (fail-closed, expected vs got) ----
    got = {}
    exp = {}
    try:
        seeds = jsonl_rows(os.path.join(REPO, canon["seeds"]["file"]))
        queries = jsonl_rows(os.path.join(REPO, canon["queries"]["file"]))
        routes = jsonl_rows(os.path.join(REPO, canon["routes"]["file"]))
        sentinels = json.loads(read_bytes(
            os.path.join(REPO, canon["sentinels"]["file"])).decode("utf-8"))["papers"]
        vc = {}
        for q in queries:
            vc[q["compiler_version"]] = vc.get(q["compiler_version"], 0) + 1
        got = {
            "seeds_rows": len(seeds), "seeds_unique": len({s["id"] for s in seeds}),
            "queries_rows": len(queries),
            "queries_unique": len({q["query_id"] for q in queries}),
            "categories_union": sorted({c for q in queries for c in q["categories"]}),
            "compiler_version_counts": dict(sorted(vc.items())),
            "routes_rows": len(routes),
            "routes_unique": len({r["route_id"] for r in routes}),
            "routes_status_outside_domain": sorted(
                {r["status"] for r in routes} - set(canon["routes"]["status_domain"])),
            "sentinel_papers": len(sentinels),
            "sentinel_held_out": sum(1 for m in sentinels.values() if m.get("held_out")),
        }
        exp = {
            "seeds_rows": canon["seeds"]["rows"], "seeds_unique": canon["seeds"]["rows"],
            "queries_rows": canon["queries"]["rows"],
            "queries_unique": canon["queries"]["rows"],
            "categories_union": canon["queries"]["categories_union"],
            "compiler_version_counts": canon["queries"]["compiler_version_counts"],
            "routes_rows": canon["routes"]["rows"],
            "routes_unique": canon["routes"]["rows"],
            "routes_status_outside_domain": [],
            "sentinel_papers": canon["sentinels"]["papers"],
            "sentinel_held_out": canon["sentinels"]["held_out"],
        }
        mismatches = {k: {"expected": exp[k], "got": got[k]}
                      for k in exp if exp[k] != got[k]}
        item("正典精确计数（canon 逐项相等,非唯一性）", canon["seeds"]["file"] + " 等四件+canon",
             "PASS" if not mismatches else "FAIL",
             "all counts == canon" if not mismatches
             else json.dumps(mismatches, ensure_ascii=False)[:400])
    except Exception as e:  # noqa: BLE001 — fail-closed on any load error
        item("正典精确计数（canon 逐项相等,非唯一性）", "canon inputs", "FAIL",
             f"input unreadable: {type(e).__name__}: {e}")
        seeds = queries = routes = []
        sentinels = {}

    # ---- 2. append-only prefix hashes ----
    def prefix_hash(path, n):
        lines = read_bytes(path).split(b"\n")
        return sha256_bytes(b"\n".join(lines[:n]) + b"\n")

    try:
        ph = {
            "seeds": (prefix_hash(os.path.join(REPO, canon["seeds"]["file"]),
                                  canon["seeds"]["prefix_rows"]),
                      canon["seeds"]["prefix_sha256"]),
            "queries": (prefix_hash(os.path.join(REPO, canon["queries"]["file"]),
                                    canon["queries"]["prefix_rows"]),
                        canon["queries"]["prefix_sha256"]),
        }
        bad = {k: v for k, v in ph.items() if v[0] != v[1]}
        item("append-only 前缀哈希（seeds prefix87 / queries prefix55 == canon）",
             "canon prefix pins", "PASS" if not bad else "FAIL",
             "prefixes byte-identical" if not bad else f"drift in {sorted(bad)}")
    except Exception as e:  # noqa: BLE001
        item("append-only 前缀哈希（seeds prefix87 / queries prefix55 == canon）",
             "canon prefix pins", "FAIL", f"{type(e).__name__}: {e}")

    # ---- 3. deterministic producers: re-run + byte-compare + criterion ----
    def criterion_check(name, rep):
        if name == "none":
            return True, "byte-stable rerun"
        if name == "verdict_pass":
            return rep.get("verdict") == "PASS", f"verdict={rep.get('verdict')}"
        if name == "dryrun":
            ok = (rep.get("verdict") == "PASS"
                  and rep.get("input", {}).get("n_rows_read") == canon["queries"]["rows"])
            return ok, (f"verdict={rep.get('verdict')}, "
                        f"n_rows_read={rep.get('input', {}).get('n_rows_read')} "
                        f"(expect {canon['queries']['rows']})")
        if name == "sentinel":
            ok = (rep.get("verdict") == "PASS"
                  and rep.get("outcome_counts", {}).get("UNRESOLVED_MISS") == 0
                  and len(rep.get("held_out_outcomes", {})) == canon["sentinels"]["held_out"])
            return ok, (f"verdict={rep.get('verdict')}, "
                        f"outcomes={rep.get('outcome_counts')}, "
                        f"held_out={sorted(rep.get('held_out_outcomes', {}))}")
        return False, f"unknown criterion {name!r}"

    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    for prod in canon["producers"]:
        script = prod["script"]
        label = f"producer 重跑一致（{os.path.basename(script)}）"
        if "evidence_glob" in prod:
            pat = os.path.join(REPO, prod["evidence_glob"]["pattern"])
            paths = sorted(glob.glob(pat))
            if len(paths) != prod["evidence_glob"]["expect_count"]:
                item(label, prod["evidence_glob"]["pattern"], "FAIL",
                     f"expected {prod['evidence_glob']['expect_count']} evidence files, "
                     f"found {len(paths)}")
                continue
        else:
            paths = [os.path.join(REPO, p) for p in prod["evidence"]]
        missing = [p for p in paths if not os.path.exists(p)]
        if missing:
            item(label, ", ".join(prod.get("evidence", [])[:2]), "EVIDENCE_MISSING",
                 f"missing: {[os.path.relpath(m, REPO) for m in missing]}")
            continue
        snapshots = {p: read_bytes(p) for p in paths}
        r = subprocess.run([sys.executable, os.path.join(REPO, script)],
                           capture_output=True, cwd=REPO, env=env)
        if r.returncode != 0:
            for p, b in snapshots.items():
                with open(p, "wb") as f:
                    f.write(b)
            item(label, script, "FAIL",
                 f"producer exit {r.returncode}: "
                 f"{r.stdout.decode('utf-8', errors='replace')[-200:]}")
            continue
        if "evidence_glob" in prod:
            paths_after = sorted(glob.glob(pat))
            if paths_after != paths:
                item(label, prod["evidence_glob"]["pattern"], "FAIL",
                     "producer changed the evidence file set")
                continue
        changed = [p for p in paths if read_bytes(p) != snapshots[p]]
        if changed:
            for p in changed:
                with open(p, "wb") as f:
                    f.write(snapshots[p])
            item(label, script, "FAIL",
                 f"persisted evidence != fresh rerun bytes (stale or hand-edited): "
                 f"{[os.path.relpath(c, REPO) for c in changed]}")
            continue
        ok, detail = True, "byte-stable rerun"
        if prod["criterion"] != "none":
            rep = json.loads(read_bytes(paths[0]).decode("utf-8"))
            ok, detail = criterion_check(prod["criterion"], rep)
        item(label, prod.get("evidence", [prod.get("evidence_glob", {}).get("pattern")])[0],
             "PASS" if ok else "FAIL", detail)

    # ---- 4. route collector evidence: EVIDENCE_PRESENT only, never an audit PASS ----
    try:
        rc = canon["route_collector_evidence"]
        audit = json.loads(read_bytes(os.path.join(REPO, rc["file"])).decode("utf-8"))
        arows = audit.get("rows") or []
        route_ids = {r["route_id"] for r in routes} if routes else set()
        aids = {r.get("route_id") for r in arows}
        ok = (len(arows) == rc["rows"] and aids == route_ids
              and all(isinstance(r.get("evidence"), dict) and r["evidence"] for r in arows))
        item("routes 外部状态审计证据件（collector,只报在场性——裁定见 adjudication validator）",
             rc["file"], "EVIDENCE_PRESENT" if ok else "FAIL",
             f"{len(arows)} rows, ids_match={aids == route_ids}, "
             f"non_empty_evidence={all(bool(r.get('evidence')) for r in arows)}")
    except Exception as e:  # noqa: BLE001
        item("routes 外部状态审计证据件（collector,只报在场性——裁定见 adjudication validator）",
             canon.get("route_collector_evidence", {}).get("file", "?"), "FAIL",
             f"{type(e).__name__}: {e}")

    # ---- 5. bundle manifest reconciliation + machine-derived active surface ----
    active_files = list(canon["must_include_active"])
    try:
        bm = canon["bundle_manifest"]
        mtext = read_bytes(os.path.join(REPO, bm["file"])).decode("utf-8")
        marker = bm["section_marker"]
        idx = mtext.rfind(marker)
        if idx < 0:
            item("bundle manifest 对账（MACHINE_COUNT == 表内枚举 == 磁盘在场）",
                 bm["file"], "FAIL", f"section {marker!r} not found")
        else:
            rest = mtext[idx:]
            nxt = re.search(r"\n## ", rest[len(marker):])
            section = rest if not nxt else rest[:len(marker) + nxt.start() + 1]
            mc = re.search(re.escape(bm["machine_count_line"])
                           + r"\s*files=(\d+)\s+fixtures=(\d+)", section)
            paths = []
            for m in re.finditer(r"`([^`\n]+)`", section):
                p = m.group(1).strip()
                if re.match(r"^(wiki|scripts|docs)/", p) and re.search(
                        r"\.(md|py|jsonl|json|sh)$", p) and "fixtures-c4b/" not in p:
                    paths.append(p)
            distinct = sorted(set(paths))
            n_fix = len(glob.glob(os.path.join(REPO, "wiki", "survey",
                                               "fixtures-c4b", "*.json")))
            missing = [p for p in distinct if not os.path.exists(os.path.join(REPO, p))]
            if not mc:
                item("bundle manifest 对账（MACHINE_COUNT == 表内枚举 == 磁盘在场）",
                     bm["file"], "FAIL", "MACHINE_COUNT line missing in #4B section")
            elif int(mc.group(1)) != len(distinct) or int(mc.group(2)) != n_fix or missing:
                item("bundle manifest 对账（MACHINE_COUNT == 表内枚举 == 磁盘在场）",
                     bm["file"], "FAIL",
                     f"declared files={mc.group(1)} vs enumerated={len(distinct)}; "
                     f"declared fixtures={mc.group(2)} vs on-disk={n_fix}; "
                     f"missing={missing[:4]}")
            else:
                item("bundle manifest 对账（MACHINE_COUNT == 表内枚举 == 磁盘在场）",
                     bm["file"], "PASS",
                     f"files={len(distinct)}, fixtures={n_fix}, all enumerated paths exist")
            # dated correction contracts / review artifacts / append-only audit
            # layer are historical by construction — live canon numbers must be
            # carried by the protocol body + hot layer, which stay in scope
            hist_pat = re.compile(r"(amendment|review|response|application|decision-log)", re.I)
            for p in distinct:
                if re.search(r"\.(md|py)$", p) and not hist_pat.search(os.path.basename(p)):
                    if p not in active_files:
                        active_files.append(p)
    except Exception as e:  # noqa: BLE001
        item("bundle manifest 对账（MACHINE_COUNT == 表内枚举 == 磁盘在场）",
             canon.get("bundle_manifest", {}).get("file", "?"), "FAIL",
             f"{type(e).__name__}: {e}")

    # ---- 6. stale-token scan: occurrence/block-level exemption, missing file = FAIL ----
    stale_hits = []
    scan_errors = []
    for rel in active_files:
        path = os.path.join(REPO, rel)
        if not os.path.exists(path):
            scan_errors.append(f"active file missing: {rel}")
            continue
        in_block = False
        try:
            for i, line in enumerate(read_bytes(path).decode("utf-8").splitlines(), 1):
                if canon["historical_exemption"]["block_begin"] in line:
                    in_block = True
                    continue
                if canon["historical_exemption"]["block_end"] in line:
                    in_block = False
                    continue
                if in_block:
                    continue
                scannable = HIST_WRAP_RE.sub("", line)
                for tok in canon["forbidden_tokens"]:
                    if tok in scannable:
                        stale_hits.append({"file": rel, "line": i, "token": tok})
        except UnicodeDecodeError:
            scan_errors.append(f"active file not valid UTF-8: {rel}")
    item("陈旧口径扫描（活跃面机器派生;occurrence 级豁免;缺文件=FAIL）",
         "canon.forbidden_tokens × derived active surface",
         "PASS" if not stale_hits and not scan_errors else "FAIL",
         f"hits={len(stale_hits)}, errors={scan_errors}" if (stale_hits or scan_errors)
         else f"0 hits over {len(active_files)} active files")

    all_green = all(c["status"] in ("PASS", "EVIDENCE_PRESENT") for c in checklist)
    report = {
        "artifact_id": "SF-PACKAGE-SUMMARY-2026-07-16-02",
        "generator": "scripts/survey/sf_package_summary.py (v2-c4b)",
        "canon": {"file": os.path.relpath(CANON_PATH, REPO).replace("\\", "/"),
                  "sha256": sha256_bytes(read_bytes(CANON_PATH))},
        "discipline": "fail-closed:正典精确计数/前缀哈希/producer 重跑字节一致/manifest 机器对账/"
                      "occurrence 级历史豁免;人不能手写绿灯——verdict 一律取自隔离重跑的新鲜输出",
        "counts": {"expected": exp, "got": got},
        "active_surface": active_files,
        "stale_token_scan": {"forbidden_tokens": canon["forbidden_tokens"],
                             "hits": stale_hits, "errors": scan_errors},
        "signature_checklist": checklist,
        "verdict": "PASS" if all_green else "FAIL",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write((json.dumps(report, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    print(f"package summary: {report['verdict']}")
    for c in checklist:
        print(f"  [{c['status']:16s}] {c['item']}")
        if c["status"] not in ("PASS", "EVIDENCE_PRESENT"):
            print(f"      -> {c['detail'][:220]}")
    return 0 if all_green else 1


if __name__ == "__main__":
    sys.exit(main())
