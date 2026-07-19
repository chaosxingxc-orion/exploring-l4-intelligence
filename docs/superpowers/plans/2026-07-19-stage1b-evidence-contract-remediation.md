# Stage-1B Evidence Contract Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the remaining review-named evidence false-greens with a generic schema-v3 contract and produce independent Windows/WSL evidence without changing research derivations or occupancy.

**Architecture:** Keep taxonomy-v5 derivation semantics frozen, but place the active evidence data under `wiki/survey/current/data/schema-v3/`. A small reusable evidence module validates structure-independent field bindings and discriminative page anchors; a v6 contract harness composes it with the existing derivation and source-resolution logic. Old v5 reports and registered reviewer artifacts remain unchanged.

**Tech Stack:** Python 3.12/3.14 standard library, `pypdf` loaded lazily, JSON sidecars, `unittest`, existing survey generators and Git-blob audit discipline.

**Design spec:** `docs/superpowers/specs/2026-07-19-stage1b-readiness-and-context-consolidation-design.md`

---

## File map

**Create**

- `scripts/survey/sf_evidence_contract.py` — pure row/signal/edge binding and PDF-anchor checks.
- `scripts/survey/test_sf_evidence_contract.py` — focused TDD characterization and unit tests.
- `scripts/survey/sf_schema_v3_migrate.py` — deterministic migration from schema-v2 sidecars.
- `scripts/survey/sf_identity_taxonomy_v6_test.py` — integration, mutation, occupancy, and report harness.
- `wiki/survey/current/data/identity-taxonomy-v6.json` — v5 derivations plus the schema-v3 contract declaration.
- `wiki/survey/current/data/schema-v3/sidecars/*.sidecar.json` — active evidence-bound sidecars.
- `wiki/survey/current/data/known-item-coding-v7.json` — generated projection.
- `wiki/survey/current/data/schema-v3-adjudication.json` — non-implementer binding-delta adjudication.
- `docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test.json` — latest local report.
- `docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test.nt.json` — Windows snapshot.
- `docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test.posix.json` — WSL snapshot.

**Modify**

- `scripts/survey/sf_coding_generator.py` — accept explicit source/output/taxonomy metadata.
- `scripts/survey/sf_dual_platform_check.py` — accept an evidence-report base path.

**Do not modify**

- `wiki/2026-07-19-system-first-research-proposal-v10-consolidated.md`
- `wiki/survey/2026-07-19-gate-s1-v9-response.md`
- `wiki/survey/2026-07-19-sf-protocol-amendment-15.md`
- `docs/checks/2026-07-19-sf-identity-taxonomy-v5-test*.json`

---

### Task 1: Add failing anchor-policy tests

**Files:**

- Create: `scripts/survey/test_sf_evidence_contract.py`
- Create later: `scripts/survey/sf_evidence_contract.py`

- [ ] **Step 1: Add the initial failing tests**

Use `apply_patch` to create this test module:

```python
#!/usr/bin/env python3
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from sf_evidence_contract import check_page_locator  # noqa: E402


class FakePage:
    def __init__(self, text):
        self._text = text

    def extract_text(self):
        return self._text


class FakeReader:
    def __init__(self, *pages):
        self.pages = [FakePage(p) for p in pages]


class AnchorPolicyTest(unittest.TestCase):
    def setUp(self):
        self.reader = FakeReader(
            "the method introduction",
            "the orchestrator decides every explore and stop action in context",
            "the appendix repeats common words but not the claim-bearing phrase",
        )

    def failures(self, locator):
        out = []
        check_page_locator(locator, self.reader, "fx#row", "row-locator", out)
        return out

    def test_bare_page_fails(self):
        self.assertTrue(any("page-token-without-anchor" in x
                            for x in self.failures("p1")))

    def test_single_generic_token_fails(self):
        self.assertTrue(any("page-anchor-too-weak" in x
                            for x in self.failures("p1 anchor='the'")))

    def test_frequent_phrase_fails(self):
        reader = FakeReader(
            "common method description",
            "common method description",
            "common method description",
            "common method description",
        )
        out = []
        check_page_locator(
            "p2 anchor='common method description'",
            reader,
            "fx#row",
            "row-locator",
            out,
        )
        self.assertTrue(any("page-anchor-not-discriminative" in x for x in out))

    def test_claim_bearing_phrase_passes(self):
        self.assertEqual([], self.failures(
            "p2 anchor='decides every explore and stop action'"))

    def test_missing_phrase_fails(self):
        self.assertTrue(any("page-anchor-missing" in x for x in self.failures(
            "p2 anchor='candidate majority controls termination'")))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and verify it fails for the missing module**

Run:

```powershell
python scripts/survey/test_sf_evidence_contract.py
```

Expected: non-zero exit with `ModuleNotFoundError: No module named 'sf_evidence_contract'`.

- [ ] **Step 3: Commit the red test**

```powershell
git add scripts/survey/test_sf_evidence_contract.py
git commit -m "test(survey): characterize strong page anchors"
```

---

### Task 2: Implement the discriminative PDF-anchor contract

**Files:**

- Create: `scripts/survey/sf_evidence_contract.py`
- Test: `scripts/survey/test_sf_evidence_contract.py`

- [ ] **Step 1: Implement normalization, parsing, and failure codes**

Create the module with these public functions and constants:

```python
#!/usr/bin/env python3
"""Schema-v3 evidence checks shared by the system-first survey tools."""
from __future__ import annotations

