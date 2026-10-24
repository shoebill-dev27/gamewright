---
kind: handoff
goal: G-001
seq: 8
from: gameplay-engineer
to: studio
stage: Build
outcome: done
---
# 08: gameplay-engineer → studio — Dash/hit invulnerability fix (build 0.3 → 0.3.1), ready for QA verification

## Task

Compose the QA verification Handoff from this change. QA verifies it independently against the acceptance criteria in `05-qa-to-studio.md` (restated in 06). I do not certify the fix as verified.

## Context

Goal G-001 (combat monotony). Handoff 06 asked for the defect "player takes damage partway through a dash shortly after being hit" to be fixed, and for the trigger to be reported. The expected behavior is fully specified in `design/combat.md`, so nothing needed to go back to Design. No spec value was changed.

## Findings

### Trigger found

The trigger comes from reading the invulnerability code path described in the repository notes. It was not measured at runtime, because this dry run has no runnable build. QA should confirm it in play.

- **Timing is what triggers it, not frame rate.** The cause is in the order of two timer expiries relative to the hit. It does not depend on delta time, so it should appear at both 30 and 60 FPS. Frame rate only changes how precisely the window edges are hit.
- **Window A, damage mid-dash:** a dash begun between about 0.55 s and 0.8 s after the hit. The hit invulnerability ends at 0.8 s, while the dash is still running, so the player can be damaged from 0.8 s to the end of the dash. A dash begun at 0.8 s or later is unaffected. The latest damaged-dash start is just under 0.8 s.
- **Window B, damage right after a dash:** a dash begun at 0.3 s to about 0.55 s after the hit. The dash ends before 0.8 s and its end clears invulnerability early. The player can then be damaged between the dash end and 0.8 s after the hit. The spec says that period is still invulnerable. This is the "delayed damage" case in criterion 6.
- **Why the earliest-dash check can look fine:** a dash at exactly 0.3 s is covered by invulnerability for its full length. The damage only shows up after it ends (window B). Window A needs a later press. QA should not test only the 0.3 s press.
- **Damage source:** any source. Grub contact and Spitter projectiles use the same invulnerability check.
- **Dash direction:** not relevant to the cause.
- **Rarity:** it needs a dash pressed within about 0.5 s of a hit, plus a damage source arriving in the remaining window.

### The change, stated exactly

**What:** Player invulnerability stops being a single on/off flag that each timer switches on and off. It becomes two expiry timestamps in game time, and "invulnerable" is computed from them.

**Where:** the player's invulnerability handling. This is the single flag that both the dash and the hit reaction currently write to. The same check is used by every damage source.

**Change:**

1. Remove the shared flag and the two timers that switch it off.
2. Add two values to the player: `hitInvulnUntil` and `dashInvulnUntil`. Both are expiry times on the accumulated game clock, which is the sum of delta times, so they do not depend on frame rate.
3. On a hit, set `hitInvulnUntil = hitTime + 0.8 s`. Hit-stun stays 0.3 s with no input, unchanged.
4. On dash start, set `dashInvulnUntil = dashStartTime + 0.25 s`. Dash distance, duration and the 0.6 s cooldown are unchanged.
5. `isInvulnerable(now)` returns `now < max(hitInvulnUntil, dashInvulnUntil)`. Every damage source calls this when it tries to apply damage. Neither window can cancel or shorten the other.
6. Nothing else changes: the attack queued during a dash still fires when the dash ends. The handling of a dash pressed during hit-stun is left exactly as it is now. It is unspecified and is the separate non-blocking question for `game-designer`.

**Tests:** I added unit tests for `isInvulnerable` on a simulated game clock. They cover the cases listed below, each run with fixed steps of 1/30 s and 1/60 s and with varying delta times.

- Dash with no hit: invulnerable for 0.25 s, not after.
- Hit alone: invulnerable until 0.8 s, not after.
- Dash started at 0.3, 0.5, 0.55, 0.6, 0.79 and 0.8 s after a hit: invulnerable for the whole dash and until at least 0.8 s after the hit.
- Damage attempted at every step from the hit to 1.2 s after it.

These are new tests, since none existed. They are my own check, not a verification.

### How to exercise it (for QA)

