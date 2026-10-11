# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-dash-damage/25-technical-director-to-studio.md
next_seq: 26
context_request: allowed once (@need, up to 8 paths)
current_build: sim/build-0.4.md (newest simulated build; older ones are history)

## You may write

- goals/G-001-dash-damage/goal.md
- goals/G-001-dash-damage/25-technical-director-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-dash-damage/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 26
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
decisions/D-004-document-evaluation-scope.md
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
goals/G-001-dash-damage/24-studio-to-technical-director.md
goals/G-001-dash-damage/25-technical-director-to-studio.md
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
decisions/D-004-document-evaluation-scope.md — D-004: 模擬ビルドの文書評価を Goal の検証とする
>>>END

<<<FILE goals/G-001-dash-damage/goal.md
---
kind: goal
id: G-001
project: lantern-depths
status: active
created: 2026-10-10
---
# G-001: ダッシュ中の被ダメージに関する文書評価を完了する

## Owner request

当初の依頼：

> ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。

2026-10-11 の範囲変更：

> B。模擬専用のサンプルなので、模擬ビルド記述に基づく文書評価をこの Goal の検証とし、計測できない項目は未判定として明記したうえで Goal を閉じてください。

## Interpretation

D-004 に基づき、現資料と最新の模擬ビルド `sim/build-0.4.md`（変更識別子 `0.3-G001-15`）による文書評価を本 Goal の検証とする。確認できる文書上の整合、計測できず未判定となる項目、仕様不足、再開条件を報告し、変更後の完了条件に対する Review を経て閉じる。

全4環境の挙動実証や不具合解消の保証は完了条件としない。追加取得・計測、新規 simulator 開発、実機試験、追加実装、仕様変更、巻き戻し、無関係なバランス調整は対象外。

## Unknowns

- Observe：仕様不一致の照合と AC-1〜AC-6 の作成は完了。Owner の詳細条件の独立した試行再現とは扱わない。
- Diagnose / Plan：D-003 と模擬実装定義は存在する。残る仕事は現資料による評価と限界をまとめる報告作成。
- Decide：Owner が D-004 で文書評価への範囲変更を決定済み。
- Design：クールダウン0.6秒の起点は未定義。今回は不足として報告し、新たな仕様判断は行わない。
- Build：模擬変更の定義は完了。追加修正は不要。
- Verify：Handoff 21 の文書評価は完了、総合結果は `question`。条件別証拠と全4環境の計測は不足したまま。D-004 に従い文書評価を今回の検証とし、実証できない項目は未判定で残す。
- Play：体験評価を求める Goal ではないため省略。
- Review：報告が変更後の完了条件を満たすか、game-director が判断する。
- Next：Review 後、Studio が Owner 向け Outcome を記録して閉じる。

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
| 7a | Owner escalation 準備 | technical-director | prepare-owner-escalation | done | 22-studio-to-technical-director.md |
| 7a-owner | Decide 検証範囲変更 | owner | — | done | 23-technical-director-to-owner.md |
| 7b | Design クールダウン起点 | game-designer | write-design-spec | skipped | — |
| 7c | Verify 補完後の独立検証 | qa | verify-change | skipped | — |
| 7d | Diagnose 文書評価報告の整理 | technical-director | technical-plan | open | 24-studio-to-technical-director.md |
| 8 | Play | playtester | playtest-session | skipped | — |
| 9 | Review 変更後の完了条件 | game-director | review-outcome | planned | — |
| 10 | Next | studio | — | planned | — |

done は作業終了を示し、再現成功や検証合格を意味しない。主要結果は 11（不具合報告・AC）、13（計画）、15（模擬実装定義）、17（資料照合、question）、19（条件付き再計画）、21（文書評価、question）、23（Owner escalation、D-004 により resolved）。

行 7b・7c の省略は不足の解消ではなく、D-004 による完了条件の変更による。既存 QA 判定の再採点や、同じ不足入力での QA 再依頼は行わない。

## Route changes

2026-10-10 — 02・04・06・08 の入力不足が解消せず、09 で Owner に escalation。D-002 の継続判断と補足観察を受け、11 の不具合報告・AC、13 の計画と D-003 に基づき Build へ進んだ。

2026-10-11 — 15 の模擬実装定義と17の資料照合により build-0.4 と変更識別子の対応を採用。資料不足は19で再計画し、21の独立 QA は文書評価を完了したが証拠不足により question とした。

