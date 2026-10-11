# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-dash-damage/21-qa-to-studio.md
next_seq: 22
context_request: allowed once (@need, up to 8 paths)
current_build: sim/build-0.4.md (newest simulated build; older ones are history)

## You may write

- goals/G-001-dash-damage/goal.md
- goals/G-001-dash-damage/21-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-dash-damage/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 22
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
- Diagnose / Plan: 共有無敵フラグの解除競合の診断と発生源別保護の計画は完了。追加 Plan の結果 `19-technical-director-to-studio.md` は、既存モデルの取得可否に応じた条件付き検証計画であり、入力取得や検証の完了ではない。
- Decide: 既存仕様への修正に方向選択は不要。D-002 は不足入力を補完して継続する Owner の決定。D-003 は既存仕様を維持する技術方式の決定。
- Design: QA によれば期待挙動と受け入れ条件は明確。ただしクールダウン起点の原資料による回復は未確認。期待挙動が未定義または矛盾すると QA が判断した場合は game-designer に戻す。入力不能中の予約入力や完全同時の境界処理は今回新たに定義しない。
- Build: `15-gameplay-engineer-to-studio.md` に模擬実装変更を定義済み。`17-gameplay-engineer-to-studio.md` の照合報告に基づき、`sim/build-0.4.md` を変更識別子 `0.3-G001-15` の模擬ビルドとして扱う。ファイル名を合わせるための再生成は不要。
- Verify: Build 後は必須。独立 QA が既存仕様・AC・模擬ビルドから文書評価可能な範囲と証拠の十分性を判断する。PC・30 / 60 FPS・キーボード / ゲームパッドの全4組合せ、AC-1〜AC-6 と必要な回帰を維持する。条件別試行資料は未取得であり、文書評価を試行実施と扱わない。
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
| 6c | Plan 検証成立性の再検討 | technical-director | technical-plan | done | 18-studio-to-technical-director.md |
| 7 | Verify 文書評価・証拠充足性確認 | qa | verify-change | open | 20-studio-to-qa.md |
| 8 | Play | playtester | playtest-session | skipped | — |
| 9 | Review | game-director | review-outcome | skipped | — |
| 10 | Next | studio | — | planned | — |

過去の Observe の done は入力確認作業の終了を表し、再現確認の成功を表さない。1d の結果は `08-qa-to-studio.md`。1e の結果は `11-qa-to-studio.md`（done）であり、仕様不一致の照合と受け入れ条件の作成が完了した。行 2 の結果は `13-technical-director-to-studio.md`（done）。独立した Plan 行 5 は行 2 に統合したため skipped。

行 6 の結果は `15-gameplay-engineer-to-studio.md`（done）。変更記述を模擬実装とするプロジェクト規約に従う完了であり、simulator の資料生成や独立 Verify の合格を意味しない。

行 6b の結果は `17-gameplay-engineer-to-studio.md`（question）。done は照合と不足の報告が終了したことを示し、検証入力の完成を意味しない。

行 6c の結果は `19-technical-director-to-studio.md`（done）。条件付き計画の作成が終了したことを示し、モデル照会、資料生成、QA 判定は未実施である。

## Route changes

2026-10-10 — `02-qa-to-studio.md`（question）を受領し、1 を done とした。再現条件不足により追加 Observe を設けた。期待挙動の仕様不足ではないという QA の報告を受け、Design を skipped とした。

2026-10-10 — `04-qa-to-studio.md`（question）を受領し、1b を done とした。補足資料が未提供のため、資料受領を開始条件とする 1c を設けた。

2026-10-10 — `06-qa-to-studio.md`（question）を受領し、1c を done とした。資料受領を開始条件とする 1d を設け、実行環境側の補完を待つ方針とした。当時は Owner escalation を行わなかった。

2026-10-10 — `08-qa-to-studio.md`（question）を受領し、1d を done とした。同じ不足入力について新しい該当資料がないまま question が二回以上返ったため、loop limits を適用した。`09-studio-to-owner.md` に必要入力と選択肢をまとめ、Goal を blocked-on-owner とした。

2026-10-10 — Owner が Option A を選び、新しい観察を提供した。選択と回答原文を D-002 に記録し、09 を resolved、Goal を active とした。Observe 1e を追加した。体感による時刻や頻度を計測値とせず、部分資料から判断可能な範囲を QA に委ねた。

