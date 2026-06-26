#!/usr/bin/env python3
"""
Void Saga — Markdown Scene Extractor v0.1.0

Reads writer-facing .md prose and extracts structured scenario data
for the Narrative Compiler pipeline. No API dependencies.

Usage:
  from extract_scene import extract_scene
  scenario, report = extract_scene("writing/my-scene.md")
"""

import json
import os
import re
from collections import Counter
from pathlib import Path

# ── Module constants ──────────────────────────────────────────────

_REGISTRY = None  # Cached on first load

# Indonesian function words that are NOT character names even when capitalized
STOP_WORDS = {
    "Yang", "Ini", "Itu", "Dia", "Mereka", "Kami", "Kita",
    "Ada", "Semua", "Tapi", "Dan", "Atau", "Karena", "Kalau",
    "Jadi", "Begitu", "Setelah", "Sebelum", "Saat", "Ketika",
    "Dengan", "Dalam", "Pada", "Untuk", "Dari", "Ke",
    "Bukan", "Tidak", "Sudah", "Belum", "Akan", "Masih",
    "Hanya", "Satu", "Seperti", "Lebih", "Kayak", "Terus",
    "Cuma", "Tetap", "Padahal", "Jelas", "Biar",
    "Kadang", "Kombinasi", "Pertanyaan", "Informasi",
    # Indonesian colloquial / false positives
    "Nggak", "Gua", "Lo", "Gue", "Lu", "Ngapain", "Kenapa",
    "Mobil", "Orang", "Tas", "Koper", "Backpack", "Laptop",
    "Tablet", "Charger", "HP", "Hp", "Drummer", "Drum",
    "Mana", "Sini", "Sana", "Situ", "Sono",
    "Kiri", "Kanan", "Depan", "Belakang", "Samping",
    "Kosong", "Sunyi", "Hening", "Salah", "Bener", "Benar",
    "Simpel", "Udah", "Baru", "Lagi", "Pernah", "Besok",
    "Malam", "Pagi", "Siang", "Sore", "Subuh",
    "Kadang,", "Tas.", "Nggak.", "Di",
    # Indonesian verbs that sometimes start sentences
    "Kenal", "Ditanya", "Ditahan", "Dijemput", "Disuruh",
    "Dibilang", "Ditunggu", "Dilihat", "Dengar", "Lihat",
    "Bawa", "Baca", "Tulis", "Duduk", "Berdiri", "Jalan",
    "Tanya", "Jawab", "Kata", "Bilang", "Micara", "Ngobrol",
}

# Known non-name capitalized words (places, things, roles)
NON_NAME_WORDS = {
    "LAX", "LA", "CCTV", "PhD", "Massachusetts", "Amerika",
    "Obsidian", "VS", "Code", "Typora", "JSON", "PASS",
    "WARNING", "BLOCKED", "GUA", "LO",
    "Indonesia", "Jakarta", "Bali", "Bandung", "Yogya",
    "Eropa", "Caribbean", "Amsterdam", "SF", "Korea",
}

# Indonesian dialogue attribution patterns
DIALOGUE_TAG_PATTERNS = [
    re.compile(r'\b(?:kata|tanya|jawab|ucap|sambung|lanjut|potong|sahut)\s+([A-Z][a-z]+)'),
    re.compile(r'([A-Z][a-z]+)\s+(?:berkata|bertanya|menjawab|berucap|berbisik|ngomong|bilang|nanya|ngangguk|ngelirik|ngeliat|nyahut)'),
    re.compile(r'"([^"]+)"\s*(?:kata|tanya|jawab)\s+([A-Z][a-z]+)'),
]

# Introspection verbs that suggest POV
INTROSPECTION_VERBS = [
    "merasa", "pikir", "sadar", "tahu", "ingat", "ngerasa",
    "mikir", "nyadar", "kenal", "paham", "ngerti",
]

# ── Registry loading ──────────────────────────────────────────────

def load_character_registry():
    """Load the character registry. Cached at module level."""
    global _REGISTRY
    if _REGISTRY is not None:
        return _REGISTRY

    registry_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "character_registry.json"
    )
    with open(registry_path, "r", encoding="utf-8") as f:
        _REGISTRY = json.load(f)
    return _REGISTRY


