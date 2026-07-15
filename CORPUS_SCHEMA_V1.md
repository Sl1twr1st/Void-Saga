# CORPUS_SCHEMA_V1 — Void Saga Canon Corpus Schema

```
Status:           FROZEN
Schema version:   1.0.0
Frozen:           2026-07-15
Governs:          void-saga-canon-v1.0 (NOT YET SEALED)
Companion:        CANON_MANIFEST_DRAFT.md (AUTHORIZED FOR AUTHORING)
Provenance:       Jali × Claude design session, 2026-07-14 → 2026-07-15
```

---

## 0. What "FROZEN" means — and does not mean

> Freeze tidak berarti seluruh metadata sudah final. Freeze berarti bentuk
> representasinya sudah cukup stabil untuk menerima seluruh corpus tanpa
> memalsukan struktur, chronology, provenance, atau authority.

Explicitly **NOT** implied by this freeze:

- `evidence_mode` hasil inheritance **bukan** klasifikasi final.
- Frame assignment system-document dengan confidence 0.5 **bukan** canon truth.
- `in_universe_author` yang ditunda (OPEN-SCHEMA-002) **bukan** kelalaian —
  ia deferral yang tercatat.
- Manifest draft **bukan** sealed canon.

Schema changes after this point require a new `schema_version` and a decision
log entry in `research/`.

---

## 1. Governing identity

> Void Engine is the evidence and interpretation layer of the Void Saga
> ecosystem. It audits claims against **sealed corpus snapshots** and supplies
> traceable evidence to readers, writers, and downstream constitutional
> systems. It does not create canon, approve forks, or replace the
> Invariant Engine.

This schema is a **shared primitive** between the Evidence Engine
(rag-project) and the Invariant Engine (VOID_SAGA_UNIVERSE):

```
Shared:      corpus schema, document identity, citation format,
             document hashing, verdict envelope states (VALID / INVALID / UNRESOLVED)
Not shared:  final verdict vocabulary, doctrine logic, workflow, user surface
```

---

## 2. Design principles

The schema stores **structure, not interpretation**. It must carry exactly
enough for an engine to:

1. menemukan sumber,
2. membedakan jenis kesaksian,
3. mengetahui posisi naratif,
4. mengetahui posisi diegetik jika tersedia,
5. melacak perubahan corpus,
6. membuat sitasi stabil,
7. tidak mencampur deklarasi dunia dengan kejadian dunia.

**Forbidden in base metadata** (derived interpretation — belongs to separate,
clearly-statused pipelines, never to corpus identity):

```
theme, character_arc, importance, truth_score, reliability_score,
symbolism, emotional_meaning, invariant_status
```

---

## 3. Canon snapshot

The highest-level object is not a document. It is a snapshot.

```json
{
  "canon_id": "void-saga-canon-v1.0",
  "schema_version": "1.0.0",
  "version": "1.0.0",
  "status": "draft",
  "sealed_at": null,
  "corpus_hash": null,
  "previous_canon_id": null,
  "counts": {
    "discovered_file_count": null,
    "registered_document_count": null,
    "included_canonical_document_count": null
  },
  "notes": "Initial Void Saga corpus."
}
```

**Rules:**

- `status` enum: `draft → candidate → sealed → superseded`. Ingestion writes
  to a *candidate*, never to an active sealed canon.
- All counts are **validator output**. They are never hand-typed and never
  copied from a document like this one.
- `canon_id` must appear on every document, section, chunk, evidence
  citation, and audit instance. A verdict without a `canon_id` is a verdict
  about no world in particular.
- After seal: mutation in-place is forbidden. Change = next candidate
  (`canon-v1.1`).

---

## 4. Document identity

```json
{
  "document_id": "bab-00",
  "canon_id": "void-saga-canon-v1.0",
  "work_id": "menatap-akhir",
  "layer": "bab",
  "source_authority": "canonical",
  "title": "Bab 00 — Menatap Akhir Era dari Balik Laptop Kantor",
  "language": ["id", "en"],
  "sequence_label": "00",
  "source_path": "Bab 00 — Menatap Akhir Era dari Balik.md",
  "source_hash": "sha256:...",
  "document_hash": "sha256:..."
}
```

**Rules:**

- `document_id` is a stable slug, independent of filename and title:
  `bab-00`, `bab-02-5`, `bab-16-5`, `bab-16-6`, `timer-00-00`,
  `timer-02-50`, `timer-16-66`, `codex-udara`, `system-opening`,
  `system-void-os-v6-6-6`. Titles may change. Identity may not.
- Filename inconsistency is real in this corpus (`Bab 02-5` uses a dash,
  `Bab 16.5` uses a dot). Identity is therefore **never** derived from
  filenames at query time — only via the manifest, once, at ingestion.

---

