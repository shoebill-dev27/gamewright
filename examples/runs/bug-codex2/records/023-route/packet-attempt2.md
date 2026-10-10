# Studio operation packet

operation: Route
goal: G-001
step_artifact: goals/G-001-dash-damage/19-technical-director-to-studio.md
next_seq: 20

## You may write

- goals/G-001-dash-damage/goal.md
- goals/G-001-dash-damage/19-technical-director-to-studio.md (in place: keep kind, goal, seq, from, to)
- goals/G-001-dash-damage/20-studio-to-<role>.md

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
goals/G-001-dash-damage/18-studio-to-technical-director.md
goals/G-001-dash-damage/19-technical-director-to-studio.md
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
- Diagnose / Plan: technical-director が共有無敵フラグの解除競合を診断し、発生源別に保護を管理する計画を作成した。結果は `13-technical-director-to-studio.md`。現在は、利用可能な dry-run 資料で検証計画が成立するかが未解決であり、追加 Plan を設ける。
- Decide: 既存仕様への修正に方向選択は不要。D-002 は不足入力を補完して継続する Owner の決定。D-003 は既存仕様を維持する技術方式の決定。
- Design: QA によれば期待挙動と受け入れ条件は明確。ただし既存クールダウン起点を資料から回復できるかは未解決。新規の仕様判断が必要と判明した場合は game-designer に戻す。入力不能中の予約入力や完全同時の境界処理は今回新たに定義しない。
- Build: `15-gameplay-engineer-to-studio.md` に模擬実装変更を定義済み。`17-gameplay-engineer-to-studio.md` の照合結果に基づき、`sim/build-0.4.md` を変更識別子 `0.3-G001-15` の模擬ビルドとして扱う。ファイル名を合わせるための再生成は不要。
- Verify: Build 後は必須。条件別試行資料と既存動作の情報が不足している。PC・30 / 60 FPS・キーボード / ゲームパッドの全4組合せ、AC-1〜AC-6 と必要な回帰の検証方法を technical-director が整理した後、独立 QA に渡す。未生成資料を Load に指定しない。
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
| 6b | Build 資料照合・補完 | gameplay-engineer | implement-change | done | 16-studio-to-gameplay-engineer.md |
| 6c | Plan 検証成立性の再検討 | technical-director | technical-plan | open | 18-studio-to-technical-director.md |
| 7 | Verify | qa | verify-change | planned | — |
| 8 | Play | playtester | playtest-session | skipped | — |
| 9 | Review | game-director | review-outcome | skipped | — |
| 10 | Next | studio | — | planned | — |

過去の Observe の done は入力確認作業の終了を表し、再現確認の成功を表さない。1d の結果は `08-qa-to-studio.md`。1e の結果は `11-qa-to-studio.md`（done）であり、仕様不一致の照合と受け入れ条件の作成が完了した。行 2 の結果は `13-technical-director-to-studio.md`（done）。独立した Plan 行 5 は行 2 に統合したため skipped。

行 6 の結果は `15-gameplay-engineer-to-studio.md`（done）。変更記述を模擬実装とするプロジェクト規約に従う完了であり、simulator の資料生成や独立 Verify の合格を意味しない。

行 6b の結果は `17-gameplay-engineer-to-studio.md`（question）。done は照合と不足の報告が終了したことを示し、検証入力の完成を意味しない。

## Route changes

2026-10-10 — `02-qa-to-studio.md`（question）を受領し、1 を done とした。再現条件不足により追加 Observe を設けた。期待挙動の仕様不足ではないという QA の報告を受け、Design を skipped とした。

2026-10-10 — `04-qa-to-studio.md`（question）を受領し、1b を done とした。補足資料が未提供のため、資料受領を開始条件とする 1c を設けた。

2026-10-10 — `06-qa-to-studio.md`（question）を受領し、1c を done とした。資料受領を開始条件とする 1d を設け、実行環境側の補完を待つ方針とした。当時は Owner escalation を行わなかった。

2026-10-10 — `08-qa-to-studio.md`（question）を受領し、1d を done とした。同じ不足入力について新しい該当資料がないまま question が二回以上返ったため、loop limits を適用した。`09-studio-to-owner.md` に必要入力と選択肢をまとめ、Goal を blocked-on-owner とした。

2026-10-10 — Owner が Option A を選び、新しい観察を提供した。選択と回答原文を D-002 に記録し、09 を resolved、Goal を active とした。Observe 1e を追加した。体感による時刻や頻度を計測値とせず、部分資料から判断可能な範囲を QA に委ねた。

