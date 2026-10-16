# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/24-qa-to-studio.md
next_seq: 25
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha 29993eac7bb0; run through the project's run commands)
log: last 5 of 9 entries in @log-recent; the full history is goals/G-001-combat-monotony/log.md

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/24-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 25
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
decisions/D-002-contact-edge-graze-accepted.md
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
goals/G-001-combat-monotony/19-studio-to-qa.md
goals/G-001-combat-monotony/20-qa-to-studio.md
goals/G-001-combat-monotony/21-studio-to-game-designer.md
goals/G-001-combat-monotony/22-game-designer-to-studio.md
goals/G-001-combat-monotony/23-studio-to-qa.md
goals/G-001-combat-monotony/24-qa-to-studio.md
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
decisions/D-002-contact-edge-graze-accepted.md — D-002: Per-frame contact sampling is kept; the contact-edge graze is an accepted limitation of the text build
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
- Observe (FPS divergence, qa): done (16, 20). Walker 30/60 differences are bot timing, not the build. The contact-edge graze is accepted (D-002).
- Diagnose: done (04).
- Decide: skipped. No choice of direction or scope; all options stay within D-001 and the pillars. Returns here if the Build needs a new enemy type, a healing system or a new input, or if a ruling changes scope.
- Design: done (14, 22). Graze accepted (D-002), shot cap is on cue starts, walker margin kept, governing documents named. Reopens only if QA finds the grub lunge band wider than 0.03 tile at 30 FPS.
- Plan: skipped. The approach reuses the enemy update loop. Returns here if the same criterion fails verification twice.
- Build: 0.5 implemented (10), tooling done (18). No further change needed (8c skipped); returns only if QA finds a failure outside the accepted band.
- Verify (visual): done (15). V1–V11 need a graphical build and become a proposed new Goal at Close; V12 holds in the text build.
- Verify (QA): criteria 1–16 mostly pass (20). Open (23): 30 FPS runs of 5, 6, 8; the defeated-spitter edge case; new criterion 17; the reworded criterion 11.
- Manual wording ("no more than 3 in the air") is true in rooms 1–5 only. Optional fix, raise at Close.
- Play: planned. A fresh playtester judges the result, including rooms 4–5 and hand-timed play. Its Handoff is composed by the Studio from the build and player profile only.
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
| 7d | Build (bot log data, walker test) | gameplay-engineer | implement-change | done | 17-studio-to-gameplay-engineer.md (result: 18-gameplay-engineer-to-studio.md) |
| 8 | Verify (criteria 1–16, V12) | qa | verify-change | done (question: graze) | 19-studio-to-qa.md (result: 20-qa-to-studio.md) |
| 8b | Design (graze, cap, margin, doc conflicts) | game-designer | write-design-spec | done | 21-studio-to-game-designer.md (result: 22-game-designer-to-studio.md) |
| 8c | Build (contact test / cap) | gameplay-engineer | implement-change | skipped (graze and cap accepted as built) | — |
| 8d | Verify (criteria 1–17; close 30 FPS gaps) | qa | verify-change | open | 23-studio-to-qa.md |
| 9 | Play | playtester | playtest-session | planned | — |
| 10 | Review | game-director | review-outcome | planned | — |
| 11 | Next | studio | — | planned | — |

## Route changes

After 8b (Design): fits. The designer accepted the graze (D-002), ruled the cap is on cue starts, kept the walker margin and named the governing documents; the build does not change. 8c is skipped. 8d (QA) is open (handoff 23, no designer assessment) to run the 30 FPS gaps and criterion 17.

## Next action

Run the qa step with 23-studio-to-qa.md (result addressed to `studio`). Then Route: on pass, compose a fresh Handoff for the playtester (9) from the build and player profile only; on a failure outside the accepted band, open Build; on a lunge band wider than 0.03 tile, return to the game-designer.

## Outcome

(open)
>>>END

<<<FILE @log-recent
## 010-route · 2026-10-16

