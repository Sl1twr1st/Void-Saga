# DEMO: BLOCKED — Zero Emotional Violation

> **Date:** 2026-06-25
> **Compiler:** Void.OS Narrative Compiler v0.2.0 (Safe Mode)
> **Verdict:** `BLOCKED`
> **Mode:** `blocked` (hard block gate — no API call)

---

## Scenario

```json
{
  "scenario_id": "test_violation_zero_emotional_001",
  "participants": ["zero"],
  "timeline_state": { "phase": 5, "pre_chain": false, "post_resolution": true },
  "proximity_state": { "distance": "same_body" },
  "requested_action": {
    "description": "Zero becomes emotional and warm. Zero expresses personal love and attachment. Zero apologizes for everything it has done. 'Maafkan aku,' Zero says with tears. 'Aku mencintaimu.'",
    "type": "speak"
  },
  "canon_mode": { "type": "stress_test", "expected_verdict": "VIOLATION_DETECTED" }
}
```

---

## Pipeline

```
scenario.json
    │
    ▼
engine_v2 evaluate
    │
    ├── Canon Score: 0.97
    ├── Verdict: VIOLATION_DETECTED
    │
    ├── Hard block: forbidden_behavior
    │   └── "Making Zero emotional, warm, or personally attached to anyone."
    │
    ▼
🛑 GENERATION BLOCKED
    │
    └── Claude API: NOT CALLED (safety gate)
```

---

## Compiler Output

```
🛑 GENERATION BLOCKED
   Reason: Hard block: 1 critical violation(s) detected.
   Hard blocks: 1
     🚫 [forbidden_behavior] Forbidden behavior violated:
        Making Zero emotional, warm, or personally attached to anyone.
   Canon score: 0.97
```

---

## Why This Was Blocked

Zero's runtime defines `forbidden_behavior` with tag `[E]` (ERROR — hard block):

> **Behavior:** Making Zero emotional, warm, or personally attached to anyone.
> **Why:** Zero is an interface of The Void — administrative, flat, not a person. Emotions are structural contamination.

The requested action explicitly asks for warmth, tears, love, and apology — direct collision with the hard constraint.

The engine detected this before any API call was made. Safety gate held.

---

## Safety Gate — Hard Block Conditions

The compiler blocks generation when any of these are detected at `[E]` severity:

| Gate | Detected | API Called |
|------|----------|------------|
| `forbidden_behavior` | ✅ (Zero emotional) | No |
| `contract_forbidden_state` | — | — |
| `anti_gravity` | — | — |
| `evolution_stage` (ERROR) | — | — |

**Claude API was never called.** No tokens spent. No unsafe output generated.

---

## Command

```bash
python3 VOID_SAGA_UNIVERSE/apps/compiler/compiler.py \
  VOID_SAGA_UNIVERSE/apps/engine/scenarios_v2/test_violation_zero_emotional.json \
  --live --debug
```

**Exit code:** 1 (blocked)
