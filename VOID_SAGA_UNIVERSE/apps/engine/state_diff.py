#!/usr/bin/env python3
"""
Void Saga State Diff Engine — v0.1.0

Phase 14K: Compare two world state snapshots and produce machine-readable diff.
Respects Residue Law: residues are never deleted, only transformed or archived.

Reference: apps/STATE_DIFF_ENGINE_SPEC.md
"""

import json
import sys
import os
from datetime import datetime


# --- Loading ---

def load_state(path):
    if not os.path.exists(path):
        return None, f"State file not found: {path}"
    with open(path, "r") as f:
        return json.load(f), None


# --- Validation ---

def validate_states(state_a, state_b):
    if state_a.get("world_id") != state_b.get("world_id"):
        return False, "INCOMPATIBLE_WORLD_STATES", "World IDs do not match."
    if state_a.get("version") != state_b.get("version"):
        return False, "INCOMPATIBLE_WORLD_STATES", "Schema versions do not match."
    phase_a = state_a.get("timeline", {}).get("boot_sequence_phase", 0)
    phase_b = state_b.get("timeline", {}).get("boot_sequence_phase", 0)
    if phase_a > phase_b:
        return False, "INVALID_TIMELINE", f"World A phase ({phase_a}) is later than World B ({phase_b})."
    return True, "PASS", None


# --- Diff Logic ---

def diff_runtimes(state_a, state_b):
    runtimes_a = {r["runtime_id"]: r for r in state_a.get("active_runtimes", [])}
    runtimes_b = {r["runtime_id"]: r for r in state_b.get("active_runtimes", [])}
    changes = []

    all_ids = set(runtimes_a.keys()) | set(runtimes_b.keys())
    for rid in sorted(all_ids):
        ra = runtimes_a.get(rid)
        rb = runtimes_b.get(rid)

        if ra is None and rb is not None:
            changes.append({"runtime_id": rid, "change_type": "added", "from": None,
                           "to": f"Stage {rb['evolution_stage']} ({rb['status']})",
                           "detail": f"Runtime '{rid}' added."})
        elif ra is not None and rb is None:
            changes.append({"runtime_id": rid, "change_type": "removed", "from": f"Stage {ra['evolution_stage']} ({ra['status']})",
                           "to": None, "detail": f"Runtime '{rid}' removed."})
        else:
            if ra["evolution_stage"] != rb["evolution_stage"]:
                changes.append({"runtime_id": rid, "change_type": "evolved",
                               "from": f"Stage {ra['evolution_stage']}", "to": f"Stage {rb['evolution_stage']}",
                               "detail": f"'{rid}' evolved from Stage {ra['evolution_stage']} to Stage {rb['evolution_stage']}."})
            if ra["status"] != rb["status"]:
                changes.append({"runtime_id": rid, "change_type": "status_changed",
                               "from": ra["status"], "to": rb["status"],
                               "detail": f"'{rid}' status changed: {ra['status']} → {rb['status']}."})

    return changes


def diff_contracts(state_a, state_b):
    contracts_a = {c["contract_id"]: c for c in state_a.get("active_contracts", [])}
    contracts_b = {c["contract_id"]: c for c in state_b.get("active_contracts", [])}
    changes = []

    all_ids = set(contracts_a.keys()) | set(contracts_b.keys())
    for cid in sorted(all_ids):
        ca = contracts_a.get(cid)
        cb = contracts_b.get(cid)

        if ca is None and cb is not None:
            changes.append({"contract_id": cid, "change_type": "formed", "from": None,
                           "to": cb["status"], "detail": f"Contract '{cid}' formed."})
        elif ca is not None and cb is None:
            changes.append({"contract_id": cid, "change_type": "dissolved", "from": ca["status"],
                           "to": None, "detail": f"Contract '{cid}' dissolved."})
        elif ca["status"] != cb["status"]:
            ct = "activated" if cb["status"] == "active" and ca["status"] == "inactive" else \
                 "broken" if cb["status"] == "broken" else "status_changed"
            changes.append({"contract_id": cid, "change_type": ct,
                           "from": ca["status"], "to": cb["status"],
                           "detail": f"Contract '{cid}': {ca['status']} → {cb['status']}."})

    return changes


def diff_protocols(state_a, state_b):
    protos_a = {p["protocol_id"]: p for p in state_a.get("active_protocols", [])}
    protos_b = {p["protocol_id"]: p for p in state_b.get("active_protocols", [])}
    changes = []

    all_ids = set(protos_a.keys()) | set(protos_b.keys())
    for pid in sorted(all_ids):
        pa = protos_a.get(pid)
        pb = protos_b.get(pid)

        if pa is None and pb is not None:
            changes.append({"protocol_id": pid, "change_type": "activated", "from": None,
                           "to": pb["status"], "detail": f"Protocol '{pid}' activated."})
        elif pa is not None and pb is None:
            changes.append({"protocol_id": pid, "change_type": "removed", "from": pa["status"],
                           "to": None, "detail": f"Protocol '{pid}' removed."})
        elif pa["status"] != pb["status"]:
            ct = "executed" if pb["status"] == "executed" and pa["status"] in ("pending", "active") else \
                 "completed" if pb["status"] == "executed" and pa["status"] == "active" else "status_changed"
            residues = pb.get("residues_produced", [])
            changes.append({"protocol_id": pid, "change_type": ct,
                           "from": pa["status"], "to": pb["status"],
                           "detail": f"Protocol '{pid}': {pa['status']} → {pb['status']}.",
                           "residues_produced": residues if residues else None})

    return changes


