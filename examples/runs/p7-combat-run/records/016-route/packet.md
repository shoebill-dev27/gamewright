# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/18-gameplay-engineer-to-studio.md
next_seq: 19
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha 29993eac7bb0; run through the project's run commands)
log: last 5 of 6 entries in @log-recent; the full history is goals/G-001-combat-monotony/log.md

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/18-gameplay-engineer-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 19
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
4. One question at a time: while an Escalation is open, do not open another. Later questions wait
   for the answer, or go into the next Escalation once it is resolved.

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
player_visible: repo/manual.md
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
(`repo/manual.md`): `run_play` shows what a player sees, `run_trace` the simulation state, and
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
- `repo/manual.md` — controls, the play script format and reaction rules (player-facing; ships
  with the build).
>>>END

<<<FILE @project-files
decisions/D-001-one-button-combat.md
design/combat-cues-visual-spec.md
design/combat.md
goals/G-001-combat-monotony/01-studio-to-playtester.md
goals/G-001-combat-monotony/02-playtester-to-studio.md
goals/G-001-combat-monotony/03-studio-to-game-designer.md
goals/G-001-combat-monotony/04-game-designer-to-studio.md
goals/G-001-combat-monotony/05-studio-to-game-designer.md
goals/G-001-combat-monotony/06-studio-to-qa.md
goals/G-001-combat-monotony/07-game-designer-to-studio.md
goals/G-001-combat-monotony/08-qa-to-studio.md
goals/G-001-combat-monotony/09-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/10-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/11-studio-to-game-designer.md
goals/G-001-combat-monotony/12-studio-to-art-director.md
goals/G-001-combat-monotony/13-studio-to-qa.md
goals/G-001-combat-monotony/14-game-designer-to-studio.md
goals/G-001-combat-monotony/15-art-director-to-studio.md
goals/G-001-combat-monotony/16-qa-to-studio.md
goals/G-001-combat-monotony/17-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/18-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/goal.md
goals/G-001-combat-monotony/log.md
project.md
repo/README.md
repo/bots.py
repo/game.py
repo/manual.md
repo/play.py
repo/tests/test_game.py
>>>END

<<<FILE @decision-titles
decisions/D-001-one-button-combat.md — D-001: Combat uses one attack button plus dash
>>>END

<<<FILE goals/G-001-combat-monotony/goal.md
---
kind: goal
id: G-001
project: lantern-depths
status: active
created: 2026-10-16
---
# G-001: Combat feels monotonous

## Owner request

> 戦闘が単調なので改善したい

## Interpretation

Success condition (qualitative): a player playing the current build's combat experiences it as varied and engaging instead of monotonous. Different situations call for noticeably different play (positioning, timing, use of attack and dash), and the player can tell why. The improvement stays inside the vision pillars: one-button combat (attack + dash only, D-001), short runs, readable threats. Numeric thresholds belong to Design; the final verdict belongs to Review.

Out of scope: new input buttons (needs Owner approval per D-001), changing run length, new biomes or content unrelated to combat variety, and any change to the core concept. Not a defect report: nothing in the request says combat is broken.

## Unknowns