import re
import unicodedata
from collections import Counter

PAGE_NUMBER_RE = re.compile(r"\bp(?P<page>\d+)\b")
STRONG_PAGE_RE = re.compile(
    r"\bp(?P<page>\d+)\s+anchor='(?P<anchor>[^']+)'"
)
EVIDENCE_KINDS = {"canon", "tex", "pdf_page", "absence"}

ROW_REQUIRED_FIELDS = [
    "core_weight_update",
    "external_component_weight_update",
    "controller_program_or_config_optimized_on_labels",
    "human_or_dev_label_model_selection",
    "deployment_label_access",
    "test_item_gold_access",
    "inference_external_new_information",
    "internal_visibility",
    "core_topology",
    "core_native_modality",
    "control_horizon",
    "decision_rights",
    "candidate_pool_exists",
    "selection_policy",
    "selection_object",
    "explicit_candidate_pool_selection",
]
SIGNAL_REQUIRED_FIELDS = ["form", "source", "lifecycle", "uses"]
EDGE_REQUIRED_FIELDS = ["signal_use", "decision_right"]


def normalized_tokens(text):
    folded = unicodedata.normalize("NFKC", text or "").casefold()
    return re.findall(r"[^\W_]+", folded, flags=re.UNICODE)


def normalized_phrase(text):
    return " ".join(normalized_tokens(text))


def _anchor_strength_failure(anchor):
    tokens = normalized_tokens(anchor)
    chars = sum(len(t) for t in tokens)
    if len(tokens) < 2 or chars < 12:
        return "page-anchor-too-weak"
    return None


def _page_text(reader, index):
    try:
        return normalized_phrase(reader.pages[index].extract_text() or "")
    except Exception:
        return ""


def check_page_locator(locator, reader, pid, what, failures):
    locator = locator or ""
    strong = {m.start(): m for m in STRONG_PAGE_RE.finditer(locator)}
    for ref in PAGE_NUMBER_RE.finditer(locator):
        match = strong.get(ref.start())
        page = int(ref.group("page"))
        if match is None:
            failures.append(f"{pid}:{what}:page-token-without-anchor:p{page}")
            continue
        anchor = match.group("anchor")
        weakness = _anchor_strength_failure(anchor)
        if weakness:
            failures.append(f"{pid}:{what}:{weakness}:p{page}:{anchor}")
            continue
        if reader is None:
            failures.append(f"{pid}:{what}:pdf-unreadable-for-page-check")
            continue
        if not 1 <= page <= len(reader.pages):
            failures.append(
                f"{pid}:{what}:page-out-of-range:p{page}/{len(reader.pages)}"
            )
            continue
        needle = normalized_phrase(anchor)
        document = [_page_text(reader, i) for i in range(len(reader.pages))]
        total = sum(text.count(needle) for text in document)
        if total > 3:
            failures.append(
                f"{pid}:{what}:page-anchor-not-discriminative:p{page}:{anchor}:{total}"
            )
            continue
        window = document[max(0, page - 2):min(len(document), page + 1)]
        if not any(needle in text for text in window):
            failures.append(f"{pid}:{what}:page-anchor-missing:p{page}:{anchor}")


