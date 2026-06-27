# Fork Interview Runtime — Design Discovery

> 2026-06-28. Research note. Not a specification. Not architecture.
>
> This document records what we learned during dogfooding of the Bab 00 Fork MVP (`mvp/`). It distinguishes observations from interpretations, hypotheses from established facts, and marks open questions explicitly.
>
> **Status:** Design discovery. Leading hypothesis only. Requires further validation.
>
> **Principle:** Observation precedes interpretation. Evidence before claims.

---

## 1. Discovery Summary

### What happened

The Bab 00 Fork MVP (`mvp/`) is complete. Genesis node, fork points, 7 laws, 4 fork examples, rule-based CLI checker — all working. `./scripts/check-fork mvp/forks/fork-01-pass.json` returns 🟢 PASS. The pipeline is end-to-end.

During dogfooding — attempting to use the MVP as a writer would — something unexpected surfaced.

**The user never naturally thought in terms of Fork Record, JSON, metadata, or structured fields.**

Instead, the user's first thought was:

> *"Gimana kalau GUA gak peduli waktu LO datang?"*

This was followed by a natural conversational sequence:

- *"Apa yang berubah?"*
- *"Berapa lama?"*
- *"Apakah akhirnya berubah pikiran?"*
- *"Apa akibat langsungnya?"*

Only **after** this conversation did enough structure exist to imagine a Fork Record.

The MVP currently starts at: Fork Record → Law Checker → Verdict.

The writer's mental model starts at: Story → What if? → Conversation → Understanding.

**The Fork Record appears to be an implementation artifact — an internal representation (IR) — not the writer's mental model.**

### What this discovery is NOT

- NOT a bug in the MVP. The checker works correctly. The laws evaluate correctly. The verdicts are sound.
- NOT a rejection of the Fork Record schema. The schema is necessary — it is what the checker consumes.
- NOT a claim that the MVP is "wrong." It is a claim that the MVP may be **missing a layer above it.**

---

## 2. What We Observed

### Raw observations (directly witnessed)

| # | Observation |
|---|-------------|
| O1 | User's first utterance was a natural-language "What if..." question in Indonesian. |
| O2 | User never referred to JSON, schema, `fork_point_id`, `touched_laws`, or any structured field. |
| O3 | User answered conversational follow-up questions naturally and without hesitation. |
| O4 | User clarified intent ("gak peduli" → "mengabaikan"? "menolak"? "menunda"?) when asked. |
| O5 | User knew immediately what changed in the story but did not know which "law" was affected. |
| O6 | User could describe downstream consequences when prompted with "apa akibat langsungnya?" |
| O7 | Only after 6–8 conversational exchanges did enough structured information exist to fill a Fork Record. |
| O8 | Once the Fork Record was filled (by someone else, from the conversation notes), the checker evaluated it correctly. |
| O9 | User expressed the fork in terms of character behavior and story events, never in terms of `law_id` or `violation severity`. |

### Interpretations (inferences drawn from observations)

| # | Interpretation | Confidence |
|---|---------------|------------|
| I1 | The writer's mental model begins with **possibility** ("what if..."), not with **structure** (JSON fields). | High — consistent with O1, O2, O9 |
| I2 | The Fork Record, as currently designed, is an **implementation artifact** — it is what the checker needs, not what the writer thinks in. | High — consistent with O2, O7, O8 |
| I3 | A conversational layer that asks clarifying questions may bridge the gap between "what if..." and a structurally evaluable Fork Record. | Medium — single dogfooding session; N=1 |
| I4 | Writers may not need to know which laws exist in order to produce law-relevant forks — the conversation may surface law implications implicitly. | Medium — O5; needs testing across more fork points and writers |
| I5 | The current MVP UX (edit JSON → run checker) is natural for the engine but friction-heavy for writers. | High — O1, O2, O7 |

---

## 3. Why the Current UX Breaks (for Writers)

### Current flow

