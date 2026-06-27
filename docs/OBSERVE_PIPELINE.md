# Observe Pipeline — Research Methodology for Executable Fiction

> The observation pipeline exists to collect evidence, not to manufacture canon.

---

## 1. Purpose

The Observe Pipeline is the research instrument of Executable Fiction. It does not create runtimes. It **collects evidence, proposes patterns, and lets the author decide what qualifies as an invariant.**

Its purpose is to test the core hypothesis:

> Behavioral invariants emerge from repeated observation of behavior. The longer and more consistently a character is written, the more extractable their invariants become.

The pipeline is designed so that this hypothesis can be empirically verified — by tracking observation history across multiple universes and measuring whether confidence converges as evidence accumulates.

---

## 2. Principles

1. **Observation precedes interpretation.** The pipeline detects behavioral patterns. It does not assign psychological labels. "Aisya deflects with humor before answering emotionally direct questions" is an observation. "Aisya is avoidant" is an interpretation. Only the first is executable.

2. **Evidence before claims.** Every proposed pattern must cite specific scenes or excerpts. A claim without a citation is invalid. This constraint applies to both heuristic extraction and LLM-assisted proposal.

3. **Human review is the gate.** The pipeline proposes. The author decides. A pattern does not become an invariant until the author accepts it. The word "invariant" is reserved for patterns that have passed human review.

4. **Confidence belongs to the pattern, not the entity.** A runtime does not have a single confidence score. Each pattern within it carries its own evidence count, its own observation history, its own confidence.

5. **The pipeline is cumulative.** Each new observation run builds on previous runs. Observation history is preserved as timestamped files. This is what makes the confidence convergence hypothesis testable.

---

## 3. Pipeline

```
writing/*.md (pure prose, no metadata)
        │
        ▼
┌─────────────────────────────────────┐
│  PHASE 1: OBSERVE                   │
│  ./scripts/observe writing/band8/day-01   │
│                                     │
│  Heuristic extraction              │
│  → Evidence Ledger (.ledger.json)   │
│  → Observation Report (human read)  │
└─────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────┐
│  PHASE 2: PROPOSE                   │
│  ./scripts/propose-runtime Aisya    │
│                                     │
│  LLM pattern proposal              │
│  (reads ledger + excerpt evidence)  │
│  → Pattern Proposal (with citations) │
└─────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────┐
│  PHASE 3: REVIEW                    │
│  (human decision)                   │
│                                     │
│  Accept → pattern becomes invariant │
│  Reject → pattern discarded          │
│  Modify → author adjusts statement  │
└─────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────┐
│  PHASE 4: SERIALIZE                 │
│  ./scripts/serialize-runtime Aisya   │
│                                     │
│  Accepted invariants                │
│  → runtime / contract / protocol    │
└─────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────┐
│  PHASE 5: EVOLVE                    │
│  ./scripts/evolve writing/band8/day-01    │
│                                     │
│  Compare new evidence against       │
│  existing invariants. Update        │
│  confidence. Propose new patterns.  │
└─────────────────────────────────────┘
```

Writing always comes first. The compiler always comes after. The pipeline does not prescribe what to write. It observes what has already been written.

---

## 4. Evidence Ledger

The evidence ledger is the ground truth layer. It is produced by heuristic (rule-based) extraction — reproducible, diffable, zero hallucination risk. It does not interpret. It counts.

### What the ledger captures

| Field | Method |
|-------|--------|
| `character_mentions` | Name frequency, chapter distribution |
| `scene_count` | Scene boundaries, chapter mapping |
| `dialogue_lines` | Count by character, by scene |
| `quoted_phrases` | Verbatim quotes with chapter:line references |
| `co_occurrence` | Which characters appear in the same scene |
| `interaction_pairs` | Which characters exchange dialogue |
| `chapter_distribution` | Which chapters each character appears in |

### Example ledger entry (conceptual)

```
Aisya:
  appears_in: [ch1, ch2, ch3, ch4, ch5]
  scene_count: 12
  dialogue_lines: 42
  co_occurs_with:
    Sita: 18 scenes
    Maya: 9 scenes
    Ika: 4 scenes (by phone)

Aisya-Sita:
  shared_scenes: 4
  direct_dialogue_turns: 31
  quoted_exchanges:
    - ch2:68-88 (Sita asks about past, Aisya deflects)
    - ch5:342-364 (Ika phone call, Aisya surrenders to the plan)
```

### Observation history

Each observe run produces a timestamped file:

```
observation_history/
  2026-06-26-observe.json
  2026-07-02-observe.json
  2026-07-10-observe.json
```

This history is the empirical foundation for the confidence convergence hypothesis. By comparing runs, we can measure:

- Does confidence rise as chapter count increases?
- Do new patterns emerge at predictable evidence thresholds?
- Does the same pattern appear independently in different observation runs?

---

## 5. Pattern Proposal

The Pattern Proposal phase uses an LLM — but the LLM is constrained. It does not read the prose freely. It receives:

1. The evidence ledger (structured counts, co-occurrence, quoted phrases)
2. Excerpt evidence (specific passages, chapter:line references)
3. A constrained prompt: "Propose candidate behavioral patterns. Every claim must cite evidence from the ledger or excerpts. No citation = invalid."

### What the LLM may output

