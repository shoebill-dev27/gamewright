# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/14-technical-director-to-studio.md, goals/G-001-combat-monotony/15-qa-to-studio.md, goals/G-001-combat-monotony/16-art-director-to-studio.md
next_seq: 17
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha e54837757611; run through the project's run commands)
log: last 5 of 6 entries in @log-recent; the full history is goals/G-001-combat-monotony/log.md

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/14-technical-director-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/15-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/16-art-director-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
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
player_visible: manual.md
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
(`manual.md`): `run_play` shows what a player sees, `run_trace` the simulation state, and
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
- `manual.md` — controls and the play script format (player-facing).
>>>END

<<<FILE @project-files
decisions/D-001-one-button-combat.md
decisions/D-002-combat-response-scope.md
decisions/D-003-run-end-and-room-rules.md
decisions/D-004-option-a-single-change-set.md
design/combat-visuals.md
design/combat.md
goals/G-001-combat-monotony/01-studio-to-playtester.md
goals/G-001-combat-monotony/02-playtester-to-game-designer.md
goals/G-001-combat-monotony/03-game-designer-to-game-director.md
goals/G-001-combat-monotony/04-studio-to-qa.md
goals/G-001-combat-monotony/05-game-director-to-studio.md
goals/G-001-combat-monotony/06-qa-to-game-designer.md
goals/G-001-combat-monotony/07-studio-to-playtester.md
goals/G-001-combat-monotony/08-playtester-to-game-designer.md
goals/G-001-combat-monotony/09-studio-to-game-designer.md
goals/G-001-combat-monotony/10-game-designer-to-studio.md
goals/G-001-combat-monotony/11-studio-to-technical-director.md
goals/G-001-combat-monotony/12-studio-to-qa.md
goals/G-001-combat-monotony/13-studio-to-art-director.md
goals/G-001-combat-monotony/14-technical-director-to-studio.md
goals/G-001-combat-monotony/15-qa-to-studio.md
goals/G-001-combat-monotony/16-art-director-to-studio.md
goals/G-001-combat-monotony/goal.md
goals/G-001-combat-monotony/log.md
manual.md
project.md
repo/README.md
repo/bots.py
repo/game.py
repo/play.py
repo/tests/test_game.py
>>>END

<<<FILE @decision-titles
decisions/D-001-one-button-combat.md — D-001: Combat uses one attack button plus dash
decisions/D-002-combat-response-scope.md — D-002: Respond to combat sameness by reworking existing enemy behavior first (Option A)
decisions/D-003-run-end-and-room-rules.md — D-003: Room mix is across rooms; zero hearts ends the run; room clear heals one heart
decisions/D-004-option-a-single-change-set.md — D-004: Build Option A as one sequential change set on the existing simulation
>>>END

<<<FILE goals/G-001-combat-monotony/goal.md
---
kind: goal
id: G-001
project: lantern-depths
status: active
created: 2026-10-15
---
# G-001: Combat feels monotonous

## Owner request

> 戦闘が単調なので改善したい

## Interpretation

Success condition (qualitative): when an action player from the project's player profile plays through combat encounters, the fights feel varied and engaging, and the player's moment-to-moment choices (positioning, timing, enemy behavior) visibly matter. The player no longer experiences the fights as the same repeated pattern.

Out of scope: adding input buttons beyond attack, dash and pause (D-001, Owner approval needed); changes to the run length or the non-combat systems; numeric targets (these belong to Design as acceptance criteria, and the final verdict to Review).

No immediate escalation: the Goal does not conflict with the vision or D-001, and it needs no reinterpretation. Improving depth through positioning, timing and enemy behavior is what pillar 1 asks for.

## Unknowns

