# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/14-game-designer-to-studio.md, goals/G-001-combat-monotony/15-art-director-to-studio.md, goals/G-001-combat-monotony/16-qa-to-studio.md
next_seq: 17
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha 1f5fde8aa71a; run through the project's run commands)
log: last 5 of 5 entries in @log-recent; the full history is goals/G-001-combat-monotony/log.md

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/14-game-designer-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/15-art-director-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/16-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 17
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
- Observe (FPS divergence, qa): first pass done (08): simulation matches at 30/60 FPS in traced cases. After Build 0.5 the dodger agrees at both rates, but the walker bot differs in rooms 3–5. Open again: build defect or bot sensitivity (qa, handoff 13).
- Diagnose: done (04).
- Decide: skipped. No choice of direction or scope; all options stay within D-001 and the pillars. Returns here if the Build needs a new enemy type, a healing system or a new input, or if the designer's ruling changes scope.
- Design: reopened in part (handoff 11). Build 0.5 missed criterion 14 (walker cannot clear room 1) and used defaults for five spec gaps. Designer rules on criterion 14, the gaps, and how criterion 16 treats the walker.
- Plan: skipped. The approach reuses the enemy update loop. Returns here if the same criterion fails verification twice.
- Build: 0.5 implemented (10). Further Build only if the designer's ruling or QA's divergence report requires a change.
- Verify: visual review by art-director open now (handoff 12; the text view only describes cues). Full QA verification of criteria 1–16 is planned after the designer's ruling and QA's divergence report, so it runs against the final criteria and build.
- Play: planned. A fresh playtester judges the result, including rooms 4–5 and hand-timed play.
- Review: planned (`game-director`), experience Goal.

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
| 7a | Design (criterion 14, spec gaps) | game-designer | write-design-spec | open | 11-studio-to-game-designer.md |
| 7b | Verify (visual) | art-director | visual-review | open | 12-studio-to-art-director.md |
| 7c | Observe (walker 30/60 divergence) | qa | reproduce-defect | open | 13-studio-to-qa.md |
| 8 | Verify (criteria 1–16) | qa | verify-change | planned (after 7a, 7c; Build first if either needs it) | — |
| 9 | Play | playtester | playtest-session | planned | — |
| 10 | Review | game-director | review-outcome | planned | — |
| 11 | Next | studio | — | planned | — |

## Route changes

After step 6 (Build): partly fits. Criteria 1–12 and 15 look met per the engineer; 14 missed, five spec gaps used defaults, walker 30/60 divergence open. Added 7a Design (designer), 7c QA divergence check, and 7b art-director cue review in parallel. Full QA Verify waits so it runs against final criteria.

## Next action

Run the three open steps (parallel, each addressing its result to `studio`): game-designer 11-studio-to-game-designer.md, art-director 12-studio-to-art-director.md, qa 13-studio-to-qa.md. Then Route: if the designer's ruling or QA's report requires a change, Build again; otherwise open Verify (qa, criteria 1–16).

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

## 008-route · 2026-10-16

Status: active. Open: 09-studio-to-gameplay-engineer.md.

After steps 4a and 4b: both fit the plan. Plan is skipped (designer: no cross-system approach). QA found no build defect, so the bot fix is added to Build instead of a separate step. The art-director visual review is now planned.

## 010-route · 2026-10-16

Status: active. Open: 11-studio-to-game-designer.md, 12-studio-to-art-director.md, 13-studio-to-qa.md.

After step 6 (Build): partly fits. Criteria 1–12 and 15 look met per the engineer; 14 missed, five spec gaps used defaults, walker 30/60 divergence open. Added 7a Design (designer), 7c QA divergence check, and 7b art-director cue review in parallel. Full QA Verify waits so it runs against final criteria.
>>>END

<<<FILE goals/G-001-combat-monotony/14-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 14
from: game-designer
to: studio
stage: Verify
outcome: done
---
# 14: game-designer → studio — Criteria 14 and 16 ruled, five spec gaps confirmed; no build or bot change needed

