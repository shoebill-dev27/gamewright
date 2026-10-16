# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/50-qa-to-studio.md
next_seq: 51
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha c09552011dd4; run through the project's run commands)
log: last 5 of 18 entries in @log-recent; the full history is goals/G-001-combat-monotony/log.md

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/50-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 51
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
design/combat-cues-visual-spec.md
design/combat-step-44-walker-limit.md
design/combat-step-46-room3-cap.md
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

- Observe: done (scripted play, rooms 1–3 + practice room; 02). FPS divergence (qa): done (16, 20); the contact-edge graze is accepted (D-002, D-003). Spitter fire times: build conforms to its spec (36).
- Diagnose: second pass done (31). Melee enemies share one answer (S1, the core of the Goal); rooms 4–5 spitter crossfire was unfair (S4). Evidence is scripted play; runner, brute and crossfire for a human are unconfirmed. A third Diagnose pass without progress goes to `game-director` review (loop limit).
- Decide: skipped. Options so far are variant parameters, a cancel flag, spitter timing, contact consequences; all inside D-001 and the pillars. Tentative again (game-director) if a later step finds the need for a new enemy type, healing, new input, or a scope or priority change.
- Design: complete (35, 38, 44, 46; D-004 to D-007). Criterion 13 walker limit: D-006. Room 3 cap: accepted as built, criterion 11 reworded to "shots in flight never exceed 2 plus living spitters" (D-007, design/combat-step-46-room3-cap.md); fallback if the playtest reopens it is a 0.2 s cue gap in room 3 (own spec step).
- Plan: skipped (approach local, reuses the enemy update loop). Returns if the same criterion fails verification twice.
- Build: 0.6 done (40); 0.6.1 done (48): F2 and F3 fixed in the player view only, tests written but not run by the engineer.
- Verify (QA): re-verify open (49): F2, F3, the "not run" list from 43, criterion 11 a–e, criterion 13 against D-006, and running the test suite first. F2/F3 failing again goes to `technical-director` (loop limit). Verify (visual): V1–V11 need a graphical build, a proposed new Goal at Close; V12 open until one exists. Art-director items from 35 and 38 wait with these.
- Play: first pass done (27). Second pass planned after Verify passes; fresh, hand-timed on rooms 2, 4 and 5 (runner, brute, crossfire) and room 3, including a variant that keeps spitters alive for about 12 s to force a cap delay; focus without the expected result. Reopen room 3 if the tester is hit by most of a simultaneous volley, reports a shot from nowhere, or a count exceeds 5.
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
| 12a | Design (Options 1–2, manual wording) | game-designer | write-design-spec | done | 33-studio-to-game-designer.md (result: 35-game-designer-to-studio.md) |
| 12b | Observe (spitter fire times, rooms 3–4) | qa | reproduce-defect | done (no defect) | 34-studio-to-qa.md (result: 36-qa-to-studio.md) |
| 12c | Design (invulnerable contact, room 3 cue overlap) | game-designer | write-design-spec | done | 37-studio-to-game-designer.md (result: 38-game-designer-to-studio.md) |
| 13 | Build (build 0.6 per Design 35 and 38) | gameplay-engineer | implement-change | done | 39-studio-to-gameplay-engineer.md (result: 40-gameplay-engineer-to-studio.md) |
| 14a | Verify (0.6, 30 and 60 FPS) | qa | verify-change | done (fail: F2, F3, 13@60, room 3) | 41-studio-to-qa.md (result: 43-qa-to-studio.md) |
| 14b | Design (criterion 13 walker limit, 60 FPS) | game-designer | write-design-spec | done (D-006, no build change) | 42-studio-to-game-designer.md (result: 44-game-designer-to-studio.md) |
| 15 | Design (room 3 cap vs criterion 11) | game-designer | write-design-spec | done (D-007, accepted as built) | 45-studio-to-game-designer.md (result: 46-game-designer-to-studio.md) |
| 16 | Build (F2, F3 only) | gameplay-engineer | implement-change | done | 47-studio-to-gameplay-engineer.md (result: 48-gameplay-engineer-to-studio.md) |
| 17 | Verify (re-verify, incl. "not run" list, criterion 11 a–e) | qa | verify-change | open | 49-studio-to-qa.md |
| 18 | Play (fresh, hand-timed rooms 2–5) | playtester | playtest-session | planned | — |
| 19 | Review | game-director | review-outcome | planned | — |
| 20 | Next | studio | — | planned | — |

