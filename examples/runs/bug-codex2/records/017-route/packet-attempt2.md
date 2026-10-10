# Studio operation packet

operation: Route
goal: G-001
step_artifact: goals/G-001-dash-damage/15-gameplay-engineer-to-studio.md
next_seq: 16

## You may write

- goals/G-001-dash-damage/goal.md
- goals/G-001-dash-damage/15-gameplay-engineer-to-studio.md (in place: keep kind, goal, seq, from, to)
- goals/G-001-dash-damage/16-studio-to-<role>.md

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
- the Goal itself has to be reinterpreted to make progress;
- the work is blocked on information or material that no Role can produce (e.g., reproduction
  details only the Owner has, a build or repository that does not exist). The brief says exactly
  what is needed and why no Role can produce it; options include providing it, narrowing the Goal,
  or stopping.

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
- A step hands back `question` twice for the same missing input, with nothing new supplied in
  between → do not route it to a Role again; escalate to the Owner for that input.
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
- Dry-run project: there is no real repository. `sim/repo-notes.md` stands in for the code. A Build
  step implements a change by stating it exactly in its Handoff (what changes, where, and how to
  exercise it); the change then counts as made, and the runtime's simulator updates `sim/` from it.

## Art direction

Dark caves lit by the player's lantern; warm light against cold blue-black. Threats use saturated
orange/red so they read against the dark.

## Design index

- `design/combat.md` — player kit, damage and invulnerability rules, enemies.
>>>END

<<<FILE @project-files
decisions/D-001-one-button-combat.md
decisions/D-002-resume-with-owner-observations.md
decisions/D-003-independent-invulnerability.md
design/combat.md
goals/G-001-dash-damage/01-studio-to-qa.md
goals/G-001-dash-damage/02-qa-to-studio.md
goals/G-001-dash-damage/03-studio-to-qa.md
goals/G-001-dash-damage/04-qa-to-studio.md
goals/G-001-dash-damage/05-studio-to-qa.md
goals/G-001-dash-damage/06-qa-to-studio.md
goals/G-001-dash-damage/07-studio-to-qa.md
goals/G-001-dash-damage/08-qa-to-studio.md
goals/G-001-dash-damage/09-studio-to-owner.md
goals/G-001-dash-damage/10-studio-to-qa.md
goals/G-001-dash-damage/11-qa-to-studio.md
goals/G-001-dash-damage/12-studio-to-technical-director.md
goals/G-001-dash-damage/13-technical-director-to-studio.md
goals/G-001-dash-damage/14-studio-to-gameplay-engineer.md
goals/G-001-dash-damage/15-gameplay-engineer-to-studio.md
goals/G-001-dash-damage/goal.md
project.md
sim/build-0.3.md
sim/build-0.4.md
sim/repo-notes.md
>>>END

<<<FILE @decision-titles
decisions/D-001-one-button-combat.md — D-001: Combat uses one attack button plus dash
decisions/D-002-resume-with-owner-observations.md — D-002: Owner の補足観察を受けて修正を継続する
decisions/D-003-independent-invulnerability.md — D-003: 無敵の終了を発生源ごとに管理する
>>>END

<<<FILE goals/G-001-dash-damage/goal.md
---
kind: goal
id: G-001
project: lantern-depths
status: active
created: 2026-10-10
---
# G-001: ダッシュ中の被ダメージ不具合を修正する

## Owner request

> ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。

## Interpretation

報告された被ダメージを再現し、仕様に反する挙動を修正して、ダッシュ時のダメージ判定が既存の仕様どおりに動くことを独立した検証で確認する。

戦闘の方向性変更、新しい入力の追加、無関係なバランス調整は対象外。

## Unknowns

