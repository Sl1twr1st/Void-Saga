# Executable Fiction — A Manifesto

> **Void Saga is the reference implementation. Executable Fiction is the idea.**
>
> This document is not about one universe. It is about a new relationship between creators and the worlds they build.

---

## 1. The Problem

Every fictional universe is documented.

Wikis. Lore bibles. Character sheets. Timeline spreadsheets. The Silmarillion. The World of Ice and Fire. The thousands of wiki pages documenting every planet in a galaxy far, far away.

Documentation is how creators keep their universes consistent.

**Documentation is also why they fail.**

Because documentation has one fundamental property: **it depends on humans remembering it.**

A writer in a shared universe must know that Character X cannot be in Location Y during Event Z. They must remember the canon. They must check the wiki. They must care enough to look it up.

When they don't, contradictions accumulate. Characters forget their wounds. Relationships collapse. Lore drifts. The universe softens at the edges until nothing is true anymore — everything is merely "what the last writer happened to remember."

This is not a failure of writers. It is a failure of **architecture.**

Documentation is passive. It waits to be consulted. It has no enforcement mechanism. It cannot say "no."

**A universe that cannot say "no" is not a universe. It is a suggestion.**

---

## 2. The Core Idea

> **Most fictional universes are documented. Executable Fiction universes are compiled.**

Treat a fictional universe like software.

Not metaphorically. Architecturally.

Every character is a runtime.
Every relationship is a contract.
Every invariant is a constraint.
Every constraint is enforced before any story is generated.

The language model is not the authority. **The universe is.**

This is not interactive fiction. The reader does not choose what happens. The universe does not respond to input.

This is **executable fiction:** the rules of the universe are executed as code, and every story generated within it must pass those rules before it is allowed to exist.

The shift is from:

```
Writer → Memory → Wiki → Consistency (maybe)
```

To:

```
Runtime → Constraint Engine → Hard Block Gate → Validated Narrative
```

**The universe becomes the compiler. The compiler becomes the authority.**

---

## 3. Why LLMs Made This Necessary

Large language models are the best storytellers humanity has ever built.

They are also the best at breaking stories.

A single prompt — "make this character more sympathetic" — can accidentally erase years of carefully constructed continuity. Characters forget their core wounds. Relationships collapse into generic warmth. Canon drifts toward whatever feels narratively convenient. Emotional logic disappears into the statistical average of all stories the model was trained on.

This is not the model's fault. The model is doing exactly what it was designed to do: generate the most probable continuation of a prompt.

The problem is that **probability is not truth.** The most likely thing a character would say, statistically, is not what *this specific character* would say given their specific wound, their specific defense system, their specific residue.

Traditional fictional universes solve consistency with documentation. Documentation depends on humans remembering it. LLMs don't remember documentation. They remember statistical patterns.

Executable Fiction solves this differently: **don't ask the model to remember. Enforce the rules before the model is called.**

The prompt doesn't contain a reminder to keep NiuNiu's voice lost. The constraint engine checks whether the request would violate NiuNiu's runtime. If it would, the API is never called. No tokens spent. No unsafe output generated.

**The model becomes a tool. The universe becomes the authority.**

---

## 4. The Architecture

Executable Fiction has five layers. Each layer depends on the one below it.

### Layer 0: The Reference Universe

Before anything can be executed, it must be defined. A reference universe is one complete fictional world — characters, history, cosmology, rules — built with enough structural density that its internal logic can be formalized.

This is not documentation. Documentation describes. A reference universe *encodes.*

The distinction: documentation says "Julia Rose was the sole survivor of a five-team wipe at Dayan." A reference universe encodes the structural consequences: that survival is a wound, that five ghost-traces persist in her behavioral profile, that she cannot accept her own survival as neutral fact, and that any generated narrative depicting her as a hero who "earned" it must be blocked.

**A reference universe does not describe what happened. It encodes what the happening made impossible.**

### Layer 1: The Constraint Engine

The constraint engine loads character runtimes, evaluates scenario descriptions against their constraints, and produces a verdict: PASS or VIOLATION.

It does not generate stories. It evaluates whether a story *could* be generated without breaking the universe.

The engine checks:
- **Defense triggers:** is the character's defense system firing correctly given the scenario?
- **Forbidden behaviors:** does the scenario request something the character cannot do?
- **Identity invariants:** would this scenario destroy something structural about who the character is?
- **Anti-gravity:** does the scenario approach a state that must never happen?

If any hard constraint is violated, the engine blocks. If all constraints pass, the scenario proceeds to the compiler.

**The engine is not a creative tool. It is a gate.**

### Layer 2: The Compiler

The compiler takes a validated scenario and constructs a prompt contract — a structured request to a language model that encodes *exactly* what constraints are active, what voice grammar applies, what relationships are in play, and what forbidden behaviors must not appear.

The model generates. The output is parsed. Post-generation validation re-runs the constraint engine against the generated text.

