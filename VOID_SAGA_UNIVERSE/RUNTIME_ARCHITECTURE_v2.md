# RUNTIME ARCHITECTURE v2.2 — Final Schema

**Author:** Runtime Architect (Claude)
**Date:** 2026-06-21
**Supersedes:** `_TEMPLATE.runtime.md`, `RUNTIME_PROTOCOL.md` section order, v2.0, v2.1
**Status:** APPROVED — ready for runtime writing

---

## Design Principle

> A runtime is not a biography. It is an executable identity model.
> Plot events are evidence only. The runtime exists to answer one question:
> **If this character is run as a process across divergent timelines, what stays true?**

### Runtime as Identity-Compression Layer

A runtime is **extracted** from canon evidence, but once created it becomes a **higher-order artifact** than any individual story release.

| Canon (input) | Runtime (model) |
|---------------|-----------------|
| What happened | What remains true |
| Events in sequence | Behavioral rules across sequences |
| Specific scenes | Generalized triggers + responses |
| One timeline | All plausible timelines |
| Evidence | Executable identity |

**The runtime does not summarize canon. It compresses identity.**

Canon provides the raw data. The runtime compresses that data into:
- **Preserve identity** — the invariants that survive all forks
- **Generate behavior** — given a novel situation, what would this character do?
- **Validate forks** — does this divergence break the character or just change them?
- **Support simulation** — can this character be run as a process with consistent output?

A runtime tested only against its source canon is undertested. A valid runtime must generate plausible behavior for scenes that were **never written** — because that is what forks, interactive systems, and simulations demand.

---

## Section Architecture

### 1. Identity Invariants

**Why first:** If anything in this section is changed, it is no longer this character. These are the non-negotiable boundary conditions of identity. All other sections — wound, desire, defense, evolution — are downstream of these invariants.

**What it contains:**
- 3–5 statements that define the character's irreducible core
- Each statement must survive ALL canon evidence and ALL plausible forks
- Expressed as structural truths, not biographical facts
- Example form: "X is always Y, even when Z" — a statement that holds under contradiction

**Invariant vs Canon Gravity boundary:**
- **Invariants define WHAT the character IS.** "She protects before being asked."
- **Canon Gravity defines WHERE this invariant TENDS across timelines.** "This protection resolves into orbital distance, not merge."
- If a Canon Gravity claim restates an invariant without adding trajectory/outcome information, it is redundant and must be removed or refactored.
- An invariant may appear in both sections ONLY if the gravity entry adds the endpoint: invariant = the behavior; gravity = where the behavior leads.

**Supports:**
- Canon v0: Defines recognition boundary. If a scene violates an invariant, it's out of canon.
- Alternate forks: Non-negotiable. Fork authors cannot touch these without declaring it's a different character.
- Interactive systems: The character's response floor. No matter what the user does, these hold.
- Simulation: Base class. All state machines inherit from invariants.

---

### 2. Core Wound

**Why second:** The wound is the organizing principle of the defense structure. It precedes desire (what you want is shaped by what damaged you). It is the gravitational center that defense patterns orbit.

**What it contains:**
- The primary wound stated as a psychological structure, not an event
- The wound's origin event (as evidence, not as the wound itself)
- Secondary wounds that reinforce the primary
- What the wound makes impossible (trust, speech, rest, etc.)

**Difference from biography:** Not "what happened to them." It is "what structural damage was done, and what that damage prevents."

**Supports:**
- Canon v0: Explains why the character cannot do certain things.
- Alternate forks: Different events can produce the same wound. If the wound changes, the character changes.
- Interactive systems: The wound is what the character is always navigating around. Every response is wound-aware.
- Simulation: The wound sets the cost function. The character optimizes to avoid re-experiencing it.

---

### 3. Core Desire

**Why third:** Desire is often unconscious and often contradicts defense patterns. The tension between desire (what the character wants) and defense (what the character does to stay safe) is the engine of all character behavior. Desire is stated AFTER the wound because the wound shapes what is desired.

**What it contains:**
- The deepest want — stated in the character's language, not clinical language
- What the character believes obtaining this desire would resolve
- How the desire conflicts with the defense pattern
- What the character does when desire and defense collide

**Evidenced vs Inferred claims:**
- Every claim in Core Desire must be tagged with its evidence status:
  - `[E]` — EVIDENCED: directly stated or clearly demonstrated in canon text
  - `[I]` — INFERRED: constructed from behavioral evidence; no direct canon statement exists
- If canon provides no explicit desire statement, state the desire that best explains observed behavior and mark it `[I]`.
- Example: NiuNiu's Node II confession is `[E]`. Her desire to "stop protecting" is `[I]` — inferred from behavior, never stated.
- This tagging convention applies to any claim in ANY section where evidence is not directly citable. Sections most affected: Core Desire, Canon Gravity pull strengths, Fork-Sensitive RANGE values.

