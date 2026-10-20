---
kind: handoff
goal: G-001
seq: 19
from: studio
to: qa
stage: Verify
outcome: routed
---
# 19: studio → qa — Verify build 0.5 against criteria 1–16 and V12; settle 16e from the new log

## Task

Verify the current build (`repo/`, sha 29993eac7bb0) independently against the combat acceptance criteria 1–16 and the timing item V12 of the visual spec. Specifically close criterion 16e (frame-rate behavior of the walker bot) using the richer `log on` output.

## Context

Goal G-001 ("戦闘が単調なので改善したい", combat feels monotonous). Build 0.5 added combat variety. The designer ruled criteria 13–16 and confirmed five spec defaults. QA's earlier check found the walker bot's 30 and 60 FPS runs differ, with no build defect shown, but 16e could not be proven because the log had no positions. A tooling step has since made the bot log carry decision-time state. Per the designer's ruling, the walker only has to meet 13 and 14 at each frame rate, and the dodger must agree across rates (16c).

## Findings

Facts about what changed since your last report (no judgment attached; verify them yourself):

- `repo/bots.py` changed in its logging only. Bot decisions are meant to be unchanged.
- `repo/tests/test_game.py`: the walker `expectedFailure` test was replaced by a test of criteria 13 and 14 at each rate. Two tests were added for the log. `repo/README.md` describes the new log.
- `repo/game.py`, `repo/play.py` and `design/combat.md` are not meant to have changed.
- `log on` now adds, after each decision line, ` | frame, grid time, frame time, player position, hearts, stun state, nearest enemy position and exact distance, shots in flight`. It also adds heart-loss lines and skipped-decision lines (while the player is stunned). See `repo/README.md` for the format.
- Commands (from the project): tests `python3 -m unittest discover -s tests`; bots `python3 bots.py {script}`; player view `python3 play.py --view player {script}`; trace `python3 play.py --view trace {script}`. Run from `repo/`. The script syntax is in `repo/manual.md`; the log switch and frame-rate options are in `repo/README.md`.

Scope of the verification:

1. Criteria 1–16 in `design/combat.md`, including the designer's rulings for 13–16 (see handoff 14).
2. 16e: run the walker bot in room 3 with `log on` at 30 and 60 FPS. Compare decisions and states by the 16e rule as ruled. State whether any frame-rate-dependent graze at the contact edge exists. Also report whether the first walker difference in room 1 at 0.30 s is explained by the exact distance values in the log.
3. Regression check: bot results with `log on` versus log off, and the existing tests.
4. V12 only (timing of the cues), from the art review (handoff 15). V1–V11 concern a future graphical build and are out of scope. Report, but do not rule on, any contradiction between `design/combat.md` and `design/combat-cues-visual-spec.md`.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- Designer's rulings on criteria 13–16 and the five spec defaults (handoff 14, Findings).

## Constraints

- Judge from the spec, the acceptance criteria and the build only.
- Supported frame rates: 30 and 60 FPS.
- Do not edit the game. Report failures with a reproduction.
- If one criterion fails for the second time, the Studio re-plans via `technical-director`; report precisely which criterion and how.

## Open questions

- Does 16e hold, or does the log show a frame-rate-dependent graze at the contact edge? If it does, state it as a finding. The designer decides whether it is acceptable.

## Expected output

A pass/fail report per criterion (1–16, V12) with reproduction steps for any failure, and a clear 16e conclusion. Address the result to `studio`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md, design/combat-cues-visual-spec.md (V12), repo/manual.md, repo/README.md, repo/bots.py, repo/tests/test_game.py, repo/game.py, repo/play.py
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: none. Read these only in the sections named, ignoring any `## Sender assessment`:
  - goals/G-001-combat-monotony/14-game-designer-to-studio.md#findings (the criteria rulings and checklist items 1–6)
  - goals/G-001-combat-monotony/15-art-director-to-studio.md#findings (V12 only)
  - goals/G-001-combat-monotony/16-qa-to-studio.md#findings (your earlier divergence report)
