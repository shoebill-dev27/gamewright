---
kind: handoff
goal: G-001
seq: 1
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 01: studio → game-designer — specify the first playable version of Lamplight Keeper

## Task

Write the design specification for the first playable version, with player-observable acceptance criteria, so that an engineer can build it and QA can verify it without further questions.

## Context

Goal G-001: the Owner asked (ja) "このコンセプトで、遊べる最初の版を作ってほしい" ("build a first playable version of this concept"). The project is a concept only: no design documents, no Decisions and no build exist. `repo/` holds only a README. This is the first step; you are the one who turns the vision into rules.

## Findings

Nothing yet. The vision, pillars, player profile and constraints are in `project.md`. They are the only source of truth so far.

## Decisions already made

None.

## Constraints

- Stay inside the vision and its pillars: one clear choice per turn (beam left, right or hold), reading ahead is the fun with no luck, a night is short (a few minutes).
- Text output only (a character grid per turn); deterministic; standard-library Python 3; played through input scripts, with no live input.
- Specify player-facing behavior, not code. The script format is the build's to define and goes in `repo/manual.md`, but your spec must say what the player must be able to do and see, for example what is displayed each turn and how a night ends.
- Specify at least: the grid and its elements (lighthouse, beam, ships, harbor, rocks, sea), turn order and what happens within a turn, how the beam turns ships aside (and what it does when it does not reach them), how ships move, win and loss conditions, how a player can work out future positions from the screen, and a small set of nights (suggest a few, rising in difficulty) that shows the core loop. Give concrete night layouts with a solution for each so QA can check them.
- Acceptance criteria must be player-observable and verifiable by playing scripts. Numeric values are yours to set here.
- Keep the scope to a first playable. Do not add mechanics beyond the vision. If a rule choice would change a pillar or needs a scope decision you do not hold, say so under Open questions rather than deciding it.
- Save the spec as `design/first-playable.md` in the Project Context, and list it in the project's design index in your Findings (the Owner owns `project.md`; do not edit it).

## Open questions

- Which rules make "the beam turns ships aside" fully readable and luck-free? Decide them in the spec.
- Is a rule choice needed that changes a pillar or the scope? If so, hand back with `outcome: question` for a `game-director` decision.

## Expected output

The design document `design/first-playable.md` and a Handoff (templates/handoff.md) summarizing it in Findings, with the spec's acceptance criteria listed, addressed to `studio` for routing (Plan or Build next).

## Sender assessment

Intake judges the Plan stage tentative: the build looks small and standard-library only, so a technical plan is likely unnecessary unless the spec proves cross-system or risky.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md (vision, player profile, current state, constraints)
- Decisions: none
- Previous handoff: none
