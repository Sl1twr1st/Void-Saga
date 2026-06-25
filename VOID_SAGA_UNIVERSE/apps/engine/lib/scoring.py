"""Canon score and evidence confidence aggregation for engine v0.4.0 Phase 2C.

Computes two-dimensional scoring:
- canon_score: how well the scenario conforms to canon constraints (0.0–1.0)
- evidence_confidence: how much of the constraint data is [E] vs [I]/[PC] (0.0–1.0)
"""


# Per-constraint-type weights for canon score penalty
VIOLATION_WEIGHTS = {
    "forbidden_behavior": 0.4,
    "identity_invariant": 0.35,
    "relationship_contract": 0.3,       # not currently implemented separately
    "anti_gravity": 0.5,
    "contract_forbidden_state": 0.3,    # contract violations
    "contract_violation_rule": 0.25,
    "defense_trigger": 0.2,             # triggered defenses are informational, not violations
}


def severity_multiplier(severity):
    """Convert severity label to numeric multiplier."""
    return 1.0 if severity == "ERROR" else 0.5


def compute_evidence_confidence(ctx):
    """Compute evidence confidence from E/I/PC tag ratios across all participants.

    evidence_confidence = E_total / (E_total + I_total + PC_total)

    Returns (score, breakdown).
    """
    e_total, i_total, pc_total = 0, 0, 0
    per_runtime = {}

    for rid, p in ctx.participants.items():
        e = p.evidence_count
        i = p.inferred_count
        pc = p.probable_canon_count
        e_total += e
        i_total += i
        pc_total += pc
        total = e + i + pc
        per_runtime[rid] = {
            "E": e, "I": i, "PC": pc,
            "ratio": round(e / total, 2) if total > 0 else 0.0
        }

    total = e_total + i_total + pc_total
    confidence = round(e_total / total, 2) if total > 0 else 0.5

    return confidence, {
        "E_total": e_total,
        "I_total": i_total,
        "PC_total": pc_total,
        "total_claims": total,
        "per_runtime": per_runtime
    }


def compute_canon_score(runtime_violations, runtime_warnings, contract_violations, total_constraints):
    """Compute canon score from violations and warnings.

    canon_score = 1.0 - sum(weight_i × severity_i) / max(total_constraints, 1)

    Returns (score, penalty_breakdown).
    """
    total_penalty = 0.0
    breakdown = []

    # Runtime violations
    for v in runtime_violations:
        ctype = v.get("constraint_type", "unknown")
        sev = v.get("severity", "ERROR")
        weight = VIOLATION_WEIGHTS.get(ctype, 0.2)
        penalty = weight * severity_multiplier(sev)
        total_penalty += penalty
        breakdown.append({
            "source": "runtime_violation",
            "constraint_type": ctype,
            "runtime_id": v.get("runtime_id", "?"),
            "severity": sev,
            "weight": weight,
            "penalty": round(penalty, 2),
            "detail": v.get("behavior", v.get("anti_gravity", v.get("violation_detail", "")))[:100]
        })

    # Runtime warnings
    for w in runtime_warnings:
        ctype = w.get("constraint_type", "unknown")
        weight = VIOLATION_WEIGHTS.get(ctype, 0.15)
        penalty = weight * 0.5  # WARNING is always 0.5 severity
        total_penalty += penalty
        breakdown.append({
            "source": "runtime_warning",
            "constraint_type": ctype,
            "runtime_id": w.get("runtime_id", "?"),
            "severity": "WARNING",
            "weight": weight,
            "penalty": round(penalty, 2),
            "detail": w.get("invariant", w.get("violation_detail", ""))[:100]
        })

    # Contract violations
    for v in contract_violations:
        ctype = v.get("constraint_type", "contract_forbidden_state")
        sev = v.get("severity", "ERROR")
        weight = VIOLATION_WEIGHTS.get(ctype, 0.3)
        penalty = weight * severity_multiplier(sev)
        total_penalty += penalty
        breakdown.append({
            "source": "contract_violation",
            "constraint_type": ctype,
            "contract_id": v.get("contract_id", "?"),
            "severity": sev,
            "weight": weight,
            "penalty": round(penalty, 2),
            "detail": v.get("violation_detail", "")[:100]
        })

    # Clamp and compute
    total_constraints = max(total_constraints, 1)
    score = 1.0 - (total_penalty / total_constraints)
    score = round(max(0.0, min(1.0, score)), 2)

    return score, {
        "total_penalty": round(total_penalty, 2),
        "total_constraints_checked": total_constraints,
        "formula": f"1.0 - ({round(total_penalty, 2)} / {total_constraints})",
        "items": breakdown
    }


def determine_canon_verdict(canon_score):
    """Map canon_score to a human-readable verdict."""
    if canon_score >= 0.95:
        return "CANON_PASS"
    elif canon_score >= 0.8:
        return "CANON_WARNING"
    else:
        return "CANON_VIOLATION"


def compute_total_constraints_checked(ctx):
    """Count total constraints available for evaluation.

    Sums triggers, forbidden behaviors, anti-gravity items across all participants.
    This is the denominator for canon_score normalization.
    """
    total = 0
    for rid, p in ctx.participants.items():
        total += p.trigger_count
        total += p.forbidden_behavior_count
        # Anti-gravity count from runtime JSON
        rt = p.runtime_json
        if rt:
            total += len(rt.get("anti_gravity", []))
    # Add contract states checked
    # (contracts are counted separately but we want a reasonable baseline)
    return max(total, 1)


def aggregate_scores(ctx, runtime_violations, runtime_warnings, contract_violations):
    """Compute full two-dimensional score from all evaluation results.

    Returns (canon_score, evidence_confidence, canon_verdict, score_details).
    """
    # Evidence confidence
    evidence_conf, evidence_breakdown = compute_evidence_confidence(ctx)

    # Total constraints checked
    total = compute_total_constraints_checked(ctx)

    # Canon score
    c_score, penalty_breakdown = compute_canon_score(
        runtime_violations, runtime_warnings, contract_violations, total
    )

    # Verdict
    verdict = determine_canon_verdict(c_score)

    details = {
        "canon_score": c_score,
        "evidence_confidence": evidence_conf,
        "canon_verdict": verdict,
        "evidence_breakdown": evidence_breakdown,
        "penalty_breakdown": penalty_breakdown,
        "total_constraints": total,
    }

    return c_score, evidence_conf, verdict, details
