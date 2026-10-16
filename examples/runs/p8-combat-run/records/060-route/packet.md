# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/63-playtester-to-studio.md, goals/G-001-combat-monotony/64-qa-to-studio.md
next_seq: 65
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha c09552011dd4; run through the project's run commands)
log: last 5 of 22 entries in @log-recent; the full history is goals/G-001-combat-monotony/log.md

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/63-playtester-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/64-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 65
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
design/combat-cues-visual-spec.md
design/combat-step-44-walker-limit.md
design/combat-step-46-room3-cap.md
design/combat-step59.md
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

- Observe: done (02; QA 16, 20, 32, 36, 56). Contact-edge graze accepted (D-002, D-003). The three hits the second playtest called unfair match the design (late swipes land in the lunge; the "no cue" hit had a cue). Open: player view at 30 FPS and the late-swipe boundary at 30 FPS (QA, 62).
- Diagnose: two passes done (04, 31); a third without progress is barred by the loop limit. Review (60, D-009) chose a variant-aware playtest instead.
- Decide: skipped. All options so far are inside D-001 and the pillars. Tentative (`game-director`, Owner escalation) per D-009 if the variant-aware playtest still shows the melee reading as one fight.
- Design: complete (D-004 to D-007). Wording for late swipes is specified (59) and not yet applied to `repo/manual.md`. The variant-named cue message (D-008) stays `proposed`, not built. Both are held until after the next playtest so the played build stays steady.
- Plan: skipped (approach local). Returns if the same criterion fails verification twice.
- Build: 0.6.1 done (48). A later Build is for the manual text, and for the message change if D-008 is taken.
- Verify (QA): pass on 0.6.1 at 30 and 60 FPS (50). Visual V1–V11 need a graphical build, a proposed new Goal at Close; V12 open.
- Play: two passes done (27, 53), both scripted with one rule for all lungers. Open: variant-aware pass on 0.6.1 (61): per-mark rules, rooms 1–5, a slow run, short scripts.
- Review: pass 1 done (60): goal-not-met, moderate confidence; the evidence does not test the differences the build was changed to create. Review runs again after the playtest.

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
| 11 | Decide (Owner escalation if the melee still reads as one fight, D-009) | game-director | prepare-owner-escalation | tentative | — |
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
| 20a | Play (variant-aware, fresh, build 0.6.1 unchanged) | playtester | playtest-session | open | 61-studio-to-playtester.md |
| 20b | Observe (30 FPS player view, late-swipe boundary) | qa | verify-change | open | 62-studio-to-qa.md |
| 21 | Build (manual late-swipe text from 59; D-008 message if taken) | gameplay-engineer | implement-change | tentative (after 20a; message change only if Design/Director take D-008) | — |
| 22 | Verify (21) | qa | verify-change | tentative (only if 21 runs) | — |
| 23 | Review (pass 2) | game-director | review-outcome | planned | — |
| 24 | Next | studio | — | planned | — |

## Route changes

After 18d and 19 (59, 60): Review is goal-not-met; per D-009 the next pass is a variant-aware playtest, not a third Diagnose. Opened Play 20a (61, build 0.6.1 unchanged) and QA 20b (62, 30 FPS gaps) in parallel. Manual text (59) and the D-008 message change wait until after the playtest so the played build stays steady.

## Next action

Run two steps in parallel: `playtester` with 61-studio-to-playtester.md and `qa` with 62-studio-to-qa.md (both address the result to `studio`). Then Route with both results: compose the Review handoff for `game-director` (pass 2) with playtest 61 and QA 62, and decide whether Build 21 (manual text, optionally D-008) runs before or after Review. If Review says the melee still reads as one fight, the Owner escalation (D-009) follows instead of a Diagnose.

## Outcome

(open)
>>>END

<<<FILE @log-recent
## 046-route · 2026-10-16

Status: active. Open: 49-studio-to-qa.md.

After 16 (Build 0.6.1, 48): fits. F2 and F3 fixed in `play.py` only; the engineer ran no tests, so QA must run the suite first. Opened Verify 17 (49), a fresh Handoff without the implementation history or Sender assessment, covering the "not run" list, criterion 11 a–e and criterion 13 per D-006.

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
>>>END

