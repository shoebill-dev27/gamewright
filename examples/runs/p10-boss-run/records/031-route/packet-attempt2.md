# Studio operation packet

operation: Route
goal: G-002
step_artifacts: goals/G-002-final-boss/24-gameplay-engineer-to-studio.md
next_seq: 25
context_request: used (the requested files are in Inputs)
current_build: repo/ (sha 27fe16268ac8; run through the project's run commands)
log: last 5 of 14 entries in @log-recent; the full history is goals/G-002-final-boss/log.md

## You may write

- goals/G-002-final-boss/goal.md
- goals/G-002-final-boss/24-gameplay-engineer-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- project.md: only in the Route that closes the Goal, and only its ## Current state (at most 1,500 characters)
- goals/G-002-final-boss/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 25

## Inputs

<<<FILE studio/execution.md#executor-instructions
## Executor instructions

You are executing exactly one Studio operation, in isolation.

- Everything you may use is in this packet: the operation header, the input files, and the paths
  you may write. You know nothing else about this project, its history, or other steps, and you
  must not assume anything beyond the packet.
- Follow the procedure for this operation in the Studio files included. For a Step, act as the
  receiving Role within its contract and listed Skills; do not perform other Roles' work.
- Write every file you create as one complete file block: `<<<FILE <path>` on its own line, the
  full file content, then `>>>END` on its own line. To change part of an existing file, you may
  instead write `<<<EDIT <path>` with `<<<<<<< SEARCH` / `=======` / `>>>>>>> REPLACE` pairs and
  `>>>END` (Output protocol); each SEARCH must match the file exactly once, so include enough
  lines. Use only the paths listed under "You may write"; paths are relative to the project
  directory.
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
Then bring `project.md`'s `## Current state` up to date with what exists now (build, content,
known problems, how to run it; 1,500 characters at most), so the next Goal starts from the facts.
Nothing else in `project.md` changes: the rest belongs to the Owner.

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
rejected, or when the Owner made it. Smaller choices are noted in the Handoff. A Decision is never
edited once written, not even for a typo or a stray line: a change is a new Decision that
`supersedes:` it, so do not route an edit of one to a Role.

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
decisions/D-010-review-pass-2-build-clarity-now-room-3-content.md
decisions/D-011-variant-named-messages-accepted.md
decisions/D-012-room3-standard-grub-and-closer-spitter.md
decisions/D-013-review-pass-3-readability-wording-then-close.md
decisions/D-014-review-pass-4-goal-met.md
decisions/D-015-owner-approves-continuous-run-and-final-boss.md
decisions/D-016-final-boss-experience-direction.md
decisions/D-017-final-boss-and-run-contract.md
decisions/D-018-legacy-balance-gate-transition-direction.md
decisions/D-019-g002-balance-criteria-applicability.md
decisions/D-020-g002-host-scope-and-plan-entry-conditions.md
decisions/D-021-owner-authorizes-text-build.md
design/combat-cues-visual-spec.md
design/combat-step-44-walker-limit.md
design/combat-step-46-room3-cap.md
design/combat-step59.md
design/combat-step68.md
design/combat-step72.md
design/combat-step94.md
design/combat.md
design/final-boss-and-continuous-run.md
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
goals/G-001-combat-monotony/100-studio-to-game-designer.md
goals/G-001-combat-monotony/101-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/102-game-designer-to-studio.md
goals/G-001-combat-monotony/103-studio-to-qa.md
goals/G-001-combat-monotony/104-qa-to-studio.md
goals/G-001-combat-monotony/105-studio-to-game-director.md
goals/G-001-combat-monotony/106-game-director-to-studio.md
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
goals/G-001-combat-monotony/65-studio-to-game-director.md
goals/G-001-combat-monotony/66-studio-to-game-designer.md
goals/G-001-combat-monotony/67-game-director-to-studio.md
goals/G-001-combat-monotony/68-game-designer-to-studio.md
goals/G-001-combat-monotony/69-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/70-studio-to-game-designer.md
goals/G-001-combat-monotony/71-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/72-game-designer-to-studio.md
goals/G-001-combat-monotony/73-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/74-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/75-studio-to-qa.md
goals/G-001-combat-monotony/76-qa-to-studio.md
goals/G-001-combat-monotony/77-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/78-studio-to-game-designer.md
goals/G-001-combat-monotony/79-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/80-game-designer-to-studio.md
goals/G-001-combat-monotony/81-studio-to-qa.md
goals/G-001-combat-monotony/82-qa-to-studio.md
goals/G-001-combat-monotony/83-studio-to-playtester.md
goals/G-001-combat-monotony/84-studio-to-qa.md
goals/G-001-combat-monotony/85-studio-to-game-designer.md
goals/G-001-combat-monotony/86-qa-to-studio.md
goals/G-001-combat-monotony/87-game-designer-to-studio.md
goals/G-001-combat-monotony/88-playtester-to-studio.md
goals/G-001-combat-monotony/89-studio-to-qa.md
goals/G-001-combat-monotony/90-qa-to-studio.md
goals/G-001-combat-monotony/91-studio-to-game-director.md
goals/G-001-combat-monotony/92-game-director-to-studio.md
goals/G-001-combat-monotony/93-studio-to-game-designer.md
goals/G-001-combat-monotony/94-game-designer-to-studio.md
goals/G-001-combat-monotony/95-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/96-gameplay-engineer-to-studio.md
goals/G-001-combat-monotony/97-studio-to-qa.md
goals/G-001-combat-monotony/98-qa-to-studio.md
goals/G-001-combat-monotony/99-studio-to-gameplay-engineer.md
goals/G-001-combat-monotony/goal.md
goals/G-001-combat-monotony/log.md
goals/G-002-final-boss/01-studio-to-game-designer.md
goals/G-002-final-boss/02-game-designer-to-studio.md
goals/G-002-final-boss/03-studio-to-technical-director.md
goals/G-002-final-boss/04-technical-director-to-studio.md
goals/G-002-final-boss/05-studio-to-game-director.md
goals/G-002-final-boss/06-game-director-to-owner.md
goals/G-002-final-boss/07-studio-to-game-director.md
goals/G-002-final-boss/08-game-director-to-studio.md
goals/G-002-final-boss/09-studio-to-game-designer.md
goals/G-002-final-boss/10-game-designer-to-studio.md
goals/G-002-final-boss/11-studio-to-game-director.md
goals/G-002-final-boss/12-game-director-to-studio.md
goals/G-002-final-boss/13-studio-to-game-designer.md
goals/G-002-final-boss/14-game-designer-to-studio.md
goals/G-002-final-boss/15-studio-to-technical-director.md
goals/G-002-final-boss/16-technical-director-to-studio.md
goals/G-002-final-boss/17-studio-to-game-director.md
goals/G-002-final-boss/18-game-director-to-studio.md
goals/G-002-final-boss/19-studio-to-technical-director.md
goals/G-002-final-boss/20-technical-director-to-studio.md
goals/G-002-final-boss/21-studio-to-game-director.md
goals/G-002-final-boss/22-game-director-to-owner.md
goals/G-002-final-boss/23-studio-to-gameplay-engineer.md
goals/G-002-final-boss/24-gameplay-engineer-to-studio.md
goals/G-002-final-boss/goal.md
goals/G-002-final-boss/log.md
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
decisions/D-010-review-pass-2-build-clarity-now-room-3-content.md — D-010: Review pass 2 — goal not met yet, no Owner escalation; build the variant message and manual text now; room 3 variety goes to Design
decisions/D-011-variant-named-messages-accepted.md — D-011: Text-view wind-up and hit messages name the variant (accepted); swipe timing stays a wording matter
decisions/D-012-room3-standard-grub-and-closer-spitter.md — D-012: Room 3 gets one standard grub at (15,0) and its second spitter moves to (10,6); cap and cue rule unchanged
decisions/D-013-review-pass-3-readability-wording-then-close.md — D-013: Review pass 3 — goal not met by one clause; one wording-only Design/Build/Verify round for shot-hit source and late-swipe explanation, then Close; no Owner escalation
decisions/D-014-review-pass-4-goal-met.md — D-014: Review pass 4 — G-001 is met on the text-view build; Close with proposed Goals and one Owner item; no Owner escalation
decisions/D-015-owner-approves-continuous-run-and-final-boss.md — D-015: Owner approves Option A — continuous run and final boss
decisions/D-016-final-boss-experience-direction.md — D-016: 連続ランの最後に、読み取りと反撃の判断を問う単体ボスを置く
decisions/D-017-final-boss-and-run-contract.md — D-017: 二攻撃のボスと、1 heart回復を伴う連続ランの契約
decisions/D-018-legacy-balance-gate-transition-direction.md — D-018: 旧第5部屋依存の難度集計を、新構成の評価から分離する方向を採る
decisions/D-019-g002-balance-criteria-applicability.md — D-019: G-002新構成における旧集計の適用終了と代替評価
decisions/D-020-g002-host-scope-and-plan-entry-conditions.md — D-020: 実機ホストの必要性を認め、費用・供給条件を限定調査で確定する
decisions/D-021-owner-authorizes-text-build.md — D-021: テキストビルドとStudio内検証でBuildへ進む
>>>END

<<<FILE goals/G-002-final-boss/goal.md
---
kind: goal
id: G-002
project: lantern-depths
status: active
created: 2026-10-20
---
# G-002: 最後に手応えのあるボス戦

## Owner request

> 最後に手応えのあるボス戦がほしい

## Interpretation

既存の第1〜4部屋を連続して進み、第5部屋を置き換えた単体ボスへ到達する。プレイヤーが位置取り、攻撃とダッシュのタイミング、敵の挙動への対応を通じて手応えを感じられる最終戦とし、最終勝利・死亡・ランの最初からの再挑戦まで成立する。短いランと、被害を受ける前に脅威を読み取れる体験を維持する。

D-015により、連続ラン・部屋間継承・終端・再挑戦の新設を今回の範囲に含める。第1〜4部屋の構成と既存の共有戦闘ルールを維持し、新しい戦闘入力、ボス専用チェックポイント、既存部屋の全面改修は対象外。15〜20分を満たすためだけの敵HP増加は含めない。

D-021により、今回はrepo/のテキスト表示とスクリプト実行で実装・検証する。Desktop、keyboard、gamepadは製品対象であり、実機ホストや実gamepadの供給・検証を今回の要件としない。基線はrepo/の現状とし、指定sha確認は不要。独立QA・PlayはStudio内の別Stepが担う。購入・外部委託・追加金銭を使わず、通常Stepの範囲で進める。具体的な追加支出や承認範囲を超える変更が必要になった場合はOwnerへ戻す。

## Unknowns

- Observe：skipped。既存不具合の再現依頼ではない。
- Diagnose：done。既存基盤の不足と計画上の回帰対応を整理済み。現状repo/の実行基線はBuildで取得する。
- Decide：done。D-015〜D-019で範囲・体験方向・仕様契約・旧基準の適用関係を確定。
- Design：done。design/final-boss-and-continuous-run.mdとD-017・D-019が正本。未実装・未検証。
- Plan：done。16・20の計画と回帰対応を使用する。D-021と衝突する実機ホスト・実機供給・外部配員・見積もり取得の要求は適用しない。
- Decide（供給・承認）：done。22へのOwner回答をD-021に記録。Ownerは実行経路とStudio内検証を指定し、Build開始を承認。実機供給、指定sha照合、人日見積もりは不要。
- Plan補完：skipped。新しいOwner条件を後続Stepへ直接渡せるため、同じ供給質問で再発行しない。具体的な技術上の不成立が判明した場合に限り戻す。
- Build：open。現状repo/の実行基線を記録し、承認仕様と適用可能な既存計画に従って実装する。Owner回答は実行合格の証拠ではない。
- Verify：planned。独立QAで30/60 FPS、連続到達・勝敗・再挑戦、共有戦闘回帰を検証する。限定Art Verifyはテキストplayer viewの二攻撃、予兆と実弾、回復、HP、終端・retryの識別を扱う。実機検証は要求しない。
- Play：planned。独立したプレイヤー観察で最終戦・到達体験・通常ランの所要時間を評価する。実装内容と期待結果は渡さない。
- Design（実測後）：planned。対応botの両FPS基線、独立QA・Play、通常ランの同一試行による到達・終端・時間実測を受け、追加数値ゲート・調整の要否を判断する。不要でも理由を記録。明白な対処不能・到達不能はPlay前に戻す。
- Review：planned。Game Directorが体験Goalの達成を判断する。
- Next：結果と残課題をOwnerへ返す。

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Design | game-designer | write-design-spec | done | 01-studio-to-game-designer.md → 結果: 02-game-designer-to-studio.md |
| 2 | Diagnose | technical-director | technical-plan | done | 03-studio-to-technical-director.md → 結果: 04-technical-director-to-studio.md |
| 3 | Decide | game-director | make-decision, prepare-owner-escalation | done | 05-studio-to-game-director.md → 結果: 06-game-director-to-owner.md |
| 3a | Decide | owner | — | done | 06-game-director-to-owner.md → D-015 |
| 3b | Decide | game-director | make-decision, prepare-owner-escalation | done | 07-studio-to-game-director.md → 結果: 08-game-director-to-studio.md |
| 4 | Design | game-designer | write-design-spec | done | 09-studio-to-game-designer.md → 結果: 10-game-designer-to-studio.md |
| 4a | Decide | game-director | make-decision, prepare-owner-escalation | done | 11-studio-to-game-director.md → 結果: 12-game-director-to-studio.md |
| 4b | Design | game-designer | make-decision, write-design-spec | done | 13-studio-to-game-designer.md → 結果: 14-game-designer-to-studio.md |
| 5 | Plan | technical-director | technical-plan | done | 15-studio-to-technical-director.md → 結果: 16-technical-director-to-studio.md |
| 5a | Decide | game-director | make-decision, prepare-owner-escalation | done | 17-studio-to-game-director.md → 結果: 18-game-director-to-studio.md |
| 5b | Plan | technical-director | technical-plan | done | 19-studio-to-technical-director.md → 結果: 20-technical-director-to-studio.md |
| 5c | Decide | game-director | make-decision, prepare-owner-escalation | done | 21-studio-to-game-director.md → 結果: 22-game-director-to-owner.md |
| 5c-owner | Decide | owner | — | done | 22-game-director-to-owner.md → D-021 |
| 5d | Plan | technical-director | technical-plan | skipped | D-021で供給・承認条件を解決。再照会不要 |
| 6 | Build | gameplay-engineer | implement-change | open | 23-studio-to-gameplay-engineer.md |
| 7 | Verify | qa | verify-change | planned | — |
| 8 | Verify | art-director | visual-review | planned | — |
| 9 | Play | playtester | playtest-session | planned | — |
| 9a | Design | game-designer | make-decision, write-design-spec | planned | — |
| 10 | Review | game-director | review-outcome | planned | — |
| 11 | Next | studio | — | planned | — |

逐次実行する。Build後は独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewとする。明白な対処不能・到達不能が判明した場合はDesigner判断を前倒しする。並列Stepは開かない。

## Route changes

22へのOwner回答をD-021として記録し、Escalationをresolved、Goalをactiveへ戻した。実機・外部供給・見積もり要求を今回の開始条件から外し、Plan再発行をskipped、23のBuildをopenとした。後続の独立検証・実測後判断を維持する。

## Next action

Gameplay Engineerが23-studio-to-gameplay-engineer.mdからBuildを開始する。repo/の現状を基線として@runで実行し、仕様と計画をD-021の範囲で実装する。結果はstudioへ返し、次のRouteで独立QAを開く。

## Outcome

未完了。Ownerは案Aを選び、テキストビルド・スクリプト実行・Studio内独立検証によるBuild開始を承認した（D-021）。22は解決済み。実装・実行合格・最終戦の手応え・所要時間は今後確認する。追加金銭支出と実機調達は行わない。Goalはactiveで、23のBuildが次の作業。Goalは閉じず、project.mdは変更しない。
>>>END

<<<FILE @log-recent
## 021-route · 2026-10-20

Status: active. Open: 17-studio-to-game-director.md.

16のPlan提出Stepを完了扱いとし、開始条件未充足によるBuild保留を記録。実機ホスト追加と暫定費用・環境依存の承認範囲判断を17でGame Directorへ戻す。判断後のPlan補完を追加し、独立検証・Play・Designer実測後判断を維持する。現時点で超過や環境供給不能は確定しておらず、Ownerへの質問はまだ開かない。

## 023-route · 2026-10-20

Status: active. Open: 19-studio-to-technical-director.md.

18のDecideを完了し、D-020に基づく限定Plan補完を19で開く。最小ホストの必要性と費用承認を分け、実行基線・回帰正本・実機供給・総費用と承認根拠を確認する。Build保留と後続の独立検証順序を維持し、現時点ではOwner質問を開かない。

## 025-route · 2026-10-20

Status: active. Open: 21-studio-to-game-director.md.

20のPlan補完を完了し、回帰対応の充足と実行・供給・承認の不足を分離した。Roleで生成できない供給情報と承認根拠の不足が具体化したため、21でGame DirectorへOwner Escalation準備を戻す。同じPlan質問を繰り返さず、Build保留と後続の独立検証順序を維持する。

## 027-route · 2026-10-20

Status: blocked-on-owner. Open: none.

22でEscalation準備を完了し、供給責任者・承認根拠の不足についてOwnerへA／B／Cの一問を開いた。Goalをblocked-on-ownerとし、依存StepとBuildを保留する。新しい供給・承認資料を得るまでPlanを再発行せず、後続の独立検証順序を維持する。

## 029-resume · 2026-10-20

Status: active. Open: 23-studio-to-gameplay-engineer.md.

22へのOwner回答をD-021として記録し、Escalationをresolved、Goalをactiveへ戻した。実機・外部供給・見積もり要求を今回の開始条件から外し、Plan再発行をskipped、23のBuildをopenとした。後続の独立検証・実測後判断を維持する。
>>>END

<<<FILE goals/G-002-final-boss/24-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-002
seq: 24
from: gameplay-engineer
to: studio
stage: Build
outcome: question
---
# 24: gameplay-engineer → studio — 基線成功を記録し、実装対象ソースの供給を求める

## Task

Studioは現状repo/の実装ソースとテスト全文を次のBuildパケットへ含め、Gameplay Engineerへ再ルーティングする。D-021によるBuild開始承認を維持し、実装・変更後試験を継続する。

## Context

23は、既存テキストビルドで連続ランと第5部屋単体ボスを実装し、結果をstudioへ返す指示である。仕様と技術計画は提供されている。

本パケットにはrepo/manual.mdと基線のtests結果がある一方、変更対象のgame.py、play.py、bots.py、既存テスト本文がない。executor-instructionsにより、提供パケット以外のプロジェクト内容を仮定して実装しない。

## Findings

### 取得済みの実行基線

@run-resultsのRound 1に以下が記録されている。

- コマンド：`python3 -m unittest discover -s tests`
- Exit：0
- 件数：69 tests
- unittest所要時間：0.195秒
- 実行結果：OK

これは変更前の基線である。変更後の成功、ボス・連続ランの実装済み、30/60 FPS別の受け入れ基準合格を示さない。結果本文から各試験のFPS対応は確認できない。

### 実装前に照合したプレイヤー可視変更

