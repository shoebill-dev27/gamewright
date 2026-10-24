# Studio operation packet

operation: Route
goal: G-002
step_artifacts: goals/G-002-final-boss/16-technical-director-to-studio.md
next_seq: 17
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha 27fe16268ac8; run through the project's run commands)
log: last 5 of 9 entries in @log-recent; the full history is goals/G-002-final-boss/log.md

## You may write

- goals/G-002-final-boss/goal.md
- goals/G-002-final-boss/16-technical-director-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- project.md: only in the Route that closes the Goal, and only its ## Current state (at most 1,500 characters)
- goals/G-002-final-boss/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 17
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

D-015により、連続ラン・部屋間継承・終端・再挑戦の新設を今回の範囲に含める。具体的なボスの仕組み、難度、数値基準、継承・終端の詳細は担当Roleが定める。第1〜4部屋の構成と既存の共有戦闘ルールを維持し、新しい戦闘入力、ボス専用チェックポイント、既存部屋の全面改修は対象外。15〜20分を満たすためだけの敵HP増加は含めない。承認範囲を超える規模・費用・リスクや既存Decisionとの衝突が判明した場合は、実装前にOwnerへ戻す。

## Unknowns

- Observe：既存の不具合報告ではないため skipped。実行による現状確認は未実施。
- Diagnose：done。静的調査では連続ラン・部屋間継承・最終勝利・専用リトライがない。指定shaとの一致、実行時の終端挙動、戦闘時間は未確認。調査の制限は04に記録。
- Decide：done。D-015でOwnerが連続ランと第5部屋の単体ボスを承認。D-016で読み取り・位置取り・回避後の反撃を中心とする方向と設計境界を確定。既存Decisionは存続し、旧第5部屋依存の基準への適用関係はDesignで整理する。
- Design：done。D-017とfinal-boss-and-continuous-run.mdで詳細契約、30/60 FPSの受け入れ基準、旧基準対応表を確定。未実装・未検証。
- Decide（既存Decisionとの整合）：done。D-018で旧集計を新構成の評価から分離する方向を確定。D-006自体の適用変更は未完了。
- Design補足：done。D-019と仕様§8・§10で旧集計の適用終了、保持する回帰、ボスdash検証、対応botのFPS比較条件、実測後のDesigner再判断を確定。過去G-001の判断・結果は保持する。
- Plan：open。確定仕様とD-019に基づき、進行・攻撃切替・表示・終端・時刻と入力の契約、共有コードへの影響、試験移行、対応bot、計測、工数と依存を確認する。指定shaと実行基線は未確認。承認超過の可能性は実装前に返す。
- Design（実測後）：planned。対応botの両FPS基線、独立QA・Play、通常ランの同一試行による到達・終端・時間実測を受け、Review前に追加数値ゲート・調整の要否を判断する。不要でも理由を記録する。明白な対処不能・到達不能はPlay前に戻す。
- Build：仕様と計画の確定後にゲーム変更が必要。
- Verify：Build後の独立QAが必要。30/60 FPS、連続到達・勝敗・再挑戦、共有戦闘ルールの回帰、実機入力経路を含む。Art Directorの限定表現確認をplannedに確定。player viewの二攻撃、予兆と実弾、回復、HP、終端・retryの識別を対象とする。
- Play：最終戦と到達体験の手応え、連続ランの所要時間を独立したプレイヤー観察で評価する。実装内容や期待結果は渡さない。
- Review：体験Goalの達成判断が必要。
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
| 5 | Plan | technical-director | technical-plan | open | 15-studio-to-technical-director.md |
| 6 | Build | gameplay-engineer | implement-change | planned | — |
| 7 | Verify | qa | verify-change | planned | — |
| 8 | Verify | art-director | visual-review | planned | — |
| 9 | Play | playtester | playtest-session | planned | — |
| 9a | Design | game-designer | make-decision, write-design-spec | planned | — |
| 10 | Review | game-director | review-outcome | planned | — |
| 11 | Next | studio | — | planned | — |

逐次実行する。D-019と仕様補足に基づくPlanを開く。Planの完了前にBuildを開かない。独立QA、Art Directorの限定Verify、独立Playの後、Designerが実測に基づく判断を記録してからReviewへ進む。初回基線やQAで明白な対処不能・到達不能が判明した場合はDesigner判断を前倒しする。現時点で並列Stepは開かない。

## Route changes

14でDesign補足を完了。D-019と仕様§8・§10による適用整理を受け、15でTechnical DirectorのPlanを開く。対応bot・両FPS基線・通常ラン同一試行計測を計画対象にし、Review前のDesigner実測後判断をplannedで追加。独立検証とPlayを維持し、Owner質問は開かない。

## Next action

Technical Directorが `15-studio-to-technical-director.md` を実行し、確定仕様・D-019に基づく実装、試験移行、対応botと計測の計画、工数・リスク、Designer再判断の依存をStudioへ返す。

## Outcome

未完了・進行中。D-015で範囲、D-016で体験方向、D-017で詳細契約、D-018・D-019で旧集計と新構成の適用関係を確定した。次は実装計画。実装、独立QA・限定Art確認・独立Play、Designerの実測後判断、Reviewは未実施。指定shaとの一致、実行成功、難度、所要時間について新しい証拠はない。現時点でOwnerへの新たな質問はなく、project.mdのCurrent stateは変更しない。
>>>END

<<<FILE @log-recent
## 009-resume · 2026-10-20

Status: active. Open: 07-studio-to-game-director.md.

Ownerの案A承認をD-015に記録し、06をresolved、Goalをactiveへ変更。連続ラン・第5部屋の単体ボス・ラン先頭からの再挑戦をInterpretationに明記し、07でGame Directorの方向Decisionを開く。その後はDesign→Plan→Build→Verify→Play→Reviewと進める。

## 011-route · 2026-10-20

Status: active. Open: 09-studio-to-game-designer.md.

08の方向確定をもってDecideを完了し、D-016に基づくDesignを09で開く。旧第5部屋依存の基準と既存Decisionの対応整理も設計成果に含める。Plan以降の順序を維持し、Art Director確認は設計結果待ちのtentativeとする。

## 015-route · 2026-10-20

Status: active. Open: 11-studio-to-game-director.md.

10で詳細Designを完了。D-006の旧集計との具体的な衝突が判明したため、D-016の再検討条件に従い11でGame DirectorのDecideを先に開く。必要なDesignerのDecision変更を条件付きで追加し、Plan以降を維持する。テキスト表示契約に基づきArt Directorの限定Verifyをplannedへ確定。

## 017-route · 2026-10-20

Status: active. Open: 13-studio-to-game-designer.md.

12で整合方向のDecideを完了。D-018はD-006自体を改訂しないため、条件付きのDesign補足を確定し13で開く。Designerが適用変更・関連比較・試験対応を確定した後にPlanへ進む。実測依存の再判断経路と後続の独立検証を維持し、現時点でOwner質問は開かない。

## 019-route · 2026-10-20

Status: active. Open: 15-studio-to-technical-director.md.

14でDesign補足を完了。D-019と仕様§8・§10による適用整理を受け、15でTechnical DirectorのPlanを開く。対応bot・両FPS基線・通常ラン同一試行計測を計画対象にし、Review前のDesigner実測後判断をplannedで追加。独立検証とPlayを維持し、Owner質問は開かない。
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
