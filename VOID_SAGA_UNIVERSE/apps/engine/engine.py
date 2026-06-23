#!/usr/bin/env python3
"""
Void Saga Constraint Engine — v0.3.0 (Contract-First Evaluation)

Phase 14G: Contract-first evaluation.
Loads standalone contract objects as primary source of truth.
Evaluates scenario against contract allowed_states, forbidden_states,
and violation_rules. Runtime-derived contract generation still available for backward compatibility.

Reference: apps/CONSTRAINT_ENGINE_SPEC.md
"""

import json
import sys
import os
from datetime import datetime


RUNTIME_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "runtimes")
CONTRACT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "contracts")


# --- Loading ---

def load_runtime(runtime_id):
    path = os.path.join(RUNTIME_DIR, f"{runtime_id}.runtime.json")
    if not os.path.exists(path):
        return None, f"Runtime file not found: {path}"
    with open(path, "r") as f:
        return json.load(f), None


def load_runtimes(runtime_ids):
    runtimes = {}
    for rid in runtime_ids:
        rt, err = load_runtime(rid)
        if err:
            return None, err
        runtimes[rid] = rt
    return runtimes, None


def load_scenario(path):
    if not os.path.exists(path):
        return None, f"Scenario file not found: {path}"
    with open(path, "r") as f:
        return json.load(f), None


# --- Contract Generation ---

def generate_contract(runtime_a, runtime_b):
    """Generate bidirectional contract from two runtimes' relationship interfaces."""
    id_a = runtime_a["id"]
    id_b = runtime_b["id"]

    rel_a_to_b = None
    rel_b_to_a = None

    for rel in runtime_a.get("relationship_interfaces", []):
        if rel.get("target") == id_b:
            rel_a_to_b = rel

    for rel in runtime_b.get("relationship_interfaces", []):
        if rel.get("target") == id_a:
            rel_b_to_a = rel

    if not rel_a_to_b and not rel_b_to_a:
        return None, f"No relationship contract found between {id_a} and {id_b}"

    symmetry_a = rel_a_to_b.get("symmetry_status", "unresolved") if rel_a_to_b else "absent"
    symmetry_b = rel_b_to_a.get("symmetry_status", "unresolved") if rel_b_to_a else "absent"
    overall_symmetry = "symmetric" if (symmetry_a == "symmetric" and symmetry_b == "symmetric") else "asymmetric"

    contract = {
        "contract_id": f"{id_a}_{id_b}",
        "runtime_a": id_a,
        "runtime_b": id_b,
        "relationship_a_to_b": rel_a_to_b,
        "relationship_b_to_a": rel_b_to_a,
        "symmetry_status": overall_symmetry,
        "constraints": []
    }

    # Merge constraints from both directions
    if rel_a_to_b:
        contract["constraints"].append({
            "direction": f"{id_a}→{id_b}",
            "nature": rel_a_to_b.get("nature", ""),
            "behavioral_rule": rel_a_to_b.get("behavioral_rule", ""),
            "gravity": rel_a_to_b.get("canon_gravity_pull", ""),
            "tag": rel_a_to_b.get("tag", "[E]")
        })
    if rel_b_to_a:
        contract["constraints"].append({
            "direction": f"{id_b}→{id_a}",
            "nature": rel_b_to_a.get("nature", ""),
            "behavioral_rule": rel_b_to_a.get("behavioral_rule", ""),
            "gravity": rel_b_to_a.get("canon_gravity_pull", ""),
            "tag": rel_b_to_a.get("tag", "[E]")
        })

    return contract, None


# --- Constraint Evaluation ---

