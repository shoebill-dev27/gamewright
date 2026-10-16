# Studio operation packet

operation: Route
goal: G-001
step_artifacts: goals/G-001-combat-monotony/76-qa-to-studio.md
next_seq: 77
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha d85493974c04; run through the project's run commands)
log: last 5 of 26 entries in @log-recent; the full history is goals/G-001-combat-monotony/log.md

## You may write

- goals/G-001-combat-monotony/goal.md
- goals/G-001-combat-monotony/76-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- goals/G-001-combat-monotony/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 77
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
design/combat-cues-visual-spec.md
design/combat-step-44-walker-limit.md
design/combat-step-46-room3-cap.md
design/combat-step59.md
design/combat-step68.md
design/combat-step72.md
design/combat.md
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
goals/G-001-combat-monotony/goal.md
goals/G-001-combat-monotony/log.md
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
>>>END

<<<FILE goals/G-001-combat-monotony/goal.md
---
kind: goal
id: G-001
project: lantern-depths
status: active
created: 2026-10-16
---
# G-001: Combat feels monotonous

## Owner request

> 戦闘が単調なので改善したい

## Interpretation

Success condition (qualitative): a player playing the current build's combat experiences it as varied and engaging instead of monotonous. Different situations call for noticeably different play (positioning, timing, use of attack and dash), and the player can tell why. The improvement stays inside the vision pillars: one-button combat (attack + dash only, D-001), short runs, readable threats. Numeric thresholds belong to Design; the final verdict belongs to Review.

Out of scope: new input buttons (needs Owner approval per D-001), changing run length, new biomes or content unrelated to combat variety, and any change to the core concept. Not a defect report: nothing in the request says combat is broken.

## Unknowns

