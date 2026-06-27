# research/ — Lab Notebook

> This folder records **why the theory changed**, not the final theory itself.

---

## What This Is

`research/` is a decision log. It preserves the reasoning that led to theory changes in Executable Fiction — context, debate, alternatives considered, and why a specific direction was chosen.

Each file captures one moment where the project's understanding shifted.

## What This Is NOT

| If you want… | Go to… |
|--------------|--------|
| The current theory | `docs/BEHAVIORAL_INVARIANTS.md` |
| Experimental evidence | `experiments/` |
| Raw prose data | `writing/` |
| Research methodology | `docs/OBSERVE_PIPELINE.md` |
| Open research questions | `docs/OPEN_QUESTIONS.md` |
| Engine implementation | `VOID_SAGA_UNIVERSE/apps/` |

`research/` does not replace any of these. It complements them — it records the **reasoning path** that connects data → theory → methodology.

## Folder Distinction

```
docs/           →  Stable theory. "What we believe."
experiments/    →  Evidence and results. "What we tested."
writing/        →  Raw dataset. "What we observed."
research/       →  Reasoning path. "Why we changed our mind."
VOID_SAGA_UNIVERSE/  →  Engine. "What we built."
```

## Why This Exists

The most important discoveries in this project — the primitive is repeated observation, runtime must be discovered not declared, confidence belongs to the invariant — emerged from **discussion, not code.**

Code commits capture what changed. Chat history captures what was said. Neither captures **why a decision was made** in a form that can be revisited six months later.

This folder is the answer to: "Why did we decide that?"

## Format

Each decision log follows a consistent structure:

1. **Context** — What was happening in the project at the time?
2. **Before** — What did we believe before this decision?
3. **Trigger** — What specific observation or discussion forced the rethinking?
4. **Decision** — What did we decide? (One sentence, bold.)
5. **Reasoning** — Why this direction over the alternatives?
6. **Implications** — What follows from this decision?
7. **Open Questions** — What does this decision NOT resolve?

## Conventions

- **Write close to the moment.** A decision log written two weeks later is a reconstruction, not a record.
- **Provisional is fine.** A decision log may end with more questions than answers. That is the point.
- **No polish required.** This is a lab notebook, not a publication. Honesty > elegance.
- **File naming:** `YYYY-MM-DD-short-slug.md`. The date is when the decision crystallized, not when the file was created.
- **Link freely.** Reference related decision logs, docs, and experiments using relative paths.

---

*Created 2026-06-27. The first two entries capture decisions from 2026-06-26 — written the following morning, while the reasoning was still fresh.*
