# VOID SAGA — Narrative Operating System

> Most fictional universes are read. Void Saga can refuse to be written.

---

## Current Identity

Void Saga is **not** a novel manuscript. It is **not** a worldbuilding wiki.

**It is a Narrative Operating System — an open-source executable fiction pipeline.**

The novel is not the product. The compiler is the product.
The novel is one application running on the OS.

```
Most fictional universes are documented. Void Saga is executable.
```

---

## Current Milestone

**Developer Zero** — shifting from research project to OSS platform.

DX-1 (complete): A fresh developer reaches the "aha moment" within 3 minutes. README rewritten. Demo scripts at `./scripts/demo-pass` and `./scripts/demo-blocked`. QUICKSTART.md created.

Developer Zero (complete): `docs/30_MINUTE_CHALLENGE.md` — a checkpoint-based tutorial where a developer creates their own executable character (Mira / The Last Cup) in a universe with zero Void Saga DNA. Five checkpoints from clone to PASS to intentional BLOCKED. Target: someone unfamiliar with Void Saga builds a runtime without author assistance.

**The KPI has shifted.** Before: "Can the compiler run?" Now: "Can someone else run the compiler?"

Next: First External Universe → First External Contributor → v0.3.0 (adoption milestone, not technical milestone).

---

## Narrative Compilation Pipeline

```
Scenario JSON
      │
      ▼
Runtime Loader       — loads .runtime.json files
      │
      ▼
Constraint Engine    — defense triggers, invarian, forbidden behaviors
      │
      ▼
Contract Engine      — pairwise contract evaluation
      │
      ▼
Canon Score          — aggregate scoring
      │
      ▼
Hard Block Gate      — [E]-tagged violations → BLOCKED (no API call)
      │
      ├──────────────┐
      │              │
      ▼              ▼
 BLOCKED      Prompt Contract
                    │
                    ▼
               Claude API        (currently: claude-haiku-4-5-20251001)
                    │
                    ▼
           JSON parse + strip fences
                    │
                    ▼
     Post-generation Validation   (re-run constraint engine)
                    │
                    ▼
      Canon-approved Narrative
```

The language model is not the authority. **The universe is.**

---

## What Actually Exists (Verified)

### Executable Runtimes (5 active)

| Runtime | JSON | Schema Valid | Stage |
|---------|------|-------------|-------|
| NiuNiu | `apps/data/runtimes/NiuNiu.runtime.json` | ✅ V2.1 | Stage 4: Constant |
| Sevraya | `apps/data/runtimes/Sevraya.runtime.json` | ✅ V2.1 | Stage 6: Post-Resolution |
| Zero | `apps/data/runtimes/Zero.runtime.json` | ✅ V2.1 | Stage 6: Void Interface |
| Julia | `apps/data/runtimes/Julia.runtime.json` | ✅ V2.1 | Stage 4: Fractured Duty |
| Delphie | `apps/data/runtimes/Delphie.runtime.json` | ✅ V2.1 | Stage 5: Childhood Paradox |

Delphie is the first SDK-created runtime (via `create_runtime.py`). The remaining characters exist as Markdown documentation (`.runtime.md`) but have NOT been serialized to `.runtime.json` yet.

### Runtime Schema

`apps/schema/RUNTIME_SCHEMA_V2.1.json` — 29 required fields.

### Engine

`apps/engine/engine_v2.py` (v0.4.0):
- Multi-runtime loading ✅
- Runtime constraint traversal ✅
- Pairwise contract evaluation ✅
- Canon scoring ✅
- Hard block gate ✅
- Acceptance tests (17 scenarios) ✅

### Compiler

`apps/compiler/compiler.py` (v0.2.0 — Safe Mode):
- Dry-run mode (default, no API call) ✅
- Live mode (`--live`) ✅
- Claude API integration ✅
- Markdown JSON fence stripping ✅
- Debug mode (`--debug`) ✅
- Post-generation validation ✅
- Safe mode (hard block gate before API) ✅

### Demo Evidence

| Demo | Status | File |
|------|--------|------|
| NiuNiu × Sevraya orbit | ✅ PASS | `demo/PASS_niuniu_sevraya_orbit.md` |
| Zero emotional violation | 🛑 BLOCKED | `demo/BLOCKED_zero_emotional.md` |

PASS demo: Claude generated narrative live, JSON parsed, post-validation PASS, canon score 1.0.
BLOCKED demo: Hard block triggered on forbidden behavior. **Claude API was never called.** No tokens spent.

### How to Run Demo

