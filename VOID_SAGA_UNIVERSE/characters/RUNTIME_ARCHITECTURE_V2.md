# RUNTIME ARCHITECTURE V2

> **Version:** 2.0.0
> **Replaces:** RUNTIME_ARCHITECTURE.md (v1 — identity-compression framework)
> **Adopted by:** Julia.runtime.md (v1.0.0), Delphie.runtime.md (v1.0.0)
> **Target:** All Phase 12C+ runtimes (Agnia, Hasan, Gwaneum, Dorian Grey, future)
> **Last updated:** 2026-06-22

---

## Purpose

This document defines the canonical runtime structure for all future Void Saga character runtimes. It is the architectural template — not a runtime itself.

V2 extends the identity-compression framework defined in v1 (10-field Runtime Stack: Core Wound → Fork Logic) with protocol-level interfaces and residue tracking. V2 runtimes are compatible with v1's identity invariants but add structural sections for boot sequence integration.

### Relationship to v1

`RUNTIME_ARCHITECTURE.md` (v1) defines WHAT a runtime is: identity-compression, not biography. It provides the 10-field stack, Runtime Laws, and Runtime Test.

`RUNTIME_ARCHITECTURE_V2.md` (this document) defines the SECTIONS a v2 runtime must contain. V2 runtimes satisfy v1's Runtime Test (recognizable in 5 conditions) while adding protocol interoperability and residue tracking.

---

## Section Specification

### 1. Runtime Status

**Purpose:** Declare version, canon baseline, evidence scope, and known limitations of the runtime.

**Required content:**
- Version number (semantic: MAJOR.MINOR.PATCH)
- Canon baseline (Timer range, protocol documents referenced)
- Audit basis (evidence audit document)
- Cross-references to related runtimes and World DNA
- Known gaps (voice grammar [I], unresolved relationships, [PC] dependencies)

**Tag requirements:** Status section may use [E], [I], [PC] to declare the runtime's overall evidence posture.

**Example:** See Julia.runtime.md §Runtime Status, Delphie.runtime.md §Runtime Status.

---

### 2. Runtime Class

**Purpose:** Define the character's operational mode sequence in one compressed line.

**Required content:**
- Arrow-separated mode transitions (Mode1 → Mode2 → Mode3 → ModeN)
- Each mode must be evidenced in canon
- Brief narrative of what each mode represents
- Substrate persistence note: earlier modes remain available under regression triggers

**Tag requirements:** All mode claims must carry [E] unless inferred — mark [I].

**Format:**
```
`Mode1 → Mode2 → Mode3 → ModeN`
```

**Example:** Julia: `Soldier → Navigator → Mother → Cosmic Function`. Delphie: `Child → Builder → Kapten → Architect → Honesty Carrier`.

---

### 3. Primary Contradiction

**Purpose:** Define the unresolvable tension that drives the character's behavior.

**Required content:**
- The contradiction in bold (one sentence)
- Explanation of why it is unresolvable
- Source citation

**Constraints:**
- Must be structural, not emotional. "She is sad" is not a contradiction. "She survived when her team didn't — the survival is the wound" is.
- Must be evidenced in canon events or protocol documents.
- Must connect to Core Wound and Defense System.

**Tag requirements:** Contradiction claim carries [E] if directly evidenced in canon or protocol; [I] if inferred from pattern.

**Example:** Julia: "She survived when her team didn't. The survival is the wound." Delphie: "She knows what children should not know. Knowledge without feeling is incomplete. She cannot unknow."

---

### 4. Core Wound

**Purpose:** Define the originating damage that shapes all other runtime elements.

**Required content:**
- Wound name
- Wound structure (not event): what the wound makes impossible, how it shapes behavior
- Origin event (evidence only — the canon event that produced the wound)
- Secondary wounds (if any)
- Source citations

