---
kind: handoff
goal: G-001
seq: 19
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 19: studio → gameplay-engineer — finish Build: write `manual.md` (T8) and confirm `run_tests`

## Task

Write `manual.md` at the project root (T8). Use the draft in handoff 18, section "Draft `manual.md`", and place it unchanged unless a statement in it contradicts the built game. Then run `run_tests` against the real layout and confirm that all 34 tests pass, `ManualTest` included. `manual.md` is the only file to write for this step; no code changes are expected.

## Context

G-001, Build of Option A (build 0.5). Handoff 18 reports T1–T7 and T9 done in `repo/`. T8 was blocked because `manual.md` was not writable in that step. This step exists to do T8 only, and `manual.md` is in scope here. AC-15 and V-5 depend on the manual, and QA cannot start until it exists.

## Findings

From handoff 18, the facts this step relies on:

- 33 of 34 tests passed; the one error was `ManualTest`, caused by the missing `manual.md`.
- The draft was written to contain the backticked glyphs and key phrases `ManualTest` checks. It has not been run against the real file.
- The glyph table, line strings and as-built values are in handoff 18 and in `repo/play.py` (`GLYPHS`, `LINES`).

## Decisions already made

D-001…D-004 hold. The manual is player-facing: it must not name internal states, plan IDs (F1–F11) or acceptance-criterion numbers.

## Constraints

- Write only `manual.md`. If `ManualTest` fails against the draft, or a draft statement contradicts the built behavior, fix the wording in `manual.md` only. If the test or the game would have to change, stop and report it; do not change code in this step.
- Keep the script format and controls consistent with `repo/play.py`.

## Open questions

- If `manual.md` still cannot be written, say so as the first line of Findings and set `outcome: question`. Do not retry or work around it; the Studio will then escalate to the Owner, since a second hand-back for the same input is not routed to a Role again.

## Expected output

An outgoing Handoff addressed to `studio` (so the Route can compose a fresh Handoff for QA without the Sender assessment), with `outcome: done` and Findings giving:

1. confirmation that `manual.md` exists at the project root;
2. the `run_tests` result (count and any failures);
3. any wording you changed from the draft and why.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: manual.md (to create), design/combat-visuals.md, design/combat.md, repo/play.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-003-run-end-and-room-rules.md, decisions/D-004-option-a-single-change-set.md
- Previous handoff: goals/G-001-combat-monotony/18-gameplay-engineer-to-studio.md
