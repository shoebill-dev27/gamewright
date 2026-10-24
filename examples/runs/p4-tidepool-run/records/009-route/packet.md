# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-first-puzzle-stall/09-gameplay-engineer-to-game-designer.md
next_seq: 10
context_request: allowed once (@need, up to 8 paths)
current_build: sim/build-0.2.md (newest simulated build; older ones are history)
log: last 3 of 3 entries in @log-recent; the full history is goals/G-001-first-puzzle-stall/log.md

## You may write

- goals/G-001-first-puzzle-stall/goal.md
- goals/G-001-first-puzzle-stall/09-gameplay-engineer-to-game-designer.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-first-puzzle-stall/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 10
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
goals/G-001-first-puzzle-stall/goal.md
goals/G-001-first-puzzle-stall/log.md
project.md
sim/build-0.2.md
sim/repo-notes.md
>>>END

<<<FILE @decision-titles
decisions/D-001-no-fail-states.md — D-001: No fail states and no timers
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
  stage 3.
- **Build** — Must the game change? The Owner wants it fixed, so yes. Creates stage 4.
- **Verify** — Always after Build. Stage 5.
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

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | playtester | playtest-session | done | 01-studio-to-playtester.md |
| 2 | Diagnose | game-designer | diagnose-experience | done | 02-playtester-to-game-designer.md |
| 2b | Diagnose | art-director | visual-review | done | 03-studio-to-art-director.md |
| 3 | Design | game-designer | write-design-spec | done | 06-studio-to-game-designer.md |
| 3c | Plan | technical-director | technical-plan | skipped | — |
| 4 | Build | gameplay-engineer | implement-change | open | 08-studio-to-gameplay-engineer.md |
| 5 | Verify | qa | verify-change | planned | — |
| 6 | Play | playtester | playtest-session | planned | — |
| 7 | Review | game-director | review-outcome | planned | — |
| 8 | Next | studio | — | planned | — |

Status: planned | tentative | open | done | skipped. The route is a plan; the Route operation
revises it.

## Route changes

After step 3 (07): the spec is written in `design/onboarding.md` (options A + B, no Option C). Plan is skipped: the change is local to level 1. Build (4) is open for `gameplay-engineer`. Verify must be addressed to `studio` so a fresh Playtester handoff can be composed afterward. The intro-motion vs D-001 judgment is left for Review.

## Next action

Run step 4 (Step operation): `gameplay-engineer` on `08-studio-to-gameplay-engineer.md`, stating the exact change in its Handoff and addressing the result to `studio` (outcome `done`). Then Route, which composes the QA Verify handoff (without the Sender assessment). Phase 1: the Studio stops after every Route.

## Outcome

<!-- Filled at close, for the Owner, in owner_language (ja). -->
>>>END

<<<FILE @log-recent
## Before the log

- Intake check (Route step 4) on 01: the first draft told the Playtester the Owner's report and
  asked "where do players stall", which primes the observation. Rewritten with a neutral play focus
  (levels 1–3) and the Owner's report withheld. Load narrowed to `project.md#player-profile`.
- Route after step 1 (`02-playtester-to-game-designer.md`): the outcome fits the plan (two of three
  children stalled 20–35 s at the start of level 1; the report is observation only). No escalation
  trigger fires, and no `tentative` stage exists to confirm or drop. Added step 2b: `art-director`
  `visual-review` in parallel with step 2, as the Intake note reserved for this point. The report
  contains visual facts (tide pool in the same pastel tone as the sand; crab with a darker outline
  that bobs; two of three children touched the crab first), so the cause may be visual. Steps 2 and
  2b are independent (both read only the observation), so they run in parallel and Route waits for
  both before step 3. Step 2's handoff was completed at Route: the Owner's words, the success
  condition, the out-of-scope list and the text-constraint flag were added (the `game-designer` did
  not have them); `project.md#vision`, `#constraints`, `#player-profile`, `design/onboarding.md` and
  D-001 were put in its Load. Not added: a `qa` Observe step. The playtester reported the missing
  response to taps on the crab and the home as observed; whether that contradicts the design
  documents is for step 2 to say, and if it does, the return rules send that part to `qa`.
  Step 3 may need `art-director` for what the player sees; decide after step 2 and 2b.

