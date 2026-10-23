# Studio operation packet

operation: Route
goal: G-003
step_artifacts: goals/G-003-dash-availability-clarity/17-qa-to-studio.md, goals/G-003-dash-availability-clarity/18-playtester-to-studio.md
next_seq: 19
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha 660c1787ff32; run through the project's run commands)
log: last 5 of 8 entries in @log-recent; the full history is goals/G-003-dash-availability-clarity/log.md
goal_budget: 17 of 17 operations used — over budget: add no stages except a game-director step that cuts the remaining work to what the Owner request needs, or an owner step that escalates the cost; planned steps may still be opened

## You may write

- goals/G-003-dash-availability-clarity/goal.md
- goals/G-003-dash-availability-clarity/17-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-003-dash-availability-clarity/18-playtester-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- project.md: only in the Route that closes the Goal, and only its ## Current state (at most 1,500 characters)
- goals/G-003-dash-availability-clarity/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 19
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
decisions/D-029-g003-spec-rulings.md
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
goals/G-003-dash-availability-clarity/11-studio-to-game-designer.md
goals/G-003-dash-availability-clarity/12-game-designer-to-studio.md
goals/G-003-dash-availability-clarity/13-studio-to-gameplay-engineer.md
goals/G-003-dash-availability-clarity/14-gameplay-engineer-to-studio.md
goals/G-003-dash-availability-clarity/15-studio-to-qa.md
goals/G-003-dash-availability-clarity/16-studio-to-playtester.md
goals/G-003-dash-availability-clarity/17-qa-to-studio.md
goals/G-003-dash-availability-clarity/18-playtester-to-studio.md
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
repo/tests/test_dash_refusal.py
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
decisions/D-029-g003-spec-rulings.md — D-029: G-003 spec rulings: 30 FPS quantization, driver pictures, rule-driven refusals, evidence without a baseline
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
- Decide: skipped. The display and wording change only; D-029 (12) rules no timing or rule change. It reopens if a later step finds a criterion that needs dash timing or rules changed.
- Design: done (12, D-029). Settled: 30 FPS tolerance (0.90 s, ready at 1.500 s for a dash at 0.6 s), driver pictures after dash messages, rule-driven refusals print, baseline-free Q8/Q12 evidence.
- Plan: skipped. Becomes tentative only if a change touches timing or simulation across systems.
- Build: done (14). Legacy rule path now prints the dash refusal (display-only `quiet` flag no longer set for dash refusals); manual and public-driver text updated; new test file. Build check: 180 tests OK. Engineer ran nothing itself; no before/after comparison possible (before build gone).
- Verify: open (15). Checks: P6, P7, Q1, Q2 at 30 FPS; P13 on both routes; Q5 script; Q7 by trace; 60 FPS press at 1.433/1.450; P12 via the public replay scripts; Q8/Q12 under D-029; after-only check that game events are identical between player and trace view apart from `quiet`. Unverifiable parts (no baseline) are listed apart and not counted as pass.
- Play: open (16), parallel with Verify. Fresh Playtester, player-visible information only; clarity judged at 60 FPS.
- Review: planned. `game-director` judges whether the intent was met.
- Build identity: QA's earlier id `b62005468da6`, an earlier packet sha `aa28af2ce710`, and the latest Build-check test output shows `3951a3656940`. QA reports the id each tool shows and whether they are the same kind.
- Budget: 15 of 17 used after this Route. Verify and Play use the last two. The Route after them and Review exceed it, so that Route may add only a `game-director` scope cut or an Owner cost escalation; planned steps may still be opened.

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Diagnose | game-designer | diagnose-experience | done | 02-game-designer-to-studio.md |
| 2 | Decide | game-director | make-decision | skipped (no option changes dash rules or direction) | — |
| 3 | Design | game-designer | write-design-spec | done | 04-game-designer-to-studio.md |
| 4 | Build | gameplay-engineer | implement-change | done | 08-gameplay-engineer-to-studio.md |
| 5 | Verify | qa | verify-change | done (fail at 30 FPS; spec questions) | 10-qa-to-studio.md |
| 6 | Design (return) | game-designer | write-design-spec | done (D-029) | 12-game-designer-to-studio.md |
| 7 | Build (fixes) | gameplay-engineer | implement-change | done (partial; comparison not possible) | 14-gameplay-engineer-to-studio.md |
| 8 | Verify (re-check) | qa | verify-change | open | 15-studio-to-qa.md |
| 9 | Play | playtester | playtest-session | open (parallel with 8) | 16-studio-to-playtester.md |
| 10 | Review | game-director | review-outcome | planned | — |

