# Studio operation packet

operation: Route
goal: G-001
step_artifact: goals/G-001-combat-monotony/04-game-designer-to-game-director.md
next_seq: 5

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/04-game-designer-to-game-director.md (in place: keep kind, goal, seq, from, to)
- goals/G-001-combat-monotony/05-studio-to-<role>.md

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
design/combat.md
goals/G-001-combat-monotony/01-studio-to-playtester.md
goals/G-001-combat-monotony/02-playtester-to-studio.md
goals/G-001-combat-monotony/03-studio-to-game-designer.md
goals/G-001-combat-monotony/04-game-designer-to-game-director.md
goals/G-001-combat-monotony/goal.md
project.md
sim/build-0.3.md
sim/repo-notes.md
>>>END

<<<FILE @decision-titles
decisions/D-001-one-button-combat.md — D-001: Combat uses one attack button plus dash
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
- 現状はビルド 0.3(5部屋、敵2種、攻撃とダッシュ)。単調さの原因候補(敵の種類・挙動、部屋構成、プレイヤーキットの幅など)は Project Context には書かれていない。
- 即時エスカレーションは不要。Goal は再解釈を要さず、ビジョンや既存の Decision と衝突しない。ただし診断で D-001 の変更や新ボタンが必要と分かれば、その時点でエスカレーションする。

各ステージの入口の問い:
- Observe: 単調さを実際にプレイして観察したか → 観察済み(Handoff 02)。ただし被弾直後のダッシュ中ダメージの疑い(問題 D)は未再現で、`qa` による再現が必要。
- Diagnose: 原因は分かっているか → 不明。
- Decide: 方向・優先度・スコープの本当の選択があるか → 診断の選択肢次第。
- Design: 意図する挙動は仕様化済みか → 変更が決まれば未仕様。
- Plan: 技術的アプローチは非自明か → 変更内容次第。
- Build: ゲームを変更する必要があるか → 診断次第。
- Verify: Build の後は常に必要。
- Play: Goal は遊び心地に関する → 変更後に必要。
- Review: 体験の Goal → 必要。

スキップしたステージ: なし。Project Context はどの問いにも答えていないため。ただし後続は結果に依存するので tentative とした。

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | playtester | playtest-session | done | [02-playtester-to-studio.md](02-playtester-to-studio.md)(開始 Handoff: [01-studio-to-playtester.md](01-studio-to-playtester.md)) |
| 2a | Diagnose | game-designer | diagnose-experience | open | [03-studio-to-game-designer.md](03-studio-to-game-designer.md) |
| 2b | Observe(欠陥 D) | qa | reproduce-defect | planned | —(`04-studio-to-qa.md` を別の Studio 操作で作成する) |
| 3 | Decide | game-director | make-decision, prepare-owner-escalation | tentative(診断が方向・優先度・スコープの実質的な選択肢を示す場合。D-001 に触れる案ならエスカレーション) | — |
| 4 | Design | game-designer | write-design-spec | tentative(変更が決まり、仕様が未整備の場合) | — |
| 5 | Plan | technical-director | technical-plan | tentative(変更が非自明・複数システムにまたがる・並列化可能な場合) | — |
| 6 | Build | gameplay-engineer | implement-change | tentative(ゲーム変更が決まった場合、または 2b で欠陥が確認された場合) | — |
| 7 | Verify | qa | verify-change | tentative(Build が行われた場合は必須) | — |
| 8 | Play | playtester | playtest-session | tentative(Build が行われた場合。新しい実行コンテキストで) | — |
| 9 | Review | game-director | review-outcome | tentative(変更が入った場合、または方向 Decision があった場合) | — |

Status: planned | tentative | open | done | skipped. Handoff: the incoming Handoff that starts the
step. Parallel steps: 2a, 2b. Step numbers need not
match Handoff seq numbers. The route is a plan; the Route operation revises it.

## Route changes

