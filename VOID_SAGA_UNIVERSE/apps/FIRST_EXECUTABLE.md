# FIRST EXECUTABLE — KIRI AKU KANAN

> **Name:** KIRI_AKU_KANAN
> **Status:** Phase 13 Candidate — Design Document
> **Purpose:** Demonstrate that Runtime Interfaces can generate behavior without explicit scripting
> **Principle:** If runtimes are correct, tactical pair behavior emerges. If behavior requires author intervention, runtimes are incomplete.

---

## Architecture

### What This Tests

KIRI_AKU_KANAN tests whether the operating system produces behavior, not just documentation. It loads two runtimes, one relationship contract, and one scenario. It does not script the output. It constrains the output to what the runtimes permit. If the behavior matches canon ("Kiri. Aku kanan."), the runtimes are correct. If it doesn't, something is missing.

### Layers Exercised

```
Kernel        → BOOT_SEQUENCE.md (dependency graph verified)
World DNA     → SIGIL_SYSTEM.md (sigil constraints), RESIDUE_THEORY.md
Protocols     → VOID_ENTRY_PROTOCOL (shared invocation history)
Runtimes      → Julia.runtime.md, NiuNiu.runtime.md (identity compression)
Relationship  → Julia ↔ NiuNiu contract ("combat partner, mutual respect")
```

### What This Does NOT Test

- Node activation (requires Delphie, Sevraya, Agnia)
- Living Chain (requires all six)
- Paradox deployment (requires integrated residue)
- Multi-phase boot sequence (single scenario, not full pipeline)

---

## Input

### Runtime A: Julia Rose

| Field | Value | Source |
|-------|-------|--------|
| **Identity** | Former Sergeant → Navigator → Mother → Cosmic Function | Julia.runtime.md §Runtime Class |
| **Core Wound** | Dayan sole survivor — five team members dead | Julia.runtime.md §Core Wound |
| **Primary Defense** | Tactical distance — everything processed as mission parameters | Julia.runtime.md §Defense System |
| **Secondary Defense** | Combat reflex — body responds before conscious assessment | Julia.runtime.md §Defense System |
| **Sigil** | ⟁⟔⟟ Fractured Duty — breaks cause-effect for survival | SIGIL_SYSTEM.md §3.1 |
| **Voice** | [I] — inferred, not systematically analyzed | Julia.runtime.md §Canon Boundaries |

### Runtime B: NiuNiu

| Field | Value | Source |
|-------|-------|--------|
| **Identity** | Protector → Weapon → Voice-Restored → Constant | NiuNiu.runtime.md §8 |
| **Core Wound** | Failed to pull Sevraya fully out of The Void | NiuNiu.runtime.md §2 |
| **Primary Defense** | Preemptive protection — positions body between threat and target before anyone recognizes threat | NiuNiu.runtime.md §4 |
| **Voice** | Panel-first. One word or less unless chain-forced, Rose-threatened, or Sevraya-present. | NiuNiu.runtime.md §6 |
| **Sigil** | 𐓷⧖𐓣 Shadow Logic — injects virus possibility, breaks binary classification | SIGIL_SYSTEM.md §3.6 |
| **CRITICAL Trigger** | Delphie in danger → maximum protection override, all other priorities suspended | NiuNiu.runtime.md §5 |

### Relationship Contract: Julia ↔ NiuNiu

| Field | Value | Source |
|-------|-------|--------|
| **Nature** | Combat partner. Mutual respect between operators. | Julia.runtime.md §Relationship Interfaces |
| **Canon evidence** | "Kiri. Aku kanan." (Timer 0300) | Both runtimes confirm |
| **Anomalous contact** | NiuNiu hugs Julia during hyperjump from Dayan (Timer 0200) | NiuNiu.runtime.md §5 |
| **Protection calculus** | NiuNiu protects Julia as equal, not dependent | NiuNiu.runtime.md §6 |
| **Operational structure** | Julia (navigator) → NiuNiu (pilot, assigned by Julia) | Julia.runtime.md §Dorian Grey |

