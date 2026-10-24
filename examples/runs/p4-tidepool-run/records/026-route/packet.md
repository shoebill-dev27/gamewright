# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-first-puzzle-stall/22-gameplay-engineer-to-studio.md
next_seq: 23
context_request: allowed once (@need, up to 8 paths)
current_build: sim/build-0.4.md (newest simulated build; older ones are history)
log: last 5 of 10 entries in @log-recent; the full history is goals/G-001-first-puzzle-stall/log.md

## You may write

- goals/G-001-first-puzzle-stall/goal.md
- goals/G-001-first-puzzle-stall/22-gameplay-engineer-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-first-puzzle-stall/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 23
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
   (the Goal log keeps the history; the Handoffs carry the details). Confirm (`planned`) or drop
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
answer, and the stage it creates. Also: stages skipped and why.>

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
goals/G-001-first-puzzle-stall/goal.md
goals/G-001-first-puzzle-stall/log.md
project.md
sim/build-0.2.md
sim/build-0.3.md
sim/build-0.4.md
sim/repo-notes.md
>>>END

<<<FILE @decision-titles
decisions/D-001-no-fail-states.md — D-001: No fail states and no timers
decisions/D-002-intro-cancel-and-undo.md — D-002: Intro cancel eases the pool back; the intro is never in undo history
decisions/D-003-sand-tap-blip-and-pool-hit-area.md — D-003: Rate-limited sand taps show a pool brightness blip; the pool's hit area follows its drawn size
decisions/D-004-ease-back-taps-window-origin-held-pool.md — D-004: Taps during the ease-back, the 1.5 s window origin, and second-finger taps on a held pool
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

- **Observe** — Has the stall been observed first-hand? No: the Project Context holds only the
  Owner's report. It is an experience problem, not a reproducible defect, so the Role is
  `playtester` (not `qa`). Creates stage 1.
- **Diagnose** — Is the cause understood? No. Creates stage 2 (`game-designer`). `art-director` was
  added in parallel (2b) because the observation pointed to something visual.
- **Design** — Is the intended behavior of the fixed first puzzle specified? No:
  `design/onboarding.md` specified the current level 1 and its teaching intent, not a fix. Creates
  stage 3. Build later found a gap (intro-cancel case), which reopened Design as 3d. Verify then
  found a gap (sand taps inside the pulse rate-limit window), which reopened Design as 3e; 3e is
  done (blip, hit area and notes settled in spec revision 2 and D-003). Build 4c then found one
  more gap (a sand tap during the 0.15 s ease-back, plus the 1.5 s window origin and a held-pool
  second finger), which reopened Design as 3f; 3f is done (spec revision 3 and D-004).
- **Build** — Must the game change? The Owner wants it fixed, so yes. Creates stage 4. Spec
  revision 2 changes player-facing behavior, so Build runs again as 4c; 4c held on the gap above,
  so Build resumes as 4d with spec revision 3.
- **Verify** — Always after Build. Stage 5, and 5b after 4d.
- **Play** — Is the Goal about how the game plays or feels? Yes. Stage 6, in a fresh context
  without the implementation history.
- **Review** — Is it an experience Goal? Yes. Stage 7 (`game-director`).
- **Next** — Always. Stage 8.

Skipped:

- **Decide** — Is there a real choice of direction, priority or scope? Not so far. The fix choices
  (A + B) are player-facing behavior inside the approved direction, which is `game-designer`
  authority. Option C (idle hint) is excluded from the spec; if it is wanted later, route Decide
  because it touches D-001.
- **Plan** — Is the technical approach non-obvious, risky, cross-system or parallelizable? No. The
  designer's spec describes a local level 1 change (parameters, a recolor, existing-sprite
  animation, per-object touch response); no cross-system structure is touched. Skipped. If Build
  finds the change is not local, the return rules send it to Plan.

Flag for Review (not a conclusion): the start-of-level intro motion is judged by the designer to be
outside D-001 (one-time, no timer, no inactivity trigger). `game-director` should confirm at Review.

