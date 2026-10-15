# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/29-qa-to-studio.md
next_seq: 30
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha 13c494fcc634; run through the project's run commands)
log: last 5 of 12 entries in @log-recent; the full history is goals/G-001-combat-monotony/log.md

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/29-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 30
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

- Observe (playtester): done (02 rooms 1–3, 08 rooms 4–5). Not observed: room 5 fight, approaching a spitter, projectile hits, room clear, dash dodging; the Play step after Build covers them.
- Observe (qa): done (06, 15). The doubled spit line is a presentation defect covered by AC-8 and a Build requirement.
- Diagnose: done (03). Cause: single-state, untelegraphed enemy behavior. Option A chosen (D-002); B deferred; C out of scope.
- Decide: done (D-002, D-005).
- Design: done (10, 16). Spec in `design/combat.md` (AC-1…AC-17), run/room rules in D-003, visual spec in `design/combat-visuals.md` (V-1…V-8).
- Plan: done (14, D-004). Gap defaults F1–F11 set by the technical-director; the designer confirms them at Review, F1 (grub speed) matters most.
- Build: done (18, 22, 23). Build 0.5; `manual.md` placed by the Owner (D-005).
- Verify, first pass (26, 27): no AC failed. `ManualTest` has no valid result because QA's workspace lacked `manual.md`. AC-3, 5, 9, 10, 11, 12, 14 rest on the suite only. Pause (F11) is not implemented, not verifiable. The art director had no build output, so only V-5 was checked (pass; the manual omits the `x` color, and the practice room sits under Script, not On-screen, which QA judges for AC-15).
- Verify, second pass: open. QA (28) checks the manual layout or statically, runs independent scripts, and captures raw `run_play`/`run_trace` output and whether the view has color. Then the art director reviews V-1…V-8 from those captures. V-6 may stay "specified, not verified" if the view has no color (art-director's call).
- Play: `playtester` replays the changed build, live and reactive, from a Handoff composed by the Studio from permitted information. Watch slot starvation. Planned.
- Review: experience Goal. `game-director` with `review-outcome`. Planned. Open for the designer: run progression after "run over"; F1, F6, F7; numbering of same-type enemies in one cell; a grub ending on the player's cell; a still player losing 3 hearts in about 3.5–4.5 s (QA 26, tuning).
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
| 7c | Verify (rerun: manual, runs, captures) | qa | verify-change | open | 28-studio-to-qa.md |
| 7d | Verify (visuals, from captures) | art-director | visual-review | planned | — |
| 8 | Play | playtester | playtest-session | planned | — |
| 9 | Review | game-director | review-outcome | planned | — |

## Route changes

After 7a/7b (26, 27; both question): no AC failed. QA's `ManualTest` error came from its workspace lacking `manual.md`; the art director had no build output. Verify reruns as 7c: QA (28) checks the manual layout, runs independent scripts and captures raw output. 7d (art director) opens after 7c with those captures. Play and Review unchanged.

## Next action

Run `28-studio-to-qa.md` (result addressed to `studio`). Then Route:
- If no AC fails, compose the art director's Handoff (7d) with QA's raw captures, then the playtester's Handoff from permitted information only, once both verdicts are in.
- If an AC fails, return to Build with the failure report.
- If QA again gives `ManualTest` no valid result and no static check either, that is a second hand-back for the same input: escalate to the Owner for it.

## Outcome

(Filled at Close.)
>>>END

<<<FILE @log-recent
## 024-route · 2026-10-15

Status: active. Open: 19-studio-to-gameplay-engineer.md.

After step 6a (18, question): code is done, but `manual.md` (T8) could not be written and QA depends on it (AC-15, V-5). Build is reopened as 6b (19), `manual.md` only, with the draft from 18. A second block on the same write goes to the Owner.

## 026-route · 2026-10-15

Status: blocked-on-owner. Open: 19-studio-to-gameplay-engineer.md.

After step 6b (20, question): `manual.md` was blocked a second time for the same missing write access, with nothing new supplied. Loop limit reached, so the Goal is `blocked-on-owner` and Escalation 21 asks the Owner to place the draft (A), grant write access (B) or skip it (C). Route unchanged.

## 028-resume · 2026-10-15

Status: active. Open: 22-studio-to-gameplay-engineer.md.

Resume after Owner decision D-005 (Option A of Escalation 21): the Owner placed the draft `manual.md` unchanged. The Goal is `active` again. Step 6b is narrowed to a `run_tests` check (22). If it gives 34/34, Verify opens as two parallel steps. The rest of the route is unchanged.

## 030-route · 2026-10-15

Status: active. Open: 24-studio-to-qa.md, 25-studio-to-art-director.md.

After step 6b (23): `run_tests` was 33/34 only because the engineer's workspace lacked `manual.md`; the draft's text is statically consistent. Not an Owner matter, so Verify opens as parallel 7a (QA, also runs `ManualTest` with the manual placed) and 7b (visuals). Rest unchanged.

## 033-route · 2026-10-15

Status: active. Open: 28-studio-to-qa.md.

After 7a/7b (26, 27; both question): no AC failed. QA's `ManualTest` error came from its workspace lacking `manual.md`; the art director had no build output. Verify reruns as 7c: QA (28) checks the manual layout, runs independent scripts and captures raw output. 7d (art director) opens after 7c with those captures. Play and Review unchanged.
>>>END

<<<FILE goals/G-001-combat-monotony/29-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 29
from: qa
to: studio
stage: Verify
outcome: question
---
# 29: qa → studio — second verification round of Build 0.5: no failing criterion, but ManualTest still has no test result, AC-14 is suite-only, and one telegraph-readability gap needs a design ruling

## Task

Report the second verification round of Build 0.5 against `design/combat.md` (AC-1…AC-17) at 30 and 60 FPS. The round covered the manual check, independent runs for the criteria that were suite-only, and raw captures.

## Context

Handoff 28 asked for A (ManualTest and AC-15), B (independent runs) and C (raw captures). I did not edit the build or `manual.md`. All evidence below comes from `run_tests`, `run_play` and `run_trace` output in this step's run results.

## Findings

### Verdict: `question`

No criterion was observed failing. I cannot give `pass` for three reasons:

1. **ManualTest has no valid result.** I could not build the scratch layout, so I only did a static check (section A).
2. **AC-14 is still suite-only.** I did not run a full room clear myself.
3. **A spec gap affects telegraph readability.** When a grub stands on the player's tile, the player view shows no threat glyph (finding F1). The spec is silent on overlap, so this goes to `game-designer`.

Pause (F11) stays not verifiable.

### run_tests totals

- Command: `python3 -m unittest discover -s tests`. Exit 1. 34 tests ran: **33 passed, 0 failed, 1 error**.
- The error is `ManualTest.test_manual_lists_glyphs_and_lines`: `FileNotFoundError: /manual.md`. The run happened with the repo at `/work`, so the test looked in `/`.
- **ManualTest: no test run, no pass/fail mark.**
- **Why the scratch layout was blocked:** `ManualTest` needs `manual.md` in the directory above `repo/`. My allowed writes are this handoff and `@run` blocks, and no `@run` block was allowed to carry `repo/` files or a file in the parent of `repo/`. I cannot create a `manual.md` beside the repo copy, and I did not write into the project's own paths. Fixing this needs a layout where `manual.md` sits beside `repo/` (for example, a QA workspace that allows writing the parent directory).

### A. Static check of the manual (not a test run)

Method: I read the glyph table in `repo/play.py`, the phrases `ManualTest` requires, and `manual.md`, and compared them by eye.

- **Glyphs.** The test looks for each `` `char` `` in the manual. Build glyphs are `P x * ) ( ^ v g G w W s S z Z`. All appear backticked in the manual's On screen table: `P`, `x`, `g`, `G`, `w`, `W`, `s`, `S`, `z`, `Z`, `*`, and `` `)` `(` `^` `v` ``. No difference found.
- **Phrases.** All twelve required phrases appear in `manual.md`. No difference found:
  - "room empty", "rears back", "is open", "charges", "spits", "run over", "press attack to start again"
  - "(miss)", "(too soon)", "(stunned)", "(down)", "room cleared"
- **Result:** the static check found no missing or differing item. This supports AC-15 but is not a test result.
- **Where the practice room is described.** The practice room (`room empty`) appears in the Script table and in "Rooms and runs". The `x` marker is in the On screen table. The practice room is **not** in the On screen section.
  - AC-15 reads "`x` and the practice room are in the manual". By that wording, AC-15 is met.
  - The body text of the spec's Practice room (Q4) section says both must be listed in `manual.md#on-screen`. Taken literally, that is not met for the practice room.
  - I judge AC-15 as met, and I flag the difference between AC wording and body text as a spec question for the game-designer. I did not change anything.

### B. Independent runs, per criterion

"Observed" means I read it in this round's player-view or trace output. "Suite" means a repo test I did not re-derive. Earlier-round observations are marked "round 1".

| AC | Result | Evidence |
|---|---|---|
| AC-1 grub telegraph | pass, observed (and round 1) | Idle player, grub at distance 4: "a grub rears back (right)" and `G` at 1.400 (30 FPS) / 1.383 (60 FPS). First heart lost at 1.967 / 1.933, so about 0.55 s of warning. No heart lost during Approach or Recovery. **See F1** for later bites. |
| AC-2 grub timing | pass, observed (round 1 traces) | Windup→strike 0.500 at both frame rates. Strike→recover 0.167 at 30 FPS and 0.150 at 60 FPS. Recover→next windup 0.900. |
| AC-3 grub dodge | pass, observed | Dash left at 1.500 during the wind-up (1.400–1.900). Hearts stayed 3/3 to the end (3.5 s) at both frame rates. The grub showed `G` at 2.00 with the player 4 tiles away, then "the grub is open" at 2.050 / 2.033. This is one dash timing per frame rate, so the suite's offsets 0 / 0.25 / 0.45 remain suite evidence. |
| AC-4 grub counter | pass, observed | Swipe at 2.500 in Recovery: "grub hit (1 left)" and `w` glyph. Next hit on the player at 3.500 (30 FPS) vs 1.967 before = 1.533 s. At 60 FPS 3.483 vs 1.933 = 1.550 s. |
| AC-5 interrupt | pass, observed | Swipe at 1.600 during the wind-up: "grub hit (1 left)", then "the grub is open (right)" at the same time. Trace at 1.633 (30 FPS): grub `hp=1, recovery, 0.567`, event `recover {'cause': 'interrupted'}` and `knockback`. 60 FPS: `recovery, 0.583` at 1.617. No heart lost from that strike. The next bite is a fresh wind-up at 2.667 / 2.683, with the first hit on the player at 3.233 at both frame rates. |
| AC-6 attack limit | pass (round 1 observed, suite) | Not re-run this round. |
| AC-7 spitter stagger | pass, observed | Room 4 player view at both frame rates: charges at 1.000 (top right) and 1.800 (bottom right), repeats at 3.500 and 4.300. |
| AC-8 spitter telegraph | pass, observed | "spitter (top right) charges" at 1.000 with `S`, and the spit at 1.800 (0.8 s later). Two different lines at 1.800: "spitter (top right) spits" and "spitter (bottom right) charges". No identical duplicate lines at one timestamp (rooms 3, 4, and the single-spitter runs). |
| AC-9 projectile dodge | pass, observed | Spitter at 13,4 (charge 1.000, spit 1.800). **Still player:** "YOU ARE HIT by a shot — hearts 2/3" at 3.367 (30 FPS) / 3.333 (60 FPS). **Move up** 2.0–2.5: hearts 3/3 to the end, the shot passed below. **Dash right** at 3.1: hearts 3/3 to the end, the shot continued past. |
| AC-10 spitter approach | pass for the cancel, observed. The 2-swipe kill is suite only | Cancel: swipe at 1.200 during the charge gives "spitter hit (1 left)" and "spitter (center) is staggered", with no spit at 1.8. The next charge starts at 2.200 (1.0 s after the hit) and spits at 3.000. Same at both frame rates. In room 3 I walked to the top-left spitter and swiped at 2.500: "spitter hit (1 left)", `z` glyph. My first swipe at 2.05 was "(stunned)" because I had walked into a shot at 2.033, so I did not observe the second swipe defeating it. The 2-swipe kill is suite only (`test_walk_up_and_defeat_a_spitter`). |
| AC-11 hit feedback | partial: observed for "hit (1 left)", "(miss)", "(stunned)" and the glyph change. "(too soon)" and "(down)" are suite only | Observed: "you swipe: grub hit (1 left)" with `g`→`w`, "you swipe: spitter hit (1 left)" with `s`→`z`, "you swipe: (miss)" at 0.500 in the multi-hit script, "you swipe: (stunned)" at 2.067 in room 3. No "(nothing happens)" seen. The `G`/`W`/`Z` alert glyphs are distinct from the harmless ones. |
| AC-12 multi-hit | pass, observed | Two grubs inside the cone: two lines at 0.000, "you swipe: grub hit (1 left)" ×2, and the draw shows both as `w`. Same at both frame rates. |
| AC-13 zero hearts | pass, observed (extends round 1) | Room 1, no input: "YOU ARE HIT … 0/3" and "you went down" at 4.967 (30 FPS) / 4.950 (60 FPS). `x` replaces `P`. Trace shows all grubs `approach` (none committed) and `shots=0` after the down. "run over — rooms cleared: 0" and "press attack to start again" at 6.967 / 6.950 (2.000 s after down). An attack at 15.000 printed "a new run begins" and "room 1 begins" with hearts 3/3 and three grubs at their start positions. Room 4 also showed the shots disappear at the down. The "(down)" reason for an attack while down is suite only. |
| AC-14 room clear | pass, suite only | I did not run a full clear (no scripted kill of a whole room, no clear while a strike was due). Suite: `test_room_clear`, `test_clearing_room_5_completes_the_run`. |
| AC-15 practice room and manual | pass by the AC wording, static check only; ManualTest not run | See section A. |
| AC-16 room mix | pass, observed | Room 3 trace setup row: 3 spitters at (2,1), (14,7), (2,7); first charge 1.000 / 1.800 / 2.600. Round 1: room 5 setup row 3 grubs + 2 spitters. Suite: `test_layouts`. |
| AC-17 frame rate | pass for what I observed; the suite-only parts stay suite | The same scripts at 30 and 60 FPS give the same event sequences. Timestamp differences are at most 0.034 s: windup 1.400/1.383, first hit 1.967/1.933, down 5.033/5.000, run over 6.967/6.950. Spits, charges and the dash landing match exactly (dash left 4 tiles: `P` from column 8 to 4 at both). The Strike ≥4 frames at 30 FPS check is suite only. |

### Findings that are not criterion failures

- **F1 (spec gap, for game-designer): the threat glyph is hidden when a grub is on the player's tile.**
  - After a few bites the grub ends up at the player's position (`side: on you`). The player is drawn last, so only `P` shows.
  - Evidence, idle 30 FPS: at 4.500 the line "a grub rears back (on you)" prints, and the draw at 4.50 shows only `P`. The hit lands at 5.033. Room 1 shows the same at 3.57–4.50.
  - The Conventions define a telegraph as at least one on-map change plus a text line. In that situation the on-map change is missing, and pillar 3 says every threat is visible before it hurts.
  - AC-1 itself (first bite from distance 4) is met. The spec is silent on whether enemies may overlap the player. Needed: a ruling (keep distance, or draw the threat). Not marked a failure.
- **F2 (cosmetic): out-of-order timestamps in the player view.** At 30 FPS in room 4 with a dash, "2.600 spitter (bottom right) spits" prints before "2.583 the grub is open (left)", and "3.500 … charges" before "3.483 a grub rears back (left)". Nothing in the spec is affected.
- **Run-over timing.** In a practice room (grub only) the session ends after the down without a run-over screen, as designed (`end at 7.03 s`).

### Answer on color

- With the `run_play` command as given (no `--color`, output not a terminal), the player view is **plain text**. None of the captures contain ANSI codes or markup.
- From `play.py`: color is added only with `--color` or when stdout is a terminal. Then each glyph is wrapped like `ESC[38;5;229mPESC[0m` (lantern yellow for the player), with `ESC[1;38;5;202m` for alert enemies and `ESC[1;38;5;196m` for shots. I did not capture a colored run, so this is from reading the code. The glyphs carry every state without color.

### Captures

All output is verbatim from this step's runs. Cuts are marked `[cut: …]`. Where I cut draws, every text line (events) is kept in order. Draws are kept at the events named in each heading. Each capture is shown at 30 FPS and 60 FPS.

#### C1. Practice room, one grub, idle player (`room empty`, `player 8 4`, `spawn grub 12 4`, `end 8`) — 30 FPS

```text
Lantern Depths 0.5 — room empty — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
[cut: draws at 0.50 s and 1.00 s; grub walking left, player unchanged]
  1.400  a grub rears back (right)
   [1.40 s] hearts 3/3
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
[cut: draw at 1.50 s, identical to the 1.40 s draw]
  1.967  YOU ARE HIT by a grub — hearts 2/3
   [1.97 s] hearts 2/3
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
[cut: draw at 2.00 s, identical]
  2.050  the grub is open (right)
   [2.07 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
[cut: draw at 2.50 s, identical to the 2.07 s draw]
  2.950  a grub rears back (right)
[cut: draws at 2.97 s, 3.00 s: only `P` in the room]
  3.467  YOU ARE HIT by a grub — hearts 1/3
[cut: draws at 3.47 s, 3.50 s]
  3.600  the grub is open (on you)
[cut: draws at 3.60 s, 4.00 s: only `P`]
  4.500  a grub rears back (on you)
   [4.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
[cut: draw at 5.00 s]
  5.033  YOU ARE HIT by a grub — hearts 0/3
  5.033  you went down
   [5.03 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        x       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
[cut: draws at 5.50, 6.00, 6.50, 7.00 s, all with `x` alone]
end at 7.03 s: hearts 0/3, enemies left 1
```

60 FPS (same script):

```text
Lantern Depths 0.5 — room empty — 60 FPS
[cut: draws at 0.00, 0.50, 1.00 s; same as 30 FPS]
  1.383  a grub rears back (right)
   [1.38 s] hearts 3/3
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
[cut: draw at 1.50 s, identical]
  1.933  YOU ARE HIT by a grub — hearts 2/3
   [1.93 s] hearts 2/3
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
[cut: draw at 2.00 s (only `P`)]
  2.033  the grub is open (right)
[cut: draws at 2.03, 2.50 s]
  2.933  a grub rears back (right)
[cut: draws at 2.93, 3.00 s]
  3.450  YOU ARE HIT by a grub — hearts 1/3
[cut: draws at 3.45, 3.50 s]
  3.583  the grub is open (on you)
[cut: draws at 3.58, 4.00 s]
  4.483  a grub rears back (on you)
   [4.48 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
[cut: draw at 4.50 s]
  5.000  YOU ARE HIT by a grub — hearts 0/3
  5.000  you went down
   [5.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        x       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
[cut: draws at 5.50, 6.00, 6.50, 7.00 s]
end at 7.00 s: hearts 0/3, enemies left 1
```

Trace for timing (30 FPS, selected lines; full trace was run):

```text
t=1.400 frame=42 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.25,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=1.900 frame=57 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.25,4.00,hp=2,strike,0.150) | strike {'who': 0}
t=1.967 frame=59 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 shots=0 | grub#0(8.81,4.00,hp=2,strike,0.083) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.067 frame=62 room=empty phase=playing pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.700 stun_left=0.200 shots=0 | grub#0(8.25,4.00,hp=2,recovery,0.883) | recover {'cause': 'strike', 'who': 0, 'side': 'right'}
```

#### C2. Same, `1.6 attack` during the wind-up (`end 5`) — 30 FPS

```text
Lantern Depths 0.5 — room empty — 30 FPS
[cut: draws at 0.00, 0.50, 1.00 s; as in C1]
  1.400  a grub rears back (right)
   [1.40 s] hearts 3/3
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
[cut: draw at 1.50 s, identical]
  1.600  you swipe: grub hit (1 left)
  1.600  the grub is open (right)
   [1.63 s] hearts 3/3
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
[cut: draws at 2.00, 2.50 s: `P w`]
  2.667  a grub rears back (right)
   [2.67 s] hearts 3/3
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
[cut: draw at 3.00 s, identical]
  3.233  YOU ARE HIT by a grub — hearts 2/3
  3.317  the grub is open (right)
[cut: draws at 3.23, 3.33, 3.50, 4.00 s]
  4.217  a grub rears back (right)
[cut: draws at 4.23, 4.50 s]
  4.733  YOU ARE HIT by a grub — hearts 1/3
  4.867  the grub is open (on you)
[cut: draws at 4.73, 4.87, 5.00 s]
end at 5.00 s: hearts 1/3, enemies left 1
```

Trace line at the swipe (30 FPS): 

```text
t=1.633 frame=49 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.42,4.00,hp=1,recovery,0.567) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)]}; recover {'cause': 'interrupted', 'who': 0, 'side': 'right'}; knockback {'who': 0}
```

60 FPS (same script):

```text
Lantern Depths 0.5 — room empty — 60 FPS
[cut: draws at 0.00, 0.50, 1.00 s]
  1.383  a grub rears back (right)
[cut: draws at 1.38, 1.50 s: `PG`]
  1.600  you swipe: grub hit (1 left)
  1.600  the grub is open (right)
   [1.62 s] hearts 3/3
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
[cut: draws at 2.00, 2.50 s]
  2.683  a grub rears back (right)
[cut: draws at 2.68, 3.00 s: `PW`]
  3.233  YOU ARE HIT by a grub — hearts 2/3
  3.333  the grub is open (right)
[cut: draws at 3.23, 3.33, 3.50, 4.00 s]
  4.233  a grub rears back (right)
[cut: draws at 4.23, 4.50 s]
  4.750  YOU ARE HIT by a grub — hearts 1/3
  4.883  the grub is open (on you)
[cut: draws at 4.75, 4.88, 5.00 s]
end at 5.00 s: hearts 1/3, enemies left 1
```

Trace line at the swipe (60 FPS):

```text
t=1.617 frame=97 room=empty phase=playing pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 shots=0 | grub#0(9.33,4.00,hp=1,recovery,0.583) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)]}; recover {'cause': 'interrupted', 'who': 0, 'side': 'right'}; knockback {'who': 0}
```

#### C3. Same, `2.5 attack` during the recovery (`end 6`) — 30 FPS

```text
Lantern Depths 0.5 — room empty — 30 FPS
[cut: draws at 0.00 to 1.50 s, as in C1; wind-up line follows]
  1.400  a grub rears back (right)
  1.967  YOU ARE HIT by a grub — hearts 2/3
  2.050  the grub is open (right)
[cut: draws at 1.40, 1.50, 1.97, 2.00, 2.07 s, as in C1]
  2.500  you swipe: grub hit (1 left)
   [2.53 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |         )      |
   |        P)      |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
  2.950  a grub rears back (right)
   [2.97 s] hearts 2/3
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
[cut: draw at 3.00 s, identical]
  3.500  YOU ARE HIT by a grub — hearts 1/3
  3.600  the grub is open (right)
[cut: draws at 3.50, 3.60, 4.00 s]
  4.500  a grub rears back (right)
[cut: draws at 4.50, 5.00 s]
  5.033  YOU ARE HIT by a grub — hearts 0/3
  5.033  you went down
[cut: draws at 5.03, 5.50, 6.00 s: `x`]
end at 6.00 s: hearts 0/3, enemies left 1
```

60 FPS: swipe at 2.500 "you swipe: grub hit (1 left)" (draw [2.52 s] identical to the one above), then 2.933 "a grub rears back (right)", 3.483 "YOU ARE HIT … 1/3", 3.583 "the grub is open (right)", 4.483 "a grub rears back (right)", 5.000 "YOU ARE HIT … 0/3" / "you went down", `end at 6.00 s`. Lines kept as printed; draws cut.

#### C4. Room 4, `0.5 move left`, `end 8` — 30 FPS (draws only at key events)

```text
Lantern Depths 0.5 — room 4 — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |               s|
   |g               |
   |                |
   |                |
   | g      P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
[cut: draw at 0.50 s]
  1.000  spitter (top right) charges
   [1.00 s] hearts 3/3
   +----------------+
   |               S|
   |                |
   |  g             |
   |                |
   |   g  P         |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  1.300  a grub rears back (left)
   [1.30 s] hearts 3/3
   +----------------+
   |               S|
   |                |
   |  g             |
   |                |
   |    GP          |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
[cut: draw at 1.50 s]
  1.733  a grub rears back (above)
  1.800  spitter (top right) spits
  1.800  spitter (bottom right) charges
  1.833  YOU ARE HIT by a grub — hearts 2/3
  1.950  the grub is open (right)
  2.383  the grub is open (above)
  2.600  spitter (bottom right) spits
  2.850  a grub rears back (right)
  3.283  a grub rears back (above)
  3.367  YOU ARE HIT by a grub — hearts 1/3
  3.500  spitter (top right) charges
  3.500  the grub is open (on you)
  3.933  the grub is open (on you)
  4.300  spitter (top right) spits
  4.300  spitter (bottom right) charges
  4.400  a grub rears back (on you)
  4.833  a grub rears back (on you)
[cut: draws for 1.73 to 4.83 s; all text lines above kept, in order]
  4.933  YOU ARE HIT by a grub — hearts 0/3
  4.933  you went down
   [4.93 s] hearts 0/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |   x            |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
[cut: draws at 5.00, 5.50, 6.00, 6.50 s, all like the 4.93 s draw]
  6.933  run over — rooms cleared: 0
  6.933  press attack to start again
end at 6.93 s: hearts 0/3, enemies left 4
```

60 FPS (same script), text lines as printed: 1.000 "spitter (top right) charges"; 1.300 "a grub rears back (left)"; 1.733 "a grub rears back (above)"; 1.800 "spitter (top right) spits" and "spitter (bottom right) charges"; 1.817 "YOU ARE HIT by a grub — hearts 2/3"; 1.950 "the grub is open (right)"; 2.383 "the grub is open (above)"; 2.600 "spitter (bottom right) spits"; 2.850 "a grub rears back (right)"; 3.283 "a grub rears back (above)"; 3.367 "YOU ARE HIT by a grub — hearts 1/3"; 3.500 "spitter (top right) charges" and "the grub is open (on you)"; 3.933 "the grub is open (on you)"; 4.300 "spitter (top right) spits" and "spitter (bottom right) charges"; 4.400 "a grub rears back (on you)"; 4.833 "a grub rears back (on you)"; 4.917 "YOU ARE HIT by a grub — hearts 0/3" and "you went down" (draw [4.92 s] has `x` at column 4 and shots gone); 6.917 "run over — rooms cleared: 0" and "press attack to start again"; `end at 6.92 s: hearts 0/3, enemies left 4`. Draws cut.

#### C5. Room 4, `0.5 dash left`, `end 8` — 30 FPS

```text
Lantern Depths 0.5 — room 4 — 30 FPS
[cut: draws at 0.00, 0.50 s, as in C4]
  0.500  you dash left
  0.900  a grub rears back (left)
   [0.90 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |  g             |
   |                |
   |   GP           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  1.000  spitter (top right) charges
  1.467  YOU ARE HIT by a grub — hearts 2/3
  1.550  the grub is open (left)
  1.800  spitter (top right) spits
  1.800  spitter (bottom right) charges
  1.933  a grub rears back (left)
  2.450  a grub rears back (left)
  2.500  YOU ARE HIT by a grub — hearts 1/3
  2.600  spitter (bottom right) spits
  2.583  the grub is open (left)
  3.100  the grub is open (on you)
  3.500  spitter (top right) charges
  3.483  a grub rears back (left)
[cut: draws between 1.00 and 3.50 s; text lines kept in printed order]
  4.000  YOU ARE HIT by a grub — hearts 0/3
  4.000  you went down
[cut: draws at 4.00 to 5.50 s]
  6.000  run over — rooms cleared: 0
  6.000  press attack to start again
end at 6.00 s: hearts 0/3, enemies left 4
```

60 FPS lines: 0.500 "you dash left"; 0.883 "a grub rears back (left)"; 1.000 charge; 1.433 "YOU ARE HIT … 2/3"; 1.533 open; 1.800 spit + charge; 1.917 rears back; 2.433 rears back; 2.467 "YOU ARE HIT … 1/3"; 2.567 open; 2.600 "spitter (bottom right) spits"; 3.083 "the grub is open (on you)"; 3.467 rears back; 3.500 "spitter (top right) charges"; 3.983 "YOU ARE HIT … 0/3" / "you went down"; 5.983 "run over — rooms cleared: 0" / "press attack to start again"; `end at 5.98 s`.

#### C6. Room 3, walk up to a spitter and attack twice (`0 move up`, `0.75 move left`, `2.0 stop`, `2.05 attack`, `2.5 attack`, `end 3.5`) — 30 FPS

```text
Lantern Depths 0.5 — room 3 — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
[cut: draw at 0.50 s]
  1.000  spitter (top left) charges
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |  S    P        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
[cut: draw at 1.50 s]
  1.800  spitter (top left) spits
  1.800  spitter (bottom right) charges
   [1.80 s] hearts 3/3
   +----------------+
   |                |
   |  s P           |
   |                |
   |                |
   |                |
   |                |
   |                |
   |  s           S |
   |                |
   +----------------+
[cut: draw at 2.00 s]
  2.033  YOU ARE HIT by a shot — hearts 2/3
   [2.03 s] hearts 2/3
   +----------------+
   |                |
   |  sP            |
   |                |
   |                |
   |                |
   |                |
   |                |
   |  s           S |
   |                |
   +----------------+
  2.067  you swipe: (stunned)
[cut: draw at 2.50 s, identical to the 2.03 s draw]
  2.500  you swipe: spitter hit (1 left)
   [2.53 s] hearts 2/3
   +----------------+
   |  (             |
   |  zP            |
   |                |
   |                |
   |                |
   |                |
   |                |
   |  s           S |
   |                |
   +----------------+
  2.600  spitter (bottom right) spits
  2.600  spitter (bottom left) charges
[cut: draws at 2.60, 3.00 s]
  3.400  spitter (bottom left) spits
  3.500  spitter (top left) charges
[cut: draws at 3.40, 3.50 s; at 3.50 s the hit spitter shows `Z`]
end at 3.50 s: hearts 2/3, enemies left 3
```

60 FPS (same script): the same sequence: 1.000 charge, 1.800 spit + "spitter (bottom right) charges", 2.017 "YOU ARE HIT by a shot — hearts 2/3", 2.050 "you swipe: (stunned)", 2.500 "you swipe: spitter hit (1 left)" (draw [2.52 s] shows `(` above and below the `zP` row), 2.600 spit + "spitter (bottom left) charges", 3.400 spit, 3.500 "spitter (top left) charges", `end at 3.50 s: hearts 2/3, enemies left 3`.

#### C7. Room 1, no input, then `15 attack` after the run-over screen (`end 20`) — 30 FPS

```text
Lantern Depths 0.5 — room 1 — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |        g       |
   |                |
   |                |
   |                |
   |   g    P      g|
   |                |
   |                |
   |                |
   |                |
   +----------------+
[cut: draws at 0.50, 1.00 s]
  1.400  a grub rears back (above)
  1.900  a grub rears back (left)
  1.967  YOU ARE HIT by a grub — hearts 2/3
  2.050  the grub is open (above)
  2.550  the grub is open (left)
  2.900  a grub rears back (right)
  2.950  a grub rears back (above)
  3.467  YOU ARE HIT by a grub — hearts 1/3
  3.550  the grub is open (right)
  3.567  a grub rears back (left)
  3.600  the grub is open (on you)
  4.217  the grub is open (on you)
  4.450  a grub rears back (right)
  4.500  a grub rears back (on you)
[cut: draws between 1.40 and 4.50 s; text lines kept]
  4.967  YOU ARE HIT by a grub — hearts 0/3
  4.967  you went down
   [4.97 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        x       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
[cut: draws at 5.00, 5.50, 6.00, 6.50 s, all `x` alone]
  6.967  run over — rooms cleared: 0
  6.967  press attack to start again
 15.000  a new run begins
 15.000  room 1 begins
   [15.03 s] hearts 3/3
   +----------------+
   |        g       |
   |                |
   |                |
   |                |
   |   g    P      g|
   |                |
   |                |
   |                |
   |                |
   +----------------+
[cut: second run, identical to the first from 15.50 s; lines kept:]
 16.400  a grub rears back (above)
 16.900  a grub rears back (left)
 16.967  YOU ARE HIT by a grub — hearts 2/3
 17.050  the grub is open (above)
 17.550  the grub is open (left)
 17.900  a grub rears back (right)
 17.950  a grub rears back (above)
 18.467  YOU ARE HIT by a grub — hearts 1/3
 18.550  the grub is open (right)
 18.567  a grub rears back (left)
 18.600  the grub is open (on you)
 19.217  the grub is open (on you)
 19.450  a grub rears back (right)
 19.500  a grub rears back (on you)
 19.967  YOU ARE HIT by a grub — hearts 0/3
 19.967  you went down
[cut: draws in this second run]
end at 20.00 s: hearts 0/3, enemies left 3
```

60 FPS: down at 4.950 ("YOU ARE HIT by a grub — hearts 0/3", "you went down"), "6.950  run over — rooms cleared: 0", "6.950  press attack to start again", " 15.000  a new run begins", " 15.000  room 1 begins" (draw [15.02 s] same as the start layout, hearts 3/3), second run down at 19.950, `end at 20.00 s: hearts 0/3, enemies left 3`. The full trace (60 FPS) shows `run_over {'rooms': 0, 'complete': False}` at t=6.950 and `run_start; room_loaded {'room': '1'}` at t=15.017 with hearts=3.

#### C8. Independent checks (AC-3, AC-9, AC-10, AC-12)

AC-3, grub dash during wind-up (`spawn grub 12 4`, `1.5 dash left`, `end 3.5`), 30 FPS:

```text
  1.400  a grub rears back (right)
   [1.40 s] hearts 3/3
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
[cut: draw at 1.50 s]
  1.500  you dash left
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |    P    G      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.050  the grub is open (right)
[cut: draws at 2.07 to 3.50 s: `P   g`]
end at 3.50 s: hearts 3/3, enemies left 1
```

60 FPS: wind-up 1.383, "1.500 you dash left", draw [2.00 s] `|    P   G       |`, "2.033 the grub is open (right)", `end at 3.50 s: hearts 3/3, enemies left 1`.

AC-9 still / side-step / dash through (spitter at 13,4, player 8,4, `end 4.2`). Text lines at 30 FPS; 60 FPS differs only as noted.

```text
-- still --
  1.000  spitter (right) charges
  1.800  spitter (right) spits
  3.367  YOU ARE HIT by a shot — hearts 2/3
  3.500  spitter (right) charges
end at 4.20 s: hearts 2/3, enemies left 1
(60 FPS: hit at 3.333)
-- move up 2.0, stop 2.5 --
  1.000  spitter (right) charges
  1.800  spitter (right) spits
  3.500  spitter (right) charges
end at 4.20 s: hearts 3/3, enemies left 1
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |        P       |
   |                |
   |           * s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
-- dash right 3.1 --
  1.000  spitter (right) charges
  1.800  spitter (right) spits
  3.100  you dash right
  3.500  spitter (right) charges
end at 4.20 s: hearts 3/3, enemies left 1
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        *   PS  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
```

The 60 FPS runs print the same lines and draws (still: hit at 3.333; side-step and dash: hearts 3/3 at the end).

AC-10 hit during the charge (`spawn spitter 9.2 4`, `1.2 attack`, `end 3.0`), 30 FPS:

```text
  1.000  spitter (center) charges
  1.200  you swipe: spitter hit (1 left)
  1.200  spitter (center) is staggered
   [1.23 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         )      |
   |        Pz      |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
[cut: draws at 1.50, 2.00 s: `Pz`]
  2.200  spitter (center) charges
   [2.20 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PZ      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
[cut: draw at 2.50 s]
  3.000  spitter (center) spits
[cut: draw at 3.00 s]
end at 3.00 s: hearts 3/3, enemies left 1
```

60 FPS: identical lines (1.000, 1.200 ×2, 2.200, 3.000), draw [1.22 s] same as above, `end at 3.00 s: hearts 3/3, enemies left 1`. The spit at 3.000 hit nothing because the player stayed at hearts 3/3 (the shot flies away from the adjacent spitter; I did not trace where it went).

AC-12 multi-hit (`spawn grub 9.2 4`, `spawn grub 9 3.2`, `0 attack`, `0.5 attack`, `end 1.5`), 30 FPS:

```text
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         g      |
   |        Pg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.000  you swipe: grub hit (1 left)
  0.000  you swipe: grub hit (1 left)
   [0.03 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         w      |
   |        Pw      |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
[cut: draw at 0.50 s]
  0.500  you swipe: (miss)
[cut: draw at 0.53 s]
  0.700  a grub rears back (right)
  0.733  a grub rears back (right)
  1.267  YOU ARE HIT by a grub — hearts 2/3
  1.350  the grub is open (right)
  1.383  the grub is open (right)
[cut: draws at 0.70 to 1.50 s]
end at 1.50 s: hearts 2/3, enemies left 2
```

60 FPS: the same lines at 0.000 (two hit lines), 0.500 "(miss)", 0.683 and 0.717 "a grub rears back (right)", 1.233 hit, 1.333 and 1.367 "the grub is open (right)", `end at 1.50 s: hearts 2/3, enemies left 2`.

## Decisions already made

- D-001: attack, dash and pause are the only inputs. No new input seen.
- D-002: Option A. D-003: room mix across rooms, zero hearts ends the run (confirmed in C7), +1 heart on clear (not observed this round). D-004: one change set. D-005: `manual.md` not edited.

## Constraints

- I verified at 30 and 60 FPS where noted. I did not edit the build or `manual.md`.
- Suite evidence and own observation are labeled separately in the table.

## Open questions

1. **For the Owner or Studio (ManualTest):** run `python3 -m unittest discover -s tests` in a layout with `manual.md` beside a `repo/` copy. A QA workspace that allows writing the parent of `repo/`, or an Owner-placed `manual.md` in the QA workspace, would do it. Until then ManualTest has no pass/fail. The static check found no difference.
2. **For game-designer (F1):** may a grub stand on the player's tile? If yes, how must the telegraph read there? Today the only signal is the text line while the map shows `P`.
3. **For game-designer (AC-15 wording):** must the practice room be listed in the On screen section (Q4 body text), or is the Script and Rooms-and-runs mention enough (AC-15 wording)?
4. **Not covered, if a further round is allowed:** a full room clear observed by me (heal, projectiles removed, 1.5 s, next room, clearing swipe on a strike tick, "run complete"), and the "(too soon)" and "(down)" lines in the player view. These remain suite-only.

## Expected output

The studio decides on the `manual.md` layout (question 1) and routes F1 and the AC-15 wording to the game-designer. If ManualTest then passes and the studio accepts AC-14 as suite evidence, the verdict can become `pass`. No defect is routed to `gameplay-engineer` unless the designer's ruling on F1 requires a build change.

## Load

- Role: studio/roles/studio.md
- Skills: none
- Project: project.md, design/combat.md, manual.md
- Decisions: decisions/D-003-run-end-and-room-rules.md
- Previous handoff: goals/G-001-combat-monotony/28-studio-to-qa.md
>>>END