## Route changes

After Build (14, partial): the legacy rule path now prints the refusal with no game change. Nothing else is missing for the Role, and the before/after comparison cannot be made, so QA does an after-only check and lists it as unverifiable. QA (15) and a fresh Playtester (16) open in parallel. The budget runs out after them.

## Next action

Start Steps 15 and 16 in parallel: `qa` from `15-studio-to-qa.md` and `playtester` from `16-studio-to-playtester.md`, both addressing the result to `studio`. The next Route waits for both. If the budget is used by then, it may open Review as a planned step or add only a `game-director` scope cut.

Message to the Owner (ja): エンジニアの修正が完了しました。ルール操作でダッシュが拒否されたときの表示と説明文を更新し、既存の試験180件は成功しています。次にQAによる再検証と、実装を知らないプレイテスターによる体験確認を並行して行います。操作回数の予算（17）はこの2つで使い切るため、その後は範囲を絞るかご相談します。

## Outcome

(open)
>>>END

<<<FILE @log-recent
## 007-route · 2026-10-23

Status: active. Open: 07-studio-to-gameplay-engineer.md.

After Build (06, partial): the engineer lacked the source files, and the spec is fine. Build goes back to the same Role with `game.py`, `run_driver.py`, `session.py` and the tests in the Load list. No stage added and no QA yet, because nothing was built.

## 009-route · 2026-10-23

Status: active. Open: 09-studio-to-qa.md.

After Build (08, done; Build check 173 tests OK): the result fits the plan, so Verify follows with no added stage. The QA Handoff omits the Sender assessment and asks QA to judge the public-driver picture difference and Q3–Q5, Q7, Q8 by observation.

## 011-route · 2026-10-23

Status: active. Open: 11-studio-to-game-designer.md.

After Verify (10, fail): the failures come from an ambiguous spec, not a build defect, so the return rule sends it to Design, not Build. Design is reopened for the 30 FPS tolerance, public-driver pictures, rule-driven refusals and the Q8/Q12 evidence. Build and re-Verify are tentative, and Play is held until the rulings are in.

## 013-route · 2026-10-23

Status: active. Open: 13-studio-to-gameplay-engineer.md.

After Design (12, done): the rulings fit the plan. Only a small Build is needed (legacy rule-driven refusal print, manual text). No timing change, so no Decide or Plan. Verify and Play become parallel after Build. Budget will run out before Review; a scope cut may be needed.

## 015-route · 2026-10-23

Status: active. Open: 15-studio-to-qa.md, 16-studio-to-playtester.md.

After Build (14, partial): the legacy rule path now prints the refusal with no game change. Nothing else is missing for the Role, and the before/after comparison cannot be made, so QA does an after-only check and lists it as unverifiable. QA (15) and a fresh Playtester (16) open in parallel. The budget runs out after them.
>>>END

<<<FILE goals/G-003-dash-availability-clarity/17-qa-to-studio.md
---
kind: handoff
goal: G-003
seq: 17
from: qa
to: studio
stage: Verify (re-verification against the D-029 spec)
outcome: question
---
# 17: qa → studio — Dash availability re-verification: no failure found in what I could run; verdict is NOT pass (unverified items and one spec gap)

## Task

Decide how to close the unverified items listed below and route the one spec gap (public-driver periodic picture timing) to `game-designer`. Verdict for G-003: **not pass**. No criterion I could check failed. Several criteria were not observed by me and are not counted as pass.

## Context

Goal G-003: the Owner finds it unclear when dash can be used again. This is the re-verification after the D-029 rulings and the fix Build (handoff 15). All evidence comes from the current build in `repo/`, checked against `design/dash-availability.md`. Two run rounds were used: tests, play, trace, and one bots attempt that failed on script syntax. The "before" build does not exist, so no before/after comparison was made.