- Observe: QA は既存仕様と模擬ビルドの記述から仕様不一致を確認し、不具合報告と AC-1〜AC-6 を作成した。Owner の詳細条件を独立した試行で再現したわけではない。追加 Observe は現時点では不要。
- Diagnose / Plan: technical-director が実装資料に基づき、共有無敵フラグを各タイマーが解除する競合を診断し、発生源別に保護を管理する修正計画を作成した。結果は `13-technical-director-to-studio.md`。実行による再現や修正は未実施。
- Decide: 既存仕様への修正に方向選択は不要。D-002 は不足入力を補完して継続する Owner の決定。D-003 は既存仕様を維持する技術方式の決定であり、ゲームの方向変更ではない。
- Design: QA によれば期待挙動と受け入れ条件は明確。入力不能中の予約入力や完全同時の境界処理は今回新たに定義しない。判断が必要になれば game-designer に戻す。
- Build: 計画と D-003 に従い模擬修正を具体化する。両ダメージ経路、再現用配置、既存クールダウン起点、試行資料を確認する。
- Verify: Build 後は必須。更新された模擬ビルドと観察資料を用い、AC-1〜AC-6 を PC・30 / 60 FPS・キーボード / ゲームパッドの全4組合せで独立検証する。
- Play: 体験や感触の改善依頼ではないため省略。
- Review: 体験 Goal やゲームの方向 Decision を伴わないため省略。
- Next: 検証後に Studio が Owner 向けの結果と残件をまとめる。

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | qa | reproduce-defect | done | 01-studio-to-qa.md |
| 1b | Observe | qa | reproduce-defect | done | 03-studio-to-qa.md |
| 1c | Observe | qa | reproduce-defect | done | 05-studio-to-qa.md |
| 1d | Observe | qa | reproduce-defect | done | 07-studio-to-qa.md |
| 1e | Observe | qa | reproduce-defect | done | 10-studio-to-qa.md |
| 2 | Diagnose / Plan | technical-director | technical-plan | done | 12-studio-to-technical-director.md |
| 3 | Decide | game-director | make-decision, prepare-owner-escalation | skipped | — |
| 4 | Design | game-designer | write-design-spec | skipped | — |
| 5 | Plan | technical-director | technical-plan | skipped | — |
| 6 | Build | gameplay-engineer | implement-change | open | 14-studio-to-gameplay-engineer.md |
| 7 | Verify | qa | verify-change | planned | — |
| 8 | Play | playtester | playtest-session | skipped | — |
| 9 | Review | game-director | review-outcome | skipped | — |
| 10 | Next | studio | — | planned | — |

過去の Observe の done は入力確認作業の終了を表し、再現確認の成功を表さない。1d の結果は `08-qa-to-studio.md`。1e の結果は `11-qa-to-studio.md`（outcome: done）であり、仕様不一致の照合と受け入れ条件の作成が完了した。行 2 の結果は `13-technical-director-to-studio.md`（outcome: done）であり、診断・計画の完了を表す。いずれも修正完了や Verify 合格ではない。独立した Plan 行 5 は行 2 に統合したため skipped。

## Route changes

2026-10-10 — `02-qa-to-studio.md`（question）を受領し、1 を done とした。再現条件不足により追加 Observe を設けた。期待挙動の仕様不足ではないという QA の報告を受け、Design を skipped とした。

2026-10-10 — `04-qa-to-studio.md`（question）を受領し、1b を done とした。補足資料が未提供のため、資料受領を開始条件とする 1c を設けた。

2026-10-10 — `06-qa-to-studio.md`（question）を受領し、1c を done とした。資料受領を開始条件とする 1d を設け、実行環境側の補完を待つ方針とした。当時は Owner escalation を行わなかった。

2026-10-10 — `08-qa-to-studio.md`（question）を受領し、1d を done とした。基本資料は補完されたが、繰り返し求めている補足観察資料と実行環境側の回答は未提供で、追加再現確認は未開始。同じ不足入力について新しい該当資料がないまま question が二回以上返ったため、loop limits を適用した。過去の再ルーティング方針を修正し、`09-studio-to-owner.md` に必要入力と選択肢をまとめ、Goal を blocked-on-owner とした。

2026-10-10 — Owner が Option A を選び、新しい観察を提供した。選択と回答原文を D-002 に記録し、09 を resolved、Goal を active とした。Observe 1e を追加し、`10-studio-to-qa.md` を open とした。体感による時刻や頻度を計測値とせず、部分資料から判断可能な範囲を QA に委ねた。

2026-10-10 — `11-qa-to-studio.md`（done）を受領し、1e を done とした。QA は不具合報告と AC-1〜AC-6 を作成し、追加の Owner 計測を必須とせず技術調査へ進めると報告した。Diagnose と Plan を technical-director の一つの Step に統合し、行 2 を `12-studio-to-technical-director.md` で open とした。行 5 は統合により skipped。Build と Verify は維持した。当時の packet にない実装資料・設計・Decision・契約・Skill の本文を読んだとは扱わず、次の Step の Load に指定した。

