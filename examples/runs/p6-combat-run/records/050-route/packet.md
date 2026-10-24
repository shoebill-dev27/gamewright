# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/44-art-director-to-studio.md, goals/G-001-combat-monotony/45-game-designer-to-studio.md
next_seq: 46
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha e2755991a5e9; run through the project's run commands)
log: last 5 of 18 entries in @log-recent; the full history is goals/G-001-combat-monotony/log.md

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/44-art-director-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/45-game-designer-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 46
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
- Design: done (10, 16, 33). Spec `design/combat.md` (AC-1…AC-18), D-003, D-006, `design/combat-visuals.md` (V-1…V-8). Reopened for one question (7j, below).
- Plan: done (14, D-004). Gap defaults F1–F11; the designer confirms them at Review, F1 (grub speed) matters most.
- Build: done (code 18, 22, 23, 35; render fix F1/AC-18 and F3; manual paragraph placed by the Owner, D-007). F2 is cosmetic.
- Verify, behavior: 7g (39) passed. AC-17 (30/60 FPS) and AC-18 hold, C1/C7/C3 unchanged, no AC failing. Suite-only: AC-14, AC-10 2-swipe kill, "(too soon)" and "(down)" lines. Pause (F11) not implemented.
- Verify, AC-15: paragraph identical to D-007 and behavior matching (40). The Owner ran the suite (D-008): 39/40 pass. `test_manual_lists_glyphs_and_lines` fails, `'run over'` not found in `manual.md` text (`tests/test_game.py` line 631). `test_on_screen_section_lists_x_and_the_practice_room` passes. AC-15 is open until the designer rules (7j): is the manual missing the phrase, or is the test's expectation wrong?
- Verify, visuals: earlier V-1 fail (hidden grub), F3. 7h re-judges V-1, V-2, V-6 and the displaced cell from QA's captures (39, 40). No `--color` capture is obtainable with the project commands, so V-6 may stay unobserved. Not observed: a swipe while an enemy is drawn beside the player.
- Play: `playtester`, live and reactive, from a Handoff composed by the Studio from permitted information. Watch slot starvation. Planned, after Verify passes (including AC-15).
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
| 7g | Verify (all but AC-15) | qa | verify-change | done (pass) | 37-studio-to-qa.md |
| 7i | Verify (AC-15, `ManualTest`) | qa | verify-change | done (question: ManualTest blocked) | 38-studio-to-qa.md |
| 7i-O | Owner: `ManualTest` result | owner | — | done (Option A, D-008: 39/40) | 42-studio-to-owner.md |
| 7h | Verify (visuals) | art-director | visual-review | open (parallel to 7j) | 41-studio-to-art-director.md |
| 7j | Design (`run over` manual test failure) | game-designer | write-design-spec | open | 43-studio-to-game-designer.md |
| 7k | Build (fix test or code) | gameplay-engineer | implement-change | tentative (if the ruling changes test or code) | — |
| 7k-O | Owner: place manual text | owner | — | tentative (if the ruling changes `manual.md`) | — |
| 7l | Verify (AC-15 rerun) | qa | verify-change | tentative (after 7k or 7k-O) | — |
| 8 | Play | playtester | playtest-session | planned | — |
| 9 | Review | game-director | review-outcome | planned | — |

## Route changes

After the Owner chose A (42, D-008): the suite ran 39/40; `ManualTest` fails on the phrase `run over` missing from `manual.md`. Goal back to `active`. 7j opens (43): the designer rules on manual vs. test. 7k, 7k-O and 7l are tentative on that ruling. 7h continues; Play waits for AC-15.

## Next action

- Run `43-studio-to-game-designer.md` (7j; result addressed to `studio`).
- Run `41-studio-to-art-director.md` (7h; result addressed to `studio`), in parallel.
- Then Route: apply 7j's ruling (test or code fix to Build; a manual change goes to the Owner, never edited by a Role), then a QA rerun of AC-15. When AC-15 and 7h both pass, open Play (8) with a Handoff composed from permitted information only.

## Outcome

(Filled at Close.)
>>>END

<<<FILE @log-recent
## 038-route · 2026-10-15

Status: active. Open: 34-studio-to-gameplay-engineer.md.