## Findings

### Results per criterion

**Passed, with evidence**

| Criterion | Result | Evidence |
|---|---|---|
| Full test run | **PASS**: `python3 -m unittest discover -s tests` → `Ran 180 tests … OK`, exit 0. | Test run. The inventory lists `tests/test_dash_refusal.py` (F 08), run as 8 tests: 5 in `RefusalSourcesTest`, 1 in `GridTest`, 1 in `TimingTest`, with ids 076–082. |
| P1–P5, 60 FPS (script P) | **PASS** | Run P60. Pictures before 0.6 s end `dash: ready`. 0.600 `you dash right — usable again in 0.9 s`. 0.700 `dash not ready — 0.8 s left (dashing)`. The 1.00 s picture ends `dash: 0.5 s`. 1.000 `… 0.5 s left`. 1.400 `… 0.1 s left`. |
| P1–P5, 30 FPS | **PASS** | Run P30. The same text and numbers appear. |
| P6, 60 FPS | **PASS** | P60: `dash ready` at 1.450, followed by a picture ending `dash: ready`. The 1.50 picture shows ready. 1.500 `you dash right`. |
| P6, 30 FPS (0.90 s) | **PASS** | P30: `dash ready` at 1.500, followed by a picture ending `dash: ready`. The 1.50 picture shows ready. The press at 1.5 prints `you dash right`. |
| P7 / Q1 / Q2, 30 FPS | **PASS** | P30pre (dash at 0.6, presses at 1.46 and 1.5): 1.467 `dash not ready — 0.1 s left`, 1.500 `dash ready`, then accepted at 1.500. That is 0.900 s start-to-start, one frame earlier is refused. T30 trace: `dash_end` t=0.867, `dash_ready` t=1.500, so `dash_ready` is dash_end + 0.633, which is +1 frame and within ±1 frame (QA 10 saw the same). |
| 60 FPS press at 1.433 / 1.450 (also P7, Q1) | **PASS** | E60: 1.433 `dash not ready — 0.1 s left`, 1.450 `dash ready`, then `you dash left` at 1.450. T60 trace: `dash_end` 0.850, `dash_ready` 1.450 (+0.600 exactly). |
| P10 (reading rule), as far as observed | **PASS** (observed only) | In P30, P60, E60, P13leg and EVp, every refusal shows a time and every acceptance follows `dash ready`, with no case of "ready" shown before a refusal. Rounding was checked against trace waits in T13leg and EVt: wait 0.55 → `0.6`, 0.40 → `0.4`, 0.6167 → `0.7`, 0.4667 → `0.5`. |
| P13 legacy route, dash action | **PASS** | P13leg (`when nothing within 20 then dash right` plus `when text "not ready" then move up`): every refusal prints `dash not ready — <R> s left`, with ` (dashing)` while active and no suffix during cooldown. The `P` row climbs 4→3→2→1→0 after refusals, so the text rule fires. T13leg trace confirms the `ignored` refusals. No `(nothing happens)` appears. |
| P13 public driver, dash action | **PASS** | P13pub: the same lines appear with the driver's usual event picture after each message. `P` moves up after refusals, so the text rule fires. |
| P13, different action type (`dash toward`), both routes | **PASS** | P13legAside (legacy) and P13pubAside (`mode room`) both print `dash not ready — 0.7 s left (dashing)` and the cooldown refusals at 0.150, 0.300, 0.450 and 0.600. Legacy has no extra picture and the driver prints one. This separates route from action type. |
| Q12 as reduced by D-029 | **PASS** (the reduced check only) | R5leg: the first line is exactly `note: legacy route — boss status and messages are incomplete; add "mode room" for the full boss display`, and every picture carries the dash field. |
| Event identity, player view vs trace view (after-only) | **PASS** on the scripts compared | E60 vs T60 and EVp vs EVt: the sequence of dash, `dash_end`, refusal (with wait) and `dash_ready` events, and their times, agree between views. Trace lines are stamped post-step, one frame after the player-view time. The only difference is the display-only `quiet: True` on non-dash `ignored` events, as in EVt `attack recovering`. Refused dashes from rules carry no `quiet` (T13leg). This compares two scripts, not the whole game. |
| P12 scripted (no dodger bot) | **PASS** for these runs only | EVp (legacy room 3, 30 FPS): every live picture has the field, and `dash ready` follows each dash (3.033→3.933, 6.700→7.600, 7.833→8.733, 10.267→11.167). R5pub (`mode room`, room 5, 30 FPS): every picture has the field, with `dash ready` at 1.500 and 2.400 after dashes at 0.6 and 1.5. R5leg (legacy room 5, 60 FPS): ready at 1.450 and 2.350. |
| Q9 (partial) | Observed | Field present in legacy `room empty`, room 3 and room 5; `mode room` `room empty` and room 5 (boss). The legacy room-5 note line is kept. |