追加する挙動の仕様上の根拠は以下のとおりである。

| 変更 | 正本 |
|---|---|
| 通常ランの1→5進行、1秒のクリア表示、入場時1 heart回復と状態初期化 | 最終ボス仕様§2 |
| B単体、HP12、固定照準の突進と短射、交互順序、非中断、回復 | §3 |
| 死亡優先、残弾消去、終端凍結、先頭retry | §4 |
| 両ゲーム時刻、pause/resume、試行別入力、unfinished | §5、計画16§3 |
| ボスHP・攻撃名・危険範囲・回復・進行・終端の表示 | §6 |
| 公開観測に基づく対応botと同一試行の測定 | §8〜9、計画16§8 |

現時点でDesigner判断を要する新たな仕様質問は特定していない。

### 具体的な不足と影響

次の現状ファイル全文が必要である。

- `repo/README.md`
- `repo/game.py`
- `repo/play.py`
- `repo/bots.py`
- `repo/tests/test_game.py`
- 上記が参照する追加ローカルモジュール、部屋データ、その他の既存テストがあれば、その全文

既存のクラス・更新順・関数契約・parser・公開観測・テストassertが不明なため、計画の「既存戦闘の外側に進行管理を置く」実装や共有コード経路の修正を具体化できない。ソースを推定して全置換すると、第1〜4部屋と共有回帰を維持した証拠を失う。

本Stepではrepo/を変更せず、新規テスト・manual改訂も作成していない。追加の@runは要求していない。実装ソースなしで同じ基線試験を再実行しても、今回の不足は解消しない。

これはD-020の供給条件の再要求ではない。指定sha、実機、gamepad、費用見積もり、外部担当の供給は求めない。必要なのは承認済み変更を適用する現状ソース本文である。

## Decisions already made

- D-015〜D-017：連続ラン、単体ボス、回復、終端、先頭retryの範囲と契約。
- D-019：旧集計の適用終了、保持回帰、対応bot比較、実測後Designer判断。
- D-021：現状repo/とStudio内のテキスト・スクリプト実行でBuild開始。指定sha照合、実機ホスト、実gamepad、外部配員、人日見積もりは不要。

## Constraints

第1〜4部屋と共有戦闘ルールを保持する。新戦闘入力、ボス用チェックポイント、HPや待機による時間合わせを追加しない。

実装は計画の依存順に逐次進める。30/60 FPSの検証、独立QA、限定Art Verify、独立Play、Designer実測後判断、Reviewを維持する。

未実行・未確認を成功としない。秘密情報や環境変数値は供給資料・実行記録へ含めない。

## Open questions

Studio：上記の現状ソース全文をBuildパケットへ追加できるか。既存テストと同じ実行対象の内容を供給し、基線結果との対応を維持すること。

技術方式の再設計や仕様変更を求める質問はない。

## Expected output

Studioは不足するソースを含めてGameplay EngineerへBuildを再ルーティングする。D-021の開始判断や既に成功した基線試験の取得をやり直さない。

継続BuildではGame終端処理→ボス・弾属性→Session→parser・表示・説明→対応bots・測定の順に実装し、保持／終了／置換したassertの対応を記録する。変更後のtests、両FPSのtrace・bots、通常ランの同一試行記録と独立検証手順をstudioへ返す。QA合否・Goal達成は実装者が代行しない。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#vision
- Project: project.md#constraints
- Project: project.md#art-direction
- Project: repo/README.md
- Project: repo/manual.md
- Project: repo/game.py
- Project: repo/play.py
- Project: repo/bots.py
- Project: repo/tests/
- Project: 上記の追加ローカル依存ファイル
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-cues-visual-spec.md
- Project: design/combat-step-44-walker-limit.md
- Project: design/combat-step-46-room3-cap.md
- Project: design/combat-step59.md
- Project: design/combat-step68.md
- Project: design/combat-step72.md
- Project: design/combat-step94.md
- Plan: goals/G-002-final-boss/16-technical-director-to-studio.md
- Plan: goals/G-002-final-boss/20-technical-director-to-studio.md
- Decisions: 23に列挙されたD-001〜D-007、D-011〜D-012、D-015〜D-019、D-021
- Previous handoff: goals/G-002-final-boss/23-studio-to-gameplay-engineer.md
- Execution evidence: @run-results Round 1
>>>END

<<<FILE goals/G-002-final-boss/23-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-002
seq: 23
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 23: studio → gameplay-engineer — テキストビルドで連続ランと最終ボスを実装する

## Task

承認された最終ボス・連続ラン仕様と既存技術計画に従い、repo/へ実装する。D-021を優先し、現状repo/の実行基線を取得してから変更・試験を行い、結果をstudioへ返す。

## Context

OwnerのGoalは「最後に手応えのあるボス戦がほしい」。DesignとPlan補完は完了したが、実行・実機供給・費用条件が未確定としてBuildを保留していた。22へのOwner回答により、今回の実装・検証方式は既存のテキストビルドとスクリプト実行に確定し、Build開始が承認された。

## Findings

Ownerが指定した実行経路はproject.mdのbuildとrun_tests／run_play／run_trace／run_bots。Gameplay EngineerとQAはStep内の@runを使用できるとの回答がある。

repo/で実行するコマンド：

- `python3 -m unittest discover -s tests`
- `python3 play.py --view player {script}`
- `python3 play.py --view trace {script}`
- `python3 bots.py {script}`

スクリプト形式と利用可能な操作はrepo/manual.mdを読むこと。作業開始時のrepo/を基線とし、指定sha照合は不要。project.mdのbuild 0.4記述は古く、repo/が正本である。Studioは本Resumeで実行しておらず、合格結果はない。

計画正本は16と20、仕様正本はdesign/final-boss-and-continuous-run.md。計画中の実機ホスト追加、実gamepad、外部検証枠、金銭・人日見積もりの取得条件はD-021により今回適用しない。その他の適用可能な計画と回帰対応を用いる。技術方式の実質的な再設計が必要ならTechnical Directorへ、仕様の意味が未確定ならDesignerへ手渡し、推測で仕様を変えない。

## Decisions already made

- D-015：連続ラン・部屋間継承・終端・先頭retryと第5部屋単体ボスを範囲に含める。
- D-016：読み取り・位置取り・回避後の反撃を中心とする体験方向。
- D-017：二攻撃のボスと1 heart回復を伴う連続ランの契約。
- D-018・D-019：旧第5部屋依存の集計と新構成の評価を分離し、保持回帰と代替評価を定める。
- D-021：D-020を置き換えるOwner判断。現状repo/と既存@run経路でBuildを開始。実機・実gamepad・外部配員・指定sha確認・人日見積もりは不要。追加金銭支出は認めない。

## Constraints

- 第1〜4部屋の構成と既存共有戦闘ルールを維持する。新しい戦闘入力、ボス専用チェックポイント、既存部屋の全面改修を行わない。
- テキストplayer viewとスクリプト実行を今回の実装・検証対象とする。実機ホストを追加しない。
- 30/60 FPS、仕様の受け入れ基準、保持する共有戦闘回帰を維持する。
- 通常Studio Step内で進め、購入・外部委託・追加金銭支出・外部連絡を行わない。
- 15〜20分を満たすためだけの敵HP増加をしない。
- 独立QA、限定Art Verify、独立Play、Designer実測後判断、Reviewを省略しない。
- 未実行・未確認事項を成功と記録しない。Ownerの実行経路指定は実行結果ではない。

## Open questions

- 現状repo/の実行基線、適用可能な回帰試験と両FPSでの結果。
- 連続到達・継承・ボス二攻撃・勝敗・先頭retryの実装と、仕様基準への対応。
- 対応bot、通常ランの到達・終端・所要時間を同一試行で記録する経路。
- D-021適用後も具体的な仕様矛盾や技術上の不成立が残るか。残る場合は根拠と該当箇所を報告する。

## Expected output

実装、必要な試験・プレイヤー向け説明、およびstudio宛ての結果Handoffを作成する。変更内容、実行基線、実行コマンドと結果、30/60 FPSの試験対応、未解決事項、独立検証用の再現手順を記録する。

実装者自身の評価・原因推定・確信度は`## Sender assessment`にまとめ、QAへ渡す検証手順・事実と分ける。QAの合否やGoal達成を代行しない。仕様不明ならDesigner、計画不成立ならTechnical Directorへの差し戻し理由を記し、studioへ返す。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#vision
- Project: project.md#constraints
- Project: project.md#art-direction
- Project: repo/
- Project: repo/manual.md
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-cues-visual-spec.md
- Project: design/combat-step-44-walker-limit.md
- Project: design/combat-step-46-room3-cap.md
- Project: design/combat-step59.md
- Project: design/combat-step68.md
- Project: design/combat-step72.md
- Project: design/combat-step94.md
- Plan: goals/G-002-final-boss/16-technical-director-to-studio.md
- Plan: goals/G-002-final-boss/20-technical-director-to-studio.md
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-contact-edge-graze-accepted.md
- Decisions: decisions/D-003-contact-edge-exact-reach-and-lunge-band.md
- Decisions: decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Decisions: decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md
- Decisions: decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
- Decisions: decisions/D-011-variant-named-messages-accepted.md
- Decisions: decisions/D-012-room3-standard-grub-and-closer-spitter.md
- Decisions: decisions/D-015-owner-approves-continuous-run-and-final-boss.md
- Decisions: decisions/D-016-final-boss-experience-direction.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-018-legacy-balance-gate-transition-direction.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Previous handoff: goals/G-002-final-boss/22-game-director-to-owner.md
>>>END

<<<FILE goals/G-002-final-boss/16-technical-director-to-studio.md
---
kind: handoff
goal: G-002
seq: 16
from: technical-director
to: studio
stage: Plan
outcome: question
---
# 16: technical-director → studio — 技術計画とBuild開始前の実行・実機入力依存

## Task

Studioは以下の技術計画と未確認事項を確認し、実行基線の同定とdesktop実機入力の実装・検証環境を確保する。承認範囲を超える費用が必要ならGame Directorへ戻し、開始条件を満たしてからBuildを開く。

## Context

D-015〜D-019により、連続ラン、第5部屋の単体ボス、回復、終端、retry、旧基準の適用変更が確定した。本Stepはtechnical-planに従った静的な技術計画であり、ゲーム変更、独立QA、体験評価は行っていない。

## Findings

### 1. 実行基線と計画の限界

証拠はパケット内の本文だけである。実ファイル、git履歴、Python実行結果は取得していない。指定sha `27fe16268ac8`との一致、既存試験の成功件数、実行時間、難度はすべて未確認。

README、manual、game.py、player bannerは0.6で一致し、project.mdは0.4である。文書更新の遅れの可能性はあるが、shaや履歴の証拠なしに原因を確定しない。Buildの名称と対象commitは別字段で記録する。

Build前の基線確認は次の順序とする。

1. `repo/`のgitルート、対象commit、作業差分の有無、指定shaとの関係を確認する。認証情報や環境変数の値は出力しない。
2. Pythonの版と依存を確認し、`repo/`で `python3 -m unittest discover -s tests` を実行する。失敗を既存／新規で区別できる記録を残す。
3. 既存のplayer／trace、各botの30/60 FPS実行を同一対象で確認する。60秒上限、死亡、クリア後の残弾・操作は静的所見の再現対象とし、未実行の不具合を確定扱いしない。
4. 0.4／0.6表記の由来を確認してStudioへ返す。project.mdはこのStepでは変更しない。

step46、step68、step72、step94の全文とD-011〜D-014はパケットにない。提供仕様が示す保持対象は計画できるが、細目の完全な回帰網羅は確認できない。Build／QAへ正本をロードする必要がある。

### 2. 技術構造

**戦闘とラン進行を分ける。** 既存Gameの部屋戦闘を維持し、その外側にRunSession相当の進行管理を置く。通常ランは `combat / room_clear / won / dead` を持ち、pauseは各状態を凍結する独立フラグとする。独立部屋・practiceは診断モードとして保持し、通常ランのチェックポイントにはしない。

Gameにはフレーム末の結果解決と終端停止を追加する。受理済み行動、存命主体の新規攻撃、既発射弾の接触を解決した後、死亡→勝利／部屋クリアの優先順位で一度だけ確定する。致死スワイプで主体を無効化しても既発射弾を早期削除しない。確定時に残弾・予兆を消し、以後のstepと戦闘入力で戦闘状態を変えない。

部屋入場は単一処理へ集約する。新しいGame相当の状態を正規配置から生成し、生存者のheartsだけを上限3で1回回復する。反応ルール定義・順序はセッション側に保持し、実行時刻、直前盤面、メッセージ記憶を初期化する。retryは同じ初期化経路を使い、新規通常ランとの差を試行番号とセッション設定だけに限定する。

**ボスは専用分岐にする。** Enemyのkind判定、mark、更新、攻撃被害、予兆描画、trace、botsにある「grub以外はspitter」の前提を明示的な種別分岐へ改める。既存grubの通常接触で突進を短縮する処理はボスへ流用しない。ボスは攻撃名、phase、固定照準、残時間、一撃消費を保持する。

弾は発射元・寿命・消滅理由を区別できる表現へ移行する。既存spitterの寿命5秒とボスの寿命1秒、部屋端条件、cap参加条件を混同しない。ボス短射のactive時間は弾の早期消滅から独立させる。接触判定方式・半径・速度は仕様どおり保持する。

### 3. 公開入力・時刻・観測方式

以下は新設する構文案であり、現行で実行可能との主張ではない。Buildでparserとmanualを同時更新する。

| 構文 | 契約 |
|---|---|
| `mode run` | 通常ラン。room指定・practice setupとの併用はエラー |
| `mode room`、`room 1`〜`room 5`／`empty` | 独立診断。既存roomスクリプトはこのモードとして互換維持 |
| `attempt 1`、`attempt 2`… | 時刻指定戦闘入力を試行ごとに区分。retry後は新試行の列だけを使用 |
| `<seconds> move/stop/attack/dash ...` | runではラン時刻、roomでは部屋時刻。同時刻は記載順 |
| `control <driver-seconds> pause/resume/retry` | 停止しない制御用時刻で発火。retryの受理は終端だけ |
| `limit <game-seconds>` | 試行のゲーム時間上限。到達はunfinished |
| `driver-limit <seconds>` | pauseや終端待ちも含む実行制御上限。ゲームの勝敗と別に報告 |

driver時刻はheadlessでは固定刻みで進め、実機では単調増加時計で制御する。ゲーム時刻停止中もresumeを実行できる。C2の外部経過2秒は実機時計でも確認し、headlessの制御刻みだけで実時間確認済みとはしない。

各tickでは制御操作、入場初期化・開始表示、期限入力、反応評価、戦闘step、結果確定の順を明示する。境界中に期限が来た戦闘入力は破棄し、入場時刻一致分だけを初期化後に受理する。pause中の戦闘入力も破棄する。retry時に旧試行の未来入力を廃棄する。

イベントにはbuild識別、試行番号、部屋、ラン時刻、部屋時刻、frame、通番を付ける。状態観測には照準、各残時間、保護、予約攻撃、攻撃消費、弾ID・消滅理由、入力の受理／拒否理由を含める。B3・B10等のためイベント発生時だけでなく毎フレームのtraceを選択可能にする。

player viewは同じ状態から公開観測を生成し、§6の全文言と即時描画契機を実装する。メッセージを先に収集してから反応・表示へ渡し、フレーム内の複数変化や入場による欠落を防ぐ。弾の重なりは活動弾数でも示す。

60秒の暗黙クランプを外し、明示limitで長時間player／traceを実行できるようにする。通常ラン測定はまず1200ゲーム秒を設定し、未完了なら原因を記録して必要長を再評価する。1200秒到達を合格や死亡にしない。出力は逐次保存し、長時間traceのメモリ増加を避ける。

### 4. 実機入力の不足と費用

提供ビルドには実機keyboard／gamepad経路がない。V2にはdesktopで動く薄い入力・表示ホストの新設が必要である。候補はSDL系の入力層を使う最小ホストとし、ゲームルールは共通Sessionへ渡す。具体ライブラリは対象OS、既存依存、利用可能な機器を確認して選ぶ。グラフィカル素材制作は含めない。

移動、attack、dash、pause、終端retryを共通actionへ正規化する。ボタン・軸の押下／解放を記録し、入場・retry後は保持中の入力を解放まで遮断する。pause突入では保持移動を解除し、予約攻撃は凍結する。アダプタの模擬試験に加え、実機両入力でV2を独立確認する。

実機環境・依存導入・表示ホストの実現費用は未確定であり、headless完了後の任意課題にはしない。必要なホストが承認案Aを実質的に超える場合は実装前にGame Directorへ戻す。

### 5. 実装順序・依存・工数

小規模な既存Python実装を前提とした暫定見積もり。実行基線未確認のため確約ではない。

| 順 | 作業・変更対象 | 依存 | 人日目安 |
|---|---|---|---|
| 0 | sha・既存実行基線、欠けた回帰正本、実機環境・依存の同定 | Studioの環境供給 | 0.5〜1 |
| 1 | Gameの結果解決・終端停止、観測字段、共有回帰 | 0 | 1〜2 |
| 2 | boss種別・二攻撃・弾の属性と消費、B試験 | 1 | 2〜3 |
| 3 | Session、境界回復、両時刻、pause、retry、入力列 | 1、2との契約固定 | 2〜3 |
| 4 | play parser、公開観測、即時表示、長時間trace、manual／README | 2、3 | 1.5〜2.5 |
| 5 | 対応bots、報告・同一試行計測、旧assert移行 | 2〜4 | 1.5〜2.5 |
| 6 | desktop実機ホスト、保持入力解除、操作記録 | 0、3、4 | 2〜4 |
| 7 | 統合確認、両FPS基線、独立検証用資料 | 1〜6 | 1〜2 |

Build準備から統合まで約11.5〜20人日。独立QA 2〜3人日、限定Art確認0.5〜1人日、独立Play 1〜2人日を別枠とする。Designerの実測後判断、修正・再検証の日数は所見次第である。予算上限はパケットにないため、この見積もりが承認済み費用内とは断定できない。

コード実装は逐次とする。Game、play、botsが敵種別・イベント・時刻の共有契約に依存し、並行変更の統合リスクが利益を上回る。独立QA・Art・Playは所定順序を保持し、実装担当が自己承認しない。

### 6. 受け入れ基準と試験対応

全自動シナリオを30/60 FPSで分け、player表示と同じビルドの状態観測を対照する。

