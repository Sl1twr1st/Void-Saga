# TASK 6D OUTPUT — Claude API Integration Safe Mode

> **Status:** COMPLETE
> **Date:** 25 June 2026

---

## What Was Built

Real Claude API integration with safety gates intact.

### Safety Architecture

```
scenario.json
    │
    ▼
engine_v2 evaluate
    │
    ├── hard_block → BLOCKED (no API call)
    │
    └── PASS/WARNING
        │
        ├── --live + ANTHROPIC_API_KEY set → Claude API
        │   └── post-generation validation via engine_v2
        │
        └── default (no --live) → dry-run stub
```

### Key Safety Features

1. **Default is dry-run.** `--live` flag required for API calls. Accidental runs cost nothing.
2. **API key from env only.** `ANTHROPIC_API_KEY` environment variable. Never hardcoded. Never in config files.
3. **Hard block gate preserved.** Forbidden behaviors, contract violations, anti-gravity → no API call.
4. **Post-generation validation.** Generated narrative is re-evaluated through engine_v2. Violations in generated output are detected.
5. **Graceful degradation.** Missing API key → `api_error` mode with clear message. Missing `anthropic` package → clear error.

### New Functions

| Function | Purpose |
|----------|---------|
| `_get_api_key()` | Read ANTHROPIC_API_KEY from env |
| `generate_via_claude(prompt)` | Call Claude API, return raw output or error |
| `validate_generated_output(output, scenario)` | Parse JSON, re-run engine on generated narrative |

### Generation Modes

| Mode | Trigger | API Called |
|------|---------|------------|
| `dry_run` | Default (no --live) | No |
| `live` | --live + API key | Yes |
| `api_error` | --live but no key/package | No |
| `validation_error` | --live but output not valid JSON | Yes (but output rejected) |
| `blocked` | Hard block gate | No |

## Test Results

| Test | Mode | Result |
|------|------|--------|
| Default (no flags) | canon_safe dry_run | Stub generated ✅ |
| --live (no API key) | api_error | Graceful error ✅ |
| --live VIOLATION (zero emotional) | blocked | Hard block, no API call ✅ |
| --dry-run PASS | dry_run | Full prompt printed ✅ |

## CLI

```bash
# Default: dry-run stub (safe, no API cost)
python compiler.py scenario.json

# Print full LLM prompt
python compiler.py scenario.json --dry-run

# Real generation (requires ANTHROPIC_API_KEY)
python compiler.py scenario.json --live

# Machine output
python compiler.py scenario.json --json
```

## Files Modified

| File | Change |
|------|--------|
| `apps/compiler/compiler.py` | Added `generate_via_claude()`, `validate_generated_output()`, `--live` flag, post-gen validation |

## Integration Ready

When `ANTHROPIC_API_KEY` is set:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python compiler.py scenario.json --live
```

The compiler will:
1. Gate on engine constraints
2. Build full prompt contract
3. Call Claude API
4. Parse JSON output
5. Re-validate through engine
6. Return scored narrative
