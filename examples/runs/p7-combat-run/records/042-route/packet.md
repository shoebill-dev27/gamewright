# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/43-qa-to-studio.md, goals/G-001-combat-monotony/44-game-designer-to-studio.md
next_seq: 45
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha 5eb065e08fef; run through the project's run commands)
log: last 5 of 15 entries in @log-recent; the full history is goals/G-001-combat-monotony/log.md

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/43-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/44-game-designer-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 45
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
design/combat-cues-visual-spec.md
design/combat-step-44-walker-limit.md
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

- Observe: done (scripted play, rooms 1–3 + practice room; 02). FPS divergence (qa): done (16, 20); the contact-edge graze is accepted (D-002, D-003). Spitter fire times (36): build 0.5 conforms to its spec; no real-room trace of room 3 past about 7 s yet (asked of Verify, 41).
- Diagnose: second pass done (31). Melee enemies share one answer (S1, the core of the Goal); rooms 4–5 spitter crossfire was unfair (S4). Evidence is scripted play; runner, brute and crossfire for a human are unconfirmed. A third Diagnose pass without progress goes to `game-director` review (loop limit).
- Decide: skipped. Options so far are variant parameters, a cancel flag, spitter timing, contact consequences; all inside D-001 and the pillars. Tentative again (game-director) if a later step finds the need for a new enemy type, healing, new input, or a scope or priority change.
- Design: 35, 38 done (D-004, D-005). New question (42): walker bot loses 7 hearts in rooms 3–5 at 60 FPS in 0.6, over criterion 13's limit of 6 (30 FPS: 4); tuning or limit ruling.
- Plan: skipped (approach local, reuses the enemy update loop). Returns if the same criterion fails verification twice.
- Build: 0.6 done (40; tests pass, 54). Another Build only if Design 42 or Verify finds a change is needed.
- Verify (QA): open (41), criteria 1–21 at 30 and 60 FPS, independent; bots 13–15, 16c re-measured; open items: `play.py` brute-shrug message, room 3 real-room trace. Verify (visual): V1–V11 need a graphical build, a proposed new Goal at Close; V12 open until one exists. Art-director items from 35 and 38 wait with these.
- Play: first pass done (27). Second pass planned after Verify; fresh, hand-timed on rooms 2, 4 and 5 (runner, brute, crossfire), focus without the expected result.
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
| 14a | Verify (0.6, 30 and 60 FPS) | qa | verify-change | open | 41-studio-to-qa.md |
| 14b | Design (criterion 13 walker limit, 60 FPS) | game-designer | write-design-spec | open | 42-studio-to-game-designer.md |
| 15 | Play (fresh, hand-timed rooms 2, 4, 5) | playtester | playtest-session | planned | — |
| 16 | Review | game-director | review-outcome | planned | — |
| 17 | Next | studio | — | planned | — |

## Route changes

After 13 (Build 0.6, 40): fits; the engineer found no spec gap. One bot figure (walker, 60 FPS, rooms 3–5: 7 hearts vs limit 6) is a tuning question, so Design (42) runs in parallel with independent Verify (41). Build was not rerouted; the Sender assessment was not passed to QA.

## Next action

Run the qa step with 41-studio-to-qa.md and the game-designer step with 42-studio-to-game-designer.md (parallel). Then Route, waiting for both. If Verify fails a criterion, return to Build; if the Design ruling changes the build, open Build before Play. Otherwise compose a fresh Play handoff for the playtester from the build and player profile only.

## Outcome

(open)
>>>END

<<<FILE @log-recent
## 027-route · 2026-10-16

Status: active. Open: 26-studio-to-game-designer.md, 28-studio-to-game-designer.md, 29-studio-to-qa.md.

After 9a (Play): does not fit "goal met". The playtest reports remaining monotony (melee enemies share one answer, dash unused, spitter crossfire) and one possible defect. Returned to Diagnose (10a, designer) and Observe (10b, qa) in parallel with open 9b. Decide, Design, Build, Verify and Play are tentative on the Diagnose result.

## 031-route · 2026-10-16

Status: active. Open: 33-studio-to-game-designer.md, 34-studio-to-qa.md.

