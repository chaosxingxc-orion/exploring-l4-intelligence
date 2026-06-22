#!/usr/bin/env bash
# Wave0 catch-up: fix the targets that failed in the first run.
# Strategy per dataset (all CN-friendly mirrors verified 2026-06-15):
#   meld           hf-mirror declare-lab/MELD   then recursively extract nested tars
#   minds14        hf-mirror PolyAI/minds14     parquet-format, no loader needed
#   minds14_xs     hf-mirror google/xtreme_s    loader-style; will skip on datasets>=3.0
#   covost2        hf-mirror facebook/covost2   loader script + AI-ModelScope CV4
#   air-bench      ModelScope evalscope/AIR-Bench (49.38GB; replaces broken qfq/...)
#   voxceleb       MARK MANUAL (gated; needs HF token or OpenDataLab account)
#   slurp_audio    Try Zenodo direct; if blocked, fall through to manual note
set -uo pipefail

WORKSPACE='/mnt/d/chao_workspace/exploring-l4-intelligence'
DR="$WORKSPACE/speechrl-data"
DS="$DR/datasets"
LOG="$DR/wave0_catchup.log"

# Activate venv & set environment for readable output + CN mirrors
source /root/.venvs/speechrl/bin/activate
export PATH="/root/.venvs/speechrl/bin:$PATH"
export LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONIOENCODING=utf-8
export TQDM_ASCII=1 NO_COLOR=1 CLICOLOR=0 TERM=dumb
export HF_ENDPOINT=https://hf-mirror.com
export HF_HUB_DOWNLOAD_TIMEOUT=60

stamp() { date '+%Y-%m-%d %H:%M:%S'; }
section() { echo; echo "================================================================"; echo "==  $* @ $(stamp)"; echo "================================================================"; }

mkdir -p "$DS"

# ----------------------------------------------------------------------------
section "MELD: complete via hf-mirror + recursive extract"
MELD="$DS/meld"
mkdir -p "$MELD"
# Download (resumes if partial). New `hf` CLI; --type dataset is the v1.x form.
hf download declare-lab/MELD --type dataset --local-dir "$MELD" \
  || echo "[meld] WARN: hf download returned non-zero; checking files"

# Recursively extract nested tarballs: MELD.Raw.tar.gz contains train/dev/test tar.gz inside
extract_once() {
  local archive="$1" outdir="$2"
  local marker="$archive.extracted"
  if [ -f "$archive" ] && [ ! -f "$marker" ]; then
    echo "[meld] extracting $(basename "$archive") -> $(basename "$outdir")"
    mkdir -p "$outdir"
    tar xzf "$archive" -C "$outdir" && touch "$marker"
  fi
}
extract_once "$MELD/MELD.Raw.tar.gz" "$MELD"
[ -d "$MELD/MELD.Raw" ] && {
  extract_once "$MELD/MELD.Raw/train.tar.gz" "$MELD/MELD.Raw"
  extract_once "$MELD/MELD.Raw/dev.tar.gz"   "$MELD/MELD.Raw"
  extract_once "$MELD/MELD.Raw/test.tar.gz"  "$MELD/MELD.Raw"
}
extract_once "$MELD/MELD.Features.Models.tar.gz" "$MELD"
echo "[meld] final size: $(du -sh "$MELD" 2>/dev/null | awk '{print $1}')"

# ----------------------------------------------------------------------------
section "MINDS-14: hf-mirror PolyAI/minds14 (parquet)"
MINDS="$DS/minds14"
mkdir -p "$MINDS"
hf download PolyAI/minds14 --type dataset --local-dir "$MINDS" \
  || echo "[minds14] WARN: download returned non-zero"
echo "[minds14] final size: $(du -sh "$MINDS" 2>/dev/null | awk '{print $1}')"

# ----------------------------------------------------------------------------
section "MINDS-14 xtreme_s: try google/xtreme_s; soft-fail on loader-script datasets"
XTS="$DS/minds14-xtreme_s"
mkdir -p "$XTS"
hf download google/xtreme_s --type dataset --local-dir "$XTS" \
  || echo "[xtreme_s] NOTE: loader-style; PolyAI/minds14 above is the parquet replacement"
echo "[xtreme_s] final size: $(du -sh "$XTS" 2>/dev/null | awk '{print $1}')"

# ----------------------------------------------------------------------------
section "CoVoST2: pull loader + tsv archives (CV4 audio is huge; defer)"
CV2="$DS/covost2"
mkdir -p "$CV2"
# Loader script + tsv files
hf download facebook/covost2 --type dataset --local-dir "$CV2" \
  || echo "[covost2] WARN: loader download failed"
