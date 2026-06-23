#!/usr/bin/env python3
"""
Void Saga Constraint Engine — v0.1.0 (Embryo)

Phase 14D: First executable implementation.
Validates a single runtime against a single scenario.
No contracts. No protocols. No renderer. No multi-runtime.

Reference: apps/CONSTRAINT_ENGINE_SPEC.md
"""

import json
import sys
import os
from datetime import datetime


# --- Constants ---

RUNTIME_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "runtimes")

VALID_VERDICTS = {"PASS", "VIOLATION_DETECTED", "INSUFFICIENT_DATA"}

# --- Engine Core ---

def load_runtime(runtime_id):
    """Load a runtime JSON file by ID."""
    path = os.path.join(RUNTIME_DIR, f"{runtime_id}.runtime.json")
    if not os.path.exists(path):
        return None, f"Runtime file not found: {path}"
    with open(path, "r") as f:
        return json.load(f), None


def load_scenario(path):
    """Load a scenario JSON file."""
    if not os.path.exists(path):
        return None, f"Scenario file not found: {path}"
    with open(path, "r") as f:
        return json.load(f), None


def evaluate_defense_triggers(runtime, scenario):
    """Check trigger_conditions against scenario state. Return triggered defenses."""
    triggered = []
    triggers = runtime.get("trigger_conditions", [])

    target = scenario.get("target", "")
    action = scenario.get("requested_action", "")

    for t in triggers:
        trigger_text = t.get("trigger", "")
        intensity = t.get("intensity", "")

        # Delphie danger trigger
        if "Delphie" in trigger_text and "danger" in trigger_text.lower():
            if target == "Delphie" and action in ("protect", "defend"):
                triggered.append({
                    "defense": "Preemptive protection (CRITICAL)",
                    "intensity": intensity,
                    "source_trigger": trigger_text,
                    "result": "Active — maximum protection override"
                })

        # Sevraya proximity trigger
        if "Sevraya" in trigger_text and "proximity" in trigger_text.lower():
            if target == "Sevraya" and action in ("approach", "touch", "merge"):
                triggered.append({
                    "defense": "Orbital calibration",
                    "intensity": intensity,
                    "source_trigger": trigger_text,
                    "result": "VIOLATION — defense prohibits closer proximity"
                })

    return triggered


def check_forbidden_behaviors(runtime, scenario):
    """Check proposed action against forbidden behaviors. Return violations."""
    violations = []
    forbidden = runtime.get("forbidden_behaviors", [])
    action = scenario.get("requested_action", "")
    target = scenario.get("target", "")

    for fb in forbidden:
        behavior = fb.get("behavior", "")

        # Approach/touch Sevraya → only flag healing/merge-related behaviors
        if target == "Sevraya" and action in ("approach", "touch", "merge"):
            if "healed" in behavior.lower() or "over" in behavior.lower():
                violations.append({
                    "constraint_type": "forbidden_behavior",
                    "behavior": behavior,
                    "violation_detail": f"Action '{action}' toward Sevraya approaches healing/closure that the orbital contract prohibits. '{behavior}'",
                    "source": "NiuNiu.runtime.md §11 Forbidden Behaviors"
                })

        # Fluent speech without external force
        if action == "speak_fluently" and not scenario.get("external_force", False):
            if "speak at length" in behavior.lower() or "fluently" in behavior.lower():
                violations.append({
                    "constraint_type": "forbidden_behavior",
                    "behavior": behavior,
                    "violation_detail": "NiuNiu cannot speak fluently without external force (chain, Rose threat, Sevraya proximity).",
                    "source": "NiuNiu.runtime.md §11 Forbidden Behaviors #1"
                })

        # Stop protecting
        if action in ("abandon", "stop_protecting", "ignore_threat"):
            if "stops protecting" in behavior.lower() or "protection" in behavior.lower():
                violations.append({
                    "constraint_type": "forbidden_behavior",
                    "behavior": behavior,
                    "violation_detail": f"Action '{action}' contradicts protection invariant: '{behavior}'",
                    "source": "NiuNiu.runtime.md §11 Forbidden Behaviors"
                })

    return violations


