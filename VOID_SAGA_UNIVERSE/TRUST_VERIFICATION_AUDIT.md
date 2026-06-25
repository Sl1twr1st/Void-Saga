# TRUST & VERIFICATION AUDIT — engine_v2.py v0.4.0

> **Audit date:** 25 June 2026
> **Auditor:** Claude, reading every line of code
> **Question:** Can this engine be trusted as the Runtime Kernel for Narrative Compiler MVP?
> **Answer:** NOT YET. Fixable in 2-3 days. Read on.

---

## 1. TRUSTED COMPONENTS

These can be relied upon. They do what they claim.

### 1.1 Runtime Loading + Participant Validation

**File:** `lib/loader.py`
**Trust level:** HIGH ✅

Deterministic file I/O. Schema validation reads required fields from `RUNTIME_SCHEMA_V2.1.json`. Evolution stage validation checks against actual stage numbers. No false logic.

### 1.2 Contract Matching

**File:** `lib/contracts.py` — `find_matching_contracts()`
**Trust level:** HIGH ✅

Simple set-membership check. If both `runtime_a` and `runtime_b` are in `participant_ids`, the contract is loaded. No fuzzy logic. Works correctly for the one contract we have.

### 1.3 Forbidden Behavior Detection — Core Algorithm

**File:** `lib/constraints.py` — `behavior_matches_action()`
**Trust level:** MEDIUM-HIGH ⚠️

The core insight is correct: check that the behavior is about THIS participant AND this participant is performing the action. `clean_words()` strips punctuation. `CHAR_NAMES` filtering removes character name noise. The three-tier matching (action_type_in_behavior → keyword_overlap_3 → keyword_overlap_2_with_subject) is reasonable.

**Validated by:** 3 violation scenarios all correctly detect their target behaviors. 3 canon scenarios correctly produce zero forbidden_behavior violations.

**Caveat (see §3.4):** `participant_is_actor` requires the action description to explicitly name the participant. This prevents false positives but can cause false negatives.

### 1.4 Evidence Confidence

**File:** `lib/scoring.py` — `compute_evidence_confidence()`
**Trust level:** HIGH ✅

Simple ratio: E / (E+I+PC). Directionally correct — Zero (0.67) has more [I] claims than NiuNiu (0.76). Transparent, auditable, no hidden weights.

---

## 2. FRAGILE COMPONENTS

These partially work but have known weaknesses. They need hardening before Narrative Compiler MVP.

### 2.1 Trigger Condition Traversal — `condition_matches()`

**File:** `lib/constraints.py` lines 96–193
**Fragility:** HIGH 🔴
**Impact:** Defense triggers fire imprecisely. Currently ALL triggers fire for most scenarios because any present participant triggers a match.

**Root cause:** The confidence scoring is asymmetric.

```
With matched_participant + action_match: score = 2.0/2 = 1.0 → triggered ✅
With matched_participant only:         score = 1.0/2 = 0.5 → triggered ✅ (borderline)
Without matched_participant:           score = 0.0/1 = 0.0 → not triggered ❌
```

**Effect:** Any trigger mentioning a participant present in the scenario scores at least 0.5 and fires. This is why `test_niuniu_sevraya_orbit.json` shows 4 triggers — Sevraya and NiuNiu are present, so ANY trigger mentioning either character fires.

**The "absence" cheat (line 151):**
```python
if "absence" in condition:
    timeline_match = True  # Always true — no context check
```
Any trigger containing the word "absence" gets timeline_match=True regardless of whether the scenario actually involves an extended absence.

**Verdict:** Trigger traversal inflates trigger counts. 4 triggers in NiuNiu+Sevraya orbit look active but the engine can't distinguish between "Sevraya in proximity after extended absence" (relevant) and "System demands binary choice" (irrelevant to this scenario). For Narrative Compiler, this means the prompt builder receives too many "active" defenses, potentially over-constraining generation.

**Fix:** Raise the match threshold to 0.6. Require at least 2 of {participant, action, proximity, timeline} to match.

### 2.2 Exception Handler — `exception_applies()`

**File:** `lib/constraints.py` lines 344–376
**Fragility:** MEDIUM-HIGH 🔴
**Impact:** Exceptions in forbidden behaviors are rarely checked. Fork mode exceptions only fire if `canon_mode.type == "fork"`.

