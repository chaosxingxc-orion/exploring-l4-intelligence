# Diffusion-ASR candidate model lock proposal

**Status:** metadata proposal only; not promoted to `docs/datasets.lock.json`. No model artifact was
downloaded or loaded. Acquisition requires an explicit owner decision after size/license/checkpoint
provenance review.

| Role | Source | Proposed revision | Local status |
|---|---|---|---|
| speech encoder | `https://huggingface.co/openai/whisper-large-v3` | `06f233fe06e710322aca913c1bc4249a0d71fce1` | absent from the three locked model directories |
| diffusion LLM | `https://huggingface.co/GSAI-ML/LLaDA-8B-Instruct` | `08b83a6feb34df1a6011b80c3c00c7563e963b07` | absent from the three locked model directories |
| trained bridge/LoRA checkpoint | `https://drive.google.com/file/d/1btAsCXTHQApnRcl_k5Wfn0zSD08yXHZh/view` | upstream link at repository commit `18c8263d4c01c519931240d8e613a5413551c5cb` | absent; immutable revision/hash unresolved |

The two Hugging Face model pages are public and ungated at metadata-check time. Their proposed
revisions are the repository heads returned by the official model API on 2026-07-22; they are not
claims that upstream will retain those heads indefinitely. Whisper large-v3 declares Apache-2.0;
LLaDA-8B-Instruct declares MIT. The paper checkpoint is linked from the Apache-2.0 code repository,
but the checkpoint's own byte hash, size, redistribution terms, and durable revision are not stated.

## Promotion gate

Before adding these rows to the canonical lock or writing an executable fetch recipe:

1. freeze the exact file allowlist and total bytes for both Hugging Face revisions;
2. resolve the Google Drive checkpoint's size, SHA-256, and artifact-specific license/provenance;
3. estimate combined CPU RAM, VRAM, and disk requirements against the RTX 5090 Laptop environment;
4. choose an isolated Python-3.10 environment path outside `~/.venvs/speechrl`;
5. make the fetch script default to `--list`/dry-run, write only under `SPEECHRL_DATA_DIR`, verify all
   promoted hashes, and keep weights/receipts external to Git;
6. require a separate decision before download, install, model load, smoke, or metric execution.

Failure of any gate keeps the first reproduction card in `MODEL_ASSET_BLOCKED` state; it does not
justify substituting one of the locally locked omni models and claiming paper reproduction.
