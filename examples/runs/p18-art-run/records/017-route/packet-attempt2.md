# Studio operation packet

operation: Route
goal: G-002
step_artifacts: goals/G-002-entity-pictures/14-qa-to-studio.md, goals/G-002-entity-pictures/15-art-director-to-studio.md
next_seq: 16
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha 57e193e6b722; run through the project's run commands)
log: last 5 of 6 entries in @log-recent; the full history is goals/G-002-entity-pictures/log.md
goal_budget: 15 of 13 operations used — over budget: add no stages except a game-director step that cuts the remaining work to what the Owner request needs, or an owner step that escalates the cost; planned steps may still be opened

## You may write

- goals/G-002-entity-pictures/goal.md
- goals/G-002-entity-pictures/14-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-002-entity-pictures/15-art-director-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- project.md: only in the Route that closes the Goal, and only its ## Current state (at most 1,500 characters)
- goals/G-002-entity-pictures/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 16
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
id: ember-hollow
name: Ember Hollow (new concept)
repository: repo/ (empty: no build exists yet)
owner_language: ja
player_visible: repo/manual.md
build: repo
page: index.html
run_tests: node --test
run_play: node play.js {script}
run_trace: node play.js --trace {script}
---
# Project: Ember Hollow (new concept)

## Vision

A short turn-based roguelike. The player descends five floors of a cave carrying a single ember.
The ember is both light and time: its glow is how far the player can see, it dims a little every
turn, and only the braziers scattered through the floors rekindle it. The creatures of the hollow
live in the dark and react to the light. Floor 5 holds the creature that keeps the hollow dark;
beating it wins the run. Dying, or letting the ember go out, ends it.

Pillars:

1. **Every turn is a decision.** Move, wait, fight or use an item; every threat that can hurt the
   player next turn is visible and readable before it does.
2. **Light is the resource.** Seeing farther and having more time are the same thing; spending the
   ember is the core trade-off of a run.
3. **A run is short and different each time.** A whole run takes 15 to 30 minutes. Floors are made
   from a seed, so every seed is a different run, and the same seed is always the same run.

## Player profile

Players who enjoy short roguelikes: they like learning how each creature behaves and planning a
few turns ahead, and accept losing a run to learn from it. They play with a keyboard, or by
clicking, in a browser.

## Current state

After G-001 (partly met): `repo/` holds a build with five floors, ember, three creature types,
the Gloom and seeded runs; rules are shared by the page and the text player (D-001); threats
and reach are marked (D-002). Design docs are in `design/` (30 acceptance checks).
`node --test` passes 49/49.

Run it: open `repo/index.html` (browser); `node play.js {script}` (add `--trace` for state);
`node --test`. Script format and player info: `repo/manual.md`.

Not verified: the browser page (checks 27-30) has been seen by no one. No whole run has been
observed: Play covered only seed 42, floor 1, 16 turns. Floors 2-5, braziers, items, hounds,
shades, Gloom, win/loss, run length and balance are unobserved. QA did not see per-test
results for checks 13, 14 (hand-made) and 26.

Known weakness: old messages stay in later frames (spec's "last 5"), so new events are hard
to tell from old.

Proposed next Goals: (1) Owner checks the page; (2) QA full test listing; (3) broad playtest
and balance; (4) message legibility.

## Constraints

- The build is JavaScript for Node.js 20 and the browser, with no dependencies and no network
  use, in `repo/`. The game's rules live in code that both ways of playing share.
- **For people: a browser page.** `repo/index.html` opens straight from the file system (no
  server) and is played with the keyboard or the mouse. It draws the floor as a grid.
- **For the team: input scripts.** `run_play` (`node play.js {script}`) plays a script and prints
  what the player sees, as text, turn by turn; `run_trace` adds the internal state; `run_tests`
  (`node --test`) runs the build's tests. The script format (including how a run's seed is
  chosen) is the build's to define, in `repo/manual.md`, which ships with the build and is all a
  player is told.
