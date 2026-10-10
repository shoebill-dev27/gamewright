# Studio operation packet

operation: Route
goal: G-001
step_artifact: goals/G-001-dash-damage/17-gameplay-engineer-to-studio.md
next_seq: 18

## You may write

- goals/G-001-dash-damage/goal.md
- goals/G-001-dash-damage/17-gameplay-engineer-to-studio.md (in place: keep kind, goal, seq, from, to)
- goals/G-001-dash-damage/18-studio-to-<role>.md

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
goals/G-001-dash-damage/16-studio-to-gameplay-engineer.md
goals/G-001-dash-damage/17-gameplay-engineer-to-studio.md
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
- Diagnose / Plan: technical-director が共有無敵フラグの解除競合を診断し、発生源別に保護を管理する計画を作成した。結果は `13-technical-director-to-studio.md`。
- Decide: 既存仕様への修正に方向選択は不要。D-002 は不足入力を補完して継続する Owner の決定。D-003 は既存仕様を維持する技術方式の決定。
- Design: QA によれば期待挙動と受け入れ条件は明確。入力不能中の予約入力や完全同時の境界処理は今回新たに定義しない。判断が必要になれば game-designer に戻す。
- Build: `15-gameplay-engineer-to-studio.md` に模擬実装変更を定義済み。指定された生成先は存在一覧にない一方、`sim/build-0.4.md` が存在する。既存資料と変更記述の対応、検証に使える観察資料、残る不足を gameplay-engineer が照合する必要がある。
- Verify: Build 後は必須。仕様・AC-1〜AC-6・対応が確認された更新ビルド・観察資料から、PC・30 / 60 FPS・キーボード / ゲームパッドの全4組合せを独立検証する。未生成の資料を Load に指定しない。
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
| 6 | Build | gameplay-engineer | implement-change | done | 14-studio-to-gameplay-engineer.md |
| 6b | Build 資料照合・補完 | gameplay-engineer | implement-change | open | 16-studio-to-gameplay-engineer.md |
| 7 | Verify | qa | verify-change | planned | — |
| 8 | Play | playtester | playtest-session | skipped | — |
| 9 | Review | game-director | review-outcome | skipped | — |
| 10 | Next | studio | — | planned | — |

過去の Observe の done は入力確認作業の終了を表し、再現確認の成功を表さない。1d の結果は `08-qa-to-studio.md`。1e の結果は `11-qa-to-studio.md`（done）であり、仕様不一致の照合と受け入れ条件の作成が完了した。行 2 の結果は `13-technical-director-to-studio.md`（done）。独立した Plan 行 5 は行 2 に統合したため skipped。

行 6 の結果は `15-gameplay-engineer-to-studio.md`（done）。変更記述を模擬実装とするプロジェクト規約に従う完了であり、simulator の資料生成や独立 Verify の合格を意味しない。

## Route changes

2026-10-10 — `02-qa-to-studio.md`（question）を受領し、1 を done とした。再現条件不足により追加 Observe を設けた。期待挙動の仕様不足ではないという QA の報告を受け、Design を skipped とした。

2026-10-10 — `04-qa-to-studio.md`（question）を受領し、1b を done とした。補足資料が未提供のため、資料受領を開始条件とする 1c を設けた。

2026-10-10 — `06-qa-to-studio.md`（question）を受領し、1c を done とした。資料受領を開始条件とする 1d を設け、実行環境側の補完を待つ方針とした。当時は Owner escalation を行わなかった。

2026-10-10 — `08-qa-to-studio.md`（question）を受領し、1d を done とした。同じ不足入力について新しい該当資料がないまま question が二回以上返ったため、loop limits を適用した。`09-studio-to-owner.md` に必要入力と選択肢をまとめ、Goal を blocked-on-owner とした。

2026-10-10 — Owner が Option A を選び、新しい観察を提供した。選択と回答原文を D-002 に記録し、09 を resolved、Goal を active とした。Observe 1e を追加した。体感による時刻や頻度を計測値とせず、部分資料から判断可能な範囲を QA に委ねた。

