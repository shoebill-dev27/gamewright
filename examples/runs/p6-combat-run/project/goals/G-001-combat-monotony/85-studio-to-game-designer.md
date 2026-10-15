---
kind: handoff
goal: G-001
seq: 85
from: studio
to: game-designer
stage: Diagnose (room-1 play findings against the held items)
outcome: routed
---
# 85: studio → game-designer — Diagnose the room-1 play findings (84) against the held items A4, D1, D2

## Task

Diagnose the experience findings in `84-playtester-to-studio.md`. For each finding, say whether it is (a) a real design issue, (b) an artifact of blind scripted play, (c) a possible implementation mismatch with the spec, or (d) already covered by a held item (A4, D1, D2 in 59) whose revisit trigger now fires or does not fire. Give options only for real design issues.

## Context

G-001, Option A (D-002). The reworked grub behavior (D-011), the display rules (D-012…D-014) and AC-19…AC-30 are built and verified at 30 and 60 FPS, with no failing criterion. A fresh playtester then played room 1 only (84), through input scripts written blind. All three sessions ended in defeat in room 1, and rooms 2–5 were not seen. A second fresh playtester is being sent to rooms 3–5 in parallel (86). Its report will come later, so scope this diagnosis to room 1 and say what further evidence would change it.

This is the second re-entry into Diagnose (earlier passes: 03, 51). The Studio expects measurable progress. If nothing in 84 exposes a gap in the current design, say so and recommend Review. Do not invent changes.

## Findings

Summary of 84. Read the full report for scripts and quotes.

- Three scripted sessions in room 1 at 30 FPS. The scripts had fixed times and could not react in real time.
- First-run defeats came at about 4.0 s (s1), 3.9 s (s2) and 7.4 s (s3). The auto-restarted runs in s1 and s2 also ended in defeat. The playtester never cleared room 1.
- Once flanked, hearts went from 3 to 0 in about 2 s of contact. Bites came about 1 s apart (s1 3.0 and 3.97; s2 1.97, 2.97 and 3.93; s3 5.4, 6.4 and 7.4).
- The player was "stunned" on swipes at 3.0 s and 10.0 s (s1) and 5.4 s (s3). The grub becomes "open" about 0.1 s after it hits, but the player is stunned and cannot use the opening. The playtester found this unfair.
- The "rears back" cue comes about 0.5 s before the bite and was readable. The playtester called the gap short.
- A dash on the cue (s3) avoided the bite and cost nothing. It was the only fight moment that felt skillful.
- The fights felt the same. The three grubs behave identically, the only decision was "when to dash", and moving away did not shake the grubs.
- There was no on-screen indication of facing. The "on you:" lines were hard to read when a grub shares the player's tile.
- Most swipes missed ("too far", "not in front"). The playtester attributes this to blind scripting and does not count it as a defect.
- Positives: clear telegraph letters, i-frames that feel good when timed, and a fast restart.

Limits on the evidence: room 1 only, scripts without live reaction, text frames only (no colour, sound or controller feel). Repeated in all three sessions: flanking deaths, stun after a hit, uniform fights. Seen once: the successful dash and the one grub defeated.

## Decisions already made

- D-001: attack and dash only, no new buttons. A facing indicator is a display matter, not an input.
- D-002: Option A, rework existing enemy behavior first.
- D-003: room mix across rooms; zero hearts ends the run.
- D-011: grubs take turns and crowd two deep; hit-stun 0.15 s; body hit; dash sets facing.
- D-012 to D-015: the display rules for "on you", cells and hit lines.

## Constraints

- Stay within the vision, D-001 and the existing Decisions. Prefer changes that reuse existing systems.
- A direction or priority change (for example, giving up an Option A scope boundary) goes to the `game-director`. State it as a need and do not decide it.
- Play must stay correct at 30 and 60 FPS.
- You cannot rule on root cause or on pass/fail. If a finding looks like the build differing from D-011 or an AC (for example, stun lasting longer than 0.15 s, or grubs not taking turns), write it as a question for `qa` with a script to run.

## Open questions

1. Do the observed deaths in room 1 (about 2 s from first contact to defeat, three times) match what D-011 and the room 1 composition (D2) intend? Does the D2 revisit trigger fire?
2. Is the stun-while-open sequence what D-011 specifies (hit-stun 0.15 s against the grub's open window)? If it is, is it a design problem? If not, is it a possible defect?
3. Does the lack of a facing indicator fire the D1 revisit trigger? Does "dash sets facing" change the reading?
4. Do "the fights felt the same" and "moving away did not shake the grubs" fire the A4 revisit trigger, or are they room-1 effects of using one enemy type?
5. What evidence would settle anything you hold: a bot run by `qa`, a live human, or the rooms 3–5 playtest in 86?

## Expected output

A diagnosis handoff addressed to `studio` (`stage: Diagnose`). It should contain:

- (a) items to hold, with their revisit triggers;
- (b) possible defects, as questions for `qa`;
- (c) design issues, with options and a recommendation;
- (d) anything that implies a direction or priority change, flagged for the `game-director`.

If you change a held item or a spec, say so and name the files. The Studio routes next.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/diagnose-experience.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, design/combat.md, design/combat-visuals.md, goals/G-001-combat-monotony/59-game-designer-to-studio.md (held items and revisit triggers)
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-response-scope.md, decisions/D-003-run-end-and-room-rules.md, decisions/D-011-grub-turns-stun-body-hit-dash-facing.md
- Previous handoff: goals/G-001-combat-monotony/84-playtester-to-studio.md
