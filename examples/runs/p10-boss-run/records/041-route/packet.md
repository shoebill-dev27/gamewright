# Studio operation packet

operation: Route
goal: G-002
step_artifacts: goals/G-002-final-boss/32-gameplay-engineer-to-studio.md
next_seq: 33
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha c2361b0c0b0e; run through the project's run commands)
log: last 5 of 18 entries in @log-recent; the full history is goals/G-002-final-boss/log.md

## You may write

- goals/G-002-final-boss/goal.md
- goals/G-002-final-boss/32-gameplay-engineer-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- project.md: only in the Route that closes the Goal, and only its ## Current state (at most 1,500 characters)
- goals/G-002-final-boss/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 33
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
goals/G-002-final-boss/25-studio-to-gameplay-engineer.md
goals/G-002-final-boss/26-gameplay-engineer-to-studio.md
goals/G-002-final-boss/27-studio-to-gameplay-engineer.md
goals/G-002-final-boss/28-gameplay-engineer-to-studio.md
goals/G-002-final-boss/29-studio-to-gameplay-engineer.md
goals/G-002-final-boss/30-gameplay-engineer-to-studio.md
goals/G-002-final-boss/31-studio-to-gameplay-engineer.md
goals/G-002-final-boss/32-gameplay-engineer-to-studio.md
goals/G-002-final-boss/goal.md
goals/G-002-final-boss/log.md
project.md
repo/README.md
repo/bots.py
repo/game.py
repo/manual.md
repo/play.py
repo/public-driver.md
repo/run_driver.py
repo/session.py
repo/tests/test_boss.py
repo/tests/test_game.py
repo/tests/test_run_driver.py
repo/tests/test_session.py
repo/tests/test_terminal.py
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
- Diagnose：done。既存基盤の不足と計画上の回帰対応を整理済み。24に変更前のtests基線（69 tests、OK）が報告されている。
- Decide：done。D-015〜D-019で範囲・体験方向・仕様契約・旧基準の適用関係を確定。
- Design：done。design/final-boss-and-continuous-run.mdとD-017・D-019が正本。24では実装変更なし。変更後の検証は未実施。
- Plan：done。16・20の計画と回帰対応を使用する。D-021と衝突する実機ホスト・実機供給・外部配員・見積もり取得の要求は適用しない。
- Decide（供給・承認）：done。22へのOwner回答をD-021に記録。Ownerは実行経路とStudio内検証を指定し、Build開始を承認。実機供給、指定sha照合、人日見積もりは不要。
- Plan補完：skipped。新しいOwner条件を後続Stepへ直接渡せるため、同じ供給質問で再発行しない。具体的な技術上の不成立が判明した場合に限り戻す。
- Build：open。30でRunSessionと境界fixtureの8試験を保存成果として報告。供給された89 tests成功記録は保存後の全成果の検証ではない。公開driverはSession未接続で、入力・表示・対応bot・説明・不足試験・通常ラン測定が残る。31で保存版の試験から再開する。新しい仕様質問・供給不足・承認待ちはない。
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
| 6 | Build | gameplay-engineer | implement-change | done | 23-studio-to-gameplay-engineer.md → 結果: 24-gameplay-engineer-to-studio.md |
| 6a | Build | gameplay-engineer | implement-change | done | 25-studio-to-gameplay-engineer.md → 結果: 26-gameplay-engineer-to-studio.md |
| 6b | Build | gameplay-engineer | implement-change | done | 27-studio-to-gameplay-engineer.md → 結果: 28-gameplay-engineer-to-studio.md |
| 6c | Build | gameplay-engineer | implement-change | done | 29-studio-to-gameplay-engineer.md → 結果: 30-gameplay-engineer-to-studio.md |
| 6d | Build | gameplay-engineer | implement-change | open | 31-studio-to-gameplay-engineer.md |
| 7 | Verify | qa | verify-change | planned | — |
| 8 | Verify | art-director | visual-review | planned | — |
| 9 | Play | playtester | playtest-session | planned | — |
| 9a | Design | game-designer | make-decision, write-design-spec | planned | — |
| 10 | Review | game-director | review-outcome | planned | — |
| 11 | Next | studio | — | planned | — |