## Route changes

After 16 (Build 0.6.1, 48): fits. F2 and F3 fixed in `play.py` only; the engineer ran no tests, so QA must run the suite first. Opened Verify 17 (49), a fresh Handoff without the implementation history or Sender assessment, covering the "not run" list, criterion 11 a–e and criterion 13 per D-006.

## Next action

Run the qa step with 49-studio-to-qa.md (result addressed to `studio`). Then Route: on pass, compose a fresh playtester Handoff (build and player profile only, no change or expected result); on fail, apply the return rules (a second failure on the same criterion goes to `technical-director`).

## Outcome

(open)
>>>END

<<<FILE @log-recent
## 037-route · 2026-10-16

Status: active. Open: 39-studio-to-gameplay-engineer.md.

After 12c (Design 38): fits. The designer ruled on blocked contact (D-005: shot consumed, lunge spent) and accepted simultaneous cue starts outside rooms 4–5; the spec is complete and no direction or scope change arose, so Decide stays tentative. Opened Build 0.6 (39) with the full change list; its result is addressed to `studio` for an independent Verify.

## 039-route · 2026-10-16

Status: active. Open: 41-studio-to-qa.md, 42-studio-to-game-designer.md.

After 13 (Build 0.6, 40): fits; the engineer found no spec gap. One bot figure (walker, 60 FPS, rooms 3–5: 7 hearts vs limit 6) is a tuning question, so Design (42) runs in parallel with independent Verify (41). Build was not rerouted; the Sender assessment was not passed to QA.

## 042-route · 2026-10-16

Status: active. Open: 45-studio-to-game-designer.md.

After 14a/14b: Verify 0.6 failed (43): F2 (brute shrug message missing in player view) and F3 (banner 0.5) are defects. Criterion 13 at 60 FPS is settled by Design 44 (D-006). Room 3 cap vs criterion 11 goes to Design (45) before Build so enemy code changes once; then Build, full re-verify, Play.

## 044-route · 2026-10-16

Status: active. Open: 47-studio-to-gameplay-engineer.md.

After 15 (Design 46): fits. Room 3 cap accepted as built (D-007), criterion 11 reworded; no enemy change, D-004/D-005/D-006 unchanged, no Decide. Build 16 is narrowed to F2 and F3 only (47), result addressed to `studio`; QA re-verify adds criterion 11 a–e.

## 046-route · 2026-10-16

Status: active. Open: 49-studio-to-qa.md.

After 16 (Build 0.6.1, 48): fits. F2 and F3 fixed in `play.py` only; the engineer ran no tests, so QA must run the suite first. Opened Verify 17 (49), a fresh Handoff without the implementation history or Sender assessment, covering the "not run" list, criterion 11 a–e and criterion 13 per D-006.
>>>END

<<<FILE goals/G-001-combat-monotony/50-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 50
from: qa
to: studio
stage: Route
outcome: pass
---
# 50: qa → studio — Re-verify of build 0.6 (repo/) at 30 and 60 FPS: PASS on everything exercised, with a short list of items not fully run

## Task

Route the result. No criterion failed in this round. No failure repeats a failure from 43, so nothing goes to the Technical Director. Decide whether the "not fully run" items below need a follow-up QA step or can be left to the hand-timed playtest. There is one non-blocking wording question for `game-designer` (criterion 11d, see Open questions).

## Context

Re-verification of build 0.6 against `design/combat.md`, `design/combat-step-44-walker-limit.md` (D-006) and `design/combat-step-46-room3-cap.md` (D-007). The evidence comes from executed runs only: unit tests, player-view and trace scripts at 30 and 60 FPS, and the bots. Times are game seconds. Visual criteria V1–V11 are out of scope. All run rounds are used (0 left), so anything not covered below could not be run.

Failures in 43: criterion 13 at 60 FPS (F1), the brute shrug message missing from the player view (F2, criterion 19a), the wrong version banner (F3), and criterion 16b as a consequence of F1. All four now pass (see below).

## Findings

### Verdict

**PASS** for every criterion exercised in this round, at both 30 and 60 FPS. Several items could only be partly covered, and they are listed explicitly under "Not run or only partly run". A reader must not take this as "every sub-item of every criterion was independently re-run".

