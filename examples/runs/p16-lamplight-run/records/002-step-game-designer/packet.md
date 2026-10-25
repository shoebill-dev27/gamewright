# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-first-playable/01-studio-to-game-designer.md
next_seq: 2
runs: play (up to 3 rounds)
run_play: python3 play.py {script}
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-001-first-playable/02-game-designer-to-<recipient>.md
- design/<name>
- decisions/D-001-<name>.md
- @run/<play>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)
- @need: instead of your files, once: a file block `<<<FILE @need` with one path per line (up to 8 project or Studio files your Role may load), then `>>>END`, to add them to this packet

## Inputs

<<<FILE studio/execution.md#executor-instructions
## Executor instructions

You are executing exactly one Studio operation, in isolation.

- Everything you may use is in this packet: the operation header, the input files, and the paths
  you may write. You know nothing else about this project, its history, or other steps, and you
  must not assume anything beyond the packet.
- Follow the procedure for this operation in the Studio files included. For a Step, act as the
  receiving Role within its contract and listed Skills; do not perform other Roles' work.
- Write every file you create as one complete file block: `<<<FILE <path>` on its own line, the
  full file content, then `>>>END` on its own line. To change part of an existing file, you may
  instead write `<<<EDIT <path>` with `<<<<<<< SEARCH` / `=======` / `>>>>>>> REPLACE` pairs and
  `>>>END` (Output protocol); each SEARCH must match the file exactly once, so include enough
  lines. Use only the paths listed under "You may write"; paths are relative to the project
  directory.
- Only file blocks are kept. Anything else you write is discarded and never shown to any later
  step, so put everything the next operation needs into the files.
- If the packet is not enough to do the operation, write the artifact that hands the work back or
  reports the blocker instead of guessing.
- Nothing exists beyond this packet and what it offers: build runs (`@run`), one request for more
  files (`@need`), and the operations that follow. There is no other environment, staff, device,
  budget or log store, so never ask the Owner for them; say plainly what your means cannot show.
>>>END

<<<FILE goals/G-001-first-playable/01-studio-to-game-designer.md
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
>>>END

<<<FILE studio/roles/game-designer.md
---
kind: role
id: game-designer
writes: design/*, decisions/*
runs: play, bots
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

<<<FILE studio/skills/write-design-spec.md
---
name: write-design-spec
description: Specify player-facing behavior — rules, parameters, edge cases — with player-observable acceptance criteria, precise enough to build and verify without guessing.
---
# Skill: Write design spec

Typical roles: game-designer, art-director (for what the player sees).

## When to use

Intended behavior is not specified well enough for an engineer to build and QA to verify.

## Inputs

The approved direction (Decision), the problem it answers, current design documents, constraints.

## Method

1. State the experience intent in one or two sentences.
2. Specify behavior as rules and numbers, not adjectives. Give every parameter a value and unit.
3. Walk the edge cases: interruptions, simultaneous events, state changes mid-action, every
   supported platform condition. Each case either gets a rule or is listed as an open question.
4. Write acceptance criteria two ways: verifiable checks for QA, and experience signals for the
   playtest and Review (kept away from the Playtester's handoff).
5. Update the project's design documents; record significant choices as Decisions.

## Output

Design spec: intent, rules and parameters, edge cases, acceptance criteria (verification and
experience), open questions, changed design documents.

## Do not

Leave "feels good" as a criterion. Do not specify the code structure.
>>>END

<<<FILE project.md
---
kind: project
id: lamplight-keeper
name: Lamplight Keeper (new concept)
repository: repo/ (empty: no build exists yet)
owner_language: ja
player_visible: repo/manual.md
build: repo
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py {script}
run_trace: python3 play.py --trace {script}
---
# Project: Lamplight Keeper (new concept)

## Vision

A short, turn-based puzzle game. The player keeps a lighthouse on a rocky coast for one night at
a time. Ships come in from the dark sea, one tile per turn, heading for the harbor; the lamp's
beam turns them aside, and every turn the player chooses where it points. Bring ships to the
harbor; let none hit the rocks.

Pillars:

1. **One clear choice per turn.** Turn the beam left, turn it right, or hold. Nothing else.
2. **Reading ahead is the fun.** Where each ship will be in a few turns, and what the beam will do
   to it, can be worked out from what is on screen. Luck does not decide a night.
3. **A night is short.** One night takes a few minutes; it is lost or won in that time.

## Player profile

Puzzle players who like short, thinky sessions with readable rules (in the spirit of small
turn-based puzzle games). They want to plan, not to react fast.

## Current state

Concept only. Nothing has been designed or built: `repo/` holds only a README. There are no
design documents and no Decisions yet.

## Constraints

- The build is a Python 3 program using the standard library only, in `repo/`.
- It is played through input scripts, with no live input: `run_play` (`python3 play.py {script}`)
  plays a script and prints what the player sees, `run_trace` adds the internal state, and
  `run_tests` runs the build's tests. The script format is the build's to define, in
  `repo/manual.md`, which ships with the build and is all a player is told.
- Text output only (a grid of characters per turn); no graphics yet.
- Deterministic: the same script always gives the same night.

## Design index

None yet.
>>>END

<<<FILE studio/templates/handoff.md
---
kind: handoff
goal: G-NNN
seq: N
from: <role-id | studio>
to: <role-id | studio>
stage: <stage the recipient performs>
outcome: <sender's step result: routed | done | partial | pass | fail | question | goal-met | goal-not-met>
---
# NN: <from> → <to> — <one-line task>

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. The sender fills Task through Open questions and drafts Expected output; the Studio
checks it against the recipient's "Works from", settles Expected output and fills Load when routing.
outcome: routed = written by the Studio; done = work finished, no verdict; partial = work under way,
nothing missing, to be continued by the same Role; pass/fail = verification verdict; question =
handed back with an open question; goal-met/goal-not-met = Review verdict.
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

## Your answer

- Write the outgoing Handoff as goals/G-001-first-playable/02-game-designer-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
