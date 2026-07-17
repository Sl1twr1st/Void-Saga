# 2026-07-17 — Citation Residence: Decision Matrix (A vs B)

> Status: **SEALED — Verdict A (2026-07-17). Implementation strategy: OPEN.**

## Contradiction yang memicu

```
M2 requires canonical citation residence
vs
current rule forbids schema change  (CLAUDE.md, menunggu OPEN_QUESTIONS)
```

Kontradiksi ini nyata dan tercatat — tidak diselesaikan diam-diam di research note.
Menyelesaikannya = keputusan eksplisit, karena salah satu opsi adalah exception
terhadap standing rule.

## Framing (koreksi model mental dari [[2026-07-17-provenance-loss-trace]])

Bukan *repair provenance* — canon identity tidak pernah jadi input pipeline.
M2 = **introduce provenance contract**. Tiga konsekuensi arsitektural:

1. **B1** harus menerima canonical identity (extractor/authoring tahu canon ada)
2. **B2** harus punya bentuk citation yang terstruktur
3. **B3** tidak boleh mereduksi citation kembali jadi teks kosong

## Premis bersama (fakta, berlaku untuk kedua opsi)

- Canon **sealed** → locator (line_range dsb.) stabil by construction terhadap
  canon v1.0; staleness hanya terjadi lewat canon version bump. Drift risk kedua
  opsi dibatasi oleh imutabilitas canon.
- **B3 (`constraints.py:402-412`) harus diubah di kedua opsi.** Tidak ada residence
  choice yang menyelamatkan citation kalau violation constructor membuangnya.
- Input eksisting = 4 kelas (43 label / 10 fuzzy / 28 path non-canon / 41 prosa).
  Coverage wajib dilaporkan per kelas, opsi mana pun.

## Opsi

**A — Canonical citation embedded in runtime schema** (v2.2: `evidence`/`source`
naik dari string ke objek `{document_id, source_hash, locator}`;
`forbidden_behaviors` dapat field citation untuk pertama kalinya).

**B — External resolver sidecar** (runtime & schema untouched; artefak mapping
milik resolver: key = lokasi citation di runtime → value = identitas canon).

## Matrix

| Kriteria | A: embedded in schema | B: resolver sidecar |
|---|---|---|
| **Authority** | Satu artefak: claim + provenance serumah. Runtime declares, canon verifies. Jelas siapa bicara. | Terbelah: runtime memegang claim, sidecar memegang *makna* claim. Dua sumber kebenaran untuk satu klaim — konflik di antaranya butuh aturan preseden sendiri. |
| **Drift risk** | Drift **terdeteksi** di load time (schema validation + hash check). Risiko sisa: dialek ganda string\|object selama koexistensi; double migration kalau schema v3 mengubah root abstraction. | Drift **struktural & silent**: edit runtime tidak menyentuh sidecar. Key sidecar berbasis posisi/path JSON (`canon_gravity[0]`) = **path-based identity lahir ulang di layer baru** — penyakit yang M2 mau sembuhkan, pindah rumah. Validator sidecar sendiri wajib ada = membangun ulang schema di luar schema. |
| **Migration cost** | **Tinggi di muka**: 122 string + 42 fb tanpa field; loader/lint/evidence_report ikut berubah; melanggar standing rule → butuh keputusan eksplisit. | **Rendah di muka**: zero schema change, zero runtime edit, inkremental per kelas (43 label dulu). Biaya pindah ke belakang: maintenance artefak bayangan. |
| **B3 survivability** | Tidak otomatis tapi **mekanis**: violation constructor tinggal meng-copy objek citation yang memang ada di constraint. Bisa dites langsung. | **Lemah**: engine tidak kenal sidecar (by design). Dua penempatan: (i) post-hoc annotator di luar engine — join via runtime_id + behavior text yang di beberapa jalur sudah dipotong `[:150]` → join on truncated text, fragile by construction; (ii) engine load sidecar — survivable, tapi engine kini bergantung dua artefak dan "sidecar tanpa coupling" gugur. |

## Observasi dari matrix (bukan verdict)

1. **Tidak ada opsi menang 4–0.** A menang authority + B3; B menang migration
   cost; drift: A = detectable drift, B = silent structural drift.
2. **Tes #4 M2 adalah diskriminator paling tajam.** Di opsi B penempatan (i),
   yang membaca canon adalah *resolver*, bukan Evidence Engine — engine tetap
   sukses penuh tanpa canon. Pertanyaan untuk Jali: kalau begitu, siapa
   sebenarnya consumer kedua? Exit criterion berbunyi "**Evidence Engine**
   membaca canon", bukan "ada komponen yang membaca canon".
3. **Tes #1 M2 (rename → tetap resolve)** gagal ulang di opsi B pada layer baru:
   reorder array di runtime = sidecar key menunjuk constraint yang salah,
   diam-diam.
4. **Pre-registered prediction Jali** (dicatat sebelum matrix dibuat): *"sidecar
   akan terlihat murah di awal, tapi berisiko jadi schema bayangan kedua."*
   Matrix konsisten dengan prediksi ini — baris drift risk dan authority adalah
   mekanismenya. Dicatat sebagai prediksi yang terkonfirmasi oleh analisis,
   BELUM oleh implementasi.
5. Jalur staged (B sebagai kendaraan migrasi → A sebagai destinasi) ada, tapi
   itu keputusan sequencing, bukan keputusan residence — di luar scope matrix ini.

## Verdict — SEALED 2026-07-17 (Jali)

**A — Promote provenance into the Evidence Engine contract.**

> Reason: Evidence Engine must become the second canonical consumer.
> A sidecar resolver creates a third-party consumer while allowing
> the engine to continue operating without canon.
> This violates the M2 exit criterion.
> Therefore canonical provenance becomes part of the engine contract,
> not an optional annotation.

### Apa yang diputuskan — dan apa yang sengaja TIDAK diputuskan

- Keputusan ini **BUKAN "schema change accepted"** — itu framing implementasi.
  Yang diputuskan: **provenance dipromosikan ke domain model.** Pertanyaannya
  berubah dari "di mana document_id disimpan" menjadi "apa itu Evidence" —
  dan jawabannya: Evidence yang bisa eksis tanpa provenance berarti engine
  tidak membutuhkan canon, berarti dia bukan consumer. Schema berubah hanyalah
  konsekuensi yang mungkin, bukan tujuan.
- **Implementation strategy: OPEN.** Masih mungkin: runtime object berubah,
  Evidence object berubah, Citation object berubah, internal adapter,
  migration layer. Satu-satunya yang tidak mungkin lagi: **Evidence tanpa
  provenance.**
- **B gugur karena topologi, bukan karena drift** (drift cuma gejala).
  Di bawah sidecar, consumer canon adalah resolver, bukan engine. Matikan
  resolver → engine tetap PASS → M2 gagal by definition.
- **Standing rule "Do NOT change schema" tetap berlaku** sampai implementation
  strategy dipilih. Verdict ini tidak membukanya — dia menetapkan kontrak yang
  implementasinya *mungkin* membutuhkan exception, lewat keputusan terpisah.

### Provenance keputusan

```
Hipotesis (canon as shared dependency)
  → Node Reader spike        (abe65b1)
  → Provenance trace         (971ba3d)
  → Decision matrix          (dokumen ini)
  → Verdict                  (A, sealed)
```

Pertama kalinya di M2 kontrak sebuah subsystem diubah berdasarkan evidence,
bukan intuisi. Bukan "A lebih elegan" — melainkan "trace membuat B tidak
memenuhi exit criterion, sehingga A menjadi satu-satunya keputusan yang
konsisten."
