---
kind: handoff
goal: G-001
seq: 3
from: gameplay-engineer
to: qa
stage: Verify
outcome: done
---
# 03: gameplay-engineer → qa — Verify fix: no damage at any point during a dash, including a dash started after a recent hit

## Task

Verify the fix for the G-001 defect (player takes damage partway through a dash started shortly after being hit) against the six acceptance criteria below. Run them at both 30 FPS and 60 FPS. The criteria are unchanged from your defect report (02).

## Context

Goal G-001. The Owner reported that damage sometimes lands during a dash. QA's report (02) reproduced it for a dash started soon after a hit and confirmed that `design/combat.md` requires full-duration dash invulnerability. A Build step has since changed the game. Verify is next.

## Findings

### What changed

- The player's invulnerability is now tracked as two separate sources: dash invulnerability (ends 0.25 s after dash start) and post-hit invulnerability (ends 0.8 s after the hit). The player is invulnerable while either one is active.
- Unchanged: dash distance and duration (4 tiles over 0.25 s), dash cooldown (0.6 s), the attack queued during a dash, hit-stun (0.3 s), damage (1 heart), the input set (D-001), and enemy behavior.
- The change is in the player's shared invulnerability logic, so it applies to both Grub bites and Spitter projectiles.

### How to exercise it

1. Enter a room with Grubs and/or Spitters and take one hit.
2. Dash at different delays after the hit:
   - the moment input returns (about 0.3 s after the hit);
   - about 0.5 s after the hit;
   - about 0.6–0.75 s after the hit;
   - just before 0.8 s after the hit.
3. Keep a Grub touching you, or a projectile arriving, throughout each dash.
4. Confirm no heart is lost from dash start to dash end.
5. Also check that a hit taken without dashing still gives 1 heart of damage, 0.3 s of hit-stun and invulnerability until 0.8 s after the hit.
6. Repeat everything at 30 FPS and at 60 FPS.

Give extra repetitions to dashes that start between about 0.55 s and 0.8 s after the hit, at both frame rates. Also check that the player stays protected for the rest of the 0.8 s window after a dash that began earlier and ended inside it.

### Acceptance criteria (unchanged)

1. Take a hit, then dash as soon as input returns after hit-stun (about 0.3 s after the hit). Repeat at least 20 times per frame rate, against a Grub contact and against a Spitter projectile. The player takes no damage at any moment from dash start to dash end (0.25 s).
2. Repeat the above, starting the dash at several delays after the hit (immediately after hit-stun, and during the remainder of the 0.8 s post-hit invulnerability window). No damage during the dash in any case.
3. With no recent hit, dashing through a Grub or into a projectile still causes no damage during the dash (no regression).
4. Without dashing, a hit still deals 1 heart, applies 0.3 s hit-stun, and grants invulnerability until 0.8 s after the hit (no regression).
5. Dash distance and duration are unchanged (4 tiles over 0.25 s), cooldown is unchanged (0.6 s), and an attack pressed during a dash still fires when the dash ends.
6. Results are the same at 30 and 60 FPS.

### Known risks

- Boundary timing: a dash started within about one frame of the 0.8 s post-hit expiry. At 30 FPS a frame is about 33 ms, so check this edge at both frame rates.
- The repository has no automated tests for invulnerability or enemies. Verification is manual, by the steps above.

## Decisions already made

- D-001 (one attack button plus dash): no input was added.

## Constraints

- Must play correctly at 30 and 60 FPS.
- No new input buttons beyond attack, dash and pause (D-001).
- Design unchanged: dash invulnerability is as specified in `design/combat.md`.

## Open questions

If you cannot exercise the build (for example, the build description does not show the changed behavior), report that as a blocker instead of guessing a verdict. If any criterion fails, or damage appears at a delay not listed above, report the delay, frame rate and enemy type.

## Expected output

A verdict handoff (`pass` or `fail`) against criteria 1–6, with results at 30 and 60 FPS. Address it to `studio`. A failure is routed back to `gameplay-engineer` with the exact delay, frame rate and enemy involved.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#constraints, design/combat.md, sim/build-0.4.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-damage-during-dash/02-qa-to-gameplay-engineer.md