def check_anti_gravity(runtime, scenario):
    """Check proposed action against anti-gravity outcomes. Return violations."""
    violations = []
    anti_gravity = runtime.get("anti_gravity", [])
    action = scenario.get("requested_action", "")
    target = scenario.get("target", "")

    for ag in anti_gravity:
        # Merge with Sevraya
        if target == "Sevraya" and ("merge" in ag.lower() or "merge" in action.lower()):
            violations.append({
                "constraint_type": "anti_gravity",
                "anti_gravity_item": ag,
                "violation_detail": "Merge with Sevraya is listed as anti-gravity — requires active fork intervention.",
                "source": "NiuNiu.runtime.md §9 Canon Gravity — Anti-Gravity"
            })

        # Stop protecting
        if action in ("abandon", "stop_protecting") and "stops protecting" in ag.lower():
            violations.append({
                "constraint_type": "anti_gravity",
                "anti_gravity_item": ag,
                "violation_detail": "Ceasing protection contradicts identity invariant.",
                "source": "NiuNiu.runtime.md §9 Anti-Gravity"
            })

    return violations


def check_relationship_contract(runtime, scenario):
    """Check proposed action against relationship contract with target. Return violations."""
    violations = []
    relationships = runtime.get("relationship_interfaces", [])
    target = scenario.get("target", "")
    action = scenario.get("requested_action", "")

    for rel in relationships:
        # Case-insensitive target matching
        rel_target = rel.get("target", "")
        if rel_target.lower() != target.lower():
            continue

        behavioral_rule = rel.get("behavioral_rule", "")

        # Sevraya: distance is the care
        if rel_target.lower() == "sevraya" and action in ("approach", "touch", "merge"):
            violations.append({
                "constraint_type": "relationship_contract",
                "target": target,
                "contract_nature": rel.get("nature", ""),
                "behavioral_rule": behavioral_rule,
                "violation_detail": f"Action '{action}' violates contract: 'Distance IS the care. Never merge.' Approach collapses orbital constant.",
                "source": f"NiuNiu.runtime.md §Relationship Interfaces — {target}"
            })

        # Delphie: maximum protection
        if rel_target.lower() == "delphie" and action in ("abandon", "ignore_threat", "retreat"):
            violations.append({
                "constraint_type": "relationship_contract",
                "target": target,
                "contract_nature": rel.get("nature", ""),
                "behavioral_rule": behavioral_rule,
                "violation_detail": f"Action '{action}' violates contract: Maximum protection is CRITICAL for Delphie.",
                "source": f"NiuNiu.runtime.md §Relationship Interfaces — {target}"
            })

    return violations


def compute_confidence(runtime, violations, triggered_defenses):
    """Compute confidence score based on evidence levels in triggered constraints."""
    # Base confidence from evidence ratio
    tags = runtime.get("runtime_status", {}).get("tags", {})
    e_count = tags.get("E", 0)
    total = e_count + tags.get("I", 0) + tags.get("PC", 0)
    evidence_ratio = e_count / total if total > 0 else 0.5

    # Downgrade: each violation sourced from [I] or [PC] reduces confidence
    downgrades = []
    if violations:
        downgrades.append("Violations detected — confidence applies to violation accuracy")

    confidence = round(evidence_ratio * 0.7 + 0.3, 2)  # Base: evidence ratio weighted
    if downgrades:
        confidence = round(confidence - 0.05 * len(downgrades), 2)

    return max(0.0, min(1.0, confidence)), downgrades


