---
kind: handoff
goal: G-002
seq: 1
from: studio
to: art-director
stage: Design
outcome: routed
---
# 01: studio → art-director — specify pictures for each kind of thing in the game

## Task

Write a visual design spec that gives each kind of thing the player sees on the floor grid its own picture, with player-observable acceptance criteria that QA and you can later check. Decide which entities are in scope (see Findings).

## Context

Goal G-002. The Owner said (verbatim): 「それぞれに絵をつけてほしい」 ("I want pictures attached to each of them"). The referent of "それぞれ" is not stated. The Studio reads it as every kind of thing the player meets on the floor grid, so that the player can tell them apart by picture. The existing build (G-001) has five floors, the ember, three creature types, braziers, items, the Gloom, and seeded runs. Threats and reach are marked on the page (D-002). The page draws the floor as a grid and opens from the file system. Nobody has yet seen the browser page, so there is no first-hand record of how it looks today.

## Findings

Studio only, no work done yet. Points for your spec:

- Core set: the player and ember, the three creature types, braziers, and items. Whether terrain tiles (wall, floor, Gloom) and the Floor 5 creature get pictures is your call. List the full set of entities in the spec, taken from `design/game-spec.md`, and say what is excluded and why.
- Ember light (pillar 2) sets how far the player sees. Say how pictures look at different light levels or in unseen and remembered tiles, if the game has those.
- Pillar 1: every threat that can hurt the player next turn must stay readable. Pictures must not hide or weaken the threat marks and reach marks of D-002. State how each coexists with the picture.
- The art style must fit the vision: a dark cave, with the ember as the light.
- Technical limits the spec must respect: no dependencies, no network, the page opens straight from the file system (no server), and the rules code stays shared and separate from drawing. The text player must not change. Do not choose the technical method beyond what the visuals need. If you think a method is non-obvious or risky (for example, how the pictures are made or stored), say so under Open questions, so the Studio can add a Plan step.
- Acceptance criteria must be player-observable (what is seen on the page), so the checks can be run by someone who looks at it. Number them so they can be cited. The existing 30 checks (27-30 cover the page) stay in force. Say which of them the pictures touch.

## Decisions already made

- D-001: shared code is plain classic-script modules (UMD style), not ES modules. This applies to any code the pictures need.
- D-002: threat marks plus reach marks on the four neighbour tiles. These must stay readable.

## Constraints

- Stay within the vision and pillars; do not change rules, balance or content.
- If you find that the Goal needs a direction choice (for example, an art style that conflicts with a pillar, or a scope much larger than "pictures"), hand back with that question per your Role contract rather than deciding it.
- If you make a significant visual decision that constrains later work, record it as a Decision.

## Open questions

- Which entities get pictures (settle in the spec).
- Does the spec's approach need a Technical Director Plan? Say yes or no, and why.

## Expected output

1. A design document `design/entity-pictures.md` with the entity list, the picture style, readability rules (marks, light), and numbered, player-observable acceptance criteria.
2. An outgoing Handoff (templates/handoff.md) addressed to `studio` (not to a Role), with `outcome` done, or `question` if blocked. Findings name the document, the entity list and your answer on Plan. The Studio routes it next, either to Plan or to Build. Address the result to `studio` because the Studio decides whether a Plan step is needed.

## Sender assessment

The Studio expects a modest spec, since the page, the marks and the build already exist. The main risks are readability of threat/reach marks over pictures, and the fact that no one has seen the page yet.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#player-profile, project.md#current-state, project.md#constraints, design/game-spec.md, design/acceptance-criteria.md, repo/manual.md
- Decisions: decisions/D-001-classic-scripts-shared-rules.md, decisions/D-002-threat-and-reach-marks.md
- Previous handoff: none
