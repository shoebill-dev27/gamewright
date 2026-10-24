---
kind: handoff
goal: G-001
seq: 55
from: studio
to: qa
stage: Observe
outcome: routed
---
# 55: studio → qa — Check six open facts about the combat build and get bot reference data

## Task

Reproduce or settle the open facts below using `run_play`, `run_trace` and `run_bots`, and report each as it behaves in the build compared with `design/combat.md` and `manual.md`. Write a defect report with acceptance criteria for anything that contradicts the spec.

## Context

G-001 (combat feels monotonous). Two playtest sessions (room 1 in handoff 50; room 2 in 54) ended in quick defeats by scripted play, so the later combat has not been judged. Some of what the playtesters reported cannot be explained from the player view alone. Behavior that the spec does not cover is not a defect; report what happens so the designer can specify it.

## Findings

Facts to settle (the playtester's report, 54, is the previous Handoff):

1. **Possibly short bite warning.** In the room 2 session the run restarted in room 1 after defeat. The log showed "a grub rears back (left)" at 11.90 s and a heart lost at 11.97 s (30 fps), about 0.07 s later. Other bites came about 0.5–0.65 s after their "rears back" line. Use `run_trace` to tell whether any grub strikes sooner than the spec's wind-up allows, or whether the line belonged to a different grub. Repeat at 30 and 60 FPS.
2. **Dash distance.** How many tiles does a dash move in open floor, and next to a wall? A playtester judged it 2–3 tiles; the manual does not say. Compare with the spec.
3. **Facing.** Does a dash change the player's facing? After a dash, does a swipe hit enemies in the original facing, or the dash direction? (The spec may be silent; report what happens.)
4. **Swipe timing against grubs.** Does a swipe hit a grub that is (a) in Strike, (b) in Recovery while adjacent, (c) just after a first hit and knocked back? How many tiles does the knockback move it, and does the swipe print "(miss)" in the case where the grub is out of reach?
5. **Grub "on you".** When a grub shares the player's tile, does a swipe hit it regardless of facing? Report for each of the four facings.
6. **Bot reference data.** `run_bots` failed once with `script line 1: cannot read 'room 1'`: its script format differs from the play-script format. Find the right format (`repo/bots.py`, `repo/README.md`). Run a passive (idle) bot and, if available, a reactive bot on room 1, and on rooms 2–5 if possible. Report clear times, hearts lost and actions used, as numbers; do not judge balance.

## Decisions already made

- D-001: one attack button plus dash.
- D-003: zero hearts ends the run; a room clear heals one heart.
- D-006: enemies may overlap the player and are never hidden.

## Constraints

- Everything must hold at both 30 and 60 FPS.
- Do not change the build. Report only.
- Run at most the rounds you need; say clearly which of the six items you could not settle.

## Open questions

- Which of the six facts contradict `design/combat.md` or `manual.md`, and which are simply unspecified?

## Expected output

A report in a Handoff addressed to `studio`, with: for each of the six items the observed behavior (with the script or trace you used), whether it matches the spec, and for each contradiction a defect with severity and acceptance criteria. Bot data as a table.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md, manual.md, project.md#constraints, the build `repo/` (`repo/README.md`, `repo/bots.py`)
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-003-run-end-and-room-rules.md, decisions/D-006-overlap-display-and-practice-room-manual.md
- Previous handoff: goals/G-001-combat-monotony/54-playtester-to-studio.md
