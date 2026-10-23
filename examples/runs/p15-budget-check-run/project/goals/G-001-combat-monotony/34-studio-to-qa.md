---
kind: handoff
goal: G-001
seq: 34
from: studio
to: qa
stage: Observe
outcome: routed
---
# 34: studio → qa — Trace spitter fire times in rooms 3 and 4 against the spec

## Task

Use the `reproduce-defect` skill to check whether the spitters in rooms 3 and 4 fire at the times and positions `design/combat.md` specifies, and how many shots are in flight. Report whether the build conforms.

## Context

G-001 (combat monotony). A fresh playtest of build 0.5 (rooms 1–5, scripted play) reported:

- in rooms 4–5 the two spitters were in "opposite corners" and "fired in sync";
- in room 3 a double fire at about 5.8 s;
- deaths in room 4 (about 15.75 s) and room 5 (about 11.1 s), from shots, with the player hit while lined up for another warning.

The room table in the design appears to put the two spitters on the same side, and the spec has them firing 0.8 s apart. The Studio does not know which side is right.

## Findings

Nothing yet; this is the Observe step. No change is requested.

## Decisions already made

- D-002: per-frame contact sampling and the contact-edge graze are accepted. Do not report graze cases as defects.

## Constraints

- Report only. Do not change the build, tests or scripts in `repo/`.
- Use the project's run commands (`run_trace`, optionally `run_play`) at both 30 and 60 FPS.
- Verify from the spec and the build, not from a guess about what the designer intends.

## Open questions

- Where is each spitter placed in rooms 3, 4 and 5 (from the trace), and does that match the spec's room table?
- Spitter shot times and cue windows in room 4 (and room 3 around 5.8 s): the offset between the two spitters, and any case where two shots start together or one cue starts less than 0.6 s after another ends. Does it match the spec, at both rates?
- Shots in flight over time in rooms 3–5, against the spec's limit.
- Does a player who stays still, and a player who dodges one line, get hit by a shot already in flight? State which cause (a shot in flight, a new aim lock, or a misread line) you see in each hit.

## Expected output

A handoff addressed to `studio` with the trace evidence (times, positions, rates), a verdict (conforms or differs, and how), and defect details with severity and reproduction steps if the build differs from the spec. State what you did not cover.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md, repo/manual.md, project.md#current-state, the build in repo/
- Decisions: decisions/D-002-contact-edge-graze-accepted.md
- Previous handoff: goals/G-001-combat-monotony/32-qa-to-studio.md
