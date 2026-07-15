from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from .models import ValidationIssue, ValidationSummary

ROOT_MANIFEST = "CANON_MANIFEST_DRAFT.md"
BAB_CONFIRMATION = "BAB_WORLD_CONFIRMATION.md"
CODEX_CONFIRMATION = "CODEX_STRUCTURAL_CONFIRMATION.md"
OUTPUT_REPORT = Path("outputs/corpus-validation-report.json")
DRAFT_JSON = Path("canon-manifest-v1.draft.json")

ALLOWED_LAYER = {"bab", "timer", "codex", "system"}
ALLOWED_SOURCE_AUTHORITY = {"canonical", "supplemental", "derived"}
ALLOWED_TEMPORAL_STATUS = {"sequential", "retroactive", "recursive", "atemporal", "uncertain"}
ALLOWED_DIEGETIC_CERTAINTY = {"exact", "approximate", "relative", "unknown", "not_applicable"}
ALLOWED_EVIDENCE_MODE = {"witnessed", "declared", "reported", "archival", "reflective", "procedural", "mixed", "unknown"}
ALLOWED_FRAME = {"bab-world", "timer-world", None}
RELATION_NAMESPACES = {
    "temporal": {"occurs_before", "occurs_after", "overlaps", "recounts"},
    "structural": {"resonates_with", "foreshadows", "recontextualizes"},
    "composition": {"composed_during", "rewritten_during", "deleted_during"},
    "derivation": {"compiled_from", "excerpted_from", "supersedes"},
}
EXPECTED_LAYER_COUNTS = {"bab": 29, "timer": 29, "codex": 5, "system": 2}
EXPECTED_INCLUDED = 65
EXPECTED_EXCLUDED = 3
EXPECTED_BAB_EXCEPTION = {"bab-02-5": "mixed"}

