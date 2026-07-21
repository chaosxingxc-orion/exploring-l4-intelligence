#!/usr/bin/env python3
"""Build and validate the lossless Stage-1A existing-corpus disposition graph."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
IMPLEMENTATION_FREEZE = "d4ec803417e1e9cfe9120afbce97c676cebbe6ee"
REVIEW_SOURCE_SHA256 = "6434ee4e8a385da1f68e9a9212e615b6f0ddb41f83a06047d78060c571fe3abe"
REVIEW_2026_07_21_SOURCE_SHA256 = "4068b8e5fe5590d894db93d8cf5dc7a93c827bef9c9c9aac1072873ae0a9a98e"
ROUND16_PRECHECK_SOURCE_SHA256 = "7aec58152c3d57826d230551eab3d0c409f49394a660fd268a6ba58c826fcc1a"

CENSUS_PATH = ROOT / "wiki/survey/2026-07-14-canonical-census-v2/paper_works.jsonl"
SEED_PATH = ROOT / "wiki/survey/2026-07-15-sf-seed-manifest.jsonl"
BIBLIOGRAPHY_PATH = ROOT / "wiki/survey/2026-07-19-sf-bibliography-v1.md"
CLAIM_PATH = ROOT / "wiki/survey/2026-07-14-claim-ledger-v2/claim_ledger_v2.jsonl"
VERSION_PIN_PATH = ROOT / "wiki/survey/2026-07-14-claim-ledger-v2/version_pins.jsonl"
FULLTEXT_PATH = ROOT / "wiki/survey/2026-07-17-sf-fulltext-ledger.jsonl"
REVIEWER_KNOWN_PATH = ROOT / "wiki/survey/current/data/reviewer-known-items-v3.json"

ARTIFACT_PATH = ROOT / "wiki/survey/current/data/existing-corpus-disposition-v1.json"
REPORT_PATH = ROOT / "docs/checks/system-first-stage1a/context-v2/existing-corpus-disposition-check.json"

CAMPAIGN_ORDER = (
    "census",
    "seed",
    "bibliography",
    "claim",
    "version_pin",
    "fulltext",
    "reviewer_known",
)
CANONICAL_ROLES = {
    "DEEPLY_READ",
    "KNOWN_QUEUE",
    "MEASUREMENT_INSTRUMENT",
    "BOUNDARY_COMPARATOR",
}
ROLE_BY_BIBLIOGRAPHY_SECTION = {
    "DEEPLY_READ": "DEEPLY_READ",
    "CALIBRATION": "BOUNDARY_COMPARATOR",
    "KNOWN_QUEUE": "KNOWN_QUEUE",
    "MEASUREMENT_INSTRUMENT": "MEASUREMENT_INSTRUMENT",
    "MEASUREMENT_INSTRUMENT(trained-RM)": "MEASUREMENT_INSTRUMENT",
    "BOUNDARY/NEGATIVE_PRIOR": "BOUNDARY_COMPARATOR",
    "STAGE1B_FIRST_BATCH(P2)": "KNOWN_QUEUE",
}
RELATIONS = {"EXACT_ID", "EXPLICIT_ALIAS", "UNRESOLVED"}
ARXIV_RE = re.compile(r"(?<!\d)(\d{4}\.\d{4,5})(?:v\d+)?(?!\d)", re.I)
ACL_RE = re.compile(r"(?<![\w.-])(\d{4}\.[a-z][a-z0-9-]*\.\d+)(?![\w.-])", re.I)
URL_RE = re.compile(r"https?://[^\s|·]+")


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def rendered_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def source_paths() -> list[Path]:
    return [
        CENSUS_PATH,
        SEED_PATH,
        BIBLIOGRAPHY_PATH,
        CLAIM_PATH,
        VERSION_PIN_PATH,
        FULLTEXT_PATH,
        REVIEWER_KNOWN_PATH,
    ]


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()  # noqa: S324 - Git object identity


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def source_receipt(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": relative(path),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "git_blob": git_blob_sha1(data),
    }


def jsonl_rows(path: Path, row_id) -> list[dict[str, Any]]:
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        payload = json.loads(line)
        rows.append(
            {
                "source_row_id": row_id(line_number, payload),
                "line_number": line_number,
                "payload": payload,
                "source_path": relative(path),
            }
        )
    return rows


def parse_bibliography(path: Path) -> list[dict[str, Any]]:
    section = None
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("## "):
            match = re.match(r"## ([^（]+)", line)
            section = match.group(1).strip() if match else None
            continue
        if not line.startswith("|") or not URL_RE.search(line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 3 or section not in ROLE_BY_BIBLIOGRAPHY_SECTION:
            raise ValueError(f"unrecognized bibliography row at line {line_number}: {line}")
        title = cells[0].replace("**", "").strip()
        urls = URL_RE.findall(cells[2])
        stable_id = first_external_id(" ".join(urls)) or hashlib.sha256(
            title.encode("utf-8")
        ).hexdigest()[:12]
        rows.append(
            {
                "source_row_id": f"line:{line_number:04d}|{stable_id}",
                "line_number": line_number,
                "payload": {
                    "title": title,
                    "authors_year": cells[1],
                    "urls": urls,
                    "section": section,
                },
                "source_path": relative(path),
            }
        )
    return rows


def load_reviewer_known(path: Path) -> list[dict[str, Any]]:
    artifact = json.loads(path.read_text(encoding="utf-8"))
    if artifact.get("schema") != "sf-reviewer-known-items-v3":
        raise ValueError("reviewer-known schema mismatch")
    if artifact.get("access_class") != "REVIEW_CLAIM_VERIFICATION":
        raise ValueError("reviewer-known access class mismatch")
    if artifact.get("query_recall_credit") is not False:
        raise ValueError("reviewer-known items cannot receive query recall credit")
    if artifact.get("source_provenance", {}).get("sha256") != REVIEW_SOURCE_SHA256:
        raise ValueError("reviewer-known source provenance mismatch")
    if (
        artifact.get("additional_source_provenance", {}).get("sha256")
        != REVIEW_2026_07_21_SOURCE_SHA256
    ):
        raise ValueError("additional reviewer-known source provenance mismatch")
    if (
        artifact.get("round16_precheck_source_provenance", {}).get("sha256")
        != ROUND16_PRECHECK_SOURCE_SHA256
    ):
        raise ValueError("round-16 precheck reviewer-known provenance mismatch")
    expected_items_hash = hashlib.sha256(canonical_json_bytes(artifact["items"])).hexdigest()
    if artifact.get("items_sha256") != expected_items_hash:
        raise ValueError("reviewer-known item payload hash mismatch")
    rows = []
    for line_number, item in enumerate(artifact["items"], 1):
        if item.get("query_recall_credit") is not False:
            raise ValueError(f"reviewer-known item {item.get('item_id')} has recall credit")
        rows.append(
            {
                "source_row_id": item["item_id"],
                "line_number": line_number,
                "payload": item,
                "source_path": relative(path),
            }
        )
    return rows


def load_source_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "census": jsonl_rows(
            CENSUS_PATH,
            lambda n, p: f"line:{n:04d}|{p['work_id']}",
        ),
        "seed": jsonl_rows(
            SEED_PATH,
            lambda n, p: f"line:{n:04d}|{p['id']}",
        ),
        "bibliography": parse_bibliography(BIBLIOGRAPHY_PATH),
        "claim": jsonl_rows(
            CLAIM_PATH,
            lambda n, p: f"line:{n:04d}|{p['claim_id']}",
        ),
        "version_pin": jsonl_rows(
            VERSION_PIN_PATH,
            lambda n, p: f"line:{n:04d}|{p.get('claim_id', '_meta')}",
        ),
        "fulltext": jsonl_rows(
            FULLTEXT_PATH,
            lambda n, p: (
                f"line:{n:04d}|NOTE"
                if p.get("record_type") == "NOTE"
                else f"line:{n:04d}|{p.get('arxiv_id', 'NO_ID')}|{p.get('kind', p.get('kind_of_row', 'event'))}"
            ),
        ),
        "reviewer_known": load_reviewer_known(REVIEWER_KNOWN_PATH),
    }


def external_tokens(text: str) -> list[str]:
    tokens = [f"arxiv:{match.lower()}" for match in ARXIV_RE.findall(text or "")]
    tokens.extend(f"acl:{match.lower()}" for match in ACL_RE.findall(text or ""))
    return sorted(set(tokens))


def first_external_id(text: str) -> str | None:
    tokens = external_tokens(text)
    return tokens[0].split(":", 1)[1] if tokens else None


def stable_node_id(tokens: list[str], fallback: str) -> str:
    arxiv = next((token[6:] for token in tokens if token.startswith("arxiv:")), None)
    if arxiv:
        return "CW-ARXIV-" + arxiv
    acl = next((token[4:] for token in tokens if token.startswith("acl:")), None)
    if acl:
        return "CW-ACL-" + acl.upper()
    safe = re.sub(r"[^A-Za-z0-9.-]+", "-", fallback).strip("-")
    if safe and len(safe) <= 48:
        return "CW-" + safe
    return "CW-HASH-" + hashlib.sha256(fallback.encode("utf-8")).hexdigest()[:16]


def default_disposition() -> dict[str, Any]:
    return {
        "reason_code": None,
        "reason": "Inherited source row retained in the explicit existing-corpus queue; no deep-read or inclusion-result claim is implied.",
        "next_action": "Fetch/code in Stage-1B only if prioritized by the frozen protocol.",
        "invalidating_condition": "A verified identity conflict, REC-0 exclusion, or later adjudication supersedes this routing.",
        "load_bearing": False,
    }


class UnionBuilder:
    def __init__(self) -> None:
        self.nodes: dict[str, dict[str, Any]] = {}
        self.index: dict[str, str] = {}
        self.destinations: list[dict[str, Any]] = []
        self.claim_edges: list[dict[str, Any]] = []

    def create_or_resolve(self, tokens: list[str], fallback: str) -> dict[str, Any]:
        candidates = {self.index[token] for token in tokens if token in self.index}
        if len(candidates) > 1:
            raise ValueError(f"identity collision for {fallback}: {sorted(candidates)}")
        if candidates:
            node = self.nodes[candidates.pop()]
        else:
            node_id = stable_node_id(tokens, fallback)
            if node_id in self.nodes:
                node_id += "-" + hashlib.sha256(fallback.encode("utf-8")).hexdigest()[:8]
            node = {
                "canonical_work_id": node_id,
                "identities": [],
                "source_memberships": [],
                "screening_decision": "INCLUDE",
                "reference_role": "KNOWN_QUEUE",
                "role_assertions": [],
                "claim_evidence": [],
                "version_pins": [],
                "fulltext_events": [],
                "current_disposition": default_disposition(),
            }
            self.nodes[node_id] = node
        for token in tokens:
            previous = self.index.get(token)
            if previous is not None and previous != node["canonical_work_id"]:
                raise ValueError(f"identity token {token} maps to two works")
            self.index[token] = node["canonical_work_id"]
        return node

    @staticmethod
    def add_identity(
        node: dict[str, Any],
        source_id: str,
        relation: str,
        provenance: str,
    ) -> None:
        identity = {
            "source_id": str(source_id),
            "relation": relation,
            "provenance": provenance,
        }
        if identity not in node["identities"]:
            node["identities"].append(identity)

    def route_work(self, campaign: str, row: dict[str, Any], node: dict[str, Any]) -> None:
        membership = {"campaign": campaign, "source_row_id": row["source_row_id"]}
        node["source_memberships"].append(membership)
        self.destinations.append(
            {
                **membership,
                "destination_type": "CANONICAL_WORK",
                "canonical_work_id": node["canonical_work_id"],
            }
        )

    def route_metadata(self, campaign: str, row: dict[str, Any], reason: str) -> None:
        self.destinations.append(
            {
                "campaign": campaign,
                "source_row_id": row["source_row_id"],
                "destination_type": "SOURCE_METADATA",
                "canonical_work_id": None,
                "reason": reason,
            }
        )

    @staticmethod
    def assert_role(node: dict[str, Any], role: str, provenance: str) -> None:
        assertion = {"role": role, "provenance": provenance}
        if assertion not in node["role_assertions"]:
            node["role_assertions"].append(assertion)

    def add_census(
        self,
        row: dict[str, Any],
        *,
        unique_cluster_id: bool,
        unique_ledger_key: bool,
    ) -> None:
        p = row["payload"]
        tokens = [f"work:{p['work_id']}"]
        if unique_cluster_id:
            tokens.append(f"cluster:{p['cluster_id']}")
        tokens.extend(external_tokens(" ".join([p.get("arxiv_id", ""), p.get("canonical_url", "")])))
        if p.get("doi"):
            tokens.append("doi:" + p["doi"].lower())
        if p.get("venue_native_id"):
            tokens.append("venue:" + p["venue_native_id"].lower())
        if p.get("ledger_key") and unique_ledger_key:
            tokens.append("alias:" + p["ledger_key"].lower())
        node = self.create_or_resolve(tokens, p["work_id"])
        provenance = f"census:{row['source_row_id']}"
        self.add_identity(
            node,
            p["cluster_id"],
            "EXACT_ID" if unique_cluster_id else "EXPLICIT_ALIAS",
            provenance,
        )
        self.add_identity(node, p["work_id"], "EXACT_ID", provenance)
        for identity in [p.get("arxiv_id"), p.get("doi"), p.get("venue_native_id")]:
            if identity:
                self.add_identity(node, identity, "EXACT_ID", provenance)
        if p.get("ledger_key"):
            self.add_identity(node, p["ledger_key"], "EXPLICIT_ALIAS", provenance)
        if p.get("title"):
            self.add_identity(node, p["title"], "EXPLICIT_ALIAS", provenance)
        if p.get("status") == "IDENTITY_UNRESOLVED":
            node["screening_decision"] = "UNRESOLVED"
            node["reference_role"] = None
            node["current_disposition"] = {
                "reason_code": "IDENTITY_UNRESOLVED",
                "reason": p.get("corrections") or p.get("notes") or "Canonical identity unresolved.",
                "source": f"{row['source_path']}:{row['line_number']}",
                "owner": "Stage-1B screener",
                "deadline_gate": "Before this work can support any load-bearing claim",
                "next_action": "Resolve the conflicting IEEE document identifier against a venue-native record if this item is prioritized.",
                "invalidating_condition": "A stable venue-native identifier or REC-0 decision is independently verified.",
                "load_bearing": False,
            }
            self.add_identity(
                node,
                "IEEE document identity candidates 6424193|6424196",
                "UNRESOLVED",
                provenance,
            )
        self.route_work("census", row, node)

    def add_seed(self, row: dict[str, Any]) -> None:
        p = row["payload"]
        tokens = external_tokens(p["id"])
        alias = "alias:" + p["id"].lower()
        if alias in self.index:
            tokens.append(alias)
        if not tokens:
            tokens = ["seed:" + p["id"].lower()]
        node = self.create_or_resolve(tokens, "SEED-" + p["id"])
        provenance = f"seed:{row['source_row_id']}"
        relation = "EXACT_ID" if external_tokens(p["id"]) else "EXPLICIT_ALIAS"
        self.add_identity(node, p["id"], relation, provenance)
        self.add_identity(node, p["name"], "EXPLICIT_ALIAS", provenance)
        self.route_work("seed", row, node)

    def add_bibliography(self, row: dict[str, Any]) -> None:
        p = row["payload"]
        tokens = external_tokens(" ".join(p["urls"]))
        if not tokens:
            tokens = ["url:" + p["urls"][0].lower()]
        node = self.create_or_resolve(tokens, "BIB-" + p["title"])
        provenance = f"bibliography:{row['source_row_id']}"
        for token in tokens:
            self.add_identity(node, token.split(":", 1)[1], "EXACT_ID", provenance)
        self.add_identity(node, p["title"], "EXPLICIT_ALIAS", provenance)
        role = ROLE_BY_BIBLIOGRAPHY_SECTION[p["section"]]
        self.assert_role(node, role, provenance)
        node["current_disposition"] = {
            "reason_code": None,
            "reason": f"Explicit current-bibliography routing from section {p['section']}; canonical role is {role}.",
            "next_action": (
                "Maintain the frozen deep-read evidence binding."
                if role == "DEEPLY_READ"
                else "Retain this role and fetch/code under the frozen protocol when scheduled."
            ),
            "invalidating_condition": "The bibliography source is superseded by an adjudicated identity or role correction.",
            "load_bearing": role == "DEEPLY_READ",
        }
        self.route_work("bibliography", row, node)

    def add_claim(self, row: dict[str, Any]) -> None:
        p = row["payload"]
        source_work_ids = (
            [p["paper_work_id"]]
            if isinstance(p["paper_work_id"], str)
            else list(p["paper_work_id"])
        )
        arxiv_ids = [value.strip() for value in str(p.get("arxiv_id", "")).split(";")]
        if len(arxiv_ids) != len(source_work_ids):
            arxiv_ids = [""] * len(source_work_ids)
        provenance = f"claim:{row['source_row_id']}"
        canonical_work_ids = []
        for work_index, (source_work_id, arxiv_id) in enumerate(
            zip(source_work_ids, arxiv_ids, strict=True)
        ):
            tokens = ["cluster:" + source_work_id]
            tokens.extend(external_tokens(arxiv_id))
            candidates = {self.index[token] for token in tokens if token in self.index}
            if len(candidates) != 1:
                raise ValueError(
                    f"claim {p['claim_id']} must resolve to exactly one inherited canonical work; "
                    f"source_work_id={source_work_id} candidates={sorted(candidates)}"
                )
            node = self.nodes[candidates.pop()]
            canonical_work_ids.append(node["canonical_work_id"])
            self.add_identity(node, source_work_id, "EXACT_ID", provenance)
            if arxiv_id:
                self.add_identity(node, arxiv_id, "EXACT_ID", provenance)
            node["claim_evidence"].append(
                {
                    "claim_id": p["claim_id"],
                    "source_work_id": source_work_id,
                    "linked_work_index": work_index,
                    "evidence_grade": p.get("evidence_grade"),
                    "discrepancy_status": p.get("discrepancy_status"),
                    "locator": p.get("source_locator"),
                    "version": p.get("paper_version_used"),
                    "support_relation": p.get("support_relation"),
                    "requires_upstream_correction": p.get("requires_upstream_correction"),
                    "source_row_id": row["source_row_id"],
                }
            )
        edge = {
            "claim_id": p["claim_id"],
            "source_row_id": row["source_row_id"],
            "source_work_ids": source_work_ids,
            "canonical_work_ids": canonical_work_ids,
            "evidence_grade": p.get("evidence_grade"),
            "discrepancy_status": p.get("discrepancy_status"),
        }
        self.claim_edges.append(edge)
        self.destinations.append(
            {
                "campaign": "claim",
                "source_row_id": row["source_row_id"],
                "destination_type": "CLAIM_EDGE",
                "canonical_work_id": None,
                "claim_id": p["claim_id"],
                "canonical_work_ids": canonical_work_ids,
            }
        )

    def add_version_pin(self, row: dict[str, Any]) -> None:
        p = row["payload"]
        if "_meta" in p:
            self.route_metadata("version_pin", row, "Version-pin overlay metadata row; not a research work.")
            return
        node = self.create_or_resolve(
            ["cluster:" + p["cluster_id"], "work:" + p["work_id"]],
            p["cluster_id"],
        )
        provenance = f"version_pin:{row['source_row_id']}"
        self.add_identity(node, p["cluster_id"], "EXACT_ID", provenance)
        self.add_identity(node, p["work_id"], "EXACT_ID", provenance)
        node["version_pins"].append(
            {
                "claim_id": p["claim_id"],
                "pinned_version": p["pinned_version"],
                "version_date": p["version_date"],
                "status": p["status"],
                "source_row_id": row["source_row_id"],
            }
        )
        self.route_work("version_pin", row, node)

    def add_fulltext(self, row: dict[str, Any]) -> None:
        p = row["payload"]
        if p.get("record_type") == "NOTE":
            self.route_metadata("fulltext", row, "Fulltext-ledger path-correction note; not a research work.")
            return
        arxiv_id = p.get("arxiv_id")
        if not arxiv_id:
            raise ValueError(f"fulltext work row lacks arXiv identity: {row['source_row_id']}")
        node = self.create_or_resolve(["arxiv:" + arxiv_id.lower()], arxiv_id)
        provenance = f"fulltext:{row['source_row_id']}"
        self.add_identity(node, arxiv_id, "EXACT_ID", provenance)
        node["fulltext_events"].append(
            {
                "kind": p.get("kind", p.get("kind_of_row")),
                "sha256": p.get("sha256"),
                "http_status": p.get("http_status"),
                "error": p.get("error"),
                "access_class": p.get("access_class"),
                "source_row_id": row["source_row_id"],
            }
        )
        self.route_work("fulltext", row, node)

    def add_reviewer_known(self, row: dict[str, Any]) -> None:
        p = row["payload"]
        tokens = ["arxiv:" + p["arxiv_id"].lower()]
        node = self.create_or_resolve(tokens, p["arxiv_id"])
        provenance = f"reviewer_known:{row['source_row_id']}"
        self.add_identity(node, p["arxiv_id"], "EXACT_ID", provenance)
        self.add_identity(node, p["title"], "EXPLICIT_ALIAS", provenance)
        self.assert_role(node, p["reference_role"], provenance)
        node["current_disposition"] = {
            "reason_code": None,
            **p["current_disposition"],
            "load_bearing": p["load_bearing"],
            "query_recall_credit": p["query_recall_credit"],
        }
        self.route_work("reviewer_known", row, node)

    def finalize(self) -> list[dict[str, Any]]:
        for node in self.nodes.values():
            asserted = {row["role"] for row in node["role_assertions"]}
            if len(asserted) > 1:
                raise ValueError(
                    f"conflicting canonical roles for {node['canonical_work_id']}: {sorted(asserted)}"
                )
            if node["screening_decision"] == "INCLUDE":
                node["reference_role"] = next(iter(asserted), "KNOWN_QUEUE")
            node["identities"].sort(key=lambda row: (row["source_id"], row["relation"], row["provenance"]))
            node["source_memberships"].sort(
                key=lambda row: (CAMPAIGN_ORDER.index(row["campaign"]), row["source_row_id"])
            )
            node["role_assertions"].sort(key=lambda row: (row["role"], row["provenance"]))
            node["claim_evidence"].sort(key=lambda row: row["claim_id"])
            node["version_pins"].sort(key=lambda row: row["source_row_id"])
            node["fulltext_events"].sort(key=lambda row: row["source_row_id"])
        self.destinations.sort(
            key=lambda row: (CAMPAIGN_ORDER.index(row["campaign"]), row["source_row_id"])
        )
        self.claim_edges.sort(key=lambda row: row["claim_id"])
        return sorted(self.nodes.values(), key=lambda row: row["canonical_work_id"])


def build_union(sources: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    builder = UnionBuilder()
    cluster_counts = Counter(row["payload"]["cluster_id"] for row in sources["census"])
    ledger_key_counts = Counter(
        row["payload"].get("ledger_key") for row in sources["census"]
        if row["payload"].get("ledger_key")
    )
    for row in sources["census"]:
        builder.add_census(
            row,
            unique_cluster_id=cluster_counts[row["payload"]["cluster_id"]] == 1,
            unique_ledger_key=ledger_key_counts[row["payload"].get("ledger_key")] == 1,
        )
    for row in sources["seed"]:
        builder.add_seed(row)
    for row in sources["bibliography"]:
        builder.add_bibliography(row)
    for row in sources["claim"]:
        builder.add_claim(row)
    for row in sources["version_pin"]:
        builder.add_version_pin(row)
    for row in sources["fulltext"]:
        builder.add_fulltext(row)
    for row in sources["reviewer_known"]:
        builder.add_reviewer_known(row)
    nodes = builder.finalize()

    arxiv_nodes = {
        node["canonical_work_id"]
        for node in nodes
        if any(ARXIV_RE.fullmatch(identity["source_id"]) for identity in node["identities"])
    }
    pinned_nodes = {
        row["canonical_work_id"]
        for row in builder.destinations
        if row["campaign"] == "version_pin" and row["destination_type"] == "CANONICAL_WORK"
    }
    pinned_arxiv_nodes = pinned_nodes & arxiv_nodes
    campaign_work_ids: dict[str, set[str]] = {campaign: set() for campaign in CAMPAIGN_ORDER}
    for destination in builder.destinations:
        campaign = destination["campaign"]
        if destination["destination_type"] == "CANONICAL_WORK":
            campaign_work_ids[campaign].add(destination["canonical_work_id"])
        elif destination["destination_type"] == "CLAIM_EDGE":
            campaign_work_ids[campaign].update(destination["canonical_work_ids"])
    claim_work_reference_count = sum(
        len(edge["canonical_work_ids"]) for edge in builder.claim_edges
    )
    source_denominators = {campaign: len(sources[campaign]) for campaign in CAMPAIGN_ORDER}
    unresolved = [node for node in nodes if node["screening_decision"] == "UNRESOLVED"]
    multi_claim_nodes = [node for node in nodes if len(node["claim_evidence"]) > 1]
    multi_grade_nodes = [
        node
        for node in nodes
        if len({row["evidence_grade"] for row in node["claim_evidence"]}) > 1
    ]
    multi_status_nodes = [
        node
        for node in nodes
        if len({row["discrepancy_status"] for row in node["claim_evidence"]}) > 1
    ]
    artifact = {
        "artifact_id": "SF-EXISTING-CORPUS-DISPOSITION-V1-2026-07-20-01",
        "schema": "sf-existing-corpus-union-v1",
        "implementation_freeze": IMPLEMENTATION_FREEZE,
        "scope_statement": (
            "Existing-source disposition only. unexplained_orphans=0 means every source row has one explicit "
            "destination; it does not mean every work is verified, included in a systematic map, or deeply read."
        ),
        "source_denominators": source_denominators,
        "source_receipts": [source_receipt(path) for path in source_paths()],
        "canonical_reference_roles": sorted(CANONICAL_ROLES),
        "source_dispositions": builder.destinations,
        "claim_edges": builder.claim_edges,
        "canonical_work_nodes": nodes,
        "identity_accounting": {
            "all_arxiv_identity_count": len(arxiv_nodes),
            "all_arxiv_identity_work_ids": sorted(arxiv_nodes),
            "version_pinned_work_count": len(pinned_nodes),
            "version_pinned_work_ids": sorted(pinned_nodes),
            "version_pinned_arxiv_identity_count": len(pinned_arxiv_nodes),
            "version_pinned_arxiv_work_ids": sorted(pinned_arxiv_nodes),
            "version_pinned_arxiv_set_equal": pinned_nodes == pinned_arxiv_nodes,
        },
        "deduplication_accounting": {
            "census_source_rows": len(sources["census"]),
            "unique_census_works": len(campaign_work_ids["census"]),
            "seed_source_rows": len(sources["seed"]),
            "unique_seed_works": len(campaign_work_ids["seed"]),
            "duplicate_seed_source_rows": len(sources["seed"]) - len(campaign_work_ids["seed"]),
            "seed_rows_reusing_census_work": len(
                campaign_work_ids["seed"] & campaign_work_ids["census"]
            ),
            "generated_seed_rows": 0,
            "claim_source_rows": len(sources["claim"]),
            "claim_work_references": claim_work_reference_count,
            "unique_claim_works": len(campaign_work_ids["claim"]),
            "deduplicated_claim_work_references": (
                claim_work_reference_count - len(campaign_work_ids["claim"])
            ),
            "claim_targets_not_in_census": len(
                campaign_work_ids["claim"] - campaign_work_ids["census"]
            ),
        },
        "unresolved_records": [
            {
                "canonical_work_id": node["canonical_work_id"],
                **node["current_disposition"],
            }
            for node in unresolved
        ],
        "summary": {
            "source_rows": sum(source_denominators.values()),
            "canonical_work_nodes": len(nodes),
            "source_metadata_rows": sum(
                row["destination_type"] == "SOURCE_METADATA" for row in builder.destinations
            ),
            "claim_edges": len(builder.claim_edges),
            "multi_target_claim_edges": sum(
                len(edge["canonical_work_ids"]) > 1 for edge in builder.claim_edges
            ),
            "multi_claim_work_count": len(multi_claim_nodes),
            "multi_evidence_grade_work_count": len(multi_grade_nodes),
            "multi_discrepancy_status_work_count": len(multi_status_nodes),
            "unexplained_orphans": 0,
            "unresolved_records": len(unresolved),
            "load_bearing_unresolved": sum(
                bool(node["current_disposition"].get("load_bearing")) for node in unresolved
            ),
        },
    }
    return artifact


def validate_union(
    artifact: dict[str, Any],
    sources: dict[str, list[dict[str, Any]]],
) -> list[str]:
    failures: set[str] = set()
    expected = Counter(
        (campaign, row["source_row_id"])
        for campaign, rows in sources.items()
        for row in rows
    )
    destinations = Counter(
        (row.get("campaign"), row.get("source_row_id"))
        for row in artifact.get("source_dispositions", [])
    )
    if destinations != expected:
        failures.add("SOURCE_DESTINATION_MISMATCH")
    if any(count > 1 for count in destinations.values()):
        failures.add("DUPLICATE_SOURCE_DESTINATION")

    node_memberships = Counter()
    claim_projections = Counter()
    external_identity_nodes: dict[str, set[str]] = {}
    for node in artifact.get("canonical_work_nodes", []):
        if "evidence_grade" in node or "discrepancy_status" in node:
            failures.add("WORK_LEVEL_CLAIM_SCALAR")
        for membership in node.get("source_memberships", []):
            node_memberships[(membership.get("campaign"), membership.get("source_row_id"))] += 1
        for claim in node.get("claim_evidence", []):
            claim_projections[(claim.get("claim_id"), node.get("canonical_work_id"))] += 1
        decision = node.get("screening_decision")
        role = node.get("reference_role")
        disposition = node.get("current_disposition", {})
        if role is not None and role not in CANONICAL_ROLES:
            failures.add("NONCANONICAL_REFERENCE_ROLE")
        if decision == "INCLUDE" and role not in CANONICAL_ROLES:
            failures.add("INCLUDE_WITHOUT_CANONICAL_ROLE")
        elif decision == "EXCLUDE":
            if role is not None:
                failures.add("EXCLUDE_WITH_ROLE")
            if not str(disposition.get("reason_code", "")).startswith("REC-0"):
                failures.add("EXCLUDE_WITHOUT_REC_0")
        elif decision == "UNRESOLVED":
            required = {"source", "reason", "owner", "deadline_gate", "next_action"}
            if any(not disposition.get(field) for field in required):
                failures.add("UNRESOLVED_OBLIGATION_INCOMPLETE")
            if disposition.get("load_bearing"):
                failures.add("LOAD_BEARING_UNRESOLVED")
        elif decision not in {"INCLUDE", "EXCLUDE", "UNRESOLVED"}:
            failures.add("INVALID_SCREENING_DECISION")
        if any(identity.get("relation") not in RELATIONS for identity in node.get("identities", [])):
            failures.add("INVALID_IDENTITY_RELATION")
        for identity_row in node.get("identities", []):
            source_id = str(identity_row.get("source_id", "")).strip().lower()
            if (
                ARXIV_RE.fullmatch(source_id)
                or ACL_RE.fullmatch(source_id)
                or source_id.startswith("10.")
            ):
                external_identity_nodes.setdefault(source_id, set()).add(
                    node.get("canonical_work_id")
                )

    if any(len(node_ids) > 1 for node_ids in external_identity_nodes.values()):
        failures.add("DUPLICATE_CANONICAL_IDENTITY")

    expected_work_memberships = Counter(
        (row["campaign"], row["source_row_id"])
        for row in artifact.get("source_dispositions", [])
        if row.get("destination_type") == "CANONICAL_WORK"
    )
    if any(count > 1 for count in node_memberships.values()):
        failures.add("DUPLICATE_SOURCE_MEMBERSHIP")
    if node_memberships != expected_work_memberships:
        failures.add("SOURCE_MEMBERSHIP_MISMATCH")

    expected_claim_rows = {
        row["source_row_id"]: (
            [row["payload"]["paper_work_id"]]
            if isinstance(row["payload"]["paper_work_id"], str)
            else row["payload"]["paper_work_id"]
        )
        for row in sources["claim"]
    }
    edges = artifact.get("claim_edges", [])
    edge_rows = Counter(edge.get("source_row_id") for edge in edges)
    if edge_rows != Counter(expected_claim_rows.keys()):
        failures.add("CLAIM_EDGE_MEMBERSHIP_MISMATCH")
    expected_projections = Counter()
    for edge in edges:
        source_row_id = edge.get("source_row_id")
        if edge.get("source_work_ids") != expected_claim_rows.get(source_row_id):
            failures.add("CLAIM_EDGE_SOURCE_WORK_MISMATCH")
        canonical_work_ids = edge.get("canonical_work_ids", [])
        if len(canonical_work_ids) != len(edge.get("source_work_ids", [])):
            failures.add("CLAIM_EDGE_TARGET_COUNT_MISMATCH")
        for canonical_work_id in canonical_work_ids:
            expected_projections[(edge.get("claim_id"), canonical_work_id)] += 1
    if claim_projections != expected_projections:
        failures.add("CLAIM_MEMBERSHIP_MISMATCH")

    denominators = {campaign: len(rows) for campaign, rows in sources.items()}
    if artifact.get("source_denominators") != denominators:
        failures.add("SOURCE_DENOMINATOR_MISMATCH")
    if artifact.get("source_receipts") != [source_receipt(path) for path in source_paths()]:
        failures.add("SOURCE_RECEIPT_MISMATCH")
    if artifact.get("summary", {}).get("unexplained_orphans") != 0:
        failures.add("UNEXPLAINED_ORPHANS_NONZERO")
    nodes = artifact.get("canonical_work_nodes", [])
    expected_heterogeneity = {
        "multi_target_claim_edges": sum(
            len(edge.get("canonical_work_ids", [])) > 1 for edge in edges
        ),
        "multi_claim_work_count": sum(len(node.get("claim_evidence", [])) > 1 for node in nodes),
        "multi_evidence_grade_work_count": sum(
            len({row.get("evidence_grade") for row in node.get("claim_evidence", [])}) > 1
            for node in nodes
        ),
        "multi_discrepancy_status_work_count": sum(
            len({row.get("discrepancy_status") for row in node.get("claim_evidence", [])}) > 1
            for node in nodes
        ),
    }
    if any(
        artifact.get("summary", {}).get(field) != value
        for field, value in expected_heterogeneity.items()
    ):
        failures.add("HETEROGENEITY_ACCOUNTING_MISMATCH")
    identity = artifact.get("identity_accounting", {})
    if identity.get("version_pinned_work_ids") != identity.get("version_pinned_arxiv_work_ids"):
        failures.add("VERSION_PIN_ARXIV_SET_MISMATCH")
    if identity.get("version_pinned_arxiv_set_equal") is not True:
        failures.add("VERSION_PIN_ARXIV_SET_NOT_PROVED")
    work_sets: dict[str, set[str]] = {campaign: set() for campaign in CAMPAIGN_ORDER}
    for destination in artifact.get("source_dispositions", []):
        campaign = destination.get("campaign")
        if campaign not in work_sets:
            continue
        if destination.get("destination_type") == "CANONICAL_WORK":
            work_sets[campaign].add(destination.get("canonical_work_id"))
        elif destination.get("destination_type") == "CLAIM_EDGE":
            work_sets[campaign].update(destination.get("canonical_work_ids", []))
    claim_reference_count = sum(len(edge.get("canonical_work_ids", [])) for edge in edges)
    expected_deduplication = {
        "census_source_rows": len(sources["census"]),
        "unique_census_works": len(work_sets["census"]),
        "seed_source_rows": len(sources["seed"]),
        "unique_seed_works": len(work_sets["seed"]),
        "duplicate_seed_source_rows": len(sources["seed"]) - len(work_sets["seed"]),
        "seed_rows_reusing_census_work": len(work_sets["seed"] & work_sets["census"]),
        "generated_seed_rows": 0,
        "claim_source_rows": len(sources["claim"]),
        "claim_work_references": claim_reference_count,
        "unique_claim_works": len(work_sets["claim"]),
        "deduplicated_claim_work_references": claim_reference_count - len(work_sets["claim"]),
        "claim_targets_not_in_census": len(work_sets["claim"] - work_sets["census"]),
    }
    if artifact.get("deduplication_accounting") != expected_deduplication:
        failures.add("DEDUPLICATION_ACCOUNTING_MISMATCH")
    if expected_deduplication["unique_census_works"] != len(sources["census"]):
        failures.add("CENSUS_WORK_COLLAPSE")
    if expected_deduplication["generated_seed_rows"] != 0:
        failures.add("GENERATED_SEED_ROWS")
    if expected_deduplication["claim_targets_not_in_census"] != 0:
        failures.add("CLAIM_CREATED_CANONICAL_WORK")
    return sorted(failures)


def make_report(artifact: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_id": "SF-EXISTING-CORPUS-DISPOSITION-CHECK-2026-07-20-01",
        "implementation_freeze": IMPLEMENTATION_FREEZE,
        "checked_artifact": {
            "path": relative(ARTIFACT_PATH),
            "sha256": hashlib.sha256(rendered_json_bytes(artifact)).hexdigest(),
        },
        "source_denominators": artifact["source_denominators"],
        "summary": artifact["summary"],
        "identity_accounting": artifact["identity_accounting"],
        "deduplication_accounting": artifact["deduplication_accounting"],
        "failure_codes": [],
        "verdict": "PASS",
        "interpretation_guard": artifact["scope_statement"],
    }


def write_outputs(
    artifact: dict[str, Any],
    *,
    artifact_path: Path = ARTIFACT_PATH,
    report_path: Path = REPORT_PATH,
) -> None:
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_bytes(rendered_json_bytes(artifact))
    report = make_report(artifact)
    if artifact_path != ARTIFACT_PATH:
        report["checked_artifact"]["path"] = artifact_path.name
    report_path.write_bytes(rendered_json_bytes(report))


def check_outputs(
    artifact: dict[str, Any],
    *,
    artifact_path: Path = ARTIFACT_PATH,
    report_path: Path = REPORT_PATH,
) -> list[str]:
    failures = []
    expected_artifact = rendered_json_bytes(artifact)
    if not artifact_path.exists() or artifact_path.read_bytes() != expected_artifact:
        failures.append("ARTIFACT_DRIFT")
    report = make_report(artifact)
    if artifact_path != ARTIFACT_PATH:
        report["checked_artifact"]["path"] = artifact_path.name
    expected_report = rendered_json_bytes(report)
    if not report_path.exists() or report_path.read_bytes() != expected_report:
        failures.append("REPORT_DRIFT")
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    sources = load_source_rows()
    artifact = build_union(sources)
    failures = validate_union(artifact, sources)
    if failures:
        print(json.dumps({"verdict": "FAIL", "failure_codes": failures}, indent=2))
        return 1
    if args.write:
        write_outputs(artifact)
        print(
            f"PASS wrote {relative(ARTIFACT_PATH)} and {relative(REPORT_PATH)}; "
            f"source_rows={artifact['summary']['source_rows']} nodes={artifact['summary']['canonical_work_nodes']}"
        )
        return 0
    drift = check_outputs(artifact)
    if drift:
        print(json.dumps({"verdict": "FAIL", "failure_codes": drift}, indent=2))
        return 1
    print(
        f"PASS {artifact['summary']['source_rows']} source rows, "
        f"{artifact['summary']['unexplained_orphans']} unexplained orphans"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