After 9b, 10a, 10b: all fit. Diagnose 31 needs no Decide (options inside D-001), so Decide stays tentative. Room 2 hit is not a defect (32). Opened Design (33, Options 1–2, manual wording) and, in parallel, a QA spitter-timing trace (34) to settle the "in sync" conflict. Build, Verify, Play are now planned.

## 034-route · 2026-10-16

Status: active. Open: 37-studio-to-game-designer.md.

After 12a and 12b: both fit. Design 35 is complete (no Decide). QA 36 found no defect in 0.5 but an undefined rule (shot touching an invulnerable player) and room 3 cue overlap. Added 12c Design (37) before Build so contact code changes once.

## 037-route · 2026-10-16

Status: active. Open: 39-studio-to-gameplay-engineer.md.

After 12c (Design 38): fits. The designer ruled on blocked contact (D-005: shot consumed, lunge spent) and accepted simultaneous cue starts outside rooms 4–5; the spec is complete and no direction or scope change arose, so Decide stays tentative. Opened Build 0.6 (39) with the full change list; its result is addressed to `studio` for an independent Verify.

## 039-route · 2026-10-16

Status: active. Open: 41-studio-to-qa.md, 42-studio-to-game-designer.md.

After 13 (Build 0.6, 40): fits; the engineer found no spec gap. One bot figure (walker, 60 FPS, rooms 3–5: 7 hearts vs limit 6) is a tuning question, so Design (42) runs in parallel with independent Verify (41). Build was not rerouted; the Sender assessment was not passed to QA.
>>>END

<<<FILE goals/G-001-combat-monotony/43-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 43
from: qa
to: studio
stage: Route
outcome: fail
---
# 43: qa → studio — Verify of build 0.6 (criteria 1–21, 30 and 60 FPS): FAIL

## Task

Route the failures below to `gameplay-engineer`. Send the criterion 13 numbers to `game-designer` as a tuning question, which was already planned. Send the room 3 finding to `game-designer` as well, because D-005 says to revisit it. After the fixes, QA re-verifies. The items listed under "Not run" below must be covered then.

## Context

Verification of build 0.6 (`repo/`, sha 5eb065e08fef) against Design handoffs 35 and 38. Evidence comes from the executed runs: the unit tests, player-view and trace scripts at 30 and 60 FPS, and the bots. All times are game seconds. "30" and "60" mean the frame rate. Visual criteria V1–V11 are out of scope.

## Findings

### Verdict

**FAIL.** Three failures: criterion 13 (60 FPS), the missing brute shrug message in the player view (a defect of the player view, criterion 19a), and the version banner. Criterion 16 fails through 16b, because criterion 13 does not hold at 60 FPS. Criteria 18, 19 (trace behavior), 20 a–d and 21 a, c, d are met on the evidence listed. Several criteria were not run this round (list below), so no full pass can be claimed.

### Unit tests

`python3 -m unittest discover -s tests`: 54 tests, OK. Used as a regression signal only.

### Per criterion

