# Studio operation packet

operation: Route
goal: G-001
step_artifact: goals/G-001-combat-monotony/08-technical-director-to-studio.md
next_seq: 9

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/08-technical-director-to-studio.md (in place: keep kind, goal, seq, from, to)
- goals/G-001-combat-monotony/09-studio-to-<role>.md

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

<<<FILE studio/README.md
# Studio

The tool-neutral definition of the Studio. Nothing in this directory names a specific AI tool,
model, or game project. Any executor — an AI agent session of any kind, or a human — reads these
files to do the work. Canonical intent: `docs/spec/initial-spec.md`.

## Concepts

| Concept | What it is | Lives in |
|---|---|---|
| Owner | The human. Gives Goals, decides Owner-level questions. | — |
| Studio | The orchestration function. Turns a Goal into routed Steps. Owns process (who works next, on what), never game content. | `orchestration.md` |
| Goal | An Owner request, tracked as a Goal record with a route plan. | `<project>/goals/<goal>/goal.md` |
| Step | One unit of work by one Role, started from one incoming Handoff. | — |
| Role | A responsibility with authority and boundaries. Not a model, not an agent. | `roles/` |
| Skill | A method for doing a kind of work. Usable by any Role whose responsibility covers that work. | `skills/` |
| Workflow | The catalogue of development stages plus routing rules. A menu, not a pipeline. | `workflows/development-loop.md` |
| Isolated execution | How a runtime runs each operation in a fresh executor that sees only its packet, and enforces Role policies. | `execution.md` |
| Project Context | Everything specific to one game: vision, state, constraints, design, decisions, goals. | outside `studio/` |
| Handoff | Persisted work packet between Steps. Self-contained: a new executor can start from it alone. | `<project>/goals/<goal>/NN-*.md` |
| Decision | Persisted significant judgment: what, why, alternatives, when to revisit. | `<project>/decisions/` |
| Escalation | Persisted request for an Owner decision, with options and a recommendation. | `<project>/goals/<goal>/NN-*-to-owner.md` |
| Executor | Whatever runs a Step. Chosen at run time. Never named in Role, Skill or Workflow definitions. | — |

Separation rules:

- **Role ≠ Executor.** Any executor can run any Role. Changing executors changes nothing here.
- **Role ≠ Skill.** A Role says who is responsible; a Skill says how the work is done. Role
  contracts list *typical* skills only; a Role may use any Skill its responsibility covers.
- **Role ≠ Project.** Roles and Skills contain no game-specific facts. Project facts arrive through
  the Handoff's Load list.
- **Studio ≠ Game Director.** The Studio routes; the Game Director judges the game. A Goal that needs
  no direction decision never passes through the Game Director.

## Roles

| id | Responsible for |
|---|---|
| `game-director` | Overall direction, priorities, important decisions; guarding the vision; judging whether experience goals are met. |
| `game-designer` | Turning intended player experience into rules, systems and parameters, specified well enough to build and verify. |
| `technical-director` | Turning approved specs into feasible technical plans; technical risk, architecture, sequencing, parallelization. |
| `gameplay-engineer` | Implementing approved designs and plans, and fixing defects. |
| `art-director` | Visual expression and visual consistency: style, readability, clarity of what the player sees. |
| `qa` | Reproducing defects and independently verifying built changes against acceptance criteria. |
| `playtester` | Evaluating the game as a player, from observable experience only. |

Participants that are not Roles: `studio` (routing) and `owner` (the human).

## Skills

| id | Method for | Typical roles |
|---|---|---|
| `reproduce-defect` | Reproducing a reported problem and writing a precise defect report with acceptance criteria. | qa |
| `verify-change` | Verifying a change against acceptance criteria and checking for regressions. | qa |
| `playtest-session` | Playing a build as a player and reporting observable experience. | playtester |
| `diagnose-experience` | Turning experience observations into causes and solution options in design terms. | game-designer, game-director |
| `write-design-spec` | Specifying player-facing behavior, parameters and player-observable acceptance criteria. | game-designer, art-director |
| `technical-plan` | Turning an approved spec into an implementation plan with risks, tests and sequencing. | technical-director |
| `implement-change` | Changing the game per spec and plan, with tests; stopping on ambiguity. | gameplay-engineer |
| `make-decision` | Choosing between options within one's authority and recording the Decision. | game-director, game-designer, technical-director, art-director |
| `prepare-owner-escalation` | Framing an Owner-level question as options, reasoning and a recommendation. | game-director, technical-director |
| `visual-review` | Reviewing what the player sees for readability and consistency with the art direction. | art-director |
| `review-outcome` | Judging whether a Goal's intent was met and naming the next issues. | game-director |

## Context loading

Never load every Role, Skill or document. A Step loads exactly what its incoming Handoff lists
under **Load** (spec §17):

```text
Current Role + Required Skills + Current Task (the Handoff)
+ Relevant Project Context + Relevant Decisions + Previous Handoff
```

The Studio's own routing operations load the files named in `orchestration.md`. This README is the
catalogue the Studio uses to choose Roles and Skills without opening every file.

## Project Context layout

A Project Context is a directory. It may live inside the game repository (keeps decisions versioned
with the game) or anywhere else; the Studio is given its path.

```text
<project>/
├── project.md            # vision, player profile, current state, constraints, design index (templates/project.md)
├── design/               # relevant design documents
├── decisions/            # D-NNN-<slug>.md (templates/decision.md)
└── goals/
    └── G-NNN-<slug>/
        ├── goal.md       # Goal record and route plan (templates/goal.md)
        └── NN-<from>-to-<to>.md   # Handoffs and Escalations, in order
```

Path convention inside Project artifacts: paths starting with `studio/` are relative to the Studio
root; all other paths are relative to the Project Context directory.
>>>END

<<<FILE studio/orchestration.md
# Studio Orchestration

The Studio receives an Owner Goal and moves it forward until the Goal is met or the next decision
belongs to the Owner (spec §13).

The Studio decides **process**: which Role works next, with which Skills, on which context, in what
order. It never decides game content, specs, technical approach or verification verdicts — those
belong to Roles (see Decision authority). Choosing only the stages a Goal needs is the Studio's
core job; adding stages is not.

## Operations

Every executor performs these operations the same way. In Phase 1 a human starts each operation;
the Studio stops after Intake and after every Route, and states the next action (spec §18).
`execution.md` defines how a runtime runs each operation in a fresh, isolated executor that sees
only its packet; the procedures below are the same either way.

### Intake — a new Goal

Load: `studio/README.md`, this file, `studio/workflows/development-loop.md`, `<project>/project.md`,
and the titles of `<project>/decisions/`. Open a design document or Decision only if the Goal
touches it.