# Pull tsv tarballs from upstream dl.fbaipublicfiles
TSV_DIR="$CV2/tsv"
mkdir -p "$TSV_DIR"
COVOST_TSVS=(
  "covost_v2.en_de.tsv.tar.gz"
  "covost_v2.en_zh-CN.tsv.tar.gz"
  "covost_v2.zh-CN_en.tsv.tar.gz"
  "covost_v2.fr_en.tsv.tar.gz"
  "covost_v2.de_en.tsv.tar.gz"
  "covost_v2.es_en.tsv.tar.gz"
)
for tgz in "${COVOST_TSVS[@]}"; do
  out="$TSV_DIR/$tgz"
  if [ ! -f "$out" ]; then
    echo "[covost2] aria2c $tgz"
    aria2c -x 8 -s 8 -c -d "$TSV_DIR" -o "$tgz" \
      "https://dl.fbaipublicfiles.com/covost/${tgz}" \
      --console-log-level=warn --summary-interval=0 2>&1 | tail -3 \
      || echo "[covost2] WARN: $tgz failed (CN may need proxy)"
  fi
  [ -f "$out" ] && tar xzf "$out" -C "$TSV_DIR" 2>/dev/null
done
echo "[covost2] downloaded tsvs: $(ls "$TSV_DIR" 2>/dev/null | wc -l)"
echo "[covost2] NOTE: full audio = Common Voice v4 mp3 (~50GB/lang). Skipped here;"
echo "[covost2] run separately when needed: modelscope download --dataset AI-ModelScope/common_voice_4_0"
echo "[covost2] final size: $(du -sh "$CV2" 2>/dev/null | awk '{print $1}')"

# ----------------------------------------------------------------------------
section "AIR-Bench: ModelScope evalscope/AIR-Bench (replaces broken qfq/...)"
AB="$DS/air-bench"
mkdir -p "$AB"
modelscope download --dataset evalscope/AIR-Bench --local_dir "$AB" --max-workers 16 \
  || echo "[air-bench] WARN: ModelScope download returned non-zero"
echo "[air-bench] final size: $(du -sh "$AB" 2>/dev/null | awk '{print $1}')"

# ----------------------------------------------------------------------------
section "SLURP audio: try Zenodo with longer timeout / IPv4 only"
SLURP_AUDIO="$DR/repos/slurp/audio"
mkdir -p "$SLURP_AUDIO"
SLURP_URLS=(
  "https://zenodo.org/record/4274930/files/slurp_real.tar.gz"
  "https://zenodo.org/record/4274930/files/slurp_synth.tar.gz"
)
for url in "${SLURP_URLS[@]}"; do
  fname=$(basename "$url")
  out="$SLURP_AUDIO/$fname"
  marker="$out.extracted"
  if [ -f "$marker" ]; then
    echo "[slurp] $fname already extracted, skip"
    continue
  fi
  if [ ! -f "$out" ] || [ -f "$out.aria2" ]; then
    echo "[slurp] aria2c $fname (IPv4 only, 60s connect timeout)"
    aria2c -4 -x 4 -s 4 -c --connect-timeout=60 --timeout=120 \
      -d "$SLURP_AUDIO" -o "$fname" "$url" \
      --console-log-level=warn --summary-interval=30 2>&1 | tail -8 \
      || echo "[slurp] WARN: $fname failed (CN often blocks Zenodo; need proxy)"
  fi
  if [ -f "$out" ] && [ ! -f "$marker" ]; then
    echo "[slurp] extracting $fname"
    tar xzf "$out" -C "$SLURP_AUDIO" && touch "$marker"
  fi
done
echo "[slurp] audio dir size: $(du -sh "$SLURP_AUDIO" 2>/dev/null | awk '{print $1}')"

# ----------------------------------------------------------------------------
section "VoxCeleb: gated, recording manual instructions"
VC="$DS/voxceleb"
mkdir -p "$VC"
cat > "$VC/HOW_TO_DOWNLOAD.txt" <<'HOWTO'
VoxCeleb is gated. Three CN-friendly options:

(A) OpenDataLab (recommended for CN):
    Register at https://opendatalab.com -> approve VoxCeleb1/2 ->
    install opendatalab CLI:  pip install opendatalab
    opendatalab login
    opendatalab get OpenDataLab/VoxCeleb1 -d /mnt/d/.../speechrl-data/datasets/voxceleb/vox1
    opendatalab get OpenDataLab/VoxCeleb2 -d /mnt/d/.../speechrl-data/datasets/voxceleb/vox2

(B) HuggingFace token + ProgramComputer/voxceleb (gated):
    1. Register https://huggingface.co/ and accept dataset terms
    2. huggingface-cli login --token YOUR_HF_TOKEN
    3. HF_ENDPOINT=https://hf-mirror.com huggingface-cli download \
         ProgramComputer/voxceleb --repo-type dataset \
         --local-dir <here>
    4. cat vox1_dev_wav_part?? > vox1_dev_wav.zip && unzip vox1_dev_wav.zip

(C) Oxford VGG official:
    https://www.robots.ox.ac.uk/~vgg/data/voxceleb/ (form-gated, slow CN)
HOWTO
echo "[voxceleb] manual instructions written to $VC/HOW_TO_DOWNLOAD.txt"

# ----------------------------------------------------------------------------
section "DONE"
echo "Catch-up finished at $(stamp). Inventory follows."
bash /root/inventory.sh