- Deterministic: the same seed and the same commands always give the same run.

## Design index

None yet.
>>>END

<<<FILE @project-files
decisions/D-001-classic-scripts-shared-rules.md
decisions/D-002-threat-and-reach-marks.md
decisions/D-003-picture-style-and-mark-layering.md
decisions/D-004-pictures-drawn-by-code-with-pure-scene-mapping.md
decisions/D-005-tile-size-and-mark-chips.md
design/acceptance-criteria.md
design/entity-pictures.md
design/game-spec.md
goals/G-001-first-playable-run/01-studio-to-game-designer.md
goals/G-001-first-playable-run/02-game-designer-to-technical-director.md
goals/G-001-first-playable-run/03-technical-director-to-gameplay-engineer.md
goals/G-001-first-playable-run/04-studio-to-game-designer.md
goals/G-001-first-playable-run/05-gameplay-engineer-to-qa.md
goals/G-001-first-playable-run/06-game-designer-to-studio.md
goals/G-001-first-playable-run/07-studio-to-gameplay-engineer.md
goals/G-001-first-playable-run/08-studio-to-game-designer.md
goals/G-001-first-playable-run/09-gameplay-engineer-to-qa.md
goals/G-001-first-playable-run/10-game-designer-to-studio.md
goals/G-001-first-playable-run/11-studio-to-gameplay-engineer.md
goals/G-001-first-playable-run/12-gameplay-engineer-to-qa.md
goals/G-001-first-playable-run/13-qa-to-studio.md
goals/G-001-first-playable-run/14-studio-to-playtester.md
goals/G-001-first-playable-run/15-playtester-to-studio.md
goals/G-001-first-playable-run/16-studio-to-game-director.md
goals/G-001-first-playable-run/17-game-director-to-studio.md
goals/G-001-first-playable-run/goal.md
goals/G-001-first-playable-run/log.md
goals/G-002-entity-pictures/01-studio-to-art-director.md
goals/G-002-entity-pictures/02-art-director-to-studio.md
goals/G-002-entity-pictures/03-studio-to-technical-director.md
goals/G-002-entity-pictures/04-technical-director-to-gameplay-engineer.md
goals/G-002-entity-pictures/05-gameplay-engineer-to-studio.md
goals/G-002-entity-pictures/06-studio-to-qa.md
goals/G-002-entity-pictures/07-studio-to-art-director.md
goals/G-002-entity-pictures/08-qa-to-studio.md
goals/G-002-entity-pictures/09-art-director-to-studio.md
goals/G-002-entity-pictures/10-studio-to-gameplay-engineer.md
goals/G-002-entity-pictures/11-gameplay-engineer-to-studio.md
goals/G-002-entity-pictures/12-studio-to-qa.md
goals/G-002-entity-pictures/13-studio-to-art-director.md
goals/G-002-entity-pictures/14-qa-to-studio.md
goals/G-002-entity-pictures/15-art-director-to-studio.md
goals/G-002-entity-pictures/goal.md
goals/G-002-entity-pictures/log.md
project.md
repo/README.md
repo/index.html
repo/manual.md
repo/play.js
repo/src/floorgen.js
repo/src/game.js
repo/src/light.js
repo/src/page.js
repo/src/pictures.js
repo/src/rng.js
repo/src/scenario.js
repo/src/scene.js
repo/src/script.js
repo/src/textview.js
repo/src/view.js
repo/tests/bot.js
repo/tests/bots.test.js
repo/tests/creatures.test.js
repo/tests/floors.test.js
repo/tests/g001-final.test.js
repo/tests/gloom.test.js
repo/tests/golden.test.js
repo/tests/golden/hashes.json
repo/tests/helpers.js
repo/tests/marks.test.js
repo/tests/pic-helpers.js
repo/tests/pictures.test.js
repo/tests/reach.test.js
repo/tests/rules.test.js
repo/tests/scene.test.js
repo/tests/view.test.js
>>>END

