"""Audio loading / resampling. Heavy deps (soundfile, librosa) are lazy-imported."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    import numpy as np

TARGET_SR = 16_000  # most speech encoders (Whisper, Qwen2-Audio) expect 16 kHz mono


def load_audio(path: str | Path, target_sr: int = TARGET_SR, mono: bool = True) -> "np.ndarray":
    """Load an audio file as a float32 waveform, resampled to ``target_sr``.

    Returns a 1-D array (mono) or (channels, samples) array.
    """
    import librosa  # lazy

    wav, _ = librosa.load(str(path), sr=target_sr, mono=mono)
    return wav


def save_audio(path: str | Path, wav: "np.ndarray", sr: int = TARGET_SR) -> None:
    """Write a waveform to disk (wav/flac inferred from extension)."""
    import soundfile as sf  # lazy

    Path(path).parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(path), wav, sr)
