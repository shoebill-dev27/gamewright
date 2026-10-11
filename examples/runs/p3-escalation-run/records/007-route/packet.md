# Studio operation packet

operation: Route
goal: G-002
step_artifacts: goals/G-002-combat-monotony/08-technical-director-to-studio.md, goals/G-002-combat-monotony/09-art-director-to-studio.md
next_seq: 10
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-002-combat-monotony/goal.md
- goals/G-002-combat-monotony/08-technical-director-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-002-combat-monotony/09-art-director-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-002-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 10
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
| 6a | Plan | technical-director | technical-plan | open | 06-game-designer-to-technical-director.md |
| 6b | Design (visual cues) | art-director | write-design-spec | open | 07-studio-to-art-director.md |
| 7 | Build | gameplay-engineer | implement-change | planned | — |
| 8a | Verify | qa | verify-change | planned | — |
| 8b | Verify (visual) | art-director | visual-review | planned | — |
| 9 | Play | playtester | playtest-session | planned | — |
| 10 | Review | game-director | review-outcome | planned | — |

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

## Next action

Two steps are open in parallel:
- technical-director starts 6a (Plan) from `06-game-designer-to-technical-director.md`.
- art-director starts 6b (Design, visual cues) from `07-studio-to-art-director.md`.

Both address their results to `studio`; the Route operation waits for both before writing the Build Handoff.
Pending Studio item: add `design/combat-enemy-depth.md` to the Design index in `project.md` (not writable in this operation; do it in the next operation that can edit `project.md`).
When Build and Verify are routed, their Handoffs must ask for results addressed to `studio` (needed to compose the independent Playtester Handoff for step 9).

## Outcome

—
>>>END

<<<FILE goals/G-002-combat-monotony/08-technical-director-to-studio.md
---
kind: handoff
goal: G-002
seq: 8
from: technical-director
to: studio
stage: Plan
outcome: done
---
# 08: technical-director → studio — Technical plan for enemy-side combat depth (build 0.4)

## Task

Merge this plan with the Art Director's cue design (step 6b, `07-studio-to-art-director.md`) and write the Build Handoff. Pass the technical limits on cues (section "Cue system and limits for the Art Director") to the Art Director. Route the spec questions (SQ1–SQ5) to `game-designer` if the Studio's process requires an answer before Build. Each question has a default I will build to if no answer arrives, and Build must tell the reader which default it used.

## Context

G-002: the Owner chose enemy-side depth with one-button combat kept (D-002). The Game Designer wrote `design/combat-enemy-depth.md` and handed it to me (`06-game-designer-to-technical-director.md`) with Q2 (layout and attack cap) and Q3 (tuning easy to change). Q1 (visuals) belongs to the Art Director. I plan from the spec and `sim/repo-notes.md` only; I have not seen the room layout data or file names, and the dry-run Build must name systems, not paths I cannot confirm.

## Findings

### Answers to Q2 and Q3

**Q2a. Do rooms 2–5 need layout changes?** Probably light ones, but I cannot confirm this from the packet because it contains no room layout data.
- Room 1 (Grubs) and room 3 (Spitters + Shieldbearer) need no layout change for the new enemies. Room 3 benefits from one or two obstacles that serve as cover from Spitters, but this is optional.
- Rooms 2, 4 and 5 (Chargers) need a **layout audit** against these requirements. Expect small edits (add or move 2–4 obstacle or wall segments per room):
  1. From the Charger's likely positions there are at least two charge directions that end in a wall or solid within 8 tiles, so wall-stun is achievable.
  2. There is open floor beside the main lanes, so the player can sidestep a 1-tile-wide lane.
  3. There is no spot where a Charger permanently has no valid windup (edge case 5: it will not wind up toward a wall less than 1 tile away, so it repositions).
  4. Room 4 (2 Chargers) has lanes that can cross without covering the whole room, and room 5 stays readable with 6 enemies.
- Decision made for the plan: a charge ends at any static solid (wall or obstacle), not only walls. See SQ3.
- A Build step can make the layout edits only once the audit has the actual layout. Put the audit first in the Build slice for rooms (task T7).

