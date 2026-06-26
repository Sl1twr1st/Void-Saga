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
└── archive/    ← yang sudah selesai / dipindahkan ke Bab atau Timer
```

## Ritme

1. **Pagi:** Tulis scenario di `dogfood/`, triage, pilih yang PASS.
2. **Siang:** Tulis prosa di `writing/day-XX/`. Satu file per scene.
3. **Sore:** Kalau scene sudah final, pindahkan ke Bab atau Timer yang sesuai.

## Aturan

- Tiap file prosa adalah satu scene hasil triage.
- Nama file: `scene_<deskripsi_singkat>.md`
- Baris pertama: judul scene + scenario_id dari JSON.
- Jangan edit sambil compile. Compile dulu. Nulis kemudian.
