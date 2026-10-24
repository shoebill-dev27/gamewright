# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/07-game-designer-to-studio.md, goals/G-001-combat-monotony/08-qa-to-studio.md
next_seq: 9
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha d2625d9e678a; run through the project's run commands)
log: last 3 of 3 entries in @log-recent; the full history is goals/G-001-combat-monotony/log.md

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/07-game-designer-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/08-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 09
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
design/combat.md
goals/G-001-combat-monotony/01-studio-to-playtester.md
goals/G-001-combat-monotony/02-playtester-to-studio.md
goals/G-001-combat-monotony/03-studio-to-game-designer.md
goals/G-001-combat-monotony/04-game-designer-to-studio.md
goals/G-001-combat-monotony/05-studio-to-game-designer.md
goals/G-001-combat-monotony/06-studio-to-qa.md
goals/G-001-combat-monotony/07-game-designer-to-studio.md
goals/G-001-combat-monotony/08-qa-to-studio.md
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

- Observe: done (scripted play, rooms 1–3 + practice room). Rooms 4–5 and hand-timed play are unobserved by a human; the final Play step covers them.
- Observe (defect, qa): open. Dodger bot results differ between 30 and 60 FPS in rooms 3–4; the project requires correct play at both. Also unverified: the build's dash invulnerability against `design/combat.md`.
- Diagnose: done (04). Leads: grubs are trivial and unreadable, spitters unreadable and dodging is dominated by walking in, dash never needed. Spitter volley overlap is still a hypothesis.
- Decide: skipped. The diagnosis offers no choice of direction or scope; all options stay within D-001 and the pillars. Returns here if Design needs a new enemy type, a healing system or a new input.
- Design: open (`game-designer`), grub readability and variation, spitter readability, light room pass.
- Plan: tentative. Only if the spec's approach is non-obvious, risky or cross-system. Constraints: 30 and 60 FPS, reuse of existing systems.
- Build: planned (`gameplay-engineer`). Verify (`qa`) planned after Build, with `art-director` in parallel if the change affects visuals (telegraph cues likely).
- Play: planned. A fresh playtester judges the result, including rooms 4–5 and hand-timed play.
- Review: planned (`game-director`), experience Goal.

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | playtester | playtest-session | done | 01-studio-to-playtester.md (report: 02-playtester-to-studio.md) |
| 2 | Diagnose | game-designer | diagnose-experience | done | 03-studio-to-game-designer.md (result: 04-game-designer-to-studio.md) |
| 3 | Decide | game-director | make-decision | skipped (no real choice; see Unknowns) | — |
| 4a | Design | game-designer | write-design-spec | open | 05-studio-to-game-designer.md |
| 4b | Observe (FPS divergence) | qa | reproduce-defect | open | 06-studio-to-qa.md |
| 5 | Plan | technical-director | technical-plan | tentative (if approach non-obvious) | — |
| 6 | Build | gameplay-engineer | implement-change | planned | — |
| 7a | Verify | qa | verify-change | planned | — |
| 7b | Verify (visual) | art-director | visual-review | tentative (if visuals change) | — |
| 8 | Play | playtester | playtest-session | planned | — |
| 9 | Review | game-director | review-outcome | planned | — |
| 10 | Next | studio | — | planned | — |

## Route changes

After step 2 (Diagnose): fits the plan. Decide is skipped (no real choice, no trigger). Added a parallel QA Observe for the 30/60 FPS bot divergence, since Design's criteria depend on both rates. A separate rooms 4–5 playtest is not added; the final Play covers it.

## Next action

Start steps 4a and 4b in parallel: the game-designer runs `05-studio-to-game-designer.md` (Design) and qa runs `06-studio-to-qa.md` (FPS divergence check). Both address results to `studio`; the next Route waits for both.

## Outcome

(open)
>>>END

<<<FILE @log-recent
## 001-intake · 2026-10-16

Status: active. Open: 01-studio-to-playtester.md.

Initial route from Intake (pattern: experience problem, cause unknown). No changes yet.

## 003-route · 2026-10-16

Status: active. Open: 03-studio-to-game-designer.md.

After step 1 (Observe): the outcome fits the plan, so Diagnose follows. The report is thin (scripted play, rooms 4–5 unseen); the Diagnose Handoff lets the designer check with bots/trace and say if more observation is needed. No stage added or dropped.

## 005-route · 2026-10-16

Status: active. Open: 05-studio-to-game-designer.md, 06-studio-to-qa.md.

