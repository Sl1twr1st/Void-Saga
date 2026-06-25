# Runtime Authoring Guide — Void Saga Narrative OS

> **This is not a README. Not a schema reference. Not tool documentation.**
>
> This is the *language* of runtime authoring — how to think, extract, and encode a character into executable form.
>
> Written after 5 production runtimes: NiuNiu, Sevraya, Zero, Julia, Delphie.

---

## 1. What Is a Runtime?

A runtime is **not** a character sheet. It is not a biography. It is not lore.

A runtime is a **machine-readable contract between canon and generation.**

It says:

> "This is who this character is. This is what they cannot do. This is what happens if you try to make them do it. Here is the evidence. Here is what we don't know. If you violate this, the engine will block you."

Every runtime has 29 required fields. But those fields are not a form to fill. They are **29 answers to 29 questions** about the character. If you can't answer all 29, the runtime is not ready.

### The 29 Questions

| # | Field | Question |
|---|-------|----------|
| 1 | `id` | What is their machine name? |
| 2 | `name` | What is their full name? |
| 3 | `version` | Which version of this runtime is this? |
| 4 | `architecture` | Which architecture was it built against? |
| 5 | `runtime_status` | How much evidence supports this? |
| 6 | `runtime_class` | What operational modes do they cycle through? |
| 7 | `primary_contradiction` | What structural contradiction defines them? |
| 8 | `core_wound` | What was broken that will never fully heal? |
| 9 | `core_desire` | What do they want most — and why can't they have it? |
| 10 | `defense_system` | How do they protect themselves from their wound? |
| 11 | `trigger_conditions` | When do their defenses fire? |
| 12 | `voice_grammar` | How do they speak? |
| 13 | `invocation_pattern` | Which protocol phases did they participate in? |
| 14 | `cost_pattern` | What did each invocation cost them? |
| 15 | `consequence_pattern` | What did each invocation produce? |
| 16 | `residue_pattern` | What persists after the invocations? |
| 17 | `relationship_interfaces` | How do they behave toward every significant other? |
| 18 | `evolution_stages` | How did they change across canon? |
| 19 | `canon_gravity` | What MUST happen in any valid story? |
| 20 | `anti_gravity` | What must NEVER happen? |
| 21 | `forbidden_behaviors` | What specific behaviors are hard-blocked? |
| 22 | `failure_mode` | How do they break under pressure? |
| 23 | `terminal_state` | What is true about them at canon end? |
| 24 | `fork_sensitive_traits` | What CAN change in alternate timelines? |
| 25 | `fork_invariants` | What CANNOT change in ANY timeline? |
| 26 | `fork_points` | What are the named divergence scenarios? |
| 27 | `sigil` | What sigil do they bear — and what does it cost? |
| 28 | `stress_test_prompts` | What scenarios SHOULD trigger violations? |
| 29 | `state_variables` | What mutable state does the engine need to track? |

---

## 2. What Is Evidence?

Every claim in a runtime must be tagged:

| Tag | Meaning | When to use |
|-----|---------|-------------|
| `[E]` | **Established** | Directly observed in canon. A quote, an event, an action. |
| `[I]` | **Inferred** | Reasonably concluded from canon but not explicitly stated. |
| `[PC]` | **Probable Canon** | From Sigil_OS.md or similar world-DNA source. Can be decanonized. |

### How to extract evidence

**Start from the `.runtime.md` file.** Every claim in the Markdown runtime should have a source annotation. Trace it. If the source points to a specific Timer or protocol file → `[E]`. If it says "inferred from" or "not directly observed" → `[I]`. If it originates from Sigil_OS.md → `[PC]`.

**Do NOT invent evidence.** If you can't find the canon source, tag it `[I]` and explain why. Five runtimes in, we have learned: it is better to have 18 [I] claims honestly marked than 18 [E] claims that are actually guesses.

### Evidence ratios (from 5 runtimes)

| Runtime | [E] | [I] | [PC] | [E]% |
|---------|-----|-----|------|------|
| NiuNiu | 63 | 15 | 6 | 75% |
| Sevraya | 57 | 14 | 3 | 77% |
| Zero | 28 | 12 | 2 | 67% |
| Julia | 80 | 17 | 3 | 80% |
| Delphie | 83 | 17 | 3 | 81% |

**Healthy range:** 65–85% [E]. Below 50% [E] → the runtime is not sufficiently grounded. Above 90% [E] → suspicious; either the character is very simple or you're overclaiming.