<<<FILE goals/G-001-combat-monotony/63-playtester-to-studio.md
---
kind: handoff
goal: G-001
seq: 63
from: playtester
to: studio
stage: Play
outcome: done
---
# 63: playtester → studio — Observation report: combat of the current build, rooms 1–5

## Task

Report what I experienced playing rooms 1–5 of the current build through the player view, with separate reaction rules per enemy mark.

## Context

Reply to handoff 61. I played only through input scripts with reaction rules, using `python3 play.py --view player`. I did not read source, design documents or tests, and I did not use the trace view or the bots. I played as the profile describes: an action player who dodges and spaces, with no combo memorizing.

## Findings

### Method

All play was scripted reaction rules, not live play. Six sessions in two rounds. I cannot feel the pad or the timing. Reaction rules act at most every 0.15 s, so "my" dodges are an approximation of a player.

| Session | Style | Result |
|---|---|---|
| room 1, 60 FPS, "fast" | Chase every grub, swipe at 1.4 tiles, step aside on "rears back" | Cleared in 6.6 s, 3/3 hearts. |
| room 2, 60 FPS, "slow" | Wait, face enemies, swipe at 1.4 tiles, step aside on every warning | Output cut at ~27 s. Room not finished. Hearts 2/3. |
| room 3, 30 FPS | Dash on warnings, walk toward enemies | Output cut at ~26 s. Room not finished. Hearts 3/3. |
| room 2, 60 FPS, "fast" | Rush the runners and grubs, back off the brute only inside 1.6 tiles | Went down at 11.4 s. |
| room 4, 60 FPS, "my style" | Chase, dash on grub warnings, step aside on spitter aim | Cleared in 15.2 s, 2/3 hearts. |
| room 5, 60 FPS, "slow" | Keep distance from the brute, step aside on every warning | Output cut at ~19.5 s. Alive at 1/3 hearts with both spitters still up. |

Rules per mark:
- **Grub `g`:** I moved aside when it reared back and swiped when it was within 1.4 tiles. Its warning is 0.5 s and a swipe cancels it, so the answer was "step out or hit it first".
- **Runner `r`:** Same as the grub. The 0.35 s warning left little time to step aside, so swiping early or moving at the first warning mattered more.
- **Brute `G`:** I stepped away or aside and did not swipe it into its warning. The manual says a swipe will not cancel it. In the fast run I did not give the brute its own dodge rule, which is my mistake and explains that death.
- **Spitter `s`:** I moved aside or dashed across the aim line (a different answer, because the shot is a slow travelling projectile), and closed in to swipe it.

I made the rules differ for the reason above. In the fast room 2 and room 1 runs I also let "move toward" override spacing.

### Room 1 → room 2 → rooms 3–5

**Room 1 (three grubs).**
- Every grub asked the same thing: step aside, or swipe it to cancel.
- Cancelling worked every time I tried (0.6 s, 1.05 s, 2.08 s, 2.53 s, and so on). The fast run took 6.6 s with no damage.
- It was easy and quick. It was also all one move; there was nothing to adapt to.

**Room 2 (two runners, a grub, a brute).**
- The runners were over quickly (one swipe each, 3.4 s and 4.3 s in the slow run, 1.3 s and 2.1 s in the fast run).
- The brute changed the pace. It is slow and has a long warning, and its swipe-cancel does not work.
- In the slow run the brute fell into a loop from about 8 s to 27 s: it rears back, I step aside, it lunges, it follows me, it rears back again. I counted six or seven of these. I never got to hit it in the gap after a lunge, because my rules did not do that.
- That stretch felt repetitive, though it may partly be the scripting.
- In the fast run, the brute killed me after three hits (7.4 s, 9.4 s, 11.4 s). I stood next to it each time and my rules did not react to its warning.

**Room 3 (three spitters, no melee).**
- Everything was "read the line, move across it".
- The spitters take aim in turn, and the aim lines are long diagonals or straight lines across the room.
- I was never hit in the 26 s I saw. Early on I killed two spitters, but the third stayed in the far corner, and for about 20 s the same pattern repeated: aim, dash, shot lands behind me, again.
- This was the most repetitive stretch of everything I played. Attention dropped, though it stayed safe.

**Room 4 (grub, runner, two spitters).**
- This was the first room that mixed asks: a melee dodge and an aim line at once.
- I was hit once by a shot at 7.45 s while moving aside, in a crowd of several projectiles.
- It felt better than rooms 1 and 3. The grub and runner lunges, the spitter lines and my own movement overlapped, and I had to choose which to answer first.

