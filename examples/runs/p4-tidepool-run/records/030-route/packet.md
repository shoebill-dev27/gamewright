# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-first-puzzle-stall/26-game-designer-to-studio.md
next_seq: 27
context_request: allowed once (@need, up to 8 paths)
current_build: sim/build-0.4.md (newest simulated build; older ones are history)
log: last 5 of 12 entries in @log-recent; the full history is goals/G-001-first-puzzle-stall/log.md

## You may write

- goals/G-001-first-puzzle-stall/goal.md
- goals/G-001-first-puzzle-stall/26-game-designer-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-first-puzzle-stall/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 27
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
decisions/D-005-reduce-motion-pulse-fills-window.md
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
decisions/D-005-reduce-motion-pulse-fills-window.md — D-005: Under reduce-motion the redirect pulse is a 0.6 s two-beat brightness pulse
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
  second finger), which reopened Design as 3f; 3f is done (spec revision 3 and D-004). Verify 5b
  then found that the spec's "pulse is already the response" window (0.6 s) is longer than the
  reduce-motion pulse (about 0.4 s), leaving a silent sand tap window; Design reopens as 3g
  (spec revision 4).
- **Build** — Must the game change? The Owner wants it fixed, so yes. Creates stage 4. Spec
  revision 2 changes player-facing behavior, so Build runs again as 4c; 4c held on the gap above,
  so Build resumed as 4d with spec revision 3; 4d is done (build 0.4). Spec revision 4 will change
  reduce-motion behavior, so Build runs again as 4e.
- **Verify** — Always after Build. Stage 5, 5b after 4d, and 5c after 4e.
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
  finds the change is not local, the return rules send it to Plan. If check 4 fails a second time
  at 5c, route to `technical-director` (loop limit).

Flag for Review (not a conclusion): the start-of-level intro motion is judged by the designer to be
outside D-001 (one-time, no timer, no inactivity trigger). `game-director` should confirm at Review.

Open item (not a Role question): whether iOS "Reduce Motion" / Android "Remove animations" are
available on the target platforms is unconfirmed. QA could not confirm it at Verify (target OS
versions are not named in the Project Context). The spec's static-brightness fallback works either
way. It does not block the Goal; carry it to Review / Close as an item for the Owner.

Open item (non-blocking): QA has no real image of the home styling or a 60 fps recording; checks
2, 3, 11, 17 and 18 rest on the build record's stated values. Carry to Review / Close.

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
| 4d | Build | gameplay-engineer | implement-change | done | 21-studio-to-gameplay-engineer.md (result: 22, build 0.4) |
| 5b | Verify | qa | verify-change | done | 23-studio-to-qa.md (fail: check 4 under reduce-motion; report: 24) |
| 3g | Design | game-designer | write-design-spec | open | 25-studio-to-game-designer.md |
| 4e | Build | gameplay-engineer | implement-change | planned | — |
| 5c | Verify | qa | verify-change | planned | — |
| 6 | Play | playtester | playtest-session | planned | — |
| 7 | Review | game-director | review-outcome | planned | — |
| 8 | Next | studio | — | planned | — |

Status: planned | tentative | open | done | skipped. The route is a plan; the Route operation
revises it.

## Route changes

After step 5b (24): 17 of 18 checks pass; check 4 fails under reduce-motion (a sand tap 0.4–0.6 s after a pulse start is silent). Spec rule 5's 0.6 s window conflicts with the 0.4 s reduce-motion pulse, so the mechanism is a design choice: Design reopens as 3g (game-designer), then Build 4e and Verify 5c. First failure of check 4, so no Plan; no escalation. Play and Review wait for the corrected build.

## Next action

Run step 3g (Step operation): `game-designer` on `25-studio-to-game-designer.md`, reporting to `studio` with spec revision 4 and, if significant, D-005. Then Route: open Build 4e (`gameplay-engineer`) with the revised spec, then Verify 5c (`qa`, fresh Handoff without Sender assessment, checks 1–18 plus any new). If check 4 fails again, route to `technical-director`. After a clean 5c, compose a Playtester Handoff from permitted information only (build and player profile; no change, no expected result). Carry the reduce-motion platform availability, the home capture and the 60 fps recording forward as non-blocking items. Phase 1: the Studio stops after every Route.