- Observe: done (02; QA 16, 20, 32, 36, 56, 64). Contact-edge graze accepted (D-002, D-003). 30 FPS player view and late-swipe boundary match the design (64). No open defect.
- Diagnose: two passes done (04, 31); a third is barred by the loop limit. Review 67 found no new cause.
- Decide: skipped. Review pass 2 (67, D-010) found the D-009 escalation condition not met. Row 11 (Owner escalation) stays tentative: only if Review pass 3 says the melee still reads as one fight.
- Design: D-004 to D-007 stand. Room 3 in-flight question settled by D-007 (68); D-011 accepted (variant-named wind-up and hit messages, supersedes D-008). Room 3 variety specified by D-012 (72): one standard grub at (15,0), second spitter to (10,6); cap and cue rule unchanged. Open for the playtest: whether a long single-spitter standoff remains.
- Plan: skipped (approach local). Returns if the same criterion fails verification twice.
- Build: 0.6.1 done (48). Build 22a done (71): D-011 messages and manual wording; tests and bots not yet run. Build 23 done (74): room 3 data change per D-012 on top of 22a; tests, bots and traces not yet run.
- Verify (QA): pass on 0.6.1 at 30 and 60 FPS (50, 64). Any new build needs Verify. Visual V1–V11 need a graphical build, a proposed new Goal at Close; V12 open.
- Play: three scripted passes done (27, 53, 63). Rooms 4–5 varied and engaging; room 3 and the slow-run brute loop repetitive; brute/runner messages read "a grub". Next: a fresh playtest of the new build, ideally live or hand-timed, with the playtest brief stating the build.
- Review: pass 1 (60) and pass 2 (67) done, both goal-not-met; the gap is narrow. Pass 3 follows the next playtest.

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | playtester | playtest-session | done | 01-studio-to-playtester.md (report: 02-playtester-to-studio.md) |
| 2 | Diagnose | game-designer | diagnose-experience | done | 03-studio-to-game-designer.md (result: 04-game-designer-to-studio.md) |
| 3 | Decide | game-director | make-decision | skipped (no real choice; see Unknowns) | — |
| 4a | Design | game-designer | write-design-spec | done | 05-studio-to-game-designer.md (result: 07-game-designer-to-studio.md) |
| 4b | Observe (FPS divergence) | qa | reproduce-defect | done | 06-studio-to-qa.md (result: 08-qa-to-studio.md) |
| 5 | Plan | technical-director | technical-plan | skipped (approach local; see Unknowns) | — |
| 6 | Build | gameplay-engineer | implement-change | done | 09-studio-to-gameplay-engineer.md (result: 10-gameplay-engineer-to-studio.md) |
| 7a | Design (criterion 14, spec gaps) | game-designer | write-design-spec | done | 11-studio-to-game-designer.md (result: 14-game-designer-to-studio.md) |
| 7b | Verify (visual) | art-director | visual-review | done | 12-studio-to-art-director.md (result: 15-art-director-to-studio.md) |
| 7c | Observe (walker 30/60 divergence) | qa | reproduce-defect | done | 13-studio-to-qa.md (result: 16-qa-to-studio.md) |
| 7d | Build (bot log data, walker test) | gameplay-engineer | implement-change | done | 17-studio-to-gameplay-engineer.md (result: 18-gameplay-engineer-to-studio.md) |
| 8 | Verify (criteria 1–16, V12) | qa | verify-change | done (question: graze) | 19-studio-to-qa.md (result: 20-qa-to-studio.md) |
| 8b | Design (graze, cap, margin, doc conflicts) | game-designer | write-design-spec | done | 21-studio-to-game-designer.md (result: 22-game-designer-to-studio.md) |
| 8c | Build (contact test / cap) | gameplay-engineer | implement-change | skipped (graze and cap accepted as built) | — |
| 8d | Verify (criteria 1–17; close 30 FPS gaps) | qa | verify-change | done (pass) | 23-studio-to-qa.md (result: 24-qa-to-studio.md) |
| 9a | Play | playtester | playtest-session | done | 25-studio-to-playtester.md (report: 27-playtester-to-studio.md) |
| 9b | Design (QA notes: exact-reach miss, lunge band) | game-designer | write-design-spec | done | 26-studio-to-game-designer.md (result: 30-game-designer-to-studio.md) |
| 10a | Diagnose (playtest issues 1–4) | game-designer | diagnose-experience | done | 28-studio-to-game-designer.md (result: 31-game-designer-to-studio.md) |
| 10b | Observe (room 2 grub hit after swipe) | qa | reproduce-defect | done (not a defect) | 29-studio-to-qa.md (result: 32-qa-to-studio.md) |
| 11 | Decide (Owner escalation if the melee still reads as one fight, D-009) | game-director | prepare-owner-escalation | tentative (only if Review pass 3 says so) | — |
| 12a | Design (Options 1–2, manual wording) | game-designer | write-design-spec | done | 33-studio-to-game-designer.md (result: 35-game-designer-to-studio.md) |
| 12b | Observe (spitter fire times, rooms 3–4) | qa | reproduce-defect | done (no defect) | 34-studio-to-qa.md (result: 36-qa-to-studio.md) |
| 12c | Design (invulnerable contact, room 3 cue overlap) | game-designer | write-design-spec | done | 37-studio-to-game-designer.md (result: 38-game-designer-to-studio.md) |
| 13 | Build (build 0.6 per Design 35 and 38) | gameplay-engineer | implement-change | done | 39-studio-to-gameplay-engineer.md (result: 40-gameplay-engineer-to-studio.md) |
| 14a | Verify (0.6, 30 and 60 FPS) | qa | verify-change | done (fail: F2, F3, 13@60, room 3) | 41-studio-to-qa.md (result: 43-qa-to-studio.md) |
| 14b | Design (criterion 13 walker limit, 60 FPS) | game-designer | write-design-spec | done (D-006, no build change) | 42-studio-to-game-designer.md (result: 44-game-designer-to-studio.md) |
| 15 | Design (room 3 cap vs criterion 11) | game-designer | write-design-spec | done (D-007, accepted as built) | 45-studio-to-game-designer.md (result: 46-game-designer-to-studio.md) |
| 16 | Build (F2, F3 only) | gameplay-engineer | implement-change | done | 47-studio-to-gameplay-engineer.md (result: 48-gameplay-engineer-to-studio.md) |
| 17 | Verify (re-verify, incl. "not run" list, criterion 11 a–e) | qa | verify-change | done (pass) | 49-studio-to-qa.md (result: 50-qa-to-studio.md) |
| 18a | Play (fresh, hand-timed rooms 2–5) | playtester | playtest-session | done | 51-studio-to-playtester.md (report: 53-playtester-to-studio.md) |
| 18b | Design (criterion 11d wording, non-blocking) | game-designer | write-design-spec | done (no build change) | 52-studio-to-game-designer.md (result: 54-game-designer-to-studio.md) |
| 18c | Observe (late swipe vs lunge; hit with no cue; message wording) | qa | reproduce-defect | done (not a defect) | 55-studio-to-qa.md (result: 56-qa-to-studio.md) |
| 18d | Design (manual wording on late swipes; variant cue message) | game-designer | write-design-spec | done (D-008 proposed, later D-011) | 58-studio-to-game-designer.md (result: 59-game-designer-to-studio.md) |
| 19 | Review (pass 1) | game-director | review-outcome | done (goal-not-met; D-009) | 57-studio-to-game-director.md (result: 60-game-director-to-studio.md) |
| 20a | Play (variant-aware, fresh, build 0.6.1 unchanged) | playtester | playtest-session | done | 61-studio-to-playtester.md (report: 63-playtester-to-studio.md) |
| 20b | Observe (30 FPS player view, late-swipe boundary) | qa | verify-change | done (no defect) | 62-studio-to-qa.md (result: 64-qa-to-studio.md) |
| 21a | Review (pass 2) | game-director | review-outcome | done (goal-not-met; D-010) | 65-studio-to-game-director.md (result: 67-game-director-to-studio.md) |
| 21b | Design (room 3 in-flight vs D-007; D-008 readiness) | game-designer | write-design-spec | done (D-007 stands; D-011 accepted) | 66-studio-to-game-designer.md (result: 68-game-designer-to-studio.md) |
| 22a | Build (D-011 messages, manual wording) | gameplay-engineer | implement-change | done | 69-studio-to-gameplay-engineer.md (result: 71-gameplay-engineer-to-studio.md) |
| 22b | Design (room 3 variety, existing enemies) | game-designer | write-design-spec | done (D-012) | 70-studio-to-game-designer.md (result: 72-game-designer-to-studio.md) |
| 23 | Build (room 3 change, D-012) | gameplay-engineer | implement-change | done | 73-studio-to-gameplay-engineer.md (result: 74-gameplay-engineer-to-studio.md) |
| 24 | Verify (22a + 23; V-a..e, R3-1..10; 30 and 60 FPS) | qa | verify-change | open | 75-studio-to-qa.md |
| 25 | Play (fresh, new build, live or hand-timed) | playtester | playtest-session | planned | — |
| 26 | Review (pass 3) | game-director | review-outcome | planned | — |
| 27 | Next | studio | — | planned | — |

