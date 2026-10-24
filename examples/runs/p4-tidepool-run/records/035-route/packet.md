# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-first-puzzle-stall/30-qa-to-studio.md
next_seq: 31
context_request: allowed once (@need, up to 8 paths)
current_build: sim/build-0.5.md (newest simulated build; older ones are history)
log: last 5 of 14 entries in @log-recent; the full history is goals/G-001-first-puzzle-stall/log.md

## You may write

- goals/G-001-first-puzzle-stall/goal.md
- goals/G-001-first-puzzle-stall/30-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-first-puzzle-stall/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 31
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
goals/G-001-first-puzzle-stall/27-studio-to-gameplay-engineer.md
goals/G-001-first-puzzle-stall/28-gameplay-engineer-to-studio.md
goals/G-001-first-puzzle-stall/29-studio-to-qa.md
goals/G-001-first-puzzle-stall/30-qa-to-studio.md
goals/G-001-first-puzzle-stall/goal.md
goals/G-001-first-puzzle-stall/log.md
project.md
sim/build-0.2.md
sim/build-0.3.md
sim/build-0.4.md
sim/build-0.5.md
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
  then found that the spec's "pulse is already the response" window (0.6 s) was longer than the
  reduce-motion pulse (about 0.4 s), leaving a silent sand tap window; Design 3g is done (spec
  revision 4 and D-005: the reduce-motion pulse is a 0.6 s two-beat brightness pulse). No spec gap
  blocks work now; two non-blocking notes from Build 4e are listed below.
- **Build** — Must the game change? The Owner wants it fixed, so yes. Creates stage 4. Spec
  revision 2 changes player-facing behavior, so Build runs again as 4c; 4c held on the gap above,
  so Build resumed as 4d with spec revision 3; 4d is done (build 0.4). Spec revision 4 changes
  reduce-motion behavior, so Build ran again as 4e; 4e is done (build 0.5).
- **Verify** — Always after Build. Stage 5, 5b after 4d, and 5c after 4e (checks 1–20, open).
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
available and readable on the target platforms is unconfirmed. The Project Context names no target
OS versions. The spec's fallback (full motion where the setting is not readable) works either way.
It does not block the Goal; carry it to Review / Close as an item for the Owner.

Open item (non-blocking): QA has no real image of the home styling or a 60 fps recording; checks
2, 3, 11, 17, 18, 19 and 20 rest on the build record's stated values. The pulse tail (0.55–0.6 s)
is also unseen on a capture. Carry to Review / Close.

Open item (non-blocking, from Build 4e, handoff 28): (a) under reduce-motion the crab brightness
change is built as one 0.4 s change at touch-down; the spec does not say whether it should be held
while the finger is down; (b) check 20's wording mentions a "0.3 s dip" between beats, but the
numbers give a return to 0 at 0.3 s with no dip. If QA reports either as a discrepancy, route to
`game-designer`; otherwise carry to Review.

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
| 3g | Design | game-designer | write-design-spec | done | 25-studio-to-game-designer.md (result: 26, spec rev 4, D-005) |
| 4e | Build | gameplay-engineer | implement-change | done | 27-studio-to-gameplay-engineer.md (result: 28, build 0.5) |
| 5c | Verify | qa | verify-change | open | 29-studio-to-qa.md |
| 6 | Play | playtester | playtest-session | planned | — |
| 7 | Review | game-director | review-outcome | planned | — |
| 8 | Next | studio | — | planned | — |

Status: planned | tentative | open | done | skipped. The route is a plan; the Route operation
revises it.

## Route changes

After step 4e (28): Build is done as build 0.5 (spec revision 4, changes 1–5); the engineer found no blocking spec gap, so Plan stays skipped and nothing escalates. Verify 5c is open for `qa` with a fresh Handoff (29) that omits the Sender assessment and lists checks 1–20 (19 and 20 new). Play and Review stay planned.

## Next action

Run step 5c (Step operation): `qa` on `29-studio-to-qa.md`, reporting to `studio` (Handoff 30). Then Route: on a clean pass, compose a Playtester Handoff from permitted information only (build and player profile; no change, no expected result) and open Play 6. If check 4 fails again, route to `technical-director` (loop limit). If QA reports the crab-hold or check 20 wording as a discrepancy, route to `game-designer`. Carry the reduce-motion platform availability, the home capture and the 60 fps recording forward as non-blocking items. Phase 1: the Studio stops after every Route.