- Observe: done (scripted play, rooms 1–3 + practice room). Rooms 4–5 and hand-timed play are unobserved by a human; the final Play step covers them.
- Observe (FPS divergence, qa): done (16). Deterministic. First walker difference is in room 1 at 0.30 s, a bot threshold at an exact tie (distance 2.5; hypothesis). In room 3 a shot hits at 60 FPS and not at 30 FPS; the log has no positions. No build defect shown, but criterion 16e is unproven. Step 7d adds the missing log data.
- Diagnose: done (04).
- Decide: skipped. No choice of direction or scope; all options stay within D-001 and the pillars. Returns here if the Build needs a new enemy type, a healing system or a new input, or if a ruling changes scope.
- Design: done for now (14). Criteria 13–16 ruled, five spec defaults confirmed, no build or bot change needed. Reopens (tentative 8b) only if the 16e evidence shows a frame-rate-dependent graze at the contact edge (the designer then states whether that is acceptable), or if walker totals in rooms 3–5 leave 3–6.
- Plan: skipped. The approach reuses the enemy update loop. Returns here if the same criterion fails verification twice.
- Build: 0.5 implemented (10). Step 7d: tooling only, richer `log on` output for bots, plus the walker 30/60 test aligned with criterion 16 as ruled. No change to simulation or bot decisions.
- Verify (visual): done (15). Cue forms are accepted. Seven visual points apply to a future graphical build (spec: design/combat-cues-visual-spec.md, V1–V12). Only V12 (timing) can be checked in the text build; V1–V11 stay unverified until a graphical build exists, so they become a proposed new Goal at Close.
- Verify (QA, criteria 1–16 + V12): planned after 7d. Compose its Handoff from 14 (checklist items 1–6; strip the Sender assessment), 15 (V12 only; report, do not rule on, any contradiction between combat.md and the visual spec) and 16 plus the 7d log (16e).
- Play: planned. A fresh playtester judges the result, including rooms 4–5 and hand-timed play.
- Review: planned (`game-director`), experience Goal. Graphical cue acceptance is still open at that point.

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | playtester | playtest-session | done | 01-studio-to-playtester.md (report: 02-playtester-to-studio.md) |
| 2 | Diagnose | game-designer | diagnose-experience | done | 03-studio-to-game-designer.md (result: 04-game-designer-to-studio.md) |
| 3 | Decide | game-director | make-decision | skipped (no real choice; see Unknowns) | — |
| 4a | Design | game-designer | write-design-spec | done | 05-studio-to-game-designer.md (result: 07-game-designer-to-studio.md) |
| 4b | Observe (FPS divergence) | qa | reproduce-defect | done | 06-studio-to-qa.md (result: 08-qa-to-studio.md) |
| 5 | Plan | technical-director | technical-plan | skipped (approach local; see Unknowns) | — |
| 6 | Build | gameplay-engineer | implement-change | done | 09-studio-to-gameplay-engineer.md (result: 10-gameplay-engineer-to-studio.md) |
| 7a | Design (criterion 14, spec gaps) | game-designer | write-design-spec | done | 11-studio-to-game-designer.md (result: 14-game-designer-to-studio.md) |
| 7b | Verify (visual) | art-director | visual-review | done | 12-studio-to-art-director.md (result: 15-art-director-to-studio.md) |
| 7c | Observe (walker 30/60 divergence) | qa | reproduce-defect | done | 13-studio-to-qa.md (result: 16-qa-to-studio.md) |
| 7d | Build (bot log data, walker test) | gameplay-engineer | implement-change | open | 17-studio-to-gameplay-engineer.md |
| 8 | Verify (criteria 1–16, V12) | qa | verify-change | planned (after 7d) | — |
| 8b | Design (frame-rate graze rule) | game-designer | write-design-spec | tentative (only if 16e shows a graze difference) | — |
| 9 | Play | playtester | playtest-session | planned | — |
| 10 | Review | game-director | review-outcome | planned | — |
| 11 | Next | studio | — | planned | — |

## Route changes

After 7a–7c: the designer ruled 14 and 16 with no build or bot change; the art review concerns a future graphical build only; QA found no build defect, but 16e is unproven (the log lacks positions). Added 7d Build (logging only, test aligned with the ruling) before Verify, and tentative 8b Design for a frame-rate graze.

## Next action

Run the gameplay-engineer step with 17-studio-to-gameplay-engineer.md (result addressed to `studio`). Then Route: if the engineer reports no behavior change, open Verify (qa, criteria 1–16 + V12) as described under Unknowns; if the engineer hands back, re-route per the return rules.

## Outcome

(open)
>>>END

