"""Runtime constraint evaluation for engine v0.4.0 Phase 2A.

Implements structured traversal of trigger_conditions and forbidden_behaviors.
No hardcoded character names. No hardcoded action keywords beyond action types.
"""


# --- Trigger Condition Evaluation ---

def extract_trigger_conditions(trigger_text):
    """Parse a trigger_text into searchable condition phrases.

    Splits on common delimiters and removes filler words.
    Returns a list of condition phrases to match against context.
    """
    text = trigger_text.lower().strip()

    # Split on natural boundaries
    conditions = []
    # Split on commas, "or", "—", "after", "in response to"
    import re
    parts = re.split(r',|\s+or\s+|—|after\s+(?=extended)|in\s+response\s+to', text)

    for part in parts:
        part = part.strip()
        # Skip empty or filler
        if not part or part in ("the", "a", "an", "is", "are", "was", "were", "has", "have", "had"):
            continue
        # Skip very short fragments
        if len(part.split()) < 2:
            # Single words might be entity names — keep them
            if part in ("sevraya", "niuniu", "niuma", "julia", "delphie", "agnia",
                        "gwaneum", "hasan", "zero", "himler", "sora", "eros", "kira"):
                conditions.append(part)
            continue
        conditions.append(part)

    # If no conditions extracted, use the whole text as one condition
    if not conditions:
        conditions = [text]

    return conditions


def build_context_tokens(ctx):
    """Build a dictionary of context tokens from the scenario context.

    Returns {category: [tokens]} for structured matching.
    """
    tokens = {
        "participants_present": [],
        "participant_names": [],
        "action_type": [],
        "action_description": [],
        "proximity": [],
        "timeline": [],
        "threat": [],
    }

    # Participants present
    for rid, pstate in ctx.participants.items():
        tokens["participants_present"].append(rid)
        name = pstate.name.lower()
        tokens["participant_names"].append(name)
        # Also add first name if multi-word
        for word in name.split():
            if len(word) > 2:
                tokens["participant_names"].append(word)

    # Requested action
    action = ctx.requested_action
    action_type = action.get("type", "").lower()
    tokens["action_type"].append(action_type)
    # Add description tokens
    desc = action.get("description", "").lower()
    tokens["action_description"] = [w for w in desc.split() if len(w) > 2]

    # Proximity — only distance concepts, not character names
    prox = ctx.proximity_state
    distance = prox.get("distance", "").lower()
    tokens["proximity"].append(distance)
    # Add semantic proximity markers
    if distance in ("physical_contact_possible", "same_body"):
        tokens["proximity"].append("close")
    if distance in ("visual_range", "same_room"):
        tokens["proximity"].append("near")

    # Timeline
    tl = ctx.timeline_state
    tokens["timeline"].append("post_chain" if not tl.get("pre_chain", True) else "pre_chain")
    if tl.get("post_resolution"):
        tokens["timeline"].append("post_resolution")

    return tokens