def values_equal(expected, declared):
    if isinstance(expected, list) and isinstance(declared, list):
        return Counter(expected) == Counter(declared)
    return expected == declared
```

Keep `pypdf` out of module-level imports; callers continue to construct readers lazily.

- [ ] **Step 2: Run the anchor tests**

```powershell
python scripts/survey/test_sf_evidence_contract.py
```

Expected: `Ran 5 tests` and `OK`.

- [ ] **Step 3: Commit the anchor implementation**

```powershell
git add scripts/survey/sf_evidence_contract.py scripts/survey/test_sf_evidence_contract.py
git commit -m "feat(survey): require discriminative page anchors"
```

---

### Task 3: Add failing row/signal/edge binding tests

**Files:**

- Modify: `scripts/survey/test_sf_evidence_contract.py`
- Modify later: `scripts/survey/sf_evidence_contract.py`

- [ ] **Step 1: Add a generic twelfth-row fixture and mutations**

Append this test class:

```python
from copy import deepcopy

from sf_evidence_contract import validate_bound_values


def binding(value):
    return {"kind": "canon", "value": value, "quote": "claim bearing quote"}


def generic_row():
    row = {
        "method_path_id": "__fx12__#path",
        "core_weight_update": False,
        "external_component_weight_update": False,
        "controller_program_or_config_optimized_on_labels": False,
        "human_or_dev_label_model_selection": False,
        "deployment_label_access": False,
        "test_item_gold_access": False,
        "inference_external_new_information": False,
        "internal_visibility": "api_only",
        "core_topology": "single_core",
        "core_native_modality": "omni_native",
        "control_horizon": "sequential",
        "decision_rights": ["branch"],
        "candidate_pool_exists": True,
        "selection_policy": "scored_select",
        "selection_object": "candidate_output",
        "explicit_candidate_pool_selection": True,
        "signals": [{
            "signal_id": "s1",
            "form": "scalar_score",
            "source": "llm_judge",
            "lifecycle": "online_step",
            "uses": ["prune"],
            "claim_evidence": {},
        }],
        "control_edges": [{
            "signal_id": "s1",
            "signal_use": "prune",
            "decision_right": "branch",
            "claim_evidence": {},
        }],
        "claim_evidence": {},
    }
    row["claim_evidence"] = {k: binding(row[k]) for k in (
        "core_weight_update", "external_component_weight_update",
        "controller_program_or_config_optimized_on_labels",
        "human_or_dev_label_model_selection", "deployment_label_access",
        "test_item_gold_access", "inference_external_new_information",
        "internal_visibility", "core_topology", "core_native_modality",
        "control_horizon", "decision_rights", "candidate_pool_exists",
        "selection_policy", "selection_object",
        "explicit_candidate_pool_selection",
    )}
    signal = row["signals"][0]
    signal["claim_evidence"] = {
        k: binding(signal[k]) for k in ("form", "source", "lifecycle", "uses")
    }
    edge = row["control_edges"][0]
    edge["claim_evidence"] = {
        k: binding(edge[k]) for k in ("signal_use", "decision_right")
    }
    return row


class BoundValueTest(unittest.TestCase):
    def failures(self, row):
        return validate_bound_values(row)

    def test_complete_generic_row_passes(self):
        self.assertEqual([], self.failures(generic_row()))

    def test_signal_source_flip_fails(self):
        row = generic_row()
        row["signals"][0]["source"] = "learned_rm_prm"
        self.assertTrue(any("signal:s1:source:evidence-value-mismatch" in x
                            for x in self.failures(row)))

    def test_coherent_edge_use_flip_still_needs_matching_evidence(self):
        row = generic_row()
        row["signals"][0]["uses"] = ["select"]
        row["signals"][0]["claim_evidence"]["uses"]["value"] = ["select"]
        row["control_edges"][0]["signal_use"] = "select"
        self.assertTrue(any("edge:0:signal_use:evidence-value-mismatch" in x
                            for x in self.failures(row)))

    def test_edge_right_flip_fails(self):
        row = generic_row()
        row["control_edges"][0]["decision_right"] = "supply"
        self.assertTrue(any("edge:0:decision_right:evidence-value-mismatch" in x
                            for x in self.failures(row)))

    def test_selection_object_flip_fails(self):
        row = generic_row()
        row["selection_object"] = "trajectory"
        self.assertTrue(any("row:selection_object:evidence-value-mismatch" in x
                            for x in self.failures(row)))

    def test_explicit_selection_flip_fails(self):
        row = generic_row()
        row["explicit_candidate_pool_selection"] = False
        self.assertTrue(any(
            "row:explicit_candidate_pool_selection:evidence-value-mismatch" in x
            for x in self.failures(row)))

    def test_missing_edge_binding_fails(self):
        row = generic_row()
        del row["control_edges"][0]["claim_evidence"]["decision_right"]
        self.assertTrue(any("edge:0:decision_right:required-evidence-missing" in x
                            for x in self.failures(row)))
