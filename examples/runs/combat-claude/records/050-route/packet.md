# Studio operation packet

operation: Route
goal: G-001
step_artifact: goals/G-001-combat-monotony/42-playtester-to-studio.md
next_seq: 43

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/42-playtester-to-studio.md (in place: keep kind, goal, seq, from, to)
- goals/G-001-combat-monotony/43-studio-to-<role>.md

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
root; all other paths are relative to the Project Context directory. `file#section` names one `## `
section by its slug: the heading in lowercase with spaces as hyphens (`project.md#current-state`).
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

Status: planned | tentative | open | done | skipped. Handoff: the file name (in this goal's directory)
of the incoming Handoff that starts the step. Parallel steps: 2a, 2b. Step numbers need not
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
goals/G-001-combat-monotony/29-studio-to-qa.md
goals/G-001-combat-monotony/30-qa-to-studio.md
goals/G-001-combat-monotony/31-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/32-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/33-studio-to-qa.md
goals/G-001-combat-monotony/34-qa-to-studio.md
goals/G-001-combat-monotony/35-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/36-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/37-studio-to-qa.md
goals/G-001-combat-monotony/38-qa-to-studio.md
goals/G-001-combat-monotony/39-studio-to-art-director.md
goals/G-001-combat-monotony/40-art-director-to-studio.md
goals/G-001-combat-monotony/41-studio-to-playtester.md
goals/G-001-combat-monotony/42-playtester-to-studio.md
goals/G-001-combat-monotony/goal.md
project.md
sim/build-0.3.md
sim/build-0.4.md
sim/build-0.5.md
sim/build-0.6.md
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
| 2b | Observe(欠陥 D) | qa | reproduce-defect | planned(Escalation の答えに依存しない。Owner の報告の原文が入力にないため Handoff は未作成。後続の Studio 操作で作成。他のステップと独立。Play の前提ではない: 7e 参照) | —(次の空き seq で `NN-studio-to-qa.md`) |
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
| 6h | Build(記述の確定のやり直し。Handoff 22 を Load に加えた) | gameplay-engineer | implement-change | done(`outcome: done`。変更内容 2.1〜2.4 に D-009 の 1 文を統合し、自己完結で確定。台帳 1〜5、7 の一部は模擬上の前提として明記。仕様との食い違いなし) | [27-studio-to-gameplay-engineer.md](27-studio-to-gameplay-engineer.md)(出力: [28-gameplay-engineer-to-studio.md](28-gameplay-engineer-to-studio.md)) |
| 7a | Verify(模擬ビルド 0.4。V1〜V12) | qa | verify-change | done(`outcome: question`。fail なし。V7(Grub 速度、同距離の遠い角)と V10 は記述から確認できず pass にできない。基準外の食い違い F-1(再開始の起点)あり。すべて模擬ビルドの記述に基づく) | [29-studio-to-qa.md](29-studio-to-qa.md)(出力: [30-qa-to-studio.md](30-qa-to-studio.md)) |
| 7b | Verify(視覚。7a と並列: visual-review) | art-director | visual-review | done(`outcome: pass`。模擬ビルド 0.6 の記述に基づく。A1〜A13 に fail なし。A5 と A9・A10・A11 の一部は確認不能(実機要)または記述なし。赤橙の使い方は D-006 に反しない。新しい Decision なし。懸念 S1〜S3 は Play で確認する) | [39-studio-to-art-director.md](39-studio-to-art-director.md)(出力: [40-art-director-to-studio.md](40-art-director-to-studio.md)) |
| 7c | Build(F-1 の修正と V7・V10 の明記。変更内容 2.1〜2.4 の更新) | gameplay-engineer | implement-change | done(`outcome: done`。修正後の変更内容 2.1〜2.4 の全体を自己完結で記述。F-1 の起点は Recovery 終了と明記、Grub 速度の列挙、遠い角の同距離は FL、プレイヤー側の数値は変更なしと明記。仕様の欠落・矛盾の報告なし。欠陥 D は範囲外) | [31-studio-to-gameplay-engineer.md](31-studio-to-gameplay-engineer.md)(出力: [32-gameplay-engineer-to-studio.md](32-gameplay-engineer-to-studio.md)) |
| 7d | Verify(再検証: F-1、V7、V10、V12(c)。あわせて V1〜V12 の回帰) | qa | verify-change | done(`outcome: question`。fail なし。F-1、V10、V12(c) は解消(pass、模擬)。V1〜V12 の回帰も pass(模擬)。V7 の「同距離のとき」の規則だけ、ビルドが「front-left corner」と書き、仕様の FL(奥の左隅)を指すか確認できず pass にできない。Grub 速度などV7 の他の部分は pass。欠陥 D は範囲外で、観察として記録) | [33-studio-to-qa.md](33-studio-to-qa.md)(出力: [34-qa-to-studio.md](34-qa-to-studio.md)) |
| 7f | Build(V7 の同距離の規則の用語を FL に合わせて明記。変更内容 2.1〜2.4 の更新) | gameplay-engineer | implement-change | done(`outcome: done`。修正後の変更内容 2.1〜2.4 の全体を自己完結で記述。Handoff 32 は「FL」と書いており「front-left」の語はなかったと報告。FL = 奥の左隅の対応表と、同距離は FL・手前の角のスロットは存在しない旨を明記。数値・規則・入力は変更なし。仕様の欠落・矛盾の報告なし。欠陥 D は範囲外) | [35-studio-to-gameplay-engineer.md](35-studio-to-gameplay-engineer.md)(出力: [36-gameplay-engineer-to-studio.md](36-gameplay-engineer-to-studio.md)) |
| 7g | Verify(再確認: V7 の同距離の規則だけ。他の基準が変わっていないことの確認) | qa | verify-change | done(`outcome: pass`。V7 の同距離は FL(奥の左隅)と一意に読める。手前の角は「there is none」と明記。V1〜V12、F-1、V10、V12(c) も前回から食い違いなし。すべて模擬ビルドの記述に基づく。欠陥 D は観察として記録。実機でしか確認できない点: V3 の窓の端の数値、30/60 FPS の実測、等距離でのログ確認) | [37-studio-to-qa.md](37-studio-to-qa.md)(出力: [38-qa-to-studio.md](38-qa-to-studio.md)) |
| 7e | Design(欠陥 D の扱い) | game-designer | write-design-spec, make-decision | skipped(Play の前には不要。規則は 2b の再現結果が出てから書くという Director の指示を維持する。Play では Playtester が何も知らされずに体験し、欠陥 D の挙動が「抜けた」感覚(§6.2)に影響したかを観察に基づいて報告する。Play か Review が、欠陥 D が結果の読み取りを妨げていると示した場合は、再び `game-designer` に回す) | — |
| 8 | Play(模擬ビルド 0.6) | playtester | playtest-session | open(7b、7g が済み、7e は skipped。新しい実行コンテキストで、模擬ビルド `sim/build-0.6.md` とプレイヤー像のみを渡す。H1〜H4 は実機では確認できない。結果は `to: studio`) | [41-studio-to-playtester.md](41-studio-to-playtester.md) |
| 9 | Review(模擬ビルドに基づく判定) | game-director | review-outcome | planned(8 の後。判定は模擬ビルドに基づく旨と、実機で確認できていない点を明記する。欠陥 D は未再現の既知の疑いとして、次の課題に挙げる) | — |

Status: planned | tentative | open | done | skipped. Handoff: the incoming Handoff that starts the
step. Parallel steps: 2a, 2b. Step numbers need not
match Handoff seq numbers. The route is a plan; the Route operation revises it.

## Route changes

- Step 1(Observe)の後: プレイテスターの観察報告(Handoff 02)は、体験の問題 A〜C(毎部屋同じ型、緊張感の欠如、ダッシュが戦闘で使われない)と、不具合の疑い D(被弾直後のダッシュ中にダメージを受けることがある)を報告した。計画どおり Diagnose(2a)に進む。
- 追加: 2b として `qa` による D の再現(`reproduce-defect`)を加えた。理由: D は仕様と食い違うか明らかな不具合の疑いであり、戻りルール(Play の結果が欠陥なら Observe は `qa`)に従う。2a の診断と互いの出力を使わない。
- 2a(Diagnose)の後: 診断(Handoff 04)は D-001 の枠内の3案を示し、方向・優先度・スコープの本当の選択があるため Decide(3)を確定し `open` にした。エスカレーションは不要と判断した。
- 3(Decide)の後: `game-director` が D-002 を記録した(主軸は案2の部屋の構成と進行、併用は予告つき Grub 突進の1つのみ。Spitter の変化、新しい敵、プレイヤー側の数値調整、キット変更は扱わない)。D-001 とビジョンの柱の範囲内で、新ボタンも不要なため、エスカレーションは発動しない。計画どおり Design(4)に進む。
- 3 の後の route 改訂: (a) Decide が実装前の実現性確認を求めたため、Plan(5a)を `planned` に確定した。(b) 突進の予告の見た目は `art-director` の範囲であり、Director も仕様後に回すと指示したため、Design(5b)を新設した。仕様が書き上がってから、5a と 5b を互いに独立なステップとして Handoff する(並列可。どちらも相手の出力を使わない)。(c) ゲーム変更が決まったため、Build(6)は `planned`、Verify(7)、Play(8)、Review(9)も `planned` に確定した。視覚要素(予告)が入るため、Verify は `art-director` の `visual-review` を並列に加える。
- 欠陥 D は、Director の指示どおり今回の戦闘仕様に含めない。2b の再現結果が出てから、ダッシュと被弾後の無敵の規則を設計書に書き足す。2b の Handoff は、Owner の報告の原文と設計文書のみを `qa` に渡す必要がある。報告文の原文は後続の Studio 操作で用意し、推測で書かない。
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
- Handoff 19 の作り方(Route 手順 4–5): 受け手 `technical-director` の Works from に合わせ、Handoff 18 の Findings(確認できたこと・できなかったこと、選択肢 (a)(b)、再開順序)を客観的な事実として抜き出した。Handoff 18 の Sender assessment は転記していない。Previous handoff として Handoff 18 を Load に入れた(`technical-director` に Sender assessment を除外する方針はない)。Handoff 18 は編集していない(受け手は Studio で、Load は Studio の routing のため)。Handoff 19 の Expected output は、Owner の判断が要る場合は Escalation(seq 20、`to: owner`)、不要な場合は `to: studio` の Handoff とした。
- 6c(Plan)の後: Escalation 20 で、`technical-director` は Owner の判断が要ると結論し、選択肢 A(実際のリポジトリとビルド・テスト手段の提供)、B(Build の範囲を実装計画と受け入れ基準の確定までに縮小)、C(模擬ビルドで工程を予行)と推奨(B。ただし実コードがあり実機で確かめたいなら A)を示した。Studio も、スコープ・費用・リスクが Goal の想定から大きく変わることを確認し、エスカレーションの条件に当たると判断した。6c を `done` にし、6d(Owner)を `open`、Goal を `blocked-on-owner` にした。
- Resume(Owner の回答、2026-10-10): Owner は Escalation 20 に Option C で回答し、条件を付けた(`sim/repo-notes.md` をコードとして扱う、Build は変更内容を Handoff に正確に書いた時点で完了、模擬ビルドはランタイムのシミュレーターが変更内容から作る、結果に模擬であることを明記し Goal の判定は模擬ビルドに基づく)。Studio は D-008(`decided_by: owner`)に Owner の言葉を含めて記録し、Escalation 20 を `resolved`(`decision: D-008`)にして、Goal を `active` に戻した。6d を `done` にした。
- Resume の route 再計画: Escalation の Option C の "If chosen" は「Owner が模擬ビルドの記述を提供した時点で Verify から再開、Goal は達成扱いにしない」だった。Owner の回答は、それとは異なる点が 3 つある。(1) 模擬ビルドを作るのは Owner ではなくランタイムのシミュレーターで、その元は Build の変更内容である。(2) `sim/repo-notes.md` をコードとして扱うため、Build(`gameplay-engineer`)は変更内容を書く工程として残る。(3) Goal の判定は模擬ビルドに基づいて行う。そのため、選択肢の記述どおりには進めず、Owner の言葉を優先して残りの route を再計画した(Resume 手順 3、選択肢に記述のない回答)。変更点は次のとおり。Build(6e)を新設して `open` にし、Handoff 21 を作った。Verify(7)、Play(8)、Review(9)は模擬ビルドを対象にし、Review は模擬ビルドに基づく判定にする。Goal を達成扱いにしない、という Escalation の記述は Owner の条件で置き換わった。ただし、結果には模擬であることを明記し、実機で確認できない点(H1〜H4)を Outcome に書く。
- 再計画での Escalation 確認: Owner の回答は D-001〜D-007、ビジョンの柱、入力ボタンに触れない。新しい Escalation の条件には当たらない。シミュレーターは Role ではないため、route の行には置かない。模擬ビルドの作成は 6e と 7 の間のランタイムの動作で、Next action に記す。
- D-007 の 7 の扱い: コードを読めない入力の欠落は、`sim/repo-notes.md` を Load に入れたことで解消した。Handoff 21 で、台帳 7 項目は `sim/repo-notes.md` に照らして確認し、答えがない項目は「模擬上の前提」と明記するよう指示した。実コードで確認済みと書かせない。
- Handoff 21 の作り方(Route 手順 4–5): 受け手 `gameplay-engineer` の Works from に合わせ、仕様と計画は Load で渡した。Previous handoff は Studio が書いた Handoff 17(Sender assessment がない)にした。Handoff 18 は Sender assessment を含むため Load に入れず、必要な事実は Handoff 21 に転記した。Expected output は `to: studio` として、Verify の `qa` と `art-director` への Handoff を Studio が組み直せるようにした。欠陥 D の原因の推測は書かせない。
- 2b の `qa` Handoff と `game-designer` の §10 追記 Handoff は、今回も作っていない(この操作で書けるのは seq 21 の 1 つ。どちらも Owner の回答に依存せず、Build とも独立で、残っている)。2b は Owner の報告の原文が入力にない限り作れない。§10 の追記は Verify の前までに済ませる。
- 6e(Build)の後: Handoff 22 は `outcome: question`。台帳 7 項目を `sim/repo-notes.md` に照らして確認し(1〜5 と 7 の一部は「模擬上の前提」と明記)、変更内容は 2.1〜2.4 に完全に書かれた。ただし波 2 以降の条件(K / T)をいつから調べ始めるか、出現位置の待ちの敵を「生きている敵」に数えるか、が仕様 §4.1 に未定義で、文面どおりだと部屋 2 の波 2 が即座に出うる(V7 に影響)。戻りルール「Build: 仕様の欠落 → Design(`game-designer`)、その後 Build に戻る」に従い、Design(6f)を新設して `open` にした。エンジニアは決めない(Skill どおり)。6e を `done` にした。
- 6e の後のエスカレーション確認: 欠落は波の出現条件の細部で、D-001〜D-008、ビジョンの柱、スコープ、入力ボタンのどれにも触れない。`game-designer` の権限(規則、ルールの細部)内の決定で、Owner エスカレーションの条件に当たらない。`game-director` に回す必要もない。ただし `game-designer` の答えが D-002・D-003 の変更やスコープの変更を要する場合は、`question` で返して Decide(`game-director`)に回す(Handoff 23 に書いた)。
- 6f の Handoff(23)の作り方(Route 手順 4–5): 受け手 `game-designer` の Works from に合わせ、Handoff 22 の Findings の「5. 仕様の欠落」から、欠落の事実、部屋ごとの K・T、選択肢 A / B / C と技術的な費用だけを抜き出した。Handoff 22 の Sender assessment(確信度、疑い 1〜3)は渡していない。`gameplay-engineer` が提案した既定 A は、選択肢の説明として「提案されている」とだけ事実を伝え、決定は `game-designer` に委ねた。Previous handoff は none(Handoff 22 が Sender assessment を含み、大部分が受け手に不要なため)。Handoff 22 は編集していない(受け手は Studio で、Load は Studio の routing のため)。
- 小さな追記の統合: 以前から残っていた「`design/combat.md` §10 に視覚仕様への参照を追記する」作業は、書き込めるのが `game-designer` で、6f と同じファイルを触るため、Handoff 23 に含めた。Verify の前までに済ませる条件はこれで満たされる。
- 6f の後: 規則の決定は Decision(D-009 を `game-designer` が記録する想定)にする。6g で Studio が `gameplay-engineer` への小さな Handoff を組み、2.1 に 1 文だけ足して Build の記述を確定させ、`to: studio` で返す。その後、シミュレーターが模擬ビルドを作り、Verify(7)を組む。
- 2b の `qa` Handoff は、今回も作っていない(Owner の報告の原文が入力にない。この操作で書けるのは seq 23 の 1 つで、Build の確定に必要な 6f を優先した)。Verify の前にある必要はないが、結果が欠陥修正を要するなら Build の再開が必要になるため、できるだけ早く処理する。
- 6f(Design)の後: Handoff 24(D-009)は `outcome: done`。`game-designer` は案 A(前の波の全員が出現中に入った時点から K・T を調べ始め、待ちの敵は生きている敵に数えない)を決め、`design/combat.md` の §4.1、§4.3 の注、V7、V12(新規)、§6.2、§8、§9 を更新し、§10 に視覚仕様への参照を追記した。数値・入力・プレイヤー側の値は変えていない。D-001〜D-003 の変更もスコープの変更もなく、`game-director` に回す必要はない。エスカレーションの条件(コンセプト・柱・Decision の変更、スコープ・費用・リスクの大幅な変化、Owner の好みが基準、不可逆、Goal の再解釈)のどれにも当たらない。6f を `done` にし、計画どおり 6g を `open` にした(Handoff 25)。§10 の参照追記は済んだので、Verify の前の条件は満たされた。
- Handoff 25 の作り方(Route 手順 4–5): 受け手 `gameplay-engineer` の Works from に合わせ、Handoff 24 の Findings から規則と足す 1 文、足りない部分の確認点を客観的に転記した。Handoff 24 には Sender assessment がなく、Previous handoff として Load に入れた。Handoff 22 の Sender assessment は転記していない。Handoff 24 は編集していない(受け手は Studio で、Load は Studio の routing のため)。Expected output は `to: studio` とし、Verify の `qa` と `art-director` への Handoff を Studio が組み直せるよう、確定した変更内容の全体を Findings に自己完結で書かせ、自己評価は Sender assessment にだけ書かせる。模擬上の前提が残る項目も一覧させる。
- Verify(7)の Handoff を作るときの条件(Route 手順 4–5 のため記録): `qa` には受け入れ基準(V7、V12 を含む)と模擬ビルドの動かし方のみを渡し、Build の Sender assessment は渡さない。`art-director` には視覚仕様と模擬ビルドを渡す。Playtester(8)には模擬ビルドとプレイヤー像のみで、仕様の数値や体験の観点(§6.2、視覚仕様 §10.2)は書かない。
- 2b の `qa` Handoff は、今回も作っていない(Owner の報告の原文が入力にない。この操作で書けるのは seq 25 の 1 つ)。独立で、残っている。
- 6g(Build)の後: Handoff 26 は `outcome: question`。止まった原因は入力の欠落だけである。Handoff 25 の Load に Handoff 22(変更内容の記述 2.1〜2.4)が入っておらず、`gameplay-engineer` は記述の全体を推測せずに返した。これは Studio の Load の漏れで、仕様の曖昧さや矛盾は報告されていない(`game-designer` に回すものはない)。D-001〜D-009、ビジョンの柱、スコープ、入力ボタンのどれにも触れず、エスカレーションの条件に当たらない。`game-director` に回す必要もない。Handoff 26 の選択肢 (a)(Handoff 22 などを Load に入れて同じ Step をやり直す)を採った。選択肢 (b)(Handoff 22 抜きで書き直す)は、記述の食い違いを保証できないため採らない。6g を `done` にし、6h を `open` にした(Handoff 27)。ループ制限には当たらない(初めての欠落で、受け入れ基準の失敗でもない)。ただし Handoff 27 でも必須ファイルが読めない場合は、再試行せず返すよう指示した。その場合は次の Route で、パケットの組み方そのものを見直す。
- Handoff 27 の作り方(Route 手順 4–5): 受け手 `gameplay-engineer` の Works from に合わせて組んだ。Load に Handoff 22(記述の元)、Handoff 17(台帳。Handoff 16 は `technical-director` の Sender assessment を含むため使わない)、設計書 2 点、`sim/repo-notes.md`、D-004〜D-009 を加えた。Previous handoff は Handoff 26 にした(`gameplay-engineer` 自身が書いたもので、Sender assessment を除外する方針は `gameplay-engineer` にない)。Handoff 22 の内容は、この操作の入力になかったため要約せず、Load での指定に留めた。Handoff 26 の Findings 2〜4 は「下書き」として渡し、Handoff 22 と台帳に照らして確認させ、食い違いは Handoff 22 側を正とするよう書いた。Handoff 26 は編集していない(`to: studio` で、Load は Studio の routing のため)。
- Handoff 26 が V12(b) について指摘した帰結(待ちの間に R の Grub を倒していたら、波 2 はすぐ出る)は、Verify の Handoff を組むときに期待値として渡す必要がある。Handoff 27 に記録した。
- 2b の `qa` Handoff は、今回も作っていない(Owner の報告の原文が入力にない。この操作で書けるのは seq 27 の 1 つ)。独立で、残っている。
- 6h(Build)の後: Handoff 28 は `outcome: done`。変更内容 2.1〜2.4 に D-009 の 1 文が統合され、Handoff 22 を読まなくても分かる形で確定した。Handoff 22 と D-009 の間に、1 文の統合以外の食い違いはなく、`game-designer` に回す問いもない(§4.3 の表の注記の言い回しが紛らわしいという指摘は、規則の食い違いではなく、表現の整理の提案として残る。Verify の期待値には影響しない)。D-001〜D-009、ビジョンの柱、スコープ、入力ボタンのどれにも触れず、エスカレーションの条件に当たらない。`game-director` に回す必要もない。6h を `done` にし、計画どおり Verify に進む。
- Verify の route 改訂: Verify(7)を 7a(`qa`)と 7b(`art-director`)の並列に分けた。7a と 7b は互いの出力を使わない。この操作で書けるのは seq 29 の 1 つだけなので、`qa` の Handoff(29)を先に作り、7b の Handoff は後続の Studio 操作が次の空き seq で作る。Play(8)は 7a と 7b の両方の後。
- 模擬ビルドの扱い: 模擬ビルドは、プロジェクトのファイル一覧に `sim/build-0.4.md` として存在する。Handoff 28 の変更内容からシミュレーターが作ったものとして扱い、Handoff 29 の Load に指定した。この操作の入力に `sim/build-0.4.md` の中身はなく、内容を確認していない。`qa` が読めない、または記述と矛盾する場合は、`qa` は推測せず報告する。
- Handoff 29 の作り方(Route 手順 4–5): 受け手 `qa` の Works from(受け入れ基準、変更の動かし方、制約。実装者の自己評価や説明は渡さない)と Independence に合わせ、Studio が新しく組んだ。Handoff 28 は Sender assessment を含み、かつ実装の説明なので Previous handoff にも Load にも入れていない(Previous handoff は none)。受け入れ基準は `design/combat.md` の V1〜V12 を Load で指定し、本文は要約しなかった。V12 の期待値「待ちの間に先に出ていた敵を倒すと、次の波はすぐ出る」は、仕様(§4.1、D-009)の規則から導かれる期待値として、実装の説明を添えずに書いた。Handoff 28 は編集していない(受け手は Studio で、Load は Studio の routing のため)。欠陥 D の原因の推測は渡していない。
- 2b の `qa` Handoff は、今回も作っていない(Owner の報告の原文が入力にない。この操作で書けるのは seq 29 の 1 つ)。独立で、残っている。Play の前までに処理する必要はないが、欠陥の修正が要る場合は Build の再開が必要になる。
- 7a(Verify)の後: Handoff 30 は `outcome: question`。V1〜V12 に fail はなく、同じ基準が 2 回失敗した事例もないため、Verify の戻りルール(2 回目の失敗は Plan)は発動しない。V7(Grub の速度の数値、遠い角が同距離のときの規則)と V10(プレイヤー側の数値)は、模擬ビルドの記述に書かれておらず、pass にできない。さらに基準外で、仕様 §3.3 と模擬ビルドの食い違い F-1(突進の再開始の待ち時間の起点が、仕様は Recovery 終了後、ビルドは突進終了後)が見つかった。
- 7a の後の route 改訂: (a) F-1 は「ビルドされた挙動が仕様と違う」ので、戻りルール「Verify: fail(built behavior differs)→ Build(`gameplay-engineer`)」に従い、Build(7c)を新設して `open` にした(Handoff 31)。仕様の文面が曖昧なら、`gameplay-engineer` は直さずに `game-designer` への質問として返す(Handoff 31 の Open questions 1)。Studio は意図を決めない(`game-designer` と `qa` の権限)。(b) V7 と V10 の未確認は、模擬ビルドの記述の欠落であり、元は変更内容(Handoff 28 の 2.1〜2.4)に数値と規則が書かれているかの問題になる。速度は仕様に数値があり、遠い角が同距離のときの規則と、プレイヤー側の数値が「変えていない」と明記されていないことが原因と見て、同じ Build(7c)で変更内容に明記させる。仕様に規則がない場合は `outcome: question` で返し、次の Route で `game-designer` に回す。(c) 再検証 7d(`qa`)を 7c の後に `planned` で加えた。(d) 7b(視覚)は F-1 の修正に影響されないので、7c と並行して作れる。次の空き seq で Handoff を組む。
- 7a の後のエスカレーション確認: F-1、V7、V10 の扱いは、D-001〜D-009、ビジョンの柱、スコープ、入力ボタンのどれにも触れない。コンセプト・柱・Decision の変更はなく、スコープ・費用・リスクの大幅な変化でもなく、不可逆でもない。Owner のエスカレーションの条件に当たらない。`game-director` に回す必要もない。
- 欠陥 D の扱い: Handoff 30 が、模擬ビルド 0.4 は被弾直後のダッシュ中にダメージを受けうることを記述しており、仕様は意図的に未定義で、Play の「抜けた」という感覚(§6.2)に影響しうると報告した。規則を決めるのは `game-designer` だが、Director の指示(2b の再現結果が出てから規則を書く)は変えない。Owner の元の報告文が入力にないため 2b の Handoff は今回も作れない。Play の前に扱うかどうかは未決なので、Design(7e)を `tentative` で加えた(条件は route 表に記載)。この操作で書けるのは seq 31 の 1 つだけで、Build の修正(7c)を優先した。Handoff 31 には欠陥 D の原因の推測や規則の変更を書かず、範囲外と明記した。
- Handoff 31 の作り方(Route 手順 4–5): 受け手 `gameplay-engineer` の Works from に合わせ、Handoff 30 の Findings(`qa` の報告。Sender assessment を持たない)から F-1、V7 の未確認 2 点、V10 の未確認、補足(V12(c))を客観的な事実として転記した。`qa` の Independence は受け手が `qa` の場合の制約で、`gameplay-engineer` への制限ではないため、Handoff 30 を Previous handoff にした。修正する変更内容の元は自分が書いた Handoff 28 で、Load に入れた(Handoff 26 の漏れの再発防止)。Handoff 30 は編集していない(受け手は Studio で、Load は Studio の routing のため)。Expected output は `to: studio` とし、再検証 7d の `qa` Handoff を Studio が Sender assessment を除いて組み直せるよう、修正後の変更内容の全体を Findings に自己完結で書かせ、自己評価は Sender assessment にだけ書かせる。
- ループ制限の確認: 同じ受け入れ基準が 2 回失敗した事例はない。7c の後の再検証で F-1 または V7・V10 が再び落ちた場合は、`technical-director` に回す。
- 2b の `qa` Handoff は、今回も作っていない(Owner の報告の原文が入力にない。この操作で書けるのは seq 31 の 1 つ)。独立で、残っている。
- 7c(Build)の後: Handoff 32 は `outcome: done`。修正後の変更内容 2.1〜2.4 の全体が自己完結で書かれ、`question` ではない。仕様の欠落・矛盾の報告はなく、`game-designer` に回すものはない。F-1 は仕様 §3.3 の文面が曖昧ではなく、仕様に合わせて起点を「Recovery の終了」と明記した。V7(Grub 速度 2.0 / 2.0 / 2.2 / 2.2 / 2.4、遠い角が同距離なら FL)と V10(プレイヤー側の数値は変更なし)も明記され、V12(c)の1文も足された。数値・規則・入力は変わらず、D-001〜D-009、ビジョンの柱、スコープに触れない。エスカレーションの条件に当たらず、`game-director` に回す必要もない。7c を `done` にし、計画どおり再検証 7d を `open` にした(Handoff 33)。
- 7c の後の注意点: Handoff 32 の報告によれば、Handoff 28 の変更内容は、すでに F-1 の起点を「前回の Recovery が終わってから」と書いていた。つまり、模擬ビルド 0.4 が「突進が終わってから」と書いた原因は、変更内容の曖昧さではなく、シミュレーターが記述を写す過程にある可能性がある(推測であり、確定していない)。7d で、更新された模擬ビルド(`sim/build-0.5.md`)がまだ F-1 を食い違いとして示すなら、それは同じ基準の2回目の食い違いとして扱い、ループ制限(同じ受け入れ基準が2回 fail → `technical-director` に回す)に従う。Studio は原因を決めつけない。
- Handoff 33 の作り方(Route 手順 4–5): 受け手 `qa` の Works from(受け入れ基準、変更の動かし方、制約。実装者の自己評価と説明は渡さない)と Independence に合わせ、Studio が新しく組んだ。Handoff 32 は変更内容の説明と Sender assessment を含むため、Previous handoff にも Load にも入れていない。期待値(F-1 の起点、V7 の数値と同距離の規則、V10、V12(c))は、仕様 `design/combat.md` と D-005、D-009 から導かれる内容として書き、実装の説明は添えていない。Previous handoff は Handoff 30(`qa` 自身の前回の報告で、Sender assessment を持たない)にした。欠陥 D は範囲外とし、原因の推測は渡していない。結果は `to: studio` にした(Play の Handoff を Studio が実装の履歴なしで組むため)。Handoff 32 は編集していない(受け手は Studio で、Load は Studio の routing のため)。
- 模擬ビルドの扱い: `sim/build-0.5.md` は、Handoff 32 の変更内容からシミュレーターが作ったものとして扱う。この操作の入力に中身はなく、Studio は内容を確認していない。
- 7b と 2b の Handoff は、今回も作っていない(この操作で書けるのは seq 33 の 1 つ。7b は 7d と独立で、Play の前までに作る。2b は Owner の報告の原文が入力にないため作れない)。
- 7d(Verify)の後: Handoff 34 は `outcome: question`。fail はない。F-1、V10、V12(c) は解消し、V1〜V12 の回帰も pass(模擬)。残った 1 点は V7 の「同距離のとき」の規則の用語で、ビルド 0.5 は「front-left corner」と書き、他の箇所の far-left / far-right と食い違うため、仕様の FL(奥の左隅)を指すか `qa` が確認できなかった。F-1 は前回と同じ点だが今回は食い違わず、V7 は前回は「記述なし(未確認)」、今回は「用語が曖昧(未確認)」で、どちらも fail ではない。したがって「同じ基準が 2 回 fail」のループ制限は発動しない。
- 7d の後の route 改訂: 期待値は仕様と D-005 で定義済みで(`qa` も明言)、Design(`game-designer`)に回す問いはない。問題は変更内容の記述の用語に限られるため、戻りルール「Verify: 食い違い → Build(`gameplay-engineer`)」に従い、Build(7f)を新設して `open` にした(Handoff 35)。再確認 7g(`qa`)を 7f の後に `planned` で加えた(同距離の規則だけ。他の基準が変わっていないことを確認する。F-1、V10、V12(c) は再確認不要)。Play(8)の前提を 7b、7g(必要なら 7e)に直した。`qa` の確認方法の候補(ビルド記述の修正、または等距離の位置での開発用ログ確認)のうち、模擬では実機の位置確認が使えず、記述の修正が最小で足りるため、前者を採った。
- 7d の後のエスカレーション確認: 用語の明記だけで、D-001〜D-009、ビジョンの柱、スコープ、入力ボタンのどれにも触れない。エスカレーションの条件に当たらず、`game-director` にも回さない。
- 注意(ループ制限): 7f の後の 7g で、V7 の同距離の規則が再び確認できない、または仕様と違う場合は、V7 の同じ基準が連続して通らないことになる。その場合は `technical-director` に回し、記述→シミュレーター変換の経路そのものを見直させる。Handoff 35 の Open question 1 で、Handoff 32 の記述が FL と書いていたかを事実として報告させる。FL と書いていたなら、用語のずれはシミュレーター側の可能性があるが、Studio は原因を決めつけない。
- Handoff 35 の作り方(Route 手順 4–5): 受け手 `gameplay-engineer` の Works from に合わせ、Handoff 34 の Findings(`qa` の報告。Sender assessment を持たない)から、V7 の同距離の規則に関する客観的な事実だけを転記した。Previous handoff は Handoff 34、修正前の変更内容の元は Handoff 32(自分が書いたもの)を Load に明記した(Handoff 26 の漏れの再発防止)。`sim/build-0.5.md` は参照のみ。Handoff 34 は編集していない(受け手は Studio で、Load は Studio の routing のため)。Expected output は `to: studio` とし、7g の `qa` Handoff を Studio が Sender assessment を除いて組み直せるよう、修正後の変更内容の全体を自己完結で書かせ、自己評価は Sender assessment にだけ書かせる。
- 7b と 2b の Handoff は、今回も作っていない(この操作で書けるのは seq 35 の 1 つ。7f が 7g と Play への経路を止めているため優先した。7b は 7f と独立で、次の空き seq で作れる。2b は Owner の報告の原文が入力にないため作れない)。7b は更新される模擬ビルドを使うため、7f の後に作る方が再作業を避けられるが、7f と並行して作ってもよい。
- 7f(Build)の後: Handoff 36 は `outcome: done`。修正後の変更内容 2.1〜2.4 の全体が自己完結で書かれ、`question` ではない。Handoff 32 は同距離の規則を「FL を選ぶ」と書いており、「front-left」「手前の角」の語はなかったと報告された。つまりビルド 0.5 の「front-left corner」はシミュレーターが記述を写す過程で生じた可能性があるが、推測であり、Studio は原因を決めつけない。今回の記述は FL = 奥の左隅(far-left corner)の対応表を足し、同距離は FL、手前の角のスロットは存在しないと明記した。数値・規則・入力は変わらず、仕様の欠落・矛盾の報告もない。D-001〜D-009、ビジョンの柱、スコープ、入力ボタンに触れず、エスカレーションの条件に当たらない。`game-designer`・`game-director` に回す必要もない。7f を `done` にし、計画どおり 7g を `open` にした(Handoff 37)。
- Handoff 37 の作り方(Route 手順 4–5): 受け手 `qa` の Works from(受け入れ基準、変更の動かし方、制約。実装者の自己評価や説明は渡さない)と Independence に合わせ、Studio が新しく組んだ。Handoff 36 は変更内容の説明と Sender assessment を含むため、Previous handoff にも Load にも入れていない。期待値(同距離は FL = 奥の左隅、手前の角のスロットは存在しない、選び直さない)は、仕様 §4.1 と D-005 から導かれる内容として書き、実装の説明は添えていない。「何を直したか」も伝えていない。Previous handoff は Handoff 34(`qa` 自身の前回の報告)。模擬ビルドは `sim/build-0.6.md`(Handoff 36 の変更内容からシミュレーターが作ったものとして扱う。この操作の入力に中身はなく、Studio は内容を確認していない)。結果は `to: studio`。Handoff 36 は編集していない(受け手は Studio で、Load は Studio の routing のため)。
- ループ制限の確認: 7g で V7 の同距離の規則が再び確認できない、または仕様と違うと報告された場合は、同じ基準が連続して通らないことになる。その場合は `technical-director` に回し、記述→模擬ビルド変換の経路を見直させる。
- 7b と 2b の Handoff は、今回も作っていない(この操作で書けるのは seq 37 の 1 つ。7b は 7g と独立で、Play の前までに作る。最新の模擬ビルドは `sim/build-0.6.md`。2b は Owner の報告の原文が入力にないため作れない)。
- 7g(Verify)の後: Handoff 38 は `outcome: pass`。V7 の同距離の規則は、ビルド 0.6 の記述で「the far-left corner」と書かれ、手前の角は「there is none」と明記されており、仕様の FL(奥の左隅)以外を指せない。部屋 3・4・5 の記述も同じ語で揃っている。V1〜V12 に fail も確認不能もなく、F-1、V10、V12(c) も前回から食い違っていない。すべて模擬ビルドの記述に基づく。V7 の同じ基準が連続して通らない事態にはならなかったので、ループ制限(`technical-director` への回付)は発動しない。7g を `done` にした。D-001〜D-009、ビジョンの柱、スコープ、入力ボタンのどれにも触れず、エスカレーションの条件に当たらない。`game-designer`・`game-director` に回すものもない。
- 7e(欠陥 D)の決定: `skipped` にした。理由: (a) 規則を決める権限は `game-designer` にあり、Director の指示(2b の再現結果が出てから規則を書く)がある。Owner の元の報告文が入力になく 2b を作れないため、Play の前に規則を決める根拠が揃わない。(b) 欠陥 D の挙動は模擬ビルドが記述しており、Playtester は何も知らされずに体験できる。Playtester に既知の欠陥として伝えると Independence に反し、観察を歪めるため、伝えない。(c) Play の結果が欠陥 D を体験の阻害要因と示した場合は、戻りルール(Play: 欠陥 → Observe(`qa`)、設計・体験の問題 → Diagnose(`game-designer`))に従い、その時点で再び回す。これは Studio の process 上の判断で、ゲームの内容は決めていない。Review では、欠陥 D を未再現の既知の疑いとして次の課題に挙げる。
- Handoff 38 は Previous handoff が 37 の `qa` 自身の報告で、受け手は Studio のため編集していない。また 38 の Open questions 2(実機でしか確認できない点: V3 の窓の端、30/60 FPS の実測、等距離のログ確認)は、Outcome の「実機で確認できない点」に H1〜H4 とあわせて書く。
- 7b の Handoff(39)を作った。Verify の残りは 7b だけで、Play の前までに必要なので、これを優先した。7b と 7g は互いの出力を使わず、7g が済んだ今、7b の入力(視覚仕様、D-006、美術方針、最新の模擬ビルド `sim/build-0.6.md`)は揃っている。Handoff 39 の作り方(Route 手順 4–5): 受け手 `art-director` の Works from(視覚的含意のある仕様、構築物のレビュー、美術方針と制約)に合わせ、Studio が新しく組んだ。実装の説明や Build の Sender assessment は渡していない。`qa` の報告から渡したのは、ビルド 0.6 に新しい音・新しいボタンがなく、点滅が 1 秒間に 3 回を超えないという客観的な事実だけにした。視覚仕様の本文は要約せず Load で指定した。Previous handoff は none。結果は `to: studio`(Play の Handoff を実装の履歴なしで組むため)。判定は模擬ビルドの記述に基づくことと、実機要の点を分けて書くことを指示した。Handoff 38 は編集していない。
- 模擬ビルドの扱い: `sim/build-0.6.md` の中身は、この操作の入力に Handoff 38 での引用の範囲でしかなく、Studio は全体を確認していない。`art-director` が読めない、または記述と矛盾する場合は推測せず報告する。
- 2b(`qa`、欠陥 D の再現)の Handoff は、今回も作っていない(Owner の報告の原文が入力にない。この操作で書けるのは seq 39 の 1 つ)。独立で、Play の前提ではなくなった(7e skipped)。原文を Owner から得られた時点で、次の空き seq で作る。
- 7b(Verify、視覚)の後: Handoff 40 は `outcome: pass`(模擬ビルド 0.6 の記述に基づく)。A1〜A13 に fail はない。A5 は確認不能(実機要)、A8・A9・A10・A11 には記述の欠落か実機要の部分が残る(欠落 G1〜G5 は矛盾ではなく、ビルドの修正は求められていない)。赤橙は害になる状態だけに使われ、D-006 に反しない。戦闘の規則・数値・入力の変更は不要で、新しい Decision(D-010)も作られていない。D-001〜D-009、ビジョンの柱、スコープに触れず、エスカレーションの条件に当たらない。`game-designer`・`game-director` に回すものもない。7b を `done` にし、計画どおり Play(8)を `open` にした(Handoff 41)。Verify の戻りルール(2 回目の失敗は Plan)に関わる事例はない。
- Handoff 41 の作り方(Route 手順 4–5): 受け手 `playtester` の Works from と Independence に合わせ、Studio が新しく組んだ。渡したのは、ビルドの入手(`sim/build-0.6.md`)、プレイヤー像(`project.md#player-profile`)、一般的な注意の向け先「戦闘」だけである。何が変わったか、期待する結果、受け入れ基準(V 系、A 系)、仕様の数値、欠陥 D の存在、Handoff 40 の内容は渡していない。Previous handoff は none、Decisions は none、Load は最小にした。結果は `to: studio`(Review の Handoff を Studio が組むため)で、判定や解決策の決定は求めず、読みだけでは判断できなかった点は「確認できなかった」と書くよう指示した。
- 指示と実際の差(Handoff 40 の Expected output 2): Handoff 40 は、§1.5 の実機項目と S1〜S3 を観察の観点として Play の Handoff に渡すよう求めていた。例の文言(「抜けたと感じたか」「レーンの上に立ったとき、まだ危ないと感じたか」など)は、設計側の仮説を示唆し、Playtester の Independence(期待する結果を示さない)に反するため、渡さなかった。Playtester は自由に観察を報告する。S1〜S3 と実機項目は、Play の報告が出た後に、Studio が観察報告と突き合わせる材料として下に残す。Playtester に渡さなかったことは Role の権限の変更ではなく、Studio の process 上の判断である。
- Play の後の戻し方(Handoff 40 の Expected output 3 と戻りルールを引き継ぐ): 「0.7 s では足りない」が出て、見た目の強調で補えないなら `game-designer` へ(`design/combat.md` §7)。S1(抜けた合図と出現中の輪の混同)、S2(解決後もレーンが赤橙のままの誤読)、Recovery の誤読が出たら `art-director` へ戻し、Handoff 40 の修正方針で見た目だけを直す(規則は変えない)。欠陥 D が体験の阻害要因と示された場合は、7e/2b の扱いに従う。
- 保留項目の引き継ぎ(Review 用): Handoff 40 の実機要項目(暗い床での 35% のレーン、レーンと弾・ランタイムの光の区別、0.7 s の十分さ、Recovery の誤読、かすりの感触、抜けた合図の過剰、小さい画面での尾根、30/60 FPS、色覚の差)、S1〜S3、ビルド記述の欠落 G1〜G5 は、Outcome の「実機で確認できない点」に H1〜H4、Handoff 38 の実機要の点(V3 の窓の端、30/60 FPS の実測、等距離でのログ確認)とあわせて書く。
- 2b の `qa` Handoff は、今回も作っていない(Owner の報告の原文が入力にない。この操作で書けるのは seq 41 の 1 つ)。独立で、残っている。

## Next action

Goal は `active`。Play(8、`playtester`)が `open`。Handoff: `goals/G-001-combat-monotony/41-studio-to-playtester.md`。

1. `playtester` が新しい実行コンテキストで Handoff 41 に従い、模擬ビルド `sim/build-0.6.md` をプレイヤー像で遊び、観察報告を `to: studio` の Handoff(`42-playtester-to-studio.md`)で返す。読みだけでは判断できない点は「確認できなかった」と書く。
2. 報告を受けた次の Route で、Studio は結果を計画と突き合わせる。(a) 見た目の混同(S1、S2、Recovery の誤読)は `art-director` へ、(b) 「0.7 s では足りない」で見た目で補えないものは `game-designer` へ、(c) 欠陥らしい挙動(欠陥 D を含む)が阻害要因と示された場合は戻りルール(Play: 欠陥 → Observe(`qa`))と 7e/2b の扱いに従う。問題がなければ Review(9)を `game-director` 向けに組む。Review には、判定が模擬ビルドに基づくことと、実機で確認できない点を明記する。
3. 2b(`qa`、`reproduce-defect`)は Owner の元の報告文が必要で、原文が入力にある場合に作る。Play か Review が欠陥 D を体験の阻害要因と示した場合は、再び回す。

Owner への報告(日本語):
- 突進の予告の見た目(視覚仕様)の確認が、模擬ビルド 0.6 の記述に基づいて pass で済みました。赤橙は害になる状態だけに使われており、規則・数値・入力に変更は要りません。Owner の判断は不要です。
- 次に、模擬ビルドとプレイヤー像だけを渡した Playtester のプレイに進みます。変更内容や期待する結果は伝えません。
- 欠陥 D(被弾直後のダッシュ中にダメージを受けることがある)は、引き続き Play の前には扱いません。再現(`qa`)には Owner の元の報告文が必要です。原文をいただければ、いつでも `qa` に回せます。
- すべて模擬ビルドの記述に基づく結果です。暗い床での読み取りやすさ、ゲームパッドの操作感、0.7 秒の予告の十分さ、30/60 FPS の実測などは、実機では確認できないままです。

## Outcome

(未完了)
>>>END

<<<FILE goals/G-001-combat-monotony/42-playtester-to-studio.md
---
kind: handoff
goal: G-001
seq: 42
from: playtester
to: studio
stage: Review
outcome: done
---
# 42: playtester → studio — ビルド 0.6 の戦闘体験の観察報告

## Task

ビルド 0.6 をプレイヤー像として遊んだ観察を報告する。判定や解決策は含めない。次の Review の Handoff を Studio が組むための材料とする。

## Context

Goal G-001(戦闘の単調さ)に関するプレイ。Handoff 41 の指示で、ビルド 0.6 の部屋 1〜5 を、戦闘に注意を向けて遊んだ。プレイヤー像は、短時間で濃いランを求めるアクション好きで、回避と間合いには慣れ、コンボ表の暗記は好まず、主にゲームパッドで遊ぶ。

## Findings

### プレイ方法(実際に使った方法)

- 実機ではなく、ドライランの約束事に従った。`sim/build-0.6.md` の「プレイヤーに見える記述」を読み、その場面を遊んだつもりで体験を書いている。
- 入力は移動、スワイプ(攻撃)、ダッシュだけを想定した。開発用の部屋選択、突進オン/オフ、30/60 FPS 切替、ログは使っていない。
- したがって、以下の「感じたこと」は記述から思い描いた体験である。実際に手を動かして得た感触ではない。
- 確認できなかったこと:
  - 実時間の感触(0.7 秒の予告が長いか短いか、3.3 秒間隔がだれるか、など)
  - 画面での実際の見え方(レーンの視認性、床の暗さ、リング、湯気、残像の見え方)
  - ゲームパッドの操作感、スティックでの避けやすさ
  - 移動速度の具体値(記述に数値がなく、Grub の歩行速度 2.0〜2.4 と比べられない)
  - 音(新しい音はないと書かれているだけ)
  - 30 FPS と 60 FPS の違いの体感

### セッション概要

部屋 1 から 5 まで順に想定して遊んだ。部屋 1 と 3 は、波が 2 回に分かれる以外は以前に近い。部屋 2、4、5 では突進する Grub(背中に暗い燃え殻色の隆起がある個体)が出て、戦い方が変わった。

### 具体的な場面

1. **部屋 1(通常 Grub 3 体、同時最大 2)**
   - 左右に Grub が出て、倒すと奥から 1 体追加で出る。
   - 見たこと: 出現中の 0.8 秒は動かず、スワイプも効かない。
   - 感じたこと: 追加の 1 体が来るので少しだけ「次が来る」感じがあるが、やることは従来どおり。注意は上がらない。
2. **部屋 2(突進 Grub 初登場)**
   - 最初の波は、奥に隆起付きの Grub が 1 体。
   - 見たこと: 3〜6 タイル離れた位置にいると、Grub が止まり、床に赤橙のレーンが伸びる。約 0.7 秒後、レーンに沿って走ってくる。
   - 感じたこと: レーンを見てから横に動くか、ダッシュで抜けられる。「見てから避ける」場面が自然に生まれる。コンボ表の暗記は要らない。
   - ダッシュで Grub をすり抜けるとダメージを受けず、白青い輪が出る(0.15 秒)。ダッシュ(0.25 秒の無敵)が狙いどおりに効いたと分かる合図になる。
   - 突進中にスワイプしても HP が減るだけで止まらない。白く光って火花が出る。「当たったのに止まらない」感じがある。
   - 2 発(HP 2)で倒せる。スワイプの硬直は 0.35 秒。
3. **隅で立ち止まってスワイプするだけの戦い方**
   - 記述の限りでは、部屋 2、4、5 では通用しない。レーンが出て、約 0.7 秒後に突っ込まれる。
4. **突進の間隔**
   - 1 体なら、前回の突進終了から約 3.3 秒以上あとに次の予告が出る。これは「突進→待つ→突進」の拍があるという意味。
   - 実際に退屈か、ちょうどよいかは確認できなかった。
5. **突進が来ない距離**
   - 記述上、Grub から 3 タイル未満に張り付くか、6 タイルより離れると、突進は始まらない。その間、普通の Grub のように歩いて噛むだけに見える。
   - 近づいて殴り続ければ、突進を一度も見ずに済む可能性がある(記述からの読みで、実際には試していない)。
6. **部屋 3(Spitter 初登場に近い構成、通常 Grub と Spitter)**
   - Spitter は動かず、2.0 秒おきに撃つ。弾速は 4.0 で、撃った瞬間の自分の位置を狙う。1 ハート減る。
   - 感じたこと: 動き続ければ避けられそう。出現後 1.0 秒は撃たないので、最初の一発の前に落ち着ける。
   - 第 2 波の Spitter は、自分から遠い奥の隅に出る。近づくのに距離がある。
7. **部屋 4(Spitter + 突進 Grub + 通常 Grub、同時最大 3)**
   - 弾を避けながら突進レーンも見る必要が出る。
   - レーンは Spitter の弾や他の敵より下に描かれる。弾と重なると見づらくなるかもしれないが、実際の見え方は確認できなかった。
   - 第 2 波は右奥の隅の Spitter と右の突進 Grub。
8. **部屋 5(6 体、同時最大 4、Spitter は 1.6 秒おき、Grub 歩行 2.4)**
   - 一番忙しい。弾、歩いてくる Grub、突進が重なる。
   - 第 2 波で左右に突進 Grub が 2 体出る。同時に条件を満たしても突進するのは 1 体ずつで、先に動くのはどちらか分からない順序(記述に「目立たない決まった順」とある)。
   - 感じたこと: 2 体同時に突進されないのは助かる。ただし「どちらが先か」を読めない。
9. **出現位置の近くに立つ**
   - 出現点の 4 タイル以内にいると、その敵は最大 2.0 秒出てこない。その間、次の波も始まらない。
   - 部屋 1 で左の出現点だけに近づくと、右の Grub だけが出て、左の Grub は遅れて出る。
   - 見たこと: 出現を待たせても押し出されない。出現した敵が自分の真上に出ることがある。出現中の 0.8 秒は無害だが、その後すぐ噛まれうる。
   - 感じたこと: 「敵が出てこない」ことに戸惑う可能性がある。待ちが見えるのかは確認できなかった。
10. **被弾直後のダッシュ**
    - 記述に「以前と同様、被弾直後にダッシュすると、ダッシュの途中でダメージを受けることがある」とある。突進が当たる瞬間にも同じことが起きうる、と書かれている。
    - 不具合らしい挙動として、観察のままここに記す。実際に起きるかは確認できなかった。

### 問題と影響度

| # | 内容 | 影響度 |
|---|------|--------|
| A | 部屋 1、3 は戦い方が前と変わらず、第 2 波が来るだけ。戦闘の変化は部屋 2、4、5 に集中している | 中(記述からの印象) |
| B | 突進 Grub に 3 タイル未満で張り付く、または 6 タイルより離れると突進が出ない。突進を見ずに済む戦い方がありうる | 中(試していない) |
| C | 突進中のスワイプは「効いているのに止まらない」。フィードバックはあるが、当たった手応えは薄そう | 低〜中(実際の感触は確認できなかった) |
| D | 出現点の近くに立つと敵が最大 2.0 秒出ず、次の波も遅れる。理由がプレイヤーに伝わるか不明 | 低〜中 |
| E | 被弾直後のダッシュで、無敵のはずが途中で被ダメージ(既知の挙動として記述あり) | 高になりうる(突進を避けるためのダッシュに影響する) |
| F | 部屋 5 は敵の種類が重なり、突進の順序も読めない。忙しさが公平な難しさか、運任せかは確認できなかった | 不明 |

### よかった点

- 予告(レーン、しゃがみ込み、色の変化)があり、見てから避けられる設計に見える。
- 背中の隆起で、突進する個体が出現直後から見分けられる。
- ダッシュで抜ける、横に避ける、という既存の操作だけで対応できる。新しいボタンも覚えることもない。
- 突進は同時に 1 体だけなので、最悪の重なりは避けられている。
- 突進後の「湯気を出して止まる」回復の時間(0.8 秒)が、反撃のチャンスとして読める。

### 観察とは分けた仮説(原因の推測)

- 部屋 2、4、5 での「立ち止まりスワイプの無効化」が、戦闘の単調さを減らしている可能性がある。ただし、実際に飽きにくくなったかは、実時間で遊ばないと言えない。
- 「近づき過ぎると突進しない」性質が、新しい単調さ(張り付き戦法)を生むかもしれない。

### プレイヤーとしての未解決の疑問

- 突進 Grub に張り付いたときも、予告なしに突進されることはないのか。
- 被弾直後のダッシュで途中被弾するのは、どのくらいの頻度で起きるのか。
- 出現を待たされているとき、画面でそれと分かるのか。
- 部屋 5 の 2 体の突進 Grub は、どちらが先に動くのか読めるのか。

## Decisions already made

None

## Constraints

- 観察は `sim/build-0.6.md` を読んで想定した体験である。実時間、見た目、ゲームパッドの感触、音は確認できなかった。
- 原因の推測と設計案は、観察と分けて書いた(仮説の節のみ)。

## Open questions

None

## Expected output

Studio が、この観察報告から次の Review の Handoff を組む。判定や解決策の決定は、この報告には含めていない。

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile、sim/build-0.6.md
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/41-studio-to-playtester.md
>>>END
