# Studio operation packet

operation: Route
goal: G-001
step_artifact: goals/G-001-dash-damage/13-technical-director-to-studio.md
next_seq: 14

## You may write

- goals/G-001-dash-damage/goal.md
- goals/G-001-dash-damage/13-technical-director-to-studio.md (in place: keep kind, goal, seq, from, to)
- goals/G-001-dash-damage/14-studio-to-<role>.md

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
goals/G-001-dash-damage/goal.md
project.md
sim/build-0.3.md
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

- Observe: QA は既存仕様と模擬ビルドの記述から仕様不一致を確認し、不具合報告と AC-1〜AC-6 を作成した。Owner の詳細条件を独立した試行で再現したわけではなく、安定再現の配置・時刻・発生境界は未確定。追加 Observe は現時点では不要。
- Diagnose / Plan: 実装原因と修正箇所は未確認。technical-director が実装資料を調べ、既存仕様を維持する修正計画と、後続の模擬検証に必要な資料を定める。同じ担当・入力で扱えるため一つの Step にまとめる。
- Decide: 既存仕様への修正に方向選択は不要。D-002 は不足入力を補完して修正を継続する Owner の決定であり、ゲームの方向変更ではない。
- Design: QA によれば期待挙動と受け入れ条件は明確。入力不能中の予約入力や完全同時の境界処理は今回新たに定義しない。判断が必要になれば game-designer に戻す。
- Build: 技術調査・計画の結果を受け、修正を実施する。
- Verify: Build 後は必須。AC-1〜AC-6 を PC・30 / 60 FPS・キーボード / ゲームパッドの全4組合せで独立検証する。
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
| 2 | Diagnose / Plan | technical-director | technical-plan | open | 12-studio-to-technical-director.md |
| 3 | Decide | game-director | make-decision, prepare-owner-escalation | skipped | — |
| 4 | Design | game-designer | write-design-spec | skipped | — |
| 5 | Plan | technical-director | technical-plan | skipped | — |
| 6 | Build | gameplay-engineer | implement-change | planned | — |
| 7 | Verify | qa | verify-change | planned | — |
| 8 | Play | playtester | playtest-session | skipped | — |
| 9 | Review | game-director | review-outcome | skipped | — |
| 10 | Next | studio | — | planned | — |

過去の Observe の done は入力確認作業の終了を表し、再現確認の成功を表さない。1d の結果は `08-qa-to-studio.md`。1e の結果は `11-qa-to-studio.md`（outcome: done）であり、仕様不一致の照合と受け入れ条件の作成が完了した。修正完了や Verify 合格ではない。独立した Plan 行 5 は行 2 に統合したため skipped とし、計画作成自体は省略しない。

## Route changes

2026-10-10 — 初回 Observe の結果 `02-qa-to-studio.md`（outcome: question）を受領し、1 を done とした。再現条件が不足しているため追加 Observe を設けた。期待挙動の仕様不足ではないという QA の報告を受け、Design を skipped とした。

2026-10-10 — `04-qa-to-studio.md`（outcome: question）を受領し、1b を done とした。補足資料が未提供のため、資料受領を開始条件とする 1c を設けた。

2026-10-10 — `06-qa-to-studio.md`（outcome: question）を受領し、1c を done とした。資料受領を開始条件とする 1d を設け、実行環境側の補完を待つ方針とした。当時は Owner escalation を行わなかった。

2026-10-10 — `08-qa-to-studio.md`（outcome: question）を受領し、1d を done とした。QA Role・Skill 等の基本資料は補完されたが、繰り返し求めている補足観察資料と実行環境側の回答は依然未提供で、追加再現確認は未開始。

同じ不足入力について、新しい該当資料がないまま question が二回以上返った場合は Role に再投入せず Owner にエスカレーションするという `studio/orchestration.md#loop-limits` を適用した。基本資料の補完は、当該観察資料の不足解消には当たらない。過去の待機・再ルーティング方針を修正し、`09-studio-to-owner.md` に必要入力と選択肢をまとめ、Goal を blocked-on-owner とした。提供不能とは断定せず、Build や検証合格へ進めなかった。

2026-10-10 — Owner が Option A を選び、新しい観察を提供した。選択と回答原文を `decisions/D-002-resume-with-owner-observations.md` に記録し、09 を resolved、Goal を active とした。Option A の帰結に従い Observe 1e を追加し、`10-studio-to-qa.md` を open とした。体感による時刻や頻度を計測値とせず、部分資料から判断可能な範囲を QA に委ねる。

2026-10-10 — `11-qa-to-studio.md`（outcome: done）を受領し、1e を done とした。QA は修正へ渡せる不具合報告と AC-1〜AC-6 を作成し、追加の Owner 計測を必須とせず技術調査へ進めると報告した。原因・変更箇所は未確認のため Diagnose と Plan の必要性を確定し、technical-director の一つの Step に統合した。行 2 を `12-studio-to-technical-director.md` で open とし、独立した行 5 は統合により skipped とした。Build と Verify は維持する。

