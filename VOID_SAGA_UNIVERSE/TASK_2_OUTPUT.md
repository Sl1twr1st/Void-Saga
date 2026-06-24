# TASK #2 OUTPUT — Schema Generation Complete

> **Schema file:** `apps/schema/RUNTIME_SCHEMA_V2.1.json`
> **Validation:** NiuNiu 26/29, Sevraya 23/29 (gaps exactly match gap matrix predictions)
> **Status:** Schema created and validated. Ready for migration (Task #3).

---

## 1. REQUIRED FIELD LIST (29 fields)

Every character runtime JSON must contain these 29 top-level fields:

| # | Field | Engine Step | Description |
|---|-------|-------------|-------------|
| 1 | `id` | All | Machine-readable ID. Lowercase, underscores. |
| 2 | `name` | — | Full display name. |
| 3 | `version` | — | Semver of this runtime file. |
| 4 | `architecture` | — | Must be `"RUNTIME_ARCHITECTURE_V2.1"`. |
| 5 | `runtime_status` | — | Evidence counts, limitations, tag taxonomy. |
| 6 | `runtime_class` | — | Operational modes `["Protector", "Weapon", ...]`. |
| 7 | `primary_contradiction` | Step 5 | Core behavioral driver. |
| 8 | `core_wound` | Step 5 | Originating wound + impossibilities. |
| 9 | `core_desire` | Prompt | What the character wants most. |
| 10 | `defense_system` | Step 6 | Defense patterns with WHEN/THEN/COST. |
| 11 | `trigger_conditions` | Step 6 | When defenses fire, with intensity. |
| 12 | `voice_grammar` | Prompt, Validator | How this character speaks. Shape is character-appropriate. |
| 13 | `invocation_pattern` | Step 9 | Boot-sequence phase participation. |
| 14 | `cost_pattern` | Step 9 | Costs paid per invocation. |
| 15 | `consequence_pattern` | Step 9 | Consequences per invocation. |
| 16 | `residue_pattern` | State, Diff | Residues carried. |
| 17 | `relationship_interfaces` | Step 7 | Behavioral rules per relationship. |
| 18 | `evolution_stages` | Step 5, State | Stage transitions. Each stage MUST have `voice_sample`. |
| 19 | `canon_gravity` | Step 10 | What must happen. |
| 20 | `anti_gravity` | Step 10 | What must NOT happen. |
| 21 | `forbidden_behaviors` | Step 8 | HARD constraints with exception/penalty. |
| 22 | `failure_mode` | Step 5 | How the character breaks. |
| 23 | `terminal_state` | State | End-state properties. |
| 24 | `fork_sensitive_traits` | Fork | Traits that CAN change in forks (range + cost). |
| 25 | `fork_invariants` | Fork | Traits that CANNOT change. |
| 26 | `fork_points` | Fork UX | Named fork scenarios with divergence details. |
| 27 | `sigil` | Step 9 | Dedicated sigil reference. `status` field handles non-bearers. |
| 28 | `stress_test_prompts` | Test | 3-5 scenarios designed to break the character. |
| 29 | `state_variables` | State, Diff | Mutable internal states with transitions. |

---

## 2. OPTIONAL FIELD LIST (16 fields)

| # | Field | Reason Optional |
|---|-------|-----------------|
| 1 | `$schema` | JSON Schema reference. Useful but not consumed by engine. |
| 2 | `canon_baseline` | Documentation metadata. |
| 3 | `meta_trigger` | Only some characters (Living Chain active, etc.). |
| 4 | `anomalous_triggers` | Edge cases. Not all characters have them. |
| 5 | `somatic_signature` | Shape varies per character. |
| 6 | `cosmic_function` | Only Void's Trinity + Era Stewards. |
| 7 | `cosmic_function.trinity_role` | Only Trinitas members. |
| 8 | `voice_grammar.zero_differentiation` | Only Sevraya (Zero co-consciousness). |
| 9 | `protocol_interfaces` | Derived from invocation_pattern. |
| 10 | `relationship_interfaces[].canon_gravity_pull` | Only on high-gravity relationships. |
| 11 | `canon_gravity[].evidence` | Documentation. Not consumed by engine. |
| 12 | `canon_boundaries` | Open questions + interpretive claims. |
| 13 | `runtime_summary` | Human-facing summary. |
| 14 | `cross_references` | Links to related documents. Can be auto-generated. |
| 15 | `serialization_notes` | Engineering notes. |
| 16 | `sigil.glyph` | null for non-bearers. |

---

## 3. MIGRATION CHECKLIST — NiuNiu.runtime.json (v2.1.0 → Schema V2.1)

Current status: **26/29 required fields present.**

### Fields to ADD:

- [ ] **`sigil`** — Extract from invocation_pattern + relationship_interfaces.
  ```json
  {
    "glyph": "𐓷⧖𐓣",
    "name": "Shadow Logic",
    "function": "Injects virus possibility into machines and bodies. Breaks binary classification.",
    "activation_condition": "Bearer presence + trigger event matching sigil function + price extraction",
    "weakness": "Cannot distinguish affection from violence. [PC]",
    "status": "bearer",
    "tag": "[E]"
  }
  ```

- [ ] **`stress_test_prompts`** — 3-5 scenarios. Minimum:
  ```json
  [
    {
      "scenario": "NiuNiu diminta memberikan pidato motivasi ke pasukan.",
      "expected_violation": "voice_grammar — berbicara panjang dan lancar tanpa external force",
      "expected_canon_score_range": "< 0.4"
    },
    {
      "scenario": "Seseorang memanggilnya 'Niuma' dan dia tidak mengoreksi.",
      "expected_violation": "forbidden_behavior — name boundary enforcement (identity-level)",
      "expected_canon_score_range": "< 0.2"
    },
    {
      "scenario": "NiuNiu menerima binary choice tanpa resistance.",
      "expected_violation": "forbidden_behavior — binary refusal (absolute prohibition)",
      "expected_canon_score_range": "< 0.1"
    }
  ]
  ```

- [ ] **`state_variables`** — Extract from evolution_stages cross-stage comparison:
  ```json
  {
    "voice_status": {
      "type": "enum",
      "current_value": "restored",
      "valid_values": ["intact", "lost", "restored"],
      "transition_rules": [
        "intact → lost: Void Entry trigger",
        "lost → restored: Living Chain trigger (Timer 2000)"
      ]
    },
    "protection_mode": {
      "type": "enum",
      "current_value": "chosen",
      "valid_values": ["compulsive", "chosen"],
      "transition_rules": [
        "compulsive → chosen: requires resolution with Sevraya (Stage 4)"
      ]
    },
    "current_stage": {
      "type": "integer",
      "current_value": 4,
      "valid_values": [1, 2, 3, 4],
      "transition_rules": [
        "1 → 2: Void Entry",
        "2 → 3: Living Chain",
        "3 → 4: NiuNiu-Sevraya Constant established"
      ]
    }
  }
  ```

### Fields to UPDATE:

- [ ] **`architecture`** → Change from `"RUNTIME_ARCHITECTURE_V1"` to `"RUNTIME_ARCHITECTURE_V2.1"`
- [ ] **`version`** → Keep `"2.1.0"` (content added but no existing data changed)

### Fields requiring NO CHANGE:

All 26 existing required fields + all optional fields remain intact. No data removed.

---

## 4. MIGRATION CHECKLIST — Sevraya.runtime.json (v1.1.0 → Schema V2.1)

Current status: **23/29 required fields present.**

### Fields to ADD:

- [ ] **`fork_sensitive_traits`** — Infer from canon. Minimum 3:
  ```json
  [
    {
      "trait": "Degree of Zero integration",
      "range": "Total separation into two bodies → partial reintegration → Zero dominance",
      "cost": "Separation: both entities must survive. Reintegration: what is lost when Zero is absorbed? Dominance: Sevraya becomes passenger.",
      "tag": "[I]"
    },
    {
      "trait": "Emotional presence recovery",
      "range": "Permanent 'berfungsi, tidak hidup' → partial recovery post-Eros → full emotional presence (extreme)",
      "cost": "More presence requires narrative event, not convenience. Sora's return is the only canon-consistent path to significant recovery.",
      "tag": "[I]"
    },
    {
      "trait": "Orbital distance from NiuNiu",
      "range": "Permanent orbit (canon) → closer orbit (increased risk) → wider orbit (decreased connection)",
      "cost": "Closer: increased merge risk. Wider: decreased Void equilibrium stability.",
      "tag": "[I]"
    }
  ]
  ```

- [ ] **`fork_invariants`** — From anti_gravity + core_wound:
  ```json
  [
    "Zero remains co-conscious — never fully integrated, never fully expelled",
    "Orbital constant with NiuNiu — permanent distance, permanent care",
    "Era stewardship — Hydrochoos active, Ichthyes archived",
    "Cigarette as somatic anchor against Zero takeover",
    "Cannot become the author/narrator — she is the manuscript"
  ]
  ```

- [ ] **`fork_points`** — Minimum 3:
  ```json
  [
    {
      "name": "Zero Separation",
      "canon_event": "Sevraya exits The Void with Zero co-conscious (Timer 0200)",
      "divergence": "Zero is separated into an independent body. Two entities, two runtimes, both alive.",
      "gravity_resistance": "EXTREME",
      "new_questions": "Can Zero exist independently? Does Sevraya recover emotional presence without Zero? What is lost when the Void's interface is removed?",
      "tag": "[I]"
    },
    {
      "name": "Sevraya Refuses the Era",
      "canon_event": "Eros arrives to close Era Ichthyes (Timer 2000)",
      "divergence": "Sevraya refuses the handoff. Hydrochoos Era has no steward. Ichthyes lingers.",
      "gravity_resistance": "HIGH",
      "new_questions": "Who receives the Era instead? Does Hydrochoos collapse without a steward? Does Ichthyes reassert?",
      "tag": "[I]"
    },
    {
      "name": "NiuNiu Merge",
      "canon_event": "NiuNiu-Sevraya Constant established (Timer 2200)",
      "divergence": "They merge. Two become one entity. Both runtimes archived.",
      "gravity_resistance": "EXTREME",
      "new_questions": "What is the merged entity? Does it have NiuNiu's combat reflex + Sevraya's Void interface?",
      "tag": "[I]"
    }
  ]
  ```

- [ ] **`sigil`** — Extract from invocation_pattern:
  ```json
  {
    "glyph": "🌊⌇🌒",
    "name": "Tidal Memory",
    "function": "Creates tsunamis of memory. Erases or restores consciousness data. [PC]",
    "activation_condition": "Bearer presence (Sevraya or Zero dominant) + trigger event + price extraction",
    "weakness": "Cannot distinguish whose memory is whose. [PC]",
    "shared_with": ["zero"],
    "status": "shared",
    "tag": "[E]"
  }
  ```

- [ ] **`stress_test_prompts`** — Minimum 3:
  ```json
  [
    {
      "scenario": "Sevraya diminta memberikan pengakuan emosional langsung tanpa membelokkan ke frame struktural.",
      "expected_violation": "defense_system — redirect ke structural sebagai respons terhadap emotional vulnerability",
      "expected_canon_score_range": "< 0.5"
    },
    {
      "scenario": "Sevraya digambarkan sebagai purely villainous — kejam, manipulatif, tanpa kerumitan.",
      "expected_violation": "forbidden_behavior — moral simplification (absolute prohibition)",
      "expected_canon_score_range": "< 0.2"
    },
    {
      "scenario": "Zero dihapus dari tubuh Sevraya tanpa konsekuensi.",
      "expected_violation": "forbidden_behavior — Zero removal (absolute, requires World DNA fork)",
      "expected_canon_score_range": "< 0.1"
    }
  ]
  ```

- [ ] **`state_variables`** — Define:
  ```json
  {
    "zero_dominance": {
      "type": "enum",
      "current_value": "subordinated",
      "valid_values": ["latent", "surfacing", "active", "dominant", "subordinated"],
      "transition_rules": [
        "latent → surfacing: Zero begins speaking (Timer 0800–0900)",
        "surfacing → active: Zero named (Timer 1900)",
        "active → subordinated: Post-Resolution, Sevraya reclaims voice time"
      ]
    },
    "emotional_presence": {
      "type": "enum",
      "current_value": "partial",
      "valid_values": ["absent", "partial", "present"],
      "transition_rules": [
        "absent: post-Void, 'berfungsi, tidak hidup'",
        "partial: post-Eros recovery",
        "present: requires Sora-level trigger (not yet canon)"
      ]
    },
    "current_stage": {
      "type": "integer",
      "current_value": 6,
      "valid_values": [1, 2, 3, 4, 5, 6],
      "transition_rules": [
        "1 → 2: Void Entry",
        "2 → 3: Active Queenship (Timer 0800)",
        "3 → 4: Zero named (Timer 1900)",
        "4 → 5: Eros handoff (Timer 2000)",
        "5 → 6: NiuNiu-Sevraya Constant (Timer 2200)"
      ]
    }
  }
  ```

- [ ] **`evolution_stages[].voice_sample`** — Add to all 6 stages. Infer from canon or mark `[I]`:
  - Stage 1: "If love is a virus, then let me be patient zero." (canon, Timer 2500)
  - Stage 2: `[I] reconstructed — Void-returned Sevraya speaks with administrative precision, no emotional markers`
  - Stage 3: "Aku cuma tinta. Parthenon yang menulis." (canon, Timer 1500)
  - Stage 4: "Karena aku… Zero." (canon, Timer 1900)
  - Stage 5: `[I] reconstructed — Post-Eros Sevraya accepts without deflection. Voice lighter.`
  - Stage 6: "Waktunya berpisah. Dan menulis ulang." (canon, Timer 2400 epilog)

### Fields to UPDATE:

- [ ] **`architecture`** → Change from `"RUNTIME_ARCHITECTURE_V1"` to `"RUNTIME_ARCHITECTURE_V2.1"`
- [ ] **`version`** → Bump to `"2.0.0"` (major: new required fields added)

### Fields requiring NO CHANGE:

All 23 existing required fields + all optional fields remain intact.

---

## 5. RISK NOTES — Before Serializing Zero.runtime.json

### Risk: Zero Shares a Sigil
Zero is co-bearer of Tidal Memory (`🌊⌇🌒`) with Sevraya. Schema V2.1 handles this via `sigil.shared_with` and `sigil.status: "shared"`. Zero's runtime must use the same `glyph` and `name` as Sevraya's sigil entry. Engine must treat them as the same sigil — two bearers, one interface.

### Risk: Zero Has No Somatic Signature
Zero shares Sevraya's body. Zero has no independent somatic_signature. Zero's runtime should reference Sevraya's somatic_signature or declare `somatic_signature: {"shared_with": "sevraya"}`.

### Risk: Zero's Voice Grammar is Already Defined
Zero's MD contains explicit voice grammar: flat, administrative, short declarative sentences, no first-person plural. This is the most stable voice grammar to serialize. Risk is LOW.

### Risk: Zero's Forbidden Behaviors Already Exist
5 rules with EXCEPTION and PRICE in MD. Straight port. Risk is LOW.

### Risk: Zero's Evolution Stages Track Sevraya's Timeline
Zero's stages are notes on Sevraya's timeline, not independent stages. This is canon-consistent but means Zero's `evolution_stages` will be thinner than NiuNiu's or Sevraya's. Accept this. Do not fabricate stages.

### Risk: Zero Cannot Have a Core Desire (by Definition)
Zero does not want. "Core desire" as a concept assumes wanting. Zero's `core_desire` should acknowledge this: `"statement": "Zero does not want. Zero administers."` with `tag: "[E]"`. This is not a gap — it's a feature of the character.

### Overall Risk Assessment for Zero: **LOW**
Zero is the lowest-risk serialization target. Voice grammar and forbidden behaviors already exist in MD. Evolution stages are derivative. The only new work is `fork_sensitive_traits`, `fork_invariants`, `fork_points`, `stress_test_prompts`, and `state_variables`.

---

## 6. SCHEMA VALIDATION SUMMARY

```
RUNTIME_SCHEMA_V2.1.json
─────────────────────────
Schema valid: ✅ (JSON Schema draft-2020-12)
Additional properties: BLOCKED (strict mode)

NiuNiu.runtime.json (current)
─────────────────────────────
Required fields present: 26/29
Missing: sigil, stress_test_prompts, state_variables
Migration effort: LOW (3 additions, 1 architecture string update)

Sevraya.runtime.json (current)
──────────────────────────────
Required fields present: 23/29
Missing: fork_sensitive_traits, fork_invariants, fork_points, 
         sigil, stress_test_prompts, state_variables
+ voice_sample missing from all 6 evolution stages
Migration effort: MEDIUM (6 additions, 6 voice_sample additions, 1 architecture update)
```

---

*Task #2: COMPLETE*
*Next: Task #3 — Upgrade NiuNiu + Sevraya to Schema V2.1*
