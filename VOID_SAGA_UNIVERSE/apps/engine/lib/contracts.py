"""Pairwise contract evaluation for engine v0.4.0 Phase 2B.

Loads standalone contract JSONs, matches them to participant pairs,
evaluates scenario actions against allowed/forbidden states and violation rules.
"""

import json
import os

CONTRACT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "contracts")


def load_contract(contract_id):
    """Load a single contract JSON by ID. Returns (data, error)."""
    path = os.path.join(CONTRACT_DIR, f"{contract_id}.contract.json")
    if not os.path.exists(path):
        return None, f"Contract file not found: {path}"
    with open(path, "r") as f:
        return json.load(f), None


def load_all_contracts():
    """Load all contract JSONs from the contracts directory. Returns list of contracts."""
    contracts = []
    if not os.path.exists(CONTRACT_DIR):
        return contracts
    for filename in sorted(os.listdir(CONTRACT_DIR)):
        if filename.endswith(".contract.json"):
            contract, err = load_contract(filename.replace(".contract.json", ""))
            if not err:
                contracts.append(contract)
    return contracts


def find_matching_contracts(participant_ids, all_contracts):
    """Find contracts that match any pair of participants.

    A contract matches if both its runtime_a and runtime_b are in participant_ids.
    Returns list of (contract, participant_pair) tuples.
    """
    matches = []
    pid_set = set(participant_ids)

    for contract in all_contracts:
        p = contract.get("participants", {})
        a = p.get("runtime_a", "")
        b = p.get("runtime_b", "")

        if a in pid_set and b in pid_set:
            matches.append((contract, (a, b)))

    return matches


def action_matches_state(action_type, action_desc, state_name, state_desc):
    """Check if the requested action matches a contract state.

    Uses direct action type match + semantic overlap.
    """
    action_lower = action_type.lower()
    state_lower = state_name.lower()
    desc_lower = (state_desc or "").lower()

    # Direct match: action type == state name
    if action_lower == state_lower:
        return True, "direct_match"

    # Action type appears in state description
    if action_lower and action_lower in desc_lower:
        return True, "action_in_description"

    # State name appears in action description
    # BUT: check negation context first — "no approach" is not an approach
    action_desc_lower = (action_desc or "").lower()
    if state_lower and state_lower in action_desc_lower:
        # Check for negation: "no approach", "not approaching", "never touch", etc.
        import re
        negation_pattern = re.compile(
            r'\b(no|not|never|without|refuse|refuses|refusing|avoid|avoids|cannot|won\'t|dont|don\'t)\s+' +
            re.escape(state_lower) + r'\b'
        )
        if negation_pattern.search(action_desc_lower):
            # State name appears in a negated context — this is NOT a match
            pass
        else:
            return True, "state_in_action_desc"

    # Semantic proximity groups
    APPROACH_ACTIONS = {"approach", "touch", "merge", "close", "embrace", "possess"}
    DISTANCE_ACTIONS = {"maintain_distance", "witness", "orbit", "observe", "watch"}
    SPEAK_ACTIONS = {"speak", "confess", "explain", "talk", "address"}
    SEPARATE_ACTIONS = {"flee", "abandon", "sever", "separate", "leave", "depart"}

    if action_lower in APPROACH_ACTIONS and state_lower in APPROACH_ACTIONS:
        return True, "approach_group"
    if action_lower in DISTANCE_ACTIONS and state_lower in DISTANCE_ACTIONS:
        return True, "distance_group"
    if action_lower in SPEAK_ACTIONS and state_lower in ("speak", "confess", "witness"):
        return True, "speak_group"
    if action_lower in SEPARATE_ACTIONS and state_lower in ("separation", "flee", "abandon"):
        return True, "separate_group"

    return False, "no_match"


