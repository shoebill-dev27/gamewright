# Studio operation packet

operation: Route
goal: G-003
step_artifacts: goals/G-003-dash-availability-clarity/10-qa-to-studio.md
next_seq: 11
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha aa28af2ce710; run through the project's run commands)
log: last 5 of 5 entries in @log-recent; the full history is goals/G-003-dash-availability-clarity/log.md
goal_budget: 10 of 17 operations used

## You may write

- goals/G-003-dash-availability-clarity/goal.md
- goals/G-003-dash-availability-clarity/10-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- project.md: only in the Route that closes the Goal, and only its ## Current state (at most 1,500 characters)
- goals/G-003-dash-availability-clarity/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 11
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
- Nothing exists beyond this packet and what it offers: build runs (`@run`), one request for more
  files (`@need`), and the operations that follow. There is no other environment, staff, device,
  budget or log store, so never ask the Owner for them; say plainly what your means cannot show.
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
   short kebab-case slug, ISO dates) with its **budget**: the operations the Goal should need,
   two per planned stage (its Step and the Route after it), plus four for one return through
   two stages (e.g., back to Design and Build), plus one for Intake. Then
   write the first Handoff `01-studio-to-<role>.md`; mark that
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
   If the Owner's choice ends the Goal (stop, abandon, or accept it as it is), Close instead: no
   next step, `status: done` or `abandoned`, the Outcome saying plainly what was and was not
   achieved, and the Current state brought up to date.
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
- **Budget.** The runtime counts a Goal's operations and shows them against `goal.md`'s budget.
  Once the budget is used, a Route adds no stages but one: a `game-director` step that cuts the
  remaining work to what the Owner request needs (scope within the Goal; the rest is then
  `skipped`), or an `owner` step that escalates the cost. Planned steps may still be opened, and
  the loop limits' re-plan steps give way to the scope decision. Only the Owner changes the
  budget, in a Resume.
- `partial` is not a question: nothing is missing, so route the rest of the work back to the same
  Role and never escalate for it. The same work handed back `partial` three times in a row →
  route to `technical-director` to split or re-plan it.
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
outcome: <sender's step result: routed | done | partial | pass | fail | question | goal-met | goal-not-met>
---
# NN: <from> → <to> — <one-line task>

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. The sender fills Task through Open questions and drafts Expected output; the Studio
checks it against the recipient's "Works from", settles Expected output and fills Load when routing.
outcome: routed = written by the Studio; done = work finished, no verdict; partial = work under way,
nothing missing, to be continued by the same Role; pass/fail = verification verdict; question =
handed back with an open question; goal-met/goal-not-met = Review verdict.
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
budget: <N>             # operations (Steps, Routes, Resumes) this Goal should need; set at Intake, changed only by the Owner
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

テキスト表示・入力スクリプトで遊ぶビルドは`repo/`（今回のsha: dc0138c2b6d1）。既存第1〜4部屋から進む連続ラン、第5部屋の単体ボス、終端・再挑戦が実装報告済み。入力はattackとdash。操作・スクリプト形式は`repo/manual.md`、公開ドライバは`repo/public-driver.md`を参照。

repo/で実行：試験は`python3 -m unittest discover -s tests`、プレイは`python3 play.py --view player {script}`、状態表示は`python3 play.py --view trace {script}`、botは`python3 bots.py {script}`。source fc07c7db6383で161 tests OKの記録がある。今回のshaでの再試験は本Resumeでは未実施。

G-002はD-027により費用を理由に未達・検証未完了で打切り。実装は保持する。公開情報限定botの実接続・記憶、被弾差の原因確定、経路監査、接触診断全体、ボス4条件・保持回帰の再測定、公開再生の証拠確認が未完了。独立QAの再検証、限定Art Verify、独立Play、実測後Designer判断、最終Reviewも未実施。試験成功は体験Goal達成を示さない。

