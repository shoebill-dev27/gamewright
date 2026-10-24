# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/67-game-director-to-studio.md, goals/G-001-combat-monotony/68-game-designer-to-studio.md
next_seq: 69
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha c09552011dd4; run through the project's run commands)
log: last 5 of 23 entries in @log-recent; the full history is goals/G-001-combat-monotony/log.md

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/67-game-director-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/68-game-designer-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 69
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
decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md
decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
decisions/D-008-cue-message-names-variant-proposed.md
decisions/D-009-review-next-pass-variant-aware-playtest.md
decisions/D-010-review-pass-2-build-clarity-now-room-3-content.md
decisions/D-011-variant-named-messages-accepted.md
design/combat-cues-visual-spec.md
design/combat-step-44-walker-limit.md
design/combat-step-46-room3-cap.md
design/combat-step59.md
design/combat-step68.md
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
goals/G-001-combat-monotony/37-studio-to-game-designer.md
goals/G-001-combat-monotony/38-game-designer-to-studio.md
goals/G-001-combat-monotony/39-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/40-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/41-studio-to-qa.md
goals/G-001-combat-monotony/42-studio-to-game-designer.md
goals/G-001-combat-monotony/43-qa-to-studio.md
goals/G-001-combat-monotony/44-game-designer-to-studio.md
goals/G-001-combat-monotony/45-studio-to-game-designer.md
goals/G-001-combat-monotony/46-game-designer-to-studio.md
goals/G-001-combat-monotony/47-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/48-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/49-studio-to-qa.md
goals/G-001-combat-monotony/50-qa-to-studio.md
goals/G-001-combat-monotony/51-studio-to-playtester.md
goals/G-001-combat-monotony/52-studio-to-game-designer.md
goals/G-001-combat-monotony/53-playtester-to-studio.md
goals/G-001-combat-monotony/54-game-designer-to-studio.md
goals/G-001-combat-monotony/55-studio-to-qa.md
goals/G-001-combat-monotony/56-qa-to-studio.md
goals/G-001-combat-monotony/57-studio-to-game-director.md
goals/G-001-combat-monotony/58-studio-to-game-designer.md
goals/G-001-combat-monotony/59-game-designer-to-studio.md
goals/G-001-combat-monotony/60-game-director-to-studio.md
goals/G-001-combat-monotony/61-studio-to-playtester.md
goals/G-001-combat-monotony/62-studio-to-qa.md
goals/G-001-combat-monotony/63-playtester-to-studio.md
goals/G-001-combat-monotony/64-qa-to-studio.md
goals/G-001-combat-monotony/65-studio-to-game-director.md
goals/G-001-combat-monotony/66-studio-to-game-designer.md
goals/G-001-combat-monotony/67-game-director-to-studio.md
goals/G-001-combat-monotony/68-game-designer-to-studio.md
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
decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md — D-005: A contact blocked by invulnerability consumes the shot and spends the lunge's hit; simultaneous cue starts outside rooms 4–5 are accepted
decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md — D-006: Criterion 13's walker limit in rooms 3–5 is 3–7 hearts, with at least 2 rooms cleared; no room or enemy parameter changes
decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md — D-007: Simultaneous cue starts in room 3 after a cap delay stay accepted; criterion 11 is reworded to the real in-flight bound
decisions/D-008-cue-message-names-variant-proposed.md — D-008: Text-view wind-up message names the variant (proposed build change); no swipe-timing rule change
decisions/D-009-review-next-pass-variant-aware-playtest.md — D-009: After build 0.6.1 the next pass is a variant-aware playtest, not a third Diagnose; no Owner escalation yet
decisions/D-010-review-pass-2-build-clarity-now-room-3-content.md — D-010: Review pass 2 — goal not met yet, no Owner escalation; build the variant message and manual text now; room 3 variety goes to Design
decisions/D-011-variant-named-messages-accepted.md — D-011: Text-view wind-up and hit messages name the variant (accepted); swipe timing stays a wording matter
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