```
Fork Record (JSON, hand-edited)
        ↓
   Law Checker (rule-based)
        ↓
      Verdict
```

### Why this is natural for the engine

The engine needs structure. It needs to know: which laws are touched, what violations occurred, what the change is, what the downstream effects are. The Fork Record JSON provides exactly this. The checker's job is to evaluate structured claims against structured laws. This design is sound for the engine's responsibility.

### Why this is unnatural for writers

A writer encountering Bab 00 does not think:

> "I will now create a JSON object with fields `fork_id`, `touched_laws`, and `violations`."

A writer encountering Bab 00 thinks:

> *"Gimana kalau GUA gak peduli waktu LO datang?"*

The writer's first move is a **story possibility** — a counterfactual about character behavior. The writer does not know (and should not need to know):

- Which `fork_point_id` this maps to
- Which `law_id`s are affected
- Whether a violation is `low`, `medium`, `high`, or `critical` severity
- What `block_on_violate` vs `price_on_violate` means

The current UX requires the writer to perform **self-extraction** — to translate their own story intuition into structured legal claims before any tool can help them. This is asking the writer to do the checker's preprocessing.

**The Fork Record is an output of understanding, not an input to it.**

---

## 4. Candidate Mental Model

### Current hypothesis

The writer's natural flow may be:

```
  Story
    ↓
  What if...?
    ↓
  Conversation (clarifying questions)
    ↓
  Structured understanding
    ↓
  Fork Record         ← internal representation, not user-facing
    ↓
  Law Checker
    ↓
  Narrative Cost
    ↓
  Continue Writing
```

If this hypothesis holds, then:

- The Fork Record is an **IR (internal representation)** — it lives between the conversation layer and the checker, not between the writer and the tool.
- The writer should never need to see or edit JSON.
- The writer's interface is **questions and answers about the story.**
- The checker's interface is **structured Fork Records and law evaluations.**
- A new layer is needed to translate between these two interfaces.

### What this hypothesis does NOT claim

- Does NOT claim that JSON is "bad" or should be removed. The checker needs structured input.
- Does NOT claim that the current MVP is wrong. It works for its designed interface (Fork Record → Verdict).
- Does NOT claim that all writers think this way. N=1. This is a single dogfooding observation.
- Does NOT claim that conversational interface is the only answer. It is the current leading hypothesis.

---

## 5. Candidate Architecture — Fork Interview Runtime

### Current best hypothesis for the missing layer

A **Fork Interview Runtime** sits between the writer and the Fork Record.

Its responsibility is **not** to judge.

Its responsibility is to **help the writer think** until the fork becomes structurally evaluable.

```
Writer: "Gimana kalau GUA gak peduli waktu LO datang?"
                ↓
┌─────────────────────────────────────────────┐
│         FORK INTERVIEW RUNTIME              │
│                                             │
│  Job: Ask clarifying questions until the    │
│  fork is structurally evaluable.            │
│                                             │
│  Does NOT:                                  │
│  - Judge the fork                           │
│  - Evaluate laws (that's the checker)       │
│  - Generate story (that's the writer)       │
│  - Require JSON knowledge from writer       │
│                                             │
│  Produces: Fork Record (JSON, for checker)  │
│  Interface: Conversational questions (text) │
└─────────────────────────────────────────────┘
                ↓
          Fork Record (JSON)
                ↓
          Law Checker
                ↓
            Verdict
```

The Fork Interview Runtime translates between two worlds:

| Writer's world | Runtime's world → | Checker's world |
|---------------|-------------------|-----------------|
| "What if..." questions | → clarifying questions → | Fork Record JSON |
| Character behavior | → mapped to → | `touched_laws` |
| Story consequences | → structured as → | `downstream_effects` |
| "Berapa lama?" | → determines → | divergence permanence |
| "Apa yang tetap sama?" | → identifies → | untouchved laws / canon gravity |

### Status of this architecture

**This is a hypothesis, not a confirmed architecture.** It emerged from one dogfooding session (N=1 writer, N=1 fork point, N=1 universe). It has not been tested with:

