#!/usr/bin/env python3
"""
Fork Checker — v0.2 with language bridge for Bab 00 fork verification.

Reads a fork record JSON, evaluates it against Bab 00 laws,
and returns a verdict: PASS / PRICE_REQUIRED / BLOCKED / VALID_FORK.

Usage:
    python3 mvp/checker/check_fork.py mvp/forks/fork-01-pass.json
    python3 mvp/checker/check_fork.py path/to/fork.json --laws mvp/laws/bab00-laws.json

Design principle:
    The language model is not the authority. The universe is.
    This checker is rule-based for MVP. It evaluates what the fork record claims
    against the law definitions.

v0.2 Language Bridge:
    Indonesian is the user-facing layer.
    English (internal_summary_en) is the temporary internal bridge.
    The checker is NOT truly multilingual yet — IA fields are surface-only.
    No embeddings. No LLM calls. No AI generation.
"""

import json
import sys
import os
from pathlib import Path

# ─── Paths ───────────────────────────────────────────────────────────
MVP_DIR = Path(__file__).resolve().parent.parent
DEFAULT_LAWS_PATH = MVP_DIR / "laws" / "bab00-laws.json"
DEFAULT_GENESIS_PATH = MVP_DIR / "genesis" / "bab00.node.json"
DEFAULT_FORK_POINTS_PATH = MVP_DIR / "genesis" / "fork-points.json"


# ─── Loaders ──────────────────────────────────────────────────────────
def load_json(path):
    """Load and return parsed JSON from path."""
    p = Path(path)
    if not p.exists():
        print(f"ERROR: File not found: {p}")
        sys.exit(1)
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def load_laws(path=None):
    """Load law definitions."""
    return load_json(path or DEFAULT_LAWS_PATH)


def load_genesis_node(path=None):
    """Load genesis node metadata."""
    return load_json(path or DEFAULT_GENESIS_PATH)


def load_fork_points(path=None):
    """Load fork point definitions."""
    return load_json(path or DEFAULT_FORK_POINTS_PATH)


# ─── Core Logic ───────────────────────────────────────────────────────
def build_law_index(laws):
    """Build {law_id: law_def} index."""
    return {law["law_id"]: law for law in laws}


def build_fork_point_index(fork_points):
    """Build {fork_point_id: fork_point_def} index."""
    return {fp["fork_point_id"]: fp for fp in fork_points}


