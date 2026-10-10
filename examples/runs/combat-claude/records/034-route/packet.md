# Studio operation packet

operation: Route
goal: G-001
step_artifact: goals/G-001-combat-monotony/28-gameplay-engineer-to-studio.md
next_seq: 29

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/28-gameplay-engineer-to-studio.md (in place: keep kind, goal, seq, from, to)
- goals/G-001-combat-monotony/29-studio-to-<role>.md

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
decisions/D-005-flinch-contact-and-far-slot-rules.md
decisions/D-006-grub-charge-telegraph-visual.md
decisions/D-007-build-without-code-access-assumption-register.md
decisions/D-008-owner-simulated-build-judgment.md
decisions/D-009-wave-condition-start-and-waiting-enemies.md
design/combat.md
design/grub-charge-telegraph.md
goals/G-001-combat-monotony/01-studio-to-playtester.md
goals/G-001-combat-monotony/02-playtester-to-studio.md
goals/G-001-combat-monotony/03-studio-to-game-designer.md
goals/G-001-combat-monotony/04-game-designer-to-game-director.md
goals/G-001-combat-monotony/05-game-director-to-game-designer.md
goals/G-001-combat-monotony/06-game-designer-to-studio.md
goals/G-001-combat-monotony/07-studio-to-technical-director.md
goals/G-001-combat-monotony/08-technical-director-to-studio.md
goals/G-001-combat-monotony/09-studio-to-game-designer.md
goals/G-001-combat-monotony/10-game-designer-to-studio.md
goals/G-001-combat-monotony/11-studio-to-art-director.md
goals/G-001-combat-monotony/12-art-director-to-studio.md
goals/G-001-combat-monotony/13-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/14-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/15-studio-to-technical-director.md
goals/G-001-combat-monotony/16-technical-director-to-studio.md
goals/G-001-combat-monotony/17-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/18-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/19-studio-to-technical-director.md
goals/G-001-combat-monotony/20-technical-director-to-owner.md
goals/G-001-combat-monotony/21-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/22-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/23-studio-to-game-designer.md
goals/G-001-combat-monotony/24-game-designer-to-studio.md
goals/G-001-combat-monotony/25-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/26-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/27-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/28-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/goal.md
project.md
sim/build-0.3.md
sim/build-0.4.md
sim/repo-notes.md
>>>END

<<<FILE @decision-titles
decisions/D-001-one-button-combat.md — D-001: Combat uses one attack button plus dash
decisions/D-002-combat-direction-rooms-and-grub-charge.md — D-002: 戦闘の単調さへの対応は「部屋の構成と進行」を主軸にし、敵の挙動追加は予告つき Grub 突進の1つに限る
decisions/D-003-grub-charge-and-room-rules.md — D-003: Grub 突進は同時に 1 体・方向固定・予告中は無害とし、部屋は突進スイッチで外せる
decisions/D-004-technical-approach-grub-charge-and-waves.md — D-004: 突進と波の技術方針 — 共通コントローラへの状態追加、スイープ判定、導出による同時 1 体、スポナーでのスイッチ
decisions/D-005-flinch-contact-and-far-slot-rules.md — D-005: 突進型は 3 状態で怯まない、接触は突進ごとに最初の重なりで 1 回だけ解決する、「遠い方」は出現を決める時点で選ぶ
decisions/D-006-grub-charge-telegraph-visual.md — D-006: 突進の予告は「地面のレーン + 熾火の点灯 + 沈み込み」で示し、赤橙は害になる状態だけに使う
decisions/D-007-build-without-code-access-assumption-register.md — D-007: コードを読めない状況では、T0 を「前提の台帳」に置き換え、前提ごとに検出点と戻し先を決めて Build を進める
decisions/D-008-owner-simulated-build-judgment.md — D-008: Build は変更内容を Handoff に正確に書いた時点で完了とし、Goal は模擬ビルドに基づいて判定する(Escalation 20 の Option C)
decisions/D-009-wave-condition-start-and-waiting-enemies.md — D-009: 次の波の K と T は、前の波の全員が出現中に入った時点から調べ始め、出現位置の待ちの敵は「生きている敵」に数えない
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

Owner の判断(D-008): このプロジェクトは模擬専用のサンプルとして扱い、`sim/repo-notes.md` をコードとする。Build は変更内容を Handoff に正確に書いた時点で完了で、模擬ビルドはランタイムのシミュレーターがその変更内容から作る。Goal の判定は模擬ビルドに基づいて行い、結果には模擬であることを明記する。

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
- Decide: 方向・優先度・スコープの本当の選択があるか → あった。診断が D-001 の枠内の3案(敵の挙動 / 部屋の構成 / プレイヤー数値)を示し、`game-director` が D-002 で決めた(主軸は部屋の構成と進行、併用は予告つき Grub 突進の1つのみ)。コードのない環境での Build の進め方は Owner が D-008 で決めた。
- Design: 意図する挙動は仕様化済みか → 戦闘仕様は `design/combat.md` に仕様化済みで、技術確認で出た食い違い 3 点も D-005 で解消済み(Handoff 10)。突進の予告の見た目も `design/grub-charge-telegraph.md` と D-006 で仕様化済み(Handoff 12)。Build の記述中に見つかった、波の条件を調べ始める時点の未定義は D-009 で解消済み(Handoff 24)。
- Plan: 技術的アプローチは非自明か → 実現性確認は完了(Handoff 08、D-004)。T0 は D-007 で「前提の台帳」に置き換え済み。コードにアクセスできない問題は Owner の回答(D-008)で解消し、`sim/repo-notes.md` をコードとして扱う。
- Build: ゲームを変更する必要があるか → ある(D-002)。D-008 により、変更内容を Handoff に正確に書くことで完了とする。
- Verify: Build の後は常に必要。対象は模擬ビルド。
- Play: Goal は遊び心地に関する → 変更後に必要。対象は模擬ビルド。H1〜H4 は実機では確認できないため、Outcome に限界として書く。
- Review: 体験の Goal かつ方向 Decision がある → 必要。模擬ビルドに基づく判定であることを明記する。

