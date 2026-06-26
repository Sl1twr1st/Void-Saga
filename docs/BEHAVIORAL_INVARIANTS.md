# Behavioral Invariants: The Primitive of Executable Fiction

> A character is executable not because they are psychologically deep, but because they exhibit stable behavioral invariants — laws a system can learn, model, and test for consistency.

---

## 1. The Core Claim

Executable Fiction is not about encoding characters.

It is about encoding **behavioral invariants.**

A behavioral invariant is a statement of the form:

> "This character almost always does X when Y."

Or:

> "This character almost never does X."

The invariant does not explain WHY. It does not require psychology, backstory, or internal monologue. It only requires that the behavior is **stable enough to be observed, stated, and tested.**

---

## 2. The Primitive

All executable fiction systems rest on one primitive:

```
Behavioral Invariant
```

Everything else — runtimes, constraints, forbidden behaviors, canon gravity, anti-gravity, defense systems, trigger conditions, voice grammar — are **derived forms** of this single primitive.

A runtime is a curated collection of behavioral invariants attached to a character.

A constraint engine is a system that tests whether a new scene is consistent with the invariants collected so far.

A compiler is a system that reports the result of that test in a form the writer can act on.

---

## 3. The Mr. Bean Test

Consider Mr. Bean.

He has:
- Almost no dialogue
- No internal monologue
- No character development across episodes
- No psychological depth whatsoever

He is not "psychologically coherent" in any meaningful sense.

Yet he is executable.

Why?

Because he has a behavioral invariant:

> Mr. Bean always attempts the simplest possible solution.
> This solution always produces the most chaotic possible outcome.

If a writer submitted a scene where Mr. Bean carefully plans a complex, multi-step solution and executes it flawlessly — the compiler should detect the violation.

Not because it violates his psychology. He has none.

Because it violates an **observed behavioral invariant.**

The Mr. Bean Test proves that psychological depth is sufficient but not necessary for executable fiction. Behavioral invariants are the necessary condition.

---

## 4. Generality

Behavioral invariants cut across genre, medium, and character complexity:

| Character | Invariant | Genre | Psychology |
|-----------|-----------|-------|-------------|
| Sherlock Holmes | Does not rest until the pattern is complete | Detective | Moderate |
| Batman | Does not kill | Superhero | High |
| Hercule Poirot | Always seeks order and symmetry | Mystery | Low |
| Gandalf | Does not use full power unless absolutely necessary | Fantasy | Archetypal |
| Mr. Bean | Simplest solution → most chaotic outcome | Comedy | None |
| Aisya | Deflects direct emotional inquiry with humor or intellect | Contemporary | High |
| NiuNiu | Protects before being asked; never speaks fluently without external force | Sci-fi / Fantasy | High |

The compiler works across all of these. Not because they share a genre. Not because they share psychological realism. Because they share **stable behavioral laws.**

---

## 5. The Boundary Condition

The question that defines the scope of Executable Fiction is not:

> "What genres can be compiled?"

It is:

> "Do the characters in this story exhibit behavioral invariants stable enough that a system can observe them, model them, and test new scenes for consistency?"

If yes: the story is within the problem space of Executable Fiction.

If no — if a story is deliberately built on characters who are random, patternless, or change without observable law — that is also valid fiction. It is simply outside this problem space. The compiler has no law to enforce.

Kafka might not be executable. That is not a failure of the compiler. It is a category distinction. A story without behavioral invariants is like a physical system without conservation laws — it may be beautiful, but you cannot build an engine for it.

---

## 6. What the Compiler Actually Locks

The compiler does not lock **behavior.**

It locks **expectation.**

Consider Batman's invariant:

> Batman does not kill.

This has held for 87 years of stories.

If a writer submits a scene where Batman kills the Joker — is the scene automatically wrong?

No.

The scene is significant **precisely because the invariant is so strong.** Eighty-seven years of "does not kill" is what gives "Batman kills the Joker" its narrative weight.

The compiler should not say:

> BLOCKED. Batman does not kill.

The compiler should say:

> This violates an invariant observed across 87 years of stories. If you proceed, narrative price is required.

The invariant does not prevent the scene. The invariant **defines what the scene costs.**

This is the difference between a rule engine and a narrative operating system. A rule engine blocks. A narrative operating system calculates price.

---

## 7. The Third Path: PRICE REQUIRED

The compiler verdict space should have four states, not three:

| Verdict | Meaning |
|---------|---------|
| PASS | Scene is consistent with all known invariants |
| WARNING | Scene approaches an invariant boundary. Review. |
| PRICE REQUIRED | Scene violates a strong invariant. You may proceed, but the violation must be narratively accounted for. The invariant's strength IS the scene's weight. |
| BLOCKED | Scene violates an absolute invariant — one whose violation would destroy the character's identity, not just challenge it. |

