"""Reusable exact contract for taxonomy v6 over frozen taxonomy-v5 semantics."""
from __future__ import annotations

from collections.abc import Mapping


SEMANTIC_KEYS = (
    "enums",
    "signal_schema",
    "control_edge_schema",
    "signal_use",
    "decision_rights",
    "reward_forms",
    "allowed_relations",
    "allowed_relations_provenance",
    "derived_v5",
    "adjudication_binding",
    "cross_platform_contract",
    "killer_and_acceptance_contract",
    "single_write_pipeline",
)
FROZEN_TAXONOMY_V5_SHA256 = (
    "9f6407266a808fb012ae63811821c3c1cd950996b8bf733fd4711812d896b106"
)

ROW_CLAIMS = (
    "core_weight_update",
    "external_component_weight_update",
    "controller_program_or_config_optimized_on_labels",
    "human_or_dev_label_model_selection",
    "deployment_label_access",
    "test_item_gold_access",
    "inference_external_new_information",
    "internal_visibility",
    "core_topology",
    "core_native_modality",
    "control_horizon",
    "decision_rights",
    "candidate_pool_exists",
    "selection_policy",
    "selection_object",
    "explicit_candidate_pool_selection",
)
SIGNAL_CLAIMS = ("form", "source", "lifecycle", "uses")
EDGE_CLAIMS = ("signal_use", "decision_right")

EXPECTED_ADDED_KEYS = frozenset({"schema", "derivation_semantics"})
EXPECTED_CHANGED_KEYS = frozenset(
    {
        "artifact_id",
        "title",
        "supersession",
        "required_evidence_contract",
        "release_binding",
    }
)
RELEASE_RULE = (
    "active release discovery resolves through "
    "wiki/survey/current/manifest.json; historical bound artifacts remain "
    "available through explicit legacy regression."
)

EXPECTED_METADATA = {
    "artifact_id": "SF-IDENTITY-TAXONOMY-V6-2026-07-19-01",
    "schema": (
        "schema-v3: row16 + signal4 + edge2 evidence bindings; "
        "discriminative PDF anchors"
    ),
    "derivation_semantics": "UNCHANGED_FROM_TAXONOMY_V5",
    "title": (
        "identity taxonomy v6 — frozen derivation semantics with schema-v3 "
        "evidence contract"
    ),
    "supersession": (
        "v6 supersedes v5 for active release discovery; derivation semantics "
        "unchanged, evidence contract upgraded to schema-v3 row16 + signal4 + "
        "edge2 bindings and discriminative PDF anchors."
    ),
}


def validate_taxonomy_v6(v5, v6):
    """Return stable failure codes; an empty list is the only pass state."""
    failures = []
    if not isinstance(v5, Mapping):
        return ["taxonomy-v5:container-invalid"]
    if not isinstance(v6, Mapping):
        return ["taxonomy-v6:container-invalid"]

    v5_keys = set(v5)
    v6_keys = set(v6)
    added = v6_keys - v5_keys
    removed = v5_keys - v6_keys
    changed = {key for key in v5_keys & v6_keys if v5[key] != v6[key]}
    if added != EXPECTED_ADDED_KEYS:
        failures.append(
            "taxonomy-v6:top-level-added-keys-mismatch:"
            f"{sorted(added)}"
        )
    if removed:
        failures.append(
            f"taxonomy-v6:top-level-removed-keys:{sorted(removed)}"
        )
    if changed != EXPECTED_CHANGED_KEYS:
        failures.append(
            "taxonomy-v6:top-level-changed-keys-mismatch:"
            f"{sorted(changed)}"
        )

    for key in SEMANTIC_KEYS:
        if key not in v5 or key not in v6 or v5.get(key) != v6.get(key):
            failures.append(f"taxonomy-v6:semantic-drift:{key}")
    if "derived_v6" in v6 or "derived_v5" not in v6:
        failures.append("taxonomy-v6:derivation-key-drift")

    for key, expected in EXPECTED_METADATA.items():
        if v6.get(key) != expected:
            failures.append(f"taxonomy-v6:metadata-mismatch:{key}")

    contract = v6.get("required_evidence_contract")
    if not isinstance(contract, Mapping):
        failures.append("taxonomy-v6:evidence-contract-container-invalid")
    else:
        if set(contract) != {"principle", "claims", "evidence_kinds"}:
            failures.append("taxonomy-v6:evidence-contract-keys-mismatch")
        if contract.get("principle") != (
            "Every load-bearing encoded value is field-bound and "
            "source-resolved before derivation."
        ):
            failures.append("taxonomy-v6:evidence-principle-mismatch")
        expected_claims = {
            "row": list(ROW_CLAIMS),
            "signal": list(SIGNAL_CLAIMS),
            "edge": list(EDGE_CLAIMS),
        }
        if contract.get("claims") != expected_claims:
            failures.append("taxonomy-v6:evidence-claims-mismatch")
        v5_contract = v5.get("required_evidence_contract")
        v5_kinds = (
            v5_contract.get("evidence_kinds")
            if isinstance(v5_contract, Mapping)
            else None
        )
        if contract.get("evidence_kinds") != v5_kinds:
            failures.append("taxonomy-v6:evidence-kinds-mismatch")

    if v6.get("release_binding") != {"rule": RELEASE_RULE}:
        failures.append("taxonomy-v6:release-binding-mismatch")
    return failures
