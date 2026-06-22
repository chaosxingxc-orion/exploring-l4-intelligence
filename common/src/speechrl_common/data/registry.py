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
    task: str = "asr"  # asr | st | ser | sid | ...


# Seed registry — extend per work. (Examples; not downloaded automatically.)
# task vocabulary: asr | st | ser | sid | intent | lid (used by prompts.instruction_for + W4 axes).
REGISTRY: dict[str, DatasetSpec] = {
    # content / semantics (ASR + ST)
    "librispeech": DatasetSpec("librispeech", hf_id="openslr/librispeech_asr", task="asr"),
    "common_voice": DatasetSpec("common_voice", hf_id="mozilla-foundation/common_voice_17_0", task="asr"),
    "covost2": DatasetSpec("covost2", hf_id="facebook/covost2", task="st"),
    "fleurs": DatasetSpec("fleurs", hf_id="google/fleurs", task="lid"),
    # speaker-ID (VoxCeleb is gated on HF -> ModelScope; local subdir only)
    "voxceleb": DatasetSpec("voxceleb", hf_id=None, subdir="voxceleb", task="sid"),
    # emotion / SER
    "meld": DatasetSpec("meld", hf_id="declare-lab/MELD", task="ser"),
    "crema_d": DatasetSpec("crema_d", hf_id="MahiA/CREMA-D", subdir="crema-d", task="ser"),
    # language + intent (SLU)
    "minds14": DatasetSpec("minds14", hf_id="PolyAI/minds14", task="intent"),
    "slurp": DatasetSpec("slurp", hf_id=None, subdir="slurp", task="intent"),
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
