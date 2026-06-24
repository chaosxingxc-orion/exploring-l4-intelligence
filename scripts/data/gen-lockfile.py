#!/usr/bin/env python3
"""Generator for docs/datasets.lock.json — the single download manifest.

Walks speechrl-data/{datasets,models,repos}, captures size + file count + source +
best-effort revision (HF commit sha from .hfd/repo_metadata.json, git HEAD for repos,
ModelScope 'master' tag otherwise) and writes the committed lockfile. The authoritative
downloadable source id per asset comes from SOURCE_OVERRIDE below.

Maintainer tool (run on a machine that has the data). Stdlib only (py3.12/3.14 OK).
Usage:  python scripts/data/gen-lockfile.py 2026-06-24 > docs/datasets.lock.json
"""
from __future__ import annotations
import json, os, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]    # scripts/data/gen-lockfile.py -> repo root
DR = Path(os.environ.get("SPEECHRL_DATA_DIR") or (REPO / "speechrl-data"))
DSETS = DR / "datasets"
MODELS = DR / "models"
REPOS = DR / "repos"
GEN_DATE = sys.argv[1] if len(sys.argv) > 1 else "unknown"

# name -> (factor_family, task, note). Drives grouping in the lockfile + docs.
DS_META = {
    "librispeech":        ("content", "asr",   "ASR; 100h+360h+960h"),
    "covost2":            ("content", "st",    "ST translations (audio via Common Voice)"),
    "fleurs-r":           ("content", "st",    "FLEURS-R restored speech; ST + language-ID"),
    "crema-d":            ("speaker+emotion", "ser", "first-proof substrate (speaker+emotion, same audio)"),
    "meld":               ("emotion", "ser",   "MELD raw + features"),
    "minds14":            ("lang+intent", "intent", "SLU intent, 14 langs"),
    "slurp":              ("lang+intent", "intent", "English SLU; audio at repos/slurp/scripts/audio"),
    "speech-massive":     ("lang+intent", "intent", "12-lang SLU intent+slot (eval-only NC)"),
    "mmau-mini":          ("audio-understanding", "audio", "audio understanding eval"),
    "mmar":               ("audio-reasoning", "audio", "audio reasoning eval"),
    "air-bench":          ("audio-benchmark", "audio", "AIR-Bench"),
    "mmsu":               ("audio-reasoning", "audio", "multi-skill spoken-reasoning MCQ"),
    "big-bench-audio":    ("audio-reasoning", "audio", "spoken reasoning, 1000 items"),
    "voicebench":         ("spoken-qa/agentic", "intent", "spoken-QA + agentic suite"),
    "heysquad":           ("spoken-qa", "intent", "extractive spoken-QA"),
    "spoken-squad":       ("spoken-qa", "intent", "ASR-noise-robust spoken QA"),
    "uro-bench":          ("spoken-dialogue", "intent", "EN+ZH spoken-dialogue agentic"),
    "vocalbench":         ("spoken-dialogue", "intent", "9-axis conversational eval"),
    "vocalbench-zh":      ("spoken-dialogue", "intent", "Mandarin spoken-interaction"),
    "voiceassistant-eval":("spoken-assistant", "intent", "13-cat assistant eval (roleplay/safety/S2S)"),
    "audiomc":            ("spoken-assistant", "intent", "multi-turn instruction retention"),
    "soulx-duplug":       ("spoken-dialogue", "intent", "full-duplex turn-taking EN+ZH (zips)"),
    "eva-bench":          ("spoken-agent", "intent", "voice-agent task+experience (airline); tiny by design"),
    "tau2-bench":         ("spoken-agent", "intent", "voice tool-use agent data"),
    "seed-tts-eval":      ("tts-eval", "asr", "Seed-TTS eval set"),
    "aime24":             ("text-reasoning-eval", "asr", "AIME 2024 math eval"),
    "aime25":             ("text-reasoning-eval", "asr", "AIME 2025 math eval"),
    "aime26":             ("text-reasoning-eval", "asr", "AIME 2026 math eval"),
}
# Authoritative downloadable source per asset (method, id) — harvested from the (now-retired) fetch
# scripts + registry/docs. Lets the unified downloader reproduce the set from the lockfile alone.
# method: hf (hf-mirror, pin --revision sha) | modelscope (tracks 'master') | modelscope-manual
# (optional evalscope set, id not recoverable -> downloader warns). SLURP is git + Zenodo (special).
SOURCE_OVERRIDE = {
    "librispeech": ("modelscope", "openslr/librispeech_asr"),
    "mmau-mini": ("hf", "TwinkStart/MMAU"),
    "mmar": ("hf", "BoJack/MMAR"),
    "meld": ("hf", "declare-lab/MELD"),
    "crema-d": ("hf", "MahiA/CREMA-D"),
    "minds14": ("hf", "PolyAI/minds14"),
    "covost2": ("hf", "facebook/covost2"),
    "fleurs-r": ("hf", "google/fleurs-r"),
    "air-bench": ("modelscope", "qfq/AIR-Bench_24.09"),
    "speech-massive": ("hf", "FBK-MT/Speech-MASSIVE"),
    "heysquad": ("hf", "yijingwu/HeySQuAD_human"),
    "mmsu": ("hf", "ddwang2000/MMSU"),
    "spoken-squad": ("hf", "AudioLLMs/spoken_squad_test"),
    "uro-bench": ("hf", "Honggao/URO-Bench"),
    "vocalbench": ("hf", "VocalNet/VocalBench"),
    "big-bench-audio": ("hf", "ArtificialAnalysis/big_bench_audio"),
    "voiceassistant-eval": ("hf", "MathLLMs/VoiceAssistant-Eval"),
    "vocalbench-zh": ("hf", "VocalNet/VocalBench-zh"),
    "audiomc": ("hf", "ScaleAI/audiomc"),
    "soulx-duplug": ("hf", "Soul-AILab/SoulX-Duplug-Eval"),
    "eva-bench": ("hf", "ServiceNow-AI/eva"),
    "voicebench": ("modelscope", "lmms-lab/voicebench"),
    "tau2-bench": ("modelscope", "evalscope/tau2-bench-data"),
    "seed-tts-eval": ("modelscope-manual", "evalscope (id not recorded; fetch manually)"),
    "aime24": ("modelscope-manual", "evalscope (id not recorded; fetch manually)"),
    "aime25": ("modelscope-manual", "evalscope (id not recorded; fetch manually)"),
    "aime26": ("modelscope-manual", "evalscope (id not recorded; fetch manually)"),
    # models (all fetched from ModelScope)
    "qwen3-omni-30b-a3b-instruct": ("modelscope", "Intel/Qwen3-Omni-30B-A3B-Instruct-int4-AutoRound"),
    "moss-audio-8b-instruct": ("modelscope", "openmoss/MOSS-Audio-8B-Instruct"),
    "nemotron3-nano-omni-nvfp4": ("modelscope", "nv-community/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-NVFP4"),
    "minicpm-o-4_5": ("modelscope", "OpenBMB/MiniCPM-o-4_5"),
    "omni-embed-nemotron-3b": ("modelscope", "nv-community/omni-embed-nemotron-3b"),
}