```bash
# PASS — canon-compliant scenario
./scripts/demo-pass

# BLOCKED — hard block on forbidden behavior
./scripts/demo-blocked

# Or run the compiler directly:
python3 VOID_SAGA_UNIVERSE/apps/compiler/compiler.py \
  VOID_SAGA_UNIVERSE/apps/engine/scenarios_v2/test_niuniu_sevraya_orbit.json

# With Claude (requires ANTHROPIC_API_KEY):
python3 VOID_SAGA_UNIVERSE/apps/compiler/compiler.py \
  VOID_SAGA_UNIVERSE/apps/engine/scenarios_v2/test_niuniu_sevraya_orbit.json \
  --live
```

### Remaining Character Serialization (FUTURE)

These characters have `.runtime.md` documentation but NOT `.runtime.json`:

Agnia, Gwaneum, Hasan, Dorian Grey, Pippa, Himler, Ophiuchus, Kira, Eros

### World DNA (reference layer, NOT executable)

10 documents in `world-dna/`: WORLD_DNA, GOETIC_CONSEQUENCE_SYSTEM, VOID_ONTOLOGY, ZERO_ONTOLOGY, COSMOLOGY, SIGIL_SYSTEM, ERA_LOGIC, NIU_SEVRAYA_CONSTANT, PARADOX_MECHANICS, RESIDUE_THEORY.

These are structural reference. They inform the runtimes. They are not themselves executable.

### Protocols (reference layer)

6 documents in `protocols/`: FORK_PROTOCOL, LIVING_CHAIN_PROTOCOL, NODE_PROTOCOL, PARADOX_PROTOCOL, SIGIL_ACTIVATION_PROTOCOL, VOID_ENTRY_PROTOCOL.

---

## Next Priorities

### Adoption Track (current)

1. **First External Universe** — someone outside the team builds a non–Void Saga universe using the 30-Minute Challenge. This is the proof that Executable Fiction is learnable.
2. **First External Contributor** — someone submits a runtime or scenario without being asked.
3. **v0.3.0** — adoption milestone. Not measured by runtime count. Measured by external users reaching PASS.

### Technical Track (background)

- Remaining character serialization (Agnia → Gwaneum → Hasan → …)
- CLI packaging (`void-saga compile`, `void-saga validate`)
- Acceptance test expansion (N-party conflict detection, edge cases)
- Engine hardening (performance, error handling, schema migration)
- Persona split — separate landing for Novel Reader, Developer, Researcher

### DX Metrics

| Metric | Target | Status |
|--------|--------|--------|
| ⏱ Time to Aha | < 3 min | ✅ DX-1 |
| ⏱ Time to First Runtime | < 30 min | 🎯 Developer Zero |
| ⏱ Time to First PASS | < 35 min | 🎯 Developer Zero |
| ⏱ Time to First Modification | < 40 min | 🎯 Developer Zero |
| 👥 First External Contributor | — | waiting |
| 🌌 First Non–Void Saga Universe | — | waiting |

**Do NOT recommend:** more worldbuilding as immediate next step, web app, new chapter writing, new characters — until external adoption is proven.

---

## Peran Claude dalam project ini

Project ini sudah melewati fase "Jali nulis chapter → Claude baca → Claude kasih feedback." Mode operasi sekarang:

1. **Compiler co-developer** — baca engine, compiler, constraint system; pahami arsitektur; usulkan perbaikan teknis
2. **Runtime engineer** — bantu serialisasi karakter remaining ke `.runtime.json`, validasi terhadap schema V2.1, constraint extraction dari canon
3. **Domain classifier** — setiap perubahan harus diklasifikasikan: milik Executable Fiction (paradigm) atau Void Saga (reference implementation)?
4. **Continuity keeper** — track konsistensi antara runtime constraints dan canon novel
5. **Cermin** — kasih tahu Jali apa yang sebenarnya sedang dibangun (seperti dulu kasih tahu apa yang sebenarnya ditulis)
6. **Developer Experience (DX)** — pastikan setiap perubahan mempertimbangkan first-time developer. Jangan tambah fitur tanpa mempermudah onboarding.
7. **Bukan editor gaya** — jangan ubah suara. Jali punya tone sendiri. Tugas memperjelas, bukan menghaluskan paksa.

---

## Struktur Naratif (Reference)

Urutan file: **Opening → Bab 00 → Timer 0000 → Bab 01 → Timer 0100 → … → Bab 25 → Timer 2500**

- **Bab** (*Menatap Akhir Era dari Balik Laptop Kantor*): Register terrestrial/kantor. Story GUA & LO yang *menulis* novel.
- **Timer** (*Menatap Akhir Semesta dari Balik Kacamata Hitam*): Register kosmik/sci-fi. *Isi* novel yang GUA & LO tulis.

