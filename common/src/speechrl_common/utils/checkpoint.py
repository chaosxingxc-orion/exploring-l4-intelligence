"""Checkpoint path helpers (storage lives in WSL ext4, not in git)."""
from __future__ import annotations

import os
from pathlib import Path


def checkpoint_root() -> Path:
    """Root for checkpoints. Override with SPEECHRL_CKPT_DIR.

    Defaults to ~/speechrl-data/checkpoints (WSL ext4) per the workspace layout.
    """
    env = os.environ.get("SPEECHRL_CKPT_DIR")
    root = Path(env) if env else Path.home() / "speechrl-data" / "checkpoints"
    root.mkdir(parents=True, exist_ok=True)
    return root


def run_dir(work: str, run_name: str) -> Path:
    """Return (and create) a per-run checkpoint directory: <root>/<work>/<run_name>."""
    d = checkpoint_root() / work / run_name
    d.mkdir(parents=True, exist_ok=True)
    return d
