---
kind: handoff
goal: G-002
seq: 2
from: art-director
to: studio
stage: Design
outcome: done
---
# 02: art-director → studio — picture spec for the floor grid is written; a short Plan step is advised

## Task

Route the finished picture spec (`design/entity-pictures.md`) to the next step. I advise a short Technical Director Plan before Build, as the method is risky (see Findings and Open questions).

## Context

Goal G-002. The Owner said 「それぞれに絵をつけてほしい」 ("I want pictures attached to each of them"). The Studio read it as every kind of thing the player sees on the floor grid. The page, the marks (D-002) and the shared rules (D-001) exist already. Nobody has seen the browser page, so the spec is written from the game spec and the manual, not from a look at the page.

## Findings

My report:

- **Document:** `design/entity-pictures.md`, with the entity list, style, light and memory rules, mark layering, numbered criteria 31 to 49, experience signals, edge cases and open questions.
- **Entity list (13 in scope):** E1 player with ember flame; E2 cave moth; E3 shade; E4 ash hound (standing and crouching poses); E5 the Gloom (a creature, one tile); E6 unlit brazier; E7 lit brazier; E8 salve; E9 oil flask; E10 wall; E11 floor; E12 `<`; E13 `>`. Inventory slots reuse the item pictures. The Floor 5 creature (the Gloom) is in. Terrain (wall, floor) is in as quiet, low-contrast pictures.
- **Excluded, with reasons:** unseen tiles (must stay blank); marks (stay marks, not pictures); the HUD, messages, summary screens and buttons (not floor-grid entities); any new content (out of scope per game-spec section 12); the text player (must not change).
- **Style:** flat strong silhouettes, small fixed palette, near-black cave, warm and bright colors reserved for the ember, red and dashed orange reserved for marks. Recorded as D-003.
- **Light:** visible tiles at full color and one brightness, remembered tiles dimmer with the same shapes, creatures never from memory, unseen blank. The player's flame size follows r (criterion 36).
- **Marks and pictures:** a fixed layering order. The threat border and badge go on top of the creature; the hound line and the Gloom area are tints under the creature; the reach border and letter are over the tile picture; stunned or staggered creatures get a pale-blue wash and no red. The marked set on the page must equal the text player's (criterion 45).
- **Existing checks touched:** 27, 29 (refined by 31 to 46), and 28 and 30 (re-check with pictures on). Checks 1 to 26 are untouched and covered by criterion 48.
- **Answer on Plan: yes, a short one.** The method is non-obvious and risky: pictures must work from `file://` (separate image files, drawing by code, inline vector or embedded data each behave differently); D-001 requires classic scripts and no drawing in rules code; a picture-mapping layer must read the same state the marks use, so pictures cannot change a mark; and the dimmed copies and flame sizes need a decision on code versus stored. The Technical Director should settle these before Build.
- **What I could not see:** the current page, tile size and mark colors. My means show none of that. I do not know whether the 10% inner margin and the 3 px border fit the actual tile size. The Build step should report tile size and current mark styling; below about 20 px per tile I should be consulted again.

## Decisions already made

- D-001: shared code is plain classic-script modules. The picture code must follow it, and the rules code stays free of drawing.
- D-002: threat marks plus reach marks. They stay readable over pictures (criteria 42 to 45).
- D-003 (new, accepted): flat dark-cave style, warm light reserved for the ember, red and orange reserved for marks, fixed layering with marks always over pictures, equal brightness inside the glow, same marked set on page and in text.

## Constraints

- No rule, balance or content changes. The text player and its output stay byte-identical (criterion 48), and `node --test` must still pass.
- No dependencies, no network, opens from `file://` without a server.
- Rules code stays shared and separate from drawing (D-001).
- Checks 1 to 30 stay in force.

## Open questions

1. Plan step (yes, as above): which method for making and storing the pictures, where the entity-and-state to picture mapping lives, and how remembered tiles and flame sizes are produced.
2. Tile size and the current mark styling are unknown; the Build or QA step should report them. Small tiles may force simpler pictures.
3. Should an Owner look at the page (proposed Goal 1) come before this Goal's build? I advise at least a screenshot of the working page before and after.
4. QA should run criteria 31 to 49 by looking at the page, with text-versus-page comparison for 45. Only someone who sees the page can check them; my means cannot.

## Expected output

The Studio routes this next to a Technical Director Plan step (advised), then Build, then QA. If the Studio decides no Plan is needed, route to Build. The Studio may fold criteria 31 to 49 into `design/acceptance-criteria.md`.

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/make-decision.md
- Project: project.md#constraints, project.md#current-state, design/entity-pictures.md, design/game-spec.md, repo/manual.md
- Decisions: decisions/D-001-classic-scripts-shared-rules.md, decisions/D-002-threat-and-reach-marks.md, decisions/D-003-picture-style-and-mark-layering.md
- Previous handoff: goals/G-002-entity-pictures/01-studio-to-art-director.md