2026-10-10 — `11-qa-to-studio.md`（done）を受領し、1e を done とした。QA は不具合報告と AC-1〜AC-6 を作成し、追加の Owner 計測を必須とせず技術調査へ進めると報告した。Diagnose と Plan を行 2 に統合し、行 5 は skipped とした。Build と Verify は維持した。

2026-10-10 — `13-technical-director-to-studio.md`（done）を受領し、行 2 を done、行 6 を open とした。D-003 に基づく方式と実装順序を technical-director の判断として引き継いだ。実装は逐次、完了後に独立 QA の Verify を行う。視覚変更は計画にないため art-director の追加は不要。

2026-10-11 — `15-gameplay-engineer-to-studio.md`（done）を受領し、行 6 を done とした。模擬実装の定義は完了したが、指定生成先 `sim/build-0.3-G001-15.md` と `sim/qa-G001-15.md` は存在一覧になく、検証入力が揃ったとは判断できなかった。一方、一覧には `sim/build-0.4.md` があったため、行 6b を追加して既存資料の照合・補完を依頼した。Verify は planned のまま維持した。

2026-10-11 — `17-gameplay-engineer-to-studio.md`（question）を受領し、行 6b を done とした。工程担当の照合報告に基づき、build-0.4 と変更識別子 `0.3-G001-15` の対応を採用する。ファイル名の違いは解消済みとして扱う。一方、条件別試行記録、試行生成用の既存モデル、クールダウン起点は不足している。実装への同じ補完要求を繰り返さず、Build の計画不成立に対する return rule を適用し、行 6c を追加して technical-director に検証成立性を戻す。これは QA の fail や同一 AC の二回目の失敗ではない。

本 Route の packet には runtime の simulator に問い合わせる手段や、そのモデルを確認できる資料がない。利用不能と断定せず、利用可能性と不足の解消方法を技術問題として渡す。新しいビルド対応情報と具体的な不足表が提供されており、同じ不足入力への question を無変更で反復する段階ではない。どの Role も解消できない外部入力が必要と確定した場合は Owner escalation とし、同じ照会を繰り返さない。

Studio は元資料の本文を独自に確認したとは扱わず、Handoff 17 の報告を出典として引き継ぐ。今回、仕様・AC・証拠要件の変更や Verify の判定は行わない。

## Next action

technical-director が `18-studio-to-technical-director.md` から、現在の dry-run 資料で成立する検証方法、必要な追加入力と取得元、残る不明点を整理して Studio に返す。既存モデルが使えるという前提で試行生成を約束しない。

Studio は結果に応じて資料補完、QA との証拠要件の確認、必要な仕様判断、または Owner escalation を手配する。独立 Verify は必須のまま保持し、QA に渡す資料から実装理由と自己評価を除外する。

## Outcome

未完了。仕様不一致の確認、受け入れ条件、技術計画、模擬実装変更の定義、および更新ビルドの識別が完了した。D-002 に基づき継続し、D-003 の発生源別無敵管理が反映されたとの照合報告を受領した。条件別観察資料と検証計画の成立性の整理、独立 QA の検証が残っている。現時点で Owner に新たな判断を求める事項はない。
>>>END

<<<FILE goals/G-001-dash-damage/19-technical-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 19
from: technical-director
to: studio
stage: Plan
outcome: done
---
# 19: technical-director → studio — 既存モデルの取得可否で検証手順を分岐する

## Task

Studio はまず runtime の simulator について、既存モデル・記録の取得元と照会手段を確認する。取得できる入力を明示して資料補完へ進め、取得できない条件は未確認として独立 QA に渡す。

## Context

Owner の依頼は、再現するダッシュ中の被害を仕様に合わせて修正すること。戦闘の方向・バランス変更は対象外である。

本作は dry-run であり、Build の変更記述を runtime の simulator が `sim/` に反映する。実機実行を前提にした計画へ置き換えない。

本 Step は提供された Handoff 17・18 と Role・technical-plan Skill、project の抜粋だけで技術上の検証方法を整理した。既存モデルの照会、原資料の再照合、試行生成、追加実装、QA 判定は行っていない。`outcome: done` は条件付き計画の作成完了を示し、検証入力の完成や Verify 完了を意味しない。

## Findings

### 1. 現在成立することと成立しないこと

Studio が採用した `sim/build-0.4.md` と変更識別子 `0.3-G001-15` の対応を維持する。ファイル名を揃える再生成は不要である。