- A different writer
- A different fork point (fp-002, fp-003)
- A different chapter (beyond Bab 00)
- A fork that the writer themselves cannot initially articulate

Do not build this yet. Validate the hypothesis first.

---

## 6. Principles

If the Fork Interview Runtime hypothesis survives further dogfooding, these principles would guide its design:

1. **Writers think in possibilities. Engines think in structure.** The runtime translates between them. Neither should be forced to think like the other.

2. **Questions come before verdicts.** The runtime's primary output is understanding, not classification. A verdict on incomplete understanding is noise.

3. **Verdicts emerge from completed understanding, not incomplete input.** The checker should receive a structurally complete Fork Record — not a half-formed intuition.

4. **The engine should help writers discover consequences rather than immediately classify ideas.** "What would happen if..." is more valuable than "VALID_FORK" as a first response.

5. **The writer never needs to know which laws exist.** The runtime asks about story changes; the runtime (or a later compiler) maps story changes to laws. The writer thinks in characters and events.

6. **Conversation is the interface. Structure is the output.** The writer speaks naturally. The runtime produces structured artifacts for the engine.

7. **The runtime is not an AI storyteller.** It does not generate prose. It does not suggest plot. It asks questions. The writer writes.

---

## 7. Example Conversation (Indonesian, from dogfooding)

The following approximates the actual dogfooding interaction. Indonesian is the writer's natural language.

---

**Writer:**
> Gimana kalau GUA gak peduli waktu LO datang?

**Runtime:**
> "Gak peduli" bisa berarti beberapa hal. Apakah GUA:
> - Mengabaikan LO sepenuhnya (tidak merespons)?
> - Menolak LO secara aktif ("Gua bisa sendiri")?
> - Atau hanya menunda — ragu sebentar, tapi akhirnya memberi ruang?

**Writer:**
> Bukan menolak. GUA cuma... gak notice. Kayak, dia terlalu fokus sama bug-nya sendiri. LO berdiri di samping, tapi GUA gak nengok.

**Runtime:**
> Jadi GUA tidak sadar LO ada di sana. Berapa lama sampai GUA akhirnya notice?

**Writer:**
> Mungkin... lima menit? LO akhirnya ketuk meja pelan. Bukan buat ngagetin. Cuma buat kasih tahu dia di situ.

**Runtime:**
> Setelah GUA notice, apakah GUA memberi ruang seperti di kanon — geser kursi, biarin LO duduk?

**Writer:**
> Iya. Setelah notice, GUA kasih ruang. Tapi lima menit pertama itu... beda. LO harus usaha buat di-notice.

**Runtime:**
> Apa akibat langsung dari lima menit itu?

**Writer:**
> LO jadi sedikit ragu. Bukan marah. Tapi kayak... "Oh, gua harus ketuk meja dulu." Ada jarak kecil yang sebelumnya gak ada. Sinkronisasi tetap terjadi, tapi LO harus memulai dengan isyarat fisik — bukan cuma berdiri.

**Runtime:**
> Apa yang tetap sama dengan kanon?

**Writer:**
> Bug tetap diperbaiki bareng. genesis.txt tetap lahir. Stealth Project tetap jalan. Cuma... ada jeda kecil di mana GUA hampir kehilangan sesuatu karena terlalu fokus.

**Runtime:**
> Sudah cukup untuk evaluasi. Fork Record bisa dibentuk. Ringkasan: GUA tidak menyadari kehadiran LO selama 5 menit di 00:03. LO harus mengetuk meja untuk mendapat perhatian. Sinkronisasi tetap terjadi, tapi LO harus memulai kontak fisik — menambahkan jarak kecil yang sebelumnya tidak ada. Tidak ada hukum yang dilanggar, tapi dinamika initiation sedikit bergeser.

**→ Fork Record dihasilkan. Checker dipanggil. Verdict: VALID_FORK.**

---