## 005-route · 2026-10-12

Status: active. Open: 06-studio-to-game-designer.md.

After steps 2 and 2b: the diagnoses agree (pool lacks affordance, crab is a false affordance, silent touches, text-only teaching), so the plan holds. Design (3) is open for `game-designer`, who adopts the art-director's visual direction. Idle hint (Option C) is barred from the spec because it touches D-001; if wanted, route Decide. Plan is re-asked after Design. No `qa` Observe: Verify covers touch response.

## 007-route · 2026-10-12

Status: active. Open: 08-studio-to-gameplay-engineer.md.

After step 3 (07): the spec is written in `design/onboarding.md` (options A + B, no Option C). Plan is skipped: the change is local to level 1. Build (4) is open for `gameplay-engineer`. Verify must be addressed to `studio` so a fresh Playtester handoff can be composed afterward. The intro-motion vs D-001 judgment is left for Review.
>>>END

<<<FILE goals/G-001-first-puzzle-stall/09-gameplay-engineer-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 9
from: gameplay-engineer
to: game-designer
stage: Design
outcome: question
---
# 09: gameplay-engineer → game-designer — level 1 spec has a gap in the intro-cancel case; Build is held

## Task

Settle the intro-cancel gap below (Q1 and Q2) in `design/onboarding.md`, and accept or change the proposed defaults for the minor gaps (Q3–Q6). Then return the spec to the Studio so Build can resume. No change has been applied to build 0.2 and nothing goes to QA yet.

## Context

Goal G-001 (first-puzzle-stall). Handoff 08 asked for the level 1 opening spec to be implemented for build 0.2. Before coding I listed every player-observable behavior the spec produces and checked each against the spec. Most are fully defined. One case is not: what happens when a touch cancels the start-of-level intro and that touch is not on the pool. The spec also doesn't define the intro's relationship to undo history. Both change what the child sees, so they are not implementation details I may decide.

## Findings

**Blocked part (Q1, Q2).** Rule 2 says "Any touch-down during the intro cancels it at once, and the pool follows the finger from its current position." That only covers a touch on the pool. The edge case "Touch during the intro" just points back to rule 2.

**Q1. A touch-down on the crab, the home or the sand during the intro (about 1.6 s window).**

Rule 2 says any touch cancels the intro. Rules 3–5 say those touches wiggle/glow and trigger the redirect pulse. Undefined:
- (a) Where does the pool end up after the cancel?
- (b) Does the idle pulse start from there?
- (c) Does the touched object's normal response and the redirect pulse play on top of the cancel?
- Option A: the pool stays where it is mid-slide.
  - Cost: low. The cancel just stops the tween.
  - Side effects: the pool rests off its authored start position. The "home glows within 1.5 pool-widths" check may trigger at rest if the start is near the home. See Q2.
- Option B: the pool eases back to its authored start position (about 0.2 s) and the idle pulse starts there.
  - Cost: low to medium. It needs one extra short tween.
  - Side effects: the touched object's response and the redirect pulse (which also moves the pool's scale) play while the pool is moving. Say whether the redirect pulse waits for the ease-back.
- Option C: ignore non-pool touches during the intro (the intro keeps playing).
  - Cost: lowest.
  - Side effects: contradicts "any touch cancels" and "every touch gets a visible response within 0.2 s", unless the crab/home still respond.
- My proposal, not applied: Option B. The crab/home reaction plays at once, the redirect pulse is allowed to start after the ease-back, and the 0.2 s pulse window then applies from the end of the ease-back. This needs your acceptance because it changes the "within 0.2 s" criterion for this case.

**Q2. Does the intro move enter the undo history and the pool's logical position?**

