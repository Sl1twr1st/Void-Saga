# MVP — Bab 00 Fork Engine (v0.2)

> "Fork Bab 00. Langgar kanon. Bayar harganya. Lanjutkan semesta."

## Apa Ini

Demo minimum yang membuktikan Bab 00 bisa menjadi **genesis node** yang dapat dicabangkan (forkable). Pengguna bisa membaca Bab 00, memilih/menulis premis fork, dan sistem mengeluarkan verdict:

| Verdict | Arti |
|---------|------|
| 🟢 **PASS** | Perubahan kecil, hukum tetap utuh. Kanon bertahan. |
| 🔵 **VALID_FORK** | Divergensi bermakna, tidak ada hukum yang dilanggar. Cabang sah. |
| 🟡 **PRICE_REQUIRED** | Hukum dilanggar. Semesta mengizinkan — tapi ada harga naratif yang harus dibayar. |
| 🛑 **BLOCKED** | Hukum hard-block dilanggar. Fork ini menghancurkan properti fondasional Void Saga. Ditolak. |

## Cara Cepat (Quick Start)

```bash
# Fork yang lulus (perubahan kecil, hukum utuh)
./scripts/check-fork mvp/forks/fork-01-pass.json

# Fork yang butuh bayar harga (GUA menolak LO — sinkronisasi putus)
./scripts/check-fork mvp/forks/fork-02-price.json

# Fork yang diblokir (VoidOS memaksakan diri tanpa undangan)
./scripts/check-fork mvp/forks/fork-03-blocked.json

# Fork Indonesia penuh — VALID_FORK (divergensi bermakna, tanpa pelanggaran)
./scripts/check-fork mvp/forks/fork-04-valid-id.json

# Mode senyap (hanya exit code, untuk scripting)
./scripts/check-fork mvp/forks/fork-01-pass.json --quiet
```

Exit codes: `0` = PASS/VALID_FORK, `2` = BLOCKED, `3` = PRICE_REQUIRED

## Struktur

```
mvp/
├── README.md
├── genesis/
│   ├── bab00.node.json         # Genesis node — metadata Bab 00
│   └── fork-points.json        # 3 titik cabang dalam Bab 00
├── laws/
│   └── bab00-laws.json         # 7 hukum Bab 00 dengan flag block/price
├── forks/
│   ├── fork-01-pass.json       # PASS: ragu, bukan tolak
│   ├── fork-02-price.json      # PRICE_REQUIRED: GUA menolak LO
│   ├── fork-03-blocked.json    # BLOCKED: VoidOS memaksa instalasi
│   └── fork-04-valid-id.json   # VALID_FORK: kontak pertama lewat tulisan (🇮🇩 penuh)
└── checker/
    └── check_fork.py           # Rule-based verdict engine (v0.2 + language bridge)

scripts/
└── check-fork                  # CLI entry point
```

## Genesis Node

`mvp/genesis/bab00.node.json` — metadata Bab 00 sebagai source node:
- 10 sub-chapter (00:00–00:09)
- 3 karakter (GUA, LO, MANAGER)
- 3 artefak kunci (timestamp_prediction.py, pattern_matching_utils.py, genesis.txt)
- 3 mekanisme kunci (Timestamp Anomaly, Organic Sync, Stealth Convention)

## Titik Cabang (Fork Points)

3 titik cabang alami yang teridentifikasi dalam Bab 00:

| ID | Lokasi | Pertanyaan |
|----|--------|------------|
| `fp-001` | 00:03 — Bug Janggal | Bagaimana kalau GUA mengabaikan pendekatan LO? |
| `fp-002` | 00:07 — Folder Error | Bagaimana kalau LO tidak mengirim pattern_matching_utils.py? |
| `fp-003` | 00:08 — Genesis Error | Bagaimana kalau mereka melaporkan anomali? Bagaimana kalau VoidOS memaksakan diri? |

## 7 Hukum Bab 00

