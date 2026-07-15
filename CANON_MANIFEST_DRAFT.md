# CANON_MANIFEST_DRAFT — void-saga-canon-v1.0

```
Status:         DRAFT — AUTHORIZED FOR AUTHORING. NOT SEALED.
Schema:         CORPUS_SCHEMA_V1 (FROZEN, 1.0.0)
Authored:       2026-07-15
Sealing:        only via void-corpus validate → snapshot → seal (not yet built)
```

This document is a **decision artifact**. It records include/exclude
decisions, sequence assignments, and relations. It is not the canon. The
canon exists when `corpus_hash` exists.

---

## 1. Scope declaration — whitelist, not folder scan

Corpus candidates are **only** the files enumerated in this manifest.
Discovery is manifest-driven. Folder scanning never adds candidates — the
Void Saga folder is also a working repo (`mvp/`, `research/`, `contra/`,
reports, agent configs), and none of that is corpus.

Three statuses, kept hard apart:

```
INCLUDED       — canonical corpus document
EXCLUDED       — registered candidate, rejected with recorded reason
OUT_OF_SCOPE   — never a candidate; not registered
```

### Expected counts (validator output confirms; this table does not decide)

| Count | Expected |
|---|---|
| included | 65 (29 bab + 29 timer + 5 codex + 2 system) |
| excluded | 3 |
| out_of_scope | everything else |

### OUT_OF_SCOPE patterns (non-candidates by definition)

```
CLAUDE*.md, AGENTS*.md, README.md, QUICKSTART.md, ENTRY_CONVENTIONS.md,
*_REPORT.md, CONTINUITY_PASS_*.md, pm-grounding-agent.json,
CORPUS_SCHEMA_V1.md, CANON_MANIFEST_DRAFT.md, logo_*.png,
mvp/, research/, contra/, docs/, dogfood/, drafts/, experiments/,
scripts/, writing/, VOID_SAGA_UNIVERSE/
```

---

## 2. Orphan decisions — LOCKED 2026-07-15

| File | Decision | Layer | Authority | Reason |
|---|---|---|---|---|
| `opening.md` | **INCLUDE** | `system` | `canonical` | Diegetic constitutional entry point: boot sequence determines consent, installation, reader position vs Void.OS |
| `Void.OS v6.6.6 Update.md` | **INCLUDE** | `system` | `canonical` | World-state mutation: CONSENT: FORGED rewrites interpretation of the entire installation. `recontextualizes → system-opening` |
| `Sigil_OS.md` | **EXCLUDE** | — | `supplemental` | Design-language reference; not canon-v1 narrative evidence. Revisit if sigil system proves explicitly diegetic |
| `THE VOID COSMOLOGY PAPER.md` | **EXCLUDE** | — | `supplemental` | Authorial explanatory model. If canonical, the engine could "prove" canon from outside the story — that kills Olbers. Admissible only under a future authorial-world-model jurisdiction |
| `Void Saga — Naskah Lengkap.md` | **EXCLUDE (hard)** | — | `derived` | See §2.1 |

### 2.1 Naskah Lengkap — dual role

```
Corpus status:   EXCLUDED
Pre-seal role:   DIVERGENCE WITNESS
```

```json
{
  "include": false,
  "source_authority": "derived",
  "derivation": {
    "type": "compiled_corpus",
    "derived_from": ["all included bab/timer/codex/system documents"]
  },
  "exclusion_reason": "compiled duplicate of canonical source documents; ingestion would duplicate passages and corrupt evidence independence"
}
```

It never enters the evidence index — ingesting it would make the
independence audit count the same witness twice. But it is **mandatory
reading for the validator before seal**: diff compiled text against the
union of sources. If the compiled manuscript is newer than the chapter
files, the sources are stale and sealing them would seal the wrong text.
The poison file works exactly once, as a witness, then retires.

---

## 3. Convention rulings (bind every row below)

