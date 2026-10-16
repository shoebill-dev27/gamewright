# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/30-game-designer-to-studio.md, goals/G-001-combat-monotony/31-game-designer-to-studio.md, goals/G-001-combat-monotony/32-qa-to-studio.md
next_seq: 33
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha 29993eac7bb0; run through the project's run commands)
log: last 5 of 11 entries in @log-recent; the full history is goals/G-001-combat-monotony/log.md

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/30-game-designer-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/31-game-designer-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/32-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 33
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

- Observe: done (scripted play, rooms 1–3 + practice room; 02). FPS divergence (qa): done (16, 20); walker 30/60 differences are bot timing, the contact-edge graze is accepted (D-002).
- Diagnose: first pass done (04). Second pass open (28): the fresh playtest (27) found melee enemies share one answer (sidestep, then swipe), the dash is never needed against melee, brutes are not worth fighting, and spitter crossfire in rooms 4–5 is repetitive or unreadable. Scripted play, single runs and cut-off rooms 2–3 limit the evidence.
- Observe (possible defect, qa): open (29). Room 2, grub hit about 0.1 s after a lunge-cancelling swipe; may be a second grub.
- Decide: skipped so far. Tentative: needed if the second Diagnose implies a new enemy type, healing, new input or a scope or priority change.
- Design: done (14, 22). 9b (26: exact-reach miss at 0.40, lunge band in D-002) is open and non-blocking. Tentative: new design if Diagnose or Decide calls for it.
- Plan: skipped (approach reuses the enemy update loop). Returns if the same criterion fails verification twice.
- Build: 0.5 done (10, 18). Tentative: only if new design or a confirmed defect requires it.
- Verify (QA): criteria 1–17 pass at 30 and 60 FPS (24). Verify (visual): done (15); V1–V11 need a graphical build, become a proposed new Goal at Close; V12 open until a graphical build exists.
- Play: first pass done (27). Tentative second pass after any new Build.
- Manual wording ("no more than 3 in the air") is true in rooms 1–5 only. Optional fix, raise at Close.
- Review: planned (`game-director`), experience Goal. The first Play indicates the Goal is not yet met.

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
| 9b | Design (QA notes: exact-reach miss, lunge band) | game-designer | write-design-spec | open | 26-studio-to-game-designer.md |
| 10a | Diagnose (playtest issues 1–4) | game-designer | diagnose-experience | open | 28-studio-to-game-designer.md |
| 10b | Observe (room 2 grub hit after swipe) | qa | reproduce-defect | open | 29-studio-to-qa.md |
| 11 | Decide (if Diagnose implies direction or scope change) | game-director | make-decision | tentative | — |
| 12a | Design (per Diagnose or Decide) | game-designer | write-design-spec | tentative | — |
| 12b | Build (design or confirmed defect) | gameplay-engineer | implement-change | tentative | — |
| 12c | Verify (after any Build) | qa | verify-change | tentative | — |
| 12d | Play (after any Build) | playtester | playtest-session | tentative | — |
| 13 | Review | game-director | review-outcome | planned | — |
| 14 | Next | studio | — | planned | — |

## Route changes

After 9a (Play): does not fit "goal met". The playtest reports remaining monotony (melee enemies share one answer, dash unused, spitter crossfire) and one possible defect. Returned to Diagnose (10a, designer) and Observe (10b, qa) in parallel with open 9b. Decide, Design, Build, Verify and Play are tentative on the Diagnose result.

## Next action

Run the game-designer step with 28-studio-to-game-designer.md, the qa step with 29-studio-to-qa.md, and the still-open 26-studio-to-game-designer.md; they are independent. Then Route: wait for all three. If the Diagnose implies a direction, scope or priority change, open Decide (`game-director`); if QA confirms a defect, open Build with the report; otherwise proceed to Design as the diagnosis calls for. If Diagnose is re-entered again without measurable progress, the `game-director` reviews (loop limit).