**Q2b. Does the 2-attacker cap fit the existing controller?** Yes, at modest cost. The shared controller has Idle, Chase and Attack. I will not add a new top-level state per attack. I will do two things:
- Run a **phase machine inside Attack**: Telegraph → Active → Recovery (plus Stunned, Cooldown, and a Waiting behavior when no slot is free). The phases and durations are data per enemy type. The existing per-type attack routine supplies the effect (lunge, projectile, charge, bash).
- Add a single **attack-slot arbiter** per room: 2 slots, first-come-first-served. An enemy asks for a slot before it can start a telegraph. It holds the slot through Telegraph and Active, and releases it when Recovery starts, on death, or when the room ends. Spitter shots in flight hold no slot. D-003's revisit trigger ("cap cannot be built within the existing controller at reasonable cost") does **not** fire.

**Q3. Keep tuning easy to change.** Every number in the spec goes into one per-type enemy data table, in seconds, tiles, tiles/s and degrees. That covers windup, tracking and lock times, charge speed and range, stun, turn rate, guard arc, bash cone, cooldowns, HP, and slot count. Code reads the table and never contains literals. A loader validation rejects any telegraph under 0.4 s (the D-003 floor). Tests read expected values from the table, plus the fixed invariants (the 0.4 s floor and the cap of 2), so retuning does not break them.

### Technical findings that change the work

1. **Existing Flinch contradicts the spec (needs a design ruling, SQ1).** Today an enemy hit by the player enters a 0.2 s Flinch that interrupts any state including Attack. That is not in `design/combat.md`. If it stays:
   - A single swipe cancels every telegraph and the "stand still and swipe" tactic survives, which defeats the goal.
   - It breaks the Charger rule that swipes do not interrupt windup, charge or recovery.
   - It would shorten Shieldbearer and Grub recovery.
   Default I will build: Flinch applies only in Chase and Waiting. It is ignored during Telegraph, Active, Recovery, Stunned and Cooldown, for every enemy type. This is the Charger rule extended to all types.
2. **Invulnerability bug blocks the spec.** Invulnerability is one flag switched off by whichever timer ends first. The known build 0.3 symptom (damage partway through a dash right after being hit) is this bug. V4, section 2.4 and "dash invulnerability full 0.25 s" depend on it being fixed. Fix: replace the flag with an expiry time (`invulnerableUntil = max(existing, new)`), or a source counter. It is a Build prerequisite and has regression tests.
3. **Facing and blocking do not exist.** Damage today is overlap-only. Shieldbearer needs enemy facing and a damage call that carries hit origin and kind (swipe, projectile, charge, bash). The guard check goes in that one damage entry point so swipes and projectiles use the same rule.
4. **Variable delta time versus fast, short attacks.** Charge 12 tiles/s is 0.4 tiles per frame at 30 FPS, and a 0.1 s hitch gives 1.2 tiles. The Grub lunge is 2 tiles in 0.15 s. Without care, a 1-tile lane and the hit window can be skipped and outcomes will differ between 30 and 60 FPS. See D-004: bounded sub-stepping of the combat update, plus a per-frame time clamp.
5. **Dash and enemy collision.** The spec requires dash to pass through a Shieldbearer, and a charge to pass through other enemies. I need to check how the existing dash and steering handle enemy–enemy and player–enemy collision (not in the notes), and add collision exceptions: no enemy–enemy collision for a charging Charger, and no player–enemy collision during dash. Walls still stop both.
6. **No existing tests** for invulnerability or enemies. A small headless test harness is needed and counts as part of the cost.

### Work breakdown (ordered; "needs" lists dependencies)

| # | Task | Needs |
|---|---|---|
| T0.1 | Invulnerability fix (expiry-based) and tests: dash right after hit, hit during dash, hit-stun and dash overlap | none |
| T0.2 | Combat time: per-frame dt clamp 0.1 s; bounded sub-steps ≤ 1/120 s for player, enemies, projectiles; timers carry overshoot; pause freezes all timers (D-004) | none |
| T0.3 | Headless harness: simulated clock, scripted input, run any scenario at 30 FPS, 60 FPS and with injected hitches; reports phase times and damage events | T0.2 |
| T1 | Enemy phase machine inside Attack; data table for all spec values; Flinch rule (SQ1); cue events (below); pause and death cancel (edge 4) | T0.2 |
| T2 | Attack-slot arbiter (2 slots, FIFO, release rules) and Waiting behavior (keep distance/approach, do not attack) | T1 |
| T3 | Grub (stop at 1.5 tiles, 0.5 s telegraph, lunge 2 tiles in 0.15 s, 0.6 s recovery, no walking contact damage) and Spitter (0.6 s aim telegraph, tracks then locks 0.2 s before firing, 2 s interval) | T1, T2 |
| T4 | Enemy facing; damage entry point with hit origin and kind; guard-arc check; projectile-versus-guard | T1 |
| T5 | Charger (see below) | T1, T2, T3 style, collision exceptions |
| T6 | Shieldbearer (see below) | T4 |
| T7 | Layout audit and room composition data (rooms 1–5 per section 5); layout edits for rooms 2, 4, 5 | none for data; audit needs the layout |
| T8 | Cue hookup to the Art Director's design via the cue interface; placeholder cues first | T1 (placeholders), Art Director output (final) |
| T9 | Automated acceptance scenarios and QA checklist | all |

