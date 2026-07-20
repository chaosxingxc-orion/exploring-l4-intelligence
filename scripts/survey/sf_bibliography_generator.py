#!/usr/bin/env python3
"""Generate the reviewer bibliography exclusively from frozen official receipts."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
LEGACY_BIBLIOGRAPHY_PATH = ROOT / "wiki/survey/2026-07-19-sf-bibliography-v1.md"
RECEIPTS_PATH = ROOT / "wiki/survey/current/data/official-metadata-receipts-v1.jsonl"
RAW_DIR = ROOT / "wiki/survey/current/data/official-metadata"
OUTPUT_PATH = ROOT / "wiki/survey/current/bibliography.md"

CANONICAL_ROLES = {
    "DEEPLY_READ",
    "KNOWN_QUEUE",
    "MEASUREMENT_INSTRUMENT",
    "BOUNDARY_COMPARATOR",
}
CHAINS = {
    "SYSTEM_FIRST_DIRECT_NEIGHBORS",
    "REWARD_AND_VERIFICATION_MECHANISMS",
    "TRAINING_FREE_AND_TRAINED_BOUNDARIES",
}
CHAIN_TITLES = {
    "SYSTEM_FIRST_DIRECT_NEIGHBORS": "System-first speech/omni agent neighbors",
    "REWARD_AND_VERIFICATION_MECHANISMS": "Reward and verification mechanisms",
    "TRAINING_FREE_AND_TRAINED_BOUNDARIES": "Training-free and trained boundary comparators",
}
SECTION_ROLE = {
    "DEEPLY_READ": "DEEPLY_READ",
    "CALIBRATION": "BOUNDARY_COMPARATOR",
    "KNOWN_QUEUE": "KNOWN_QUEUE",
    "MEASUREMENT_INSTRUMENT": "MEASUREMENT_INSTRUMENT",
    "MEASUREMENT_INSTRUMENT(trained-RM)": "MEASUREMENT_INSTRUMENT",
    "BOUNDARY/NEGATIVE_PRIOR": "BOUNDARY_COMPARATOR",
    "STAGE1B_FIRST_BATCH(P2)": "KNOWN_QUEUE",
}
ARXIV_RE = re.compile(r"(?<!\d)(\d{4}\.\d{4,5})(?:v\d+)?(?!\d)", re.I)
ACL_RE = re.compile(r"aclanthology\.org/([^/\s]+)", re.I)
GITHUB_RE = re.compile(r"github\.com/([^/\s]+/[^/\s]+)", re.I)
URL_RE = re.compile(r"https?://[^\s|·]+")
ATOM_NS = "{http://www.w3.org/2005/Atom}"
OAI_NS = "{http://www.openarchives.org/OAI/2.0/}"
ARXIV_OAI_NS = "{http://arxiv.org/OAI/arXiv/}"

DIRECT_NEIGHBOR_POLICIES = {
    "2510.02995": ("KNOWN_QUEUE", "SYSTEM_FIRST_DIRECT_NEIGHBORS", 272),
    "2605.28480": ("KNOWN_QUEUE", "SYSTEM_FIRST_DIRECT_NEIGHBORS", 273),
    "2511.02834": ("BOUNDARY_COMPARATOR", "SYSTEM_FIRST_DIRECT_NEIGHBORS", 274),
    "2606.15141": ("BOUNDARY_COMPARATOR", "SYSTEM_FIRST_DIRECT_NEIGHBORS", 275),
    "2602.13685": ("BOUNDARY_COMPARATOR", "SYSTEM_FIRST_DIRECT_NEIGHBORS", 276),
    "2407.09886": ("KNOWN_QUEUE", "SYSTEM_FIRST_DIRECT_NEIGHBORS", 277),
    "2604.15710": ("BOUNDARY_COMPARATOR", "SYSTEM_FIRST_DIRECT_NEIGHBORS", 278),
    "2505.09558": ("MEASUREMENT_INSTRUMENT", "TRAINING_FREE_AND_TRAINED_BOUNDARIES", 279),
    "2602.13891": ("MEASUREMENT_INSTRUMENT", "TRAINING_FREE_AND_TRAINED_BOUNDARIES", 280),
}
REVIEWER_P2_POLICIES = {
    "2508.16665": ("KNOWN_QUEUE", "REWARD_AND_VERIFICATION_MECHANISMS", 290),
    "2510.18982": ("KNOWN_QUEUE", "REWARD_AND_VERIFICATION_MECHANISMS", 291),
    "2509.25845": ("BOUNDARY_COMPARATOR", "TRAINING_FREE_AND_TRAINED_BOUNDARIES", 294),
}
REVIEW_PATH = "wiki/audit/system-first-stage1a/round-14/stage1a-final-gates-plan-doctoral-adversarial-review.md"


def normalize_heading(line: str) -> str | None:
    if not line.startswith("## "):
        return None
    value = line[3:].strip()
    return value.split("（", 1)[0].strip()


def identity_from_urls(urls: list[str]) -> dict[str, str]:
    joined = " ".join(urls)
    arxiv = ARXIV_RE.search(joined)
    if arxiv:
        return {"kind": "arxiv", "id": arxiv.group(1)}
    acl = ACL_RE.search(joined)
    if acl:
        return {"kind": "acl", "id": acl.group(1).rstrip("/")}
    github = GITHUB_RE.search(joined)
    if github:
        return {"kind": "github", "id": github.group(1).rstrip("/")}
    raise ValueError(f"bibliography row has no supported official identity: {urls}")


def legacy_chain(section: str) -> str:
    if section == "MEASUREMENT_INSTRUMENT":
        return "SYSTEM_FIRST_DIRECT_NEIGHBORS"
    if section in {"MEASUREMENT_INSTRUMENT(trained-RM)", "BOUNDARY/NEGATIVE_PRIOR"}:
        return "TRAINING_FREE_AND_TRAINED_BOUNDARIES"
    return "REWARD_AND_VERIFICATION_MECHANISMS"


def legacy_bibliography_policies() -> dict[str, dict[str, Any]]:
    policies: dict[str, dict[str, Any]] = {}
    section = None
    for line_number, line in enumerate(
        LEGACY_BIBLIOGRAPHY_PATH.read_text(encoding="utf-8").splitlines(), 1
    ):
        heading = normalize_heading(line)
        if heading is not None:
            section = heading
            continue
        if not line.startswith("|") or "http" not in line:
            continue
        if section not in SECTION_ROLE:
            raise ValueError(f"unsupported legacy bibliography section at line {line_number}")
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        identity = identity_from_urls(URL_RE.findall(cells[-1]))
        identity_id = identity["id"]
        if identity_id in policies:
            raise ValueError(f"duplicate legacy bibliography identity {identity_id}")
        role = SECTION_ROLE[section]
        policies[identity_id] = {
            "identity": identity,
            "reference_role": role,
            "chain": legacy_chain(section),
            "direct_neighbor": False,
            "source_locator": f"{LEGACY_BIBLIOGRAPHY_PATH.relative_to(ROOT).as_posix()}:{line_number}",
            "next_action": (
                "Maintain the frozen D2 evidence binding."
                if role == "DEEPLY_READ"
                else "Retain this role; fetch/code under the frozen protocol when prioritized."
            ),
            "load_bearing": role == "DEEPLY_READ",
            "access_class": "PROVENANCE_FETCH",
        }
    return policies


def additional_policies() -> dict[str, dict[str, Any]]:
    policies = {}
    for identity_id, (role, chain, line_number) in {
        **DIRECT_NEIGHBOR_POLICIES,
        **REVIEWER_P2_POLICIES,
    }.items():
        policies[identity_id] = {
            "identity": {"kind": "arxiv", "id": identity_id},
            "reference_role": role,
            "chain": chain,
            "direct_neighbor": identity_id in DIRECT_NEIGHBOR_POLICIES,
            "source_locator": f"{REVIEW_PATH}:{line_number}",
            "next_action": (
                "Keep as a nonblocking P2 comparator; fetch/code in Stage-1B if prioritized."
                if identity_id in REVIEWER_P2_POLICIES
                else "Route as an existing direct neighbor; reach D2 only before supporting a load-bearing claim."
            ),
            "load_bearing": False,
            "access_class": "REVIEW_CLAIM_VERIFICATION",
        }
    return policies


def all_policies() -> dict[str, dict[str, Any]]:
    policies = legacy_bibliography_policies()
    additions = additional_policies()
    overlap = set(policies) & set(additions)
    if overlap:
        raise ValueError(f"additions duplicate retained bibliography identities: {sorted(overlap)}")
    policies.update(additions)
    if len(policies) != 77:
        raise ValueError(f"expected 77 bibliography policies, got {len(policies)}")
    return policies


def collapse_space(value: str) -> str:
    return " ".join(value.split())


def parse_arxiv(identity: dict[str, str], raw: bytes) -> dict[str, Any]:
    root = ET.fromstring(raw)
    matches = []
    for entry in root.findall(f"{ATOM_NS}entry"):
        entry_id = collapse_space(entry.findtext(f"{ATOM_NS}id", default=""))
        match = ARXIV_RE.search(entry_id)
        if match and match.group(1) == identity["id"]:
            matches.append(entry)
    if len(matches) != 1:
        raise ValueError(f"official Atom payload has {len(matches)} entries for {identity['id']}")
    entry = matches[0]
    entry_id = collapse_space(entry.findtext(f"{ATOM_NS}id", default=""))
    version = re.search(rf"{re.escape(identity['id'])}(v\d+)?$", entry_id)
    authors = [
        collapse_space(author.findtext(f"{ATOM_NS}name", default=""))
        for author in entry.findall(f"{ATOM_NS}author")
    ]
    published = collapse_space(entry.findtext(f"{ATOM_NS}published", default=""))
    return {
        "identity": identity,
        "title": collapse_space(entry.findtext(f"{ATOM_NS}title", default="")),
        "authors": authors,
        "year": int(published[:4]),
        "stable_url": f"https://arxiv.org/abs/{identity['id']}",
        "source_version": version.group(1) if version and version.group(1) else "unversioned-entry-id",
    }


def parse_arxiv_oai(identity: dict[str, str], raw: bytes) -> dict[str, Any]:
    root = ET.fromstring(raw)
    record = root.find(f".//{OAI_NS}record")
    if record is None:
        error = root.find(f".//{OAI_NS}error")
        raise ValueError(
            f"official arXiv OAI payload has no record for {identity['id']}: "
            f"{collapse_space(error.text or '') if error is not None else 'unknown error'}"
        )
    header_id = collapse_space(record.findtext(f"{OAI_NS}header/{OAI_NS}identifier", default=""))
    if header_id != f"oai:arXiv.org:{identity['id']}":
        raise ValueError(f"arXiv OAI identity {header_id!r} does not match {identity['id']!r}")
    metadata = record.find(f"{OAI_NS}metadata/{ARXIV_OAI_NS}arXiv")
    if metadata is None or collapse_space(metadata.findtext(f"{ARXIV_OAI_NS}id", default="")) != identity["id"]:
        raise ValueError("arXiv OAI metadata identity mismatch")
    authors = []
    for author in metadata.findall(f"{ARXIV_OAI_NS}authors/{ARXIV_OAI_NS}author"):
        parts = [
            collapse_space(author.findtext(f"{ARXIV_OAI_NS}forenames", default="")),
            collapse_space(author.findtext(f"{ARXIV_OAI_NS}keyname", default="")),
            collapse_space(author.findtext(f"{ARXIV_OAI_NS}suffix", default="")),
        ]
        authors.append(" ".join(part for part in parts if part))
    created = collapse_space(metadata.findtext(f"{ARXIV_OAI_NS}created", default=""))
    datestamp = collapse_space(
        record.findtext(f"{OAI_NS}header/{OAI_NS}datestamp", default="")
    )
    return {
        "identity": identity,
        "title": collapse_space(metadata.findtext(f"{ARXIV_OAI_NS}title", default="")),
        "authors": authors,
        "year": int(created[:4]),
        "stable_url": f"https://arxiv.org/abs/{identity['id']}",
        "source_version": f"oai-datestamp:{datestamp}",
    }


def bibtex_fields(raw: bytes) -> tuple[str, dict[str, str]]:
    text = raw.decode("utf-8")
    header = re.search(r"@\w+\s*\{\s*([^,]+),", text)
    if not header:
        raise ValueError("official BibTeX payload lacks a citation key")
    fields: dict[str, str] = {}
    position = header.end()
    while position < len(text):
        match = re.search(r"([A-Za-z_]+)\s*=\s*", text[position:])
        if not match:
            break
        name = match.group(1).lower()
        cursor = position + match.end()
        if cursor >= len(text):
            break
        opener = text[cursor]
        if opener == "{":
            depth = 1
            end = cursor + 1
            while end < len(text) and depth:
                depth += (text[end] == "{") - (text[end] == "}")
                end += 1
            value = text[cursor + 1:end - 1]
        elif opener == '"':
            end = cursor + 1
            while end < len(text) and text[end] != '"':
                end += 2 if text[end] == "\\" else 1
            value = text[cursor + 1:end]
            end += 1
        else:
            end = text.find(",", cursor)
            value = text[cursor:end if end >= 0 else len(text)]
        fields[name] = collapse_space(value)
        position = end
    return header.group(1).strip(), fields


def clean_bibtex_text(value: str) -> str:
    accents = {
        "`": "\u0300",
        "'": "\u0301",
        "^": "\u0302",
        '"': "\u0308",
        "~": "\u0303",
        "v": "\u030c",
        "c": "\u0327",
    }

    def replace_accent(match: re.Match[str]) -> str:
        return unicodedata.normalize("NFC", match.group(2) + accents[match.group(1)])

    value = re.sub(r"\\([`'\^\"~vc])\{?([A-Za-z])\}?", replace_accent, value)
    value = value.replace("{", "").replace("}", "")
    value = value.replace("\\&", "&").replace("\\_", "_")
    return collapse_space(value)


def parse_acl(identity: dict[str, str], raw: bytes) -> dict[str, Any]:
    citation_key, fields = bibtex_fields(raw)
    official_url = fields.get("url", "").rstrip("/")
    official_doi = fields.get("doi", "")
    if not (
        official_url.casefold().endswith("/" + identity["id"].casefold())
        or official_doi.casefold().endswith("/" + identity["id"].casefold())
    ):
        raise ValueError(
            f"ACL BibTeX URL/DOI does not bind {identity['id']!r}; "
            f"citation_key={citation_key!r}"
        )
    authors = [
        clean_bibtex_text(author)
        for author in re.split(r"\s+and\s+", fields.get("author", ""))
        if author.strip()
    ]
    return {
        "identity": identity,
        "title": clean_bibtex_text(fields.get("title", "")),
        "authors": authors,
        "year": int(fields.get("year", "0")),
        "stable_url": fields.get("url", f"https://aclanthology.org/{identity['id']}/"),
        "source_version": citation_key,
    }


def parse_github(identity: dict[str, str], raw: bytes) -> dict[str, Any]:
    payload = json.loads(raw)
    if payload.get("full_name", "").casefold() != identity["id"].casefold():
        raise ValueError("GitHub repository identity mismatch")
    created = payload.get("created_at", "")
    return {
        "identity": identity,
        "title": payload.get("name") or payload["full_name"],
        "authors": [payload.get("owner", {}).get("login") or identity["id"].split("/", 1)[0]],
        "year": int(created[:4]),
        "stable_url": payload.get("html_url", f"https://github.com/{identity['id']}"),
        "source_version": str(payload.get("id")),
    }


def parse_official_payload(
    identity: dict[str, str],
    raw: bytes,
    media_type: str,
) -> dict[str, Any]:
    if identity["kind"] == "arxiv" and media_type == "application/atom+xml":
        return parse_arxiv(identity, raw)
    if identity["kind"] == "arxiv" and media_type == "application/xml":
        return parse_arxiv_oai(identity, raw)
    if identity["kind"] == "acl" and media_type == "application/x-bibtex":
        return parse_acl(identity, raw)
    if identity["kind"] == "github" and media_type == "application/json":
        return parse_github(identity, raw)
    raise ValueError(f"unsupported official payload {identity['kind']} / {media_type}")


def load_receipts(path: Path = RECEIPTS_PATH) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def validate_receipts(receipts: list[dict[str, Any]]) -> list[str]:
    failures: set[str] = set()
    policies = all_policies()
    identities = [row.get("identity", {}).get("id") for row in receipts]
    if len(identities) != len(set(identities)):
        failures.add("DUPLICATE_IDENTITY")
    if set(identities) != set(policies):
        failures.add("RECEIPT_DENOMINATOR_MISMATCH")
    for receipt in receipts:
        identity = receipt.get("identity", {})
        identity_id = identity.get("id")
        raw_binding = receipt.get("raw", {})
        if any(
            not raw_binding.get(field)
            for field in ("path", "bytes", "sha256", "media_type")
        ):
            failures.add("RAW_BINDING_INCOMPLETE")
            continue
        raw_path = ROOT / raw_binding["path"]
        if not raw_path.is_file():
            failures.add("RAW_PAYLOAD_MISSING")
            continue
        raw = raw_path.read_bytes()
        if len(raw) != raw_binding["bytes"] or hashlib.sha256(raw).hexdigest() != raw_binding["sha256"]:
            failures.add("RAW_PAYLOAD_HASH_MISMATCH")
            continue
        try:
            parsed = parse_official_payload(identity, raw, raw_binding["media_type"])
        except (ET.ParseError, ValueError, KeyError, TypeError, json.JSONDecodeError):
            failures.add("OFFICIAL_IDENTITY_ROUNDTRIP_FAILED")
            continue
        if parsed["identity"] != identity:
            failures.add("OFFICIAL_IDENTITY_ROUNDTRIP_FAILED")
        normalized = receipt.get("normalized", {})
        for field in ("title", "authors", "year", "stable_url"):
            if normalized.get(field) != parsed.get(field):
                failures.add("NORMALIZED_METADATA_MISMATCH")
        if receipt.get("source_version") != parsed.get("source_version"):
            failures.add("SOURCE_VERSION_MISMATCH")
        if receipt.get("query_recall_credit") is not False:
            failures.add("QUERY_RECALL_CREDIT_FORBIDDEN")
        if receipt.get("access_class") not in {
            "ID_DEREFERENCE",
            "PROVENANCE_FETCH",
            "REVIEW_CLAIM_VERIFICATION",
        }:
            failures.add("ACCESS_CLASS_INVALID")
        policy = policies.get(identity_id)
        if policy is None:
            failures.add("UNEXPECTED_IDENTITY")
        else:
            expected_policy = {
                key: policy[key]
                for key in (
                    "reference_role",
                    "chain",
                    "direct_neighbor",
                    "next_action",
                    "load_bearing",
                )
            }
            if receipt.get("bibliography") != expected_policy:
                failures.add("BIBLIOGRAPHY_POLICY_MISMATCH")
            if receipt.get("source_provenance") != policy["source_locator"]:
                failures.add("SOURCE_PROVENANCE_MISMATCH")
        combined = str(normalized.get("title", "")) + " " + " ".join(
            normalized.get("authors", []) if isinstance(normalized.get("authors"), list) else []
        )
        if not normalized.get("title") or not normalized.get("authors"):
            failures.add("PLACEHOLDER_OR_EMPTY_METADATA")
        if any(
            token.casefold() in combined.casefold()
            for token in ("登记待读", "作者见官方页", "TBD", "UNKNOWN_AUTHOR", "placeholder")
        ):
            failures.add("PLACEHOLDER_OR_EMPTY_METADATA")
    return sorted(failures)


def markdown_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_bibliography(receipts: list[dict[str, Any]]) -> str:
    groups = {chain: [] for chain in CHAINS}
    for receipt in receipts:
        groups[receipt["bibliography"]["chain"]].append(receipt)
    lines = [
        "---",
        'artifact_id: "SF-REVIEWER-BIBLIOGRAPHY-V2-2026-07-20-01"',
        'metadata_source: "wiki/survey/current/data/official-metadata-receipts-v1.jsonl"',
        'discipline: "official raw payload -> normalized receipt -> rendered row; known-ID accesses have zero query recall credit"',
        "---",
        "",
        "# Reviewer bibliography: system-first closure",
        "",
        "Each work appears once. Roles are the four current protocol roles; chain placement does not change mapping denominators or evidence grade.",
        "",
    ]
    order = [
        "SYSTEM_FIRST_DIRECT_NEIGHBORS",
        "REWARD_AND_VERIFICATION_MECHANISMS",
        "TRAINING_FREE_AND_TRAINED_BOUNDARIES",
    ]
    for chain in order:
        rows = sorted(
            groups[chain],
            key=lambda row: (
                row["bibliography"]["reference_role"],
                row["normalized"]["title"].casefold(),
            ),
        )
        lines.extend(
            [
                f"## {CHAIN_TITLES[chain]} ({len(rows)})",
                "",
                "| Official citation | Authors / year | Protocol role | Disposition |",
                "|---|---|---|---|",
            ]
        )
        for receipt in rows:
            normalized = receipt["normalized"]
            citation = f"[{markdown_escape(normalized['title'])}]({normalized['stable_url']})"
            authors = "; ".join(normalized["authors"])
            lines.append(
                "| "
                + " | ".join(
                    [
                        citation,
                        markdown_escape(f"{authors}, {normalized['year']}"),
                        receipt["bibliography"]["reference_role"],
                        markdown_escape(receipt["bibliography"]["next_action"]),
                    ]
                )
                + " |"
            )
        lines.append("")
    lines.extend(
        [
            f"**Total: {len(receipts)} unique works (65 retained + 12 reviewer-directed additions).**",
            "",
            "Exposure note: these are persisted known-ID metadata/provenance accesses, not systematic discovery queries; query recall credit is false for every receipt.",
            "",
        ]
    )
    return "\n".join(lines)


def write_output(receipts: list[dict[str, Any]], output: Path = OUTPUT_PATH) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_bibliography(receipts), encoding="utf-8", newline="\n")


def check_output(receipts: list[dict[str, Any]], output: Path = OUTPUT_PATH) -> list[str]:
    expected = render_bibliography(receipts).encode("utf-8")
    if not output.is_file() or output.read_bytes() != expected:
        return ["BIBLIOGRAPHY_DRIFT"]
    return []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args(argv)
    output = args.output if args.output.is_absolute() else ROOT / args.output
    receipts = load_receipts()
    failures = validate_receipts(receipts)
    if failures:
        print(json.dumps({"verdict": "FAIL", "failure_codes": failures}, indent=2))
        return 1
    if args.write:
        write_output(receipts, output)
        try:
            output_label = output.relative_to(ROOT).as_posix()
        except ValueError:
            output_label = str(output)
        print(f"PASS wrote {output_label} with {len(receipts)} unique works")
        return 0
    drift = check_output(receipts, output)
    if drift:
        print(json.dumps({"verdict": "FAIL", "failure_codes": drift}, indent=2))
        return 1
    print(f"PASS {len(receipts)} receipt-derived unique works")
    return 0


if __name__ == "__main__":
    sys.exit(main())
