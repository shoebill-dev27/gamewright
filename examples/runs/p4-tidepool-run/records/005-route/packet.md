# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-first-puzzle-stall/04-game-designer-to-studio.md, goals/G-001-first-puzzle-stall/05-art-director-to-studio.md
next_seq: 6
context_request: allowed once (@need, up to 8 paths)
current_build: sim/build-0.2.md (newest simulated build; older ones are history)

## You may write

- goals/G-001-first-puzzle-stall/goal.md
- goals/G-001-first-puzzle-stall/04-game-designer-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-first-puzzle-stall/05-art-director-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-first-puzzle-stall/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 06
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
goals/G-001-first-puzzle-stall/goal.md
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
- **Diagnose** — Is the cause understood? No. Creates stage 2 (`game-designer`). `art-director` is
  not added now; it is added at Route if the observation points to something visual.
- **Design** — Is the intended behavior of the fixed first puzzle specified? No:
  `design/onboarding.md` specifies the current level 1 and its teaching intent, not a fix. Creates
  stage 3. If Diagnose finds an ordinary defect against the existing spec, Route drops this stage.
- **Build** — Must the game change? The Owner wants it fixed, so yes. Creates stage 4.
- **Verify** — Always after Build. Stage 5.
- **Play** — Is the Goal about how the game plays or feels? Yes. Stage 6, in a fresh context
  without the implementation history.
- **Review** — Is it an experience Goal? Yes. Stage 7 (`game-director`).
- **Next** — Always. Stage 8.

Skipped for now:

- **Decide** — Is there a real choice of direction, priority or scope? Not at this point. Choosing
  among fixes for player-facing behavior inside the approved direction is `game-designer`
  authority. Route adds Decide if Diagnose or Design produces options that change direction,
  priority or scope, and escalates if a trigger fires.
- **Plan** — Is the technical approach non-obvious, risky, cross-system or parallelizable? Not
  knowable until a fix is specified; a level 1 teaching change is expected to be local. Route
  re-asks this after Design and adds Plan if the answer is yes.

Flag for Diagnose (not a conclusion): `project.md` lists "No mechanic may depend on reading text"
as a constraint and says level 1 teaches with a text bubble, for players some of whom are early
readers.

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | playtester | playtest-session | done | 01-studio-to-playtester.md |
| 2 | Diagnose | game-designer | diagnose-experience | open | 02-playtester-to-game-designer.md |
| 2b | Diagnose | art-director | visual-review | open | 03-studio-to-art-director.md |
| 3 | Design | game-designer | write-design-spec | planned | — |
| 4 | Build | gameplay-engineer | implement-change | planned | — |
| 5 | Verify | qa | verify-change | planned | — |
| 6 | Play | playtester | playtest-session | planned | — |
| 7 | Review | game-director | review-outcome | planned | — |
| 8 | Next | studio | — | planned | — |

Status: planned | tentative | open | done | skipped. The route is a plan; the Route operation
revises it.

## Route changes

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

## Next action

Run steps 2 and 2b (Step operation, in either order or in parallel): `game-designer` on
`02-playtester-to-game-designer.md` and `art-director` on `03-studio-to-art-director.md`. Then
Route, which waits for both. Phase 1: the Studio stops after every Route and states the next
action.

## Outcome

<!-- Filled at close, for the Owner, in owner_language (ja). -->
>>>END

<<<FILE goals/G-001-first-puzzle-stall/04-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 4
from: game-designer
to: studio
stage: Route
outcome: done
---
# 04: game-designer → studio — diagnosis of the level 1 stall (build 0.2), ready to route to Design

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. -->

## Task

Route this diagnosis. Merge it with the art-director's review of level 1 (handoff 03, not available to me). Then route `game-designer` Design (route step 3 in `goal.md`), unless the Director needs to confirm something first (see "Needs a Director's eye").

## Context

Goal G-001 (first-puzzle-stall). Owner's words: 「最初のパズルで子どもが手を止めてしまう。直したい」. Success condition: children aged 7–10 begin purposeful touch interaction with level 1 on their own, with no long pause and no adult explanation. This diagnosis works from the playtester's report (`02-playtester-to-game-designer.md`, three simulated sessions). The Load list was `project.md` vision, player profile and constraints, `design/onboarding.md`, and D-001. I did not read `sim/build-0.2.md` or the art-director's result.

## Findings

### Diagnosis (diagnose-experience)

**Symptoms, with evidence**

- **S1: Delayed first touch on the pool.**
  - Age 7 spent about 20 s on the crab and home, then looked at the parent. The parent read the bubble aloud and the child solved it quickly.
  - Age 8 spent about 35 s and reached the pool only by chance.
  - Age 9 read the bubble and dragged the pool in 10 s.
  - Both children who stalled went to the crab first. Activity rose, then produced no result, then dropped (looking at the parent).
