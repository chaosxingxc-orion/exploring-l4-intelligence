"""Spectral features (log-mel) for traditional speech tasks. Lazy torch/torchaudio."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    import torch

from speechrl_common.audio.io import TARGET_SR


def log_mel_spectrogram(
    wav: "torch.Tensor",
    sr: int = TARGET_SR,
    n_mels: int = 80,
    n_fft: int = 400,
    hop_length: int = 160,
) -> "torch.Tensor":
    """Compute a log-mel spectrogram (Whisper-style defaults: 80 mels, 25ms/10ms)."""
    import torch
    import torchaudio  # lazy

    mel = torchaudio.transforms.MelSpectrogram(
        sample_rate=sr, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels
    )(wav)
    return torch.log(torch.clamp(mel, min=1e-10))