PRICE REQUIRED is not a softer BLOCKED. It is a fundamentally different category.

A violation that carries PRICE REQUIRED means: the writer is choosing to break a known law. That choice IS the story. The compiler's job is not to prevent the choice. It is to ensure the writer **knows they are making it,** knows how strong the invariant is, and knows that the narrative must carry the cost.

This principle already exists in Void Saga — the Goetic Consequence System, residue theory, the idea that every invocation carries a cost. The theory now generalizes it: **every invariant violation is an invocation.** Every breakage of a known law produces residue.

---

## 8. Void Saga's True Role

Void Saga is not the center of Executable Fiction.

Void Saga is the **first dataset.**

The relationship is:

```
Executable Fiction (theory)
        │
        ▼
Runtime Model (abstraction)
        │
        ▼
Narrative Compiler (engine)
        │
        ├── Reference Universe: Void Saga     (sci-fi / fantasy)
        ├── Reference Universe: Band 8        (contemporary realist)
        └── Reference Universe: [future]      (any genre)
```

Void Saga was the first universe to be compiled. It proved the compiler could work. But it was never the only thing the compiler was for.

The Aisya Draft Runtime (2026-06-26) proved that the compiler works for a contemporary realist universe with no speculative elements. It confirmed that the compiler is universe-agnostic.

Mr. Bean, Sherlock Holmes, Batman — these are not implementations. They are **existence proofs.** They demonstrate that behavioral invariants exist across the entire spectrum of fiction, independent of genre, medium, or psychological depth.

---

## 9. What This Does NOT Claim

1. **This does not claim all fiction is executable.** Fiction without stable character invariants exists and is valid. It is outside this problem space.

2. **This does not claim the compiler understands meaning.** Invariant detection is pattern recognition, not semantic comprehension. The compiler detects that "Aisya deflects under emotional pressure." It does not know why.

3. **This does not claim invariants are permanent.** Characters can change. Invariants can break. The break must be detectable — "this pattern held for 15 chapters and was violated in chapter 16" — not automatically blocked.

4. **This does not replace the author.** The compiler is a tool for the writer, not a replacement for the writer. It detects patterns. The writer decides whether those patterns are laws.

5. **This does not claim every invariant is equally strong.** Invariants vary in confidence, in evidence count, in structural importance. Some are core identity. Some are situational. The compiler must distinguish between them.

---

## 10. What Follows From This

If this theory is correct, then the following are not separate design decisions — they are **consequences:**

- **Draft → Beta → Locked maturity levels** are a consequence of invariants having confidence curves. An invariant observed 3 times at confidence 0.35 is draft. An invariant observed 87 times at confidence 0.97 is locked.

- **Evidence traceability** is a consequence of invariants being empirical claims. Every invariant must be traceable to the scenes that produced it. Without traceability, it is not an invariant — it is an opinion.

- **Author approval** is a consequence of invariants being curated. The system proposes. The author decides what is law. The compiler enforces only what the author has approved.

- **Cross-universe compilation** is a consequence of the primitive being behavioral, not psychological or genre-specific. The same detection machinery works on Void Saga, Band 8, and Mr. Bean — because it is looking for the same thing: stable patterns of behavior.

- **PRICE REQUIRED** is a consequence of the compiler locking expectation, not behavior. A law that has never been broken carries immense weight when it finally is. The compiler must measure that weight, not prevent its use.

---

## 11. Status

This document defines the **theoretical primitive** of Executable Fiction.

It does not specify:
- How invariants are detected (engineering concern)
- How confidence is calculated (engineering concern)
- What the runtime schema v2 looks like (engineering concern)
- What the author review interface looks like (engineering concern)

These are implementation details. They are consequences of the theory, not the theory itself.

A separate document — the Invariant Extraction and Compilation Architecture — will address the engineering path from theory to working system.

---

## Related

- `docs/THEORY_EXECUTABLE_FICTION_V2.md` — earlier draft of this document (superseded, preserved for provenance)
- `VOID_SAGA_UNIVERSE/EXECUTABLE_FICTION_MANIFESTO.md` — the v1 paradigm statement
- `VOID_SAGA_UNIVERSE/apps/data/runtimes/Aisya.runtime.json` — first non-Void-Saga runtime
- `VOID_SAGA_UNIVERSE/apps/data/runtimes/NiuNiu.runtime.json` — first Void Saga runtime (v2.1.0)

---

*Written 2026-06-26. Based on the Aisya Draft Runtime session, the Mr. Bean Test, and subsequent theoretical refinement. This document makes a scientific claim about the nature of executable characters. It should be tested, challenged, and refined.*
