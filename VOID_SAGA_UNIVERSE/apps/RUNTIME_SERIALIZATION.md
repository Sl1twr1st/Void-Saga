# RUNTIME SERIALIZATION — Phase 14A

> **Date:** 2026-06-23
> **Phase:** 14A — Design Document
> **Purpose:** Convert Void Saga Runtime OS from human-readable Markdown into machine-readable JSON schemas
> **Dependency:** Phase 11 (Protocols), Phase 12 (Runtimes), Phase 13A (Validation)

---

## STEP 1 — Schema Audit

### Existing Data Structures in V2 Runtime Architecture

| # | Section | Data Type | Cardinality | Tagged | Machine-parseable? |
|---|---------|-----------|-------------|--------|-------------------|
| 1 | RuntimeStatus | Key-value + text | 1 | [E]/[I]/[PC] | Partially — version, classification are structured; limitations are free text |
| 2 | RuntimeClass | Arrow-separated sequence | 1 | [I] | Yes — modes in ordered list |
| 3 | PrimaryContradiction | Bold thesis + explanation | 1 | [E]/[I] | Thesis is extractable; explanation is free text |
| 4 | CoreWound | Name + structure + origin + secondary | 1 | [E]/[I]/[PC] | Wound name and structure fields are typed; evidence is free text |
| 5 | DefenseSystem | WHEN→THEN→COST blocks | 1 primary + N secondary | [E]/[I] | Fully structured — trigger, response, cost are discrete fields |
| 6 | InvocationPattern | Table: Phase, Invocation, Role, Status | N rows | [E]/[I] | Fully structured — table is directly mappable to array |
| 7 | CostPattern | Table: Cost, Invocation, Irreversibility | N rows | [E]/[I]/[PC] | Fully structured |
| 8 | ConsequencePattern | Table: Consequence, Invocation, Detail | N rows | [E]/[I]/[PC] | Fully structured |
| 9 | ResiduePattern | Table: Residue, Origin, Form, Tag | N rows | [E]/[I]/[PC] | Fully structured — form uses controlled vocabulary |
| 10 | ProtocolInterfaces | Per-protocol subsections | N sections | [E]/[I]/[PC] | Partially — interface description is free text |
| 11 | RelationshipInterfaces | Per-relationship subsections | N sections | [E]/[I]/[PC] | Partially — nature and behavioral rule are typed |
| 12 | EvolutionStages | Table + LOST/GAINED transitions | 3–6 stages | [E]/[I]/[PC] | Fully structured — operational mode, residue, relevance are typed fields |
| 13 | FailureMode | Primary + alternative + triggers | 1–2 modes | [E]/[I] | Partially — modes are named; triggers are structured |
| 14 | TerminalState | Bullet properties | N properties | [E]/[I] | Partially — properties are tagged; characterization is free text |
| 15 | CanonBoundaries | Open questions + interpretive claims | N items | [I]/[PC] | Fully structured — each boundary is a typed item with source |
| 16 | RuntimeSummary | Compressed formula | 1 | [I] | Yes — single string |

### Audit Finding

**15 of 16 sections are partially or fully machine-parseable.** The primary obstacle is free-text evidence descriptions and interface characterizations. These can be preserved as `description` fields without blocking structured extraction. Only 1 section (RuntimeSummary) is purely textual.

**Controlled vocabularies identified:**
- Residue forms: `ghost | node | fork | wound | echo | archive | error | runtime | sigil | interference`
- Invocation phases: `VOID_ENTRY | SIGIL_ACTIVATION | LIVING_CHAIN | NODE | PARADOX | ZERO_NODE`
- Evolution stage variables: operational_mode, primary_residue, protocol_relevance
- Tag taxonomy: `[E] | [I] | [PC]`
- Relationship natures: `combat_partner | orbital_constant | twin_paradox | mother_daughter | etc.`
- Defense triggers: threat types, character-proximity, emotional-content, system-demands

---

## STEP 2 — Runtime Object Design

### CHARACTER_RUNTIME_SCHEMA_V1

