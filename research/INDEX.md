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
| 2026-06-27 | **Executable Fiction Research Program** — repo identity shift | Audit: structure now reflects research program, not software project | ❌ Superseded same day by invariant-engine reclassification |
| 2026-06-27 | **invariant-engine reclassification** — project identity = invariant-engine; Void Saga = first dataset | `contra/` teardown + parent-folder discussion. Research claims downgraded until extractor + 2nd author + validation exist | ✅ Governs identity. `research/2026-06-27-invariant-engine-reclassification.md`; roadmap in `CLAUDE.md` Current Milestone |
| 2026-06-27 | **ID/EN precision gap = monolingual matcher**, not language quality | Jali: engine less precise on Indonesian prose. Diagnosis from `constraints.py` — English-syntax parser + token overlap, no stemming; invariants authored in English → cross-language penalty | ⏳ Parked for Fase 2. `research/2026-06-27-language-matching-bridge.md`. Bridge = Sastrawi (cheap) → multilingual embeddings (real, = contra #1). EXP-003 candidate. |
| 2026-06-27 | **Bab 00 Fork MVP** — genesis node forkability demonstrated via rule-based prototype | One-month focus: "Bab 00 bisa bercabang tanpa kehilangan hukum." Built `mvp/`: genesis node, 3 fork points, 7 laws, 4 fork examples, CLI checker (PASS / PRICE_REQUIRED / BLOCKED / VALID_FORK). All rule-based; verdicts declared by fork author, not auto-extracted. | ✅ Shipped as working prototype. `research/2026-06-27-bab00-fork-mvp.md` |
| 2026-06-27 | **v0.2 Language Bridge** — Indonesian surface + English internal bridge for fork checker | Existing forks English-dominant; novel + users are Indonesian. Added `title_id`, `premise_id`, `change_id`, `immediate_effect_id` (user-facing) + `internal_summary_en` (checker bridge). Checker is NOT multilingual — bridge is declarative, temporary. | ✅ Implemented. `research/2026-06-27-bab00-fork-mvp.md` (same log). |
| 2026-06-27 | **Milestone language audit** — overclaiming removed from CLAUDE.md | Per `contra/` discipline: "proven forkable" → "working rule-based prototype demonstrates"; "Proves Bab 00 is forkable" → "Working demonstration". Added explicit scope note: Bab 00 only, verdicts declared by author. | ✅ Applied to CLAUDE.md Current Milestone. |
| 2026-07-17 | **Canon as shared dependency** — canon-v1.0 proven as source of truth for a consumer outside itself (Node Reader); M2 reframed from "bikin importer" to "make subsystems consume canon" | Node reader spike (`abe65b1`): `?node=` routing + renderer abstraction backed by canon identity; UI requested zero canon/manifest/validator changes. Guardrail: consumer count = 1 today; "platform" label deferred until ≥2 independent consumers (Evidence Engine = M2 exit criterion). | ⏳ `research/2026-07-17-canon-as-shared-dependency.md`. Formal debt logged: legacy `bab00` IDs → canonical `bab-00`. |

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

*Updated 2026-06-27 (end of day). 12 entries. The timeline is cumulative — new entries are appended, never removed. Rejected decisions stay in the timeline with ❌ status. Provenance is preserved.*
