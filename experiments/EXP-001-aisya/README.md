# EXP-001 — Aisya (Band 8 Universe)

## Question

Can behavioral invariants emerge from 5 chapters of contemporary realist prose written without any Executable Fiction planning?

## Hypothesis

Yes. If behavioral invariants are products of repeated observation rather than authorial design, then a character written organically for 5 chapters should exhibit detectable patterns — even in a realist genre with zero speculative elements.

Prediction: confidence will be low (~0.30–0.40) due to small sample size, but patterns should be extractable.

## Dataset

- **Universe:** Band 8 (contemporary realist)
- **Character:** Aisya (ex-drummer, PhD candidate)
- **Chapters:** 5 (`writing/band8/day-01/1 Arrival LAX.md` through `5 Dinner.md`)
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
| **Source** | `writing/band8/day-02/` |
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

---

## Phase C — Measurement Framework & Trajectory Tracking (Planned)

> Phase C is not about finding new invariants. It is about measuring whether existing invariants stabilize, strengthen, or decay as evidence accumulates across independently written datasets.

### Research Question

Does an invariant's confidence trajectory — measured across independently written datasets — converge toward a stable value, or does it oscillate unpredictably?

### Hypothesis (Signal Stability)

If behavioral invariants are genuine properties of a character rather than artifacts of a single dataset, then the same invariant should be detectable across independently written datasets — and its confidence should trend upward as cumulative evidence increases.

**Signal Stability** is the paired metric to **Noise Robustness:**

| Metric | Question | Phase |
|--------|----------|-------|
| **Noise Robustness** | Is the signal still visible when the draft is messy? | Phase B |
| **Signal Stability** | Does the same signal appear in independently written datasets? | Phase C |

Noise Robustness tests resilience against drafting chaos. Signal Stability tests reproducibility across observation contexts. Both are necessary. Neither is sufficient alone.

### Measurement Framework

By Phase C, EXP-001 will track six metrics per invariant:

| Metric | Definition | Type |
|--------|------------|------|
| **Confidence** | Evidence count / (evidence count + violations). Per-invariant, not per-runtime. | Quantitative |
| **Detection Rate** | Candidate invariants with new supporting evidence / total checked | Quantitative |
| **Noise Robustness** | Detection rate under unstructured, organic prose | Quantitative |
| **Signal Stability** | Does the same invariant appear across independently written datasets? | Binary per invariant |
| **Candidate Discovery** | New invariants not observed in previous phases | Count |
| **Untestable Context Rate** | Invariants with zero observation opportunity / total checked | Quantitative |

These six metrics together form the **Invariant Stability Index (ISI)** — a per-invariant score, not a single runtime score. Each invariant carries its own measurement history. Confidence belongs to the invariant, not the entity.

### Trajectory Tracking Table

The core output of Phase C is not a verdict. It is a trajectory:

```
Invariant                    Phase A   Phase B   Phase C   Trend
──────────────────────────────────────────────────────────────
Humor Deflection             0.35      0.42      ?         ↑
Refuse → Accept              0.31      0.39      ?         ↑
Emotional Vocabulary Gap     0.41      0.58      ?         ↑
Drum Override                0.28      Untest.   ?         ?
Overthinking                 0.33      0.51      ?         ↑
```

**Trend interpretation:**
- ↑ — confidence rising across datasets (supporting Signal Stability)
- → — confidence flat (stable but not strengthening)
- ↓ — confidence declining (possible disconfirmation — investigate)
- ? — insufficient data or untestable in current phase

A consistent ↑ trend across 3+ phases would provide the strongest evidence yet that behavioral invariants are genuine properties of the character, not artifacts of a single writing session.

### Next Experiment: Cross-Universe Validation

The most valuable Phase C is not more Band 8 chapters.

The most valuable Phase C is a **new novel, new author, new genre, zero Executable Fiction planning.**

```
Band 8 (Aisya)          → contemporary realist, single author
        vs
Universe X (new)        → different genre, different author
```

If the same observe → propose → review pipeline detects behavioral invariants in a completely independent universe — one with no relationship to Void Saga or Band 8 — then the methodology begins to separate from the project:

> Executable Fiction moves from "framework for this project" to "methodology testable across independent works."

That is the next research milestone.

### Phase C Design Constraints

- **Do not guide the writing.** The author writes pure prose. No runtime planning. No compiler awareness.
- **Do not re-extract from scratch.** Use the evolve mechanism: compare new evidence against existing invariants. Update confidence. Propose new patterns only if evidence crosses threshold.
- **Do not merge confidence.** Each invariant keeps its own trajectory. No averaging into a single "character confidence."
- **Track what disappears.** An invariant that was observable in Phases A–B but absent in Phase C is as informative as one that strengthens.

---

*Phase C is planned but not scheduled. It waits for a new independent dataset — a novel written without Executable Fiction awareness, in a genre and universe distinct from both Void Saga and Band 8.*
