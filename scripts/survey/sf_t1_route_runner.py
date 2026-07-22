#!/usr/bin/env python3
"""Collect bounded REC-7 dispositions for the 50 registered T1 proceedings routes.

The collector reads only the frozen route manifest and wordlist.  It stores raw official TOC bytes
outside Git, records hashes and matched titles, and treats inaccessible or unparsable routes as
``WAIVED_UNAVAILABLE`` rather than as zero-hit executions.  It does not resolve paper claims, fetch
full text, call a research model, or expand the registered venue/year grid.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import time
import unicodedata
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urljoin


USER_AGENT = "exploring-l4-intelligence Stage-1B bounded T1 REC-7 collector"
MAX_ATTEMPTS = 2
SPACING_SECONDS = 3.0
READ_CAP = 8_000_000
HUBS = {
    "ICML": "https://proceedings.mlr.press/",
    "MM": "https://dl.acm.org/conference/mm",
    "ICASSP": "https://ieeexplore.ieee.org/xpl/conhome/1000002/all-proceedings",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKC", value.lower())
    value = re.sub(r"[-_/]", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def compile_wordlist(document: dict[str, Any]) -> dict[str, tuple[str, ...]]:
    return {
        name: tuple(sorted({normalize(item) for item in document["groups"][name]}))
        for name in ("A", "B", "C")
    }


def _contains(normalized_title: str, term: str) -> bool:
    return re.search(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])", normalized_title) is not None


def match_title(title: str, words: dict[str, tuple[str, ...]]) -> dict[str, Any]:
    normalized = normalize(title)
    hits = {name: [term for term in terms if _contains(normalized, term)] for name, terms in words.items()}
    return {
        "matched": bool(hits["A"] or (hits["B"] and hits["C"])),
        "normalized_title": normalized,
        "wordlist_hits": hits,
    }


class _AnchorParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._href: str | None = None
        self._parts: list[str] = []
        self.anchors: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "a" and self._href is None:
            self._href = dict(attrs).get("href") or ""
            self._parts = []

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._href is not None:
            text = re.sub(r"\s+", " ", html.unescape(" ".join(self._parts))).strip()
            self.anchors.append((self._href, text))
            self._href = None
            self._parts = []


def _anchors(body: bytes) -> list[tuple[str, str]]:
    parser = _AnchorParser()
    parser.feed(body.decode("utf-8", "replace"))
    return parser.anchors


def _is_paper_link(href: str, venue: str, year: int) -> bool:
    clean = href.split("?", 1)[0].split("#", 1)[0]
    lower = clean.lower().rstrip("/")
    if venue in {"ACL", "EMNLP"}:
        return bool(re.search(rf"/(?:{year}\.)[^/]+$", lower))
    if venue == "NEURIPS":
        return "/hash/" in lower and lower.endswith(".html")
    if venue == "ICML":
        return lower.endswith(".html") and not lower.endswith("index.html")
    if venue in {"CVPR", "ICCV"}:
        return lower.endswith("_paper.html")
    if venue == "IS":
        return lower.endswith("_interspeech.html")
    return False


def extract_titles(body: bytes, venue: str, year: int) -> list[str]:
    source = body.decode("utf-8", "replace")
    if venue == "ICML":
        titles = {
            re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", match))).strip()
            for match in re.findall(
                r"<p\b[^>]*class=[\"'][^\"']*\btitle\b[^\"']*[\"'][^>]*>(.*?)</p>",
                source,
                flags=re.IGNORECASE | re.DOTALL,
            )
        }
        return sorted({title for title in titles if title}, key=lambda value: (normalize(value), value))
    if venue == "IS":
        titles = {
            re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", match))).strip()
            for match in re.findall(
                r"<a\b[^>]*href=[\"'][^\"']+_interspeech\.html[\"'][^>]*>.*?"
                r"<p\b[^>]*>\s*(.*?)<br\b",
                source,
                flags=re.IGNORECASE | re.DOTALL,
            )
        }
        return sorted({title for title in titles if title}, key=lambda value: (normalize(value), value))
    titles = {
        text
        for href, text in _anchors(body)
        if text and _is_paper_link(href, venue, year)
    }
    return sorted(titles, key=lambda value: (normalize(value), value))


def effective_entry_url(url: str, venue: str) -> str:
    if venue in {"CVPR", "ICCV"} and "?" not in url:
        return url.rstrip("/") + "?day=all"
    return url


def network_transport(url: str) -> tuple[int | None, bytes, int, str | None]:
    last_error: str | None = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.status, response.read(READ_CAP), attempt, None
        except urllib.error.HTTPError as error:
            last_error = f"HTTP_{error.code}"
            if error.code not in {429, 500, 502, 503, 504}:
                return error.code, b"", attempt, last_error
        except Exception as error:  # noqa: BLE001 - bounded network failure becomes evidence.
            last_error = f"{type(error).__name__}: {str(error)[:200]}"
        if attempt < MAX_ATTEMPTS:
            time.sleep(SPACING_SECONDS)
    return None, b"", MAX_ATTEMPTS, last_error


def _resolve_entry(
    route: dict[str, Any],
    transport: Callable[[str], tuple[int | None, bytes, int, str | None]],
) -> tuple[str | None, dict[str, Any]]:
    venue = route["venue_code"]
    hub = HUBS.get(venue)
    if not hub:
        return None, {"failure_code": "NO_REGISTERED_OFFICIAL_HUB"}
    status, body, attempts, error = transport(hub)
    receipt = {
        "hub_url": hub,
        "http_status": status,
        "attempts": attempts,
        "body_sha256": hashlib.sha256(body).hexdigest() if body else None,
        "body_bytes": len(body),
        "failure_code": error,
    }
    if status != 200 or not body:
        return None, receipt

    year_text = str(route["year"])
    candidates: list[str] = []
    for href, text in _anchors(body):
        joined = urljoin(hub, href)
        combined = f"{text} {joined}"
        if year_text not in combined:
            continue
        if venue == "ICML" and re.search(r"proceedings\.mlr\.press/v\d+/?$", joined):
            candidates.append(joined.rstrip("/") + "/")
        elif venue == "MM" and "/doi/proceedings/" in joined:
            candidates.append(joined)
        elif venue == "ICASSP" and re.search(r"/xpl/conhome/\d+/(?:proceeding|all-proceedings)", joined):
            candidates.append(joined)
    unique = sorted(set(candidates))
    receipt["candidate_urls"] = unique
    if len(unique) != 1:
        receipt["failure_code"] = "ENTRY_RESOLUTION_FAILED"
        return None, receipt
    return unique[0], receipt


def collect_route(
    route: dict[str, Any],
    words: dict[str, tuple[str, ...]],
    raw_dir: Path,
    *,
    transport: Callable[[str], tuple[int | None, bytes, int, str | None]] = network_transport,
    reuse_raw: bool = False,
) -> dict[str, Any]:
    base: dict[str, Any] = {
        "schema": "sf-rec7-t1-route-disposition-v1",
        "route_id": route["route_id"],
        "venue_code": route["venue_code"],
        "year": route["year"],
        "registered_status": route["status"],
        "registered_entry_status": route["entry_status"],
        "collected_at_utc": utc_now(),
    }
    if route["entry_status"] == "NOT_APPLICABLE" or route["status"] == "NOT_HELD":
        return {
            **base,
            "disposition": "NOT_HELD",
            "resolved_entry_url": None,
            "n_titles_total": 0,
            "n_matched": 0,
            "matched_titles": [],
            "impact": "No proceedings existed for this registered venue-year route.",
        }

    resolution_receipt = None
    url = route.get("entry_url")
    if route["entry_status"] == "ENTRY_TO_RESOLVE":
        url, resolution_receipt = _resolve_entry(route, transport)
        if not url:
            return {
                **base,
                "disposition": "WAIVED_UNAVAILABLE",
                "resolved_entry_url": None,
                "resolution_receipt": resolution_receipt,
                "failure_code": (resolution_receipt or {}).get("failure_code") or "ENTRY_RESOLUTION_FAILED",
                "n_titles_total": None,
                "n_matched": None,
                "matched_titles": [],
                "impact": "Venue-route omission risk remains; no zero-hit claim is made.",
            }

    url = effective_entry_url(str(url), route["venue_code"])
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_path = raw_dir / f"{route['route_id']}.html"
    raw_reused = bool(reuse_raw and raw_path.is_file())
    if raw_reused:
        status, body, attempts, error = 200, raw_path.read_bytes(), 0, None
    else:
        status, body, attempts, error = transport(url)
    if status != 200 or not body:
        return {
            **base,
            "disposition": "WAIVED_UNAVAILABLE",
            "resolved_entry_url": url,
            "resolution_receipt": resolution_receipt,
            "http_status": status,
            "attempts": attempts,
            "failure_code": error or f"HTTP_{status}",
            "n_titles_total": None,
            "n_matched": None,
            "matched_titles": [],
            "impact": "Venue-route omission risk remains; no zero-hit claim is made.",
        }

    if not raw_reused:
        raw_path.write_bytes(body)
    titles = extract_titles(body, route["venue_code"], int(route["year"]))
    if not titles:
        return {
            **base,
            "disposition": "WAIVED_UNAVAILABLE",
            "resolved_entry_url": url,
            "resolution_receipt": resolution_receipt,
            "http_status": status,
            "attempts": attempts,
            "raw_reused": raw_reused,
            "failure_code": "NO_PARSEABLE_TITLES",
            "raw_toc_ref": raw_path.as_posix(),
            "raw_toc_sha256": hashlib.sha256(body).hexdigest(),
            "raw_toc_bytes": len(body),
            "n_titles_total": None,
            "n_matched": None,
            "matched_titles": [],
            "impact": "Official page was reachable but title extraction was unsupported; no zero-hit claim is made.",
        }

    matches = []
    for title in titles:
        decision = match_title(title, words)
        if decision["matched"]:
            matches.append({"title": title, **decision})
    return {
        **base,
        "disposition": "EXECUTED",
        "resolved_entry_url": url,
        "resolution_receipt": resolution_receipt,
        "http_status": status,
        "attempts": attempts,
        "raw_reused": raw_reused,
        "raw_toc_ref": raw_path.as_posix(),
        "raw_toc_sha256": hashlib.sha256(body).hexdigest(),
        "raw_toc_bytes": len(body),
        "n_titles_total": len(titles),
        "n_matched": len(matches),
        "matched_titles": matches,
        "impact": "Registered title route executed with the frozen wordlist.",
    }


def write_report(
    path: Path,
    rows: list[dict[str, Any]],
    routes_sha256: str,
    wordlist_sha256: str,
) -> dict[str, Any]:
    counts = Counter(row["disposition"] for row in rows)
    report = {
        "schema": "sf-stage1b-t1-rec7-closeout-v1",
        "routes_sha256": routes_sha256,
        "wordlist_sha256": wordlist_sha256,
        "summary": {
            "routes_dispositioned": len(rows),
            "executed": counts["EXECUTED"],
            "not_held": counts["NOT_HELD"],
            "waived_unavailable": counts["WAIVED_UNAVAILABLE"],
            "titles_total_on_executed_routes": sum(row.get("n_titles_total") or 0 for row in rows if row["disposition"] == "EXECUTED"),
            "matched_titles": sum(row.get("n_matched") or 0 for row in rows if row["disposition"] == "EXECUTED"),
            "zero_hit_claim_for_waived_routes": False,
        },
        "rows": rows,
    }
    payload = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload, encoding="utf-8", newline="\n")
    return report


def merge_rows(base: list[dict[str, Any]], replacements: list[dict[str, Any]]) -> list[dict[str, Any]]:
    base_ids = [row["route_id"] for row in base]
    if len(base_ids) != len(set(base_ids)):
        raise ValueError("duplicate route_id in base report")
    replacement_by_id = {row["route_id"]: row for row in replacements}
    if len(replacement_by_id) != len(replacements):
        raise ValueError("duplicate route_id in replacement rows")
    missing = sorted(set(replacement_by_id) - set(base_ids))
    if missing:
        raise ValueError(f"replacement route_id not present in base report: {missing}")
    return [replacement_by_id.get(route_id, row) for route_id, row in zip(base_ids, base)]


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--routes", type=Path, required=True)
    parser.add_argument("--wordlist", type=Path, required=True)
    parser.add_argument("--raw-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--route-id", action="append", default=[])
    parser.add_argument("--merge-from", type=Path)
    parser.add_argument("--reuse-raw", action="store_true")
    args = parser.parse_args()

    routes_raw = args.routes.read_bytes()
    words_raw = args.wordlist.read_bytes()
    routes = _load_jsonl(args.routes)
    if args.route_id:
        selected = set(args.route_id)
        routes = [row for row in routes if row["route_id"] in selected]
        missing = selected - {row["route_id"] for row in routes}
        if missing:
            raise SystemExit(f"unknown route IDs: {sorted(missing)}")
    words = compile_wordlist(json.loads(words_raw))
    results = []
    for index, row in enumerate(routes):
        if index:
            time.sleep(SPACING_SECONDS)
        result = collect_route(row, words, args.raw_dir, reuse_raw=args.reuse_raw)
        results.append(result)
        print(
            f"{row['route_id']:22s} {result['disposition']:20s} "
            f"titles={result.get('n_titles_total')} matched={result.get('n_matched')} "
            f"failure={result.get('failure_code', '')}",
            flush=True,
        )
    final_results = results
    if args.merge_from:
        prior = json.loads(args.merge_from.read_text("utf-8"))
        final_results = merge_rows(prior["rows"], results)
    report = write_report(
        args.output,
        final_results,
        hashlib.sha256(routes_raw).hexdigest(),
        hashlib.sha256(words_raw).hexdigest(),
    )
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    return 0 if len(final_results) == 50 else 1


if __name__ == "__main__":
    raise SystemExit(main())