```json
{
  "$schema": "https://void-saga.dev/schemas/character-runtime-v1.json",
  "id": "string (e.g., 'niuniu', 'sevraya', 'julia')",
  "name": "string (full character name)",
  "version": "string (semver)",
  "architecture": "RUNTIME_ARCHITECTURE_V2",
  "canon_baseline": {
    "timer_range": "string",
    "protocols": ["string"],
    "audit_basis": "string"
  },
  "runtime_status": {
    "evidence_count": "number",
    "file_count": "number",
    "total_mentions": "number",
    "limitations": ["string"],
    "tags": { "E": "number", "I": "number", "PC": "number" }
  },
  "runtime_class": {
    "modes": ["string"],
    "classification_note": "string (optional, if [I])",
    "tag": "[E] | [I] | [PC]"
  },
  "primary_contradiction": {
    "thesis": "string",
    "explanation": "string",
    "tag": "[E] | [I] | [PC]"
  },
  "core_wound": {
    "name": "string",
    "structure": {
      "description": "string",
      "impossibilities": ["string"]
    },
    "origin_event": {
      "description": "string",
      "timer_reference": "string",
      "tag": "[E] | [I] | [PC]"
    },
    "secondary_wounds": [
      {
        "description": "string",
        "tag": "[E] | [I] | [PC]"
      }
    ]
  },
  "defense_system": {
    "primary_defense": {
      "name": "string",
      "trigger": "string",
      "response": "string",
      "cost": "string",
      "tag": "[E] | [I] | [PC]"
    },
    "secondary_defenses": [
      {
        "name": "string",
        "trigger": "string",
        "response": "string",
        "cost": "string",
        "tag": "[E] | [I] | [PC]"
      }
    ],
    "defense_disabled_by": {
      "invocation": "string",
      "mechanism": "string",
      "tag": "[E] | [I] | [PC]"
    }
  },
  "invocation_pattern": [
    {
      "phase": "number | null",
      "invocation": "string",
      "role": "string",
      "participation_type": "direct | indirect | failed | unresolved",
      "tag": "[E] | [I] | [PC]"
    }
  ],
  "cost_pattern": [
    {
      "cost": "string",
      "invocation": "string",
      "irreversible": "boolean",
      "tag": "[E] | [I] | [PC]"
    }
  ],
  "consequence_pattern": [
    {
      "consequence": "string",
      "invocation": "string",
      "detail": "string",
      "tag": "[E] | [I] | [PC]"
    }
  ],
  "residue_pattern": {
    "total_count": "number",
    "load_profile": "string",
    "residues": [
      {
        "name": "string",
        "origin": "string",
        "form": "ghost | node | fork | wound | echo | archive | error | runtime | sigil | interference",
        "tag": "[E] | [I] | [PC]"
      }
    ]
  },
  "protocol_interfaces": [
    {
      "protocol": "string",
      "phase": "number | null",
      "interface_description": "string",
      "participation_type": "direct | indirect",
      "tag": "[E] | [I] | [PC]"
    }
  ],
  "relationship_interfaces": [
    {
      "target": "string (runtime id)",
      "nature": "string",
      "behavioral_rule": "string",
      "symmetry_status": "symmetric | asymmetric | unresolved",
      "tag": "[E] | [I] | [PC]"
    }
  ],
  "evolution_stages": [
    {
      "stage_number": "number",
      "name": "string",
      "operational_mode": "string",
      "primary_residue": "string",
      "protocol_relevance": "string",
      "lost_in_transition": ["string"],
      "gained_in_transition": ["string"],
      "tag": "[E] | [I] | [PC]"
    }
  ],
  "failure_mode": {
    "primary": {
      "name": "string",
      "description": "string",
      "tag": "[E] | [I] | [PC]"
    },
    "alternative": {
      "name": "string",
      "description": "string",
      "tag": "[E] | [I] | [PC]"
    },
    "trigger_conditions": ["string"]
  },
  "terminal_state": {
    "properties": [
      {
        "property": "string",
        "tag": "[E] | [I] | [PC]"
      }
    ]
  },
  "canon_boundaries": {
    "open_questions": [
      {
        "question": "string",
        "status": "unresolved"
      }
    ],
    "interpretive_claims": [
      {
        "claim": "string",
        "source": "string (e.g., 'Sigil_OS.md')",
        "tag": "[I] | [PC]",
        "decanonization_risk": "string"
      }
    ]
  },
  "runtime_summary": {
    "narrative_formula": "string",
    "compressed_formula": "string",
    "distinction": "string"
  },
  "cross_references": {
    "related_runtimes": ["string (runtime ids)"],
    "world_dna_dependencies": ["string (file paths)"],
    "protocol_dependencies": ["string (file paths)"]
  }
}
```

### Design Notes

1. **All 16 V2 sections preserved.** No structural information lost.
2. **Controlled vocabularies** for residue forms, participation types, and tag taxonomy enable querying.
3. **`tag` field on every claim** preserves [E]/[I]/[PC] discipline. A constraint engine can filter by evidence level.
4. **`symmetry_status` on relationships** enables automated contract verification between two loaded runtimes.
5. **`lost_in_transition` and `gained_in_transition` as arrays** enable state machine representation of character evolution.
6. **Free-text fields** (`interface_description`, `behavioral_rule`, `detail`) preserved for human readability. Machine processing uses structured fields; human fallback reads descriptions.