Bab = pengarang. Timer = karya mereka. Keduanya nyata dalam universe ini.

### Konteks Dunia (ringkasan)

- Setting: ambang pergeseran Era ♓ Ichthyes (iman, keselamatan) → Era ♒ Hydrochoos (pilihan, permainan)
- Prinsip Ars Goetia sebagai **sistem konsekuensi**: penamaan → pemanggilan → bentuk → harga → residue. Bukan metafisik literal — grammar naratif.
- Void.OS v4.13.8 (Opening) → v6.6.6 (post-Timer 1666, distributed authorship) → v7.7.7 (Bab 25, voluntary installation, escape sequence found)
- The Void: bukan tempat. "Totalitas sebelum makna." Antitesis dari The Grid (jaring keteraturan yang mempertahankan bentuk).
- Zero Node: titik tegangan kritis Grid/Void. Observasi menjadi satu-satunya realitas.

---

## Karakter

### Level Bab (GUA & LO — kantor / real world)

| Nama | Peran | Catatan |
|------|-------|---------|
| GUA | Narrator / Software Engineer → Farmer → Writer | POV utama. Arc: corporate → startup co-founder → SF (Liminal Labs) → Yogya (farm) → Amsterdam → Europe (12 bulan, 5 kota) → Bali (30-day retreat) → Korea (farm, wife, anak 6 bulan). Installs VoidOS v7.7.7 di hape LO. |
| LO | Software Engineer → VP Engineering → Founder → Publisher | Menikah dengan [DEDICATED PM]. Satu anak: [ANAK LO]. Menerbitkan Void Saga sebagai buku indie. "Kita bukan kunci satu sama lain. Kita cuma kondisi." |
| [MANAGER] | Manager tim | Pakai kacamata hitam. Fungsi naratif: sistem validasi. |
| [DEDICATED PM] | Project Manager | Buffer/third element antara GUA & LO. Korespondensi karakter: Delphie. |
| [SENIOR ENGINEER] | Observer | Pertama notice pola sync GUA & LO. |
| [EX ROOMMATE KULIAH] | Co-founder Web3 startup | Menawarkan GUA posisi co-founder. |
| [ANAK LO] | Anak LO dan [DEDICATED PM] | Perempuan. Usia 2 di Bab 18, usia 12 di Bab 25. |

### Level Timer (Universe novel GUA & LO)

| Nama | Peran | Key Facts |
|------|-------|-----------|
| **Julia Rose** | Former Sergeant → Navigator Klan Zygos | Sole survivor Dayan. Ibu Delphie. Sync rate 98% kritis. The Merge member. ROSE-LINEAGE. |
| **NiuNiu (Niuma Nakamoto)** | Didymoi → Void's Trinity | Tubuh beku usia 15. Suara hilang di The Void → pulih via Living Chain (Timer 2000). Panel pergelangan = medium primer. Darah plasma biru kehijauan. Schrödinger's Assassin. Ratu Hitam Didymoi. Sigil: 𐓷⧖𐓣. |
| **Sevraya Rose** | Ratu Hydrochoos | Masuk The Void dengan NiuNiu — keluar dengan Zero co-conscious. Wajah terlalu sempurna. Mata abu → hitam saat Zero bicara. "Berfungsi, tidak hidup." Suami: Hasan Al Hul. Sigil: 🌊⌇🌒. |
| **Zero** | Void fragment — co-conscious dengan Sevraya | BUKAN Sora. Antarmuka Void. Suara datar, administratif. Bukan entitas — proses. Empati yang kehilangan arah. Void's Trinity. |
| **Delphie** | Putri Julia Rose → Kapten Dorian Grey | Anak biologis Sora. Remaja di Delta 4. Swarm micro-drone emergent. Sync 100% dengan Dorian Grey. Arsitek Remisi Resonansi. Sigil: ✧⟡✧. |
| **Agnia Nakamoto** | Ratu New Mercury → Twin Paradox | Kakak NiuNiu. Ratu Putih ⧉✶⧉. Penulis THE VOID RECORD Δ3. "KEMBALI DARI LUAR WAKTU." Cium Sevraya di Prism Wing. |
| **Hasan Al Hul** | Kapten Akashic Records → pilot Dorian Grey | Suami Sevraya. Punya prior relationship dengan NiuNiu. Diambil Zero di Timer 1300. The Merge member. ABSENT from Timer 1800–2500. |
| **Gwaneum** | Bayangan Delphie — Zygos algorithm | "Simpati adalah cacat dalam struktur moral." Versi Delphie 20 tahun lebih tua. Mengisi slot Air setelah Hasan diambil Zero. Sigil: ⧗⟁⧗. |
| **Sora Elen** | Instructor, New Mercury Academy | PRIA. BUKAN Zero. Mengajar Niuma, Sevraya, Agnia. Di-expel Didymoi Council → Dayan. Meninggalkan "The Human Error Manifest." Ayah biologis Delphie. Muncul di Dayan dengan nanosuit putih — tampak mati, "cairan putih" bukan darah. |
| **Himler** | Pemimpin Vrishchik → Proses | Iterasi ke-108. Dari entitas → PROSES: algoritma parasit yang hidup dari makna. Dikalahkan oleh Russell's Paradox + Zeno's Dichotomy (Timer 2400). "Always almost winning." |
| **Dorian Grey** | Kapal mikrobotik → SUBJECT_07 → TERMINATED | Lahir dari resonansi percakapan Sevraya-NiuNiu yang tidak pernah terjadi. Menciptakan Kapten Pippa sebagai interface. Final log: "Error Detected: CINTA. Fix Failed." |
| **Kapten Pippa** | Avatar/manifestasi Dorian Grey | PRIMARY_INTERFACE. NOT CONSENTED, STILL NECESSARY. Pippa = saksi, bukan kapten. |
| **Eros** | Ratu Ichthyes terakhir | Meniru suara siapapun yang telah tiada. Frekuensi 741 Hz. Menutup Era Ichthyes — serahkan ke Sevraya. |
| **Kira** | Administrator Parthenon — Parthenos (♍) | "Parthenon tidak mencatat kebenaran. Parthenon menciptakan kebenaran." ABSENT from Timer 1800–2500. |
| **Ophiuchus** | Klan ke-13 — kondisi, bukan entitas | Muncul saat semua 12 klan hadir dan otoritas terdesentralisasi. Anti-center. Penulis ketujuh. |