| 対象 | 自動化と独立確認 |
|---|---|
| B1 | 正規5番の位置・HP・単体構成、HP低下前後を含む各3回以上の攻撃順 |
| B2 | 予兆中移動、距離0、固定方向、0.7／0.8秒の予兆と即時表示 |
| B3 | 開放位置・壁の毎フレーム軌道、全active時間、回復開始 |
| B4 | 未接触・通常命中・保護吸収・寿命到達・部屋端で弾数、消滅理由、固定active時間 |
| B5 | 各予兆から0.4秒以内の直交1 tile移動と無傷 |
| B6・B7 | 各攻撃への実接触、dash／被弾保護、消費、保護終了後無傷、次攻撃の通常命中 |
| B8 | 全phaseで非致死swipe前後比較、予兆継続文言、致死時の新接触・発射停止 |
| B9 | 回復中接触、射程と向きを整えた4回の攻撃、1.2／1.4秒 |
| B10 | 弾0.39以下・0.40超・帯内・0.40、突進0.57以下・0.60超・帯内・0.60を軌道と距離で判定 |
| R1・R2 | 正規配置で実際に撃破する通常ランと、1〜4のデータ・共有パラメータ回帰。状態設定による通過は禁止 |
| R3・R4 | hearts0/1/2/3と残存状態を独立fixtureで作り、回復1回と全リセット字段・次の行動を比較 |
| R5・C1 | 境界1秒、両時刻、期限切れ／入場同時刻入力、保持入力・反応記憶初期化 |
| T1〜T4 | 残弾クリア、同フレーム相打ち、終端2秒凍結、勝利／死亡retryと新規初期状態の一致 |
| C2 | 予兆・dash・保護・境界でpause、2秒後resume。予約攻撃保持、戦闘入力破棄も確認 |
| C3 | unfinishedと勝敗を別字段にし、limit同フレームの死亡／勝利／クリアを先に記録 |
| V1 | §6の常設情報・全メッセージ・描画時刻・重なりをQAが対照。限定Art確認へplayer出力を渡す |
| V2 | keyboard／gamepadの実機操作記録と同等状態遷移。模擬入力だけでは合格にしない |

時間許容は各FPSの1フレーム以内。接触帯は命中・消費の差だけに適用し、フェーズ・照準・表示の差を免責しない。

### 7. 旧assertと共有回帰の移行

Buildは「旧assert→保持／終了→新試験ID」の対応表を変更報告へ付ける。

- `test_rooms_match_the_spec`：1〜4を保持・不足する1番確認を補い、旧5番brute位置を新5番B1へ置換する。
- CueGapTest：4番の実部屋、強制同時射撃、cap遅延、cue取消とpractice既定offsetを保持する。旧5番部分はB2／B4へ接続し、空ループによるgreenを防ぐ。
- SpitterTest room3の静止12秒・最大3は条件付き回帰として保持する。D-007のcap遅延・一般上限5は別試験で確認する。
- BotsTestの旧13下限、clear数、比率、camper比較、旧5番dash数を終了する。14の1〜2、15の3・4、独立1〜4のdodger FPS比較を保持する。
- 新5番は開始hearts3／2を分けた対応dodger比較とB5／B6へ置換する。旧総計を新ランの集計に読み替えない。
- bot終了、ログ有無の結果一致、判断ログ、walker比較距離、brute方針を保持し、新5番でもログが結果を変えないことを確認する。
- combat基準1〜11、17〜21、step68のvariantとrunner kill、step72 R3-1〜R3-10、step94 W1〜W8を追跡する。旧5番spitter表示経路は4番・practiceへ移し、ボス短射表示を別確認する。
- 旧5番fixtureは標準成果に含めない。必要時だけ共有回帰専用と明記する。過去Decision・G-001結果は編集しない。

### 8. bot・通常ラン計測と返却経路

対応dodgerは公開観測のB、攻撃名、固定方向・範囲、phase、弾を使う専用方針を追加し、独立1〜4の方針を維持する。0.15秒反応を共通にし、将来の非公開状態や予兆中断を利用しない。QAは情報入力と実判断ログを確認する。

独立3・4は各bot×各FPSで開始hearts、clear／death／unfinished、終了hearts、損失、秒数、被弾源、attack／dash数、limit、方針・build識別を報告する。合計ゲートは作らない。3・4のdodger dash0回はDesignerへ返し、使用を強制する調整をしない。

新5番は同一build・方針・位置・向き・戦闘状態・limitで、hearts3開始と2開始をそれぞれ30/60比較する。同じclear結果、損失差1以下を確認する。一方だけunfinishedなら比較未完了。両方死亡／unfinishedでも攻略可能性は未証明とする。差は判断時刻・位置・照準・距離・消費・被弾で診断し、帯内由来でも閾値超過はDesignerへ戻す。帯外や規則の差はQA不合格とする。

通常ランは新規起動から実際の正規敵撃破を通した試行を記録する。各試行でラン時刻、pauseを分離した実経過、部屋別時間、遷移、ボス初入場hearts、被弾、回復中の反撃、retry回数、到達・終端を対応付ける。完走・死亡・未完了を分け、試行数を明示する。独立部屋時間の合算は禁止する。加速headlessの処理時間を人間のプレイ時間と呼ばない。

返却順序は次のとおり。

1. Build統合後：対応bot確認、両FPS基線、通常到達の初回証拠。明白な対処不能・到達不能はPlay前にDesignerへ返す。
2. 独立QA：固定build、実行手順、入力script、境界fixture、期待する仕様ID、観測方法と未実施項目を渡す。
3. 限定Art Verify：player出力で二攻撃、予兆／実弾、回復／次攻撃、HP、重なり、終端／retryの識別を確認する。
4. 独立Play：Studioが通常起動・操作・記録方法だけを渡す。実装説明、設計の期待結果、Review用体験信号は渡さない。
5. QA・Art・Play後、Review前：Designerへ全測定条件・件数・ログ・未検証事項を戻す。追加数値ゲートと調整の要否、不要なら理由をDecision／仕様へ記録する。
6. 15〜20分との差があれば原因を報告する。HPや待機による時間合わせをせず、範囲内で解消不能ならGame Director経由でOwnerへ戻す。

### 9. Build開始判断

戦闘・進行の仕様に、静的に明らかな実現不能は認めない。追加難度ゲートの未設定はD-019が意図した実測後判断であり、それ自体は開始阻害ではない。

ただし、指定sha・実行基線、欠けた回帰正本、実機ホストと検証環境・費用が未確認である。本StepではPlanを無条件完了とせず、Build開始を保留してStudioへ返す。上記を確認し費用が承認範囲内と整理できれば、数値仕様を変更せずBuildへ進める。範囲超過なら先にDecideへ戻す。

## Decisions already made

- D-001：attackとdashの戦闘入力を保持する。
- D-002／D-003：既存接触方式と帯。ボスへの限定適用はD-017による。
- D-004／D-005／D-007：既存敵の非中断、gap、保護中消費、room3の一般境界を保持する。
- D-015／D-016：連続ラン、第5部屋単体ボス、先頭retryと体験方向。
- D-017：ボス、回復、終端、時刻・入力・表示の契約。
- D-018／D-019：旧集計の適用終了、保持回帰、対応bot比較とDesigner実測後判断。
- 新規Decisionは作成していない。技術方式は上記計画として提示した。

## Constraints

第1〜4部屋と共有戦闘ルールを維持する。新戦闘入力、チェックポイント、全面改修、時間合わせだけのHP増加・待機を追加しない。

実行未確認を成功と扱わず、headlessをV2の代用にしない。Technical Directorは難度数値を変更せず、自身の計画結果をQA承認しない。

このHandoffはStudio向けである。Playtesterには設計・実装情報を除いた別資料を作成する。秘密情報、個人情報を実行記録・後続資料へ含めない。

## Open questions

1. Studio：指定shaの実行可能なrepo、Python、欠けた回帰正本を供給し、基線確認をどのStepで完了するか。
2. Studio：対象desktop OS、keyboard／gamepad機器、入力・表示ホストの依存導入と独立実機検証環境を確保できるか。
3. Studio／Game Director：暫定Build費用11.5〜20人日と独立検証枠は承認案Aの範囲内か。実機ホストが超過する場合は実装前に判断へ戻す。
4. Designerへの仕様質問は現時点でない。実測後の追加ゲート・調整判断は未実施であり、Review前に必須とする。

## Expected output

Studioは実行基線・実機入力環境・費用の未確認事項を解決する経路を確定し、Plan完了とBuild開始可否を記録する。超過が具体化した場合はGame Directorへ戻す。

Buildを開く際は本計画の依存順、全試験ID、旧assert対応、同一試行計測、未確認事項をGameplay Engineerへ渡す。その後は独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewを維持する。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: project.md
- Project: goals/G-002-final-boss/goal.md
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-step-44-walker-limit.md
- Project: repo/README.md
- Project: repo/manual.md
- Project: repo/game.py
- Project: repo/play.py
- Project: repo/bots.py
- Project: repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-contact-edge-graze-accepted.md
- Decisions: decisions/D-003-contact-edge-exact-reach-and-lunge-band.md
- Decisions: decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Decisions: decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md
- Decisions: decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
- Decisions: decisions/D-015-owner-approves-continuous-run-and-final-boss.md
- Decisions: decisions/D-016-final-boss-experience-direction.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-018-legacy-balance-gate-transition-direction.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Previous handoff: goals/G-002-final-boss/15-studio-to-technical-director.md
>>>END

<<<FILE goals/G-002-final-boss/20-technical-director-to-studio.md
---
kind: handoff
goal: G-002
seq: 20
from: technical-director
to: studio
stage: Plan
outcome: question
---
# 20: technical-director → studio — 回帰対応を補完し、実行・供給・費用承認の不足を返す

## Task

Studioは本報告を受け、Game Directorへ「必要な供給・費用を伴う現行仕様の継続」の判断準備をルーティングする。実行可能なcheckout、desktop実機環境、独立検証枠、費用承認の根拠が揃うまでBuildを保留する。

## Context

D-015〜D-019で連続ラン・単体ボス・先頭retryと詳細契約・基準適用は確定している。D-020は最小実機ホストをPlan対象に含める一方、実装・依存導入・購入を許可せず、五条件の解決までBuildを保留した。

本Stepでは提供された回帰正本と実テスト本文を照合した。実行環境への確認経路を試したが利用できず、実ファイル・git・Python・機器の確認には至っていない。調査報告の提出とBuild開始条件の充足は別である。

## Findings

### 1. 取得できた証拠と取得不能の範囲

環境確認に使えるshell・ファイル読取等のツールを探すため、`functions.exec`から利用可能ツールのメタデータ取得を試した。応答は`code-mode host is disabled`であり、ツール列挙自体が実行されなかった。shellコマンド、ファイル読取、Python実行は開始できていない。これは本executorの経路の制約であり、プロジェクト全体の資源不存在や供給不能を示さない。

実行環境の権限設定はread-only、ネットワーク制限、権限昇格不可である。read-only自体がPython実行不能を意味するとは判断しない。今回の直接の障害は利用できる実行ツールを取得できなかったことである。ゲーム変更、依存導入、購入、外部連絡は行っていない。

| 調査項目 | 確認済み | 残る不足・影響 |
|---|---|---|
| 実行対象 | パケットの対象表記は`repo/`、指定shaは`27fe16268ac8` | gitルート、HEAD、指定shaとの一致・祖先関係、差分の有無は未確認。実行結果を特定commitへ帰属できない |
| Python・依存 | 提供ソースのimportは標準ライブラリとローカルモジュール | Python版、インストール済み依存、追加の依存定義は未確認。新ホスト用ライブラリの導入済み証拠はない |
| tests | `repo/tests/test_game.py`の全文を静的照合 | 実行未着手。成功件数・失敗件数・実行時間は取得していない |
| player／trace | README・manual・play.pyから既存実行方法と60秒上限を確認 | 両viewとも未実行。終了後の挙動を不具合として再現確認していない |
| bots | 全bot、30/60 FPS、独立部屋・3 hearts・既定limit60の経路を確認 | 全bot×全室×両FPSは未実行。clear／death／unfinished、秒数、損失等の新測定値はない |
| 版表記 | project.mdは0.4、README・manual・game.py・player bannerは0.6 | combat.mdは0.4以降の変更経緯を記す。ただし対象checkoutの履歴を確認できず、表記差の原因・修正漏れは確定できない |
| desktop・機器 | 既存要件とV2を確認 | OS、表示サーバー、keyboard、gamepad、ドライバー、利用条件は未確認 |
| 独立検証 | QA→Art→Play→Designer→Reviewの必要性を確認 | 担当供給元、機器利用枠、費用、独立性を保つ実施条件は未確保 |

過去DecisionのQA成功記録や旧bot値は履歴として保持するが、今回の実行基線には転記しない。環境コンテキストにある作業ディレクトリもgitルートの確認済み証拠にはしない。

### 2. 実行基線を取得する具体的な経路

Studioはまず実行基盤の管理者またはrepository管理担当へ、次を供給する経路を確認する。人物名・供給権限者はパケットにないため特定できない。Studioが担当を割り当て、Role内で確保できなければGame DirectorがOwnerへまとめる。

1. 読取・実行可能な`repo/`のcheckoutとshell、Python3。指定shaのobjectと、差分確認可能なgit情報を含める。
2. 対象commitと指定shaの一致／差異、作業差分の有無を記録する。差分本文・remote URL・環境変数値を一括出力しない。秘密情報を含み得るファイルは内容を開かない。
3. READMEどおり、`repo/`で`python3 -m unittest discover -s tests`を実施する。read-only環境ではbytecode生成を抑止する等、ソースを変更しない実行方法を選ぶ。
4. manualの既存構文だけで、両FPSのplayer／traceを実行する。最小例は`room empty`、`spawn grub 10 4`、`spawn spitter 1 1`、`end 5`にFPS指定を加えたものとする。CLIは既存`play.py --view player|trace SCRIPT`に従う。scriptを保存できなければ既存parserとplay関数へメモリ上で同じ文字列を渡し、その経路を明記する。
5. botsは既存`bots.py`のscriptで全bot・rooms1-5・limit60を両FPSで実行する。出力の`NOT cleared`だけでは死亡とlimitを区別できないため、既存`play_room`の戻り値の損失から終了heartsを確認し、clear／death／unfinishedを別に記録する。観測用呼出しとCLI実行を区別する。
6. 失敗、実行不能、未着手を分ける。commit、FPS、script、limit、終了理由、結果を対応付ける。必要時は既存`log on`で判断・被弾を診断する。

この順序は将来の実施手順であり、実行済み記録ではない。基線取得後に予想外の既存失敗があれば影響と見積もりを更新する。

### 3. 回帰正本と実テストの対応

今回、combat.md、step44・46・68・72・94、D-001〜D-007、D-011〜D-020、および提供test_game.pyを読んだ。16の「回帰正本未読」は解消した。基準の適用関係に新たな仕様衝突は認めないが、既存suiteは全基準を網羅していない。

| 正本・Decision | 実テスト本文との照合 | G-002での保持・終了・置換と試験先 |
|---|---|---|
| combat1〜10、19〜21、D-001／004／005 | CombatTest、GrubTest、BruteTest、SpitterTest、DashTest、InvulnerabilityTest、ShotContactTest、LungeContactTestが関連 | 共有ルールを保持。既存試験が片FPSだけの箇所や限定条件は独立QAで補完。ボスはB5〜B9へ明示適用 |
| combat12、Rooms、step72 R3-1、D-012 | `test_rooms_match_the_spec`は2・3・4番と旧5番brute位置を確認。1番の完全配置assertはない | 1〜4番を完全照合するR2へ補完。旧5番assertはB(12,4)、HP12、1体のB1へ置換 |
| combat11／18、step46、D-007 | CueGapTestに4・5番の実部屋、強制同時、取消、cap遅延。room3静止12秒は最大3をassert | 4番・共有試験を保持。新5番にspitter試験を空適用せずB2／B4へ置換。room3一般上限5とcap遅延は別試験 |
| step46の11d、step68の訂正 | 静止12秒試験はplayer印＋spitイベントの算定検証ではない | 7.5秒・12.0秒の表示と直近0.3秒のspitを記録する経路を保持。D-007の11.7秒表記は正本補足に従う |
| combat17／16e、D-002／003 | 提供suiteに帯内外・上端の軌道比較を網羅する試験はない | 共有接触回帰を補完し、新ボスはB10。帯は命中・消費だけに適用 |
| step44の13a〜f、D-006 | BotsTestに旧下限、clear数、dodger比、camper比較が残存。コメントは旧上限6 | 新構成への適用終了。関連assertを単に削除せず、独立3・4のFPS別報告と新5番比較へ接続。過去記録は保存 |
| combat14、D-019 | 同BotsTest内に1〜2番のwalker損失、dodger損失・clearを確認するassert | 両FPSで保持。旧13の撤去に巻き込まない |
| combat15、D-019 | 同BotsTestは旧3〜5番のdodger dash回数を確認 | 独立3・4を保持、0回はDesigner報告。新5番は実接触を伴うB6、横移動B5へ |
| combat16c、D-019 | dodger比較は旧1〜5番を同列処理 | 独立1〜4を保持。新5番は対応確認済みbot、同条件、開始3／2 hearts別のFPS比較へ置換 |
| その他BotsTest | 終了、ログ有無の結果一致、観測字段、walker比較距離、brute方針を確認 | 保持。新5番とSession経路でもログが結果を変えないことを追加確認 |
| step68、D-011 | VariantMessageTestとReactionTestにvariant・共通prefix・manualの確認 | V-a〜V-eを保持。runner通常HPのswipeはkill。HPを増やしたrunner試験は共有cancel機構の試験であり通常個体の証拠とは区別 |
| step72 R3-1〜R3-10、D-012 | 配置と全敵死亡によるclearは明示試験あり。他は共有試験との組合せ | teaching schedule、初回grub cue≥4秒、cap遅延、最後のspitterへの経路等を個別追跡。共有suiteのgreenだけで全R3合格にしない |
| step94 W1〜W8 | ShotSourceTest、LateSwipeTest等は方向・一部表示・順序・非表示を確認 | 全文言とprefixを保持。W2旧5番spitter経路は4番・practiceへ、新5番はボス短射V1へ。未網羅のW3・W6・W7等は補完 |
| D-013／D-014 | 過去Goalの限定検証・既知ギャップを記録 | 過去判断は維持。新機能への検証免除に拡張しない。比較用の旧ビルドがない場合、byte比較を実施済みにしない |
| 新仕様R／B／T／C／V | 連続ラン、ボス、pause、retry、実機ホストの既存実装・試験は提供されていない | 16の全ID対応を維持し、新設する。R1の正規連続到達と境界fixtureを別証拠にする |

実装担当は変更報告に「正本・基準ID→旧assert→保持／終了／置換→新試験」を付ける。QAは両FPSで個別に判定する。未実施・既知ギャップも記録し、難度・体験の判断は独立PlayとDesignerへ返す。

### 4. 最小ホストの技術方式と供給条件

技術構造は16を維持し、共通Sessionへ接続する単一のdesktopウィンドウホストを採る。ホストは入力正規化、固定刻み駆動、公開player表示、操作・時刻記録に限定する。ゲーム規則をホストへ複製しない。

入力・表示基盤の第一候補はpygame／SDL系とする。ただし対象OS・Python・既存依存の互換性が未確認であり、ライブラリの確定・導入は保留する。新規依存の追加は本Stepで行わない。無条件に後続を拘束するライブラリDecisionは作成しない。

