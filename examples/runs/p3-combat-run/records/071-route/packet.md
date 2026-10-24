# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/57-playtester-to-studio.md
next_seq: 58
context_request: allowed once (@need, up to 8 paths)
current_build: sim/build-0.8.md (newest simulated build; older ones are history)

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/57-playtester-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 58
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
decisions/D-002-combat-variety-direction.md
decisions/D-003-input-during-hit-stun.md
decisions/D-004-phase-2-technical-approach.md
decisions/D-005-phase-2-flinch-contact-and-dash-window.md
decisions/D-006-lunge-cue-realignment-and-flinch-immune-hit-feedback.md
decisions/D-007-verify-against-build-0-5.md
decisions/D-008-phase-1-spawn-and-wave-rules.md
decisions/D-009-judging-basis-criteria-1-and-2.md
design/combat.md
design/g001-combat-escalation.md
design/g001-telegraph-visuals.md
goals/G-001-combat-monotony/01-studio-to-playtester.md
goals/G-001-combat-monotony/02-playtester-to-game-designer.md
goals/G-001-combat-monotony/03-studio-to-qa.md
goals/G-001-combat-monotony/04-game-designer-to-game-director.md
goals/G-001-combat-monotony/05-qa-to-studio.md
goals/G-001-combat-monotony/06-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/07-game-director-to-game-designer.md
goals/G-001-combat-monotony/08-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/09-studio-to-qa.md
goals/G-001-combat-monotony/10-qa-to-studio.md
goals/G-001-combat-monotony/11-game-designer-to-studio.md
goals/G-001-combat-monotony/12-studio-to-qa.md
goals/G-001-combat-monotony/13-studio-to-technical-director.md
goals/G-001-combat-monotony/14-studio-to-art-director.md
goals/G-001-combat-monotony/15-qa-to-studio.md
goals/G-001-combat-monotony/16-technical-director-to-studio.md
goals/G-001-combat-monotony/17-art-director-to-studio.md
goals/G-001-combat-monotony/18-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/19-studio-to-game-designer.md
goals/G-001-combat-monotony/20-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/21-qa-to-studio.md
goals/G-001-combat-monotony/22-game-designer-to-studio.md
goals/G-001-combat-monotony/23-studio-to-qa.md
goals/G-001-combat-monotony/24-studio-to-art-director.md
goals/G-001-combat-monotony/25-art-director-to-studio.md
goals/G-001-combat-monotony/26-qa-to-studio.md
goals/G-001-combat-monotony/27-studio-to-owner.md
goals/G-001-combat-monotony/28-studio-to-qa.md
goals/G-001-combat-monotony/29-qa-to-studio.md
goals/G-001-combat-monotony/30-studio-to-qa.md
goals/G-001-combat-monotony/31-qa-to-studio.md
goals/G-001-combat-monotony/32-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/33-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/34-studio-to-game-designer.md
goals/G-001-combat-monotony/35-game-designer-to-studio.md
goals/G-001-combat-monotony/36-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/37-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/38-studio-to-qa.md
goals/G-001-combat-monotony/39-studio-to-art-director.md
goals/G-001-combat-monotony/40-qa-to-studio.md
goals/G-001-combat-monotony/41-art-director-to-studio.md
goals/G-001-combat-monotony/42-studio-to-game-designer.md
goals/G-001-combat-monotony/43-studio-to-art-director.md
goals/G-001-combat-monotony/44-game-designer-to-studio.md
goals/G-001-combat-monotony/45-art-director-to-studio.md
goals/G-001-combat-monotony/46-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/47-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/48-studio-to-qa.md
goals/G-001-combat-monotony/49-studio-to-art-director.md
goals/G-001-combat-monotony/50-qa-to-studio.md
goals/G-001-combat-monotony/51-art-director-to-studio.md
goals/G-001-combat-monotony/52-studio-to-game-designer.md
goals/G-001-combat-monotony/53-game-designer-to-studio.md
goals/G-001-combat-monotony/54-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/55-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/56-studio-to-playtester.md
goals/G-001-combat-monotony/57-playtester-to-studio.md
goals/G-001-combat-monotony/goal.md
project.md
sim/build-0.3.md
sim/build-0.4.md
sim/build-0.5.md
sim/build-0.6.md
sim/build-0.7.md
sim/build-0.8.md
sim/repo-notes.md
>>>END

