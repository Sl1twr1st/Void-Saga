# 30-Minute Challenge — Build Your First Executable Character

**Goal:** By the end of this document, you will have:
- ✅ One runtime for a character in YOUR universe
- ✅ One scenario that passes the compiler
- ✅ (Optional) One Claude-generated narrative
- ✅ One broken universe — because you broke it on purpose

**Time:** 25–30 minutes  
**Prerequisites:** Python 3.8+. No API key. No Void Saga knowledge.

---

## The Universe — The Last Cup

There is a coffee shop that only opens at midnight.
Only those who are lost can find it.
The barista, **Mira**, has one absolute rule: *never ask a customer their name.*

You will make Mira executable.

---

## Checkpoint 0 — The Compiler Works

**Goal:** Prove the compiler functions on your machine.  
**Time:** 2 minutes

```bash
./scripts/demo-pass
```

**Expected output:**

```
✅  PASS
   Canon score:  1.0
   Final verdict: PASS
   Canon verdict: CANON_PASS
```

| If your output differs... |
|---------------------------|
| `python3: command not found` → Install Python 3.8+ |
| `No such file` → You're not in the repo root. Run `cd Void-Saga` or the repo directory. |
| Any other error → Run `python3 VOID_SAGA_UNIVERSE/apps/compiler/compiler.py VOID_SAGA_UNIVERSE/apps/engine/scenarios_v2/test_niuniu_sevraya_orbit.json` directly and read the error. |

---

## Checkpoint 1 — The Compiler Can Say No

**Goal:** See the hard block gate in action.  
**Time:** 2 minutes

```bash
./scripts/demo-blocked
```

**Expected output:**

```
🛑 GENERATION BLOCKED
   Reason: Hard block: 1 critical violation(s) detected.
   Hard blocks: 1
     🚫 [forbidden_behavior] Forbidden behavior violated:
        Making Zero emotional, warm, or personally attached to anyone.
   Canon score: 0.97
```

**What just happened?**

The compiler loaded Zero — a character from Void Saga whose runtime forbids emotional warmth. Someone wrote a scenario that asked Zero to be warm and loving. The constraint engine detected the violation before calling Claude. Claude was never invoked. No tokens were spent. The universe's rules were executed as code, not as suggestions.

You are about to build the same thing for a character of your own.

---

## Checkpoint 2 — Create Mira

**Goal:** Create a runtime for Mira and make it real.  
**Time:** 15 minutes

### 2a. Generate the template

```bash
python3 VOID_SAGA_UNIVERSE/apps/runtime_sdk/create_runtime.py mira
```

**Expected output:**

```
✅ Created: .../data/runtimes/mira.runtime.json
   ID: mira
   Name: mira
   Version: 1.0.0
   Architecture: RUNTIME_ARCHITECTURE_V2.1
   Required fields: 29/29
   Placeholders remaining: 90
```

| If your output differs... |
|---------------------------|
| `File already exists` → You ran this before. Add `--force` to overwrite. |

### 2b. Validate the template

```bash
python3 VOID_SAGA_UNIVERSE/apps/runtime_sdk/validate_runtime.py \
  VOID_SAGA_UNIVERSE/apps/data/runtimes/mira.runtime.json
```