**Room 5 (two grubs, a brute, two spitters).**
- This was the busiest room, and the only one where my attention stayed high all the way through.
- I took a shot at 6.8 s while walking through an aim line, then took a hit that I think came from the brute's lunge at 9.7 s (see the unexplained hit below), and was at 1/3 hearts by 9.7 s.
- I did kill the brute (11.45 s) and the grubs. The room did not clear in the part I saw; the output was cut while the spitters were still firing and I was still dodging.

### Repeated vs. different

- **Repeated:** the "rears back → step aside → swipe in the gap" loop in room 1, and the slow room 2 brute dance. The spitter-only room 3 felt the same from about 6 s on.
- **Felt different:** the brute (first time my swipe could not stop the warning), spitters (the first enemy that fights from range, with a line to read), and rooms 4–5 (several asks at once). Rooms 3 → 4 → 5 differ mostly in how many things overlap, not in what each thing asks.

### Did anything hurt me that I couldn't explain?

- **Brute lunge at 9.72 s in room 5.** The only message was "YOU ARE HIT by a grub". The brute's hit is reported as "a grub", and its warning also says "a grub rears back". A runner's and a brute's warnings read the same way in the message line. Only the `cue:` line (`r` / `G`) says which enemy it is. That was confusing for a moment, and a player without the cue line would not know.
- **Grub hit at 5.82 s in room 2 (slow run).** My swipe landed at 5.72 s ("grub hit") with 0.13 s left on the warning, but did not cancel it, and the lunge arrived. This was explainable (a grub needs 2 swipes, and the first one only wounded it), but easy to misjudge.
- **Spitter shots in rooms 4 and 5.** The two hits I took came from walking across lines in a field of several shots. I could tell where they came from in the printed rooms. In live play with this many `*` on screen I would expect some hits to feel unfair.

### Impact

| Issue | Impact |
|---|---|
| Room 3 spitter standoff repeats the same dodge for 20+ s | High on feel (boredom) |
| Brute loop in room 2 (dodge, wait, dodge) | Medium on feel |
| Brute and runner warnings read "a grub rears back" | Medium on clarity |
| Rooms 4–5 shot clutter | Medium |
| Room 1 offers only one kind of ask | Low to medium, as a first room it is fine |

### Positives

- Warnings were always shown before damage; I always knew roughly where danger would land.
- Room 4 and room 5 were clearly different from the single-ask rooms, and engaging.
- The brute's no-flinch rule makes it distinct from the grubs.
- The runner is a quick, readable one-swipe threat.

### Limits of my evidence

- All play was scripted reaction rules; I did not hold a pad or react in real time. Rule choices (for example, "move toward" in the fast runs) decided several outcomes.
- Outputs for room 2 (slow), room 3 and room 5 were cut by the output limit, at about 27 s, 26 s and 19.5 s. I did not see how they ended.
- I did not play room 1 slow or in my own style, or rooms 3, 4 and 5 as a fast-clear run. Room 4 was my favourite style only and room 5 only slow. The 30 FPS run was room 3 only; I made no comparison against 60 FPS.
- I saw no difference I could attribute to frame rate.
- I did not play the practice room.

## Decisions already made

None.

## Constraints

Player view only; no source, design or tests read.

## Open questions

None for the studio. I cannot say, from scripts, whether the room 3 and brute loops would feel as flat to a human player; a live check would help.

## Expected output

Studio reads this and routes experience issues to game-designer, and the "a grub rears back" wording on brute and runner to whoever owns clarity or defects.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, repo/manual.md, the build (`repo/`)
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/61-studio-to-playtester.md
>>>END

<<<FILE goals/G-001-combat-monotony/64-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 64
from: qa
to: studio
stage: Observe
outcome: done
---
# 64: qa → studio — 30 FPS coverage closed: player view (rooms 1–5) and late-swipe boundary match the design and 60 FPS; no defect; one spec conflict on shots in flight (room 3) for Design

## Task

Close the two gaps left by handoff 56: the player view at 30 FPS for rooms 1–5, and the late-swipe boundary at 30 FPS for a grub and a runner. Report any difference from 60 FPS or from `design/combat.md`.

## Context