<<<FILE @decision-titles
decisions/D-001-classic-scripts-shared-rules.md — D-001: Shared code is plain classic-script modules (UMD style), not ES modules
decisions/D-002-threat-and-reach-marks.md — D-002: threat marks plus reach marks on the four neighbour tiles
decisions/D-003-picture-style-and-mark-layering.md — D-003: flat dark-cave pictures, and marks always drawn over pictures
decisions/D-004-pictures-drawn-by-code-with-pure-scene-mapping.md — D-004: pictures are drawn by code on the canvas; a pure scene module maps the view model to pictures
decisions/D-005-tile-size-and-mark-chips.md — D-005: tile 28 px, dark chips behind badges and reach letters, player and shade/Gloom contrast
>>>END

<<<FILE goals/G-002-entity-pictures/goal.md
---
kind: goal
id: G-002
project: ember-hollow
status: active
created: 2026-10-26
budget: 13
---
# G-002: Pictures for each kind of thing in the game

## Owner request

> それぞれに絵をつけてほしい

## Interpretation

"それぞれ" has no stated referent. The Studio reads it as: **each kind of thing the player meets and sees on the floor grid gets its own picture** (a drawn image instead of a bare glyph or colour), with the player and ember, each creature type (three), braziers, and items as the core set. Whether terrain tiles (walls, floor, the Gloom) and the final-floor creature are included is the Art Director's call from the design docs, within this reading.

Success, observable: on the browser page, a player can tell every kind of entity apart by its picture at a glance, the pictures fit the cave and ember mood of the vision, and the threat and reach marks (D-002) and the ember-light visibility are still as readable as before.

Out of scope: rule, balance or content changes; new creatures or items; the text player's output (`node play.js`) and its format; sound; animation unless the spec asks for it. The pictures must not add dependencies or network use, and the page must still open from the file system (project constraints).

Risk noted: if the Owner meant something narrower (e.g., creatures only) or wider (e.g., a picture for every floor), the Art Director's scope list will show it. The Owner can correct it on seeing the Design step's result. This is not escalated now, because the reading above is a plain one and stays within the vision.

## Unknowns

- Observe: skipped. This is an addition, not a problem report. No one has yet seen the browser page (project.md Current state).
- Diagnose: skipped. Nothing is misbehaving.
- Decide: skipped. Visual style within the vision is the Art Director's authority; no direction or priority choice is open.
- Design: settled. Spec design/entity-pictures.md (criteria 31 to 49), D-003, and D-005 (tile size and mark chips).
- Plan: settled. Method fixed in the Technical Director's plan and D-004.
- Build: second pass done (D-005 applied; 69/69 tests). Not yet seen by anyone: board width at 28 px, chip placement, player outline.
- Verify: second pass open. QA checks criteria 31 to 49 with real screenshots (one key name per `shot` press); the Art Director gives the visual verdict in parallel.
- Play: tentative. Only if the page can actually be shown to a playtester with the available means. Otherwise the limit is stated at Close.
- Review: skipped. Not an experience Goal and no direction Decision is involved.

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Design | art-director | write-design-spec | done | 02-art-director-to-studio.md |
| 2 | Plan | technical-director | technical-plan | done | 04-technical-director-to-gameplay-engineer.md |
| 3 | Build | gameplay-engineer | implement-change | done | 05-gameplay-engineer-to-studio.md |
| 4a | Verify | qa | verify-change | done | 08-qa-to-studio.md |
| 4b | Verify (visual) | art-director | visual-review | done | 09-art-director-to-studio.md |
| 5 | Build (fix 44, D-005) | gameplay-engineer | implement-change | done | 11-gameplay-engineer-to-studio.md |
| 6a | Verify (2nd, screenshots) | qa | verify-change | open | 12-studio-to-qa.md |
| 6b | Verify (visual, screenshots) | art-director | visual-review | open | 13-studio-to-art-director.md |
| 7 | Play | playtester | playtest-session | tentative | — |