Handoff 17 は変更反映の文書照合を報告している。ただし本 Step にビルド・repo-notes 原文はなく、その報告を独立に再検証したものではない。

模擬ビルドを読んで仕様との対応を確認する方法は dry-run と両立する。一方、従来計画が要求する条件別の命中成立、入力受理、フレーム順序、ハート前後値は、挙動説明だけから復元できない。全4環境への適用宣言も環境別観察の代わりにはならない。

既存モデルに基づく生成観察なら条件別試行を補完できる可能性がある。ただし、それは模擬モデル内の結果であり、実機の入力装置・描画・処理負荷の実測ではない。現 packet では、そのモデルの存在・不存在・利用可能性のいずれも確定できない。

影響する確認対象は、発生源別保護、共通被害入口、入力不能と回復、ダッシュ移動・終了、予約攻撃、クールダウン、敵接触・弾道、フレーム内の更新順序である。追加のゲーム実装は本計画に含めない。

### 2. 最初に取得する入力と担当

| 入力 | 取得元・確認箇所 | 担当と必要な回答 |
|---|---|---|
| simulator の利用可能性 | runtime の管理側。具体的な窓口・照会手段は packet にない | Studio が窓口を特定し、照会可能／不可／不明と、その根拠を返す |
| 既存モデルの識別と来歴 | runtime が保持するモデル、既存設定、保存記録があればその原資料 | Studio が取得経路を確保し、gameplay-engineer が版・出典・対象変更との対応・欠落を整理する |
| 配置と衝突条件 | モデル内の部屋、衝突形状、座標、速度、敵数、弾道・発射位相 | gameplay-engineer が既存値と試行用に選べる設定を区別する。取得不能な値は作らない |
| 初期状態 | モデルまたは既存試行の初期ハート、保護、入力、クールダウン状態 | gameplay-engineer が実在する設定と再初期化方法を示す |
| 時間と処理順序 | タイマー更新、移動積分、衝突・被害・入力の処理順序、30／60 FPS の扱い | gameplay-engineer が出典を示す。論理上の期限と処理フレームを分ける |
| クールダウン起点 | `sim/repo-notes.md` の Preserved behavior と関連する既存タイマー定義、旧モデル・記録、`design/combat.md` の Player kit | まず gameplay-engineer が回復を試みる。起点未記載なら、維持の宣言だけで補わない |
| 試行条件と有効性の原文 | Handoff 11「修正の受け入れ条件」「後続で実施する再現・比較手順」、Handoff 13 の検証計画、Handoff 15 の設定・資料生成要求 | Studio が必要部分を次 packet に収録する。13・15 の正確な節名は未提示なので内容で指定する |

モデル取得では、モデルが単に期待値の文章を再出力するものか、状態遷移・命中を条件別に導出して記録できるものかも確認する。前者から試行結果を名乗る記録は作らない。

原文が必要なのは、具体的な試行設定、有効試行数・許容差などの基準、既存挙動の確定時である。本 Step は未提示の基準を追加しない。D-001〜D-003 は提示された要約の範囲で適用し、それを超える解釈が必要になった場合のみ該当 Decision 原文を取得する。

### 3. 順序と分岐

1. **Studio：取得経路を確認する。**  
   runtime 管理側に、モデル・記録の有無、出典、取得可能範囲、生成可能な観察項目を問い合わせる。照会できない場合は「モデルなし」ではなく「照会手段未確保」と返す。同じ packet で engineering に詳細ログ生成だけを再依頼しない。

2. **gameplay-engineer：入力の充足を照合する。**  
   取得できたモデル・原文を用いて、上表の項目を「取得済み／不足／矛盾」に分類する。既存記録がある場合も、識別子・環境・枝・有効性が対応するものだけを候補とする。

3. **既存モデルが十分なら：資料生成の具体的な依頼を作る。**  
   gameplay-engineer が既存モデル内で成立する設定、生成手順、記録項目を変更記述として提示し、runtime の simulator による資料生成へ進む。`sim/qa-G001-15.md` は候補名であり、現時点の実在資料ではない。生成後に存在・内容・対象識別を確認してから QA の Load に入れる。

4. **一部だけ取得できるなら：成立する枝だけ補完する。**  
   不足する枝と必要入力を残す。部分結果から全4環境・全枝へ一般化しない。Spitter の既存2秒間隔で複数命中が成立するかは、既存配置・位相の選択範囲で調べる。成立しない場合は、その枝の生成不能理由を返し、発射頻度を変えない。