<<<FILE @log-recent
## 003-route · 2026-10-16

Status: active. Open: 03-studio-to-game-designer.md.

After step 1 (Observe): the outcome fits the plan, so Diagnose follows. The report is thin (scripted play, rooms 4–5 unseen); the Diagnose Handoff lets the designer check with bots/trace and say if more observation is needed. No stage added or dropped.

## 005-route · 2026-10-16

Status: active. Open: 05-studio-to-game-designer.md, 06-studio-to-qa.md.

After step 2 (Diagnose): fits the plan. Decide is skipped (no real choice, no trigger). Added a parallel QA Observe for the 30/60 FPS bot divergence, since Design's criteria depend on both rates. A separate rooms 4–5 playtest is not added; the final Play covers it.

## 008-route · 2026-10-16

Status: active. Open: 09-studio-to-gameplay-engineer.md.

After steps 4a and 4b: both fit the plan. Plan is skipped (designer: no cross-system approach). QA found no build defect, so the bot fix is added to Build instead of a separate step. The art-director visual review is now planned.

## 010-route · 2026-10-16

Status: active. Open: 11-studio-to-game-designer.md, 12-studio-to-art-director.md, 13-studio-to-qa.md.

After step 6 (Build): partly fits. Criteria 1–12 and 15 look met per the engineer; 14 missed, five spec gaps used defaults, walker 30/60 divergence open. Added 7a Design (designer), 7c QA divergence check, and 7b art-director cue review in parallel. Full QA Verify waits so it runs against final criteria.

## 014-route · 2026-10-16

Status: active. Open: 17-studio-to-gameplay-engineer.md.

After 7a–7c: the designer ruled 14 and 16 with no build or bot change; the art review concerns a future graphical build only; QA found no build defect, but 16e is unproven (the log lacks positions). Added 7d Build (logging only, test aligned with the ruling) before Verify, and tentative 8b Design for a frame-rate graze.
>>>END

<<<FILE goals/G-001-combat-monotony/18-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-001
seq: 18
from: gameplay-engineer
to: studio
stage: Build
outcome: done
---
# 18: gameplay-engineer → studio — Bot log now carries decision-time state; walker 30/60 test replaced by tests of criteria 13/14 per rate and dodger agreement

## Task

Report the tooling and test change from handoff 17, for routing to QA. No simulation or bot decision changed.

## Context

G-001, build 0.5. QA (handoff 16) could not close criterion 16e because `log on` printed action names and times only. The designer ruled (handoff 14) that the walker only has to meet 13 and 14 at each rate and the dodger must agree across rates (16c).

## Findings

### Files changed

- `repo/bots.py`: log only. `Brain` gained log-only fields `grid` and `shadow`, a `skip` method, and `note` now appends ` | <state>`. New helpers `_state` and `_hurt_lines`. `play_room` calls `brain.skip` while the player is stunned, and records state around `game.step()` only when `log` is on. Bot functions, thresholds (2.5, 1.1), `REACTION = 0.15`, the grid logic in `due`, and `game.py` are untouched. Added imports `SHOT_LIFE`, `SHOT_REACH`.
- `repo/tests/test_game.py`: the walker `expectedFailure` test is replaced by `test_walker_meets_criteria_13_and_14_at_each_rate` (the dodger test, unchanged, already covers 16c). Added `test_bot_log_adds_state_and_changes_no_result` and `test_walker_logs_the_exact_distance_it_compared`. Other tests are unchanged.
- `repo/README.md`: describes the new log.
- `game.py`, `play.py`, `design/combat.md`: not changed.

### Log format (`log on`)