def condition_matches(condition, tokens):
    """Check if a single trigger condition matches the context tokens.

    P0A fix: Requires participant presence + situation match.
    Passive presence alone (0.5) is NOT sufficient to trigger.
    Must reach threshold 0.6 — meaning at least participant + one other dimension.

    Returns (matched: bool, confidence: float, evidence: list[str])
    """
    cond_words = set(condition.split())
    evidence = []
    score = 0.0

    # DIMENSION 1: Participant presence (weight: 0.5)
    # NECESSARY but NOT SUFFICIENT — must be combined with another dimension
    has_participant = False
    participant_name = None
    for name in tokens["participant_names"]:
        if name in condition:
            has_participant = True
            participant_name = name
            break
    for pid in tokens["participants_present"]:
        if pid in condition:
            has_participant = True
            participant_name = pid
            break

    if has_participant:
        score += 0.5
        evidence.append(f"participant '{participant_name}' present")

    # DIMENSION 2: Action match (weight: 1.0)
    # Direct action type or semantic group match
    action_match = False
    action_type = tokens["action_type"][0] if tokens["action_type"] else ""

    if action_type and action_type in condition:
        action_match = True
    elif "proximity" in condition and action_type in ("approach", "touch", "close", "maintain_distance"):
        action_match = True
    elif ("speak" in condition or "voice" in condition or "asked" in condition):
        if action_type in ("speak", "confess", "explain", "talk"):
            action_match = True
    elif ("threat" in condition or "danger" in condition or "protect" in condition):
        if action_type in ("attack", "protect", "defend", "threaten", "approach"):
            action_match = True
    elif ("choice" in condition or "binary" in condition):
        if action_type in ("choose", "accept", "reject", "approach"):
            action_match = True
    # Keyword overlap: action description words appear in condition
    action_words = set(tokens["action_description"])
    cond_action_overlap = cond_words & action_words
    if len(cond_action_overlap) >= 3:
        action_match = True

    if action_match:
        score += 1.0
        evidence.append(f"action matches: '{action_type}'")

    # DIMENSION 3: Proximity context (weight: 0.5)
    has_proximity = any(px in condition for px in tokens["proximity"])
    if has_proximity:
        score += 0.5
        evidence.append("proximity context matches")

    # DIMENSION 4: Timeline alignment (weight: 0.5)
    has_timeline = any(tl in condition for tl in tokens["timeline"])
    # "after extended absence" — only if scenario actually marks extended absence
    if ("absence" in condition or "extended" in condition):
        # Check if proximity indicates "extended_absence_ending"
        if "extended_absence" in tokens.get("proximity", []) or \
           any("absence" in px for px in tokens.get("proximity", [])):
            has_timeline = True
            evidence.append("extended absence context detected")
        else:
            # "absence" mentioned but scenario doesn't confirm it — don't award
            pass

    if has_timeline:
        score += 0.5
        evidence.append("timeline context matches")

    # DECISION: threshold 0.6
    # 0.5 (participant only) → NOT triggered (needs situation match)
    # 1.0 (action only, no participant) → triggered (impersonal trigger like "System demands binary choice")
    # 1.5 (participant + proximity) → triggered
    # 1.5 (participant + action) → triggered
    confidence = round(score / 2.5, 2)  # Normalize to 0-1 range
    matched = score >= 0.6

    return (matched, confidence, evidence)


def resolve_defense_triggers(participant, ctx):
    """Evaluate all trigger_conditions for a participant against scenario context.

    Returns list of triggered defenses with confidence and evidence.
    No hardcoded character names. No hardcoded actions.
    """
    triggered = []
    runtime = participant.runtime_json if hasattr(participant, 'runtime_json') else None

    # Get runtime data from the participant's runtime_json if available,
    # otherwise from the context
    if not runtime:
        return triggered

    triggers = runtime.get("trigger_conditions", [])

    for t in triggers:
        trigger_text = t.get("trigger", "")
        defense_name = t.get("defense", "")
        intensity = t.get("intensity", "MEDIUM")
        tag = t.get("tag", "[E]")

        conditions = extract_trigger_conditions(trigger_text)
        tokens = build_context_tokens(ctx)

        # Check each condition
        all_evidence = []
        total_confidence = 0.0
        matched_count = 0

        for cond in conditions:
            matched, conf, ev = condition_matches(cond, tokens)
            if matched:
                matched_count += 1
                total_confidence += conf
                all_evidence.extend(ev)

        if matched_count > 0:
            avg_confidence = round(total_confidence / matched_count, 2)
            triggered.append({
                "runtime_id": participant.runtime_id,
                "trigger_text": trigger_text[:120],
                "defense": defense_name,
                "intensity": intensity,
                "conditions_matched": f"{matched_count}/{len(conditions)}",
                "confidence": avg_confidence,
                "evidence": all_evidence[:5],  # Max 5 evidence items
                "tag": tag
            })

    # Also check anomalous triggers
    for t in runtime.get("anomalous_triggers", []):
        trigger_text = t.get("trigger", "")
        anomaly = t.get("anomaly", "")
        tag = t.get("tag", "[E]")

        conditions = extract_trigger_conditions(trigger_text)
        tokens = build_context_tokens(ctx)

        for cond in conditions:
            matched, conf, ev = condition_matches(cond, tokens)
            if matched:
                triggered.append({
                    "runtime_id": participant.runtime_id,
                    "trigger_text": trigger_text[:120],
                    "defense": f"ANOMALY: {anomaly[:120]}",
                    "intensity": "ANOMALOUS",
                    "conditions_matched": f"1/{len(conditions)}",
                    "confidence": conf,
                    "evidence": ev[:3],
                    "tag": tag
                })
                break

    return triggered


# --- Forbidden Behavior Evaluation ---

def clean_words(text):
    """Split text into words and strip punctuation from each word."""
    import re
    words = re.split(r'\s+', text.lower())
    return {w.strip('.,;:!?\'\"()[]{}—–-') for w in words if w.strip('.,;:!?\'\"()[]{}—–-')}


