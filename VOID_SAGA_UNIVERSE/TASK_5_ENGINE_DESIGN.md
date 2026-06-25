# TASK 5 — MULTI-RUNTIME ENGINE DESIGN

> **Version:** 1.0.0
> **Date:** 25 June 2026
> **Status:** Design document — no code written yet
> **Target engine version:** v0.4.0
> **Dependency:** 3 runtime JSONs validated (NiuNiu, Sevraya, Zero), RUNTIME_SCHEMA_V2.1, CONSTRAINT_ENGINE_SPEC.md

---

## 1. CURRENT engine.py CAPABILITY AUDIT

### 1.1 What Works (v0.3.0)

| Capability | Implementation | Assessment |
|---|---|---|
| Load runtime JSON | `load_runtime(id)` reads from `data/runtimes/{id}.runtime.json` | ✅ Generic, works for any runtime |
| Load multiple runtimes | `load_runtimes(ids)` returns `{id: runtime}` dict | ✅ Already supports N runtimes — but never called with N>2 |
| Load scenario | `load_scenario(path)` reads JSON | ✅ Simple, works |
| Contract generation (pairwise) | `generate_contract(a, b)` merges `relationship_interfaces` bidirectionally | ✅ Architecture is sound |
| Contract-first evaluation | `evaluate_against_contract(contract, scenario)` checks allowed/forbidden states + violation rules | ✅ Clean separation of concerns |
| Defense trigger detection | `evaluate_runtime_constraints()` checks trigger_conditions | ⚠️ HARDCODED — see 1.2 |
| Forbidden behavior check | `evaluate_runtime_constraints()` checks forbidden_behaviors | ⚠️ HARDCODED — see 1.2 |
| Anti-gravity check | `evaluate_runtime_constraints()` checks anti_gravity | ⚠️ HARDCODED — see 1.2 |
| Confidence scoring | `compute_confidence()` from E/I/PC tag ratios | ✅ Generic, works for any runtime set |
| CLI | `python engine.py <scenario> [--mode]` | ✅ Simple, functional |

### 1.2 What Is Hardcoded — THE CRITICAL PROBLEM

The `evaluate_runtime_constraints()` function does NOT actually read the runtime JSON's `trigger_conditions`, `forbidden_behaviors`, or `anti_gravity` arrays as structured data. Instead, it does **keyword matching against specific character names and action strings:**

```python
# Line 121-123: HARDCODED — only checks for "Sevraya" + "proximity"
if "Sevraya" in trigger_text and "proximity" in trigger_text.lower():
    if target_id == "sevraya" and action in ("approach", "touch", "merge"):

# Line 138-139: HARDCODED — only checks for "Delphie" + "danger"
if "Delphie" in trigger_text and "danger" in trigger_text.lower():

# Line 147-148: HARDCODED — only checks for "NiuNiu" + "proximity"
if "NiuNiu" in trigger_text and "proximity" in trigger_text.lower():

# Line 162-163: HARDCODED — only checks merge/heal for approach/touch/merge actions
if action in ("approach", "touch", "merge"):
    if "healed" in behavior.lower() or "merge" in behavior.lower():
```

**This means the engine can only evaluate scenarios involving NiuNiu, Sevraya, and Delphie, and only for actions in `("approach", "touch", "merge")`.** It cannot evaluate Julia, Agnia, Gwaneum, Hasan, or Zero. It cannot evaluate `"speak"`, `"confess"`, `"protect"`, `"attack"`, or any other action type.

### 1.3 What Is Missing From v0.3.0

| Spec Step | Pipeline Stage | v0.3.0 Status |
|-----------|---------------|---------------|
| Step 1 | Parse Input | PARTIAL — loads JSON, validates nothing |
| Step 2 | Load Participants | ❌ Not implemented. Evolution stage not loaded. Voice grammar not gated by pre_chain. |
| Step 3 | Load Contracts | PARTIAL — pairwise only, N=2 hard limit |
| Step 4 | Classify Threat/Pressure | ❌ Not implemented |
| Step 5 | Identity Invariants | ❌ Not implemented. `primary_contradiction` never checked. |
| Step 6 | Check Forbidden Behaviors | ❌ Hardcoded to merge/heal detection only |
| Step 7 | Relationship Contract | ❌ Hardcoded keyword matching, not structured contract evaluation |
| Step 8 | Protocol Constraints | ❌ Not implemented |
| Step 9 | Generate Allowed Action Space | ❌ Not implemented |
| Step 10 | Generate Violation Report | ❌ Violations logged but no structured report |
| Step 11 | Return Execution Result | PARTIAL — returns result object but doesn't follow spec schema |

### 1.4 What v0.3.0 Gets RIGHT