2026-10-10 — `13-technical-director-to-studio.md`（done）を受領し、行 2 を done とした。診断・計画が予定した Build の入力を満たすという担当の報告を受け、行 6 を `14-studio-to-gameplay-engineer.md` で open とした。D-003 に基づく方式と実装順序は technical-director の判断として引き継ぐ。実装は逐次、完了後に独立 QA の Verify を行う。視覚変更は計画にないため art-director の追加は不要。

新しい Owner escalation の根拠はない。本 Route packet には gameplay-engineer の Works from はあるが、契約全文・Skill・設計・実装資料・Decision・QA 報告の本文は含まれない。これらの内容を確認済みとは扱わず、次の Step packet に Load 資料として要求する。欠落や矛盾があれば具体的に報告し、推測で実装しない。

## Next action

新しい executor で gameplay-engineer が `14-studio-to-gameplay-engineer.md` とその Load 資料から Build を開始する。模擬修正の内容、変更対象、試し方、simulator が更新する資料と観察要件を Handoff に記し、結果を Studio に返す。

Studio はその結果と模擬資料の更新を確認してから、実装者の自己評価・理由を除いた入力で独立 QA に Verify を依頼する。本 Route では Build や Verify を実行しない。

## Outcome

未完了。QA による仕様不一致の確認と受け入れ条件の作成、technical-director による資料上の原因診断と修正計画が完了した。D-002 に基づき継続し、D-003 の発生源別無敵管理を Build に渡した。独立した詳細再現、修正、修正後の検証はまだ完了していない。現時点で Owner に新たな判断を求める事項はない。
>>>END

<<<FILE goals/G-001-dash-damage/15-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-001
seq: 15
from: gameplay-engineer
to: studio
stage: Build materialization
outcome: done
---
# 15: gameplay-engineer → studio — 発生源別の無敵管理を模擬実装し、資料更新を依頼する

## Task

以下の模擬実装変更を simulator に反映し、ビルド `0.3-G001-15` と QA 用観察資料を生成する。その後、実装理由と Sender assessment を除いた資料を新しい executor の QA に渡し、独立 Verify を依頼する。

## Context

G-001 はダッシュ中にダメージを受ける不具合の修正。提供された `studio/skills/implement-change.md` を適用し、仕様、AC-1〜AC-6、technical-director の計画、D-001〜D-003 の本文に従って変更を定義した。

本 Handoff の変更記述が dry-run の模擬実装となる。実コード、実機試験、自動テストの実行はない。simulator による資料更新と観察生成は未実施であり、更新済みビルドの存在や QA 合格を報告するものではない。

## Findings

### プレイヤーから見える変更と仕様の対応

| 挙動 | 根拠 |
|---|---|
| 先行被弾の有無によらず、ダッシュ全期間の接触・弾命中でハートを失わない | combat のダッシュ仕様、AC-1〜AC-3 |
| ダッシュ終了後も、先行被弾から0.8秒までの保護が残る | 被弾仕様、AC-4、D-003 |
| 防いだ命中でハート減少や入力不能を開始せず、保護時間を延長しない | D-003 |
| 両保護が終了すれば通常の被害が成立する | 被弾仕様、AC-5 |
| ダッシュ距離・時間・クールダウン、攻撃予約、通常被弾の量と時間を維持する | combat、AC-5〜AC-6 |

新しい入力やプレイヤー向けのルールは追加しない。

### 模擬実装変更

対象は `sim/repo-notes.md` の Player invulnerability と、それに接続するダッシュ、被弾、接触・弾命中の責務。ソースのファイル名や関数名は資料にないため指定しない。下記の状態名は今回の模擬実装で定義する名称である。

| 対象 | 変更後 |
|---|---|
| 無敵状態 | `dashProtectionActive` と `hitProtectionActive` を独立管理する。有効な無敵は両者の論理和。書き込み可能な旧共通フラグは廃止する |
| ダッシュ開始 | 既存のダッシュ開始が成立した時点でダッシュ保護だけを開始する。被弾保護とその終了時刻を変更しない |
| ダッシュ継続・終了 | 保護は既存のダッシュ継続状態に対応させる。既存の終了処理でダッシュ保護だけを解除する。保護専用の独立タイマーを追加しない |
| Grub 接触 | 接触によるプレイヤー被害を共通の被害入口に接続する。ハート減少・入力不能の適用前に有効な無敵を判定する |
| Spitter 弾命中 | 弾命中によるプレイヤー被害も同じ入口・同じ判定を使用する |
| 保護中の命中 | プレイヤー被害処理を終了する。ハート、入力不能、被弾保護の状態・終了時刻を変更しない。既存の弾の消滅等、被害以外の命中処理は変更しない |
| 保護なしの命中 | 既存どおり1ハート減少、0.3秒入力不能を適用する。被害成立時刻から0.8秒まで被弾保護を有効にする |
| 入力不能終了 | 既存どおり入力を回復する。被弾保護を解除しない |
| 被弾保護終了 | 被弾保護だけを解除する。ダッシュ保護を変更しない |
| 無敵の参照 | 旧共通フラグへの参照を論理和の参照に置換する。派生値を保持する場合も、各タイマーから直接書き換えない |

