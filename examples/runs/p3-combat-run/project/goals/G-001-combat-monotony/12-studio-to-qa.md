---
kind: handoff
goal: G-001
seq: 12
from: studio
to: qa
stage: Verify
outcome: routed
---
# 12: studio → qa — Verify the dash/hit invulnerability fix against the named build

## Task

Verify, in the build named under Load, that taking damage during a dash shortly after a hit no longer happens. Check at 30 FPS and at 60 FPS, and return a `pass` or `fail` report with per-criterion evidence.

## Context

Goal G-001 (combat monotony). QA earlier confirmed a defect: after the player is hit and dashes within the hit-invulnerability window, damage could land during the dash (`05-qa-to-studio.md`). A fix has been made. Your previous attempt (`10-qa-to-studio.md`) was blocked because no build file was in the packet. The build files are now listed explicitly under Load.

## Findings

Acceptance criteria (from `05-qa-to-studio.md`, as summarized in your handoff 10):

1. Dash at the earliest moment (about 0.3 s after the hit): no damage during the 0.25 s dash, at least 20 repeats per frame rate, with Grub contact and with Spitter projectile.
2. Dash presses at varied delays after the hit (including during hit-stun, and just before, at and after 0.8 s): no damage during an active dash.
3. Different dash directions (towards and away from the damage source), rooms 1–5, Grubs and Spitters.
4. Dash with no preceding hit: full 0.25 s invulnerability, no regression.
5. Existing rules hold: hit-stun 0.3 s with no input, hit invulnerability to 0.8 s, dash cooldown 0.6 s, attack queued during a dash fires at its end.
6. Damage that would have landed mid-dash is not delayed to land right after the dash ends; damage after the windows expire is normal.

Notes:
- `design/combat.md` was clarified since your last look: hit invulnerability and dash invulnerability are independent timers, and the player is invulnerable while either is active (D-003 also fixes input during hit-stun as ignored, not buffered). The clarification restores no new behavior and adds none. The room enemy range there is now 3–7 (for a later phase; not part of this check).
- The dash-during-hit-stun case is now specified as ignored (D-003). Check it as part of criterion 2 and 5.
- Record boundary results around 0.8 s and 0.85 s with the frame length at 30 FPS (about 33 ms) and 60 FPS (about 17 ms) in view.
- Your plan in handoff 10 (matrix, repeat counts, flicker/sound cues) stands.

## Decisions already made

- D-001: Combat uses one attack button plus dash.
- D-003: Input during hit-stun is ignored, not buffered; hit and dash invulnerability are independent timers.

## Constraints

- Verify from `design/combat.md`, the acceptance criteria and the build. Do not change the spec or the build.
- Must be verified at both 30 and 60 FPS.
- The latest build is `sim/build-0.4.md`; `sim/build-0.3.md` is the baseline for comparison. If neither shows the fix (or the fix cannot be observed), report that as a blocker with `outcome: question`. Do not infer behavior from descriptions of intent.

## Open questions

None new. The non-blocking question about dash during hit-stun is answered by D-003.

## Expected output

A verification report to `studio` with `outcome: pass` or `fail`, per-criterion results at 30 and 60 FPS with evidence, regressions checked, and any undefined behavior found.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md; project.md#constraints; sim/build-0.4.md; sim/build-0.3.md; goals/G-001-combat-monotony/05-qa-to-studio.md (defect report with the original criteria)
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-003-input-during-hit-stun.md
- Previous handoff: goals/G-001-combat-monotony/10-qa-to-studio.md