## 5. Layers

Two lists, deliberately distinct:

```json
{
  "schema_supported_layers": ["bab", "timer", "codex", "system", "void_incident"],
  "manifest_active_layers":  ["bab", "timer", "codex", "system"]
}
```

Schema describes what the format **can hold**. Manifest describes what the
snapshot **actually contains**. New work-forms extend the manifest, not the
schema version.

| Layer | Epistemic function |
|---|---|
| `bab` | Kesaksian human-realism dan kejadian personal |
| `timer` | Kesaksian cosmic/diegetic dan resonance |
| `codex` | Declared world model |
| `system` | Machine register: boot sequences, OS updates, world-state mutations |
| `void_incident` | Observational anomaly report (reserved; no instances in canon-v1.0) |

**Layer determines source type, not truth.** Admissibility is decided by
Doctrine, per audit. Example: Codex is admissible as *declaration*, but never
sufficient alone to prove *consequence* — which is where
`DECLARED_BUT_UNREAL` lives (see §15).

---

## 6. Source authority

```
canonical | supplemental | draft | fork | external | derived
```

- `canonical` means: *this document is officially part of the corpus.*
  It does **not** mean: *everything it says is embodied in the world.*
  A Codex can be canonical as a document while its claims remain unproven
  as world-state. This distinction is guarded hard.
- Banned field names: `truth_level`, `reliability_score`.
- `derived` requires a derivation object:

```json
{
  "source_authority": "derived",
  "derivation": {
    "type": "compiled_corpus",
    "derived_from": ["bab-00", "bab-01", "..."]
  }
}
```

**Validator rule:** derived artifacts must never enter the primary retrieval
collection.

---

## 7. Temporal model — two axes, framed

A single sequence axis falsifies this corpus. Void Saga separates reading
order from world order, and contains **two diegeses**, not one timeline with
two registers.

### 7.1 `sequence_narrative`

Reader-encounter order. Monotonic integers spaced by 10 (insertion-friendly
during candidate phase), assigned from the canonical reading-order manifest —
never from title numbers.

### 7.2 `diegetic_frame`

```
"bab-world" | "timer-world" | null
```

Bab-world (GUA/LO: kantor → Yogya → Korea) and timer-world (Dayan → The
Void → Era ⛎) are distinct diegeses.

**Validator rule (hard):** `sequence_within_frame` values MUST NOT be
compared across different `diegetic_frame` values. A diegetic Olbers audit is
frame-scoped by definition.

### 7.3 `sequence_within_frame`

Nullable integer. In-world event order **within one frame only**.

> **CONVENTION (ruling 2026-07-15):** `sequence_within_frame` orders the
> **primary narrated events**, not the document's composition moment.
> Composition lives in `composition_relations` (§9.3). Archival documents
> receive `temporal_status: retroactive` plus a `recounts` relation.
> Without this ruling, every archive document is ambiguous.

### 7.4 `diegetic_certainty`

```
exact | approximate | relative | unknown | not_applicable
```

Optional free-text `diegetic_period` (e.g. `"post-dayan-15-years"`). Never
force false precision — `null` + `relative` is an honest state.

---

## 8. `temporal_status`

```
sequential | retroactive | atemporal | recursive | uncertain
```

| Status | Meaning | Canonical exemplar |
|---|---|---|
| `sequential` | Events follow the frame's main trajectory | most Bab & Timer |
| `retroactive` | Appears late in reading order; primary events sit earlier in world order | `timer-02-50` (THE VOID RECORD Δ3), `timer-25-00` (Fragment Mundur) |
| `atemporal` | Not on any linear timeline | all `codex` |
| `recursive` | Actively rewrites the meaning of previously read documents | `system-void-os-v6-6-6` (CONSENT: FORGED) |
| `uncertain` | Temporal position is deliberately unstable | `timer-16-66` (timestamp 16:66 — impossible by design) |

Every enum value has a real inhabitant in canon-v1.0. None is speculative.

---

## 9. Relations — four namespaces, never one flat list

A single `relations[]` looks flexible and loses law. Four namespaces:

### 9.1 `temporal_relations`

```
occurs_before | occurs_after | overlaps | recounts
```

### 9.2 `structural_relations`

```
resonates_with | foreshadows | recontextualizes
```

### 9.3 `composition_relations`

```
composed_during | rewritten_during | deleted_during
```

(Reserved for later versions: `drafted_during`, `restored_during`,
`completed_during`.)

**Why a separate namespace:** `timer-07-00 occurs_during bab-07` is
diegetically false. What is true is: *the textual artifact timer-07-00 was
composed during events narrated in bab-07.* That is a different level of
reality — production causality, not chronology. In this novel, deletion of a
document is a story event (`timer-10-00 deleted_during bab-10` by LO;
`timer-20-00 deleted_during bab-20` by GUA). The schema records the events;
it is not required to resolve the paradox of a deleted document that exists.

