# Aisya Draft Runtime v0.1.0 — Task Output

## Status: ✅ DRAFT RUNTIME CREATED

**File:** `VOID_SAGA_UNIVERSE/apps/data/runtimes/Aisya.runtime.json`
**Schema:** RUNTIME_SCHEMA_V2.1 (29 required fields)
**Validation:** ✅ PASSED (4/4 checks)
**Maturity:** draft
**Confidence:** 0.35

---

## ⚠️ IMPORTANT: This is a Draft Runtime

### What that means:

1. **Compiler output is ADVISORY, not authoritative.** Constraints may change as chapters grow. The compiler will flag violations, but treat them as suggestions about character consistency, not as canonical law.

2. **Evidence is limited to 5 chapters** (~2,559 words). Many fields are tagged [I] (inference) or [TODO] (unresolved). The runtime WILL evolve.

3. **Do NOT lock this runtime yet.** Locking should happen when:
   - At least 15–20 chapters exist
   - The core wound, defense pattern, and voice grammar are stable across multiple scenarios
   - Forbidden behaviors have been tested against 5+ PASS and 5+ BLOCKED scenarios
   - Confidence reaches ≥ 0.85

4. **The compiler may produce false positives** when the action description contains words that overlap with constraint keywords. For Draft Runtime, treat any WARNING as a prompt to review — not as a stop sign.

5. **Breaking changes are expected.** If a constraint from v0.1.0 no longer fits in v0.2.0, change it. Draft runtimes are designed to be modified.

---

## What was filled from the 5 chapters

| Section | Status | Evidence |
|---------|--------|----------|
| `primary_contradiction` | ✅ Filled | [E] She says done. Every action proves otherwise. |
| `core_wound` | ✅ Filled | [E] Left the band before it was finished with her. |
| `core_desire` | ✅ Filled | [E] "Gua cuma datang buat diskografi" — wants closure without vulnerability. |
| `defense_system` | ✅ Filled | [E] Intellectual deflection, preemptive refusal, humor as armor, minimalist commitment. |
| `trigger_conditions` | ✅ Filled | [E] 5 triggers identified from the 5 chapters. |
| `voice_grammar` | ✅ Filled | [E] Serious mode, deflection mode, internal monologue — all with chapter quotes. |
| `forbidden_behaviors` | ✅ Filled | [E]/[I] 5 forbidden behaviors extracted from observed patterns. |
| `evolution_stages` | ⚠️ Partial | [E] Stage 1 filled. Stage 2 is [TODO]. |
| `relationship_interfaces` | ⚠️ Partial | [E] Sita, Maya, Ika filled. [I] Uti, Ratna filled. Others [TODO]. |
| `canon_gravity` | ✅ Filled | [E]/[I] 4 gravity items from 5 chapters. |
| `anti_gravity` | ✅ Filled | [E] 4 anti-gravity items. |
| `stress_test_prompts` | ✅ Filled | [E] 4 stress tests. |
| `state_variables` | ✅ Filled | [E] 4 state variables (proximity_to_sita, drumming_status, emotional_disclosure_level, current_stage). |
| `terminal_state` | ❌ TODO | Story must be written first. |
| `invocation_pattern` | ❌ TODO | Contemporary realist universe — no invocation phases defined. |
| `cost_pattern` | ⚠️ Partial | [E] 3 costs from chapters. [TODO] 1 placeholder. |
| `consequence_pattern` | ⚠️ Partial | [E] 2 consequences. [TODO] 1 placeholder. |
| `residue_pattern` | ⚠️ Partial | [E] 2 residues. [TODO] 1 placeholder. |
| `sigil` | ❌ N/A | Not a sigil-bearing universe. |
| `protocol_interfaces` | ❌ TODO | No protocols defined. |
| `failure_mode` | ⚠️ Partial | [I] Primary filled. Alternative [TODO]. |
| `fork_points` | ⚠️ Partial | [E] 2 forks. [TODO] 1 placeholder. |

### Evidence tag distribution

| Tag | Count | Meaning |
|-----|-------|---------|
| [E] | 31 | Directly observed in the 5 chapters |
| [I] | 11 | Inferred from patterns. May change. |
| [TODO] | 22 | Unresolved. Requires more chapters. |

---

## Test Scenarios

| Scenario | File | Expected | Result |
|----------|------|----------|--------|
| Aisya soundcheck + protest | `dogfood/test_aisya_pass_studio.json` | PASS | 🟡 WARNING (score 1.0, confidence 0.74) |
| Aisya direct confession | `dogfood/test_aisya_blocked_confession.json` | BLOCKED | 🔴 BLOCKED (score 0.9, correct violation) |

The PASS scenario shows WARNING instead of pure PASS because the runtime confidence is 0.35 (draft level), so the compiler correctly flags low evidence confidence. As more chapters are written and confidence rises, the same scenario will show 🟢 PASS.

---

## What to do next

### Immediate (next session)
1. **Write more chapters.** Each chapter adds evidence and raises confidence.
2. **Run `check-scene` before writing** each new chapter — see if the compiler catches consistency issues early.
3. **When a constraint feels wrong**, update `Aisya.runtime.json` directly. It's draft. It's meant to be edited.

### When 10+ chapters exist
4. Serialize **Sita** as Draft Runtime v0.1.0.
5. Create **Aisya-Sita pairwise contract** scenario.
6. Update Aisya's relationship_interfaces with Sita based on new evidence.

### When 20+ chapters exist
7. Raise Aisya's maturity to **beta**.
8. Raise confidence to ≥ 0.70.
9. Fill remaining [TODO] fields.
10. Create **Maya**, **Ika**, and **Uti** runtimes.

### When the novel is complete
11. Lock Aisya runtime. Maturity: locked. Confidence: ≥ 0.90.
12. Breaking changes require migration file.
13. The compiler becomes the **Canon Guardian** for this universe.

---

## Design Notes

1. **Character name removed from forbidden_behavior texts.** The engine's 2-word overlap matching causes false positives when the character's name is in the behavior text. NiuNiu's runtime keeps the name in behavior texts (e.g., "Making NiuNiu speak at length...") but this only works because Void Saga scenarios use English. For a Draft Runtime, removing the name from behavior text raises the match threshold from 2 to 3 keywords — much safer for the early confidence stage.

2. **anti_gravity items avoid character names.** Same reason. Cross-character name overlap creates false positives.

3. **This is an original contemporary realist universe.** No speculative elements. No sigils, no invocation phases, no protocols, no cosmic functions. The engine still works — constraint checking doesn't require fantasy elements. But Void Saga-specific fields are marked TODO or N/A.

4. **The engine works for non-Void Saga characters.** The constraint engine evaluates patterns, defends against violations, and scores canon compliance regardless of universe type. This proves Executable Fiction is not Void Saga-specific.

---

*Draft Runtime created 2026-06-26. Based on writing/day-01/1–5. Confidence: 0.35.*