2026-10-10 — `11-qa-to-studio.md`（done）を受領し、1e を done とした。QA は不具合報告と AC-1〜AC-6 を作成し、追加の Owner 計測を必須とせず技術調査へ進めると報告した。Diagnose と Plan を行 2 に統合し、行 5 は skipped とした。Build と Verify は維持した。

2026-10-10 — `13-technical-director-to-studio.md`（done）を受領し、行 2 を done、行 6 を open とした。D-003 に基づく方式と実装順序を technical-director の判断として引き継いだ。実装は逐次、完了後に独立 QA の Verify を行う。視覚変更は計画にないため art-director の追加は不要。

2026-10-11 — `15-gameplay-engineer-to-studio.md`（done）を受領し、行 6 を done とした。模擬実装の定義は完了したが、指定生成先 `sim/build-0.3-G001-15.md` と `sim/qa-G001-15.md` は存在一覧になく、検証入力が揃ったとは判断できない。一方、一覧には `sim/build-0.4.md` がある。ファイル名だけで変更反映や観察内容を断定せず、行 6b を追加して gameplay-engineer に既存資料の照合・補完を依頼する。これは受け入れ条件の再失敗に対する修正ではなく、Build の検証入力を整える作業である。Verify は planned のまま維持する。

本 Route は既存ファイルの一覧を確認した範囲に限る。設計、Decision、QA 報告、計画、sim 資料の本文を確認済みとは扱わない。次の Step は存在する資料を Load し、内容から対応関係と不足を報告する。生成予定の二つのパスは Load に入れない。現時点では、どの Role も不足を解消できないと確定していないため、新しい Owner escalation は行わない。

## Next action

gameplay-engineer が `16-studio-to-gameplay-engineer.md` とその Load 資料から、既存の `sim/build-0.4.md`・`sim/repo-notes.md` と変更記述を照合する。実在する検証入力、ビルド対応、不足項目、必要な simulator 更新を具体化して Studio に返す。

Studio は結果を受け、仕様・AC・更新ビルド・観察資料を揃えて独立 QA に Verify を依頼する。その入力から実装理由と自己評価を除外する。本 Route では Build の補完や Verify を実行しない。

## Outcome

未完了。仕様不一致の確認、受け入れ条件、技術計画、模擬実装変更の定義が完了した。D-002 に基づき継続し、D-003 の発生源別無敵管理を変更記述に反映した。更新ビルドと観察資料の対応確認、および独立 QA の検証が残っている。現時点で Owner に新たな判断を求める事項はない。
>>>END

<<<FILE goals/G-001-dash-damage/17-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-001
seq: 17
from: gameplay-engineer
to: studio
stage: Verification input resolution
outcome: question
---
# 17: gameplay-engineer → studio — 変更反映を識別、試行資料と既存動作の不足を差し戻す

## Task

既存の `sim/build-0.4.md` を変更 `0.3-G001-15` の模擬ビルドとして採用する。独立 Verify に不足する試行資料について、simulator が利用できる既存モデルの有無を確認し、生成不能なら technical-director に検証計画の成立性を戻す。

## Context

`studio/skills/implement-change.md` を適用し、Handoff 15 の変更記述と、今回提供された実装資料・模擬ビルドを照合した。追加の実装変更やプレイヤー向け挙動は定義していない。

読んだ資料は、Handoff 16、Role・Skill、project の vision・constraints、combat、repo-notes、build-0.3、build-0.4、Handoff 11・13・15、D-001〜D-003。本作業は提供文書の照合であり、コード実行、実機計測、自動テスト、simulator による新規試行生成ではない。

変更の反映は文書上で確認できる。一方、全条件を評価する試行資料と既存クールダウン起点が不足しているため、検証入力の完成としては返せない。独立 QA の pass / fail は判定しない。

## Findings

### ビルドと変更の対応

| 資料 | 明示された識別 | Handoff 15 との対応・不一致 |
|---|---|---|
| `sim/repo-notes.md` | 表題 build 0.4、Implemented change identifier `0.3-G001-15`。現ビルドを `sim/build-0.4.md` と指定 | 発生源別状態、論理和、開始・終了の分離、共通被害入口、旧共通書き込みの除去が対応 |
| `sim/build-0.4.md` | Build identifier `0.3-G001-15` | ダッシュ全期間の保護、両終了順序、通常被弾、延長防止、維持する操作の記述が対応 |
| `sim/build-0.3.md` | build 0.3。repo-notes が旧ビルドと明記 | 修正前の比較資料。修正後の証拠には使わない |