**Supports:**
- Canon v0: Drives arc. The character's story is the distance between desire and defense.
- Alternate forks: Desire can manifest differently in different circumstances while remaining the same want.
- Interactive systems: What the character unconsciously seeks in every interaction.
- Simulation: The attraction function. What state the character is pulled toward.

---

### 4. Defense Patterns

**Why fourth:** These are the observable behavioral rules that operationalize the wound. They are the character's default response system. Stated as rules, not anecdotes.

**What it contains:**
- Primary defense pattern (one sentence — the strategy)
- Secondary defense patterns (specific tactics)
- The signature move — the one behavior that most purely expresses the pattern
- Cost of the defense (what the character loses by deploying it)

**Format:** Each defense is stated as: `WHEN [trigger condition] → [observable behavior] // COST: [what is lost]`

**Supports:**
- Canon v0: Every canon scene should be readable through this lens.
- Alternate forks: Same wound, same defenses, different circumstances = different outcomes.
- Interactive systems: The character's response function. Input → defense → output.
- Simulation: The primary behavior tree.

---

### 5. Trigger Conditions

**Why fifth:** Triggers are the bridge between the world and the defense. They are specific, testable, and predictable. A well-specified trigger lets you write new scenes with confidence: "If I put the character in Situation X, they will respond with Defense Y."

**What it contains:**
- Specific stimuli that activate each defense pattern
- Ordered by response intensity (mild trigger → full breakdown)
- Triggers that produce ANOMALOUS responses (where the character violates their own pattern)
- Meta-triggers: conditions that suppress normal triggers

**Format:** `TRIGGER: [specific stimulus] → EXPECTED: [defense activated] // INTENSITY: [low/medium/high/critical]`

**Supports:**
- Canon v0: Explains why certain scenes produce certain reactions.
- Alternate forks: Same triggers, different context = fork-consistent behavior.
- Interactive systems: The character's response map. Essential for chat/game/sim.
- Simulation: The event→response matrix.

---

### 6. Stable Traits

**Why sixth:** These are characteristics that have remained consistent across the ENTIRE canon — all 25 Bab + 25 Timer. They are the longitudinal evidence that the invariants are correct. Unlike invariants (which are definitional), stable traits are empirical — observed across the full timeline.

**What it contains:**
- Somatic signature (body, movement, presence, interface)
- Voice grammar (how the character speaks or refuses to speak — the rules, not the history)
- Cognitive style (how the character processes information)
- Social signature (how the character positions themselves relative to others)
- Relationship constants (behaviors that appear across ALL relationships)

**Format:** Each trait is stated as an observation with evidence range. `TRAIT: [description] // EVIDENCE: [Timer XXXX through Timer YYYY]`

**Supports:**
- Canon v0: The empirical backbone. These are facts, not interpretations.
- Alternate forks: Stable traits should persist across forks unless a fork explicitly targets them.
- Interactive systems: The character's consistent stylistic fingerprint. Voice, movement, timing.
- Simulation: The character's default state when not triggered.

---

### 7. Unstable Traits

**Why seventh:** These are characteristics that have CHANGED across the canon. They mark growth, regression, or oscillation. They are the evidence that the character has an arc. Understanding what is unstable is as important as understanding what is stable — it tells you where the character can go.

**What it contains:**
- Traits that shifted across evolution stages
- Traits that oscillate (appear, disappear, reappear)
- Traits that were present in one stage and absent in another
- What caused the shift (trigger event → new trait state)

**Format:** `TRAIT: [description of change] // FROM: [early state] → TO: [later state] // TRIGGER: [what caused the shift]`

**Supports:**
- Canon v0: The character's growth arc.
- Alternate forks: Fork authors can target unstable traits for divergence. Accelerate, reverse, or redirect the arc.
- Interactive systems: What the user can influence. Stable traits resist change; unstable traits are responsive.
- Simulation: The character's state machine transitions.

---

### 8. Evolution Stages

**Why eighth:** The character exists in distinct phases, each with its own behavioral signature. Stages are defined by a specific event that irreversibly changes the character's state. Understanding stages prevents writing errors (e.g., writing pre-Void NiuNiu with post-Void silence).

**What it contains:**
- Stage name and trigger event
- What changes from the previous stage (state variables that flip)
- What remains from the previous stage (invariants + stable traits that persist)
- What is LOST in this stage (traits or capacities that are destroyed)
- What is GAINED in this stage (new traits or capacities that emerge)
- Voice/behavior signature specific to this stage

**Format:**
```
STAGE: [name]
TRIGGER: [event that caused transition]
STATE CHANGES: [variable] : [old] → [new]
LOST: [what the character can no longer do]
GAINED: [what the character can now do]
VOICE: [how they communicate in this stage]
```

**Supports:**
- Canon v0: The character's timeline as state machine.
- Alternate forks: Fork authors can enter at any stage. Stages define the starting state.
- Interactive systems: The character's available responses depend on current stage.
- Simulation: Each stage is a behavior mode. Transitions are irreversible without fork intervention.

