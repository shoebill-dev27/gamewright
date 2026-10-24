# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/20-qa-to-studio.md
next_seq: 21
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha 29993eac7bb0; run through the project's run commands)
log: last 5 of 7 entries in @log-recent; the full history is goals/G-001-combat-monotony/log.md

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/20-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 21
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
goals/G-001-combat-monotony/19-studio-to-qa.md
goals/G-001-combat-monotony/20-qa-to-studio.md
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
- Observe (FPS divergence, qa): done (16). Deterministic. First walker difference is in room 1 at 0.30 s, a bot threshold at an exact tie (distance 2.5; hypothesis). In room 3 a shot hits at 60 FPS and not at 30 FPS. Criterion 16e was unproven for lack of log data; the 7d log now supplies it, and QA settles it in Verify.
- Diagnose: done (04).
- Decide: skipped. No choice of direction or scope; all options stay within D-001 and the pillars. Returns here if the Build needs a new enemy type, a healing system or a new input, or if a ruling changes scope.
- Design: done for now (14). Criteria 13–16 ruled, five spec defaults confirmed. Reopens (tentative 8b) only if the 16e evidence shows a frame-rate-dependent graze at the contact edge (the designer then states whether that is acceptable), or if walker totals in rooms 3–5 leave 3–6.
- Plan: skipped. The approach reuses the enemy update loop. Returns here if the same criterion fails verification twice.
- Build: 0.5 implemented (10). 7d done (18): tooling only (richer `log on` output, walker test aligned with criterion 16). The engineer reports no change to simulation or bot decisions; QA verifies that independently.
- Verify (visual): done (15). Cue forms are accepted. Seven visual points apply to a future graphical build (spec: design/combat-cues-visual-spec.md, V1–V12). Only V12 (timing) can be checked in the text build; V1–V11 stay unverified until a graphical build exists, so they become a proposed new Goal at Close.
- Verify (QA, criteria 1–16 + V12): open (19). Handoff composed without the engineer's assessment.
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
| 8 | Verify (criteria 1–16, V12) | qa | verify-change | open | 19-studio-to-qa.md |
| 8b | Design (frame-rate graze rule) | game-designer | write-design-spec | tentative (only if 16e shows a graze difference) | — |
| 9 | Play | playtester | playtest-session | planned | — |
| 10 | Review | game-director | review-outcome | planned | — |
| 11 | Next | studio | — | planned | — |

## Route changes

After 7d: the engineer reports log-only changes with byte-identical log-off output, so the plan holds. Opened Verify (QA, criteria 1–16 + V12, incl. 16e from the new log) with a Handoff that omits the engineer's assessment. 8b stays tentative on the 16e result.

## Next action

Run the qa step with 19-studio-to-qa.md (result addressed to `studio`). Then Route: if it passes, compose the Play Handoff for a fresh playtester from the build and player profile only; if 16e shows a frame-rate graze, open 8b (game-designer); if a criterion fails, return to Build with the failure report (a second failure of the same criterion goes to technical-director).

## Outcome

(open)
>>>END

<<<FILE @log-recent
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

## 016-route · 2026-10-16

Status: active. Open: 19-studio-to-qa.md.

After 7d: the engineer reports log-only changes with byte-identical log-off output, so the plan holds. Opened Verify (QA, criteria 1–16 + V12, incl. 16e from the new log) with a Handoff that omits the engineer's assessment. 8b stays tentative on the 16e result.
>>>END

<<<FILE goals/G-001-combat-monotony/20-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 20
from: qa
to: studio
stage: Verify
outcome: question
---
# 20: qa → studio — Build 0.5 (sha 29993eac7bb0) verified against 1–16 and V12; one open item for the designer: a frame-rate-dependent graze at the contact edge

## Task

Report the independent verification of build 0.5 against combat criteria 1–16 and V12, and settle 16e from the new `log on` output.

## Context

All evidence is from runs made in this step (tests, bots with and without `log`, play/trace scripts). No run rounds are left. Anything not run is marked "not run". The verdict is not `pass` yet. Criteria 1–15 and 16a–d pass. For 16e, the walker's differences are explained by bot timing. But a frame-rate-dependent graze at the contact edge exists in the build, shown by a scripted reproduction. The spec does not say whether that is acceptable, so it goes to `game-designer` through the Studio. No criterion has failed for a second time.

## Findings

### A. Per-criterion result

