# SYSTEM MAP

> **Type:** Kernel — Architecture Document
> **Layer:** System Overview
> **Last updated:** 2026-06-22

---

## Purpose

VOID SAGA is a narrative operating system — a kitab that pretends to be an OS. [I] It is not a novel about the future. It is a machine that prays in front of The Void. [I]

This document maps every component of the system: what exists, where it lives, and how it connects to everything else.

---

## Kernel

| File | Function |
|------|----------|
| `kernel/BOOT_SEQUENCE.md` | Defines the 6-phase startup order from Void Entry to Zero Node. Every phase consumes the output of the previous phase. No phase can be skipped. |

Kernel defines startup order and the dependency graph. It is the smallest layer — one file, one sequence, one invariant: the pipeline is linear (no phase can be skipped). [I]

---

## World DNA

World DNA defines the laws of reality. All protocols, runtimes, forks, and apps must conform to these documents. Violating a World DNA Forbidden Move requires a fork manifest.

| File | Function |
|------|----------|
| `world-dna/WORLD_DNA.md` | Core forces (Grid, Void, Zero, Ophiuchus, Dorian Grey, Goetic System), forkable constants, world-level forbidden moves. The constitution. |
| `world-dna/VOID_ONTOLOGY.md` | What The Void IS — its nature, behavior, limits, state transitions, Six Kunci, Void's Trinity. |
| `world-dna/ZERO_ONTOLOGY.md` | What Zero IS — its origin (Sevraya's fragment), function (Void's interface), limits, permanence. |
| `world-dna/RESIDUE_THEORY.md` | Residue as fundamental law: the structural remainder that outlasts its cause. Properties, forms, protocol implications. |
| `world-dna/GOETIC_CONSEQUENCE_SYSTEM.md` | The Goetic chain (Name → Sigil → Invocation → Manifestation → Bargain → Binding → Consequence → Residue) as grammar for all invocation. |
| `world-dna/COSMOLOGY.md` | How reality functions: Grid-Void tension, five elements, Nodes, apertures, consciousness as pressure artifact, Straw Cosmology model [PC]. |
| `world-dna/SIGIL_SYSTEM.md` | What sigils are: consequence given permanent form. Six canon sigils, lifecycle, binding mechanics, residue accumulation. |
| `world-dna/ERA_LOGIC.md` | What Eras are: dominant meaning-implementation patterns. Ichthyes (ARCHIVED), Hydrochoos (ACTIVE), Ophiuchus (SHADOW). VoidOS version mapping. |
| `world-dna/NIU_SEVRAYA_CONSTANT.md` | The NiuNiu-Sevraya Constant as world law: permanent orbital configuration maintaining Void equilibrium. Distance as preservation. |
| `world-dna/PARADOX_MECHANICS.md` | Paradox as world law: the excluded middle made structural. Russell's Paradox + Zeno's Dichotomy as mechanisms. Relationship to Nodes, Zero, and the boot sequence. |

---

## Protocol Layer

Protocols are invocations given structural form. They define what is summoned, what is paid, what remains, what can fail, and what cannot be known.

### Active Protocols

| File | Function | Input | Output | Depends on |
|------|----------|-------|--------|------------|
| `protocols/FORK_PROTOCOL.md` | Fork creation as Goetic invocation. Types, canon gravity, cost, residue. | Canon timeline | Alternate release | World DNA (all) |
| `protocols/SIGIL_ACTIVATION_PROTOCOL.md` | Sigil invocation: activation conditions, per-sigil costs, Void Lock as forced activation precedent. Converts `SIGIL_SYSTEM.md` into protocol form. | Named residue (sigil) | Activated sigil + activation residue | `SIGIL_SYSTEM.md`, `VOID_ONTOLOGY.md` |
| `protocols/VOID_ENTRY_PROTOCOL.md` | Crossing the Grid-Void boundary and returning. Two methods: direct entry, Vesica Piscis. | Human identity | Residue | `VOID_ONTOLOGY.md`, `ZERO_ONTOLOGY.md`, `COSMOLOGY.md` |
| `protocols/LIVING_CHAIN_PROTOCOL.md` | 666-day binding of six sigil-bearers. Forced proximity, shared pain, forced honesty. Dissolution through mutual acceptance. | Named residue (sigils) | Accepted residue | `VOID_ENTRY_PROTOCOL.md`, `SIGIL_SYSTEM.md` |
| `protocols/NODE_PROTOCOL.md` | Accepted residue becomes structural support for reality. Node I (memory), Node II (witness), Node III (self-recording). | Accepted residue | Integrated structure | `LIVING_CHAIN_PROTOCOL.md`, `SIGIL_SYSTEM.md`, `COSMOLOGY.md` |
| `protocols/PARADOX_PROTOCOL.md` | Integrated structure deployed as executable contradiction against binary classification. Phase 5 of boot sequence. | Integrated structure (Node) | Executable contradiction | `PARADOX_MECHANICS.md`, `NODE_PROTOCOL.md`, `ZERO_ONTOLOGY.md` |

