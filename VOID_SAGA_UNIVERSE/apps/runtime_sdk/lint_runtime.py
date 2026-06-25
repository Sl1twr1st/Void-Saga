#!/usr/bin/env python3
"""
Runtime SDK — lint_runtime.py

Semantic quality linting. Does NOT check schema validity — that's validate_runtime.py.
Reports on coverage, evidence distribution, and structural completeness.

Usage:
  python3 lint_runtime.py ../data/runtimes/Delphie.runtime.json
  python3 lint_runtime.py ../data/runtimes/Delphie.runtime.json --json
  python3 lint_runtime.py ../data/runtimes/Delphie.runtime.json --threshold 0.5
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


def lint(runtime, threshold=0.4):
    """Run semantic lint checks. Returns list of findings."""
    findings = []
    stats = compute_stats(runtime)

    # ---- CRITICAL (missing essential sections) ----

    # Voice grammar — multiple valid shapes (flat characteristics, pre/post split, etc.)
    vg = runtime.get("voice_grammar", {})
    has_characteristics = (
        (vg.get("characteristics") and len(vg.get("characteristics", [])) > 0) or
        (vg.get("pre_restoration") or vg.get("pre_chain")) or
        (vg.get("post_restoration") or vg.get("post_chain"))
    )
    voice_tags = count_tags_in(vg)
    if sum(voice_tags.values()) == 0:
        findings.append({
            "severity": "WARNING",
            "category": "voice_grammar",
            "detail": "No evidence tags in voice_grammar. Tag as [I] if inferred, [E] if from canon dialogue."
        })
    if not has_characteristics:
        findings.append({
            "severity": "WARNING",
            "category": "voice_grammar",
            "detail": "No voice characteristics found (checked: characteristics[], pre_restoration, pre_chain, post_restoration, post_chain). Character may lack distinct voice in generated narrative."
        })
    voice_samples = 0
    for stage in runtime.get("evolution_stages", []):
        vs = stage.get("voice_sample", "")
        if vs and not vs.startswith("PLACEHOLDER"):
            voice_samples += 1
    if voice_samples == 0:
        findings.append({
            "severity": "WARNING",
            "category": "voice_samples",
            "detail": "No non-placeholder voice samples in any evolution stage. Generated dialogue may drift."
        })

    # Forbidden behaviors
    fb = runtime.get("forbidden_behaviors", [])
    if len(fb) == 0:
        findings.append({
            "severity": "ERROR",
            "category": "forbidden_behaviors",
            "detail": "No forbidden behaviors defined. Hard block gate has nothing to enforce."
        })
    elif len(fb) < 3:
        findings.append({
            "severity": "WARNING",
            "category": "forbidden_behaviors",
            "detail": f"Only {len(fb)} forbidden behavior(s). Recommend at least 3 for meaningful gate enforcement."
        })

    # Stress tests
    st = runtime.get("stress_test_prompts", [])
    if len(st) < 3:
        findings.append({
            "severity": "WARNING",
            "category": "stress_tests",
            "detail": f"Only {len(st)} stress test(s). Schema requires 3-5. Minimum 3 recommended."
        })

    # Fork invariants
    fi = runtime.get("fork_invariants", [])
    if len(fi) < 3:
        findings.append({
            "severity": "WARNING",
            "category": "fork_invariants",
            "detail": f"Only {len(fi)} fork invariant(s). Recommend at least 3."
        })

    # State variables
    sv = runtime.get("state_variables", {})
    if len(sv) < 2:
        findings.append({
            "severity": "WARNING",
            "category": "state_variables",
            "detail": f"Only {len(sv)} state variable(s). Recommend at least 2 for state diff engine."
        })

    # Relationships
    rels = runtime.get("relationship_interfaces", [])
    if len(rels) == 0:
        findings.append({
            "severity": "ERROR",
            "category": "relationships",
            "detail": "No relationship interfaces defined. Contract engine has nothing to evaluate."
        })
    elif len(rels) < 3:
        findings.append({
            "severity": "WARNING",
            "category": "relationships",
            "detail": f"Only {len(rels)} relationship(s). Most characters have 5-7."
        })

    # Evolution stages
    stages = runtime.get("evolution_stages", [])
    if len(stages) < 2:
        findings.append({
            "severity": "WARNING",
            "category": "evolution_stages",
            "detail": f"Only {len(stages)} evolution stage(s). Recommend at least 2."
        })

    # Voice samples in stages
    missing_voice = []
    for s in stages:
        vs = s.get("voice_sample", "")
        if not vs or vs.startswith("PLACEHOLDER"):
            missing_voice.append(s.get("name", f"Stage {s.get('stage_number', '?')}"))
    if missing_voice:
        findings.append({
            "severity": "WARNING",
            "category": "voice_samples",
            "detail": f"Missing voice samples in stages: {', '.join(missing_voice)}"
        })

    # ---- EVIDENCE DISTRIBUTION ----

    tags = runtime.get("runtime_status", {}).get("tags", {})
    e_count = tags.get("E", 0)
    i_count = tags.get("I", 0)
    pc_count = tags.get("PC", 0)
    total = e_count + i_count + pc_count

    if total == 0:
        findings.append({
            "severity": "ERROR",
            "category": "evidence",
            "detail": "Zero evidence claims. Runtime has no documented basis in canon."
        })
    else:
        e_ratio = e_count / total if total > 0 else 0
        i_ratio = i_count / total if total > 0 else 0

        if e_ratio < threshold:
            findings.append({
                "severity": "WARNING",
                "category": "evidence_coverage",
                "detail": f"[E] ratio is {e_ratio:.0%} (below {threshold:.0%} threshold). "
                          f"Too many claims are inferred or probable canon."
            })

        if i_ratio > 0.35:
            findings.append({
                "severity": "INFO",
                "category": "evidence_confidence",
                "detail": f"[I] ratio is {i_ratio:.0%}. High inference rate — verify claims against canon."
            })

    # ---- PLACEHOLDER CHECK ----
    placeholder_count = count_placeholders(runtime)
    if placeholder_count > 0:
        findings.append({
            "severity": "ERROR",
            "category": "placeholders",
            "detail": f"{placeholder_count} PLACEHOLDER values still present. Runtime is incomplete."
        })

    return findings, stats


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


def count_tags_in(obj, depth=0):
    """Count [E], [I], [PC] tags recursively."""
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


def compute_stats(runtime):
    """Compute coverage statistics."""
    tags = runtime.get("runtime_status", {}).get("tags", {})
    total = tags.get("E", 0) + tags.get("I", 0) + tags.get("PC", 0)

    rels = runtime.get("relationship_interfaces", [])
    rels_resolved = sum(1 for r in rels if r.get("symmetry_status") != "unresolved")
    rels_with_gravity = sum(1 for r in rels if r.get("canon_gravity_pull"))

    stages = runtime.get("evolution_stages", [])
    stages_with_voice = sum(1 for s in stages
                          if s.get("voice_sample") and not s.get("voice_sample", "").startswith("PLACEHOLDER"))

    fb = runtime.get("forbidden_behaviors", [])
    fb_hard = sum(1 for f in fb if f.get("tag") == "[E]")

    st = runtime.get("stress_test_prompts", [])
    st_with_range = sum(1 for s in st if s.get("expected_canon_score_range"))

    return {
        "name": runtime.get("name", "Unknown"),
        "version": runtime.get("version", "0.0.0"),
        "id": runtime.get("id", "unknown"),
        "evidence": {
            "total": total,
            "E": tags.get("E", 0),
            "I": tags.get("I", 0),
            "PC": tags.get("PC", 0),
            "E_ratio": tags.get("E", 0) / total if total > 0 else 0,
        },
        "relationships": {
            "count": len(rels),
            "resolved": rels_resolved,
            "with_gravity": rels_with_gravity,
        },
        "evolution_stages": {
            "count": len(stages),
            "with_voice_samples": stages_with_voice,
        },
        "forbidden_behaviors": {
            "count": len(fb),
            "hard_blocks": fb_hard,
        },
        "stress_tests": {
            "count": len(st),
            "with_score_range": st_with_range,
        },
        "state_variables": len(runtime.get("state_variables", {})),
        "fork_invariants": len(runtime.get("fork_invariants", [])),
        "fork_points": len(runtime.get("fork_points", [])),
        "placeholders": count_placeholders(runtime),
    }


def print_report(findings, stats):
    """Human-readable lint report."""
    print(f"🔍 Lint: {stats['name']} ({stats['id']}) v{stats['version']}")
    print()

    # Coverage bars (20 chars max)
    def bar(value, max_val, label):
        if max_val == 0:
            return f"{label:22s} [░░░░░░░░░░░░░░░░░░░░] 0%"
        ratio = min(value / max_val, 1.0)
        filled = int(ratio * 20)
        pct = int(ratio * 100)
        return f"{label:22s} [{'█' * filled}{'░' * (20 - filled)}] {pct}%"

    ev = stats["evidence"]
    print("   ┌─ Evidence ─────────────────────────────")
    max_ev = max(ev["total"], 1)
    print(f"   │ {bar(ev['E'], max_ev, '[E] Established')}")
    print(f"   │ {bar(ev['I'], max_ev, '[I] Inferred')}")
    print(f"   │ {bar(ev['PC'], max_ev, '[PC] Probable Canon')}")
    print(f"   │ Total: {ev['total']} claims")
    print(f"   └────────────────────────────────────────")
    print()

    print("   ┌─ Structure ────────────────────────────")
    rels = stats["relationships"]
    print(f"   │ Relationships:       {rels['count']:3d}  ({rels['resolved']} resolved, {rels['with_gravity']} with gravity)")
    stages = stats["evolution_stages"]
    print(f"   │ Evolution Stages:    {stages['count']:3d}  ({stages['with_voice_samples']} with voice samples)")
    fb = stats["forbidden_behaviors"]
    print(f"   │ Forbidden Behaviors: {fb['count']:3d}  ({fb['hard_blocks']} hard blocks)")
    st = stats["stress_tests"]
    print(f"   │ Stress Tests:        {st['count']:3d}  ({st['with_score_range']} with score range)")
    print(f"   │ State Variables:     {stats['state_variables']:3d}")
    print(f"   │ Fork Invariants:     {stats['fork_invariants']:3d}")
    print(f"   │ Fork Points:         {stats['fork_points']:3d}")
    print(f"   │ Placeholders:        {stats['placeholders']:3d}")
    print(f"   └────────────────────────────────────────")
    print()

    if findings:
        errors = [f for f in findings if f["severity"] == "ERROR"]
        warnings = [f for f in findings if f["severity"] == "WARNING"]
        infos = [f for f in findings if f["severity"] == "INFO"]

        print(f"   ┌─ Findings ─────────────────────────────")
        for f in errors:
            print(f"   │ ❌ [{f['category']}] {f['detail']}")
        for f in warnings:
            print(f"   │ ⚠️  [{f['category']}] {f['detail']}")
        for f in infos:
            print(f"   │ ℹ️  [{f['category']}] {f['detail']}")
        print(f"   └────────────────────────────────────────")
        print()

        print(f"   {len(errors)} errors, {len(warnings)} warnings, {len(infos)} info")
    else:
        print(f"   ✅ No issues found.")

    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Semantic linting for Void Saga runtime JSON files."
    )
    parser.add_argument("path", help="Path to runtime JSON file")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument(
        "--threshold", "-t",
        type=float,
        default=0.4,
        help="Minimum [E] evidence ratio before warning (default: 0.4)"
    )
    args = parser.parse_args()

    runtime = load_runtime(args.path)
    findings, stats = lint(runtime, args.threshold)

    if args.json:
        print(json.dumps({"findings": findings, "stats": stats}, indent=2, ensure_ascii=False))
    else:
        print_report(findings, stats)

    # Exit 1 if errors found
    errors = [f for f in findings if f["severity"] == "ERROR"]
    sys.exit(1 if errors else 0)
