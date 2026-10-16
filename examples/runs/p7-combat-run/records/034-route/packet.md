# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/35-game-designer-to-studio.md, goals/G-001-combat-monotony/36-qa-to-studio.md
next_seq: 37
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha 29993eac7bb0; run through the project's run commands)
log: last 5 of 12 entries in @log-recent; the full history is goals/G-001-combat-monotony/log.md

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/35-game-designer-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/36-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 37
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
decisions/D-003-contact-edge-exact-reach-and-lunge-band.md
decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
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
goals/G-001-combat-monotony/25-studio-to-playtester.md
goals/G-001-combat-monotony/26-studio-to-game-designer.md
goals/G-001-combat-monotony/27-playtester-to-studio.md
goals/G-001-combat-monotony/28-studio-to-game-designer.md
goals/G-001-combat-monotony/29-studio-to-qa.md
goals/G-001-combat-monotony/30-game-designer-to-studio.md
goals/G-001-combat-monotony/31-game-designer-to-studio.md
goals/G-001-combat-monotony/32-qa-to-studio.md
goals/G-001-combat-monotony/33-studio-to-game-designer.md
goals/G-001-combat-monotony/34-studio-to-qa.md
goals/G-001-combat-monotony/35-game-designer-to-studio.md
goals/G-001-combat-monotony/36-qa-to-studio.md
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
decisions/D-003-contact-edge-exact-reach-and-lunge-band.md — D-003: A miss of exactly the reach is inside the contact band; measured lunge band recorded (follow-up to D-002)
decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md — D-004: Rooms 4–5 get a rule-based 0.6 s cue gap; the brute's wind-up is not cancelled by a swipe; the room 2 spitter is deferred
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