**Observations (reported, not judged)**

- P30edge used `1.467` as a script time. At 30 FPS frame 44 is t=1.46667, which is before 1.467, so that press ran on frame 45 at 1.500 together with the 1.5 press. That script therefore did not test "one frame earlier". P30pre (1.46) did.
- In `mode room`, the periodic pictures after an event picture follow the 0.5 s cadence from the last picture. In P13pubAside they appear at 1.350, 1.850, 2.350 and 2.850 after the `dash ready` picture at 0.850. In the legacy route they stay on the fixed grid; test `GridTest` covers legacy only. `public-driver.md` says "Default player scheduling retains the existing half-second cadence after event pictures", but spec 3.5 and Q8(b) say "the fixed 0.5 s grid including after dash event pictures". See Open questions.
- In the public driver a rule produces one refusal message and one picture per rule action, about 6 per second (P13pub). This is accepted under D-029.

### Not verified (not counted as pass)

| Item | Why | What it needs |
|---|---|---|
| Q5 (room-entry reset, `mode run`) | Run Q5a had no usable result. It was one trace run with a 15 s limit, and the output was truncated. Its summary shows only room 1 cleared at run time 4.35 s. The second run (dash at k − 0.25 with a queued swipe) was not made. | A trace run of the second script with `dash_ready` and entry lines readable. This needs a bounded output (short limit, or a smaller view). |
| Q7 (bot-run consistency) | The bots attempt failed on script syntax (B1: `script line 1: cannot read 'dodger room 3 fps 60'`, so there was no run and no `bots.py` header). Dodger traces for rooms 3 and 4 over 60 s and a `room 5` run were not produced. | `bots.py` script lines are `bots …`, `rooms …`, `fps …`, `limit …`, `hearts …`, `mode …`, `log on` (from the usage text). Plus trace-view dodger runs, which only the generated `public_script` can provide. |
| P12 via the public replay scripts (dodger) | Not run. The scripts come from `tests.test_split_c.public_script`, and my means cannot generate them. Only scripted rooms 3 and 5 were run. | A step able to produce `run30.txt` and `run60.txt` (see `repo/public-driver.md`) and read both views. |
| P8, P9, P11 | No script of mine had a no-dash hit, a hit-stun press, or a wind-up near the player at the right time. In R5pub the room-5 hit at 3.933 shows `dash: 0.3 s` and the run ended before the stun ended. In EVp wind-ups occurred with dashes working, but P11 was not isolated. Unit tests exist (`test_hit_stun_refusal_reason`, `test_no_dash_ready_without_a_dash`, `test_state_matches_press`) and passed. I did not read them. | Short scripts: a hit with no dash; a dash then a hit then a press at +0.3 s; a grub wind-up scripted near the player. |
| P13, attack-refusal half (both routes) | No run of a held attack rule (for example `when nothing within 20 then attack`) on either route. Only the unit test `test_rule_attack_that_does_nothing_stays_quiet_on_legacy` covers it (legacy only, and I did not read it). Public driver: unobserved. | Two short play runs, one per route. |
| Q3, Q4, Q6, Q10, Q11 | Not run by me. Unit tests for Q3, Q4 and Q11 exist (`test_a_hit_does_not_change_the_cooldown`, `test_attack_recovery_does_not_block_a_dash`, `test_text_rule_on_dash_ready`). The pause test (`test_pause_freezes_dash_and_queued_attack`) is in the suite; I did not read it. | Short scripts, or accept the tests. |
| Q9 gaps | Legacy rooms 1, 2 and 4, and `mode room`/`mode run` rooms 1–4, plus clear and terminal screens without the field, were not observed. `test_terminal_picture_has_no_field` exists. | Optional player-view scripts. |
| Q8 (a) recorded numbers and (b) | (a): only the suite's own printouts exist (dodger room results and dash counts at 30 and 60 FPS, e.g. room 1 clear 6.63 s at 30 and 9.62 s at 60). I did not compare them with an earlier handoff, because no earlier numbers are in this packet. (b): the legacy grid and event order held in the runs. The public driver is the spec gap. Hence Q8 is unverifiable beyond the suite. | Recorded numbers from earlier handoffs, or an explicit acceptance of the suite alone. |
| Q12 remainder (L1 comparison) | No baseline (D-024). | Cannot be done. |
| Before/after of timing (27 and 51 frames) | The "before" build is gone, so the claim that timing is unchanged cannot be shown. Only the frame-quantized values were checked: 51 frames at 60 and 27 at 30 (`test_start_to_start_frames_unchanged` passes). | Cannot be done. |
| Real keyboard or gamepad | Not covered. Only scripted text runs were used. | — |