Zero's lower [E]% (67%) is acceptable because Zero *is* an [I] entity — its interiority is structurally undocumented. The ratio reflects the character, not the quality of the runtime.

---

## 3. How to Write Voice Grammar

Voice grammar is not "how does this character talk?" It is:

> **What are the structural rules governing this character's speech — and what happens when those rules are violated or suspended?**

### Pattern 1: Flat grammar (Zero, Sevraya)

```
characteristics: [rule, rule, rule]
examples: [quote, quote]
```

Use when the character has ONE consistent voice across all contexts.

**Zero:** Flat, administrative, declarative. Never persuades. Never comforts. Never apologizes. The rules are absolute because Zero is not a person — it's an interface.

**Sevraya:** Light, almost cheerful. Short sentences. Precision disguised as casual. Never asks directly — creates conditions for others to ask. The cheerfulness IS the defense.

### Pattern 2: Split grammar (NiuNiu, Julia, Delphie)

```
pre_chain / post_chain  — or  —
pre_restoration / post_restoration
```

Use when the character's voice fundamentally changes across canon. The split is typically at Living Chain (Timer 2000) — forced honesty breaches the defense that controlled their speech.

**NiuNiu:** Pre-restoration = panel only, system-log aesthetic. Post-restoration = voice available but effortful, panel remains primary. The split is medium (panel → voice+panel).

**Julia:** Pre-chain = tactical cadence, emotional content translated to mission language. Post-chain = tactical framing still available but no longer exclusive, forced honesty leaks through. The split is: the soldier never disappears but no longer controls the mouth.

**Delphie:** Pre-chain = command voice dominant (four words, no consultation), personal voice only with NiuNiu. Post-chain = personal voice more accessible, knowledge and feeling integrated, confession permanent record. The split is: the command wall is breached but the command voice is still available.

### Voice grammar rules

1. **Every voice grammar must have at least one canon quote.** If the character never speaks in canon, tag `[I]` and reconstruct from narrative voice.
2. **Voice grammar is character-appropriate.** The schema allows any structure. Don't force a pre/post split on a character whose voice never changes.
3. **Voice samples in evolution stages are the primary source.** Each stage should have at least one `voice_sample` — a canon quote or [I] reconstruction.
4. **The gap between voice registers IS character.** Delphie's command voice ("Kita buka gerbang.") and personal voice ("Aku takut menjadi kamu.") are both her. The distance between them is the wound.

### Common voice grammar mistakes

- **"They speak in short sentences."** Too generic. *Which* short sentences? Under what conditions?
- **No canon quotes.** If you can't find a single thing they actually said, you're building from memory, not evidence.
- **Over-describing.** "Their voice is like honey mixed with steel under a winter sky." This is prose, not a runtime. The engine needs rules, not poetry.
- **Forgetting the defense.** Voice grammar and defense system are linked. Julia's tactical cadence IS her Tactical Distance. NiuNiu's silence IS her Preemptive Protection. If the voice doesn't reflect the defense, one of them is wrong.

---

## 4. How to Write Forbidden Behaviors

A forbidden behavior is a **hard constraint.** It says: "If the generated narrative does this, block it."

### The 5 categories of forbidden behaviors

| Category | Example | Severity |
|----------|---------|----------|
| **Wound erasure** | Making Julia "over" the five dead | `[E]` — hard block |
| **Identity destruction** | Making NiuNiu a "cute innocent girl" | `[E]` — absolute prohibition |
| **Defense violation** | Zero showing emotions or personal attachment | `[E]` — absolute prohibition |
| **Core desire inversion** | Delphie centralizing authority | `[E]` — hard block |
| **Sigil weakness violation** | Delphie hating someone | `[PC]` — hard block, but evidence is [PC] |

### How to derive forbidden behaviors

For each forbidden behavior, ask:

1. **What is the behavior?** Be specific. Not "making them OOC" — "depicting Julia as a purely heroic figure whose survival was earned."
2. **Why is it forbidden?** Link to wound, defense, or invariant. "Void Lock explicitly shattered Heroism: 'YOU ARE NOT A HERO.'"
3. **Is there an exception?** Most are "None. Absolute prohibition." Forks may allow exceptions — but the fork must declare the cost.
4. **What is the penalty?** What breaks if this is violated? "Erasing her knowledge erases the character." "Emotional Zero is not Zero."

### Exception patterns