## Outcome

<!-- Filled at close, for the Owner, in owner_language (ja). -->
>>>END

<<<FILE @log-recent
## 023-route · 2026-10-12

Status: active. Open: 21-studio-to-gameplay-engineer.md.

After step 3f (20): the designer settled the ease-back sand tap, 1.5 s window origin and held-pool second finger in spec revision 3 and D-004; no spec gap remains. Build resumes as 4d (item 1 changed, items 2–5 as planned), then Verify 5b with checks 1–18. Plan stays skipped; no escalation.

## 026-route · 2026-10-12

Status: active. Open: 23-studio-to-qa.md.

After step 4d (22): Build is done as build 0.4 (spec revision 3, items 1–5); the engineer found no spec gap, so Plan stays skipped and nothing escalates. Verify 5b is open for `qa` with a fresh Handoff (23) that omits the Sender assessment and lists checks 1–18 (4, 13, 17, 18 new or changed). The report goes to `studio`; Play and Review stay planned.

## 028-route · 2026-10-12

Status: active. Open: 25-studio-to-game-designer.md.

After step 5b (24): 17 of 18 checks pass; check 4 fails under reduce-motion (a sand tap 0.4–0.6 s after a pulse start is silent). Spec rule 5's 0.6 s window conflicts with the 0.4 s reduce-motion pulse, so the mechanism is a design choice: Design reopens as 3g (game-designer), then Build 4e and Verify 5c. First failure of check 4, so no Plan; no escalation. Play and Review wait for the corrected build.

## 030-route · 2026-10-12

Status: active. Open: 27-studio-to-gameplay-engineer.md.

After step 3g (26): the designer chose the reduce-motion mechanism (0.6 s two-beat brightness pulse, spec revision 4, D-005) and found no other silent window. Default-mode behavior is unchanged. Build 4e is open for `gameplay-engineer` (27), then Verify 5c (checks 1–20; 19 and 20 new). Plan stays skipped; no escalation.

## 033-route · 2026-10-12

Status: active. Open: 29-studio-to-qa.md.

After step 4e (28): Build is done as build 0.5 (spec revision 4, changes 1–5); the engineer found no blocking spec gap, so Plan stays skipped and nothing escalates. Verify 5c is open for `qa` with a fresh Handoff (29) that omits the Sender assessment and lists checks 1–20 (19 and 20 new). Play and Review stay planned.
>>>END

<<<FILE goals/G-001-first-puzzle-stall/30-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 30
from: qa
to: studio
stage: Route
outcome: pass
---
# 30: qa → studio — build 0.5 level 1 verification against checks 1–20 (spec revision 4): all 20 pass on the build record; one spec gap and three observations to route

## Task

Route the result of verifying build 0.5 (level 1). Checks 1–20 pass on the build record, with the limits below. Send the spec gap SG-1 and the check 20 wording discrepancy (O1) to `game-designer`. Ask for the device captures listed under "Unconfirmed".

## Context

Goal G-001, verification of `sim/build-0.5.md` against `design/onboarding.md` revision 4 (D-001, D-003, D-004, D-005). This is a dry-run project, so I read the build record against the spec and made no device capture or 60 fps recording. Every number below is what the build record states, not my measurement. Build 0.4 failed check 4 only under reduce-motion (F1, `24-qa-to-studio.md`). No implementer assessment was received.

## Findings

### Verdict per check

"Record" means the result rests only on the build record. "Capture" means a real device or 60 fps recording is still needed to confirm it.

