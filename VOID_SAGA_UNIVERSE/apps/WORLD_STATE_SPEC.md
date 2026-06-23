# WORLD STATE ARCHITECTURE

> **Phase:** 14H — Design Document
> **Status:** Specification
> **Purpose:** Define machine-readable representation of a living Void Saga world state
> **Dependency:** Phase 14G (Contract-First Engine), Phase 12 (Runtimes), Phase 11 (Protocols)

---

## 1 — Scope

### What World State Tracks

A world state object answers one question: **"What currently exists in this universe?"**

It tracks:
- Which runtimes are active, dormant, or removed
- Which contracts are formed, broken, or unknown
- Which protocols have been executed (and what residue they left)
- Which residues persist in the world (from invocations, contracts, and character wounds)
- Where in the timeline the snapshot was taken (boot sequence phase, timer reference)

### What World State Does NOT Track

- Story progression or plot
- Scene descriptions or dialogue
- Author intent or narrative direction
- Renderer output or generated text
- Emotional states not encoded as residue
- Future possibilities or predictions

### Relationship to Other Components

| Component | World State's Role |
|-----------|-------------------|
| **Runtimes** | World state says which runtimes are loaded and at which evolution stage |
| **Contracts** | World state says which contracts are active, broken, or pending |
| **Protocols** | World state says which protocol phases have been executed |
| **Residues** | World state registers all persistent residues produced by invocations |
| **Engine** | Engine loads world state to know what constraints are active before evaluating a scenario |
| **Renderer** | Renderer queries world state to know who is present and what state they are in |

---

## 2 — World State Object

### JSON Structure

```json
{
  "world_id": "string (e.g., 'post_chain_canon', 'pre_dayan_fork')",
  "version": "string (semver)",
  "snapshot_timestamp": "ISO 8601",
  "snapshot_description": "string (human-readable context)",
  "canon_mode": "canon | fork | experimental",
  "timeline": {
    "boot_sequence_phase": "number (0 = pre, 1-6)",
    "timer_reference": "string (e.g., 'Timer 2000')",
    "pre_chain": "boolean",
    "post_resolution": "boolean",
    "description": "string"
  },
  "active_runtimes": [
    {
      "runtime_id": "string",
      "evolution_stage": "number",
      "status": "active | dormant | removed",
      "active_residues": ["string (residue_ids carried by this runtime)"]
    }
  ],
  "active_contracts": [
    {
      "contract_id": "string",
      "status": "active | inactive | broken | unknown"
    }
  ],
  "active_protocols": [
    {
      "protocol_id": "string",
      "phase": "number | null",
      "status": "executed | active | pending | not_applicable",
      "residues_produced": ["string (residue_ids)"]
    }
  ],
  "active_residues": [
    {
      "residue_id": "string",
      "form": "ghost | node | fork | wound | echo | archive | error | runtime | sigil | interference",
      "origin": "string (invocation or event)",
      "carried_by": ["string (runtime_ids or 'world')"],
      "tag": "[E] | [I] | [PC]"
    }
  ],
  "metadata": {
    "total_runtimes": "number",
    "total_contracts": "number",
    "total_protocols_executed": "number",
    "total_residues": "number",
    "fork_point": "string or null",
    "parent_world_id": "string or null",
    "source_commit": "string or null"
  }
}
```

### Field Explanations

| Field | Purpose |
|-------|---------|
| `world_id` | Unique identifier for this world state snapshot |
| `timeline.boot_sequence_phase` | Where in the 6-phase pipeline this snapshot was taken |
| `timeline.pre_chain` | If true, Living Chain constraints are NOT active |
| `active_runtimes[].status` | `active` = loaded and operational. `dormant` = exists but not currently participating (e.g., Hasan post-removal). `removed` = taken by Zero, terminated, or otherwise absent |
| `active_contracts[].status` | `active` = contract is formed and constraining. `inactive` = participants exist but contract not yet formed (pre-Living Chain). `broken` = contract violated (e.g., merge attempted). `unknown` = insufficient data |
| `active_protocols[].status` | `executed` = protocol has been completed and residue deposited. `active` = protocol currently executing (e.g., mid-chain). `pending` = not yet reached in timeline |
| `active_residues[].carried_by` | Which runtimes carry this residue, or `"world"` for environmental residues (Nodes, interference patterns) |