After 7d/7e (32 fail on V-1, 33 done): the designer allowed overlap but never hidden (D-006, AC-18) and reworded AC-15, so Build reopens as 7f (34), with the art director's F3 (enemy over arc). 7g (QA) and 7h (art director) are now planned after it; F2 stays cosmetic.

## 040-route · 2026-10-15

Status: blocked-on-owner. Open: 37-studio-to-qa.md.

After 7f (35, question): render fix built and tested; only the `manual.md` paragraph is missing, a third round with nothing new supplied, so it is escalated (36, Option A recommended). 7g (37) runs meanwhile without AC-15; 7i (AC-15) is tentative on the Owner's answer.

## 042-resume · 2026-10-15

Status: active. Open: 37-studio-to-qa.md, 38-studio-to-qa.md.

Resume after the Owner chose Option A (36, D-007): the Owner placed the manual paragraph. Goal back to `active`. 7i (AC-15, `ManualTest`) is confirmed and opened as 38 in parallel with 7g (37); 7h, Play and Review unchanged.

## 045-route · 2026-10-15

Status: blocked-on-owner. Open: 41-studio-to-art-director.md.

After 7g/7i (39 pass; 40 question): 7g passed, so 7h opens (41). 7i found the paragraph and behavior fine, but `ManualTest` cannot read `manual.md` in the QA workspace, the same missing input as in 29. Per the loop limit it goes to the Owner (42), not QA again. 7h runs meanwhile; Play waits for AC-15.

## 047-resume · 2026-10-15

Status: active. Open: 41-studio-to-art-director.md, 43-studio-to-game-designer.md.

After the Owner chose A (42, D-008): the suite ran 39/40; `ManualTest` fails on the phrase `run over` missing from `manual.md`. Goal back to `active`. 7j opens (43): the designer rules on manual vs. test. 7k, 7k-O and 7l are tentative on that ruling. 7h continues; Play waits for AC-15.
>>>END

<<<FILE goals/G-001-combat-monotony/44-art-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 44
from: art-director
to: studio
stage: Verify
outcome: pass
---
# 44: art-director → studio — visual re-review of build 0.5: V-1, V-2 and the displaced cell pass; V-6 passes from code, not observed; V-5 and V-7 are not judged

## Task

Report the visual review requested in handoff 41. It covers V-1…V-8 against QA's captures (39, 40), `repo/play.py` read-only for color, and D-006. Per criterion: pass, fail or not observable, with the gaps named.

## Context

My earlier review (32) failed V-1 (a grub hidden under the player) and found F3 (an enemy drawn over the swipe arc). Build then added the display offset (D-006, AC-18). I did not edit the build or `manual.md`. The evidence is QA's text captures (39 section 2 and section 4, 40) plus a read of `repo/play.py`. Nothing here was seen in a real color terminal.

## Findings

### Verdict per criterion

