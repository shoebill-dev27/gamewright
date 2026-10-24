---
kind: handoff
goal: G-001
seq: 7
from: studio
to: playtester
stage: Observe
outcome: routed
---
# 07: studio → playtester — Play rooms 4 and 5 of the build and report what you experience

## Task

Play rooms 4 and 5 of the build as an action player would, and report what you observe. Rooms 1–3 and the practice room are not part of this round.

## Context

G-001: the Owner finds combat monotonous. This round collects first-hand player experience for rooms 4 and 5, which have not been played yet. You are given no further information about the build, on purpose.

## Findings

Nothing to pass on: your report is the evidence.

How to play: the build is in `repo/`. A session is an input script; `manual.md` describes the controls and the script format. Run a script with:

`python3 play.py --view player {script}`

Use the player view only, as a player would see the game.

Play focus: pay attention to combat.

Please report, as observed:

- Rooms 4 and 5: which enemy types appear, how many, and what they do over time and between rooms.
- Whether rooms 4 and 5 feel different from each other, and how.
- First contact with each enemy type: what you can see before taking damage, and whether you have a way to respond.
- How your choices (movement, timing, attack, dash) affect the outcome. Prefer short scripts, inspecting the result between runs and reacting, over one long blind script per room.
- What you see when your own attack lands, and how many attacks it takes to defeat each enemy type.
- Whether you can approach any ranged enemy, and when.
- How many hits you can take.
- What happens after you go down or clear a room (record only what you observe).
- Anything that looks broken or confusing. Report it as an observation; do not diagnose it.

## Decisions already made

None that you need.

## Constraints

- Act as a player: use only the player view and `manual.md`.
- No new input buttons exist beyond attack, dash and pause.
- Report observable experience only. Do not propose fixes or design changes.

## Open questions

None.

## Expected output

An observation report (templates/handoff.md) addressed to `game-designer`, stage Diagnose. Put the observations in Findings and write nothing about causes or solutions.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, manual.md, the build in repo/ (run with the command above)
- Decisions: none
- Previous handoff: none
