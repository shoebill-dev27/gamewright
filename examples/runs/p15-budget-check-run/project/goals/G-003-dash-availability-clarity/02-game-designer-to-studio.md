---
kind: handoff
goal: G-003
seq: 2
from: game-designer
to: studio
stage: Diagnose
outcome: done
---
# 02: game-designer → studio: Diagnosis of unclear dash availability

## Task

Route the diagnosis below. No Director decision is needed. The next stage is Design, with the game-designer writing the spec for the recommended option. Then Build, then QA.

## Context

Goal G-003: a player using only what the build shows can tell whether dash is available now and, when it is not, when it will be again. The Owner's report was 「ダッシュがいつまた使えるのか分かりにくい。分かるようにしてほしい」. This step diagnosed the cause from `design/combat.md`, `repo/manual.md`, `repo/public-driver.md` and one play run on sha dc0138c2b6d1 (dash-cooldown-probe, 60 FPS, practice room). I did not run the trace view or the tests.

## Findings

### What the player sees today (evidence: the probe run, player view)

Dash inputs were at 0.5, 0.8, 1.2, 1.5, 2.5 and 2.6 s.

| Time | Output | Reading |
|---|---|---|
| 0.5 | `you dash right` | accepted |
| 0.8 | `(nothing happens)` | refused, 0.3 s after the dash started and 0.05 s after it ended |
| 1.2 | `(nothing happens)` | refused, 0.7 s after the dash started |
| 1.5 | `you dash right` | accepted, 1.0 s after |
| 2.5 | `you dash right` | accepted |
| 2.6 | `(nothing happens)` | refused |

- **Hearts line:** every picture shows only `hearts n/3` and the room. There is no dash indicator, no ready or cooling state, and no time remaining. This is true of the half-second periodic pictures and of the pictures printed after events.
- **No dash event pictures:** the dash itself produced no event picture. The next picture came at the next half-second tick.
- **Refusal text:** a dash during cooldown prints only `(nothing happens)`. That text does not name the dash or say it is cooling down. It does not give a time or say when the dash will return. A player cannot tell a refusal from a dash that happened but was invisible.
- **No readiness message:** nothing is printed when the dash becomes usable again.
- **Manual:** the Controls section says only "a quick burst… You cannot be hurt while dashing." It does not mention any recovery, cooldown, refusal or readiness. The Warnings section mentions dash only as a way to avoid lunges and shots.
- **Design spec:** `design/combat.md` says "Cooldown 0.6 s" and does not say when that 0.6 s starts. The probe shows the dash is refused 0.7 s after its start, so the 0.6 s is not measured from the start. It is probably measured from the dash end (dash 0.25 s, so ready at about start + 0.85 s). The probe puts the ready moment between 0.7 s and 1.0 s after the start, consistent with that. The trace view would confirm it. I did not run it, and the exact value is not needed for the diagnosis.
- **Not yet checked:** whether the cooldown behaves differently after a hit, during enemy wind-ups, or across a room transition. The manual says combat timers reset on room entry, so a fresh dash is probably ready on entry. This is unverified.

### Causes (all missing information, not rules)

1. **Missing information (primary).** The player view has no dash state anywhere, not in the header, not in the cue line, and not in a message. The state exists in the game, because dash is refused and later accepted, but the player cannot see it. Without it the player has to guess.
2. **No readiness event.** The periodic pictures come every 0.5 s, which is too coarse for a 0.6 s cooldown. Even with a persistent indicator, readiness could be shown up to 0.5 s late. A message on the exact ready moment is needed.
3. **Ambiguous refusal wording.** `(nothing happens)` is the only feedback on a failed dash. It gives no reason or time, and it is not clearly about the dash.
4. **Undocumented rule.** The manual says nothing about cooldown, and the spec leaves its start point unstated. Documentation alone cannot fix the problem, because the player is also reading the screen during fast fights.

The unclarity is the same in every situation I could test, because no output carries dash state. It is missing information, not late information or placement. Late information applies only to the periodic-picture cadence in cause 2.