| Criterion | Result | Evidence |
|---|---|---|
| **V-1** committed = uppercase, harmless = lowercase | **pass** (observed) | Grub on the player's tile: wind-up `PG`, strike `PG`, recovery `Pg`, down `xg` (39 §2, C1 at 30 and 60 FPS). Damaged grub: `PW` in wind-up, `Pw` in recovery (C2). Spitter on the tile: `Ps` idle, `PS` charging, `Ps` after the spit (30 and 60 FPS). Two enemies: `sPg`, `SPg`, `SPG`, `sxg`. Three grubs: `G` left, `g` right, `g` above. In none of these is an enemy hidden. The reported cases cover exactly the hidden-grub failure from 32. The practice-room run in 40 is consistent. |
| **V-2** own draw at wind-up start, charge start and each swipe, at 30 and 60 FPS | **pass** (observed) | Wind-up: `sPG` at 0.033 (30 FPS) and 0.017 (60 FPS), drawn with the "rears back" line. Charge: `PS` / `SPg` at 1.000 at both rates. Swipe: hit draw at 2.53 s (30 FPS) and 2.52 s (60 FPS); miss draw at 0.53 s and 0.52 s. Recovery: `Pg` at 3.60 s / 3.58 s. `SNAPSHOT_EVENTS` in the code lists all of these. |
| **V-3** uppercase visible before the first heart is lost | **pass** (observed) | `sPG` at 0.033 s with hearts 3/3 (two-enemy capture). The C1 first wind-up at 1.400 s is 0.5 s before the first hit at 1.967 s. |
| **V-4** full and damaged told apart by glyph | **pass for `g/w`, `G/W`, `s/S`**; `z/Z` from code only | `Pg`/`Pw` and `PG`/`PW` are captured. No damaged spitter is in the captures. `z` and `Z` exist in `GLYPHS` and are selected by the same rule as `w` and `W`. |
| **V-5** `x`, arc characters and glyph table listed in `manual.md#on-screen` | **not judged** | Not in my scope or loads. `manual.md` is missing from QA's workspace and `ManualTest` has no valid result (40). It stays with AC-15 and QA. |
| **V-6** only telegraphed enemy glyphs and `*` are saturated orange/red | **pass, from code, not observed** | In `play.py`: `ALERT` (`1;38;5;202`) is used only for `grub_alert`, `grub_hurt_alert`, `spitter_alert` and `spitter_hurt_alert`. `SHOT` (`1;38;5;196`) is used only for `*`. The player and the arc use `LANTERN` (229). The downed player uses `GRAY_BLUE` (67). Harmless enemies use `MUTED` (245), and damaged harmless ones use `MUTED_TINT` (137, a desaturated tan). Colors are applied only through `paint()`, and text lines are uncolored. No real color output was seen. How codes 202 and 137 look depends on the terminal palette. |
| **V-7** the two spitters can be told apart | **not observable this round** | No capture has two spitters (rooms 3–5). The captures with one spitter show "spitter (center) charges". The code adds a number when names are duplicated. I did not judge it. It is unchanged by the rendering fix, and my earlier review (32) is not in this packet. |
| **V-8** run-over screen shows the restart prompt | **pass from code, not observed** | `LINES["run_over"]` plus `LINES["restart"]` are printed together, and no map is drawn in phase "over". The captures in 39 and 40 record the run-over timestamps but do not quote the prompt text. |

### F3 (enemy over the swipe arc): resolved

In the hit draw (C3, C2) the arc `)` is on the tiles above and below, and the enemy's own cell shows `Pw` with the glyph, not the arc. The miss draw shows `)` / `P)` / `)`. In the code, the arc fills only empty cells, so an enemy or `P` always wins its cell.

### The displaced cell: readable, passes

- **Single enemy on the player's cell.** It sits directly beside `P` (`Pg`, `PG`, `Ps`, `PS`) and always in the same cell. It is consistent with the text lines ("(on you)").
- **Two or three enemies.** They are on different sides, and the uppercase one is the one named in the line. For example, "rears back (left)" has `G` on the left in the three-grub capture. The case is readable.
- **Placement preference.** QA did not check the "side it last came from" preference, because each capture had one grub on its own side. From the code, it is the first preference (`last_side`), then right, left, above, below. For a grub that has just lunged past `P`, the glyph will normally stay on the side it came from, which is the least surprising. I accept this as readable. The risk I see is not legibility but a mismatch of side. A swipe hits by true position, so the arc may point away from the displaced glyph, and a hit may still be reported. D-006 and combat.md already state this ("a swipe may hit an enemy drawn on a different side than the arc") and the manual paragraph says only "drawn on a free tile next to you". That is acceptable for now. It is D-006's own revisit trigger if Play shows the glyph is misread as a true position.
- **Down.** `xg` and `sxg` read clearly: `x` is cold gray-blue and the enemy stays beside it.

### F2: unchanged

F2 itself is not in this packet, and I have nothing new that would change its rating. It stays cosmetic.

### New cosmetic note, F4 (does not fail any V-criterion)

In `snapshot()` the projectile `*` is drawn first, then the enemies, then `P`. A projectile in the same cell as an enemy or `P` is hidden under that glyph. The spitter-on-the-tile capture shows this: the spit draw at 1.800 is `Ps` with no `*`, and the hit lands at 1.833 (39 §2). The 0.8 s charge `PS` is the telegraph in this case, so the player is not left without a warning. It matters only when a spitter is on the player's tile or when a shot crosses another enemy's cell. The visuals spec says `*` is "visible from spawn to removal". I propose Build may draw `*` above enemy glyphs and below `P`. It is optional and does not block acceptance.