**Charger (T5):**
- The lane and the hit area are the same geometry: a 1-tile-wide box swept from the Charger along its locked direction until the first static solid or 8 tiles. Windup is 0.8 s: tracking 0.5 s, locked 0.3 s.
- Contact uses a swept test per sub-step, so it cannot tunnel.
- On a hit, it deals 1 damage and keeps going. A touch during invulnerability does nothing, is not "used up" and the charge keeps going. A touch that did damage is not repeated in the same charge.
- It ends at a solid (1.5 s stun with the stun cue) or after 8 tiles (0.8 s recovery). Then 1.0 s cooldown.
- Rules: swipes never interrupt it; it passes through enemies; death cancels immediately with no damage; edge case 5 reposition.

**Shieldbearer (T6):**
- Facing turns toward the player at ≤ 90°/s. Guard arc is 120°, so ±60° from facing.
- The guard check uses the angle from the Shieldbearer's facing to the attack origin: the player's position for a swipe, the projectile's position at impact for a shot.
- Guard is up in every phase except Recovery. Telegraph 0.6 s, with no turning from telegraph start until the end of recovery. The bash is a 1.5-tile cone over 0.1 s. Recovery is 0.8 s with guard down. Cooldown is 0.6 s.
- A bash starts only if the player is in the front 60° within 1.5 tiles and a slot is free.
- A blocked swipe emits the block event, which carries both visual and sound hooks.

### Cue system and limits for the Art Director

The cue system is separate from the combat logic, so the Art Director's visuals can be swapped with no logic change.

- **Interface.** Logic only emits events through a cue sink. It never reads anything back, and nothing in gameplay depends on cue timing or assets.
  - `TelegraphStart` carries enemy id, attack type, shape, total duration.
  - `TelegraphUpdate` carries shape (position and direction, which can change while tracking), progress 0–1, and a `locked` flag.
  - `TelegraphEnd` carries completed or cancelled.
  - There are also `BlockCue` (position, direction), `StunStart/End`, and `GuardDown` for the Shieldbearer's recovery.
- **Shapes.** Cone (origin, direction, radius, angle), lane/line (origin, direction, length, width), aim line (origin, direction, length). The shape is the real hit geometry. A cue may be drawn larger, but never smaller than the hit area.
- **Lane indicator.** The lane is 1 tile wide and up to 8 tiles long, with its length cut at the first solid. It updates every frame during the 0.5 s tracking phase and then holds still. The logic gives the final length each frame. A stretched sprite or quad is easy to support. Per-tile art is only possible if it tiles cleanly and can be cut at any length.
- **Lock moment.** The `locked` flag lets the cue change when tracking ends (Charger last 0.3 s, Spitter last 0.2 s, Grub direction at end of telegraph). Players need this to dodge fairly (V4).
- **Draw budget.** The cap bounds active telegraph cues to 2, counting Spitter aim lines. Add at most 2 stun cues (room 4 has 2 Chargers), the Shieldbearer guard-down cue, and short block cues. Draw cost is small, but the cues must be cheap sprites or quads, not full-screen effects or per-frame generated meshes.
- **Time-driven only.** Animation must be driven by the progress value or elapsed seconds, never by frame counts or fixed frame-per-frame sprite strips. Telegraphs are as short as 0.4 s, which is 12 frames at 30 FPS.
- **First frame.** The cue is shown from the first rendered frame after telegraph start. Any fade-in is the Art Director's call, but the telegraph timer does not wait for it. Preload cue assets so first use causes no hitch.
- **Layering.** Cues draw above the floor and below UI. They must stay readable with up to 6 enemies and Spitter projectiles on screen.

