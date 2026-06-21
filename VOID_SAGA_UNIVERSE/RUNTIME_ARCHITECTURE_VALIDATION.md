# RUNTIME ARCHITECTURE VALIDATION

**Reference implementation:** `characters/NiuNiu.runtime.md` v2.0.0
**Architecture:** Runtime Architecture v2.2
**Validator:** Runtime Architect (Claude)
**Date:** 2026-06-21
**Status:** Architecture stress-test complete — no architecture changes made

---

## Executive Summary

Architecture v2.2 survived its first reference implementation. **12/12 sections were successfully populated** from canon evidence. **No section was impossible to write.** However, the implementation exposed **8 structural issues** across four categories: ambiguity, overlap, simulation-readiness, and validation gaps.

**Severity distribution:**
- Critical: 0 (architecture is functional)
- High: 2 (Identity Invariants vs Canon Gravity boundary, Defense Pattern format for simulation)
- Medium: 4 (Core Desire inference, Fork-Sensitive range specification, State Variable Registry location, Voice Grammar machine-readability)
- Low: 2 (Continuity Hooks redundancy, Trigger Condition NLP dependency)

---

## Section-by-Section Findings

### 1. Identity Invariants

**Easy to populate.** NiuNiu has five clean invariants extracted from 25 Timers of evidence. The format (numbered, one-sentence claims) forced precision.

**Issue: Boundary with Canon Gravity.** Invariant #5 ("She protects a Rose-lineage figure") and Gravity #1 ("She protects a Rose-lineage figure without being asked") are nearly identical. The invariant says WHAT she is. The gravity says WHERE she tends. But for NiuNiu, protection IS both — it's definitional AND gravitational. The architecture doesn't specify what to do when an invariant and a gravity describe the same behavior from different angles.

**Recommendation:** Add a rule: *If a behavior qualifies as an Identity Invariant, it should NOT be restated as Canon Gravity unless the gravity adds a specific OUTCOME not captured by the invariant.* Invariant = "She protects." Gravity = "She protects AND this protection resolves into orbital distance, not merge." The gravity must specify the endpoint, not just the behavior.

**Severity:** HIGH — will recur for every character whose core behavior IS their trajectory.

### 2. Core Wound

**Easy to populate.** NiuNiu's wound is well-documented. The "wound structure (not event)" subsection was essential — it forced separation of psychological damage from plot events.

**No issues.**

### 3. Core Desire

**Moderately difficult.** Canon provides behavioral evidence but rarely states desire directly. NiuNiu's Node II confession ("Aku tidak tahu bagaimana berhenti membayangi seorang Rose") was the only explicit desire statement in the entire canon. For characters without such a confession, this section will require significant inference.

**Issue: Inference dependency.** Future runtime authors for characters like Hasan (who never confesses desire directly) or Kira (who narrates, never introspects) will struggle. The architecture assumes canon provides desire evidence. For some characters, it does not.

**Recommendation:** Add guidance: *If canon provides no explicit desire statement, state the desire that best explains the character's observed behavior, and mark it [INFERRED].* This distinguishes evidence-based from inference-based desires without blocking implementation.

**Severity:** MEDIUM — affects characters with limited interiority in canon.

### 4. Defense Patterns

**Easy to populate.** The WHEN → THEN // COST format worked well. NiuNiu's defenses are highly patterned and canon-rich.

**Issue: Machine-readability.** The format is human-readable but not parseable. A simulation system cannot execute `WHEN: Someone she protects is positioned as passive victim` without NLP. The triggers are semantic, not syntactic.

**Recommendation:** Do NOT change the format — semantic triggers are the correct level of abstraction for a human-authored runtime. But ADD a companion section for simulation-facing runtimes: **Trigger Signatures** — machine-detectable proxies. Example:

```
HUMAN TRIGGER: Someone she protects is positioned as passive victim
SIM PROXY: target.agency_level < 0.3 AND target.threat_proximity > 0.7
```

This would live in a simulation protocol, not in the runtime itself — the runtime stays human-readable, and the simulation layer maps semantic triggers to detectable signals.

**Severity:** HIGH — affects all simulation/chat/game releases. But fix belongs in a simulation protocol, not the runtime architecture.

### 5. Trigger Conditions