At 30 FPS and 60 FPS, in rooms 1–5 with Grubs and Spitters:

1. Take a hit. Then dash at delays after the hit of about 0.3, 0.4, 0.5, 0.55, 0.6, 0.7, 0.79, 0.8 and 0.85 s, with a damage source (Grub in contact, or a Spitter projectile timed to arrive) present through the dash and the time after it.
2. Check there is no damage during the dash.
3. Check there is no damage between the dash end and 0.8 s after the hit.
4. Check that damage can land again normally after 0.8 s after the hit, if no dash is active.
5. Dash with no preceding hit. Check the full 0.25 s is invulnerable and damage can land right after it.
6. Repeat with dash directions towards and away from the damage source.

### Criteria addressed

All six criteria in `05-qa-to-studio.md`:

| Criterion | How it is addressed |
|---|---|
| 1, 2, 3 | Covered by the change. The window-A and window-B timings need particular attention. |
| 4 | Covered by the dash-only timestamp. |
| 5 | Hit-stun, the 0.8 s hit window, the 0.6 s cooldown and the queued attack are untouched, but QA should still check them. |
| 6 | Window B is the "damage delayed to land right after the dash ends" case. It is now covered, because the hit window is no longer cleared by the dash end. |

### Known risks

- **More protection than before in one case.** A dash begun just after a hit used to lose invulnerability when it ended, and now keeps it until 0.8 s after the hit. The spec requires this. Some players may notice more safe time after a hit-then-dash. That is a design matter and I did not change it.
- **Boundary frames.** The check is `now < expiry`. A damage event exactly on the 0.8 s or 0.25 s boundary is treated as expired. At variable delta time this can differ by one frame from what a tester expects. QA should treat a one-frame difference at the exact boundary as expected.
- **Unspecified:** a dash pressed during hit-stun is unchanged (ignored or buffered, whichever it is now). It is not part of this fix.
- **Other flag users.** I found no other writer of the old flag in the notes. QA should watch for any other effect that depended on it, such as flicker or sound cues for invulnerability. The repository notes don't describe any.

## Decisions already made

- D-001: Combat uses one attack button plus dash. No new input was added.

## Constraints

- It must play correctly at 30 and 60 FPS. The fix uses accumulated game time, not frame counts.
- It reuses the existing player invulnerability code. No new systems.
- No value in `design/combat.md` changed.

## Open questions

- Non-blocking, for `game-designer`: should a dash pressed during hit-stun be ignored or buffered? It is unspecified and unchanged here.

## Expected output

The Studio composes the verification Handoff to `qa` from the "Findings" section (the change, how to exercise it, criteria addressed, known risks). It leaves out `## Sender assessment`. QA verifies against the six criteria at 30 and 60 FPS and returns a pass/fail verdict.

## Sender assessment

**Root cause (from code notes, not measured at runtime):** invulnerability was one shared boolean. The dash set it and started a 0.25 s timer. A hit set it and started a timer ending 0.8 s after the hit. Each timer's expiry unconditionally set the flag off, whatever else was still active. So whichever timer fired first cleared the other's protection:

- Window A: the hit timer (0.8 s) fires mid-dash when the dash began between about 0.55 s and 0.8 s after the hit.
- Window B: the dash timer fires and clears the flag while the hit window is still running, when the dash began between 0.3 s and about 0.55 s after the hit.

QA's hypothesis, one timer's expiry clearing the other's flag, is **confirmed**. It happens in both directions. The "dash begun during or just after hit-stun restarts or cancels a timer" variant is not needed to explain the behavior, so I discarded it.

**Frame rate:** the logic is the same at both rates. It depends on the order of expiries on the timeline. I expect it at both 30 and 60 FPS, but this is inferred, not observed.

**Confidence:** high on the root cause given the notes. Medium on the exact window edges (about 0.55 s and 0.8 s), which follow from the stated durations and the earliest dash start of 0.3 s. I own test results only at unit level, on the simulated clock. I have not played the build, and QA should verify on the real one.

## Load

- Role: studio/roles/qa.md
- Skills: none
- Project: design/combat.md; sim/build-0.3.md; project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/06-studio-to-gameplay-engineer.md
