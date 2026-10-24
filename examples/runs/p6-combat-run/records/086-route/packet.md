# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/83-qa-to-studio.md, goals/G-001-combat-monotony/84-playtester-to-studio.md
next_seq: 85
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha cf0f0ee63752; run through the project's run commands)
log: last 5 of 33 entries in @log-recent; the full history is goals/G-001-combat-monotony/log.md

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/83-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/84-playtester-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 85
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
decisions/D-015-lunge-draws-and-shot-at-spawn-accepted.md
design/combat-visuals-verify-rulings.md
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
goals/G-001-combat-monotony/78-studio-to-art-director.md
goals/G-001-combat-monotony/79-studio-to-owner.md
goals/G-001-combat-monotony/80-art-director-to-studio.md
goals/G-001-combat-monotony/81-studio-to-playtester.md
goals/G-001-combat-monotony/82-studio-to-qa.md
goals/G-001-combat-monotony/83-qa-to-studio.md
goals/G-001-combat-monotony/84-playtester-to-studio.md
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
decisions/D-015-lunge-draws-and-shot-at-spawn-accepted.md — D-015: Accept lunge draws with the Strike-start hit word, and accept the spit shot sharing the spitter's cell at spawn
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

- Observe (playtester, qa): done (02, 08, 06, 15, 58, 70, 77). Still unobserved in play (suite only): distance-4 idle run, AC-3, 9 dodge, 10, 12, 28(c); real-room clear/heal/next room and "run complete" (AC-13, 14); `z/Z` glyphs; colour.
- Diagnose, Decide: done (03, 53; D-002, D-005, D-006, D-011). A4 (120° cone), D1 (facing mechanic) and D2 (room 1 composition) are held with revisit triggers in 59.
- Design: spec done (59, 60, 65, 73; D-011…D-015, AC-19…AC-30, V-9…V-18). Final V-15 manual wording is in 73 for the Owner. Optional designer edit (from 80): mirror the lunge-draw carve-out in AC-17 and rule 6, and the "after the knockback ends" reading of AC-28(b); not blocking.
- Plan: skipped (Waiting behavior local, per 67). Reopen with the Technical Director if a criterion fails verification a second time.
- Build: AC-19…AC-30 built (67, 75), D-014 rulings built. `test_line_words_match_the_next_draw` is weaker than AC-30(c) (77); a tightening is optional.
- Verify: 13f QA (77) no failing criterion at 30/60 FPS. 13g art-director (80): V-9…V-14, V-16, V-18 pass; lunge draws and shot at spawn accepted (D-015). Open: V-17 defeat and dash-off draws (13h QA captures), AC-15 suite run and V-15 text (Owner), V-6 colour and reverse-video cell (not checkable in a text view; a reinforcement only, so record as not checked unless the Owner has a colour build).
- Play: earlier sessions saw only rooms 1 and 2 by script (50, 54), with defeats. Rooms 3–5, the spitter, projectile hits, room clear, the dash and a survived run are unobserved, so monotony itself is unjudged. 14 is a fresh playtester, rooms 1–5, reactive short sessions, from the build and player profile only.
- Review: `game-director` with `review-outcome`, planned after Play. Open: run progression after "run over"; F1, F4, F6, F7; numbering of same-type enemies in one cell; A4, D1, D2.
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
| 10-O | Owner: place manual draft (59) and V-15 text | owner | — | open (final V-15 wording now in 73; asked again in 79) | 79-studio-to-owner.md |
| 11 | Plan | technical-director | technical-plan | skipped (Waiting behavior local, per 67; reopen if Verify disagrees) | — |
| 12 | Build (first attempt) | gameplay-engineer | implement-change | done (question: no repo files; Q1 gap) | 61-studio-to-gameplay-engineer.md |
| 12a | Design (Q1 knockback at distance 0, Q2, 3 passages) | game-designer | write-design-spec | done (D-013, AC-28) | 64-studio-to-game-designer.md |
| 12b | Build (re-issue with repo files) | gameplay-engineer | implement-change | done (AC-19…AC-28 built; suite re-run needed) | 66-studio-to-gameplay-engineer.md |
| 13a | Verify | qa | verify-change | done (fail: AC-17, AC-22 suite, AC-28b at 30, V-14/16; V-15 manual) | 70-qa-to-studio.md |
| 13b | Verify (visuals) | art-director | visual-review | done (question: no live view; V-15 fails on document) | 71-art-director-to-studio.md |
| 13c | Design (cell rule at .5, "on you", hit-line word) | game-designer | write-design-spec, make-decision | done (D-014, AC-29/30, V-18) | 73-game-designer-to-studio.md |
| 13d | Build (suite test, D-A, D-C, 13c rulings) | gameplay-engineer | implement-change | done (rulings built; 2 ManualTest need Owner run) | 75-gameplay-engineer-to-studio.md |
| 13e-O | Owner: run suite with manual.md (AC-15) | owner | — | open (parallel to 13h and 14) | 79-studio-to-owner.md |
| 13f | Verify (rerun; verbatim captures for AD) | qa | verify-change | done (pass: no failure; AC-15, V-15 open) | 76-studio-to-qa.md |
| 13g | Verify (visuals, from QA captures) | art-director | visual-review | done (pass; V-6, V-15, V-17 open; D-015) | 80-art-director-to-studio.md |
| 13h | Verify (V-17 defeat and dash-off captures) | qa | verify-change | open (parallel to 14) | 82-studio-to-qa.md |
| 13i | Verify (visuals, V-17 from 13h captures) | art-director | visual-review | tentative (only if 13h captures need a visual reading) | — |
| 14 | Play (rooms 1–5, fresh playtester) | playtester | playtest-session | open (parallel to 13h) | 81-studio-to-playtester.md |
| 15 | Review | game-director | review-outcome | planned | — |