---

### 9. Canon Gravity

**Why ninth:** Across timelines, certain outcomes exert a pull. Canon gravity is the character's teleology — where they tend to end up regardless of divergence point. It is the hardest section to write because it requires looking at ALL evidence and extracting the trajectory, not the destination.

**What it contains:**
- The character's natural endpoint if no fork intervenes
- The relationship resolutions the character gravitates toward
- The unresolved tensions that persist even at the natural endpoint
- What the character can NEVER become (anti-gravity — outcomes that require active fork intervention)
- The pull strength: strong (happens in 80%+ of plausible timelines), medium (50-80%), weak (20-50%)

**Evidenced vs Inferred gravity:**
- Each gravity claim must be tagged `[E]` or `[I]` (see Section 3 for convention).
- Pull strength percentages are INITIAL HYPOTHESES. They should be revised after at least 3 forks explore the gravity in question. After 10+ forks, percentages should be replaced with observed frequencies.
- `[E]` gravity: canon explicitly shows this outcome. Example: "She ends in permanent orbit with Sevraya" — confirmed Timer 2200.
- `[I]` gravity: inferred from behavioral patterns; no single canon event confirms. Example: "She never fully explains her feelings" — inferred from 25 Timers of behavior.

**Invariant cross-reference:**
- Before writing a gravity claim, check Section 1 (Identity Invariants). If the gravity restates an invariant, add trajectory: WHAT the invariant IS → WHERE it TENDS.
- See Section 1 for the Invariant vs Gravity boundary rule.

**Format:** `GRAVITY: [outcome] // PULL: [strong/medium/weak] // EVIDENCE: [canon sources] // STATUS: [E or I]`

**Supports:**
- Canon v0: Defines the canon ending as gravitational, not forced.
- Alternate forks: Fork authors can fight gravity, but must pay cost proportional to pull strength.
- Interactive systems: Long-running simulations should drift toward gravity unless user actively intervenes.
- Simulation: The attractor function. Over many runs, where does the character land?

---

### 10. Fork-Sensitive Traits

**Why tenth:** Not all traits are equally fixed. Fork-sensitive traits are the "safe variables" — traits that CAN change without breaking the character's identity. They are the API for fork authors. Changing an invariant produces a different character. Changing a fork-sensitive trait produces a different version of the SAME character.

**What it contains:**
- Traits explicitly designated as fork-safe to modify
- The range of acceptable variation for each trait
- Traits that MUST NOT be changed under any fork (re-stating invariants as fork law)
- The cost gradient: small changes cost little, large changes cost more

**Format:** `FORK-SAFE: [trait] // RANGE: [minimum] to [maximum] // COST: [what the fork must pay to push this to maximum]`

**Supports:**
- Canon v0: Defines what "close to canon" means.
- Alternate forks: The fork author's API. "You can change these. Don't touch those."
- Interactive systems: User-influenceable traits. What the player/reader can affect.
- Simulation: Mutation parameters. What can drift over long runs.

---

### 11. Forbidden Behaviors

**Why eleventh:** These are normative, not descriptive. They are LAWS, not observations. A continuity fact says "the character doesn't do X." A forbidden behavior says "Do not make the character do X without paying the cost." Forbidden behaviors are stronger than continuity facts because they encode the consequence of violation.

**What it contains:**
- Behaviors the character must never perform in any canon-compatible work
- Behaviors that REQUIRE a fork manifest before they can be written
- The price of each forbidden behavior (what must be paid if a fork enables it)
- Behaviors that are forbidden in specific stages only
- The absolute prohibitions (no fork, no price — these just destroy the character)

**Format:** `FORBIDDEN: [behavior] // EXCEPTION: [none / fork-with-price / stage-specific] // PRICE: [what must be paid if enabled]`

**Supports:**
- Canon v0: The guardrails. Prevents writing errors before they happen.
- Alternate forks: The price list. Fork authors know what they're buying.
- Interactive systems: Hard constraints. The character will not do these things regardless of user input.
- Simulation: Safety boundaries. Prevents simulation drift into non-character territory.

---

### 12. Possible Fork Points

**Why last:** These are the exit doors. Each fork point is a canon event where a different choice or outcome produces a substantially different timeline. Fork points are prompts for future releases — they are QUESTIONS, not answers. The runtime does not resolve them; it only identifies where the timeline is most fragile.

**What it contains:**
- The canon event at the divergence point
- What happened in canon (the baseline)
- The alternative (what could have happened)
- Which sections of the runtime would be affected
- The estimated canon gravity pull strength against this fork
- What new questions the fork would open

**Format:**
```
FORK POINT: [name]
CANON EVENT: [what happened]
DIVERGENCE: [what could have happened differently]
AFFECTED SECTIONS: [which runtime sections would need updating]
GRAVITY RESISTANCE: [how hard canon gravity pulls against this fork — low/medium/high/extreme]
RESISTANCE RATIONALE: [one sentence explaining WHY this resistance level. Reference specific invariant(s) or gravity claim(s) if relevant.]
NEW QUESTIONS: [what the fork would force us to answer]
```