- Step 1(Observe)の後: プレイテスターの観察報告(Handoff 02)は、体験の問題 A〜C(毎部屋同じ型、緊張感の欠如、ダッシュが戦闘で使われない)と、不具合の疑い D(被弾直後のダッシュ中にダメージを受けることがある)を報告した。計画どおり Diagnose(2a)に進む。
- 追加: 2b として `qa` による D の再現(`reproduce-defect`)を並列で加えた。理由: D は仕様と食い違うか明らかな不具合の疑いであり、開発ループの戻りルール(Play の結果が欠陥なら Observe は `qa`)に従う。2a の診断(A〜C)と互いの出力を使わないため並列にできる。
- 2b で欠陥が確認された場合、修正は Build(6)・Verify(7)に合流させるか、パターン1(Observe → Build → Verify)の別ルートとするかを、2b の結果を受けた Route で決める。意図する挙動が設計文書で未定義と分かった場合は Design(`game-designer`)に回る。
- 2b の Handoff は、今回の操作の書き込み範囲外のため未作成。次の Studio 操作で `04-studio-to-qa.md` を作る。
- 観察は `sim/build-0.3.md` の記述に基づくドライランであり、ゲームパッドの操作感や実時間は未確認。この制約を 2a の Handoff に引き継いだ。

## Next action

Studio は Route を終えて停止する。次の操作は 2 つ。
1. 人間が Handoff `goals/G-001-combat-monotony/03-studio-to-game-designer.md` から `game-designer`(Diagnose、`diagnose-experience`)のステップを開始する。
2. 並列の 2b(`qa`、`reproduce-defect`)のために、Studio が `04-studio-to-qa.md` を作成する Route 操作を行う。Owner の報告と設計文書のみを渡し、プレイテスターの推測は含めない。

2a の結果(診断と選択肢)は、次の Route で `game-director`(Decide)に渡すかどうかを判断する。D-001 の変更や新ボタンが必要な案が出た場合はエスカレーションする。

Owner への報告(日本語):
- 観察が完了した。どの部屋も「立って振る・横にずれる」で突破でき、緊張感がなく、ダッシュも戦闘で使われなかった。Owner の「単調」という所見と整合する観察だが、プレイテスターには所見を伝えておらず、独立した結果である。
- ただし、この観察はドライランとして記述を読んだものであり、ゲームパッドの操作感や実時間は未確認。
- 次は、ゲームデザイナーが原因を診断し、D-001 の枠内で選択肢を出す。
- 副次的に、被弾直後のダッシュ中にダメージを受ける不具合の疑いが見つかった。こちらは QA が別に再現する。
- いまのところ Owner の判断は不要。

## Outcome

(未完了)
>>>END

<<<FILE goals/G-001-combat-monotony/04-game-designer-to-game-director.md
---
kind: handoff
goal: G-001
seq: 4
from: game-designer
to: game-director
stage: Decide
outcome: done
---
# 04: game-designer → game-director — ビルド 0.3 の戦闘が単調な原因の診断と、D-001 の枠内の選択肢

## Task

下の診断と3つの選択肢を見て、G-001 の方向・優先度・スコープを決める。どの案(または組み合わせ)を進めるか、新しい敵や見た目の作業をどこまで許すかを決めること。仕様や数値の最終決定は、方向が決まってからの `write-design-spec` で行う。

## Context

Goal G-001 の Owner の依頼は「戦闘が単調なので改善したい」。成功条件は、想定プレイヤーが戦闘中に、同じ行動の繰り返しではなく、位置取り・タイミング・敵の挙動への対応といった判断を実感できること。
Observe で、プレイテスターがビルド 0.3 を全5部屋通してプレイした(`02-playtester-to-studio.md`)。体験の問題 A〜C が `game-designer` に回り、これが最初の Diagnose。
観察はドライランで、`sim/build-0.3.md` の記述から推定した体験。ゲームパッドの操作感、音、演出、各部屋の実時間は未確認。このため、それらに依存する原因は仮説として分けて書く。

## Findings

### 1. 診断: 症状と原因

根拠は `design/combat.md` の記述(以下「設計書」)と、プレイテスターの観察(以下「観察」)。

**共通の原因(A・B・C のすべてに効いている)**

