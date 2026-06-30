#!/usr/bin/env python3
"""
Scene Gate Validator — rule-based check on generated fork scenes.

Deterministic. No AI calls. Checks whether a generated scene still
feels like Bab 00 based on voice contract, segment map, and fork record.

Usage:
    python3 mvp/checker/check_scene.py mvp/runs/{slug}/fork-scene.draft.md \\
      --packet mvp/runs/{slug}/scene-prompt-packet.json

Returns JSON with overall PASS/WARNING/FAIL and per-check details.
"""

import json
import re
import sys
from pathlib import Path


def load_json(path):
    p = Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text())


def check_voice_pov(text):
    """Check if the scene uses first-person gua narration."""
    gua_count = len(re.findall(r'\bgua\b', text, re.IGNORECASE))
    lo_count = len(re.findall(r'\blo\b', text, re.IGNORECASE))

    # Count third-person markers (GUA referred to as 'dia'/'ia'/'GUA' in narration)
    dia_refs = len(re.findall(r'\bdia\b', text))
    gua_name_refs = len(re.findall(r'\bGUA\b', text))

    # Strong signal: gua used frequently, not just in dialogue
    has_gua_narration = gua_count >= 3
    has_lo_texture = lo_count >= 2
    third_person_dominant = (dia_refs + gua_name_refs) > (gua_count + lo_count) * 0.5

    # Check for forbidden patterns
    has_aku = bool(re.search(r'\baku\b', text))
    has_saya = bool(re.search(r'\bsaya\b', text))
    has_dia_narration = dia_refs >= 3  # Multiple 'dia' references suggest third-person drift

    issues = []
    if not has_gua_narration:
        issues.append("Scene lacks first-person 'gua' narration. Expected at least 3 uses.")
    if not has_lo_texture:
        issues.append("Scene lacks 'lo' texture — LO should feel present in the prose.")
    if third_person_dominant:
        issues.append("Third-person references ('dia', 'GUA') dominate over first-person ('gua').")
    if has_aku:
        issues.append("Forbidden pronoun 'aku' found. Use 'gua' for GUA narration.")
    if has_saya:
        issues.append("Forbidden pronoun 'saya' found. Use 'gua' for GUA narration.")

    if third_person_dominant and not has_gua_narration:
        status = "FAIL"
    elif third_person_dominant or not has_gua_narration or has_aku or has_saya:
        status = "WARNING"
    else:
        status = "PASS"

    return {
        "id": "voice_pov",
        "label": "GUA POV",
        "status": status,
        "message": f"gua×{gua_count} lo×{lo_count} dia×{dia_refs} GUA×{gua_name_refs}",
        "issues": issues,
    }


def check_paragraph_rhythm(text):
    """Check if paragraphs are short and fragmentary like Bab 00."""
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    if not paragraphs:
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]

    total_paras = len(paragraphs)
    if total_paras == 0:
        return {"id": "paragraph_rhythm", "label": "Paragraph Rhythm", "status": "FAIL",
                "message": "No paragraphs found.", "issues": ["Scene appears empty."]}

    # Count words per paragraph
    word_counts = [len(p.split()) for p in paragraphs]
    avg_words = sum(word_counts) / total_paras
    short_paras = sum(1 for w in word_counts if w <= 25)  # ~1-3 lines
    short_ratio = short_paras / total_paras

    issues = []
    if avg_words > 50:
        issues.append(f"Average paragraph length is {avg_words:.0f} words — too long for Bab 00 style (target: ≤25).")
    if short_ratio < 0.5:
        issues.append(f"Only {short_ratio:.0%} of paragraphs are short (≤25 words). Bab 00 prefers fragmentary rhythm.")

    if avg_words > 60 and short_ratio < 0.3:
        status = "FAIL"
    elif avg_words > 40 or short_ratio < 0.5:
        status = "WARNING"
    else:
        status = "PASS"

    return {
        "id": "paragraph_rhythm",
        "label": "Paragraph Rhythm",
        "status": status,
        "message": f"avg {avg_words:.0f} words/para, {short_ratio:.0%} short",
        "issues": issues,
    }