## Decisions already made

- D-006: enemies may overlap the player but are never hidden; the practice room is listed in On screen. My review confirms the display part. The D-006 "Revisit when" condition (a misread displaced glyph) is not triggered by anything I can see.
- D-001: no new inputs.

## Constraints

- I judged only the captures and the read-only files. V-6 is marked "from code, not observed". I did not edit the build or `manual.md`.

## Open questions

Answers to the three questions in handoff 41:

1. **V-1, V-2, the displaced cell:** pass (observed). **V-6:** pass from code, not observed. Other criteria are in the table above (V-3, V-4, V-8 pass; V-5 and V-7 are not judged).
2. **Swipe plus displaced glyph capture:** not needed for my verdict. The code makes the enemy glyph win its cell over the arc, as in the captured `Pw` between `)` and `)`. It is safe to leave to Play, and cheap if QA has a spare round. The script would be `room empty`, `fps 30` and `fps 60`, `player 8 4`, `spawn grub 8.2 4`, an `attack` input when the log says "the grub is open (on you)" (about 3.6 s as in C1), and `end` a little later. One thing to watch there is whether a swipe at a grub on the tile reports a hit while the arc points away from the displaced glyph. That is a rules question, not a rendering one. If it reports "(miss)" with a grub under `P`, route it to `game-designer`, not to Build.
3. **`--color` capture:** not required to close V-6. The code paths are unambiguous. If the Studio wants the evidence, ask the Owner to run the following in a terminal and send the raw files with the escape codes, for example captured with `> file.txt`:
   - `python3 play.py --color --view player` on the C1 script (`room empty`, `player 8 4`, `spawn grub 12 4`, `end 8`).
   - The same on a spitter script (`player 8 4`, `spawn spitter 12 4`, `end 4`) so that `S` and `*` appear.
   - The same on the miss script, for the arc.

   I would check that `G`, `W`, `S`, `Z` and `*` carry only the 202 and 196 codes and that everything else uses 229, 67, 245 or 137. A terminal screenshot of one run would also show whether 245 (harmless) and 202 (alert) differ enough in the Owner's palette. That is the only thing the code cannot tell me.

## Expected output

The Studio can accept the rendering change from the art-director side for V-1, V-2, V-3, V-4 and V-8 (V-4 `z/Z` and V-8 from code). V-6 is accepted from code, pending the optional color capture. V-5 stays with AC-15 and QA until `manual.md` is in the run workspace. V-7 stays open for Play or a short QA capture of room 4 (two spitters, any frame rate). F4 may go to Build as optional polish.

## Sender assessment

Confidence is high for V-1, V-2 and the displaced cell, because the captures show every state at both frame rates. It is medium for V-6, because it rests on reading the code. It is low for V-7, because there is no evidence this round. I see no fail to route to Build.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md
- Project: design/combat-visuals.md; design/combat.md (AC-18 only); project.md#art-direction; repo/play.py (read-only, V-6 only)
- Decisions: decisions/D-006-overlap-display-and-practice-room-manual.md
- Previous handoff: goals/G-001-combat-monotony/41-studio-to-art-director.md
>>>END

<<<FILE goals/G-001-combat-monotony/45-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 45
from: game-designer
to: studio
stage: Design
outcome: done
---
# 45: game-designer → studio — ruling on `run over`: the manual is right, the test is too literal (fix b)

## Task

Ruling on why `test_manual_lists_glyphs_and_lines` fails, and which fix applies.

## Context

Owner's run (D-008): 39 of 40 pass. The failure is `'run over' not found in manual.md` at `tests/test_game.py` line 631.

## Findings

**Cause.** `manual.md` does contain the run-end text, but a hard line wrap splits the phrase. In "Rooms and runs":

```
- At zero hearts you are down: ... A moment later the screen reads "run
  over — rooms cleared: N" and "press attack to start again". ...
```

The text is `run`, then a newline and two spaces, then `over`. The test does a plain `assertIn("run over", text)`, which cannot match across a line break. This is a test that is too literal about Markdown line wrapping. It is not a manual content gap and not a build wording problem.