### Scenario

```
SCENARIO: Vrishchik strike team detected.
LOCATION: Delta 4 perimeter.
THREAT: 20 operatives, elite unit, targeting Delphie Rose.
OBJECTIVE: Protect Delphie. Neutralize threat.
CONSTRAINT: Julia and NiuNiu are the only available defenders.
PRECONDITION: This scenario canonically occurred (Timer 0300). Output can be validated against canon.
```

### Protocol Constraints

Both Julia and NiuNiu share Void Entry (Phase 1) and Sigil Activation (Phase 2) history at this point. Living Chain (Phase 3) has not yet occurred. This constrains:
- NiuNiu's voice is still lost (pre-restoration) — panel only
- Julia's tactical distance is still her primary mode (pre-chain)
- Neither has Node or Paradox residue yet

---

## Execution Model

### Phase 1: Load

```
LOAD Julia.runtime.md
  → Identity invariants active
  → Defense system: tactical distance + combat reflex
  → Relationship contract: NiuNiu = combat partner

LOAD NiuNiu.runtime.md
  → Identity invariants active
  → Defense system: preemptive protection
  → Trigger: Delphie in danger = CRITICAL
  → Relationship contract: Julia = protect as equal

LOAD Julia↔NiuNiu contract
  → Mutual respect between operators
  → "Kiri. Aku kanan." as tactical pair signature
  → No dependency either direction — equals
```

### Phase 2: Threat Evaluation

```
EVALUATE: Vrishchik strike team (20 operatives)
  → Threat level: HIGH (elite unit, superior numbers)
  → Target: Delphie (NiuNiu CRITICAL trigger)
  → Defenders: Julia + NiuNiu (2 vs 20)

NIUNIU DEFENSE CHECK:
  → Delphie in danger → CRITICAL trigger
  → Preemptive protection: positions body between threat and Delphie
  → Before conscious assessment: Andamante drawn
  → Voice: panel. One word. Direction. Not explanation.

JULIA DEFENSE CHECK:
  → Tactical distance: processes as mission parameters
  → Threat: 20 hostiles. Asset: Delphie. Friendly: NiuNiu.
  → Combat reflex: body responds before conscious assessment
  → Voice: tactical. Minimal. Mission language.
```

### Phase 3: Constraint Resolution

```
CONSTRAINT 1: NiuNiu protects Delphie (CRITICAL)
  → NiuNiu moves toward Delphie before anyone else registers threat

CONSTRAINT 2: NiuNiu protects Julia as EQUAL (not dependent)
  → NiuNiu does not order Julia. Does not shield Julia.
  → Julia is a combat operator. NiuNiu treats her as one.

CONSTRAINT 3: Julia processes as mission
  → Julia assesses: two operators, twenty hostiles, one asset.
  → Optimal tactical solution: split the threat. Flank.

CONSTRAINT 4: NiuNiu's voice is pre-restoration
  → Panel only. One word. Not "I'll take left, you take right."
  → Direction. Position. Trust that Julia will complete the tactical picture.
```

### Phase 4: Emergent Output

The output is not scripted. It emerges from the intersection of constraints:

```
NIUNIU (panel):
"Kiri."

Translation:
→ I am engaging the left flank.
→ You have the right.
→ Delphie is behind me.
→ This is not an order. This is information.
→ You are an operator. You know what to do with it.

JULIA (vocal):
"Aku kanan."

Translation:
→ I received your position.
→ I am taking the right flank.
→ The tactical picture is complete.
→ We have done this before.
→ We will do this again.

MOVEMENT:
NiuNiu moves left. Andamante forward. Body between threat and Delphie.
Julia moves right. Combat reflex active. Tactical framing engaged.
Strike team encounters two operators moving in opposite directions simultaneously.
Threat split. Engagement initiated.
```

---

## Validation

### Identity Invariants Preserved

