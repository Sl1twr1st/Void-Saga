# Writing — Prose Workspace

Ini tempat nulis. Bukan tempat compile. Bukan tempat debug constraint.

Compiler sudah dijalankan di `dogfood/`. Scene sudah PASS.
Sekarang tinggal nulis.

## Struktur

```
writing/
├── day-01/     ← hari ini
├── day-02/     ← besok
├── day-03/     ← lusa
└── archive/    ← semua draft — riwayat, bukan sampah
```

## Ritme

1. **Pagi:** Tulis scenario di `dogfood/`, triage, pilih yang PASS.
2. **Siang:** Tulis prosa di `writing/day-XX/`. Satu file per scene.
3. **Sore:** Kalau scene sudah final, **bukan dipindahkan.** Tetap simpan draft-nya.

## Aturan

- Tiap file prosa adalah satu scene hasil triage.
- Nama file deskriptif, bisa dibaca tiga bulan lagi: `niuniu_menunggu.md`, `lensa_pertama.md`, `sevraya_menyalakan_rokok.md`.
- Baris pertama: judul scene + scenario_id dari JSON.
- Jangan edit sambil compile. Compile dulu. Nulis kemudian.

## Dari Draft ke Novel

Writing/ bukan temporary. Draft punya nilai sejarah.

Kalau scene sudah final dan masuk ke Bab atau Timer:

1. Simpan draft di `writing/archive/`.
2. Di file Bab/Timer, tambahkan baris pertama:

```
<!-- Derived from: writing/day-01/niuniu_menunggu.md -->
```

Kenapa? Karena tiga bulan dari sekarang lo bakal pengen lihat:
"Draft pertama scene ini kayak apa?"

Itu data yang mahal.