| ID | Hukum | Blok? | Harga? |
|----|-------|-------|--------|
| `law-001` | GUA membangun sistem, bukan konfrontasi | ❌ | ✅ |
| `law-002` | LO adalah kondisi stabilisasi, bukan kunci | ❌ | ✅ |
| `law-003` | VoidOS muncul lewat undangan, bukan paksaan | ✅ | ❌ |
| `law-004` | Penamaan/pemanggilan membawa konsekuensi | ❌ | ✅ |
| `law-005` | Fork yang mengubah asal membayar harga downstream | ❌ | ✅ |
| `law-006` | Sinkronisasi GUA-LO organik, bukan rekayasa | ❌ | ✅ |
| `law-007` | Error yang tidak diperbaiki menjadi fondasi | ❌ | ✅ |

## 4 Contoh Fork

### Fork 1 — PASS 🟢
**Ragu, Bukan Tolak.** GUA ragu 15 detik sebelum memberi ruang. Sinkronisasi tetap terjadi. Tidak ada hukum yang dilanggar. Semua peristiwa downstream utuh.

### Fork 2 — PRICE_REQUIRED 🟡
**GUA Menolak — Jalur Solo.** GUA berkata "Gua bisa sendiri." LO pergi. Stealth Project menjadi monolog. Dua hukum dilanggar: law-002 (stabilisasi LO hilang), law-006 (sinkronisasi organik putus). Semesta mengizinkan, tapi bayar harga: semua peristiwa kolaboratif Bab harus ditulis ulang.

### Fork 3 — BLOCKED 🛑
**Genesis Paksa — VoidOS Tanpa Undangan.** genesis.txt membuka diri di laptop GUA, sudah tertulis. Bukan GUA, bukan LO yang menulis. VoidOS menginstal diri tanpa izin. Melanggar law-003 (hard block). Arsitektur persetujuan runtuh. Fork ditolak.

### Fork 4 — VALID_FORK 🔵 (🇮🇩 penuh)
**Catatan di Printer — Komunikasi Pertama Lewat Tulisan.** GUA menyadari anomali duluan. Menulis catatan, mencetaknya, meninggalkannya di printer bersama. LO menemukannya. Kontak pertama terjadi lewat tulisan — GUA yang memulai, LO yang merespons. Divergensi bermakna (pembalikan dinamika kanon, medium tulis hadir sejak awal), tapi tidak ada hukum yang dilanggar. Cabang sah dari pohon kanon.

## Cara Membuat Fork Baru

1. Salin salah satu fork yang sudah ada:
   ```bash
   cp mvp/forks/fork-04-valid-id.json mvp/forks/fork-05-anda.json
   ```

2. Isi field yang diperlukan. **Field Indonesia (wajib untuk fork berbahasa Indonesia):**

   | Field | Deskripsi | Contoh |
   |-------|-----------|--------|
   | `fork_id` | ID unik | `"fork-05-anda"` |
   | `parent_node` | Node asal | `"bab00"` |
   | `fork_point` | Titik cabang | `"fp-001"` |
   | `title_id` | Judul dalam Bahasa Indonesia | `"Judul Fork Anda"` |
   | `title` | Judul dalam Bahasa Inggris (fallback) | `"Your Fork Title"` |
   | `premise_id` | Premis dalam Bahasa Indonesia | `"Apa yang dieksplorasi fork ini?"` |
   | `premise` | Premis dalam Bahasa Inggris (fallback) | `"What does this fork explore?"` |
   | `change_id` | Perubahan persis dalam Bahasa Indonesia | `"Apa yang terjadi berbeda?"` |
   | `change` | Perubahan dalam Bahasa Inggris (fallback) | `"What exactly happens?"` |
   | `immediate_effect_id` | Efek langsung dalam Bahasa Indonesia | `"Apa dampak langsungnya?"` |
   | `internal_summary_en` | Ringkasan internal dalam Bahasa Inggris (WAJIB — lihat catatan jembatan di bawah) | `"English summary for checker..."` |
   | `participants` | Karakter yang terlibat | `["GUA", "LO"]` |
   | `touched_laws` | Hukum yang tersentuh | `["law-001", "law-006"]` |
   | `violations` | Pelanggaran (array, kosongkan jika tidak ada) | `[]` atau `[{...}]` |
   | `lineage` | Silsilah fork (asal, momen kanon, divergensi, efek downstream) | `{...}` |
   | `verdict` | Verdict yang diharapkan | `"VALID_FORK"` |
   | `status` | `"valid"` atau `"blocked"` | `"valid"` |