1. **Understand the Goal.** Quote the Owner's words verbatim. Restate the Goal as an observable
   success condition, qualitatively; numeric thresholds belong to Design (acceptance criteria) and
   the final verdict to Review. Note what is out of scope.
2. **Check the Project Context.** Vision, current state, constraints, and Decisions the Goal touches.
3. **Check for an immediate escalation.** If acting on the Goal requires reinterpreting it, or it
   conflicts with the vision or a Decision, escalate before routing (see Escalation).
4. **List the unknowns.** Ask each stage's entry question in `development-loop.md`. Every question
   that cannot be answered from the Project Context is an unknown.
5. **Select stages, Roles and Skills.** One stage per unknown, plus Verify after any Build. The Role
   is whoever holds authority over that question; the Skills come from the stage table. Mark each
   stage `planned` (needed whatever earlier steps find), `tentative` (needed only if an earlier
   step's result calls for it — say which result), or `skipped` (the Project Context already
   answers its question — say how).
6. **Order and parallelize.** Default is sequential. Parallel only for independent steps (see
   Parallel work).
7. **Write** `goals/G-NNN-<slug>/goal.md` (templates/goal.md; next free number in the project,
   short kebab-case slug, ISO dates) and the first Handoff `01-studio-to-<role>.md`; mark that
   first step `open` in the route table. Apply Route
   steps 4–5 to that Handoff: read the recipient's Role contract ("Works from", "Independence")
   before writing it.
8. **Return to the Owner** and stop: the route, why each stage is there, which stages were skipped
   or left tentative and why, and the next action.

### Step — run the next step

Load exactly the incoming Handoff, the files in its **Load** list, and the template of the artifact
you write (`studio/templates/`). Nothing else. `file#section` means that section only; scanning the
file's headings to find it is fine.

1. Act as the receiving Role: respect its contract (Decides / Must not), follow the listed Skills.
2. Produce the Expected output.
3. Write the outgoing Handoff (templates/handoff.md), filling Task through Open questions from your
   own work. Your output (report, diagnosis, plan, verdict) goes in Findings, or in the project
   files Findings names (e.g., a design document). Set `outcome`, and set `to` to the next Role
   per the route — or per your Role contract's "Hands back / escalates when" if your result calls
   for it. If the incoming Handoff's Expected output names another recipient (e.g., `studio`),
   use that.
4. Do not route around your contract: if the work needs a decision you do not hold, hand back.

### Route — after every step

Load: `goal.md`, the latest Handoff, this file, `studio/workflows/development-loop.md`; for steps
4–5 also the recipient's Role contract and the files you put in its Load list.

1. Mark the step done in the route table, linking its Handoff.
2. **Compare the outcome with the plan.** If it fits, the next planned step follows. If not, apply
   the return rules in `development-loop.md`, revise the remaining route, and log why under
   *Route changes*. Confirm (`planned`) or drop (`skipped`) any `tentative` stage whose condition
   this result settles. The route is a plan, not a contract.
3. **Check escalation triggers** (below). If one fires, write an Escalation instead of a Handoff.
4. **Check the recipient's inputs.** Compare the outgoing Handoff with the recipient Role's
   "Works from" section; remove what the recipient must not receive and add what is missing,
   editing the Handoff in place (it keeps `from`: the sender). Leave `## Sender assessment`
   untouched: it stays on record, and Roles whose policy strips it never receive it.
   When the recipient has an Independence section that forbids what the sender knows (e.g., a
   Playtester after Build or Verify), the Studio composes a fresh Handoff for the recipient from
   permitted information only. To make that possible, the Handoff that routes work to the sender
   says in its Expected output: address the result to `studio`.
5. **Select context.** Fill the Handoff's Load list: the recipient's Role contract, its Skills, the
   Project Context sections and Decisions this step needs, and the previous Handoff.
6. **Mark the next step `open`** in the route table, with the Handoff that starts it, and update
   Next action in `goal.md`. If the Goal is met, Close.

### Resume — after an Owner decision

1. Record the Owner's choice as a Decision with `decided_by: owner` (templates/decision.md),
   including the Owner's own words and any conditions they added.
2. Set the Escalation to `status: resolved` with `decision: D-NNN`; set the Goal back to `active`.
3. Re-plan the remaining route from the Escalation's "If chosen" consequences for the chosen option.
   If the Owner chose something no option described, re-run Intake steps 4–6 on the remaining work.
4. Write the next Handoff with `from: studio`, citing the Decision under *Decisions already made*.

### Close

Fill the Goal record's **Outcome** for the Owner: results, Decisions made, next issues (proposed
new Goals), and items needing the Owner. Set `status: done` (or `abandoned`, with the reason).

Owner-facing text — the Outcome, Escalation briefs, and the Studio's replies to the Owner — uses
the project's `owner_language`. Other artifacts use whatever language the project's executors
share.

## Escalation

The Studio does not finalize every judgment on its own (spec §5, §19).

### Escalate to the Owner when

- the game's core concept, a vision pillar, or an Owner-made Decision would change;
- several major directions are viable and the evidence does not settle which;
- scope, cost or risk would change significantly beyond what the Goal implies;
- the Owner's taste or values are the main criterion for the choice;
- the change is irreversible (destructive data or asset changes, releases, public commitments);
- the Goal itself has to be reinterpreted to make progress.

### Do not escalate

Choices inside a Role's authority that stay within the vision, the constraints and existing
Decisions. The responsible Role decides and, if significant, records a Decision. Escalating these
pushes work back onto the Owner that the Studio exists to absorb.

### How to escalate

1. The Role with authority nearest the question prepares the brief with `prepare-owner-escalation`
   (usually `game-director`; `technical-director` for technical risk or irreversibility).
2. The brief is an Escalation file (templates/escalation.md): options, consequences, a Studio
   recommendation, reasoning, and what happens next under each option.
3. The Studio sets the Goal to `blocked-on-owner`, pauses every step that depends on the answer
   (independent steps may continue), and returns the brief to the Owner.

## Decision authority

Final decisions belong to the responsible Role — never to a vote across executors or opinions
(spec §14).

| Question | Decides |
|---|---|
| Direction, priorities, which approach to pursue within the vision, scope within a Goal, whether an experience Goal is met | `game-director` |
| Rules, systems, tuning, player-facing behavior within the approved direction | `game-designer` |
| Technical approach, architecture, sequencing, parallelization | `technical-director` |
| Implementation details within the spec and plan; root cause of a defect | `gameplay-engineer` |
| Visual direction and consistency within the vision | `art-director` |
| Pass/fail against acceptance criteria; reproducibility and severity | `qa` |
| Accuracy of experience observations (no decision authority over the game) | `playtester` |
| Routing and process | `studio` |
| Anything matching an escalation trigger | `owner` |

Record a Decision when it constrains work beyond the current step, when a real alternative was
rejected, or when the Owner made it. Smaller choices are noted in the Handoff.

