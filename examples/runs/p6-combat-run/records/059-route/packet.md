# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/53-game-designer-to-studio.md, goals/G-001-combat-monotony/54-playtester-to-studio.md
next_seq: 55
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha 097ad2a377c5; run through the project's run commands)
log: last 5 of 22 entries in @log-recent; the full history is goals/G-001-combat-monotony/log.md

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/53-game-designer-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/54-playtester-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 55
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

- Observe (playtester, qa): done (02, 08, 06, 15).
- Diagnose, Decide: first pass done (03; D-002, D-005, D-006): single-state, untelegraphed enemy behavior; Option A. Diagnose re-entered once (51) on Play findings from room 1: harsh opener (3 grubs, stun on hit), unclear swipe "(miss)" on a rearing or biting grub, facing only by moving, unclear dash end point. Findings came from scripted play, so timings need checking with trace and bots.
- Design: done (10, 16, 33, 45). Spec `design/combat.md` (AC-1…AC-18), D-003, D-006, `design/combat-visuals.md` (V-1…V-8), D-009 (test ruling).
- Plan: done (14, D-004). Gap defaults F1–F11; the designer confirms them at Review, F1 (grub speed) matters most.
- Build: done (18, 22, 23, 35, 47; manual paragraph placed by the Owner, D-007). F2 is cosmetic. Pause (F11) not implemented.
- Verify: done. Behavior 7g (39) passed, AC-17 and AC-18 hold. AC-15 passes (D-010, 40/40).
- Verify, visuals: done (44). V-4 `z/Z` and V-6 from code only. V-7 (two spitters, room 4) not observed. F4 optional polish, left for Review.
- Play: first session (50) saw room 1 only, by scripts, two defeats. Rooms 2–5, the spitter, projectile hits, room clear are still unobserved. Second Play session (52) is open for them, with a fresh playtester.
- Review: `game-director` with `review-outcome`. Planned, after Diagnose and the second Play. Open: run progression after "run over"; F1, F4, F6, F7; numbering of same-type enemies in one cell; a still player going down in about 5 s.
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
| 9a | Diagnose (Play findings) | game-designer | diagnose-experience | open | 51-studio-to-game-designer.md |
| 9b | Play (parts not yet seen) | playtester | playtest-session | open | 52-studio-to-playtester.md |
| 10 | Review | game-director | review-outcome | planned | — |

## Route changes

After Play (50): the report covers room 1 only (scripted, two defeats) and shows experience issues, not defects. Diagnose re-opens (9a, 51) per the Play return rule. A second Play (9b, 52, fresh playtester) opens in parallel for the unseen rooms. Review waits for both.

## Next action

- `game-designer` starts 9a from `51-studio-to-game-designer.md`; the result is addressed to `studio` (`53-game-designer-to-studio.md`).
- In parallel, `playtester` starts 9b from `52-studio-to-playtester.md` in a fresh executor context; the result is addressed to `studio` (`54-playtester-to-studio.md`).
- Then Route: a direction or scope question goes to Decide (`game-director`), a spec change to Design, defects to Observe (`qa`); otherwise Review.

## Outcome

(Filled at Close.)
>>>END

<<<FILE @log-recent
## 047-resume · 2026-10-15

Status: active. Open: 41-studio-to-art-director.md, 43-studio-to-game-designer.md.

After the Owner chose A (42, D-008): the suite ran 39/40; `ManualTest` fails on the phrase `run over` missing from `manual.md`. Goal back to `active`. 7j opens (43): the designer rules on manual vs. test. 7k, 7k-O and 7l are tentative on that ruling. 7h continues; Play waits for AC-15.

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
>>>END

<<<FILE goals/G-001-combat-monotony/53-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 53
from: game-designer
to: studio
stage: Route
outcome: done
---
# 53: game-designer → studio: Diagnosis of the room-1 play findings (handoff 51)

## Task

Route the options below by authority. `game-director` needs to decide the two items in group D, and the Studio should schedule one cheap re-check (see Expected output). The spec is not edited in this step.

## Context

G-001 (combat monotony), Option A (D-002). The playtester (50) went down twice in room 1 and saw nothing past it. This is my diagnosis from the report, the spec (`design/combat.md`, `design/combat-visuals.md`), `manual.md` and two runs.

