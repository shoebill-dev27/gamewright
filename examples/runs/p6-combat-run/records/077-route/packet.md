# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/73-game-designer-to-studio.md
next_seq: 74
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha 74624711b510; run through the project's run commands)
log: last 5 of 29 entries in @log-recent; the full history is goals/G-001-combat-monotony/log.md

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/73-game-designer-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 74
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

- Observe (playtester, qa): done (02, 08, 06, 15, 58, 70). Still unobserved: AC-1, 3, 9, 10, 12, 28(c); real-room clear/heal/next room and "run complete" (AC-13, 14); spitter player-view runs; V-6, V-7, V-8. These go to the next Verify.
- Diagnose, Decide: done (03, 53; D-002, D-005, D-006, D-011). A4 (120° cone), D1 (facing mechanic) and D2 (room 1 composition) are held with revisit triggers in 59.
- Design: spec done (59, 60, 65; D-011, D-012, D-013, AC-19…AC-28, V-9…V-17). Reopened (13c, 72) for three gaps found by Verify 70: cell rule at exactly .5 tile (30 FPS display), meaning of "on you", and which position the hit-line word names.
- Plan: skipped (Waiting behavior local, per 67). Reopen with the Technical Director if the fix for the 30/60 FPS display or hit-line word fails verification a second time.
- Build: AC-19…AC-28 built (67). To fix next (13d): `CrowdTest.test_hit_stun_is_short` fails at both rates (test or build wrong? unknown); D-A display at 30 FPS; D-C hit-line word; plus the 72 rulings. The last suite run: 63 tests, 4 problems (2 `ManualTest` from missing `manual.md` in that environment, 2 hit-stun).
- Verify: 13a QA failed (70): AC-17, AC-22 (suite), AC-28(b) display at 30 FPS, V-10, V-14 (general sentence), V-16, V-15 (manual text, Owner step). Passed: AC-2, 4, 5, 7, 11, 19, 21, 23–27, AC-28 a/d/e, V-9, V-11, V-17. First failure for each failed item, so no TD re-plan. AC-15 failed once earlier (D-008), passed in D-010; a second AC-15 failure goes to the Technical Director. 13b art-director (71): no live view, question; only V-15 judged (fails on the document). V-1…V-4, V-6, V-7, V-9…V-14, V-16, V-17 and the color view are unassessed; the visual review runs after the rebuild, from QA's verbatim captures.
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
| 10-O | Owner: place manual draft (59) and V-15 text | owner | — | open (final V-15 wording follows 13c) | 62-studio-to-owner.md |
| 11 | Plan | technical-director | technical-plan | skipped (Waiting behavior local, per 67; reopen if Verify disagrees) | — |
| 12 | Build (first attempt) | gameplay-engineer | implement-change | done (question: no repo files; Q1 gap) | 61-studio-to-gameplay-engineer.md |
| 12a | Design (Q1 knockback at distance 0, Q2, 3 passages) | game-designer | write-design-spec | done (D-013, AC-28) | 64-studio-to-game-designer.md |
| 12b | Build (re-issue with repo files) | gameplay-engineer | implement-change | done (AC-19…AC-28 built; suite re-run needed) | 66-studio-to-gameplay-engineer.md |
| 13a | Verify | qa | verify-change | done (fail: AC-17, AC-22 suite, AC-28b at 30, V-14/16; V-15 manual) | 70-qa-to-studio.md |
| 13b | Verify (visuals) | art-director | visual-review | done (question: no live view; V-15 fails on document) | 71-art-director-to-studio.md |
| 13c | Design (cell rule at .5, "on you", hit-line word) | game-designer | write-design-spec, make-decision | open | 72-studio-to-game-designer.md |
| 13d | Build (suite test, D-A, D-C, 13c rulings) | gameplay-engineer | implement-change | planned | — |
| 13e-O | Owner: run suite with manual.md (AC-15) | owner | — | planned (after 13d) | — |
| 13f | Verify (rerun; verbatim captures for AD) | qa | verify-change | planned | — |
| 13g | Verify (visuals, from QA captures) | art-director | visual-review | planned | — |
| 14 | Play (rooms 1–5, fresh playtester) | playtester | playtest-session | planned | — |
| 15 | Review | game-director | review-outcome | planned | — |

## Route changes

