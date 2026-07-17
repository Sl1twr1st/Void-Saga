# 2026-07-17 — Provenance Loss Trace (First M2 Investigation)

## Trigger

Pertanyaan pembuka M2, formulasi Jali: **"Di titik mana citation kehilangan
identitas kanonnya?"** Trace satu citation end-to-end sebelum mendesain apa pun:

```
source document → extractor output → evidence object → runtime citation → rendered verdict
```

Empat cek di setiap boundary: document_id masih ada? source_hash masih ada?
masih bergantung path? ada transform yang membuang provenance?

Rule investigasi: **jangan desain layer baru sebelum ketahuan persis di mana
identitasnya hilang.** Catatan ini findings only — keputusan desain belum diambil.

## Headline — identitas tidak hilang di boundary; identitas tidak pernah masuk

`grep -r "document_id\|source_hash" VOID_SAGA_UNIVERSE/` → **zero hits**
(diverifikasi 2026-07-17). Seluruh sisi engine — extractor, runtime JSON, schema,
constraint engine, compiler, verdict — tidak mengandung satu pun referensi ke
identitas canon. Konsisten dengan temuan spike ([[2026-07-17-canon-as-shared-dependency]]):
zero coupling. Runtimes ditulis Juni; canon di-seal 2026-07-15. Pipeline lahir
sebelum canon ada.

Konsekuensi: "provenance loss boundary" bukan kebocoran yang bisa ditambal —
ini **edge yang belum pernah dibangun**. Tapi di dalam pipeline sendiri ada dua
titik kehilangan provenance internal yang genuin (lihat B2 dan B3).

## Trace per boundary

Citation yang di-trace: (a) hard-block path — Zero forbidden_behavior
(demo `BLOCKED_zero_emotional.md`), (b) rich path — NiuNiu
`core_wound.origin_event.timer_reference = "Timer 0200 / Timer 0250"`.

### B0 — Canon record (`canon-v1.0.json`)

Identitas lengkap: `document_id` (`timer-02-00`), `source_hash`, `document_hash`,
`source_path`, `pair_document_id`, sequence. Path hadir sebagai metadata di
samping id+hash, bukan sebagai key. **Satu-satunya stage di mana keempat cek lolos.**

### B1 — Source → extractor output (`apps/extractor/extract_scene.py`)

- Extractor **tidak pernah membaca canon** — tidak ada import, tidak ada lookup.
- Identitas scenario lahir dari **filename**: `scenario_id = slug(Path(md_filename).stem)`
  (`extract_scene.py:545-549`). Path-based identity sejak lahir.
- Report membawa `filename` + `filepath` absolut (`extract_scene.py:707-708`).
- Transform pembuang provenance: prosa → summary 500 karakter
  (`extract_scene.py:748`); nama → runtime_id via `character_registry.json`.
  Kalimat mana menghasilkan match mana: tidak tercatat.
- document_id ❌ · source_hash ❌ · path-dependent ✅ · provenance-dropping ✅

### B2 — Evidence object / runtime citation (`.runtime.json` + `RUNTIME_SCHEMA_V2.1.json`)

Sensus semua string bersifat sitasi (field `evidence`, `source`, `timer_reference`,
`world_dna_ref`, `origin`, `canon_baseline`) di 8 runtime JSON (5 committed +
GUA/LO/Aisya draft): **122 string**, terbagi empat kelas:

| Kelas | n | Contoh | Resolvable ke canon? |
|---|---|---|---|
| Label informal `Timer NNNN` / `Bab NN` | 43 | `"Timer 0200 / Timer 0250"` | Parseable, tapi lewat **skema penamaan ketiga** — bukan document_id (`timer-02-00`), bukan filename. Mapping-nya hari ini hanya ada di kepala manusia. |
| Fuzzy / range | 10 | `"Timer 0100+"`, `"Across 25 Timers"` | Tidak deterministik. |
| Path-based `.md` | 28 | `world-dna/ZERO_ONTOLOGY.md §4`, `NODE_PROTOCOL.md`, `NiuNiu.runtime.md §6` | **Sebagian besar menunjuk ke luar canon.** Canon = 65 dok layer bab/timer/codex/system; world-dna & protocols bukan canon documents. |
| Prosa murni tanpa locator | 41 | `"Years playing in Band 8"` | Tidak resolvable. |