## Outcome

(open)
>>>END

<<<FILE @log-recent
## 016-route · 2026-10-16

Status: active. Open: 19-studio-to-qa.md.

After 7d: the engineer reports log-only changes with byte-identical log-off output, so the plan holds. Opened Verify (QA, criteria 1–16 + V12, incl. 16e from the new log) with a Handoff that omits the engineer's assessment. 8b stays tentative on the 16e result.

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
>>>END

<<<FILE goals/G-001-combat-monotony/30-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 30
from: game-designer
to: studio
stage: Design
outcome: done
---
# 30: game-designer → studio — Both spec rulings made as wording only; no Build and no re-Verify needed

## Task

Report my rulings on the two points from QA's close-out verification (handoff 24, section D) and the files changed. Route onward: the playtest is not affected.

## Context

G-001 (combat monotony). Build 0.5 passed QA against criteria 1–17 at 30 and 60 FPS. The build is unchanged. Handoff 26 asked for two small rulings on the contact-edge graze accepted in D-002.

## Findings

### Ruling 1: a shot at exactly the reach (0.400)

- **A miss of exactly the reach is inside the band.** Either result is accepted at either rate, and 30 and 60 FPS may differ. It is not a guaranteed miss.
- This keeps `distance <= reach` in the build. QA's observation (hit at 30 FPS, miss at 60 FPS for a nominal 0.400) is correct behavior under the clarified spec and is not a failure of 17b.
- The same rule applies to lunges at exactly 0.600.
- Spec wording in `design/combat.md`, with no number changed:
  - The band is now more than reach − tolerance and up to and including the reach: more than 0.39 to 0.40 for shots, more than 0.57 to 0.60 for lunges. This removes the overlap at 0.39 and 0.57 and the gap at the reach.
  - 17a: 0.39 or less hits at both rates (as before).
  - 17b: "more than 0.40" (was "0.40 or more") misses at both rates.
  - 17c: lunge 0.57 or less hits at both rates; more than 0.60 misses at both rates (was "0.60 or more").
  - 17d: the band includes exactly the reach; the sampling rule, 16e and the edge cases are aligned.
- Every case QA verified (shots 0.390 hit and 0.407 miss; lunges 0.570 hit and 0.610 miss) is still covered with the same result. Those criteria remain valid.

### Ruling 2: lunge band width

- The measured figures are recorded: a guaranteed hit up to about 0.585 at 30 FPS, a band of about 0.015 tile at 30 FPS and about 0.004 tile at 60 FPS.
- **Limitation, stated in the files:** five probes only, not a full scan. The rates disagreed only at 0.590. There is no evidence of a band wider than 0.03 tile, which is the threshold that triggers a report back to the designer. The shot figure of about 0.003 tile is derived, not scanned.
- Recorded in `design/combat.md` (sampling rule, replacing "not yet run") and in the new Decision D-003.

### Where it is recorded

- I did not edit D-002, because it is not on my write list for this step. The ruling is a short follow-up Decision, **D-003**, which refines D-002 and does not supersede it. D-002 still says "derived, not yet run" for the lunge band, and D-003 carries the measured figures. Studio: if you want D-002's text brought in line, route that edit separately. It is not needed for correctness.
- Files changed: `design/combat.md` and `decisions/D-003-contact-edge-exact-reach-and-lunge-band.md` (new).

## Decisions already made

- D-001: one attack button plus dash; no new input.
- D-002: per-frame contact sampling is kept; the graze is an accepted limitation.
- D-003 (new): exactly the reach is inside the band; measured lunge band recorded.

## Constraints