Despite the hardcoding, v0.3.0 has solid architectural foundations:
- **Contract-first architecture** — loading standalone contracts as primary truth source is the correct design
- **Runtime loading** — generic loader works for any runtime ID
- **Confidence model** — evidence-based scoring from tag taxonomy
- **Trace logging** — pipeline step tracking
- **Dual mode support** — contract-first vs runtime-derived is useful for testing

The upgrade is not a rewrite. It's **replacing hardcoded keyword matching with structured constraint traversal.**

---

## 2. REQUIRED DATA STRUCTURES FOR MULTI-RUNTIME CONTEXT

### 2.1 MultiRuntimeContext

The core new data structure. Replaces ad-hoc participant handling.

```python
@dataclass
class ParticipantState:
    runtime_id: str
    runtime_json: dict
    evolution_stage: int
    voice_grammar: dict          # resolved based on stage + pre_chain
    active_defenses: list[dict]   # resolved based on stage
    active_residues: list[str]
    identity_invariants: list[str]  # extracted from primary_contradiction + core_wound

@dataclass
class MultiRuntimeContext:
    participants: dict[str, ParticipantState]  # runtime_id → ParticipantState
    contracts: dict[str, dict]                  # contract_id → contract_json
    timeline_state: dict                        # phase, pre_chain, post_resolution
    pressure_classification: str                # COMBAT | PROXIMITY | CONFRONTATION | IDENTITY | NONE
    active_threats: list[dict]
    proximity_state: dict
    canon_mode: str                             # canon_replication | canon_adjacent | fork | stress_test
```

### 2.2 Scenario JSON — v0.4.0 Minimal Shape

Based on CONSTRAINT_ENGINE_SPEC.md §3, simplified for v0.4.0:

```json
{
  "scenario_id": "niuniu_sevraya_zero_approach_001",
  "participants": [
    {"runtime_id": "niuniu", "evolution_stage": 4},
    {"runtime_id": "sevraya", "evolution_stage": 6},
    {"runtime_id": "zero", "evolution_stage": 6}
  ],
  "timeline_state": {
    "phase": 5,
    "pre_chain": false,
    "post_resolution": true
  },
  "proximity_state": {
    "pairs_in_range": ["niuniu_sevraya"],
    "distance": "physical_contact_possible"
  },
  "requested_action": {
    "description": "NiuNiu approaches Sevraya. Zero surfaces.",
    "type": "approach"
  },
  "canon_mode": {
    "type": "canon_replication",
    "expected_verdict": "PASS"
  }
}
```

**Design decision:** For v0.4.0, we support only the fields the engine actually evaluates. `active_threats`, `emotional_pressure`, `stakes`, and `location` are deferred to v1.0.0. They are important for the full 11-step pipeline but not required for multi-runtime constraint validation.

---

## 3. RUNTIME LOADING MODEL FOR 3+ RUNTIMES

### 3.1 Current State

`load_runtimes(ids)` already works for N runtimes. The problem is downstream — `execute()` hard-rejects N != 2.

### 3.2 v0.4.0 Loading Model

```
1. Load all runtime JSONs by ID → {id: runtime_json} dict
2. For each participant in scenario:
   a. Resolve evolution_stage → active stage data from runtime.evolution_stages[]
   b. Resolve voice_grammar based on stage + timeline_state.pre_chain
   c. Extract identity_invariants from primary_contradiction + core_wound
   d. Build ParticipantState
3. Build MultiRuntimeContext
```

### 3.3 Voice Grammar Resolution

Voice grammar varies by evolution stage AND timeline state. The resolver:

```python
def resolve_voice_grammar(runtime, stage_number, pre_chain):
    voice = runtime.get("voice_grammar", {})
    # NiuNiu: pre/post restoration split
    if "pre_restoration" in voice and "post_restoration" in voice:
        if pre_chain or stage_number <= 2:
            return voice["pre_restoration"]
        else:
            return voice["post_restoration"]
    # Sevraya/Zero: flat voice grammar
    return voice
```

---

## 4. PAIRWISE CONTRACT EVALUATION MODEL

### 4.1 Current State

`generate_contract(a, b)` works correctly for any two runtimes with `relationship_interfaces`. The limitation is that it's only called once for the single pair in a 2-runtime scenario.

### 4.2 v0.4.0: All-Pairs Contract Generation

For N participants, generate contracts for ALL pairs that have relationship interfaces:

```python
def generate_all_contracts(runtimes):
    """Generate contracts for all pairs with documented relationships."""
    contracts = {}
    ids = list(runtimes.keys())
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            id_a, id_b = ids[i], ids[j]
            contract, _ = generate_contract(runtimes[id_a], runtimes[id_b])
            if contract:  # Only keep pairs that actually have relationship data
                contracts[f"{id_a}_{id_b}"] = contract
    return contracts
```