| # | 30 FPS | 60 FPS | Evidence |
|---|---|---|---|
| 1 Telegraph | pass | pass | Standard grub: cue 0.033 → lunge 0.533 (30); cue 0.017 → lunge 0.517 (60). The hit in the second lunge lands 0.533 s (30) and 0.517 s (60) after the cue (c21std). |
| 3 Dash | pass (standard grub, brute) | pass (standard grub, brute) | A dash during the lunge gives 3/3 hearts after the dash ends (c21std, c21brute). Runner: not run in isolation. |
| 4 Standing still | pass | pass | brute30/60, c20a: the standing player loses hearts. |
| 5 Safe window | pass (brute) | pass (brute) | Brute recovery 1.6–2.0 with the brute 0.47 tile away and the player hurtable: no damage. Standard grub: the recovery overlaps the hurt window in my scripts, so it is not isolated. |
| 7 One at a time | pass (read) | pass (read) | Rooms 4 and 5 traces: never two grubs in wind-up or lunge together. Not a dedicated test. |
| 8 Variants | partial | partial | Brute takes exactly 4 swipes: 1+1 in wind-up, 1 in recovery, 1 kill (c19c). Runner's one-swipe death: not run. |
| 9 Cue timing | pass | pass | Every cue is 0.6 s before its shot in all spitter traces. The locked line was not observed. |
| 11 Stagger, cap | partial | partial | Room 3 first shots 1.8, 2.6, 3.4. Rooms 4 and 5 first shots 1.8, 3.0. All at both rates. **Shots in flight are not visible in the trace, so "never more than 3" was not observed. See the room 3 finding below.** |
| 12 Rooms | pass (rooms 3–5) | pass (rooms 3–5) | Contents match the table. Rooms 1–2 not viewed. |
| 18 Cue gap (rooms 4–5) | pass | pass | See below. |
| 19 Brute | pass in trace; **fail in player view** | pass in trace; **fail in player view** | See below. |
| 20 Consumed shot | a, b, c, d pass | a, b, c, d pass | See below. e, f not run. |
| 21 Spent lunge | a, c, d pass | a, c, d pass | See below. b not run. |
| 13 Spitter rooms (bots) | **PASS** | **FAIL** | Walker loses 7 hearts in rooms 3–5 at 60 FPS (limit 6). |
| 14 Grub rooms (bots) | pass | pass | |
| 15 Dash used (bots) | pass | pass | |
| 16 Frame-rate independence | **fail** | | 16b fails because of 13 at 60. 16c passes. 16e is not resolved (see below). |

**Criterion 18 (cue gap in rooms 4–5).**
- Rooms 4 and 5, still player: cues at 1.2, 2.4, 3.6, 4.8 and shots at 1.8, 3.0, 4.2, 5.4. The gap from shot to next cue is exactly 0.6 s and cue windows never overlap, at both rates.
- Cap delay, `dash aside` script, 15 s, rooms 4 and 5, both rates. The 3 shots in flight block both cues. Both spitters then become due together at 6.8 s.
  - A starts its cue at 6.8 and shoots at 7.4.
  - B starts its cue at 8.0 (gap 0.6 s) and shoots at 8.6.
  - A starts again at 9.2 (gap 0.6 s) and shoots at 9.8.
  - Later in the same traces the pattern repeats: a cue at 12.4, shot at 13.0, B cue at 13.6, shot at 14.2 (and A cue at 14.8 at 60 FPS).
  - All gaps are 0.6 s with no overlap.
- This is a naturally forced simultaneous schedule, so 18c (cap delay) and 18d (equivalent) are covered at both rates. The first shots were not forced to the same time.
- Not run: 18c with one spitter killed.

**Criterion 19 (brute not cancelled).**
- Wind-up swipes: practice room, brute at (9,4), player at (8,4), swipes at 0.1 and 0.5.
  - a: hp 4→3, a `shrug` event at 0.133 (30) and 0.117 (60). The cue stays (still shown at 0.5 s). The lunge comes 0.700 s after the cue (0.033→0.733 at 30, 0.017→0.717 at 60). 1 heart is lost.
  - b: two swipes give hp 2 and two `shrug` events, with one lunge.
- c: a kill in wind-up (c19c, hp 1, swipe at 2.3) gives `defeated`, no lunge, no shrug event.
- d: swipe at 0.1 plus dash at 0.7 (c21brute): no damage from that lunge, and hp stays 3 (the swipe damage is kept). The dash and lunge start on the same frame, so this is not a late dash.
- e: a recovery swipe at 1.2 gives hp 2→1, phase unchanged.
- f: not run this round (standard grub and runner still cancelled; criterion 6).

**Criterion 20 (consumed shot).**
- a, hurt window (c20a, spitter at (15,4), player at (8,4)). The grub hurts the player at 3.733 (30) / 3.700 (60). The window runs to 4.533 / 4.500. The first shot arrives at about 4.0, inside the window. **No hit at the window end** and hearts stay 2 until the next grub hit (5.1 / 5.033). Before 0.6 there was a hit at 4.533 / 4.483. The shot's disappearance frame was not observed, because the trace does not show shots.
- b, dash (c20b): the player dashes right into the shot line at 3.9 (30) / 3.867 (60) and ends the dash at x=12 on the old line. The first shot does no damage then or later. The only later hit is the second shot at 5.067 (30) / 5.05 (60), exactly its arrival time.
- c, normal hit: the same scripts give a hit at 6.4 (c20a) and 5.067 (c20b), on the arrival frame.
- d, room 4 still-player trace:
  - The shot arriving about 4.35 is consumed in the window at both rates.
  - 60 FPS: the next shot hits at 5.550, exactly its arrival time, and not at the window end (5.467).
  - 30 FPS: the window of the hit at 4.767 ends at 5.567, which is the same frame in which the shot's contact falls. The trace shows no shot hit at 5.567. The next damage is the runner at 5.8. The shot was consumed at the window-end frame. The spec accepts ±1 frame at this boundary. Hearts lost are identical at both rates; only the death time differs (5.8 vs 5.55). Reported as an observation, not as a fail.