```
Candidate Pattern:
  Aisya deflects with humor before answering emotionally direct questions.
  Evidence:
    - ch2:68-88 — Sita asks "Lo dulu suka gua." Aisya answers "Iya" quickly,
      then immediately deflects: "Sembari mengutuk Ratna. Mulut bangsat Ratna."
    - ch4:338-344 — Maya asks about motivation. Aisya intellectualizes:
      "Secara administratif: lolos. Secara naratif: kacau."
    - ch5:342-364 — Ika pushes. Aisya pivots to humor: "Ini terlalu berlebihan
      buat urusan diskografi."
  Confidence: 0.34
  Type: behavioral (character-level)

Candidate Pattern:
  Aisya refuses help or offers before accepting.
  Evidence:
    - ch2:24-41 — Sita offers ride: "Ikut gua dulu." Aisya's internal response:
      "Dia ingin mengajukan keberatan. Tapi keberatan butuh alternatif."
    - ch5:144-173 — Sita offers room. Aisya lists hotel, Airbnb, hostel.
      Accepts only after all alternatives fail.
  Confidence: 0.42
  Type: behavioral (character-level)
```

### What the LLM may NOT do

- Output a completed runtime JSON directly
- Make claims without citing evidence
- Assign psychological labels ("Aisya is avoidant")
- Declare a pattern as invariant (only human review can do that)

The LLM is an **analyst with a constrained mandate,** not an oracle.

---

## 6. Human Review

Human review is the gate between "pattern" and "invariant." The word "invariant" is reserved for patterns that have passed this gate.

### Review actions

| Action | Meaning |
|--------|---------|
| **Accept** | Pattern becomes an invariant. Enters the runtime/contract. |
| **Reject** | Pattern discarded. Recorded with reason. |
| **Modify** | Author adjusts the statement. "Deflects with humor" → "Deflects with humor or intellectual framing." |
| **Defer** | Not enough evidence yet. Keep observing. |

### Why human review is non-negotiable

The compiler enforces invariants. If a pattern is incorrectly promoted to invariant, the compiler will enforce a false constraint — blocking scenes that should be allowed.

The cost of a false positive in serialization (blocking a valid scene) is higher than the cost of a false negative (failing to detect a real invariant). Human review is the only mechanism that can weigh this asymmetry.

---

## 7. Serialization

Serialization is the final phase: converting accepted invariants into artifacts the compiler can use.

The key insight: **serialization is format conversion, not content creation.** All content decisions happened in Observe → Propose → Review.

### Serialization targets

| Scale | Artifact |
|-------|----------|
| Individual | Character Runtime (`.runtime.json`) |
| Interaction | Relationship Contract (`.contract.json` — proposed, not yet implemented) |
| Community | Social Protocol (future) |
| World | World Protocol (future) |
| Cross-world | Narrative Law (future) |

For v0.1.0, only Character Runtime serialization is implemented. Other targets are documented in OPEN_QUESTIONS.

---

## 8. Evolution

`./scripts/evolve` is the pipeline's cumulative mechanism. It does not re-extract from scratch. It compares new evidence against existing invariants.

### What evolve reports

```
Evolution Report
─────────────────
New evidence processed: +5 chapters (ch6-ch10)

Character: Aisya
  Confidence: 0.35 → 0.47
  Existing invariants:
    ✓ "deflects with humor" — reinforced (new evidence: ch6:45-52, ch8:112-118)
    ✓ "refuses before accepting" — reinforced (ch7:23-30, ch9:88-95)
  New candidate patterns:
    • "uses silence before difficult decisions" (evidence: ch8:201-208, ch10:15-22)

Interaction: Aisya ↔ Sita
  Interaction count: 8 → 21
  Existing contract: none
  Recommendation: Sufficient evidence for Draft Relationship Contract.

World:
  No recurring protocol detected.
```

### Why evolve matters

`evolve` is the command that makes the confidence convergence hypothesis testable. Each run adds a data point. Over time, confidence curves either converge (supporting the hypothesis) or don't (refuting it).

It also answers a practical writer question: "I just wrote 5 more chapters. What changed?"

---

## 9. Future Questions

This pipeline is a research instrument first, a writer tool second. The following remain open:

1. At what evidence threshold does a pattern become a "strong" invariant (confidence ≥ 0.80)? Is the threshold universal or universe-specific?

2. Can Relationship Contracts be extracted by the same observe → propose → review → serialize pipeline, or do they require a different mechanism?

3. Does the LLM pattern proposal phase produce consistent results across different LLM models and prompt formulations?

4. At what scale (how many chapters, how many interactions) do World Protocols become detectable?

5. Can the observe pipeline work on non-prose narrative forms — screenplays, RPG logs, chat transcripts?

See `docs/OPEN_QUESTIONS.md` for the full research agenda.

---

## Related

- `docs/BEHAVIORAL_INVARIANTS.md` — the theoretical foundation. Primitive = repeated observation.
- `docs/OPEN_QUESTIONS.md` — five research questions. None answered.
- `VOID_SAGA_UNIVERSE/apps/extractor/extract_scene.py` — current heuristic extraction (Phase 1 seed)
- `VOID_SAGA_UNIVERSE/apps/data/runtimes/Aisya.runtime.json` — first Draft Runtime, extracted via manual observe → propose → serialize

---

*Written 2026-06-26. This document describes a research methodology, not a completed implementation. The pipeline will be built incrementally as the theory is tested against evidence.*