- **P1. 敵の挙動が各1種類で、プレイヤーに別の答えを求めない。**
  - Grub は「まっすぐ歩いて接触で噛む。予告なし」(設計書)。Spitter は「その場に固定で、2秒ごとに遅い弾を撃つ」(設計書)。
  - どちらも「向き直って振る」「横に1歩ずれる」で足りる。観察の部屋4〜5の型と一致する。
  - 敵が2種類でそれぞれ挙動が単純なので、混成にしても足し算にしかならず、組み合わせの判断が生まれない。
- **P2. 部屋の構成に進行がない。**
  - 設計書は「5部屋、各3〜6体、Grub と Spitter の混成」としか定義していない。敵の強さ、出現の仕方、配置が部屋ごとに変わる記述がない。
  - これが「2分目も15分目も同じ」(A)と「部屋が進んでも脅威が変わらない」(疑問)の直接の原因と考えられる。

**A. 毎部屋同じ型で変化しない**

- 主因は P1 と P2。
- 補助的な要因として、プレイヤー側の選択肢が攻撃とダッシュだけ(D-001)なので、敵が型を変えない限り、型は変わらない。

**B. 緊張感がほとんどない**

- **B1. Grub の脅威が低い。**
  - HP2、攻撃1ダメージ、回復0.35秒。Grub は一直線に来るので、その場で振れば接触前に倒せる(観察:「近づかれる前に片付く」)。
  - 被弾は3体が同時に来たときだけ、という観察と整合する。
- **B2. Spitter の脅威が低い。**
  - 弾が遅く、固定のリズム(2秒ごと)で、狙いが単純。横に1歩ずれれば避けられる(観察)。
  - 読める脅威(柱3)としては成立しているが、避けるのに技量が要らない。
- **B3. 被弾の罰が軽い(推定)。**
  - 被弾後は0.3秒の硬直のあと、被弾から0.8秒は無敵(設計書)。
  - 最大ハート数、弾のダメージ量などは設計書に未記載で、被弾の重さは断定できない。観察でも被弾は少なかった。

**C. ダッシュが戦闘で使われない**

- **C1. ダッシュを必要とする脅威がない。**
  - ダッシュは4タイル・0.25秒の全区間無敵で、クールダウン0.6秒(設計書)。性能は十分に強い。
  - 歩くだけで足りる敵(P1、B1、B2)しかいないため、使う理由がない。性能の問題ではなく、需要の問題と見る。
- **C2. ダッシュに「攻めの使い道」がない。**
  - 設計書では、ダッシュは移動と無敵のみ。攻撃はダッシュ中に予約されて終了後に出る。位置取りで敵を崩す動機がない(推定)。

**確認が必要な仮説(観察が届いていない部分)**

- H1. ゲームパッドでの実際の入力感。攻撃の回復0.35秒とダッシュのクールダウンが、実機で「軽すぎる」か「普通」か。
- H2. 各部屋の実時間。5部屋で15〜20分に届くか、テンポが単調さを悪化させているか。
- H3. 音と演出が単調さを強めている、または緩和している可能性。
- H4. 敵の移動速度、弾速、配置の具体値。設計書にない。観察は「遅い」「簡単」と述べているが、数値の根拠はない。

### 2. 設計書の未定義事項(記録)

被弾後のダッシュ(欠陥 D)に関わる事実として、設計書は次のことを定義していない。

- 被弾の硬直(0.3秒)中にダッシュ入力を受け付けるか。
- 被弾後の無敵(0.8秒)とダッシュの無敵(0.25秒)が重なったときの扱い。
- 無敵の終了時刻と、ダッシュの途中で被弾が成立する条件。
- ダッシュのクールダウン中に被弾した場合の挙動。

設計書の文面どおりなら、ダッシュ中は常に無敵で、被弾から0.8秒も無敵なので、「ダッシュ途中のダメージ」は期待される挙動にならない。だから、この観察は不具合の疑いで、設計の抜けではなく実装の問題かもしれない。ただし、上の抜けが原因である可能性も残る。再現と原因の特定は `qa` の仕事で、ここでは扱わない。`qa` の結果次第で、期待される挙動を設計書に書き足す必要がある。