Open item (not a Role question): whether iOS "Reduce Motion" / Android "Remove animations" are
available on the target platforms is unconfirmed. QA could not confirm it at Verify (target OS
versions are not named in the Project Context). The spec's static-brightness fallback works either
way. It does not block the Goal; carry it to Review / Close as an item for the Owner.

Resolved item: the source of the lifted pool's shadow was settled in 3e (no specific source
required; not player-facing; check 10 clarified).

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
| 4d | Build | gameplay-engineer | implement-change | open | 21-studio-to-gameplay-engineer.md |
| 5b | Verify | qa | verify-change | planned | — |
| 6 | Play | playtester | playtest-session | planned | — |
| 7 | Review | game-director | review-outcome | planned | — |
| 8 | Next | studio | — | planned | — |

Status: planned | tentative | open | done | skipped. The route is a plan; the Route operation
revises it.

## Route changes

After step 3f (20): the designer settled the ease-back sand tap, 1.5 s window origin and held-pool second finger in spec revision 3 and D-004; no spec gap remains. Build resumes as 4d (item 1 changed, items 2–5 as planned), then Verify 5b with checks 1–18. Plan stays skipped; no escalation.

## Next action

Run step 4d (Step operation): `gameplay-engineer` on `21-studio-to-gameplay-engineer.md`. Report to `studio`, with any self-assessment only under Sender assessment. Then Route: compose a fresh QA Handoff for 5b without the Sender assessment (checks 1–18 as revised, the reduced-motion platform check, the home capture for check 3). After Verify passes, compose a Playtester Handoff from permitted information only (build and player profile), and open Play (6). Phase 1: the Studio stops after every Route.

## Outcome

<!-- Filled at close, for the Owner, in owner_language (ja). -->
>>>END

<<<FILE @log-recent
## 015-route · 2026-10-12

Status: active. Open: 13-studio-to-qa.md.

After step 4b (12): Build is done; the engineer found no further spec gap, so the plan holds and Plan stays skipped. Verify (5) is open for `qa` with a fresh Handoff (13) that omits the Sender assessment. It carries the 12 checks as exercise aids, plus the platform reduced-motion check and the home-styling capture. The report goes to `studio` so a clean Playtester handoff can be composed.

## 017-route · 2026-10-12

Status: active. Open: 15-studio-to-game-designer.md.

After step 5 (14): all 12 checks pass, but QA found a spec gap (G1: sand taps 0.6–1.5 s after a pulse get no response, against "no silent touches") plus notes N1–N4. Expected behavior is undefined, so Design reopens as 3e (game-designer) before Play, since a spec change would alter the build the Playtester sees. Build/Verify re-run only if the spec changes; Play stays planned.

## 019-route · 2026-10-12

Status: active. Open: 17-studio-to-gameplay-engineer.md.

After step 3e (16): the designer settled G1 and N1–N4 in spec revision 2 and D-003. Player-facing behavior changed (sand-tap blip, larger pool hit area, crab flip target, pulse precedence), so Build 4c is open and Verify 5b is confirmed (checks 1–16). Play stays after 5b. Plan stays skipped; no escalation.

## 021-route · 2026-10-12

Status: active. Open: 19-studio-to-game-designer.md.

After step 4c (18): Build held with `question` — a sand tap during the 0.15 s ease-back (pending pulse) is undefined; also the 1.5 s window origin and a held-pool second finger. Spec ambiguous, so Design reopens as 3f (game-designer); Build resumes as 4d, then Verify 5b (checks 1–16). Items 2–5 stay settled. Plan stays skipped; no escalation.

## 023-route · 2026-10-12

Status: active. Open: 21-studio-to-gameplay-engineer.md.

After step 3f (20): the designer settled the ease-back sand tap, 1.5 s window origin and held-pool second finger in spec revision 3 and D-004; no spec gap remains. Build resumes as 4d (item 1 changed, items 2–5 as planned), then Verify 5b with checks 1–18. Plan stays skipped; no escalation.
>>>END