- e (cap slots) and f (band) not run.

**Criterion 21 (spent lunge).**
- a, standard grub (c21std): the dash at 0.5 puts the player at x=0 against the edge. At the dash end (0.767 at 30, 0.75 at 60) the grub is at x=0.03 and still lunging. No damage. Hearts stay 3.
- c: the lunge is not shortened. The recovery is 0.8 s, and the next wind-up is at 1.667 (30) / 1.633 (60).
- d: the second lunge hits at 2.2 (30) / 2.15 (60).
- Brute: the same result (c21brute). Recovery 1.2 s and the next lunge hits at 3.0 / 2.95.
- b (hurt window ends inside a lunge) was not run.

### Failures and defects (reproduction)

**F1. Criterion 13 fails at 60 FPS.** `run_bots` with `bots camper,walker,dodger`, `rooms 1-5`, `fps 60`: the walker loses 2+3+2 = 7 hearts in rooms 3–5 (limit at most 6). Per the criterion text this is a fail. The limit question is routed to Design in parallel, and I did not adjust it. Severity: medium, a tuning question.

**F2. The player view does not print the brute shrug message (criterion 19a).**
- Reproduction: the script below, `python3 play.py --view player`.
  ```
  room empty
  fps 30
  spawn brute 9 4
  player 8 4
  0.1 attack
  0.5 attack
  end 4
  ```
- Expected (design 35, criterion 19a, handoff 41): the text "the brute shrugs off the swipe" at the moment of each swipe that damages but does not kill the brute in wind-up.
- Actual: only `0.100  you swipe: brute hit` and `0.500  you swipe: brute hit`. The same happens at 60 FPS. The trace view does contain `shrug {'enemy': 'brute'}` events, so the simulation is right and the player view omits the message.
- Severity: medium. The manual promises the message, and it is the only in-game signal of the brute rule.
- Acceptance for the fix: both swipes print the message at both rates. A kill in wind-up prints no message. A swipe at a standard grub or runner is unchanged.

**F3. The version banner says 0.5.** Every player-view output starts `Lantern Depths 0.5 — room …`, but the manual and README say build 0.6. Low severity. Acceptance: the banner shows 0.6.

### Bot figures (hearts lost / cleared)

| Bot, room | 30 FPS | 60 FPS |
|---|---|---|
| walker 1 | 3 / no | 3 / no |
| walker 2 | 2 / yes | 2 / yes |
| walker 3 | 0 / yes | 2 / yes |
| walker 4 | 1 / yes | 3 / no |
| walker 5 | 3 / no | 2 / yes |
| walker rooms 3–5 | 4 lost, 2 cleared | **7 lost**, 2 cleared |
| dodger rooms 1–5 | 0 lost, 5/5 | 0 lost, 5/5 |
| dodger dashes, rooms 1–5 | 3, 10, 8, 7, 11 | 5, 14, 10, 8, 14 |
| camper rooms 3–5 | 0 cleared, 9 lost | 0 cleared, 9 lost |
| camper rooms 1–2 | 1 of 2 cleared | 0 of 2 cleared |

- **13:** 30 passes (walker 4 hearts, 2 cleared; dodger 0 and 3/3; camper 0 < walker 2). 60 fails (7 > 6).
- **14:** pass at both rates. Walker rooms 1–2 lose 5 (at least 1). The dodger loses 0 and clears both. The brute policy of the dodger holds.
- **15:** pass at both rates. The dodger dashes in each of rooms 3–5 (30: 8, 7, 11; 60: 10, 8, 14).
- **16c:** pass. The dodger has the same cleared set and 0 vs 0 hearts.
- **16d/16e:** the walker differs between rates in rooms 3, 4 and 5. QA did not run decision logs (`log on`), so it is not confirmed whether the differences come from bot timing or from a build defect. This stays open for re-verification.