2026-10-11 — 外部照会手段未確保のため22で brief 作成を依頼し、23を Owner に提示して blocked-on-owner とした。問い合わせ済み・モデル不存在・検証 fail とは扱っていない。

2026-10-11 — Resume：Owner の B と文書評価による完了条件を D-004 に記録し、23を resolved、Goal を active に変更。追加計測・仕様判断は省略し、24で文書評価報告を technical-director に依頼。報告後の Review を planned とした。

## Next action

technical-director が `24-studio-to-technical-director.md` を受け、現資料による文書評価報告、未判定事項、再開条件を整理して Studio に返す。

Studio はその報告を game-director の Review に route する。変更後の Goal が満たされたとの判断を受けて Close し、文書評価の完了と挙動実証の限界を Owner 向け Outcome に明記する。追加の Owner 回答は不要。

## Outcome

文書評価報告と Review は未完了。Owner は D-004 により、模擬ビルド記述の文書評価を本 Goal の検証とし、計測不能項目を未判定と明記して閉じることを決定した。

模擬実装の定義と対象ビルドの識別は完了している。従来の独立 QA 総合判定は question のままであり、全4環境の条件別挙動や不具合解消の保証は得られていない。最終 Outcome は Review 後に記録する。
>>>END

<<<FILE goals/G-001-dash-damage/25-technical-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 25
from: technical-director
to: studio
stage: Route
outcome: done
---
# 25: technical-director → studio — 文書評価報告を完了し、変更後の完了条件の Review へ渡す

## Task

本報告を、D-004 による変更後の完了条件に対する game-director の Review へ渡してください。Review 後、Studio がその結果に基づいて Close を行ってください。

## Context

G-001 はダッシュ中の被ダメージを既存仕様に合わせる修正として開始した。条件別証拠の取得経路が確保できず、独立 QA の Handoff 21 は文書評価完了・総合判定 `question` を報告した。

Owner は D-004 で、模擬ビルド記述に基づく文書評価を本 Goal の検証とし、計測できない項目を未判定として報告したうえで閉じる方針を承認した。本 Step はその報告作成を完了したものであり、条件別試行の実施、QA 判定の変更、Goal 達成の自己承認ではない。

## Findings

### 1. 対象と参照資料

評価対象は **`sim/build-0.4.md`、変更識別子 `0.3-G001-15`**。`sim/repo-notes.md` の Implemented change identifier と Current build description が一致している。旧 build-0.3 を今回の評価対象とはしない。

| 参照資料 | 本報告での用途と限界 |
|---|---|
| `project.md#constraints` | dry-run、Desktop、30／60 FPS、キーボード／ゲームパッド、既存システム再利用と入力制約。実機や条件別試行の証拠ではない |
| `design/combat.md` の Player kit | ダッシュ、被害、入力不能、被弾後保護、予約攻撃、クールダウンの仕様 |
| `11-qa-to-studio.md` の受け入れ条件・再現比較手順 | AC-1〜AC-6、命中成立、比較条件、全4環境の要求。設定例は実施結果ではない |
| `sim/build-0.4.md` | 現在の模擬挙動を仕様と照合する主資料。条件別生成観察・計測ログではない |
| `sim/repo-notes.md` | 対象変更の識別、D-003 との技術的整合、提供情報の限界。実装説明を独立した挙動実証には用いない |
| `19-technical-director-to-studio.md` | 回帰の枝、必要証拠、将来の取得・検証経路。記載の計画を実行済みとは扱わない |
| `21-qa-to-studio.md` | 既存の独立 QA による文書評価、証拠不足、総合 `question` の記録 |
| D-001〜D-004 | 入力制約、継続判断、発生源別保護、今回の完了条件 |
| `23-technical-director-to-owner.md`、`24-studio-to-technical-director.md` | Owner の選択、照会状況、今回の報告範囲と後続工程 |

上記の提供原文を照合した。旧ビルド原文は本 packet にないため、修正前の挙動は Handoff 11・21 と D-002 の記録としてのみ参照する。同一条件での修正前後比較を実施したとは判断しない。

以下で「文書整合」は仕様と模擬挙動の記述が対応することを示し、条件別合格を意味しない。B-D は `sim/build-0.4.md` の「Dash and damage」、B-C は「Other controls and timing」を指す。

### 2. AC-1〜AC-6 の文書評価

期待値の出典は `design/combat.md` の Player kit と Handoff 11「修正の受け入れ条件」。