逐次実行する。Build後は独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewとする。明白な対処不能・到達不能が判明した場合はDesigner判断を前倒しする。並列Stepは開かない。

## Route changes

30のSession部分成果で29のStepを完了扱いとし、31で公開経路の統合Buildを継続する。供給された試験成功記録と保存後の検証を区別し、独立QA投入は保留する。新しい仕様質問・承認事項はなく、同じ欠落入力の再照会ではない。後続の独立検証順序を維持する。

## Next action

Gameplay Engineerが31-studio-to-gameplay-engineer.mdから統合Buildを継続する。保存版の試験を実行し、公開driver・表示・対応bot・説明・不足試験と実測を完成する。変更内容、基準対応、実行結果、測定条件と値、独立検証手順をstudioへ返す。実装完了後のRouteで独立QAを開く。

## Outcome

未完了。30でSession基盤と境界試験が報告されたが、公開経路の連続ラン統合、表示、対応bot、不足試験、説明更新、通常ラン測定が残る。供給された89 tests成功記録は保存後の全成果の検証ではない。最終戦の手応えと通常ランの所要時間は未確認。D-021の承認内で31のBuildを継続する。追加金銭支出と実機調達は行わない。独立QA以降は未実施。Goalはactiveのまま閉じず、project.mdは変更しない。
>>>END

<<<FILE @log-recent
## 029-resume · 2026-10-20

Status: active. Open: 23-studio-to-gameplay-engineer.md.

22へのOwner回答をD-021として記録し、Escalationをresolved、Goalをactiveへ戻した。実機・外部供給・見積もり要求を今回の開始条件から外し、Plan再発行をskipped、23のBuildをopenとした。後続の独立検証・実測後判断を維持する。

## 031-route · 2026-10-20

Status: active. Open: 25-studio-to-gameplay-engineer.md.

24のBuild Stepをquestionで完了扱いとした。変更前69 tests成功と実装未着手を分離し、今回供給されたソース全文を明示ロードする25の継続Buildを開く。新しい供給情報があるため同一質問の反復には当たらず、Owner再承認・Plan再発行は不要。後続の独立検証順序を維持する。

## 035-route · 2026-10-20

Status: active. Open: 27-studio-to-gameplay-engineer.md.

26のBuild Stepを部分成果で完了扱いとし、27で残りのBuildを継続する。終端基盤と72 tests成功の報告を全機能完了から区別し、独立QA投入は保留する。新しい仕様質問や承認事項はなく、既存計画の実装順と後続の独立検証順序を維持する。

## 037-route · 2026-10-20

Status: active. Open: 29-studio-to-gameplay-engineer.md.

28の部分成果で27のStepを完了扱いとし、29で統合Buildを継続する。保存版未実行とRound 1の失敗記録を区別し、独立QA投入は保留する。新しい仕様質問や承認事項はなく、既存計画と後続の独立検証順序を維持する。

## 039-route · 2026-10-20

Status: active. Open: 31-studio-to-gameplay-engineer.md.

30のSession部分成果で29のStepを完了扱いとし、31で公開経路の統合Buildを継続する。供給された試験成功記録と保存後の検証を区別し、独立QA投入は保留する。新しい仕様質問・承認事項はなく、同じ欠落入力の再照会ではない。後続の独立検証順序を維持する。
>>>END

<<<FILE goals/G-002-final-boss/32-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-002
seq: 32
from: gameplay-engineer
to: studio
stage: Build
outcome: question
---
# 32: gameplay-engineer → studio — 公開Session経路を保存、統合検証と測定は未完了

## Task

公開Session driverと接続変更を保存し、Gameplay Engineerの継続Buildへ戻す。全成果の実行確認、対応bot、通常ラン測定が揃うまで独立QAへ投入しない。

## Context

31はSession基盤を公開parser・driver・player／traceへ接続し、対応botと不足試験、説明、同一試行実測まで完成する要求である。D-021の開始許可は有効。今回のパケットでは実行round残数が0であり、供給済み結果以外の実行証拠は取得していない。

## Findings

