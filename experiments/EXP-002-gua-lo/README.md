# EXP-002 — GUA & LO (Void Saga Bab-level)

## Question

Can behavioral invariants emerge from 25 chapters of meta-narrative prose — characters who are themselves portrayed as "authors writing a novel" — written over 2 years without any Executable Fiction planning?

## Hypothesis

Yes. If behavioral invariants are products of repeated observation rather than authorial design, then characters written organically for 25 chapters across 2 years should exhibit stronger, higher-confidence invariants than a character written for 5 chapters.

Prediction: confidence will be higher than EXP-001 (0.35) due to larger sample size, despite the characters being in a realist register and never designed for extraction.

## Dataset

- **Universe:** Void Saga (Bab-level — the "authors" who write the Timer chapters)
- **Characters:** GUA (narrator, software engineer → farmer → writer) and LO (VP Engineering → founder → publisher)
- **Chapters:** 25 (`Bab 00 — ...` through `Bab 25 — ...`)
- **Genre:** Contemporary realist (the Bab frame). The characters exist in a realist register while co-writing a sci-fi/fantasy novel.
- **Author intent:** Written as pure memoir/narrative. No runtime planning across 2 years of writing.

## Method

- **Pipeline:** Manual Observe → Propose → Review → Serialize (OBSERVE_PIPELINE.md, executed by Claude)
- **Chapters read directly:** 3 of 25 (Bab 06, 08, 25)
- **Remaining evidence:** CLAUDE.md continuity log
- **Schema:** RUNTIME_SCHEMA_V2.1 (29 fields)
- **Date:** 2026-06-26
- **Status:** ⚠️ **Uncommitted.** Theory still settling. Runtimes held in working tree pending resolution of OPEN_QUESTIONS.

## Result

### Extraction — GUA
- **12 candidate patterns** identified from 25 chapters
- **5 invariants** at high confidence
- **Runtime extracted:** `VOID_SAGA_UNIVERSE/apps/data/runtimes/GUA.runtime.json` (uncommitted)
- **Confidence:** 0.45 (Draft maturity, higher than Aisya's 0.35)

| # | Invariant | Evidence | Confidence |
|---|-----------|----------|------------|
| 1 | Geographical escape after emotional crisis | 5 relocations across 25 chapters | HIGH |
| 2 | Builds systems/protocols to contain what can't be said directly | RELATIONSHIP PROTOCOL, AGREEMENTS.md, VoidOS, Inheritance Rule | HIGH |
| 3 | Commit messages as emotional diary | Bab 08: `// deprecate self.existence()` | HIGH |
| 4 | Autonomous mode after project completion | Bab 08 ending, 10-year silence | HIGH |
| 5 | LO's physical presence overrides exit system | Bab 08, Bab 25 | HIGH |

### Extraction — LO
- **10 candidate patterns** identified
- **4 invariants** at high confidence
- **Runtime extracted:** `VOID_SAGA_UNIVERSE/apps/data/runtimes/LO.runtime.json` (uncommitted)
- **Confidence:** 0.45

| # | Invariant | Evidence | Confidence |
|---|-----------|----------|------------|
| 1 | Detects GUA's signal degradation and intervenes without being asked | Bab 08: 15-hour flight, 3 AM door | VERY HIGH |
| 2 | Preemptive destruction when something becomes too important | Bab 06: "Gua hancurin duluan." | HIGH |
| 3 | Strategic opacity — reveals personal history only under pressure | Bab 16.5: first marriage reveal | HIGH |
| 4 | Frames care as system maintenance | "Ini integritas sistem." "Node lo lagi drop." | HIGH |

### Interaction discovery
- **Multiple invariants belong to the PAIR, not to either individual:**
  - MERGE keyword (LO defines, GUA receives)
  - 3 AM Door (LO initiates, GUA's defense collapses)
  - Napkin Protocol (co-authored artifact)
  - Orbit (structural pattern, not individual behavior)

This finding directly produced OPEN_QUESTIONS #1 and #2.

### Compiler validation

| Scenario | Result |
|----------|--------|
| GUA collapse → LO intervenes with structure → recovery | 🟢 PASS (canon score 1.0) |
| GUA confesses directly: "Gua takut, tolong jangan pergi" | 🔴 BLOCKED (2 violations, canon score 0.96) |

## Conclusion

**Supports hypothesis.** Twenty-five chapters of unplanned, organic character writing produced stronger invariants (confidence 0.45) than 5 chapters (0.35). The confidence difference is in the predicted direction.

### Key findings beyond the hypothesis

1. **Unit of observation ≠ unit of serialization.** Many invariants emerged from pair interaction, not individual behavior. This was not predicted by the theory at experiment time and directly generated OPEN_QUESTIONS #1.

2. **The mechanism is universe-agnostic.** GUA and LO exist in a realist register with no speculative elements. The same constraint engine that validates NiuNiu (sci-fi/fantasy) validated GUA (contemporary realist). The primitive does not change with genre.

3. **Confidence scales with chapters** across two independent experiments (Aisya: 0.35 at 5 chapters, GUA/LO: 0.45 at 25 chapters). Two data points do not confirm a curve, but they are consistent with the hypothesis.

### Limitations
- Only 3 of 25 chapters read directly. Remaining evidence from summaries.
- Manual extraction. Not automated.
- Anti-gravity tuning required 3 rounds (same limitation as EXP-001).
- Runtimes uncommitted — theory must settle before serialization is final.

### Next
- Do NOT commit GUA/LO runtimes until OPEN_QUESTIONS #1–#2 are answered.
- If Relationship Contract becomes first-class, extract pair invariants from individual runtimes.
- Compare against EXP-003 (new novel, different genre) when available.

---

*Experiment conducted 2026-06-26. Method: manual extraction. Status: uncommitted, pending theory settlement.*