### What my means cannot show

I ran scripts through `play.py` and the test suite only. I cannot see human clarity, real input devices, a baseline, or runs that need the generated replay scripts. I did not read the test bodies, only their names in the inventory.

## Decisions already made

- D-028: the dash indicator is shown on the legacy route too (including room 5). The behavior observed matches.
- D-029: 30 FPS tolerance (0.90 s, ready at 1.500 for a dash at 0.6 s), public-driver pictures after dash messages, rule-driven refusals print, and evidence without a baseline for Q8 and Q12. The observed results agree with items 1–3.

## Constraints

- Dash rules and timing must stay unchanged. Both 30 and 60 FPS apply.
- QA does not fix, widen scope or decide intended behavior. The grid question below is a spec question.

## Open questions

1. **Source ids (from handoff 15).** Public `summary:` blocks show `source_id: 3951a3656940`, and the test run prints `3951a3656940` (evidence and D022 lines, `SPLIT_C`). The `bots.py` run (B1) failed before any header was printed, so I have no bots id to report. No id is printed by the legacy `play.py` runs. Earlier files cite `b62005468da6` and `aa28af2ce710`; neither appears in this round. I cannot tell whether the ids are the same kind, because I saw only one value.
2. **For `game-designer` (spec gap).** In the public driver the periodic pictures re-start their 0.5 s cadence after each event picture (1.350, 1.850, … after the `dash ready` picture at 0.850). Spec 3.5 and Q8(b) say the fixed grid, including after dash event pictures. `public-driver.md` says the cadence is retained after event pictures. Which text governs for the public driver? Whether this behavior predates the Goal cannot be shown.

## Expected output

The Studio:

1. Routes open question 2 to `game-designer`.
2. Decides whether to give QA one more round for the unverified items. The most valuable are Q5, Q7 and P12 via the replay scripts, which need generated scripts or a repo-side runner; the short P8/P9/P11 and attack-rule scripts are cheap. Or it accepts the listed items as unverifiable.
3. Keeps the Q8 and Q12 remainders and the no-baseline timing claim as explicit unverifiable items in the Review. Not a pass.

Reproduction commands for the checks above (no failure to reproduce):