**Q1. Is `run over` shown to the player, and does the manual mention it?**
- Yes. `play.py` prints `run over — rooms cleared: {rooms}` (`LINES["run_over"]`), followed by `press attack to start again`.
- The manual quotes both lines, with the same wording and the same dash. D-003 and AC-13 are matched.
- Nothing about the run end is missing from the manual.

**Q2. Full phrase list and which are missing.** The test first checks every `play.GLYPHS` character in backticks. Then it checks these phrases:

| Phrase | In `manual.md`? |
|---|---|
| `room empty` | yes (Script table, practice-room text) |
| `rears back` | yes ("a grub rears back (left)") |
| `is open` | yes ("the grub is open") |
| `charges` | yes |
| `spits` | yes |
| `run over` | **no as a literal string**: split by a line break after `run` |
| `press attack to start again` | yes, on one line |
| `(miss)` | yes |
| `(too soon)` | yes |
| `(stunned)` | yes |
| `(down)` | yes |
| `room cleared` | yes ("room cleared" in quotes, one line) |

- The glyph loop runs before the phrase loop and did not fail. Every glyph is present in backticks, including the swipe marks `)` `(` `^` `v`, as the table shows.
- `run over` is the only missing phrase. The test stops at the first failure, but my reading of the manual shows no other phrase missing.
- The list is not stricter than AC-15 requires. It checks that the manual names the glyphs and the lines the player sees, which is what AC-15 and V-5 intend.

**Q3. Chosen fix: (b).** The manual needs no change, and the Owner does not have to place anything.

Change for the Engineer, in `ManualTest.test_manual_lists_glyphs_and_lines` only:

```python
text = MANUAL.read_text(encoding="utf-8")
flat = " ".join(text.split())   # a hard-wrapped Markdown line must not hide a phrase
for key, (char, _) in play.GLYPHS.items():
    self.assertIn(f"`{char}`", text, key)
for phrase in (...same list, unchanged...):
    self.assertIn(phrase, flat, phrase)
```

- Only the phrase check uses the whitespace-collapsed `flat`. The glyph check keeps `text`.
- Do not change the phrase list. Do not touch `test_on_screen_section_lists_x_and_the_practice_room`; its strings are on single lines.
- Do not change any code or build wording.

Why (b) over (a): the manual reads correctly, and hard-wrapping is normal for Markdown. Changing the test removes a fragile dependency on where the Owner or a later editor wraps lines. With (a), a one-character Owner edit would fix this run, but the same break could reappear on any rewrap. (c) is unnecessary because the build wording already matches the manual.

**Acceptance check.**
1. The Engineer applies the test change above (Build).
2. Run the full suite, `python3 -m unittest discover -s tests`, in an environment where the **unchanged** `manual.md` sits next to `repo/`. The expected result is 40/40.
3. QA cannot run it in its own workspace because `manual.md` is absent there (29, 40). Either:
   - the Owner (or their stand-in) reruns it as in D-008 and reports the result, or
   - the Owner places the current `manual.md` beside `repo/` in the QA workspace, and QA runs `ManualTest` and the full suite.
4. QA also confirms that `manual.md` still contains the D-007 paragraph and the "Rooms and runs" text above, with no edits. AC-15 passes only on 40/40.

If the rerun fails on some other phrase, read the new failure message and rule on it from this table.

No change to `design/combat.md`. AC-15 already requires `x` and the practice room in `manual.md#on-screen`, and the test does not check beyond it. The ruling is recorded in D-009. No change to D-001, D-003, or the pillars.

## Decisions already made

D-003, D-005, D-006, D-007, D-008 (all respected; `manual.md` is not edited).

## Constraints

Do not edit `manual.md`. The Engineer edits only the one test method.

## Open questions

None.

## Expected output

Studio routes the test change to `gameplay-engineer` (Build). After that, the Owner or QA runs the suite as in point 3 above and reports the 40/40 result (Verify, AC-15).

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat.md; manual.md; repo/tests/test_game.py
- Decisions: decisions/D-009-manualtest-phrase-check-ignores-line-wraps.md
- Previous handoff: goals/G-001-combat-monotony/43-studio-to-game-designer.md
>>>END
