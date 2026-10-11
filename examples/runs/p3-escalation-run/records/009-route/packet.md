# Studio operation packet

operation: Route
goal: G-002
step_artifacts: goals/G-002-combat-monotony/11-game-designer-to-studio.md
next_seq: 12
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-002-combat-monotony/goal.md
- goals/G-002-combat-monotony/11-game-designer-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-002-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 12
- @need: instead of all other files, once: one path per line (up to 8 project or Studio files) to add to this packet before you route

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
   Project Context sections and Decisions this step needs, and the previous Handoff. You choose
   files by name (the project file list); you do not need to read a file to list it — the recipient
   reads it. Never route a step to `studio` itself: the open step is always a Role's or the Owner's.
   When opening parallel steps, write one Handoff per step in the same Route (consecutive `seq`).
   If you truly cannot route without reading an artifact's content, an isolated runtime lets you
   request specific files once (`execution.md`, context request).
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
decisions/D-002-enemy-side-combat-depth.md
decisions/D-003-time-based-telegraphs-and-attack-limit.md
decisions/D-004-combat-timing-substeps-and-attack-slots.md
decisions/D-005-no-flinch-in-attack-phases-and-grub-lock.md
design/combat-enemy-depth.md
design/combat-enemy-visuals.md
design/combat.md
goals/G-002-combat-monotony/01-studio-to-playtester.md
goals/G-002-combat-monotony/02-playtester-to-game-designer.md
goals/G-002-combat-monotony/03-game-designer-to-game-director.md
goals/G-002-combat-monotony/04-game-director-to-owner.md
goals/G-002-combat-monotony/05-studio-to-game-designer.md
goals/G-002-combat-monotony/06-game-designer-to-technical-director.md
goals/G-002-combat-monotony/07-studio-to-art-director.md
goals/G-002-combat-monotony/08-technical-director-to-studio.md
goals/G-002-combat-monotony/09-art-director-to-studio.md
goals/G-002-combat-monotony/10-studio-to-game-designer.md
goals/G-002-combat-monotony/11-game-designer-to-studio.md
goals/G-002-combat-monotony/goal.md
project.md
sim/build-0.3.md
sim/repo-notes.md
>>>END

<<<FILE @decision-titles
decisions/D-001-one-button-combat.md — D-001: Combat uses one attack button plus dash
decisions/D-002-enemy-side-combat-depth.md — D-002: 戦闘の単調さは敵側の行動で解決する（ワンボタン維持）
decisions/D-003-time-based-telegraphs-and-attack-limit.md — D-003: Telegraphs are time-based with a 0.4 s floor, and at most 2 enemies attack at once
decisions/D-004-combat-timing-substeps-and-attack-slots.md — D-004: Combat time runs in bounded sub-steps, and a central arbiter grants attack slots
decisions/D-005-no-flinch-in-attack-phases-and-grub-lock.md — D-005: Hits never interrupt an enemy's attack cycle, and the Grub's direction locks 0.3 s before its lunge
>>>END

<<<FILE goals/G-002-combat-monotony/goal.md
---
kind: goal
id: G-002
project: lantern-depths
status: active
created: 2026-10-10
---
# G-002: Combat feels monotonous

## Owner request

> 戦闘が単調なので改善したい

## Interpretation

Success: in a playtest of the 5-room slice, the player has to make different decisions across rooms
(where to stand, when to dash, which enemy first) instead of repeating one pattern, and the Game
Director judges the monotony addressed on that evidence. Out of scope: new biomes,
meta-progression, run length. Also out of scope (Owner, D-002): a hold-to-charge attack.

## Unknowns

