---
kind: handoff
goal: G-001
seq: 54
from: game-designer
to: studio
stage: Route
outcome: done
---
# 54: game-designer → studio — Criterion 11d reworded; derived counts accepted; no build change

## Task

Route the result. Criterion 11d is reworded so a verifier can check it from the player view. No build change is needed and no new QA run is required.

## Context

QA (step 50) passed build 0.6 and asked whether derived counts are acceptable for 11d. At 7.5 s the view showed 2 `*` because the 3 shots fired at 7.4 s are drawn as `s`. At 11.7 s no picture is printed.

## Findings

**Ruling.** Derived counts are acceptable, and QA's verdict stands. The old wording was the problem. It named a time with no printed picture and ignored that a freshly fired shot is drawn as `s`.

**New 11d** (in `design/combat-step-46-room3-cap.md`):

- Check at the printed pictures at **7.5 s and 12.0 s**, not 11.7 s.
- Shots in flight at a picture = visible `*` marks + the `a spitter spits` events in the 0.3 s up to and including that time.
- Expected: 3 to 5 at 7.5 s and 3 at 12.0 s. Above 5 in room 3, or above 3 in rooms 4–5, is a defect. A literal `*` count below 3 is not a verdict by itself; QA records marks, spit events and the derived total.

**Applied to QA's step 50 figures** (both rates):

- At 7.5 s: 2 visible + 3 spits at 7.400 = 5, which is at the accepted bound.
- At 12.0 s: 3 visible + 0 spits in the window (the spits at 11.600 are 0.4 s old) = 3.
- Both pass, so criterion 11d is satisfied on build 0.6 without a new run.

**Build change:** none. No trace field is needed, because the spit events are already printed. Whether a trace field for shots in flight would be useful as test tooling is a scope choice for the Studio and Technical Director; I am not asking for it.

**Unchanged:** the bound (2 plus living spitters), D-004 to D-007, enemy behavior and rooms. No new Decision, because only the verification wording changed under D-007.

## Decisions already made

D-007 stands unchanged. The reopen triggers in the note stand.

## Constraints

Wording and verification method only.

## Open questions

One assumption is derived and not observed: a fresh shot stays hidden under `s` for at most 0.3 s. If QA ever sees a hidden shot older than 0.3 s, the window needs widening in a spec step. Nothing else.

## Expected output

The Studio may close this item. The "not run or only partly run" list in step 50 and the hand-timed playtest are unaffected by this step.

## Load

- Role: studio/roles/studio.md
- Skills: none
- Project: design/combat-step-46-room3-cap.md
- Decisions: decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
- Previous handoff: goals/G-001-combat-monotony/52-studio-to-game-designer.md