### Pending Protocols

| File | Function | Status |
|------|----------|--------|
| `protocols/ZERO_NODE_PROTOCOL.md` | Node network at critical mass achieves reality-scale self-observation. | Phase 11 pending. Entity localized (Timer 1700), incubating (Void.OS v6.6.6). |
| `protocols/ERA_TRANSITION_PROTOCOL.md` | Steward-initiated closure of one Era and activation of the next. Single observed instance (Ichthyes→Hydrochoos, Timer 2000). | Phase 11 pending. Lifecycle documented in `ERA_LOGIC.md`. |

---

## Character Runtime Layer

Runtimes are identity-compression, not biography. Each runtime is the compressed structural remainder of a character's full canon arc — wounds, defenses, triggers, voice grammar, evolution stages, canon gravity, fork logic.

A runtime answers: if this character is run as a process in a scene, chat, game, app, or fork, what patterns keep them recognizable as themselves?

| File | Character | Version | Notes |
|------|-----------|---------|-------|
| `characters/NiuNiu.runtime.md` | NiuNiu Nakamoto | v2.1.0 | 4 evolution stages (Niuma → Silent Protector → Voice-Restored → Constant). Void's Trinity member. |
| `characters/Sevraya.runtime.md` | Sevraya Rose | v1.1.0 | 6 evolution stages. Co-conscious host of Zero. Ratu Hydrochoos. Era steward. |
| `characters/Zero.runtime.md` | Zero | v1.1.0 | Void fragment sharing Sevraya's body. Void's interface. Not a person — a function. |
| `characters/RUNTIME_ARCHITECTURE.md` | — | — | Defines the 10-field Runtime Stack (Core Wound → Fork Logic) + Runtime Laws + Runtime Test. Not a Phase 11 Protocol. |
| `characters/_TEMPLATE.runtime.md` | — | — | Template for new character runtimes. |
| `characters/README.md` | — | — | Character layer overview. |

**Pending runtimes:** Julia Rose, Delphie Rose, Agnia Nakamoto, Gwaneum, Hasan Al Hul, Kira, Eros, Dorian Grey, Kapten Pippa, Himler, Ophiuchus.

---

## Fork Layer

Forks are alternate residues, not clean variants. A fork diverges from canon at a declared point and produces an alternate trajectory. Once released, it cannot be taken back. Even abandoned forks leave ghost residue.

| File | Handle | Type | Status |
|------|--------|------|--------|
| `forks/niuniu_voice_restored.fork.md` | `N_U.voice_restored` | `character_fork` | Prototype. Divergence: NiuNiu's voice restored post-Void.OS v6.6.6, with complications. |
| `forks/_TEMPLATE.fork.md` | — | — | Template for new forks. |

---

## Release Layer

Releases are packaged story outputs generated by the operating system. They are instances of canon interpreted through specific forks, runtimes, and protocols.

| Path | Contents |
|------|----------|
| `releases/README.md` | Release layer overview. |
| `releases/alternate-bab/` | Alternate Bab-track releases. Empty — seeded. |
| `releases/alternate-timer/` | Alternate Timer-track releases. Empty — seeded. |

---

## App Layer

Apps are interactive interfaces built on top of World DNA + Protocols + Runtimes. They consume canon infrastructure and produce interactive experiences.

| File | Function |
|------|----------|
| `apps/CHARACTER_CHAT_APP.md` | Interactive character chat application design. Consumes character runtimes, World DNA, and protocol constraints. |

---

## Top-Level Documents

Reports, roadmaps, and architectural validation documents at the `VOID_SAGA_UNIVERSE/` root.

| File | Function |
|------|----------|
| `README.md` | Studio overview and entry point. |
| `STUDIO_MAP.md` | Earlier system map / directory structure documentation. |
| `ROADMAP_NEXT_PHASE.md` | Development roadmap. Phase 11 planning. |
| `RUNTIME_ARCHITECTURE_v2.md` | Runtime architecture specification v2. |
| `RUNTIME_ARCHITECTURE_VALIDATION.md` | Validation report for runtime architecture. |
| `RUNTIME_WORLD_DNA_PATCH_REPORT.md` | Patch report for World DNA integration with runtimes. |
| `WORLD_DNA_MINIMUM_VALIDATION.md` | Validation report for World DNA minimum requirements. |
| `NIU_SEVRAYA_CONSTANT_VALIDATION.md` | Cross-runtime validation of the NiuNiu-Sevraya Constant. |
| `SEVRAYA_ZERO_RUNTIME_VALIDATION.md` | Validation report for Sevraya-Zero runtime separation. |
| `RUNTIME_ARCHITECTURE_v2.md` | Runtime architecture specification v2 — earlier version of `characters/RUNTIME_ARCHITECTURE.md`. |
| `PHASE_11_COMPLETE.md` | Phase 11 completion report — documents all completed protocols, World DNA, kernel documents, remaining work, and Phase 12 readiness. |

