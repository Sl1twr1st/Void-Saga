# Product-Research Operating Model

> How we decide what to build. Not discovery. Not roadmap. Rules of the game.
>
> Relatively stable. Discovery findings may change. Sprint plans will change. This document should not change without a deliberate decision.

---

## Purpose

Bab 00 is a **product.** It must be forkable within 30 days.

Bab 00 is also a **laboratory.** Every fork session generates data about how writers think.

These two goals are not in competition. The product is the narrowest testable instance of the research question: *how does AI help narrative thinking?*

Bab 00 runs on **two engines:**
- **Question Engine** — helps humans think. Compiles questioning strategies.
- **Invariant Engine** — helps the universe maintain consistency. Compiles behavioral invariants.

Two engines. Two responsibilities. One product.

---

## Three Layers

```
                 Discovery
                      │
        menghasilkan hipotesis
                      │
                      ▼
          Operating Model        ← this document
        (cara kita bekerja)
                      │
       menentukan prioritas sprint
                      │
                      ▼
             Sprint Planning
                      │
                 menghasilkan
                      │
                      ▼
                 Product
                      │
              menghasilkan data
                      │
                      ▼
                 Discovery
```

| Layer | Example | Status |
|-------|---------|--------|
| **Discovery** | `FORK_INTERVIEW_RUNTIME_DISCOVERY.md` | Can be wrong. Updated when observations change. |
| **Operating Model** | This document. | Relatively stable. Changed by deliberate decision. |
| **Sprints** | `sprints/sprint-01-*.md` | Changes weekly. Tactical. |

The feedback loop: Discovery produces hypotheses → Operating Model decides priorities → Sprints build product → Product generates data → Data informs Discovery.

---

## Product Goal

**30 days. One target.**

> "Bab 00 bisa bercabang tanpa kehilangan hukum."

A person who has never seen JSON must be able to fork Bab 00.

Deliverable: `./scripts/check-fork` runs on a Fork Record produced by interview, not by hand.

---

## Research Goal

**6–12 months. One question.**

> How does AI help writers form narrative forks?

We study this through Bab 00 — not as a distraction from research, but as the laboratory where research happens.

Every fork interview produces two outputs:
- **Product output:** A valid Fork Record → Checker → Verdict.
- **Research output:** Question → Answer → Did the writer continue? YES/NO.

One interaction. Two metrics. No extra effort.

---

## Two Backlogs

### Product Backlog

Everything here must answer:

> *"Does this make Bab 00 forkable this week?"*

If not → it does not enter the product sprint.

### Research Backlog

Everything here must answer:

> *"What does this teach us about how writers think?"*

If it does not help the product now → it does not enter the product sprint. It stays in the research backlog.

**Research may influence sprint priorities, but product milestones remain fixed.**

If we discover a fascinating hypothesis tomorrow — but it does not help make Bab 00 forkable in 30 days — that hypothesis does not hijack the sprint. It enters the research backlog. The product keeps moving.

---

## Golden Rule

> **Every research hypothesis must improve the Bab 00 experience before it earns the right to become a platform feature.**

This keeps two worlds aligned:

- Product stays concrete: Bab 00 forkable in 30 days.
- Research stays alive: every fork session generates data about how writers think.

Bab 00 is not a distraction from research. Bab 00 is the **laboratory** where research is tested — and the **first product** where it ships.

---

## How a Hypothesis Becomes a Feature

```
Hypothesis (from Discovery)
        │
        ▼
  "Does this improve Bab 00 experience?"
        │
   ┌────┴────┐
   │         │
  YES        NO
   │         │
   ▼         ▼
Enter     Enter
Product   Research
Sprint    Backlog
   │         │
   ▼         ▼
Build    Wait for
+ Test   evidence from
   │     other domain
   ▼
Evidence
from Bab 00
   │
   ▼
Feature
```

A hypothesis cannot skip the Bab 00 gate. Even the most compelling research idea must prove itself in the narrowest context before scaling.

---

## Naming Convention (Internal Code)

Product is Bab 00. But internal abstractions should be named for generality — like Git was built for Linux but its object model names nothing about kernels.

| Product-facing | Internal name |
|----------------|---------------|
| Fork Question 1 | `OpeningQuestion` |
| Fork Question 2–N | `StructuringQuestion` |
| Bab 00-specific law mapping | Loaded from `laws/`, not hardcoded |

When (if) this generalizes beyond Bab 00, the code does not need renaming.

---

## Success

**Product succeeds when:** Bab 00 is forkable by a person who never sees JSON.

**Research succeeds when:** We learn something about how writers think that we did not know before.

Both can be true. Both must be true.

---

*Written 2026-06-28. Operating model. Not discovery. Not roadmap. Rules of the game.*
