# Primitive Is Repeated Observation, Not Character

**Date:** 2026-06-26
**Status:** Accepted. Supersedes previous framing of Executable Fiction as character-first.

---

## Context

The Aisya Draft Runtime had just been extracted — the first non-Void-Saga runtime, from 5 chapters of contemporary realist prose. The extraction worked: 5 behavioral invariants identified, serialized, and validated against the compiler.

During the same session, draft runtimes for GUA and LO (the two narrators of Void Saga) were extracted from 25 chapters each. These extractions revealed something the character-first framing could not accommodate.

---

## Before

Executable Fiction was framed as:

> Encoding behavioral invariants of characters so the compiler can test new scenes for consistency.

The assumption was that invariants belong to individual characters. A runtime is a character. A contract is between two characters. The entity boundary was the character boundary.

This framing was implicit in:
- The runtime schema (one file per character)
- The compiler architecture (load runtimes → evaluate constraints per character)
- The language we used: "character runtime," "character invariant"

---

## Trigger

While reviewing GUA and LO runtimes together, several critical patterns did not fit into a single character:

- **MERGE** — LO gets on a plane. This is not GUA's behavior or LO's behavior. It is a **protocol between them** that activates under specific conditions.
- **3 AM Door** — GUA opens the door at 3 AM without asking who is there. LO is always the one standing outside. Neither character does this with anyone else.
- **Napkin** — The Relationship Protocol v2.0 was written on a napkin. The napkin is not a character. It is an artifact produced by an interaction pattern.
- **Timer 25:00** — GUA returns to Jakarta only to write the final Timer. The behavior belongs to neither GUA nor LO alone. It belongs to the **joint authorship** that defines their relationship.
- **Orbit** — GUA and LO maintain a stable distance that neither can close and neither can leave. The orbit is the invariant. It cannot be assigned to GUA or LO individually.

These are not edge cases. They are central to the narrative architecture of Void Saga. A theory that cannot accommodate the MERGE protocol is a theory that does not describe the most important thing in the story.

---

## Decision

**The primitive of Executable Fiction is repeated observation, not character or interaction.**

Character runtime, relationship contract, world protocol, and narrative law are not different kinds of things. They are the same kind of thing — a curated collection of invariants — observed at different scales.

The unit of observation may vary. The unit of compilation is the invariant.

---

## Reasoning

If the compiler only understands character-level invariants, then the MERGE protocol must be awkwardly squeezed into GUA's runtime AND LO's runtime — duplicated, decontextualized, and stripped of its interactional nature.

But the MERGE protocol is not "GUA does X" or "LO does Y." It is:

> When LO says MERGE, GUA opens the door. This has held across 25 chapters. Confidence: 0.90.

The invariant belongs to the **pair.** Not to GUA. Not to LO.

The Mr. Bean Test already pointed in this direction. Mr. Bean's invariant ("simplest solution → most chaotic outcome") is observable at the character level. But the test was only a proof that invariants exist at the individual scale. It did not prove that invariants ONLY exist at the individual scale.

GUA-LO proved that the individual scale is not sufficient.

The revised framing:

```
Repeated observation of behavior
        │
        ▼
Candidate invariant
        │
        ▼
Serialized to appropriate target:
  ├── Character Runtime     (individual scale)
  ├── Relationship Contract (interaction scale)
  ├── Social Protocol       (community scale)
  ├── World Protocol        (world scale)
  └── Narrative Law         (cross-world scale)
```

All five targets are the same underlying thing: invariants. Only the observation scope differs.

---

## Implications

1. **The compiler architecture must eventually support non-character targets.** Currently the compiler loads runtimes and contracts separately. In the long term, these should be a unified invariant store with a `scope` field. (Not now — schema changes wait for theory settlement.)

2. **Confidence scales with observation count, not with entity complexity.** A relationship contract observed 15 times (confidence 0.90) is stronger than a character runtime observed 5 times (confidence 0.35). The target type does not determine confidence. The evidence count does.

3. **The extraction pipeline does not need to know what it is extracting.** Whether the output is a character runtime, a relationship contract, or a world protocol, the observe → propose → review → serialize pipeline is identical. Only the serialization target changes.

4. **New target types can be added without changing the primitive.** If we later discover that a particular narrative pattern is best serialized as a "Location Protocol" or a "Temporal Invariant," the primitive does not change. Observation → invariant → serialization target.

5. **The theory is now scale-free.** The same primitive that describes Aisya's humor deflection also describes the Living Chain (six characters, shared cost, forced honesty, 666 days). Same mechanism, different scope.

---

## Open Questions

1. **Is Relationship Contract the right name for the interaction-scale target?** Or is "Pair Invariant," "Dyad Protocol," or something else more precise?

2. **At what evidence threshold does a pair-level invariant stabilize into a contract?** The MERGE protocol has ~15 observations across 25 chapters. Would it be detectable at 5 chapters? 10?

3. **Do all interaction invariants require both characters to be present in the scene?** Some GUA-LO invariants manifest when they are apart (the long-distance decay pattern, the ghost commit). Does the compiler need to model absence?

4. **What is the relationship between a character invariant and a contract invariant that involves that character?** If Aisya "deflects with humor" and Aisya-Sita "maintains calibrated distance," are these two independent invariants or two manifestations of the same underlying pattern?

5. **Can a contract invariant exist without character invariants?** Is the MERGE protocol derivable from GUA's and LO's individual patterns, or does it emerge from their interaction in a way that cannot be reduced to individual behavior?

---

## Related

- `docs/BEHAVIORAL_INVARIANTS.md` — Section 2.1: Possible Serialization Targets. The scale hierarchy.
- `experiments/EXP-001-aisya/README.md` — First cross-universe runtime. Character-scale only (so far).
- [[2026-06-26-discovered-not-declared]] — The observation pipeline decision. Why runtime creation cannot start from author declaration.
- [[2026-06-26-confidence-per-invariant]] — Confidence belongs to the invariant, not the entity. (Not yet written.)
