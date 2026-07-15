# ROADMAP — Void Saga Ecosystem

```
Authored:    2026-07-15
Supersedes:  scattered status across CLAUDE.md, research/, pm-grounding-agent.json
North Star:  Orang bisa BACA, bisa FORK, bisa CHAT sama novel ini.
Outer loop:  tulis saga → segel canon → biarkan manusia lain masuk →
             lihat apakah sistem menahan dunia yang bukan hanya ditulis Jali
```

---

## Peta besar — empat lapis

```
Void Saga Ecosystem
│
├── Canon Corpus          the novel (65 dokumen) — sumber segalanya
├── Evidence Engine       rag-project — read-side: klaim → evidence → verdict
├── Invariant Engine      VOID_SAGA_UNIVERSE — write-side: fork → hukum → harga
└── Experience Layer      belum ada — tempat BACA / CHAT / FORK hidup
```

Tiga kemampuan user dipetakan begini:

| Kemampuan | Ditenagai oleh | Status hari ini |
|---|---|---|
| **BACA** | Novel terbit (KPG/indie) + companion | Draft complete, belum sealed, belum terbit |
| **CHAT** | Evidence Engine + sealed corpus + Goetia UI | Engine jadi, corpus baru 1 bab, UI belum ada |
| **FORK** | Invariant Engine + fork checker + interview UX | MVP jadi (Bab 00, CLI), belum bisa dipakai non-teknis |

---

## STATUS — yang sudah selesai (per 2026-07-15)

### Naskah
- ✅ Draft lengkap: 29 Bab + 29 Timer + 5 Codex + Opening + Void.OS Update (65 dokumen)
- ✅ Continuity pass (2026-06-27)

### Invariant Engine (write-side)
- ✅ Engine v2 + compiler (safe mode, hard block gate, live Claude generation proven)
- ✅ 5 runtime characters, schema V2.1
- ✅ **Bab 00 Fork MVP**: 7 laws, 3 fork points, 3 demo forks, CLI `check-fork`
  (PASS / PRICE_REQUIRED / BLOCKED / VALID_FORK)

### Evidence Engine (rag-project)
- ✅ Constitutional pipeline: Claim → Jurisdiction → Doctrine → Investigation →
  Evidence → Verdict (traceable)
- ✅ Doctrine Olbers (1 dari Goetia); Echo & Saturn masih Law ringan
- ✅ 3 Lens (keyword/embedding/hybrid), Mind router (fast/strong, provider-agnostic)
- ✅ Tripwire tests (off-domain, independence, capable-of-support)
- ⚠️ Corpus baru Bab 00 doang

### Keputusan arsitektur (sesi audit 2026-07-14 → 15)
- ✅ Identitas: Void Engine = evidence layer, BUKAN research program kedua
- ✅ Verdict **envelope** dishare (VALID/INVALID/UNRESOLVED); vocabulary final TIDAK
- ✅ Dua temporal axis + diegetic frame (bab-world ≠ timer-world)
- ✅ Empat namespace relasi (temporal / structural / composition / derivation)
- ✅ `composed_during`: 13 relasi komposisi Bab→Timer dari continuity log
- ✅ **CORPUS_SCHEMA_V1.md — FROZEN** (diuji terhadap 14 kasus tersulit; 2 strain
  → OPEN-SCHEMA-001/002, nol hack)
- ✅ **CANON_MANIFEST_DRAFT.md** — 65 included, 3 excluded, whitelist scope
- ✅ Keputusan orphan terkunci (opening & Void.OS update masuk; Sigil_OS,
  Cosmology Paper, Naskah Lengkap keluar — Naskah Lengkap = divergence witness)

---

## MILESTONES — urutan tidak bisa ditawar

### M1 — SEGEL DUNIA → `canon-v1.0` 🔒
*Gate untuk semua yang lain. Ini "Fase 1" dalam bentuk teknis.*

1. Commit identity declaration ke README rag-project
2. Human editor pass: `sequence_within_frame` timer-world + review
   `evidence_mode` section Timer (default `mixed` conf 0.4 = terlemah)