- Observe: done (scripted play, rooms 1–3 + practice room; 02). FPS divergence (qa): done (16, 20); the contact-edge graze is accepted (D-002, D-003).
- Diagnose: second pass done (31). Melee enemies share one answer (S1, the core of the Goal); rooms 4–5 spitter crossfire is unfair because cue gaps are only 0.2 s (S4). Evidence is scripted play; runner, brute and crossfire for a human are unconfirmed. A third Diagnose pass without progress goes to `game-director` review (loop limit).
- Observe (qa): room 2 grub hit after swipe is not a defect (32); the swipe landed during the lunge. Open: trace of rooms 3–4 spitter fire times (34), because the playtest said "in sync" and "opposite corners", which conflicts with the spec.
- Decide: skipped. The diagnosed options (31) are variant parameters, a per-variant cancel flag, spitter timing and room contents, all inside D-001 and the pillars. Tentative again (game-director) if Design finds the need for a new enemy type, healing, new input, or a scope or priority change.
- Design: 9b done (30, D-003). Open (33): Options 1 and 2 (Option 3 at the designer's discretion), manual wording on when a swipe cancels, and the "3 in the air" wording.
- Plan: skipped (approach local, reuses the enemy update loop). Returns if the same criterion fails verification twice.
- Build: 0.5 done (10, 18). Planned after Design 33 (new build 0.6).
- Verify (QA): criteria 1–17 pass for 0.5 at 30 and 60 FPS (24); new and changed criteria need Verify after the next Build. Verify (visual): V1–V11 need a graphical build, a proposed new Goal at Close; V12 open until a graphical build exists.
- Play: first pass done (27). Second pass planned after the next Verify; ideally hand-timed on rooms 2, 4 and 5 (runner, brute, crossfire; see 31 finding 5).
- Manual wording ("no more than 3 in the air") is true in rooms 1–5 only; included in Design 33.
- Review: planned (`game-director`), experience Goal. The Goal is not yet met.

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
| 8d | Verify (criteria 1–17; close 30 FPS gaps) | qa | verify-change | done (pass) | 23-studio-to-qa.md (result: 24-qa-to-studio.md) |
| 9a | Play | playtester | playtest-session | done | 25-studio-to-playtester.md (report: 27-playtester-to-studio.md) |
| 9b | Design (QA notes: exact-reach miss, lunge band) | game-designer | write-design-spec | done | 26-studio-to-game-designer.md (result: 30-game-designer-to-studio.md) |
| 10a | Diagnose (playtest issues 1–4) | game-designer | diagnose-experience | done | 28-studio-to-game-designer.md (result: 31-game-designer-to-studio.md) |
| 10b | Observe (room 2 grub hit after swipe) | qa | reproduce-defect | done (not a defect) | 29-studio-to-qa.md (result: 32-qa-to-studio.md) |
| 11 | Decide (if Design implies direction or scope change) | game-director | make-decision | tentative | — |
| 12a | Design (Options 1–2, manual wording) | game-designer | write-design-spec | open | 33-studio-to-game-designer.md |
| 12b | Observe (spitter fire times, rooms 3–4) | qa | reproduce-defect | open | 34-studio-to-qa.md |
| 13 | Build (build 0.6 per Design) | gameplay-engineer | implement-change | planned | — |
| 14 | Verify (after Build, 30 and 60 FPS) | qa | verify-change | planned | — |
| 15 | Play (fresh, hand-timed rooms 2, 4, 5) | playtester | playtest-session | planned | — |
| 16 | Review | game-director | review-outcome | planned | — |
| 17 | Next | studio | — | planned | — |

## Route changes

After 9b, 10a, 10b: all fit. Diagnose 31 needs no Decide (options inside D-001), so Decide stays tentative. Room 2 hit is not a defect (32). Opened Design (33, Options 1–2, manual wording) and, in parallel, a QA spitter-timing trace (34) to settle the "in sync" conflict. Build, Verify, Play are now planned.

## Next action

Run the game-designer step with 33-studio-to-game-designer.md and the qa step with 34-studio-to-qa.md; they are independent. Then Route: wait for both. If the trace contradicts the spec or 31's S4 cause, send the result back to the designer before Build; if QA confirms a spitter defect, route it to Build with the report. If Design implies a direction or scope change, open Decide (`game-director`).

## Outcome

(open)
>>>END

<<<FILE @log-recent
## 018-route · 2026-10-16

Status: active. Open: 21-studio-to-game-designer.md.

After 8 (Verify): partly fits. 1–15 and 16a–d pass; the walker difference is bot timing. QA found a frame-rate-dependent graze plus a cap and margin question, which only the designer can rule. 8b is now open (handoff 21). Added 8c Build (tentative) and 8d Verify (planned).

## 021-route · 2026-10-16

Status: active. Open: 23-studio-to-qa.md.

After 8b (Design): fits. The designer accepted the graze (D-002), ruled the cap is on cue starts, kept the walker margin and named the governing documents; the build does not change. 8c is skipped. 8d (QA) is open (handoff 23, no designer assessment) to run the 30 FPS gaps and criterion 17.

## 023-route · 2026-10-16

Status: active. Open: 25-studio-to-playtester.md, 26-studio-to-game-designer.md.

After 8d (Verify): fits. QA passed criteria 1–17 at 30 and 60 FPS; only V12 stays open (no graphical build). Opened 9a Play (fresh playtester, build and player profile only) and, in parallel, 9b Design for two non-blocking QA notes on the contact edge (wording and D-002 record).

## 027-route · 2026-10-16

Status: active. Open: 26-studio-to-game-designer.md, 28-studio-to-game-designer.md, 29-studio-to-qa.md.

After 9a (Play): does not fit "goal met". The playtest reports remaining monotony (melee enemies share one answer, dash unused, spitter crossfire) and one possible defect. Returned to Diagnose (10a, designer) and Observe (10b, qa) in parallel with open 9b. Decide, Design, Build, Verify and Play are tentative on the Diagnose result.

## 031-route · 2026-10-16

Status: active. Open: 33-studio-to-game-designer.md, 34-studio-to-qa.md.

After 9b, 10a, 10b: all fit. Diagnose 31 needs no Decide (options inside D-001), so Decide stays tentative. Room 2 hit is not a defect (32). Opened Design (33, Options 1–2, manual wording) and, in parallel, a QA spitter-timing trace (34) to settle the "in sync" conflict. Build, Verify, Play are now planned.
>>>END

<<<FILE goals/G-001-combat-monotony/35-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 35
from: game-designer
to: studio
stage: Route
outcome: done
---
# 35: game-designer → studio — Design spec for Options 1 and 2 (cue gap in rooms 4–5, brute not cancelled), Option 3 deferred, manual wording given

## Task

Route to **Build** (build 0.6, `gameplay-engineer`), then QA at 30 and 60 FPS, then a hand-timed Playtest. The spec is in `design/combat.md` (marked "step 35"), the decision in `decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md`. No Decide step is needed: no new enemy, no healing, no new input, no scope change. The visual spec was not changed (items for `art-director` below).

## Context

G-001 (combat monotony). Handoff 33 asked for a spec for Options 1 and 2 of handoff 31, a ruling on Option 3, and exact manual wording. The parallel QA trace of spitter fire times in rooms 3–4 (handoff 34) was not available. The spec for Option 1 does not depend on it. I ran no `play` or `bots` this step, because the changes are to a build that does not exist yet. So I verified nothing about build behavior. The bot expectations below are derivations and are marked.

## Findings

### Rulings

1. **Option 1: a cue gap rule in rooms 4 and 5.**
   - Rule: a spitter in those rooms may start a cue only if (a) no other spitter in the room has a cue running, (b) the last shot in the room was at least 0.6 s ago (1 ms tolerance so an exact tie counts), and (c) the existing shot cap allows it. Otherwise it waits 0.2 s and checks again (the existing cap-delay mechanism, and the delay carries forward).
   - Parameter: first-shot offset 1.2 s in rooms 4–5 (first shots at 1.8 s and 3.0 s, then alternating every 1.2 s, each spitter every 2.4 s). This meets the rule exactly, so the rule normally delays nothing. Room 3 and practice rooms keep offset 0.8 s and no gap rule, so **criterion 11 for room 3 does not change**.
   - It does not depend on the "in sync" claim. If two spitters ever would fire together, the second waits and the pattern settles to alternating.
   - Cap stays 3. Interval stays 2.4 s. Run length is unaffected.
   - Consequence I want the Build step to know: with 1.2 s spacing and shots living up to 5 s, the cap (fewer than 3 in flight at a cue start) can delay a cue when the player is far from the spitters. That is accepted.
2. **Option 2: the brute's wind-up is not cancelled by a swipe.**
   - A per-variant flag "swipe cancels wind-up": standard yes, runner yes, brute no. A swipe that damages a winding-up brute deals 1 damage, shows the message `the brute shrugs off the swipe`, does not stagger it, does not remove its cue, and the lunge goes ahead on its normal timer. A swipe that kills it in wind-up kills it with no lunge and no message. The dash still avoids the lunge.
   - Derivation: the brute's recovery is 1.2 s and a swipe takes 0.35 s, so up to four swipes fit in one window if the player is in reach and facing from the first frame, about three with a human reaction. So a full-health brute normally needs two windows ("dodge, hit, dodge, hit"). Not measured.
3. **Option 3 (spitter in room 2): deferred.** Reasons: it changes criterion 14 and the identity of room 2 in the same slice as the brute rule, which both address the "dodge the brute forever" problem. If both are built, the playtest cannot say which one worked. Revisit after the playtest (D-004). Rooms are unchanged in this slice.
4. **Signal beyond the manual (Option 2): yes, one.** The in-game message `the brute shrugs off the swipe` (a rule in the spec, text view). For `art-director` (presentation): a hit reaction on a brute swiped in wind-up that reads as "took the hit, not interrupted", clearly different from the stagger of a cancelled grub (V10 and V8 stay valid). I kept the existing `a grub rears back` message for all variants unchanged, so reaction rules with `text "rears back"` keep working. A brute-specific rear-back message was not asked for.
5. **Visual spec:** no change made. One sentence is outdated for rooms 4–5 ("spitter cues are normally 0.8 s apart ... rarely overlap"): there they are at least 0.6 s apart and never overlap by rule. `art-director` can update that.

### Changed and new criteria (all in `design/combat.md`)

| Criterion | Change |
|---|---|
| 6 Cancel | Now standard grub and runner only. A kill in wind-up still has no stagger and no lunge, for every variant. The brute is criterion 19. |
| 8 Variants | Brute still dies to four swipes in any phase (clarified). |
| 3 Dash works | Stated to hold for the brute too (the brute's answer now). |
| 11 Stagger and cap | Room 3 unchanged. Rooms 4–5: first shots at 1.8 and 3.0 s ±1 frame. Never more than 3 in flight in rooms 1–5, must be re-verified in 4–5 (timing changed). |
| **18 (new)** Cue gap in rooms 4–5 | Traces of rooms 4 and 5 (at least 15 s, both rates): no cue overlaps another; every cue starts at least 0.6 s (minus 1 frame) after the previous shot in the room; also after one spitter is killed and under cap delay; cue 0.6 s ±1 frame before the shot. Optional d: if the Build step can force both spitters to the same first shot, the gap must still hold; if not, QA says it was not run. |
| **19 (new)** Brute not cancelled | Practice room, brute about 1 tile away, player in the lane not dashing: (a) one swipe in wind-up: 1 damage, message, no stagger, lunge at 0.7 s ±1 frame, 1 heart lost; (b) two swipes: both deal damage, one lunge; (c) a killing swipe in wind-up: dies, no lunge, no message; (d) dash plus swipe: no damage taken, swipe damage applied; (e) recovery swipe: 1 damage, phase unchanged; (f) standard grub and runner still cancel. |
| 16a | Now lists 18 and 19 among the criteria that hold at both rates; 16e likewise. |
| 13, 14, 15 | Numbers unchanged. Expected effects below. |

### Bot expectations re-derived (none verified; the bots must be run on 0.6)

- **13 (rooms 3–5, walker 3–6 hearts, clears at least 2 of 3; dodger at most half of the walker's total and clears 3/3).** Room 5 has a brute: the walker ignores cues and swipes, so it now takes the lunge it used to cancel. Expect more hearts lost in room 5. In 0.5 the 60 FPS walker was already at exactly 6, so expect the upper limit to be exceeded at 60 FPS and the clears possibly to fall below 2. The effect of the cue gap on the walker could go either way (fire rate is unchanged: one shot per 1.2 s). Rule already in force (step 22): a walker outside the limit is reported to `game-designer` as a tuning question, not a build defect. **Cannot verify without running the bots.**
- **14 (rooms 1–2: walker at least 1 lost; dodger at most 1 lost, clears both).** Walker: the lower limit is safe. Dodger: **at risk** if its policy swipes the brute in wind-up to cancel. Bot rule I set: against the brute (`G`) the dodger sidesteps or dashes on the cue and swipes only in recovery. I could not check what `bots.py` does. **Build step: check the dodger's brute handling and change it if needed** (test tooling). QA reports dodger hearts in rooms 1–2 at both rates.
- **15 (dodger dashes at least once in each of rooms 3–5).** At risk in room 4: with a 0.6 s gap the dodger may sidestep everything and never dash. If it fails, QA reports to `game-designer`; it is not a build defect and I do not want the gap shortened to force it. **Cannot verify without running the bots.**
- **16c (dodger agrees between rates, per-room hearts within 1, same cleared set):** no reason for a change; verify.

### Exact manual wording (`repo/manual.md`, applied by the Build step)

Change the title to the new build number (for example `# Lantern Depths — how to play build 0.6`).

1. In "On screen", replace the Grub line with:

   `- **Grub (`g`)**: 2 swipes. **Runner (`r`)**: fast, 1 swipe, short warning. **Brute (`G`)**: slow, 4 swipes, long warning; a swipe does not interrupt it.`

2. In "Warnings", in the first bullet ("A grub rears back"), replace the sentence from `The line is fixed ...` to `... to cancel the lunge.` with these two sentences:

   `The line is fixed where you stood when the grub began; step 1 tile to the side or dash to avoid the lunge. A swipe (within 1.5 tiles) that lands during the warning cancels the lunge of a grub or a runner; once the lunge has started, a swipe no longer stops it.`

3. In the same bullet, after the sentence `After a lunge the grub is harmless for a while: that is the time to swipe it.` and before `Only one grub rears back or lunges at a time.`, add:

   `A brute is different: a swipe during its warning hurts it but does not stop it ("the brute shrugs off the swipe"), and it lunges anyway. Step aside or dash, then swipe it while it recovers (1.2 s).`

4. In "Warnings", the spitter bullet: replace `Shots are slow-looking but travel 3 tiles a second, and no more than 3 are in the air at once.` with:

   `Shots are slow-looking but travel 3 tiles a second. In rooms 1–5 no more than 3 are in the air at once. In rooms 4 and 5 the spitters take turns: after one takes aim and spits, there are at least 0.6 s before another takes aim.`

5. In "Warnings", the last bullet: replace `A swipe that interrupts a grub's warning staggers it for 0.4 s.` with:

   `A swipe that interrupts a grub's or runner's warning staggers it for 0.4 s. A brute is not staggered.`

(Scope of "3 in the air": rooms 1–5 only; a practice room with four or more spitters can have more, as the spec says.) The swipe-only-during-warning item from QA (handoff 32) is covered by item 2. It is a wording fix and not a rule change.

### What QA must verify

- Criteria 18 and 19 as written, at 30 and 60 FPS, and criteria 1–12, 17 re-run for regressions (6, 8, 11 are changed). Especially: room 3 timing unchanged (1.8, 2.6, 3.4 s); rooms 4–5 first shots at 1.8 and 3.0 s; at most 3 in flight in rooms 1–5.
- Standard grub and runner cancel and stagger exactly as before (19f).
- The bots on 0.6 at both rates: report the numbers for 13, 14, 15, 16c, and compare with the 0.5 values given in `design/combat.md`. Anything outside the criteria goes to `game-designer` with the numbers, and not "fixed" in the build. Say clearly what was not run (for example the forced-sync test in 18d).
- Manual lines applied as given, and the version title updated.
- The result of handoff 34 (spitter fire times in rooms 3–4 in build 0.5) when it arrives: if it shows the spitters really did fire together in 0.5, tell me. The gap rule covers it either way, but the cause would then be a build or cap-delay defect in 0.5.

### What the Playtester should focus on (without the expected result)

Hand-timed, no script reactions at a fixed delay. Rooms 2, 4 and 5, at least two attempts each. In every room: what you did against each kind of enemy and why; what you thought was going to happen before each hit and what happened instead; for each hit taken, what hit you and what you could have done. Rooms 4–5: when you got hit by a shot, whether the shot came from a line you had seen being drawn, and what you were doing at the time. Room 2: what you did about the large enemy, and whether you finished the room. Note anything you tried to do with the attack button on any enemy that did not behave as you expected. Report whether you used the dash, when, and why. Do not tell the Playtester about the cue gap, the brute flag or the messages.

## Decisions already made

- D-001 (attack and dash only): kept. D-002, D-003 (contact sampling, graze, exactly the reach): untouched.
- D-004 (new, this step): the cue gap rule and offset in rooms 4–5, the brute flag, Option 3 deferred. Alternatives rejected there: offset only without a rule, cap 2 in rooms 4–5, the rule in room 3, a new melee enemy or a wider lane, a partial-cancel brute rule, and Option 3 in this slice.

## Constraints

- No new input, no new enemy type, no healing, no scope change. Correct at 30 and 60 FPS (all timings run on accumulated time). Lane geometry is identical for all variants. The build must not change contact sampling.

## Open questions

- For `game-director` / Studio: none that need a Decide step.
- Whether a human who has not read the manual notices the brute's "shrug" message (the only in-game signal). If the playtest shows it is missed, the next step is a presentation change for `art-director`.
- Whether the walker/dodger numbers for 13–15 hold on 0.6: only the bots can say.
- Whether Option 3 or a room change is needed: decide after the hand-timed playtest.

## Expected output

Studio routes: Build (`gameplay-engineer`: spec items 1 and 2, the manual lines, check/adjust the dodger's brute policy, provide a forced-sync test if cheap), QA (above), then the Playtester briefed as above, and `art-director` informed of the two presentation items (brute hit reaction; spitter-cue spacing remark). A Build is needed.

## Sender assessment

Confidence: high that the rules are complete and testable (every new rule has a number and a player-observable check). Medium that the Option 1 offset and gap will feel right to a human (derived from the spec: a 0.6 s gap is enough for a 1-tile sidestep, which takes about 0.15 s plus reaction, but not measured). Medium-low on bot expectations for 13–15: the brute change plausibly pushes the walker over its limit in room 5 and the dodger's brute handling is unknown to me. I ran nothing, so nothing here is verified against a build.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat.md, design/combat-cues-visual-spec.md, repo/manual.md, project.md#vision, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-contact-edge-graze-accepted.md, decisions/D-003-contact-edge-exact-reach-and-lunge-band.md, decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
- Previous handoff: goals/G-001-combat-monotony/33-studio-to-game-designer.md
>>>END

<<<FILE goals/G-001-combat-monotony/36-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 36
from: qa
to: studio
stage: Observe
outcome: done
---
# 36: qa → studio — Spitters in rooms 3–5: build 0.5 conforms to the 0.5 spec at 30 and 60 FPS; the "sync" report is explained but not reproduced in a real room; one spec gap on shots that touch an invulnerable player

## Task

Check whether the spitters in rooms 3 and 4 (and 5) fire at the positions and times `design/combat.md` specifies, how many shots are in flight, and whether the playtest observations are defects.

## Context

G-001. Evidence: `run_trace` of rooms 3, 4 and 5 with a player who does nothing (30 and 60 FPS), plus two scripted practice-room traces. Those traces used the room-4 spitters at (15,0) and (15,8), the player at (8,4), a sidestep down 1 tile during the first cue, and in one script a return to y=4 (30 and 60 FPS each).

Per the spec header, build 0.5 behaves **without** the step 35 parts. So the expected 0.5 values are offset 0.8 s in every room, and no cue-gap rule. The trace does not print projectiles. "Shots in flight" below is derived from fire times, the 3.0 tiles/s speed and the hit times, and I label it as derived.

## Findings

### 1. Positions: match the spec's room table

- Room 3: spitters at (2,1), (14,7), (2,7). Match.
- Room 4: runner (1,4), standard (0,1), spitters (15,0) and (15,8). Match.
- Room 5: standard (1,1), standard (0,6), brute (4,8), spitters (15,0) and (15,8). Match.
- The "opposite corners" vs "same side" question has a simple answer. In rooms 4 and 5 both spitters are on the **east wall (x=15)**, one at the north end and one at the south end. A playtester would call that "opposite corners". The Studio's reading of "same side" is also correct. They do not contradict each other. The spec has no layout the build departs from.

### 2. Times: match the 0.5 spec at both rates

- **First shots.**
  - Room 3: 1.8, 2.6 and 3.4 s, at both rates.
  - Rooms 4 and 5: 1.8 and 2.6 s, at both rates.
  - The cue (`cue=True`) starts at `fire_in=0.600` and the shot is at 0.6 s later, within one frame, at both rates.
  - The rooms 4–5 times of 1.8 and 2.6 s are the 0.5 default (offset 0.8). The step 35 value (1.8 and 3.0 s) is not in the build yet.
- **Interval.** Room 4 spitter at (15,0): 1.8 then 4.2 s, an interval of 2.4 s. Other shots are later than the nominal 2.4 s only by the cap delay:
  - Room 4 spitter at (15,8): nominal 5.0 s, observed 5.2 s. Derived: the cue was due at 4.4 s with 3 shots in flight, and was released at 4.6 s once the 1.8 s shot was spent.
  - Room 3 spitter at (2,1): nominal 4.2 s, observed 4.6 s. Derived: the cue was blocked at 3.6 s with 3 in flight and released at 4.0 s.
  - This is the "delay carries forward" rule (spec "Cap delay").
- **Rate differences.** All fire and cue times match between 30 and 60 FPS to within one frame. Hit times differ by about one frame, as expected.

### 3. Cue windows and gaps (rooms 4–5, still player, both rates)

- Room 4 cues: spitter (15,0) at 1.2–1.8, spitter (15,8) at 2.0–2.6, spitter (15,0) at 3.6–4.2, spitter (15,8) at 4.6–5.2.
- Room 5 has the same pattern up to the observed times.
- No cue windows overlap.
- The gap from a shot to the next cue **start** by the other spitter is **0.2 s** at 1.8 → 2.0, and **0.4 s** at 4.2 → 4.6.
- That is the 0.5 behaviour ("old 0.2 s between consecutive cues"). It is below the step 35 rule of 0.6 s, as expected for 0.5.
- It explains why a player who sidesteps the first line can have the second spitter lock onto them 0.2 s later, which matches "hit while lined up for another warning".

### 4. Simultaneous fire: reproducible in the practice room, not observed in a real room

- In the practice-room replica of room 4 (script `d4-*-back`, both rates), **both spitters start a cue at 6.8 s** (`aim; aim`, both `fire_in=0.600`) and would both fire at 7.4 s. Both rates agree.
- Derived cause:
  - The (15,0) spitter's cue was due at 6.0 s. It was blocked by the cap, because the missed 2.6 s shot was still alive (shots live up to 5 s), plus the 4.2 s and 5.0 s shots.
  - It was released at 6.8 s, after the 4.2 s shot hit at 6.733.
  - The (15,8) spitter's cue was due at 6.8 s. Both therefore start together.
- This matches the playtester's "fired in sync", but only through the cap delay on a player who survives.
- The 0.5 spec text has nothing that stops two cues starting together (cap counts shots only; the spec allows up to 2 + the number of living spitters in flight). The 0.5 build conforms to its text. The step 35 gap rule would prevent this case.
- **Not shown in a real room:** my still player in rooms 4 and 5 dies at about 5.3 s and 6.2 s, before any cap delay. I have no real-room trace past 7 s.

### 5. Shots in flight (derived)

- Room 3: 3 in flight from 3.4 to 3.9 s, then 2, then 3 again with the 4.6 and 5.0 s shots. Never above 3 (spec limit: cap check of fewer than 3 at cue start).
- Room 4 (and 5): 3 in flight at 4.2 s (shots from 1.8, 2.6 and 4.2 s). The cap blocks the next cue until a shot is spent.
- Practice replica: 3 in flight from about 5.0 to 6.7 s (derived). It stays within 2 + the number of living spitters.
- No count exceeded the spec in any trace. I did not see a printed projectile count.

### 6. Hits: which cause

Cause names: **in flight** = a shot already fired that reaches the player; **new lock** = a cue that starts after the player has moved and aims at their current position; **misread** = the player re-entering a line.

- **Player stays still (rooms 3, 4, 5).**
  - Every shot hit is a shot aimed at the standing player at its cue start. It is already in flight by the time it arrives, about 2.1–2.55 s after firing.
  - Room 3: hits at 3.9, 4.7 and 5.5 s (down at 5.5 s, with no input at all).
  - Room 4: runner lunge at about 3.7 s, then shots at about 4.5 s and 5.3 s.
  - Room 5: shots at 4.33 s and 5.13–5.15 s, then the brute lunge at about 6.15 s (down).
  - This is "standing still is punished", as specified.
- **Player dodges one line (practice replica).**
  - Sidestep down during the first cue (1.3–1.55 s): the first shot passes at a lateral miss of about 0.87 tile (derived). No hit at either rate.
  - If the player **stays** at the new position, the next cue (2.0 s) locks there, and the 2.6 s shot hits at 4.97 s (30 FPS) and 5.0 s (60 FPS). Cause: **new lock** on the standing player.
  - Later hit at 6.93 s: a **new lock** again (cue at 3.6 s locked on y=5).
  - If the player steps back up (2.1 s), the 2.6 s shot misses. Then they stand at (8,4) and are hit at 4.33 s (30 FPS) and 4.35 s (60 FPS). That is the original **in flight** shot from 1.8 s, still flying along its line, and the player stepped back into it. Cause: **in flight, misread** by the player. It is not a build error. The shot's line is the original line.
  - The hit at about 6.75 s is a **new lock** on the standing player.
  - I saw no hit on a player who had left a line and stayed out of it.

### 7. Spec gap (not a defect): a shot that touches an invulnerable player is not consumed

- Room 4, still player. The first shot from (15,0) (fired at 1.8 s) should reach the player at about 4.35 s (derived: path 8.06 tiles minus the 0.4 reach, at 3.0 tiles/s). The player is invulnerable from the runner hit at 3.7 s until 4.53 s (30 FPS) or 4.48 s (60 FPS).
- The shot's damage lands **exactly when the hurt invulnerability ends** (4.533 at 30 FPS, 4.483 at 60 FPS). The same happens with the second shot: derived arrival 5.15 s, hit at 5.333 (30 FPS) and 5.283 (60 FPS), again the moment the hurt window ends.
- Hypothesis (not confirmed in code): a shot whose contact is blocked by invulnerability is not removed and is still within reach when the window ends.
- The spec says a shot "disappears … on contact with the player" and "invulnerability stops the damage". It does not say whether a blocked contact consumes the shot, and "two shots arriving together" only says at most 1 damage per window. **The expected behavior is not defined, so this is for `game-designer`, not a defect.**
- Player-visible effect: a hit can land 0.15–0.2 s after the shot visibly reached the player, and close hits can chain at the end of each 0.8 s window. This probably contributes to the "hit while lined up" and quick deaths in rooms 4–5.
- Severity if the designer rules it unintended: medium (hurts the experience). Frequency: any shot arriving during i-frames and still within 0.4 tile when they end. Not seen with the dash, because I did not test one.
- Observation (not a defect): in room 3 the three hits are 0.8 s apart, which equals the invulnerability window, so a still player loses all 3 hearts in 1.6 s.

### Verdict

- **Build 0.5 conforms to the 0.5 spec** for spitter positions, first-shot times, cue timing (0.6 s ±1 frame), interval and cap delay, and in-flight count, at 30 and 60 FPS.
- **Differs from the step 35 spec (0.6)** in rooms 4–5, as expected: offset 0.8 instead of 1.2, no 0.6 s gap rule. Criterion 18 does not apply to 0.5.
- No defect found. Two items go to `game-designer`: the invulnerable-contact gap (finding 7), and whether simultaneous cue starts after a cap delay in room 3 should be prevented (the step 35 gap rule only covers rooms 4–5).

## Decisions already made

- D-002: graze accepted. No reported hit was in a graze band. The shot lateral miss is not near 0.39–0.40 in any case above.

## Constraints

Report only. The build, tests and scripts in `repo/` are unchanged.

## Not covered

- The playtester's deaths at 15.75 s (room 4) and 11.1 s (room 5), the room 3 double fire at about 5.8 s, and their scripts: not reproduced. I had no script, and my still player dies at about 5.3–6.2 s. In my room 3 still trace nothing fires at 5.8 s before the death at 5.5 s.
- A 15 s or longer real-room trace with a surviving player in rooms 4–5, so no real-room cap-delay alignment and no cue overlap check beyond about 6 s.
- A spitter being killed, and the gap in rooms 4–5 with one spitter left.
- A dash through a shot, and the invulnerable-contact behavior with the dash.
- `run_play`, `run_tests` and `run_bots` were not run.
- Code-level causes (hypotheses are labelled as hypotheses).
- Exact lateral misses for each shot were derived, not read from a trace of the shot position.

## Open questions

- For `game-designer`: should a shot that touches an invulnerable player (dash or hurt) be removed, or keep going and hit once the window ends? Same question applies at a lesser scale to lunges.
- For `game-designer`: is two cues starting together after a cap delay acceptable in room 3 and practice rooms?
- For `studio`: if a real-room check is wanted before 0.6, a reaction-rule script that dodges (as in the manual's example) in rooms 4 and 5 for 15 s or more would give the trace. I did not use my last run on it.

## Expected output

Studio routes findings 7 and the room-3 simultaneous-start question to `game-designer`. Handoff 27's room 4–5 items can be treated as explained by the 0.5 spec (0.2 s lock gap, cap alignment, unconsumed shot), pending the step 35 build.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md, repo/manual.md, project.md#current-state, the build in repo/
- Decisions: decisions/D-002-contact-edge-graze-accepted.md
- Previous handoff: goals/G-001-combat-monotony/34-studio-to-qa.md
>>>END