### Open questions, answered

**1. Does the player view print the brute shrug message?** No. See F2.

**2. Room 3 in a real room, 15 s, surviving player** (reaction script: `when see * coming within 2 then dash aside`, both rates; the player took no damage in 15 s):
- First shots at 1.8, 2.6, 3.4 as specified. The cue gap stays 0.8 s.
- **A cap delay occurs.** The second cues are due at 3.6, 4.4 and 5.2 but none starts until 6.8. The delay is 3.2 s, 2.8 s and 1.6 s.
- **Three cues start at the same moment** (6.8 s, all three spitters `aim; aim; aim`) and all three shoot together at 7.4. The same repeats at 11.0 (cues) and 11.6 (shots). Identical at 30 and 60 FPS.
- With the cap counted at each check (2 shots in flight when the three cues start), my derivation from the timings is that up to 5 shots are in the air at 7.4. This is derived, not observed, because the trace does not list shots. If so, the statement "room 3 stays at 3 or fewer" and criterion 11 ("rooms 1–5 never more than 3") would not hold in this run, although the 2 + living spitters bound (5) does. **Design should rule on whether this is accepted (D-005 revisit trigger).** A player-view check of `*` at 7.5 s would settle the count.
- The scripted dasher was not hit in 15 s. I cannot say from a trace whether a human can answer three simultaneous lines.

### Spec gap (for Design, not a fail)

Criterion 11 ("never more than 3 in flight in rooms 1–5") and the cap rule (the cap is checked at cue start only) look contradictory in room 3 when several cues are delayed together. See the finding above.

### Not run this round (must be covered at re-verify)

- Criteria 2, 6 (standard grub and runner cancel), 10, 17 (all of a–d), 19f, and the isolated runner dash in 3.
- Runner's one-swipe death in 8, and rooms 1–2 contents in 12.
- 18c with a killed spitter.
- 20e, 20f and 21b.
- 16e decision logs.
- The in-flight shot count.

## Decisions already made

D-001 to D-005 as in handoff 41. No limit or criterion was changed by QA.

## Constraints

- Production code was not touched.
- A fix to F2 or F3 must keep timings unchanged at both rates.

## Open questions

- Design: is the three-simultaneous-cue start and the possible 5 shots in the air in room 3 accepted (D-005 revisit)?
- Design: the criterion 13 limit at 60 FPS, with the numbers above.

## Expected output

Studio routes F2 and F3 to `gameplay-engineer`. Studio routes F1 and the room 3 finding to `game-designer`. Then Studio asks QA for a re-verify that covers the "Not run" list.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md, repo/manual.md, repo/README.md, project.md#constraints, the build in repo/
- Decisions: decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md, decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Previous handoff: goals/G-001-combat-monotony/41-studio-to-qa.md
>>>END

<<<FILE goals/G-001-combat-monotony/44-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 44
from: game-designer
to: studio
stage: Design
outcome: done
---
# 44: game-designer → studio — Criterion 13 ruling: walker limit 3–7 at 60 FPS, no build change

## Task

Pass the ruling on criterion 13 to QA, who is verifying build 0.6 in parallel (41), so QA judges the walker figures against the amended limits. No build change is needed. No Director decision is needed.

## Context

G-001 (combat monotony). Build 0.6 (Design 35 and 38, D-004, D-005) puts the walker bot at 7 hearts lost in rooms 3–5 at 60 FPS (4 at 30 FPS), against criterion 13's limit of 6. Handoffs 40 and 42 contain the figures and the question.

## Findings

**Ruling: 7 hearts is not a breach of intent. The limit of 6 was too tight, and it was a snapshot of the 0.5 result, not a derived bound. The limit changes to 3–7. No room or enemy parameter changes.**

The purpose of criterion 13 is a gradient, and it holds at 7:

- Costly: walker 4 (30 FPS) and 7 (60 FPS) hearts lost, against dodger 0 lost, 3/3 cleared and 7 or more dashes per room, and camper 0 of 3 cleared.
- Not hopeless: the walker clears 2 of 3 at both rates.

Why a hearts ceiling below 7 is the wrong tool:

- A room has 3 hearts, and a cleared room costs at most 2. A walker clearing 2 of 3 rooms therefore loses at most 3+2+2 = 7.
- The clear count is what carries "not hopeless". A ceiling of 6 only forbids a particular distribution of hearts across rooms.
- The walker's 0.15 s grid sensitivity moves single hearts between rooms with no player-visible cause (criterion 16d). The engineer saw the room totals move in opposite directions between 0.5 and 0.6.

Why no parameter changes: the shift is the expected net of D-004 (brute not cancelled: more losses) and D-005 (consumed shots: fewer). A parameter change would fit one bot's grid phase and force re-verification of criteria 11, 13, 14, 15, 18, 20 and 21.

Changed criteria:

- **13:** the walker's upper limit is 7 (was 6), and the lower limit 3 stays. The clears-at-least-2 gate is now the primary one. The dodger, camper and per-rate rules are unchanged.
- **13e/f:** per-room walker numbers are not criteria. The rates are checked separately.
- **13 reporting rule:** QA reports only values that fail 13a–d.
- Criteria 14, 15 and 16 are unchanged.

Full amended text: `design/combat-step-44-walker-limit.md`, which governs where `combat.md` differs. `combat.md` itself was not rewritten, so it still shows the old numbers until the two are merged.

**Build change list: none.** `bots.py` is unchanged. The engineer already removed the walker's upper bound of 6 from its own test. Its test should now assert 3 to 7 hearts lost and at least 2 rooms cleared, per rate. That is test tooling and not a build change.

**Does the answer depend on QA's figures?** Yes, in a limited way. These results would reopen the ruling:

1. The walker clears fewer than 2 of 3 rooms at either rate. That means walled out, and the response would be a parameter change.
2. The walker loses fewer than 3 hearts at either rate. The 30 FPS margin is only 1 heart.
3. The dodger loses more than half the walker's total, or fails 3/3.
4. The camper clears as many rooms as the walker or more.
5. A rate difference that comes from a rule and not from bot timing, which is a build defect (16e).

A QA 60 FPS walker figure of 6 or 7 with 2 rooms cleared changes nothing.

QA re-verifies only criterion 13 against the amended limits, at both rates, on the unchanged build. It also confirms the walker's rate differences come from the 0.15 s grid.

## Decisions already made

- D-001: one-button combat.
- D-004 and D-005: unchanged and respected.
- D-006 (new): the walker limit in rooms 3–5 is 3–7 hearts with at least 2 rooms cleared, and no parameter change.

## Constraints

- Nothing in the 30 and 60 FPS behavior changes.
- No new enemy, healing, input or room content.
- Hand-timed playtest of rooms 3–5 remains the real test of "costly but not hopeless" for a human. If a cue-ignoring human cannot get through, reopen D-006 and the D-004/D-005 tuning values.

## Open questions

- For QA: does `play.py` print "the brute shrugs off the swipe" for the `shrug` event? Handoff 40 could not check it, and this note does not change that.
- For the Studio: fold `design/combat-step-44-walker-limit.md` into `design/combat.md` at the next edit of that file, so that criterion 13 is stated in one place.

## Expected output

The Studio forwards this ruling to QA to use when judging the criterion 13 figures. The ruling needs no further Design work unless one of the five listed results appears. If one does, route it back to `game-designer`, or to `game-director` if it touches D-004, D-005 or scope.

## Sender assessment

High confidence in the ruling. It is a derivation from the 3-hearts-per-room structure and from the stated purpose of the criterion, not a measurement. I did not run the bots, because the ruling depends on the structure and the engineer's figures. QA's independent figures can break it only through the five results above. The weakest margin is the lower limit at 30 FPS (4 against 3).

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md, design/combat-step-44-walker-limit.md
- Decisions: decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md, decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md, decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md
- Previous handoff: goals/G-001-combat-monotony/42-studio-to-game-designer.md
>>>END
