# Executable Fiction v2 — Behavioral Invariants

> **NOTE (2026-06-26):** This document has been superseded by [`BEHAVIORAL_INVARIANTS.md`](./BEHAVIORAL_INVARIANTS.md), which separates the theory (what makes a character executable) from the engineering (how invariants are extracted and compiled). This document is preserved for provenance — it captured the initial insight. The canonical theoretical statement is now in `BEHAVIORAL_INVARIANTS.md`.

---

## The Reframing (Preserved from Original)

On 2026-06-26, while creating the Aisya Draft Runtime — the first runtime for a non-Void-Saga, contemporary realist universe — a critical error in framing was identified.

The previous assumption was:

> "The compiler works because characters are psychologically coherent."

This is wrong. Or at least imprecise in a way that matters.

The correct framing is:

> "The compiler works because characters exhibit stable behavioral invariants."

The difference is not semantic. It changes what Executable Fiction applies to.

---

## Evidence: The Mr. Bean Test

Consider Mr. Bean.

- Almost no dialogue
- No internal monologue
- No character development across episodes
- No psychological depth whatsoever

Yet Mr. Bean is executable. Why?

Because he has a law:

> Mr. Bean always attempts the simplest possible solution, which always produces the most chaotic possible outcome.

That is not psychology. That is a behavioral invariant.

If Mr. Bean were placed in a scenario where he carefully plans a complex solution and executes it flawlessly — the compiler should flag it. Not because it violates his "psychology." Because it violates an observed invariant.

---

## Examples Across Genres

| Character | Invariant | Genre | Psychological Depth |
|-----------|-----------|-------|---------------------|
| Sherlock Holmes | Does not rest until the pattern is complete | Detective | Moderate |
| Batman | Does not kill | Superhero | High |
| Hercule Poirot | Always seeks order and symmetry | Mystery | Low |
| Gandalf | Does not use full power unless absolutely necessary | Fantasy | Low (archetypal) |
| Mr. Bean | Simplest solution → most chaotic outcome | Comedy | None |
| Aisya | Deflects direct emotional inquiry with humor or intellect | Contemporary Realist | High |

The compiler works across all of these. Not because they share a genre. Not because they share a level of psychological realism. Because they share **stable behavioral laws.**

---

## The Boundary of Executable Fiction

The question is not:

> "What genres can be compiled?"

The question is:

> "Do the characters in this story exhibit behavioral invariants stable enough that a system can learn them, model them, and test new scenes for consistency?"

If yes: executable.

If no — if the story is deliberately built on characters who are random, patternless, or change without any observable law — that is also valid fiction. It is simply outside the problem space that Executable Fiction solves.

Kafka might not be executable. That is not a failure of the compiler. It is a category distinction.

---

## From Prescriptive to Descriptive

### v1 (Current): Prescriptive Constraints

The author defines what the character must and must not do:

```json
{
  "forbidden_behaviors": [
    {
      "behavior": "Speaking genuine feelings aloud with unguarded sincerity",
      "tag": "[E]"
    }
  ]
}
```

The compiler checks: "Does the scene violate this rule?"

The system is entirely dependent on the author's intuition about what the rules are.

### v2 (Future): Descriptive Invariants

The system observes the character across chapters, detects repeating patterns, proposes invariants, and the author approves or rejects:

```json
{
  "invariants": [
    {
      "statement": "When asked directly about her feelings, deflects with humor or intellectual framing",
      "confidence": 0.91,
      "evidence_count": 23,
      "first_observed": "chapter-01",
      "last_observed": "chapter-05",
      "violations_observed": 0,
      "source_scenes": [
        "chapter-01:lines-68-88",
        "chapter-02:lines-108-128",
        "chapter-05:lines-342-364"
      ],
      "status": "author_approved",
      "author_note": "Structural, not situational. Core defense."
    }
  ]
}
```

The compiler asks: "Does the new scene violate an invariant that has been observed 23 times across 5 chapters with zero prior violations?"

The system has observable evidence. The author retains final authority. The runtime becomes **a model of behavior extracted from the text, curated by the writer.**

---

## The Confidence Curve