**Easy to populate.** Same format strengths and NLP weaknesses as Defense Patterns.

**Issue: Intensity scale is underspecified.** LOW/MEDIUM/HIGH/CRITICAL are used but never defined. Does HIGH mean "always activates this defense" or "activates with visible effort to suppress"? Different architects will use the scale differently.

**Recommendation:** Define the intensity scale in RUNTIME_PROTOCOL.md:
- LOW: Defense activates but can be overridden by circumstance.
- MEDIUM: Defense activates reliably. Character shows awareness of it.
- HIGH: Defense activates immediately. Character may not be aware of it.
- CRITICAL: Defense overrides all other priorities. Character cannot suppress it.

**Severity:** MEDIUM — consistency issue across future runtimes.

### 6. Stable Traits

**Easy to populate.** Somatic Signature and Voice Grammar were direct lifts from the old runtime, enriched with new canon evidence. Relationship Signature was new and worked well as a compact reference.

**Issue: Relationship Signature vs Trigger Conditions overlap.** "Protect Delphie at maximum priority" appears in both the Relationship Signature (as a behavioral rule) AND Trigger Conditions (as a CRITICAL trigger). The information is not contradictory, but it is duplicated — and future edits risk desynchronization.

**Recommendation:** Relationship Signature should be a SUMMARY. Trigger Conditions should be the SPECIFICATION. The relationship signature says WHAT. The trigger says WHEN and HOW. The architecture already supports this distinction but the implementation blurred it. Add a note: *Trigger Conditions are authoritative for behavior. Relationship Signature is a convenience index.*

**Severity:** LOW — duplication is harmless if both sections are maintained together.

### 7. Unstable Traits

**Easy to populate.** The FROM → TO // TRIGGER format was effective. NiuNiu has five clean unstable traits with clear transition events.

**No issues.**

### 8. Evolution Stages

**Easy to populate.** NiuNiu has four distinct stages with clear triggers. The State Variable Registry table was useful for compact reference.

**Issue: State Variable Registry location.** The registry is embedded in Section 8 (Evolution Stages) per v2.1 spec. But during implementation, I found myself wanting to reference it from Section 10 (Fork-Sensitive Traits) and Section 7 (Unstable Traits). Having it buried in Section 8 makes cross-referencing awkward.

**Recommendation:** Consider extracting the State Variable Registry as a standalone compact table AFTER Section 8, or as an appendix within the runtime. It is the most cross-referenced artifact in the entire document. Alternatively: keep it in Section 8 but add a one-line pointer from Sections 7 and 10: `See Section 8 (State Variable Registry) for full variable states.`

**Severity:** MEDIUM — navigation friction, not architectural flaw.

### 9. Canon Gravity

**Easy to populate for NiuNiu** because her patterns are strong. Will be harder for characters with less screen time.

**Issue: Pull strength estimates are intuition, not data.** "STRONG (90%+)" is a guess. There is no empirical basis for these numbers until multiple forks exist and their outcomes can be analyzed. For now, these are architectural promises, not measured values.

**Recommendation:** Add a note: *Pull strength estimates are initial hypotheses. They should be revised after at least 3 forks explore the gravity in question. After 10+ forks, percentages should be replaced with observed frequencies.* This frames gravity as falsifiable rather than declared.

**Severity:** LOW — the architecture acknowledges this is speculative. No change needed, just documentation.

### 10. Fork-Sensitive Traits

**Moderately difficult.** The RANGE field was the hardest to specify. How wide is "wide enough" for voice restoration timing? I used narrative anchors (Dayan, chain, touch) rather than quantitative ranges, which feels right for a narrative system but wrong for a simulation one.

**Issue: RANGE specification format is inconsistent.** Some ranges are event-anchored ("Never restored → restored at Dayan → restored by chain"). Others are qualitative ("Complete suppression → panel-only hints → brief vocal admissions"). A simulation system cannot parse either.

**Recommendation:** Accept that Fork-Sensitive Traits are narrative-facing, not simulation-facing. For simulation, a separate **Tunable Parameters** document should map narrative ranges to quantitative sliders. The runtime stays human-readable; the simulation layer provides the numerical interface. This is the same pattern as Defense Patterns → Trigger Signatures.

