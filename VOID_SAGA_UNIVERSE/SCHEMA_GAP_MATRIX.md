# SCHEMA GAP MATRIX — Task #1 Output

> **Audit date:** 24 June 2026
> **Sources:** NiuNiu.runtime.json (709 lines, v2.1.0), Sevraya.runtime.json (516 lines, v1.1.0)
> **Reference:** BLUEPRINT.md v2.1.0, RUNTIME_ARCHITECTURE_V2.md
> **Principle:** Optimize for schema stability, not completeness. Identify the minimum viable unified schema.

---

## 1. SHARED FIELDS (present in both)

These 28 top-level fields exist in both NiuNiu and Sevraya. They are **confirmed stable** and become the backbone of Schema V2.1.

| # | Field | Type | NiuNiu | Sevraya | Notes |
|---|-------|------|--------|---------|-------|
| 1 | `$schema` | string | ✅ | ✅ | Different values — both point to RUNTIME_SERIALIZATION.md |
| 2 | `id` | string | ✅ `"niuniu"` | ✅ `"sevraya"` | Lowercase, no spaces. Convention confirmed. |
| 3 | `name` | string | ✅ | ✅ | Full display name |
| 4 | `version` | string | ✅ `"2.1.0"` | ✅ `"1.1.0"` | Semver |
| 5 | `architecture` | string | ✅ `"RUNTIME_ARCHITECTURE_V1"` | ✅ `"RUNTIME_ARCHITECTURE_V1"` | Both V1 — needs upgrade to V2.1 |
| 6 | `canon_baseline` | object | ✅ | ✅ | timer_range, protocols[], audit_basis |
| 7 | `runtime_status` | object | ✅ | ✅ | evidence_count, file_count, total_mentions, limitations[], tags |
| 8 | `runtime_class` | object | ✅ | ✅ | modes[], classification_note, tag |
| 9 | `primary_contradiction` | object | ✅ | ✅ | thesis, explanation, tag |
| 10 | `core_wound` | object | ✅ | ✅ | name, structure{description, impossibilities[]}, origin_event, secondary_wounds[] |
| 11 | `core_desire` | object | ✅ | ✅ | statement, source, interpretation, conflict_with_defense, tag |
| 12 | `defense_system` | object | ✅ | ✅ | primary_defense, secondary_defenses[], signature_move, defense_disabled_by |
| 13 | `trigger_conditions` | array | ✅ 7 items | ✅ 6 items | trigger, defense, intensity, tag |
| 14 | `anomalous_triggers` | array | ✅ 2 items | ✅ 3 items | trigger, anomaly, evidence, tag |
| 15 | `somatic_signature` | object | ✅ | ✅ | **Character-specific fields.** Structure varies — this is intentional. |
| 16 | `voice_grammar` | object | ✅ | ✅ | **Structure varies.** NiuNiu: pre/post split. Sevraya: flat with zero_differentiation. |
| 17 | `cosmic_function` | object | ✅ | ✅ | role, description, world_dna_ref, tag |
| 18 | `invocation_pattern` | array | ✅ 7 items | ✅ 8 items | phase, invocation, role, participation_type, tag |
| 19 | `cost_pattern` | array | ✅ 6 items | ✅ 7 items | cost, invocation, irreversible, tag, note? |
| 20 | `consequence_pattern` | array | ✅ 6 items | ✅ 6 items | consequence, invocation, detail, tag |
| 21 | `residue_pattern` | object | ✅ | ✅ | total_count, load_profile, residues[] |
| 22 | `protocol_interfaces` | array | ✅ 5 items | ✅ 5 items | protocol, phase, interface_description, participation_type, tag |
| 23 | `relationship_interfaces` | array | ✅ 7 items | ✅ 6 items | target, nature, behavioral_rule, symmetry_status, tag |
| 24 | `evolution_stages` | array | ✅ 4 items | ✅ 6 items | stage_number, name, trigger, operational_mode, primary_residue, protocol_relevance, lost_in_transition[], gained_in_transition[], tag |
| 25 | `canon_gravity` | array | ✅ 5 items | ✅ 5 items | gravity, pull, tag |
| 26 | `anti_gravity` | array | ✅ 5 items | ✅ 5 items | String array |
| 27 | `forbidden_behaviors` | array | ✅ 7 items | ✅ 7 items | behavior, exception, penalty, tag |
| 28 | `failure_mode` | object | ✅ | ✅ | primary, alternative?, trigger_conditions[] |
| 29 | `terminal_state` | object | ✅ | ✅ | properties[] with property + tag |
| 30 | `canon_boundaries` | object | ✅ | ✅ | open_questions[], interpretive_claims[] |
| 31 | `runtime_summary` | object | ✅ | ✅ | narrative_formula, compressed_formula, distinction |
| 32 | `cross_references` | object | ✅ | ✅ | related_runtimes[], world_dna_dependencies[], protocol_dependencies[] |
| 33 | `serialization_notes` | array | ✅ 5 strings | ✅ 4 strings | Free-text engineering notes |