Status: active. Open: 11-studio-to-game-designer.md, 12-studio-to-art-director.md, 13-studio-to-qa.md.

After step 6 (Build): partly fits. Criteria 1–12 and 15 look met per the engineer; 14 missed, five spec gaps used defaults, walker 30/60 divergence open. Added 7a Design (designer), 7c QA divergence check, and 7b art-director cue review in parallel. Full QA Verify waits so it runs against final criteria.

## 014-route · 2026-10-16

Status: active. Open: 17-studio-to-gameplay-engineer.md.

After 7a–7c: the designer ruled 14 and 16 with no build or bot change; the art review concerns a future graphical build only; QA found no build defect, but 16e is unproven (the log lacks positions). Added 7d Build (logging only, test aligned with the ruling) before Verify, and tentative 8b Design for a frame-rate graze.

## 016-route · 2026-10-16

Status: active. Open: 19-studio-to-qa.md.

After 7d: the engineer reports log-only changes with byte-identical log-off output, so the plan holds. Opened Verify (QA, criteria 1–16 + V12, incl. 16e from the new log) with a Handoff that omits the engineer's assessment. 8b stays tentative on the 16e result.

## 018-route · 2026-10-16

Status: active. Open: 21-studio-to-game-designer.md.

After 8 (Verify): partly fits. 1–15 and 16a–d pass; the walker difference is bot timing. QA found a frame-rate-dependent graze plus a cap and margin question, which only the designer can rule. 8b is now open (handoff 21). Added 8c Build (tentative) and 8d Verify (planned).

## 021-route · 2026-10-16

Status: active. Open: 23-studio-to-qa.md.

After 8b (Design): fits. The designer accepted the graze (D-002), ruled the cap is on cue starts, kept the walker margin and named the governing documents; the build does not change. 8c is skipped. 8d (QA) is open (handoff 23, no designer assessment) to run the 30 FPS gaps and criterion 17.
>>>END

<<<FILE goals/G-001-combat-monotony/24-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 24
from: qa
to: studio
stage: Verify
outcome: pass
---
# 24: qa → studio — Build 0.5 verified against criteria 1–17: pass; V12 stays open; two small notes for the designer (shot tie at exactly 0.40, lunge band)

## Task

Report the close-out verification of build 0.5 against `design/combat.md` criteria 1–17 (plus V12 for the text build), and give the verdict. The next step is a playtest, composed without implementation history.

## Context

G-001 (combat monotony). The build is unchanged since handoff 20. Handoff 23 asked for these checks: 5, 6 and 8 at 30 FPS, the "no renumber" edge case, criterion 17 with known misses, criterion 11 in its new wording, and the unit tests. All evidence below comes from runs made in this step (tests, bots, play/trace scripts). Anything not re-run is marked as carried over. The build and the spec were not changed.

## Findings

### A. Per-criterion result