---

## Dependency Diagram

```
┌─────────────────────────────────────────────────────┐
│                      KERNEL                         │
│                  BOOT_SEQUENCE.md                   │
│         Defines startup order and dependency        │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│                    WORLD DNA                        │
│   WORLD_DNA.md  ←  VOID_ONTOLOGY.md                 │
│   ZERO_ONTOLOGY.md  ←  RESIDUE_THEORY.md            │
│   GOETIC_CONSEQUENCE_SYSTEM.md  ←  COSMOLOGY.md     │
│   SIGIL_SYSTEM.md  ←  ERA_LOGIC.md                  │
│   NIU_SEVRAYA_CONSTANT.md                           │
│         Defines laws of reality                     │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│                   PROTOCOLS                         │
│   FORK_PROTOCOL.md                                  │
│   SIGIL_ACTIVATION_PROTOCOL.md                      │
│   VOID_ENTRY_PROTOCOL.md                            │
│   LIVING_CHAIN_PROTOCOL.md                          │
│   NODE_PROTOCOL.md                                  │
│   PARADOX_PROTOCOL.md                               │
│   [ZERO_NODE_PROTOCOL.md]  (pending)                │
│   [ERA_TRANSITION_PROTOCOL.md]  (pending)           │
│         Defines invocations and their costs         │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│               CHARACTER RUNTIMES                    │
│   RUNTIME_ARCHITECTURE.md                           │
│   NiuNiu.runtime.md  ←  Sevraya.runtime.md          │
│   Zero.runtime.md                                   │
│   [Julia, Delphie, Agnia, Gwaneum, Hasan, ...]      │
│         Compressed identity from canon arc          │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│                    FORKS                            │
│   niuniu_voice_restored.fork.md                     │
│         Alternate residues, not clean variants      │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│               RELEASES / APPS                       │
│   releases/alternate-bab/                           │
│   releases/alternate-timer/                         │
│   apps/CHARACTER_CHAT_APP.md                        │
│         Packaged outputs + interactive interfaces   │
└─────────────────────────────────────────────────────┘
```

**Dependency rule:** Each layer builds on the layer above it. World DNA imports nothing from Protocols. Protocols import World DNA. Runtimes import World DNA + Protocols. Forks import Runtimes + World DNA. Releases and Apps import everything below them.

---

## Operating Principle

The system operates on one invariant, repeated at every layer:

> **No transformation is free.**

```
Every invocation has cost.
Every cost produces consequence.
Every consequence leaves residue.
Residue can become structure. [I]
```

This is the Goetic chain applied as operating system architecture. It is not a theme. It is not a motif. It is a constraint that every component must satisfy.

- **Kernel** enforces the sequence: no phase skipped, no phase reversed.
- **World DNA** defines the laws: what can be invoked, what cannot be touched, what always leaves residue.
- **Protocols** document the invocations: what is summoned, what is paid, what remains.
- **Runtimes** compress the results: identity as accumulated residue of canon events.
- **Forks** test the constraint: can the same laws produce different valid outputs?
- **Releases** package the outputs: instances of the system running.
- **Apps** make it interactive: the reader becomes participant; consent is asked.

---

## Canon Status

### Evidenced [E]

- All World DNA documents derive from canon Timer/Bab narrative, Codex volumes, and cross-referenced runtime evidence.
- Protocol documents document canon events (Void Entry, Living Chain, Node activation) with evidenced mechanics, costs, and residues.
- Runtime files compress evidenced canon behavior into identity invariants, defense patterns, and evolution stages.
- The fork template and prototype fork are declared as such — prototype, not canon.

### Inferred [I]

- "Narrative operating system" framing — the architecture interprets Void Saga as an OS; this is a structural reading of canon, not a canon statement.
- Dependency diagram layering — the kernel→World DNA→Protocols→Runtimes→Forks→Releases hierarchy is an architectural choice, not a canon requirement.
- Pending protocol positions — PARADOX, ZERO_NODE, SIGIL_ACTIVATION, and ERA_TRANSITION are inferred as protocol candidates from canon events; their protocol documents do not yet exist.
- Operating principle as system constraint — "every invocation has cost" is canon [E]; framing it as OS architecture is [I].

### Probable Canon [PC]

- None. This document references no Probable Canon sources.

---

**This document invents no new canon. It maps existing files and their relationships. The "narrative OS" framing is architectural interpretation, marked [I] throughout.**
