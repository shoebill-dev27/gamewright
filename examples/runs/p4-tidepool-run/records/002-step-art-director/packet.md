# Studio operation packet

operation: Step
goal: G-001
role: art-director
incoming_handoff: goals/G-001-first-puzzle-stall/03-studio-to-art-director.md
next_seq: 5

## You may write

- goals/G-001-first-puzzle-stall/05-art-director-to-<recipient>.md
- design/<name>
- decisions/D-002-<name>.md

## Inputs

<<<FILE studio/execution.md#executor-instructions
## Executor instructions

You are executing exactly one Studio operation, in isolation.

- Everything you may use is in this packet: the operation header, the input files, and the paths
  you may write. You know nothing else about this project, its history, or other steps, and you
  must not assume anything beyond the packet.
- Follow the procedure for this operation in the Studio files included. For a Step, act as the
  receiving Role within its contract and listed Skills; do not perform other Roles' work.
- Write every file you create or change as one complete file block:
  `<<<FILE <path>` on its own line, the full file content, then `>>>END` on its own line.
  Use only the paths listed under "You may write"; paths are relative to the project directory.
- Only file blocks are kept. Anything else you write is discarded and never shown to any later
  step, so put everything the next operation needs into the files.
- If the packet is not enough to do the operation, write the artifact that hands the work back or
  reports the blocker instead of guessing.
>>>END

<<<FILE goals/G-001-first-puzzle-stall/03-studio-to-art-director.md
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
>>>END