共通被害入口の判定順序は次のとおりとする。

1. 接触／弾命中が成立する。
2. `dashProtectionActive OR hitProtectionActive` を確認する。
3. 真ならプレイヤー被害を適用せず終了する。
4. 偽なら既存の通常被弾処理を適用し、被弾保護を開始する。

既存イベントの実行順序は変更しない。この順序指定は被害入口内の処理順序であり、同時刻のダッシュ開始・終了と命中の優先順位を新設するものではない。

旧操作の置換範囲は、ダッシュ開始の共通オン、ダッシュ終了の共通オフ、被害成立の共通オン、被弾タイマー終了の共通オフ、および無敵判定の全参照。両命中源に旧フラグを直接操作する迂回経路を残さない。提供資料にない操作箇所まで実コード検索で確認したという意味ではない。

既存の可変 delta time とタイマー機構を再利用する。ダッシュは4タイル・0.25秒、クールダウン0.6秒。クールダウンの既存起点、ダッシュ中の攻撃予約と終了時発動は変更しない。保存形式への変更は定義しない。

### simulator に依頼する資料更新

以下は生成先の指定であり、本 Step で作成済みのファイルではない。

| 資料 | 更新・生成先 | 内容・用途 |
|---|---|---|
| 開発者向け実装資料 | `sim/repo-notes.md` | 本変更、ビルド識別子、両命中経路、旧共通操作の置換を記録。他の実装項目は維持 |
| プレイヤー向け模擬ビルド | `sim/build-0.3-G001-15.md` | ビルド識別子、読み方、ダッシュ・接触・弾命中・通常被弾の観察可能な挙動。内部状態・原因・自己評価を含めない |
| QA 用試行資料 | `sim/qa-G001-15.md` | 下記シナリオの設定、実際に生成した模擬観察、無効試行、未確認項目を分離して記録 |

旧 `sim/build-0.3.md` は修正前の比較資料として識別する。新資料が未生成の間は旧資料を修正後の証拠として扱わない。

dry-run の実行・確認方法は、新ビルドの説明と QA 用試行資料を読むこと。実行コマンドは存在しない。simulator は期待結果をそのまま観察結果として転記せず、各条件の模擬イベントとハート変化を生成すること。生成できない項目は資料不足と記す。

### 試行の共通設定

全シナリオを PC の30 FPS・キーボード、30 FPS・ゲームパッド、60 FPS・キーボード、60 FPS・ゲームパッドで扱う。AC-1〜AC-4 は Grub 接触と Spitter 弾命中を独立試行にする。AC-1 はさらに前半・後半を分ける。

以下は新しく用意する試行配置の指定であり、既存の部屋座標や観察済み配置ではない。

- Grub 試行は部屋1〜2の壁に遮られない直線区間を使う。ダッシュ始点を基準点、進行方向を正方向として、4タイルの経路とその先に通常被弾を確認できる余地を確保する。
- 先行被弾なしの試行では対象 Grub を1体、先行被弾ありでは初回被弾用と評価対象の Grub を各1体とする。初回被弾用が予定外の再接触を起こさない配置を選ぶ。
- 弾試行は混在部屋の開けた区間で Spitter を1体使い、先行被弾が必要な場合は Grub を1体加える。既存の発射間隔2秒、弾速、AIを変えず、発射位相と初期位置で評価時刻に弾道がプレイヤーと交差するよう設定する。
- 他の敵・弾が予定外に干渉した場合は、そのイベントも記録し、条件を満たさない試行を無効とする。
- 各試行はダッシュ使用可能、保護なし、入力可能から開始する。初期ハート `H` は既存仕様で実在する値を使い、予定被弾で死亡しない状態を選ぶ。最大ハート数は新設しない。
- 具体的な座標、当たり判定寸法、敵の移動速度は資料にない。simulator は実際に用いたプレイヤー・敵の座標、向き、弾の発射位置・時刻・経路を記録し、再読可能な配置にする。これらを生成できない場合は配置未確定と報告する。