After 13a/13b (70, 71): 13a failed (AC-17, AC-22 suite, AC-28b display at 30 FPS, V-10/14/16, V-15 manual); first failure of each, so no TD re-plan. Three spec gaps go to Design 13c (72) before Build. 13b was a question (AD could not run the build): not re-asked; visuals are reviewed after the rebuild from QA's captures. No escalation.

## Next action

- `game-designer` runs 13c from `72-studio-to-game-designer.md` and addresses the result to `studio`.
- Then Route: compose Build 13d for `gameplay-engineer` from the 13c rulings plus 70's failures (`test_hit_stun_is_short`, D-A, D-C). No Sender assessment goes on to QA later.
- After Build: Owner runs the suite with the unchanged `manual.md` in place (13e-O, AC-15) and places the V-15 text (10-O stays open; final wording comes with 13c). Then QA re-verifies (13f) and includes verbatim player-view captures of the six setups listed in 71 at 30 and 60 FPS; the art-director then reviews from those captures (13g).
- If 13f and 13g pass: compose a fresh Play handoff (14) for the playtester from the build and player profile only.

## Outcome

(Filled at Close.)
>>>END

<<<FILE @log-recent
## 066-route · 2026-10-16

Status: active. Open: 61-studio-to-gameplay-engineer.md.

After 10c (60): done. The visual spec is text/display only, so no rule change and no escalation. Opened Build (12, 61) and Owner manual placement (10-O, 62) in parallel. 60's "Build updates manual.md" corrected to the D-005 pattern (Owner places). 13b confirmed planned (the view changes).

## 068-route · 2026-10-16

Status: active. Open: 64-studio-to-game-designer.md.

After Build 12 (63, question): Build could not start (no repo files in its packet) and the spec lacks the knockback direction at distance 0. Per the Build return rule, Design re-opens (12a, 64); Build re-issues as 12b with repo files named in Load. No parallel Build, since both touch the same files. No escalation.

## 070-route · 2026-10-16

Status: active. Open: 66-studio-to-gameplay-engineer.md.

After 12a (65): done. Q1 is settled by D-013 and AC-28; Q2 and three passages are clarified. No parameter, input or direction change, so no Decide and no escalation. Build re-issued as 12b (66) with the repo files in Load. 11 stays tentative.

## 072-route · 2026-10-16

Status: active. Open: 68-studio-to-qa.md, 69-studio-to-art-director.md.

After 12b (67): done, fits the plan; no spec gap, no escalation. Opened Verify in parallel: 13a QA (68, no Sender assessment, full suite with manual.md plus bots at 30/60 FPS) and 13b art-director (69). Tentative Plan (11) dropped: Waiting behavior is local.

## 075-route · 2026-10-16

Status: active. Open: 72-studio-to-game-designer.md.

After 13a/13b (70, 71): 13a failed (AC-17, AC-22 suite, AC-28b display at 30 FPS, V-10/14/16, V-15 manual); first failure of each, so no TD re-plan. Three spec gaps go to Design 13c (72) before Build. 13b was a question (AD could not run the build): not re-asked; visuals are reviewed after the rebuild from QA's captures. No escalation.
>>>END

<<<FILE goals/G-001-combat-monotony/73-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 73
from: game-designer
to: studio
stage: Build (the Studio composes the step for gameplay-engineer)
outcome: done
---
# 73: game-designer → studio — Rulings for the three spec gaps (cell at .5, "on you", hit-line word); criteria changed

## Task

Compose the Build step for `gameplay-engineer`. The engineer applies the rulings below and fixes the failing suite test and the display defects from 70. QA then re-verifies the items listed under "QA must re-verify".

## Context

G-001, Option A (D-002). QA's verification (70) failed on three spec gaps (D-A, D-B, D-C). All three are settled in `design/combat.md` ("Cells, sides and 'on you'") and `design/combat-visuals.md`, and recorded in D-014. These are the first Design returns for these items (AC-19…AC-28 and V-9…V-17 were new at 70). I did not edit `manual.md` and did not run `play`/`bots`; the rulings come from reading 70 and `repo/game.py`.

## Findings

### Rulings