```

- [ ] **Step 2: Run the tests and verify the missing function fails**

```powershell
python scripts/survey/test_sf_evidence_contract.py
```

Expected: non-zero exit with `ImportError` for `validate_bound_values`.

- [ ] **Step 3: Commit the red binding tests**

```powershell
git add scripts/survey/test_sf_evidence_contract.py
git commit -m "test(survey): specify complete evidence bindings"
```

---

### Task 4: Implement generic bound-value validation

**Files:**

- Modify: `scripts/survey/sf_evidence_contract.py`
- Test: `scripts/survey/test_sf_evidence_contract.py`

- [ ] **Step 1: Add reusable binding validation**

Append:

```python
def _validate_binding(owner, field, expected, evidence, failures):
    entry = (evidence or {}).get(field)
    if entry is None:
        failures.append(f"{owner}:{field}:required-evidence-missing")
        return
    if entry.get("kind") not in EVIDENCE_KINDS:
        failures.append(f"{owner}:{field}:evidence-kind-invalid")
    if not values_equal(expected, entry.get("value")):
        failures.append(f"{owner}:{field}:evidence-value-mismatch")


def validate_bound_values(row):
    pid = row.get("method_path_id", "?")
    failures = []
    row_evidence = row.get("claim_evidence") or {}
    for field in ROW_REQUIRED_FIELDS:
        _validate_binding(f"{pid}:row", field, row.get(field),
                          row_evidence, failures)
    for signal in row.get("signals", []):
        sid = signal.get("signal_id", "?")
        evidence = signal.get("claim_evidence") or {}
        for field in SIGNAL_REQUIRED_FIELDS:
            _validate_binding(f"{pid}:signal:{sid}", field,
                              signal.get(field), evidence, failures)
    for index, edge in enumerate(row.get("control_edges", [])):
        evidence = edge.get("claim_evidence") or {}
        for field in EDGE_REQUIRED_FIELDS:
            _validate_binding(f"{pid}:edge:{index}", field,
                              edge.get(field), evidence, failures)
    return failures