- Schema melegalkan semuanya: `"evidence": {"type": "string"}`,
  `"source": {"type": "string"}` (`RUNTIME_SCHEMA_V2.1.json:167,258,457,665`).
  Citation tanpa identitas bukan pelanggaran schema — schema-nya memang tidak
  punya konsep identitas.
- **Temuan paling tajam: `forbidden_behaviors` — driver HARD BLOCK — tidak punya
  field sitasi sama sekali.** 42 entri di 8 runtime, semuanya hanya
  `behavior/exception/penalty/tag`. Tag `[E]` MENGKLAIM ada evidence di canon
  tapi tidak menunjuk apa pun. Enforcement terkuat, provenance terlemah.
- document_id ❌ · source_hash ❌ · path-dependent sebagian (28/122) ·
  provenance tidak dibuang di sini — **tidak pernah ada**.

### B3 — Runtime citation → violation object (`apps/engine/lib/constraints.py:402-412`)

Violation membawa: `constraint_type, runtime_id, behavior, exception_checked,
penalty, match_reason, tag, severity`. Field sitasi free-text yang ada di section
lain (`evidence`, `source`) **tidak di-copy** ke violation. Violation menyitir
*runtime*, bukan *canon*.

**Ini provenance loss internal yang sesungguhnya:** bahkan sitasi informal
"Timer 0200" pun gugur di sini. Apapun perbaikan di B2, kalau B3 tidak
meneruskannya, verdict tetap buta.

- document_id ❌ · source_hash ❌ · path ❌ (runtime_id only) · provenance-dropping ✅

### B4 — Violation → rendered verdict (`apps/compiler/compiler.py` + demo)

Verdict BLOCKED (`demo/BLOCKED_zero_emotional.md:53-58`): reason string +
teks behavior + canon score. Teks behavior dipotong `[:120]`/`[:150]`
(`compiler.py:150,489,496,503`). Rantai provenance berakhir di teks constraint
runtime. Pembaca verdict tidak bisa menelusuri ke prosa mana pun.

- document_id ❌ · source_hash ❌ · path ❌ · transform lossy ✅ (truncation)

## Empat tes M2 vs kondisi hari ini

| Tes | Hari ini |
|---|---|
| 1. Rename markdown path → citation tetap resolve | Gagal trivially — tidak ada yang resolve. |
| 2. Ubah source_hash → citation ditolak stale | Mustahil dites — hash tidak ada di mana pun di sisi engine. |
| 3. document_id tak dikenal → hard failure | N/A — tidak ada document_id. |
| 4. Canon tidak tersedia → consumer gagal eksplisit | **Kebalikannya yang terjadi: engine sukses penuh tanpa canon.** Ini bukti terkuat Evidence Engine belum jadi consumer — dia tidak akan menyadari kalau canon dihapus. |

## Implikasi (fakta, bukan desain)

1. Resolver M2 apa pun menghadapi **empat kelas input** (43 label / 10 fuzzy /
   28 path / 41 prosa), bukan satu. 100% resolusi tidak mungkin tanpa menulis
   ulang sitasi; angka coverage harus dilaporkan per kelas, bukan agregat.
2. **28 sitasi path-based mayoritas menunjuk dokumen non-canon** (world-dna,
   protocols, runtime.md). M2 = zero canon changes, jadi kelas ini hanya bisa:
   out of scope, atau di-flag `unresolvable-by-design`. Keputusan milik Jali.
3. **Tension terbuka:** exit criterion M2 ("citations resolve ke document_id +
   source_hash") vs aturan berdiri "Do NOT change schema" (CLAUDE.md, menunggu
   OPEN_QUESTIONS). Sitasi kanonik butuh tempat tinggal: di dalam runtime
   (= schema change) atau di luarnya (= artefak mapping milik resolver).
   Dua-duanya punya harga. **Belum diputuskan — sengaja.**
4. Perbaikan di B2 saja tidak cukup — B3 membuang apa pun yang B2 bawa.
   Definisi "consumer kedua" minimal menyentuh dua boundary.

## Status

- Trace selesai. Zero file engine/canon diubah — investigasi read-only.
- Keputusan desain resolver / tempat tinggal citation identity: **NOT TAKEN.**
