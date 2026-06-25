#!/usr/bin/env python3
"""
Runtime SDK — create_runtime.py

Creates a new runtime JSON file from TEMPLATE.runtime.json.
Fills structural fields (architecture, schema path, version).
Remaining fields use TEMPLATE placeholders — author fills them in.

Usage:
  python3 create_runtime.py Delphie
  python3 create_runtime.py Delphie --output ../data/runtimes/
"""

import json
import os
import sys
import argparse
from datetime import datetime

SDK_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(SDK_DIR, "TEMPLATE.runtime.json")
DEFAULT_OUTPUT = os.path.join(SDK_DIR, "..", "data", "runtimes")


def load_template():
    if not os.path.exists(TEMPLATE_PATH):
        print(f"❌ TEMPLATE not found: {TEMPLATE_PATH}")
        sys.exit(1)
    with open(TEMPLATE_PATH, "r") as f:
        return json.load(f)


def slugify(name):
    """Convert display name to runtime ID."""
    return name.lower().replace(" ", "_").replace("-", "_")


def create_runtime(name, output_dir=DEFAULT_OUTPUT, force=False):
    rid = slugify(name)
    filename = f"{rid.capitalize()}.runtime.json" if rid == name.lower() else f"{name.replace(' ', '_')}.runtime.json"
    # Use the standard naming: {Name}.runtime.json where Name is capitalized
    # For multi-word names like "Dorian Grey" → Dorian_Grey.runtime.json
    filename = f"{name.replace(' ', '_')}.runtime.json"
    output_path = os.path.join(output_dir, filename)

    if os.path.exists(output_path) and not force:
        print(f"❌ File already exists: {output_path}")
        print(f"   Use --force to overwrite.")
        sys.exit(1)

    template = load_template()

    # Fill structural fields
    template["id"] = slugify(name)
    template["name"] = name
    template["version"] = "1.0.0"
    template["architecture"] = "RUNTIME_ARCHITECTURE_V2.1"
    template["canon_baseline"]["audit_basis"] = f"{name}.runtime.md v1.0.0"
    template["$schema"] = "../schema/RUNTIME_SCHEMA_V2.1.json"

    # Set sigil default for non-bearer characters
    template["sigil"]["status"] = "none"

    # Write
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # Count
    required = count_required(template)
    total = len(template)
    placeholders = count_placeholders(template)

    print(f"✅ Created: {output_path}")
    print(f"   ID: {template['id']}")
    print(f"   Name: {template['name']}")
    print(f"   Version: {template['version']}")
    print(f"   Architecture: {template['architecture']}")
    print(f"   Schema: {template['$schema']}")
    print(f"   Required fields: {required}/29")
    print(f"   Total fields: {total}")
    print(f"   Placeholders remaining: {placeholders}")
    print()
    print(f"   Next steps:")
    print(f"   1. Fill in PLACEHOLDER values from {name}.runtime.md")
    print(f"   2. python3 validate_runtime.py {output_path}")
    print(f"   3. python3 lint_runtime.py {output_path}")
    print(f"   4. python3 evidence_report.py {output_path}")
    print(f"   5. Add test scenarios")
    print(f"   6. Run engine validation")

    return output_path


def count_required(runtime):
    required_fields = [
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
    return sum(1 for f in required_fields if f in runtime)


def count_placeholders(obj, depth=0):
    """Count PLACEHOLDER strings recursively."""
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a new Void Saga character runtime from template."
    )
    parser.add_argument("name", help="Character display name (e.g. 'Delphie')")
    parser.add_argument(
        "--output", "-o",
        default=DEFAULT_OUTPUT,
        help=f"Output directory (default: {DEFAULT_OUTPUT})"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Overwrite existing file"
    )
    args = parser.parse_args()

    create_runtime(args.name, args.output, args.force)