**What I could and could not check.** I had no `run_trace` and no usable bot run.
- The `run_bots` round failed: `script line 1: cannot read 'room 1'`. The bots script format is not the play-script format, and no rounds are left. There is therefore **no passive-bot or active-bot reference**.
- I used two `run_play` scripts instead: a still player in room 1 (`room1-still`) and a one-grub probe in the practice room (`wind-up-swipe`).
- Everything about "how a competent player fares" is reasoning, not measurement.

## Findings

### 1. What the runs show

**Still player, room 1** (60 FPS). Hearts are lost at 1.93, 3.43 and 4.95 s, and the player goes down at 4.95 s.
- This matches the spec note "idle player down at about 5 s".
- The bites are 1.5 s apart. Several strikes (about 2.4–2.5 s, 4.0–4.2 s) fall inside the 0.8 s post-hit invulnerability and are absorbed.
- Wind-ups overlap as the report says: 2.883 and 2.933 s, and 3.53 s (left) overlapping the "above" grub's strike. Never more than 2 are committed at once, so the attack limit (AC-6) holds.
- All three grubs arrive within about 1.5 s of each other (rear-backs at 1.38, 1.88 and 2.88 s) because they start about the same distance away. That is why room 1 produces simultaneous threats.

**Swipe on a rearing grub** (practice room, one grub). A swipe 0.27 s into a wind-up (1.05 s):
- prints "grub hit (1 left)" and "the grub is open";
- the glyph drops from `G` to `w`;
- no heart is lost to that bite (AC-5 interrupt works).

The grub is **hittable during wind-up**. The tester's guess in 50 ("probably not hittable") is wrong, and the manual never says so.

**The "(miss)" results.** In my probe the two misses (1.5 s, 2.0 s) happened because the first hit knocked the grub back 1 tile. It stood about 2 tiles away, outside the 1.5-tile reach. "(miss)" was truthful.
- The tester's misses at 2.1 s and 4.0 s may be the same effect, or a facing error, or a swipe during Strike.
- My probe did **not** test a swipe during Strike or an adjacent Recovery. That case is unsettled.

### 2. Classification of the findings

| Finding | Spec-conforming? | Class |
|---|---|---|
| Loop is identical in room 1 | Yes. Room 1 is a teaching room (D-003) | Open: see §3 |
| Simultaneous rear-backs (0.03–0.05 s apart) | Yes. The limit is 2 at once, with no spacing rule | **Tuning / rule gap** |
| 3 hearts gone fast | Yes. The bites are at least 1.5 s apart for a still player, and 0.8 s apart after invulnerability for a moving one | **Tuning** (stacks with the rows above and below) |
| Stun 0.3 s blocks the counter | Yes, spec text | **Tuning** (sharpest complaint) |
| Swipe hits a winding-up grub; the tester thought it can't | The spec is fine, the manual is silent | **Manual** |
| Swipe "(miss)" next to a grub | Probably knockback or facing; "(miss)" is truthful | **Readability** (cause not fully settled) |
| Cannot turn without moving; swipes hit air after a dash | Yes. Facing is move-only | **Direction** (D-001 / facing) |
| Dash end point unclear; felt like 2–3 tiles | Spec says 4 tiles | **Unknown**: possible as-built difference or wall clamp. Needs `run_trace`. The manual gives no distance |
| Grub "on you" drawn beside `P` | Yes (D-006) | **Display / readability** |

### 3. Causes (design terms)

1. **No spacing between grub commitments.** The spec limits grubs to 2 in Wind-up/Strike but sets no minimum gap between wind-up starts. Three grubs with equal start distance converge together, so one safe response (step or dash) covers one grub. The 0.8 s invulnerability absorbs some bites but not enough to make this read as skill.
2. **Stun 0.3 s overlaps the counter window.** The best answer to a wind-up is to hit the grub in it (interrupt), but hit-stun removes that answer right after a hit. The wind-up is 0.5 s, so a 0.3 s stun leaves about 0.2 s. This explains the "unfair" feeling in 50.
3. **The best tools are not taught.** The manual says "step away or dash" for a wind-up and does not mention the interrupt, the knockback after a hit (grub ends about 2 tiles away, out of reach), or the dash distance. The tester therefore concluded the grub is unhittable.
4. **Facing is move-only, with unspecified edge cases.** Two spec gaps:
   - The spec does not say whether a dash changes facing.
   - The spec does not say whether an enemy at distance about 0 (a grub "on you") is inside the 90° cone, since it has no direction.

   Both feed the "I couldn't hit what was next to me" feeling.