### What this example shows

1. The writer never used the word "law," "violation," "severity," or "JSON."
2. The writer answered 6 clarifying questions naturally.
3. The conversation produced enough structure to fill all required Fork Record fields.
4. The Fork Record was a **byproduct** of the conversation, not the starting point.
5. The runtime did not judge. It asked questions until the picture was clear.

---

## 8. Candidate Runtime State Machine

**Exploratory only. Not implementation guidance.**

This is a conceptual sketch of what states a Fork Interview Runtime might move through. It is not a specification. It may be wrong. It is written here to make the hypothesis concrete enough to test.

```
  START
    ↓
  SELECT FORK POINT
  (Where in Bab 00 does this branch?)
    ↓
  DESCRIBE WHAT CHANGED
  (Open-ended: "What if...?")
    ↓
  CLARIFY INTENT
  (Disambiguate: reject vs ignore vs delay?)
    ↓
  CLARIFY DURATION
  (How long does the change last? Permanent? Temporary?)
    ↓
  CLARIFY PERMANENCE
  (Does the character return to canon behavior? When?)
    ↓
  IMMEDIATE CONSEQUENCES
  (What happens right after the change?)
    ↓
  WHAT STAYED THE SAME
  (Canon gravity — which facts are untouched?)
    ↓
  READY FOR EVALUATION
  (Enough structure exists to build Fork Record)
    ↓
  FORK RECORD (generated, not hand-edited)
    ↓
  LAW CHECKER
    ↓
  VERDICT + NARRATIVE COST
```

### Notes on this state machine

- States 2–7 may loop. A writer might clarify intent, then realize duration matters differently, and return.
- Not all forks need all states. A tiny fork ("GUA hesitates 5 seconds") might skip CLARIFY PERMANENCE.
- The state machine is **question-driven**, not data-driven. Each state corresponds to a class of clarifying question.
- This is the **maximum** path. The minimum path might be: SELECT → DESCRIBE → CONSEQUENCES → READY.
- The state machine is a hypothesis about **conversation structure**, not about code.

---

## 9. Roadmap (Exploratory Sprints)

Each sprint is designed to **learn something**, not to build production software. Each sprint includes:
- **What we are trying to learn**
- **What evidence would support the hypothesis**
- **What would falsify it**

### Sprint 1 — Static Interview Flow

**Goal:** Test whether a fixed sequence of questions can reliably produce a valid Fork Record.

**Method:**
- Hardcode the state machine above as a static question sequence.
- No adaptivity. Same questions for every fork.
- Run 5 forks (different fork points, different writers if possible) through the static interview.
- Measure: does the output Fork Record pass the checker? Does the writer feel the questions were relevant?

**Learning target:** Is a static question flow sufficient, or is adaptivity required?

**Supports hypothesis if:** ≥4/5 forks produce valid Fork Records that survive checker evaluation.

**Falsifies hypothesis if:** Static questions consistently miss important fork dimensions, producing incomplete or irrelevant Fork Records.

---

### Sprint 2 — Adaptive Questions

**Goal:** Test whether question branching (different questions based on earlier answers) improves interview quality.

**Method:**
- Add basic branching: if writer says "menolak," ask about permanence. If "menunda," ask about duration.
- Compare against Sprint 1 results: fewer irrelevant questions? More complete Fork Records?
- Same 5-fork benchmark.

**Learning target:** Does adaptivity reduce friction compared to static flow?

**Supports hypothesis if:** Writers report fewer "this question doesn't apply" moments. Fork Records are more complete.

**Falsifies hypothesis if:** Adaptivity adds complexity without measurable improvement in Fork Record quality.

---

### Sprint 3 — Law-Aware Interview

**Goal:** Test whether the runtime should know which laws exist during the interview.

**Method:**
- Give the runtime access to Bab 00 law definitions.
- After the writer describes the change, the runtime internally checks: "Which laws might this touch?"
- The runtime asks targeted follow-ups for potentially-affected laws.
- Example: if the change involves GUA-LO interaction, ask questions relevant to law-002 and law-006.

