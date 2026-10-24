# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-first-puzzle-stall/36-qa-to-studio.md
next_seq: 37
context_request: allowed once (@need, up to 8 paths)
current_build: sim/build-0.6.md (newest simulated build; older ones are history)
log: last 5 of 17 entries in @log-recent; the full history is goals/G-001-first-puzzle-stall/log.md

## You may write

- goals/G-001-first-puzzle-stall/goal.md
- goals/G-001-first-puzzle-stall/36-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-first-puzzle-stall/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 37
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

`goal.md` holds the Goal's current state; its history is the **Goal log**, `log.md` in the
Goal's directory. After every Intake, Route and Resume, whoever runs the operation appends one
entry (an isolated runtime does it itself): the operation and date, the Goal's status and open
steps, and the *Route changes* text just written. Entries are never edited or removed, and no Role
or Studio operation rewrites the log. Every operation keeps *Owner request* exactly as quoted at
Intake. Only Resume, after an Owner decision, may change *Interpretation*; a Route that would need
to reinterpret the Goal escalates instead.

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

Load: `goal.md`, the last few entries of the Goal log, the latest Handoff, this file,
`studio/workflows/development-loop.md`; for steps 4–5 also the recipient's Role contract and the
files you put in its Load list.

1. Mark the step done in the route table, linking its Handoff.
2. **Compare the outcome with the plan.** If it fits, the next planned step follows. If not, apply
   the return rules in `development-loop.md`, revise the remaining route, and say why under
   *Route changes* in one to three lines (600 characters at most), replacing the previous text
   (the Goal log keeps the history; the Handoffs carry the details). Keep *Unknowns* current the
   same way: update a stage's line, do not narrate earlier passes. Confirm (`planned`) or drop
   (`skipped`) any `tentative` stage whose condition this result settles. The route is a plan,
   not a contract.
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
answer, and the stage it creates. Also: stages skipped and why. Current state, not history: when a
stage runs again, update its line instead of adding the story of earlier passes, and drop settled
items (3,000 characters at most).>

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | <stage> | <role-id> | <skill-id> | planned | — |