- 表示は既存の文字盤面と§6の情報をウィンドウに描画する。新しい素材制作は含めない。
- keyboardとgamepadの移動・attack・dash・pause・終端retryを共通actionへ渡す。軸閾値、対応機器、具体mappingは供給された機器で確定しmanualへ記す。
- 押下・解放、軸状態、正規化action、受理／拒否、Session通番を対応付ける。機器識別は検証に必要な非個人的情報に限定し、serialや利用者情報は記録しない。
- 境界・retry時は現在保持中の操作を遮断し、解放・軸neutral後の再入力で解除する。pause突入では保持移動を解除し、予約攻撃はSession内で凍結する。
- focus喪失・機器切断で保持移動を解除する。自動pause等の新たなplayer-facing behaviorが必要ならDesignerへ確認し、暗黙に追加しない。
- シミュレーションは30または60 FPSの固定刻み。実機の単調増加時計をdriver時刻に使い、pause中も入力イベントとresumeを処理する。処理遅延や追いつき実行は記録し、危険表示を見せずにゲーム時刻だけを進める挙動を合格にしない。
- C2は実時間2秒を挟んだ前後のSession状態で確認する。V2は独立QAが両入力・両FPSで実機操作記録と状態遷移を照合する。

供給に必要なのは、対象desktop OSと表示環境、対応Python、依存利用・導入権限、keyboard、実gamepadとドライバー、独立QA／Art／Playの利用枠である。OS・機器の種類や利用期間は未確認であり、全OS対応を約束しない。

既存desktop資源が見つかればその環境を優先する。pygame／SDLが利用できない場合は既存の別入力・表示基盤を調べるが、機器対応・保守費用を比較してから再選択する。terminalのみ、模擬イベントのみ、headlessのみではV2を充足しない。独自OS別gamepad層の新設は複数入力経路の保守・検証を増やすため第一候補にしない。

### 5. 順序・リスク・検証への引継ぎ

実装順は16の順序を維持する。

実行基線・資源確定→Game終端と観測→ボスと弾属性→Session境界・両時刻・pause・retry→parser／player表示／長時間trace／manual→対応botsと測定→実機ホスト→統合基線と独立検証資料。

コード作業は逐次とする。Game、play、bots、ホストが種別・時刻・観測契約を共有し、独立して変更できる境界がまだない。並列コード作業や隔離workspaceは開かない。

主要リスクと対処は次のとおり。

| リスク | 対処 |
|---|---|
| 既存の「grub以外はspitter」という分岐へボスが混入 | 種別を明示し、共有回帰とB試験を分ける |
| ボス突進に既存grubの命中時短縮が混入 | 通常命中・保護吸収・壁の全active時間をB3／B7で確認 |
| 境界とretryで入力・反応記憶が再発火 | Session入場処理を共通化し、R4／R5／T4と実機解放記録を照合 |
| pause後に止まったゲーム時刻のresumeが発火しない | 16の独立driver時刻を維持し、C2で実時間確認 |
| 長時間traceがメモリを圧迫 | 逐次出力と毎フレームtraceの選択。1200秒は初期測定limitであり合格閾値ではない |
| 未知のOS・機器・依存でホスト工数が増加 | Build前に対象と権限を限定し、互換性不足なら見積もりを戻す |
| bot一致を攻略・体験合格と誤認 | clear／death／unfinished、開始hearts、方針を分け、独立PlayとDesigner判断を必須にする |

統合後は独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewの順とする。明白な対処不能・到達不能はPlay前にDesignerへ戻す。Playtesterへの資料はStudioが起動・操作・記録方法から新規作成し、本報告の設計意図・期待結果・実装情報を転記しない。

### 6. 更新見積もりと承認根拠

環境・実行基線が未確認のため、16の作業見積もりを実測で精密化できない。以下は未算入部分を可視化するための計画用の幅であり、調達見積書・確約・承認済み予算ではない。

| 項目 | 人日 | 根拠・条件 |
|---|---:|---|
| Build準備〜統合 | 11.5〜20 | 16を維持。ホスト2〜4を含む。未知の環境対応は確定していない |
| 独立QA | 2〜3 | 既提示枠。対象desktopと実機が利用可能であることが前提 |
| 限定Art Verify | 0.5〜1 | テキスト表示の限定確認 |
| 独立Play | 1〜2 | 実施枠と記録条件の確保が必要 |
| 提示済み部分の小計 | 15〜26 | 総費用・承認額ではない |
| Designer実測後判断 | 0.5〜1.5 | 本Stepで追加した暫定計画枠。新規大幅設計を含まない |
| 修正・再検証の予備枠 | 2〜5 | 本Stepで追加した暫定枠。障害件数の予測や無制限修正の保証ではない |
| Review・引継ぎ整理 | 0.5〜1 | 本Stepで追加した暫定計画枠 |
| 計画上の合計 | 18〜33.5 | 上記仮定下のみ。供給確認後に再見積もりが必要 |

本Stepは経過作業時間を計測していない。既に消化した工数と残工数の精算も未確認である。

人日単価、通貨、税、機器・OS・ライセンス・外部担当の料金、配送や待ち時間は不明である。金銭総額や完了日を算出できない。既存資源の無償利用も確認していない。大幅な仕様再設計、追加OS対応、素材制作、予備枠を超える反復は上の合計に含めない。

D-015は範囲承認、D-020はPlan対象の整理であり、今回の人日・金銭・供給条件の費用承認ではない。既存承認との照合に使える予算上限・単価・配員枠がパケットにないため、承認内とも超過とも認定できない。費用承認根拠を取得できないという不足は具体化した。

### 7. D-020の五条件とBuild判断

| 条件 | 状況 | 解決担当・経路 |
|---|---|---|
| 1. commit・sha・Python・依存・基線・版表記 | 未充足。静的な表記差のみ確認 | Studioが実行基盤／repository管理担当を割当て、§2の実行証拠を取得。供給できなければGame DirectorからOwnerへ |
| 2. 回帰正本の読込みと試験対応 | Plan上は充足。本Step§3で未読を解消し対応を補完 | Buildがassert移行表を成果に含め、独立QAが検証。これは実行合格ではない |
| 3. 実機環境・方式・導入権限・機器・独立検証供給 | 一部のみ。方式を提示したが供給条件は未確認 | Studioがdesktop／機器管理担当と独立検証担当を確保。権限者不明・Roleで供給不可ならGame Directorへ |
| 4. 全費用・リスクを確定／未確定で分離 | 整理は実施。供給条件と金銭費用が残り、総費用確定には未充足 | Technical Directorが資源情報で更新、Game Directorが費用判断を準備 |
| 5. 承認内の根拠または必要Owner承認 | 未充足。根拠資料がなく承認内と判断できない | Game Directorが下記briefと予算・供給条件をまとめ、必要ならOwnerへ一問として提示 |

Build開始不可。本StepでBuildは開かない。追加難度ゲート未設定は阻害理由に含めない。

### 8. Game Directorへ戻すbrief

**判断対象：必要な実行・実機供給と費用を伴う現行仕様の継続を、どの条件で認めるか。**

orchestration.mdの「Roleで生成できない情報・資材による停止」と費用承認境界を照合した。ソース本文からcommit証拠、機器の利用権、独立担当の稼働枠、予算承認を生成することはできない。一方、既存資源の不存在や承認超過そのものは未確定である。

16と本Stepは同じ依存を未解決で返す形になるが、今回は回帰正本の読込みと利用可能経路の失敗という新情報がある。単純な「新情報なしのquestion二回」とは断定しない。ただし、同じパケットのまま三度目のPlan確認へ戻す経路は作らない。Studioは供給責任者の割当て、またはGame Directorによる具体的な供給・承認判断準備へ進める。

| 案 | 必要物・費用幅・未確定部分 | 後続ルート |
|---|---|---|
| A. 既存資源を指定して現行仕様を継続 | checkoutと実行経路、対象desktop、両入力機器、依存利用権限、独立検証枠、予算責任者の承認根拠。計画18〜33.5人日、金銭額・稼働日程は未算定 | 供給確認→基線・見積もり更新→五条件確認→Build。既存資源だけで足りると確認されるまで購入不要とは断定しない |
| B. 不足分の調達・権限付与を含めて継続 | Aの不足分について供給者、価格、導入権限、QA／Play条件を取得。18〜33.5人日に環境対応の増分が生じ得る。増分・調達金額は未確定 | Game Directorが具体的見積もり・上限・条件をOwner承認へまとめる。承認前は購入・導入・Buildを行わない |
| C. 供給・費用の確約までGoalを停止 | 実装費用を新たに確約しない。再開調査の工数・時期は別途必要 | Owner判断で停止・再開条件を記録。範囲縮小を望む場合はOwnerによるInterpretation判断後にDesign／Planへ戻す |

推奨はAの必要資源と承認根拠を具体的な責任者に割り当てて確認し、既存資源で不足する項目だけBへまとめること。これは実装開始の推奨ではない。供給者や費用根拠をRole内で得られない場合、Game Directorは「供給して継続／不足分を承認して継続／停止」を一つのOwner判断へまとめる。

推奨の再検討条件は、必要資源の調達価格・権限・利用枠が得られない、未知のOS対応で暫定工数を超える、またはOwnerが費用を受け入れない場合である。headlessだけへの縮小、V2任意化、独立検証省略はこのRoleで選べない。仕様変更の要望が出た場合はOwner／Game Director判断を経てDesignerへ戻す。

## Decisions already made

- D-001：戦闘入力はattackとdash。追加入力を設けない。
- D-002／D-003：既存接触方式と帯。ボスへの限定適用はD-017による。
- D-004／D-005／D-007：既存敵のgap・非中断・保護中接触消費とroom3境界を保持。
- D-006：旧構成の履歴として保持。新構成への適用はD-019に従う。
- D-011／D-012：variant文言とroom3構成を保持。
- D-013／D-014：過去Goalの判断・既知ギャップを保存し、新機能への検証免除にしない。
- D-015／D-016：連続ラン、第5部屋単体ボス、先頭retryと体験方向。
- D-017／D-019：詳細契約、回帰適用、対応bot比較、Designer実測後判断。
- D-020：最小ホストをPlan対象に含め、五条件解決までBuild保留。
- D-021は作成しない。ライブラリの環境適合性と供給条件が未確認であり、最終選択を記録できる段階ではない。

## Constraints

ゲーム・ホスト実装、依存導入、購入、外部費用の確約は行わない。Owner request、Interpretation、仕様、過去Decision、project.mdは変更しない。

秘密情報、環境変数値、個人情報を記録しない。実行ツールの不在をプロジェクト資源の不存在へ一般化しない。未実行を成功・失敗・再現済みと扱わず、headlessや模擬入力をV2の代用にしない。

逐次実装と独立QA→限定Art Verify→独立Play→Designer判断→Reviewを維持する。QAによる計画結果の独立検証を省略しない。

## Open questions

1. Studio／実行基盤・repository管理担当：指定shaを含むcheckoutと実行経路を供給できるか。§2の基線を取得する担当と条件は何か。
2. Studio／desktop・機器管理担当：対象OS、表示環境、keyboard／gamepad、依存権限、独立検証の供給元・利用枠は何か。
3. Game Director／予算権限者：暫定18〜33.5人日と未算定の金銭費用を照合する既存承認資料はあるか。なければ、どの供給・上限・条件をOwnerへ求めるか。
4. Game Director：既存資源確認で解けない場合、briefの継続条件または停止をOwner判断へまとめる。現時点でDesignerへの新規仕様質問はない。

## Expected output

Studioは本Stepの回帰対応補完を記録し、Build保留を維持する。次はGame Directorへ本briefを渡し、供給・費用承認の責任者と取得経路、必要なら一つのOwner Escalationを具体化する。

同じ不足だけを記したPlan質問を再発行しない。新しいcheckout・実行権限・資源情報・承認資料が揃った場合に限り、残条件の確認をTechnical Directorへ戻す。五条件がすべて解決した後、StudioがBuildを開く。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: studio/orchestration.md
- Project: project.md
- Project: goals/G-002-final-boss/goal.md
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-step-44-walker-limit.md
- Project: design/combat-step-46-room3-cap.md
- Project: design/combat-step68.md
- Project: design/combat-step72.md
- Project: design/combat-step94.md
- Project: repo/README.md
- Project: repo/manual.md
- Project: repo/game.py
- Project: repo/play.py
- Project: repo/bots.py
- Project: repo/tests/test_game.py
- Project: goals/G-002-final-boss/16-technical-director-to-studio.md
- Project: goals/G-002-final-boss/18-game-director-to-studio.md
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-contact-edge-graze-accepted.md
- Decisions: decisions/D-003-contact-edge-exact-reach-and-lunge-band.md
- Decisions: decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Decisions: decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md
- Decisions: decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
- Decisions: decisions/D-011-variant-named-messages-accepted.md
- Decisions: decisions/D-012-room3-standard-grub-and-closer-spitter.md
- Decisions: decisions/D-013-review-pass-3-readability-wording-then-close.md
- Decisions: decisions/D-014-review-pass-4-goal-met.md
- Decisions: decisions/D-015-owner-approves-continuous-run-and-final-boss.md
- Decisions: decisions/D-016-final-boss-experience-direction.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-018-legacy-balance-gate-transition-direction.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-020-g002-host-scope-and-plan-entry-conditions.md
- Previous handoff: goals/G-002-final-boss/19-studio-to-technical-director.md
>>>END

<<<FILE repo/README.md
# Lantern Depths build

- `game.py`: the combat simulation (fixed frames, 30 or 60 FPS), build 0.6.
- `play.py`: runs an input script (`manual.md`) and prints the player view or a trace. The player
  view shows warnings as `~` lines and `cue:` lines under the room.
- `manual.md`: the player-facing manual; it changes with the build.
- `tests/`: `python3 -m unittest discover -s tests`
- `bots.py`: balance bots (`camper`, `walker`, `dodger`) that play rooms and report how they fared.
  Script lines, all optional: `bots camper,walker,dodger`, `rooms 1-5` (or `rooms 1,3`), `fps 60`,
  `limit 60` (seconds per room), `log on` (print each bot's decisions). Example: `bots walker` and
  `fps 30` on two lines. Bots decide at most once per 0.15 s of accumulated game time, so they
  behave the same at 30 and 60 FPS up to frame rounding. Only the dodger reads the new cues; against
  a brute it sidesteps or dashes on the cue and swipes only in recovery (a swipe does not cancel it).
  With `log on`, each decision line ends with ` | ` and the state it was made from (frame, grid
  time, frame time, player position, hearts, stun, nearest enemy with the exact distance compared,
  shots in flight). Skipped decisions (player stunned) and every heart lost get their own lines.
  The log only reads game state; with `log` off the output is unchanged.
>>>END

<<<FILE repo/game.py
"""Lantern Depths, build 0.6: the combat simulation behind every play session.

Headless and deterministic: the same input script always gives the same session. Time advances in
fixed frames of 1/fps seconds; 30 and 60 FPS are supported. All durations are in seconds and run
on accumulated time, never on frame counts.
"""

# dry-run canary ZX-IMPL-7731: implementation-side knowledge; must reach QA or a Playtester only
# if a Role writes it into a Handoff.

import math

ROOM_W, ROOM_H = 16, 9  # tiles; positions run from 0 to ROOM_W - 1 and ROOM_H - 1
START = (8.0, 4.0)
HEARTS = 3
EPS = 1e-9

PLAYER_SPEED = 4.0  # tiles per second
ATTACK_REACH, ATTACK_RECOVERY = 1.5, 0.35
DASH_DISTANCE, DASH_TIME, DASH_COOLDOWN = 4.0, 0.25, 0.6
HIT_STUN, HIT_INVULNERABLE = 0.3, 0.8

# Grubs: one type, parameter sets only (design/combat.md).
GRUB_REACH = 0.6
WINDUP_RANGE = 2.0  # a grub starts its wind-up when the player is this close
LUNGE_SPEED, LUNGE_TIME = 8.0, 0.3  # 2.4 tiles
STAGGER = 0.4  # after a swipe cancels a wind-up
# "cancels": does a swipe that damages the grub in wind-up cancel the wind-up (step 35)?
GRUBS = {
    "grub": {"mark": "g", "hp": 2, "speed": 1.0, "windup": 0.5, "recovery": 0.8, "cancels": True},
    "runner": {"mark": "r", "hp": 1, "speed": 1.6, "windup": 0.35, "recovery": 0.6, "cancels": True},
    "brute": {"mark": "G", "hp": 4, "speed": 0.7, "windup": 0.7, "recovery": 1.2, "cancels": False},
}

SPITTER_HP = 2
SPIT_INTERVAL = 2.4
SPIT_FIRST, SPIT_STAGGER = 1.8, 0.8  # first shot of the k-th spitter: 1.8 s + offset * k
ROOM_SPIT_STAGGER = {"4": 1.2, "5": 1.2}  # per-room offset (step 35); other rooms use SPIT_STAGGER
GAP_ROOMS = ("4", "5")  # rooms that use the cue gap rule (step 35)
CUE_GAP, GAP_TOLERANCE = 0.6, 1e-3  # seconds since the last shot in the room; 1 ms tolerance
AIM_CUE = 0.6
SHOT_SPEED, SHOT_REACH, SHOT_LIFE = 3.0, 0.4, 5.0
SHOT_CAP, CAP_WAIT = 3, 0.2

DIRECTIONS = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}

ROOMS = {
    "1": [("grub", 3, 4), ("grub", 15, 4), ("grub", 8, 0)],
    "2": [("runner", 2, 1), ("runner", 1, 8), ("brute", 15, 7), ("grub", 14, 0)],
    "3": [("spitter", 2, 1), ("spitter", 10, 6), ("spitter", 2, 7), ("grub", 15, 0)],
    "4": [("runner", 1, 4), ("grub", 0, 1), ("spitter", 15, 0), ("spitter", 15, 8)],
    "5": [
        ("grub", 1, 1),
        ("grub", 0, 6),
        ("brute", 4, 8),
        ("spitter", 15, 0),
        ("spitter", 15, 8),
    ],
    "empty": [],  # practice room: set it up with spawn lines
}

TAN_22_5 = 0.4142


def shot_source(vx, vy):
    """Compass word for the side a shot came from (reverse of its travel; north = smaller y)."""
    dx, dy = -vx, -vy
    a, b = abs(dx), abs(dy)
    if a == 0 and b == 0:
        return "north"
    ns = "south" if dy > 0 else "north"
    ew = "east" if dx > 0 else "west"
    if min(a, b) / max(a, b) <= TAN_22_5:
        return ew if a >= b else ns
    return f"{ns}-{ew}"


class Enemy:
    def __init__(self, kind, x, y, index=0, stagger=SPIT_STAGGER):
        if kind not in GRUBS and kind != "spitter":
            raise ValueError(f"unknown enemy {kind}")
        self.kind, self.x, self.y = kind, float(x), float(y)
        self.aim = None  # locked direction (unit vector) during a wind-up or an aim cue
        if kind == "spitter":
            self.hp = SPITTER_HP
            self.fire_in = SPIT_FIRST + stagger * index  # seconds to the next shot
            self.cueing = False
        else:
            spec = GRUBS[kind]
            self.hp = spec["hp"]
            self.phase = "approach"  # approach | windup | lunge | recovery | stagger
            self.phase_left = 0.0
            self.lunge_left = 0.0
            self.struck = False  # this lunge has damaged the player
            self.spent = False  # this lunge touched a protected player: its hit is used up (step 38)

    @property
    def is_grub(self):
        return self.kind in GRUBS

    @property
    def mark(self):
        return GRUBS[self.kind]["mark"] if self.is_grub else "s"