1. `sequence_within_frame` orders **primary narrated events**, not
   composition moments. Composition lives in `composition_relations`.
2. `sequence_within_frame` is never compared across `diegetic_frame` values.
3. All counts are validator output.
4. Diegetic sequence values are **not** filled by model inference. Rows
   marked `TBD` await a `human_editor` pass with provenance recorded.
   Unfilled is an honest state; fabricated is not.
5. `sequence_narrative` follows the canonical reading order (Opening → Bab
   00 → Timer 0000 → interleaved → Bab 25 → Timer 2500 → Codex Tanah →
   Codex The Void), spaced by 10.

---

## 4. Tested rows — the 14 cases that proved the schema

Schema freeze was conditional on these being representable without hacks.
Result: 12 clean passes, 2 strains resolved via the OPEN-SCHEMA registry
(001, 002 — see CORPUS_SCHEMA_V1 §16). Zero schema changes required.

| # | document_id | layer | seq_narr | frame | temporal_status | Key relations & findings |
|---|---|---|---|---|---|---|
| 1 | `system-opening` | system | 10 | bab-world (conf 0.5) | sequential | Target of `recontextualizes` from #2. **OPEN-SCHEMA-001**: frame assignment debatable — absorbed by provenance, not schema change |
| 2 | `system-void-os-v6-6-6` | system | 450 | null | **recursive** | `recontextualizes → system-opening`. Exemplar of `recursive`: CONSENT FORGED rewrites all prior meaning |
| 3 | `naskah-lengkap` | — | — | — | — | EXCLUDED/derived; `compiled_from` all; divergence witness (§2.1) |
| 4 | `codex-udara` | codex | 130 | null | atemporal | Sits **between** bab-04 and timer-04-00 — codex interrupts a resonance pair. Proves sequence and resonance are independent structures |
| 5 | `bab-00` | bab | 20 | bab-world | sequential | Composition context for #6 |
| 6 | `timer-00-00` | timer | 30 | timer-world (event pos: 0, cosmogony) | sequential | `composed_during → bab-00`. Dual identity: corpus document AND in-world artifact (genesis.txt). Held by composition relation + archival/mixed evidence_mode |
| 7 | `bab-02-5` | bab | 80 | bab-world | sequential | Decimal label absorbed by integer spacing. Filename uses dash (`Bab 02-5`) — identity from manifest, not filename |
| 8 | `timer-02-50` | timer | 90 | timer-world | **retroactive** | THE VOID RECORD Δ3. `recounts` → origin era; `composed_during → bab-03` (Phoenix night — NOT its pair bab-02-5). **OPEN-SCHEMA-002**: in-universe author (Agnia) deferred to v1.1 |
| 9 | `bab-16-6` | bab | 430 | bab-world | sequential | `resonates_with → timer-16-66`. Interval, one page |
| 10 | `timer-16-66` | timer | 440 | timer-world | **uncertain** | Exemplar of `uncertain`: timestamp 16:66 impossible by design. `diegetic_certainty: relative` |
| 11 | `timer-10-00` | timer | 260 | timer-world | sequential | `composed_during → bab-10`, `deleted_during → bab-10` (LO). Document deleted in-story yet present in corpus — schema records the events, manifest records existence, and is not forced to adjudicate the paradox |
| 12 | `timer-07-00` | timer | 200 | timer-world | sequential | `composed_during → bab-07`. Exemplar for future cross_frame_authorship audit: "kita capek pelan-pelan" vs 20 years passing outside The Void |
| 13 | `codex-the-void` | codex | 650 | null | atemporal | End of reading order. Same pattern as #4 |
| 14 | `timer-25-00` | timer | 630 | timer-world (event pos: earliest — pre timer-01-00) | **retroactive** | Fragment Mundur: diegetically first, narratively last. The document that would make a one-axis schema lie hardest |

---

## 5. Full document register — INCLUDED (65)