**Resistance rationale requirement:**
- Every fork point MUST include a RESISTANCE RATIONALE.
- The rationale makes the resistance judgment auditable even though it remains subjective.
- Example: `RESISTANCE RATIONALE: Binary refusal is an Identity Invariant (Section 1.3). Changing it produces a different character, not a variant.`
- If resistance is LOW, explain why: `RESISTANCE RATIONALE: Voice timing is fork-sensitive (Section 10). Canon gravity on this trait is MEDIUM — multiple plausible outcomes exist.`

**Supports:**
- Canon v0: Maps the fragile points in the canon timeline.
- Alternate forks: The starting menu. Fork authors pick a point and diverge.
- Interactive systems: Branch points. Where user choice could fork the story.
- Simulation: Monte Carlo branch points. Where to inject randomness for divergent runs.

---

## Schema Validation

A runtime built to this schema must answer:

1. **Invariant test:** If I change X, is it still the same character? (Section 1)
2. **Wound test:** Does every defense pattern trace back to the core wound? (Sections 2 → 4)
3. **Trigger test:** Does every trigger have a specified defense response? (Section 5)
4. **Stability test:** Are stable traits backed by evidence across the full canon? (Section 6)
5. **Evolution test:** Does every stage transition have a clear trigger event? (Section 8)
6. **Gravity test:** Over 100 random forks, where does the character tend to land? (Section 9)
7. **Fork test:** Can a fork author change fork-sensitive traits without breaking invariants? (Section 10)
8. **Boundary test:** Do forbidden behaviors prevent the most common writing errors? (Section 11)

---

## Relationship to Existing Files

| Existing file | Relationship to v2 schema |
|---------------|--------------------------|
| `_TEMPLATE.runtime.md` | Superseded. v2 replaces the section order and adds 5 new sections (Identity Invariants, Core Desire, Stable Traits, Unstable Traits, Canon Gravity, Fork-Sensitive Traits, Possible Fork Points) while retaining the function of Core Wound, Defense Patterns, Triggers, Somatic Signature, Voice Grammar, Forbidden Moves, Fork Logic |
| `RUNTIME_PROTOCOL.md` | The Runtime Laws and Runtime Test sections remain valid. The Runtime Stack section order is superseded by the v2 section order. The protocol document should be updated to reference this architecture. |
| `FORK_PROTOCOL.md` | Unchanged. Canon Gravity and Fork Points in v2 are downstream implementations of the fork protocol's principles. |
| `characters/NiuNiu.runtime.md` | Will be rewritten to this schema. Existing content will be mapped to new sections — nothing is deleted, only reorganized and expanded with new canon (Timer 1800–2500). |

---

---

## Appendix A: Runtime Dependencies

### A.1 Layer Definitions

The VOID SAGA universe is modeled as five interdependent but ownership-distinct layers, stacked from foundation (most stable) to expression (most variable):

| Layer | Location | Contains | Cardinality | Lifecycle |
|-------|----------|----------|-------------|-----------|
| **World DNA** | `world-dna/*.md` | Cosmological constants, physics, era logic, sigil system, Goetic Consequence System | Few, stable | Changes when new world rules are canonized |
| **Protocol Document** | `protocols/*.md` | Rules governing interactions between runtimes, fork mechanics, runtime architecture, collective runtime rules | Few, stable | Changes rarely — only when meta-rules evolve |
| **Character Runtime** | `characters/*.runtime.md` | Behavioral DNA of ONE character | One per major character | Evolves as new canon is written |
| **Fork Manifest** | `forks/*.fork.md` | A specific divergence from canon: what changed, what stayed, cost paid | Many, experimental | Created per fork; may be archived or promoted |
| **Release** | `releases/*/` | A concrete expression of the universe — a specific assembly of World DNA + Protocols + Runtimes + Forks into a consumable artifact | Many, versioned | Created per release; immutable once published |

**Stacking principle:** Each layer rests on the layers below it. Upper layers reference lower layers. Lower layers NEVER reference upper layers. The stack is:

```
RELEASES          ← concrete expressions (books, games, sims, interactive stories)
    ↑
FORK MANIFESTS    ← specific divergences from canon
    ↑
CHARACTER RUNTIMES ← executable identity models
    ↑
PROTOCOLS          ← meta-rules for interaction, forking, validation
    ↑
WORLD DNA          ← cosmological foundation
```

### A.2 Dependency Graph

