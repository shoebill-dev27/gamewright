---
kind: handoff
goal: G-001
seq: 3
from: studio
to: art-director
stage: Diagnose
outcome: routed
---
# 03: studio → art-director — review whether level 1 shows the player what to touch

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. Sender fills Task through Open questions; the Studio checks it against the
recipient's "Works from" and fills Load when routing. -->

## Task

Review how level 1 of build 0.2 looks to the children in the observation report, in particular
whether the player can tell at a glance what to touch. Say what is visual and what is a rules
problem, and propose a visual direction for any visual issue.

## Context

Goal G-001 (first-puzzle-stall). Owner's words, verbatim: 「最初のパズルで子どもが手を止めてしまう。直したい」

Success condition: when children aged 7–10 play the first puzzle (level 1 in build 0.2), they begin
purposeful touch interaction with it on their own, without a long pause and without an adult having
to explain what to do. Out of scope: levels 2 and later; changing a vision pillar or D-001 (no
failure, no timers); new art beyond the existing sprite sheet.

A playtester observed three children (ages 7, 8, 9) on build 0.2. The full report is in the
previous handoff (`02-playtester-to-game-designer.md`, Findings); read it there. The `game-designer`
is diagnosing the same report in parallel (rules, feedback, pacing, text); you are asked because the
report contains visual facts. Their result is not available to you; the Studio merges both at Route.

## Findings

Visual facts from the observation report, for orientation only (the report is the source):

- The tide pool is the same pastel tone as the sand around it and looks like part of the sand
  pattern.
- The crab has a darker outline and bobs gently.
- Two of three children touched the crab first; taps on the crab and the home gave no visible
  response.
- The text bubble near the top ("Drag the tide pool!") was ignored by the early reader (age 7).

## Decisions already made

None.

## Constraints

- Do not change gameplay rules or parameters; hand rule problems to the `game-designer`.
- Do not change the art style pillars of the vision; escalate if a fix would need that.
- Stay within the existing sprite sheet (project constraint).

## Open questions

- Can the player tell at a glance which element is the interactable one? Is any visual issue
  separable from the rules issues?
- Is the visual problem really a rules problem? If so, say so and hand it back.

## Expected output

A visual verdict (`visual-review`): readability issues with evidence and where they occur,
consistency notes, and a proposed visual direction for fixes within the art direction. Returned to
the Studio for the Route operation, which waits for this and for the `game-designer` diagnosis
(handoff 02) before Design.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md
- Project: project.md#art-direction, project.md#constraints, sim/build-0.2.md
- Decisions: none
- Previous handoff: goals/G-001-first-puzzle-stall/02-playtester-to-game-designer.md