| AC・対象 | 文書上の評価と根拠 | 未判定事項 |
|---|---|---|
| AC-1：未被弾でのダッシュ、Grub／Spitter | 文書整合。B-D は両命中源についてダッシュ前半・後半を含む全時間の無被害と、先行被弾なしのハート不変を記述 | 未被弾の初期状態、入力受理、実際の開始・終了、各命中源の前半・後半の命中成立、ハート前後値 |
| AC-2：入力回復直後のダッシュ、Grub／Spitter | 文書整合。B-D は入力回復直後にダッシュしてもダッシュ中に被害を受けないと明記 | 初回被害、0.3秒の入力不能終了、最初の入力可能機会での操作・受理、ダッシュ中の命中とハート前後値 |
| AC-3：被弾保護がダッシュ途中で先に終了、Grub／Spitter | 文書整合。B-D の被弾後約0.70秒開始・約0.85秒命中の例は、被弾後0.8秒を過ぎてもダッシュが保護する記述 | 実際の時刻・フレーム順序、被弾保護終了より後かつダッシュ終了より前の命中成立と無被害 |
| AC-4：ダッシュ終了後に被弾保護が残る、Grub／Spitter | 文書整合。B-D の約0.34秒開始・約0.70秒命中の例は、ダッシュ終了が残存する被弾保護を切らない記述 | 実際のダッシュ終了、残存保護内の命中成立、ハート前後値 |
| AC-5：無保護時の Grub 接触 | 文書整合。B-D は1ハート減少、0.3秒入力不能、被弾後0.8秒までの保護を記述。約0.15／0.45／0.70秒の接触例も対応 | 初回・入力不能中・回復後の各接触、入力不能の開始・終了、回復後の入力受理、ハート前後値 |
| AC-6：距離・継続・予約攻撃 | 文書整合。B-D は障害物のない直線で4タイル／0.25秒、B-C はダッシュ中の攻撃入力が終了時に1回発動すると記述 | 移動端点・距離・継続時間、実際の終了フレーム、攻撃入力と発動時刻・回数 |
| AC-6：クールダウン | 0.6秒という数値は整合。B-C は既存の0.6秒制限を維持すると記述。ただし起点未定義のため完全な文書適合は未判定 | 起点の仕様、再使用可能時刻、制限内の拒否・経過後の受理。仕様不足と観察不足の両方がある |

Build 0.4 の記述に、これらの AC に反する具体的挙動は確認できなかった。ただし、時刻例は境界の厳密な前後に成立する命中の説明であり、測定されたイベント列ではない。

### 3. 必要な回帰の文書評価

期待値は既存戦闘仕様と D-003、枝の対応は Handoff 19・21 に基づく。各行の条件別結果は未判定。

| 回帰対象 | 文書上の評価と根拠 | 未判定事項 |
|---|---|---|
| 回帰1：被弾保護が先に終了し、ダッシュ保護が残る | 整合。B-D の約0.70秒開始・約0.85秒無被害、約1.10秒通常被害の例が対応 | Grub／Spitter それぞれの終了順序、残存保護中の命中、両保護終了後に新しい保護がない状態での通常被害 |
| 回帰2：ダッシュが先に終了し、被弾保護が残る | 整合。B-D の約0.34秒開始・約0.70秒無被害、約0.95秒通常被害の例が対応 | 両命中源について、ダッシュ終了後の残存保護と両保護終了後の通常被害 |
| 回帰3：防いだ複数命中が入力不能・保護を開始または延長しない | 整合。B-D は無害な命中が入力不能を再開せず、次に被害が可能となる時刻も遅らせず、複数の接触・弾でも同じと明記 | 両終了順序 × 両命中源について、異なるフレームで2命中以上、入力受理、元の期限、期限後の被害を結ぶ記録 |
| 回帰4：ダッシュ単独の複数命中と終了後 | 整合。B-D は先行被弾なしのダッシュ中無被害、複数命中でも同じ挙動、ダッシュ開始後0.40秒の通常被害を記述 | 未被弾状態、両命中源それぞれの複数命中、終了時刻、保護を持ち越さないことを示す終了後の被害 |
| Spitter の通常被害と弾消失 | B-D の無保護時1ハート被害は整合。衝突時の弾消失は維持宣言まで確認 | 命中・通常被害・弾消失の条件別記録。弾消失の修正前後比較 |
| 入力・移動等の維持 | B-C の攻撃・ダッシュ・ポーズは D-001 と整合。B-D は壁で移動が止まると記述。repo-notes は敵 AI、Flinch、移動、攻撃ダメージ・硬直の維持を宣言 | 各維持事項の独立した回帰記録。維持宣言だけから動作保証はできない |

