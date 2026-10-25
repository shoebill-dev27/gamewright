# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-first-playable-run/03-technical-director-to-gameplay-engineer.md
next_seq: 4
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha cb0825a94f02; run through the project's run commands)
log: last 2 of 2 entries in @log-recent; the full history is goals/G-001-first-playable-run/log.md
goal_budget: 4 of 19 operations used

## You may write

- goals/G-001-first-playable-run/goal.md
- goals/G-001-first-playable-run/03-technical-director-to-gameplay-engineer.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- project.md: only in the Route that closes the Goal, and only its ## Current state (at most 1,500 characters)
- goals/G-001-first-playable-run/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 04
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

Concept only. Nothing has been designed or built: `repo/` holds only a README. There are no
design documents and no Decisions yet.

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
design/acceptance-criteria.md
design/game-spec.md
goals/G-001-first-playable-run/01-studio-to-game-designer.md
goals/G-001-first-playable-run/02-game-designer-to-technical-director.md
goals/G-001-first-playable-run/03-technical-director-to-gameplay-engineer.md
goals/G-001-first-playable-run/goal.md
goals/G-001-first-playable-run/log.md
project.md
repo/README.md
>>>END

<<<FILE @decision-titles
decisions/D-001-classic-scripts-shared-rules.md — D-001: Shared code is plain classic-script modules (UMD style), not ES modules
>>>END

<<<FILE goals/G-001-first-playable-run/goal.md
---
kind: goal
id: G-001
project: ember-hollow
status: active
created: 2026-10-26
budget: 19
---
# G-001: First complete playable run in the browser

## Owner request

> このコンセプトで、最初から最後まで通して遊べる版を作ってほしい。ブラウザで遊べるようにしてほしい

## Interpretation

Success condition: a person opens `repo/index.html` straight from the file system in a browser and can play one whole run with keyboard or mouse. The run starts on floor 1, passes through all five floors, and ends in one of the ways the vision names: beating the floor-5 creature (win), dying, or the ember going out. No setup, server or developer step is needed. The vision's pillars hold in that run: readable threats, light as the resource, a short seeded run (same seed gives the same run).

The team-side means from `project.md#constraints` also ship, because verification depends on them: `node play.js {script}`, `--trace`, `node --test`, and `repo/manual.md` (the script format and everything a player is told).

Out of scope (not requested): saving or resuming runs, meta-progression between runs, sound, mobile or touch layouts, network features, content beyond what one complete five-floor run needs, and any change to the vision or pillars.

## Unknowns

- Observe: skipped. No build exists and nothing is reported broken or off.
- Diagnose: skipped. There is no problem to explain.
- Decide: skipped. Design stayed inside the vision and Goal scope and raised no direction, priority or scope choice. Reopens only if Plan finds the spec too costly and scope must change (then `game-director`).
- Design: done (spec and 30 acceptance checks in `design/`). Reopens if Plan or Build sends back a spec question. Balance is unverified; Play must report it.
- Plan: open. Cross-system work (shared rules core for browser and Node, deterministic seeded generation, floor generator guarantees, threat marking consistent with creature actions, browser renderer, script player and trace, bulk-seed test support for checks 14, 21, 23, 26). Technical approach and sequencing are the `technical-director`'s.
- Build: planned. The game must be created from scratch.
- Verify: planned. QA against the acceptance criteria through the scripts and tests; Art Director visual review in parallel (grid readability, threat clarity).
- Play: planned. A Playtester plays from `repo/manual.md` and the player profile only.
- Review: planned. `game-director` judges whether the intent was met and names the next issues.

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Design | game-designer | write-design-spec | done | 01-studio-to-game-designer.md |
| 2 | Decide | game-director | make-decision | skipped | — |
| 3 | Plan | technical-director | technical-plan | open | 02-game-designer-to-technical-director.md |
| 4 | Build | gameplay-engineer | implement-change | planned | — |
| 5a | Verify | qa | verify-change | planned | — |
| 5b | Verify (visual) | art-director | visual-review | planned | — |
| 6 | Play | playtester | playtest-session | planned | — |
| 7 | Review | game-director | review-outcome | planned | — |
| 8 | Next | studio | — | planned | — |