- Wording clarifications only. No parameter, tolerance or other criterion was reopened.
- The `manual.md` sentence "no more than 3 are in the air at once" (QA's note in handoff 24, section B) is not a spec matter. Whether to say "in the five rooms" is a text edit for whoever owns the manual, and it does not affect the playtest.

## Open questions

None for the designer. If the Studio wants D-002 itself updated, that needs a role with it on its write list.

## Expected output

- **Build needed: no.** `distance <= reach` is kept.
- **Re-Verify needed: no.** The change is wording only, and every tested value keeps its verified result. The one-off case QA flagged (nominal 0.400) is now in the accepted band, so there is nothing left to re-check.
- The playtest can proceed as planned. Nothing here is for the Playtester's handoff.

## Sender assessment

Confidence is high that no Build or re-Verify is needed. The only residual risk is that a future tester scripts a miss of exactly 0.400 or 0.600 and expects a fixed result. The spec now says explicitly that none is promised.

## Load

- Role: studio/roles/studio-routing.md
- Skills: none
- Project: design/combat.md
- Decisions: decisions/D-002-contact-edge-graze-accepted.md, decisions/D-003-contact-edge-exact-reach-and-lunge-band.md
- Previous handoff: goals/G-001-combat-monotony/26-studio-to-game-designer.md
>>>END

<<<FILE goals/G-001-combat-monotony/31-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 31
from: game-designer
to: studio
stage: Route
outcome: done
---
# 31: game-designer → studio — Second Diagnose: why combat still felt repetitive after build 0.5, with ranked options

## Task

Route this diagnosis. I recommend **no Decide step**. All options below are changes to variant parameters, one per-variant rule flag, per-room spitter timing and room contents. All use existing systems and stay inside D-001 and the pillars. The next step is Design (write-design-spec) for the options marked "do", then Build and QA. Two small side items for QA are listed at the end.

## Context

Goal G-001: the Owner finds combat monotonous. Diagnose 04 led to design 14/22, build 0.5 and QA criteria 1–17 passing. Handoff 27 is a fresh playtester report on rooms 1–5. This is the second Diagnose, so the focus is what 0.5 did and did not fix. I read 27 against `design/combat.md`. I ran no `play` or `bots` this step, because the evidence needed is a hand-timed human session, which scripts cannot give. My claims about timing come from the spec numbers.

## Findings

### 1. What 0.5 fixed and what it left (against 04)

| Symptom in 04 | Status after 0.5 (from 27) |
|---|---|
| Grubs trivial, no telegraph | **Fixed.** Warnings are consistently readable, and cancel and stagger on swipe "felt good". Ignoring the cue now costs hearts (room 1, timed script: three hits in under 3 s). |
| Spitter volleys unreadable | **Partly fixed.** A single aim line and glow are readable. In rooms 4–5, several threats at once are not (symptom 4 below). |
| Dash never needed | **Not fixed** for melee. The dash is still optional there. |
| Rooms 1–2 interchangeable | **Not fixed in play.** Contents differ, but the answer is the same ("sidestep on the warning, then swipe or ignore"). |

The 0.5 changes made threats readable, which was needed for pillar 3. They did not make enemies ask for different answers. Readability turned the grub into "see flash, move, hit".

### 2. Symptoms, causes, and design cause versus script artifact

**S1. Melee enemies share one answer (most important for the Goal).**
- **Design cause (supported by `combat.md`):** grub, runner and brute are one behavior (wind-up, lunge, recovery, same 1.2-tile lane, same 2.4-tile lunge, same cancel rule). The parameter sets change *how long you have* but not *what you do*. The wind-up cancel works the same on all three, and sidestepping the same 1.2-tile lane works the same on all three.
- **Runner: probably partly a script artifact.** The runner's wind-up is 0.35 s. The lane is 0.6 tile either side, so a player needs a sideways move of just over 0.6 tile, about 0.15 s at 4 tiles/s. A script with a fixed 0.15 s reaction finishes at about 0.30 s, just under 0.35 s. A human with 0.25 s reaction plus 0.15 s of movement needs about 0.40 s, which is **over** 0.35 s. For a human the runner is likely a real test, unless the player swipes it in the wind-up, which is a different answer from the standard grub. The playtester's finding "the runner's short warning never tested the player" is therefore not safe to use. It needs a human check.
- **Brute: design cause plus artifact.** The brute asks for the same dodge as the others, only slower, and dodging costs nothing. The playtester dodged for 20+ s and never fought it. The room does not clear until it dies (rule: a room ends when all enemies are defeated), so a human has a reason the scripted player did not apply. A human who tries to clear room 2 will end up fighting it. What the design lacks is a *different way* to fight it. The same swipe-cancel works, so "fight the brute" is "dodge, then swipe", as for any grub. The playtester's open question ("is the brute meant to be attacked?") shows the player was not told by the game that it must die.
- **Attention drop by the second grub (room 1):** a design cause shared with the rest of S1. Three identical grubs in one room mean three repeats of the same loop. It is also helped by the script's perfect play: a human who is hit once will have more variation.

**S2. The dash was never needed against melee. Low priority; mostly a consequence of S1.**
- Cause: a 1.2-tile lane is cleared by a 1-tile sidestep, which is cheaper than a dash (0.6 s cooldown). That is by design and the dash does its job against shots. I do not recommend forcing the dash into melee. For example, widening a lane to need a dash would break the visual spec ("lane geometry identical"), and would make the cue harder to read. Instead, the dash's job is to be the answer in crossfire (S4). The dash can also close a gap on a recovering enemy (dash toward, queued swipe), which is a valid use that the scripts never tried.
- Answer to the playtester's question: no, the dash is not only for spitters, but only the spitter rooms currently make it better than a sidestep.

**S3. A single spitter loop is repetitive and drawn out. Mostly a script artifact.**
- The scripts chose to dodge on every cue and to approach slowly. Crossing 15 tiles takes about 3.75 s at 4 tiles/s, and the build 0.5 walker in QA's bots takes hearts for charging. In 04, charging was free, so this has changed. A human who rushes the last spitter finishes in a few seconds. A scripted dodge-and-approach loop is long by choice.
- Real design residue: a stationary spitter that fires every 2.4 s at one fixed pattern has no variation. This is acceptable for one spitter and not the first thing to fix.

**S4. Rooms 4–5: crossfire felt unfair (second most important, and the only real threat). Most important to *fairness*.**
- Observed: deaths at 15.75 s (room 4) and 11.1 s (room 5), all from shots, with hits from shots already in flight while lined up for another warning. Stepping out of one line put the player into another.
- Causes (from `combat.md`, to be confirmed in a trace):
  1. **Cue gap is only 0.2 s.** With two spitters, the first shots are at 1.8 s and 2.6 s and each repeats every 2.4 s. Each cue lasts 0.6 s, so cue windows are 1.2–1.8, 2.0–2.6, 3.6–4.2, 4.4–5.0 s. After one cue ends, the next begins 0.2 s later and **locks onto the player's position at that moment**, which is where the player stands after sidestepping the first. A good dodge of line 1 is therefore the aim point of line 2. The playtester's "stepping aside put me in another line" is the same thing. The player has no time to reposition before the next lock.
  2. **Shots live long.** A shot at 3 tiles/s crosses the 16-tile room in about 5 s (its lifetime limit). With two spitters firing every 1.2 s combined, 3–4 shots are in the air most of the time. Slow shots linger, so the playtester dodged a line only to meet a shot already in flight.
  3. Rooms 4–5 also contain grubs (a lunge under fire). In room 5 the brute adds a third source.
- **Discrepancy to flag (for QA, not blocking):** 27 says the spitters are in "opposite corners" and "fire in sync". Per the room table, they are at (15,0) and (15,8): the **same side** (two east corners). Per the spec, they are 0.8 s apart, not in sync. In room 3 a 5.8 s double fire was reported. The cap delay can bring two shots closer together, so this could be real, or a misreading of the printed picture. The conclusions above hold either way, but a trace of room 4 would settle which one it is.
- Not a defect on its face: criterion 13 requires cue-ignoring to cost 3–6 hearts across rooms 3–5, so the room is meant to bite. The problem is that a **cue-reading** player also dies. The scripted dodger bot clears 3/3, so the scripts that read cues in 27 (0.15 s fixed reaction, but diverted by overlapping lines) are not the bot's policy. This is the single clearest place where "hard" turns into "unfair".

### 3. Options

All stay inside D-001 and the pillars (readable threats, short runs).

**Option 1: Breathing room in spitter rooms 4–5 (addresses S4, helps S2).** *Do.*
- Change: for rooms 4–5 only, space the two spitters' cues so there is a **gap of at least 0.6 s** between one cue ending and the next starting (for example, a first-shot offset of 1.2 s instead of 0.8 s for the second spitter, with the 2.4 s interval unchanged: cue windows 1.2–1.8, 2.4–3.0, 3.6–4.2…). Optionally also lower the shots-in-flight cap to 2 in those rooms. Room 3 stays exactly as spec'd, so criterion 11 does not change.
- Why: the player gets time to take the sidestep and reposition before the next lock, so each line is a separate decision. The dash then becomes the way to cross a lane for a counter-attack rather than a panic button. This preserves "spitter danger forces movement".
- Cost: low. It is a per-room parameter (stagger, cap) on the existing spitter timing rule, with no new code path beyond a per-room value.
- Risk: criterion 13 (walker 3–6 hearts lost, dodger at most half) may move. The walker is already at the 60 FPS upper limit (6). If the walker drops below 3 total, that is a tuning matter for me, not a build defect, and a re-check of the numbers is part of the spec. Keep the interval unchanged, so run length is unaffected.
- Fit: strengthens pillar 3 (readable threats) and the Positives (spitter danger).

**Option 2: Make the melee variants ask for different answers (addresses S1, S2). *Do.***
- Change: add one per-variant flag to the existing grub rule, "can a swipe in the wind-up cancel the lunge", and use it for the **brute**:
  - **Brute (`G`)**: a swipe during its wind-up still damages it but does **not** cancel the lunge. The answer is "sidestep (or dash through), then punish in its 1.2 s recovery". Four swipes need more than one window, so the player must dodge, hit, and dodge again.
  - **Standard and runner**: unchanged (cancel works), so the runner remains "commit to the swipe or step out quickly" and the standard grub is "either".
- Why: three enemies would then want three different things (swipe-cancel quickly, either, dodge-and-punish). The brute becomes a different fight and gives a reason to learn the cue (swiping into its wind-up now costs a heart). It reuses the existing rule and parameter table, and the cue visuals are unchanged (the lane and tint are the same for all variants).
- Cost: low. It is a flag in the existing wind-up cancel check, plus the manual line (brute swipe does not stop the lunge) and a spec/criterion for it (criterion 6 and 8 need a brute case).
- Risk: it makes the brute harder, which could hurt room 5 (already deadly, deaths at 11 s). The brute's lunge is also dodgeable, so it stays fair. Check that a cue-reading player stays safe. A player who has learned "a swipe cancels" and swipes the brute in the wind-up gets hit, and this is a learning moment that should be signalled: the manual and the message ("a brute rears back, heavy") need a short line. That text is not mine to style; art-director can add presentation.

**Option 3: Give the brute a reason to be fought, in room 2 (addresses S1; also S4's single-source problem).** *Do, after 1 and 2 if the team wants a smaller first slice.*
- Change: in room 2, replace the Standard grub at (14,0) with a spitter at (14,0) (existing enemy). Room 2 becomes "runners and a brute under one spitter".
- Why: stalling and dodging the brute for 20 s now costs hearts from shots, so dodging forever is no longer free, and room 2 differs in *kind* from room 1 (no more "same fight, more enemies"). It mixes the two existing enemy classes earlier, as the player profile (comfortable with dodging and spacing) suggests.
- Cost: low (room data).
- Risk: criterion 14 (grub rooms: walker loses at least 1 heart, dodger loses at most 1 and clears both) must be rechecked with a spitter in room 2, and the rooms 1–2 sentence in the spec changes. It brings room 2 closer to 4. Not for a first slice if 1 and 2 already fix the feel.

**Needs a Decide step (named only, not chosen, not recommended now):**
- A **new enemy type** (for example a melee enemy with a genuinely different behavior, like a charger or a shielded enemy), a healing or recovery system, any new input, or a change to run length or the number of rooms. Each would need the `game-director`. I raise one only if a human playtest after Options 1–2 still reports that the melee fights feel the same. At present the evidence is scripted play, so it is premature.

**Ranking:** 1 first (the only real threat and the least fair), 2 second (the main monotony cause), 3 optional third. 1 and 2 are independent and can be built together.

### 4. The most important symptoms for the Goal

1. **S1 (melee shares one answer)** is the Goal's core: it directly produces "monotonous", and rooms 1–2 reading as the same fight.
2. **S4 (crossfire in rooms 4–5)** is the most important *problem*: the only real danger, and the one that feels unfair. A fix here protects the positives. It is also late in a run, where a player decides whether to continue.
3. S2 follows from S1. S3 is mostly a scripted-play artifact.

### 5. What the evidence cannot settle (hand-timed human session needed)

- **Runner:** with a human reaction of 0.2–0.3 s, does the 0.35 s wind-up actually test the player (my estimate says yes) and do they choose swipe or sidestep? A human needs to play room 2 at least twice and say what they did against the runner.
- **Brute:** does a human who must clear room 2 fight the brute at all, and what do they do? Do they notice the room will not clear while it lives? Kill at least one brute (the playtester never did).
- **Rooms 4–5:** is the crossfire unfair for a human, or only for a scripted player who reacts at a fixed 0.15 s? Hand-timed play in rooms 4–5, at least two attempts each, noting cause of each hit (a shot in flight, a new lock, or a line misread). Also whether the two spitters really fire together.
- **Rooms 2 and 3 endings:** the playtester's output was cut off, so the end of those sessions is unknown. Do not treat the 20+ s brute dodging as a finding about clear times.
- **Dash:** whether a human uses it on purpose against shots once Option 1 is in. Experience signal: at least once in a room, not only in panic.

## Decisions already made

- D-001: attack and dash only; no new input. All options comply.
- D-002: per-frame contact sampling and the contact-edge graze stay. Not touched here.
- D-003 (step 30, band wording): not touched.
- Step 9b and the room 2 possible defect (handoff 29) are separate and not diagnosed here.

## Constraints

- Pillars: one-button combat, short runs (15–20 min), readable threats. Play correctly at 30 and 60 FPS. Reuse existing systems.
- Option 1 keeps the 2.4 s interval, so run length is unaffected. Option 2 and 3 are content and rule-flag changes. No run-length change.
- The visual spec says lane geometry is identical for all variants. Option 2 keeps this. Any option that changes lane width per variant would need `art-director` and a spec change, and I do not propose one.

## Open questions

- None that need a Decide step.
- For the Studio: whether to take Options 1 and 2 as one Design step (my recommendation) or 1 first. If a human playtest of the hand-timed kind can run **before** the Design step, it would settle the runner and brute questions above and could change the priority of Option 2. It is not blocking, because Option 1 is justified by the spec numbers alone.

## Expected output

Route to Design for `game-designer` (write-design-spec) for Options 1 and 2, with Option 3 as optional. The spec updates `design/combat.md`: per-room spitter stagger and cap for rooms 4–5, the brute wind-up flag, manual text, and any rewritten criteria (6, 8, 13, 14 if room 2 changes), plus new player-observable criteria (for example: a cue-reading player in rooms 4–5 can name which line to avoid; a brute swipe in its wind-up does not cancel the lunge). Then Build, then QA at 30 and 60 FPS, then a **hand-timed** playtest of rooms 2, 4 and 5 (briefed on the unknowns in Findings 5).

Two side items for QA, not blocking: (a) a trace of room 4 and of room 3 around 5.8 s to confirm spitter fire times and shots in flight against the spec (0.8 s apart, at most 3 in flight), given 27's "in sync" report; (b) handoff 29, the room 2 defect, already routed.

## Sender assessment

Confidence: high that S1 is a design cause (one shared behavior and answer, and the 0.5 changes tuned timing, not the answer). Medium on S4's causes: they come from the spec numbers and the playtester's account, and the "in sync" and "opposite corners" statements conflict with the spec, so a trace is wanted. Medium-low on the runner and brute conclusions: they rest on scripted play and on my reaction-time arithmetic. I ran no `play` or `bots` this step, so I did not verify any build behavior.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#constraints, design/combat.md, design/combat-cues-visual-spec.md, repo/manual.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-contact-edge-graze-accepted.md
- Previous handoff: goals/G-001-combat-monotony/31-game-designer-to-studio.md
>>>END

<<<FILE goals/G-001-combat-monotony/32-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 32
from: qa
to: studio
stage: Triage
outcome: done
---
# 32: qa → studio — Room 2 "grub hit right after a swipe": not a build defect (swipe landed during the lunge); manual wording is misleading

## Task

Report whether the playtester's room 2 observation (handoff 27, item 5) is a defect, a rules-conforming case, or not reproducible. Verdict: **not a build defect. It reproduces, and it conforms to design/combat.md.** One low-severity documentation wording issue is noted for routing.

## Context

Goal G-001. The playtester reported:

- a grub rearing back at about 5.37 s;
- "grub hit" from their swipe at about 5.9 s;
- a grub hit on the player at about 6.017 s.

They asked whether the swipe failed to cancel the lunge or a second grub hit them. The exact script was not preserved. I reconstructed a comparable reaction-rule script (sidestep on "rears back", swipe things within 1.4, approach) and ran `run_trace` at 60 and 30 FPS in room 2. `run_tests` passed (34 tests, OK).

## Findings

### Timeline check against the playtester's numbers

Wind-up for a standard grub is 0.5 s, so a wind-up starting at 5.37 s turns into a lunge at about 5.87 s. The swipe at 5.9 s therefore landed about 0.03 s after the lunge began, not during the wind-up. The grub is then in flight, and the hit at 6.017 s is the lunge reaching the player, about 0.1 s later. The playtester's timeline fits one grub whose swipe came too late to cancel. I derived this from the numbers and could not check it against the original run.

### Trace evidence, 30 FPS (same pattern reproduced)

| Time (s) | Event |
|---|---|
| 2.633 | grub `windup:0.500` |
| 3.133 | grub `lunge` begins |
| 3.300 | `attack {'hits': [('grub','hit')]}`: grub hp 2→1, phase still `lunge` (grub at about (11.95,3.25), player (11.60,4.13), distance about 0.95, within the 1.5 reach) |
| 3.367 | `hurt {'source':'grub','hearts':2}`, 0.067 s after the swipe; the grub goes to `recovery:0.800` |

The sequence is the same as the playtester's: "grub hit", then hurt about 0.07–0.1 s later. It is the same grub, there is no second grub, and the lunge was already in flight when the swipe landed.

The same pattern appears for a brute at 30 FPS: swipe hit during `lunge` at 4.567, hurt at 4.633, source labelled `grub` (the brute is a brute grub). A runner lunge also hit at 5.933 on the same frame the swipe defeated a brute.

### Trace evidence, 60 FPS

- 4.033: grub `windup:0.500`. The player was at (12.93,5.27) and the grub at (12.79,3.60), so the distance was about 1.68, **outside the 1.5 swipe reach**. The swipes at 4.033–4.483 hit or killed the brute. The attacks at 4.183 and 4.333 were ignored as `recovering`.
- 4.533: lunge. 4.650: the player is hit, and the grub stops early at contact and goes to `recovery`.
- Here the swipe never reached the winding-up grub, so this is not a failed cancel.
- 5.033: a swipe hits the grub in recovery (hp 2→1), phase unchanged.
- 5.467: the grub winds up again. 5.500: a swipe kills it during wind-up with no stagger and no lunge, which matches the "kill in wind-up" rule.

### Not the D-002 graze

The lunge contacts were not edge cases. The grub stopped about 0.5 tile (60 FPS: (12.83,4.53) vs player (12.87,5.07), distance about 0.54) from a stationary player in the lane's center. That is far from the 0.57–0.60 band, and the hit came from the player standing in the lane, not from a near-reach path.

### Expected vs actual

- Expected (design/combat.md, Grub rules): "A swipe that damages a grub in wind-up cancels the wind-up." Also: a grub hit but not killed during Lunge "continues its phase unchanged", and a lunge that reaches the player deals 1 damage unless the player is invulnerable.
- Actual: the swipe landed in the lunge, the lunge continued, and the hit followed. This conforms.
- Documentation conflict (low): `repo/manual.md` says "step 1 tile to the side, dash, or swipe it (within 1.5 tiles) to cancel the lunge." It does not say the swipe only works during the warning, and "cancel the lunge" can read as covering a lunge already moving. combat.md is clear and says a lunge in flight is not cancelled. The manual's own warning duration (0.5 s) hints at the limit but does not state it. This is a manual wording gap, not a build defect. Fixing it is a manual change, and I do not decide intended player-facing wording.

### Classification, severity, reproducibility

- Defect: none found. Rules-conforming, with the documents agreeing on the build's behavior.
- Reproducibility: the pattern reproduced at 30 FPS (grub and brute) and the timing arithmetic fits the playtester's report. At 60 FPS my script did not produce the same sequence, because the swipe never reached the winding-up grub. I did not run a controlled 60 FPS case of a swipe landing just after lunge start.
- Severity of the manual wording issue: low (it can mislead a player about when the swipe cancels). Frequency: any swipe that lands after the wind-up ends.

### Not covered

- The exact original script and its trace are unavailable, so the match is by arithmetic and a comparable reproduction.
- I did not observe a non-lethal swipe during wind-up (the "cancel plus 0.4 s stagger" case) in these traces. The tests passed, but I did not inspect which tests cover it.
- I did not check at code level how the 1.5 reach is measured. The distances above come from trace positions.
- No unit or script was changed. The build was not modified.

## Decisions already made

- D-002: per-frame contact sampling kept, graze accepted. This case is not the graze (see above).

## Constraints

Report only, verified from design/combat.md, repo/manual.md, D-002 and the build (trace, tests). The build is unchanged.

## Open questions

- For `game-designer`: should the manual say explicitly that a swipe only cancels a lunge during the wind-up, and that a lunge already moving is not cancelled (the grub stays hittable and the lunge still hurts unless the player dashes or sidesteps)? This is wording, not a rule change. The combat.md rule is unambiguous, so no ruling on intent is needed. Whether to reword the manual is the designer's call.
- Related and optional, for the same designer: nothing else is raised by this case.

## Expected output

Studio decides routing: close handoff 27 item 5 as not-a-defect, and send the manual wording question above to `game-designer` (low priority). No fix is requested from `gameplay-engineer`.

If the studio wants more evidence, a controlled practice-room script (`room empty`, `spawn grub`, `player`, swipe at 0.45 s vs 0.55 s after the cue) at fps 30 and 60 would show the two sides of the 0.5 s boundary. I did not run it, since the verdict does not depend on it.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md, repo/manual.md, project.md#current-state, the build in repo/
- Decisions: decisions/D-002-contact-edge-graze-accepted.md
- Previous handoff: goals/G-001-combat-monotony/29-studio-to-qa.md
>>>END