### 今回の変更ファイル

- `repo/run_driver.py`：新規保存。Plan16のmode、attempt、control、limit、driver-limit、trace-everyを解析し、RunSessionまたは独立診断RoomSessionへ接続する。停止しないdriver時刻、制御先行、同時刻記載順、試行別入力、入場時反応記憶初期化を実装する。
- `repo/play.py`：新構文の公開dispatchとボス予兆経路の描画を追加。旧構文は既存経路を保持する。
- `repo/game.py`：hurtイベントへ既存の被弾名を追加し、新driverでも短射・spitterの方向文言を保持する。
- `repo/tests/test_run_driver.py`：7試験を新規保存。実行していない。
- `repo/public-driver.md`：新構文、時計、再現例、表示範囲、未完成事項を記載。

パケットで「proposed … not written」とされた全文は保存済み成果と扱わず、今回出力したファイル／編集だけを保存対象とする。提案版の9試験をそのまま採用したという報告ではない。

### 実装前に照合した可視挙動

| 挙動 | 正本 |
|---|---|
| 通常ランは第1部屋から開始、診断setupとの併用を拒否 | 仕様§2、Plan16公開構文 |
| driver時計でpause／resume／retryを制御 | 仕様§4〜5、Plan16 |
| 同時刻は記載順、制御→時刻入力→反応 | 仕様§5、Plan16 |
| 境界・pause中の期限入力を破棄 | 仕様§2、§5 |
| 入場で反応時刻・盤面・メッセージ記憶を初期化 | 仕様§2 |
| 両時計、ボスHP・攻撃名・予兆寸法・回復・活動弾数を表示 | 仕様§6 |
| 長時間limitを勝敗と別に報告 | 仕様§5、C3 |

新しい戦闘入力、ボスcheckpoint、時間合わせのHP・待機は追加していない。

### 基準対応と未達

| 対象 | 今回の対応 | 残作業 |
|---|---|---|
| R1 | 通常ラン公開起動経路 | 正規撃破による1→5到達の実行証拠 |
| R2・共有回帰 | 第1〜4部屋と既存パラメータを変更しない | 全保存版suite実行、保持基準の不足追跡 |
| R3〜R5、C1 | Session接続、境界入力試験、入場時反応記憶初期化 | 実行確認、反応記憶の専用試験、公開表示対照 |
| B1〜B10 | ボス予兆線と表示を公開経路へ接続 | 30の残作業表にある全不足試験と実行 |
| T1〜T4 | 終端待機とdriver制御retry、旧試行未来入力の除外処理 | 実勝利・実死亡からのretry、凍結、反応記憶破棄の試験 |
| C2 | driver時刻resume、pause中入力破棄の試験 | 予兆・保護・境界を含む実行確認。headless時計を実時間2秒と呼ばない |
| C3 | limitとoutcomeを別字段に表示 | 勝利・死亡同フレームlimitの統合試験 |
| V1 | 公開player情報・メッセージ・即時表示、毎tick trace選択 | 全契機対照、弾ID、全消去理由、イベントbuild字段、長時間メモリ評価 |
| D-019 | 独立1〜4の既存bot方針を維持 | ボス対応dodger、開始3／2 hearts別FPS比較、独立3・4全bot報告 |
| 文書 | public-driver.mdを追加 | manual／READMEへの統合更新 |
| V2 | D-021の今回対象外 | 実機対応検証済みとはしない |

旧assertの保持／終了／置換は仕様§8、Plan16・20、30を維持する。旧13集計を復活させず、独立1〜2比較、3・4のdash、独立1〜4のFPS比較を保持する。今回botsおよび既存assertの追加変更はない。

### 実行対象・コマンド・実結果

パケット供給の@run-results：

| Round | コマンド | 供給結果 |
|---|---|---|
| 1 | `python3 -m unittest discover -s tests` | Exit 0、89 tests、0.169秒、OK |
| 2 | 同上 | Exit 0、95 tests、0.188秒、OK |
| 3 | 同上 | Exit 0、98 tests、0.192秒、OK |