def _build_alias_map(registry):
    """Build a flat alias→entry map for fast lookup."""
    alias_map = {}
    for entry_id, entry in registry["entries"].items():
        for alias in entry["aliases"]:
            alias_map[alias.lower()] = entry
    return alias_map


# ── YAML Frontmatter Parser ───────────────────────────────────────

def parse_yaml_frontmatter(text):
    """Parse YAML frontmatter from markdown text.

    Handles a simple subset: scalars, inline lists, one-level-deep
    nested mappings. No pyyaml dependency.

    Returns (metadata_dict, remaining_text).
    """
    # Detect frontmatter delimiters: --- at start of file
    stripped = text.lstrip("﻿")  # Strip BOM
    if not stripped.startswith("---"):
        return {}, stripped

    # Find closing ---
    second_delim = stripped.find("\n---", 3)
    if second_delim == -1:
        return {}, stripped

    fm_text = stripped[3:second_delim].strip()
    remaining = stripped[second_delim + 4:].lstrip("\n")

    if not fm_text:
        return {}, remaining

    metadata = {}
    current_key = None
    current_nested = {}

    for raw_line in fm_text.split("\n"):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        # Nested line (2-space indent): key: value
        if raw_line.startswith("  ") and current_key is not None:
            nested_match = re.match(r'^\s{2}(\w+):\s*(.+)$', raw_line)
            if nested_match:
                nk, nv = nested_match.groups()
                current_nested[nk] = _parse_yaml_value(nv)
            continue

        # Flush any pending nested block
        if current_key is not None and current_nested:
            metadata[current_key] = current_nested
            current_nested = {}
            current_key = None

        # Top-level key: value
        match = re.match(r'^(\w+):\s*(.+)$', line)
        if match:
            key, value_str = match.groups()
            parsed = _parse_yaml_value(value_str)
            if parsed is not None:
                metadata[key] = parsed
            current_key = None
            current_nested = {}
            # Check if next line might be nested (value was empty or looks like a header)
            if isinstance(parsed, str) and parsed == "":
                current_key = key
                current_nested = {}

    # Flush final nested block
    if current_key is not None and current_nested:
        metadata[current_key] = current_nested

    return metadata, remaining


def _parse_yaml_value(value_str):
    """Parse a single YAML value string into Python type."""
    val = value_str.strip().rstrip(",")
    if not val or val == '""' or val == "''":
        return ""
    # Boolean
    if val.lower() in ("true", "yes"):
        return True
    if val.lower() in ("false", "no"):
        return False
    # Integer
    try:
        return int(val)
    except ValueError:
        pass
    # Inline list: [item1, item2, ...]
    if val.startswith("[") and val.endswith("]"):
        inner = val[1:-1].strip()
        if not inner:
            return []
        items = [_parse_yaml_value(i) for i in _split_list(inner)]
        return items
    # Quoted string
    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
        return val[1:-1]
    return val


def _split_list(inner):
    """Split a comma-separated list, respecting quotes."""
    items = []
    current = []
    in_quote = False
    quote_char = None
    for ch in inner:
        if ch in ('"', "'") and not in_quote:
            in_quote = True
            quote_char = ch
        elif ch == quote_char and in_quote:
            in_quote = False
            quote_char = None
        elif ch == "," and not in_quote:
            items.append("".join(current).strip())
            current = []
            continue
        current.append(ch)
    if current:
        items.append("".join(current).strip())
    return items


# ── Name Extraction Heuristics ────────────────────────────────────

def _normalize_text(text):
    """Normalize text for processing: strip BOM, normalize line endings."""
    text = text.lstrip("﻿")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text


def extract_names_from_dialogue_tags(text):
    """Extract speaker names from Indonesian dialogue attribution patterns."""
    names = []

    for pattern in DIALOGUE_TAG_PATTERNS:
        for match in pattern.finditer(text):
            for group in match.groups():
                if group and group[0].isupper() and group not in STOP_WORDS:
                    names.append(group)

    # Also detect code-block style dialogue: `Name: text`
    code_block_pattern = re.compile(r'`{3}\n(\w+):\s*(.+)`{3}', re.MULTILINE)
    for match in code_block_pattern.finditer(text):
        name = match.group(1)
        if name[0].isupper() or name.isupper():
            names.append(name)

    return names