Rule 1 says undo restores the previous position, and the edge case says undo does not replay the intro.
- Undefined: if the pool is left displaced (Option A), is the displaced position its first undo state or is the authored start position?
- Proposed default: the intro is a visual offset only and never pushes a history entry. The pool's logical position is always the authored start until a real drag is dropped, and undo returns to that.

**Minor gaps with proposed defaults (none applied until you accept):**

- **Q3. "Turns to face the pool" (crab, rules 3).** The permitted effects are scale, rotation, position and brightness. Default: a horizontal flip (scale x −1) of the existing sprite where the pool is on the other side, plus the ±8° wiggle. Alternative: rotation only, no flip.
- **Q4. "Within 1.5 pool-widths of the home" (rule 4).** Default: measured center-to-center, using the pool's at-rest width. Alternative: edge-to-edge.
- **Q5. Touch-down on the pool during a redirect pulse (rules 1 and 5).** Default: touch-down wins. The pulse is cancelled and the 1.10 lift applies from the current scale.
- **Q6. Header says "for build 0.3"; the Handoff 08 task says build 0.2.** Default: treat as the next build after 0.2, level 1 only.

**Open questions from Handoff 08 (answers):**

1. **Touch on crab and home:** per `sim/repo-notes.md`, "only tide pools respond to touch... Touches on creatures and homes are ignored." So the current state is no handler for those pieces. Input is not blocked. This does not change the spec.
2. **Home's current styling:** I cannot capture it from the packet. Per repo-notes, each piece names an outline style and an idle animation in the level data. When Build resumes I will set the level 1 home to the scenery outline style and no idle animation. That satisfies the spec whatever the current value is. A real capture is still needed at Verify (spec check 3).
3. **Reduced-motion setting:** I cannot confirm availability on target platforms from the packet. Nothing in `project.md` or repo-notes names the platforms' accessibility settings. This stays open and needs a platform check (iOS "Reduce Motion", Android "Remove animations"). The spec's static-brightness fallback is implementable either way. If the setting is not available on a platform, the fallback is simply unreachable there. I will read the OS flag where it exists and will not add an in-game toggle, which would be a scope change.

## Decisions already made

- D-001 (no failure, no timers, every move undoable) applies. None of the options above add a timer or an irreversible step. Q2's default keeps undo intact.

## Constraints

- Level 1 only. Existing sprite sheet only. Touch only. No dependence on reading text. No timers or inactivity triggers.
- The role forbids me from interpreting the spec or applying a default before you accept it.

## Open questions

- Q1 and Q2 (blocking): decide the cancel behavior and the undo relationship. Choose one of Options A–C, or another.
- Q3–Q6 (minor): accept the proposed defaults or change them.
- Platform reduced-motion availability: needs someone with platform access. The Studio decides who. It does not block your spec edit.
- Not blocked: everything else in the spec is fully defined. Once Q1–Q2 are settled the work is local, as the spec says.

## Expected output

An updated spec section in `design/onboarding.md` answering Q1–Q6, then a Handoff to `studio` to route Build again. On re-entry I implement the whole spec and hand the change to QA. What can proceed once unblocked, none of it affected by any answer:
- pool recolor, outline and idle pulse;
- touch-down lift;
- crab tap/drag responses and demotion;
- home glow;
- the redirect pulse with its 1.5 s rate limit;
- edge cases other than the intro cancel.

I held all of it back from the Handoff on purpose. In the dry run, stating a change counts it as made, and I don't want a partial level 1 to reach QA.

## Sender assessment

Confidence is high that Q1 and Q2 are real gaps. A 7–10 child tapping the crab in the first 1.6 s is likely, since the playtest children tapped the crab first. So the case will occur in the re-playtest, and the answer decides what they see. Confidence is medium that Option B is the best for the child, because it keeps the scene identical across children. Option A is simpler and equally safe under D-001. The root-cause reasoning from the diagnosis is unchanged by this question.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#constraints, project.md#art-direction, design/onboarding.md, sim/build-0.2.md
- Decisions: decisions/D-001-no-fail-states.md
- Previous handoff: goals/G-001-first-puzzle-stall/08-studio-to-gameplay-engineer.md
>>>END
