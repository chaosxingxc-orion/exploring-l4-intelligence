"""Verifiable reward functions for speech RL (GRPO/PPO).

These are deliberately dependency-light and string-based so they can serve as
verl/TRL reward callables. ``jiwer`` is lazy-imported only for WER/CER.
"""
from __future__ import annotations

import re


def _normalize(text: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace — standard ASR scoring norm."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s']", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def wer(reference: str, hypothesis: str) -> float:
    """Word error rate in [0, inf). Lower is better."""
    import jiwer  # lazy

    return float(jiwer.wer(_normalize(reference), _normalize(hypothesis)))


def asr_reward(reference: str, hypothesis: str) -> float:
    """Reward in [0, 1] for ASR: 1 - clipped WER. Use directly as a GRPO reward."""
    return max(0.0, 1.0 - wer(reference, hypothesis))


def exact_match_reward(reference: str, hypothesis: str) -> float:
    """1.0 if normalized strings match (classification tasks: emotion, gender, …)."""
    return 1.0 if _normalize(reference) == _normalize(hypothesis) else 0.0