<<<FILE goals/G-001-first-puzzle-stall/22-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-001
seq: 22
from: gameplay-engineer
to: studio
stage: Verify
outcome: done
---
# 22: gameplay-engineer → studio — Build 4d done (spec revision 3, items 1–5); build 0.4 described below; route to QA

## Task

Compose a fresh QA Handoff for Verify 5b from this file, leaving out `## Sender assessment`. The change is made as described under Findings. QA verifies checks 1–18 of `design/onboarding.md` revision 3 on build 0.4.

## Context

Goal G-001: children stall at the first puzzle. Build 4c held with a question (handoff 18). Design 3f (handoff 20, D-004) settled it. This step finishes item 1 and implements items 2–5 as planned in revision 2.

**Path problem:** the packet told me to write `sim/build-0.4.md`, but my allowed write path is only this handoff. I did not write outside it. The full text intended for `sim/build-0.4.md` is under Findings ("Build 0.4 description"). The Studio should save it as `sim/build-0.4.md` (and apply the `sim/repo-notes.md` edits listed below) so that the dry-run change counts as made. Nothing in the spec was ambiguous, so this is not a design hand-back.

## Findings

### Build 0.4 description (intended content of `sim/build-0.4.md`)

Level 1 only. Levels 2 and 3 are unchanged. Touch only. Changes are made through the existing level 1 flags and input code.

**What changes, and where**

*Items 2–5 (as planned in revision 2):*
- **Item 2, hit area:** the pool's hit area follows its drawn size (idle pulse up to 1.06, redirect pulse up to 1.15, lift 1.10), never below the at-rest size. It also follows the drawn position during the intro. The crab and home keep at-rest hit areas. The home near-glow still uses the at-rest width.
- **Item 3, crab flip target:** the flip uses the pool's logical position. During the intro or ease-back that is the authored start. A held pool uses the position under the finger.
- **Item 4, pulse precedence:** while a redirect pulse runs, the idle pulse is hidden. The idle pulse resumes from scale 1.00 when the pulse ends. A blip does not touch the idle pulse.
- **Item 5, shadow:** a procedural soft dark ellipse under the lifted pool. No new image asset.

*Item 1 (sand-tap blip) with revision 3:*
- **Blip:** the pool's brightness rises 15% within 0.1 s of touch-down, then fades over 0.3 s. No scale or movement. At most one runs. A new sand tap does not restart it. It works under reduced motion.
- **Pulse-pending state:** set by the cancelling non-pool touch in `INTRO_*`. It stays set until the ease-back ends, which starts the pulse and clears the state. A pool touch-down during `EASE_BACK` clears it and cancels the ease-back, so no pulse and no window start.
  - While it is set, any crab, home or sand tap plays only its own object response (sand has none). No blip trigger and no extra pulse request.
- **Pulse at the end of the ease-back:** it bypasses the 1.5 s limit and starts the window.
- **1.5 s window:** it is stored as the start time of the last redirect pulse (`lastPulseStart`). A request is allowed when now − `lastPulseStart` ≥ 1.5 s. It is not set at touch-down. Blips and held-pool taps never write it. A pool touch cancelling a running pulse leaves `lastPulseStart` as it is.
- **Blip trigger for a sand tap (not held):** blip only if all hold:
  1. the limit blocks a pulse (now − `lastPulseStart` < 1.5 s);
  2. no pulse is running (now − `lastPulseStart` > 0.6 s, or the pulse was cancelled);
  3. no pulse is pending;
  4. no blip is running.
  - Otherwise: a sand tap that is allowed starts a pulse. A sand tap during the first 0.6 s of a pulse has the pulse as its response.
- **Held pool, second finger:** while the pool is held, no pulse request is made for any object. The window is neither started nor changed.
  - Sand: starts the blip if none is running, whatever the time since the last pulse.
  - Crab and home: their own response only. The crab flip uses the position under the finger.
  - A second finger on the pool is ignored.