```

- [ ] **Step 2: Run all focused tests**

```powershell
python scripts/survey/test_sf_evidence_contract.py
```

Expected: `Ran 12 tests` and `OK`.

- [ ] **Step 3: Commit the generic validator**

```powershell
git add scripts/survey/sf_evidence_contract.py scripts/survey/test_sf_evidence_contract.py
git commit -m "feat(survey): bind row signal and edge evidence"
```

---

### Task 5: Write the deterministic schema-v3 migration

**Files:**

- Create: `scripts/survey/sf_schema_v3_migrate.py`
- Read: `wiki/survey/sidecars/*.sidecar.json`
- Create: `wiki/survey/current/data/schema-v3/sidecars/*.sidecar.json`

- [ ] **Step 1: Implement explicit migration policy**

The migration must use these exact policies:

```python
ANCHOR_REPLACEMENTS = {
    "p4 probe": "p4 anchor='create extend probe and prune branches'",
    "p5 cost": "p5 anchor='accuracy cost trade off'",
    "p3 Algorithm": "p3 anchor='every decision auditable'",
    "p8 Fig": "p8 anchor='natural stop time aligns with correct majority emergence'",
    "p14 delegated": "p14 anchor='asymmetric delegated architecture'",
    "p4 explore": "p4 anchor='decides every explore and stop action'",
}

POSITIVE_SELECTION_EVIDENCE = {
    "2026.findings-acl.1724#pipeline": "selection_policy",
    "2026.findings-acl.511#prm-guided-search": "selection_policy",
    "2602.16485#calibrated-orchestration": "candidate_pool_exists",
    "2604.16529#rtv": "selection_policy",
    "2604.16529#rtv-pdr-pipeline": "selection_policy",
    "2605.08083#discovered-controller": "selection_policy",
    "2606.01667#agentic-orchestration": "selection_policy",
}

NO_EXPLICIT_SELECTION = {
    "2026.findings-acl.1243#closed-prompt-only",
    "2026.findings-acl.1243#open-sft-variant",
    "2604.16529#pdr-random-k",
    "2606.03054#trained-gate",
}
```

For positive-selection rows, clone the named existing binding twice and replace `value` with the
actual `selection_object` and `explicit_candidate_pool_selection`. For `NO_EXPLICIT_SELECTION`, emit
`absence` bindings with:

```python
{
    "kind": "absence",
    "value": actual_value,
    "scope": "complete pinned method path",
    "note": "No explicit scored/tournament candidate selection is encoded for this method path; "
            "candidate-pool existence alone is not explicit selection.",
}
```

For every signal, clone its `form` binding, change `value` to `signal["source"]`, and store it as
`claim_evidence.source`. For every edge, extract the existing `canon:` or `tex:` quote from
`source_locator`, then create `claim_evidence.signal_use` and `claim_evidence.decision_right` using
that kind and quote. A locator without an extractable quote is a hard migration error.

Set each migrated sidecar's schema to:

```text
v3 (taxonomy v6: row16 + signal4 + edge2 field-bound evidence; strong PDF anchors)
```

Set `schema_v3_binding_status` to `PENDING_INDEPENDENT_ADJUDICATION`; do not reuse a prior adjudicator
identity to self-approve the new binding relation.

- [ ] **Step 2: Add a check-only mode before writing**

The command interface must be:

```powershell
python scripts/survey/sf_schema_v3_migrate.py --check
python scripts/survey/sf_schema_v3_migrate.py --write
```

`--check` builds all outputs in memory and exits non-zero if the input set is not exactly eight
sidecars, eleven method paths, twelve signals, or if any row/signal/edge binding is absent.

- [ ] **Step 3: Run check mode**

Expected output:

```text
schema-v3 migration: PASS (8 sidecars, 11 rows, 12 signals; pending adjudication)
```

- [ ] **Step 4: Write schema-v3 sidecars and inspect the diff**

```powershell
python scripts/survey/sf_schema_v3_migrate.py --write
git diff --check
git status --short
```

Expected: eight new sidecars only; no historical sidecar changes.

- [ ] **Step 5: Commit the migration tool and pending sidecars**

```powershell
git add scripts/survey/sf_schema_v3_migrate.py wiki/survey/current/data/schema-v3/sidecars
git commit -m "feat(survey): migrate evidence sidecars to schema v3"
```

---

### Task 6: Perform non-implementer binding-delta adjudication

**Files:**

- Create: `wiki/survey/current/data/schema-v3-adjudication.json`
- Modify: `wiki/survey/current/data/schema-v3/sidecars/*.sidecar.json`

- [ ] **Step 1: Give a fresh non-implementer reviewer the bounded packet**

The packet contains only:

```text
design §5-6
the eight schema-v3 sidecars
their pinned canonical records and fulltext locators
the six new binding fields (row selection x2, signal source, edge use/right)
the six anchor replacements
```

The reviewer returns one row per binding with:

```json
{
  "method_path_id": "2606.01667#agentic-orchestration",
  "owner": "edge:1",
  "field": "decision_right",
  "verdict": "AGREE",
  "reason": "The cited explore/stop decision sentence supports tool_call control."
}
```

Allowed verdicts are `AGREE` and `DISAGREE`; there is no silent skip. Record the actual reviewer task
identifier returned by the execution environment once at document top level as `reviewer_id`; reject
an empty identifier or any example/sentinel value.

- [ ] **Step 2: Apply every evidence-backed disagreement**

For each `DISAGREE`, change the encoded value or binding quote according to the cited source, rerun
the focused test, and include the change in `schema-v3-adjudication.json`. Do not downgrade a
disagreement to prose-only notes.

- [ ] **Step 3: Stamp the accepted delta**

After all rows are `AGREE`, set each sidecar's:

```text
schema_v3_binding_status = ADJUDICATED_AGREE
schema_v3_binding_adjudicator = the same non-empty reviewer_id recorded by the adjudication document
```

Recompute `adjudication_row_sha256` with the existing canonical row-hash algorithm because the row
content changed before this adjudication stamp.

- [ ] **Step 4: Commit adjudication separately from implementation**

```powershell
git add wiki/survey/current/data/schema-v3-adjudication.json wiki/survey/current/data/schema-v3/sidecars
git commit -m "audit(survey): adjudicate schema v3 evidence bindings"
```

---

### Task 7: Parameterize the coding generator and produce coding v7

**Files:**

- Modify: `scripts/survey/sf_coding_generator.py`
- Create: `wiki/survey/current/data/known-item-coding-v7.json`

- [ ] **Step 1: Add explicit CLI arguments while preserving legacy imports**

Use `argparse` with these defaults:

```python
ACTIVE_SIDECAR_DIR = os.path.join(
    REPO, "wiki", "survey", "current", "data", "schema-v3", "sidecars"
)
ACTIVE_OUT = os.path.join(
    REPO, "wiki", "survey", "current", "data", "known-item-coding-v7.json"
)
ACTIVE_TAXONOMY = "wiki/survey/current/data/identity-taxonomy-v6.json"
```

The accepted arguments are `--profile {v6,v7}`, `--sidecar-dir`, `--out`, `--taxonomy`, and `--check`.
The CLI defaults to profile `v7` and its active paths. Change `load_sidecars` to accept a directory.
Preserve existing callers by keeping `render(sidecars)` as profile v6; use the exact signature
`render(sidecars, taxonomy=LEGACY_TAXONOMY, profile="v6")`. Profile v7 emits:

```text
artifact_id = SF-KNOWN-ITEM-CODING-V7-2026-07-19-01
title = known-item coding v7 — GENERATED projection of schema-v3 sidecars
```

Profile v6 must retain the existing artifact id, title, supersession text, and taxonomy path byte for
byte. Do not change `ROW_KEY_ORDER`, row ordering, or JSON formatting.

- [ ] **Step 2: Run the old v6 regression through explicit arguments**

```powershell
python scripts/survey/sf_coding_generator.py --check `
  --profile v6 `
  --sidecar-dir wiki/survey/sidecars `
  --out wiki/survey/2026-07-19-sf-known-item-coding-v6.json `
  --taxonomy wiki/survey/2026-07-19-sf-identity-taxonomy-v5.json
```

Expected: `[OK] coding byte-identical to generator output`.

- [ ] **Step 3: Generate and check coding v7**

```powershell
python scripts/survey/sf_coding_generator.py
python scripts/survey/sf_coding_generator.py --check
```

Expected: eleven generated rows and a zero-diff check.

- [ ] **Step 4: Commit the generator and coding v7**

```powershell
git add scripts/survey/sf_coding_generator.py wiki/survey/current/data/known-item-coding-v7.json
git commit -m "feat(survey): generate schema v3 coding v7"
```

---

### Task 8: Create taxonomy v6 without changing derivations

**Files:**

- Create: `wiki/survey/current/data/identity-taxonomy-v6.json`
- Compare: `wiki/survey/2026-07-19-sf-identity-taxonomy-v5.json`

- [ ] **Step 1: Copy the v5 semantic content through an apply-patch addition**

The v6 file keeps `enums`, `signal_schema`, `control_edge_schema`, `signal_use`, `decision_rights`,
`reward_forms`, `allowed_relations`, `allowed_relations_provenance`, `derived_v5`,
`adjudication_binding`, `cross_platform_contract`, `killer_and_acceptance_contract`, and
`single_write_pipeline` equal after JSON parsing. Change only metadata and the
evidence-contract/release declarations. Build this delta as Python, merge it into a deep copy of v5,
then serialize the result as JSON:

```python
v6_contract_delta = {
  "artifact_id": "SF-IDENTITY-TAXONOMY-V6-2026-07-19-01",
  "schema": "schema-v3: row16 + signal4 + edge2 evidence bindings; discriminative PDF anchors",
  "derivation_semantics": "UNCHANGED_FROM_TAXONOMY_V5",
  "required_evidence_contract": {
    "principle": "Every load-bearing encoded value is field-bound and source-resolved before derivation.",
    "claims": {
     "row": [
      "core_weight_update",
      "external_component_weight_update",
      "controller_program_or_config_optimized_on_labels",
      "human_or_dev_label_model_selection",
      "deployment_label_access",
      "test_item_gold_access",
      "inference_external_new_information",
      "internal_visibility",
      "core_topology",
      "core_native_modality",
      "control_horizon",
      "decision_rights",
      "candidate_pool_exists",
      "selection_policy",
      "selection_object",
      "explicit_candidate_pool_selection"
     ],
     "signal": ["form", "source", "lifecycle", "uses"],
     "edge": ["signal_use", "decision_right"]
    },
    "evidence_kinds": dict(v5["required_evidence_contract"]["evidence_kinds"]),
  }
}
```

Retain the key name `derived_v5`: v6 changes the evidence contract, not the frozen derivation language.
Serialize the evaluated dictionary so the actual JSON stores the complete v5 `evidence_kinds`
object. Change `release_binding.rule` only to point active release discovery at
`wiki/survey/current/manifest.json`; historical bound artifacts remain available through explicit
legacy regression.

- [ ] **Step 2: Add a semantic-equality assertion to the v6 harness preparation**

Use a small inline diagnostic during implementation:

```powershell
python -c "import json; a=json.load(open('wiki/survey/2026-07-19-sf-identity-taxonomy-v5.json',encoding='utf-8')); b=json.load(open('wiki/survey/current/data/identity-taxonomy-v6.json',encoding='utf-8')); keys=['enums','signal_schema','control_edge_schema','signal_use','decision_rights','reward_forms','allowed_relations','allowed_relations_provenance','derived_v5','adjudication_binding','cross_platform_contract','killer_and_acceptance_contract','single_write_pipeline']; print(all(a[k]==b[k] for k in keys))"
```

Expected: `True`.

- [ ] **Step 3: Commit taxonomy v6**

```powershell
git add wiki/survey/current/data/identity-taxonomy-v6.json
git commit -m "docs(survey): freeze taxonomy v6 evidence contract"
```

---

### Task 9: Add the v6 integration and mutation harness

**Files:**

- Create: `scripts/survey/sf_identity_taxonomy_v6_test.py`
- Read: `scripts/survey/sf_identity_taxonomy_v5_test.py`
- Read: `scripts/survey/sf_evidence_contract.py`

- [ ] **Step 1: Build the v6 harness around the existing derivation**

The new harness imports `derive`, `row_hash`, `run_expectations`, and `validate` from
`sf_identity_taxonomy_v5_test`; copy the v5 `occupancy` function into v6 unchanged because it is
currently nested in `main`. Reuse the frozen K1-K7/A1-A8 fixture construction without changing its
inputs or expected truth values. Load v6 taxonomy, coding v7, and schema-v3 sidecars from the new
paths. It must call, in this order for every load-bearing row:

```python
structure_failures = validate(rows)
binding_failures = sum((validate_bound_values(row) for row in rows), [])
source_failures = reconcile_v6(sidecars, coding_text)
```

Implement `reconcile_v6` by copying v5 `reconcile` and changing only these seams: render coding with
`profile="v7"`; call `check_page_locator` anywhere v5 called `check_page_tokens`; validate every
`pdf_page` row/signal/edge binding locator; add `validate_bound_values`; require
`schema_v3_binding_status == "ADJUDICATED_AGREE"`; and resolve the active v6 paths. Preserve v5's
ledger/hash/canon/TeX/PDF resolution and actor-separation checks unchanged.

Persist reports under:

```python
OUT_DIR = os.path.join(REPO, "docs", "checks", "system-first-stage1a", "evidence-v6")
OUT = os.path.join(OUT_DIR, "identity-taxonomy-v6-test.json")
```

- [ ] **Step 2: Add legitimate-rehash mutations**

Include the existing E1-E5 and sensitivity mutations plus these exact new cases:

```text
E3b_generic_anchor_the
E3c_frequent_phrase
E6_signal_source_flip
E7_edge_use_coherent_flip
E8_edge_right_coherent_flip
E9_selection_object_flip
E10_explicit_selection_flip
E11_missing_signal_source_binding
E12_missing_edge_right_binding
```

For E6-E12, recompute the adjudication row hash after mutation. Expected failures must contain the
specific binding/anchor code, not `row-hash`.

- [ ] **Step 3: Add generic twelfth-row integration checks**

Use the `generic_row()` shape from the unit test. Assert:

```text
good row -> validate_structure + validate_bound_values both empty
source flip -> signal source mismatch
edge use flip -> edge use mismatch
selection object flip -> row selection mismatch
missing binding -> required-evidence failure
```

No lookup table may mention `__fx12__#path` outside the fixture itself.

- [ ] **Step 4: Run the v6 harness on Windows**

```powershell
python scripts/survey/sf_identity_taxonomy_v6_test.py
```

Expected: overall `PASS`; occupancy exactly matches the v5 report:

```text
reward_guided=6/11
rq_sys_compatible=5/11
method_candidate=0/11
reward_guided_selection=4/11
trajectory_pool=2/11
```

- [ ] **Step 5: Commit the v6 harness and Windows report**

```powershell
git add scripts/survey/sf_identity_taxonomy_v6_test.py docs/checks/system-first-stage1a/evidence-v6
git commit -m "test(survey): enforce schema v3 contract end to end"
```

---

### Task 10: Parameterize and run dual-platform verification

**Files:**

- Modify: `scripts/survey/sf_dual_platform_check.py`
- Create/update: `docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test.*.json`

- [ ] **Step 1: Add `--base` to the aggregator**

Use `argparse` and default `--base` to:

```text
docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test
```

Keep the required platform suffixes `nt` and `posix`, PASS assertions, and exact occupancy equality.

- [ ] **Step 2: Re-run Windows and verify its stamp**

```powershell
python scripts/survey/sf_identity_taxonomy_v6_test.py
python -c "import json; p='docs/checks/system-first-stage1a/evidence-v6/identity-taxonomy-v6-test.nt.json'; d=json.load(open(p,encoding='utf-8')); print(d['platform'],d['verdict'])"
```

Expected: `{'os': 'nt', 'python': '3.14.3'} PASS` or the actual installed 3.14 patch version.

- [ ] **Step 3: Run the canonical WSL2 environment**

```powershell
wsl -d Ubuntu-24.04 bash -lc "source ~/.venvs/speechrl/bin/activate && cd /mnt/d/chao_workspace/exploring-l4-intelligence && python scripts/survey/sf_identity_taxonomy_v6_test.py"
```

Expected: overall `PASS`, `os=posix`, Python 3.12.x.

- [ ] **Step 4: Aggregate both snapshots**

```powershell
python scripts/survey/sf_dual_platform_check.py
```

Expected:

```text
occupancy equality: CONFIRMED
dual-platform check: PASS (0 failures)
```

- [ ] **Step 5: Confirm historical audit files are untouched**

```powershell
python scripts/survey/sf_audit_immutability_check.py
git status --short
```

Expected: immutability `PASS`; only the planned v6 files and reports are changed.

- [ ] **Step 6: Commit dual-platform evidence**

```powershell
git add scripts/survey/sf_dual_platform_check.py docs/checks/system-first-stage1a/evidence-v6
git commit -m "test(survey): preserve dual-platform evidence v6"
```

---

### Task 11: Run Plan-A final verification

**Files:**

- Verify all Plan-A files.

- [ ] **Step 1: Run focused and integration tests**

```powershell
python scripts/survey/test_sf_evidence_contract.py
python scripts/survey/sf_schema_v3_migrate.py --check
python scripts/survey/sf_coding_generator.py --check
python scripts/survey/sf_identity_taxonomy_v6_test.py
python scripts/survey/sf_dual_platform_check.py
python scripts/survey/sf_audit_immutability_check.py
```

Expected: every command exits zero.

- [ ] **Step 2: Verify taxonomy semantics and occupancy against v5**

Run a diagnostic that loads both reports and asserts equality of `occupancy`; expected output is
`occupancy_equal=True`.

- [ ] **Step 3: Verify no Stage-1B execution occurred**

```powershell
git diff 4af9052..HEAD -- docs/integrity/experiment_attempt_registry.jsonl wiki/survey/2026-07-15-sf-queries.jsonl
```

Expected: no diff in the attempt registry or frozen query records.

- [ ] **Step 4: Check repository cleanliness and record the Plan-A checkpoint**

```powershell
git diff --check
git status --short
git log -8 --oneline
```

Expected: clean working tree. Plan B may now consume the v6 paths; no readiness statement is emitted
until Plan B's context and correction gates pass.