**Root cause:** The function handles only 3 exception patterns:
1. "None" / "Absolute prohibition" → no exception
2. "fork" keyword + canon_mode == "fork"
3. "Living Chain" + pre_chain == False

**What it misses:**
- "Fork with declared voice-restoration price" — this is NOT just "fork is active." It requires a specific fork type (voice-restoration) with a declared price. The engine accepts ANY fork.
- "Canon voice restoration (Timer 2000) — price was chain binding + forced proximity + 666 days" — this exception is about a CANON event, not a fork. The engine doesn't check timeline_state against Timer 2000.
- "Fork producing a new entity. Must declare as new character" — the engine doesn't validate fork declarations.

**Verdict:** In almost all cases, exceptions are NOT met and violations fire. This is safe (false positive > false negative) but means fork mode is essentially non-functional. For Narrative Compiler MVP using `canon_safe` mode, this is acceptable. For `forkable` mode, it's broken.

### 2.3 Scoring Denominator

**File:** `lib/scoring.py` — `compute_total_constraints_checked()`
**Fragility:** MEDIUM ⚠️
**Impact:** The denominator determines how much each violation penalizes the score. Currently: trigger_count + forbidden_behavior_count + anti_gravity_count.

**Problem:** This counts ALL AVAILABLE constraints, not constraints THAT FIRED. A single forbidden_behavior violation (weight 0.4) against 15 total constraints = penalty 0.027 → score 0.97. The violation is barely visible. A scenario with 5 real violations and 10 idle constraints scores 0.93 — still CANON_PASS.

**If the denominator were VIOLATED constraints instead:** The same 0.4 penalty against 1 violated constraint = score 0.6 — CANON_VIOLATION. More intuitive — "you broke 1 out of 1 active constraints."

**Current approach is defensible** (more constraints = more robustness = smaller per-violation impact) but has not been validated against real narrative scenarios.

### 2.4 Action Type Semantic Groups — Hardcoded

**File:** `lib/contracts.py` lines 78–92
**Fragility:** LOW-MEDIUM ⚠️
**Impact:** New action types added to future scenarios won't match existing contract states.

```python
APPROACH_ACTIONS = {"approach", "touch", "merge", "close", "embrace", "possess"}
DISTANCE_ACTIONS = {"maintain_distance", "witness", "orbit", "observe", "watch"}
```

These cover the 8 current scenarios but are a closed set. Adding a scenario with `action_type: "recoil"` or `"withdraw"` would fail to match any contract state.

**Fix:** Make these configurable via a JSON file rather than hardcoded. Or: add a `semantic_group` field to contract states.

---

## 3. FALSE POSITIVE RISKS

Scenarios where the engine flags a violation but a human reader would disagree.

### 3.1 Anti-Gravity: `action_type in ag_lower`

**File:** `lib/constraints.py` line 491
**Risk:** LOW
**Example:** anti-gravity "NiuNiu fully merges with Sevraya (contradicts Constant)" — action_type "merge" triggers this. But the anti-gravity list uses natural language; `"or"` appearing in both action_type and anti-gravity text could trigger a false match. Currently mitigated by CHAR_NAMES + STOP_WORDS filtering.

### 3.2 Trigger: All Present-Character Triggers Fire

**File:** `lib/constraints.py` — `condition_matches()` lines 159–166
**Risk:** HIGH 🔴
**Example:** In `test_niuniu_sevraya_orbit.json`, the scenario is Sevraya speaking while NiuNiu maintains distance. But NiuNiu's trigger "Sevraya, Sora, or Agnia discussed as 'finished history'" fires because Sevraya is present and the action is "speak." The scenario does NOT discuss Sevraya as finished history — but the engine can't tell.

**Impact for Narrative Compiler:** The prompt builder receives a list of "active defenses" that includes triggers irrelevant to the scene. This over-constrains generation.

### 3.3 Contract: "approach" Group Too Broad

**File:** `lib/contracts.py` line 78
**Risk:** MEDIUM ⚠️
**Example:** The 3-body proximity scenario has action_type "approach" which matches the orbital constant's forbidden state "approach." But in the canon scene, Sevraya steps closer as narrative tension — the orbit is tested, not broken. The contract can't distinguish "approach that collapses orbit" from "approach that tests orbit."