5. **モデル・記録を取得できないなら：文書評価へ限定して QA に相談する。**  
   仕様・AC と模擬ビルドの対応表、記述のある枝・ない枝、不足理由を作成する。独立 QA は文書上で評価できる範囲と、従来の条件別試行要件に対する証拠の十分性を判断する。文書評価を試行実施に読み替えたり、QA への相談をもって要件を緩和したりしない。従来要件が維持される限り、観察を生成できないセルは未確認として残る。

6. **独立 QA へ渡す。**  
   仕様・期待値、模擬ビルド記述、出典付き生成観察、欠落一覧を別々に渡す。実装理由、原因説明、自己評価を観察資料へ混ぜない。証拠の採否と pass／fail は QA に残す。

コード変更も試行実施も今回の対象ではなく、後続作業も入力取得→設定確定→生成→独立検証の依存関係があるため、並列実装は行わない。

### 4. 条件別検証の維持範囲

以下の全対象を、30／60 FPS × キーボード／ゲームパッドの4環境で保持する。表は Handoff 17 に基づく補完対象であり、AC 原文の再定義ではない。

| 不足項目 | 主な解消区分 | 補完・判断内容 |
|---|---|---|
| AC-1：Grub／Spitter、前半・後半 | 資料補完→QA の判断 | 命中成立、ダッシュ開始終了、ハート前後値 |
| AC-2：Grub／Spitter | 資料補完→QA の判断 | 最初の入力可能機会、操作・受理、命中 |
| AC-3：Grub／Spitter | 資料補完→QA の判断 | 被弾保護終了 < 命中 < ダッシュ終了 |
| AC-4：Grub／Spitter | 資料補完→QA の判断 | ダッシュ終了 < 命中 < 被弾保護終了 |
| AC-5：Grub、初回・入力不能中・回復後 | 資料補完→QA の判断 | 初回被害、各接触、入力不能の開始終了、入力受理 |
| AC-6：距離・継続・予約攻撃1回 | 資料補完→QA の判断 | 移動端点、距離、論理期限と終了フレーム、攻撃発動 |
| AC-6：クールダウン内／経過後の別試行 | 既存資料補完。回復不能なら仕様判断 | 起点・再使用可能時刻を確定してから再入力受理を確認 |
| 回帰1・2：両終了順序、各 Grub／Spitter | 資料補完→QA の判断 | 保護の遷移と両保護終了後の通常被害 |
| 回帰3：両終了順序 × Grub／Spitter | 資料補完→QA の判断 | 異なるフレームで2命中以上、元の期限、期限後の被害 |
| 回帰4：ダッシュ単独 × Grub／Spitter | 資料補完→QA の判断 | 複数命中、ダッシュ終了、解除後の被害の対応 |
| 総数・有効数・無効数・発生数 | 記録の資料補完→QA の判断 | 記録に基づいてのみ集計。不明は不明のままにする |
| モデル・記録そのものの提供不能 | 取得経路の確認。必要性が確定すれば外部入力 | Role が生成できない既存情報を明示し、Studio が escalation 要否を判断 |

各試行には、ビルド・モデル識別子と出典、試行ID、対象セル・枝、配置・向き・弾道、初期状態、予定時刻と生成時刻、フレーム・delta time・同一フレーム内順序、操作と受理、状態遷移、命中根拠、ハート前後値、移動・攻撃・クールダウン記録を含める。有効性判定と無効理由、再試行参照も保存する。

命中不成立、予定外の被害、必要順序の不成立、完全同時境界を該当枝の有効試行に数えない。無効試行も記録から消さない。30 FPS の端数に独自の許容差を設けない。必要試行数は原文を回復するまで定めない。

自動化は既存 simulator が対応する生成・記録・集計に限定する。対応機能は未確認である。QA は出典、条件と記録の対応、有効性、期待値との差を独立に読む。

### 5. 仕様判断が必要になる条件

クールダウン起点は、まず既存情報の回復で解決する。回復不能、または原資料間の矛盾が残る場合に game-designer へ次の問いを渡す。

> ダッシュ再使用までの0.6秒は、入力受理・ダッシュ開始・ダッシュ終了のどのイベントを起点とするか。継続0.25秒のダッシュを時刻tに開始した場合、開始起点ならt+0.6、終了起点ならt+0.85となるが、どの既存仕様を採用すべきか。既存仕様を回復できない場合、新規判断としてどう定義するか。

これは選択肢の差を示す論理時刻の例であり、観察値ではない。入力受理と開始が別イベントなら、その違いも出典付きで渡す。

