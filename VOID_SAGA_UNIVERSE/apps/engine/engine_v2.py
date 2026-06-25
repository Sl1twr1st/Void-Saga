#!/usr/bin/env python3
"""
Void Saga Constraint Engine — v0.4.0 (Multi-Runtime Skeleton)

Phase 1 implementation. Loads N runtimes, builds MultiRuntimeContext,
validates participants, outputs structured summary.

Reference: TASK_5_ENGINE_DESIGN.md, CONSTRAINT_ENGINE_SPEC.md
"""

import json
import sys
import os

# Allow running from any directory
sys.path.insert(0, os.path.dirname(__file__))

from lib.loader import load_runtimes, load_scenario, validate_participants
from lib.context import build_context
from lib.constraints import (
    resolve_defense_triggers,
    check_forbidden_behaviors,
    check_identity_invariants,
    check_anti_gravity,
)


def execute(scenario_path):
    """Execute a multi-runtime scenario. Loads runtimes, builds context, returns summary."""

    # Step 1: Load scenario
    scenario, err = load_scenario(scenario_path)
    if err:
        return {
            "status": "INSUFFICIENT_DATA",
            "verdict": "INSUFFICIENT_DATA",
            "error": err
        }

    scenario_id = scenario.get("scenario_id", os.path.basename(scenario_path))
    participant_ids = [p["runtime_id"] for p in scenario.get("participants", [])]

    if not participant_ids:
        return {
            "status": "INSUFFICIENT_DATA",
            "verdict": "INSUFFICIENT_DATA",
            "error": "No participants in scenario"
        }

    # Step 2: Load all runtimes
    runtimes, err = load_runtimes(participant_ids)
    if err:
        return {
            "status": "INSUFFICIENT_DATA",
            "verdict": "INSUFFICIENT_DATA",
            "error": err
        }

    # Step 3: Validate participants
    validation_errors = validate_participants(scenario, runtimes)
    if validation_errors:
        return {
            "status": "INSUFFICIENT_DATA",
            "verdict": "INSUFFICIENT_DATA",
            "error": "Participant validation failed",
            "validation_errors": validation_errors
        }

    # Step 4: Build multi-runtime context
    ctx = build_context(scenario, runtimes)

    if ctx.load_errors:
        return {
            "status": "INSUFFICIENT_DATA",
            "verdict": "INSUFFICIENT_DATA",
            "error": "Context build failed",
            "load_errors": ctx.load_errors
        }

    # Step 5: Evaluate runtime constraints
    all_triggers = []
    all_violations = []
    all_warnings = []

    for rid in ctx.participant_ids:
        p = ctx.participants[rid]

        # 5a: Resolve defense triggers
        triggers = resolve_defense_triggers(p, ctx)
        all_triggers.extend(triggers)

        # 5b: Check forbidden behaviors
        fb_violations = check_forbidden_behaviors(p, ctx)
        for v in fb_violations:
            if v["severity"] == "ERROR":
                all_violations.append(v)
            else:
                all_warnings.append(v)

        # 5c: Check identity invariants
        id_violations = check_identity_invariants(p, ctx)
        all_warnings.extend(id_violations)

        # 5d: Check anti-gravity
        ag_violations = check_anti_gravity(p, ctx)
        for v in ag_violations:
            if v["severity"] == "ERROR":
                all_violations.append(v)
            else:
                all_warnings.append(v)

    # Determine verdict
    if all_violations:
        verdict = "CONSTRAINT_VIOLATION"
    elif all_warnings:
        verdict = "CONSTRAINT_WARNING"
    else:
        verdict = "CONSTRAINT_PASS"

    # Build constraint result
    constraint_result = {
        "verdict": verdict,
        "triggers_fired": len(all_triggers),
        "violations": all_violations,
        "warnings": all_warnings,
        "trigger_details": all_triggers
    }

    # Step 6: Build summary output
    participants_summary = []
    for rid in ctx.participant_ids:
        p = ctx.participants[rid]
        participants_summary.append({
            "runtime_id": p.runtime_id,
            "name": p.name,
            "version": p.version,
            "architecture": p.architecture,
            "evolution_stage": p.evolution_stage,
            "stage_name": p.stage_name,
            "sigil": f"{p.sigil_name} ({p.sigil_status})",
            "defenses": p.defense_count,
            "triggers": p.trigger_count,
            "relationships": p.relationship_count,
            "forbidden_behaviors": p.forbidden_behavior_count,
            "evidence": f"E:{p.evidence_count} I:{p.inferred_count} PC:{p.probable_canon_count}",
            "voice_sample_preview": p.voice_sample[:100] if p.voice_sample else "[none]",
            "schema_valid": "PASS" if not p.schema_missing else f"MISSING: {p.schema_missing}"
        })

    # Collect relationship pairs
    relationship_pairs = []
    ids = ctx.participant_ids
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            rt_a = runtimes[ids[i]]
            rt_b = runtimes[ids[j]]
            rel_a = None
            rel_b = None
            for rel in rt_a.get("relationship_interfaces", []):
                if rel.get("target") == ids[j]:
                    rel_a = rel
            for rel in rt_b.get("relationship_interfaces", []):
                if rel.get("target") == ids[i]:
                    rel_b = rel
            if rel_a or rel_b:
                relationship_pairs.append({
                    "pair": f"{ids[i]}↔{ids[j]}",
                    "a_to_b": rel_a.get("nature") if rel_a else "undocumented",
                    "b_to_a": rel_b.get("nature") if rel_b else "undocumented",
                    "symmetry": "symmetric" if (rel_a and rel_b and
                        rel_a.get("symmetry_status") == "symmetric" and
                        rel_b.get("symmetry_status") == "symmetric") else "asymmetric/unresolved"
                })

    timeline = ctx.timeline_state
    action = ctx.requested_action
    canon = ctx.canon_mode

    return {
        "execution_id": f"exec_{scenario_id}",
        "engine_version": "0.4.0",
        "engine_phase": "Phase 1 — Multi-Runtime Skeleton",
        "status": "COMPLETED",
        "verdict": "STRUCTURE_VALID",
        "scenario": {
            "scenario_id": scenario_id,
            "participant_count": len(ctx.participant_ids),
            "participant_ids": ctx.participant_ids,
            "timeline": {
                "phase": timeline.get("phase", "unspecified"),
                "pre_chain": timeline.get("pre_chain", True),
                "post_resolution": timeline.get("post_resolution", False)
            },
            "proximity": ctx.proximity_state,
            "requested_action": action,
            "canon_mode": canon
        },
        "participants": participants_summary,
        "relationships_detected": relationship_pairs,
        "totals": {
            "participants": len(ctx.participant_ids),
            "total_defenses": ctx.total_defenses,
            "total_triggers": ctx.total_triggers,
            "total_relationships": ctx.total_relationships,
            "total_forbidden_behaviors": ctx.total_forbidden_behaviors,
            "total_evidence_claims": ctx.total_evidence
        },
        "validation": {
            "schema_warnings": ctx.schema_warnings if ctx.schema_warnings else "none",
            "load_errors": ctx.load_errors if ctx.load_errors else "none"
        },
        "constraint_evaluation": constraint_result
    }