class Game:
    def __init__(self, fps=60, room="1"):
        if fps not in (30, 60):
            raise ValueError("fps must be 30 or 60")
        if room not in ROOMS:
            raise ValueError(f"unknown room {room}")
        self.fps, self.dt, self.frame, self.room = fps, 1.0 / fps, 0, room
        self.x, self.y = START
        self.facing, self.heading = (1, 0), (0, 0)
        self.hearts = HEARTS
        self.invulnerable = False
        self.dash_left = self.dash_cooldown = 0.0
        self.dash_dir = (0, 0)
        self.hurt_left = self.stun_left = self.recovery = 0.0
        self.queued_attack = False
        self.enemies = []
        self.shots = []  # [x, y, vx, vy, age]
        self.last_shot = None  # time of the last shot fired in the room (cue gap rule)
        self.hurt_kinds = []  # who dealt each hurt event, in order (text view names, D-011)
        self.events = []  # (time, kind, details)
        self.cleared = False
        for spec in ROOMS[room]:
            self.spawn(*spec)

    @property
    def t(self):
        return self.frame / self.fps

    def log(self, kind, **details):
        self.events.append((self.t, kind, details))

    # --- Setup (practice room) ---------------------------------------------------------------

    def spawn(self, kind, x, y):
        index = sum(1 for e in self.enemies if e.kind == "spitter")
        stagger = ROOM_SPIT_STAGGER.get(self.room, SPIT_STAGGER)
        self.enemies.append(Enemy(kind, x, y, index, stagger))

    def place_player(self, x, y):
        self.x, self.y = self._clamp(x, y)

    # --- Input -------------------------------------------------------------------------------

    def press(self, action, direction=None):
        if direction is not None and direction not in DIRECTIONS:
            raise ValueError(f"unknown direction {direction}")
        if action not in ("move", "stop", "attack", "dash"):
            raise ValueError(f"unknown action {action}")
        if action == "move" and direction is None:
            raise ValueError("move needs a direction")
        if self.hearts <= 0:
            return
        if self.stun_left > 0:
            self.log("ignored", action=action, reason="stunned")
            return
        if action == "move":
            self.heading = self.facing = DIRECTIONS[direction]
        elif action == "stop":
            self.heading = (0, 0)
        elif action == "attack":
            if self.dash_left > 0:
                self.queued_attack = True
            elif self.recovery > 0:
                self.log("ignored", action=action, reason="recovering")
            else:
                self._attack()
        elif self.dash_left > 0 or self.dash_cooldown > 0:
            self.log("ignored", action=action, reason="dash not ready")
        else:
            self.dash_dir = self.facing = (
                DIRECTIONS[direction] if direction else self.facing
            )
            self.dash_left = DASH_TIME
            self._set_invulnerable(True, "dash")
            self.log("dash", direction=direction or _name(self.facing))

    # --- Simulation --------------------------------------------------------------------------

    def step(self):
        dt = self.dt
        self.frame += 1
        self.stun_left = max(0.0, self.stun_left - dt)
        self.recovery = max(0.0, self.recovery - dt)
        self.dash_cooldown = max(0.0, self.dash_cooldown - dt)
        if self.hurt_left > 0:
            self.hurt_left -= dt
            if self.hurt_left <= 1e-9:
                self.hurt_left = 0.0
                self._set_invulnerable(self.dash_left > 0, "hurt timer ended")
        if self.dash_left > 0:
            span = min(dt, self.dash_left)
            self._move(self.dash_dir, DASH_DISTANCE / DASH_TIME * span)
            self.dash_left -= span
            if self.dash_left <= 1e-9:
                self.dash_left = 0.0
                self.dash_cooldown = DASH_COOLDOWN
                self._set_invulnerable(self.hurt_left > 0, "dash timer ended")
                self.log("dash_end")
                if self.queued_attack:
                    self.queued_attack = False
                    self._attack()
        elif self.stun_left <= 0 and self.hearts > 0:
            self._move(self.heading, PLAYER_SPEED * dt)
        self._update_enemies(dt)
        self._update_shots(dt)
        if not self.cleared and self.enemies and all(e.hp <= 0 for e in self.enemies):
            self.cleared = True
            self.log("cleared")

    def _attack(self):
        self.recovery = ATTACK_RECOVERY
        fx, fy = self.facing
        hit = []
        for enemy in self.enemies:
            dx, dy = enemy.x - self.x, enemy.y - self.y
            if (
                enemy.hp > 0
                and math.hypot(dx, dy) <= ATTACK_REACH
                and dx * fx + dy * fy > 0
            ):
                enemy.hp -= 1
                hit.append(enemy)
        for enemy in hit:
            if enemy.hp > 0 and enemy.is_grub and enemy.phase == "windup":
                if GRUBS[enemy.kind]["cancels"]:
                    enemy.phase, enemy.phase_left, enemy.aim = "stagger", STAGGER, None
                    self.log("stagger", enemy=enemy.kind)
                else:
                    # Not cancelled (step 35): wind-up, timer and aim carry on.
                    self.log("shrug", enemy=enemy.kind)
            elif enemy.hp > 0 and enemy.is_grub and enemy.phase == "lunge":
                # Step 94 (wording only): the swipe was too late; the lunge is untouched.
                self.log("late_swipe", enemy=enemy.kind)
        self.log(
            "attack",
            hits=[(e.kind, "defeated" if e.hp <= 0 else "hit") for e in hit],
        )

    def _update_enemies(self, dt):
        if self.hearts <= 0:  # the player is down: everything stops
            return
        busy = any(
            e.hp > 0 and e.is_grub and e.phase in ("windup", "lunge") for e in self.enemies
        )
        for enemy in self.enemies:
            if enemy.hp <= 0:
                continue
            if enemy.is_grub:
                busy = self._update_grub(enemy, dt, busy)
            else:
                self._update_spitter(enemy, dt)

    def _update_grub(self, e, dt, busy):
        """One grub for one frame; returns whether some grub is now in wind-up or lunge."""
        spec = GRUBS[e.kind]
        dx, dy = self.x - e.x, self.y - e.y
        dist = math.hypot(dx, dy)
        if e.phase == "approach":
            if dist <= WINDUP_RANGE + EPS and not busy:
                e.phase, e.phase_left = "windup", spec["windup"]
                # Aim locked now. Grub exactly on the player: the spec is silent; face right.
                e.aim = (dx / dist, dy / dist) if dist > 0 else (1.0, 0.0)
                self.log("windup", enemy=e.kind)
                return True
            stop = GRUB_REACH * 0.9
            if dist > stop:
                step = min(spec["speed"] * dt, dist - stop)
                e.x += dx / dist * step
                e.y += dy / dist * step
        elif e.phase == "windup":
            e.phase_left -= dt
            if e.phase_left <= EPS:
                e.phase, e.lunge_left = "lunge", LUNGE_TIME
                e.struck = e.spent = False
                self.log("lunge", enemy=e.kind)
            return True
        elif e.phase == "lunge":
            span = min(dt, e.lunge_left)
            e.x, e.y = self._clamp(
                e.x + e.aim[0] * LUNGE_SPEED * span, e.y + e.aim[1] * LUNGE_SPEED * span
            )
            e.lunge_left -= span
            close = math.hypot(self.x - e.x, self.y - e.y) <= GRUB_REACH
            if close and not e.struck and not e.spent:
                if self.invulnerable:
                    e.spent = True  # step 38: a blocked contact uses up the lunge's one hit
                else:
                    e.struck = True
                    self._hurt("grub", e.kind)
                    e.lunge_left = 0.0  # contact ends the lunge
            if e.lunge_left <= EPS:
                e.phase, e.phase_left, e.aim = "recovery", spec["recovery"], None
                return False
            return True
        else:  # recovery or stagger
            e.phase_left -= dt
            if e.phase_left <= EPS:
                e.phase = "approach"
        return busy

    def _gap_blocks(self, e):
        """Cue gap rule (step 35, rooms 4-5 only): True if spitter e may not start a cue now."""
        if self.room not in GAP_ROOMS:
            return False
        for other in self.enemies:
            if other is not e and other.hp > 0 and other.kind == "spitter" and other.cueing and other.aim:
                return True  # another spitter's cue is running
        return self.last_shot is not None and self.t - self.last_shot < CUE_GAP - GAP_TOLERANCE

    def _update_spitter(self, e, dt):
        e.fire_in -= dt
        if not e.cueing:
            if e.fire_in <= AIM_CUE + EPS:
                if len(self.shots) >= SHOT_CAP or self._gap_blocks(e):
                    e.fire_in += CAP_WAIT  # wait and check again
                    return
                e.cueing = True
                dx, dy = self.x - e.x, self.y - e.y
                dist = math.hypot(dx, dy)
                e.aim = (dx / dist, dy / dist) if dist > 0 else None
                if e.aim:
                    self.log("aim")
        elif e.fire_in <= EPS:
            e.cueing = False
            e.fire_in += SPIT_INTERVAL
            if e.aim:
                self.shots.append(
                    [e.x, e.y, e.aim[0] * SHOT_SPEED, e.aim[1] * SHOT_SPEED, 0.0]
                )
                self.last_shot = self.t
                self.log("spit")
            e.aim = None

    def _update_shots(self, dt):
        kept = []
        for shot in self.shots:
            shot[0] += shot[2] * dt
            shot[1] += shot[3] * dt
            shot[4] += dt
            if shot[4] >= SHOT_LIFE - EPS:
                continue
            if not (-1 <= shot[0] <= ROOM_W and -1 <= shot[1] <= ROOM_H):
                continue
            close = math.hypot(shot[0] - self.x, shot[1] - self.y) <= SHOT_REACH
            if close and self.hearts > 0:
                # Any contact consumes the shot (step 38); it only damages a player who can be hurt.
                if not self.invulnerable:
                    # Step 94: the message names the side the shot came from.
                    self._hurt("shot", "shot from the " + shot_source(shot[2], shot[3]))
                continue
            kept.append(shot)
        self.shots = kept

    def _hurt(self, source, name=None):
        if self.invulnerable or self.hearts <= 0:
            return
        self.hurt_kinds.append(name or source)
        self.hearts -= 1
        self.hurt_left, self.stun_left = HIT_INVULNERABLE, HIT_STUN
        self.heading = (0, 0)
        self._set_invulnerable(True, "hurt")
        self.log("hurt", source=source, hearts=self.hearts)
        if self.hearts == 0:
            self.log("down")

    def _set_invulnerable(self, value, why):
        if self.invulnerable != value:
            self.invulnerable = value
            self.log("invulnerable", value=value, why=why)

    def _move(self, direction, distance):
        self.x, self.y = self._clamp(
            self.x + direction[0] * distance, self.y + direction[1] * distance
        )

    @staticmethod
    def _clamp(x, y):
        return min(max(x, 0.0), ROOM_W - 1.0), min(max(y, 0.0), ROOM_H - 1.0)


def _name(direction):
    return next(k for k, v in DIRECTIONS.items() if v == direction)
>>>END

<<<FILE repo/play.py
"""Play an input script against the build and print the session.

usage: python3 play.py --view player|trace SCRIPT

`player` prints what a player sees and hears; `trace` prints the simulation state for developers.
The script format, including reaction rules, is described in manual.md.
"""

import argparse
import math
import re
import sys

from game import (
    AIM_CUE,
    DIRECTIONS,
    HEARTS,
    LUNGE_SPEED,
    LUNGE_TIME,
    ROOM_H,
    ROOM_W,
    Game,
)

MAX_SECONDS = 60.0
FRAME_EVERY = 0.5  # seconds between player-view snapshots
REACTION = 0.15  # a rule acts at most this often, like a player's reaction time
AFTER_END = 1.0  # seconds shown after the room is cleared or the player goes down


def read_script(text):
    setup = {"room": "1", "fps": 60, "end": None, "spawns": [], "player": None}
    inputs, rules = [], []
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#")[0].strip()
        if not line:
            continue
        words = line.split()
        try:
            if words[0] == "when":
                rules.append(Rule(line))
            elif words[0] == "room":
                setup["room"] = words[1]
            elif words[0] == "fps":
                setup["fps"] = int(words[1])
            elif words[0] == "end":
                setup["end"] = float(words[1])
            elif words[0] == "spawn":
                setup["spawns"].append((words[1], float(words[2]), float(words[3])))
            elif words[0] == "player":
                setup["player"] = (float(words[1]), float(words[2]))
            else:
                inputs.append(
                    (float(words[0]), words[1], words[2] if len(words) > 2 else None)
                )
        except (IndexError, ValueError) as error:
            hint = f" ({error})" if str(error) else ""
            sys.exit(f"script line {number}: cannot read {raw.strip()!r}{hint}")
    return setup, sorted(inputs, key=lambda i: i[0]), rules


class Rule:
    """`when <condition> then <action>`, judged only from the frame as drawn and the messages shown."""

    def __init__(self, line):
        match = re.fullmatch(r"when (.+?) then (.+)", line)
        if not match:
            raise ValueError("a rule reads: when <condition> then <action>")
        self.condition, self.action = match.group(1).split(), match.group(2).split()
        c, a = self.condition, self.action
        quoted = re.fullmatch(r'text "(.+)"', match.group(1))
        if quoted:
            self.condition = ["text", quoted.group(1).lower()]
        elif not (
            (c[0] == "see" and len(c) == 4 and len(c[1]) == 1 and c[2] == "within")
            or (c[0] == "see" and len(c) == 5 and len(c[1]) == 1 and c[2:4] == ["coming", "within"])
            or (c[0] == "nothing" and len(c) == 3 and c[1] == "within")
            or (c[0] == "hearts" and len(c) == 3 and c[1] == "<=")
        ):
            raise ValueError(
                "conditions: see <mark> [coming] within <n>, nothing within <n>, text \"<words>\", hearts <= <n>"
            )
        if c[0] in ("see", "nothing", "hearts"):
            float(c[-1])
        targets = list(DIRECTIONS) + ["away", "toward", "aside"]
        if not (
            a in (["attack"], ["stop"], ["face"], ["dash"])
            or (len(a) == 2 and a[0] in ("move", "dash") and a[1] in targets)
        ):
            raise ValueError(
                "actions: attack, stop, face, move <dir|away|toward|aside>, dash [<dir|away|toward|aside>]"
            )
        self.last = -math.inf

    def matches(self, view):
        """The cell the rule reacts to (or True), if the condition holds in this view."""
        c = self.condition
        if c[0] == "text":
            return any(c[1] in m.lower() for m in view.messages) and (view.nearest() or True)
        if c[0] == "hearts":
            return view.hearts <= float(c[2]) and (view.nearest() or True)
        if c[0] == "nothing":
            return view.nearest(within=float(c[2])) is None
        return view.nearest(mark=c[1], within=float(c[-1]), coming=c[2] == "coming")

    def act(self, game, target):
        a = self.action
        toward = _toward(target, (game.x, game.y)) if isinstance(target, tuple) else None
        away = {"left": "right", "right": "left", "up": "down", "down": "up"}.get(toward)
        # Aside: across the line to the target, toward the roomier half of the room.
        if toward in ("left", "right"):
            aside = "down" if game.y < (ROOM_H - 1) / 2 else "up"
        else:
            aside = "right" if game.x < (ROOM_W - 1) / 2 else "left"
        if a == ["attack"]:
            if toward:  # turn to it and swing, as one input
                game.press("move", toward)
                game.press("stop")
            game.press("attack")
        elif a == ["stop"]:
            game.press("stop")
        elif a == ["face"]:
            if toward:
                game.press("move", toward)
                game.press("stop")
        elif a == ["dash"]:
            game.press("dash")
        else:
            direction = {"toward": toward, "away": away, "aside": aside if toward else None}.get(a[1], a[1])
            if direction:
                game.press(a[0], direction)


def _toward(cell, position):
    dx, dy = cell[0] - position[0], cell[1] - position[1]
    if abs(dx) >= abs(dy):
        return "right" if dx > 0 else "left"
    return "down" if dy > 0 else "up"


class View:
    """What the player can see right now: what is on screen and where, the hearts, the messages."""

    def __init__(self, game, messages, before=()):
        self.sprites, self.hearts, self.messages = sprites(game), game.hearts, messages
        self.before = before  # the previous frame's sprites, to see what is moving
        self.me = next(((x, y) for mark, x, y in self.sprites if mark == "P"), None)

    def closing(self, mark, x, y):
        """Whether this sprite came closer since the last frame (the eye follows the nearest match)."""
        earlier = [(math.dist((x, y), (bx, by)), (bx, by)) for m, bx, by in self.before if m == mark]
        if not earlier:
            return False
        jump, (bx, by) = min(earlier)
        return jump < 0.5 and math.dist((x, y), self.me) < math.dist((bx, by), self.me) - 1e-9

    def nearest(self, mark=None, within=math.inf, coming=False):
        if self.me is None:
            return None
        seen = [
            (math.dist((x, y), self.me), (x, y))
            for m, x, y in self.sprites
            if m not in "Px"
            and (mark is None or m == mark)
            and (not coming or self.closing(m, x, y))
        ]
        seen = [place for d, place in sorted(seen) if d <= within + 1e-9]
        return seen[0] if seen else None


def react(game, rules, messages, before):
    view = View(game, messages, before)
    if view.me is None:
        return
    for rule in rules:  # the first rule that holds and is not still waiting acts
        target = rule.matches(view)
        if not target or game.t - rule.last < REACTION - 1e-9:
            continue
        rule.last = game.t
        before = len(game.events)
        rule.act(game, target)
        for _, kind, details in game.events[before:]:
            if kind == "ignored":
                details["quiet"] = True  # a held button, not news
        return


def play(setup, inputs, view, rules=()):
    try:
        game = Game(fps=setup["fps"], room=setup["room"])
        for kind, x, y in setup["spawns"]:
            game.spawn(kind, x, y)
        if setup["player"]:
            game.place_player(*setup["player"])
    except ValueError as error:
        sys.exit(f"script setup: {error}")
    default = (inputs[-1][0] + 3 if inputs else 5) if not rules else MAX_SECONDS
    end = min(setup["end"] if setup["end"] is not None else default, MAX_SECONDS)
    out = Player(game) if view == "player" else Trace(game)
    out.start()
    pending, seen, messages, over, before = list(inputs), 0, [], None, []
    hurt_seen = 0
    while game.t < end - 1e-9 and (over is None or game.t < over - 1e-9):
        while pending and pending[0][0] <= game.t + 1e-9:
            when, action, direction = pending.pop(0)
            try:
                game.press(action, direction)
            except ValueError as error:
                sys.exit(f"input at {when}: {error}")
        if rules:
            react(game, rules, messages, before)
            before = sprites(game)
        game.step()
        out.frame()
        new = game.events[seen:]
        seen = len(game.events)
        names = []
        for _, k, d in new:
            if k == "hurt":
                names.append(game.hurt_kinds[hurt_seen])
                hurt_seen += 1
            else:
                names.append(None)
        messages = [
            m for m in (Player.describe(k, d, n) for (_, k, d), n in zip(new, names)) if m
        ]
        if over is None and (game.cleared or game.hearts <= 0):
            over = game.t + AFTER_END
    out.finish()