- Observe: done (02; QA 16, 20, 32, 36, 56, 64). Contact-edge graze accepted (D-002, D-003). 30 FPS player view and late-swipe boundary closed: match the design and 60 FPS (64). No open defect.
- Diagnose: two passes done (04, 31); a third without progress is barred by the loop limit. Review (60, D-009) chose a variant-aware playtest instead.
- Decide: skipped. All options so far are inside D-001 and the pillars. Tentative (`game-director`, Owner escalation) per D-009 if Review pass 2 says the melee still reads as one fight.
- Design: complete (D-004 to D-007). Open, non-blocking (66): QA's room 3 in-flight question vs D-007, and whether D-008 (variant-named cue message, `proposed`) is ready to build. Manual late-swipe wording (59) not yet applied to `repo/manual.md`.
- Plan: skipped (approach local). Returns if the same criterion fails verification twice.
- Build: 0.6.1 done (48). A later Build is for the manual text and, if Design/Director take it, the D-008 message.
- Verify (QA): pass on 0.6.1 at 30 and 60 FPS (50, 64). Visual V1–V11 need a graphical build, a proposed new Goal at Close; V12 open.
- Play: three passes done (27, 53, 63). The variant-aware pass (63): rooms 4–5 varied and engaging; room 3 and the slow-run brute loop repetitive; brute/runner messages read "a grub". Scripted play only; a human check is not done.
- Review: pass 1 done (60): goal-not-met. Pass 2 open (65) with playtest 63 and QA 64.

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
| 11 | Decide (Owner escalation if the melee still reads as one fight, D-009) | game-director | prepare-owner-escalation | tentative (only if Review pass 2 says so) | — |
| 12a | Design (Options 1–2, manual wording) | game-designer | write-design-spec | done | 33-studio-to-game-designer.md (result: 35-game-designer-to-studio.md) |
| 12b | Observe (spitter fire times, rooms 3–4) | qa | reproduce-defect | done (no defect) | 34-studio-to-qa.md (result: 36-qa-to-studio.md) |
| 12c | Design (invulnerable contact, room 3 cue overlap) | game-designer | write-design-spec | done | 37-studio-to-game-designer.md (result: 38-game-designer-to-studio.md) |
| 13 | Build (build 0.6 per Design 35 and 38) | gameplay-engineer | implement-change | done | 39-studio-to-gameplay-engineer.md (result: 40-gameplay-engineer-to-studio.md) |
| 14a | Verify (0.6, 30 and 60 FPS) | qa | verify-change | done (fail: F2, F3, 13@60, room 3) | 41-studio-to-qa.md (result: 43-qa-to-studio.md) |
| 14b | Design (criterion 13 walker limit, 60 FPS) | game-designer | write-design-spec | done (D-006, no build change) | 42-studio-to-game-designer.md (result: 44-game-designer-to-studio.md) |
| 15 | Design (room 3 cap vs criterion 11) | game-designer | write-design-spec | done (D-007, accepted as built) | 45-studio-to-game-designer.md (result: 46-game-designer-to-studio.md) |
| 16 | Build (F2, F3 only) | gameplay-engineer | implement-change | done | 47-studio-to-gameplay-engineer.md (result: 48-gameplay-engineer-to-studio.md) |
| 17 | Verify (re-verify, incl. "not run" list, criterion 11 a–e) | qa | verify-change | done (pass) | 49-studio-to-qa.md (result: 50-qa-to-studio.md) |
| 18a | Play (fresh, hand-timed rooms 2–5) | playtester | playtest-session | done | 51-studio-to-playtester.md (report: 53-playtester-to-studio.md) |
| 18b | Design (criterion 11d wording, non-blocking) | game-designer | write-design-spec | done (no build change) | 52-studio-to-game-designer.md (result: 54-game-designer-to-studio.md) |
| 18c | Observe (late swipe vs lunge; hit with no cue; message wording) | qa | reproduce-defect | done (not a defect) | 55-studio-to-qa.md (result: 56-qa-to-studio.md) |
| 18d | Design (manual wording on late swipes; variant cue message) | game-designer | write-design-spec | done (manual text pending; D-008 proposed) | 58-studio-to-game-designer.md (result: 59-game-designer-to-studio.md) |
| 19 | Review (pass 1) | game-director | review-outcome | done (goal-not-met; D-009) | 57-studio-to-game-director.md (result: 60-game-director-to-studio.md) |
| 20a | Play (variant-aware, fresh, build 0.6.1 unchanged) | playtester | playtest-session | done | 61-studio-to-playtester.md (report: 63-playtester-to-studio.md) |
| 20b | Observe (30 FPS player view, late-swipe boundary) | qa | verify-change | done (no defect) | 62-studio-to-qa.md (result: 64-qa-to-studio.md) |
| 21a | Review (pass 2) | game-director | review-outcome | open | 65-studio-to-game-director.md |
| 21b | Design (room 3 in-flight vs D-007; D-008 readiness) | game-designer | write-design-spec | open (non-blocking) | 66-studio-to-game-designer.md |
| 22 | Build (manual late-swipe text from 59; D-008 message if ready) | gameplay-engineer | implement-change | tentative (after 21a and 21b; only if Review/Design call for it) | — |
| 23 | Verify (22) | qa | verify-change | tentative (only if 22 runs) | — |
| 24 | Next | studio | — | planned | — |

