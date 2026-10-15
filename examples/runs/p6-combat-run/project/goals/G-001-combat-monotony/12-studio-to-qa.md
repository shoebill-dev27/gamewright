---
kind: handoff
goal: G-001
seq: 12
from: studio
to: qa
stage: Observe
outcome: routed
---
# 12: studio → qa — Reproduce and log the repeated spitter attack line

## Task

On the current build, reproduce the spitter attack text that appears to be printed twice, and write a defect report with severity and acceptance criteria.

## Context

During a playtest of rooms 4–5 the spitter's attack line looked doubled. Rooms 4–5 each have spitters that fire a pair of shots on a beat. The design documents say one line per spitter is expected, so two lines may be correct; the problem is that identical lines read as a duplicate. This is a presentation question. The spitter's behavior is about to be reworked (target `design/combat.md`, acceptance criterion AC-8, which requires the line to name the spitter), so the report should say what is observable on the current build, not propose a fix.

## Findings

Nothing yet beyond the observation above. Build under test: `repo/` at sha e54837757611.

## Decisions already made

None that bear on this defect.

## Constraints

- Use the project's run commands (`run_play`, `run_trace`, `run_bots` in `project.md`); a play session is an input script (`manual.md`).
- Check at both 30 and 60 FPS if the script format allows it; say so if it does not.
- Do not verify or comment on the rest of the Option A spec; that is a later step.

## Open questions

- Is the doubled line one event printed twice (a defect), or two spitters each printing their own line (one line per spitter)?
- Does it occur in room 4, room 5, or both? Does it change with the number of spitters?

## Expected output

A defect report (reproduction script, observed vs. expected, severity, acceptance criteria). Address the result to `studio`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md, manual.md, project.md#constraints, goals/G-001-combat-monotony/08-playtester-to-game-designer.md
- Decisions: none
- Previous handoff: none