def diff_residues(state_a, state_b):
    residues_a = {r["residue_id"]: r for r in state_a.get("active_residues", [])}
    residues_b = {r["residue_id"]: r for r in state_b.get("active_residues", [])}
    changes = []
    errors = []

    all_ids = set(residues_a.keys()) | set(residues_b.keys())
    for rid in sorted(all_ids):
        ra = residues_a.get(rid)
        rb = residues_b.get(rid)

        if ra is None and rb is not None:
            changes.append({"residue_id": rid, "change_type": "created", "from": None,
                           "to": "active", "form": rb["form"], "carried_by": rb.get("carried_by", []),
                           "detail": f"Residue '{rid}' created."})
        elif ra is not None and rb is None:
            errors.append({"residue_id": rid, "error": "RESIDUE_LAW_VIOLATION",
                          "detail": f"Residue '{rid}' absent from World B. Residues cannot be deleted per RESIDUE_THEORY.md. Must be archived or transformed, not removed."})
        else:
            changed = False
            detail_parts = []
            if ra["form"] != rb["form"]:
                detail_parts.append(f"form: {ra['form']} → {rb['form']}")
                changed = True
            if set(ra.get("carried_by", [])) != set(rb.get("carried_by", [])):
                detail_parts.append(f"carriers changed")
                changed = True
            if ra.get("transform_note") != rb.get("transform_note"):
                detail_parts.append("transform note added")
                changed = True
            if changed:
                changes.append({"residue_id": rid, "change_type": "transformed",
                               "from": ra["form"], "to": rb["form"], "form": rb["form"],
                               "carried_by": rb.get("carried_by", []),
                               "detail": "; ".join(detail_parts) if detail_parts else "Residue transformed."})

    return changes, errors


def diff_timeline(state_a, state_b):
    ta = state_a.get("timeline", {})
    tb = state_b.get("timeline", {})
    changes = []

    for field in ["boot_sequence_phase", "timer_reference", "pre_chain", "post_resolution"]:
        va = ta.get(field)
        vb = tb.get(field)
        if va != vb:
            changes.append({"field": field, "from": va, "to": vb})

    return changes


# --- Main ---

def execute(state_a_path, state_b_path, output_path=None):
    state_a, err = load_state(state_a_path)
    if err:
        return {"verdict": "MISSING_STATE", "error": err}

    state_b, err = load_state(state_b_path)
    if err:
        return {"verdict": "MISSING_STATE", "error": err}

    valid, verdict, validation_error = validate_states(state_a, state_b)
    if not valid:
        return {"verdict": verdict, "error": validation_error}

    runtime_changes = diff_runtimes(state_a, state_b)
    contract_changes = diff_contracts(state_a, state_b)
    protocol_changes = diff_protocols(state_a, state_b)
    residue_changes, residue_errors = diff_residues(state_a, state_b)
    timeline_changes = diff_timeline(state_a, state_b)

    total = len(runtime_changes) + len(contract_changes) + len(protocol_changes) + len(residue_changes) + len(timeline_changes)

    diff = {
        "diff_id": f"diff_{os.path.basename(state_a_path).replace('.json', '')}_to_{os.path.basename(state_b_path).replace('.json', '')}",
        "world_a": state_a["world_id"],
        "world_b": state_b["world_id"],
        "timestamp": datetime.now().isoformat(),
        "verdict": "PASS" if not residue_errors else "RESIDUE_LAW_VIOLATION",
        "runtime_changes": runtime_changes,
        "contract_changes": contract_changes,
        "protocol_changes": protocol_changes,
        "residue_changes": residue_changes,
        "timeline_changes": timeline_changes,
        "errors": residue_errors if residue_errors else [],
        "summary": {
            "total_runtime_changes": len(runtime_changes),
            "total_contract_changes": len(contract_changes),
            "total_protocol_changes": len(protocol_changes),
            "total_residue_changes": len(residue_changes),
            "total_timeline_changes": len(timeline_changes),
            "total_errors": len(residue_errors),
            "net_change_description": f"{total} total changes. {len(residue_errors)} residue law violation(s)."
        }
    }

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(diff, f, indent=2, ensure_ascii=False)

    return diff


# --- CLI ---

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python state_diff.py <state_a.json> <state_b.json> [--output <output.json>]")
        sys.exit(1)

    state_a_path = sys.argv[1]
    state_b_path = sys.argv[2]
    output_path = None

    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]

    result = execute(state_a_path, state_b_path, output_path)
    print(json.dumps(result, indent=2, ensure_ascii=False))