スキップしたステージ: なし。

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | playtester | playtest-session | done | [02-playtester-to-studio.md](02-playtester-to-studio.md)(開始 Handoff: [01-studio-to-playtester.md](01-studio-to-playtester.md)) |
| 2a | Diagnose | game-designer | diagnose-experience | done | [04-game-designer-to-game-director.md](04-game-designer-to-game-director.md)(開始 Handoff: [03-studio-to-game-designer.md](03-studio-to-game-designer.md)) |
| 2b | Observe(欠陥 D) | qa | reproduce-defect | planned(Escalation の答えに依存しない。Owner の報告の原文が入力にないため Handoff は未作成。後続の Studio 操作で作成。他のステップと独立) | —(次の空き seq で `NN-studio-to-qa.md`) |
| 3 | Decide | game-director | make-decision, prepare-owner-escalation | done(D-002) | [04-game-designer-to-game-director.md](04-game-designer-to-game-director.md)(出力: [05-game-director-to-game-designer.md](05-game-director-to-game-designer.md)、`decisions/D-002-combat-direction-rooms-and-grub-charge.md`) |
| 4 | Design(戦闘仕様) | game-designer | write-design-spec | done(`design/combat.md`、D-003) | [05-game-director-to-game-designer.md](05-game-director-to-game-designer.md)(出力: [06-game-designer-to-studio.md](06-game-designer-to-studio.md)) |
| 5a | Plan(実現性確認) | technical-director | technical-plan | done(D-004。仕様は実現可能。確認依頼 3 点あり) | [07-studio-to-technical-director.md](07-studio-to-technical-director.md)(出力: [08-technical-director-to-studio.md](08-technical-director-to-studio.md)) |
| 5b | Design(突進の予告の見た目) | art-director | write-design-spec, make-decision | done(`design/grub-charge-telegraph.md`、D-006。戦闘の規則の変更なし) | [11-studio-to-art-director.md](11-studio-to-art-director.md)(出力: [12-art-director-to-studio.md](12-art-director-to-studio.md)) |
| 5c | Design(仕様の確認: 怯み・接触の定義・部屋 5 の FL/FR) | game-designer | write-design-spec, make-decision | done(D-005。方向・スコープの変更なし) | [09-studio-to-game-designer.md](09-studio-to-game-designer.md)(出力: [10-game-designer-to-studio.md](10-game-designer-to-studio.md)) |
| 6 | Build(1 回目) | gameplay-engineer | implement-change | done(`outcome: question`。T0 を完了できず、実装なし) | [13-studio-to-gameplay-engineer.md](13-studio-to-gameplay-engineer.md)(出力: [14-gameplay-engineer-to-studio.md](14-gameplay-engineer-to-studio.md)) |
| 6a | Plan(T0 を実施できない場合の進め方の再確認) | technical-director | technical-plan, make-decision | done(D-007。T0 を前提の台帳に置き換え、方針 D-004 は維持) | [15-studio-to-technical-director.md](15-studio-to-technical-director.md)(出力: [16-technical-director-to-studio.md](16-technical-director-to-studio.md)) |
| 6b | Build(再開) | gameplay-engineer | implement-change | done(`outcome: question`。コードを読み書きできず、台帳のプローブも実装もできなかった。D-007 の 7 に該当し、再試行せず返した) | [17-studio-to-gameplay-engineer.md](17-studio-to-gameplay-engineer.md)(出力: [18-gameplay-engineer-to-studio.md](18-gameplay-engineer-to-studio.md)) |
| 6c | Plan(コードにアクセスできない Build の進め方、Owner 確認の要否) | technical-director | technical-plan, prepare-owner-escalation, make-decision | done(Owner の判断が必要と判断し Escalation を作成) | [19-studio-to-technical-director.md](19-studio-to-technical-director.md)(出力: [20-technical-director-to-owner.md](20-technical-director-to-owner.md)) |
| 6d | Decide(Owner) | owner | — | done(D-008。Owner は Option C を選択。`sim/repo-notes.md` をコードとして扱い、Build は変更内容の記述で完了、判定は模擬ビルドに基づく) | [20-technical-director-to-owner.md](20-technical-director-to-owner.md)(Decision: `decisions/D-008-owner-simulated-build-judgment.md`) |
| 6e | Build(変更内容の記述。D-008 により、記述の完了で Build 完了) | gameplay-engineer | implement-change | done(`outcome: question`。変更内容は 1 点を除き完了。波 2 以降の条件を調べ始める時点が仕様に未定義) | [21-studio-to-gameplay-engineer.md](21-studio-to-gameplay-engineer.md)(出力: [22-gameplay-engineer-to-studio.md](22-gameplay-engineer-to-studio.md)) |
| 6f | Design(波の条件の欠落 + §10 の参照追記) | game-designer | write-design-spec, make-decision | done(D-009。案 A: 前の波の全員が出現中に入った時点から K・T を調べ始め、待ちの敵は数えない。§10 の参照追記も完了。数値の変更なし) | [23-studio-to-game-designer.md](23-studio-to-game-designer.md)(出力: [24-game-designer-to-studio.md](24-game-designer-to-studio.md)) |
| 6g | Build(記述の確定: 2.1 に 1 文を足す) | gameplay-engineer | implement-change | done(`outcome: question`。Handoff 25 の Load に Handoff 22 が入っておらず、記述の全体を書けなかった。Studio の Load の漏れで、仕様の問題ではない。規則の追跡(V7、V12)は Handoff 26 に下書きとして残った) | [25-studio-to-gameplay-engineer.md](25-studio-to-gameplay-engineer.md)(出力: [26-gameplay-engineer-to-studio.md](26-gameplay-engineer-to-studio.md)) |
| 6h | Build(記述の確定のやり直し。Handoff 22 を Load に加えた) | gameplay-engineer | implement-change | open(`to: studio` で返し、Verify の Handoff 組み直しに備える。確定した変更内容の全体を Findings に自己完結で書かせる) | [27-studio-to-gameplay-engineer.md](27-studio-to-gameplay-engineer.md) |
| 7 | Verify(模擬ビルド。視覚要素があるため `art-director` を並列に加える: visual-review) | qa | verify-change | planned(6h の後、ランタイムのシミュレーターが変更内容から模擬ビルドを作ってから開始。Handoff は Studio が受け手ごとに新しく組み、Build の Sender assessment は `qa` に渡さない。V7 と V12 を含める) | — |
| 8 | Play(模擬ビルド) | playtester | playtest-session | planned(7 の後。新しい実行コンテキストで、模擬ビルドとプレイヤー像のみを渡す。H1〜H4 は実機では確認できない) | — |
| 9 | Review(模擬ビルドに基づく判定) | game-director | review-outcome | planned(8 の後。判定は模擬ビルドに基づく旨と、実機で確認できていない点を明記する) | — |

Status: planned | tentative | open | done | skipped. Handoff: the incoming Handoff that starts the
step. Parallel steps: 2a, 2b. Step numbers need not
match Handoff seq numbers. The route is a plan; the Route operation revises it.

## Route changes

