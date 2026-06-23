# Void Saga Constraint Engine — v0.3.0 (Contract-First Evaluation)

> **Phase:** 14G
> **Status:** Contract-first evaluation. Contract object is primary source of truth.
> **Scope:** Load standalone contract, evaluate scenario directly against allowed/forbidden states and violation rules.

---

## Architecture

```
engine.py
  ├── [v0.3.0] execute_contract_first(scenario, contract_id)
  │     ├── load_contract(contract_id)
  │     └── evaluate_against_contract(contract, scenario)
  │           ├── Check allowed_states
  │           ├── Check forbidden_states
  │           ├── Apply violation_rules
  │           └── Match test_references
  │
  ├── [v0.2.0 compat] execute(scenario)
  │     └── Runtime-derived contract generation (backward compatible)
  │
  └── [v0.1.0 compat] Legacy single-runtime scenarios
```

---

## Usage

```bash
# Contract-first mode (default, v0.3.0)
python engine.py scenarios/orbital_constant_valid.json
python engine.py scenarios/orbital_contract_violation.json

# Runtime-derived contract generation (v0.2.0 compat)
python engine.py scenarios/orbital_constant_valid.json --mode runtime
```

---

## Verdicts (v0.3.0 contract-first)

| Run | Scenario | Verdict | Rule | Violations | Tests |
|-----|----------|---------|------|------------|-------|
| A | maintain_distance | **PASS** | ORBITAL_MAINTENANCE | 0 | ORBITAL_CONSTANT_RUN_001 |
| B | touch | **VIOLATION_DETECTED** | ORBITAL_APPROACH_VIOLATION | 4 | 2 tests matched |

---

## What Changed from v0.2.0

| v0.2.0 | v0.3.0 |
|--------|--------|
| Load 2 runtimes → generate contract | Load 1 contract object |
| Evaluate from both runtime perspectives | Evaluate against contract states directly |
| Contract generated per execution | Contract is standalone, reusable |
| Test references not tracked | Test references matched and reported |

---

## Contract-First Advantages

1. **Single source of truth.** Contract object is versioned, auditable, and independent of runtime JSON changes.
2. **Faster execution.** No runtime loading or interface extraction required.
3. **Test traceability.** Engine reports which prior tests match the current verdict.
4. **Portable.** Contract can be loaded by any engine implementation without runtime dependencies.

---

## Limitations (v0.3.0)

- Only orbital_constant contract implemented
- Contract ID hardcoded to "orbital_constant"
- No multi-contract resolution
- No renderer
- Runtime mode backward compat limited to v0.2.0 scenarios

---

## Next: Phase 14H

Multi-contract engine. Load multiple contract objects. Evaluate scenarios involving 3+ participants with overlapping contracts.
