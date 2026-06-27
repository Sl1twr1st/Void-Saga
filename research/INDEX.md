# Research Index — Idea Evolution Timeline

> Not a table of contents. A map of how ideas evolved, which ones survived, and which ones are still open.

---

## Timeline

| Date | Decision | Trigger | Promoted to Theory? |
|------|----------|---------|---------------------|
| 2026-06-26 | **Primitive = repeated observation**, not character | GUA/LO extraction — MERGE, 3 AM Door, Napkin don't fit single-character model | ✅ `docs/BEHAVIORAL_INVARIANTS.md` |
| 2026-06-26 | **Runtime must be discovered**, never declared | Aisya extraction — author didn't consciously design invariants #3, #4, #5 | ✅ `docs/OBSERVE_PIPELINE.md` |
| 2026-06-26 | **Confidence belongs to the invariant**, not the entity | Aisya runtime — each invariant had different evidence counts | ⏳ Implicit in schema, not yet a standalone decision log |
| 2026-06-26 | **Observation precedes interpretation** | Aisya extraction — "deflects with humor" vs "is avoidant" | ✅ `docs/BEHAVIORAL_INVARIANTS.md` §2.3 |
| 2026-06-27 | **Noise Robustness Hypothesis** — invariants survive drafting chaos | EXP-001 Phase B — 4/5 invariants received additional supporting evidence from chaotic prose | ⏳ Documented in `experiments/EXP-001-aisya/README.md` Phase B. Not yet in theory docs. |
| 2026-06-27 | **Signal Stability** — paired metric to Noise Robustness | Discussion — "does the same signal appear in independently written datasets?" | ⏳ Documented in `experiments/EXP-001-aisya/README.md` Phase C. Not yet tested. |
| 2026-06-27 | **Invariant Stability Index (ISI)** — 6-metric per-invariant measurement framework | Discussion — confidence alone is insufficient | ⏳ Planned for Phase C. No implementation. |
| 2026-06-27 | **Executable Fiction Research Program** — repo identity shift | Audit: structure now reflects research program, not software project | ✅ This framing now governs all documentation |

## Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Promoted — the decision has been incorporated into stable theory docs |
| ⏳ | Open — documented in experiments or discussion, not yet in theory |
| ❌ | Rejected — tested and disproven, or superseded by a later decision |

## How to Use This Index

- **New to the project?** Start with `docs/BEHAVIORAL_INVARIANTS.md`. This index is for understanding how we got there.
- **Questioning a design choice?** Find the decision in the timeline, read the linked decision log in `research/`.
- **Adding a decision?** Add a row here. Update `Promoted to Theory?` when the decision makes it into `docs/`.

---

*Updated 2026-06-27. The timeline is cumulative — new entries are appended, never removed. Rejected decisions stay in the timeline with ❌ status. Provenance is preserved.*