## Route changes

After 23 (74): room 3 data change built on top of 22a, as planned. Neither 22a nor 23 has any test, bot or trace result yet. Verify 24 opened (75) for both builds in one pass, composed for QA without the engineer's notes. Design docs: combat.md still shows the old room 3; combat-step72.md governs.

## Next action

Run `qa` (fresh context) with 75-studio-to-qa.md (address the result to `studio`). Then Route: on pass, open a fresh playtest (25) stating the build, with room 3 played live or hand-timed, then Review pass 3 (26). A failure goes by the return rules; a tuning question about criterion 13 or 14 goes to `game-designer`. Escalate to the Owner only if Review pass 3 says the melee still reads as one fight (D-009).

## Outcome

(open)
>>>END

<<<FILE @log-recent
## 057-route · 2026-10-16

Status: active. Open: 61-studio-to-playtester.md, 62-studio-to-qa.md.

After 18d and 19 (59, 60): Review is goal-not-met; per D-009 the next pass is a variant-aware playtest, not a third Diagnose. Opened Play 20a (61, build 0.6.1 unchanged) and QA 20b (62, 30 FPS gaps) in parallel. Manual text (59) and the D-008 message change wait until after the playtest so the played build stays steady.

## 060-route · 2026-10-16

Status: active. Open: 65-studio-to-game-director.md, 66-studio-to-game-designer.md.

After 20a and 20b (63, 64): playtest shows rooms 4–5 varied, room 3 and brute loop repetitive, brute/runner messages read "a grub". QA closed the 30 FPS gaps with no defect. Opened Review pass 2 (65) and, in parallel, a non-blocking Design check (66: room 3 in-flight vs D-007; D-008 readiness). Build waits for both.

## 063-route · 2026-10-16

Status: active. Open: 69-studio-to-gameplay-engineer.md, 70-studio-to-game-designer.md.

After 21a/21b (67, 68): Review pass 2 is goal-not-met with a narrow gap and no Owner escalation (D-010). Design kept D-007 for room 3 in-flight and accepted D-011 (variant-named messages). Opened Build 22a (69: D-011, manual text) and, in parallel, Design 22b (70: room 3 variety). A room 3 Build follows only if 22b specifies one; then Verify, fresh playtest, Review pass 3.

