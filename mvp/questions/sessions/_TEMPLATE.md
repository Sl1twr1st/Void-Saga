# Session Template

```yaml
session_id: <YYYY-MM-DD-NNN>
writer: <name>
fork_point: <fp-001 | fp-002 | fp-003>
writer_input: "<what if...>"
blocked_state: YES | NO
completed: YES | NO
fork_record_produced: YES | NO
checker_verdict: <PASS | PRICE_REQUIRED | BLOCKED | VALID_FORK | N/A>
notes: ""
```

## Interview Log

```yaml
- step: 1
  intent: <intent id>
  variant: <A | B | C>
  answer: "<writer's answer>"

  # Multidimensional evidence — TTI alone is insufficient.
  # Fast TTI + shallow idea ≠ slow TTI + direction-changing idea.
  time_to_next_idea_ms: <milliseconds — null if never continued>
  continued: YES | NO

  # Qualitative dimensions
  new_concept_created: YES | NO       # did the writer name something new?
  idea_depth: surface | medium | deep # surface = plot mechanic, deep = meaning/stake
  writer_energy: higher | same | lower # did energy rise, stay flat, or drop?
  confidence: high | medium | low      # writer's own sense of clarity

  notes: ""

- step: 2
  ...
```

## Summary

```yaml
total_steps: 0
total_continued: 0
total_stopped: 0
stopped_at_step: <null if completed>
fork_record_valid: YES | NO | N/A
median_tti_ms: 0
steps_with_new_concept: 0
energy_trajectory: rising | flat | falling | mixed
```