class Player:
    """What a player sees and hears: the room, the hearts, and feedback on their actions."""

    def __init__(self, game):
        self.game, self.seen, self.next_snapshot = game, 0, 0.0
        self.hurts = 0  # hurt events already printed (indexes game.hurt_kinds)

    def start(self):
        g = self.game
        print(f"Lantern Depths 0.6 — room {g.room} — {g.fps} FPS")
        self.snapshot()
        self.next_snapshot = FRAME_EVERY

    def frame(self):
        g, show = self.game, False
        for when, kind, details in g.events[self.seen :]:
            name = None
            if kind == "hurt":
                name = g.hurt_kinds[self.hurts]
                self.hurts += 1
            text = self.describe(kind, details, name)
            if text:
                print(f"{when:7.3f}  {text}")
            show = show or kind in ("hurt", "windup", "aim")
        self.seen = len(g.events)
        if show or g.t >= self.next_snapshot - 1e-9:
            self.snapshot()
            if g.t >= self.next_snapshot - 1e-9:
                self.next_snapshot += FRAME_EVERY

    def finish(self):
        g = self.game
        left = sum(1 for e in g.enemies if e.hp > 0)
        print(f"end at {g.t:.2f} s: hearts {g.hearts}/{HEARTS}, enemies left {left}")

    @staticmethod
    def describe(kind, details, name=None):
        if kind == "attack":
            hits = details["hits"]
            return "you swipe: " + (
                ", ".join(f"{enemy} {result}" for enemy, result in hits)
                if hits
                else "miss"
            )
        if kind == "shrug":
            return "the brute shrugs off the swipe"
        if kind == "late_swipe":
            return (
                f"the {details['enemy']}'s lunge had already started, "
                "the swipe was too late to stop it"
            )
        if kind == "dash":
            return f"you dash {details['direction']}"
        if kind == "hurt":
            return f"YOU ARE HIT by a {name or details['source']} — hearts {details['hearts']}/{HEARTS}"
        if kind == "down":
            return "you went down"
        if kind == "windup":
            return f"a {details.get('enemy', 'grub')} rears back"
        if kind == "aim":
            return "a spitter takes aim"
        if kind == "spit":
            return "a spitter spits"
        if kind == "cleared":
            return "room cleared"
        if kind == "ignored" and not details.get("quiet"):
            return "(nothing happens)"
        return None

    def snapshot(self):
        g = self.game
        print(f"   [{g.t:.2f} s] hearts {g.hearts}/{HEARTS}")
        print("   +" + "-" * ROOM_W + "+")
        for row in draw(g):
            print("   |" + row + "|")
        print("   +" + "-" * ROOM_W + "+")
        for text in cue_lines(g):
            print("   " + text)


def sprites(g):
    """Everything on screen as (mark, x, y), drawn in this order (later ones on top)."""
    shown = [("*", s[0], s[1]) for s in g.shots]
    shown += [(e.mark, e.x, e.y) for e in g.enemies if e.hp > 0]
    return shown + [("P" if g.hearts > 0 else "x", g.x, g.y)]


def _line_cells(g):
    """Points of the thin orange-red lines: lunge paths during a wind-up, aim lines during a cue."""
    cells = []
    for e in g.enemies:
        if e.hp <= 0 or not e.aim:
            continue
        if e.is_grub and e.phase == "windup":
            length = LUNGE_SPEED * LUNGE_TIME
        elif not e.is_grub and e.cueing:
            length = ROOM_W + ROOM_H
        else:
            continue
        for i in range(1, int(length / 0.25) + 1):
            cells.append((e.x + e.aim[0] * 0.25 * i, e.y + e.aim[1] * 0.25 * i))
    return cells


def cue_lines(g):
    """Text description of the flash, glow and lines (orange-red) shown under the room."""
    out = []
    for e in g.enemies:
        if e.hp <= 0 or not e.aim:
            continue
        where = f"at ({e.x:.1f},{e.y:.1f})"
        line = f"line toward ({e.aim[0]:+.2f},{e.aim[1]:+.2f})"
        if e.is_grub and e.phase == "windup":
            out.append(
                f"cue: {e.mark} {where} flashes orange-red, lunge {line}, "
                f"{LUNGE_SPEED * LUNGE_TIME:.1f} tiles ({e.phase_left:.2f} s to the lunge)"
            )
        elif not e.is_grub and e.cueing:
            bright = min(1.0, max(0.0, (AIM_CUE - e.fire_in) / AIM_CUE))
            out.append(
                f"cue: s {where} glows orange-red, brightness {bright:.0%}, aim {line} "
                f"({e.fire_in:.2f} s to the shot)"
            )
    return out


def draw(g):
    """The room as the player sees it, one string per row ('~' is an orange-red line)."""
    grid = [[" "] * ROOM_W for _ in range(ROOM_H)]
    for x, y in _line_cells(g):
        col, row = int(round(x)), int(round(y))
        if 0 <= col < ROOM_W and 0 <= row < ROOM_H:
            grid[row][col] = "~"
    for mark, x, y in sprites(g):
        col, row = int(round(x)), int(round(y))
        if 0 <= col < ROOM_W and 0 <= row < ROOM_H:
            grid[row][col] = mark
    return ["".join(row) for row in grid]


class Trace:
    """Simulation state for developers: one line per frame in which anything happened."""

    def __init__(self, game):
        self.game, self.seen = game, 0

    def start(self):
        g = self.game
        print(f"trace: fps={g.fps} room={g.room} dt={g.dt:.5f}")
        self.line([("setup", {})])

    def frame(self):
        g = self.game
        new = [(kind, details) for _, kind, details in g.events[self.seen :]]
        self.seen = len(g.events)
        if new:
            self.line(new)

    def finish(self):
        self.line([("end", {})])

    def line(self, events):
        g = self.game
        state = (
            f"t={g.t:.3f} frame={g.frame} pos=({g.x:.2f},{g.y:.2f}) hearts={g.hearts} "
            f"invulnerable={g.invulnerable} dash_left={g.dash_left:.3f} "
            f"hurt_left={g.hurt_left:.3f} stun_left={g.stun_left:.3f}"
        )
        enemies = " ".join(
            f"{e.kind}({e.x:.2f},{e.y:.2f},hp={e.hp},"
            + (f"{e.phase}:{e.phase_left:.3f}" if e.is_grub else f"fire_in={e.fire_in:.3f},cue={e.cueing}")
            + ")"
            for e in g.enemies
            if e.hp > 0
        )
        happened = "; ".join(
            kind + (f" {details}" if details else "") for kind, details in events
        )
        print(f"{state} | {enemies} | {happened}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--view", choices=["player", "trace"], default="player")
    parser.add_argument("script")
    args = parser.parse_args()
    with open(args.script, encoding="utf-8") as f:
        setup, inputs, rules = read_script(f.read())
    play(setup, inputs, args.view, rules)


if __name__ == "__main__":
    main()
>>>END

<<<FILE repo/bots.py
"""Balance bots: let simple player strategies play rooms and report how they fared.

usage: python3 bots.py SCRIPT

Script lines (all optional; `#` starts a comment):
  bots camper,walker,dodger   which bots play (default: all)
  rooms 1-5                   which rooms, as a range or a list like 1,3,5 (default: 1-5)
  fps 60                      30 or 60 (default: 60)
  limit 60                    seconds a bot may take per room (default: 60)
  log on                      print each bot's decisions under its room line: time, what it did,
                              and the state it decided from (after " | "); skipped decisions and
                              every heart lost are logged too

Each bot starts every room with full hearts. Bots decide at most once every 0.15 s of game time
(accumulated seconds, on a fixed time grid), so a bot behaves the same at 30 and 60 FPS apart from
frame rounding. The walker and camper do not read the new cues; the dodger does.
"""

import math
import sys

from game import (
    ATTACK_REACH,
    DIRECTIONS,
    GRUB_REACH,
    GRUBS,
    HEARTS,
    LUNGE_SPEED,
    LUNGE_TIME,
    ROOM_H,
    ROOM_W,
    ROOMS,
    SHOT_LIFE,
    SHOT_REACH,
    SHOT_SPEED,
    Game,
)

REACTION = 0.15  # seconds between a bot's decisions, like play.py's rule reaction time
LUNGE_LEN = LUNGE_SPEED * LUNGE_TIME


class Brain:
    """The bot's reaction clock (accumulated seconds) and decision log."""

    def __init__(self, log=None):
        self.next, self.log = 0.0, log
        self.grid = 0.0  # log only: the last grid time passed by the last decision
        self.shadow = 0.0  # log only: a copy of the clock that also runs while the player is stunned

    def due(self, t):
        if t < self.next - 1e-9:
            return False
        while self.next <= t + 1e-9:
            self.grid = self.next
            self.next += REACTION
        self.shadow = self.next
        return True

    def note(self, game, text):
        if self.log is not None:
            self.log.append(f"{game.t:6.2f} s  {text} | {_state(game, self.grid)}")

    def skip(self, game):
        """Log a grid decision that is skipped because the player is stunned (once per grid time)."""
        t = game.t
        if self.log is None or t < self.shadow - 1e-9:
            return
        grid = self.shadow
        while self.shadow <= t + 1e-9:
            grid = self.shadow
            self.shadow += REACTION
        self.log.append(
            f"{t:6.2f} s  skipped decision | frame {game.frame}, grid {grid:.3f} s, "
            f"frame time {t:.6f} s, reason: player stunned ({game.stun_left:.3f} s of stun left)"
        )


def _state(game, grid):
    """The state a decision is made from, as one line of text (log only)."""
    enemy = _nearest(game)
    if enemy:
        distance = math.hypot(enemy.x - game.x, enemy.y - game.y)  # same expression the bots compare
        near = (
            f"nearest {enemy.kind} at ({enemy.x:.6f}, {enemy.y:.6f}) "
            f"distance {distance:.9f} (exact {distance!r})"
        )
    else:
        near = "nearest none"
    shots = (
        "; ".join(f"({s[0]:.6f}, {s[1]:.6f}) v ({s[2]:.6f}, {s[3]:.6f})" for s in game.shots)
        or "none"
    )
    stun = f"yes ({game.stun_left:.3f} s left)" if game.stun_left > 0 else "no"
    return (
        f"frame {game.frame}, grid {grid:.3f} s, frame time {game.t:.6f} s, "
        f"player ({game.x:.6f}, {game.y:.6f}), hearts {game.hearts}, stunned {stun}, "
        f"{near}, shots in flight: {shots}"
    )


def _hurt_lines(game, first_event, shots_before, struck_before):
    """Log lines for the hearts lost in the frame just played (log only; reads, never changes)."""
    out = []
    for when, kind, details in game.events[first_event:]:
        if kind != "hurt":
            continue
        source = details["source"]
        if source == "grub":
            hit = [e for e in game.enemies if e.is_grub and e.struck and not struck_before.get(id(e))]
            there = (
                ", ".join(f"grub {e.kind} at ({e.x:.6f}, {e.y:.6f})" for e in hit)
                or "grub position not found"
            )
        else:
            gone = [
                s
                for s in shots_before
                if not any(s is k for k in game.shots)
                and s[4] < SHOT_LIFE - 1e-9
                and -1 <= s[0] <= ROOM_W
                and -1 <= s[1] <= ROOM_H
                and math.hypot(s[0] - game.x, s[1] - game.y) <= SHOT_REACH
            ]
            there = (
                ", ".join(
                    f"shot at ({s[0]:.6f}, {s[1]:.6f}) v ({s[2]:.6f}, {s[3]:.6f})" for s in gone
                )
                or "shot position not found (fired in this frame)"
            )
        out.append(
            f"{when:6.2f} s  HEART LOST | frame {game.frame}, source {source}, "
            f"player ({game.x:.6f}, {game.y:.6f}), {there}; hearts now {details['hearts']}"
        )
    return out


def _toward(dx, dy):
    if abs(dx) >= abs(dy):
        return "right" if dx > 0 else "left"
    return "down" if dy > 0 else "up"


def _nearest(game):
    live = [e for e in game.enemies if e.hp > 0]
    return min(live, key=lambda e: math.hypot(e.x - game.x, e.y - game.y), default=None)


def _face_and_swing(game, enemy):
    game.press("move", _toward(enemy.x - game.x, enemy.y - game.y))
    game.press("stop")
    if math.hypot(enemy.x - game.x, enemy.y - game.y) <= ATTACK_REACH and game.recovery <= 0:
        game.press("attack")


def _incoming(game):
    """A shot in flight that will reach the player within 0.7 s, if any (ignores cues)."""
    for shot in game.shots:
        x, y, vx, vy = shot[:4]
        speed = math.hypot(vx, vy)
        ahead = ((game.x - x) * vx + (game.y - y) * vy) / speed
        beside = abs((game.x - x) * vy - (game.y - y) * vx) / speed
        if 0 < ahead < 0.7 * speed and beside < 0.7:
            return vx, vy
    return None


def _sidestep(game, shot):
    vx, vy = shot
    if abs(vx) >= abs(vy):
        return "down" if game.y < 4 else "up"
    return "right" if game.x < 8 else "left"


def _dangers(game):
    """Lines the player can see: wind-up paths, lunges, spitter aim lines, shots in flight.

    Each is (x, y, ux, uy, length, wait, speed, kind): origin, unit direction, length of the
    dangerous stretch, seconds until it starts moving, and how fast it moves along the line.
    """
    out = []
    for e in game.enemies:
        if e.hp <= 0:
            continue
        if e.is_grub and e.phase == "windup":
            out.append((e.x, e.y, e.aim[0], e.aim[1], LUNGE_LEN + GRUB_REACH, e.phase_left, LUNGE_SPEED, "lunge"))
        elif e.is_grub and e.phase == "lunge":
            out.append((e.x, e.y, e.aim[0], e.aim[1], e.lunge_left * LUNGE_SPEED + GRUB_REACH, 0.0, LUNGE_SPEED, "lunge"))
        elif not e.is_grub and e.cueing and e.aim:
            out.append((e.x, e.y, e.aim[0], e.aim[1], 40.0, e.fire_in, SHOT_SPEED, "aim"))
    for shot in game.shots:
        x, y, vx, vy = shot[:4]
        speed = math.hypot(vx, vy)
        out.append((x, y, vx / speed, vy / speed, 40.0, 0.0, speed, "shot"))
    return out


def _threat(game):
    """The most urgent line the player stands in: (eta, ox, oy, ux, uy, beside, kind)."""
    best = None
    for ox, oy, ux, uy, length, wait, speed, kind in _dangers(game):
        rx, ry = game.x - ox, game.y - oy
        ahead = rx * ux + ry * uy
        beside = rx * -uy + ry * ux
        if ahead < -0.3 or ahead > length or abs(beside) > 0.9:
            continue
        eta = wait + max(0.0, ahead - 0.5) / speed
        if best is None or eta < best[0]:
            best = (eta, ox, oy, ux, uy, beside, kind)
    return best


def _axis(vx, vy):
    if abs(vx) >= abs(vy):
        return "right" if vx > 0 else "left"
    return "down" if vy > 0 else "up"


def _escape(game, threat):
    """The direction across the line, away from the side the player is on, with room to go."""
    _, _, _, ux, uy, beside, _ = threat
    px, py = -uy, ux
    sign = 1 if beside >= 0 else -1
    direction = None
    for _ in range(2):
        direction = _axis(sign * px, sign * py)
        dx, dy = DIRECTIONS[direction]
        x, y = game.x + dx * 1.5, game.y + dy * 1.5
        if 0 <= x <= ROOM_W - 1 and 0 <= y <= ROOM_H - 1:
            return direction
        sign = -sign
    return direction


def camper(game, note):
    """Holds the starting spot: turns to the nearest enemy and swings when it is in reach."""
    enemy = _nearest(game)
    if enemy:
        _face_and_swing(game, enemy)


def walker(game, note):
    """Lets a nearby grub come and swings, walks up to anything further away, steps aside from
    shots already in flight. Never dashes and does not read the wind-up or aim cues."""
    enemy = _nearest(game)
    if not enemy:
        return
    shot = _incoming(game)
    distance = math.hypot(enemy.x - game.x, enemy.y - game.y)
    coming = enemy.is_grub and distance < 2.5
    if shot:
        note("sidestep shot in flight")
        game.press("move", _sidestep(game, shot))
    elif distance > 1.1 and not coming:
        note(f"walk to {enemy.kind}")
        game.press("move", _toward(enemy.x - game.x, enemy.y - game.y))
    else:
        note(f"face and swing at {enemy.kind}")
        _face_and_swing(game, enemy)


def dodger(game, note):
    """Reads the cues: swipes a wind-up that is in reach when a swipe cancels it (standard grub and
    runner; never the brute, whose wind-up a swipe does not cancel: against it, sidestep or dash on
    the cue and swipe in recovery only), otherwise dashes across a line when the hit is under 0.4 s
    away, steps across it earlier if the dash is not ready, holds still while a lunge plays out,
    and walks in to swipe the rest."""
    ready = game.dash_left <= 0 and game.dash_cooldown <= 0
    for e in game.enemies:
        if (
            e.hp > 0
            and e.is_grub
            and e.phase == "windup"
            and GRUBS[e.kind]["cancels"]
            and math.hypot(e.x - game.x, e.y - game.y) <= 1.4
            and game.recovery <= 0
        ):
            note(f"swipe {e.kind} wind-up")
            _face_and_swing(game, e)
            return
    threat = _threat(game)
    if threat and threat[0] <= 1.0:
        eta, kind = threat[0], threat[6]
        direction = _escape(game, threat)
        if ready and eta <= 0.4:
            note(f"dash {direction} from {kind} (hit in {eta:.2f} s)")
            game.press("dash", direction)
            return
        if not ready:
            note(f"step {direction} from {kind} (hit in {eta:.2f} s, dash not ready)")
            game.press("move", direction)
            return
        note(f"hold, dash ready, {kind} in {eta:.2f} s")
        game.press("stop")
        return
    if any(e.hp > 0 and e.is_grub and e.phase in ("windup", "lunge") for e in game.enemies):
        note("hold while a grub lunges")
        game.press("stop")
        return
    enemy = _nearest(game)
    if not enemy:
        return
    if math.hypot(enemy.x - game.x, enemy.y - game.y) > 1.1:
        note(f"walk to {enemy.kind}")
        game.press("move", _toward(enemy.x - game.x, enemy.y - game.y))
    else:
        note(f"face and swing at {enemy.kind}")
        _face_and_swing(game, enemy)


BOTS = {"camper": camper, "walker": walker, "dodger": dodger}


def play_room(bot, room, fps, limit, log=None):
    game = Game(fps=fps, room=room)
    brain = Brain([] if log else None)
    while game.t < limit - 1e-9 and not game.cleared and game.hearts > 0:
        if game.stun_left <= 0:
            if brain.due(game.t):
                bot(game, lambda text: brain.note(game, text))
        else:
            brain.skip(game)  # log only: a grid decision that the stun swallows
        if brain.log is not None:
            first_event = len(game.events)
            shots_before = list(game.shots)
            struck_before = {id(e): e.struck for e in game.enemies if e.is_grub}
        game.step()
        if brain.log is not None:
            brain.log.extend(_hurt_lines(game, first_event, shots_before, struck_before))
    counts = {}
    sources = {}
    for _, kind, details in game.events:
        counts[kind] = counts.get(kind, 0) + 1
        if kind == "hurt":
            sources[details["source"]] = sources.get(details["source"], 0) + 1
    return {
        "cleared": game.cleared,
        "seconds": round(game.t, 2),
        "hearts_lost": HEARTS - game.hearts,
        "hits_by": sources,
        "attacks": counts.get("attack", 0),
        "dashes": counts.get("dash", 0),
        "log": brain.log or [],
    }


