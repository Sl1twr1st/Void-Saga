# Sprint 01 — Discover Questions

> Minggu 1. Phase 0 complete (governance).
>
> Target: **Intent Library v0.1** — bukan interview flow, bukan daftar pertanyaan.
>
> Kita tidak membangun state machine. Kita menemukan intent di balik pertanyaan yang membuka cerita.

---

## Why This Sprint Exists

Phase 0 memberi kita governance. Sekarang kita tahu **bagaimana** project berkembang.

Hipotesis dari discovery:

| H | Claim |
|---|-------|
| H1 | Writers come to the runtime when blocked, not when writing fluently. |
| H2 | Question quality = generativity (does it open space?), not precision (does it narrow?). |
| H3 | Narrow-scope generative questions outperform wide-scope ones for blocked writers. |

Untuk menguji ini, kita butuh objek yang bisa diukur.

**Objek itu bukan pertanyaan — tapi intent di balik pertanyaan.**

Satu intent bisa punya banyak wording (variant). Kalau satu wording jelek, intent-nya tetap valid. Kalau objek penelitian = wording, dataset cepat kotor. Kalau objek penelitian = intent, kita bisa A/B test wording.

---

## Research Unit Hierarchy

```
Story Problem
        │
        ▼
Question Intent        ← unit penelitian
        │
        ▼
Question Variant       ← wording — bisa A/B/C
        │
        ▼
Interview Session      ← evidence disimpan di sini
        │
        ▼
Evidence               ← continued? time to next idea?
```

### Mirror: same pattern as invariant pipeline

```
Observation → Pattern → Candidate Invariant → Accepted Invariant
     │              │                │
     ▼              ▼                ▼
Interview      Observed        Candidate        Validated
Session        Effect          Question         Question
```

---

## Sprint Deliverable

### Intent Library v0.1

```
mvp/questions/
    _TEMPLATE.md              ← pointer to new structure
    _TEMPLATE_INTENT.md        ← template for intent files
    intents/
        opening/
            clarify-intent.md        ← 1 session evidence (dogfooding)
            surface-stake.md         ← 1 session evidence (dogfooding)
            hidden-motivation.md     ← 0 sessions (untested)
            narrow-lens.md           ← 0 sessions (untested)
        structuring/
            duration.md              ← 1 session evidence (dogfooding)
            immediate-consequences.md ← 1 session evidence (dogfooding)
            canon-gravity.md         ← 1 session evidence (dogfooding)
        law-aware/                   ← empty (Sprint 3)
        recovery/                    ← empty (Sprint 4)
    sessions/
        _TEMPLATE.md                 ← template for session records
        2026-06-28-001.md            ← dogfooding session (6 steps, all YES)
```

### Each intent is a research object

```yaml
id: opening-001
name: Clarify Intent
purpose: Disambiguate "what if..." into specific behavioral change.
hypothesis: H2
variants: [A, B, C]  ← multiple wordings, same intent
total_sessions: N
best_variant: B
```

### Each variant is independently measurable

| Variant | Wording | Sessions | Continue Rate | Median TTI |
|----------|---------|----------|---------------|------------|
| A | "Apakah [X] mengabaikan, menolak, atau tidak menyadari?" | 8 | 83% | 18s |
| B | "Apa yang sebenarnya ingin [X] hindari?" | 5 | 60% | 41s |
| C | "Kalau [X] tidak merespons, keputusan apa yang dia ambil?" | 7 | 71% | 17s |

### Each session is an evidence record

```yaml
session_id: 2026-06-28-001
writer: Jali
blocked_state: YES
steps:
  - intent: opening-001, variant: A, continued: YES, tti_ms: 18000
  - intent: opening-002, variant: A, continued: YES, tti_ms: 9000
  ...
```

---

## Primary Metric: Time To Next Idea

Bukan: *Continue Rate* (YES/NO).

Tapi: **Time To Next Idea (TTI)** — berapa milidetik dari pertanyaan selesai sampai penulis mulai menghasilkan ide baru?

| Question | Median TTI |
|----------|------------|
| opening-002 (surface-stake) | 9s |
| structuring-003 (canon-gravity) | 8s |
| structuring-001 (duration) | 12s |
| structuring-002 (consequences) | 14s |
| opening-001 (clarify-intent) | 18s |

Data dari 1 sesi. Perlu 20 sesi untuk mulai melihat pola. Tapi arahnya sudah menarik: stake dan canon-gravity paling cepat. Clarify-intent (yang strukturnya A/B/C) paling lambat — possible karena struktur multiple-choice butuh processing time, atau karena dia pertanyaan pertama.

TTI langsung nyambung ke hipotesis inti: **pertanyaan mana yang paling cepat mengembalikan imajinasi?**

---

## Target

**20 interviews completed. Bukan 20 forks.**

- 8 menghasilkan fork record valid.
- 5 berhenti di tengah.
- 4 ternyata bukan fork (eksplorasi tanpa perubahan struktural).
- 3 berubah jadi ide baru di luar Bab 00.

**Semuanya data.**

Kalau kita hanya menghitung fork yang jadi, kita kehilangan evidence paling berharga: di mana proses berpikir macet.

---

## What We Do NOT Build

- ❌ Interview flow / state machine
- ❌ Adaptive branching (Sprint 2)
- ❌ Law-aware questions (Sprint 3)
- ❌ Conversation memory (Sprint 4)
- ❌ NL → Fork Record compiler (Sprint 5)
- ❌ Web UI
- ❌ Any change to checker or laws

---

## Exit Criteria

Sprint 1 selesai ketika:

- [ ] 20 interview sessions completed and logged
- [ ] ≥3 intents have ≥5 sessions each (enough to start comparing variants)
- [ ] TTI data collected for all sessions
- [ ] Initial patterns: which intents have lowest median TTI? Which variants within an intent perform best?
- [ ] ≥10 sessions produce valid Fork Records
- [ ] H1 data: what % of sessions started from blocked state?
- [ ] Decision: proceed to Sprint 2 OR revise intent set and re-run

---

## What Falsifies This Sprint

- **All intents have median TTI > 60s** → no question consistently restarts thinking. The unblocking hypothesis may be wrong.
- **No pattern across intents** → question effectiveness is purely idiosyncratic. Intent library cannot generalize.
- **<5 Fork Records valid** → intents don't produce enough structure. Structuring intents insufficient.
- **Variant performance is random** → wording matters more than intent. Unit of research should be wording, not intent.

---

## Phase 0 Context

Sprint ini adalah sprint pertama setelah Phase 0 (governance: `PRODUCT_RESEARCH_OPERATING_MODEL.md`).

Golden rule berlaku: setiap intent harus meningkatkan pengalaman Bab 00 sebelum berhak jadi platform feature.

Research may influence sprint priorities, but product milestone (Bab 00 forkable in 30 days) remains fixed.

---

*Sprint 01 — Discover Questions. Minggu 1. Deliverable: Intent Library v0.1. Metric: Time To Next Idea. Target: 20 interviews.*