- Observe (playtester): done (02 rooms 1–3, 08 rooms 4–5). Not observed: room 5 fight, approaching a spitter, projectile hits, room clear, dash dodging; the Play step after Build covers them.
- Observe (qa): done (06). Spec gaps were ruled on in Design (10, D-003). Open: the doubled spit line is logged as a minor presentation defect (12, `open`). Nothing verified at 30 FPS yet.
- Diagnose: done (03). Cause: single-state, untelegraphed enemy behavior. Option A chosen (D-002); B deferred; C out of scope.
- Decide: done (D-002). No Owner escalation.
- Design: done (10). Spec in `design/combat.md` (AC-1…AC-17), run/room rules in D-003. Visual rulings (glyphs, colors, telegraph readability) are `open` with `art-director` (13).
- Plan: `open` (11). `technical-director`: the spec is cross-system (attack-slot limit, aim-lock, hit-cancel, run-end flow, 30/60 FPS) and its feasibility is unchecked. Also covers the manual update task.
- Build: `gameplay-engineer`. Planned: the game must change. Starts after Plan, with the QA report (12) and the art rulings (13).
- Verify: `qa` after Build; `art-director` in parallel because visuals change. Planned.
- Play: `playtester` replays the changed build, live and reactive. Planned.
- Review: experience Goal. `game-director` with `review-outcome`. Planned. Run progression after "run over" is not defined; the Director may take it up there.
- Skipped: none.

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | playtester | playtest-session | done | 02-playtester-to-game-designer.md |
| 2 | Diagnose | game-designer | diagnose-experience | done | 03-game-designer-to-game-director.md |
| 3a | Decide | game-director | make-decision | done | 05-game-director-to-studio.md |
| 3b | Observe (defects) | qa | reproduce-defect | done | 06-qa-to-game-designer.md |
| 3c | Observe (rooms 4–5) | playtester | playtest-session | done | 08-playtester-to-game-designer.md |
| 4 | Design | game-designer | write-design-spec | done | 10-game-designer-to-studio.md |
| 5a | Plan | technical-director | technical-plan | open | 11-studio-to-technical-director.md |
| 5b | Observe (spit line) | qa | reproduce-defect | open | 12-studio-to-qa.md |
| 5c | Design (visuals) | art-director | visual-review, write-design-spec | open | 13-studio-to-art-director.md |
| 6 | Build | gameplay-engineer | implement-change | planned | — |
| 7a | Verify | qa | verify-change | planned | — |
| 7b | Verify (visuals) | art-director | visual-review | planned | — |
| 8 | Play | playtester | playtest-session | planned | — |
| 9 | Review | game-director | review-outcome | planned | — |

## Route changes

After step 4 (Design): the spec fits the plan, no escalation trigger. Plan is confirmed (cross-system, feasibility unchecked) and opened with two independent parallel steps: QA logs the duplicate spit line (12) and art-director reviews the visuals (13). Build, Verify, Play are now planned; Verify adds an art-director visual review.

## Next action

Run the three open steps (independent, in any order): `11-studio-to-technical-director.md` (Plan), `12-studio-to-qa.md` (QA), `13-studio-to-art-director.md` (art-director). Each addresses its result to `studio`. When all three are finished, run Route: it opens Build for `gameplay-engineer` (or sends a spec problem back to `game-designer`).

## Outcome

(Filled at Close.)
>>>END

<<<FILE @log-recent
## 003-route · 2026-10-15

Status: active. Open: 02-playtester-to-game-designer.md.

After step 1 (Observe): the report fits the plan, so Diagnose follows. Coverage is limited to rooms 1–3 in scripted play. Open items (hit lockout, grub not dying, post-death state) go to the designer to check against design/combat.md; any defect found goes to `qa`.

## 005-route · 2026-10-15

Status: active. Open: 03-game-designer-to-game-director.md, 04-studio-to-qa.md.

After step 2 (Diagnose): fits the plan, so Decide follows. Opened a parallel QA Observe (3b) for the two possible defects; it is independent of Decide. Added a tentative playtester round on rooms 4–5 (3c), to be opened only if the Director asks for it.

## 008-route · 2026-10-15

Status: active. Open: 07-studio-to-playtester.md.

After steps 3a and 3b: the Director chose Option A (D-002) and asked for a rooms 4–5 play round first, so 3c is confirmed and opened (07). QA found spec gaps, not defects; they join the Design step, which is now planned and waits for the 3c report.

## 010-route · 2026-10-15

Status: active. Open: 09-studio-to-game-designer.md.

After step 3c: the rooms 4–5 report fits the plan (no defects, no escalation trigger), so Design is opened (09). The Handoff carries the report, the Director's direction (05) and QA's spec questions (06), plus the missing Skill and Decisions D-001/D-002.

## 012-route · 2026-10-15

Status: active. Open: 11-studio-to-technical-director.md, 12-studio-to-qa.md, 13-studio-to-art-director.md.

After step 4 (Design): the spec fits the plan, no escalation trigger. Plan is confirmed (cross-system, feasibility unchecked) and opened with two independent parallel steps: QA logs the duplicate spit line (12) and art-director reviews the visuals (13). Build, Verify, Play are now planned; Verify adds an art-director visual review.
>>>END

<<<FILE goals/G-001-combat-monotony/14-technical-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 14
from: technical-director
to: studio
stage: Plan
outcome: done
---
# 14: technical-director → studio — Technical plan for the Option A combat rework (build 0.5)

## Task

Route this plan to `gameplay-engineer` (Build). The spec is feasible within the constraints. Nothing needs to go back to `game-designer` before Build. The spec has a few gaps (F1–F11 below) with defaults I set so Build is not blocked. The designer should confirm them at Review, and F1 (grub speed) matters most.

## Context

G-001, Option A (D-002), spec `design/combat.md` (AC-1…AC-17), rules in D-003. The current build is `repo/` at sha e54837757611 (version 0.4). It is one simulation module (`game.py`, about 200 lines), a script and view runner (`play.py`), balance bots (`bots.py`) and one test file.

Steps 12 (QA defect log, duplicate spit line) and 13 (art-director review of visual states) run in parallel with Plan. Their outputs may change message wording and glyph/color notes before Build starts. The plan keeps both in single data tables so that change is a data edit (task T5).

## Findings