Defaults unless a row notes otherwise: `source_authority: canonical`,
`work_id: menatap-akhir`, `language: [id, en]`, bab → frame `bab-world` /
sequential, timer → frame `timer-world` / sequential, codex → frame null /
atemporal, `sequence_within_frame: TBD (human_editor)`.

Resonance is bijective: every bab pairs with exactly one timer (29 ↔ 29).

### 5.1 system (2)

| seq | document_id | temporal_status | Relations / notes |
|---|---|---|---|
| 10 | `system-opening` | sequential | No resonance pair. OPEN-SCHEMA-001 |
| 450 | `system-void-os-v6-6-6` | recursive | `recontextualizes → system-opening`. No pair |

### 5.2 bab (29) ↔ timer (29), interleaved reading order

Composition relations sourced from the continuity log (`explicit_text`,
confidence 1.0). Timers without a recorded composition context have none —
absence is recorded honestly, not inferred.

| seq | document_id | pair | Composition / status notes |
|---|---|---|---|
| 20 | `bab-00` | `timer-00-00` | |
| 30 | `timer-00-00` | `bab-00` | `composed_during → bab-00` (genesis.txt) |
| 40 | `bab-01` | `timer-01-00` | |
| 50 | `timer-01-00` | `bab-01` | |
| 60 | `bab-02` | `timer-02-00` | |
| 70 | `timer-02-00` | `bab-02` | |
| 80 | `bab-02-5` | `timer-02-50` | filename: `Bab 02-5` (dash) |
| 90 | `timer-02-50` | `bab-02-5` | retroactive; `composed_during → bab-03`; OPEN-SCHEMA-002 |
| 100 | `bab-03` | `timer-03-00` | |
| 110 | `timer-03-00` | `bab-03` | `composed_during → bab-03` (Phoenix night, with timer-02-50) |
| 120 | `bab-04` | `timer-04-00` | |
| 130 | `codex-udara` | — | atemporal; interrupts the 04 pair |
| 140 | `timer-04-00` | `bab-04` | |
| 150 | `bab-05` | `timer-05-00` | |
| 160 | `timer-05-00` | `bab-05` | `composed_during → bab-05` (post-dinner) |
| 170 | `bab-06` | `timer-06-00` | |
| 180 | `timer-06-00` | `bab-06` | |
| 190 | `bab-07` | `timer-07-00` | |
| 200 | `timer-07-00` | `bab-07` | `composed_during → bab-07` (long distance) |
| 210 | `bab-08` | `timer-08-00` | |
| 220 | `timer-08-00` | `bab-08` | |
| 230 | `bab-09` | `timer-09-00` | POV shift to LO |
| 240 | `timer-09-00` | `bab-09` | |
| 250 | `bab-10` | `timer-10-00` | |
| 260 | `timer-10-00` | `bab-10` | `composed_during → bab-10` (Narita); `deleted_during → bab-10` (LO) |
| 270 | `bab-11` | `timer-11-00` | |
| 280 | `timer-11-00` | `bab-11` | `composed_during → bab-11` (Liminal Labs, first night) |
| 290 | `codex-air` | — | atemporal |
| 300 | `codex-api` | — | atemporal |
| 310 | `bab-12` | `timer-12-00` | |
| 320 | `timer-12-00` | `bab-12` | |
| 330 | `bab-13` | `timer-13-00` | |
| 340 | `timer-13-00` | `bab-13` | `composed_during → bab-13` (night before LO leaves) |
| 350 | `bab-14` | `timer-14-00` | |
| 360 | `timer-14-00` | `bab-14` | `composed_during → bab-14` (Jakarta) |
| 370 | `bab-15` | `timer-15-00` | |
| 380 | `timer-15-00` | `bab-15` | |
| 390 | `bab-16` | `timer-16-00` | |
| 400 | `timer-16-00` | `bab-16` | `composed_during → bab-16` (panic attack night) |
| 410 | `bab-16-5` | `timer-16-50` | filename: `Bab 16.5` (dot) |
| 420 | `timer-16-50` | `bab-16-5` | `composed_during → bab-16-5` (night before wedding) |
| 430 | `bab-16-6` | `timer-16-66` | Interval |
| 440 | `timer-16-66` | `bab-16-6` | **uncertain**; timestamp 16:66 |
| — | *(seq 450 = `system-void-os-v6-6-6`, see §5.1)* | | |
| 460 | `bab-17` | `timer-17-00` | |
| 470 | `timer-17-00` | `bab-17` | `composed_during → bab-17` (Yogya, pulpen) |
| 480 | `bab-18` | `timer-18-00` | |
| 490 | `timer-18-00` | `bab-18` | `composed_during → bab-18` (Bandung) |
| 500 | `bab-19` | `timer-19-00` | |
| 510 | `timer-19-00` | `bab-19` | |
| 520 | `bab-20` | `timer-20-00` | |
| 530 | `timer-20-00` | `bab-20` | `deleted_during → bab-20` (GUA). Composition context unrecorded — left absent, not inferred |
| 540 | `bab-21` | `timer-21-00` | |
| 550 | `timer-21-00` | `bab-21` | |
| 560 | `bab-22` | `timer-22-00` | |
| 570 | `timer-22-00` | `bab-22` | |
| 580 | `bab-23` | `timer-23-00` | |
| 590 | `timer-23-00` | `bab-23` | |
| 600 | `bab-24` | `timer-24-00` | VOID SAGA — COMPLETE (in-story) |
| 610 | `timer-24-00` | `bab-24` | |
| 620 | `bab-25` | `timer-25-00` | 10 years later |
| 630 | `timer-25-00` | `bab-25` | **retroactive** — Fragment Mundur; event position earliest in timer-world |

