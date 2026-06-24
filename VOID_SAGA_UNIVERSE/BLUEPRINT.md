# VOID SAGA — EXECUTIVE BLUEPRINT v2.1.0

> **Status:** Revised architecture. Strategic reframing applied. 30/60 day roadmap defined.
> **Target:** Narrative Compiler MVP → CLI demo → Public web demo.
> **Prinsip:** The compiler is the product. The frontend is a client. What ships is better than what's complete.

---

# 0. STRATEGIC REFRAMING

## What This Is NOT

VOID_SAGA_UNIVERSE is not:

- ❌ A novel
- ❌ A wiki
- ❌ A lore database
- ❌ A storytelling website

## What This IS

**VOID_SAGA_UNIVERSE is a Narrative Operating System.**

The ultimate product is not a website. The ultimate product is a **Narrative Compiler** — a system capable of:

1. Loading character runtimes
2. Loading world states
3. Loading contracts and protocols
4. Evaluating canon constraints
5. Generating narrative possibilities through an LLM
6. Measuring canon deviation (canon score)
7. Producing canon-safe forks

The web application is only one possible interface. The compiler is the product. The frontend is a client.

## Long-Term Vision

Assume the final system eventually supports:

- Character simulation
- Canon-safe chat
- Fork generation
- Timeline divergence
- Contract validation
- State transition tracking
- Alternate reality branches
- Narrative version control

**The roadmap optimizes for reaching that future.**

It does not optimize for visual presentation. It optimizes for **executable narrative intelligence.**

## Architecture as Product

```
                        THE COMPILER (product)
                       ┌──────────────────────┐
                       │  Prompt → Constraint  │
                       │  → Generate → Score   │
                       └──────────┬───────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
    ┌─────────▼────────┐ ┌───────▼───────┐ ┌─────────▼────────┐
    │   CLI (client)   │ │ Web (client)  │ │ Discord (client) │
    │   Phase 7        │ │ Phase 8       │ │ Future           │
    └──────────────────┘ └───────────────┘ └──────────────────┘
```

All clients consume the same compiler. The compiler does not know which client is calling it. The compiler only knows: runtimes, contracts, world state, prompt → narrative + score.

---

# 1. EXECUTIVE SUMMARY

## What Changed From v1.0

The previous blueprint treated serialization, voice grammar, forbidden behaviors, World DNA, and protocols as a single monolithic Phase 1-2. That was wrong. It created schema instability risk and delayed the only thing that matters: **a working Narrative Compiler.**

This revision restructures the roadmap around one question:

> *What is the shortest path from current state to a system that accepts a prompt, loads character constraints, generates prose, validates output, and returns a canon score?*

## Key Corrections

| v1.0 Problem | v2.0 Fix |
|---|---| 
| Phase 1 bundled schema + serialization + expansion = 14 tasks in one phase | Split into 1A (schema only), 1B (serialization factory), 1C (expansion — voice/forbidden behaviors) |
| Phase 2 forced full World DNA + Protocol serialization before engine touched them | Replaced with minimal executable world model. Only serialize what the engine consumes. |
| No Narrative Compiler phase existed | **Phase 4: Narrative Compiler MVP** — the centerpiece of the entire roadmap |
| Web App at Phase 8, after API | Web App delayed to Phase 8. CLI demo at Phase 7 as public-facing milestone. |
| No Chapter Registry | Introduced in Phase 2A as bridge between canon narrative and executable state |
| World DNA formalization assumed equal priority to runtime | Corrected: runtime + contract + state are the execution-critical trio. Ontology is supporting documentation until the engine requires it. |

## Revised Architecture Target

```
┌──────────────────────────────────────────────────┐
│              WEB APP (Next.js)                   │  ← Phase 8
│              CLI DEMO (terminal)                 │  ← Phase 7
└─────────────────────┬────────────────────────────┘
                      │
┌─────────────────────▼────────────────────────────┐
│            NARRATIVE COMPILER                    │  ← Phase 4 ★
│  Prompt → Runtime Load → Constraint Evaluate     │
│  → LLM Generate → Validate → Canon Score         │
└─────────────────────┬────────────────────────────┘
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
┌────────────┐  ┌────────────┐  ┌────────────┐
│ CONSTRAINT │  │  CHAPTER   │  │   FORK     │    ← Phase 3, 2A, 5
│ ENGINE V2  │  │  REGISTRY  │  │  CATALOG   │
│ (multi-    │  │  (canon↔   │  │  (storage) │
│  runtime)  │  │  state)    │  │            │
└─────┬──────┘  └─────┬──────┘  └─────┬──────┘
      │               │               │
      └───────────────┼───────────────┘
                      ▼
┌──────────────────────────────────────────────────┐
│              DATA LAYER                          │  ← Phase 1A–1C, 2A
│  8 Runtime JSON · 6 Contract JSON               │
│  Minimal World Model · Chapter Registry          │
└──────────────────────────────────────────────────┘
```

---

# 2. REVISED ARCHITECTURE PRIORITIES

## What The Engine Actually Consumes

After auditing `engine.py` v0.3.0 and the 11-step pipeline in `CONSTRAINT_ENGINE_SPEC.md`, here is what the constraint engine actually reads:

| Data Type | Engine Usage | Priority |
|---|---|---|
| **Runtime JSON** | Identity invariants, defense triggers, forbidden behaviors, voice grammar, relationship interfaces | **CRITICAL** |
| **Contract JSON** | Allowed/forbidden states, violation rules, anti-gravity, trigger conditions | **CRITICAL** |
| **World State JSON** | Current timeline position, active runtimes, active contracts, residues | **CRITICAL** |
| **Chapter Registry** | Maps canon narrative positions to machine state. Needed for "fork from chapter X" to resolve. | **HIGH** |
| **World DNA (minimal)** | Era context, element constraints, world-level forbidden moves | **MEDIUM** |
| **Protocol JSON** | Boot sequence gates, protocol dependency chain | **MEDIUM** |
| **Full Ontology** | Void states, Zero co-consciousness mechanics, paradox deployment conditions, residue taxonomies | **LOW** (deferred) |

## Execution Dependency Chain

```
Runtime JSON ──┐
               ├──→ Constraint Engine V2 ──→ Narrative Compiler ──→ CLI Demo
Contract JSON ─┘        │                                              │
                        │                                              │
Chapter Registry ───────┘                                              │
                        │                                              │
World State Schema ─────┘                                              │
                                                                       │
Fork Catalog ─────────────────────────────────────────────────────────┘
                                                                       │
Web App ───────────────────────────────────────────────────────────────┘
```

**Rule:** Nothing goes into the engine that the engine doesn't ask for. Nothing goes into the Narrative Compiler that the engine can't validate.

---

# 3. REVISED DEVELOPMENT PHASES

---

## PHASE 1A: RUNTIME SCHEMA STABILIZATION

**Duration:** 3-5 hari
**Dependency:** None (uses existing NiuNiu + Sevraya JSON)
**Risk:** LOW — purely formal, no new content

### Purpose

Before serializing 6 additional runtimes, we need a single schema that:
- Is backward-compatible with NiuNiu.runtime.json (709 lines, V1-heritage)
- Is forward-compatible with Sevraya.runtime.json (516 lines, V2-heritage)
- Defines exactly which fields are required vs optional
- Is machine-validatable (JSON Schema standard)
- Can be loaded by `engine.py` without modification

### Deliverable

`apps/data/schemas/RUNTIME_SCHEMA_V2.1.json` — JSON Schema (draft-2020-12)

### Tasks

- [ ] **1A.1** Field audit: diff NiuNiu JSON fields vs Sevraya JSON fields vs V2 architecture spec. Produce gap matrix.
- [ ] **1A.2** Define unified field list: required fields, optional fields, field types, enum values where applicable.
- [ ] **1A.3** Write `RUNTIME_SCHEMA_V2.1.json`.
- [ ] **1A.4** Validate NiuNiu JSON against schema. Fix schema if needed. Do NOT modify runtime data.
- [ ] **1A.5** Validate Sevraya JSON against schema. Fix schema if needed. Do NOT modify runtime data.
- [ ] **1A.6** Write `SCHEMA_V2.1_MIGRATION_GUIDE.md` — documents what changed, why, and how to migrate existing runtimes.