## Route changes

After Design: it fits the plan. Decide dropped (skipped): the designer resolved all ambiguities inside the vision and scope. Plan opens with the Design handoff; its Load list was corrected to the existing skill `technical-plan`.

## Next action

Start step 3: `technical-director` with `goals/G-001-first-playable-run/02-game-designer-to-technical-director.md`. Its plan goes to `gameplay-engineer`.

## Outcome

(open)
>>>END

<<<FILE @log-recent
## 001-intake · 2026-10-26

Status: active. Open: 01-studio-to-game-designer.md.

Intake: initial route. Observe and Diagnose skipped (no build, no problem). Decide tentative: only if Design needs a direction, priority or scope choice. Budget 19 = 7 planned steps x 2, plus 4 for one return, plus 1 for Intake.

## 003-route · 2026-10-26

Status: active. Open: 02-game-designer-to-technical-director.md.

After Design: it fits the plan. Decide dropped (skipped): the designer resolved all ambiguities inside the vision and scope. Plan opens with the Design handoff; its Load list was corrected to the existing skill `technical-plan`.
>>>END

<<<FILE goals/G-001-first-playable-run/03-technical-director-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 3
from: technical-director
to: gameplay-engineer
stage: Build
outcome: done
---
# 03: technical-director → gameplay-engineer — build the five-floor Ember Hollow run from the plan below

## Task

Build the first complete playable Ember Hollow exactly to `design/game-spec.md` and `design/acceptance-criteria.md`. This means the shared rules code, the seeded floor generator, the text runner `play.js` (with `--trace`), the browser page, the tests, and `repo/manual.md`. Follow the structure and order of work in Findings. Do not change the spec. Send spec questions to `game-designer` through the Studio.

## Context

G-001: the Owner asked for the concept to be playable from start to finish in the browser. Design is done (spec and 30 checks). This is the Plan step's output; Build, Verify, Play and Review follow. `repo/` is empty (README only). The Plan did not run anything: there was no code to run tests or traces against. Everything below is reasoning, not measurement. Balance is unverified; the Play step reports it.

## Findings

### 1. Approach in one paragraph

One pure, deterministic rules engine holds all game state in plain JSON-serializable objects. It has one entry point, `step(state, action)`, and one read function, `view(state)`. The view function computes visibility, threat marks and the HUD data. `view` feeds both the text renderer (`play.js`) and the page renderer, so the two cannot disagree (spec section 9: "both must give the same information"). There is no running random generator during play. All randomness is in floor generation, from a generator seeded by hash(seed, floor, attempt). Creature behaviour is fully deterministic from state, so the same seed plus the same commands always gives the same run.

### 2. Affected systems and file structure (all in `repo/`)

```
index.html          loads src/*.js as classic scripts, then page.js (D-001)
play.js             CLI: node play.js [--trace] <script>   (script format: see 5)
manual.md           script format, seed choice, controls, how to read the output
src/rng.js          string/int seed -> 32-bit hash; mulberry32-style PRNG; sub-seeding by (seed, floor, attempt)
src/floorgen.js     generateFloor(seed, n) -> {w,h,tiles,start,stairsDown,braziers,items,creatureSpawns}
                    validateFloor(floor, n) -> list of violated guarantees (used by the generator AND tests)
src/game.js         newRun(seed), step(state, action), creature planning, ember, items, end states
src/view.js         visibility, threat marks, view(state) -> render model
src/textview.js     renderFrame(view) -> text lines (used by play.js and tests)
src/script.js       parseScript(text) -> {seed, commands}; runScript(seed, commands, opts) -> frames/log
src/scenario.js     fromAscii(rows, opts): build a hand-made state (map, E, HP, creatures, items) for tests
src/page.js         browser only: canvas or DOM grid, keyboard and mouse, summary screen
tests/*.test.js     node --test (see 4)
tests/bot.js        threat-following bot using only the public API (see 4)
```

Every `src` file except `page.js` must load under both Node 20 and the browser (D-001: no import/export, no `window`/`document`, no `Date`/`Math.random`).

### 3. Rules module design points

