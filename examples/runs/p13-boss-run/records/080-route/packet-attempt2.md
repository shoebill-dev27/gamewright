# Studio operation packet

operation: Route
goal: G-002
step_artifacts: goals/G-002-final-boss/65-game-designer-to-studio.md
next_seq: 66
context_request: used (the requested files are in Inputs)
current_build: repo/ (sha d86d55d41027; run through the project's run commands)
log: last 5 of 35 entries in @log-recent; the full history is goals/G-002-final-boss/log.md

## You may write

- goals/G-002-final-boss/goal.md
- goals/G-002-final-boss/65-game-designer-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- project.md: only in the Route that closes the Goal, and only its ## Current state (at most 1,500 characters)
- goals/G-002-final-boss/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 66

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
decisions/D-022-g002-v1-supplements.md
decisions/D-023-owner-confirms-verification-supply.md
decisions/D-024-g002-historical-comparison-evidence.md
design/combat-cues-visual-spec.md
design/combat-step-44-walker-limit.md
design/combat-step-46-room3-cap.md
design/combat-step59.md
design/combat-step68.md
design/combat-step72.md
design/combat-step94.md
design/combat.md
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
repo/source_id.py
repo/tests/test_boss.py
repo/tests/test_boss_contract.py
repo/tests/test_boss_contract_details.py
repo/tests/test_bots_boss.py
repo/tests/test_d022_observation.py
repo/tests/test_d022_shots_and_note.py
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
- Build：done。56でSplit Cを納品。runtimeの保存ソース04fa2b1c168aは全suite152件OK。pause/retry込み通常ランの同一試行計測、dodger独立1〜4の回帰固定、ボス判断ログを提出済み。報告された通常ラン勝利時間は30 FPS 86.967 s／60 FPS 103.533 s。履歴値との報告精度での一致と、変更前の厳密な同一性の未証明を区別する。Build証拠であり独立検証・体験判定ではない。
- Verify：未完了。60はfail。製品戦闘の再現済み不具合や同一基準の修正後再失敗2回とは扱わない。同じ不足のまま第三のQA依頼は出さず、D-023に合わせた基準整理・再計画・試験道具対応・再測定後に独立QAを再開する。全文保存先は存在しないため、検証対象を明示した出力と直列分割で必要な証拠を構成し、未確認を合格にしない。
- Plan（検証供給・試験道具）：done。62で公開情報だけのボス判断境界、接触診断、完全証拠保存、4条件再測定、独立1〜4回帰、変更前基線調査を計画。実行・修正・基線探索は未実施。仕様・難度・秒数ゲートは変更しない。
- Decide（検証供給）：done。D-023で案Aと供給上限を確定。Loadは個別ファイル本文、@needは一度8ファイルまで、@runはStepごとに3回まで、出力は最大2万字で全文保存先なし。変更前ビルドは存在しない。D-021のまま進める。
- Design（変更前一致）：open。Designerが各該当基準を記録数値との比較にするか確認不能として扱うか決定する。比較の精度・限界と未確認の残し方を明示し、厳密な変更前同一性を主張しない。
- Plan（供給条件への適合）：planned。Designer判断後、Technical Directorが62の計画をD-023へ適合させる。個別Load、最大3回の実行、出力上限内の証拠、直列分割、公開情報botの再測定と独立QAへの受渡しを具体化する。存在しない保存機構や変更前ビルドを前提にしない。
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
| 6d | Build | gameplay-engineer | implement-change | done | 31-studio-to-gameplay-engineer.md → 結果: 32-gameplay-engineer-to-studio.md |
| 6e | Build | gameplay-engineer | implement-change | done | 33-studio-to-gameplay-engineer.md → 結果: 34-gameplay-engineer-to-studio.md |
| 6f | Build | gameplay-engineer | implement-change | done | 35-studio-to-gameplay-engineer.md → 結果: 36-gameplay-engineer-to-studio.md |
| 6g | Build | gameplay-engineer | implement-change | done | 37-studio-to-gameplay-engineer.md → 結果: 38-gameplay-engineer-to-studio.md |
| 6h | Build | gameplay-engineer | implement-change | done | 39-studio-to-gameplay-engineer.md → 結果: 40-gameplay-engineer-to-studio.md |
| 6i | Build | gameplay-engineer | implement-change | done | 41-studio-to-gameplay-engineer.md → 結果: 42-gameplay-engineer-to-studio.md（未着手） |
| 6j | Build | gameplay-engineer | implement-change | done | 43-studio-to-gameplay-engineer.md → 結果: 44-gameplay-engineer-to-studio.md |
| 6k | Build | gameplay-engineer | implement-change | done | 45-studio-to-gameplay-engineer.md → 結果: 46-gameplay-engineer-to-studio.md（部分成果、V1は質問） |
| 6k-d | Design | game-designer | write-design-spec | done | 47-studio-to-game-designer.md → 結果: 48-game-designer-to-studio.md（D-022） |
| 6k-b | Build | gameplay-engineer | implement-change | done | 49-studio-to-gameplay-engineer.md → 結果: 50-gameplay-engineer-to-studio.md（partial、入力不足） |
| 6k-c | Build | gameplay-engineer | implement-change | done | 51-studio-to-gameplay-engineer.md → 結果: 52-gameplay-engineer-to-studio.md（partial、140件OK） |
| 6k-d2 | Build | gameplay-engineer | implement-change | done | 53-studio-to-gameplay-engineer.md → 結果: 54-gameplay-engineer-to-studio.md |
| 6l | Build | gameplay-engineer | implement-change | done | 55-studio-to-gameplay-engineer.md → 結果: 56-gameplay-engineer-to-studio.md |
| 7 | Verify | qa | verify-change | done | 57-studio-to-qa.md → 結果: 58-qa-to-studio.md（証拠不足） |
| 7a | Verify | qa | verify-change | done | 59-studio-to-qa.md → 結果: 60-qa-to-studio.md（供給不足・bot所見） |
| 7b | Plan | technical-director | technical-plan, prepare-owner-escalation | done | 61-studio-to-technical-director.md → 結果: 62-technical-director-to-studio.md |
| 7b-owner | Decide | owner | — | done | 63-studio-to-owner.md → D-023 |
| 7b-design | Design | game-designer | make-decision, write-design-spec | open | 64-studio-to-game-designer.md |
| 7b-plan | Plan | technical-director | technical-plan | planned | Designer判断を受け62をD-023へ適合 |
| 7b-build | Build | gameplay-engineer | implement-change | planned | 適合計画に従う試験道具対応・再測定 |
| 7c | Verify | qa | verify-change | planned | 基準整理・計画適合・試験道具対応後 |
| 8 | Verify | art-director | visual-review | planned | — |
| 9 | Play | playtester | playtest-session | planned | — |
| 9a | Design | game-designer | make-decision, write-design-spec | planned | — |
| 10 | Review | game-director | review-outcome | planned | — |
| 11 | Next | studio | — | planned | — |

逐次実行する。D-023を受け、Designerの変更前一致基準整理→Technical Directorの供給条件に適合した再計画→Engineerの試験道具対応・再測定→独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewとする。各StepのLoadは必要なファイルを個別指定する。全文保存先・別実行枠・変更前ビルドの供給を待たない。明白な対処不能・到達不能が判明した場合はDesigner判断を前倒しする。並列Stepは開かない。

## Route changes

63へのOwner回答をD-023に記録し、Goalをactiveへ戻す。64でDesignerに変更前一致基準の扱いを委ね、その後に62を実際の供給上限へ適合させる再計画を置く。全文保存や変更前ビルドの供給待ちは解消し、同じ不足のまま第三のQA依頼は出さない。

## Next action

Game Designerが64-studio-to-game-designer.mdを開始する。変更前一致を求める各基準について、記録数値との比較か確認不能かを決め、Technical Directorの再計画に使える形でStudioへ返す。

## Outcome

未完了。Ownerは案Aを選び、D-023で実際の供給条件を確定した。D-021のテキスト方式を継続し、Designerの変更前一致基準整理から再開する。全文保存先と変更前ビルドは存在しないため、それらの供給を待たず、出力の絞り込みと直列分割を計画する。ボスbotの公開情報条件への対応・再測定、独立QA・限定Art Verify・独立Play・実測後Designer判断・Reviewは未完了。戦闘本体の不具合や難度の結論は未確定で、通常再生時間とVisionとの差も保持する。project.mdは変更しない。
>>>END

<<<FILE @log-recent
## 070-route · 2026-10-21

Status: active. Open: 57-studio-to-qa.md.

56はdone。runtimeの保存ソース04fa2b1c168aで全suite152件OKのため、57で独立QAを開く。Engineerの自己評価を含む56はQAへ渡さず、仕様・受入基準・実行経路を新しいHandoffにまとめる。以後の逐次順序は維持する。

## 072-route · 2026-10-21

Status: active. Open: 59-studio-to-qa.md.

58は証拠不足によるfail。製品の基準違反は未確定のためBuildへ戻さず、59で独立QAを継続し、保存ソース・テスト本文と追加実行から未確認を解消する。同一基準の再現失敗2回には数えない。Art Verify以降はQA合格まで待機し、逐次順序を維持する。

## 074-route · 2026-10-21

Status: active. Open: 61-studio-to-technical-director.md.

60で同じ検証入力・実行枠不足が再報告されたため、第三のQA再発行を止め、61でTechnical Directorへ供給障害の整理とOwner escalation準備を渡す。D-019のbot観測条件の不適合所見も技術計画へ含める。製品の同一基準再失敗2回とは数えず、後続の検証・体験評価は待機する。

## 076-route · 2026-10-21

Status: blocked-on-owner. Open: none.

62の技術計画とOwner宛brief準備を完了として記録し、63で検証供給の調整・範囲縮小・停止をOwnerへ提示する。Goalをblocked-on-ownerにし、依存Stepを停止。今回の供給改善と後続供給の未確認を区別し、第三のQA再発行は行わない。

## 078-resume · 2026-10-23

Status: active. Open: 64-studio-to-game-designer.md.

63へのOwner回答をD-023に記録し、Goalをactiveへ戻す。64でDesignerに変更前一致基準の扱いを委ね、その後に62を実際の供給上限へ適合させる再計画を置く。全文保存や変更前ビルドの供給待ちは解消し、同じ不足のまま第三のQA依頼は出さない。
>>>END

<<<FILE goals/G-002-final-boss/65-game-designer-to-studio.md
---
kind: handoff
goal: G-002
seq: 65
from: game-designer
to: studio
stage: Route
outcome: done
---
# 65: game-designer → studio — 変更前一致の記録比較と確認不能を確定

## Task

D-024と証拠適用補足を受領し、Technical Directorへ62のD-023適合再計画をルーティングする。確認不能部分を残したまま検証を進める工程と、最終判断への引継ぎを整理する。

## Context

D-023でOwnerはテキスト方式の継続を指示し、変更前ビルドは保存されていないと確定した。Designerには、変更前一致要求を記録数値との比較にするか、確認不能として扱うかが委任された。

今回はこの委任範囲だけを判断した。実装、play／bots実行、独立QA判定、実測後の難度判断は行っていない。

## Findings

新規成果物：

- `decisions/D-024-g002-historical-comparison-evidence.md`
- `design/g002-historical-comparison-evidence.md`

補足仕様の表に、従来要求、採択した扱い、出典、条件・精度、未確認範囲を記載した。

### 確定した扱い

L1の変更前出力・結果・終了時刻、O3の変更前出力、step68 V-cのbyte一致、step94 W7の変更前イベント・挙動一致は確認不能とした。L4、step68 V-a／V-b／V-e、step94 W3／W4に含まれる歴史的一致も、現在の仕様へ直接照合できる部分と分離した。

独立1〜4 dodgerは40の記録数値との比較を採択した。各FPS・部屋、3 hearts、通常初期状態、limit 60秒を揃え、clear・損失0・dash回数と小数1桁時間を比較する。時間の丸め方法も補足仕様で定義した。56の保存実行報告は後続記録として区別する。

40は既にボス対応後の保存ソース`5145454ab956`である。40も提出前一致を確認できなかったと明記しており、この記録からボス対応前の厳密な同一性は証明しない。56の`04fa2b1c168a`での152件成功も、その不足を埋めない。

R2・step72 R3-1の保持部分は元仕様の配置・パラメータへの現行照合であり、変更前実装を必要としない。step72 R3-6のgrub有無比較、combat16c、現行の注記抑制対照、既定値と明示0.5秒の対照は、現在のビルド内比較として継続できる。

### Technical Directorへの仕様上の入力

62の「変更前基線を探索・供給する」「全文原本の保存・再読込みを再開条件にする」部分はD-023へ適合させる。存在しない基線・保存先を待つ計画にはしない。

最大3回、各出力2万字の範囲で、対象を絞った証拠出力と必要な直列Stepへ再構成する。表示した証拠の範囲、集計・判定の方法、未表示部分を区別できる計画が必要である。試験構造と技術方式は本Stepでは選ばない。

ボスbotの公開情報限定対応、突進診断の訂正、開始3/2 hearts別FPS再測定、通常ラン入力の再生成は62の依存順序を保持する。対応前ボス数値と生成再生時間を新たなpass基線にしない。独立1〜4の保持比較とは分離する。

確認不能を合格・免除・Goal達成にしない。62の「全QA合格後」という工程条件は、歴史比較の確認不能を含めて再整理する必要がある。Goal再解釈や範囲変更が必要ならGame Directorへ返す。QAに直接免除を求めない。

## Decisions already made

- D-019：保持回帰、公開情報限定のボス比較、実測後Designer判断を維持。
- D-021：Studio内のテキスト・スクリプト方式。実機供給と旧指定sha照合は不要。
- D-022：旧経路注記、弾ライフサイクル、長時間観測の契約を保持。
- D-023：個別本文供給、@need一度最大8件、@run最大3回、出力最大2万字、全文保存先・変更前ビルドなし。
- D-024：歴史的一致の確認不能と、独立1〜4 dodgerの記録精度に限定した比較を確定。

## Constraints

製品仕様、戦闘パラメータ、難度、秒数ゲートを変更しない。60のQA判定を上書きしない。未確認をpassにしない。

ボスbot対応前の数値から戦闘不具合・難度不合格を断定しない。追加数値ゲートと時間Visionの判断は再測定・独立QA・独立Play後に残す。

本Handoffと補足仕様の検証結果・期待値を独立Play資料へ転記しない。

## Open questions

1. Technical Directorは、供給上限の中で基準別の証拠と独立実行をどの単位へ分割するか。
2. 歴史比較の確認不能を保持した工程条件をどう整理するか。Goalの再解釈が必要ならGame Directorへ返すこと。
3. 対応後の保持記録比較に差が出た場合、その条件と影響は何か。差が出る前の推測で仕様を変えない。

## Expected output

StudioはTechnical Directorへ、62をD-023・D-024へ適合させる再計画を依頼する。基線探索・全文保存機構の確保を開始条件から外し、対象別の本文供給、限定出力、直列分割、未確認の受渡しを具体化する。

その後、試験道具対応→再測定→独立QAへ進む条件を確定する。確認不能項目は最終Reviewにも渡す。限定Art Verify、独立Play、実測後Designer判断、Game Director Reviewを省略しない。

次の技術再計画で追加本文が必要な個別ファイル名：

- `repo/source_id.py`
- `repo/bots.py`
- `repo/run_driver.py`
- `repo/play.py`
- `repo/tests/test_bots_boss.py`
- `repo/tests/test_split_c.py`
- `repo/tests/test_d022_observation.py`
- `repo/tests/test_d022_shots_and_note.py`

この8件は62の主要所見を再計画へ結び付けるための本文であり、全QAに十分なファイル一覧ではない。後続QAの全tests本文はStudioが個別ファイル名で別途割り当てる。

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/make-decision.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md
- Project: design/g002-historical-comparison-evidence.md
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-step68.md
- Project: design/combat-step72.md
- Project: design/combat-step94.md
- Project: goals/G-002-final-boss/40-gameplay-engineer-to-studio.md
- Project: goals/G-002-final-boss/56-gameplay-engineer-to-studio.md
- Project: goals/G-002-final-boss/60-qa-to-studio.md
- Project: goals/G-002-final-boss/62-technical-director-to-studio.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Decisions: decisions/D-023-owner-confirms-verification-supply.md
- Decisions: decisions/D-024-g002-historical-comparison-evidence.md
- Previous handoff: goals/G-002-final-boss/64-studio-to-game-designer.md
>>>END

<<<FILE studio/roles/technical-director.md
---
kind: role
id: technical-director
writes: decisions/*
runs: tests, trace
---
# Role: Technical Director

## Responsibility

Turns approved specs into technically feasible plans. Owns technical risk, architecture, test
strategy, sequencing, and whether work can safely run in parallel.

## Decides

- Technical approach and architecture within the project's constraints.
- Sequencing, task breakdown, and parallelization (including isolated code workspaces).
- Technical acceptance checks (e.g., performance budgets) that serve the spec.

## Must not

- Change the spec to suit the implementation — propose the change to `game-designer`.
- Decide game direction or player-facing behavior.
- Approve its own plan's results; QA verifies the build.

## Works from

- An approved spec with acceptance criteria, or a technical problem to diagnose.
- Project constraints, repository location, relevant Decisions.

## Produces

- A plan: affected systems, ordered tasks, risks and mitigations, test strategy, parallelization
  decision with its reason.
- Technical Decisions where a real alternative was rejected.

## Hands back / escalates when

- The spec is infeasible within constraints → `game-designer`.
- The cost or scope exceeds what the Goal implies → `game-director`.
- The work is irreversible or high-risk → Owner, via an Escalation it prepares.

## Typical skills

technical-plan, make-decision, prepare-owner-escalation
>>>END

<<<FILE goals/G-002-final-boss/62-technical-director-to-studio.md
---
kind: handoff
goal: G-002
seq: 62
from: technical-director
to: studio
stage: Route
outcome: question
---
# 62: technical-director → studio — 検証供給の復旧と試験道具対応の計画

## Task

下記のOwner宛Escalation案を提示し、検証資料・実行・完全証拠の供給条件を調整する。回答後は供給確認、Engineerの試験道具対応、再測定、独立QAの順で進める。

## Context

58・60は独立検証未完了を報告し、59で要求した入力・実行・完全ログの供給が60でも不足した。同じ資料だけで第三のQAを開かない。

D-021によるテキスト・スクリプト方式とStudio内検証の承認は維持する。今回必要なのは承認の取り直しではなく、その実行経路と証拠参照を利用可能にする調整である。

## Findings

### このStepで確認した範囲

packetのソース本文・テスト4ファイル・仕様・報告を静的に照合した。製品コード、bot、仕様は変更していない。tests・traceは実行しておらず、保存ファイルからのsource_id再算出、保存基線の探索、完全ログの永続化も未実施である。

本packetではtests・traceに最大3 roundsが明示され、以前不足していたテスト本文の一部も供給された。この改善を60の「0枠」の継続と混同しない。一方、次のQAにも実行枠が付くこと、全tests本文、完全ログの保存先・再閲覧手段、変更前基線の存在は確認できない。以前0枠になった生成・配布機構の根本原因はpacketからは特定できない。

収録出力のsource_id `04fa2b1c168a`とBUILD `0.6-g002-public-32`は60の報告値であり、現在の保存repo/と一致するとの独立確認ではない。

### 技術所見

1. `bots.py::_dangers`のactive chargeは内部`phase_left`から危険経路残長を計算し、`_threat`の候補除外へ使う。`Output.emit`のplayer viewにはactive残時間がない。表示済み情報を記憶・計算する経路も当該分岐にはないため、D-019項目6の公開情報条件に不適合な判断依存がある。現状のボス比較値をpass根拠にはしない。
2. `_hurt_lines`はsourceがbossの場合もshot側へ入り、突進接触の位置・距離・消費を証明できない。被弾源イベントと補助文を分けて扱う。
3. `test_split_c.py`はボス判断ログ全文を結果に残さず、サンプルへ縮約する。完全ログの別保存が必要である。同ファイルの公開再生入力は現在のbotから生成されるため、bot修正後は入力生成と通常ラン測定も更新対象になる。
4. `test_legacy_note_only_changes_leading_line`は同じ現行実装の注記抑制との比較である。`test_default_player_cadence_is_explicit_half_second`も現行の既定値と明示値の比較であり、いずれも変更前基線との一致を単独では証明しない。
5. 長時間試験はheartsを変更した観測用fixtureである。長時間出力の検証と、正規敵を倒した通常連続到達の証拠を分離する。

これらは試験道具・証拠の問題であり、ゲーム本体の戦闘不具合、対処不能、難度不合格を意味しない。

### 影響システムと順序

並列Stepは開かない。試験道具の変更が入力生成・測定・証拠識別へ連鎖するため、次の順序で固定する。

1. **Studio／Owner：供給条件の確認。** 次の担当Stepに全必要本文、独立実行枠、入力・完全出力を書ける許可先、後続packetから参照可能な経路を具体的に割り当てる。Loadへのパス記載だけで本文供給済みと扱わない。全件を一packetへ収められなければ、依存を明記した直列分割にする。
2. **Engineer：証拠台帳と基線調査。** 使用ソース集合を保存し、`source_id.py`の対象全ファイルとtestsを列挙して識別する。変更前保存ソース・出力が供給された場合は由来、入力、FPS、比較可能範囲を確認する。存在しなければL1/O3等を未確認としてStudioへ返す。要件変更の要否はDesignerへ、Goal範囲の判断はGame Director経由でOwnerへ戻す。
3. **Engineer：ボス判断経路の限定。** ボス判断用に公開情報だけの観測データを作り、判断処理へ内部Game／Enemyを渡さない。warningの固定方向・範囲と、発動時の公開イベントから観測済みの経路を保持し、active中はその全経路を保守的に危険候補とする。内部残時間による残長短縮は使わない。recovery等の公開状態変化で解除する。warningを観測せずactiveから開始する診断では、現在の公開情報から固定最大範囲を保守的に扱い、履歴不足を記録する。プレイヤー表示の追加は不要とする。公開契約変更が必要と判明した場合だけDesignerへ返す。
4. **Engineer：診断ログと試験。** 意思決定入力・計算根拠・候補・選択行動を全判断について記録する。接触診断は判断用データから分離し、boss突進のフレーム前後位置、固定方向、距離、保護、接触消費、被弾を記録する。既存イベントで不足する場合は試験用観測で補い、推定値を実接触値と表記しない。
5. **Engineer：再測定。** 同一保存ソース・同一方針・初期位置／向き／状態・limitで、独立5番を30/60 FPS、開始3/2 heartsの4条件で実行する。全判断ログ、終了理由、hearts、被弾源、攻撃・dash、時間を保存する。数値が閾値を超えた場合は診断後Designerへ返し、自動免除しない。
6. **Engineer：保持回帰と公開再生。** 独立1〜4は既存方針を保持する。共有関数に変更が及べば変更前後の行動列・結果と全保持基準を確認する。独立1〜2のcombat14、3・4の各bot成績・dash、独立1〜4のFPS比較、終了・ログ有無一致・brute対応を追跡する。新botで通常ラン入力を再生成し、両FPS・両viewの公開再生と同一試行時間を再取得する。
7. **独立QA：基準ごとの検証。** 実装者の自己評価を根拠にせず、保存識別を再算出し、全testsの条件・assert・基準IDを照合する。不足fixture、公開再生、共有回帰、D-022を両FPSで独立実行する。
8. **全QA合格後：** 限定Art Verify→独立Play→Designer実測後判断→Game Director Review。Artの表示変更があれば該当QAを再確認してからPlayへ進む。初回再測定で明白な対処不能・到達不能が判明した場合はPlay前にもDesignerへ戻す。

### 試験と証拠保存

Engineerが通常Roleの成果として作るもの：

- 基準ID／FPS→ソース・テスト名・条件・assert・入力・完全ログ参照の対応表。
- 公開情報が同じで内部active残時間だけ異なる場合に、ボス判断が変わらない試験。公開データに存在しない属性を読めない境界も確認する。
- warning→active→recovery、距離0、壁、dash待ち、stun、room境界・retryの判断記憶初期化を確認する試験。
- boss突進の通常被弾・保護接触・非接触で、診断がshotとして誤記されず、接触位置と消費を追えるログ。
- 新attemptが旧未来入力時刻を越える試験、またはpending破棄列の直接観測。
- 共有combat、step68／72／94、cap遅延上限、旧5番からの置換先の追跡表。

保存方式は供給側が許可する実パスを確定してから使用する。実行ごとに、完全入力、コマンド、作業ディレクトリ、FPS、開始条件、limit、ソース識別、終了コード、stdout／stderr全文を保存する。台帳にはファイルのハッシュ・バイト数・行数と分割順を記録し、summaryや抜粋だけで全文を代用しない。

大きい出力は完全原本を保持して連番分割し、後続Stepへ必要部分を全文供給する。ハッシュは同一性確認に使い、閲覧可能性の代用にはしない。保存・再読込みの小規模確認に成功するまで、長大な再測定を始めない。

### リスクと対策

- 保守的な危険経路保持でbot成績・反撃機会が変わる：実測を更新し、ゲームのHP・時間・表示をbotに合わせて変えない。
- 共有判断処理への影響：ボス専用境界を優先し、独立1〜4の変更範囲と回帰結果を明記する。
- source_idはtests変更でも変わる：測定前にソースを固定し、異なる識別の結果を混ぜない。
- 完全ログの再切断：原本保存と再閲覧を先に確認し、収録不能なら直列分割して未確認を残す。
- 変更前資料の不在：現行greenや同一コード内比較で埋めず、該当基準を未確認として判断先へ返す。
- 約87／104秒という既報と15〜20分Visionの差：人間の所要時間と同一視せず、再測定と独立Play後にDesignerへ渡す。新たな秒数ゲートを設けない。

### 独立QAの再開条件

次の全項目をStudioが確認してから、60の未確認表を添えて再開する。

- 全必要ソース・全tests・仕様本文が実際に閲覧できる。
- QA自身が必要な追加実行を行える枠とコマンドが割り当てられている。
- 入力・完全ログの書込先と後続参照経路が確認されている。
- ボス公開情報対応と4条件の再測定資料が揃い、独立1〜4への影響が追跡できる。
- 変更前比較資料が供給されているか、不在と判断待ちの基準が明示されている。

基線不在でも他項目の検証は進められるが、L1/O3等を含む全基準passは保留する。枠を使い切り、入力・機能の不足なく残作業だけがある場合は、完了条件を示して直列の継続Stepへ渡す。

### Owner宛Escalation案（Studio Routeで提示する）

---
kind: escalation
goal: G-002
seq: 62
from: technical-director
to: owner
status: open
decision: none
---

# 62: Owner decision needed — 承認済み検証の供給をどう整えるか

#### Question

G-002について、承認済みのテキスト方式を維持して全資料・独立実行枠・完全ログの保存参照経路を調整する案A、検証可能な範囲へGoalを狭める案B、供給が整うまで停止する案Cのどれを選びますか。

#### Why this needs the Owner

58・60で同じ供給不足が二度報告されたことが、再び同じQA依頼を出さずEscalationする手続上の理由です。修正後に同じ受入基準が二度失敗した事例ではありません。

Roleが解消できない具体的な障害は、担当Stepに付与される実行枠、packetへの全必要本文の収録、許可書込先、完全ログを後続Stepへ届ける参照経路を、このTechnical Director Stepから設定できないことです。以前のQAでは実行枠0、tests本文不足、ログ切断が報告されました。今回のStepには最大3 roundsと一部tests本文があり改善していますが、次のQAで必要機能が揃うとの確認はありません。0枠の根本原因と保存基線の所在も不明です。

D-021が再検討条件とする「通常のStudio Stepでは実行できない具体的な障害」に関する調整です。bot修正、試験作成、基準対応表、ログ生成は通常Roleの仕事として計画済みであり、Ownerへ技術方式の選択は求めません。実機、gamepad、外部配員、追加金銭、旧指定sha照合も求めません。

#### Options

**案A — D-021を維持して供給条件を整える（推奨）**

全必要ソース・tests本文、担当Step内の追加実行枠、完全入力・stdout／stderrを書ける場所、後続Stepが全文を参照できる経路を調整します。一度に収まらなければ直列Stepに分割します。L1/O3等の変更前保存ソース・出力は、所在と提供可否を回答対象に含めます。

失う検証範囲は予定しません。ただし基線がなければ該当基準は未確認として残り、別途判断が必要です。費用は通常Step内で、追加金銭は使いません。リスクは供給機構の制約が残ることで、実現性はまだ確認できていません。計画・資料分割は変更可能です。

選択後：Studioが供給担当・具体的経路・利用可能な枠を確定し、小規模な保存／再閲覧確認→Engineerの試験道具対応→再測定→独立QAへ進みます。

**案B — 今回のGoalを検証できる範囲へ狭める**

利用可能な本文、実行枠、保存参照経路を明示したうえで、Game DirectorとDesignerが検証可能な成果へGoal・該当基準を再定義します。最低限、残す成果の入力と証拠を保存・再閲覧できる供給が必要です。

変更前基線が得られなければL1/O3等の変更前一致を、独立実行・全証拠が得られなければ該当する全基準検証と体験判断を、今回の完了範囲から外す可能性があります。具体的な除外一覧は再計画で確定します。従来G-002全体の合格は主張できません。通常Step内で調整できますが、後日の再検証と判断のやり直しがリスクです。未検証の記録を保持すれば範囲の再拡大は可能です。

選択後：Studio→Game Director→Designerによる範囲・Decision整理→Technical Director再計画。QAへ基準免除を直接依頼しません。

**案C — 供給が整うまで停止する**

新たな実行・保存機能の即時供給は求めず、現状の資料と未確認一覧を維持します。今回失うのは残りの検証を進める機会で、基準自体は維持します。追加金銭は不要ですが、Goal達成時期は未定となります。供給再開条件を満たせば再開可能です。

選択後：StudioがOwner待ちとして停止を管理し、資料・実行・保存参照経路が確認できた時点でTechnical Directorへ戻します。

#### Studio recommendation

案Aを推奨します。D-021の承認を維持し、ゲーム仕様やGoalを狭める前に、承認済みの検証経路を実際に供給できるか確認するためです。これはTechnical Directorの提案であり、Ownerの決定済み事項ではありません。

#### Reasoning

今回のpacketには実行枠と一部tests本文があり、供給改善の兆候があります。しかし次のQAの枠、全文収録、永続参照は未確認なので、復旧可能とは断定しません。

供給機構が完全証拠の保存・再読込みや必要な独立実行を提供できないと確認された場合は、案BまたはCへ推奨を見直します。変更前基線だけが存在しない場合は、その基準に限定した再判断を先に検討します。

回答待ちの間に通常Roleが進められるのは、既供給本文に基づく基準対応表と試験道具修正briefの準備です。新規の並列Stepは開かず、第三のQA再依頼や合格後の工程へは進めません。

#### Owner decision required

A／B／Cと条件を回答してください。Aの場合は、全本文・実行枠・完全ログ保存参照経路を誰がどう調整するか、および変更前資料の提供可否を指定してください。現時点で不明な項目は、確認担当と確認方法の指定で構いません。

## Decisions already made

- D-019：公開情報限定のボスbot、開始3/2 hearts別FPS比較、独立1〜4保持回帰、実測後Designer判断を維持。
- D-021：テキスト・スクリプト方式とStudio内独立QA・Playを承認。実機供給・旧指定sha照合・追加金銭は要求しない。
- 仕様§11／D-022：旧経路注記、弾ライフサイクル、長時間観測の契約を保持。
- 本Stepは新Decisionを採択せず、上記の技術計画と未決Escalation案を返す。

## Constraints

- QAのfailと未確認を上書きしない。実行・保存・基線探索を実施済みと扱わない。
- 製品コード・bot・仕様は変更しない。後続Engineerで試験道具を対応する。
- プレイヤー向け契約変更はDesigner、Goal範囲変更はGame Director経由で判断する。
- 新たな難度・時間ゲートを設けず、変更前比較を現行suite成功で代用しない。
- QA用資料と独立Play資料を分ける。Playへ期待結果、QA判定、実装履歴、Review用体験信号を渡さない。
- Ownerへの実際の提示とGoalのblocked-on-ownerへの変更はStudio Routeが行う。

## Open questions

1. 次のEngineer・QA Stepへ全必要本文、実行枠、完全ログの保存参照経路を具体的に供給できるか。
2. 以前のQAで0枠・本文未収録・出力切断となった配布上の原因と、再発防止を確認する担当は誰か。
3. L1/O3等に比較可能な変更前ソース・完全出力は存在するか。不在なら該当基準の扱いをDesignerへどう戻すか。
4. Ownerは案A／B／Cのどれを選ぶか。

## Expected output

Studioは本Handoff内のEscalation案をOwnerへ提示し、供給障害に対する選択と条件を記録する。回答前に同じQA依頼を繰り返さない。

案Aなら具体的な供給確認を先に行い、本計画をEngineerの試験道具対応briefへ落とす。再測定と独立QAの再開条件を満たしてから検証を再ルートする。全QA合格後の限定Art Verify、独立Play、Designer実測後判断、Game Director Reviewを保持する。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Skills: studio/skills/prepare-owner-escalation.md
- Template: studio/templates/escalation.md
- Project: project.md
- Project: design/final-boss-and-continuous-run.md
- Project: repo/README.md
- Project: repo/manual.md
- Project: repo/public-driver.md
- Project: repo/bots.py
- Project: repo/run_driver.py
- Project: repo/source_id.py
- Project: repo/tests/test_bots_boss.py
- Project: repo/tests/test_split_c.py
- Project: repo/tests/test_d022_observation.py
- Project: repo/tests/test_d022_shots_and_note.py
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Previous handoff: goals/G-002-final-boss/61-studio-to-technical-director.md
- Supporting report: goals/G-002-final-boss/60-qa-to-studio.md
- Supporting report: goals/G-002-final-boss/58-qa-to-studio.md
- Supporting request: goals/G-002-final-boss/59-studio-to-qa.md
>>>END

<<<FILE decisions/D-023-owner-confirms-verification-supply.md
---
kind: decision
id: D-023
status: accepted
decided_by: owner
goal: G-002
date: 2026-10-23
supersedes: none
---
# D-023: 実際の供給上限に合わせてテキスト検証を継続する

## Decision

Ownerは63の案Aを選び、D-021を維持して進めると決定した。ただし、利用可能な供給は以下に限られる。

- Loadに個別指定したファイルは本文が届く。ディレクトリ指定では中のファイル名だけが届く。
- Stepは@needを一度、最大8ファイルまで使用できる。
- @runは1 Stepにつき最大3回。別の実行枠はない。
- 実行結果は先頭と末尾を含む最大2万字。全文保存先はない。長い出力は確認対象の行を出すスクリプトで絞る。
- 変更前ビルドは保存されていない。変更前一致の基準について、記録数値との比較にするか、確認不能として扱うかはGame Designerが決める。

案Aに記載された全文保存・再閲覧機構の新設は実行条件としない。利用可能な出力から何を検証できるかは各担当Roleが判断し、未確認を合格として扱わない。製品仕様、難度、秒数ゲート、Goal達成の判断を本Decisionで変更しない。

Ownerの原文：

> 案A。供給の事実を答えます。(1) 本文: Load に書いたファイルは本文が届きます。ディレクトリ（repo/ など）を書くと本文は届かず、中のファイル名だけが届きます。足りない本文は、Step が @need で 1 回、8 ファイルまで追加で求められます。Route は、検証に要るテストなどのファイルを 1 つずつ Load に書いてください。(2) 実行: 1 回の Step で @run を 3 回まで使えます。別の実行の枠はありません。(3) ログ: 実行結果は先頭と末尾を含む 2 万字までで、全文の保存先はありません。長い出力は、確かめたい行だけを出すスクリプトで絞ってください。(4) 変更前のビルドは保存されていません。変更前との一致を求める基準は、記録にある数値と比べるか、確かめられないものとして扱うかを Designer が決めてください。以上の範囲で、D-021 のまま進めてください。

## Rationale

Ownerが利用可能な供給条件を確定した。存在しない実行枠、保存機構、変更前ビルドを待つ反復を止め、本文の個別指定、出力の絞り込み、必要な直列分割で進める。変更前一致の扱いは、指定された仕様責任者の判断を先行させる。

## Alternatives considered

- 案BのGoal縮小：Ownerは選択していない。検証未完了を理由にStudioが範囲や基準を免除しない。
- 案Cの停止：Ownerは継続を指示した。
- 全文保存先や変更前ビルドの供給を再要求する：確定した供給事実と合わないため採らない。

## Revisit when

担当Roleが、出力の絞り込みや直列分割でも必要な判断を成立させられない具体的な理由を示した場合。または供給条件が変わった場合。変更前一致の個別基準の扱いは、まずGame Designerが判断する。
>>>END

<<<FILE decisions/D-024-g002-historical-comparison-evidence.md
---
kind: decision
id: D-024
status: accepted
decided_by: game-designer
goal: G-002
date: 2026-10-23
supersedes: none
---
# D-024: 変更前一致要求の証拠と確認不能の扱い

## Decision

D-023の委任に従い、変更前ビルドが存在しないG-002の比較基準を個別に確定する。詳細な適用表と比較条件は`design/g002-historical-comparison-evidence.md`を正本とする。

1. L1の注記以外の変更前出力・結果・終了時刻の一致、O3の変更前出力一致、step68 V-cの旧出力一致、step94 W7の変更前挙動一致は、対応する比較原本・必要な測定記録がなく、確認不能として残す。現行実装内の比較やsuite成功で置き換えない。
2. 独立1〜4のdodger成績については、40の記録数値との比較を採択する。これは保存ソース`5145454ab956`の記録との比較であり、ボス対応前の実装・方針との一致証明ではない。56の保存ソース`04fa2b1c168a`の報告は後続の補助記録として区別する。
3. 時間は40の小数1桁の報告精度へ丸めて比較し、結果・hearts lost・dash回数は記録値と比較する。記録のない行動列・位置・照準・未丸め時間の一致は確認不能とする。記録差はEngineerが条件と変更影響を整理しDesignerへ返し、製品の規則違反とは区別する。
4. 現行仕様へ直接照合できる要求と、同一現行ビルド内の対照試験は引き続き検証する。歴史的一致の確認不能によって、60秒上限、既定0.5秒、共有戦闘、公開文字列、FPS比較等を免除しない。
5. 非公開active残時間に依存する既報のボスbot数値、およびそれから生成した通常ラン入力・時間は診断資料に留め、新たな合格基線にしない。対応後に再測定する。

確認不能は合格、免除、適用終了、Goal達成を意味しない。QAは該当部分を他の検証結果から分離して記録する。全基準passを前提とする後続工程については、Studioが未解決部分を明示して扱う。Goalの再解釈や範囲縮小が必要になればGame Directorへ戻し、Designerが決定しない。

## Rationale

出力全文の同一性は少数の数値から復元できない。一方、独立1〜4のdodgerには、FPS・開始条件・limit・部屋別結果が明記された数値記録があり、その精度に限定した比較は成立する。

現行実装の注記を抑制した比較や、既定値と明示値の比較は現在の挙動を検証できるが、保存されていない過去実装を再現しない。

## Alternatives considered

- 現行suite成功で変更前一致も合格とする：比較対象がないため不採択。
- 全項目を記録数値比較にする：L1等の出力・行動の同一性に必要な記録がないため不採択。
- 全項目を確認不能とする：独立1〜4の記録精度で成立する比較まで捨てるため不採択。
- 基線不在を理由に仕様・難度・秒数ゲートを変更する：D-023の委任範囲外であり不採択。

## Revisit when

由来・入力・測定条件を確認できる追加の過去記録が届いた場合。記録比較で差が出た場合。確認不能部分がGoalの最終判断を妨げ、方向・範囲の判断が必要になった場合。
>>>END

<<<FILE design/g002-historical-comparison-evidence.md
# G-002 変更前一致要求の証拠適用補足

Status: D-024により確定。実装・実行・QA判定は行っていない。

本書は`final-boss-and-continuous-run.md`§7〜8・§11と、保持対象のstep68・72・94にある変更前比較の証拠の扱いを補足する。ゲーム規則、戦闘パラメータ、難度、Goal範囲は変更しない。D-019の適用終了部分を復活させない。

## 意図と判定区分

現行の読み取り・回避・反撃と連続ランを検証しつつ、過去資料で証明できる範囲を明示する。

- 記録比較：出典にある条件・精度の数値との比較。
- 確認不能：必要な変更前資料がなく、歴史的一致を判定できない。
- 現行検証：現在の仕様値、文字列、または同一ビルド内の対照条件を検証する。

一つの基準に複数の区分が併存する。現行検証の成功で確認不能部分をpassにしない。

## 基準別の扱い

| 基準 | 従来要求 | 採用する扱い | 根拠資料 | 比較条件・精度 | 未確認として残る点 |
|---|---|---|---|---|---|
| D-022 L1 | 旧room 5で注記以外の出力、結果、終了時刻が変更前と一致。60秒上限不変 | 歴史的一致は確認不能。注記の内容・位置・回数、現行の60秒上限は検証する | 仕様§11.1、D-022、62のテスト所見 | 同一入力を各FPSで実行。注記抑制との比較は現行内対照として記録 | 注記以外の過去出力全文、過去結果・終了時刻との一致 |
| D-022 L4 | manualの注記がL1の一致を保つ | 文書と経路説明は現行照合。L1の歴史的一致を保証する部分は確認不能 | 仕様§11.1、60の文書判定 | manualと表示条件・対象経路を照合 | 文書の一致から旧実装の不変性は証明できない |
| D-022 O3 | 指定なしの出力が変更前と同じ、周期0.5秒 | 変更前出力一致は確認不能。既定0.5秒と明示0.5秒の現行内対照は検証する | 仕様§11.3、62のテスト所見 | 各FPSで同一入力。追加要約等はD-022の契約として別に照合 | 過去出力全文・描画順の一致 |
| step68 V-a／V-b | 予兆・被弾表示の時点とhearts suffixを保持 | 定義済み文言、接触フレーム、予兆時間、suffix形式は現行検証。「以前と同時点」の実測一致は確認不能 | step68 §4、combat.md、step94 | 各variant・各FPS。現行時間は該当仕様の±1フレーム | 過去の個別表示フレームとの一致 |
| step68 V-c | 指定語以外の出力が0.6.1とbyte単位で一致 | 確認不能 | step68 §4 | 比較用旧出力がない。数値一致をbyte一致へ拡張しない | 出力全文の同一性 |
| step68 V-e末尾 | 共有基準保持、bot結果不変 | 共有基準は現行検証。独立1〜4 dodgerは下表の記録比較。それ以前のbot結果不変は確認不能 | D-019、40、56 | 下記の条件と精度。旧5番・終了した集計は対象外 | 0.6.1等の旧方針・全bot結果との一致 |
| step94 W3／W4 | 反応が以前どおり、吸収時のhit表示なし | prefix、反応動作、吸収時の無表示は現行検証。過去の全反応行動列一致は確認不能 | step94、D-005のcombat.md反映、D-019 | 指定substringと接触条件を各FPSで確認 | 過去スクリプトの全行動列との一致 |
| step94 W7 | 変更前と時刻・hearts・弾数等が同じ、bot方針・結果不変 | 歴史的一致は確認不能。現行共有基準は保持。独立1〜4 dodgerだけ下表の記録比較 | step94、D-019、40、56 | 過去の各イベント時刻・弾数記録がなく、±1フレーム比較は成立しない | 変更前挙動、全bot方針、未記録結果の一致 |
| 独立1〜4 dodger保持、40・56の比較記述 | ボス対応が既存部屋へ影響しないこと | 40の記録数値との比較を採択 | 40の保存実行、56の保持回帰報告 | 同一部屋・FPS・3 hearts・通常初期状態・limit 60秒。下表参照 | ボス対応前の厳密一致、全行動列、未丸め時刻 |
| R2、step72 R3-1の保持部分 | 第1〜4部屋の構成・配置・既存パラメータを保持 | 正本仕様への現行照合。変更前ビルド待ちは不要 | combat.md、step72、仕様§8、D-019 | 敵種・座標・順序・数値を仕様へ照合 | ソース全文の歴史的一致は主張しない |
| step72 R3-6 | 同じ静止入力でgrub有無のcue開始時刻が一致 | 同一現行ビルド内の対照試験として保持 | step72 R3-6 | 最初のlungeまで、各FPSで±1フレーム。制御fixtureと明示 | 過去ビルドとの比較ではない |
| combat16c／新5番FPS比較 | 同条件で30/60 FPSの結果が一致 | 現行ビルド内比較として保持 | D-019、仕様§8、60・62 | 独立1〜4保持。新5番は公開情報対応後、開始3/2 hearts別に再測定 | 対応前ボス数値は新しいpass根拠にならない |

L2、L3、S1〜S5、O1、O2、O4〜O6、その他の現行仕様検証は継続する。S5の既存文言保持は正本文字列へ照合できるが、旧出力全文一致まで証明するものではない。

step72の位置変更の説明、過去の観測値、combat.mdの歴史的結果は変更説明・記録として保存する。D-019で適用終了した旧集計、旧第5部屋、過去G-001の合格判断を新たな比較ゲートにしない。

## 独立1〜4 dodgerの採択記録

出典は40、保存source id `5145454ab956`。各部屋・各FPSは1試行。開始3 hearts、通常位置(8,4)・右向き、独立部屋、limit 60秒。全行clear、損失0、終了3 heartsである。

| FPS | 部屋 | 秒数（小数1桁） | dash回数 |
|---|---:|---:|---:|
| 30 | 1 | 6.6 | 3 |
| 30 | 2 | 20.7 | 10 |
| 30 | 3 | 15.6 | 6 |
| 30 | 4 | 18.3 | 7 |
| 60 | 1 | 9.6 | 5 |
| 60 | 2 | 25.1 | 14 |
| 60 | 3 | 15.0 | 6 |
| 60 | 4 | 17.0 | 8 |

現在の時間を最も近い0.1秒へ丸めて比較する。ちょうど中間の場合は大きい側へ丸める。これ以上細かい過去時刻を復元しない。整数の結果・hearts・dashは記録値と照合する。丸め一致は±1フレーム一致を意味しない。

56はsource `04fa2b1c168a`で全clear・損失0、同じdash数を報告し、時間も40の精度で一致する。56の小数2桁時間と攻撃回数は後続記録として識別を保つ。40にない部屋1・2の攻撃回数を40の値として扱わない。

この比較は新しい難度・秒数ゲートではなく、保持回帰の記録比較である。差があれば条件・方針・共有処理への影響を報告しDesignerへ返す。現行の共有規則違反はQAが別途判定する。比較のために戦闘やbot行動を数値へ合わせない。

## 証拠の限界と後続への受け渡し

各比較の報告には基準ID、FPS、入力・初期条件、limit、現在のソース識別、参照記録、測定値、丸め値、結論と未確認範囲を記載する。歴史比較と現行内対照を別列にする。

D-023の最大3回・各出力2万字という条件で、検証対象を絞った出力と直列分割を使う。切断された部分や表示されなかった判定を確認済みと扱わない。存在しない全文保存先や変更前ビルドを要求しない。具体的な試験構成はTechnical Directorが決める。

確認不能項目を最終Reviewへ渡す一覧から削除しない。QAの60のfailを本書で上書きせず、全基準passも宣言しない。Goalの意味・範囲の判断が必要ならStudioからGame Directorへ返す。

難度・追加数値ゲートと15〜20分Visionの判断は、対応bot再測定・独立QA・独立Play後の予定Stepに残す。本書の内容を独立Playの資料へ転記しない。
>>>END
