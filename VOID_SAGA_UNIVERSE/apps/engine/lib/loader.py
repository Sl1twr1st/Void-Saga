"""Runtime + scenario loading for Void Saga constraint engine v0.4.0."""

import json
import os

RUNTIME_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "runtimes")
SCHEMA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "schema")


def load_runtime(runtime_id):
    """Load a single runtime JSON by ID. Returns (data, error)."""
    path = os.path.join(RUNTIME_DIR, f"{runtime_id}.runtime.json")
    if not os.path.exists(path):
        return None, f"Runtime file not found: {path}"
    with open(path, "r") as f:
        return json.load(f), None


def load_runtimes(runtime_ids):
    """Load multiple runtime JSONs. Returns ({id: data}, error)."""
    runtimes = {}
    for rid in runtime_ids:
        rt, err = load_runtime(rid)
        if err:
            return None, err
        runtimes[rid] = rt
    return runtimes, None


def load_scenario(path):
    """Load a scenario JSON file. Returns (data, error)."""
    if not os.path.exists(path):
        return None, f"Scenario file not found: {path}"
    with open(path, "r") as f:
        return json.load(f), None


def validate_participants(scenario, runtimes):
    """Validate that all scenario participants have corresponding loaded runtimes
    and declared evolution stages exist."""
    errors = []
    for p in scenario.get("participants", []):
        rid = p.get("runtime_id")
        if rid not in runtimes:
            errors.append(f"Participant '{rid}' not found in loaded runtimes")
            continue
        stage = p.get("evolution_stage")
        rt = runtimes[rid]
        stages = rt.get("evolution_stages", [])
        stage_numbers = [s["stage_number"] for s in stages]
        if stage not in stage_numbers:
            errors.append(
                f"Participant '{rid}' stage {stage} not found. "
                f"Valid stages: {stage_numbers}"
            )
    return errors


def validate_schema(runtime_data):
    """Lightweight schema validation: check required fields from RUNTIME_SCHEMA_V2.1.
    Returns list of missing required fields."""
    with open(os.path.join(SCHEMA_DIR, "RUNTIME_SCHEMA_V2.1.json"), "r") as f:
        schema = json.load(f)
    required = schema.get("required", [])
    missing = [f for f in required if f not in runtime_data]
    return missing