| # | Result | Evidence |
|---|---|---|
| 1 Telegraph | pass, 30 and 60 | Trace `c1-stand`: windup at frame 1 (0.033 s at 30, 0.017 s at 60). The lunge starts exactly 0.5 s later (0.533 / 0.517). The first hit lands at 0.667 / 0.633, so cue to hit is 0.633 s / 0.617 s, which is ≥ 0.5 s. The test suite checks the gap at both rates. |
| 2 Sidestep | pass, 30 and 60 | Trace `c2-side`: the player moves up from 0.1 s to 0.35 s (1.07 tiles at 30, 1.0 at 60). Hearts stay 3 through the first lunge. Later damage in that trace comes from a second lunge the script does not dodge. |
| 3 Dash | pass, 30 and 60 | Trace `c3-dash-late` (dash at 0.65 s, inside the window): 3 hearts at both rates, `dash` and `dash_end` logged, no `ignored`. The tests dash at offsets 0, 0.25, 0.5 and 0.6 s after the cue at both rates. |
| 4 Standing still | pass, 30 and 60 | `c1-stand` loses 2 hearts in 3 s at both rates. The test suite checks it at both rates. |
| 5 Safe window | pass at 60 (test). 30 FPS not run. | `test_recovery_is_safe` and `test_grub_walking_alone_does_not_hurt` run at 60 only. In `game.py`, grub damage happens only in the lunge phase, so I expect the same result at 30, but I did not observe it. Hurt-invulnerability (0.8 s) equals recovery (0.8 s), so trace `c1-stand` cannot isolate it. |
| 6 Cancel | pass | Trace `c6-kill-windup` at 30 and 60: the runner is defeated in wind-up, the room clears, with no stagger event and no lunge. Swipe during wind-up gives stagger and no lunge (tests, both rates). The two-swipe kill is a 60 FPS test only. |
| 7 One at a time | pass, 30 and 60 | Test: the maximum number of grubs in wind-up or lunge is 1 at both rates. |
| 8 Variants | pass | Swipes to defeat 2 / 1 / 4 (60 FPS test; not run at 30). Marks `r` and `G` are drawn (test) and listed in `manual.md`. |
| 9 Aim cue | pass, 30 and 60 | Room 3 test: aim to spit is 0.6 s ±1 frame. The shot follows the locked line (y stays 4.0 in the spitter test). |
| 10 Dodge | pass, 30 and 60 | Spitter sidestep test. |
| 11 Stagger | pass, 30 and 60 | Room 3 test: first shots at 1.8 / 2.6 / 3.4 s ±1 frame, and at most 3 shots in flight over 12 s. See finding C for a 4-spitter observation. |
| 12 Rooms | pass | `ROOMS` in `game.py` matches the table for all 5 rooms (I read it). The test checks rooms 2, 4 and the brute in room 5. |
| 13 | pass at each rate | See table B. |
| 14 | pass at each rate | See table B. |
| 15 Dash used | pass at each rate | Dodger dashes in rooms 3/4/5: 8/7/11 at 30 FPS, 10/8/14 at 60 FPS. |
| 16a | pass, with the gaps listed for 5, 6 and 8 | |
| 16b | pass | See table B. |
| 16c | pass | The dodger is identical at both rates: 0 hearts lost in every room and 5/5 cleared. |
| 16d | acknowledged | The walker differs between rates (per room, 30 FPS: 3✗ 2✓ 0✓ 1✓ 3✗; 60 FPS: 3✗ 2✓ 2✓ 2✓ 2✓). |
| 16e | walker differences: bot timing. Graze: open (see D and E). | |
| V12 | not assessable | There is no graphical build. The text-view reference timings hold at both rates: wind-up to lunge is exactly 0.5 s, and aim to spit is 0.6 s ±1 frame. The cue appears on frame 1 at both rates. |

### B. Criteria 13/14/15 numbers

The bots ran with `log off`, from `bots.py`, at each rate separately.

