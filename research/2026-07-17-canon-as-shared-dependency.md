# 2026-07-17 — Canon as Shared Dependency (Node Reader Spike)

## Trigger

Architecture spike (commit `abe65b1`): buktikan apakah `canon-v1.0.json` bisa jadi
source of truth untuk node-aware reader. Scope: 2 node (`bab-00`, `timer-00-00`),
no fork changes, no canon changes.

## Result — PASSED

```
UI  →  Experience Registry (mvp/node-registry.json)  →  Canon v1.0  →  Markdown
```

- Node identity (document_id, layer, pair_document_id, sequence_narrative,
  source_authority, source_path) dibaca runtime dari canon. UI tidak mengarang
  identitas sendiri. Sebelum spike, identitas node bahkan tidak ada — UI hardcoded
  ke satu filename.
- Navigasi bab-00 → timer-00-00 di-derive dari `pair_document_id` +
  `sequence_narrative`. TIDAK bergantung pada relasi `composed_during`
  (diverifikasi: zero referensi di implementation).
- Renderer abstraction (BabRenderer / TimerRenderer) menggantikan `_process_bab00`
  — aplikasi mengenal jenis dokumen, bukan satu file.
- Boundary test paling penting: spike TIDAK meminta field baru di canon /
  manifest / validator. Yang kurang hanya `display_title`, `button_text`,
  `render_mode`, `fork_enabled` — semuanya domain UI, ditampung di experience
  registry. Pemisahan identity/experience terbukti natural, bukan dipaksakan.

## Decision

1. **Canon dipromosikan dari "output M1" menjadi shared dependency.**
   Dependency graph target:

   ```
   Void Saga (Authoring) → Canon v1.x → { Node Reader, Evidence Engine, (Fork Engine) }
   ```

2. **M2 di-reframe**: dari "Canonical Ingestion / bikin importer" menjadi
   membangun cara subsystem mengonsumsi canon. Nama kandidat Jali:
   "Canon Consumer Platform".

## Guardrails (contra discipline)

- **"Shared dependency" = hypothesis dengan satu validated consumer, bukan
  platform doctrine.** Spike ini membuktikan canon BISA dikonsumsi oleh satu
  consumer di luar dirinya — belum membuktikan canon berfungsi sebagai dependency
  bersama. Consumer kedua (M2) yang menentukan apakah istilahnya dipromosikan
  atau di-downgrade.
- **Consumer count hari ini = 1** (Node Reader). Evidence Engine
  (`engine_v2.py`, `.runtime.json`) hari ini TIDAK membaca canon — zero coupling,
  diverifikasi 2026-07-17. Klaim "Evidence Engine adalah consumer pertama"
  adalah rencana, bukan fakta.
- **Kata "platform" belum earned.** Sama polanya dengan "research program" /
  "emergence detection engine" yang di-downgrade di Fase 0: label naik sebelum
  evidence. Rule: "platform" boleh dipakai setelah ≥2 consumer independen jalan.
- **M2 exit criterion (satu, konkret):** Evidence Engine menjadi consumer canon
  kedua — invariant/runtime citations resolve ke canon `document_id` +
  `source_hash`, bukan path markdown mentah. Search / Timeline / Glossary /
  Character browser BUKAN deliverable M2 (bentuknya sama dengan contra #4:
  premature expansion).

## Formal debt

- **Legacy runtime IDs must eventually migrate to canonical document_id.**
  Fork records / interview / checker masih pakai `bab00`; canon pakai `bab-00`.
  Sengaja tidak disentuh di spike (ripple besar). Wajib dibayar sebelum Fork
  Engine jadi consumer canon.

## Status

- Spike committed: `abe65b1` (3 file: node-registry, fork-ui, index.html).
- Canon / manifest / validator / prose: untouched.
- Full node reader (65 nodes): NOT STARTED — deliberately.
