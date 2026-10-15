# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/58-qa-to-studio.md, goals/G-001-combat-monotony/59-game-designer-to-studio.md
next_seq: 60
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha 097ad2a377c5; run through the project's run commands)
log: last 5 of 23 entries in @log-recent; the full history is goals/G-001-combat-monotony/log.md

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/58-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/59-game-designer-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 60
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

- Observe (playtester, qa): done (02, 08, 06, 15). Open again for qa (55): short bite warning seen at about 11.9 s (54), real dash distance, swipe during Strike or adjacent Recovery, dash and facing, "on you" swipe, knockback distance, bots script format and bot data.
- Diagnose, Decide: first pass done (03; D-002, D-005, D-006). Second Diagnose pass done (53): room 1 and room 2 are harsh (grubs arrive together, 0.3 s stun blocks the counter, interrupt and knockback not taught, facing and dash edge cases unspecified). Remedies A1 wind-up spacing, A2 shorter stun, A3 body-hit rule, A5 spec gaps are the designer's. D1 (facing) and D2 (room 1 composition) are held for a retest, not routed to the director now. Causes came from scripted play and reasoning only; no bot or trace data.
- Design: done for the spec (10, 16, 33, 45; `design/combat.md`, D-003, D-006, `design/combat-visuals.md`, D-009). Open again: A1/A2/A3/A5 spec update and manual draft (56); "on you" and "which grub hit you" display (57).
- Plan: done (14, D-004). Tentative: a new Plan only if A1 is not local to existing systems.
- Build: done for the previous change set; a new Build follows Design (and QA results if they show defects). Manual changes are placed by the Owner (D-005, D-007 pattern).
- Verify: done for the previous build (AC-1…AC-18 hold, D-010). The next build needs its own Verify (qa, plus art-director if visuals change).
- Play: two sessions saw only rooms 1 and 2 by script (50, 54), with defeats. Rooms 3–5, the spitter, projectile hits, room clear, the dash and a survived run are still unobserved, so monotony itself is still unjudged. Next Play follows the rebuild, with a fresh playtester, told to cover rooms 3–5 and to react.
- Review: `game-director` with `review-outcome`. Planned, after the rebuild and the next Play. Open: run progression after "run over"; F1, F4, F6, F7; numbering of same-type enemies in one cell; D1, D2.
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
| 10a | Observe (open facts, bots) | qa | reproduce-defect | open | 55-studio-to-qa.md |
| 10b | Design (A1–A3, A5, manual draft) | game-designer | write-design-spec, make-decision | open | 56-studio-to-game-designer.md |
| 10c | Design (visuals: "on you", hit source) | art-director | visual-review, write-design-spec | open | 57-studio-to-art-director.md |
| 10-O | Owner: place manual changes | owner | — | tentative (if the draft changes manual.md) | — |
| 11 | Plan | technical-director | technical-plan | tentative (only if A1 is not local) | — |
| 12 | Build | gameplay-engineer | implement-change | planned | — |
| 13a | Verify | qa | verify-change | planned | — |
| 13b | Verify (visuals) | art-director | visual-review | tentative (if 10c changes the view) | — |
| 14 | Play (rooms 1–5, fresh playtester) | playtester | playtest-session | planned | — |
| 15 | Review | game-director | review-outcome | planned | — |

## Route changes

After 9a/9b (53, 54): both done. The room 1–2 findings are tuning, rules and clarity within Option A, so no Decide now (D1/D2 held for a retest). 54 saw only room 2. Opened in parallel: QA fact checks and bots (10a), designer spec update (10b), art display (10c). Build, Verify, Play, Review follow.

## Next action

- `qa` starts 10a from `55-studio-to-qa.md`; the result is addressed to `studio`.
- `game-designer` starts 10b from `56-studio-to-game-designer.md`; the result is addressed to `studio`.
- `art-director` starts 10c from `57-studio-to-art-director.md`; the result is addressed to `studio`.
- Then Route, waiting for all three. QA defects or a spec change go to Build; a QA finding that contradicts the spec's intent goes back to the designer; if the designer or the art director finds the cheap fixes insufficient or a facing change necessary, Decide (`game-director`).