| | 30 FPS | 60 FPS |
|---|---|---|
| Walker lost, rooms 3–5 (need 3–6) | 0+1+3 = 4 | 2+2+2 = 6 (top of range) |
| Walker cleared, rooms 3–5 (need ≥ 2) | 2 | 3 |
| Dodger lost / cleared, rooms 3–5 (need ≤ half the walker's loss; 3/3) | 0 / 3 | 0 / 3 |
| Camper cleared, rooms 3–5 (must be < walker) | 0 | 0 |
| Walker lost, rooms 1–2 (need ≥ 1) | 3+2 = 5 | 3+2 = 5 |
| Dodger lost / cleared, rooms 1–2 (need ≤ 1; both cleared) | 0 / 2 | 0 / 2 |

The walker at 60 FPS sits at exactly 6, the limit of the range. A change of one heart would break 13. This is a tuning note for the designer, not a failure.

### C. Other observations

Neither of these fails a criterion as written.

1. **Shot cap exceeded with four spitters (practice room).** Trace `cap-four-spitters-60` has four spitters. Cues start for three spitters at 4.6 s, and each cap check sees only 2 shots in flight. At 5.2 s all three fire, while the shots from 2.6 s and 3.4 s are still in flight. By my count that is 5 shots in flight; the trace shows the hits at 5.3 s and 6.1 s. The spec text checks the cap only when a cue starts, so this may be intended. Criterion 11 says "never more than 3 in flight", and the 3-spitter room 3 stayed ≤ 3 in the test. No real room has 4 spitters. Question for the designer: is the cap a limit on cue starts or on shots in flight?
2. **Hit-stun can last one frame longer than 0.3 s.** Several `skipped decision` lines show "0.000 s of stun left" while the bot was still skipped. Examples: 60 FPS camper room 1 at frame 180; 30 FPS camper room 3 at frame 126. I infer that a tiny floating-point residue keeps `stun_left` above 0 for one extra frame. It is within ±1 frame. It shifts one bot decision, and it is a plain float effect, not tied to one frame rate.
3. **Criterion 6 and 8:** the two-swipe and variant-swipe tests run at 60 FPS only.
4. **Not run:** the "spitter index not renumbered after a defeat" edge case. No test or trace covers it.
5. **Edge cases that were run:** grub at distance 0 (trace `edge-dist0`) aims right (+1,0) and shows the cue and line. The cap delay carries forward (trace `cap-four-spitters-60`: shots at 5.2 s instead of 4.2 s, then +2.4 s).
6. **Manual check:** `manual.md` lists the marks `r` and `G`, the `~` line, both messages, warnings of 0.5 / 0.35 / 0.7 s and the 0.4 s stagger. It matches the spec.

### D. 16e — walker, room 3, 30 vs 60 FPS (`log on`)

**Room 1 at 0.30 s (the first walker difference): fully explained by the log.**
- The walker swings when `distance < 2.5`. At 0.30 s the player is at (8.0, 2.8) and the grub at (8.0, 0.3) at both rates, so the true distance is exactly 2.5.
- The logged exact values are 2.5000000000000004 at 30 FPS and 2.4999999999999964 at 60 FPS.
- So 30 FPS evaluates "not < 2.5" and walks (it swings first at 0.47 s). 60 FPS evaluates "< 2.5" and swings at 0.30 s.
- The cause is floating-point residue at an exact threshold tie in the bot. The game and the real geometry are the same. This confirms the hypothesis in handoff 16.

**Room 3: positions diverge long before any damage.**
- Decisions up to 1.05 s are the same action ("walk to spitter"). The decision grid is the same at both rates. The 30 FPS decisions land 0–1 frame later (for example 0.17 vs 0.15 s), so the player keeps its old heading up to 0.033 s longer.
- Already at 1.20 s the player is at (4.267, 2.933) at 30 FPS and (3.8, 3.4) at 60 FPS.
- The aim cue is locked on the player's position at its start, so the first shots differ in direction. From the logs: v = (2.28, 1.95) at 30 FPS and v = (1.8, 2.4) at 60 FPS. At 1.80 s the players are 0.47 tile apart.
- At 60 FPS the walker, at (3.8, 2.2) at 2.10 s, walks left into the shot. The hit at 2.25 s is at distance ≈ 0.37 (player (3.2, 2.2), shot (2.84, 2.12)), and ≈ 0.47 one frame earlier. That is a clear hit, not a graze.
- At 30 FPS the walker, at (2.933, 3.067) at 2.10 s, is somewhere else, so there is no contact.

**Conclusion:** I found no pair of decisions at the same game time (±1 frame) from the same positions that gave different outcomes. The walker difference comes from bot decision timing, plus the different positions that follow from it. The walker's room 3 difference is not a build defect. The logs are cut at 20000 characters (up to about 9.3 s at 30 FPS). They cover the first divergence and the whole of room 3 at 60 FPS, but not every later decision.

### E. Frame-rate-dependent graze at the contact edge (exists)

**Reproduction.** Shot reach is 0.4. Scripts, run at `fps 30` and `fps 60`, with `python3 play.py --view trace`:

```text
room empty
fps 30            # and 60
spawn spitter 1.04 3.70
1.3 move up
1.4 stop
end 5
```

| Spitter position | 30 FPS | 60 FPS |
|---|---|---|
| (1.04, 3.70) | **no hit**, 3 hearts at 5 s | **hit at 4.100 s**, 2 hearts |
| (1.00, 3.70) | hit at 4.100 s | hit at 4.117 s |
| (1.00, 3.73) | hit at 4.100 s | hit at 4.117 s |
| (1.00, 3.76) | hit at 4.100 s | hit at 4.117 s |

**What happens.** The first shot (spit at 1.8 s) is locked on the player at (8, 4.0), as of the cue start at 1.2 s. The player then stands at (8, 3.6). The shot line passes at a perpendicular distance of about 0.3996 from the player, which is 0.0004 inside the reach of 0.4. Contact is a distance check once per frame (a shot moves 0.1 tile per frame at 30 FPS and 0.05 at 60 FPS). The hit needs a sampled frame within about ±0.017 tile of the closest approach. That window is narrower than the frame step at both rates, so which rate catches it depends on the phase.

**Reading the 16e rule.** The scripted input, the player position and the shot line are identical at both rates, and the outcome differs. This is not a walker-timing effect. 16e defines a build defect as "same decision, same time, same positions, different outcome". Read literally, this matches. But the Timing rule in the spec only guarantees "no tunnelling", and the spec does not say what collision sampling is allowed to do at the reach edge. I do not decide whether it is acceptable.

**Size (derived by my arithmetic, not run).**
- The effect only exists when the lateral miss is within about 0.003 tile of the 0.4 reach. Misses of 0.4 or more never hit, and misses more than about 0.003 inside always hit at both rates.
- Grub lunges use reach 0.6 and a step up to 0.27 tile at 30 FPS. The same logic gives a wider band, about 0.015 tile at 30 FPS. I did not test grubs for this.
- Severity: low. Frequency: only when a player's lateral miss falls in that very narrow band. The effect is a hit or a miss and does not change timing.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- Designer's rulings on 13–16 and the five spec defaults (handoff 14). They were applied as written.

## Constraints

- This verification used only the spec, the criteria and the build.
- The game was not edited.
- Supported frame rates are 30 and 60 FPS.

## Open questions

For `game-designer`, through the Studio:

1. Is the frame-rate-dependent graze (finding E) acceptable for the text build? If yes, 16e passes as ruled and the verdict becomes `pass`. If not, `gameplay-engineer` must change the contact test (for example a swept test between frames) and QA re-verifies. This would be the first failure of 16, so no `technical-director` re-plan is triggered.
2. Is the shot cap a limit on starting cues (as built) or a hard limit on shots in flight (finding C1)?
3. The walker at 60 FPS in rooms 3–5 totals exactly 6 hearts, the upper limit of criterion 13. Does the designer want to keep that margin?
4. Contradictions between `design/combat.md` and `design/combat-cues-visual-spec.md` (reported only, no ruling):
   - **Lunge line.** `combat.md` says a "thin" orange-red line for the lunge path. The visual spec draws a lane 1.2 tiles wide.
   - **Spitter glow.** `combat.md` and the text view show the glow starting at 0%. The visual spec requires a floor of at least 30%.
   - **Grub cue behaviour.** `combat.md` says the grub "flashes" for the whole wind-up. The visual spec says a steady tint with a slight pulse, no strobe, at 3 Hz or less. The lane in the visual spec stays at full strength until the lunge starts and fades during it. The text view removes the line when the lunge starts.
   - **Text marks.** `combat.md` leaves the `r` / `G` marks open for the graphical build. The visual spec uses silhouette and size instead, which answers the open question.

## Expected output

The Studio routes finding E and open questions 1–3 to `game-designer`. After the ruling:
- If E is accepted, QA's verdict is `pass`, and the gaps on criteria 5, 6, 8 at 30 FPS can be closed with one more test run.
- If E is not accepted, the Studio routes to `gameplay-engineer` with the reproduction above.

V12 stays open until a graphical build exists.

## Regression check

- **Existing tests:** `python3 -m unittest discover -s tests` ran 34 tests, all OK. This includes the replaced walker test (13 and 14 at each rate), the dodger agreement test and the two new log tests.
- **Log on vs off:** the visible results are identical for the camper in all rooms at both rates, and for the walker in rooms 1, 2 and 3 (room 3 from the separate runs) at both rates. The `all30-log` and `all60-log` outputs were cut at 20000 characters (walker rooms 3–5 and the dodger are not in the visible part). The unit test `test_bot_log_adds_state_and_changes_no_result` covers every bot, rooms 1 and 3 and both rates, and passes.
- **Bots unchanged:** the `log off` numbers equal the table in handoff 16 and the walker/dodger figures in handoff 14 (walker 4 lost / 2 cleared at 30 FPS and 6 lost / 3 cleared at 60 FPS in rooms 3–5, dodger 0 lost).
- **Log format:** every decision line has frame, grid time, frame time, player position, hearts, stun, nearest enemy with the exact distance, and shots in flight. Heart-loss lines and skipped-decision lines appear as described in `README.md`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md, design/combat-cues-visual-spec.md, repo/manual.md, repo/README.md, repo/bots.py, repo/tests/test_game.py, repo/game.py, repo/play.py
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/19-studio-to-qa.md
>>>END