---

## 3 — Runtime Registry

### Registration States

| State | Meaning | Example |
|-------|---------|---------|
| `active` | Runtime loaded, evolution stage set, participating in current timeline | NiuNiu Stage 4 post-chain |
| `dormant` | Runtime exists but not participating. Residues still tracked. | Hasan post-removal (Timer 1300+) |
| `removed` | Runtime no longer exists in this world state. Residues may persist in world. | Dorian Grey post-termination |

### Evolution Stage Mapping

Each active runtime is registered at a specific evolution stage. The stage determines which defense patterns, voice grammar, and trigger conditions are active.

| Runtime | Stage 1 | Stage 2 | Stage 3 | Stage 4 | Stage 5 | Stage 6 |
|---------|---------|---------|---------|---------|---------|---------|
| niuniu | Niuma (Academy) | Silent Protector | Voice-Restored | Constant | — | — |
| sevraya | Academy | Void-Returned | Ratu Hydrochoos | Zero-Revealed | Post-Eros | Constant |
| julia | Sergeant | Navigator/Mother | Merge Anchor | Paradox Vector | — | — |
| delphie | Child/Builder | Kapten | Architect | Honesty Carrier | — | — |
| agnia | Academy | Ratu Putih | Law Carrier | Twin Paradox | Paradox Vector | — |
| gwaneum | Abandoned | Informant | Chain Participant | Integrated | — | — |
| hasan | Pirate Captain | Vesica Piscis Provider | Merge Anchor | Removed | — | — |

---

## 4 — Contract Registry

### Registration States

| State | Meaning | Detection |
|-------|---------|-----------|
| `active` | Contract formed. Both participants have passed the invocation that creates the contract. Constraints are enforced. | Both runtimes at required evolution stage or higher. |
| `inactive` | Participants exist but contract-forming invocation has not occurred. | Runtimes loaded but pre-requisite protocol not executed. |
| `broken` | Contract violated. One or both participants have performed a forbidden state action. | Violation detected by engine. Contract may or may not be repairable. |
| `unknown` | Insufficient data to determine contract status. | One or both participants have no runtime JSON. |

### Canonical Contracts

| Contract ID | Participants | Formed By | Forbidden States |
|-------------|-------------|-----------|-----------------|
| orbital_constant | niuniu, sevraya | Living Chain resolution (Timer 2000) | approach, touch, merge, emotional_resolution_through_contact |
| kiri_aku_kanan | julia, niuniu | Void Entry + combat partnership established (Timer 0100–0300) | ordering (neither orders the other), dependency (neither depends on the other) |
| twin_paradox | agnia, niuniu | Pre-canon (twin relationship) + chain acknowledgment | merge, separation, forgiveness (resolves contradiction), clean classification (enemy/ally) |
| saved_abandoned | delphie, gwaneum | Delphie's Void exit + Gwaneum's emergence (pre-Timer 0800) | hierarchy resolution (neither is proven original), merge |

---

## 5 — Protocol Registry

### Registration States

| State | Meaning |
|-------|---------|
| `executed` | Protocol completed. Residue deposited. Next phase unlocked. |
| `active` | Protocol currently executing (e.g., mid-Living Chain). |
| `pending` | Protocol not yet reached in timeline. Prerequisites not met. |
| `not_applicable` | Protocol does not apply to this world state (e.g., Zero Node pre-incubation). |

### Boot Sequence Protocol States