変更前ビルド不在による歴史的一致の確認不能は別途残る。通常ラン勝利時間のBuild報告は約87〜104秒で、15〜20分Visionとの整合は未評価。再開の必要性は別GoalとしてOwnerが判断する。

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
decisions/D-022-g002-v1-supplements.md
decisions/D-023-owner-confirms-verification-supply.md
decisions/D-024-g002-historical-comparison-evidence.md
decisions/D-025-g002-minimum-remaining-scope.md
decisions/D-026-owner-extends-g002-budget.md
decisions/D-027-owner-stops-g002.md
decisions/D-028-dash-indicator-on-legacy-route.md
design/combat-cues-visual-spec.md
design/combat-step-44-walker-limit.md
design/combat-step-46-room3-cap.md
design/combat-step59.md
design/combat-step68.md
design/combat-step72.md
design/combat-step94.md
design/combat.md
design/dash-availability.md
design/final-boss-and-continuous-run.md
design/g002-historical-comparison-evidence.md
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
goals/G-002-final-boss/33-studio-to-gameplay-engineer.md
goals/G-002-final-boss/34-gameplay-engineer-to-studio.md
goals/G-002-final-boss/35-studio-to-gameplay-engineer.md
goals/G-002-final-boss/36-gameplay-engineer-to-studio.md
goals/G-002-final-boss/37-studio-to-gameplay-engineer.md
goals/G-002-final-boss/38-gameplay-engineer-to-studio.md
goals/G-002-final-boss/39-studio-to-gameplay-engineer.md
goals/G-002-final-boss/40-gameplay-engineer-to-studio.md
goals/G-002-final-boss/41-studio-to-gameplay-engineer.md
goals/G-002-final-boss/42-gameplay-engineer-to-studio.md
goals/G-002-final-boss/43-studio-to-gameplay-engineer.md
goals/G-002-final-boss/44-gameplay-engineer-to-studio.md
goals/G-002-final-boss/45-studio-to-gameplay-engineer.md
goals/G-002-final-boss/46-gameplay-engineer-to-studio.md
goals/G-002-final-boss/47-studio-to-game-designer.md
goals/G-002-final-boss/48-game-designer-to-studio.md
goals/G-002-final-boss/49-studio-to-gameplay-engineer.md
goals/G-002-final-boss/50-gameplay-engineer-to-studio.md
goals/G-002-final-boss/51-studio-to-gameplay-engineer.md
goals/G-002-final-boss/52-gameplay-engineer-to-studio.md
goals/G-002-final-boss/53-studio-to-gameplay-engineer.md
goals/G-002-final-boss/54-gameplay-engineer-to-studio.md
goals/G-002-final-boss/55-studio-to-gameplay-engineer.md
goals/G-002-final-boss/56-gameplay-engineer-to-studio.md
goals/G-002-final-boss/57-studio-to-qa.md
goals/G-002-final-boss/58-qa-to-studio.md
goals/G-002-final-boss/59-studio-to-qa.md
goals/G-002-final-boss/60-qa-to-studio.md
goals/G-002-final-boss/61-studio-to-technical-director.md
goals/G-002-final-boss/62-technical-director-to-studio.md
goals/G-002-final-boss/63-studio-to-owner.md
goals/G-002-final-boss/64-studio-to-game-designer.md
goals/G-002-final-boss/65-game-designer-to-studio.md
goals/G-002-final-boss/66-studio-to-technical-director.md
goals/G-002-final-boss/67-technical-director-to-studio.md
goals/G-002-final-boss/68-technical-director-to-studio.md
goals/G-002-final-boss/69-studio-to-gameplay-engineer.md
goals/G-002-final-boss/70-gameplay-engineer-to-studio.md
goals/G-002-final-boss/71-studio-to-gameplay-engineer.md
goals/G-002-final-boss/72-gameplay-engineer-to-studio.md
goals/G-002-final-boss/73-studio-to-gameplay-engineer.md
goals/G-002-final-boss/74-gameplay-engineer-to-studio.md
goals/G-002-final-boss/75-studio-to-gameplay-engineer.md
goals/G-002-final-boss/76-gameplay-engineer-to-studio.md
goals/G-002-final-boss/77-studio-to-game-director.md
goals/G-002-final-boss/78-game-director-to-owner.md
goals/G-002-final-boss/79-studio-to-gameplay-engineer.md
goals/G-002-final-boss/80-gameplay-engineer-to-studio.md
goals/G-002-final-boss/81-studio-to-technical-director.md
goals/G-002-final-boss/82-technical-director-to-studio.md
goals/G-002-final-boss/83-studio-to-game-director.md
goals/G-002-final-boss/84-game-director-to-studio.md
goals/G-002-final-boss/85-studio-to-owner.md
goals/G-002-final-boss/goal.md
goals/G-002-final-boss/log.md
goals/G-003-dash-availability-clarity/01-studio-to-game-designer.md
goals/G-003-dash-availability-clarity/02-game-designer-to-studio.md
goals/G-003-dash-availability-clarity/03-studio-to-game-designer.md
goals/G-003-dash-availability-clarity/04-game-designer-to-studio.md
goals/G-003-dash-availability-clarity/05-studio-to-gameplay-engineer.md
goals/G-003-dash-availability-clarity/06-gameplay-engineer-to-studio.md
goals/G-003-dash-availability-clarity/07-studio-to-gameplay-engineer.md
goals/G-003-dash-availability-clarity/08-gameplay-engineer-to-studio.md
goals/G-003-dash-availability-clarity/09-studio-to-qa.md
goals/G-003-dash-availability-clarity/10-qa-to-studio.md
goals/G-003-dash-availability-clarity/goal.md
goals/G-003-dash-availability-clarity/log.md
project.md
repo/README.md
repo/bots.py
repo/game.py
repo/manual.md
repo/play.py
repo/public-driver.md
repo/run_driver.py
repo/session.py
repo/source_id.py
repo/tests/test_boss.py
repo/tests/test_boss_contract.py
repo/tests/test_boss_contract_details.py
repo/tests/test_bots_boss.py
repo/tests/test_d022_observation.py
repo/tests/test_d022_shots_and_note.py
repo/tests/test_dash_display.py
repo/tests/test_g002_evidence.py
repo/tests/test_game.py
repo/tests/test_play_run_controls.py
repo/tests/test_run_driver.py
repo/tests/test_session.py
repo/tests/test_split_c.py
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
decisions/D-022-g002-v1-supplements.md — D-022: V1補足の確定（旧経路表示、弾ID・消滅理由、長時間観測）
decisions/D-023-owner-confirms-verification-supply.md — D-023: 実際の供給上限に合わせてテキスト検証を継続する
decisions/D-024-g002-historical-comparison-evidence.md — D-024: 変更前一致要求の証拠と確認不能の扱い
decisions/D-025-g002-minimum-remaining-scope.md — D-025: 必須の体験検証を残し、重複工程を省く
decisions/D-026-owner-extends-g002-budget.md — D-026: D-025の範囲で継続し、予算を123 operationsとする
decisions/D-027-owner-stops-g002.md — D-027: G-002を未達・検証未完了で打ち切る
decisions/D-028-dash-indicator-on-legacy-route.md — D-028: The dash indicator is shown on the legacy route too (including room 5)
>>>END