### 1. Feasibility (answers to the open questions)

- **Attack-slot limit (max 2 grubs in Wind-up or Strike): feasible.**
  - Each tick, count grubs whose state is Wind-up or Strike.
  - Grubs that are in range (≤ 1.25 tiles) and not yet attacking are candidates. Sort them by (distance, spawn index), so ties are deterministic. Give out the free slots in that order.
  - A cancelled wind-up, a defeated grub, and the move to Recovery all free the slot at once.
  - Spawn index is the tie-break because "the nearer grub takes the free slot" has no rule for equal distances.
- **Spitter aim-lock: feasible, and almost free.**
  - The existing shot is already a straight line with a velocity fixed at fire time. Aim-lock means computing that velocity at the end of Charge, from the player's position at that instant.
  - No homing and no new projectile system are needed. Keep the shot as `[x, y, vx, vy]` so `bots.py` still unpacks it.
- **Reuse.**
  - Keep the countdown-float timer pattern already used for stun, recovery and cooldown (decrement by `dt`, 1e-9 epsilon). Keep the enemy list, the shot list and the event log.
  - Add per-enemy `state` and `timer` fields. No new classes beyond a few small helper functions.
- **No spec item is infeasible.** No cost or scope flag for the Director. Nothing irreversible. There is no save data.
  - Existing script files still parse.
  - Their results will differ from 0.4, which is intended.

### 2. Approach

**State machines on elapsed seconds**
- Grub states: Approach, Wind-up, Strike, Recovery, plus a short Knockback overlay.
- Spitter states: Idle, Charge, Recovery, Stagger.
- Each transition carries the leftover time. When `timer <= 1e-9`, the next state starts with `duration + timer`, where the overshoot is non-positive. A loop handles several transitions in one tick.
- With the carry, a timestamp error is less than one frame (0.033 s at 30 FPS, 0.017 s at 60 FPS) and does not accumulate. This fits the spec's 0.04 / 0.02 tolerance.
- Spitter volleys use an absolute schedule in seconds from `room_start_t` (first Charge at 1.0 + 0.8·k, then every 2.5 s). Only spitters count for k, in spawn order. A Stagger re-bases that spitter's schedule to `now + 1.0`.

**Strike hit check**
- The Strike lunge moves up to 1 tile in 0.15 s, which is 0.22 tile per frame at 30 FPS.
- Evaluate the "within 1.0 tile at any moment" test as the closest approach over the tick's movement segment. This is a small analytic swept-distance helper, not a sample at the end of the tick.
- Evaluate it in the tick the Strike begins and in every tick until the transition. At 30 FPS this gives 4 or 5 evaluations, which meets "at least 4 frames".
- The lunge target is the player's position when Wind-up ended, as the Strike row says. Lunge length is min(1.0, distance to that spot). A grub hurts the player at most once per Strike.

**Tick order in `step()`**
1. Decrement timers.
2. Move the player and dash. A queued attack fires at dash end.
3. Room-clear check. Attacks from `press()` and from a queued attack have already happened.
4. Enemies, then shots. Neither runs once the player is down, and on clear all shots are removed first.
5. Phase timers: the down countdown, the room-transition countdown and the run-over state.

This makes "a clearing swipe cancels the strike or projectile hit due on that tick" hold. In 0.4 the clear check is at the end of the tick, so it must move.

**Run flow**
- It lives in `Game`, so `play.py` and `bots.py` share it. The phases are playing, cleared-waiting, down, and run over/complete.
- `cleared` keeps its meaning "current room cleared". It stays true until the next room loads, so bots that stop on it keep working.
- The practice room (`empty`) is not a run: no heal, no transition, and the session ends 2.0 s after the player goes down.
- Room load puts the player at (8, 4). It resets enemies and shots and leaves hearts and the other player timers alone.

**Swipe and feedback**
- Cone: with axis-aligned facing, hit when `along > 0` and `|across| <= along`, within 1.5. An enemy on top of the player counts as a hit. 0.4 uses a 180° half-plane test, so this is a change.
- The swipe arc is state in the simulation (`arc_left`, direction), so it is visible at any frame within 0.15 s.
- Event names kept for compatibility: `attack`, `hurt`, `down`, `spit`, `cleared`, `ignored`, `dash`.
  - `attack` gains per-hit remaining HP.
  - `ignored` gains `reason` values: `stunned`, `too soon` (renamed from `recovering`), `down`, `dash not ready`.
- New events: `windup`, `strike`, `recover`, `charge`, `stagger`, `knockback`, `defeated`, `room_loaded`, `heal`, `run_over`, `run_complete`, `run_start`.

**Trace** (a QA-facing interface)
- Add `state` and `timer` to each enemy column, and `room=` to the state line.
- A line is printed for every state change. AC-6 can then be checked by counting Wind-up/Strike grubs per line, and AC-2 timings read directly from the lines.

