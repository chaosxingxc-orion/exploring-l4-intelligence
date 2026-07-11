#!/usr/bin/env bash
# lean_axiom_gate.sh — machine-check the axiom footprint of the Lean library proofs/tfrl.
#
# It runs a `#print axioms`-style audit (via Lean.collectAxioms) over EVERY public declaration in the
# `TfrlProofs` namespace and FAILS (exit 1) if any of them transitively depends on an axiom outside the
# whitelist:
#     { propext, Classical.choice, Quot.sound, TfrlProofs.BestOfN.beirami_thm_3_1 }
# The first three are Lean's standard classical axioms; `beirami_thm_3_1` is the single named,
# cited imported axiom (Beirami et al. 2024, Thm 3.1) documented in TfrlProofs.lean. Any NEW axiom
# (or a stray `sorryAx`) sneaking into the library trips this gate.
#
# Run inside WSL2 Ubuntu-24.04 with the Lean toolchain (elan) available. Usage:
#     bash scripts/lean_axiom_gate.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TFRL_DIR="$REPO_ROOT/proofs/tfrl"
LAKE="${LAKE:-$HOME/.elan/bin/lake}"

AUDIT="$TFRL_DIR/_AxiomAudit.lean"
cat > "$AUDIT" <<'LEAN'
import TfrlProofs
open Lean Elab Command

run_cmd do
  let env ← getEnv
  let wl : List Name :=
    [``propext, ``Classical.choice, ``Quot.sound, ``TfrlProofs.BestOfN.beirami_thm_3_1]
  let mut names : Array Name := #[]
  for (n, _) in env.constants.toList do
    if (`TfrlProofs).isPrefixOf n && !n.isInternal then
      names := names.push n
  let mut offenders : Array (Name × Name) := #[]
  for n in names do
    let axs ← collectAxioms n
    for a in axs do
      if !wl.contains a then
        offenders := offenders.push (n, a)
  if offenders.isEmpty then
    logInfo m!"AXIOM_GATE_OK checked {names.size} TfrlProofs declarations; only whitelisted axioms present"
  else
    throwError m!"AXIOM_GATE_FAIL {offenders}"
LEAN

cleanup() { rm -f "$AUDIT" "${AUDIT%.lean}.olean" "${AUDIT%.lean}.ilean" 2>/dev/null || true; }
trap cleanup EXIT

cd "$TFRL_DIR"
echo "[axiom-gate] auditing TfrlProofs.* against whitelist {propext, Classical.choice, Quot.sound, beirami_thm_3_1} ..."
set +e
OUT="$("$LAKE" env lean "$AUDIT" 2>&1)"
RC=$?
set -e
echo "$OUT"
if [ "$RC" -eq 0 ] && echo "$OUT" | grep -q "AXIOM_GATE_OK"; then
  echo "[axiom-gate] PASS"
  exit 0
fi
echo "[axiom-gate] FAIL (lean rc=$RC)"
exit 1