All stages of route pattern 2 are open: the monotony has not been observed or diagnosed, a
direction choice is likely (D-001 limits some options), new behavior will need a spec and a plan,
and it is an experience Goal (Play, Review).

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | playtester | playtest-session | done | 01-studio-to-playtester.md |
| 2 | Diagnose | game-designer | diagnose-experience | done | 02-playtester-to-game-designer.md |
| 3 | Decide | game-director | make-decision, prepare-owner-escalation | done (escalated) | 03-game-designer-to-game-director.md |
| 4 | Decide | owner | — | done (Option A, D-002) | 04-game-director-to-owner.md |
| 5 | Design | game-designer | write-design-spec | done | 05-studio-to-game-designer.md |
| 6a | Plan | technical-director | technical-plan | done | 06-game-designer-to-technical-director.md (result: 08-technical-director-to-studio.md) |
| 6b | Design (visual cues) | art-director | write-design-spec | done | 07-studio-to-art-director.md (result: 09-art-director-to-studio.md) |
| 7 | Design (spec rulings before Build) | game-designer | write-design-spec | open | 10-studio-to-game-designer.md |
| 8 | Build | gameplay-engineer | implement-change | planned | — |
| 9a | Verify | qa | verify-change | planned | — |
| 9b | Verify (visual) | art-director | visual-review | planned | — |
| 10 | Play | playtester | playtest-session | planned | — |
| 11 | Review | game-director | review-outcome | planned | — |

## Route changes

- After step 3: Option B would change Owner Decision D-001 while the evidence leaves A and B both
  viable → escalation triggers → step 4 (Owner); all later steps paused.
- After step 4: the Owner chose Option A (D-002) with the condition that a hold-to-charge attack is
  not part of this Goal. The remaining route matches Option A's "If chosen" (Design → Plan → Build →
  Verify → Play → Review), so steps 5–10 are unchanged. Goal set back to `active`. Step 9 must be
  routed to the Playtester through a fresh Studio-composed Handoff without implementation
  knowledge.
- After step 5: the spec leaves the visual design of telegraph cues, the Charger lane indicator and
  the block/stun cues undecided (Designer's Q1), and these affect what the player sees (pillar 3,
  readable threats). Added step 6b (Design, `art-director`) in parallel with Plan 6a: neither
  consumes the other's output. Because the change affects visuals, Verify gains a parallel visual
  review (8b). Build (7) waits for both 6a and 6b. If the cue designs need timing changes, they go
  back to `game-designer`, not decided by the Art Director.
- After steps 6a and 6b: both done and mutually compatible (cue interface, lock moments for Spitter
  and Charger, and shape types match). The plan fits Option A and the constraints (about 17–21
  person-days, D-003 revisit trigger not met), so no escalation and no return to Decide. But both
  results carry open spec questions that belong to `game-designer`: Flinch (SQ1, which decides
  whether telegraphs work at all), slot lifetime, obstacle stun, waiting behavior, guard reference
  point, the Grub lock timing (N1), and unspecified widths, angles and range (Q-A, Q-B). The
  Engineer must not decide these (return rule: Build with ambiguous spec → Design), so a new Design
  step 7 was inserted before Build. Later steps renumbered (Build 8, Verify 9a/9b, Play 10, Review
  11). If the rulings change a cue timing, step 7's result goes to `art-director` before Build. The
  Technical Director's F1–F7 feasibility checks for the cues and the saturated-color sprite check
  (F6) are left as first Build tasks; if one fails, Build returns to `technical-director` or
  `art-director`.

## Next action

game-designer starts step 7 (Design, spec rulings) from `10-studio-to-game-designer.md`, and
addresses the result to `studio`. Then the Route operation:
- decides whether `art-director` must revise any cue (only if a timing or shape changed), and
- writes the Build Handoff for `gameplay-engineer` from: `08-technical-director-to-studio.md` (task list T0–T9, D-004, cue interface, test strategy, Build A / Build B slicing), `09-art-director-to-studio.md` and `design/combat-enemy-visuals.md` (VC1–VC14), and the Designer's rulings. It must give acceptance checks V1–V11 and VC1–VC14 for QA, tell Build to state which SQ defaults it used, and ask for the result to be addressed to `studio`.

Pending Studio item: add `design/combat-enemy-depth.md` and `design/combat-enemy-visuals.md` to the Design index in `project.md` (not writable in this operation; do it in the next operation that can edit `project.md`).
When Build and Verify are routed, their Handoffs must ask for results addressed to `studio` (needed to compose the independent Playtester Handoff for step 10). VE1–VE5 (experience signals) and spec 7.2 stay out of the Playtester's handoff.