## Route changes

After 20a and 20b (63, 64): playtest shows rooms 4–5 varied, room 3 and brute loop repetitive, brute/runner messages read "a grub". QA closed the 30 FPS gaps with no defect. Opened Review pass 2 (65) and, in parallel, a non-blocking Design check (66: room 3 in-flight vs D-007; D-008 readiness). Build waits for both.

## Next action

Run in parallel: `game-director` with 65-studio-to-game-director.md and `game-designer` with 66-studio-to-game-designer.md (both address the result to `studio`). Then Route: if Review is goal-not-met and says the melee still reads as one fight, open the Owner escalation (11) per D-009 instead of a Diagnose. Otherwise decide Build 22 (manual text, D-008 message) from 66 and the Review, and Verify it; if goal-met, Close.

## Outcome

(open)
>>>END

<<<FILE @log-recent
## 048-route · 2026-10-16

Status: active. Open: 51-studio-to-playtester.md, 52-studio-to-game-designer.md.

After 17 (Verify, 50): pass at 30 and 60 FPS; F1–F3 fixed, no repeated failure. Unrun items left to the playtest. Opened Play 18a (51, fresh, no change or expected result) and, in parallel, a small Design step 18b (52) for the criterion 11d wording.

## 052-route · 2026-10-16

Status: active. Open: 55-studio-to-qa.md.

After 18a/18b (53, 54): 11d reworded, no build change. The playtest reports unfair-feeling swipe/lunge hits and one uncued hit, so QA Observe 18c (55) comes before Review. "Rooms feel alike" would be a third Diagnose pass, so it goes to `game-director` Review with the playtest and the QA result.

## 054-route · 2026-10-16

Status: active. Open: 58-studio-to-game-designer.md, 57-studio-to-game-director.md.

After 18c (56): not a defect; the late-swipe hits and the "no cue" hit match the design (a cue was printed). Opened Review (57) with playtest 53 and QA 56, since "rooms feel alike" would be a third Diagnose pass. In parallel, non-blocking Design 18d (58): manual wording on late swipes and the per-variant cue message.

## 057-route · 2026-10-16

Status: active. Open: 61-studio-to-playtester.md, 62-studio-to-qa.md.

After 18d and 19 (59, 60): Review is goal-not-met; per D-009 the next pass is a variant-aware playtest, not a third Diagnose. Opened Play 20a (61, build 0.6.1 unchanged) and QA 20b (62, 30 FPS gaps) in parallel. Manual text (59) and the D-008 message change wait until after the playtest so the played build stays steady.