After step 2 (Diagnose): fits the plan. Decide is skipped (no real choice, no trigger). Added a parallel QA Observe for the 30/60 FPS bot divergence, since Design's criteria depend on both rates. A separate rooms 4–5 playtest is not added; the final Play covers it.
>>>END

<<<FILE goals/G-001-combat-monotony/07-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 7
from: game-designer
to: studio
stage: Route
outcome: done
---
# 07: game-designer → studio — Combat spec for readable grubs and spitters, with a room pass

## Task

Route the finished spec in `design/combat.md` onward (Build, with QA verification and a later art-director review). Reconcile criteria 13–16 with QA's result on the 30/60 FPS bot divergence.

## Context

Goal G-001: the Owner finds combat monotonous. Diagnosis 04 found threats that are either trivial (grubs) or unreadable (spitters), and a dash that is never needed. The Studio accepted options A and B with a light pass on C and skipped Decide. This step wrote the spec.

## Findings

Spec is in `design/combat.md` (the whole document was updated). Summary:

- **A, Grub.** It now has four phases: approach, wind-up (0.5 s, standard), lunge, recovery (0.8 s). The aim is locked at the start of the wind-up, and the cue is an orange-red flash plus a path line. The lunge is the only damaging action. A swipe cancels a wind-up. Only one grub is in wind-up or lunge at a time. Two parameter variants of the same Grub (Runner: 1 HP, fast; Brute: 4 HP, slow, long wind-up). No new enemy type, so no Decide is needed.
- **B, Spitter.** 0.6 s aim cue with the aim locked at its start, shot speed 3.0 tiles/s, interval 2.4 s, staggered first shots (1.8 s + 0.8 s per spitter), at most 3 shots in flight.
- **C, Rooms.** Room 1 unchanged, room 2 now Runner×2 + Brute + Standard, room 3 unchanged (new spitter behavior), room 4 one Runner, room 5 one Brute. Rooms 4–5 content was read from `game.py` room data.
- **Acceptance criteria.** 16 checks. Criteria 1–12 are direct play checks (practice room, both FPS). Criteria 13–16 are bot comparisons at both FPS (walker loses 3–6 hearts over rooms 3–5; good dodger loses at most half and clears them).

Hypotheses checked by reading code (not by `run_trace` / `run_tests`):

- **C4 (overlapping volleys) is supported by the code.** Every `Enemy` is created with `cooldown = SPIT_INTERVAL` and the same interval, so all spitters in a room fire on the same frame at 2.0 s, 4.0 s and so on. Volleys are synchronized by construction. At shot speed 1.6 and a room width of 16, a shot is in flight for up to about 10 s, so many shots can be on screen.
- **Dash invulnerability matches the design in the code.** `press("dash")` sets invulnerable for `DASH_TIME`; `_hurt` and the shot check both return early when invulnerable; the flag is cleared when the dash ends unless the hurt timer is running. This is a code reading, not a run.

## Decisions already made

- D-001: one attack button plus dash; no new input. The spec adds none.
- Studio routing: Decide skipped. The spec uses only parameter variants of the existing Grub and Spitter. No new enemy type, no healing or recovery system.

## Constraints

- Pillars: one-button combat, short runs, readable threats. Plays correctly at 30 and 60 FPS (durations in seconds, not frames; per-frame travel stays below the contact reach).
- The playtester's raw losses were not used as balance data.

## Open questions

- **QA result on the FPS divergence.** Criteria 13–16 depend on the bots behaving the same at both rates. Reconcile when QA's result is in.
- **Bots do not read the new cues.** The existing walker and dodger logic must be updated, or reaction-rule scripts used, so that the "good dodger" in criterion 13 exists. This is test tooling for engineering; the thresholds in 13–15 are initial values and may need one tuning pass after the first bot runs (tuning range for wind-up is in the spec).
- **Art review.** The cues (flash, path line, spitter glow, line against the dark) are specified as player-observable behavior only. `art-director` should review after Build because the change affects visuals.
- **Marks and messages.** `repo/manual.md` must list the `r` / `G` marks and the new messages.
- Plan: not needed in my view. The change reuses the existing enemy update loop and adds timers and states; no cross-system approach. Engineering may decide otherwise.

## Expected output

Build per `design/combat.md`; QA verifies criteria 1–12 with play scripts, and 13–16 once bots and FPS behavior are settled; then art-director review; later a Playtester pass on the built rooms (including rooms 4–5, which no human has seen).

