# Contra — Week One Teardown

> 2026-06-27. PM-lens adversarial review, requested by Jali. Deliberately one-sided *against* the project. This is the prosecution. Read it when the internal story feels too clean.

Based on direct reading of: `engine_v2.py` (399 LOC), `compiler.py` (824 LOC), `extract_scene.py` (809 LOC), `docs/BEHAVIORAL_INVARIANTS.md`, `docs/OPEN_QUESTIONS.md`, `experiments/EXP-001-aisya/README.md`, `experiments/EXP-002-gua-lo/README.md`, runtime JSONs, git log/status. Not from CLAUDE.md claims alone.

---

## Verdict

You built **two things that got swapped**, and the theory is eating the product.

There is one real, small, sharp, shippable product inside this repo. And there is a "research program" wrapping it in language much larger than its evidence. The kernel is genuinely good. The research framing has become a very comfortable place to hide.

"Jadi sesuatu" reframed: the thing most likely to *jadi sesuatu* — outlive your own head, get used by someone else, or get the novel finished and read — is **not** the research program. It is the writer tool buried inside it, plus the finished novel you haven't admitted is finished.

---

## What is genuinely strong (do not dismiss when reading the rest)

The theory is coherent and — rare — falsifiable in principle. `BEHAVIORAL_INVARIANTS.md` is clear writing. Four real assets:

1. **PRICE REQUIRED as a fourth verdict.** Not decoration — a product insight. "The compiler does not lock behavior, it locks expectation; the strength of an invariant *is* the narrative weight of breaking it." Sellable to any novelist in one sentence. Batman/Mr. Bean make it instantly legible to a layperson. It is demo-able.
2. **"Observation precedes interpretation" + the anti-MBTI stance.** An honest intellectual differentiator. A real defense against "this is just a character sheet."
3. **The pipeline actually runs end-to-end.** Engine, compiler, a hard-block gate that blocks *before* the API call, post-generation validation. PASS and BLOCKED demos have evidence. Not vaporware. Most GitHub "frameworks" never get this far.
4. **The discipline of "nothing enters theory without evidence."** Holding GUA/LO uncommitted because theory hasn't settled is rare rigor.

None of the below erases these. They are why the project is worth being brutal with.

---

## Blind spots (the brutal part)

### 1. The "extractor" does not extract invariants

The biggest one. `extract_scene.py` (809 LOC) is regex for name detection, Indonesian dialogue tags, POV, and setting → it builds a scenario JSON. That's it. The thing that actually produces invariants from prose — the core of the entire theory — is **read manually and formulated by hand** (by Jali, or by Claude reading the prose). Every experiment README admits this ("Manual extraction. Not automated").

So the claim "the compiler is an emergence detection engine" is, right now, a technical falsehood. The emergence detector is *a human (or Claude) reading a novel.* The engine only checks consistency against hand-written invariants. The theory↔implementation gap is enormous, and no document states it this plainly.

### 2. The confidence numbers are degenerate

The formula is `evidence / (evidence + violations)`. Violations are ~always 0 because the prose is written by one consistent author who never violates their own characters. So confidence is just a monotonic function of chapter count. Therefore "confidence scales with chapters" is a **tautology, not a finding.** 0.35 vs 0.45 "in the predicted direction" — those are two **hand-assigned** numbers, then declared consistent with the prediction. That is not evidence. It is confirmation bias wearing a quantitative costume.

### 3. N=1 author, N=2 universes, both yours

The entire "research program" is one person + Claude. Claude proposes the invariants, Claude validates them, Claude assigns confidence, Claude writes the experiment records. Zero inter-rater reliability. EXP-001 admits it: "Single reader (Claude session)." Fully circular.

The KPI has shifted four times — "can the compiler run → can someone else run it → does it change what a writer decides → does the mechanism reproduce across universes" — and **not one shift involved a second human.** The adoption track is "paused." The goalposts keep moving toward versions that need *less* external validation, not more.

### 4. OPEN_QUESTIONS is architecture astronautics