### Options (player-observable terms; dash timing and rules unchanged in all three)

- **Option A: persistent dash status.**
  - Change: every picture carries a dash state in the status area, for example `dash: ready` or `dash: 0.4 s`.
  - Addresses: causes 1 and 4.
  - Trade-offs:
    - The state is always visible and glanceable.
    - It reuses the existing hearts/status line and needs no new input.
    - Between the 0.5 s pictures the countdown can lag, so it should be paired with the ready message from Option B.
    - It adds one line or field to every picture.
  - Risk: low.
  - Fit with vision: supports "readable" play without adding input complexity.
- **Option B: event messages.**
  - Change: replace the refusal text with `dash not ready: 0.3 s left` (or similar), and print a `dash ready` message at the moment it returns, with an event picture.
  - Addresses: causes 2 and 3.
  - Trade-offs:
    - It is exact at the moment of readiness.
    - It reuses the message system.
    - A player who never tries to dash while it is cooling down never sees the countdown.
    - The ready message adds noise in busy fights.
  - Risk: low.
  - Fit: good.
- **Option C: documentation only.**
  - Change: state the cooldown and its start point in the manual and the spec.
  - Addresses: cause 4 only.
  - Trade-offs:
    - It has no build cost.
    - It does not meet the Goal, because the player still cannot see the state in play.
  - It is needed in addition to A and/or B anyway.

### Recommendation

Do A and B together, with C included in the same change. The player then has the state at a glance, an exact "ready" moment, and a reason when a dash is refused. All three reuse existing output and need no new input (D-001) or timing change. Describe all of it in seconds, not frames, so it works at 30 and 60 FPS.

Design will set the exact wording, the refresh rate of the countdown, and the acceptance criteria. Design will also state the start point of the 0.6 s cooldown as documented behavior, matching what the build does, not as a rule change.

### Director decision

- **No option needs a `game-director` decision.** Each option changes display and wording only. None changes recovery length, invulnerability, input buttons, scope or a pillar, so the tentative Decide stage does not need to run.
- **Trigger for escalation:** if Design finds that the actual cooldown behavior differs from the spec in a way that cannot be documented as is (for example, it differs between situations), that would become a direction question for `game-director`. Nothing so far suggests it.

### Whether a first-hand play observation is needed

Not to settle the cause. The player-view output shows the information is absent. Two items would help the later stages:
1. Build or QA should confirm the exact ready moment and the cooldown start point with the trace view.
2. Check the after-hit and room-transition cases before the spec fixes the wording. I have not done either.

I did not request a human playtest. I can't see whether a human would find the new display clear. That belongs to the later Play/Review stages.

### Unrelated notes (proposed future Goals, not scope)

- Nothing in the player view shows dash invulnerability while it is active. Whether the player knows when they are safe is a separate question and was not examined here.
- Dash input during the dash itself and queued attacks are not shown either. Not examined.

## Decisions already made

- D-001: one attack button plus dash; no new input buttons without Owner approval. All options comply.

## Constraints

- Dash rules (recovery length, invulnerability) stay as they are.
- No new inputs.
- Express timing in seconds so 30 and 60 FPS behave the same.
- Reuse the existing text view and message system.
- Design must add no numeric thresholds beyond what it specifies and verifies; this diagnosis sets none.

## Open questions

- When exactly does the 0.6 s cooldown start (dash end is probable; trace to confirm)?
- Does the cooldown behave the same after a hit, during enemy wind-ups, and after a room transition?
- What countdown refresh rate fits the 0.5 s picture cadence without clutter, and should an event picture be emitted when the dash becomes ready?
- Should the boss room (room 5) and the legacy route show the same indicator? The legacy route is intentionally limited under D-022.

## Expected output

Route to `game-designer` for the Design stage: a spec for options A+B+C with player-observable acceptance criteria, then Build and QA. The tentative Decide stage is not needed unless Design finds an escalation trigger.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#constraints, design/combat.md, repo/manual.md, repo/public-driver.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-003-dash-availability-clarity/02-game-designer-to-studio.md
