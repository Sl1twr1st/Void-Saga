# STATE DIFF ENGINE SPECIFICATION

> **Phase:** 14I — Design Document
> **Status:** Specification
> **Purpose:** Compare two world state snapshots and produce machine-readable change history
> **Dependency:** Phase 14H (World State Architecture), Phase 14G (Contract-First Engine)

---

## 1 — Scope

### What a State Diff Is

A state diff is a machine-readable record of change between two world state snapshots. It answers:

> "What changed between Snapshot A and Snapshot B?"

It detects:
- Runtimes added, removed, evolved, or changed status
- Contracts formed, broken, activated, or dissolved
- Protocols executed, activated, or completed
- Residues created or transformed
- Timeline advancement

### What a State Diff Is NOT

- A simulation. It does not predict what happens next.
- A scene generator. It does not produce narrative.
- A story. It does not interpret why things changed.
- Author intent inference. It does not guess motivation.
- A replacement for canon. It records what the world state says changed — not what canon says should have changed.

### Philosophy

State is memory. Diff is history. History is not narrative — history is the trace of change. The engine records transitions. A renderer may later tell stories about them.

---

## 2 — Input Objects

### WORLD_STATE_A and WORLD_STATE_B

Both must conform to the schema defined in `apps/WORLD_STATE_SPEC.md` §2.

### Validation Rules

| Rule | Description | Failure Verdict |
|------|-------------|-----------------|
| Same schema version | Both snapshots must use the same `version` field | INCOMPATIBLE_WORLD_STATES |
| Same world lineage | `world_id` must share a common prefix or one must be `parent_world_id` of the other | INCOMPATIBLE_WORLD_STATES |
| Valid timeline ordering | `world_a.timeline.boot_sequence_phase <= world_b.timeline.boot_sequence_phase` | INVALID_TIMELINE |
| Both files parse | JSON must be valid | MISSING_STATE |

### Verdicts

| Verdict | Meaning |
|---------|---------|
| PASS | Diff computed successfully. Changes detected and documented. |
| NO_CHANGES | Snapshots are identical. No diff produced. |
| INCOMPATIBLE_WORLD_STATES | Snapshots are from different worlds or schema versions. Diff not possible. |
| MISSING_STATE | One or both state files not found or invalid JSON. |
| INVALID_TIMELINE | World B's timeline is earlier than World A's. Time does not move backward. |

---

## 3 — Diff Object Schema

```json
{
  "diff_id": "string (e.g., 'diff_pre_chain_to_post_chain_v1')",
  "world_a": "string (world_id of earlier snapshot)",
  "world_b": "string (world_id of later snapshot)",
  "timestamp": "ISO 8601",
  "verdict": "PASS | NO_CHANGES",
  "runtime_changes": [
    {
      "runtime_id": "string",
      "change_type": "evolved | status_changed | added | removed",
      "from": "string or null (previous state)",
      "to": "string (new state)",
      "detail": "string (human-readable description)"
    }
  ],
  "contract_changes": [
    {
      "contract_id": "string",
      "change_type": "formed | broken | activated | dissolved",
      "from": "string or null",
      "to": "string",
      "detail": "string"
    }
  ],
  "protocol_changes": [
    {
      "protocol_id": "string",
      "change_type": "executed | activated | completed",
      "from": "string or null",
      "to": "string",
      "detail": "string",
      "residues_produced": ["string (residue_ids)"]
    }
  ],
  "residue_changes": [
    {
      "residue_id": "string",
      "change_type": "created | transformed | archived",
      "from": "string or null",
      "to": "string",
      "form": "ghost | node | fork | wound | echo | archive | error | runtime | sigil | interference",
      "carried_by": ["string (runtime_ids or 'world')"],
      "detail": "string"
    }
  ],
  "timeline_changes": [
    {
      "field": "string (e.g., 'boot_sequence_phase', 'timer_reference', 'pre_chain')",
      "from": "string or number or boolean",
      "to": "string or number or boolean"
    }
  ],
  "summary": {
    "total_runtime_changes": "number",
    "total_contract_changes": "number",
    "total_protocol_changes": "number",
    "total_residue_changes": "number",
    "total_timeline_changes": "number",
    "net_change_description": "string (one-sentence summary)"
  }
}
```

---

## 4 — Runtime Diff Rules

### Detection Logic

```
For each runtime_id in world_a.active_runtimes ∪ world_b.active_runtimes:

  IF runtime exists in B but NOT in A:
    → change_type: "added"

  IF runtime exists in A but NOT in B:
    → change_type: "removed"

  IF runtime exists in both:
    IF evolution_stage differs:
      → change_type: "evolved"
    IF status differs:
      → change_type: "status_changed"
```

