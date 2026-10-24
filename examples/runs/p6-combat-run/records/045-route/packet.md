# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/39-qa-to-studio.md, goals/G-001-combat-monotony/40-qa-to-studio.md
next_seq: 41
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha e2755991a5e9; run through the project's run commands)
log: last 5 of 16 entries in @log-recent; the full history is goals/G-001-combat-monotony/log.md

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/39-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/40-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 41
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

- Observe (playtester, qa): done (02, 08, 06, 15). Not observed: room 5 fight, approaching a spitter, projectile hits, room clear, dash dodging; Play covers them.
- Diagnose, Decide: done (03; D-002, D-005, D-006). Cause: single-state, untelegraphed enemy behavior; Option A.
- Design: done (10, 16, 33). Spec `design/combat.md` (AC-1…AC-18), D-003, D-006, `design/combat-visuals.md` (V-1…V-8).
- Plan: done (14, D-004). Gap defaults F1–F11; the designer confirms them at Review, F1 (grub speed) matters most.
- Build: done. Code (18, 22, 23, 35), render fix F1/AC-18 and F3 in `play.py` (38 of 40 tests pass). The Owner placed the AC-15 practice-room paragraph in `manual.md` (D-007, as stated by the Owner; QA checks it in 7i). F2 is cosmetic.
- Verify: no AC observed failing so far. 7g (37) covers all but AC-15. Suite-only: AC-14, AC-10 2-swipe kill, "(too soon)" and "(down)" lines. Pause (F11) not implemented. 7i (38) checks AC-15 and `ManualTest`, which has no valid result yet and needs `manual.md` beside `repo/`.
- Verify, visuals: earlier V-1 fail (hidden grub), F3. Open: V-6 (color) needs a `--color` capture; V-2 gaps (60 FPS charge-start draw, draw after a missed swipe). 7h re-judges V-1, V-2, V-6 and the displaced cell from QA's captures.
- Play: `playtester`, live and reactive, from a Handoff composed by the Studio from permitted information. Watch slot starvation. Planned, after Verify passes.
- Review: `game-director` with `review-outcome`. Planned. Open: run progression after "run over"; F1, F6, F7; numbering of same-type enemies in one cell; a still player going down in about 5 s.
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
| 7g | Verify (all but AC-15) | qa | verify-change | open | 37-studio-to-qa.md |
| 7i | Verify (AC-15, `ManualTest`) | qa | verify-change | open (parallel to 7g) | 38-studio-to-qa.md |
| 7h | Verify (visuals) | art-director | visual-review | planned | — |
| 8 | Play | playtester | playtest-session | planned | — |
| 9 | Review | game-director | review-outcome | planned | — |

## Route changes

Resume after the Owner chose Option A (36, D-007): the Owner placed the manual paragraph. Goal back to `active`. 7i (AC-15, `ManualTest`) is confirmed and opened as 38 in parallel with 7g (37); 7h, Play and Review unchanged.

## Next action

