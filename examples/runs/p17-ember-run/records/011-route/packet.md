# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-first-playable-run/09-gameplay-engineer-to-qa.md, goals/G-001-first-playable-run/10-game-designer-to-studio.md
next_seq: 11
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha 441c03da0488; run through the project's run commands)
log: last 4 of 4 entries in @log-recent; the full history is goals/G-001-first-playable-run/log.md
goal_budget: 10 of 19 operations used

## You may write

- goals/G-001-first-playable-run/goal.md
- goals/G-001-first-playable-run/09-gameplay-engineer-to-qa.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-first-playable-run/10-game-designer-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- project.md: only in the Route that closes the Goal, and only its ## Current state (at most 1,500 characters)
- goals/G-001-first-playable-run/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 11
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
decisions/D-002-threat-and-reach-marks.md
design/acceptance-criteria.md
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
goals/G-001-first-playable-run/goal.md
goals/G-001-first-playable-run/log.md
project.md
repo/README.md
repo/index.html
repo/manual.md
repo/play.js
repo/src/floorgen.js
repo/src/game.js
repo/src/light.js
repo/src/page.js
repo/src/rng.js
repo/src/scenario.js
repo/src/script.js
repo/src/textview.js
repo/src/view.js
repo/tests/bot.js
repo/tests/bots.test.js
repo/tests/creatures.test.js
repo/tests/floors.test.js
repo/tests/gloom.test.js
repo/tests/helpers.js
repo/tests/reach.test.js
repo/tests/rules.test.js
repo/tests/view.test.js
>>>END