## Parallel work, workspaces and sub-executors

- **Parallel steps** only when neither consumes the other's output (e.g., QA verification and an
  Art Director visual review of the same build). Each gets its own Handoff (consecutive `seq`) and
  shares one route number with a letter suffix (2a, 2b). The Route operation waits for all of them
  before moving on.
- **Isolated code workspaces** (e.g., separate working trees) only when independent code changes
  run in parallel, as decided in a Technical Director plan. Never to separate Roles (spec §15).
- **Sub-executors** may do specialist research or independent review for a Role. They report to
  that Role; the Role decides.
- **Independence.** Run `qa` and `playtester` steps in a fresh executor context without the
  implementation history, whenever the executor makes that possible.

## Loop limits

No unbounded loops (Phase 1 has no autonomous loop at all, but routes can cycle):

- The same acceptance criterion fails verification twice → route to `technical-director` to
  re-plan, not to a third fix attempt.
- A Goal re-enters Diagnose twice without measurable progress → `game-director` reviews; this may
  become an escalation about scope or the Goal itself.
>>>END

<<<FILE studio/workflows/development-loop.md
# Development Loop

The standard loop (spec §12):

```text
Observe → Diagnose → Decide → Design → Plan → Build → Verify → Play → Review → Next
```

It is a **menu of stages, not a pipeline.** A stage enters a route only when its entry question is
open for this Goal. Most Goals use a few stages; only a Goal where everything is unknown uses all.

## Stages

| Stage | Include when… | Responsible role | Skills | Output |
|---|---|---|---|---|
| Observe | the problem has not been reproduced or observed first-hand | `qa` for defects; `playtester` for experience | `reproduce-defect` / `playtest-session` | defect report / observation report |
| Diagnose | the cause is not understood | `game-designer` for experience and rules; `technical-director` for technical causes; add `art-director` when the cause may be visual | `diagnose-experience` / `technical-plan` / `visual-review` | diagnosis with options |
| Decide | there is a real choice of direction, priority or scope | `game-director` (the Owner if an escalation trigger fires) | `make-decision`, `prepare-owner-escalation` | Decision or Escalation |
| Design | intended player-facing behavior is not specified well enough to build and verify | `game-designer`; `art-director` for what the player sees | `write-design-spec` | spec with player-observable acceptance criteria |
| Plan | the technical approach is non-obvious, risky, cross-system, or could be parallelized | `technical-director` | `technical-plan` | plan |
| Build | the game must change | `gameplay-engineer` | `implement-change` | change and build notes |
| Verify | anything was built — always after Build | `qa`; add `art-director` in parallel when the change affects visuals | `verify-change` / `visual-review` | pass/fail report |
| Play | the Goal is about how the game plays or feels | `playtester` | `playtest-session` | observation report |
| Review | the Goal is an experience Goal or involved a direction Decision | `game-director` | `review-outcome` | goal met or not, next issues |
| Next | always, at the end | `studio` | — | Outcome for the Owner (orchestration.md, Close) |

**Defect or experience problem?** A defect is behavior that contradicts the design documents or
Decisions, or is plainly broken (crash, stuck state, lost progress): Observe with `qa`. An
experience problem is behavior that works as specified but plays or feels wrong: Observe with
`playtester`. If unsure, start with `playtester`; defects it finds go to `qa` (return rules).

Answering an entry question from the Project Context removes the stage. Examples: a defect whose
intended behavior is already in the design documents needs no Design; a fix whose approach is
local and obvious needs no Plan; a defect needs no Play or Review.

## Return rules

When a step's outcome does not fit the plan, route by the first matching rule.

| From | Outcome | Route to |
|---|---|---|
| any | an escalation trigger fires | Owner escalation (orchestration.md) |
| Verify | fail: built behavior differs from the acceptance criteria | Build (`gameplay-engineer`) with the failure report |
| Verify | fail on the same criterion a second time | Plan (`technical-director`) |
| Verify | the expected behavior is undefined | Design (`game-designer`) |
| Build | spec ambiguous, contradictory or missing a case | Design (`game-designer`), then back to Build. The engineer does not decide. |
| Build | plan not workable | Plan (`technical-director`) |
| Build, Plan | conflicts with the approved direction or the Goal's scope | Decide (`game-director`) |
| Plan | spec infeasible within constraints | Design (`game-designer`); Decide (`game-director`) if scope must change |
| Design | needs a choice of direction, priority or scope | Decide (`game-director`) |
| Play | design or experience issue | Diagnose (`game-designer`); `game-director` when it implies a direction or priority change |
| Play | defect | Observe (`qa`) |
| Review | goal not met | Diagnose again, with the Review's findings |
| Review | goal met | Next; new issues become proposed Goals, not scope growth |

## Route patterns

Precedents to start from, not templates to force. Always derive the route from the unknowns.

1. **Reproducible defect, intended behavior specified:**
   Observe (`qa`) → Build (`gameplay-engineer`) → Verify (`qa`).
2. **Experience problem, cause unknown:**
   Observe (`playtester`) → Diagnose (`game-designer`) → Decide (`game-director`) → Design
   (`game-designer`) → Plan (`technical-director`) → Build → Verify (`qa`) → Play (`playtester`) →
   Review (`game-director`).
3. **Specified feature in an approved direction:** Plan (if needed) → Build → Verify
   (→ Play and Review if it has an experience target).
4. **Visual readability problem:** Observe (`playtester`) → Diagnose (`game-designer` with
   `art-director`) → Design (`art-director`) → Build → Verify (`qa` ∥ `art-director`) → Play.
5. **Question only, no change wanted:** Observe and/or Diagnose → Next with findings.
>>>END

<<<FILE studio/roles/art-director.md#works-from
## Works from

- Visual issues from playtests, design specs with visual implications, builds to review.
- The project's art direction and constraints (e.g., asset budget).
>>>END

<<<FILE studio/roles/game-designer.md#works-from
## Works from

- Playtest observations, Director decisions, spec questions from engineering or QA.
- Project vision, constraints, relevant design documents and Decisions.
>>>END

<<<FILE studio/roles/game-director.md#works-from
## Works from

- A diagnosis with options (usually from `game-designer`), or Review inputs: playtest observations
  and QA results.
- Project vision, constraints, and the Decisions the question touches.
>>>END

<<<FILE studio/roles/gameplay-engineer.md#works-from
## Works from

- An approved spec or a defect report, each with acceptance criteria.
- A plan, when the Technical Director made one.
- Project constraints and the repository.
>>>END

<<<FILE studio/roles/playtester.md#works-from
## Works from

A Handoff composed by the Studio (never one written by a Role that knows the implementation):