現時点では Owner escalation の新しい根拠はない。技術担当が調査できる未解決事項を Owner に戻さず、同じ資料で QA Observe を繰り返さない。本 Route packet に実装資料・設計・Decision の本文、technical-director の契約全文と Skill 本文は含まれないため、それらを読んだとは扱わない。次の Step packet に Load 資料を含め、欠落があれば具体的な不足を報告する。

## Next action

新しい executor で technical-director が `12-studio-to-technical-director.md` とその Load 資料から技術調査・計画を開始する。実装原因、変更箇所、修正手順、AC-1〜AC-6 の模擬検証に必要な資料を整理し、結果を Studio に返す。

次の packet には特に `sim/repo-notes.md`、`design/combat.md`、`sim/build-0.3.md` と関連 Decision の本文を含める。資料が欠ける場合は内容を推測せず、欠落と進められる範囲を報告する。

## Outcome

未完了。QA は既存仕様と模擬ビルドの記述の不一致を確認し、修正の受け入れ条件を作成した。D-002 に基づく継続方針のもと、次は技術調査・計画を行う。独立した詳細再現、修正、修正後の検証はまだ完了していない。現時点で Owner に新たな判断を求める事項はない。
>>>END

<<<FILE goals/G-001-dash-damage/13-technical-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 13
from: technical-director
to: studio
stage: Build routing
outcome: done
---
# 13: technical-director → studio — 無敵の競合解除を分離する修正計画

## Task

本計画と D-003 を gameplay-engineer に渡し、Build に進める。Build の変更を反映した模擬資料を用意した後、独立した QA に AC-1〜AC-6 の Verify を依頼する。

## Context

G-001 はダッシュ中に被害が発生する不具合の修正である。D-002 により Owner の部分的な観察を使って継続している。

本 Step は提供された `studio/skills/technical-plan.md` を適用し、仕様、実装資料、模擬ビルド、QA 報告を照合した。実リポジトリは存在せず、コード実行・新しい再現試行・修正は行っていない。以下の時刻例は検証用の予定条件であり、測定結果ではない。

## Findings

### 診断と根拠

`sim/repo-notes.md` の Player invulnerability には、次の実装が明記されている。

1. 無敵は一つのオン／オフフラグ。
2. ダッシュがフラグをオンにし、0.25 秒タイマーを開始する。
3. 被弾もフラグをオンにし、被弾から 0.8 秒で終了するタイマーを開始する。
4. 各タイマーは終了時に共通フラグをオフにする。

この構造では、一方のタイマー終了が他方の保護を解除する。実装資料に根拠のある原因であり、単に Owner の時刻の重なりから推測したものではない。

たとえば被弾時刻を t=0、ダッシュ開始を t=0.70 とすると、仕様上のダッシュ終了は t=0.95 となる。現方式では t=0.80 に被弾タイマーが共通フラグをオフにするため、t=0.85 の命中を防げなくなる。この順序は Owner の「待ってからダッシュし、後半に被害」と整合する。ただし実際の配置やフレーム処理順序を含む再現は未実施であり、Owner の発生率や Spitter の一例まで実証したものではない。

逆順の欠陥も導ける。入力不能終了後、たとえば t=0.34 にダッシュを開始すると終了予定は t=0.59。現方式ではこの終了が、t=0.80 まで残るべき被弾由来の保護を消す。これは資料から導いた AC-4 の回帰対象であり、新たな観察済み不具合としては扱わない。

### 変更箇所と順序

実装資料にファイル名・関数名はないため、以下は変更する責務の指定である。架空のソースパスを作らず、Build Handoff では対応する模擬実装項目を明示する。

| 順序 | 対象 | 変更・確認内容 |
|---|---|---|
| 1 | プレイヤー無敵とダメージ入口 | 現在の共通フラグの設定・解除・参照箇所を整理する。Grub 接触と Spitter 弾の双方が新しい判定を利用することを確認する |
| 2 | 無敵状態 | ダッシュ由来と被弾由来を分離する。有効な無敵は `dashProtectionActive OR hitProtectionActive` とし、共通値を残す場合もこの派生値だけにする |
| 3 | ダッシュ開始・終了 | 既存のダッシュの開始・終了に保護を結び付ける。開始・終了で被弾由来の状態を変更しない |
| 4 | 被弾処理・タイマー終了 | 実際の被害成立で 1 ハート減少、0.3 秒入力不能、被弾後 0.8 秒までの保護を開始する。タイマー終了は被弾由来の状態だけを解除する |
| 5 | 全ダメージ経路 | 接触・弾命中とも、被害や入力不能を適用する前に有効な無敵を確認する。防いだ命中で被害処理や保護時間の再開始を行わない |
| 6 | 回帰確認・模擬資料更新依頼 | 下記の検証条件、変更後の挙動と証拠の要件を Build Handoff に正確に記載し、simulator に反映させる |

