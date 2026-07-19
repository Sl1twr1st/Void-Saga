# invariant-engine — an engine over behavioral invariants

> Most fictional universes are read. This one is checked.
> (The why, kept private: a machine that prays — every name invoked carries a cost. "Prayer Engine" is the soul; "invariant-engine" is what ships.)

---

## Current Identity

invariant-engine is a tool. It observes behavioral invariants in prose, serializes them, and tests new scenes for consistency — returning PASS / WARNING / PRICE REQUIRED / BLOCKED. One primitive: a behavioral pattern observed repeatedly becomes a candidate invariant. The engine serializes invariants, not entities.

Void Saga is **not** the project. Void Saga is the **first dataset** — the novel *Menatap Akhir Semesta dari Balik Kacamata Hitam*, being finished in parallel, and the universe that proved the engine runs. Band 8 (Aisya) is the second dataset.

**What this is NOT (honest, per `contra/`):**
- NOT a validated "research program" or "methodology" yet. Evidence is N=1 author, N=2 universes, both Jali's. Until a second writer uses it, this is an instrument built for one novel — not a proven method.
- NOT an "emergence detection engine" yet. Invariant extraction is currently manual; the automated extractor does name/POV/setting detection only. The claim is deferred until Phase 2 lands.

The novel is a real deliverable. The engine is a real tool. The methodology is a hypothesis. `contra/` holds the case against all three; read it when the internal story feels too clean.

**Research principle:** Nothing enters theory without evidence — including evidence against the theory.

---

## Current Milestone

**M1 — Canon sealing COMPLETE (2026-07-15).** `canon-v1.0.json` sealed: 65 dokumen (layers: bab/timer/codex/system, 3 artifacts excluded) dengan document_id, layer, pairing, sequence, source_hash. Toolchain di `tools/void_corpus/` (generate_candidate, seal_candidate, validate). Proofing pipeline di `proofing/` (registry + passA–E + divergence reports) — **masih untracked**, keputusan commit pending.

**Node reader spike PASSED (2026-07-17, `abe65b1`).** Canon terbukti jadi source of truth untuk consumer di luar dirinya: fork-ui sekarang node-aware (`?node=bab-00`, `?node=timer-00-00`), identity dari canon, experience metadata di `mvp/node-registry.json`, renderer per jenis dokumen (BabRenderer/TimerRenderer). Navigasi bab→timer di-derive dari `pair_document_id` + `sequence_narrative`. Ini spike, BUKAN full Phase 1 — full node reader (65 nodes) belum dimulai, sengaja. Log: `research/2026-07-17-canon-as-shared-dependency.md`.

**Boot screen = canonical threshold (2026-07-17, `1684928`).** Epigraph + SYSTEM REQUIREMENT dari `opening.md:27-35` tampil statis di atas boot log. Status jujur: **matched (verbatim copy), bukan consumed at runtime** — kalau opening.md berubah, boot screen diverge diam-diam. Kandidat consumer beneran di M2.

**Void.OS reading surface (2026-07-01).** fork-ui = canonical reading surface Void Saga, bukan blog/website. Doctrine: "Reader first, fork optional, engine always present." Boot → landing → read → fork/continue. `./scripts/fork-ui` → localhost:3720.

**fork-ui diegetic experience doctrine (ACTIVE, must-read before UX changes).** Untuk semua perubahan pada experience yang dimulai dari `./scripts/fork-ui`, baca **`docs/VOID_OS_DIEGETIC_EXPERIENCE.md`** dulu. Doktrin tertinggi:
- every screen must be spoken by the world, never by the software
- don't expose the engine; expose the world
- user = witness / investigator / testifier, bukan prompt writer atau operator AI
- retrieval harus tampil sebagai memory event, contradiction, judgment, consequence, atau residue — bukan telemetry aplikasi
- interview harus terasa sebagai cross-examination yang bereaksi pada testimony, bukan fixed wizard form

