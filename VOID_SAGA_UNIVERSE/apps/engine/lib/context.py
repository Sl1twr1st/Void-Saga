"""Multi-runtime context data structures for engine v0.4.0."""

from dataclasses import dataclass, field


@dataclass
class ParticipantState:
    """Resolved state for one participant in a scenario."""
    runtime_id: str
    name: str
    version: str
    architecture: str
    stage_name: str
    voice_grammar: dict
    voice_sample: str
    defense_count: int
    trigger_count: int
    relationship_count: int
    forbidden_behavior_count: int
    sigil_name: str
    sigil_status: str
    evidence_count: int
    inferred_count: int
    probable_canon_count: int
    runtime_json: dict = field(default_factory=dict, repr=False)
    evolution_stage: int = 1
    schema_missing: list = field(default_factory=list)


@dataclass
class MultiRuntimeContext:
    """Complete context for a multi-runtime scenario evaluation."""
    scenario_id: str
    participants: dict  # runtime_id → ParticipantState
    timeline_state: dict
    proximity_state: dict
    requested_action: dict
    canon_mode: dict
    participant_ids: list = field(default_factory=list)
    total_defenses: int = 0
    total_triggers: int = 0
    total_relationships: int = 0
    total_forbidden_behaviors: int = 0
    total_evidence: int = 0
    load_errors: list = field(default_factory=list)
    schema_warnings: list = field(default_factory=list)


def resolve_voice_grammar(runtime, stage_number, pre_chain):
    """Resolve active voice grammar based on evolution stage and timeline state."""
    voice = runtime.get("voice_grammar", {})
    if "pre_restoration" in voice and "post_restoration" in voice:
        if pre_chain or stage_number <= 2:
            return voice["pre_restoration"]
        else:
            return voice["post_restoration"]
    return voice


def build_participant_state(runtime, stage_number, pre_chain):
    """Build a ParticipantState for one runtime at a specific evolution stage."""
    rid = runtime["id"]
    stages = runtime.get("evolution_stages", [])
    stage_data = next((s for s in stages if s["stage_number"] == stage_number), None)

    if not stage_data:
        return None

    voice = resolve_voice_grammar(runtime, stage_number, pre_chain)
    tags = runtime.get("runtime_status", {}).get("tags", {})
    sigil = runtime.get("sigil", {})

    schema_missing = []
    try:
        from .loader import validate_schema
        schema_missing = validate_schema(runtime)
    except Exception:
        pass

    return ParticipantState(
        runtime_id=rid,
        name=runtime.get("name", rid),
        version=runtime.get("version", "unknown"),
        architecture=runtime.get("architecture", "unknown"),
        runtime_json=runtime,
        evolution_stage=stage_number,
        stage_name=stage_data.get("name", f"Stage {stage_number}"),
        voice_grammar=voice,
        voice_sample=stage_data.get("voice_sample", "[no voice sample]"),
        defense_count=len(runtime.get("defense_system", {}).get("secondary_defenses", [])) + 1,
        trigger_count=len(runtime.get("trigger_conditions", [])),
        relationship_count=len(runtime.get("relationship_interfaces", [])),
        forbidden_behavior_count=len(runtime.get("forbidden_behaviors", [])),
        sigil_name=sigil.get("name", "none"),
        sigil_status=sigil.get("status", "none"),
        evidence_count=tags.get("E", 0),
        inferred_count=tags.get("I", 0),
        probable_canon_count=tags.get("PC", 0),
        schema_missing=schema_missing,
    )


def build_context(scenario, runtimes):
    """Build a MultiRuntimeContext from a scenario and loaded runtimes."""
    ctx = MultiRuntimeContext(
        scenario_id=scenario.get("scenario_id", "unknown"),
        participants={},
        timeline_state=scenario.get("timeline_state", {}),
        proximity_state=scenario.get("proximity_state", {}),
        requested_action=scenario.get("requested_action", {}),
        canon_mode=scenario.get("canon_mode", {}),
    )

    for p in scenario.get("participants", []):
        rid = p["runtime_id"]
        rt = runtimes.get(rid)
        if not rt:
            ctx.load_errors.append(f"Runtime '{rid}' not loaded")
            continue

        stage = p.get("evolution_stage", 1)
        pre_chain = scenario.get("timeline_state", {}).get("pre_chain", True)

        pstate = build_participant_state(rt, stage, pre_chain)
        if not pstate:
            ctx.load_errors.append(
                f"Stage {stage} not found for runtime '{rid}'"
            )
            continue

        ctx.participants[rid] = pstate
        ctx.participant_ids.append(rid)
        ctx.total_defenses += pstate.defense_count
        ctx.total_triggers += pstate.trigger_count
        ctx.total_relationships += pstate.relationship_count
        ctx.total_forbidden_behaviors += pstate.forbidden_behavior_count
        ctx.total_evidence += pstate.evidence_count

        if pstate.schema_missing:
            ctx.schema_warnings.append({
                "runtime_id": rid,
                "missing_fields": pstate.schema_missing
            })

    return ctx
