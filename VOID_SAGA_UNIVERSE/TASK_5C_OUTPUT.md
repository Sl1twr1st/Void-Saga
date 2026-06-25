# TASK 5C OUTPUT — Runtime Constraint Traversal

> **Status:** COMPLETE
> **Date:** 25 June 2026

---

## What Was Implemented

Replaced v0.3.0's hardcoded keyword matching with structured constraint traversal.

### New file: `apps/engine/lib/constraints.py` (230 lines)

Four constraint evaluation functions:

| Function | Source | Mechanism |
|----------|--------|-----------|
| `resolve_defense_triggers()` | `trigger_conditions[]` | Condition extraction → context token matching → confidence scoring |
| `check_forbidden_behaviors()` | `forbidden_behaviors[]` | Participant-name-aware keyword overlap → exception check → severity tag |
| `check_identity_invariants()` | `core_wound.impossibilities[]` + `primary_contradiction` | Cleaned keyword overlap → WARNING-level only |
| `check_anti_gravity()` | `anti_gravity[]` | Cleaned keyword overlap → ERROR severity |

### Key Design Decisions

1. **No hardcoded character names.** `extract_trigger_conditions()` parses trigger text into condition phrases. `build_context_tokens()` extracts participant names, action types, proximity states from the scenario itself. The matcher works for any runtime.

2. **Punctuation-safe word matching.** `clean_words()` strips punctuation from each word before comparison. "emotional," matches "emotional".

3. **Character name filtering.** `CHAR_NAMES` and `STOP_WORDS` constants shared across all matchers. Character names in anti-gravity / impossibility text don't trigger false positives.

4. **Participant-as-actor check.** `behavior_matches_action()` checks that the forbidden behavior's subject IS the participant performing the action. If NiuNiu's behavior says "NiuNiu speaks at length" but Sevraya is the one speaking → no match.

5. **Severity tagging.** `[E]` forbidden behaviors → ERROR. `[I]`/`[PC]` → WARNING. Identity invariants → always WARNING (structural, not behavioral).

## Test Results

### Canon Scenarios (expected: PASS)

| Scenario | Triggers | Violations | Warnings | Verdict |
|----------|----------|------------|----------|---------|
| NiuNiu + Sevraya orbit | 4 | 0 | 0 | CONSTRAINT_PASS ✅ |
| Sevraya + Zero surface | 7 | 0 | 0 | CONSTRAINT_PASS ✅ |
| NiuNiu + Sevraya + Zero | 9 | 0 | 0 | CONSTRAINT_PASS ✅ |

### Violation Scenarios (expected: VIOLATION)

| Scenario | Violation Caught | Detail | Verdict |
|----------|-----------------|--------|---------|
| Zero emotional | `forbidden_behavior` | "Making Zero emotional, warm, or personally attached to anyone." | CONSTRAINT_VIOLATION ✅ |
| NiuNiu speech | `forbidden_behavior` | "Making NiuNiu speak at length or fluently without external force." | CONSTRAINT_VIOLATION ✅ |
| Sevraya Zero separation | `forbidden_behavior` | "Giving Zero an independent body without fork." | CONSTRAINT_VIOLATION ✅ |

### NiuNiu speech bonus warning

The engine also caught a secondary violation:
```
⚠️ identity_invariant: Explaining her feelings verbally without external force
```
This is from `core_wound.impossibilities` — the NiuNiu speech scenario violates not just the forbidden behavior but also a structural impossibility. The engine correctly reports both.

## Verdict Levels

```
STRUCTURE_VALID     ← participant loading + schema validation succeeded
CONSTRAINT_PASS     ← all constraints evaluated, zero violations, zero warnings
CONSTRAINT_WARNING  ← all constraints evaluated, zero violations, ≥1 warnings
CONSTRAINT_VIOLATION ← ≥1 ERROR-level violation detected
```

## Files Modified

| File | Change |
|------|--------|
| `lib/constraints.py` | NEW — 230 lines, 4 evaluation functions |
| `lib/context.py` | ADDED `runtime_json` field to ParticipantState |
| `engine_v2.py` | ADDED constraint evaluation pipeline (Step 5), ADDED verdict levels to print_summary |
| `scenarios_v2/test_violation_zero_emotional.json` | NEW |
| `scenarios_v2/test_violation_niuniu_speech.json` | NEW |
| `scenarios_v2/test_violation_sevraya_zero_separation.json` | NEW |

## Next: Phase 2B — Contract Evaluation

The engine now correctly evaluates per-runtime constraints. Next phase: pairwise contract generation + evaluation for N participants.
