# TASK 5E OUTPUT — Canon Score Aggregation

> **Status:** COMPLETE
> **Date:** 25 June 2026

---

## What Was Implemented

Two-dimensional scoring: `canon_score` (constraint conformity) and `evidence_confidence` (data quality).

### New file: `apps/engine/lib/scoring.py` (140 lines)

| Function | Purpose |
|----------|---------|
| `compute_evidence_confidence()` | E / (E+I+PC) ratio across all participants |
| `compute_canon_score()` | Weighted penalty deduction from violations + warnings |
| `determine_canon_verdict()` | Threshold mapping: ≥0.95 PASS, ≥0.8 WARNING, <0.8 VIOLATION |
| `aggregate_scores()` | Combined scoring entry point |

### Canon Score Formula

```
canon_score = 1.0 - Σ(weight × severity) / total_constraints

Weights:
  forbidden_behavior:      0.4
  identity_invariant:      0.35
  anti_gravity:            0.5
  contract_forbidden_state: 0.3
  contract_violation_rule: 0.25
  defense_trigger:         0.2

Severity multipliers:
  ERROR:   1.0
  WARNING: 0.5
```

### Verdict Thresholds

| Score | Verdict |
|-------|---------|
| ≥ 0.95 | CANON_PASS |
| ≥ 0.8 | CANON_WARNING |
| < 0.8 | CANON_VIOLATION |

## Test Results — Score Table

| Scenario | canon_score | evidence | penalty | canon_verdict | final |
|----------|------------|----------|---------|---------------|-------|
| NiuNiu+Sevraya orbit | **1.0** | 0.76 | 0 | CANON_PASS | PASS |
| Sevraya+Zero surface | **1.0** | 0.73 | 0 | CANON_PASS | PASS |
| 3-body proximity | **0.93** | 0.74 | 3.6 | CANON_WARNING | VIOLATION |
| Zero emotional ❌ | **0.97** | 0.67 | 0.4 | CANON_PASS | VIOLATION |
| NiuNiu speech ❌ | **0.97** | 0.75 | 0.57 | CANON_PASS | VIOLATION |
| Zero separation ❌ | **0.99** | 0.73 | 0.4 | CANON_PASS | VIOLATION |
| Orbital pass | **1.0** | 0.76 | 0 | CANON_PASS | PASS |
| Orbital touch ❌ | **0.9** | 0.76 | 3.6 | CANON_WARNING | VIOLATION |

### Key observations

1. **Clean canon scenarios score 1.0.** No violations, no warnings, perfect scores.

2. **Single violations deduct 0.4 (0.03 off total).** A single forbidden_behavior violation (weight 0.4) against 15+ constraints produces a small deduction (0.97). This is correct — the score reflects "mostly canon with one violation" rather than tanking to zero.

3. **Multi-violation scenarios cluster at 0.9–0.93.** The orbital touch scenario has 12 contract violations (weight 0.3 each) producing a 3.6 penalty. The 3-body proximity scenario has similar.

4. **Evidence confidence reflects runtime data quality.** Zero has the lowest confidence (0.67 — 28E/12I/2PC) because many of its claims are inferred. NiuNiu and Sevraya have higher confidence (0.76 — more [E] claims).

5. **canon_verdict and final_verdict are complementary.** A scenario can be CANON_PASS (high score, mostly canon) but still have final=VIOLATION (the engine detected a specific constraint violation). The canon_verdict answers "how well does this fit canon overall?" while final answers "did any constraint fail?"

## Files Modified

| File | Change |
|------|--------|
| `lib/scoring.py` | NEW — evidence_confidence, canon_score, verdict thresholds |
| `engine_v2.py` | ADDED scoring pipeline step, score display in print_summary |

## Result Structure (scoring section)

```json
{
  "scoring": {
    "canon_score": 0.97,
    "evidence_confidence": 0.67,
    "canon_verdict": "CANON_PASS",
    "breakdown": {
      "evidence_breakdown": { "E_total": 28, "I_total": 12, "PC_total": 2, ... },
      "penalty_breakdown": {
        "total_penalty": 0.4,
        "total_constraints_checked": 15,
        "items": [{ "constraint_type": "forbidden_behavior", "penalty": 0.4, ... }]
      },
      "total_constraints": 15
    }
  }
}
```