**Learning target:** Does law awareness help the runtime ask better questions, or does it bias the interview toward legal framing too early?

**Supports hypothesis if:** Law-aware questions surface relevant dimensions the writer hadn't considered, without making the writer think in "law" terms.

**Falsifies hypothesis if:** Law awareness causes the runtime to steer the writer toward particular verdicts, or makes the conversation feel like a legal deposition rather than a story discussion.

---

### Sprint 4 — Conversation Memory + Contradiction Detection

**Goal:** Test whether the runtime should remember earlier answers and flag contradictions.

**Method:**
- Store all writer answers during the session.
- Before finalizing the Fork Record, check: does any answer contradict an earlier answer?
- Example: writer says "GUA tidak notice LO" early, but later says "GUA lihat LO dari sudut mata." Flag the contradiction and ask for clarification.

**Learning target:** Do writers contradict themselves during fork interviews? Does flagging improve Fork Record quality?

**Supports hypothesis if:** Contradictions are detected and resolved before the Fork Record is built, preventing incoherent records.

**Falsifies hypothesis if:** Contradictions are rare (the interview naturally prevents them) or flagging them feels punitive rather than helpful.

---

### Sprint 5 — Natural Language → Fork Record Compiler

**Goal:** Test whether a conversation transcript can be compiled into a Fork Record without manual structuring.

**Method:**
- Take 10 completed interviews (writer + runtime Q&A transcripts).
- Build a compiler that extracts: fork_point, change description, touched laws (via keyword/pattern matching on answers), downstream effects, canon gravity statements.
- Compare compiler output against hand-structured Fork Records from the same conversations.

**Learning target:** Can structured Fork Records be reliably compiled from natural-language Q&A?

**Supports hypothesis if:** ≥80% of compiler-generated Fork Records match hand-structured ones on key fields (touched_laws, violations, verdict alignment).

**Falsifies hypothesis if:** Compilation requires human judgment for core fields, suggesting the conversation itself is not sufficient structure.

---

### Important

These sprints are **exploratory**, not a commitment. Sprint 1 is the only one that should be attempted immediately. Sprints 2–5 depend on what Sprint 1 teaches us. The roadmap may be wrong. The hypothesis may be wrong. The goal is to find out quickly and cheaply.

---

## 10. Open Questions

These are **unresolved.** Do not answer them prematurely. They are recorded here so that future dogfooding sessions can gather evidence toward resolution.

### Interview scope

1. **Does every fork require an interview?** Or can tiny forks (e.g., "GUA hesitates 2 seconds") bypass the interview and go directly to Fork Record?
2. **Can a fork be created mid-interview?** If the writer answers 3 questions and says "actually, bukan ini yang gua maksud," does the interview restart or branch?
3. **Is the interview reusable?** If the writer forks the same fork point twice with different changes, does the second interview benefit from the first?

### Question design

4. **Which questions are universal across all fork points?** "Apa yang berubah?" may be universal. "Apakah VoidOS tetap muncul lewat undangan?" may only apply to fp-003.
5. **Which questions depend on the selected fork point?** Should the runtime load fork-point-specific questions from `fork-points.json`?
6. **Should laws influence questions before, during, or after the interview?** Three competing hypotheses:
   - **Before:** Law-aware questions from the start (Sprint 3).
   - **During:** Laws are consulted only when the writer's answers suggest a law might be relevant.
   - **After:** The interview is law-agnostic. Laws are only checked when the Fork Record is complete.

### Completion

7. **When is a Fork Record "complete enough" for evaluation?** What is the minimum set of fields that must be populated before the checker should run?
8. **Can the runtime detect incompleteness?** If the writer says "GUA berubah" but cannot describe consequences, should the runtime refuse to produce a Fork Record?

### Writer experience