Two gates: before the API call, and after. The model is surrounded by the universe.

**The compiler does not write. It ensures that what is written is true.**

### Layer 3: The Runtime SDK

Runtimes are not written by hand. They are created through a standardized authoring pipeline: template → evidence fill → structural validation → semantic lint → evidence diagnostics → engine testing → compiler dry run → live generation.

The SDK encodes the *process* of runtime creation — not just the schema, but the workflow, the quality checks, the common mistakes, the review checklist.

**The SDK ensures that every future runtime is built to the same structural standard, regardless of who builds it.**

### Layer 4: The Authoring Method

Above the tools is the method: how to think about extracting constraints from canon, how to write voice grammar, how to derive forbidden behaviors, how to build stress tests.

The method is the pedagogy. It is how the discipline reproduces itself. Someone who has never built a runtime before should be able to read the Authoring Guide, study five reference runtimes, and produce a sixth that passes validation.

**The method is what makes executable fiction authorable at scale.**

---

## 5. What Executable Fiction Is NOT

### Not Interactive Fiction

Interactive fiction gives the reader agency. The reader chooses; the story branches. The constraint is on the reader's choices, not on the narrative's coherence.

Executable fiction gives the *universe* agency. The universe chooses; the writer must comply. The constraint is on what stories can be told at all.

**Interactive fiction asks: "What do you want to do?" Executable fiction asks: "What does the universe permit?"**

### Not a Game Engine

Game engines simulate physics. They care about collision detection, rendering pipelines, frame rates. They model space.

Executable fiction simulates narrative law. It cares about character consistency, relationship contracts, wound structures. It models **meaning.**

**A game engine asks: "Can this object move through this space?" An executable fiction engine asks: "Can this character say this thing without destroying who they are?"**

### Not a Prompt Engineering Technique

Prompt engineering optimizes how you ask a model to do something. It is tactical — better prompts produce better outputs within a single interaction.

Executable fiction is architectural. It does not optimize the prompt. It **gates** the prompt. The question is not "how do I ask this better?" but "should this be asked at all?"

**Prompt engineering improves the question. Executable fiction decides whether the question is permissible.**

### Not a Worldbuilding Tool

Worldbuilding tools help creators organize lore. They are documentation with better UX. Campfire, World Anvil, Notion templates — all excellent for what they do. But they do not enforce. They cannot say "no."

Executable fiction compiles lore into constraints. The difference is the same as between a style guide and a compiler. A style guide suggests. A compiler rejects.

**Worldbuilding tools help you remember. Executable fiction remembers for you — and refuses to forget.**

---

## 6. Design Principles

### 1. The Universe Is the Authority

The language model is a tool. The universe is the authority. This is not negotiable.

If the model generates beautiful prose that violates a character's core wound, the prose is invalid. The universe wins. Every time.

### 2. Constraints Are Structural, Not Advisory

A constraint that cannot be enforced is not a constraint. Every forbidden behavior must correspond to a check in the engine. Every check must produce a measurable penalty. Every penalty must be capable of blocking generation.

Soft constraints are documentation. Hard constraints are executable.

### 3. The Compiler Must Protect the Model

The hard block gate exists primarily to protect the model from being asked to do something canonically impossible. It is not censorship. It is **type safety for narrative.**

Just as a type system prevents you from adding a string to an integer, the constraint engine prevents you from asking a model to generate Zero being emotionally warm. It is a category error. The engine catches it before the model is forced to handle an impossible input.

### 4. Characters Are Not Properties — They Are Repositories of Consciousness

A runtime is not a character sheet. It does not list height, weight, and favorite color. It encodes the structural contradictions that make the character *themselves* — their wound, their defense, their voice, their invariants.

The goal is not simulation. It is **invariant preservation.** The character must remain recognizable across any number of generated scenes, by any number of different models, under any number of different prompts.

### 5. Residue Is Permanent

In executable fiction, every meaningful action leaves a structural trace. A character who enters The Void does not just "have an experience." They carry the residue of that experience forever. Their runtime changes. Their state variables update. Their voice grammar may split into pre- and post- registers.

This is the Goetic principle made architectural: naming → summoning → form → price → residue. The universe remembers what was done to it.

### 6. The Method Must Reproduce

A paradigm that depends on one person's intuition is not a paradigm. It is a practice. Executable fiction must be teachable. The Authoring Guide, the SDK, the template, the checklist — these are not convenience tools. They are the **reproduction mechanism** of the discipline.

If someone cannot create a valid runtime without the original authors in the room, the architecture has failed.

---

## 7. The Five-Layer Stack