def evaluate_fork(fork_record, law_index, fork_point_index=None, genesis_node=None):
    """
    Evaluate a fork record against the law index.

    Returns a verdict dict with:
        - verdict: PASS | PRICE_REQUIRED | BLOCKED | VALID_FORK
        - blocked_by: list of blocking violations (if BLOCKED)
        - prices: list of price-required violations (if PRICE_REQUIRED)
        - touched_laws_detail: list of all touched laws with evaluation
        - reason: human-readable explanation
        - status: valid | blocked
    """
    violations = fork_record.get("violations", [])
    touched_law_ids = fork_record.get("touched_laws", [])
    fork_id = fork_record.get("fork_id", "unknown")
    # v0.2 bridge: prefer internal_summary_en for internal evaluation;
    # fall back to change field for backward compatibility
    change = fork_record.get("internal_summary_en") or fork_record.get("change", "")
    has_bridge = bool(fork_record.get("internal_summary_en"))
    has_indonesian = bool(fork_record.get("title_id"))

    blocked_by = []
    prices = []
    touched_detail = []
    untouched_detail = []

    # Evaluate explicit violations
    for v in violations:
        law_id = v.get("law_id", "")
        law = law_index.get(law_id)

        if law is None:
            touched_detail.append({
                "law_id": law_id,
                "law_name": "UNKNOWN LAW",
                "violated": True,
                "severity": v.get("severity", "unknown"),
                "warning": f"Law '{law_id}' not found in law index. Verify law exists."
            })
            continue

        entry = {
            "law_id": law_id,
            "law_name": law["name"],
            "statement": law["statement"],
            "violated": True,
            "severity": v.get("severity", "unspecified"),
            "description": v.get("description", ""),
            "block_on_violate": law.get("block_on_violate", False),
            "price_on_violate": law.get("price_on_violate", False),
        }

        if law.get("block_on_violate", False):
            blocked_by.append(entry)
        elif law.get("price_on_violate", False):
            prices.append(entry)

        touched_detail.append(entry)

    # Evaluate touched laws that were NOT explicitly violated
    # (they were touched but the fork claims no violation)
    violated_law_ids = {v.get("law_id") for v in violations}
    for law_id in touched_law_ids:
        if law_id not in violated_law_ids:
            law = law_index.get(law_id)
            if law:
                untouched_detail.append({
                    "law_id": law_id,
                    "law_name": law["name"],
                    "statement": law["statement"],
                    "violated": False,
                    "note": "Touched but not violated — fork remains compliant with this law."
                })

    # Determine verdict
    if blocked_by:
        # Find the primary block reason (first critical, then highest severity)
        critical_blocks = [b for b in blocked_by if b.get("severity") == "critical"]
        primary = critical_blocks[0] if critical_blocks else blocked_by[0]

        verdict = "BLOCKED"
        reason = (
            f"BLOCKED: {primary['law_name']} is a hard-block law. "
            f"{primary.get('description', 'Violation detected.')} "
            f"This fork cannot proceed because it destroys a foundational property "
            f"of the Void Saga universe."
        )
        status = "blocked"

    elif prices:
        price_laws = [p["law_name"] for p in prices]
        reason = (
            f"PRICE_REQUIRED: Violation of {', '.join(price_laws)}. "
            f"The universe permits this divergence, but it carries narrative cost. "
            f"See fork record 'price' field for required payments."
        )
        verdict = "PRICE_REQUIRED"
        status = "valid"

    elif not violations and change:
        # No violations at all — could be PASS or VALID_FORK
        # VALID_FORK: substantial change but no law broken, meaningful downstream effects
        # PASS: trivial/small change, everything intact, no structural divergence

        downstream = fork_record.get("lineage", {}).get("downstream_effects", [])

        # Check for structural divergence markers
        structural_markers = [
            "No structural difference",
            "nothing downstream",
            "changes nothing downstream",
            "no structural",
            "hanya",
            "cuma",
        ]
        has_structural_change = len(downstream) > 0 and not any(
            any(marker.lower() in str(e).lower() for marker in structural_markers)
            for e in downstream
        )

        # If fork has its own expected verdict, respect it for edge cases
        expected = fork_record.get("verdict", "")

        if expected == "PASS" or not has_structural_change:
            verdict = "PASS"
            reason = (
                f"PASS: No law violated. The change is within normal behavioral range. "
                f"The canon remains intact."
            )
        else:
            verdict = "VALID_FORK"
            reason = (
                f"VALID_FORK: This fork introduces meaningful divergence without "
                f"violating any Bab 00 law. All touched laws remain intact. "
                f"The fork is a legitimate branch of the canon tree."
            )
        status = "valid"

    else:
        verdict = "PASS"
        reason = "PASS: No violations detected. No change specified."
        status = "valid"

    return {
        "fork_id": fork_id,
        "verdict": verdict,
        "status": status,
        "reason": reason,
        "blocked_by": blocked_by if blocked_by else None,
        "prices": prices if prices else None,
        "touched_laws_detail": touched_detail + untouched_detail,
        "total_laws_touched": len(touched_law_ids),
        "total_violations": len(violations),
        # v0.2 bridge metadata
        "has_bridge": has_bridge,
        "has_indonesian": has_indonesian,
    }


# ─── Output Formatters ────────────────────────────────────────────────
def format_banner(fork_record):
    """Format the fork banner. Prefers title_id (Indonesian) when available."""
    fp = fork_record.get("fork_point", "unknown")
    # v0.2 bridge: show Indonesian title first when available
    title_id = fork_record.get("title_id", "")
    title_en = fork_record.get("title", "Untitled Fork")
    display_title = title_id if title_id else title_en

    banner = f"""
╔══════════════════════════════════════════════════════════════╗
║  FORK CHECK — invariant-engine                              ║
║  Genesis Node: {fork_record.get('parent_node', 'unknown'):<44} ║
║  Fork Point:   {fp:<44} ║
║  Title:        {display_title[:46]:<46} ║
╚══════════════════════════════════════════════════════════════╝
"""
    return banner


