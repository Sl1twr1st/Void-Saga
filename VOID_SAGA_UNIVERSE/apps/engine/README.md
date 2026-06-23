# Void Saga Constraint Engine — v0.2.0 (Two-Runtime Contract)

> **Phase:** 14E
> **Status:** Two-runtime contract validation
> **Scope:** Load two runtimes, generate contract, evaluate from both directions

---

## What This Is

Upgraded from single-runtime validation (v0.1.0) to two-runtime contract validation (v0.2.0). The engine now loads two runtime JSONs, extracts relationship interfaces from both directions, generates a merged contract, and evaluates scenarios from both characters' perspectives.

---

## Architecture

```
engine.py
  ├── load_runtimes([id_a, id_b])
  ├── generate_contract(runtime_a, runtime_b)
  │     ├── Extracts relationship_interfaces from both directions
  │     ├── Compares symmetry_status
  │     └── Merges behavioral rules into shared constraints
  ├── evaluate_runtime_constraints(runtime, scenario, target, is_actor)
  │     ├── Defense triggers
  │     ├── Forbidden behaviors (deduplicated)
  │     └── Anti-gravity (merge/healing only)
  ├── evaluate_contract(contract, scenario)
  └── execute(scenario_path)
```

---

## Usage

```bash
# Valid orbital constant scenario
python engine.py scenarios/orbital_constant_valid.json

# Invalid touch/merge scenario
python engine.py scenarios/orbital_contract_violation.json

# Legacy single-runtime scenarios still work
python engine.py scenarios/valid_delphie_protection.json
```

---

## Verdicts

| Run | Scenario | Verdict | Violations |
|-----|----------|---------|------------|
| A | Sevraya appears. Both maintain distance. | **PASS** | 0 |
| B | Sevraya approaches, attempts touch. | **VIOLATION_DETECTED** | 6 (3 types, 2 runtimes) |

---

## Limitations (v0.2.0)

- NiuNiu + Sevraya contract only (hardcoded runtime IDs in scenario)
- No protocol constraints loaded
- No renderer
- Keyword-based trigger matching
- Single action per scenario
- Contract generation depends on both runtimes having relationship_interfaces with matching target IDs (case-insensitive)

---

## Next: Phase 14F

Negative test prototype. Automated violation detection with structured violation sourcing.