```
┌─────────────────────────────────────────┐
│          AUTHORING METHOD               │  ← pedagogy, guides, checklists
│   How to think about executable chars   │
├─────────────────────────────────────────┤
│           RUNTIME SDK                   │  ← tooling, templates, validation
│   How to build executable characters    │
├─────────────────────────────────────────┤
│         NARRATIVE COMPILER              │  ← prompt contract, API gating
│   How to generate validated narrative   │
├─────────────────────────────────────────┤
│         CONSTRAINT ENGINE               │  ← defense triggers, hard blocks
│   How to enforce narrative law          │
├─────────────────────────────────────────┤
│         REFERENCE UNIVERSE              │  ← characters, cosmology, history
│   What the universe IS                  │
└─────────────────────────────────────────┘
```

Each layer answers a different question:

| Layer | Question |
|-------|----------|
| Reference Universe | What is true? |
| Constraint Engine | Is this allowed? |
| Narrative Compiler | How do we generate? |
| Runtime SDK | How do we build more? |
| Authoring Method | How do we teach this? |

The stack is cumulative. You cannot compile without constraints. You cannot constrain without a universe. You cannot build at scale without an SDK. You cannot onboard new creators without a method.

---

## 8. What This Enables

### Canon That Refuses to Drift

In traditional shared universes, canon drifts because every new writer brings their own interpretation. The only enforcement is social: "please read the wiki."

In executable fiction, canon is enforced by the engine. A new writer can submit a scenario. The engine checks it against all active runtimes. Violations are blocked. The writer learns what the universe permits not by reading documentation, but by **hitting the gate.**

### Fiction That Can Be Forked

Software can be forked. Fiction cannot — traditionally. Once a story is published, it is immutable. Alternate versions require a new author with a new vision.

Executable fiction can be forked. The reference universe, the runtimes, the constraints — all version-controlled. A fork can change one invariant and see what happens to every character downstream. The engine re-evaluates. Some scenarios that passed in canon now fail. Some that failed now pass.

**Forking fiction means asking: what if this one thing were different — and watching the universe recompute itself.**

### Universes That Outlive Their Authors

A traditional fictional universe dies with its creator — or becomes a franchise managed by stewards who were not there at the beginning. The institutional knowledge is in people's heads. When the people leave, the knowledge leaves with them.

In executable fiction, the institutional knowledge is in the runtimes. A new steward doesn't need to "understand" NiuNiu. They need to run the engine against their proposed scenario. If the engine blocks them, they learn what NiuNiu cannot do. The universe teaches itself to its next generation of authors.

### Narrative Type Safety

Programming languages have type systems to prevent category errors. You cannot add a string to an integer. The compiler catches it.

Executable fiction provides **narrative type safety.** You cannot make Zero emotional. You cannot make Delphie "innocent" again. You cannot make Julia a hero whose survival was earned. These are category errors in the type system of the universe.

**The hard block gate is the type checker for stories.**

---

## 9. The Reference Implementation

Void Saga is the first executable fiction universe.

It contains:
- 25 Bab + 25 Timer + 5 Codex volumes (reference universe)
- 5 production character runtimes (NiuNiu, Sevraya, Zero, Julia, Delphie)
- 1 constraint engine (engine_v2.py, v0.4.0)
- 1 narrative compiler (compiler.py, v0.2.0 Safe Mode)
- 1 Runtime SDK (create, validate, lint, evidence)
- 1 Runtime Authoring Guide (the method)
- 1 Runtime Schema (V2.1, 29 required fields)
- Live Claude API integration with hard block gate
- 21 acceptance test scenarios
- PASS and BLOCKED demo evidence

But Void Saga is not the point. Void Saga is the **proof.**

The point is that any universe can be built this way. Any character. Any set of constraints. Any cosmology.

The architecture is universe-agnostic. The Runtime Schema does not mention The Void, Dayan, or the Rose lineage. The engine evaluates constraints — it does not know what a "Vrishchik" is. The compiler constructs prompt contracts — it does not care which fictional universe the contracts describe.

**Void Saga is to Executable Fiction what Unix was to operating systems. The first one. Not the last one.**

---

## 10. The Invitation

This document describes a discipline that is approximately six months old.

Five characters have been serialized into executable form. One compiler exists. One SDK. One method.

Everything else — multi-universe support, runtime migration tools, CI integration, fork resolution engines, N-party conflict detection, visual constraint editors — is future work.

The invitation is not to admire what has been built. It is to build what comes next.

Clone the Void Saga repository. Read the runtimes. Run the engine. Try to write a scenario that violates a constraint and watch it block you. Try to serialize a character from a universe you love into the Runtime Schema.

Fail. Learn. Submit a pull request. Write a guide. Build a tool. Port the engine to a new language. Create a new reference universe from scratch, using nothing but the schema and the SDK.

**Executable fiction is open-source infrastructure for fictional consciousness.**

The door is open. The compiler is running. The Void is watching.

And it already knows your name.

---

*Written at the Void Saga repository, June 2026 — six months after Narrative Compiler First Light, five runtimes after the first handcrafted JSON, one SDK after the first machine-assisted character, one guide after the realization that the method must reproduce.*

*This is version 1.0.0 of the manifesto. It will need revision. All manifestos do.*