Status: planned | tentative | open | done | skipped. Play becomes planned if the page can be shown to a player.

## Route changes

After Build (done): D-005 applied, 69/69 tests. Fresh Handoffs for QA (12) and the Art Director (13) open in parallel, without the engineer's assessment. Budget: 11 of 13 used before this Route; both steps bring it to 14, so the next Route must apply the budget rule (scope step or Owner step).

## Next action

Start steps 6a and 6b in parallel: qa with `12-studio-to-qa.md`, art-director with `13-studio-to-art-director.md`. Both address their results to studio. The next Route waits for both and, with the budget used up, may add only a game-director scope step or an owner step.

## Outcome

(Written at Close, in Japanese.)
>>>END

<<<FILE @log-recent
## 003-route · 2026-10-26

Status: active. Open: 03-studio-to-technical-director.md.

After Design (done): spec design/entity-pictures.md written, D-003 recorded. Art Director advised a Plan because the picture method is risky, so Plan is now planned and open. Build follows; Verify and Play unchanged.

## 005-route · 2026-10-26

Status: active. Open: 04-technical-director-to-gameplay-engineer.md.

After Plan (done): plan written (04) and D-004 recorded; the spec is feasible, no hand-back to Design. Build is now open with the plan as its Handoff. The engineer addresses the build notes to studio so Verify can get a fresh Handoff without the Sender assessment.

## 007-route · 2026-10-26

Status: active. Open: 06-studio-to-qa.md, 07-studio-to-art-director.md.

After Build (done): build notes (05) are addressed to studio. QA (06) and the Art Director (07) get fresh Handoffs without the engineer's assessment and run in parallel. Play stays tentative: it depends on whether anyone can show the page.

## 010-route · 2026-10-26

Status: active. Open: 10-studio-to-gameplay-engineer.md.

After Verify (done): QA failed criterion 44 (no reach-letter backing); the Art Director's D-005 asks for more legibility changes. Both go to one Build (10). Then Verify runs again in parallel with screenshots. Budget: 10 of 13 used; steps 5 to 6b plus Routes need more, so the next Route must check the budget rule.

## 012-route · 2026-10-26

Status: active. Open: 12-studio-to-qa.md, 13-studio-to-art-director.md.

After Build (done): D-005 applied, 69/69 tests. Fresh Handoffs for QA (12) and the Art Director (13) open in parallel, without the engineer's assessment. Budget: 11 of 13 used before this Route; both steps bring it to 14, so the next Route must apply the budget rule (scope step or Owner step).
>>>END

<<<FILE goals/G-002-entity-pictures/14-qa-to-studio.md
---
kind: handoff
goal: G-002
seq: 14
from: qa
to: studio
stage: Verify
outcome: partial
---
# 14: qa → studio — second verification of the entity pictures: no criterion fails, but most visual criteria are still unchecked; 44 not verified

## Task

Route the result. The first real screenshots exist, and nothing seen fails. The scenes that matter most (reach marks, threat marks, creatures other than a moth, the flame at r = 2) cannot be reached with the `shot` tool as it works. Studio decides how to get those scenes seen (see Open questions). This is not a pass.

## Context

Goal G-002, second QA pass, against `design/entity-pictures.md` criteria 31 to 49 on the build with D-005 applied. I changed nothing in `repo/`. I did not use implementer assessments.

Budget: I used 1 round each of `tests`, `play` and `shot` (two `shot` runs). I did not use the second round, because no further run available to me could reach the missing scenes (see Findings, "Why more runs did not help").

## Findings

### Means used

