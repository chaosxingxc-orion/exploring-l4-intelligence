"""Reproducibility helpers."""
from __future__ import annotations

import os
import random


def seed_everything(seed: int = 42, *, deterministic: bool = False) -> int:
    """Seed Python, NumPy, and (if available) PyTorch RNGs.

    Heavy libs are imported lazily so this works before they are installed.

    Args:
        seed: the seed value.
        deterministic: if True and torch is present, force deterministic cuDNN.

    Returns:
        The seed used (handy for logging).
    """
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)

    try:
        import numpy as np

        np.random.seed(seed)
    except ImportError:
        pass

    try:
        import torch

        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        if deterministic:
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
    except ImportError:
        pass

    return seed