3. Bangun `void-corpus validate` — termasuk **divergence witness check**
   (diff Naskah Lengkap vs sumber; kalau kompilasi lebih baru, sumber basi)
4. `snapshot` → `seal` → `git tag canon-v1.0`

**Deliverable:** corpus hash. Klaim "Void Saga selesai" berhenti jadi
DECLARED_BUT_UNREAL.

### M2 — ENGINE MEMBACA SELURUH NOVEL
*Prasyarat CHAT. Depends: M1.*

1. Ingestion per CORPUS_SCHEMA_V1 (section-aware chunking, dual chunk identity)
2. Fix bahasa: multilingual embedding + exact-match channel tetap hidup
   (genesis ≠ Genesis Error ≠ genesis.txt)
3. Tripwire suite lolos di full corpus + battery klaim canon (continuity log
   sebagai regression suite = Continuity CI)
4. Audit loop single-pass stabil (BELUM agentic iteration)

**Deliverable:** CLI tanya-novel dengan verdict bersitasi lintas 65 dokumen.
Dogfood internal.

### M3 — CHAT: "Tanya Void Saga" (reader alpha)
*Depends: M2. Sekaligus funnel Fase 3.*

1. UI invocation: pembaca **memilih Goetia** (Olbers/Saturn/Echo), bukan
   kolom "ask anything" — "Pilih hukum yang berani lo pakai untuk membaca"
2. Output = verdict card (doctrine, claim, verdict, evidence, unresolved),
   bukan jawaban chatbot biasa
3. Reader ledger: persist AuditInstance per pembaca (Personal Akashic Record;
   encounter state ≠ truth state)
4. Alpha 5–10 pembaca

**Deliverable:** web interface pertama. Pembaca paling engaged = kandidat
penulis kedua.

### M4 — FORK: penulis kedua
*Depends: M2 + Fork MVP yang sudah ada. = objective 30-hari PM agent.*

1. Conversational fork interview → Fork Record (tanpa lihat JSON)
2. Evidence-backed verdict: Evidence Engine mengaudit klaim pelanggaran
   hukum dengan sitasi — verdict berhenti jadi deklarasi penulis fork
3. Anti-confirmation safeguards baru masuk di sini (immutable investigation
   plan, support + contradiction queries, boleh berhenti INSUFFICIENT)

**Deliverable:** 1 fork PASS/PRICE_REQUIRED dari orang yang bukan Jali,
bukan Claude.

### M5 — BACA: terbit
*Jalur paralel, timeline eksternal (KPG / indie). Tidak menunggu M2–M4;
hanya menunggu M1.*

**Deliverable:** buku + link companion (M3) di halaman belakang.

### M6 — UNIVERSE HIDUP (Loop 4 — north star jangka panjang)

fork diterima → branch corpus → evidence index rebuilt → audit battery rerun
→ **verdict delta**: "Before fork: Claim X SUPPORTED. After: FAILED. New
residue detected." Fork benar-benar mengubah semesta.

---

## GUARDRAILS — yang TIDAK dikerjakan sekarang

- ❌ Doctrine baru (freeze di Olbers sampai M2 beres)
- ❌ Agentic investigation loop sebelum single-pass stabil (M4 baru boleh)
- ❌ Schema v3 / serialisasi karakter sisa / entity layer (OPEN-SCHEMA-002
  menunggu v1.1)
- ❌ Platform/web sebelum genesis + law nyata (urutan: genesis → law →
  first fork → platform)
- ❌ Konstitusi baru. Constitution freeze sampai enforcement map penuh
- ❌ Research program kedua. Void Engine = evidence layer. Titik.

---

## NEXT ACTION (satu, konkret)

**M1 step 1–2:** commit identity declaration ke rag-project README, lalu
human editor pass untuk timer-world sequence. Dua-duanya gak butuh kode baru.
Setelah itu baru validator.

```
CORPUS_SCHEMA_V1        FROZEN
CANON_MANIFEST_DRAFT    AUTHORED
CANON_V1.0              NOT YET SEALED   ← lo di sini
```