5. **Monotony vs harshness.** In ~10 s of play every grub did the same loop. That is expected in a teaching room and does not show that monotony is solved or still present, because the tester died before any variation (rooms 2–5, spitter). Harshness is now masking the question. Only a survived run (52) can answer it.

### 4. Options

**A. Mine: rules and tuning (game-designer authority; changes the spec in the next step)**

- **A1. Wind-up spacing.** A grub may not start a Wind-up within 0.5 s of another grub's Wind-up start. This reuses the spitter stagger idea.
  - Addresses: pressure, simultaneous rear-backs.
  - Cost: a small rule. It must hold at 30 and 60 FPS (use seconds).
  - Risk: cluster fights become longer. It does not change the single-grub cycle.
  - Fit: pillar 3. No D-001 effect.
- **A2. Shorter stun.** 0.3 s → 0.15 s **[tune]**, or keep 0.3 s but let the swipe buffer and fire when the stun ends.
  - Addresses: the "can't hit back" frustration.
  - Risk: low. The invulnerability time is unchanged.
- **A3. Body hit rule.** An enemy within about 0.5 tile of the player (the "on you" case) is always hit by a swipe, regardless of facing.
  - Addresses: "on you" confusion and part of the facing complaint.
  - It does not change how the player turns.
- **A4. Cone width.** 90° → about 120° **[tune]** for more forgiveness.
  - Cost: low. Risk: it weakens positioning, so try it only if A3 is not enough.
- **A5. Spec gaps to close either way:** whether a dash changes facing, and the exact distance-0 swipe rule if A3 is not taken.

**B. Manual and clarity (no rule change; the Studio decides who edits `manual.md`)**

- State that a swipe during a rear-back cancels the bite (the best counter).
- State that a first hit knocks the grub back about a tile, so a follow-up may need a step forward.
- State the dash distance (about 4 tiles) and that a hit stuns for a moment.
- Add "(too far)" or similar wording to "(miss)" for a swipe when an enemy is within about 2.5 tiles. This is a display text matter.

**C. Art-director (display)**

- "On you" readability. Suggestion: the text line could name where the glyph is drawn ("open, on you, drawn right"), or the displaced glyph could be marked. This does not change D-006.
- Review whether "YOU ARE HIT by a grub" should say which grub (left or above).

**D. Needs `game-director` (not mine to choose)**

- **D1. Facing.** The tester's request ("turn without moving" or "swipe behind you") conflicts with D-001 for a new input. Variants that change the facing mechanic are all direction decisions:
  - Auto-face the nearest enemy on swipe.
  - A dash that keeps facing (a "backstep").
  - A 360° swipe.
  
  I recommend trying A3 and A4 first and escalating this only if the tester still reports it.
- **D2. Room 1 composition.** Options:
  - Fewer grubs. This breaks the spec's "3–6 enemies per room".
  - Uneven grub start distances. This is the "staggered arrival" that D-002 defers as part of Option B.
  
  A1 reaches a similar effect inside Option A, so I do not need either of these now.

### 5. Trade-offs in short

- A1 + A2 + A3 are cheap and keep the Option A reading (one telegraph, one answer). They may leave a still player's time-to-down near 5 s, which is fine because that is a reference value, not a target.
- B is nearly free and should happen regardless. The tester's central confusion (unhittable while winding up) is a manual gap.
- D1 and D2 are bigger changes. Taking them before the cheap fixes would change scope or direction on one session of scripted play.

## Decisions already made

- D-001: one attack button plus dash. A turn-without-moving input is not allowed without the Owner.
- D-002: Option A first; B (including staggered arrival) deferred.
- D-003: room mix is across rooms; zero hearts ends the run; clear heals 1.
- D-006: enemies may overlap the player and are never hidden.

## Constraints