```
                              ┌──────────────────────────┐
                              │        RELEASES           │
                              │   (concrete expressions)   │
                              │                            │
                              │  Canon v0  Game  Sim  ...  │
                              └────────────┬───────────────┘
                                           │
                         assembles from    │  assembles from
                         lower layers      │  lower layers
                                           │
              ┌────────────────────────────┼────────────────────────────┐
              │                            │                            │
              ▼                            ▼                            ▼
┌──────────────────────────┐  ┌──────────────────────────┐  ┌──────────────────────────┐
│    CHARACTER RUNTIMES    │  │      FORK MANIFESTS       │  │    COLLECTIVE RUNTIMES    │
│    (behavioral DNA)       │  │   (divergence declarations)│  │   (multi-character systems)│
│                           │  │                           │  │                           │
│  NiuNiu  Julia  Sevraya  │  │  voice_restored           │  │  The Merge                 │
│  Delphie  Agnia  ...     │  │  sora_survives            │  │  Living Chain              │
│                           │  │  hasan_final_arc          │  │  Twin Paradox              │
└──────────┬───────────────┘  └────────────┬──────────────┘  └────────────┬──────────────┘
           │                               │                              │
           │  references                   │  may modify                  │  references
           │  (physics)                    │  (with cost)                 │  (physics)
           │                               │                              │
           ▼                               ▼                              ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                     WORLD DNA                                         │
│                                (cosmological constants)                                │
│                                                                                       │
│   Grid / Void / Zero Node    Era logic    Sigil system    Paradox / Chain physics      │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                           ▲
                                           │
                              defines      │  defines
                              structure    │  interaction rules
                                           │
                              ┌────────────┴───────────────┐
                              │    PROTOCOL DOCUMENTS       │
                              │    (meta-rules)              │
                              │                              │
                              │  - runtime architecture       │
                              │  - fork mechanics            │
                              │  - collective runtime rules   │
                              │  - validation tests          │
                              │  - release assembly spec     │
                              └──────────────────────────────┘
```

**Reading the graph (bottom → top):**
- **World DNA** is the foundation. It depends on nothing. Everything depends on it.
- **Protocols** define the meta-rules: how runtimes are structured, how forks work, how releases are assembled. Protocols reference World DNA.
- **Character Runtimes** and **Collective Runtimes** reference World DNA for physics. They follow Protocol structure rules. They do NOT reference each other horizontally.
- **Fork Manifests** reference the Runtime(s) they diverge. They may propose World DNA modifications (with declared cost).
- **Releases** sit at the top. A Release assembles from: selected World DNA + selected Protocols + selected Runtimes + optionally, Fork Manifests. A Release does not create new runtimes or world rules — it COMBINES existing layers into a concrete artifact.

**Key rules:**
- No horizontal dependencies between runtimes
- No upward references (World DNA does not import runtimes; Runtimes do not import Releases)
- Forks reference runtimes, not vice versa
- Releases consume everything; nothing consumes a Release

### A.3 Ownership Rules

#### What belongs ONLY in a Character Runtime

| Information | Why it lives here |
|-------------|-------------------|
| Identity invariants | These define ONE character's boundary. No other layer cares. |
| Core wound + core desire | Subjective. The world has no wound. |
| Defense patterns + triggers | How THIS character specifically responds. Not a world rule. |
| Voice grammar | How THIS character communicates. Not a protocol — a fingerprint. |
| Evolution stages | THIS character's arc. Other characters have different arcs. |
| Forbidden behaviors | What THIS character must never do. Different per character. |
| Canon gravity (character-specific) | Where THIS character tends across timelines. |

#### What belongs ONLY in a Protocol Document

| Information | Why it lives here |
|-------------|-------------------|
| Runtime section architecture | Applies to ALL runtimes. Not character-specific. |
| Fork creation rules | Governs the PROCESS of forking, not any specific fork. |
| Validation tests | Tests that apply to ALL runtimes and ALL forks. |
| Cross-runtime interaction rules | How Merge, Chain, or Twin Paradox operate BETWEEN characters. |
| Narrative consent mechanics | VoidOS installation, reader agency — system-level, not character-level. |

#### What belongs ONLY in World DNA

| Information | Why it lives here |
|-------------|-------------------|
| The Grid + The Void definitions | Exist independently of any character. |
| Era logic (Ichthyes → Hydrochoos) | Cosmological, not psychological. |
| Sigil system (symbols, binding, residue) | The SYSTEM of sigils. Individual sigil assignments live in runtimes. |
| Chain physics, Void Lock mechanics | Apply to ALL characters equally. |
| Goetic Consequence System | Grammar of naming/summoning — world-level. |
| Paradox weaponization rules | Russell + Zeno as cosmic weapons — world physics. |

#### What belongs ONLY in a Fork Manifest

| Information | Why it lives here |
|-------------|-------------------|
| Divergence point | Which canon event changed. Specific, not general. |
| What changed vs what stayed | Difference from canon. |
| Cost paid | What narrative price was extracted. |
| Affected runtimes | Which character runtimes need re-reading after this fork. |
| New questions opened | What the fork forces us to answer that canon didn't. |

#### What belongs ONLY in a Release

