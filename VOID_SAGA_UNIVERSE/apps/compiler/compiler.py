#!/usr/bin/env python3
"""
Void Saga Narrative Compiler — v0.1.0 (First Light)

Runs the constraint engine, gates on verdict, produces stub narrative.
No external LLM yet. Shows what WOULD be sent to an LLM.

Usage:
  python compiler.py <scenario_path>
  python compiler.py <scenario_path> --json
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "engine"))

from engine_v2 import execute as engine_execute
from lib.context import build_context
from lib.loader import load_runtimes, load_scenario


def build_stub_story(ctx, result):
    """Generate a stub narrative from runtime data WITHOUT calling an LLM.

    Uses voice samples, relationship data, and scenario context to build
    a template that shows what information is available.
    """
    sc = result.get("scoring", {})
    ce = result.get("constraint_evaluation", {})
    cte = result.get("contract_evaluation", {})

    # Gather character voices
    voices = []
    for pid in ctx.participant_ids:
        p = ctx.participants[pid]
        voices.append({
            "id": pid,
            "name": p.name,
            "stage": f"Stage {p.evolution_stage}: {p.stage_name}",
            "voice_sample": p.voice_sample,
            "sigil": f"{p.sigil_name} ({p.sigil_status})",
        })

    # Gather relationships
    relationships = result.get("relationships_detected", [])

    # Gather forbidden exclusions
    exclusions = []
    for v in ce.get("violations", []):
        if v.get("constraint_type") == "forbidden_behavior":
            exclusions.append(f"DO NOT: {v.get('behavior', '')}")
    for v in cte.get("violations", []):
        exclusions.append(f"DO NOT: {v.get('violation_detail', '')[:120]}")

    # Gather triggered defenses for context
    active_defenses = []
    for t in ce.get("trigger_details", []):
        active_defenses.append(
            f"[{t.get('intensity', '?')}] {t.get('runtime_id', '?')}: "
            f"{t.get('defense', '')}"
        )

    # Build stub narrative
    action = ctx.requested_action
    participant_names = [p.name for p in ctx.participants.values()]

    stub = f"""┌──────────────────────────────────────────────────────────┐
│  STUB NARRATIVE — First Light                            │
│  Not LLM-generated. Context available for generation.    │
└──────────────────────────────────────────────────────────┘

CHARACTERS PRESENT:
"""
    for v in voices:
        stub += f"  {v['name']} ({v['id']}) — {v['stage']}\n"
        stub += f"    Voice: \"{v['voice_sample'][:120]}\"\n"
        stub += f"    Sigil: {v['sigil']}\n"

    stub += f"""
SCENE:
  {action.get('description', 'No description')}

"""
    if active_defenses:
        stub += "ACTIVE DEFENSES:\n"
        for d in active_defenses:
            stub += f"  {d}\n"
        stub += "\n"

    if relationships:
        stub += "RELATIONSHIPS:\n"
        for r in relationships:
            stub += f"  {r['pair']}: {r['symmetry']}\n"
            stub += f"    → {r['a_to_b']}\n"
            stub += f"    ← {r['b_to_a']}\n"
        stub += "\n"

    if exclusions:
        stub += "CONSTRAINT EXCLUSIONS (what NOT to write):\n"
        for e in exclusions:
            stub += f"  ❌ {e[:150]}\n"
        stub += "\n"

    if active_defenses and not exclusions:
        stub += "No constraint violations. All canon boundaries respected.\n\n"

    stub += f"""CONTEXT FOR GENERATION:
  Era: Hydrochoos (ACTIVE)
  Timeline phase: {ctx.timeline_state.get('phase', '?')}
  Pre-chain: {ctx.timeline_state.get('pre_chain', True)}
  Post-resolution: {ctx.timeline_state.get('post_resolution', False)}
  Proximity: {ctx.proximity_state.get('distance', '?')}

CANON SCORE: {sc.get('canon_score', 0)}
EVIDENCE CONFIDENCE: {sc.get('evidence_confidence', 0)}
CANON VERDICT: {sc.get('canon_verdict', '?')}

