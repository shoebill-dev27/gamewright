---
kind: handoff
goal: G-001
seq: 2
from: qa
to: gameplay-engineer
stage: Build
outcome: done
---
# 02: qa → gameplay-engineer — Fix damage taken on the last frame of a dash

## Task

Fix the defect: the player takes damage on the final frame of a dash, although `design/combat.md` says the player is invulnerable for the full dash duration. Do not add inputs (D-001). The fix must hold at 30 and 60 FPS.

## Context

The Owner reported: 「ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。」 ("I sometimes take damage even while dashing.") No steps were given. QA reproduced the defect with the `trace` and `play` runs below.

## Findings

### Expected behavior (source)

`design/combat.md`, Player kit: "**Dash**: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration."

The document is clear on this point. Invulnerability is documented, so this is a defect, not a spec gap.

### Minimal reproduction (practice room, a Grub arrives as the dash ends)

```text
room empty
fps 60
end 4
player 2 4
spawn grub 8 4
0.5 dash right
```

The 30 FPS variant is identical except `fps 30`.

Observed (60 FPS trace):
- Frame 31, t=0.517: dash starts, `invulnerable=True` (why: dash).
- Frame 45, t=0.750, one step with these events in order: `invulnerable False (dash timer ended)`, `dash_end`, `invulnerable True (hurt)`, `hurt {source: grub, hearts: 2}`. The player is at x=6.00, the full 4 tiles.
- The player view prints `0.750  YOU ARE HIT by a grub — hearts 2/3` in the same snapshot where the dash has just ended.
- Frames 31–45 are 15 frames, which is 0.25 s. Frame 45 is therefore the last frame of the dash, not the first frame after it.

Observed at 30 FPS: same pattern. The hit comes on frame 23 (t=0.767), the frame where `dash timer ended`, with hearts 3 → 2. The dash is frames 16–23.

Expected: no damage until the dash is over. A Grub touching the player on the last dash frame should not hurt. Damage may start only after the dash ends, and the normal hit rules then apply: 1 heart, 0.3 s hit-stun, invulnerable until 0.8 s after the hit.

### Boundary and variations (one condition varied at a time)

- **Grub contact during the dash, earlier than the last frame.** Script: `player 2 4`, `spawn grub 5 4`, `0.5 dash right`, at 60 and 30 FPS. The player passes through the Grub and takes no damage during the dash (hearts 3 at t=0.75 / 0.767). The first hit comes later, at t≈1.433, after the dash has ended. That is correct behavior.
- **Contact on the last dash frame** (the reproduction above): damage is taken. This is the defect.
- So the faulty window appears to be only the final dash frame: about 0.0167 s at 60 FPS and 0.033 s at 30 FPS. It occurs when an enemy's contact is evaluated on that frame.
- **Frame-rate dependence:** reproduced at both 30 and 60 FPS. The defect is not caused by frame rate, but the window is twice as long at 30 FPS.
- **Not yet tested:**
  - Spitter projectiles landing on the last dash frame.
  - Contact on the first dash frame.
  - A dash with a queued attack.
  - Dashing in other directions.
  - Rooms 1–5 with several enemies.

  The acceptance criteria below include these, so the fix is verified against them.
- **Hypothesis, not confirmed:** the dash timer is cleared and invulnerability is dropped before the contact/damage check runs in the same frame. The engineer should confirm or refute this.

### Existing tests

`python3 -m unittest discover -s tests`: 7 tests, all OK. None covers damage at the dash boundary.

### Severity and frequency

- Severity: hurts the experience. The dash is the player's defensive tool, and a dash that visibly completes and still hurts feels broken. It does not block progress.
- Frequency: low per dash, because the window is one frame. It becomes more common against Grubs, which chase the player and often arrive at the dash end point. It is reproducible with the script above every time.

## Decisions already made

D-001: one attack button plus dash. No new inputs. The fix needs none.

## Constraints

- Must play correctly at 30 and 60 FPS.
- Prefer changes that reuse existing systems.
- Do not change the documented dash rules (0.25 s, 4 tiles, 0.6 s cooldown) or the hit rules (hit-stun 0.3 s, invulnerable until 0.8 s after the hit).

## Open questions

None for the design: the intended behavior is documented. One detail is for the engineer to confirm against `design/combat.md`. If an enemy touches the player on the last dash frame, the player may be hit on the next frame once the dash is over, as long as the enemy is still in contact. The document does not forbid this, and QA treats it as acceptable. If the engineer thinks a short grace period after the dash is needed, hand it to `game-designer` rather than adding one.

## Expected output

A fix with a regression test. The test must cover the last-dash-frame boundary at 30 and 60 FPS. Put the build notes (root cause, what changed, tests run) in the outgoing Handoff and address the result to `studio`, which will route it to QA for independent verification against the acceptance criteria below. Hand back instead if the work needs a decision you do not hold (spec gap, plan not workable).

### Acceptance criteria (player-observable)

1. **Repro script, 60 FPS.** The script above no longer shows `hurt` at t=0.750. Hearts stay 3/3 through the dash. Any later hit happens only after the dash has ended (t > 0.75 s) and follows the normal hit rules.
2. **Repro script, 30 FPS.** The same script with `fps 30` shows no `hurt` at t=0.767. Hearts stay 3/3 through the dash. Any later hit happens only after t=0.767.
3. **In the trace at both frame rates,** no `hurt` event appears in a frame where `dash_left` was still above 0 at the start of that frame, or in the frame in which the dash ends. `invulnerable` stays True from the dash start until the dash end frame.
4. **Pass-through regression.** `player 2 4` / `spawn grub 5 4` / `0.5 dash right` still gives no damage during the dash at 30 and 60 FPS, and the first hit still comes after the dash.
5. **Other attackers.** A Spitter projectile reaching the player on the last dash frame, and on the first dash frame, does no damage at 30 or 60 FPS. QA will check this with `spawn spitter` scripts.
6. **Normal rules unchanged.** Outside the dash, a Grub bite still costs 1 heart, with 0.3 s hit-stun and invulnerability until 0.8 s after the hit. The dash still covers 4 tiles in 0.25 s with a 0.6 s cooldown. A queued attack still fires when the dash ends.
7. `python3 -m unittest discover -s tests` passes, including the new boundary test.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, design/combat.md, manual.md, repo/README.md, repo/play.py, repo/tests/test_game.py, repo/game.py
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-dash-damage/01-studio-to-qa.md