- `node --test`: exit 0, 69 tests, 69 pass, 0 fail.
- `node play.js` on a seed 42 script (`dddd ss ..`): exit 0. Frames are well-formed and refused moves are marked "(refused: no turn passed)".
- `shot` start: a fresh page, 0 keys, 1 screenshot, `console_errors: []`.
- `shot` walk: keys `d d d d s s Space Space` (one key name per press, as asked). 8 keys pressed, 1 screenshot, `console_errors: []`. The screenshot shows Turn 6, so two presses were refused moves.
- I did not read `page.js` or `pictures.js` this round, so I make no code-level claims about the D-005 changes.

### What the two screenshots show (1000x700 viewport, tile 28 px)

Observed on the page:

- Wall: stone-block texture, clearly lighter than the floor.
- Floor: dark speckled ground.
- Unlit brazier: a small grey bowl. It is visible but small and low in contrast on the floor.
- Player: pale head, blue cloak and a gold flame, with a dark outline. At turn 0 the player stands on `<` (confirmed by the text frame) and is still readable there.
- `<`: blue rising steps.
- Moth: pale winged picture on the floor about 3 to 4 tiles away. It has no threat border and no reach mark. Not adjacent, so none was expected.
- Remembered tiles: wall segments at the edge of the explored area are visibly darker than visible walls. Unseen tiles are black.
- The board is near black overall. The brightest warm spot on the board is the player's flame.
- Both loads had empty `console_errors`.
- The inventory buttons show text only (`[1] empty`), as expected with no items.
- The ember bar and the HP, turn and ember text are shown.

Layout: the canvas is about 786 px wide and 450 px high (x 12 to 798, y 51 to 500). At the 1000 px viewport the side panel wraps below the board, and the lower buttons (New seed) are cut off by the 700 px viewport height. I could not set a 1280 px window. By calculation, the board plus the gap plus the panel needs 12 + 786 + 16 + (300 to 360) + 12 = about 1126 to 1186 px, which is under 1280. So the panel should sit beside the board at 1280 px. This is computed, not measured.

### Why more runs did not help

- `shot` takes keys only. It cannot choose a seed, set the URL hash, or place the player next to a hound, a shade or the Gloom.
- With the default seed and the first few turns, only a quiet start room is reachable.
- I may not write `repo/` files (a fixture page or scenario harness), so I cannot build the missing scenes myself.

### Per-criterion result

| # | Result | Evidence and limit |
|---|---|---|
| 31 | not checkable (partial) | Seen with their own picture: wall, floor, unlit brazier, player, `<`, moth. Not seen on the page: shade, hound, Gloom, lit brazier, salve, oil, `>`. The Node mapping test covers all entities in structure only. |
| 32 | not checkable | Needs shade, hound and Gloom on the page, and greyscale. Not seen. |
| 33 | not checkable | Only the unlit brazier and `<` were seen. No salve, oil flask, lit brazier or `>`. |
| 34 | pass for what was seen | Wall and floor are told apart at a glance. The brazier, moth and player stand out from plain floor. The unlit brazier is the weakest of these. |
| 35 | partial | Player visible on `<` at turn 0 (screenshot 1). The lit brazier case was not seen. |
| 36 | not checkable | Only r = 6 seen. No r = 2 screenshot is reachable with keys. |
| 37 | not checkable | No items in inventory. |
| 38 | pass for terrain, partial overall | Remembered wall is visibly darker than visible wall, and the same shapes are kept. Unseen is black. The no-creature-on-memory part is untested on the page. |
| 39 | not checkable | Needs a tile at the edge of the glow next to a remembered tile at r = 6 and r = 2. Not seen at either. |
| 40 | not checkable | Needs a run through E thresholds. |
| 41 | pass, limited | Dark frame, warmest bright spot on the board is the flame. Only quiet start frames were seen; no lit brazier. |
| 42 | not checkable | No creature with a threat mark was seen. |
| 43 | not checkable | No crouch line or Gloom area seen. |
| 44 | **not verified (re-check order not fulfilled)** | No reach mark appeared in either screenshot, so I could not see the new letter backing. This is neither a pass nor a repeat fail. The earlier fail (no backing) stands as the last observed state until a reach mark on an item tile and on a lit brazier is seen. |
| 45 | pass at view level only | `criterion 45` test passes (scripted runs with hound crouch, Gloom gather, flare and random walks). Page marks vs text marks not compared pixel-wise. |
| 46 | not checkable | No stunned or crouching creature seen. |
| 47 | pass for first load | `console_errors` empty on both loads. All pictures that appeared loaded. The whole picture set was not exercised. |
| 48 | pass, with the limits stated in 08 | 69 of 69 tests pass, including 7 of 7 golden hash tests. `node play.js` runs. |
| 49 | not checkable | Controls only partly exercised: `d`, `s` and Space moved or waited (turn 0 to 6, E 100 to 94). Clicks, slots, R/N and summary screens not exercised. |