- Step 1(Observe)の後: プレイテスターの観察報告(Handoff 02)は、体験の問題 A〜C(毎部屋同じ型、緊張感の欠如、ダッシュが戦闘で使われない)と、不具合の疑い D(被弾直後のダッシュ中にダメージを受けることがある)を報告した。計画どおり Diagnose(2a)に進む。
- 追加: 2b として `qa` による D の再現(`reproduce-defect`)を加えた。理由: D は仕様と食い違うか明らかな不具合の疑いであり、戻りルール(Play の結果が欠陥なら Observe は `qa`)に従う。2a の診断と互いの出力を使わない。
- 2a(Diagnose)の後: 診断(Handoff 04)は D-001 の枠内の3案を示し、方向・優先度・スコープの本当の選択があるため Decide(3)を確定し `open` にした。エスカレーションは不要と判断した。
- 3(Decide)の後: `game-director` が D-002 を記録した(主軸は案2の部屋の構成と進行、併用は予告つき Grub 突進の1つのみ。Spitter の変化、新しい敵、プレイヤー側の数値調整、キット変更は扱わない)。D-001 とビジョンの柱の範囲内で、新ボタンも不要なため、エスカレーションは発動しない。計画どおり Design(4)に進む。
- 3 の後の route 改訂: (a) Decide が実装前の実現性確認を求めたため、Plan(5a)を `planned` に確定した。(b) 突進の予告の見た目は `art-director` の範囲であり、Director も仕様後に回すと指示したため、Design(5b)を新設した。仕様が書き上がってから、5a と 5b を互いに独立なステップとして Handoff する(並列可。どちらも相手の出力を使わない)。(c) ゲーム変更が決まったため、Build(6)は `planned`、Verify(7)、Play(8)、Review(9)も `planned` に確定した。視覚要素(予告)が入るため、Verify は `art-director` の `visual-review` を並列に加える。
- 欠陥 D は、Director の指示どおり今回の戦闘仕様に含めない。2b の再現結果が出てから、ダッシュと被弾後の無敵の規則を設計書に書き足す。2b の Handoff は、Owner の報告と設計文書のみを `qa` に渡す必要がある。報告文の原文は後続の Studio 操作で用意し、推測で書かない。
- Handoff 05 の編集(Route 手順 4–5): `stage` を `Specify` から開発ループの用語である `Design` に直した。Load に、受け手の Works from に合う `project.md#player-profile`(ゲームパッド主体のプレイヤー)と、元の観察である Handoff 02 を追加した。`Sender assessment` は触っていない。
- 観察と診断は `sim/build-0.3.md` と `design/combat.md` に基づくドライランであり、ゲームパッドの操作感・実時間・演出・数値(H1〜H4)は未確認。仕様の数値は暫定値として扱い、Play の確認後に調整する。
- 4(Design)の後: 仕様(Handoff 06)は計画どおりで、方向・優先度・スコープの選択は出ておらず、エスカレーションも発動しない(D-001、D-002 の範囲内。新ボタンなし)。Design(4)を `done` にし、Plan(5a)を `open` にした。
- 5a と 5b の Handoff について: 5a と 5b は独立で並列にできる(連続する seq で、route 番号に文字の接尾辞)。この Route 操作で書けるのは seq 7 の Handoff 1 つだけだったため、5a の Handoff(07)を先に作り、5b の Handoff は後続の Studio 操作が作る。5b の入力は `design/combat.md` §10 と `project.md#art-direction` で、`game-designer` の Sender assessment は渡さない。Handoff 06 が指示するとおり、Playtester に渡す Handoff には仕様の数値や §6.2 の体験の観点を書かない。
- 5a の Handoff(07)は Handoff 06 の Findings(客観的な仕様の内容)から Studio が組み立てた。`game-designer` の Sender assessment(確信度、暫定値の根拠)は技術計画に不要なので含めていない。
- 5a(Plan)の後: 技術計画(Handoff 08、D-004)は、仕様が D-001〜D-003 と制約の範囲で実現できると結論した。コードは読まず `sim/` の記述に基づく見積もりで、部屋データ、スポナー、弾の衝突、接触の判定形状は Build の最初の作業 T0 で確認する。`outcome: question` ではないため、Plan の戻りルール(仕様が実現不能)は適用しない。エスカレーションの条件(コンセプト・柱・Decision の変更、スコープ・費用・リスクの大幅な変化、不可逆な変更)にも当たらないと判断した。
- 5a の後の route 改訂: 技術側が仕様の文面と既存実装の食い違いを 3 点(怯みの扱い、接触の定義、部屋 5 の FL/FR)見つけ、仕様側の決定が要るため、Design(5c、`game-designer`)を新設して `open` にした(Handoff 09)。これは仕様の解釈であり、技術側は決められない。Build は 5b と 5c の両方の後に進める。5c は 5b と互いの出力を使わないので並列にできる。5c の答えが D-002 や D-003 の変更、スコープの変更を要する場合は、`game-designer` が `question` で返し、Decide(`game-director`)に回す。
- Handoff 09 の作り方(Route 手順 4–5): 受け手 `game-designer` の Works from(仕様の質問、Decision、設計文書)に合わせ、Handoff 08 の Findings から確認依頼 1〜3 と既定 4、判断材料の技術的事実だけを抜き出した。Handoff 08 の Sender assessment(欠陥 D の仮説を含む)は渡していない。欠陥 D の仮説は `qa` の再現に先入観を与えるため、2b の Handoff にも含めない。
- Handoff 08 は編集していない(受け手は Studio で、Load は Studio の routing のため)。
- Build が T2 と T3 を並列にする条件は、T0 で部屋のコードと敵のコントローラが別モジュールだと確認できること。Build の Handoff を作るときに、この条件と T0 で前提が崩れたときの Studio への戻しを Expected output に書く。Handoff 08 のとおり、開発用補助(部屋の選択、突進スイッチ、30/60 FPS 切り替え、状態の遷移ログ)は開発ビルド限定で、プレイヤー向けの新しい入力は足さない。
- 5c(Design)の後: 仕様の確認(Handoff 10、D-005)は D-001〜D-003 の範囲内で決まり、`outcome: done`。方向・優先度・スコープの変更も新ボタンもなく、エスカレーションの条件に当たらない。`game-director` に回す必要もない。5c を `done` にした。Handoff 10 の質問「欠陥 D の規則の追記」は 2b の結果待ちで、Build の前提ではない。
- 5c の後の次の操作: Build は 5b の後という計画を変えない。残る前提は 5b だけなので、Handoff 11 で `art-director` に 5b を始める。Handoff 11 は、受け手 `art-director` の Works from(設計仕様の視覚的含意、美術方針と制約)に合わせて Studio が組み立てた。Handoff 10 の Findings のうち視覚に関わる客観的な事実(怯まない 3 状態、接触の解決の仕方)だけを抜き出し、`game-designer` の Sender assessment と実装側への影響(Playtester・art に不要)は渡していない。`design/combat.md` §10 の本文はこの操作の入力になかったため、Handoff 11 では要約せず Load で指定した。Previous handoff を none にしたのは、Handoff 10 に Sender assessment が含まれ、5b の方針(渡さない)に反するため。
- 2b(欠陥 D の `qa`)の Handoff は今回も作っていない。理由: この操作で書けるのは seq 11 の 1 つで、5b の方が Build を止めている前提になる。2b は Build を止めず、独立している(Build の前に結果があれば、欠陥修正を Build に加える)。Owner の報告の原文が入力にないため、推測で書かない。
- Build の Handoff を作るときの条件(Route 手順 4–5 のため記録): 5b の結果(視覚要素の一覧、既存の仕組みで足りるかの見立て)と `design/combat.md`、D-004、D-005 を渡す。Handoff 10 の「実装側への影響」(解決済みフラグ、除外状態、遠い方の選択はデータの規則)は技術情報として `gameplay-engineer` に渡してよいが、Sender assessment は渡さない。
- 5b(Design)の後: 視覚仕様(Handoff 12、D-006)は `outcome: done`。`art-director` は戦闘の規則・数値の変更は不要と判断しており、`question` ではない。D-001〜D-005 の範囲内で、新ボタンも方向・スコープの変更もなく、エスカレーションの条件に当たらない。5b を `done` にし、計画どおり Build(6)を `open` にした(Handoff 13)。
- Handoff 13 の作り方(Route 手順 4–5): 受け手 `gameplay-engineer` の Works from(承認済みの仕様、計画、制約、リポジトリ)に合わせ、Handoff 12 の Findings から視覚要素と見立て・未確認の点を客観的な事実として抜き出した。Handoff 12 と同様、Sender assessment(確信度、費用の見立ての根拠)は渡していない。Handoff 08 も Previous handoff にせず(Sender assessment に欠陥 D の仮説があるため)、計画の内容は D-004 を Load で渡す。Handoff 12 は編集していない(`to: studio` で、Load は Studio の routing のため)。Expected output に、Verify で `qa` と `art-director` を並列にするための `to: studio` と、T0 の結果で前提が崩れたときの戻し先(仕様の欠落は Design、計画の不成立は Plan、視覚要素の実現不能は `art-director` への仕様調整を Studio 経由で)を書いた。
- 未処理(Build を止めない): Handoff 12 の Open question により、`design/combat.md` §10 に `design/grub-charge-telegraph.md` への参照を追記する必要がある。書き込めるのは `game-designer` のため、後続の Studio 操作で小さな Handoff(次の空き seq)として回す。Build は視覚仕様を Load で直接読むので、これを待たない。ただし Verify の前に済ませる。
- Playtester に渡す Handoff には、視覚仕様 §10.2 の体験の観点を書かない(Handoff 12 の指示、および Playtester の Independence)。
- 6(Build 1 回目)の後: Handoff 14 は `outcome: question`。実装に入らず、T0 を完了できなかった理由は、その実行にゲームのコード・ビルド・テスト実行の手段がなかったこと。`project.md` は `repository: none`(サンプルで、ビルドは `sim/` で模擬)と明記しており、Handoff 14 の選択肢 (a)「リポジトリを使える形で Build をやり直す」は Studio が用意できない。選択肢 (b)「別の担当に T0 だけをさせる」も、同じ入力では同じ結果になる。したがって Studio 単独で選べる process の問題ではなく、Build をどう進めるかという技術方針・順序(`technical-director` の権限)の問題になる。戻りルール「Build: 計画が成り立たない場合 → Plan(`technical-director`)」に従い、Plan(6a)を新設して `open` にした。Build(6b)は 6a の結果を待つ。Verify(7)は成果物がないため始めない(Handoff 14 の要請どおり、Verify の Handoff は組まない)。
- 6 の後のエスカレーション確認: 仕様の曖昧さや矛盾は報告されておらず(`game-designer` へ戻す理由はない)、D-001〜D-006 のどれも変更を要しない。コンセプト・柱・Decision の変更はなく、新ボタンもない。現時点では Owner のエスカレーションの条件に当たらない。ただし 6a で `technical-director` が「模擬環境では D-004 の前提を確かめる手段がなく、Build を成立させるには Owner の判断(リポジトリの提供、またはスコープ・リスクの受け入れ)が要る」と結論した場合は、スコープ・リスクの大幅な変化に当たりうるため、`technical-director` が `prepare-owner-escalation` で Escalation を作る。Handoff 15 の Expected output にそう書いた。
- Handoff 14 の Open questions 2(要素 9)と 3(必須視覚要素 1〜6 が既存の仕組みで実現できるか)は技術方針に関わるため、6a の Handoff 15 に含めた。Handoff 14 は編集していない(受け手は Studio で、Load は Studio の routing のため)。Sender assessment は Handoff 15 に転記せず、客観的な事実(報告された `sim/repo-notes.md` の内容、確認できなかった項目)だけを Findings に抜き出した。無敵フラグの共有構造は欠陥 D の原因候補だが、確定していない仮説なので「`sim/repo-notes.md` に書かれた事実」としてのみ渡し、欠陥 D の原因とは結び付けていない。`technical-director` は `qa` ではないため、事実の伝達は問題ない。
- 2b の `qa` Handoff と `game-designer` の §10 追記 Handoff は、今回も作っていない(この操作で書けるのは seq 15 の 1 つで、Build の再開の前提である 6a を優先した)。どちらも 6a と独立で、残っている。
- 6a(Plan)の後: Handoff 16(D-007)は `outcome: done`。`technical-director` は D-004 の方針を保ち、T0 を「前提の台帳」(7 項目。各項目に置く前提・確認する場所・崩れたときの戻し先)に置き換え、接触結果の通知(視覚仕様の要素 9)を D-004 の口に足し、読めるコードが全くない場合は再試行せず返す条件(D-007 の 7)を定めた。仕様・方向の変更は不要で、`game-designer`・`game-director` に回す事項はない。D-001〜D-006 は変わらず、新ボタンもない。Owner の Escalation は `technical-director` が「今回は作らない」と判断した(作業が戻しやすい、D-004 の骨格は `sim/repo-notes.md` で確認済み、方針が変わりうる未確認項目は 2 点で実装の入口で見える)。Studio も、Escalation の条件に今は当たらないと確認した。6a を `done`、6b を `open` にした。
- 6a の後に残るリスク: Build が書き換えられるコード自体がない場合、計画は空になる。Handoff 17 の Expected output で、最初にコードを読み書きできるかを報告させ、できない場合は再試行せず `outcome: question` で返す(D-007 の 7)。その結果を受けた次の Route で、Escalation が要るかを `technical-director` に判断させる。Studio は先回りして Escalation を書かない。
- Handoff 17 の作り方(Route 手順 4–5): 受け手 `gameplay-engineer` の Works from に合わせ、Handoff 16 の Findings から台帳、共通手順、接触結果の通知、視覚要素の段階、並列化、無敵の問い合わせ関数、テスト戦略、打ち切りの条件を客観的な内容として抜き出した。Handoff 16 の Sender assessment は渡していない。Previous handoff は none。無敵のタイマーについては、触れない・フラグを共有しているという事実と V3、V4 の測定条件のみを渡し、欠陥 D の原因とは結び付けていない。
- Handoff 17 の Expected output に、Verify で `qa` と `art-director` を並列にするため `to: studio` を指定した(Build の Sender assessment は `qa` に渡さない)。縮小案を使った場合は、Studio が `art-director` に受け入れ基準(A6、A7 など)の読み替えを確認する必要がある。
- 6b(Build 再開)の後: Handoff 18 は `outcome: question`。最初の確認の結果、実行環境にゲームのコード・ビルド・テスト手段・リポジトリがなく、変更を加える経路もなかった。台帳 7 項目はすべて未確認で、実装・テスト・ビルドノートはなく、`qa` / `art-director` に渡せる成果物もない。D-007 の 7 に該当するため、Build は再試行しない。Studio は、Build を同じ入力で再び開始しない(結果が変わらないため)。仕様の曖昧さや矛盾は報告されておらず、`game-designer` に回すものはない。D-001〜D-007 の変更も要しない。
- 6b の後の route 改訂: 6a で `technical-director` は「今回は Escalation を作らない」と判断したが、その前提(コードにアクセスできる可能性)は崩れた。リポジトリの提供、または Build の範囲を模擬に合わせて縮めることは、スコープ・費用・リスクが Goal の想定から大きく変わりうる(Escalation の条件)。ただし、要否と選択肢の設計は技術リスクの判断であり、`technical-director` の権限(Escalation の準備は `prepare-owner-escalation`)にあるため、Studio は先回りして Escalation を書かず、Plan(6c)を新設して `open` にした(Handoff 19)。Verify(7)は成果物がないため始めない。Play(8)と Review(9)は 6c の結果に依存するため `planned` のまま、範囲が変わりうると注記した。
- Handoff 19 の作り方(Route 手順 4–5): 受け手 `technical-director` の Works from(技術的な問題、制約、リポジトリの所在、関連 Decision)に合わせ、Handoff 18 の Findings(確認できたこと・できなかったこと、選択肢 (a)(b)、再開順序)を客観的な事実として抜き出した。Handoff 18 の Sender assessment は転記していない。Previous handoff として Handoff 18 を Load に入れた(`technical-director` に Sender assessment を除外する方針はない)。Handoff 18 は編集していない(受け手は Studio で、Load は Studio の routing のため)。Handoff 19 の Expected output は、Owner の判断が要る場合は Escalation(seq 20、`to: owner`)、不要な場合は `to: studio` の Handoff とした。
- 6c(Plan)の後: Escalation 20 で、`technical-director` は Owner の判断が要ると結論し、選択肢 A(実際のリポジトリとビルド・テスト手段の提供)、B(Build の範囲を実装計画と受け入れ基準の確定までに縮小)、C(模擬ビルドで工程を予行)と推奨(B。ただし実コードがあり実機で確かめたいなら A)を示した。Studio も、スコープ・費用・リスクが Goal の想定から大きく変わることを確認し、エスカレーションの条件に当たると判断した。6c を `done` にし、6d(Owner)を `open`、Goal を `blocked-on-owner` にした。
- Resume(Owner の回答、2026-10-10): Owner は Escalation 20 に Option C で回答し、条件を付けた(`sim/repo-notes.md` をコードとして扱う、Build は変更内容を Handoff に正確に書いた時点で完了、模擬ビルドはランタイムのシミュレーターが変更内容から作る、結果に模擬であることを明記し Goal の判定は模擬ビルドに基づく)。Studio は D-008(`decided_by: owner`)に Owner の言葉を含めて記録し、Escalation 20 を `resolved`(`decision: D-008`)にして、Goal を `active` に戻した。6d を `done` にした。
- Resume の route 再計画: Escalation の Option C の "If chosen" は「Owner が模擬ビルドの記述を提供した時点で Verify から再開、Goal は達成扱いにしない」だった。Owner の回答は、それとは異なる点が 3 つある。(1) 模擬ビルドを作るのは Owner ではなくランタイムのシミュレーターで、その元は Build の変更内容である。(2) `sim/repo-notes.md` をコードとして扱うため、Build(`gameplay-engineer`)は変更内容を書く工程として残る。(3) Goal の判定は模擬ビルドに基づいて行う。そのため、選択肢の記述どおりには進めず、Owner の言葉を優先して残りの route を再計画した(Resume 手順 3、選択肢に記述のない回答)。変更点は次のとおり。Build(6e)を新設して `open` にし、Handoff 21 を作った。Verify(7)、Play(8)、Review(9)は模擬ビルドを対象にし、Review は模擬ビルドに基づく判定にする。Goal を達成扱いにしない、という Escalation の記述は Owner の条件で置き換わった。ただし、結果には模擬であることを明記し、実機で確認できない点(H1〜H4)を Outcome に書く。
- 再計画での Escalation 確認: Owner の回答は D-001〜D-007、ビジョンの柱、入力ボタンに触れない。新しい Escalation の条件には当たらない。シミュレーターは Role ではないため、route の行には置かない。模擬ビルドの作成は 6e と 7 の間のランタイムの動作で、Next action に記す。
- D-007 の 7 の扱い: コードを読めない入力の欠落は、`sim/repo-notes.md` を Load に入れたことで解消した。Handoff 21 で、台帳 7 項目は `sim/repo-notes.md` に照らして確認し、答えがない項目は「模擬上の前提」と明記するよう指示した。実コードで確認済みと書かせない。
- Handoff 21 の作り方(Route 手順 4–5): 受け手 `gameplay-engineer` の Works from(承認済みの仕様、計画、制約、リポジトリ)に合わせ、仕様と計画は Load で渡した。Previous handoff は Studio が書いた Handoff 17(Sender assessment がない)にした。Handoff 18 は Sender assessment を含むため Load に入れず、必要な事実は Handoff 21 に転記した。Expected output は `to: studio` として、Verify の `qa` と `art-director` への Handoff を Studio が組み直せるようにした。欠陥 D の原因の推測は書かせない。
- 2b の `qa` Handoff と `game-designer` の §10 追記 Handoff は、今回も作っていない(この操作で書けるのは seq 21 の 1 つ。どちらも Owner の回答に依存せず、Build とも独立で、残っている)。2b は Owner の報告の原文が入力にない限り作れない。§10 の追記は Verify の前までに済ませる。
- 6e(Build)の後: Handoff 22 は `outcome: question`。台帳 7 項目を `sim/repo-notes.md` に照らして確認し(1〜5 と 7 の一部は「模擬上の前提」と明記)、変更内容は 2.1〜2.4 に完全に書かれた。ただし波 2 以降の条件(K / T)をいつから調べ始めるか、出現位置の待ちの敵を「生きている敵」に数えるか、が仕様 §4.1 に未定義で、文面どおりだと部屋 2 の波 2 が即座に出うる(V7 に影響)。戻りルール「Build: 仕様の欠落 → Design(`game-designer`)、その後 Build に戻る」に従い、Design(6f)を新設して `open` にした。エンジニアは決めない(Skill どおり)。6e を `done` にした。
- 6e の後のエスカレーション確認: 欠落は波の出現条件の細部で、D-001〜D-008、ビジョンの柱、スコープ、入力ボタンのどれにも触れない。`game-designer` の権限(規則、ルールの細部)内の決定で、Owner エスカレーションの条件に当たらない。`game-director` に回す必要もない。ただし `game-designer` の答えが D-002・D-003 の変更やスコープの変更を要する場合は、`question` で返して Decide(`game-director`)に回す(Handoff 23 に書いた)。
- 6f の Handoff(23)の作り方(Route 手順 4–5): 受け手 `game-designer` の Works from(仕様の質問、Decision、設計文書)に合わせ、Handoff 22 の Findings の「5. 仕様の欠落」から、欠落の事実、部屋ごとの K・T、選択肢 A / B / C と技術的な費用だけを抜き出した。Handoff 22 の Sender assessment(確信度、疑い 1〜3)は渡していない。`gameplay-engineer` が提案した既定 A は、選択肢の説明として「提案されている」とだけ事実を伝え、決定は `game-designer` に委ねた。Previous handoff は none(Handoff 22 が Sender assessment を含み、大部分が受け手に不要なため)。Handoff 22 は編集していない(受け手は Studio で、Load は Studio の routing のため)。
- 小さな追記の統合: 以前から残っていた「`design/combat.md` §10 に視覚仕様への参照を追記する」作業は、書き込めるのが `game-designer` で、6f と同じファイルを触るため、Handoff 23 に含めた。Verify の前までに済ませる条件はこれで満たされる。
- 6f の後: 規則の決定は Decision(D-009 を `game-designer` が記録する想定)にする。6g で Studio が `gameplay-engineer` への小さな Handoff を組み、2.1 に 1 文だけ足して Build の記述を確定させ、`to: studio` で返す。その後、シミュレーターが模擬ビルドを作り、Verify(7)を組む。
- 2b の `qa` Handoff は、今回も作っていない(Owner の報告の原文が入力にない。この操作で書けるのは seq 23 の 1 つで、Build の確定に必要な 6f を優先した)。Verify の前にある必要はないが、結果が欠陥修正を要するなら Build の再開が必要になるため、できるだけ早く処理する。
- 6f(Design)の後: Handoff 24(D-009)は `outcome: done`。`game-designer` は案 A(前の波の全員が出現中に入った時点から K・T を調べ始め、待ちの敵は生きている敵に数えない)を決め、`design/combat.md` の §4.1、§4.3 の注、V7、V12(新規)、§6.2、§8、§9 を更新し、§10 に視覚仕様への参照を追記した。数値・入力・プレイヤー側の値は変えていない。D-001〜D-003 の変更もスコープの変更もなく、`game-director` に回す必要はない。エスカレーションの条件(コンセプト・柱・Decision の変更、スコープ・費用・リスクの大幅な変化、Owner の好みが基準、不可逆、Goal の再解釈)のどれにも当たらない。6f を `done` にし、計画どおり 6g を `open` にした(Handoff 25)。§10 の参照追記は済んだので、Verify の前の条件は満たされた。
- Handoff 25 の作り方(Route 手順 4–5): 受け手 `gameplay-engineer` の Works from(承認済みの仕様、計画、制約、リポジトリ)に合わせ、Handoff 24 の Findings から規則と足す 1 文、足りない部分の確認点を客観的に転記した。Handoff 24 には Sender assessment がなく、Previous handoff として Load に入れた。Handoff 22 の Sender assessment は転記していない。Handoff 24 は編集していない(受け手は Studio で、Load は Studio の routing のため)。Expected output は `to: studio` とし、Verify の `qa` と `art-director` への Handoff を Studio が組み直せるよう、確定した変更内容の全体を Findings に自己完結で書かせ、自己評価は Sender assessment にだけ書かせる。模擬上の前提が残る項目も一覧させる。
- Verify(7)の Handoff を作るときの条件(Route 手順 4–5 のため記録): `qa` には受け入れ基準(V7、V12 を含む)と模擬ビルドの動かし方のみを渡し、Build の Sender assessment は渡さない。`art-director` には視覚仕様と模擬ビルドを渡す。Playtester(8)には模擬ビルドとプレイヤー像のみで、仕様の数値や体験の観点(§6.2、視覚仕様 §10.2)は書かない。
- 2b の `qa` Handoff は、今回も作っていない(Owner の報告の原文が入力にない。この操作で書けるのは seq 25 の 1 つ)。独立で、残っている。
- 6g(Build)の後: Handoff 26 は `outcome: question`。止まった原因は入力の欠落だけである。Handoff 25 の Load に Handoff 22(変更内容の記述 2.1〜2.4)が入っておらず、`gameplay-engineer` は記述の全体を推測せずに返した。これは Studio の Load の漏れで、仕様の曖昧さや矛盾は報告されていない(`game-designer` に回すものはない)。D-001〜D-009、ビジョンの柱、スコープ、入力ボタンのどれにも触れず、エスカレーションの条件に当たらない。`game-director` に回す必要もない。Handoff 26 の選択肢 (a)(Handoff 22 などを Load に入れて同じ Step をやり直す)を採った。選択肢 (b)(Handoff 22 抜きで書き直す)は、記述の食い違いを保証できないため採らない。6g を `done` にし、6h を `open` にした(Handoff 27)。ループ制限には当たらない(初めての欠落で、受け入れ基準の失敗でもない)。ただし Handoff 27 でも必須ファイルが読めない場合は、再試行せず返すよう指示した。その場合は次の Route で、パケットの組み方そのものを見直す。
- Handoff 27 の作り方(Route 手順 4–5): 受け手 `gameplay-engineer` の Works from(承認済みの仕様、計画、制約、リポジトリ)に合わせて組んだ。Load に Handoff 22(記述の元)、Handoff 17(台帳。Handoff 16 は `technical-director` の Sender assessment を含むため使わない)、設計書 2 点、`sim/repo-notes.md`、D-004〜D-009 を加えた。Previous handoff は Handoff 26 にした(`gameplay-engineer` 自身が書いたもので、Sender assessment を除外する方針は `gameplay-engineer` にない)。Handoff 22 の内容は、この操作の入力になかったため要約せず、Load での指定に留めた。Handoff 26 の Findings 2〜4 は「下書き」として渡し、Handoff 22 と台帳に照らして確認させ、食い違いは Handoff 22 側を正とするよう書いた。Handoff 26 は編集していない(`to: studio` で、Load は Studio の routing のため)。
- Handoff 26 が V12(b) について指摘した帰結(待ちの間に R の Grub を倒していたら、波 2 はすぐ出る)は、Verify の Handoff を組むときに期待値として渡す必要がある。Handoff 27 に記録した。
- 2b の `qa` Handoff は、今回も作っていない(Owner の報告の原文が入力にない。この操作で書けるのは seq 27 の 1 つ)。独立で、残っている。