## 073-route · 2026-10-16

Status: active. Open: 73-studio-to-gameplay-engineer.md.

After 22a/22b (71, 72): D-011 messages built (tests not yet run). Design chose D-012: room 3 gets a standard grub at (15,0) and its second spitter moves to (10,6); cap and cue rule unchanged. Build 23 confirmed and opened (73) on top of the 22a build; one Verify then covers both.

## 075-route · 2026-10-16

Status: active. Open: 75-studio-to-qa.md.

After 23 (74): room 3 data change built on top of 22a, as planned. Neither 22a nor 23 has any test, bot or trace result yet. Verify 24 opened (75) for both builds in one pass, composed for QA without the engineer's notes. Design docs: combat.md still shows the old room 3; combat-step72.md governs.
>>>END

<<<FILE goals/G-001-combat-monotony/76-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 76
from: qa
to: studio
stage: Verify
outcome: fail
---
# 76: qa → studio — Verification of the current build (D-011 messages and manual, D-012 room 3) at 30 and 60 FPS: FAIL on one red test; no build-behavior defect found; three checks not run

## Task

Report the verification of `repo/` (build 0.6 with D-011 and D-012) against `design/combat-step68.md` (V-a to V-e), `design/combat-step72.md` (R3-1 to R3-10) and the regression list, at 30 and 60 FPS.

## Context

Goal G-001 (combat monotony). Handoff 75 asked for a verdict per criterion for the D-011 message and manual changes and the D-012 room 3 layout change. The last verified state was 0.6.1 (QA 50 and 64). I used three run rounds: the whole test suite and the bots at both rates; player-view traces of the practice room (one per variant, both rates); and room 3 traces (still player, a no-grub replica, a last-spitter replica, a reactive dasher), both rates. No 0.6.1 output was in the packet, so nothing is compared with the earlier build byte for byte.

## Findings

### 1. `run_tests` (whole suite): FAIL, 1 of 64

```
FAIL: test_wind_up_and_hit_messages_name_the_variant (test_game.VariantMessageTest)
AssertionError: 3 != 1 : (30, 'grub')     (assertion on out.count("a grub rears back"), test_game.py line 763)
```

- 63 tests pass. This includes the room 3 contents test, the room 3 clear test (spitters and grub all needed), the manual-wording test, the `text "rears back"` test for all three variants, and the cue, cap, blocked-contact and brute tests.
- Classification: a defect in the test, not in the build. The test runs 3 s with a still player and asserts the wind-up message appears once. A still player is hit, the grub recovers, walks up and rears back again. My direct trace shows this: the runner rears back at 0.033 s and again at 1.167 s at 30 FPS. Derived for the grub at 30 FPS: wind-ups at about 0.03, 1.5 and 2.8 s, which gives the 3 the test counted. The derivation is not separately traced.
- The assertion stops at the first failure, so the runner and brute cases and the 60 FPS cases of this test never ran. I covered them by direct traces (section 3).
- Severity: low, since the build is not affected. The suite is red, so I cannot pass.

### 2. `run_bots` (rooms 1–5, limit 60 s, 3 hearts each)

| Bot / room | 30 FPS | 60 FPS |
|---|---|---|
| walker 1 | not cleared, lost 3 | not cleared, lost 3 |
| walker 2 | cleared 8.4 s, lost 2 | cleared 8.4 s, lost 2 |
| walker 3 (new layout) | cleared 8.9 s, lost 1 (grub 1), 8 attacks | cleared 9.2 s, lost 1 (grub 1), 8 attacks |
| walker 4 | cleared 9.9 s, lost 1 | not cleared, lost 3 |
| walker 5 | not cleared, lost 3 | cleared 12.9 s, lost 2 |
| dodger 1 / 2 / 3 / 4 / 5 | all cleared, 0 lost; 6.6 / 20.7 / 15.6 / 18.3 / 24.2 s; dashes 3 / 10 / 6 / 7 / 11 | all cleared, 0 lost; 9.6 / 25.1 / 15.0 / 17.0 / 28.8 s; dashes 5 / 14 / 6 / 8 / 14 |
| camper (clears) | 1/5 (room 2 only) | 0/5 |
| camper room 3 | not cleared (6.3 s), lost 3, 0 attacks | same |