### Test strategy

**Automated (headless harness, T0.3, each scenario run at 30 FPS, 60 FPS and with a hitch):**
- Invulnerability regression: dash right after hit, hit during dash, expiry order.
- V1/V2: phase timings for Grub, Spitter, Charger and Shieldbearer within ±0.05 s; no damage before the telegraph has run fully.
- V3: walking Grub contact deals no damage; a lunge deals 1; a stationary player in a corner takes lunge damage.
- V4: leaving the lane in the final 0.3 s dodges; a dash over the contact moment dodges; standing in the lane takes 1.
- V5: wall hit gives a 1.5 s stun with 1 damage per swipe.
- V6/V7: front swipe deals 0, side or back swipe deals 1, shot blocked at front, front vulnerable for 0.8 s after a bash.
- V8: in room 5, a monitor asserts the count of enemies in Telegraph or Active is never above 2 across a long scripted run.
- V9: room data matches section 5.
- V10: input map has only attack, dash and pause.
- V11 edge cases 1, 4, 7. For 7, a 0.1 s hitch and a larger one: no skipped telegraph, damage never in the update that starts a telegraph, at least one rendered frame of cue first.
- Invariants: same input timing gives the same hit or miss at 30 and 60 FPS.

**Manual QA (cannot be automated):** how the cues look and read (V1 visual part), block and stun cue sound and visual, feel of rooms 2–5, and a 30 versus 60 FPS side-by-side check using a frame-cap option. Add a debug option for frame cap and hitch injection if one does not exist.

### Parallelization decision

- **Code work is sequential.** T1–T6 all change the shared enemy controller and the damage entry point. Parallel work would produce conflicts there, and the team is small. No isolated workspaces.
- **Safe to run in parallel with the code work:** the Art Director's cue assets (separate files, interface fixed above) and the room layout audit and data (T7, separate data). Final cue hookup (T8) waits for the art.
- **Build slicing.** If the route allows two Build steps, split after T3: Build A = T0–T4 (foundation, Grub and Spitter, slots, facing and damage API, with tests); Build B = T5–T9 (Charger, Shieldbearer, rooms, cues). If the route has only one Build step, use one Handoff in the task order above. A reader can check that Build A needs no Charger or Shieldbearer.

### Cost and risk (rough)

Roughly 17–21 person-days, with high uncertainty because I have seen only the repo notes: T0 about 3, T1 2, T2 1, T3 1.5, T4 1.5, T5 2.5, T6 3, T7 1–2, T8 1.5–2, tuning and test pass about 2. This fits Option A and does not exceed what the Goal implies, so no escalation to `game-director`.

| Risk | Mitigation |
|---|---|
| Flinch undermines telegraphs (finding 1) | SQ1 default plus a test: a swipe during a telegraph does not change timing |
| Invulnerability bug (finding 2) | T0.1 first, with tests |
| Tunneling and 30/60 FPS drift | Sub-steps and swept contact (D-004), harness at 30, 60 and with hitches |
| Regression of build 0.3 enemy behavior (no tests today) | Harness first; keep the old behavior only where the spec leaves it unchanged |
| Slot starvation in room 5 (6 enemies, 2 slots) | FIFO grant, and a test that every enemy gets a slot within a bounded time |
| Room 5 readability and Shieldbearer flanking difficulty | Design risk, not technical. All values are in the data table to retune after playtest |
| Collision assumptions (dash and charge pass-through) are unverified | First Build task is to check and report the existing behavior |
| Layout unknown | T7 audit before any layout edits |

### Spec questions (the Game Designer decides; I do not change the spec)

- **SQ1 (flinch).** Should an enemy hit by the player ignore Flinch during Telegraph, Active, Recovery, Stunned and Cooldown? Default: yes for all types, Flinch only in Chase and Waiting. Spec 2.2 and 4.1 imply this, but 3.1, 3.2 and 4.2 are silent. If the answer is no for some types, the "stand still and swipe" tactic may return.
- **SQ2 (slot lifetime).** The slot is held through Telegraph and Active and released at the start of Recovery. A Spitter releases when the shot is fired. Is that the intended reading of "in a telegraph or attack phase"?
- **SQ3 (obstacles).** Does a charge ending on an obstacle (not a wall) also stun? Default: yes, any static solid.
- **SQ4 (waiting behavior).** What should an enemy do while it waits for a slot? Default: Grub holds position about 1.5 tiles away or circles slowly (no attack); Charger repositions; Shieldbearer keeps walking toward the player but does not start a bash; Spitter stays put.
- **SQ5 (guard reference point).** Is the guard check against the player's position at the swipe, or against the swipe hitbox's center? Default: the player's position at swipe time, so close side hits are not accidentally blocked. A shot is checked at its position when it reaches the shield.

