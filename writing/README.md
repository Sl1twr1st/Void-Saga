# Writing — Prose Workspace

Tempat nulis prosa. Bukan tempat compile. Bukan tempat debug constraint.

## Dua Universe, Dua Workflow

Proyek ini punya dua universe dengan cara kerja berbeda:

| | Void Saga | Band 8 |
|---|---|---|
| **Status** | Runtime mature, constraint ketat | Draft awal, constraint belum settled |
| **Workflow** | Scenario JSON → Compiler → PASS → Prosa | Prosa langsung |
| **Lokasi nulis** | `dogfood/` (scenario) → `Bab *.md` / `Timer *.md` | `writing/band8/day-XX/` |
| **Compiler** | Nge-gate sebelum nulis | Belum diperlukan |
| **Penelitian** | — | Observe → Propose → Review → Serialize |

**Lo sekarang nulis Band 8.** Gak perlu bikin scenario JSON. Gak perlu jalanin triage. Tulis aja.

## Struktur

```
writing/
├── README.md                  ← lo disini
├── archive/                   ← arsip global
└── band8/                     ← Band 8 universe
    ├── day-01/                ← 5 chapter (Arrival LAX … Dinner)
    ├── day-02/                ← 5 chapter (Night … Cute Gitaris)
    └── day-03/                ← weekend ini
```

Nanti kalau mulai universe baru:

```
writing/
├── band8/
│   ├── day-01/
│   ├── day-02/
│   └── day-03/
└── universe-x/                ← novel baru, genre beda
    └── day-01/
```

## Cara Nulis (Band 8)

1. **Buka folder hari ini:** `writing/band8/day-03/`
2. **Bikin file `.md` baru.** Nama deskriptif: `11 Rekaman Pertama.md`, `12 Uti Datang.md`, dsb.
3. **Tulis.** Gak ada format khusus. Gak ada metadata. Pure prose.
4. **Ulangi.** Selesai satu chapter, lanjut chapter berikutnya.

Gak ada yang harus di-compile dulu. Gak ada yang harus di-triage. Compiler belum diperlukan karena constraint Band 8 belum settled — lo masih menulis untuk *menemukan* invariant-nya, bukan untuk *menjaga* invariant yang udah established.

## Kapan Compiler Dibutuhkan?

Nanti. Setelah invariant Band 8 mulai stabil (confidence > 0.60), compiler bisa dipakai buat spot-check scene. Tapi itu urusan nanti. Sekarang: **prosa dulu, observasi kemudian.**

## Dari Draft ke Final

Writing/ bukan temporary. Draft punya nilai sejarah.

Kalau chapter udah matang dan layak masuk ke "novel final":

1. Simpan draft di `writing/archive/`.
2. Di file final, tambahkan baris pertama:

```
<!-- Derived from: writing/band8/day-01/1 Arrival LAX.md -->
```

Kenapa? Karena lo bakal pengen lihat: "Draft pertama chapter ini kayak apa?"

Itu data riset yang mahal.

## Referensi

- `experiments/EXP-001-aisya/README.md` — hasil observasi invariant Aisya (Phase A + B + C)
- `docs/OBSERVE_PIPELINE.md` — metodologi: observe → propose → review → serialize → evolve
- `docs/BEHAVIORAL_INVARIANTS.md` — teori: compiler serializes invariants, not entities
