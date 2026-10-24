---
kind: handoff
goal: G-001
seq: 95
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 95: studio → gameplay-engineer — Build the wording-only messages: shot-hit source (A) and late-swipe line (B)

## Task

Implement the two text-view messages and the manual wording exactly as specified in `design/combat-step94.md`, with tests. Wording only: no rule, number, timing, cap, cue or input change.

## Context

Goal G-001 (combat feels monotonous). Review pass 3 (D-013) found the goal not met by one clause: a shot hit names no source, and no line says why a late swipe did not stop a lunge. The game-designer wrote the spec (handoff 94). QA verifies the build next, then Review pass 4 as a paper check.

## Findings

From the spec (read it for the exact wording and formulas; it governs):

- **(A)** Shot hit message becomes `YOU ARE HIT by a shot from the <direction>` followed by the existing suffix. `<direction>` is one of eight compass words (north is the top of the drawn room, smaller y). It is the side the shot came from, the reverse of its travel direction, taken from the shot's locked travel vector at the contact frame, before the shot is removed. The formula and the 22.5° sector boundary are in the spec. Absorbed shots still show no message. Output is identical at 30 and 60 FPS.
- **(B)** One line when a swipe damages, without killing, a grub, runner or brute in its Lunge phase: `the <grub|runner|brute>'s lunge had already started, the swipe was too late to stop it`. It comes before any `YOU ARE HIT by` line of the same frame. It must not contain `rears back`, `takes aim` or `YOU ARE HIT by`. The brute's wind-up line `the brute shrugs off the swipe` stays untouched. No line in other phases or on a kill.
- **Manual:** the spec ends with the exact replacement wording for `repo/manual.md`. Apply it (the designer could not edit that file).
- **Acceptance criteria W1–W8** are in the spec: direction words, prefix and substrings, absorbed shots, the late-swipe line, no line elsewhere, no behavior change (same traces as before within ±1 frame, `bots.py` output unchanged, suite green), same wording at both frame rates.
- **Risk to check:** if `bots.py`, a reaction rule or a test matches the full string `YOU ARE HIT by a shot` by equality instead of a substring, fix the tool or test, not the rule text.
- **Placement note:** the spitter at (15,7) gives a ratio of 3/7 = 0.43, above 0.4142, so the diagonal `south-east` is expected there. Check your result against the formula.

## Decisions already made

- D-001: one-button combat, no new inputs.
- D-005: blocked contact consumes the shot and spends the lunge's hit.
- D-011: variant-named wind-up and hit messages accepted.
- D-013: wording-only round, then Close.

## Constraints

- Wording only. Keep `takes aim`, `rears back`, `YOU ARE HIT by` and the brute "shrugs off" line.
- Reuse the existing message system.
- Same effect at 30 and 60 FPS.
- If the spec is ambiguous, contradictory or missing a case, stop and hand back (outcome `question`); do not decide.
- Run `python3 -m unittest discover -s tests` and `python3 bots.py {script}` for the existing scripts to confirm no behavior change.

## Open questions

None.

## Expected output

The changed `repo/game.py` (and `repo/bots.py` / tests only if needed per the risk above), the manual wording applied, new tests for W1–W8 where testable, and build notes in the outgoing Handoff. Address the result to `studio`, so QA can receive a fresh Handoff without the implementation history.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat-step94.md, design/combat.md, repo/manual.md, repo/game.py, repo/bots.py, repo/tests/test_game.py, repo/README.md
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md, decisions/D-011-variant-named-messages-accepted.md, decisions/D-013-review-pass-3-readability-wording-then-close.md
- Previous handoff: goals/G-001-combat-monotony/94-game-designer-to-studio.md
