---
kind: handoff
goal: G-001
seq: 9
from: studio
to: qa
stage: Verify
outcome: routed
---
# 09: studio → qa — Verify the dash/hit invulnerability fix against your six acceptance criteria

## Task

Verify independently (skill `verify-change`) that the change described below fixes the defect you reported ("player takes damage partway through a dash shortly after being hit"), and check for regressions. Return a pass/fail verdict per criterion.

## Context

Goal G-001 (combat monotony). While walking through the game, the Playtester saw damage during a dash shortly after a hit. You reproduced it and wrote the defect report with six acceptance criteria in `05-qa-to-studio.md`. Intended behavior is already specified in `design/combat.md`, and no spec value was changed. The gameplay engineer changed the build (0.3 → 0.3.1) to fix it.

## Findings

### What changed (observable description)

Player invulnerability no longer uses one shared on/off state. The hit window (0.8 s after a hit) and the dash window (0.25 s from dash start) are now tracked as two independent expiry times on the game clock, and the player is invulnerable while either is active. One window can no longer end the other's protection. Every damage source (Grub contact, Spitter projectiles) uses the same check. Hit-stun (0.3 s, no input), dash distance and duration, the 0.6 s dash cooldown, and the attack queued during a dash are unchanged. The handling of a dash pressed during hit-stun is also unchanged, and is not specified in `design/combat.md`. Unit tests on a simulated clock were added by the engineer; they are not a substitute for your verification.

### How to exercise it

At 30 FPS and 60 FPS, in rooms 1–5 with Grubs and Spitters:

1. Take a hit. Then dash at delays after the hit of about 0.3, 0.4, 0.5, 0.55, 0.6, 0.7, 0.79, 0.8 and 0.85 s, with a damage source (Grub in contact, or a Spitter projectile timed to arrive) present through the dash and the time after it.
2. Check there is no damage during the dash.
3. Check there is no damage between the dash end and 0.8 s after the hit.
4. Check that damage lands again normally after 0.8 s after the hit, if no dash is active.
5. Dash with no preceding hit. Check the full 0.25 s is invulnerable and damage can land right after it.
6. Repeat with dash directions towards and away from the damage source.

Do not test only the earliest dash after a hit (about 0.3 s); later presses and the period after the dash ends matter too.

### Notes for the verdict

- A dash that follows a hit now keeps protection until 0.8 s after the hit, as the spec requires. This may feel like more safe time than before.
- The expiry check is `now < expiry`. A one-frame difference for damage landing exactly on a 0.8 s or 0.25 s boundary is expected, not a failure.
- Watch for any other effect that depended on the old shared invulnerability state (for example flicker or sound cues), and report any you find.
- A dash pressed during hit-stun is unspecified. Report what you observe, without failing it; the design owner will decide separately.

## Decisions already made

- D-001: Combat uses one attack button plus dash. No new input was added.

## Constraints

- Must play correctly at both 30 and 60 FPS.
- Verify from `design/combat.md`, your acceptance criteria and the build, not from the engineer's explanation.
- Do not change the spec or the build. If expected behavior is undefined for a case, report it instead of ruling on it.

## Open questions

None.

## Expected output

A verification report with a pass/fail verdict for each of your six criteria at 30 and 60 FPS, any regressions, and any undefined-behavior cases. Address it to `studio`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md; project.md#constraints; the latest build under sim/ (`sim/build-*.md`, the player-visible build per project.md)
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/05-qa-to-studio.md
