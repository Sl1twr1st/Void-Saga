from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .validate import validate_manifest_file

DEFAULT_MANIFEST = "canon-manifest-v1.draft.json"
DEFAULT_REPORT = "outputs/corpus-validation-report.json"
DEFAULT_OUTPUT = "canon-v1.0.candidate.json"


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_validator_result(manifest_path: Path, root: Path, report_path: Path | None) -> tuple[dict[str, Any], str]:
    if report_path and report_path.exists():
        result = _load_json(report_path)
        return result, str(report_path)
    result = validate_manifest_file(manifest_path, root)
    return result, str(manifest_path)


def _git_commit(root: Path) -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    except Exception:
        return None


def _build_document_record(root: Path, record: dict[str, Any]) -> dict[str, Any]:
    source_path = root / record["source_path"]
    if not source_path.exists():
        raise ValueError(f"missing included source file: {record['source_path']}")
    raw = source_path.read_bytes()
    source_hash = _sha256_bytes(raw)
    document_hash = source_hash
    enriched = dict(record)
    enriched["source_hash"] = source_hash
    enriched["document_hash"] = document_hash
    return enriched


def _corpus_hash(documents: list[dict[str, Any]]) -> str:
    ordered = sorted((doc["document_id"], doc["document_hash"]) for doc in documents)
    payload = "\n".join(f"{document_id}:{document_hash}" for document_id, document_hash in ordered).encode("utf-8")
    return _sha256_bytes(payload)


def generate_candidate(manifest: dict[str, Any], validator_result: dict[str, Any], root: Path, validator_reference: str) -> dict[str, Any]:
    result = validator_result.get("result")
    if result not in {"VALID", "VALID_WITH_WARNINGS"}:
        raise ValueError("validator result must be VALID or VALID_WITH_WARNINGS")

    included = manifest.get("included_documents", [])
    excluded = manifest.get("excluded_artifacts", [])
    documents = [_build_document_record(root, record) for record in included]
    candidate = {
        "canon_id": manifest.get("canon_id"),
        "version": "v1.0",
        "status": "candidate",
        "schema_version": manifest.get("schema_version"),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "document_count": len(documents),
        "excluded_artifact_count": len(excluded),
        "layers": validator_result.get("statistics", {}).get("layers", {}),
        "documents": documents,
        "corpus_hash": _corpus_hash(documents),
        "previous_canon_id": None,
        "validator": {
            "result": result,
            "reference": validator_reference,
            "warnings": validator_result.get("warnings", []),
            "errors": validator_result.get("errors", []),
        },
        "source_git_commit": _git_commit(root),
    }
    return candidate


def generate_candidate_file(
    manifest_path: Path | str,
    root: Path | str,
    report_path: Path | str | None = None,
    output_path: Path | str | None = None,
) -> dict[str, Any]:
    manifest_path = Path(manifest_path)
    root = Path(root)
    report = Path(report_path) if report_path else None
    manifest = _load_json(manifest_path)
    validator_result, validator_reference = _load_validator_result(manifest_path, root, report)
    candidate = generate_candidate(manifest, validator_result, root, validator_reference)
    destination = Path(output_path) if output_path else root / DEFAULT_OUTPUT
    destination.write_text(json.dumps(candidate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return candidate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST)
    parser.add_argument("--report", default=DEFAULT_REPORT)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--root", default=".")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    manifest_path = root / args.manifest if not Path(args.manifest).is_absolute() else Path(args.manifest)
    report_path = root / args.report if args.report and not Path(args.report).is_absolute() else Path(args.report)
    output_path = root / args.output if not Path(args.output).is_absolute() else Path(args.output)
    candidate = generate_candidate_file(manifest_path, root, report_path=report_path, output_path=output_path)
    print(json.dumps({
        "status": candidate["status"],
        "document_count": candidate["document_count"],
        "excluded_artifact_count": candidate["excluded_artifact_count"],
        "corpus_hash": candidate["corpus_hash"],
        "source_git_commit": candidate["source_git_commit"],
        "validator_result": candidate["validator"]["result"],
        "output": str(output_path),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