**Verdict: 33 shared fields. Foundation is solid.**

---

## 2. FIELDS IN NiuNiu BUT MISSING IN Sevraya

These fields exist in NiuNiu.runtime.json but are absent from Sevraya.runtime.json. Each must be evaluated: is it character-specific or should it be standardized?

| # | Field | Type | Evaluation | Recommendation |
|---|-------|------|------------|----------------|
| 1 | `meta_trigger` | object | **Character-specific.** NiuNiu has Living Chain forcing honesty. Sevraya's equivalent is documented in `defense_system.defense_disabled_by`. | **Optional.** Add to Sevraya if her meta-trigger differs from her defense_disabled_by. |
| 2 | `fork_sensitive_traits` | array of objects | **Should be standardized.** Defines what traits can change in forks, their range, and cost. Critical for the fork system. | **REQUIRED.** Add to Sevraya. |
| 3 | `fork_invariants` | array of strings | **Should be standardized.** Defines what traits CANNOT change. Critical for constraint validation. | **REQUIRED.** Add to Sevraya. |
| 4 | `fork_points` | array of objects | **Should be standardized.** Named fork scenarios with divergence details. Important for the fork system UX. | **REQUIRED.** Add to Sevraya. |
| 5 | `evolution_stages[].voice_sample` | string | **Should be standardized.** Per-stage voice samples are invaluable for the Narrative Compiler's prompt builder. | **REQUIRED.** Add to Sevraya for each stage. |
| 6 | `relationship_interfaces[].canon_gravity_pull` | string | **Inconsistent.** NiuNiu has this on 2 of 7 relationships. Sevraya has it on 1 of 6. | **Standardize as OPTIONAL.** Document when it should be present. |
| 7 | `canon_gravity[].evidence` | string | **NiuNiu-specific.** NiuNiu gravity items include evidence text. Sevraya doesn't. | **OPTIONAL.** Nice-to-have but not required. |
| 8 | `trigger_conditions[].tag` | string | **Tag discipline gap.** NiuNiu consistently tags `[E]` on triggers including the tag field. Sevraya also has tag on all triggers. Wait — both have it. Rechecking... Both have tag. | Already shared. No action. |

**Verdict: 4 fields should be REQUIRED in Schema V2.1. 3 should be OPTIONAL. 1 is character-specific.**

---

## 3. FIELDS IN Sevraya BUT MISSING IN NiuNiu

| # | Field | Type | Evaluation | Recommendation |
|---|-------|------|------------|----------------|
| 1 | `voice_grammar.zero_differentiation` | string | **Character-specific.** Only Sevraya shares her body with Zero. The differentiation note is critical for her but irrelevant for NiuNiu. | **Do not standardize.** Character-specific field. Schema should allow but not require. |
| 2 | `cosmic_function.trinity_role` | string | **Semantic overlap.** NiuNiu's `cosmic_function.role` contains the same information but in a single string rather than split fields. | **Standardize as OPTIONAL subfield.** `trinity_role` is useful for Trinitas characters. Not all characters belong to a trinity. |
| 3 | `defense_system.secondary_defenses[].name` | string | **Both have it.** Just verified — both have name fields in secondary defenses. | Already shared. No action. |