<<<FILE @decision-titles
decisions/D-001-classic-scripts-shared-rules.md — D-001: Shared code is plain classic-script modules (UMD style), not ES modules
decisions/D-002-threat-and-reach-marks.md — D-002: threat marks plus reach marks on the four neighbour tiles
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
- Decide: skipped. Design stayed inside the vision and Goal scope and raised no direction, priority or scope choice. Reopens only if Plan or a spec question finds scope must change (then `game-director`).
- Design: spec and 30 checks done. Check 14 settled by D-002 (reach marks). Open: flare stun timing and hound bite at lunge distance 1 (handoff 08). Balance is unverified; Play must report it.
- Plan: done (handoff 03). Reasoning only, nothing measured.
- Build: open. First pass written (05, partial; 34 tests passed in the runtime's check, bots, generator and page unexecuted). Now applying D-002 reach marks and finishing (handoff 07).
- Verify: planned. QA against the acceptance criteria through the scripts and tests, after Build and Design 4c; Art Director visual review in parallel (grid readability, threat and reach mark clarity). Checks 27-30 need a human opening `index.html`.
- Play: planned. A Playtester plays from `repo/manual.md` and the player profile only.
- Review: planned. `game-director` judges whether the intent was met and names the next issues.

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Design | game-designer | write-design-spec | done | 01-studio-to-game-designer.md |
| 2 | Decide | game-director | make-decision | skipped | — |
| 3 | Plan | technical-director | technical-plan | done | 02-game-designer-to-technical-director.md |
| 4a | Build | gameplay-engineer | implement-change | open | 07-studio-to-gameplay-engineer.md |
| 4b | Design (check 14 question) | game-designer | write-design-spec | done | 04-studio-to-game-designer.md |
| 4c | Design (flare stun, hound bite) | game-designer | write-design-spec | open | 08-studio-to-game-designer.md |
| 5a | Verify | qa | verify-change | planned | — |
| 5b | Verify (visual) | art-director | visual-review | planned | — |
| 6 | Play | playtester | playtest-session | planned | — |
| 7 | Review | game-director | review-outcome | planned | — |
| 8 | Next | studio | — | planned | — |

## Route changes

After Build (05, partial) and Design 4b (06): check 14 is settled by D-002 reach marks, so Build continues with those changes (07). 05's two other rule questions go to a parallel Design step (08). Verify waits for both. 05 is not sent to qa. Budget is nearly used up: a further return would pass it.

## Next action

Start steps 4a and 4c, in either order: `gameplay-engineer` with `07-studio-to-gameplay-engineer.md`, and `game-designer` with `08-studio-to-game-designer.md`. The Route after both opens Verify (qa with art-director in parallel), or returns a changed ruling to Build first.

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

## 005-route · 2026-10-26

Status: active. Open: 03-technical-director-to-gameplay-engineer.md, 04-studio-to-game-designer.md.

After Plan: it fits. Build opens (03). The TD's spec question on check 14 vs threat marks opens as a parallel Design step (04); Build does not consume its answer. Verify waits for both. Skills in 03's Load set to implement-change.

## 008-route · 2026-10-26

Status: active. Open: 07-studio-to-gameplay-engineer.md, 08-studio-to-game-designer.md.

After Build (05, partial) and Design 4b (06): check 14 is settled by D-002 reach marks, so Build continues with those changes (07). 05's two other rule questions go to a parallel Design step (08). Verify waits for both. 05 is not sent to qa. Budget is nearly used up: a further return would pass it.
>>>END

<<<FILE goals/G-001-first-playable-run/09-gameplay-engineer-to-qa.md
---
kind: handoff
goal: G-001
seq: 9
from: gameplay-engineer
to: qa
stage: Verify
outcome: partial
---
# 09: gameplay-engineer → qa — reach marks (D-002) built, but not executed and two places not updated; verify with care

## Task

Verify the reach-mark change against checks 14 and 29 and spec 9.7 and 11. Run `node --test` first. Failures in older tests that assert the old marking are expected to be listed under Known gaps and sent back to `gameplay-engineer`.

## Context

G-001. Handoff 07 asked for the check-14 amendment (D-002). I could only see part of the repository, and I did not run anything in this step (no `@run` used). So this is `partial`: the code and new tests are written, but not executed by me. The runtime's Build check follows this handoff.

## Findings

What changed:
- `repo/src/view.js`: marks use E after this turn's dimming (current E minus `drainRate`). The planner context (visibility for shade fear, path distances, r) is built from the player's position at the end of the turn. New `view.reach` list: `{dir, x, y, creatures:[{id, letter, damage}]}` for each neighbour tile that has at least one mark. Each cell gets `reach` (letters). Reach comes from `planAction` with a hypothetical player position. Tiles with no mark: wall, creature-occupied, `>`, unlit brazier. Creatures orthogonally adjacent to the player or to a non-wall neighbour tile are listed even without line of sight. Creature `state` labels now come from the after-dimming planning too. No marks once `end` is set or when the ember would be 0.
- `repo/src/textview.js`: a `Danger: N (m), E (h, s)` line (or `Danger: none`) under the map; `?` on the map for reach tiles (floor tiles without an item; `!` stays the threat glyph); legend updated.
- `repo/src/page.js`: dashed orange tile highlight with creature letters for each reach entry, and a `Danger:` line, both from `view.reach` (red threat marks unchanged, so they are distinct).
- `repo/manual.md`: the final format and readings 9-10.
- `repo/tests/reach.test.js` (new): hand-made scenarios (moth, hound, shade at r=2, Wait at E=20 vs 21, unlit brazier and stairs with no mark, lit brazier with a mark, walls/creature tiles), a strict check-14 test over 20 seeds × up to 600 random-walk commands (each damage event logged as `threat` or `reach` via `t.diagnostic`), and a sampled-states test (threat flags equal the planner with the after-dimming ember).
- `STUN_TURNS` and the bite rule are untouched.

How to exercise: `node --test`; look at the diagnostics of the check-14 test; play a script such as `seed 1` with moves toward a moth and read the `Danger:` line before each step; open `index.html` (check 29 needs a human).

Known gaps (honest list):
1. I could not see `repo/play.js`, `tests/bots.test.js`, `tests/creatures.test.js`, `tests/rules.test.js`, `tests/bot.js`, so I did not replace the old check-14 assertion or the old sampled-states test there. They may still use the old rule (e.g. exempting the player's own move) or fail with the new after-dimming marks. `reach.test.js` carries the strict form, but the old assertion must be removed or replaced by whoever sees those files. `--trace` fields `markedBefore`/`steppedAdjacent`/`radiusChanged` in play.js likely still use the old meaning.
2. Nothing was run: no tests, no trace, no bot checks (14, 26), no page. The new tests may fail or reveal a rule gap; the random walk may rarely trigger a hound or the Gloom, so those cases are covered only by the hand-made scenarios (the Gloom slam by `hurtsAt` logic, untested).
3. No test for a creature shown only because it is adjacent to a neighbour tile with line of sight blocked (I did not build a reliable scenario).
4. Reading to confirm with the Game Designer: a lit brazier tile gets reach marks (the flare happens only when lighting), whereas spec 9.7 says "a brazier tile gets none". Without it, strict check 14 could not hold on a lit brazier. Easy to change in `view.js` (`t === 'B' && !litSet`).
5. Page appearance (checks 27-30) not seen.

## Decisions already made

- D-001: classic-script UMD modules.
- D-002: threat plus reach marks, after-dimming E, strict check 14.

## Constraints

- Report only what was run. No creature behaviour, numbers, content or scope were changed.

## Open questions

- Lit brazier reach marks (Known gap 4), for the Game Designer via the Studio.
- Still open and unchanged: flare stun reading, hound bite at lunge distance 1 (step 08).

## Expected output

A verification verdict on checks 14 and 29 (and a regression pass on the rest), with gaps routed back to `gameplay-engineer`; in particular the old check-14 assertion and play.js trace fields from Known gap 1 need an engineer who can see those files.

## Sender assessment

Confidence is moderate for the logic in view.js (it mirrors `execute`'s context: `makeCtx` after dimming uses the same r, distances and visibility). I expect possible old-test failures, as noted. I did not run anything, so this is not evidence of a pass.

## Build check

The runtime ran `run_tests` (`node --test`) on the build exactly as this step wrote it: exit 0 (2.2 s).

```text
 8 creature #4 moth
ℹ threat seed c14-15 command 16 creature #2 moth
ℹ reach  seed c14-15 command 76 creature #1 moth
ℹ reach  seed c14-16 command 17 creature #3 moth
ℹ threat seed c14-16 command 18 creature #3 moth
ℹ threat seed c14-16 command 32 creature #1 moth
ℹ threat seed c14-16 command 35 creature #1 moth
ℹ reach  seed c14-18 command 57 creature #1 moth
ℹ damage events: threat 12, reach 7
✔ sampled states: threat flags equal what the planner does with the ember after dimming (72.52129ms)
✔ check 1: a new run shows E=100, r=6, HP 12/12, floor 1/5 (9.728115ms)
✔ check 2: waiting costs 1 E; radius thresholds (1.968941ms)
✔ check 3: move, wait, fight and item use each cost exactly 1 E; refused actions cost 0 and no turn (0.986429ms)
✔ check 4: brazier at E=30 gives 89, at E=80 gives 99; a lit brazier gives nothing later (0.422896ms)
✔ check 5: E reaching 0 ends the run; creatures do not act (0.509883ms)
✔ check 6: messages at E 20, 10, 5 and when r drops (0.487809ms)
✔ check 7: remembered tiles stay; out-of-sight creatures are not listed (0.994251ms)
✔ check 8: oil +30 up to 100 then dim; salve +5 up to 12 (0.17279ms)
✔ check 19: HP 0 gives "You fell on floor N"; HP 0 with E 0 gives ember out (0.366144ms)
✔ check 20: after an end state further commands change nothing (0.29589ms)
✔ check 24: descending keeps E and HP apart from dimming, increments floor, places on < (1.244349ms)
✔ check 25: a full inventory leaves the item on the floor with a message; the move still costs a turn (0.299038ms)
✔ visibility: adjacent tiles and clear distance-2 straight tiles are always visible at r=2 (15.071563ms)
✔ visibility: walls block line of sight; the glow is circular (0.519365ms)
✔ check 9.1-9.9: the text frame shows every item of spec section 9 (1.232512ms)
✔ view and rules agree: marked threats come from the planner (adjacent moth is marked, distant one is not) (0.468042ms)
ℹ tests 43
ℹ suites 0
ℹ pass 43
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 2035.934056
```

## Load

- Role: studio/roles/qa.md
- Skills: none
- Project: design/game-spec.md, design/acceptance-criteria.md, repo/manual.md
- Decisions: decisions/D-002-threat-and-reach-marks.md
- Previous handoff: goals/G-001-first-playable-run/07-studio-to-gameplay-engineer.md
>>>END

<<<FILE goals/G-001-first-playable-run/10-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 10
from: game-designer
to: studio
stage: Design
outcome: done
---
# 10: game-designer → studio — flare stun timing and hound bite at distance 1 ruled; both built readings ratified

## Task

Route the rulings below to Build (continuing under handoff 07) and to Verify. No code change is needed for the two asked questions.

## Context

G-001: first playable five-floor run. Handoff 08 asked for rulings on two spec questions raised by the Build (handoff 05). The rule was to change a built reading only if it contradicts the spec text or a pillar (readable threats, a decision every turn).

## Findings

### 1. Flare stun: reading A (built) is ratified

- **Ruling:** "Stunned for 2 turns" and "skips its next 2 actions" mean 2 creature actions. The first is in the lighting turn's own creature phase, the second is in the next turn. The creature acts again in the second turn after the lighting turn.
- **Reason:** The spec text says "skips its next 2 actions". The lighting turn's creature phase is the creature's next action, so reading A is the literal reading. No pillar is violated: the frame after the lighting turn shows "stunned" (1 skip remaining), which is true because the creature will skip the next action. The frame after that shows it unstunned, and it can then act, so a threat mark on it is accurate. Marks and states never mislead.
- **Effect on the player:** The flare buys one full free player turn plus the lighting turn. This is a deliberate, modest strength. Reading B would give two full free turns and is not needed. Play can report if flares are too weak.
- **Changed text only:**
  - Spec section 3, flare bullet: explicit timing added.
  - Check 13 reworded so QA does not have to guess ("next 2 turns" was ambiguous).
  - The manual says "acts on the third turn after", counting the lighting turn as the first. That is the same timing as the new text. Build may reword it for clarity.

### 2. Hound bite at lunge distance 1: built reading is ratified

- **Ruling:** A hound adjacent to the player at the start of its action bites for 3. Here a crouching hound whose target stepped adjacent is just a hound adjacent at its action, so the existing adjacent-bite rule applies. "Cannot move, no damage" applies only to a blocked lunge: a wall or another creature stops the hound before it ends adjacent to the player.
- **Reason:** This agrees with the spec's lunge text ("if the player is still within 2 tiles in the line, the hound ends adjacent and the player takes 3"). It also keeps the hound readable. The crouch mark and its line cover distance 1 and 2, and the reach mark already shows a step toward the hound as dangerous. No pillar is contradicted.
- **Changed text only:** one clarifying sentence in the spec's lunge paragraph.

### 3. Two related points the Build flagged or implied, also ruled

- **Lit brazier (manual reading 10): ratified.** A lit brazier has no flare, so it gets reach marks like a floor tile. Otherwise strict check 14 could not hold there.
- **Unlit brazier and the Gloom: new ruling, Build to confirm.** A flare does not stun the Gloom (spec section 7). An unlit brazier tile therefore gets no reach mark from creatures the flare stuns, but it does get a reach mark from the Gloom if the Gloom would hurt the player there at its next action (for example the arena braziers beside a gathered Gloom).
  - This follows from D-002's strict check 14 and the pillar. It is expressible as a planner rule: skip stunnable creatures on unlit brazier hypotheticals, but still evaluate the Gloom.
  - I could not see the build's code. If the build currently shows no reach mark at all on unlit brazier tiles, this is a small Build return.
  - Spec section 9 and check 14 were amended to say so.

### Design files amended in place

- `design/game-spec.md`: flare timing sentence (section 3), lunge adjacency and "blocked" definition (section 4), brazier reach-mark rule (section 9).
- `design/acceptance-criteria.md`: check 13 reworded, and the brazier sentence in check 14. The 30 checks and their numbering are unchanged.

### What I could not show

I could not run anything. The unlit-brazier-and-Gloom ruling is unchecked against the code. Balance impact of the flare timing is unmeasured.

## Decisions already made

- D-002: threat marks plus reach marks, check 14 strict. The Gloom-on-brazier ruling is an application of it. No new Decision was written because nothing changed direction.

## Constraints

- No numbers changed. Scope and the 30 checks are unchanged.

## Open questions

- For Build: does the current reach-mark code evaluate the Gloom on unlit brazier tiles (Finding 3)? If not, add it; this is the only possible code change from this handoff.
- For QA: apply the reworded check 13 and the brazier sentence in check 14. Add a hand-made scenario for each, with a gathered Gloom beside an arena brazier and a hound at distance 1 after a step toward it.

## Expected output

Studio routes Finding 3 to Build if needed, then Verify runs checks 1-26 against the amended spec. This handoff changes no verdicts.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/game-spec.md, design/acceptance-criteria.md, repo/manual.md
- Decisions: decisions/D-002-threat-and-reach-marks.md
- Previous handoff: goals/G-001-first-playable-run/08-studio-to-game-designer.md
>>>END