### Regressions

1 to 26: covered by the passing named tests above. 27: the page shows the grid, ember bar with E and r, HP, floor, turn, inventory slots and buttons in the screenshots. The last 5 messages and the seed line fall below the 700 px viewport, so I did not see them. 28 and 30 are not checked.

### Observations to pass on (visual, not criterion fails)

- At the 1000 px viewport the panel is under the board and the page needs scrolling. Expected from `flex-wrap`, not a defect, but the 1280 px fit is unmeasured.
- The unlit brazier is small and grey on dark floor. It reads, but is the least prominent picture in the frames.

### Verdict

No criterion is shown to fail this round. No criterion that needs a threat, reach, creature, item, flare or low-radius scene is verified. Criterion 44, which was to be re-checked first, is not verified. The change cannot count as verified.

## Decisions already made

- D-002: threat and reach marks. D-003: flat dark-cave pictures, marks over pictures. D-005: tile 28 px, dark chips behind badges and reach letters, player and shade/Gloom contrast.

## Constraints

- I changed no file in `repo/`, and I did not decide intended look or behaviour.
- I do not mark a criterion pass by inference from code or tests.

## Open questions

1. Studio: how to get the missing scenes seen. Options:
   a. Allow QA to write a QA-only fixture page and script under a new path (for example `qa/`) that loads the real `src/` files, sets a seed through the URL hash, and drives a scenario (hound crouch, Gloom gather, shade at r = 2, flare, items) before the screenshot. The role allows QA to add test tooling, but this packet's write list did not include such a path.
   b. Extend `shot` so its input can set the URL hash (seed) or a viewport width. The missing 1280 px measurement needs that too.
   c. Ask the Owner to look at the page at 1280 px.
2. Which scenes the next pass must capture. Criterion 44 first:
   - a reach mark on an item tile and on a lit brazier, letters readable on the dark chip;
   - a threat border and `!` chip on an adjacent moth and a hound, one of them in row 0;
   - a crouching hound with its line, and a Gloom area over items;
   - a stunned creature;
   - the player on a lit brazier, and at r = 2 next to r = 6 (flame size and glow edge);
   - a shade and the Gloom next to the floor (contrast, D-005 item 6);
   - the inventory with a salve and an oil flask;
   - the page at 1280 px (measure panel position and any horizontal scroll).
3. If a second QA pass is routed, give it the harness in 1a or 1b and at least one `shot` round with a seed that places a moth, hound and shade within the first 30 turns. The seed must come from a text trace (`node play.js --trace`) taken beforehand.

## Expected output

Studio chooses the means in Open question 1, then routes a third QA pass that covers the scenes in Open question 2. Success: every criterion 31 to 49 is marked pass, or a stated not-checkable with a named reason that the Owner accepts. A failing criterion goes to `gameplay-engineer`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/entity-pictures.md, design/acceptance-criteria.md, repo/manual.md, repo/index.html, the build in repo/ (`node --test`, `node play.js {script}`, `node play.js --trace {script}`, screenshots of `index.html`)
- Decisions: decisions/D-002-threat-and-reach-marks.md, decisions/D-003-picture-style-and-mark-layering.md, decisions/D-005-tile-size-and-mark-chips.md
- Previous handoff: goals/G-002-entity-pictures/12-studio-to-qa.md
>>>END

