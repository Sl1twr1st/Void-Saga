# START HERE — Fork Bab 00

You are about to fork the opening chapter of the Void Saga universe. Forking means: take a moment in the story, change it your way, and see whether the universe's laws allow it — PASS, VALID FORK, PRICE REQUIRED, or BLOCKED.

You never edit JSON. You answer questions in your own words.

## Do this

1. **Read the chapter:** [`input/bab-00.md`](input/bab-00.md)
2. **Run the tool** (from the repo root):

   ```bash
   ./scripts/start-fork
   ```

   It asks your name, then a few questions. Answer in plain language. Your answers are saved to `mvp/runs/<your-name>/answers.md`.

3. **Translate (still manual):** right now, Jali or Claude turns your answers into a fork record at `mvp/runs/<your-name>/fork-record.json`. **This is the only step that is not automated yet** — it is the gate the project is working toward closing.

4. **Check the fork:**

   ```bash
   ./scripts/check-fork mvp/runs/<your-name>/fork-record.json
   ```

   You get a verdict against the 7 Bab 00 laws.

## The flow, honestly

```
You answer in prose
        ↓   ./scripts/start-fork
answers.md  (yours, untouched)
        ↓   TRANSLATE — still manual (Jali/Claude)   ← the Fase 2 gate
fork-record.json
        ↓   ./scripts/check-fork
Verdict: PASS / VALID_FORK / PRICE_REQUIRED / BLOCKED
```

The whole point of this version is to make that one manual step **visible** — so we can see exactly where the writer stops being able to do it alone.