- **State**: `{seed, floor, turn, hp, ember, inv[4], player{x,y}, floorData, lit[], seenTiles (per floor), creatures[], messages[], end|null, defeated, stats}`. Creatures have fixed ids in placement order. This is the tie-break order for the creature phase (spec 11).
- **Turn order, exactly as in spec 2/3/8/11**: player action -> effects (brazier, item pickup, oil/salve, attack) -> win check (Gloom at 0 HP) -> dimming (1, or 2 near the Gloom) -> ember check (0 = end, creatures do not act) -> creature phase in id order -> HP check. Stairs: dim, then the new floor starts with no creature phase. Refused actions (wall, refused item) return `{turnConsumed:false}` and change nothing, including the turn counter and E.
- **Drain distance**: measure the Gloom's Manhattan distance to the player after the player's action, which is the position at the end of the player's half of the turn. If the engineer picks otherwise, record it in `manual.md` and in the Handoff.
- **One planner for creatures and threat marks (the risk the Game Designer flagged for check 14)**: write `planAction(state, creature)`, which returns an intent: `idle | move{to} | attack{damage} | crouch{line} | lunge{path} | gather{area} | slam{area} | stunned | staggered`. The creature phase executes the intents. `view()` marks a threat when `planAction` on the current state returns an intent that damages the player (attack, lunge ending in line, slam on a marked area, crouch with its line). It must not use a second copy of the conditions. A unit test asserts this by sampling many states.
- **Hound lunge, flare, stun and stagger** are state fields with turn counters (`stunned:n`, `crouching`, `staggered:n`, `marked area`), decremented in a fixed place in the creature phase. Write each rule in its own function with a comment citing the spec section.
- **Pathing**: BFS over walkable tiles, neighbours in the order N, E, S, W. This gives the spec's tie-break. A creature counts creatures as blockers for its step but not for the path distance used for triggers, except where the spec says "walkable path". Pick one reading, document it in `manual.md` notes, and keep it consistent in `planAction`.
- **Visibility**: circle test `dx²+dy² <= (r+0.5)²` plus a wall line of sight (Bresenham or equivalent, symmetric enough that adjacent tiles and clear-line distance-2 tiles at r >= 2 are always visible). Unit-test those two guarantees explicitly. Mark seen tiles in the floor's memory grid; creatures are never remembered.
- **Gloom**: separate branch in `planAction` (stalk, gather, slam, staggered). It stays in the arena unless the player is in the arena (spec 7). The flare ignores it.
- **Messages**: keep the last 5 in state, plus an `events` list per step (for the trace and the check-12 turn log).

### 4. Floor generator, and bulk-seed support (checks 14, 21, 23, 26)

Floor generation is the riskiest part (check 23). Plan:
- Generate in attempts. Attempt k uses `rng(seed, floor, k)`. Place rooms, join them with corridors, place `<` and `>`, braziers, items and creatures. Run `validateFloor`. If it fails, try k+1 (cap about 200; if it ever caps out, throw loudly rather than ship a bad floor). Because the attempt number is a pure function of the seed and floor, determinism holds.
- Take `>` as a room far from `<` by BFS, so the 30/40-step rules are met by construction and checked by the validator.
- Brazier rule "not on the shortest path for both": use the strict test `dist(<,t)+dist(t,>) == D` (on any shortest path), so either reading of the spec is satisfied. Do the same for the "at least one item off the shortest path" rule.
- Floor 5: start room, corridor, arena of at least 14x10 holding the Gloom and 3 braziers, with the entrance at least 20 steps from `<` and the Gloom at least 8 steps from the entrance. No `>`.
- Floor n depends only on (seed, n). `generateFloor` takes nothing else, which gives check 21's cross-floor identity for free. A test asserts it by running two different command lists on floor 1 and comparing floor 2 outputs.