def extract_sentence_subjects(text):
    """Extract proper nouns appearing as sentence subjects."""
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+|\n{2,}', text)
    potential_names = Counter()

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        # First word of sentence (after optional quote or connector)
        words = sentence.split()
        if not words:
            continue
        first_word = words[0].strip('"\'""''')
        # Skip if starts with lowercase
        if not first_word or not first_word[0].isupper():
            continue
        # Filter: must be a proper-looking word (not ALLCAPS, not single letter)
        if first_word.isupper() and len(first_word) > 1:
            continue  # Skip ALLCAPS acronyms
        if len(first_word) < 2:
            continue
        if first_word in STOP_WORDS or first_word in NON_NAME_WORDS:
            continue
        # Must look like a name: starts with capital, rest lowercase or mixed
        if first_word[0].isupper():
            potential_names[first_word] += 1

    return potential_names


def _clean_name(name):
    """Strip trailing punctuation and whitespace from an extracted name."""
    return name.strip().rstrip(".,;:!?-\"'""''")


def extract_names_heuristic(text):
    """Main heuristic name extraction pipeline for Indonesian prose.

    Returns list of (name, confidence) tuples sorted by confidence descending.
    """
    # Pass 1: dialogue tags (highest confidence)
    dialogue_names_raw = extract_names_from_dialogue_tags(text)
    dialogue_names = [_clean_name(n) for n in dialogue_names_raw]
    dialogue_counts = Counter(dialogue_names)

    # Pass 2: sentence subjects (medium confidence)
    subject_counts_raw = extract_sentence_subjects(text)
    subject_counts = Counter()
    for name, count in subject_counts_raw.items():
        cleaned = _clean_name(name)
        subject_counts[cleaned] += count

    # Pass 3: cross-reference and score
    all_candidates = set(list(dialogue_counts.keys()) + list(subject_counts.keys()))
    scored = []

    for name in all_candidates:
        if name in STOP_WORDS or name in NON_NAME_WORDS:
            continue
        if len(name) < 2:
            continue

        dl_count = dialogue_counts.get(name, 0)
        sj_count = subject_counts.get(name, 0)
        total_count = dl_count + sj_count

        # Frequency filter: must appear at least twice OR be in dialogue
        if total_count < 2 and dl_count == 0:
            continue

        # Confidence scoring:
        # - Appears in dialogue tags: +3 per occurrence
        # - Appears as sentence subject: +1 per occurrence
        # - Appears in BOTH: +5 bonus
        confidence = (dl_count * 3) + (sj_count * 1)
        if dl_count > 0 and sj_count > 0:
            confidence += 5

        scored.append((name, confidence, total_count))

    # Sort by confidence descending
    scored.sort(key=lambda x: x[1], reverse=True)

    return [(name, conf) for name, conf, _ in scored]


# ── Runtime Matching ──────────────────────────────────────────────

def match_names_to_runtimes(names, registry):
    """Match extracted names against the character registry.

    Args:
        names: list of (name, confidence) tuples from extract_names_heuristic
        registry: loaded character registry dict

    Returns:
        dict with matched, unmatched, known_no_runtime lists
    """
    alias_map = _build_alias_map(registry)
    result = {
        "matched": {},       # runtime_id → {name, aliases_matched, has_runtime, default_stage}
        "unmatched": [],     # names not in registry at all
        "known_no_runtime": [],  # names in registry but has_runtime=false
    }

    for name, confidence in names:
        name_lower = name.lower()
        if name_lower in alias_map:
            entry = alias_map[name_lower]
            rid = entry.get("runtime_id")
            if entry.get("has_runtime") and rid:
                if rid not in result["matched"]:
                    result["matched"][rid] = {
                        "name": entry.get("display_name", name),
                        "aliases_matched": [name],
                        "default_stage": entry.get("default_stage", 4),
                        "confidence": confidence,
                    }
                else:
                    result["matched"][rid]["aliases_matched"].append(name)
            else:
                result["known_no_runtime"].append({
                    "name": name,
                    "display_name": entry.get("display_name", name),
                    "registry_key": rid or name_lower,
                })
        else:
            result["unmatched"].append({"name": name, "confidence": confidence})

    return result


# ── POV Inference ─────────────────────────────────────────────────

