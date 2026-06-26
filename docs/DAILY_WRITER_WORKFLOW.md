# Daily Writer Workflow — Scene Triage

> The compiler is your first editor. It reads your ideas before you spend
> hours writing them.

---

## The Problem

You have an idea for a scene. You write 2000 words. Halfway through, you
realize: "This character wouldn't do this. This breaks canon. This scene
can't happen yet."

You delete 2000 words. You lost two hours.

---

## The Solution

Before you write prose, write a 10-line scenario JSON.
Run the compiler. It tells you whether this scene is ready to write.

```
Idea → Scenario JSON → Compiler → Decision → Writing
       (10 lines)      (2 seconds)  (informed)  (no waste)
```

---

## The Loop

### Step 1 — Morning: Write Scene Ideas

Create 3–5 scenario JSON files in `dogfood/`.

Each file is one scene idea. Give it a name you'll recognize in three months:

```json
{
  "scenario_id": "sevraya_visits_dayan_ruins",
  "participants": [
    {"runtime_id": "sevraya", "evolution_stage": 6},
    {"runtime_id": "zero", "evolution_stage": 6}
  ],
  "timeline_state": {
    "phase": 5,
    "pre_chain": false,
    "post_resolution": true
  },
  "proximity_state": {
    "pairs_in_range": [],
    "distance": "same_body"
  },
  "requested_action": {
    "description": "Sevraya stands at the edge of what was once Dayan. Zero surfaces. 'Radius 3km,' Zero says. 'No data remains.' Sevraya does not cry. She lights a cigarette. 'Good.'",
    "type": "speak"
  },
  "canon_mode": {
    "type": "canon_replication",
    "expected_verdict": "PASS"
  }
}
```

This took 2 minutes to write. Compare to 2 hours of prose.

### Step 2 — Triage

```bash
./scripts/triage-scenes dogfood
```

You get:

```
╔══════════════════════════════════════════════════════════════╗
║  SCENE TRIAGE  —  What is ready to write today?            ║
╚══════════════════════════════════════════════════════════════╝

SCENARIO                               VERDICT   SCORE  INTERPRETATION
────────────────────────────────────── ──────── ──────  ──────────────────────────
dayan_ruins                            🟢 PASS    1.0  ready to write
niuniu_dialog                          🔴 BLOCKED   0.97  Forbidden behavior: NiuNiu speaks fluently without external force
pre_chain_tension                      🟡 WARNING    1.0  low evidence confidence — verify canon basis

──────────────────────────────────────────────────────────────
  3 scenarios triaged  │  🟢 1 PASS  │  🟡 1 WARNING  │  🔴 1 BLOCKED
```

### Step 3 — Decide

| Verdict | What to do |
|---------|-----------|
| 🟢 PASS | **Write this today.** The compiler approved it. Open your editor. |
| 🟡 WARNING | **Review before writing.** Check the timeline state, proximity, or evidence confidence. Maybe the scene is fine with a small adjustment. Maybe it needs a setup scene first. |
| 🔴 BLOCKED | **Do NOT delete.** This is your most interesting idea. The compiler tells you exactly what must change. Save it as a long-term arc or create a fork. |

### Step 4 — Write

Open your editor. Write the PASS scenes. The compiler already checked
them against every active runtime constraint. You are not guessing —
you are executing.

### Step 5 — Archive

Move BLOCKED scenes to a `dogfood/future/` folder.
They are your outline. Each BLOCKED scene tells you:

> "This cannot happen yet. Here is what must happen first."

That list of prerequisites IS your next chapter.

---

## BLOCKED Is Not Rejection

A compiler that only says NO is a gate. A compiler that tells you
*what must change for this to become YES* is an editor.

When a scene is BLOCKED, the compiler tells you why. Read the reason.
It will say something like:

- "NiuNiu cannot speak fluently without external force"
- "Zero cannot express emotional warmth"
- "Orbital contract forbids touch between NiuNiu and Sevraya"

Each reason implies a path forward:

| Reason | Path forward |
|--------|-------------|
| "NiuNiu cannot speak" | Write the Living Chain arc first (Timer 2000). After that, speech is possible. |
| "Zero cannot be emotional" | Write Zero as administrative. Emotion is not Zero. Let Sevraya carry the feeling. |
| "Orbital contract forbids touch" | The distance IS the care. Write proximity without contact. |

The compiler does not block creativity. It channels creativity toward
what is canonically possible — which is often more interesting than
what is generically easy.

---

## Forking a BLOCKED Scene

Some BLOCKED scenes are not "not yet." They are "not in THIS timeline."

If you have a scene that should exist but cannot under current canon,
create a fork:

1. Copy the BLOCKED scenario to `dogfood/forks/`.
2. Write a short `fork.md` explaining what changed in this timeline.
3. The fork's premise is: "What if this one constraint were different?"

Forks are not betrayals of canon. They are evidence that the universe
is alive enough to generate alternate possibilities.

---

## Example: A Day in the Loop

**Morning (10 min):**

```bash
# 1. Write 3 scene ideas
vim dogfood/niuniu_mengamati.json
vim dogfood/sevraya_zero_berbicara.json
vim dogfood/julia_kembali_ke_dayan.json

# 2. Triage
./scripts/triage-scenes dogfood
```

**Output:**

```
🟢 niuniu_mengamati          — PASS, ready to write
🟡 sevraya_zero_berbicara    — WARNING, pre-chain timeline may not match stage
🔴 julia_kembali_ke_dayan    — BLOCKED, forbidden behavior triggered
```

**Decision (2 min):**

- `niuniu_mengamati`: Write today. 30 minutes.
- `sevraya_zero_berbicara`: Adjust timeline to post-chain. Retriage. Takes 5 minutes.
- `julia_kembali_ke_dayan`: Save to `future/`. This scene belongs after a transition arc.

**Writing (30 min):**

Open editor. Write `scene_morning`. No canon anxiety. Compiler already checked it.

**Total time: 42 minutes.**
**Scenes written: 1 PASS. Scenes queued: 1 adjusted, 1 future arc.**
**Words wasted on impossible scenes: 0.**

---

## From Draft to Novel

Writing is not temporary. Drafts are history.

When a scene is final and moves into a Bab or Timer:

1. Save the draft to `writing/archive/`.
2. In the Bab/Timer file, add as the first line:

```
<!-- Derived from: writing/day-01/niuniu_menunggu.md -->
```

Months later, you will want to see: "What did the first draft of this scene look like?"

That data is expensive. Keep it.

---

## The Four Layers

```
Canon      (Bab / Timer)         ← what is already true
    ↑
Decision   (dogfood + compiler)  ← what is ready to write today
    ↑
Drafting   (writing/)            ← writing
    ↑
Publication (Bab / Timer baru)   ← derived from writing/
```

The compiler is not a generator. It is your first editor.
The human editor arrives after the compiler has finished its work.

Every morning the question is no longer:

> "What do I want to write today?"

It is:

> "Of the ideas I have, which ones are ready to be born?"

---

## Setup

1. Ensure you have Python 3.8+.
2. Clone the Void Saga repository.
3. Run `./scripts/demo-pass` once to verify the compiler works.
4. Create your first scenario in `dogfood/`.
5. Run `./scripts/triage-scenes dogfood`.

No API key required for triage. The compiler runs in dry-run mode by default.

---

## What This Is Not

- **Not AI generation.** The triage script does not call Claude. You are deciding what to write — the compiler is validating your decision.
- **Not a replacement for writing.** The compiler does not write prose. It gates scenes. You still write the words.
- **Not a creative straightjacket.** BLOCKED scenes are not deleted — they are queued as future arcs, transition goals, or fork premises.

---

## Metrik

| What | Target |
|------|--------|
| Time to triage 3 scenes | < 2 min |
| Scenes written today | ≥ 1 PASS |
| Words wasted on impossible scenes | 0 |
| BLOCKED scenes saved as future arcs | all of them |