1. **Cell at .5 (Gap 1, D-A).** `cell(v) = floor(v + 0.5 + 0.005)` on each axis, used for the player and for enemies. An exact .5 (or up to 0.005 below it) goes to the larger index (right/down). The built code uses `int(round(...))` (`cell_of`), which is Python's round-half-even and is float-noise sensitive at .5, the likely reason for the 30 FPS mismatch. For QA's case the player (14.5) is cell 15 and the grub at 13.5 is cell 14, so the grub is drawn **left** at both rates. Also, the display side of an on-you enemy may only be a cell inside the room: for `player 14.5`, a grub on the tile cannot be shown to the right (cell 16 does not exist), so it is shown and knocked left from the first draw. AC-28(b) now says so.
2. **"On you" (Gap 2, D-B).** On you = true distance to the player ≤ 0.5 tile (the body-hit radius, same test as the swipe; tolerance 1e-6). It is defined once and used for the `on you:` entry, the displaced glyph, "(on you)" in telegraph/open/hit lines, and the knockback. The old 0.05-tile `ON_TILE` for text and knockback goes away. A grub 0.2 tile away now reads "(on you)" in every line, has an entry in the `on you:` line, and is drawn displaced; no draw has a side word and an entry for the same enemy. An enemy farther than 0.5 tile gets a side word and no entry, even when it shares the player's cell (it is then drawn in the cell on the side of its true offset, and that is the side the word names).
3. **Side/corner word of an enemy not on you.** From the cell offset to `P` (left/right/above/below for straight, corner words otherwise). If it shares the player's cell, the side of the larger true-offset axis (tie: horizontal). So the word always matches where the glyph is drawn (new V-18). The distance suffix rule is unchanged (compare words, as before).
4. **Hit-line word (Gap 3, D-C).** For a grub: the position word fixed at the instant the Strike begins (end of Wind-up), stored for that strike and used in the `hurt` event and the hit line. Not the lunge position at the damage tick. A still player gets the same word as in the "rears back" line. For QA's 4.3 s case the expected word is the corner word at both rates (the grub wound up from the top right). A draw made during the 0.15 s Strike may show the lunged glyph; the line still names the Wind-up position. Spitter hit lines are unchanged.
5. **Knockback of an on-you grub (D-013 reworded).** Direction: the side it is drawn on. End point: 1.0 tile from the player's true position on that side (so the glyph lands in the cell it was already drawn in). The normal case (more than 0.5 tile away) stays "straight away". Exactly on the tile the result is the same as before; the only behavioral change is for a grub 0.05–0.5 tile away (before: straight away from the true offset; now: toward its display side, ending 1.0 from the player).

### Changed criteria

- `design/combat.md`: **AC-17** (now AC-1…AC-30, adds identical cells/words), **AC-28** (a) adds the 0.2-tile case, (b) rewritten for the edge (`player 14.5`, shown left from the first draw, ends at x 13.5, same cell and words at both rates), **AC-29** (new, cell at an exact half tile: grub at x 13.5 with player 14.5; ±1 pairs at 8.5), **AC-30** (new, one meaning of on you and of position words, and the hit-line word). AC-23, AC-26 (note only) and the knockback text are reworded without changing their pass conditions.
- `design/combat-visuals.md`: **V-10** (adds: no side word for an entry, no "(on you)" without one), **V-12** (adds the 0.2-tile room 2 case), **V-14** (general sentence now compares with the Wind-up start draw), **V-16** (adds half-tile cells and the Strike-start word), **V-18** (new).
- Unchanged: V-9, V-11, V-13, V-17, V-1…V-8, and every other AC.

### QA must re-verify (both frame rates)

AC-17; AC-28 (a, b, and c if a room 2 on-you run is possible); AC-29; AC-30; V-10, V-12, V-14, V-16, V-18; V-15 after the Owner places the manual text. Also the items from 70 §6 that were not observed (AC-1, AC-3, AC-9, AC-10, AC-12, AC-14 real clear, AC-13 restart, V-2/V-4/V-7/V-8 spitter views) remain open for that round. AC-22 (suite part) is the engineer's `test_hit_stun_is_short` matter.

### Previously passing behavior that changes

- Knockback end point of a grub 0.05–0.5 tile from the player (see ruling 5). AC-28(a) as QA ran it (`spawn grub 8 4`) is unaffected: still 9.00.
- The `_pos`-based words: positions near cell borders may now be named by cell (matches the picture). Scripted left/right cases (V-14, V-11) are unaffected. The `ON_TILE` 0.05 test is replaced by the 0.5 test (the same as `BODY_HIT`) for words and knockback. No timing, damage, hit-test, cap or spacing value changes. AC-2, 4, 5, 7, 11, 19, 21, 23–27 and AC-28 a/d/e do not depend on these and should still pass. If the engineer finds that one does, report it back; do not change a number.
- AC-23(c) note: a grub 0.8 tile behind can share the player's cell (for example the player at x 8.4) and is not on you; it is drawn beside `P` on the side it is offset toward and a swipe prints "(miss) not in front". This is the scenario of AC-30(b).