Goal G-001. The build was not changed. Evidence comes from this step's runs only:
- `python3 -m unittest discover -s tests`: 59 tests, OK.
- Player view at 30 and 60 FPS for rooms 1–5. They are reaction scripts, as in handoff 55. Rooms 3–5 ran 12–15 s.
- Practice-room traces at 30 and 60 FPS for the grub and runner, in reach and out of reach.
- Grub swipes at 0.40, 0.50, 0.52 and 0.60 s, and a room 1 reaction trace at both rates.

## Findings

### 1. Player view at 30 FPS, rooms 1–5: matches the design, the manual and 60 FPS in everything the rules fix

**Warnings and cue lines**
- Every grub, runner and brute wind-up printed `a grub rears back` and a picture with `~`. A `cue:` line named the enemy (`g`, `r`, `G`) and gave the lane direction, 2.4 tiles, and the seconds left.
  - Standard grub: starts at "0.50 s", e.g. room 1, 2.033 s.
  - Runner: "0.35 s", e.g. room 2, 3.000 s.
  - Brute: "0.70 s", e.g. room 2, 25.967 s, and room 5, 5.000 s.
- The countdown falls consistently between prints, e.g. 0.50 → 0.03 s in room 1. The 60 FPS runs show the same values within one frame.
- The line disappears when the lunge starts. The manual and `combat.md` accept this.
- Spitters: `a spitter takes aim` → `a spitter spits` is 0.6 s apart at both rates. Brightness rises 0% → 33% → 50% → 83% in the `cue:` lines. The text view starts at 0%, as ruled in step 22.

**Spitter timing**
- Room 3, first shots: 1.8, 2.6 and 3.4 s at both rates.
- Rooms 4 and 5, first shots: 1.8 and 3.0 s at both rates.
- Cue gap in rooms 4–5 at 30 FPS:
  - Room 4: shots at 1.8, 3.0, 4.2, … with the next cue starting 0.6 s after each. Cues are 2.4 → 3.0, 3.6 → 4.2, 6.8 → 7.4, 8.0 → 8.6, and so on.
  - Room 5: 7.000 → 7.600, then 8.400 → 9.000. The gap is 0.8 s, which is at least 0.6 s.
  - No cue windows overlap.
- Cap delay in room 5 at 60 FPS: the cue due at 6.0 s was delayed to 7.0 s. This is allowed.

**Hit messages**
- `YOU ARE HIT by a grub — hearts n/3` and `… by a shot …` appear on the frame of contact.
- Shot hits: room 3 at 5.633 (30 FPS) against 5.667 (60 FPS), and room 5 at 4.333 against 4.350. That is within one frame.

**Brute**
- Room 5, a swipe during the wind-up:
  - 30 FPS: 7.867, a swipe 0.07 s before the lunge. It printed `the brute shrugs off the swipe`, the cue stayed, and the hit followed at 8.000.
  - 60 FPS: 8.517, same behaviour, with the hit at 8.783.
- Room 2, 30 FPS: swipes during the lunge (26.733) and recovery (27.233, 27.733) printed only `you swipe: brute hit`, with no shrug message. The fourth hit, at 28.100, printed `brute defeated` with no shrug message, even though the brute was already winding up (cue at 28.067). That matches criterion 19c: a killing swipe in wind-up shows no message and there is no lunge.

**One at a time and cancel**
- Room 5, 30 FPS: a swipe at 7.033 cancelled the winding-up grub. Its cue vanished and the next wind-up was the brute's, at 7.233.
- Room 1, 30 FPS: a second grub began its wind-up (2.800) only while the first was in recovery.

**Blocked contact (D-005) seen unprompted at 30 FPS**
- Room 1 reaction trace: the player was hit at 2.767, so the window ran to 3.567.
- The grub's lunge touched the player at about 3.467 (grub at 7.11, player at 7.47) while protected.
- At 3.567 the window ended with the grub still lunging, 0.43 tile from the player. Hearts stayed at 2, and the grub went into recovery at 3.733.
- This matches criterion 21b: the lunge's hit is spent.
- At 60 FPS the same room gave a hit at 3.567 instead. That timeline differs: the player was at 7.87, and first contact came after the window had ended, which is a legitimate hit.

