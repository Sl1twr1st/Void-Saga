# TASK 5B OUTPUT — Multi-Runtime Engine Skeleton

> **Status:** COMPLETE
> **Engine version:** v0.4.0 — Phase 1 (Skeleton)
> **Date:** 25 June 2026

---

## Files Created

| File | Lines | Purpose |
|------|-------|---------|
| `apps/engine/lib/__init__.py` | 1 | Library package marker |
| `apps/engine/lib/loader.py` | 54 | Runtime/scenario loading + participant validation + schema check |
| `apps/engine/lib/context.py` | 148 | ParticipantState dataclass, MultiRuntimeContext, build_context() |
| `apps/engine/engine_v2.py` | 202 | CLI entry point + execute() + print_summary() |
| `apps/engine/scenarios_v2/test_niuniu_sevraya_orbit.json` | 24 | 2-participant canon orbit |
| `apps/engine/scenarios_v2/test_sevraya_zero_surface.json` | 24 | 2-participant co-consciousness |
| `apps/engine/scenarios_v2/test_niuniu_sevraya_zero_proximity.json` | 27 | 3-participant complex proximity |

## Validation Results

### Test 1: NiuNiu + Sevraya (2 participants)

```
Verdict: STRUCTURE_VALID ✅
Participants: niuniu (Stage 4, Shadow Logic bearer, 5 defenses, 7 triggers)
              sevraya (Stage 6, Tidal Memory shared, 5 defenses, 6 triggers)
Relationships: niuniu↔sevraya (symmetric orbital constant)
Schema: both PASS
```

### Test 2: Sevraya + Zero (2 participants, shared body)

```
Verdict: STRUCTURE_VALID ✅
Participants: sevraya (Stage 6, Tidal Memory shared)
              zero (Stage 6, Tidal Memory shared)
Relationships: sevraya↔zero (asymmetric — Zero documents Sevraya as host; Sevraya has no relationship_interfaces entry for Zero)
Schema: both PASS
Note: asymmetry is expected — Sevraya's relationship to Zero is documented in somatic_signature.shared_with, not relationship_interfaces.
```

### Test 3: NiuNiu + Sevraya + Zero (3 participants)

```
Verdict: STRUCTURE_VALID ✅
Participants: 3
Relationships detected: 3 pairs
  - niuniu↔sevraya: symmetric (orbital constant)
  - niuniu↔zero: asymmetric (Zero→NiuNiu documented; NiuNiu→Zero undocumented)
  - sevraya↔zero: asymmetric (Zero→Sevraya documented; Sevraya→Zero undocumented)
Schema: all 3 PASS
Totals: 13 defenses, 18 triggers, 17 relationships, 19 forbidden behaviors, 148 evidence claims
```

## Key Architecture Decisions

### 1. Separated library from entry point
`lib/loader.py` + `lib/context.py` can be imported by the Narrative Compiler (Phase 4) without coupling to the CLI.

### 2. Voice grammar resolution is character-aware
NiuNiu's pre/post-restoration split is detected and resolved based on `pre_chain` flag and evolution stage. Other characters use flat voice grammar.

### 3. Relationship detection is bidirectional
Engine checks both directions of `relationship_interfaces`. Asymmetry is documented, not treated as error.

### 4. Schema validation is lightweight
Validates required fields from RUNTIME_SCHEMA_V2.1.json but does NOT run full JSON Schema validation (too heavy for every run). Missing fields reported as warnings, not blockers.

### 5. CLI supports both human and machine output
Default: formatted summary. `--json`: raw JSON for pipeline consumption.

## CLI Usage

```bash
# Human-readable summary
python apps/engine/engine_v2.py scenarios_v2/test_niuniu_sevraya_orbit.json

# Machine-readable JSON
python apps/engine/engine_v2.py scenarios_v2/test_niuniu_sevraya_zero_proximity.json --json

# Library import
from engine_v2 import execute
result = execute("scenarios_v2/test_niuniu_sevraya_orbit.json")
```

## What Phase 1 Does NOT Do

- ❌ Constraint evaluation (defense triggers, forbidden behaviors)
- ❌ Contract generation + evaluation
- ❌ Canon scoring
- ❌ Conflict detection
- ❌ Allowed action space generation
- ❌ LLM integration

## Next: Phase 2 — Constraint Evaluation Core

Implement:
1. Deterministic trigger matching (`match_trigger_to_context()`)
2. Structured forbidden behavior evaluation
3. Identity invariant checking
4. Contract evaluation (replacing hardcoded keyword matching)

Files to modify: `lib/context.py` (add constraint modules), `engine_v2.py` (add evaluation pipeline steps).