---

## STEP 3 — Protocol Object Design

### PROTOCOL_SCHEMA_V1

```json
{
  "$schema": "https://void-saga.dev/schemas/protocol-v1.json",
  "id": "string (e.g., 'void_entry', 'living_chain')",
  "name": "string",
  "type": "invocation | meta",
  "phase": "number | null",
  "status": "active | pending",
  "law_references": ["string (file paths)"],
  "runtime_references": ["string (runtime ids)"],
  "boot_sequence_position": {
    "input": "string",
    "output": "string",
    "previous_phase": "string | null",
    "next_phase": "string | null"
  },
  "purpose": "string",
  "invocation": {
    "mechanism_description": "string",
    "observed_instances": [
      {
        "participants": ["string (runtime ids)"],
        "location": "string",
        "timer_reference": "string",
        "tag": "[E] | [I] | [PC]"
      }
    ],
    "activation_conditions": ["string"],
    "tag": "[E] | [I] | [PC]"
  },
  "participants": [
    {
      "runtime_id": "string",
      "role": "string",
      "contribution": "string",
      "tag": "[E] | [I] | [PC]"
    }
  ],
  "costs": [
    {
      "cost": "string",
      "paid_by": ["string (runtime ids)"],
      "irreversible": "boolean",
      "tag": "[E] | [I] | [PC]"
    }
  ],
  "consequences": [
    {
      "consequence": "string",
      "detail": "string",
      "tag": "[E] | [I] | [PC]"
    }
  ],
  "residues": [
    {
      "residue": "string",
      "origin": "string",
      "form": "ghost | node | fork | wound | echo | archive | error | runtime | sigil | interference",
      "tag": "[E] | [I] | [PC]"
    }
  ],
  "failure_modes": [
    {
      "name": "string",
      "description": "string",
      "observed": "boolean",
      "consequence": "string",
      "tag": "[E] | [I] | [PC]"
    }
  ],
  "ontology": {
    "chain_formula": "string",
    "pipeline_position": "string",
    "tag": "[E] | [I] | [PC]"
  },
  "canon_status": {
    "evidenced": ["string"],
    "inferred": ["string"],
    "probable_canon": ["string"]
  }
}
```

---

## STEP 4 — Contract Object Design

### CONTRACT_SCHEMA_V1

```json
{
  "$schema": "https://void-saga.dev/schemas/contract-v1.json",
  "id": "string (e.g., 'niuniu_sevraya', 'julia_niuniu')",
  "runtime_a": "string (runtime id)",
  "runtime_b": "string (runtime id)",
  "contract_type": "foundational | structural | operational",
  "nature": "string",
  "symmetry": "symmetric | asymmetric | unresolved",
  "gravity": {
    "runtime_a_pull": "string (e.g., '80%+')",
    "runtime_b_pull": "string",
    "world_dna_backing": "boolean",
    "akashic_registered": "boolean"
  },
  "behavioral_rule": {
    "from_a_to_b": "string",
    "from_b_to_a": "string"
  },
  "conflict_events": [
    {
      "event": "string",
      "timer_reference": "string",
      "tag": "[E] | [I] | [PC]"
    }
  ],
  "cross_runtime_verification": {
    "verified": "boolean",
    "audit_reference": "string"
  },
  "constraints": [
    {
      "constraint": "string",
      "source": "string",
      "violation_consequence": "string",
      "tag": "[E] | [I] | [PC]"
    }
  ],
  "test_results": [
    {
      "execution_id": "string",
      "test_type": "positive | negative",
      "verdict": "PASS | TEST PASS | FAIL",
      "execution_file": "string"
    }
  ]
}
```

### Design Notes

1. **Bidirectional behavioral rules** (`from_a_to_b` / `from_b_to_a`) capture asymmetry explicitly.
2. **`gravity` object** encodes the quantitative pull strengths documented in runtime canon gravity sections.
3. **`conflict_events` array** documents adversarial contract history — essential for twin paradox and saved/abandoned.
4. **`constraints` array with `violation_consequence`** enables the constraint engine to produce specific rejection messages.
5. **`test_results` array** links contracts to their execution reports — full traceability from schema to validation.

---

## STEP 5 — Dependency Graph Mapping

### Schema Dependency Graph

