# Language Matching Bridge — ID/EN precision gap (Fase 2 note)

> 2026-06-27. Parked for Fase 2. Do not build before the novel ships (Fase 1).

## Observation (Jali)

Running the engine repeatedly, results on **Indonesian prose are less precise than on English prose.** Jali writes the logic, code, and invariant definitions in English; the prose (Void Saga) in Indonesian. The engine kept reporting Indonesian as weaker. Cause of confusion.

## Diagnosis (grounded in `apps/engine/lib/constraints.py`)

It is **not** "Indonesian is a worse language for the engine." It is a monolingual matcher. Three English biases, read from the code:

1. **Trigger parser is hard-coded to English syntax.** `extract_trigger_conditions` splits on `or`, `after`, `in response to` and strips English stopwords (`the/a/is/are/has`). Indonesian connectives (`atau`, `setelah`, `ketika`, `sebagai respons`) match none → the trigger text isn't segmented → falls back to whole-string matching (constraints.py:39–40).
2. **Matching is bare token overlap, no stemming.** `cond_words = set(condition.split())`. Indonesian is agglutinative — one root ("tatap") surfaces as *menatap, menatapnya, ditatap, tatapan, tertatap* → different tokens → no match. English morphology is shallow → tokens coincide more often.
3. **Invariants are authored in English.** When prose is English, prose tokens share the invariant's language → "looks better." When prose is Indonesian, the engine is matching **across a language boundary** with a matcher that doesn't know it.

**Reframe:** the metric is measuring *same-language vs cross-language matching* + *no morphological normalization* — not language quality. The engine isn't saying Indonesian is worse; it's saying the matcher is monolingual. Implementation artifact, not a property of the language or the writing.

## Bridge — two tiers

**Cheap (closes much, ~days):**
- Add Indonesian delimiters + stopwords to the trigger parser.
- Add **Sastrawi** (standard ID stemmer, pip, pure-python) to normalize *both* sides — prose tokens AND invariant keywords — to roots before overlap. *menatap→tatap*, *melindungi→lindung*. Add an English stemmer (nltk Snowball) for symmetry.
- Decide invariant trigger language: author ID trigger lexicons, or keep EN + per-invariant ID synonym map.

**Real (dissolves the problem — this IS Fase 2 / kills contra #1):**
- Replace token-overlap with **multilingual sentence embeddings** (LaBSE / multilingual-e5 / paraphrase-multilingual-MiniLM). Embed the invariant phrase and each scene sentence; match by cosine similarity in a shared multilingual space. "melindungi sebelum diminta" matches the English invariant "protects before being asked" by **meaning**, not string. Language becomes irrelevant — which is exactly the theory (observation precedes interpretation; meaning, not surface).

## Why this is also a clean experiment (EXP-003 candidate)

Falsifiable test, fits the evidence discipline:
- If multilingual semantic matching **closes** the ID/EN gap → strong evidence the invariants are genuinely language-agnostic *meaning* patterns (supports the theory).
- If it **does not** close → the invariants were secretly English-surface artifacts. Critical finding about the theory.

Either outcome is worth more than guessing. Run it; don't assume.

## Grounding caveat

This is Fase 2. Tempting because it "cures" the confusion, but the roadmap says finish the novel first. The only bounded thing that de-confuses now without derailing: a **quarter-day Sastrawi spike** — does stemming alone close part of the gap? Measure before/after on one runtime against ID prose. Everything beyond that waits for Fase 2.

## Related
- `contra/2026-06-27-contra-week-one.md` #1 (manual/keyword extractor) — this gap is a symptom of it.
- `docs/OPEN_QUESTIONS.md` #3 (does the compiler compile stories or evidence / is it medium-agnostic) — language-agnosticism is the same question one level down.