Handoff 15 が指定した `sim/build-0.3-G001-15.md` と実在ファイル名は異なるが、識別子と相互参照は一致する。名前を合わせるための再生成は不要。

実装資料の対応箇所：

- `Player invulnerability`: 独立した保護状態、論理和、ダッシュ継続状態への接続、被弾から0.8秒の保護、各終了処理の分離、旧参照・書き込みの置換。
- `Contact and projectile damage`: Grub と Spitter の共通入口、被害適用前の判定、防いだ命中で状態・期限を変更しない処理。
- `Preserved behavior`: 距離・時間・クールダウン・予約攻撃、既存イベント順序、敵・移動等の維持。

変更記述との実装上の矛盾は本文から見つからない。ただし「既存クールダウン起点を維持」は起点そのものの特定ではない。

Handoff 15 の資料生成要求に対する不足は、QA 用の条件別試行記録がないこと。`sim/qa-G001-15.md` は存在しないと Handoff 16 が報告しており、今回の packet にも含まれない。repo-notes の `Limits of available implementation detail` は、配置、実時刻・処理順序、初期ハート、有効試行総数を復元できず、実行済み記録もないと明記している。

### QA に渡せる実在資料

| ファイル・節 | 用途 | 証拠の限界 |
|---|---|---|
| `design/combat.md` の Player kit | 仕様・期待値 | 観察ではない |
| `11-qa-to-studio.md` の「修正の受け入れ条件」「後続で実施する再現・比較手順」 | AC と有効性の基準 | 修正後の結果ではない |
| `sim/build-0.4.md` 冒頭・Dash and damage・Other controls and timing | 対象変更を識別したプレイヤー向け模擬挙動 | 全4環境への適用を文章で宣言しているが、環境別・試行別ログはない |
| `sim/build-0.3.md` | 修正前の症状比較 | 環境や発生条件の詳細はない |

build-0.4 の挙動記述は実在する模擬資料であり、単なる未生成ファイル扱いにはしない。ただし、例示時刻や「命中が成立する」という文章から、実際のフレーム順序や有効試行数を導くことはできない。

QA には仕様・期待値、模擬ビルドの記述、後続で生成される観察記録を別項目として渡す。repo-notes、D-003 の原因説明、Handoff 13・15 の実装理由、本 Handoff の Sender assessment は QA 向け観察資料に混ぜない。

### AC・回帰の資料充足

表の「有効性不足」は、該当挙動の模擬記述はあるが、計画の要求する条件別観察がない状態。「未確認」は必要な枝・詳細自体が確定していない状態。どちらも失敗判定ではない。

各セルは独立に評価する対象であり、4環境共通という宣言を4件の観察に数えない。