**Severity:** MEDIUM — same simulation gap as Defense Patterns / Trigger Conditions.

### 11. Forbidden Behaviors

**Easy to populate.** The FORBIDDEN / EXCEPTION / PRICE format was effective. NiuNiu produced 9 forbidden behaviors with clear boundaries.

**Issue: PRICE specification is narrative, not quantitative.** "Must show what was lost when fluency was gained" is a rubric, not a validation check. A fork author might believe they showed the cost when a reviewer disagrees. This is inherent to narrative systems — cost is subjective — but it means Forbidden Behaviors cannot be automatically validated.

**Recommendation:** Accept this limitation. Forbidden Behaviors are HUMAN-VALIDATED constraints. A simulation system can check "did the character do X?" (binary) but cannot check "was the narrative price paid?" (judgment). The architecture should explicitly state: *Forbidden Behavior compliance is validated by human review, not automation.* This is not a bug — it's a feature boundary.

**Severity:** LOW — accepted limitation.

### 12. Possible Fork Points

**Easy to populate.** NiuNiu has six rich fork points with clear divergence events.

**Issue: GRAVITY RESISTANCE is the most speculative field in the entire architecture.** "EXTREME" vs "HIGH" resistance is a judgment call with no empirical basis. Two architects reviewing the same fork point may disagree on resistance level.

**Recommendation:** Add a companion field: **RESISTANCE RATIONALE.** A one-sentence explanation of WHY this resistance level was chosen. Example: `GRAVITY RESISTANCE: EXTREME. RATIONALE: Binary refusal is an Identity Invariant (Section 1.3). Changing it produces a different character, not a variant.` This makes the judgment auditable even if it remains subjective.

**Severity:** LOW — the rationale field makes the judgment transparent.

---

## Cross-Cutting Findings

### Finding 1: The Human/Simulation Boundary

The most persistent pattern across all issues: **the runtime architecture is optimized for human authorship, not machine consumption.** Defense Patterns use semantic triggers. Canon Gravity uses intuitive percentages. Forbidden Behaviors use narrative prices. Voice Grammar is a style guide.

This is CORRECT for the architecture's primary purpose (preserving identity across forks) but creates friction for simulation/chat/game releases.

**Solution (not an architecture change):** The Release layer should include a **Simulation Mapping** step. When assembling a simulation release, a simulation protocol maps:
- Semantic triggers → detectable signals
- Narrative ranges → quantitative sliders
- Voice grammar → output constraints (max sentence length, vocabulary filters, panel/text ratio)
- Canon gravity → attractor weights

The runtime stays human-readable. The simulation protocol provides the machine-readable interface. This is a Release concern, not a Runtime concern — the architecture already supports this through the five-layer stack.

### Finding 2: The Invariant/Gravity Boundary

Identity Invariants and Canon Gravity overlap when a character's core behavior IS their trajectory. The architecture defines them as separate sections but doesn't provide a tiebreaker rule for when they describe the same phenomenon.

**Solution (architecture clarification):**
- Invariants define WHAT the character IS. "She protects before being asked."
- Gravity defines WHERE this invariant TENDS. "This protection resolves into orbital distance, not merge."
- If a gravity restates an invariant without adding trajectory information, it is redundant and should be removed.

### Finding 3: The Inference Gap

Core Desire, Canon Gravity pull strengths, and Fork-Sensitive RANGE values required significant inference beyond canon evidence. This is not a flaw — it's the point of a runtime (compressing identity, not summarizing canon). But the architecture should distinguish EVIDENCED claims from INFERRED claims.

**Solution (metadata convention):** Add `[E]` (evidenced) or `[I]` (inferred) tags to claims that are not directly stated in canon. Example:

```
GRAVITY: She ends in permanent orbit with Sevraya. [E] — confirmed Timer 2200 LOG_062, LOG_066
GRAVITY: She never fully explains her feelings. [I] — inferred from behavior; no canon statement exists
```

### Finding 4: Continuity Hooks Are Redundant But Useful

The Continuity Hooks section restates facts already distributed across Invariants, Stable Traits, Evolution Stages, and Forbidden Behaviors. For NiuNiu, 13/14 hooks are restatements.

However, they serve a distinct function: **a single-point validation checklist.** When reviewing a fork, you don't want to scan 12 sections to verify all facts are preserved. You want one list.