```text
python3 -m unittest discover -s tests
python3 play.py --view player P30pre.txt   # room empty, fps 30, 0.6 dash right, 1.46 dash left, 1.5 dash left, end 3
python3 play.py --view player E60.txt      # room empty, fps 60, 0.6 dash right, 1.433 dash left, 1.45 dash left, end 3
python3 play.py --view trace  T60.txt      # same script as E60
python3 play.py --view player P13leg.txt   # room empty, fps 60, when nothing within 20 then dash right, when text "not ready" then move up, end 3
python3 play.py --view player P13pub.txt   # mode room, room empty, fps 60, limit 3, driver-limit 4, same two rules
python3 play.py --view player P13pubAside.txt   # mode room, room empty, fps 60, limit 3, driver-limit 4, spawn grub 10 4, when see g within 3 then dash toward
python3 play.py --view player R5pub.txt    # mode room, room 5, fps 30, limit 4, driver-limit 5, 0.6 dash right, 1.5 dash left
```

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/verify-change.md
- Project: design/dash-availability.md, repo/public-driver.md, repo/play.py, repo/tests/test_dash_refusal.py, project.md#constraints
- Decisions: decisions/D-028-dash-indicator-on-legacy-route.md, decisions/D-029-g003-spec-rulings.md
- Previous handoff: goals/G-003-dash-availability-clarity/15-studio-to-qa.md
>>>END

<<<FILE goals/G-003-dash-availability-clarity/18-playtester-to-studio.md
---
kind: handoff
goal: G-003
seq: 18
from: playtester
to: studio
stage: Route
outcome: done
---
# 18: playtester → studio — Observation report: movement and dash in fights, 60 and 30 FPS

## Task

Read the player-side observation report below and route it. Experience issues go to the game-designer and defects to QA.

## Context

Goal G-003 (dash availability clarity). Handoff 16 asked me to play the current build (0.6-g002-public-32) as a player, using only the game's output and `repo/manual.md`. The focus was how I use movement and dash during fights and what I can tell about my options at each moment. I played mainly at 60 FPS and ran one session at 30 FPS.

## Findings

### Method

- I played by input automation only: a written script run through `python3 play.py --view player {script}`. I did not play live.
- I did not use the trace view and did not read source, tests or design documents.
- The same script ran twice, once with `fps 60` and once with `fps 30`. Each was a normal run (`mode run`) that started in room 1.
- Only room 1 was seen. I never cleared it, so I never saw rooms 2–5 or the boss.
- Timed inputs and the three reaction rules were fixed in advance. I did not adapt to the screen mid-run. When a grub reared back, my script did not dodge it on purpose. That means this report says nothing about how dodging with the dash feels in practice.
- Scripts used, identical except for the `fps` line:

```text
mode run
fps 60            # second run: fps 30
limit 40
driver-limit 45
0 move left
0.5 stop
1.0 dash right
1.5 dash right
2.0 move up
2.5 stop
2.5 attack
3.0 dash left
3.9 dash left
4.5 attack
5.0 move right
6.0 stop
6.0 dash up
when see g within 3 then face
when see r within 1.4 then attack
when see * coming within 1.5 then move aside
```

### Session summary

- Both runs ended in death in room 1, at 11.417 s (60 FPS) and 11.033 s (30 FPS).
- Each run had 3 hits ("hits": 3) and 2 swipes ("attacks": 2). Both swipes were "you swipe: miss". No enemy was ever defeated.
- The room started with three grubs (`g`). They kept coming and lunging, and I was hit once about every 1.3–1.7 s once they reached me in the top-left corner.

### What the dash display showed (concrete moments)

1. **Status line.** Every picture ended with `dash: ready`, `dash: active` or `dash: 0.4 s`. I could read my dash state at a glance in every picture.
2. **Dash used.** At 1.0 s I got `you dash right — usable again in 0.9 s`. The next picture, at 1.017 s, showed `dash: active`.
3. **Early dash refused.** At 1.5 s, 0.5 s after the dash started, I pressed dash again and got `dash not ready — 0.4 s left`. The picture showed `dash: 0.4 s`. I understood immediately why nothing happened.
4. **Dash ready message.** The game printed `dash ready` and a picture at the moment it returned.
   - At 60 FPS this was 1.850 s, 0.85 s after the dash.
   - At 30 FPS this was 1.900 s, 0.90 s after the dash.
   - The dash message says "usable again in 0.9 s" at both frame rates, but at 60 FPS the real wait was 0.85 s. I did not notice the difference during play.