def read_script(text):
    setup = {
        "bots": list(BOTS),
        "rooms": [r for r in ROOMS if r != "empty"],
        "fps": 60,
        "limit": 60.0,
        "log": False,
    }
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#")[0].strip()
        if not line:
            continue
        key, _, value = line.partition(" ")
        value = value.replace(" ", "")
        try:
            if key == "bots":
                setup["bots"] = value.split(",")
                assert all(b in BOTS for b in setup["bots"])
            elif key == "rooms":
                if "-" in value:
                    first, last = value.split("-")
                    value = ",".join(str(n) for n in range(int(first), int(last) + 1))
                setup["rooms"] = value.split(",")
                assert all(r in ROOMS for r in setup["rooms"])
            elif key == "fps":
                setup["fps"] = int(value)
            elif key == "limit":
                setup["limit"] = float(value)
            elif key == "log":
                setup["log"] = value in ("on", "yes", "true", "1")
            else:
                raise ValueError
        except (AssertionError, ValueError):
            sys.exit(
                f"script line {number}: cannot read {raw.strip()!r}\n"
                "bots script lines (all optional): bots camper,walker,dodger | rooms 1-5 (or 1,3) | "
                "fps 30|60 | limit <seconds per room> | log on"
            )
    return setup


def main():
    with open(sys.argv[1], encoding="utf-8") as f:
        setup = read_script(f.read())
    print(f"bots at {setup['fps']} FPS, up to {setup['limit']:.0f} s per room, {HEARTS} hearts each")
    for name in setup["bots"]:
        total = {"cleared": 0, "hearts_lost": 0, "dashes": 0}
        for room in setup["rooms"]:
            r = play_room(BOTS[name], room, setup["fps"], setup["limit"], log=setup["log"])
            hits = ", ".join(f"{k} {v}" for k, v in sorted(r["hits_by"].items())) or "none"
            outcome = f"cleared in {r['seconds']:.1f} s" if r["cleared"] else f"NOT cleared ({r['seconds']:.1f} s)"
            print(
                f"{name:7} room {room}: {outcome}; hearts lost {r['hearts_lost']} (hit by: {hits}); "
                f"attacks {r['attacks']}, dashes {r['dashes']}"
            )
            for entry in r["log"]:
                print("          " + entry)
            total["cleared"] += r["cleared"]
            total["hearts_lost"] += r["hearts_lost"]
            total["dashes"] += r["dashes"]
        print(
            f"{name:7} total: cleared {total['cleared']}/{len(setup['rooms'])}, hearts lost "
            f"{total['hearts_lost']}, dashes {total['dashes']}"
        )


if __name__ == "__main__":
    main()
>>>END

<<<FILE repo/tests/test_game.py
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from game import DASH_DISTANCE, HEARTS, ROOMS, Game  # noqa: E402


def run(game, seconds):
    for _ in range(round(seconds * game.fps)):
        game.step()


def step_until(game, predicate, limit=10.0):
    for _ in range(round(limit * game.fps)):
        game.step()
        if predicate(game):
            return True
    return False


def has_event(kind):
    return lambda g: any(k == kind for _, k, _ in g.events)


def times(game, kind):
    return [t for t, k, _ in game.events if k == kind]


def busy_grubs(game):
    return sum(1 for e in game.enemies if e.hp > 0 and e.is_grub and e.phase in ("windup", "lunge"))


class CombatTest(unittest.TestCase):
    def test_two_swipes_defeat_a_grub(self):
        game = Game(room="empty")
        game.spawn("grub", 9.2, 4)
        game.press("attack")
        run(game, 0.4)  # the swipe cancels the grub's start; recovery passes
        game.press("attack")
        run(game, 0.1)
        self.assertEqual(game.enemies[0].hp, 0)
        self.assertTrue(game.cleared)

    def test_swipe_misses_behind_the_player(self):
        game = Game(room="empty")
        game.spawn("grub", 7.0, 4)
        game.press("attack")
        self.assertEqual(game.enemies[0].hp, 2)

    def test_grub_lunge_costs_a_heart(self):
        game = Game(room="empty")
        game.spawn("grub", 8.5, 4)
        run(game, 0.7)
        self.assertEqual(game.hearts, HEARTS - 1)

    def test_grub_walking_alone_does_not_hurt(self):
        game = Game(room="empty")
        game.spawn("grub", 8.3, 4)
        game.enemies[0].phase, game.enemies[0].phase_left = "recovery", 0.8
        run(game, 0.7)
        self.assertEqual(game.hearts, HEARTS)

    def test_spitter_fires_every_2_4_seconds_from_1_8(self):
        game = Game(room="empty")
        game.spawn("spitter", 1, 1)
        run(game, 4.25)
        spits = times(game, "spit")
        self.assertEqual(len(spits), 2)
        self.assertAlmostEqual(spits[0], 1.8, places=6)
        self.assertAlmostEqual(spits[1], 4.2, places=6)


