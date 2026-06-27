# Runtime Must Be Discovered, Never Declared

**Date:** 2026-06-26
**Status:** Accepted. Defines the implementation policy for all runtime creation.

---

## Context

The Aisya Draft Runtime was created manually: Claude read 5 chapters of prose, identified behavioral patterns, proposed candidate invariants, and the author accepted or rejected each one. The process worked — 5 invariants accepted, serialized, and validated.

Immediately after, the question arose: should we build a `create-runtime` tool to automate this?

The instinct to build tooling was strong. The extraction was manual and labor-intensive. A script that reads prose and outputs a runtime JSON felt like the obvious next step.

We did not build it. This log records why.

---

## Before

The previous implementation path, documented in the Runtime SDK and the 30-Minute Challenge, assumed:

> An author declares what their character is like. The compiler enforces those declarations.

The SDK provides a template (`TEMPLATE.runtime.json`), a creation script (`create_runtime.py`), and a validation script (`validate_runtime.py`). The workflow is:

```
Author intent → Runtime JSON → Compiler enforcement
```

This workflow assumes the author knows their character's invariants before writing. The author is the source of truth. The runtime is a declaration of intent.

---

## Trigger

During the Aisya extraction session, several patterns emerged that the author had NOT consciously designed:

- **Invariant #3 (emotional vocabulary gap):** The author did not plan for Aisya to be unable to speak emotional words. It emerged from the prose. When the pattern was pointed out, the author recognized it as true — but they had not intended it.

- **Invariant #4 (drum kit override):** This was present in only one chapter out of five. It was not "designed." It was a moment where the prose made a choice the author had not premeditated.

- **Invariant #5 (overthinking):** Originally observed as internal deliberation. In Phase B, it evolved into multi-agent social simulation — a manifestation the author did not anticipate when writing the first 5 chapters.

If the author had been asked to declare Aisya's invariants before writing, they would not have listed these. The invariants were **discovered in the prose, not declared before it.**

This raised a question: if the author cannot reliably declare their own character's invariants before writing, who can?

The answer: no one. Invariants are not declared. They are observed.

---

## Decision

**Runtime creation must begin with observation of existing prose, never with author declaration of intent.**

The correct workflow is:

```
observe → propose → review → serialize → evolve
```

Not:

```
declare → serialize → enforce
```

The observation pipeline exists to collect evidence, not to manufacture canon. Runtime is discovered from evidence, never declared upfront.

---

## Reasoning

### 1. Authors are unreliable reporters of their own characters

This is not a criticism. It is a property of how fiction writing works. Characters emerge through the act of writing. The author discovers the character at the same time the reader does — sometimes later.

Asking an author to declare invariants before writing is like asking a scientist to declare results before running the experiment. The declaration may be sincere. It is not evidence.

### 2. Intentions are not invariants

An author may intend for a character to be "brave" or "guarded" or "charismatic." But the prose may reveal a character who is brave in some situations and avoidant in others — a pattern the author did not consciously design but consistently executed.

The invariant is what the prose actually does, not what the author meant it to do.

### 3. Discovery is the mechanism that separates Executable Fiction from personality typing

If runtimes are author-declared, Executable Fiction is MBTI with JSON — assign a category, derive expected behaviors. "Aisya is an INTJ, therefore she deflects with humor."

But if runtimes are discovered from prose, Executable Fiction is an empirical methodology. The invariant is not true because the author said so. It is true because it was observed N times with 0 violations.

### 4. The pipeline already works this way

The Aisya extraction was manual — Claude read prose and proposed patterns. But the structure was:

```
Prose (5 chapters)
    ↓
Observe (read, identify patterns)
    ↓
Propose (5 candidate invariants with citations)
    ↓
Review (author accepts/rejects each)
    ↓
Serialize (convert to .runtime.json)
```

This worked. The output was a valid runtime that the compiler enforced correctly (PASS on orbit scene, BLOCKED on emotional confession, WARNING on studio soundcheck).

The manual pipeline proved the concept. Automating it is an engineering problem, not a theoretical one.

---

## Implications

### Implementation policy

**Do NOT build `create-runtime`** — a tool that asks the author to declare invariants and outputs a runtime JSON.

Instead, build (eventually, not now):

- `observe` — heuristic extraction from prose → evidence ledger
- `propose` — LLM-assisted pattern proposal (reads ledger, proposes invariants with citations)
- `review` — human gate (author accepts/rejects/modifies each pattern)
- `serialize` — format conversion only. No content creation.
- `evolve` — rerun observe + propose on additional chapters. Compare against existing invariants.

### Naming discipline

The word "invariant" is reserved for patterns that have passed human review. Before review, they are "candidate patterns" or "proposed invariants." This distinction prevents the system from treating unverified LLM output as ground truth.

### Author role

The author is the gate, not the source. The author does not declare what is true. The author decides whether an observed pattern qualifies as an invariant.

This preserves authorial authority while acknowledging that authors do not have perfect introspective access to their own characters.

### Confidence direction

Confidence rises with observation count. An author-declared runtime would have confidence 1.0 on day one — which is meaningless. An observation-derived runtime starts at confidence 0.35 (5 chapters of evidence) and rises as more chapters are written.

The confidence curve IS the evidence curve.

---

## Open Questions

1. **What is the minimum evidence threshold for proposing a candidate pattern?** Aisya's drum kit override had only 2 observations in 1 chapter. It was accepted as [E]-tagged. Was that premature?

2. **Can an author override the pipeline?** If the author is certain about an invariant that has not yet appeared in prose, can they manually add it? If so, what tag distinguishes "author-declared" from "observation-derived"?

3. **What happens when new prose contradicts an accepted invariant?** Does the invariant lose confidence? Does the prose trigger a review? Is this the mechanism by which character development becomes observable?

4. **Does the observe pipeline work for non-prose forms?** Screenplays, chat logs, RPG transcripts — does the same heuristic extraction work across formats?

5. **At what point does manual extraction become unsustainable?** Aisya: 5 chapters, manageable. GUA: 25 chapters, harder. Void Saga: 50+ chapters, impossible to manually re-extract every time. When does automation become necessary?

---

## Related

- `docs/OBSERVE_PIPELINE.md` — The pipeline specification. Phase 1–5: observe, propose, review, serialize, evolve.
- `docs/BEHAVIORAL_INVARIANTS.md` — Section 2.3: Observation Precedes Interpretation.
- `experiments/EXP-001-aisya/README.md` — The experiment that triggered this decision.
- [[2026-06-26-primitive-observation]] — The primitive decision. Why the unit of compilation is the invariant.
- [[2026-06-26-confidence-per-invariant]] — Confidence belongs to the invariant, not the entity. (Not yet written.)