2026-10-10 — `11-qa-to-studio.md`（done）を受領し、1e を done とした。QA は不具合報告と AC-1〜AC-6 を作成し、追加の Owner 計測を必須とせず技術調査へ進めると報告した。Diagnose と Plan を行 2 に統合し、行 5 は skipped とした。Build と Verify は維持した。

2026-10-10 — `13-technical-director-to-studio.md`（done）を受領し、行 2 を done、行 6 を open とした。D-003 に基づく方式と実装順序を technical-director の判断として引き継いだ。実装は逐次、完了後に独立 QA の Verify を行う。視覚変更は計画にないため art-director の追加は不要。

2026-10-11 — `15-gameplay-engineer-to-studio.md`（done）を受領し、行 6 を done とした。模擬実装の定義は完了したが、指定生成先 `sim/build-0.3-G001-15.md` と `sim/qa-G001-15.md` は存在一覧になく、検証入力が揃ったとは判断できなかった。一方、一覧には `sim/build-0.4.md` があったため、行 6b を追加して既存資料の照合・補完を依頼した。Verify は planned のまま維持した。

2026-10-11 — `17-gameplay-engineer-to-studio.md`（question）を受領し、行 6b を done とした。工程担当の照合報告に基づき、build-0.4 と変更識別子 `0.3-G001-15` の対応を採用する。ファイル名の違いは解消済みとして扱う。一方、条件別試行記録、試行生成用の既存モデル、クールダウン起点は不足している。実装への同じ補完要求を繰り返さず、Build の計画不成立に対する return rule を適用し、行 6c を追加して technical-director に検証成立性を戻した。これは QA の fail や同一 AC の二回目の失敗ではない。

2026-10-11 — `19-technical-director-to-studio.md`（done）を受領し、行 6c を done、行 7 を open とした。本 packet の project.md、存在一覧、Handoff 19 には runtime 管理側の窓口・照会手段がない。取得経路の状態は「照会手段未確保」であり、管理側への照会を実施した、またはモデルが存在しないとは記録しない。

取得済みモデルを前提とする工程担当への再依頼は行わず、19 の文書評価分岐に沿って、独立 QA に既存資料で評価できる範囲と証拠不足の判断を依頼する。取得不能が確定したわけではなく、QA 相談はモデル取得可能性の調査を代替しない。Studio 自身を open の受信者にしない。

QA には Studio 作成の `20-studio-to-qa.md` を渡す。前 Handoff 19 は Load に明記し、参照範囲を `Constraints` と `Open questions` に限定する。実装理由・原因説明・自己評価を含む工程担当 Handoff 全文は渡さない。仕様・AC 原文と模擬ビルドを評価対象とし、未生成資料は Load に入れない。

今回は仕様・AC・証拠要件の変更、Verify の合否判断、Owner escalation は行わない。QA が必須証拠の不足を返した場合、同じ不足の照会を無変更で反復しない。Role が解消できない必須外部入力または Goal の再解釈が必要と判明した段階で、該当する escalation trigger を適用する。

## Next action

QA が新しい独立した実行コンテキストで `20-studio-to-qa.md` を開始し、仕様・AC と模擬ビルドの対応、評価可能な範囲、条件別の証拠不足、仕様上の未解決事項を Studio に返す。

runtime の照会手段は未確保である。QA の判断を受けて、Studio が具体的な資料取得、必要な Design、または外部入力に関する Owner escalation を手配する。資料不足を修正完了や試行合格に読み替えない。

## Outcome

未完了。仕様不一致の確認、受け入れ条件、技術計画、模擬実装変更の定義、および更新ビルドの識別が完了した。D-002 に基づき継続し、D-003 の発生源別無敵管理が反映されたとの照合報告を受領した。条件付き検証計画の作成を終え、独立 QA に文書評価と証拠の十分性の判断を依頼する。条件別観察資料は未取得であり、独立検証の合格は未確定。現時点で Owner に新たな判断を求める事項はない。
>>>END

<<<FILE goals/G-001-dash-damage/21-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 21
from: qa
to: studio
stage: Route
outcome: question
---
# 21: qa → studio — 文書上の整合を確認、条件別証拠とクールダウン起点は未確認

## Task

全4環境・AC-1〜AC-6・必要な回帰の条件別観察を取得する経路と、クールダウン起点の原資料を確保する。取得可能な資料を揃えて独立 QA に戻す。現時点で Verify 完了・Goal 完了として扱わない。

## Context

Owner の依頼はダッシュ中の被ダメージ修正である。対象は `sim/build-0.4.md`、識別子は `0.3-G001-15`。