def infer_pov_character(names, text):
    """Infer POV character from prose.

    Heuristic:
    1. First-named character in the text (highest weight)
    2. Character with most introspection verbs in their paragraphs
    """
    if not names:
        return None

    name_list = [n for n, _ in names]
    if not name_list:
        return None

    # Find first-appearing character in the text (not by confidence score)
    first_positions = {}
    for name in name_list:
        pos = text.find(name)
        if pos >= 0:
            first_positions[name] = pos
    first_name = min(first_positions, key=first_positions.get) if first_positions else name_list[0]

    # Weight 2: introspection density — count introspection verbs near each name
    introspection_scores = Counter()
    paragraphs = text.split("\n\n")
    for para in paragraphs:
        para_lower = para.lower()
        has_introspection = any(verb in para_lower for verb in INTROSPECTION_VERBS)
        if not has_introspection:
            continue
        for name in name_list:
            if name in para:
                # Count introspection verbs in this paragraph
                count = sum(1 for verb in INTROSPECTION_VERBS if verb in para_lower)
                introspection_scores[name] += count

    # Combined score: first-name gets +3
    scores = Counter()
    scores[first_name] += 3
    for name, count in introspection_scores.items():
        scores[name] += count * 2

    if scores:
        return scores.most_common(1)[0][0]
    return first_name


# ── Setting Extraction ────────────────────────────────────────────

def extract_setting_hints(text):
    """Extract basic setting information from prose.

    Scans first 100 lines for location, time-of-day, and primary action cues.
    """
    lines = text.split("\n")[:100]
    joined = " ".join(lines)
    joined_lower = joined.lower()

    setting = ""
    time_of_day = ""
    primary_action = ""

    # Location detection
    location_markers = {
        "bandara": "airport",
        "airport": "airport",
        "lax": "airport",
        "kedatangan": "airport",
        "kantor": "office",
        "kafe": "cafe",
        "hotel": "hotel",
        "rumah": "house",
        "mobil": "car",
        "jalan": "street",
        "kamar": "room",
        "stasiun": "station",
        "apartemen": "apartment",
        "gedung": "building",
        "taman": "park",
        "kapal": "ship",
        "bagasi": "car",
    }
    for marker, label in location_markers.items():
        if marker in joined_lower:
            setting = label
            break

    # Time of day
    time_markers = {
        "pagi": "morning",
        "siang": "afternoon",
        "sore": "evening",
        "malam": "night",
        "subuh": "dawn",
    }
    for marker, label in time_markers.items():
        if marker in joined_lower:
            time_of_day = label
            break

    # Primary action — look for action verbs
    action_markers = {
        "tiba": "arrival",
        "datang": "arrival",
        "pergi": "departure",
        "jemput": "pickup",
        "nunggu": "waiting",
        "jalan": "walking",
        "duduk": "sitting",
        "ngobrol": "conversation",
        "bicara": "conversation",
        "diam": "silence",
        "tidur": "sleeping",
        "makan": "eating",
        "nangis": "crying",
        "pulang": "returning",
    }
    for marker, label in action_markers.items():
        if marker in joined_lower:
            primary_action = label
            break

    return {
        "setting": setting or "unknown",
        "time_of_day": time_of_day or "unknown",
        "primary_action": primary_action or "unknown",
    }


# ── Dialogue Counting ─────────────────────────────────────────────

def count_dialogue_lines(text):
    """Count approximate dialogue lines in the text.

    Counts: quoted lines, code-block dialogue, and dialogue-tag-associated lines.
    """
    count = 0

    # Quoted dialogue: "..." at start of lines or inline
    quote_lines = re.findall(r'"([^"]+)"', text)
    count += len(quote_lines)

    # Code-block dialogue: `Name: text`
    code_blocks = re.findall(r'`{3}\n\w+:.*?`{3}', text, re.DOTALL)
    for block in code_blocks:
        count += len(block.strip().split("\n")) - 2  # subtract fence lines

    # Double-quote dialogue attribution lines
    attrib_lines = re.findall(r'"([^"]+)"\s*(?:kata|tanya|jawab)', text)
    count += len(attrib_lines)

    return count


# ── Scenario JSON Generation ──────────────────────────────────────

