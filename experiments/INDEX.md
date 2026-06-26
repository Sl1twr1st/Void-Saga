# Experiments — Executable Fiction Research

> Theory → Method → Experiment → Measurement → Theory Revision

Each experiment tests a specific hypothesis using the Observe Pipeline methodology.

## Active Experiments

| ID | Question | Dataset | Status |
|----|----------|---------|--------|
| EXP-001 | Can behavioral invariants emerge from 5 chapters of contemporary realist prose? | Aisya (Band 8, 5 chapters) | ✅ Complete |
| EXP-002 | Can invariants emerge from 25 chapters of meta-narrative prose written without Executable Fiction intent? | GUA-LO (Void Saga Bab-level, 25 chapters) | ✅ Complete |
| EXP-003 | — | — | 🔬 Planned |

## Measurement

All experiments contribute to the confidence convergence graph:

```
Confidence
  1.0 │
      │
  0.8 │                                    ○ GUA (25 ch)
      │
  0.6 │
      │
  0.4 │              ○ LO (25 ch)
      │    ○ Aisya (5 ch)
  0.2 │
      │
  0.0 ┼─────┬─────┬─────┬─────┬─────
      0     5    10    15    20    25
                  Chapters
```

Hypothesis: confidence converges toward 1.0 as chapter count increases. Each new experiment adds a data point.

## Experiment Template

```
experiments/EXP-NNN-name/
  README.md         — Question, Hypothesis, Method, Result, Conclusion
  dataset/          — Source prose (symlinks or copies)
  runs/             — Observation history
    2026-XX-XX-observe.json
    2026-XX-XX-observe.json
  artifacts/        — Serialized invariants (if any)
  notes.md          — Free-form observations during experiment
```