9. **Does the interview feel like help or friction?** The current JSON-editing UX is friction. But a long interview might also be friction of a different kind.
10. **How many questions is too many?** Is there a point where the writer abandons the fork because the interview is exhausting?
11. **Should the runtime explain WHY it's asking each question?** Or should questions feel natural and un-explained?

### Generalization

12. **Does this interview model generalize beyond Bab 00?** If laws are chapter-specific, does the interview need to be chapter-specific too?
13. **Does this model generalize beyond Void Saga?** A different universe with different laws — does the interview structure remain valid?

---

## 11. Non-Goals

This document is **NOT** proposing:

- ❌ Embeddings or vector search
- ❌ AI story generation or prose writing
- ❌ Blockchain, tokens, or marketplace
- ❌ Expansion beyond Bab 00 (yet)
- ❌ Replacing the current checker (`check_fork.py`)
- ❌ Replacing the current Fork Record schema
- ❌ A web application or production UI
- ❌ Natural language understanding via LLM (Sprint 5 compilation is pattern-based, not semantic)
- ❌ Multilingual architecture beyond the existing v0.2 bridge

**The discovery concerns interaction design, not intelligence.**

The current checker is correct. The current Fork Record schema is necessary. The current laws are well-formed. The only thing being questioned is: **what should happen BEFORE the Fork Record exists?**

---

## 12. Success Metrics

If a Fork Interview Runtime is eventually built, it is successful when:

| # | Metric | Measured by |
|---|--------|-------------|
| M1 | Writers never need to edit JSON. | Zero JSON-editing steps in the writer's workflow. |
| M2 | Writers naturally answer story questions. | Interview completion rate ≥80% (writer reaches READY state). |
| M3 | The runtime produces a valid Fork Record. | Generated Fork Record passes `check_fork.py` without manual correction. |
| M4 | The existing checker can evaluate that record. | Zero changes required to `check_fork.py` to accept runtime-generated records. |
| M5 | Writers feel they are discussing story possibilities rather than filling forms. | Post-interview survey: "I felt like I was exploring my story" > "I felt like I was filling out paperwork." |

These metrics are **aspirational.** They have not been validated. They may be wrong. They are recorded here so that future implementation has a target to measure against.

---

## Status

**This is a design discovery document, not a decision log.**

Nothing in this document has been promoted to theory. Nothing has been implemented. The Fork Interview Runtime is a leading hypothesis from a single dogfooding session (N=1 writer, N=1 fork point).

Next step: validate the hypothesis with additional dogfooding across different fork points and, ideally, a different writer. Sprint 1 (static interview flow) is the lowest-cost validation.

If the hypothesis is falsified — if writers prefer direct Fork Record editing, or if interviews consistently fail to produce evaluable records — this document becomes a record of a hypothesis that was tested and rejected. That is still valuable.

---

## Addendum (same day, post-discussion)

> The following hypotheses emerged from discussion of the original discovery document above. They extend — and in some cases reframe — the Fork Interview Runtime hypothesis. They are recorded here as **new hypotheses**, not conclusions. N=1. Single dogfooding session. Single discussion.

### A. Deeper Observation — When Writers Come to the Runtime

Two additional observations surfaced during discussion:

| # | Observation |
|---|-------------|
| O10 | The writer initiated the dogfooding session from a state of not writing. The flow was not currently moving. |
| O11 | The writer would not have initiated a "fork interview" while already writing fluently. The trigger was blockage, not curiosity. |

From these, a reframing hypothesis:

> **H1: Writers primarily interact with the runtime when they are blocked, not while they are already writing fluently.**

If H1 holds, the product category may be fundamentally misidentified.

### B. Product Category Shift

| We assumed | It may actually be |
|------------|-------------------|
| Writing Assistant | **Writing Unblocker** |
| Tool for creating forks | **Narrative Catalyst** |
| Fork Record generator | **Story Opener** |

This is not a feature distinction. It is a **category distinction.**

A Writing Assistant helps someone who is already writing. A Writing Unblocker helps someone who has stopped. The user arrives in a different state. The first job is different. The success metric is different.