時間は既存の可変 delta time に従って処理し、フレーム数を固定値として無敵時間に置き換えない。ダッシュが継続中なのに保護だけが先に切れる独立タイマーを追加しない。

ダッシュは 4 タイル・0.25 秒・クールダウン 0.6 秒、ダッシュ中の攻撃入力は終了時発動を維持する。移動、壁、敵 AI、敵の Flinch、攻撃の威力・硬直は変更しない。既存のクールダウン起点は資料に明記されていないため、起点を新しく決定しない。

### 検証条件

全条件を PC の「30 FPS・キーボード」「30 FPS・ゲームパッド」「60 FPS・キーボード」「60 FPS・ゲームパッド」で評価する。以下の t は各試行の初回被弾からの予定経過秒であり、実際のフレーム時刻とは区別する。

| AC | 設定・確認手順 | 必要な観察 |
|---|---|---|
| AC-1 | 先行被弾なし、ダッシュ使用可能な状態で開始。ダッシュ前半・後半の接触と弾命中を別試行で確認 | 実際のダッシュ開始・終了、保護期間内の接触／命中、前後のハート不変 |
| AC-2 | 被弾後、入力不能終了を確認した最初の入力可能な機会にダッシュ。入力不能中の予約は使わない | 入力不能終了、入力受理、実際のダッシュ開始、期間内の接触／命中とハート不変 |
| AC-3 | t=0.70 開始、t=0.85 命中、t=0.95 終了予定を候補にする | 実際に「被弾後 0.8 秒経過 < 命中 < ダッシュ終了」が成立し、ハート不変 |
| AC-4 | 入力不能終了後の t=0.34 開始、t=0.59 終了、t=0.70 命中を候補にする | 実際に「ダッシュ終了 < 命中 < 被弾後 0.8 秒」が成立し、ハート不変 |
| AC-5 | 保護のない状態で Grub 接触。その後、入力不能中とその終了後から t=0.8 までに追加接触を設定 | 初回 1 ハート減少、0.3 秒入力不能、その後の入力回復、無敵期間内の追加被害なし |
| AC-6 | 壁のない直線でダッシュ。期間中に一度攻撃入力。クールダウン内・経過後の再入力を確認 | 4 タイル移動、0.25 秒継続、0.6 秒クールダウン、予約攻撃が途中で発動せず終了時に一度発動 |

AC-1〜AC-4 は Grub 接触と Spitter 弾命中の両方を、それぞれ独立した試行として記録する。各試行はダッシュ使用可能・既存の保護なしの初期状態から始め、先行被弾が必要な場合はその被害成立を記録する。

追加回帰として、両方の保護が終了した後に別の攻撃を受け、通常の被害が成立することを確認する。これにより無敵の解除漏れを検出する。短時間に防いだ命中を複数回配置しても保護が延長されないことも確認する。

時刻例は完全同時の命中を避けた設定である。各 FPS で実際に成立した順序を記録し、条件を満たさなければ配置や予定時刻を調整して再試行する。丸めだけで条件成立や合格としない。0.25 秒などがフレーム境界に一致しない場合は、論理上の時間と観察フレームの両方を示す。許容誤差や同時イベントの新仕様はここでは定めない。

### 安定した試行と模擬資料の要件

Build は Handoff に「何を、どこで、どう変更し、どう試すか」を記載し、実行環境の simulator が `sim/` を更新する。technical-director は本 Step で `sim/` を変更しない。

更新する資料には次の情報が必要である。

- **実装資料:** 発生源別の状態、開始・終了の操作、有効な無敵の判定、両ダメージ経路への適用、旧共通フラグの直接解除を除去したこと。
- **プレイヤー向け模擬ビルド:** 更新対象を識別できるビルド識別子と、接触・弾命中時、ダッシュ時、通常被弾時の観察可能な挙動。内部実装の説明を混在させない。
- **QA 用の試行資料:** 各 AC・環境・命中源について、条件と実際の観察を対応させた記録。期待結果だけの表を実行結果の代用にしない。

試行記録に必要な項目：