Invariants are not binary (exists / doesn't exist). They emerge over time:

```
Chapter 1–3:    Pattern noticed. Confidence ~0.30.     Status: draft
Chapter 5–8:    Pattern repeats. Confidence ~0.65.     Status: beta
Chapter 10–15:  Pattern holds with few exceptions.    Confidence ~0.85.   Status: locked
Chapter 20+:    Pattern structural. Violation would    Confidence ~0.95.   Status: canonical
                require rewriting earlier chapters.
```

A Draft Runtime is not an incomplete runtime. It is a runtime whose invariants are at low confidence — still emerging, still subject to revision. The maturity levels (draft → beta → locked) are not about how many fields are filled. They are about **how stable the observed invariants have become.**

---

## Implications for Architecture

### 1. Runtime format should invert

Current: Core wound, core desire, defense system → constraints derived from these.

Future: Observed invariants are primary. Core wound and defense system become **interpretations of the invariants**, not sources of them.

### 2. The compiler's relationship to the author changes

Current: Author writes rules. Compiler enforces them.

Future: System observes patterns. System proposes invariants. Author approves or rejects. Compiler enforces the approved set.

The compiler becomes a **pattern detector** first, a constraint enforcer second.

### 3. Evidence traceability becomes critical

Every invariant must be traceable to specific scenes. "Aisya deflects under emotional pressure" must link to chapter-02:lines-108-128. Without traceability, invariants are just the author's opinion — which is the v1 approach we are moving beyond.

### 4. Cross-universe extraction becomes possible

If invariants are behavioral rather than psychological, the same extraction engine can work on:
- Void Saga (sci-fi / fantasy hybrid)
- Aisya's story (contemporary realist)
- Sherlock Holmes (detective)
- Mr. Bean (comedy)

The extraction engine does not need to understand genre. It needs to detect repetition, pattern, and rule-like regularity in character behavior.

---

## Workflow v2

```
Writer writes chapters (prose)
        │
        ▼
System scans for repeating behavioral patterns
        │
        ▼
System proposes invariants with confidence scores
        │
        ▼
Author reviews:
  ✓ Accept  → invariant enters runtime
  ✗ Reject → invariant discarded (with reason)
  ~ Modify → author adjusts the statement
        │
        ▼
Runtime grows organically from observed behavior
        │
        ▼
Compiler enforces only invariants the author has approved
```

The writer never writes a runtime from scratch. The writer writes prose. The runtime **emerges** from the prose and is **curated** by the writer.

---

## What This Does NOT Claim

1. **This does not claim all fiction is executable.** Fiction without stable character invariants exists. It is valid. It is outside this problem space.

2. **This does not claim the compiler understands meaning.** Invariant detection is pattern recognition, not semantic understanding. "Aisya deflects" is a behavioral regularity. The compiler does not know WHY she deflects.

3. **This does not claim invariants are permanent.** Characters can change. Invariants can break. But the break must be detectable — the system must see "this pattern held for 15 chapters and was violated in chapter 16" and flag it, not block it.

4. **This does not replace the author.** The system proposes. The author disposes. The compiler enforces only what the author has approved. Authorial intent remains sovereign.

---

## Next: From Theory to Implementation

What needs to be built to make v2 real:

| # | Component | Purpose |
|---|-----------|---------|
| 1 | Pattern detector | Scan N chapters, detect repeating behavioral sequences |
| 2 | Invariant proposer | From detected patterns, propose "X always does Y when Z" |
| 3 | Confidence calculator | Score each proposed invariant: frequency, recency, violation count |
| 4 | Evidence tracer | Link each invariant to specific lines/scenes |
| 5 | Author review interface | Accept / reject / modify proposed invariants |
| 6 | Runtime v2 schema | Runtime stores invariants, not just prescriptive constraints |

---

## Status

This document is a theoretical foundation. It does not deprecate the existing runtime schema, compiler, or engine. It defines the direction for the next major version.

The Aisya Draft Runtime (v0.1.0, 2026-06-26) was built using the v1 prescriptive approach — the author extracted constraints from 5 chapters manually. It proved that Executable Fiction works for non-Void-Saga universes.

The v2 approach — descriptive, observation-extracted, author-curated invariants — is the path to making this process automatic, scalable, and author-friendly.

---

## Related

- `VOID_SAGA_UNIVERSE/EXECUTABLE_FICTION_MANIFESTO.md` — the paradigm statement (v1)
- `VOID_SAGA_UNIVERSE/apps/data/runtimes/Aisya.runtime.json` — first non-Void-Saga runtime (v1 format)
- `dogfood/TASK_AISYA_DRAFT_RUNTIME_OUTPUT.md` — task output and draft maturity concept
- `CLAUDE.md` — project identity and current milestones

---

*Written 2026-06-26. Based on the Aisya Draft Runtime session and subsequent discussion with the Void Saga author. This document may itself evolve as the theory is tested against implementation.*