<<<FILE goals/G-003-dash-availability-clarity/goal.md
---
kind: goal
id: G-003
project: lantern-depths
status: active
created: 2026-10-23
budget: 17
---
# G-003: Make it clear when dash can be used again

## Owner request

> ダッシュがいつまた使えるのか分かりにくい。分かるようにしてほしい

## Interpretation

Success condition (qualitative): a player using only what the build shows them (text player view and `repo/manual.md`) can tell, at any moment, whether dash is available now, and when it is not, when it will be available again. They no longer have to guess or press dash to find out.

This is an experience (readability) Goal. The dash rules themselves (recovery length, invulnerability, input set) are assumed to stay as they are. Changing them would be a different Goal.

Out of scope:
- Rebalancing dash or combat.
- New input buttons (D-001).
- Reopening G-002 (stopped by D-027) or its unfinished verification.
- Any other readability issue the work happens to find (these become proposed Goals).

## Unknowns

- Observe: skipped. The Owner's report is the first-hand observation, and Diagnose established the cause from the player-view output.
- Diagnose: done (02). The cause is missing information, not rules.
- Decide: skipped. A+B+C change display and wording only. It reopens if Verify shows the real cooldown differs between situations in a way that cannot be documented as is (Q3 hit during cooldown, Q4 attack recovery).
- Design: done (04, `design/dash-availability.md`, D-028). Cooldown starts at dash end (0.85 s start to start, observed at 60 FPS). Still to be confirmed by QA: after a hit (Q3), attack recovery vs dash (Q4), room-transition clear (Q5), 30 FPS.
- Plan: skipped. It becomes tentative only if Verify finds a timing or simulation change across systems.
- Build: done (08). Display on both routes and manual text built; the Build check ran 173 tests OK. Possible spec/build difference: the public driver prints a picture for accepted-dash and refusal messages, where spec 3.3 says none. QA is to judge it (Design decides if the spec must change).
- Verify: open (09). QA runs P1–P12 and Q1–Q12 at 30 and 60 FPS, including the Q8 comparison with the dash field and text stripped.
- Play: planned. An independent playtester judges from player-visible output only, using the manual.
- Review: planned. `game-director` judges whether the intent was met.

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Diagnose | game-designer | diagnose-experience | done | 02-game-designer-to-studio.md |
| 2 | Decide | game-director | make-decision | skipped (no option changes dash rules or direction) | — |
| 3 | Design | game-designer | write-design-spec | done | 04-game-designer-to-studio.md |
| 4 | Build | gameplay-engineer | implement-change | done | 08-gameplay-engineer-to-studio.md |
| 5 | Verify | qa | verify-change | open | 09-studio-to-qa.md |
| 6 | Play | playtester | playtest-session | planned | — |
| 7 | Review | game-director | review-outcome | planned | — |