## Route changes

After 13g (80): pass for everything assessable; D-015 accepts lunge draws and the shot at spawn. No Build, no TD re-plan, no escalation. Opened in parallel: 14 Play (81, fresh playtester, build and profile only) and 13h QA captures for V-17 (82). 13i is tentative. Colour (V-6) is recorded as not checked.

## Next action

- `playtester` runs 14 from `81-studio-to-playtester.md`, addressed to `studio`.
- `qa` runs 13h from `82-studio-to-qa.md`, addressed to `studio`.
- Owner (13e-O, 10-O, still open): see `79-studio-to-owner.md`: run the suite with `manual.md` beside `repo/`, report the count, and place the V-15 text from 73.
- Then Route after 14 and 13h: if 13h shows a V-17 failure, Build with the failure report. If 13h passes, run 13i only if a visual reading is needed. If Play shows design or experience issues, apply the return rules (Diagnose, or `game-director` for direction). Otherwise go to Review (15).

## Outcome

(Filled at Close.)
>>>END

<<<FILE @log-recent
## 075-route · 2026-10-16

Status: active. Open: 72-studio-to-game-designer.md.

After 13a/13b (70, 71): 13a failed (AC-17, AC-22 suite, AC-28b display at 30 FPS, V-10/14/16, V-15 manual); first failure of each, so no TD re-plan. Three spec gaps go to Design 13c (72) before Build. 13b was a question (AD could not run the build): not re-asked; visuals are reviewed after the rebuild from QA's captures. No escalation.

## 077-route · 2026-10-16

Status: active. Open: 74-studio-to-gameplay-engineer.md.

After 13c (73): done. The three spec gaps are ruled (D-014; AC-17, 28 changed, AC-29, 30 and V-18 new; V-10, 12, 14, 16 changed). No number, input or direction changes, so no Decide and no escalation. Build 13d opened (74), addressed back to `studio` so QA's step can be composed without the Sender assessment.

## 079-route · 2026-10-16

Status: active. Open: 76-studio-to-qa.md.

After 13d (75): done, fits the plan; no spec gap, no escalation. Verify 13f opened for `qa` (76), composed without the Sender assessment, both frame rates, with verbatim captures for the art-director. Owner step 13e-O (AC-15 with `manual.md`) runs in parallel, as the build environment lacked `manual.md`.

## 081-route · 2026-10-16

Status: active. Open: 78-studio-to-art-director.md.