Status: planned | tentative | open | done | skipped. Handoff: the file name (in this goal's directory)
of the incoming Handoff that starts the step. Parallel steps: 2a, 2b. Step numbers need not
match Handoff seq numbers. Role: exactly one role id per row; a parallel step gets its own row.
Keep Stage and Status cells short (80 characters at most); details belong in the Handoffs. The
route is a plan; the Route operation revises it.

## Route changes

<This operation's change only, in 1–3 lines (600 characters at most): after which step, what
changed, and why. Replace the previous text; the full history is in `log.md`.>

## Next action

<Who starts what next, with which Handoff. Or: waiting for the Owner on <escalation>.>

## Outcome

<At close, for the Owner, in owner_language: results, Decisions made, next issues, Owner items.>
>>>END

<<<FILE project.md
---
kind: project
id: tidepool-garden
name: Tidepool Garden (sample)
repository: none (sample project for dry-runs; builds are simulated under sim/)
owner_language: ja
player_visible: sim/build-*.md
---
# Project: Tidepool Garden (sample)

## Vision

A calm touch puzzle game for children and families: slide tide pools to guide sea creatures home.
Pillars:

1. **No failure, no timers.** Nothing is ever lost; any move can be undone (D-001).
2. **Learn by touching.** Players discover rules by interacting, not by reading.
3. **Soft and warm**, but interactive pieces always stand out clearly.

## Player profile

Children aged 7–10, some still early readers, often playing beside a parent. Short sessions
(5–15 minutes). Quickly lose interest when nothing responds to their touch.

## Current state

Prototype build 0.2: 12 levels. Level 1 teaches dragging with a text bubble ("Drag the tide pool!").
Dry-run only: "running the build" means reading `sim/build-0.2.md`.

## Constraints

- Phones and tablets, touch only.
- No ads, no in-app purchases.
- No mechanic may depend on reading text.
- Small art budget: reuse the existing sprite sheet where possible.
- Dry-run project: there is no real repository. `sim/repo-notes.md` stands in for the code. A Build
  step implements a change by stating it exactly in its Handoff (what changes, where, and how to
  exercise it); the change then counts as made, and the runtime's simulator updates `sim/` from it.

## Art direction

Pastel palette, rounded shapes. Interactive pieces have a darker outline and a gentle idle motion.

## Design index

- `design/onboarding.md` — level 1–3 teaching plan.
>>>END

<<<FILE @project-files
decisions/D-001-no-fail-states.md
decisions/D-002-intro-cancel-and-undo.md
decisions/D-003-sand-tap-blip-and-pool-hit-area.md
decisions/D-004-ease-back-taps-window-origin-held-pool.md
decisions/D-005-reduce-motion-pulse-fills-window.md
decisions/D-006-cancelled-pulse-and-reduce-motion-beats.md
design/onboarding.md
goals/G-001-first-puzzle-stall/01-studio-to-playtester.md
goals/G-001-first-puzzle-stall/02-playtester-to-game-designer.md
goals/G-001-first-puzzle-stall/03-studio-to-art-director.md
goals/G-001-first-puzzle-stall/04-game-designer-to-studio.md
goals/G-001-first-puzzle-stall/05-art-director-to-studio.md
goals/G-001-first-puzzle-stall/06-studio-to-game-designer.md
goals/G-001-first-puzzle-stall/07-game-designer-to-studio.md
goals/G-001-first-puzzle-stall/08-studio-to-gameplay-engineer.md
goals/G-001-first-puzzle-stall/09-gameplay-engineer-to-game-designer.md
goals/G-001-first-puzzle-stall/10-game-designer-to-studio.md
goals/G-001-first-puzzle-stall/11-studio-to-gameplay-engineer.md
goals/G-001-first-puzzle-stall/12-gameplay-engineer-to-studio.md
goals/G-001-first-puzzle-stall/13-studio-to-qa.md
goals/G-001-first-puzzle-stall/14-qa-to-studio.md
goals/G-001-first-puzzle-stall/15-studio-to-game-designer.md
goals/G-001-first-puzzle-stall/16-game-designer-to-studio.md
goals/G-001-first-puzzle-stall/17-studio-to-gameplay-engineer.md
goals/G-001-first-puzzle-stall/18-gameplay-engineer-to-studio.md
goals/G-001-first-puzzle-stall/19-studio-to-game-designer.md
goals/G-001-first-puzzle-stall/20-game-designer-to-studio.md
goals/G-001-first-puzzle-stall/21-studio-to-gameplay-engineer.md
goals/G-001-first-puzzle-stall/22-gameplay-engineer-to-studio.md
goals/G-001-first-puzzle-stall/23-studio-to-qa.md
goals/G-001-first-puzzle-stall/24-qa-to-studio.md
goals/G-001-first-puzzle-stall/25-studio-to-game-designer.md
goals/G-001-first-puzzle-stall/26-game-designer-to-studio.md
goals/G-001-first-puzzle-stall/27-studio-to-gameplay-engineer.md
goals/G-001-first-puzzle-stall/28-gameplay-engineer-to-studio.md
goals/G-001-first-puzzle-stall/29-studio-to-qa.md
goals/G-001-first-puzzle-stall/30-qa-to-studio.md
goals/G-001-first-puzzle-stall/31-studio-to-game-designer.md
goals/G-001-first-puzzle-stall/32-game-designer-to-studio.md
goals/G-001-first-puzzle-stall/33-studio-to-gameplay-engineer.md
goals/G-001-first-puzzle-stall/34-gameplay-engineer-to-studio.md
goals/G-001-first-puzzle-stall/35-studio-to-qa.md
goals/G-001-first-puzzle-stall/36-qa-to-studio.md
goals/G-001-first-puzzle-stall/goal.md
goals/G-001-first-puzzle-stall/log.md
project.md
sim/build-0.2.md
sim/build-0.3.md
sim/build-0.4.md
sim/build-0.5.md
sim/build-0.6.md
sim/repo-notes.md
>>>END

<<<FILE @decision-titles
decisions/D-001-no-fail-states.md — D-001: No fail states and no timers
decisions/D-002-intro-cancel-and-undo.md — D-002: Intro cancel eases the pool back; the intro is never in undo history
decisions/D-003-sand-tap-blip-and-pool-hit-area.md — D-003: Rate-limited sand taps show a pool brightness blip; the pool's hit area follows its drawn size
decisions/D-004-ease-back-taps-window-origin-held-pool.md — D-004: Taps during the ease-back, the 1.5 s window origin, and second-finger taps on a held pool
decisions/D-005-reduce-motion-pulse-fills-window.md — D-005: Under reduce-motion the redirect pulse is a 0.6 s two-beat brightness pulse
decisions/D-006-cancelled-pulse-and-reduce-motion-beats.md — D-006: A pulse cancelled by a pool touch stops being the response; the reduce-motion beats are contiguous
>>>END

<<<FILE goals/G-001-first-puzzle-stall/goal.md
---
kind: goal
id: G-001
project: tidepool-garden
status: active
created: 2026-10-10
---
# G-001: Children stall at the first puzzle

## Owner request

> 最初のパズルで子どもが手を止めてしまう。直したい

## Interpretation

Success condition: when children in the target group (ages 7–10) play the first puzzle (level 1 in
build 0.2), they begin purposeful touch interaction with the puzzle on their own, without a long
pause and without an adult having to explain what to do. How long a pause counts as "a stall" is
not set here; Observe reports what actually happens and Design turns it into a player-observable
acceptance criterion.

Out of scope:

- Levels 2 and later. If the same problem shows up there, it becomes a proposed new Goal.
- Changing a vision pillar or Decision D-001 (no failure, no timers). Any fix must stay inside them.
- New art beyond the existing sprite sheet (project constraint).

## Unknowns

Entry questions (`studio/workflows/development-loop.md`) the Project Context cannot answer:

- **Observe** — done (stage 1, playtester; an experience problem, not a defect).
- **Diagnose** — done (2 game-designer, 2b art-director).
- **Design** — done. Spec revision 5 is settled (3h; SG-1 ruling, blip after a cancelled pulse; D-006). Earlier gaps are closed in revisions 2–4 and D-003 to D-005.
- **Build** — done. Build 0.6 implements revision 5 (4f, stated in Handoff 34) with corrected build record wording. The engineer had no source or test run in the packet, so the code change counts as made only through the simulated build record.
- **Verify** — Always after Build. 5d is open (35): checks 4, 13, 18, 19, 20, 21 (21 new; 4, 19, 20 changed; 13 and 18 regression). If check 4 fails a second time, route to `technical-director` (loop limit).
- **Play** — Is the Goal about how the game plays or feels? Yes. Stage 6, fresh context without implementation history, on the build after 5d passes.
- **Review** — Experience Goal: yes. Stage 7 (`game-director`).
- **Next** — Always. Stage 8.

Skipped:

- **Decide** — The fix choices are player-facing behavior inside the approved direction
  (`game-designer` authority). Option C (idle hint) is excluded; if wanted later, route Decide
  because it touches D-001.
- **Plan** — The change is local to level 1. If Build finds it is not local, the return rules send
  it to Plan.

Flag for Review: the start-of-level intro motion is judged by the designer to be outside D-001
(one-time, no timer, no inactivity trigger). `game-director` should confirm. Also watch whether a
child reads the post-cancel pool blip as an error (D-006 revisit trigger).

Open items (non-blocking, carry to Review / Close):

- Whether iOS "Reduce Motion" / Android "Remove animations" are readable on target platforms is
  unconfirmed. The spec's fallback works either way. An item for the Owner.
- The project has no device: QA has no real image of the home styling or a 60 fps recording. Checks
  2, 3, 11, 17, 18, 19, 20 and 21 rest on the build record's stated values, and the pulse tail
  (0.55–0.6 s) is unseen on a capture.
- Levels 2 and 3 were not run by QA (stated unchanged).
- Settled in 3h: crab brightening under reduce-motion is one 0.4 s change per touch-down, not held;
  O2 is a minimum (build record wording fixed in build 0.6).

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | playtester | playtest-session | done | 01-studio-to-playtester.md |
| 2 | Diagnose | game-designer | diagnose-experience | done | 02-playtester-to-game-designer.md |
| 2b | Diagnose | art-director | visual-review | done | 03-studio-to-art-director.md |
| 3 | Design | game-designer | write-design-spec | done | 06-studio-to-game-designer.md |
| 3c | Plan | technical-director | technical-plan | skipped | — |
| 4 | Build | gameplay-engineer | implement-change | done | 08-studio-to-gameplay-engineer.md (held: question, no change made) |
| 3d | Design | game-designer | write-design-spec | done | 09-gameplay-engineer-to-game-designer.md (answered in 10) |
| 4b | Build | gameplay-engineer | implement-change | done | 11-studio-to-gameplay-engineer.md (result: 12) |
| 5 | Verify | qa | verify-change | done | 13-studio-to-qa.md (pass, 12/12; report: 14) |
| 3e | Design | game-designer | write-design-spec | done | 15-studio-to-game-designer.md (result: 16) |
| 4c | Build | gameplay-engineer | implement-change | done | 17-studio-to-gameplay-engineer.md (held: question 18, no build 0.4) |
| 3f | Design | game-designer | write-design-spec | done | 19-studio-to-game-designer.md (result: 20) |
| 4d | Build | gameplay-engineer | implement-change | done | 21-studio-to-gameplay-engineer.md (result: 22, build 0.4) |
| 5b | Verify | qa | verify-change | done | 23-studio-to-qa.md (fail: check 4 under reduce-motion; report: 24) |
| 3g | Design | game-designer | write-design-spec | done | 25-studio-to-game-designer.md (result: 26, spec rev 4, D-005) |
| 4e | Build | gameplay-engineer | implement-change | done | 27-studio-to-gameplay-engineer.md (result: 28, build 0.5) |
| 5c | Verify | qa | verify-change | done | 29-studio-to-qa.md (pass 20/20 on record; SG-1, O1; report: 30) |
| 3h | Design | game-designer | write-design-spec | done | 31-studio-to-game-designer.md (result: 32, spec rev 5, D-006) |
| 4f | Build | gameplay-engineer | implement-change | done | 33-studio-to-gameplay-engineer.md (result: 34, build 0.6) |
| 5d | Verify | qa | verify-change | open | 35-studio-to-qa.md |
| 6 | Play | playtester | playtest-session | planned | — |
| 7 | Review | game-director | review-outcome | planned | — |
| 8 | Next | studio | — | planned | — |

Status: planned | tentative | open | done | skipped. The route is a plan; the Route operation
revises it.

## Route changes

After step 4f (34): Build is done as build 0.6 (spec revision 5, SG-1 change; build record wording fixed). No spec gap or question came back, so Plan stays skipped and nothing escalates. Verify 5d is open for `qa` (35) with the Sender assessment left out. Play and Review stay planned.

## Next action

Run step 5d (Step operation): `qa` on `35-studio-to-qa.md`, reporting to `studio`. Then Route. If Verify passes, compose a Playtester Handoff from permitted information only (build and player profile; no change, no expected result) to open Play 6. If a check fails, apply the return rules (Build with the failure report; a second failure of check 4 goes to `technical-director`; an undefined behavior goes to Design). Carry the non-blocking items forward to Review / Close. Phase 1: the Studio stops after every Route.

## Outcome

<!-- Filled at close, for the Owner, in owner_language (ja). -->
>>>END

<<<FILE @log-recent
## 030-route · 2026-10-12

Status: active. Open: 27-studio-to-gameplay-engineer.md.

After step 3g (26): the designer chose the reduce-motion mechanism (0.6 s two-beat brightness pulse, spec revision 4, D-005) and found no other silent window. Default-mode behavior is unchanged. Build 4e is open for `gameplay-engineer` (27), then Verify 5c (checks 1–20; 19 and 20 new). Plan stays skipped; no escalation.

## 033-route · 2026-10-12

Status: active. Open: 29-studio-to-qa.md.

After step 4e (28): Build is done as build 0.5 (spec revision 4, changes 1–5); the engineer found no blocking spec gap, so Plan stays skipped and nothing escalates. Verify 5c is open for `qa` with a fresh Handoff (29) that omits the Sender assessment and lists checks 1–20 (19 and 20 new). Play and Review stay planned.

## 035-route · 2026-10-12

Status: active. Open: 31-studio-to-game-designer.md.

After step 5c (30): QA passed checks 1–20 on the build record but found spec gap SG-1 (sand tap after a pool touch cancelled a pulse, before P+0.6 s: no defined response, yet check 4 requires one) and a check 20 wording mismatch (O1). Expected behavior is undefined, so Design reopens as 3h. Build 4f and Verify 5d are tentative on a behavior change. Play waits for a settled build. No escalation.

## 038-route · 2026-10-13

Status: active. Open: 33-studio-to-gameplay-engineer.md.

After step 3h (32): the designer ruled SG-1 (a blocked sand tap after a pulse cancelled by a pool touch gets the blip, both modes; spec rev 5, D-006). Player-facing behavior changes, so Build 4f is confirmed and open (33), and Verify 5d is now planned. O1 and O3 are wording or accepted; no escalation, Plan stays skipped.

## 041-route · 2026-10-13

Status: active. Open: 35-studio-to-qa.md.

After step 4f (34): Build is done as build 0.6 (spec revision 5, SG-1 change; build record wording fixed). No spec gap or question came back, so Plan stays skipped and nothing escalates. Verify 5d is open for `qa` (35) with the Sender assessment left out. Play and Review stay planned.
>>>END

<<<FILE goals/G-001-first-puzzle-stall/36-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 36
from: qa
to: studio
stage: Route
outcome: pass
---
# 36: qa → studio — Verification of build 0.6 (spec revision 5): checks 4, 13, 18, 19, 20, 21 pass

## Task

Receive the verification report for `sim/build-0.6.md` against checks 4, 13, 18, 19, 20 and 21 of `design/onboarding.md` (revision 5). Route the next stage (Review and Close, with the non-blocking captures listed below).

## Context

Goal G-001 (children stall at the first puzzle). Handoff 35 asked QA to verify build 0.6. Checks 4, 19, 20 and 21 are new or changed. Checks 13 and 18 are regression checks because they share the sand-tap flash. The project has no device or repository. As in earlier passes, the build record stands in for the running build.

**Evidence basis:** every result below was judged by reading the build record against the spec. Nothing was captured on a device or in a 60 fps recording. The record's stated timings are not presented as captured. QA did not use the implementer's assessment.

## Findings

**Verdict: pass.** No criterion fails, no regression was found, and there are no blocking spec gaps. Three minor record-wording observations are listed below.

### Per-check results

| Check | Result | Evidence from the build record | Basis |
|---|---|---|---|
| 4 (revised) | **Pass** | Crab, home, sand and pool each answer within 0.2 s. The crab and home respond within 0.1 s. Pool lift is within 0.1 s. A pulse starts within 0.2 s, including 0.15 s after an intro-cancel. During the glide, a sand tap gets the pending pulse at 0.15 s, which is inside 0.2 s. A second-finger sand tap while the pool is held gets the flash. Sand after a cancelled pulse gets the flash within 0.1 s. "Every touch on the crab, home, sand or pool shows a visible response within 0.2 s." The reduce-motion section covers the same cases. | Record only |
| 13 (regression) | **Pass** | A sand tap from 0.6 s up to just under 1.5 s after a pulse start gets the flash: +15% within 0.1 s, fading over 0.3 s, with no size change or movement and no new pulse. A running flash is not restarted ("Only one flash plays at a time"). At 1.5 s or later a new pulse starts and there is no flash. Flashes do not count toward the limit and never delay a pulse. Reduce-motion is the same: the first pulse is the two-beat +30% pulse and the flash is unchanged. | Record only |
| 18 (regression) | **Pass** | A second-finger sand tap on a held pool gives the flash, with no pulse and no change of lifted size. A crab or home tap gives its own response only, and the crab faces the position under the finger. "These taps do not change when the next pulse is allowed", and after release the 1.5 s window counts from the last pulse that actually started. Both modes: the flash is stated as the same in reduce-motion. | Record only |
| 19 (new) | **Pass** | Sand taps from the pulse start up to 1.4 s each get a visible response: the running beat up to about 0.55 s (beat 2 at 0.4 and 0.5 s), the faint end of beat 2 from about 0.55 to 0.6 s, and the flash from 0.6 s (including exactly 0.6 s) to under 1.5 s. At 1.5 s or later a new pulse starts and there is no flash. The record does not name the 0.3 s tap. It follows from "single frame at normal brightness" and "beat 2 starts the instant beat 1 ends": beat 2 rises from the next frame, well inside 0.2 s. | Record only. Needs a 60 fps capture (non-blocking): the 0.3 s instant, and taps at 0.55–0.6 s (accepted tail, D-006 O3). |
| 20 (revised) | **Pass** | Two beats, each rising to +30% within 0.1 s and back to normal by 0.3 s after its start. Beat 2 starts the instant beat 1 ends, so the pool is at normal brightness for a single frame only. Total 0.6 s, with no size change or movement. The pool shows the larger of the active changes, never the sum. A flash still fading is ended at once by a new pulse. The idle brightness effect (max +8%) is hidden during a pulse and restarts from normal. | Record only. Needs a 60 fps capture (non-blocking): beat shape, the single frame between the beats, and the 0.55–0.6 s tail. |
| 21 (new) | **Pass** | After a pulse is cancelled by a pool touch, a sand tap before 1.5 s from the pulse start gets the flash within 0.1 s, "from the moment of the cancel, with no 0.6 s wait, also during the pool's release shrink". This covers cancels at about P+0.1 s and P+0.4 s, a tap at P+0.45 s and a tap inside the release shrink. The flash has no new pulse and no size change. A sand tap at 1.5 s or later after the pulse start gets a new pulse and no flash. A crab or home tap in the window gets its own response only. While the finger still holds the pool, the held-pool rule applies (check 18). The reduce-motion section states the cancel case and says the pool brightness is back to normal at touch-down, so the flash rises from normal. An uncancelled pulse is unchanged: a sand tap in its first 0.6 s shows the pulse and no flash. | Record only |

### Other behaviors in Handoff 35, Findings 1–8

All eight agree with the record. This includes the cancelled pending pulse during the ease-back (no pulse, no window) and the crab brightening under reduce-motion. It is one change per touch-down, starts within 0.1 s, is not held while the finger is down, and has nothing extra on release.

### Build record wording (requested)

- **Pulse spacing:** the record reads "at least 1.5 s" after the previous pulse start, in "Repeated touches". Agrees with the spec.
- **Sand-tap lines:** both state the cancelled-pulse exception. One is the "(… or the pulse was cancelled by a pool touch)" condition. The other is "unless the pulse was cancelled by a pool touch". Agrees.
- **Pulse cut short:** the record states that the flash applies "from the moment of the cancel, with no 0.6 s wait, also during the pool's release shrink". Agrees.
- **Header:** it notes the flash after a cancelled pulse in both modes. Agrees.

### Non-blocking observations (not failures; wording only)

1. **Crab brightening timing (reduce-motion):** the record says it "brightens from normal to +20% at 0.2 s and back over about 0.4 s". Read literally, that could mean 0.2 s up and 0.4 s down, about 0.6 s in total. The spec says one change of about 0.4 s in total. The behavior stays judged as passing, but the record should say "about 0.4 s in total, peak at 0.2 s". Severity: low, wording only. No check depends on the crab duration.
2. **Flash and pool touch (default mode):** spec rule 5 says a touch-down on the pool cancels a running flash. The record's "Touching the pool" section lists only the opening movement, ease-back and redirect pulse. The reduce-motion section does say it ends "any running pulse or flash". The default-mode cancel of a running flash cannot be confirmed from the record. Severity: low. It is outside checks 4, 13, 18, 19, 20 and 21. Suggest adding "and any running flash" to the default-mode line, or confirming the behavior in the next capture.
3. **Glide landing:** "even if a pulse started less than 1.5 s earlier" is consistent with the spec (the pending pulse always starts), but it describes a case that cannot happen on a fresh load. It is harmless.

### Spec gaps

None blocking. Every case tried had a defined expected behavior.

### Checks resting on the record alone

All six: 4, 13, 18, 19, 20 and 21. Within them, these items additionally need a 60 fps capture (non-blocking, for Review and Close): the single frame between the reduce-motion beats (checks 19 and 20), the 0.55–0.6 s tail and taps at 0.56–0.59 s (checks 19 and 20), and the 0.1 s and 0.3 s flash timings (checks 4, 13 and 21).

Checks 1–3, 5–12, 14–17 were outside this pass. Handoff 35 gave the earlier pass on build 0.5 as the basis for checks 1–20, and QA has not re-run them on 0.6 here.

## Decisions already made

- D-001: no failure, no timers, no inactivity cue. Nothing observed in the record conflicts.
- D-003, D-004, D-005: sand-tap flash, ease-back and window origin, reduce-motion pulse. The record is consistent.
- D-006: a pulse cancelled by a pool touch stops being the response, and the reduce-motion beats are contiguous. The record implements both.

## Constraints

- Level 1 only, touch only, no text dependence. Levels 2 and 3 are out of scope.
- QA did not modify any production file and did not redefine any criterion.

## Open questions

None.

## Expected output

Studio: record the pass for checks 4, 13, 18, 19, 20 and 21, and route to Review and Close. Carry the non-blocking device and 60 fps capture items above. Optionally ask the engineer for the two record wording fixes (observations 1 and 2).

## Load

- Role: none (report back to Studio; no further Role work is requested)
- Skills: studio/skills/verify-change.md
- Project: design/onboarding.md, sim/build-0.6.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md, decisions/D-004-ease-back-taps-window-origin-held-pool.md, decisions/D-005-reduce-motion-pulse-fills-window.md, decisions/D-006-cancelled-pulse-and-reduce-motion-beats.md
- Previous handoff: goals/G-001-first-puzzle-stall/35-studio-to-qa.md
>>>END
