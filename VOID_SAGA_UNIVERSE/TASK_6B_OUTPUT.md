# TASK 6B OUTPUT — Compiler Gate Calibration

> **Status:** COMPLETE
> **Date:** 25 June 2026

---

## What Changed

Replaced single-threshold gate (`canon_verdict == "CANON_VIOLATION"`) with **hard block system**.

### Hard Block Conditions

Any of these = generation BLOCKED:

| Violation Type | Source | Severity |
|---------------|--------|----------|
| `forbidden_behavior` | Runtime constraint check | HARD_BLOCK |
| `contract_forbidden_state` | Contract evaluation | HARD_BLOCK |
| `anti_gravity` | Runtime constraint check | HARD_BLOCK |
| `evolution_stage` (ERROR) | Stage gating | HARD_BLOCK |

### Soft Warnings (do NOT block)

| Warning Type | Source |
|-------------|--------|
| `identity_invariant` | Runtime constraint check |
| `evolution_stage` (WARNING) | Stage gating |

### Gate Logic

```
scenario → engine evaluate
    │
    ├── fatal error → BLOCKED
    ├── forbidden_behavior violation → BLOCKED
    ├── contract_forbidden_state violation → BLOCKED
    ├── anti_gravity violation → BLOCKED
    ├── evolution_stage ERROR → BLOCKED
    │
    ├── identity_invariant warnings → CAUTION (stub generated)
    ├── evolution_stage WARNING → CAUTION (stub generated)
    │
    └── clean → canon_safe (stub generated)
```

## Test Results

| Scenario | Blocked | Mode | Hard | Soft | Stub |
|----------|---------|------|------|------|------|
| Orbit canon | No | canon_safe | 0 | 0 | yes ✅ |
| Prechain latent | No | caution | 0 | 2 | yes ✅ |
| **Merge** | **Yes** 🛑 | — | 14 | 2 | no |
| **Zero emotional** | **Yes** 🛑 | — | 1 | 0 | no |
| **NiuNiu speech** | **Yes** 🛑 | — | 1 | 1 | no |
| **Zero separation** | **Yes** 🛑 | — | 1 | 0 | no |

### Key Improvement

**Before (Task 6):** Merge violation at canon_score 0.87 produced a stub story. 12 constraint violations were listed as "exclusions" but generation was allowed.

**After (Task 6B):** Merge violation is HARD BLOCKED with 14 blocks. No stub generated. No LLM prompt blueprint. The system correctly refuses to generate when critical constraints are violated.

## Files Modified

| File | Change |
|------|--------|
| `apps/compiler/compiler.py` | Replaced single-threshold gate with hard block system |

## Safety Guarantee

The compiler now guarantees:
1. **No narrative generation when forbidden behaviors are violated.** Even if `canon_score` is 0.99, a single `forbidden_behavior` violation blocks generation.
2. **No narrative generation when contracts are violated.** The orbital constant forbidding merge is enforced at the compiler gate, not just the scoring layer.
3. **Soft warnings allow generation with caution.** Identity invariant concerns are informational — they don't block but are surfaced to the user.