- **S2: Touches on non-target objects get no response.**
  - Taps on the crab and home did nothing, and dragging the crab did not move it.
  - Ages 7 and 8 repeated these attempts. The playtester reports that to the children it looked like touch that did not register.
- **S3: Level 1 depends on reading.**
  - The only instruction is the text bubble. The early reader (7) ignored it and needed it read aloud. The reader (9) was fine.
  - Levels 2–3 went smoothly for everyone once the pool mechanic was known, so the problem is local to the opening.

**Causes, in design terms**

- **C1: The wrong object looks interactive and the right one does not.**
  - Readability and affordance problem. The crab has a darker outline and a gentle bob, which are the usual signals of a touchable thing.
  - The pool is the same pastel tone as the sand and reads as part of the sand pattern.
  - This breaks pillar 3 ("interactive pieces always stand out clearly") and explains why 2 of 3 went to the crab. It explains S1 and feeds S2.
- **C2: Feedback gap.**
  - A touch on any non-solution object gives no response, so the child gets no information and no redirection.
  - This turns a wrong first guess into a dead end. It explains S2 and the drop in activity in S1. It also conflicts with the profile ("quickly lose interest when nothing responds").
- **C3: The teaching channel is text.**
  - `design/onboarding.md` has level 1 teach through a text bubble only. That breaks pillar 2 ("learn by touching, not by reading") and the constraint "No mechanic may depend on reading text".
  - The flag in the handoff is confirmed as a design defect, not just a style question. It explains S3 and why the early reader needed help.
- **C4 (weaker): No self-demonstrating moment.**
  - Nothing in the scene shows what a pool does, so a child who skips the text has no other source for the rule. This is a contributing cause, not an independent one.

**Intended vs. not intended (answer to the open question)**

- `design/onboarding.md` specifies only that the pool is dragged to the home. It says nothing about touches on the crab or home.
- The crab not being draggable is consistent with the design, because the mechanic is moving pools.
- Total silence on touch is not an intended experience. It is a design gap (C2), not necessarily a code defect.
- I cannot tell from the packet whether input is actually registering on the crab and home, or whether there is simply no handler. Suggested action: a small `qa` check on build 0.2 that touches on the crab and home are received. This is cheap and does not block Design. If input is not registering, that is a separate defect for qa. If it is registering with no handler, option B below covers it.

**Options**

*Option A: make the pool the obvious thing to touch, and teach without text.*
- What it changes:
  - Give the pool a clear "touch me" look: stronger contrast or outline against the sand, a soft shimmer or pulse.
  - In level 1, tone down the crab's false affordance (reduce the bob or outline emphasis) so the pool wins attention.
  - Replace text-only teaching with a looping non-text cue, such as a ghost hand or pool sliding toward the home. Keep the bubble only as optional extra, or drop it.
- Addresses: S1, S3 (C1, C3, C4).
- Cost: low to medium. Mostly parameters and the existing sprite sheet. Visual details need the art-director's input. New art is out of scope, so tint, outline or animation on existing sprites must be enough.
- Risk: low. If the cue is too strong the puzzle becomes trivial, which is acceptable for level 1.
- Vision fit: strong (pillars 2 and 3, the text constraint, D-001).

*Option B: make the whole scene respond to touch and use it to guide.*
- What it changes:
  - Tapping the crab makes it react (wiggle, look toward the pool). Tapping the home makes it glow gently. Dragging the crab makes it resist slightly or turn toward the pool.
  - Every touch gets a visible response within a short time.
- Addresses: S2 directly, and S1 by redirecting wrong guesses to the pool (C2).
- Cost: low to medium. Needs small reaction animations on existing sprites and a response to touch on every object.
- Risk: low. It could add noise in later levels, so scope it to level 1 first.
- Vision fit: strong. It supports "learn by touching" and the profile, and it has no failure or timer.
- Limit: alone it does not make the pool visible, so a child may still look for it for a while.

*Option C: an idle demonstration hint (assist after inactivity).*
- What it changes: if the child has not touched the pool after a set time, a non-text demo plays (the pool slides to the home and back, or a ghost hand appears).
- Addresses: S1 and S3 as a safety net.
- Cost: low.
- Risk: it adds an idle timer, which sits near D-001 ("no timers"). I judge it fits the pillar's intent, because it is a hint timer, not a pressure or loss timer. Nothing is lost and no deadline is implied. Still, the Director should confirm that reading because D-001 is an Owner pillar.
- Limit: it fixes the stall after the fact rather than preventing it, so on its own it leaves the first 5–10 s dead.
- Vision fit: acceptable, pending that confirmation.

