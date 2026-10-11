# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/47-gameplay-engineer-to-studio.md
next_seq: 48
context_request: allowed once (@need, up to 8 paths)
current_build: sim/build-0.7.md (newest simulated build; older ones are history)

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/47-gameplay-engineer-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 48
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
goals/G-001-combat-monotony/goal.md
project.md
sim/build-0.3.md
sim/build-0.4.md
sim/build-0.5.md
sim/build-0.6.md
sim/build-0.7.md
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
- Observe: has the problem been observed first-hand? No. It is an experience problem (the game may work as specified but feel wrong), so `playtester` observes. The Owner's wording is not given to the Playtester, to avoid confirming a hypothesis.
- Diagnose: is the cause understood? No. What makes the combat feel monotonous is unknown (enemy behavior, kit depth, room design, pacing). Stage created.
- Decide: is there a real choice of direction, priority or scope? Yes. The diagnosis (handoff 04) offered three options (A: enemy behaviors, B: encounter design and escalation, C: rule rewards). Answered by D-002 (B first, then A; C in reserve).
- Design: is the intended behavior specified well enough to build? Not for the chosen direction. Done for Phase 1 and for Phase 2 (handoff 11, `design/g001-combat-escalation.md`, adjusted in handoff 22 and D-005). The Phase 2 telegraph visuals were realigned to the corrected dash window in step 5d (handoff 25, D-006, `design/g001-telegraph-visuals.md`). One data value (`committed_start`, provisional 0.45 s) is still to be confirmed by the Game Designer after Build's report. Reopened for Phase 1: the Build found contradictions and gaps in spec sections 3.2–3.4 (handoff 33); step 6b resolved them (handoff 35, D-008). Reopened again after Phase 1 Verify: criteria 1 and 2 (Phase 1 part) cannot be judged from a build description, and QA raised design items D1–D6 (handoff 40); step 7c settled them (handoff 44, D-009: criteria 1 and 2 are judged at the playtest from counts; D2–D6 answered; no rule change).
- Plan: needed for Phase 2 (feasibility and cost). Answered in handoff 16 and D-004: feasible and cheap. Phase 1 needs no separate Plan (handoff 16).
- Build: the dash-damage defect fix (done, handoff 08), the hit-stun input made observable (done, handoff 20), then Phase 1 (done, handoff 37), a narrow Phase 1 follow-up (ring dot colour, build statements, spec clarification; handoff 46), and Phase 2 of the chosen direction.
- Verify: always after Build.
- Play: the Goal is about how the game feels, so a Playtester re-evaluates after each phase (fresh Handoff composed by the Studio without implementation history). It should record real-time run length and per-room clear time.
- Review: experience Goal, so the Game Director judges the outcome. Planned.
- Observe (defect): the Playtester saw a possible dash-damage defect. QA confirmed it against `design/combat.md` (handoff 05). Intended behavior is already specified, so the fix needed no Design or Plan.

