---
kind: handoff
goal: G-001
seq: 96
from: gameplay-engineer
to: studio
stage: Verify
outcome: done
---
# 96: gameplay-engineer → studio — Shot-hit source (A) and late-swipe line (B) built, ready for QA

## Task

Verify the wording-only build of `design/combat-step94.md` (W1–W8) at 30 and 60 FPS with `play.py --view player`, then route to Review pass 4.

## Context

Goal G-001, D-013. Wording only: no rule, number, timing, cap, cue or input change.

## Findings

What changed:
- `repo/game.py`: new `shot_source(vx, vy)` applies the spec formula (reverse of the locked travel vector, 0.4142 sector boundary, eight words). When a shot damages the player, the hurt record name is `shot from the <direction>`, so the existing message system prints `YOU ARE HIT by a shot from the <direction> — hearts n/3`. The direction is read from the shot at the contact frame, before removal. Absorbed shots still log no hurt. The hurt event `source` stays `shot`.
- `repo/game.py` `_attack`: a new `late_swipe` event (enemy variant) when a swipe damages without killing a grub, runner or brute in its lunge phase. It is logged before the `attack` event; the hit line comes in a later step. No state is touched.
- `repo/play.py`: `Player.describe` prints the `late_swipe` event as `the <variant>'s lunge had already started, the swipe was too late to stop it`.
- `repo/manual.md`: the two replacement wordings applied as given in the spec.
- `repo/tests/test_game.py`: the old shot-message test now expects `from the west`; new `ShotSourceTest` (W1, W3, W4 prefix, W8) and `LateSwipeTest` (W5, W6).

How to exercise: practice room, player at (8,4), a single spitter at the placements in W1 (expected: east, north, west, south, north-east, and south-east for (15,7), 3/7 above 0.4142). For W5: grub at (10,4), swipe once the `lunge` trace line appears and the grub is within 1.5 tiles.

Risk check: `bots.py` uses the hurt event `source` (`shot`, `grub`), which is unchanged. No code or test in the repo matches the full string `YOU ARE HIT by a shot` by equality, except the one test updated above. Rules use substring matching (`c[1] in m.lower()`), so `text "by a shot"` still matches.

Criteria addressed: W1–W8. Not covered by tests: W2 (rooms 4 and 5 against `cue:` lines) and W7 comparison traces with the old build; QA should run these.

## Decisions already made

D-001, D-005, D-011, D-013.

## Constraints

Wording only. `takes aim`, `rears back`, `YOU ARE HIT by` and the brute shrug line are unchanged.

## Open questions

None.

## Expected output

QA verdict on W1–W8, then Review pass 4.

## Sender assessment

I did not run the suite or any script in this step (the run rounds were not used), so the new and updated tests are unexecuted. The change is small and uses only existing structures, so I expect green, but QA's run is the first real check. The late-swipe test relies on the grub reaching within 1.5 tiles during the lunge before contact (at 30 FPS the frame positions are x=9.73, 9.47), which should hold.

## Load

- Role: studio/roles/qa.md
- Skills: none
- Project: design/combat-step94.md, repo/game.py, repo/play.py, repo/manual.md, repo/tests/test_game.py
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md, decisions/D-011-variant-named-messages-accepted.md, decisions/D-013-review-pass-3-readability-wording-then-close.md
- Previous handoff: goals/G-001-combat-monotony/95-studio-to-gameplay-engineer.md
