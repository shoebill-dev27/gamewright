# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-dash-damage/23-technical-director-to-owner.md
next_seq: 24
context_request: allowed once (@need, up to 8 paths)
current_build: sim/build-0.4.md (newest simulated build; older ones are history)

## You may write

- goals/G-001-dash-damage/goal.md
- goals/G-001-dash-damage/23-technical-director-to-owner.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-dash-damage/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 24
- @need: instead of all other files, once: a file block `<<<FILE @need` with one path per line (up to 8 project or Studio files), then `>>>END`, to add them to this packet before you route

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
   *Route changes* in one or two lines (the Handoffs carry the details; `goal.md` is rewritten by
   every Route, so keep it short). Confirm (`planned`) or drop (`skipped`) any `tentative` stage
   whose condition this result settles. The route is a plan, not a contract.
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
  Art Director visual review of the same build). Each gets its own Handoff (consecutive `seq`).
  Steps open at the same time are parallel; label their rows as you like (e.g., 2a, 2b). The Route
  operation waits for all of them before moving on.
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
goals/G-001-dash-damage/20-studio-to-qa.md
goals/G-001-dash-damage/21-qa-to-studio.md
goals/G-001-dash-damage/22-studio-to-technical-director.md
goals/G-001-dash-damage/23-technical-director-to-owner.md
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

- Observe: QA は仕様不一致の照合と AC-1〜AC-6 の作成を完了した。Owner の詳細条件を独立した試行で再現したわけではない。
- Diagnose / Plan: 発生源別保護の計画と D-003 は確定済み。Handoff 19 の条件付き検証計画に対し、モデル・記録の取得経路は依然未確保。
- Decide: ゲームの方向選択は不要。ただし、Role が提供できない外部資料へのアクセス、または元の Goal の扱いについて Owner 向けの選択肢が必要。
- Design: QA は AC-6 のクールダウン起点を仕様不足と判定した。combat と repo-notes の原文にも起点はない。既存原資料が得られなければ game-designer が判断する。Studio や技術側では決めない。
- Build: 模擬実装変更の定義は完了。対象は `sim/build-0.4.md`、変更識別子 `0.3-G001-15`。資料不足を理由とする追加修正は未承認。
- Verify: Handoff 21 は文書評価を完了したが、総合結果は question。AC-1〜AC-6、全4環境、必要な回帰の条件別証拠が不足している。具体的な仕様不一致による fail ではない。
- Play / Review: 体験 Goal や方向 Decision を伴わないため省略。
- Next: 独立検証の結果、または Owner による範囲変更・中止の決定を受けて結果をまとめる。

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
| 6c | Plan 検証成立性の再検討 | technical-director | technical-plan | done | 18-studio-to-technical-director.md |
| 7 | Verify 文書評価・証拠充足性確認 | qa | verify-change | done | 20-studio-to-qa.md |
| 7a | Owner escalation 準備 | technical-director | prepare-owner-escalation | open | 22-studio-to-technical-director.md |
| 7b | Design クールダウン起点 | game-designer | write-design-spec | tentative | — |
| 7c | Verify 補完後の独立検証 | qa | verify-change | planned | — |
| 8 | Play | playtester | playtest-session | skipped | — |
| 9 | Review | game-director | review-outcome | skipped | — |
| 10 | Next | studio | — | planned | — |

done は各 Step の作業終了を示し、再現成功や Verify 合格を意味しない。主要な結果は Observe 1e＝`11-qa-to-studio.md`、Plan 2＝`13-technical-director-to-studio.md`、Build 6＝`15-gameplay-engineer-to-studio.md`、資料照合 6b＝`17-gameplay-engineer-to-studio.md`（question）、再計画 6c＝`19-technical-director-to-studio.md`、Verify 7＝`21-qa-to-studio.md`（question）。

行 7b は修正継続時に既存起点を回復できない、または資料間の矛盾が残る場合に実施する。既存原資料で解決すれば skipped とする。行 7c は元の Goal を維持する限り必須。両行は必要入力と継続方針が整うまで開始しない。現在開いている工程は行 7a の brief 作成である。