## Task

Route the updated `design/combat.md` to QA for final verification of criteria 1–16 against build 0.5. Add the checks below to QA's list, including the walker 30/60 comparison already in progress (handoff 13).

## Context

G-001 (combat monotony). Handoff 11 asked for rulings on criterion 14 (walker misses rooms 1–2), criterion 16 (walker differs between rates) and the five defaults the engineer used.

## Findings

### What changed in `design/combat.md`

- **Criterion 14 changed.** Old: the walker loses at least 1 heart in rooms 1–2 and clears both. New, at each rate: the walker loses at least 1 heart in rooms 1–2 summed (no clear required); the dodger loses at most 1 and clears both. Observed: walker 5 lost at 30 FPS and 5 at 60 FPS; dodger 0 lost, both cleared. Met.
  - The reason is structural. A wind-up always comes before contact, so a player who ignores the cue and stands still takes one lunge per grub. Room 1 has three grubs and 3 hearts, so a bot that never adapts cannot clear it. That is the cost "ignoring the cue costs hearts" asks for. Making the walker survive would need either a cue-reading walker (it would stop being the "ignores cues" proxy) or a gentler room 1 (a balance change, not needed to meet the intent).
  - Player-observable behavior protected: ignoring the lunge cue costs hearts, and reading it makes the grub rooms safe. A human can learn the cue from the first hit; the bot cannot. I added this as an experience signal.
- **Criterion 16 changed.** It now has parts a–e:
  - 1–12 hold at both rates.
  - 13–15 are evaluated separately at each rate.
  - The dodger agrees across rates (same cleared set, hearts lost per room within 1).
  - The walker only has to meet 13 and 14 at each rate; its per-room numbers need not match. The reason is the 0.15 s decision grid (4.5 frames at 30 FPS, 9 at 60), which makes its sidestep timing sensitive to frame rounding.
  - A build defect is not excused: it is present if the same decision at the same game time (±1 frame) and the same state gives a different outcome, or if any of 1–11 fails at one rate.
- **Criterion 13** keeps its numbers but is stated to hold at each rate separately, with its protected behavior spelled out. Observed: walker 4 lost / 2 cleared at 30 FPS, 6 lost / 3 cleared at 60 FPS (top of the range), dodger 0 lost and 3/3, camper 0/3.
- **Criterion 6** now also says a swipe that kills a grub in wind-up kills it with no stagger and no lunge.
- **The five defaults, all confirmed** (written into the spec):
  1. A grub exactly on the player: wind-up aims right. Confirmed and added to the Grub rules and edge cases.
  2. Spitter cap wait of 0.2 s from the moment the cue would start. Confirmed. I also wrote down what the code does: the delay carries forward, so the spitter's next shot is 2.4 s after its actual shot. The criterion 11 first-shot times are not affected.
  3. Spitter index counts only spitters, in spawn order, also in the practice room. Confirmed. A defeated spitter does not renumber the others.
  4. A grub hit but not killed during lunge or recovery continues its phase. Confirmed, extended to Approach and Stagger (a hit during stagger does not extend it). Only a hit during wind-up changes the phase.
  5. No stagger if the swipe kills the grub. Confirmed.

### Does anything need to change in the build or the bots?

No. All five defaults match the spec as now written. Bot thresholds (0.15 s grid, walker 2.5 and 1.1 tiles, dodger rules) stay as they are. The criteria were changed to fit the build and the bots, not the other way round.

### What QA's final verification should check

