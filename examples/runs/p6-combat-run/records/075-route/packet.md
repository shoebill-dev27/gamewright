# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/70-qa-to-studio.md, goals/G-001-combat-monotony/71-art-director-to-studio.md
next_seq: 72
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha 74624711b510; run through the project's run commands)
log: last 5 of 28 entries in @log-recent; the full history is goals/G-001-combat-monotony/log.md

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/70-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/71-art-director-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 72
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

- Observe (playtester, qa): done (02, 08, 06, 15, 58). Not settled by QA: "(miss)" text first-hand, knockback of an on-you grub in open floor, D-58-1 at 30 FPS. These go to Verify against the new spec.
- Diagnose, Decide: done (03, 53; D-002, D-005, D-006, D-011). A4 (120° cone), D1 (facing mechanic) and D2 (room 1 composition) are held with revisit triggers in 59.
- Design: done (59, 60, 65; `design/combat.md`, `design/combat-visuals.md`, D-011, D-012, D-013, AC-19…AC-28, V-9…V-17).
- Plan: done (14, D-004). The engineer reports Waiting behavior fits the existing grub movement, so the tentative new Plan is dropped unless Verify says otherwise.
- Build: done (67). Open caveats: the last suite run had 4 problems (2 `ManualTest` from a missing `manual.md` in that environment, 2 from a test fixed but not re-run); bots and the color view were not run. Manual text for V-15 and the D-013 sentence is Owner-placed (D-005, D-007); 10-O is open.
- Verify: 13a (qa, 68) and 13b (art-director, 69) open in parallel on the new build: AC-1…AC-28 at both frame rates, V-9…V-17, full suite with `manual.md` present.
- Play: earlier sessions saw only rooms 1 and 2 by script (50, 54), with defeats. Rooms 3–5, the spitter, projectile hits, room clear, the dash and a survived run are unobserved, so monotony itself is unjudged. Next Play follows Verify: fresh playtester, rooms 1–5, reactive play; judged against the retest guideline, which is not forwarded.
- Review: `game-director` with `review-outcome`, planned after the next Play. Open: run progression after "run over"; F1, F4, F6, F7; numbering of same-type enemies in one cell; A4, D1, D2.
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
| 10-O | Owner: place manual draft (59) and V-15 text | owner | — | open | 62-studio-to-owner.md |
| 11 | Plan | technical-director | technical-plan | skipped (Waiting behavior local, per 67; reopen if Verify disagrees) | — |
| 12 | Build (first attempt) | gameplay-engineer | implement-change | done (question: no repo files; Q1 gap) | 61-studio-to-gameplay-engineer.md |
| 12a | Design (Q1 knockback at distance 0, Q2, 3 passages) | game-designer | write-design-spec | done (D-013, AC-28) | 64-studio-to-game-designer.md |
| 12b | Build (re-issue with repo files) | gameplay-engineer | implement-change | done (AC-19…AC-28 built; suite re-run needed) | 66-studio-to-gameplay-engineer.md |
| 13a | Verify | qa | verify-change | open | 68-studio-to-qa.md |
| 13b | Verify (visuals) | art-director | visual-review | open | 69-studio-to-art-director.md |
| 14 | Play (rooms 1–5, fresh playtester) | playtester | playtest-session | planned | — |
| 15 | Review | game-director | review-outcome | planned | — |

## Route changes

After 12b (67): done, fits the plan; no spec gap, no escalation. Opened Verify in parallel: 13a QA (68, no Sender assessment, full suite with manual.md plus bots at 30/60 FPS) and 13b art-director (69). Tentative Plan (11) dropped: Waiting behavior is local.

## Next action

- `qa` runs 13a from `68-studio-to-qa.md` and `art-director` runs 13b from `69-studio-to-art-director.md`, in parallel; both address results to `studio`.
- Owner answers `62-studio-to-owner.md` (A recommended: place the manual text; 65 adds one suggested line for `manual.md`). It does not block Verify, but QA reports which manual text is missing.
- Then Route waits for both results. If both pass: compose a fresh Play handoff for the playtester (14) from the build and player profile only, with no change or result information.