MODEL_META = {
    "qwen3-omni-30b-a3b-instruct": "INT4 generation backbone (W1)",
    "moss-audio-8b-instruct":      "generation comparator (W1)",
    "nemotron3-nano-omni-nvfp4":   "NVFP4 generation backbone (W1)",
    "minicpm-o-4_5":               "GGUF/raw generation comparator (W1)",
    "omni-embed-nemotron-3b":      "W4 flagship frozen omni-embedding backbone",
}

def run(cmd, timeout=180):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout).stdout.strip()
    except Exception:
        return ""

def human(nbytes: int) -> str:
    f = float(nbytes)
    for u in ("B", "K", "M", "G", "T"):
        if f < 1024 or u == "T":
            return f"{f:.0f}{u}" if u in ("B", "K") else f"{f:.1f}{u}"
        f /= 1024
    return f"{f:.1f}T"

def size_bytes(path: Path) -> int:
    out = run(["du", "-sb", path.as_posix()])
    try:
        return int(out.split()[0])
    except Exception:
        return 0

def count_files(path: Path) -> int:
    n = 0
    try:
        for _root, _dirs, files in os.walk(path):
            n += sum(1 for f in files if not f.startswith("."))
    except Exception:
        return 0
    return n

def hf_meta(d: Path):
    p = d / ".hfd" / "repo_metadata.json"
    if not p.exists():
        return None
    try:
        j = json.loads(p.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return None
    lic = (j.get("cardData") or {}).get("license")
    if not lic:
        lic = next((t.split("license:", 1)[1] for t in j.get("tags", []) if t.startswith("license:")), None)
    return {"hf_id": j.get("id"), "sha": j.get("sha"), "last_modified": j.get("lastModified"), "license": lic}

def detect(d: Path, data_path: Path | None = None):
    """Return (source, revision) for a dataset/model dir."""
    p = data_path or d
    if (d / ".git").exists():
        sha = run(["git", "-C", d.as_posix(), "rev-parse", "HEAD"])
        url = run(["git", "-C", d.as_posix(), "config", "--get", "remote.origin.url"])
        url = url.replace("https://ghfast.top/", "")  # strip CN proxy prefix
        return ({"kind": "git", "url": url}, sha or "unknown")
    m = hf_meta(d)
    if m and m.get("sha"):
        return ({"kind": "hf", "hf_id": m["hf_id"], "license": m.get("license"),
                 "last_modified": m.get("last_modified")}, m["sha"])
    if (d / ".msc").exists() or (d / ".mv").exists():
        return ({"kind": "modelscope"}, "master (modelscope; unpinned -- content-fingerprinted)")
    return ({"kind": "unknown"}, "unknown (no local metadata -- content-fingerprinted)")

def entry(name: str, d: Path, kind: str, meta_note: str, family: str, task: str,
          status: str, data_path: Path | None = None, extra: dict | None = None):
    p = data_path or d
    nbytes = size_bytes(p)
    src, rev = detect(d, data_path)
    if name in SOURCE_OVERRIDE:  # authoritative downloadable id for the unified fetcher
        method, sid = SOURCE_OVERRIDE[name]
        src = dict(src); src["kind"] = method; src["id"] = sid
    e = {
        "name": name, "kind": kind, "local_subdir": p.relative_to(DR).as_posix(),
        "source": src, "revision": rev, "status": status,
        "size_h": human(nbytes), "size_bytes": nbytes, "files": count_files(p),
        "task": task, "factor_family": family, "note": meta_note,
    }
    if extra:
        e.update(extra)
    return e

def main():
    datasets, models, refs = [], [], []
    total = 0

    for name, (family, task, note) in DS_META.items():
        if name == "slurp":
            d = REPOS / "slurp"
            data_path = REPOS / "slurp" / "scripts" / "audio"
            e = entry(name, d, "dataset", note, family, task, "COMPLETE", data_path=data_path,
                      extra={"audio_zenodo_record": "4274930",
                             "transcripts": "repos/slurp/dataset (git)",
                             "datasets_symlink": "datasets/slurp -> repos/slurp/scripts/audio (create on setup)"})
        else:
            d = DSETS / name
            if not d.exists():
                continue
            e = entry(name, d, "dataset", note, family, task, "COMPLETE")
        datasets.append(e); total += e["size_bytes"]

    for name, note in MODEL_META.items():
        d = MODELS / name
        if not d.exists():
            continue
        e = entry(name, d, "model", note, "model", "-", "COMPLETE")
        models.append(e); total += e["size_bytes"]
    # broken symlink note
    gguf = MODELS / "minicpm-o-4_5-gguf"
    if gguf.is_symlink() and not gguf.exists():
        models.append({"name": "minicpm-o-4_5-gguf", "kind": "model", "status": "BROKEN_SYMLINK",
                       "note": f"dangling symlink -> {os.readlink(gguf)}; use minicpm-o-4_5 instead"})

    for r in ["slurp", "mbr-for-asr", "AudioGenie-Reasoner", "TTRL", "TPO", "JitRL", "slue-toolkit"]:
        d = REPOS / r
        if not (d / ".git").exists():
            continue
        src, rev = detect(d)
        refs.append({"name": r, "kind": "ref-repo", "local_subdir": f"repos/{r}",
                     "source": src, "revision": rev})

    doc = {
        "_comment": "FROZEN dataset/model lock for speechrl-data. Re-generate with "
                    "scripts/data/gen-lockfile.py. Datasets are not in git; this records the "
                    "exact local snapshot. SHA-pinned where metadata exists; ModelScope/unknown "
                    "entries are content-fingerprinted (size_bytes + files). See docs/data.md.",
        "frozen": True,
        "generated": GEN_DATE,
        "data_root": "${SPEECHRL_DATA_DIR:-<repo>/speechrl-data}",
        "totals": {"locked_datasets": sum(1 for e in datasets if e["status"] == "COMPLETE"),
                   "models": sum(1 for e in models if e.get("status") == "COMPLETE"),
                   "total_bytes": total, "total_h": human(total)},
        "datasets": datasets, "models": models, "ref_repos": refs,
    }
    json.dump(doc, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")

if __name__ == "__main__":
    main()