### Unit tests

`python3 -m unittest discover -s tests`: 59 tests, OK (43 had 54, so 5 are new). They passed and I used them only as a regression signal.

### Re-check of the 43 failures

| 43 finding | Result | Evidence |
|---|---|---|
| F2: brute shrug message (19a) | **pass** at 30 and 60 | Script: `room empty`, `spawn brute 9 4`, `player 8 4`, swipes at 0.1 and 0.5. Each wind-up swipe prints `the brute shrugs off the swipe` at the swipe time (0.100 and 0.500), before `you swipe: brute hit`. The cue stays (0.23 s / 0.22 s to the lunge at 0.5). The lunge hit comes at 0.800 (30) / 0.783 (60), 1 heart lost. No message on a recovery swipe (1.3 s: `you swipe: brute hit` only). No message when a swipe kills in wind-up (swipe at 2.3 gives `brute defeated`, room cleared, no lunge). A swipe at a standard grub or runner is unchanged (`you swipe: grub hit`, `grub defeated`, `runner defeated`; no shrug). A swipe during hit-stun prints `(nothing happens)`. |
| F3: banner build number | **pass** | Every player-view output starts `Lantern Depths 0.6 — …`. |
| F1 / 16b: criterion 13 at 60 FPS | **pass** under D-006 | See criterion 13 below. |

### Per criterion

| # | 30 FPS | 60 FPS | Evidence |
|---|---|---|---|
| 1 Telegraph | pass | pass | Cue 0.033 → lunge 0.533 (30); cue 0.017 → lunge 0.517 (60). The cue line says 0.50 s to the lunge. Also seen in the h21b traces (windup 3.900 → lunge 4.400 at 30; 3.883 → 4.383 at 60). |
| 2 Sidestep | pass | pass | Grub at (9,4), player at (8,4); `0.1 move down`, `0.35 stop` (1 tile). Hearts stay 3/3 through the whole lunge and the recovery (s2). |
| 3 Dash | pass (standard, brute, runner as stated) | pass | Standard grub and brute: see 43 (c21), and 21a below. Runner: dash right at 0.3 and at 0.4 (lunge starts 0.383), hearts stay 3/3. The control without a dash is hit at 0.467 (30) / 0.433 (60). Limit: both runner scripts dash away from the lunge direction, so the no-damage result is partly displacement. A dash into the runner's lunge line was not run. |
| 4 Standing still | pass | pass | Control runner hit at 0.467 / 0.433; brute hits at 0.800 / 0.783 and 2.767 / 2.717 (f2). |
| 5 Safe window | pass | pass | Standard grub (c5std): sidestep the lunge (y=5), then walk to (6.8, 4.4) at 1.0–1.5, about 0.45 tile from the recovering grub, with no hurt window active. Hearts 3/3 at 1.6. Brute: see 43. |
| 6 Cancel | pass | pass | Standard grub, swipes at 0.1 and 0.6 (c6): the first swipe in wind-up stops the lunge (hearts 3/3 at 0.5, the grub rears again at 0.533 / 0.517, which is the 0.4 s stagger). The second swipe kills it in wind-up: `grub defeated`, `room cleared`, no lunge, no stagger. Runner: one swipe kills it in wind-up, no lunge (rswipe). The runner's non-lethal cancel cannot be observed (HP 1, any damaging swipe kills it). |
| 7 One at a time | pass (read) | pass (read) | Room 4 and 5 traces and bot logs: no two grubs in wind-up or lunge together. No dedicated three-grub script this round (carried from 43). |
| 8 Variants | pass | pass | Runner dies to one swipe (rswipe, at 0.100 at both rates). Brute needs exactly 4 (swipes at 0.1, 0.5, 1.3, 2.3 → `brute defeated`). Marks `r` and `G` appear in the views; the manual lists them. |
| 9 Cue timing | pass | pass | Room 3 cues 1.2/2.0/2.8 → shots 1.8/2.6/3.4; simultaneous cues 6.8 → 7.4 and 11.0 → 11.6, each 0.6 s. The d10 shot flew along the locked line (y=4) while the player had moved to y≈5. Each simultaneous cue has its own distinct aim line. |
| 10 Dodge | pass | pass | d10: spitter (15,4), player (8,4), `1.3 move down`, `1.55 stop` (1 tile). The first shot (1.8) passes on row 4, hearts 3/3 through 5.0 at both rates. |
| 11 Stagger and cap (amended) | pass | pass | See the criterion 11 section below. |
| 12 Rooms | pass | pass | Room 1: grubs at (3,4), (15,4), (8,0). Room 2: runners (2,1), (1,8), brute (15,7), standard (14,0). Room 3 spitters at (2,1), (14,7), (2,7). Rooms 4 and 5 as in 43 and as in the traces (room 4 runner (1,4), grub (0,1), spitters (15,0), (15,8)). |
| 13 Spitter rooms (D-006) | pass | pass | See below. |
| 14 Grub rooms | pass | pass | See below. |
| 15 Dash used | pass | pass | See below. |
| 16 Frame-rate independence | pass (16a–d); 16e partly confirmed | | See below. |
| 17 Contact edge | a, b, c pass; d partly | a, b, c pass; d partly | See below. |
| 18 Cue gap rooms 4–5 | pass (a, b, c); d not run | pass (a, b, c); d not run | See below. |
| 19 Brute | a, b, c, e, f pass; d carried from 43 | same | See F2 above. d: carried from 43, not re-run. |
| 20 Consumed shot | a, b, f pass; c, d carried; e partly | a, b, f pass; c, d carried; e partly | See below. |
| 21 Spent lunge | a, b, c, d pass | a, b, c, d pass | See below. |

