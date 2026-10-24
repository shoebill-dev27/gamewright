# Studio operation packet

operation: Resume
goal: G-002
escalation: goals/G-002-final-boss/22-game-director-to-owner.md
next_seq: 23
next_decision: D-021
current_build: repo/ (sha 27fe16268ac8; run through the project's run commands)
log: last 5 of 13 entries in @log-recent; the full history is goals/G-002-final-boss/log.md

## You may write

- decisions/D-021-<slug>.md
- goals/G-002-final-boss/22-game-director-to-owner.md
- goals/G-002-final-boss/goal.md
- goals/G-002-final-boss/23-studio-to-<role>.md

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

<<<FILE studio/templates/decision.md
---
kind: decision
id: D-NNN
status: accepted        # proposed | accepted | superseded
decided_by: <role-id | owner>
goal: <G-NNN, or none>
date: YYYY-MM-DD
supersedes: <D-NNN, or none>
---
# D-NNN: <the decision in a few words>

## Decision

<What was decided, and its limits.>

## Rationale

<Why.>

## Alternatives considered

<Other options and why they were not chosen.>

## Revisit when

<What change in evidence or circumstances should reopen this.>
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
>>>END

<<<FILE goals/G-002-final-boss/goal.md
---
kind: goal
id: G-002
project: lantern-depths
status: blocked-on-owner
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
- Plan：16・20で計画と回帰対応を補完。回帰正本の読込み・試験対応はPlan上充足したが、実行合格ではない。指定sha・実行基線、実機供給・独立検証枠、費用承認は未確認。計画合計18〜33.5人日は暫定で、金銭費用・日程は未算定。D-020の五条件未充足につきBuild保留。
- Decide（実装開始条件）：done。D-020で最小実機ホストを既存要件の実現作業としてPlan対象に含める。費用・リスクの承認は未確定で、超過・供給不能も未確定。Buildは五条件の解決まで保留する。
- Plan補完：done。20で回帰対応、最小ホスト方式、未算入工数と必要供給物を整理。executorのツール取得経路が利用できず実行未着手。資源不存在・供給不能・承認超過は確定していない。
- Decide（供給・承認）：Owner回答待ち。22でGame DirectorのEscalation準備を完了。既存資源・承認根拠の確認責任者指定（A）、不足分の見積もり・調達条件取得（B）、条件整備まで停止（C）の一問をOwnerへ開いた。推奨はA。供給責任者・予算権限者と承認根拠は未確認で、同じ不足だけでPlanを再発行しない。選択のみを未確定費用やBuildの承認とは扱わない。
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
| 5 | Plan | technical-director | technical-plan | done | 15-studio-to-technical-director.md → 結果: 16-technical-director-to-studio.md（question・開始条件未充足） |
| 5a | Decide | game-director | make-decision, prepare-owner-escalation | done | 17-studio-to-game-director.md → 結果: 18-game-director-to-studio.md |
| 5b | Plan | technical-director | technical-plan | done | 19-studio-to-technical-director.md → 結果: 20-technical-director-to-studio.md |
| 5c | Decide | game-director | make-decision, prepare-owner-escalation | done | 21-studio-to-game-director.md → 結果: 22-game-director-to-owner.md |
| 5c-owner | Decide | owner | — | open | 22-game-director-to-owner.md |
| 5d | Plan | technical-director | technical-plan | tentative | Owner回答と新しい供給・承認資料の取得後、残条件を確認 |
| 6 | Build | gameplay-engineer | implement-change | planned | — |
| 7 | Verify | qa | verify-change | planned | — |
| 8 | Verify | art-director | visual-review | planned | — |
| 9 | Play | playtester | playtest-session | planned | — |
| 9a | Design | game-designer | make-decision, write-design-spec | planned | — |
| 10 | Review | game-director | review-outcome | planned | — |
| 11 | Next | studio | — | planned | — |

逐次実行する。22のOwner Escalationのみをopenとし、回答に依存するRoleのStepは開かない。回答待ちに継続できる独立作業はない。Owner回答をResumeでDecisionに記録した後、選択条件と新しい供給・承認資料に応じて再計画する。同じ資料だけでPlanを繰り返さず、必要なOwner判断とD-020の五条件が解決するまでBuildを保留する。独立QA、Art Directorの限定Verify、独立Play、Designerの実測後判断、Reviewの順序を維持する。初回基線やQAで明白な対処不能・到達不能が判明した場合はDesigner判断を前倒しする。並列Stepは開かない。

## Route changes

22でEscalation準備を完了し、供給責任者・承認根拠の不足についてOwnerへA／B／Cの一問を開いた。Goalをblocked-on-ownerとし、依存StepとBuildを保留する。新しい供給・承認資料を得るまでPlanを再発行せず、後続の独立検証順序を維持する。

## Next action

Ownerが `22-game-director-to-owner.md` にA／B／Cと条件を回答する。推奨はA（既存資源と承認根拠の確認責任者指定）。A／Bでは供給・検証枠・予算の回答権限者を役割で指定し、Bでは調査対象・担当・既存配員枠・停止条件、Cでは再開条件を添える。回答後にStudioがResumeでDecisionを記録して再計画する。未確定費用の承認やBuild開始とは扱わない。

## Outcome

未完了・Owner回答待ち。D-015〜D-020を維持し、回帰正本と試験対応の計画補完、および22の供給・費用条件に関するEscalation準備を完了した。OwnerにはA／B／Cの選択と条件を求め、既存資源と承認根拠の確認責任者を指定するAを推奨する。実行基線、実機・独立検証の供給、費用承認は未解決。計画合計は暫定18〜33.5人日で、金銭総額・日程は未算定、承認済みではない。実装、独立検証、Play、Designer実測後判断、Reviewは未実施。指定sha一致、実行成功、実機供給、難度、所要時間の新しい証拠はなく、資源不存在や承認超過とは断定しない。Goalはblocked-on-owner。回答待ちの独立作業はなく、Buildを含む依存作業を保留する。Goalは閉じず、project.mdのCurrent stateは変更しない。
>>>END

<<<FILE @log-recent
## 019-route · 2026-10-20

Status: active. Open: 15-studio-to-technical-director.md.

14でDesign補足を完了。D-019と仕様§8・§10による適用整理を受け、15でTechnical DirectorのPlanを開く。対応bot・両FPS基線・通常ラン同一試行計測を計画対象にし、Review前のDesigner実測後判断をplannedで追加。独立検証とPlayを維持し、Owner質問は開かない。

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
>>>END

<<<FILE goals/G-002-final-boss/22-game-director-to-owner.md
---
kind: escalation
goal: G-002
seq: 22
from: game-director
to: owner
status: open
decision: none
---
# 22: Owner判断依頼 — 現行仕様の継続に必要な供給・費用条件

## Question

連続ラン・第5部屋の単体ボス・先頭retryという現行仕様を継続するため、必要資源と既存費用承認の確認責任者を指定する案A、不足分の見積もり・調達条件の取得まで進める案B、供給・費用条件が整うまで停止する案Cのどれを選びますか。

## Why this needs the Owner

供給責任者、機器の利用権、独立検証の稼働枠、予算承認根拠は、ゲーム仕様やソースからRoleが生成できません。orchestration.mdの「Roleで生成できない情報・資材による停止」に該当します。費用・権限の承認もStudioの権限外です。

限定Plan補完は終了しました。実行経路の取得に至らず、指定shaとの一致、実行基線、実機供給は未確認です。これは当該executorの制約であり、プロジェクト資源の不存在や供給不能の証拠ではありません。予算不明も、承認内・承認超過のいずれとも扱いません。

D-015は範囲の承認であり、無制限の費用承認ではありません。D-020の五条件が揃うまでBuildは保留します。本書は判断準備であり、Owner承認取得済みとは扱いません。

## Options

### Option A — 既存資源と承認根拠の確認責任者を指定する

現行のゲーム体験と仕様を維持し、既存資源で継続できるかを確認します。Ownerには、次の回答権限を持つ担当・役割を指定していただきます。人物の個人情報や秘密情報は不要です。

| 必要物・回答内容 | 回答すべき権限者 |
|---|---|
| 読取・実行可能なcheckout、指定sha `27fe16268ac8`のgit情報、shell・Python3の実行経路と利用条件 | repository／実行基盤の管理権限者 |
| 対象desktop OS・表示環境、keyboard・実gamepad・ドライバー、利用期間、依存の利用・導入権限 | desktop／機器／依存利用の管理権限者 |
| 独立QA、限定Art Verify、独立Playの担当供給元・実機利用枠・独立性を保てる条件 | 配員・検証環境の供給権限者 |
| 既存承認の対象作業・配員枠・費用上限・適用条件を確認できる非秘密の資料 | 予算承認権限者。Ownerと異なる場合はその役割を指定 |

現時点の暫定計画は18〜33.5人日です。既存資源の無償利用も未確認で、金銭総額・日程は確約できません。担当を指定しても資源が揃う保証はなく、確認後に不足が判明するリスクがあります。購入・導入・実装に着手しないため、確認段階で停止できます。

選択後：Ownerの回答をStudioがResumeで記録し、指定先から新しい供給情報・承認資料を取得します。その資料を基にTechnical Directorが基線・見積もり・残条件を確認します。既存承認で費用・リスクを判断できなければ、具体的な追加承認をOwnerへ戻します。同じ資料だけでPlanを繰り返しません。

### Option B — 不足分の見積もり・調達条件の取得まで進める

現行仕様を維持し、Aの責任者指定に加えて、既存資源で不足する項目について価格・供給条件・権限付与条件を取得する準備を選びます。未見積もりの購入や実装費用を包括承認する案ではありません。

18〜33.5人日は暫定で、未知の環境対応により増える可能性があります。調達準備の追加工数、機器・ライセンス・外部検証等の料金、納期は未確定です。Ownerには調査担当、調査に使える既存配員枠、対象と停止条件を指定していただきます。追加有償調査が必要なら、その具体的な費用承認前に停止します。

見積もり取得後に継続を見送れますが、承認された調査工数は消化されます。供給時期や互換性が想定と合わず、再見積もりが必要になるリスクがあります。

選択後：StudioがResumeで調査条件を記録します。外部照会が必要なら、その対象・内容について明示的な指示を得てから進めます。Technical Directorが供給条件と更新見積もりを整理し、Game Directorが具体的な金額・上限・条件を伴う承認依頼をOwnerへ戻します。購入・依存導入・Buildは、この案の選択だけでは許可しません。

### Option C — 供給・費用条件が整うまで停止する

現行仕様と既存Decisionを保存し、Goalの進行を停止します。新たな実装費用は確約しませんが、既消化工数の精算は未確認のまま残ります。再開時には資源・互換性・見積もりの再確認が必要となり、再開調査の工数や待ち時間が生じ得ます。

成果を破棄しないため再開可能です。ただし、ボス戦の提供は進まず、完了時期も定まりません。

選択後：StudioがOwner判断を記録し、停止と再開条件を管理します。責任者指定、必要資源、承認根拠が新たに揃った時点でResumeし、Technical Directorの残条件確認へ戻します。範囲縮小を希望する場合は、Ownerが変更内容を明示した後、ResumeでInterpretationを扱い、Design／Planへ戻します。

## Studio recommendation

案Aを推奨します。まず供給と予算の回答権限者を指定し、既存資源・既存承認で継続できるかを確認してください。

これは供給情報の提出と責任者指定を求める推奨です。18〜33.5人日の費用承認、資源の供給確約、Build開始の推奨ではありません。

## Reasoning

D-015で選ばれた到達体験を維持しつつ、未確認の購入を約束せずに不足を絞れるためです。現状は供給不能も予算超過も確定しておらず、直ちに調達や範囲縮小を選ぶ根拠はありません。

暫定18〜33.5人日は、Build準備〜統合11.5〜20、独立QA 2〜3、限定Art 0.5〜1、独立Play 1〜2、Designer判断0.5〜1.5、修正・再検証2〜5、Review・引継ぎ0.5〜1の合計です。単価・通貨・税、機器・OS・ライセンス・外部担当料金、既消化分との精算、日程、未知の環境対応増分は未確定です。金銭総額や納期には換算できません。

既存資源の不足が確認され、限定した見積もり取得が可能なら案Bへ推奨を見直します。回答権限者・利用枠を確保できない、更新費用を受け入れられない場合は案Cを検討します。工数幅の増加、Owner DecisionやVisionの変更が必要になった場合も、実装前に再判断します。

どの継続案でも、Buildを開くにはD-020の五条件をすべて解決する必要があります。

1. 対象commit・指定shaとの関係、Python・依存、実行基線、版表記差と影響の記録。
2. 回帰正本と保持・置換試験の対応。これは20でPlan上充足しましたが、実行合格ではありません。
3. 実機対象環境・方式・依存権限・両入力機器・独立検証の供給条件の確認。
4. 全費用・リスクの確定部分と未確定部分の整理。
5. 承認内と判断できる根拠、または必要な具体的Owner承認。

技術方式はTechnical Director、詳細仕様はDesignerの権限に残します。headlessのみへの縮小、V2任意化、独立検証の省略は行いません。条件解決後も逐次作業と、独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewを維持します。明白な対処不能・到達不能はPlay前にもDesignerへ戻します。

回答待ちの間に継続する独立作業はありません。Studioは次のRouteで本EscalationをOwnerへ開き、依存Stepを停止してGoalをblocked-on-ownerにします。本Stepではgoal.mdや既存Decisionを変更せず、実装・依存導入・購入・外部費用の確約・外部連絡も行いません。play／botsは実行しておらず、新しい実測証拠はありません。

## Owner decision required

A／B／Cと条件を回答してください。

AまたはBの場合は、上表の供給責任者・検証枠の権限者・予算権限者を役割で指定してください。まだ指定できない項目は未指定と回答できますが、その不足が解決するまでBuildは保留します。Bの場合は調査対象・担当・利用可能な既存配員枠・停止条件も指定してください。

この回答による責任者指定・情報確認への同意と、未確定の購入・導入・実装費用の承認は区別します。費用承認には、具体的な対象・見積もり・上限・条件が必要です。Cの場合は再開条件を添えてください。

---

**Owner response (2026-10-20):** 案A。回答の権限者はすべて Owner（私）で、ここで回答します。(1) 実行経路: project.md の build: と run_tests / run_play / run_trace / run_bots がそのまま実行経路です。gameplay-engineer と qa は Step の中で @run を使い、サンドボックスでテスト・プレイ・トレース・ボットを実行できます（G-001 と同じ）。基線は repo/ の現状で、指定 sha の確認は不要です。project.md の「build 0.4」は古い記述で、repo/ が正です。(2) 実機・gamepad・デスクトップの表示環境はなく、用意もしません。Constraints の「Desktop, keyboard and gamepad」は製品の対象環境で、今回の検証環境の要求ではありません。検証は G-001 と同じく、テキスト表示のビルドとスクリプト実行で行います。(3) 独立した QA と Play は、Studio の qa と playtester の Step が担います。外部の配員はありません。(4) 費用: 購入・外部委託・追加の金銭は一切ありません。予算は Studio の通常の Step の範囲で、人日の見積もりは不要です。以上で D-020 の条件は満たされたものとして、Build へ進んでください。
>>>END