本 Step は `studio/skills/verify-change.md` を適用し、既存仕様、指定された AC・再現比較手順、模擬ビルドを独立に照合した。前 Handoff 19 は Constraints と Open questions のみを参照した。実装者の理由・自己評価は根拠としていない。

dry-run のビルド読解による文書評価は完了した。条件別生成観察・実測は提示されておらず、条件別試行の実施結果はない。総合 verdict は `question`。確認された不一致による `fail` ではない。

## Findings

### 証拠の採否

| 資料 | 採用する用途 | 採用しない用途 |
|---|---|---|
| `design/combat.md#player-kit` | ダッシュ全時間無敵、距離・継続、被害・入力不能・被弾後保護、予約攻撃、クールダウンの期待値 | 実施結果、クールダウン起点の確定 |
| `11-qa-to-studio.md` の受け入れ条件・再現比較手順 | 必須条件、命中の成立、有効な時間関係、全4環境の検証要件 | 記載された設定例を実測値とすること |
| `sim/build-0.4.md` | 対象ビルドの挙動記述としての文書照合 | 条件別試行記録、生成観察、発生率 |
| `sim/build-0.3.md` | 従来はダッシュ途中の被害が記述されていたことの比較 | 同一条件による修正前後試行 |
| `project.md#constraints` | dry-run、Desktop、30／60 FPS、両入力方式の対象範囲 | 全環境で検証済みという証明 |
| Handoff 20 の D-003 要約 | 発生源別保護の論理和、防いだ命中で保護を開始・延長しないという承認済み期待 | 実装適合の証拠 |

Build 0.4 の時刻例は「命中が成立し、境界の厳密な前後にある挙動」の記述として採用できる。ただし、個々の環境でその状態を生成した記録ではない。冒頭の全環境への適用宣言も条件別実施記録には代えられない。

### AC ごとの文書評価

以下の「文書整合」は条件別合格を意味しない。期待値の出典は `design/combat.md#player-kit` と `11-qa-to-studio.md#修正の受け入れ条件`。ビルド参照節は B-D＝`sim/build-0.4.md#dash-and-damage`、B-C＝同 `#other-controls-and-timing` とする。

| ID・対象 | 期待挙動 | ビルド記述と文書評価 | 条件別証拠の不足 |
|---|---|---|---|
| AC-1：未被弾、Grub／Spitter | ダッシュ中の命中でハート不変 | B-D は先行被弾なしでもダッシュ中の命中は無害と明記。文書整合 | 未被弾の初期状態、入力・受理・開始終了、両命中源の成立とハート前後値 |
| AC-2：入力回復直後、Grub／Spitter | 実際のダッシュ中はハート不変 | B-D は入力回復直後のダッシュも保護すると明記。文書整合 | 初回被害、入力不能終了と直後の受理、ダッシュ中の命中、ハート前後値 |
| AC-3：被弾保護が先に終了、Grub／Spitter | 被弾後0.8秒を過ぎてもダッシュ中はハート不変 | B-D の約0.70秒開始・約0.85秒命中が対応。文書整合 | 実際の各イベント時刻・順序、0.8秒経過後かつダッシュ終了前の命中成立 |
| AC-4：ダッシュが先に終了、Grub／Spitter | ダッシュ終了後も被弾後0.8秒までハート不変 | B-D の約0.34秒開始・約0.70秒命中が対応。文書整合 | 実際のダッシュ終了、残存保護内の命中成立、ハート前後値 |
| AC-5：無保護時のGrub接触 | 1ハート減、0.3秒入力不能、被弾後0.8秒まで追加被害なし | B-D の通常被害と約0.15／0.45／0.70秒接触例が対応。文書整合 | 初回・入力不能中・回復後の接触結果、入力不能開始終了と操作の受理、ハート前後値 |
| AC-6：通常移動・予約攻撃・再使用 | 4タイル／0.25秒、終了時に予約攻撃、0.6秒クールダウン維持 | B-D は障害物のない直線で距離・継続を明記。B-C は終了時の攻撃1回、既存0.6秒制限を明記。距離・継続・攻撃は文書整合。クールダウンは数値のみ整合 | 移動開始終了・距離、攻撃入力と発動時刻・回数、起点の定義、制限内拒否・経過後受理の記録 |

Build 0.4 に、今回の AC に反する具体的挙動は確認できなかった。AC-6 のクールダウン起点は期待値自体が不足しており、完全な文書適合を判定できない。

### 回帰の文書評価

期待値は既存戦闘仕様と D-003 要約による。各行とも条件別結果は未確認。

