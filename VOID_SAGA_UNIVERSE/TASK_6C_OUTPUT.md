# TASK 6C OUTPUT — LLM Prompt Contract

> **Status:** COMPLETE
> **Date:** 25 June 2026

---

## What Was Built

`build_llm_prompt()` — complete LLM prompt contract ready for API integration.

### Prompt Structure

```
┌─ SYSTEM PROMPT ─────────────────────────────┐
│ Universe Context (Era, Grid/Void, Constant) │
│ Character Runtimes (per participant):       │
│   - Stage, Sigil, Voice, Core Wound         │
│   - Primary Contradiction                   │
│ ABSOLUTE PROHIBITIONS (DO NOT):             │
│   - Forbidden behaviors per character       │
│   - Tagged [E] = DO NOT, [I]/[PC] = AVOID   │
│ ANTI-GRAVITY (MUST NOT HAPPEN)              │
│ RELATIONSHIP CONTRACTS                      │
│ OUTPUT FORMAT (JSON Schema)                 │
│ CANON COMPLIANCE (score, confidence, mode)  │
└─────────────────────────────────────────────┘

┌─ USER PROMPT ───────────────────────────────┐
│ SCENE description                           │
│ TIMELINE (phase, pre/post chain)            │
│ PROXIMITY                                   │
│ POV CHARACTER                               │
│ ACTIVE DEFENSES (HIGH/CRITICAL only)        │
│ CAUTION — SOFT WARNINGS (if any)            │
│ Generation instructions                     │
└─────────────────────────────────────────────┘
```

### Key Design Decisions

1. **Forbidden behaviors as PROHIBITIONS ONLY.** "DO NOT write NiuNiu speaking at length or fluently without external force." Never "NiuNiu could consider staying silent." The language is imperative and negative.

2. **Evidence-tagged prohibitions.** `[E]` behaviors = DO NOT. `[I]`/`[PC]` behaviors = AVOID. The LLM gets graded severity.

3. **Anti-gravity as separate section.** Listed after prohibitions as universe-level constraints.

4. **Relationship contracts in prompt.** The behavioral rules between character pairs are injected directly.

5. **Structured JSON output.** The LLM MUST return valid JSON with `narrative`, `character_lines`, `pov_character`, and `canon_compliance_notes`.

6. **No API call yet.** `--dry-run` prints the full prompt. Integration is one function call away.

## CLI

```bash
# Normal: stub story + prompt summary
python compiler.py scenario.json

# Dry-run: full system + user prompt
python compiler.py scenario.json --dry-run

# JSON: structured result
python compiler.py scenario.json --json
```

## Dry-Run Examples

### PASS — NiuNiu+Sevraya orbit (canon safe)

System prompt: ~2800 chars. Includes 2 character runtimes, 14 prohibitions (DO NOT), 5 anti-gravity items, 1 relationship contract.
User prompt: ~400 chars. Scene context only — no warnings, no active defenses.

### WARNING — Sevraya+Zero prechain latent (caution)

System prompt: ~2300 chars. 2 character runtimes, 12 prohibitions, 4 anti-gravity items.
User prompt: includes ACTIVE DEFENSES (INVOLUNTARY Zero takeover trigger) and SOFT WARNINGS (latent stage constraint).

### VIOLATION — Zero emotional (blocked)

No prompt generated. Hard blocked at gate.
Reason: "Forbidden behavior violated: Making Zero emotional, warm, or personally attached to anyone."

## Files Modified

| File | Change |
|------|--------|
| `apps/compiler/compiler.py` | Replaced `build_llm_prompt_blueprint()` with `build_llm_prompt()`. Added `--dry-run`. Added `OUTPUT_SCHEMA`. Removed rogue `_gate_and_build` duplicate. |

## Next: Real LLM Integration

When ready, add:
```python
import anthropic
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-6",
    system=llm_prompt["system_prompt"],
    messages=[{"role": "user", "content": llm_prompt["user_prompt"]}]
)
```