def check_artifact_presence(text):
    """Check if scene includes office/tooling artifacts."""
    patterns = [
        (r'>\s', 'terminal prompt'),
        (r'\[SYSTEM', 'system tag'),
        (r'\[GIT', 'git log'),
        (r'\[JIRA', 'Jira reference'),
        (r'\bSlack\b', 'Slack mention'),
        (r'\bterminal\b', 'terminal mention'),
        (r'\bdef \w+\(', 'code function'),
        (r'\btimestamp\b', 'timestamp mention'),
        (r'\blogs\b', 'logs mention'),
        (r'\bJira\b', 'Jira mention'),
        (r'```|`', 'code block'),
    ]

    found = []
    for pat, label in patterns:
        if re.search(pat, text):
            found.append(label)

    # De-duplicate
    found = list(set(found))

    issues = []
    if len(found) < 2:
        issues.append("Scene contains few office/tooling artifacts. Bab 00 texture relies on logs, Slack, terminal, code.")
    if len(found) == 0:
        status = "WARNING"
    else:
        status = "PASS"

    return {
        "id": "artifact_presence",
        "label": "Artifact Presence",
        "status": status,
        "message": f"Found: {', '.join(found) if found else 'none'}",
        "issues": issues,
    }


def check_segment_anchor(text, packet):
    """Check if scene respects the target segment's canon anchor."""
    if not packet:
        return {"id": "segment_anchor", "label": "Segment Anchor", "status": "PASS",
                "message": "No packet — skipped.", "issues": []}

    segment_ctx = packet.get("segment_context", {})
    must_preserve = segment_ctx.get("must_preserve", [])
    danger_zones = segment_ctx.get("danger_zones", [])
    target_segment = packet.get("target_segment", "unknown")
    segment_label = segment_ctx.get("label", "")

    issues = []

    # Check must_preserve items are at least partially reflected
    preserved_found = 0
    for item in must_preserve:
        # Simple keyword check — extract key terms
        terms = [t.lower() for t in re.findall(r'[A-Za-z]+', item) if len(t) > 3]
        if any(t in text.lower() for t in terms[:4]):
            preserved_found += 1

    if len(must_preserve) > 0:
        preserve_ratio = preserved_found / len(must_preserve)
        if preserve_ratio < 0.3:
            issues.append(f"Few 'must_preserve' items from segment {target_segment} ({segment_label}) found in scene.")

    # Check danger zones
    for danger in danger_zones:
        # Extract key forbidden phrases
        if "bertahun-tahun" in danger.lower() or "years" in danger.lower():
            if re.search(r'bertahun-tahun|telah bertahun|sudah bertahun|bekerja bersamanya selama', text, re.IGNORECASE):
                issues.append("DANGER: Scene invents prior long relationship ('bertahun-tahun bekerja bersama').")
                return {
                    "id": "segment_anchor",
                    "label": "Segment Anchor",
                    "status": "FAIL",
                    "message": f"Violates danger zone of segment {target_segment}.",
                    "issues": issues,
                }
        if "timestamp anomaly" in danger.lower() or "remove the timestamp" in danger.lower():
            # Don't fail — just note if timestamp isn't mentioned
            pass

    if any("FAIL" in i or "DANGER" in i for i in issues):
        status = "FAIL"
    elif len(issues) > 0:
        status = "WARNING"
    else:
        status = "PASS"

    return {
        "id": "segment_anchor",
        "label": "Segment Anchor",
        "status": status,
        "message": f"Segment {target_segment} ({segment_label}): {preserved_found}/{len(must_preserve)} preserved items found.",
        "issues": issues,
    }


def check_forbidden_backstory(text, packet):
    """Check for invented prior familiarity that contradicts Bab 00."""
    # These patterns indicate invented backstory
    forbidden_patterns = [
        (r'bertahun-tahun\s+bekerja(?:\s+bersama|\s+dengan)', 'invented multi-year work history'),
        (r'telah\s+bertahun', 'invented multi-year familiarity'),
        (r'sudah\s+kenal\s+(?:lama|sejak)', 'invented prior personal relationship'),
        (r'sahabat\s+(?:lama|sejak)', 'invented close friendship'),
        (r'sejak\s+kuliah', 'invented college history'),
        (r'teman\s+sekantor\s+selama', 'invented long office friendship'),
    ]

    issues = []
    for pat, desc in forbidden_patterns:
        if re.search(pat, text, re.IGNORECASE):
            issues.append(f"Forbidden backstory: {desc}. This contradicts Bab 00 canon unless fork record explicitly permits it.")

    if issues:
        return {
            "id": "forbidden_backstory",
            "label": "Forbidden Backstory",
            "status": "FAIL",
            "message": f"{len(issues)} forbidden backstory pattern(s) found.",
            "issues": issues,
        }

    return {
        "id": "forbidden_backstory",
        "label": "Forbidden Backstory",
        "status": "PASS",
        "message": "No forbidden backstory patterns detected.",
        "issues": [],
    }