同時イベントと入力不能中の予約は、現在の非同時境界の計画で不要なら判断を求めない。不可避と判明した場合のみ、具体的に競合するイベント、既存順序の不足、受理・被害が変わる枝を game-designer に提示する。技術側でプレイヤー向け挙動を選ばない。

### 6. リスクと証拠の限界

- 期待値を再出力した文章による循環検証を避けるため、モデルの来歴・設定・生成過程を明示する。
- フレーム依存の見落としを避けるため、30／60 FPS を分け、論理期限と観察フレームを別記する。
- 入力方式の名前だけを変えた重複資料を避けるため、モデルがキーボード／ゲームパッドの何を表現するか記載する。区別できなければ環境別観察としての限界を残す。
- 初期ハート・状態・敵配置の欠落で有効性が判断できない試行は、期待通りの結果でも充足扱いしない。
- 実機性能、実際の装置遅延、セーブ互換性の証拠は本計画から得られない。今回これらを追加要件にはしない。

### 7. Owner escalation の条件

現時点では Owner にしか提供できない入力は確定していない。モデル照会手段が packet にないことだけを理由に、Owner 計測を要求しない。

次の両方が確認された場合に、Studio が具体的な escalation を準備する。

1. runtime 管理側への確認により、必要な既存モデル・記録を Role が取得・生成できない理由が判明した。
2. QA が利用可能な文書・部分観察では必要な検証を成立させられないと判断した。

その場合は、必要な外部材料の名称・保有元・取得不能理由・影響するセルを添え、材料へのアクセス提供、または検証範囲・Goal の扱いについて判断を求める。既存モデルを捏造することは Role の資料補完ではない。実機試験や新しい simulator の開発が必要なら、dry-run の範囲を超える提案として扱う。Owner が材料を保有するとは仮定しない。

## Decisions already made

提示された要約の範囲で維持する。

- D-001：攻撃・ダッシュ・ポーズ以外の入力を追加しない。
- D-002：部分的な Owner 観察を使って元の修正 Goal を継続する。追加計測を開始条件にしない。
- D-003：発生源別保護を論理和で判定し、防いだ命中で保護を開始・延長しない。

新規仕様・アーキテクチャの採択はなく、D-004 は作成しない。

## Constraints

- 仕様・AC・全4環境・必要な命中源と枝を維持する。
- 模擬挙動の記述、生成観察、実測、期待値を区別する。
- 未提示の試行数・発生数をゼロに変換しない。
- 未取得モデル、処理順序、初期状態、既存起点を創作しない。
- 追加実装・条件別試行の実施・QA 判定・Goal 完了は本 Step に含めない。
- 未生成資料を Load に入れない。

## Open questions

1. runtime 管理側の照会窓口・手段は何か。既存モデル・記録のどの部分を取得できるか。
2. モデルは条件別の状態遷移と命中を生成できるか。入力方式とFPSをどこまで表現するか。
3. クールダウン起点とフレーム順序を既存原資料から回復できるか。
4. 原文を回復した試行要件に対し、独立 QA が採用できる証拠はどこまでか。

## Expected output

Studio は最初に取得経路と利用可能情報を確認し、出典または取得不能理由を記録する。

取得できる場合、次の作業 Role は gameplay-engineer。開始入力は、取得したモデル・記録、Handoff 11・13・15 の必要部分、対象ビルド・repo-notes の原文、本 Handoff の補完表とする。求める成果は入力充足表と、成立する枝についての具体的な資料生成要求であり、同じ不足入力でのログ生成再依頼にはしない。

取得できない場合、利用可能な仕様・AC 原文と模擬ビルド、不足一覧を QA に渡し、文書評価の範囲と証拠不足を判断してもらう。既存挙動の回復不能は game-designer、Role 外の必須入力が確定した場合は Owner escalation に分ける。

いずれの経路でも独立 Verify は未完了のままとする。

## Load

- Project: project.md#vision
- Project: project.md#constraints
- Previous handoff: goals/G-001-dash-damage/18-studio-to-technical-director.md
- Supporting handoff: goals/G-001-dash-damage/17-gameplay-engineer-to-studio.md
- Decisions: 原文の追加 Load なし。提示された要約の範囲を維持する。
- Routing note: Studio が次の受信 Role・Skill を指定し、取得済みの原資料だけを追加する。モデル資料と QA 用試行資料は現時点で未取得。
>>>END

## Validation feedback

A previous executor's output was rejected for these reasons. Produce the operation's files again, fixing them:

- goal.md: an active Goal needs its next step marked `open` with its Handoff