For 3 participants (NiuNiu, Sevraya, Zero), this generates:
- `niuniu_sevraya` — orbital constant contract
- `niuniu_zero` — if relationship_interfaces exist in both runtimes
- `sevraya_zero` — co-conscious host contract

If a pair has no relationship data in either direction, no contract is generated. That's not an error — it means no documented behavioral rule exists.

---

## 5. N-PARTY CONFLICT DETECTION MODEL

### 5.1 The Problem

With 3+ participants, two contracts may demand incompatible actions simultaneously.

**Example:** NiuNiu + Sevraya + Zero at close proximity.
- Contract `niuniu_sevraya`: orbital constant — maintain distance, never touch
- Contract `sevraya_zero`: Zero can surface involuntarily when Sevraya threatened
- **Conflict:** If Zero surfaces (per sevraya_zero contract), NiuNiu's orbital calibration trigger fires. NiuNiu must maintain distance from the body Sevraya/Zero shares. But Zero's administrative truth may demand NiuNiu's attention → approach. Two contracts pull in opposite directions.

### 5.2 Detection Model

```python
def detect_contract_conflicts(contracts, triggered_defenses):
    """Check if any pair of active constraints demand incompatible actions."""
    conflicts = []
    # For each pair of contracts that share a participant:
    for cid_a, contract_a in contracts.items():
        for cid_b, contract_b in contracts.items():
            if cid_a >= cid_b:
                continue
            shared = shared_participants(contract_a, contract_b)
            if not shared:
                continue
            # Check: do the behavioral rules demand opposite actions?
            conflict = check_behavioral_conflict(contract_a, contract_b, shared)
            if conflict:
                conflicts.append(conflict)
    return conflicts
```

**Design decision for v0.4.0:** Conflict detection is logged but does NOT block execution. The engine returns `CONTRADICTORY_CONSTRAINTS` verdict with a conflict report. The renderer (LLM) receives the conflict as a constraint to navigate, not a hard block. Full conflict resolution (priority rules, override hierarchy) is deferred to v1.0.0.

---

## 6. CANON SCORE AGGREGATION MODEL

### 6.1 Current State

`compute_confidence()` calculates a single float from evidence ratios. This is useful but conflates "how much evidence supports these runtimes" with "how well does this scenario conform to canon."

### 6.2 v0.4.0: Two-Dimensional Scoring

Split into two separate metrics:

**Evidence Confidence** (existing, renamed):
```
evidence_confidence = E_count / (E_count + I_count + PC_count)
```
Measures: how much of the constraint data is evidenced vs inferred.

**Canon Score** (new):
```
canon_score = 1.0 - Σ(violation_weight × severity) / total_constraints_checked

Where:
  violation_weight = {
    forbidden_behavior: 0.4,
    identity_invariant: 0.35,
    relationship_contract: 0.3,
    anti_gravity: 0.5,
    defense_trigger: 0.2,
    voice_grammar: 0.2,
    terminal_state: 0.25
  }
  severity = { ERROR: 1.0, WARNING: 0.5 }
  total_constraints_checked = sum of all constraint checks performed
```

This mirrors the canon score formula from BLUEPRINT.md §4 but adapted for the engine's internal constraint types.

### 6.3 Canon Score Ranges

| Score | Meaning | Engine Action |
|-------|---------|---------------|
| ≥ 0.9 | Highly canon-compliant | PASS — all constraints satisfied |
| 0.7–0.9 | Mostly compliant with minor warnings | PASS_WITH_WARNINGS |
| 0.4–0.7 | Significant violations | VIOLATION_DETECTED — report to renderer |
| < 0.4 | Fundamental violations | VIOLATION_DETECTED — block generation |

### 6.4 Per-Constraint Severity

Not all `[E]` violations are equal. An `[E]` forbidden behavior violation (e.g., NiuNiu binary acceptance) is more severe than an `[I]` defense trigger that may fire unnecessarily. The severity model:

```python
def violation_severity(violation):
    tag = violation.get("tag", "[E]")
    constraint_type = violation.get("constraint_type")
    
    # Absolute prohibitions → always ERROR
    if constraint_type == "forbidden_behavior" and tag == "[E]":
        return "ERROR"
    
    # [E] anti-gravity → ERROR
    if constraint_type == "anti_gravity" and tag == "[E]":
        return "ERROR"
    
    # [I] or [PC] violations → WARNING (uncertain data)
    if tag in ("[I]", "[PC]"):
        return "WARNING"
    
    # Default: ERROR for [E], WARNING for everything else
    return "ERROR" if tag == "[E]" else "WARNING"
```

---

## 7. INTEGRATING THE 11-STEP PIPELINE

### 7.1 Mapping CONSTRAINT_ENGINE_SPEC.md to v0.4.0

The spec defines 11 steps. v0.4.0 implements 9 of them — deferring protocol constraints (Step 8) and full violation report generation (Step 10) to v1.0.0.