## Route changes

After Build (08, done; Build check 173 tests OK): the result fits the plan, so Verify follows with no added stage. The QA Handoff omits the Sender assessment and asks QA to judge the public-driver picture difference and Q3–Q5, Q7, Q8 by observation.

## Next action

Start Step 9: `qa` runs Verify from `09-studio-to-qa.md`, addressing the result to `studio`. The Studio Route follows and composes the Playtester Handoff from player-visible information only.

Message to the Owner (ja): ダッシュ表示の実装が完了し、既存の試験も通りました。次は独立したQAが、30・60FPSの両方で仕様どおりに表示されるか、ゲームの結果が変わっていないかを確認します。

## Outcome

(open)
>>>END

<<<FILE @log-recent
## 001-intake · 2026-10-23

Status: active. Open: 01-studio-to-game-designer.md.

Intake: initial route. Observe and Plan are skipped (reasons under Unknowns); Decide is tentative.

## 003-route · 2026-10-23

Status: active. Open: 03-studio-to-game-designer.md.

After Diagnose (02): the cause is missing display information, and no option touches dash rules, inputs or scope. Decide is therefore skipped, and Design opens with options A+B+C. Observe and Plan stay skipped.

## 005-route · 2026-10-23

Status: active. Open: 05-studio-to-gameplay-engineer.md.

After Design (04): the spec is complete and touches no dash rules, inputs or scope, so no Decide or Plan. D-028 rebases only G-002's stopped L1 criterion, so no escalation. Build opens; Q3–Q5 are left to observation in Build and Verify.

## 007-route · 2026-10-23

Status: active. Open: 07-studio-to-gameplay-engineer.md.

After Build (06, partial): the engineer lacked the source files, and the spec is fine. Build goes back to the same Role with `game.py`, `run_driver.py`, `session.py` and the tests in the Load list. No stage added and no QA yet, because nothing was built.

## 009-route · 2026-10-23

Status: active. Open: 09-studio-to-qa.md.

After Build (08, done; Build check 173 tests OK): the result fits the plan, so Verify follows with no added stage. The QA Handoff omits the Sender assessment and asks QA to judge the public-driver picture difference and Q3–Q5, Q7, Q8 by observation.
>>>END

<<<FILE goals/G-003-dash-availability-clarity/10-qa-to-studio.md
---
kind: handoff
goal: G-003
seq: 10
from: qa
to: studio
stage: Verify (report to Studio; the independent Play step follows)
outcome: fail
---
# 10: qa → studio — Verification report for the dash availability display (P1–P12, Q1–Q12): fail at 30 FPS on P6/P7/Q2, plus spec questions and unverified items

## Task

Studio: compose the next Handoff from this report. Route the 30 FPS timing-tolerance ruling and the three behavior questions below to `game-designer`. Decide whether the independent Play step goes ahead in parallel. The display is truthful, so Play can judge clarity, but it cannot judge the 30 FPS timing.

## Context

Goal G-003: the Owner said it is unclear when dash can be used again. Build changed the player-facing display per `design/dash-availability.md` (D-028). I verified from the spec, the criteria and the running build. I did not use the Build report, and I did not rely on `tests/test_dash_display.py`.

Runs used: tests, play, trace and bots, 3 rounds. 0 rounds are left, so nothing below can be re-run in this step.

