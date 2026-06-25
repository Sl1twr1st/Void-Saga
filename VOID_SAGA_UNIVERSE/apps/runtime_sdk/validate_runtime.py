#!/usr/bin/env python3
"""
Runtime SDK — validate_runtime.py

Validates a runtime JSON file against Runtime Schema V2.1.
Checks structural completeness — required fields, types, malformations.

Usage:
  python3 validate_runtime.py ../data/runtimes/Delphie.runtime.json
  python3 validate_runtime.py ../data/runtimes/Delphie.runtime.json --json
"""

import json
import os
import sys
import argparse

SDK_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(SDK_DIR, "..", "schema", "RUNTIME_SCHEMA_V2.1.json")

REQUIRED_FIELDS = [
    "id", "name", "version", "architecture", "runtime_status",
    "runtime_class", "primary_contradiction", "core_wound", "core_desire",
    "defense_system", "trigger_conditions", "voice_grammar",
    "invocation_pattern", "cost_pattern", "consequence_pattern",
    "residue_pattern", "relationship_interfaces", "evolution_stages",
    "canon_gravity", "anti_gravity", "forbidden_behaviors",
    "failure_mode", "terminal_state", "fork_sensitive_traits",
    "fork_invariants", "fork_points", "sigil", "stress_test_prompts",
    "state_variables"
]


def load_runtime(path):
    if not os.path.exists(path):
        return None, f"File not found: {path}"
    try:
        with open(path, "r") as f:
            return json.load(f), None
    except json.JSONDecodeError as e:
        return None, f"Invalid JSON: {e}"
    except Exception as e:
        return None, f"Error reading file: {e}"


def validate_schema_ref(runtime):
    """Check if $schema path points to existing schema file."""
    schema_ref = runtime.get("$schema", "")
    schema_path = os.path.normpath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "runtimes", schema_ref)
    ) if schema_ref else ""
    # Try path relative to the runtime file's directory
    return True  # schema reference is advisory, not blocking