If H1 is correct, the runtime's primary user is not "a writer managing branches of their canon." The primary user is **"a writer who is stuck."**

### C. KPI Shift — The First Question

If the writer arrives blocked, then the KPI of the runtime changes fundamentally.

| Current assumed KPI | Possible actual KPI |
|---------------------|---------------------|
| Produces a valid Fork Record | **After one question, does the writer start imagining story again?** |
| Correctly classifies the fork (PASS/BLOCKED/etc.) | **Did the conversation restart narrative thinking?** |
| Verdict accuracy | **Narrative flow restoration** |

The Fork Record and verdict are still outputs. But they may be **secondary outputs.** The primary output may be: the writer is no longer stuck.

This implies a metric that is not currently measured anywhere in the MVP:

> **Time-to-imagination:** How many conversational turns from "gua mentok" to the writer producing new story ideas unprompted?

### D. Opening Questions vs. Closing Questions

During the dogfooding discussion, a specific moment revealed something about question design.

The user was clarifying GUA's response to LO's approach. Three framings were offered:

- *"Mengabaikan?"* (ignoring)
- *"Menolak?"* (rejecting)
- *"Tidak sadar?"* (not noticing)

The response was: *"Membuka."* — because the third option opened new story possibilities. Not because it was most correct. Because it was most **generative.**

This produced a taxonomy hypothesis:

#### Closing questions

Questions that ask the writer to **choose** between existing options:

- *"Apakah A atau B?"*
- *"Apakah GUA menolak atau menerima?"*

These tend to narrow. The writer picks one. The thinking stops.

#### Opening questions

Questions that ask the writer to **explore** what is at stake:

- *"Apa yang sebenarnya dipertaruhkan di sini?"*
- *"Kalau keputusan ini berubah, apa yang ikut berubah?"*
- *"Apa yang sebenarnya sedang dihindari karakter?"*
- *"Apa yang LO rasakan yang GUA tidak lihat?"*

These tend to expand. The writer discovers something. The thinking continues.

> **H2: The quality of a question is not measured by how precisely it narrows the answer space, but by whether it opens new imaginative territory.**

This is counterintuitive for an engine design. Engines want deterministic inputs. But the writer who is blocked does not need determinism — they need **movement.**

### E. Two Modes, Not One

If H1 and H2 hold, the Fork Interview Runtime may need two distinct modes, not one continuous interview flow.

#### Mode 1 — Opening Mode

**Goal:** Restart narrative thinking.

**Characteristics:**
- Does not mention laws, JSON, or verdicts.
- Does not ask the writer to choose between options.
- Asks opening questions: stakes, consequences, what's being avoided, what's at risk.
- Success metric: writer begins generating ideas unprompted.
- Exit condition: writer is no longer stuck.

#### Mode 2 — Structuring Mode

**Goal:** Produce a structurally evaluable Fork Record.

**Characteristics:**
- Activated only after ideas are flowing.
- Asks structuring questions: who, when, permanent, consequences, what stayed the same.
- Maps story answers to `touched_laws`, `violations`, `downstream_effects`.
- Success metric: valid Fork Record that passes the checker.
- Exit condition: Fork Record is complete enough for evaluation.

**Mode transition is not automated.** The runtime should detect (or the writer should signal) when thinking has restarted. The transition from Mode 1 to Mode 2 is itself a design question — premature structuring kills exploration; never structuring leaves the writer without a verdict.

### F. Revised Architecture

```
Writer is blocked
        ↓
┌──────────────────────────────┐
│   MODE 1: OPENING MODE       │
│                              │
│   Job: Restart thinking.     │
│   Asks: Opening questions.   │
│   Metric: Writer imagines    │
│           story again.       │
│   Exit:  Ideas are moving.   │
└──────────────────────────────┘
        ↓
  Ideas begin moving
        ↓
┌──────────────────────────────┐
│   MODE 2: STRUCTURING MODE   │
│                              │
│   Job: Build Fork Record.    │
│   Asks: Who, when, permanent,│
│          consequences.       │
│   Metric: Valid Fork Record. │
│   Exit:  Ready for checker.  │
└──────────────────────────────┘
        ↓
    Fork Record
        ↓
    Law Checker
        ↓
      Verdict
```