**Differences between 30 and 60 FPS in the reaction scripts**
- Final outcomes differ:
  - Room 1: cleared at 1 heart (30 FPS) against down at 5.83 s (60 FPS).
  - Room 2: cleared at 28.1 s (30 FPS) against 11.7 s (60 FPS), both with 1 heart.
  - Room 5: 1 heart at 15 s with 2 enemies left (30 FPS) against 3 left (60 FPS).
  - Rooms 3 and 4: the same hearts at 12 s and 15 s.
- The reaction rules act on a 0.15 s grid, so positions diverge early. Examples are the room 2 grub that was avoided for many seconds at 30 FPS, and the different paths in room 1.
- I did not isolate a case of the same decision from the same state at the same time giving a different result. By criterion 16d/16e this is bot-timing sensitivity, not a finding. I make no claim beyond that.

**Verdict for item 1: matches. No difference in warnings, cue lines or messages between 30 and 60 FPS beyond one-frame timing.**

### 2. Late-swipe boundary at 30 FPS: matches the design, and differs from 60 FPS by less than one 30-FPS frame

Practice room, grub at 9.3 or 10, player at 8,4. A scripted input fires on the first frame after its timestamp at both rates (0.50 → frame 16 at 30 FPS and frame 31 at 60 FPS). Within a frame, the swipe is resolved before the grub's wind-up timer expires.

**Standard grub**

| Case | 30 FPS | 60 FPS |
|---|---|---|
| In reach, swipe mid-wind-up (0.40) | swipe at 0.433: stagger 0.367, hp 2→1, no lunge, new wind-up at 0.833 | swipe at 0.417: stagger 0.383, no lunge, new wind-up at 0.817 |
| In reach, swipe on the frame the lunge starts (0.50) | swipe at 0.533, frame 16: **cancelled** (stagger 0.367) | swipe at 0.517, frame 31: **cancelled** (stagger 0.383) |
| In reach, swipe one frame after the lunge starts (0.52) | lunge 0.533, swipe 0.567: hp 2→1, lunge continues, hit at 0.633 (hearts 3→2) | lunge 0.517, swipe 0.550: same, hit at 0.617 |
| In reach, swipe 0.60 (late) | swipe 0.633 with the hit in the same row; not cancelled | swipe 0.617 with the hit in the same row; not cancelled |
| Out of reach (grub starts 2 tiles away), swipe 0.30 | `hits: []` at 0.333; wind-up unchanged (0.200 left); lunge at 0.533; hit at 0.733 | `hits: []` at 0.317; lunge at 0.517; hit at 0.700 |

- At both rates the last swipe that cancels is the one landing on the frame the lunge begins. A swipe one frame later does not cancel.
- Lunge start is 0.533 s at 30 FPS and 0.517 s at 60 FPS. The difference is 0.017 s, half a 30-FPS frame. The cancel limit therefore differs by under one frame at 30 FPS.
- The 60 FPS probes bracket the boundary between frames 31 and 33. I did not probe frame 32.
- Lunge hit times differ by one to two frames (0.733 against 0.700, 0.633 against 0.617), which is frame sampling.

**Runner**

| Case | 30 FPS | 60 FPS |
|---|---|---|
| In reach, swipe 0.20, mid-wind-up | `runner defeated` at 0.233; no lunge; cleared | `runner defeated` at 0.217; same |
| In reach, swipe 0.43, after the lunge began | lunge 0.400, swipe 0.467: runner defeated before contact; hearts 3 | lunge 0.367, swipe 0.450: same; hearts 3 |
| Out of reach (2 tiles), swipe 0.20 | `hits: []`; wind-up continues; lunge 0.400; hit 0.600 (hearts 3→2) | `hits: []`; lunge 0.367; hit 0.550 |

- The runner's out-of-reach swipe does not cancel at either rate.
- The runner has 1 hp, so an in-reach swipe always kills it. The "a late swipe does not cancel the lunge" case is not separable from a kill for a runner. It showed as a kill at both rates, with the lunge ending before contact. The spec cannot tell "cancel" from "kill" for a runner, and I report it as observed behaviour only.
- After the first hit, the second runner lunge fell at 1.600 s (30 FPS) against 1.517 s (60 FPS), a 0.083 s gap. It comes from the earlier contact-frame difference of 0.05 s plus frame quantization. Both rates took two hits.

**Verdict for item 2: matches. At 30 FPS the cancel boundary sits at the frame the lunge starts, as at 60 FPS, and differs by less than one 30-FPS frame.**