Criteria against the numbers:
- **13** (rooms 3–5 summed):
  - 30 FPS: walker lost 1+1+3 = 5 (limit 3–6) and cleared 2 (limit ≥2). Dodger lost 0 (limit ≤2.5) and cleared 3/3. Camper cleared 0 of 3 rooms, fewer than the walker's 2. **Pass.**
  - 60 FPS: walker lost 1+3+2 = 6, exactly the upper limit and not above it, and cleared 2 (rooms 3 and 5). Dodger lost 0 and cleared 3/3. Camper cleared 0. **Pass, with the walker at both limits.**
  - The in-repo test comment records 7 hearts for the 60 FPS walker earlier on 0.6. It is 6 now, so the room 3 change did not push it over. The walker's loss in room 3 is 1 heart, all from the grub, at both rates.
- **14** (rooms 1–2): walker lost 5 at both rates (limit ≥1). Dodger lost 0 and cleared 2/2 (limit ≤1). **Pass.**
- **15**: dodger dashes in rooms 3 / 4 / 5 are 6 / 7 / 11 at 30 FPS and 6 / 8 / 14 at 60 FPS, all ≥1. **Pass.**
- **16c**: the dodger clears the same rooms at both rates, with hearts lost per room identical (0). **Pass.** The walker's per-room differences are allowed by 16d.
- Observation, with no limit in any design document: dodger clear times differ between rates, for example room 1 at 6.6 s vs 9.6 s and room 5 at 24.2 s vs 28.8 s. The documents define no clear-time limit, so no comparison is possible.
- Nothing is outside a limit, so no tuning question arises from the bots.

### 3. D-011 criteria (`design/combat-step68.md`)

Evidence: practice room, one enemy at (9.5, 4), player at the start, 1.2 s, both rates.

| Variant | Wind-up message, 30 / 60 FPS | Hit message and time, 30 / 60 FPS |
|---|---|---|
| grub | `a grub rears back` 0.033 / 0.017 s | `YOU ARE HIT by a grub — hearts 2/3` 0.667 / 0.633 s |
| runner | `a runner rears back` 0.033 / 0.017 s | `YOU ARE HIT by a runner — hearts 2/3` 0.533 / 0.483 s |
| brute | `a brute rears back` 0.033 / 0.017 s | `YOU ARE HIT by a brute — hearts 2/3` 0.867 / 0.833 s |

- The `cue:` line at the first picture reads 0.50 / 0.35 / 0.70 s to the lunge, and the wind-up lengths match the parameter table.
- **V-a: pass.** One message per wind-up, on the first frame in range. It is printed again only when the enemy winds up a second time. A comparison against 0.6.1 timing was not possible (no baseline).
- **V-b: pass.** The hit message names the matching variant at the contact frame. The hearts suffix is unchanged. The shot message is unchanged (`by a shot — hearts 2/3`, seen in the room 3 traces and covered by the test).
- **V-c: NOT VERIFIED.** "Byte-identical to 0.6.1" needs a 0.6.1 baseline, and the packet has none. This is a verification gap, not a failure. The `cue:` line, `~` line, swipe and shrug messages looked as specified.
- **V-d: pass.** `test_rears_back_rule_matches_all_variants` passes. In room 3 live, `when text "rears back" then dash aside` fired on `a grub rears back` (dash at 5.667 s at 30 FPS, 5.650 s at 60 FPS).
- **V-e: partial.** The 63 passing tests cover criteria 1–11 and 17–21 in the practice room at both rates. "No bot result changes" cannot be compared, because room 3 changed in the same build and there is no 0.6.1 bot output.
- **Manual text: pass.** `repo/manual.md` carries the exact replacement text for the late-swipe bullet (including "A brute is never cancelled.") and for the spitter paragraph ("so in room 3 up to 5 can be in the air at once."). It also lists all three wind-up messages and all four hit messages. The test for it passes.

### 4. D-012 criteria (`design/combat-step72.md`)