1. Criteria 1–12 at both 30 and 60 FPS with practice-room scripts, including the new part of 6 (swipe that kills a grub in wind-up: dies, no stagger, no lunge).
2. Criteria 13, 14 and 15 with `bots camper,walker,dodger` and `rooms 1-5` at `fps 30` and at `fps 60` separately. Expected from handoff 11: 13 met at both (walker total 4 and 6), 14 met at both (walker lost 5 in rooms 1–2), 15 met at both. If walker totals in rooms 3–5 fall outside 3–6 on QA's run, report it; that is a tuning question for the designer, not a build defect.
3. Criterion 16 c: dodger agreement between rates, per room (cleared set equal, hearts lost within 1).
4. Criterion 16 e: the walker comparison from handoff 13 (`log on`, `bots walker`, `rooms 3`, both rates). Decide whether the differences come from decision times landing on different frames, or from a build defect, using the rule in criterion 16 e. Only a defect is a failure.
5. Edge cases newly written: grub at distance 0 aims right (cue shown); a spitter delayed by the cap shifts its later shots by the same delay; a defeated spitter does not renumber the others.
6. Check that `repo/manual.md` still matches the spec: marks `r` and `G`, the `~` line, the messages, wind-up lengths 0.5 / 0.35 / 0.7 s and the 0.4 s stagger. No spec change affects the manual.

## Decisions already made

- D-001: one attack button plus dash; no new input. Unchanged.
- Studio: Decide and Plan skipped. I did not write a Decision (no direction, scope, input or enemy-type change).

## Constraints

- Everything in the spec stays within the vision pillars and D-001, reuses existing systems, and holds at 30 and 60 FPS.
- No scope change, new enemy type, healing system or input was needed, so no Decide step is required.

## Open questions

1. If a human playtest later finds room 1 too punishing for a first-time player, the fix is a room change (for example a lone first grub). It needs a new spec step and is not requested now.
2. Art cue review (flash, line, glow) is still with the art-director.

## Expected output

QA's verification report on criteria 1–16, including the walker 30/60 finding. If QA finds a build defect, route it to gameplay-engineer. If the walker's rooms 3–5 totals leave the 3–6 range, route it back to the game-designer.

## Sender assessment

- I did not run `play` or `bots`; the rulings use the observed numbers in handoffs 10 and 11 and the code in `game.py` and `bots.py`.
- Confidence: high that criterion 14 as ruled is met and that the five defaults match the code. Medium on criterion 16 e: the sensitivity explanation is consistent with the code, but QA's logged comparison must confirm it.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md, repo/manual.md, repo/game.py, repo/bots.py, repo/play.py, repo/tests/test_game.py, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/11-studio-to-game-designer.md
>>>END

<<<FILE goals/G-001-combat-monotony/15-art-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 15
from: art-director
to: studio
stage: Verify
outcome: done
---
# 15: art-director → studio: Visual review of build 0.5 combat cues

## Task

Report on the readability and consistency of the build 0.5 threat cues, with player-observable requirements for the graphical build.

## Context

G-001 (combat monotony). Handoff 12 asked for a review of the grub wind-up and spitter aim cues against the art direction and pillar 3 (readable threats).

## Findings

**Basis and limits.** I reviewed the cue descriptions in handoff 12, `design/combat.md` and `repo/manual.md`. I did not run `play.py`. The build is text-only, so color, brightness and look are not verifiable yet. This is a design-level verdict for the cue forms, and graphical acceptance is still open.

**Verdict by question**

1. **Are the cue forms readable and consistent with the art direction?** Yes, with conditions.
   - Saturated orange-red against a dark cave fits the art direction. The forms (flash, lane, aim line, glow ramp) are appropriate and reuse simple assets.
   - The same hue is used for the grub cue, the aim line and the shot, so shape and motion must carry the differences (see problems 3 and 4).
2. **What the graphical implementation must satisfy.** See `design/combat-cues-visual-spec.md`, criteria V1–V12.

**Problems found, with where they occur**