<<<FILE goals/G-002-entity-pictures/15-art-director-to-studio.md
---
kind: handoff
goal: G-002
seq: 15
from: art-director
to: studio
stage: Verify
outcome: partial
---
# 15: art-director → studio — final visual review: only the plain-floor view could be seen; most verdicts stay unverified

## Task

Record this visual review. Decide whether another look is worth the cost (see Open questions). Pass the one suggested small change (dim factor) to the next Build, if the Studio agrees.

## Context

Goal G-002 (pictures for each thing on the floor grid). Handoff 13 asked for a verdict per criterion 31 to 46 from real screenshots. The `shot` tool gave one usable screenshot (round 2 of the first run). Round 1 failed because the key script `dddd` is not a valid key name; keys must be space-separated (`d d d d`). The usable screenshot is floor 1, turn 2, seed unknown, after `d d d d s s`. Each run yields one image taken after the last key. The page picks a random seed on load, and the tool cannot set a `#seed` hash. So I cannot reproduce or aim at a hound, the Gloom, a stunned creature, marks or two flame radii. I did not use the last run: it would give one more random frame and no way to reach those scenes.

## Findings

**What the screenshot shows (verified by sight).** Console errors: none (`console_errors: []`). The board is 28 columns by 16 rows at 28 px, so 784 x 448 px. The viewport was 1000 px wide, so the side panel wrapped below the board, as designed by the flex-wrap.

**Fit in 1280 px (arithmetic, not seen).** 12 margin + 786 board with border + 16 gap + 360 panel = about 1174 px, which is under 1280. TILE 28 should fit side by side, and the fallback 26 is not needed. This is not seen in a 1280 window.

**Per criterion (31 to 46):**

| # | Verdict | Evidence |
|---|---|---|
| 31 | unverified (partial) | Seen with their own picture: wall, floor, `<`, unlit brazier, the player. Not seen: moth, shade, hound, Gloom, lit brazier, salve, oil, `>`. |
| 32 | unverified | No creature on screen. Greyscale not available. |
| 33 | unverified | Only `<` and the unlit brazier were seen. |
| 34 | **pass** (wall vs floor; player vs floor) | Wall is light-grey brick, floor is dark brown speckle, clear at a glance. The player stands out from the plain floor. Item and creature standing-out unverified. |
| 35 | unverified (partial) | The player reads clearly on plain floor: pale head, blue cloak, gold flame with a dark outline. Not seen on `<` or on a lit brazier. |
| 36 | unverified | Only r=6 was seen (flame large and clear, with a pale core). No r=2 frame. |
| 37 | unverified | The inventory was empty in this frame (`[1] empty` and so on, with no picture, as required). Item pictures in the slots were not seen. |
| 38 | partial | Remembered brick wall at the left of the board keeps its shape and is clearly dimmer (pass). Remembered floor tiles (lower middle and left) are nearly black, and the speckle is not visible. This is only borderline "same shape, dimmer". No creature on a remembered tile, and unseen tiles are blank (pass). |
| 39 | unverified | The visible-floor edge against remembered floor looks clear in this frame (visible floor is brown, remembered is near-black). No frame at r=2. |
| 40 | unverified | Needs frames across an E threshold. |
| 41 | **pass** (as far as one frame shows) | Near-black background. The warmest, brightest spot is the player's flame. No lit brazier seen. |
| 42 | unverified | No threat border or chip seen. |
| 43 | unverified | No hound line or Gloom area seen. |
| 44 | unverified | No reach mark seen. |
| 45 | not mine | Tile-set equality is QA's check. |
| 46 | unverified | No stunned or staggered creature, no crouching hound seen. |

