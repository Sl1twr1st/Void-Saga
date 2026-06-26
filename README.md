# Void Saga — A Narrative Compiler

> Most fictional universes are documented. Void Saga is executable.

Void Saga compiles the rules of a fictional universe and enforces them
**before** any language model generates text. You define character runtimes,
constraints, and relationship contracts. The compiler gates every scenario.
If the narrative violates canon, the LLM never gets called.

---

## See It Work — Two Commands

### ✅ PASS

```bash
./scripts/demo-pass
```

```
✅  PASS
   Canon score:  1.0
   Final verdict: PASS
   Canon verdict: CANON_PASS

Congratulations.

You have just used a Narrative Compiler.

The compiler loaded character runtimes, evaluated constraints,
scored canon compliance, and approved this scenario for generation.
No LLM was called. The universe decided first.
```

### 🛑 BLOCKED

```bash
./scripts/demo-blocked
```

```
🛑 GENERATION BLOCKED
   Reason: Hard block: 1 critical violation(s) detected.
   Hard blocks: 1
     🚫 [forbidden_behavior] Forbidden behavior violated:
        Making Zero emotional, warm, or personally attached to anyone.
   Canon score: 0.97
```

**Canon score 0.97 — nearly perfect. Still blocked. Claude API was never
called. No tokens spent. No unsafe output generated.**

This is not prompt engineering. This is a **type system for narrative.**

---

## What Just Happened?

```
Scenario JSON
      │
      ▼
Runtime Loader          ← loads character constraints, voice grammar, sigils
      │
      ▼
Constraint Engine       ← checks forbidden behaviors, invariants, defense triggers
      │
      ▼
Contract Engine         ← checks relationship rules between characters
      │
      ▼
Canon Score             ← 0.0–1.0. How aligned is this scenario with canon?
      │
      ▼
Hard Block Gate         ← critical violations stop here. No LLM called.
      │
      ├──────────────────┐
      │                  │
      ▼                  ▼
 BLOCKED           Prompt Contract   ← builds constrained LLM prompt
                        │
                        ▼
                   Claude API
                        │
                        ▼
               JSON Validation
                        │
                        ▼
         Canon-approved Narrative
```

The PASS demo ran a scenario where NiuNiu and Sevraya stay in their
established orbital relationship — every constraint passed, canon score
1.0. The compiler approved the scenario for generation.

The BLOCKED demo tried to make Zero emotional. Zero is a Void interface —
an administrative process, not a person. Zero's runtime forbids warmth or
personal attachment. The constraint engine detected the violation, the
hard block gate fired, and the compiler refused to proceed. Claude was
never asked to generate a single token.

**The language model is not the authority. The universe is.**

Each step maps to a file you can read, modify, or extend.

---

## Quickstart

→ **[10-Minute Quickstart](QUICKSTART.md)** — prerequisites, step-by-step
walkthrough, optional Claude API integration, and what to do next.

---

## Repo Map

```
Void-Saga/
│
├── README.md                          ← you are here
├── QUICKSTART.md                      ← start here after the demos
│
├── scripts/
│   ├── demo-pass                      ← ./scripts/demo-pass
│   └── demo-blocked                   ← ./scripts/demo-blocked
│
└── VOID_SAGA_UNIVERSE/
    │
    ├── apps/
    │   ├── compiler/
    │   │   └── compiler.py            ← entry point. run this directly.
    │   │
    │   ├── engine/
    │   │   ├── engine_v2.py           ← main pipeline
    │   │   ├── lib/
    │   │   │   ├── loader.py          ← loads runtimes + scenarios
    │   │   │   ├── constraints.py     ← constraint evaluation
    │   │   │   ├── contracts.py       ← relationship contract engine
    │   │   │   └── scoring.py         ← canon score calculation
    │   │   └── scenarios_v2/          ← test scenarios (JSON)
    │   │
    │   ├── data/
    │   │   ├── runtimes/              ← character runtime files (JSON)
    │   │   └── contracts/             ← relationship contracts (JSON)
    │   │
    │   └── runtime_sdk/
    │       ├── TEMPLATE.runtime.json  ← build your own runtime
    │       ├── create_runtime.py
    │       └── validate_runtime.py
    │
    └── demo/                          ← saved execution outputs
        ├── PASS_niuniu_sevraya_orbit.md
        └── BLOCKED_zero_emotional.md
```

---

## What NOT to Read First

```
❌ TASK_*.md / PHASE_*.md     — internal development artifacts
❌ *_REPORT.md / *_AUDIT.md   — historical validation outputs
❌ SESSION_STATE.md           — ephemeral session tracker
❌ INDEX.md / STUDIO_MAP.md   — internal team navigation
```

These files exist for the authors. They are not onboarding material.
Start with the demos above, then the Quickstart.

---

## Current Status (v0.2.0 — First Light)

**Implemented**

- Runtime Schema V2.1
- Multi-runtime loading
- Constraint Engine
- Pairwise Contract Engine
- Canon Scoring
- Hard Block Gate
- Claude API integration (`--live`)
- Post-generation validation

**Active Runtimes (5)**

- **NiuNiu** — Stage 4: Constant. Shadow Logic.
- **Sevraya** — Stage 6: Post-Resolution. Tidal Memory.
- **Zero** — Stage 6: Void Interface. Administrative voice.
- **Julia** — Stage 4: Fractured Duty. Human cost carrier.
- **Delphie** — Stage 5: Childhood Paradox. First SDK-created runtime.

---

## The Problem

Large language models are excellent storytellers.
They are also excellent at breaking stories.

A single prompt can accidentally erase years of worldbuilding:

- characters forget their core wounds
- relationships collapse
- canon drifts
- lore contradicts itself
- emotional logic disappears

Traditional fictional universes solve this with documentation.
Documentation depends on humans remembering it.
LLMs don't.

**The solution:** treat a fictional universe like software. Compile the rules.
Execute them before generation.

---

## Learn More

| I want to… | Go here… |
|------------|----------|
| Run the demos step by step | [QUICKSTART.md](QUICKSTART.md) |
| **Build my own character in 30 min** | **[30-Minute Challenge](docs/30_MINUTE_CHALLENGE.md)** |
| Understand the paradigm | [Executable Fiction Manifesto](VOID_SAGA_UNIVERSE/EXECUTABLE_FICTION_MANIFESTO.md) |
| Learn to author a runtime | [Runtime Authoring Guide](VOID_SAGA_UNIVERSE/RUNTIME_AUTHORING_GUIDE.md) |
| Build a character with the SDK | [Runtime SDK README](VOID_SAGA_UNIVERSE/apps/runtime_sdk/README.md) |
| Read the runtime schema | [RUNTIME_SCHEMA_V2.1.json](VOID_SAGA_UNIVERSE/apps/schema/RUNTIME_SCHEMA_V2.1.json) |
| See engine internals | [Engine README](VOID_SAGA_UNIVERSE/apps/engine/README.md) |
| Read saved execution outputs | [demo/](VOID_SAGA_UNIVERSE/demo/) |

---

## Philosophy

Void Saga is built on an Ars Goetia–inspired consequence system.

Names have weight.
Sigils bind.
Contracts constrain.
Residues persist.

Every meaningful action leaves structural consequences inside the universe.

The goal is not to simulate reality.
The goal is to make narrative law executable.

---

## License

MIT

---

Documentation describes a universe.
Execution proves it exists.
