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


# --- LLM Prompt Contract (Task 6C) ---

OUTPUT_SCHEMA = {
    "type": "object",
    "required": ["narrative", "character_lines", "pov_character", "canon_compliance_notes"],
    "properties": {
        "narrative": {
            "type": "string",
            "description": "Full scene prose in Void Saga style. 150-500 words. Indonesian or English as appropriate to character voices."
        },
        "character_lines": {
            "type": "object",
            "description": "Map of character_id → list of dialogue lines spoken in this scene.",
            "additionalProperties": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "pov_character": {
            "type": "string",
            "description": "Character ID whose perspective the narrative follows."
        },
        "canon_compliance_notes": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Brief notes on how this narrative respects canon constraints."
        }
    }
}


def build_llm_prompt(ctx, result):
    """Build the complete LLM prompt contract — ready for API integration.

    Returns a dict with system_prompt (string) and user_prompt (string).
    These are the EXACT strings to send to Claude.

    Forbidden behaviors appear ONLY as PROHIBITIONS (DO NOT).
    They are NEVER framed as creative suggestions.
    """
    ce = result.get("constraint_evaluation", {})
    cte = result.get("contract_evaluation", {})
    sc = result.get("scoring", {})

    # ── SYSTEM PROMPT ──────────────────────────────────────
    system = f"""You are Void.OS Narrative Compiler v0.1.0 — First Light.

You write scenes in the Void Saga universe. This is a Narrative Operating System, not a generic chatbot. You are bound by character constraints that have the force of LAW.

═══ UNIVERSE CONTEXT ═══
Era: Hydrochoos (ACTIVE). Ichthyes: TERMINATED.
The Grid maintains form. The Void erases form.
Nodes are wounds that stopped resisting themselves.
The NiuNiu-Sevraya Constant: permanent orbit without merge — distance as preservation.
Void.OS v6.6.6: distributed authorship. No centralized control.
Principle: "Berenang atau tenggelam — dua-duanya sah."

═══ CHARACTER RUNTIMES ═══
"""
    # Per-character system prompt
    for pid in ctx.participant_ids:
        p = ctx.participants[pid]
        rt = p.runtime_json
        voice = p.voice_grammar

        # Voice description
        if isinstance(voice, dict):
            if "tone" in voice:
                voice_desc = voice.get("tone", "") + ". " + ". ".join(voice.get("characteristics", [])[:3])
            elif "status" in voice:
                voice_desc = f"Status: {voice.get('status', '?')}. Medium: {voice.get('medium', '?')}. "
                voice_desc += ". ".join(voice.get("characteristics", [])[:3])
            else:
                voice_desc = json.dumps(voice, ensure_ascii=False)[:300]
        else:
            voice_desc = str(voice)[:300]

        system += f"""── {p.name} ({pid}) ──
Stage: {p.evolution_stage} — {p.stage_name}
Sigil: {p.sigil_name} ({p.sigil_status})
Voice: {voice_desc}
Voice Sample: "{p.voice_sample[:150]}"
Core Wound: {rt.get('core_wound', {}).get('name', '?')}
Primary Contradiction: {rt.get('primary_contradiction', {}).get('thesis', '?')[:200]}

"""

    # Forbidden behaviors as PROHIBITIONS ONLY
    system += "═══ ABSOLUTE PROHIBITIONS ═══\n"
    system += "The following MUST NOT appear in ANY generated narrative.\n"
    system += "These are HARD CONSTRAINTS, not creative suggestions.\n\n"

    for pid in ctx.participant_ids:
        p = ctx.participants[pid]
        rt = p.runtime_json
        for fb in rt.get("forbidden_behaviors", []):
            if fb.get("tag") == "[E]":
                system += f"DO NOT write {p.name} {fb['behavior'][0].lower() + fb['behavior'][1:]}\n"
            else:
                system += f"AVOID writing {p.name} {fb['behavior'][0].lower() + fb['behavior'][1:]} [tag: {fb.get('tag', '[I]')}]\n"

    # Anti-gravity as prohibitions
    system += "\n═══ ANTI-GRAVITY (MUST NOT HAPPEN) ═══\n"
    for pid in ctx.participant_ids:
        p = ctx.participants[pid]
        rt = p.runtime_json
        for ag in rt.get("anti_gravity", []):
            system += f"DO NOT: {ag}\n"

    # Contract prohibitions
    contracts = result.get("relationships_detected", [])
    if contracts:
        system += "\n═══ RELATIONSHIP CONTRACTS ═══\n"
        for c in contracts:
            system += f"{c['pair']} ({c['symmetry']}): {c['a_to_b']}\n"

    system += f"""
═══ OUTPUT FORMAT ═══
You MUST respond with valid JSON matching this schema:
{json.dumps(OUTPUT_SCHEMA, indent=2, ensure_ascii=False)}

═══ CANON COMPLIANCE ═══
Canon Score: {sc.get('canon_score', 0)}
Evidence Confidence: {sc.get('evidence_confidence', 0)}
Generation Mode: {result.get('generation_mode', 'canon_safe')}

Write within canon boundaries. Respect all prohibitions.
The engine has validated these constraints. Do not violate them.
"""

    # ── USER PROMPT ────────────────────────────────────────
    action = ctx.requested_action
    timeline = ctx.timeline_state
    proximity = ctx.proximity_state

    # Active defense context
    defense_text = ""
    for t in ce.get("trigger_details", []):
        if t.get("intensity") in ("HIGH", "CRITICAL", "INVOLUNTARY"):
            defense_text += f"- [{t.get('intensity')}] {t.get('runtime_id')}: {t.get('defense', '')}\n"

    # Soft warnings context
    warning_text = ""
    for w in result.get("soft_warnings", []):
        warning_text += f"- [{w['type']}] {w['reason'][:150]}\n"

    user = f"""Write a scene in Void Saga style.

SCENE: {action.get('description', '')}

TIMELINE: Phase {timeline.get('phase', '?')}, {'pre-chain' if timeline.get('pre_chain') else 'post-chain'}{', post-resolution' if timeline.get('post_resolution') else ''}
PROXIMITY: {proximity.get('distance', '?')}
POV CHARACTER: {ctx.participant_ids[0] if ctx.participant_ids else 'unknown'}"""

    if defense_text:
        user += f"""

ACTIVE DEFENSES (these character patterns are currently triggered):
{defense_text}"""

    if warning_text:
        user += f"""

CAUTION — SOFT WARNINGS (be mindful of these):
{warning_text}"""

    user += """

Write 150-500 words. Stay in character voice. Respect all prohibitions.
Return valid JSON only. No preamble, no explanation outside the JSON."""

    return {
        "system_prompt": system,
        "user_prompt": user,
        "total_chars": len(system) + len(user),
        "output_schema": OUTPUT_SCHEMA,
    }


