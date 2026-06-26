# Dogfood — Scene Triage Workspace

Taruh scenario JSON di sini. Jalankan triage. Ambil keputusan.

## Loop Harian

```bash
# 1. Tulis 3-5 ide scene sebagai .json
#    Nama file deskriptif, bukan scene_01:
vim dogfood/niuniu_mengamati.json
vim dogfood/sevraya_zero_berbicara.json
vim dogfood/julia_kembali_ke_dayan.json

# 2. Triage
./scripts/triage-scenes dogfood

# 3. Lihat tabel
# 🟢 PASS  → tulis hari ini di writing/
# 🟡 WARNING → cek timeline/proximity/stage
# 🔴 BLOCKED → simpan, ini outline chapter berikutnya

# 4. Pindahkan BLOCKED ke future/
mkdir -p dogfood/future
mv dogfood/scene_yang_blocked.json dogfood/future/
```

## Format Cepat

Copy dari `drafts/scenarios/pass_example.json`, ganti:
- `scenario_id`
- `participants`
- `requested_action.description`
- `requested_action.type` (pakai `speak` untuk aman)

Referensi lengkap: `drafts/scenarios/README.md`

## Empat Layer

```
Canon      (Bab / Timer)         ← apa yang sudah benar
    ↑
Decision   (dogfood + compiler)  ← apa yang layak ditulis hari ini
    ↑
Drafting   (writing/)            ← menulis
    ↑
Publication (Bab / Timer baru)   ← derived from writing/
```

Compiler adalah editor pertama. Editor manusia datang setelahnya.
