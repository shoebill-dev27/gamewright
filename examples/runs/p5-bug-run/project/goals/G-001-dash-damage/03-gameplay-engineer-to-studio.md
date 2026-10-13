---
kind: handoff
goal: G-001
seq: 3
from: gameplay-engineer
to: studio
stage: Verify
outcome: done
---
# 03: gameplay-engineer → studio — Dash last-frame damage fixed; route to QA for verification

## Task

Route to `qa` for independent verification of the fix for damage taken on the last frame of a dash, against the acceptance criteria in handoff 02.

## Context

Goal G-001. QA's defect report (02) showed the player took damage on the final frame of a dash, although `design/combat.md` says the player is invulnerable for the full dash duration. The fix is in `repo/game.py`; regression tests are in `repo/tests/test_game.py`. No new inputs (D-001) and no design change.

## Findings

### What changed

- `repo/game.py`, `Game.step`: invulnerability from the dash is no longer dropped the moment the dash timer reaches 0. The dash-end frame is flagged (`dash_ended_now`), and the protection is released only after that frame's enemy-contact and projectile checks. The `dash_end` event is still logged in the same frame, and so is `invulnerable False (dash timer ended)`, now after the damage checks.
- New helper `Game._sync_invulnerable`: invulnerable while any source holds (dash active, dash-end frame, or hit timer running). The hit timer ending during a dash therefore no longer cancels dash protection.
- Dash rules (0.25 s, 4 tiles, 0.6 s cooldown), hit rules (1 heart, 0.3 s stun, 0.8 s invulnerability) and the queued attack on dash end are unchanged.
- `repo/tests/test_game.py`: new `DashInvulnerabilityTest` at 30 and 60 FPS:
  - Grub contact on the last dash frame: no hurt in or before the dash-end frame, and hurt only afterwards under normal rules.
  - Invulnerable throughout the dash and dropped on the last frame.
  - Pass-through of a Grub mid-dash, with hits only after the dash.
  - Spitter-style shot on the last dash frame and on the first dash frame: no damage.
  - A shot after the dash ends: damage.
  - A hit timer ending mid-dash: dash protection is kept.

### How to exercise

- Repro script from 02 with `fps 60` and `fps 30` via `python3 play.py --view trace <script>`. Expected: no `hurt` in the dash-end frame (frame 45 at 60 FPS, frame 23 at 30 FPS). The first `hurt` comes in a later frame, with normal hit rules after it.
- Pass-through script (`spawn grub 5 4`) at both frame rates.
- Spitter scripts with `spawn spitter` for criterion 5.
- `python3 -m unittest discover -s tests`.

### Criteria addressed

1, 2, 3 (last-frame behavior), 4 (pass-through), 5 (projectile tests, plus the Grub), 6 (rules unchanged, covered by the existing tests), 7 (test run).

### Known risks

- After the dash ends, an enemy still in contact can hurt on the very next frame. 02 accepts this, and no grace period was added. If QA or the Owner wants one, it is a `game-designer` decision.
- Not exercised by me in play scripts: dashing up or down, rooms 1–5 with several enemies, and a queued attack combined with last-frame contact. QA should check them.

## Decisions already made

D-001: one attack button plus dash; no inputs added.

## Constraints

- Plays correctly at 30 and 60 FPS.
- No change to documented dash or hit rules.

## Open questions

None.

## Expected output

A QA verification verdict (pass/fail) against the acceptance criteria in handoff 02, with the reproduction and trace evidence at 30 and 60 FPS.

## Sender assessment

- Root cause (confirmed): in `Game.step`, the dash branch called `_set_invulnerable(False, "dash timer ended")` as soon as `dash_left` reached 0. `_update_enemies` and `_update_shots` run later in the same step, so a Grub contact or shot on the dash's last frame saw `invulnerable == False`. The shared path is the invulnerable flag. The fix covers Grubs and shots together.
- Evidence: after the first fix proposal, the 60 FPS trace of the repro showed `dash_end` and `invulnerable False` at frame 45 (t=0.750) with no `hurt`. The first `hurt` came at frame 46 (t=0.767), after the dash.
- Test run on the proposed change: 3 failures, all in my new tests, none in the fix. (a) The pass-through test assumed exactly 2 hearts after 2 s, but the Grub keeps biting every 0.8 s. (b) The last-frame shot test at 30 FPS stopped one frame early, because 0.25 s is 7.5 frames and the rounded run length was wrong. I corrected both: (a) now checks the first hit time and `hearts < HEARTS`, and (b) steps until the next step ends the dash.
- The corrected tests were not re-run after these two edits, so QA's independent run of the suite is the first confirmation. The other 12 tests passed in the earlier run. My confidence in the fix is high. My confidence that the corrected tests pass is moderate-high.
- Unconfirmed: 02 says the first hit in the pass-through script comes at t≈1.433. I did not re-trace that and did not rely on the figure in the test.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#constraints, design/combat.md, manual.md, repo/README.md, repo/play.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-dash-damage/02-qa-to-gameplay-engineer.md