## Outcome

<!-- Filled at close, for the Owner, in owner_language (ja). -->
>>>END

<<<FILE @log-recent
## 019-route · 2026-10-12

Status: active. Open: 17-studio-to-gameplay-engineer.md.

After step 3e (16): the designer settled G1 and N1–N4 in spec revision 2 and D-003. Player-facing behavior changed (sand-tap blip, larger pool hit area, crab flip target, pulse precedence), so Build 4c is open and Verify 5b is confirmed (checks 1–16). Play stays after 5b. Plan stays skipped; no escalation.

## 021-route · 2026-10-12

Status: active. Open: 19-studio-to-game-designer.md.

After step 4c (18): Build held with `question` — a sand tap during the 0.15 s ease-back (pending pulse) is undefined; also the 1.5 s window origin and a held-pool second finger. Spec ambiguous, so Design reopens as 3f (game-designer); Build resumes as 4d, then Verify 5b (checks 1–16). Items 2–5 stay settled. Plan stays skipped; no escalation.

## 023-route · 2026-10-12

Status: active. Open: 21-studio-to-gameplay-engineer.md.

After step 3f (20): the designer settled the ease-back sand tap, 1.5 s window origin and held-pool second finger in spec revision 3 and D-004; no spec gap remains. Build resumes as 4d (item 1 changed, items 2–5 as planned), then Verify 5b with checks 1–18. Plan stays skipped; no escalation.

## 026-route · 2026-10-12

Status: active. Open: 23-studio-to-qa.md.

After step 4d (22): Build is done as build 0.4 (spec revision 3, items 1–5); the engineer found no spec gap, so Plan stays skipped and nothing escalates. Verify 5b is open for `qa` with a fresh Handoff (23) that omits the Sender assessment and lists checks 1–18 (4, 13, 17, 18 new or changed). The report goes to `studio`; Play and Review stay planned.

## 028-route · 2026-10-12

Status: active. Open: 25-studio-to-game-designer.md.

After step 5b (24): 17 of 18 checks pass; check 4 fails under reduce-motion (a sand tap 0.4–0.6 s after a pulse start is silent). Spec rule 5's 0.6 s window conflicts with the 0.4 s reduce-motion pulse, so the mechanism is a design choice: Design reopens as 3g (game-designer), then Build 4e and Verify 5c. First failure of check 4, so no Plan; no escalation. Play and Review wait for the corrected build.
>>>END

<<<FILE goals/G-001-first-puzzle-stall/26-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 26
from: game-designer
to: studio
stage: Build
outcome: done
---
# 26: game-designer → studio — reduce-motion silent-touch window closed (spec revision 4, D-005)

## Task

Route Build for spec revision 4 (reduce-motion only), then Verify. Default-mode behavior does not change.

## Context

Goal G-001. QA (handoff 24) found check 4 failing only with the OS reduce-motion setting on: a sand tap 0.4–0.6 s after a pulse start showed nothing (F1). Handoff 25 asked for the mechanism and an answer on S1. I chose the mechanism, did the pass over the other reduce-motion windows, and wrote `design/onboarding.md` revision 4 and D-005. D-001 is not touched, no idle or inactivity cue is added, and the vision holds, so no escalation to `game-director` is needed.

## Findings

**Mechanism (F1):** under reduce-motion the redirect pulse is a brightness double-beat on the pool: each beat rises to +30% by 0.1 s after its start and returns to 0 by 0.3 s after its start; beat 2 starts 0.3 s after beat 1; total 0.6 s; no scale change, no movement. It replaces the earlier brightness change of about 0.4 s. The pulse now fills the same 0.6 s as the default pulse, so rule 5 condition (2) and the 1.5 s / 0.6 s timings are unchanged and the "pulse is already the response" assumption of D-003 holds in both modes.

**S1:** acceptable. The pulse and the flash differ in count (two beats against one) and height (+30% against +15%). No new art.