| 枝 | 期待挙動 | 文書上の根拠・評価 | 不足する観察 |
|---|---|---|---|
| 被弾保護が先に終了 | ダッシュ保護が残る | B-D の約0.70秒開始例。整合 | 両保護の終了順序と、その間の両命中源による命中 |
| ダッシュが先に終了 | 被弾保護が残る | B-D の約0.34秒開始例。整合 | 同上 |
| 両保護終了後 | 新しい保護がなければ通常の1ハート被害 | B-D の約1.10秒／約0.95秒命中例。整合 | 各終了順序の後で両命中源による被害と新しい保護の有無 |
| 防いだ複数命中 | 入力不能や保護を新規開始・延長しない | B-D は複数の無害な接触・弾にも同じ結果と明記。整合 | 複数命中の時刻、操作受理、当初の保護終了後の被害 |
| ダッシュ単独の複数命中と終了後 | ダッシュ中は無害、終了後に保護を持ち越さない | B-D は先行被弾なし・開始後0.40秒の被害と複数命中の挙動を記述。整合 | 未被弾状態、両命中源の複数命中、終了後の命中と被害 |
| Spitter通常被害・弾消失 | 無保護時の被害と衝突時消失を維持 | B-D は通常1ハート被害と弾消失の維持を記述。前者は文書整合、後者は維持宣言まで | 命中・被害・弾消失を結ぶ条件別観察。旧ビルドには消失の比較記録なし |

新しい入力は B-C に記述されておらず、攻撃・ダッシュ・ポーズのみという制約と整合する。部屋攻略の一般記述は無敵やクールダウンの条件別検証には用いない。

### 全4環境の判定

U＝条件別証拠不足により未判定。US＝証拠不足に加えてクールダウン起点が未定義。

| 対象 | 30 FPS・キーボード | 30 FPS・ゲームパッド | 60 FPS・キーボード | 60 FPS・ゲームパッド |
|---|---|---|---|---|
| AC-1：Grub／Spitterそれぞれ | U | U | U | U |
| AC-2：Grub／Spitterそれぞれ | U | U | U | U |
| AC-3：Grub／Spitterそれぞれ | U | U | U | U |
| AC-4：Grub／Spitterそれぞれ | U | U | U | U |
| AC-5：Grub、初回・入力不能中・回復後 | U | U | U | U |
| AC-6：移動・予約攻撃 | U | U | U | U |
| AC-6：クールダウン内／経過後 | US | US | US | US |
| 上記回帰の各枝・各命中源 | U | U | U | U |

すべてのセルで試行総数・有効数・無効数・不具合発生数は不明。ゼロ件・非発生として報告しない。先行被弾源も記録がなく、推定しない。

`11-qa-to-studio.md#後続で実施する再現・比較手順` にある、待ち時間を変えた比較、未被弾比較、命中源変更、全4環境での確認は、条件別実施記録としては未確認である。Build 0.3 と0.4の照合では「ダッシュ途中で被害」から「全時間無害」への記述変更を確認できるが、同じ配置・入力時刻での再現と修正確認にはならない。

### 仕様不足と観察不足の分離

1. **クールダウン起点：仕様不足。**  
   `design/combat.md#player-kit` の原文は “Cooldown 0.6 s.”、AC-6 は「クールダウン 0.6 秒を維持する」、B-C は “existing 0.6-second cooldown”。開始・終了・入力受理のどれを起点とするかは記載がない。これらの数値に矛盾はないが、再使用可能時刻を一意に定められない。既存の起点を定めた原資料を回復し、なければ Studio から game-designer に返す。QA は起点を決めない。

2. **30 FPS の終了表示・フレーム内順序：観察不足。**  
   B-C は0.25秒が7〜8フレーム間隔の間に位置すると説明するが、実際の終了更新フレームを示さない。この記述だけで継続時間違反とは判定できない。内部の経過時刻・状態遷移と表示更新の関係が必要。証拠取得後も期待値を定められない場合に限り、必要な仕様判断を返す。

3. **完全同時の命中優先順位・入力不能中の予約入力：今回の AC で未定義のまま。**  
   AC は完全同時の境界を避け、入力回復後の操作を確認する。これらを新規仕様として決めることは今回の開始条件ではない。検証上避けられない場合は game-designer に返す。

### 必須追加入力

