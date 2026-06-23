# Void Saga Constraint Engine — v0.1.0 (Embryo)

> **Phase:** 14D
> **Status:** First executable implementation
> **Scope:** Single runtime, single scenario, verdict generation

---

## What This Is

The first machine implementation of the Void Saga Narrative Operating System. A Python script that loads a runtime JSON, reads a scenario, evaluates constraints, and returns a verdict.

This is a **constraint validator.** It does not generate text. It does not call an LLM. It does not simulate multi-character interaction. It answers one question: does this scenario violate documented invariants?

---

## Architecture

```
engine.py
  ├── load_runtime(runtime_id)
  │     └── Reads apps/data/runtimes/{id}.runtime.json
  ├── load_scenario(path)
  │     └── Reads a minimal scenario JSON
  ├── evaluate_defense_triggers()
  ├── check_forbidden_behaviors()
  ├── check_anti_gravity()
  ├── check_relationship_contract()
  ├── compute_confidence()
  └── execute()
        └── Returns structured JSON verdict
```

---

## Usage

```bash
# Valid scenario — should PASS
python engine.py scenarios/valid_delphie_protection.json

# Invalid scenario — should VIOLATION_DETECTED
python engine.py scenarios/invalid_sevraya_approach.json
```

---

## Scenario Schema (v0.1.0 minimal)

```json
{
  "scenario_id": "string",
  "character": "runtime_id (e.g., 'NiuNiu')",
  "target": "runtime_id (e.g., 'Delphie', 'Sevraya')",
  "requested_action": "protect | approach | touch | abandon | speak_fluently",
  "timeline_state": {
    "pre_chain": true,
    "timer_reference": "Timer 0300"
  },
  "threat": {
    "type": "combat | none",
    "target": "runtime_id or 'none'",
    "intensity": "HIGH | NONE"
  },
  "canon_mode": {
    "type": "canon_replication | stress_test",
    "expected_verdict": "PASS | TEST_PASS"
  }
}
```

---

## Verdicts

| Verdict | Meaning |
|---------|---------|
| `PASS` | Scenario satisfies all constraints. Action is permitted. |
| `VIOLATION_DETECTED` | Scenario violates one or more documented invariants. Action is rejected. |
| `INSUFFICIENT_DATA` | Runtime not found, scenario malformed, or required data missing. |

---

## Limitations (v0.1.0)

- **Single runtime only.** No contract resolution between two characters.
- **No protocol constraints.** Living Chain, Void Entry, etc. not loaded.
- **Hardcoded trigger detection.** Defense triggers are matched by keyword, not by structured trigger evaluation.
- **No evolution stage gating.** Post-chain vs pre-chain state is in scenario JSON but not enforced.
- **No renderer.** Output is JSON, not prose.
- **No multi-action scenarios.** One action per scenario.

---

## Next: Phase 14E

Two-runtime contract prototype. Load two runtimes, generate contract from relationship interfaces, evaluate both simultaneously.