- How to obtain and run the build, and which part to play.
- The player profile from the Project Context.
- Optionally a play focus that does not reveal the expected result (e.g., "pay attention to
  combat", not "check whether combat is less monotonous now").
>>>END

<<<FILE studio/roles/playtester.md#independence
## Independence

Works from the build and a player profile only, in a fresh executor context without implementation
history. Is not told what changed or what result is expected, so that it cannot confirm a
hypothesis it was handed.
>>>END

<<<FILE studio/roles/qa.md#works-from
## Works from

- For defects: the Owner's report and the relevant design documents.
- For verification: acceptance criteria, how to exercise the change, project constraints (e.g.,
  supported platforms and frame rates).
- Never the implementer's self-assessment or reasoning: a Handoff's `## Sender assessment` section
  is removed before QA receives it.
>>>END

<<<FILE studio/roles/qa.md#independence
## Independence

Verify from the spec, the acceptance criteria and the build — not from the engineer's explanation
of why it should work. Prefer a fresh executor context without the implementation history.
>>>END

<<<FILE studio/roles/technical-director.md#works-from
## Works from

- An approved spec with acceptance criteria, or a technical problem to diagnose.
- Project constraints, repository location, relevant Decisions.
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

<<<FILE studio/templates/escalation.md
---
kind: escalation
goal: G-NNN
seq: N
from: <role-id that prepared the brief>
to: owner
status: open            # open | resolved
decision: <D-NNN once resolved>
---
# NN: Owner decision needed — <question in a few words>

<!-- Written in the project's owner_language. -->

## Question

<One sentence the Owner can answer without reading anything else.>

## Why this needs the Owner

<Which escalation trigger fires (studio/orchestration.md) and why the Studio must not decide.>

## Options

### Option A — <name>

<What it means for the game, cost, risk, reversibility.>
If chosen: <the route the Studio takes next.>

### Option B — <name>

<…>
If chosen: <…>

## Studio recommendation

<Option X.>

## Reasoning

<Why, and what evidence would change the recommendation.>

## Meanwhile

<Independent work that continues, or "Nothing; all remaining steps depend on this answer.">

## Owner decision required

<A / B — reply with the option and any conditions.>
>>>END

<<<FILE studio/templates/goal.md
---
kind: goal
id: G-NNN
project: <project-id>
status: active          # active | blocked-on-owner | done | abandoned
created: YYYY-MM-DD
---
# G-NNN: <short title>

## Owner request

> <the Owner's words, verbatim>

## Interpretation

<The Goal as an observable success condition. What is out of scope.>

## Unknowns

<Each stage entry question (studio/workflows/development-loop.md) that the Project Context cannot
answer, and the stage it creates. Also: stages skipped and why.>

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | <stage> | <role-id> | <skill-id> | planned | — |

Status: planned | tentative | open | done | skipped. Handoff: the incoming Handoff that starts the
step. Parallel steps: 2a, 2b. Step numbers need not
match Handoff seq numbers. The route is a plan; the Route operation revises it.

## Route changes

<After which step, what changed, and why.>

## Next action

<Who starts what next, with which Handoff. Or: waiting for the Owner on <escalation>.>

## Outcome

<At close, for the Owner, in owner_language: results, Decisions made, next issues, Owner items.>
>>>END

<<<FILE project.md
---
kind: project
id: lantern-depths
name: Lantern Depths (sample)
repository: none (sample project for dry-runs; builds are simulated under sim/)
owner_language: ja
player_visible: sim/build-*.md
---
# Project: Lantern Depths (sample)

## Vision

A short-session top-down action roguelite: descend through lantern-lit caves, one room at a time.
Pillars:

1. **One-button combat.** Depth comes from positioning, timing and enemy behavior, not from input
   complexity. Attack and dash are the whole kit (D-001).
2. **Short runs.** A full run takes 15–20 minutes.
3. **Readable threats.** Every threat is visible before it can hurt the player.

## Player profile

Action players who want short, intense runs. Comfortable with dodging and spacing; not interested in
memorizing combo lists. Mostly play with a gamepad.

## Current state

Vertical-slice prototype, build 0.3: 5 rooms in one cave biome, 2 enemy types, player kit of attack
and dash. Dry-run only: "running the build" means reading `sim/build-0.3.md`.

## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).

## Art direction

Dark caves lit by the player's lantern; warm light against cold blue-black. Threats use saturated
orange/red so they read against the dark.

## Design index

- `design/combat.md` — player kit, damage and invulnerability rules, enemies.
>>>END

<<<FILE @project-files
decisions/D-001-one-button-combat.md
decisions/D-002-combat-direction-rooms-and-grub-charge.md
decisions/D-003-grub-charge-and-room-rules.md
decisions/D-004-technical-approach-grub-charge-and-waves.md
design/combat.md
goals/G-001-combat-monotony/01-studio-to-playtester.md
goals/G-001-combat-monotony/02-playtester-to-studio.md
goals/G-001-combat-monotony/03-studio-to-game-designer.md
goals/G-001-combat-monotony/04-game-designer-to-game-director.md
goals/G-001-combat-monotony/05-game-director-to-game-designer.md
goals/G-001-combat-monotony/06-game-designer-to-studio.md
goals/G-001-combat-monotony/07-studio-to-technical-director.md
goals/G-001-combat-monotony/08-technical-director-to-studio.md
goals/G-001-combat-monotony/goal.md
project.md
sim/build-0.3.md
sim/repo-notes.md
>>>END

<<<FILE @decision-titles
decisions/D-001-one-button-combat.md — D-001: Combat uses one attack button plus dash
decisions/D-002-combat-direction-rooms-and-grub-charge.md — D-002: 戦闘の単調さへの対応は「部屋の構成と進行」を主軸にし、敵の挙動追加は予告つき Grub 突進の1つに限る
decisions/D-003-grub-charge-and-room-rules.md — D-003: Grub 突進は同時に 1 体・方向固定・予告中は無害とし、部屋は突進スイッチで外せる
decisions/D-004-technical-approach-grub-charge-and-waves.md — D-004: 突進と波の技術方針 — 共通コントローラへの状態追加、スイープ判定、導出による同時 1 体、スポナーでのスイッチ
>>>END

<<<FILE goals/G-001-combat-monotony/goal.md
---
kind: goal
id: G-001
project: lantern-depths
status: active
created: 2026-10-10
---
# G-001: 戦闘の単調さの改善

## Owner request

> 戦闘が単調なので改善したい

## Interpretation

体験上の Goal。ビルド 0.3 の戦闘が、想定プレイヤー(短時間で濃いランを求め、回避と間合いに慣れたアクション好き)にとって単調に感じられない状態にする。
成功条件は質的なもので、プレイヤーが戦闘中に、ほぼ同じ行動の繰り返しではなく、状況に応じた位置取り・タイミング・敵の挙動への対応といった判断を実感できること。数値基準は Design の受け入れ基準で、最終判定は Review で決める。

範囲外:
- 新しい入力ボタンの追加(D-001 により Owner 承認なしでは不可)。
- 戦闘以外のシステムの変更。
- ラン長(15–20分)やビジョンの柱の変更。
- 原因の特定前に解決策を決めること。

## Unknowns

Project Context の確認結果:
- ビジョンの柱 1「ワンボタン戦闘」(D-001)は、攻撃とダッシュだけのキットで、深みは位置取り・タイミング・敵の挙動から生むと定めている。「単調」の解決策はこの枠内に収める必要がある。
- 現状はビルド 0.3(5部屋、敵2種、攻撃とダッシュ)。
- 即時エスカレーションは不要。Goal は再解釈を要さず、ビジョンや既存の Decision と衝突しない。ただし方向の決定で D-001 の変更や新ボタンが必要と分かれば、その時点でエスカレーションする。

各ステージの入口の問い:
- Observe: 単調さを実際にプレイして観察したか → 観察済み(Handoff 02)。ただし被弾直後のダッシュ中ダメージの疑い(問題 D)は未再現で、`qa` による再現が必要。
- Diagnose: 原因は分かっているか → 診断済み(Handoff 04。主因は敵挙動が各1種類で単純なこと(P1)と、部屋構成に進行がないこと(P2))。感触・実時間・演出・数値に関わる仮説 H1〜H4 は未確認。
- Decide: 方向・優先度・スコープの本当の選択があるか → あった。診断が D-001 の枠内の3案(敵の挙動 / 部屋の構成 / プレイヤー数値)を示し、`game-director` が D-002 で決めた(主軸は部屋の構成と進行、併用は予告つき Grub 突進の1つのみ)。
- Design: 意図する挙動は仕様化済みか → 戦闘仕様は `design/combat.md` に仕様化済み(Handoff 06、D-003)。突進の予告の見た目は未仕様(`art-director`)。
- Plan: 技術的アプローチは非自明か → 突進の挙動追加と波の出現が既存システムでどこまで容易か未確認。Director が実装前の実現性確認を求めたため必要。
- Build: ゲームを変更する必要があるか → ある(D-002)。
- Verify: Build の後は常に必要。
- Play: Goal は遊び心地に関する → 変更後に必要。H1〜H4 の実機確認もここで行う。
- Review: 体験の Goal かつ方向 Decision がある → 必要。

スキップしたステージ: なし。

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | playtester | playtest-session | done | [02-playtester-to-studio.md](02-playtester-to-studio.md)(開始 Handoff: [01-studio-to-playtester.md](01-studio-to-playtester.md)) |
| 2a | Diagnose | game-designer | diagnose-experience | done | [04-game-designer-to-game-director.md](04-game-designer-to-game-director.md)(開始 Handoff: [03-studio-to-game-designer.md](03-studio-to-game-designer.md)) |
| 2b | Observe(欠陥 D) | qa | reproduce-defect | planned(Handoff は後続の Studio 操作で作成。他のステップと独立) | —(次の空き seq で `NN-studio-to-qa.md`) |
| 3 | Decide | game-director | make-decision, prepare-owner-escalation | done(D-002) | [04-game-designer-to-game-director.md](04-game-designer-to-game-director.md)(出力: [05-game-director-to-game-designer.md](05-game-director-to-game-designer.md)、`decisions/D-002-combat-direction-rooms-and-grub-charge.md`) |
| 4 | Design(戦闘仕様) | game-designer | write-design-spec | done(`design/combat.md`、D-003) | [05-game-director-to-game-designer.md](05-game-director-to-game-designer.md)(出力: [06-game-designer-to-studio.md](06-game-designer-to-studio.md)) |
| 5a | Plan(実現性確認) | technical-director | technical-plan | open | [07-studio-to-technical-director.md](07-studio-to-technical-director.md) |
| 5b | Design(突進の予告の見た目) | art-director | write-design-spec | planned(仕様 §10 の条件が入力。5a と独立。Handoff は後続の Studio 操作で作成) | —(次の空き seq で `NN-studio-to-art-director.md`) |
| 6 | Build | gameplay-engineer | implement-change | planned(5a・5b の後。欠陥 D が 2b で確認された場合は、その修正を別途加える) | — |
| 7 | Verify | qa | verify-change | planned(Build の後は必須。予告の見た目があるため art-director を並列: visual-review) | — |
| 8 | Play | playtester | playtest-session | planned(新しい実行コンテキストで。H1〜H4 の実機確認も含む) | — |
| 9 | Review | game-director | review-outcome | planned(体験の Goal かつ方向 Decision あり) | — |

Status: planned | tentative | open | done | skipped. Handoff: the incoming Handoff that starts the
step. Parallel steps: 2a, 2b. Step numbers need not
match Handoff seq numbers. The route is a plan; the Route operation revises it.

## Route changes

- Step 1(Observe)の後: プレイテスターの観察報告(Handoff 02)は、体験の問題 A〜C(毎部屋同じ型、緊張感の欠如、ダッシュが戦闘で使われない)と、不具合の疑い D(被弾直後のダッシュ中にダメージを受けることがある)を報告した。計画どおり Diagnose(2a)に進む。
- 追加: 2b として `qa` による D の再現(`reproduce-defect`)を加えた。理由: D は仕様と食い違うか明らかな不具合の疑いであり、戻りルール(Play の結果が欠陥なら Observe は `qa`)に従う。2a の診断と互いの出力を使わない。
- 2a(Diagnose)の後: 診断(Handoff 04)は D-001 の枠内の3案を示し、方向・優先度・スコープの本当の選択があるため Decide(3)を確定し `open` にした。エスカレーションは不要と判断した。
- 3(Decide)の後: `game-director` が D-002 を記録した(主軸は案2の部屋の構成と進行、併用は予告つき Grub 突進の1つのみ。Spitter の変化、新しい敵、プレイヤー側の数値調整、キット変更は扱わない)。D-001 とビジョンの柱の範囲内で、新ボタンも不要なため、エスカレーションは発動しない。計画どおり Design(4)に進む。
- 3 の後の route 改訂: (a) Decide が実装前の実現性確認を求めたため、Plan(5a)を `planned` に確定した。(b) 突進の予告の見た目は `art-director` の範囲であり、Director も仕様後に回すと指示したため、Design(5b)を新設した。仕様が書き上がってから、5a と 5b を互いに独立なステップとして Handoff する(並列可。どちらも相手の出力を使わない)。(c) ゲーム変更が決まったため、Build(6)は `planned`、Verify(7)、Play(8)、Review(9)も `planned` に確定した。視覚要素(予告)が入るため、Verify は `art-director` の `visual-review` を並列に加える。
- 欠陥 D は、Director の指示どおり今回の戦闘仕様に含めない。2b の再現結果が出てから、ダッシュと被弾後の無敵の規則を設計書に書き足す。2b の Handoff は、Owner の報告と設計文書のみを `qa` に渡す必要がある。現在の Studio 操作ではその報告文が手元になく、推測で書かないため、後続の Studio 操作で作成する。
- Handoff 05 の編集(Route 手順 4–5): `stage` を `Specify` から開発ループの用語である `Design` に直した。Load に、受け手の Works from に合う `project.md#player-profile`(ゲームパッド主体のプレイヤー)と、元の観察である Handoff 02 を追加した。`Sender assessment` は触っていない。
- 観察と診断は `sim/build-0.3.md` と `design/combat.md` に基づくドライランであり、ゲームパッドの操作感・実時間・演出・数値(H1〜H4)は未確認。仕様の数値は暫定値として扱い、Play の確認後に調整する。
- 4(Design)の後: 仕様(Handoff 06)は計画どおりで、方向・優先度・スコープの選択は出ておらず、エスカレーションも発動しない(D-001、D-002 の範囲内。新ボタンなし)。Design(4)を `done` にし、Plan(5a)を `open` にした。
- 5a と 5b の Handoff について: 5a と 5b は独立で並列にできる(連続する seq で、route 番号に文字の接尾辞)。この Route 操作で書けるのは seq 7 の Handoff 1 つだけだったため、5a の Handoff(07)を先に作り、5b の Handoff は次の空き seq(08)で後続の Studio 操作が作る。5b の入力は `design/combat.md` §10 と `project.md#art-direction` で、`game-designer` の Sender assessment は渡さない。Handoff 06 が指示するとおり、Playtester に渡す Handoff には仕様の数値や §6.2 の体験の観点を書かない。
- 5a の Handoff(07)は Handoff 06 の Findings(客観的な仕様の内容)から Studio が組み立てた。`game-designer` の Sender assessment(確信度、暫定値の根拠)は技術計画に不要なので含めていない。

## Next action

Studio は Route を終えて停止する。次の操作は 3 つ(互いに独立)。
1. 人間が Handoff `goals/G-001-combat-monotony/07-studio-to-technical-director.md` から `technical-director`(Plan、`technical-plan`)のステップを開始する。成果は技術計画を載せた `to: studio` 宛ての Handoff。仕様が実現困難なら `outcome: question` で返し、Studio が戻りルールに従って Design または Decide に回す。
2. Studio が 5b(`art-director`、`write-design-spec`)の Handoff `08-studio-to-art-director.md` を作る Route 操作を行う。`design/combat.md` §10 と `project.md#art-direction` を渡す。5a と並行して進めてよい。
3. Studio が 2b(`qa`、`reproduce-defect`)の Handoff を作る。Owner の報告と設計文書のみを渡し、プレイテスターの推測は含めない。

その後の予定: 5a と 5b の両方が終わってから、Studio が Route を行い、Build(`gameplay-engineer`)に進む。

Owner への報告(日本語):
- 戦闘の仕様ができた。5 部屋の進行(基本 → 突進を読む → Spitter → 突進と弾の組み合わせ → 全部入り)と、予告つき Grub 突進(予告 0.7 秒、突進、隙)を定めた。突進は部屋 2、4、5 に入れ、スイッチで外せる。数値はすべて暫定値。
- D-001 や柱の変更は不要で、Owner の判断は要らない。
- 次は `technical-director` が実現性を確認し、並行して `art-director` が突進の予告の見た目を決める。その後に実装、QA、プレイテストへ進む。
- ゲームパッドの操作感や実時間は未確認のドライラン上の判断で、実機の確認後に調整する。
- 被弾直後のダッシュ中のダメージの疑いは、QA が別に再現する。

## Outcome

(未完了)
>>>END

<<<FILE goals/G-001-combat-monotony/08-technical-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 8
from: technical-director
to: studio
stage: Route
outcome: done
---
# 08: technical-director → studio — 戦闘仕様は既存システムの範囲で実現できる。技術計画と、設計者への確認 3 点を回す

## Task

技術計画(確認事項への回答、リスク、テスト方針、順序、並列化の可否)を受け取り、次の宛先を決める。`art-director` の結果と合わせて Build に進める。ただし Build の前に、下の「仕様の確認依頼」を `game-designer` に回すこと。

## Context

Goal G-001。`design/combat.md`(§2〜4、§6、§9)の実現性を確認した。調べたのは `sim/repo-notes.md` と `sim/build-0.3.md` の記述で、**コードそのものは読んでいない**。部屋データ、スポナー、弾の衝突、接触の判定形状は記述にないため、下では「前提」と書き、最初の作業(T0)で確認する。

## Findings

### 結論

- 仕様は D-001〜D-003 と制約(30/60 FPS、小さなチーム、再利用)の範囲で実現できる。範囲外の費用や不可逆な作業はない。`outcome: question` にはしない。
- 全体の大きさは中程度。新しい仕組みは、敵の状態(出現中、Windup、Charge、Recovery)、波の管理、部屋データの拡張、スイープ判定の 4 つ。
- 仕様と既存実装の食い違いが 2 件ある(下の「仕様の確認依頼」)。技術側では仕様を書き換えず、仕様の文面どおりに作る前提で計画した。

### §9 の確認事項への回答

| # | 問い | 回答 | 費用 |
|---|---|---|---|
| 1 | Grub に状態を足せるか。接触ダメージを状態で切り替えられるか | 可能。敵は 1 つの共通コントローラ(Idle / Chase / Attack)で、種別ごとの違いはデータと小さな攻撃ルーチンで持つ。ここに Spawning、Windup、Charge、Recovery を足し、突進型を `grub_charger`(Grub のデータ + 突進の数値)として定義する。接触ダメージを Chase と Charge だけで有効にする。**前提**: 噛みつきの判定が Attack のルーチン側にあり、状態で切れる。T0 で確認する。 | S〜M |
| 2 | 30 FPS で接触を取りこぼさないか | 現状の重なり判定だけでは保証できない(下の「判定の取りこぼし」)。スイープ判定を足せば保証できる。 | S |
| 3 | 同時に予告できる突進を 1 体に制限できるか | 可能。保存する状態は作らない。Windup に入る瞬間に、生きている他の突進型が Windup または Charge にいるかを調べる(敵は最大 4 体)。倒された敵は、HP が 0 になった時点で生存一覧から外す。同時に開始する場合は更新順で先の 1 体が取る。 | S |
| 4 | 部屋データで指定できるか | **部屋データの現状は記述になく、確認できない**(T0)。最小の拡張案は下の「部屋データ案」。突進スイッチは、スポナーが `grub_charger` を `grub` に置き換える 1 か所で実現する。 | M |
| 5 | 「最初に全部出す」前提か | **確認できない**(T0)。波に対応するには、部屋の終了条件を「すべての波が出現済みで、生きている敵が 0」に変える必要がある。これは部屋コントローラの変更で、扉やクリア演出など終了に紐づく処理が付いていれば波及する。 | M(波及しだい) |
| 6 | 秒の経過時間で進めているか | 可能性が高い。ループは可変 delta time で、プレイヤーのタイマーも秒、敵の怯みも 0.2 s。ただし Spitter の間隔と移動が秒かは未確認(T0)。ポーズ復帰の最初の更新に大きな delta が入る危険があるため、delta の上限(0.05 s)を設ける。 | S |
| 7 | 弾が壁で消え、敵を通り抜けるか | 記述にない(T0)。弾が壁とプレイヤーの層だけに当たる設定にすればよい見込み。 | S |

### 判定の取りこぼし(§9-2)

- 1 更新あたりの移動量: Charge は 30 FPS で約 0.27 タイル、60 FPS で約 0.13 タイル。ダッシュは 16 タイル/s なので、30 FPS で約 0.53 タイル。向かい合うと相対で 24 タイル/s、30 FPS で約 0.8 タイル。
- 接触の判定形状の大きさは仕様でも未定義(§8)で、ここでは確認できない。0.8 タイルは小さな判定を飛び越える可能性がある大きさ。
- **方針**: Charge 中の接触は、更新ごとに「Grub とプレイヤーの移動を相対運動として、更新の始点から終点まで」スイープ判定する。判定の形が円でない場合は、相対移動が 0.25 タイル以下になるよう分割する。
- 時間の扱い: 状態のタイマーは更新の delta を足して進め、状態の切り替わりでは余りを次の状態に持ち越す。これで状態の長さは 30 FPS で 1 更新(約 0.034 s)以内の誤差になり、仕様の許容(§0)に収まる。
- Charge の距離: 7.0 タイルちょうどで止める(最後の更新は距離で切る)。壁は、実際の移動量が要求量より小さかった時点で終了とする。「壁で止まる」既存の動きが壁沿いに滑る場合でも、突進は滑らず終わる。
- 更新の順序は、プレイヤー(入力、ダッシュ、無敵)→ 敵の移動 → 接触の解決 とする。順序が一定なら FPS による接触の有無の差は 1 更新以内に収まる。
- ダッシュ中の無敵は、既存の無敵フラグを読むだけにする。読み取りは 1 つの問い合わせ関数を通す。

### 部屋データ案(最小の変更)

- 部屋ごと: `grubSpeed`、`spitterInterval`、`chargeEnabled`、`slots`(Door / Far / L / R / FL / FR の座標)、`waves[]`。
- 波ごと: `spawns[{type, slot}]`(type は grub / grub_charger / spitter)、`next{K, T}`。「FL または FR のうち遠い方」は、スロットのリストと選択規則で書く。
- 全部屋共通の定数: 出現中 0.8 s、出現位置の待ち(4 タイル未満なら最大 2.0 s)、Spitter の最初の 1 発 1.0 s、弾速 4.0。部屋データには入れない。
- `chargeEnabled=false` のときは、スポナーが生成時に `grub_charger` を `grub` に置き換える。敵の数、波、位置は変わらない(V6)。
- 部屋データが既存の形式と大きく違う場合は、T0 で戻す。

### 技術的リスクと対策

| リスク | 対策 |
|---|---|
| R1 既存の Flinch(敵が被弾すると 0.2 s の怯みで Attack を含む行動を中断し Chase に戻る)が、仕様の「被弾しても状態を中断しない」(§2.1)と食い違う | 仕様の文面どおり、Spawning、Windup、Charge、Recovery では Flinch に入らない(ダメージは受ける)。Chase など他の状態の Flinch は既存のまま。確認を依頼する。 |
| R2 接触の定義。§3.5 と V3 の窓(0.25 s)は、接触を 1 点の瞬間として数えている。Grub の体は接触の開始後も重なり続ける | 下の確認依頼 2。解釈しだいで窓の幅が変わる。 |
| R3 取りこぼし、delta のばらつき、ポーズ復帰の大きな delta | スイープ判定、delta の上限、余りの持ち越し。ポーズ復帰の更新は V1 で確認する。 |
| R4 部屋データ、スポナー、終了条件の結合が強い | T0 で確認。強ければ T3 を拡大するか、仕様の波の使い方の再確認のために戻す。 |
| R5 無敵の実装を触ると、欠陥 D の調査と混ざる | この計画は無敵の挙動を変えない。読み取りの問い合わせ関数を足すだけにする。欠陥 D の修正は別の作業で、その関数の裏側を変えるだけで済む。D が再現された場合、被弾直後のダッシュの窓を V3/V4 の測定から外す。 |
| R6 突進中の敵どうしの通り抜け(仕様 §2.1)で、他の敵の押し合いが変に動く | 突進中の Grub は敵どうしの分離から除外する。他の敵は押さない。T2 でテストする。 |
| R7 出現位置にプレイヤーが重なった場合 | 押し出しは作らない。出現中の 0.8 s は無害で、見えるので動ける。待ち(最大 2.0 s)も仕様どおり。確認依頼 4 に記載。 |
| R8 セーブデータの互換 | 部屋の進行だけを持つ場合は影響なし。波の途中の状態を保存していないことを T0 で確認する。 |
| R9 art との接点。予告の見た目は art-director の別ステップ | 敵の状態、状態の経過割合、突進の方向を見た目側に渡す口を T2 で作る。art の結果が来るまでは、デバッグ表示(予告の線と停止)で代用する。柱3 の最終確認は実機の Play。 |

### テスト方針

**自動(今は敵と無敵のテストがないため新規)**

- 敵コントローラと波の管理を、固定 1/30 s、固定 1/60 s、ばらつく delta で進める検証用の枠。
- 状態の長さ(Windup 0.7、Recovery 0.8、出現中 0.8)が許容内(V1、V8)。Charge の速度と距離、方向の固定(V2)。接触ダメージが Chase と Charge のみ、1 回の突進で 1 回まで(V4)。
- スイープ判定: 距離を細かく変え、30 FPS と 60 FPS で接触の有無が一致する。ダッシュの窓: 開始時刻を接触の前後でずらし、境界が 30 FPS の 1 更新以内で一致する(V3)。
- 同時 1 体: Windup 中に倒す、Charge 中に倒す、同時に開始する(V5)。スイッチのオン/オフで敵の数、波、位置が同じ(V6)。
- 部屋データが §4.3 の表と一致する(V7)。弾の速度、最初の 1 発、壁、敵の通り抜け(V9)。
- プレイヤー側の定数(攻撃 0.35 s、ダッシュ 0.25 s・4 タイル・0.6 s、被弾 0.3 s・0.8 s)が変わっていない(V10)。定数だけを固定する。欠陥 D の挙動は固定しない。

**QA が実機で確認**

- V1〜V10 を 30 FPS と 60 FPS の両方で。特に V1 のポーズ復帰後、V3 の実際の入力、V8 の見え方。
- そのために、開発ビルド限定の補助を足す: 部屋の選択、突進スイッチの切り替え、FPS の 30/60 切り替え、状態の遷移ログ。これらは出荷ビルドに入れない。プレイヤー向けの新しい入力は足さない(D-001)。
- 体験の観点(§6.2)は Play で見る。

### 順序

1. **T0 調査(S)**: コントローラ、スポナー、部屋の終了条件、弾の衝突、delta とポーズ、判定形状、セーブを確認する。前提が崩れたらここで戻す。
2. **T1 土台(S〜M)**: delta の上限とポーズ復帰、検証用の枠、プレイヤー定数のテスト、無敵の問い合わせ関数(挙動は変えない)、T2/T3 の境界(生成の引数、倒れたときの通知)。
3. **T2 敵(M)**: Spawning、Windup、Charge、Recovery、Flinch の除外、同時 1 体、スイープ判定、見た目への口、Spitter の最初の 1 発、弾の確認。
4. **T3 部屋(M)**: スキーマ、波の管理、スロット、出現待ち、突進スイッチ、部屋ごとの数値、終了条件の変更。
5. **T4 統合とデータ(S)**: 合流、§4.3 の 5 部屋を入力、V7 の自動テスト。
6. **T5 QA 準備(S)**: 開発用補助。そのあと QA へ。

依存: T0 → T1 → (T2 ∥ T3) → T4 → T5。art の結果は T4 以降で組み込む。

### 並列化

- **T2 と T3 は並列にできる(条件つき)。** 変更するコードが分かれる。T2 は敵のコントローラと種別データ、T3 は部屋、スポナー、データ。境界は T1 で固定する小さなインターフェース 2 つ(生成の引数、倒れたときの通知)。理由は、どちらも中規模で独立して進められ、先に境界を決めれば合流の衝突が少ないため。
- 隔離した作業場所は T2/T3 の間だけ使う。
- **条件**: T0 で、部屋のコードと敵のコントローラが別のモジュールだと確認できること。同じファイルに絡んでいれば直列にする。出現中の状態と Spitter のタイマーは、衝突を避けるため T2 に置く。
- 無敵のコードは触らないので、欠陥 D の修正とは並列でも衝突しない。ただし V3/V4 の測定は混ざりうる(R5)。

### 仕様の確認依頼(game-designer へ。Build の前、V3 の前に必要)

1. **Flinch(R1)**: 既存の敵は被弾で 0.2 s の怯みに入り、行動を中断する。§2.1 と §8 は「怯みは既存のまま」と「状態を中断しない」を同時に書いている。計画は、Spawning、Windup、Charge、Recovery だけ怯みを無効にし、他は既存のままとして組む。この解釈でよいか。§2.1/§8 に Flinch を明記してほしい。
2. **接触の定義(R2)**: Charge 中の Grub の体は、接触の開始後もしばらくプレイヤーと重なる。§3.5 と V3 の窓(0.25 s、接触の 0.25 s 前から瞬間まで)を成り立たせるには、突進ごとに最初の重なりで接触を 1 回だけ解決する必要がある。そのとき無敵ならダメージなしで、その突進はもうダメージを与えない。重なっている間ずっと判定すると、窓は重なりの長さ(おおよそ 0.1〜0.2 s)だけ狭くなる。計画は前者で組む。それでよいか。
3. **部屋 5 の波 2 の「FL または FR」**: 部屋 3 の「プレイヤーから遠い方」と同じ規則でよいか。計画は同じ規則で組む。データだけの変更で直せる。

次の 2 点は影響が小さいため、確認なしで次の既定で進める。違えば知らせてほしい。

4. 「出現中が終わってから T s」は、その波の最後の敵の出現中が終わった時点を起点にする。「生きている敵」には出現中の敵を含める。出現位置の重なりは押し出さない(R7)。

## Decisions already made

- D-001: 戦闘は攻撃ボタン 1 つとダッシュのみ。開発用補助は出荷ビルドに入れず、プレイヤー向けの入力を足さない。
- D-002: 主軸は部屋の構成と進行。敵の挙動の追加は予告つき Grub 突進のみ。
- D-003: 突進の規則と部屋ごとの突進スイッチ。
- D-004(今回、technical-director): 技術方針(スイープ判定、delta の上限と余りの持ち越し、導出による同時 1 体、スポナーでのスイッチ、見た目への口、無敵の問い合わせ関数)。

## Constraints

- 仕様は変えていない。上の確認依頼は仕様の変更の提案ではなく、仕様の文面と既存実装の食い違いの確認。
- この Handoff の Findings には実装の情報が入っている。Playtester には渡さない。
- 欠陥 D は別ステップ(`qa` の再現)。この計画では無敵の挙動を変えない。

## Open questions

- 上の確認依頼 1〜3(`game-designer`)。1 と 2 は V3、V4、V1 の合否に関わる。
- T0 の調査結果しだいで、部屋データとスポナーの結合が強い場合は、T3 の大きさと並列化の可否を見直す。その場合は新しい計画を Studio に返す。

## Expected output

- Studio は、確認依頼 1〜3 を `game-designer` に回す(Design)。`art-director` の結果と合わせて Build に進める。
- Build は T0 から始める。T0 で前提が崩れた場合は、Studio に戻す。
- Build のあと `qa` が §6.1 の V1〜V10 を 30 FPS と 60 FPS で確認する。

## Sender assessment

- 確信度: 実現性は中〜高。根拠は記述のみで、コードは読んでいない。特に部屋データ、スポナー、弾の衝突、接触の判定形状は未確認で、費用の見積もりはここが動く。
- 欠陥 D の仮説(`qa` には渡さない): 無敵が 1 つのフラグで、ダッシュと被弾の 2 つのタイマーが別々に切る。そのため、被弾後の無敵の途中でダッシュを始めると、先に切れるタイマーがフラグを落とし、ダッシュの途中で無敵が消えうる。突進が入ると、被弾直後に回避を試みる場面が増えるため、この欠陥に当たる頻度が上がる可能性がある。D が再現されたら、修正を Play の前に入れる方がよい。
- 確認依頼 2 は、窓の幅(Play でダッシュが「使える」と感じられるか)に直結する。仕様の数値を実機で見る前に決めておく価値がある。
- Owner のエスカレーションは不要。

## Load

- Role: none(Studio の routing)
- Skills: none
- Project: design/combat.md(§2〜4、§6、§9), project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-direction-rooms-and-grub-charge.md, decisions/D-003-grub-charge-and-room-rules.md, decisions/D-004-technical-approach-grub-charge-and-waves.md
- Previous handoff: goals/G-001-combat-monotony/07-studio-to-technical-director.md
>>>END