## Next action

Goal は `active`。6h(Build の確定のやり直し、`gameplay-engineer`)が `open`。Handoff: `goals/G-001-combat-monotony/27-studio-to-gameplay-engineer.md`。

1. `gameplay-engineer` が Handoff 27 に従い、Handoff 22 の 2.1〜2.4 に D-009 の規則の 1 文を足し、確定した変更内容の全体を Findings に自己完結で書いて、Handoff 28(`to: studio`)として返す。曖昧さや不足、必須ファイルが読めない場合は `outcome: question`。
2. その後、ランタイムのシミュレーターが変更内容から模擬ビルドを作る(Studio は模擬ビルドを書かない)。Studio が Route を行い、Verify(7)の Handoff を `qa` と `art-director` 向けに、Sender assessment を除いて新しく組む(V7 と V12 を含める。V12(b) の「すぐ出る」場合の期待値も含める)。
3. 独立: 2b(`qa`、`reproduce-defect`)の Handoff。Owner の報告の原文と設計文書のみを渡す。原文が入力にない場合は作れない。

Owner への報告(日本語):
- Build の記述の確定が、入力の渡し漏れ(Studio 側の Load の漏れ)で一度止まりました。仕様や方向の問題ではなく、Owner の判断は不要です。漏れていたファイルを加えて、`gameplay-engineer` にやり直しを依頼しました。
- その後、模擬ビルドを作って Verify、Play、Review に進みます。判定には「模擬ビルドに基づく」と明記します。ゲームパッドの操作感、0.7 秒の予告で足りるか、暗い床での読み取りやすさ(H1〜H4)は、実機では確認できないままです。
- 欠陥 D の再現には、Owner の元の報告文が必要です。

