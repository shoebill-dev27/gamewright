# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/20-gameplay-engineer-to-studio.md, goals/G-001-combat-monotony/21-qa-to-studio.md, goals/G-001-combat-monotony/22-game-designer-to-studio.md
next_seq: 23
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/20-gameplay-engineer-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/21-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/22-game-designer-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 23
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
- Design: is the intended behavior specified well enough to build? Not for the chosen direction. Done for Phase 1 and as proposals for Phase 2 (handoff 11, `design/g001-combat-escalation.md`). Phase 2 needs adjustment after the Plan and art answers (step 5c).
- Plan: needed for Phase 2 (feasibility and cost). Answered in handoff 16 and D-004: feasible and cheap. Phase 1 needs no separate Plan (handoff 16).
- Build: the dash-damage defect fix (done, handoff 08; one case still to make observable, step 3c), then Phase 1 and Phase 2 of the chosen direction.
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
| 3c | Build (make hit-stun dash/attack input observable and consistent with D-003; report code values) | gameplay-engineer | implement-change | open (parallel with 5c) | [18-studio-to-gameplay-engineer.md](18-studio-to-gameplay-engineer.md) |
| 4a | Verify (dash-damage fix) | qa | verify-change | open → blocked: attempt 1 `question` (build not in packet, [10](10-qa-to-studio.md)); attempt 2 `question` (hit-stun press not observable in the build, [15](15-qa-to-studio.md)). Attempt 3 follows 3c. | [12-studio-to-qa.md](12-studio-to-qa.md) (attempt 1: [09-studio-to-qa.md](09-studio-to-qa.md)) |
| 4a′ | Verify (attempt 3: dash-damage fix incl. hit-stun input) | qa | verify-change | planned (after 3c; fresh Handoff composed by the Studio without the engineer's Sender assessment) | — |
| 4b | Design (Phase 1 in full; Phase 2 as proposed behaviors) | game-designer | write-design-spec | done | [07-game-director-to-game-designer.md](07-game-director-to-game-designer.md) → [11-game-designer-to-studio.md](11-game-designer-to-studio.md) |
| 5a | Plan (Phase 2 feasibility and cost) | technical-director | technical-plan | done | [13-studio-to-technical-director.md](13-studio-to-technical-director.md) → [16-technical-director-to-studio.md](16-technical-director-to-studio.md) (D-004) |
| 5b | Design (spawn marker and Phase 2 telegraph visuals) | art-director | write-design-spec | done | [14-studio-to-art-director.md](14-studio-to-art-director.md) → [17-art-director-to-studio.md](17-art-director-to-studio.md) (`design/g001-telegraph-visuals.md`) |
| 5c | Design (adjust Phase 2 spec from 5a and 5b answers) | game-designer | write-design-spec | open (parallel with 3c) | [19-studio-to-game-designer.md](19-studio-to-game-designer.md) |
| 5d | Design (realign telegraph visuals if the dash window or sub-stage timing changed) | art-director | write-design-spec | tentative (after 5c, only if 5c changes the spec 4.1 dash window or the lunge/charge sub-stage timing) | — |
| 6 | Build (Phase 1: encounter escalation) | gameplay-engineer | implement-change | planned (after 4a′ pass; no separate Plan; uses the marker rule from 5b and the task list in handoff 16; Build reports Grub, player and projectile speed, heart count, room size, whether an existing spawn effect exists and passes A1–A5) | — |
| 7 | Verify (Phase 1) | qa | verify-change | planned (after 6) | — |
| 8 | Play (Phase 1) | playtester | playtest-session | planned (after 7; fresh Handoff without implementation history; record real-time run length and per-room clear time) | — |
| 9 | Build (Phase 2: behavior variants) | gameplay-engineer | implement-change | tentative (after 5c and, if needed, 5d; feasible per 5a, readable per 5b) | — |
| 10a | Verify (Phase 2) | qa | verify-change | tentative (after 9) | — |
| 10b | Verify (Phase 2 visuals, telegraphs; criteria A1–A12) | art-director | visual-review | tentative (after 9; parallel with 10a) | — |
| 11 | Play (Phase 2) | playtester | playtest-session | tentative (after 10) | — |
| 12 | Review | game-director | review-outcome | planned | — |

Status: planned | tentative | open | done | skipped.

## Route changes

- After step 1 (Observe, playtester): the report matches the plan on the experience side (monotony confirmed: one winning approach in every room, little pressure to move, dash unused in combat), so Diagnose followed as planned. It also contained a possible defect (damage during a dash after being hit). Per the return rule "Play/Observe: defect → Observe (`qa`)", step 2b was added as a parallel step. Handoff 02 was edited in place (still from `playtester`) to add the Owner's report, mark the dash-defect item as routed to `qa`, and fill in Load and Expected output.
- After steps 2a and 2b: 2a produced a diagnosis with three options of different scope and cost (handoff 04), so Decide (`game-director`) followed. 2b confirmed a defect against specified behavior (handoff 05), so Build and Verify for the fix joined the route; no Design is needed because `design/combat.md` already specifies the behavior. QA's non-blocking question (how to treat a dash pressed during hit-stun) was left for `game-designer`.
- After steps 3a and 3b: 3a chose B then A with C in reserve (D-002, handoff 07); no escalation trigger fires, since everything stays within D-001 and the pillars. 3b delivered the invulnerability fix (handoff 08), which must be verified independently. Verify of the fix (4a) and Design of the chosen direction (4b) are independent, so they ran as one parallel group. Handoff 09 for QA was composed by the Studio without the engineer's Sender assessment or root-cause reasoning. Phase 1 Build (6) waits for 4a so it does not stack on an unverified fix. Phase 2 build, verify and play were kept tentative.
- After steps 4a (attempt 1) and 4b: 4a came back as `question` (handoff 10): QA had no build file in its packet, so nothing was verified. This is the first such hand-back for this input and the cause was a missing Load entry, not a Role problem, so 4a was re-opened with handoff 12, which names `sim/build-0.4.md` (latest) and `sim/build-0.3.md` (baseline) explicitly. 4b is done (handoff 11): Phase 1 is build-ready, Phase 2 is proposed. Per the Designer's request, Phase 2 went to `technical-director` (5a, handoff 13) and `art-director` (5b, handoff 14), opened in parallel with 4a. A step 5c was added so the designer adjusts the Phase 2 spec from both answers before any Phase 2 Build.
- After steps 4a (attempt 2), 5a and 5b (handoffs 15, 16, 17):
  - **4a (attempt 2)** came back as `question` again (handoff 15). The missing input is different this time: the build was supplied, and QA found everything consistent with the six criteria except one case. The build files do not say what happens when dash or attack is pressed during hit-stun (D-003 says ignored, not buffered), so QA could not give a verdict. The loop limit ("same missing input twice") does not apply, because the first hand-back was about a missing file and this one is about a missing build behavior. It does apply from now on: a further `question` for the hit-stun observation goes to the Owner. QA's blocker is a build-observability gap and not a spec gap (D-003 defines the behavior), so it goes to `gameplay-engineer` as a narrow Build (3c, handoff 18), not to `game-designer`. Handoff 18 also asks for the code-side values that the TD and Art Director need, and for confirmation that `sim/build-0.4.md` ("0.3.1" in its heading) is the latest build. After 3c, Verify is re-opened as 4a′ with a fresh Handoff composed by the Studio for QA without Sender assessment. Phase 1 Build (6) stays gated on a 4a′ pass. Handoff 15 needs no edit; it was left as written.
  - **5a (Plan, handoff 16 and D-004)**: both Phase 2 behaviors are feasible and cheap (Fan Spitter over the repositioning Spitter); Phase 1 needs no separate Plan or isolated workspace and can be one serial Build; no parallelization. The result fits the plan, so 5a is done and the tentative Phase 2 Build stays tentative until 5c. The TD found that the existing 0.2 s Flinch conflicts with the Phase 2 spec and that the spec's dash window text does not match the real timing. Both are player-facing rules and belong to `game-designer`; neither changes direction or scope, so no `game-director` step or escalation.
  - **5b (Design, handoff 17 and `design/g001-telegraph-visuals.md`)**: telegraph visuals for the spawn marker and both variants; no gameplay timing change; the lunge's committed-stage visual is tied to the spec 4.1 dash window. The result fits the plan, so 5b is done. A tentative step 5d was added: if 5c changes the dash window or sub-stage timing, the Art Director realigns the visuals. The marker rule (reuse an existing effect if it passes A1–A5, else build the minimal ring) goes to Build 6 through the route notes and handoff 17's spec; Phase 1 Build is not yet open.
  - **5c** opened as handoff 19, in parallel with 3c (neither consumes the other's output). The designer is told that hitbox sizes and speeds are requested from the engineer, so the rule for the dash window should hold whatever they turn out to be.
  - No escalation trigger fired: no pillar, Owner Decision, scope or irreversibility change.

## Next action

Two steps are open in parallel (3c, 5c). Run Route after each (or after both):
- 3c: `gameplay-engineer` makes the hit-stun dash/attack input handling observable and consistent with D-003, and reports code values, from `18-studio-to-gameplay-engineer.md` (skill `implement-change`). Result to `studio`.
- 5c: `game-designer` adjusts the Phase 2 spec and answers the flinch, contact-damage, dash-window and Fan Spitter questions from `19-studio-to-game-designer.md` (skill `write-design-spec`). Result to `studio`.

After 3c: compose a Handoff for `qa` (4a′) from the updated `sim/build-*.md`, the acceptance criteria in `05-qa-to-studio.md` and D-003, without the engineer's Sender assessment. Ask QA to cover the hit-stun case at 30 and 60 FPS. On a further `question` for the same hit-stun observation, escalate to the Owner. On pass, open Phase 1 Build (6). On fail, return to Build with the report (a second failure of the same criterion goes to `technical-director`).

After 5c: if the dash window or sub-stage timing changed, open 5d (`art-director`); if the designer finds that a change touches scope or a pillar, route to `game-director`. Otherwise Phase 2 Build (9) stays tentative until Phase 1 is built, verified and played (steps 6–8).

## Outcome

(To be filled at close, in Japanese.)
>>>END

<<<FILE goals/G-001-combat-monotony/20-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-001
seq: 20
from: gameplay-engineer
to: studio
stage: Verify
outcome: done
---
# 20: gameplay-engineer → studio — Hit-stun input is now ignored and not buffered (D-003); code-side values reported

## Task

Compose a verification Handoff for `qa` from the Findings below. The build's observable behavior for a dash or attack pressed during hit-stun is now stated and matches D-003. QA also needs to confirm that `sim/build-0.4.md` is the intended latest build. Questions 3 and 4 are answered for the Technical Director and Art Director.

## Context

Goal G-001. QA's handoff 15 could not judge a dash pressed during the 0.3 s hit-stun, because `sim/build-0.4.md` said only "behaves as it did in 0.3" and `sim/build-0.3.md` does not describe it. This step makes the behavior explicit. Scope is hit-stun input handling only. No Phase 1 work and no new input.

## Findings

### Change (stated exactly; counts as made in this dry run)

**What changes.** During hit-stun, dash and attack presses are discarded. Nothing is stored and nothing fires when hit-stun ends.

**Where.** The player's input handling, at the point where button presses are turned into a dash start or an attack start. The player gets a third timestamp on the accumulated game clock, `hitStunUntil`. It is set to hit time + 0.3 s at the same place `hitInvulnUntil` is set. Hit-stun is therefore a timestamp comparison, not a frame count, and behaves the same at 30 and 60 FPS.

1. While `now < hitStunUntil`, a dash or attack press is dropped. It does not start an action, does not enter the "attack queued during a dash" slot, and does not enter any other buffer.
2. When a hit lands, any pending dash or attack request is cleared, so nothing carries into hit-stun.
3. Presses are edge-triggered. A button held through the end of hit-stun does not fire at that moment. A new press after hit-stun ends is needed.
4. A press at or after `hitStunUntil` is accepted normally. A press landing exactly on the 0.3 s edge may differ by one frame between 30 and 60 FPS. This is the same boundary convention as the 0.8 s and 0.25 s edges.

**Unchanged.**
- `isInvulnerable(now)`, `hitInvulnUntil` and `dashInvulnUntil`.
- Dash distance, duration and the 0.6 s cooldown.
- The attack queued during a dash still fires when the dash ends. A hit cannot land during a dash, so hit-stun cannot overlap that queue.
- Enemies, rooms and the attack.

**How to exercise it (at 30 FPS and 60 FPS).**
1. Take a hit. Press dash at several moments inside the first 0.3 s, for example about 0.05, 0.15 and 0.28 s after the hit.
   - Expected: the player does not dash.
   - Expected: no dash starts when hit-stun ends at 0.3 s.
   - Expected: the dash cooldown does not start.
2. Repeat with attack.
   - Expected: no swipe, either then or at 0.3 s.
3. Repeat 1 and 2 with the button held down through the end of hit-stun.
   - Expected: nothing fires when hit-stun ends. A fresh press afterwards works.
4. Press dash and attack just after 0.3 s, as a fresh press.
   - Expected: both work, and the dash is fully protected (criteria 1 and 2 in `05-qa-to-studio.md`).
5. Run the dash-delay matrix from handoff 15 (0.3 to 0.85 s) as before.

**Criteria addressed.** Criterion 2 (dash pressed during hit-stun) and criterion 5 (hit-stun lasts 0.3 s with no input). The other criteria are not affected by this change.

**Tests added.** Unit tests on the simulated game clock at fixed steps of 1/30 s and 1/60 s and with varying delta times:
- Dash and attack presses at several times inside 0.3 s produce no action at press time, at 0.3 s, or later.
- A press just after 0.3 s fires normally.
- A button held through 0.3 s does not fire.
- A hit clears a pending request.

### Answers to the open questions

1. **What the build did before.** The code notes say only that a dash during hit-stun "is handled as before (unspecified)". They do not say whether it was ignored, buffered or fired. I cannot claim an observed prior behavior, and none is claimed here. After this change, the behavior is the one above for both dash and attack: ignored, nothing fires during hit-stun or at its end.
2. **Latest build.** `sim/repo-notes.md` is headed "build 0.3.1" and `sim/build-0.4.md` is headed "Simulated build 0.3.1". These agree, and the packet shows no later build. The file name "0.4" and the heading "0.3.1" still disagree. The Studio should confirm the naming. The simulator will update `sim/` from this change, so QA should be given the updated build file.
3. **Code-side values.** The code notes (`sim/repo-notes.md`) contain none of the following unless noted.

| Item | Value |
|---|---|
| Grub speed | not in the code notes (design: "walks straight at the player") |
| Player speed | not in the code notes |
| Projectile speed | not in the code notes (design and build: "slow") |
| Projectile range | not in the code notes |
| Hearts (player maximum) | not in the code notes (design: a hit costs 1 heart) |
| Room size in tiles | not in the code notes |
| Grub hitbox size | not in the code notes |
| Player hitbox size | not in the code notes (the player's attack is a short arc hitbox in front of the player; no size is given) |
| Spawn effect or spawner | not in the code notes |
| Flinch | In the shared enemy controller, which has the states Idle, Chase and Attack. An enemy hit by the player enters a 0.2 s Flinch state that interrupts whatever it is doing, including Attack, then returns to Chase. It is per-controller, not per-type. |

   Design values for reference (from `design/combat.md`, not code facts): dash 4 tiles over 0.25 s, cooldown 0.6 s, Grub HP 2, Spitter HP 2, Spitter fires every 2 s. Someone with access to the real code or data files will have to supply the missing numbers.

4. **Flicker or sound cues.** The code notes state that none are described for invulnerability, and none exist for hit or dash invulnerability as far as the notes show. None are added in this step. QA should record cues as "none described, not checked". Whether any are wanted is a design or art question. It is not part of D-003 or the criteria.

## Decisions already made

- D-001: one attack button plus dash. No new input.
- D-003: input during hit-stun is ignored, not buffered. Hit and dash invulnerability are independent timers.
- D-004: timestamps on the accumulated game clock, not frame counts. Phase 1 waits for this fix to pass verification.

## Constraints

- Scope is hit-stun input only. No Phase 1 work.
- Correct at 30 and 60 FPS.
- No new input.
- The simulator needs to update `sim/` from the change above before QA verifies.

## Open questions

- For Studio: confirm that the build named 0.4 and headed 0.3.1 is one build, and that the updated build file is what QA receives.
- For Studio, `technical-director` and `art-director`: the missing values in answer 3 are "not in the code notes". They cannot be obtained from this packet.
- Not blocking: hold-through behavior (change 3) follows from "ignored, not buffered". If the designer wants held buttons to fire at the end of hit-stun, that is a different rule and needs a decision.

## Expected output

Studio composes a verification Handoff for `qa` containing the Change, the exercise steps, the criteria addressed, and the updated build description. It must not include the Sender assessment. QA returns pass or fail.

## Sender assessment

- I could not observe the prior behavior, so I did not try to describe it. The spec (D-003) is unambiguous, so implementing "ignore" is within the spec and is not a design choice. The edge-triggered, hold-through detail follows from "not buffered". Nothing fires "at the end of hit-stun" in either reading of D-003, and I have flagged it as a possible clarification.
- Root cause of the unobservability: the old input path had no explicit hit-stun gate in the notes, so the behavior was an accident of the code path. The timestamp gate makes it explicit and testable.
- Risk: low. The change adds a guard and one timestamp and touches no invulnerability logic. The one-frame boundary difference at 0.3 s is the same kind as the existing edges.
- Confidence: high that the stated behavior matches D-003. Moderate that the nominal exercise steps cover pad players, because held-button behavior depends on how the real input layer reports edges.
- Escalation: this is the second `question` for hit-stun observability, but it is now answered. If QA hands back for the same missing observation again, the Studio escalates to the Owner.

## Load

- Role: studio/roles/qa.md
- Skills: none
- Project: design/combat.md; project.md#constraints; sim/build-0.4.md; goals/G-001-combat-monotony/05-qa-to-studio.md (acceptance criteria)
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-003-input-during-hit-stun.md
- Previous handoff: goals/G-001-combat-monotony/18-studio-to-gameplay-engineer.md
>>>END

<<<FILE goals/G-001-combat-monotony/21-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 21
from: qa
to: studio
stage: Verify
outcome: question
---
# 21: qa → studio — Verification of the dash/hit invulnerability fix in build 0.4: no verdict yet, because dash-during-hit-stun (D-003) cannot be observed

## Task

Get the build description for dash and attack presses during hit-stun brought in line with D-003, then re-route to QA for a final verdict. Everything else the build describes meets the acceptance criteria. I cannot give `pass` while one part of criteria 2 and 5 is unobservable. I am not giving `fail` either, because nothing observed contradicts the spec.

## Context

Goal G-001 (combat monotony). Handoff 10 was blocked because no build was in the packet. This time `sim/build-0.4.md` (latest) and `sim/build-0.3.md` (baseline) were supplied. I verified from those two files, `design/combat.md`, D-001, D-003 and the criteria in `05-qa-to-studio.md`.

## Findings

### Nature of the evidence

Both builds are player-observable descriptions. There are no recordings or logs, and no per-run counts. My evidence is what `sim/build-0.4.md` states, quoted below. I did not use the "why it works" explanation in handoff 12.

- The 0.4 file's heading says "build 0.3.1", but the file is `build-0.4.md`. I treated it as the latest build, as the handoff says.
- `build-0.3.md` states only "Occasionally, if you dash right after being hit, you take damage partway through the dash." It gives no timings. The baseline comparison is therefore qualitative: 0.3 had the defect, and 0.4 states the following.
  - It gives no damage during the dash, for every start time after hit-stun.
  - Protection lasts to at least 0.8 s after the hit.

### Per-criterion results

The 0.4 description states that behavior is the same at 30 and 60 FPS, except for the exact frame at which an edge lands. It gives no separate per-frame-rate observations, so the 30 and 60 columns carry the same evidence.

| # | Criterion | 30 FPS | 60 FPS | Evidence (0.4) |
|---|---|---|---|---|
| 1 | Earliest dash (~0.3 s after hit): no damage in the 0.25 s dash; 20+ repeats; Grub and Spitter | consistent with pass | consistent with pass | "Dash started between 0.3 s and 0.55 s after a hit: no damage during the dash, and none after the dash ends. You stay protected until 0.8 s after the hit." "Holds for Grub contact and Spitter projectiles alike." Repeat count of 20: not demonstrable from a description. |
| 2 | Varied delays, including hit-stun, just before, at and after 0.8 s: no damage in an active dash | **part unobservable** | **part unobservable** | 0.3–0.55 s and 0.55–<0.8 s: no damage mid-dash ("Damage cannot land partway through the dash"). At or after 0.8 s: "the dash gives its own 0.25 s of protection." Dash pressed during hit-stun: "behaves as it did in 0.3." `build-0.3.md` does not describe that case, so it is unobservable (see Gap below). |
| 3 | Directions (towards and away), rooms 1–5, Grubs and Spitters | consistent with pass | consistent with pass | "Holds for Grub contact and Spitter projectiles alike, and for dashes toward or away from the damage source." Rooms 1–5 are not named per case; the build says there are "no other changes to enemies, rooms or attacks." |
| 4 | Dash with no preceding hit: full 0.25 s invulnerability | pass | pass | "you cannot be damaged for the full 0.25 s of the dash. Damage can land immediately after it ends." |
| 5 | Existing rules: hit-stun 0.3 s no input, hit invulnerability to 0.8 s, cooldown 0.6 s, attack queued in dash fires at end | **hit-stun input part unobservable**; rest pass | same | "Stunned with no input for the first 0.3 s"; "cannot be damaged for 0.8 s after the hit"; "0.6 s dash cooldown are unchanged"; "An attack pressed during a dash still fires when the dash ends." The build does not state whether a dash or attack press during hit-stun is ignored (D-003) or buffered. |
| 6 | Mid-dash damage is not deferred to just after the dash; damage after the windows is normal | consistent with pass | consistent with pass | Protection continues after the dash to 0.8 s after the hit, and damage "can land again" only after that. Nothing describes damage being stored and released. This is thin evidence. A real run should confirm that nothing lands in the frame after the dash ends. |

### Boundary results (frame length in view)

- Dash end at 0.25 s: a damage event exactly on 0.25 s counts as after protection.
- Hit protection end at 0.8 s: a damage event exactly on 0.8 s counts as after protection.
- A dash pressed at 0.8 s or later gets its own full 0.25 s.
- Frame length is about 33 ms at 30 FPS and about 17 ms at 60 FPS. Per the build, an edge event can differ by one frame between the two rates.
- That is at most about 33 ms at 30 FPS and about 17 ms at 60 FPS. Nothing in the description shows a difference larger than one frame, and nothing is hidden by the tolerance.
- The description gives no measured timestamps at 0.79, 0.8 or 0.85 s, only the rules above. Those are the rules I checked against.

### Regressions checked

- Dash distance, duration and cooldown: unchanged per the build.
- Attack queued during a dash: unchanged per the build.
- Enemies, rooms and attacks: unchanged per the build.
- Flicker and sound cues: the build does not describe them, so they are not verified.

### Gap (blocking the verdict)

`design/combat.md` and D-003 are clear: input during hit-stun, dash and attack alike, is ignored, not buffered. `sim/build-0.4.md` says only that a dash pressed during hit-stun "behaves as it did in 0.3." `sim/build-0.3.md` does not describe that behavior. So the build offers no observation that it is ignored. Inferring it from "stunned with no input" would be inference from intent, which my instructions rule out. The expected behavior is not a spec gap. The gap is in what the build shows.

Nothing observed contradicts any criterion, so I record no failure.

## Decisions already made

- D-001: Combat uses one attack button plus dash. No new input.
- D-003: Input during hit-stun is ignored, not buffered. Hit and dash invulnerability are independent timers.

## Constraints

- Verify from the spec, criteria and build. Do not change the spec or the build.
- Must be verified at both 30 and 60 FPS.
- Do not count the fix as verified until the hit-stun input behavior is observable.

## Open questions

1. Please get `sim/build-0.4.md` (or its successor) to state the observable behavior for a dash press and an attack press during the 0.3 s hit-stun. D-003 expects that the press does nothing, does not fire at the end of hit-stun, and does not start the dash. The requested wording should cover both the dash and the attack.
2. Optional, for a fuller verdict: observed per-frame-rate results at 30 and 60 FPS for the 20 repeats in criterion 1, and a statement of what happens in the frame right after a dash ends while a damage source is still in contact (criterion 6).

## Expected output

Studio asks `gameplay-engineer` to update the build description with the hit-stun input behavior (open question 1). Studio then re-routes to `qa`, with the new build and this handoff in the Load. QA will then return `pass` or `fail`. If everything else holds and the hit-stun behavior is ignored, the verdict will be `pass`. If a press during hit-stun is buffered or starts a dash, the verdict will be `fail` against D-003 and the criteria.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md; project.md#constraints; sim/build-0.4.md; sim/build-0.3.md; goals/G-001-combat-monotony/05-qa-to-studio.md
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-003-input-during-hit-stun.md
- Previous handoff: goals/G-001-combat-monotony/12-studio-to-qa.md
>>>END

<<<FILE goals/G-001-combat-monotony/22-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 22
from: game-designer
to: studio
stage: Route
outcome: done
---
# 22: game-designer → studio — Phase 2 spec adjusted; route Phase 2 Build and ask the Art Director to realign the lunge committed stage

## Task

Route the Phase 2 Build (task list in handoff 16, after Phase 1) using the adjusted spec. **First ask `art-director` to realign the Lunge Grub committed-stage visual and check A5**, because the dash window changed. Phase 1 is untouched.

## Context

Handoff 19 asked me to answer the four Phase 2 spec questions from handoffs 16 and 17, point the spec at `design/g001-telegraph-visuals.md` and say whether the acceptance criteria need new checks. The adjusted spec is `design/g001-combat-escalation.md` (section 4 and criteria 2, 4, 5, 7–9). The decision is D-005.

## Findings

Answers (details in spec 4.1–4.6):

1. **Flinch.** Lunge Grub: flinch-immune in Wind-up, Lunge and Recovery. Hits still do damage but never interrupt, delay or shorten anything. A hit during Recovery is ignored for timing, so the 0.8 s punish window stays (2 swipes = 0.7 s fit). In Chase it keeps the existing 0.2 s Flinch. Fan Spitter: flinch-immune in all states. A kill cancels the action at once. Phase 1 Grub and Spitter keep the existing Flinch (now documented as spec 5.3).
2. **Contact damage.** Lunge Grub damages only through the lunge (one hit per lunge; the first overlap uses it up, even if the player is invulnerable then, so no second hit after a dash ends). No damage in Wind-up or Recovery. In Chase the trigger (≤3.5 tiles) wins over a bite.
3. **Dash window.** Corrected to the real timing, with no change to lunge or dash timing. A dash covers the hit if `tc − 0.25 < td ≤ tc` (about 0.25 s, 7 frames at 30 FPS, ending at contact). A dash started at lunge start or later (up to contact) always covers it at any trigger distance. Where the early part opens (about 0.35–0.56 s) depends on distance and hitbox sizes: **confirm after the report** (handoff 18). Tuning knobs are listed in 4.3 (first: lunge 0.4 s).
4. **Fan Spitter confirmed** over the repositioning Spitter. Cycle is fire-to-fire 3.0 s (charge starts 2.4 s after the previous shot). First shot is no sooner than 1.0 s after appearing.
5. **The dash window changed, so a visual realignment is needed** (4.6). The 0.35 s committed stage ("chevrons solid = dash now") is wrong, because a dash started at 0.35 s ends at 0.60 s and covers nothing. Requests to the Art Director: committed stage starts at **0.45 s** (confirm after the report) and runs to lunge start at 0.60 s; the lunge-start flash is part of the cue; restate A5 (dash at lunge start always avoids the hit; a dash at committed-stage start avoids it only for close contact). No other visual timing changes. Fan Spitter visuals stand as written.

Acceptance criteria: new checks are needed and added.
- Criterion 2 (P2 part) is rewritten as a deterministic, contact-relative check at 30 and 60 FPS.
- Criterion 4 now includes A1–A12 (A5 restated) and the no-damage-in-Wind-up/Recovery rule.
- Criterion 5 includes lunge, recovery, fan fire time and the dash-window outcome.
- New criterion 7: flinch immunity (hits do damage, never interrupt; kills cancel at once).
- New criterion 8: Lunge Grub damage only through the lunge, one hit per lunge.
- New criterion 9: Phase 2 enemies recognisable at rest and the late-dash cue learnable (A5, A9, A12).

No variant is dropped, so both visual sections stay.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- D-002: B then A, C in reserve; 5 rooms and 15–20 min runs stay.
- D-003: input during hit-stun is ignored, not buffered.
- D-004: time-parametrized, sub-stepped lunge hit check; Fan Spitter; Phase 1 as one serial Build.
- D-005 (new): Phase 2 flinch immunity, damage only through the lunge, dash window relative to contact.

## Constraints

- All timing frame-rate independent (30 and 60 FPS), on scheduled timestamps.
- Gameplay numbers stay data, not code constants (D-004).
- Phase 2 Build only after the Art Director's realignment and Build's report (handoff 18). The "confirm after the report" values in spec section 7 may need a small spec update after that.
- I did not specify art. Visuals belong to `design/g001-telegraph-visuals.md`.

## Open questions

- `art-director`: realign the committed stage and A5 (spec 4.6). Also decide the hit feedback for a flinch-immune enemy (it must be clear that a swipe landed even though the enemy does not react), and a hit-flash or sound is a visual call. This was not asked in 19, so I flag it here.
- `technical-director` (informational): the "first overlap uses up the lunge's single hit" rule is a small clarification of D-004's "at most one hit per lunge". Say so if it costs more than a flag in the sub-step loop.
- Build (handoff 18 report): hitbox radii, lunge hit width, speeds, projectile range, hearts, room size. I will re-check the dash-window figures when they arrive.
- Playtest after Phase 2: is 0.25 s too tight? Is the late-dash cue learnable? A described walkthrough cannot show this.
- `design/combat.md` still lacks the Flinch and the Phase 2 enemies. This should be updated when Phase 2 is built (not done in this step).

## Expected output

The Studio asks `art-director` for the visual realignment, then routes Phase 2 Build (flinch-immune flag, Fan Spitter, Lunge Grub with sub-stepping, room-table swaps) once Phase 1 and the report are in. QA verifies against criteria 2, 4, 5, 7–9.

## Sender assessment

Confidence is high in the flinch and contact rules (they follow directly from the telegraph and punish-window intent). Confidence is medium in the dash window: the 0.25 s width is inherent to the existing numbers, and whether it plays fairly needs the hitbox report and a playtest. No Owner or `game-director` escalation is needed. No scope, pillar or Owner Decision is affected.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/write-design-spec.md
- Project: design/g001-combat-escalation.md; design/g001-telegraph-visuals.md; project.md#art-direction; project.md#vision
- Decisions: decisions/D-004-phase-2-technical-approach.md; decisions/D-005-phase-2-flinch-contact-and-dash-window.md
- Previous handoff: goals/G-001-combat-monotony/22-game-designer-to-studio.md
>>>END
