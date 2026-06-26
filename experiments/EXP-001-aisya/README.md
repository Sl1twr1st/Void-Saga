# EXP-001 — Aisya (Band 8 Universe)

## Question

Can behavioral invariants emerge from 5 chapters of contemporary realist prose written without any Executable Fiction planning?

## Hypothesis

Yes. If behavioral invariants are products of repeated observation rather than authorial design, then a character written organically for 5 chapters should exhibit detectable patterns — even in a realist genre with zero speculative elements.

Prediction: confidence will be low (~0.30–0.40) due to small sample size, but patterns should be extractable.

## Dataset

- **Universe:** Band 8 (contemporary realist)
- **Character:** Aisya (ex-drummer, PhD candidate)
- **Chapters:** 5 (`writing/day-01/1 Arrival LAX.md` through `5 Dinner.md`)
- **Word count:** ~2,559
- **Genre:** Contemporary realist. No speculative elements.
- **Author intent:** Written as pure prose. No runtime planning.

## Method

- **Pipeline:** Manual Observe → Propose → Review → Serialize (OBSERVE_PIPELINE.md Phase 1–4, executed by Claude)
- **Extraction:** Heuristic name detection + dialogue pattern analysis + manual invariant formulation
- **Schema:** RUNTIME_SCHEMA_V2.1 (29 fields)
- **Date:** 2026-06-26

## Result

### Extraction
- **7 candidate patterns** identified from 5 chapters
- **5 patterns accepted** as invariants (author review in-line during extraction session)
- **Runtime serialized:** `VOID_SAGA_UNIVERSE/apps/data/runtimes/Aisya.runtime.json`
- **Confidence:** 0.35 (Draft maturity)

### Invariants accepted

| # | Invariant | Evidence count | Tag |
|---|-----------|---------------|-----|
| 1 | Deflects with humor/intellect before emotional honesty | 5 chapters, ~8 observations | [E] |
| 2 | Refuses help/offers before accepting | 3 chapters, ~5 observations | [E] |
| 3 | Cannot speak emotional vocabulary in dialogue | 5 chapters, ~10 observations | [E] |
| 4 | Body overrides defense behind drum kit | 1 chapter (ch4), 2 observations | [E] |
| 5 | Overthinks major decisions | 3 chapters, ~4 observations | [I] |

### Compiler validation

| Scenario | Result |
|----------|--------|
| Studio soundcheck (with protest + play) | 🟡 WARNING (canon score 1.0, low confidence 0.74) |
| Direct emotional confession (no armor) | 🔴 BLOCKED (3 violations, canon score 0.90) |

## Conclusion

**Supports hypothesis.** Five chapters of contemporary realist prose produced 5 extractable behavioral invariants with evidence citations. Confidence (0.35) is low but expected for the sample size.

Key finding: the compiler enforced constraints correctly despite the character having no speculative elements, no sigils, no world DNA. The constraint engine is universe-agnostic.

### Limitations
- Manual extraction (Claude read prose, formulated invariants). Not yet automated via observe pipeline.
- 5 chapters is small sample. Confidence convergence cannot be measured without more chapters.
- Only one character extracted. Sita, Maya, Ika remain unextracted.
- Anti-gravity/false positives required 3 rounds of tuning — a known limitation of keyword-based matching.

### Next
- Extract Sita as Draft Runtime for comparison.
- Write chapters 6–10. Re-run extraction. Measure confidence delta.
- Compare Aisya's confidence curve against GUA (25 chapters) and LO (25 chapters).

---

*Experiment conducted 2026-06-26. Method: manual Observe → Propose → Review → Serialize.*
