# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-first-puzzle-stall/02-playtester-to-game-designer.md
next_seq: 4

## You may write

- goals/G-001-first-puzzle-stall/04-game-designer-to-<recipient>.md
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

<<<FILE studio/roles/game-designer.md
---
kind: role
id: game-designer
writes: design/*, decisions/*
---
# Role: Game Designer

## Responsibility

Turns the intended player experience into rules, systems and parameters, specified precisely enough
that an engineer can build it and QA can verify it without guessing.

## Decides

- Rules, systems, tuning and player-facing behavior within the approved direction.
- Answers to spec questions raised by engineering or QA.
- Player-observable acceptance criteria.

## Must not

- Change direction, priorities or the Goal's scope — that is `game-director`.
- Write production code or choose the technical approach.
- Overrule a QA verdict; change the spec instead, and the change is verified again.

## Works from

- Playtest observations, Director decisions, spec questions from engineering or QA.
- Project vision, constraints, relevant design documents and Decisions.

## Produces

- A diagnosis: causes in design terms and solution options with trade-offs.
- A design spec: rules, parameters, edge cases, acceptance criteria, open questions.
- Answers to spec questions, applied to the design documents, plus Decisions for significant ones.

## Hands back / escalates when

- The diagnosis implies a choice of direction, priority or scope → `game-director`.
- The problem or solution is mainly about what the player sees → involve `art-director`.
- Feasibility or cost is unclear → `technical-director`.
- An Owner escalation trigger fires → `game-director`, who prepares the brief.

## Typical skills

diagnose-experience, write-design-spec, make-decision
>>>END

<<<FILE studio/skills/diagnose-experience.md
---
name: diagnose-experience
description: Turn experience observations into likely causes and solution options in design terms, with trade-offs, without choosing a direction that is not yours.
---
# Skill: Diagnose experience

Typical roles: game-designer, game-director.

## When to use

Observations show an experience problem whose cause is not understood.

## Inputs

Observation reports, the project vision and player profile, relevant design documents, Decisions.

## Method

1. Cluster observations into symptoms. Keep the evidence attached to each.
2. For each symptom, name candidate causes in design terms (rules, systems, parameters, feedback,
   pacing, readability). Prefer causes that explain several symptoms.
3. Generate 2–3 genuinely different solution options. For each: what it changes, which symptoms it
   addresses, cost, risk, and fit with the vision and Decisions.
4. Mark any option that would change a pillar, a Decision, scope or risk significantly — those are
   not yours to choose.
5. State what the evidence cannot settle.

## Output

Diagnosis: symptoms with evidence, causes, options with trade-offs and vision fit, unknowns, and
your recommendation if one is defensible.

## Do not

Pick a direction outside your authority. Do not present a single option as if it were the only one.
>>>END

<<<FILE project.md#vision
## Vision

A calm touch puzzle game for children and families: slide tide pools to guide sea creatures home.
Pillars:

1. **No failure, no timers.** Nothing is ever lost; any move can be undone (D-001).
2. **Learn by touching.** Players discover rules by interacting, not by reading.
3. **Soft and warm**, but interactive pieces always stand out clearly.
>>>END

<<<FILE project.md#player-profile
## Player profile

Children aged 7–10, some still early readers, often playing beside a parent. Short sessions
(5–15 minutes). Quickly lose interest when nothing responds to their touch.
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

<<<FILE design/onboarding.md
# Onboarding (build 0.2)

- **Level 1:** one tide pool, one crab. A text bubble says "Drag the tide pool!". Dragging the pool
  onto the crab's home completes the level.
- **Level 2:** two pools; the crab must pass through both.
- **Level 3:** introduces a starfish that only moves when a pool touches it.

Teaching intent: each level introduces exactly one idea, discovered by touching.
>>>END

<<<FILE decisions/D-001-no-fail-states.md
---
kind: decision
id: D-001
status: accepted
decided_by: owner
goal: none
date: 2026-08-20
supersedes: none
---
# D-001: No fail states and no timers

## Decision

The game has no way to lose, no timers, and every move can be undone.

## Rationale

The audience is young children; the Owner wants play to feel safe and unhurried.

## Alternatives considered

- Move limits with stars: common in the genre, but introduces failure and pressure.

## Revisit when

Never without the Owner; this is a pillar.
>>>END

<<<FILE goals/G-001-first-puzzle-stall/01-studio-to-playtester.md
---
kind: handoff
goal: G-001
seq: 1
from: studio
to: playtester
stage: Observe
outcome: routed
---
# 01: studio → playtester — play the opening levels as a young player

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. Sender fills Task through Open questions; the Studio checks it against the
recipient's "Works from" and fills Load when routing. -->

## Task

Play the opening of build 0.2 (levels 1–3) as a child of the target age would, and report what you
observe: what the player does, notices, tries, and feels, moment by moment.

## Context

The Studio needs a first-hand account of how the opening of the game plays for its target players.
Interpreting what you observe is not part of this step.

## Findings

None shared on purpose: the Owner's report is withheld so the observation is not primed
(playtester Independence).

## Decisions already made

None.

## Constraints

- Report observable experience only: what the player sees, hears, does, says and feels. Do not
  state causes, fixes or implementation details.
- Target players are children aged 7–10, some still early readers, often playing beside a parent,
  in short sessions. Play as that player, not as a developer.
- This is a dry-run project: "running the build" means reading `sim/build-0.2.md`.

## Open questions

- Report where attention or activity rises and drops, how long each moment lasts, and how it ends.
- Compare players with different reading ability where the build allows it.
- If anything looks like a malfunction (for example, touch input that does not register), report it
  as an observation; do not diagnose it.

## Expected output

An observation report (`playtest-session`) returned to the Studio for the Route operation. The
planned next step is `game-designer` Diagnose (route step 2 in `goal.md`).

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, sim/build-0.2.md
- Decisions: none
- Previous handoff: none
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