def build_llm_prompt_blueprint(ctx, result):
    """DEPRECATED — kept for compatibility. Use build_llm_prompt() instead."""
    prompt = build_llm_prompt(ctx, result)
    return f"""┌──────────────────────────────────────────────────────────┐
│  LLM PROMPT CONTRACT — Task 6C                            │
│  Ready for API integration. Use --dry-run to view.       │
└──────────────────────────────────────────────────────────┘

═══ SYSTEM PROMPT ({len(prompt['system_prompt'])} chars) ═══
{prompt['system_prompt'][:3000]}
...

═══ USER PROMPT ({len(prompt['user_prompt'])} chars) ═══
{prompt['user_prompt'][:2000]}
...

═══ OUTPUT SCHEMA ═══
{json.dumps(prompt['output_schema'], indent=2, ensure_ascii=False)}
"""


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

    # Step 4: Build stub + prompt contract
    stub = build_stub_story(ctx, engine_result)
    llm_prompt = build_llm_prompt(ctx, engine_result)

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
        "llm_prompt": llm_prompt,
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

    # LLM prompt summary
    llm = result.get("llm_prompt", {})
    if llm:
        print(f"   ┌─ LLM Prompt Contract ────────────────────────")
        print(f"   │ System prompt: {len(llm.get('system_prompt', ''))} chars")
        print(f"   │ User prompt: {len(llm.get('user_prompt', ''))} chars")
        print(f"   │ Total: {llm.get('total_chars', 0)} chars")
        print(f"   │ Output schema: {len(json.dumps(llm.get('output_schema', {})))} chars")
        print(f"   │ Use --dry-run to view full prompt")
        print(f"   └────────────────────────────────────────────")
        print()


# --- CLI ---

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compiler.py <scenario_path> [--json] [--dry-run]")
        print("  scenario_path : Path to scenario JSON file")
        print("  --json        : Output raw JSON")
        print("  --dry-run     : Print full LLM prompt without calling API")
        print()
        print("Example:")
        print("  python compiler.py ../engine/scenarios_v2/test_niuniu_sevraya_orbit.json --dry-run")
        sys.exit(1)

    scenario_path = sys.argv[1]
    output_json = "--json" in sys.argv
    dry_run = "--dry-run" in sys.argv

    result = compile_scenario(scenario_path)

    if output_json:
        clean = {k: v for k, v in result.items()
                 if k not in ("stub_story", "llm_prompt")}
        print(json.dumps(clean, indent=2, ensure_ascii=False))
    elif dry_run and result["status"] == "COMPLETED":
        llm = result.get("llm_prompt", {})
        if llm:
            print("═══ SYSTEM PROMPT ═══")
            print(llm.get("system_prompt", "No system prompt"))
            print("\n═══ USER PROMPT ═══")
            print(llm.get("user_prompt", "No user prompt"))
            print(f"\n═══ METADATA ═══")
            print(f"Total chars: {llm.get('total_chars', 0)}")
            print(f"Output schema: {json.dumps(llm.get('output_schema', {}), indent=2, ensure_ascii=False)}")
    else:
        print_compile_result(result)
        if result["status"] == "BLOCKED":
            sys.exit(1)