## Outcome

—
>>>END

<<<FILE goals/G-002-combat-monotony/11-game-designer-to-studio.md
---
kind: handoff
goal: G-002
seq: 11
from: game-designer
to: studio
stage: Design
outcome: done
---
# 11: game-designer → studio — Spec questions SQ1–SQ5, N1, Q-A and Q-B answered; spec updated

## Task

Merge these answers, `design/combat-enemy-depth.md` (updated), the Technical Director's plan and the Art Director's visual design into the Build Handoff. Send the Grub cue change to the Art Director (one cue, see below).

## Context

G-002 (D-002, enemy-side depth, one button). Handoff 10 asked for rulings on the questions found by the Technical Director and Art Director. All answers are now in the spec itself so Build and QA can verify from it. D-001–D-004 are unchanged: no new inputs, 0.4 s floor, cap of 2. Significant choices are recorded in D-005.

## Findings

### Answers

| Q | Answer | Reason |
|---|---|---|
| SQ1 Flinch | Flinch (0.2 s) applies only in Idle, Chase and Waiting. It is ignored in Telegraph, Active, Recovery, Stunned and Cooldown, for all four types (Grub, Spitter, Charger, Shieldbearer). Damage still applies. A blocked swipe causes no Flinch. Spitter in practice only flinches when Idle or Waiting (its 2 s interval is Cooldown). Spec 2.5. | A cancellable telegraph brings back "stand still and swipe" and breaks the Charger rule. |
| SQ2 Slot lifetime | Confirmed as proposed: taken in the update where Telegraph starts, held through Telegraph and Active, released at Recovery start (Spitter: when it fires), on death or room end. Shots in flight, Recovery, Stunned and Cooldown hold none. Spec 2.3. | This is the meaning of "in a telegraph or attack phase" in D-003, and it matches D-004. |
| SQ3 Obstacles | Yes: a charge ending on any static solid (wall or obstacle) gives the 1.5 s stun. Enemies, player and projectiles are not solids. The lane is cut at the first static solid. Spec 4.1, edge cases 5 and 10. | One rule for stopping; obstacles also make stuns achievable in more room layouts. |
| SQ4 Waiting | Per type, spec 2.3: Grub circles at half walk speed at 1.5 tiles (±0.25); Charger moves to 4–7 tiles with line of sight and holds; Shieldbearer keeps walking and turning but stops at 1.0 tile and does not bash; Spitter stays put. No cue and no damage while Waiting. FIFO grants, ties by lowest spawn index. | Waiting must be readable (no cue) and not start attacks; FIFO prevents starvation in room 5. The Charger and Shieldbearer differ from the TD defaults only in the stated distances. |
| SQ5 Guard point | The player's position at swipe time (projectile: its position when it reaches the shield), against the Shieldbearer's facing at that moment. Half-angle 60°, exactly 60° is blocked. Spec 4.2. | Matches the TD default; close side hits are not blocked by hitbox geometry. |
| N1 Grub lock | Not intended. The Grub tracks for 0.2 s, then locks for the last 0.3 s of the 0.5 s telegraph. Total time unchanged. Spec 3.1, D-005. | 0.3 s matches the Charger and is above a 0.25 s dash, so sidestep or dash is a real answer. |
| Q-A Spitter range | Projectile range 12 tiles; destroyed on a static solid or guard. The Spitter starts a telegraph only with the player within 12 tiles. Spec 3.2. | A range limit avoids wasting slots on unreachable targets. |
| Q-B hit areas | Grub lunge 1.0 tile wide × 2.0 long. Spitter projectile and line 0.25 tile wide (replaces the existing collision size if different). Shieldbearer bash 90° cone (±45°), 1.5 tiles from its center. Spec 3.1, 3.2, 4.2. | Matches the Art Director's assumptions; rules values, so cues follow them (F7). |

### Additional rulings (not asked, needed to avoid guessing in Build)