## Outcome

(Filled at Close.)
>>>END

<<<FILE @log-recent
## 064-route · 2026-10-16

Status: active. Open: 57-studio-to-art-director.md.

After 10a/10b (58, 59): both done; 10c (57) still open, so the Route waits for it. 59's rules already settle D-58-1 (a hit in Strike cancels it), dash distance, facing and miss wording. Left for Build/Verify: on-you knockback direction, "(miss)" first-hand, D-58-1 at 30 FPS. The Owner step for the manual draft (10-O) is now planned.

## 066-route · 2026-10-16

Status: active. Open: 61-studio-to-gameplay-engineer.md.

After 10c (60): done. The visual spec is text/display only, so no rule change and no escalation. Opened Build (12, 61) and Owner manual placement (10-O, 62) in parallel. 60's "Build updates manual.md" corrected to the D-005 pattern (Owner places). 13b confirmed planned (the view changes).

## 068-route · 2026-10-16

Status: active. Open: 64-studio-to-game-designer.md.

After Build 12 (63, question): Build could not start (no repo files in its packet) and the spec lacks the knockback direction at distance 0. Per the Build return rule, Design re-opens (12a, 64); Build re-issues as 12b with repo files named in Load. No parallel Build, since both touch the same files. No escalation.

## 070-route · 2026-10-16

Status: active. Open: 66-studio-to-gameplay-engineer.md.

After 12a (65): done. Q1 is settled by D-013 and AC-28; Q2 and three passages are clarified. No parameter, input or direction change, so no Decide and no escalation. Build re-issued as 12b (66) with the repo files in Load. 11 stays tentative.

## 072-route · 2026-10-16

Status: active. Open: 68-studio-to-qa.md, 69-studio-to-art-director.md.

After 12b (67): done, fits the plan; no spec gap, no escalation. Opened Verify in parallel: 13a QA (68, no Sender assessment, full suite with manual.md plus bots at 30/60 FPS) and 13b art-director (69). Tentative Plan (11) dropped: Waiting behavior is local.
>>>END

<<<FILE goals/G-001-combat-monotony/70-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 70
from: qa
to: studio
stage: Verify (report to Studio; the Studio composes the next step)
outcome: fail
---
# 70: qa → studio — Verification report for the combat response change set (AC-1…AC-28, V-9…V-17) at 30 and 60 FPS: FAIL

## Task

Report the pass/fail result of verifying the current build in `repo/` against `design/combat.md` (AC-1…AC-28) and `design/combat-visuals.md` (V-9…V-17, earlier V items as regression) at 30 and 60 FPS. Route the failures. Verdict: **fail**. One failure is a genuine test failure, one is a frame-rate-dependent display defect, and one is a manual gap that criterion V-15 needs.

## Context

Handoff 68 asked for verification of the grub turn-taking, engagement cap, 0.15 s hit-stun, body hit, dash facing, miss causes, Strike cancel, on-tile knockback, `on you:` line and attacker position in hit lines. I verified from the spec, criteria and build only. All runs (tests, play, trace, bots) are in `@run-results`, and no rounds are left. I did not edit the repo or `manual.md`.

## Findings

### 1. Test suite (`python3 -m unittest discover -s tests`)

Ran 63 tests: **failures=2, errors=2**, so 59 passed. The earlier Owner run (D-010) was 40/40, so the suite has grown and that result does not carry over.

- `ManualTest.test_manual_lists_glyphs_and_lines`: ERROR, `FileNotFoundError: '/manual.md'`.
- `ManualTest.test_on_screen_section_lists_x_and_the_practice_room`: ERROR, same cause.
  - The tests look for `manual.md` one level above `repo/`, and it is not present in my environment. This is an environment gap, not a build result.
  - **AC-15 cannot be judged by me this round.** The Owner must run the suite with the unchanged `manual.md` in place (as in D-008 and D-010) and report counts and any failure by name.
  - By reading, `manual.md#on-screen` lists `x` (table row) and the practice room (paragraph), so AC-15's wording looks satisfied.