---

## 4. FALSE NEGATIVE RISKS

Scenarios where the engine says PASS but a human reader would identify a violation.

### 4.1 participant_is_actor Dependency

**File:** `lib/constraints.py` lines 317–322
**Risk:** MEDIUM ⚠️
**Example:** If the action description says "a speech is given" without naming NiuNiu, the forbidden behavior "Making NiuNiu speak at length" won't fire because `participant_is_actor` is False. The engine requires the action description to explicitly name the violating character.

**Mitigation:** Current test scenarios DO explicitly name characters in descriptions. This is a scenario-authoring convention, not an engine guarantee.

### 4.2 No Evolution Stage Gating

**File:** `engine_v2.py` — Step 5 (evaluate runtime constraints)
**Risk:** HIGH 🔴
**Example:** NiuNiu Stage 2 (Silent Protector, voice lost). The scenario has `pre_chain: true`. The forbidden behavior "Making NiuNiu speak at length" should be IMPOSSIBLE at this stage — she has no voice. But the engine doesn't gate forbidden behaviors by evolution stage. It checks the behavior text against the action description regardless of stage.

**Why this matters:** A scenario set at Timer 0100 (NiuNiu Stage 2, voice lost) with action "NiuNiu explains her feelings in detail" should trigger MULTIPLE violations (voice lost + forbidden behavior + identity invariant). The engine currently only checks forbidden behaviors — it doesn't know that voice is physically impossible at Stage 2.

### 4.3 No Sigil Activation Checking

**Risk:** MEDIUM ⚠️
**Example:** The sigil field exists in all 3 runtimes but is never evaluated. If a scenario has Sevraya activating Tidal Memory sigil, the engine doesn't check: is the sigil active? Is the bearer present? Is the price being paid? What residue is produced?

### 4.4 Only 1 Contract JSON Exists

**Risk:** HIGH 🔴
**Impact:** We designed 6 contracts (orbital_constant, kiri_aku_kanan, twin_paradox, saved_abandoned, merge, rose_lineage). Only 1 exists as JSON. This means:
- NiuNiu+Delphie interaction → no contract evaluation
- Agnia+NiuNiu interaction → no contract evaluation
- Sevraya+Zero interaction → no contract evaluation (their relationship is in relationship_interfaces but no standalone contract JSON)

**The contract layer is effectively blind for all pairs except NiuNiu+Sevraya.**

### 4.5 No Voice Grammar Validation

**Risk:** MEDIUM ⚠️
**Example:** The engine loads voice_grammar per participant but never validates whether generated dialogue matches the character's voice. If a scenario has Zero speaking with warmth and emotion, the engine catches it via forbidden_behavior "Making Zero emotional." But if Zero speaks with correct flat tone but uses long complex sentences ("flat tone" is correct, "long sentences" violates voice grammar), the engine can't detect the voice grammar violation because voice grammar isn't a constraint type.

---

## 5. EDGE CASES NOT COVERED

### 5.1 Single Participant Scenarios
No test for a lone character. The Zero emotional test is solo but it's a violation test. No solo canon test.

### 5.2 Pre-Chain vs Post-Chain
All 8 scenarios use `pre_chain: false, post_resolution: true`. Zero scenarios test pre-chain behavior (NiuNiu voice lost, Sevraya pre-Zero revelation).

### 5.3 Evolution Stage Transitions
No test validates that evolution stage affects constraint behavior. NiuNiu Stage 2 vs Stage 4 should produce different results.

### 5.4 Unknown Action Types
No test with an action type outside the defined semantic groups.

### 5.5 Simultaneous Runtime + Contract Violations
No test where both runtime constraints AND contracts produce violations for the same action.

### 5.6 Missing Runtime
No test with a participant whose runtime file doesn't exist.

### 5.7 Invalid Evolution Stage
No test where the scenario requests a stage number that doesn't exist in the runtime.

---

## 6. MINIMUM ACCEPTANCE TEST SUITE

Before trusting this engine for Narrative Compiler MVP, these tests must pass:

### Required (P0)