## Sender assessment

Confidence: high that the spec is complete and internally consistent: lunge distance 2.4 tiles against a trigger of 2.0 and bite reach 0.6, so a lunge reaches a stationary player. Medium on the numeric thresholds in 13–15: I did not simulate the new design, and the existing bots cannot play it. Unverified: build behavior by `run_trace` / `run_tests`; the dodger bot's FPS behavior; whether the walker clears at least 2 of rooms 3–5 with the new spitter.

## Load

- Role: studio/roles/studio.md
- Skills: none
- Project: project.md#vision, project.md#constraints, project.md#art-direction, design/combat.md, repo/manual.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/05-studio-to-game-designer.md
>>>END

<<<FILE goals/G-001-combat-monotony/08-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 8
from: qa
to: studio
stage: Observe
outcome: done
---
# 08: qa → studio — 30 vs 60 FPS dodger discrepancy reproduced; build timing consistent, cause not isolated

## Task

Report on the 30 vs 60 FPS discrepancy in the balance-bot results and on dash invulnerability in the build (0.4). Studio decides the next routing.

## Context

Goal G-001 (combat monotony). The project constraint is "must play correctly at both 30 and 60 FPS". Studio handoff 06 reported that the dodger bot failed room 3 at 60 FPS and cleared it at 30 FPS. No build or bot change was made in this step; this is report only.

## Findings

### 1. Reproduction (bot results)

Script (`run_bots`, one script per rate, first line optional):

```text
bots camper,walker,dodger
rooms 1-5
fps 60        # second run: fps 30
```

Build at the time of the run: `repo/` 0.4 (the combat.md changes are SPEC for the next build and are not in this build).

| Bot / room | 60 FPS | 30 FPS |
|---|---|---|
| dodger room 3 | NOT cleared (19.7 s), 3 hearts lost (shot 3), attacks 3, dashes 13 | cleared 9.5 s, 0 hearts lost, attacks 6, dashes 4 |
| dodger room 4 | cleared 21.8 s, 2 lost (shot), dashes 9 | cleared 17.8 s, 2 lost (shot), dashes 6 |
| dodger room 5 | cleared 17.7 s, 1 lost, dashes 8 | cleared 17.8 s, 1 lost, dashes 8 |
| dodger rooms 1, 2 | 5.1 s and 7.1 s, 0 lost | 5.0 s and 7.0 s, 0 lost |
| dodger total | cleared 4/5, 6 hearts lost, 30 dashes | cleared 5/5, 3 hearts lost, 18 dashes |
| walker | 5/5 cleared, 1 heart lost in total (room 3, shot) | identical outcomes |
| camper | 2/5 cleared, 9 hearts lost | identical outcomes |

- **Reproduced**: yes, the 06 observation is exactly as reported.
- **Deterministic**: yes. Two identical 60 FPS runs gave byte-identical output. The game is headless and deterministic.
- **Where it stops**: only the dodger differs materially, in rooms 3 and 4. Rooms 1, 2, 5 and the walker and camper agree. Their clear times differ by at most 0.1 s, which is one frame of quantization.
- **Bots test**: `python3 -m unittest discover -s tests` passes (14 tests).

### 2. Does the simulation itself differ between 30 and 60 FPS? (traces)

Not in anything I could measure. Traces were taken in the practice room (`room empty`, `spawn`, `player`) at both rates:

- **Spitter timing**: the shot is fired at t=2.000 and t=4.000 at both rates.
- **Shot damage**: with no dash, the player is hit at t=4.250 at 60 FPS, losing 1 heart. Shot travel time is the same.
- **Dash distance**: 4.00 tiles at both rates (the test suite also checks this).
- **Dash duration**: the dash ends at t=0.250 at 60 FPS (frame 15) and t=0.267 at 30 FPS (frame 8). This is frame rounding of up to one frame.
- **Hit-stun and hurt-invulnerability**: a hit gives stun 0.300 s and invulnerability 0.800 s at both rates. The second grub hit comes 0.8 s after the first (t=0.250 → 1.050 at 60 FPS, 0.267 → 1.067 at 30 FPS).
- **Not directly traced**: grub walk speed and cooldown are computed from `dt` in the same way at both rates. I did not test them separately beyond the bot room runs.

So the simulation constants and event times agree within one frame. The measured discrepancy sits in the dodger bot's results.

### 3. Dash invulnerability vs `design/combat.md` ("invulnerable for the full dash duration")

The build matches at both rates in the cases I traced.