| # | Mode | Result | Evidence and limits |
|---|------|--------|---------------------|
| 1 | both | PASS (record) | About 1.6 s after load in default mode, and from load under reduce-motion, only the pool has the darker outline and an idle effect. Default: scale pulse 1.00–1.06 over 2 s. Reduce-motion: brightness rise of up to +8% over 2 s. The crab does not bob and the home does not move. |
| 2 | both | PASS (record, thin margin, capture) | The build states about 1.8:1 in grayscale on the starting colors, against a threshold of 1.5:1. This is a stated value, not a pixel measurement. Re-measure on a real grayscale capture. The color difference is stated to remain under reduce-motion. |
| 3 | both | PASS (record; home capture needed) | The crab has the lighter outline and does not bob. The home has the lighter outline and no motion. Nothing else has a darker outline. The home styling comes from the build text, not an image. Take a capture. |
| 4 | both | PASS on the exercised cases (record); spec gap SG-1 reserved | See "Check 4 detail" and SG-1. |
| 5 | both | PASS (record) | A dragged crab does not move. Default: it leans about 10° and springs back. Reduce-motion: the lean is replaced by a crab brightening of 0 → +20% → 0 over about 0.4 s, with no movement. One pool pulse at touch-down, subject to the 1.5 s limit. |
| 6 | both | PASS (record) | Pulses start at least 1.5 s apart, counted from the previous pulse start. Flashes neither count nor delay. Five seconds of rapid tapping gives three or four pulses. See O2 on one wording slip. |
| 7 | default | PASS (record) | The intro runs once per load and not on rotation. A pool touch-down cancels it, and the pool follows the finger from its drawn position. Under reduce-motion the intro is skipped, as the spec says. |
| 8 | both | PASS (record) | The level is completed by touch with the bubble hidden. |
| 9 | both | PASS (record) | There is no failure, timer or inactivity cue. Nothing happens if the screen is left alone. Undo restores the previous position, and a second undo does nothing. |
| 10 | both | PASS (record) | Only the existing sheet plus the procedural oval shadow. |
| 11 | default | PASS (record, capture) | During the intro, a crab, home or sand touch stops the intro. The pool glides back in 0.15 s. The crab flip and wiggle, or the home glow, start within 0.1 s. The pulse starts 0.15 s after touch-down, which is inside 0.2 s. The pulse is not blocked, and the idle pulse starts from normal size after it. Frame-level timing needs a capture. |
| 12 | default | PASS (record) | After an intro-cancel, drag, drop and undo return the pool to the start spot. A second undo does nothing. The intro and the ease-back add no undo step. The build also describes undo after a drop in the reduce-motion case. |
| 13 | both | PASS (record) | A sand tap from 0.6 s up to under 1.5 s after the pulse start gives the +15% flash (within 0.1 s, fade over 0.3 s) with no scale change and no pulse. This covers 0.8–1.3 s. A running flash is not restarted. A tap at 1.5 s or later starts a pulse and no flash. Under reduce-motion the first pulse is the two-beat +30% brightness pulse and the flash looks the same as in default mode. |
| 14 | default (reduce-motion by inference) | PASS (record) | Default: the outermost rim grabs the pool at idle 1.06 and at pulse 1.15. A touch just outside the smallest size goes to the sand. The hit area is never below at-rest. The build's reduce-motion section does not restate the hit area. It says the pool still grows to 1.10 and has no scale pulse, so the at-rest size applies by inference. |
| 15 | default | PASS (record) | The flip uses the pool's logical position (the start spot) during the slide and the glide. |
| 16 | both | PASS (record) | Default: after an intro-cancel by a non-pool touch the pulse shows from the end of the glide, the idle pulse is hidden during it and restarts from normal size, and a flash-only tap leaves the idle pulse running. Reduce-motion: the idle brightness effect is hidden during a pulse and starts again from normal brightness. A flash-only sand tap does not interrupt it. It stops while the pool is held and restarts from normal brightness on release. |
| 17 | default | PASS (record, capture) | A second crab, home or sand touch during the glide plays only that object's response. There is no flash and no extra pulse. Exactly one pulse starts 0.15 s after the first touch, including for a touch at the 0.15 s moment. A sand tap 0.6 s to under 1.5 s after that pulse start gets the flash. The 0.05 s, 0.10 s and 0.15 s cases need a 60 fps recording. |
| 18 | both | PASS (record) | A second-finger sand tap on a held pool gives the +15% flash (within 0.1 s, 0.3 s fade) whatever the time since the last pulse, unless a flash is already showing. The pool keeps its lift and shadow. A crab or home tap gives only its own response. These taps do not change when the next pulse is allowed. After release, a sand tap behaves as in check 13, counted from the last pulse that actually started. |
| 19 | reduce-motion | PASS (record, capture) | See "Check 19 sweep". |
| 20 | reduce-motion | PASS on the numbers (record, capture); wording discrepancy O1 | See "Check 20". |