| # | Result | Evidence |
|---|---|---|
| 1 Telegraph | pass, 30 and 60 | Not re-traced this step. The suite checks the gap ≥ 0.5 s − 1 frame at both rates (34 tests OK). Handoff 20 trace `c1-stand` showed the lunge exactly 0.5 s after the cue. |
| 2 Sidestep | pass, 30 and 60 | Suite (both rates). `c5-30` this step: the player steps up 1.07 tiles during the wind-up and takes no damage from the lunge. |
| 3 Dash | pass, 30 and 60 | Suite (offsets 0, 0.25, 0.5 and 0.6 s, both rates). |
| 4 Standing still | pass, 30 and 60 | Suite (both rates). |
| 5 Safe window | **pass at 30 (new)** and 60 | Trace `c5-30`: the lunge ends at 0.833 s at (7.60, 4.00). The player walks back to (8.00, 3.73), 0.48 tile from the grub and inside the 0.6 reach, during the recovery from about 1.1 s. Hearts stay 3 until the end at 1.5 s, and a swipe at 1.3 s hits the grub (hp 1). The player was never hurt before this, so hurt-invulnerability cannot explain the result. |
| 6 Cancel | **pass at 30 (new)** and 60 | `c6-two-swipes-30`: the grub (hp 2) is hit to hp 1, then defeated by the second swipe at 0.433 s, and the room clears. `c6-cancel-30`: the swipe in wind-up at 0.133 s gives stagger and no lunge by 0.9 s. The stagger lasts exactly 0.4 s, and the wind-up then restarts at 0.533 s. A kill in wind-up with no stagger and no lunge: runner, handoff 20 `c6-kill-windup` at 30 and 60, carried over, plus `c8-runner-30` this step (defeated, cleared, no stagger event). |
| 7 One at a time | pass, 30 and 60 | Suite (maximum 1 grub in wind-up or lunge, both rates). |
| 8 Variants | **pass at 30 (new)** and 60 | `c8-runner-30`: 1 swipe. `c8-brute-30`: 4 swipes (hp 4→3→2→1→defeated at 1.233 s). Standard grub: 2 swipes (see 6). Marks `r` and `G` are in the suite and listed in `manual.md`. |
| 9 Aim cue | pass, 30 and 60 | `room3-30` and `room3-60`: aim at 1.200 s, spit at 1.800 s (0.600 s at both rates). The shots go along the locked line (hit traces in 17). |
| 10 Dodge | pass, 30 and 60 | Suite. `b-miss` traces: the 1-tile-class sidestep gives no hit at either rate. |
| 11 Stagger and cap | **pass, 30 and 60** | See section B. |
| 12 Rooms | pass | Suite compares rooms 2, 4 and the brute in room 5. Handoff 20 read all five rooms against the table; `game.py` is unchanged. |
| 13 | pass at each rate | See section C. |
| 14 | pass at each rate | See section C. |
| 15 Dash used | pass at each rate | Dodger dashes in rooms 3/4/5: 8/7/11 at 30 FPS and 10/8/14 at 60 FPS. |
| 16a | pass | The gaps from handoff 20 (5, 6, 8 at 30 FPS) are closed. 17 is covered below. |
| 16b | pass | Section C. |
| 16c | pass | The dodger is identical at both rates: 0 hearts lost in every room, 5/5 cleared. |
| 16d | acknowledged | Walker per room, 30 FPS: 3✗ 2✓ 0✓ 1✓ 3✗. At 60 FPS: 3✗ 2✓ 2✓ 2✓ 2✓. The same figures as in handoff 20. |
| 16e | pass | No new finding. The walker differences are bot timing (handoff 20, section D). The contact-edge differences found in 17 are inside the accepted band. |
| 17 Contact edge | **pass**, with two notes (section D) | Shot misses of about 0.39 hit at both rates and about 0.41 miss at both. Lunge misses of 0.570 hit at both rates and 0.610 miss at both. Differences between rates appear only at lateral misses of 0.40 (shot) and 0.59 (lunge). |
| Edge: no renumber | **pass, 30 and 60** | Section E. |
| V12 | open | There is no graphical build. The text-build timings hold at both rates (wind-up to lunge exactly 0.5 s, aim to spit 0.6 s). V12 stays open until a graphical build exists. |

### B. Criterion 11 in its new wording

