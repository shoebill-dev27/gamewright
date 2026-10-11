# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/07-game-director-to-game-designer.md, goals/G-001-combat-monotony/08-gameplay-engineer-to-studio.md
next_seq: 9
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/07-game-director-to-game-designer.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/08-gameplay-engineer-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 09
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
decisions/D-002-combat-variety-direction.md
design/combat.md
goals/G-001-combat-monotony/01-studio-to-playtester.md
goals/G-001-combat-monotony/02-playtester-to-game-designer.md
goals/G-001-combat-monotony/03-studio-to-qa.md
goals/G-001-combat-monotony/04-game-designer-to-game-director.md
goals/G-001-combat-monotony/05-qa-to-studio.md
goals/G-001-combat-monotony/06-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/07-game-director-to-game-designer.md
goals/G-001-combat-monotony/08-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/goal.md
project.md
sim/build-0.3.md
sim/build-0.4.md
sim/repo-notes.md
>>>END

<<<FILE @decision-titles
decisions/D-001-one-button-combat.md — D-001: Combat uses one attack button plus dash
decisions/D-002-combat-variety-direction.md — D-002: Fix combat monotony with encounter escalation first, then enemy behaviors that demand movement and the dash
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
- Decide: is there a real choice of direction, priority or scope? Yes. The diagnosis (handoff 04) offers three options (A: enemy behaviors, B: encounter design and escalation, C: rule rewards) that differ in scope and cost.
- Design: is the intended behavior specified well enough to build? Not for any change yet. Tentative on the chosen option.
- Plan: tentative. Needed only if the chosen change is non-obvious, risky or cross-system.
- Build: tentative for the chosen direction. Planned for the dash-damage defect fix (confirmed by QA).
- Verify: always after Build.
- Play: the Goal is about how the game feels, so a Playtester re-evaluates after Build (tentative with Build of the chosen direction).
- Review: experience Goal, so the Game Director judges the outcome. Planned.
- Observe (defect): the Playtester saw a possible dash-damage defect. QA confirmed it against `design/combat.md` (handoff 05). Intended behavior is already specified, so the fix needs no Design or Plan.

