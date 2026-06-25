# Runtime SDK — Void Saga Narrative Operating System

> **The Runtime SDK is not for users. It is for maintainers of the Narrative Operating System.**
>
> It is the first step toward making executable fiction authorable at scale.

---

## Purpose

The Runtime SDK standardizes character runtime creation.

Before the SDK, every runtime (NiuNiu, Sevraya, Zero, Julia) was handcrafted JSON — copying hundreds of lines, manually checking 29 required fields, and hoping nothing was missed.

After the SDK:

```
create_runtime Delphie
    ↓
fill evidence from .runtime.md
    ↓
validate — structural checks
    ↓
lint — semantic quality
    ↓
evidence_report — coverage diagnostic
    ↓
engine tests — constraint validation
    ↓
compiler dry run — prompt contract
    ↓
compiler live — Claude generation
```

No handwritten JSON. No missed fields. No guessing.

---

## Tools

| Tool | Purpose | Blocks on |
|------|---------|-----------|
| `create_runtime.py` | Generate new runtime from TEMPLATE | File exists (unless `--force`) |
| `validate_runtime.py` | Structural schema validation | Missing fields, wrong types |
| `lint_runtime.py` | Semantic quality checks | Placeholders, missing essentials |
| `evidence_report.py` | Evidence tag distribution diagnostic | Never — advisory only |

---

## Quick Start

### 1. Create a new runtime

```bash
python3 create_runtime.py Delphie
```

Produces: `../data/runtimes/Delphie.runtime.json`

- 29 required fields present ✅
- Architecture set to `RUNTIME_ARCHITECTURE_V2.1` ✅
- Schema reference correct ✅
- Version initialized to `1.0.0` ✅
- All content fields use `PLACEHOLDER` markers

### 2. Fill in evidence

Open the generated JSON. Replace every `PLACEHOLDER_*` with actual content extracted from the character's `.runtime.md` file and canon sources.

Work section by section in this order:

1. **Canon baseline** — timer range, protocols, audit basis
2. **Runtime status** — evidence counts, limitations, tags
3. **Runtime class** — operational modes, classification note
4. **Primary contradiction** — thesis, explanation
5. **Core wound** — name, structure, origin event
6. **Core desire** — statement, source, conflict with defense
7. **Defense system** — primary, secondary, signature, disabled-by
8. **Trigger conditions** — when each defense fires
9. **Voice grammar** — tone, characteristics, examples
10. **Invocation pattern** — which boot phases, what role
11. **Cost pattern** — what was paid per invocation
12. **Consequence pattern** — what resulted
13. **Residue pattern** — what persists
14. **Relationship interfaces** — one per significant relationship
15. **Evolution stages** — one per operational mode
16. **Canon gravity** — what must happen
17. **Anti-gravity** — what must NOT happen
18. **Forbidden behaviors** — hard constraints
19. **Failure mode** — how the character breaks
20. **Terminal state** — end-state properties
21. **Fork sensitive traits** — what can be modified
22. **Fork invariants** — what cannot change
23. **Fork points** — named divergence scenarios
24. **Sigil** — glyph, function, status
25. **Stress test prompts** — 3-5 violation scenarios
26. **State variables** — mutable internal state

### 3. Validate

```bash
python3 validate_runtime.py ../data/runtimes/Delphie.runtime.json
```

Must pass with `✅ VALIDATION PASSED` before proceeding.

### 4. Lint

```bash
python3 lint_runtime.py ../data/runtimes/Delphie.runtime.json
```

Address all ERROR findings. WARNING findings should be reviewed — they may be acceptable for v1.0.0.

### 5. Evidence diagnostic

```bash
python3 evidence_report.py ../data/runtimes/Delphie.runtime.json
```

Check that [E] ratio is ≥ 50%. Below that, the runtime may not be sufficiently grounded in canon.

### 6. Test

Create 2+ test scenarios in `../engine/scenarios_v2/`:
- One canon PASS scenario
- One VIOLATION scenario

Run engine validation:

```bash
python3 ../engine/engine_v2.py ../engine/scenarios_v2/test_delphie_pass.json
```

### 7. Compiler dry run

```bash
python3 ../compiler/compiler.py ../engine/scenarios_v2/test_delphie_pass.json
```

Check prompt contract and constraint evaluation before spending API tokens.

### 8. Compiler live

```bash
python3 ../compiler/compiler.py ../engine/scenarios_v2/test_delphie_pass.json --live
```

---

## TEMPLATE.runtime.json

The template satisfies Runtime Schema V2.1 structurally. Every required field exists. Unknown values use `PLACEHOLDER` markers.

Future runtime authors should edit **content**, not **structure**.

The template is the single source of truth for what a valid runtime looks like. If the schema changes, update the template first, then regenerate.

---

## Design Principles

1. **Schema-first.** TEMPLATE is the law. Tools enforce the template.
2. **Progressive disclosure.** create → validate → lint → evidence → test → compile. Each step adds confidence.
3. **Diagnostic, not prescriptive.** Lint and evidence tools report quality — they don't block. Only validate blocks.
4. **No engine coupling.** SDK tools read runtime JSON. They do not import engine modules. They do not call Claude.
5. **Authoring velocity.** The metric is: how fast can a maintainer go from "this character needs a runtime" to "compiler live generation works"?

---

## Current Runtime Inventory

| Runtime | v | [E] | [I] | [PC] | Stages | Rels | Created |
|---------|---|-----|-----|------|--------|------|---------|
| NiuNiu | 2.1.0 | 63 | 15 | 6 | 4 | 7 | Handcrafted |
| Sevraya | 2.0.0 | 57 | 14 | 3 | 6 | 6 | Handcrafted |
| Zero | 1.0.0 | 28 | 12 | 2 | 6 | 4 | Handcrafted |
| Julia | 1.0.0 | 55 | 18 | 3 | 4 | 7 | Handcrafted |
| *Delphie* | — | — | — | — | — | — | **First SDK runtime** |

---

## Future

- `diff_runtime.py` — compare two versions of a runtime, show what changed
- `migrate_runtime.py` — upgrade a runtime to a newer schema version
- `batch_validate.py` — validate all runtimes in a directory
- Integration with CI — block PRs that break runtime validation

---

*Runtime SDK v1.0.0 — The authoring toolkit for executable fiction.*