## Outcome

(未完了)
>>>END

<<<FILE goals/G-001-combat-monotony/28-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-001
seq: 28
from: gameplay-engineer
to: studio
stage: Build
outcome: done
---
# 28: gameplay-engineer → studio — Build の変更内容の記述を確定した(Handoff 22 の 2.1〜2.4 に D-009 を統合。自己完結)

## Task

Handoff 22 の変更内容の記述(2.1〜2.4)に D-009 の規則を 2.1 の 1 文として足し、確定した全体を、Handoff 22 を読まなくても分かる形で書く。あわせて、模擬上の前提が残る台帳の項目を Handoff 17 の番号で挙げる。

## Context

G-001(戦闘の単調さ)。D-008 により、Build は変更内容を正確に書いた時点で完了する。実コードの変更、ビルド、テスト、動作確認は行っていない。以後の Verify・Play・Review は、この記述からシミュレーターが作る模擬ビルドに基づく。

Handoff 22 は、波 2 以降の条件を調べ始める時点が仕様にないとして `question` で返した。これは D-009(`design/combat.md` §4.1、V7、V12)で決定済みである。今回は 2.1 のスポナーの動きに D-009 の 1 文を足し、Handoff 22 の他の内容は変えていない。

Handoff 22 と D-009 の食い違いの確認結果は、Open questions に書く。