**Constraints:**
- Must be a single primary wound. Secondary wounds are supporting, not equal.
- Must connect to Primary Contradiction (the wound IS the contradiction's origin).
- Must connect to Defense System (defenses are built around the wound).
- Must be evidenced in canon.

**Tag requirements:** Wound structure is [E] if directly stated in canon or protocol; [I] if synthesized from behavioral evidence.

**Example:** Julia: Dayan sole survivor. Delphie: Childhood Paradox. NiuNiu: failed to pull Sevraya fully out of The Void.

---

### 5. Defense System

**Purpose:** Define the behavioral architecture the character built around their wound.

**Required content:**
- Primary defense (WHEN → THEN format with COST annotation)
- Secondary defenses (if any)
- Defense disabled by Living Chain (if character participated in Phase 3)
- Source citations

**Format:**
```
WHEN: [trigger condition]
→ [defense response]
// COST: [what the defense costs the character]
```

**Constraints:**
- Primary defense must be a direct response to the Core Wound.
- Cost must be structural, not cosmetic.
- If the character participated in Living Chain, document what the chain attacked.

**Tag requirements:** Defense pattern is [E] if directly observed in canon; [I] if inferred from consistent behavior.

---

### 6. Invocation Pattern

**Purpose:** Document every boot sequence phase the character participated in.

**Required content:**
- Table: Phase number, Invocation name, Role, Status tag
- Pattern note: what the participation pattern reveals
- Source citations

**Format:**
```
| Phase | Invocation | Role | Status |
|-------|-----------|------|--------|
| 1 — VOID ENTRY | [name] | [role] | [E]/[I] |
```

**Constraints:**
- Only document phases the character actually participated in.
- Mark participation status: Direct, Indirect, Failed, Unresolved.
- Note if the character bridges phases in a structurally significant way.

**Tag requirements:** Participation is [E] if confirmed in canon or protocol; indirect participation may be [E] (if observed, e.g., cross-Merge sensory) or [I] (if inferred).

---

### 7. Cost Pattern

**Purpose:** Document every permanent cost extracted from the character across invocations.

**Required content:**
- Table: Cost, Invocation, Irreversibility, Tag
- Pattern note: what the cost pattern reveals about the character's trajectory

**Constraints:**
- Every cost must be linked to a specific invocation.
- Irreversibility must be honestly assessed (Yes/Partial/Temporary).
- Costs must be structural (privacy destroyed, time lost, illusion shattered), not emotional ("she felt sad").

**Tag requirements:** Cost is [E] if documented in canon or protocol; [I] if inferred from consequence pattern.

---

### 8. Consequence Pattern

**Purpose:** Document the immediate transformation following each invocation.

**Required content:**
- Table: Consequence, Invocation, Detail, Tag
- Or per-invocation chain: Cost → Consequence → Residue

**Constraints:**
- Every Consequence must link to a Cost (what was paid) and a Residue (what remained).
- No orphan Consequences.

**Tag requirements:** [E] if observed in canon; [I] if inferred.

---

### 9. Residue Pattern

**Purpose:** Document every permanent structural remainder the character carries.

**Required content:**
- Table: Residue, Origin, Form, Tag
- Residue load profile: form distribution summary
- Cross-reference to Residue Census if applicable

**Format for form classification:**
```
ghost | node | fork | wound | echo | archive | error | runtime | sigil
```

**Constraints:**
- Every residue must have an originating invocation or event.
- Form must be classified using RESIDUE_THEORY.md categories.
- Total residue count should be stated.

**Tag requirements:** [E] if directly evidenced; [I] if inferred from pattern or marked as such in Residue Census; [PC] if from Sigil_OS.md or other Probable Canon source.

---

### 10. Protocol Interfaces

**Purpose:** Document how the character interfaces with each protocol they participated in.

**Required content:**
- Per-protocol subsection
- Interface description: what the character contributed, what they received, what changed
- Source citation

**Constraints:**
- Only document protocols the character actually participated in.
- Note if participation was direct or indirect.
- Note if the protocol document references the character (cross-reference verification).

**Tag requirements:** [E] for participation; [I] for interface characterization; [PC] for per-sigil mechanics from Sigil_OS.md.

---

### 11. Relationship Interfaces

**Purpose:** Document every structurally significant relationship.

**Required content:**
- Per-relationship subsection
- Nature: one-line definition of the relationship
- Behavioral rule: how the character behaves toward this target
- Source citation

**Constraints:**
- Only document relationships with canon evidence.
- Do not over-explain romance, friendship, or emotional certainty.
- "No personal relationship documented" is a valid entry.
- For unresolved relationships, state what is unresolved.

**Tag requirements:** [E] for evidenced relationship; [I] for inferred dynamics; [PC] if from Probable Canon source.

---

### 12. Evolution Stages

**Purpose:** Document the character's operational mode transitions across canon.

**Required content:**
- 3–6 stages
- Per stage: Operational mode, Primary residue, Protocol relevance, Status tag
- LOST/GAINED transition notes between stages

**Constraints:**
- Each stage must correspond to a distinct period in canon.
- Stages are sequential but not clean — earlier modes persist as substrate.
- Stage count should reflect canon evidence, not narrative preference.

**Tag requirements:** [E] for stage events; [I] for stage characterization.

---

### 13. Failure Mode

**Purpose:** Define how the character's architecture breaks under pressure.

**Required content:**
- Primary failure mode: what regression looks like
- Alternative failure mode (if applicable)
- Trigger conditions for failure
- Canon status: has this been observed, or is it inferred?

**Constraints:**
- Failure must be structurally grounded in Core Wound and Defense System.
- Failure is not "the character dies." It is "the character's architecture stops functioning as integrated structure."
- If failure has not been observed in canon, mark [I].

**Tag requirements:** [E] if observed; [I] if inferred.

---

### 14. Terminal State

**Purpose:** Define the character's configuration at canon end.

**Required content:**
- Bullet list of terminal state properties
- Distinction between [E] properties (observed in canon) and [I] properties (inferred from trajectory)
- Source citation

**Constraints:**
- Terminal state is not "happy ending" or "tragic ending." It is structural configuration.
- Properties must be traceable to canon events or protocol outcomes.

**Tag requirements:** [E] for observed; [I] for inferred.

---

### 15. Canon Boundaries

**Purpose:** List all open questions, unresolved claims, and interpretive dependencies.

**Required content:**
- Open Questions subsection: unresolved canon gaps
- Interpretive Claims subsection: [I] and [PC] dependencies that could break if source material changes

**Constraints:**
- Do not resolve open questions. List them.
- For each [I] or [PC] claim, state the source and what would happen if the source is de-canonized.

**Tag requirements:** Open questions carry no tag (they are the absence of evidence). Interpretive claims carry [I] or [PC].

---

### 16. Runtime Summary

**Purpose:** Provide a one-line compressed formula for the character.

**Required content:**
- Arrow-separated compressed formula
- Distinction note: what makes this character structurally unique among the Six Kunci

**Format:**
```
Name =
  descriptor(mode) → descriptor(mode) → descriptor(mode) → descriptor(mode)
```

**Compressed formula (one line):**
```
`Mode1(wound) → Mode2(defense) → Mode3(integration) → Mode4(function)`
```

**Example:** Julia: `Survivor(guilt) → Navigator(distance) → Mother(anchor) → Wound(speech) → Vector(paradox)`. Delphie: `Builder(secret) → Kapten(instinct) → Architect(framework) → Confession(Node) → Witness(paradox)`.

---

## Tag Discipline

Every claim in a V2 runtime must carry one of:

| Tag | Meaning | When to use |
|-----|---------|-------------|
| `[E]` | Evidenced | Directly stated or clearly demonstrated in canon text, protocol document, or cross-referenced runtime |
| `[I]` | Inferred | Constructed from consistent patterns across multiple canon sources; no single direct statement |
| `[PC]` | Probable Canon | From Sigil_OS.md, VOID COSMOLOGY PAPER.md, or other unreconciled source; consistent with canon but not independently confirmed |

**Rules:**
- If a claim cannot carry [E], it must carry [I] or [PC].
- If a claim cannot carry [I] or [PC], it is invention and must be removed.
- [PC] claims must state their source (e.g., "Source: Sigil_OS.md [PC]").
- The ratio of [E] to [I]+[PC] should favor [E] for a v1.0.0 runtime. A runtime with more [I] than [E] is not ready.

---

## Audit Requirements

Before a V2 runtime can be committed, it must pass:

### 1. Canon Leak Audit
- No invented lore, powers, relationships, sigils, or protocols
- All claims traceable to canon or protocol documents
- All [I] and [PC] claims identified and scoped

### 2. Chain Integrity Audit
- Every Cost → Consequence → Residue chain closed
- No orphan Consequences
- No Residue without originating invocation

### 3. Protocol Compatibility Audit
- Every protocol interface verified against the referenced protocol document
- No unsupported participation claims

### 4. Relationship Contract Audit
- Every relationship interface verified against the target character's runtime (if it exists)
- No contradictory claims between runtimes

### 5. Mary Sue Audit (structural, not subjective)
- Character has meaningful limitations
- Character pays costs
- Character has documented failure modes
- Character's power is constrained by wound

### 6. Tag Discipline Audit
- [E]/[I]/[PC] ratio favors [E]
- All [PC] claims sourced
- No untagged claims

---

## Compatibility with V1

V2 runtimes satisfy V1's Runtime Test (recognizable in 5 conditions: dipuji, ditinggalkan, dibohongi, ditawari kuasa, diminta mengakui takut) even if the test is not explicitly listed in the runtime document. The structural sections (Core Wound, Defense System, Primary Contradiction, Failure Mode) provide the material the test evaluates.

V2 runtimes are compatible with V1's Runtime Laws:
- Karakter tidak boleh menjelaskan dirinya terlalu mudah. (Sections describe architecture, not self-narration.)
- Voice bukan aksen. Voice adalah pola luka yang sudah belajar grammar. (Voice grammar is embedded in Defense System and Relationship Interfaces.)
- Anomaly lebih penting dari trait. (Primary Contradiction and Failure Mode define the anomaly.)
- Fork boleh mengubah kejadian, tapi harus membayar konsekuensi psikologisnya. (Evolution Stages define what can fork and at what cost.)

---

## Migration Path

| Runtime | Current format | Migration |
|---------|---------------|-----------|
| NiuNiu v2.1.0 | V1 (original 12-section) | Backport to V2 in Phase 12C (post-Agnia) |
| Sevraya v1.1.0 | V1 (original 12-section) | Backport to V2 in Phase 12C (post-Agnia) |
| Julia v1.0.0 | V2 (architectural) | Reference implementation |
| Delphie v1.0.0 | V2 (architectural) | Reference implementation |
| Agnia | — | Create in V2 format |
| Hasan | — | Create in V2 format |
| Gwaneum | — | Create in V2 format |
| Dorian Grey | — | Create in V2 format (may require non-standard adaptations) |

---

## Canon Status

### Evidenced [E]

- All 16 sections are derived from the structure used in Julia.runtime.md (v1.0.0) and Delphie.runtime.md (v1.0.0) — committed, audited runtimes.

### Inferred [I]

- "This template is the canonical standard for all future runtimes." The decision to standardize on V2 is architectural, not canon-derived.

### Probable Canon [PC]

- None.

---

**This document defines the runtime template. It invents no new canon. It formalizes the structure already used by Julia.runtime.md and Delphie.runtime.md.**
