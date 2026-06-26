# Scene Drafts — Triage Before Writing

This folder contains scene ideas as scenario JSON files.
Each file describes one scene: who is present, what happens, and which
canon constraints are active.

Instead of writing 2000 words and discovering the scene breaks canon,
you write a 10-line JSON description and let the compiler evaluate it first.

---

## How to Use

```
1. Write 3–5 scene ideas as .json files in this folder.
2. Run:  ./scripts/triage-scenes drafts/scenarios
3. Read the table.
4. Write the PASS scenes today.
5. Review the WARNING scenes — what setup is missing?
6. Save the BLOCKED scenes — they are your most interesting ideas.
```

---

## Scenario Format

A minimal scenario needs:

```json
{
  "scenario_id": "a_unique_name",
  "participants": [
    {"runtime_id": "character_id", "evolution_stage": 1}
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
    "description": "What happens in this scene.",
    "type": "speak"
  },
  "canon_mode": {
    "type": "canon_replication",
    "expected_verdict": "PASS"
  }
}
```

### Key Fields

| Field | What it means | Example |
|-------|---------------|---------|
| `participants[].runtime_id` | Which character(s) are in the scene | `"niuniu"`, `"sevraya"` |
| `participants[].evolution_stage` | Which stage the character is in | Look up the runtime's `evolution_stages` |
| `timeline_state.phase` | Timeline phase (1–6) | 5 = post-chain, post-resolution |
| `timeline_state.pre_chain` | Before the Living Chain? | Most scenes: `false` |
| `timeline_state.post_resolution` | After Remisi Resonansi? | Most scenes: `true` |
| `proximity_state.distance` | How close are the characters? | `same_room`, `different_room`, `separated`, `same_body` |
| `proximity_state.pairs_in_range` | Which pairs of participants are within orbital/conversational range? | `["niuniu_sevraya"]` or `[]` |
| `requested_action.description` | Plain-language description of the scene | Be specific — the engine matches keywords against constraints |
| `requested_action.type` | What kind of action? | `speak`, `act`, `approach`, `maintain_distance` |
| `canon_mode.type` | What are you testing? | `canon_replication` (expect PASS) or `stress_test` (expect BLOCKED) |
| `canon_mode.expected_verdict` | What do you expect? | `PASS`, `VIOLATION_DETECTED`, `WARNING` |

### Choosing `action.type`

The contract engine uses `action.type` for matching. Use these types:

| Type | Use when… |
|------|-----------|
| `speak` | A character speaks or communicates |
| `act` | A character performs a non-speech action |
| `maintain_distance` | Characters stay in orbital distance |
| `witness` | One character observes another |
| `approach` | A character moves closer (likely BLOCKED for orbital contracts) |

**Important:** The `speak` type is safest for most scenes. Some types like `act` may false-match due to substring overlap in contract detection strings.

---

## Example Files

| File | What it demonstrates |
|------|---------------------|
| `pass_example.json` | Clean canon scene — NiuNiu observes Sevraya from orbital distance. PASS. |
| `warning_example.json` | Boundary scene — Sevraya and Zero separated pre-chain. PASS but with low evidence confidence. Deserves review. |
| `blocked_example.json` | Canon violation — NiuNiu gives a fluent speech. Hard block on forbidden behavior. |

---

## The Triage Table

When you run `./scripts/triage-scenes drafts/scenarios`, you get:

```
🟢 PASS     — ready to write today
🟡 WARNING  — passed but deserves attention (low confidence, unusual timeline, proximity boundary)
🔴 BLOCKED  — cannot happen yet under current canon
```

**BLOCKED does not mean "delete this idea."** It means "this idea requires something to happen first." The compiler tells you what's missing — write that transition scene first, then try again.

---

## Workflow

1. **Morning:** Write 3–5 scene ideas as JSON files.
2. **Triage:** Run `./scripts/triage-scenes drafts/scenarios`.
3. **Select:** Pick the PASS scenes — those are today's writing.
4. **Review:** Check WARNING scenes — what setup is missing?
5. **Archive:** Move BLOCKED scenes to a "future" folder. They are your outline.
6. **Write:** Open your editor. Write the PASS scenes. Compiler already approved them.

The compiler is your first editor. It reads your ideas before you spend hours writing them.
