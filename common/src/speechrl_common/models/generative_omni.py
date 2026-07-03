"""Generative omni loader + candidate sampler — the GPU side of Operator-B best-of-N.

Generation lives here (GPU, heavy); the pure *selection* over the produced candidates lives in
``speechrl_common.rl.decode`` (best_of_n / mbr / soft_bon). Keeping them split mirrors the Lean
split: decode.py is the discrete object the proofs reason about; this module just feeds it samples.

Heavy imports (torch/transformers) are inside the functions, per the package's lazy-import discipline,
so ``import speechrl_common`` stays light. Targets the latest open-source omni models (Qwen3-Omni etc.).
"""
from __future__ import annotations

from typing import Any


def load_generative_omni(model_path: str, *, device: str = "cuda", dtype: str = "auto") -> tuple[Any, Any]:
    """Load a (model, processor) pair for a generative omni model on GPU.

    Defaults target Qwen3-Omni (``Qwen3OmniMoeForConditionalGeneration``); the processor is loaded via
    ``AutoProcessor`` so sibling omni checkpoints resolve their own processor class.
    """
    import torch  # noqa: F401  (ensures CUDA context / clear error if missing)
    from transformers import AutoProcessor

    try:
        from transformers import Qwen3OmniMoeForConditionalGeneration as _Model
    except Exception:  # pragma: no cover - fallback for sibling omni families
        from transformers import AutoModelForCausalLM as _Model

    processor = AutoProcessor.from_pretrained(model_path, trust_remote_code=True)
    model = _Model.from_pretrained(
        model_path, dtype=dtype, device_map=device, trust_remote_code=True
    ).eval()
    return model, processor


def _build_inputs(processor: Any, audio_path: str, instruction: str, device: str) -> dict:
    conversation = [{
        "role": "user",
        "content": [
            {"type": "audio", "audio": audio_path},
            {"type": "text", "text": instruction},
        ],
    }]
    inputs = processor.apply_chat_template(
        conversation, add_generation_prompt=True, tokenize=True,
        return_dict=True, return_tensors="pt",
    )
    return {k: (v.to(device) if hasattr(v, "to") else v) for k, v in inputs.items()}


def generate_candidates(model: Any, processor: Any, audio_path: str, instruction: str, *,
                        n: int = 8, temperature: float = 0.7, top_p: float = 0.9,
                        max_new_tokens: int = 200, device: str = "cuda", seed: int = 42,
                        greedy: bool = False) -> list[str]:
    """Produce a candidate pool of decoded transcripts for one audio clip.

    ``greedy=True`` returns the single deterministic decode (the best-of-N N=1 baseline); otherwise
    ``n`` temperature-sampled candidates (one ``generate`` call with ``num_return_sequences=n``).
    """
    import torch

    inputs = _build_inputs(processor, audio_path, instruction, device)
    # Cast floating-point inputs (e.g. audio input_features) to the model's dtype; leave int ids/masks.
    try:
        mdtype = next(model.parameters()).dtype
    except StopIteration:  # pragma: no cover
        mdtype = torch.bfloat16
    inputs = {k: (v.to(mdtype) if (torch.is_tensor(v) and torch.is_floating_point(v)) else v)
              for k, v in inputs.items()}
    n_in = inputs["input_ids"].shape[1]
    gen: dict[str, Any] = {"max_new_tokens": max_new_tokens, "return_audio": False}
    if greedy:
        gen.update(do_sample=False, num_return_sequences=1)
    else:
        torch.manual_seed(seed)
        gen.update(do_sample=True, temperature=temperature, top_p=top_p, num_return_sequences=n)
    with torch.no_grad():
        try:
            out = model.generate(**inputs, **gen)
        except TypeError:
            gen.pop("return_audio", None)
            out = model.generate(**inputs, **gen)
    seqs = out.sequences if hasattr(out, "sequences") else out
    return [
        processor.batch_decode(seqs[i:i + 1, n_in:], skip_special_tokens=True)[0].strip()
        for i in range(seqs.shape[0])
    ]