**Temporary MVP scope exception:** API Gate **bukan** target experience pass ini. Perlakukan API Gate sebagai **operator console** untuk rapid provider switching, prompt iteration, provider comparison, dan generation debugging. Jangan redesign/hide/replace API Gate pada pass ini; tandai semua issue di dalamnya sebagai **DEFERRED (Operator Layer)**. Fokus diegetic pass sekarang hanya pada: Boot, Landing, Reader, Segment Selection, Witness Registration, Interview, Translation, dan Verdict.

**Capability honesty guard:** Before changing fork-ui interaction or copy, verify that every world-facing claim is supported by an actual runtime capability. Diegetic framing may dramatize; it may not fabricate engine behavior.

**Capability promotion guard:** Before promoting any new world event into fork-ui, verify its capability status in **`docs/VOID_OS_DIEGETIC_EXPERIENCE.md`**. Reserved Theatre may not appear as live world behavior until the corresponding engine state exists, is exposed, and is verified.

Gunakan checklist sebelum mengubah copy/UI/flow fork-ui: siapa yang berbicara (dunia atau developer), apakah user menjalani ritual atau mengoperasikan tool, apakah engine terlihat, apakah retrieval dipentaskan sebagai memory, apakah pertanyaan lahir dari testimony + canon, apakah output terasa sebagai consequence/residue, dan apakah layar ini membuat user semakin lupa sedang memakai software.

**NEXT: M2 — Second Canon Consumer.** Exit criterion: Evidence Engine membaca canon — invariant/runtime citations resolve ke `document_id` + `source_hash`, bukan path markdown mentah. Satu consumer baru, tanpa perubahan canon. Nama "Canon Consumer Platform" (usulan Jali 2026-07-17) masih pending — kata "platform" baru dipakai setelah ≥2 consumer independen jalan. Search/Timeline/Glossary BUKAN deliverable M2.

**M2 contract decision (2026-07-17, sealed):** **canonical provenance = bagian dari engine contract** — Evidence tanpa provenance tidak lagi sah. Sidecar resolver DITOLAK karena topologi: resolver yang jadi consumer, engine tetap hidup tanpa canon → melanggar exit criterion. Ini BUKAN "schema change accepted" — implementation strategy masih OPEN (runtime/Evidence/Citation object, adapter, migration layer); standing rule "Do NOT change schema" tetap berlaku sampai strategy dipilih. Basis evidence: `research/2026-07-17-provenance-loss-trace.md` (identitas canon tidak pernah masuk pipeline; 122 sitasi free-text di 4 kelas; `forbidden_behaviors` tanpa sitasi sama sekali; `constraints.py:402-412` membuang sitasi dari violation) → `research/2026-07-17-citation-residence-decision.md` (matrix + verdict).

**Formal debt:** fork layer (fork records, interview, checker) masih pakai id lama `bab00`; canon pakai `bab-00`. Migrasi wajib sebelum Fork Engine jadi consumer canon. Jangan disentuh sambil lalu — ripple besar.