| 対象・必要な命中源と枝 | 30 FPS キーボード | 30 FPS ゲームパッド | 60 FPS キーボード | 60 FPS ゲームパッド | 実在する記述／不足 |
|---|---|---|---|---|---|
| AC-1 Grub／Spitter、それぞれ前半・後半 | 有効性不足 | 有効性不足 | 有効性不足 | 有効性不足 | early/late の保護記述あり。各枝の命中成立・ハート前後値・開始終了記録なし |
| AC-2 Grub／Spitter | 有効性不足 | 有効性不足 | 有効性不足 | 有効性不足 | 入力回復直後のダッシュ保護記述あり。最初の入力可能機会・受理・命中の記録なし |
| AC-3 Grub／Spitter | 有効性不足 | 有効性不足 | 有効性不足 | 有効性不足 | 0.70開始・0.85命中の例あり。実際の「被弾保護終了 < 命中 < ダッシュ終了」未確認 |
| AC-4 Grub／Spitter | 有効性不足 | 有効性不足 | 有効性不足 | 有効性不足 | 0.34開始・0.70命中の例あり。実際の逆順成立未確認 |
| AC-5 Grub、初回被害・入力不能中・回復後 | 有効性不足 | 有効性不足 | 有効性不足 | 有効性不足 | 1ハート・0.3秒・0.8秒と追加接触の記述あり。入力受理と各接触のイベント記録なし |
| AC-6 距離・継続・予約攻撃1回 | 有効性不足 | 有効性不足 | 有効性不足 | 有効性不足 | 4タイル・0.25秒・終了時1回の記述あり。移動端点・発動ログなし。30 FPS の終了フレームも未確認 |
| AC-6 クールダウン内／経過後の別試行 | 未確認 | 未確認 | 未確認 | 未確認 | 0.6秒維持の宣言のみ。既存起点、再入力受理、再使用可能時刻なし |
| 回帰1 被弾保護が先に終了、Grub／Spitter、両保護終了後の通常被害 | 有効性不足 | 有効性不足 | 有効性不足 | 有効性不足 | 1.10秒の被害例あり。前後の命中と状態遷移の記録なし |
| 回帰2 ダッシュ保護が先に終了、Grub／Spitter、両保護終了後の通常被害 | 有効性不足 | 有効性不足 | 有効性不足 | 有効性不足 | 0.95秒の被害例あり。同上 |
| 回帰3 延長なし、両終了順序 × Grub／Spitter、異なるフレームで2命中以上 | 有効性不足 | 有効性不足 | 有効性不足 | 有効性不足 | 複数命中で延長しない記述あり。各枝の命中回数・フレーム・元の期限後の被害未確認 |
| 回帰4 ダッシュのみ、Grub／Spitter、複数命中後の解除 | 有効性不足 | 有効性不足 | 有効性不足 | 有効性不足 | ダッシュ中無被害と開始0.40秒後の被害例あり。複数命中と解除を結ぶ試行記録なし |

計画の要件を満たす「観察済み」の試行セルは、この packet からは提示できない。有効・無効試行の記録もなく、総数・発生数は不明。未提示を「0回試行」や「被害0件」に変換しない。

### 補完する資料の変更記述

本 Step が定義するのは以下の資料補完要求であり、simulator の反映完了ではない。ゲーム実装、仕様、AC は変更しない。

1. `sim/build-0.4.md` は現ビルドとして維持する。時刻例を試行ログへ読み替えない。
2. simulator が利用できる既存モデルを確認する。必要なのは衝突形状・座標・速度・発射位相、実在する初期ハート、タイマー更新と移動積分・イベント順序、既存クールダウン起点。取得元を明記し、新規仕様で穴埋めしない。
3. それらが利用可能な場合、QA 用資料を生成する。生成先は既存要求の `sim/qa-G001-15.md` を候補とするが、別名でも識別子と参照が明確ならよい。本 Step では同ファイルを作成していない。
4. 上表の全セル・全枝について、Handoff 15 の設定を目標として試す。AC-1 は前半・後半、AC-2 は入力回復後の最初の機会、AC-3／4 は厳密な前後関係、AC-5 は入力不能中と回復後、AC-6 は距離・時間・攻撃とクールダウンの別試行を記録する。
5. 追加回帰は両終了順序とダッシュのみの解除を分ける。延長防止は異なるフレームで少なくとも2回の成立した命中と元の期限後の被害を対応させる。Spitter の既存2秒間隔で配置が成立しない場合、既存挙動内の配置・位相を具体化して記録し、発射頻度を変えない。成立不能ならその枝を不足として返す。

各試行に必要な観察：

- ビルド識別子、試行ID、AC／回帰、FPS、入力方式、命中源、枝。
- 部屋・全敵とプレイヤーの配置・向き、弾道と発射時刻、初期ハート、保護・入力・クールダウンの初期状態。
- 予定時刻と生成した模擬時刻を別欄にし、フレーム番号、delta time、同一フレーム内順序を記録。
- 初回被害、入力不能開始・終了、入力操作と受理、ダッシュ開始・終了、命中成立の根拠、ハート前後値。
- 論理上の期限と観察フレーム、移動端点・距離、攻撃発動回数、既存クールダウン起点と再使用可能時刻。
- 総数・有効数・無効数、有効試行での被害発生数、無効理由、再試行への参照。

命中不成立、予定外の被害、必要順序の不成立、完全同時境界は該当枝の有効試行に数えない。30 FPS の端数を独自の許容誤差で処理しない。観察を生成できない項目には、不足する入力と理由を明記する。