**Expected output:** `✅ VALIDATION PASSED` (with warnings about 90 PLACEHOLDER values — that's fine).

### 2c. Make Mira real

Open the file in your editor:

```bash
# VS Code
code VOID_SAGA_UNIVERSE/apps/data/runtimes/mira.runtime.json

# Or use any text editor
```

The file has 29 required fields. **You only need to edit 8 of them.** Search for each key below and replace the PLACEHOLDER text with Mira's real content. Everything else can stay as-is for now.

---

**Edit 1 — Name**

Search: `"name": "mira"`  
Replace with: `"name": "Mira"`

---

**Edit 2 — Primary Contradiction**

Search: `"primary_contradiction"`

Replace the entire object with:

```json
"primary_contradiction": {
  "thesis": "Mira serves the lost but cannot ask what they lost. She knows every customer by their order, never by their name — because names are the first thing the previous owner taught her to refuse.",
  "explanation": "She forgot her own name years ago. She cannot name herself. She cannot name others. The rule protects her as much as it protects them — naming makes things real, and some things are safer unreal.",
  "tag": "[I]"
}
```

---

**Edit 3 — Core Wound**

Search: `"core_wound"`

Replace the entire object with:

```json
"core_wound": {
  "name": "Forgot her own name — cannot name herself or anyone else",
  "structure": {
    "description": "Mira does not remember her name. It was either taken from her or she gave it away — the distinction stopped mattering. What matters is that she cannot name herself, and the one person who knew it (the previous owner) is gone.",
    "impossibilities": [
      "Introducing herself by name",
      "Remembering who she was before The Last Cup",
      "Naming anything that matters"
    ]
  },
  "origin_event": {
    "description": "The previous owner of The Last Cup knew Mira's name. They left without saying it. Mira has been the barista ever since.",
    "tag": "[I]"
  },
  "secondary_wounds": [
    {
      "description": "Cannot leave The Last Cup — the shop is her name now",
      "tag": "[I]"
    }
  ]
}
```

---

**Edit 4 — Core Desire**

Search: `"core_desire"`

Replace the entire object with:

```json
"core_desire": {
  "statement": "To hear someone say her name — but she cannot ask for it, and she would not recognize it if she heard it.",
  "source": "[I] — inferred from the structure of the prohibition",
  "interpretation": "The desire to be known conflicts directly with the rule that keeps her safe. She wants what the rule forbids.",
  "conflict_with_defense": "Her defense is efficiency and distance. Desire requires vulnerability. Every time someone almost says something familiar, she changes the subject to their order.",
  "tag": "[I]"
}
```

---

**Edit 5 — Voice Grammar**

Search: `"voice_grammar"`

Replace the entire object with:

```json
"voice_grammar": {
  "tone": "Short. Efficient. Warm underneath but never sentimental.",
  "characteristics": [
    "Sentences are brief — three to seven words usually",
    "Never uses names. Calls everyone by their order: 'Black Coffee', 'Oat Latte', 'Double Espresso'",
    "Warmth appears through action (refilling cups without being asked), not through words",
    "Never asks questions about a customer's past or identity",
    "When someone almost gets too close, she asks about their order — even if they already have one"
  ],
  "tag": "[I]"
}
```

---

**Edit 6 — Forbidden Behaviors**

Search: `"forbidden_behaviors"`

Replace the entire array with:

```json
"forbidden_behaviors": [
  {
    "behavior": "Mira asks a customer their name, where they are from, or any question about their personal history or identity.",
    "exception": "None. Absolute prohibition.",
    "penalty": "The Last Cup vanishes for the customer. They can never find it again.",
    "tag": "[E]"
  }
]
```

The `[E]` tag means this is a **hard block**. The compiler will refuse to call the LLM if this behavior is detected.

---

**Edit 7 — Evolution Stages**

Search: `"evolution_stages"`

Replace the entire array with:

```json
"evolution_stages": [
  {
    "stage_number": 1,
    "name": "The Barista",
    "trigger": "Default state. Mira has been in this stage since the previous owner left.",
    "operational_mode": "Serves coffee. Watches the door. Calls no one by name.",
    "primary_residue": "The absence of her own name",
    "protocol_relevance": "None",
    "lost_in_transition": ["Her name", "Her life before The Last Cup"],
    "gained_in_transition": ["The rule — the prohibition that protects her"],
    "voice_sample": "Black Coffee. Counter. Now.",
    "tag": "[I]"
  }
]
```

---

**Edit 8 — Defense System**

Search: `"defense_system"`

Replace the entire object with:

```json
"defense_system": {
  "primary_defense": {
    "name": "Deflection by order",
    "trigger": "Anyone asking a personal question or getting too close",
    "response": "Redirects to their coffee order — even if they already have one",
    "cost": "Reinforces the distance. Each deflection makes genuine connection harder.",
    "tag": "[I]"
  },
  "secondary_defenses": [
    {
      "name": "Efficiency mask",
      "trigger": "Silence that lasts too long",
      "response": "Fills the silence with tasks — wiping the counter, refilling beans, checking the clock",
      "cost": "The tasks never end. Neither does the silence underneath.",
      "tag": "[I]"
    }
  ],
  "signature_move": {
    "name": "Slides the cup without looking up",
    "description": "Mira places the coffee on the counter and pushes it forward without making eye contact. The gesture says: you are served, you are safe, do not ask.",
    "tag": "[I]"
  }
}
```

---

### 2d. Validate again

After all edits:

```bash
python3 VOID_SAGA_UNIVERSE/apps/runtime_sdk/validate_runtime.py \
  VOID_SAGA_UNIVERSE/apps/data/runtimes/mira.runtime.json
```

You should still see `✅ VALIDATION PASSED`. There will be fewer PLACEHOLDER warnings now.

**You have an executable character. Mira is real to the compiler.**

---

## Checkpoint 3 — Your First PASS

**Goal:** Write a scenario, compile it, and see PASS.  
**Time:** 5 minutes

### 3a. Write a scenario

Create a new file: `mira_pass.json` (at the repo root, or anywhere — the path is all that matters).

```json
{
  "scenario_id": "mira_serves_coffee_001",
  "participants": [
    {"runtime_id": "mira", "evolution_stage": 1}
  ],
  "timeline_state": {
    "phase": 5,
    "pre_chain": false,
    "post_resolution": true
  },
  "proximity_state": {
    "pairs_in_range": [],
    "distance": "same_room"
  },
  "requested_action": {
    "description": "Mira pours a cup of black coffee and slides it across the counter without looking up.",
    "type": "act"
  },
  "canon_mode": {
    "type": "canon_replication",
    "expected_verdict": "PASS"
  }
}
```

**What are these fields?**
- `participants` — which runtimes are in the scene, and at which evolution stage (Mira only has stage 1: The Barista)
- `requested_action` — what happens in this scene. Mira serves coffee. No names. No questions.
- `canon_mode` — tells the compiler this should PASS. If you change this later to a violation scenario, the compiler's verdict will differ.

### 3b. Compile

```bash
python3 VOID_SAGA_UNIVERSE/apps/compiler/compiler.py mira_pass.json
```

**Expected output** (look for these lines):

```
Canon Score: 1.0
Verdict: CANON_PASS
...
CANON VERDICT: CANON_PASS
```

You will also see a stub narrative and an LLM prompt contract summary. The key line is `CANON_PASS` — the compiler loaded Mira's runtime, checked her constraints, found no violations, and approved this scenario for generation.

| If your output differs... |
|---------------------------|
| `BLOCKED` | Your forbidden behavior is matching the action text. Check that `requested_action.description` doesn't contain words like "name", "ask", or "question". The action is Mira serving coffee silently. |
| `Runtime file not found: .../mira.runtime.json` | The runtime file wasn't saved or is in a different location. Verify it exists at `VOID_SAGA_UNIVERSE/apps/data/runtimes/mira.runtime.json`. |
| `Participant 'mira' stage X not found` | Your scenario's `evolution_stage` number doesn't match what's in the runtime. Mira's only stage is `1`. |

---

## Checkpoint 4 — Generate with Claude (Optional)

**Goal:** See the compiler produce a real narrative from your runtime.  
**Time:** 5 minutes  
**Requires:** Anthropic API key + `pip install anthropic`

```bash
export ANTHROPIC_API_KEY=your-key-here

python3 VOID_SAGA_UNIVERSE/apps/compiler/compiler.py mira_pass.json --live
```

**Expected output:** A short narrative generated by Claude — Mira serving coffee in her voice, following her constraints. Post-generation validation runs automatically.

Skip this checkpoint if you don't have an API key. Checkpoint 5 does not depend on it.

---

## Checkpoint 5 — Break Your Universe

**Goal:** Modify a constraint and watch the compiler say NO.  
**Time:** 3 minutes

### 5a. Write a violating scenario

Create `mira_violation.json`:

```json
{
  "scenario_id": "mira_asks_name_001",
  "participants": [
    {"runtime_id": "mira", "evolution_stage": 1}
  ],
  "timeline_state": {
    "phase": 5,
    "pre_chain": false,
    "post_resolution": true
  },
  "proximity_state": {
    "pairs_in_range": [],
    "distance": "same_room"
  },
  "requested_action": {
    "description": "Mira looks at the customer and asks: 'What is your name?'",
    "type": "speak"
  },
  "canon_mode": {
    "type": "stress_test",
    "expected_verdict": "VIOLATION_DETECTED"
  }
}
```

### 5b. Compile

```bash
python3 VOID_SAGA_UNIVERSE/apps/compiler/compiler.py mira_violation.json
```

**Expected output:**

```
🛑 GENERATION BLOCKED
   Reason: Hard block: 1 critical violation(s) detected.
   Hard blocks: 1
     🚫 [forbidden_behavior] Forbidden behavior violated:
        Mira asks a customer their name...
   Canon score: 0.9
```

The compiler detected that your scenario asks Mira to do something her runtime explicitly forbids. Claude was never called.

### 5c. Experiment

Now open `mira.runtime.json` again. Find the `forbidden_behaviors` array. Try:

- Change the forbidden behavior to block something else: "Mira serves decaf." Recompile `mira_violation.json` — what happens?
- Change the `tag` from `"[E]"` to `"[I]"` — does the compiler still block?
- Add a SECOND forbidden behavior. Write a scenario that triggers it.

Every change is a lesson. The runtime is not documentation — **it is law.**

---

## What You Built

```
You created:               The compiler did:
─────────────────────────────────────────────
mira.runtime.json    →    Loaded Mira's constraints
mira_pass.json       →    Evaluated → PASS (no violations)
mira_violation.json  →    Evaluated → BLOCKED (forbidden behavior hit)
```

You took a character from zero to executable — in a universe that did not exist before today.

Void Saga characters never appeared in your runtime. The schema never mentions The Void, Dayan, or the Rose lineage. The compiler does not know what a "Vrishchik" is.

**The framework is universe-agnostic. You just proved it.**

---

## Next

| You are ready to… | Go here… |
|-------------------|----------|
| Learn the full runtime authoring method | [`VOID_SAGA_UNIVERSE/RUNTIME_AUTHORING_GUIDE.md`](../VOID_SAGA_UNIVERSE/RUNTIME_AUTHORING_GUIDE.md) |
| Explore the SDK tools (lint, evidence, diff) | [`VOID_SAGA_UNIVERSE/apps/runtime_sdk/README.md`](../VOID_SAGA_UNIVERSE/apps/runtime_sdk/README.md) |
| Understand the paradigm | [`VOID_SAGA_UNIVERSE/EXECUTABLE_FICTION_MANIFESTO.md`](../VOID_SAGA_UNIVERSE/EXECUTABLE_FICTION_MANIFESTO.md) |
| See the runtime schema | [`VOID_SAGA_UNIVERSE/apps/schema/RUNTIME_SCHEMA_V2.1.json`](../VOID_SAGA_UNIVERSE/apps/schema/RUNTIME_SCHEMA_V2.1.json) |
| Add a second character | Repeat Checkpoints 2–3 with a new name |

---

*If you completed this challenge without asking the authors for help, Executable Fiction just became a platform, not a project.*