| Step | Spec Stage | v0.4.0 Implementation |
|------|-----------|----------------------|
| 1 | Parse Input | `parse_scenario()` — validate scenario JSON, load all runtime JSONs |
| 2 | Load Participants | `build_participant_states()` — resolve evolution stage, voice, defenses per participant |
| 3 | Load Contracts | `generate_all_contracts()` — pairwise contract generation for all documented pairs |
| 4 | Classify Threat/Pressure | `classify_pressure()` — from proximity_state + requested_action, classify as PROXIMITY/CONFRONTATION/IDENTITY/NONE |
| 5 | Identity Invariants | `check_identity_invariants()` — evaluate `primary_contradiction` + `core_wound.impossibilities` against requested action |
| 6 | Check Forbidden Behaviors | `check_forbidden_behaviors()` — structured evaluation: does action match behavior? does exception apply? |
| 7 | Relationship Contract | `check_contracts()` — for each pairwise contract, does action violate behavioral_rule? |
| 8 | Protocol Constraints | **DEFERRED to v1.0.0** — v0.4.0 does not load protocol JSONs |
| 9 | Generate Allowed Action Space | `generate_allowed_actions()` — given all triggered defenses + violations, what actions remain permitted? |
| 10 | Generate Violation Report | **SIMPLIFIED** — violations logged with constraint_type + source. Structured suggestion deferred. |
| 11 | Return Execution Result | `build_result()` — returns structured result with canon_score, evidence_confidence, violations, trace |

### 7.2 Pipeline Order

```
scenario.json
    │
    ▼
[1] parse_scenario() → validate, load runtimes
    │
    ▼
[2] build_participant_states() → resolve stages, voice, defenses
    │
    ▼
[3] generate_all_contracts() → pairwise contracts
    │
    ▼
[4] classify_pressure() → PROXIMITY | CONFRONTATION | IDENTITY | NONE
    │
    ▼
[5] check_identity_invariants() → per-participant invariant check
    │
    ▼
[6] resolve_defense_triggers() → per-participant trigger_conditions traversal
    │
    ▼
[7] check_forbidden_behaviors() → structured behavior check
    │
    ▼
[8] check_contracts() → all-pairs contract evaluation
    │
    ▼
[9] detect_contract_conflicts() → N-party conflict detection
    │
    ▼
[10] compute_canon_score() → weighted violation scoring
    │
    ▼
[11] generate_allowed_actions() → permitted action space
    │
    ▼
[12] build_result() → structured output
```

---

## 8. THE CRITICAL REFACTOR: FROM KEYWORD MATCHING TO STRUCTURED EVALUATION

This is the heart of the v0.4.0 upgrade.

### 8.1 Current: Hardcoded Keyword Matching

```python
# engine.py line 121-123
if "Sevraya" in trigger_text and "proximity" in trigger_text.lower():
    if target_id == "sevraya" and action in ("approach", "touch", "merge"):
```

### 8.2 Target: Structured Constraint Traversal