## Route changes

2026-10-10 — Handoff 02・04・06 の question に対して追加 Observe を設定した。08 でも同じ不足が解消せず、loop limits により 09 で Owner に escalation した。

2026-10-10 — Owner が継続と補足観察を選び、D-002 を記録。Observe 1e を再開し、11 の不具合報告・AC を受領した。Diagnose / Plan を行 2 に統合し、独立 Plan 行 5 は省略した。

2026-10-10 — 13 と D-003 を受け Build を開始。方向・視覚変更は不要として、game-director・art-director は追加しなかった。

2026-10-11 — 15 の模擬実装定義を受領。検証資料不足に対して資料照合 6b を追加し、17 に基づき build-0.4 と変更識別子の対応を採用した。

2026-10-11 — 17 の不足報告を受け、同じ資料生成要求を反復せず Plan 6c に戻した。19 の条件付き計画を受け、照会手段未確保のまま文書評価分岐で独立 QA に 20 を渡した。モデル不存在や取得不能の確認とは扱っていない。

2026-10-11 — 21 を受領し、行 7 を done とした。QA は条件別証拠を必須とし、文書整合だけでは検証未完了と判断した。fail ではないため Build への修正差し戻しや「同じ AC の二回目の失敗」は適用しない。

2026-10-11 — 既存の引継ぎでは repo-notes にも起点・衝突条件・イベント記録がなく、外部照会経路も未確保である。外部入力の blocker として、アクセス提供・範囲縮小・中止の Owner 向け brief 作成を 22 で technical-director に渡す。モデル不存在・照会実施済みとは断定しない。

2026-10-11 — 状態管理を訂正した。新しい open Escalation はまだないため Goal は active、行 7a は open とする。brief を受領し、Owner 宛ての open Escalation を Route する時点で blocked-on-owner に変更する。依存する実装・検証は開始しない。

## Next action

technical-director が `22-studio-to-technical-director.md` から Owner 向け Escalation を作成する。必要な外部入力、未確保の取得経路、影響する検証条件、選択肢と推奨案を日本語で明示する。

Studio はその成果物を次の Route で確認し、Owner 宛ての open Escalation として提示するときに Goal を blocked-on-owner にする。現在は brief 作成中であり、Owner の回答待ちではない。QA・実装への同じ不足入力での再依頼は行わない。

## Outcome

未完了。仕様不一致の確認、受け入れ条件、D-003 に基づく模擬実装変更と対象ビルドの識別は完了した。独立 QA は文書上の整合を確認したが、全4環境の条件別証拠不足とクールダウン起点の未定義により、検証結果は question。

必要資料へのアクセスを Role の作業だけでは確保できないため、technical-director が Owner 向けの選択肢を準備する。Goal はその作業中の active 状態である。修正完了・検証合格とは報告しない。追加 Owner 計測、新規 simulator 開発、検証要件の緩和は決定していない。
>>>END

<<<FILE goals/G-001-dash-damage/23-technical-director-to-owner.md
---
kind: escalation
goal: G-001
seq: 23
from: technical-director
to: owner
status: open
decision: null
---
# 23: Owner decision needed — ダッシュ被ダメージ修正の検証をどう進めるか

## Question

ダッシュ中の被ダメージ修正について、A「必要資料または取得窓口へのアクセスを手配して修正・検証を継続」、B「現資料による調査・文書評価報告へ Goal を縮小」、C「未検証事項を明記して中止」のどれを選びますか。

## Why this needs the Owner

必要な検証証拠を現資料や Role の作業だけでは作れず、その取得に必要な外部窓口・アクセスも確保できていません。外部入力の手配、または依頼範囲の変更・中止について判断が必要です。

D-002 では元の修正 Goal の継続が選ばれています。Studio が独自に検証要件を緩め、文書評価だけで修正完了とすることはできません。今回の再検討は、不可欠な情報を既存資料や Role の作業から得られない場合という D-002 の条件に対応します。