**Readability notes from the one frame:**
- `<` (blue rising bars) is clear and reads as steps at 28 px.
- Unlit brazier (grey bowl) is small but recognisable, and distinct from the floor.
- Player outline works on floor. Not tested on `<` or a lit brazier, where it matters most.
- D-005 item 7 (dim factor): remembered wall and remembered floor do not merge; the wall is clearly visible against the floor. The remembered floor, though, is close to black, and the speckle is lost. I suggest 0.65 (see Required changes).

**Open points from handoff 13 that this frame cannot answer:** reach letters on salve, lit brazier and stairs tiles; reach next to the Gloom area or hound line (dash versus red border merging); threat chip hiding the shade head or moth antenna, including row 0; stunned chips; flame at r=2; Shade and Gloom against floor; the player on `<` and on a lit brazier. All stay **unverified**.

**Visual intent met?** Not confirmed. What was seen fits the cave and ember mood (dark cave, one warm light, quiet terrain) and the pictures drawn so far read clearly. Nothing seen contradicts D-005. The marks, which carry pillar 1, were not seen at all, so I do not call the Goal's visual intent met.

**Required changes.** None are demanded by what was seen. One small change is recommended:
1. `repo/src/pictures.js`, `dim()`: change the factor `0.55` (the final `* 0.55`) to `0.65`. Reason: remembered floor is almost black. Check that visible floor is still clearly brighter than remembered floor (criterion 39). This changes no mark or rule. If QA finds the visible/remembered gap too small after the change, go back to 0.60.

## Decisions already made

- D-003 (style, layering), D-004 (pictures drawn by code), D-005 (TILE 28, chips, outline, violet, Gloom ring) all stand. No new decision.

## Constraints

- No edits to `repo/`. Visual matters only; rules, balance and the text player are out of scope.
- Only what a screenshot shows counts as verified. Nothing above is a pass from code reading alone.

## Open questions

1. How can the missing scenes be seen? With the available `shot` tool the seed is random, so scenes cannot be aimed at. Options for the Studio: (a) a Build step adds a way to start from a fixed seed or scenario from the page (for example honouring `#seed`, which `page.js` already supports, if the tool can open `index.html#<seed>`; this needs a tool that passes a URL hash, which the run line `screenshots of index.html` does not show); (b) QA, who can run the Node text player with a seed, picks a seed and a script that reach each scene, and the page is then opened with that seed; (c) the Owner looks at the page himself or herself for the marks and the creatures. I cannot decide which of these the means allow. Say plainly: with the means in this step, criteria 32, 33, 35 (on `<` and a lit brazier), 36 (r=2), 37, 40 and 42 to 44, 46 cannot be shown.
2. Does the Studio accept the Goal on the partial evidence, or hold G-002 until the mark scenes are seen? My recommendation: hold, because the marks are pillar 1 and the D-005 chips and backings were never seen working.

## Expected output

The Studio records this partial review. It then either (a) routes the dim-factor change to the gameplay-engineer and arranges a way to see the marked scenes (open question 1), then returns to art-director for a short final verdict on criteria 35, 36, 42 to 44 and 46, or (b) hands the open scenes to the Owner as a look-and-confirm item.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md
- Project: design/entity-pictures.md, repo/src/page.js, repo/src/pictures.js, the build in repo/
- Decisions: decisions/D-003-picture-style-and-mark-layering.md, decisions/D-005-tile-size-and-mark-chips.md
- Previous handoff: goals/G-002-entity-pictures/13-studio-to-art-director.md
>>>END

## Validation feedback

A previous executor's output was rejected for these reasons. Produce the operation's files again, fixing them:

- goal.md: the Goal has used 15 of its 13 operations, so add no stages but one: a game-director step to cut the remaining work to what the Owner request needs (the rest is then skipped), or an owner step to escalate the cost. Planned steps may still be opened
- goals/G-002-entity-pictures/16-studio-to-game-director.md: Load entry missing: 14-qa-to-studio.md (did you mean goals/G-002-entity-pictures/14-qa-to-studio.md? Paths are relative to the project)