<<<FILE @decision-titles
decisions/D-001-one-button-combat.md — D-001: Combat uses one attack button plus dash
decisions/D-002-combat-variety-direction.md — D-002: Fix combat monotony with encounter escalation first, then enemy behaviors that demand movement and the dash
decisions/D-003-input-during-hit-stun.md — D-003: Input during hit-stun is ignored, not buffered
decisions/D-004-phase-2-technical-approach.md — D-004: Time-parametrized, sub-stepped lunge hit check; Fan Spitter over the repositioning Spitter; Phase 1 as one serial Build
decisions/D-005-phase-2-flinch-contact-and-dash-window.md — D-005: Phase 2 enemies are flinch-immune during their actions; Lunge Grub damages only through the lunge; dash window is defined relative to contact
decisions/D-006-lunge-cue-realignment-and-flinch-immune-hit-feedback.md — D-006: Lunge committed stage follows the spec through a tunable start; cold-white overlay feedback for hits on flinch-immune enemies
decisions/D-007-verify-against-build-0-5.md — D-007: Verify the hit-stun input change against `sim/build-0.5.md`; `sim/build-0.4.md` is outdated
decisions/D-008-phase-1-spawn-and-wave-rules.md — D-008: Phase 1 spawns are deterministic from ordered candidate lists; waves trigger on an unresolved-enemy count; Spitters keep the 5-tile rule through a far-end alternative
decisions/D-009-judging-basis-criteria-1-and-2.md — D-009: Phase 1 criteria 1 and 2 are judged at the playtest from counts; spawn-sampling, first-shot, fallback and room-size questions settled without a rule change to the build
>>>END

<<<FILE goals/G-001-combat-monotony/goal.md
---
kind: goal
id: G-001
project: lantern-depths
status: active
created: 2026-10-11
---
# G-001: Improve monotonous combat

## Owner request

> 戦闘が単調なので改善したい

## Interpretation

Success condition (qualitative): a player from the project's player profile experiences combat in the current build as varied and engaging rather than repetitive. Playing a run involves meaningful moment-to-moment variation in how the player positions, times and responds to enemies. Numeric thresholds belong to Design; the final verdict belongs to Review.

Constraints that shape any solution:
- Pillar 1 and D-001: combat stays one-button (attack + dash). No new input buttons without Owner approval. Variety must come from positioning, timing and enemy behavior.
- Readable threats (pillar 3) and 30/60 FPS correctness must be preserved.
- Small team: prefer reusing existing systems.

Out of scope: new input buttons or a larger player kit, changes to run length, new biomes or rooms unrelated to combat variety, and non-combat systems.

Not an immediate escalation: the Goal does not conflict with the vision or D-001. It must be solved inside them. If Diagnose finds that the only viable fixes need a new button or change a pillar, that triggers an Owner escalation then.

## Unknowns

Entry questions from `development-loop.md`:
- Observe: experience problem, so `playtester` observed (done). A possible dash-damage defect was confirmed by QA against `design/combat.md` (handoff 05).
- Diagnose: done (handoff 04): three options.
- Decide: done. D-002 chose B (encounter escalation) first, then A (enemy behaviors); C in reserve.
- Design: done for Phase 1 and Phase 2 (handoffs 11, 22, 25, 35, 44, 53; D-005, D-006, D-008, D-009). Settled since: Phase 1 spec gaps (D-008), the judging basis for criteria 1 and 2 (D-009), and spec 3.3 wording plus the neutral playtest record sheet (handoff 53, no rule change). One Phase 2 data value (`committed_start`, provisional 0.45 s) is still to be confirmed after Build's report.
- Plan: done (handoff 16, D-004). Phase 1 needs no separate Plan.
- Build: done for the dash-damage fix (08), hit-stun input (20), Phase 1 (37), the narrow Phase 1 follow-up (47) and the wording-only update (55; `sim/build-0.8.md` is the newest build). Phase 2 is tentative.
- Verify: Phase 1 verified with criteria 1 and 2 open (QA pass in handoff 50, Art Director pass in handoff 51). Always after Build.
- Play: the Goal is about feel, so a Playtester evaluates after each phase (fresh Handoff without implementation history). Phase 1 playtest is open (handoff 56).
- Review: experience Goal, so the Game Director judges the outcome. Planned.