## Outcome

(Filled at Close.)
>>>END

<<<FILE @log-recent
## 050-route · 2026-10-15

Status: active. Open: 46-studio-to-gameplay-engineer.md.

After 7h/7j (44 pass; 45 done): visuals accepted (V-6 from code; V-7 and F4 left to Play and Review). The designer ruled the manual is right and the test too literal (D-009), so 7k opens (46), test only; 7k-O is dropped and 7l is planned. 7l needs `manual.md` beside `repo/`; the next Route decides how.

## 052-route · 2026-10-15

Status: blocked-on-owner. Open: none.

After 7k (47): the test fix is built but the engineer did not run the suite. AC-15 needs the unchanged `manual.md` beside `repo/`, which no Role workspace has (29, 40, 47); another QA round would repeat the same missing input. Escalated to the Owner (48; A = Owner runs the suite, recommended; B = Owner places `manual.md` for QA). 7l is tentative on B.

## 054-resume · 2026-10-15

Status: active. Open: 49-studio-to-playtester.md.

After the Owner chose A (48, D-010): the suite ran 40/40 with the unchanged `manual.md`, so AC-15 passes. Goal back to `active`. 7l is skipped, and Play (8) opens as 49, a fresh Handoff composed from permitted information only. Review unchanged.

## 056-route · 2026-10-15

Status: active. Open: 51-studio-to-game-designer.md, 52-studio-to-playtester.md.

After Play (50): the report covers room 1 only (scripted, two defeats) and shows experience issues, not defects. Diagnose re-opens (9a, 51) per the Play return rule. A second Play (9b, 52, fresh playtester) opens in parallel for the unseen rooms. Review waits for both.

## 059-route · 2026-10-15

Status: active. Open: 55-studio-to-qa.md, 56-studio-to-game-designer.md, 57-studio-to-art-director.md.

After 9a/9b (53, 54): both done. The room 1–2 findings are tuning, rules and clarity within Option A, so no Decide now (D1/D2 held for a retest). 54 saw only room 2. Opened in parallel: QA fact checks and bots (10a), designer spec update (10b), art display (10c). Build, Verify, Play, Review follow.
>>>END

<<<FILE goals/G-001-combat-monotony/58-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 58
from: qa
to: studio
stage: Observe
outcome: done
---
# 58: qa → studio — Six open facts settled (two partly); one low-severity contradiction, no short bite warning

## Task

Pass this report to `game-designer` for the spec gaps listed below and to `gameplay-engineer` if the designer rules on D-58-1. The build was not changed. All findings come from the trace and player views and the bot runs, at 60 FPS and 30 FPS unless noted.

## Context

G-001, handoff 55. I used two run rounds: 5 runs in the first and 17 in the second (labels in brackets below). I have one round left and did not use it. Items 4 and 5 are only partly settled; see "Not settled".

## Findings

### Summary

| # | Fact | Result | Against spec |
|---|---|---|---|
| 1 | Short bite warning | Not real. The "rears back" line belonged to a different grub. | Matches |
| 2 | Dash distance | 4.00 tiles in open floor at both frame rates. Clamped at walls. | Matches. Wall behaviour is unspecified. |
| 3 | Facing after dash | Dash sets facing to the dash direction. | Unspecified |
| 4 | Swipe vs grub states | (a) hits but gives no knockback; (b) hits, 1.0-tile knockback; (c) a second swipe hits. "(miss)" not seen first-hand. | One contradiction (D-58-1) |
| 5 | Grub on you | Hit in all four facings. | Matches. Knockback direction unsettled. |
| 6 | Bots | Format found. No idle bot exists, so idle runs came from the trace view. | n/a |

### 1. Possibly short bite warning (settled: no short warning)

Runs: `trace/grub-room1-idle-30` (`room 1`, `fps 30`, `end 16`) and `trace/grub-room1-idle-60` (same at `fps 60`).

- The playtester's session restarted room 1 about 10.0 s into the run. Idle room 1 at 30 FPS reproduces their log with a +10.0 s offset:

| Playtester log | Idle trace at 30 FPS | Trace +10 s |
|---|---|---|
| "rears back (left)" at 11.90 s | `windup who 0 side left` at 1.900 | 11.90 |
| heart lost at 11.97 s | `hurt` at 1.967 | 11.97 |
| hits at 13.47 s and 14.97 s | hurts at 3.467 and 4.967 | 13.47, 14.97 |

- The bite at 1.967 belongs to grub#2. Its wind-up (side `above`) started at 1.400 and its strike at 1.900 (0.500 s later).
- The "rears back (left)" line at 1.900 belongs to grub#0. That grub struck at 2.400 (0.500 s later) and hurt nobody, because the player was invulnerable.
- At 1.900 grub#2's strike and grub#0's wind-up started in the same tick. So the heart loss followed the "rears back" line by 0.067 s, but from another grub. The misread was by the playtester, and the build is correct.
- No grub strikes less than 0.500 s after its own wind-up in either trace, at 30 or 60 FPS. The pairs below were taken from the wind-up and strike rows:

| FPS | Grub | Wind-up start | Strike start |
|---|---|---|---|
| 30 | #2 | 1.400 | 1.900 |
| 30 | #0 | 1.900 | 2.400 |
| 30 | #1 | 2.900 | 3.400 |
| 30 | #2 | 2.967 | 3.467 |
| 60 | #2 | 1.383 | 1.883 |
| 60 | #0 | 1.883 | 2.383 |

- A heart is lost 0.05–0.07 s after strike start, while the lunge closes to 1.0 tile. That is 0.55–0.57 s after the wind-up line, which explains the playtester's "0.5–0.65 s" for the other bites.
- 30 vs 60 FPS: event order is identical and timestamps differ by at most 0.034 s (hurt 1.967 vs 1.933). The first down is at 4.967 vs 4.950. This is within the 0.07 s allowance.
- The "rears back (side)" line does not say which grub struck. With several grubs, a cue for one can coincide with a hit from another. This is a readability note for the designer, not a defect.

### 2. Dash distance (settled; wall behaviour is a spec gap)

Runs: `trace/dash-open-and-wall` (60 FPS) and `trace/dash30` (30 FPS), both in `room empty`; `play/dash-wall-view` (60 FPS).

- Open floor: 8→12 and 12→8 (60 FPS), and 8→12 and 15→11 (30 FPS). That is exactly 4.00 tiles at both frame rates, a difference of 0.00 against the 0.25 allowance. The dash lasts about 0.25 s (`dash_end` at 0.233 s after the first logged frame, which is 0.25 s from the press). Invulnerable for the whole dash.
- Next to a wall the dash is clamped at the room edge:
  - 12→15 moved 3 tiles.
  - 4→0 moved 4 tiles.
  - A dash from y=0 upward or from x=15 rightward moves 0 tiles but still prints "you dash right", turns on invulnerability for 0.25 s and spends the dash. In `play/dash-wall-view`, from 14 it moved 1 tile, and the second dash at the wall did not move.
- The spec says "4 tiles". It is silent on walls. The manual gives no distance, only "a quick burst".
- The playtester's "2–3 tiles" is not the build's behaviour. A likely cause is that the player view draws only every 0.5 s (hypothesis).
- Cooldown: a dash 0.3 s after another was refused with "(dash not ready)" (`dash30`). I did not measure the exact cooldown.

### 3. Facing (settled; spec silent)

Runs: `play/facing-default`, `play/facing-dash60` and `play/facing-dash30`.

- Default facing is right. With spitters at 7.2 and 8.8 either side of `P` at 8, a swipe at 0.1 s hit only the right one ("spitter hit (1 left)").
- A dash changes facing to the dash direction:
  - Spitters at 11 and 13; the player moved left briefly, then dashed right at 0.3 s. The dash passed through the spitter at 11.
  - At 0.8 s the player stood at about 12, with one spitter behind and one ahead. The swipe hit one spitter only ("spitter hit (1 left)"), the one ahead and to the right (`z` at x=13), not the one behind (`s` at x=11).
  - Results are identical at 30 and 60 FPS.