1. 試行 ID、対象ビルド、AC、FPS、入力方式、試行回数と発生数。
2. 部屋、敵の種類・数・位置、プレイヤー位置・向き、ダッシュ方向、初期ハート、クールダウンと保護の初期状態。Spitter は発射時刻と弾の経路も記載する。
3. 初回被害成立、入力不能開始・終了、入力操作と受理、ダッシュ開始・終了、攻撃入力・発動、再使用可能になる時刻。
4. 各接触／弾命中の時刻、フレーム、同一フレーム内の順序、ハートの前後値。無敵で被害を防いだ場合にも接触／命中が成立した証拠を残す。
5. 計画時刻と実際のイベント時刻の区別。初回被弾から 0.8 秒の基準点、ダッシュ終了との前後関係。
6. 移動の始点・終点とタイル距離、ダッシュ継続時間、クールダウンの既存起点・終了、攻撃発動回数。
7. 「仕様からの期待」「simulator が生成した観察」「未実施／資料不足」の区別。実機測定や Owner の追加観察を装わない。

接触が成立しなかった試行や、AC-3 の命中が実際にはダッシュ終了後だった試行は、該当 AC の有効な試行数に含めない。再現用配置を Build／simulator が具体化し、QA が同条件を読み取れる形にする。現資料から配置座標や実施回数を創作しない。

### テスト戦略とリスク

既存テストはない。後続で状態遷移を自動確認できる場合は、「被弾保護が先に終了」「ダッシュ保護が先に終了」「両方終了」「防いだ命中はタイマーを延長しない」を最小の回帰項目とする。dry-run ではこれらを試行資料の明示的な検証シナリオとして扱い、実行可能なテストを走らせたとは報告しない。

独立 QA は全4環境の観察資料から AC を評価する。Build の自己確認は QA 合格の代わりにならない。

| リスク | 対策 |
|---|---|
| 古いタイマーや一部の命中経路が共通フラグを操作し続ける | 全設定・解除・参照箇所を Build で整理し、両命中源と両終了順序を確認 |
| 保護が永久に残る、または命中で延長される | 両保護終了後の通常被弾と、防いだ連続命中を回帰確認 |
| 可変 delta time による順序差 | 30 / 60 FPS ごとに実時刻と処理順序を記録し、境界同時命中を避ける |
| ダッシュ終了の変更が攻撃予約や移動へ影響する | 既存ライフサイクルを再利用し、AC-6 を全環境で確認 |
| 資料にないクールダウン起点や境界仕様を補ってしまう | 既存動作を保存し、判断が必要なら Studio 経由で game-designer に返す |

追加の状態と論理和は一定量の処理で、大規模な性能変更を必要としない。性能を実測したわけではない。保存形式への変更は計画に含めない。該当状態が保存対象だと Build で判明した場合は互換性の影響を報告して計画を再評価する。

**並列化:** 実装は並列化しない。無敵状態・タイマー・両命中経路が同じ判定に依存し、分担による不整合のリスクが利益を上回る。小規模な一連の修正として Build を行い、その後に独立 Verify を置く。

## Decisions already made

- D-001: 攻撃・ダッシュ・ポーズ以外の入力を Owner 承認なく追加しない。
- D-002: Owner の部分的な観察を使い、元の修正 Goal を継続する。
- D-003: 無敵の発生源を分離し、論理和で有効な保護を判定する。既存の時間・入力仕様は変更しない。

## Constraints

- 本 Step は診断と修正計画の完了であり、Build 完了・QA 合格ではない。
- 戦闘の方向性、バランス、敵の挙動、新しい入力を変更しない。
- 入力不能中の予約入力、ダッシュ開始・終了と命中が完全同時の場合の優先順位を決めない。
- QA に必要な観察資料と開発者向け実装資料を区別する。Playtester に実装資料を渡さない。
- Owner の体感値、仕様からの予定条件、模擬実装上の推論、後続の観察結果を区別する。

## Open questions

Build を阻止する必須資料の不足はない。追加の Owner 計測を要求せずに進められる。

Build で具体化する事項は、再現用配置、実際のフレーム内イベント順序、両命中経路の判定接続、既存クールダウン起点である。現資料にない実装上の事情が本方式を妨げる場合は、推測で補わず Studio に返す。

仕様上の完全同時イベントの優先順位や入力不能中の予約を決めなければ修正できないと判明した場合は、具体的な競合例を添えて game-designer に戻す。

## Expected output

Studio は gameplay-engineer に本計画、D-003、仕様・実装資料を渡して Build を依頼する。Build Handoff は変更内容と模擬資料の更新・試行要件を具体化する。

更新後、独立 QA が AC-1〜AC-6 を全4環境で Verify する。観察結果が欠ける条件は合格とせず、不足または失敗として返す。修正 Goal の完了判断はこの計画だけでは行わない。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: project.md#vision
- Project: project.md#current-state
- Project: project.md#constraints
- Project: design/combat.md
- Project: sim/repo-notes.md
- Project: sim/build-0.3.md
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-resume-with-owner-observations.md
- Decisions: decisions/D-003-independent-invulnerability.md
- Project: goals/G-001-dash-damage/11-qa-to-studio.md
- Previous handoff: goals/G-001-dash-damage/12-studio-to-technical-director.md
>>>END
