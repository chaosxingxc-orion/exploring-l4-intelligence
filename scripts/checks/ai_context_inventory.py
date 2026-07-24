"""Side-effect-free fixed inventories shared by context and archive checkers."""

from __future__ import annotations

import hashlib
import json


REGISTRY_BASELINE_COUNT = 93
REGISTRY_BASELINE_PREFIX_SHA256 = (
    "73ded37c810911465eaeea0046e69f6d0e705bb1e27eb025816d0f6e5362ff0d"
)
CAMPAIGN_INDEX_BASELINE_COUNT = 44
CAMPAIGN_INDEX_BASELINE_PREFIX_SHA256 = "11a006bada352394069c72aafc8f9e2d958c303942fe47bbfee752c068fdc1db"


def registry_prefix_sha256(artifacts, count: int = REGISTRY_BASELINE_COUNT) -> str:
    """Hash canonical path/blob rows for the immutable registry baseline prefix."""

    canonical = [
        {"path": entry["path"], "git_blob": entry["git_blob"]}
        for entry in artifacts[:count]
    ]
    raw = json.dumps(
        canonical, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def campaign_index_prefix_sha256(
    semantic_entries, count: int = CAMPAIGN_INDEX_BASELINE_COUNT
) -> str:
    """Hash the exact immutable campaign-semantic prefix."""

    canonical = []
    for entry in semantic_entries[:count]:
        canonical.append(
            {
                "path": entry["path"],
                "git_blob": entry["git_blob"],
                "round": entry["round"],
                "type": entry["type"],
                "verdict": entry["verdict"],
                "disposition": entry["disposition"],
                "supersession": {
                    "mode": entry["supersession"]["mode"],
                    "target": entry["supersession"]["target"],
                    "target_current_carrier": entry["supersession"][
                        "target_current_carrier"
                    ],
                    "target_current_carrier_section": entry["supersession"][
                        "target_current_carrier_section"
                    ],
                    "transfer_rule": entry["supersession"]["transfer_rule"],
                },
                "current_carrier": entry["current_carrier"],
                "current_carrier_section": entry["current_carrier_section"],
            }
        )
    raw = json.dumps(
        canonical, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


ARCHIVE_TRANSITIONS = (
    {
        "source": "wiki/survey/2026-07-18-sf-protocol-amendment-9.md",
        "destination": (
            "wiki/archive/working/system-first-stage1a/amendments/"
            "2026-07-18-sf-protocol-amendment-9.md"
        ),
        "git_blob": "c786137a5628d963156229b6407cb8eb955e3a4c",
    },
    {
        "source": "wiki/survey/2026-07-18-sf-protocol-amendment-10.md",
        "destination": (
            "wiki/archive/working/system-first-stage1a/amendments/"
            "2026-07-18-sf-protocol-amendment-10.md"
        ),
        "git_blob": "8c6df6a092e327b2327242a1b2a47ad4f6b941e2",
    },
    {
        "source": "wiki/survey/2026-07-18-sf-protocol-amendment-11.md",
        "destination": (
            "wiki/archive/working/system-first-stage1a/amendments/"
            "2026-07-18-sf-protocol-amendment-11.md"
        ),
        "git_blob": "31c714d582f6188440da4397df05d6950aa9ba33",
    },
    {
        "source": "wiki/survey/2026-07-18-sf-protocol-amendment-12.md",
        "destination": (
            "wiki/archive/working/system-first-stage1a/amendments/"
            "2026-07-18-sf-protocol-amendment-12.md"
        ),
        "git_blob": "73c96fc47c05941d76532b3e46fa47b659004cf5",
    },
    {
        "source": "wiki/survey/2026-07-19-sf-protocol-amendment-13.md",
        "destination": (
            "wiki/archive/working/system-first-stage1a/amendments/"
            "2026-07-19-sf-protocol-amendment-13.md"
        ),
        "git_blob": "126c4dc93d1f323ba0ca5e9d3de86cc44e513045",
    },
    {
        "source": "wiki/survey/2026-07-19-sf-protocol-amendment-14.md",
        "destination": (
            "wiki/archive/working/system-first-stage1a/amendments/"
            "2026-07-19-sf-protocol-amendment-14.md"
        ),
        "git_blob": "f4c4f6490e8cc03d9103e7c4d212cd5d1dd61834",
    },
    {
        "source": "wiki/survey/2026-07-19-sf-protocol-amendment-15.md",
        "destination": (
            "wiki/archive/working/system-first-stage1a/amendments/"
            "2026-07-19-sf-protocol-amendment-15.md"
        ),
        "git_blob": "5586d6f840927f975e18a500cef74a11d9e3a48a",
    },
)