Five questions, all "should the schema be X / should Contract be first-class / should the root abstraction be SerializableArtifact." These are design questions that **cannot be answered without external data that is not being gathered.** "No schema changes until questions answered" + "questions answerable only by external data we aren't collecting" = a stall disguised as discipline. The research structure manufactures a respectable reason not to move.

### 5. You are running GUA's own invariant

Stated plainly: GUA invariant #2, which you extracted yourself, is *"Builds systems/protocols to contain what can't be said directly."* The pivot from "I'm writing a novel" → "I'm running the Executable Fiction Research Program" **is exactly that behavior.**

The novel — 87KB+ of prose — is done. The unfinished thing is not the novel. The unfinished thing is the *decision* about whether this is a novel or software. Building a compiler is a very sophisticated way to avoid saying "I wrote a novel and I want people to read it." (Mirror function, per Claude's role in this project.)

### 6. The market does not exist — or does not yet

"Executable fiction" as a category has ~zero existing demand. Nearest comparables: World Anvil, Campfire, Sudowrite, character-bible tools. None use compiler/invariant framing. That is either a moat (novel framing) or a signal that nobody wants it. You have never tested which, because there has never been a second user.

---

## Roadmap (PM lens: kill / sharpen / keep)

Assumed goal: not a VC-scale startup, but "jadi sesuatu" = outlives your head, gets used by someone else, or helps the novel get finished and read.

**Phase 0 — Decide the product (1 week, zero code).** Answer the question you keep avoiding: is this a *novel*, a *writer tool*, or a *paper*? It cannot be all three. Recommendation: **writer tool**, with the novel as dataset/demo and the theory as marketing.

**Phase 1 — Kill the research framing, ship the kernel.** One concrete product: a *consistency linter for fiction writers.* Feed it prose; it flags "this character usually does X, here they did Y," cites the chapter where the pattern formed, and returns a PRICE REQUIRED verdict with its weight. ~80% already exists in the engine. Missing: automated extraction (Phase 2) and a UI a non-technical writer can use. This is what has a market. PRICE REQUIRED is the hook.

**Phase 2 — Kill the manual extractor.** Replace the regex extractor with LLM-based extraction that genuinely proposes candidate invariants + citations from raw prose. Until this works, **do not** say "emergence detection engine" anywhere — it is currently a false claim. Highest-leverage technical task: it's what turns "human invents rules, engine checks" into an actual system.

**Phase 3 — External validation, or admit this is a practice not a methodology.** One brutal test: hand the pipeline to **one other writer** (not you, not Claude alone). Someone at KPG, someone on siapabilang. See whether (a) the extraction makes sense to them, (b) the verdict is useful. If there is no second author within 90 days, delete the words "research program" and "methodology" from the repo and call it "a writing instrument I built for my own novel." That is honest and still impressive. Methodology requires N>1. You have N=1.

**Phase 4 — Fix confidence or drop it.** While violations≈0, the confidence number is theater. Either (a) introduce *held-out validation*: hold back some chapters, extract from the rest, see if the invariants predict the held-out chapters — that is real confidence — or (b) drop the number and use raw evidence count + a maturity label. Do not publish a number that only means "I wrote a lot of chapters."

**KEEP as-is:** the novel (strongest, clearest asset — finish and publish it; KPG is a real channel), PRICE REQUIRED, the Batman/Mr. Bean framing, the evidence discipline.

**STOP:** schema v3 debate, serializing the remaining Void Saga characters, all OPEN_QUESTIONS about architecture — premature until Phase 2–3 land.

---

## One sentence

You don't have a theory problem — the theory is good. You have a *category* problem: you're calling "research program" something that is actually "a writer tool with no users yet + a novel you won't admit is finished," and the research structure gives you an honorable reason to face neither.

---

## Counter-counter (space for the defense)

> Left intentionally open. When you answer any point above, log the rebuttal here with date and evidence. A contra that survives rebuttal stays. A contra that gets answered becomes proof the project passed a real test. Do not delete — answer.

- [ ] #1 extractor — rebuttal:
- [ ] #2 confidence — rebuttal:
- [ ] #3 N=1 — rebuttal:
- [ ] #4 open questions — rebuttal:
- [ ] #5 GUA's invariant — rebuttal:
- [ ] #6 market — rebuttal:
