"""speechrl_common — shared utilities for the speech-multimodal-LLM RL research series.

Importing this package is intentionally cheap: only light helpers are pulled in at the
top level. Heavy dependencies (torch, transformers, librosa, mlflow, …) are imported
lazily inside the functions that need them, so `import speechrl_common` succeeds even
before the full ML stack is installed.
"""

from speechrl_common.utils.seed import seed_everything
from speechrl_common.utils.logging import get_logger

__version__ = "0.1.0"

__all__ = ["seed_everything", "get_logger", "__version__"]