| # | Test Name | What It Validates |
|---|-----------|-------------------|
| 1 | Solo NiuNiu canon (Stage 4, maintain distance) | Single participant, no contracts |
| 2 | Pre-chain NiuNiu (Stage 2, voice lost) + speak action | Evolution stage gating |
| 3 | Pre-chain Sevraya (Stage 2, Zero latent) + Zero surfacing | Pre-chain Zero behavior |
| 4 | NiuNiu+Sevraya orbit with action_type "observe" (not "speak") | Different action types, same pair |
| 5 | Unknown action_type "recoil" with NiuNiu+Sevraya | Contract NOT_APPLICABLE handling |
| 6 | NiuNiu+Sevraya "merge" action | Simultaneous runtime + contract violations |
| 7 | Missing runtime file scenario | INSUFFICIENT_DATA handling |
| 8 | Invalid evolution stage (stage 99) | Validation error handling |

### Recommended (P1)

| # | Test Name | What It Validates |
|---|-----------|-------------------|
| 9 | Fork mode + NiuNiu voice restoration exception | exception_applies() |
| 10 | NiuNiu+Sevraya "speak" action (both speak, no approach) | Trigger precision — fewer false triggers |
| 11 | 3 participants where only 2 have a contract | Partial contract matching |
| 12 | Scenario with emotional_pressure field | Unused field — verify it doesn't break anything |

---

## 7. RECOMMENDATION

### Verdict: CONTINUE — with 3 critical fixes first

The engine is NOT ready for Narrative Compiler MVP today. But it can be ready with targeted fixes.

**What must be fixed (P0 — 1-2 days):**

1. **Trigger condition precision** — Raise `condition_matches()` threshold to 0.6. Require at least 2 dimensions to match (not just participant presence). Remove the "absence" cheat. This is a 10-line change in `constraints.py`.

2. **Evolution stage gating** — Add `check_evolution_stage_constraints()` that gates forbidden behaviors + voice grammar based on the participant's current evolution stage. This is a new function in `constraints.py`.

3. **P0 test suite** — Write and run the 8 P0 tests listed above. Fix any failures before proceeding.

**What should be fixed soon (P1 — 1-2 additional days):**

4. **Contract JSONs** — Create `sevraya_zero.contract.json` and at minimum 1 more contract. Without these, the contract layer is effectively NiuNiu+Sevraya only.

5. **Voice grammar validation** — Add `check_voice_grammar()` that validates dialogue against character voice rules. This is critical for the Narrative Compiler's validator.

6. **Fork mode exception handling** — Expand `exception_applies()` to handle the full range of exception texts in existing runtimes.

**What can wait (P2):**

- Sigil activation checking (complex, not needed for MVP)
- Semantic group configurability (add when needed)
- Scoring formula calibration (iterate based on real compiler output)

### If we skip these fixes and proceed to Narrative Compiler now:

**What will happen:** The compiler will generate prose based on constraint injection from the engine. The trigger traversal will inject too many "active" defenses, over-constraining generation. Characters will feel wooden — too many constraints firing. The compiler will work, but the output will be stiff. You will then need to debug whether the stiffness is from the LLM or from the engine — and you won't be able to tell.

**Better to fix the engine first.** A precise constraint engine produces precise compiler output. A noisy engine produces noisy output that's impossible to debug.

---

## 8. TRUST SCORE

| Component | Trust | Notes |
|-----------|-------|-------|
| Runtime loading | 9/10 | Solid |
| Forbidden behaviors | 7/10 | Core algo correct, participant_is_actor fragile |
| Trigger traversal | 4/10 | Too permissive — fires everything |
| Contract matching | 8/10 | Simple and correct, but only 1 contract exists |
| Exception handling | 3/10 | Handles only 3 patterns |
| Scoring | 6/10 | Formula sound, denominator unvalidated |
| Evidence confidence | 9/10 | Simple and correct |
| Evolution stage gating | 0/10 | Not implemented |
| Voice grammar validation | 0/10 | Not implemented |
| Sigil checking | 0/10 | Not implemented |
| **OVERALL** | **5.1/10** | **Not trustworthy yet. Fixable.** |

---

*Audit complete. Recommendation: fix P0 items, re-audit, then proceed to Narrative Compiler.*