- Everything stays within D-001. All timings are in seconds and must hold at 30 and 60 FPS.
- This note contains design-side reasoning. Do not forward it to a Playtester unchanged; give them only what they need to play.

## Open questions

- **Dash distance.** Does the as-built dash go 4 tiles? The tester saw 2–3. Needs `run_trace` (QA or the engineer).
- **Swipe during Strike or an adjacent Recovery.** Does it hit? My probe did not test it.
- **Does a dash change facing?** The spec is silent.
- **Can a skilled player survive room 1?** I have no bot data (the bots script failed). The next run should find the bots script format first.
- **Monotony.** Is it still present once players survive? Waiting for 52 (rooms 2–5, spitter).

## Expected output

The Studio, in order:

1. Route group D to `game-director` only if wanted now. My recommendation is not to.
2. Send group B to whoever owns the manual, and group C to `art-director`.
3. Next step for me: a design-spec update with A1, A2, A3 and A5 (A4 held back). It must also state the new acceptance criteria and keep the 30/60 FPS requirement.
4. After that, one new playtest of room 1 and one bots round with a correct script format (a passive bot and a reactive bot), to see whether room 1 is survivable.

## Sender assessment

**Recommendation:** A1 + A2 + A3 together, plus B and C. Hold D until a retest.

- **Confidence in the causes:**
  - High: the lack of spacing (confirmed in the still run) and the manual gap on the interrupt (confirmed by the probe).
  - Medium: the stun as the main frustration. Only the tester's report supports it, and no live reaction data exists.
  - Low: the dash distance and "(miss)" next to a grub. Untested.
- The tester's own caveat applies: timed scripts, no live reaction. Some failures are likely timing errors.

## Load

- Role: none (Studio routing)
- Skills: none
- Project: design/combat.md, design/combat-visuals.md, manual.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-response-scope.md, decisions/D-006-overlap-display-and-practice-room-manual.md
- Previous handoff: goals/G-001-combat-monotony/51-studio-to-game-designer.md
>>>END

<<<FILE goals/G-001-combat-monotony/54-playtester-to-studio.md
---
kind: handoff
goal: G-001
seq: 54
from: playtester
to: studio
stage: Play
outcome: done
---
# 54: playtester → studio — Observation report: room 2 by script, little else reached

## Task

Report what a first-time player experienced in the later rooms and with enemies other than the first room's grub, paying attention to combat.

## Context

Handoff 52 asked for a play session over the unseen parts of the game. I played by input script only (`python3 play.py --view player {script}`, using only the manual). Live play was not available. I used one scripted run. It was a blind script, so I could not react to the screen mid-run. The result is thin, and I say below what I did not see.

## Findings

### Method

- One scripted run: `room 2`, 30 fps, 20 s. The script was a swipe at 1 s, move right at 3 s, stop at 5 s, swipe at 5.5 s, dash left at 8 s, swipe at 10 s.
- I chose the moves in advance from the manual, so nothing was adjusted to what was on screen.
- I did not use the remaining run rounds. This report rests on that single run.

### What I saw and did not see

- **Seen:** the opening of room 2. It had four grubs, all `g`, placed around the edges. They drifted toward me from all sides and ended up around my tile.
- **Seen by accident:** room 1 again. My swipe at 10 s came after I went down, and "press attack to start again" restarted the run in room 1. It had three grubs. I did nothing there but stand still, and I went down at 14.97 s.
- **Not seen:**
  - rooms 3, 4 and 5 (I never cleared a room, "rooms cleared: 0" both times);
  - any spitter, so no `S`/`Z` charge, no `*` shot, and no "staggered";
  - a "room cleared" heal;
  - "run complete".
- **Never exercised:** the dash. It fired at 8 s, after I was already down, so I learned nothing about how it feels. I have no opinion on dash timing or recharge.
- **Reached with the manual's means:** `room 3`–`room 5` can be selected by script. I did not try them. I should have, since that is the direct way to see the later rooms and any spitters. This is the main gap in my report.

### Concrete moments (room 2, standing mostly still)

