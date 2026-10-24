---
kind: handoff
goal: G-001
seq: 3
from: gameplay-engineer
to: qa
stage: Verify
outcome: done
---
# 03: gameplay-engineer → qa — Verify fix: player takes damage mid-dash when the dash overlaps the end of post-hit invulnerability

## Task

Verify the change below against the acceptance criteria in handoff 02, at both 30 FPS and 60 FPS. Give a pass or fail verdict.

## Context

Goal G-001. The Owner reported: "Sometimes I take damage even while dashing." QA's defect report (02) established that `design/combat.md` says the dash makes the player invulnerable for its full 0.25 s. It also says a hit is followed by 0.3 s hit-stun and then invulnerability until 0.8 s after the hit. The change is stated below and counts as made, per the dry-run rules in `project.md#constraints`.

## Findings

### Change

Where: the player invulnerability logic. The enemy controller, hit-stun, dash movement and cooldown are not touched.

What:
1. The shared invulnerability on/off flag and its two "switch the flag off" timer callbacks are removed.
2. Two independent sources of invulnerability remain:
   - Dash source: the player is invulnerable while the dash state is active, read from the dash state itself.
   - Post-hit source: on a hit, `hitInvulnUntil = hitTime + 0.8 s` is stored, using accumulated game time. The source is active while `gameTime < hitInvulnUntil`.
3. `isInvulnerable = isDashing || gameTime < hitInvulnUntil`.
4. The damage check reads `isInvulnerable` at the moment damage would apply.

Frame rate: both sources compare against accumulated game time or the dash state, with no per-frame countdown.

Tests added: unit tests stepping the simulation at fixed delta times of 1/30 s and 1/60 s, covering hit then dash at several offsets, a dash with no prior hit, damage resuming after the invulnerability window, and a dash and a hit in the same frame.

### How to exercise it (maps to the acceptance criteria in 02)

At both 30 FPS and 60 FPS:
1. Get hit, then dash at about 0.3 s, 0.4 s, 0.55 s, 0.7 s and 0.79 s after the hit, with a Grub in contact range. Expect no damage for the full dash (criteria 1 and 2).
2. Repeat with a Spitter projectile crossing the dash path (criterion 3).
3. Dash with no recent hit and enemies in contact range. Expect no damage (criterion 4).
4. Regression (criterion 5):
   - Dash is still 4 tiles over 0.25 s, with a 0.6 s cooldown.
   - An attack pressed during a dash is still queued and fires when the dash ends.
   - A hit still deals 1 heart with 0.3 s hit-stun.
   - After a dash that ends before 0.8 s after the hit, the player stays invulnerable until 0.8 s after the hit.
   - Once the dash and the post-hit window have both ended, the player takes damage normally.
5. Also try a dash started and a dash ended while an enemy is in contact range (edge frames of the dash).

## Decisions already made

- D-001: no new input buttons beyond attack, dash and pause. This change adds none.

## Constraints

- Must play correctly at both 30 and 60 FPS.
- Desktop, keyboard and gamepad.
- No new input buttons (D-001).

## Open questions

None.

## Expected output

A verification Handoff with outcome `pass` or `fail`, stating the result for each acceptance criterion at 30 FPS and at 60 FPS. Address the result to `studio`.

## Sender assessment

- Root cause: confidence is high, from the implementation notes. The single on/off flag with two timers that each clear it on expiry produces exactly the reported symptom: occasional damage when a dash is started shortly after a hit. The window is the 0.55 s to 0.8 s range from QA's hypothesis, which is consistent with it.
- Frame rate: the cause is not frame-rate dependent by itself. The window is set by the timer arithmetic. A variable delta time only shifts the exact moment of expiry by up to one frame. The fix uses game-time comparison and dash state, so both frame rates should behave the same.
- Self-test: no real build exists in this dry-run. The verdicts are from reasoning about the code path and the described unit tests, not from execution. QA must verify independently.
- Not confirmed: whether any damage during a dash with no prior hit exists. No other mechanism is known from the notes. If QA reproduces damage in criterion 4, the cause is something else, so hand back.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#constraints, design/combat.md, sim/build-0.4.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-dash-damage/02-qa-to-gameplay-engineer.md
