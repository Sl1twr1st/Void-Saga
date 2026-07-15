import json
import tempfile
import unittest
from pathlib import Path

from tools.void_corpus.validate import validate_manifest_file
from tools.void_corpus.generate_candidate import generate_candidate_file
from tools.void_corpus.seal_candidate import seal_candidate_file


BAB_IDS = [
    "bab-00", "bab-01", "bab-02", "bab-02-5", "bab-03", "bab-04", "bab-05", "bab-06", "bab-07", "bab-08",
    "bab-09", "bab-10", "bab-11", "bab-12", "bab-13", "bab-14", "bab-15", "bab-16", "bab-16-5", "bab-16-6",
    "bab-17", "bab-18", "bab-19", "bab-20", "bab-21", "bab-22", "bab-23", "bab-24", "bab-25",
]
TIMER_IDS = [
    "timer-00-00", "timer-01-00", "timer-02-00", "timer-02-50", "timer-03-00", "timer-04-00", "timer-05-00", "timer-06-00", "timer-07-00", "timer-08-00",
    "timer-09-00", "timer-10-00", "timer-11-00", "timer-12-00", "timer-13-00", "timer-14-00", "timer-15-00", "timer-16-00", "timer-16-50", "timer-16-66",
    "timer-17-00", "timer-18-00", "timer-19-00", "timer-20-00", "timer-21-00", "timer-22-00", "timer-23-00", "timer-24-00", "timer-25-00",
]
CODEX_IDS = ["codex-udara", "codex-air", "codex-api", "codex-tanah", "codex-the-void"]
SYSTEM_IDS = ["system-opening", "system-void-os-v6-6-6"]
EXCLUDED_IDS = ["sigil-os", "void-cosmology-paper", "naskah-lengkap"]


def _source_path(document_id: str) -> str:
    if document_id.startswith("bab-"):
        name = document_id.replace("bab-", "")
        display = name.replace("-", ".") if name in {"16-5", "16-6"} else name
        display = display.upper() if display in {"THE VOID"} else display
        display = display if display != "02.5" else "02-5"
        return f"Bab {display} — Menatap Akhir Era dari Balik.md"
    if document_id.startswith("timer-"):
        tail = document_id.replace("timer-", "").replace("-", "")
        return f"Timer {tail} — Menatap Akhir Semesta dari Balik.md"
    mapping = {
        "codex-udara": "Codex Udara — Menatap Akhir Semesta dari Balik.md",
        "codex-air": "Codex Air — Menatap Akhir Semesta dari Balik.md",
        "codex-api": "Codex Api — Menatap Akhir Semesta dari Balik.md",
        "codex-tanah": "Codex Tanah — Menatap Akhir Semesta dari Balik.md",
        "codex-the-void": "Codex The Void — Menatap Akhir Semesta dari Balik.md",
        "system-opening": "opening.md",
        "system-void-os-v6-6-6": "Void.OS v6.6.6 Update.md",
        "sigil-os": "Sigil_OS.md",
        "void-cosmology-paper": "THE VOID COSMOLOGY PAPER.md",
        "naskah-lengkap": "Void Saga — Naskah Lengkap.md",
    }
    return mapping[document_id]