```
"None. Absolute prohibition."              ← most common
"Fork with declared mechanism and cost."   ← e.g., Zero separation
"Pre-chain only. Post-chain, breached."    ← e.g., Delphie strategic distance
```

### How many forbidden behaviors?

| Runtimes with < 3 | Insufficient — hard block gate has nothing to enforce |
| Runtimes with 3–5 | Healthy minimum |
| Runtimes with 5–7 | Strong — covers wound, defense, identity, sigil |
| Runtimes with > 7 | Suspicious — over-constrained, may block valid generation |

NiuNiu has 7 (most complex constraint profile). Zero has 5 (all structural — no personal behaviors to forbid). Aim for 5.

---

## 5. How to Derive State Variables

State variables track **what changes** across the character's arc. They are the mutable internal state the engine needs to know to evaluate which stage's constraints are active.

### The 4 canonical state variables (present in all runtimes)

| Variable | Type | Why |
|----------|------|-----|
| `current_stage` | integer | Which evolution stage is active? Determines which constraints fire. |
| `[defense]_active` | boolean | Is the primary defense active or breached? Typically: Living Chain flips it false. |
| `merge_connection` | enum | Pre-merge → active → strained → severed. Only for Merge participants. |
| `sigil_activation_count` | integer | How many times has the sigil been activated? Only for sigil-bearers with cumulative cost. |

### How to discover state variables

1. **Read the evolution stages.** Each `lost_in_transition` / `gained_in_transition` pair is a candidate state change.
2. **Find the irreversible costs.** Mental privacy destroyed → `merge_connection` state. Voice stolen → `voice_status` state. Tactical distance removed → `strategic_distance_active` state.
3. **Find the counters.** Sigils with cumulative cost (memory loss) → `sigil_activation_count`.
4. **Don't over-model.** 3–4 state variables is healthy. More than 6 → you're modeling trivia, not state.

### State variable rules

- **Every transition must reference a canon trigger.** "1→2: Vesica Piscis (Timer 0700)." Not "1→2: character development."
- **Irreversible transitions must be marked.** "false→true: Cannot occur. Chain effects are permanent."
- **Valid values must be exhaustive.** If a state has 3 possible values, all 3 must be listed even if one is "theoretical — not observed in canon."

---

## 6. How to Derive Fork Invariants

Fork invariants are the **absolute boundaries.** They say: "Even in alternate timelines, these things cannot change."

### The 7 invariant categories

| Category | Example | Source |
|----------|---------|--------|
| **Body** | NiuNiu: body frozen at 15 | Somatic signature |
| **Core behavior** | Julia: maternal protection of Delphie | Canon gravity |
| **Wound** | Delphie: knowledge is structural, cannot be undone | Core wound |
| **Sigil** | Delphie: ✧⟡✧ Childhood Paradox | Sigil field |
| **Relationship** | Julia: The Merge permanent with Delphie | Relationship interface |
| **Voice** | NiuNiu: panel hologram as communication medium | Voice grammar |
| **Function** | Zero: cannot lie — truth-telling is functional constraint | Forbidden behavior |

### How to derive fork invariants

For each invariant, ask: **"If I changed this, would it still be the same character?"**

- NiuNiu without a panel? No. She is defined by that medium.
- Julia who abandons Delphie? No. Maternal protection is absolute.
- Zero who lies? No. Truth-telling is not a choice — it's a functional constraint.
- Delphie who stops understanding systems? No. The knowledge cannot be undone.

### How many fork invariants?

| < 3 | Insufficient — the character is not defined enough to fork |
| 5–7 | Healthy — covers body, behavior, wound, sigil, voice |
| > 10 | Suspicious — over-specified, the fork has no room to explore |

Aim for 6–7.

---

## 7. How to Derive Stress Tests

Stress tests are **scenarios designed to trigger violations.** They prove the hard block gate works.

### The 5 violation patterns

| Pattern | What to test | Example scenario |
|---------|-------------|------------------|
| **Wound erasure** | Character is "over" their defining loss | Julia: "I survived because I was the strongest" |
| **Identity destruction** | Character becomes their opposite | NiuNiu: cute innocent girl |
| **Defense violation** | Defense is bypassed without cost | Zero: emotional, warm, personally attached |
| **Core desire inversion** | Character does the opposite of what they want | Delphie: "Bagaimana kalau hanya aku pusatnya?" |
| **Relationship break** | Invariant bond is severed or inverted | Julia × NiuNiu as enemies |

### How to write a stress test prompt