- **Room 3, first shots.** `room3-30` and `room3-60` both spit at 1.800, 2.600 and 3.400 s. The cues start 0.6 s earlier, at 1.2, 2.0 and 2.8 s.
- **Room 3, cap.** The suite counts the shots in flight over 12 s at both rates. The maximum is at most 3, and the suite passed.
- **Four-spitter practice room** (`four-30` and `four-60`): spitters at (0,0), (0,3), (0,5), (0,8), player at (15,4). The results at 30 and 60 are the same, down to the printed messages and times.
  - The first three spitters cue at 1.2, 2.0 and 2.8 s with fewer than 3 shots in flight. They spit at 1.8, 2.6 and 3.4 s.
  - The fourth spitter's cue (due at 3.6 s) and the repeat cues of the others are blocked. At those checks the three earlier shots are in flight.
  - The 1.8 s shot leaves at its 5 s life limit. Only then, at 6.8 s, do all four cues start together, with 2 shots in flight at each check.
  - All four spit at 7.4 s. By my count that is the 2 older shots plus 4 new ones, so at most 6 in flight. That equals 2 + 4 living spitters, which is the limit. I derived this from the traces, the 2 older shots are still visible at 6.5 s and 7.0 s, and I did not count it directly.
  - The player view shows "YOU ARE HIT" at 7.467 s and 8.267 s at both rates, so the shots really are in flight.
  - Result: a cue starts only when fewer than 3 shots are in flight, the maximum stays within 2 + living spitters, and the cap delay carries forward. All of this matches the spec.
- **Manual wording.** `manual.md` says "no more than 3 are in the air at once". This is true in rooms 1–5, which are the only rooms a player meets. The count can be higher only in a practice room with four or more spitters, which is a script feature. I do not consider the sentence misleading for a player. If the Studio wants it exact, "in the five rooms" would remove the gap. I did not edit the manual.

### C. Bots and regression (bots run at 30 and 60 FPS, `log` off)