- Decision line: `<time> s  <action> | frame N, grid G s, frame time T s, player (x, y), hearts H, stunned no|yes (S s left), nearest <kind> at (x, y) distance D (exact <repr>), shots in flight: (x, y) v (vx, vy); …|none`. The part before ` | ` is identical to the old line. `distance` is the same `math.hypot` expression the bot compares, printed to 9 decimals and as the full float repr.
- Skipped line: `<time> s  skipped decision | frame, grid, frame time, reason: player stunned (S s of stun left)`, once per grid time swallowed by the stun.
- Heart-loss line: `<time> s  HEART LOST | frame N, source grub|shot, player (x, y), grub <kind> at (x, y) | shot at (x, y) v (vx, vy); hearts now H`.

### Run results

- `run_tests`: `python3 -m unittest discover -s tests` → Ran 34 tests, OK. This was with the final `bots.py` and `test_game.py`. A temporary comparison harness (original bots.py kept as a copy plus a comparison test; not delivered) also ran 37 tests OK. That harness is not part of the repo.
- Criterion 4, log off: before and after output were compared byte for byte with the temporary harness, for `bots walker,dodger,camper`, `rooms 1-5`, at 30 and 60 FPS. Both are identical. With `log on`, removing the new ` | …` parts and the new HEART LOST and skipped lines gives exactly the old log (863 lines at 30 FPS, 968 at 60 FPS).

Output before and after (identical), hearts lost per room 1/2/3/4/5:

| Bot, rate | Per room | Totals |
|---|---|---|
| walker 30 | 3✗ 2✓ 0✓ 1✓ 3✗ | cleared 3/5, lost 9, dashes 0 |
| walker 60 | 3✗ 2✓ 2✓ 2✓ 2✓ | cleared 4/5, lost 11, dashes 0 |
| dodger 30 | 0✓ ×5 | cleared 5/5, lost 0, dashes 35 (rooms 3/4/5: 8/7/11) |
| dodger 60 | 0✓ ×5 | cleared 5/5, lost 0, dashes 48 (rooms 3/4/5: 10/8/14) |
| camper 30 | 3✗ 2✓ 3✗ 3✗ 3✗ | cleared 1/5, lost 14, dashes 0 |
| camper 60 | 3✗ 3✗ 3✗ 3✗ 3✗ | cleared 0/5, lost 15, dashes 0 |

Camper recorded output (before = after):

```text
30 FPS
camper  room 1: NOT cleared (5.7 s); hearts lost 3 (hit by: grub 3); attacks 5, dashes 0
camper  room 2: cleared in 10.2 s; hearts lost 2 (hit by: grub 2); attacks 8, dashes 0
camper  room 3: NOT cleared (5.5 s); hearts lost 3 (hit by: shot 3); attacks 0, dashes 0
camper  room 4: NOT cleared (6.7 s); hearts lost 3 (hit by: shot 3); attacks 1, dashes 0
camper  room 5: NOT cleared (6.2 s); hearts lost 3 (hit by: grub 1, shot 2); attacks 0, dashes 0
camper  total: cleared 1/5, hearts lost 14, dashes 0
60 FPS
camper  room 1: NOT cleared (5.7 s); hearts lost 3 (hit by: grub 3); attacks 4, dashes 0
camper  room 2: NOT cleared (8.9 s); hearts lost 3 (hit by: grub 3); attacks 5, dashes 0
camper  room 3: NOT cleared (5.5 s); hearts lost 3 (hit by: shot 3); attacks 0, dashes 0
camper  room 4: NOT cleared (6.8 s); hearts lost 3 (hit by: shot 3); attacks 1, dashes 0
camper  room 5: NOT cleared (6.1 s); hearts lost 3 (hit by: grub 1, shot 2); attacks 0, dashes 0
camper  total: cleared 0/5, hearts lost 15, dashes 0
```

### Sample of the new lines (walker)

Room 1, 0.15–0.50 s:

```text
30 FPS
  0.17 s  walk to grub | frame 5, grid 0.150 s, frame time 0.166667 s, player (8.000000, 3.333333), hearts 3, stunned no, nearest grub at (8.000000, 0.166667) distance 3.166666667 (exact 3.166666666666667), shots in flight: none
  0.30 s  walk to grub | frame 9, grid 0.300 s, frame time 0.300000 s, player (8.000000, 2.800000), hearts 3, stunned no, nearest grub at (8.000000, 0.300000) distance 2.500000000 (exact 2.5000000000000004), shots in flight: none
  0.47 s  face and swing at grub | frame 14, grid 0.450 s, frame time 0.466667 s, player (8.000000, 2.133333), hearts 3, stunned no, nearest grub at (8.000000, 0.400000) distance 1.733333333 (exact 1.7333333333333338), shots in flight: none
60 FPS
  0.15 s  walk to grub | frame 9, grid 0.150 s, frame time 0.150000 s, player (8.000000, 3.400000), hearts 3, stunned no, nearest grub at (8.000000, 0.150000) distance 3.250000000 (exact 3.2499999999999982), shots in flight: none
  0.30 s  face and swing at grub | frame 18, grid 0.300 s, frame time 0.300000 s, player (8.000000, 2.800000), hearts 3, stunned no, nearest grub at (8.000000, 0.300000) distance 2.500000000 (exact 2.4999999999999964), shots in flight: none
  0.45 s  face and swing at grub | frame 27, grid 0.450 s, frame time 0.450000 s, player (8.000000, 2.800000), hearts 3, stunned no, nearest grub at (8.000000, 0.450000) distance 2.350000000 (exact 2.349999999999996), shots in flight: none
```

Room 3, 1.80–2.60 s:

```text
30 FPS
  1.80 s  sidestep shot in flight | frame 54, grid 1.800 s, frame time 1.800000 s, player (2.933333, 1.866667), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 1.273664878 (exact 1.273664878302845), shots in flight: (2.076083, 1.064895) v (2.282502, 1.946840)
  1.97 s  sidestep shot in flight | frame 59, grid 1.950 s, frame time 1.966667 s, player (2.933333, 2.533333), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 1.795054936 (exact 1.7950549357114955), shots in flight: (2.456500, 1.389368) v (2.282502, 1.946840)
  2.10 s  walk to spitter | frame 63, grid 2.100 s, frame time 2.100000 s, player (2.933333, 3.066667), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 2.267646847 (exact 2.267646846892655), shots in flight: (2.760834, 1.648947) v (2.282502, 1.946840)
  2.27 s  sidestep shot in flight | frame 68, grid 2.250 s, frame time 2.266667 s, player (2.933333, 2.400000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 1.682590595 (exact 1.682590595216522), shots in flight: (3.141251, 1.973420) v (2.282502, 1.946840)
  2.40 s  walk to spitter | frame 72, grid 2.400 s, frame time 2.400000 s, player (2.933333, 2.933333), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 2.146832292 (exact 2.1468322917472777), shots in flight: (3.445585, 2.232999) v (2.282502, 1.946840)
  2.57 s  walk to spitter | frame 77, grid 2.550 s, frame time 2.566667 s, player (2.933333, 2.266667), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 1.573389829 (exact 1.5733898294941195), shots in flight: (3.826001, 2.557472) v (2.282502, 1.946840)
60 FPS
  1.80 s  sidestep shot in flight | frame 108, grid 1.800 s, frame time 1.800000 s, player (2.600000, 2.200000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 1.341640786 (exact 1.3416407864998732), shots in flight: (2.030000, 1.040000) v (1.800000, 2.400000)
  1.95 s  sidestep shot in flight | frame 117, grid 1.950 s, frame time 1.950000 s, player (3.200000, 2.200000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 1.697056275 (exact 1.6970562748477185), shots in flight: (2.300000, 1.400000) v (1.800000, 2.400000)
  2.10 s  walk to spitter | frame 126, grid 2.100 s, frame time 2.100000 s, player (3.800000, 2.200000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 2.163330765 (exact 2.1633307652784017), shots in flight: (2.570000, 1.760000) v (1.800000, 2.400000)
  2.25 s  HEART LOST | frame 135, source shot, player (3.200000, 2.200000), shot at (2.840000, 2.120000) v (1.800000, 2.400000); hearts now 2
  2.25 s  skipped decision | frame 135, grid 2.250 s, frame time 2.250000 s, reason: player stunned (0.300 s of stun left)
  2.40 s  skipped decision | frame 144, grid 2.400 s, frame time 2.400000 s, reason: player stunned (0.150 s of stun left)
  2.55 s  skipped decision | frame 153, grid 2.550 s, frame time 2.550000 s, reason: player stunned (0.000 s of stun left)
  2.57 s  walk to spitter | frame 154, grid 2.550 s, frame time 2.566667 s, player (3.200000, 2.200000), hearts 2, stunned no, nearest spitter at (2.000000, 1.000000) distance 1.697056275 (exact 1.6970562748477185), shots in flight: none
```