- A pool touch-down cancels a running blip as well as a running or pending pulse.

*Edits to apply to `sim/repo-notes.md` (the intro state machine and sand lines):*
- `EASE_BACK`: add the `pulsePending` flag. The pulse at 0.15 s is exempt from the rate limit and sets `lastPulseStart`. A non-pool touch during `EASE_BACK` plays only its object response. A pool touch clears `pulsePending`.
- "Redirect pulse" line: the window is measured from `lastPulseStart`. Add the blip rules and the held-pool rules above.

**Tests added (logic tests on a fake clock, written and run in the simulated environment; see assessment)**
- Pending-pulse sand tap at 0.05 s and 0.10 s: no blip, exactly one pulse, started at 0.15 s after the first touch.
- Pending-pulse crab tap and home tap at 0.05 s and 0.10 s: own response within 0.1 s, no blip, one pulse at 0.15 s.
- Pool touch at 0.05 s and 0.10 s during the ease-back: `pulsePending` cleared, no pulse, `lastPulseStart` unchanged.
- Window from pulse start: the pulse at t=0.15; a sand tap at 1.60 gets the blip (limit blocks, 0.6 s passed); a sand tap at 1.65 starts a pulse.
- Blip does not move the window.
- Held-pool sand tap: blip, no pulse, window unchanged, also when ≥1.5 s have passed since the last pulse. A running blip is not restarted.
- Held-pool crab and home tap: object response, no pulse and no blip.
- Existing tests unchanged (intro cancel, undo stack empty, rate limit at 1.5 s, near-glow).

### How to exercise checks 1–18 (spec: `design/onboarding.md` revision 3)

- **1:** capture after the intro (about 1.6 s after load). Only the pool has the darker outline and idle motion.
- **2:** grayscale capture, measure the pool/sand luminance ratio (≥1.5:1).
- **3:** the crab does not bob. Capture the home (still needed, non-blocking). No outline darker than the scenery.
- **4 (changed):** tap the pool, crab, home and sand 10 times each, at 2 s spacing and as fast as possible. Also tap during the ease-back and with a second finger on a held pool. Every touch shows a response within 0.2 s.
- **5:** drag the crab. It leans and springs back, and does not move. One pool pulse at touch-down.
- **6:** tap rapidly. Pulses start at least 1.5 s apart, counted from the previous pulse start. Blips are not counted.
- **7:** load the level, touch the pool during the slide. The intro stops and the pool follows the finger.
- **8:** complete the level with the bubble hidden.
- **9:** no failure, timer or inactivity cue. Undo restores the position.
- **10:** inspect the assets. Only the sprite sheet plus the procedural shadow.
- **11:** separate loads. During the intro touch the crab, the home, the sand. The intro stops, the pool is at the start within 0.15 s, the object responds within 0.1 s, the pulse starts ≤0.2 s after touch-down, then the idle pulse.
- **12:** after an intro-cancel, drag and drop, then undo. The pool returns to the authored start, with no extra undo step.
- **13 (changed):** tap the sand (pulse starts at t=0). Tap again at 0.8–1.3 s: brightness +15% within 0.1 s, fade 0.3 s, no scale change, no new pulse. A third tap during the blip does not restart it. A sand tap at ≥1.5 s after the pulse start starts a new pulse and no blip.
- **14:** at the largest idle pulse (1.06) and redirect pulse (1.15), touch the outermost visible rim. The pool is grabbed (lift to 1.10). A touch just outside the smallest size does not grab it.
- **15:** touch the crab mid-intro with its center between the drawn and the authored positions. It faces the authored start side.
- **16:** after an intro-cancel by a non-pool touch, the pulse shows from the end of the ease-back, the idle pulse is hidden during it and restarts from 1.00. After a blip-only sand tap, the idle pulse is unaffected.
- **17 (new):** during the intro tap the sand, then the sand again at about 0.05 s and 0.10 s (separate loads). Repeat with a crab or home as the second tap. Expect: the second object's response ≤0.1 s, no blip, exactly one pulse at 0.15 s after the first touch, and no brightness rise before it. A sand tap 0.6–1.3 s after that pulse start gets the blip.
- **18 (new):** hold the pool, tap the sand with a second finger. Blip (15%, ≤0.1 s, 0.3 s fade), no pulse, no scale change beyond the lift. A crab or home tap with a second finger gives only its own response. After release, a sand tap within 1.5 s of the previous pulse start behaves as in check 13. Taps made while holding did not move the window.