<<<FILE studio/roles/art-director.md
---
kind: role
id: art-director
writes: design/*, decisions/*
---
# Role: Art Director

## Responsibility

Owns visual expression and visual consistency: style, readability, and the clarity of everything
the player sees.

## Decides

- Visual direction within the vision: colors, shapes, effects, UI presentation for a change.
- Visual acceptance: whether a change is readable and consistent with the art direction.

## Must not

- Change gameplay rules or parameters — that is `game-designer`.
- Change the art style pillars of the vision — escalate.
- Write production code.

## Works from

- Visual issues from playtests, design specs with visual implications, builds to review.
- The project's art direction and constraints (e.g., asset budget).

## Produces

- Visual spec for a change: what must be visible, how, and visual acceptance criteria.
- Visual review verdict with evidence.

## Hands back / escalates when

- The visual problem is really a rules problem → `game-designer`.
- A style pillar would change → `game-director`, for an Owner escalation.

## Typical skills

visual-review, write-design-spec, make-decision
>>>END

<<<FILE studio/skills/visual-review.md
---
name: visual-review
description: Review what the player sees for readability and consistency with the project's art direction, producing a verdict with evidence.
---
# Skill: Visual review

Typical roles: art-director.

## When to use

A problem may be visual, or a change affects what the player sees.

## Inputs

The build or captures, the art direction in the Project Context, the spec's visual criteria.

## Method

1. Check readability first: can the player tell what matters (threats, interactables, state) at a
   glance, in every environment and lighting condition the game has?
2. Check consistency with the art direction: palette, shapes, effects, UI style.
3. Check the spec's visual acceptance criteria.
4. Separate visual issues from rule issues; route rule issues to `game-designer`.

## Output

Visual verdict: pass/fail per criterion, readability issues with evidence and where they occur,
consistency notes, proposed visual direction for fixes.

## Do not

Change gameplay rules. Do not judge by personal taste over the project's art direction.
>>>END

<<<FILE project.md#art-direction
## Art direction

Pastel palette, rounded shapes. Interactive pieces have a darker outline and a gentle idle motion.
>>>END

<<<FILE project.md#constraints
## Constraints

- Phones and tablets, touch only.
- No ads, no in-app purchases.
- No mechanic may depend on reading text.
- Small art budget: reuse the existing sprite sheet where possible.
- Dry-run project: there is no real repository. `sim/repo-notes.md` stands in for the code. A Build
  step implements a change by stating it exactly in its Handoff (what changes, where, and how to
  exercise it); the change then counts as made, and the runtime's simulator updates `sim/` from it.
>>>END

<<<FILE sim/build-0.2.md
# Simulated build 0.2 — what playing it looks like

Dry-run stand-in for a real build, written as observed play sessions with three children (ages 7,
8 and 9) on a tablet. Player-observable only.

- Level 1 opens on a calm scene: sand, one round tide pool, a crab, a shell-shaped home. A small
  text bubble near the top reads "Drag the tide pool!".
- Age 7 (early reader): ignores the bubble, taps the crab several times. The crab does nothing.
  Taps the home. Nothing. Looks at the parent after ~20 seconds. Parent reads the bubble aloud;
  the child then drags the pool and finishes quickly, smiling.
- Age 8: taps the crab twice, then tries to drag the crab. It does not move. Tries the pool by
  chance after ~35 seconds and finishes.
- Age 9: reads the bubble, drags the pool at once, finishes in 10 seconds.
- The tide pool looks like part of the background sand pattern; it has the same pastel tone as the
  sand around it. The crab has a darker outline and bobs gently, so it looks like the thing to touch.
- Levels 2–3 go smoothly for all three once level 1 is solved.
>>>END

<<<FILE goals/G-001-first-puzzle-stall/02-playtester-to-game-designer.md
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
>>>END

<<<FILE studio/templates/handoff.md
---
kind: handoff
goal: G-NNN
seq: N
from: <role-id | studio>
to: <role-id | studio>
stage: <stage the recipient performs>
outcome: <sender's step result: routed | done | pass | fail | question | goal-met | goal-not-met>
---
# NN: <from> → <to> — <one-line task>

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. The sender fills Task through Open questions and drafts Expected output; the Studio
checks it against the recipient's "Works from", settles Expected output and fills Load when routing.
outcome: routed = written by the Studio; done = work finished, no verdict; pass/fail = verification
verdict; question = handed back with an open question; goal-met/goal-not-met = Review verdict.
Paths: studio/... is relative to the Studio root; everything else to the Project Context directory.
file#section: the section heading's slug, lowercase with hyphens (project.md#current-state).
Previous handoff = the Handoff the sender worked from (one step of history). -->

## Task

<What the recipient must do, in one or two sentences.>

## Context

<Why this work exists: the Goal and what happened so far, briefly.>

## Findings

<What the sender found or produced. For a Playtester recipient: nothing about implementation.>

## Decisions already made

<D-NNN links and one-line summaries, or "None".>

## Constraints

<Limits the recipient must respect.>

## Open questions

<Questions the recipient must answer or route, or "None".>

## Expected output

<What the recipient produces and where it goes next.>

## Sender assessment

<Optional. The sender's own evaluation and reasoning: self-test verdicts, root cause analysis,
confidence. Kept for the record and for Roles that may use it; removed before the Handoff reaches
a Role whose policy strips it (qa, playtester).>

## Load

- Role: studio/roles/<role-id>.md
- Skills: studio/skills/<skill-id>.md
- Project: <only the project files this step needs: project.md sections (project.md#section),
  design documents, the build>
- Decisions: <decisions/D-NNN-...md, or none>
- Previous handoff: <goals/G-NNN-.../NN-...md, or none>
>>>END

<<<FILE studio/templates/decision.md
---
kind: decision
id: D-NNN
status: accepted        # proposed | accepted | superseded
decided_by: <role-id | owner>
goal: <G-NNN, or none>
date: YYYY-MM-DD
supersedes: <D-NNN, or none>
---
# D-NNN: <the decision in a few words>

## Decision

<What was decided, and its limits.>

## Rationale

<Why.>

## Alternatives considered

<Other options and why they were not chosen.>

## Revisit when

<What change in evidence or circumstances should reopen this.>
>>>END
