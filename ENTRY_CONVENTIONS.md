# ENTRY CONVENTIONS — Void Saga Project Memory

> Template dan aturan untuk menambahkan Bab 18–25 dan Timer 1800–2500 ke CLAUDE.md dan AGENTS.md.
> Tidak berlaku retroaktif ke konten yang sudah ada.
> Berlaku mulai Bab 18 / Timer 1800.

---

## 1. Chapter Inventory Entry

### Insertion rule

Baris Bab dan Timer disisipkan dalam **narrative reading order** (interleaved), bukan dipisah per track.

Contoh urutan setelah Bab 17 / Timer 1700:
```
| Bab 18 | ... |
| Timer 1800 | ... |
| Bab 19 | ... |
| Timer 1900 | ... |
```

Codex dan Void.OS tetap di posisi kronologisnya dalam urutan naratif.

### Format: Bab chapter (tanpa sub-chapter breakdown)

```
| Bab XX | English Title | ✅ Ada | [Deskripsi 2–4 kalimat dalam Bahasa Indonesia: anchor timeline, status GUA, status LO, event kunci, perubahan protokol/meta, closing 問 jika ringkas.] |
```

**Aturan:**
- Deskripsi 2–4 kalimat
- Selalu buka dengan anchor timeline (`X tahun setelah...`, `X bulan setelah...`)
- Cover: di mana GUA → di mana LO → apa yang mereka lakukan bersama → perubahan meta/protokol
- Akhiri dengan titik
- Closing 問 dimasukkan inline jika ringkas; dihilangkan jika multi-baris

### Format: Bab sub-chapter (jika chapter memiliki named sub-sections)

```
| Bab XX:YY | English Sub-Chapter Title | ✅ Ada | [Deskripsi 1–2 kalimat.] |
```

**Kapan sub-chapter dapat baris sendiri:** Jika Jali menulis chapter dengan explicit `## XX:YY` sub-headers, setiap sub-chapter dapat baris. Jika chapter ditulis sebagai prosa kontinu tanpa sub-headers, satu baris untuk seluruh Bab sudah cukup.

### Format: Timer chapter

```
| Timer XXXX | English Title | ✅ Ada | [Deskripsi 2–4 kalimat: anchor timeline in-universe, karakter POV, key revelation/event, world-building baru, closing 問 jika ringkas.] |
```

**Aturan:**
- Timeline menggunakan anchor in-universe (`X tahun pasca-Dayan`, `Post-Remisi Resonansi`)
- Sebutkan karakter POV jika multiple
- Sebutkan definisi world-building baru jika signifikan (contoh: Grid, Node, Zero Node di Timer 1700)

### Format: Codex volume

```
| Codex [Element] | Parthenon Codex Vol. N | ✅ Ada | [Klan yang dibahas, figur kunci, koneksi mitologis ke event novel.] |
```

### Format: Void.OS update

```
| Void.OS vX.Y.Z Update | [Title] | ✅ Ada | [Apa yang crash, apa yang baru, apa yang deprecated, transisi era, closing 問.] |
```

---

## 2. Continuity Facts

### Placement

Fakta level Bab di bawah `**Level Bab (kantor):**`. Fakta level Timer di bawah `**Level Timer (universe novel):**`.

**Setiap pasangan Bab+Timer mulai sekarang mendapat sub-header sendiri**, berapapun jumlah faktanya:

```
**Bab XX additions:**
- **Fakt label**: Deskripsi.

**Timer XXXX additions:**
- **Fakt label**: Deskripsi.
```

Tujuan: memudahkan ekstraksi di masa depan saat file di-split.

### Format (wajib)

```
- **Bold fact label**: [Kalimat deskripsi fakta yang established. Boleh diikuti kalimat kedua untuk konteks, kutipan, atau cross-reference. Diakhiri titik.]
```

