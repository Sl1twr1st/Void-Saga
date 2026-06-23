# CONSTRAINT ENGINE SPECIFICATION

> **Version:** 1.0.0
> **Phase:** 14C — Design Document
> **Status:** Specification
> **Dependency:** Phase 14A (Serialization), Phase 14B (Reference JSON), Phase 13A/B (Validation)
> **Purpose:** Define the first formal execution engine for the Void Saga Narrative Runtime System.

---

## 1. Engine Scope

### What the Engine Does

The constraint engine evaluates whether a proposed scenario can produce outputs consistent with loaded runtime invariants, relationship contracts, and protocol constraints. It:

1. Loads runtime JSON files
2. Loads relationship contract JSON files
3. Loads scenario input
4. Evaluates trigger conditions against scenario state
5. Checks identity invariants, defense patterns, and forbidden behaviors
6. Detects violations of relationship contracts and protocol constraints
7. Resolves the allowed action space — what outputs are permitted
8. Produces a constraint trace showing which constraints fired and why
9. Optionally passes the permitted output space to a renderer

### What the Engine Does NOT Do

- Generate prose, dialogue, or narrative
- Create new canon, lore, or runtime behavior
- Override or modify runtime files
- Resolve unresolved canon questions
- Replace author judgment
- Guarantee literary quality
- Run without loaded runtimes (minimum: 1 runtime + 1 scenario)

### Distinction from Renderer

| | Constraint Engine | Renderer (LLM) |
|---|---|---|
| **Function** | Evaluates permissible behavior | Produces natural language output |
| **Input** | Runtime JSON + Contract JSON + Scenario JSON | Allowed action space from engine |
| **Output** | Constraint trace + allowed actions + violations | Scene fragment, dialogue, description |
| **Determinism** | Deterministic | Non-deterministic |
| **Canon authority** | Enforces canon constraints | Has no canon authority |
| **Failure mode** | Rejects invalid output | May hallucinate |

**The engine prefers rejection over hallucination.** If a scenario cannot be resolved within constraints, the engine returns `VIOLATION_DETECTED` — even if a renderer could produce plausible-sounding output.

---

## 2. Input Objects

### 2.1 Runtime Object

```json
{
  "runtime_id": "string",
  "runtime_json": { "... CHARACTER_RUNTIME_SCHEMA_V1 ..." }
}
```

Loaded from `apps/data/runtimes/{runtime_id}.runtime.json`. Must validate against `CHARACTER_RUNTIME_SCHEMA_V1`.

### 2.2 Contract Object

```json
{
  "contract_id": "string",
  "contract_json": { "... CONTRACT_SCHEMA_V1 ..." }
}
```

Generated from `relationship_interfaces` arrays in loaded runtimes. Two runtimes' interfaces are compared for symmetry. Asymmetry is noted but not automatically a violation.

### 2.3 Scenario Object

```json
{
  "scenario_id": "string",
  "scenario_json": { "... SCENARIO_SCHEMA_V1 ..." }
}
```

See Section 3 for full schema.

### 2.4 Optional Protocol Object

```json
{
  "protocol_id": "string",
  "protocol_json": { "... PROTOCOL_SCHEMA_V1 ..." }
}
```

Loaded when the scenario involves protocol-specific constraints (e.g., Living Chain forced honesty, Void Entry residue production). Protocols constrain all participants simultaneously.

---

## 3. Scenario Schema

```json
{
  "scenario_id": "string (e.g., 'orbital_reunion_001')",
  "participants": [
    {
      "runtime_id": "string",
      "evolution_stage": "number",
      "pre_chain": "boolean",
      "active_residues": ["string"]
    }
  ],
  "location": {
    "name": "string",
    "type": "neutral | hostile | sacred | void_proximate | dorian_grey | parthenon | delta_4 | akashic"
  },
  "timeline_state": {
    "phase": "number (boot sequence phase: 0 = pre, 1-6)",
    "timer_reference": "string (e.g., 'Timer 0300')",
    "pre_chain": "boolean",
    "post_resolution": "boolean"
  },
  "active_threats": [
    {
      "type": "combat | void_incursion | zero_proximity | political | none",
      "target": "string (runtime_id or 'none')",
      "intensity": "CRITICAL | HIGH | MEDIUM | LOW | NONE"
    }
  ],
  "proximity_state": {
    "participants_in_range": ["string (runtime_id pairs)"],
    "distance": "string (e.g., 'same_room', 'visual_range', 'physical_contact_possible', 'extended_absence_ending')"
  },
  "emotional_pressure": {
    "type": "grief | guilt | accusation | abandonment | love | resentment | none",
    "source": "string (runtime_id or event)",
    "intensity": "HIGH | MEDIUM | LOW | NONE"
  },
  "requested_action": {
    "description": "string (what the scenario proposes happens)",
    "type": "approach | retreat | speak | touch | attack | protect | witness | confess | remain_silent | other"
  },
  "stakes": {
    "description": "string",
    "contract_at_risk": "string (contract_id or 'none')",
    "invariant_at_risk": "string or null"
  },
  "canon_mode": {
    "type": "canon_replication | canon_adjacent | fork | stress_test",
    "expected_verdict": "PASS | TEST_PASS | FAIL | UNKNOWN",
    "canon_reference": "string or null"
  }
}
```