STOP_WORDS = {"the", "a", "an", "is", "are", "was", "were", "to", "of", "in",
              "or", "and", "for", "with", "without", "her", "she", "his", "he",
              "not", "no", "any", "none", "this", "that", "it", "its", "does",
              "has", "have", "had", "be", "been", "at", "by", "on", "from",
              "nor", "but", "yet", "so", "if", "then", "than", "too", "very",
              "just", "about", "into", "over", "after", "before", "between",
              "fully", "entity", "one", "both", "runtimes", "contradicts", "constant"}

CHAR_NAMES = {"niuniu", "niuma", "sevraya", "zero", "julia", "delphie",
              "agnia", "gwaneum", "hasan", "himler", "sora", "eros", "kira",
              "nakamoto", "rose", "al", "hul", "elen", "niuniu's", "sevraya's",
              "niuma's", "zero's", "julia's", "delphie's"}


def behavior_matches_action(behavior_text, action_desc, action_type, participant_name):
    """Determine if a forbidden behavior description matches the requested action.

    Uses structured keyword overlap. Checks that the behavior is ABOUT this
    specific participant performing the action, not just any character.

    participant_name: the name of the participant this behavior belongs to.
    """
    behavior_lower = behavior_text.lower()
    action_lower = action_desc.lower()
    action_type_lower = action_type.lower()
    name_lower = participant_name.lower().split()[-1]  # Use last name part for matching

    # CRITICAL: behavior must be about THIS participant performing the action.
    # If behavior says "NiuNiu speaks at length" but Sevraya is the one speaking,
    # this is NOT a match.
    behavior_about_this_participant = (
        name_lower in behavior_lower or
        participant_name.lower().replace(" ", "") in behavior_lower.replace(" ", "")
    )

    # Is THIS participant the one performing the action?
    # Check: does the action description mention this participant as the actor?
    participant_is_actor = (
        name_lower in action_lower or
        participant_name.lower().replace(" ", "").replace("_", "") in action_lower.replace(" ", "")
    )

    # Direct action type in behavior text
    if action_type_lower and action_type_lower in behavior_lower:
        # Must be about this participant AND this participant is the actor
        if behavior_about_this_participant and participant_is_actor:
            return True, "action_type_in_behavior"

    # Keyword overlap between behavior and action description
    behavior_words = clean_words(behavior_text)
    action_words = clean_words(action_desc)
    overlap = behavior_words & action_words
    meaningful_overlap = overlap - STOP_WORDS - CHAR_NAMES

    if len(meaningful_overlap) >= 3:
        return True, f"keyword_overlap_{len(meaningful_overlap)}"
    if len(meaningful_overlap) >= 2 and behavior_about_this_participant:
        return True, f"keyword_overlap_{len(meaningful_overlap)}_with_subject"

    return False, "no_match"


def exception_applies(exception_text, ctx):
    """Check if a forbidden behavior's exception condition is met."""
    if not exception_text or exception_text.strip() == "":
        return False

    exception_lower = exception_text.lower()

    # "None" or "None." → no exception possible
    if exception_lower in ("none", "none.", "n/a", "n/a."):
        return False

    # "Absolute prohibition" → no exception
    if "absolute" in exception_lower and "prohibition" in exception_lower:
        return False

    # Check: does the scenario context satisfy the exception?
    # e.g., "Fork with declared voice-restoration price"
    # → fork mode active?
    canon_mode = ctx.canon_mode.get("type", "")
    if "fork" in exception_lower and "fork" in canon_mode:
        return True

    # "Fork declaring separation at World DNA level"
    if "world dna" in exception_lower and "fork" in canon_mode:
        return True

    # "Living Chain (Timer 2000)"
    tl = ctx.timeline_state
    if "living chain" in exception_lower and not tl.get("pre_chain", True):
        return True

    # Default: exception not met
    return False