Skipped: none.

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | playtester | playtest-session | done | [01](01-studio-to-playtester.md) → [02](02-playtester-to-game-designer.md) |
| 2a | Diagnose | game-designer | diagnose-experience | done | [02](02-playtester-to-game-designer.md) → [04](04-game-designer-to-game-director.md) |
| 2b | Observe (possible defect: damage during dash) | qa | reproduce-defect | done | [03](03-studio-to-qa.md) → [05](05-qa-to-studio.md) |
| 3a | Decide | game-director | make-decision | done (D-002) | [04](04-game-designer-to-game-director.md) → [07](07-game-director-to-game-designer.md) |
| 3b | Build (fix dash-damage defect) | gameplay-engineer | implement-change | done | [06](06-studio-to-gameplay-engineer.md) → [08](08-gameplay-engineer-to-studio.md) |
| 3c | Build (hit-stun input observable, consistent with D-003) | gameplay-engineer | implement-change | done | [18](18-studio-to-gameplay-engineer.md) → [20](20-gameplay-engineer-to-studio.md) |
| 4a–4a″ | Verify (dash-damage fix), attempts 1 to 4 | qa | verify-change | done, no verdict (`question` each time: build file missing, hit-stun not observable, outdated build description, criteria text missing from Load); superseded by 4a‴ | [09](09-studio-to-qa.md), [12](12-studio-to-qa.md), [23](23-studio-to-qa.md), [28](28-studio-to-qa.md); reports [10](10-qa-to-studio.md), [15](15-qa-to-studio.md), [21](21-qa-to-studio.md), [26](26-qa-to-studio.md), [29](29-qa-to-studio.md) |
| 4c | Verify decision (which build description is current) | owner | — | done (D-007: `sim/build-0.5.md`) | [27](27-studio-to-owner.md) |
| 4a‴ | Verify (attempt 5, against `sim/build-0.5.md`) | qa | verify-change | done: **pass** ([31](31-qa-to-studio.md)); criteria 1–6 at 30 and 60 FPS, no regression against 0.3 | [30](30-studio-to-qa.md) |
| 4b | Design (Phase 1 in full; Phase 2 as proposed behaviors) | game-designer | write-design-spec | done | [07](07-game-director-to-game-designer.md) → [11](11-game-designer-to-studio.md) |
| 5a | Plan (Phase 2 feasibility and cost) | technical-director | technical-plan | done (D-004) | [13](13-studio-to-technical-director.md) → [16](16-technical-director-to-studio.md) |
| 5b | Design (spawn marker and Phase 2 telegraph visuals) | art-director | write-design-spec | done | [14](14-studio-to-art-director.md) → [17](17-art-director-to-studio.md) |
| 5c | Design (adjust Phase 2 spec) | game-designer | write-design-spec | done (D-005) | [19](19-studio-to-game-designer.md) → [22](22-game-designer-to-studio.md) |
| 5d | Design (realign Lunge Grub visual; hit feedback for flinch-immune enemies) | art-director | write-design-spec | done (D-006) | [24](24-studio-to-art-director.md) → [25](25-art-director-to-studio.md) |
| 6, 6b, 6c | Build Phase 1 (attempt 1 `question`; Design resolved gaps, D-008; attempt 2 done) | gameplay-engineer / game-designer | implement-change / write-design-spec | done | [32](32-studio-to-gameplay-engineer.md) → [33](33-gameplay-engineer-to-studio.md); [34](34-studio-to-game-designer.md) → [35](35-game-designer-to-studio.md); [36](36-studio-to-gameplay-engineer.md) → [37](37-gameplay-engineer-to-studio.md) |
| 7a | Verify (Phase 1, `sim/build-0.6.md`) | qa | verify-change | done, `question` ([40](40-qa-to-studio.md)): criteria 3, 4, 5, 10 pass; criteria 1 and 2 need counted runs | [38](38-studio-to-qa.md) |
| 7b | Verify (visual review of the spawn marker ring) | art-director | visual-review | done: pass on the described look ([41](41-art-director-to-studio.md)); dot colour row later corrected | [39](39-studio-to-art-director.md) |
| 7c | Design (judging basis for criteria 1 and 2; items D1–D6) | game-designer | write-design-spec | done (D-009): criteria 1 and 2 judged at the playtest from counts | [42](42-studio-to-game-designer.md) → [44](44-game-designer-to-studio.md) |
| 7d | Verify (visual follow-up: dot colour, capture checks) | art-director | visual-review | done: dot `#FFC14D`, statements S0–S3 | [43](43-studio-to-art-director.md) → [45](45-art-director-to-studio.md) |
| 7f | Build (narrow: ring dot, S0–S3, spec points (a)–(d)) | gameplay-engineer | implement-change | done | [46](46-studio-to-gameplay-engineer.md) → [47](47-gameplay-engineer-to-studio.md) |
| 7e | Verify (narrow re-verify, `sim/build-0.7.md`) | qa | verify-change | done: **pass** ([50](50-qa-to-studio.md)); criteria 1 and 2 recorded "deferred to playtest" | [48](48-studio-to-qa.md) |
| 7g | Verify (re-review of ring dot and S0–S3) | art-director | visual-review | done: **pass** ([51](51-art-director-to-studio.md)) | [49](49-studio-to-art-director.md) |
| 7h | Design (spec 3.3 wording items; neutral playtest record sheet) | game-designer | write-design-spec | done ([53](53-game-designer-to-studio.md)): wording only, no new Decision | [52](52-studio-to-game-designer.md) |
| 7i | Build (wording only: seven build description items) | gameplay-engineer | implement-change | done ([55](55-gameplay-engineer-to-studio.md)): all seven items and the "linear in game time" option stated; "solid" not changed (no wording given); no behavior changed. `sim/build-0.8.md` is the newest build. | [54](54-studio-to-gameplay-engineer.md) |
| 8 | Play (Phase 1) | playtester | playtest-session | open | [56-studio-to-playtester.md](56-studio-to-playtester.md) |
| 9 | Build (Phase 2: behavior variants) | gameplay-engineer | implement-change | tentative (after the Phase 1 playtest, only if combat is still monotonous, per D-002 "B then A"; its Handoff must carry the "confirm after the report" values from spec section 7 (`committed_start`, default 0.45 s, clamped to [0, 0.60 s], clamp reported), the 5d Build-report items, an update of `design/combat.md` for Flinch and the Phase 2 enemies, and the Designer's "first overlap uses up the lunge's single hit" note from handoff 22) | — |
| 9b | Design (confirm Phase 2 dash-window figures and `committed_start`; 2 HP damage-marker question) | game-designer | write-design-spec | tentative (after 9's report) | — |
| 10a | Verify (Phase 2; criteria 2, 4, 5, 7–9) | qa | verify-change | tentative (after 9 and 9b) | — |
| 10b | Verify (Phase 2 visuals; criteria A1–A13) | art-director | visual-review | tentative (after 9; parallel with 10a) | — |
| 11 | Play (Phase 2) | playtester | playtest-session | tentative (readability of the 0.15 s committed stage at 30 FPS, learnability of the late-dash cue, whether hits on flinch-immune enemies are noticed) | — |
| 12 | Review | game-director | review-outcome | planned (Phase 1 recorded as "verified, with criteria 1 and 2 open until counts exist"; never as met without counts) | — |

Status: planned | tentative | open | done | skipped.

## Route changes

Earlier Route changes (steps 1 to 7h) are summarized here; the Handoffs carry the details.

- Step 1 found a possible defect, so QA ran in parallel (2b). Diagnose gave three options and D-002 chose B then A.
- Verify of the dash-damage fix took five attempts. The hand-backs came from build-description gaps and Load gaps, not from a failed criterion. The Owner settled which description is current (D-007), and the fix passed (31).
- Phase 1 Build handed back once on spec contradictions. Design resolved them (D-008), and Build then succeeded (37).
- Phase 1 Verify raised that criteria 1 and 2 need counted runs. Design moved them to the playtest (D-009). The narrow Build (47) fixed the ring dot colour, and both re-verifications passed (50, 51).
- Design closed spec 3.3 wording items as wording only and wrote the neutral record sheet (53). Tentative 7i was confirmed and became a wording-only Build.
- After step 7i (handoff 55, gameplay-engineer `done`):
  - **Fits the plan.** Wording only, and no escalation trigger fires. The engineer stated the seven items. `sim/build-0.8.md` (the newest build, the file the update was applied to) shows all seven and "linear in game time". Its heading says 0.8, so the label matches the file. The engineer's own text predicted "0.7", which is a slip and changes nothing. The Designer classified the change as wording only, so QA does not re-verify.
  - **Reported, not routed now.** Two sentences are unqualified but true only for rooms 3 to 5 ("For Spitters the second point is the other end of the same wall"; "A Spitter near a held corner appears at the far end of its wall"). Handoff 53 told Build to keep the first one, and the Designer holds the rule. Both stay as playtest and Review notes. `sim/repo-notes.md` still says the latest description is headed 0.3.3. It is a note, not a build description, and does not reach the Playtester.
  - **Step 8 is opened as handoff 56**, composed by the Studio for `playtester` from permitted information only. The Load list names the Playtester Role, the skill, `project.md#player-profile` and `sim/build-0.8.md`. There is no previous handoff, and nothing from handoffs 44 to 55 (Sender assessments, QA and Art Director findings, wording lists) goes to the Playtester. The Designer's record sheet (handoff 53) is pasted unchanged. The play focus is "combat, where enemies come from and what you do", and it states no expected result. The result is addressed to `studio` so Route can check counts before Review.
  - **Counts rule.** Review must not take criteria 1 and 2 as met without counted attempts. If the playtest returns without counts (it is a description in this dry run), the Studio escalates to the Owner: accept "not judged" for the dry run, or stop. Not triggered now, because the playtest has not run.

## Next action

`playtester` runs step 8 from [56-studio-to-playtester.md](56-studio-to-playtester.md): play rooms 1 to 5 of `sim/build-0.8.md`, fill in the record sheet, and address the result to `studio`.

After it (Route): check whether counts exist for the Part A attempts and the Part C measurements. If they do, route to `game-director` for Review (step 12), and open Phase 2 (steps 9 onward) only if combat is still monotonous (D-002). A defect found by the Playtester goes to `qa`. A design or experience issue goes to `game-designer`. A "white" or "pale" ring centre in the notes goes to the Art Director. If no counted attempts exist, escalate to the Owner.

## Outcome

(To be filled at close, in Japanese.)
>>>END

<<<FILE goals/G-001-combat-monotony/57-playtester-to-studio.md
---
kind: handoff
goal: G-001
seq: 57
from: playtester
to: studio
stage: Play
outcome: done
---
# 57: playtester → studio — Observation report for build 0.8, rooms 1 to 5: record sheet mostly not available

## Task

Report what I observed playing build 0.8, rooms 1 to 5, using the record sheet from handoff 56.

## Context

This is a dry run. The only thing I could "run" was the text description `sim/build-0.8.md`. I did not play live, I had no clock, no log, no controller input and no recorded session. I could not count hits, deaths, clear times or log lines. Where the sheet asks for something I did not count or measure, I write "not available". Anything marked **(read)** comes from the build description. It is not something I saw or counted in play.

Player profile used: an action player who wants short, intense runs, is comfortable with dodging and spacing, and plays on a gamepad.

## Findings

### Method actually used

- I read the build description once and walked each room through in my head and in notes.
- I did not play live, use input automation, or watch a recorded session.
- I have no numbers from play. Nothing below is a measurement.

### PLAYTEST RECORD SHEET

**Part A. Held positions, rooms 4 and 5**

I did not do any of the 50 attempts (room 4 and room 5, NW/NE/SW/SE/Centre, attempts 1 to 5). All 50 are missing.

For every one of them:
- Hits taken: not available
- Died: not available
- Held the position the whole attempt: not available

The description says whether you take hits depends on room size and speeds, and it does not state those. I therefore did not guess hit counts.

What the description says about holding a corner **(read, not observed)**:
- A player in a corner sees arrivals on the other edges, 5 or more tiles away, unless the fallback applies.
- A Spitter whose home corner is covered appears at the far end of its wall.
- Grubs from opposite edges can reach you at about the same time.

**Part B. Free play, rooms 1 to 5**

I did not play the rooms. For every room, the following are therefore not available:
- F1 (dashes in combat and why): 0 dashes made by me, because I did not play. I have no combat reason to report.
- F4 (where I was, whether and where I moved before the enemy appeared, step-by-step actions): not available.
- F5 (leaving my spot, how often, why): not available.
- Hits taken and died: not available.

F2 and F3 below describe what the description says the player would see **(read)**.

| Room | Arrivals and edges (read) | F2: what draws attention (read) | F3: simultaneous arrivals on the floor (read) |
|---|---|---|---|
| 1 | Grub at the west edge at the start. A second Grub 1.0 s later, also west, further along the wall. A Spitter at the east edge, mid-height, at the start. No wave 2. | An orange-red ring with an amber dot on the floor, 0.8 s before the enemy appears. | At the start, 2 rings: a west Grub and the east Spitter. The second Grub's ring follows 1.0 s later. |
| 2 | Same as room 1. Wave 2 is 1 Grub at the east edge. | Same ring. | Same as room 1. Wave 2 may begin while wave 1 enemies are alive. |
| 3 | Wave 1 has 2 west Grubs and a Spitter at the north edge near the NE corner. Wave 2 has 2 Grubs on the east edge, one nearer the north and one nearer the south, ringing together. | Same ring. | Wave 2 shows 2 rings at the same moment on the east edge. |
| 4 | Wave 1 has 2 west Grubs ringing together, 1 east Grub, and a Spitter at the north edge near the NW corner. Wave 2 has a north Grub and a south Spitter near the SE corner. | Same ring. | Wave 1 has at least 2 rings together on the west edge. I did not see the exact count on the floor. |
| 5 | Wave 1 has 2 west Grubs, 1 east Grub, a south Spitter near the SW corner and a north Spitter near the NE corner. Wave 2 has a north Grub and a south Grub ringing together. | Same ring. | Wave 1 has rings on the west, east, south and north edges. Wave 2 has 2 rings together, north and south. |

I never actually noticed any arrival. The "when I first noticed it" part of F2 is not available. The description says the ring is visible for its whole 0.8 s from 8 or more tiles away, including outside the lantern's light.

**Part C. Records and measurements**

- `SPAWN_FALLBACK` lines per room (rooms 1 to 5): not available. I have no log.
- Time between the two enemies of each "at the same time" pair:
  - Measured by me: not available.
  - From the description **(read, scheduled time, not measured)**: 0 s between ring starts and appearances for room 3 wave 2, room 4 wave 1 west edge, room 5 wave 1 west edge, and room 5 wave 2. The description allows up to about 0.034 s of frame difference at 30 FPS.
  - The +1.0 s Grub in rooms 1 to 3 is scheduled 1.0 s after the first Grub (read).
- Real elapsed time for a full run and clear time per room: not available. I had no clock and did not play.
- Values:
  - Grub speed: not available
  - Player speed: not available
  - Projectile speed: not available
  - Projectile range: not available
  - Player hearts: not available
  - Room size (width by height): not available
  - Grub, player and Spitter hitbox sizes: not available
  - The description states that these are not given, and I could not measure them.
  - Read from the description, not measured: a Grub takes two swipes, the dash lasts 0.25 s, the dash cooldown is 0.6 s, and the post-hit protection is 0.8 s with a 0.3 s stun.
- Surprises or damage from nowhere: none. I took no damage because I did not play.

### Other observations (from reading, not from play)

- A room no longer starts with enemies on the floor. A ring warns of each arrival 0.8 s ahead, so arrivals should be readable and not feel unfair.
- A Spitter does not fire for 1.0 s after appearing, which gives time to react.
- Wave 2 can start early after a kill, before the room looks nearly empty. A player could find that sudden. I cannot say how it felt.
- I cannot say whether standing still is still a good answer in rooms 4 and 5. That needs live play and the room size.
- The ring is described as a placeholder. I could not judge how it looks.

## Decisions already made

None that concern me.

## Constraints

- I worked only from the build description and the player profile. I opened no design documents, earlier handoffs, decisions or other builds.
- I reported no cause or implementation guesses.

## Open questions

- The sheet needs real play (live, automated or human) to produce Part A, Part B and the measured parts of Part C. Please route it to an executor that can run the build, with a clock and the debug log.

## Expected output

This report goes to `studio`. Part A, Part B and most of Part C are not available from this dry run.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile; sim/build-0.8.md
- Decisions: none
- Previous handoff: none
>>>END