BAB_FILE_MAP = {
    "bab-00": "Bab 00 — Menatap Akhir Era dari Balik.md",
    "bab-01": "Bab 01 — Menatap Akhir Era dari Balik.md",
    "bab-02": "Bab 02 — Menatap Akhir Era dari Balik.md",
    "bab-02-5": "Bab 02-5 — Menatap Akhir Era dari Balik.md",
    "bab-03": "Bab 03 — Menatap Akhir Era dari Balik.md",
    "bab-04": "Bab 04 — Menatap Akhir Era dari Balik.md",
    "bab-05": "Bab 05 — Menatap Akhir Era dari Balik.md",
    "bab-06": "Bab 06 — Menatap Akhir Era dari Balik.md",
    "bab-07": "Bab 07 — Menatap Akhir Era dari Balik.md",
    "bab-08": "Bab 08 — Menatap Akhir Era dari Balik.md",
    "bab-09": "Bab 09 — Menatap Akhir Era dari Balik.md",
    "bab-10": "Bab 10 — Menatap Akhir Era dari Balik.md",
    "bab-11": "Bab 11 — Menatap Akhir Era dari Balik.md",
    "bab-12": "Bab 12 — Menatap Akhir Era dari Balik.md",
    "bab-13": "Bab 13 — Menatap Akhir Era dari Balik.md",
    "bab-14": "Bab 14 — Menatap Akhir Era dari Balik.md",
    "bab-15": "Bab 15 — Menatap Akhir Era dari Balik.md",
    "bab-16": "Bab 16 — Menatap Akhir Era dari Balik.md",
    "bab-16-5": "Bab 16.5 — Menatap Akhir Era dari Balik.md",
    "bab-16-6": "Bab 16.6 — Menatap Akhir Era dari Balik.md",
    "bab-17": "Bab 17 — Menatap Akhir Era dari Balik.md",
    "bab-18": "Bab 18 — Menatap Akhir Era dari Balik.md",
    "bab-19": "Bab 19 — Menatap Akhir Era dari Balik.md",
    "bab-20": "Bab 20 — Menatap Akhir Era dari Balik.md",
    "bab-21": "Bab 21 — Menatap Akhir Era dari Balik.md",
    "bab-22": "Bab 22 — Menatap Akhir Era dari Balik.md",
    "bab-23": "Bab 23 — Menatap Akhir Era dari Balik.md",
    "bab-24": "Bab 24 — Menatap Akhir Era dari Balik.md",
    "bab-25": "Bab 25 — Menatap Akhir Era dari Balik.md",
}
TIMER_FILE_MAP = {
    "timer-00-00": "Timer 0000 — Menatap Akhir Semesta dari Balik.md",
    "timer-01-00": "Timer 0100 — Menatap Akhir Semesta dari Balik.md",
    "timer-02-00": "Timer 0200 — Menatap Akhir Semesta dari Balik.md",
    "timer-02-50": "Timer 0250 — Menatap Akhir Semesta dari Balik.md",
    "timer-03-00": "Timer 0300 — Menatap Akhir Semesta dari Balik.md",
    "timer-04-00": "Timer 0400 — Menatap Akhir Semesta dari Balik.md",
    "timer-05-00": "Timer 0500 — Menatap Akhir Semesta dari Balik.md",
    "timer-06-00": "Timer 0600 — Menatap Akhir Semesta dari Balik.md",
    "timer-07-00": "Timer 0700 — Menatap Akhir Semesta dari Balik.md",
    "timer-08-00": "Timer 0800 — Menatap Akhir Semesta dari Balik.md",
    "timer-09-00": "Timer 0900 — Menatap Akhir Semesta dari Balik.md",
    "timer-10-00": "Timer 1000 — Menatap Akhir Semesta dari Balik.md",
    "timer-11-00": "Timer 1100 — Menatap Akhir Semesta dari Balik.md",
    "timer-12-00": "Timer 1200 — Menatap Akhir Semesta dari Balik.md",
    "timer-13-00": "Timer 1300 — Menatap Akhir Semesta dari Balik.md",
    "timer-14-00": "Timer 1400 — Menatap Akhir Semesta dari Balik.md",
    "timer-15-00": "Timer 1500 — Menatap Akhir Semesta dari Balik.md",
    "timer-16-00": "Timer 1600 — Menatap Akhir Semesta dari Balik.md",
    "timer-16-50": "Timer 1650 — Menatap Akhir Semesta dari Balik.md",
    "timer-16-66": "Timer 1666 — Menatap Akhir Semesta dari Balik.md",
    "timer-17-00": "Timer 1700 — Menatap Akhir Semesta dari Balik.md",
    "timer-18-00": "Timer 1800 — Menatap Akhir Semesta dari Balik.md",
    "timer-19-00": "Timer 1900 — Menatap Akhir Semesta dari Balik.md",
    "timer-20-00": "Timer 2000 — Menatap Akhir Semesta dari Balik.md",
    "timer-21-00": "Timer 2100 — Menatap Akhir Semesta dari Balik.md",
    "timer-22-00": "Timer 2200 — Menatap Akhir Semesta dari Balik.md",
    "timer-23-00": "Timer 2300 — Menatap Akhir Semesta dari Balik.md",
    "timer-24-00": "Timer 2400 — Menatap Akhir Semesta dari Balik.md",
    "timer-25-00": "Timer 2500 — Menatap Akhir Semesta dari Balik.md",
}
CODEX_FILE_MAP = {
    "codex-udara": "Codex Udara — Menatap Akhir Semesta dari Balik.md",
    "codex-air": "Codex Air — Menatap Akhir Semesta dari Balik.md",
    "codex-api": "Codex Api — Menatap Akhir Semesta dari Balik.md",
    "codex-tanah": "Codex Tanah — Menatap Akhir Semesta dari Balik.md",
    "codex-the-void": "Codex The Void — Menatap Akhir Semesta dari Balik.md",
}
SYSTEM_FILE_MAP = {
    "system-opening": "opening.md",
    "system-void-os-v6-6-6": "Void.OS v6.6.6 Update.md",
}
EXCLUDED_FILE_MAP = {
    "sigil-os": "Sigil_OS.md",
    "void-cosmology-paper": "THE VOID COSMOLOGY PAPER.md",
    "naskah-lengkap": "Void Saga — Naskah Lengkap.md",
}


