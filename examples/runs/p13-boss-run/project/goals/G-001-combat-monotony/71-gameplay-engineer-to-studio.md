---
kind: handoff
goal: G-001
seq: 71
from: gameplay-engineer
to: studio
stage: Build
outcome: done
---
# 71: gameplay-engineer → studio — D-011 variant-named messages and manual wording built (tests and bot run still to be executed)

## Task

Hand the D-011 build to Verify (QA). Route it to `qa` without the Sender assessment.

## Context

Goal G-001. Handoff 69 asked for the D-011 message strings and the manual wording from `design/combat-step68.md`, with tests. No rule, timing, room or hearts value was changed.

## Findings

What changed and where:

- `repo/play.py` (text views):
  - The wind-up message is now `a <kind> rears back`, with kind `grub`, `runner` or `brute`. It is built from the existing `windup` event's `enemy` field.
  - The hit message is now `YOU ARE HIT by a <name> — hearts n/3`. The name is `grub`, `runner`, `brute` or `shot`. The suffix is unchanged.
  - `Player.describe` takes an optional third argument, the hit's name. Callers that omit it still work.
  - The player view and the reaction-rule message list use the same names, so `text "rears back"` still matches all three wind-ups.
- `repo/game.py`: a new list `Game.hurt_kinds` records the attacker's name for each `hurt` event, in order. The event dict, `source`, trace output and bot statistics are unchanged.
- `repo/manual.md`:
  - The grub warning bullet lists the three wind-up messages.
  - The late-swipe wording is replaced with the exact text from `design/combat-step68.md` section 2.
  - The in-flight sentence is replaced with the exact text from section 1.
  - The hit-message line lists all four hit messages.
- `repo/tests/test_game.py`: new class `VariantMessageTest` with these cases:
  - the wind-up message for each variant, at 30 and 60 FPS;
  - the hit message for each variant plus the shot, at both rates;
  - a `text "rears back"` rule matching all three wind-ups;
  - the manual wording.

How to exercise (practice room, player at 8,4, no inputs):
- `room empty`, `spawn runner 9.5 4`, `end 3`: expect `a runner rears back`, then `YOU ARE HIT by a runner — hearts 2/3`. Repeat with `grub` and `brute`.
- Compare trace output and bot output for the same scripts against 0.6.1: they should be identical.

Acceptance criteria addressed: V-a, V-b, V-c, V-d. V-e relies on rules, timings, rooms and hearts being untouched.

Known risks:
- The Player view reads `game.hurt_kinds` by the running index of `hurt` events. This relies on every `hurt` event appending exactly once, which `_hurt` does.
- Nothing else keys on the old strings. The existing tests only check `a grub rears back` with a standard grub.

Open build item: the build identifier or sha is not set. The banner stays `Lantern Depths 0.6`, which an existing test asserts, so I did not change it. The Studio should state the build number for the playtest brief (D-009 item 5).

## Decisions already made

- D-001, D-011 (accepted). D-004 to D-007 are not reopened.

## Constraints

None new.

## Open questions

None.

## Expected output

QA verifies V-a to V-e at 30 and 60 FPS. The test run (`run_tests`) and the bot run (`run_bots`) have not been executed in this step; they are Verify's first task.

## Sender assessment

I could not run `run_tests` or `run_bots` in this step. The change is a presentation-only edit: `game.py` only gains a read-only list, so the simulation and bot numbers cannot move. This is derived from reading the code, not measured. Confidence is high on the strings and moderate on the new tests until they are run.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat-step68.md, design/combat.md, design/combat-step-46-room3-cap.md, repo/manual.md, repo/play.py, repo/game.py, repo/tests/test_game.py
- Decisions: decisions/D-011-variant-named-messages-accepted.md
- Previous handoff: goals/G-001-combat-monotony/69-studio-to-gameplay-engineer.md