**Criterion 11 (amended, step 46).**
- a: Room 3 first shots at 1.8, 2.6 and 3.4 at both rates (n11a). Room 4 first shots at 1.8 and 3.0 at both rates (t18c). Room 5: carried from 43.
- b: In the real room 3 with the reaction script, the second cues (due 3.6, 4.4, 5.2) are delayed by the cap to 6.8, and all three start together. This is the same at 30 and 60 FPS and is accepted by D-007. At 6.5 s three shots are in the air and one leaves the room before 6.8, so each check sees 2, which is fewer than 3.
- c: Rooms 4 and 5: every bot log line I read (0–9 s per run, both rates) lists at most 3 shots in flight. Cue windows never overlap (criterion 18a), so 3 is the derived maximum. Room 3: at most 5 (derived, below), which is the accepted bound.
- d (count of `*` at 7.5 and 11.7): **the literal count is not readable from the player view.** See Open questions.
  - 7.5 s, both rates: 2 visible `*` (two older shots far from the spitters). The 3 shots fired at 7.4 are 0.3 tile from their spitters and share the spitter's cell, which is drawn as `s`. The three `a spitter spits` events at 7.400 give a derived total of 2 + 3 = **5**, which is at the accepted bound, not above.
  - 11.7 s: the player view prints no picture at 11.7. The 11.5 picture has 0 `*` marks, and the three spits come at 11.600, so the count at 11.7 is a derived **3**. The 12.0 picture shows 3 marks at both rates.
  - Nothing above 5 and nothing above 3 in rooms 4–5 was seen.
- e: Cue timing 0.6 s per cue holds for the simultaneous cues (6.8 → 7.4 and 11.0 → 11.6), each along its own locked line.