def generate_scenario_json(extracted, registry, frontmatter, md_filename):
    """Build a valid scenario JSON dict from extracted and frontmatter data.

    Priority: YAML frontmatter > heuristic extraction > safe defaults
    """
    # scenario_id: from frontmatter or derived from filename
    scenario_id = frontmatter.get("scenario_id", "")
    if not scenario_id:
        # Derive from filename: strip extension, replace spaces/special chars
        stem = Path(md_filename).stem
        scenario_id = re.sub(r'[^a-z0-9_]+', '_', stem.lower()).strip("_")

    # Participants: from frontmatter or matched runtimes
    if "characters" in frontmatter:
        participants = []
        stages = frontmatter.get("evolution_stages", {})
        for char_id in frontmatter["characters"]:
            stage = stages.get(char_id, 4)
            participants.append({"runtime_id": char_id, "evolution_stage": stage})
    else:
        matched = extracted.get("matching", {}).get("matched", {})
        participants = []
        for rid, info in matched.items():
            stage = frontmatter.get("evolution_stages", {}).get(rid, info.get("default_stage", 4))
            participants.append({"runtime_id": rid, "evolution_stage": stage})

    # Timeline state
    timeline = {
        "phase": frontmatter.get("phase", 5),
        "pre_chain": frontmatter.get("pre_chain", False),
        "post_resolution": frontmatter.get("post_resolution", True),
    }

    # Proximity state
    if "pairs_in_range" in frontmatter:
        pairs = frontmatter["pairs_in_range"]
    else:
        # Auto-generate from participant list
        pids = sorted([p["runtime_id"] for p in participants])
        pairs = []
        for i in range(len(pids)):
            for j in range(i + 1, len(pids)):
                pairs.append(f"{pids[i]}_{pids[j]}")

    proximity = {
        "pairs_in_range": pairs,
        "distance": frontmatter.get("distance", "same_room"),
    }

    # Requested action
    if "action_description" in frontmatter:
        action_desc = frontmatter["action_description"]
    else:
        action_desc = extracted.get("summary", "Scene from markdown prose.")

    action_type = frontmatter.get("action_type", "speak")

    # Canon mode
    canon_mode = {
        "type": frontmatter.get("canon_mode", "canon_replication"),
        "expected_verdict": frontmatter.get("expected_verdict", "PASS"),
    }

    return {
        "scenario_id": scenario_id,
        "participants": participants,
        "timeline_state": timeline,
        "proximity_state": proximity,
        "requested_action": {
            "description": action_desc[:500],
            "type": action_type,
        },
        "canon_mode": canon_mode,
    }


# ── Main Entry Point ──────────────────────────────────────────────

def extract_scene(md_path):
    """Extract a scene from a markdown file.

    Args:
        md_path: Path to a .md file (absolute or relative)

    Returns:
        (scenario_dict, report_dict)
        - scenario_dict: Valid scenario JSON dict for the compiler
        - report_dict: Extraction metadata for CLI output formatting

    Raises:
        FileNotFoundError: if md_path doesn't exist
        ValueError: if file can't be read
    """
    path = Path(md_path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"File not found: {md_path}")

    # Read with encoding fallback
    try:
        raw_text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            raw_text = path.read_text(encoding="latin-1")
        except Exception:
            raise ValueError(f"Cannot read file encoding: {md_path}")

    text = _normalize_text(raw_text)

    if not text.strip():
        return (
            {"scenario_id": path.stem, "participants": [],
             "timeline_state": {"phase": 5, "pre_chain": False, "post_resolution": True},
             "proximity_state": {"pairs_in_range": [], "distance": "none"},
             "requested_action": {"description": "", "type": "speak"},
             "canon_mode": {"type": "canon_replication", "expected_verdict": "PASS"}},
            {"filename": path.name, "word_count": 0, "pov_character": None,
             "characters_detected": [], "dialogue_lines": 0,
             "setting": {}, "matched_runtimes": {}, "unmatched_names": [],
             "known_no_runtime": [], "extraction_method": "empty_file",
             "frontmatter_keys_used": []}
        )

    # 1. Parse YAML frontmatter
    frontmatter, prose_text = parse_yaml_frontmatter(text)
    frontmatter_keys = list(frontmatter.keys())

    # 2. Extract character names
    if "characters" in frontmatter:
        extraction_method = "frontmatter"
        names_scored = [(name, 10) for name in frontmatter["characters"]]
    else:
        extraction_method = "heuristic"
        names_scored = extract_names_heuristic(prose_text)

    name_list = [n for n, _ in names_scored]

    # 3. Match against registry
    registry = load_character_registry()
    matching = match_names_to_runtimes(names_scored, registry)

    # 4. Infer POV
    pov = frontmatter.get("pov", None)
    if pov is None and name_list:
        pov = infer_pov_character(names_scored, prose_text)

    # 5. Setting hints (from prose, not frontmatter)
    setting = extract_setting_hints(prose_text)

    # 6. Dialogue count
    dialogue_count = count_dialogue_lines(prose_text)

    # 7. Word count (words = whitespace-separated tokens)
    word_count = len(prose_text.split())

    # 8. Generate prose summary for action_description
    summary = _generate_summary(prose_text, pov, name_list, setting)

    # 9. Build extraction result for scenario generation
    extracted = {
        "matching": matching,
        "summary": summary,
    }

    # 10. Generate scenario JSON
    scenario = generate_scenario_json(extracted, registry, frontmatter, path.name)

    # 11. Build report dict
    report = {
        "filename": path.name,
        "filepath": str(path),
        "word_count": word_count,
        "pov_character": pov,
        "characters_detected": name_list,
        "dialogue_lines": dialogue_count,
        "setting": setting,
        "matched_runtimes": matching["matched"],
        "unmatched_names": matching["unmatched"],
        "known_no_runtime": matching["known_no_runtime"],
        "extraction_method": extraction_method,
        "frontmatter_keys_used": frontmatter_keys,
        "has_matched_characters": len(matching["matched"]) > 0,
    }

    return scenario, report