**Player view**
- Add snapshots at: swipe, wind-up/charge start, going down, room load and run over. The arc and telegraph are then always on screen. The 0.5 s cadence alone is fragile for a 0.5 s wind-up.
- Colors: ANSI orange/red for threat states, enabled by a `--color` flag or when stdout is a TTY. Glyphs must make the three states distinguishable without color. This keeps captured logs plain.

### 3. Ordered tasks (single change set, sequential)

Build keeps the existing file layout. `Game` stays in `game.py`; Build may add small helper functions but no new modules.

- **T1. Sim core: grub and spitter state machines.**
  - Includes the slot allocator, swept strike check, knockback, the 1.25 / 1.0 / 2.0 tiles-per-second constants, 3.0 shot speed, the 2.5 s stagger schedule, Charge cancel and aim-lock.
  - Depends on nothing.
- **T2. Player attack changes.** Depends on T1.
  - 90° cone.
  - Arc state.
  - Hit/defeat feedback events with remaining HP.
  - Hit on a Wind-up grub: cancel the wind-up and give a 0.6 s Recovery.
  - Hit on a Charging spitter: cancel the charge and give a 1.0 s Stagger.
  - Reasons on every ignored attack.
- **T3. Run and room flow.** Depends on T2 (clear check and tick order).
  - Down handling: enemies freeze and shots are removed.
  - The 2.0 s countdown, then run over.
  - Restart on attack.
  - Clear: remove shots, heal +1 (max 3), 1.5 s of free input, load the next room.
  - Room 5: "run complete".
  - Practice-room rules.
- **T4. Trace.** Depends on T1–T3. Add enemy state, the room column and the new events.
- **T5. Player view.** Depends on T1–T3 and the event vocabulary from T1–T4. Check outputs 12 and 13 first.
  - One `GLYPHS` table (character and ANSI color, per kind and state: full, telegraph, damaged) and one `LINES` table of player-visible strings, both in `play.py`.
  - Lines: "a grub rears back", "spitter (top right) charges", the spit line naming its spitter, the swipe-result lines, the reasons, "you went down", "room cleared", "run complete", and the run-over screen.
  - Position names come from a 3×3 grid. If two spitters share a label, add a numeric disambiguator.
  - Update the version string to 0.5.
- **T6. Bots.** Depends on T3.
  - Fix `hearts_lost` to count `hurt` events. After a clear the +1 heal makes `HEARTS - game.hearts` wrong.
  - Check `_incoming` still works.
  - Optional, low priority: a "reactive" bot that dashes or backs off during a wind-up, to give the live playtest a datapoint on "grubs not trivial / dash matters". Include it only if it is cheap.
- **T7. Tests.** Written alongside T1–T6; see section 4.
- **T8. `manual.md`** (owner: `gameplay-engineer`, in the same change set). Done after T5 has frozen the glyph and message tables. See section 6.
- **T9. As-built report** to the Studio (section 5).

### 4. Test strategy per acceptance criterion

All engineer-written tests run through `run_tests` (unittest). Timing tests are parameterized over fps 30 and 60 and assert against spec times with the spec tolerance (0.04 s at 30 FPS, 0.02 s at 60 FPS). QA still verifies independently from trace and player view, as the spec says.

Existing tests that break by design, to be rewritten:
- two-swipe test (the grub now bites later);
- immediate-bite test;
- 2.0 s spitter interval (now 2.5 s with a 1.0 s first charge);
- double-grub invulnerability test (timings change). Keep its purpose: a dash right after a hit keeps both protections at 30 and 60 FPS.

The bots smoke test must still pass.