def make_valid_manifest() -> dict:
    included = []
    seq = 10
    for document_id in SYSTEM_IDS:
        included.append({
            "document_id": document_id,
            "layer": "system",
            "source_authority": "canonical",
            "source_path": _source_path(document_id),
            "diegetic_frame": "bab-world" if document_id == "system-opening" else None,
            "temporal_status": "sequential" if document_id == "system-opening" else "recursive",
            "sequence_narrative": 10 if document_id == "system-opening" else 450,
            "relations": [] if document_id == "system-opening" else [{"namespace": "structural", "relation_type": "recontextualizes", "target_document_id": "system-opening"}],
        })
    for idx, document_id in enumerate(BAB_IDS, start=1):
        included.append({
            "document_id": document_id,
            "layer": "bab",
            "source_authority": "canonical",
            "source_path": _source_path(document_id),
            "diegetic_frame": "bab-world",
            "temporal_status": "sequential",
            "diegetic_certainty": "relative" if document_id == "bab-02-5" else "exact",
            "evidence_mode": "mixed" if document_id == "bab-02-5" else "witnessed",
            "sequence_narrative": 20 + (idx - 1) * 20,
            "sequence_within_frame": None,
            "confirmation_status": "confirmed",
            "relations": [],
        })
    timer_seq_values = [30, 50, 70, 90, 110, 140, 160, 180, 200, 220, 240, 260, 280, 320, 340, 360, 380, 400, 420, 440, 470, 490, 510, 530, 550, 570, 590, 610, 630]
    harvest_modes = {"timer-00-00": "archival", "timer-02-50": "archival", "timer-07-00": "mixed", "timer-11-00": "archival", "timer-12-00": "archival", "timer-14-00": "archival", "timer-15-00": "archival", "timer-16-00": "mixed", "timer-16-66": "archival", "timer-17-00": "archival", "timer-22-00": "archival", "timer-23-00": "mixed", "timer-25-00": "archival"}
    harvest_temp = {"timer-00-00": "retroactive", "timer-02-50": "retroactive", "timer-07-00": "uncertain", "timer-11-00": "retroactive", "timer-12-00": "retroactive", "timer-13-00": "recursive", "timer-14-00": "retroactive", "timer-15-00": "retroactive", "timer-16-66": "uncertain", "timer-17-00": "uncertain", "timer-22-00": "recursive", "timer-23-00": "recursive", "timer-24-00": "recursive", "timer-25-00": "retroactive"}
    harvest_certainty = {"timer-02-50": "relative", "timer-07-00": "relative", "timer-08-00": "relative", "timer-11-00": "unknown", "timer-12-00": "relative", "timer-13-00": "relative", "timer-14-00": "relative", "timer-15-00": "relative", "timer-16-66": "relative", "timer-17-00": "relative", "timer-21-00": "relative", "timer-22-00": "unknown", "timer-23-00": "relative", "timer-24-00": "relative", "timer-25-00": "relative"}
    low_conf = {"timer-16-66", "timer-22-00"}
    medium_conf = {"timer-02-50", "timer-07-00", "timer-08-00", "timer-11-00", "timer-12-00", "timer-13-00", "timer-17-00", "timer-21-00", "timer-23-00", "timer-24-00"}
    relative_order = {tid: "sesudah" for tid in TIMER_IDS}
    for tid in ["timer-00-00", "timer-11-00", "timer-12-00", "timer-14-00", "timer-15-00", "timer-25-00"]:
        relative_order[tid] = "sebelum"
    for tid in ["timer-02-50", "timer-16-66"]:
        relative_order[tid] = "bersamaan"
    composed = {
        "timer-00-00": "bab-00", "timer-02-50": "bab-03", "timer-03-00": "bab-03", "timer-05-00": "bab-05", "timer-07-00": "bab-07", "timer-10-00": "bab-10",
        "timer-11-00": "bab-11", "timer-13-00": "bab-13", "timer-14-00": "bab-14", "timer-16-00": "bab-16", "timer-16-50": "bab-16-5", "timer-17-00": "bab-17", "timer-18-00": "bab-18"
    }
    for document_id, seq_narr in zip(TIMER_IDS, timer_seq_values):
        relations = []
        if document_id in composed and composed[document_id] != "unknown":
            relations.append({"namespace": "composition", "relation_type": "composed_during", "target_document_id": composed[document_id]})
        if document_id == "timer-10-00":
            relations.append({"namespace": "composition", "relation_type": "deleted_during", "target_document_id": "bab-10"})
        if document_id == "timer-20-00":
            relations.append({"namespace": "composition", "relation_type": "deleted_during", "target_document_id": "bab-20"})
        included.append({
            "document_id": document_id,
            "layer": "timer",
            "source_authority": "canonical",
            "source_path": _source_path(document_id),
            "diegetic_frame": "timer-world",
            "temporal_status": harvest_temp.get(document_id, "sequential"),
            "diegetic_certainty": harvest_certainty.get(document_id, "exact"),
            "evidence_mode": harvest_modes.get(document_id, "witnessed"),
            "editorial_confidence": "low" if document_id in low_conf else "medium" if document_id in medium_conf else "high",
            "relative_order_review": relative_order[document_id],
            "composed_during": composed.get(document_id, "unknown"),
            "sequence_narrative": seq_narr,
            "sequence_within_frame": None,
            "relations": relations,
        })
    codex_seq = {"codex-udara": 130, "codex-air": 290, "codex-api": 300, "codex-tanah": 640, "codex-the-void": 650}
    placement = {"codex-udara": "after bab-04", "codex-air": "after timer-11-00", "codex-api": "after codex-air", "codex-tanah": "after timer-25-00", "codex-the-void": "end of corpus"}
    for document_id in CODEX_IDS:
        included.append({
            "document_id": document_id,
            "layer": "codex",
            "source_authority": "canonical",
            "source_path": _source_path(document_id),
            "diegetic_frame": None,
            "temporal_status": "atemporal",
            "diegetic_certainty": "not_applicable",
            "sequence_narrative": codex_seq[document_id],
            "narrative_placement": placement[document_id],
            "relations": [],
        })
    excluded = [{
        "document_id": did,
        "source_authority": "derived" if did == "naskah-lengkap" else "supplemental",
        "source_path": _source_path(did),
        "status": "EXCLUDED",
        "exclusion_reason": "fixture"
    } for did in EXCLUDED_IDS]
    return {
        "canon_id": "void-saga-canon-v1.0",
        "schema_version": "CORPUS_SCHEMA_V1",
        "manifest_status": "DRAFT",
        "included_documents": included,
        "excluded_artifacts": excluded,
        "open_schema_dispositions": [
            {"id": "OPEN-SCHEMA-001", "status": "recorded", "disposition": "no_required_v1_change"},
            {"id": "OPEN-SCHEMA-002", "status": "deferred", "disposition": "deferred_to_v1_1"},
        ],
    }