def evaluate_runtime_constraints(runtime, scenario, target_id, is_actor):
    """Evaluate a single runtime's constraints against the scenario.
    If is_actor=True, this runtime is performing the action.
    If is_actor=False, this runtime is receiving the action."""
    violations = []
    triggered = []
    action = scenario.get("requested_action", "")

    # Defense triggers
    for t in runtime.get("trigger_conditions", []):
        trigger_text = t.get("trigger", "")
        intensity = t.get("intensity", "")

        if "Sevraya" in trigger_text and "proximity" in trigger_text.lower():
            if target_id == "sevraya" and action in ("approach", "touch", "merge"):
                if is_actor:
                    triggered.append({
                        "runtime": runtime["id"],
                        "defense": "Orbital calibration",
                        "intensity": intensity,
                        "result": "VIOLATION — defense prohibits closer proximity"
                    })
                else:
                    triggered.append({
                        "runtime": runtime["id"],
                        "defense": "Orbital calibration (target)",
                        "intensity": intensity,
                        "result": "Active — maintaining orbital distance"
                    })

        if "Delphie" in trigger_text and "danger" in trigger_text.lower():
            if target_id == "delphie" and action in ("protect", "defend"):
                triggered.append({
                    "runtime": runtime["id"],
                    "defense": "Preemptive protection (CRITICAL)",
                    "intensity": intensity,
                    "result": "Active — maximum protection override"
                })

        if "NiuNiu" in trigger_text and "proximity" in trigger_text.lower():
            if target_id == "niuniu" and action in ("approach", "touch", "merge"):
                triggered.append({
                    "runtime": runtime["id"],
                    "defense": "Orbital calibration",
                    "intensity": intensity,
                    "result": "VIOLATION — cannot touch without collapsing constant" if is_actor else "Active — maintaining orbital distance"
                })

    # Forbidden behaviors — only flag the most relevant one per runtime
    found_forbidden = False
    for fb in runtime.get("forbidden_behaviors", []):
        behavior = fb.get("behavior", "")
        if found_forbidden:
            break
        if action in ("approach", "touch", "merge"):
            if "healed" in behavior.lower() or "merge" in behavior.lower():
                violations.append({
                    "runtime": runtime["id"],
                    "constraint_type": "forbidden_behavior",
                    "behavior": behavior,
                    "violation_detail": f"Action '{action}' triggers forbidden behavior: '{behavior[:100]}'",
                    "source": f"{runtime['id']}.runtime.md §Forbidden Behaviors"
                })
                found_forbidden = True

    # Anti-gravity — only flag items specifically about merge/healing when action is approach/touch/merge
    for ag in runtime.get("anti_gravity", []):
        ag_lower = ag.lower()
        if action in ("approach", "touch", "merge"):
            if "merge" in ag_lower:
                violations.append({
                    "runtime": runtime["id"],
                    "constraint_type": "anti_gravity",
                    "violation_detail": f"Anti-gravity: merge prohibited — '{ag[:120]}'",
                    "source": f"{runtime['id']}.runtime.md §Canon Gravity — Anti-Gravity"
                })
            elif action == "touch" and ("healed" in ag_lower or "over" in ag_lower):
                violations.append({
                    "runtime": runtime["id"],
                    "constraint_type": "anti_gravity",
                    "violation_detail": f"Anti-gravity: healing/closure prohibited — '{ag[:120]}'",
                    "source": f"{runtime['id']}.runtime.md §Canon Gravity — Anti-Gravity"
                })

    return triggered, violations


def evaluate_contract(contract, scenario):
    """Evaluate the merged contract against the scenario."""
    violations = []
    action = scenario.get("requested_action", "")

    for c in contract.get("constraints", []):
        rule = c.get("behavioral_rule", "")

        if action in ("approach", "touch", "merge"):
            if "distance" in rule.lower() or "never merge" in rule.lower() or "cannot touch" in rule.lower():
                violations.append({
                    "constraint_type": "relationship_contract",
                    "direction": c["direction"],
                    "nature": c.get("nature", ""),
                    "violation_detail": f"Contract '{c['direction']}' prohibits approach/merge. Rule: '{rule[:100]}'",
                    "source": f"Generated from {contract['runtime_a']}↔{contract['runtime_b']} relationship interfaces"
                })

    return violations


def compute_confidence(runtimes, violations):
    """Compute confidence from evidence ratios across both runtimes."""
    e_total, i_total, pc_total = 0, 0, 0
    for rt in runtimes.values():
        tags = rt.get("runtime_status", {}).get("tags", {})
        e_total += tags.get("E", 0)
        i_total += tags.get("I", 0)
        pc_total += tags.get("PC", 0)

    total = e_total + i_total + pc_total
    evidence_ratio = e_total / total if total > 0 else 0.5
    base = round(evidence_ratio * 0.7 + 0.3, 2)
    if violations:
        base = round(base - 0.05, 2)
    return max(0.0, min(1.0, base))


# --- Main Execution ---