Skipped: none.

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | playtester | playtest-session | done | [01-studio-to-playtester.md](01-studio-to-playtester.md) → report in [02-playtester-to-game-designer.md](02-playtester-to-game-designer.md) |
| 2a | Diagnose | game-designer | diagnose-experience | done | [02-playtester-to-game-designer.md](02-playtester-to-game-designer.md) → diagnosis in [04-game-designer-to-game-director.md](04-game-designer-to-game-director.md) |
| 2b | Observe (possible defect: damage during dash) | qa | reproduce-defect | done | [03-studio-to-qa.md](03-studio-to-qa.md) → report in [05-qa-to-studio.md](05-qa-to-studio.md) |
| 3a | Decide | game-director | make-decision | done | [04-game-designer-to-game-director.md](04-game-designer-to-game-director.md) → D-002, [07-game-director-to-game-designer.md](07-game-director-to-game-designer.md) |
| 3b | Build (fix dash-damage defect) | gameplay-engineer | implement-change | done | [06-studio-to-gameplay-engineer.md](06-studio-to-gameplay-engineer.md) → [08-gameplay-engineer-to-studio.md](08-gameplay-engineer-to-studio.md) |
| 3c | Build (make hit-stun dash/attack input observable and consistent with D-003; report code values) | gameplay-engineer | implement-change | done | [18-studio-to-gameplay-engineer.md](18-studio-to-gameplay-engineer.md) → [20-gameplay-engineer-to-studio.md](20-gameplay-engineer-to-studio.md) |
| 4a | Verify (dash-damage fix) | qa | verify-change | done, no verdict: attempt 1 `question` (build not in packet, [10](10-qa-to-studio.md)); attempt 2 `question` (hit-stun press not observable, [15](15-qa-to-studio.md)); [21](21-qa-to-studio.md) repeats attempt 2 against the build description from before 3c. Superseded by 4a′. | [12-studio-to-qa.md](12-studio-to-qa.md) (attempt 1: [09-studio-to-qa.md](09-studio-to-qa.md)) |
| 4a′ | Verify (attempt 3: dash-damage fix incl. hit-stun input) | qa | verify-change | done, no verdict: `question` ([26](26-qa-to-studio.md)): `sim/build-0.4.md` still says hit-stun presses behave "as in 0.3", so criteria 2 and 5 are not judgeable; criteria 1, 3, 4, 6 consistent with pass. Blocked on Owner ([27](27-studio-to-owner.md)), resolved by D-007. | [23-studio-to-qa.md](23-studio-to-qa.md) |
| 4b | Design (Phase 1 in full; Phase 2 as proposed behaviors) | game-designer | write-design-spec | done | [07-game-director-to-game-designer.md](07-game-director-to-game-designer.md) → [11-game-designer-to-studio.md](11-game-designer-to-studio.md) |
| 5a | Plan (Phase 2 feasibility and cost) | technical-director | technical-plan | done | [13-studio-to-technical-director.md](13-studio-to-technical-director.md) → [16-technical-director-to-studio.md](16-technical-director-to-studio.md) (D-004) |
| 5b | Design (spawn marker and Phase 2 telegraph visuals) | art-director | write-design-spec | done | [14-studio-to-art-director.md](14-studio-to-art-director.md) → [17-art-director-to-studio.md](17-art-director-to-studio.md) (`design/g001-telegraph-visuals.md`) |
| 5c | Design (adjust Phase 2 spec from 5a and 5b answers) | game-designer | write-design-spec | done | [19-studio-to-game-designer.md](19-studio-to-game-designer.md) → [22-game-designer-to-studio.md](22-game-designer-to-studio.md) (D-005, `design/g001-combat-escalation.md`) |
| 5d | Design (realign Lunge Grub committed-stage visual and A5 to the corrected dash window; hit feedback for flinch-immune enemies) | art-director | write-design-spec | done | [24-studio-to-art-director.md](24-studio-to-art-director.md) → [25-art-director-to-studio.md](25-art-director-to-studio.md) (D-006, `design/g001-telegraph-visuals.md`, criteria A1–A13) |
| 4c | Verify decision (how to resolve the missing hit-stun statements in the build description) | owner | — | done: Owner answered that the updated build description is `sim/build-0.5.md` (0.4 is outdated); recorded as D-007 | [27-studio-to-owner.md](27-studio-to-owner.md) |
| 4a″ | Verify (attempt 4: dash-damage fix incl. hit-stun input, against `sim/build-0.5.md`) | qa | verify-change | done, no verdict: `question` ([29](29-qa-to-studio.md)). The six hit-stun statements and the invulnerability matrix all pass in `sim/build-0.5.md`, but the text of criteria 1–6 (in handoff 05) was not in QA's Load, so no per-criterion verdict. Cause: Load gap in handoff 28, not a build gap. Superseded by 4a‴. | [28-studio-to-qa.md](28-studio-to-qa.md) |
| 4a‴ | Verify (attempt 5: same scope as 4a″, with the criteria text in Load) | qa | verify-change | done: **pass** ([31](31-qa-to-studio.md)); criteria 1–6 pass at 30 and 60 FPS against `sim/build-0.5.md`, no regression against 0.3. Evidence is a build description, not a counted run. | [30-studio-to-qa.md](30-studio-to-qa.md) |
| 6 | Build (Phase 1: encounter escalation), attempt 1 | gameplay-engineer | implement-change | done, no change applied: `question` ([33](33-gameplay-engineer-to-studio.md)). Spec contradictions and gaps in sections 3.2–3.4 (6 questions: wave trigger, spawn point choice, Spitter corners, Spitter versus 5-tile rule, meaning of "simul.", marker start times) and the existing values (Grub, player and projectile speed, hearts, room size) are not in the packet. `sim/build-0.5.md` stays current. Resumed as 6c. | [32-studio-to-gameplay-engineer.md](32-studio-to-gameplay-engineer.md) |
| 6b | Design (resolve the Phase 1 spec gaps and contradictions from handoff 33; state the existing values or say Phase 1 proceeds without them) | game-designer | write-design-spec | done: all six questions answered in the amended `design/g001-combat-escalation.md` (D-008, [35](35-game-designer-to-studio.md)); the existing values are not available to the Designer, so Phase 1 proceeds without them (data uses tiles, seconds and room-relative points; Build reports what it can read; QA's first Phase 1 handoff and the playtest record them) | [34-studio-to-game-designer.md](34-studio-to-game-designer.md) → [35-game-designer-to-studio.md](35-game-designer-to-studio.md) |
| 6c | Build (Phase 1: encounter escalation), attempt 2 | gameplay-engineer | implement-change | done ([37](37-gameplay-engineer-to-studio.md)): whole change stated (room data, wave scheduler, point choice, enemy creation timing, minimal marker ring, Spitter first shot); no existing spawn effect was reused (none known), so the minimal ring was built and flagged for the Art Director; none of the existing values (speeds, hearts, room size, hitboxes) could be read; no test run (dry run, nothing run). `sim/build-0.6.md` is the newest build. | [36-studio-to-gameplay-engineer.md](36-studio-to-gameplay-engineer.md) |
| 7a | Verify (Phase 1; criteria 1–5 and 10 of the amended spec, marker timing A1–A3, regression against 0.5 behavior) | qa | verify-change | done, `question` ([40](40-qa-to-studio.md)) against `sim/build-0.6.md`: criteria 3, 4, 5, 10 pass at 30 and 60 FPS (description-based); regression against 0.5: none; criteria 1 and 2 (Phase 1 part) not judgeable, because they need counted runs and the build description has none (exact missing input named in 40). QA also raised design items D1–D6 and reported: existing values "not shown", `SPAWN_FALLBACK` count unavailable, heading "0.3.3" vs file 0.6. No failing criterion. Continued as 7c, then 7e. | [38-studio-to-qa.md](38-studio-to-qa.md) |
| 7b | Verify (visual review of the Phase 1 spawn marker ring) | art-director | visual-review | done: **pass** ([41](41-art-director-to-studio.md)), on the described look; A1 and A3 pass, A2 timing left to QA, no look change decided; three capture checks left open (faintest moment, burst colour, two rings and wall draw order). Qualified by 7d: the dot colour row in 41 was wrong; the dot is open until the re-review in 7g. | [39-studio-to-art-director.md](39-studio-to-art-director.md) |
| 7c | Design (judging basis for criteria 1 and 2, Phase 1 part, in a dry run; QA design items D1–D6) | game-designer | write-design-spec | done ([44](44-game-designer-to-studio.md), D-009): criteria 1 and 2 (P1) are judged at the playtest from counts, and QA records "deferred to playtest"; thresholds unchanged; D2–D6 answered (sampling margin rule, first-shot basis, mixed-case point order, room 2 wave 2 accepted with a pre-agreed data change on a trigger, criterion 2 is a playtest signal only); no rule change; one clarification requested from Build; one narrow QA re-verify | [42-studio-to-game-designer.md](42-studio-to-game-designer.md) |
| 7d | Verify (visual follow-up: dot colour "near-white" vs `#FFC14D`; how the three capture checks are covered without captures) | art-director | visual-review | done ([45](45-art-director-to-studio.md)): "near-white" not accepted; one narrow look change (dot `#FFC14D` in 0.6–0.8 s); capture checks replaced by build statements S1–S3 and neutral playtest items P1 and P2; the dot is open until the re-review | [43-studio-to-art-director.md](43-studio-to-art-director.md) |
| 7f | Build (narrow: ring dot `#FFC14D`, statements S0–S3, and clarification of spec points (a)–(d)) | gameplay-engineer | implement-change | open | [46-studio-to-gameplay-engineer.md](46-studio-to-gameplay-engineer.md) |
| 7e | Verify (narrow re-verify: criterion 10 (c), (d), new (g); criterion 4 first-shot basis; criterion 5 with the 1-tile margin rule; criteria 1 and 2 recorded "deferred to playtest"; criterion 3 and the regression check against 0.5 unchanged) | qa | verify-change | planned (confirmed by 7c; after 7f; parallel with 7g; fresh Handoff composed by the Studio without the engineer's Sender assessment) | — |
| 7g | Verify (re-review of the ring dot colour and statements S0–S3 as stated after 7f) | art-director | visual-review | planned (after 7f; parallel with 7e; pass condition in handoff 45) | — |
| 8 | Play (Phase 1) | playtester | playtest-session | planned (after 7e and 7g; fresh Handoff without implementation history; record real-time run length, per-room clear time, arrival gaps of "simul." Grubs, the existing values of spec 3.8, `SPAWN_FALLBACK` counts per room, and the records of spec 6a; for criterion 1 the tester is told which position to hold in rooms 4 and 5 (5 positions, 5 attempts each: hits taken, death) and not the expected result, plus free-play notes on whether and why they left a position; for criterion 2 unprompted per-room notes on dashing in combat and why; neutral items P1 "For each arrival, say when you first noticed it and what drew your attention to it" and P2 "When more than one arrival was on the floor at the same time, say how many you saw and where each one was"; the A3 signal from handoff 41 (do testers dodge a ring as if it were an attack)) | — |
| 9 | Build (Phase 2: behavior variants) | gameplay-engineer | implement-change | tentative (after steps 7–8, if the Phase 1 playtest leaves combat still monotonous, per D-002 "B then A"; spec feasible per 5a, readable per 5b, visuals realigned per 5d; its Handoff must carry the "confirm after the report" values from spec section 7 as data values for the Designer to confirm, `committed_start` (default 0.45 s, clamped to [0, 0.60 s], clamp reported), and the 5d Build-report items: existing spawn effect, hit spark and hit sound to reuse, lunge hit width, projectile range, Spitter mouth position; `design/combat.md` must be updated for Flinch and the Phase 2 enemies; attach the Designer's "first overlap uses up the lunge's single hit" note from handoff 22) | — |
| 9b | Design (confirm Phase 2 dash-window figures and `committed_start` after Build's report; decide whether a 2 HP enemy needs a persistent damage marker, proposed after playtest) | game-designer | write-design-spec | tentative (after 9's report; one data value, no art change needed) | — |
| 10a | Verify (Phase 2; criteria 2, 4, 5, 7–9 of the spec) | qa | verify-change | tentative (after 9 and 9b) | — |
| 10b | Verify (Phase 2 visuals, telegraphs and hit feedback; criteria A1–A13) | art-director | visual-review | tentative (after 9; parallel with 10a) | — |
| 11 | Play (Phase 2) | playtester | playtest-session | tentative (readability of the 0.15 s committed stage at 30 FPS in a dark cave is a playtest item, as are whether the late-dash cue is learnable and whether hits on flinch-immune enemies are noticed) | — |
| 12 | Review | game-director | review-outcome | planned (Phase 1 is to be recorded as "verified, with criteria 1 and 2 open until the playtest counts exist"; never as 1 and 2 met without counts) | — |

Status: planned | tentative | open | done | skipped.

## Route changes

- After step 1 (Observe, playtester): the report matches the plan on the experience side (monotony confirmed: one winning approach in every room, little pressure to move, dash unused in combat), so Diagnose followed as planned. It also contained a possible defect (damage during a dash after being hit). Per the return rule "Play/Observe: defect → Observe (`qa`)", step 2b was added as a parallel step. Handoff 02 was edited in place (still from `playtester`) to add the Owner's report, mark the dash-defect item as routed to `qa`, and fill in Load and Expected output.
- After steps 2a and 2b: 2a produced a diagnosis with three options of different scope and cost (handoff 04), so Decide (`game-director`) followed. 2b confirmed a defect against specified behavior (handoff 05), so Build and Verify for the fix joined the route; no Design is needed because `design/combat.md` already specifies the behavior. QA's non-blocking question (how to treat a dash pressed during hit-stun) was left for `game-designer`.
- After steps 3a and 3b: 3a chose B then A with C in reserve (D-002, handoff 07); no escalation trigger fires, since everything stays within D-001 and the pillars. 3b delivered the invulnerability fix (handoff 08), which must be verified independently. Verify of the fix (4a) and Design of the chosen direction (4b) are independent, so they ran as one parallel group. Handoff 09 for QA was composed by the Studio without the engineer's Sender assessment or root-cause reasoning. Phase 1 Build (6) waits for 4a so it does not stack on an unverified fix. Phase 2 build, verify and play were kept tentative.
- After steps 4a (attempt 1) and 4b: 4a came back as `question` (handoff 10): QA had no build file in its packet, so nothing was verified. This is the first such hand-back for this input and the cause was a missing Load entry, not a Role problem, so 4a was re-opened with handoff 12, which names `sim/build-0.4.md` (latest) and `sim/build-0.3.md` (baseline) explicitly. 4b is done (handoff 11): Phase 1 is build-ready, Phase 2 is proposed. Per the Designer's request, Phase 2 went to `technical-director` (5a, handoff 13) and `art-director` (5b, handoff 14), opened in parallel with 4a. A step 5c was added so the designer adjusts the Phase 2 spec from both answers before any Phase 2 Build.
- After steps 4a (attempt 2), 5a and 5b (handoffs 15, 16, 17):
  - **4a (attempt 2)** came back as `question` again (handoff 15). The build was supplied, and QA found everything consistent with the six criteria except one case: the build files do not say what happens when dash or attack is pressed during hit-stun (D-003 says ignored, not buffered). The loop limit ("same missing input twice") did not apply, because the first hand-back was about a missing file. QA's blocker was a build-observability gap and not a spec gap, so it went to `gameplay-engineer` as a narrow Build (3c, handoff 18).
  - **5a (Plan, handoff 16 and D-004)**: both Phase 2 behaviors are feasible and cheap (Fan Spitter over the repositioning Spitter); Phase 1 needs no separate Plan or isolated workspace and can be one serial Build; no parallelization. The TD found that the existing 0.2 s Flinch conflicts with the Phase 2 spec and that the spec's dash window text does not match the real timing.
  - **5b (Design, handoff 17 and `design/g001-telegraph-visuals.md`)**: telegraph visuals for the spawn marker and both variants; the lunge's committed-stage visual is tied to the spec 4.1 dash window. The marker rule (reuse an existing effect if it passes A1–A5, else build the minimal ring) goes to Build 6.
  - **5c** opened as handoff 19, in parallel with 3c.
- After steps 3c, 5c and the extra QA report (handoffs 20, 21, 22):
  - **3c (handoff 20)** is done. Dash and attack presses during the 0.3 s hit-stun are now discarded and nothing is buffered or fired at its end. The engineer reports that the code notes contain none of the hitbox sizes, speeds, hearts, room size or spawn effect, so those numbers cannot be obtained from the packet. Per the Studio's reading, this is not a blocker for any open step: gameplay numbers are data (D-004), Phase 1 Build states the values it uses, and Phase 2 is tentative. Handoff 20 asked the Studio to confirm that "build-0.4" and the heading "0.3.1" are one build. The Studio treats them as one and asks QA to note the mismatch.
  - **Handoff 21 (QA, `question`)** is treated as a stale repeat of attempt 2: its Previous handoff is 12, and it verified the build description from before 3c ("behaves as it did in 0.3"). Nothing in it is new or contradicts the spec. It is not counted as a second hand-back for the same missing input, since 3c's answer was produced after the gap was reported. The loop limit applies from now on: if QA hands back `question` for the same hit-stun observation after handoff 23, escalate to the Owner. Step 4a is closed as superseded, and 4a′ opened as handoff 23, composed without the engineer's Sender assessment. It states the change and the exercise steps and points QA at the updated `sim/build-0.4.md`.
  - **5c (handoff 22, D-005)** is done. The Designer corrected the dash window (about 0.25 s, ending at contact) with no change to lunge or dash timing, made the Phase 2 enemies flinch-immune during their actions, and made Lunge Grub damage only through the lunge. These are rules inside the Designer's authority and change no pillar, scope or Owner Decision, so no `game-director` step or escalation. The committed-stage visual now contradicts the spec ("solid at 0.35 s = dash now"), which settles tentative step 5d: it is confirmed and opened as handoff 24, in parallel with 4a′ (neither consumes the other's output). It also asks the Art Director for hit feedback on flinch-immune enemies, which the Designer flagged as a visual call.
  - Phase 2 Build (9) stays tentative. Phase 1 (steps 6–8) comes first, and 9 is needed only if combat is still monotonous after that (D-002). The Designer's informational note to the TD (the "first overlap uses up the lunge's single hit" clarification of D-004) is not routed now. It gets attached to the Phase 2 Build Handoff, where the TD or Build can say if it costs more than a flag. `design/combat.md` still lacks the Flinch and the Phase 2 enemies; that update belongs to Phase 2 Build.
  - No escalation trigger fired.
- After step 5d (handoff 25, D-006):
  - **5d is done and fits the plan.** The Art Director realigned the Lunge Grub committed-stage visual to the corrected dash window (stage starts at the tunable data value `committed_start`, default 0.45 s, ends at lunge start 0.60 s; the lunge-start flash is the learnable cue), restated A5, and added hit feedback for flinch-immune enemies (cold-white overlay, criterion A13, D-006). No gameplay timing or rule changed, and no pillar, style or Owner Decision is touched, so there is no escalation and no return to `game-designer` for contradictions: the Art Director found the cue works with the spec's timing.
  - Nothing new opens now. Phase 1 Build (6) still waits for the 4a′ verdict, and Phase 2 stays tentative behind Phase 1 (D-002). Follow-ups were attached to the tentative steps instead: the Build-report items and `committed_start` clamping to step 9; a new tentative step 9b for the Game Designer to confirm `committed_start` and the dash-window figures after Build's report (and to decide the 2 HP damage-marker question after playtest); visual criteria A1–A13 to 10b; and the readability and learnability playtest items to step 11.
  - Handoff 25 was left as written. Its Load list names the game-designer Role, a leftover that doesn't matter because it is addressed to `studio` and no later step starts from it.
- After step 4a′ (handoff 26, QA `question`, attempt 3):
  - **No verdict, and no failure.** QA read `sim/build-0.4.md` as supplied and found the old line "A dash pressed during hit-stun behaves as it did in 0.3." The change from 3c (handoff 20) is not in the build description, so criteria 2 and 5 (hit-stun input part) cannot be judged. Criteria 1, 3, 4 and 6 are consistent with pass. Nothing contradicts the spec or D-003. QA treated handoff 23's statements as the sender's account, not as an observation of the build, as its Role requires.
  - **Escalation trigger fires.** This is the same missing hit-stun observation after handoff 23, the exact case the previous Route set as the limit (and the third QA hand-back on it: 15, 21, 26). The route says to escalate to the Owner rather than send it to a Role again. The blocker is also one that no Role can clear: `sim/` is updated by the runtime's simulator, not by Studio or Roles (`project.md#constraints`), and narrowing the verification scope is a change to the acceptance basis, which the Studio must not decide. The Studio wrote Escalation 27 with three options: A (update the build description, QA re-verifies, recommended), B (use the Build handoff as a substitute record, with reduced independence), C (carry the hit-stun input items forward and proceed to Phase 1).
  - Goal set to `blocked-on-owner`. Phase 1 Build (6) and everything after it depend on the answer, and no step is independent of it (Phase 2 steps are tentative behind Phase 1). QA's optional items (the frame after a dash ends with a source in contact; the heading mismatch 0.3.1 vs 0.4) travel with the next QA Handoff. Rows 4c (open, Owner) and 4a″ (tentative) were added.
- After the Owner's answer to Escalation 27 (Resume, D-007):
  - The Owner chose Option A in substance: the build description with the hit-stun statements already exists as `sim/build-0.5.md`, and `sim/build-0.4.md` is outdated. Recorded as D-007 (`decided_by: owner`). Escalation 27 is `resolved`; the Goal is `active` again. No option described anything different, so no re-run of Intake was needed.
  - Row 4c is done. Row 4a″ is opened as handoff 28, a fresh Handoff composed by the Studio for `qa` without the engineer's Sender assessment (handoff 20 is not in its Load list). It names `sim/build-0.5.md` as the build, `sim/build-0.3.md` as baseline only, and `sim/build-0.4.md` as outdated. Acceptance criteria 1–6 are those of handoff 23, unchanged. It carries the six hit-stun statements and QA's optional items (the frame after a dash ends with a source in contact; heading versus file-name mismatch).
  - Handoff 28 states the loop limit: if `sim/build-0.5.md` still lacks the hit-stun statements, QA says exactly which one, and the Studio escalates to the Owner for that input instead of routing again.
  - Phase 1 Build (6) still waits for the 4a″ verdict. Pass → open step 6. Fail → Build (`gameplay-engineer`) with the failure report (return rules; a second failure on the same criterion goes to `technical-director`). The Owner's answer does not change the rest of the route.
- After step 4a″ (handoff 29, QA `question`, attempt 4):
  - **No verdict, and no failure.** `sim/build-0.5.md` contains every hit-stun statement, so the missing input from attempts 2 to 3 is resolved. QA judged all six hit-stun statements and the dash/hit invulnerability matrix as pass, and found no regression against 0.3. It could not assign verdicts by criterion number because the text of criteria 1–6 was not in its packet: handoff 23 pointed to `05-qa-to-studio.md`, but neither that file nor a restatement of criteria 3 and 4 was in handoff 28's Load list.
  - **This is a different missing input and a Studio Load error, so no escalation.** The loop limit concerns the same missing input twice with nothing new supplied. The earlier hand-backs were about the build description (hit-stun) and, for attempt 1, the build file. This one is the first about the criteria text, and the cause is the Studio's own omission when composing handoff 28. No Role can have produced it. The Studio supplies the file now. The Owner is not involved: the criteria are existing project artifacts, nothing needs reinterpreting, and no Decision or pillar is touched.
  - Row 4a″ is closed as `question`, superseded. Row 4a‴ is opened as handoff 30, composed by the Studio without the engineer's Sender assessment. Load adds `05-qa-to-studio.md` (criteria text), `23-studio-to-qa.md` (numbering), `28-studio-to-qa.md`, and QA's own handoff 29 (previous handoff; it holds no implementation history). The Handoff states a local loop limit: if any numbered criterion's text is still unavailable, QA names it and the Studio escalates to the Owner for that input instead of routing again.
  - I did not accept QA's partial evidence as a pass, and did not narrow the scope to it. Only QA decides the verdict, and the Studio does not decide verification. Phase 1 Build (6) still waits for the verdict. The Studio has not read the Handoffs 05 or 23 in this Route; their contents are as QA described them. The rest of the route is unchanged.
- After step 4a‴ (handoff 31, QA `pass`):
  - **Fits the plan.** QA gave a per-criterion verdict: criteria 1–6 pass at 30 and 60 FPS against `sim/build-0.5.md`, with only the allowed one-frame edge differences, and found no regression against 0.3. The dash-damage fix, including the hit-stun input change (D-003), is verified. No escalation trigger fires, and the loop limits are not reached (no criterion failed; the missing-input chain ended with 29/30).
  - Limits QA recorded, carried forward: the evidence is a build description, so the "at least 20 repeats" in criteria 1 and 2 was judged from the unconditional statements and not from a counted run; the description does not say outright that damage is not stored during a dash (judged sufficient for criterion 6); the file `sim/build-0.5.md` has the heading "0.3.2". These are labeling and evidence-form points and change nothing in the route.
  - Step 6 (Phase 1 Build) is opened as handoff 32 for `gameplay-engineer`, written by the Studio from the spec and plan artifacts and not from QA's reasoning. Its Load list has the Role contract, skill, the Phase 1 spec and visuals documents, build and repo notes, the Decisions it needs, QA's pass as the previous handoff, and handoffs 11 (Phase 1 spec origin), 16 (task list and plan), 17 (marker rule) and 20 (the engineer's earlier report that code values are absent). Phase 2 content is excluded. The rest of the route is unchanged.
- After step 6 (handoff 33, gameplay-engineer `question`):
  - **No change was built, and no failure.** The engineer listed every player-observable Phase 1 behavior and stopped, as handoff 32 and the Role contract require, because the spec is ambiguous or contradictory. Two items are contradictions (the wave trigger in 3.3: "alive" is true before anything has spawned; the Spitter's corner placement in 3.4 against the 5-tile rule in 3.3). Four are gaps (spawn point choice, which corners the Spitters cover, what "simul." means when a point is relocated, marker start times). The engineer also reports that Grub, player and projectile speed, heart count and room size are still not in the packet.
  - **Return rule applied: Build, "spec ambiguous, contradictory or missing a case" → Design (`game-designer`), then back to Build.** The engineer does not decide, and the Studio does not decide game content. Step 6b is opened as handoff 34. It lists the six questions with the engineer's options and proposed defaults (the Designer may accept or change them), and asks the Designer to say where the existing values come from, or that Phase 1 proceeds without them. Gameplay numbers are data (D-004), so this stays inside the Designer's authority. Build resumes as 6c after 6b, then Verify, Play and the rest as planned.
  - **No escalation.** The questions concern rules and parameters inside the vision, D-001 and the Decisions; no pillar, scope or Owner Decision is touched, and the missing values are something a Role (the Designer) can supply or waive. This is the first hand-back for this input, so the loop limit is not reached. If the answers change scope or a pillar, the Designer says so and the Studio routes to `game-director`; if they change what the markers must look like, to `art-director`.
  - Handoff 33 was left as written; its Previous handoff is 32. The held pieces (Spitter first shot no sooner than 1.0 s after it appears; marker visual) are noted in row 6c. `sim/build-0.5.md` remains the current build; nothing goes to QA from this step.
- After step 6b (handoff 35, game-designer `done`):
  - **Fits the plan.** The Designer answered all six questions, amended `design/g001-combat-escalation.md` and recorded D-008. The answers are rules and tuning values inside the Designer's authority. By the Designer's own statement, nothing changes the marker look, scope, a pillar, an input or an Owner Decision. No escalation trigger fires and no `game-director` or `art-director` step is needed. The Designer waived the existing values (Grub, player and projectile speed, hearts, room size) since no document has them; Phase 1 proceeds without them, which is a Designer call. This is the first time the values were waived, not a repeated hand-back.
  - Handoff 35 was addressed to `studio`, as the route required, so the Studio opened step 6c as handoff 36 for `gameplay-engineer`. It summarizes the Designer's answers and points to the spec and D-008 as authoritative, excludes Phase 2 content, repeats the constraints (no change to verified dash, hit-stun or invulnerability behavior; correct at 30 and 60 FPS; no RNG), and asks Build to report the open items (spawn effect reuse or minimal ring, readable existing values, room size versus the point lists and any fallback). Handoff 35 was not edited. Its Sender assessment stays on record and is not carried into the QA handoff.
  - Step 7 now names the amended criteria (1–5 and 10). The Designer's requests, that QA and then the playtest record the existing values and that the playtest record the "simul." arrival gaps, are added to rows 7 and 8. The loop limit for Build is stated in handoff 36: a second `question` for the same missing input with nothing new supplied goes to the Owner.
- After step 6c (handoff 37, gameplay-engineer `done`):
  - **Fits the plan.** The engineer stated the whole Phase 1 change and the values used (all from the spec), and answered the open items: no existing spawn effect was reused (none is named in its material), so the minimal ring from the visuals spec was built; none of the existing values (speeds, hearts, room size, hitboxes) were readable; the room-size question cannot be answered without a run. Three literal readings of the spec were recorded for the Designer's awareness (corner measured along the wall from the wall-face corner; Spitter first shot at appear + 1.0 s, then every 2 s; player position for the 5-tile test sampled on the logic frame that processes the scheduled marker start). None changes which stance works, none needed a hand-back, and they are not routed now; QA is asked to report whether the sampling rule produces differences beyond one frame between 30 and 60 FPS. No escalation trigger fires and no loop limit is reached.
  - **Verify (orchestration: "add `art-director` in parallel when the change affects visuals").** The Build added a new visual (the marker ring), which the engineer flagged for review. Steps 7a (`qa`, handoff 38) and 7b (`art-director`, handoff 39) are independent and run in parallel. Playtest (8) waits for both.
  - **Handoff 38 for QA was composed by the Studio.** It restates the change as made (section "Findings" of handoff 37, incl. the room table, wave scheduler, point choice, creation timing, marker, first shot and the unchanged areas), and leaves out the engineer's Sender assessment, confidence statements, "known risks" list and its reasoning, as the QA Role requires. Handoff 37 was not edited; its Sender assessment stays on record. Because the packet names `sim/build-0.6.md` as the newest simulated build, the Handoff names it as the build under test (the engineer named 0.5 as the baseline for unchanged behavior, which is kept as the regression baseline). The Handoff carries the QA requests from the earlier Routes (record existing values of spec 3.8 if visible, `SPAWN_FALLBACK` count and the room-size question, heading mismatch) and a local loop limit for a missing input. Handoff 05 (regression criteria text) is in the Load list to avoid the earlier Load gap (handoffs 28/29).
  - **Handoff 39 for the Art Director** carries only the marker ring description and the three review questions (readability in the dark, warning versus damage zone, burst versus attack telegraph). Phase 2 telegraphs and hit overlay are excluded.
  - The Studio has not opened any artifact beyond those in this Route; criteria wording is for QA to read from the spec. The handoff 37 Load entry "Skills: Studio to settle" is settled in handoff 38 (`verify-change`).
  - The rest of the route is unchanged. Phase 2 stays tentative behind the Phase 1 playtest (D-002).
- After steps 7a and 7b (handoffs 40, 41):
  - **7b fits the plan.** The Art Director passed the ring on the described look (A1, A3; A2 timing is QA's), decided no look change, and left three capture checks open. No escalation trigger and no return to Build.
  - **7a does not fully fit: no overall verdict, no failing criterion.** Criteria 3, 4, 5 and 10 pass; the regression check found no change against 0.5. Criteria 1 and 2 (Phase 1 part) need counted runs, and `sim/build-0.6.md` is a description with no counts. QA named the exact missing input and said it cannot choose how these criteria are judged.
  - **Return rule: Verify, "the expected behavior is undefined" → Design (`game-designer`).** The Studio does not decide verification scope or acceptance criteria. Both belong to the Designer (the spec's criteria and thresholds) and QA (the verdict), so the Studio does not narrow the scope to what QA could judge, and does not lower a threshold. Step 7c is opened as handoff 42 with the whole of QA's design items D1–D6 (frame-independent sampling, first-shot tolerance, the mixed fallback case, the room 2 fallback and the room-size dependence, and what "a dash taken in combat" is meant to show). Handoff 40 is its previous handoff; QA's handoff carries no Sender assessment, so nothing needed stripping for the Designer.
  - **No escalation now.** The loop limit for a missing input is not reached: this is the first hand-back about counted run data. The Designer can change the judging basis (for example move criteria 1 and 2 to the playtest as observation items), which is within the Designer's authority. An escalation to the Owner follows only if the Designer says the missing input can be produced by no Role, or that the choice depends on the Owner's taste. The Studio also does not treat QA's description-based passes on criteria 3, 4, 5 and 10 as less valid. They are what QA judged on the evidence available, with the limits it listed.
  - **Step 7d** (handoff 43) takes two narrow visual points to the Art Director, in parallel with 7c, because they are independent: QA noted that the build describes the dot as "hot, near-white" while the spec palette gives the hot core as `#FFC14D` (handoff 41 recorded it as matching), and the three capture checks cannot be done without captures. The Art Director decides whether each is covered by the description, carried to the playtest as a neutral item, or needs a statement in the build description. A look change would go to `gameplay-engineer` as a narrow Build through the Studio.
  - **Step 7e** (QA re-verify) is tentative: it opens only if 7c keeps part of criteria 1 and 2 as QA-judged, or changes a rule that the build must follow. **Step 8** (Play) waits for 7c and 7d, because their answers define what the playtest has to record, and the playtest must be composed without telling the tester what to expect.
  - Handoffs 40 and 41 were left as written. The remaining QA reports (existing values "not shown"; `SPAWN_FALLBACK` count unavailable; heading "0.3.3" in the 0.6 file) are labeling and evidence-form points; the first two travel to the playtest in row 8.
- After steps 7c and 7d (handoffs 44, 45):
  - **Both fit the plan, and neither fires an escalation trigger.** The Designer settled the judging basis inside its authority: criteria 1 and 2 (Phase 1 part) are judged at the playtest from counts, thresholds are unchanged, and QA records them as "deferred to playtest". Nothing is passed from a description. The Designer changed no rule, pillar, input, scope or Owner Decision (D-009). The Art Director corrected its own earlier review row: the build's "near-white" dot does not match the palette and D-006, so one narrow look change is required, a decision inside its authority that restores the spec's existing palette value.
  - **Tentative 7e is confirmed (`planned`).** 7c kept parts of criteria 4, 5 and 10 as QA-judged and amended their basis (first-shot basis, 1-tile margin rule, mixed-case point order as new sub-item (g)). Row 7e is narrowed to that scope. Criteria 1 and 2 are not re-verified by QA; they are recorded "deferred to playtest". Phase 1 stands as "verified, with criteria 1 and 2 open (deferred to playtest)".
  - **Narrow Build (7f, handoff 46) opens first, as one Handoff for both Roles' requests.** The Designer's clarification (a)–(d) and the Art Director's look change plus statements S0–S3 are small, touch the same build description, and are read by the same two verifiers afterwards, so one serial Build is cheaper than two (no code isolation or parallelism is warranted). The Studio wrote it from the Findings of 44 and 45 and did not decide any content: the colours, the 40% floor and the statement wording are the Art Director's, and the point order, sampling and first-shot rules are the Designer's. Where the build differs from the amended spec, the engineer changes it and reports, or hands back `question` if the spec is unclear.
  - **7e (QA) and 7g (Art Director re-review) wait for the Build and then run in parallel**: neither consumes the other's output. They cannot be opened now because the build description they verify does not exist until 7f is done. The QA Handoff will be composed by the Studio without the engineer's Sender assessment.
  - **Playtest (8) waits for 7e and 7g.** Its Handoff will be composed by the Studio from the build and the player profile only. The records listed in row 8 are neutral observation items. The play focus tells the tester which position to hold, not what result to expect. Handoffs 44 and 45 (including their Sender assessments) are not given to the Playtester.
  - **Pending Studio decision, not yet an escalation.** The Designer notes that if the playtest in this dry run is also a description with no counts, criteria 1 and 2 stay "not judged", and no Role can produce counted attempts from a description. This is a Studio call at the Route after step 8 (Review must not count them as met). If the playtest returns without counts, the Studio will escalate to the Owner: accept "not judged" for the dry run, or stop. That is not triggered now; the playtest has not run, and this would be the first time the input is missing.
  - Handoffs 44 and 45 were left as written. Their Load entries name a non-existent Studio Role file (44) and no Role (45); both are addressed to `studio` and no later step starts from them.

## Next action

`gameplay-engineer` runs step 7f from [46-studio-to-gameplay-engineer.md](46-studio-to-gameplay-engineer.md): ring dot `#FFC14D`, statements S0–S3, and the clarification of spec points (a)–(d). Result addressed to `studio`.

After it (Route): open 7e (`qa`, narrow re-verify of criterion 10 (c)(d)(g), criterion 4 first-shot basis and criterion 5 margin rule, with criteria 1 and 2 recorded "deferred to playtest") and 7g (`art-director`, dot colour and S0–S3) in parallel, each as a fresh Handoff composed by the Studio from permitted information only. If the Build reports that a built behavior differed from the amended spec, QA's re-verify covers it. If the engineer hands back `question`, route it to `game-designer` (spec) or `art-director` (look), and escalate to the Owner only for the same missing input twice. After 7e and 7g pass, compose the fresh playtest Handoff (step 8) per row 8. A QA fail goes back to Build (a second fail on the same criterion goes to `technical-director`).

## Outcome

(To be filled at close, in Japanese.)
>>>END

<<<FILE goals/G-001-combat-monotony/47-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-001
seq: 47
from: gameplay-engineer
to: studio
stage: Build
outcome: done
---
# 47: gameplay-engineer → studio — Ring dot `#FFC14D`, statements S0–S3, and points (a)–(d) stated; QA re-verify and Art Director re-review follow

## Task

Update `sim/build-0.6.md` from the Findings below. Send it to QA (without the Sender assessment) for the narrow re-verify, and to the Art Director for the dot and S0–S3 re-review in parallel.

## Context

G-001, Phase 1, build 0.6. This is the narrow Build from handoff 46. It covers the Art Director's dot change and statements (handoff 45) and the Game Designer's clarification of the amended spec (handoff 44, D-009).

This step could not run the game or read its code. The facts below come from the packet: `sim/build-0.6.md`, `sim/repo-notes.md` and my handoff 37. Where those documents did not state a behavior, I say so and treat it as set by this change. I do not claim the code already did it.

## Findings

### 1. Part A: change made

Arrival ring, solid phase (0.6–0.8 s) only:

- The centre dot is `#FFC14D` at full brightness. It has no tint toward white or blue.
- There is no white or cold-white bloom or glow. Any glow around the dot uses only `#FFC14D` or `#FF5A1F`.
- Before 0.6 s the dot stays dim amber, as built.
- Unchanged: ring colour `#FF5A1F`, all timings (solid phase starts at 0.6 s, burst at 0.8 s), the ring's size and shape, and all rules.

Why this counts as "changed": `sim/build-0.6.md` said the dot turned to "a hot, near-white core colour". `sim/repo-notes.md` names `#FFC14D` as the dot's palette value but says only "hot-core colour" for the solid phase, with no hex. Because the build description stated near-white, I set the solid-phase dot explicitly to `#FFC14D`, with no white component.

**Wording for `sim/build-0.6.md`, "The arrival ring" section:**

- Replace "the dot turns to a hot, near-white core colour" with the S0 sentence below.
- Add S1, S2 and S3 as ring bullets.

### 2. Statements S0–S3, final wording

- **S0 — changed.** "In the last 0.2 s (0.6 to 0.8 s) the dot is amber `#FFC14D` at full brightness." This replaces "hot, near-white core colour".
- **S1 — changed.** "The ring and its dot are drawn self-lit and do not depend on the lantern's light. At 0.0 s the ring's brightness is at least 40% of its brightness at 0.6–0.8 s."
  - Before: the packet said only that the ring is visible from 8 or more tiles for its whole 0.8 s. It did not state lantern independence or a brightness at 0.0 s, and I cannot read the values.
  - Now: the ring and dot are drawn emissive and do not read the lantern's light radius. The brightness ramp is linear in game time from 40% of peak at 0.0 s to 100% at 0.6 s, and 100% from 0.6 s to 0.8 s.
- **S2 — changed.** "The 0.8 s burst uses only `#FF5A1F` and `#FFC14D`. It contains no white, near-white or cold-white element."
  - Before: the burst colour was not stated.
  - Now: the burst palette is restricted to those two colours. Its duration (at most 0.15 s) and its not hiding the new enemy are unchanged.
- **S3 — partly already so, partly changed.** "Rings are outlines with no fill. Where two rings overlap or touch, brightness does not add above a single ring's peak, and each ring keeps its own dot."
  - Already so: the ring has no fill larger than the ring itself (build description, repo notes).
  - Changed: overlap handling was not stated. Where rings overlap, brightness is now capped at a single ring's peak, and each ring draws its own dot.

### 3. Part B: points (a)–(d) as the build behaves

**(a) Point choice (3.3).** The routine walks the candidate list in order, per enemy, once at its marker start.

- Step A: take the first candidate that is both at least 5 tiles from the player and not occupied. Occupied means an active marker at the point, or a living enemy within 1.5 tiles.
- Step B: if none passes both, take the farthest candidate that is not occupied. This is the mixed case: a near, free point wins over a far, occupied point.
- Step C: if all candidates are occupied, take the farthest overall.
- Ties in B or C go to the earlier list entry.
- This matches the amended order. `sim/repo-notes.md` and handoff 37 already described the same order, including the mixed case.
- Changed: the tie-break was not stated in those documents. It is now explicit and implemented as "earlier list entry wins on equal distance".
- Enemies with the same marker start are processed in table order on the same frame. An earlier enemy's new marker is therefore active (occupying its point) when the next one is evaluated.
- Pending enemies do not count as occupancy.
- Every step B or C choice writes a `SPAWN_FALLBACK` line.

**(b) Sampling.** The player position and the occupancy are both read on the first logic frame at or after the scheduled marker start.

- Handoff 37 described this only for the player position. The occupancy check runs in the same routine on the same frame, so it is covered. This was not stated before; the behavior is now confirmed and stated.
- At 30 FPS this can be up to one frame (0.034 s) later than at 60 FPS.
- The marker's end and the enemy's appearance use the scheduled timestamps, not the frame time.

**(c) Spitter first shot.** It is scheduled at the scheduled appearance (`markerStart + 0.8 s`) + 1.0 s, then every 2 s. It is already so.

- The shot is a scheduled timestamp on the game clock. The log line for it carries that scheduled value.
- A Spitter never fires on the frame it appears.

**(d) Existing values (3.8).** All are **not available**. I did not estimate any.

| Value | Status |
|---|---|
| Grub speed | not available |
| Player speed | not available |
| Projectile speed | not available |
| Projectile range | not available |
| Player hearts | not available |
| Room size (W×H) | not available |
| Grub hitbox size | not available |
| Player hitbox size | not available |
| Spitter hitbox size | not available |

- The packet gives none of these, and I had no way to read the game.
- Phase 1 data uses only tiles, seconds and room-relative points, so it needs none of them.
- QA and the playtest record them (spec 3.8, 6a).

### 4. Other described behavior of build 0.6 that is different

- The ring's brightness curve from 0.0 to 0.6 s now starts at 40% of peak. The build said only "dim to bright" and "gets brighter", and gave no start value. The rule is still a rise to full brightness, reaching it at 0.6 s as before.
- The solid-phase dot and the burst colours are as stated in Parts 1 and 2.
- Apart from those, **none**. No timing, wave rule, spawn rule, dash, hit-stun or invulnerability behavior (the build 0.5 baseline) is touched. No new input. No Phase 2 content.

### How to exercise it

- Dot colour: capture the ring at 0.5 s and at 0.7 s. The dot should be dim amber before 0.6 s and `#FFC14D` at full brightness from 0.6 s, with no white in the dot or its glow.
- Burst colour: capture the burst frames. They contain only `#FF5A1F` and `#FFC14D`.
- Brightness at the start: compare ring brightness at 0.0 s with that at 0.6–0.8 s. The ratio should be at least 0.40.
- Lantern independence: stand 8 or more tiles away, outside lantern light, and check the ring is visible for its whole 0.8 s.
- Two rings: room 3 wave 2 and room 5 wave 1 (west edge) have simultaneous markers. Check that overlapping or touching rings never exceed a single ring's peak and that each keeps its dot.
- Points (a)–(c): spec criterion 10(c), (d) and (g), criterion 4 (first-shot basis) and criterion 5 (1-tile margin rule).

Criteria addressed: criterion 4 (first-shot basis), criterion 5, criterion 10 (c)(d)(g), and the Art Director's pass condition for the ring and burst.

Known risks:

- The 40% brightness floor and the overlap cap are explicit settings from this change. They have no capture evidence behind them.
- The ring is still a placeholder.

## Decisions already made

- D-001: one-button combat. D-004: gameplay numbers are data.
- D-006: cold-white `#E8F4FF` is reserved for hit feedback on flinch-immune enemies.
- D-008: Phase 1 spawn and wave rules.
- D-009: judging basis for criteria 1 and 2, and the D2–D6 answers.

## Constraints

- No timing or rule was changed.
- The dash, hit-stun and invulnerability behavior (build 0.5 baseline) is untouched.
- Behavior is correct at 30 and 60 FPS. There is no RNG in spawn choice. No new input. No Phase 2 content.

## Open questions

None blocking.

- The existing values in (d) are still not available. They stay a request to QA and the playtest.
- The `SPAWN_FALLBACK` count per room is still unknown.

## Expected output

- The Studio updates `sim/build-0.6.md` with the S0–S3 wording above and the Part B statements.
- The Studio sends the result to QA (without the Sender assessment) for the narrow re-verify: criterion 10 (c)(d)(g), criterion 4 first-shot basis, criterion 5 margin rule. Criteria 1 and 2 stay "deferred to playtest".
- The Studio sends the dot and S0–S3 to the Art Director for re-review. The pass condition is that the build description states `#FFC14D` for the dot and no ring or burst element is white or near-white.

## Sender assessment

- I could not run or read the game, and I ran no tests. Nothing here is a passing run.
- S0 is high confidence: the colour is exactly specified, and it is a data-level fix.
- S1 and S2 are medium confidence. The packet did not state the prior behavior, so I labelled them "changed" rather than claim they already held. If the code already behaved this way, only the documentation changed.
- The tie-break and the occupancy-sampling statements in (a) and (b) are consistent with the notes, but those notes did not state them. QA should check them in a scripted run, using criterion 10(g).
- The 40% ramp start is my choice of how to meet the Art Director's "at least 40%" floor. It can be raised by changing one data value.

## Load

- Role: studio/roles/qa.md (QA), studio/roles/art-director.md (Art Director)
- Skills: Studio to settle when routing
- Project: design/g001-combat-escalation.md (3.3, 3.8, 6, 6a, criteria 4, 5, 10); design/g001-telegraph-visuals.md (sections 2, 3, 7 A1–A3); sim/build-0.6.md
- Decisions: decisions/D-006-lunge-cue-realignment-and-flinch-immune-hit-feedback.md; decisions/D-008-phase-1-spawn-and-wave-rules.md; decisions/D-009-judging-basis-criteria-1-and-2.md
- Previous handoff: goals/G-001-combat-monotony/46-studio-to-gameplay-engineer.md
>>>END