### Check 4 detail (both modes)

- **Crab, home, sand and pool, 10 taps each, at 2 s spacing and as fast as possible:** each touch has a response.
  - Crab: flip and wiggle (default) or the brightening (reduce-motion), starting within 0.1 s of touch-down.
  - Home: the glow, within 0.1 s.
  - Sand: a pulse within 0.2 s, or the pulse already running, or the flash within 0.1 s.
  - Pool: the lift to 1.10 and the shadow, within 0.1 s.
- **Rapid tapping:** a crab or home tap inside the 1.5 s limit gets its own response. Sand gets the pulse or the flash. The build's last line under "Repeated touches" states that every touch gets a response.
- **Second finger on a held pool:** sand gives the flash, and crab or home give their own response. No pulse starts. This is covered by check 18.
- **Second tap during the glide (default only):** the object's own response plus the pending pulse, which is at most 0.15 s after the first touch.
- **Reduce-motion:** the sand-tap sweep is in check 19. The window that was silent in build 0.4 (0.4–0.6 s) is now covered by beat 2, and the build says a tap exactly at 0.6 s gets the flash.

### Check 19 sweep (reduce-motion, P = pulse start)

P is a pulse start. The sweep points are t = 0.0, 0.1 … 1.4 s, plus 0.55 s and 1.5 s.

| t after P | Build record says | Result |
|-----------|-------------------|--------|
| 0.0–0.2 | Beat 1 rising to its +30% peak at 0.1 s, then falling | PASS |
| 0.3 | Beat 2 starts at this instant. The pool is at normal brightness for a single frame. A touch on that frame sees beat 2 rise from the next frame, well inside 0.2 s | PASS (record, capture of the single frame) |
| 0.4, 0.5 | Inside beat 2 (peak at 0.4 s, falling at 0.5 s). These were silent in build 0.4 | PASS |
| 0.55 | The last part of beat 2. The build calls it "faint and about to end" | PASS on the record only; marginal, needs a 60 fps capture |
| 0.6 | The flash. The build says exactly 0.6 s now gets the flash | PASS |
| 0.7–1.4 | The flash (+15% within 0.1 s, 0.3 s fade, not restarted while running) | PASS |
| 1.4 then 1.5–1.6 | The flash is running and the new pulse starts. The flash ends. The pool shows the larger change, never the sum | PASS |
| 1.5 or later (fresh) | A new pulse and no flash | PASS |

- No sweep point is silent.
- The build does not state brightness values for the falling part of beat 2, so I cannot judge how visible the 0.55 s tap is from the record.
- Taps at 0.56–0.59 s are not in the sweep. The spec lists this as an open remaining gap.

### Check 20 (reduce-motion pulse shape)

- The build record matches the spec numbers:
  - Two beats, each reaching +30% within 0.1 s and back to normal 0.3 s after its start.
  - Beat 2 starts 0.3 s after beat 1, and the total is 0.6 s.
  - No size change and no movement.
  - The pool shows the larger of the active changes, never the sum.
  - A pulse starting during a flash ends the flash. Touching the pool ends any pulse or flash.
  - The idle effect is hidden during the pulse.
- The beat shape, the single-frame return to zero and the 0.55–0.6 s tail need a 60 fps capture.

### Spec gap and observations

