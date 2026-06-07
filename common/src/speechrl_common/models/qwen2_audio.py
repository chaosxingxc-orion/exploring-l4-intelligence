"""Thin loader for Qwen2-Audio (a common speech-multimodal-LLM base for W1/W2).

Kept dependency-free at import time; transformers/torch are imported on call.
Swap or extend with SALMONN / Qwen2.5-Omni loaders alongside this module.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

DEFAULT_MODEL_ID = "Qwen/Qwen2-Audio-7B-Instruct"


@dataclass
class LoadedModel:
    model: Any
    processor: Any
    model_id: str


def load_qwen2_audio(
    model_id: str = DEFAULT_MODEL_ID,
    *,
    device_map: str | None = "auto",
    torch_dtype: str = "bfloat16",
    attn_implementation: str | None = "flash_attention_2",
) -> LoadedModel:
    """Load Qwen2-Audio model + processor.

    Args:
        model_id: HF hub id or local path.
        device_map: passed to from_pretrained ("auto" shards across the GPU).
        torch_dtype: "bfloat16" / "float16" / "float32".
        attn_implementation: "flash_attention_2" (needs flash-attn) or None/"sdpa".
    """
    import torch
    from transformers import AutoProcessor, Qwen2AudioForConditionalGeneration

    dtype = getattr(torch, torch_dtype)
    processor = AutoProcessor.from_pretrained(model_id)
    model = Qwen2AudioForConditionalGeneration.from_pretrained(
        model_id,
        device_map=device_map,
        torch_dtype=dtype,
        attn_implementation=attn_implementation,
    )
    return LoadedModel(model=model, processor=processor, model_id=model_id)
