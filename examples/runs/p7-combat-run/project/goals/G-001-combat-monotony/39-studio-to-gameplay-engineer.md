---
kind: handoff
goal: G-001
seq: 39
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 39: studio → gameplay-engineer — Build 0.6: cue gap, brute no-cancel, consumed shots, spent lunges

## Task

Implement build 0.6 in `repo/` per the complete spec in `design/combat.md` (sections marked "step 35" and "step 38") and the change list below. Update tests and the manual. Stop and hand back with a question if the spec is ambiguous, contradictory or missing a case; do not decide design yourself.

## Context

G-001 (combat monotony). Build 0.5 is done and passed QA at 30 and 60 FPS. Playtest 27 and Diagnose 31 found melee enemies sharing one answer and unfair spitter crossfire in rooms 4–5. Design 35 (D-004) specified the cue gap and brute behavior. QA 36 found 0.5 conforms to its spec but left two behaviors undefined; the designer ruled on them in 38 (D-005). The spec is now complete. This Build changes contact consequences only; contact detection stays as it is.

## Findings

Complete change list for Build 0.6 (from handoff 38):

1. Spitter offset per room: 0.8 s default (rooms 1–3, practice rooms); 1.2 s in rooms 4–5 (first shots 1.8 and 3.0 s in those rooms).
2. Cue gap rule in rooms 4–5 only: a spitter starts a cue only if no other spitter's cue is running, the last shot in the room was at least 0.6 s ago (1 ms tolerance), and the cap allows it; otherwise wait 0.2 s and check again. A cancelled cue is not a shot. Room 3 and practice rooms do not use the rule.
3. Brute (`G`) wind-up is not cancelled by a swipe: the swipe deals 1 damage, shows "the brute shrugs off the swipe", the cue and timer continue, and the lunge happens at 0.7 s. Kill during wind-up: no lunge, no message. Flag per variant: standard yes, runner yes, brute no.
4. Dodger bot policy against the brute: sidestep or dash on the cue, swipe in recovery only. Check `repo/bots.py` and change it if needed.
5. Shot consumed on any contact: a shot with contact (distance <= 0.4, unchanged) on a player who is dashing, in hit-stun (0.3 s) or in hurt invulnerability (until 0.8 s after the hit) is removed on that frame with no damage. It does not pass through and does not wait for the window to end.
6. Lunge hit spent: a lunge that makes contact with a protected player deals no damage for the rest of that lunge, even if protection ends while the grub is still in reach. The lunge is not cancelled or shortened. The next lunge damages normally.
7. No change to the cue gap rule for room 3 or practice rooms, and none to contact detection (`distance <= reach` per frame after movement; D-002, D-003).
8. Manual (`repo/manual.md`): update the version number; add the step 35 lines; add (a) "A shot that reaches you while you are dashing or still flashing after a hit is stopped and does no damage." and (b) "A grub's lunge that touches you while you cannot be hurt does no damage, even if your protection ends during that lunge."; amend "A swipe that interrupts a grub's warning staggers it for 0.4 s" with the brute exception.

Also in the build: confirm in code whether 0.5's late damage (QA saw it land exactly at the end of the hurt window: 4.533 / 5.333 s at 30 FPS, 4.483 / 5.283 s at 60 FPS) came from an unconsumed shot. Report what you find; the rule in item 5 holds either way.

Criteria QA will verify (all in `design/combat.md`): new 20 (a–f, shots) and 21 (a–d, lunges); amended 3, 13, 14, 15, 16 (a and e); notes on 11 and 18; existing 18 and 19 stay.

## Decisions already made

- D-001: attack and dash only; no new input.
- D-002, D-003: contact sampling and exact reach, unchanged.
- D-004: cue gap rule and offset in rooms 4–5, brute no-cancel flag, room 2 spitter deferred (Option 3).
- D-005: a contact blocked by invulnerability consumes the shot and spends the lunge's hit; simultaneous cue starts outside rooms 4–5 are accepted.

## Constraints

- Must play correctly at 30 and 60 FPS; all durations on accumulated time.
- Room 3 criterion 11 stays (first shots 1.8, 2.6, 3.4 s ±1 frame).
- No new input, enemy, healing, room content or message beyond those listed. Prefer reuse of the existing enemy update loop.
- Tests: `python3 -m unittest discover -s tests` must pass, with new tests for items 2, 3, 5 and 6 at both 30 and 60 FPS.
- Visual criteria and art-director items are deferred until a graphical build exists; do not act on them.

## Open questions

- Is 0.5's late damage really an unconsumed shot? (Confirm in code; see Findings.)
- Walker hearts in rooms 4–5: two opposite effects (brute lunge no longer cancelled, shots consumed). Run `run_bots` for the rooms and report clear times, hearts lost and actions used against the 0.5 values in handoffs 13–16. Values outside criterion 13–15 limits are tuning for `game-designer`, not a build defect: report them, do not tune.

## Expected output

The changed build in `repo/` (version 0.6), updated tests and manual, and build notes covering what changed per item 1–8, the code finding above, test results and the bot figures. Address the result to `studio` (not to QA), so the Studio can compose an independent Verify handoff. If blocked by an ambiguous or missing spec case, hand back with `outcome: question` to `studio`.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat.md, repo/manual.md, repo/README.md, repo/game.py, repo/bots.py, repo/tests/test_game.py, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-contact-edge-graze-accepted.md, decisions/D-003-contact-edge-exact-reach-and-lunge-band.md, decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md, decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Previous handoff: goals/G-001-combat-monotony/38-game-designer-to-studio.md