This architecture is a **hypothesis about user state**, not a hypothesis about code structure. The two modes exist because the writer arrives in two different states — blocked and unblocked — not because the interview needs two phases.

### G. Revised Sprint 1

The original Sprint 1 proposed a static interview state machine. The discussion above suggests a different starting point:

**Sprint 1 (revised): Question Design, Not Flow Design**

**Goal:** Discover which questions restart narrative thinking.

**Method:**
- Prepare a set of opening questions (5–10 candidates).
- Test each against a writer who is currently stuck on a Bab 00 fork.
- Measure: after this question, does the writer start talking about story unprompted?
- Classify each question as: **opened** (writer generated new ideas) or **closed** (writer picked an option and stopped).

**Learning target:** Can we build a taxonomy of opening vs. closing questions? Are there repeatable patterns?

**Supports hypothesis if:** Some questions consistently open thinking across multiple stuck moments. A pattern emerges.

**Falsifies hypothesis if:** Question effectiveness is purely idiosyncratic (depends entirely on the specific writer and specific block). No pattern generalizes.

**This replaces the original Sprint 1 (Static Interview Flow).** The original Sprint 1 assumed the interview should produce a Fork Record. The revised Sprint 1 assumes the first problem is restarting thinking. Flow design comes after question design.

### H. What This Changes (If True)

| Dimension | Original hypothesis | Extended hypothesis |
|-----------|-------------------|---------------------|
| When writers come | Anytime they want to fork | **When they are blocked** |
| First job | Clarify the fork | **Restart narrative thinking** |
| First KPI | Fork Record produced | **Writer imagines story again** |
| Question quality | Precision of clarification | **Generativity — does it open space?** |
| Runtime structure | One interview flow | **Two modes: Opening → Structuring** |
| Product category | Writing Assistant | **Writing Unblocker / Narrative Catalyst** |
| Hardest problem | Mapping story to laws | **Designing the first question** |

### I. New Open Questions

Added to the original 13:

14. **How do we detect that a writer is blocked vs. just exploring?** Is this something the writer signals explicitly, or something the runtime must infer?
15. **Can a single well-designed opening question restart narrative thinking?** What is the minimum viable intervention?
16. **Is there a universal opening question?** Or does it depend on the writer, the chapter, the type of block?
17. **How does the runtime know when to transition from Mode 1 to Mode 2?** Does the writer say "okay, I'm ready to structure this"? Or does the runtime detect idea generation?
18. **Can Mode 1 and Mode 2 be the same runtime with different prompts?** Or do they require fundamentally different interaction designs?
19. **If the writer is not actually blocked — just curious — does Mode 1 still add value?** Or is it unnecessary friction for the non-blocked user?

### J. Status of This Addendum

These are **discussion hypotheses, not validated findings.** They emerged from analyzing a single dogfooding interaction and the conversation that followed. They have not been tested against:

- A different writer
- A different type of blockage
- A different fork point
- A different chapter
- A writer who is NOT blocked (curious exploration vs. stuck)

The original discovery document (Sections 1–12) stands as the first observation. This addendum (Sections A–J) is the second layer of interpretation. Both are provisional.

**Next action:** Test H1 first — "do writers primarily come to the runtime when blocked?" — by observing real writing sessions. If H1 is falsified, much of this addendum collapses. If H1 holds, the product category shift from Writing Assistant to Writing Unblocker becomes the central design question.

---

*Written 2026-06-28. Research note. Observation precedes interpretation. Evidence before claims. This addendum extends the original discovery document with hypotheses from post-dogfooding discussion. Nothing here is confirmed. Everything here is testable.*