- 0–2.5 s: four grubs walked in from the corners and edges. Nothing was dangerous, and it was calm and readable. My early swipe at 1.0 s hit nothing ("(miss)") because everything was far away. That is my script's fault, not the game's.
- 2.73 s: "a grub rears back (left)", and the `G` showed up top-left of me. At 3.0 s a second one reared back on the right. Two threats were on screen within about 0.3 s of each other. The text cue and the capital `G` were easy to read.
- 3.38 s: "the grub is open (left)". I was not swiping then, so I missed the chance to counter.
- 3.57 s: first hit, 3/3 → 2/3. The attacker was a grub that had reared back about half a second earlier. I could have dodged, but my script could not react.
- 4.0–5.2 s: grubs sat directly left and right of me, taking turns biting. The log shows "open" and "rears back" calls every few tenths of a second. It felt like I was standing in a ring of grubs with no gap to leave through.
- 5.07 s: hit, 2/3 → 1/3.
- 5.5 s: my swipe hit one grub ("grub hit (1 left)"). A grub is therefore a two-hit enemy, and my swipe landed on only one of the three adjacent grubs.
- 5.87 s: hit again and down. Three hits, about 2.3 s after the first bite began, and no room cleared.
- Room 1 repeat, 11.4–14.97 s: the same pattern with three grubs. I was hit at 11.97 s, 13.47 s and 14.97 s and went down. In both runs I died without clearing anything, but I also did not try to play it.

### Did the fights feel different from each other?

Room 1 and room 2 fought the same way: grubs close in, rear back, bite and open up. Room 2 simply had one more grub. I cannot say anything about rooms 3–5 or other enemy types.

### Did my choices matter?

I can't judge this fairly, because I never reacted. Visible signs that they could matter:

- Each bite is announced by a "rears back" line, a capital `G`, and a delay of roughly half a second before the hit. That is enough time to dash or step away.
- A grub is "open" after biting, which invites a counter-swipe.

Signs that choices could matter less than they should:

- Several grubs arrive together and cycle their bites, so there always seems to be one about to bite. It felt like an "avoid the next bite" loop rather than a back-and-forth.
- The swipe only reaches a little more than one tile. With grubs on both sides, one swipe hit one grub.

### Unclear, unreadable or possibly unfair

- **Possibly short warning (medium, uncertain):** at 11.90 s the log shows "a grub rears back (left)" and the hit at 11.97 s. That is only about 0.07 s later. The other bites I could trace came about 0.5–0.65 s after their rear-back line. I can't tell if this was a different grub's earlier wind-up whose line I misattributed, or a real short warning. If real, it would be impossible to react to and would feel unfair.
- **Grubs on my tile (low–medium):** several lines read "the grub is open (on you)" or "rears back (on you)". Grubs seem to be able to stack on my tile. The screen then draws them beside me, so I could not tell which side the bite would come from, or where to swing. For an action player who relies on spacing, that is confusing.
- **Cornered (medium):** with grubs on both sides I was boxed in. I couldn't tell whether I could have walked out, since I did not try.

### Broken

Nothing was clearly broken in what I saw. The 11.97 s hit timing above is the one thing worth a second look.

### Positives

- The text cues ("rears back (left)", "the grub is open") and the capital/lowercase marks made it easy to follow what each grub was doing.
- The restart flow worked: after "run over", attack began a fresh run in room 1 with full hearts.
- Runs are short. I went down in about 6 s in room 2 and about 5 s in room 1, which suits a player who wants short, intense runs.

### Open player questions

- How are the later rooms different? Do they have spitters, and how many grubs?
- Can I dash out of the ring of grubs and counter from outside? I never tested it.
- Is the very short warning at 11.9 s real?

## Decisions already made

None.

## Constraints

I used only the player view and the manual. I read no source, tests or design files, and did not use the trace view or the bots.

## Open questions

- Please route a follow-up session that plays `room 3`, `room 4` and `room 5` directly, ideally live or with several short reactive scripts. It should dash and counter-swipe on the "rears back" cues, and it should place spitters with `room empty` if they are not in the early rooms. This report does not cover later rooms, spitters or the dash.

## Expected output

This report goes to `studio`, which decides whether to route a follow-up play session and whether to pass the experience issues to `game-designer` and the possibly short bite warning to `qa`.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, manual.md, the build `repo/`
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/52-studio-to-playtester.md
>>>END