def _clean_cell(cell: str) -> str | None:
    value = cell.strip()
    if not value or value == "—":
        return None
    value = re.sub(r"`", "", value)
    value = re.sub(r"\*", "", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def parse_markdown_table(lines: list[str]) -> list[dict[str, str | None]]:
    table_lines = [line for line in lines if line.strip().startswith("|")]
    if len(table_lines) < 3:
        return []
    headers = [_clean_cell(c) or "" for c in table_lines[0].strip().strip("|").split("|")]
    rows: list[dict[str, str | None]] = []
    for raw in table_lines[2:]:
        cells = [_clean_cell(c) for c in raw.strip().strip("|").split("|")]
        if len(cells) < len(headers):
            cells += [None] * (len(headers) - len(cells))
        rows.append({headers[i]: cells[i] for i in range(len(headers))})
    return rows


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def section_lines(lines: list[str], heading: str) -> list[str]:
    start = None
    for i, line in enumerate(lines):
        if line.strip() == heading:
            start = i + 1
            break
    if start is None:
        return []
    end = len(lines)
    for i in range(start, len(lines)):
        if lines[i].startswith("### ") and lines[i].strip() != heading:
            end = i
            break
    return lines[start:end]


def parse_manifest_header(text: str) -> dict[str, str]:
    title_match = re.search(r"#\s+CANON_MANIFEST_DRAFT\s+[—-]\s+([^\n]+)", text)
    schema_match = re.search(r"Schema:\s+([^\n]+)", text)
    status_match = re.search(r"Status:\s+([^\n]+)", text)
    return {
        "canon_id": title_match.group(1).strip() if title_match else "",
        "schema_version": schema_match.group(1).strip() if schema_match else "",
        "manifest_status": status_match.group(1).strip() if status_match else "",
    }


def build_source_path_map() -> dict[str, str]:
    merged = {}
    merged.update(BAB_FILE_MAP)
    merged.update(TIMER_FILE_MAP)
    merged.update(CODEX_FILE_MAP)
    merged.update(SYSTEM_FILE_MAP)
    merged.update(EXCLUDED_FILE_MAP)
    return merged


def parse_confirmation_table(path: Path) -> list[dict[str, str | None]]:
    return parse_markdown_table(read_lines(path))


def parse_manifest_tables(root: Path) -> dict[str, Any]:
    manifest_path = root / ROOT_MANIFEST
    text = manifest_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    return {
        "header": parse_manifest_header(text),
        "system": parse_markdown_table(section_lines(lines, "### 5.1 system (2)")),
        "order": parse_markdown_table(section_lines(lines, "### 5.2 bab (29) ↔ timer (29), interleaved reading order")),
        "timer_harvest": parse_markdown_table(section_lines(lines, "### 5.2A harvested timer metadata (accepted editorial state)")),
        "codex": parse_markdown_table(section_lines(lines, "### 5.3 codex (5)")),
        "excluded": parse_markdown_table(section_lines(lines, "## 6. EXCLUDED register (3)")),
        "open_schema_001_present": "OPEN-SCHEMA-001" in text,
        "open_schema_002_present": "OPEN-SCHEMA-002" in text,
    }


def _parse_relation_notes(document_id: str, note: str | None) -> list[dict[str, str]]:
    if not note:
        return []
    relations: list[dict[str, str]] = []
    for rel_type in ("composed_during", "rewritten_during", "deleted_during"):
        for target in re.findall(rf"{rel_type}\s*→\s*([a-z0-9\-]+)", note):
            relations.append({"namespace": "composition", "relation_type": rel_type, "target_document_id": target})
    if document_id == "system-void-os-v6-6-6":
        relations.append({"namespace": "structural", "relation_type": "recontextualizes", "target_document_id": "system-opening"})
    return relations


def build_draft_manifest_from_repository(root: Path) -> dict[str, Any]:
    parsed = parse_manifest_tables(root)
    bab_confirmation = {row["document_id"]: row for row in parse_confirmation_table(root / BAB_CONFIRMATION)}
    codex_confirmation = {row["document_id"]: row for row in parse_confirmation_table(root / CODEX_CONFIRMATION)}
    source_paths = build_source_path_map()

    order_rows = parsed["order"]
    timer_harvest = {row["document_id"]: row for row in parsed["timer_harvest"]}
    system_rows = {row["document_id"]: row for row in parsed["system"]}
    codex_rows = {row["document_id"]: row for row in parsed["codex"]}
    excluded_rows = {row["document_id"]: row for row in parsed["excluded"]}

    included_documents: list[dict[str, Any]] = []

    for document_id, row in system_rows.items():
        included_documents.append({
            "document_id": document_id,
            "layer": "system",
            "source_authority": "canonical",
            "source_path": source_paths[document_id],
            "diegetic_frame": "bab-world" if document_id == "system-opening" else None,
            "temporal_status": row["temporal_status"],
            "sequence_narrative": int(row["seq"]),
            "relations": _parse_relation_notes(document_id, row.get("Relations / notes")),
        })

    for row in order_rows:
        document_id = row.get("document_id")
        if not document_id or document_id.startswith("*(seq") or document_id.startswith("seq"):
            continue
        if document_id.startswith("bab-"):
            conf = bab_confirmation[document_id]
            included_documents.append({
                "document_id": document_id,
                "layer": "bab",
                "source_authority": "canonical",
                "source_path": source_paths[document_id],
                "diegetic_frame": conf["frame"],
                "temporal_status": conf["temporal_status"],
                "diegetic_certainty": conf["certainty"],
                "evidence_mode": conf["evidence_mode_default"],
                "sequence_narrative": int(row["seq"]),
                "sequence_within_frame": None,
                "confirmation_status": "confirmed",
                "pair_document_id": row.get("pair"),
                "relations": _parse_relation_notes(document_id, row.get("Composition / status notes")),
            })
        elif document_id.startswith("timer-"):
            harvest = timer_harvest[document_id]
            included_documents.append({
                "document_id": document_id,
                "layer": "timer",
                "source_authority": "canonical",
                "source_path": source_paths[document_id],
                "diegetic_frame": "timer-world",
                "temporal_status": harvest["temporal_status"],
                "diegetic_certainty": harvest["diegetic_certainty"],
                "evidence_mode": harvest["evidence_mode"],
                "editorial_confidence": harvest["editorial_confidence"],
                "relative_order_review": harvest["relative_order_review"],
                "composed_during": harvest["composed_during"],
                "sequence_narrative": int(row["seq"]),
                "sequence_within_frame": None,
                "pair_document_id": row.get("pair"),
                "relations": _parse_relation_notes(document_id, row.get("Composition / status notes")),
            })

    for document_id, row in codex_rows.items():
        if document_id not in codex_confirmation:
            continue
        conf = codex_confirmation[document_id]
        included_documents.append({
            "document_id": document_id,
            "layer": "codex",
            "source_authority": conf["source_authority"],
            "source_path": source_paths[document_id],
            "diegetic_frame": None,
            "temporal_status": conf["temporal_status"],
            "diegetic_certainty": "not_applicable",
            "sequence_narrative": int(row["seq"]),
            "narrative_placement": conf["narrative_placement"],
            "relations": [],
        })

    excluded_artifacts = []
    for document_id, row in excluded_rows.items():
        excluded_artifacts.append({
            "document_id": document_id,
            "source_authority": row["source_authority"],
            "source_path": source_paths[document_id],
            "status": "EXCLUDED",
            "exclusion_reason": row["exclusion_reason"],
        })

    header = parsed["header"]
    manifest = {
        "canon_id": header["canon_id"],
        "schema_version": header["schema_version"],
        "manifest_status": header["manifest_status"],
        "included_documents": sorted(included_documents, key=lambda d: d["sequence_narrative"]),
        "excluded_artifacts": excluded_artifacts,
        "open_schema_dispositions": [
            {"id": "OPEN-SCHEMA-001", "status": "recorded", "disposition": "no_required_v1_change"},
            {"id": "OPEN-SCHEMA-002", "status": "deferred", "disposition": "deferred_to_v1_1"},
        ],
    }
    return manifest


def write_draft_manifest(root: Path, manifest: dict[str, Any]) -> Path:
    path = root / DRAFT_JSON
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def load_manifest(manifest_path: Path, root: Path) -> tuple[dict[str, Any], Path]:
    if manifest_path.suffix.lower() == ".json":
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        return data, manifest_path
    manifest = build_draft_manifest_from_repository(root)
    written = write_draft_manifest(root, manifest)
    return manifest, written


def _status_allowed(status: str | None) -> bool:
    if not status:
        return False
    upper = status.upper()
    return "DRAFT" in upper or "AUTHORED" in upper


def validate_manifest_data(manifest: dict[str, Any], root: Path, manifest_path: Path) -> ValidationSummary:
    errors: list[ValidationIssue] = []
    warnings: list[ValidationIssue] = []

    canon_id = manifest.get("canon_id")
    schema_version = manifest.get("schema_version")
    status = manifest.get("manifest_status")
    if not canon_id:
        errors.append(ValidationIssue("manifest_parse_failure", "canon_id missing"))
    if not schema_version:
        errors.append(ValidationIssue("manifest_parse_failure", "schema_version missing"))
    if not _status_allowed(status):
        errors.append(ValidationIssue("manifest_parse_failure", "manifest_status must remain draft/authored, not sealed"))

    included = manifest.get("included_documents", [])
    excluded = manifest.get("excluded_artifacts", [])
    if not isinstance(included, list) or not isinstance(excluded, list):
        errors.append(ValidationIssue("manifest_parse_failure", "document arrays missing or malformed"))
        included, excluded = [], []

    all_docs = included + excluded
    document_ids: dict[str, dict[str, Any]] = {}
    source_paths: set[str] = set()
    excluded_paths = {record.get("source_path") for record in excluded}

    for record in all_docs:
        doc_id = record.get("document_id")
        src = record.get("source_path")
        if not doc_id:
            errors.append(ValidationIssue("manifest_parse_failure", "document record missing document_id"))
            continue
        if doc_id in document_ids:
            errors.append(ValidationIssue("duplicate_document_id", f"duplicate document_id: {doc_id}", document_id=doc_id))
        else:
            document_ids[doc_id] = record
        if not src:
            errors.append(ValidationIssue("manifest_parse_failure", f"missing source_path for {doc_id}", document_id=doc_id))
        elif src in source_paths:
            errors.append(ValidationIssue("duplicate_source_path", f"duplicate source_path: {src}", document_id=doc_id, path=src))
        else:
            source_paths.add(src)

    for record in included:
        doc_id = record["document_id"]
        src = record["source_path"]
        path = root / src
        if not path.exists():
            errors.append(ValidationIssue("missing_included_file", f"included file missing: {src}", document_id=doc_id, path=src))
        if src in excluded_paths:
            errors.append(ValidationIssue("excluded_file_ingested", f"excluded file also included: {src}", document_id=doc_id, path=src))
        layer = record.get("layer")
        if layer not in ALLOWED_LAYER:
            errors.append(ValidationIssue("invalid_enum", f"invalid layer for {doc_id}: {layer}", document_id=doc_id))
        if record.get("source_authority") not in ALLOWED_SOURCE_AUTHORITY:
            errors.append(ValidationIssue("invalid_enum", f"invalid source_authority for {doc_id}", document_id=doc_id))
        if record.get("temporal_status") not in ALLOWED_TEMPORAL_STATUS:
            errors.append(ValidationIssue("invalid_enum", f"invalid temporal_status for {doc_id}: {record.get('temporal_status')}", document_id=doc_id))
        if record.get("diegetic_frame") not in ALLOWED_FRAME:
            errors.append(ValidationIssue("invalid_enum", f"invalid diegetic_frame for {doc_id}: {record.get('diegetic_frame')}", document_id=doc_id))
        if "diegetic_certainty" in record and record.get("diegetic_certainty") not in ALLOWED_DIEGETIC_CERTAINTY:
            errors.append(ValidationIssue("invalid_enum", f"invalid diegetic_certainty for {doc_id}: {record.get('diegetic_certainty')}", document_id=doc_id))
        if "evidence_mode" in record and record.get("evidence_mode") not in ALLOWED_EVIDENCE_MODE:
            errors.append(ValidationIssue("invalid_enum", f"invalid evidence_mode for {doc_id}: {record.get('evidence_mode')}", document_id=doc_id))
        for relation in record.get("relations", []):
            namespace = relation.get("namespace")
            relation_type = relation.get("relation_type")
            target = relation.get("target_document_id")
            if namespace not in RELATION_NAMESPACES or relation_type not in RELATION_NAMESPACES.get(namespace, set()):
                errors.append(ValidationIssue("invalid_enum", f"invalid relation namespace/type on {doc_id}", document_id=doc_id))
            if target not in document_ids:
                errors.append(ValidationIssue("broken_relation", f"relation target missing: {target}", document_id=doc_id))

    for record in excluded:
        doc_id = record["document_id"]
        src = record["source_path"]
        if not (root / src).exists():
            errors.append(ValidationIssue("missing_excluded_file", f"excluded file missing: {src}", document_id=doc_id, path=src))
        if record.get("source_authority") not in ALLOWED_SOURCE_AUTHORITY:
            errors.append(ValidationIssue("invalid_enum", f"invalid source_authority for excluded {doc_id}", document_id=doc_id))

    layers = {layer: [doc for doc in included if doc.get("layer") == layer] for layer in ALLOWED_LAYER}
    if len(included) != EXPECTED_INCLUDED:
        errors.append(ValidationIssue("included_count_mismatch", f"expected {EXPECTED_INCLUDED} included documents, found {len(included)}"))
    if len(excluded) != EXPECTED_EXCLUDED:
        errors.append(ValidationIssue("included_count_mismatch", f"expected {EXPECTED_EXCLUDED} excluded artifacts, found {len(excluded)}"))
    for layer, expected in EXPECTED_LAYER_COUNTS.items():
        if len(layers[layer]) != expected:
            errors.append(ValidationIssue("included_count_mismatch", f"expected {expected} {layer} docs, found {len(layers[layer])}"))

    timer_docs = layers["timer"]
    if len(timer_docs) != 29:
        errors.append(ValidationIssue("missing_required_harvest_metadata", f"timer harvest count must equal 29, found {len(timer_docs)}"))
    for doc in timer_docs:
        for field in ["evidence_mode", "temporal_status", "diegetic_certainty", "relative_order_review", "composed_during"]:
            if field not in doc or doc.get(field) in (None, ""):
                errors.append(ValidationIssue("missing_required_harvest_metadata", f"timer harvest field missing: {field}", document_id=doc["document_id"]))
        if doc.get("sequence_within_frame") in (None, ""):
            warnings.append(ValidationIssue("sequence_within_frame_missing", "Timer sequence ordinals are not yet materialized.", document_id=doc["document_id"]))
        if doc.get("relative_order_review") and doc.get("sequence_within_frame") in (None, ""):
            warnings.append(ValidationIssue("relative_order_not_materialized", "relative_order_review is preserved without exact ordinals.", document_id=doc["document_id"]))
        if doc.get("composed_during") == "unknown":
            warnings.append(ValidationIssue("composed_during_unknown", "composed_during remains unknown where no explicit evidence exists.", document_id=doc["document_id"]))
        if doc.get("editorial_confidence") == "low":
            warnings.append(ValidationIssue("editorial_confidence_low", "editorial confidence remains low.", document_id=doc["document_id"]))

    bab_docs = layers["bab"]
    if len(bab_docs) != 29:
        errors.append(ValidationIssue("included_count_mismatch", f"bab confirmation count must equal 29, found {len(bab_docs)}"))
    if any(doc.get("diegetic_frame") != "bab-world" for doc in bab_docs):
        errors.append(ValidationIssue("invalid_enum", "all Bab must remain in bab-world"))
    for doc_id, expected_mode in EXPECTED_BAB_EXCEPTION.items():
        doc = document_ids.get(doc_id)
        if not doc or doc.get("evidence_mode") != expected_mode:
            errors.append(ValidationIssue("missing_required_harvest_metadata", f"Bab exception missing for {doc_id}: expected evidence_mode {expected_mode}", document_id=doc_id))

    codex_docs = layers["codex"]
    if len(codex_docs) != 5:
        errors.append(ValidationIssue("included_count_mismatch", f"codex confirmation count must equal 5, found {len(codex_docs)}"))
    for doc in codex_docs:
        if doc.get("diegetic_frame") is not None:
            errors.append(ValidationIssue("invalid_enum", f"Codex frame must be null for {doc['document_id']}", document_id=doc["document_id"]))
        if doc.get("temporal_status") != "atemporal":
            errors.append(ValidationIssue("invalid_enum", f"Codex temporal status must be atemporal for {doc['document_id']}", document_id=doc["document_id"]))
        if doc.get("source_authority") != "canonical":
            errors.append(ValidationIssue("invalid_enum", f"Codex source_authority must be canonical for {doc['document_id']}", document_id=doc["document_id"]))

    open_schema = {item.get("id"): item for item in manifest.get("open_schema_dispositions", [])}
    if "OPEN-SCHEMA-001" not in open_schema:
        errors.append(ValidationIssue("manifest_parse_failure", "OPEN-SCHEMA-001 disposition missing"))
    else:
        warnings.append(ValidationIssue("system_frame_uncertain", "system frame assignment remains recorded as debatable without requiring schema change.", document_id="system-opening"))
    if "OPEN-SCHEMA-002" not in open_schema:
        errors.append(ValidationIssue("manifest_parse_failure", "OPEN-SCHEMA-002 disposition missing"))
    else:
        warnings.append(ValidationIssue("in_universe_author_deferred", "OPEN-SCHEMA-002 remains deferred.", document_id="timer-02-50"))

    deduped_warnings = []
    seen_warning_keys = set()
    for warning in warnings:
        key = (warning.code, warning.document_id)
        if key not in seen_warning_keys:
            deduped_warnings.append(warning)
            seen_warning_keys.add(key)
    warnings = deduped_warnings

    result = "INVALID" if errors else "VALID_WITH_WARNINGS" if warnings else "VALID"
    exit_code = 1 if result == "INVALID" else 0
    statistics = {
        "included_documents": len(included),
        "excluded_artifacts": len(excluded),
        "layers": {layer: len(layers[layer]) for layer in ["bab", "timer", "codex", "system"]},
        "duplicate_document_ids": len([e for e in errors if e.code == "duplicate_document_id"]),
        "missing_files": len([e for e in errors if e.code in {"missing_included_file", "missing_excluded_file"}]),
        "broken_relations": len([e for e in errors if e.code == "broken_relation"]),
        "invalid_enums": len([e for e in errors if e.code == "invalid_enum"]),
        "timer_metadata_harvested": len(timer_docs),
        "bab_structurally_confirmed": len(bab_docs),
        "codex_structurally_confirmed": len(codex_docs),
    }
    return ValidationSummary(result=result, exit_code=exit_code, errors=errors, warnings=warnings, statistics=statistics, manifest_path=str(manifest_path))


def validate_manifest_file(manifest_path: Path | str, root: Path | str) -> dict[str, Any]:
    manifest_path = Path(manifest_path)
    root = Path(root)
    try:
        manifest, effective_manifest_path = load_manifest(manifest_path, root)
        summary = validate_manifest_data(manifest, root, effective_manifest_path)
        return summary.to_dict()
    except json.JSONDecodeError as exc:
        return ValidationSummary(
            result="INVALID",
            exit_code=1,
            errors=[ValidationIssue("manifest_parse_failure", f"JSON parse failed: {exc}")],
            warnings=[],
            statistics={},
            manifest_path=str(manifest_path),
        ).to_dict()
    except Exception as exc:  # pragma: no cover - runtime safety
        return ValidationSummary(
            result="RUNTIME_FAILURE",
            exit_code=2,
            errors=[ValidationIssue("runtime_failure", str(exc))],
            warnings=[],
            statistics={},
            manifest_path=str(manifest_path),
        ).to_dict()


def _print_terminal_summary(result: dict[str, Any]) -> None:
    stats = result.get("statistics", {})
    layers = stats.get("layers", {})
    print("VOID CORPUS VALIDATION")
    print("======================")
    print(f"Included documents: {stats.get('included_documents', 0)}/{EXPECTED_INCLUDED}")
    print(f"Excluded artifacts: {stats.get('excluded_artifacts', 0)}/{EXPECTED_EXCLUDED}")
    print(f"Bab: {layers.get('bab', 0)}")
    print(f"Timer: {layers.get('timer', 0)}")
    print(f"Codex: {layers.get('codex', 0)}")
    print(f"System: {layers.get('system', 0)}")
    print(f"Duplicate document IDs: {stats.get('duplicate_document_ids', 0)}")
    print(f"Missing files: {stats.get('missing_files', 0)}")
    print(f"Broken relations: {stats.get('broken_relations', 0)}")
    print(f"Invalid enums: {stats.get('invalid_enums', 0)}")
    print(f"Timer metadata harvested: {stats.get('timer_metadata_harvested', 0)}/29")
    print(f"Bab structurally confirmed: {stats.get('bab_structurally_confirmed', 0)}/29")
    print(f"Codex structurally confirmed: {stats.get('codex_structurally_confirmed', 0)}/5")
    print("Warnings:")
    grouped: list[str] = []
    warning_texts = {
        "sequence_within_frame_missing": "Timer sequence ordinals are not yet materialized.",
        "composed_during_unknown": "composed_during remains unknown where no explicit evidence exists.",
        "relative_order_not_materialized": "relative_order_review is preserved without exact ordinals.",
        "editorial_confidence_low": "Some harvested timer entries retain low editorial confidence.",
        "system_frame_uncertain": "system-opening frame assignment remains recorded as debatable.",
        "in_universe_author_deferred": "in_universe_author remains deferred where disposition says so.",
    }
    seen_codes = []
    for warning in result.get("warnings", []):
        code = warning["code"]
        if code not in seen_codes:
            seen_codes.append(code)
            grouped.append(warning_texts.get(code, warning["message"]))
    if not grouped:
        print("- none")
    else:
        for line in grouped:
            print(f"- {line}")
    print(f"RESULT: {result['result'].replace('_', ' ')}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=ROOT_MANIFEST)
    parser.add_argument("--root", default=".")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    manifest_path = root / args.manifest if not Path(args.manifest).is_absolute() else Path(args.manifest)
    result = validate_manifest_file(manifest_path, root)
    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    (root / OUTPUT_REPORT).write_text(json.dumps({k: v for k, v in result.items() if k != 'exit_code'}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if manifest_path.suffix.lower() != ".json" and result["result"] != "RUNTIME_FAILURE":
        manifest = build_draft_manifest_from_repository(root)
        write_draft_manifest(root, manifest)
    _print_terminal_summary(result)
    return int(result["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