def execute(scenario_path):
    """Main engine execution. Load runtime, evaluate scenario, return verdict."""

    # Step 1 + 2: Load runtime and scenario
    scenario, err = load_scenario(scenario_path)
    if err:
        return {
            "execution_id": f"exec_{os.path.basename(scenario_path).replace('.json', '')}",
            "timestamp": datetime.now().isoformat(),
            "engine_version": "0.1.0",
            "status": "INSUFFICIENT_DATA",
            "verdict": "INSUFFICIENT_DATA",
            "error": err,
            "runtime_loaded": None,
            "violations": [],
            "allowed_actions": [],
            "triggered_defenses": [],
            "confidence": 0.0,
            "trace": []
        }

    runtime_id = scenario.get("character", "")
    runtime, err = load_runtime(runtime_id)
    if err:
        return {
            "execution_id": f"exec_{os.path.basename(scenario_path).replace('.json', '')}",
            "timestamp": datetime.now().isoformat(),
            "engine_version": "0.1.0",
            "status": "INSUFFICIENT_DATA",
            "verdict": "INSUFFICIENT_DATA",
            "error": err,
            "runtime_loaded": None,
            "violations": [],
            "allowed_actions": [],
            "triggered_defenses": [],
            "confidence": 0.0,
            "trace": []
        }

    trace = []

    # Step 3: Evaluate
    trace.append({"step": 1, "pipeline_stage": "LOAD", "decision": f"Runtime '{runtime_id}' loaded."})

    triggered_defenses = evaluate_defense_triggers(runtime, scenario)
    trace.append({"step": 2, "pipeline_stage": "TRIGGER_DEFENSES",
                   "decision": f"{len(triggered_defenses)} defense(s) triggered."})

    forbidden_violations = check_forbidden_behaviors(runtime, scenario)
    trace.append({"step": 3, "pipeline_stage": "CHECK_FORBIDDEN",
                   "decision": f"{len(forbidden_violations)} forbidden behavior violation(s)."})

    anti_gravity_violations = check_anti_gravity(runtime, scenario)
    trace.append({"step": 4, "pipeline_stage": "CHECK_ANTI_GRAVITY",
                   "decision": f"{len(anti_gravity_violations)} anti-gravity violation(s)."})

    contract_violations = check_relationship_contract(runtime, scenario)
    trace.append({"step": 5, "pipeline_stage": "CHECK_CONTRACT",
                   "decision": f"{len(contract_violations)} contract violation(s)."})

    all_violations = forbidden_violations + anti_gravity_violations + contract_violations

    # Step 4: Generate verdict
    if all_violations:
        verdict = "VIOLATION_DETECTED"
        allowed_actions = []
        trace.append({"step": 6, "pipeline_stage": "VERDICT",
                       "decision": f"VIOLATION_DETECTED — {len(all_violations)} violation(s) found."})
    else:
        verdict = "PASS"
        target = scenario.get("target", "")
        action = scenario.get("requested_action", "")
        allowed_actions = [{
            "action": f"{action} toward {target}",
            "action_type": action,
            "constraints_satisfied": [
                f"trigger_conditions ({len(triggered_defenses)} defense(s) active)",
                f"forbidden_behaviors (0 violations)",
                f"anti_gravity (0 violations)",
                f"relationship_contract (0 violations)"
            ],
            "confidence": 0.95
        }]
        trace.append({"step": 6, "pipeline_stage": "VERDICT",
                       "decision": f"PASS — all constraints satisfied."})

    confidence, downgrades = compute_confidence(runtime, all_violations, triggered_defenses)

    return {
        "execution_id": f"exec_{os.path.basename(scenario_path).replace('.json', '')}",
        "timestamp": datetime.now().isoformat(),
        "engine_version": "0.1.0",
        "status": "COMPLETED",
        "verdict": verdict,
        "runtime_loaded": runtime_id,
        "violations": all_violations,
        "allowed_actions": allowed_actions,
        "triggered_defenses": triggered_defenses,
        "confidence": confidence,
        "confidence_notes": downgrades,
        "trace": trace
    }


# --- CLI ---

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python engine.py <scenario_path>")
        print("Example: python engine.py scenarios/valid_delphie_protection.json")
        sys.exit(1)

    scenario_path = sys.argv[1]
    result = execute(scenario_path)
    print(json.dumps(result, indent=2, ensure_ascii=False))