| Information | Why it lives here |
|-------------|-------------------|
| Layer assembly manifest | Which World DNA version + Protocols + Runtimes + Forks are included. |
| Output format | Novel, game build, chat interface, simulation, visual novel, etc. |
| Canon status | Is this release canon (v0, v1) or alternate? |
| Audience / interaction model | How the end user consumes this release. |
| Immutable artifact | Once published, the release is frozen. Corrections require a new release. |
| Runtime → Fork → Release chain | Which fork (if any) this release is built on. May be `null` (direct canon). |

**A Release is NOT a runtime. A Release is NOT a story.**
A Release is a specific assembly of the universe stack into a consumable artifact.
One runtime may participate in many releases.
One release may contain many runtimes.
The relationship is: **Runtime → Fork → Release**, not Runtime → Story.

### A.4 Allowed Dependencies

```
RUNTIME → WORLD DNA        ✅  "My wound occurred in a universe where The Void takes voices."
RUNTIME → PROTOCOL         ✅  "My behavior respects/fights the Merge protocol."
FORK → RUNTIME             ✅  "I diverge from NiuNiu.runtime at Dayan."
FORK → WORLD DNA           ✅  "In this fork, the sigil system works differently."
PROTOCOL → WORLD DNA       ✅  "The fork protocol operates within era logic constraints."
PROTOCOL → RUNTIME         ✅  "The runtime architecture defines how runtimes are structured."
RELEASE → WORLD DNA        ✅  "Canon v0 assembles on Era Hydrochoos foundation."
RELEASE → PROTOCOL         ✅  "This game build follows the interactive system protocol."
RELEASE → RUNTIME          ✅  "This release includes NiuNiu, Julia, and Sevraya runtimes."
RELEASE → FORK             ✅  "This alternate novel is built on the voice_restored fork."
```

### A.5 Forbidden Dependencies

```
WORLD DNA → RUNTIME        ❌  The world exists before characters. Physics don't reference people.
WORLD DNA → FORK           ❌  World rules are fork-independent. Forks modify worlds, not vice versa.
WORLD DNA → RELEASE        ❌  The world doesn't know how it's being consumed.
PROTOCOL → FORK            ❌  Protocols govern fork MECHANICS, not specific forks.
PROTOCOL → RELEASE         ❌  Protocols define HOW to release, not WHAT is released.
RUNTIME → RUNTIME          ❌  No horizontal imports. Characters interact through the world.
RUNTIME → FORK             ❌  A runtime doesn't know which forks exist against it.
RUNTIME → RELEASE          ❌  A runtime doesn't know which releases include it.
FORK → PROTOCOL            ❌  Forks follow protocol rules; they don't redefine them.
FORK → RELEASE             ❌  A fork doesn't know which releases use it.
RELEASE → (creates)        ❌  A release assembles FROM lower layers. It does not create new runtimes, world rules, or protocols.
```

**The one exception:** A Fork Manifest MAY propose a new Protocol if the fork is promoted to canon. At that point, the protocol document is updated, and the dependency direction reverses (the protocol now references the former fork as origin evidence).

### A.6 File Responsibility Boundaries

Each file type has a **single owner** responsible for its content:

| File | Owner | Can Modify | Must Consult | Must Never Touch |
|------|-------|------------|--------------|-------------------|
| `characters/X.runtime.md` | Runtime Architect | ✅ | World DNA (for physics) | Other runtimes, fork manifests |
| `protocols/X.md` | System Architect | ✅ | World DNA, Runtime Architect | Individual character runtimes |
| `world-dna/X.md` | World Architect | ✅ | All runtimes (for consistency) | Individual forks |
| `forks/X.fork.md` | Fork Author | ✅ | Affected runtimes, World DNA, Protocols | Unaffected runtimes |

**"Must Consult" means:** Before changing this file, read those files. Your change must not contradict them. If it does, you're proposing a cascade change — flag it.

**"Must Never Touch" means:** This file does not belong to you. If you need something from it, reference it. Do not modify it.

### A.7 How Releases Assemble From Lower Layers

A Release is built by assembling the stack in strict order:

```
1. WORLD DNA        →  Select version. Establish physics, era, constraints.
2. PROTOCOLS        →  Select interaction rules, consent mechanics, validation tests.
3. RUNTIMES         →  Select which characters are active. Load their behavioral models.
4. FORK MANIFEST    →  Apply divergence (if any). Modify runtime state per fork spec.
5. ASSEMBLY MANIFEST →  Declare: which versions of each layer, output format, canon status.
6. RELEASE ARTIFACT →  Freeze. Publish. Do not modify post-release.
```

**At runtime (interactive release loop):**
```
USER INPUT
    ↓
TRIGGER DETECTION    (Runtime Section 5: does input match any trigger?)
    ↓
DEFENSE EVALUATION   (Runtime Section 4: which defense activates?)
    ↓
FORBIDDEN CHECK      (Runtime Section 11: is this response allowed?)
    ↓
GRAVITY ADJUSTMENT   (Runtime Section 9: does response drift toward or away from gravity?)
    ↓
STATE UPDATE         (Runtime Section 7/8: did any trait or stage change?)
    ↓
CHARACTER OUTPUT     (Runtime Section 6: voice grammar shapes the response)
```