| AC | Coverage |
|---|---|
| AC-1 | Unit test, practice room, grub at distance 4, idle player. Wind-up event ≥ 0.45 s before the first `hurt`, and no `hurt` outside Strike. View-capture test for the "a grub rears back" line. The glyph change is compared against the `GLYPHS` table, then eyeballed by QA in the player view. |
| AC-2 | Unit test on event timestamps (wind-up 0.5, strike 0.15, recovery 0.9). |
| AC-3 | Unit test: dash away at the start, middle and last frame of Wind-up, in open space. The geometry must keep 4 tiles clear of walls. Zero hearts lost each time. |
| AC-4 | Unit test: swipe in Recovery, damaged state, next Strike ≥ 1.5 s after the previous one for a still player. |
| AC-5 | Unit test: swipe during Wind-up. No heart lost, 0.6 s Recovery, slot freed. |
| AC-6 | Unit test with 5 grubs in the practice room, scanning each frame for ≤ 2 in Wind-up/Strike. Room 5 has only 3 grubs, so the stronger test is needed. Also run room 5 through `run_bots` at both frame rates as a smoke check. |
| AC-7 | Unit test on Charge/Fire times in rooms 3, 4 and 5 (1.0, 1.8, 2.6 and every 2.5 s). See F5 for the interpretation. |
| AC-8 | View-capture test: charge line 0.8 s before each spit, spit line names its spitter, no identical lines at one timestamp. |
| AC-9 | Unit test with a spitter and an idle player (hit for 1 heart). Also tests that move ≥ 1 tile off the line, and that dash through the line. Margins ≥ 1 frame. A dash that ends within 0.4 tile of a shot is still a hit (invulnerability covers the dash only), so tests must dash clear. |
| AC-10 | Unit test: walk up and defeat a practice-room spitter in 2 swipes; a hit in Charge fires nothing. QA does a scripted walk in room 3 (`run_trace` / `run_play`). |
| AC-11 | View-capture test for each outcome line and each reason. No bare "(nothing happens)" anywhere in `play.py` output. Distinctness of the three glyph/color states is asserted from the table. |
| AC-12 | Unit test: two grubs in the cone give two hit lines. |
| AC-13 | Unit test and view-capture test: down line, `x`, enemies frozen, shots removed, "(down)", run-over screen at 2.0 s, restart on attack. Needs script handling for F7. |
| AC-14 | Unit test: heal +1, capped at 3; shots removed; next room after 1.5 s; same-tick clear with a shot placed on top of the player (set by the test); "run complete" in room 5, reached by setting HP in the test. |
| AC-15 | View-capture test for the practice room. Small test that each player-visible string in the `LINES` table and each glyph appears in `manual.md`. QA reads the manual. |
| AC-16 | Unit test: trace setup rows vs the layouts. |
| AC-17 | AC-1…AC-14 tests run at both fps. Differential test: 3–4 fixed scripts with inputs on multiples of 0.1 s, run at 30 and 60. Same event-kind sequence and timestamps within 0.07 s. Bots are compared only on aggregates. Dash-distance difference ≤ 0.25 tile is already covered by the existing dash test. |

Additional tests:
- Moving during the 0.35 s swipe recovery works (spec rule, "not yet observed").
- A `StrikeFrames` test: at 30 FPS the Strike is evaluated in ≥ 4 ticks for every phase offset of the leftover carry.

QA and playtest only, not automatable:
- Reading the glyph/color distinction and the arc in the player view.
- All [tune] values and the experience signals (live reactive playtest after Build).
- Whether grubs are trivial and the dash matters.

### 5. As-built values Build must report

- Swipe reach and the cone as computed.
- Projectile speed and the shot hit radius (existing 0.4; the spec does not say).
- Grub walking speed and the waiting-grub behavior (F2).
- Strike lunge distance and speed.
- Knockback distance and duration (spec 1 tile / 0.2 s, plus wall clamping).
- Spitter Recovery (0.6) and Stagger (1.0).
- Every [tune] timing as built: 0.5, 0.9, 0.6 (cancel recovery), 0.8, 2.5, 3.0, heal +1.
- The glyph/color table and arc pattern.
- The exact player-visible strings.
- Maximum measured timestamp error at 30 and 60 FPS, and the maximum cross-fps difference.
- Minimum Strike frames at 30 FPS.
- What was chosen for each of F1–F11.

### 6. `manual.md` update (task T8)

- **Owner:** `gameplay-engineer`, in Build, same change set.
- **When:** after T5 has frozen glyphs and strings, and after reading outputs 12 and 13.
- **Wording:** take player-visible wording from `design/combat.md`: the practice room, `x`, the new glyph/states, the swipe arc, the run-over screen, the attack messages (miss / too soon / stunned / down), telegraph lines, the room-clear heal and the 1.5 s pause, and restart by attack.
- Update the title and the on-screen description to build 0.5.
- Describe behavior; do not copy [tune] numbers, so the manual does not drift.
- Keep it player-facing: no implementation notes, no design rationale. A Playtester reads it.
- QA checks AC-15 against it.

### 7. Risks and mitigations

- **Frame-rate dependence.**
  - Mitigation: elapsed-seconds timers with leftover carry, a swept strike check, no frame counts, and tests at both frame rates.
  - AC-17's 0.07 s cross-fps bound is tight, since a distance-triggered Wind-up start can be late by up to one frame at 30 FPS.
  - Measure first. If the delta exceeds about 0.05 s, add sub-frame carry for distance triggers (leftover = tick time minus time of crossing).
- **Tick-order regression (clear vs damage).** Mitigation: the AC-14 same-tick test.
- **Slot starvation.** With a still player and three grubs, the two nearest grubs are always nearer after their lunge, so the third waits indefinitely. This is per spec ("the nearer takes the slot") and reads as "readable", but it is a tuning question. Do not change it in Build; watch it in the live playtest.
- **Bots drift.** The shot shape and `cleared` meaning are kept. Hearts lost are counted from events.
- **Late changes from outputs 12 and 13.** Handled by the data tables (T5).
- **Old scripts.** They still parse, and results differ from 0.4.
- **Performance.** Negligible (at most 6 enemies).

### 8. Parallelization decision

**One change set, one engineer, no isolated workspaces.** See D-004.
- All behavior lives in `game.py`, and the trace, view and bots all depend on its event vocabulary. Parallel branches would conflict in `game.py` or would be written against a vocabulary that is still moving.
- The total size is small.
- The manual and tests wait for the string and glyph tables.
- Steps 12 and 13 are non-code inputs; they do not create parallel code work.