### 3. Defects: none

I found nothing that is wrong against `design/combat.md` or `repo/manual.md`. One conflict inside the spec, found while reading the room 3 views, is below. It is not a build defect.

### Spec gap for `game-designer` (not a defect, low to medium priority): room 3 shots in flight, and simultaneous cue starts in a real room

**What the room 3 reaction runs show (same at 30 and 60 FPS)**
- All three spitters started a cue at the same moment twice: 5.800 (at both rates) and 10.000 (30 FPS) or 9.800 (60 FPS). In both cases all three then fired together 0.6 s later.
- Their checks run on the same 0.2 s grid after cap delays. The first start at 5.8 s followed the hit by a shot at 5.633 / 5.667 s, which freed a cap slot. This is my reading of the pattern and is not confirmed in code.
- This is the "real-room trace in room 3 with a surviving player past 7 s" asked for in `combat.md` open questions and D-005 (revisit).
- In both runs the player (a reaction script with "move aside") took no hit from the simultaneous volleys. Hearts stayed at 2 from 5.8 s to 12 s. The lines did cross at the player's row (30 FPS, 10.0 s). So this case did not show unanswerable shots.
- At least 4 `*` are visible in flight at 7.0, 7.5 and 8.0 s at both rates. Up to 5 would be expected: two earlier shots plus the three fired at 6.4 s. Criterion 11 says "in rooms 1–5 never more than 3 shots in flight". The cap section says real rooms stay at 3 or fewer, citing a QA observation, and also says the count at a check can reach 2 + the number of living spitters. For three spitters that is 5.
- I counted `*` from the pictures only. I did not run a trace for the exact count, and shots in the same cell as a spitter can be hidden. I cannot say whether the number is exactly 4 or 5.

**Question for Design:** is the simultaneous start in room 3 still accepted (D-005), and is "never more than 3 in flight in rooms 1–5" still the rule in room 3? The two statements conflict when a cap delay releases all three spitters at once.

**Reproduction:**
```text
room 3
fps 30
end 12
when see * coming within 1.5 then move aside
when text "takes aim" then move aside
when see s within 1.4 then attack
```
Run it at `fps 30` and `fps 60` and look at the cue starts at 5.8 s and the stars at 7.0–8.0 s.

**Acceptance criterion if Design wants a change:** in a trace of room 3 with a moving player over 12 s, the shot count never exceeds the number the spec states, at both frame rates.

## Decisions already made

- D-002/D-003: contact-edge graze. No contact in these runs was in the band. The lunge contacts were at lateral miss 0 against 0.6.
- D-004: the brute is not cancelled by a swipe. Confirmed at both rates (see item 1).
- D-005: a lunge's hit is spent when it touches a protected player. Seen at 30 FPS (room 1) and consistent with the room 5 observations in handoff 56. The simultaneous-start acceptance is raised again above because the revisit trigger has now been traced.

## Constraints

- The build and documents were not changed.
- Not run:
  - A frame-32 probe at 60 FPS.
  - A brute late-swipe boundary pair, beyond the room 2 and 5 views.
  - Dash cases at 30 FPS.
  - A trace of room 3 for the exact in-flight count.
  - A human playtest.
  - Isolating the 30/60 FPS reaction-script divergences.
- Experience judgments (monotony, fun) are not assessed here.

## Open questions

For `game-designer`:
1. The room 3 shot-count conflict and the simultaneous-start acceptance (above).
2. The manual wording from handoff 56 is still open. It should say a swipe cancels a lunge only during the warning, and not when the grub is out of reach. This step again showed an out-of-reach swipe that did nothing (2 tiles, `hits: []`, at both rates) and the cancel limit at the lunge start.
3. For a 1-hp runner, "cancel" and "kill" cannot be told apart by a swipe in reach. If the design means a separate runner cancel rule, it does not show up in play.

## Expected output

Studio: record the two 30 FPS gaps as closed and matching. Route the room 3 in-flight-count and simultaneous-start question to `game-designer`. No change is requested from `gameplay-engineer`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md, studio/skills/reproduce-defect.md
- Project: design/combat.md, repo/manual.md, the build in repo/
- Decisions: decisions/D-003-contact-edge-exact-reach-and-lunge-band.md, decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
- Previous handoff: goals/G-001-combat-monotony/62-studio-to-qa.md
>>>END