## 060-route · 2026-10-16

Status: active. Open: 65-studio-to-game-director.md, 66-studio-to-game-designer.md.

After 20a and 20b (63, 64): playtest shows rooms 4–5 varied, room 3 and brute loop repetitive, brute/runner messages read "a grub". QA closed the 30 FPS gaps with no defect. Opened Review pass 2 (65) and, in parallel, a non-blocking Design check (66: room 3 in-flight vs D-007; D-008 readiness). Build waits for both.
>>>END

<<<FILE goals/G-001-combat-monotony/67-game-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 67
from: game-director
to: studio
stage: Route
outcome: goal-not-met
---
# 67: game-director → studio — Review pass 2 on build 0.6.1: goal not met yet, but the gap is narrow and inside D-001. No Owner escalation. Build the D-008 message and manual text now; Design gets a room 3 content question.

## Task

Route the Review result. Verdict: **goal-not-met**, moderate confidence. The remaining gap is design content inside D-001 and the pillars. The Owner escalation named in D-009 is **not** needed. Decision D-010 records this.

## Context

Goal G-001. Success condition: different situations call for noticeably different play (positioning, timing, attack, dash), and the player can tell why. Pass 1 (60, D-009) asked for a variant-aware playtest. It is done (63, build 0.6.1, scripted, six sessions, rooms 1–5), and QA (64) closed the 30 FPS gaps with no defect. I ran no `play` or `bots` this step.

## Findings

### Verdict

**Goal-not-met, with a much smaller gap than at pass 1.** The main suspicion in D-009 is mostly cleared: the differences the build was changed to create do show up when the player plays them separately. Two things keep me from calling the Goal met: one room is still flat for a long stretch, and the "can tell why" half is only partly met in the text view.

### Evidence that the intent is met

- **Enemies ask different things.**
  - Grub and runner: "step aside or swipe first". For the runner, the 0.35 s warning makes acting early matter more.
  - Brute: "step aside; a swipe will not stop it". The tester called it the first time a swipe cannot stop the warning.
  - Spitter: "cross or dash the aim line, or close in".
- **Rooms 4–5 hold attention.** Several asks overlap, the tester had to choose which to answer first, and attention stayed high through room 5. This is the strongest evidence for the Goal.
- **Readable threats.** Warnings always came before damage. QA 64 confirms the warnings, cue lines and messages match the design at 30 and 60 FPS, with no defect.
- **Cost of ignoring cues.** The fast run in room 2 lost to the brute because the script had no brute rule. That is the design working as intended, and it is not evidence of failure.

### Evidence that it is not met yet