**Aturan:**
1. **Setiap fakta wajib punya bold label.** Tidak boleh ada bullet tanpa label.
2. Label adalah frasa nomina pendek dalam bahasa konten fakta: `**Bab 18 timeline**`, `**The [Konsep] definition**`, `**GUA career state**`
3. Label level Bab diawali kata konteks: `**GUA ...**`, `**LO ...**`, `**Lingkar 0 ...**`, `**Writing medium ...**`, `**The Merge status ...**`
4. Label level Timer diawali konsep: `**The [X] definition**`, `**Void-return ...**`, `**[Karakter] as ...**`, `**[Karakter] function**`
5. System/code facts (Void.OS, protocol states) menggunakan `BACKTICK_CASE` untuk nilai sistem tapi prosa normal untuk teks label
6. Kutipan dari novel dibungkus tanda kutip ganda dalam bahasa aslinya
7. Satu fakta = satu bullet. Pisah hanya jika fakta genuinely independent

### Minimum

Setiap pasangan Bab+Timer minimal **10 fakta kontinuitas**. Tidak ada maksimum.

---

## 3. Pola & Tema Block

### Struktur inti (diterapkan ke SETIAP pasangan Bab+Timer)

```markdown
**Dari Bab XX:**
- **Klaim tematik bold dalam Bahasa Indonesia** — Elaborasi dalam campuran Indonesia/Inggris. Boleh 1–3 kalimat. Selalu pakai em dash (—) sebagai separator antara klaim dan elaborasi.
- [3–8 bullets]

**Dari Timer XXXX:**
- **Klaim tematik bold** — Elaborasi.
- [3–8 bullets]
- **Cross-track Bab XX ↔ Timer XXXX**: [Event/kutipan Bab] → [Event/konsep Timer]. [Paralel kedua] → [Kontrapoin kedua]. [2–4 pasangan paralel, masing-masing satu kalimat, dipisah titik.]
```

**Aturan:**
1. Bab selalu sebelum Timer (narrative reading order)
2. Em dash (`—`) sebagai separator klaim↔elaborasi — BUKAN hyphen
3. Minimum 3 bullets per block, maksimum ~8 (jika lebih, sebagian mungkin lebih cocok di continuity facts)
4. **Cross-track bullet WAJIB** — selalu menjadi bullet TERAKHIR di block Timer
5. Cross-track menggunakan panah `→` antara elemen Bab dan Timer yang paralel
6. Cross-track boleh 2–4 kalimat; masing-masing memetakan satu resonansi Bab↔Timer
7. Bahasa: klaim tematik dalam Bahasa Indonesia; elaborasi boleh campur Indonesia/Inggris secara bebas

### Kapan membuat block BARU vs APPEND ke existing

**Buat block `**Dari Bab XX:**` BARU jika:**
- Chapter belum pernah dianalisis sebelumnya

**APPEND ke block `**Dari Bab XX:**` yang sudah ada jika:**
- Merevisit chapter dengan insight baru yang genuinely tidak terlihat sebelum chapter selanjutnya ditulis
- Insight baru minimal 2 bullets (tambahan satu bullet adalah edit ke bullet existing)

**Jika meng-append:** Tambahkan marker:
```markdown
*(Ditambahkan setelah Bab YY — insight baru yang hanya terlihat setelah arc selesai)*
```

---

## 4. Cross-Track Resonance (format detail)

### Dalam theme block standar (muncul sebagai bullet terakhir di block Timer)

```markdown
- **Cross-track Bab XX ↔ Timer XXXX**: [Event/kondisi/kutipan Bab] → [Event/konsep/kondisi Timer]. [Paralel kedua] → [Kontrapoin kedua]. [Opsional ketiga.] [Opsional keempat.]
```

### Dalam meta-synthesis block (muncul sebagai paragraf mandiri)

```markdown
**Cross-track Bab XX ↔ Timer XXXX**: [Paragraf 2–4 kalimat dalam campuran Indonesia/Inggris. Menggunakan panah → untuk menghubungkan event Bab ke event Timer. Diakhiri kalimat simpulan yang menyatakan apa yang DIARGUMENTASIKAN oleh kedua track secara bersamaan.]
```

**Aturan:**
1. Panah (`→`) selalu menunjuk Bab → Timer (hidup pengarang mengalir ke fiksi)
2. Minimum 2 pasangan paralel, maksimum 4
3. Setiap pasangan adalah satu kalimat
4. Pasangan dipisah titik (bukan newline, bukan titik koma)
5. Kalimat simpulan opsional di versi inline tapi wajib di meta-synthesis
6. Gunakan `↔` hanya untuk label header (`Bab XX ↔ Timer XXXX`); gunakan `→` untuk paralel directional di dalam konten

