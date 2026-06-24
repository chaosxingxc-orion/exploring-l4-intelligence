"""A tiny dataset registry so each work refers to datasets by name, not path.

Actual data lives in WSL ext4 (``~/speechrl-data/datasets`` or $SPEECHRL_DATA_DIR),
never in git. Register HF hub ids or local subdirs here as the works adopt datasets.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DatasetSpec:
    name: str
    hf_id: str | None = None  # Hugging Face hub id, if applicable
    subdir: str | None = None  # local subdir under the data root, if applicable
    task: str = "asr"  # asr | st | ser | sid | intent | lid
    revision: str | None = None  # pinned snapshot (HF/git sha); None = unpinned. See docs/datasets.lock.json


# Seed registry — the speech *factor-family* datasets W4 disentangles, referred to by name.
# The dataset SET IS FROZEN to the local snapshot; the full inventory (incl. the ~17 semantic eval
# benches) plus exact per-asset revisions live in docs/datasets.lock.json. `revision` below is the
# HF/git commit sha where the local snapshot recorded one; None = unpinned (ModelScope 'master' or
# content-fingerprinted). task vocabulary: asr | st | ser | sid | intent | lid (used by
# prompts.instruction_for + the W4 axes).
REGISTRY: dict[str, DatasetSpec] = {
    # content / semantics (ASR + ST)
    "librispeech": DatasetSpec("librispeech", hf_id="openslr/librispeech_asr", task="asr"),  # local snapshot via ModelScope (master)
    "common_voice": DatasetSpec("common_voice", hf_id="mozilla-foundation/common_voice_17_0", task="asr"),  # example only — NOT in the frozen local set
    "covost2": DatasetSpec("covost2", hf_id="facebook/covost2", task="st"),
    "fleurs": DatasetSpec("fleurs", hf_id="google/fleurs-r", subdir="fleurs-r", task="lid",
                          revision="c621c0b7b569dcebcd50273a187a35d1a1fc895f"),  # FLEURS-R (restored) is what's on disk
    # speaker-ID: VoxCeleb was a placeholder (gated, never downloaded) and has been removed;
    # speaker identity is exercised via crema_d (speaker + emotion on the same audio).
    # emotion / SER
    "meld": DatasetSpec("meld", hf_id="declare-lab/MELD", task="ser",
                        revision="9abc51ee7903424ffb971297608aa6d3d0de3bfa"),
    "crema_d": DatasetSpec("crema_d", hf_id="MahiA/CREMA-D", subdir="crema-d", task="ser",
                          revision="ac5b65fb890f1db0d2f7d6268d13994f481e5567"),
    # language + intent (SLU)
    "minds14": DatasetSpec("minds14", hf_id="PolyAI/minds14", task="intent"),
    "slurp": DatasetSpec("slurp", hf_id=None, subdir="slurp", task="intent",
                        revision="8eb16545762be97ace75334109d73824217311f1"),  # git; audio at repos/slurp/scripts/audio (Zenodo 4274930)
}


def data_root() -> Path:
    """Root for datasets. Override with SPEECHRL_DATA_DIR (defaults to WSL ext4 path)."""
    env = os.environ.get("SPEECHRL_DATA_DIR")
    return Path(env) if env else Path.home() / "speechrl-data" / "datasets"


def get(name: str) -> DatasetSpec:
    """Look up a registered dataset (raises KeyError if unknown)."""
    return REGISTRY[name]


def register(spec: DatasetSpec) -> None:
    """Add/override a dataset spec at runtime."""
    REGISTRY[spec.name] = spec