def check_entity_scope(text, packet):
    """Check for unauthorized capitalized names in the scene."""
    if not packet:
        return {"id": "entity_scope", "label": "Entity Scope", "status": "PASS",
                "message": "No packet — skipped.", "issues": []}

    allowed = set(packet.get("allowed_entities", ["GUA", "LO", "MANAGER"]))
    # Add common terms that aren't entities
    common_terms = {
        "GUA", "LO", "MANAGER",
        "JIRA", "SLACK", "GIT", "VOID", "BAB",
        "API", "EOD", "PR", "DM", "PM", "UI", "OK",
        "SYSTEM", "ACTIVE", "CONNECTED", "ON", "TRACK",
        "PASSED", "APPROVED", "RESOLVED", "COLLABORATED",
        "BOOT", "ERROR", "WARNING", "FAILED", "DETECTED",
        "MONITOR", "OPERATIONAL", "UNDEFINED", "LOCAL", "ONLY",
        "UNTRACKED", "END", "DAY", "ZERO", "ORIGIN", "TOTAL",
        "MINOR", "SEVERITY", "ACTION", "LOW", "HIGH",
        "VOIDOS", "VOID_OS", "VOID", "OS",
        "HYDROCHOOS", "ICHTHYES", "PARTHEON",
        "SPRINT", "WEEK", "BURNDOWN",
        "BEFORE_TIME", "INITIALIZING", "CRITICAL",
        "ABOUT_THE_STORY", "VOID_MANUSCRIPT", "BOOT_SEQUENCE",
        "ORIGIN_LOG", "AUTO", "SAVE", "HOOK",
        "PATH", "REASON", "STATUS",
        "TABLE", "OF", "CONTENTS",
        "NEW", "MERCURY", "ROSE", "LINEAGE",
        "PULL", "REQUEST", "REVIEWER", "COMMENTS",
        # Technical/office terms that appear in generated scenes
        "TIMESTAMP", "CODE", "LOG", "LOGS", "TASK", "TASKS",
        "BUG", "FIX", "SYNC", "MERGE", "PUSH", "COMMIT",
        "BRANCH", "MAIN", "DEV", "OPS", "SERVER", "BUILD",
        "TEST", "TESTS", "CHECK", "RUN", "DEBUG", "REFACTOR",
        "SPRINT", "BACKLOG", "BOARD", "TICKET",
        "SLACK", "ZOOM", "EMAIL", "CALENDAR", "MEETING",
        "DESK", "OFFICE", "PANTRY", "FLOOR", "WINDOW",
        "KEYBOARD", "MOUSE", "SCREEN", "MONITOR", "LAPTOP",
        "NOTEBOOK", "CURSOR", "TERMINAL", "CONSOLE",
        "CLI", "API", "HTTP", "JSON", "XML", "SQL",
        "PYTHON", "JAVA", "REACT", "NODE",
        "FIRST", "CONTACT", "DAILY", "STANDUP", "PANTRY",
        "FOLDER", "STEALTH", "GENESIS", "PROJECT", "PROTOCOL",
        "AVOIDANCE", "FORK",
        "SCENE", "GATE", "VOICE", "CONTRACT",
        "SKIP", "FOR", "NOW", "GENERATE", "WITH", "THIS",
        "SHOW", "GALLERY", "MAKE", "ANOTHER",
        "READ", "BAB", "HAVE", "ENTER", "BEGIN", "INTERVIEW",
        "TRANSLATE", "THE", "BACK", "NEXT", "FINISH",
        "PASS", "VALID", "PRICE", "REQUIRED", "BLOCKED",
        "WARNING", "FAIL",
        # Common Indonesian office terms
        "JAM", "PAGI", "SIANG", "SORE", "MALAM",
        "SELAMAT", "TERIMA", "KASIH",
        # Common English verbs/nouns that appear capitalized in prose
        "UNTITLED", "DRAFT", "RECORD", "RECORDED",
    }

    # Find capitalized words (potential entities) not in allowed or common
    cap_words = set(re.findall(r'\b([A-Z][A-Za-z]{2,})\b', text))
    unknown = cap_words - allowed - common_terms

    # Filter out common Indonesian/English words that happen to be capitalized
    # (sentence starts, etc.) — they should have lowercase occurrences in the text
    lower_text = text.lower()
    truly_unknown = set()
    for w in unknown:
        # If the word appears lowercase somewhere, it's a common word, not an entity
        if w.lower() in lower_text and w.lower() != w:
            continue  # skip — appears in lowercase too
        # If the word only appears once, likely a sentence-start artifact
        count = len(re.findall(rf'\b{re.escape(w)}\b', text))
        if count <= 1:
            continue  # skip — single occurrence
        truly_unknown.add(w)

    # Also add any entities from the interview
    introduced = packet.get("interview", {}).get("introduced_entities", [])
    introduced_names = {e["name"] for e in introduced} if introduced else set()
    truly_unknown = truly_unknown - introduced_names

    issues = []
    if truly_unknown:
        issues.append(f"Unregistered entities (always capitalized): {', '.join(sorted(truly_unknown)[:5])}. These may be invented entities not in the fork record.")

    if len(truly_unknown) > 3:
        status = "WARNING"
    elif truly_unknown:
        status = "WARNING"
    else:
        status = "PASS"

    return {
        "id": "entity_scope",
        "label": "Entity Scope",
        "status": status,
        "message": f"Allowed: {len(allowed) + len(introduced_names)} names. Unknown: {len(truly_unknown)}.",
        "issues": issues,
    }