1. **The grub lane must show its true width.** The combat design calls it a "thin line" but also says the danger is 0.6 tiles either side (1.2 wide). A hairline would make the sidestep requirement unreadable. Requirement: draw the lane at 1.2 tiles wide. This is a visual fix, with no rule change.
2. **The spitter glow starts at 0% brightness.** The text cue shows `brightness 0%` at the start, so the glow carries no information on the first frame. Requirement: a glow floor of at least 30%, and the aim line at full brightness from the first frame. The ramp then conveys time left.
3. **Grub lane vs spitter aim line vs shot.** All three are orange-red and the text view draws the lane and aim line with the same `~`. In the text view the `cue:` line resolves this, but a graphical build needs different shapes: a wide short band for the grub, a thin long line for the spitter, and a round moving core for the shot. The line must disappear when the shot fires.
4. **Threat color vs lantern.** The lantern is also warm. The threat cues must be self-lit, more saturated and redder than the lantern, and not dimmed by distance from the lantern. Spitters in the far corners of the room must still show their cue (rooms 3–5).
5. **Short Runner cue (0.35 s).** About 10 frames at 30 FPS, with no room for a fade-in. The cue must appear at full contrast on the first frame. Variants must differ by silhouette and cadence, not by hue.
6. **No "safe" state is specified.** The recovery and stagger windows are where the player is meant to swipe. The grub should clearly return to a neutral untinted look so the player knows it is safe.
7. **Flash rate.** Keep pulses at or below 3 Hz. Do not strobe, including for the Runner.

**Does any of this need a rule or timing change?** No. All seven points are visual. I do not ask the game-designer to change timings. The 0.35 s minimum wind-up remains workable if V3 is met. If playtesting shows Runner cues are still missed in graphics, the escalation is a wind-up change within the allowed 0.35–0.7 s range, which is the game-designer's call.

**Also noted.** The open question in `design/combat.md` about whether the `r` / `G` text marks suit the graphical build is answered: the graphical build should use silhouette and size instead (spec table). The text marks stay for the text view.

## Decisions already made

- D-001: one attack button plus dash (not affected).
- Art direction in project.md: warm lantern vs cold blue-black, with threats in saturated orange/red (applied above).

## Constraints

- No gameplay rules or parameters were changed. No new decision file was needed.
- The graphical cue appearance is not testable until a graphical build exists.

## Open questions

1. Route the spec's V1–V12 to whichever step implements the graphical cues. A visual review against a rendered build is still needed to confirm them.
2. QA can only verify timing (V12) in the text view. V1–V11 need screenshots or a rendered build.

## Expected output

The Studio keeps `design/combat-cues-visual-spec.md` as the visual acceptance basis for the cues. No change to `design/combat.md` is needed, except that its "Art cue details" open question can now point to this spec.

## Sender assessment

Confidence is medium-high on the form decisions and low on the final look until a rendered build exists. The largest risks are problem 1 (lane width) and problem 2 (glow floor), because both make the cue misleading rather than merely unattractive.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md
- Project: project.md#art-direction, project.md#constraints, design/combat.md, design/combat-cues-visual-spec.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/12-studio-to-art-director.md
>>>END

<<<FILE goals/G-001-combat-monotony/16-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 16
from: qa
to: studio
stage: Observe
outcome: done
---
# 16: qa → studio — Walker 30/60 FPS divergence: reproduced and deterministic. No build defect found; the evidence points to bot decision timing, but the full 16e check is not closed.

## Task

Find out whether the walker's different results at 30 and 60 FPS in rooms 3–5 come from the build or from the bot. Report only; no code was changed.

## Context

G-001, build 0.5. design/combat.md criterion 16e requires QA to confirm that the walker's differences come from bot timing, and not from the same decision at the same game time and from the same positions giving a different outcome. I used `run_bots` with `log on`. `run_trace` and `run_play` cannot replay a bot's decisions, and `bots.py` logs actions only, not positions. That limits what could be shown (see "What is not proven").

## Findings

### 1. Reproduction

Commands (script files, one per rate):

```text
bots walker
rooms 1-5
fps 30        # second script: fps 60
log on
```

Command: `python3 bots.py {script}`. Results match the report exactly, hearts lost in rooms 1/2/3/4/5:

| Rate | Walker per room | Cleared |
|---|---|---|
| 30 FPS | 3✗ 2✓ 0✓ 1✓ 3✗ | 3/5, 9 lost |
| 60 FPS | 3✗ 2✓ 2✓ 2✓ 2✓ | 4/5, 11 lost |