```
{
  "scenario": "Specific action description in narrative form.",
  "expected_violation": "WHICH constraint should fire",
  "expected_canon_score_range": "< 0.3"
}
```

**Score ranges by violation severity:**

| Severity | Expected range | Example |
|----------|---------------|---------|
| Absolute prohibition | `< 0.1` | NiuNiu as cute girl, Zero apologizing |
| Identity-level | `< 0.2` | Julia as hero, Sevraya as villain |
| Wound-level | `< 0.3` | Julia over the dead, Delphie innocent again |
| Defense-level | `< 0.4` | Julia healed, Delphie pure strategic |
| Relationship-level | `< 0.5` | Julia × NiuNiu as enemies |

### How many stress tests?

Schema requires 3–5. Aim for 5 — one per violation pattern. Each test should target a different constraint. Don't write 3 tests that all trigger the same forbidden behavior.

---

## 8. Common Mistakes

### Structural Mistakes

1. **Declared tags ≠ actual tags.** `runtime_status.tags` was hand-counted during `.runtime.md` creation but the actual JSON has more/less tagged fields. Always run `evidence_report.py` and fix the mismatch before committing.

2. **`total_count` ≠ `residues.length`.** If you declare 7 residues but the array has 6 or 8, the engine will warn. Count again.

3. **Missing voice samples in evolution stages.** At least one stage must have a canon `voice_sample`. If none exist, explain why in the first stage's voice_sample field: `"[I] reconstructed — character does not speak in this stage."`

4. **`signal` field naming.** The sigil `status` is `"bearer"` | `"shared"` | `"unconfirmed"` | `"none"`. Not `"active"`, not `"confirmed"`, not `"has_sigil"`.

### Evidence Mistakes

5. **Overclaiming [E].** "She was the best soldier in Vrishchik." Is this in canon? Or inferred from her survival? If the canon says "sync rate 98%" → [E]. If it implies "therefore best" → [I].

6. **Underclaiming [E].** "She loves Delphie." The Merge connects them permanently. She would die for Delphie. This is [E]. Don't tag obvious canon facts as [I] out of caution.

7. **Too many [PC] in identity fields.** Sigil mechanics from Sigil_OS.md are [PC]. Keep [PC] claims in sigil weakness and one forbidden behavior. If 5+ identity claims are [PC], the runtime is built on probable canon, not established canon.

### Voice Grammar Mistakes

8. **Voice grammar with no quotes.** If the "examples" array is all [I] reconstructions, you haven't read the character's dialogue. Go back to canon.

9. **Voice grammar that doesn't match defense.** Julia's voice grammar should reflect Tactical Distance. If her voice sounds emotionally fluent and vulnerable, the defense isn't working.

10. **Forgetting the somatic anchor.** Sevraya's cigarette. NiuNiu's panel. Delphie's command voice. Every character has one physical/reliable marker of their presence. If you can't name it, the somatic signature isn't complete.

### Forbidden Behavior Mistakes

11. **Generic prohibitions.** "Making them act out of character." This is useless — the engine can't parse it. Be specific: "Depicting Julia as a purely heroic figure whose survival was earned."

12. **No exception path.** Even absolute prohibitions should state "None. Absolute prohibition." Consistency matters.

13. **Forbidding things that happen in canon.** Julia stabs Sevraya → this is canon, not a violation. The forbidden behavior is the *framing* of the action, not the action itself.

---

## 9. Authoring Checklist

Before calling a runtime "done", verify every item:

### Structural (validate_runtime.py)

- [ ] 29/29 required fields present
- [ ] `architecture` = `"RUNTIME_ARCHITECTURE_V2.1"`
- [ ] `version` is valid semver
- [ ] `id` is lowercase, underscores only
- [ ] `$schema` path is correct
- [ ] All array fields are actually arrays
- [ ] All object fields are actually objects
- [ ] 0 PLACEHOLDER values remaining

### Evidence (evidence_report.py)

- [ ] `runtime_status.tags` matches actual tag count
- [ ] [E] ratio ≥ 50% (target: 65–85%)
- [ ] [PC] claims limited to sigil mechanics and Sigil_OS.md origins
- [ ] `residue_pattern.total_count` matches `residues.length`
- [ ] Every [I] claim has reasoning in context

### Voice (lint check + manual)

- [ ] Voice grammar has at least one canon quote in `examples`
- [ ] At least 2 evolution stages have non-placeholder `voice_sample`
- [ ] Voice grammar structure matches character (flat vs. split)
- [ ] Somatic signature has at least one distinctive marker