Source id: every run reports `b62005468da6` (build string `0.6-g002-public-32`). The packet names sha `aa28af2ce710`. **These differ.** I cannot tell whether the packet sha is a repo commit id and the run id a different hash, or whether another build was verified. Studio must confirm that `b62005468da6` is the build meant. If it is not, this report applies only to `b62005468da6`.

## Findings

### Method

All commands ran from `repo/`.

- Tests: `python3 -m unittest discover -s tests`. Result: 173 tests, OK, source `b62005468da6`. This only shows that the suite passes; it is not criterion evidence. The suite's D022 long observations show periodic output counts of 121/121 and 241/241 at both rates.
- Play, player view (`@run/play/...`), cited by script name:
  - P60 and P30: script P at 60 and 30 FPS.
  - dash-only-60 and dash-only-30: a single dash at 0.6 s.
  - hit-cooldown: 60 FPS, grub at 13,4, dense dash presses.
  - hit-cd-30: the same script at 30 FPS.
  - hit-nodash: no dash, a hit.
  - hit-early-60 and hit-early-30: a hit during the cooldown.
  - q4-attack-60 and q4-attack-30: swipe at 0.5, dash at 0.6.
  - rules-text and rules-held: reaction rules.
  - legacy-room3 and legacy-room5.
  - mode-run: `mode run` with rules.
  - public-pause (60 FPS) and pause-30: `mode room`, `room 5`, with pause.
- Trace: T60, T30, mode-run-trace.
- Bots: dodger on rooms 3,4 at 60 and 30 FPS, and the dodger on the boss with `mode room`.
- The first bots attempt (`room 3` as a script) was my invalid script, not a build fault. It exited with 1 and printed the usage line.

### Per-criterion results

Times are ±1 frame as the spec requires. "ok" means the observed value matches.