### Change Types

| Change Type | Trigger | Example |
|-------------|---------|---------|
| `evolved` | `evolution_stage` incremented | niuniu: Stage 3 → Stage 4 |
| `status_changed` | `status` field changed | hasan: active → dormant |
| `added` | Runtime present in B, absent in A | Delphie enters world |
| `removed` | Runtime present in A, absent in B | Dorian Grey terminates |

### Reference Examples

```json
{ "runtime_id": "niuniu", "change_type": "evolved", "from": "Stage 3 (Voice-Restored)", "to": "Stage 4 (Constant)", "detail": "Living Chain resolution triggered stage transition." },
{ "runtime_id": "hasan", "change_type": "status_changed", "from": "active", "to": "dormant", "detail": "Taken by Zero at Timer 1300. Removed from active participation. Residues persist." },
{ "runtime_id": "sevraya", "change_type": "evolved", "from": "Stage 4 (Zero-Revealed)", "to": "Stage 5 (Post-Eros)", "detail": "Era handoff received. Sevraya-Zero distinction stabilized." }
```

---

## 5 — Contract Diff Rules

### Detection Logic

```
For each contract_id in world_a.active_contracts ∪ world_b.active_contracts:

  IF contract exists in B but NOT in A:
    → change_type: "formed"

  IF contract exists in A but NOT in B:
    → change_type: "dissolved"

  IF contract exists in both:
    IF status differs:
      IF b.status == "broken":
        → change_type: "broken"
      IF b.status == "active" AND a.status == "inactive":
        → change_type: "activated"
```

### Change Types

| Change Type | Trigger | Example |
|-------------|---------|---------|
| `formed` | Contract newly added to registry | orbital_constant appears post-chain |
| `broken` | Contract status changed to `broken` | merge attempted, contract violated |
| `activated` | Contract status changed from `inactive` to `active` | kiri_aku_kanan activated by combat partnership |
| `dissolved` | Contract removed from registry | Contract participants separated beyond repair |

### Reference Examples

```json
{ "contract_id": "orbital_constant", "change_type": "formed", "from": null, "to": "active", "detail": "NiuNiu-Sevraya Constant formed at Living Chain resolution. 'Aku yang tinggal. Dan aku yang lewat.'" },
{ "contract_id": "twin_paradox", "change_type": "activated", "from": "inactive", "to": "active", "detail": "Twin paradox acknowledged during chain. No longer avoidance." }
```

---

## 6 — Protocol Diff Rules

### Detection Logic

```
For each protocol_id in world_a.active_protocols ∪ world_b.active_protocols:

  IF protocol exists in B but NOT in A:
    → change_type: "activated"

  IF protocol exists in both:
    IF status differs:
      IF b.status == "executed" AND a.status == "active":
        → change_type: "completed"
      IF b.status == "executed" AND a.status == "pending":
        → change_type: "executed"

  IF residues_produced differs:
    → include residues_produced in change record
```

### Change Types

| Change Type | Trigger | Example |
|-------------|---------|---------|
| `executed` | Protocol completed execution. Residue deposited. | LIVING_CHAIN executed. 5 residues produced. |
| `activated` | Protocol newly added to registry | NODE protocol activated |
| `completed` | Active protocol finished | Mid-chain → chain dissolved |

### Reference Examples

```json
{ "protocol_id": "LIVING_CHAIN", "change_type": "executed", "from": "pending", "to": "executed", "detail": "666-day chain dissolved through mutual acceptance.", "residues_produced": ["living_chain_wound_restored_voice", "living_chain_echo_orbital_constant", "living_chain_wound_sevraya_zero_distinction", "living_chain_echo_twin_paradox_acknowledged", "living_chain_wound_wound_as_mouth"] },
{ "protocol_id": "NODE", "change_type": "activated", "from": null, "to": "pending", "detail": "Node protocol now reachable. Pre-requisites satisfied.", "residues_produced": [] }
```

---

## 7 — Residue Diff Rules

### Detection Logic

```
For each residue_id in world_a.active_residues ∪ world_b.active_residues:

  IF residue exists in B but NOT in A:
    → change_type: "created"

  IF residue exists in both:
    IF form differs:
      → change_type: "transformed"
    IF carried_by differs:
      → change_type: "transformed"

  IF residue exists in A but NOT in B:
    → Residues are NEVER deleted per RESIDUE_THEORY.md.
    → IF residue absent from B's active_residues, it has been ARCHIVED.
    → change_type: "archived"
```

### Change Types