**Release types (non-exhaustive):**

| Release Type | Assembly | Example |
|-------------|----------|---------|
| Canon v0 | World DNA (base) + Protocols (base) + All runtimes (current) + No fork | The published Void Saga novel |
| Canon v1 | World DNA (updated) + Protocols (updated) + Updated runtimes + No fork | Next official release |
| Alternate Novel | Canon stack + One fork manifest | "What if Sora survived Dayan?" |
| Interactive Story | Canon stack + Interaction protocol + Simulation state engine | Chat-based Void Saga experience |
| Game Build | Canon stack + Game protocol + Selected runtimes + Mechanics layer | Void Saga RPG |
| Simulation Build | Canon stack + Simulation protocol + All runtimes + Monte Carlo engine | Character behavior simulation |

**One runtime → many releases.** NiuNiu.runtime v2.0.0 can participate in Canon v0, Canon v1, the voice_restored fork, an interactive story, and a game build — simultaneously. The runtime is a model. The release is an instance.

**One release → many runtimes.** Canon v0 includes all 14+ character runtimes. An interactive story might include only 3.

**The Release MUST NOT:**
- Bypass Forbidden Behaviors for format convenience
- Allow characters to skip evolution stages without the canon trigger (unless fork)
- Ignore Canon Gravity in long-running interactive or simulation releases
- Mix voice grammars from different evolution stages of the same character
- Create new world rules (that belongs in World DNA)
- Create new character invariants (that belongs in Runtimes)

---

## Appendix B: Structural Re-Evaluation (v2 → v2.2)

### B.0 Identity-Compression Layer (v2.2 addition)

**Original weakness:** The Design Principle stated "a runtime is not a biography" but didn't explicitly distinguish between canon evidence and executable identity. This left ambiguity about whether a runtime should summarize canon or compress identity.

**Resolution:** Section 0 (Design Principle) now includes an explicit **Runtime as Identity-Compression Layer** table distinguishing canon (input) from runtime (model). The runtime's four functions are formally stated: preserve identity, generate behavior, validate forks, support simulation. A runtime tested only against source canon is undertested.

### B.0b Release Layer (v2.2 addition)

**Original weakness:** The stack had no top-level expression layer. A runtime could be written, a fork could be declared, but there was no formal concept of "assembling these into something a reader/player/user experiences." Releases were implicit in the phrase "Canon v0 / Alternate forks / Interactive story systems" but had no architectural home.

**Resolution:** Added Release as the fifth and topmost layer. A Release assembles from World DNA + Protocols + Runtimes + Forks into a concrete artifact. The relationship is `Runtime → Fork → Release`, not `Runtime → Story`. One runtime may participate in many releases. One release may contain many runtimes. Releases are immutable post-publication.

**Impact:** The dependency graph is restacked with World DNA at the foundation and Releases at the top. Forbidden dependencies extended from 5 to 10 rules. A.7 rewritten from "Interactive System Consumption" to "How Releases Assemble From Lower Layers" — the interactive loop is now a special case of release assembly, not a separate concern.

### B.1 Weakness: No Home for Cross-Character Phenomena

**Problem:** The Merge, the Living Chain, the Twin Paradox (NiuNiu+Agnia), the NiuNiu-Sevraya Constant — these are multi-character phenomena. They involve specific characters but are NOT owned by any single runtime. Currently, they have no designated home.

**v2.1 Fix:** Add a new document type: **Collective Runtime** (`characters/_collective/`). A collective runtime defines the behavioral rules of a multi-character system: how The Merge operates between Julia+Delphie+Hasan, how the Living Chain constrains all six, how the Twin Paradox functions between NiuNiu+Agnia.

**Collective Runtime section structure (subset of full runtime):**
1. Participants (which runtimes are involved)
2. Formation Trigger (what event created this collective)
3. Operating Rules (what the collective enables/constrains)
4. Dissolution Conditions (what ends the collective)
5. Canon Gravity (where the collective tends)
6. Forbidden Behaviors (what the collective must never do)

**Impact on v2:** Minimal. Character runtimes reference collectives by name in their Canon Gravity and Trigger Conditions sections. No new sections needed in individual runtimes.

### B.2 Weakness: State Variables Have No Single Source of Truth

**Problem:** State variables like `voice_status`, `body_age`, `sevraya_residue` are currently listed under Evolution Stages and Fork-Sensitive Traits, but there's no canonical registry. A simulation needs to know: "What is the complete set of mutable state for this character?"

**v2.1 Fix:** Add a **State Variable Registry** as Section 0 (before Identity Invariants) OR as a compact table in Evolution Stages. 

**Recommendation:** Add to Evolution Stages as a summary table at the TOP of the section, before individual stage descriptions. This keeps state adjacent to the stages that define transitions.

