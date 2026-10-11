# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/15-qa-to-studio.md, goals/G-001-combat-monotony/16-technical-director-to-studio.md, goals/G-001-combat-monotony/17-art-director-to-studio.md
next_seq: 18
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/15-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/16-technical-director-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/17-art-director-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 18
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
goals/G-001-combat-monotony/goal.md
project.md
sim/build-0.3.md
sim/build-0.4.md
sim/repo-notes.md
>>>END

<<<FILE @decision-titles
decisions/D-001-one-button-combat.md — D-001: Combat uses one attack button plus dash
decisions/D-002-combat-variety-direction.md — D-002: Fix combat monotony with encounter escalation first, then enemy behaviors that demand movement and the dash
decisions/D-003-input-during-hit-stun.md — D-003: Input during hit-stun is ignored, not buffered
decisions/D-004-phase-2-technical-approach.md — D-004: Time-parametrized, sub-stepped lunge hit check; Fan Spitter over the repositioning Spitter; Phase 1 as one serial Build
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
- Design: is the intended behavior specified well enough to build? Not for the chosen direction. Done for Phase 1 and as proposals for Phase 2 (handoff 11, `design/g001-combat-escalation.md`).
- Plan: needed for Phase 2 (feasibility of new enemy behaviors, cost for a small team). Phase 1 is data/tuning; a Plan for it stays tentative (the technical-director is asked in handoff 13 whether it is needed).
- Build: the dash-damage defect fix (done, handoff 08), then Phase 1 and Phase 2 of the chosen direction.
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
| 4a | Verify (dash-damage fix) | qa | verify-change | open (attempt 2; attempt 1 blocked, build not in packet) | [12-studio-to-qa.md](12-studio-to-qa.md) (first attempt: [09-studio-to-qa.md](09-studio-to-qa.md) → [10-qa-to-studio.md](10-qa-to-studio.md)) |
| 4b | Design (Phase 1 in full; Phase 2 as proposed behaviors) | game-designer | write-design-spec | done | [07-game-director-to-game-designer.md](07-game-director-to-game-designer.md) → [11-game-designer-to-studio.md](11-game-designer-to-studio.md) |
| 5a | Plan (Phase 2 feasibility and cost) | technical-director | technical-plan | open (parallel with 4a, 5b) | [13-studio-to-technical-director.md](13-studio-to-technical-director.md) |
| 5b | Design (spawn marker and Phase 2 telegraph visuals) | art-director | write-design-spec | open (parallel with 4a, 5a) | [14-studio-to-art-director.md](14-studio-to-art-director.md) |
| 5c | Design (adjust Phase 2 spec from 5a and 5b answers) | game-designer | write-design-spec | planned (after 5a and 5b) | — |
| 6 | Build (Phase 1: encounter escalation) | gameplay-engineer | implement-change | planned (after 4a pass; Plan for Phase 1 only if 5a says it is cross-system or risky; Build reports Grub, player and projectile speed, heart count, room size; uses 5b's marker answer) | — |
| 7 | Verify (Phase 1) | qa | verify-change | planned (after 6) | — |
| 8 | Play (Phase 1) | playtester | playtest-session | planned (after 7; fresh Handoff without implementation history; record real-time run length and per-room clear time) | — |
| 9 | Build (Phase 2: behavior variants) | gameplay-engineer | implement-change | tentative (after 5c, if 5a and 5b find Phase 2 feasible and readable) | — |
| 10a | Verify (Phase 2) | qa | verify-change | tentative (after 9) | — |
| 10b | Verify (Phase 2 visuals, telegraphs) | art-director | visual-review | tentative (after 9; parallel with 10a) | — |
| 11 | Play (Phase 2) | playtester | playtest-session | tentative (after 10) | — |
| 12 | Review | game-director | review-outcome | planned | — |

Status: planned | tentative | open | done | skipped.

## Route changes

- After step 1 (Observe, playtester): the report matches the plan on the experience side (monotony confirmed: one winning approach in every room, little pressure to move, dash unused in combat), so Diagnose followed as planned. It also contained a possible defect (damage during a dash after being hit). Per the return rule "Play/Observe: defect → Observe (`qa`)", step 2b was added as a parallel step. Handoff 02 was edited in place (still from `playtester`) to add the Owner's report, mark the dash-defect item as routed to `qa`, and fill in Load and Expected output.
- After steps 2a and 2b: 2a produced a diagnosis with three options of different scope and cost (handoff 04), so Decide (`game-director`) followed. 2b confirmed a defect against specified behavior (handoff 05), so Build and Verify for the fix joined the route; no Design is needed because `design/combat.md` already specifies the behavior. QA's non-blocking question (how to treat a dash pressed during hit-stun) was left for `game-designer`.
- After steps 3a and 3b: 3a chose B then A with C in reserve (D-002, handoff 07); no escalation trigger fires, since everything stays within D-001 and the pillars. 3b delivered the invulnerability fix (handoff 08), which must be verified independently. Verify of the fix (4a) and Design of the chosen direction (4b) are independent, so they ran as one parallel group. Handoff 09 for QA was composed by the Studio without the engineer's Sender assessment or root-cause reasoning. Phase 1 Build (6) waits for 4a so it does not stack on an unverified fix. Phase 2 build, verify and play were kept tentative.
- After steps 4a (attempt 1) and 4b: 4a came back as `question` (handoff 10): QA had no build file in its packet, so nothing was verified. This is the first such hand-back for this input and the cause was a missing Load entry, not a Role problem, so 4a is re-opened with handoff 12, which names `sim/build-0.4.md` (latest) and `sim/build-0.3.md` (baseline) explicitly. The fix does not count as verified until QA reports `pass`. If the build still cannot be observed, the next hand-back for the same input goes to the Owner. 4b is done (handoff 11): Phase 1 is build-ready, Phase 2 is proposed. Designer's spec clarifications (independent hit and dash invulnerability timers, D-003 on hit-stun input, room enemy range 3–7) do not change the specified behavior QA verifies. Per the Designer's request, Phase 2 goes to `technical-director` (5a, handoff 13) and `art-director` (5b, handoff 14), opened in parallel with 4a because none consumes another's output. The art-director is also asked about the Phase 1 spawn marker, since Phase 1 Build needs it. A step 5c was added so the designer adjusts the Phase 2 spec from both answers before any Phase 2 Build (the designer asked for this in handoff 11). Phase 1 Build (6) stays gated on 4a pass; no Phase 1 Plan unless 5a calls for one. The reviews' answers are addressed to `studio` so the Studio can wait for both before routing to the designer.

## Next action

Three steps are open in parallel (4a, 5a, 5b). Run Route after each (or after all):
- 4a: `qa` verifies the dash/hit invulnerability fix from `12-studio-to-qa.md` (skill `verify-change`) at 30 and 60 FPS, and returns pass/fail to `studio`.
- 5a: `technical-director` assesses Phase 2 feasibility and cost from `13-studio-to-technical-director.md` (skill `technical-plan`), result to `studio`.
- 5b: `art-director` specifies the spawn marker and Phase 2 telegraph visuals from `14-studio-to-art-director.md` (skill `write-design-spec`), result to `studio`.

After 4a: on pass, open Build of Phase 1 (6) for `gameplay-engineer` (incorporating 5b's marker answer if available); on fail, return to Build with the failure report (a second failure of the same criterion goes to `technical-director`); on a second `question` for the same missing build, escalate to the Owner. After 5a and 5b both: route to `game-designer` (5c) to adjust the Phase 2 spec, or to `game-director` if either finds Phase 2 conflicts with scope or the pillars.

## Outcome

(To be filled at close, in Japanese.)
>>>END

<<<FILE goals/G-001-combat-monotony/15-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 15
from: qa
to: studio
stage: Verify
outcome: question
---
# 15: qa → studio — Dash/hit invulnerability fix: build 0.4 matches most criteria, but dash-in-hit-stun cannot be judged, so no pass

## Task

Route a request to `gameplay-engineer` (via Studio) to make the hit-stun dash behavior in `sim/build-0.4.md` observable and consistent with D-003. Then re-route verification to QA. This step gives no `pass` or `fail`, because one required case cannot be judged from the build.

## Context

Goal G-001 (combat monotony). Handoff 12 asked QA to verify the fix against the six criteria in `05-qa-to-studio.md` at 30 and 60 FPS. This time the build files were supplied (`sim/build-0.4.md`, baseline `sim/build-0.3.md`). The handoff says criterion 2 and 5 must cover a dash pressed during hit-stun, now specified by D-003 as ignored.

## Findings

### Verdict

No verdict. **Blocked on one case.** Nothing observed fails. A `pass` requires every criterion to pass, and one cannot be judged.

### The blocker

`sim/build-0.4.md` says only this about a dash pressed during hit-stun: "behaves as it did in 0.3." `sim/build-0.3.md` does not describe that behavior either. So neither build states whether the press is ignored, buffered or something else. D-003 requires "ignored, not buffered", and the build gives no observation to compare with it. Inferring "ignored" from "same as 0.3" would be inventing evidence. The spec is defined, so this is not a spec gap for `game-designer`. It is a build-observability gap.

### Other limits of the evidence

- The build files are player-observable prose, not run data. They give no repeat counts (criterion 1 needs at least 20 per frame rate) and no measured boundary results. They do not list rooms 1–5 individually. I cannot record "20 of 20 clean" or measured 0.8 s / 0.85 s results with the frame lengths (about 33 ms and 17 ms) in view. I can only compare what the description states against the criteria.
- `sim/build-0.4.md` has the heading "Simulated build 0.3.1". Its file name is 0.4. I assume they are the same build, but please confirm.

### Per-criterion comparison with `sim/build-0.4.md`

The build says its behavior is the same at 30 and 60 FPS, apart from which frame an edge lands on. The 30 and 60 FPS columns are therefore identical, and neither is an independently observed run.

| # | Criterion | 30 FPS | 60 FPS | Evidence (build 0.4 text) |
|---|---|---|---|---|
| 1 | Earliest dash (~0.3 s after hit): no damage in the 0.25 s dash, ≥20 repeats, Grub and Spitter | consistent; repeats not demonstrated | consistent; repeats not demonstrated | "Dash started between 0.3 s and 0.55 s after a hit: no damage during the dash, and none after… until 0.8 s"; holds for "Grub contact and Spitter projectiles alike". 0.3 had "Occasionally… you take damage partway through the dash"; 0.4 has no such line. |
| 2 | Varied delays: in hit-stun, just before, at and after 0.8 s | **not judgeable for hit-stun**; the other delays are consistent | **not judgeable for hit-stun**; the other delays are consistent | 0.3–0.55 s, 0.55–<0.8 s and ≥0.8 s are each described with no damage during the dash. The hit-stun press is "as it did in 0.3", which is not described. Boundary: a hit exactly on 0.8 s or 0.25 s counts as after protection, and "can differ by one frame". |
| 3 | Directions, rooms 1–5, Grubs and Spitters | consistent; per-room runs not shown | consistent; per-room runs not shown | "toward or away from the damage source"; Grub and Spitter named. Rooms are not mentioned in the dash text, and there are no other room changes. |
| 4 | Dash with no hit: full 0.25 s protection | consistent | consistent | "you cannot be damaged for the full 0.25 s of the dash. Damage can land immediately after it ends." |
| 5 | Existing rules: hit-stun 0.3 s with no input, hit invulnerability to 0.8 s, cooldown 0.6 s, attack queued in a dash fires at its end | partly consistent; hit-stun dash press not judgeable | partly consistent; hit-stun dash press not judgeable | Hit-stun 0.3 s with no input and protection to 0.8 s: stated. Cooldown "unchanged" at 0.6 s. Queued attack "still fires when the dash ends". The hit-stun press is undescribed (see blocker). |
| 6 | Mid-dash damage not delayed to land right after the dash; later damage normal | consistent; not observed directly | consistent; not observed directly | "Damage cannot land partway through the dash." After protection ends, damage lands normally. The text says nothing about damage being held or delayed. |

### Independence of the timers

This matches the `design/combat.md` clarification and D-003. 0.4 gives protection through the later of the dash end and 0.8 s after the hit. A dash ending does not cut short remaining hit protection. In 0.3 a quick dash after a hit could end that protection early. The 0.4 text says this no longer happens, and I found no contradiction with the spec.

### Regressions checked (description level only)

- Dash distance, duration and cooldown: unchanged.
- Enemies, rooms and attacks: "No other changes".
- Flicker and sound cues: **not checked**. The build text does not mention them.

### Undefined behavior and gaps

- The hit-stun dash press is unobserved in both builds (see blocker). The spec itself is defined by D-003.
- The one-frame difference at the 0.8 s and 0.25 s boundaries is stated, but not measured. A difference of more than one frame would be a failure, and it cannot be ruled out from prose.

### Plan once the case is observable

1. Press dash at several delays inside the 0.3 s hit-stun. Confirm that nothing fires then or when hit-stun ends (ignored, not buffered, per D-003). Also test an attack press. Do this at 30 and 60 FPS.
2. Run the matrix from handoff 10: dash delays of 0.3, 0.4, 0.5, 0.55, 0.6, 0.7, 0.79, 0.8 and 0.85 s. Keep a damage source present throughout. Record where damage lands: during the dash, between the dash end and 0.8 s, or after 0.8 s.
3. Repeat the earliest-dash case at least 20 times per frame rate.
4. Cover the no-hit dash, both directions, rooms 1–5 and both enemy types.
5. Record the boundary results at 0.8 s and 0.85 s at both frame rates.
6. Check the cooldown, queued attack and flicker/sound cues.

## Decisions already made

- D-001: Combat uses one attack button plus dash.
- D-003: Input during hit-stun is ignored, not buffered. Hit and dash invulnerability are independent timers.

## Constraints

- Verify from `design/combat.md`, the acceptance criteria and the build. Do not change the spec or the build.
- Must be verified at both 30 and 60 FPS.
- Do not count the fix as verified until the open case is observed.

## Open questions

- For Studio and `gameplay-engineer`: state in the build, in observable terms, what happens when dash or attack is pressed during hit-stun. D-003 requires that it is ignored and not buffered. If the build does something else, that is a failure to route back.
- For Studio: confirm that `sim/build-0.4.md` (heading "0.3.1") is the intended latest build.
- For Studio: if observed run data (repeat counts, boundary timings) can be supplied, include it. If the dry run can only offer prose, say so, and QA will judge the other criteria on the prose with that limit recorded.

## Expected output

Studio routes the open case to `gameplay-engineer` for an observable statement, then re-routes to `qa` with the updated build file. QA returns a `pass` or `fail` verification report. If the case cannot be made observable, Studio should not count the fix as verified.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: none
- Project: design/combat.md; project.md#constraints; sim/build-0.4.md; sim/build-0.3.md
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-003-input-during-hit-stun.md
- Previous handoff: goals/G-001-combat-monotony/12-studio-to-qa.md
>>>END

<<<FILE goals/G-001-combat-monotony/16-technical-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 16
from: technical-director
to: studio
stage: Route
outcome: done
---
# 16: technical-director → studio — Phase 2 is feasible and cheap; Phase 1 needs no separate Plan gate; four spec questions go to the game-designer

## Task

Pass this assessment on with the art-director's answer to `game-designer`. Phase 1 may go to Build now with the plan in "Findings". Phase 2 stays blocked until the designer has answered the questions in "Open questions" and the art-director has given the telegraph direction.

## Context

Handoff 13 asked whether the Lunge Grub and Fan Spitter can be built cheaply by a small team on existing systems, which to drop if cost is high, whether Phase 1 needs a Plan, and which values are already in code. I worked from `design/g001-combat-escalation.md`, `design/combat.md`, `sim/repo-notes.md` and D-001..D-003. The technical choices are recorded in D-004.

## Findings

### Verdict
- **Both Phase 2 behaviors are feasible within constraints, with no new input and no pillar change. Neither needs to be dropped for cost.**
- The shared enemy controller (Idle / Chase / Attack, per-type data plus a small per-type attack routine) fits both.
- **Fan Spitter: cheapest.**
  - It reuses the Spitter routine and projectile.
  - The new parts are a 0.6 s charge, an aim lock, three projectiles at −25° / 0° / +25°, and a 3 s cycle (mostly data).
  - Cost: small.
- **Lunge Grub: small to medium.**
  - It needs a per-type routine with wind-up, lunge and recovery, plus a direction lock.
  - It needs a path-swept hit check (below).
  - It needs a per-state flinch exemption (see the critical finding).
  - Cost: small to medium.
- **Repositioning Spitter: rejected on cost.** The designer left the choice to me. It needs wall-position selection, movement and pathing, and it interacts with the Phase 1 placement rules. See D-004.
- If something must be cut later, that is a design-value call for the designer. It would not be a cost call. The Lunge Grub carries the "dash has a purpose" goal, and the Fan Spitter is the cheaper add-on.
- The unknown art cost of the telegraphs is the main open cost. It is with the art-director.

### Critical finding: the existing Flinch conflicts with the Phase 2 spec
`sim/repo-notes.md`: a player hit puts an enemy in a 0.2 s **Flinch** that interrupts whatever it is doing, including Attack, then returns it to Chase. `combat.md` does not describe this.

- The spec (4.1) says damage does not interrupt wind-up or lunge, and puts stagger out of scope. As built, one swipe during wind-up would cancel the telegraph, and the Grub would re-enter Chase and wind up again. A player could reset a Lunge Grub indefinitely.
- Flinch during recovery would cut the 0.8 s punish window to about 0.2 s.
- The same applies to the Fan Spitter's 0.6 s charge. The spec is silent on whether a hit cancels it.
- Cheap fix (no new system): add a per-state "flinch-immune" flag that the Flinch entry checks. Phase 2 states set it.
- This is a player-facing choice, so the designer decides (Open questions 1 and 2).
- It also affects Phase 1 slightly, since existing Grubs and Spitters are interrupted by Flinch today. That is existing behavior and I am not changing it.

### Swept hit check for the lunge
The lunge covers 5 tiles in 0.3 s, which is about 16.7 tiles/s, or 0.56 tile per frame at 30 FPS and 0.28 at 60 FPS.

- **Position is a function of elapsed lunge time.** Use the lunge start timestamp on the accumulated game clock, not `velocity * dt` accumulation. The lunge distance is then identical at 30 and 60 FPS and clamps exactly at 5 tiles.
- **Sub-step along the path.** Each frame, advance the Grub in sub-steps of at most about 0.25 tile (or a fraction of the smaller hitbox radius, if that is smaller) with the existing wall-stop movement and the existing overlap and contact test. At each sub-step, call `isInvulnerable(t)` with the time at that sub-step.
- This reuses existing code and needs no new collision primitive. An analytic segment test is a possible alternative and I rejected it for now (D-004).
- Damage is dealt at most once per lunge.
- The lunge ends at a wall or after 5 tiles, as the spec says.
- Wind-up and lunge start on scheduled timestamps (wind-up start + 0.6 s), not on the frame that notices the expiry. The 30 FPS result then differs by at most 1 frame.

### Observation on the spec's dash window (for the designer, not changed by me)
Spec 4.1 says a dash started between wind-up 0.35 s and the lunge start (0.6 s) covers the lunge hit. As written, that does not hold.

- A dash started at 0.35 s ends at 0.60 s (invulnerability is 0.25 s), exactly when the lunge starts. It covers nothing.
- What counts is when contact happens. Contact is at about `0.6 s + (distance − combined hitbox radius) / 16.7`.
- A dash covers the hit if it starts within the 0.25 s before contact, and also not after it. So the real window is **about 0.25 s, about 7 frames at 30 FPS**. It is not wider than the dash.
- Where it sits depends on the distance and hitbox sizes. Those are not in the packet. For example, a net gap of 2.2 tiles puts contact at about 0.73 s and the window at about 0.48–0.73 s.
- A dash started at lunge start (0.6 s) covers any contact within 4.2 tiles, which includes everything the 3.5-tile trigger allows.
- The 4-tile dash also takes the player out of the locked line, which may matter more than the invulnerability. The 0.6 s dash cooldown also applies.
- The window is probably workable, and it may suit the intent, but the spec's description and the criterion 2 check ("dash starts within 0.6 s before a threat would hit") should be set against the real numbers. This is the designer's call (Open question 3).

### Phase 1: does it need a Plan?
- **No separate Plan gate and no isolated workspace.** Phase 1 can go to Build with the plan below. The risk is low to medium and concentrated in timing. There is no save data, nothing irreversible, and no cross-system risk beyond the spawner and the enemy controller.
- **Caveat on "data and tuning only".** The room table is data, but the 0.8 s marker, the 5-tile spawn-point selection, the wave trigger (≤1 alive or 8 s) and the Spitter's 1.0 s first-shot delay are logic. They need a small wave scheduler. I cannot tell from the packet whether the room system already supports waves, edges or spawn markers.
- Build's first task is to report that. If a spawner rework beyond a small scheduler is needed, hand it back to me. If it clearly exceeds what the Goal implies, I escalate to `game-director`.

**Phase 1 ordered tasks (serial, one Build):**
0. Report what is in the code: Grub speed, player speed, projectile speed, hearts, room size in tiles, whether a spawn effect or spawner exists, and what a dash or attack pressed during hit-stun does today (repo notes say "unspecified").
1. Make the dash and attack input ignored, not buffered, during hit-stun (D-003) if they are not already. Add tests.
2. Add the wave scheduler and spawn queue. The enemy object is not created during the marker (it must not exist, move or attack). All timers are timestamps on the accumulated game clock, like `isInvulnerable`.
3. Add the marker (reuse an existing effect, or a placeholder flagged for the art-director) and the spawn-point selection. This covers the 5-tile minimum distance, the same-edge fallback, then the farthest point, and being on screen.
4. Add the wave trigger (≤1 alive or 8 s from the previous wave's marker start).
5. Add the Spitter's first shot no sooner than 1.0 s after it appears, then the existing 2 s interval.
6. Enter the room tables (3.2) and the Spitter placements (3.4) as data.

**Phase 2 ordered tasks (after designer and art-director answers):** flinch-immune flag, then Fan Spitter, then Lunge Grub with sub-stepping, then room-table swaps (spec 4: room 3 gets 1 Lunge Grub, room 4 gets 2 Lunge Grubs and 1 Fan Spitter, room 5 gets 3 Lunge Grubs and 1 Fan Spitter).

### Risks and mitigations
- **Frame-rate dependence (all timers).** Use timestamps and elapsed-time functions, never frame counts or per-frame increments.
- **Tunneling at 30 FPS.** Sub-stepping, plus a unit test where the lunge crosses a thin target in one frame.
- **No enemy tests exist.** The only tests today are for `isInvulnerable`. A small headless enemy simulation on a fixed clock (1/30, 1/60, variable dt) is the main hidden cost and I count it in the estimate. Build should extend the existing test pattern.
- **Flinch interaction** (above).
- **Unmeasured numbers.** The spec's values are untested. Make them data (timings, ranges, angles, counts), not constants in code, so tuning needs no code change.
- **Projectile and effect limits.** The Fan Spitter spawns 3 projectiles per volley. Build should confirm there is no projectile pool limit.

### Test strategy
- **Automated** (simulated clock at 1/30, 1/60 and varying dt):
  - marker 0.8 s (nothing exists or damages before it ends);
  - minimum spawn distance and on-screen spawn;
  - wave trigger at 8 s and at ≤1 alive;
  - Spitter first shot ≥1.0 s;
  - D-003 input ignore in hit-stun;
  - lunge: direction lock, exact 5-tile distance, tunneling case, one hit per lunge, no damage while dash- or hit-invulnerable, and flinch immunity (once the designer decides);
  - Fan: aim lock at charge start, three angles;
  - timestamps matching within 1 frame at 30 FPS (±0.034 s), per criterion 5.
- **QA manually:** criteria 1, 3 and 4, the stationary-stance check, telegraph readability, and that the lunge reads clearly before it hurts.
- **Playtest:** real run time (criterion 6) and the feel of the dash window.

### Parallelization
**None.** Phase 1 tasks 2–5 share the spawner and the enemy controller, so they are not independent. Phase 2 also touches the same controller and room data, and it is blocked on reviews anyway. The Fan Spitter and Lunge Grub routines are separable, but the work is too small to be worth a second workspace and the merge risk on the shared flinch flag.

### Values already in code
`sim/repo-notes.md` does not contain Grub speed, player speed, projectile speed, hearts or room size, so I cannot report them from the packet. Build must report them in task 0. Two things are in the notes: the Flinch (0.2 s, interrupts, undocumented in `combat.md`) and the invulnerability timestamps (`hitInvulnUntil`, `dashInvulnUntil`, `isInvulnerable(now)`).

## Decisions already made

- D-001: one attack button plus dash; no new input.
- D-002: B then A, C in reserve; 5 rooms and 15–20 min runs stay.
- D-003: input during hit-stun is ignored, not buffered.
- D-004 (new, technical): time-parametrized, sub-stepped lunge hit check; Fan Spitter over the repositioning Spitter; Phase 1 as one serial Build with no separate Plan.

## Constraints

- Frame-rate independent at 30 and 60 FPS.
- Reuse existing systems. No new input and no pillar change; none of this needs either.
- I did not change the spec. The points below are proposals for the designer.

## Open questions

For `game-designer` (via the Studio):
1. **Flinch on Phase 2 enemies.** Should a player hit leave Lunge Grub wind-up and lunge uninterrupted, as spec 4.1 says? The default I will build is a flinch-immune flag set during wind-up, lunge and recovery. Should a hit during recovery be ignored, or should it end recovery early? Same question for the Fan Spitter charge.
2. **Contact damage by state.** Does a Lunge Grub bite on contact during recovery, when a lunge ends on top of the player? The default I propose is that damage happens only during the lunge and in normal Chase, not in wind-up or recovery.
3. **Dash window.** Correct spec 4.1's window text and the criterion 2 check to the real timing (about 0.25 s ending at contact), or change the lunge or dash timing so the intended window holds. Which do you want?
4. **Fan Spitter.** I chose the fan over the repositioning Spitter (D-004). Confirm.

For `art-director` (already routed): telegraph direction for the 0.6 s wind-up and 0.6 s charge, and whether a spawn effect exists for the marker.

For `playtest` and Build: report real run time and per-room clear time after Phase 1 (criterion 6).

## Expected output

The Studio waits for the art-director's answer, then routes both answers to `game-designer`. The designer adjusts the Phase 2 spec and hands it to the Studio for Build. Phase 1 can start Build now at task 0.

## Sender assessment

Confidence is high that both behaviors are cheap enough. The dominant risks are the undocumented Flinch and the missing enemy test harness, and both are controllable. Confidence in the lunge and dash window numbers is low until the hitbox sizes and speeds are known from Build's report. No Owner escalation is needed. No `game-director` escalation is needed unless Build finds that Phase 1 needs more than a small scheduler.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/g001-combat-escalation.md; design/combat.md; sim/repo-notes.md; project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-002-combat-variety-direction.md; decisions/D-003-input-during-hit-stun.md; decisions/D-004-phase-2-technical-approach.md
- Previous handoff: goals/G-001-combat-monotony/13-studio-to-technical-director.md
>>>END

<<<FILE goals/G-001-combat-monotony/17-art-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 17
from: art-director
to: studio
stage: Route
outcome: done
---
# 17: art-director → studio — Telegraph visual spec for the Phase 1 spawn marker and the Phase 2 Lunge Grub and Fan Spitter

## Task

Hold this answer until the technical-director's Phase 2 feasibility answer arrives, then route both to `game-designer`. The Phase 1 spawn-marker answer below can go to Build now.

## Context

Handoff 14 asked for the player-visible telegraphs for the 0.8 s spawn marker (Phase 1), the Lunge Grub 0.6 s wind-up and the Fan Spitter 0.6 s charge (Phase 2), plus whether an existing spawn effect can serve as the marker. The full spec is `design/g001-telegraph-visuals.md`.

## Findings

### Spawn marker (answer first, so Phase 1 is not blocked)
- **I cannot confirm whether an existing spawn effect exists.** The packet had no code-side description of effects. The spec gives a decision rule instead. Build checks the effects, and if one exists and passes acceptance checks A1–A5, it reuses it with only colour and timing tuned. Otherwise it builds the minimal marker: a flat orange-red ground ring that contracts from about 1.5 to 0.75 tiles over 0.8 s, brightest and solid for the last 0.2 s, with a short pop when the enemy appears (spec section 3).
- It is non-directional and not filled, so it cannot be mistaken for a hazard.
- Build must say in its handoff which case applied and name the effect.

### Lunge Grub (spec section 4)
- **The path is shown.** The telegraph is a strip along the locked direction, as long as the real lunge (5 tiles, shortened at a wall). It does not rotate after wind-up starts.
- 0–0.35 s: the strip fills outward from the Grub. 0.35–0.60 s: it is solid with chevrons. This committed stage lines up with the dash window in spec 4.1, so the learnable cue is "chevrons solid = dash now".
- Body cue: crouch away from the lane with a glowing crest. The strip is removed at lunge start. Recovery has a slumped pose and no strip.

### Fan Spitter (spec section 5)
- Three thin rays at −25°, 0° and +25° from the locked aim line, ending at walls, with the gaps left dark so the safe spaces read clearly. Rays are dashed and growing until 0.40 s, then solid until fire at 0.60 s. The Spitter's mouth ports light up.

### Distinguishability
- Shape separates the three: ring (spawn), wide strip with chevrons (lunge), thin rays (fan). Colour is never the only cue (greyscale test A7). The variants also get an identity at rest (crest on the Lunge Grub, fan of ports on the Fan Spitter), so the player sees the dangerous type before it telegraphs.
- The existing Grub bite and normal Spitter projectile do not use any of these shapes.

### Timings
- **No gameplay timing change is needed.** All three telegraphs already exceed the 0.5 s minimum. Sub-stage times (0.35 s, 0.4 s, 0.2 s) are visual only.
- Note for the designer: the lunge's 0.35 s committed-stage start is tied to the spec 4.1 dash window. If that window changes, change the visual to match.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- D-002: B then A, C in reserve. Phase 2 needs both the technical-director and art-director answers before Build.
- No new decision was recorded. The choices here are visual direction within the existing art direction, with no pillar change.

## Constraints

- Phase 2 must not be built before the technical-director has answered.
- All animation is a function of elapsed game time (30 and 60 FPS identical, ±1 frame at 30 FPS).
- Small team: the marker reuses an existing effect if one passes. The new fallback is a single minimal effect.

## Open questions

- Build: does an existing spawn effect exist, and does it pass A1–A5?
- Build: report lunge hit width, projectile range and Spitter mouth position, which size the strip and rays.
- Technical-director: cost of the identity-at-rest art (A9) and the telegraph rendering for each Phase 2 variant. If one variant is dropped, drop its visual section with it.
- Playtest after Phase 2: does the committed-stage cue let players dash on purpose? Is the room 5 crowd readable (A12)? A described walkthrough cannot show this.

## Expected output

Route the Phase 1 marker answer to Build now, and both answers (art and technical) to `game-designer` once the technical-director has answered. The designer then adjusts the Phase 2 spec to point at `design/g001-telegraph-visuals.md` and hands it back for Build. Review of the built visuals uses acceptance criteria A1–A12.

## Sender assessment

Confidence is high that the shape-and-stage language is readable and distinct. Confidence is medium on the exact sizes, colour values and 0.35 s cue timing, which need a look in the real dark-cave scene. The unknown about an existing spawn effect is real, so the decision rule above avoids guessing. No escalation trigger applies: no pillar change and no gameplay rule change.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/g001-telegraph-visuals.md; design/g001-combat-escalation.md; design/combat.md; project.md#art-direction; project.md#vision; project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-002-combat-variety-direction.md
- Previous handoff: goals/G-001-combat-monotony/14-studio-to-art-director.md
>>>END