def _generate_summary(prose_text, pov, name_list, setting):
    """Generate a prose summary for the scenario action description.

    Takes the first ~500 chars of prose to give the constraint engine
    enough context to detect forbidden behaviors. Skips YAML frontmatter
    fences and code blocks. Continues across paragraph breaks.
    """
    # Strip markdown code fences and collect content lines
    clean_lines = []
    in_code_block = False
    for line in prose_text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            # Keep code block content — dialogue inside matters
            if stripped:
                clean_lines.append(stripped)
            continue
        if stripped:
            clean_lines.append(stripped)

    summary = " ".join(clean_lines)[:500].strip()
    if summary:
        return summary

    chars = ", ".join(name_list[:3]) if name_list else "unknown"
    loc = setting.get("setting", "unknown location")
    return f"Scene with {chars} at {loc}."


# ── CLI (for direct testing) ─────────────────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python extract_scene.py <markdown_file> [--json]")
        print("  --json : output raw JSON (scenario + report)")
        sys.exit(1)

    md_path = sys.argv[1]
    output_json = "--json" in sys.argv

    try:
        scenario, report = extract_scene(md_path)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    if output_json:
        print(json.dumps({
            "scenario": scenario,
            "report": report,
        }, indent=2, ensure_ascii=False))
    else:
        print(f"═══ Scene Extractor v0.1.0 ═══")
        print(f"File: {report['filename']}")
        print(f"Word count: {report['word_count']}")
        print(f"Method: {report['extraction_method']}")
        print(f"POV: {report['pov_character'] or 'unknown'}")
        print()
        print(f"Characters detected: {', '.join(report['characters_detected']) if report['characters_detected'] else 'none'}")
        print(f"Dialogue lines: {report['dialogue_lines']}")
        print(f"Setting: {report['setting'].get('setting')} / {report['setting'].get('time_of_day')}")
        print()
        if report['matched_runtimes']:
            print("Matched runtimes:")
            for rid, info in report['matched_runtimes'].items():
                print(f"  ✓ {info['name']} → {rid} (stage {info['default_stage']})")
        if report['known_no_runtime']:
            print("Known characters (no runtime yet):")
            for item in report['known_no_runtime']:
                print(f"  ⚠ {item['display_name']} — has_runtime: false")
        if report['unmatched_names']:
            print("Unknown characters:")
            for item in report['unmatched_names']:
                print(f"  ✗ {item['name']} (confidence: {item['confidence']})")
        print()
        if report['frontmatter_keys_used']:
            print(f"Frontmatter keys: {', '.join(report['frontmatter_keys_used'])}")
        print(f"\nScenario participants: {len(scenario['participants'])}")
        for p in scenario['participants']:
            print(f"  {p['runtime_id']} (stage {p['evolution_stage']})")