No spec item is infeasible. Everything above fits the constraints (no new inputs, 30 and 60 FPS, 5-room slice).

## Decisions already made

- D-001: one attack button plus dash; no new inputs.
- D-002 (Owner): enemy-side depth. No hold-to-charge attack in this work.
- D-003 (Game Designer): time-based telegraphs, 0.4 s floor, 2-attacker cap. The cap fits the existing controller, so its revisit trigger is not met.
- D-004 (Technical Director, new): bounded sub-stepped combat time with a frame-time clamp, and a central attack-slot arbiter.

## Constraints

- No new inputs. Spec numbers are fixed by the Game Designer; I change none. Playtester handoffs (step 9) must not include implementation details or the experience signals in spec 7.2.
- The Build is a dry-run: state the changes exactly (what, where, how to exercise), naming systems rather than file paths I cannot confirm.

## Open questions

- SQ1–SQ5 above, for `game-designer`. Defaults are stated so Build can proceed.
- Layout audit result for rooms 2–5 (T7), once the layout data is available to the Build step.

## Expected output

The Studio writes the Build Handoff (to `technical-director` or the Build Role per the route) with: the task list T0–T9 in order, D-004, the cue interface from this plan merged with the Art Director's cue design, the defaults for SQ1–SQ5 (or the Game Designer's answers), and the acceptance checks V1–V11 for QA. The Build Handoff should be addressed to `studio` for the result per the routing note. The Studio also passes the cue-limits section to the Art Director.

## Sender assessment

Confidence: high on the architecture (phase machine, arbiter, sub-stepping) and the flinch and invulnerability findings, which come directly from the repo notes. Medium on cost and layout, because I have no layout data and have not seen the code, only the notes. The biggest risk to the goal itself is SQ1: if flinch cancels telegraphs, the monotony problem returns whatever else is built.

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: project.md#constraints, design/combat-enemy-depth.md, design/combat.md, sim/repo-notes.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-enemy-side-combat-depth.md, decisions/D-003-time-based-telegraphs-and-attack-limit.md, decisions/D-004-combat-timing-substeps-and-attack-slots.md
- Previous handoff: goals/G-002-combat-monotony/06-game-designer-to-technical-director.md
>>>END

<<<FILE goals/G-002-combat-monotony/09-art-director-to-studio.md
---
kind: handoff
goal: G-002
seq: 9
from: art-director
to: studio
stage: Design
outcome: done
---
# 09: art-director → studio — Visual cues for enemy telegraphs, charge lane, block and stun are designed

## Task

Merge this visual design with the Technical Director's plan (step 6a) and write the Build Handoff. Pass the open questions below to `game-designer` and the Technical Director.

## Context

Goal G-002 「戦闘が単調なので改善したい」, Option A (D-002). The Game Designer's spec in `design/combat-enemy-depth.md` left the visual cues undecided (its Q1). Handoff 07 asked for a visual design with player-observable readability criteria. No timings, damage, ranges or rules were changed.

## Findings

The full visual spec is in `design/combat-enemy-visuals.md`. In short:

- **One shared approach** for all four damaging attacks: a threat shape (outline plus fill that is full exactly when damage can begin), a lock change (thin dashed orange outline becomes thick solid red with a 0.1 s white-hot flash, and the locked state persists), and a rim pulse on the attacking enemy. Everything is driven by elapsed seconds, so it reads the same at 30 and 60 FPS.
- **Shapes tell attacks apart even in grayscale:** Grub is a short arrow-rectangle, Spitter is a thin aim line with a reticle, Charger is a 1-tile-wide lane with chevrons and an end-cap bar, Shieldbearer bash is a wedge.
- **Lock moments:** Spitter at 0.4 s of 0.6 s, Charger at 0.5 s of 0.8 s (lane rotates and updates before, fixed after), Shieldbearer bash drawn locked from the start, Grub at the end of the telegraph.
- **Palette rule:** saturated orange/red appears only on active threats. Non-threat information (Shieldbearer guard plate, block cue, stun sparks, guard-down opening) uses cold steel/cyan-white, so "hot = danger, cold = opening".
- **Lantern vs threat:** the lantern is a soft, amber, edge-less glow. Threat shapes are hard-edged, saturated, drawn above the lighting pass (so they show in the dark), and have a dark keyline for lit floor.
- **Room 5:** at most 2 threat shapes at once (D-003). Fills are alpha-capped at 35 %, outlines are opaque, and the Charger lane draws underneath. Waiting and recovering enemies show no orange/red.
- **Block cue:** steel-white spark ring at the contact point plus a plate flash, 0.2 s, with a distinct clank sound. **Stun cue (1.5 s):** tilted low sprite with circling steel sparks that blink faster in the last 0.3 s. **Open recovery (0.8 s):** only a dimmed sprite and a dust puff.
- **Acceptance:** VC1–VC14 (QA checks at both frame rates, including contrast ≥ 3:1, lock timing ±0.05 s, shape matches hit area, no strobing) and VE1–VE5 (experience signals for Review; do not put these in the Playtester's handoff).

## Decisions already made

- D-001: one attack button plus dash; no new buttons.
- D-002 (Owner): enemy-side depth only; no hold-to-charge attack.
- D-003: time-based telegraphs with a 0.4 s floor; at most 2 simultaneous attackers.

## Constraints

- Do not change specified timings, damage, ranges or rules. The questions below ask for confirmation or a change by the owning Role.
- Scope: the 5-room slice only.
- Hit areas and cue geometry must come from the same data (cost flag F7).

## Open questions

1. **For `game-designer` (N1, worth routing before Build):** the Grub's direction locks at the end of its 0.5 s telegraph and the lunge takes 0.15 s, which leaves almost no reaction time after the lock. Is that intended? If not, the lock point should move earlier (for example 0.2 s before the lunge, like the Spitter). The visual works either way.
2. **For `game-designer` / `technical-director` (Q-A, Q-B):** Spitter projectile range, and the real widths and angles of the Grub lunge, the Spitter line and the Shieldbearer bash cone. The visual spec assumes about 1 tile wide for the Grub and about 90° for the cone, and will follow the real hit areas.
3. **For `technical-director` (F1–F7):** check that a shared threat-shape renderer with three masks and a chevron texture is cheap, that an outline/rim effect on enemy silhouettes is available (fallback: pre-baked brighter outline sprites), the draw cost of an 8-tile lane plus 2 shapes plus projectiles at 30 FPS, that cue states come from enemy state and phase time (not animation frames), and that the cue is on screen at least one rendered frame before damage. Also check whether the slice has audio support for the single block "clank" sound; if not, drop only the sound part of VC7.
4. **For the Build step (F6):** check existing enemy sprites for saturated orange/red accents. These would conflict with the reserved-color rule and need a small recolor task.
5. **For the Studio:** link `design/combat-enemy-visuals.md` in the `project.md` Design index next to `design/combat-enemy-depth.md`.

## Expected output

A Build Handoff written by the Studio, combining the Technical Director's plan with `design/combat-enemy-visuals.md`. The Build Handoff should include the acceptance criteria VC1–VC14 for QA. Later, the Art Director's visual review of the build checks VC1–VC14 and VE1–VE5 (the VE items stay out of the Playtester's handoff).

## Sender assessment

Confidence: medium-high that the shared shape + lock + rim approach keeps room 5 readable, because the attack limit of 2 caps the on-screen shapes. Main risks: (a) the Grub lock timing (question 1), which is a rules issue, not a visual one; (b) the colors are proposed values and need a check on real captures for the 3:1 contrast criterion in lit areas; (c) the steel-colored cues might get lost beside the lantern's pale light, which visual review should confirm.

## Load

- Role: none (Studio routing)
- Skills: none
- Project: design/combat-enemy-visuals.md, design/combat-enemy-depth.md, project.md#art-direction
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-enemy-side-combat-depth.md, decisions/D-003-time-based-telegraphs-and-attack-limit.md
- Previous handoff: goals/G-002-combat-monotony/07-studio-to-art-director.md
>>>END