─── STUB PROSE ───────────────────────────────────────────
[Scene: {', '.join(participant_names)}. {action.get('description', '')[:200]}]

[Generation would use {len(voices)} character voice grammars,
 {len(relationships)} relationship contracts,
 {len(exclusions)} constraint exclusions,
 and {len(active_defenses)} active defense patterns
 to guide LLM prose generation.]
─── END STUB ─────────────────────────────────────────────
"""
    return stub


def build_llm_prompt_blueprint(ctx, result):
    """Show what system prompt + context WOULD be sent to an LLM.

    This is a blueprint — no actual API call. When we integrate Claude,
    this becomes the actual prompt.
    """
    ce = result.get("constraint_evaluation", {})

    # System prompt per character
    system_parts = []
    for pid in ctx.participant_ids:
        p = ctx.participants[pid]
        rt = p.runtime_json

        char_prompt = f"""YOU ARE: {p.name} ({pid})
Evolution Stage: {p.evolution_stage} — {p.stage_name}
Voice Grammar: {json.dumps(p.voice_grammar, ensure_ascii=False) if isinstance(p.voice_grammar, dict) else str(p.voice_grammar)[:300]}
Sigil: {p.sigil_name} ({p.sigil_status})
Core Wound: {rt.get('core_wound', {}).get('name', '?')}
Primary Contradiction: {rt.get('primary_contradiction', {}).get('thesis', '?')[:200]}
Forbidden Behaviors:"""

        for fb in rt.get("forbidden_behaviors", []):
            char_prompt += f"\n  - {fb['behavior']} (exception: {fb.get('exception', 'none')})"

        system_parts.append(char_prompt)

    system_prompt = "\n\n---\n\n".join(system_parts)

    # Context
    context = {
        "scene": ctx.requested_action.get("description", ""),
        "timeline": ctx.timeline_state,
        "proximity": ctx.proximity_state,
        "active_defenses": [
            {"intensity": t.get("intensity"), "character": t.get("runtime_id"),
             "defense": t.get("defense")}
            for t in ce.get("trigger_details", [])
        ],
        "contracts": result.get("relationships_detected", []),
        "constraint_exclusions": [
            v.get("behavior", v.get("violation_detail", ""))
            for v in ce.get("violations", [])
        ],
    }

    blueprint = f"""┌──────────────────────────────────────────────────────────┐
│  LLM PROMPT BLUEPRINT                                     │
│  This is what WOULD be sent to Claude API.                │
│  No external call made.                                   │
└──────────────────────────────────────────────────────────┘

══════════ SYSTEM PROMPT ══════════
{system_prompt[:3000]}
...

══════════ CONTEXT ════════════════
{json.dumps(context, indent=2, ensure_ascii=False)[:2000]}
...