Bulk support (this is what the four bulk checks need):
- `runScript(seed, commands, opts)` is a pure function that returns frames, the final state, a turn log and `events`. It is the single code path for `play.js`, the tests and the bots. It makes no I/O calls.
- `tests/bulk.test.js` loops 50 seeds x floors 1-5 through `generateFloor` + `validateFloor` (check 23) and 10 seeds for layout difference (check 22). Keep it fast (a few seconds in total) so `node --test` stays usable.
- `tests/bot.js` is a bot that plays through the public API only. It reads `view(state)` with threat marks, avoids marked tiles, heads for `>`, takes braziers within about 10 steps of the path, fights what blocks the way, and fights the Gloom with the gather/dodge/stagger rhythm. Use it for check 14 (20 seeds, with the damage-after-mark assertion made on the turn log), check 26 (3 or more seeds in 250-700 turns, at least one win), and as a smoke test. If the bot cannot get a result, report that to the Studio rather than tuning numbers: balance is for Play, spec changes are for the Game Designer.
- `tests/` helpers use `scenario.fromAscii` for rules that are hard to reach by seed (check 4 at E = 30, check 5, the hound lunge, the slam, brazier flare stun, full inventory, HP 0 + E 0 tie, win with E <= 5). Do not rely on finding such situations in generated floors.

### 5. Runner, trace, script format (the build's to define; recommended shape)

Define the final format in `manual.md`. Recommended: a text file. The first non-comment line is `seed <integer or text>`. Then command tokens separated by whitespace or newlines: `w a s d` (or `n e s w` if preferred) for move/fight, `.` for wait, `1`-`4` to use a slot. `#` starts a comment. No seed line = a documented default seed. `node play.js <script>` prints, for each turn, the frame from `renderFrame(view)`. This covers the map, HUD (E number and bar, r, "dims n/turn"), HP, floor/turn, inventory, visible creatures with type/HP/state/position, threats marked `!`, the last 5 messages and the seed. At an end state it prints the summary lines (result, floor, turns, defeated, HP, E, seed) and ignores later commands (check 20). `--trace` adds, per turn: each creature's id, position, state, intent and path distance; the threat list with reason; E, drain rate, RNG-free confirmation (no state besides the above); events with damage sources. Trace is for the team; the text frame is for the player.

### 6. Tests (what is automated, what QA checks by looking)

Automated by `node --test`: checks 1-25 (numbers, rules, determinism, generator) and check 26 via the bot. Each test names its check number in its title. Page checks 27-30 are by looking (QA/Art Director). Also give the page a testable seam: have `page.js` call only `step`, `view` and the new-run function, and put no rule logic in it, so QA can trust that what the page shows is what the text shows. The 30-check list is not complete without a human opening `index.html`; say so honestly in the next handoff.

### 7. Ordered tasks

1. **Skeleton and ground rules** (everything depends on it): `rng.js`, `scenario.js`, `game.js` core turn loop with player actions, ember/dimming/radius table, items, brazier (rekindle + flare hook), stairs, end states, 4-slot inventory. Tests for checks 1-8, 19-20 (partial), 24-25.
2. **Floor generator and validator** (riskiest, do it early): `floorgen.js` for floors 1-5, `validateFloor`, bulk test for checks 22/23, determinism tests for 21.
3. **View and runner**: `view.js` (visibility and the two guarantees), `textview.js`, `script.js`, `play.js` with `--trace`, first `manual.md`. From here a human can play in text.
4. **Creatures**: `planAction` for moth, shade, hound; threat marks from the same planner; flare stun; tests for checks 9-14 (scenario-based) and the turn log for check 12.
5. **The Gloom**: drain, stalk/gather/slam/stagger, win, arena rules; checks 15-18.
6. **Browser page**: `index.html` + `page.js` with keyboard and mouse controls, summary screen, threat highlight, remembered vs. visible brightness, lit vs. unlit brazier, seed always shown (checks 27-30). Test by opening via `file://`; Node tests cannot show this.
7. **Bots and run length**: `tests/bot.js`, check 14 over 20 seeds, check 26. Finish `manual.md`.
8. **Final Handoff to QA** (stage Verify): list what is automated and what only a human can check, `run_tests`/`play.js` outputs the engineer saw, and any spec reading chosen.

### 8. Risks and mitigations

