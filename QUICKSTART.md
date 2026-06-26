# Quickstart — 10 Minutes to Aha

You will run two commands.
After the second one, you will understand what Executable Fiction is.

---

## Prerequisites

- Python 3.8+
- No API key required for this quickstart.

---

## Step 1 — Clone

```bash
git clone https://github.com/your-org/Void-Saga.git
cd Void-Saga
```

---

## Step 2 — PASS

Run the compiler on a canon-valid scenario:

```bash
./scripts/demo-pass
```

Expected output:

```
✅  PASS
   Canon score:  1.0
   Final verdict: PASS
   Canon verdict: CANON_PASS

Congratulations.

You have just used a Narrative Compiler.

The compiler loaded character runtimes, evaluated constraints,
scored canon compliance, and approved this scenario for generation.
No LLM was called. The universe decided first.
```

---

## Step 3 — BLOCKED

Now try a scenario that violates canon:

```bash
./scripts/demo-blocked
```

Expected output:

```
🛑 GENERATION BLOCKED
   Reason: Hard block: 1 critical violation(s) detected.
   Hard blocks: 1
     🚫 [forbidden_behavior] Forbidden behavior violated:
        Making Zero emotional, warm, or personally attached to anyone.
   Canon score: 0.97
```

---

## What just happened?

Two commands. Two outcomes.

Same compiler. Different scenarios.

The first scenario passed because it respected the character's constraints — NiuNiu and Sevraya in their established orbit, no violations.

The second scenario tried to make Zero emotional. Zero's runtime forbids this. Canon score was 0.97 — nearly perfect — but the constraint was **hard**. No exceptions. Claude API was never called.

```
Scenario JSON
      │
      ▼
Runtime Loader          ← loads character constraints, voice, sigils
      │
      ▼
Constraint Engine       ← checks forbidden behaviors, invariants
      │
      ▼
Contract Engine         ← checks relationship rules
      │
      ▼
Canon Score             ← 0.0–1.0 alignment with canon
      │
      ▼
Hard Block Gate         ← violations stop here. No LLM called.
      │
      ├──────────────┐
      ▼              ▼
 BLOCKED       Prompt Contract → Claude API → Validated Narrative
```

**The LLM is not the authority. The universe is.**

---

## Step 4 — Read a Runtime

Open a character file:

```bash
cat VOID_SAGA_UNIVERSE/apps/data/runtimes/Zero.runtime.json
```

You'll see the `forbidden_behaviors` array — including the exact rule that blocked the second scenario.

Every constraint the compiler enforces lives in these files. They are readable JSON. You can add, remove, or modify them.

---

## Step 5 — Run with Claude (optional)

If you have an Anthropic API key:

```bash
export ANTHROPIC_API_KEY=your-key-here

python3 VOID_SAGA_UNIVERSE/apps/compiler/compiler.py \
  VOID_SAGA_UNIVERSE/apps/engine/scenarios_v2/test_niuniu_sevraya_orbit.json \
  --live
```

The compiler will pass the canon-validated scenario to Claude and return generated prose. Post-generation validation runs automatically.

---

## What's next?

| I want to… | Go to… |
|------------|--------|
| **Build my own character in 30 min** | **[30-Minute Challenge](docs/30_MINUTE_CHALLENGE.md)** |
| Understand the full pipeline | `README.md → What just happened?` |
| Build a character with the full SDK | `VOID_SAGA_UNIVERSE/apps/runtime_sdk/README.md` |
| Write a new scenario | `VOID_SAGA_UNIVERSE/apps/engine/scenarios_v2/` (copy any existing file) |
| Read saved execution outputs | `VOID_SAGA_UNIVERSE/demo/` |
| See the runtime schema | `VOID_SAGA_UNIVERSE/apps/schema/RUNTIME_SCHEMA_V2.1.json` |

---

*If something doesn't run, check that you're in the repo root and Python 3 is available. No pip installs required for the dry-run path.*