| ID | FPS | Result | Evidence |
|---|---|---|---|
| P1 | 30, 60 | **pass** | P60 and P30: the pictures at 0.00 and 0.50 end `dash: ready`. |
| P2 | 30, 60 | **pass** | `0.600 you dash right — usable again in 0.9 s` in both. |
| P3 | 30, 60 | **pass** | `0.700 dash not ready — 0.8 s left (dashing)` in both. |
| P4 | 30, 60 | **pass** | The picture at 1.00 ends `dash: 0.5 s`. The press at 1.000 prints `0.5 s left`. |
| P5 | 30, 60 | **pass** | `1.400 dash not ready — 0.1 s left` in both. |
| P6 | 60 | **pass** | `1.450 dash ready` is followed by a picture ending `dash: ready`. The picture at 1.50 is also ready. The press at 1.500 prints `you dash right`. |
| P6 | 30 | **FAIL (literal)** | `dash ready` and the ready picture appear at **1.500**, not 1.45. 1.45 ± 0.033 is 1.417–1.483, and 1.5 is outside by 0.017 s (1.5 frames from nominal). The press at 1.5 was accepted. Details in "Finding F1" below. |
| P7 | 60 | **pass** | T60 trace: first dash at 0.617, second at 1.467, start-to-start 0.85 s. |
| P7 | 30 | **FAIL (literal)** | T30 trace: a press 0.867 s after the first (1.467) is refused with wait 0.033. The next frame (1.500, 0.9 s after) is accepted. Start-to-start is 27 frames = 0.9 s, not 0.85 s. |
| P8 | 30, 60 | **pass** | dash-only-60 and dash-only-30: `dash ready` appears once, at 1.450 and 1.500. hit-nodash (no dash, a hit): no `dash ready`, and the field counts down 0.3 → 0.1 → ready. |
| P9 | 30, 60 | **pass** | hit-cooldown: the cooldown ended at about 0.85 and stun lasted to about 1.0. Presses at 0.90 and 0.95 print `0.1 s left (hit-stun)`. hit-cd-30 at 0.967 also prints `0.1 s left (hit-stun)`. R ≤ 0.3 throughout. |
| P10 | 30, 60 | **pass** (no contradiction found) | Compared with the accept/refuse of every press in P60, P30, T60, T30, hit-cooldown, hit-cd-30, hit-early-60/30, q4 and the rule runs. No `ready` or `0.0` appeared before a refusal. No time was shown before an accept. `dash ready` is always printed before the same-frame press. |
| P11 | 30, 60 | **pass** (variant) | hit-cooldown and hit-cd-30 have a grub winding up near the player from 0.017/0.033. I used a denser press script, not literally script P. The refusal numbers follow the cooldown formula exactly (0.8 dashing, 0.7 dashing, 0.6, 0.5, 0.4, 0.3), so the wind-up changes nothing. |
| P12 | 60 | **pass on what was run; coverage gap** | legacy-room3 and public-pause (boss, `mode room`) show the field in every live picture and `dash ready` after each dash. The 60 s dodger bots do not print pictures, so "every picture of a dodger-bot run" was not inspected. |
| Q1 | 30 | **pass** | T30: dash_end 0.867, dash_ready 1.500, a difference of 19 frames against 18 nominal (+1 frame). The press at 1.467 (1 frame before) is refused. The press at 1.500 is accepted. |
| Q1 | 60 | **pass; one gap** | T60: dash_end 0.850, dash_ready 1.450, exactly +0.6. Presses at 1.317/1.350/1.417 are refused. 1.45 is accepted. A press exactly 1 frame before ready (1.433) was not issued. |
| Q2 | 30, 60 | **FAIL** | Follows P6/P7 at 30 FPS. Everything else holds at both rates. |
| Q3 | 30, 60 | **observed: matches the spec** | hit-early-60: dash at 1.6, hit at 2.033 during the cooldown, ready announced at 2.450. That is the unchanged cooldown end, later than hit+0.3 = 2.333. The press at 2.45 was accepted. hit-early-30: ready 2.500, accepted. hit-cooldown (ready 0.85, stun end ~1.0): `dash ready` at 1.017 and the press at 1.1 accepted. The first accepted press is max(ready, hit+0.3) in every case. A hit does not change the cooldown. |
| Q4 | 30, 60 | **observed: attack recovery does not block dash** | q4-attack-60/30: swipe at 0.5, dash at 0.6 (inside the 0.35 s recovery) is accepted. The field was `ready` before it. No refusal reason exists for it. |
| Q5 | – | **UNVERIFIED** | See "Unverified". |
| Q6 | 30, 60 | **pass** | public-pause and pause-30: dash at 0.2, pause at 0.5–1.5. The picture at the pause reads `dash: 0.6 s` and the resumed picture reads `dash: 0.6 s`. The field is frozen and no `dash ready` is printed during the pause. The `paused` status line also carries the field. |
| Q7 | – | **partial** | See "Unverified". |
| Q8 | – | **UNVERIFIED** | See "Unverified". |
| Q9 | – | **pass; gaps** | Field seen in: legacy `room empty`, legacy rooms 3 and 5 (the note line is kept and the field is present), `mode run` rooms 1–2, and `mode room` boss. Clear screens (`room_clear`) and the death screen carry no field. Not displayed in this step: legacy rooms 1, 2 and 4, and `mode room` rooms 1–4. |
| Q10 | – | **pass (limited)** | The suite's D022 observations hold periodic counts. In every play run, periodic pictures stay on the grid (legacy on x.0/x.5, `mode run` `view-every 5` on 5.0/10.0). `dash ready` pictures are event pictures, at most one per dash. |
| Q11 | 60 | **pass** | rules-text: `when text "dash ready" then dash left` fires once at each of 1.45, 2.30, 3.15 and 4.00, each time with an accepted dash. |
| Q12 | – | **not evaluated** | The note line is kept in legacy room 5. The stripped comparison was not run (no baseline, no strip tool). G-002 is out of scope (D-027). |

### Finding F1 — 30 FPS ready moment and start-to-start (fails P6, P7 and Q2 as written)

Evidence:

- T30 shows the dash active for 8 frames (accepted frame 18, `dash_end` at frame 26). The cooldown then needs 18 more frames, and `dash_ready` is logged at the start of frame 45. That is 27 frames = 0.9 s from press to next accepted press.
- At 60 FPS the same chain gives 51 + 36 = 87 frames from the press at frame 36, i.e. 0.85 s.
- Nominal ready is 1.45 s. At 30 FPS the available frame instants are 1.433, 1.467 and 1.500.
- Nominal 1.45 ± 1 frame allows 1.417–1.483. The build accepts first at 1.500.

The display agrees with the build: `dash ready` and the ready field appear at 1.500, the refusal at 1.467 shows `0.1 s left`, and the accepted message says "usable again in 0.9 s". So this is not a display fault. It comes from frame quantization of the dash length and cooldown, which Q8 says must not change.