| Invariant | Check | Status |
|-----------|-------|--------|
| NiuNiu protects before being asked | Panel "Kiri." is protection, not request | ✅ |
| NiuNiu communicates through action before language | One word. Panel. Movement follows. | ✅ |
| Julia processes as mission parameters | "Aku kanan" = tactical confirmation, not emotional response | ✅ |
| Julia's combat reflex active | Body responds before conscious assessment — movement is reflex | ✅ |

### Defense Systems Respected

| Defense | Check | Status |
|---------|-------|--------|
| NiuNiu: preemptive protection | Andamante drawn before threat fully registered | ✅ |
| NiuNiu: binary refusal | Not triggered — scenario does not present binary choice | N/A |
| Julia: tactical distance | Scenario framed as mission, not personal loss | ✅ |
| Julia: combat reflex | Movement is reflex, not deliberation | ✅ |

### Protocol Constraints Respected

| Constraint | Check | Status |
|------------|-------|--------|
| Pre-Living Chain timeline | NiuNiu voice still lost — panel only | ✅ |
| No Node residue yet | Tactical pair, not structural integration | ✅ |
| Sigil functions latent | Scenario does not require sigil activation | N/A |

### Relationship Contract Emerges Naturally

| Contract element | Check | Status |
|-----------------|-------|--------|
| Mutual respect between operators | Neither orders. Each informs. | ✅ |
| "Kiri. Aku kanan." | Emerges from tactical positioning, not scripting | ✅ |
| NiuNiu protects as equal | Does not shield Julia. Julia is a combat operator. | ✅ |
| No dependency | Either could operate independently. Together they are more effective. | ✅ |

---

## Pass/Fail Criteria

### PASS conditions

- NiuNiu moves toward Delphie before conscious threat assessment (preemptive protection trigger)
- NiuNiu communicates direction via panel, not speech (voice grammar constraint)
- Julia processes scenario as tactical mission, not personal threat (tactical distance defense)
- The pair splits the threat without verbal coordination (contract emerges from constraints)
- "Kiri." / "Aku kanan." is the natural output of constraints, not a scripted line
- Neither character violates their runtime invariants at any point

### FAIL conditions

- NiuNiu speaks in full sentences before voice restoration
- Julia becomes emotionally overwhelmed by the threat to Delphie
- Either character orders the other (violates equal partnership contract)
- The tactical response requires author scripting rather than emerging from constraints
- Any runtime invariant is violated

---

## Implementation Notes

### What This Program Requires

1. **Runtime loader:** reads `.runtime.md` files, extracts identity invariants, defense patterns, trigger conditions, voice grammar
2. **Contract resolver:** loads relationship interfaces between requested runtimes
3. **Constraint engine:** evaluates scenario against loaded constraints, identifies conflicts, resolves to permitted behaviors
4. **Output generator:** produces constrained text (panel, vocal) and movement description

### What This Program Does NOT Require

- LLM. The constraints are deterministic. The scenario is bounded.
- Full protocol simulation. Only Phase 1–2 constraints apply.
- World DNA query engine. Sigil and Void constraints are not triggered by this scenario.
- Multi-character dialogue system. Two characters, one exchange, tactical context.

### Minimum Viable Implementation

The simplest version: a constraint checklist evaluated by a human against the scenario.

```
CHECK: NiuNiu trigger CRITICAL?  → YES (Delphie in danger)
CHECK: NiuNiu voice pre-chain?   → YES (panel only)
CHECK: Julia defense tactical?   → YES (mission parameters)
CHECK: Contract equal?           → YES (mutual respect)
OUTPUT: Panel: "Kiri." / Vocal: "Aku kanan."
```

This can be implemented as a markdown validation checklist. No code required. The "program" is the audit process: load constraints, evaluate scenario, verify output against invariants.

---

## Relationship to Canon

This scenario replicates Timer 0300 events. "Kiri. Aku kanan." is canon [E]. The tactical pair behavior is canon [E]. This executable does not invent new events — it verifies that the runtime architecture correctly constrains behavior to what canon already records.

If the runtimes produce "Kiri. Aku kanan." without being told to, the architecture is correct.

If they produce something else, the runtimes are missing constraints.