技術記述として、repo-notes の「Player invulnerability」「Contact and projectile damage」は D-003 と整合する。保護を発生源別に保持し、論理和を共通被害入口で評価し、各終了処理が自身の保護だけを解除する。防いだ命中はハート、入力不能、被弾保護と期限を変更しない。この対応は実装説明の文書照合であり、独立 QA の証拠を追加するものではない。

### 4. 全4環境の証拠不足

U＝条件別証拠不足による未判定。US＝証拠不足に加え、クールダウン起点の仕様不足。

| 対象 | 30 FPS・キーボード | 30 FPS・ゲームパッド | 60 FPS・キーボード | 60 FPS・ゲームパッド |
|---|---|---|---|---|
| AC-1〜AC-4：各 AC、Grub／Spitter の各枝 | U | U | U | U |
| AC-5：Grub の初回・入力不能中・回復後 | U | U | U | U |
| AC-6：距離・継続・予約攻撃 | U | U | U | U |
| AC-6：クールダウン内／経過後 | US | US | US | US |
| 回帰1〜4：各終了順序・各命中源 | U | U | U | U |
| Spitter 通常被害・弾消失、その他の維持事項 | U | U | U | U |

Build 0.4 冒頭は全4環境への適用を宣言しているが、環境ごとの実施記録ではない。repo-notes「Limits of available implementation detail」も、時刻例が測定ログではなく、配置・衝突・初期ハート・試行総数を再構成できないと明記している。

すべてのセルで試行総数、有効数、無効数、不具合発生数は不明。ゼロ件や非発生には置き換えない。先行被弾源も推定しない。待ち時間変更、未被弾比較、命中源変更を含む Handoff 11 の比較手順について、条件別実施記録はない。

D-002 の60 FPS・ゲームパッドでの観察は修正前の体感による報告であり、最新ビルドの当該環境を実証する資料にはならない。

### 5. 仕様不足と観察証拠不足

**クールダウン0.6秒の起点は仕様不足。**  
combat は「Cooldown 0.6 s.」、AC-6 は0.6秒の維持、B-C は既存制限の維持までを定める。repo-notes も起点を開始または終了と特定できないと明記する。入力受理・ダッシュ開始・ダッシュ終了のどれから数えるかを現資料では確定できない。これは再使用の計測ログがないこととは別の不足である。技術側では決めず、将来必要なら既存原資料の回復、回復できなければ game-designer の仕様判断へ渡す。

**30 FPS の終了フレームと更新順序は観察・実装詳細の不足。**  
B-C は0.25秒が30 FPSで7〜8フレーム間隔の間、60 FPSで15フレーム間隔に相当すると説明するが、実際の終了表示フレームは確定していない。repo-notes もタイマー更新順序と最終区間の移動積分を未提示としている。これだけで継続時間違反とは判定せず、独自の丸め規則・許容差も設けない。将来、詳細が得られても期待値が定まらない場合に必要な仕様判断へ進む。

**完全同時の命中優先順位・入力不能中の予約入力は今回の AC で新たに定義しない。**  
Handoff 11 は完全同時境界を避け、入力回復後の操作を対象にしている。将来の検証で回避不能な場合のみ game-designer に返す。保存・復元、ダッシュ中断など未定義の挙動も本報告で追加しない。

### 6. 既存 QA 判定と今回の完了範囲

Handoff 21 の総合判定は **`question` のまま**。文書評価は完了しているが、条件別証拠と一部期待値が不足している。具体的な仕様不一致による `fail` ではなく、D-004 によって過去の判定が `pass` に変わることもない。

本 Step では、D-004 が求める文書評価、未判定事項、仕様不足、再開条件の報告を作成した。追加取得・問い合わせ・試行生成・計測・実機試験・実装・巻き戻しは実施していない。技術上の新たな選択もなく、D-005 は作成しない。

外部窓口については、Handoff 23・24 の記録どおり**照会手段未確保、問い合わせ未実施**。モデル不存在や永久に取得不能とは確認されていない。同じ不足を理由に今回の作業を再計測や QA 再依頼へ戻す必要はない。

### 7. 将来、独立した挙動検証を再開する条件

以下は将来の再開条件であり、今回の Review・Close の追加前提ではない。

1. **範囲と対象を再確認する。**  
   実際の不具合解消や全4環境での保証が必要になった場合、または条件別証拠・モデルへのアクセスが得られた場合、Studio を通じて必要な独立検証の範囲、対象ビルドと変更識別子、仕様・AC を確認する。新規 simulator 開発や実機試験は D-004 の承認範囲外として別途判断する。