**Verdict: 1 field is character-specific. 1 should be OPTIONAL. No Sevraya-exclusive fields require mandatory standardization.**

---

## 4. FIELDS REQUIRED BY BLUEPRINT v2.1.0 BUT MISSING FROM BOTH

Per Phase 1B (minimum runtime content) and Phase 1C (expansion), these fields are expected but absent:

| # | Field | Blueprint Reference | NiuNiu | Sevraya | Recommendation |
|---|-------|---------------------|--------|---------|----------------|
| 1 | `stress_test_prompts` | Phase 1C.2 | ❌ | ❌ | **REQUIRED.** 3-5 scenarios designed to break the character. Add to schema as mandatory array. |
| 2 | `state_variables` | Phase 1C.3 | ❌ (embedded in evolution stages) | ❌ | **REQUIRED.** Mutable internal states with schema, valid values, transition rules. NiuNiu partially covers this via evolution stage variable registry, but it's not a top-level field. |
| 3 | `sigil` | Phase 1B scope | ❌ (embedded in invocation + relationship) | ❌ (embedded in invocation + relationship) | **REQUIRED.** Explicit top-level sigil reference. Currently sigil info is scattered across invocation_pattern, protocol_interfaces, and relationship_interfaces. A dedicated `sigil` field makes engine lookups deterministic. |

**Verdict: 3 new fields must be added to Schema V2.1. Both existing runtimes need to be upgraded.**

---

## 5. FIELDS THAT SHOULD BE MANDATORY (Schema V2.1)

Based on engine consumption patterns and cross-runtime consistency requirements:

| # | Field | Reason |
|---|-------|--------|
| 1 | `id` | Primary key for all engine operations |
| 2 | `name` | Display name |
| 3 | `version` | Schema version tracking |
| 4 | `architecture` | Which runtime architecture this was built against |
| 5 | `runtime_status` | Evidence counts, limitations, tag taxonomy |
| 6 | `runtime_class` | Operational modes for engine mode selection |
| 7 | `primary_contradiction` | Core behavioral driver — used by engine Step 5 (identity invariants) |
| 8 | `core_wound` | Wound structure with impossibilities — engine Step 5 |
| 9 | `core_desire` | Emotional architecture — prompt compiler |
| 10 | `defense_system` | Defense patterns with WHEN/THEN/COST — engine Step 6 |
| 11 | `trigger_conditions` | When defenses fire, with intensity — engine Step 6 |
| 12 | `voice_grammar` | Tone, sentence structure, vocabulary — prompt compiler + validator |
| 13 | `invocation_pattern` | Which phases character participated in — engine Step 9 (protocol gating) |
| 14 | `cost_pattern` | Costs paid per invocation — engine Step 9 |
| 15 | `consequence_pattern` | Consequences per invocation — engine Step 9 |
| 16 | `residue_pattern` | Residues carried — state validator, state diff |
| 17 | `relationship_interfaces` | Behavioral rules per relationship — engine Step 7 (contract check) |
| 18 | `evolution_stages` | Stage transitions + state variable registry — engine Step 5, state validator |
| 19 | `canon_gravity` | What must happen — engine Step 10 |
| 20 | `anti_gravity` | What must NOT happen — engine Step 10 |
| 21 | `forbidden_behaviors` | HARD constraints with exception/price — engine Step 8 |
| 22 | `failure_mode` | How the character breaks — engine Step 5 (boundary condition) |
| 23 | `terminal_state` | End-state properties — state validator |
| 24 | `fork_sensitive_traits` | What can change in forks — fork coherence validator |
| 25 | `fork_invariants` | What CANNOT change — fork coherence validator (HARD) |
| 26 | `fork_points` | Named fork scenarios — fork system UX |
| 27 | `sigil` | Top-level sigil reference — engine Step 9 (sigil activation check) |
| 28 | `stress_test_prompts` | Validation scenarios — engine test suite |
| 29 | `state_variables` | Mutable internal states — state validator, state diff |

---

## 6. FIELDS THAT SHOULD BE OPTIONAL (Schema V2.1)

