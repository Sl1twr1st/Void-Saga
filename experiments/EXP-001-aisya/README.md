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

*Phase A conducted 2026-06-26. Method: manual Observe → Propose → Review → Serialize.*

---

## Phase B — Noise Robustness Spot-Check (2026-06-26)

### Question

Do previously observed Aisya candidate invariants remain detectable when new chapters are written organically, without compiler-aware structuring, under normal drafting noise?

### Hypothesis (Noise Robustness)

Behavioral invariants should remain detectable despite normal drafting noise — fragmented narrative, non-linear scenes, and prose written without Executable Fiction intent.

### Dataset

| Field | Value |
|-------|-------|
| **Source** | `writing/day-02/` |
| **Chapters** | 6 Night, 7 Force Majeure Emosional, 8 Sprinkler, Iblis, dan Pintu yang Dikunci, 9 Emotionally Bruises, 10 Cute Gitaris |
| **Word count** | ~85 KB across 5 files |
| **Method** | Organic / chaotic / throw-up writing |
| **Author intent** | Written as pure prose. No runtime planning. No scene triage. |
| **Date** | 2026-06-26 |

### Method

Lightweight spot-check — read all 5 chapters, matched observed behavior against 5 candidate invariants from Phase A. No re-extraction. No new invariant formulation. Conservative: evidence counted only when behavior was directly observable in text.

### Result

| # | Invariant | Phase B Evidence | Status |
|---|-----------|-----------------|--------|
| 1 | Deflects with humor/intellect before emotional honesty | Multiple observations across ch 6, 8, 9 | Supporting evidence added |
| 2 | Refuses before accepting ("nggak… iya" pattern) | Multiple observations across ch 8, 9 | Supporting evidence added |
| 3 | Cannot speak emotional vocabulary directly in dialogue | Strongest additional evidence; present in nearly every chapter | Supporting evidence added |
| 4 | Body overrides defense behind drum kit | No drum-kit context appears in ch 6–10 | Untestable |
| 5 | Overthinks major decisions | Multiple observations; qualitatively stronger | Supporting evidence added |

**Detection rate:** 4/5 candidate invariants received additional supporting evidence. 1/5 was untestable due to missing context.

### Key findings

1. **Chaos did not destroy the signal.** Despite being written organically, non-linearly, and without compiler-aware structuring, the same behavioral signals remained detectable. This adds supporting evidence to the Noise Robustness Hypothesis.

2. **This does not prove the runtime is final.** Additional evidence strengthens existing candidate invariants; it does not validate the serialized runtime. Full re-extraction with the updated dataset is a separate experiment.

3. **Invariants may evolve in manifestation while retaining the same underlying pattern.** Aisya's overthinking (Invariant 5) was previously observed as internal/personal deliberation ("Should I take the PhD?"). In Phase B, it manifests as systems-level social simulation — modeling the probable behavior of 5 other characters as input to her own decision:

   > "Kalau gua bilang nggak, Ratna akan cari sendiri. Ika akan pura-pura ini prosedur. Priska akan menemukan cara membuatnya jadi tontonan. Maya akan bilang semua orang harus jujur... Candice akan bikin folder index. Jadi lebih baik gua ada di ruangan."

   The pattern (overthinking-as-decision-mechanism) persists; the expression (internal → multi-agent simulation) deepens. This raises a question for future theory: *does an invariant describe a fixed behavior, or the shape of a behavioral trajectory?*

### Metrics for future Phase C runs

| Metric | Definition | Phase A | Phase B |
|--------|-----------|---------|---------|
| **Detection Rate** | Candidate invariants with new evidence / total checked | — | 4/5 |
| **New Evidence Count** | Chapters producing at least one observation | 5/5 | 5/5 |
| **Noise Robustness** | Detection rate under unstructured prose | — | 4/5 (1 untestable) |
| **Candidate Discovery** | New invariants not in previous phase | — | Not assessed |
| **Untestable Context Count** | Invariants with zero opportunity for observation | — | 1/5 |

### Limitations

- Spot-check only. No re-extraction performed. New invariants may exist that were not captured.
- 1 untestable invariant does not imply disconfirmation — only missing context.
- 5 additional chapters increase total dataset to 10 (~87.5 KB). Still a small sample.
- No inter-rater verification. Single reader (Claude session).