攻撃が通り過ぎただけの試行を保護成功に数えない。接触または弾の当たり判定が成立した記録が必要である。

### AC ごとの入力・命中設定

`t` は先行被弾成立からの予定経過秒、`d` は実際のダッシュ開始時刻。下表の数値は試行の目標であり、観察結果ではない。

| ID | 操作・命中の目標 | 期待するハートと確認点 |
|---|---|---|
| AC-1 前半 | 先行被弾なしでダッシュ入力。`d+0.07秒`付近に接触／弾命中を配置 | `H→H`。実際の開始後かつ終了前であること |
| AC-1 後半 | 別試行で`d+0.18秒`付近に接触／弾命中を配置 | `H→H`。前半だけの確認で代用しない |
| AC-2 | t=0で通常被弾。0.3秒の入力不能終了を観察した最初の入力可能な機会にダッシュ入力。`d+0.10秒`付近で命中 | 初回`H→H−1`、評価命中`H−1→H−1`。入力不能中の予約を使わない |
| AC-3 | t=0で被弾、t=0.70付近にダッシュ開始、t=0.85付近に命中 | 初回以外の減少なし。実際に「被弾保護終了 < 命中 < ダッシュ終了」が成立すること |
| AC-4 | t=0で被弾、入力可能になってからt=0.34付近にダッシュ開始、t=0.70付近に命中 | 初回以外の減少なし。実際に「ダッシュ終了 < 命中 < 被弾保護終了」が成立すること |
| AC-5 | 保護なしで Grub 接触。追加接触をt=0.15、0.45、0.70付近に設定。入力不能中と終了後の既存入力の受理状況を記録 | 初回のみ`H→H−1`。0.3秒入力不能、終了後の入力回復、0.8秒まで追加減少なし |
| AC-6 | 敵・壁に干渉しない直線でダッシュ。`d+0.10秒`付近で攻撃を一度入力。クールダウン内と終了後の再入力は別試行で行う | 4タイル、論理時間0.25秒。攻撃は途中発動せず終了時に一度。既存起点から0.6秒の再使用制限を維持 |

AC-6 のクールダウン試行は、既存の起点を `c` と記録できた後に、`c+0.50秒`付近と`c+0.70秒`付近の入力を設定する。起点をダッシュ開始または終了と仮定しない。既存起点が資料化できなければ、この項目は未確認として戻す。

### 追加回帰

次を全4環境、Grub／Spitter の別試行で用意する。

1. **被弾保護が先に終了:** AC-3の配置でダッシュ中の命中を防ぎ、両保護終了後のt=1.10付近に別の命中を置く。期待は後者のみ1ハート減少。
2. **ダッシュ保護が先に終了:** AC-4の配置でダッシュ終了後の命中を防ぎ、両保護終了後のt=0.95付近に別の命中を置く。期待は後者のみ1ハート減少。
3. **防いだ命中による延長なし:** 上記に加え、被弾保護終了前またはダッシュ終了前に、異なるフレームで少なくとも2回の成立した命中を配置する。元の保護終了後の命中で通常被害が成立することを確認する。命中回数が不足した試行はこの回帰の証拠にしない。
4. **ダッシュのみの解除:** 先行被弾なしでダッシュ中に複数命中を防ぎ、終了後の`d+0.40秒`付近に命中を置く。期待は終了後に1ハート減少。防いだ命中が被弾保護を新規開始していないことも確認する。

複数の弾・接触が必要な配置は既存の敵挙動で成立させる。成立しない場合は時刻や配置を調整して記録し、敵の発射頻度や攻撃仕様を変更しない。

### 記録形式と有効性

試行IDを `G001-15/<ACまたは回帰>/<FPS>/<入力>/<命中源>/<枝>/<連番>` とする。各セルについて少なくとも1件の有効な模擬試行を生成することを依頼する。これは予定件数であり、実施数ではない。

各試行に次を残す。

- 対象ビルド、AC、環境、部屋、全敵の種類・数・位置、プレイヤー位置・向き・ダッシュ方向、初期ハート、保護・クールダウンの初期状態。
- 計画時刻と実際の模擬イベント時刻を別欄にする。各イベントのフレーム番号、delta time、同一フレーム内の処理順番号を記録する。
- 初回被害、入力不能開始・終了、入力操作・受理、ダッシュ開始・終了、各接触／命中、ハート前後値、攻撃入力・発動、再使用可能時刻。
- 被弾後0.8秒の論理基準点、ダッシュの論理終了時刻と観察フレーム、実際の前後関係。
- 移動始点・終点、距離、継続時間、クールダウン起点と終了、攻撃発動回数。
- 試行総数、有効数、無効数、条件を満たす試行での被害発生数。無効理由と再試行の対応。