| Change Type | Trigger | Example |
|-------------|---------|---------|
| `created` | New residue appears | orbital_constant residue formed |
| `transformed` | Residue form or carrier changed | wound transforms to echo |
| `archived` | Residue removed from active registry | Era Ichthyes → ARCHIVED |

### Residue Law

**Residues are never deleted.** If a residue is absent from `active_residues` in World B but present in World A, it has been archived — not erased. The diff engine must flag this explicitly.

### Reference Examples

```json
{ "residue_id": "living_chain_echo_orbital_constant", "change_type": "created", "from": null, "to": "active", "form": "echo", "carried_by": ["niuniu", "sevraya"], "detail": "NiuNiu-Sevraya Constant — permanent orbital configuration. Maintains Void equilibrium." },
{ "residue_id": "void_entry_wound_lost_voice", "change_type": "transformed", "from": "wound (complete loss)", "to": "wound (partially healed)", "form": "wound", "carried_by": ["niuniu"], "detail": "Voice restored by Living Chain but never fully healed. Panel remains primary." },
{ "residue_id": "era_ichthyes", "change_type": "archived", "from": "active", "to": "archived", "form": "archive", "carried_by": ["world"], "detail": "Era Ichthyes closed by Eros. 741 Hz frequency persists as residue. Not deleted." }
```

---

## 8 — Timeline Diff Rules

### Detection Logic

```
Compare world_a.timeline with world_b.timeline.

For each field in timeline:
  IF value differs:
    → record change

Special handling:
  - boot_sequence_phase: integer comparison
  - pre_chain: boolean flip (true → false = chain occurred)
  - timer_reference: string comparison (informational only — does not imply causality)
```

### Change Record Format

```json
{ "field": "boot_sequence_phase", "from": 2, "to": 3 },
{ "field": "pre_chain", "from": true, "to": false },
{ "field": "timer_reference", "from": "Timer 1800", "to": "Timer 2000" }
```

### Constraints

- Timeline advancement does not imply narrative causation. It records that time moved.
- The engine does not interpret timer references. It only records that they changed.
- Post-resolution flag change is informational — it does not trigger contract or protocol changes by itself.

---

## 9 — Reference Diff: POST_CHAIN_DIFF_V1

### World A: PRE_CHAIN_WORLD_STATE_V1

```
world_id: pre_chain_v1
timeline: Phase 2, Timer 1800, pre-chain=true
runtimes: 7 (all at pre-chain stages)
contracts: 2 (kiri_aku_kanan active, twin_paradox inactive)
protocols: 2 executed (VOID_ENTRY, SIGIL_ACTIVATION)
residues: 10 (pre-chain wounds, ghosts, echoes)
```

### World B: POST_CHAIN_CANON_V1

```
world_id: post_chain_canon_v1
timeline: Phase 3, Timer 2000, pre-chain=false, post_resolution=true
runtimes: 7 (niuniu Stage 4, sevraya Stage 5, others evolved)
contracts: 4 (orbital_constant formed, twin_paradox activated)
protocols: 3 executed (+ LIVING_CHAIN)
residues: 16 (+ 6 new, 1 transformed)
```

### POST_CHAIN_DIFF_V1

