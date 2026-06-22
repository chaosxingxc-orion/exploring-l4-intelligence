#!/usr/bin/env bash
# Probe Hugging Face reachability + auth for the models/datasets this repo downloads.
# Read-only: confirms repos resolve before kicking off a large fetch. For ModelScope
# reachability use: bash projects/speech-mllm-training-free-rl/scripts/wave0_fetch.sh check
# Override the venv with SPEECHRL_VENV.
set +e
V="${SPEECHRL_VENV:-$HOME/.venvs/speechrl}"
echo "HOME=$HOME  whoami=$(whoami)"
echo "venv python: $([ -x "$V/bin/python" ] && "$V/bin/python" --version 2>&1 || echo MISSING)"
echo "hf script:    $([ -e "$V/bin/hf" ] && echo present || echo MISSING)"
echo "hfcli script: $([ -e "$V/bin/huggingface-cli" ] && echo present || echo MISSING)"
echo "curl:         $(command -v curl || echo MISSING)"
"$V/bin/python" - <<'PY'
from huggingface_hub import HfApi, __version__, get_token
print("hub:", __version__, " token_configured:", bool(get_token()))
api = HfApi()
items = [
 ("model","nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-NVFP4"),
 ("model","Qwen/Qwen3-Omni-30B-A3B-Instruct"),
 ("model","OpenMOSS/MOSS-Audio-8B"),
 ("model","openbmb/MiniCPM-o-4_5-gguf"),
 ("model","nvidia/omni-embed-nemotron-3b"),
 ("dataset","openslr/librispeech_asr"),
 ("dataset","AudioLLMs/MMAU-mini"),
 ("dataset","BoJack/MMAR"),
 ("dataset","declare-lab/MELD"),
 ("dataset","MahiA/CREMA-D"),
 ("dataset","PolyAI/minds14"),
 ("dataset","facebook/covost2"),
 ("dataset","google/fleurs"),
]
for kind, rid in items:
    try:
        info = api.model_info(rid) if kind == "model" else api.dataset_info(rid)
        print("OK    %-7s %-54s gated=%s" % (kind, rid, getattr(info, "gated", None)))
    except Exception as e:
        print("FAIL  %-7s %-54s %s" % (kind, rid, type(e).__name__))
PY
echo "[done]"