### Observations for QA (stated without judgment)

- Room 1, 0.30 s: the exact distance the walker compared is 2.5000000000000004 at 30 FPS (not `< 2.5`, so it walks) and 2.4999999999999964 at 60 FPS (`< 2.5`, so it swings). This matches the floating-point tie hypothesis in handoff 16. Both decisions are on grid time 0.300 at frame time 0.300000.
- Room 3: the states at the same grid time already differ before the 2.10–2.25 s hit. At grid 1.800 s the player is at (2.933, 1.867) at 30 FPS and (2.600, 2.200) at 60 FPS. The shot velocities differ too: (2.283, 1.947) at 30 FPS and (1.800, 2.400) at 60 FPS, because the aim direction was locked at the start of the cue from different player positions. The logged data therefore contains no pair of decisions with the same state at the same game time in this window.
- The 60 FPS hit is logged at frame 135 (2.25 s) with the player at (3.200, 2.200) and the shot at (2.840, 2.120): centre distance about 0.369, inside the 0.4 reach. The 30 FPS player's positions in this window are different, so the log does not show a graze at the contact edge for this case. Whether any frame-rate-dependent graze exists is not shown by this data.

## Decisions already made

- D-001: one attack button plus dash; no new input. Unchanged.
- Designer's rulings (handoff 14) applied as written.

## Constraints

- No change to simulation, bot decisions, thresholds, the 0.15 s grid, or player-visible output. Log off is byte-identical to before.

## Open questions

None for the engineer. Whether any frame-rate-dependent contact-edge graze is acceptable is for the game-designer after QA reads the log; the log above did not show a graze case.

## Expected output

QA runs `bots walker`, `rooms 3`, `log on` at `fps 30` and `fps 60`, compares decisions and states by the 16e rule, and reports. Also QA's verification of 1–16 continues as planned in handoff 14.

## Sender assessment

- Behavior preservation: confirmed by the byte comparison of log-off output and by stripping the new log parts (both described above), for all three bots, rooms 1–5, both rates. The added `skip` uses a shadow clock so it never changes `Brain.next`. `_hurt_lines` only reads state; `shots_before` and `struck_before` are copies taken before `step`.
- The heart-loss shot position is found by comparing the shot list before and after the step. A shot that hits in the frame it is fired would be reported as "shot position not found"; no such case appeared in the logs checked.
- The new walker test passes at both rates with the existing numbers (30 FPS: rooms 3–5 lost 4, cleared 2/3; 60 FPS: lost 6, cleared 3/3; rooms 1–2 lost 5 at both rates). The 60 FPS walker sits at the top of the criterion 13 limit (6).
- Confidence: high that nothing behavioral changed; medium on the 16e conclusion, which QA must draw.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md (criteria 13–16), repo/bots.py, repo/game.py, repo/tests/test_game.py, repo/README.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/17-studio-to-gameplay-engineer.md
>>>END
