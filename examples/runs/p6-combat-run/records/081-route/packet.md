# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/77-qa-to-studio.md
next_seq: 78
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha cf0f0ee63752; run through the project's run commands)
log: last 5 of 31 entries in @log-recent; the full history is goals/G-001-combat-monotony/log.md

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/77-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 78
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
| Goal | An Owner request, tracked as a Goal record (current state and route plan) and an append-only Goal log (history). | `<project>/goals/<goal>/goal.md`, `log.md` |
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
id: lantern-depths
name: Lantern Depths (sample, playable)
repository: repo/ (a small headless build; played through input scripts)
owner_language: ja
player_visible: manual.md
build: repo
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}
---
# Project: Lantern Depths (sample, playable)

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

Vertical-slice prototype, build 0.4 in `repo/`: 5 rooms in one cave biome, 2 enemy types, player
kit of attack and dash. Build 0.4 fixed damage during a dash. A play session is an input script
(`manual.md`): `run_play` shows what a player sees, `run_trace` the simulation state, and
`run_tests` runs the build's tests. `run_bots` lets the team's balance bots play rooms and reports
clear times, hearts lost and actions used (`repo/bots.py`).

## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).

## Art direction

Dark caves lit by the player's lantern; warm light against cold blue-black. Threats use saturated
orange/red so they read against the dark.

## Design index

- `design/combat.md` — player kit, damage and invulnerability rules, enemies.
- `manual.md` — controls and the play script format (player-facing).
>>>END

<<<FILE @project-files
decisions/D-001-one-button-combat.md
decisions/D-002-combat-response-scope.md
decisions/D-003-run-end-and-room-rules.md
decisions/D-004-option-a-single-change-set.md
decisions/D-005-owner-places-manual-draft.md
decisions/D-006-overlap-display-and-practice-room-manual.md
decisions/D-007-practice-room-paragraph-placed-by-owner.md
decisions/D-008-manualtest-run-by-owner-one-failure.md
decisions/D-009-manualtest-phrase-check-ignores-line-wraps.md
decisions/D-010-owner-ran-suite-ac15-passes.md
decisions/D-011-grub-turns-stun-body-hit-dash-facing.md
decisions/D-012-on-you-line-for-displaced-enemies.md
decisions/D-013-knockback-of-grub-on-players-tile.md
decisions/D-014-one-rule-for-cells-on-you-and-hit-line-word.md
design/combat-visuals.md
design/combat.md
goals/G-001-combat-monotony/01-studio-to-playtester.md
goals/G-001-combat-monotony/02-playtester-to-game-designer.md
goals/G-001-combat-monotony/03-game-designer-to-game-director.md
goals/G-001-combat-monotony/04-studio-to-qa.md
goals/G-001-combat-monotony/05-game-director-to-studio.md
goals/G-001-combat-monotony/06-qa-to-game-designer.md
goals/G-001-combat-monotony/07-studio-to-playtester.md
goals/G-001-combat-monotony/08-playtester-to-game-designer.md
goals/G-001-combat-monotony/09-studio-to-game-designer.md
goals/G-001-combat-monotony/10-game-designer-to-studio.md
goals/G-001-combat-monotony/11-studio-to-technical-director.md
goals/G-001-combat-monotony/12-studio-to-qa.md
goals/G-001-combat-monotony/13-studio-to-art-director.md
goals/G-001-combat-monotony/14-technical-director-to-studio.md
goals/G-001-combat-monotony/15-qa-to-studio.md
goals/G-001-combat-monotony/16-art-director-to-studio.md
goals/G-001-combat-monotony/17-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/18-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/19-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/20-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/21-studio-to-owner.md
goals/G-001-combat-monotony/22-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/23-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/24-studio-to-qa.md
goals/G-001-combat-monotony/25-studio-to-art-director.md
goals/G-001-combat-monotony/26-qa-to-studio.md
goals/G-001-combat-monotony/27-art-director-to-studio.md
goals/G-001-combat-monotony/28-studio-to-qa.md
goals/G-001-combat-monotony/29-qa-to-studio.md
goals/G-001-combat-monotony/30-studio-to-game-designer.md
goals/G-001-combat-monotony/31-studio-to-art-director.md
goals/G-001-combat-monotony/32-art-director-to-studio.md
goals/G-001-combat-monotony/33-game-designer-to-studio.md
goals/G-001-combat-monotony/34-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/35-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/36-studio-to-owner.md
goals/G-001-combat-monotony/37-studio-to-qa.md
goals/G-001-combat-monotony/38-studio-to-qa.md
goals/G-001-combat-monotony/39-qa-to-studio.md
goals/G-001-combat-monotony/40-qa-to-studio.md
goals/G-001-combat-monotony/41-studio-to-art-director.md
goals/G-001-combat-monotony/42-studio-to-owner.md
goals/G-001-combat-monotony/43-studio-to-game-designer.md
goals/G-001-combat-monotony/44-art-director-to-studio.md
goals/G-001-combat-monotony/45-game-designer-to-studio.md
goals/G-001-combat-monotony/46-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/47-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/48-studio-to-owner.md
goals/G-001-combat-monotony/49-studio-to-playtester.md
goals/G-001-combat-monotony/50-playtester-to-studio.md
goals/G-001-combat-monotony/51-studio-to-game-designer.md
goals/G-001-combat-monotony/52-studio-to-playtester.md
goals/G-001-combat-monotony/53-game-designer-to-studio.md
goals/G-001-combat-monotony/54-playtester-to-studio.md
goals/G-001-combat-monotony/55-studio-to-qa.md
goals/G-001-combat-monotony/56-studio-to-game-designer.md
goals/G-001-combat-monotony/57-studio-to-art-director.md
goals/G-001-combat-monotony/58-qa-to-studio.md
goals/G-001-combat-monotony/59-game-designer-to-studio.md
goals/G-001-combat-monotony/60-art-director-to-studio.md
goals/G-001-combat-monotony/61-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/62-studio-to-owner.md
goals/G-001-combat-monotony/63-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/64-studio-to-game-designer.md
goals/G-001-combat-monotony/65-game-designer-to-studio.md
goals/G-001-combat-monotony/66-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/67-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/68-studio-to-qa.md
goals/G-001-combat-monotony/69-studio-to-art-director.md
goals/G-001-combat-monotony/70-qa-to-studio.md
goals/G-001-combat-monotony/71-art-director-to-studio.md
goals/G-001-combat-monotony/72-studio-to-game-designer.md
goals/G-001-combat-monotony/73-game-designer-to-studio.md
goals/G-001-combat-monotony/74-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/75-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/76-studio-to-qa.md
goals/G-001-combat-monotony/77-qa-to-studio.md
goals/G-001-combat-monotony/goal.md
goals/G-001-combat-monotony/log.md
manual.md
project.md
repo/README.md
repo/bots.py
repo/game.py
repo/play.py
repo/tests/test_game.py
>>>END