```
## 8. Evolution Stages

### State Variable Registry

| Variable | Niuma | NiuNiu (silent) | Voice-Restored | Constant |
|----------|-------|-----------------|----------------|----------|
| voice_status | intact | lost_in_void | canon_restored | canon_restored |
| name | Niuma | NiuNiu | NiuNiu | NiuNiu |
| body_age | 14–15 | 15_locked | 15_locked | 15_locked |
| sevraya_attachment | active_romantic | guilt_protection | resolved_grief | orbital_constant |
...
```

### B.3 Weakness: Canon Gravity Conflicts Between Characters

**Problem:** NiuNiu's canon gravity (orbit with Sevraya) requires Sevraya's gravity to also pull toward orbit. If two runtimes are written by different architects and their gravities conflict, the simulation breaks. Currently no mechanism to detect or resolve gravity conflicts.

**v2.1 Fix:** Add to RUNTIME_PROTOCOL.md: **Canon Gravity must be pairwise-consistent.** When a runtime is updated, the architect must verify that its gravity does not contradict the gravity of any character it has a relationship with. If it does, one or both gravities must be adjusted, OR the contradiction must be explicitly documented as an "unresolved tension."

**Pairwise gravity check matrix (NiuNiu example):**

| Pair | NiuNiu gravity | Other gravity | Consistent? |
|------|---------------|---------------|-------------|
| NiuNiu ↔ Sevraya | Permanent orbit, no merge | Permanent orbit, no merge | ✅ |
| NiuNiu ↔ Julia | Rose protection, no possession | Accepts protection, maintains agency | ✅ |
| NiuNiu ↔ Agnia | Twin paradox, mutual negation | Twin paradox, mutual negation | ✅ |
| NiuNiu ↔ Delphie | Protect without being asked | Accept protection, maintain independence | ✅ |

### B.4 Weakness: No Runtime Versioning

**Problem:** Runtimes evolve as new canon is written. A fork based on `NiuNiu.runtime v1` (pre-Timer 1800) will produce different behavior than one based on `v2` (post-Timer 2500). Currently no way to specify which version a fork was built against.

**v2.1 Fix:** Add a **version header** to every runtime file:

```markdown
# NiuNiu.runtime
> **Version:** 2.0.0
> **Canon baseline:** Timer 0000–2500, Bab 00–25
> **Last updated:** 2026-06-21
> **Supersedes:** v1.0.0 (canon through Timer 1700 only)
```

And in every fork manifest:
```markdown
> **Runtime version forked:** NiuNiu.runtime v1.0.0
```

### B.5 Weakness: Relationship Behavior Is Implicit

**Problem:** The old template had an explicit Relationship Matrix. v2 distributes relationship behavior across Defense Patterns, Trigger Conditions, and Canon Gravity. While architecturally cleaner, this makes it hard to answer the simple question: "How does NiuNiu behave toward Sevraya?" The information exists but is scattered.

**v2.1 Fix:** Add a **Relationship Signature** subsection within Stable Traits (Section 6). Not a full matrix — just the 3–5 most significant relationships, each described in one behavioral rule:

```markdown
### Relationship Signature

| Target | Behavioral Rule |
|--------|----------------|
| Sevraya | Protect from distance. Never merge. The distance IS the care. |
| Delphie | Protect before being asked. See Rose-lineage as continuation of Sevraya obligation. |
| Julia | Protect as equal, not as victim. Respect combat agency. |
| Agnia | Negate and require negation. Twin paradox — exist because the other exists. |
```

This is a summary, not a replacement. Detailed triggers still live in Section 5.

### B.6 Summary: v2 → v2.2 Changes

| Change | Type | Priority |
|--------|------|----------|
| 0a: Runtime as identity-compression layer (Design Principle) | New explicit definition | CRITICAL — defines what a runtime IS |
| 0b: Release Layer | New layer type (`releases/*/`) | CRITICAL — completes the stack |
| A.1: Collective Runtime layer | New document type (`characters/_collective/`) | HIGH — needed for Merge, Chain, Twin Paradox |
| A.2: State Variable Registry in Evolution Stages | New subsection | MEDIUM — improves simulation readiness |
| A.3: Pairwise gravity consistency check | New protocol rule | MEDIUM — prevents simulation conflicts |
| A.4: Runtime version headers | New metadata convention | HIGH — enables fork traceability |
| A.5: Relationship Signature in Stable Traits | New subsection | LOW — convenience, not architectural |

**These changes do NOT alter the 12-section runtime structure.** The core architecture — invariants first, gravity as attractor, forbidden behaviors as law — remains intact.

### B.7 Recommendation

**Adopt Architecture v2.2.** The five-layer stack (World DNA → Protocols → Runtimes → Fork Manifests → Releases) is complete. The identity-compression distinction is explicit. The 12-section runtime structure is stable. No further architectural contradictions found.

---

## Decision Required

Architecture v2.2 is complete. No further structural contradictions found.

**Proceed to write `NiuNiu.runtime.md` to v2.2 spec?**