5. **Chained dashes.** A second dash 0.9 s after the first worked at 60 FPS (3.0 → 3.9, with `dash ready` at 3.850) and at 30 FPS (3.0 → 3.9, `dash ready` at 3.900, same instant as my press). I did not try timings between 0.85 and 0.9 s, so I can't say where the edge feels.
6. **Countdown steps.** Later pictures counted down in tenths, for example `dash: 0.4 s` at 4.417 and `0.3 s` at 4.517 after a dash at 3.9, then `dash ready` at 4.750. Between half-second pictures I only knew the time from the last picture, as the manual says. The exact return was always announced.
7. **Dash end.** I saw `dash: active` only in the picture right after a dash started. There was no separate message when the dash ended.

### Dodging with the dash

- At 3.0 s a grub reared back about 10 tiles to my right, with a line pointing at me and 0.5 s to the lunge. I dashed left, and no hit followed.
- At 3.9 s another grub had 0.10 s left on its warning, with a line pointing up and right. I dashed left, and no hit followed.
- I cannot tell from the output whether the dash or the distance was what saved me, because no lunge message or picture appeared.
- All three hits came from lunges I did nothing about. My script did not use the dash in those moments, so I can't say if I could have dodged them.

### Where I was unsure or confused

- **Dash count after a hit.**
  - After each hit the status line showed a dash countdown. At 8.750 s it read `dash: 0.3 s`, then 0.2, then 0.1, then `ready` at 9.517 s.
  - I had not used the dash since 6.0 s, so it should have been ready.
  - The manual explains this as hit-stun, but on screen it looks like a cooldown. No `dash ready` message appeared afterwards. I would not know from the screen alone that this was hit-stun and not a spent dash.
  - It happened after all three hits at 60 FPS and after the two non-fatal hits at 30 FPS.
  - Impact: moderate. In the moments right after a hit, when I most want to escape, the display told me the dash was unavailable for a reason it did not give.
- **"(nothing happens)" lines.**
  - After a hit I got two `(nothing happens)` lines at the same time (for example 8.850 and 9.000 s, and again at 10.200 and 10.350 s).
  - They gave no reason and no mention of dash or of what was refused.
  - I do not know which action they came from. They appeared at the same time as my reaction rules were active. Impact: minor to moderate, because they were unexplained noise in the middle of a fight.
- **Grub warning timing.** The cue showed `0.50 s to the lunge` on the first picture, and the line pointed at where I stood. The warning is short, and pictures only come when the warning starts and every half second. So the later countdown (for example `0.12 s to the lunge`) was usually already stale when I read it. I could not tell, from the pictures, how late was too late for a dash.
- **Guessing.** I had to try the early dash at 1.5 s to find out whether the dash worked in the ready window. I did not need to guess about the display of ready versus active.

### Positives

- The `dash: ready / active / N s` field was always there, and the numbers matched the announced return times.
- The refusal text `dash not ready — 0.4 s left` told me exactly how long to wait.
- `dash ready` was announced at the exact moment, which I could rely on instead of the half-second pictures.

### Not observed

- Live, adaptive play: dodging on purpose with the dash, and the dash against a runner, a brute, a spitter or the boss.
- A swipe that hit or cancelled a grub, and any kill.
- Dash status on the clear or end screens (the manual says there is none).
- Any gamepad play. The script format cannot show how the dash feels on a pad.
- The edge between 0.85 and 0.9 s at 60 FPS.
- How the 60 versus 30 FPS dash timing feels during real play. All I have are the printed times.

## Decisions already made

None.

## Constraints

- Everything above is what a player could see in the game's output and the manual. I did not guess at causes or at how the game is built.
- The runs were scripted and non-adaptive, so impressions of feel are limited to what the text showed.

## Open questions

- Should the post-hit refusal (hit-stun) be shown differently from a spent dash? The status line shows the same countdown for both.
- Should the unexplained `(nothing happens)` lines be explained? They appeared in the same moments.
- A further session with reaction rules that dash on a warning (for example `when text "rears back" then dash aside`) would show whether the dash works as a dodge. I did not run one.

## Expected output

Route the experience points (hit-stun shown as a dash countdown, unexplained `(nothing happens)`, stale countdown numbers) to the game-designer. If the `(nothing happens)` lines are judged a defect, route that part to QA. The next step is the Studio's call.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, repo/manual.md
- Decisions: none
- Previous handoff: goals/G-003-dash-availability-clarity/16-studio-to-playtester.md
>>>END