```
RUNTIME_SCHEMA_V1
  ├── references PROTOCOL_SCHEMA_V1 (via protocol_interfaces[].protocol)
  ├── references RUNTIME_SCHEMA_V1 (via relationship_interfaces[].target)
  ├── references CONTRACT_SCHEMA_V1 (via cross_references)
  └── uses controlled vocabularies from RESIDUE_THEORY

PROTOCOL_SCHEMA_V1
  ├── references RUNTIME_SCHEMA_V1 (via participants[].runtime_id)
  ├── references PROTOCOL_SCHEMA_V1 (via boot_sequence_position.next_phase)
  └── uses controlled vocabularies from RESIDUE_THEORY, GOETIC_CONSEQUENCE

CONTRACT_SCHEMA_V1
  ├── references RUNTIME_SCHEMA_V1 (via runtime_a, runtime_b)
  ├── references RUNTIME_SCHEMA_V1 (via test_results[].execution_id → execution report)
  └── validated against cross_runtime_verification
```

### Load Order

```
1. Load World DNA constants (residue forms, invocation phases, tag taxonomy)
2. Load PROTOCOL_SCHEMA_V1 files (6 active, 2 pending)
3. Load CHARACTER_RUNTIME_SCHEMA_V1 files (7 runtimes)
4. Load CONTRACT_SCHEMA_V1 files (generated from relationship interfaces)
5. Validate cross-references
6. Boot sequence verification (Phase 1→2→3→4→5→6 dependency chain)
```

---

## STEP 6 — Migration Path from Markdown → JSON

### Phase 14A (this document)
- Schema design and specification
- No file conversion

### Phase 14B (proposed)
- Create `schemas/` directory
- Write JSON Schema files for validation
- Create one reference implementation: `characters/niuniu.runtime.json`
- Validate against schema
- Compare with Markdown source for completeness

### Phase 14C (proposed)
- Batch conversion: all 7 runtimes to JSON
- Batch conversion: all 6 active protocols to JSON
- Auto-generate contracts from relationship interfaces
- Cross-reference validation

### Phase 14D (proposed)
- Constraint engine: load JSON runtimes, evaluate scenarios
- Replace manual constraint checking with automated resolution
- First automated execution test (re-run KIRI_AKU_KANAN with JSON input)

### Backward Compatibility

- Markdown runtimes remain canonical
- JSON is a **serialization layer**, not a replacement
- Discrepancies between Markdown and JSON resolve to Markdown (canonical source)
- JSON schemas versioned independently: v1.0.0 initial, semver thereafter

---

## STEP 7 — Readiness Assessment

### Schema Design Completeness

| Schema | Sections Covered | Controlled Vocabularies | Machine-parseable Claims | Readiness |
|--------|-----------------|------------------------|--------------------------|-----------|
| CHARACTER_RUNTIME | 16/16 V2 sections | 5 vocabularies | 80%+ of claims are typed fields | **READY** |
| PROTOCOL | 10/10 sections | 3 vocabularies | 75%+ of claims are typed fields | **READY** |
| CONTRACT | 7/7 fields | 3 vocabularies | 90%+ of claims are typed fields | **READY** |

### What These Schemas Enable

| Capability | Previously | With JSON Schemas |
|-----------|-----------|-------------------|
| Load a runtime | Read ~400 lines of Markdown | Parse one JSON file |
| Verify a claim's evidence level | Human reads [E] tag | Machine queries `tag` field |
| Check if two runtimes are contract-compatible | Human reads both relationship interfaces | Machine compares `relationship_interfaces[].target` fields |
| Trace residue to origin invocation | Human follows cross-references | Machine queries `residue_pattern.residues[].origin` against `invocation_pattern` |
| Validate that a fork doesn't break invariants | Human checks coherence test | Machine checks invariants against fork's declared divergence point |
| Run a constraint check | Human reads runtime, evaluates scenario | Machine loads JSON, resolves constraints |

### Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Markdown→JSON drift | HIGH | Markdown remains canonical. JSON is serialization. Drift detected by cross-reference validation in Phase 14C. |
| Free-text fields not machine-actionable | MEDIUM | Structured fields carry the constraint data. Free-text is human-readable fallback. |
| Schema too rigid for narrative nuance | MEDIUM | `description` fields preserve full narrative context. Schema constrains structure, not content. |
| Controlled vocabulary incomplete | LOW | Vocabularies derived from existing canon. Extensible as new forms emerge. |

### Verdict

**READY for Phase 14B — Reference Implementation.**

The three JSON schemas cover all structured data in the Void Saga Runtime OS. No lore created. No canon modified. The schemas are a serialization layer — a bridge between human-readable architecture and machine-executable constraints. Phase 14B should produce one working reference implementation (NiuNiu runtime) to validate the schema before batch conversion.