### 同じ要求を繰り返さないための差し戻し

repo-notes はすでに、提供資料だけでは具体的な試行を復元できないと回答している。従って、同じ packet で「詳細ログを生成せよ」とだけ再依頼しても不足は解消しない。

Studio はまず、runtime の simulator に上記の既存モデル・記録があるかを確認する。これは新たな Owner 計測を開始条件にする依頼ではない。

- **利用できる場合:** 出典付きでモデルを補い、上記の観察資料を生成する。
- **利用できない場合:** technical-director に、現在の dry-run 入力では承認済み計画の試行要件を満たせないことを戻す。利用可能な検証方法と追加入力を具体化し、必要なら QA と証拠要件を調整する。gameplay-engineer が要件を緩めない。
- **既存クールダウン起点を回復できず、新しく決める必要がある場合:** game-designer へ判断を戻す。開始起点・終了起点等で再使用可能時刻が変わるため、今回選択しない。
- **同時イベントや入力不能中の予約の判断が不可欠と判明した場合:** 競合する具体例を付けて game-designer へ戻す。現時点では境界を避ける計画のため、新規判断を要求しない。

## Decisions already made

- D-001: 攻撃・ダッシュ・ポーズ以外の入力を追加しない。
- D-002: 部分的な Owner 観察を使って元の修正 Goal を継続する。追加計測を開始条件にしない。
- D-003: 発生源別の保護を論理和で判定し、防いだ命中で保護を開始・延長しない。

## Constraints

- 模擬実装の反映、模擬ビルドの挙動記述、条件別観察、実測を区別する。
- 未生成ファイルや未確認の試行を完了扱いしない。
- 仕様・AC・計画を独断で変更しない。全4環境と必要な命中源・枝を省略しない。
- クールダウン起点、完全同時イベント、入力不能中の予約を新設しない。
- 原因説明・実装理由・自己評価は QA の観察資料から分離する。
- 独立 Verify と Goal 完了の判断は本 Step では行わない。

## Open questions

1. runtime の simulator は、repo-notes で未提供とされた既存モデルとイベント情報を利用できるか。できる場合、その出典は何か。
2. 利用できない場合、technical-director はどの追加入力・検証方法で計画を成立させるか。
3. 既存クールダウン起点は回復可能か。不可能なら、仕様判断を game-designer に戻す必要があるか。

## Expected output

Studio は build-0.4 と変更 `0.3-G001-15` の対応を採用し、ファイル名だけを理由とする再生成を終了する。

次に、simulator の利用可能な入力を確認して資料補完へ進むか、生成不能の具体的理由と本表を technical-director に渡す。観察資料が整った後に、原因説明や自己評価を除いた資料を独立 QA へ渡す。不足を残す場合は、その条件を未確認と明示し、Verify 完了として扱わない。

## Sender assessment

文書照合では、Handoff 15 の主要な変更は実装資料に反映され、模擬ビルドも同じ識別子を持つ。変更全体の未反映とみなす根拠はない。

ただし、保護されるという挙動説明だけでは、命中成立やフレーム順序を要求する計画の証拠には足りない。今回の阻害要因は実装変更の記述不足ではなく、試行生成に必要な既存情報と観察記録の不足である。文書上の整合以上の自己評価や合格判定は行っていない。

## Load

- Project: project.md#constraints
- Project: design/combat.md
- Project: sim/repo-notes.md
- Project: sim/build-0.3.md
- Project: sim/build-0.4.md
- Project: goals/G-001-dash-damage/11-qa-to-studio.md
- Project: goals/G-001-dash-damage/13-technical-director-to-studio.md
- Project: goals/G-001-dash-damage/15-gameplay-engineer-to-studio.md
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-resume-with-owner-observations.md
- Decisions: decisions/D-003-independent-invulnerability.md
- Previous handoff: goals/G-001-dash-damage/16-studio-to-gameplay-engineer.md
>>>END

## Validation feedback

A previous executor's output was rejected for these reasons. Produce the operation's files again, fixing them:

- goals/G-001-dash-damage/18-studio-to-technical-director.md: Load must include studio/roles/technical-director.md
