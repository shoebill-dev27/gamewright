---
kind: handoff
goal: G-003
seq: 4
from: game-designer
to: studio
stage: Design
outcome: done
---
# 04: game-designer → studio — Dash availability spec (A+B+C) ready for Build

## Task

Route Build to `gameplay-engineer` from `design/dash-availability.md`, then QA and an independent playtest. The spec covers the persistent status (A), the messages (B) and the manual and spec text (C), with player-observable acceptance criteria in seconds.

## Context

Goal G-003 (Owner: 「ダッシュがいつまた使えるのか分かりにくい。分かるようにしてほしい」). Diagnose (02) found missing information. Handoff 03 asked for the spec and for the cooldown start point to be confirmed. Dash rules, inputs and timing stay as they are.

## Findings

My report:

- **Cooldown start point (confirmed at 60 FPS, player view):** the 0.6 s cooldown starts when the dash ends. In run `cd-start` a dash at 0.500 was accepted, presses at 1.300 and 1.333 were refused, and 1.350 was accepted. That is start + 0.25 + 0.6 = 0.85 s. This is now documented in `design/combat.md` (edited) and the spec.
- **Wind-up:** a dash is accepted during an enemy wind-up (run `cd-after-hit`, press at 0.050), and the following dash timing fits the same rule. Wind-ups do not change the cooldown.
- **After a hit: NOT confirmed.** The one refusal after a hit (2.200) fell inside hit-stun (hit at 2.150, input ignored for 0.3 s) after the cooldown had already ended, so it does not show whether a hit changes the cooldown. The spec's rule is that it does not; QA criterion Q3 checks it. If the build differs, QA hands back with `outcome: question` and a `game-director` question follows, as the escalation condition in 03 says. Nothing observed so far triggers it.
- **Room transition:** the cooldown clears at entry per `final-boss-and-continuous-run.md` §2; not re-observed. QA criterion Q5 checks it.
- **Attack recovery vs dash:** not tested. The spec counts anything that makes the build refuse a dash as unavailable time, so the display follows the build; QA criterion Q4 records which it is.
- **30 FPS:** not run; the 0.85 s start-to-start is expected, checked by Q1/Q2.
- **Spec content (A, B, C):**
  - A: every live picture ends with `dash: ready`, `dash: active` or `dash: <R> s`, where R is the time to usable, rounded UP to a tenth (never shows ready early).
  - B: an accepted dash prints `you dash <dir> — usable again in 0.9 s`. A refused dash prints `dash not ready — <R> s left`, with `(dashing)` or `(hit-stun)` as the reason when it applies. `dash ready` is printed at the exact ready moment, with an event picture, and only after a dash was used.
  - C: drop-in manual text is in section 8 of the spec, because `repo/manual.md` is not on my write list. The Dash line in `design/combat.md` is edited directly.
  - Pictures and results otherwise unchanged; the periodic grid and `view-every` are unaffected.
- **Decision D-028:** the indicator is also shown on the legacy route, including room 5, because the probes and most scripts use that route. G-002 criterion L1 is therefore rebased to ignore the dash field, dash text and `dash ready` lines. This touches an accepted G-002 criterion, so the Studio should confirm it for the QA plan.
- **Boss room and legacy route:** both show the same indicator (see D-028).
- **Not examined:** whether a human finds the one-decimal display clear (playtest); dash invulnerability display and queued inputs (out of scope, proposed Goals).

## Decisions already made

- D-001: no new input buttons. Respected.
- D-022: legacy route stays limited; only the display is added (D-028).
- D-028 (new, this step): dash indicator on the legacy route including room 5; L1 rebased.

## Constraints

- No change to dash length, distance, invulnerability, cooldown value or inputs.
- All timing in seconds; criteria hold at 30 and 60 FPS (±1 frame).
- Reuse the existing text view and message system. No new input.
- Dash invulnerability display and queued inputs are out of scope.
- Existing player-view comparisons and golden outputs will differ by the new field and text; compare with them stripped (Q8). Game results must not change.
- Applying `repo/manual.md` text (spec section 8) belongs to the Build step.

## Open questions

- Hit during cooldown (Q3) and attack recovery vs dash (Q4): unconfirmed; QA records them from the build. A cooldown that differs by situation in an undocumentable way returns to the Studio as `question` for `game-director`.
- Whether the Build step finds the extra field breaks reaction-rule parsing; if so it reports back to the designer.
- Whether the human playtest finds the display clear and not cluttered in rooms 4–5 and the boss (experience signals, section 7 of the spec; not for the Playtester's handoff).

## Expected output

- Build: dash field, messages, `dash ready` with event picture, trace records (`dash_start`, `dash_end`, `dash_ready`) and the manual text, with no change to game results.
- QA: criteria P1–P12 and Q1–Q12 in `design/dash-availability.md` at 30 and 60 FPS, including the unconfirmed cases Q3–Q5.
- Independent playtest from player-visible output only, using section 5 (player-visible criteria) of the spec and the manual. Do not pass section 7 to the Playtester.
- The result goes back to `game-designer` if Q3 or Q4 show behavior the spec does not describe.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: none specified by the designer; per Studio routing for Build
- Project: design/dash-availability.md, design/combat.md, repo/manual.md, repo/public-driver.md, design/final-boss-and-continuous-run.md#2-ランと入場
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-022-g002-v1-supplements.md, decisions/D-028-dash-indicator-on-legacy-route.md
- Previous handoff: goals/G-003-dash-availability-clarity/03-studio-to-game-designer.md