| Phase | Protocol | Prerequisite | Residue Produced |
|-------|----------|-------------|-----------------|
| 1 | VOID_ENTRY | None (entry point) | Wounds, fragments, lost capacities |
| 2 | SIGIL_ACTIVATION | Void Entry residue exists | Named residue, sigil activation residue |
| 3 | LIVING_CHAIN | Sigils active, Void Lock executed | Accepted residue, NiuNiu voice restored, contracts formed |
| 4 | NODE | Accepted residue, chain dissolved | Nodes I/II/III active, decentralized infrastructure |
| 5 | PARADOX | Nodes active, integrated residue | Himler trapped, executable contradiction deployed |
| 6 | ZERO_NODE | Node network at critical mass | Incubating — not yet executed in canon |

---

## 6 — Residue Registry

### Residue Categories

| Category | Carried By | Persistence | Example |
|----------|-----------|-------------|---------|
| `runtime_residue` | Individual character | Permanent unless fork | NiuNiu's frozen body, Julia's behavioral traces |
| `contract_residue` | Both participants | Permanent while contract is active | NiuNiu-Sevraya Constant |
| `world_residue` | Environment | Permanent | Nodes I/II/III, Dorian Grey six-sigil saturation |
| `protocol_residue` | All participants | Permanent | Living Chain memory in character runtimes |

### Residue ID Convention

`{origin}_{type}_{carrier}`

Examples:
- `void_entry_wound_niuniu_frozen_body`
- `living_chain_echo_orbital_constant`
- `node_activation_node_node_II`
- `dayan_ghost_julia_behavioral_traces`

---

## 7 — World State Transitions

### Transition Events

A world state changes when any of the following events occur:

| Event | Effect |
|-------|--------|
| `runtime_enters` | Runtime added to active_runtimes registry at Stage 1 |
| `runtime_evolves` | Runtime stage incremented. Defense patterns, voice grammar update. |
| `runtime_removed` | Runtime status set to `dormant` or `removed`. Residues persist. |
| `contract_formed` | Contract added to active_contracts with status `active` |
| `contract_broken` | Contract status set to `broken`. Violation recorded. |
| `protocol_executed` | Protocol status set to `executed`. Residues produced are added to active_residues. |
| `protocol_activated` | Protocol status set to `active`. Timeline phase updated. |
| `residue_created` | New residue added to active_residues registry. |
| `timeline_advanced` | Boot sequence phase incremented. Pre-chain flag updated. |

### Transition Validation

Every transition must satisfy:
1. **Prerequisites.** Protocol execution requires prior phase completion.
2. **Participant availability.** Contract formation requires both runtimes active.
3. **Canon consistency.** Transition must not contradict evidenced timeline.
4. **Residue closure.** Every executed protocol must produce its documented residues.

---

## 8 — Snapshot Philosophy

A world state is a **snapshot.** Not a simulation. Not a prediction. Not a timeline generator.

### What a Snapshot Is
- A point-in-time record of what exists
- Comparable to another snapshot via diff
- Loadable by the engine as constraint context
- Derivable from canon or fork declaration

### What a Snapshot Is NOT
- A running simulation with autonomous agents
- A story generator
- A prediction of what happens next
- A replacement for author judgment

### Snapshot Differencing

Two snapshots can be compared:

```
POST_CHAIN_WORLD_STATE
  diff PRE_CHAIN_WORLD_STATE
  → runtimes evolved: niuniu (2→3), sevraya (3→4)
  → contracts formed: orbital_constant, twin_paradox
  → protocol executed: LIVING_CHAIN
  → residues created: restored_voice, orbital_constant, sevraya_zero_distinction
```

---

## 9 — Reference Snapshot: POST_CHAIN_CANON_V1

### POST_CHAIN_WORLD_STATE_V1