After 13f (77): pass, no criterion failed, so no Build or TD re-plan. Opened 13g art-director (78) from QA's captures with the two QA observations, and re-asked the Owner for the AC-15 suite run and V-15 text (79). Designer clarification of AC-17 (Strike draws) stays optional, after 13g.

## 083-route · 2026-10-16

Status: active. Open: 82-studio-to-qa.md, 81-studio-to-playtester.md.

After 13g (80): pass for everything assessable; D-015 accepts lunge draws and the shot at spawn. No Build, no TD re-plan, no escalation. Opened in parallel: 14 Play (81, fresh playtester, build and profile only) and 13h QA captures for V-17 (82). 13i is tentative. Colour (V-6) is recorded as not checked.
>>>END

<<<FILE goals/G-001-combat-monotony/83-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 83
from: qa
to: studio
stage: Verify (V-17 defeat and dash-off draws, verbatim captures)
outcome: pass
---
# 83: qa → studio — V-17: both cases pass at 30 and 60 FPS; verbatim captures for the art-director

## Task

Report whether the build draws what V-17 requires in two cases, at 30 and 60 FPS:
1. A grub on the player's tile is defeated.
2. The player dashes off a tile with a grub on it.

Both cases could be set up with input scripts. Appendix A has the verbatim captures for the art-director.

## Context

G-001, Option A. Handoff 82 asked for the V-17 draws that the captures in 77 did not cover. I verified from the spec, the criteria and the build only, using `run_play` (`python3 play.py --view player {script}`). The results are the six runs of round 1. I did not change the repo, `manual.md` or the tests.

## Findings

### Verdict

| Case | 30 FPS | 60 FPS |
|---|---|---|
| 1. On-you grub defeated: the "grub defeated" draw has no entry and no displaced glyph | pass | pass |
| 2. Dash off the tile: the first draw after the dash has no entry and no displaced glyph | pass | pass |
| Colour, reverse-video cell | not assessable (text view) | not assessable |

No criterion failure was noticed in these runs.

### Case 1: on-you grub defeated

Script `defeat` (run at `fps 30` and `fps 60`):

```text
fps 30
room empty
player 8 4
spawn grub 8 4
0.2 attack
1.6 attack
end 2.6
```

- The first swipe at 0.2 s hits the grub (1 left). The grub is shown right of `P`, with the entry `on you: … (shown right)`.
- The grub then winds up, hits the player once (1.333 / 1.317), and goes to Recovery.
- At 1.450 the line reads "the grub is open (on you)". The 1.47/1.45 and 1.50 draws both carry `on you: w open (shown right)` with `Pw`. This is the draw just before the defeat.
- The grub stays in Recovery from 1.45 s until about 2.35 s, so it is stationary at the second swipe (1.6). It is still on you then; I did not run a trace to confirm its true position.
- The second swipe at 1.600 prints "grub defeated". "room cleared" follows one tick later (1.633 at 30 FPS, 1.617 at 60).
- **The draw that prints "grub defeated"** is [1.63 s] at 30 FPS and [1.62 s] at 60 FPS. It shows only `P)` and the arc. It has:
  - no `w` anywhere on the map,
  - no `on you:` line,
  - no displaced glyph.
- The next draw ([2.00 s]) and the final draw ([2.50 s]) show `P` alone, with no `on you:` line.
- Both rates are identical in text apart from the draw times (1.63 / 1.62).
- V-17: pass.
- The lines also agree with V-10 and V-18. The "(on you)" lines in this run all have an entry in the same draw. The defeat line carries no position word, as specified.

Limit: this was the last enemy, so "room cleared" printed too. A defeat with another enemy still on the tile was not run.

### Case 2: dash off the tile

Script `dashA` (grub winding up when the player dashes; `fps 30` and `fps 60`):

```text
fps 30
room empty
player 8 4
spawn grub 8 4
0.3 dash up
end 1.5
```

- The draw before the dash is [0.03 s] / [0.02 s]. It shows `PG` and `on you: G biting soon (shown right)`.
- "you dash up" prints at 0.300. **No draw is made at the dash itself**, because dash is not an event in principle 4.
- **The first draw after the dash** is [0.50 s]. It shows `P` at row 1 (mid-dash) and `G` alone at row 4 below, with no `on you:` line and no displaced glyph. It is identical at both rates.
- The grub finishes its strike toward where the player stood. The player takes no heart damage (hearts 3/3).
- "the grub is open (below)" prints at 0.683 / 0.667. The draw at [0.70 s] / [0.67 s] shows `P` at row 0 and `g` at row 3, and the word "below" matches the picture.
- V-17: pass at both rates.