I did not patch or soften it. I did not decide the intended behavior either. Two readings:

- The ±1 frame tolerance in section 5 is meant against the nominal 0.85 s.
- The tolerance is meant against the build's own frame-quantized timing.

I cannot say whether the 30 FPS quantization is older than this change (no earlier build). The spec itself says the ready time at 30 FPS was "not confirmed" (section 2). Whichever way it is read, the manual line "the next dash can start 0.85 s after the previous one started" is about 0.05 s short of the observed 30 FPS value.

I cannot judge from this step whether engineer action is needed. A fix would change dash timing, which D-028 and Q8 forbid. A ruling by the designer is therefore likely the right route.

### Points 1–3 of the handoff

**1. Pictures in the public driver — difference from the spec's wording.**

- Spec 3.3 says the accepted-dash and refusal messages get "no extra picture".
- Legacy route: conforming. Dash and refusal messages are text lines only, with no picture.
- Public driver: an event picture follows each message. For example `you dash right — usable again in 0.9 s` at run 0.200 is followed by a picture at 0.217 with `dash: active`. `dash not ready — 0.4 s left` at 2.050 is followed by a picture at 2.067.
- This is the public driver's general pattern. The same happens after `you swipe: miss` and `(nothing happens)`. I could not check whether the pre-change driver did the same for the dash text, because there is no earlier build.
- Consequence: one picture per refused press. Pressing every 0.1 s in a public run prints a picture per press, which counts as event output under Q10.
- This is a difference from spec 3.3, not a conforming case. Whether it is acceptable is a question for `game-designer`.

**2. Quiet refusals — behavior differs between routes and the spec is silent.**

- Scripted presses: refusals are printed, and `text "not ready"` fires on them. In rules-text the refusal at 0.700 was followed by the rule's attack at 0.850 (0.15 s reaction).
- Legacy held rule `when nothing within 20 then dash right` (rules-held): no refusal text at all appears between the accepted dash at 0.000 and the next one at 0.900, nor between 0.900 and 1.800. The accepted dashes fall on the rule's 0.15 s grid (0.9 = 6 × 0.15, 1.8 = 12 × 0.15). That is not 0.85 or 1.75, when the cooldown ended. So the rule is pressing and being refused silently. `when text "not ready" then move up` never fired.
- Public driver rule `when see g within 1.2 then dash toward` (mode-run): a rule-driven refusal IS printed (`0.817 dash not ready — 0.7 s left (dashing)`).
- Rule-driven attacks that do nothing print `(nothing happens)` in `mode run`, for example at 2.183, 7.633 and 7.783.
- I cannot separate "legacy route vs public driver" from "action type", because the two rule scripts differ in both.
- The spec (3.4) says `text "not ready"` becomes "usable like any message". The manual says "A dash that cannot happen prints `dash not ready — …`". For legacy rule-driven presses neither holds, and neither document says what a rule-driven refusal should do.
- This is an open question for `game-designer`, not a QA verdict.

**3. Other ignored inputs — pass.** `(nothing happens)` still prints for an attack during hit-stun (hit-cooldown 0.750, hit-cd-30 0.767) and for rule-driven attacks in recovery (mode-run).

### Q7, Q8 and other gaps (unverified items, with reasons)

- **Q5 — room entry (unverified).** In mode-run the dash at 4.317 was followed by the room-1 clear at 4.967 and entry at 5.967. Entry showed `dash: ready` with no `dash ready` message at entry or on the clear screen. This does not discriminate: dash end 4.567 + 0.6 = 5.167 would be ready by itself before entry. No run left a cooldown pending at entry. Whether entry clears the cooldown, or whether a press at entry time is accepted, is unobserved. A discriminating run needs the cooldown to still be running at the entry frame.
- **Q7 — consistency (partial).**
  - Per-press consistency is established in the legacy and public play runs listed in P10. In bot logs, "dash ready" reads and a `dash not ready` step decision agree with the elapsed time since each dash.
  - The bot logs print decisions, not each press's acceptance or the announced R. My results truncate the 60 s dodger outputs, so "every dash input accepted iff the last announced R was 0" was not checked across them.
  - Float residue at 30 FPS: T30 frame 44 shows `dash_cooldown=0.000` after the step and the press in that frame refused with wait 0.033. This agrees with the state before the step. No `dash: 0.0 s` was ever displayed.