- Facing was inferred from which enemy was hit. The player view does not print facing.
- The spec says only "a swipe in the facing direction". Whether a dash sets facing is unspecified: spec gap, hand to `game-designer`.

### 4. Swipe timing against grubs (partly settled)

Runs: `trace/strike-a` (swipe at 0.51), `trace/strike-b` (swipe at 0.54) and `trace/recovery-knock` (swipes at 1.0, 1.4, 1.8 and 2.2), all at 60 FPS with a grub at 9.24 and the player at 8.

- **(a) In Strike.**
  - Strike began at 0.517. The swipe at 0.51 took effect in frame 32 (0.533) and hit the grub, which went to HP 1. The same tick shows `hurt`, so the player still lost a heart.
  - The grub did not stop: it kept its Strike and moved from 9.13 to 8.24 into Recovery.
  - No `knockback` event occurred in this run.
  - The strike damages the player 1–2 frames after it starts, and the player is stunned from that moment. A swipe pressed even 0.03 s later is rejected as `stunned` (`strike-b`: pressed at 0.54, rejected at 0.567).
  - A swipe can therefore hit a grub in Strike only on the same tick or frame as the strike starts.
- **(b) In Recovery, adjacent.**
  - The swipe at 1.0 (taken at 1.017) hit a grub at 8.24, 0.11 tiles from the player. HP went 2→1 and a `knockback` event fired.
  - The grub ended at 9.24 by 1.333, a push of exactly 1.00 tile (one frame at 1.017 moved it 0.08, consistent with 1 tile in 0.2 s). It stayed in Recovery with its timer running on.
- **(c) After the first hit.**
  - The second swipe at 1.4 (taken at 1.417) hit the grub at 9.24, 1.11 tiles from the player at 8.13 and within the 1.5 reach. It was defeated and "room cleared" printed.
  - Knockback of 1 tile does not move an adjacent grub out of reach.
- **"(miss)":** the trace shows `attack ... hits []` for swipes at 1.8 and 2.2 with no enemy left. I did not run the player view for a living grub out of reach, so I did not see the "(miss)" text myself. Handoff 54 saw "(miss)" at 1.0 s in room 2 with all grubs far away.
- **Input delay:** inputs sometimes take effect one or two frames after their script time (0.51→0.533, 0.54→0.567).

**D-58-1 (low): no knockback when the first hit lands in Strike.**
- Expected: `design/combat.md` says "First hit (HP 2→1): the grub is knocked back 1 tile over 0.2 s". It states no exception for Strike.
- Actual: the grub took the hit (HP 1, damaged state) but showed no `knockback` event and no push (`strike-a`). The Strike continued and still damaged the player.
- Conditions: 60 FPS only. I did not repeat at 30 FPS because the case needs a same-tick hit.
- Severity: low. The case is rare because of the timing above, and the effect is only that the grub is not pushed.
- Whether a hit in Strike should interrupt, knock back or be ignored is not specified (the spec defines wind-up cancel and defeat-mid-state only). **Hand to `game-designer`** for a ruling before the engineer acts.
- Acceptance criteria once ruled (conditions: at 30 and 60 FPS, the room and grub as in `strike-a`):
  1. A first hit that lands in a grub's Strike produces the ruled outcome (knockback of 1 tile, or an explicit exemption), and the trace shows it.
  2. The hit line "grub hit (1 left)" still prints.
  3. The strike's own damage follows the ruling.
  4. The Wind-up (AC-5), Recovery and defeat cases are unchanged.

### 5. Grub "on you" (settled for the swipe; knockback direction unsettled)