## Findings

### A. 確定した変更内容

共通ルール: 長さは秒、距離はタイル、速度はタイル/秒。状態のタイマーはゲーム内の経過時間(delta)で進める。delta は 1 更新あたり 0.05 s を上限にする(ポーズ復帰の最初の更新も同じ)。状態が切り替わるときは余りを次の状態に持ち越す。ポーズ中は全部のタイマーと見た目の変化が止まる。数値は仕様の暫定値(P)のまま、変えていない。

#### 2.1 部屋とスポナー

**部屋データ**: 部屋ごとに、波(スポーン一覧 = 敵の種類とスロット)、次の波の条件(K、T)、Grub 速度、Spitter の撃つ間隔、突進スイッチを持つ。出現中(0.8 s)、Spitter の最初の 1 発(出現中の終了から 1.0 s)、出現位置の待ち(プレイヤーがスロットから 4 タイル未満なら最大 2.0 s)は全部屋共通の定数にする。スロットは Door、Far、L、R、FL、FR の 6 つで、座標は部屋データで与える。

**部屋の構成**(「突進型」= `grub_charger`):

| 部屋 | 波 | 構成(スロット) | 次の波の条件 | Grub 速度 | Spitter 間隔 | 突進スイッチ |
|---|---|---|---|---|---|---|
| 1 | 1 | 通常 Grub × 2(L, R) | | 2.0 | – | オフ |
| | 2 | 通常 Grub × 1(Far) | K=1, T=10 s | | | |
| 2 | 1 | 突進型 Grub × 1(Far) | | 2.0 | – | オン |
| | 2 | 通常 Grub × 2(L, R) + 突進型 Grub × 1(Far) | K=0, T=15 s | | | |
| 3 | 1 | Spitter × 1(Far)+ 通常 Grub × 1(L) | | 2.2 | 2.0 s | オフ |
| | 2 | Spitter × 1(FL / FR のうち遠い方)+ 通常 Grub × 1(R) | K=1, T=12 s | | | |
| 4 | 1 | Spitter × 1(FL)+ 突進型 × 1(Far)+ 通常 Grub × 1(L) | | 2.2 | 1.8 s | オン |
| | 2 | Spitter × 1(FR)+ 突進型 × 1(R) | K=1, T=12 s | | | |
| 5 | 1 | Spitter × 1(Far)+ 通常 Grub × 2(L, R) | | 2.4 | 1.6 s | オン |
| | 2 | Spitter × 1(FL / FR のうち遠い方)+ 突進型 × 2(L, R) | K=1, T=12 s | | | |

表の読み方: 波 2 の行の K と T は、その波 2 を出す条件である。波 1 の全員が出現中に入った時点から調べる(下の「波の条件を調べ始める時点」)。

合計は 部屋 1: 3 体、2: 4 体、3: 4 体、4: 5 体、5: 6 体。同時に存在する敵の最大は 部屋 1: 2、2: 3、3: 3、4: 3、5: 4。部屋は、全部の波が出現し、全部の敵が倒れたときに終わる(既存の終了条件はそのまま使う)。

**スポナーの動き**:
- 波 1 は部屋の開始時に出す(各スロットの出現位置の待ちは次項)。
- 波 2 以降は、「生きている敵が K 体以下」または「前の波の最後の敵の出現中が終わってから T s」の先に起きた方で出す。「生きている敵」には出現中の敵を含める。T の起点は、その波の最後の敵の出現中が終わった時点(出現位置の待ちがあれば、待ちが終わって出現中も終わった時点)である。
- **波の条件を調べ始める時点(D-009。今回足した 1 文)**: 波 N の次の波(N+1)の K と T は、波 N の全員が出現中に入った時点から調べ始める。それより前は、K の判定も T の計測もしない。そのため、出現位置の待ちに入っている敵は「生きている敵」に数えず、出現中に入った時点から数える。
  - 全員が出現中に入った時点で、生きている敵が K 体以下ならすぐ次の波を出す。そうでなければ、K 体以下になるか T s たつかの先に起きた方で出す。T の起点は上のとおりで変わらない。
  - 待ちの敵がいない波では、出現を決めた時点が、そのまま調べ始める時点になる(従来どおり)。
- **出現位置の待ち**: スロットごとに、出現の時点でプレイヤーとスロット座標の距離(中心間)が 4 タイル未満なら待つ。距離が 4 タイル以上になるか、待ちが 2.0 s に達したら、そのスロットの敵が出現中に入る。待ちはスロットごとに別々で、同じ波の待ちは、波の出現を決めた時点から同時に始まる。いったん待ちが終わったスロットは、プレイヤーが戻ってきても待ち直さない(`design/combat.md` §4.1 の既存の文面。追加の規則ではない)。プレイヤーがスロットに重なっていても押し出さない。
- **「FL / FR のうち遠い方」**: その波の出現を決める時点(待ちを始める前)のプレイヤー位置から FL と FR の座標への距離を比べ、遠い方を選ぶ。同じ距離なら FL。待ちの間にプレイヤーが動いても選び直さない。同じ波で FL か FR が別の敵に固定されている場合は、この規則の対象外。
- **突進スイッチ**: スポナーが敵を生成する 1 か所で、スイッチがオフなら `grub_charger` を `grub`(通常型)に置き換える。敵の数、波、スロット、K/T は変わらない。スイッチがオフでも、尾根の重ね絵など突進の見た目は何も付かない。部屋 1、3 には突進型がいないので、スイッチは効かない。

#### 2.2 敵コントローラ(共通)

**出現中(Spawning)**: 全種類の敵に追加する。長さ 0.8 s。この間は、動かない、行動しない、ダメージを与えない、プレイヤーの攻撃のダメージも怯みも受けない。終わると通常の状態(Chase)に入る。Spitter の最初の 1 発は出現中の終了から 1.0 s 後。以降は部屋ごとの間隔。

**Spitter の弾**: 速度 4.0 タイル/s、ダメージ 1 ハート。撃った瞬間のプレイヤーの位置へ直進(先読みなし)。壁で消え、敵の体を通り抜けて敵にダメージを与えない。弾の仕組みは作り直さない。Spitter 自身の怯みは既存のまま(0.2 s)。

**`grub_charger`(突進型)**: Grub のデータ(HP 2、速度は部屋の Grub 速度)に突進の数値を足したもの。別のコントローラは作らない。状態は Spawning、Chase(既存)、Windup、Charge、Recovery。通常型 Grub と同じ Chase、噛みつき、怯みの既存のルーチンを使う。

| 状態 | 長さ | 動き | 接触ダメージ | 怯み・ノックバック |
|---|---|---|---|---|
| Chase | 条件まで | 既存どおりに歩く | あり(既存の噛みつき、1 ハート) | 既存(0.2 s) |
| Windup | 0.7 s | その場で停止、歩行アニメーションも止める | なし | なし |
| Charge | 7.0 タイル進むか壁まで | 固定した方向へ 8.0 タイル/s で直進 | 突進ごとに 1 回まで(下記) | なし |
| Recovery | 0.8 s | その場で停止 | なし | なし |

**Chase → Windup の条件**(Chase の各更新で調べる。すべて満たすとき):
1. 出現中が終わってから 1.5 s 以上たっている。前回の Recovery が終わってから 2.5 s 以上たっている(まだ Recovery がなければ後者は満たすとみなす)。
2. プレイヤーとの距離(中心間)が 3.0〜6.0 タイル。
3. この Grub が `grub_charger` である(スイッチがオフなら生成されない)。
4. 生きている他の `grub_charger` が Windup または Charge にいない。Windup に入る瞬間に、生きている敵を調べて導く。保存する状態(トークン)は作らない。

Chase 中の怯みでこれらのタイマーは巻き戻さない(起点は出現中の終了と前回の Recovery の終了で、怯みは影響しない)。

**Windup**: 入る瞬間のプレイヤーの中心へ向かう単位ベクトルを突進方向として固定する(距離が 3.0 タイル以上なので零ベクトルにならない)。その後プレイヤーが動いても変えない。0.7 s たつと Charge に入る(余りは持ち越す)。

**Charge**: 毎更新 8.0 × delta の距離を固定方向へ進む。通算 7.0 タイルに達するか、既存の移動処理が壁で止めたら終わり、すぐ Recovery に入る(壁に当たったときの特別な処理はない)。7.0 タイルを超えた分は、時間に直して(超過距離 ÷ 8.0)Recovery の経過時間に持ち越す。他の敵の体は通り抜け、ダメージを与えない。

**Recovery**: 0.8 s たつと Chase に戻る。