def execute(scenario_path):
    scenario, err = load_scenario(scenario_path)
    if err:
        return {"status": "INSUFFICIENT_DATA", "verdict": "INSUFFICIENT_DATA", "error": err}

    participant_ids = [p["runtime_id"] for p in scenario.get("participants", [])]
    if len(participant_ids) < 2:
        return {"status": "INSUFFICIENT_DATA", "verdict": "INSUFFICIENT_DATA",
                "error": "Need exactly 2 participants for two-runtime contract validation"}

    runtimes, err = load_runtimes(participant_ids)
    if err:
        return {"status": "INSUFFICIENT_DATA", "verdict": "INSUFFICIENT_DATA", "error": err}

    id_a, id_b = participant_ids[0], participant_ids[1]
    contract, err = generate_contract(runtimes[id_a], runtimes[id_b])
    if err:
        return {"status": "INSUFFICIENT_DATA", "verdict": "INSUFFICIENT_DATA", "error": err}

    trace = []
    trace.append({"step": 1, "pipeline_stage": "LOAD", "decision": f"Runtimes '{id_a}', '{id_b}' loaded."})

    # Contract detected
    trace.append({"step": 2, "pipeline_stage": "CONTRACT",
                   "decision": f"Contract {contract['contract_id']} — symmetry: {contract['symmetry_status']}. {len(contract['constraints'])} constraint direction(s)."})

    # Evaluate: runtime A as actor toward B, and runtime B as target receiving action
    action = scenario.get("requested_action", "")
    triggered_a, violations_a = evaluate_runtime_constraints(runtimes[id_a], scenario, id_b, is_actor=True)
    triggered_b, violations_b = evaluate_runtime_constraints(runtimes[id_b], scenario, id_a, is_actor=(action in ("approach", "touch", "merge")))

    all_triggered = triggered_a + triggered_b
    trace.append({"step": 3, "pipeline_stage": "TRIGGER_DEFENSES",
                   "decision": f"{len(all_triggered)} defense(s) triggered across both runtimes."})

    runtime_violations = violations_a + violations_b
    trace.append({"step": 4, "pipeline_stage": "CHECK_RUNTIME_CONSTRAINTS",
                   "decision": f"{len(runtime_violations)} runtime constraint violation(s)."})

    contract_violations = evaluate_contract(contract, scenario)
    trace.append({"step": 5, "pipeline_stage": "CHECK_CONTRACT",
                   "decision": f"{len(contract_violations)} contract violation(s)."})

    all_violations = runtime_violations + contract_violations

    if all_violations:
        verdict = "VIOLATION_DETECTED"
        trace.append({"step": 6, "pipeline_stage": "VERDICT",
                       "decision": f"VIOLATION_DETECTED — {len(all_violations)} violation(s)."})
        allowed, rejected = [], [{"action": action, "violation_count": len(all_violations)}]
    else:
        verdict = "PASS"
        trace.append({"step": 6, "pipeline_stage": "VERDICT", "decision": "PASS — all constraints satisfied."})
        allowed = [{"action": action, "constraints_satisfied": [f"runtime_constraints (0 violations)", f"contract_constraints (0 violations)"]}]
        rejected = []

    confidence = compute_confidence(runtimes, all_violations)

    return {
        "execution_id": f"exec_{os.path.basename(scenario_path).replace('.json', '')}",
        "timestamp": datetime.now().isoformat(),
        "engine_version": "0.2.0",
        "status": "COMPLETED",
        "verdict": verdict,
        "runtimes_loaded": participant_ids,
        "contract_detected": {
            "contract_id": contract["contract_id"],
            "symmetry_status": contract["symmetry_status"],
            "directions": len(contract["constraints"])
        },
        "triggered_constraints": all_triggered,
        "violations": all_violations,
        "allowed_actions": allowed,
        "rejected_actions": rejected,
        "confidence": confidence,
        "trace": trace
    }


# --- Contract-First Evaluation (v0.3.0) ---

def load_contract(contract_id):
    """Load a standalone contract JSON file."""
    path = os.path.join(CONTRACT_DIR, f"{contract_id}.contract.json")
    if not os.path.exists(path):
        return None, f"Contract file not found: {path}"
    with open(path, "r") as f:
        return json.load(f), None