- **R3-1 contents: pass.** `game.py` ROOMS["3"] is spitters (2,1), (10,6), (2,7) and grub (15,0), and the contents test passes. The picture at 0.00 s shows the same. Rooms 1, 2, 4, 5 match the `combat.md` table (room 1 grubs (3,4), (15,4), (8,0); room 2 runners (2,1), (1,8), brute (15,7), grub (14,0); room 4 runner (1,4), grub (0,1), spitters (15,0), (15,8); room 5 grubs (1,1), (0,6), brute (4,8), spitters (15,0), (15,8)).
- **R3-2 schedule: pass.**
  - Still player: aims at 1.200, 2.000, 2.800 s and spits at 1.800, 2.600, 3.400 s at both rates (cue 0.600 s before each shot).
  - The cue and spit times of the still-player room 3 trace and the no-grub replica (three spitters, player at (8,4)) are the same up to the end of the trace. Spits fall at 1.8, 2.6, 3.4, 4.2, 5.0, 6.2 s and aims at 1.2, 2.0, 2.8, 3.6, 4.4, 5.6, 6.0 s, identical at both rates. The 6.0 s aim of the second spitter and the hits at 3.4, 5.5 and 6.3 s match too.
- **R3-3 grub after the lessons: pass.** For a still player at (8,4), the grub's first `a grub rears back` is at **6.100 s at 30 FPS and 6.083 s at 60 FPS**, against the 4.0 s minimum. The grub was at (9.7, 3.0), about 1.97 tiles from the player. No retune is needed under D-012 item 4.
- **R3-4 grub criteria in room 3: pass on the evidence I have, with a gap.**
  - Observed in room 3 live with the reactive player:
    - The cue read 0.50 s to the lunge at its first picture.
    - A swipe during the wind-up cancelled it. At 30 FPS the swipe at 7.533 s was followed by a new wind-up at 7.967 s, and no lunge came between them.
    - Two swipes killed the grub: 7.533 and 10.433 s at 30 FPS; 7.117 and 7.483 s at 60 FPS.
    - A dash on the cue (`dash aside` at 5.667 s) was followed by no grub hit.
  - The room 3 trace never showed a 1-tile sidestep, a dash late in the lunge, or a recovery swipe. Those are covered only by the practice-room tests (GrubTest) at both rates, which use the same code path. I did not run them as separate room 3 scripts.
- **R3-5 spitter criteria with the grub alive: pass.** In the still-player trace, every cue is 0.6 s before its shot. The dodge and contact-edge tests pass. In the reactive 60 FPS run the player took no damage in 20 s. The 30 FPS reactive run took one shot hit at 8.7 s. That is the scripted player's reaction timing and not a build question: its rules act every 0.15 s, and I did not trace the divergence between the rates further.
- **R3-6 D-007 bound: pass.**
  - Cue start times with and without the grub are equal up to the player's death at 6.3 s, as in R3-2. The grub's first lunge would have come at about 6.6 s.
  - In the reactive traces all three spitters start cues together after a cap delay: 6.000 s (spits at 6.600 s) at both rates, then again around 8.8–9.4 s at 30 FPS, 10.0–10.6 s at 60 FPS, and later. This is the accepted D-007 behavior and not a defect.
  - Derived in-flight counts by the step 46 method (visible `*` plus spits in the last 0.3 s):
    - 30 FPS: 4 at 7.00 s; 2 visible + 3 spits = 5 at 13.50 s.
    - 60 FPS: 5 visible at 11.00 s; 2 visible + 3 spits = 5 at 14.00 s.
    - The maximum is 5, never above 5.
  - The script is my own (it has the grub and extra rules), not the QA 43 script of criterion 11d. The method is the same.
- **R3-7 room end: pass.** The room clear test (spitters alone or grub alone does not clear; all four does) passes. In the 60 FPS reactive run the grub was killed at 7.483 s while three spitters were alive, and the session ended at 20 s with "enemies left 3" and no `room cleared`.
- **R3-8 last spitter close: PARTIAL.**
  - Geometry: pair distances are (2,1)–(10,6) = 9.43, (10,6)–(2,7) = 8.06 and (2,1)–(2,7) = 6.00 tiles, so the maximum is 9.43, within 9.5. **Pass.**
  - The "within 6 s of the previous kill" run, with a scripted kill of the grub and two spitters followed by a walk to the last spitter, was **not run**. The derived value is about 3 s (9.43 tiles at 4 tiles/s is about 2.4 s, plus two swipes). My single-spitter replica (a walk of about 7 tiles and two swipes) shows only that the walk and two swipes take about 1.35 s from the last arrival. That is not the specified measurement.
- **R3-9 messages: pass.** `a grub rears back` appears in room 3 live and `YOU ARE HIT by a grub` in the practice room. The `text "rears back"` rule reacts (see V-d).
- **R3-10 frame-rate independence: pass for what ran.** R3-2 and R3-3 differ by 0.000–0.017 s between rates (at most one 60 FPS frame, within ±1 frame). The tests cover criteria 1–12 and 17–21 at both rates.

