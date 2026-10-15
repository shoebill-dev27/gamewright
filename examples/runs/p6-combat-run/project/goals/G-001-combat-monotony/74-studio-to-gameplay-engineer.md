---
kind: handoff
goal: G-001
seq: 74
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 74: studio → gameplay-engineer — Apply the five rulings of 73 and fix the failures from 70

## Task

Change the build so that it follows the five rulings in `73-game-designer-to-studio.md` (cell at an exact half tile, one meaning of "on you", side word of an enemy not on you, hit-line word fixed at Strike start, knockback of an on-you grub). Also fix the failing `CrowdTest.test_hit_stun_is_short` and the display defects from 70. Add or adjust tests for AC-28(b), AC-29 and AC-30.

## Context

G-001 (combat feels monotonous), Option A (D-002). AC-19…AC-28 were built in 67. QA's verification (70) failed on AC-17, AC-22 (suite), AC-28(b) at 30 FPS, V-10, V-14, V-16 and V-15 (manual text, which is an Owner step). Three spec gaps caused most of this. The game-designer settled them in 73 and D-014, and the criteria were changed in `design/combat.md` (AC-17, 28, 29, 30) and `design/combat-visuals.md` (V-10, 12, 14, 16, 18). No Plan stage is needed; the change is local to the existing simulation and display code.

## Findings

What to build (details and reasoning in 73 "Rulings"; the design documents hold the exact criteria):

1. **Cell rule.** `cell(v) = floor(v + 0.5 + 0.005)` per axis, for the player and for enemies. It replaces the `int(round(...))` in `cell_of`, which is float-noise sensitive at .5. A displayed side for an on-you enemy must be a cell inside the room (the `player 14.5` case: show and knock left from the first draw).
2. **On you.** True distance to the player ≤ 0.5 tile (the `BODY_HIT` radius, tolerance 1e-6). Use it for the `on you:` entry, the displaced glyph, "(on you)" in telegraph, open and hit lines, and the knockback. Remove the 0.05-tile `ON_TILE` test for text and knockback. A draw never has both a side word and an `on you:` entry for the same enemy.
3. **Side word of an enemy not on you.** From the cell offset to `P`. If it shares the player's cell, use the larger true-offset axis (tie: horizontal). The distance suffix rule is unchanged.
4. **Hit-line word.** For a grub, store the position word at the instant the Strike begins (end of Wind-up) and use it in the `hurt` event and the hit line. Do not use the lunge position at the damage tick. Spitter hit lines are unchanged.
5. **Knockback of an on-you grub.** Toward the side it is drawn on; end point 1.0 tile from the player's true position on that side. The normal case (more than 0.5 tile away) stays "straight away". `spawn grub 8 4` still ends at 9.00.

Also fix from 70:

- `CrowdTest.test_hit_stun_is_short` fails at both frame rates. Find out whether the test or the build is wrong. The spec is the 0.15 s hit-stun in D-011 and AC-22. If the build is wrong, fix the build. If the test is wrong, fix the test and say why in the build notes. If the spec itself is unclear, hand back `question`; do not decide.
- The 30 FPS display mismatch (D-A) and the hit-line word (D-C) are covered by rulings 1–4.
- The last suite run in your environment had two `ManualTest` errors from a missing `manual.md`. Make sure `manual.md` is available when you run `run_tests` (read it; do not edit it).

## Decisions already made

- D-001: no new buttons. D-002, D-004, D-005, D-007: Option A, single sequential change set, the Owner places manual text.
- D-011: grubs take turns, two deep; hit-stun 0.15 s; body hit; dash sets facing.
- D-012: `on you:` line and attacker position in hit lines.
- D-013: knockback of a grub on the player's tile (direction and end-point wording superseded by D-014 where they differ).
- D-014: one rule for cells, sides, "on you" and the hit-line word (the rulings above).

## Constraints

- Do not change any number (timings, the 0.5 tile radius, the cap, spacing). The only new use of a value is the "on you" radius, which equals the existing `BODY_HIT`.
- Must play correctly at both 30 and 60 FPS.
- Do not edit `manual.md` (the Owner's) or the design documents.
- No new input buttons. Reuse existing systems.
- If AC-2, 4, 5, 7, 11, 19, 21, 23–27 or AC-28 a/d/e stop passing because of your change, report it; do not change a number to fix it. AC-21 has a thin margin (1.97 s, limit 1.9).
- If the spec is ambiguous, contradictory or missing a case, stop and hand back `question` to `studio`.

## Open questions

- Which side is wrong in `test_hit_stun_is_short`, the test or the build (answer in the build notes)?

## Expected output

Build notes in an outgoing Handoff addressed to `studio` (so that the Studio can compose the QA step from permitted information). They must contain:

- what changed, by file;
- the `run_tests` result with `manual.md` present (count and any failures);
- trace or play evidence at 30 and 60 FPS for AC-28(b), AC-29 and AC-30;
- the answer to the open question;
- anything in the 73 "Previously passing behavior that changes" list that behaved differently than described.

Keep your own reasoning and self-test verdicts under `## Sender assessment`; it is removed before QA receives the Handoff.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, design/combat.md, design/combat-visuals.md, manual.md (read only), repo/README.md, repo/game.py, repo/play.py, repo/bots.py, repo/tests/test_game.py (build in repo/; run commands in project.md)
- Decisions: decisions/D-011-grub-turns-stun-body-hit-dash-facing.md, decisions/D-012-on-you-line-for-displaced-enemies.md, decisions/D-013-knockback-of-grub-on-players-tile.md, decisions/D-014-one-rule-for-cells-on-you-and-hit-line-word.md
- Previous handoff: goals/G-001-combat-monotony/73-game-designer-to-studio.md (read for the rulings; its Sender assessment is the designer's own reasoning), with failures in goals/G-001-combat-monotony/70-qa-to-studio.md