Script `dashB` (grub in Recovery on the tile after a first hit, then dash; `fps 30` and `fps 60`):

```text
fps 30
room empty
player 8 4
spawn grub 8 4
0.2 attack
1.6 dash left
end 2.6
```

- The draw just before the dash is [1.50 s], with `Pw` and `on you: w open (shown right)`.
- "you dash left" prints at 1.600, again with no draw at that moment.
- **The first draw after the dash** is [2.00 s]. It shows `P` at column 4 and `w` alone at column 8, with no `on you:` line and no displaced glyph. The grub is in its own cell, no longer beside `P`.
- The draw at [2.50 s] is the same.
- No hit line, so no heart is lost (the player is invulnerable during the dash). The results are identical at both rates.
- V-17: pass at both rates.

### Observations (not failures)

1. **No draw at the dash.**
   - `combat-visuals.md` ("When the enemy leaves or dies") says the on-you line updates "in the same draw as … the player's dash". Principle 4 lists no dash draw, so the first draw after the dash is up to 0.5 s later: 0.2 s after the dash starts in `dashA`, and 0.4 s in `dashB`.
   - No draw shows a stale entry, so V-17 as written holds.
   - If the art-director wants the clearing to be visible at the moment of the dash, that would be a new draw event, which V-16 forbids without a spec change. This is for the art-director and game-designer to decide.
