---
title: "Owner amendment: retire the first-slice numeric budget caps"
record_id: "SAEA-OWNER-AMENDMENT-2026-08-06-BUDGET-CAPS"
date: "2026-08-06"
issued_by: "research owner (in-session directive, 2026-08-06)"
amends: "2026-08-04-owner-consolidated-execution-contract.md §6 (Resources row)"
status: "SIGNED_BY_OWNER"
model_touch_performed: false
---

# Owner amendment — retire the first-slice numeric budget caps

## 1. Disposition

On 2026-08-06 the owner signed explicitly: **retire the three numeric ceilings in the Resources row
of the consolidated execution contract §6** (≤3,000 frozen-core calls, ≤40 GPU-hours, ≤20 hours of
speech audio). From the effective date of this record those figures are no longer machine-enforced
conditions, and are no longer a ground on which a gate refuses.

Reason (as the owner stated it): this study is in its Stage-2 exploration period, and the numeric
caps repeatedly took up attention in design and planning discussion, out of proportion to the actual
protection they delivered.

## 2. What is retained unchanged (outside the scope of this retirement)

This amendment **retires the numeric ceilings only**. The following mechanisms **remain in force and
remain machine-enforced**:

- **Paid API spend = 0**: that item of contract §6 is unchanged;
- **Exposure pre-registration**: before every model/tool contact a row must land in the study repo's
  `docs/exposure-ledger.md`, carrying the execution profile, split role, split identity hash,
  consumed flag, and carrier;
- **One-shot attempt semantics**: `(run_id, attempt_id)` is never reusable; usage is persisted
  before sending; a failed attempt's actual usage still enters the durable record; a retry must use
  a new attempt;
- **Per-run self-consistency**: the `ExecutionPlan` still declares this run's planned call count /
  audio seconds / GPU hours, and is still verified field by field against its exposure row
  (registered value ≥ planned value); a run must never exceed the allowance **it registered for
  itself**;
- **Stage-3 stop line**: profiles such as `paper-scale-confirmatory` still fail closed without
  exception (contract §7 unchanged).

That is: the exposure ledger still answers "who touched what, and when" — there is simply no longer
a whole-slice numeric ceiling.

## 3. Engineering consequences (recorded honestly)

The 2026-08-05 independent review filed "the same exposure allowance can be consumed repeatedly" as
P0-4. The **one-time-consumption half** of that finding stays closed (see the attempt semantics in
§2); its **numeric-ceiling half** no longer applies because of this amendment — this is not a
regression, but the owner deliberately narrowing the contract's obligations. No later review should
file "the first-slice numeric caps are not enforced" as a defect.

If the owner later wishes to restore numeric budgets, that requires a new dated amendment; the
implementer must never reintroduce them unilaterally.

## 4. Implementer obligations

- remove `FIRST_SLICE_CAPS` and its whole-slice summation check from the code;
- never raise the budget-allocation question again in any design, plan, or status document;
- correct the study's `docs/engineering.md` and the exposure-ledger explanatory text in step,
  leaving no residual wording that says "the caps are enforced";
- the ledger's three columns — calls / speech audio seconds / gpu hours — **are retained as a
  record** (they are useful facts) but no longer carry enforcement semantics.

## 5. Invalidation condition

This record is superseded in place when the owner restores or modifies the budget obligations by a
new dated record.

---

**Language conversion (2026-08-25).** Re-issued in English with terms, scope, dates, signature, and
authority unchanged; content is preserved throughout — this is a language conversion, not an edit.
Pre-conversion bytes are Git blob `657bf44b8702913af03f25d9bab1593810e38daf`; the conversion is
recorded in `wiki/Decision-Log-2026-08.md` continuation entry 95.