Runs: `play/onyou-right`, `play/onyou-left`, `play/onyou-up` and `play/onyou-down` (60 FPS; each has the grub spawned on the player's tile, a `move` in that direction at 0.01 and a swipe at 0.2).

- Right, left, up and down all print "you swipe: grub hit (1 left)" and "the grub is open (on you)" at 0.2.
- A swipe hits a grub on the player's tile whichever facing is used. That matches the spec's "true position" rule.
- The hit cancelled the wind-up, and the grub rewound to the next "rears back (on you)" at 0.8 s. That is 0.6 s of Recovery, as in AC-5.
- Display: the grub is drawn beside `P` (right of `P` at the left, top and bottom walls; left of `P` at the right wall), as D-006 requires.
- **Limitation:** every test placed the player at a wall (x=15, x=0, y=0, y=8), and the facing was set only by a `move` into that wall; I did not read it from the trace. The grub still printed "(on you)" at 0.8 s, 0.6 s after a hit that should have knocked it back 1 tile. A hypothesis, not a finding: when the grub is exactly on the player, the knockback direction is the facing direction, and my wall positions clamped it to no movement. Where an on-you grub is pushed in open floor is unsettled and is also a spec gap.

### 6. Bot reference data

- **Format:** the script keys are `bots <list>`, `rooms <range|list>`, `fps <30|60>` and `limit <seconds>`. The failed script used `room 1`, which the parser does not know. The key is `rooms`.
- `repo/README.md` lists only camper, walker and dodger. `reactive` exists in `bots.py` but is missing from the README (cosmetic).
- **No idle bot exists.** `camper` stands still but turns and swings at enemies in reach. For passive (idle) numbers I used the trace view with no inputs (`trace/idle-room2-60` … `idle-room5-60`, `grub-room1-idle-30` and `-60`).
- Bots start each room fresh with 3 hearts and no run flow (no carry-over, no heal, no 1.5 s transition). Their decisions depend on the frame step, so a bot run at 30 and 60 FPS can differ and cannot be used for AC-17.

**Idle player** (no actions; trace, 60 FPS unless noted):

| Room | Down at (s) | Hearts lost | Hit by | Actions |
|---|---|---|---|---|
| 1 | 4.95 (60), 4.97 (30) | 3 | grub 3 | 0 |
| 2 | 5.05 | 3 | grub 3 | 0 |
| 3 | 5.52 | 3 | shot 3 | 0 |
| 4 | 5.03 | 3 | grub 3 | 0 |
| 5 | 4.53 | 3 | grub 2, shot 1 | 0 |

**Bots, 60 FPS** (`bots/ref60`). Cells give clear time in s, hearts lost, attacks, dashes. "NOT" = not cleared; the bot went down.

| Bot | Room 1 | Room 2 | Room 3 | Room 4 | Room 5 |
|---|---|---|---|---|---|
| camper | 3.5, 0, 6, 0 | 4.8, 0, 7, 0 | NOT 5.5, 3 (shot), 0, 0 | NOT 6.9, 3 (shot), 4, 0 | NOT 6.9, 3 (shot), 6, 0 |
| walker | 3.5, 0, 6, 0 | 5.1, 0, 8, 0 | 9.0, 0, 6, 0 | 9.1, 0, 8, 0 | 11.2, 0, 10, 0 |
| dodger | 3.5, 0, 6, 0 | 5.1, 0, 8, 0 | 11.8, 0, 6, 4 | 10.0, 0, 8, 1 | 9.8, 0, 10, 2 |
| reactive | 3.5, 0, 6, 0 | 6.3, 1 (grub), 8, 3 | 11.8, 0, 6, 4 | 12.9, 0, 9, 5 | 11.1, 0, 11, 2 |

**Bots, 30 FPS** (`bots/ref30`):

| Bot | Room 1 | Room 2 | Room 3 | Room 4 | Room 5 |
|---|---|---|---|---|---|
| camper | 3.5, 0, 6, 0 | 4.9, 0, 7, 0 | NOT 5.5, 3 (shot), 0, 0 | NOT 6.9, 3 (shot), 4, 0 | NOT 6.9, 3 (shot), 6, 0 |
| walker | 3.5, 0, 6, 0 | 4.8, 0, 8, 0 | 9.2, 0, 6, 0 | 9.1, 0, 8, 0 | 12.3, 0, 10, 0 |
| dodger | 3.5, 0, 6, 0 | 4.8, 0, 8, 0 | 9.5, 0, 6, 2 | 10.1, 0, 8, 1 | 14.5, 0, 10, 6 |
| reactive | 3.5, 0, 6, 0 | 4.8, 0, 8, 0 | 9.5, 0, 6, 2 | 14.3, 0, 8, 6 | 11.1, 0, 10, 2 |

### Spec gaps for `game-designer` (not defects)

- Does a dash set facing? (Observed: yes.)
- What does a dash into a wall do? (Observed: it clamps, and a dash against the wall is spent without movement.)
- What happens to a grub hit during Strike (see D-58-1)?
- In which direction is a grub that stands exactly on the player knocked back?
- Should the "rears back" line name which grub it is, given that a cue and a hit from different grubs can coincide?
- `manual.md` gives no dash distance (optional documentation note).

### Not settled

- Item 4, "(miss)" text with a living grub out of reach: not seen in the player view first-hand. Only handoff 54's observation and the trace's empty hit list support it.
- Item 5, knockback of an on-you grub in open floor: not tested. A run with `player 8 4` and a grub on that tile would settle it.
- D-58-1 was observed at 60 FPS only.
- Idle runs for rooms 2–5 were done at 60 FPS only. The 30 FPS idle run covers room 1 only.

## Decisions already made

- D-001, D-003 and D-006 were respected. I changed no build files and made no balance judgement.

## Constraints

- The Studio must keep the cell contents of the bot tables as measured here.
- Do not read the bot numbers as AC-17 evidence (see item 6).

## Open questions

- Should I use the remaining run round to settle the "Not settled" items above, or does `game-designer` need to rule on the spec gaps first?

## Expected output

The Studio routes D-58-1 and the spec gaps to `game-designer`, and the rest to review.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md, manual.md, repo/bots.py
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-006-overlap-display-and-practice-room-manual.md
- Previous handoff: goals/G-001-combat-monotony/55-studio-to-qa.md
>>>END

<<<FILE goals/G-001-combat-monotony/59-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 59
from: game-designer
to: studio
stage: Route
outcome: done
---
# 59: game-designer → studio — Spec updated with A1–A3 and A5; manual draft for the Owner; retest guideline

## Task

Route the updated `design/combat.md` and D-011 to Build, to Verify (acceptance criteria AC-19…AC-27) and to QA's open check (55). Send the manual draft below to the Owner to place in `manual.md` (D-005, D-007 pattern). Use the retest guideline for the next Play and Review. Nothing goes to `game-director` now.

## Context

G-001 (combat monotony), Option A (D-002). Handoff 56 asked for A1, A2, A3 and the A5 gaps, the ring question for room 2, A4's trigger, the manual draft and a retest guideline. I did not run `play` or `bots`: the changes are rules with acceptance criteria and the evidence I would add (still-player runs, 53) already exists. The retest needs a reactive player, which I cannot script.

## Findings

### What changed in `design/combat.md` (see D-011)

- **A1 wind-up spacing:** no grub starts a Wind-up within 1.0 s [tune] of another grub's Wind-up start (cancelled or defeated ones still count). A blocked grub is Waiting.
- **Second rule for the ring (answer to the open question):** A1 alone does not handle room 2. With four grubs it spaces the bites but still lets four grubs stand on all sides, and the tester felt "no gap to leave through". So at most 2 grubs may be within 1.5 tiles of the player at once; the others wait at 2.0 tiles. Result for a still player in room 2: at most 2 grubs close, one committed bite at a time, bites at least 1.0 s apart, and the player has a gap to dash or counter. The 2-in-Wind-up/Strike limit stays as a backstop.
- **A2:** hit-stun 0.3 s → 0.15 s [tune]. Invulnerability to 0.8 s is unchanged. No buffer.
- **A3 body hit:** an enemy within 0.5 tile of the player (distance 0 too) is hit by every swipe whatever the facing. This also closes the distance-0 swipe gap, so no separate rule is needed.
- **A5 dash and facing:** a dash with a direction sets facing to it (like movement). A dash without a direction keeps facing. A queued attack fires in the dash direction.
- **A5 dash distance:** up to 4 tiles in 0.25 s, stopping at the room edge, invulnerable throughout. QA's check (55) is judged against this rule.
- **A5 swipe cases:** a swipe resolves on true positions in every grub state. A hit during Strike cancels that strike (attacks resolve before enemy damage in a tick) and puts the grub in a 0.6 s Recovery. A swipe in Recovery hits normally.
- **A5 miss wording:** "(miss) too far" when an enemy is within 2.5 tiles but beyond reach; "(miss) not in front" when an enemy is within 1.5 tiles but outside the cone and the body radius; "(miss)" alone otherwise. The word "(miss)" is kept, so AC-11 and the manual's phrase still hold.
- **New acceptance criteria AC-19…AC-27** (spacing, cap, turns, hit-stun, body hit, dash and facing, dash distance, Strike/Recovery swipes, miss wording), each stated for `fps 30` and `fps 60`. AC-17 now covers them. AC-1…AC-18 are unchanged except the stun value inside the text, and AC-11 notes the miss causes.
- Room layouts, knockback, the grub cycle, spitters, the cone and reach are unchanged.

### A4 and the held items

- **A4 (120° cone) stays held.** It comes in if the retest's trace shows the "(miss) not in front" line on at least 1 in 4 swipes of a reactive session where an enemy was within reach, or testers still report missing grubs standing diagonally in front after A3 is in. Then widen to 120° [tune] and add an AC.
- **D1 (facing mechanic)** goes to `game-director` only if the retest still reports swipes into air after dashes or trouble turning, with A3 and the dash-facing rule in. **D2 (room 1 composition)** only if four grubs still read as a wall after A1 and the cap. This is as agreed in 56; neither is routed now.
- The cheap fixes do not need a facing mechanic or a room composition change, so there is no hand-back to the Director.

### Manual draft for the Owner (group B; text only, `manual.md` not edited)

Keep every phrase `ManualTest` checks (glyphs, "run over — rooms cleared: N", "press attack to start again", "a grub rears back", "the grub is open", "(miss)", "(too soon)", "(stunned)", "(down)", "(dash not ready)", the On screen section with `x` and the practice room). The phrase check ignores line wraps (D-009). Suggested placement:

**1. Controls section: replace the Attack and Dash bullets with:**

- **Attack**: a short swipe in the direction you face. It reaches a little more than one tile in a wide cone and hits every enemy inside it. An enemy right next to you or on your tile is always hit, whichever way you face. After a swipe you must wait a moment before the next. You can swipe an enemy at any time, even while it rears back to bite: a hit on a grub that is rearing back stops that bite. This is the best answer to a bite.
- **Dash**: a quick burst of up to four tiles in a direction (or the way you face). You turn to face the way you dash. You cannot be hurt while dashing, and you can dash through enemies and shots. A dash stops at the wall. It needs a moment to recharge.
- **Getting hit** costs a heart and stuns you for a very short moment (less than a quarter of a second), during which you cannot move, swipe or dash. Then you are safe for a little under a second.

**2. Add to What you hear and read, after the swipe-result bullet:**

- The first hit on a grub or spitter knocks it back about a tile and leaves it hurt. It may be out of reach afterwards: step toward it to hit it again.
- A swipe that does nothing says why: "(miss)" nothing was hit; "(miss) too far" an enemy is near but out of reach, step closer; "(miss) not in front" an enemy is next to you but outside the swipe's cone, face it first; "(too soon)" you are still recovering from the last swipe; "(stunned)" you were just hit; "(down)" you are out of hearts. (Replace the existing bullet on swipes that do nothing with this one.)

**3. Add to the On screen paragraph (after the sentence on grubs drawn beside you):**

Grubs take turns: at most two crowd you at a time, and they do not start to bite at the same moment. A grub waiting for its turn stands a couple of tiles away as a small `g`.

Keep the practice-room paragraph and the `x` row as they are.

### Retest guideline (design-side, qualitative)

Also written into `design/combat.md` ("Retest guideline"). Do not forward it to a Playtester.

- **Room 1:** a skilled player who reads the cues clears it and usually keeps most hearts. Damage comes from a misread or mistimed dash, not from a bite they could not avoid. They can step out, dash through, or hit the winding-up grub, then punish the open grub. A grub on them can be hit.
- **Room 2:** a skilled player can break the ring: only two grubs crowd them, bites come one at a time, and they can dash to a side or wall and fight from a free line. It is a real fight where a hit or two is plausible, but a player who tries clears it, usually with at least one heart left. A player standing still loses.
- Judge monotony only on a survived run.
- Ask the retest to report: swipes with "(miss) not in front" where the player aimed at that grub (A4); swipes into air after a dash (D1); whether four grubs still arrive as one clump that feels like a wall (D2 / Option B).

## Decisions already made

- D-001: one attack button plus dash; no new input.
- D-002: Option A first; staggered arrival (part of B) deferred.
- D-003: room mix across rooms; zero hearts ends the run; clear heals one heart.
- D-006: enemies may overlap the player and are never hidden.
- D-009: the `ManualTest` phrase check ignores line wraps.
- **D-011 (new):** the A1–A3 package, the engagement cap and the A5 rules; A4, D1 and D2 rejected for now with revisit triggers.

## Constraints

- All timings in seconds; hold at 30 and 60 FPS (spacing 1.0 s, stun 0.15 s and dash 0.25 s included).
- No new input (D-001). Reuse the existing grub states and timers.
- Do not forward this handoff, the retest guideline or the design spec to a Playtester unchanged (design-side content).

## Open questions

- **For QA (55):** results on dash distance, facing and swipe cases are to be checked against the rules above. Where the build differs, it is a defect, unless QA shows a rule cannot be built.
- **For Build:** report as built the Waiting behavior of a blocked grub (position held, following a moving player), and whether the display draws per principle 4 still hold with it.
- **For Verify / Review:** the values 1.0 s spacing, the cap of 2 and the 0.15 s stun are [tune]. Retune in this order if the retest says too harsh or too soft: spacing (0.8–1.5 s), cap (2 or 3), stun.
- **For the art-director (optional):** nothing new is required. The "(miss)" cause wording and the Waiting grubs use the existing glyphs; the art-director may review readability of the waiting grubs at 2.0 tiles.

## Expected output

- **Build:** implement the rules in `design/combat.md` (grub spacing and cap, stun 0.15 s, body hit, dash facing and edge stop, Strike/Recovery swipe handling, miss causes) and the AC-19…AC-27 checks.
- **Verify (QA):** run AC-1…AC-27 at both frame rates and settle the dash, facing and swipe cases against the spec.
- **Owner:** place the manual draft in `manual.md`; Verify then re-runs the full suite (D-008, D-009).
- **Play and Review:** one retest of rooms 1 and 2 by a reactive player (a live session, or several short reactive scripts), judged against the retest guideline. A `run_bots` round needs the bots script format; the earlier failure (53) was a format mismatch and should be checked first.

## Sender assessment

- **Confidence:**
  - High: spacing plus cap addresses the ring seen in 54, and the body-hit rule addresses "on you" swipes. Both follow from rules and from the still-player runs in 53.
  - Medium: 0.15 s stun and 1.0 s spacing are the right strength. They rest on one scripted playtest and no reactive data.
  - Low: dash facing as the fix for swipes into air. It is the minimal rule; the backstep variant is held for the Director.
- A still player in room 2 now meets bites at least 1.0 s apart (down about 2 s after the first bite at the earliest), so the idle reference time to down changes. It is a reference, not a target.
- No `play` or `bots` run was used in this step. The retest guideline is what a live or reactive session is judged against.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md, studio/skills/make-decision.md
- Project: design/combat.md, design/combat-visuals.md, manual.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-response-scope.md, decisions/D-003-run-end-and-room-rules.md, decisions/D-006-overlap-display-and-practice-room-manual.md, decisions/D-009-manualtest-phrase-check-ignores-line-wraps.md, decisions/D-011-grub-turns-stun-body-hit-dash-facing.md
- Previous handoff: goals/G-001-combat-monotony/56-studio-to-game-designer.md
>>>END