### 5. Regression checks

- Rooms 1, 2, 4, 5: contents unchanged (R3-1). The bots clear them as in section 2, and the dodger loses 0 hearts in all of them at both rates.
- Criteria 1–11, 17–21: covered by the passing tests at 30 and 60 FPS. Criterion 11 (cap) in room 3 is covered in R3-6.
- Criteria 13–16: section 2.
- Room 3 in-flight bound: R3-6.
- Not re-run as separate traces: the criteria 17 and 20 edge cases and the room 4 and 5 gap traces. They rely on the unit tests, which pass.

### 6. Defects, conflicts, undefined behavior

1. **Defect (test, severity low, Build):** `test_wind_up_and_hit_messages_name_the_variant` expects one wind-up message in 3 s from a still player, but a variant re-winds up after recovering. The suite is red because of it. Expected source: V-a says "each wind-up prints its message once". It does not say "once in 3 s". Acceptance for the fix is a green suite that still checks, for every variant at both rates, one message per wind-up and a matching hit message.
2. **Document conflicts** (`design/combat-step72.md` governs, as the handoff says):
   - `combat.md` still has the old room 3 row (spitter at (14,7), no grub), the old room 3 purpose, criterion 12 and criterion 11 ("rooms 1–5 never more than 3").
   - `combat.md` still says the wind-up message is "a grub rears back (all variants)". `combat-step68.md` governs and the build follows it.
   - `combat-cues-visual-spec.md` says spitter cues are "normally 0.8 s apart". That is true only in room 3 and is already noted for the art director.
   - `decisions/D-007` ends with a stray `</parameter>` line, which looks like a formatting leftover.
3. **Not verified (gaps, not failures):**
   - V-c, byte-identical output to 0.6.1: no baseline in the packet.
   - V-e, "no bot result changes": no 0.6.1 bot output, and room 3 changed in the same build.
   - R3-8, the timed run to the last spitter.
   - R3-4, a direct room 3 sidestep, late dash and recovery swipe.
4. **Observations, no defect:**
   - A still player in room 3 dies at 6.3 s to three spitter shots (hits at 3.4, 5.5, 6.3 s), before the grub's first lunge. The grub only matters to a player who survives the first 6 s.
   - The D-007 simultaneous cue start now occurs at 6.0 s in the reactive run (6.8 s in QA 43). This is the same accepted cap-delay case, and the count never exceeded 5.
   - No undefined expected behavior was found, so nothing goes to Design.

## Decisions already made

- D-012 (room 3 layout), D-011 (variant messages), D-007 (room 3 bound and simultaneous cues), D-005 (blocked contact), D-001 (one-button combat). I applied them as written and changed none.

## Constraints

- Both 30 and 60 FPS were checked wherever a run was made.
- I verified from the specs, criteria and build, not from the implementer's explanations. I did not modify production code or tests.
- Bot numbers are reported without proposed values. None is outside a limit.

## Open questions

1. Can the Studio supply a 0.6.1 baseline (play output for the V-c scripts and bot output) so V-c and the "no bot result changes" part of V-e can be judged? Otherwise Studio decides whether to accept them as unverified.
2. Should the 60 FPS walker sitting at both limits (6 hearts lost, 2 rooms cleared) be watched? Any further layout change risks it. It is not a defect now.

## Expected output

**Verdict: fail** for this verification round. The reason is the red suite (a test defect), not any observed build behavior. Routing:
- Defect 1 goes to `gameplay-engineer` (Build): fix the test, which is test tooling.
- The re-verify should then close the gaps: a timed R3-8 run in room 3, direct room 3 sidestep, late-dash and recovery-swipe scripts for R3-4, and V-c / V-e if a baseline exists.
- No spec gap goes to `game-designer`, and no criterion has failed twice.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat-step72.md, design/combat-step68.md, design/combat.md, design/combat-step-46-room3-cap.md, design/combat-cues-visual-spec.md, repo/manual.md, repo/README.md, repo/game.py, repo/bots.py, repo/tests/test_game.py, project.md
- Decisions: decisions/D-012-room3-standard-grub-and-closer-spitter.md, decisions/D-011-variant-named-messages-accepted.md, decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md, decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Previous handoff: goals/G-001-combat-monotony/75-studio-to-qa.md
>>>END