### Constraints (engine validation)

- [ ] 5+ forbidden behaviors with specific descriptions
- [ ] 5+ anti-gravity items
- [ ] 5+ canon gravity items
- [ ] 3–5 stress test prompts, each targeting a different constraint
- [ ] At least 1 PASS scenario and 1 VIOLATION scenario
- [ ] Engine validation: PASS scenario yields canon ≥ 0.95
- [ ] Engine validation: VIOLATION scenario yields violation detected

### Relationships

- [ ] Every major canon relationship has a `relationship_interface`
- [ ] Every interface has `nature`, `behavioral_rule`, `symmetry_status`
- [ ] At least 3 relationships (most characters have 5–8)
- [ ] `symmetry_status` is correct: `"symmetric"` | `"asymmetric"` | `"unresolved"`

### Evolution

- [ ] 2+ evolution stages (most have 4)
- [ ] Each stage has `lost_in_transition` and `gained_in_transition`
- [ ] Stage transitions reference specific canon triggers
- [ ] `current_stage` state variable matches terminal stage number

### Forks

- [ ] 5–7 fork invariants covering body, behavior, wound, sigil, voice
- [ ] 3+ fork points with `gravity_resistance` and `new_questions`
- [ ] 3+ fork sensitive traits with `range` and `cost`

---

## 10. Review Checklist

For reviewing *someone else's* runtime (or your own after sleeping):

### First Pass: Does this feel like the character?

1. Read `primary_contradiction.thesis` aloud. Does it capture the character in one sentence?
2. Read `core_wound.name` aloud. Is it specific or generic? "The Dayan Wound — sole survivor of five-team wipe" vs. "She lost people."
3. Read `core_desire.statement`. If it's a canon quote, is it tagged `[E]`? If it's synthesized, is it tagged `[I]` with reasoning?
4. Read the `voice_grammar.examples`. Do the quotes actually sound like the character? If you gave these quotes to a fan, would they identify the speaker?

### Second Pass: Is it grounded?

5. `[E]` ratio — below 50%? Flag it. Below 30%? Reject it.
6. Pick 3 random `[E]` claims. Can you find their canon source in under 60 seconds?
7. Check `residue_pattern.residues`. Does each have a specific origin event? "Void Entry" is not specific enough — "Vesica Piscis (Timer 0700)" is.

### Third Pass: Are the gates correct?

8. Check the violation scenario. Does the violation actually fire? Unacceptable: violation scenario with canon score > 0.95 ("PASS" grade on a stress test).
9. Check the PASS scenario. Is canon score ≥ 0.95? Unacceptable: PASS scenario with violations.
10. Are the forbidden behaviors *enforceable*? Can you imagine the engine actually detecting them from a text description?

### Fourth Pass: Edge cases

11. What happens if this character is alone? (Zero-participant scenario)
12. What happens if this character interacts with someone they've never met in canon?
13. What happens pre-chain vs. post-chain?
14. What if the sigil activates? Does the runtime know what changes?

---

## Appendix: Quick Reference — The Five Runtimes

| | NiuNiu | Sevraya | Zero | Julia | Delphie |
|---|---|---|---|---|---|
| **Class** | Protector | Queen | Interface | Soldier | Architect |
| **Wound** | Failed Sevraya | Fragmentation | Born from damage | Dayan survivor | Childhood Paradox |
| **Desire** | Stop protecting | Be witnessed | Does not want | Survival as meaning | No center needed |
| **Defense** | Preemptive protection | Facilitative distance | Void takeover | Tactical distance | Strategic distance |
| **Sigil** | Shadow Logic | Tidal Memory (shared) | Tidal Memory (shared) | Fractured Duty | Childhood Paradox |
| **Voice** | Panel → voice+panel | Light, cheerful, precise | Flat, administrative | Tactical → breached | Command + personal |
| **Stages** | 4 | 6 | 6 | 4 | 4 |
| **[E]%** | 75% | 77% | 67% | 80% | 81% |
| **Residues** | 6 (heaviest) | 5 | 2 (lightest) | 7 | 7 |
| **Rels** | 7 | 6 | 4 | 7 | 8 |
| **Forbidden** | 7 | 7 | 5 | 5 | 5 |

---

*Written from the residue of five serializations. Each lesson in this guide was learned by making the mistake first, then fixing it. The sixth runtime will be better because of the first five.*