### 9.4 `derivation_relations`

```
compiled_from | excerpted_from | supersedes
```

**Relation record shape (all namespaces):**

```json
{
  "relation_type": "composed_during",
  "source_document_id": "timer-07-00",
  "context_document_id": "bab-07",
  "certainty": "explicit",
  "provenance": { "source": "explicit_text", "confidence": 1.0 }
}
```

---

## 10. Resonance mapping

Bab–Timer pairing is formal structure. Normalize once at ingestion; never
derive from filenames at query time.

```json
{ "resonance_group": "00", "resonance_role": "human",  "resonance_pair_id": "timer-00-00" }
{ "resonance_group": "00", "resonance_role": "cosmic", "resonance_pair_id": "bab-00" }
```

Codex and system documents: all three fields `null`. Multi-document
`resonance_scope` is deferred — not forced in v1.

**Note:** resonance pair ≠ composition context. `timer-02-50` pairs with
`bab-02-5` by structure, but was composed during `bab-03` (Phoenix night).
The namespaces exist so this is representable without contradiction.

---

## 11. `evidence_mode`

Candidate textual type — **not** a final judgement. Doctrine may reject or
re-audit any classification.

```
witnessed | declared | reported | archival | reflective | procedural | mixed | unknown
```

### Assignment: null + inherited

Never materialize an unreviewed mode. Distinguish *not yet classified* from
*classified as mixed*:

```json
{
  "evidence_mode": null,
  "inherited_evidence_mode": "mixed",
  "evidence_mode_source": "document_default"
}
```

### Layer defaults (document defaults ONLY — not claims about content)

| Layer | Default | Provenance | Confidence |
|---|---|---|---|
| `bab` | `witnessed` | `filename_rule` | 0.6 |
| `codex` | `declared` | `filename_rule` | 0.8 |
| `system` | `procedural` | `filename_rule` | 0.7 |
| `timer` | `mixed` | `filename_rule` | 0.4 |

Bab routinely contains emails, system logs, files-within-files, Slack
messages, and Timer text being written — `bab → witnessed` is a default, not
a truth. Same for Timer (archive blocks, logs, witnessed scenes in one
document — e.g. `timer-00-00` *is* the content of genesis.txt).

### Resolution order

```
passage override → section mode → document default → unknown
```

Passage-level override is **post-v1, not P0**. Do not let evidence_mode
perfectionism block the sealing ceremony — that is exactly what the
provenance layer exists to absorb.

---

## 12. Provenance

Every derived metadata field carries origin and confidence:

```json
{
  "metadata_provenance": {
    "sequence_narrative": { "source": "canonical_manifest", "confidence": 1.0 },
    "sequence_within_frame": { "source": "human_editor", "confidence": 0.8 },
    "temporal_status": { "source": "human_editor", "confidence": 0.9 }
  }
}
```

Source enum:

```
explicit_text | canonical_manifest | filename_rule | human_editor | model_inference | migration
```

**Rule:** `model_inference` is never silently canon. Provenance is what
allows sealing imperfect data without pretending it is perfect.

---

## 13. Section and chunk schemas

### 13.1 Section

Documents are split into sections before chunking. Section markers
(`00:02 — Genesis Error`) are part of the text's form, not decoration.

```json
{
  "section_id": "bab-00::00-02-genesis-error",
  "document_id": "bab-00",
  "canon_id": "void-saga-canon-v1.0",
  "section_order": 1,
  "section_marker": "00:02",
  "section_title": "Genesis Error",
  "evidence_mode": null,
  "inherited_evidence_mode": "witnessed",
  "evidence_mode_source": "document_default",
  "start_char": 0,
  "end_char": 1850,
  "section_hash": "sha256:..."
}
```

### 13.2 Chunk — dual identity

Text alone is not identity. This corpus repeats ritual text (boot sequences,
log formats, sync-rate lines, sigil blocks) by design.

```
chunk_id = sha256(canon_id + document_id + section_id +
                  chunker_version + chunk_index + start_char + end_char + text)

content_fingerprint = sha256(normalized_text)
```

- `chunk_id` answers: *which chunk, in which snapshot, from which location?*
  It is snapshot-specific and is **not** identity across canons.
- `content_fingerprint` answers: *does the same content appear elsewhere?*

Fingerprint collisions are **signal, not bug**:

```
same fingerprint + different chunk_id + same canon
  → real textual/ritual repetition (evidence of pattern)

same fingerprint + source is a derived compiled document
  → duplicate-artifact flag (independence hazard)
```

Chunk records duplicate retrieval-filter fields from the document (`layer`,
`sequence_narrative`, `diegetic_frame`, `temporal_status`,
`evidence_mode`) — normal denormalization. Source of truth remains the
document manifest.