None of the options changes a pillar, a Decision or the scope as written. Option C touches D-001 by interpretation only.

**Recommendation**

- A + B together are defensible. A removes the cause of the first wrong guess (C1) and the reading dependency (C3). B turns a wrong guess into redirection instead of a dead end (C2). Together they cover all three symptoms with low cost and low risk, using the existing sprite sheet.
- Hold C in reserve. Add it only if a re-playtest of A + B still shows a stall.
- The art-director's review of the level 1 visuals should settle the specifics of the pool's look and the crab's emphasis. Design should reconcile A with that result.

**Draft acceptance criteria (to be finalized in Design)**

All are player-observable, tested with children aged 7–10 and no adult help.
1. The child's first touch-down on the tide pool happens within 10 s of level start. The 9-year-old's 10 s with the bubble is the best observed baseline, and the target is no worse for non-readers.
2. No period longer than about 8 s with no touch interaction before the first pool drag. Looking to the parent for help counts as a stall.
3. Every touch on the crab, home or pool gets a visible response, and no touch is silently ignored.
4. Level 1 is completable by a child who does not read the bubble.

The exact numbers are my proposal from three data points and can be tuned in Design.

**Unknowns (what the evidence cannot settle)**

- The evidence is three simulated sessions, with no spoken quotes and no timings beyond those above. Thresholds are therefore tentative.
- Whether the crab's outline and bob are the main pull, or whether the pool's camouflage alone is enough to explain the stall. They are correlated in this data. A and B together do not need this settled, but a later test could separate them.
- The 8-year-old's reading ability is not stated, so I cannot attribute that stall to the text.
- Whether touch on the crab and home registers in the build (see the qa check above).
- The art-director's result (handoff 03) is not available, so the visual specifics are open.

**Needs a Director's eye (optional, before or in parallel with Design)**

- Confirm that an idle hint (Option C) is compatible with D-001. It is not needed if Design goes with A + B only.

## Decisions already made

- D-001 (no fail states, no timers, every move undoable) is unchanged and respected by A + B.
- No new Decision made in this step. Choosing A + B is within Design's authority and, once the spec is written, can be recorded then if the Studio wants one.

## Constraints

- Out of scope: levels 2 and later, any change to a pillar or D-001, and new art beyond the existing sprite sheet.
- Design needs to work out how the pool becomes more visible using only existing sprites (tint, outline, animation).

## Open questions

- For the Studio: does the art-director's result (03) change the visual direction of Option A? Merge before routing Design.
- For `qa` (optional, non-blocking): do touches on the crab and home register in build 0.2?
- After the change is built: does a re-playtest with children (ideally one early reader and one non-reader of the bubble) meet the draft criteria?

## Expected output

Route to `game-designer` Design: a design spec (`write-design-spec`) for level 1. It covers the pool affordance, the crab's de-emphasis, a response for every touch, the non-text teaching cue, the final acceptance criteria, and edge cases. It updates `design/onboarding.md` and takes into account the art-director's result.

## Sender assessment

Confidence is medium-high that C1–C3 are the main causes, since they explain all observed behavior and match the profile. Confidence in the exact thresholds is low because of the small simulated sample. I did not make a choice outside my authority.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, design/onboarding.md
- Decisions: decisions/D-001-no-fail-states.md
- Previous handoff: goals/G-001-first-puzzle-stall/04-game-designer-to-studio.md (this file); the art-director's handoff 03 to be merged by the Studio
>>>END

<<<FILE goals/G-001-first-puzzle-stall/05-art-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 5
from: art-director
to: studio
stage: Diagnose
outcome: done
---
# 05: art-director → studio — visual review of level 1 (build 0.2): the pool does not read as touchable, and the crab does

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. -->

## Task

Return the visual verdict (`visual-review`) on level 1 of build 0.2 to the Studio for the Route operation, which merges it with the `game-designer` diagnosis before Design.

## Context

Goal G-001 (first-puzzle-stall). Owner's words, verbatim: 「最初のパズルで子どもが手を止めてしまう。直したい」

Handoff 03 asked whether the player can tell at a glance what to touch, what is visual versus rules, and what visual direction to take. The evidence is the observation report (`02-playtester-to-game-designer.md`) and `sim/build-0.2.md`: three children (ages 7, 8, 9), simulated sessions, no timings beyond those given, no quotes. The `game-designer` result was not available to me.

## Findings

### Visual verdict