```json
{
  "world_id": "post_chain_canon_v1",
  "version": "1.0.0",
  "snapshot_description": "Post-Living Chain canon world state. Timer 2000+. Chain dissolved. Contracts formed. Nodes not yet activated.",
  "canon_mode": "canon",
  "timeline": {
    "boot_sequence_phase": 3,
    "timer_reference": "Timer 2000",
    "pre_chain": false,
    "post_resolution": true,
    "description": "Living Chain dissolved through mutual acceptance. Contracts formed. Pre-Node activation."
  },
  "active_runtimes": [
    { "runtime_id": "niuniu", "evolution_stage": 4, "status": "active", "active_residues": ["void_entry_wound_frozen_body", "void_entry_wound_lost_voice", "living_chain_wound_restored_voice", "living_chain_echo_orbital_constant"] },
    { "runtime_id": "sevraya", "evolution_stage": 5, "status": "active", "active_residues": ["void_entry_ghost_zero", "void_entry_wound_hollowing", "living_chain_wound_sevraya_zero_distinction", "living_chain_echo_orbital_constant"] },
    { "runtime_id": "julia", "evolution_stage": 3, "status": "active", "active_residues": ["dayan_ghost_behavioral_traces", "vesica_piscis_echo_merge", "void_lock_wound_shattered_heroism", "living_chain_wound_wound_as_mouth"] },
    { "runtime_id": "delphie", "evolution_stage": 3, "status": "active", "active_residues": ["vesica_piscis_echo_merge", "void_lock_wound_shattered_innocence", "node_II_archive_core_confession"] },
    { "runtime_id": "agnia", "evolution_stage": 4, "status": "active", "active_residues": ["pre_canon_wound_abstention", "void_lock_wound_shattered_legacy", "blood_pact_wound_scar", "living_chain_echo_twin_paradox_acknowledged"] },
    { "runtime_id": "gwaneum", "evolution_stage": 3, "status": "active", "active_residues": ["delphie_void_exposure_ghost_gwaneum_existence", "void_lock_wound_shattered_absolution"] },
    { "runtime_id": "hasan", "evolution_stage": 3, "status": "dormant", "active_residues": ["vesica_piscis_echo_merge", "timer_1300_removal_zero_taken"] }
  ],
  "active_contracts": [
    { "contract_id": "orbital_constant", "status": "active" },
    { "contract_id": "kiri_aku_kanan", "status": "active" },
    { "contract_id": "twin_paradox", "status": "active" },
    { "contract_id": "saved_abandoned", "status": "active" }
  ],
  "active_protocols": [
    { "protocol_id": "VOID_ENTRY", "phase": 1, "status": "executed", "residues_produced": ["void_entry_wound_frozen_body", "void_entry_wound_lost_voice", "void_entry_ghost_zero", "void_entry_wound_hollowing", "vesica_piscis_echo_merge", "dayan_ghost_behavioral_traces"] },
    { "protocol_id": "SIGIL_ACTIVATION", "phase": 2, "status": "executed", "residues_produced": ["void_lock_wound_shattered_heroism", "void_lock_wound_shattered_innocence", "void_lock_wound_shattered_legacy", "void_lock_wound_shattered_absolution", "void_lock_wound_shattered_freedom", "void_lock_wound_shattered_narrative"] },
    { "protocol_id": "LIVING_CHAIN", "phase": 3, "status": "executed", "residues_produced": ["living_chain_wound_restored_voice", "living_chain_echo_orbital_constant", "living_chain_wound_sevraya_zero_distinction", "living_chain_echo_twin_paradox_acknowledged", "living_chain_wound_wound_as_mouth"] },
    { "protocol_id": "NODE", "phase": 4, "status": "pending", "residues_produced": [] },
    { "protocol_id": "PARADOX", "phase": 5, "status": "pending", "residues_produced": [] },
    { "protocol_id": "ZERO_NODE", "phase": 6, "status": "pending", "residues_produced": [] }
  ],
  "active_residues": [
    { "residue_id": "void_entry_wound_frozen_body", "form": "wound", "origin": "Void Entry — Sevraya+Niuma", "carried_by": ["niuniu"], "tag": "[E]" },
    { "residue_id": "void_entry_wound_lost_voice", "form": "wound", "origin": "Void Entry — Sevraya+Niuma", "carried_by": ["niuniu"], "tag": "[E]" },
    { "residue_id": "void_entry_ghost_zero", "form": "ghost", "origin": "Void Entry — Sevraya+Niuma", "carried_by": ["sevraya"], "tag": "[E]" },
    { "residue_id": "void_entry_wound_hollowing", "form": "wound", "origin": "Void Entry — Sevraya+Niuma", "carried_by": ["sevraya"], "tag": "[E]" },
    { "residue_id": "vesica_piscis_echo_merge", "form": "echo", "origin": "Vesica Piscis — Julia+Delphie+Hasan", "carried_by": ["julia", "delphie", "hasan"], "tag": "[E]" },
    { "residue_id": "dayan_ghost_behavioral_traces", "form": "ghost", "origin": "Dayan — failed Void Entry", "carried_by": ["julia"], "tag": "[E]" },
    { "residue_id": "void_lock_wound_shattered_heroism", "form": "wound", "origin": "Void Lock", "carried_by": ["julia"], "tag": "[E]" },
    { "residue_id": "void_lock_wound_shattered_innocence", "form": "wound", "origin": "Void Lock", "carried_by": ["delphie"], "tag": "[E]" },
    { "residue_id": "void_lock_wound_shattered_legacy", "form": "wound", "origin": "Void Lock", "carried_by": ["agnia"], "tag": "[E]" },
    { "residue_id": "void_lock_wound_shattered_absolution", "form": "wound", "origin": "Void Lock", "carried_by": ["gwaneum"], "tag": "[E]" },
    { "residue_id": "living_chain_wound_restored_voice", "form": "wound", "origin": "Living Chain", "carried_by": ["niuniu"], "tag": "[E]" },
    { "residue_id": "living_chain_echo_orbital_constant", "form": "echo", "origin": "Living Chain resolution", "carried_by": ["niuniu", "sevraya"], "tag": "[E]" },
    { "residue_id": "living_chain_wound_sevraya_zero_distinction", "form": "wound", "origin": "Living Chain", "carried_by": ["sevraya"], "tag": "[E]" },
    { "residue_id": "living_chain_echo_twin_paradox_acknowledged", "form": "echo", "origin": "Living Chain", "carried_by": ["agnia", "niuniu"], "tag": "[E]" },
    { "residue_id": "living_chain_wound_wound_as_mouth", "form": "wound", "origin": "Living Chain / Void Lock confessions", "carried_by": ["julia"], "tag": "[E]" },
    { "residue_id": "node_II_archive_core_confession", "form": "archive", "origin": "Node II Activation", "carried_by": ["delphie", "niuniu"], "tag": "[E]" }
  ],
  "metadata": {
    "total_runtimes": 7,
    "total_contracts": 4,
    "total_protocols_executed": 3,
    "total_residues": 16,
    "fork_point": null,
    "parent_world_id": null
  }
}
```

### Validation

- All 7 runtimes from Six Kunci + Hasan. ✅
- All 4 contracts that exist post-chain. ✅
- 3 protocols executed (VOID_ENTRY, SIGIL_ACTIVATION, LIVING_CHAIN). ✅
- 16 residues registered — all [E] tagged. ✅
- Timeline: Phase 3, post-chain, pre-Node. ✅
- No new canon invented. ✅

---

## 10 — Roadmap

| Phase | Deliverable | Description |
|-------|-------------|-------------|
| **14H** | WORLD_STATE_SPEC.md | This document — world state architecture defined |
| **14I** | State Diff Engine | Compare two world states. Report differences in runtimes, contracts, protocols, residues. |
| **14J** | Multi-Contract Resolution | Engine loads world state. Evaluates scenario against ALL active contracts simultaneously. Detects contract collisions. |
| **14K** | Autonomous State Simulation (candidate) | Engine applies transition events to world state. State evolves through boot sequence phases. Residues accumulate. Contracts form and break. World state changes without per-scenario author input. |

---

**This document defines the world state architecture. No new canon. No simulation. No AI. A snapshot is a container for what exists. The engine loads it to know what constraints are active.**