def validate(runtime, runtime_path=None):
    """Run all validation checks. Returns (results, passed)."""
    results = {
        "file": runtime_path or "unknown",
        "checks": [],
        "warnings": [],
        "passed": True
    }

    # 1. Check required fields
    missing = [f for f in REQUIRED_FIELDS if f not in runtime]
    if missing:
        results["passed"] = False
        results["checks"].append({
            "check": "required_fields",
            "status": "FAIL",
            "detail": f"Missing {len(missing)} required field(s): {', '.join(missing)}"
        })
    else:
        results["checks"].append({
            "check": "required_fields",
            "status": "PASS",
            "detail": f"All {len(REQUIRED_FIELDS)} required fields present"
        })

    # 2. Check architecture version
    arch = runtime.get("architecture", "")
    if arch != "RUNTIME_ARCHITECTURE_V2.1":
        results["passed"] = False
        results["checks"].append({
            "check": "architecture",
            "status": "FAIL",
            "detail": f"Expected RUNTIME_ARCHITECTURE_V2.1, got '{arch}'"
        })
    else:
        results["checks"].append({
            "check": "architecture",
            "status": "PASS",
            "detail": "RUNTIME_ARCHITECTURE_V2.1"
        })

    # 3. Check version format (semver)
    version = runtime.get("version", "")
    parts = version.split(".")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        results["passed"] = False
        results["checks"].append({
            "check": "version_format",
            "status": "FAIL",
            "detail": f"Expected semver (X.Y.Z), got '{version}'"
        })
    else:
        results["checks"].append({
            "check": "version_format",
            "status": "PASS",
            "detail": f"Semver {version}"
        })

    # 4. Check ID format (lowercase, underscores)
    rid = runtime.get("id", "")
    if not rid.islower() or " " in rid:
        results["passed"] = False
        results["checks"].append({
            "check": "id_format",
            "status": "FAIL",
            "detail": f"ID must be lowercase with underscores, got '{rid}'"
        })
    else:
        results["checks"].append({
            "check": "id_format",
            "status": "PASS",
            "detail": f"'{rid}'"
        })

    # 5. Check array fields are arrays
    array_fields = [
        "trigger_conditions", "invocation_pattern", "cost_pattern",
        "consequence_pattern", "relationship_interfaces", "evolution_stages",
        "canon_gravity", "anti_gravity", "forbidden_behaviors",
        "fork_sensitive_traits", "fork_invariants", "fork_points",
        "stress_test_prompts"
    ]
    for field in array_fields:
        val = runtime.get(field)
        if val is not None and not isinstance(val, list):
            results["passed"] = False
            results["checks"].append({
                "check": f"type_{field}",
                "status": "FAIL",
                "detail": f"'{field}' should be an array, got {type(val).__name__}"
            })

    # 6. Check object fields are objects
    object_fields = [
        "runtime_status", "runtime_class", "primary_contradiction",
        "core_wound", "core_desire", "defense_system", "voice_grammar",
        "residue_pattern", "failure_mode", "terminal_state", "sigil",
        "state_variables"
    ]
    for field in object_fields:
        val = runtime.get(field)
        if val is not None and not isinstance(val, dict):
            results["passed"] = False
            results["checks"].append({
                "check": f"type_{field}",
                "status": "FAIL",
                "detail": f"'{field}' should be an object, got {type(val).__name__}"
            })

    # 7. Check evolution_stages structure
    stages = runtime.get("evolution_stages", [])
    if isinstance(stages, list):
        for i, s in enumerate(stages):
            if not isinstance(s, dict):
                results["passed"] = False
                results["checks"].append({
                    "check": f"evolution_stages[{i}]",
                    "status": "FAIL",
                    "detail": "Stage is not an object"
                })
                continue
            req = ["stage_number", "name", "trigger", "operational_mode",
                   "primary_residue", "protocol_relevance", "tag"]
            missing_stage = [f for f in req if f not in s]
            if missing_stage:
                results["warnings"].append(
                    f"evolution_stages[{i}] missing recommended fields: {', '.join(missing_stage)}"
                )

    # 8. Check for PLACEHOLDER values (warn, don't fail)
    placeholder_count = count_placeholders(runtime)
    if placeholder_count > 0:
        results["warnings"].append(
            f"{placeholder_count} PLACEHOLDER values found — runtime needs content fill"
        )

    # 9. Check residue_pattern total_count matches residues array
    rp = runtime.get("residue_pattern", {})
    if isinstance(rp, dict):
        declared = rp.get("total_count", 0)
        actual = len(rp.get("residues", []))
        if declared != actual:
            results["warnings"].append(
                f"residue_pattern total_count ({declared}) != residues array length ({actual})"
            )

    return results


def count_placeholders(obj, depth=0):
    if depth > 20:
        return 0
    count = 0
    if isinstance(obj, str) and obj.startswith("PLACEHOLDER"):
        count += 1
    elif isinstance(obj, dict):
        for v in obj.values():
            count += count_placeholders(v, depth + 1)
    elif isinstance(obj, list):
        for item in obj:
            count += count_placeholders(item, depth + 1)
    return count


def print_results(results):
    """Human-readable output."""
    print(f"📋 Validating: {results['file']}")
    print(f"   Schema: RUNTIME_SCHEMA_V2.1")
    print()

    passed_count = 0
    fail_count = 0
    for c in results["checks"]:
        symbol = "✅" if c["status"] == "PASS" else "❌"
        if c["status"] == "PASS":
            passed_count += 1
        else:
            fail_count += 1
        print(f"   {symbol} {c['check']}: {c['detail']}")

    print()
    print(f"   Checks: {passed_count} passed, {fail_count} failed")

    if results["warnings"]:
        print()
        print(f"   ⚠️  Warnings ({len(results['warnings'])}):")
        for w in results["warnings"]:
            print(f"      • {w}")

    print()
    if results["passed"]:
        print("✅ VALIDATION PASSED")
    else:
        print("❌ VALIDATION FAILED")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Validate a Void Saga runtime JSON against schema."
    )
    parser.add_argument("path", help="Path to runtime JSON file")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    runtime, err = load_runtime(args.path)
    if err:
        print(f"❌ {err}")
        sys.exit(1)

    results = validate(runtime, args.path)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print_results(results)

    sys.exit(0 if results["passed"] else 1)