| Criterion | Verdict | Evidence |
|---|---|---|
| Readability: the interactable is identifiable at a glance | **Fail** | The tide pool, the only interactable, has the same pastel tone as the sand and looks like part of the sand pattern. In the sessions, the 7- and 8-year-olds did not touch it for about 20 s (until the parent read the bubble) and about 35 s (by chance). The 9-year-old found it only by reading the bubble. |
| Consistency with the art direction ("interactive pieces have a darker outline and a gentle idle motion") | **Fail, in two directions** | (a) The pool is interactive but has no outline or idle motion. (b) The crab has the outline and the bob but is not interactive, so it is a false affordance. Two of three children went to the crab first, tapped it repeatedly (age 7), and tried to drag it (age 8). |
| Palette and shapes (pastel, rounded) | Pass, as far as the report shows | No complaint or evidence against it. The problem is that the palette gives no separation, not that it is off-style. |
| Text bubble as a visual aid | Fail as an affordance | The 7-year-old ignored it. It is placed apart from the pool and points at nothing. It also cannot carry information (constraint: no mechanic may depend on reading text). Whether to keep it as supplementary text is a design question. |

The shell-shaped home: the packet does not say whether it has an outline or idle motion. The 7-year-old tapped it, so it may be read as touchable. This is an unknown and needs a capture check.

### Separating visual from rules

**Visual (mine):**
- The pool has no affordance cues.
- The crab and possibly the home carry affordance cues they should not have, as long as they are not interactive.

**Rules, feedback and text (route to `game-designer`; I do not decide these):**
- Taps on the crab and home give no response, and dragging the crab does nothing. This reads to children as touch that did not register. If it is not intended, it may be a defect for `qa`.
- Whether the crab should respond at all, for example by guiding toward the pool. If it does, its outline and bob become correct.
- The reliance on a text bubble in level 1.
- What counts as a stall (a threshold for Design).

The visual problem is real and separable. It is not only a rules problem, but it is probably not the whole cause. The silent, non-responding crab and home extend the stall once a child picks the wrong target, so a visual fix alone may not be enough. Evidence is three simulated sessions, and I cannot say how much each cause contributes.

### Proposed visual direction (within the art direction and the existing sprite sheet)

1. **Make the pool the unmistakable interactable.** Give it the same darker outline weight the crab has now, and the same kind of gentle idle motion (slow scale pulse or ripple using the existing sprite, no new art).
2. **Separate the pool from the sand by value and hue.** Use a more saturated pastel water blue or teal, still pastel and rounded. Check by squinting or viewing in grayscale: the pool must still separate from the sand there.
3. **Make interactivity exclusive.** Among everything in the scene, the pool is the only element with outline plus idle motion, unless the game-designer makes another element interactive. If the crab stays non-interactive, remove its interactive styling: lighter or no outline, static, or only a one-off ambient motion different from the pool's. If the crab is made responsive, keep the styling and make sure the response (the game-designer's call) matches it.
4. **Do not rely on the text bubble.** It can stay as a supplement. Any pictorial cue such as a hand or arrow would be new art, which is out of scope. Reusing an existing sprite as a cue would need a check of the sheet.
5. **Home:** apply the same rule. Confirm in a capture whether it carries interactive styling and remove it if it does and is not interactive.

Whether recoloring or tinting the pool counts as "new art beyond the existing sprite sheet" should be confirmed by Design. I read a tint or recolor of an existing sprite as within the constraint.

### Proposed visual acceptance criteria (for Design to adopt or adjust)

- In a capture of level 1 at start, the pool is the only element with a darker outline plus idle motion, and it is distinguishable from the sand in grayscale.
- No non-interactive element has interactive styling.
- Playtest (children aged 7–10, no adult help): the first purposeful touch goes to the pool. The pause threshold is set by Design, not here.

## Decisions already made

None. No style pillar changes, so no escalation is needed, and no decision file was written.

## Constraints

- No change to gameplay rules or parameters, no change to style pillars, and no new art beyond the existing sprite sheet.
- Must not conflict with D-001 (no failure, no timers).

## Open questions

- For `game-designer` and Design: should the crab respond to touch? This decides whether its styling stays (direction 3).
- Is the home interactable? Check styling against the build.
- Is the missing response to taps an intended behavior or a defect for `qa`?
- After the visual fix, a playtest should check whether the stall is gone without the text bubble.

## Expected output

The Studio merges this verdict with the `game-designer` diagnosis at Route, then moves to Design, where the visual direction above becomes the visual part of the spec and its acceptance criteria.

## Sender assessment

Confidence is high that the pool's lack of affordance and the crab's false affordance are visual causes of the stall. Confidence is moderate that they are the main cause, because the report shows silent non-response as an aggravating factor. Evidence is limited to three simulated sessions.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#art-direction, project.md#constraints, sim/build-0.2.md
- Decisions: none
- Previous handoff: goals/G-001-first-puzzle-stall/03-studio-to-art-director.md
>>>END