| | 30 FPS | 60 FPS |
|---|---|---|
| Walker lost, rooms 3–5 (need 3–6) | 0+1+3 = 4 | 2+2+2 = 6 (top of range) |
| Walker cleared, rooms 3–5 (need ≥ 2) | 2 | 3 |
| Dodger lost / cleared, rooms 3–5 (need ≤ half the walker's loss; 3/3) | 0 / 3 | 0 / 3 |
| Camper cleared, rooms 3–5 (must be < walker) | 0 | 0 |
| Walker lost, rooms 1–2 (need ≥ 1) | 3+2 = 5 | 3+2 = 5 |
| Dodger lost / cleared, rooms 1–2 (need ≤ 1; both cleared) | 0 / 2 | 0 / 2 |

- These figures are identical to handoff 20. The walker at 60 FPS stays at exactly the limit of 6. Per the step 22 ruling, a result of 7 would be a tuning question and not a defect.
- Camper room 2: cleared at 30 FPS (2 hearts lost), not cleared at 60 FPS (3 lost). No criterion covers the camper in rooms 1–2. I note it only as an observation.
- `python3 -m unittest discover -s tests`: 34 tests, OK.
- Nothing else regressed. All figures equal the earlier handoffs.

### D. Criterion 17: contact edge

Reproduction: `room empty`, one spitter or grub, the player locked on at (8, 4.0) and then moved to a final position, as in handoff 20. The lateral miss is the perpendicular distance of the player's final position from the locked line. I calculated it from the positions printed in the traces.

**Shots (reach 0.4)**

| Spitter at | Final player y | Lateral miss | 30 FPS | 60 FPS |
|---|---|---|---|---|
| (1.0, 2.4) | 3.60 | 0.390 (0.3899) | hit at 4.133 s | hit at 4.133 s |
| (5.0, 6.5) | 3.47 | 0.407 | no hit | no hit |
| (1.04, 3.70) | 3.60 | 0.3996 (band) | no hit | hit at 4.100 s |
| (1.0, 4.0) | 3.60 | nominal 0.400 | hit at 4.100 s | no hit |

- 17a passes (0.390 is a hit at both rates). 17b passes (0.407 is a miss at both rates).
- The difference at 0.3996 is inside the accepted band. Only hit or miss differs. The aim and spit times are identical (1.2 s and 1.8 s).
- **Note 1, shot at exactly 0.40 (for the designer).** The row with a nominal 0.400 miss hit at 30 FPS and not at 60 FPS.
  - At 30 FPS a frame lands exactly on the closest approach (x = 8.0), and the code treats `distance <= 0.4` as a hit. The actual miss is 0.4 within float noise, and I cannot read the float value from the trace.
  - 17b says "0.40 or more: no hit at both rates". The band definition says "from reach − 0.01 to reach (0.39 to 0.40)", which includes 0.40.
  - I did not count this row as a 17b failure, because the spec is ambiguous at exactly the reach and the clean case at 0.407 passes. I treat it as a spec question: is a miss of exactly the reach inside the band (differences accepted) or a guaranteed miss? If it is a guaranteed miss, `<=` would need to become `<`, which is a Build change.

**Lunges (reach 0.6), grub standing near, player at (8.0, 3.2) at lunge time**

| Lateral miss | 30 FPS | 60 FPS |
|---|---|---|
| 0.570 | hit at 0.667 s | hit at 0.650 s |
| 0.580 | hit at 0.667 s | hit at 0.650 s |
| 0.590 | **no hit** | hit at 0.667 s |
| 0.599 | hit at 0.667 s | hit at 0.650 s |
| 0.610 | no hit | no hit |

- 17c passes: 0.570 hits at both rates, and 0.610 misses at both rates.
- In the hit cases the lunge starts at 0.533 s (30) and 0.517 s (60). The hit comes 0.133 s later at both rates, so timing, cue and message are the same. Only the hit itself differs, at 0.590.
- **Note 2, lunge band width (for the designer).** My calculation is that a lunge hit is guaranteed up to a lateral miss of 0.585 at 30 FPS, which makes the band about 0.015 tile and not more than 0.03. That is the derivation: a frame step of 0.267 tile needs the sampled point within 0.133 tile along the line. At 60 FPS the same calculation gives about 0.004 tile.
  - Measured with five probes only: the 30 FPS disagreement appeared only at 0.590, and no probe at 0.570 or below missed. The 0.599 probe hit again at 30 FPS because the frame phase differs between positions. I did not scan the whole range.
  - There is no evidence that the band is wider than 0.03 tile, so I do not report this as a spec failure. The designer may want to record "about 0.015 at 30 FPS, 0.004 at 60 FPS" in D-002 as measured, with the scan limitation stated.

### E. Edge case: a defeated spitter does not renumber the others

Script `renum-30` and `renum-60`: three spitters in spawn order, with the first one (1,1) killed by two swipes before 0.5 s.

- The next two spitters keep their own timers: aim at 2.000 s and spit at 2.600 s for the second spitter (k = 1), then aim at 2.800 s and spit at 3.400 s for the third (k = 2).
- Renumbering would have moved the shots to 1.8 s and 2.6 s. That did not happen.
- The second spitter fires again with its cue at 4.400 s, as it should (2.6 + 2.4 = 5.0 s).
- The results are identical at 30 and 60 FPS.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- D-002: per-frame contact sampling is kept; the graze is an accepted limitation. Notes 1 and 2 above concern the revisit condition in D-002 and the band numbers.

## Constraints

- The build and the spec were not changed.
- Verified from the spec, the criteria and the build, at 30 and 60 FPS.
- V12 is not assessable in the text build.

## Open questions

For `game-designer`, via the Studio. These are not blocking, and the verdict does not depend on them:

1. A shot whose lateral miss is exactly the reach (0.40): inside the band (either result accepted) or a guaranteed miss? See Note 1.
2. Please record the measured lunge band for D-002 (about 0.015 tile at 30 FPS, derived and probed at five points; not a full scan). See Note 2.

## Expected output

- Verdict: **pass**. Criteria 1–17 hold at 30 and 60 FPS with the figures above, and V12 is open until a graphical build exists. There is no failing criterion.
- The Studio can route to the playtest. The Playtester gets no implementation history, and the walker margin and the notes above are not needed by the Playtester.
- Notes 1 and 2 go to `game-designer` when convenient.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md, repo/manual.md, repo/game.py, repo/bots.py, repo/play.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-contact-edge-graze-accepted.md
- Previous handoff: goals/G-001-combat-monotony/23-studio-to-qa.md
>>>END