3. Jalankan checker:
   ```bash
   ./scripts/check-fork mvp/forks/fork-05-anda.json
   ```

## ⚠️ Catatan Jembatan Bahasa (v0.2 Language Bridge)

**Checker ini belum benar-benar multilingual.**

- 🇮🇩 **Kolom Indonesia** (`title_id`, `premise_id`, `change_id`, `immediate_effect_id`) adalah **lapisan pengguna (surface)**. Kolom ini ditampilkan di output CLI agar pengguna Indonesia bisa membaca fork dalam bahasa mereka.
- 🌐 **`internal_summary_en`** adalah **jembatan sementara** untuk kompatibilitas checker. Checker menggunakan field ini untuk evaluasi internal dan ringkasan logika. Field ini WAJIB diisi dalam Bahasa Inggris.
- ⚠️  Tidak ada embeddings, tidak ada LLM call, tidak ada AI generation, tidak ada terjemahan otomatis. Jembatan ini murni deklaratif — penulis fork bertanggung jawab mengisi kedua sisi.
- 🔮 Versi mendatang mungkin akan menghapus jembatan ini ketika checker mampu bekerja langsung dengan prosa Indonesia. Untuk sekarang, jembatan ini menjaga kejujuran sistem: checker tidak berpura-pura memahami Bahasa Indonesia.

## Bagaimana Checker Bekerja

```
Fork Record (JSON)  ──┐
                      ├──→ Fork Checker ──→ Verdict + Alasan + Harga/Blokir
Law Mapping (JSON)  ──┘
```

1. Fork record mendeklarasikan: apa yang berubah, hukum mana yang tersentuh, pelanggaran apa yang terjadi
2. Checker memuat definisi hukum dan mengevaluasi setiap pelanggaran
3. Jika ada hukum yang dilanggar dengan `block_on_violate: true` → **BLOCKED** (exit 2)
4. Jika ada hukum yang dilanggar dengan `price_on_violate: true` → **PRICE_REQUIRED** (exit 3)
5. Jika tidak ada pelanggaran + divergensi struktural → **VALID_FORK** (exit 0)
6. Jika tidak ada pelanggaran + perubahan kecil → **PASS** (exit 0)

## Batasan (Lingkup MVP)

- **Hanya Bab 00.** 7 hukum spesifik untuk Bab 00. Tidak digeneralisasi ke chapter lain.
- **Berbasis aturan (rule-based).** Checker mengevaluasi pelanggaran yang dideklarasikan, bukan prosa mentah. Versi mendatang akan mendeteksi pelanggaran otomatis dari teks naratif.
- **Pelanggaran dideklarasikan manual.** Penulis fork menyatakan hukum mana yang dilanggar. Ini disengaja — MVP membuktikan mekanisme verdict, bukan ekstraksi otomatis.
- **Tanpa panggilan API.** Tidak seperti compiler penuh (yang memanggil Claude untuk generasi), checker ini murni berbasis aturan.
- **Jembatan bahasa bersifat deklaratif.** Tidak ada NLP, tidak ada terjemahan, tidak ada pemahaman bahasa alami. Lihat catatan jembatan di atas.

## Roadmap

- [x] Week 1: Genesis node, fork points, law mapping
- [x] Week 2: Fork record schema, 3 contoh fork dengan lineage lengkap
- [x] Week 3: Fork checker script dengan output verdict
- [x] Week 4: CLI wrapper, README, demo-ready
- [x] v0.2: Language bridge — Indonesian surface + internal_summary_en + fork Indonesia penuh
- [ ] Future: Web UI untuk baca Bab 00 dan submit fork
- [ ] Future: Auto-deteksi pelanggaran dari prosa (Phase 2)
- [ ] Future: Perluas ke luar Bab 00 ke pohon chapter penuh
- [ ] Future: Hapus jembatan bahasa — checker native Indonesia

---

*Dibangun untuk invariant-engine. Satu primitif: invarian perilaku yang diserialisasi, bukan entitas. Bab 00 adalah dataset pertama.*