<<<FILE @decision-titles
decisions/D-001-one-button-combat.md — D-001: Combat uses one attack button plus dash
decisions/D-002-combat-response-scope.md — D-002: Respond to combat sameness by reworking existing enemy behavior first (Option A)
decisions/D-003-run-end-and-room-rules.md — D-003: Room mix is across rooms; zero hearts ends the run; room clear heals one heart
decisions/D-004-option-a-single-change-set.md — D-004: Build Option A as one sequential change set on the existing simulation
decisions/D-005-owner-places-manual-draft.md — D-005: The Owner places the draft `manual.md` (Option A)
decisions/D-006-overlap-display-and-practice-room-manual.md — D-006: Enemies may overlap the player but are never hidden; the practice room is listed in the On screen section
decisions/D-007-practice-room-paragraph-placed-by-owner.md — D-007: The Owner places the practice-room paragraph in `manual.md` (Option A)
decisions/D-008-manualtest-run-by-owner-one-failure.md — D-008: The Owner ran `run_tests` for AC-15 (Option A); one `ManualTest` failure goes to the designer
decisions/D-009-manualtest-phrase-check-ignores-line-wraps.md — D-009: The `ManualTest` phrase check ignores line wraps; `manual.md` stays unchanged
decisions/D-010-owner-ran-suite-ac15-passes.md — D-010: The Owner ran `run_tests` for the AC-15 rerun (Option A); 40/40 passes
decisions/D-011-grub-turns-stun-body-hit-dash-facing.md — D-011: Grubs take turns and crowd two deep; hit-stun 0.15 s; body hit; dash sets facing
decisions/D-012-on-you-line-for-displaced-enemies.md — D-012: Mark an enemy on the player's tile with an `on you:` line, and name the attacker's position in hit lines
decisions/D-013-knockback-of-grub-on-players-tile.md — D-013: A grub on the player's tile is knocked back toward the side it is drawn on
decisions/D-014-one-rule-for-cells-on-you-and-hit-line-word.md — D-014: One rule for cells, sides, "on you" and the hit-line word
>>>END

<<<FILE goals/G-001-combat-monotony/goal.md
---
kind: goal
id: G-001
project: lantern-depths
status: active
created: 2026-10-15
---
# G-001: Combat feels monotonous

## Owner request

> 戦闘が単調なので改善したい

## Interpretation

Success condition (qualitative): when an action player from the project's player profile plays through combat encounters, the fights feel varied and engaging, and the player's moment-to-moment choices (positioning, timing, enemy behavior) visibly matter. The player no longer experiences the fights as the same repeated pattern.

Out of scope: adding input buttons beyond attack, dash and pause (D-001, Owner approval needed); changes to the run length or the non-combat systems; numeric targets (these belong to Design as acceptance criteria, and the final verdict to Review).

No immediate escalation: the Goal does not conflict with the vision or D-001, and it needs no reinterpretation. Improving depth through positioning, timing and enemy behavior is what pillar 1 asks for.

## Unknowns