### 9. Spec gaps and chosen defaults (none blocking)

For the designer to confirm at Review:

- **F1. Grub speed.** The spec says 2.0 tiles/s "as observed", but build 0.4 has 1.2. Build implements the spec's 2.0. The designer should confirm that was intended, because grubs will arrive much faster than in 0.4.
- **F2. Unslotted grub.** The spec says "approaching/circling" with no circling rule. Default: it approaches to 1.25 tiles, then holds and waits for a slot. Report as built.
- **F3. Spitter with the player on top of it.** Zero distance gives no direction. Default: no projectile for that volley (as in 0.4), logged in the trace only.
- **F4. Stagger re-base.** After a cancelled charge, the spitters' volleys may no longer be offset, so "never fire together" is guaranteed only from room start. Default: per spec, no extra spacing.
- **F5. AC-7 wording.** "Never start a Charge or fire in the same 0.5 s" is read as no two Charge starts and no two Fires within 0.5 s. A Fire and another spitter's Charge start do coincide at 1.8 s by the spec's own numbers.
- **F6. Run complete.** The timing and screen text are not specified. Default: "room cleared" then "run complete" at the clear, the +1 heal, the 1.5 s free-input window, then a final screen "run complete — rooms cleared: 5". Attack starts a new run.
- **F7. Run-over vs scripts.** "A scripted session ends at the run-over screen" conflicts with AC-13 (attack at the screen starts a new run). Default: the session stops at the screen unless the script has a later input, in which case that attack restarts the run. The practice room always ends 2.0 s after going down.
- **F8. Hits in other grub states.**
  - A hit in Strike: damage applies, the lunge continues, no knockback.
  - A hit in Recovery: knockback applies and the Recovery timer is not extended.
  - Knockback applies to a first hit in any other state.
- **F9. Damaged plus telegraph.** The spec lists three states but a damaged grub can also wind up. Default: the telegraph glyph has priority, and the text line gives the HP. The art-director review (13) should confirm.
- **F10. Other ignored inputs.** To remove every bare "(nothing happens)": any input during stun prints "(stunned)", and a dash on cooldown prints "(dash not ready)". The wording of the second is new.
- **F11. Pause.** The spec's "Pause: all timers freeze" has no implementation in the current build or script format, and no AC covers it. Build adds no pause. QA should mark it not verifiable here. The designer may add a script verb later.

## Decisions already made

- D-001: one attack button plus dash.
- D-002: rework existing enemy behavior (Option A). B deferred, C out of scope.
- D-003: room mix across rooms, zero hearts ends the run, clear heals one heart.
- D-004 (new): Option A is built as one sequential change set.

## Constraints

- No new inputs (D-001). Correct at 30 and 60 FPS. Reuse existing systems.
- The spec's player-facing behavior is unchanged except where F1–F11 fill gaps.

## Open questions

- **For the designer, non-blocking:** F1–F11, especially F1, F6 and F7.
- **For `art-director` (step 13):** F9 and the plain-text fallback for color.
- **For QA (step 12):** whether the spit line wording changes.
- **For the Studio:** none for Build to start.

## Expected output

- **Next:** `gameplay-engineer`, Build. Deliverables: T1–T9 in one change set with passing `run_tests`, `run_bots` at 30 and 60 FPS, updated `manual.md`, and the as-built report from section 5.
- **Then:** QA verifies AC-1…AC-17 at 30 and 60 FPS from the trace and player view, followed by a live reactive playtest for the [tune] values.
- **After Build,** the designer reviews F1–F11 against the as-built report.

## Sender assessment

- High confidence on feasibility. The attack-slot limit and aim-lock fit the existing structures.
- Main schedule risk: the tight cross-fps bound (7), and rework of the tests.
- F1 is the item most likely to change how the game feels. Grubs at 2.0 tiles/s instead of 1.2 may reduce the player's reaction time more than the designer expects.
- Not checked by me: I did not run the build or the tests. The check on 1.2 against the spec's 2.0 is from reading `game.py` (`GRUB_SPEED`).

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: none specified
- Project: project.md#constraints, design/combat.md, manual.md, repo/README.md, repo/game.py, repo/play.py, repo/bots.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-response-scope.md, decisions/D-003-run-end-and-room-rules.md, decisions/D-004-option-a-single-change-set.md
- Previous handoff: goals/G-001-combat-monotony/14-technical-director-to-studio.md
>>>END

<<<FILE goals/G-001-combat-monotony/15-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 15
from: qa
to: studio
stage: Observe
outcome: done
---
# 15: qa → studio — Defect report: identical "a spitter spits" lines at one timestamp (rooms 4–5)

## Task

Studio: route this report. The doubled line is reproduced. It is two spitters each printing one line, not one event printed twice. The defect is presentation only: the two lines are identical and do not say which spitter fired.

## Context