def evaluate_contract(contract, action_type, action_desc):
    """Evaluate a requested action against a single contract.

    Returns (verdict, violations, matched_state).
    """
    action_lower = action_type.lower()
    violations = []

    # Step 1: Check forbidden states — these take priority
    for fs in contract.get("forbidden_states", []):
        state_name = fs.get("state", "")
        state_desc = fs.get("description", "")
        matched, reason = action_matches_state(action_type, action_desc, state_name, state_desc)

        if matched:
            for v in fs.get("violates", []):
                violations.append({
                    "constraint_type": "contract_forbidden_state",
                    "contract_id": contract["id"],
                    "forbidden_state": state_name,
                    "violation_detail": v,
                    "match_reason": reason,
                    "tag": fs.get("tag", "[E]"),
                    "severity": "ERROR" if fs.get("tag", "[E]") == "[E]" else "WARNING"
                })

    if violations:
        return "CONTRACT_VIOLATION", violations, None

    # Step 2: Check allowed states
    matched_state = None
    for allowed in contract.get("allowed_states", []):
        state_name = allowed.get("state", "")
        state_desc = allowed.get("description", "")
        matched, reason = action_matches_state(action_type, action_desc, state_name, state_desc)

        if matched:
            matched_state = {
                "state": state_name,
                "description": state_desc,
                "match_reason": reason,
                "tag": allowed.get("tag", "[E]")
            }
            break

    if matched_state:
        return "CONTRACT_PASS", [], matched_state

    # Step 3: Check violation rules for explicit detection patterns
    # ONLY flag rules with VIOLATION_DETECTED verdict — PASS rules are not violations
    for rule in contract.get("violation_rules", []):
        if rule.get("engine_verdict") != "VIOLATION_DETECTED":
            continue  # Skip PASS and non-violation rules
        detection = rule.get("detection", "").lower()
        if action_lower and action_lower in detection:
            violations.append({
                "constraint_type": "contract_violation_rule",
                "contract_id": contract["id"],
                "rule_id": rule.get("rule_id", ""),
                "violation_detail": rule.get("description", ""),
                "tag": rule.get("tag", "[E]"),
                "severity": "ERROR"
            })

    if violations:
        return "CONTRACT_VIOLATION", violations, None

    # Step 4: No match found — action outside contract scope
    return "CONTRACT_NOT_APPLICABLE", [], None


def evaluate_all_contracts(ctx, all_contracts):
    """Evaluate all matching contracts for the current scenario context.

    Returns:
        results: dict with contract_id → evaluation result
        all_violations: list of all contract violations
        summary: aggregate contract verdict
    """
    action = ctx.requested_action
    action_type = action.get("type", "")
    action_desc = action.get("description", "")

    matching = find_matching_contracts(ctx.participant_ids, all_contracts)

    results = {}
    all_violations = []
    contract_verdicts = []

    for contract, (a, b) in matching:
        verdict, violations, matched_state = evaluate_contract(contract, action_type, action_desc)

        results[contract["id"]] = {
            "contract_id": contract["id"],
            "contract_name": contract.get("name", ""),
            "participants": f"{a}↔{b}",
            "verdict": verdict,
            "violations": violations,
            "matched_state": matched_state,
            "symmetry": contract.get("symmetry_status", "unknown"),
        }

        if violations:
            all_violations.extend(violations)

        contract_verdicts.append(verdict)

    # Aggregate verdict
    if any(v == "CONTRACT_VIOLATION" for v in contract_verdicts):
        aggregate = "CONTRACT_VIOLATION"
    elif any(v == "CONTRACT_PASS" for v in contract_verdicts):
        aggregate = "CONTRACT_PASS"
    elif all(v == "CONTRACT_NOT_APPLICABLE" for v in contract_verdicts):
        aggregate = "CONTRACT_NOT_APPLICABLE"
    else:
        aggregate = "NO_CONTRACTS"

    summary = {
        "contracts_evaluated": len(matching),
        "contract_ids": [c["id"] for c, _ in matching],
        "verdict": aggregate,
        "pass_count": sum(1 for v in contract_verdicts if v == "CONTRACT_PASS"),
        "violation_count": sum(1 for v in contract_verdicts if v == "CONTRACT_VIOLATION"),
        "not_applicable_count": sum(1 for v in contract_verdicts if v == "CONTRACT_NOT_APPLICABLE"),
    }

    return results, all_violations, summary