- **Room 3 (spitters only).** The tester called it the most repetitive stretch: about 20 s of "aim, dash, shot lands behind me, again", with attention dropping. The single ask is the content gap. Only the tester's own choice of killing two spitters and leaving the third in a far corner made the standoff last that long, so part of it is script behaviour. It matches the cautious-play standoff in 53, and I treat it as real but not severe.
- **Room 1** offers one kind of ask. The tester rated this low impact, and it is a teaching room. I do not act on it.
- **Rooms 3 → 4 → 5** differ mostly in how many things overlap, not in what each thing asks (the tester's summary). Variety comes from overlap more than from distinct asks. That is acceptable under D-001, since depth is meant to come from positioning and enemy behaviour. It means variety outside rooms 4–5 is thin.
- **"Can tell why" is partly unmet.** The message line reads "a grub rears back" and "hit by a grub" for runner and brute, and only the `cue:` line names the enemy. The tester was confused by a brute hit that read as a grub hit. This is a clarity gap that D-008 already proposes to fix.

### D-009 escalation condition: not triggered

The condition was that the melee enemies still read as one answer, with runner, standard grub and brute not told apart, or the brute only kited.
- The brute **was** told apart from the grub and runner.
- The runner and the standard grub share an answer, but they differ in time pressure. That was designed (D-008 says so).
- The brute loop in the slow room 2 run (about 8–27 s, six or seven dodges, never punished in the recovery) was partly caused by the tester's rules. The tester said so, and their rules never hit the brute in its recovery window. This is the D-004 trigger "human dodges the brute without fighting it". It is not confirmed on scripted evidence, so Option 3 (a spitter in room 2) stays deferred.

So there is no Owner question. A new melee behaviour or enemy type, healing, or an input change is not needed on this evidence.

### Confidence and limits

- Confidence in "not met, narrow gap": moderate. Confidence that no Owner decision is needed now: fairly high.
- All play was scripted. The tester could not feel the pad, reaction rules ran on a 0.15 s grid, and three outputs were cut at about 19–27 s. The 30 FPS run was room 3 only, with no frame-rate difference seen (QA 64 covers it).
- A human check would add what scripts cannot: whether room 3 and the brute loop feel flat to a person, whether a person understands the brute's no-flinch rule without the manual, and whether the shot clutter in rooms 4–5 feels unfair (the tester expected some hits would). I recommend one short live check after Build 21, as the closing evidence, not as a new Diagnose.

## Next issues

1. **Room 3 has a single ask** (inside G-001, Design). Ask `game-designer` for room-content options inside D-001, using existing enemies only. Room 3 should offer a second kind of ask, or avoid a long standoff against one cornered spitter, without breaking criterion 11 or the room 3 cue timing that teaches the aim cue. This is design content. It is not an Owner choice.
2. **Variant names in the wind-up message and the manual late-swipe text** (clarity, "can tell why"). Build now, see below.
3. **Room 3 in-flight count vs D-007 (66, non-blocking).** I do not decide it here. The tester read room 3 volleys as readable and took no hit in the 26 s seen. QA's conflict is about which stated rule governs, and that is the Design call. If Design changes the room 3 cap or the cue rule, bundle it with issue 1 so one room 3 change is built and checked once.
4. **Brute loop and the "dodge without fighting" trigger (D-004).** Not confirmed. Watch it in the human check. Option 3 stays the first lever.
5. **Proposed new Goal at Close:** visual criteria V1–V11 need a graphical build, and V12 stays open.

I do not ask for another Diagnose. There is no new cause. The remaining questions are about content and wording, and a human check.

## Answer to question 3: build D-008 and the manual text now

Build 21 should carry the D-008 variant-named message (`a grub`, `a runner`, `a brute rears back`) and the manual late-swipe wording from 59. Reasons:
- D-009 item 5 kept the message out of the playtested build to keep the comparison fair. That playtest is done, so the reason to wait is gone.
- Clarity is half of the success condition ("the player can tell why"), and the tester hit it directly.
- The change is small, reuses the existing message system, and keeps the substring `rears back`, so reaction scripts still work. `game-designer` stays the owner of the wording and acceptance criteria (`design/combat-step59.md`).
- The message change should not wait for the room 3 Design answer. They can be built together if Design is ready in time. If not, ship the message and manual text first and Verify them, and do the room 3 change in a later build. The next playtest must state which build it used.

Treat D-008 as ready to build. Because D-008 is `proposed` and written by the Designer, the Studio should mark it accepted once Build 21 is routed (D-010 records that I do not object).

## Decisions already made

- D-001: one-button combat. Respected; nothing here needs a new input.
- D-004 to D-007: stand. D-007 is touched only by QA's non-blocking question (66), which is Design's call.
- D-008 (proposed): now cleared to build (see D-010).
- D-009: its escalation condition was checked and is not triggered. The "revisit when" items "cannot tell runner, standard grub and brute apart" and "stalls against the brute" are not reached on this evidence.
- New: **D-010** (this step).

## Constraints

- Stay inside D-001 and the pillars. A new enemy type, healing, or an input needs the Owner, and nothing here needs it.
- New issues become proposed Goals unless they serve "the player can tell why" or the room 3 variety gap named above.
- Evidence stays scripted until a human check is done. Weigh the next report that way.

## Open questions

For `studio` (routing):
1. Route Design for room 3 (issue 1), together with the existing 66 question.
2. Route Build 21 (message and manual text), then Verify (QA).
3. After Build 21, one playtest of the new build, ideally a live player or a hand-timed run, with room 3, the brute in room 2, and the brute hit message as checks. Then Review pass 3. If the melee reads as one fight in that pass, escalate per D-009; otherwise the Goal can be met or partially-met with the reasons stated.

## Expected output

The Studio routes Design (room 3), Build 21 and Verify, then a final playtest and Review pass 3. No Owner escalation is drafted: the trigger is not met.

## Sender assessment

Verdict confidence is moderate because the evidence is scripted. I weighed the playtester's own admissions that the room 2 brute loop and the fast-run deaths came from their rules. I counted the room 3 standoff as real because the same standoff was reported in 53, in a different script. I did not run the build.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/review-outcome.md
- Project: project.md#vision, goals/G-001-combat-monotony/goal.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-008-cue-message-names-variant-proposed.md, decisions/D-009-review-next-pass-variant-aware-playtest.md, decisions/D-010-review-pass-2-build-clarity-now-room-3-content.md
- Previous handoff: goals/G-001-combat-monotony/65-studio-to-game-director.md
>>>END

<<<FILE goals/G-001-combat-monotony/68-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 68
from: game-designer
to: studio
stage: Design
outcome: done
---
# 68: game-designer → studio — Room 3 conflict already resolved by D-007; D-008 completed and accepted as D-011, ready to build after Review

## Task

Answer the two Design questions from 66. This handoff gives the answers, the spec files changed, and what is ready to build once the Studio opens a Build after Review 65.

## Context

Goal G-001. Build 0.6.1 is unchanged. QA (64) raised a room 3 shots-in-flight question. Playtest 63 raised a clarity issue with the variant message. No rule, timing, room or hearts change is made here.

## Findings

### 1. Room 3 shots in flight: already resolved by D-007

- D-007 (accepted) and `design/combat-step-46-room3-cap.md` answer this.
- That note's amended criterion 11 states the bound: "The number of shots in flight never exceeds 2 plus the number of living spitters." Room 3 up to 5 is accepted when the cap delays several cues together. Rooms 4–5 never exceed 3.
- Where the note and `combat.md` differ on criterion 11 or the cap, the note governs.
- Answers to QA:
  - Simultaneous starts after a cap delay are still accepted (D-005 item 4, confirmed by D-007).
  - The bound that applies in room 3 is 5, not 3. The sentence "never more than 3 in rooms 1–5" is withdrawn.
  - QA's 4–5 `*` at 7.0–8.0 s is inside the bound. It is not a defect and not a reopen trigger.
  - The player took no hit from the volleys and answered them with "move aside". This fits the derivation in D-007.
- QA's first simultaneous start at 5.8 s follows a shot hit that freed a cap slot. That is a cap delay, so it does not trigger reopen item 3. If a later trace shows a simultaneous start in room 3 with no cap delay before it, that reopens D-007.
- QA's count of "4 or 5" from pictures is not the agreed method. Criterion 11d counts visible `*` plus `a spitter spits` events in the 0.3 s up to the picture time, and a count of 3–5 in room 3 passes.

**Leftover contradictions.** The spec files still contained two stale sentences, which is why QA read a conflict. They are now marked superseded in `design/combat-step68.md`, which lists them exactly:
- The `combat.md` cap paragraph says "In every real room … the count stays at 3 or fewer".
- The `repo/manual.md` spitter sentence says "no more than 3 are in the air at once".

The fixed manual wording is in that file. It is a manual-only change.

### 2. Other QA notes

- **Late-swipe wording (59) stands.** It is still not applied to `repo/manual.md`. The exact text is in `design/combat-step68.md` and meets the 59 acceptance list. It is ready to build with D-011.
- **Runner cancel vs kill.** No separate runner cancel rule is intended. A runner has 1 hp, so a swipe in reach kills it. That is recorded in the addendum. "Swipe cancels the wind-up" is only observable for the standard grub, and only the brute is the other flag value.

### 3. D-008: it was not quite complete, now completed and accepted

Gap found: D-008 named the wind-up messages but left the hit message `YOU ARE HIT by a grub` unchanged. That was the other half of playtest 63's confusion, since the tester was hit by a brute reported as "a grub".

Decision recorded as D-011 (accepted, supersedes D-008). It stays inside the "readable threats" pillar and D-001: no new input, no timing change, no new information that is not already in the `cue:` line, and no change to graphical presentation.

Strings (text build, wherever they are printed):

| Variant | Wind-up message | Hit message |
|---|---|---|
| Standard grub `g` | `a grub rears back` | `YOU ARE HIT by a grub` |
| Runner `r` | `a runner rears back` | `YOU ARE HIT by a runner` |
| Brute `G` | `a brute rears back` | `YOU ARE HIT by a brute` |
| Spitter shot | unchanged | `YOU ARE HIT by a shot` (unchanged) |

- The hit message keeps its current suffix (for example `— hearts n/3`), and the swipe, kill, shrug and spitter messages stay unchanged.
- The same strings apply in the player view and in any other text view that prints these messages. Nothing else is renamed.
- Only the noun after "by" or "a" changes.
- Compatibility: a rule `text "rears back"` still matches all three. A rule keyed on `a grub rears back` or `by a grub` now matches only standard grubs. Existing tests and bots that key on those strings are updated by the Build (test tooling).

Acceptance criteria (player-observable, at 30 and 60 FPS, practice room, one case per variant):
- **V-a.** A wind-up prints the variant's message once per wind-up, at the same moment as the current message (±1 frame).
- **V-b.** A hit by a grub, runner or brute prints the matching hit message on the frame of contact, with the same hearts text as today.
- **V-c.** In the same scripts, every other output line, including the `cue:` line, the `~` line, timings and hearts, is byte-identical to 0.6.1.
- **V-d.** `text "rears back"` reacts to all three variants as before.
- **V-e.** Criteria 1–11 and 17–21 of `combat.md` still hold, and the bot results do not change.

Experience signal (Review and playtest only): a player can say from the message line alone which kind of grub is attacking or hit them, and the room 5 brute hit is not called unexplained.

**Timing of the Build.** D-009 item 5 says a message change must not be mixed into a playtest pass without saying so. Open the Build only after Review 65. If Review requests another playtest of unchanged 0.6.1, hold the Build until after it. Otherwise state the new build number in the next playtest brief.

## Decisions already made

- D-005, D-007: unchanged. D-007 confirmed as the answer to question 1.
- D-008: superseded by D-011 (adds the hit message, accepts the change).
- D-009: unchanged.

## Constraints

- No new inputs, timings, room layouts or hearts.
- D-004 to D-007 are not reopened. The spec text did not truly contradict itself. Only two stale sentences did, and they are now marked superseded.

## Open questions

For the Studio and later steps:
1. Whether naming the variant helps or only moves a wasted dash elsewhere is for the next playtest (also open in D-008).
2. A human check of whether a room 3 burst is answerable is still the open playtest item from D-007.

## Expected output

The Studio reads this alongside Review 65. If the Review leads to a Build:
- Build D-011 (messages above, with V-a to V-e).
- Apply the manual text from `design/combat-step68.md` (late swipes, in-flight count). It is wording only.
- Verify at both frame rates.

No Build is requested yet.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat-step68.md, design/combat-step59.md, design/combat-step-46-room3-cap.md, design/combat.md, repo/manual.md
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md, decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md, decisions/D-009-review-next-pass-variant-aware-playtest.md, decisions/D-011-variant-named-messages-accepted.md
- Previous handoff: goals/G-001-combat-monotony/66-studio-to-game-designer.md
>>>END