- `CrowdTest.test_hit_stun_is_short` (fps=30): FAIL at `tests/test_game.py` line 282, `assertTrue(game.invulnerable)` was False.
- `CrowdTest.test_hit_stun_is_short` (fps=60): same FAIL.
  - I cannot see the test source, so I cannot say whether the test or the build is wrong.
  - My own traces show the rule behaving as specified: invulnerable until 0.8 s after the hit (30 FPS: hit 0.567, ends 1.367; 60 FPS: hit 0.550, ends 1.350), and stun 0.15 s.
  - This is a failing test in the suite and counts as a failure of AC-22 and AC-17 until the engineer explains it.

### 2. Defects found by playing

**D-A (30 FPS only): the grub is drawn on the opposite side of its true position after a wall knockback. This breaks V-16, V-10 and the intent of AC-28(b) and D-013.**

Reproduce:
```
fps 30
room empty
player 14.5 4
spawn grub 14.5 4
end 2
0.2 attack
```
- Trace at 30 FPS: after the hit, the grub moves to x=14.33 and then 13.50 (left, 1.0 tile). It winds up at 0.800 with `side: left` and strikes with `pos: left`. The true positions satisfy AC-28(b): left, 1.0 tile, inside the room.
- Player view at 30 FPS: the draws at 0.50 s, 0.80 s, 1.00 s and 1.33 s still show `on you: w open (shown right)` / `on you: W biting soon (shown right)` and the glyph to the **right** of `P`, from 0.5 s until about 1.45 s.
  - In the same draws, the text lines say "a grub rears back (left)" and "YOU ARE HIT by a grub (left)". Picture and text contradict each other, and the grub appears to have jumped to the side the player was not shown.