**Recommendation:** Keep Continuity Hooks. Accept the redundancy. Add a note: *This section is intentionally redundant. It exists as a validation checklist, not a source of truth. If a hook contradicts an earlier section, the earlier section is authoritative.*

---

## Architecture Scorecard

| Section | Populability | Ambiguity | Simulation Readiness | Validation Readiness |
|---------|-------------|-----------|---------------------|---------------------|
| 1. Identity Invariants | ✅ Easy | ⚠️ Boundary with Gravity | ✅ Binary check | ⚠️ Human validation only |
| 2. Core Wound | ✅ Easy | ✅ Clear | ✅ Structural | ✅ Canon-backed |
| 3. Core Desire | ⚠️ Moderate | ⚠️ Inference-dependent | ⚠️ Not machine-actionable | ❌ Subjective |
| 4. Defense Patterns | ✅ Easy | ✅ Clear | ❌ Semantic triggers | ⚠️ Human validation |
| 5. Trigger Conditions | ✅ Easy | ⚠️ Intensity scale | ❌ NLP-dependent | ⚠️ Human validation |
| 6. Stable Traits | ✅ Easy | ⚠️ Overlap with Triggers | ⚠️ Voice grammar is style | ✅ Observable |
| 7. Unstable Traits | ✅ Easy | ✅ Clear | ✅ Trackable | ✅ Observable |
| 8. Evolution Stages | ✅ Easy | ⚠️ Registry location | ✅ State machine | ✅ Stage-gated |
| 9. Canon Gravity | ⚠️ Moderate | ❌ Pull strength speculative | ❌ Percentages not actionable | ❌ Requires fork data |
| 10. Fork-Sensitive Traits | ⚠️ Moderate | ⚠️ Range specification | ❌ Narrative ranges | ❌ Subjective |
| 11. Forbidden Behaviors | ✅ Easy | ⚠️ Price is narrative | ❌ Price not machine-checkable | ⚠️ Binary + human review |
| 12. Possible Fork Points | ✅ Easy | ❌ Resistance speculative | ❌ Not actionable | ❌ Requires fork data |

**Legend:**
- ✅ = Section works as designed
- ⚠️ = Section works but has documented friction
- ❌ = Section requires human judgment or future data; cannot be fully automated

---

## Recommendations

### Do now (no architecture change):

1. **Add [E] / [I] tags** to Core Desire and Canon Gravity claims to distinguish evidenced from inferred.
2. **Add RESISTANCE RATIONALE field** to Possible Fork Points.
3. **Define intensity scale** (LOW/MEDIUM/HIGH/CRITICAL) in RUNTIME_PROTOCOL.md.
4. **Add redundancy note** to Continuity Hooks.
5. **Clarify Invariant vs Gravity boundary** in architecture document: invariants define WHAT, gravity defines WHERE the invariant TENDS.

### Do when scaling to additional runtimes:

6. **Create Simulation Mapping Protocol** as a Release-layer document. Maps human-readable runtime fields to machine-actionable signals. This is the bridge between the runtime architecture and simulation/chat/game releases.
7. **Extract State Variable Registry** as a standalone appendix within each runtime, referenced from Sections 7, 8, and 10.
8. **After 3+ runtimes exist**, audit Canon Gravity claims for cross-character consistency.

### Architecture is ready for:

- Writing additional character runtimes (Julia, Delphie, Sevraya, Agnia, Gwaneum, etc.)
- Writing Collective Runtimes (The Merge, Living Chain, Twin Paradox, NiuNiu-Sevraya Constant)
- Creating the first Release manifests
- Prototyping simulation mappings

---

## Verdict

**Architecture v2.2 passes its first stress test.** All 12 sections are functional. The 5-layer stack (World DNA → Protocols → Runtimes → Fork Manifests → Releases) correctly separated concerns. The identity-compression distinction held: NiuNiu.runtime.md describes who NiuNiu IS across timelines, not what happened to her in one timeline.

The exposed issues are simulation-readiness gaps, not architectural flaws. They are correctly addressed at the Release layer (Simulation Mapping Protocol), not the Runtime layer. The runtime should stay human-readable. The simulation interface should bridge human → machine.

**Proceed to next runtime.**