### 5.3 codex (5)

| seq | document_id | Placement note |
|---|---|---|
| 130 | `codex-udara` | after bab-04 |
| 290 | `codex-air` | after timer-11-00 |
| 300 | `codex-api` | after codex-air |
| 640 | `codex-tanah` | after timer-25-00 |
| 650 | `codex-the-void` | end of corpus |

All: `layer: codex`, `temporal_status: atemporal`, `diegetic_frame: null`,
`diegetic_certainty: not_applicable`, no resonance fields.

---

## 6. EXCLUDED register (3)

| document_id | source_authority | exclusion_reason |
|---|---|---|
| `sigil-os` | supplemental | design-language reference; not part of canon-v1 narrative evidence |
| `void-cosmology-paper` | supplemental | authorial explanatory model; excluded from primary canon evidence to protect Olbers from outside-the-story proof |
| `naskah-lengkap` | derived | compiled duplicate; would corrupt evidence independence. Pre-seal role: divergence witness (§2.1) |

Excluded ≠ deleted. All three remain registered, citable under future
special jurisdictions, and outside the evidence index.

---

## 7. What remains before seal

1. **Human editor pass** — `sequence_within_frame` + `diegetic_certainty`
   for timer-world (anchors exist: timer-00-00 cosmogony first,
   timer-25-00 events pre-timer-01-00, timer-02-50 recounts origin era).
   Provenance: `human_editor`.
2. **Evidence-mode review** — timer sections at minimum (default `mixed`,
   confidence 0.4 is the weakest default in the corpus).
3. **Build `void-corpus validate`** — including the Naskah Lengkap
   divergence witness check (must run before any seal).
4. **Snapshot** → `canon/candidates/canon-v1.0.json`.
5. **Seal** → corpus hash, `git tag canon-v1.0`.
6. rag-project side (separate repo): commit identity declaration to README;
   ingest only from sealed snapshots.

```
CANON_V1.0    Status: NOT YET SEALED
```

*Until the corpus hash exists, "Void Saga selesai" remains
DECLARED_BUT_UNREAL — by this project's own law.*