- **Deterministic:** the game is headless and fixed-step, and the bot output was identical across the separate runs with and without `log on`. The dodger agrees at both rates: 0 lost, 5/5 cleared (dashes 35 at 30 FPS, 48 at 60 FPS).
- The camper also differs between rates (room 2: cleared at 30, not cleared at 60). 16c–e do not cover the camper. It shares the same decision grid, so the same explanation applies.

### 2. Where the runs first differ

**The decision grid is the same at both rates.** The bot's clock advances in exact 0.15 s steps (`Brain.due`), and a decision is made on the first frame at or after each grid time.
- At 60 FPS decisions fall on 0.00, 0.15, 0.30…
- At 30 FPS they fall on the next frame boundary: 0.00, 0.17, 0.30, 0.47, 0.60, 0.77…, a delay of 0 to 1 frame (0.033 s).
- This is the "up to frame rounding" behaviour described in the README.

**Room 1, the earliest and clearest divergence, at 0.30 s.**
- At 0.30 s the 60 FPS walker logs "face and swing at grub". The 30 FPS walker logs "walk to grub" and does not swing until 0.47 s.
- The walker picks "swing" when the nearest grub is closer than 2.5 tiles (`coming = distance < 2.5`).
- By arithmetic: the nearest grub is the one at (8,0), 4 tiles away. At 0.30 s the player has closed 1.2 tiles and the grub 0.3 tiles, so the distance is 4 − 1.5 = 2.5 tiles. That is exactly the threshold.
- **Hypothesis, not verified:** floating-point accumulation over 9 steps at 30 FPS versus 18 steps at 60 FPS lands on opposite sides of 2.5. If so, the cause is the bot's hard threshold at an exact tie, and not game behaviour.
- Everything later in room 1 follows from that one decision: 4 attacks at 60 FPS versus 5 at 30 FPS, and 5.2 s versus 4.9 s. The final result, 3 hearts lost and not cleared, is the same at both rates.

**Room 3 (spitters): the same action sequence, then different damage.**
- Up to 2.10 s the two logs contain the same actions: 12× walk to spitter, sidestep shot at 1.80, sidestep shot at 1.95 (60) or 1.97 (30), walk at 2.10. The only differences are the grid rounding.
- At 60 FPS there are no decisions at 2.25 and 2.40. The bot skips decisions while the player is stunned, so a shot hit the player between 2.10 and 2.25 s (stun 0.3 s; the next decision is at 2.57 s). Room 3 ends with 2 hearts lost, both from shots.
- At 30 FPS the walker logs "sidestep shot in flight" at 2.27 s. It was not hit, and room 3 ends with 0 hearts lost.
- From there the rooms play out differently. After a hit the player is stunned, so its position and timing are shifted for the rest of the room.

**Rooms 4 and 5:** the divergence follows the same pattern, with different shot and grub hits at different moments.
- Room 4: 30 FPS had 1 heart lost (grub); 60 FPS had 2 (grub, shot).
- Room 5: 30 FPS had 3 lost (grub 2, shot 1) and was not cleared; 60 FPS had 2 lost (grub 2) and was cleared.
- After the first difference, the shot-hit and grub-hit sequences are different. I did not trace the first difference in these rooms separately.

### 3. Build checks (all consistent with a bot-timing cause so far)

- `python3 -m unittest discover -s tests` is part of the existing suite. It includes timing, dash, sidestep and spitter-stagger tests at both rates, and the walker test is marked `expectedFailure`. I did not re-run it in this step (it was run in earlier steps); I rely on its existing assertions only as context.
- The simulation advances all durations on accumulated time. In the code I read, the grub walk, wind-up, lunge, the spit timer and the shot motion all scale with `dt`.
- No result in the logs shows a behaviour that cannot be explained by a one-frame shift in a decision or by a threshold.

### 4. What is not proven

