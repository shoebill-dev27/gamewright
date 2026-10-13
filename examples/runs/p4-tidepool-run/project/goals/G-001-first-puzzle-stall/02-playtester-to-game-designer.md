---
kind: handoff
goal: G-001
seq: 2
from: playtester
to: game-designer
stage: Diagnose
outcome: done
---
# 02: playtester → game-designer — diagnose the experience issues seen in the opening of build 0.2

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. Sender fills Task through Open questions; the Studio checks it against the
recipient's "Works from" and fills Load when routing. -->

## Task

Diagnose the experience issues in the observation report below (build 0.2, levels 1–3): symptoms
with evidence, causes in design terms, and 2–3 solution options with trade-offs.

## Context

Goal G-001 (first-puzzle-stall). Owner's words, verbatim: 「最初のパズルで子どもが手を止めてしまう。直したい」

Success condition: when children aged 7–10 play the first puzzle (level 1 in build 0.2), they begin
purposeful touch interaction with it on their own, without a long pause and without an adult having
to explain what to do. What counts as a stall is not set; Design turns it into a player-observable
acceptance criterion. Out of scope: levels 2 and later; changing a vision pillar or D-001 (no
failure, no timers); new art beyond the existing sprite sheet.

Flag, not a conclusion: `project.md` lists "No mechanic may depend on reading text" as a constraint,
and level 1 teaches with a text bubble.

The Studio asked the playtester for a first-hand account of how the opening plays for its target
players (`01-studio-to-playtester.md`, Owner's report withheld on purpose). The report below is
that account. It was produced from player-observable information only; no causes were assessed.
The `art-director` is reviewing the visuals of level 1 in parallel (handoff 03); their result is not
available to you, and the Studio will merge both at Route.

## Findings

### Observation report (playtest-session)

**Method.** Dry-run project, so no live play. I "ran the build" by reading `sim/build-0.2.md`, a
written stand-in for observed sessions with three children (ages 7, 8, 9) on a tablet. I played
nobody myself, so everything below is taken from that account. Not recorded in it, therefore not
reported: spoken quotes, the 8-year-old's reading ability, how long levels 2–3 took, and how any
player felt other than where stated.

**Session summary.** Level 1 starts with a calm scene: sand, one round tide pool, a crab, a
shell-shaped home, and a small text bubble near the top reading "Drag the tide pool!". Two of the
three children did not solve it for 20–35 seconds. The third solved it in 10 seconds. After level 1,
levels 2–3 went smoothly for all three.

**Concrete moments**

| Player | What they did | Time | How it ended |
|---|---|---|---|
| Age 7 (early reader) | Ignored the bubble. Tapped the crab several times; the crab did nothing. Tapped the home; nothing. | About 20 s, then looked at the parent | Parent read the bubble aloud. The child dragged the pool, finished quickly and smiled. |
| Age 8 | Tapped the crab twice, then tried to drag the crab; it did not move. | About 35 s before touching the pool, by chance | Finished level 1 after that. |
| Age 9 | Read the bubble and dragged the pool at once. | 10 s | Finished. |

- Activity rose at the start for the 7- and 8-year-old (tapping, dragging the crab) and then
  stopped producing results. The 7-year-old's activity ended in looking at the parent, and rose
  again once the parent read the bubble.
- Two of three children went to the crab first. The crab has a darker outline and bobs gently.
- The tide pool is the same pastel tone as the sand around it and looks like part of the sand
  pattern.
- Reading ability: the early reader (7) did not use the bubble on their own and needed it read
  aloud. The 9-year-old read it and was not delayed. The 8-year-old's reading ability is not stated.

**Possible malfunction, reported as observed, not diagnosed.** Taps on the crab and the home gave no
visible response, and dragging the crab did not move it. To the children this looked like touch that
did not register. I cannot tell whether this is intended.

**Issues with impact** (my rating of effect on the experience)

1. Level 1 opening: no response to the children's touches for 20–35 s, ended by outside help (7) or
   by chance (8). High for ages 7 and 8; none for age 9.
2. Taps and drags on the crab and home produce nothing. Medium to high for ages 7 and 8, who tried
   them repeatedly.

**Positives.** Once level 1 was solved, levels 2–3 went smoothly for all three. The 7-year-old
smiled on finishing level 1 after the parent's help. The 9-year-old finished at once.

**Open player questions (inferred from behavior, not stated by the children).** The children's
behavior suggests they were looking for what to touch, and two chose the crab.

## Decisions already made

None.

## Constraints

- The playtester decides nothing about the game. This report is observation only; the interpretation
  and any fix belong to you.
- Evidence is three simulated sessions, no timings beyond those above, and no spoken quotes.

## Open questions

- Which of the observed behaviors are the intended experience and which are not? In particular, is
  no response to taps on the crab and home intended? If it is a defect rather than an experience
  issue, route that part to `qa`.
- Does anything need a further playtest (for example a different play focus) before you decide?

## Expected output

A diagnosis (`diagnose-experience`): symptoms with evidence, causes, options with trade-offs and
vision fit, unknowns, and your recommendation if one is defensible. Mark any option that changes a
pillar, a Decision, scope or risk significantly. Returned to the Studio for the Route operation.
The planned next step is `game-designer` Design (route step 3 in `goal.md`).

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/diagnose-experience.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints,
  design/onboarding.md
- Decisions: decisions/D-001-no-fail-states.md
- Previous handoff: goals/G-001-first-puzzle-stall/01-studio-to-playtester.md