- **O1 (check 20 wording against the numbers; for Design, not resolved by QA).** Check 20 says "the 0.3 s dip between beats". The numbers in both the spec and the build make the pool return to 0 exactly when beat 2 starts, so the build has no 0.3 s dip. The build says normal brightness lasts one frame. The spec edge case claims every instant of the first 0.6 s shows a brightness change except the end of beat 2, which also differs by that one frame. Design should say which is meant: a one-frame return to 0, or a real gap between the beats. I passed check 20 on the numbers, which the build matches. A shape change would reopen it.
- **O2 (build wording slip).** Under "Repeated touches" the build says a new pulse "starts at most 1.5 s after the start of the previous pulse". The next lines say "at least 1.5 s apart", and the spec says a minimum. I read it as a minimum, and I expect the build to behave that way. The sentence should be corrected in the build record.
- **O3 (0.55–0.6 s tail).** This remains the spec's open gap. It is not judged without a capture (see check 19).
- **SG-1 (spec conflict; for `game-designer`; not in the exercised cases).**
  - **Scenario (both modes):**
    1. A pulse starts at P.
    2. The child touches the pool, which cancels the pulse (rule 1).
    3. The child releases quickly, for example at P+0.2, and the 0.15 s release shrink ends at P+0.35.
    4. The child then taps sand before P+0.6, for example at P+0.45.
  - **What the rules give:** the 1.5 s limit blocks a pulse. Rule 5 condition (2) is defined by time since the pulse start, which is under 0.6 s. The build says "a sand tap during the first 0.6 s of a pulse shows the pulse itself and no flash". The pulse was cancelled, so no pulse is running and nothing else plays. I derived this from the rules and the build text, not from an explicit statement in either.
  - **Why it is a conflict:** check 4 says every tap gets a visible response "whatever the time since the previous tap". The spec does not say what happens to the "pulse is the response" window when the pulse is cancelled. This sits in the spec, so I did not fail check 4 on my own reading, and I did not pass it silently either. It is not new in build 0.5: the same rules applied to 0.4 and to revision 3.
  - **Needed from Design:** either the flash is allowed once the pulse is cancelled, or the "running" window ends at the cancel, or the criterion is narrowed. If Design says the criterion governs, check 4 fails in both modes. The fix would then be Build work (`gameplay-engineer`).

### Regressions checked (default mode)

- The only change is that a sand tap at exactly 0.6 s gets the flash (previously nothing). It is consistent with check 13 and the spec.
- Pool drag, clamping, release shrink, drop on home and drop on crab, home glow range, crab facing, rotation, and second finger on a held pool are all described as in 0.4.
- Levels 2 and 3 are stated as unchanged. I did not run them.

### Unconfirmed (rests only on the build record; needs a device or 60 fps capture)

- Check 2: the 1.8:1 grayscale contrast. Check 3: the home styling.
- Frame-level timing for checks 11 and 17, and the 0.05 s and 0.10 s cases.
- Checks 19 and 20: the beat shape, the single frame between beats, the 0.55 s tap and the 0.55–0.6 s tail. These also cover checks 2, 18 and 20 in the packet's list.

## Decisions already made

- D-001: holds. No failure, timer or inactivity cue.
- D-003: the blip and hit area behave as specified.
- D-004: ease-back taps, the window origin and the held pool behave as specified.
- D-005: the build implements the two-beat reduce-motion pulse. F1 is closed on the record, because 0.4–0.6 s is no longer silent.

## Constraints

- Level 1 only. Touch only. No dependence on text.
- Existing sprite sheet only, plus the procedural shadow.
- The same criterion is not failing a second time, so no `technical-director` route is triggered. If SG-1 turns into a check 4 fail, this would be the first fail of that form for the SG-1 case. It is not the F1 case, which passed.
- The Playtester receives no implementation detail from this report.

## Open questions

- **For game-designer:** resolve SG-1, and rule on O1 (a one-frame return to zero or a gap between beats).
- **For Studio:**
  - Arrange the device captures listed under "Unconfirmed", including the home styling capture.
  - Fix the wording slip in O2.
  - Reduce-motion availability on the target OS versions is still not known, and is not part of this verification.

## Expected output

The Studio routes SG-1 and O1 to `game-designer`. If neither changes behavior, build 0.5 can go to the Playtester round, which may include children on devices with reduce-motion on. If the captures contradict any "record" result above, they return to `gameplay-engineer`. Tell the Playtester only what to observe:
- Whether the child touches the pool within about 10 s.
- Whether a tap on the sand, crab or home leads the child to the pool.
- Whether any touch looks as if the game did not notice it.
- Whether the child fails to pick up the pool by its edge.

## Load

- Role: studio/roles/studio.md
- Skills: none
- Project: design/onboarding.md, sim/build-0.5.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md, decisions/D-004-ease-back-taps-window-origin-held-pool.md, decisions/D-005-reduce-motion-pulse-fills-window.md
- Previous handoff: goals/G-001-first-puzzle-stall/29-studio-to-qa.md
>>>END