```json
{
  "diff_id": "post_chain_diff_v1",
  "world_a": "pre_chain_v1",
  "world_b": "post_chain_canon_v1",
  "timestamp": "2026-06-23T00:00:00Z",
  "verdict": "PASS",
  "runtime_changes": [
    { "runtime_id": "niuniu", "change_type": "evolved", "from": "Stage 3 (Voice-Restored)", "to": "Stage 4 (Constant)", "detail": "Living Chain forced speech. Resolution with Sevraya established orbital constant." },
    { "runtime_id": "sevraya", "change_type": "evolved", "from": "Stage 4 (Zero-Revealed)", "to": "Stage 5 (Post-Eros)", "detail": "Distinguished self from Zero. Received Era handoff from Eros." },
    { "runtime_id": "julia", "change_type": "evolved", "from": "Stage 2 (Navigator/Mother)", "to": "Stage 3 (Merge Anchor)", "detail": "Stabbed Sevraya. Wound became organ of speech. Tactical distance removed." },
    { "runtime_id": "agnia", "change_type": "evolved", "from": "Stage 3 (Law Carrier)", "to": "Stage 4 (Twin Paradox Acknowledged)", "detail": "Accusation delivered. NiuNiu did not deny. Twin paradox acknowledged as structure." },
    { "runtime_id": "hasan", "change_type": "status_changed", "from": "active", "to": "dormant", "detail": "Taken by Zero at Timer 1300. Removed from active participation. Vacancy created for Gwaneum." }
  ],
  "contract_changes": [
    { "contract_id": "orbital_constant", "change_type": "formed", "from": null, "to": "active", "detail": "NiuNiu-Sevraya Constant formed." },
    { "contract_id": "twin_paradox", "change_type": "activated", "from": "inactive", "to": "active", "detail": "Twin paradox acknowledged. No longer avoidance." }
  ],
  "protocol_changes": [
    { "protocol_id": "LIVING_CHAIN", "change_type": "executed", "from": "pending", "to": "executed", "detail": "666-day chain dissolved through mutual acceptance.", "residues_produced": ["living_chain_wound_restored_voice", "living_chain_echo_orbital_constant", "living_chain_wound_sevraya_zero_distinction", "living_chain_echo_twin_paradox_acknowledged", "living_chain_wound_wound_as_mouth"] }
  ],
  "residue_changes": [
    { "residue_id": "living_chain_wound_restored_voice", "change_type": "created", "from": null, "to": "active", "form": "wound", "carried_by": ["niuniu"], "detail": "Voice forced open by chain. Functional but not healed." },
    { "residue_id": "living_chain_echo_orbital_constant", "change_type": "created", "from": null, "to": "active", "form": "echo", "carried_by": ["niuniu", "sevraya"], "detail": "Permanent orbital configuration. Akashic registered. Maintains Void equilibrium." },
    { "residue_id": "living_chain_wound_sevraya_zero_distinction", "change_type": "created", "from": null, "to": "active", "form": "wound", "carried_by": ["sevraya"], "detail": "Sevraya can speak as herself even with Zero present." },
    { "residue_id": "living_chain_echo_twin_paradox_acknowledged", "change_type": "created", "from": null, "to": "active", "form": "echo", "carried_by": ["agnia", "niuniu"], "detail": "'Kami bukan dua. Kami bukan satu.' Mutual negation as permanent structure." },
    { "residue_id": "living_chain_wound_wound_as_mouth", "change_type": "created", "from": null, "to": "active", "form": "wound", "carried_by": ["julia"], "detail": "Stab delivered to Sevraya becomes permanent organ of speech." },
    { "residue_id": "void_entry_wound_lost_voice", "change_type": "transformed", "from": "wound (complete loss)", "to": "wound (partially healed)", "form": "wound", "carried_by": ["niuniu"], "detail": "Voice restored by chain but panel remains primary. Never fully healed." }
  ],
  "timeline_changes": [
    { "field": "boot_sequence_phase", "from": 2, "to": 3 },
    { "field": "pre_chain", "from": true, "to": false },
    { "field": "post_resolution", "from": false, "to": true },
    { "field": "timer_reference", "from": "Timer 1800", "to": "Timer 2000" }
  ],
  "summary": {
    "total_runtime_changes": 5,
    "total_contract_changes": 2,
    "total_protocol_changes": 1,
    "total_residue_changes": 6,
    "total_timeline_changes": 4,
    "net_change_description": "Living Chain executed. 5 runtimes evolved. 2 contracts formed. 6 residues created, 1 transformed. Timeline advanced from Phase 2 (pre-chain) to Phase 3 (post-resolution)."
  }
}
```

### Validation

- All changes are evidenced in canon. ✅
- No new residues invented. ✅
- Residue transformation (voice_loss) respects Residue Theory — never deleted, only transformed. ✅
- Timeline advancement is recorded without interpretation. ✅
- Hasan status change (active → dormant) is documented, not dramatized. ✅

---

## 10 — Diff Philosophy

State is memory. It records what exists at a moment.

Diff is history. It records what changed between moments.

History is not narrative. It does not explain why things changed. It does not assign meaning. It does not tell a story.

The engine records transitions. A renderer may later tell stories about them.

This separation is structural:
- **World State** = snapshot (static)
- **State Diff** = transition (comparative)
- **Renderer** = narrative (generative)

The engine must never confuse these three layers.

---

## 11 — Roadmap

| Phase | Deliverable | Description |
|-------|-------------|-------------|
| 14H | World State Architecture | Container for what exists |
| **14I** | **State Diff Engine** | **This document — compare two snapshots** |
| 14J | World State Validator | Verify world state satisfies all active constraints |
| 14K | Multi-Contract Resolution | Engine resolves scenarios against all active contracts simultaneously |
| 14L | Autonomous State Evolution | Engine applies transition events. State evolves without per-scenario author input. |

---

**This document defines the state diff engine. No new canon. No simulation. No prediction. The engine compares two snapshots and records what changed.**