- **Dash into a grub** (`player 0 4`, grub at 0.5, 4, `0.0 dash left`): invulnerable from the dash press until the dash-timer-ended frame. The first hit lands at t=0.250 (60 FPS) and t=0.267 (30 FPS), in the same simulation step in which the dash ends. No hit occurs while the dash is active.
- **Dash through a shot**: in the practice room, a shot due to reach the player at about t=4.25 was crossed by a dash started at 4.1 s. The dash covered 4.1–4.35 s at 60 FPS and 4.133–4.367 s at 30 FPS. No hurt event occurred at either rate. The control run without the dash was hit at t=4.250.
- **Invulnerability handoff**: the trace shows invulnerability dropping on "dash timer ended" and being re-set by "hurt" in the same step. This is consistent with the spec and with the existing test.
- **Not tested**: a dash started while hurt-invulnerable (the existing test `test_a_dash_right_after_a_hit_keeps_both_protections` covers it at both rates and passes), and dash against a lunging grub (not in this build).

### 4. Defect assessment

- **Build defect confirmed?** No. I found no build behaviour that differs between 30 and 60 FPS beyond ±1 frame rounding.
- **Bot issue?** Likely, but not isolated. This is a hypothesis, not a finding: the dodger acts every frame, with no reaction delay, and dashes whenever a shot is detected and the dash is ready. Dashes are 4 tiles long. A one-frame difference in when a shot is first detected, or in where the dash ends, may be enough to shift later decisions in a chaotic way (13 dashes at 60 FPS vs 4 at 30 FPS in room 3). Note that `play.py` limits rules to one action per 0.15 s but `bots.py` does not.
- **Ruled out**: non-determinism; differing spit timing, dash distance, hit-stun and hurt-invulnerability timing; dash invulnerability missing at either rate in the traced cases.
- **Not ruled out**: an unnoticed 30/60 difference in a case I did not trace, for example shot reach and position checks while the player is dashing past a shot at different frame offsets. I did not examine this. I could not produce a per-frame bot decision log because `bots.py` only prints summaries and I may not change it.
- **Cannot yet say** whether the dodger's room 3 result "should" be the 30 FPS or the 60 FPS result. Neither rate is defined as correct by the spec.

### 5. Severity and frequency

- **Severity**: medium for the project's evaluation. The discrepancy affects bot-based balance verification, not the player, as far as measured. If the cause turns out to be the build, it would be a constraint violation.
- **Frequency**: always reproduced at the given scripts (deterministic).

### 6. Effect on the 07 spec's acceptance criteria

`design/combat.md` criteria 13–16 depend on the dodger behaving the same at both rates, and the existing bots do not react to the new cues. They stay conditional. Criteria 1–12 cannot be run against build 0.4 at all (grub wind-up, aim cue, new rooms and variants are not in the build).

## Decisions already made

None.

## Constraints

- No change to the build or bots was made.
- Must play correctly at both 30 and 60 FPS (project.md#constraints).

## Open questions

- Is the room 3 / room 4 dodger split purely a bot-sensitivity effect? To settle it, either update the dodger with a frame-rate-independent reaction (an accumulated-time reaction delay like `play.py`'s 0.15 s) and re-run, or log the dodger's per-frame decisions, e.g. via a `gameplay-engineer` change to `bots.py`.
- Suggested check for that next run: a reaction-rule script in `play.py` (for example `when see * coming within 2 then dash aside` plus the walker-like rules) in room 3 at 30 and 60 FPS. If it gives the same outcome at both rates, the build is not the cause.
- Which of the two results should count as the dodger baseline for criterion 13? Studio / `game-designer` to say once the bot is fixed.

## Expected output

This report. Proposed next step by Studio:

- Route to `gameplay-engineer` to make the dodger bot frame-rate independent (accumulated-time reaction delay) and to add reaction to the new cues. Do not change the build for this.
- Afterwards, QA re-runs the bots at 30 and 60 FPS (`bots camper,walker,dodger`, `rooms 1-5`, both rates), and verifies criteria 13–16.

If a defect is later confirmed in the build, acceptance criteria for the fix:
1. The same bot script gives equal pass/fail per room at 30 and 60 FPS, with hearts lost within ±1 and clear time within ±0.5 s.
2. Traces of dash into a grub and through a shot show no hurt event during the dash at either rate.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: project.md#constraints, design/combat.md, repo/bots.py, repo/game.py, repo/play.py
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/06-studio-to-qa.md
>>>END