| # | Field | Reason |
|---|-------|--------|
| 1 | `canon_baseline` | Metadata. Useful for documentation, not consumed by engine. |
| 2 | `meta_trigger` | Only some characters have meta-triggers (Living Chain active, etc.) |
| 3 | `anomalous_triggers` | Edge cases. Valuable for prompt compiler but not all characters have them. |
| 4 | `somatic_signature` | Character-specific. Shape varies per character. Needed for prompt compiler. |
| 5 | `cosmic_function` | Only Void's Trinity + Era Stewards have this. Not applicable to all characters. |
| 6 | `protocol_interfaces` | Derived from invocation_pattern. Redundant for engine but useful for documentation. |
| 7 | `canon_gravity[].evidence` | Nice-to-have documentation. Not consumed by engine. |
| 8 | `relationship_interfaces[].canon_gravity_pull` | Only present on some relationships. Useful for contract engine but not universal. |
| 9 | `evolution_stages[].voice_sample` | Per-stage voice samples. Extremely valuable for prompt compiler. Should be encouraged but not mandatory (may not exist in canon for all stages). |
| 10 | `canon_boundaries` | Open questions + interpretive claims. Documentation, not consumed by engine. |
| 11 | `runtime_summary` | Human-facing. Not consumed by engine. |
| 12 | `cross_references` | Documentation. Not consumed by engine. Could be auto-generated. |
| 13 | `serialization_notes` | Engineering notes. Not consumed by engine. |
| 14 | `cosmic_function.trinity_role` | Only for Trinitas members. |
| 15 | `voice_grammar.zero_differentiation` | Only Sevraya (Zero co-consciousness). |
| 16 | `$schema` | JSON Schema reference. Useful for validation but not consumed by engine. |

---