その他、設計書に未記載で、次の仕様化で必要になる項目: 最大ハート数、敵の速度、弾速と弾のダメージ、敵の出現位置、弾が壁や他の敵に当たる扱い。

### 3. 選択肢(すべて D-001 の枠内。新しい入力ボタンは不要)

**案1: 敵の挙動を増やす(予告つきの突進と、Spitter の撃ち方の変化)**

- 変更内容:
  - Grub に、予告つきの突進を持つ型を追加する。例えば、立ち止まって短く溜めたあと、直線上に素早く突っ込む。
  - Spitter に撃ち方の変化を追加する。例えば、3連射や、プレイヤーの進行方向を狙う弾。
  - 既存の敵の枠組みに挙動を足す形が基本で、新しい敵の種類は作らない。
- 効く症状: A(型を壊す)、B(駆け引きが生まれる)、C(突進をダッシュの無敵で抜ける、という使い道ができる)。
- コスト: 中。既存の敵の仕組みを再利用できるが、新しい挙動の実装と調整が要る。予告の見た目(溜めの動き、色、効果音)が必要になる。
- リスク: 予告が読めないと、柱3(害を与える前に見える)に反する。予告の長さと見た目の調整が必要。
- 戻しやすさ: 高。敵の型ごとに部屋への配置を外せば元に戻る。
- ビジョンとの適合: 高。深みを敵の挙動から生む、というD-001の趣旨そのもの。

**案2: 部屋の構成と進行を作る(既存の敵のまま、出し方と強さを変える)**

- 変更内容:
  - 時間差で敵を出す波、出現位置の指定(Spitter が通り道を撃ち抜く位置、Grub が背後から来る位置など)、部屋ごとの数と数値の上昇(Grub の速度、Spitter の発射間隔)を定義する。
  - 最初は敵の種類は2つのまま。
- 効く症状: A(部屋ごとに状況が変わる)、B(圧が上がる)、C(同時に複数の脅威が来るので、ダッシュで抜ける場面ができる)。
- コスト: 低。既存の敵とシステムだけで、主にデータと配置の変更。
- リスク: 数値を上げるだけだと、型は同じまま「速くなっただけ」になり得る。A の根本(P1)は解けない可能性がある。
- 戻しやすさ: 非常に高い。
- ビジョンとの適合: 高。ただし、効果は構成の作り込み次第。

**案3: プレイヤー側の数値を締める(「立って振る」が通らないようにする)**

- 変更内容:
  - 攻撃の回復を長くする、被弾後の無敵を短くする、Grub の体力を増やす、ダッシュのクールダウンを変える、などの調整。
  - さらに踏み込む場合は「ダッシュに攻めの使い道を与える」(例えば、ダッシュで敵を通り抜けると一瞬スタンさせる)という、キットの変更もあり得る。これは入力を増やさないので D-001 の範囲内だが、ダッシュの役割を変える点で、ワンボタン戦闘(柱1)の解釈に触れる。選ぶ場合は方向の判断が必要。
- 効く症状: B(罰が重くなる)、C(ダッシュが必要になる)。A への効果は小さい。
- コスト: 低(数値のみの調整)。キット変更を含めると中。
- リスク: 実機の感触(H1)が未確認のまま数値を触ることになる。敵が変わらないので、不快な縛りに感じられるおそれがある。30 FPS と 60 FPS の両方で、フレーム数ではなく秒で定義する必要がある。
- 戻しやすさ: 数値は高い。キット変更は中。
- ビジョンとの適合: 数値調整は適合。キット変更は柱1の解釈の確認が要る。

### 4. 推奨(根拠: 設計書と観察。実機の確認は未済)

**案2を先に行い、案1のうち「予告つきの Grub の突進」だけを同時に試す、という段階的な進め方を推奨する。**

- 理由:
  - 主因 P1(敵が単調)を解くのは案1だけ。しかし、新しい挙動は予告の見た目も含めて費用がかかる。
  - 案2は低コストで戻しやすく、P2(進行がない)を解く。
  - 案1の最小の一つ(Grub の突進)を足すと、C(ダッシュの使い道)に直接効く。Spitter の変化や新しい敵の種類は、結果を見てから決められる。
