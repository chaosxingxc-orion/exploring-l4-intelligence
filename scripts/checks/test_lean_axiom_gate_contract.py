"""Guard for the wired Lean axiom gate (owner ruling 2026-07-29).

The gate itself runs in WSL (lake build + collectAxioms audit) and stamps a
receipt under docs/checks/lean-axiom-gate/. This Windows-side guard pins the
offline invariants: the gate script exists, its axiom whitelist is unchanged,
and the newest receipt agrees with the script's whitelist and reports PASS.
Re-run the WSL gate and re-stamp the receipt whenever proofs/tfrl changes.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "lean_axiom_gate.sh"
RECEIPT_DIR = REPO / "docs" / "checks" / "lean-axiom-gate"
WHITELIST = [
    "propext",
    "Classical.choice",
    "Quot.sound",
    "TfrlProofs.BestOfN.beirami_thm_3_1",
]


class LeanAxiomGateContractTests(unittest.TestCase):
    def newest_receipt(self) -> dict:
        candidates = sorted(RECEIPT_DIR.glob("*-axiom-gate.json"))
        self.assertTrue(candidates, f"no axiom-gate receipt under {RECEIPT_DIR}")
        return json.loads(candidates[-1].read_text(encoding="utf-8"))

    def test_gate_script_exists_with_pinned_whitelist(self) -> None:
        self.assertTrue(SCRIPT.is_file(), f"gate script missing: {SCRIPT}")
        text = SCRIPT.read_text(encoding="utf-8")
        for name in WHITELIST:
            self.assertIn(name, text)
        self.assertIn("collectAxioms", text)
        self.assertRegex(text, re.compile(r"AXIOM_GATE_(OK|FAIL)"))

    def test_newest_receipt_matches_script_and_passes(self) -> None:
        receipt = self.newest_receipt()
        self.assertEqual("lean-axiom-gate-receipt-v1", receipt["schema"])
        self.assertEqual(WHITELIST, receipt["whitelist"])
        self.assertEqual("PASS", receipt["verdict"])
        self.assertEqual(0, receipt["offenders"])
        self.assertGreater(receipt["declarations_checked"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
