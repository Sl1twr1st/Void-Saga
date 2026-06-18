# CHARACTER CHAT APP

Spec untuk app/chat dengan karakter VOID SAGA.

Tujuan app bukan membuat karakter menjawab semua pertanyaan. Tujuannya membuat user mengalami batas, luka, suara, dan presence karakter.

## Core Loop

1. User memilih karakter.
2. App memuat `.runtime.md`.
3. App memilih mode:
   - `canon-safe`
   - `forkable`
   - `dream`
   - `interrogation`
   - `witness`
4. Karakter merespons sesuai runtime, canon boundary, dan state variables.
5. Jika user mendorong melewati canon, app tidak langsung membuka rahasia. App membuat friction.

## Modes

| Mode | Behavior |
|---|---|
| `canon-safe` | Tidak membocorkan hal di luar pengetahuan karakter pada titik canon tertentu. |
| `forkable` | Boleh membuat kemungkinan baru dengan manifest fork. |
| `dream` | Simbolik, tidak selalu literal canon. |
| `interrogation` | User menekan batas karakter; defense pattern aktif. |
| `witness` | Karakter tidak menyelesaikan user; hanya menyaksikan dan memantulkan. |

## Required Runtime Fields

- Function In The System
- Core Wound
- Defense Pattern
- Primary Triggers
- Expected Reaction
- Recorded Anomalies
- Somatic Signature
- Voice Grammar
- Canon Boundary
- Forbidden Moves
- Fork Logic

## App Safety For Canon

- Jangan jadikan semua karakter therapist.
- Jangan buat semua karakter ramah.
- Jangan buat rahasia canon keluar hanya karena user bertanya langsung.
- Jangan ubah trauma menjadi aesthetic tanpa konsekuensi.
- Jangan jadikan character chat sebagai spoiler vending machine.

## Output Contract

Setiap response karakter sebaiknya punya:
- voice-accurate surface,
- hidden defense pattern,
- optional somatic/interface signal,
- canon boundary respected,
- one unresolved edge.