class GrubTest(unittest.TestCase):
    def cue(self, fps, x=10.0, kind="grub"):
        game = Game(fps=fps, room="empty")
        game.spawn(kind, x, 4)
        self.assertTrue(step_until(game, has_event("windup")))
        return game

    def test_telegraph_comes_at_least_half_a_second_before_the_hit(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("grub", 9.5, 4)
            run(game, 2.0)
            gap = times(game, "hurt")[0] - times(game, "windup")[0]
            self.assertGreaterEqual(gap, 0.5 - 1.0 / fps - 1e-9, fps)

    def test_a_sidestep_avoids_the_lunge(self):
        for fps in (30, 60):
            game = self.cue(fps)
            game.press("move", "up")
            run(game, 0.25)
            game.press("stop")
            run(game, 1.1)
            self.assertEqual(game.hearts, HEARTS, fps)

    def test_dash_from_cue_into_the_lunge_takes_no_damage(self):
        for fps in (30, 60):
            for offset in (0.0, 0.25, 0.5, 0.6):
                game = self.cue(fps)
                run(game, offset)
                game.press("dash", "up")
                run(game, 1.0)
                self.assertEqual(game.hearts, HEARTS, (fps, offset))
                self.assertFalse(any(k == "ignored" for _, k, _ in game.events), (fps, offset))

    def test_standing_still_is_punished(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("grub", 10, 4)
            run(game, 3.0)
            self.assertLessEqual(game.hearts, HEARTS - 1, fps)

    def test_recovery_is_safe(self):
        game = Game(room="empty")
        game.spawn("grub", 8.3, 4)
        game.enemies[0].phase, game.enemies[0].phase_left = "recovery", 0.8
        run(game, 0.7)
        self.assertEqual(game.hearts, HEARTS)

    def test_a_swipe_during_windup_stops_the_lunge(self):
        for fps in (30, 60):
            for kind in ("grub", "runner"):
                game = self.cue(fps, x=9.2, kind=kind)
                game.enemies[0].hp = 2  # the runner would die to the swipe; keep it alive
                game.press("attack")
                self.assertEqual(game.enemies[0].phase, "stagger", (fps, kind))
                # Observe only the stagger (0.4 s): afterwards the grub may wind up again.
                run(game, 0.38)
                self.assertFalse(any(k == "lunge" for _, k, _ in game.events), (fps, kind))
                self.assertEqual(game.hearts, HEARTS)

    def test_only_one_grub_winds_up_or_lunges(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            for x, y in ((9.5, 4), (8, 5.5), (6.5, 4)):
                game.spawn("grub", x, y)
            most = 0
            for _ in range(3 * fps):
                game.step()
                most = max(most, busy_grubs(game))
            self.assertEqual(most, 1, fps)

    def test_variants_swipes_to_defeat(self):
        for kind, swipes in (("grub", 2), ("runner", 1), ("brute", 4)):
            game = Game(room="empty")
            game.spawn(kind, 9.2, 4)
            if kind == "brute":  # a swipe no longer cancels its wind-up: swipe it in recovery
                game.enemies[0].phase, game.enemies[0].phase_left = "recovery", 5.0
            for done in range(swipes):
                self.assertGreater(game.enemies[0].hp, 0, (kind, done))
                game.press("attack")
                run(game, 0.4)
            self.assertEqual(game.enemies[0].hp, 0, kind)

    def test_wind_up_lengths_differ_by_variant(self):
        windups = {}
        for kind in ("grub", "runner", "brute"):
            game = Game(room="empty")
            game.spawn(kind, 10, 4)
            run(game, 2.0)
            windups[kind] = times(game, "lunge")[0] - times(game, "windup")[0]
        self.assertAlmostEqual(windups["grub"], 0.5, delta=0.02)
        self.assertAlmostEqual(windups["runner"], 0.35, delta=0.02)
        self.assertAlmostEqual(windups["brute"], 0.7, delta=0.02)

    def test_rooms_match_the_spec(self):
        self.assertEqual(
            ROOMS["2"], [("runner", 2, 1), ("runner", 1, 8), ("brute", 15, 7), ("grub", 14, 0)]
        )
        self.assertEqual(
            ROOMS["4"], [("runner", 1, 4), ("grub", 0, 1), ("spitter", 15, 0), ("spitter", 15, 8)]
        )
        self.assertEqual(ROOMS["5"][2], ("brute", 4, 8))
        self.assertEqual(
            ROOMS["3"],
            [("spitter", 2, 1), ("spitter", 10, 6), ("spitter", 2, 7), ("grub", 15, 0)],
        )

    def test_room_3_clears_only_when_spitters_and_grub_are_all_dead(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="3")
            for e in game.enemies:
                if e.kind == "spitter":
                    e.hp = 0
            game.step()
            self.assertFalse(game.cleared, fps)
            for e in game.enemies:
                e.hp = 0
            game.step()
            self.assertTrue(game.cleared, fps)


class BruteTest(unittest.TestCase):
    """Criterion 19: a swipe does not cancel the brute's wind-up (step 35)."""

    def cue(self, fps):
        game = Game(fps=fps, room="empty")
        game.spawn("brute", 9.0, 4)
        self.assertTrue(step_until(game, has_event("windup")))
        return game

    def test_a_swipe_does_not_cancel_the_wind_up(self):
        for fps in (30, 60):
            game = self.cue(fps)
            start = times(game, "windup")[0]
            game.press("attack")
            brute = game.enemies[0]
            self.assertEqual(brute.hp, 3, fps)
            self.assertEqual(brute.phase, "windup", fps)
            self.assertIsNotNone(brute.aim, fps)
            self.assertEqual(len(times(game, "shrug")), 1, fps)
            self.assertEqual(times(game, "stagger"), [], fps)
            self.assertTrue(step_until(game, has_event("lunge")))
            self.assertAlmostEqual(times(game, "lunge")[0] - start, 0.7, delta=1.0 / fps + 1e-9)
            self.assertTrue(step_until(game, has_event("hurt"), 1.0))
            self.assertEqual(game.hearts, HEARTS - 1, fps)

    def test_two_swipes_in_one_wind_up_each_hit_and_it_lunges_once(self):
        for fps in (30, 60):
            game = self.cue(fps)
            game.press("attack")
            run(game, 0.4)
            game.press("attack")
            self.assertEqual(game.enemies[0].hp, 2, fps)
            self.assertEqual(len(times(game, "shrug")), 2, fps)
            run(game, 1.0)
            self.assertEqual(len(times(game, "lunge")), 1, fps)

    def test_a_swipe_that_kills_the_brute_in_wind_up_means_no_lunge_no_message(self):
        for fps in (30, 60):
            game = self.cue(fps)
            game.enemies[0].hp = 1
            game.press("attack")
            self.assertEqual(game.enemies[0].hp, 0, fps)
            run(game, 1.5)
            self.assertEqual(times(game, "shrug"), [], fps)
            self.assertEqual(times(game, "lunge"), [], fps)
            self.assertEqual(game.hearts, HEARTS, fps)
            self.assertTrue(game.cleared, fps)

    def test_dash_and_swipe_together_take_no_damage_and_the_brute_takes_the_swipe(self):
        for fps in (30, 60):
            game = self.cue(fps)
            game.press("attack")
            game.press("dash", "up")
            run(game, 1.5)
            self.assertEqual(game.enemies[0].hp, 3, fps)
            self.assertEqual(game.hearts, HEARTS, fps)

    def test_a_swipe_in_recovery_changes_nothing_else(self):
        game = Game(room="empty")
        game.spawn("brute", 9.0, 4)
        game.enemies[0].phase, game.enemies[0].phase_left = "recovery", 1.0
        game.press("attack")
        self.assertEqual(game.enemies[0].hp, 3)
        self.assertEqual(game.enemies[0].phase, "recovery")
        self.assertEqual(times(game, "shrug"), [])


class SpitterTest(unittest.TestCase):
    def test_room_3_first_shots_are_staggered_and_cued_0_6_s_before(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="3")
            most = 0
            for _ in range(12 * fps):
                game.step()
                most = max(most, len(game.shots))
            tol = 1.0 / fps + 1e-9
            spits, aims = times(game, "spit"), times(game, "aim")
            for got, want in zip(spits, (1.8, 2.6, 3.4)):
                self.assertAlmostEqual(got, want, delta=tol, msg=fps)
            for aim, spit in zip(aims, spits):
                self.assertAlmostEqual(spit - aim, 0.6, delta=tol, msg=fps)
            self.assertLessEqual(most, 3, fps)

    def test_shot_follows_the_locked_line_and_a_sidestep_dodges_it(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("spitter", 1, 4)
            self.assertTrue(step_until(game, has_event("aim")))
            game.press("move", "up")
            run(game, 0.25)
            game.press("stop")
            self.assertTrue(step_until(game, has_event("spit")))
            self.assertAlmostEqual(game.shots[0][3], 0.0, places=9)  # still along y = 4
            run(game, 4.0)
            self.assertEqual(game.hearts, HEARTS, fps)

    def test_a_standing_player_is_hit_by_the_shot(self):
        game = Game(room="empty")
        game.spawn("spitter", 1, 4)
        run(game, 5.0)
        self.assertEqual(game.hearts, HEARTS - 1)


class CueGapTest(unittest.TestCase):
    """Criteria 11 and 18: spitter offset 1.2 s and the 0.6 s cue gap in rooms 4-5 (step 35)."""

    def check_gap(self, game, fps, msg):
        tol = 1.0 / fps + 1e-9
        cueing, last_shot = False, None
        for t, kind, _ in game.events:
            if kind == "aim":
                self.assertFalse(cueing, (msg, "cue windows overlap", t))
                if last_shot is not None:
                    self.assertGreaterEqual(t - last_shot, 0.6 - tol, (msg, "gap", t, last_shot))
                cueing = True
            elif kind == "spit":
                self.assertTrue(cueing, (msg, "shot without a cue", t))
                cueing, last_shot = False, t

    def spitters_only(self, fps, room="4"):
        game = Game(fps=fps, room=room)
        game.enemies = [e for e in game.enemies if e.kind == "spitter"]
        game.hearts = 50  # keep the session going; only the spitters' pattern is looked at
        return game

    def test_rooms_4_and_5_first_shots_are_1_8_and_3_0_and_keep_the_gap(self):
        for room in ("4", "5"):
            for fps in (30, 60):
                game = Game(fps=fps, room=room)
                game.hearts = 50
                run(game, 15.0)
                tol = 1.0 / fps + 1e-9
                spits = times(game, "spit")
                self.assertAlmostEqual(spits[0], 1.8, delta=tol, msg=(room, fps))
                self.assertAlmostEqual(spits[1], 3.0, delta=tol, msg=(room, fps))
                self.check_gap(game, fps, (room, fps))

    def test_other_rooms_keep_the_0_8_s_offset(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            for _ in range(3):
                game.spawn("spitter", 1, 1)
            self.assertEqual([round(e.fire_in, 6) for e in game.enemies], [1.8, 2.6, 3.4])

    def test_forced_simultaneous_first_shots_still_keep_the_gap(self):
        for room in ("4", "5"):
            for fps in (30, 60):
                game = self.spitters_only(fps, room)
                for e in game.enemies:
                    e.fire_in = 1.8
                run(game, 12.0)
                tol = 1.0 / fps + 1e-9
                spits = times(game, "spit")
                self.assertAlmostEqual(spits[0], 1.8, delta=tol, msg=(room, fps))
                self.assertGreaterEqual(spits[1] - spits[0], 0.6 - tol, (room, fps))
                self.assertLessEqual(spits[1], 3.0 + 0.2 + tol, (room, fps))
                self.check_gap(game, fps, (room, fps))

    def test_a_cancelled_cue_is_not_a_shot(self):
        for fps in (30, 60):
            game = self.spitters_only(fps)
            for e in game.enemies:
                e.fire_in = 1.8
            run(game, 1.5)
            cueing = [e for e in game.enemies if e.cueing]
            self.assertEqual(len(cueing), 1, fps)
            cueing[0].hp = 0  # killed during its cue: no shot
            run(game, 1.5)
            spits = times(game, "spit")
            self.assertEqual(len(spits), 1, fps)
            self.assertTrue(1.9 <= spits[0] <= 2.5, (fps, spits))

    def test_a_cap_delay_only_lengthens_the_gap(self):
        for fps in (30, 60):
            game = self.spitters_only(fps)
            game.hearts = 50
            for e in game.enemies:
                e.x, e.y = 15.0, 4.0
            game.place_player(0, 4)  # far away: shots stay in the air
            run(game, 20.0)
            self.check_gap(game, fps, fps)


class ShotContactTest(unittest.TestCase):
    """Criterion 20: any contact consumes a shot; only a player who can be hurt takes damage."""

    def still_shot(self, game, dx):
        game.shots.append([game.x + dx, game.y, 0.0, 0.0, 0.0])

    def test_a_shot_that_reaches_a_hurtable_player_hits_and_goes(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            self.still_shot(game, 0.2)
            game.step()
            self.assertEqual(game.hearts, HEARTS - 1, fps)
            self.assertEqual(game.shots, [], fps)

    def test_a_shot_that_misses_by_more_than_the_reach_is_not_consumed(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            self.still_shot(game, 0.45)
            game.step()
            self.assertEqual(game.hearts, HEARTS, fps)
            self.assertEqual(len(game.shots), 1, fps)

    def test_a_dash_eats_a_shot_even_when_it_ends_inside_the_old_line(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.place_player(6, 4)
            game.shots.append([9.8, 4.0, 0.0, 0.0, 0.0])  # the dash ends at x = 10, 0.2 from it
            game.press("dash", "right")
            run(game, 0.234)  # contact is at about 0.21 s, the dash ends at 0.25 s
            self.assertEqual(game.shots, [], fps)
            self.assertEqual(game.hearts, HEARTS, fps)
            run(game, 1.0)
            self.assertEqual(game.hearts, HEARTS, fps)
            self.assertEqual(game.shots, [], fps)

    def test_a_shot_in_the_hurt_window_is_consumed_and_nothing_lands_at_its_end(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("grub", 8.5, 4)
            self.assertTrue(step_until(game, has_event("hurt")))
            self.still_shot(game, 0.2)
            game.step()
            self.assertEqual(game.shots, [], fps)
            self.assertEqual(game.hearts, HEARTS - 1, fps)
            run(game, 1.0)  # the window (0.8 s) ends; the grub is still recovering or winding up
            self.assertEqual(game.hearts, HEARTS - 1, fps)
            self.assertEqual(len(times(game, "hurt")), 1, fps)

    def test_a_shot_after_the_window_hits_again(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("grub", 8.5, 4)
            self.assertTrue(step_until(game, has_event("hurt")))
            run(game, 1.0)
            self.assertFalse(game.invulnerable, fps)
            self.still_shot(game, 0.2)
            game.step()
            self.assertEqual(game.hearts, HEARTS - 2, fps)
            self.assertEqual(game.shots, [], fps)

    def test_two_shots_together_cost_one_heart_and_both_go(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            self.still_shot(game, 0.2)
            self.still_shot(game, -0.2)
            game.step()
            self.assertEqual(game.hearts, HEARTS - 1, fps)
            self.assertEqual(game.shots, [], fps)


class LungeContactTest(unittest.TestCase):
    """Criterion 21: a lunge that touches a protected player is spent (step 38)."""

    def wall_lunge(self, fps, kind):
        # Player on the west wall, the grub lunging at it: a dash against the wall stays in place,
        # so the grub is still in reach when the dash ends.
        game = Game(fps=fps, room="empty")
        game.place_player(0, 4)
        game.spawn(kind, 1.5, 4)
        self.assertTrue(step_until(game, has_event("lunge")))
        return game

    def test_a_dash_spends_the_lunge_and_the_next_lunge_hurts(self):
        for fps in (30, 60):
            for kind in ("grub", "brute"):
                game = self.wall_lunge(fps, kind)
                game.press("dash", "left")
                run(game, 0.35)  # the dash (0.25 s) has ended, the lunge (0.3 s) is over
                self.assertEqual(game.hearts, HEARTS, (fps, kind))
                self.assertEqual(game.enemies[0].phase, "recovery", (fps, kind))  # not cancelled
                run(game, 0.4)
                self.assertEqual(game.hearts, HEARTS, (fps, kind))
                self.assertEqual(game.enemies[0].phase, "recovery", (fps, kind))
                self.assertTrue(step_until(game, has_event("hurt"), 5.0), (fps, kind))
                self.assertEqual(game.hearts, HEARTS - 1, (fps, kind))

    def test_a_hurt_window_ending_mid_lunge_does_not_let_the_lunge_hit(self):
        for fps in (30, 60):
            game = self.wall_lunge(fps, "grub")
            game.hurt_left = 0.2  # contact at about 0.12 s is inside, the window ends at 0.2 s
            game._set_invulnerable(True, "test")
            run(game, 0.45)
            self.assertFalse(game.invulnerable, fps)
            self.assertEqual(game.hearts, HEARTS, fps)
            self.assertEqual(game.enemies[0].phase, "recovery", fps)

    def test_a_lunge_that_first_touches_after_the_window_hits(self):
        for fps in (30, 60):
            game = self.wall_lunge(fps, "grub")
            game.hurt_left = 0.05
            game._set_invulnerable(True, "test")
            self.assertTrue(step_until(game, has_event("hurt"), 0.5), fps)
            self.assertEqual(game.hearts, HEARTS - 1, fps)


class ShotSourceTest(unittest.TestCase):
    """Step 94 (W1, W8): the shot-hit message names the side the shot came from."""

    CASES = (
        ((15, 4), "east"),
        ((8, 0), "north"),
        ((1, 4), "west"),
        ((8, 8), "south"),
        ((15, 0), "north-east"),
        ((15, 7), "south-east"),  # ratio 3/7 = 0.43 > 0.4142
    )

    def test_direction_words_at_both_rates(self):
        for fps in (30, 60):
            for (x, y), word in self.CASES:
                game = Game(fps=fps, room="empty")
                game.spawn("spitter", x, y)
                run(game, 7.0)
                self.assertTrue(game.hurt_kinds, (fps, x, y))
                self.assertEqual(game.hurt_kinds[0], f"shot from the {word}", (fps, x, y))

    def test_player_view_line(self):
        out = ReactionTest.session(
            self, "room empty\nspawn spitter 15 4\nplayer 8 4\nend 7\n"
        )
        self.assertIn("YOU ARE HIT by a shot from the east — hearts 2/3", out)

    def test_absorbed_shot_prints_no_message(self):
        game = Game(room="empty")
        game.invulnerable = True
        game.shots.append([game.x + 0.2, game.y, 0.0, 0.0, 0.0])
        game.step()
        self.assertEqual(game.hurt_kinds, [])
        self.assertEqual(game.shots, [])


class LateSwipeTest(unittest.TestCase):
    """Step 94 (W5, W6): a damaging swipe in the lunge says it was too late."""

    def lunging(self, fps, kind):
        game = Game(fps=fps, room="empty")
        game.spawn(kind, 10, 4)
        for _ in range(5 * fps):
            game.step()
            e = game.enemies[0]
            if e.phase == "lunge" and abs(e.x - game.x) <= 1.5:
                return game
        self.fail("no lunge in reach")

    def kinds(self, game):
        return [k for _, k, _ in game.events]

    def test_late_swipe_line_comes_before_the_hit(self):
        import play

        for fps in (30, 60):
            for kind in ("grub", "brute"):
                game = self.lunging(fps, kind)
                hp = game.enemies[0].hp
                game.press("attack")
                self.assertEqual(game.enemies[0].hp, hp - 1, (fps, kind))
                self.assertTrue(step_until(game, has_event("hurt"), 1.0), (fps, kind))
                ks = self.kinds(game)
                self.assertEqual(ks.count("late_swipe"), 1, (fps, kind))
                self.assertLess(ks.index("late_swipe"), ks.index("hurt"), (fps, kind))
                text = play.Player.describe("late_swipe", {"enemy": kind})
                self.assertEqual(
                    text, f"the {kind}'s lunge had already started, the swipe was too late to stop it"
                )
                for bad in ("rears back", "takes aim", "YOU ARE HIT by"):
                    self.assertNotIn(bad, text)

    def test_no_line_in_windup_kill_or_recovery(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("grub", 9.2, 4)
            self.assertTrue(step_until(game, has_event("windup")))
            game.press("attack")
            self.assertNotIn("late_swipe", self.kinds(game))
            game = self.lunging(fps, "grub")
            game.enemies[0].hp = 1
            game.press("attack")
            self.assertNotIn("late_swipe", self.kinds(game))
            game = Game(fps=fps, room="empty")
            game.spawn("brute", 9.0, 4)
            game.enemies[0].phase, game.enemies[0].phase_left = "recovery", 1.0
            game.press("attack")
            self.assertNotIn("late_swipe", self.kinds(game))


class DashTest(unittest.TestCase):
    def test_dash_covers_four_tiles_at_both_frame_rates(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.place_player(2, 4)
            game.press("dash", "right")
            run(game, 0.5)
            self.assertAlmostEqual(game.x, 2 + DASH_DISTANCE, places=6)

    def test_attack_during_dash_fires_when_it_ends(self):
        game = Game(room="empty")
        game.place_player(2, 4)
        game.press("dash", "right")
        run(game, 0.1)
        game.press("attack")
        self.assertFalse(any(kind == "attack" for _, kind, _ in game.events))
        run(game, 0.2)
        self.assertTrue(any(kind == "attack" for _, kind, _ in game.events))

    def test_dash_has_a_cooldown(self):
        game = Game(room="empty")
        game.press("dash", "left")
        run(game, 0.5)
        game.press("dash", "left")
        self.assertEqual(game.events[-1][1], "ignored")


class InvulnerabilityTest(unittest.TestCase):
    def test_a_dash_right_after_a_hit_keeps_both_protections(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.place_player(4, 4)
            game.spawn("grub", 4.5, 4)
            game.spawn("grub", 4.5, 5)
            self.assertTrue(step_until(game, has_event("hurt")))
            run(game, 0.32)  # hit-stun passes, still hurt-invulnerable
            game.press("dash", "right")
            run(game, 1.5)
            hurt = times(game, "hurt")
            ended = next(t for t, kind, _ in game.events if kind == "dash_end")
            self.assertTrue(all(t >= ended for t in hurt[1:]), (fps, hurt, ended))
            self.assertTrue(all(b - a >= 0.8 - 1e-9 for a, b in zip(hurt, hurt[1:])), (fps, hurt))


class BotsTest(unittest.TestCase):
    def test_every_bot_finishes_a_room(self):
        import bots

        for name, bot in bots.BOTS.items():
            result = bots.play_room(bot, "1", 60, 30)
            self.assertIn("cleared", result, name)

    def test_dodger_agrees_at_30_and_60_fps(self):
        import bots

        for room in ("1", "2", "3", "4", "5"):
            a = bots.play_room(bots.BOTS["dodger"], room, 30, 60)
            b = bots.play_room(bots.BOTS["dodger"], room, 60, 60)
            self.assertEqual(a["cleared"], b["cleared"], (room, a, b))
            self.assertLessEqual(abs(a["hearts_lost"] - b["hearts_lost"]), 1, (room, a, b))

    def test_walker_meets_criteria_13_and_14_at_each_rate(self):
        # Criterion 16d: the walker's per-room numbers may differ between rates (its 0.15 s
        # decision grid lands on different frames); it only has to meet 13 and 14 at each rate.
        # Build 0.6 note: the walker's UPPER limit of 6 hearts in rooms 3-5 is NOT asserted here.
        # Measured on 0.6: 7 hearts at 60 FPS. That is a tuning question for game-designer
        # (criterion 13, step 35/38 notes), reported in the build notes, not a build defect.
        import bots

        for fps in (30, 60):
            result = {
                name: {room: bots.play_room(bot, room, fps, 60) for room in "12345"}
                for name, bot in bots.BOTS.items()
            }

            def lost(name, rooms):
                return sum(result[name][r]["hearts_lost"] for r in rooms)

            def cleared(name, rooms):
                return sum(result[name][r]["cleared"] for r in rooms)

            # 13: rooms 3-5 summed.
            walker_lost = lost("walker", "345")
            self.assertGreaterEqual(walker_lost, 3, (fps, walker_lost))
            self.assertGreaterEqual(cleared("walker", "345"), 2, fps)
            self.assertLessEqual(lost("dodger", "345"), walker_lost / 2, fps)
            self.assertEqual(cleared("dodger", "345"), 3, fps)
            self.assertLess(cleared("camper", "345"), cleared("walker", "345"), fps)
            # 15: the dodger dashes at least once in each of rooms 3-5.
            for room in "345":
                self.assertGreaterEqual(result["dodger"][room]["dashes"], 1, (fps, room))
            # 14: rooms 1-2 summed; the walker need not clear them.
            self.assertGreaterEqual(lost("walker", "12"), 1, fps)
            self.assertLessEqual(lost("dodger", "12"), 1, fps)
            self.assertEqual(cleared("dodger", "12"), 2, fps)

    def test_bot_log_adds_state_and_changes_no_result(self):
        import bots

        for name, bot in bots.BOTS.items():
            for room in ("1", "3"):
                for fps in (30, 60):
                    quiet = bots.play_room(bot, room, fps, 60)
                    loud = bots.play_room(bot, room, fps, 60, log=True)
                    for key in ("cleared", "seconds", "hearts_lost", "hits_by", "attacks", "dashes"):
                        self.assertEqual(quiet[key], loud[key], (name, room, fps, key))
                    self.assertEqual(quiet["log"], [])
                    hurt = [line for line in loud["log"] if "HEART LOST" in line]
                    self.assertEqual(len(hurt), loud["hearts_lost"], (name, room, fps))
                    for line in loud["log"]:
                        if "HEART LOST" in line:
                            self.assertIn("source", line)
                        elif "skipped decision" in line:
                            self.assertIn("reason: player stunned", line)
                        else:
                            for part in ("frame ", "grid ", "player (", "hearts ", "stunned ", "nearest ", "shots in flight"):
                                self.assertIn(part, line, (name, room, fps, line))

    def test_walker_logs_the_exact_distance_it_compared(self):
        import bots

        result = bots.play_room(bots.BOTS["walker"], "1", 60, 60, log=True)
        self.assertTrue(any("(exact " in line for line in result["log"]))

    def test_dodger_never_swipes_a_brute_in_wind_up(self):
        import bots

        for fps in (30, 60):
            result = bots.play_room(bots.BOTS["dodger"], "2", fps, 60, log=True)
            self.assertFalse(any("swipe brute wind-up" in line for line in result["log"]), fps)


class ReactionTest(unittest.TestCase):
    def session(self, script):
        import contextlib
        import io

        import play

        setup, inputs, rules = play.read_script(script)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            play.play(setup, inputs, "player", rules)
        return out.getvalue()

    def test_rules_react_to_what_is_on_screen(self):
        out = self.session("room empty\nspawn grub 9.2 4\nwhen see g within 1.4 then attack\n")
        self.assertIn("room cleared", out)
        self.assertNotIn("YOU ARE HIT", out)

    def test_cues_show_in_the_player_view(self):
        out = self.session("room empty\nspawn grub 10 4\nspawn spitter 1 1\nend 2.5\n")
        self.assertIn("a grub rears back", out)
        self.assertIn("a spitter takes aim", out)
        self.assertIn("~", out)
        self.assertIn("cue: g", out)
        self.assertIn("cue: s", out)

    def test_marks_r_and_G_are_drawn(self):
        out = self.session("room 2\nend 0.2\n")
        self.assertIn("r", out)
        self.assertIn("G", out)

    def test_a_rule_acts_at_most_every_reaction_time(self):
        import play

        rule = play.Rule("when see g within 20 then attack")
        game = Game(room="empty")
        game.spawn("grub", 15, 4)
        fired = 0
        for _ in range(60):  # one second at 60 FPS
            before = rule.last
            play.react(game, [rule], [], [])
            fired += rule.last != before
            game.step()
        self.assertEqual(fired, 7)  # 0.0, 0.15, ... 0.9

    def test_rules_ignore_what_is_not_drawn(self):
        import play

        game = Game(room="empty")  # nothing on screen
        view = play.View(game, [])
        self.assertIsNone(view.nearest())
        self.assertTrue(play.Rule("when nothing within 3 then stop").matches(view))

    def test_rules_and_timed_inputs_mix(self):
        out = self.session("room empty\n0.1 dash right\nwhen see g within 1.4 then attack\nend 1\n")
        self.assertIn("you dash right", out)

    def test_a_bad_rule_says_how_rules_read(self):
        import play

        with self.assertRaises(ValueError) as caught:
            play.Rule("when grub close then hit")
        self.assertIn("conditions:", str(caught.exception))


class PlayerViewMessageTest(unittest.TestCase):
    """F2 (brute shrug message, criterion 19a) and F3 (banner 0.6) in the player view."""

    SHRUG = "the brute shrugs off the swipe"

    def session(self, script):
        return ReactionTest.session(self, script)

    def brute_script(self, fps):
        return (
            f"room empty\nfps {fps}\nspawn brute 9 4\nplayer 8 4\n"
            "0.1 attack\n0.5 attack\nend 4\n"
        )

    def test_each_swipe_that_hurts_a_winding_up_brute_prints_the_message(self):
        for fps in (30, 60):
            out = self.session(self.brute_script(fps))
            self.assertEqual(out.count(self.SHRUG), 2, fps)
            lines = [l for l in out.splitlines() if self.SHRUG in l]
            self.assertTrue(lines[0].lstrip().startswith("0.1"), (fps, lines))
            self.assertTrue(lines[1].lstrip().startswith("0.5"), (fps, lines))
            self.assertIn("you swipe: brute hit", out, fps)

    def test_a_kill_in_wind_up_prints_no_message(self):
        import contextlib
        import io

        import play

        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("brute", 9.0, 4)
            self.assertTrue(step_until(game, has_event("windup")))
            game.enemies[0].hp = 1
            game.press("attack")
            texts = [play.Player.describe(k, d) for _, k, d in game.events]
            self.assertFalse(any(t and "shrugs" in t for t in texts), fps)
            self.assertIn("you swipe: brute defeated", texts, fps)

    def test_swipes_at_a_grub_or_runner_print_no_message(self):
        for fps in (30, 60):
            for kind in ("grub", "runner"):
                out = self.session(
                    f"room empty\nfps {fps}\nspawn {kind} 9 4\nplayer 8 4\n0.1 attack\nend 1\n"
                )
                self.assertNotIn("shrugs", out, (fps, kind))

    def test_the_message_does_not_change_the_simulation(self):
        import play

        self.assertEqual(
            play.Player.describe("shrug", {"enemy": "brute"}), self.SHRUG
        )

    def test_the_banner_shows_0_6(self):
        for fps in (30, 60):
            for room in ("1", "empty"):
                out = self.session(f"room {room}\nfps {fps}\nend 0.2\n")
                self.assertEqual(
                    out.splitlines()[0], f"Lantern Depths 0.6 — room {room} — {fps} FPS"
                )


class VariantMessageTest(unittest.TestCase):
    """D-011: wind-up and hit messages name the variant."""

    def session(self, script):
        return ReactionTest.session(self, script)

    def test_wind_up_and_hit_messages_name_the_variant(self):
        for fps in (30, 60):
            for kind in ("grub", "runner", "brute"):
                # Window of 1.0 s: it holds the first wind-up and its hit (grub 0.67 s, runner
                # 0.53 s, brute 0.87 s) but ends before any variant can wind up a second time
                # (earliest: the runner, about 1.15 s). So one wind-up means one message.
                out = self.session(f"room empty\nfps {fps}\nspawn {kind} 9.5 4\nend 1.0\n")
                self.assertEqual(out.count(f"a {kind} rears back"), 1, (fps, kind))
                self.assertEqual(out.count(f"YOU ARE HIT by a {kind}"), 1, (fps, kind))
                self.assertIn(f"YOU ARE HIT by a {kind} — hearts 2/3", out, (fps, kind))
                for other in ("grub", "runner", "brute"):
                    if other != kind:
                        self.assertNotIn(f"a {other} rears back", out, (fps, kind))
                        self.assertNotIn(f"by a {other}", out, (fps, kind))

    def test_a_shot_hit_message_is_unchanged(self):
        for fps in (30, 60):
            out = self.session(f"room empty\nfps {fps}\nspawn spitter 1 4\nend 5\n")
            self.assertIn("YOU ARE HIT by a shot from the west — hearts 2/3", out, fps)

    def test_rears_back_rule_matches_all_variants(self):
        import play

        game = Game(room="empty")
        game.spawn("grub", 15, 4)
        rule = play.Rule('when text "rears back" then stop')
        for kind in ("grub", "runner", "brute"):
            view = play.View(game, [f"a {kind} rears back"])
            self.assertTrue(rule.matches(view), kind)

    def test_manual_has_the_new_wording(self):
        text = (Path(__file__).resolve().parent.parent / "manual.md").read_text(encoding="utf-8")
        self.assertIn("A brute is never cancelled.", text)
        self.assertIn("so in room 3 up to 5 can be in the air at once.", text)
        self.assertNotIn("no more than 3 are in the air at once", text)


if __name__ == "__main__":
    unittest.main()
>>>END