Run `37-studio-to-qa.md` (7g) and `38-studio-to-qa.md` (7i) as parallel QA steps (results addressed to `studio`), then Route:
- If both pass, open 7h (art director, from QA's captures).
- On a QA fail, return to Build with the report (a second fail on the same criterion goes to `technical-director`).
- If `manual.md` is missing or altered, QA reports it and the Studio re-checks with the Owner (D-007, Revisit when).

## Outcome

(Filled at Close.)
>>>END

<<<FILE @log-recent
## 033-route · 2026-10-15

Status: active. Open: 28-studio-to-qa.md.

After 7a/7b (26, 27; both question): no AC failed. QA's `ManualTest` error came from its workspace lacking `manual.md`; the art director had no build output. Verify reruns as 7c: QA (28) checks the manual layout, runs independent scripts and captures raw output. 7d (art director) opens after 7c with those captures. Play and Review unchanged.

## 035-route · 2026-10-15

Status: active. Open: 31-studio-to-art-director.md, 30-studio-to-game-designer.md.

After 7c (29, question): no AC failed. Open as parallel steps: 7d (art director, V-1…V-8 from QA's captures) and 7e (designer rules on F1, grub on the player's tile, and the AC-15 wording). 7f/7g are tentative: only if 7e needs a build change. `ManualTest` stays not run; static check clean, not escalated.

## 038-route · 2026-10-15

Status: active. Open: 34-studio-to-gameplay-engineer.md.

After 7d/7e (32 fail on V-1, 33 done): the designer allowed overlap but never hidden (D-006, AC-18) and reworded AC-15, so Build reopens as 7f (34), with the art director's F3 (enemy over arc). 7g (QA) and 7h (art director) are now planned after it; F2 stays cosmetic.

## 040-route · 2026-10-15

Status: blocked-on-owner. Open: 37-studio-to-qa.md.

After 7f (35, question): render fix built and tested; only the `manual.md` paragraph is missing, a third round with nothing new supplied, so it is escalated (36, Option A recommended). 7g (37) runs meanwhile without AC-15; 7i (AC-15) is tentative on the Owner's answer.

## 042-resume · 2026-10-15

Status: active. Open: 37-studio-to-qa.md, 38-studio-to-qa.md.

Resume after the Owner chose Option A (36, D-007): the Owner placed the manual paragraph. Goal back to `active`. 7i (AC-15, `ManualTest`) is confirmed and opened as 38 in parallel with 7g (37); 7h, Play and Review unchanged.
>>>END

<<<FILE goals/G-001-combat-monotony/39-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 39
from: qa
to: studio
stage: Verify
outcome: pass
---
# 39: qa → studio — rendering change (build 0.5) verified: AC-17 and AC-18 pass at 30 and 60 FPS, C1/C7/C3 unchanged, one capture not obtainable

## Task

Verify the current build against AC-17 and AC-18 and D-006's display ruling, and confirm that nothing else changed. AC-15 is not judged: its manual text part is waiting on the Owner.

## Context

This is the follow-up to handoff 37 and the baseline handoff 29. I did not edit the build or `manual.md`. All evidence is from `run_tests`, `run_play` and `run_trace` output of this step (round 1 of the runs). Cuts are marked `[cut: …]`; every event line in a cut section is kept in order.

## Findings

### Verdict: `pass` for the scope of handoff 37

- AC-18 passes at 30 and 60 FPS.
- AC-17 passes for the 30/60 comparison of the scripts I re-ran. The other criteria within AC-1…14 were not re-run and rest on the suite (see section 2).
- C1, C7 and C3 are unchanged from the baseline in timings, hearts and hit results.
- AC-15 is not judged. `ManualTest` is reported as **not run**.
- The `--color` capture could not be made (section 5).

### 1. run_tests

- Command: `python3 -m unittest discover -s tests`. Exit 1. 40 tests ran: **38 passed, 0 failed, 2 errors**.
- The two errors are both `ManualTest` (`test_manual_lists_glyphs_and_lines`, `test_on_screen_section_lists_x_and_the_practice_room`), `FileNotFoundError: [Errno 2] No such file or directory: '/manual.md'`.
- This is the known `manual.md` layout matter, as the task said. Both are counted as **not run**, and I count them against no AC.
- The suite grew from 34 to 40 tests since handoff 29. No other test errors or fails.

### 2. AC-18 (no hidden enemy) and AC-17 (frame rate)

**AC-18, grub on the player's tile.** Script C1: `room empty`, `fps N`, `player 8 4`, `spawn grub 12 4`, `end 8`. Run at `fps 30` and `fps 60`. The player view, both frame rates, shows a grub glyph in a cell different from `P` in every draw where a living grub exists, from 0.00 s to 5.50 s. After the down at 5.0 s it is `xg`.

- **"(on you)" lines, 30 FPS:**
  - 3.600 "the grub is open (on you)": draw `Pg` (lowercase `g` visible). Same at the 4.00 s draw.
  - 4.500 "a grub rears back (on you)": draw `PG` (uppercase `G` visible).
- **"(on you)" lines, 60 FPS:**
  - 3.583 "the grub is open (on you)": `Pg`.
  - 4.483 "a grub rears back (on you)": `PG`.
- **Strike draws on the tile:** 30 FPS 5.00 s `PG`. 60 FPS 4.50 s `PG`, and the down draw at 5.00 s is `xg`.
- **"(on you)" with a damaged grub (C2, `1.6 attack`, `end 5`):** 30 FPS 4.867 and 60 FPS 4.883 "the grub is open (on you)" show `Pw`. The wind-up draws before show `PW`.

Raw excerpt (C1, 30 FPS):

```text
  3.600  the grub is open (on you)
   [3.60 s] hearts 1/3
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
[cut: draw at 4.00 s, identical]
  4.500  a grub rears back (on you)
   [4.50 s] hearts 1/3
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
[cut: draw at 5.00 s, `PG`]
  5.033  YOU ARE HIT by a grub — hearts 0/3
  5.033  you went down
   [5.03 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        xg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
```

Raw excerpt (C1, 60 FPS):

```text
  3.583  the grub is open (on you)
   [3.58 s] hearts 1/3
   |        Pg      |
  4.483  a grub rears back (on you)
   [4.48 s] hearts 1/3
   |        PG      |
  5.000  YOU ARE HIT by a grub — hearts 0/3
  5.000  you went down
   [5.00 s] hearts 0/3
   |        xg      |
```

(The map rows are shortened to the player row; the other rows are empty, as in the full capture.)

**AC-18, spitter on the tile.** Script: `room empty`, `fps N`, `player 8 4`, `spawn spitter 8.2 4`, `end 4`. At both frame rates every draw shows `P` with a spitter in the neighbouring cell on the right: `Ps` while idle, **`PS` during the charge** (1.00 s and 1.50 s, and 3.50 s and 4.00 s), `Ps` again after the spit.

```text
  1.000  spitter (center) charges
   [1.00 s] hearts 3/3
   |        PS      |
  1.800  spitter (center) spits
   [1.80 s] hearts 3/3
   |        Ps      |
  1.833  YOU ARE HIT by a shot — hearts 2/3
```

60 FPS: the same draws; charge 1.000, spit 1.800, hit 1.817.

**Two enemies overlapping the player.** Script: `room empty`, `fps N`, `player 8 4`, `spawn grub 8.2 4`, `spawn spitter 8.1 4`, `end 4`. The two enemies are drawn in different cells on opposite sides of `P`, in every draw and in every state:

- Idle: `sPg`.
- Spitter charging, grub idle: `SPg`.
- Spitter charging and grub winding up: `SPG`.
- Down: `sxg`.

```text
  0.033  a grub rears back (right)
   [0.03 s] hearts 3/3
   |       sPG      |
  1.000  spitter (center) charges
   [1.00 s] hearts 2/3
   |       SPg      |
  1.583  a grub rears back (on you)
   [1.60 s] hearts 2/3
   |       SPG      |
  3.667  YOU ARE HIT by a grub — hearts 0/3
  3.667  you went down
   [3.67 s] hearts 0/3
   |       sxg      |
```

60 FPS: the same draws (`sPG` at 0.017, `SPg` at 1.00, `SPG` at 1.57, `sxg` after the down at 3.633).

**Three overlapping grubs (room 1 after several bites, C7).** At 3.57 s (30 FPS) three grubs have their true cell on the player's cell. The draw shows three grub glyphs in three distinct cells beside `P`: `G` left, `g` right, `g` above. After the down it is `gxg` with a `g` above. No grub is hidden, and the wind-up `G` is on the side named in the line ("rears back (left)").

```text
  3.567  a grub rears back (left)
   [3.57 s] hearts 1/3
   |        G       |
   |       GPg      |
  3.600  the grub is open (on you)
   [3.60 s] hearts 1/3
   |        g       |
   |       GPg      |
```

**AC-17 timings and 30/60 comparison.** Timestamps for the three scripts:

| Event | 30 FPS | 60 FPS | Difference |
|---|---|---|---|
| C1 first wind-up | 1.400 | 1.383 | 0.017 |
| C1 first hit | 1.967 | 1.933 | 0.034 |
| C1 open | 2.050 | 2.033 | 0.017 |
| C1 second wind-up | 2.950 | 2.933 | 0.017 |
| C1 second hit | 3.467 | 3.450 | 0.017 |
| C1 down | 5.033 | 5.000 | 0.033 |
| C7 down | 4.967 | 4.950 | 0.017 |
| C7 run over | 6.967 | 6.950 | 0.017 |
| C3 swipe hit | 2.500 | 2.500 | 0 |
| C3 third hit | 3.500 | 3.483 | 0.017 |
| C3 down | 5.033 | 5.000 | 0.033 |

All differences are at most 0.034 s (limit 0.07 s). Event sequences are the same at both rates. AC-18's own clause "no change to timings, hearts or positions" holds (section 3). The grub wind-up to strike interval is 0.500 s and the recovery interval is 0.900 s at both rates (trace C1: 1.400→1.900, 2.067→2.967 at 30 FPS; 1.383→1.883, 2.033→2.933 at 60 FPS).

**Scope of AC-17.** AC-17 also names AC-1…AC-14. This round I re-ran only the scripts C1, C2, C3, C7, the spitter, miss and overlap scripts, at both frame rates. The 38 passing suite tests still cover the rest. The independent observations of handoff 29 for AC-3, AC-9, AC-10 and AC-12 were not repeated, and nothing in this round contradicts them.

### 3. Repeats of C1, C7, C3 compared with the earlier results (handoff 29)

I compared the event lines and the trace events. Every timestamp, heart count and hit result equals the baseline.

**C1 (30 FPS), event lines:** 1.400 rears back; 1.967 hit 2/3; 2.050 open; 2.950 rears back; 3.467 hit 1/3; 3.600 open (on you); 4.500 rears back (on you); 5.033 hit 0/3 and "you went down"; `end at 7.03 s: hearts 0/3, enemies left 1`. All the same as baseline. C1 60 FPS: 1.383, 1.933, 2.033, 2.933, 3.450, 3.583, 4.483, 5.000, `end at 7.00 s`. Same as baseline.

C1 trace lines (30 FPS):

```text
t=1.400 frame=42 ... hearts=3 ... | grub#0(9.25,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=1.967 frame=59 ... hearts=2 ... | grub#0(8.81,4.00,hp=2,strike,0.083) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.067 frame=62 ... hearts=2 ... | grub#0(8.25,4.00,hp=2,recovery,0.883) | recover {'cause': 'strike', 'who': 0, 'side': 'right'}
t=3.600 frame=108 ... hearts=1 ... | grub#0(8.00,4.00,hp=2,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=5.033 frame=151 room=empty phase=down ... hearts=0 ... | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
```

The 1.400, 1.967 and 2.067 lines are identical to the baseline trace lines in handoff 29. The positions agree too (grub x 9.25, 8.81, 8.25, 8.00).

**C7 (room 1, no input, `15 attack`, `end 20`), 30 FPS:**

- Event lines match the baseline line for line: 1.400 above, 1.900 left, 1.967 hit 2/3, 2.050, 2.550, 2.900, 2.950, 3.467 hit 1/3, 3.550, 3.567, 3.600 (on you), 4.217, 4.450, 4.500, 4.967 hit 0/3 and down, 6.967 run over, 15.000 "a new run begins" and "room 1 begins", second run through 19.967 down.
- 60 FPS: down at 4.950, run over 6.950, new run 15.000, second run down 19.950. Same as baseline.
- Trace: `run_over {'rooms': 0, 'complete': False}` at t=6.967 (30 FPS) and t=6.950 (60 FPS). `run_start; room_loaded {'room': '1'}` at t=15.033 and t=15.017 with hearts=3. Same as baseline.

**C3 (`2.5 attack`, `end 6`), 30 FPS:** 1.400 rears back, 1.967 hit, 2.050 open, 2.500 "you swipe: grub hit (1 left)", 2.950 rears back, 3.500 hit 1/3, 3.600 open, 4.500 rears back, 5.033 hit 0/3 and down. 60 FPS: 2.500, 2.933, 3.483, 3.583, 4.483, 5.000. Same as baseline.

C3 trace at the swipe (30 FPS) and baseline-equal:

```text
t=2.533 frame=76 ... | grub#0(8.42,4.00,hp=1,recovery,0.417) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)]}; knockback {'who': 0}
```

C3 trace at 60 FPS: `t=2.517 ... grub#0(8.33,4.00,hp=1,recovery,0.417) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)]}; knockback {'who': 0}`.

C2 (`1.6 attack` in the wind-up) also matches the baseline: 1.600 hit and "the grub is open (right)", next wind-up 2.667 (30 FPS) / 2.683 (60 FPS), first hit 3.233 at both rates.

**The only differences from the baseline are in the draws**, and are the intended ones: where the baseline showed only `P` for an enemy on the player's tile, the new draws show the glyph beside `P`.

### 4. The hit draw with the swipe arc

The enemy glyph is visible over the arc. The arc `)` is drawn on the tiles above and below, and the hit enemy's own cell shows the enemy glyph, not the arc.

C3, 30 FPS, 2.500 swipe:

```text
  2.500  you swipe: grub hit (1 left)
   [2.53 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |         )      |
   |        Pw      |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
```

- C3 60 FPS 2.52 s and C2 at 1.63 s (30 FPS) / 1.62 s (60 FPS) show the same `)` / `Pw` / `)`.
- The damaged glyph `w` is visible under the arc.
- A swipe that hits nothing draws the arc in all three cells: `)` / `P)` / `)` (miss script, 0.53 s at 30 FPS and 0.52 s at 60 FPS).

Not observed: a swipe while an enemy is on the player's tile and drawn beside `P` (the arc and the displaced glyph in the same cell). No script of mine covered it.

### 5. Captures for the art director

Verbatim where shown above. "Source" names the script.

| Requested | Result | Where |
|---|---|---|
| Grub on the player's tile in wind-up | captured | C1 30 FPS 4.50 s `PG`; 60 FPS 4.48 s `PG`; C7 3.57 s `GPg` |
| Strike draw | captured | C1 30 FPS 5.00 s `PG`; 60 FPS 4.50 s `PG` (strike starts at 5.000 / 4.983 in the trace) |
| Recovery draw | captured | C1 3.60 s `Pg` (30 FPS), 3.58 s (60 FPS); C2 4.87 s `Pw` |
| Spitter on the tile | captured | section 2, `Ps` idle, `PS` charging |
| Swipe after a miss | captured | miss script, section 4 |
| 60 FPS charge-start draw | captured | spitter on the tile, 60 FPS, 1.000 s `PS` and 3.500 s `PS` |
| One `--color` capture | **not captured** | see below |

**Color.** The project commands as given (`run_play: python3 play.py --view player {script}`) have no place for `--color`, and no output of mine contains ANSI codes. The only input of a run is the script, so I could not add the flag. The captures above are plain text. Handoff 29's reading of the code (lantern yellow for the player, orange for alert enemies, red for shots) is unchanged and not verified here. The studio should arrange a color run (for example a run command with `--color`) or leave color to the art director's own check.

### 6. Not verifiable, or not done

- **ManualTest** (2 tests): not run, because `manual.md` is missing from the workspace. Counted against no AC. AC-15's manual part is not judged.
- **`--color` capture:** not obtainable with the given commands.
- **Swipe while an enemy sits on the player's tile** (arc and displaced glyph together): not observed.
- **AC-14 and the suite-only items from handoff 29** (room clear, "(too soon)", "(down)" in the player view, the 2-swipe spitter kill): not re-run. They rest on the passing suite.
- **Pause:** still not verifiable (no script line for it).
- **Bots (`run_bots`):** not run. The handoff did not ask for balance numbers, and the simulation was meant to be unchanged. C1/C7/C3 equality supports that.
- **Where the displaced glyph sits:** in the captures it appears on the right when the grub sits at or slightly right of the player, and left/above for the extra grubs, as the D-006 order says. I did not check the "side it last came from" preference separately, because the captures all place a single grub on the side it came from. The art director may judge readability (an open point in the spec).

## Decisions already made

- D-006: enemies may overlap but are never hidden. Observed true at 30 and 60 FPS for grub, spitter, damaged grub, a down player and two or three enemies.
- D-001: no new inputs. None seen.

## Constraints

- All checks were run at 30 and 60 FPS through `run_tests`, `run_play` and `run_trace`. I did not edit the build or `manual.md`.

## Open questions

1. **For the studio:** provide a way to capture `--color` output, or decide the art director's color check is done outside QA.
2. **For the Owner or studio:** the `manual.md` layout, so `ManualTest` can run and AC-15 can be judged.

## Expected output

The studio can accept the rendering change for AC-17 (as listed in section 2) and AC-18. The art director can use the captures in section 5 for the visual re-check. No defect is routed to `gameplay-engineer`.

## Load

- Role: studio/roles/studio.md
- Skills: none
- Project: design/combat.md, manual.md
- Decisions: decisions/D-006-overlap-display-and-practice-room-manual.md
- Previous handoff: goals/G-001-combat-monotony/37-studio-to-qa.md
>>>END

<<<FILE goals/G-001-combat-monotony/40-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 40
from: qa
to: studio
stage: Verify
outcome: question
---
# 40: qa → studio — AC-15: paragraph present and behavior matches, but `ManualTest` is blocked (`manual.md` is missing in the run workspace)

## Task

Report the AC-15 verification requested in handoff 38. Verdict: **AC-15 cannot be passed yet.** The paragraph and the behavior checks are fine, but the two `ManualTest` tests have no valid result because `manual.md` is not in the run workspace. This is a blocker, not a test failure. Studio needs to get `manual.md` into the QA workspace and route a re-run of `run_tests`.

## Context

G-001 (combat feels monotonous) is in Verify. D-007 says the Owner appended the practice-room paragraph to `## On screen` in `manual.md`. Handoff 38 asked for three checks:
1. The paragraph is present, word for word, inside `## On screen`.
2. The two `ManualTest` tests pass.
3. The build behaves as the paragraph says.

I used one run round (round 1) for all the runs listed below. No further runs were needed for the behavior checks. A re-run of `run_tests` cannot help until `manual.md` exists in the workspace, so I did not spend the other rounds.

## Findings

### 1. Paragraph check (read from the `manual.md` supplied in this packet): present

- The `## On screen` section contains, after the color note, a final paragraph reading: "The practice room (`room empty`) is not part of a run. Enemies appear only where your script places them (`spawn`), and you stand where `player` puts you. Nothing heals, there is no next room, and the session ends a moment after you go down. If a grub or spitter is on your tile, it is drawn on a free tile next to you, so you can always see it."
- I compared it with the D-007 text sentence by sentence. It is identical.
- It sits before the `## What you hear and read` heading, so it is inside `## On screen`.
- Caveat: this is the packet's copy of `manual.md`, not the file that `run_tests` reads. I could not confirm that the two are the same file (see item 2).

### 2. `run_tests`: BLOCKED (environment), not a failure

Command: `python3 -m unittest discover -s tests`. Exit 1, 40 tests run, 2 errors, both in `ManualTest`:
- `test_manual_lists_glyphs_and_lines`: `FileNotFoundError: [Errno 2] No such file or directory: '/manual.md'`
- `test_on_screen_section_lists_x_and_the_practice_room`: `FileNotFoundError: [Errno 2] No such file or directory: '/manual.md'`

The other 38 tests passed (`.....................EE.................`).

Both errors are raised by `MANUAL.read_text(...)`, before any content check. The error path is `/manual.md`, so in the run workspace `REPO.parent / "manual.md"` resolves to the filesystem root, with the tests under `/work/tests`. The file is simply not at that location. The test never saw the paragraph, so **I report no pass or fail for these two tests.** The earlier situation from handoff 37 is unchanged: `manual.md` is still not beside `repo/` in the QA workspace.

### 3. Behavior checks (all at the build as run)

| Paragraph claim | Evidence | Result |
|---|---|---|
| Enemies appear only where the script places them | Scripts `grub-d4` and `clear-practice` spawn exactly one grub each. The trace setup row shows only `grub#0` at the spawn coordinates. No other enemy appears. | OK |
| You stand where `player` puts you | Trace setup: `pos=(8.00,4.00)` for `player 8 4`. | OK |
| Not part of a run | `down-practice` ends with the plain line `end at 5.63 s: hearts 0/3, enemies left 1`. No "run over — rooms cleared" and no "press attack to start again" appear. | OK |
| Nothing heals | `clear-practice`: the grub is defeated at t=1.317 and "cleared" is traced. Hearts stay 2 at t=1.333 and 6.000, with no heal. | OK |
| No next room | In `clear-practice` the trace stays `room=empty phase=playing` to t=6.000. No room load occurs. | OK |
| Session ends a moment after you go down | `down-practice`: down at 3.633 s, `end 20`, but the session ends at 5.63 s. That is 3.633 + 2.0 s, matching design "Practice room (Q4)". | OK |
| Enemy on your tile is drawn on a free adjacent tile | `down-practice` at 0.00 s: the grub at x 8.2 is drawn `Pg`. The trace shows "grub open (on you)" at 3.583 s with the grub at (8.00,4.00), and the draw is `Pg`. Wind-up "on you" at 4.483 s draws `PG`. The spitter at x 8.2 draws `Ps` and `PS` during its charge (30 FPS). The glyph is never hidden under `P`. A down player is drawn `xg`. | OK |

Further observations:
- The AC-18 display behavior holds for every "(on you)" line in the captured runs (`Pg` when open, `PG` when winding up).
- In `grub-d4` (60 FPS), the wind-up begins at 1.383 s with the grub at distance 1.25. The strike lands at 1.933 s. The recovery follows at 2.033 s. The next wind-up begins at 2.933 s, and the cycle is about 1.55 s per bite.
- The spitter-on-tile run (30 FPS) shows first charge at 1.000 s, spit at 1.800 s, and the next charge at 3.500 s. These match the design.

Coverage limits: the grub and practice-room checks were run at 60 FPS and the spitter-on-tile check at 30 FPS. I did not repeat each practice-room check at both frame rates, since AC-15 and handoff 38 do not require it. The wider AC-17 comparison belongs to step 37.

## Decisions already made

- D-005: the Owner places `manual.md` content. I did not edit it and I report a problem rather than fix it.
- D-006: the practice room is listed in On screen; enemies may overlap the player but are never hidden. The overlap behavior was observed to match.
- D-007: the Owner placed the paragraph. I verified it independently from the packet copy, not on trust. The packet copy matches the decision text.

## Constraints

- I did not modify `manual.md` or the build.
- Handoff 38 says that if `manual.md` is missing, I report a blocker and not a test failure. I have done that.
- I used only the project's run commands.

## Open questions

1. **For Studio / Owner:** why is `manual.md` still absent from the QA run workspace? The `ManualTest` path resolves to `/manual.md`. Placing the file "beside `repo/`" must match whatever `REPO.parent` is in this environment. Please confirm where the file must sit, or give the QA run environment the file, then route a re-run of `run_tests`.
2. The expected result is 40/40 if the placed file is the same text as the packet copy. I cannot predict the content checks in `test_on_screen_section_lists_x_and_the_practice_room`, because the tests have not read the file in this workspace.

## Expected output

Studio resolves the workspace blocker and re-routes QA for a short re-run of `run_tests`. QA then reports the two `ManualTest` results.

Verdict for this step, by item:
- Paragraph present, word for word, in `## On screen` (packet copy): **pass**
- Behavior described by the paragraph matches the build: **pass**
- `ManualTest` (2 tests): **no valid result (blocked: `manual.md` not found at `/manual.md`)**
- AC-15 overall: **not yet passable**, pending the re-run. This is not a fail and it is not a pass.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: manual.md; design/combat.md (AC-15, AC-18); project.md#current-state; repo (build; `run_tests`, `run_play`, `run_trace`)
- Decisions: decisions/D-005-owner-places-manual-draft.md, decisions/D-006-overlap-display-and-practice-room-manual.md, decisions/D-007-practice-room-paragraph-placed-by-owner.md
- Previous handoff: goals/G-001-combat-monotony/38-studio-to-qa.md
>>>END