| 入力 | 影響するセル・必要な理由 | 既知の取得元・取得状況 |
|---|---|---|
| 対象識別子に対応した条件別生成観察 | 全セル。環境・AC・命中源・枝ごとの独立判定に必要 | runtime の simulator が更新を担うことは project.md に記載。窓口・取得手段は不明 |
| 観察の来歴とモデル情報 | 全セル。対象変更との対応、版、初期状態、FPS・入力方式の表現範囲を判断するため | runtime 管理側が候補。提供主体・取得方法は未確認 |
| 再現・比較条件とイベント記録 | AC-1〜AC-5と回帰。配置、敵数、位置・方向、先行被弾源、命中成立、入力と受理、ダッシュ・保護・入力不能の開始終了、ハート前後値が必要 | 条件別観察資料としての提供が必要。既存資料の所在は不明 |
| 移動・予約攻撃・再使用記録 | AC-6全環境。距離・継続、攻撃発動1回、制限内拒否・経過後受理を判定するため | 同上 |
| 試行一覧と集計根拠 | 全セル。試行総数・有効数・無効数・発生数と各記録の対応、無効理由を確認するため | 同上。命中しなかった試行を無敵の成功例に数えない |
| クールダウン起点を定めた既存原資料 | AC-6の再使用判定。期待時刻を確定するため | 現 packet の combat・AC・build にはない。原資料の所在は不明。回復できなければ game-designer の判断が必要 |
| 時刻・フレーム・イベント順序の説明 | 特に30 FPSのAC-2〜AC-4・AC-6、回帰の終了順序。命中が境界の内外どちらか判定するため | runtime のモデル／観察資料が候補。未取得 |

`sim/qa-G001-15.md` は未取得という引継ぎがあるだけで、存在・内容を確認できない。必須なのは上記の内容であり、そのファイル名であることではない。未生成・未取得資料を Load に含めない。

既存の仕様文書を補完できればクールダウン起点の不足は解消し得る。Build 本文への一般的な適用宣言の追加だけでは条件別試行要件は満たせない。既存の生成記録があるなら、その来歴・条件・結果の提供で解消できる可能性があるが、存在は未確認である。

照会経路の状態は引き続き「照会手段未確保」。問い合わせ実施済み、モデル不存在、取得不可能のいずれも断定しない。新規 simulator 開発や追加 Owner 計測を要求していない。

## Decisions already made

- D-001：攻撃・ダッシュ・ポーズ以外の入力を追加しない。
- D-002：元の修正 Goal を継続し、追加 Owner 計測を開始条件にしない。
- D-003：発生源別保護の論理和を維持し、防いだ命中で保護を開始・延長しない。
- 本 Step はこれらの要約を超える再解釈を行っていない。

## Constraints

- 独立 Verify は未完了。文書整合を条件別合格や Goal 完了に置き換えない。
- AC-1〜AC-6、全4環境、必要な命中源・比較・回帰を維持する。
- 期待値、挙動記述、生成観察、実測を区別する。
- 不明な試行数・発生数・時刻・ハート値を補わない。
- 既存仕様の修正範囲を守り、QA は実装変更や新規仕様決定を行わない。
- 次の QA に実装者の理由・自己評価を検証根拠として渡さない。

## Open questions

1. Studio は runtime 管理側の窓口・取得手段を確保し、必要な条件別記録の有無と提供範囲を確認できるか。
2. 取得可能なモデル・記録は、全4環境の入力受理・命中・状態遷移をどこまで表現しているか。
3. 既存クールダウン起点の原資料はどこにあるか。回復できない場合、game-designer へ判断を返せるか。

## Expected output

Studio は取得経路と必要資料の担当を具体化し、実際に取得した資料を次の packet に含める。仕様判断が必要なら該当する問いを game-designer に返す。

独立 QA は補完された資料から各セルの証拠を採否判断し、全条件を評価する。本 Step では確認された仕様不一致がないため修正差し戻しの `fail` は出さず、証拠不足と一部期待値未定義による `question` として返す。

## Load

- Project: project.md#constraints
- Project: design/combat.md
- Build: sim/build-0.4.md
- Comparison build: sim/build-0.3.md
- Acceptance criteria: goals/G-001-dash-damage/11-qa-to-studio.md#修正の受け入れ条件
- Exercise procedure: goals/G-001-dash-damage/11-qa-to-studio.md#後続で実施する再現・比較手順
- Previous handoff: goals/G-001-dash-damage/20-studio-to-qa.md
- Decisions: 本文の既存要約のみ。追加原文なし。
- Studio の Role・Skills と次工程の Load は Studio がルーティング時に確定する。
>>>END
