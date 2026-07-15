from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .generate_candidate import generate_candidate, _load_json
from .validate import validate_manifest_file

DEFAULT_CANDIDATE = "canon-v1.0.candidate.json"
DEFAULT_OUTPUT = "canon-v1.0.json"
MANIFEST_JSON = "canon-manifest-v1.draft.json"
MANIFEST_MD = "CANON_MANIFEST_DRAFT.md"
WARNING_STATUS = {
    "sequence_within_frame_missing": {"status": "accepted_for_v1", "disposition": "accepted_for_v1"},
    "relative_order_not_materialized": {"status": "accepted_for_v1", "disposition": "accepted_for_v1"},
    "composed_during_unknown": {"status": "accepted_for_v1", "disposition": "accepted_for_v1"},
    "editorial_confidence_low": {"status": "accepted_for_v1", "disposition": "accepted_for_v1"},
    "system_frame_uncertain": {"status": "deferred_with_disposition", "disposition": "OPEN-SCHEMA-001"},
    "in_universe_author_deferred": {"status": "deferred_with_disposition", "disposition": "OPEN-SCHEMA-002"},
}
BLOCKING_STATUSES = {"blocking"}


def _git_head(root: Path) -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    except Exception:
        return None


def _git_commit_exists(root: Path, commit: str) -> bool:
    try:
        subprocess.run(["git", "rev-parse", "--verify", f"{commit}^{{commit}}"], cwd=root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False


def _git_status_lines(root: Path) -> list[str]:
    try:
        out = subprocess.check_output(["git", "status", "--porcelain"], cwd=root, text=True)
        return [line for line in out.splitlines() if line.strip()]
    except Exception:
        return []


def _tracked_corpus_changes(root: Path, candidate_path: Path) -> tuple[list[str], list[str]]:
    manifest = _load_json(root / MANIFEST_JSON)
    corpus_paths = {record['source_path'] for record in manifest.get('included_documents', [])}
    corpus_paths.update(record['source_path'] for record in manifest.get('excluded_artifacts', []))
    corpus_paths.add(MANIFEST_JSON)
    corpus_paths.add(MANIFEST_MD)
    changed = []
    warnings = []
    for line in _git_status_lines(root):
        status = line[:2]
        path = line[3:]
        if path in corpus_paths:
            changed.append(path)
        elif path == str(candidate_path.relative_to(root)):
            continue
        elif path.startswith('proofing/') or path == 'proofing/':
            warnings.append(path)
    return changed, warnings


def _accepted_warnings(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    accepted = []
    seen = set()
    for warning in candidate.get('validator', {}).get('warnings', []):
        code = warning['code']
        if code in seen:
            continue
        seen.add(code)
        meta = WARNING_STATUS.get(code, {"status": "blocking", "disposition": None})
        accepted.append({"code": code, **meta})
    return accepted


def seal_candidate(candidate: dict[str, Any], root: Path, sealed_by: str) -> tuple[dict[str, Any], list[str]]:
    if candidate.get('status') != 'candidate':
        raise ValueError("candidate status must be 'candidate'")
    if candidate.get('document_count') != len(candidate.get('documents', [])):
        raise ValueError('candidate document count mismatch')
    source_commit = candidate.get('source_git_commit')
    if not source_commit or not _git_commit_exists(root, source_commit):
        raise ValueError('candidate source commit could not be verified')

    manifest_path = root / MANIFEST_JSON
    validator_result = validate_manifest_file(manifest_path, root)
    if validator_result.get('result') not in {'VALID', 'VALID_WITH_WARNINGS'}:
        raise ValueError('validator result must be VALID or VALID_WITH_WARNINGS')

    current_manifest = _load_json(root / MANIFEST_JSON)
    regenerated = generate_candidate(current_manifest, validator_result, root, str(manifest_path))
    if regenerated['document_count'] != candidate['document_count']:
        raise ValueError('candidate document count mismatch')
    if regenerated['corpus_hash'] != candidate['corpus_hash']:
        raise ValueError('corpus hash changed since candidate creation')

    current_docs = {doc['document_id']: doc for doc in regenerated['documents']}
    for doc in candidate['documents']:
        cur = current_docs.get(doc['document_id'])
        if cur is None:
            raise ValueError(f"missing candidate document during seal: {doc['document_id']}")
        if cur['source_hash'] != doc['source_hash']:
            raise ValueError(f"included source changed since candidate creation: {doc['document_id']}")

    accepted_warnings = _accepted_warnings(candidate)
    if any(item['status'] in BLOCKING_STATUSES for item in accepted_warnings):
        raise ValueError('blocking warnings present; candidate not sealable')

    sealed = dict(candidate)
    sealed['status'] = 'sealed'
    sealed['sealed_at'] = datetime.now(timezone.utc).isoformat()
    sealed['sealed_by'] = sealed_by
    sealed['seal_git_commit'] = _git_head(root)
    sealed['source_git_commit'] = source_commit
    sealed['corpus_hash'] = candidate['corpus_hash']
    sealed['candidate_corpus_hash'] = candidate['corpus_hash']
    sealed['validator_result'] = candidate.get('validator', {}).get('result')
    sealed['accepted_warnings'] = accepted_warnings
    sealed['previous_canon_id'] = candidate.get('previous_canon_id')
    return sealed, [w for w in _tracked_corpus_changes(root, root / DEFAULT_CANDIDATE)[1]]


def seal_candidate_file(candidate_path: Path | str, root: Path | str, sealed_by: str, output_path: Path | str | None = None) -> dict[str, Any]:
    root = Path(root)
    candidate_path = Path(candidate_path)
    changed, warnings = _tracked_corpus_changes(root, candidate_path)
    if changed:
        raise ValueError('git working tree has corpus/manifest changes: ' + ', '.join(changed))
    candidate = _load_json(candidate_path)
    sealed, extra_warnings = seal_candidate(candidate, root, sealed_by)
    if warnings or extra_warnings:
        sealed['seal_warnings'] = sorted(set(warnings + extra_warnings))
    destination = Path(output_path) if output_path else root / DEFAULT_OUTPUT
    if destination == candidate_path:
        raise ValueError('sealed output must not overwrite candidate')
    destination.write_text(json.dumps(sealed, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return sealed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--candidate', default=DEFAULT_CANDIDATE)
    parser.add_argument('--output', default=DEFAULT_OUTPUT)
    parser.add_argument('--root', default='.')
    parser.add_argument('--sealed-by', default='Rizali Alma')
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    candidate_path = root / args.candidate if not Path(args.candidate).is_absolute() else Path(args.candidate)
    output_path = root / args.output if not Path(args.output).is_absolute() else Path(args.output)
    sealed = seal_candidate_file(candidate_path, root, sealed_by=args.sealed_by, output_path=output_path)
    print(json.dumps({
        'status': sealed['status'],
        'corpus_hash': sealed['corpus_hash'],
        'candidate_corpus_hash': sealed['candidate_corpus_hash'],
        'validator_result': sealed['validator_result'],
        'output': str(output_path),
        'seal_git_commit': sealed['seal_git_commit'],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