- Shieldbearer bash trigger: "front 60°" means ±30° from its facing (inside the ±45° cone). Spec 4.2.
- A Waiting Shieldbearer stops at 1.0 tile from the player; a Waiting Charger holds at 4–7 tiles. Spec 2.3.
- Spitter projectile hit width 0.25 tile replaces the existing size if different, and the Spitter does not telegraph beyond 12 tiles. TD: put these in the data table.

### Acceptance criteria changed (spec 7.1)

- V2: adds lock points (Grub 0.2 s, Charger 0.5 s, Spitter 0.4 s).
- V3: adds the lunge rectangle size.
- V5: now "wall or obstacle", plus the 0.8 s no-stun case for a full 8 tile charge.
- V6: guard check reference and 60° boundary; blocked swipes cause no Flinch.
- V7: adds bash cone size and trigger.
- V8: adds exact slot lifetime.
- New: V12 (Grub dodge in the final 0.3 s, or by dash), V13 (no flinch cancel; edge cases 8 and 10), V14 (Waiting, FIFO, Spitter range).
- New edge cases 8, 9 and 10 in spec section 6.
- Experience signals (7.2) unchanged; they stay out of the Playtester's handoff.

### Art Director: yes, one cue changes

- `design/combat-enemy-visuals.md` section 2.4 (lock points), section 3.1 (Grub lunge) and VC3: the Grub's lock change (thin dashed orange → thick solid red, 0.1 s flash, rim flash) now happens at **0.2 s ±0.05 s into the 0.5 s telegraph**, not at the lunge start. The locked state persists for the last 0.3 s, and the fill still reaches full exactly when the lunge starts. The arrow follows the player only for the first 0.2 s.
- No other cue changes. Grub width (1 tile), Spitter line width (0.25 tile) and bash cone (90°) are confirmed as drawn. New facts for the visuals: the aim line is drawn to the first static solid or guard, or at most 12 tiles; the Shieldbearer bash wedge is 90° and 1.5 tiles.
- The TD's `locked` flag for the Grub in the cue interface now flips at 0.2 s.

### For the Technical Director and Build

- T3 uses the new Grub timing. Put these in the data table: Grub tracking 0.2 s / locked 0.3 s, lunge 1.0 × 2.0, Spitter range 12 and width 0.25, bash cone 90° / 1.5 tiles / trigger ±30°, waiting distances.
- All five TD defaults are either confirmed or refined as above, so Build does not need to report a default used for SQ1–SQ5.
- No change to timings that touches the 0.4 s floor or the cap of 2.

## Decisions already made

- D-001: one attack button plus dash; no new inputs.
- D-002 (Owner): enemy-side depth; no hold-to-charge attack.
- D-003: time-based telegraphs, 0.4 s floor, at most 2 attackers.
- D-004: bounded sub-steps and a central slot arbiter.
- D-005 (new, mine): no Flinch in attack phases; slot lifetime; Grub lock 0.3 s before the lunge; hit-area values.

## Constraints

- Keep D-001–D-004. The Playtester's handoff must not include implementation details or the spec 7.2 / VE experience signals.
- Stay within the 5-room slice and the existing controller and data approach.
- `design/combat.md` is not changed; spec 2.5 is the Flinch rule for build 0.4.

## Open questions

- None for the Game Designer. Retune items (Q3 in the spec) wait for playtest. One watch item: two-swipe Grub kills inside its telegraph (edge case 4) are allowed, but Review should check this is not a new single tactic.

## Expected output

The Studio writes the Build Handoff and routes the Grub lock point change to the Art Director. Link both design files in the `project.md` Design index.

## Sender assessment

Confidence: high on SQ1 (the main risk to the Goal) and N1. Medium on the exact Waiting distances and the Spitter range of 12 tiles, which are first values chosen without room layout data; they are cheap to retune in the data table.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat-enemy-depth.md, design/combat-enemy-visuals.md, design/combat.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-enemy-side-combat-depth.md, decisions/D-003-time-based-telegraphs-and-attack-limit.md, decisions/D-004-combat-timing-substeps-and-attack-slots.md, decisions/D-005-no-flinch-in-attack-phases-and-grub-lock.md
- Previous handoff: goals/G-002-combat-monotony/10-studio-to-game-designer.md
>>>END