- At 60 FPS the same script is correct. The 0.50 s draw shows `wP` with no `on you:` line, and 0.80 s shows `WP`, matching the text (left).
- Likely cause (QA's reading, not verified): the grub rests at exactly x=13.5, a half-tile boundary, so its cell differs between frame rates.
- The spec does not say how cells round at exactly .5. The engineer should check it, and the designer should say if the rule needs a line.

**D-B: position word "(left)" in a line while the same draw has an `on you:` entry for that grub (room 2).**
- 30 FPS, `room 2`, `end 6`: "the grub is open (left)" at 3.383, and the draw at 3.40 shows `on you: g open (shown left)`.
- The same happens at 4.383 with "(right)" and `on you: … g open (shown right)`.
- 60 FPS shows the same at 3.383 and 4.383.
- The text line takes its word from the true position (about 0.2 tile away, so "left"). The on-you line and the displaced glyph use cell equality.
- V-12 and "Position words" say "same tile as the player: on you", and a reader sees both "(left)" and an on-you entry.
- **Spec gap:** "same tile" is not defined as true-position-based or cell-based. The game-designer or art-director must decide (see Open questions).

**D-C: the hit-line position word differs between frame rates (room 2, around 4.3 s). This is V-16, and V-14's general sentence at 30 FPS.**
- 30 FPS: "YOU ARE HIT by a grub (right)" at 4.300 (trace `pos: right`, grub at 8.67,3.55). The draw before the hit (4.00) shows `G` at the top right.
- 60 FPS: "(top right)" at 4.283 (grub at 8.76,3.49). The draw before the hit shows `G` at the top right, so it matches.
- The word is taken from the lunge position at the damage tick, which differs between frame rates, so at 30 FPS the named position does not match the uppercase glyph in the draw before the hit.
- The scripted V-14 scenario (one grub left, one right) passes at both rates.

**D-D (Owner step, not a code defect): `manual.md` lacks the text that V-15 requires.**
- Not present:
  - The `on you:` line, and "a letter beside `P` named on that line is on your tile". The manual only says "drawn on a free tile next to you".
  - The position in the hit line ("YOU ARE HIT by a grub (left)"), "(on you)", and the position words, in `#what-you-hear-and-read`.
- Outdated: the manual still says "(miss)" means "nothing in reach". No criterion requires the miss causes ("too far", "not in front") to be in the manual, but the player-visible text now differs from the manual.
- Present and consistent: glyph table, `x`, arcs, the practice room in On screen (V-5, AC-15 wording).
- Needed by a criterion: V-15 (both parts). The Owner places the draft text (open Owner step). Then re-check V-15 and rerun the suite.

### 3. Per-criterion results

"Observed" means I saw it in this round's runs. Rows marked "not observed" were not re-run this round, so I cannot confirm them, and no regression was seen in the evidence I do have.

**AC list**

| ID | Result | Evidence |
|---|---|---|
| AC-1 | not observed (indirect: telegraph precedes the first bite by 0.5 s in all runs) | no distance-4 run |
| AC-2 | pass 30/60 | windup 0.5 (0.800→1.300), strike 0.15, recovery 0.9 on the 60 FPS trace (0.900 at recover) and 0.883 on the 30 FPS trace (0.9 minus one tick) |
| AC-3 | not observed | |
| AC-4 | pass 30/60 | `cycle` runs: bites at 0.567→2.100 (30, gap 1.53 s) and 0.533→2.083 (60, gap 1.55 s) after a counter hit in Recovery |
| AC-5 | pass 30/60 | `strike-a-30` and `far-knock`: hit in Windup, `recover interrupted` about 0.6 s, no heart lost |
| AC-6 | pass (sampled) | room 5 still: only one grub in Windup/Strike at each sampled row, both rates |
| AC-7 | pass 30/60 | room 5: charges at 1.000 and 1.800, repeats at 3.500 and 4.300 |
| AC-8 | partial | charge/spit rows name the spitter, no duplicates; player view of spitter not run |
| AC-9, AC-10, AC-12 | not observed | |
| AC-11 | pass | one reason per miss ("too far", "not in front", plain "(miss)"); "stunned" and "dash not ready" appear in the trace as ignored actions |
| AC-13 | partial | `you went down`, `x`, enemies stop, shots=0, `over` 2.0 s later (30: 5.267→7.267; 60: 5.250→7.250). Run-over screen text and attack-restart not observed |
| AC-14 | partial | practice room only: "grub defeated" then "room cleared". Heal, next-room load, same-tick clear and "run complete" not observed |
| AC-15 | **cannot judge, needs the Owner's run** | see §1 |
| AC-16 | pass for rooms 1, 2, 5 | setup rows match; rooms 3 and 4 not observed |
| AC-17 | **fail** | event timings agree within 0.02 s (e.g. room 2: windups 2.733/3.733/4.733 at both rates), but D-A and D-C break the 30/60 identity of the display and hit-line positions, and AC-22's suite test fails |
| AC-18 | partial | on-tile windup and open draws show `G`/`g` beside `P`. The distance-4 idle run to 5.5 s and the spitter `S` case were not run |
| AC-19 | pass 30/60 | wind-up starts in room 2 at 2.733, 3.733, 4.733 (both rates); room 1 at 1.400, 2.400, 3.400 (30) and 1.383, 2.383, 3.383 (60); room 5 at 2.233, 3.233, 4.233 (30). Gaps are 1.0 s. Single grub: AC-2 cycle unchanged |
| AC-20 | pass (sampled) | room 2: at the sampled rows at most 2 grubs are within 1.5 tiles, the others `waiting-cap` at about 2.0 (e.g. 3.233: g1 and g3 at 2.0). Not every tick is visible in the trace |
| AC-21 | pass, thin margin | first to third heart: 3.300→5.267 = 1.97 s (30), 3.283→5.250 = 1.97 s (60), limit 1.9. One grub committed at a time |
| AC-22 (behavior) | pass 30/60 | stun ends 0.15 s after the hit. Attack at +0.05 s and dash are "stunned". Attack at +0.28 s swipes. Invulnerability ends 0.8 s after the hit. Dash 0.25 s after the hit not exercised |
| AC-22 (suite) | **fail** | `CrowdTest.test_hit_stun_is_short` fails at both rates, see §1 |
| AC-23 | pass 30/60 | (a) on-tile and 0.2 tile: hit. (b) 0.4 tile behind, facing right and left: hit. (c) 0.8 tile behind: `miss: not in front` |
| AC-24 | pass 30/60 | `dash left` after facing right gives `facing: left` and `(` arc; `dash` with no direction after `move up` goes up and the attack faces up; an attack queued during a dash fires at dash end facing left |
| AC-25 | pass 30/60 | `dash right` from x=8 ends at 12.00; `dash left` from x=2 ends at 0.00; both last about 0.233 s (0.25 minus one tick); a second dash at +0.4 s is "dash not ready". Damage during a wall-shortened dash not exercised |
| AC-26 | pass 30/60 | a swipe on the first tick of Strike (30: 0.567; 60: 0.550) hits and cancels it, no heart lost, 0.6 s Recovery. A swipe in Recovery in front hits. No "(miss)" |
| AC-27 | pass 30/60 | "(miss) too far" (grub 2.0 ahead), "(miss) not in front" (grub 1.0 below), "(miss)" alone; arc drawn in all three |
| AC-28 (a) | pass 30/60 | `player 8 4`, `spawn grub 8 4`: shown right with `on you:`; after the hit the 0.23/0.22 s draw still shows it on the tile, the 0.50 s draw shows `w` right of `P` with no `on you:`; true position 9.00 (1.0 tile) |
| AC-28 (b) | true positions pass; **display fails at 30** | see D-A |
| AC-28 (c) | not observed | no room 2 run with an on-tile grub |
| AC-28 (d) | pass | knock-on-tile sequence shows state and timers unchanged; next bite is 1.5 s or more after the previous |
| AC-28 (e) | pass | "you swipe: grub hit (1 left)" without "(on you)" |

**V list**

| ID | Result |
|---|---|
| V-1 | pass for grubs; `w` in the hit draw |
| V-2 | pass for windup start and swipe draws at both rates; charge and projectile draws not observed |
| V-3 | pass |
| V-4 | pass for `g/w`, `G/W`; `s/z`, `S/Z` not observed |
| V-5 | pass by reading `manual.md` (glyph table, `x`, arcs) |
| V-6 | not assessable in the text view |
| V-7, V-8 | not observed this round (V-8: the trace shows `over` but the restart prompt was not seen in a player view) |
| V-9 | pass at 30/60 for the scripted case; absent when no one is on the tile |
| V-10 | pass in self-consistency; D-A shows the picture can contradict the true position |
| V-11 | pass 30/60 (`gPg`, only one entry in the on-you line, "shown left") |
| V-12 | pass for a grub truly on the tile; D-B for the room 2 case |
| V-13 | pass for grub hits (every line has a position); shot hit line not seen in a player view |
| V-14 | pass for the scripted left/right case at both rates; general sentence fails at 30 in room 2 (D-C) |
| V-15 | **fail** (D-D) |
| V-16 | **fail** (D-A, D-C) |
| V-17 | pass 30/60: on-tile grub defeated, and a dash off the tile (`dashoff`): the next draw has no entry and no displaced glyph |

### 4. Strike at 30 FPS (the open point D-58-1)

Observed first-hand. A swipe at 0.52 s and 0.53 s (processed at the first Strike tick, 0.567) hits the grub, cancels the strike and costs no heart. A swipe at 0.50 s hits it in its last Wind-up tick. A swipe after the damage tick (0.55 s) is "stunned", because the 0.15 s stun covers the rest of the 0.15 s Strike. In practice the cancel window is one tick (0.033 s at 30 FPS, 0.017–0.033 s at 60 FPS). That matches the written rule, but the designer may want to know it is this narrow.

### 5. Reference data from the balance bots (no balance judgement)

The script grammar needed was `fps N` and optionally `rooms N`. `room 1` is rejected ("cannot read"). The default is 60 FPS. Cells are clear time, hearts lost, attacks, dashes.

**60 FPS**

| Bot | Room 1 | Room 2 | Room 3 | Room 4 | Room 5 | Total |
|---|---|---|---|---|---|---|
| camper | 3.5 s, 0, 6, 0 | 4.5 s, 0, 6, 0 | NOT cleared 5.5 s, 3 lost (shots), 0, 0 | NOT cleared 6.9 s, 3 lost (shots), 4, 0 | NOT cleared 6.9 s, 3 lost (shots), 6, 0 | 2/5, 9 hearts, 0 dashes |
| walker | 3.5 s, 0, 6, 0 | 5.1 s, 0, 8, 0 | 9.0 s, 0, 6, 0 | 9.1 s, 0, 8, 0 | 11.2 s, 0, 10, 0 | 5/5, 0, 0 |
| dodger | 3.5 s, 0, 6, 0 | 5.1 s, 0, 8, 0 | 11.8 s, 0, 6, 4 | 10.0 s, 0, 8, 1 | 9.8 s, 0, 10, 2 | 5/5, 0, 7 |
| reactive | 3.5 s, 0, 6, 0 | 6.7 s, 0, 9, 2 | 11.8 s, 0, 6, 4 | 12.9 s, 0, 9, 5 | 11.1 s, 0, 11, 2 | 5/5, 0, 13 |

**30 FPS**

| Bot | Room 1 | Room 2 | Room 3 | Room 4 | Room 5 | Total |
|---|---|---|---|---|---|---|
| camper | 3.5 s, 0, 6, 0 | 4.5 s, 0, 6, 0 | NOT cleared 5.5 s, 3 lost (shots), 0, 0 | NOT cleared 6.9 s, 3 lost (shots), 4, 0 | NOT cleared 6.9 s, 3 lost (shots), 6, 0 | 2/5, 9 hearts, 0 dashes |
| walker | 3.5 s, 0, 6, 0 | 4.8 s, 0, 8, 0 | 9.2 s, 0, 6, 0 | 9.1 s, 0, 8, 0 | 12.3 s, 0, 10, 0 | 5/5, 0, 0 |
| dodger | 3.5 s, 0, 6, 0 | 4.8 s, 0, 8, 0 | 9.5 s, 0, 6, 2 | 10.1 s, 0, 8, 1 | 14.5 s, 0, 10, 6 | 5/5, 0, 9 |
| reactive | 3.5 s, 0, 6, 0 | 4.8 s, 0, 8, 0 | 9.5 s, 0, 6, 2 | 14.3 s, 0, 8, 6 | 11.1 s, 0, 10, 2 | 5/5, 0, 10 |

Idle-player reference (down time, a still player):

| Room | 30 FPS | 60 FPS |
|---|---|---|
| room 1 | about 3.93 s | about 3.90 s |
| room 2 | 5.27 s | 5.25 s |
| room 5 | 4.60 s | 4.57 s |

### 6. Could not observe

- Anything needing the Owner's suite run: the two `ManualTest` tests (AC-15) and any test that reads `manual.md`. Also the source of `test_hit_stun_is_short`.
- Not run this round: AC-1 (distance 4), AC-3 (dash away in wind-up), AC-9, AC-10, AC-12, AC-28(c).
- Not run this round: real-room clear with heal and next-room load (AC-14), "run complete", the run-over screen text, and the attack-restart (AC-13, V-8).
- No spitter player-view runs this round (V-2 charge/projectile draws, V-4 `s/z/S/Z`, V-7, shot hit line).
- Colors (V-6) are not assessable in the text view.
- Engagement cap at every tick (only trace samples at events and the 0.5 s draws were read).

### 7. Failed before?

From this packet alone: AC-15 failed once before on the line-wrap in `run over` (D-009) and was then settled by the Owner's run (D-010). I cannot confirm the earlier history of any other criterion, since the earlier reports are not in my packet. AC-19…AC-28 are new this round. The Studio should check the loop count for AC-17, AC-22, V-14 and V-16 against the earlier reports before routing.

## Decisions already made

- D-001: one attack button plus dash. No new inputs.
- D-009: the manual phrase check ignores line wraps.
- D-010: AC-15 passed on the Owner's run (40/40) for the earlier build. It does not cover the current 63-test suite.
- D-011: grubs take turns, crowd two deep; hit-stun 0.15 s; body hit; dash sets facing.
- D-012: `on you:` line; hit lines name the attacker position.
- D-013: knockback of an on-tile grub toward its display side.

## Constraints

- Do not edit `manual.md`. The Owner places the draft text.
- No production changes by QA. All findings go to the engineer or designer.
- A criterion failing a second time goes to `technical-director` (check the loop counts in §7).
- Must play correctly at both 30 and 60 FPS. D-A, D-C and the suite failure are the reasons this fails.

## Open questions

1. **To `gameplay-engineer`:** why does `CrowdTest.test_hit_stun_is_short` fail at both frame rates when the traces show the rule correct? Is the test or the build wrong? Fix D-A (display side and cell at the half-tile boundary) so that the 30 and 60 FPS views match.
2. **To `game-designer` (spec gaps):**
   - Does "on you" in text lines and the hit line mean true-position same tile, or same drawn cell (D-B)?
   - Should the hit-line word come from the position at the damage tick, or from the glyph position in the draw before the hit (D-C)?
   - How do cells round at exactly .5 tile (D-A)?
3. **To the Owner:** run `python3 -m unittest discover -s tests` in `repo/` with the unchanged `manual.md` beside it and report counts and any failure by name (AC-15). Place the V-15 draft text in `manual.md`; QA will then recheck V-15.

## Expected output

The Studio composes the next step from this report. Route the failures to `gameplay-engineer` (suite failure, D-A, D-C) and `game-designer` (D-B and the position-word definitions). Route the manual text and the suite rerun to the Owner. After the fixes, QA re-verifies AC-17, AC-22, AC-28(b), V-10, V-14, V-15, V-16 at both frame rates, plus the "not observed" list in §6.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md, design/combat.md, design/combat-visuals.md, manual.md, repo/ (build: run commands in project.md)
- Decisions: decisions/D-009-manualtest-phrase-check-ignores-line-wraps.md, decisions/D-010-owner-ran-suite-ac15-passes.md, decisions/D-011-grub-turns-stun-body-hit-dash-facing.md, decisions/D-012-on-you-line-for-displaced-enemies.md, decisions/D-013-knockback-of-grub-on-players-tile.md
- Previous handoff: goals/G-001-combat-monotony/68-studio-to-qa.md
>>>END

<<<FILE goals/G-001-combat-monotony/71-art-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 71
from: art-director
to: studio
stage: Verify
outcome: question
---
# 71: art-director → studio — Visual review of the combat view could not be done first-hand; only V-15 is judged (fail)

## Task

Hand back the visual review of V-9…V-17. The packet gave me no way to run `play.py` and no `repo/`, so I saw no live frame, plain or color. I judged only what the packet shows: `manual.md` against V-5, V-8 and V-15. Please re-route the review to an executor that can run `python3 play.py --view player {script}` in `repo/`.

## Context

G-001, Option A (D-002). Handoff 69 asked for a per-item verdict on V-9…V-17 with V-1…V-8 as regression, and a clear split between what I saw and what I inferred. I could not see anything first-hand, so I will not mark any item pass or fail from the view. A verdict from code or spec text alone would be a guess, and the two points earlier rounds could not see (the reverse-video cell in color mode and the `on you:` line in a live frame) are exactly what cannot be inferred.

## Findings

**Seen first-hand: nothing.** No frame was run.

**Read from `manual.md` (document only, not the build):**

| Item | Verdict | Basis |
|---|---|---|
| V-15 | **FAIL** | `manual.md#on-screen` does not list the `on you:` line and does not say that a letter beside `P` named on that line is on the player's tile. It says the displaced enemy is "drawn on a free tile next to you, so you can always see it", which is the reading the playtesters got wrong. `manual.md#what-you-hear-and-read` has "the grub is open" with no position word, no `YOU ARE HIT by a grub (<position>)` line, no spit-shot hit line, no "(on you)" and no list of position words. |
| V-5 | Pass on the document | `x`, the arc characters and the glyph table are all listed in `#on-screen`. Not checked against the build. |
| V-8 | Pass on the document | The restart prompt is documented ("run over — rooms cleared: N", "press attack to start again"). Not checked against the build. |

**Not assessed (need a live run):** V-1 to V-4, V-6, V-7, V-9 to V-14, V-16, V-17. This includes whether the reverse-video cell reads against the dark background and keeps the orange/red threat colors.

**Owner-placed text (D-005, D-007):** I do not edit `manual.md`. For the Owner, a proposal that follows V-15:
- In `#on-screen`: "When an enemy is on your tile, a line `on you:` appears under the hearts, for example `on you: G biting soon (shown right)`. The letter beside `P` that this line names is on your tile, not on that side. In color it also has an inverse cell." Replace "so you can always see it" so it no longer implies the drawn side is the real position.
- In `#what-you-hear-and-read`: add the position words (`on you`, `left`, `right`, `above`, `below`, `top left`, `top right`, `bottom left`, `bottom right`, plus the distance form when two same-type enemies would read alike), "the grub is open (left)", "(on you)", `YOU ARE HIT by a grub (left)` and `YOU ARE HIT by a spit shot from spitter (top right)`.

## Decisions already made

- D-001: no new inputs.
- D-006: overlap is a display offset only; enemies are never hidden.
- D-012: `on you:` line and attacker position in hit lines.

## Constraints

- I review and specify only. I did not edit the repo or `manual.md`.
- No visual rule changed. V-15's text is an Owner placement.

## Open questions

- **For the Studio:** Re-route the live visual review with `repo/` access. It needs these setups at `fps 30` and `fps 60`, in the plain view and in a color run:
  1. `room empty`, `player 8 4`, `spawn grub 8 4`, then attacks. Check V-9, V-10, V-12, V-17 and the reverse-video cell.
  2. A grub on the player's tile plus one to its right. Check V-11.
  3. A grub on each side with only one striking. Check V-14.
  4. A spitter shot hitting the player. Check V-13.
  5. Room 2 with four grubs around the player. Check that the new lines do not push the praised ones off screen.
  6. A swipe that misses too far away and one that misses with the enemy not in front.
- **For the Owner:** place the V-15 text (proposal above), or confirm that it is deferred.

## Expected output

The Studio re-routes the visual review to an executor that can run the build, and routes the V-15 text to the Owner. I will then give a per-item pass/fail with first-hand evidence.

## Sender assessment

Confidence is high that V-15 fails on the document. I have no confidence either way on V-9 to V-14, V-16, V-17 or the color view, because nothing was run. The packet-only V-5 and V-8 passes do not show that the build matches the manual.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md
- Project: project.md#art-direction, design/combat-visuals.md, manual.md, repo/
- Decisions: decisions/D-006-overlap-display-and-practice-room-manual.md, decisions/D-012-on-you-line-for-displaced-enemies.md
- Previous handoff: goals/G-001-combat-monotony/69-studio-to-art-director.md
>>>END