### Exit Criteria

```
✅ RUNTIME_SCHEMA_V2.1.json exists and is valid JSON Schema
✅ NiuNiu.runtime.json passes validation (0 errors)
✅ Sevraya.runtime.json passes validation (0 errors)
✅ Migration guide written
✅ engine.py can load both runtimes without modification
```

---

## PHASE 1B: SERIALIZATION FACTORY

**Duration:** 2-3 minggu
**Dependency:** Phase 1A COMPLETE
**Risk:** MEDIUM — voice grammar and forbidden behaviors must be inferred from canon for some characters

### Purpose

Serialize all 6 remaining runtime Markdown files to validated JSON. No new canon research — extraction only. Where data is missing (voice grammar, forbidden behaviors), mark it `[I]` (inferred) and document the inference path.

### Scope — Per Character

Each runtime JSON must contain:
- Identity + core wound + primary contradiction
- Evolution stages with state variable registry
- Defense system with WHEN/THEN/COST patterns
- Voice grammar (even if `[I]` — must be structured)
- Forbidden behaviors with EXCEPTION and PRICE
- Relationship interfaces (with symmetry status)
- Invocation, cost, consequence, residue patterns
- Sigil (if bearer)
- Canon gravity items
- Anti-gravity items

### Serialization Priority

Ordered by engine dependency — who interacts with whom first:

| Priority | Character | Status | Challenge |
|---|---|---|---|
| **P1** | Zero | MD has voice grammar + forbidden behaviors. Straight port. | Low |
| **P2** | Julia | V2 MD exists. Voice grammar `[I]`. Forbidden behaviors absent. | Medium |
| **P3** | Delphie | V2 MD exists. Voice grammar `[I]`. Forbidden behaviors absent. | Medium |
| **P4** | Agnia | V2 MD exists. Voice grammar `[I]`. Forbidden behaviors absent. | Medium |
| **P5** | Gwaneum | V2 MD exists. Voice grammar `[I]`. Forbidden behaviors absent. | Medium |
| **P6** | Hasan | v0.5.0 compact. Missing Defense, Evolution, Failure sections. | High |

### Tasks

