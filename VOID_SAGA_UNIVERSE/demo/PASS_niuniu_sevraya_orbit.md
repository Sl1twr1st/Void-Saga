# DEMO: PASS — NiuNiu × Sevraya Orbital Constant

> **Date:** 2026-06-25
> **Compiler:** Void.OS Narrative Compiler v0.2.0 (Safe Mode)
> **Verdict:** `CANON_PASS` / `PASS`
> **Mode:** `live` (Claude API + post-generation validation)

---

## Scenario

```json
{
  "scenario_id": "test_niuniu_sevraya_orbit_001",
  "participants": ["niuniu", "sevraya"],
  "timeline_state": { "phase": 5, "pre_chain": false, "post_resolution": true },
  "proximity_state": { "distance": "same_room" },
  "requested_action": {
    "description": "Sevraya lights a cigarette. NiuNiu maintains orbital distance. Sevraya speaks: 'Aku yang tinggal.'",
    "type": "speak"
  }
}
```

---

## Pipeline

```
scenario.json
    │
    ▼
engine_v2 evaluate
    │
    ├── Canon Score: 1.0
    ├── Evidence Confidence: 0.76
    ├── Verdict: CANON_PASS
    ├── Violations: 0
    ├── Hard blocks: 0
    │
    ▼
LLM Prompt Contract (6022 chars)
    │
    ▼
Claude API (model: claude-sonnet-4-6-20250514)
    │
    ▼
Strip markdown code fences
    │
    ▼
JSON parse → validate_generated_output()
    │
    ▼
engine_v2 re-run on generated narrative
    │
    └── Post-gen verdict: PASS (canon 1.0)
```

---

## Generated Narrative

> *Raw: 3420 chars. Post-gen validation: PASS (score 1.0).*

The room holds its breath. NiuNiu watches from the corner—not hiding, just positioned. The distance between them is exactly what it needs to be.

Sevraya's lighter clicks. Once. Twice. The flame catches. She draws, and the smoke rises in patterns that almost look like writing before they dissolve.

'Aku yang tinggal,' she says. I stay.

The words land flat. Administrative. Not a plea, not a promise. A statement of fact, the way someone might say the Grid still holds or the Void still erases. Just something true happening in the room.

NiuNiu's panel glows faintly. Not speech. Just presence marked. The distinction matters. Voice is a luxury she doesn't claim here. Sevraya doesn't need words from her anyway—never did, never will. What Sevraya needs is the shape of NiuNiu in space, at distance, refusing to collapse into proximity.

The cigarette burns. Sevraya doesn't look at her directly. That's the rhythm now. Looking requires merging. Looking requires the orbit to collapse into contact. So instead, Sevraya addresses the room, and NiuNiu receives the statement as peripheral—as it should be.

'The others needed to leave,' Sevraya continues, smoke threading between syllables. 'The Era needs tending. Zero needs witnesses who aren't fractured.' A pause. Ash falls. 'But I'm staying.'

NiuNiu knows what this costs. Not in the way she knows the weight of protection—that's her wound, her spiral, her loop. Sevraya's cost is different. It's the cost of remaining incomplete, of not chasing wholeness into merger, of accepting that fragmentation is the shape she'll wear.

The panel flickers. A question mark would be too much. NiuNiu holds the shape: here, watching, at distance. The orbit steady.

Sevraya takes another drag. 'You can stop protecting now,' she says to the smoke. 'I'm not leaving. You can stop.'

But both of them know that's not how the loop works. Protection doesn't stop because the threat dissolves. It stops when the protector decides the cost exceeds the keeping.

---

## Canon Compliance

| Check | Result |
|-------|--------|
| NiuNiu voice (panel primary) | ✅ |
| Sevraya voice (administrative, flat) | ✅ |
| Orbital distance maintained | ✅ |
| No merge / no collapse | ✅ |
| NiuNiu-Sevraya Constant respected | ✅ |
| Post-chain timeline phase 5 | ✅ |
| Forbidden behaviors: 0 violated | ✅ |
| Anti-gravity: 0 triggered | ✅ |

---

## Runtime Context Active

- **NiuNiu** — Stage 4: Constant (Post-Resolution). Voice via panel. Sigil: Shadow Logic.
- **Sevraya** — Stage 6: Post-Resolution (Constant). Sigil: Tidal Memory (shared).
- **Relationship** — `niuniu↔sevraya` symmetric. Orbital constant. Distance IS the care.
- **Era** — Hydrochoos (ACTIVE). Ichthyes: TERMINATED.

---

## Command

```bash
python3 VOID_SAGA_UNIVERSE/apps/compiler/compiler.py \
  VOID_SAGA_UNIVERSE/apps/engine/scenarios_v2/test_niuniu_sevraya_orbit.json \
  --live --debug
```