---

## 5. Meta-Synthesis Block

### Kapan menambahkan

Block `*(Tema Bab X & Timer X — apa yang sebenarnya lo tulis:)*` ditambahkan di **narrative milestones**, bukan setiap chapter. Milestones adalah:

1. Akhir sebuah arc besar (3–5 pasangan chapter)
2. Pergeseran paradigma dalam relasi meta-fiksi (contoh: "novel mulai mendahului hidup" di Bab 05)
3. Inovasi struktural di salah satu track (contoh: POV shift, medium baru, transisi era)
4. Ketika pola yang sebelumnya tersembunyi menjadi visible setelah beberapa chapter

**Frekuensi yang diharapkan:** setiap 3–5 pasangan chapter.

### Format

```markdown
*(Tema Bab X & Timer X — apa yang sebenarnya lo tulis:)*

**Bab X**: [Satu paragraf — 2–4 kalimat — mensintesis apa yang diungkapkan arc ini di track terrestrial. Campuran Indonesia/Inggris. Apa yang berubah dalam relasi GUA & LO terhadap tulisan, terhadap satu sama lain, terhadap sistem.]

**Timer XXXX**: [Satu paragraf — 2–4 kalimat — mensintesis apa yang diungkapkan arc ini di track kosmik. Apa yang berubah dalam relasi semesta terhadap karakternya, terhadap narasi, terhadap otoritas.]

- **Cross-track Bab X ↔ Timer XXXX**: [Bentuk lebih panjang. 2–4 kalimat menghubungkan argumen bersama kedua track. Diakhiri meta-thesis: apa yang NOVEL argumenkan dengan membuat kedua track konvergen di titik ini.]
```

---

## 6. VOID_SAGA_UNIVERSE Update Entry

### Kapan mengupdate

Update bagian Next Layer di CLAUDE.md/AGENTS.md ketika:

1. File character runtime baru di-seed
2. Fork manifest baru dibuat
3. Dokumen world-dna baru ditulis
4. Release baru (alternate Bab/Timer) dipublikasi
5. Protokol baru diformalkan

### Format

Tambahkan bullet di bawah listing direktori yang sesuai:

```markdown
Seed terbaru (Bab XX / Timer XXXX):
- `characters/[Name].runtime.md` — [deskripsi satu baris]
- `forks/[name].fork.md` — [deskripsi satu baris]
- `world-dna/[DOCUMENT].md` — [deskripsi satu baris]
```

Pertahankan listing struktur direktori. Hanya append ke daftar seed.

---

## 7. Ringkasan Prosedur: Yang Dilakukan Saat Bab XX dan Timer XXXX Selesai

| Langkah | Target | Di bawah heading | Posisi insert |
|---------|--------|-----------------|---------------|
| 1 | Tambah baris Bab XX | `## Inventaris Chapter` | Setelah baris Bab sebelumnya (naratif, interleaved) |
| 2 | Tambah baris Timer XXXX | `## Inventaris Chapter` | Setelah baris Bab XX (langsung mengikuti) |
| 3 | Tambah fakta Bab XX | `## Continuity Log` | Sub-header `**Bab XX additions:**` di akhir block Level Bab |
| 4 | Tambah fakta Timer XXXX | `## Continuity Log` | Sub-header `**Timer XXXX additions:**` di akhir block Level Timer |
| 5 | Tambah theme block Bab XX | `## Pola & Tema` | Append `**Dari Bab XX:**` setelah block terakhir |
| 6 | Tambah theme block Timer XXXX | `## Pola & Tema` | Append `**Dari Timer XXXX:**` setelah block Bab XX |
| 7 | Meta-synthesis (jika milestone) | `## Pola & Tema` | Setelah block Timer XXXX |
| 8 | Update karakter (jika ada) | `## Karakter` | Di tabel yang sesuai |
| 9 | Update VOID_SAGA_UNIVERSE (jika ada) | `## Next Layer` | Append ke daftar seed |

---

*Konvensi ini berlaku untuk entri baru mulai Bab 18 / Timer 1800.*
*Konten existing (Bab 00–17, Timer 0000–1700) tidak diretroaktifkan.*