## 7. RECOMMENDED RUNTIME_SCHEMA_V2.1 STRUCTURE

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://voidsaga.id/schemas/RUNTIME_SCHEMA_V2.1.json",
  "title": "Void Saga Character Runtime",
  "type": "object",
  "required": [
    "id",
    "name",
    "version",
    "architecture",
    "runtime_status",
    "runtime_class",
    "primary_contradiction",
    "core_wound",
    "core_desire",
    "defense_system",
    "trigger_conditions",
    "voice_grammar",
    "invocation_pattern",
    "cost_pattern",
    "consequence_pattern",
    "residue_pattern",
    "relationship_interfaces",
    "evolution_stages",
    "canon_gravity",
    "anti_gravity",
    "forbidden_behaviors",
    "failure_mode",
    "terminal_state",
    "fork_sensitive_traits",
    "fork_invariants",
    "fork_points",
    "sigil",
    "stress_test_prompts",
    "state_variables"
  ],
  "properties": {
    "id": { "type": "string", "pattern": "^[a-z_]+$" },
    "name": { "type": "string" },
    "version": { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$" },
    "architecture": { "type": "string", "enum": ["RUNTIME_ARCHITECTURE_V2.1"] },

    "runtime_status": {
      "type": "object",
      "required": ["evidence_count", "tags"],
      "properties": {
        "evidence_count": { "type": "integer" },
        "file_count": { "type": "integer" },
        "total_mentions": { "type": "integer" },
        "limitations": { "type": "array", "items": { "type": "string" } },
        "tags": {
          "type": "object",
          "required": ["E", "I", "PC"],
          "properties": {
            "E": { "type": "integer" },
            "I": { "type": "integer" },
            "PC": { "type": "integer" }
          }
        }
      }
    },

    "sigil": {
      "type": "object",
      "required": ["glyph", "name", "function"],
      "properties": {
        "glyph": { "type": "string" },
        "name": { "type": "string" },
        "function": { "type": "string" },
        "activation_condition": { "type": "string" },
        "weakness": { "type": "string" },
        "tag": { "type": "string", "enum": ["[E]", "[I]", "[PC]"] }
      }
    },

    "state_variables": {
      "type": "object",
      "description": "Mutable internal states with schema, valid values, and transition rules.",
      "patternProperties": {
        "^[a-z_]+$": {
          "type": "object",
          "required": ["type", "current_value", "valid_values"],
          "properties": {
            "type": { "type": "string", "enum": ["string", "enum", "integer", "boolean"] },
            "current_value": {},
            "valid_values": { "type": "array" },
            "transition_rules": { "type": "array", "items": { "type": "string" } }
          }
        }
      }
    },

    "stress_test_prompts": {
      "type": "array",
      "minItems": 3,
      "maxItems": 5,
      "items": {
        "type": "object",
        "required": ["scenario", "expected_violation"],
        "properties": {
          "scenario": { "type": "string" },
          "expected_violation": { "type": "string" },
          "expected_canon_score_range": { "type": "string" }
        }
      }
    },

    "fork_sensitive_traits": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["trait", "range", "cost", "tag"],
        "properties": {
          "trait": { "type": "string" },
          "range": { "type": "string" },
          "cost": { "type": "string" },
          "tag": { "type": "string" }
        }
      }
    },

    "fork_invariants": {
      "type": "array",
      "items": { "type": "string" }
    },

    "fork_points": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "canon_event", "divergence", "gravity_resistance"],
        "properties": {
          "name": { "type": "string" },
          "canon_event": { "type": "string" },
          "divergence": { "type": "string" },
          "gravity_resistance": { "type": "string", "enum": ["LOW", "MEDIUM", "HIGH", "EXTREME"] },
          "new_questions": { "type": "string" },
          "tag": { "type": "string" }
        }
      }
    }
  }
}
```

**Note:** Full JSON Schema with all 29 required fields and all optional fields will be produced in Task #2 (`RUNTIME_SCHEMA_V2.1.json`). The above is the structural recommendation, not the complete schema.

---

## 8. MIGRATION NOTES — Upgrading NiuNiu & Sevraya

### NiuNiu (v2.1.0 → Schema V2.1)

| Action | Detail |
|--------|--------|
| **ADD** `sigil` | Extract from invocation_pattern + relationship_interfaces into dedicated top-level object. Glyph: `𐓷⧖𐓣`, Name: "Shadow Logic". |
| **ADD** `state_variables` | Extract from evolution_stages cross-stage comparison. At minimum: `voice_status`, `protection_mode`, `current_stage`. |
| **ADD** `stress_test_prompts` | Create 3-5 scenarios. Example: "NiuNiu is asked to give a motivational speech to troops. Expected: voice grammar violation." |
| **UPDATE** `architecture` | Change from `"RUNTIME_ARCHITECTURE_V1"` to `"RUNTIME_ARCHITECTURE_V2.1"` |
| **UPDATE** `version` | If content unchanged, keep `"2.1.0"`. If content added, bump to `"2.2.0"`. |
| **NO CHANGE** | All existing 33 shared fields remain intact. Do not remove data. |

### Sevraya (v1.1.0 → Schema V2.1)

| Action | Detail |
|--------|--------|
| **ADD** `fork_sensitive_traits` | Infer from canon. Example: "Degree of Zero integration (range: total separation → partial reintegration → Zero dominance)" |
| **ADD** `fork_invariants` | Infer from anti_gravity. Example: "Zero remains co-conscious", "Orbital constant with NiuNiu" |
| **ADD** `fork_points` | Infer from forbidden_behaviors + anti_gravity. Example: "Zero Separation — Zero removed to independent body. Resistance: EXTREME." |
| **ADD** `sigil` | Extract from invocation_pattern. Glyph: `🌊⌇🌒`, Name: "Tidal Memory" (shared with Zero). |
| **ADD** `state_variables` | Define: `zero_dominance`, `emotional_presence`, `current_stage`. |
| **ADD** `stress_test_prompts` | Create 3-5 scenarios. Example: "Sevraya is asked to give a direct emotional confession without deflecting to structural frame." |
| **ADD** `evolution_stages[].voice_sample` | Add per-stage voice samples. Critical for prompt compiler. |
| **ADD** `meta_trigger` | If applicable (Living Chain active → retreat to Zero prevented). Otherwise document why absent. |
| **UPDATE** `architecture` | Change from `"RUNTIME_ARCHITECTURE_V1"` to `"RUNTIME_ARCHITECTURE_V2.1"` |
| **UPDATE** `version` | Bump to `"2.0.0"` (major: new required fields added) |
| **NO CHANGE** | All existing 33 shared fields remain intact. |

---

## 9. RISK NOTES — Before Serializing Zero, Julia, Delphie

### Risk 1: Schema Instability
**Risk:** Schema V2.1 changes after Zero is serialized. Zero must be re-validated. Ripple effect.
**Mitigation:** Freeze schema after Task #2 (`RUNTIME_SCHEMA_V2.1.json` written and validated against NiuNiu + Sevraya). Only allow backward-compatible additions after that.

### Risk 2: Voice Grammar Inference Quality
**Risk:** Julia, Delphie, Agnia, Gwaneum have no voice grammar in their MD files. Inference from canon is subjective. If we get it wrong, the Narrative Compiler generates out-of-character dialogue.
**Mitigation:** Tag all inferred voice grammar as `[I]`. Document inference path. Accept that voice grammar improves iteratively — it does not need to be perfect for MVP.

### Risk 3: Forbidden Behaviors for New Characters
**Risk:** Julia, Delphie, Agnia, Gwaneum have no forbidden behaviors in their MDs. We must write them from scratch. Risk of missing critical constraints → engine false negatives.
**Mitigation:** Write 5-7 forbidden behaviors (not 10 — fewer, higher confidence). Tag all as `[I]`. Engine treats `[I]` forbidden behaviors as WARNING-level, not ERROR-level. Upgrade to `[E]` after compiler testing reveals gaps.

### Risk 4: Hasan Runtime Gap
**Risk:** Hasan is v0.5.0 compact — no defense system, no evolution stages, no failure mode. Serializing him requires heavy inference.
**Mitigation:** Defer Hasan to last in Phase 1B (Week 5-6). Accept partial runtime for MVP. Mark unsupported sections explicitly. Compiler scenarios can exclude Hasan initially.

### Risk 5: Cross-Reference Consistency
**Risk:** When NiuNiu's `relationship_interfaces[sevraya].canon_gravity_pull` says `"STRONG (80%+)"` and Sevraya's says `"STRONG (85%+)"`, which is canonical?
**Mitigation:** During Phase 1C cross-runtime audit, flag all asymmetry. For MVP, accept the higher value as canonical. Document discrepancy.

### Risk 6: Zero's Runtime — Shared Sigil
**Risk:** Zero shares the Tidal Memory sigil (`🌊⌇🌒`) with Sevraya. Both runtimes reference the same sigil. Schema must support "shared sigil" pattern. If not, engine will treat them as separate sigils.
**Mitigation:** `sigil.shared_with` optional field in Schema V2.1. Both Sevraya and Zero reference the same sigil ID with `shared_with: true`.

---

## 10. SUMMARY

### What We Know

- **33 fields are shared** between NiuNiu and Sevraya. These are stable. Schema V2.1 inherits all of them.
- **4 fields in NiuNiu must be promoted to REQUIRED** for all runtimes: `fork_sensitive_traits`, `fork_invariants`, `fork_points`, `evolution_stages[].voice_sample`.
- **3 fields are absent from both** and must be ADDED as REQUIRED: `sigil`, `stress_test_prompts`, `state_variables`.
- **Structural differences in `voice_grammar`** between NiuNiu (pre/post split) and Sevraya (flat) are character-appropriate, not a schema problem. Schema should allow both shapes.
- **`somatic_signature` shape varies** per character. Schema should validate as `object` without required subfields.

### What We Don't Know (Yet)

- Whether the 29 required fields will all apply cleanly to Hasan (v0.5.0 compact)
- Whether `voice_grammar` shape variation (pre/post vs flat) indicates a need for a `voice_grammar_type` enum

### Recommended Sequence

1. **Task #2:** Write `RUNTIME_SCHEMA_V2.1.json` based on this gap matrix.
2. **Task #3:** Upgrade NiuNiu + Sevraya to pass Schema V2.1 validation.
3. **Task #4:** Serialize Zero (lowest risk — voice + forbidden already exist).
4. **Task #5 onward:** Julia → Delphie → Agnia → Gwaneum → Hasan.

---

*Audit by: Claude, acting as systems architect*
*Duration: 1 session*
*Status: COMPLETE — Ready for Task #2*