══════════ OUTPUT SCHEMA ══════════
{{
  "narrative": "Full prose text in Void Saga style...",
  "character_dialogue": {{
    "{ctx.participant_ids[0] if ctx.participant_ids else 'char1'}": ["line1", "line2"],
    "{ctx.participant_ids[1] if len(ctx.participant_ids) > 1 else 'char2'}": ["line1"]
  }},
  "pov_character": "{ctx.participant_ids[0] if ctx.participant_ids else 'unknown'}",
  "tone": "Void Saga — {ctx.canon_mode.get('type', 'canon_replication')}"
}}
"""
    return blueprint


def compile_scenario(scenario_path):
    """Run the full compilation pipeline.

    1. Evaluate via constraint engine
    2. Gate on verdict
    3. Build stub narrative
    4. Build LLM prompt blueprint
    """
    # Step 1: Engine evaluation
    engine_result = engine_execute(scenario_path)

    if engine_result["status"] != "COMPLETED":
        return {
            "status": "BLOCKED",
            "reason": engine_result.get("error", "Engine evaluation failed"),
            "engine_result": engine_result,
        }

    # Step 2: Build context for stub/prompt generation
    scenario, err = load_scenario(scenario_path)
    if err:
        return {"status": "BLOCKED", "reason": err}

    participant_ids = [p["runtime_id"] for p in scenario.get("participants", [])]
    runtimes, err = load_runtimes(participant_ids)
    if err:
        return {"status": "BLOCKED", "reason": err}

    ctx = build_context(scenario, runtimes)

    # Step 3: Hard block gate — check critical violations first
    ce = engine_result.get("constraint_evaluation", {})
    cte = engine_result.get("contract_evaluation", {})
    sc = engine_result.get("scoring", {})
    final_verdict = engine_result.get("final_verdict", "?")
    canon_verdict = sc.get("canon_verdict", "?")

    # Collect all violations from runtime + contracts
    rt_violations = ce.get("violations", [])
    ct_violations = cte.get("violations", [])
    all_violations = rt_violations + ct_violations
    all_warnings = ce.get("warnings", [])

    # HARD BLOCK conditions — any of these = generation blocked
    hard_blocks = []
    for v in all_violations:
        ctype = v.get("constraint_type", "")

        if ctype == "forbidden_behavior":
            hard_blocks.append({
                "type": "forbidden_behavior",
                "severity": "HARD_BLOCK",
                "reason": f"Forbidden behavior violated: {v.get('behavior', '')[:150]}",
                "detail": v,
            })
        elif ctype == "contract_forbidden_state":
            hard_blocks.append({
                "type": "contract_violation",
                "severity": "HARD_BLOCK",
                "reason": f"Contract forbidden state: {v.get('forbidden_state', '')} — {v.get('violation_detail', '')[:150]}",
                "detail": v,
            })
        elif ctype == "anti_gravity":
            hard_blocks.append({
                "type": "anti_gravity",
                "severity": "HARD_BLOCK",
                "reason": f"Anti-gravity violation: {v.get('anti_gravity', '')[:150]}",
                "detail": v,
            })
        elif ctype == "evolution_stage" and v.get("severity") == "ERROR":
            hard_blocks.append({
                "type": "evolution_stage",
                "severity": "HARD_BLOCK",
                "reason": f"Evolution stage violation: {v.get('violation_detail', '')[:150]}",
                "detail": v,
            })

    # SOFT WARNINGS — do not block but flag
    soft_warnings = []
    for w in all_warnings:
        soft_warnings.append({
            "type": w.get("constraint_type", "warning"),
            "severity": "SOFT_WARNING",
            "reason": w.get("invariant", w.get("violation_detail", ""))[:150],
        })

    if hard_blocks:
        return {
            "status": "BLOCKED",
            "blocked": True,
            "reason": f"Hard block: {len(hard_blocks)} critical violation(s) detected.",
            "hard_blocks": hard_blocks,
            "soft_warnings": soft_warnings,
            "canon_score": sc.get("canon_score", 0),
            "canon_verdict": canon_verdict,
            "final_verdict": final_verdict,
            "engine_result": engine_result,
        }

    # Step 4: No hard blocks — safe to generate stub
    stub = build_stub_story(ctx, engine_result)
    prompt_blueprint = build_llm_prompt_blueprint(ctx, engine_result)

    # Step 5: Determine generation mode
    generation_mode = "canon_safe"
    if soft_warnings:
        generation_mode = "caution"
    if canon_verdict == "CANON_WARNING":
        generation_mode = "caution"

    return {
        "status": "COMPLETED",
        "blocked": False,
        "generation_mode": generation_mode,
        "final_verdict": final_verdict,
        "canon_verdict": canon_verdict,
        "canon_score": sc.get("canon_score", 0),
        "evidence_confidence": sc.get("evidence_confidence", 0),
        "hard_blocks": [],
        "soft_warnings": soft_warnings,
        "violations": rt_violations,
        "warnings": all_warnings,
        "allowed_generation_context": {
            "participants": ctx.participant_ids,
            "voice_grammars_loaded": len(ctx.participant_ids),
            "relationships_loaded": len(engine_result.get("relationships_detected", [])),
            "active_defenses": len(ce.get("trigger_details", [])),
            "constraint_exclusions": len(ce.get("violations", [])),
        },
        "stub_story": stub,
        "llm_prompt_blueprint": prompt_blueprint,
        "engine_result": engine_result,
    }


def print_compile_result(result):
    """Pretty-print compilation result."""
    if result["status"] == "BLOCKED":
        print("🛑 GENERATION BLOCKED")
        print(f"   Reason: {result.get('reason', 'Unknown')}")
        hard_blocks = result.get("hard_blocks", [])
        if hard_blocks:
            print(f"   Hard blocks: {len(hard_blocks)}")
            for b in hard_blocks:
                print(f"     🚫 [{b['type']}] {b['reason'][:120]}")
        soft = result.get("soft_warnings", [])
        if soft:
            print(f"   Soft warnings: {len(soft)}")
            for w in soft[:3]:
                print(f"     ⚠️ [{w['type']}] {w['reason'][:100]}")
        print(f"   Canon score: {result.get('canon_score', 0)}")
        return

    mode_icon = {
        "canon_safe": "✅",
        "caution": "⚠️",
        "constrained": "🔒",
    }.get(result["generation_mode"], "○")

    print(f"⚡ Void.OS Compiler v0.1.0 — First Light")
    print(f"   Mode: {result['generation_mode']} {mode_icon}")
    print(f"   Canon Score: {result['canon_score']} | Evidence: {result['evidence_confidence']}")
    print(f"   Verdict: {result['canon_verdict']} | Final: {result['final_verdict']}")
    print()

    ctx = result.get("allowed_generation_context", {})
    print(f"   Generation context:")
    print(f"     Participants: {ctx.get('participants', [])}")
    print(f"     Voice grammars: {ctx.get('voice_grammars_loaded', 0)}")
    print(f"     Relationships: {ctx.get('relationships_loaded', 0)}")
    print(f"     Active defenses: {ctx.get('active_defenses', 0)}")
    print(f"     Constraint exclusions: {ctx.get('constraint_exclusions', 0)}")
    print()

    soft = result.get("soft_warnings", [])
    violations = result.get("violations", [])
    if soft or violations:
        if violations:
            print(f"   ⚠️  Violations ({len(violations)}):")
            for v in violations[:3]:
                print(f"     [{v.get('constraint_type', '?')}] {v.get('behavior', v.get('violation_detail', ''))[:100]}")
        if soft:
            print(f"   💡 Soft warnings ({len(soft)}):")
            for w in soft[:3]:
                print(f"     [{w['type']}] {w['reason'][:100]}")
        print()

    # Print stub story
    if result.get("stub_story"):
        print(result["stub_story"])
        print()

    # Print LLM blueprint summary
    bp = result.get("llm_prompt_blueprint", "")
    if bp:
        lines = bp.split("\n")
        # Print just the header
        for line in lines[:6]:
            print(line)
        print(f"   (Full LLM prompt blueprint: {len(bp)} chars — use --json for complete output)")
        print()


# --- CLI ---

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compiler.py <scenario_path> [--json]")
        print("  scenario_path : Path to scenario JSON file")
        print("  --json        : Output raw JSON (includes full engine result + prompt blueprint)")
        print()
        print("Example:")
        print("  python compiler.py ../engine/scenarios_v2/test_niuniu_sevraya_orbit.json")
        sys.exit(1)

    scenario_path = sys.argv[1]
    output_json = "--json" in sys.argv

    result = compile_scenario(scenario_path)

    if output_json:
        # Strip verbose fields for clean JSON
        clean = {k: v for k, v in result.items()
                 if k not in ("stub_story", "llm_prompt_blueprint")}
        print(json.dumps(clean, indent=2, ensure_ascii=False))
    else:
        print_compile_result(result)
        if result["status"] == "BLOCKED":
            sys.exit(1)