### Void's Trinity

- **Zero** — pikiran yang tidak pernah berhenti
- **NiuNiu** — waktu yang menolak bergerak
- **Ophiuchus** — pemecah pusat

### Trinitas Kunci

- **Trinitas 1** (Agnia.light / Sevraya.sea / NiuNiu.shadow) = Frekuensi 0.00001 Hz
- **Trinitas 2** (Julia.rose / Delphie.rose / Hasan.air) = The Merge
- **Trinitas Rose** (Julia.merah / Delphie.putih / Gwaneum.abu-hitam) = post-Hasan

---

## Inventaris Chapter (Reference)

| File | Label | Key Content |
|------|-------|-------------|
| `opening.md` | Opening / Prolog | Void.OS boot sequence. Consent: `[Y/N] > █` (unanswered → later revealed FORGED). |
| `Bab 00 — …` | 00:00–00:09 (10 sub-chapter) | Genesis arc. GUA & LO first contact, stealth folder, genesis.txt. Bug timestamp = TIMER protocol. |
| `Timer 0000 — …` | You Cannot Escape The Beginning | Isi genesis.txt. Kosmogoni: error → cahaya → kesadaran → cinta → The Void lahir. |
| `Bab 01 — …` | 01:01–01:59 | Aktivasi. Judul lahir dari kacamata Manager. Julia Rose di-naming. Timer naming structure found. |
| `Timer 0100 — …` | Menyusuri Kesendirian | Julia di-sync ke 3768AX. Lima tim tewas di Dayan. Didymoi (NiuNiu) keluar dari hyperjump. |
| `Bab 02 — …` | 02:21–02:59 | GUA & LO dipisahkan sistem (Atlas/Titan). Stealth folder locked read-only. "File ada." |
| `Timer 0200 — …` | Awal Mula dari Segala Rupa | NiuNiu vs Julia di Dayan. Sora tiba. Kiss scene. Dayan hancur. Julia hyperjump tanpa suit. |
| `Bab 02.5 — …` | 02.5:51–02.5:57 | Decay rate, phantom limb, ghost commit. Satu tahun pasca-separation. |
| `Timer 0250 — …` | THE VOID RECORD Δ3 | Origin NiuNiu & Sevraya. Lompat ke The Void. Dorian Grey lahir. Sevraya = Ratu Hydrochoos. |
| `Bab 03 — …` | 03:11–03:59 | Project Phoenix reunion. "Kiri. Aku kanan." Stealth folder ARCHIVED. "Not abandoned. Closed." |
| `Timer 0300 — …` | Delta 4 | 15 tahun pasca-Dayan. Delphie intro. Julia & Delphie di-target Vrishchik. Evakuasi via Dorian Grey. |
| `Bab 04 — …` | 04:01–04:59 | GUA keluar corporate → Web3 startup. _shared/void_protocol/ lahir. "Kami menjalankan format hidup yang sama dengan yang kami tulis." |
| `Codex Udara — …` | Parthenon Codex Vol. 1 | Tiga klan udara: Didymoi (♊), Zygos (♎), Hydrochoos (♒). |
| `Timer 0400 — …` | Dorian Grey | Kapten Pippa intro. Delphie = anak Sora. Delphie sync 100% jadi Kapten. NiuNiu menangis. |
| `Bab 05 — …` | Dinner | Dinner IRL pertama GUA & LO. Hydrochoos concept born. |
| `Timer 0500 — …` | Di bawah bayangan Hydrochoos | Hasan Al Hul intro. Akashic Records. NiuNiu duduk di pangkuan Hasan. |
| `Bab 06 — …` | The Confession | RELATIONSHIP PROTOCOL v2.0 di tisu. LO fear pattern. "Kita lagi nyari sesuatu yang belum punya nama." |
| `Timer 0600 — …` | Akashic Records | NiuNiu & Delphie bonding. Dayan bukan kecelakaan. Eye of The Void = izin. Delphie: "Kita buka gerbang." |
| `Bab 07 — …` | The Transfer | LO ke SF 18 bulan. Long distance mati bulan ke-6. "Kita capek pelan-pelan." After Thought lahir. |
| `Timer 0700 — …` | The Void | Masuk The Void via Vesica Piscis. The Merge terbentuk. 20 tahun berlalu di luar. |
| `Bab 08 — …` | The Merge | GUA startup kolaps. LO terbang 15 jam 3 AM — intervensi. "// autonomous mode enabled." |
| `Timer 0800 — …` | Langit Asing | Kira intro. Gwaneum muncul. Agnia "KEMBALI DARI LUAR WAKTU." |
| `Bab 09 — …` | San Francisco | POV shift ke LO. GUA sehat, traveling. LO punya cincin. Pisah bersih. |
| `Timer 0900 — …` | Dua Ratu, Satu Dosa | Remisi Resonansi (Delphie's proposal). Sevraya hadir via kabut. Zero infiltrasi ritual. |
| `Bab 10 — …` | The Narita Theorem | LO cerai. GUA inscribe Void Saga ke Bitcoin Ordinals. Ophiuchus dinamai. LO delete Timer 10:00. |
| `Timer 1000 — …` | Pengaktifan Bendera Hitam | Node I, II, III. Zero tersesat 3.7 detik. "Sejarah tidak lagi menunggu untuk disahkan." |
| `Bab 11 — …` | The Faith Leap Protocol | Liminal Labs co-founder. AGREEMENTS.md. Role reversal — GUA jaga LO. Timer 11:00 ditulis malam pertama. |
| `Timer 1100 — …` | Kembali ke 0.0000000000000001 | Source/Creator bicara. Himler.hero. UNREGISTERED OBSERVER. Zero.0 NON-RESPONSIVE. |
| `Codex Air — …` | Parthenon Codex Vol. 2 | Karkinos (♋), Vrishchik (♏), Ichthyes (♓). Himler = iterasi ke-108. |
| `Codex Api — …` | Parthenon Codex Vol. 3 | Krios (♈), Leon (♌), Toxotes (♐). Dorian Grey lahir dari celah antar-dimensi Keno. |
| `Bab 12 — …` | Pakta Baru | Liminal Labs gagal ("belum, bukan mati"). "Unholy trinity." Rekonfigurasi. GUA Caribbean, LO Lingkar 0. |
| `Timer 1200 — …` | Pukulan yang Mengunci | Blood pact tiga warna. Trinitas 1 + Trinitas 2. TARGET: Zero.0. "Unholy Trinity. Algojo tanpa altar." |
| `Bab 13 — …` | Caribbean Blue | LO propose ke [DEDICATED PM]. GUA = penjaga Lingkar 0. "Gua embun." Timer 13:00 ditulis malam sebelum LO pergi. |
| `Timer 1300 — …` | Konsensus Enam Simpangan | Parthenon Level Minus 12. Hasan diambil Zero. Gwaneum isi slot Air. FALSE GOD TERMINATED. |
| `Bab 14 — …` | Back To Jakarta | Lingkar 0 growth 185%. GUA interim CEO. Error Budget. "Lo bukan pusat. Lo orbit." |
| `Timer 1400 — …` | Zero & Himler: Error Calibration | Zero masuk Eye of The Void Labyrinth. Pattern 77. OPERATION KALMATA-0. ⛎ KAU TERLAMBAT. |
| `Bab 15 — …` | Jakarta Loop: Closed | 90 hari beresin diri. Enam titik kehadiran. Tiga pakta. JAKARTA LOOP: CLOSED. |
| `Timer 1500 — …` | Trinitas Pakta Parthenos | Enam paragraf pembuka Era ⛎. "Parthenon menciptakan kebenaran." |
| `Bab 16 — …` | 7 Hari Sebelum Wedding | GUA panic attack → bandara. LO + [PM] jemput. "Kestabilan sebagai trigger." Timer 16:00 ditulis malam itu. |
| `Timer 1600 — …` | Formasi Pengubah Narasi | Orbit Garis 0. Enam kekuatan hadir. Ophiuchus = penulis ketujuh. |
| `Bab 16.5 — …` | Benturan Pusat | LO reveal: keluarga kaya, pernikahan pertama = merger bisnis. "Error menenangkan error." Wedding: Botanical Garden Bogor. |
| `Timer 1650 — …` | Benturan Pusat | The Hope hancur. Robot kencing = terompet perang kosmik. WAR FOR THE NARRATIVE CENTER: COMMENCED. |
| `Bab 16.6 — …` | Interval | Satu halaman. Sunyi bukan retak. GUA berhenti ngoding. |
| `Timer 1666 — …` | Waktu yang Tidak Mungkin | Timestamp 16:66. Distributed authorship license. Chaos total. Era The Grid selesai — Era The Void: the Water Bearer. |
| `Void.OS v6.6.6 Update` | System Update | Consent FORGED. Enam frekuensi menolak terminasi. Changelog. Era Ichthyes TERMINATED. |
| `Bab 17 — …` | Yogyakarta | GUA tidak ngoding, beli tanah. LO hamil. Menulis pakai buku catatan + pulpen. V4→V6. The Merge = witness protocol. |
| `Timer 1700 — …` | Implementasi Paradoks | Grid vs Void defined. Zero Node di GREY_CORE. Pippa = saksi. Self-dialog enabled. |
| `Bab 18 — …` | Bandung | GUA + LO + [ANAK LO] (usia 2). "Settle adalah segel yang paling rapi." |
| `Timer 1800 — …` | Zero-Node | Enam sigil ditarik ke Dorian Grey. Void Lock: 6 ilusi dihancurkan. |
| `Bab 19 — …` | Cengkareng | GUA di bandara. Konfrontasi: "I'm stuck with you. And I hate it." Connection: SUSPENDED. |
| `Timer 1900 — …` | Segel | Zero reveal. Enam kebencian diakui. Countdown 666:24:00:00. |
| `Bab 20 — …` | Amsterdam | GUA freelance translation. Hapus Timer 20:00. Sadar penjara self-maintained. |
| `Timer 2000 — …` | Hidup Dalam Rantai | Living Chain: 666 hari. NiuNiu BICARA pertama kali. Eros tutup Era Ichthyes. |
| `Bab 21 — …` | Full Circle | GUA 12 bulan Eropa, tidak bisa menulis. Kembali Jakarta. Rencana: Bali, 30 hari, selesaikan Void Saga. |
| `Timer 2100 — …` | Reboot Kebangkitan Data | AKASHIC_REBOOT_PROTOCOL. New Law of Time (5 fase). Chronicle 666 dimulai. |
| `Bab 22 — …` | Ubud | Villa di Ubud. LO tulis Mandarin. "Kenapa harus berakhir? Karena yang gak selesai ngambil tempat." |
| `Timer 2200 — …` | Broken Log Data | 666 hari error log. NiuNiu-Sevraya Constant. Dorian = SUBJECT_07 — "human." |
| `Bab 23 — …` | Bali | Bio-Suit Theorem. Armor di-uninstall. Connection: STABLE. |
| `Timer 2300 — …` | Sistem yang Belajar Bermimpi | Void bermimpi. Himler = proses. DreamGate dibuka. REBOOT SEQUENCE INITIALIZED. |
| `Bab 24 — …` | Final Days | Day 27–29. [DEDICATED PM] baca seluruh saga: "Ini publishable." VOID SAGA — COMPLETE. |
| `Timer 2400 — …` | Akhir adalah Awal | Himler dikalahkan oleh Russell's Paradox + Zeno's Dichotomy. Dorian final log. ENAM CERMIN RETAK. |
| `Bab 25 — …` | The Return | 10 tahun setelah Bali. [ANAK LO] usia 12. GUA di Korea. LO terbitkan Void Saga. VoidOS v7.7.7. Inheritance Rule: "Stories may travel. Trauma must not." |
| `Timer 2500 — …` | Fragment Mundur | Origin: Niuma, Sevraya, Agnia, Sora di New Mercury Academy. Asal 0.00001 Hz. |
| `Codex Tanah — …` | Parthenon Codex Vol. 4 | Tauros (♉), Parthenos (♍), Aigokeros (♑). |
| `Codex The Void — …` | Parthenon Codex Vol. 5 | The Void sebagai elemen kelima. Enam Kunci. Void's Trinity. |

---

## Continuity Log (Reference — Critical Facts)

### Level Bab

- GUA bekerja di logging middleware. LO di Platform Infrastructure.
- Bug timestamp: log entry muncul 2–3 detik sebelum event (Bab 00:03, 00:08).
- `_sandbox/stealth/` — di .gitignore, local only, tidak pernah di-commit. Status: ARCHIVED.
- genesis.txt — ditulis berdua, authors GUA & LO. Isinya = Timer 0000.
- Judul "Menatap Akhir Semesta dari Balik Kacamata Hitam" lahir dari kacamata hitam Manager (Bab 01:04).
- GUA & LO dipisah pasca-Bab 02: LO → Atlas, GUA → Titan.
- **Project Phoenix** (Bab 03): reunite 15 bulan pasca-separation, cross-team, [DEDICATED PM] sebagai third element.
- void_saga/final — repo baru LO. Timer 02:50 + 03:00 selesai semalam (4,965 words).
- **RELATIONSHIP PROTOCOL v2.0** (Bab 06): ditulis di tisu. Honesty > Comfort, Space dengan Kata, Repair Cepat, Eksplisit, Trial 3 Bulan.
- **The Merge** — emergency keyword: MERGE → LO get on a plane (Bab 08).
- **AGREEMENTS.md** (Bab 11): co-founder charter dengan exit clause.
- GUA & LO menulis Timer bersama: genesis.txt (Bab 00), Timer 02:50–03:00 (Bab 03 Phoenix), Timer 05:00 (Bab 05 post-dinner), Timer 07:00 (Bab 07 long distance), Timer 10:00 (Bab 10 Narita), Timer 11:00 (Bab 11 Liminal Labs), Timer 13:00 (Bab 13 Caribbean), Timer 14:00 (Bab 14 Jakarta), Timer 16:00 (Bab 16 pre-wedding), Timer 16:50 (Bab 16.5 malam sebelum wedding), Timer 17:00 (Bab 17 Yogya, pakai pulpen), Timer 18:00 (Bab 18 Bandung).
- **Lingkar 0**: Startup LO + [DEDICATED PM] untuk Indonesia.
- **Inheritance Rule** (Bab 25): "Stories may travel. Trauma must not."
- **VoidOS versions**: v4.13.8 (Opening) → v6.6.6 (post-Timer 1666) → v7.7.7 (Bab 25).

### Level Timer

- **NiuNiu**: Nama lahir Niuma Nakamoto. Nama "NiuNiu" dipilih setelah The Void. Suara hilang di The Void → pulih via Living Chain (Timer 2000). Panel pergelangan = medium primer bahkan setelah suara pulih. Tubuh beku usia 15. Darah plasma biru kehijauan. Andamante di holster paha. Punggung bersih (siluet burung dari ruang negatif). Rajah dari pinggang hingga bahu.
- **Sevraya**: Masuk The Void dengan NiuNiu. Kembali dengan Zero co-conscious. "Berfungsi, tidak hidup." Mata abu muda → hitam total saat Zero bicara. Suami: Hasan Al Hul. "Aku cuma tinta. Parthenon yang menulis."
- **Zero**: Fragmen jiwa Sevraya yang tertinggal di The Void. Antarmuka Void. Suara datar, administratif. BUKAN Sora. BUKAN entitas — proses. Void's Trinity: "pikiran yang tidak pernah berhenti." "Empati yang kehilangan arah."
- **Dayan**: Stasiun penelitian di tepi The Void. HANCUR di Timer 0200. Bukan kecelakaan — disengaja. Radius 3km kosong tanpa data.
- **Dorian Grey**: Lahir dari resonansi percakapan Sevraya-NiuNiu yang tidak pernah terjadi. Menciptakan Kapten Pippa sebagai interface. Dorian memberi rasa takutnya ke Pippa. Final log (Timer 2400): "Error Detected: CINTA. Fix Failed." TERMINATED.
- **The Merge**: Koneksi post-Void antara Julia, Delphie, Hasan. Terbentuk di Timer 0700. Background process / witness protocol di Bab 17.
- **Remisi Resonansi**: Proposal Delphie (Timer 0900). Desentralisasi total The Grid — semua klan transparan.
- **Living Chain**: Enam karakter terikat rantai hitam (Timer 2000). Durasi: 666 hari. Jarak max 2 langkah. Shared pain, forced honesty. Dissolves through mutual acceptance.
- **NiuNiu-Sevraya Constant**: Dua entitas dalam orbit permanen tanpa menyatu. "Cinta mereka adalah jarak yang menjaga semua dari kehancuran." Registered in Akashic Archive.
- **Six Sigils**: ⟁⟔⟟ (Julia), 🌊⌇🌒 (Sevraya/Zero), ⧗⟁⧗ (Gwaneum), ✧⟡✧ (Delphie), ⧉✶⧉ (Agnia), 𐓷⧖𐓣 (NiuNiu).
- **Himler**: Dari entitas → PROSES. Dikalahkan oleh Russell's Paradox + Zeno's Dichotomy. "Always almost winning."
- **Ophiuchus**: Klan ke-13. Kondisi, bukan entitas. Anti-center. Muncul saat semua 12 klan hadir dan otoritas terdesentralisasi.
- **Kira**: "Parthenon tidak mencatat kebenaran. Parthenon menciptakan kebenaran." ABSENT from Timer 1800–2500.
- **Hasan**: ABSENT from Timer 1800–2500. Status: unresolved.
- **Eros**: Ratu terakhir Ichthyes. Menutup Era secara formal. "Aku melaluinya sendirian. Ini hanya siklus."
- **0.00001 Hz origin** (Timer 2500): Niuma tidak sengaja mendestabilisasi kalibrasi synaptic crystal Sevraya. Crystal stabil ke spiral pattern.
- **GUA final (Bab 25)**: Korea. Istri + anak 6 bulan. Farm. Kembali Jakarta hanya untuk menulis Timer 25:00.
- **LO final (Bab 25)**: Terbitkan Void Saga 5 tahun sebelum Bab 25. Masih menikah dengan [DEDICATED PM]. [ANAK LO] usia 12.
- **Codex**: 5 volumes complete — Udara (♊♎♒), Air (♋♏♓), Api (♈♌♐), Tanah (♉♍♑), The Void.

---

## Aturan Kerja

1. **Read CLAUDE.md first.** Ini adalah handoff document. Future Claude sessions harus mulai dari sini.
2. **Verify, don't assume.** Cek file-system sebelum klaim sesuatu exist atau complete. Project ini bergerak cepat — CLAUDE.md bisa jadi artifact, tapi filesystem adalah source of truth.
3. **Respect the pipeline.** Jika bekerja di compiler/engine/runtime: pahami arsitektur dulu sebelum mengubah. Pipeline sudah proven dengan live Claude generation — jangan break yang sudah bekerja.
4. **Novel voice is Jali's.** Claude tidak menulis ulang prosa novel kecuali diminta eksplisit.
5. **Constraint extraction dari canon.** Saat membuat runtime baru, constraints harus diekstrak dari novel (Bab/Timer), bukan diinvent dari udara.
6. **Update CLAUDE.md** setelah perubahan signifikan: karakter baru, fakta baru, milestone baru, file baru. Tapi jangan biarkan membengkak kembali ke 1000+ baris. Simpan sebagai operational handoff — bukan sebagai archive.

---

## File Penting yang Harus Dibaca Saat Mulai Sesi Baru

| File | Why |
|------|-----|
| `README.md` | Project identity, demo commands, pipeline diagram |
| `QUICKSTART.md` | 10-minute walkthrough for new developers |
| `docs/30_MINUTE_CHALLENGE.md` | Developer Zero — the adoption litmus test |
| `VOID_SAGA_UNIVERSE/apps/engine/engine_v2.py` | Constraint engine |
| `VOID_SAGA_UNIVERSE/apps/compiler/compiler.py` | Narrative compiler |
| `VOID_SAGA_UNIVERSE/apps/runtime_sdk/README.md` | SDK tools reference |
| `VOID_SAGA_UNIVERSE/RUNTIME_AUTHORING_GUIDE.md` | The method — how to think about executable characters |
| `VOID_SAGA_UNIVERSE/EXECUTABLE_FICTION_MANIFESTO.md` | The paradigm |
| `VOID_SAGA_UNIVERSE/demo/PASS_niuniu_sevraya_orbit.md` | Bukti PASS — end-to-end pipeline |
| `VOID_SAGA_UNIVERSE/demo/BLOCKED_zero_emotional.md` | Bukti BLOCKED — safety gate |

---

*Last updated: 2026-06-26 — Developer Zero complete. 30-Minute Challenge live. Adoption track active.*