Skipped: none.

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | playtester | playtest-session | done | [01-studio-to-playtester.md](01-studio-to-playtester.md) → report in [02-playtester-to-game-designer.md](02-playtester-to-game-designer.md) |
| 2a | Diagnose | game-designer | diagnose-experience | done | [02-playtester-to-game-designer.md](02-playtester-to-game-designer.md) → diagnosis in [04-game-designer-to-game-director.md](04-game-designer-to-game-director.md) |
| 2b | Observe (possible defect: damage during dash) | qa | reproduce-defect | done | [03-studio-to-qa.md](03-studio-to-qa.md) → report in [05-qa-to-studio.md](05-qa-to-studio.md) |
| 3a | Decide | game-director | make-decision (prepare-owner-escalation if a trigger fires) | open | [04-game-designer-to-game-director.md](04-game-designer-to-game-director.md) |
| 3b | Build (fix dash-damage defect) | gameplay-engineer | implement-change | open | [06-studio-to-gameplay-engineer.md](06-studio-to-gameplay-engineer.md) |
| 4 | Verify (dash-damage fix) | qa | verify-change | planned (after 3b; Studio composes the Handoff from the engineer's report addressed to `studio`) | — |
| 5 | Design | game-designer | write-design-spec | tentative (if 3a chooses a change) | — |
| 6 | Plan | technical-director | technical-plan | tentative (if the chosen change is non-obvious, risky or cross-system) | — |
| 7 | Build (chosen direction) | gameplay-engineer | implement-change | tentative (if 3a chooses a change) | — |
| 8a | Verify (chosen direction) | qa | verify-change | tentative (after 7) | — |
| 8b | Verify (visuals, e.g. telegraphs) | art-director | visual-review | tentative (after 7, only if the change affects visuals; parallel with 8a) | — |
| 9 | Play | playtester | playtest-session | tentative (after 7; fresh Handoff composed by the Studio without implementation history) | — |
| 10 | Review | game-director | review-outcome | planned | — |

Status: planned | tentative | open | done | skipped.

## Route changes

- After step 1 (Observe, playtester): the report matches the plan on the experience side (monotony confirmed: one winning approach in every room, little pressure to move, dash unused in combat), so Diagnose followed as planned. It also contained a possible defect (damage during a dash after being hit). Per the return rule "Play/Observe: defect → Observe (`qa`)", step 2b was added as a parallel step. Handoff 02 was edited in place (still from `playtester`) to add the Owner's report, mark the dash-defect item as routed to `qa`, and fill in Load and Expected output.
- After steps 2a and 2b: 2a produced a diagnosis with three options of different scope and cost (handoff 04), so Decide (`game-director`) follows. No Owner escalation trigger fires: every option stays within D-001 and the pillars. 2b confirmed a defect against specified behavior (handoff 05), so Build (`gameplay-engineer`) and Verify (`qa`) for the fix join the route. No Design is needed because `design/combat.md` already specifies the behavior. The fix restores specified behavior and does not consume the Decide output, so 3a and 3b run in parallel and the Route waits for both. The earlier tentative Build and Verify rows were split into one pair for the defect fix (3b, 4) and one pair for the chosen direction (7, 8a/8b). The `art-director` visual review (8b) is its own parallel row with the proper role. QA's non-blocking question (how to treat a dash pressed during hit-stun) is left for `game-designer` to fold into any later spec. It does not block the fix.

## Next action

Two parallel steps are open:
- 3a: `game-director` runs Decide from `04-game-designer-to-game-director.md` (skill `make-decision`). The expected output is a Decision with the chosen direction and scope.
- 3b: `gameplay-engineer` fixes the dash-damage defect from `06-studio-to-gameplay-engineer.md` (skill `implement-change`), with the result addressed to `studio`.

After both finish, run Route again. Step 4 (Verify the fix with `qa`) follows 3b, with a fresh Handoff composed by the Studio without the engineer's self-assessment. Step 5 (Design) follows 3a if a change is chosen.

## Outcome

(To be filled at close, in Japanese.)
>>>END

<<<FILE goals/G-001-combat-monotony/07-game-director-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 7
from: game-director
to: game-designer
stage: Design
outcome: done
---
# 07: game-director → game-designer — Write the design spec for G-001 per D-002 (escalation first, then enemy behaviors)

## Task

Write the design spec (skill `write-design-spec`) for the direction chosen in D-002. Phase 1 is encounter escalation within the existing 5 rooms. Phase 2 is 1–2 telegraphed enemy behavior variants. Include player-observable acceptance criteria.

## Context

Goal G-001: the Owner said 「戦闘が単調なので改善したい」. Your diagnosis (handoff 04) found that enemy behavior gives no reason to move (C1) and that encounters do not escalate (C3). The Playtester's walkthrough found that "hold position and swipe" wins every room. I chose B then A, with C in reserve, and recorded it as D-002. This handoff carries the scope and limits so you can write the spec.

## Findings

### Direction chosen (D-002)

- **Phase 1, Option B.** Using existing Grubs and Spitters, escalate across rooms 1–5 in count, Grub/Spitter mix, spawn positions and Spitter placement. Use multi-side spawns and staggered waves so a corner is not a complete answer in later rooms. One or two room-layout variants that make corners less safe are optional. Room 1 should stay approachable, and the ramp should read as a clear arc.
- **Phase 2, Option A.** In scope. Add 1–2 behavior variants on the existing enemies, for example a Grub with a telegraphed wind-up and lunge (so the dash is the answer) and/or a Spitter that repositions or fires a spread or faster shot. Specify the behaviors, but mark them **pending feasibility (`technical-director`) and telegraph visual direction (`art-director`)**.
- **Option C is not adopted.** Do not add attack/dash reward rules or passivity penalties in this spec. Do not add hit-stun or invulnerability retuning either. Note it only as a possible follow-up if passivity persists after Phases 1 and 2.

### Scope decisions answered from your open questions

- Adding new enemy behavior (A) is in scope for G-001, as Phase 2.
- `art-director` should be involved for telegraph visuals, and `technical-director` for feasibility, before Phase 2 is built. I am asking the Studio to route these (see Open questions). Do not wait for them to write the Phase 1 spec.
- B stays inside the 5-room, 15–20 min structure. Do not add rooms or lengthen the run. Real-time run length is unmeasured, so the spec should ask the next playtest to record it.

### Acceptance criteria (player-observable)

Use these as a base and make them testable in the spec:

1. A player cannot clear a later room (e.g. rooms 4–5) by holding one position and attacking.
2. The dash is used in combat in a typical room. This is expected to be fully met only after Phase 2.
3. Later rooms feel different from room 1 in composition, spawn directions or structure.
4. Every threat is visible before it can hurt.
5. Behavior and timing are identical at 30 and 60 FPS.
6. Run length stays within 15–20 minutes. It needs a real-time measurement, which a described walkthrough cannot give.

Mark which criteria belong to Phase 1 and which only to Phase 2.

## Decisions already made

- D-001: Combat uses one attack button plus dash. No new input buttons without Owner approval.
- D-002: Pursue B (encounter escalation, existing enemies) first, then A (telegraphed behavior variants, gated on technical and art review). C in reserve. 5 rooms and the 15–20 min run stay.

## Constraints

- No new input and no pillar change. If the spec would need either, hand it back to me for an Owner escalation.
- All timing must be frame-rate independent (30 and 60 FPS).
- Reuse existing systems (small team). Prefer data and tuning for Phase 1.
- The mid-dash damage oddity is with `qa` (handoff 03) and is not decided here. If QA confirms a build defect, do not change the spec. If it shows a spec ambiguity (for example how hit invulnerability interacts with dash invulnerability), amend `design/combat.md` as a spec clarification.
- Choose exact numbers (counts, speeds, telegraph durations) in the spec. They are your call. Flag any you cannot justify from the evidence as needing playtest tuning.

## Open questions

- Request to the Studio: route `technical-director` (feasibility and cost of the Phase 2 behaviors for a small team) and `art-director` (telegraph visuals meeting pillar 3) once your Phase 2 behavior proposal is written. Their input gates the Phase 2 build, not the Phase 1 build.
- Can the Phase 1 ramp make corners unsafe enough without layout changes, or are one or two layout variants needed? Decide in the spec.
- Does any Phase 1 composition rely on behavior the current Grub/Spitter cannot show (for example, simultaneous multi-side arrival at the current Grub speed)? Flag it if so.

## Expected output

A design spec for G-001 (written via `write-design-spec`) that:
- covers Phase 1 in full and Phase 2 as proposed behaviors pending review;
- includes the player-observable acceptance criteria above, mapped to phases;
- states what is out of scope (new input, extra rooms, Option C rules).

Next, the Studio sends Phase 1 to Build and Phase 2 proposals to `technical-director` and `art-director`. Playtest follows each phase and should record real-time run length.

## Sender assessment

Confidence is high that B-then-A is the right order. It fits the evidence, the vision and the small team, and it keeps Phase 2 cost visible before it is committed. The main uncertainties are tuning and Phase 2 feasibility, which a described walkthrough cannot settle, so the decision leaves both to later review and playtest. No escalation trigger applies.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision; project.md#player-profile; project.md#constraints; design/combat.md
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-002-combat-variety-direction.md
- Previous handoff: goals/G-001-combat-monotony/04-game-designer-to-game-director.md
>>>END

<<<FILE goals/G-001-combat-monotony/08-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-001
seq: 8
from: gameplay-engineer
to: studio
stage: Build
outcome: done
---
# 08: gameplay-engineer → studio — Dash/hit invulnerability fix (build 0.3 → 0.3.1), ready for QA verification

## Task

Compose the QA verification Handoff from this change. QA verifies it independently against the acceptance criteria in `05-qa-to-studio.md` (restated in 06). I do not certify the fix as verified.

## Context

Goal G-001 (combat monotony). Handoff 06 asked for the defect "player takes damage partway through a dash shortly after being hit" to be fixed, and for the trigger to be reported. The expected behavior is fully specified in `design/combat.md`, so nothing needed to go back to Design. No spec value was changed.

## Findings

### Trigger found

The trigger comes from reading the invulnerability code path described in the repository notes. It was not measured at runtime, because this dry run has no runnable build. QA should confirm it in play.

- **Timing is what triggers it, not frame rate.** The cause is in the order of two timer expiries relative to the hit. It does not depend on delta time, so it should appear at both 30 and 60 FPS. Frame rate only changes how precisely the window edges are hit.
- **Window A, damage mid-dash:** a dash begun between about 0.55 s and 0.8 s after the hit. The hit invulnerability ends at 0.8 s, while the dash is still running, so the player can be damaged from 0.8 s to the end of the dash. A dash begun at 0.8 s or later is unaffected. The latest damaged-dash start is just under 0.8 s.
- **Window B, damage right after a dash:** a dash begun at 0.3 s to about 0.55 s after the hit. The dash ends before 0.8 s and its end clears invulnerability early. The player can then be damaged between the dash end and 0.8 s after the hit. The spec says that period is still invulnerable. This is the "delayed damage" case in criterion 6.
- **Why the earliest-dash check can look fine:** a dash at exactly 0.3 s is covered by invulnerability for its full length. The damage only shows up after it ends (window B). Window A needs a later press. QA should not test only the 0.3 s press.
- **Damage source:** any source. Grub contact and Spitter projectiles use the same invulnerability check.
- **Dash direction:** not relevant to the cause.
- **Rarity:** it needs a dash pressed within about 0.5 s of a hit, plus a damage source arriving in the remaining window.

### The change, stated exactly

**What:** Player invulnerability stops being a single on/off flag that each timer switches on and off. It becomes two expiry timestamps in game time, and "invulnerable" is computed from them.

**Where:** the player's invulnerability handling. This is the single flag that both the dash and the hit reaction currently write to. The same check is used by every damage source.

**Change:**

1. Remove the shared flag and the two timers that switch it off.
2. Add two values to the player: `hitInvulnUntil` and `dashInvulnUntil`. Both are expiry times on the accumulated game clock, which is the sum of delta times, so they do not depend on frame rate.
3. On a hit, set `hitInvulnUntil = hitTime + 0.8 s`. Hit-stun stays 0.3 s with no input, unchanged.
4. On dash start, set `dashInvulnUntil = dashStartTime + 0.25 s`. Dash distance, duration and the 0.6 s cooldown are unchanged.
5. `isInvulnerable(now)` returns `now < max(hitInvulnUntil, dashInvulnUntil)`. Every damage source calls this when it tries to apply damage. Neither window can cancel or shorten the other.
6. Nothing else changes: the attack queued during a dash still fires when the dash ends. The handling of a dash pressed during hit-stun is left exactly as it is now. It is unspecified and is the separate non-blocking question for `game-designer`.

**Tests:** I added unit tests for `isInvulnerable` on a simulated game clock. They cover the cases listed below, each run with fixed steps of 1/30 s and 1/60 s and with varying delta times.

- Dash with no hit: invulnerable for 0.25 s, not after.
- Hit alone: invulnerable until 0.8 s, not after.
- Dash started at 0.3, 0.5, 0.55, 0.6, 0.79 and 0.8 s after a hit: invulnerable for the whole dash and until at least 0.8 s after the hit.
- Damage attempted at every step from the hit to 1.2 s after it.

These are new tests, since none existed. They are my own check, not a verification.

### How to exercise it (for QA)

At 30 FPS and 60 FPS, in rooms 1–5 with Grubs and Spitters:

1. Take a hit. Then dash at delays after the hit of about 0.3, 0.4, 0.5, 0.55, 0.6, 0.7, 0.79, 0.8 and 0.85 s, with a damage source (Grub in contact, or a Spitter projectile timed to arrive) present through the dash and the time after it.
2. Check there is no damage during the dash.
3. Check there is no damage between the dash end and 0.8 s after the hit.
4. Check that damage can land again normally after 0.8 s after the hit, if no dash is active.
5. Dash with no preceding hit. Check the full 0.25 s is invulnerable and damage can land right after it.
6. Repeat with dash directions towards and away from the damage source.

### Criteria addressed

All six criteria in `05-qa-to-studio.md`:

| Criterion | How it is addressed |
|---|---|
| 1, 2, 3 | Covered by the change. The window-A and window-B timings need particular attention. |
| 4 | Covered by the dash-only timestamp. |
| 5 | Hit-stun, the 0.8 s hit window, the 0.6 s cooldown and the queued attack are untouched, but QA should still check them. |
| 6 | Window B is the "damage delayed to land right after the dash ends" case. It is now covered, because the hit window is no longer cleared by the dash end. |

### Known risks

- **More protection than before in one case.** A dash begun just after a hit used to lose invulnerability when it ended, and now keeps it until 0.8 s after the hit. The spec requires this. Some players may notice more safe time after a hit-then-dash. That is a design matter and I did not change it.
- **Boundary frames.** The check is `now < expiry`. A damage event exactly on the 0.8 s or 0.25 s boundary is treated as expired. At variable delta time this can differ by one frame from what a tester expects. QA should treat a one-frame difference at the exact boundary as expected.
- **Unspecified:** a dash pressed during hit-stun is unchanged (ignored or buffered, whichever it is now). It is not part of this fix.
- **Other flag users.** I found no other writer of the old flag in the notes. QA should watch for any other effect that depended on it, such as flicker or sound cues for invulnerability. The repository notes don't describe any.

## Decisions already made

- D-001: Combat uses one attack button plus dash. No new input was added.

## Constraints

- It must play correctly at 30 and 60 FPS. The fix uses accumulated game time, not frame counts.
- It reuses the existing player invulnerability code. No new systems.
- No value in `design/combat.md` changed.

## Open questions

- Non-blocking, for `game-designer`: should a dash pressed during hit-stun be ignored or buffered? It is unspecified and unchanged here.

## Expected output

The Studio composes the verification Handoff to `qa` from the "Findings" section (the change, how to exercise it, criteria addressed, known risks). It leaves out `## Sender assessment`. QA verifies against the six criteria at 30 and 60 FPS and returns a pass/fail verdict.

## Sender assessment

**Root cause (from code notes, not measured at runtime):** invulnerability was one shared boolean. The dash set it and started a 0.25 s timer. A hit set it and started a timer ending 0.8 s after the hit. Each timer's expiry unconditionally set the flag off, whatever else was still active. So whichever timer fired first cleared the other's protection:

- Window A: the hit timer (0.8 s) fires mid-dash when the dash began between about 0.55 s and 0.8 s after the hit.
- Window B: the dash timer fires and clears the flag while the hit window is still running, when the dash began between 0.3 s and about 0.55 s after the hit.

QA's hypothesis, one timer's expiry clearing the other's flag, is **confirmed**. It happens in both directions. The "dash begun during or just after hit-stun restarts or cancels a timer" variant is not needed to explain the behavior, so I discarded it.

**Frame rate:** the logic is the same at both rates. It depends on the order of expiries on the timeline. I expect it at both 30 and 60 FPS, but this is inferred, not observed.

**Confidence:** high on the root cause given the notes. Medium on the exact window edges (about 0.55 s and 0.8 s), which follow from the stated durations and the earliest dash start of 0.3 s. I own test results only at unit level, on the simulated clock. I have not played the build, and QA should verify on the real one.

## Load

- Role: studio/roles/qa.md
- Skills: none
- Project: design/combat.md; sim/build-0.3.md; project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/06-studio-to-gameplay-engineer.md
>>>END