30 FPSでは0.25秒が整数フレームに一致しない。論理時間と観察フレームを併記し、丸めによる独自の許容誤差を設けない。同時境界、命中不成立、予定外の先行被弾、AC-3／AC-4の順序不成立は該当条件の有効試行に含めず、配置や入力時刻を調整する。

## Decisions already made

- D-001: 攻撃・ダッシュ・ポーズ以外の入力を追加しない。
- D-002: Owner の部分的観察を使って元の修正 Goal を継続する。追加計測を開始条件にしない。
- D-003: 無敵を発生源別に管理し、論理和で判定する。防いだ命中で保護を延長しない。

## Constraints

戦闘の方向性、バランス、敵 AI、Flinch、移動・壁、攻撃の威力・硬直を変更しない。固定フレーム数への置換、ダッシュ保護専用の別タイマー、保存形式変更は行わない。実装は並列化しない。

入力不能中の予約、完全同時イベントの優先順位、クールダウン起点の新仕様を決めない。判断が不可欠な具体例が出た場合は Studio 経由で game-designer に戻す。

プレイヤー向け資料に実装資料や自己評価を混在させない。QA には期待と観察を分離して渡す。Build の自己確認は独立 QA の合格を代替しない。

## Open questions

模擬実装変更を定義するための必須資料不足はない。次の事項は資料生成時に確認する必要がある。

- 各 FPS で命中が成立する正確な配置、発射位相、実際のイベント順序。
- 既存クールダウン起点。資料から復元できなければ推測せず AC-6 の不足として返す。
- 更新ビルドと観察資料が指定識別子に対応して生成されたか。
- 提供資料にない保存・復元やダッシュ中断が判明した場合の影響。その場合は対象部分を止め、technical-director に再計画を求める。

これらの未確認事項を観察済みとして埋めない。仕様判断や計画変更が必要になった場合は、解決前に QA へ完成品として渡さない。

## Expected output

Studio は simulator に本変更と資料生成を依頼し、更新ビルド、全 AC・全4環境・必要命中源の観察資料を揃える。不足した資料は具体的な条件を付けて補完または差し戻す。

その後、仕様・AC・更新ビルド・観察資料を新しい executor の QA に渡す。原因説明、実装理由、Sender assessment は除外する。QA は不足を合格で補わず、独立した Verify 結果を Studio に返す。

## Sender assessment

提供資料上の原因は、二つの終了処理が共通フラグを解除し、他方の保護まで失わせること。今回の変更は両終了順序を同じ発生源別管理で扱い、片方だけを修正する方式にはしていない。

自己確認は文書照合のみ実施した。D-003 の各項目に対応する変更、両命中経路、旧操作の置換、AC-1〜AC-6、解除漏れと延長防止の回帰条件が記載されていることを確認した。承認済み仕様との文面上の整合は確認したが、挙動の合格判定はしていない。

コード実行、自動テスト、実機計測、新しい再現試行、simulator 観察生成は未実施。正確な配置、イベントログ、クールダウン起点は未確認。保存互換性への影響も資料から有無を断定できない。変更記述は完了しているが、実行結果の信頼性は後続資料と独立 QA で確認する必要がある。

## Load

- Project: project.md#vision
- Project: project.md#current-state
- Project: project.md#constraints
- Project: design/combat.md
- Project: sim/repo-notes.md
- Project: sim/build-0.3.md
- Project: goals/G-001-dash-damage/11-qa-to-studio.md
- Project: goals/G-001-dash-damage/13-technical-director-to-studio.md
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-resume-with-owner-observations.md
- Decisions: decisions/D-003-independent-invulnerability.md
- Previous handoff: goals/G-001-dash-damage/14-studio-to-gameplay-engineer.md
>>>END

## Validation feedback

A previous executor's output was rejected for these reasons. Produce the operation's files again, fixing them:

- goals/G-001-dash-damage/16-studio-to-qa.md: Load entry missing: sim/build-0.3-G001-15.md
- goals/G-001-dash-damage/16-studio-to-qa.md: Load entry missing: sim/qa-G001-15.md