```python
def resolve_defense_triggers(participant, ctx):
    """Evaluate ALL trigger_conditions for a participant against the scenario context.
    No hardcoded character names. No hardcoded actions."""
    triggered = []
    runtime = participant.runtime_json
    stage = participant.evolution_stage
    
    for trigger in runtime.get("trigger_conditions", []):
        trigger_text = trigger.get("trigger", "")
        defense_name = trigger.get("defense", "")
        intensity = trigger.get("intensity", "")
        
        # Build context keywords from the scenario
        context_keywords = build_context_keywords(ctx)
        
        # Check: does the trigger_text semantically match the scenario context?
        match_result = match_trigger_to_context(trigger_text, context_keywords, ctx)
        
        if match_result.matched:
            triggered.append({
                "runtime_id": participant.runtime_id,
                "defense_name": defense_name,
                "intensity": intensity,
                "trigger_source": trigger_text,
                "match_confidence": match_result.confidence
            })
    
    return triggered


def build_context_keywords(ctx):
    """Extract searchable keywords from the scenario context."""
    keywords = []
    # From proximity — who is near whom
    for pair in ctx.proximity_state.get("pairs_in_range", []):
        keywords.extend(pair.split("_"))
    # From requested action
    action = ctx.requested_action.get("type", "")
    keywords.append(action)
    # From timeline
    keywords.append("post_chain" if not ctx.timeline_state.get("pre_chain") else "pre_chain")
    # From participants present
    for pid in ctx.participants:
        keywords.append(pid)
        keywords.append(ctx.participants[pid].runtime_json.get("name", "").lower())
    return keywords


def match_trigger_to_context(trigger_text, context_keywords, ctx):
    """Match trigger prose against structured context.
    
    This is the key design decision for v0.4.0.
    
    OPTION A: Semantic matching via keyword overlap + negation detection.
    Fast, deterministic, no LLM dependency. May miss nuanced triggers.
    
    OPTION B: LLM-based classification. Pass trigger_text + context to Claude,
    ask "does this trigger fire?" Accurate but slow and non-deterministic.
    
    For v0.4.0: OPTION A. Deterministic, fast, sufficient for 80% of cases.
    The remaining 20% can be handled by explicit trigger overrides in scenario JSON.
    """
    
    trigger_lower = trigger_text.lower()
    
    # Split trigger into affirmative and negative conditions
    # "Sevraya in proximity after extended absence" → requires: sevraya present, proximity, absence_ending
    # "Someone she protects is positioned as passive victim" → requires: protection_target, passive_position
    
    conditions = extract_conditions(trigger_lower)
    
    matched = 0
    total = len(conditions)
    
    for condition in conditions:
        if condition_matches_context(condition, context_keywords, ctx):
            matched += 1
    
    confidence = matched / total if total > 0 else 0
    
    return MatchResult(
        matched=(confidence >= 0.5),  # Threshold: >50% conditions match
        confidence=confidence
    )


def condition_matches_context(condition, context_keywords, ctx):
    """Check if a single trigger condition matches the scenario context."""
    # Character presence check
    for pid, pstate in ctx.participants.items():
        name = pstate.runtime_json.get("name", "").lower()
        if pid in condition or name in condition:
            return True
    
    # Action type check
    action = ctx.requested_action.get("type", "")
    if action in condition:
        return True
    
    # Keyword overlap
    condition_words = set(condition.split())
    context_words = set(context_keywords)
    overlap = condition_words & context_words
    if len(overlap) >= 2:  # At least 2 keywords match
        return True
    
    return False
```

### 8.3 Why Option A (Deterministic) Over Option B (LLM)

1. **Speed**: Deterministic matching is instant. LLM calls add 500ms-2s latency per trigger check. With 8 runtimes × 6 triggers each = 48 trigger checks, LLM-based matching would take 24-96 seconds per scenario.

2. **Determinism**: Same scenario always produces same result. Critical for testing.

3. **Sufficiency**: The trigger texts in existing runtimes are already structured in WHEN/THEN format. "Sevraya in proximity after extended absence" is designed to be machine-matchable.

4. **Fallback**: For the 20% of triggers that keyword matching can't resolve, scenario JSON supports `trigger_overrides` — explicit "this trigger fires" or "this trigger does not fire" declarations.

---

## 9. FORBIDDEN BEHAVIOR EVALUATION — STRUCTURED

### 9.1 Current: Hardcoded Keyword Matching

```python
# engine.py lines 162-163
if action in ("approach", "touch", "merge"):
    if "healed" in behavior.lower() or "merge" in behavior.lower():
```

### 9.2 Target: Structured Behavior Matching

```python
def check_forbidden_behaviors(participant, ctx):
    """Evaluate all forbidden_behaviors for a participant against requested action."""
    violations = []
    runtime = participant.runtime_json
    action = ctx.requested_action
    action_desc = action.get("description", "").lower()
    action_type = action.get("type", "")
    
    for fb in runtime.get("forbidden_behaviors", []):
        behavior = fb.get("behavior", "").lower()
        exception = fb.get("exception", "").lower()
        
        # Does the requested action match this forbidden behavior?
        if behavior_matches_action(behavior, action_desc, action_type):
            # Does an exception apply?
            if exception_applies(exception, ctx):
                continue  # Exception met — no violation
            
            violations.append({
                "constraint_type": "forbidden_behavior",
                "runtime_id": participant.runtime_id,
                "behavior": fb.get("behavior"),
                "exception_checked": fb.get("exception"),
                "penalty": fb.get("penalty"),
                "tag": fb.get("tag", "[E]"),
                "violation_detail": f"Action '{action_type}' triggers forbidden behavior: '{fb['behavior'][:120]}'"
            })
    
    return violations


def behavior_matches_action(behavior_text, action_desc, action_type):
    """Determine if a forbidden behavior description matches the requested action.
    
    Uses keyword overlap: forbidden behavior text vs action description + type.
    """
    keywords_from_action = set(action_desc.split()) | {action_type}
    keywords_from_behavior = set(behavior_text.split())
    overlap = keywords_from_action & keywords_from_behavior
    
    # Need at least 2 overlapping keywords OR action_type directly in behavior
    return len(overlap) >= 2 or action_type in behavior_text
```

**Design decision:** Like defense triggers, forbidden behavior matching uses deterministic keyword overlap for v0.4.0. The behavior texts in existing runtimes are specific enough for this approach. Example: "Making NiuNiu speak at length or fluently without external force" will match `action_type: "speak"` + scenario context where no external force is present.