def format_lineage(fork_record):
    """Format lineage information."""
    lineage = fork_record.get("lineage", {})
    if not lineage:
        return ""

    lines = [
        "─── Lineage ─────────────────────────────────────────────",
        f"  Forked from:  {lineage.get('forked_from', 'unknown')}",
        f"  Forked at:    {lineage.get('forked_at', 'unknown')}",
        f"  Canon moment: {lineage.get('canon_moment', 'unknown')[:80]}",
        f"",
        f"  Divergence:   {lineage.get('divergence', 'unknown')[:120]}",
        f"",
    ]

    downstream = lineage.get("downstream_effects", [])
    if downstream:
        lines.append("  Downstream effects:")
        for i, effect in enumerate(downstream, 1):
            lines.append(f"    {i}. {effect}")

    return "\n".join(lines)


def format_indonesian_surface(fork_record, result):
    """Format Indonesian user-facing fields when available (v0.2 bridge)."""
    has_id = result.get("has_indonesian", False)
    if not has_id:
        return ""

    lines = ["─── Indonesian Surface (v0.2 bridge) ─────────────────────"]

    premise_id = fork_record.get("premise_id", "")
    change_id = fork_record.get("change_id", "")
    effect_id = fork_record.get("immediate_effect_id", "")

    if premise_id:
        lines.append(f"  Premis:  {premise_id[:110]}")
    if change_id:
        lines.append(f"  Perubahan: {change_id[:108]}")
    if effect_id:
        lines.append(f"  Efek langsung: {effect_id[:105]}")

    return "\n".join(lines)


def format_bridge_note(result):
    """Show bridge status when active (v0.2)."""
    if result.get("has_bridge"):
        return (
            "\n─── Bridge Note ──────────────────────────────────────────\n"
            "  🌐 internal_summary_en digunakan untuk evaluasi internal.\n"
            "  🇮🇩 Kolom Indonesia adalah lapisan pengguna (surface).\n"
            "  ⚠️  Checker ini belum benar-benar multilingual.\n"
            "     internal_summary_en adalah jembatan sementara."
        )
    return ""


def format_law_evaluation(result):
    """Format law-by-law evaluation."""
    touched = result.get("touched_laws_detail", [])
    if not touched:
        return ""

    lines = ["─── Law Evaluation ─────────────────────────────────────"]

    for entry in touched:
        status_icon = "✗" if entry.get("violated") else "✓"
        law_name = entry.get("law_name", "Unknown")
        severity = entry.get("severity", "")
        block = " [HARD BLOCK]" if entry.get("block_on_violate") and entry.get("violated") else ""
        price = " [PRICE]" if entry.get("price_on_violate") and entry.get("violated") and not entry.get("block_on_violate") else ""

        lines.append(f"  {status_icon} {law_name}{block}{price}")
        if entry.get("violated") and entry.get("description"):
            lines.append(f"    → {entry['description'][:100]}")

    return "\n".join(lines)


def format_price(fork_record):
    """Format price information if PRICE_REQUIRED."""
    price = fork_record.get("price")
    if not price:
        return ""

    lines = [
        "",
        "─── Required Price ──────────────────────────────────────",
        f"  Type: {price.get('type', 'PRICE_REQUIRED')}",
        f"  Narrative cost: {price.get('narrative_cost', '')[:120]}",
        "",
    ]

    payments = price.get("required_payments", [])
    if payments:
        lines.append("  Required payments:")
        for i, p in enumerate(payments, 1):
            lines.append(f"    {i}. {p}")

    resistance = price.get("canon_gravity_resistance", "")
    if resistance:
        lines.append(f"")
        lines.append(f"  Canon gravity: {resistance}")

    return "\n".join(lines)