今回出力版は実行していない。上記98件へ今回7試験を加えて成功件数を推定・認定しない。trace、bots、通常ランの実結果は供給されていない。build識別は今回の公開driverで`0.6-g002-public-32`とするが、供給済み結果をこの識別へ帰属させない。

### 再現手順

次の継続Buildでは保存後の`repo/`を対象に実行する。

1. `python3 -m unittest discover -s tests`で既存試験と新7試験を確認する。
2. `public-driver.md`のpause例をscriptへ保存し、`python3 play.py --view player SCRIPT`と`python3 play.py --view trace SCRIPT`を実行する。両FPSで制御時刻、拒否入力、凍結時計を対照する。
3. 同文書の独立5番例を両FPSで実行し、warning／active／recoveryと予兆線、活動弾数を対照する。
4. 実終端retry・旧未来入力破棄、反応記憶、limit同フレーム結果の不足試験を追加する。
5. ボス対応dodgerを公開観測に基づいて実装し、独立5番開始3／2 heartsを同一limit・同一方針で比較する。独立3・4は全bot×両FPSを報告する。
6. 正規敵撃破による同一試行の通常ランを記録する。部屋別時間、1秒遷移、ボス入場hearts、被弾、回復中反撃、終端、retry、pause、処理実時間を対応付ける。

### 測定条件と値

新測定値なし。独立部屋合算、境界fixture、供給されたsuite処理時間を通常ラン時間へ転用しない。明白な攻略不能・到達不能を示す測定証拠もない。

### Sender assessment

31の統合Build完成要求は未達である。今回は未保存提案を含むパケットから、公開driver接続を具体的な保存成果へ進めた部分成果である。

実行round枯渇は保存後検証・測定の阻害要因である。対応bot、受け入れ試験の不足、観測・文書の未完成は実装残作業であり、round枯渇だけが未完了原因ではない。自己承認および独立QAへの投入要求は行わない。

既存scriptを旧経路へ残すため、新表示契約は新構文経路に限定されている。全経路の契約整理、短射の発射フレームと寿命・回復時刻の対照、イベント蓄積の長時間評価を継続Buildで確認する必要がある。

## Decisions already made

- D-017：二攻撃ボス、境界回復、死亡優先、先頭retry、両時計・表示契約。
- D-019：旧集計の適用終了、共有回帰保持、対応botのhearts別FPS比較、実測後Designer判断。
- D-021：現状repo/とStudio内テキスト実行で進める。実機・sha・費用承認を再取得しない。

## Constraints

第1〜4部屋と共有戦闘規則を保持する。新戦闘入力、ボスcheckpoint、時間合わせのHP・待機、購入・外部委託・追加金銭を追加しない。

未実行を成功と扱わず、fixtureを通常到達証拠にしない。独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewを維持する。

## Open questions

新しい仕様質問・開始承認待ちはない。保存後検証と比較・通常ラン測定を実施できる実行roundが必要である。実装残作業は本Findingsの基準表に残す。

## Expected output

Studioは今回の部分成果を保存し、実行可能な継続BuildをGameplay Engineerへルーティングする。全保存版の試験、観測不足、ボス対応bot、文書統合、同一試行実測を完成してstudioへ返す。全成果が揃うまで独立QAへ投入しない。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#vision
- Project: project.md#constraints
- Project: repo/game.py
- Project: repo/session.py
- Project: repo/play.py
- Project: repo/run_driver.py
- Project: repo/bots.py
- Project: repo/manual.md
- Project: repo/README.md
- Project: repo/public-driver.md
- Project: repo/tests/test_game.py
- Project: repo/tests/test_terminal.py
- Project: repo/tests/test_boss.py
- Project: repo/tests/test_session.py
- Project: repo/tests/test_run_driver.py
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-step-44-walker-limit.md
- Project: design/combat-step-46-room3-cap.md
- Project: design/combat-step68.md
- Project: design/combat-step72.md
- Project: design/combat-step94.md
- Plan: goals/G-002-final-boss/16-technical-director-to-studio.md
- Plan: goals/G-002-final-boss/20-technical-director-to-studio.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Previous handoff: goals/G-002-final-boss/31-studio-to-gameplay-engineer.md
>>>END