**Player-facing changes, reduce-motion on only:**
1. Redirect pulse: two beats of +30% over 0.6 s (was one change of about 0.4 s).
2. Overlap rule: the pool shows the larger of the active brightness changes, never the sum. A pulse that starts while a flash is fading ends the flash. This case can occur at a sand tap at 1.5 s or later while a flash from a tap just before is still fading.
3. Idle brightness change specified: one slow rise of at most +8% and back per 2.0 s, hidden during a pulse, resuming from 0. If the build already uses a different amount, the engineer reconciles it to this. Keep it lower and slower than the flash.
4. Crab wiggle and lean: a brightness change on the crab of about 0.4 s, 0 to +20% and back. The crab does not move. The flip stays instant.

**Pass over the other windows (revision 4 edge case):**
- Ease-back, pending pulse, post-intro-cancel, second tap during the ease-back: do not arise, because the intro is skipped. The first non-pool touch of the load starts a pulse within 0.2 s, as no previous pulse exists.
- Held-pool second finger: unchanged. Sand gives the +15% flash, crab and home give their own response, no pulse. No silent case.
- Flash timing: unchanged (+15% within 0.1 s, 0.3 s fade, not restarted while running). The blip window starts at 0.6 s or later after the pulse start, the same as the default and the build.
- Home glow (already brightness) and the pool grab (lift 1.10, shadow): unchanged.
- No other silent-touch case found.

**Checks:**
- Changed: 4 (now explicitly holds in both modes), 13 (holds with reduce-motion on), 14, 16 and 18 (mode notes), 5, 11, 15 and 17 (annotated as default-mode or noting the reduce-motion form).
- New: 19 (reduce-motion sweep: sand tap every 0.1 s from 0 to 1.4 s after a pulse start, none silent), 20 (reduce-motion pulse shape: two beats, +30%, 0.3 s each, 0.6 s total, no scale, larger-of-not-sum).
- Unchanged in content: 1–3, 6–10, 12.

**Needs a 60 fps capture:** the beat shape and the dip between beats (checks 19, 20), plus the earlier tight-timing cases of checks 11, 17 and 18 (QA's S3).

## Decisions already made

- D-001: holds. No failure, timer or inactivity cue.
- D-002: unchanged.
- D-003: its "pulse is already the response" assumption now holds in reduce-motion too; D-005 amends it for that mode. Blip and hit area unchanged.
- D-004: unchanged.
- D-005 (new): the reduce-motion pulse is a 0.6 s two-beat brightness pulse.
- Revision 3 items 1–5 and all default-mode behavior: not reopened.

## Constraints

- Level 1 only. Touch only. No text dependence. Existing sprite sheet plus the procedural shadow.
- Default-mode behavior must not change. QA must re-run checks 13 and 16 in the default mode as regression.
- Studio rule from QA: this is the first failure of check 4 in this form. If check 4 fails again after this fix, route to `technical-director`.

## Open questions

- Remaining gap (non-blocking): a tap in the last ~0.05 s of a pulse (0.55–0.6 s) sees only the tail of beat 2, in both modes. This matches the accepted default-mode behavior. A 60 fps capture will show whether it reads as a silent touch.
- Not mine to answer: whether the setting exists and is readable on the target OS versions. The mechanism relies on it being readable. Where it is not, the full motion is shown and the reduce-motion rules do not apply. The Studio should name the target platforms and versions.
- The home styling capture (check 3) is still open from handoff 24.

## Expected output

- Build (`gameplay-engineer`): implement the reduce-motion changes above and state them exactly in the handoff, including how to exercise them with the setting on (the sweep in check 19). Then Verify (QA): re-run check 4 under reduce-motion, new checks 19 and 20, and checks 13, 16, 18 in both modes.
- The Playtester receives only the observation list from handoff 24, not this handoff.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: none
- Project: design/onboarding.md, sim/build-0.4.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md, decisions/D-004-ease-back-taps-window-origin-held-pool.md, decisions/D-005-reduce-motion-pulse-fills-window.md
- Previous handoff: goals/G-001-first-puzzle-stall/25-studio-to-game-designer.md
>>>END