def format_block_detail(result, fork_record):
    """Format block details."""
    blocked = result.get("blocked_by")
    if not blocked:
        return ""

    lines = [
        "",
        "─── Block Details ──────────────────────────────────────",
    ]
    for b in blocked:
        lines.append(f"  Law:    {b['law_name']}")
        lines.append(f"  Reason: {b.get('description', 'No description')[:120]}")

    # Check for downstream contamination
    lineage = fork_record.get("lineage", {})
    downstream = lineage.get("downstream_effects", [])
    if downstream:
        lines.append(f"")
        lines.append(f"  Contaminated downstream ({len(downstream)} effects):")
        for i, effect in enumerate(downstream, 1):
            lines.append(f"    {i}. {effect[:120]}")

    return "\n".join(lines)


def format_verdict(result):
    """Format the final verdict block."""
    verdict = result["verdict"]
    icons = {
        "PASS": "🟢",
        "VALID_FORK": "🔵",
        "PRICE_REQUIRED": "🟡",
        "BLOCKED": "🛑",
    }
    icon = icons.get(verdict, "❓")

    lines = [
        "",
        "═══════════════════════════════════════════════════════════",
        f"  VERDICT: {icon} {verdict}",
        f"  Status:  {result['status']}",
        f"",
        f"  {result['reason']}",
        "═══════════════════════════════════════════════════════════",
    ]
    return "\n".join(lines)


def format_summary(result):
    """Format a summary line."""
    return (
        f"  Laws touched: {result['total_laws_touched']} | "
        f"Violations: {result['total_violations']} | "
        f"Verdict: {result['verdict']}"
    )


# ─── Main ─────────────────────────────────────────────────────────────
def check_fork(fork_path, laws=None, verbose=True):
    """
    Main entry point. Load fork record, evaluate, return result dict.

    Args:
        fork_path: Path to fork record JSON
        laws: Optional path to laws JSON
        verbose: If True, prints formatted output

    Returns:
        dict with verdict, reason, and details
    """
    # Load
    fork_record = load_json(fork_path)
    laws_data = load_laws(laws)
    law_index = build_law_index(laws_data)

    # Optional context
    genesis_node = None
    fork_point_index = None
    try:
        genesis_node = load_genesis_node()
        fork_points = load_fork_points()
        fork_point_index = build_fork_point_index(fork_points)
    except (FileNotFoundError, SystemExit):
        pass  # Context files optional; evaluation can proceed without them

    # Evaluate
    result = evaluate_fork(fork_record, law_index, fork_point_index, genesis_node)

    if verbose:
        print(format_banner(fork_record))
        print(format_indonesian_surface(fork_record, result))
        print(format_lineage(fork_record))
        print(format_law_evaluation(result))
        print(format_price(fork_record))
        print(format_block_detail(result, fork_record))
        print(format_bridge_note(result))
        print(format_verdict(result))

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: check-fork <path/to/fork.json> [--laws path/to/laws.json] [--quiet]")
        print("")
        print("Examples:")
        print("  python3 mvp/checker/check_fork.py mvp/forks/fork-01-pass.json")
        print("  python3 mvp/checker/check_fork.py mvp/forks/fork-02-price.json")
        print("  python3 mvp/checker/check_fork.py mvp/forks/fork-03-blocked.json")
        sys.exit(1)

    fork_path = sys.argv[1]
    laws_path = None
    quiet = False

    # Parse optional flags
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--laws" and i + 1 < len(args):
            laws_path = args[i + 1]
            i += 2
        elif args[i] == "--quiet" or args[i] == "-q":
            quiet = True
            i += 1
        else:
            print(f"Unknown argument: {args[i]}")
            sys.exit(1)

    result = check_fork(fork_path, laws=laws_path, verbose=not quiet)

    # Exit code based on verdict
    if result["verdict"] == "BLOCKED":
        sys.exit(2)
    elif result["verdict"] == "PRICE_REQUIRED":
        sys.exit(3)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