Handoff 12 asked whether the repeated spitter attack line is one event printed twice (a defect) or two spitters each printing their own line (one line per spitter). It also asked in which rooms it occurs and whether it changes with spitter count. Build under test: `repo/` at sha e54837757611 (the player view header reads "Lantern Depths 0.4"). All evidence comes from the run commands in `project.md`, driven by input scripts.

## Findings

### Verdict

- **Reproduced: yes.** Every volley in rooms 4 and 5 prints two identical lines at the same timestamp.
- **Cause class: two events, not one event printed twice.**
  - With one spitter, the trace shows one `spit` event per volley.
  - With two spitters, the trace shows `spit; spit` per volley.
  - So the count of lines follows the count of spitters, i.e. one line per spitter. That matches the "one line per spitter" expectation stated in handoff 12.
- **What is wrong:** the text is the same for both spitters ("a spitter spits"). It carries no name or position, so the player cannot tell the lines apart and reads them as a duplicate. This is a presentation defect. It is not a logic or double-fire defect.

### Reproduction

Script A (player view, room 4):
```
room 4
fps 60
end 5
```
Command: `python3 play.py --view player {script}`

Observed:
```
  2.000  a spitter spits
  2.000  a spitter spits
  4.000  a spitter spits
  4.000  a spitter spits
```

Script B (trace, one spitter):
```
room empty
fps 60
spawn spitter 15 0
player 8 4
end 6
```
Observed: a single `spit` event at t=2.000, 4.000 and 6.000.

Script C (trace, two spitters):
```
room empty
fps 60
spawn spitter 15 0
spawn spitter 15 8
player 8 4
end 6
```
Observed: `spit; spit` at t=2.000, 4.000 and 6.000. The projectile count follows: the player view shows two `*`, one per spitter, so the pair is two shots and not a duplicate print.

### Conditions varied

| Condition | Result | View used |
|---|---|---|
| Room 4, 60 FPS | Pair of identical lines at 2.0, 4.0, 6.0, 8.0 s | player and trace |
| Room 4, 30 FPS | `spit; spit` at 2.0, 4.0, 6.0, 8.0 s, same as 60 FPS | trace only |
| Room 5, 60 FPS | `spit; spit` at 2.0, 4.0, 6.0, 8.0 s | trace only |
| 1 spitter (practice room) | One `spit` per volley | trace only |
| 2 spitters (practice room) | `spit; spit` per volley | trace only |

- **Frame rate:** the script format has an `fps 30|60` line, so both frame rates can be set. The behavior and the timestamps are the same at both.
- **Rooms:** it occurs in both room 4 and room 5, because both have the same two corner spitters at (15,0) and (15,8).
- **Spitter count:** the number of identical lines equals the number of spitters. Room 3 (3 spitters) was not run; I expect three identical lines there, and that is a hypothesis, not an observation.

### Not run (round budget)

- The player-view text for room 5 and for the one-spitter case. The trace `spit` events were used as the evidence there.
- The player view at 30 FPS.
- Room 3.

### Expected, and its source

- `design/combat.md` AC-8 (build 0.5 target): "The spit line names its spitter; there are no identical duplicate lines at one timestamp."
- AC-8 describes the target build, not the current one. No document defines the current build's line text as a defect. The current build behaves as "one line per spitter", which is what handoff 12 says the design expects. The defect is therefore measured against AC-8, which the planned spitter rework must satisfy. It is not a regression against an earlier spec.
- The cause of the missing name is not known. A plausible hypothesis (unverified) is that the line text is a fixed string that does not take the spitter's identity.

### Severity and frequency

- **Severity: cosmetic / low.** The mechanics are unaffected. The cost is readability: the player cannot tell which spitter fired, and the repeated line looks like a bug.
- **Frequency:** every volley in rooms 4 and 5 (about every 2.0 s on the current build), 100% of volleys.

### Evidence

The trace rows for the room 4 runs at 30 and 60 FPS, the room 5 run at 60 FPS, and the one-spitter and two-spitter runs are quoted above and in the run results of this step.

## Decisions already made

None bear on this defect.

## Constraints

- Report only what is observable on the current build; no fix is proposed.
- The rest of the Option A spec was not verified or commented on.

## Open questions

None for the Owner. Process note for the Studio: the observed behavior matches "one line per spitter", so this is not a duplicate-event bug. Treat it as presentation covered by AC-8, to be verified after the rework.

## Acceptance criteria for the fix