### Notes for the Studio

- The strike cancel window (AC-26, D-58-1) is one tick wide (0.033 s at 30 FPS). No change; written as is. I added a known-note to AC-26.
- AC-21 has a thin margin (1.97 s, limit 1.9). No change; it will move if the engineer changes spacing or the cap, which these rulings do not.
- The art-director reviews the new wording at Verify (D-006 / D-012 stay valid). One point to look at: a draw during the Strike can show the lunged grub nearer than the hit line names (alternative rejected in D-014).
- This was not an escalation case: no direction, scope or pillar change.

### Final V-15 manual lines (for the Owner to place; manual.md not edited)

The existing draft (65, 71) holds for the glyph table, `x`, arcs, practice room and the `on you:` meaning; the points below replace or sharpen the position wording only.

For `manual.md#on-screen`:
- "If a grub is on you, a line starting `on you:` appears under your hearts. It lists each one with its letter, what it is doing (`walking`, `biting soon`, `open`, `charging`, `idle`) and the side where it is drawn, for example `on you: G biting soon (shown right)`. A letter beside `P` that is named on that line is on your own tile, not beside you. A grub that is on you is always hit by your swipe. When no line appears, nothing is on you."

For `manual.md#what-you-hear-and-read`:
- "Lines that tell you where an enemy is use the same words: `on you` (it is within half a tile of you), `left`, `right`, `above`, `below`, and `top left`, `top right`, `bottom left`, `bottom right`. The word names the side of `P` where the letter is drawn. When two enemies of the same kind would get the same word, a distance is added, for example `left, 1 tile`."
- "When you lose a heart the line says what hit you and where it came from: `YOU ARE HIT by a grub (left)`, `(on you)`, `(top right)`, or `YOU ARE HIT by a spit shot from spitter (top right)`. The place named is where the grub was when it started its bite, which is the place you saw it wind up."
- (Outdated line, not required by a criterion) "`(miss)` alone means nothing was within 2.5 tiles; `(miss) too far` means something is within 2.5 tiles but beyond your reach; `(miss) not in front` means something is within reach but outside your swing."

## Decisions already made

- D-001, D-005, D-007, D-011, D-012, D-013 as in 72.
- **D-014 (new):** the rulings above. D-013 stays in force; its direction/end-point wording is superseded by D-014 where they differ, as described in ruling 5.

## Constraints

- The engineer implements; I specify no code structure. Build must not change any number (timings, 0.5 tile, cap, spacing) beyond the new `on you` radius that equals the existing body-hit radius.
- Must play correctly at both 30 and 60 FPS. `manual.md` is the Owner's.

## Open questions

None for the designer. For the Studio: the art-director's review of the wording at Verify; the Owner's suite run and manual text (as in 70); the engineer's explanation of `CrowdTest.test_hit_stun_is_short`.

## Expected output

Build (`gameplay-engineer`): code changes for rulings 1–5 plus the failing test and the display defects from 70; trace/play evidence at 30 and 60 FPS for AC-28(b), AC-29 and AC-30 before handing to QA. Then Verify (`qa`) with the list above.

## Sender assessment

I am confident in rulings 1–3 and 5 (they follow from the cause that QA reported and from the code). Ruling 4 is a choice between the Strike-start position and the last draw the player saw; I took the Strike-start position because the grub stands still then and it does not depend on the frame. The residual risk is the visual mismatch of a lunged glyph in a draw made inside the 0.15 s Strike, noted for the art-director.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, design/combat.md, design/combat-visuals.md, repo/ (build)
- Decisions: decisions/D-011-grub-turns-stun-body-hit-dash-facing.md, decisions/D-012-on-you-line-for-displaced-enemies.md, decisions/D-013-knockback-of-grub-on-players-tile.md, decisions/D-014-one-rule-for-cells-on-you-and-hit-line-word.md
- Previous handoff: goals/G-001-combat-monotony/70-qa-to-studio.md
>>>END