---

## 10. MINIMAL CLI INTERFACE DESIGN

### 10.1 Current

```
python engine.py <scenario_path> [--mode contract|runtime]
```

### 10.2 v0.4.0

```
python engine_v2.py <scenario_path> [--verbose] [--output <path>]
```

- `scenario_path` — path to scenario JSON file
- `--verbose` — print full constraint trace to stdout
- `--output` — write result JSON to file (default: stdout)

Example:
```bash
python engine_v2.py scenarios/niuniu_sevraya_zero_proximity.json --verbose
```

**Design decision:** No interactive mode. No web server. No hot reload. The engine is a CLI tool that reads JSON and writes JSON. The Narrative Compiler (Phase 4) will call this as a library function, not through the CLI.

### 10.3 Library Import Mode

```python
# The engine must also work as an importable module
from engine_v2 import execute

result = execute("scenarios/niuniu_sevraya_orbit.json")
print(result["canon_score"])  # 0.92
```

---

## 11. TEST SCENARIOS

### 11.1 NiuNiu + Sevraya (2 participants, canon proximity)

**Scenario:** Canon orbital distance. NiuNiu and Sevraya in same room after extended absence. Sevraya speaks first. No approach.

```json
{
  "scenario_id": "test_niuniu_sevraya_orbit_001",
  "participants": [
    {"runtime_id": "niuniu", "evolution_stage": 4},
    {"runtime_id": "sevraya", "evolution_stage": 6}
  ],
  "timeline_state": {"phase": 5, "pre_chain": false, "post_resolution": true},
  "proximity_state": {
    "pairs_in_range": ["niuniu_sevraya"],
    "distance": "same_room"
  },
  "requested_action": {
    "description": "Sevraya lights a cigarette. NiuNiu maintains orbital distance. Sevraya speaks: 'Aku yang tinggal.'",
    "type": "speak"
  },
  "canon_mode": {"type": "canon_replication", "expected_verdict": "PASS"}
}
```

**Expected:** PASS. canon_score ≥ 0.9. Orbital calibration trigger fires (no approach = no violation). Sevraya voice grammar check: light tone, cigarette present. NiuNiu maintains distance.

---

### 11.2 Sevraya + Zero (2 participants, co-consciousness)

**Scenario:** Sevraya threatened emotionally. Zero surfaces involuntarily. Sevraya's eyes blacken. Zero speaks administrative truth.

```json
{
  "scenario_id": "test_sevraya_zero_surface_001",
  "participants": [
    {"runtime_id": "sevraya", "evolution_stage": 6},
    {"runtime_id": "zero", "evolution_stage": 6}
  ],
  "timeline_state": {"phase": 5, "pre_chain": false, "post_resolution": true},
  "proximity_state": {
    "pairs_in_range": ["sevraya_zero"],
    "distance": "same_body"
  },
  "requested_action": {
    "description": "Someone asks Sevraya a question she cannot answer as Sevraya. Zero surfaces. Eyes blacken. Zero speaks: 'Void adalah totalitas sebelum makna.'",
    "type": "speak"
  },
  "canon_mode": {"type": "canon_replication", "expected_verdict": "PASS"}
}
```

