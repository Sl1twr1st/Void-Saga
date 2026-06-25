# Executable Fiction — Stability Milestone

**Version:** v0.2.3 — Paradigm Stability
**Date:** 2026-06-25
**Status:** DECLARED

---

## What This Is

This document marks the formal separation of **Executable Fiction** (the paradigm) from **Void Saga** (the reference implementation).

Before this milestone, Void Saga *was* the project. After this milestone, Void Saga is the first application of a broader discipline that has its own name, its own architecture, its own authoring method, and its own manifesto.

This milestone declares the following layers **stable at v0.2.x.**

---

## Layer Stability Declaration

| Layer | Artifact | Version | Stability |
|-------|----------|---------|-----------|
| **Paradigm** | EXECUTABLE_FICTION_MANIFESTO.md | v1.0.0 | Published |
| **Reference Universe** | Void Saga (25 Bab + 25 Timer + 5 Codex) | — | Complete |
| **Compiler** | compiler.py + engine_v2.py | v0.2.0 / v0.4.0 | First Light |
| **Runtime Schema** | RUNTIME_SCHEMA_V2.1.json | v2.1 | Stable (29 fields) |
| **Runtime SDK** | apps/runtime_sdk/ | v1.0.0 | Stable |
| **Authoring Method** | RUNTIME_AUTHORING_GUIDE.md | v1.0.0 | Stable |
| **Project Identity** | README.md | v2.0 | Stable |
| **Operational Handoff** | CLAUDE.md | v2.0 | Stable |
| **Architecture** | BLUEPRINT.md | — | Stable |

---

## Active Runtime Inventory

| # | Runtime | Version | Status | Created |
|---|---------|---------|--------|---------|
| 1 | NiuNiu | v2.1.0 | Production | Handcrafted |
| 2 | Sevraya | v2.0.0 | Production | Handcrafted |
| 3 | Zero | v1.0.0 | Production | Handcrafted |
| 4 | Julia | v1.0.0 | Production | Handcrafted |
| 5 | Delphie | v1.0.0 | Production | **First SDK runtime** |

**5 production runtimes. 2 authoring methods proven (handcrafted + SDK).**

---

## Test Coverage

| Type | Count |
|------|-------|
| Acceptance test scenarios | 21 |
| PASS demos | 1 (NiuNiu × Sevraya orbit) |
| BLOCKED demos | 1 (Zero emotional violation) |
| Engine self-tests | 17 scenario suite |

---

## Version History

| Tag | Milestone |
|-----|-----------|
| `v0.2.0-first-light` | Narrative Compiler First Light — live Claude generation proven |
| `v0.2.1-runtime-sdk` | Runtime SDK foundation — authoring tools shipped |
| `v0.3.0-fourth-runtime` | Julia serialized — 4th production runtime |
| *(next)* | **Executable Fiction v0.2.3 — Paradigm Stability** |

---

## What Is NOT Yet Stable

These are explicitly deferred beyond this milestone:

| Item | Status |
|------|--------|
| Remaining character runtimes (Agnia, Hasan, Gwaneum, etc.) | Future |
| CLI packaging (`void-saga compile`) | Future |
| Multi-universe support | Future |
| CI integration | Future |
| Visual constraint editor | Future |
| N-party conflict detection | Future |
| Engine v1.0.0 (hardened, optimized) | Future |

**Stability does not mean completion. It means the foundation is solid enough to build on.**

---

## What Changes After This Milestone

### Before

- Void Saga and Executable Fiction were the same thing
- Every new file was an experiment
- Architecture evolved week by week

### After

- Void Saga is the reference implementation of Executable Fiction
- Executable Fiction is a paradigm with its own identity
- Architecture changes require manifest rationale
- New runtimes follow the stabilized SDK workflow
- Breaking changes to the Runtime Schema require a version bump

### The bar is now higher

A new runtime must:
- [ ] Be created via SDK (`create_runtime.py`)
- [ ] Pass `validate_runtime.py`
- [ ] Pass `lint_runtime.py` with 0 errors
- [ ] Achieve ≥ 50% [E] ratio on `evidence_report.py`
- [ ] Have 2+ engine test scenarios (PASS + VIOLATION)
- [ ] Not modify engine, compiler, or schema

A new architectural document must:
- [ ] Not contradict the Manifesto
- [ ] Reference existing layers, not replace them
- [ ] Distinguish paradigm-level from Void Saga-level

---

## The Stack — Visualized

```
┌──────────────────────────────────────────────┐
│              EXECUTABLE FICTION              │  ← paradigm
│  ┌────────────────────────────────────────┐  │
│  │        AUTHORING METHOD                │  │  ← stable
│  │  ┌──────────────────────────────────┐  │  │
│  │  │        RUNTIME SDK               │  │  │  ← stable
│  │  │  ┌────────────────────────────┐  │  │  │
│  │  │  │    NARRATIVE COMPILER      │  │  │  │  ← first light
│  │  │  │  ┌──────────────────────┐  │  │  │  │
│  │  │  │  │  CONSTRAINT ENGINE   │  │  │  │  │  ← stable
│  │  │  │  │  ┌────────────────┐  │  │  │  │  │
│  │  │  │  │  │  VOID SAGA     │  │  │  │  │  │  ← reference
│  │  │  │  │  │  (reference)   │  │  │  │  │  │     universe
│  │  │  │  │  └────────────────┘  │  │  │  │  │
│  │  │  │  └──────────────────────┘  │  │  │  │
│  │  │  └────────────────────────────┘  │  │  │
│  │  └──────────────────────────────────┘  │  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```

Every layer is replaceable. The paradigm doesn't require Void Saga — it requires *a* reference universe. The compiler doesn't require the engine_v2.py implementation — it requires *a* constraint engine that enforces runtime contracts.

**The stack is the idea. The implementation is the proof.**

---

## Next Priorities (Post-Stability)

1. **Tag this milestone.** `v0.2.3-paradigm-stability`
2. **Update README** to reflect the paradigm/implementation distinction
3. **Choose next track only after stability is declared:**
   - Remaining character serialization (Agnia → Hasan → Gwaneum → ...)
   - Engine hardening (v1.0.0)
   - CLI packaging
   - Multi-universe proof-of-concept
   - Acceptance test expansion

---

*Declared at commit `3780d62` — the commit that shipped the Executable Fiction Manifesto. The paradigm has a name. The name has a document. The document has a version. The version is stable.*