- **Generator guarantees fail on some seeds** (check 23): attempt loop plus validator; run the 50-seed test often. Mitigation if the geometry makes constraints incompatible: report to the Game Designer the exact seed and rule. Do not weaken a rule silently. The Game Designer's suggested first cut is floor size or brazier count, not creature behaviour.
- **Threat marks diverge from creature actions** (check 14): the single `planAction` design above, plus a sampled-states test and the bot assertion.
- **Visibility edge cases**: the two stated guarantees are unit-tested; the exact algorithm is the engineer's choice.
- **`file://` page**: no modules, no fetch, no storage requirement (D-001). Do not use `fetch`/XHR.
- **Determinism leaks**: no `Math.random`, `Date`, object-key order dependence on user input, or locale-dependent formatting in `src/` (except `page.js`). The test for check 21 compares byte-identical output of two runs.
- **Run length** (check 26) may land outside 250-700 turns with the first-estimate numbers. This is a balance result: report it, do not tune the spec's numbers yourself.
- **Test speed**: keep `node --test` to seconds; bots run fewer seeds in the default run.

### 9. Parallelization

Not parallel. One engineer owns the shared state/step API, and tasks 2-5 and 6 all depend on it. Isolated workspaces and merges would cost more than they save for one build of this size. The page (task 6) could be split off after the API in task 3 is stable, but the Studio should only do that if the schedule demands it.

### 10. Spec readings and one spec question (found in planning)

1. **Possible conflict in check 14 and spec section 9.7 (needs a Game Designer answer; routed by the Studio).** A threat mark means "can hurt the player at its next action". A moth that is not adjacent has no mark. If the player steps next to it, the moth attacks in the same turn's creature phase, so damage comes from a creature that was visible but not marked in the previous output. The same applies to an adjacent step toward a shade at r = 2. Read literally, check 14 ("no damage from a creature that was not shown and marked before it hit") would fail with correct rules. **Build should implement the rules as written and make the check-14 test assert the narrowest reading that can be defended: every damaging creature was visible in the previous frame, and it was threat-marked there unless the player's own move ended adjacent to it (or inside its reach).** The test must log both cases so QA sees the split. Verify must not call check 14 final until the Game Designer confirms the wording or revises the spec (for example by marking "would strike if you step adjacent" tiles). The Studio should send this question to `game-designer` before Verify.
2. Small readings to settle and write in `manual.md` (no spec change needed): the exact drain-distance moment (3 above); the path-distance rule for triggers with creatures as blockers (3); a stunned hound already crouching has its crouch cancelled (spec 3 says so); descending from an arrival tile never triggers creature actions (spec 2).

## Decisions already made

- D-001: shared code is plain classic-script (UMD) modules, no ES modules, because `index.html` must open from the file system.
- Not a Decision, only a planning choice: a single `planAction` function feeds both creature actions and threat marks.

## Constraints

- JavaScript for Node.js 20 and the browser, no dependencies, no network, no build step; rules in code shared by the page and `play.js` (D-001); `repo/index.html` opens from the file system.
- Deterministic: same seed + same commands = same run (byte-identical text). No rule uses real time or `Math.random`.
- Do not change the spec, concept, pillars or scope. Content is what the spec lists; no saving, sound or mobile layouts. Spec questions go to `game-designer` through the Studio; scope questions to `game-director`.
- The script format and seed choice are yours, defined in `repo/manual.md`, which is all a player is told. The page may choose its own seed on "new run", but it must show the seed, and the same seed must repeat the run.
- Write only under `repo/` (and the Handoff files the Studio lets you write).

## Open questions

- Spec question for `game-designer` (the Studio routes it): check 14 versus the threat-mark definition when the player steps next to a creature (see Findings 10.1). Build continues in the meantime on the reading given there.
- No question for the Owner.

## Expected output

The build in `repo/` per Findings 2-7, with `node --test` passing and `node play.js` playable. A Handoff to `qa` (stage Verify) that states: which checks are automated and passing; which only a human can check (27-30); what you ran and saw (test and trace output); the exact script format (pointing to `repo/manual.md`); the readings you chose (Findings 10.2); and anything you could not make pass, with seed and rule. If a spec rule turns out infeasible, hand back to `game-designer` with the exact question.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: as set by the Studio when routing (the Plan lists no required skill)
- Project: project.md#vision, project.md#constraints, design/game-spec.md, design/acceptance-criteria.md, repo/README.md
- Decisions: decisions/D-001-classic-scripts-shared-rules.md
- Previous handoff: goals/G-001-first-playable-run/02-game-designer-to-technical-director.md
>>>END
