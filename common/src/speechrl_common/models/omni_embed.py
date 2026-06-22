"""Loader + audio→embedding for the omni-embed-nemotron-3b flagship backbone (frozen).

Mirrors ``qwen2_audio.py``'s discipline: nothing heavy at import time; ``torch`` and
``sentence_transformers`` are imported inside ``load_omni_embedder``. The model is a
SentenceTransformer (Transformer → mean Pooling → L2 Normalize), output dim 2048, cosine.
The disentanglement hook is the text paired with the audio in a document item.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

DEFAULT_OMNI_EMBED_ID = "nvidia/omni-embed-nemotron-3b"
EMBED_DIM = 2048


@dataclass
class LoadedEmbedder:
    model: Any
    model_id: str
    embed_dim: int = EMBED_DIM


def load_omni_embedder(
    model_id: str = DEFAULT_OMNI_EMBED_ID,
    *,
    device: str | None = "cuda",
    torch_dtype: str = "bfloat16",
    attn_implementation: str | None = "flash_attention_2",
    trust_remote_code: bool = True,
) -> LoadedEmbedder:
    """Load the frozen omni-embed SentenceTransformer.

    Pass a local path as ``model_id`` to use an on-disk copy. ``attn_implementation`` falls back
    to ``"sdpa"`` if flash-attn is unavailable (e.g. on Blackwell sm_120). The model is frozen
    (``eval``, no grad) — this is *training-free* by construction.
    """
    import torch
    from sentence_transformers import SentenceTransformer

    model_kwargs = {"torch_dtype": getattr(torch, torch_dtype)}
    if attn_implementation:
        model_kwargs["attn_implementation"] = attn_implementation

    def _build(mk):
        return SentenceTransformer(
            model_id, trust_remote_code=trust_remote_code, model_kwargs=mk, device=device
        )

    try:
        model = _build(model_kwargs)
    except Exception:
        # flash-attn unavailable on this arch — retry with SDPA.
        model = _build({**model_kwargs, "attn_implementation": "sdpa"})

    model.eval()
    return LoadedEmbedder(model=model, model_id=model_id, embed_dim=EMBED_DIM)


def embed_audio(embedder: LoadedEmbedder, wav, *, sr: int = 16_000,
                task_prompt: str | None = None, normalize: bool = True):
    """Embed a single 1-D waveform (np.ndarray @ ``sr``, assumed 16 kHz). Returns ``(embed_dim,)``.

    ``task_prompt`` is the conditioning text paired with the audio (the disentanglement hook).
    """
    return embed_batch(embedder, [wav], sr=sr, task_prompt=task_prompt, normalize=normalize)[0]


def embed_batch(embedder: LoadedEmbedder, wavs, *, sr: int = 16_000,
                task_prompt: str | None = None, normalize: bool = True, batch_size: int = 8):
    """Embed a list of 1-D waveforms. Returns an ``(N, embed_dim)`` float32 array.

    Audio is passed as document items ``{"audio": wav[, "text": task_prompt]}`` to the
    SentenceTransformer's ``encode_document`` (mirrors the model card's usage).
    """
    import numpy as np

    docs = []
    for wav in wavs:
        item: dict[str, Any] = {"audio": np.asarray(wav)}
        if task_prompt is not None:
            item["text"] = task_prompt
        docs.append(item)
    emb = embedder.model.encode_document(
        docs, batch_size=batch_size, convert_to_numpy=True, normalize_embeddings=normalize
    )
    return np.asarray(emb, dtype=np.float32)
