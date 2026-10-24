---
kind: handoff
goal: G-001
seq: 17
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 17: studio → gameplay-engineer — implement revision 2 of the level 1 spec (build 0.3 → next build)

## Task

Change level 1 so that it matches revision 2 of `design/onboarding.md` and Decision D-003, starting from build 0.3. Then state exactly what changed, where, and how to exercise it, so Verify can run again.

## Context

Goal G-001: children aged 7–10 stalled at the start of level 1. Build 0.3 implements options A + B, and QA passed its 12 checks. Verify then found a spec gap: a sand tap 0.6–1.5 s after a pulse got no response, which breaks "no silent touches". The game-designer settled this and some related notes in revision 2 of the spec (Handoff 16). Player-facing behavior changed, so Build and Verify run again before the Playtester session.

## Findings

The designer's changes, summarized. `design/onboarding.md` (revision 2) is authoritative; read it for exact values and edge cases.

1. **Sand-tap blip (new, rule 5, D-003).** A sand tap blocked by the pulse rate limit, landing after the running pulse has ended (0.6–1.5 s after a pulse start), makes the pool brighten 15% within 0.1 s and fade over 0.3 s. It is brightness only, with no scale change. A running blip is not restarted. It is touch-triggered only. A sand tap in the first 0.6 s of a pulse needs no extra response. The pulse rate limit itself is unchanged.
2. **Pool hit area (rule 1, D-003).** The hit area follows the pool's drawn size and is never below the at-rest size. The home-glow distance still uses the at-rest width.
3. **Crab flip target (rule 3).** The crab flips toward the pool's logical position, which is the authored start position during the intro slide and the ease-back after an intro cancel.
4. **Pulse precedence (rules 2 and 5).** The redirect pulse is shown. The idle pulse is not shown during it and resumes from scale 1.00 afterward. The build record does not say whether 0.3 already does this.
5. **Shadow source (check 10).** Not player-facing. A softly drawn ellipse, or an existing sprite with color and size changes, is acceptable. Add no new image asset.

Unchanged: the 0.2 s response criterion, D-002 (intro cancel eases back over 0.15 s; the intro is never in undo history), and the exclusion of option C (idle hint).

## Decisions already made

- D-001: no failure, no timers, every move undoable. Nothing may be triggered by inactivity.
- D-002: intro cancel eases back over 0.15 s; the intro is never in the undo history.
- D-003: rate-limited sand taps show a pool brightness blip; the pool's hit area follows its drawn size.

## Constraints

- Level 1 only. Touch only. No mechanic may depend on text.
- Existing sprite sheet only: color, flip, size, rotation, position and brightness changes, plus a procedurally drawn shadow. No new image assets.
- Dry-run project: the change counts as made once you state it exactly (what changes, where, how to exercise it). `sim/repo-notes.md` stands in for the code.
- Implement the spec as written. If it is ambiguous, contradictory or missing a case, stop and hand back `question`; do not decide design.
- Do not widen scope to levels 2+.

## Open questions

- State in your Handoff whether build 0.3 already showed the redirect pulse over the idle pulse and resumed the idle pulse from scale 1.00 (item 4). Say what you changed if it did not.
- If you find a further spec gap, hand it back as `question`.

## Expected output

Address the result to `studio`, not to QA. The Studio will compose QA's Handoff from permitted information. Write a Handoff that contains:

- the exact changes (what, where, parameters) for items 1–5 and any other rule touched;
- how to exercise each change in the build, including the new and changed checks 4, 10 and 13–16 in the spec;
- the new build record, `sim/build-0.4.md`, if the simulator expects one;
- your own evaluation, only under `## Sender assessment`.

## Sender assessment

None. This Handoff was written by the Studio from the designer's Handoff (16).

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/onboarding.md, sim/build-0.3.md, sim/repo-notes.md, project.md#constraints
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-002-intro-cancel-and-undo.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md
- Previous handoff: goals/G-001-first-puzzle-stall/16-game-designer-to-studio.md
