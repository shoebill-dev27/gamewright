# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-first-playable-run/01-studio-to-game-designer.md
next_seq: 2
runs: play (up to 3 rounds)
run_play: node play.js {script}
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-001-first-playable-run/02-game-designer-to-<recipient>.md
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

<<<FILE goals/G-001-first-playable-run/01-studio-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 1
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 01: studio → game-designer — specify a complete five-floor run of Ember Hollow

## Task

Write the design spec for the first complete playable version of Ember Hollow: everything the player-facing game needs so that one run, from floor 1 to a win or a loss, can be built and verified. Include player-observable acceptance criteria with numbers.

## Context

G-001. The Owner asked (ja): "このコンセプトで、最初から最後まで通して遊べる版を作ってほしい。ブラウザで遊べるようにしてほしい" ("Make a version of this concept that can be played from start to finish, playable in the browser"). The project is concept only: `repo/` holds a README, with no design documents and no Decisions. You are the first step. After you come Plan (`technical-director`), Build, Verify, Play and Review. The Plan and Build steps work from your spec and cannot ask you what you meant, so it must stand alone.

## Findings

Nothing yet; this is the first step. The vision, pillars, player profile and constraints are in `project.md` (see Load). Points to cover:

- **Ember and light:** how the glow sets how far the player sees, how it dims per turn, how braziers rekindle it, what happens when it goes out, and how the player can read the ember's state.
- **Turn actions:** move, wait, fight, use an item; what each costs and does.
- **Creatures:** the roster for five floors and how each reacts to light and acts. Each behavior must be learnable. Every threat that can hurt the player next turn is visible and readable beforehand (pillar 1).
- **Floor 5 creature:** the one that keeps the hollow dark. Its behavior, and the win condition.
- **Items:** only what the run needs, with their effects.
- **Floors:** what a floor contains (layout rules, brazier placement, creature and item placement) and that floors derive from a seed (same seed gives the same run, different seeds differ).
- **Run shape:** the 15–30 minute target, translated into floor sizes and counts that can be checked; the end of run states and what the player sees at each.
- **Player-facing information:** what the screen must show (grid, ember state, health, threats, messages), described by what the player can tell, not by layout code. Keyboard and mouse controls in the browser.
- **Acceptance criteria:** player-observable and numeric where numbers matter, checkable through text output of `node play.js {script}` and by looking at the browser page.

## Decisions already made

None. (There are no Decisions in the project.)

## Constraints

- Stay inside the vision and pillars. If completing the spec would need a change to the concept, a pillar, or the scope of the Goal, hand back to the Studio for a `game-director` decision instead of choosing it yourself.
- Specify player-facing behavior only. Do not decide technical approach, architecture or file structure. The script format is the build's to define in `repo/manual.md`; do not specify it.
- Keep content to what one complete five-floor run needs. No saving, meta-progression, sound or mobile layouts.
- The game is deterministic: the same seed and commands always give the same run. Rules must allow this (no rule that depends on real time or other outside input).
- The spec must be buildable in the project's technology (JavaScript, Node.js 20 and browser, no dependencies, no network); keep rules simple enough to implement and test as such.
- Write the spec as project design documents under `design/` (for example `design/game-spec.md`), not only in the Handoff. Use several files if that helps, and name them in Findings.

## Open questions

None for you to route beyond the escalation condition in Constraints. List any ambiguity you resolved yourself, with the choice made, in Findings of your outgoing Handoff.

## Expected output

The design spec in `design/`, with player-observable acceptance criteria. The outgoing Handoff goes to `technical-director` (stage Plan), with the spec file names under Findings. If the spec needs a direction, priority or scope choice that is not yours, set `to` to `studio` with `outcome: question` and say which choice.

## Sender assessment

Studio's routing view: the vision is already specific, so no Diagnose or Decide stage is planned. The main risk is size: five floors with a creature roster and a boss in one spec. Prefer a small, complete content set with clear behaviors over a large one. The art-director's visual review comes after Build; what the player must see should be in your acceptance criteria.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#player-profile, project.md#current-state, project.md#constraints, repo/README.md
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

<<<FILE project.md#vision
## Vision

A short turn-based roguelike. The player descends five floors of a cave carrying a single ember.
The ember is both light and time: its glow is how far the player can see, it dims a little every
turn, and only the braziers scattered through the floors rekindle it. The creatures of the hollow
live in the dark and react to the light. Floor 5 holds the creature that keeps the hollow dark;
beating it wins the run. Dying, or letting the ember go out, ends it.

Pillars:

1. **Every turn is a decision.** Move, wait, fight or use an item; every threat that can hurt the
   player next turn is visible and readable before it does.
2. **Light is the resource.** Seeing farther and having more time are the same thing; spending the
   ember is the core trade-off of a run.
3. **A run is short and different each time.** A whole run takes 15 to 30 minutes. Floors are made
   from a seed, so every seed is a different run, and the same seed is always the same run.
>>>END

<<<FILE project.md#player-profile
## Player profile

Players who enjoy short roguelikes: they like learning how each creature behaves and planning a
few turns ahead, and accept losing a run to learn from it. They play with a keyboard, or by
clicking, in a browser.
>>>END

<<<FILE project.md#current-state
## Current state

Concept only. Nothing has been designed or built: `repo/` holds only a README. There are no
design documents and no Decisions yet.
>>>END

<<<FILE project.md#constraints
## Constraints

- The build is JavaScript for Node.js 20 and the browser, with no dependencies and no network
  use, in `repo/`. The game's rules live in code that both ways of playing share.
- **For people: a browser page.** `repo/index.html` opens straight from the file system (no
  server) and is played with the keyboard or the mouse. It draws the floor as a grid.
- **For the team: input scripts.** `run_play` (`node play.js {script}`) plays a script and prints
  what the player sees, as text, turn by turn; `run_trace` adds the internal state; `run_tests`
  (`node --test`) runs the build's tests. The script format (including how a run's seed is
  chosen) is the build's to define, in `repo/manual.md`, which ships with the build and is all a
  player is told.
- Deterministic: the same seed and the same commands always give the same run.
>>>END

<<<FILE repo/README.md
# Ember Hollow build

Empty: the first playable build goes here (see `../project.md`, Constraints).
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

- Write the outgoing Handoff as goals/G-001-first-playable-run/02-game-designer-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