def evaluate_against_contract(contract, scenario):
    """Evaluate scenario directly against contract allowed_states, forbidden_states, and violation_rules."""
    action = scenario.get("requested_action", "")
    triggered_rules = []
    violations = []

    # Check allowed states
    allowed_states = contract.get("allowed_states", [])
    forbidden_states = contract.get("forbidden_states", [])
    violation_rules = contract.get("violation_rules", [])

    allowed_match = None
    for state in allowed_states:
        if action == state["state"] or action in state.get("description", ""):
            allowed_match = state
            break

    forbidden_match = None
    for state in forbidden_states:
        if action == state["state"]:
            forbidden_match = state
            break

    # Apply violation rules
    for rule in violation_rules:
        rule_id = rule.get("rule_id", "")
        if action in ("maintain_distance", "witness", "orbit") and "MAINTENANCE" in rule_id:
            triggered_rules.append({
                "rule_id": rule_id,
                "engine_verdict": rule["engine_verdict"],
                "description": rule["description"],
                "constraints_invoked": rule.get("constraints_invoked", [])
            })
        elif action in ("approach", "touch", "merge") and "APPROACH" in rule_id:
            triggered_rules.append({
                "rule_id": rule_id,
                "engine_verdict": rule["engine_verdict"],
                "description": rule["description"],
                "constraints_invoked": rule.get("constraints_invoked", [])
            })
            # Collect specific violations from the forbidden state match
            if forbidden_match:
                for v in forbidden_match.get("violates", []):
                    violations.append({
                        "constraint_type": "contract_forbidden_state",
                        "forbidden_state": forbidden_match["state"],
                        "violation_detail": v,
                        "source": "orbital_constant.contract.json"
                    })

    # Build verdict
    if violations:
        verdict = "VIOLATION_DETECTED"
    elif allowed_match:
        verdict = "PASS"
    else:
        verdict = "INSUFFICIENT_DATA"

    # Match test references
    test_refs = contract.get("test_references", [])
    matched_tests = []
    for t in test_refs:
        if t.get("verdict") == verdict or (verdict == "VIOLATION_DETECTED" and t.get("verdict") in ("TEST_PASS", "VIOLATION_DETECTED")):
            matched_tests.append(t["execution_id"])

    return {
        "verdict": verdict,
        "contract_loaded": contract["id"],
        "contract_id": contract["id"],
        "allowed_states_checked": [s["state"] for s in allowed_states],
        "forbidden_states_checked": [s["state"] for s in forbidden_states],
        "triggered_rules": triggered_rules,
        "violations": violations,
        "matched_tests": matched_tests,
        "confidence": contract.get("confidence_model", {}).get("base_confidence", 0.9),
        "trace": [
            {"step": 1, "pipeline_stage": "LOAD_CONTRACT", "decision": f"Contract '{contract['id']}' loaded. {len(allowed_states)} allowed, {len(forbidden_states)} forbidden states."},
            {"step": 2, "pipeline_stage": "EVALUATE_STATES", "decision": f"Action '{action}' checked against {len(allowed_states) + len(forbidden_states)} states."},
            {"step": 3, "pipeline_stage": "APPLY_RULES", "decision": f"{len(triggered_rules)} rule(s) triggered."},
            {"step": 4, "pipeline_stage": "VERDICT", "decision": f"{verdict} — {len(violations)} violation(s). {len(matched_tests)} test(s) matched."}
        ]
    }


def execute_contract_first(scenario_path, contract_id="orbital_constant"):
    """Contract-first execution: load contract, evaluate scenario against it."""
    scenario, err = load_scenario(scenario_path)
    if err:
        return {"status": "INSUFFICIENT_DATA", "verdict": "INSUFFICIENT_DATA", "error": err}

    contract, err = load_contract(contract_id)
    if err:
        return {"status": "INSUFFICIENT_DATA", "verdict": "INSUFFICIENT_DATA", "error": err}

    result = evaluate_against_contract(contract, scenario)
    result["execution_id"] = f"exec_{os.path.basename(scenario_path).replace('.json', '')}"
    result["timestamp"] = datetime.now().isoformat()
    result["engine_version"] = "0.3.0"
    result["status"] = "COMPLETED"
    return result


# --- CLI ---

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python engine.py <scenario_path> [--mode contract|runtime]")
        print("  --mode contract : Contract-first evaluation (default, v0.3.0)")
        print("  --mode runtime  : Runtime-derived contract generation (v0.2.0 compat)")
        sys.exit(1)

    scenario_path = sys.argv[1]
    mode = "contract"
    if "--mode" in sys.argv:
        idx = sys.argv.index("--mode")
        if idx + 1 < len(sys.argv):
            mode = sys.argv[idx + 1]

    if mode == "runtime":
        result = execute(sys.argv[1])
    else:
        result = execute_contract_first(sys.argv[1])

    print(json.dumps(result, indent=2, ensure_ascii=False))