- 案3は、実機の感触を確認してから判断する。今は主案にしない。
- 反対の見方: 案1を全面的に進めれば、A の根本には強く効く。ただし、見た目の作業(予告の演出)と実装の量が増える。これはスコープの判断になる。

### 5. 検証すべき観点(後で Play や Review で、プレイヤーが観察できる形)

- 立ち止まって振り続けるだけでは、後半の部屋で被弾するか。
- 部屋ごとに、敵の出方や対応の仕方が違うと感じるか(「2分目と15分目が同じ」でなくなるか)。
- 突進の予告が、害を与える前に見えて読めるか(柱3)。
- ダッシュを、移動以外の戦闘の場面で自発的に使うか。使った理由を言えるか。
- 被弾が「自分の判断ミスのせい」と感じられるか(理不尽でないか)。
- 30 FPS と 60 FPS で、予告の長さや回避のしやすさが同じに感じられるか。

## Decisions already made

- D-001: 戦闘は攻撃ボタン1つとダッシュのみ。新しい入力ボタンは Owner の承認なしには追加できない。上の3案はいずれもこの範囲内で、D-001 の変更は不要。

## Constraints

- D-001 の枠内。ビジョンの柱(ワンボタン戦闘、短いラン、読める脅威)を保つ。
- 既存のシステムの再利用を優先する(小さなチーム)。
- 30 FPS と 60 FPS の両方で正しく動くこと。時間は秒で定義する。
- 範囲外: 戦闘以外のシステム、ラン長、ビジョンの柱の変更。
- 数値と仕様の最終決定は、方向が決まった後の仕様化で行う。

## Open questions

`game-director` に決めてほしいこと:

1. **方向の選択**: 案1(敵の挙動)、案2(部屋の構成)、案3(数値)のどれを主にするか。または推奨の段階的な組み合わせでよいか。これは優先度とスコープの本当の選択で、選び方によって作業量と見た目の作業が変わる。
2. **見た目の作業**: 案1は、予告の見た目(溜めの動き、効果音)が必要になる。`art-director` を巻き込むか。巻き込む場合、いつ。
3. **実現可能性**: 案1の敵の挙動追加と、案2の波の出現が、既存の敵と部屋のシステムでどこまで簡単にできるか分からない。`technical-director` に確認するか。
4. **実機の確認**: H1〜H4(操作感、実時間、演出、数値)を、次の Play で実機確認するのか。確認してから数値を決めるのか。
5. **欠陥 D**: `qa` の再現結果が出たら、ダッシュと被弾後の無敵の規則を設計書に書き足す。この件を G-001 に含めるか、別扱いにするか。

## Expected output

`game-director` が、案(または組み合わせ)、優先度、スコープを決める。その結果を決定として記録し(`make-decision`)、`game-designer` に仕様化(`write-design-spec`)を渡す。必要なら `art-director` と `technical-director` に確認を回す。D-001 の変更は必要ないので、Owner のエスカレーションは不要と見ている。

## Sender assessment

- 確信度: P1 と P2 が主因という診断は、設計書の記述と観察が一致しているので、中〜高。B3(被弾の罰の軽さ)と C2(ダッシュの攻めの使い道がない)は、設計書の未定義部分が多く、推定にとどまる。
- 観察はドライランで、感触に関わる原因(H1〜H4)は未確認。数値を決める前に、実機の確認が望ましい。
- 欠陥 D は、設計書の文面と矛盾する観察なので、実装の問題の可能性が高いと見るが、断定せず `qa` に任せる。
- 決定ファイル(`decisions/D-002-...`)は書いていない。方向を決めるのは `game-director` で、この段階で設計上の重要な決定は行っていないため。

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/make-decision.md
- Project: project.md#vision, project.md#constraints, project.md#current-state, design/combat.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/03-studio-to-game-designer.md
>>>END

## Validation feedback

A previous executor's output was rejected for these reasons. Produce the operation's files again, fixing them:

- goal.md: only one step (or one group of parallel steps 2a, 2b) may be open
