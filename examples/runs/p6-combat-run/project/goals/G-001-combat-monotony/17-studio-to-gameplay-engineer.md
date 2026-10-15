---
kind: handoff
goal: G-001
seq: 17
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 17: studio → gameplay-engineer — Build the Option A combat rework (build 0.5)

## Task

Implement the Option A combat rework as one sequential change set (tasks T1–T9 in handoff 14), following the spec `design/combat.md` (AC-1…AC-17), the visual spec `design/combat-visuals.md` (V-1…V-8), the run/room rules in D-003, and the spit-line requirement from handoff 15. Stop and hand back if the spec is ambiguous or contradictory; do not decide design questions.

## Context

G-001, "Combat feels monotonous". D-002 chose Option A: rework existing enemy behavior (telegraphed grub and spitter state machines, attack-slot limit, spitter aim-lock, run/room flow). Design is done. The Technical Director found the spec feasible (14). QA reproduced the duplicate spit line (15). The art-director reviewed the visuals (16). Build under change: `repo/` at sha e54837757611 (version 0.4).

## Findings

**Plan (handoff 14, read it in full).** Key points:
- Elapsed-seconds timers with leftover carry; swept strike check; tick order in `step()` as in section 2; no new modules.
- Task order T1 sim core → T2 player attack → T3 run/room flow → T4 trace → T5 player view (data tables `GLYPHS` and `LINES` in `play.py`) → T6 bots → T7 tests → T8 `manual.md` → T9 as-built report.
- Test strategy per AC in section 4, with timing tests at 30 and 60 FPS.
- Spec gap defaults F1–F11 are set by the Technical Director. Use them unless item 3 below overrides. Report each choice as built.

**Defect report (handoff 15).** The doubled "a spitter spits" line is two spitters each printing the same text, not a double event. It is a presentation defect measured against AC-8. Acceptance criteria for the fix:
1. In rooms 4 and 5, at `fps 30` and `fps 60`, each spit line names its spitter (for example by position).
2. No two lines at the same timestamp have identical text, for 1, 2 and 3 spitters (rooms 3, 4, 5).
3. The number of spit lines at a timestamp equals the number of spitters that fired, and the number of `spit` trace events is unchanged.
4. Each spit line can be matched to its projectile's `*`.
5. Spit timing and projectile behavior are unchanged apart from what the rework intentionally changes.

**Visual spec (handoff 16, `design/combat-visuals.md`).** Rulings to implement:
- The glyph carries the state, not color alone. Uppercase means committed to hurting (`G`, `W`, `S`, `Z`); lowercase means harmless (`g`, `w`, `s`, `z`). A damaged enemy uses the `w/z` family.
- Orange/red is reserved for telegraphed enemies and `*`. The player, the swipe arc and `x` never use it. Harmless enemies are muted.
- Extra room draws at Wind-up start, Charge start, projectile spawn, every swipe, grub Recovery start and player down. Timings are untouched.
- Text lines name the enemy and its position, for example "a grub rears back (left)". Add the "the grub is open" line at the start of grub Recovery and a spitter stagger line.
- Swipe arc glyphs `) ( ^ v` in lantern color on the tiles in reach.
- The run-over screen adds "press attack to start again".
- Optional, for the designer: a visible invulnerability marker (`p` for `P`). Do not add it unless the designer specifies it.

**Studio notes on how the plan and the visual spec fit together:**
1. The extra draws on events are the same thing as the plan's T5 "snapshots". Build them. If they turn out not to be cheap, hand back with `outcome: question` and do not drop them silently.
2. `manual.md` (T8) is yours. Include the glyph table, `x`, the swipe arc, the practice room, the new lines and the run-over screen. Describe behavior; do not copy [tune] numbers. Write it player-facing only.
3. Where handoff 14 (F9, glyph defaults) and `design/combat-visuals.md` differ, follow `design/combat-visuals.md` for glyphs, colors and line wording, and say so in the as-built report. Rules, timings and parameters come only from `design/combat.md`, D-003 and the plan.
4. Pause (F11): no implementation, per the plan.

## Decisions already made

- D-001: one attack button plus dash; no new inputs.
- D-002: Option A, reuse existing enemy behavior; B deferred, C out of scope.
- D-003: room mix across rooms; zero hearts ends the run; clear heals one heart.
- D-004: Option A is built as one sequential change set on the existing simulation; no isolated workspaces.

## Constraints

- Correct at both 30 and 60 FPS. Reuse existing systems; small team.
- No new input buttons (attack, dash, pause only).
- Do not change rules, timings or parameters in `design/combat.md` beyond the plan's gap defaults.
- Keep the shot shape `[x, y, vx, vy]` and the meaning of `cleared`, so `bots.py` keeps working.

## Open questions

- None blocking Build. Non-blocking for the designer at Review: F1 (grub speed 2.0 vs 1.2 in 0.4), F6, F7.
- If a spec ambiguity or contradiction stops you, hand back to `game-designer` via the Studio with `outcome: question`.

## Expected output

- T1–T9 in one change set: passing `run_tests`, `run_bots` at 30 and 60 FPS, updated `manual.md`, and the as-built report with the values listed in handoff 14 section 5 plus the visual tables and strings.
- Address the result to `studio`. The Studio composes the verification Handoff for QA, which must not see implementation reasoning, so keep verdicts and reasoning in `## Sender assessment`.
- Do not write verification verdicts for QA or the art-director.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, design/combat.md, design/combat-visuals.md, manual.md, repo/README.md, repo/game.py, repo/play.py, repo/bots.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-response-scope.md, decisions/D-003-run-end-and-room-rules.md, decisions/D-004-option-a-single-change-set.md
- Previous handoff: goals/G-001-combat-monotony/14-technical-director-to-studio.md, goals/G-001-combat-monotony/15-qa-to-studio.md, goals/G-001-combat-monotony/16-art-director-to-studio.md