対象は模擬ビルド `sim/build-0.4.md`、変更識別子 `0.3-G001-15` です。独立 QA は Handoff 21 で文書評価を完了しましたが、総合判定は `question` です。具体的な仕様不一致を確認した `fail` や二度目の受け入れ失敗ではありません。条件別の生成観察・実測がなく、全4環境での検証は未完了です。

### 必要な外部入力と影響

| 必要な資料・アクセス | 影響する検証 | 候補提供元と現在の状態 |
|---|---|---|
| 対象変更との対応、版・出典・初期状態、FPS・入力方式の表現範囲が分かるモデル情報と観察の来歴 | 全条件の証拠として採用できるか | runtime 管理側が候補。窓口・照会手段は未確保、保有状況も未確認 |
| 配置・衝突条件、先行被弾源、命中成立、入力と受理、ダッシュ・被弾保護・入力不能の開始終了、ハート前後値の条件別記録 | AC-1〜AC-5、Grub／Spitter、両保護の終了順序・複数命中・保護終了後の被害・弾消失などの回帰 | 既存モデル・保存記録の管理側が候補。所在・取得方法は不明 |
| 移動距離・継続時間、予約攻撃の入力と発動時刻・回数、再使用の拒否・受理、時刻とフレーム内順序の記録 | AC-6、特に30 FPSの終了時刻と状態遷移 | runtime のモデル・観察資料が候補。未取得 |
| 試行一覧、有効・無効の理由、各記録と集計の対応 | 全条件の試行総数・有効数・無効数・不具合発生数 | 条件別記録の管理側が候補。件数はすべて不明 |
| クールダウン0.6秒の起点を定めた既存原資料 | AC-6の再使用可能時刻 | 既存仕様・旧モデル等が候補。所在不明。回復できなければ game-designer の仕様判断が必要 |

対象環境は30／60 FPS × キーボード／ゲームパッドの全4環境です。AC-1〜AC-6、必要な命中源・比較・回帰を維持します。命中しなかった試行を無敵の成功例に数えることはできません。

既存資料には衝突形状・速度・座標・弾道・発射位相がなく、フレーム別試行や試行総数を復元できません。dry-run 規約は runtime の simulator による更新を定めていますが、モデルへのアクセスや条件別観察の生成能力を保証していません。

取得経路の状態は「照会手段未確保」です。問い合わせ実施済み、モデル不存在、永久に取得不能とは判断していません。Handoff 19 が想定した runtime 管理側への確認は未実施であり、その escalation 条件がすべて成立したと扱うものではありません。今回は、その確認自体を始められないことが blocker です。Owner がモデルを保有しているとも仮定していません。

## Options

### Option A — アクセスを手配し、元の修正 Goal を継続する

必要資料を扱う runtime 管理側の窓口・取得手段、または出典付きの既存モデル・記録の提供を手配します。まず必要なのはアクセスであり、Owner 自身の追加計測を開始条件にはしません。

ゲーム仕様と元の検証範囲を維持します。D-001 の入力制約、D-003 の発生源別保護の論理和を変更しません。資料が提供されても、十分性や検証合格は保証されません。

費用・所要時間は、窓口、資料の有無、提供範囲、既存モデルの能力が分かるまで不明です。取得しても一部条件しか補えず、再判断が必要になるリスクがあります。アクセス確認後に B／C を再検討でき、今回の選択だけで新規 simulator 開発や実機試験を承認することにはなりません。

選択後の route：
Studio が取得経路と提供範囲を具体化し、実際に取得した資料を次の packet に収録します。technical-director の Handoff 19 に沿い、gameplay-engineer が対象変更との対応と入力の不足を照合します。既存モデルで可能な補完のみを具体化し、取得・生成された証拠を独立 QA に戻します。部分結果を全環境へ一般化しません。