- [ ] **1B.1** Serialize Zero → `Zero.runtime.json`. Validate against schema. Load into engine, test 1 valid + 1 invalid scenario.
- [ ] **1B.2** Serialize Julia → `Julia.runtime.json`. Infer voice grammar from Timer canon. Write 8-10 forbidden behaviors. Validate + engine test.
- [ ] **1B.3** Serialize Delphie → `Delphie.runtime.json`. Infer voice grammar. Write forbidden behaviors. Validate + engine test.
- [ ] **1B.4** Serialize Agnia → `Agnia.runtime.json`. Infer voice grammar. Write forbidden behaviors. Validate + engine test.
- [ ] **1B.5** Serialize Gwaneum → `Gwaneum.runtime.json`. Infer voice grammar. Write forbidden behaviors. Validate + engine test.
- [ ] **1B.6** Serialize Hasan → `Hasan.runtime.json`. Infer evolution stages, defense system, voice grammar from feasibility audit + canon. Validate + engine test.
- [ ] **1B.7** Upgrade NiuNiu + Sevraya JSON to schema V2.1 (add missing fields, don't break existing).

### Exit Criteria

```
✅ 8 runtime JSON files in apps/data/runtimes/
✅ All 8 pass RUNTIME_SCHEMA_V2.1.json validation
✅ All 8 load into engine.py without error
✅ Each runtime has ≥1 valid and ≥1 invalid scenario that produces correct engine verdict
```

---

## PHASE 1C: RUNTIME EXPANSION

**Duration:** 1-2 minggu
**Dependency:** Phase 1B COMPLETE
**Risk:** LOW — enrichment of existing data, not new structures

### Purpose

Phase 1B got runtimes into machine-readable form. Phase 1C makes them *rich*. This is where we fill `[I]` gaps, add stress test prompts, and define state variable schemas.

### Tasks

- [ ] **1C.1** For each runtime: review all `[I]` (inferred) claims. Upgrade to `[E]` where canon evidence is found. Document remaining `[I]` claims with explicit resolution criteria.
- [ ] **1C.2** For each runtime: add `stress_test_prompts` — 3-5 scenarios designed to break the character. (Template field already exists, content missing.)
- [ ] **1C.3** For each runtime: add `state_variables` — mutable internal states with schema, valid values, and transition rules. (Currently only NiuNiu has this via evolution stage variable registry.)
- [ ] **1C.4** Cross-runtime consistency check: run all 8 JSONs through a pairwise relationship validator. Flag asymmetries. (e.g., if NiuNiu's relationship to Sevraya says "orbit" but Sevraya's to NiuNiu says "merge" → conflict.)

### Exit Criteria

```
✅ [I] claims documented with resolution paths
✅ Stress test prompts exist for all 8 runtimes (3-5 each)
✅ State variable schemas exist for all 8 runtimes
✅ Cross-runtime relationship audit clean (0 unresolved asymmetries)
```

---

## PHASE 2A: CHAPTER REGISTRY + MINIMAL WORLD MODEL

**Duration:** 1-2 minggu
**Dependency:** Phase 1A COMPLETE (Phase 1B/1C can run in parallel)
**Risk:** LOW — data mapping, no new engine logic

### Purpose

The engine can validate character behavior, but it doesn't know *where in the story* that behavior occurs. The Chapter Registry bridges canon narrative and executable state.

Additionally, we extract only the world-level rules the engine actually consumes — not the full ontology.

### 2A.1 Chapter Registry

**File:** `apps/data/content/chapter_registry.json`

Every chapter/timer entry:
```json
{
  "chapter_id": "bab-00-00",
  "title": "Genesis Error",
  "file_path": "../Bab 00-00.md",
  "chapter_type": "bab",
  "track": "terrestrial",
  "narrative_order": 1,
  "participants": ["gua", "lo"],
  "timer_equivalent": null,
  "boot_sequence_phase": null,
  "era": "ichthyes_terminal",
  "world_state_before": null,
  "world_state_after": null,
  "contracts_created": [],
  "residues_created": ["genesis.txt", "stealth_folder"],
  "fork_allowed": true,
  "fork_divergence_points": [
    "setting: kantor tech → alternatif",
    "gender: GUA/LO gender swap",
    "relationship: first contact berbeda"
  ]
}
```

**Tasks:**
- [ ] **2A.1.1** Map all ~50 chapter/timer files to structured entries
- [ ] **2A.1.2** Identify characters present per chapter
- [ ] **2A.1.3** Identify which boot sequence phase each Timer belongs to
- [ ] **2A.1.4** Identify residues created per chapter
- [ ] **2A.1.5** Identify contracts formed/broken per chapter
- [ ] **2A.1.6** Define fork divergence points per chapter (what can a user change?)
- [ ] **2A.1.7** Validate: all `file_path` values resolve to actual files on disk

### 2A.2 Minimal Executable World Model

**File:** `apps/data/world/world_executable.json`

Only what the engine needs:

```json
{
  "version": "1.0.0",
  "current_era": "hydrochoos",
  "eras": {
    "ichthyes": {"status": "TERMINATED", "voidos": "v4.13.8"},
    "hydrochoos": {"status": "ACTIVE", "voidos": "v6.6.6"}
  },
  "elements": {
    "udara": {"clans": ["didymoi", "zygos", "hydrochoos"]},
    "air": {"clans": ["karkinos", "vrishchik", "ichthyes"]},
    "api": {"clans": ["krios", "leon", "toxotes"]},
    "tanah": {"clans": ["tauros", "parthenos", "aigokeros"]},
    "void": {"clans": []}
  },
  "boot_sequence": [
    "void_entry",
    "sigil",
    "living_chain",
    "node",
    "paradox",
    "zero_node"
  ],
  "world_forbidden_moves": [
    "no_single_absolute_center",
    "void_not_just_villain",
    "grid_not_just_prison",
    "error_is_not_bug"
  ],
  "goetic_chain": [
    "name", "sigil", "invocation", "manifestation",
    "bargain", "binding", "consequence", "residue"
  ]
}
```

**Tasks:**
- [ ] **2A.2.1** Extract era definitions + lifecycle states
- [ ] **2A.2.2** Extract element → clan mapping
- [ ] **2A.2.3** Extract boot sequence dependency chain
- [ ] **2A.2.4** Extract world-level forbidden moves
- [ ] **2A.2.5** Extract Goetic chain process
- [ ] **2A.2.6** Validate: all references from runtime JSON resolve against this model

### Exit Criteria

```
✅ chapter_registry.json — all ~50 chapters mapped with metadata
✅ world_executable.json — engine-loadable world model
✅ All file_path references resolve to actual files
✅ Fork divergence points defined for every chapter
✅ Runtime references resolve against world model (e.g., "era": "hydrochoos" in runtime JSON matches world model)
```

---

## PHASE 3: CONSTRAINT ENGINE V2 — MULTI-RUNTIME

**Duration:** 2-3 minggu
**Dependency:** Phase 1B COMPLETE (need all runtime JSONs)
**Risk:** MEDIUM — extending pipeline from 1-2 to N runtimes

### Purpose

`engine.py` v0.3.0 handles single-runtime or pairwise contract evaluation. This phase extends it to the full 11-step pipeline defined in `CONSTRAINT_ENGINE_SPEC.md`, supporting N simultaneous participants with all active contracts, protocols, and world constraints.

### 3.1 Multi-Runtime Evaluator

**File:** `apps/engine/engine_v2.py`

**Tasks:**
- [ ] **3.1.1** Scenario loader: accept structured scenario with N participants, world state reference, requested action
- [ ] **3.1.2** Runtime resolver: given participant list, load all relevant runtime JSONs
- [ ] **3.1.3** Contract resolver: load all contracts where ≥2 of the participants appear
- [ ] **3.1.4** Identity invariant check per participant (Step 5)
- [ ] **3.1.5** Defense trigger check per participant (Step 6)
- [ ] **3.1.6** Relationship contract check for all pairs (Step 7)
- [ ] **3.1.7** Forbidden behavior check per participant (Step 8)
- [ ] **3.1.8** Protocol constraint check (Step 9) — boot sequence gating
- [ ] **3.1.9** Canon gravity check (Step 10) — world-level forbidden moves
- [ ] **3.1.10** Aggregator (Step 11): `{verdict: PASS|VIOLATION|WARNING, confidence: 0.0-1.0, violations: [...], warnings: [...], allowed_actions: [...], suggested_constraints: [...]}`

### 3.2 Contract Set Completion

**Tasks:**
- [ ] **3.2.1** `kiri_aku_kanan.contract.json` — Julia + NiuNiu tactical coherence
- [ ] **3.2.2** `twin_paradox.contract.json` — Agnia + NiuNiu stable incoherence
- [ ] **3.2.3** `saved_abandoned.contract.json` — Delphie + Gwaneum identity paradox
- [ ] **3.2.4** `merge.contract.json` — Julia + Delphie + Hasan triadic bond
- [ ] **3.2.5** `rose_lineage.contract.json` — Julia + Delphie + Gwaneum trinitas
- [ ] **3.2.6** N-party contract support in engine (currently only pairwise)
- [ ] **3.2.7** Contract conflict resolution: when two active contracts produce contradictory constraints

### 3.3 Validation Test Suite

**Tasks:**
- [ ] **3.3.1** 2-character canon scene (expected: PASS)
- [ ] **3.3.2** 3-character canon scene — Julia + Delphie + NiuNiu at Delta 4 (expected: PASS)
- [ ] **3.3.3** 6-character Living Chain scenario (expected: PASS with warnings)
- [ ] **3.3.4** 2-character canon violation — Sevraya tries to merge with NiuNiu (expected: VIOLATION)
- [ ] **3.3.5** 3-character contract conflict — two contracts produce opposite constraints (expected: WARNING with conflict report)
- [ ] **3.3.6** Forbidden move — character proposes world-level violation (expected: VIOLATION)

### Exit Criteria

```
✅ engine_v2.py loads N runtimes + contracts simultaneously
✅ Full 11-step pipeline operational
✅ 6 contracts validated + engine-loadable
✅ 6 test scenarios: expected verdicts match actual verdicts (100% accuracy)
✅ Contract conflict resolution operational
✅ Canon-safe mode vs forkable mode functional
```

---

## PHASE 4: NARRATIVE COMPILER MVP ★

**Duration:** 3-4 minggu
**Dependency:** Phase 3 COMPLETE (engine must handle multi-runtime)
**Risk:** HIGH — first integration of LLM with constraint system

### Purpose

This is the centerpiece. The Narrative Compiler accepts a user prompt, loads character constraints, calls Claude, validates output, and returns a canon-scored narrative.

This is not "AI writes a novel." This is **"constraint-bound narrative generation"** — the AI proposes, the engine disposes.

### 4.1 Prompt Compiler

**File:** `narrative_engine/prompt_compiler.py`

**Input:**
```json
{
  "characters": ["niuniu", "sevraya"],
  "world_state": "post_chain_world_state_v1",
  "situation": "NiuNiu and Sevraya in orbit around Aeonexus. Sevraya speaks first.",
  "mode": "canon_safe",
  "length": "scene"
}
```

**Output:** Complete Claude system prompt containing:
- Character identity + voice grammar + forbidden behaviors for each participant
- Active contracts between participants with allowed/forbidden states
- World context: era, location, current world state
- Structured output schema (JSON) for machine validation

**Tasks:**
- [ ] **4.1.1** Runtime-to-prompt converter: `runtime JSON → "You are [character]..." prose`
- [ ] **4.1.2** Contract-to-prompt converter: relationship rules as natural language constraints
- [ ] **4.1.3** World state injector: era, location, timeline position
- [ ] **4.1.4** Forbidden behaviors injector: HARD CONSTRAINTS — do not violate
- [ ] **4.1.5** Voice grammar injector: tone, sentence structure, vocabulary rules
- [ ] **4.1.6** Output schema injector: JSON Schema for structured narrative output
- [ ] **4.1.7** Context limits: ensure compiled prompt fits within Claude context window

### 4.2 Narrative Generator

**File:** `narrative_engine/generator.py`

**Tasks:**
- [ ] **4.2.1** Single-scene generation: 2 characters, 1 location, 1 situation
- [ ] **4.2.2** Multi-character scene: 3+ characters with turn-based dialogue
- [ ] **4.2.3** Structured output parsing: Claude returns JSON → extract narrative text + metadata
- [ ] **4.2.4** Context management: inject chapter context for canon-grounded generation
- [ ] **4.2.5** Retry logic: if Claude output doesn't conform to output schema, retry with correction

### 4.3 Narrative Validator

**File:** `narrative_engine/validator.py`

**Tasks:**
- [ ] **4.3.1** Claim extractor: from generated narrative, identify "who did what, who said what"
- [ ] **4.3.2** Per-claim constraint check via engine_v2.py
- [ ] **4.3.3** Voice consistency check: does each character's dialogue match their voice grammar?
- [ ] **4.3.4** Forbidden behavior check: did any character violate their forbidden behaviors?
- [ ] **4.3.5** Canon score computation: `1.0 - (violation_count * violation_weight) / total_claims`
- [ ] **4.3.6** Return structured verdict: `{canon_score, violations[], warnings[], suggestions[]}`

### 4.4 Compiler Pipeline (End-to-End)

**File:** `narrative_engine/compiler.py`

```
User Prompt
    │
    ▼
Prompt Compiler ──→ Runtime JSONs + Contracts + World State
    │
    ▼
Narrative Generator ──→ Claude API ──→ Raw Output
    │
    ▼
Narrative Validator ──→ engine_v2.py ──→ Verdict
    │
    ├── canon_score ≥ 0.8 → RETURN narrative + score
    │
    └── canon_score < 0.8 → Regenerate with violation feedback (max 3 attempts)
                              │
                              ├── improved → RETURN
                              └── still failing → RETURN with violations + "constraint conflict" warning
```

**Tasks:**
- [ ] **4.4.1** Build compiler pipeline
- [ ] **4.4.2** Implement regeneration loop (max 3 attempts)
- [ ] **4.4.3** Implement constraint conflict reporting (when regeneration can't resolve)
- [ ] **4.4.4** Log every compilation: prompt, raw output, validation result, canon score, regeneration count

### 4.5 MVP Test Suite

**Tasks:**
- [ ] **4.5.1** NiuNiu + Sevraya orbital scene (expected: canon_score ≥ 0.8)
- [ ] **4.5.2** Julia + NiuNiu tactical scene (expected: canon_score ≥ 0.8)
- [ ] **4.5.3** Delphie + Gwaneum identity confrontation (expected: canon_score ≥ 0.7)
- [ ] **4.5.4** NiuNiu long emotional monologue — should violate voice grammar (expected: canon_score < 0.5)
- [ ] **4.5.5** NiuNiu + Sevraya merge attempt — should violate forbidden behaviors (expected: canon_score < 0.3)
- [ ] **4.5.6** User fork: "GUA dan LO di dapur restoran" → generate Bab 00 variant (expected: canon_score ≥ 0.6, different from canon)

### Exit Criteria

```
✅ Prompt compiler produces valid Claude system prompts from runtime JSON
✅ Narrative generator produces structured JSON output from Claude
✅ Narrative validator computes canon_score from generated output
✅ Compiler pipeline: prompt → generate → validate → return (end-to-end)
✅ Regeneration loop operational (max 3 attempts)
✅ 6 test scenarios: 3 high-score, 2 low-score (correct rejection), 1 fork variant
✅ All outputs logged for audit
```

---

## PHASE 5: FORK CATALOG

**Duration:** 2-3 minggu
**Dependency:** Phase 4 COMPLETE (need compiler to generate forks)
**Risk:** LOW — standard CRUD + tree structure

### Purpose

Users can save forks (manual or AI-generated), browse forks by chapter, and navigate fork trees. This is the persistence layer the Narrative Compiler writes to.

### 5.1 Fork Database

**File:** `fork_system/database.py`
**Storage:** SQLite (`data/forks.db`)

**Schema:**
```sql
forks (
  fork_id TEXT PRIMARY KEY,
  created_by TEXT NOT NULL,
  created_at TEXT NOT NULL,
  source_chapter_id TEXT NOT NULL,
  fork_type TEXT NOT NULL,  -- 'manual' | 'ai_assisted'
  user_prompt TEXT,
  content TEXT NOT NULL,
  divergence_point TEXT NOT NULL,
  canon_score REAL,
  constraint_verdict TEXT,  -- JSON
  runtime_snapshot TEXT,    -- JSON
  parent_fork_id TEXT,
  public INTEGER DEFAULT 1
)
```

**Tasks:**
- [ ] **5.1.1** Database schema + migrations
- [ ] **5.1.2** Create fork (manual)
- [ ] **5.1.3** Create fork (AI-assisted — calls Narrative Compiler, saves result)
- [ ] **5.1.4** Read fork by ID
- [ ] **5.1.5** List forks by source chapter
- [ ] **5.1.6** List forks by author
- [ ] **5.1.7** Search forks (keyword, character, chapter)
- [ ] **5.1.8** Delete fork (author only)

### 5.2 Fork Tree

**Tasks:**
- [ ] **5.2.1** Tree builder: given a chapter_id, build nested fork tree
- [ ] **5.2.2** Tree statistics: depth, breadth, total nodes per branch
- [ ] **5.2.3** Canon distance: how many forks removed from canon?

### 5.3 Fork Coherence Validator

**Tasks:**
- [ ] **5.3.1** Declaration completeness check (5 required fields from FORK_PROTOCOL.md)
- [ ] **5.3.2** Wound consistency check
- [ ] **5.3.3** Voice integrity check
- [ ] **5.3.4** Canon boundary respect check
- [ ] **5.3.5** Coherence score: 0.0–1.0

### Exit Criteria

```
✅ Forks can be created, read, listed, searched, deleted
✅ AI-assisted fork creation calls Narrative Compiler end-to-end
✅ Fork tree query operational for any chapter
✅ Coherence validator returns structured score + concerns
```

---

## PHASE 6: API LAYER

**Duration:** 2-3 minggu
**Dependency:** Phase 5 COMPLETE (fork system must exist)
**Risk:** LOW — standard REST API over existing Python modules

### Purpose

Expose all backend logic through HTTP endpoints. This is the contract between backend and any future frontend (CLI, web, Discord bot).

### Framework: FastAPI

### Endpoints

#### Content
- `GET /api/v1/chapters` — list all chapters with metadata
- `GET /api/v1/chapters/{id}` — full chapter content (Markdown)
- `GET /api/v1/chapters/{id}/forks` — forks from this chapter
- `GET /api/v1/chapters/{id}/tree` — fork tree from this chapter

#### Compiler
- `POST /api/v1/compile` — run Narrative Compiler
  - Body: `{characters, world_state, situation, mode, length}`
  - Response: `{narrative, canon_score, violations, warnings}`

#### Forks
- `POST /api/v1/forks` — create fork (manual or AI-assisted)
- `GET /api/v1/forks/{id}` — read fork
- `DELETE /api/v1/forks/{id}` — delete fork
- `GET /api/v1/forks?author=X&chapter=Y` — search forks

#### Engine
- `POST /api/v1/engine/validate` — validate scenario without generation
- `GET /api/v1/engine/runtime/{character}` — get runtime summary
- `GET /api/v1/engine/world` — get world model summary

### Tasks

- [ ] **6.1** FastAPI app scaffold
- [ ] **6.2** Content endpoints
- [ ] **6.3** Compiler endpoint
- [ ] **6.4** Fork endpoints
- [ ] **6.5** Engine endpoints
- [ ] **6.6** Error handling + HTTP status codes
- [ ] **6.7** Rate limiting for `/compile` (Claude API cost)
- [ ] **6.8** OpenAPI/Swagger docs (auto-generated)
- [ ] **6.9** API integration tests

### Exit Criteria

```
✅ All endpoints documented via Swagger
✅ Content: read any chapter via API
✅ Compiler: prompt → narrative + canon_score via API
✅ Forks: CRUD via API
✅ Engine: validate scenario via API
✅ Rate limiting active on compilation endpoint
✅ Integration tests pass
```

---

## PHASE 7: CLI DEMO (PUBLIC MILESTONE)

**Duration:** 2-3 minggu
**Dependency:** Phase 6 COMPLETE (API must exist)
**Risk:** LOW — terminal UI over existing API

### Purpose

Before investing in a web frontend, ship a CLI tool that demonstrates the Narrative Compiler. This is the first thing actual humans will use. It must feel like magic.

### Experience

```
$ void compile "Julia ketemu NiuNiu di Delta 4 setelah 15 tahun"

⚡ Void.OS v6.6.6 — Narrative Compiler
─────────────────────────────────────
Characters: Julia Rose (Stage 2), NiuNiu (Stage 2)
World State: delta_4_post_dayan
Mode: canon_safe
─────────────────────────────────────

Generating...

─────────────────────────────────────
Julia menginjakkan kaki di Delta 4. Udara di sini selalu terasa
berbeda — lebih ringan, tapi juga lebih asing. Sudah 15 tahun.

NiuNiu sudah berdiri di ujung dermaga. Tidak bergerak. Tidak
menoleh. Panel di pergelangannya menyala: "Kau terlambat."

"Aku tahu," kata Julia. "Aku selalu terlambat."

─────────────────────────────────────
CANON SCORE: 0.87 ✅
Violations: 0
Warnings:
  • Julia's soldier reflex not triggered by proximity threat
    (acceptable in colony setting)
─────────────────────────────────────

Saved as fork #0034-delta. | View: void fork 0034-delta
```

### Commands

```
void compile "<prompt>"          Generate narrative from prompt
void validate "<scenario>"       Validate without generating
void read <chapter_id>           Read canon chapter
void fork <chapter_id>           Fork chapter (interactive)
void forks <chapter_id>          List forks
void tree <chapter_id>           View fork tree
void runtime <character>         View character runtime summary
void status                       Current world state summary
```

### Tasks

- [ ] **7.1** CLI scaffold (Click or Typer for Python)
- [ ] **7.2** `compile` command → calls Narrative Compiler via API
- [ ] **7.3** Formatted output: narrative + canon_score + violations + warnings
- [ ] **7.4** `read` command → formatted chapter display
- [ ] **7.5** `fork` command → interactive fork creation
- [ ] **7.6** `forks` + `tree` commands
- [ ] **7.7** `runtime` + `status` commands
- [ ] **7.8** Colorized output, progress indicators, error handling
- [ ] **7.9** `void --help` comprehensive help

### Exit Criteria

```
✅ All 8 commands operational
✅ compile command returns scored narrative
✅ Output is formatted, readable, and feels like "Void.OS"
✅ Error states handled gracefully
✅ Help text complete
✅ Tested by ≥1 human who is not the developer
```

---

## PHASE 8: WEB APP

**Duration:** 4-6 minggu
**Dependency:** Phase 7 COMPLETE (CLI validates the compiler + API works)
**Risk:** MEDIUM — frontend development scope

### Purpose

The CLI validated the system. The Web App makes it accessible to anyone with a browser. This is the distributed authorship platform.

### Tech Stack

- **Framework:** Next.js (App Router)
- **Styling:** Tailwind CSS
- **Theme:** Dark (Void aesthetic)
- **Hosting:** Vercel (free tier)
- **API:** Connects to Phase 6 FastAPI backend

### Pages

| Route | Page | Core Function |
|---|---|---|
| `/` | Library | All chapters, fork counts, search |
| `/read/[id]` | Reader | Chapter content + fork list + "Bikin versi kamu" button |
| `/fork/[id]` | Fork Creator | Two tabs: manual editor + AI prompt |
| `/fork/view/[fork_id]` | Fork Viewer | Read fork + fork-from-here |
| `/tree/[id]` | Fork Tree | Visual tree of all forks from a chapter |
| `/profile/[author]` | Profile | All forks by this author |

### States Per Page

Every page handles: **Loading** (skeleton), **Empty** (no data yet), **Error** (with retry), **Edge** (boundary cases).

### Components

- `ChapterCard` — metadata + fork count
- `ForkCard` — author, timestamp, canon_score badge, divergence
- `VoidButton` — primary action with glow
- `ConstraintBadge` — PASS/VIOLATION/WARNING with color
- `CanonScore` — numeric score with visual indicator
- `MarkdownRenderer` — dark-themed prose renderer
- `TreeVisualizer` — interactive fork tree (SVG/Canvas)
- `VoidSpinner` — loading animation

### Tasks

- [ ] **8.1** Next.js project scaffold + Tailwind + dark theme
- [ ] **8.2** Library page
- [ ] **8.3** Reader page
- [ ] **8.4** Fork Creator (Manual tab)
- [ ] **8.5** Fork Creator (AI tab)
- [ ] **8.6** Fork Viewer
- [ ] **8.7** Fork Tree
- [ ] **8.8** Profile page
- [ ] **8.9** Responsive design (mobile + desktop)
- [ ] **8.10** Deploy to Vercel

### Exit Criteria

```
✅ All 6 page types functional
✅ Manual fork creation works
✅ AI-assisted fork creation works (prompt → generate → preview → edit → save)
✅ Fork tree visual navigable
✅ Responsive on mobile
✅ Deployed to public URL
✅ Tested by ≥3 humans
```

---

## PHASE 9: POLISH & PUBLIC LAUNCH

**Duration:** 2-3 minggu
**Dependency:** Phase 8 COMPLETE
**Risk:** LOW

### Tasks

- [ ] **9.1** Content review: all chapters render correctly
- [ ] **9.2** Typography polish for long-form reading
- [ ] **9.3** Mobile reading experience optimization
- [ ] **9.4** OG images for social sharing
- [ ] **9.5** About page: explain distributed authorship concept
- [ ] **9.6** Contributor guide
- [ ] **9.7** Domain setup
- [ ] **9.8** Final test with 5-10 readers
- [ ] **9.9** Launch

---

# 4. NARRATIVE COMPILER MVP SPECIFICATION

## Input Contract

```json
{
  "characters": ["niuniu", "sevraya"],
  "world_state_ref": "post_chain_world_state_v1",
  "situation": "free text describing the scene context",
  "mode": "canon_safe | forkable",
  "length": "beat | scene | sequence",
  "chapter_context": "bab-00-00"  // optional: anchor to a canon chapter
}
```

## Output Contract

```json
{
  "narrative": "Full prose text in Void Saga style...",
  "canon_score": 0.0,
  "verdict": "PASS | PASS_WITH_WARNINGS | VIOLATION",
  "violations": [
    {
      "type": "forbidden_behavior | voice_grammar | contract | world_rule",
      "character": "niuniu",
      "rule_broken": "no_speaking_at_length_without_external_force",
      "offending_text": "...",
      "severity": "ERROR | WARNING"
    }
  ],
  "warnings": [
    {
      "type": "...",
      "message": "...",
      "recommendation": "..."
    }
  ],
  "regeneration_attempts": 1,
  "compilation_log_id": "comp_20260624_001"
}
```

## Canon Score Formula

```
canon_score = 1.0 — Σ(violation_weight × severity) / total_claims

Where:
  violation_weight = {
    forbidden_behavior: 0.4,
    contract: 0.3,
    voice_grammar: 0.2,
    world_rule: 0.5
  }
  severity = { ERROR: 1.0, WARNING: 0.5 }
  total_claims = number of character actions + dialogue lines in output
```

## Mode Behavior

| Mode | Constraint Strictness | Canon Gravity | Use Case |
|---|---|---|---|
| `canon_safe` | All constraints enforced. No relaxation. | FULL | Generating canon-compliant scenes |
| `forkable` | Identity invariants enforced. Some behavioral constraints relaxed. | PARTIAL | User creating alternate versions |

---

# 5. PUBLIC DEMO PATH

## Minimum Viable Demo (After Phase 7)

What ships: **CLI tool** that a friend can install and run.

```
pip install void-saga
void compile "NiuNiu ketemu Sevraya setelah Living Chain"
```

Experience: terminal. Output: prose + canon score. Feeling: Void.OS.

**This should exist before any web UI is built.**

## First Public Demo (After Phase 8)

What ships: **Website** at a public URL.

Reader experience: read canon chapters → click "Bikin versi kamu" → prompt or write → see result with canon score → save → others can read.

**This is the distributed authorship platform.**

---

# 6. RISK ANALYSIS

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **LLM cannot produce Void Saga voice** | MEDIUM | HIGH | Acceptable. The voice doesn't need to be Jali-level. It needs to be *bound by constraints*. The constraint engine is the product; the prose is the demo. |
| **Schema instability during Phase 1A** | LOW | HIGH | Only two existing runtimes to reconcile. 3-5 day timebox. If it takes longer, freeze schema and proceed with what works. |
| **Hasan runtime unsupported by canon** | MEDIUM | MEDIUM | v0.5.0 compact runtime is sufficient for Phase 1B. Full runtime can be deferred to Phase 1C or later. |
| **Claude API cost at scale** | LOW (near-term) | LOW | CLI demo has negligible cost. Web app with rate limiting keeps costs predictable. Not a concern until >100 DAU. |
| **Regeneration loop never converges** | MEDIUM | MEDIUM | Max 3 attempts hard limit. Return partial output with violations documented. "Constraint conflict" is a valid system output — it proves the engine works. |
| **Multi-runtime engine performance** | LOW | LOW | 8 runtimes × 6 contracts = small search space. No performance concern at this scale. |
| **Web app scope creep** | HIGH | MEDIUM | Phase 8 is the most vulnerable to feature creep. Enforce: "what the CLI does, but in a browser." No additional engine features during web phase. |

---

# 7. FINAL RECOMMENDATION

## Critical Path (What Must Ship)

```
Phase 1A (Schema) → Phase 1B (Serialization) → Phase 3 (Engine V2)
                                                      │
                                                      ▼
                                            Phase 4 (Narrative Compiler) ★
                                                      │
                                                      ▼
                                            Phase 7 (CLI Demo) ← FIRST PUBLIC THING
```

**Everything else is supporting infrastructure.** Phase 2A (Chapter Registry), Phase 1C (Runtime Expansion), Phase 5 (Fork Catalog), Phase 6 (API), Phase 8 (Web App) — all valuable, all deferred until the compiler works.

## What To Do Today

**Phase 1A, Task 1A.1 — Field audit: diff NiuNiu JSON vs Sevraya JSON vs V2 architecture spec.**

This requires zero new content. Two existing JSONs. One architecture doc. Produce a gap matrix showing exactly what fields exist, what's missing, and what the unified schema must support.

Estimated time: 1-2 hours.
Risk: zero. Reversible. Informational.

## What NOT To Do

- ❌ Do not write new World DNA documents until the compiler asks for them
- ❌ Do not design the web UI until the CLI works
- ❌ Do not build the API until the compiler produces valid output
- ❌ Do not serialize protocols until the engine requires protocol gating
- ❌ Do not aim for Jali-quality prose from the LLM — aim for constraint-correct prose
- ❌ Do not add features during Phase 8 (web app) that aren't in the CLI

---

# PHASE SUMMARY TABLE

| Phase | Name | Duration | Depends On | Risk | Output |
|---|---|---|---|---|---|
| **1A** | Schema Stabilization | 3-5 hari | — | LOW | `RUNTIME_SCHEMA_V2.1.json` |
| **1B** | Serialization Factory | 2-3 minggu | 1A | MEDIUM | 8 runtime JSON validated |
| **1C** | Runtime Expansion | 1-2 minggu | 1B | LOW | Stress tests + state variables |
| **2A** | Chapter Registry + World Model | 1-2 minggu | 1A | LOW | `chapter_registry.json` + `world_executable.json` |
| **3** | Constraint Engine V2 | 2-3 minggu | 1B | MEDIUM | `engine_v2.py` + 6 contracts |
| **4** | Narrative Compiler MVP ★ | 3-4 minggu | 3 | HIGH | `compiler.py` end-to-end |
| **5** | Fork Catalog | 2-3 minggu | 4 | LOW | SQLite fork DB |
| **6** | API Layer | 2-3 minggu | 5 | LOW | FastAPI server |
| **7** | CLI Demo | 2-3 minggu | 6 | LOW | `void` CLI tool |
| **8** | Web App | 4-6 minggu | 7 | MEDIUM | Next.js deployed |
| **9** | Polish & Launch | 2-3 minggu | 8 | LOW | Public launch |

**Critical path to first demo (1A → 1B → 3 → 4 → 7): ~12-18 minggu**

---

---

# 8. ROADMAP TO NARRATIVE COMPILER MVP — 30/60 DAYS

> **Assumptions:** Single primary developer. Existing engine works. Serialization pattern exists (NiuNiu, Sevraya). Validation reports exist. Limited time, limited resources. Prioritize demonstrable compiler over architectural perfection.

---

## 8.1 DAY 0 — Current State

### What Exists Today

**Engine (working code):**
- `engine.py` v0.3.0 — constraint evaluator. Single runtime + pairwise contract mode.
- `state_diff.py` v0.1.0 — compares two world state snapshots. Detects 23 change types.
- Contract-first mode operational. Runtime-derived contract generation as fallback.

**Data (production-ready JSON):**
- `NiuNiu.runtime.json` — 709 lines, 65 evidence, 4 stages, voice grammar, 7 relationships, 7 forbidden behaviors
- `Sevraya.runtime.json` — 516 lines, 60 evidence, 6 stages, voice grammar + Zero differentiation, 8 forbidden behaviors
- `orbital_constant.contract.json` — 3 allowed states, 5 forbidden, 3 triggers, confidence 0.92
- `PRE_CHAIN_WORLD_STATE_V1.json` — 7 runtimes, 4 contracts, 2 protocols, 18 residues
- `POST_CHAIN_WORLD_STATE_V1.json` — 7 runtimes, 4 contracts, 3 protocols, 25 residues

**Scenarios (test data):**
- `valid_delphie_protection.json` — PASS
- `invalid_sevraya_approach.json` — VIOLATION_DETECTED
- `orbital_constant_valid.json` — PASS
- `orbital_contract_violation.json` — TEST_PASS

**Execution Reports (validated):**
- `KIRI_AKU_KANAN_RUN_001.md` — coherence contract: PASS
- `ORBITAL_CONSTANT_RUN_001.md` — distance contract: PASS
- `ORBITAL_CONTRACT_VIOLATION_RUN_001.md` — negative test: TEST_PASS
- `SAVED_ABANDONED_RUN_001.md` — identity paradox: PASS
- `TWIN_PARADOX_RUN_001.md` — contradiction contract: PASS

**Specifications (blueprint):**
- `CONSTRAINT_ENGINE_SPEC.md` — 540-line, 11-step pipeline, 8 constraint types
- `WORLD_STATE_SPEC.md` — world state schema
- `STATE_DIFF_ENGINE_SPEC.md` — diff engine spec
- `RUNTIME_SERIALIZATION.md` — JSON schema definitions for all data types
- `CHARACTER_CHAT_APP.md` — app spec

**Kernel:**
- `BOOT_SEQUENCE.md` — 6-phase pipeline invariant
- `SYSTEM_MAP.md` — complete system topology

**Character Runtimes (Markdown, not yet JSON):**
- Julia, Delphie, Agnia, Gwaneum, Hasan, Zero — V2 architecture MD files with audit reports

### What Does NOT Exist

- ❌ Unified runtime JSON schema (NiuNiu V1-heritage, Sevraya V2-heritage — not aligned)
- ❌ Runtime JSON for Julia, Delphie, Agnia, Gwaneum, Hasan, Zero
- ❌ Multi-runtime engine (>2 characters evaluated simultaneously)
- ❌ LLM integration (no Claude API calls from engine)
- ❌ Narrative compiler (prompt → constraint → generate → validate → score)
- ❌ Chapter registry (machine-readable index of canon chapters)
- ❌ Fork storage
- ❌ Any user interface

---

## 8.2 DAY 30 — Target State

### What Must Exist After 30 Days

**1. Unified Runtime Schema (from Phase 1A)**
- `RUNTIME_SCHEMA_V2.1.json` validated against both NiuNiu and Sevraya
- Migration guide written
- All future serialization uses this schema

**2. Five Runtime JSONs Total**
- NiuNiu ✅ (existing, upgraded to V2.1)
- Sevraya ✅ (existing, upgraded to V2.1)
- Zero ✅ (new — lowest effort, voice grammar + forbidden behaviors already in MD)
- Julia ✅ (new — voice grammar inferred, forbidden behaviors written)
- Delphie ✅ (new — voice grammar inferred, forbidden behaviors written)

**3. Multi-Runtime Engine (Phase 3 — first milestone)**
- `engine_v2.py` loads up to 5 runtimes simultaneously
- Pairwise contract resolution for all loaded characters
- Identity invariant + defense trigger + forbidden behavior checks operational
- Tested: 2-character canon scene (PASS), 3-character canon scene (PASS), 2-character violation (correct REJECT)

**4. Narrative Compiler — First Light (Phase 4 — prototype)**
- Single-scene, 2-character generation working end-to-end
- Pipeline: user prompt → prompt compiler (runtime→system prompt) → Claude API → parse output → constraint validate → canon score
- Tested with: NiuNiu + Sevraya orbital scene, Julia + NiuNiu tactical scene
- Canon score computed and returned
- Violations detected and reported

**5. Minimal Chapter Registry (Phase 2A — first 15 entries)**
- Bab 00:00 through Bab 03:59 + Timer 0000 through Timer 0300 mapped
- Enough to support "fork from any early chapter"

### Day 30 Deliverables

```
✅ RUNTIME_SCHEMA_V2.1.json
✅ 5 runtime JSONs (NiuNiu, Sevraya, Zero, Julia, Delphie)
✅ engine_v2.py — multi-runtime evaluation (up to 5 participants)
✅ compiler.py — first working prototype (prompt → narrative + canon_score)
✅ chapter_registry.json — first 15 entries
✅ 3 compiler test runs documented (2 PASS, 1 correct REJECT)
```

### Day 30 — What Is NOT Expected

- ❌ All 8 runtimes serialized (Agnia, Gwaneum, Hasan deferred to Day 60)
- ❌ Regeneration loop (single-pass generation only)
- ❌ Fork catalog
- ❌ API layer
- ❌ CLI tool
- ❌ Any UI

---

## 8.3 DAY 60 — Target State

### What Must Exist After 60 Days

**1. All 8 Runtime JSONs Serialized + Validated**
- Agnia, Gwaneum, Hasan added
- All 8 pass schema validation
- All 8 load into engine without error
- Cross-runtime relationship audit clean

**2. Constraint Engine V2 Complete**
- Full 11-step pipeline from `CONSTRAINT_ENGINE_SPEC.md`
- 6 contracts operational (orbital_constant + kiri_aku_kanan + twin_paradox + saved_abandoned + merge + rose_lineage)
- N-party contract support (triadic Merge, Trinitas Rose)
- Contract conflict resolution (when two active contracts produce contradictory constraints)
- Test suite: 6 scenarios, 100% expected verdict accuracy

**3. Narrative Compiler MVP — Full Pipeline**
- Prompt compiler: runtime + contract + world state → Claude system prompt
- Narrative generator: structured JSON output from Claude
- Narrative validator: claim extraction → constraint check → voice check → canon score
- **Regeneration loop**: generate → validate → if canon_score < 0.8, regenerate with violation feedback (max 3 attempts)
- Constraint conflict reporting: when regeneration cannot resolve
- Compilation log: every run logged for audit

**4. Chapter Registry Complete**
- All ~50 chapters/timers mapped
- Fork divergence points defined per chapter

**5. Fork Catalog (Basic)**
- SQLite database: create, read, list, search forks
- AI-assisted fork: calls Narrative Compiler, saves result
- Fork tree query: get all forks from a chapter, nested

**6. CLI Demo Tool**
- `void compile "<prompt>"` — working end-to-end
- `void read <chapter>` — formatted output
- `void forks <chapter>` — list
- `void tree <chapter>` — tree view
- `void runtime <character>` — summary
- `void status` — world state summary
- Tested by ≥1 human who is not the developer

**7. Compiler Test Suite**
- 6 test scenarios documented:
  - 3 high-score (≥0.8): NiuNiu+Sevraya orbit, Julia+NiuNiu tactical, Delphie+Gwaneum confrontation
  - 2 low-score (correct rejection): NiuNiu emotional monologue, NiuNiu+Sevraya merge attempt
  - 1 fork variant: "GUA dan LO di dapur restoran"

### Day 60 Deliverables

```
✅ 8 runtime JSONs — all validated, all engine-loadable
✅ engine_v2.py — full 11-step pipeline, 6 contracts, N-party support
✅ compiler.py — full pipeline with regeneration loop
✅ chapter_registry.json — all ~50 chapters mapped
✅ forks.db — SQLite fork catalog operational
✅ void CLI — 8 commands operational
✅ 6 compiler test scenarios documented
✅ Tested by ≥1 human
```

### Day 60 — What Is NOT Expected

- ❌ Web application
- ❌ API layer (CLI calls Python modules directly)
- ❌ Full ontology serialization (World DNA beyond `world_executable.json`)
- ❌ Protocol execution engine (protocols used as constraint references only)

---

## 8.4 CRITICAL PATH

Tasks that absolutely must happen. In exact order.

```
WEEK 1-2: FOUNDATION
─────────────────────
  □ Schema audit: NiuNiu JSON vs Sevraya JSON → gap matrix
  □ Write RUNTIME_SCHEMA_V2.1.json
  □ Validate both existing runtimes against schema
  □ Upgrade NiuNiu + Sevraya to V2.1
  □ Serialize Zero → Zero.runtime.json (fastest — voice + forbidden exist)
  □ Serialize Julia → Julia.runtime.json

WEEK 3-4: ENGINE UPGRADE
─────────────────────────
  □ Build engine_v2.py: multi-runtime loader (up to 5 runtimes)
  □ Implement identity invariant + defense trigger + forbidden behavior checks
  □ Write kiri_aku_kanan.contract.json + twin_paradox.contract.json
  □ Test: 2-char PASS, 3-char PASS, 2-char correct REJECT
  □ Serialize Delphie → Delphie.runtime.json

WEEK 5-6: COMPILER — FIRST LIGHT
─────────────────────────────────
  □ Build prompt_compiler.py: runtime + contract → Claude system prompt
  □ Build generator.py: call Claude API, parse structured output
  □ Build validator.py: extract claims → constraint check → canon score
  □ Build compiler.py: pipeline end-to-end
  □ Test: NiuNiu+Sevraya orbit (expect ≥0.8), merge attempt (expect <0.3)
  □ Write first 15 chapter_registry.json entries

WEEK 7-8: COMPILER — FULL PIPELINE + REMAINING RUNTIMES
────────────────────────────────────────────────────────
  □ Add regeneration loop (max 3 attempts)
  □ Add constraint conflict reporting
  □ Serialize Agnia → Agnia.runtime.json
  □ Serialize Gwaneum → Gwaneum.runtime.json
  □ Serialize Hasan → Hasan.runtime.json
  □ Cross-runtime relationship audit
  □ Complete remaining 3 contracts

WEEK 9-10: FORK CATALOG + CLI
──────────────────────────────
  □ SQLite fork database: schema + CRUD
  □ AI-assisted fork: compiler → save
  □ Fork tree query
  □ Complete chapter_registry.json (all ~50 chapters)
  □ Build void CLI: compile, read, fork, forks, tree, runtime, status
  □ 6 compiler test scenarios documented

WEEK 11-12: BUFFER + HARDEN
─────────────────────────────
  □ Buffer week for overflow from weeks 1-10
  □ Test with ≥1 human
  □ Fix issues found
  □ Document everything
  □ DEMO READY
```

---

## 8.5 NICE-TO-HAVE (Deferred Past Day 60)

These are valuable but NOT on the critical path to a demonstrable compiler:

- ❌ Full World DNA JSON bundle (use `world_executable.json` minimal model instead)
- ❌ Protocol JSON bundle (protocols referenced as prose constraints, not executable)
- ❌ Runtime stress test prompts (Phase 1C)
- ❌ Runtime state variable schemas (Phase 1C)
- ❌ [I] → [E] claim upgrades (Phase 1C)
- ❌ API layer (FastAPI) — CLI calls modules directly
- ❌ Web application — Phase 8, after CLI validated
- ❌ Discord bot
- ❌ Multi-chapter narrative generation (single-scene only for MVP)
- ❌ Character simulation / autonomous mode
- ❌ Timeline divergence engine

---

## 8.6 RISKS

### Risk 1: LLM Voice Quality
**Risk:** Claude cannot produce prose that feels like Void Saga, even with constraint injection.
**Likelihood:** MEDIUM
**Impact:** The compiler works (constraints enforced, canon score computed) but the output feels generic.
**Mitigation:** **This is acceptable for MVP.** The compiler's job is constraint enforcement + canon scoring, not Jali-quality prose. The demo proves the system works. Voice quality improves with prompt engineering over time.
**Fallback:** If voice is completely wrong, narrow demo to "canon score calculator" — show that the engine correctly identifies violations. That alone proves the architecture.

### Risk 2: Regeneration Loop Never Converges
**Risk:** Generated output consistently scores < 0.8, regeneration with violation feedback doesn't improve scores.
**Likelihood:** MEDIUM
**Impact:** User experience degrades — constant "constraint conflict" warnings.
**Mitigation:** Max 3 attempts hard limit. Return best attempt with violations documented. "Constraint conflict" is a valid system output — it proves the engine works. The demo narrative: "Look — the system correctly refuses to let NiuNiu give a speech."
**Fallback:** For demo, pre-select prompts known to produce high scores. Ship with a "demo script" of 5 prompts that work well.

### Risk 3: Schema Drift During Serialization
**Risk:** Character 5 (Gwaneum) requires a field not in the schema. Schema must be revised. Earlier runtimes must be re-validated.
**Likelihood:** MEDIUM
**Impact:** Ripple effect — every schema change requires re-validation of all previously serialized runtimes.
**Mitigation:** Schema V2.1 designed to be maximally permissive (optional fields preferred over required). Serialize in order of complexity: Zero (simplest) → Julia → Delphie → Agnia → Gwaneum → Hasan (hardest). If schema must change, change it early.
**Fallback:** Freeze schema after Zero + Julia + Delphie. Remaining 3 runtimes can be serialized with `[I]` markers for fields that don't fit.

### Risk 4: Hasan Runtime Insufficient Canon Evidence
**Risk:** Hasan's compact runtime (v0.5.0) lacks Defense System, Evolution Stages, and Failure Mode. Inference from canon may be too speculative.
**Likelihood:** HIGH
**Impact:** Hasan.runtime.json exists but with heavy `[I]` markers. Engine may produce false positives or miss violations.
**Mitigation:** Accept that Hasan is a partial runtime for MVP. Document what can and cannot be validated. Focus compiler demo on characters with complete runtimes (NiuNiu, Sevraya, Zero, Julia, Delphie).
**Fallback:** Exclude Hasan from MVP compiler scenarios. 7 runtimes is sufficient for demo.

### Risk 5: Single Developer Bottleneck
**Risk:** One person doing schema design + serialization + engine development + LLM integration + CLI + testing. Progress blocked if developer is blocked.
**Likelihood:** HIGH
**Impact:** Timeline slips.
**Mitigation:** Claude Code assists with all code generation. Serialization is mechanical (MD → JSON) — AI can do 80% of the work. Human reviews. Developer focuses on architecture decisions + testing.
**Fallback:** Reduce scope. Day 60 target becomes: 5 runtimes + compiler prototype + CLI. Not all 8. Not fork catalog. Ship what works.

---

## 8.7 RECOMMENDED DEVELOPMENT SEQUENCE

### The Exact Order Work Should Be Executed

```
□ 1. Schema Audit (1-2 hours)
      Diff NiuNiu.runtime.json vs Sevraya.runtime.json vs RUNTIME_ARCHITECTURE_V2.md.
      Produce gap matrix. Identify exactly which fields are shared, which differ,
      which are missing.
      FILE: SCHEMA_GAP_MATRIX.md

□ 2. Write RUNTIME_SCHEMA_V2.1.json (2-4 hours)
      Based on gap matrix. Maximally permissive. Optional fields preferred.
      Validate against NiuNiu + Sevraya. Fix schema until both pass.
      FILE: apps/data/schemas/RUNTIME_SCHEMA_V2.1.json

□ 3. Upgrade NiuNiu + Sevraya to V2.1 (2-3 hours)
      Add missing fields. Do not remove or change existing data.
      Re-validate. Re-test in engine.py.
      FILES: NiuNiu.runtime.json, Sevraya.runtime.json (updated)

□ 4. Serialize Zero (1 day)
      Easiest — voice grammar + forbidden behaviors already in MD.
      Convert to JSON. Validate against schema. Test in engine.
      FILE: Zero.runtime.json

□ 5. Serialize Julia (2-3 days)
      Infer voice grammar from Timer canon. Write 8-10 forbidden behaviors.
      Convert V2 MD fields to JSON. Validate. Test.
      FILE: Julia.runtime.json

□ 6. Build engine_v2.py — Multi-Runtime Loader (3-4 days)
      Extend engine.py to load N runtimes simultaneously.
      Implement: identity check, defense trigger check, forbidden behavior check.
      Test with 2-char and 3-char scenarios using NiuNiu + Sevraya + Zero.
      FILE: apps/engine/engine_v2.py

□ 7. Write kiri_aku_kanan.contract.json + twin_paradox.contract.json (1-2 days)
      Based on execution reports (KIRI_AKU_KANAN_RUN_001, TWIN_PARADOX_RUN_001).
      Validate via engine_v2.
      FILES: 2 new contract JSONs

□ 8. Serialize Delphie (2-3 days)
      Same process as Julia. Voice grammar from canon.
      FILE: Delphie.runtime.json

□ 9. Build prompt_compiler.py (2-3 days)
      Runtime JSON + contract JSON → Claude system prompt string.
      Must fit within Claude context window.
      Must produce structured output schema for response parsing.
      FILE: narrative_engine/prompt_compiler.py

□ 10. Build generator.py (1-2 days)
       Call Claude API with compiled prompt.
       Parse structured JSON response.
       Handle malformed responses (retry).
       FILE: narrative_engine/generator.py

□ 11. Build validator.py (2-3 days)
       Extract claims from generated narrative.
       Feed claims through engine_v2.
       Compute canon score.
       Return violations + warnings.
       FILE: narrative_engine/validator.py

□ 12. Build compiler.py — Pipeline Integration (1-2 days)
       Wire prompt_compiler → generator → validator.
       Single-pass (no regeneration yet).
       Log everything.
       FILE: narrative_engine/compiler.py

□ 13. First Compiler Test (1 day)
       NiuNiu + Sevraya orbital scene. Expect ≥0.8.
       NiuNiu + Sevraya merge attempt. Expect <0.3.
       Document results.
       FILE: COMPILER_FIRST_LIGHT_REPORT.md

□ 14. First 15 Chapter Registry Entries (1 day)
       Bab 00:00 → Bab 03:59 + Timer 0000 → Timer 0300.
       FILE: apps/data/content/chapter_registry.json

□ 15. Serialize Agnia (2 days)
       FILE: Agnia.runtime.json

□ 16. Serialize Gwaneum (2 days)
       FILE: Gwaneum.runtime.json

□ 17. Serialize Hasan (2-3 days)
       Most complex. Accept [I] markers for unsupported sections.
       FILE: Hasan.runtime.json

□ 18. Complete Remaining Contracts (2 days)
       saved_abandoned.contract.json, merge.contract.json, rose_lineage.contract.json
       FILES: 3 new contract JSONs

□ 19. Add Regeneration Loop to Compiler (1-2 days)
       Max 3 attempts. Violation feedback injected into retry prompt.
       Constraint conflict reporting.
       UPDATE: narrative_engine/compiler.py

□ 20. Complete Chapter Registry (1 day)
       All ~50 entries.
       UPDATE: apps/data/content/chapter_registry.json

□ 21. Cross-Runtime Audit (1 day)
       Pairwise relationship check. Flag asymmetries.
       FILE: CROSS_RUNTIME_AUDIT_REPORT.md

□ 22. Build Fork Database (1-2 days)
       SQLite schema. CRUD. AI-assisted fork (compiler → save).
       FILE: fork_system/database.py

□ 23. Build void CLI (2-3 days)
       All 8 commands.
       FILE: void (CLI entry point)

□ 24. Compiler Test Suite (1-2 days)
       6 scenarios: 3 high-score, 2 low-score, 1 fork variant.
       All documented with expected vs actual canon scores.
       FILE: COMPILER_TEST_SUITE.md

□ 25. Human Testing + Fixes (2-3 days)
       ≥1 human tests CLI and compiler.
       Fix issues found.
       FILE: TEST_FEEDBACK_REPORT.md

□ 26. DEMO READY
```

---

## 8.8 TOTAL EFFORT ESTIMATE

| Week | Major Milestone | Effort |
|------|----------------|--------|
| 1 | Schema + Zero + Julia | Schema audit, V2.1, upgrade existing, serialize 2 runtimes |
| 2 | Engine V2 + Contracts | Multi-runtime engine, 2 new contracts, Delphie runtime |
| 3 | Compiler First Light | Prompt compiler, generator, validator, pipeline integration |
| 4 | First Light Test + Registry | Compiler test, chapter registry first 15, buffer |
| 5 | Remaining Runtimes | Agnia, Gwaneum, Hasan serialized |
| 6 | Compiler Full Pipeline | Regeneration loop, remaining contracts, cross-runtime audit |
| 7 | Fork Catalog + Registry Complete | SQLite fork DB, complete chapter registry |
| 8 | CLI Tool | All 8 commands, formatted output |
| 9 | Test Suite + Buffer | Compiler test suite, human testing, buffer for overflow |
| 10 | Harden + Demo | Fix issues, document, demo prep |
| 11-12 | Buffer | Overflow protection |

**Total: 10-12 weeks to Day 60 demo.**

---

*Blueprint version: 2.1.0 — Strategic Reframing + 30/60 Day Roadmap*
*Dibuat: 24 Juni 2026*
*Last revised: 24 Juni 2026*
