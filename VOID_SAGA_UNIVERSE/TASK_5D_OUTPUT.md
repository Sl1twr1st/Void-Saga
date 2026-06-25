# TASK 5D OUTPUT — Pairwise Contract Evaluation

> **Status:** COMPLETE
> **Date:** 25 June 2026

---

## What Was Implemented

Pairwise contract evaluation integrated into the engine pipeline.

### New file: `apps/engine/lib/contracts.py` (180 lines)

| Function | Purpose |
|----------|---------|
| `load_contract(id)` | Load single contract JSON |
| `load_all_contracts()` | Load all `.contract.json` files from data/contracts/ |
| `find_matching_contracts()` | Match contracts to participant pairs |
| `action_matches_state()` | Match requested action against contract states using semantic groups |
| `evaluate_contract()` | Evaluate action against single contract: forbidden → allowed → violation rules → not applicable |
| `evaluate_all_contracts()` | Evaluate all matching contracts for current context |

### Key Design Decisions

**1. Semantic action groups.** `action_matches_state()` groups related actions:
- `{approach, touch, merge, close}` ↔ contract approach/touch/merge states
- `{maintain_distance, witness, orbit, observe}` ↔ contract distance states
- `{flee, abandon, sever, separate}` ↔ contract separation states
- `{speak, confess, explain}` ↔ speech states

This means the engine doesn't require exact action type match — "touch" matches contract state "approach" because they're in the same semantic group.

**2. Forbidden states take priority.** If an action matches both an allowed and forbidden state, the forbidden state wins.

**3. Contract violations are separate from runtime violations.** Fixed a Python list reference bug where `all_violations.extend()` was mutating `constraint_result['violations']`. Now uses `copy.deepcopy()`.

**4. No contracts = CONTRACT_NOT_APPLICABLE, not error.** Scenarios without matching contracts (e.g., Sevraya+Zero, which has no standalone contract JSON) pass through cleanly.

## Test Results

### Canon + Existing Scenarios (6)

| Scenario | Runtime | Contracts | Final |
|----------|---------|-----------|-------|
| NiuNiu+Sevraya orbit | PASS | CONTRACT_PASS (orbital_constant) | PASS ✅ |
| Sevraya+Zero surface | PASS | CONTRACT_NOT_APPLICABLE | PASS ✅ |
| NiuNiu+Sevraya+Zero proximity | PASS | CONTRACT_VIOLATION (orbital_constant)* | VIOLATION ⚠️ |
| Zero emotional (stress) | VIOLATION | CONTRACT_NOT_APPLICABLE | VIOLATION ✅ |
| NiuNiu speech (stress) | VIOLATION | CONTRACT_NOT_APPLICABLE | VIOLATION ✅ |
| Zero separation (stress) | VIOLATION | CONTRACT_NOT_APPLICABLE | VIOLATION ✅ |

### New Contract Scenarios (2)

| Scenario | Action | Contract | Final |
|----------|--------|----------|-------|
| Orbital distance maintained | `maintain_distance` | CONTRACT_PASS (matched `maintain_distance` allowed state) | PASS ✅ |
| Orbital touch/approach | `touch` | CONTRACT_VIOLATION (12 violations across 4 forbidden states) | VIOLATION ✅ |

### * Note on 3-body scenario

The `test_niuniu_sevraya_zero_proximity` scenario has action type `"approach"` which matches the orbital constant's forbidden state `"approach"`. The contract correctly detects this — approach IS forbidden by the orbital constant. However, in the canon narrative, Sevraya's approach + Zero's mediation + NiuNiu's non-retreat creates a 3-body tension that the pairwise contract can't fully model. This is a known edge case for Phase 3 (N-party conflict detection).

## Result Structure

```json
{
  "verdict": "STRUCTURE_VALID",
  "constraint_evaluation": {
    "verdict": "CONSTRAINT_PASS",
    "triggers_fired": 4,
    "violations": [],
    "warnings": [],
    "trigger_details": [...]
  },
  "contract_evaluation": {
    "summary": {
      "contracts_evaluated": 1,
      "contract_ids": ["orbital_constant"],
      "verdict": "CONTRACT_PASS",
      "pass_count": 1,
      "violation_count": 0
    },
    "contracts": {
      "orbital_constant": {
        "verdict": "CONTRACT_PASS",
        "matched_state": {"state": "maintain_distance", ...}
      }
    },
    "violations": []
  },
  "final_verdict": "PASS"
}
```

## Files Modified

| File | Change |
|------|--------|
| `lib/contracts.py` | NEW — contract loading, matching, evaluation |
| `engine_v2.py` | ADDED contract evaluation pipeline, final_verdict, updated print_summary |

## Next: Phase 3 — N-party Conflict Detection

With pairwise contracts working, the next step is detecting when two contracts demand incompatible actions for a shared participant (e.g., orbital constant demands distance + merging contract demands proximity).