def print_summary(result):
    """Pretty-print engine result to terminal."""
    if result["status"] != "COMPLETED":
        print(f"❌ {result['status']}: {result.get('error', 'Unknown error')}")
        if "validation_errors" in result:
            for e in result["validation_errors"]:
                print(f"   • {e}")
        if "load_errors" in result:
            for e in result["load_errors"]:
                print(f"   • {e}")
        return

    s = result["scenario"]
    t = result["totals"]

    print(f"⚡ Void.OS Engine v{result['engine_version']} — {result['engine_phase']}")
    print(f"   Scenario: {s['scenario_id']}")
    print(f"   Participants: {t['participants']} ({', '.join(s['participant_ids'])})")
    print(f"   Timeline: phase={s['timeline']['phase']}, pre_chain={s['timeline']['pre_chain']}")
    print(f"   Action: {s['requested_action'].get('description', s['requested_action'].get('type', '?'))[:120]}")
    print()
    # Constraint evaluation verdict
    ce = result.get("constraint_evaluation", {})
    ce_verdict = ce.get("verdict", "NO_EVALUATION")
    verdict_icon = {"CONSTRAINT_PASS": "✅", "CONSTRAINT_WARNING": "⚠️", "CONSTRAINT_VIOLATION": "❌"}.get(ce_verdict, "○")
    print(f"   Structure: {result['verdict']} ✅")
    print(f"   Constraints: {ce_verdict} {verdict_icon}")
    if ce.get("triggers_fired", 0) > 0:
        print(f"   Triggers fired: {ce['triggers_fired']}")
        for t in ce.get("trigger_details", []):
            print(f"     • [{t['intensity']}] {t['runtime_id']}: {t['defense'][:80]}")
            print(f"       Match: {t['conditions_matched']} conditions, confidence={t['confidence']}")
    if ce.get("violations"):
        print(f"   Violations: {len(ce['violations'])}")
        for v in ce["violations"]:
            print(f"     ❌ [{v['constraint_type']}] {v['runtime_id']}: {v.get('behavior', v.get('anti_gravity', ''))[:100]}")
    if ce.get("warnings"):
        print(f"   Warnings: {len(ce['warnings'])}")
        for w in ce["warnings"][:3]:
            print(f"     ⚠️ [{w['constraint_type']}] {w['runtime_id']}: {w.get('invariant', w.get('violation_detail', ''))[:100]}")
    print()
    print(f"   ┌─ Participants ─────────────────────────────")
    for p in result["participants"]:
        print(f"   │ {p['name']} ({p['runtime_id']}) v{p['version']}")
        print(f"   │   Stage {p['evolution_stage']}: {p['stage_name']}")
        print(f"   │   Sigil: {p['sigil']}")
        print(f"   │   Defenses: {p['defenses']} | Triggers: {p['triggers']} | Relationships: {p['relationships']} | Forbidden: {p['forbidden_behaviors']}")
        print(f"   │   Evidence: {p['evidence']} | Schema: {p['schema_valid']}")
        print(f"   │   Voice: \"{p['voice_sample_preview']}\"")
        print(f"   │")
    print(f"   └────────────────────────────────────────────")
    print()
    if result["relationships_detected"]:
        print(f"   ┌─ Relationships ────────────────────────────")
        for r in result["relationships_detected"]:
            print(f"   │ {r['pair']}: {r['symmetry']}")
            print(f"   │   → {r['a_to_b']}")
            print(f"   │   ← {r['b_to_a']}")
            print(f"   │")
        print(f"   └────────────────────────────────────────────")
    else:
        print(f"   No documented relationships found between participants.")
    print()
    print(f"   Totals: {t['total_defenses']} defenses, {t['total_triggers']} triggers, "
          f"{t['total_relationships']} relationships, {t['total_forbidden_behaviors']} forbidden, "
          f"{t['total_evidence_claims']} evidence claims")


# --- CLI ---

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python engine_v2.py <scenario_path> [--json]")
        print("  scenario_path : Path to scenario JSON file")
        print("  --json        : Output raw JSON (default: formatted summary)")
        print()
        print("Example:")
        print("  python engine_v2.py scenarios/test_niuniu_sevraya_orbit.json")
        sys.exit(1)

    scenario_path = sys.argv[1]
    output_json = "--json" in sys.argv

    result = execute(scenario_path)

    if output_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print_summary(result)
        if result["status"] != "COMPLETED":
            sys.exit(1)