クールダウン起点は観察不足とは別の仕様問題です。既存原資料を回復できなければ Studio から game-designer に返します。新規 simulator 開発・実機試験が必要と判明した場合は、着手前に別途 scope 判断へ戻します。

### Option B — 調査・文書評価報告へ Goal を縮小する

成果物を「現資料で分かること、文書上の整合、未検証事項と再開条件の報告」に変更します。元の「修正を独立検証する」という依頼を変更するため、Owner の明示的な再解釈が必要です。

追加の資料取得・試行を今回の完了条件から外せますが、ダッシュ中の被害が全4環境で解消したとは保証できません。「修正の独立検証完了」「全条件合格」とは報告しません。ゲーム仕様や既存ビルドを変更・巻き戻す選択ではありません。

既存資料の整理が中心となりますが、必要工数は未見積もりです。未検証の挙動を残すリスクがあります。後から修正検証へ戻せますが、Owner による再度の範囲設定と Option A の入力確保が必要です。

選択後の route：
Studio が Owner の範囲変更と新しい完了条件を記録し、報告作成へ route します。報告には QA の `question`、全4環境の証拠不足、クールダウン起点の不足を残します。変更後の Goal に対する Review を経て扱いを決め、選択だけで完了にはしません。

### Option C — 未検証事項を明記して中止する

元の修正 Goal を中止し、`abandoned` とします。追加の資料取得・実装・検証は進めません。模擬変更は記録に残りますが、その有効性について検証合格を主張しません。この選択は変更の巻き戻しを意味しません。

今後の検証作業を止められますが、不具合解消を保証できない状態が残ります。中止記録の整理工数は未見積もりです。将来の再開は可能ですが、Owner の再開判断、対象ビルド・仕様の再確認、必要資料の確保から再開します。

選択後の route：
Studio が中止判断と未検証事項を記録し、Goal を `abandoned` にします。再開する場合は Studio を通じて範囲を確認し、Option A の取得・入力照合経路へ戻します。

## Studio recommendation

**Option A を推奨します。** まず窓口・アクセス、または出典付き既存資料を確保できるか確認し、元の修正 Goal を維持する案です。これは推奨であり、選択済みではありません。

## Reasoning

D-002 で選ばれた修正継続に沿い、QA が不足とした証拠を補える可能性があります。現時点で具体的な仕様不一致は確認されていませんが、文書整合だけでは条件別合格を代替できません。新しいモデルや一般的な挙動宣言を作って検証結果とすることもできません。

アクセスの実行可能性、取得・補完の費用と期間は不明です。次の情報が判明すれば推奨を見直します。

- 既存資料では必要条件を表現できず、新規 simulator 開発や実機試験が必要となる場合。
- 取得経路を確保できない理由、または取得・補完の費用が明らかになり、Owner の許容範囲を超える場合。
- Owner が現資料による報告に価値を認め、修正の独立検証を今回の成果に求めない場合は B。
- 報告への縮小も望まず、これ以上の対応を終える場合は C。

提供期限や開発費は設定していません。Owner は選択時に許容できる条件を付けられます。

## Meanwhile

この Step では本 brief の作成のみを行いました。資料取得、問い合わせ、試行生成、追加実装、独立検証、仕様判断は実施しておらず、回答に依存する工程は開始していません。独立して継続できる残作業はありません。

Goal は現在 `active` のままです。次に Studio が本 Escalation を Route して Owner に提示し、その時点で Goal を `blocked-on-owner` に変更して回答待ちを記録します。本 Step では状態変更や D-004 の採択を行いません。

## Owner decision required

**A／B／C と、あれば条件を回答してください。**

A の場合、分かる範囲で資料の提供先・取得窓口・アクセス手配の方法を添えてください。不明なら不明と回答できます。その場合も取得済みとは扱わず、Studio が手配上の未解決事項を残します。Owner 自身による追加計測は必須ではありません。

B は調査・文書評価報告への範囲変更、C は未検証のままの中止への明示的な同意として記録します。
>>>END