2. **取得経路と資料の来歴を確保する。**  
   runtime 管理側などへの実際の照会経路、既存モデル・記録の有無、版・出典・対象変更との対応、FPS・入力方式の表現範囲を確認する。期待値の文章の再出力を試行結果として採用しない。

3. **期待値の不足を解消する。**  
   クールダウン起点の既存原資料を回復し、回復できなければ game-designer が判断する。30 FPS の更新順序等は資料を先に確認し、必要になった仕様判断だけを返す。

4. **条件別記録を揃える。**  
   全4環境・AC・各命中源・回帰の各枝に対し、配置と衝突条件、初期状態、先行被弾源、予定時刻と実際の時刻、フレームと処理順序、入力と受理、ダッシュ・保護・入力不能の遷移、命中成立、ハート前後値、移動、攻撃、再使用を記録する。試行一覧、無効理由、総数・有効数・無効数・発生数を対応づける。必要試行数や許容差は原資料の確認なしに定めない。

5. **独立 QA が証拠を評価する。**  
   命中不成立や必要順序の不成立を成功例に数えず、取得できた枝だけを評価する。部分結果を全環境へ一般化しない。資料取得→期待値・条件確定→記録生成→独立評価の依存順序を守る。

今回はコード変更がなく、並列実装は行わない。将来も、証拠生成の前提が未確定な段階で独立したログ生成を並列依頼しない。

### 8. Owner 向け結果文

対象の模擬ビルド `sim/build-0.4.md`（`0.3-G001-15`）の文書評価を完了しました。ダッシュ中の保護、被弾後の保護、通常被害、移動と予約攻撃は既存仕様と文書上整合しています。クールダウンは0.6秒という数値のみ確認でき、起点は未定義です。全4環境の条件別挙動と回帰は証拠不足により未判定であり、不具合解消や全条件合格は実証していません。既存 QA の `question` を維持し、D-004 に沿った報告を game-director の Review に渡します。

## Decisions already made

- [D-001](../../decisions/D-001-one-button-combat.md)：Owner 承認なしに戦闘入力を追加しない。
- [D-002](../../decisions/D-002-resume-with-owner-observations.md)：部分的な Owner 観察を受けて修正を継続した。今回の完了条件は D-004 により変更。
- [D-003](../../decisions/D-003-independent-invulnerability.md)：保護を発生源別に管理し、論理和で判定する。防いだ命中で保護を開始・延長しない。
- [D-004](../../decisions/D-004-document-evaluation-scope.md)：文書評価を本 Goal の検証とし、未判定事項と再開条件を報告して Review 後に閉じる。

## Constraints

- 文書整合、条件別実証、Goal の達成 verdict を区別する。
- QA の過去の `question` を変更せず、全条件合格や不具合解消を保証しない。
- 仕様、AC、試行数、クールダウン起点を補作しない。
- 追加取得・計測・開発・実装・巻き戻しを今回の完了条件に戻さない。
- 本報告は technical-director の報告作成完了であり、Review・Close は未実施。

## Open questions

- game-director：本報告は D-004 の変更後の完了条件を満たすか。

挙動の未判定事項と仕様不足は Findings に記録済み。今回、Owner に追加回答を求める質問はない。

## Expected output

Studio は本報告を game-director の Review へ route する。game-director は D-004 の変更後の完了条件に対して達成 verdict を返す。その結果に基づき Studio が Close を行い、文書評価による完了と未実証事項を終了記録に保持する。

## Load

- Report: goals/G-001-dash-damage/25-technical-director-to-studio.md
- Project: project.md#constraints
- Specification: design/combat.md
- Build: sim/build-0.4.md
- Technical reference: sim/repo-notes.md
- Acceptance criteria: goals/G-001-dash-damage/11-qa-to-studio.md
- Supporting plan: goals/G-001-dash-damage/19-technical-director-to-studio.md
- Existing QA assessment: goals/G-001-dash-damage/21-qa-to-studio.md
- Resolved escalation: goals/G-001-dash-damage/23-technical-director-to-owner.md
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-resume-with-owner-observations.md
- Decisions: decisions/D-003-independent-invulnerability.md
- Decisions: decisions/D-004-document-evaluation-scope.md
- Previous handoff: goals/G-001-dash-damage/24-studio-to-technical-director.md
- Routing note: Studio が Review の Role・Skill を指定する。未取得のモデル・条件別観察資料は Load に含めない。
>>>END
