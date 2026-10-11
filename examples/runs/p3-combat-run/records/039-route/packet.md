# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/31-qa-to-studio.md
next_seq: 32
context_request: allowed once (@need, up to 8 paths)
current_build: sim/build-0.5.md (newest simulated build; older ones are history)

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/31-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 32
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
goals/G-001-combat-monotony/goal.md
project.md
sim/build-0.3.md
sim/build-0.4.md
sim/build-0.5.md
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
- Design: is the intended behavior specified well enough to build? Not for the chosen direction. Done for Phase 1 and for Phase 2 (handoff 11, `design/g001-combat-escalation.md`, adjusted in handoff 22 and D-005). The Phase 2 telegraph visuals were realigned to the corrected dash window in step 5d (handoff 25, D-006, `design/g001-telegraph-visuals.md`). One data value (`committed_start`, provisional 0.45 s) is still to be confirmed by the Game Designer after Build's report.
- Plan: needed for Phase 2 (feasibility and cost). Answered in handoff 16 and D-004: feasible and cheap. Phase 1 needs no separate Plan (handoff 16).
- Build: the dash-damage defect fix (done, handoff 08), the hit-stun input made observable (done, handoff 20), then Phase 1 and Phase 2 of the chosen direction.
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
| 4a‴ | Verify (attempt 5: same scope as 4a″, with the criteria text in Load) | qa | verify-change | open (fresh Handoff composed by the Studio without the engineer's Sender assessment; Load adds handoffs 05, 23, 28 and QA's own 29) | [30-studio-to-qa.md](30-studio-to-qa.md) |
| 6 | Build (Phase 1: encounter escalation) | gameplay-engineer | implement-change | planned (after the 4a‴ verdict; no separate Plan; uses the marker rule from 5b and the task list in handoff 16; Build reports Grub, player and projectile speed, heart count, room size, whether an existing spawn effect exists and passes A1–A5; handoff 20 says none of these numbers are in the code notes, so Build must state the values it uses) | — |
| 7 | Verify (Phase 1) | qa | verify-change | planned (after 6) | — |
| 8 | Play (Phase 1) | playtester | playtest-session | planned (after 7; fresh Handoff without implementation history; record real-time run length and per-room clear time) | — |
| 9 | Build (Phase 2: behavior variants) | gameplay-engineer | implement-change | tentative (after steps 6–8, if the Phase 1 playtest leaves combat still monotonous, per D-002 "B then A"; spec feasible per 5a, readable per 5b, visuals realigned per 5d; its Handoff must carry the "confirm after the report" values from spec section 7 as data values for the Designer to confirm, `committed_start` (default 0.45 s, clamped to [0, 0.60 s], clamp reported), and the 5d Build-report items: existing spawn effect, hit spark and hit sound to reuse, lunge hit width, projectile range, Spitter mouth position; `design/combat.md` must be updated for Flinch and the Phase 2 enemies; attach the Designer's "first overlap uses up the lunge's single hit" note from handoff 22) | — |
| 9b | Design (confirm Phase 2 dash-window figures and `committed_start` after Build's report; decide whether a 2 HP enemy needs a persistent damage marker, proposed after playtest) | game-designer | write-design-spec | tentative (after 9's report; one data value, no art change needed) | — |
| 10a | Verify (Phase 2; criteria 2, 4, 5, 7–9 of the spec) | qa | verify-change | tentative (after 9 and 9b) | — |
| 10b | Verify (Phase 2 visuals, telegraphs and hit feedback; criteria A1–A13) | art-director | visual-review | tentative (after 9; parallel with 10a) | — |
| 11 | Play (Phase 2) | playtester | playtest-session | tentative (after 10; readability of the 0.15 s committed stage at 30 FPS in a dark cave is a playtest item, as are whether the late-dash cue is learnable and whether hits on flinch-immune enemies are noticed) | — |
| 12 | Review | game-director | review-outcome | planned | — |

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

## Next action

`qa` runs step 4a‴ from [30-studio-to-qa.md](30-studio-to-qa.md): verify the dash-damage fix, including the hit-stun input, against `sim/build-0.5.md` with the criteria text from `05-qa-to-studio.md` now in Load; address the result to `studio`.

After the verdict (Route): pass → open Phase 1 Build (6); fail → Build with the report (a second failure on the same criterion → `technical-director`); `question` because a criterion's text is still unavailable → escalate to the Owner for that input.

## Outcome

(To be filled at close, in Japanese.)
>>>END

<<<FILE goals/G-001-combat-monotony/31-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 31
from: qa
to: studio
stage: Verify
outcome: pass
---
# 31: qa → studio — Verification of the dash-damage fix (incl. hit-stun input) against build 0.5: criteria 1–6 pass, overall pass

## Task

Verify the dash-damage fix, including the hit-stun input part, against `sim/build-0.5.md` (D-007). Give a verdict for criteria 1–6 and an overall verdict. The criteria wording is taken from handoff 05 (it governs). Handoff 23 supplies the numbering.

**Overall verdict: pass.** All six criteria pass at 30 FPS and 60 FPS. The only differences between the two frame rates are the one-frame edge differences that the build and the spec allow.

## Context

- Build under verification: `sim/build-0.5.md`. Baseline for the regression check: `sim/build-0.3.md`. `sim/build-0.4.md` was not used.
- The criteria text is now available, so this closes the question left open in handoff 29. Nothing is missing, and no criterion is unclear.
- Handoff 05 and handoff 23 agree. Handoff 23 characterises criteria 1 and 2 as dash protection, criterion 5 as hit-stun with no input, and criterion 6 as the frame after a dash ends. That matches the wording in 05. I found no disagreement to report.
- The build is a player-observable description, not a runnable build. Each verdict below rests on what the description states. The description says its statements hold "same at 30 FPS and 60 FPS; only the exact frame at which an edge lands differs".

## Findings

### Per-criterion verdicts (wording from handoff 05)

| # | Criterion (short) | Verdict | Evidence in `sim/build-0.5.md` |
|---|---|---|---|
| 1 | Dash at the earliest accepted moment (0.3 s after a hit): no damage during the 0.25 s dash, with a Grub in contact or a projectile arriving mid-dash. At least 20 repeats per frame rate with no damage. | PASS | "Dash started between 0.3 s and 0.55 s after a hit: no damage during the dash, and none after it ends. You stay protected until 0.8 s after the hit." "A dash or attack pressed just after 0.3 s works normally, and the dash is fully protected." "This holds for Grub contact and Spitter projectiles alike." The 0.3 baseline line "Occasionally … you take damage partway through the dash" is gone. The description states the behavior unconditionally, with no "occasionally" qualifier. |
| 2 | Dash presses at several delays after the hit, including early (during hit-stun) and just before, at and just after 0.8 s: no damage during any active dash. | PASS | Presses at about 0.05, 0.15 and 0.28 s start no dash, so no active dash exists to be damaged. This is consistent with D-003. Dashes started at 0.3–0.55 s and at 0.55 s to just under 0.8 s: no damage during the dash. Protection lasts through the later of the dash end and 0.8 s. A dash started at 0.8 s or later gets its own 0.25 s of protection. An event landing exactly on the 0.8 s or 0.25 s boundary counts as after protection, and may differ by one frame between 30 and 60 FPS. That is allowed. |
| 3 | Different dash directions (toward and away from the source), rooms 1–5, Grubs and Spitters. | PASS | "This holds for Grub contact and Spitter projectiles alike, and for dashes toward or away from the damage source." The description gives no room-specific exception for rooms 1–5. |
| 4 | A dash with no preceding hit still gives full 0.25 s invulnerability (no regression). | PASS | "Dash with no preceding hit: you cannot be damaged for the full 0.25 s of the dash." |
| 5 | Existing rules hold: hit-stun 0.3 s with no input; hit invulnerability until 0.8 s; dash cooldown 0.6 s; an attack pressed during a dash fires when the dash ends. | PASS | Stun: "You are stunned for the first 0.3 s", and dash and attack presses in that window do nothing. This matches D-003: nothing is buffered, held buttons do not fire, a fresh press works, and a hit cancels any waiting request. Hit invulnerability: "you cannot be damaged for 0.8 s after the hit". Cooldown: "the 0.6 s dash cooldown [is] unchanged". Attack queue: "If a swipe was pressed during a dash, it still fires when the dash ends." |
| 6 | Damage previously taken mid-dash is not delayed to land right after the dash ends. A hit landing after the invulnerability windows expire is normal. | PASS | After a hit, a dash is covered through the later of the dash end and 0.8 s, so nothing lands at the dash end while hit protection is active. With no preceding hit, "damage can land immediately after it ends". This is the normal case the criterion allows, because both windows have expired. The boundary frame counts as after protection and may differ by one frame between frame rates. Limit of this evidence: the description does not say outright that damage is not stored during a dash. It says only that no damage lands during the dash, and that damage afterwards follows the normal rules. I judged that sufficient for criterion 6 as worded. |

### Hit-stun input (the new part of criteria 2 and 5), re-checked against the criteria text

All six statements from handoff 28 are stated in the build and match D-003:
1. A dash press in hit-stun starts no dash and no cooldown.
2. An attack press in hit-stun gives no swipe, and nothing fires later.
3. Nothing fires at the end of the stun.
4. A held button does not fire. Release and re-press works.
5. Presses after 0.3 s work normally. A press exactly on the 0.3 s edge may differ by one frame between 30 and 60 FPS.
6. The hit-stun length is the same at 30 and 60 FPS.

Criterion 2 in handoff 05 was written before D-003. It lists "pressed early, during hit-stun" as a delay to test. Under D-003 such a press starts no dash, so the criterion's condition ("no damage during an active dash") holds because no dash exists. This is not a spec conflict.

### Conditions and limits

- **Frame rates:** the description states identical behavior at 30 and 60 FPS, apart from the exact edge frame. The only differences are the allowed one-frame boundary differences (0.3 s, 0.25 s and 0.8 s edges).
- **"At least 20 repeats per frame rate" (criteria 1 and 2):** the build is a description, so I could not actually repeat the dash 20 times. I judged against the unconditional statements above. If the Studio wants a counted run, it needs a runnable build.

### Regression check against `sim/build-0.3.md`

- Rooms 1–5, enemy behavior, the "hold position and swipe" pattern, and the rarely needed dash read the same as in 0.3. This is expected, because Phase 1 is not built yet.
- Dash distance, dash duration (0.25 s), the 0.6 s cooldown, and enemies, rooms and attacks are stated as unchanged.
- The only intended difference from 0.3 is the removal of the "occasionally take damage partway through the dash" line.
- No regression found.

### Optional notes

- **Frame right after a dash ends with a source in contact:** with no preceding hit, damage can land on that frame. After a hit, protection continues to the later of the dash end and 0.8 s. The boundary frame counts as after protection and may differ by one frame between 30 and 60 FPS, which is allowed.
- **Naming mismatch:** the file is `sim/build-0.5.md` but its heading reads "Simulated build 0.3.2". This is a labeling issue only. I treated the file as build 0.5 per D-007.
- **Invulnerability flicker and sound cues:** none described, not checked.

## Decisions already made

- D-003: input during hit-stun is ignored, not buffered. Build 0.5 matches it.
- D-007: verify against `sim/build-0.5.md`. I did.

## Constraints

- I did not widen or narrow the criteria. I did not modify the build.
- The verdict is limited to what the description states, as noted under "Conditions and limits".

## Open questions

None. The wording of criteria 1–6 was sufficient for a verdict on each. The loop-limit escalation to the Owner is not needed.

## Expected output

For `studio`: record the dash-damage fix, including the hit-stun input change, as verified (pass). Phase 1 of the chosen direction may proceed.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: sim/build-0.5.md, sim/build-0.3.md (baseline only), design/combat.md, project.md#constraints
- Decisions: decisions/D-003-input-during-hit-stun.md, decisions/D-007-verify-against-build-0-5.md
- Previous handoff: goals/G-001-combat-monotony/30-studio-to-qa.md
>>>END