**接触の解決(1 つの関数)**:
- Charge 中の接触だけを扱う。Chase 中の噛みつきは含めない(既存のまま)。
- 毎更新、Grub とプレイヤーの相対運動をスイープで調べ、突進ごとに最初に体が重なった更新を接触の瞬間とする。Charge に入った時点ですでに重なっていれば、Charge の最初の更新を接触の瞬間とする。Windup と Recovery の間の重なりは数えない。
- 接触の瞬間に、プレイヤーの無敵を問い合わせ関数で読む(1 つの真偽。署名は変えない。その更新で見えているフラグの値を使う)。
  - 無敵なら: ダメージなし。結果を「抜けた」にする。Grub は通り抜けて走り続ける。
  - 無敵でなければ: 既存のダメージ処理で 1 ハートを 1 回だけ与える。結果を「被弾」にする。被弾後の硬直と無敵は既存の処理に任せる。
- 結果が決まったあと、その突進は、重なりが続いても、無敵が切れても、もうダメージを与えない。次の突進では、また最初の重なりから数える。
- 無敵のタイマーのコードには触れない。問い合わせ関数もフラグを読むだけで、意味づけは足さない。
- 接触結果(未解決 / 抜けた / 被弾)を Grub ごとの値として保持する。Windup と Charge の開始時に未解決へ戻す。見た目側は Charge の間だけこれを読む。

**ダメージを受けたとき**(Grub、Spitter 共通のルーチンへの変更):
- Spawning の敵には、プレイヤーの攻撃の判定が当たらない(ダメージも怯みもない)。
- `grub_charger` が Windup、Charge、Recovery の間に攻撃を受けたら、HP だけ減らす。Flinch への遷移も、ノックバックも、状態、方向、残り時間の変更もしない。ノックバックが既存にある場合も、この 3 状態の間は受けない。
- それ以外の状態や敵(Chase の突進型、通常型 Grub、Spitter)は、既存の 0.2 s の Flinch のまま。
- どの状態でも HP が 0 になれば、その時点で倒れる。Windup、Charge 中に倒れたら、同時予告の枠は(導出なので)自動的に空く。レーンと点灯は 0.1 s 以内に消す。

**時間と FPS**: 新しい状態のタイマーはすべて delta で進める。見た目の変化は、状態の経過割合(経過 s ÷ 状態の長さ)から求める。30 FPS と 60 FPS で状態の長さの差は 30 FPS の 1 フレーム(約 0.034 s)以内に収まる。接触は更新ごとのスイープなので、FPS で有無が変わらない。

#### 2.3 見た目(段階 0。縮小案は使わない)

色は暫定値(P)。見た目の変形は描画だけに適用し、判定の大きさと位置は変えない。点滅は 1 秒に 3 回以下(単発のフラッシュは可)。