1. In rooms 4 and 5, at both `fps 30` and `fps 60`, each spit line names its spitter (for example by position, as in "spitter (top right) spits").
2. No two lines printed at the same timestamp have identical text, for any spitter count (check 1, 2 and 3 spitters; rooms 3, 4 and 5).
3. The number of spit lines at a timestamp equals the number of spitters that fired, and the number of `spit` trace events is unchanged.
4. Each spit line can be matched to its projectile (that spitter's `*`).
5. Spit timing and projectile behavior are unchanged by this fix, apart from whatever the rework intentionally changes.

## Expected output

Studio routes this defect report to the owner of the spitter rework, as a presentation requirement alongside AC-8.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md, manual.md, project.md#constraints
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/12-studio-to-qa.md
>>>END

<<<FILE goals/G-001-combat-monotony/16-art-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 16
from: art-director
to: studio
stage: Design
outcome: done
---
# 16: art-director → studio — Visual review of the Option A spec: rulings and visual spec for Build

## Task

Route the visual spec in `design/combat-visuals.md` to Build alongside `design/combat.md`. Route the manual change and the one question below.

## Context

G-001: combat monotony. D-002 chose Option A. The game-designer's spec (`design/combat.md`) leaves glyphs and colors to Build and to my review. The rooms 4–5 playtest (08) found that spitters read as scenery and their shots were never reacted to. This was a spec review against `project.md#art-direction` and pillar 3. There is no build yet, so nothing could be checked against actual output. I changed no rules, timings or parameters.

## Findings

### Verdicts

| Question | Verdict | Evidence |
|---|---|---|
| Are Wind-up, Charge and Recovery distinguishable from idle and harmless states? | **Fail as specified, fixed by rulings below.** | The spec says only "glyph and color change". The view is text, so a color-only change would be invisible. A Recovery that "returns to the normal glyph" is identical to Approach in a still frame. |
| Can the player see the telegraph in time? | **Fail as specified.** | The room is drawn every 0.5 s, and the grub Wind-up lasts 0.5 s. A frame can miss it entirely. The swipe arc lasts 0.15 s and would almost never be drawn. |
| Do threat colors read against the dark? | **Pass in principle.** | Saturated orange/red against cold blue-black matches the art direction. Not verifiable until the build exists. |
| Are damaged states and the downed marker clear? | **Pass with changes.** | The spec requires a distinct glyph and color but gives none. Rulings fix them. `x` was unstyled. |

### Rulings (what to keep, what to change)

**Keep:**
- Saturated orange/red for committed threats and projectiles.
- The swipe arc, the damaged state, the remaining-HP hit lines and the explicit "(miss)" reasons.
- The `x` downed marker and the run-over text.

**Change** (full detail in `design/combat-visuals.md`):
1. **Glyph carries the state, not color alone.** Uppercase means committed to hurting (`G`, `W`, `S`, `Z`). Lowercase means harmless (`g`, `w`, `s`, `z`). A damaged enemy uses the `w/z` family.
2. **Harmless enemies are muted.** Orange/red is reserved for telegraphed enemies and `*`. The player, the swipe arc and `x` never use it. This makes the telegraph the loudest thing on the map, and it is what makes the spitter stop looking like scenery.
3. **Extra draws on telegraph events.** The room is drawn at Wind-up start, Charge start, projectile spawn, every swipe, grub Recovery start and player down. Otherwise short telegraphs fall between 0.5 s frames. Timings are untouched.
4. **Text lines name the enemy and its position.** Grub: "a grub rears back (left)". Spitter lines are named by position. A new "the grub is open" line marks the start of Recovery, the counter window. A stagger line is added for spitters.
5. **Swipe arc glyphs** `) ( ^ v` in lantern color on the tiles in reach.
6. **Run-over screen** adds the line "press attack to start again", because the spec's restart rule is otherwise undiscoverable.

### Handoff items

- **`manual.md` must be updated** (not on my write list): the glyph table, the `x` marker, the arc, the practice room, the new lines and the run-over screen (V-5). Route to whoever owns the manual, after Build fixes the final glyphs.
- **Acceptance:** V-1…V-8 in `design/combat-visuals.md` join AC-1…AC-17 for Verify. After Build, I should review the actual player view for color and legibility.
- `design/combat.md` is unchanged. Its line "chosen in Build and documented in the manual" now means: follow `design/combat-visuals.md` and document any change in `manual.md`.

## Decisions already made

- D-001: one attack button plus dash.
- D-002: Option A, reuse existing enemy behavior.
- No new decision recorded; nothing here changes a style pillar.

## Constraints

- No rule, timing or parameter changed. No new inputs. Reuse existing systems.

## Open questions

- **For Build / Plan:** can the extra draws on events (principle 4) be added cheaply? If not, tell `game-designer`: a 0.5 s Wind-up cannot be guaranteed visible with only a 0.5 s draw cadence.
- **Optional, for game-designer:** should the player's invulnerability (hit and dash) be visible? Suggested `p` for `P`. This needs no rule change.

## Expected output

The Studio routes Build (`gameplay-engineer`) with `design/combat.md` plus `design/combat-visuals.md`, then Verify (`qa`) with AC-1…AC-17 and V-1…V-8, then a visual review of the built player view by the art-director.

## Sender assessment

Confidence high on glyph, case and event-draw rulings: they follow from the text view and the 0.5 s draw cadence. Confidence medium on colors: they cannot be judged until a build exists.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: none specified
- Project: design/combat.md, design/combat-visuals.md, manual.md
- Decisions: decisions/D-002-combat-response-scope.md
- Previous handoff: goals/G-001-combat-monotony/13-studio-to-art-director.md
>>>END