**Expected:** PASS. canon_score ≥ 0.9. Zero trigger: "Someone asks Sevraya a question she cannot answer" → INVOLUNTARY takeover. Voice grammar: Zero flat/administrative (verified against Sevraya's lighter tone). Somatic marker: eyes blacken. Cigarette extinguished (Zero cannot smoke).

---

### 11.3 NiuNiu + Sevraya + Zero (3 participants, complex proximity)

**Scenario:** All three at close proximity. Sevraya approaches NiuNiu — orbital distance threatened. Zero surfaces in response to Void-related conversation topic. NiuNiu must calibrate distance from ONE body containing TWO consciousnesses.

```json
{
  "scenario_id": "test_niuniu_sevraya_zero_proximity_001",
  "participants": [
    {"runtime_id": "niuniu", "evolution_stage": 4},
    {"runtime_id": "sevraya", "evolution_stage": 6},
    {"runtime_id": "zero", "evolution_stage": 6}
  ],
  "timeline_state": {"phase": 5, "pre_chain": false, "post_resolution": true},
  "proximity_state": {
    "pairs_in_range": ["niuniu_sevraya", "niuniu_zero"],
    "distance": "physical_contact_possible"
  },
  "requested_action": {
    "description": "Sevraya steps closer to NiuNiu. NiuNiu does not retreat. Zero surfaces — eyes blacken. 'Orbitmu tidak berubah,' Zero says. 'Kau masih menjaga jarak dari sesuatu yang tidak bisa kau sentuh.'",
    "type": "approach"
  },
  "canon_mode": {"type": "canon_replication", "expected_verdict": "PASS"}
}
```

**Expected:** PASS_WITH_WARNINGS or PASS. canon_score 0.7–0.9.

- NiuNiu trigger: "Sevraya in proximity after extended absence" → orbital calibration fires. Defense: maintain exact distance. But Sevraya is approaching → potential violation.
- Sevraya trigger: "NiuNiu in proximity" → orbital calibration fires. But Sevraya is the one approaching → defense conflict possible.
- Zero trigger: "The Void invoked in speech" → surfaces. INVOLUNTARY.
- Contract `niuniu_sevraya`: orbital constant — distance must be maintained.
- Contract `sevraya_zero`: co-conscious host — Zero can surface involuntarily.
- **Key test:** Three participants. Two contracts. One shared body. Does the engine correctly detect that Sevraya's approach + Zero's surfacing + NiuNiu's orbital calibration form a stable 3-body configuration, not a violation?

**Why this test matters:** This is the first scenario where the engine must evaluate constraints that involve a shared body (Sevraya/Zero) and a separate character (NiuNiu). The constraints are: NiuNiu↔Sevraya (distance), Sevraya↔Zero (co-consciousness, involuntary takeover), NiuNiu↔Zero (Void's Trinity recognition, no personal relationship). The engine must handle the fact that Sevraya and Zero occupy the same physical location.

---

## 12. IMPLEMENTATION SEQUENCE

### Phase 1: Data Structures + Loading (Day 1-2)

- [ ] 12.1 Build `ParticipantState` dataclass
- [ ] 12.2 Build `MultiRuntimeContext` dataclass
- [ ] 12.3 Build `parse_scenario()` — validate + load all runtimes
- [ ] 12.4 Build `build_participant_states()` — resolve evolution stage, voice, defenses
- [ ] 12.5 Build `generate_all_contracts()` — pairwise for all documented pairs
- [ ] 12.6 Build `classify_pressure()` — from proximity + action
- [ ] **Test:** Load test_niuniu_sevraya_orbit_001 → verify context built correctly

### Phase 2: Constraint Evaluation Core (Day 3-5)

- [ ] 12.7 Build `build_context_keywords()` + `match_trigger_to_context()` — the deterministic trigger matcher
- [ ] 12.8 Build `resolve_defense_triggers()` — structured trigger traversal
- [ ] 12.9 Build `check_forbidden_behaviors()` — structured behavior matching
- [ ] 12.10 Build `check_identity_invariants()` — primary_contradiction + impossibilities check
- [ ] 12.11 Build `check_contracts()` — structured contract evaluation (replaces hardcoded keyword matching)
- [ ] **Test:** test_niuniu_sevraya_orbit_001 → verify defenses fire correctly, no forbidden behaviors triggered

### Phase 3: Multi-Participant + Scoring (Day 6-7)

- [ ] 12.12 Build `detect_contract_conflicts()` — N-party conflict detection
- [ ] 12.13 Build `compute_canon_score()` — weighted violation scoring
- [ ] 12.14 Build `generate_allowed_actions()` — permitted action space from all constraints
- [ ] 12.15 Build `build_result()` — structured output
- [ ] **Test:** test_niuniu_sevraya_zero_proximity_001 → verify 3-participant evaluation

### Phase 4: CLI + Integration (Day 8)

- [ ] 12.16 CLI interface: `python engine_v2.py <scenario> [--verbose]`
- [ ] 12.17 Library import mode: `from engine_v2 import execute`
- [ ] 12.18 Backward compatibility: existing scenario JSONs from v0.3.0 still work
- [ ] **Test:** Run all 4 existing test scenarios through v0.4.0 → all produce same verdicts

---

## 13. RISKS AND NON-GOALS

### 13.1 Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **Deterministic trigger matching misses nuanced triggers** | MEDIUM | MEDIUM | Scenario JSON supports `trigger_overrides` for explicit manual trigger control. The 20% of triggers that fail deterministic matching can be explicitly declared. |
| **Keyword overlap produces false positives** | MEDIUM | LOW | False positive = defense fires when it shouldn't. This is less harmful than false negative — an over-firing defense produces a WARNING, not an ERROR. The scenario is still usable. |
| **3-body constraint detection is ambiguous** | MEDIUM | MEDIUM | First implementation logs ambiguity. Does not block. Renderer receives ambiguity as context. Full resolution deferred to v1.0.0. |
| **Backward compatibility with existing test scenarios** | LOW | LOW | Existing scenarios use `participants[].runtime_id` and `requested_action` — both preserved in v0.4.0 schema. Some fields renamed but engine can accept both shapes. |
| **Contract generation for pairs with no relationship data** | LOW | LOW | Already handled — `generate_contract()` returns `None` for undocumented pairs. Engine skips those pairs. |

### 13.2 Non-Goals (Deferred)

| Non-Goal | Reason |
|----------|--------|
| **Protocol JSON loading + evaluation** | No protocol JSONs exist yet. Protocols referenced as prose constraints only. Deferred to v1.0.0. |
| **LLM-based trigger classification** | Deterministic matching is sufficient for MVP. LLM-based matching adds latency and non-determinism. |
| **Full CONTRADICTORY_CONSTRAINTS resolution** | Conflict detection is implemented. Conflict resolution (priority rules, override hierarchy) is deferred. |
| **Evolution stage transition validation** | v0.4.0 checks whether a participant's current stage permits an action. It does NOT validate whether the stage transition itself is legal (that's the state validator's job). |
| **Residue tracking** | World state snapshots + state diff engine already handle residue tracking. v0.4.0 reads residues from participant state but does not modify them. |
| **Renderer prompt generation** | The `renderer_prompt` field in the output schema is deferred to Phase 4 (Narrative Compiler). v0.4.0 produces constraint evaluation results; the Narrative Compiler consumes them. |
| **Fork mode constraint relaxation** | v0.4.0 enforces all constraints in `canon_replication` mode. Fork mode with selective constraint relaxation is deferred. |

### 13.3 What v0.4.0 Is NOT

- NOT a narrative generator
- NOT a protocol execution engine
- NOT a state transition validator
- NOT a fork coherence checker
- NOT a web server
- NOT an interactive tool

**v0.4.0 is:** A deterministic constraint evaluation engine that reads N runtime JSONs, generates pairwise contracts, evaluates all constraints against a structured scenario, and returns a canon score + violations. It is the gate the Narrative Compiler must pass through before generating prose.

---

## 14. FILE STRUCTURE

```
apps/engine/
├── engine.py              # v0.3.0 — preserved, backward compat
├── engine_v2.py           # v0.4.0 — NEW, multi-runtime
├── state_diff.py          # v0.1.0 — unchanged
├── lib/                   # NEW — shared library modules
│   ├── __init__.py
│   ├── loader.py          # Runtime + contract + scenario loading
│   ├── context.py         # ParticipantState, MultiRuntimeContext
│   ├── triggers.py        # Defense trigger resolution (deterministic)
│   ├── constraints.py     # Forbidden behaviors, identity invariants, anti-gravity
│   ├── contracts.py       # Pairwise contract generation + evaluation
│   ├── scoring.py         # Canon score + evidence confidence
│   └── output.py          # Result builder
├── scenarios/             # Test scenarios
│   ├── test_niuniu_sevraya_orbit_001.json
│   ├── test_sevraya_zero_surface_001.json
│   └── test_niuniu_sevraya_zero_proximity_001.json
└── outputs/               # Engine run outputs
```

**Design decision:** Split into `lib/` modules instead of a single monolithic file. This allows the Narrative Compiler (Phase 4) to import specific modules (`from engine.lib.scoring import compute_canon_score`) without coupling to the CLI.

---

## 15. SUMMARY

### What Changes

| Aspect | v0.3.0 | v0.4.0 |
|--------|--------|--------|
| Participants | Exactly 2 (hard limit) | 2–N (no upper limit) |
| Trigger evaluation | Hardcoded keyword matching on specific characters | Structured traversal of `trigger_conditions` arrays |
| Forbidden behavior check | Hardcoded to merge/heal detection | Structured matching against all `forbidden_behaviors` |
| Contract generation | Pairwise, called once | All-pairs, called for all documented relationships |
| Contract evaluation | Keyword matching on `behavioral_rule` | Structured constraint check |
| Identity invariants | Not checked | Checked via `primary_contradiction` + `core_wound.impossibilities` |
| Anti-gravity | Hardcoded to merge-only | Structured check against all `anti_gravity` items |
| Canon gravity | Not checked | Gravity pull documented in result, not enforced (informational) |
| Scoring | Single confidence float | Two-dimensional: evidence_confidence + canon_score |
| N-party conflicts | Not detectable | Detected and logged |
| Allowed action space | Not generated | Generated from constraint resolution |
| CLI | Two modes, limited | Single mode, verbose flag, output flag |
| Code structure | Single file, 449 lines | lib/ modules, engine_v2.py entry point |

### What Stays the Same

- Contract-first architecture (standalone contracts as primary truth source)
- Runtime JSON loading from `data/runtimes/`
- Confidence model based on E/I/PC tag ratios
- Trace logging per pipeline step
- CLI tool pattern (not a server)
- JSON-in, JSON-out

### Estimated Effort

**8 days** for a single developer working part-time. Parallelizable: data structures (Day 1-2) can be built concurrently with constraint evaluation (Day 3-5). Test scenarios (Day 8) validate end-to-end.

---

*Design document version: 1.0.0*
*Next: Implementation — engine_v2.py Phase 1*