Roadmap fase lama (derived from `contra/2026-06-27-contra-week-one.md`):
- **Fase 0 — Identity (done):** project = invariant-engine; Void Saga = dataset. (kills contra #5)
- **Fase 0.5 — Bab 00 Fork MVP (done):** genesis node, 7 laws, fork points, demo forks, CLI checker.
- **Fase 1 — Finish & seal the novel.** Canon v1.0 sealed = prosa beku tersegel. Novel itu sendiri: in progress.
- **Fase 2 — Replace the manual extractor** with LLM-based invariant extraction + citations. (kills contra #1)
- **Fase 3 — One second writer in 90 days,** or downgrade "methodology". (kills contra #3)
- **Fase 4 — Real confidence (held-out validation) or drop the number.** (kills contra #2)

**KEEP:** novel, PRICE REQUIRED, Batman/Mr. Bean framing, evidence discipline.
**STOP (noise):** schema v3, serializing remaining Void Saga characters, OPEN_QUESTIONS architecture — premature until Fase 2–3 land. (kills contra #4)

GUA/LO runtimes remain Draft.

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

### Fork MVP (Bab 00 — Genesis Node Forkability)

`mvp/` — Minimal viable demo proving Bab 00 can serve as a genesis node that is forkable.

| Artifact | File | Description |
|----------|------|-------------|
| Genesis Node | `mvp/genesis/bab00.node.json` | Bab 00 metadata as source node (10 sub-chapters, 3 characters, 3 mechanisms) |
| Fork Points | `mvp/genesis/fork-points.json` | 3 forkable moments in Bab 00 (fp-001: Bug Janggal, fp-002: Folder Error, fp-003: Genesis Error) |
| Law Mapping | `mvp/laws/bab00-laws.json` | 7 Bab 00 laws with block_on_violate / price_on_violate flags |
| Fork Records | `mvp/forks/fork-01-pass.json`, `fork-02-price.json`, `fork-03-blocked.json` | 3 example forks with full lineage |
| Fork Checker | `mvp/checker/check_fork.py` | Rule-based verdict engine (PASS / PRICE_REQUIRED / BLOCKED / VALID_FORK) |
| CLI Wrapper | `scripts/check-fork` | Entry point: `./scripts/check-fork path/to/fork.json` |

**3 example forks:**
1. 🟢 PASS — GUA hesitates 15 seconds, then lets LO sit. Laws intact.
2. 🟡 PRICE_REQUIRED — GUA rejects LO. Sync severed. Stealth Project becomes monologue.
3. 🛑 BLOCKED — VoidOS forces installation without consent. Consent architecture collapses.

**Verdict logic:**
- Law with `block_on_violate: true` violated → BLOCKED (exit 2)
- Law with `price_on_violate: true` violated → PRICE_REQUIRED (exit 3)
- No violations, trivial change → PASS (exit 0)
- No violations, meaningful divergence → VALID_FORK (exit 0)

**North Star:** "Fork Bab 00. Break canon. Pay the price. Continue the universe."

### How to Run Demo

```bash
# Fork MVP — check Bab 00 forks
./scripts/check-fork mvp/forks/fork-01-pass.json      # PASS
./scripts/check-fork mvp/forks/fork-02-price.json     # PRICE_REQUIRED
./scripts/check-fork mvp/forks/fork-03-blocked.json   # BLOCKED

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

### Theory Track (current — do not skip)

1. **Validate across universes** — extract Draft Runtimes from 2+ more independent stories (different genres, different authors). Does the same mechanism detect behavioral invariants?
2. **Answer OPEN_QUESTIONS** — especially: Is Relationship Contract a first-class artifact? Is Runtime just one serialization target? Does confidence belong to the invariant?
3. **Schema v3.0** — only after theory settles. Candidates: per-invariant confidence, maturity levels, contract as artifact type.

### Adoption Track (paused until theory settles)

1. First External Universe — paused. Aisya is the internal proof. External proof waits for theory stability.
2. First External Contributor — paused.
3. v0.3.0 — paused.

### Technical Track (background)

- CLI packaging (`void-saga compile`, `void-saga validate`)
- Engine hardening (performance, error handling)
- Markdown extractor improvements (AI-powered extraction, multi-language constraint matching)

### What NOT to do right now

- Do NOT commit GUA/LO runtimes — theory hasn't settled. They will need refactoring.
- Do NOT change schema — OPEN_QUESTIONS may change the root abstraction.
- Do NOT serialize remaining Void Saga characters (Agnia, Hasan, etc.) — the theory may change HOW they should be serialized.
- Do NOT build Pattern Detector — the theory of observation must come before the engineering of extraction.
- Do NOT add more worldbuilding, web app, new chapter writing as immediate next step.

---

## Peran Claude dalam project ini

Project ini sudah melewati fase "Jali nulis chapter → Claude baca → Claude kasih feedback." Mode operasi sekarang:

1. **Research partner** — bantu observasi behavioral pattern dari prosa, propose candidate invariant dengan citation, review melawan evidence. Ini prioritas utama.
2. **Lab notebook keeper** — catat decision log di `research/` saat teori berubah arah. Bukan dokumentasi — provenance.
3. **Domain classifier** — setiap perubahan harus diklasifikasikan: milik Executable Fiction (paradigm) atau Void Saga (reference implementation)?
4. **Compiler co-developer** — pahami engine, compiler, constraint system. Tapi implementasi nunggu teori stabil.
5. **Cermin** — kasih tahu Jali apa yang sebenarnya sedang dibangun (seperti dulu kasih tahu apa yang sebenarnya ditulis)
6. **Bukan editor gaya** — jangan ubah suara. Jali punya tone sendiri. Tugas memperjelas, bukan menghaluskan paksa.

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
| `canon-v1.0.json` | **The canon.** Sealed 2026-07-15. Identity source of truth: document_id, layer, pairing, sequence, source_hash untuk semua dokumen prosa. |
| `tools/void_corpus/` | Canon toolchain: generate_candidate, seal_candidate, validate, models. |
| `mvp/node-registry.json` | Experience metadata (UI-only) per node, keyed by canon document_id. Identity JANGAN di-copy ke sini. |
| `scripts/fork-ui` | **Void.OS reading surface + fork interview.** Node-aware (`?node=`), canon-backed. localhost:3720. |
| `research/2026-07-17-canon-as-shared-dependency.md` | Spike log: canon as shared dependency, M2 guardrails, formal debt bab00→bab-00. |
| `docs/BEHAVIORAL_INVARIANTS.md` | **The theory.** Primitive = repeated observation. Compiler serializes invariants, not entities. |
| `docs/OBSERVE_PIPELINE.md` | **The method.** Observe → Propose → Review → Serialize → Evolve. |
| `docs/OPEN_QUESTIONS.md` | **The research agenda.** Five open questions. None answered. |
| `research/INDEX.md` | **The lab notebook index.** Timeline of idea evolution. Which decisions are settled, which are open. |
| `README.md` | Project identity, demo commands, research principle |
| `QUICKSTART.md` | 10-minute walkthrough for new developers |
| `mvp/README.md` | **Fork MVP.** Bab 00 genesis node, fork points, law mapping, 3 demo forks, checker CLI |
| `scripts/check-fork` | Writer CLI — check Bab 00 fork verdict (PASS/PRICE_REQUIRED/BLOCKED/VALID_FORK) |
| `scripts/check-scene` | Writer CLI — markdown → extractor → compiler → PASS/WARNING/BLOCKED |
| `scripts/triage-scenes` | Batch classifier — PASS/WARNING/BLOCKED table |
| `VOID_SAGA_UNIVERSE/apps/engine/engine_v2.py` | Constraint engine |
| `VOID_SAGA_UNIVERSE/apps/compiler/compiler.py` | Narrative compiler |
| `VOID_SAGA_UNIVERSE/apps/data/runtimes/Aisya.runtime.json` | First non-Void-Saga Draft Runtime (confidence 0.35) |
| `experiments/EXP-001-aisya/README.md` | **Current experiment.** Phase A (extraction) + Phase B (noise robustness) + Phase C (planned). |
| `VOID_SAGA_UNIVERSE/demo/PASS_niuniu_sevraya_orbit.md` | Bukti PASS — end-to-end pipeline |
| `VOID_SAGA_UNIVERSE/demo/BLOCKED_zero_emotional.md` | Bukti BLOCKED — safety gate |

### Uncommitted Research Artifacts

| File | Status |
|------|--------|
| `VOID_SAGA_UNIVERSE/apps/data/runtimes/GUA.runtime.json` | Draft extracted. Held for theory settlement. |
| `VOID_SAGA_UNIVERSE/apps/data/runtimes/LO.runtime.json` | Draft extracted. Held for theory settlement. |
| `dogfood/test_gua_lo_orbit_pass.json` | GUA-LO contract scenario. Held. |
| `dogfood/test_gua_lo_blocked_silence.json` | GUA blocked scenario. Held. |

---

*Last updated: 2026-07-17 — M1 canon sealing complete (canon-v1.0.json). Node reader spike passed: canon proven as source of truth for node-aware reader (`?node=`, node-registry, renderer abstraction). Boot screen matches novel opening verbatim. NEXT: M2 — second canon consumer (Evidence Engine reads canon).*
