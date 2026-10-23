---
kind: handoff
goal: G-001
seq: 12
from: studio
to: art-director
stage: Verify
outcome: routed
---
# 12: studio → art-director — Review the new combat cues for readability (build 0.5)

## Task

Review the threat cues added in build 0.5 against the art direction and the "readable threats" pillar. The build is a headless text view, so judge what the cues must look like in a graphical build, and report concrete requirements or problems.

## Context

G-001 (combat monotony). The combat redesign adds telegraphed attacks so the player can read a threat and respond (dash, sidestep, swipe). The cues are new visuals. QA verifies behavior separately; you judge readability and consistency.

## Findings

Cues as they appear in the player view (`run_play`):
- **Grub wind-up (0.5 s before the lunge):** a line `a grub rears back`, plus a snapshot where the lunge path is a row of `~` marks (2.4 tiles) from the grub along the locked direction. Under the room: `cue: g at (x,y) flashes orange-red, lunge line toward (ux,uy), 2.4 tiles (0.50 s to the lunge)`. Variants: Runner (mark `r`) and Brute (mark `G`) have different wind-up lengths per `design/combat.md`.
- **Spitter aim (0.6 s before the shot):** `a spitter takes aim`, `~` marks along the locked line to the room edge, and `cue: s at (x,y) glows orange-red, brightness NN%, aim line toward (ux,uy) (0.60 s to the shot)`. Brightness rises from 0% to 100%. Then `a spitter spits` and the shot `*` moves along the line.
- The flash, glow and line are described only in text. Color and look are not rendered.

## Decisions already made

- D-001: one attack button plus dash.
- Art direction (project.md): dark caves lit by the player's lantern, warm light against cold blue-black; threats use saturated orange/red so they read against the dark.

## Constraints

- Small team: prefer requirements that reuse existing assets and effects.
- Threats must be visible before they can hurt the player (pillar 3). Multiple enemies can be on screen, so cues must stay distinguishable from each other, from shots, and from the lantern light.
- Do not change timings or rules; those belong to the game-designer. If a readability problem needs a timing or rule change, say so in your report.

## Open questions

1. Are the cue forms (flash, lunge line, aim line, glow ramp) readable and consistent with the art direction? Any clash or ambiguity (e.g. lunge line vs aim line vs shot)?
2. What must a graphical implementation satisfy (contrast, shape, duration visibility, differentiating Runner/Grub/Brute and spitter), stated player-observably?

## Expected output

A report with findings and player-observable visual requirements or acceptance criteria. Address the result to `studio`. Do not change the game design files unless your findings name them.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md
- Project: project.md#art-direction, project.md#constraints, design/combat.md, repo/manual.md, the build (repo/; `python3 play.py --view player {script}`, script format in repo/manual.md)
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: none