def check_law_echo(text, packet):
    """Simple check: scene shouldn't obviously contradict touched laws."""
    if not packet:
        return {"id": "law_echo", "label": "Law Echo", "status": "PASS",
                "message": "No packet — skipped.", "issues": []}

    laws_touched = packet.get("laws_touched", [])
    if not laws_touched:
        return {"id": "law_echo", "label": "Law Echo", "status": "PASS",
                "message": "No laws touched.", "issues": []}

    issues = []
    # Simple pattern check: if law-003 (consent) is touched, check for force language
    if "law-003" in laws_touched:
        force_patterns = [r'dipaksa', r'dipaksakan', r'tanpa izin', r'memaksa', r'override']
        if any(re.search(p, text, re.IGNORECASE) for p in force_patterns):
            issues.append("law-003 (VoidOS via invitation): Scene contains force/override language — may contradict consent architecture.")

    # If law-006 (organic sync) is touched, check for engineered coordination
    if "law-006" in laws_touched:
        engineered = [r'disengaja', r'direncanakan', r'koordinasi', r'disuruh', r'disepakati untuk']
        if any(re.search(p, text, re.IGNORECASE) for p in engineered):
            issues.append("law-006 (organic sync): Scene may depict engineered coordination rather than independent convergence.")

    status = "WARNING" if issues else "PASS"

    return {
        "id": "law_echo",
        "label": "Law Echo",
        "status": status,
        "message": f"{len(laws_touched)} laws touched, {len(issues)} potential contradictions.",
        "issues": issues,
    }


def check_scene(scene_path, packet_path=None):
    """Main entry point. Run all checks and return result dict."""
    scene_text = Path(scene_path).read_text()
    packet = load_json(packet_path) if packet_path else None

    checks = [
        check_voice_pov(scene_text),
        check_paragraph_rhythm(scene_text),
        check_artifact_presence(scene_text),
        check_segment_anchor(scene_text, packet),
        check_forbidden_backstory(scene_text, packet),
        check_entity_scope(scene_text, packet),
        check_law_echo(scene_text, packet),
    ]

    # Determine overall
    statuses = [c["status"] for c in checks]
    if "FAIL" in statuses:
        overall = "FAIL"
    elif statuses.count("WARNING") >= 2:
        overall = "WARNING"
    elif "WARNING" in statuses:
        overall = "WARNING"
    else:
        overall = "PASS"

    issues = []
    for c in checks:
        for i in c.get("issues", []):
            issues.append(f"[{c['label']}] {i}")

    return {
        "ok": True,
        "overall": overall,
        "checks": checks,
        "issues": issues,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: check_scene.py <path/to/scene.md> [--packet path/to/packet.json]")
        sys.exit(1)

    scene_path = sys.argv[1]
    packet_path = None
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--packet" and i + 1 < len(args):
            packet_path = args[i + 1]
            i += 2
        else:
            i += 1

    result = check_scene(scene_path, packet_path)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if result["overall"] == "FAIL":
        sys.exit(2)
    elif result["overall"] == "WARNING":
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