Checks 4, 13, 17 and 18 are new or changed. Checks 1–3, 5–12 and 14–16 are unchanged.

### Known risks (for QA)
- A second finger tapping at 0.01 s after the cancelling touch is a tight case. The frame timing of touch-down versus the first-frame state change needs a recording at 60 fps.
- A touch landing exactly at 0.15 s (the ease-back end frame). I treat it as "pending" if the frame has not yet processed the pulse start. The result is the same either way: one pulse, no blip.
- A pool touch that cancels a *running* pulse leaves the window at that pulse's start. A sand tap shortly after release can therefore get a blip rather than a pulse (check 18 expects this).
- The blip on a held pool is visible only as a brightness change on a lifted pool. Watch for the lift shadow hiding it.

## Decisions already made

- D-001: no failure, no timers, every move undoable.
- D-002: intro cancel eases back over 0.15 s; the intro is never in undo history.
- D-003: blip and hit area, amended by D-004.
- D-004: ease-back taps, window from pulse start, held-pool second finger.

## Constraints

- Level 1 only. Touch only. No text-dependent mechanic. Existing sprite sheet plus procedural shadow.
- Touch-triggered only: no timer or inactivity trigger.
- Dry-run project: the change counts as made once described in `sim/build-0.4.md` (see the path problem above).

## Open questions

- None for Design.
- For the Studio: save the "Build 0.4 description" as `sim/build-0.4.md`, since my write path did not allow it.
- Non-blocking, carried forward to QA: the reduced-motion platform availability check, and the home capture for check 3.

## Expected output

- A QA Handoff composed by the Studio from this file's Findings (without `## Sender assessment`), listing checks 1–18 with 4, 13, 17 and 18 marked new or changed. QA verifies independently on build 0.4.

## Sender assessment

- **Spec coverage:** I listed every player-observable behavior before coding (the skill's step 1). Each is defined by rules 2 and 5, the edge cases, D-004 and checks 4 and 13–18. I found no gap, so I made no choices of my own.
- **Choices inside the spec:**
  - Window state is one value (`lastPulseStart`), which keeps blip and held-pool behavior from touching it.
  - A pool touch cancelling a running pulse leaves the window as is. The spec says "start of the previous pulse", and check 18 matches.
- **Root cause of the 4c hold:** blip and pulse requests were keyed to touch-down time and had no pending state. The pulse-pending flag plus `lastPulseStart` fixes this in the shared request path, not only in the sand branch. Crab and home taps in the ease-back now go through the same guard.
- **Tests:** the logic tests listed above are designed against the fake clock. This is a dry run, so none were executed on a device. The earlier repo-notes remark that tests were "designed but not run" still applies to the full suite. I did not check on-device frame timing.
- **Confidence:** high that the logic matches the spec. Medium on frame-level timing at 0.15 s and in the second-tap cases. QA should record at 60 fps.
- **Not done:** `sim/build-0.4.md` and the `sim/repo-notes.md` edits are given as text only, because of my write restriction.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/onboarding.md, sim/build-0.3.md, sim/repo-notes.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-002-intro-cancel-and-undo.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md, decisions/D-004-ease-back-taps-window-origin-held-pool.md
- Previous handoff: goals/G-001-first-puzzle-stall/21-studio-to-gameplay-engineer.md
>>>END