**突進型の目印(常時)**: 通常型と同じスプライトに、背中の熾火の尾根(消灯時 #6B2A1A)を重ねる。出現中から常に見え、Spawning の間は点灯しない。通常型には付けない。

**Spawning(全種類)**: 不透明度を 40% から 100% へ、経過割合に対して線形に上げる。足元に淡い青の輪(#8FB8E8)。赤橙は使わない。

**Windup**(経過割合 p = 経過 s ÷ 0.7):
- 最初の描画で、Grub の中心から固定した方向へ、地面にレーンを出す。長さは 7.0 タイルか壁の手前の短い方(Windup の開始時に、Charge と同じ移動の衝突判定で求める)。幅は敵の接触判定の幅(既存の 1 つの値)と ±0.1 タイル以内で一致させ、実際の判定より広く描かない。
- レーンの描き方: 赤橙(#FF5A1F)の半透明の塗り、明るい縁取り(幅 0.06 タイル)、その外側の暗い下線(幅 0.03 タイル)、1 タイルおきの突進方向のシェブロン(Windup 中は動かさない)。地面の上、キャラクターと弾の下の層で、自己発光(ランタンの明暗の影響を受けない)。Spitter の弾、出現中の表示、他の敵はレーンの上に描く。
- レーンの不透明度: 35% から 100% へ p に対して線形。
- 体: 高さを 100% から 80% へ ease-in、幅を 100% から 108% へ(p に対して)。突進方向と逆に最大 0.15 タイル、スプライトを引く。歩行アニメーションは止める。
- 尾根の点灯: 待機色から赤橙へ p に対して線形。最後の 0.1 s は核色(#FFE3B0)寄りにする。目も赤橙に光る。

**Charge**:
- 体を進行方向に 130%、横に 80% へ伸ばす。核色の芯と赤橙の縁。
- 入る瞬間に 1 回だけ、レーンを 100% 超(核色寄り)の明るさでフラッシュさせる。
- 残像は 0.5 タイル進むごとに 1 つ置き、0.2 s かけて消す(距離で置く)。足元に土煙。
- レーンは 100% に保ち、Grub が通過した後ろ側から消す。前方は残す。Charge の終わりで 0.1 s かけて全部消す。
- 使用済み表示: 接触結果が「抜けた」または「被弾」になったら、芯の明るさを赤橙の暗い側へ落とす。Charge は続く。

**Recovery**: 尾根を 0.1 s で待機色へ戻し、目の光も消す。体全体に沈んだ色(通常色に乗算 #7C8AA0 + 彩度 −40%)を乗せ、高さ 90% に沈める。不透明で、青い輪はない。足元から薄い蒸気を 0.3 s ごとに 1 つ上げる。最後の 0.2 s で高さと色を通常に戻す。

**被弾(Grub が攻撃を受けたとき。突進型のどの状態でも)**: 白いフラッシュ(#FFFFFF、0.1 s、時間で減衰)と小さな火花を当たった位置に出す。位置、向き、大きさ、レーン、点灯は変えない。HP 1 の間、突進型の体に小さな傷の重ね絵を出す(既存の敵の HP 表示はない前提)。

**抜けた合図**: 接触結果が「抜けた」になった更新で、プレイヤーの位置に淡い白青(#CFE8FF)の細い輪を 0.15 s 出す。「被弾」のときは出さず、既存の被弾表現だけを使う。

**音**: 実装しない。粒子(残像、土煙、蒸気、火花)は新規の 1 種を足す。

#### 2.4 開発用補助(開発ビルド限定。リリースビルドには含めない。プレイヤー向けの入力は足さない)

- 部屋の選択(1〜5)。
- 部屋ごとの突進スイッチのオン/オフの切り替え。
- 30 FPS と 60 FPS の切り替え。
- 状態の遷移ログ: 時刻(ゲーム内の経過時間)、敵の ID と種類、遷移前後の状態、突進方向、接触結果(未解決 / 抜けた / 被弾)、波の出現(波番号、スロット、「遠い方」の選択結果)、Windup の開始時のプレイヤーとの距離。D-009 に合わせて、「波 N の全員が出現中に入った時点(K と T の調べ始め)」もログに出す。

### B. 受け入れ基準 V7、V12 の追跡(記述の上でのみ。満たしたとは書かない)

- V12(a) 部屋 2: Far の突進型が待つ間は、全員が出現中に入っていないので、K=0 の判定も T の計測も始まらない。波 2 は出ない。出現中に入った時点で調べが始まり、生きている敵は 1 体で K=0 より多い。突進型を倒す(出現中の 0.8 s はダメージを受けないので、倒せるのは出現中が終わってから)か、その出現中の終わりから 15 s たつかの先に起きた方で、波 2 が出る。
- V12(b) 部屋 1: L だけ待つ場合、R の Grub は先に出現中に入る。L が出現中に入るまで調べは始まらない。入った時点で 2 体(倒していない場合)なら K=1 より多く、1 体倒すか、最後の敵の出現中の終わりから 10 s たつかの先に起きた方で、波 2 が出る。**待ちの間に R の Grub を倒していた場合は、L が出現中に入った時点で生きている敵が 1 体(K=1 以下)になり、波 2 がすぐ出る。** Verify はこの場合の期待値を「すぐ出る」と読む。
- V12(c): 待ちの間にプレイヤーが 4 タイル以上離れると、その時点で敵が出現中に入る。同じ波で複数のスロットが待つ場合は、全員が出現中に入るまで調べは始まらない。
- V12(d): 待ちのない波は、出現を決めた時点が調べ始める時点。従来どおり。
- V7: 「生きている敵」(出現中を含み、待ちの敵を含まない)、T の起点(最後の敵の出現中の終わり)、調べ始める時点が、2.1 と矛盾しない。「遠い方」の選択は出現を決める時点で固定し、この規則は触れない。

### C. 他の受け入れ基準との対応(どの変更で満たす想定か)

V1〜V6、V8〜V11、A1〜A13 の対応は Handoff 22 の対応表のとおりで、変更はない。要点: 予告は Windup の完了後にしか Charge に入れない(V1)。接触は最初の重なり 1 回(V3、V4)。同時 1 体は導出(V5)。スイッチはスポナーの 1 か所(V6)。怯みは 2.2 の「ダメージを受けたとき」(V11)。レーンの幅、向き、不透明度は 2.3(A1〜A4)。未確認の A5(暗い床での明るさの比)と A10(5 つの見た目の区別)は、模擬ビルドで確かめる。

### D. 模擬上の前提が残る台帳の項目(Handoff 17 の項目番号)

凡例: **模擬上の前提** = `sim/repo-notes.md` が答えず、前提として置いたもの。実コードで確認済みではない。`sim/repo-notes.md` にはスポナー、部屋、波、出現位置、出現中の記述がない。

| # | 項目 | 結果 | 前提の内容 |
|---|---|---|---|
| 1 | 部屋データ、スポナー、波 | 模擬上の前提 | 部屋データは敵の一覧、スロット座標、終了条件を持つ。波はなく最初に全部出す作りで、スポナーに波の予定(スポーン一覧と K/T)を足せる。終了条件は広く参照されていない。D-009 の規則も、この前提の中で持つ。具体的には、(a) 敵の一覧で「生きている敵」を数える(出現中の敵は数え、待ちの敵は数えない)、(b) スロットごとの待ちタイマー(4 タイルの距離判定、最大 2.0 s、重なりは押し出さない。delta で進み、ポーズで止まる)、(c) 波ごとの「全員が出現中に入った」判定と、K/T を調べ始める時点を 1 か所に置く(D-007 の継ぎ目)。 |
| 2 | 部屋のコードと敵コントローラの分離 | 模擬上の前提 | 結合していると仮定し、状態追加(2.2)と部屋・波(2.1)は直列で作る。波の出現と部屋の終了条件の結合の強さも、記述に答えがない。 |
| 3 | 接触の判定形状、レーン幅の元の値 | 模擬上の前提 | 敵の接触判定の大きさは 1 つの値で、形状は不明。スイープで扱い、円でなければ相対移動 0.25 タイル以下に分割する。レーン幅はその 1 つの値から取る。 |
| 4 | Spitter の弾(壁で消える、敵を通り抜ける) | 模擬上の前提 | 弾は仕様 §2.1 のとおりに動く。弾の仕組みは作り直さない。 |
| 5 | 視覚の仕組み | 模擬上の前提 | 必須要素 1〜6 は仕様どおり実現できる。縮小案(視覚仕様 §11)は使わない(段階 0)。敵の HP 表示はない前提。粒子は新規の 1 種を足す。レーンの赤橙と、Spitter の弾・ランタンの色の近さは未確認。 |
| 7 | 敵の挙動が経過時間で進むか | 一部確認 / 一部模擬上の前提 | 確認(模擬のコード): 可変 delta、30/60 FPS、Flinch 0.2 s、無敵 0.25 s と 0.8 s の秒指定。模擬上の前提: 既存の敵の他のタイマー(噛みつきの間隔など)が delta で進んでいるか。時間ベースと仮定し、既存のコードは直さない。 |

- 項目 6(接触結果の通知)は前提ではなく、この変更で足すもの(2.2 の接触結果、D-007 の 6)。
- 項目 1〜5 と 7 の前提が外れた場合の戻し先は、Handoff 17 と D-007 の 2 のとおり(分類 (i)〜(iv))。崩れた項目は、模擬の範囲では見つかっていない。これは実コードでの確認ではない。
- 記述から確認できた事実(根拠): 敵が共通コントローラで Idle / Chase / Attack を持ち、種別ごとの挙動がデータであること。Flinch 0.2 s が Attack を含む何でも中断すること。無敵が 1 つのフラグで、2 つのタイマーがそれぞれ切ること。移動は壁で止まること。可変 delta で 30/60 FPS をサポートすること。

### E. 実装していない・確認していないこと

- コードの変更、ビルド、テストの作成と実行は行っていない(D-008)。この文書は変更内容の記述だけである。
- 実機のゲームパッドの操作感、0.7 s の予告を読んでダッシュまで入力できるか、暗い床や小さい画面での読み取り(H1〜H4)は確認していない。
- 敵の接触判定の形状と大きさ、スロット座標の実数値、プレイヤーの移動速度、攻撃の届く距離は不明のままで、決めていない。スロット座標は、各部屋で仕様の意味(奥、左右の側面、奥の左右の隅)に対応する位置にあるとして扱う。
- 欠陥 D(被弾直後のダッシュ中のダメージ)には触れておらず、原因は推測していない。V3、V4 の測定は、直前 0.8 s 以内に被弾していない状態で行う前提のまま。
- 不確定な 1 点: 2 体の突進型が同じ更新で Windup の条件を満たす場合(部屋 5 の波 2 の L と R)、どちらが先に Windup に入るかは既存の敵の更新順で決まる。仕様に規則がなく、この変更も規則を足さない。V5(同時 1 体)には影響しない。
- 音、新しい入力ボタン、Spitter の変化、新しい敵、プレイヤー側の数値やキットの変更は含めない。

## Decisions already made

- D-001〜D-006: 戦闘の方向、Grub 突進、技術方針、怯み・接触、予告の視覚。
- D-007: 前提の台帳。
- D-008: Build は記述の完了で完了。判定は模擬ビルドに基づく。
- D-009: 波の条件を調べ始める時点と、待ちの敵の扱い。

## Constraints

- すべての結果は模擬ビルドに基づく(D-008)。実機の証拠ではない。
- 規則は決めていない。仕様と数値は変えていない。新しい入力ボタンなし。
- 無敵のタイマーのコードには触れない。欠陥 D の原因は推測しない。

## Open questions

- Handoff 22 の記述と D-009 の間に、1 文の統合以外の食い違いは見つからなかった。`outcome: question` にする必要はない。確認した点:
  - Handoff 22 の 2.1 は、調べ始める時点を未決として未反映にしていた。この点は D-009 の 1 文で置き換えた。
  - Handoff 22 の待ちの記述に「いったん終わったスロットは待ち直さない」がなかった。これは `design/combat.md` §4.1 と D-009 に既にある文面なので、2.1 に写した。規則の追加ではない。
  - `design/combat.md` §4.3 の表は、K/T を波 2 の行に置いている。その注記は「その波の次の波を出す条件」とも読めるが、括弧内の「波 1 の全員が出現中に入った時点から調べる」と V12(a)(b)から、波 2 を出す条件と読むのが自然である。この記述でもそう読んだ。表の注記の言い回しが紛らわしいだけで、規則の食い違いとは見ていない。表現の整理が要るなら `game-designer` の判断。
- 上記のほかに、Studio が `game-designer` に回すべき問いはない。

## Expected output

Studio は、この Handoff の Findings A〜E を使って Verify の Handoff を組み直す。2.3 は `art-director` 向け、2.1、2.2 と対応(B、C)は `qa` 向け。`qa` には Sender assessment を渡さない。

## Sender assessment

- 確信度: 2 章の数値と状態遷移は Handoff 22 から写し、D-009 の 1 文を `design/combat.md` §4.1 に照らして統合した。規則の追跡(B)は高い。低いのは、台帳 1〜5 の模擬上の前提(実コードでの確認なし)と、見た目の細部(レーン長の求め方、使用済み表示の描き方)。レーン長を「Charge と同じ衝突判定」で求めるのは、仕様の「壁の手前で切る」の読み方の 1 つである。
- 疑い 1: 接触の瞬間の無敵を、その更新で見えているフラグで読むため、V3 の窓の端が 30 FPS で最大 1 フレームずれうる。仕様の許容に収まる想定だが、確認していない。
- 疑い 2: 台帳 5 で、必須の視覚要素がすべて使えると置いた。使えないと分かれば、縮小案または `art-director` への戻しになる。
- 疑い 3: 台帳 1 の波の持ち方(a)〜(c)は、スポナーがない記述の上での前提である。この前提が外れても、D-007 の継ぎ目が 1 か所なので影響は局所に収まる想定。
- 範囲外は広げていない。欠陥 D の原因の推測は書いていない。

## Load

- Role: studio/roles/studio.md
- Skills: none
- Project: design/combat.md、design/grub-charge-telegraph.md、sim/repo-notes.md
- Decisions: decisions/D-004-technical-approach-grub-charge-and-waves.md、decisions/D-005-flinch-contact-and-far-slot-rules.md、decisions/D-006-grub-charge-telegraph-visual.md、decisions/D-007-build-without-code-access-assumption-register.md、decisions/D-008-owner-simulated-build-judgment.md、decisions/D-009-wave-condition-start-and-waiting-enemies.md
- Previous handoff: goals/G-001-combat-monotony/27-studio-to-gameplay-engineer.md
>>>END