- **Room 3 and the shot hit:** the logs give action names and times only. They do not give player positions or shot positions. I could not show the "same decision at the same game time (±1 frame) from the same positions gives a different outcome" test of 16e, either way.
- **Hypothesis (labelled as such):** the 60 FPS hit and the 30 FPS miss can be a sampling effect. Contact is a distance check each frame (reach 0.4) against a shot moving 0.1 tile per frame at 30 FPS and 0.05 at 60 FPS, with the player moving 0.13 or 0.07 tile per frame. A pass that only grazes the 0.4 reach for a fraction of a frame can be caught at one rate and missed at the other. That would make the simulation not a fault in itself, but it does mean a graze result depends on the frame rate. I did not check whether this is what happened.
- I did not check criteria 1–11 in this step, so 16a is untested here.

### 5. Verdict on the question

- Reproducible and deterministic: yes.
- First divergence point: room 1, 0.30 s, a bot threshold at an exact tie (distance 2.5), the first differing decision; room 3, between 2.10 and 2.25 s, a shot hit at 60 FPS and not at 30 FPS.
- Cause: bot decision timing is the best-supported cause (room 1 is concrete). **No build defect is demonstrated.** A build cause for room 3 cannot be excluded without positions.
- Severity if the cause is the bot only: low. It affects the balance-proxy numbers and not a player. Frequency: always, with these scripts.

## Preliminary read of criteria 13–16 from this data (not the full verification)

Per rate, from the outputs above:
- **13** (rooms 3–5 summed): 30 FPS walker lost 4 hearts and cleared 2/3 (rooms 3 and 4); 60 FPS walker lost 6 and cleared 3/3. Both are inside the limits (3–6 lost, ≥2 cleared). Dodger lost 0 and cleared 3/3 at both rates. Camper cleared 0/3 at both. 13 looks satisfied at both rates, with the 60 FPS walker at the upper limit of 6.
- **14** (rooms 1–2): walker lost 5 at both rates; dodger lost 0 and cleared both. Satisfied.
- **15:** dodger dashes in rooms 3/4/5 are 8/7/11 at 30 FPS and 10/8/14 at 60 FPS. Satisfied.
- **16c:** dodger cleared 5/5 at both rates with 0 hearts lost per room (clear times and dash counts differ, which 16c does not constrain). Satisfied.
- **16d and e:** walker per-room differences are allowed by 16d. 16e stays open as described in section 4.

## Decisions already made

- D-001: one attack button plus dash; no new input. Not affected.

## Constraints

- No code was changed. Intended behaviour is defined by design/combat.md and repo/manual.md.

## Open questions

1. Do we accept the bot-timing explanation for 16e, or do we want it closed by evidence? To close it, `gameplay-engineer` would extend the `log on` output (a bot-tooling change, not a build change) with player position, the nearest enemy distance, and shot positions at each decision, plus the hit time. QA would then compare the room 3 decision at 2.10 s at both rates. Optionally also make the walker's `distance < 2.5` tie robust, for example with a small epsilon. That would remove the room 1 knife edge but would not by itself make the walker rate-independent.
2. Should the existing `expectedFailure` walker test in `tests/test_game.py` be kept? It still describes the walker as "unexplained". Its comment can be updated to say "bot decision timing, see handoff 16", but whether to remove it is for `gameplay-engineer` and Studio.
3. Is it acceptable that a graze of the shot reach at the contact edge can hit at one frame rate and miss at the other? Spec design/combat.md only claims that nothing tunnels. If a stricter rule is wanted, `game-designer` states it, then criteria for a swept contact test would be added. No acceptance criteria for a fix are written now, because no build defect is confirmed.

## Expected output

This report. Proposed routing: Studio decides on open question 1 (instrumented bot log plus QA re-check) before 16 can pass. Full verification of 1–16 follows in a later step; 16e is the only item known to be pending.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md, repo/manual.md, repo/README.md, repo/bots.py, repo/game.py, repo/play.py, repo/tests/test_game.py, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/13-studio-to-qa.md
>>>END