- Observe (playtester, qa): done (02, 08, 06, 15, 58, 70). Still unobserved: AC-1, 3, 9, 10, 12, 28(c); real-room clear/heal/next room and "run complete" (AC-13, 14); spitter player-view runs; V-6, V-7, V-8. These go to Verify 13f (76).
- Diagnose, Decide: done (03, 53; D-002, D-005, D-006, D-011). A4 (120° cone), D1 (facing mechanic) and D2 (room 1 composition) are held with revisit triggers in 59.
- Design: spec done (59, 60, 65, 73; D-011…D-014, AC-19…AC-30, V-9…V-18). Final V-15 manual wording is in 73 for the Owner.
- Plan: skipped (Waiting behavior local, per 67). Reopen with the Technical Director if the fix for the 30/60 FPS display or hit-line word fails verification a second time.
- Build: AC-19…AC-30 built (67, 75). D-014 rulings 1–5 built; hit-stun test fixed (test was wrong). Two edited tests were not re-run; `ManualTest` (2) could not run without `manual.md` in the build environment, so AC-15 is open for the Owner.
- Verify: 13a QA failed (70): AC-17, AC-22 (suite), AC-28(b) at 30 FPS, V-10, V-14, V-16, V-15 (manual text, Owner step). First failure for each, so no TD re-plan. AC-15 failed once earlier (D-008), passed in D-010; a second AC-15 failure goes to the Technical Director. 13b art-director (71): no live view, question. The visual review runs from QA's verbatim captures (13f output).
- Play: earlier sessions saw only rooms 1 and 2 by script (50, 54), with defeats. Rooms 3–5, the spitter, projectile hits, room clear, the dash and a survived run are unobserved, so monotony itself is unjudged. Next Play follows Verify: fresh playtester, rooms 1–5, reactive play; judged against the retest guideline, which is not forwarded.
- Review: `game-director` with `review-outcome`, planned after the next Play. Open: run progression after "run over"; F1, F4, F6, F7; numbering of same-type enemies in one cell; A4, D1, D2.
- Skipped: none.

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | playtester | playtest-session | done | 02-playtester-to-game-designer.md |
| 2 | Diagnose | game-designer | diagnose-experience | done | 03-game-designer-to-game-director.md |
| 3a | Decide | game-director | make-decision | done | 05-game-director-to-studio.md |
| 3b | Observe (defects) | qa | reproduce-defect | done | 06-qa-to-game-designer.md |
| 3c | Observe (rooms 4–5) | playtester | playtest-session | done | 08-playtester-to-game-designer.md |
| 4 | Design | game-designer | write-design-spec | done | 10-game-designer-to-studio.md |
| 5a | Plan | technical-director | technical-plan | done | 14-technical-director-to-studio.md |
| 5b | Observe (spit line) | qa | reproduce-defect | done | 15-qa-to-studio.md |
| 5c | Design (visuals) | art-director | visual-review, write-design-spec | done | 16-art-director-to-studio.md |
| 6a | Build (code) | gameplay-engineer | implement-change | done | 17-studio-to-gameplay-engineer.md |
| 6b | Build (`run_tests` check, manual placed) | gameplay-engineer | implement-change | done | 23-gameplay-engineer-to-studio.md |
| 7a | Verify | qa | verify-change | done (question, no AC failed) | 26-qa-to-studio.md |
| 7b | Verify (visuals) | art-director | visual-review | done (question, no build output) | 27-art-director-to-studio.md |
| 7c | Verify (rerun: manual, runs, captures) | qa | verify-change | done (question, no AC failed) | 29-qa-to-studio.md |
| 7d | Verify (visuals, from captures) | art-director | visual-review | done (fail: V-1, F3) | 32-art-director-to-studio.md |
| 7e | Design (F1 overlap, AC-15 wording) | game-designer | write-design-spec | done | 33-game-designer-to-studio.md |
| 7f | Build (F1/F3 render, manual paragraph) | gameplay-engineer | implement-change | done (render built) | 35-gameplay-engineer-to-studio.md |
| 7f-O | Owner: place the manual paragraph | owner | — | done (Option A, D-007) | 36-studio-to-owner.md |
| 7g | Verify (all but AC-15) | qa | verify-change | done (pass) | 37-studio-to-qa.md |
| 7i | Verify (AC-15, `ManualTest`) | qa | verify-change | done (question: ManualTest blocked) | 38-studio-to-qa.md |
| 7i-O | Owner: `ManualTest` result | owner | — | done (Option A, D-008: 39/40) | 42-studio-to-owner.md |
| 7h | Verify (visuals) | art-director | visual-review | done (pass; V-6 from code, V-7 not seen) | 41-studio-to-art-director.md |
| 7j | Design (`run over` manual test failure) | game-designer | write-design-spec | done (test too literal, D-009) | 43-studio-to-game-designer.md |
| 7k | Build (test fix, line wraps) | gameplay-engineer | implement-change | done (test changed, suite not run) | 46-studio-to-gameplay-engineer.md |
| 7k-O | Owner: place manual text | owner | — | skipped (manual unchanged, D-009) | — |
| 7l-O | Owner: AC-15 rerun | owner | — | done (Option A, D-010: 40/40) | 48-studio-to-owner.md |
| 7l | Verify (AC-15 rerun by QA) | qa | verify-change | skipped (Owner's 40/40 run, D-010) | — |
| 8 | Play (room 1) | playtester | playtest-session | done (room 1 only, scripted, 2 defeats) | 49-studio-to-playtester.md |
| 9a | Diagnose (Play findings) | game-designer | diagnose-experience | done (A1–A3, A5, B, C, D held) | 51-studio-to-game-designer.md |
| 9b | Play (parts not yet seen) | playtester | playtest-session | done (thin: room 2 only, 1 script) | 52-studio-to-playtester.md |
| 10a | Observe (open facts, bots) | qa | reproduce-defect | done (6 facts settled, 2 partly; D-58-1 ruled in 59) | 55-studio-to-qa.md |
| 10b | Design (A1–A3, A5, manual draft) | game-designer | write-design-spec, make-decision | done (spec, D-011, manual draft) | 56-studio-to-game-designer.md |
| 10c | Design (visuals: "on you", hit source) | art-director | visual-review, write-design-spec | done (V-9…V-17, D-012) | 57-studio-to-art-director.md |
| 10-O | Owner: place manual draft (59) and V-15 text | owner | — | open (final V-15 wording now in 73) | 62-studio-to-owner.md |
| 11 | Plan | technical-director | technical-plan | skipped (Waiting behavior local, per 67; reopen if Verify disagrees) | — |
| 12 | Build (first attempt) | gameplay-engineer | implement-change | done (question: no repo files; Q1 gap) | 61-studio-to-gameplay-engineer.md |
| 12a | Design (Q1 knockback at distance 0, Q2, 3 passages) | game-designer | write-design-spec | done (D-013, AC-28) | 64-studio-to-game-designer.md |
| 12b | Build (re-issue with repo files) | gameplay-engineer | implement-change | done (AC-19…AC-28 built; suite re-run needed) | 66-studio-to-gameplay-engineer.md |
| 13a | Verify | qa | verify-change | done (fail: AC-17, AC-22 suite, AC-28b at 30, V-14/16; V-15 manual) | 70-qa-to-studio.md |
| 13b | Verify (visuals) | art-director | visual-review | done (question: no live view; V-15 fails on document) | 71-art-director-to-studio.md |
| 13c | Design (cell rule at .5, "on you", hit-line word) | game-designer | write-design-spec, make-decision | done (D-014, AC-29/30, V-18) | 73-game-designer-to-studio.md |
| 13d | Build (suite test, D-A, D-C, 13c rulings) | gameplay-engineer | implement-change | done (rulings built; 2 ManualTest need Owner run) | 75-gameplay-engineer-to-studio.md |
| 13e-O | Owner: run suite with manual.md (AC-15) | owner | — | planned (parallel to 13f; not blocking it) | — |
| 13f | Verify (rerun; verbatim captures for AD) | qa | verify-change | open | 76-studio-to-qa.md |
| 13g | Verify (visuals, from QA captures) | art-director | visual-review | planned | — |
| 14 | Play (rooms 1–5, fresh playtester) | playtester | playtest-session | planned | — |
| 15 | Review | game-director | review-outcome | planned | — |

## Route changes

After 13d (75): done, fits the plan; no spec gap, no escalation. Verify 13f opened for `qa` (76), composed without the Sender assessment, both frame rates, with verbatim captures for the art-director. Owner step 13e-O (AC-15 with `manual.md`) runs in parallel, as the build environment lacked `manual.md`.

## Next action

- `qa` runs 13f from `76-studio-to-qa.md` and addresses the result to `studio`.
- Owner: run `python3 -m unittest discover -s tests` with the unchanged `manual.md` beside `repo/` (13e-O, AC-15), report the count and any failure by name, and place the V-15 text from 73 (10-O).
- Then Route: if 13f passes, art-director reviews from the captures (13g). If 13g passes too, compose a fresh Play handoff (14) for the playtester from the build and player profile only.
- A second failure of the same criterion goes to the `technical-director` (Plan).

## Outcome

(Filled at Close.)
>>>END

<<<FILE @log-recent
## 070-route · 2026-10-16

Status: active. Open: 66-studio-to-gameplay-engineer.md.

After 12a (65): done. Q1 is settled by D-013 and AC-28; Q2 and three passages are clarified. No parameter, input or direction change, so no Decide and no escalation. Build re-issued as 12b (66) with the repo files in Load. 11 stays tentative.

## 072-route · 2026-10-16

Status: active. Open: 68-studio-to-qa.md, 69-studio-to-art-director.md.

After 12b (67): done, fits the plan; no spec gap, no escalation. Opened Verify in parallel: 13a QA (68, no Sender assessment, full suite with manual.md plus bots at 30/60 FPS) and 13b art-director (69). Tentative Plan (11) dropped: Waiting behavior is local.

## 075-route · 2026-10-16

Status: active. Open: 72-studio-to-game-designer.md.

After 13a/13b (70, 71): 13a failed (AC-17, AC-22 suite, AC-28b display at 30 FPS, V-10/14/16, V-15 manual); first failure of each, so no TD re-plan. Three spec gaps go to Design 13c (72) before Build. 13b was a question (AD could not run the build): not re-asked; visuals are reviewed after the rebuild from QA's captures. No escalation.

## 077-route · 2026-10-16

Status: active. Open: 74-studio-to-gameplay-engineer.md.

After 13c (73): done. The three spec gaps are ruled (D-014; AC-17, 28 changed, AC-29, 30 and V-18 new; V-10, 12, 14, 16 changed). No number, input or direction changes, so no Decide and no escalation. Build 13d opened (74), addressed back to `studio` so QA's step can be composed without the Sender assessment.

## 079-route · 2026-10-16

Status: active. Open: 76-studio-to-qa.md.

After 13d (75): done, fits the plan; no spec gap, no escalation. Verify 13f opened for `qa` (76), composed without the Sender assessment, both frame rates, with verbatim captures for the art-director. Owner step 13e-O (AC-15 with `manual.md`) runs in parallel, as the build environment lacked `manual.md`.
>>>END

<<<FILE goals/G-001-combat-monotony/77-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 77
from: qa
to: studio
stage: Verify (report to Studio; the Studio composes the next step)
outcome: pass
---
# 77: qa → studio — Verification of the D-014 rebuild (sha cf0f0ee63752) at 30 and 60 FPS: no failures found; V-15 and the AC-15 suite run still depend on the Owner

## Task

Report the verification of the rebuilt `repo/` against AC-1…AC-30 and V-1…V-18 at 30 and 60 FPS. Route the result. Give the art-director the verbatim player-view captures of the six setups from 71 (Appendix A).

## Context

G-001, Option A. Report 70 failed AC-17, AC-22 (suite), AC-28(b) at 30 FPS, V-10, V-14, V-16 and V-15. D-014 (73) ruled the three spec gaps. This is the first verification of the rebuild. I verified from the spec, the criteria and the build only: the suite, play and trace runs of this round, and a reading of the test source. All runs are in `@run-results`. I did not edit the repo, `manual.md` or the design documents.

## Findings

### Verdict

- **No criterion failed on anything observed.** Every item that failed in 70 and could be re-run now passes at both rates (AC-17 as far as observed, AC-22 suite, AC-28(b), V-10, V-14, V-16), and the new AC-29, AC-30 and V-18 pass where observed. So this is not a second failure of any criterion.
- **Not complete.**
  - V-15 (manual text) is not in place: `manual.md` is unchanged and still says only "drawn on a free tile next to you". I report it as not checkable and did not judge it.
  - AC-15 (the two `ManualTest` tests) could not be run here. The environment has no `manual.md` beside `repo/`, and I may not place one.
  - Some items were covered only by the passing suite and not played; they are marked below.
- The art-director's live visual review (V-9…V-18 first-hand, colour, the reverse-video cell) is still open. Appendix A is the material for it.

### 1. Test suite (`python3 -m unittest discover -s tests`)

- Ran 73 tests, **71 passed, 2 errors**.
- Both errors are `ManualTest.*` with `FileNotFoundError: '/manual.md'`. That is the environment gap, not a build result.
- **AC-15 is not judged by me.**
  - By reading the unchanged `manual.md`: every glyph in `play.GLYPHS` is listed as `` `c` ``, the 12 required phrases are present, and the On screen section contains `` `x` ``, "The practice room (`room empty`)" and "drawn on a free tile next to you". I expect it to pass.
  - The Owner's run (route step 13e-O) decides it.
- `CrowdTest.test_hit_stun_is_short` now **passes at both rates**. This is the 70 failure.
  - Test source vs AC-22: it hits the player, then an attack 0.05 s later must be "stunned" and one at +0.25 s must swipe. The invulnerability checks are at +0.75 s (true) and +0.85 s (false). That matches the spec: stun 0.15 s, invulnerability until 0.8 s.
  - The earlier 0.79 check landed on a frame where invulnerability had correctly ended, so the test was wrong, not the build.
  - The test does not exercise "a dash behaves the same way". That is a coverage gap, not a spec mismatch.
- `KnockbackTest.test_edge_grub_is_shown_and_knocked_left` matches AC-28(b) and AC-29(c).
  - It checks the first draw (P at column 15, grub at column 14, `on you: g walking (shown left)`, no "(shown right)").
  - It checks the end at x 13.5 ± 0.1 in cell 14 with no entry, and that the first wind-up and hit words are "left", at both rates.
  - It does not check that every line before the hit says "(on you)"; my play captures do.
- `CellRuleTest.test_line_words_match_the_next_draw` matches AC-30(c) only partly.
  - It skips lines that read "on you", and for "is open" lines it accepts a match with any lowercase `g/w` in the draw.
  - Room 2 always has several, so a wrong word on an "open" line could pass. In this run the only checked lines are the two "rears back" lines (top left, top right).
  - The behaviour is correct in my captures (see AC-30(c)). The test is weaker than the spec and should be tightened, but it is not a failure.
- The traceback line numbers (1135, 1145) exceed the length of the `test_game.py` copy in my packet. I cannot tell whether the executed file equals that copy. The Owner's run should use the repo as built.

### 2. Per-criterion table (30 / 60 FPS)

- "Observed" means seen in this round's play or trace runs.
- "Suite" means a passing suite test that loops both rates, with the test read against the spec. It is not a play observation.

| ID | 30 | 60 | Evidence |
|---|---|---|---|
| AC-1 | pass | pass | Suite (`test_telegraph_and_timing`, `test_grub_glyph_telegraph_before_first_hit`). Indirect: in every capture the wind-up line and `G` come 0.5 s before the first hit (ac29: 0.033→0.567 / 0.017→0.533). No distance-4 play run. |
| AC-2 | pass | pass | Observed (ac29 trace): wind-up 0.5, strike 0.15 (0.533→0.683 / 0.517→0.667), recovery 0.9 (0.683→1.583 / 0.667→1.567). |
| AC-3 | pass | pass | Suite only. |
| AC-4 | pass | pass | Suite only (`test_swipe_in_recovery_hits_and_next_bite_is_late`). Not played this round. |
| AC-5 | pass | pass | Observed (ac28b trace): swipe at 0.200 during Wind-up gives `recover interrupted`, the next wind-up at 0.800 (0.6 s), no heart lost before it. |
| AC-6 | pass | pass | Suite; room 2 shows one grub in Wind-up/Strike per sample. |
| AC-7 | pass | pass | Observed for one spitter (first charge 1.000, next 3.500). Two-spitter stagger: suite only. |
| AC-8 | pass | pass | Observed (spit): "spitter (right) charges" 1.000, "spits" 1.800 (0.8 s later), second pair 3.500 / 4.300; named, no duplicates. |
| AC-9 | pass | pass | Observed: a still player on the line is hit for 1 heart (3.367 / 3.333). Dodge and dash-through: suite only. |
| AC-10 | pass | pass | Suite only. |
| AC-11 | pass | pass | Observed: "(miss) too far", "(miss) not in front". Other reasons: suite. |
| AC-12 | pass | pass | Suite only (`test_multi_hit`). |
| AC-13 | pass | pass | Observed in room 2 (down at 5.267 / 5.250): "you went down", `x`, enemies calm, no on-you line, hit line "(on you)". Run-over screen and restart: suite only (`test_zero_hearts`, `test_down_screen_in_the_player_view`). |
| AC-14 | pass | pass | Suite only (`test_room_clear`, `test_clearing_room_5_completes_the_run`). No real-room clear was played. |
| AC-15 | not judged | not judged | The two `ManualTest` tests could not run (§1). Owner step. |
| AC-16 | pass | pass | Suite (`test_layouts`); room 2 setup row seen in the trace. |
| AC-17 | pass (as observed) | pass (as observed) | See "AC-17 detail". The AC-15 part is open. |
| AC-18 | pass | pass | Observed: in every on-you draw the grub's `g/G/w/W` is beside `P`, and every on-you "rears back" and "is open" line has a matching glyph in its draw. Not played: the distance-4 idle run to 5.5 s, and the spitter-on-`P` case (suite `VisibilityTest` passes). |
| AC-19 | pass | pass | Observed, room 2: wind-ups at 2.733, 3.733, 4.733 at both rates (gaps 1.0 s). |
| AC-20 | pass (sampled) | pass (sampled) | Trace at 3.233: grubs #0 and #2 inside 1.5, #1 and #3 `waiting-cap` at 2.00. Suite checks every tick (`test_engagement_cap`). |
| AC-21 | pass | pass | Re-measured: first heart to third heart 3.300→5.267 = **1.967 s** (30), 3.283→5.250 = **1.967 s** (60). Limit 1.9, margin 0.067 s. One grub is committed at a time. |
| AC-22 behaviour | pass | pass | Observed: stun_left 0.150 at the hit; invulnerability ends 0.800 s after the hit (0.567→1.367, 0.533→1.333). Attack at +0.05 and +0.25: suite. |
| AC-22 suite | pass | pass | `test_hit_stun_is_short` passes (§1). |
| AC-23 | pass | pass | Suite (`test_body_hit`, cases a/b/c). In play, a swipe on a grub at 8.2 hit it (knock82). |
| AC-24, 25, 26 | pass | pass | Suite only. Not re-observed in play or trace. |
| AC-27 | pass | pass | Observed: "(miss) too far" (grub 2.0 ahead) and "(miss) not in front" (grub 1.0 below), arc drawn in both. The third case: suite. |
| AC-28(a) | pass | pass | Observed: `spawn grub 8 4` and `8.2 4` are shown right in every draw (`on you: … (shown right)`) until the hit. 0.3 s later the draw shows `Pw` right, no entry. True position 9.0 ± 0.1: suite only (`test_on_tile_grub_steps_to_its_display_side`, `test_grub_02_tile_away_ends_one_tile_on_its_shown_side`). No trace this round. |
| AC-28(b) | pass | pass | Observed and traced, see "AC-28(b) detail". This was the 70 failure. |
| AC-28(c) | pass | pass | Suite only (`test_slots_and_distance`). Not played in room 2. |
| AC-28(d) | pass | pass | Observed (ac28b trace): the knockback leaves the Recovery timer alone (interrupt at 0.200 → next wind-up 0.800). The 1.5 s bite gap: suite. |
| AC-28(e) | pass | pass | Observed: "you swipe: grub hit (1 left)" with no "(on you)". |
| AC-29(a) | pass | pass | Observed (ac29): `gP` in columns 14/15 at 0 s and in every draw while the grub is still. "rears back (left)", hit "(left)". |
| AC-29(b) | pass | pass | Suite only (`test_one_tile_either_side_of_8_5`): 9.5 reads "right", 7.5 reads "left", never "on you". |
| AC-29(c) | pass | pass | Observed (ac28b): the grub rests at 13.5. `wP` is in cell 14 at 0.50 s, `WP` at 0.80 and 1.00, identical at both rates. Lines say "left". |
| AC-30(a) | pass | pass | Observed on `spawn grub 8.2 4` for 1.5 s with an attack at 0.2 (knock82). Every line for the grub within 0.5 tile reads "(on you)" with an on-you entry, and no side word appears with an entry. The 4 s run without an attack was not played. |
| AC-30(b) | pass | pass | Suite only (`test_shared_cell_beyond_half_tile_is_not_on_you`): "left", drawn left, no entry, "(miss) not in front". Not played. |
| AC-30(c) | pass | pass | Observed, room 2 to 6 s. "rears back (top left)" at 2.733 and "(top right)" at 3.733 have the `G` in that corner of the next draw. The 3.383 and 4.383 "is open" lines read "(on you)" and the draws carry the entries. |
| AC-30(d) | pass | pass | Observed. Hit words are top left (3.300 / 3.283), top right (4.300 / 4.283), and on you (5.267 / 5.250). Each equals the word and the `G` corner at its wind-up start. 4.3 s is "top right" at both rates, as expected. |
| AC-30(e) | pass | pass | Observed (v14): right grub strikes → "(right)" (0.600 / 0.567). Swapped (trace, spawn order 6.75 then 9.25) → "(left)". |
| V-1 | pass | pass | Grubs and the spitter `S` observed. |
| V-2 | pass | pass | Wind-up, charge, swipe and recovery draws exist at the event times at both rates. |
| V-3 | pass | pass | |
| V-4 | pass | pass | `g/G/w/W` and `s/S` observed. `z/Z` not observed. |
| V-5, V-8 | pass | pass | Document only, V-5 and V-8 as in 70. The run-over screen was not played; suite `test_down_screen_in_the_player_view` passes. |
| V-6 | not assessable | not assessable | Text view. |
| V-7 | pass | pass | One spitter observed; the two-spitter distinction is in the suite (`test_two_spitters_in_one_spot_get_numbers`). |
| V-9 | pass | pass | Observed: the line sits under the hearts line, and is absent when nothing is on you. |
| V-10 | pass | pass | Observed in every on-you draw: the line's letter is in the cell on the side it names, and the case matches the state (`G … biting soon`, `g … open`, `g … walking`). No side word for an enemy with an entry, and no "(on you)" without one. |
| V-11 | pass | pass | Observed (neighbor): `gPg`, one entry only (shown left), the real neighbour at 9,4 has none. |
| V-12 | pass | pass | Observed: "rears back (on you)" with `G … biting soon`; "is open (on you)" with `g … open`. Room 2, 3.383 and 4.383: "(on you)", never "(left)" or "(right)". |
| V-13 | pass | pass | Observed: grub hit lines always carry a word. Shot hit: "YOU ARE HIT by a spit shot from spitter (right)". |
| V-14 | pass | pass | Observed, scripted case and the swap. General sentence, room 2: see AC-30(d). |
| V-15 | not checkable | not checkable | The manual text is not in place (Owner). |
| V-16 | pass | pass | Observed: half-tile cell, `Pw`/`WP` and the hit words are identical at 30 and 60; no extra draws seen. |
| V-17 | not re-observed | not re-observed | Passed in 70. The defeat draw and the dash-off draw were not re-run. The first-hit draw behaves as specified (entry present in the immediate draw, gone 0.3 s later). |
| V-18 | pass | pass | Observed in every room 2 and `player 14.5` line and draw. See the note below on hit-line words in lunge draws. |

### 3. AC-17 detail (30 / 60 identity)

- Event times agree within 0.02 s in all compared pairs (e.g. room 2 wind-ups 2.733 / 3.733 / 4.733 at both rates).
- The same events occur in the same order.
- The compared draws are identical: ac28b, ac29, knock8, neighbor and v14.
- The hit words are identical: top left, top right, on you.
- Cells and words at rest are identical (13.5 → cell 14).

### 4. AC-28(b) detail (the 70 failure)

- Script: `player 14.5 4`, `spawn grub 14.5 4`, `0.2 attack`, `end 2`. See Appendix B for the full output.
- Before the hit (0–0.2 s): `gP` / `GP`, `on you: … (shown left)`, "rears back (on you)". The grub is never drawn right.
- After the hit (trace): the grub moves 14.50→14.33 (30) or 14.42 (60) and rests at **13.50**, 1.0 tile left, inside the room.
- At rest: `wP` / `WP` in cell 14, no on-you entry. The wind-up line at 0.800 reads "(left)" and the hit line at 1.333 / 1.317 reads "(left)", both identical at 30 and 60.
- Later: after its lunge the grub is on the player again. "the grub is open (on you)" at 1.450 and `on you: w open (shown left)` appear at both rates.

### 5. Observations for the designer and the art-director (not failures)

1. **Lunge draws and the hit-line word.**
   - Draws made at the moment of a hit show the lunged grub.
   - Room 2, 30 FPS, 4.300: `G` is drawn right of `P` (grub at 8.67,3.55), while the hit line says "(top right)". At 60 FPS, 4.283, the grub is at 8.76,3.49 and `G` is still drawn top right. The same event is therefore drawn in different cells at the two rates.
   - Room 2, 3.300 / 3.283: `G` is left of `P` while the line says "(top left)" at both rates.
   - V-14 and D-014 allow this (draws during the Strike are not compared, and the hit line names the Wind-up position). Rule 6 of "Cells, sides and 'on you'" and AC-17 only speak of resting positions.
   - Please confirm that this reads acceptably (art-director, as D-014 anticipated). The designer could state whether the carve-out also covers AC-17.
2. **"Never inside 0.9 tile" in AC-28(b).** During the 0.2 s knockback the grub is in flight (14.33 at 0.233 s, 14.42 at 0.217 s). I read the sentence as applying after the knockback ends, and it holds at rest (1.0 tile). The designer may want to say so.
3. **Shot at spawn.** In the draw at the moment of a spit ("1.800 spitter (right) spits") no `*` is visible, because the shot starts in the spitter's own cell and the spitter glyph is drawn over it. The `*` first shows in the 2.00 s draw. The glyph table says the projectile is "visible from spawn to removal". Principle 4 asks for a draw at projectile spawn, and that draw exists. The art-director decides whether this matters.
4. **Weak test.** `test_line_words_match_the_next_draw` is weaker than AC-30(c) (§1).

### 6. Still not observed

- Distance-4 idle run (AC-1/18), dash-away in wind-up (AC-3), projectile dodge and dash-through (AC-9), spitter walk-up (AC-10), multi-hit (AC-12), AC-28(c) in room 2, AC-29(b) and AC-30(b) in play, and the 4 s run for AC-30(a). All of these pass in the suite at both rates.
- Real-room clear, heal and next room, "run complete", run-over screen and restart (AC-13/14, V-8): suite only.
- V-17 defeat and dash-off draws, `z/Z` glyphs (V-4), colour (V-6, reverse video).
- AC-24, 25, 26 in play (suite only).

### 7. Failed before?

- AC-17, AC-22, AC-28(b), V-10, V-14 and V-16 each failed once, in 70. They pass now, so none is failing a second time.
- V-15 failed in 70 and 71 because the manual lacked the text. It is not judged now, because the text is still not placed.
- No criterion goes to `technical-director`.

## Decisions already made

- D-001, D-011, D-012, D-013, D-014 as listed in 76.

## Constraints

- No change to the repo, `manual.md` or the design documents. No spec decisions by QA.

## Open questions

1. **To the Owner:**
   - Run `python3 -m unittest discover -s tests` with the unchanged `manual.md` beside `repo/` and report counts and any failure by name. Expected: 73 tests, 0 failures if the `ManualTest` pair passes (AC-15).
   - Place the V-15 text (lines in 73). QA then checks V-15.
2. **To the art-director:** the live visual review of V-9…V-18 from Appendix A and the build, including the observations in §5 (items 1 and 3), colour and the reverse-video cell.
3. **To the game-designer** (optional): whether AC-17 and rule 6 should say anything about draws made during a Strike (§5 item 1), and the reading of "never inside 0.9 tile" (§5 item 2).
4. **To the Studio:** if a play-view run of the §6 items is wanted before closing, QA can do it in a further Verify round. I consider the suite coverage of those items sufficient for no-failure but not for "observed".

## Expected output

The Studio routes the Owner steps (suite run, V-15 text) and the art-director's visual review. If both come back clean, G-001 Verify can be closed. Appendices A and B hold the captures.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md, design/combat.md, design/combat-visuals.md, manual.md, repo/ (build)
- Decisions: decisions/D-011-grub-turns-stun-body-hit-dash-facing.md, decisions/D-012-on-you-line-for-displaced-enemies.md, decisions/D-013-knockback-of-grub-on-players-tile.md, decisions/D-014-one-rule-for-cells-on-you-and-hit-line-word.md
- Previous handoff: goals/G-001-combat-monotony/76-studio-to-qa.md

---

# Appendix A — verbatim player-view captures of the six setups in 71 (`python3 play.py --view player`)

## A1. Grub on the player's tile, then attack (`room empty`, `player 8 4`, `spawn grub 8 4`, `0.2 attack`, `end 1.5`)

### 30 FPS

```text
Lantern Depths 0.5 — room empty — 30 FPS
   [0.00 s] hearts 3/3
on you: g walking (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.033  a grub rears back (on you)
   [0.03 s] hearts 3/3
on you: G biting soon (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.200  you swipe: grub hit (1 left)
  0.200  the grub is open (on you)
   [0.23 s] hearts 3/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |         )      |
   |        Pw      |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.800  a grub rears back (right)
   [0.80 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PW      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PW      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.333  YOU ARE HIT by a grub (right) — hearts 2/3
   [1.33 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PW      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.450  the grub is open (on you)
   [1.47 s] hearts 2/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 1.50 s: hearts 2/3, enemies left 1
```

### 60 FPS

```text
Lantern Depths 0.5 — room empty — 60 FPS
   [0.00 s] hearts 3/3
on you: g walking (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a grub rears back (on you)
   [0.02 s] hearts 3/3
on you: G biting soon (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.200  you swipe: grub hit (1 left)
  0.200  the grub is open (on you)
   [0.22 s] hearts 3/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |         )      |
   |        Pw      |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.800  a grub rears back (right)
   [0.80 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PW      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PW      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.317  YOU ARE HIT by a grub (right) — hearts 2/3
   [1.32 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PW      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.450  the grub is open (on you)
   [1.45 s] hearts 2/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 1.50 s: hearts 2/3, enemies left 1
```

## A2. One grub on the tile plus one on the tile to its right (`room empty`, `player 8 4`, `spawn grub 8 4`, `spawn grub 9 4`, `end 1`)

### 30 FPS

```text
Lantern Depths 0.5 — room empty — 30 FPS
   [0.00 s] hearts 3/3
on you: g walking (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.033  a grub rears back (on you)
   [0.03 s] hearts 3/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.567  YOU ARE HIT by a grub (on you) — hearts 2/3
   [0.57 s] hearts 2/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.683  the grub is open (on you)
   [0.70 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 1.00 s: hearts 2/3, enemies left 2
```

### 60 FPS

```text
Lantern Depths 0.5 — room empty — 60 FPS
   [0.00 s] hearts 3/3
on you: g walking (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a grub rears back (on you)
   [0.02 s] hearts 3/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.533  YOU ARE HIT by a grub (on you) — hearts 2/3
   [0.53 s] hearts 2/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.667  the grub is open (on you)
   [0.67 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 1.00 s: hearts 2/3, enemies left 2
```

## A3. One grub left, one right, only the right one strikes first (`room empty`, `player 8 4`, `spawn grub 9.25 4`, `spawn grub 6.75 4`, `end 1.5`)

### 30 FPS

```text
Lantern Depths 0.5 — room empty — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.033  a grub rears back (right)
   [0.03 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.600  YOU ARE HIT by a grub (right) — hearts 2/3
   [0.60 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.683  the grub is open (on you)
   [0.70 s] hearts 2/3
on you: g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
on you: g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.033  a grub rears back (left)
   [1.03 s] hearts 2/3
on you: g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
on you: g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 1.50 s: hearts 2/3, enemies left 2
```

### 60 FPS

```text
Lantern Depths 0.5 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a grub rears back (right)
   [0.02 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.567  YOU ARE HIT by a grub (right) — hearts 2/3
   [0.57 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.667  the grub is open (on you)
   [0.67 s] hearts 2/3
on you: g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
on you: g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.017  a grub rears back (left)
   [1.02 s] hearts 2/3
on you: g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
on you: g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 1.50 s: hearts 2/3, enemies left 2
```

The swap (left grub strikes first, spawn order 6.75 then 9.25) was run in the trace view only: hit `pos: 'left'` at 0.600 (30) and 0.567 (60), then the right grub winds up at 1.033 / 1.017 with `side: 'right'`.

## A4. A spit shot hitting the player (`room empty`, `player 8 4`, `spawn spitter 13 4`, `end 5`)

### 30 FPS

```text
Lantern Depths 0.5 — room empty — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.000  spitter (right) charges
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    S  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    S  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.800  spitter (right) spits
   [1.80 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P   *s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P  * s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P*   s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.367  YOU ARE HIT by a spit shot from spitter (right) — hearts 2/3
   [3.37 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.500  spitter (right) charges
   [3.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    S  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [4.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    S  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  4.300  spitter (right) spits
   [4.30 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [4.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P   *s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P  * s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 5.00 s: hearts 2/3, enemies left 1
```

### 60 FPS

```text
Lantern Depths 0.5 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.000  spitter (right) charges
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    S  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    S  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.800  spitter (right) spits
   [1.80 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P   *s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P  * s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P*   s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.333  YOU ARE HIT by a spit shot from spitter (right) — hearts 2/3
   [3.33 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.500  spitter (right) charges
   [3.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    S  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [4.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    S  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  4.300  spitter (right) spits
   [4.30 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [4.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P   *s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P  * s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 5.00 s: hearts 2/3, enemies left 1
```

## A5. Room 2 with four grubs, still player (`room 2`, `end 6`)

### 30 FPS

```text
Lantern Depths 0.5 — room 2 — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |              g |
   |  g             |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |               g|
   | g              |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |   g         g  |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |              g |
   |  g             |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |            g   |
   |    g           |
   |                |
   |        P       |
   |                |
   |             g  |
   |   g            |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |     g      g   |
   |                |
   |        P       |
   |                |
   |            g   |
   |    g           |
   |                |
   +----------------+
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |           g    |
   |      g         |
   |        P       |
   |           g    |
   |    g           |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |      g   g     |
   |        P       |
   |          g     |
   |     g          |
   |                |
   |                |
   +----------------+
  2.733  a grub rears back (top left)
   [2.73 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |       G g      |
   |        P       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |       G g      |
   |        P       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  3.300  YOU ARE HIT by a grub (top left) — hearts 2/3
   [3.30 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |         g      |
   |       GP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  3.383  the grub is open (on you)
   [3.40 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         g      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         g      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  3.733  a grub rears back (top right)
   [3.73 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         G      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [4.00 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         G      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  4.300  YOU ARE HIT by a grub (top right) — hearts 1/3
   [4.30 s] hearts 1/3
on you: g walking (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPG      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  4.383  the grub is open (on you)
   [4.40 s] hearts 1/3
on you: g walking (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [4.50 s] hearts 1/3
on you: g walking (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  4.733  a grub rears back (on you)
   [4.73 s] hearts 1/3
on you: G biting soon (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 1/3
on you: G biting soon (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  5.267  YOU ARE HIT by a grub (on you) — hearts 0/3
  5.267  you went down
   [5.27 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gxg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [5.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gxg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [6.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gxg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
end at 6.00 s: hearts 0/3, enemies left 4
```

### 60 FPS

```text
Lantern Depths 0.5 — room 2 — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |              g |
   |  g             |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |               g|
   | g              |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |   g         g  |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |              g |
   |  g             |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |            g   |
   |    g           |
   |                |
   |        P       |
   |                |
   |             g  |
   |   g            |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |     g      g   |
   |                |
   |        P       |
   |                |
   |            g   |
   |    g           |
   |                |
   +----------------+
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |           g    |
   |      g         |
   |        P       |
   |           g    |
   |    g           |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |      g   g     |
   |        P       |
   |          g     |
   |     g          |
   |                |
   |                |
   +----------------+
  2.733  a grub rears back (top left)
   [2.73 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |       G g      |
   |        P       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |       G g      |
   |        P       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  3.283  YOU ARE HIT by a grub (top left) — hearts 2/3
   [3.28 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |         g      |
   |       GP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  3.383  the grub is open (on you)
   [3.38 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         g      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         g      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  3.733  a grub rears back (top right)
   [3.73 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         G      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [4.00 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         G      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  4.283  YOU ARE HIT by a grub (top right) — hearts 1/3
   [4.28 s] hearts 1/3
on you: g walking (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         G      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  4.383  the grub is open (on you)
   [4.38 s] hearts 1/3
on you: g walking (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [4.50 s] hearts 1/3
on you: g walking (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  4.733  a grub rears back (on you)
   [4.73 s] hearts 1/3
on you: G biting soon (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 1/3
on you: G biting soon (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  5.250  YOU ARE HIT by a grub (on you) — hearts 0/3
  5.250  you went down
   [5.25 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gxg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [5.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gxg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [6.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gxg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
end at 6.00 s: hearts 0/3, enemies left 4
```

## A6. Misses: too far, and enemy not in front

### A6a. Too far (`room empty`, `player 8 4`, `spawn grub 10 4`, `0 attack`, `end 0.5`), 30 FPS

```text
Lantern Depths 0.5 — room empty — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.000  you swipe: (miss) too far
   [0.03 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         )      |
   |        P)g     |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
  0.400  a grub rears back (right)
   [0.40 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 0.50 s: hearts 3/3, enemies left 1
```

### A6a. Too far, 60 FPS

```text
Lantern Depths 0.5 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.000  you swipe: (miss) too far
   [0.02 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         )      |
   |        P)g     |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
  0.383  a grub rears back (right)
   [0.38 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 0.50 s: hearts 3/3, enemies left 1
```

### A6b. Not in front (`room empty`, `player 8 4`, `spawn grub 8 5`, `0 attack`, `end 0.5`), 30 FPS

```text
Lantern Depths 0.5 — room empty — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |        g       |
   |                |
   |                |
   |                |
   +----------------+
  0.000  you swipe: (miss) not in front
  0.033  a grub rears back (below)
   [0.03 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         )      |
   |        P)      |
   |        G)      |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |        G       |
   |                |
   |                |
   |                |
   +----------------+
end at 0.50 s: hearts 3/3, enemies left 1
```

### A6b. Not in front, 60 FPS

```text
Lantern Depths 0.5 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |        g       |
   |                |
   |                |
   |                |
   +----------------+
  0.000  you swipe: (miss) not in front
  0.017  a grub rears back (below)
   [0.02 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         )      |
   |        P)      |
   |        G)      |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |        G       |
   |                |
   |                |
   |                |
   +----------------+
end at 0.50 s: hearts 3/3, enemies left 1
```

---

# Appendix B — AC-28(b) (the 70 failure) and AC-29(a), player view

## B1. AC-28(b): `fps N`, `room empty`, `player 14.5 4`, `spawn grub 14.5 4`, `0.2 attack`, `end 2`

Trace summary (positions at rest): 30 FPS, windup `side: 'on you'` at 0.033, interrupt and knockback at 0.200, grub at 14.33 at 0.233 and at **13.50** from 0.800. Windup `side: 'left'` at 0.800, strike 1.300, hurt `pos: 'left'` at 1.333. 60 FPS: same sequence, grub 14.42 at 0.217, windup `left` at 0.800, hurt `pos: 'left'` at 1.317.

### 30 FPS

```text
Lantern Depths 0.5 — room empty — 30 FPS
   [0.00 s] hearts 3/3
on you: g walking (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              gP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.033  a grub rears back (on you)
   [0.03 s] hearts 3/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              GP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.200  you swipe: grub hit (1 left)
  0.200  the grub is open (on you)
   [0.23 s] hearts 3/3
on you: w open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              wP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              wP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.800  a grub rears back (left)
   [0.80 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              WP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              WP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.333  YOU ARE HIT by a grub (left) — hearts 2/3
   [1.33 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              WP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.450  the grub is open (on you)
   [1.47 s] hearts 2/3
on you: w open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              wP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
on you: w open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              wP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 2/3
on you: w open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              wP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.00 s: hearts 2/3, enemies left 1
```

### 60 FPS

```text
Lantern Depths 0.5 — room empty — 60 FPS
   [0.00 s] hearts 3/3
on you: g walking (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              gP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a grub rears back (on you)
   [0.02 s] hearts 3/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              GP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.200  you swipe: grub hit (1 left)
  0.200  the grub is open (on you)
   [0.22 s] hearts 3/3
on you: w open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              wP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              wP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.800  a grub rears back (left)
   [0.80 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              WP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              WP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.317  YOU ARE HIT by a grub (left) — hearts 2/3
   [1.32 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              WP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.450  the grub is open (on you)
   [1.45 s] hearts 2/3
on you: w open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              wP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
on you: w open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              wP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 2/3
on you: w open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              wP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.00 s: hearts 2/3, enemies left 1
```

## B2. AC-29(a): `fps N`, `room empty`, `player 14.5 4`, `spawn grub 13.5 4`, `end 2`

### 30 FPS

```text
Lantern Depths 0.5 — room empty — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              gP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.033  a grub rears back (left)
   [0.03 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              GP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              GP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.567  YOU ARE HIT by a grub (left) — hearts 2/3
   [0.57 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              GP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.683  the grub is open (on you)
   [0.70 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              gP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              gP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              gP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.583  a grub rears back (on you)
   [1.60 s] hearts 2/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              GP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 2/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              GP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.00 s: hearts 2/3, enemies left 1
```

### 60 FPS

```text
Lantern Depths 0.5 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              gP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a grub rears back (left)
   [0.02 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              GP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              GP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.533  YOU ARE HIT by a grub (left) — hearts 2/3
   [0.53 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              GP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.667  the grub is open (on you)
   [0.67 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              gP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              gP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              gP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.567  a grub rears back (on you)
   [1.57 s] hearts 2/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              GP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 2/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              GP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.00 s: hearts 2/3, enemies left 1
```
>>>END