def write_fixture(root: Path, manifest: dict) -> Path:
    for record in manifest["included_documents"] + manifest["excluded_artifacts"]:
        path = root / record["source_path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(record["document_id"], encoding="utf-8")
    (root / "proofing").mkdir(parents=True, exist_ok=True)
    (root / "proofing" / "example.txt").write_text("ignored", encoding="utf-8")
    manifest_path = root / "canon-manifest-v1.draft.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest_path


def write_validation_report(root: Path, result: str = "VALID_WITH_WARNINGS") -> Path:
    report = {
        "result": result,
        "errors": [] if result != "INVALID" else [{"code": "included_count_mismatch", "message": "fixture invalid"}],
        "warnings": [{"code": "sequence_within_frame_missing", "message": "fixture warning"}] if result == "VALID_WITH_WARNINGS" else [],
        "statistics": {
            "included_documents": 65,
            "excluded_artifacts": 3,
            "layers": {"bab": 29, "timer": 29, "codex": 5, "system": 2},
        },
    }
    output_dir = root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "corpus-validation-report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report_path


def init_git_repo(root: Path) -> str:
    import subprocess
    subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "config", "user.name", "Hermes Test"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.email", "hermes@example.com"], cwd=root, check=True)
    subprocess.run(["git", "add", "."], cwd=root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "commit", "-m", "fixture"], cwd=root, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    return commit


class VoidCorpusValidateTests(unittest.TestCase):
    def validate(self, mutate=None):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = make_valid_manifest()
            if mutate:
                mutate(manifest, root)
            manifest_path = write_fixture(root, manifest)
            return validate_manifest_file(manifest_path, root)

    def test_valid_manifest_passes(self):
        result = self.validate()
        self.assertEqual(result["result"], "VALID_WITH_WARNINGS")
        self.assertEqual(result["exit_code"], 0)

    def test_missing_included_file_fails(self):
        def mutate(manifest, root):
            pass
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = make_valid_manifest()
            manifest_path = write_fixture(root, manifest)
            (root / manifest["included_documents"][0]["source_path"]).unlink()
            result = validate_manifest_file(manifest_path, root)
            self.assertEqual(result["result"], "INVALID")
            self.assertTrue(any(e["code"] == "missing_included_file" for e in result["errors"]))

    def test_missing_excluded_file_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = make_valid_manifest()
            manifest_path = write_fixture(root, manifest)
            (root / manifest["excluded_artifacts"][0]["source_path"]).unlink()
            result = validate_manifest_file(manifest_path, root)
            self.assertEqual(result["result"], "INVALID")
            self.assertTrue(any(e["code"] == "missing_excluded_file" for e in result["errors"]))

    def test_duplicate_document_id_fails(self):
        def mutate(manifest, root):
            manifest["included_documents"].append(dict(manifest["included_documents"][0]))
        result = self.validate(mutate)
        self.assertEqual(result["result"], "INVALID")
        self.assertTrue(any(e["code"] == "duplicate_document_id" for e in result["errors"]))

    def test_duplicate_source_path_fails(self):
        def mutate(manifest, root):
            manifest["included_documents"][1]["source_path"] = manifest["included_documents"][0]["source_path"]
        result = self.validate(mutate)
        self.assertEqual(result["result"], "INVALID")
        self.assertTrue(any(e["code"] == "duplicate_source_path" for e in result["errors"]))

    def test_invalid_layer_fails(self):
        def mutate(manifest, root):
            manifest["included_documents"][0]["layer"] = "weird"
        result = self.validate(mutate)
        self.assertEqual(result["result"], "INVALID")
        self.assertTrue(any(e["code"] == "invalid_enum" for e in result["errors"]))

    def test_broken_relation_fails(self):
        def mutate(manifest, root):
            manifest["included_documents"][31]["relations"].append({"namespace": "structural", "relation_type": "recontextualizes", "target_document_id": "missing-doc"})
        result = self.validate(mutate)
        self.assertEqual(result["result"], "INVALID")
        self.assertTrue(any(e["code"] == "broken_relation" for e in result["errors"]))

    def test_excluded_file_cannot_be_included(self):
        def mutate(manifest, root):
            manifest["included_documents"].append({
                "document_id": "dupe-excluded",
                "layer": "bab",
                "source_authority": "canonical",
                "source_path": manifest["excluded_artifacts"][0]["source_path"],
                "diegetic_frame": "bab-world",
                "temporal_status": "sequential",
                "diegetic_certainty": "exact",
                "evidence_mode": "witnessed",
                "sequence_narrative": 999,
                "sequence_within_frame": None,
                "relations": [],
            })
        result = self.validate(mutate)
        self.assertEqual(result["result"], "INVALID")
        self.assertTrue(any(e["code"] == "excluded_file_ingested" for e in result["errors"]))

    def test_timer_harvest_count_must_equal_29(self):
        def mutate(manifest, root):
            manifest["included_documents"] = [d for d in manifest["included_documents"] if d["document_id"] != "timer-25-00"]
        result = self.validate(mutate)
        self.assertEqual(result["result"], "INVALID")
        self.assertTrue(any(e["code"] == "missing_required_harvest_metadata" for e in result["errors"]))

    def test_missing_timer_sequence_is_warning(self):
        result = self.validate()
        self.assertTrue(any(w["code"] == "sequence_within_frame_missing" for w in result["warnings"]))

    def test_unknown_composed_during_is_allowed(self):
        result = self.validate()
        self.assertFalse(any(e["code"] == "composed_during_unknown" for e in result["errors"]))
        self.assertTrue(any(w["code"] == "composed_during_unknown" for w in result["warnings"]))

    def test_bab_confirmation_count_must_equal_29(self):
        def mutate(manifest, root):
            manifest["included_documents"] = [d for d in manifest["included_documents"] if d["document_id"] != "bab-25"]
        result = self.validate(mutate)
        self.assertEqual(result["result"], "INVALID")
        self.assertTrue(any(e["code"] == "included_count_mismatch" for e in result["errors"]))

    def test_codex_confirmation_count_must_equal_5(self):
        def mutate(manifest, root):
            manifest["included_documents"] = [d for d in manifest["included_documents"] if d["document_id"] != "codex-the-void"]
        result = self.validate(mutate)
        self.assertEqual(result["result"], "INVALID")
        self.assertTrue(any(e["code"] == "included_count_mismatch" for e in result["errors"]))

    def test_out_of_scope_files_are_ignored(self):
        result = self.validate()
        self.assertFalse(any(e["code"] == "out_of_scope_file_detected" for e in result["errors"]))


class SealCandidateTests(unittest.TestCase):
    def seal(self, mutate_manifest=None, mutate_files=None, validator_result="VALID_WITH_WARNINGS", mutate_candidate=None):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = make_valid_manifest()
            if mutate_manifest:
                mutate_manifest(manifest, root)
            manifest_path = write_fixture(root, manifest)
            report_path = write_validation_report(root, validator_result)
            commit = init_git_repo(root)
            candidate_path = root / "canon-v1.0.candidate.json"
            generate_candidate_file(manifest_path, root, report_path=report_path, output_path=candidate_path)
            if mutate_files:
                mutate_files(manifest, root)
            if mutate_candidate:
                data = json.loads(candidate_path.read_text(encoding="utf-8"))
                mutate_candidate(data)
                candidate_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
            sealed_path = root / "canon-v1.0.json"
            sealed = seal_candidate_file(candidate_path, root, sealed_by="Rizali Alma", output_path=sealed_path)
            sealed_written = sealed_path.read_text(encoding="utf-8")
            candidate_written = candidate_path.read_text(encoding="utf-8")
            return sealed, sealed_written, candidate_written, commit

    def test_valid_candidate_can_be_sealed(self):
        sealed, sealed_written, _, _ = self.seal()
        self.assertIn('"status": "sealed"', sealed_written)
        self.assertEqual(sealed["status"], "sealed")

    def test_sealed_output_preserves_corpus_hash(self):
        sealed, _, candidate_written, _ = self.seal()
        candidate = json.loads(candidate_written)
        self.assertEqual(sealed["corpus_hash"], candidate["corpus_hash"])
        self.assertEqual(sealed["candidate_corpus_hash"], candidate["corpus_hash"])

    def test_modified_source_blocks_seal(self):
        with self.assertRaisesRegex(ValueError, "(included source changed since candidate creation|git working tree has corpus/manifest changes)"):
            self.seal(mutate_files=lambda manifest, root: (root / manifest["included_documents"][0]["source_path"]).write_text("mutated", encoding="utf-8"))

    def test_invalid_validator_result_blocks_seal(self):
        with self.assertRaisesRegex(ValueError, "validator result must be VALID or VALID_WITH_WARNINGS"):
            self.seal(validator_result="INVALID")

    def test_candidate_status_required(self):
        with self.assertRaisesRegex(ValueError, "candidate status must be 'candidate'"):
            self.seal(mutate_candidate=lambda data: data.update({"status": "sealed"}))

    def test_sealed_output_never_overwrites_candidate(self):
        _, sealed_written, candidate_written, _ = self.seal()
        candidate = json.loads(candidate_written)
        self.assertEqual(candidate["status"], "candidate")
        self.assertIn('"status": "sealed"', sealed_written)

    def test_document_count_change_blocks_seal(self):
        with self.assertRaisesRegex(ValueError, "candidate document count mismatch"):
            self.seal(mutate_candidate=lambda data: data.update({"document_count": 64}))

    def test_seal_metadata_is_recorded(self):
        sealed, _, _, commit = self.seal()
        self.assertEqual(sealed["sealed_by"], "Rizali Alma")
        self.assertEqual(sealed["source_git_commit"], commit)
        self.assertEqual(sealed["validator_result"], "VALID_WITH_WARNINGS")


class CandidateSnapshotGeneratorTests(unittest.TestCase):
    def generate(self, mutate_manifest=None, mutate_files=None, validator_result="VALID_WITH_WARNINGS"):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = make_valid_manifest()
            if mutate_manifest:
                mutate_manifest(manifest, root)
            manifest_path = write_fixture(root, manifest)
            report_path = write_validation_report(root, validator_result)
            if mutate_files:
                mutate_files(manifest, root)
            commit = init_git_repo(root)
            candidate_path = root / "canon-v1.0.candidate.json"
            candidate = generate_candidate_file(manifest_path, root, report_path=report_path, output_path=candidate_path)
            written = candidate_path.read_text(encoding="utf-8")
            return candidate, written, commit

    def test_candidate_generation_succeeds_from_current_valid_manifest(self):
        candidate, written, commit = self.generate()
        self.assertIn('"status": "candidate"', written)
        self.assertEqual(candidate["status"], "candidate")
        self.assertEqual(candidate["version"], "1.0.0")
        self.assertEqual(candidate["document_count"], 65)
        self.assertEqual(candidate["excluded_artifact_count"], 3)
        self.assertEqual(candidate["source_git_commit"], commit)

    def test_deterministic_rerun_produces_same_corpus_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = make_valid_manifest()
            manifest_path = write_fixture(root, manifest)
            report_path = write_validation_report(root)
            init_git_repo(root)
            first = generate_candidate_file(manifest_path, root, report_path=report_path, output_path=root / "first.json")
            second = generate_candidate_file(manifest_path, root, report_path=report_path, output_path=root / "second.json")
            self.assertEqual(first["corpus_hash"], second["corpus_hash"])

    def test_changing_one_source_byte_changes_document_hash_and_corpus_hash(self):
        baseline, _, _ = self.generate()
        changed, _, _ = self.generate(mutate_files=lambda manifest, root: (root / manifest["included_documents"][0]["source_path"]).write_text("mutated", encoding="utf-8"))
        doc_id = baseline["documents"][0]["document_id"]
        before = {d["document_id"]: d for d in baseline["documents"]}[doc_id]
        after = {d["document_id"]: d for d in changed["documents"]}[doc_id]
        self.assertNotEqual(before["document_hash"], after["document_hash"])
        self.assertNotEqual(baseline["corpus_hash"], changed["corpus_hash"])

    def test_missing_document_blocks_generation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = make_valid_manifest()
            manifest_path = write_fixture(root, manifest)
            report_path = write_validation_report(root)
            init_git_repo(root)
            (root / manifest["included_documents"][0]["source_path"]).unlink()
            with self.assertRaisesRegex(ValueError, "missing included source file"):
                generate_candidate_file(manifest_path, root, report_path=report_path, output_path=root / "candidate.json")

    def test_invalid_validator_result_blocks_generation(self):
        with self.assertRaisesRegex(ValueError, "validator result must be VALID or VALID_WITH_WARNINGS"):
            self.generate(validator_result="INVALID")

    def test_excluded_artifact_changes_do_not_affect_corpus_hash(self):
        baseline, _, _ = self.generate()
        changed, _, _ = self.generate(mutate_files=lambda manifest, root: (root / manifest["excluded_artifacts"][0]["source_path"]).write_text("changed excluded", encoding="utf-8"))
        self.assertEqual(baseline["corpus_hash"], changed["corpus_hash"])

    def test_document_ordering_does_not_affect_final_corpus_hash(self):
        baseline, _, _ = self.generate()
        reversed_candidate, _, _ = self.generate(mutate_manifest=lambda manifest, root: manifest.update({"included_documents": list(reversed(manifest["included_documents"]))}))
        self.assertEqual(baseline["corpus_hash"], reversed_candidate["corpus_hash"])

    def test_candidate_status_is_never_sealed(self):
        candidate, _, _ = self.generate()
        self.assertEqual(candidate["status"], "candidate")
        self.assertNotEqual(candidate["status"], "sealed")

    def test_git_commit_metadata_is_recorded(self):
        candidate, _, commit = self.generate()
        self.assertEqual(candidate["source_git_commit"], commit)


if __name__ == "__main__":
    unittest.main()