---

## 14. Citation

A hash is a seal, not a locator. Citations must be verifiable **and**
re-anchorable.

```json
{
  "citation": {
    "canon_id": "void-saga-canon-v1.0",
    "document_id": "bab-07",
    "section_id": "bab-07::07-21",
    "start_char": 1234,
    "end_char": 1456,
    "quote_text": "…full quoted span…",
    "quoted_hash": "sha256:...",
    "retrieval_chunk_id": "…",
    "anchor_status": "exact"
  }
}
```

- `quote_text` is the **full** quote (head-tail only for extreme lengths).
  Storage murah. Ambiguitas mahal.
- `anchor_status` enum: `exact | relocated | modified | ambiguous | orphaned`.

### Re-anchoring procedure (across canon versions)

```
1. Exact-match quote_text in new canon.
2. One hit             → relocated (verify quoted_hash → exact).
3. Multiple hits       → disambiguate via section lineage + neighboring context.
4. Zero hits           → fuzzy match → modified (if close) 
5. Still nothing       → orphaned.
```

**Purpose:** verdict deltas must distinguish *evidence removed* from
*evidence moved* from *evidence rewritten*. Without `anchor_status`, every
canon version bump floods Loop 4 with false verdict changes.

---

## 15. Audit temporal scope (doctrine-facing)

Doctrines must declare their axis explicitly. Three lawful scopes:

```
document_local          — residue within one document
frame_longitudinal      — residue across documents, ordered by
                          sequence_within_frame, single frame only
cross_frame_authorship  — Bab composition context → Timer artifact,
                          via composition_relations (production causality)
```

Plus the atemporal declaration audit:

```
declared in atemporal source (codex)
  → search witnessed residue across bab/timer
  → if none found: FAILED, finding: DECLARED_BUT_UNREAL
```

`DECLARED_BUT_UNREAL` is a **doctrine finding**, not a generic verdict label.
The machine grammar stays stable; the poetic language stays alive:

```json
{ "verdict": "FAILED", "finding": "DECLARED_BUT_UNREAL" }
```

---

## 16. OPEN-SCHEMA registry

Formal, auditable deferrals. Not hacks. Not omissions.

```
OPEN-SCHEMA-001
  System document diegetic frame assignment
  Trigger:     system-opening — Void.OS speaks across frames; assignment
               to bab-world is defensible but not certain.
  Resolution:  handled through nullable frame + provenance confidence
               (human_editor, confidence ≤ 0.5)
  Schema change required: no

OPEN-SCHEMA-002
  In-universe authorship representation
  Trigger:     timer-02-50 — THE VOID RECORD Δ3 has an in-universe author
               (Agnia). v1 has no in_universe_author field.
  Rationale:   the field is half a step into an entity/authorship layer
               that theory has not settled. Representable meanwhile via
               temporal_status: retroactive + evidence_mode: archival +
               recounts relation.
  Resolution:  deferred to entity/authorship layer, schema v1.1
  Schema change required for canon-v1.0: no
```

New strains discovered during authoring join this registry with the next
number. They do not silently mutate the schema.

---

## 17. Sealing ceremony — specified, NOT built

P0 commands (future work; listed here as spec, not as existing tools):

```
void-corpus validate
void-corpus snapshot --version 1.0.0
void-corpus seal canon-v1.0
```

### validate must check

- `document_id` uniqueness; source files exist; hashes valid
- layer ∈ manifest_active_layers; required metadata complete
- `sequence_narrative` collision-free; resonance pairs bijective and mutual
- temporal_status valid; no cross-frame sequence comparisons anywhere
- derived artifacts absent from primary retrieval collection
- **divergence witness check:** diff `Void Saga — Naskah Lengkap.md`
  (EXCLUDED, derived) against the union of its `compiled_from` sources.
  If the compiled manuscript is newer than the source files, sealing the
  sources would seal stale text. This check runs BEFORE any seal.
- counts computed and written by validator only

### snapshot

Writes `canon/candidates/canon-v1.0.json` (candidate manifest).

### seal

Computes corpus hash → status `sealed` → timestamp → forbids in-place
mutation → `git tag canon-v1.0`.

After that, "Void Saga selesai" stops being DECLARED_BUT_UNREAL. The claim
acquires technical residue.

---

## Verdict

```
CORPUS_SCHEMA_V1        Status: FROZEN
CANON_MANIFEST_DRAFT    Status: AUTHORIZED FOR AUTHORING
CANON_V1.0              Status: NOT YET SEALED
```

*Frozen 2026-07-15. Amendments require a new schema_version and a decision
log in `research/`. The Constitution of Void Inquiry governs how claims are
examined; this schema governs what the world is made of when they are.*
