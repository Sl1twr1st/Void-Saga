# START HERE — Fork Bab 00

You are about to fork the opening chapter of the Void Saga universe. Forking means: take a moment in the story, change it your way, and see whether the universe's laws allow it — PASS, VALID FORK, PRICE REQUIRED, or BLOCKED.

You never edit JSON. You answer questions in your own words.

## Two ways in

### Way A — Terminal (script)

```bash
./scripts/start-fork
```

Minimal. Works. Feels like running a tool.

### Way B — Web UI (local)

```bash
./scripts/fork-ui
```

Opens a local web page. Same questions. Same output. Feels like entering a universe.

Both produce the same `answers.md` in `mvp/runs/<your-name>/`.

## The flow

```
You answer in prose
        ↓   ./scripts/start-fork   OR   ./scripts/fork-ui
answers.md  (yours, untouched)
        ↓   TRANSLATE — still manual (Jali/Claude)   ← the Fase 2 gate
fork-record.json
        ↓   ./scripts/check-fork
Verdict: PASS / VALID_FORK / PRICE_REQUIRED / BLOCKED
```

The whole point of this version is to make that one manual step **visible** — so we can see exactly where the writer stops being able to do it alone.

## After your fork is checked

If your verdict is PRICE REQUIRED, the universe permits your divergence but asks for narrative cost. Read the fork record's `price` field to see what you owe.