**Criterion 13 (D-006: walker 3–7 hearts and at least 2 rooms cleared in rooms 3–5; dodger at most half of the walker's total and 3/3; camper clears fewer than the walker).**

| | 30 FPS | 60 FPS |
|---|---|---|
| walker room 3 / 4 / 5 | 0 lost cleared / 1 lost cleared / 3 lost not cleared | 2 lost cleared / 3 lost not cleared / 2 lost cleared |
| walker total | 4 lost, 2 of 3 cleared | **7 lost**, 2 of 3 cleared |
| dodger | 0 lost, 3 of 3 | 0 lost, 3 of 3 |
| camper | 0 of 3 cleared | 0 of 3 cleared |

Pass at both rates. The 60 FPS walker figure of 7 is the upper limit; the 30 FPS total of 4 is one above the lower limit of 3. This matches the engineer's figures in the step 44 note. Per the reporting rule, no number is outside 13a–13d, so nothing is reported to `game-designer`.

**Criterion 14.** Walker in rooms 1–2: 5 lost at both rates (room 1: 3 lost, not cleared; room 2: 2 lost, cleared). Dodger: 0 lost and both rooms cleared at both rates. Pass.

**Criterion 15.** Dodger dashes in rooms 3, 4, 5: 30 FPS 8, 7, 11; 60 FPS 10, 8, 14. Pass.

**Criterion 16.**
- 16b: 13, 14 and 15 hold at each rate.
- 16c: the dodger has the same cleared set (5/5) and 0 hearts lost at both rates.
- 16d: the walker differs between rates, as allowed.
- 16e: partly confirmed. I read the logs (`log on`) for the walker in room 3 from 0 s to about 9.5 s at both rates, and about 9 s of rooms 4 and 5. The walker's decisions run on the 0.15 s grid. A decision happens on the first frame at or after the grid time, so at 30 FPS it lands up to one frame later than at 60 FPS (for example grid 0.150: frame time 0.1667 at 30, 0.150 at 60; the walker is at x 7.333 vs 7.400). Positions therefore differ from the first second, and with them the cue-start aim lines and the shot geometry in room 3. Each heart lost that I read has a different position or decision timing behind it, such as the room 3 hits at 2.25 and 6.97 at 60 FPS, and the room 4 shot hit at 7.90 at 60 FPS. I found no case where the same decision at the same game time (±1 frame) from the same positions had a different outcome, and no rule-caused difference. The logs are cut at 20000 characters, so the later parts of rooms 4 and 5 (past about 9 s) were not read. See "Not run or only partly run".

**Criterion 17 (contact edge), scripts like those of handoff 20 (spitter at (15,4), player at (8,4) with a sidestep of known length).**
- a (shot, lateral miss 0.39 or less): miss about 0.27 (30) / 0.20 (60): hit at both, at 4.033 / 4.017 (t17a2).
- b (more than 0.40): miss about 0.67 (30) / 0.60 (60): no hit at either rate, hearts 3 through 4.6 (t17c). Note: at 0.33–0.40 (t17a, t17b) the rates disagree only at about 0.40, inside the band: 30 FPS with y=4.40 gives no hit, 60 FPS with y=4.40 hits at 4.117, and 60 FPS with y=4.33 hits at 4.050. This is in the accepted band, and the only difference is the hit itself.
- c (lunge): lateral miss 0.533 gives a hit at both rates (0.633 / 0.617); lateral miss 0.667 gives no hit at both rates (l17hit, l17miss). One case on each side of the band.
- d: for shots, the rates differ at the 0.40 reach, which is accepted (see b). I did not scan the lunge band width, so I cannot say the lunge band is within 0.03 tile. I saw no evidence that it is wider.

**Criterion 18 (cue gap in rooms 4–5, 15 s traces at both rates).**
- a, b: Still player: cues 1.2, 2.4, 3.6, 4.8 and shots 1.8, 3.0, 4.2, 5.4: the gap from a shot to the next cue is exactly 0.6 s, and cue windows never overlap. The dash script t18c in room 4 (cap delay) gives A cue 1.2 / B cue 2.4 / A cue 3.6 / B cue 5.0 (the cap delayed it by 0.2 s) / A cue 6.2 / B cue 7.4. Gaps are 0.6 s or longer at both rates.
- c with one spitter killed (k18c, room 4): spitter A killed at 2.033 (30) / 2.017 (60). The remaining spitter B cues at 2.4 (gap 0.6 from A's shot at 1.8), then at 4.8 and 7.2 (shots every 2.4 s). Gap rule respected at both rates. A spitter killed during its own cue (the cancelled-cue case) was not run.
- d: not run. The Build step provides no forced simultaneous-first-shot test, and the practice room does not use the rule.
- e: criterion 9 and the cap hold in rooms 4–5 in these traces.

**Criterion 20 (consumed shot).**
- a: Hurt window (h21b scripts): a shot hurts the player at 3.833 and the window ends at 4.633. There is no damage at the window end, hearts stay 2 until the end of the run at both rates.
- b: Dash (e20): dash right at 3.9 into the first shot. The `*` is gone by the 4.0 picture, and hearts are 3/3 at 4.07 / 4.05. The dash ends on the old line. Not repeated this round for a second shot after the dash.
- c: Normal hit unchanged: a shot reaching the unprotected player hits on arrival (b21a/b21c: `YOU ARE HIT by a shot` at 3.833). The "shot arriving at least a frame after the window ends hits" half is carried from 43.
- d (room 4 still-player 15 s): carried from 43. Not re-run.
- e (cap slots): partly. The `*` disappears at the dash contact (e20 at 4.0), but the player view prints every 0.5 s and the trace does not list shots, so the frame of the in-flight count drop was not observed.
- f (band): f20b: the player crosses the first shot's line with a lateral miss of about 0.48–0.53 (above 0.40). The shot is not consumed: the `*` is still visible and moving left at 4.0, 4.5 and 5.0. No damage at either rate.

**Criterion 21 (spent lunge).**
- a (dash): carried from 43 (c21std, c21brute). Not re-run.
- b (hurt window ends inside the lunge): h21b with the grub at x 2.59, 2.60 and 2.61, at both rates. The shot hurts at 3.833. The grub lunge starts at 4.4 (30) / 4.383–4.367 (60). Contact begins before the window ends at 4.633, and the grub is still lunging at 4.633 (x 8.32–8.58, player at 8.45, within 0.6). Hearts stay 2 to 5.0: no lunge damage. A lunge whose first contact comes after the window ends hits: b21a hits at 4.667 (30) / 4.633 (60), b21c at 4.800 / 4.750.
- c, d: carried from 43 (recovery 0.8 s; the second lunge hits normally).

### Observations (not failures)

1. The text view draws a shot that is within one cell of a spitter as `s` (shots just fired at 7.4 and 11.6 are not visible as `*` until about 0.2 s later). It does not break a criterion. It does make the room 3 `*` count at 7.5 s unreadable (see criterion 11d). Severity: low, presentation only (`art-director` owns presentation of the shot).
2. The 60 FPS walker total of 7 hearts sits at the D-006 limit, and the 30 FPS total of 4 sits near the lower limit of 3. A later change to rooms 3–5 will move these (D-006 says to re-measure).

### Not run or only partly run

- 3: a dash into the runner's lunge line (the runner scripts dash away from the lunge).
- 7: a dedicated script with three close grubs.
- 17d: the lunge band width scan.
- 18c: a spitter killed while its cue is running. 18d: not run (no forcing test exists).
- 19d, 20c (second half), 20d, 21a, 21c, 21d: carried from 43, not re-run on this build.
- 20e: the frame of the in-flight drop (`*` gone) was not observed; the view and the trace do not list it.
- 16e: the logs are cut at 20000 characters (a tool limit). The parts of rooms 4 and 5 beyond about 9 s were not read. To read them, use shorter bot scripts (for example `limit 6`, or `rooms 4` with a second script for the tail).
- Reason for all of the above: the runs were limited to the rounds available (0 left), and the tool output limit.

## Decisions already made

D-004, D-005, D-006, D-007 stand and were applied as written. D-006 limits were used for criterion 13; D-007 for criterion 11. No criterion or limit was changed by QA.

## Constraints

- Production code was not touched.
- Visual criteria V1–V11 are out of scope (no graphical build).

## Open questions

1. For `game-designer`, non-blocking: criterion 11d says "count the `*` marks at 7.5 s and at 11.7 s, expected 3 to 5". In the text view the literal count at 7.5 s is 2 (the 3 shots fired at 7.4 are drawn as `s`), and no picture is printed at 11.7 s. I judged it from the three spit events plus the visible marks (derived 5 at 7.5, 3 at 11.7; 3 marks seen at 12.0). A count of 2 is outside the stated expected range but the rule only names counts above 5 (or above 3 in rooms 4–5) as defects, so I did not invent a verdict from the literal number. Please say whether the derived counts are acceptable, or give a time at which the marks can be counted (for example 7.7 s or 12.0 s) or a trace field for shots in flight.

## Expected output

Studio decides the next step: either close this verify (no failing criterion), or ask QA for a small follow-up covering the "not run or only partly run" list (needs rounds and shorter bot logs for 16e). The playtest items in D-004 to D-007 remain open for the hand-timed playtest.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md, design/combat-step-44-walker-limit.md, design/combat-step-46-room3-cap.md, repo/manual.md, repo/README.md, project.md#constraints, the build in repo/
- Decisions: decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md, decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md, decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md, decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
- Previous handoff: goals/G-001-combat-monotony/49-studio-to-qa.md
>>>END