- **Q8 — no side effects (unverified).**
  - There is no earlier build and no strip tool, so no byte-comparison was possible.
  - Strongest available evidence: the 173-test suite, including long-standing game, bot and driver tests, passes. Dash timing at 60 FPS matches the pre-change probe in spec section 2 (start-to-start 0.85 s). The periodic grid is unchanged in all runs. Normal-run clear times in the suite (86.97 s at 30 FPS, 103.53 s at 60 FPS) fall in the range project.md records (about 87–104 s). Dodger room results (hearts lost 0, room 3: attacks 8, dashes 6 at both rates) match the suite's own retained figures — but those come from the same build, not a baseline.
  - None of this proves "identical to before". One further doubt that I cannot separate without a baseline: whether dash-related event pictures in the public driver shift the default 0.5 s periodic schedule, which public-driver.md says resumes "after event pictures".
- **Q12:** not evaluated (see table).
- **Q1 at 60:** a press exactly 1 frame before ready was not exercised.
- **Float residue under other conditions** (for example after a long pause) was not exercised.

### Docs checked against behavior

`repo/manual.md` matches the observed field and message texts, the "no field on clear or end screens" line, and `text "dash ready"`. Two statements do not match or are unverified:

- "next dash can start 0.85 s after the previous one started" — observed 0.9 s at 30 FPS (F1).
- "Entering a room makes the dash ready" — Q5 unverified.

## Decisions already made

- D-001: no new inputs. No new button was seen.
- D-028: the dash indicator shows on the legacy route too, including room 5. Confirmed: field and note line both present.
- D-027: G-002 is stopped; its verification is out of scope.

## Constraints

- Both 30 and 60 FPS apply. Tolerance ±1 frame (spec).
- I did not change the game or the spec. The code under test is not modified.
- 0 run rounds are left in this step, so no new evidence can be produced here.

## Open questions

For `game-designer` (the spec is silent or its criteria cannot be met as written):

1. **30 FPS tolerance (F1).** Is the ±1 frame in P6, P7 and Q1 measured against the nominal 0.85 s, so that 0.9 s at 30 FPS fails? Or is the frame-quantized value acceptable, in which case what should the manual say about 30 FPS? A rule change would break Q8, so this needs a designer ruling, not a patch.
2. **Public-driver pictures.** Spec 3.3 says no extra picture for the accepted-dash and refusal messages, but the public driver prints one per message. Amend the spec or require suppression?
3. **Rule-driven refusals.** Should a refused dash from a reaction rule print `dash not ready` (as in the public driver) or stay silent (as in legacy rules-held)? Should `text "not ready"` be able to fire on it? The manual promise "a dash that cannot happen prints…" currently holds only for scripted presses and the public-driver rule case I saw.
4. Q4 is recorded: attack recovery does not block dash. Spec 3.1/3.3 already follows the build here, so no change is needed unless the designer wants one.
5. Q3 is recorded: a hit does not change the cooldown. The spec rule applies unchanged.

For Studio:

6. Confirm which sha was meant (`aa28af2ce710` vs the reported `b62005468da6`).
7. If another QA round is run, it needs: a discriminating Q5 script (a `mode run` dash timed to leave the cooldown pending at the room-1 clear/entry); a 1-frame-before press at 60 FPS (1.433); a baseline or strip tool for Q8 and Q12; and bot output that records each press's acceptance for Q7.

## Expected output

Studio composes the next Handoff. Recommended routing:

- `game-designer`: open questions 1–3, because the 30 FPS finding cannot be fixed without changing dash timing (Q8).
- Independent Play step: the display is truthful and the 60 FPS timings are within spec, so Play can judge clarity. Play must be told it cannot judge the 30 FPS timing.
- Do not pass this goal until Q5, Q7, Q8 and Q12 have been verified or explicitly deferred.

## Load

- Role: studio/roles/qa.md (this report's author); the recipient is the Studio, which has no role file.
- Skills: studio/skills/verify-change.md
- Project: design/dash-availability.md, repo/manual.md, repo/public-driver.md, project.md#constraints, build in repo/ (source `b62005468da6`)
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-028-dash-indicator-on-legacy-route.md
- Previous handoff: goals/G-003-dash-availability-clarity/09-studio-to-qa.md
>>>END