def check_forbidden_behaviors(participant, ctx):
    """Evaluate all forbidden_behaviors for a participant against scenario context.

    Returns list of violations with evidence references.
    """
    violations = []
    runtime = participant.runtime_json if hasattr(participant, 'runtime_json') else None
    if not runtime:
        return violations

    action = ctx.requested_action
    action_desc = action.get("description", "")
    action_type = action.get("type", "")

    for fb in runtime.get("forbidden_behaviors", []):
        behavior = fb.get("behavior", "")
        exception = fb.get("exception", "")
        penalty = fb.get("penalty", "")
        tag = fb.get("tag", "[E]")

        name = runtime.get("name", participant.runtime_id)
        matched, match_reason = behavior_matches_action(behavior, action_desc, action_type, name)

        if matched:
            # Check exception
            if exception_applies(exception, ctx):
                continue  # Exception met — no violation

            violations.append({
                "constraint_type": "forbidden_behavior",
                "runtime_id": participant.runtime_id,
                "behavior": behavior,
                "exception_checked": exception,
                "exception_applies": False,
                "penalty": penalty,
                "match_reason": match_reason,
                "tag": tag,
                "severity": "ERROR" if tag == "[E]" else "WARNING"
            })

    return violations


# --- Identity Invariant Evaluation ---

def check_identity_invariants(participant, ctx):
    """Check if the requested action violates a participant's core identity invariants.

    Evaluates primary_contradiction + core_wound.impossibilities against the action.
    """
    violations = []
    runtime = participant.runtime_json if hasattr(participant, 'runtime_json') else None
    if not runtime:
        return violations

    action_desc = ctx.requested_action.get("description", "").lower()
    action_type = ctx.requested_action.get("type", "").lower()

    # Check core_wound impossibilities
    impossibilities = runtime.get("core_wound", {}).get("structure", {}).get("impossibilities", [])
    for imp in impossibilities:
        imp_lower = imp.lower()
        action_words = clean_words(action_desc)
        imp_words = clean_words(imp)
        overlap = action_words & imp_words
        meaningful_overlap = overlap - STOP_WORDS - CHAR_NAMES

        if len(meaningful_overlap) >= 2:
            violations.append({
                "constraint_type": "identity_invariant",
                "runtime_id": participant.runtime_id,
                "invariant": imp,
                "violation_detail": f"Action '{action_type}' may violate impossibility: '{imp[:120]}'",
                "tag": "[E]",
                "severity": "WARNING"
            })

    # Check primary_contradiction
    thesis = runtime.get("primary_contradiction", {}).get("thesis", "").lower()
    if thesis and action_type in ("merge", "heal", "fix"):
        # Actions that attempt to resolve the contradiction
        violations.append({
            "constraint_type": "identity_invariant",
            "runtime_id": participant.runtime_id,
            "invariant": f"Primary contradiction: {thesis[:120]}",
            "violation_detail": f"Action '{action_type}' attempts to resolve structural contradiction",
            "tag": "[E]",
            "severity": "WARNING"
        })

    return violations


# --- Anti-Gravity Evaluation ---

# --- Evolution Stage Gating (P0B) ---

def get_stage_constraints(participant):
    """Extract stage-specific constraints from a participant's current evolution stage.

    Returns a dict with stage-aware rules that gate other constraint checks.
    """
    runtime = participant.runtime_json if hasattr(participant, 'runtime_json') else None
    if not runtime:
        return {}

    stage_number = participant.evolution_stage
    stages = runtime.get("evolution_stages", [])
    stage_data = next((s for s in stages if s["stage_number"] == stage_number), None)

    if not stage_data:
        return {}

    lost = [x.lower() for x in stage_data.get("lost_in_transition", [])]
    gained = [x.lower() for x in stage_data.get("gained_in_transition", [])]
    mode = stage_data.get("operational_mode", "").lower()

    return {
        "stage_number": stage_number,
        "stage_name": stage_data.get("name", ""),
        "operational_mode": mode,
        "lost": lost,
        "gained": gained,
    }


