# Open Questions — Executable Fiction Research

> 2026-06-26. Theory milestone: `27312d5`. These questions emerged from the GUA-LO-Aisya experiments. None are answered. All are testable.

---

## 1. Is the Relationship Contract a new first-class artifact?

Current state: all invariants live inside character runtimes. But GUA and LO revealed that many invariants only emerge when two characters interact. MERGE. Napkin. 3 AM Door. Orbit.

Question: should the system have a separate artifact type — `*.contract.json` — that sits alongside `*.runtime.json` and holds pair-level invariants?

Implication: if yes, individual runtimes become shorter and cleaner. Relationship behavior is extracted OUT of character runtimes and INTO pair contracts.

Test: extract GUA-LO invariants into a separate contract file. Compare GUA.runtime before and after. Does the runtime become cleaner? Do the invariants make more sense at the pair level?

---

## 2. Is Character Runtime just one serialization target among many?

Current state: everything is a `*.runtime.json`. The schema assumes "runtime = character."

But the theory now says: the compiler serializes invariants, not entities. An invariant observed at the individual scale becomes a Character Runtime. An invariant observed at the pair scale becomes a Relationship Contract. An invariant observed at the world scale becomes a World Protocol.

Question: should the root abstraction be `SerializableArtifact`, with `Runtime`, `Contract`, `Protocol`, and `Law` as subtypes?

Implication: if yes, the schema hierarchy inverts. Runtime is no longer the root object. It is one implementation of a more general interface.

Test: sketch a minimal schema where `{type: "runtime"|"contract"|"protocol"|"law", invariants: [...]}` is the root. Does the compiler work unchanged?

---

## 3. Does the compiler compile stories, or evidence?

Current framing: "the narrative compiler compiles stories."

But if the pipeline is `Observation → Repetition → Invariant → Serialization → Compilation`, then the story is not the thing being compiled. The story is the **source of evidence.** The compiler compiles the invariants extracted from that evidence.

Question: is the compiler story-agnostic? Could the same pipeline accept evidence from a screenplay, a visual novel script, RPG session logs, a chat transcript, a diary, or an interview transcript?

Implication: if yes, Executable Fiction is not a "novel compiler." It is an **evidence compiler** — a system that extracts behavioral invariants from any sequential narrative medium and tests new scenes for consistency.

Test: feed the pipeline a non-prose narrative form (e.g., screenplay dialogue, chat logs). Does the extractor detect behavioral patterns? Does the compiler flag violations?

---

## 4. Do invariants always emerge from repeated observation?

Current assumption: invariants are products of repeated observation. Confidence scales with observation count.

But: what about an invariant the author knows is true but has not written yet? What about an invariant derived from a single high-impact scene rather than many repetitions? What about an invariant that IS the character but only appears once — like Batman's origin?

Question: is "repeated observation" the ONLY path to invariant crystallization, or are there other paths (authorial declaration, single-event trauma, cultural consensus)?

Implication: if other paths exist, the confidence model needs to account for them. An author-declared invariant might start at confidence 0.80 even with zero observations — but the system must track that it is declared, not observed.

Test: compare a runtime built purely from observation (Aisya, 5 chapters) with a runtime built from authorial declaration (a character spec written before any prose). Do they produce different compiler behavior? Should they?

---

## 5. Should confidence attach to the invariant, not the artifact?

Current state: `runtime_status.confidence = 0.35` describes the entire runtime.

But different invariants within the same runtime have different observation counts. "Aisya deflects with humor" (observed 8 times) should have higher confidence than "Aisya accepts help after exactly 3 alternatives" (observed 2 times).

Question: should confidence be per-invariant rather than per-runtime? Should each invariant carry its own evidence count, violation count, and confidence score?

Implication: if yes, the compiler's verdict becomes more granular. Instead of "WARNING — runtime confidence 0.35," it says "WARNING — invariant 'deflects with humor' confidence 0.68, invariant '3 alternatives before accepting help' confidence 0.22."

Test: modify the Aisya runtime to include per-invariant confidence. Run the compiler. Does the output change in a useful way?

---

## Related

- `docs/OBSERVE_PIPELINE.md` — the research instrument designed to test these questions empirically.
- `docs/BEHAVIORAL_INVARIANTS.md` — the theoretical foundation.

---

## Status

These five questions define the next research phase. They emerged from a single day of experimentation (GUA, LO, Aisya) but their answers will determine the architecture of Executable Fiction v2.

None are urgent. The theory should be allowed to settle while more prose is written. The best validation is: do the same patterns emerge independently from different stories, written at different times, in different genres?

If they do, the answers to these questions will become obvious.

If they don't, the questions themselves may need revision.

---

*Written 2026-06-26. Based on the GUA-LO-Aisya experiments and subsequent theoretical refinements. To be revisited after more stories exist as evidence.*
