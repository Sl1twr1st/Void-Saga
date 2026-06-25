#!/usr/bin/env python3
"""
Runtime SDK — evidence_report.py

Authoring diagnostic. Analyzes evidence tag distribution across a runtime.
Prints coverage bars for key sections.

Usage:
  python3 evidence_report.py ../data/runtimes/Delphie.runtime.json
  python3 evidence_report.py ../data/runtimes/Delphie.runtime.json --json
"""

import json
import os
import sys
import argparse


def load_runtime(path):
    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        sys.exit(1)
    with open(path, "r") as f:
        return json.load(f)


def count_tags_in(obj, depth=0):
    """Count [E], [I], [PC] tags recursively in any object."""
    if depth > 20:
        return {"E": 0, "I": 0, "PC": 0}
    counts = {"E": 0, "I": 0, "PC": 0}
    if isinstance(obj, dict):
        tag = obj.get("tag", "")
        if tag == "[E]":
            counts["E"] += 1
        elif tag == "[I]":
            counts["I"] += 1
        elif tag == "[PC]":
            counts["PC"] += 1
        for v in obj.values():
            sub = count_tags_in(v, depth + 1)
            for k in counts:
                counts[k] += sub[k]
    elif isinstance(obj, list):
        for item in obj:
            sub = count_tags_in(item, depth + 1)
            for k in counts:
                counts[k] += sub[k]
    return counts


def analyze(runtime):
    """Full evidence analysis."""
    declared = runtime.get("runtime_status", {}).get("tags", {})
    actual = count_tags_in(runtime)

    # Section-level breakdown
    sections = {}
    for key in runtime:
        if key in ("$schema", "id", "name", "version", "architecture", "canon_baseline",
                    "runtime_status", "runtime_summary", "cross_references",
                    "serialization_notes", "canon_boundaries"):
            continue
        sec_tags = count_tags_in(runtime[key])
        total = sum(sec_tags.values())
        if total > 0:
            sections[key] = sec_tags

    # Evolution stages sub-breakdown
    stage_breakdown = []
    for s in runtime.get("evolution_stages", []):
        stage_tags = count_tags_in(s)
        total = sum(stage_tags.values())
        stage_breakdown.append({
            "stage": s.get("stage_number", "?"),
            "name": s.get("name", "Unknown"),
            "tags": stage_tags,
            "total": total
        })

    # Voice sample coverage
    stages = runtime.get("evolution_stages", [])
    voice_coverage = sum(1 for s in stages
                        if s.get("voice_sample") and not s.get("voice_sample", "").startswith("PLACEHOLDER"))

    # Relationship symmetry coverage
    rels = runtime.get("relationship_interfaces", [])
    sym_dist = {"symmetric": 0, "asymmetric": 0, "unresolved": 0}
    for r in rels:
        status = r.get("symmetry_status", "unresolved")
        sym_dist[status] = sym_dist.get(status, 0) + 1

    return {
        "name": runtime.get("name", "Unknown"),
        "id": runtime.get("id", "unknown"),
        "version": runtime.get("version", "0.0.0"),
        "declared_tags": declared,
        "actual_tags": actual,
        "total_evidence": sum(actual.values()),
        "sections": sections,
        "stage_breakdown": stage_breakdown,
        "voice_coverage": f"{voice_coverage}/{len(stages)}",
        "relationship_symmetry": sym_dist,
        "relationships_total": len(rels),
        "forbidden_behaviors": len(runtime.get("forbidden_behaviors", [])),
        "stress_tests": len(runtime.get("stress_test_prompts", [])),
        "fork_invariants": len(runtime.get("fork_invariants", [])),
        "state_variables": len(runtime.get("state_variables", {})),
    }


def bar_chart(value, max_val, width=20):
    if max_val == 0:
        return "░" * width
    filled = int(min(value / max_val, 1.0) * width)
    return "█" * filled + "░" * (width - filled)


def print_report(analysis):
    """Human-readable evidence report with bars."""
    a = analysis
    total = max(a["total_evidence"], 1)
    d = a["declared_tags"]
    act = a["actual_tags"]

    print(f"📊 Evidence Report: {a['name']} ({a['id']}) v{a['version']}")
    print()

    # Summary
    print("   ┌─ Evidence Summary ──────────────────────")
    print(f"   │ Declared:  E:{d.get('E',0)}  I:{d.get('I',0)}  PC:{d.get('PC',0)}")
    print(f"   │ Actual:    E:{act.get('E',0)}  I:{act.get('I',0)}  PC:{act.get('PC',0)}")
    if d != act:
        print(f"   │ ⚠️  Declared != Actual — update runtime_status.tags")
    print(f"   └──────────────────────────────────────────")
    print()

    # Coverage bars
    print("   ┌─ Coverage ──────────────────────────────")
    max_section = max(
        max(sum(v.values()) for v in a["sections"].values()) if a["sections"] else 1,
        1
    )
    for sec_name, tags in sorted(a["sections"].items()):
        sec_total = sum(tags.values())
        bar = bar_chart(sec_total, max_section)
        tag_str = f"E:{tags.get('E',0)} I:{tags.get('I',0)} PC:{tags.get('PC',0)}"
        print(f"   │ {sec_name:30s} {bar} {tag_str}")
    print(f"   └──────────────────────────────────────────")
    print()

    # Stage breakdown
    print("   ┌─ Evolution Stages ──────────────────────")
    for s in a["stage_breakdown"]:
        st = s["total"]
        bar = bar_chart(st, max(st for s in a["stage_breakdown"]))
        print(f"   │ Stage {s['stage']}: {s['name']:25s} {bar} {st} claims")
    print(f"   └──────────────────────────────────────────")
    print()

    # Structure summary
    print("   ┌─ Structure ─────────────────────────────")
    print(f"   │ Voice samples:     {a['voice_coverage']}")
    rels = a["relationship_symmetry"]
    print(f"   │ Relationships:     {a['relationships_total']} (sym:{rels['symmetric']} asym:{rels['asymmetric']} unres:{rels['unresolved']})")
    print(f"   │ Forbidden:         {a['forbidden_behaviors']}")
    print(f"   │ Stress tests:      {a['stress_tests']}")
    print(f"   │ Fork invariants:   {a['fork_invariants']}")
    print(f"   │ State variables:   {a['state_variables']}")
    print(f"   └──────────────────────────────────────────")
    print()

    # Quick verdict
    e_ratio = act.get("E", 0) / total if total > 0 else 0
    i_ratio = act.get("I", 0) / total if total > 0 else 0

    if e_ratio >= 0.7:
        quality = "✅ STRONG — well-evidenced runtime"
    elif e_ratio >= 0.5:
        quality = "⚠️  ADEQUATE — acceptable but verify [I] claims"
    elif e_ratio >= 0.3:
        quality = "⚠️  WEAK — too many inferred claims, review against canon"
    else:
        quality = "❌ INSUFFICIENT — runtime may not be grounded in canon"

    print(f"   Verdict: {quality}")
    print(f"   [E] ratio: {e_ratio:.0%}  [I] ratio: {i_ratio:.0%}  [PC] ratio: {act.get('PC',0)/total if total else 0:.0%}")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evidence coverage diagnostic for Void Saga runtime JSON files."
    )
    parser.add_argument("path", help="Path to runtime JSON file")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    runtime = load_runtime(args.path)
    analysis = analyze(runtime)

    if args.json:
        print(json.dumps(analysis, indent=2, ensure_ascii=False))
    else:
        print_report(analysis)