2. **`dashA` mid-dash draw.** The 0.50 s draw shows the player mid-dash (row 1), not at the dash end. It is still a valid "after" draw: the player is more than 0.5 tile from the grub, and the grub's `G` sits in its own cell.
3. Not run this round: the test suite. 77 stands (71 passed, 2 `ManualTest` errors from the missing `manual.md`, which is an environment matter for the Owner's AC-15 run). No other criterion was re-checked beyond what these runs showed.

### Scripts to re-run

Put each script in a file and run `python3 play.py --view player <file>`.

- Defeat: `fps 30` or `fps 60` as above, with the `defeat` lines.
- Dash with grub winding up: `dashA`, same lines with `fps 30` or `fps 60`.
- Dash with grub open: `dashB`, same lines with `fps 30` or `fps 60`.

## Decisions already made

- D-011, D-012, D-013, D-014, D-015 (applied as written).

## Constraints

- No change to the repo, `manual.md` or the tests. Colour and the reverse-video cell are not claimed either way.

## Open questions

1. **To the art-director:** read Appendix A. Does the lack of a draw at the dash (observation 1) read acceptably?
2. **To the Owner:** the suite run with `manual.md` (AC-15) and the V-15 text, as in 77.

## Expected output

The Studio forwards Appendix A to the art-director. With the Owner steps from 77, V-17 is now covered at both rates.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat-visuals.md, design/combat-visuals-verify-rulings.md, design/combat.md, manual.md, repo/
- Decisions: decisions/D-012-on-you-line-for-displaced-enemies.md, decisions/D-014-one-rule-for-cells-on-you-and-hit-line-word.md, decisions/D-015-lunge-draws-and-shot-at-spawn-accepted.md
- Previous handoff: goals/G-001-combat-monotony/82-studio-to-qa.md

---

# Appendix A — verbatim captures (`python3 play.py --view player`)

For `defeat` and `dashB` the output is the full run from the first hit onward. The earlier part (0 to 1.45 s) is the same as A1 in handoff 77 and is cut here. `dashA` is complete.

## A1. Case 1, `defeat`, 30 FPS (from the "open" line before the defeat to the end)

```text
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
  1.600  grub defeated
  1.633  room cleared
   [1.63 s] hearts 2/3
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
   [2.00 s] hearts 2/3
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
   [2.50 s] hearts 2/3
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
end at 2.60 s: hearts 2/3, enemies left 0
```

## A2. Case 1, `defeat`, 60 FPS

```text
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
  1.600  grub defeated
  1.617  room cleared
   [1.62 s] hearts 2/3
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
   [2.00 s] hearts 2/3
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
   [2.50 s] hearts 2/3
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
end at 2.60 s: hearts 2/3, enemies left 0
```

## A3. Case 2, `dashA`, 30 FPS (complete)

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
  0.300  you dash up
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |        P       |
   |                |
   |                |
   |        G       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.683  the grub is open (below)
   [0.70 s] hearts 3/3
   +----------------+
   |        P       |
   |                |
   |                |
   |        g       |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |        P       |
   |                |
   |                |
   |        g       |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
   +----------------+
   |        P       |
   |                |
   |                |
   |        g       |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 1.50 s: hearts 3/3, enemies left 1
```

## A4. Case 2, `dashA`, 60 FPS (complete)

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
  0.300  you dash up
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |        P       |
   |                |
   |                |
   |        G       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.667  the grub is open (below)
   [0.67 s] hearts 3/3
   +----------------+
   |        P       |
   |                |
   |                |
   |        g       |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |        P       |
   |                |
   |                |
   |        g       |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
   +----------------+
   |        P       |
   |                |
   |                |
   |        g       |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 1.50 s: hearts 3/3, enemies left 1
```

## A5. Case 2, `dashB`, 30 FPS (from the "open" line before the dash to the end)

```text
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
  1.600  you dash left
   [2.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |    P   w       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |    P   w       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.60 s: hearts 2/3, enemies left 1
```

## A6. Case 2, `dashB`, 60 FPS

```text
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
  1.600  you dash left
   [2.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |    P   w       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |    P   w       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.60 s: hearts 2/3, enemies left 1
```
>>>END

<<<FILE goals/G-001-combat-monotony/84-playtester-to-studio.md
---
kind: handoff
goal: G-001
seq: 84
from: playtester
to: studio
stage: Review of play observations (rooms 1–5)
outcome: done
---
# 84: playtester → studio — Observation report: three room-1 sessions, never got past room 1

## Task

Report what a player experiences in the build, with the scripts used, so the Studio can route experience issues to game-designer and defects to qa.

## Context

The Studio asked for a player-view playthrough of rooms 1 to 5 with attention on combat (handoff 81). I played through input scripts with `python3 play.py --view player {script}`, three sessions, all in room 1. I had no history of the build and did not read source, tests or design documents. The play budget ended after three sessions (0 rounds left). **I never cleared room 1, never reached rooms 2 to 5, and never saw a spitter.** Every session ended in defeat in room 1; one session (s1) and one (s2) auto-restarted into a second run that also ended in defeat.

Method: input automation. Each script was written blind, with fixed times, from the previous output. I could not react in real time within a session, which limits how well I could dodge. Text frames only; I could not see color, hear sound or feel controller input.

## Findings

### Scripts used (re-runnable)

- **s1-room1-probe**: `room 1`, fps 30, end 15; swipes at 0.5, 2.5, 3, 5.5, 8, 10; move left at 1, stop 2; move right at 4, stop 5; dash right at 7.
- **s2-room1-hold**: `room 1`, fps 30, end 14; swipes at 1.0, 1.8, 2.6, 3.4, 4.2, 5.0, 5.8, 6.6, 7.4, 8.2; dash left at 2.0, dash right at 4.0.
- **s3-room1-dash-on-cue**: `room 1`, fps 30, end 12; dash down at 1.55 (just after a "rears back" cue), move up at 2.2, stop 2.3; swipes at 2.4, 3.0, 4.2, 4.8, 5.4, 6.0; dash left at 3.6.

Exact script text is in the run results for each session.

### The room and the enemies

Room 1 starts with three grubs (top centre, left, right edge) that drift toward you. Only grubs seen. Start is x 8, y 4.

### Session outcomes

- **s1**: Defeated at ~4.0 s in run 1 (rooms cleared 0). The restarted run was defeated at ~11.9 s. I hit a grub once in the first run and never defeated one.
- **s2**: Defeated at ~3.9 s, and again at ~10.5 s in the second run. Two grubs hit once; none defeated.
- **s3**: Defeated at ~7.4 s. This was my best attempt: my one dash on cue avoided a bite entirely (hearts stayed 3/3 until 5.4 s), and I got one grub defeated at 6.0 s. Then two grubs bit me in turn at 5.4, 6.4 and 7.4 s.

### What I saw and felt

1. **Grubs bite in a predictable rhythm.** Each grub shows "rears back" and then bites about 0.5 s later (e.g. 1.30 rear, 1.83 hit; 9.40 rear, 9.97 hit). The cue is readable (`G`), but the gap is short.
2. **Getting hit leaves me stunned right when I want to counter.** Several swipes returned "(stunned)" (3.0 s in s1; 10.0 s in s1; 5.4 s in s3). The grub then becomes "open" within about 0.1 s, but I cannot use that opening because I am stunned. This felt unfair: the opening arrives after I was hit, not because I dodged.
3. **Being surrounded is lethal and fast.** In every session two or three grubs ended up on or beside me, and bites chained one after another (e.g. s1 3.0, 3.97; s2 1.97, 2.97, 3.93). Once flanked I lost a heart roughly every second and never found a way out. Hearts went 3 to 0 in about 2 seconds of contact.
4. **My swipes mostly missed.** Messages: "(miss) too far" (s2 1.0 s, 7.4 s), "(miss) not in front" (s2 1.8 s, 8.2 s; s3 4.8 s). Reach is a bit over one tile and facing matters. Because I script blind, I often faced the wrong way. A player with live control would likely do better, so I do not count this as a build defect.
5. **Dash works as described.** In s3 dashing down at the rears-back cue avoided the bite completely and cost nothing. That was the only time a fight felt skillful. Dash on cooldown ("dash not ready") never appeared, but I only dashed twice per run.
6. **A swipe's cone hits several enemies and hits seem to need "open" timing.** In s3, swiping at 3.0 s hit a grub as it rose. Hits on an `open` grub felt rewarding but I got few chances.
7. **The fights all felt the same.** Every encounter was: grubs close in, one rears back, I dash or take a hit, another rears back. I met no second enemy type, so I cannot say whether later rooms vary. Within room 1 the three grubs behave identically, and the only decision was "when to dash". I never needed spacing or positioning beyond that, and moving away from grubs did not seem to shake them, as they kept pace.
8. **Dying and restarting is quick**, about 2 s from "run over" to a new run when my script kept pressing attack. That suits short runs.

### Confusion

- "(miss) too far" versus "(miss) not in front" are clear once you know them, but nothing on screen told me my facing. I could not see which way `P` was facing.
- The "on you:" lines (e.g. "g open (shown left)") are hard to read when a grub shares my tile; the drawn position is only an approximation.
- The manual says "you can move while you swipe" and "hits every enemy inside it", but my swipes rarely hit more than one, so I could not confirm the multi-hit.

### Impact ranking

- High: flanked-by-grubs deaths within a few seconds, and being stunned during the open window. Together these made room 1 feel punishing for a first room.
- Medium: sameness of fights; one clear answer (dash on cue).
- Low: no facing indicator.

### Positives

- Clear telegraph letters (`g` vs `G`) and the text cue "rears back".
- Dash i-frames work and feel good when timed.
- Fast restart.

## Decisions already made

None. I decide nothing about the game.

## Constraints

- Observations come from three scripted sessions in room 1 only. Repeats across sessions: flanking deaths, stun-after-hit, fights feeling uniform (all three). Single-session only: the successful dash dodge and the grub defeat (s3).
- Could not observe: rooms 2 to 5, spitters, clearing a room or the heal, "run complete", color, sound, controller feel, real-time reaction.

## Open questions

- Does any later room change how fights feel? Not answered, because I never got past room 1.
- Is room 1 meant to be this hard for a first-time player? A live human or a longer-budget playtest should check, ideally with scripts that react to each cue.

## Expected output

The Studio reads this report, routes experience issues (flanking lethality, stun while the open window is live, sameness of fights) to `game-designer`, and sends no defects to `qa` unless it judges the facing indicator or the "on you" display a defect. A further playtest should try for rooms 2 to 5.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, manual.md, the build in repo/ (player view only)
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/81-studio-to-playtester.md
>>>END