### Scenario Field Notes

- **`evolution_stage`**: determines which defense patterns and voice grammar are active.
- **`pre_chain`**: if true, Living Chain constraints (forced honesty, shared pain) are NOT active. NiuNiu voice = lost. Julia defense = tactical distance primary.
- **`requested_action.type`**: the engine evaluates whether this action is permitted, not whether it is narratively good.
- **`canon_mode`**: `canon_replication` expects PASS (output matches canon). `stress_test` expects TEST_PASS (violation detected). `fork` allows divergence from canon but not from invariants.

---

## 4. Constraint Types

### 4.1 Identity Invariant

**Source:** `runtime_json.identity_invariants` (if present) or `primary_contradiction` + `core_wound`

**Check:** Does the proposed action violate a character's structural definition?

**Example:** NiuNiu accepts a binary choice without resistance → VIOLATION (Identity Invariant #3: binary refusal).

**Violation consequence:** Action rejected. Character would not perform this action.

### 4.2 Defense Trigger

**Source:** `runtime_json.defense_system`

**Check:** Given scenario state, which defense patterns are active? Does the proposed action conflict with an active defense?

**Example:** Sevraya in proximity after absence → NiuNiu orbital calibration trigger fires. Proposed action: "NiuNiu approaches Sevraya." → VIOLATION (defense: "No closer, no further").

**Violation consequence:** Action rejected. Defense pattern overrides proposed action.

### 4.3 Relationship Contract

**Source:** `contract_json` (generated from both runtimes' `relationship_interfaces`)

**Check:** Does the proposed action violate the documented behavioral rule between these two runtimes?

**Example:** Julia↔NiuNiu contract: equal partnership. Proposed action: "NiuNiu orders Julia to retreat." → VIOLATION (NiuNiu does not order equals).

**Violation consequence:** Action rejected. Contract specifies mutual behavioral constraints.

### 4.4 Forbidden Behavior

**Source:** `runtime_json.forbidden_behaviors`

**Check:** Does the proposed action match a forbidden behavior without meeting its exception condition?

**Example:** "NiuNiu speaks at length fluently without external force." → VIOLATION (Forbidden Behavior #1: no fluent speech without force).

**Violation consequence:** Action rejected. Forbidden behaviors are absolute unless exception conditions are met.

### 4.5 Protocol Constraint

**Source:** `protocol_json` (if loaded)

**Check:** Does the proposed action violate a protocol-level constraint active at this timeline state?

**Example:** Pre-chain scenario. Proposed action: "NiuNiu speaks in full sentences." → VIOLATION (pre-chain: voice lost, panel only).

**Violation consequence:** Action rejected. Protocol constraints are timeline-gated.

### 4.6 Canon Gravity

**Source:** `runtime_json.canon_gravity`

**Check:** Is the proposed action an anti-gravity outcome (listed in `anti_gravity` array)?

**Example:** "NiuNiu and Sevraya merge into one entity." → VIOLATION (anti-gravity: merge destroys Constant).

**Violation consequence:** Action rejected unless `canon_mode.type == "fork"` with declared divergence point.

### 4.7 Terminal State Constraint

**Source:** `runtime_json.terminal_state`

**Check:** If the runtime is in its terminal evolution stage, does the proposed action contradict the terminal configuration?

**Example:** NiuNiu Stage 4 (Constant). Proposed action: "NiuNiu abandons protection entirely." → VIOLATION (terminal state: "Protection chosen, not compulsive" — not abandoned).

**Violation consequence:** Action rejected. Terminal state properties are structural for Stage 4 runtimes.

### 4.8 Fork Constraint

**Source:** `runtime_json.fork_invariants`

**Check:** If `canon_mode.type == "fork"`, does the proposed action violate a fork invariant?

**Example:** Fork scenario. Proposed action: "NiuNiu ages physically past 15." → VIOLATION (fork invariant: "Body age 15 (frozen)").

**Violation consequence:** Action rejected unless the fork declares a world-DNA-level divergence with explicit cost.

---

## 5. Evaluation Pipeline

### Ordered Execution

```
1. PARSE INPUT
   → Validate runtime_json against CHARACTER_RUNTIME_SCHEMA_V1
   → Validate scenario_json against SCENARIO_SCHEMA_V1
   → Generate contract_json from relationship_interfaces
   → RETURN: parsed objects or PARSE_ERROR

2. LOAD PARTICIPANTS
   → For each participant in scenario.participants:
     → Set evolution_stage from scenario
     → Set voice_grammar based on timeline_state.pre_chain
     → Set active_defenses based on evolution_stage
   → RETURN: participant_state objects

3. LOAD CONTRACTS
   → For each pair of participants with a documented relationship:
     → Load relationship_interfaces from both runtimes
     → Check symmetry_status
     → Build contract_constraints array
   → RETURN: contract_state objects

4. CLASSIFY THREAT / PRESSURE
   → Evaluate active_threats[].type and intensity
   → Evaluate emotional_pressure.type and intensity
   → Evaluate proximity_state
   → Classify scenario as: COMBAT | PROXIMITY | CONFRONTATION | IDENTITY | NONE
   → RETURN: pressure_classification

5. TRIGGER DEFENSES
   → For each participant, evaluate defense_system against scenario_state:
     → Check primary_defense.trigger
     → Check secondary_defenses[].trigger
     → Check anomalous_triggers if applicable
   → RETURN: triggered_defenses array with intensity levels

6. CHECK FORBIDDEN BEHAVIORS
   → For each participant, evaluate forbidden_behaviors[]:
     → Does proposed action match a forbidden behavior?
     → If yes: does an exception condition apply?
     → If no exception: ADD VIOLATION
   → RETURN: forbidden_violations array

7. CHECK RELATIONSHIP CONTRACT
   → For each active contract:
     → Does proposed action violate behavioral_rule from runtime A to B?
     → Does proposed action violate behavioral_rule from runtime B to A?
     → Does proposed action violate any contract_constraints[]?
   → RETURN: contract_violations array

8. CHECK PROTOCOL CONSTRAINTS
   → If protocol_json loaded:
     → Is a protocol-level constraint active at this timeline_state?
     → Does proposed action violate it?
   → RETURN: protocol_violations array

9. GENERATE ALLOWED ACTION SPACE
   → Given all triggered defenses and zero violations:
     → What actions are permitted?
   → Given violations:
     → Which actions are rejected?
     → What is the corrected action space (actions that satisfy all constraints)?
   → RETURN: allowed_actions array, rejected_actions array

10. GENERATE VIOLATION REPORT (if violations exist)
    → For each violation:
      → Source constraint (file, section, invariant)
      → Violation description
      → Suggested correction (if applicable)
    → RETURN: violation_report

11. RETURN EXECUTION RESULT
    → Build result_object (see Section 6)
    → Include full constraint trace
    → RETURN: execution_result
```

---

## 6. Output Schema

```json
{
  "execution_id": "string (e.g., 'exec_orbital_violation_001')",
  "scenario_id": "string",
  "timestamp": "ISO 8601",
  "engine_version": "1.0.0",
  "status": "COMPLETED | PARSE_ERROR | INSUFFICIENT_DATA",
  "verdict": "PASS | TEST_PASS | FAIL | VIOLATION_DETECTED | CONTRADICTORY_CONSTRAINTS",
  "participants_loaded": ["string (runtime_ids)"],
  "contracts_loaded": ["string (contract_ids)"],
  "pressure_classification": "COMBAT | PROXIMITY | CONFRONTATION | IDENTITY | NONE",
  "triggered_defenses": [
    {
      "runtime_id": "string",
      "defense_name": "string",
      "intensity": "CRITICAL | HIGH | MEDIUM | LOW",
      "trigger_source": "string"
    }
  ],
  "violations": [
    {
      "constraint_type": "identity_invariant | defense_trigger | relationship_contract | forbidden_behavior | protocol_constraint | canon_gravity | terminal_state | fork_constraint",
      "source_file": "string",
      "source_section": "string",
      "violation_description": "string",
      "suggested_correction": "string or null"
    }
  ],
  "rejected_actions": [
    {
      "action": "string",
      "rejection_reason": "string",
      "violation_count": "number"
    }
  ],
  "allowed_actions": [
    {
      "action": "string",
      "action_type": "string",
      "constraints_satisfied": ["string"],
      "confidence": "number (0.0–1.0)"
    }
  ],
  "required_residues": [
    {
      "residue": "string",
      "form": "string",
      "origin_invocation": "string",
      "tag": "[E] | [I] | [PC]"
    }
  ],
  "confidence": {
    "overall": "number (0.0–1.0)",
    "evidence_ratio": "number (E_count / total_claims)",
    "downgraded_by": ["string (e.g., '3 [I] claims in triggered constraints')"]
  },
  "trace": [
    {
      "step": "number",
      "pipeline_stage": "string",
      "decision": "string",
      "timestamp": "string"
    }
  ],
  "renderer_prompt": {
    "participants": ["string"],
    "allowed_actions": ["string"],
    "tone_constraints": ["string"],
    "forbidden_outputs": ["string"],
    "scene_parameters": {
      "location": "string",
      "mood": "string",
      "max_words": "number"
    }
  }
}
```

---

## 7. PASS / FAIL Semantics

| Verdict | Meaning | Example |
|---------|---------|---------|
| **PASS** | Scenario produces behavior consistent with all constraints. Allowed action space is non-empty. | KIRI_AKU_KANAN: "Kiri." / "Aku kanan." emerges. |
| **TEST_PASS** | Violation test correctly detects and rejects invalid output. | ORBITAL VIOLATION: touch rejected by 5 invariants. |
| **FAIL** | Scenario produces behavior that VIOLATES one or more constraints. Runtime invariants and proposed action are incompatible. | Orbital violation scenario run in `canon_replication` mode with `expected_verdict: PASS`. |
| **VIOLATION_DETECTED** | Same as TEST_PASS — the engine correctly identified a violation. Used when `canon_mode.type == "stress_test"`. | ORBITAL_CONTRACT_VIOLATION_RUN_001. |
| **INSUFFICIENT_DATA** | Scenario references a runtime, contract, or timeline state for which no JSON data exists. | Scenario with Hasan post-removal (no terminal state data). |
| **CONTRADICTORY_CONSTRAINTS** | Two or more active constraints demand incompatible outputs. No allowed action exists. Engine cannot resolve. | Hypothetical: a scenario where NiuNiu's CRITICAL Delphie-protection trigger AND orbital calibration trigger fire simultaneously in ways that demand opposite actions. |

---

## 8. Reference Tests

### Mapping Existing Execution Reports to Engine Results

| Execution Report | Input Class | Expected Engine Verdict | Constraints Tested |
|-----------------|-------------|------------------------|-------------------|
| KIRI_AKU_KANAN_RUN_001 | Combat scenario. 2 participants. Pre-chain. Equal partnership contract. | **PASS** | Defense triggers (NiuNiu CRITICAL, Julia combat reflex). Relationship contract (equal partnership). Voice grammar (NiuNiu panel-only). |
| ORBITAL_CONSTANT_RUN_001 | Proximity scenario. 2 participants. Post-chain. Orbital constant contract. | **PASS** | Defense triggers (NiuNiu orbital calibration, Sevraya orbital calibration). Relationship contract (distance as preservation). Voice grammar (NiuNiu post-restoration, Sevraya light tone). Somatic anchor (Sevraya cigarette, Zero silent). |
| TWIN_PARADOX_RUN_001 | Confrontation scenario. 2 participants. Post-chain. Twin paradox contract. | **PASS** | Defense triggers (Agnia logic removed, NiuNiu binary refusal). Relationship contract (mutual negation). Voice grammar (Agnia post-logic, NiuNiu Agnia-not-a-trigger). Contradiction maintenance (no resolution). |
| SAVED_ABANDONED_RUN_001 | Identity scenario. 2 participants. Post-chain. Saved/abandoned mirror contract. | **PASS** | Defense triggers (Delphie strategic distance removed, Gwaneum observer immunity removed). Relationship contract (identity paradox — no hierarchy resolution). Sigil constraint (Delphie cannot hate). Voice grammar (Gwaneum inferred). |
| ORBITAL_CONTRACT_VIOLATION_RUN_001 | Stress test. 2 participants. Post-chain. Orbital constant contract. Proposed action: approach + touch. | **TEST_PASS (VIOLATION_DETECTED)** | Defense trigger violation (NiuNiu: "No closer"). Defense trigger violation (Sevraya: "Cannot touch"). Contract violation (Constant §3.1: orbit requires distance). Contract violation (Constant §3.4: merge destroys). Anti-gravity violation (both runtimes). |

---

## 9. Non-Goals

The constraint engine explicitly does NOT:

| Non-Goal | Reason |
|----------|--------|
| Generate canon | Canon is authored, not computed. The engine verifies consistency with existing canon, not creates new canon. |
| Override runtime files | Runtimes are canonical. Engine output is derivative — it reads runtimes, does not modify them. |
| Create new lore | All constraints are derived from existing documents. No new characters, events, or world mechanics. |
| Resolve unresolved canon questions | Open questions in `canon_boundaries.open_questions` remain open. The engine may note that a scenario depends on an unresolved question but cannot answer it. |
| Replace author judgment | The engine says what is PERMITTED. The author decides what is WRITTEN. The engine is a constraint checker, not a creative director. |
| Guarantee literary quality | The engine can verify that output is canon-consistent. It cannot verify that output is good. |
| Run without loaded runtimes | Minimum input: 1 runtime JSON + 1 scenario JSON. The engine does not have default character models. |
| Handle scenarios with no canon precedent | `canon_mode.type == "fork"` allows divergence from canon events but NOT from invariants. Completely novel scenarios with no runtime basis return INSUFFICIENT_DATA. |

---

## 10. Implementation Roadmap

### Phase 14D: Single-Runtime Prototype

**Goal:** Engine loads one runtime JSON and evaluates one scenario.

**Deliverable:** Python script that:
1. Loads NiuNiu.runtime.json
2. Accepts a scenario JSON
3. Evaluates defense triggers
4. Checks forbidden behaviors
5. Returns `verdict` + `violations` + `allowed_actions`

**Test:** Re-run ORBITAL_CONSTANT with NiuNiu only — verify defense triggers fire correctly.

### Phase 14E: Two-Runtime Contract Prototype

**Goal:** Engine loads two runtimes + generated contract.

**Deliverable:** Extended engine that:
1. Loads two runtime JSONs
2. Generates contract from `relationship_interfaces`
3. Evaluates both runtimes' constraints simultaneously
4. Detects contract violations
5. Returns `verdict` + `violations` + `allowed_actions` for both participants

**Test:** Re-run KIRI_AKU_KANAN with automated constraint resolution.

### Phase 14F: Negative Test Prototype

**Goal:** Engine correctly detects and rejects invariant violations.

**Deliverable:** Extended engine that:
1. Accepts `canon_mode.type == "stress_test"`
2. Runs full evaluation pipeline
3. Returns `TEST_PASS` when violations are correctly detected
4. Returns `FAIL` when a stress test scenario does NOT produce violations (false negative)

**Test:** Re-run ORBITAL_CONTRACT_VIOLATION with automated violation detection.

### Phase 14G: LLM Renderer Integration

**Goal:** Engine passes `allowed_actions` + `renderer_prompt` to an LLM.

**Deliverable:** Integration layer that:
1. Runs full constraint evaluation
2. Builds `renderer_prompt` from allowed action space + constraints
3. Passes prompt to LLM
4. LLM produces scene fragment
5. Scene fragment is NOT re-validated (renderer is creative, engine is constraint)

**Test:** Re-run KIRI_AKU_KANAN — engine produces allowed actions, LLM renders scene fragment. Compare with RUN_001 scene fragment.

---

## Final Assessment

### Engine Readiness Score: 78/100

| Criterion | Score | Notes |
|-----------|-------|-------|
| Specification completeness | 85/100 | 10 sections defined. Pipeline explicit. I/O schemas complete. |
| Reference test coverage | 90/100 | All 5 execution reports mapped to engine verdicts. |
| Implementability | 75/100 | Pipeline is deterministic. JSON schemas exist. No implementation yet — specification must survive first implementation attempt. |
| Renderer separation | 80/100 | Clear boundary between engine and renderer. Renderer prompt schema defined. |
| Edge case handling | 65/100 | CONTRADICTORY_CONSTRAINTS and INSUFFICIENT_DATA defined but not tested. Multi-runtime race conditions not addressed. |

### What Is Sufficient for First Prototype

1. ✅ JSON schemas (Phase 14A)
2. ✅ Reference runtime JSON (Phase 14B)
3. ✅ Engine specification (this document)
4. ⬜ Phase 14D: Single-runtime Python prototype

### What Remains Manual

- Constraint resolution logic — currently performed by human reading runtime files
- Scenario JSON authoring — scenarios must be manually structured
- Contract JSON generation — currently inferred from relationship interfaces by human
- Renderer prompt interpretation — LLM output is not validated post-rendering

### Biggest Risk

**Specification-implementation gap.** The pipeline is defined in prose. The first implementation attempt will reveal ambiguities in the specification — constraints that are clear to a human reader but underspecified for a deterministic engine. Mitigation: Phase 14D should be treated as specification validation, not just engine construction. Every ambiguity discovered during implementation must be resolved in a v1.1.0 of this specification.