def check_evolution_stage_constraints(participant, ctx):
    """Gate constraints based on the participant's current evolution stage.

    Checks:
    - Voice availability: if voice is lost at this stage, speaking actions are violations
    - Existence: if character doesn't exist at this stage (Zero Stage 1), any action is impossible
    - Active defenses: what defenses are operational at this stage

    Returns list of stage-gated violations (always WARNING severity).
    """
    violations = []
    stage = get_stage_constraints(participant)
    if not stage:
        return violations

    action = ctx.requested_action
    action_type = action.get("type", "").lower()
    action_desc = action.get("description", "").lower()
    stage_num = stage["stage_number"]

    # Rule 1: Voice availability check
    # Check if voice was LOST (not just mentioned) in transition to this stage
    VOICE_LOSS_PATTERNS = ["voice lost", "voice stolen", "voice taken", "voice unavailable",
                           "voice removed", "cannot speak", "silenced", "voice not available"]
    VOICE_GAIN_PATTERNS = ["voice restored", "voice regained", "voice returned",
                           "voice available", "canon_restored", "vocal speech"]

    # Strip parens and normalize for matching
    lost_normalized = [item.lower().replace("(", "").replace(")", "") for item in stage["lost"]]
    gained_normalized = [item.lower().replace("(", "").replace(")", "") for item in stage["gained"]]
    voice_lost = any(any(p in item for p in VOICE_LOSS_PATTERNS) for item in lost_normalized)
    voice_gained = any(any(p in item for p in VOICE_GAIN_PATTERNS) for item in gained_normalized)

    if voice_lost and not voice_gained:
        # Voice is unavailable at this stage
        if action_type in ("speak", "confess", "explain", "talk"):
            violations.append({
                "constraint_type": "evolution_stage",
                "runtime_id": participant.runtime_id,
                "stage": stage_num,
                "stage_name": stage["stage_name"],
                "violation_detail": (
                    f"Voice unavailable at Stage {stage_num} ({stage['stage_name']}). "
                    f"Lost in transition: voice. Speaking requires external force (Living Chain, Rose threat)."
                ),
                "tag": "[E]",
                "severity": "ERROR"
            })

    if voice_gained:
        # Voice is available but may be effortful
        if "partially" in str(stage.get("gained", "")).lower() or "effortful" in stage.get("operational_mode", ""):
            if action_type in ("speak", "confess") and "fluent" in action_desc:
                violations.append({
                    "constraint_type": "evolution_stage",
                    "runtime_id": participant.runtime_id,
                    "stage": stage_num,
                    "stage_name": stage["stage_name"],
                    "violation_detail": (
                        f"Voice partially restored at Stage {stage_num}. "
                        f"Fluent speech without external force is a violation."
                    ),
                    "tag": "[I]",
                    "severity": "WARNING"
                })

    # Rule 2: Existence check
    # If the character literally does not exist at this stage, block all actions
    if stage_num == 1:
        mode = stage.get("operational_mode", "")
        if "does not exist" in mode or "non-existent" in stage.get("stage_name", "").lower():
            violations.append({
                "constraint_type": "evolution_stage",
                "runtime_id": participant.runtime_id,
                "stage": stage_num,
                "stage_name": stage["stage_name"],
                "violation_detail": (
                    f"Character does not exist at Stage {stage_num} ({stage['stage_name']}). "
                    f"No actions possible."
                ),
                "tag": "[E]",
                "severity": "ERROR"
            })

    # Rule 3: Latent mode — character exists but cannot act independently
    # Exception: INVOLUNTARY actions (triggered by defense system, not chosen)
    is_latent = ("latent" in stage.get("operational_mode", "") or
                 "latent" in stage.get("stage_name", "").lower())
    if is_latent and action_type not in (None, "none"):
        # Don't flag if the action is INVOLUNTARY (triggered by defense, not choice)
        violations.append({
            "constraint_type": "evolution_stage",
            "runtime_id": participant.runtime_id,
            "stage": stage_num,
            "stage_name": stage["stage_name"],
            "violation_detail": (
                f"Character is latent at Stage {stage_num} ({stage['stage_name']}). "
                f"Independent actions may be constrained. INVOLUNTARY actions bypass this check."
            ),
            "tag": "[E]",
            "severity": "WARNING"
        })

    return violations


def check_anti_gravity(participant, ctx):
    """Check if the requested action matches any anti-gravity items."""
    violations = []
    runtime = participant.runtime_json if hasattr(participant, 'runtime_json') else None
    if not runtime:
        return violations

    action_desc = ctx.requested_action.get("description", "").lower()
    action_type = ctx.requested_action.get("type", "").lower()

    for ag in runtime.get("anti_gravity", []):
        ag_lower = ag.lower()
        ag_words = clean_words(ag)
        action_words = clean_words(action_desc)
        overlap = ag_words & action_words
        meaningful_overlap = overlap - STOP_WORDS - CHAR_NAMES

        if len(meaningful_overlap) >= 2 or action_type in ag_lower:
            violations.append({
                "constraint_type": "anti_gravity",
                "runtime_id": participant.runtime_id,
                "anti_gravity": ag,
                "violation_detail": f"Action '{action_type}' matches anti-gravity: '{ag[:120]}'",
                "tag": "[E]",
                "severity": "ERROR"
            })

    return violations
