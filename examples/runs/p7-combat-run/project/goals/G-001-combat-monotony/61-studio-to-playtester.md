---
kind: handoff
goal: G-001
seq: 61
from: studio
to: playtester
stage: Play
outcome: routed
---
# 61: studio → playtester — Play the combat of the current build as a player, rooms 1–5, with per-enemy reaction rules

## Task

Play the current build as a player would, through input scripts, and report what you experienced. Use the player view (`python3 play.py --view player {script}`) only.

## Context

You are evaluating the combat of a short-session top-down action roguelite. Judge only what you can observe as a player.

## Findings

Not applicable (no implementation information is passed to the Playtester).

## Decisions already made

None.

## Constraints

- Player profile: action players who want short, intense runs; comfortable with dodging and spacing; not interested in memorizing combo lists; mostly play with a gamepad.
- Read the player-visible manual `repo/manual.md` for the controls, the script format and reaction rules. Use the player view; do not use the trace view or the balance bots.
- Do not read source code, design documents or tests.

## Open questions

Please cover these in your report, in your own words:

- What did each enemy mark (`g`, `r`, `G`, `s`) ask of you? Did you answer them the same way or differently, and why?
- How did room 1 differ from room 2, and room 2 from rooms 3–5?
- Was there a point where something felt repeated, or a point where it felt different from what came before?
- Did anything hurt you that you could not explain?

## Expected output

An observation report (templates/handoff.md), addressed to `studio`, from `playtester`, `outcome: done`. In Findings, include:

- the scripts you used (short) and what happened;
- observations from the player's side only;
- the limits of your evidence (scripted reactions, truncated output, anything not played).

How to play:

- Write **separate reaction rules for each enemy mark** (`g`, `r`, `G`, `s`) and say in the report why each rule differs, or why you chose not to make them differ.
- Play **rooms 1 and 2 as well as rooms 3–5**.
- In rooms where you can, include **one run where you try to clear the room as fast as you can** and **one run in the style you like best**.
- Include **one slow, deliberate run** (waiting for the right moment rather than pressing in).
- Keep each script short enough that the output is not truncated: use `end`, and run rooms separately.
- If the manual describes a way to choose the frame rate, also play at least one room at 30 FPS as well as 60.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, repo/manual.md, the build (`repo/`, run with `python3 play.py --view player {script}`)
- Decisions: none
- Previous handoff: none
