# Studio operation packet

operation: Route
goal: G-002
step_artifacts: goals/G-002-final-boss/70-gameplay-engineer-to-studio.md
next_seq: 71
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha b16847e998d2; run through the project's run commands)
log: last 5 of 38 entries in @log-recent; the full history is goals/G-002-final-boss/log.md

## You may write

- goals/G-002-final-boss/goal.md
- goals/G-002-final-boss/70-gameplay-engineer-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- project.md: only in the Route that closes the Goal, and only its ## Current state (at most 1,500 characters)
- goals/G-002-final-boss/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 71
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
goals/G-002-final-boss/66-studio-to-technical-director.md
goals/G-002-final-boss/67-technical-director-to-studio.md
goals/G-002-final-boss/68-technical-director-to-studio.md
goals/G-002-final-boss/69-studio-to-gameplay-engineer.md
goals/G-002-final-boss/70-gameplay-engineer-to-studio.md
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
- Design（変更前一致）：done。65とD-024で、歴史的一致の確認不能、独立1〜4 dodgerの40の記録精度での比較、現行仕様照合・現行内対照を分離した。確認不能はpass・免除にせず最終Reviewへ残す。
- Plan（供給条件への適合）：done。68が62の実行計画を置換する。E0棚卸し→E1公開情報bot→E2接触診断→E3ボス4条件→E4保持回帰→E5公開再生→独立Q1〜Q6を直列実行する。各Step最大3回・各出力2万字以内、欠落は未確認。存在しない保存機構や変更前ビルドを前提にしない。
- Build（試験道具・再測定）：open。69でEngineerのE0のみ開始する。実在する全テストファイル・全テストID・基準対応と未対応を棚卸しし、対象別証拠出力を整える。E1以降はE0の結果を受けて個別に開く。
- Decide（後続工程条件）：planned。歴史的確認不能を残して限定Art Verify以降へ進む条件をGame Directorに判断してもらう。Engineer・QAは先行可能。現行検証の完了を全基準passやGoal達成に読み替えない。
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
| 7b-design | Design | game-designer | make-decision, write-design-spec | done | 64-studio-to-game-designer.md → 結果: 65-game-designer-to-studio.md（D-024） |
| 7b-plan | Plan | technical-director | technical-plan | done | 66-studio-to-technical-director.md → 結果: 68-technical-director-to-studio.md |
| 7b-e0 | Build | gameplay-engineer | implement-change | open | 69-studio-to-gameplay-engineer.md |
| 7b-build | Build | gameplay-engineer | implement-change | planned | 68のE1→E2→E3群→E4群→E5群を直列分割 |
| 7c | Verify | qa | verify-change | planned | E0の全試験台帳を使い68のQ1〜Q6を直列分割 |
| 7d | Decide | game-director | make-decision, prepare-owner-escalation | planned | 歴史的確認不能を保持した後続評価工程の条件判断 |
| 8 | Verify | art-director | visual-review | planned | — |
| 9 | Play | playtester | playtest-session | planned | — |
| 9a | Design | game-designer | make-decision, write-design-spec | planned | — |
| 10 | Review | game-director | review-outcome | planned | — |
| 11 | Next | studio | — | planned | — |

逐次実行する。68に従いE0→E1→E2→E3群→E4群→E5群→独立Q1〜Q6を進める。E0の全試験台帳からQAの個別Loadを割り当て、追加試験も含め未配布を残さない。現行必須検証、公開情報条件、再測定、記録差へのDesigner回答が揃い、歴史比較以外の不足を解消した後、Game Directorが歴史的確認不能を保持した評価継続の条件を判断する。認められた場合、限定Art Verify→独立Play→Designer実測後判断→Reviewへ進む。各StepのLoadは個別ファイル指定。全文保存先・別実行枠・変更前ビルドを待たない。明白な対処不能・到達不能や規定外の比較差はDesignerへ戻す。並列Stepは開かない。

## Route changes

68で再計画を完了し、62の実行計画を置換する。69でEngineerのE0棚卸し・対象別出力整備を開き、以降の対応・測定・独立QAは直列分割する。歴史的確認不能を保持した後続評価の条件判断をGame Directorに残し、同じ不足のまま第三のQA依頼は出さない。

## Next action

Gameplay Engineerが69-studio-to-gameplay-engineer.mdでE0を開始する。全テストの実在名・IDと基準対応を棚卸しし、対象別証拠出力を整えてStudioへ返す。Studioは結果からE1の個別Loadと、後続QAへの全試験配布台帳を具体化する。

## Outcome

未完了。供給上限に適合した68の計画を受け、Engineerの試験棚卸しから開始する。変更前の厳密な同一性は確認不能として保持し、独立1〜4 dodgerは記録精度に限定して比較する。全文保存先や変更前ビルドの供給は待たない。試験道具対応・再測定、独立QA、後続評価の工程条件判断、限定Art Verify・独立Play・実測後Designer判断・Reviewは未完了。確認不能を合格やGoal達成とは扱わず、戦闘本体の不具合・難度・通常ラン時間とVisionとの差の判断を残す。project.mdは変更しない。
>>>END

<<<FILE @log-recent
## 076-route · 2026-10-21

Status: blocked-on-owner. Open: none.

62の技術計画とOwner宛brief準備を完了として記録し、63で検証供給の調整・範囲縮小・停止をOwnerへ提示する。Goalをblocked-on-ownerにし、依存Stepを停止。今回の供給改善と後続供給の未確認を区別し、第三のQA再発行は行わない。

## 078-resume · 2026-10-23

Status: active. Open: 64-studio-to-game-designer.md.

63へのOwner回答をD-023に記録し、Goalをactiveへ戻す。64でDesignerに変更前一致基準の扱いを委ね、その後に62を実際の供給上限へ適合させる再計画を置く。全文保存や変更前ビルドの供給待ちは解消し、同じ不足のまま第三のQA依頼は出さない。

## 080-route · 2026-10-23

Status: active. Open: 66-studio-to-technical-director.md.

65のDesignを完了とし、D-024の記録比較・確認不能・現行検証の区分を採用する。66でTechnical Directorへ62のD-023・D-024適合再計画を開く。歴史的一致の未確認を保持した後続工程条件を整理し、同じ不足のまま第三のQA依頼は出さない。

## 082-route · 2026-10-23

Status: active. Open: 66-studio-to-technical-director.md.

65のDesignを完了とし、D-024の記録比較・確認不能・現行検証の区分を採用する。66でTechnical Directorへ62のD-023・D-024適合再計画を開く。歴史的一致の未確認を保持した後続工程条件を整理し、同じ不足のまま第三のQA依頼は出さない。

## 084-route · 2026-10-23

Status: active. Open: 69-studio-to-gameplay-engineer.md.

68で再計画を完了し、62の実行計画を置換する。69でEngineerのE0棚卸し・対象別出力整備を開き、以降の対応・測定・独立QAは直列分割する。歴史的確認不能を保持した後続評価の条件判断をGame Directorに残し、同じ不足のまま第三のQA依頼は出さない。
>>>END

<<<FILE goals/G-002-final-boss/70-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-002
seq: 70
from: gameplay-engineer
to: studio
stage: Route
outcome: partial
---
# 70: gameplay-engineer → studio — E0棚卸しと対象別証拠出力道具

## Task

E0の棚卸し・暫定対応・出力道具を確認し、68に従ってE1へ進める。後続QAには下記台帳の個別ファイル本文を配布する。

## Context

69から受領したE0のみを実施した。製品で観測できる挙動の変更はない。製品ソース、bot方針、既存テストは変更していない。

60のfailは維持する。公開情報botの修正、接触診断、再測定、通常ラン入力の再生成は今回行っていない。本文供給と既知の試験不足を分離し、未確認をsuite成功でpassにしない。

## Findings

### 1. 成果と識別

変更ファイルは `repo/tests/test_g002_evidence.py` のみ。packetに「proposed in a run round; not written」として供給された全文を、そのまま最終成果として保存する。これにより収録Round 1と同じ試験道具を保持する。Handoffはsource_idの対象外である。

収録Round 1の固定コマンド：

```text
cd repo
python3 -m unittest discover -s tests
```

実行時source_idは `c12166443a05`。Exit 0、154 tests、unittest報告2.971秒、実行枠表示3.1秒。これは実装者側の確認であり独立QAではない。最終保存後の識別・実行結果はruntimeのBuild checkと照合する。過去source `04fa2b1c168a` と今回の識別を混同しない。

識別対象は次の19ファイル。F番号の13ファイルに、`game.py`、`session.py`、`play.py`、`run_driver.py`、`bots.py`、`source_id.py`を加える。source_idは相対パスと本文を順番にハッシュする。manual、設計資料、Handoff、非Pythonファイルはこの識別の対象外であり、同一性を保証しない。

### 2. 実在ファイル棚卸し

以下は予定一覧ではなく、Round 1で実在を列挙した結果。全13件表示、未表示0件。69の既存12ファイルに証拠道具1件が追加され、既存一覧との差はこの1件のみだった。

```text
FILES_BEGIN
columns: F number repo-relative-path
F 01 tests/test_boss.py
F 02 tests/test_boss_contract.py
F 03 tests/test_boss_contract_details.py
F 04 tests/test_bots_boss.py
F 05 tests/test_d022_observation.py
F 06 tests/test_d022_shots_and_note.py
F 07 tests/test_g002_evidence.py
F 08 tests/test_game.py
F 09 tests/test_play_run_controls.py
F 10 tests/test_run_driver.py
F 11 tests/test_session.py
F 12 tests/test_split_c.py
F 13 tests/test_terminal.py
FILES_END total=13 shown=13 unshown=0 excluded=non-Python-files
```

ファイル列挙の対象はsource_idと同じ `tests/*.py`。discoverはunittestの標準探索を使用する。今回discoverした全IDは次節にある。将来サブディレクトリへ試験を追加する場合、現行source_idのglob対象との差を別途解消する必要がある。今回そのような追加試験が存在するとの主張はしない。

### 3. discoverされた全テストID

列Gは `module.class`、列Iは連番とmethod。完全なテストIDは直前のGに `.` とmethodを連結したもの。以下の番号は本Handoffの対応表でも使用する。総154件、全154件表示、重複0、loader.errorsは空。FPS別subTest件数を154に加算していない。

```text
TEST_IDS_BEGIN
columns: G module.class; I number method; full-ID=G+"."+method
G test_boss.BossTest
I 001 test_boss_kill_and_existing_lethal_shot_is_death_only
I 002 test_charge_contact_keeps_full_active_duration
I 003 test_four_swipes_fit_in_recovery
I 004 test_initial_single_boss
I 005 test_lifetime_expiration_precedes_contact
I 006 test_nonlethal_swipe_preserves_warning
I 007 test_short_shot_contact_does_not_accelerate_recovery
I 008 test_wall_and_blocked_contact_keep_full_charge
I 009 test_warning_duration_and_locked_aim
G test_boss_contract.BossAdditionalContractTest
I 010 test_attack_order_survives_low_hp
I 011 test_lethal_warning_swipe_prevents_new_attack
I 012 test_nonlethal_swipe_preserves_every_phase
I 013 test_one_tile_sidestep_during_each_warning
I 014 test_zero_distance_locks_right_for_both_attacks
G test_boss_contract.BossContractTest
I 015 test_early_contact_does_not_advance_recovery
I 016 test_uncontacted_shot_expiry_coincides_with_recovery
G test_boss_contract_details.B10ContactBandTest
I 017 test_charge_inside_and_outside_the_band
I 018 test_shot_inside_and_outside_the_band
G test_boss_contract_details.B3ChargeMovementTest
I 019 test_open_charge_moves_2_4_tiles_in_0_3_s
I 020 test_wall_clamps_without_moving_recovery_start
G test_boss_contract_details.B6DashContactTest
I 021 test_dash_through_charge_is_spent_and_harmless_afterwards
I 022 test_dash_through_shot_consumes_it_and_no_later_damage
G test_boss_contract_details.B7ProtectionExpiryTest
I 023 test_charge_touched_in_protection_cannot_hit_when_it_ends
G test_boss_contract_details.B9RecoveryTest
I 024 test_recovery_contact_is_harmless
I 025 test_recovery_lengths
G test_boss_contract_details.C2PauseTest
I 026 test_pause_freezes_protection_timer
I 027 test_pause_in_warning_freezes_and_resume_continues
G test_boss_contract_details.C3LimitTest
I 028 test_limit_in_combat_is_unfinished_with_no_result
I 029 test_same_frame_death_or_victory_is_recorded_beside_the_limit
G test_boss_contract_details.TerminalTest
I 030 test_t1_clear_removes_shots_and_refuses_chasing_damage
I 031 test_t2_same_frame_death_wins_over_victory
I 032 test_t2_survivor_wins_only
I 033 test_t3_terminal_state_is_frozen
I 034 test_t4_retry_from_win_and_death_equals_a_new_run
G test_bots_boss.BossPolicyTest
I 035 test_dodger_in_the_lane_holds_or_dodges_and_never_swipes
I 036 test_dodger_off_the_lane_holds_during_the_warning
I 037 test_threat_follows_the_displayed_locked_lane
G test_bots_boss.OutcomeTest
I 038 test_log_changes_no_result_in_the_boss_room
I 039 test_start_hearts_and_outcome_fields
I 040 test_unfinished_is_reported_at_the_limit
G test_bots_boss.RunDriverTest
I 041 test_play_run_smoke
I 042 test_read_script_hearts_and_mode
G test_bots_boss.SourceIdTest
I 043 test_source_id_is_stable_hex
G test_d022_observation.ObservationTest
I 044 test_controlled_twenty_minutes_at_each_rate
I 045 test_default_player_cadence_is_explicit_half_second
I 046 test_dispatch_and_validation
I 047 test_interval_preserves_events_and_result
I 048 test_legacy_note_only_changes_leading_line
I 049 test_public_spitter_and_boss_share_sequence
I 050 test_retry_resets_periodic_schedule
I 051 test_summary_clocks_counts_pause_and_retry
I 052 test_summary_once_for_clear_death_and_limit
G test_d022_shots_and_note.LegacyNoteTest
I 053 test_note_scope_and_position
G test_d022_shots_and_note.ShotLifecycleTest
I 054 test_clear_room_sequence_and_retry
I 055 test_legacy_emission_has_no_new_events
I 056 test_player_messages_hide_ids
I 057 test_short_shot_removal_and_fixed_recovery
G test_g002_evidence.EvidenceToolTest
I 058 test_bounded_selection_reports_missing_ranges
I 059 test_inventory_all_files_and_discovered_ids
G test_game.BotsTest
I 060 test_bot_log_adds_state_and_changes_no_result
I 061 test_dodger_agrees_at_30_and_60_fps
I 062 test_dodger_never_swipes_a_brute_in_wind_up
I 063 test_every_bot_finishes_a_room
I 064 test_retained_criteria_14_and_15_at_each_rate
I 065 test_walker_logs_the_exact_distance_it_compared
G test_game.BruteTest
I 066 test_a_swipe_does_not_cancel_the_wind_up
I 067 test_a_swipe_in_recovery_changes_nothing_else
I 068 test_a_swipe_that_kills_the_brute_in_wind_up_means_no_lunge_no_message
I 069 test_dash_and_swipe_together_take_no_damage_and_the_brute_takes_the_swipe
I 070 test_two_swipes_in_one_wind_up_each_hit_and_it_lunges_once
G test_game.CombatTest
I 071 test_grub_lunge_costs_a_heart
I 072 test_grub_walking_alone_does_not_hurt
I 073 test_spitter_fires_every_2_4_seconds_from_1_8
I 074 test_swipe_misses_behind_the_player
I 075 test_two_swipes_defeat_a_grub
G test_game.CueGapTest
I 076 test_a_cancelled_cue_is_not_a_shot
I 077 test_a_cap_delay_only_lengthens_the_gap
I 078 test_forced_simultaneous_first_shots_still_keep_the_gap
I 079 test_other_rooms_keep_the_0_8_s_offset
I 080 test_room_4_first_shots_are_1_8_and_3_0_and_keep_the_gap
G test_game.DashTest
I 081 test_attack_during_dash_fires_when_it_ends
I 082 test_dash_covers_four_tiles_at_both_frame_rates
I 083 test_dash_has_a_cooldown
G test_game.GrubTest
I 084 test_a_sidestep_avoids_the_lunge
I 085 test_a_swipe_during_windup_stops_the_lunge
I 086 test_dash_from_cue_into_the_lunge_takes_no_damage
I 087 test_only_one_grub_winds_up_or_lunges
I 088 test_recovery_is_safe
I 089 test_room_3_clears_only_when_spitters_and_grub_are_all_dead
I 090 test_rooms_match_the_spec
I 091 test_standing_still_is_punished
I 092 test_telegraph_comes_at_least_half_a_second_before_the_hit
I 093 test_variants_swipes_to_defeat
I 094 test_wind_up_lengths_differ_by_variant
G test_game.InvulnerabilityTest
I 095 test_a_dash_right_after_a_hit_keeps_both_protections
G test_game.LateSwipeTest
I 096 test_late_swipe_line_comes_before_the_hit
I 097 test_no_line_in_windup_kill_or_recovery
G test_game.LungeContactTest
I 098 test_a_dash_spends_the_lunge_and_the_next_lunge_hurts
I 099 test_a_hurt_window_ending_mid_lunge_does_not_let_the_lunge_hit
I 100 test_a_lunge_that_first_touches_after_the_window_hits
G test_game.PlayerViewMessageTest
I 101 test_a_kill_in_wind_up_prints_no_message
I 102 test_each_swipe_that_hurts_a_winding_up_brute_prints_the_message
I 103 test_swipes_at_a_grub_or_runner_print_no_message
I 104 test_the_banner_shows_0_6
I 105 test_the_message_does_not_change_the_simulation
G test_game.ReactionTest
I 106 test_a_bad_rule_says_how_rules_read
I 107 test_a_rule_acts_at_most_every_reaction_time
I 108 test_cues_show_in_the_player_view
I 109 test_marks_r_and_G_are_drawn
I 110 test_rules_and_timed_inputs_mix
I 111 test_rules_ignore_what_is_not_drawn
I 112 test_rules_react_to_what_is_on_screen
G test_game.ShotContactTest
I 113 test_a_dash_eats_a_shot_even_when_it_ends_inside_the_old_line
I 114 test_a_shot_after_the_window_hits_again
I 115 test_a_shot_in_the_hurt_window_is_consumed_and_nothing_lands_at_its_end
I 116 test_a_shot_that_misses_by_more_than_the_reach_is_not_consumed
I 117 test_a_shot_that_reaches_a_hurtable_player_hits_and_goes
I 118 test_two_shots_together_cost_one_heart_and_both_go
G test_game.ShotSourceTest
I 119 test_absorbed_shot_prints_no_message
I 120 test_direction_words_at_both_rates
I 121 test_player_view_line
G test_game.SpitterTest
I 122 test_a_standing_player_is_hit_by_the_shot
I 123 test_room_3_first_shots_are_staggered_and_cued_0_6_s_before
I 124 test_shot_follows_the_locked_line_and_a_sidestep_dodges_it
G test_game.VariantMessageTest
I 125 test_a_shot_hit_message_is_unchanged
I 126 test_manual_has_the_new_wording
I 127 test_rears_back_rule_matches_all_variants
I 128 test_wind_up_and_hit_messages_name_the_variant
G test_play_run_controls.DriverDiscardTest
I 129 test_old_future_timed_input_is_discarded_on_retry
G test_play_run_controls.PlayRunPauseTest
I 130 test_no_pause_arguments_keep_the_old_result_shape
I 131 test_pause_freezes_run_time_but_counts_driver_time
G test_play_run_controls.PlayRunRetryTest
I 132 test_retries_start_new_attempts_and_reset_reaction_memory
I 133 test_zero_retries_stops_at_the_first_terminal
G test_run_driver.DriverTest
I 134 test_boundary_discards_input_and_accepts_entry_time
I 135 test_control_precedes_combat_input_and_resume_uses_driver_time
I 136 test_limit_exceeds_sixty_seconds
I 137 test_public_parser_dispatch
I 138 test_run_rejects_diagnostic_setup
I 139 test_same_time_source_order
I 140 test_shot_direction_message
G test_session.SessionTest
I 141 test_boundary_healing_and_clocks
I 142 test_boundary_replaces_all_combat_state
I 143 test_limit_records_result_separately
I 144 test_pause_freezes_boundary
I 145 test_pause_freezes_dash_and_queued_attack
I 146 test_retry_rejected_outside_terminal
I 147 test_terminal_retry_matches_new_run
I 148 test_zero_hearts_never_recovers_or_enters
G test_split_c.SplitCTest
I 149 test_boss_actual_decision_logs_and_hearts_comparisons
I 150 test_public_normal_pause_victory_retry_death_retry
I 151 test_retained_independent_dodger_baseline_and_fps_comparison
G test_terminal.TerminalTest
I 152 test_clear_cleans_hazards_and_freezes_every_combat_field
I 153 test_death_precedes_clear_and_existing_shot_still_hits
I 154 test_player_runner_returns_after_terminal_clock_freezes
TEST_IDS_END total=154 shown=154 unshown=0 excluded=subTest-expansion
```

### 4. 暫定対応表：新仕様

全13テストファイルの本文が今回Inputsに届いたため、下表は名前だけからの推測ではなく、供給された操作・assertを読んだ暫定対応である。ただし独立判定でも、仕様の全条件充足宣言でもない。番号は§3の完全IDへ対応する。

| 基準 | 試験番号 | assert・観測と不足 |
|---|---|---|
| R1 | 150 | 公開生成入力再生で3試行、初回clear・全5部屋・ボス入場3 hearts・hurt0。旧bot生成なのでD-024では診断資料。全正規敵撃破とplayer対照列は不足 |
| R2 | 090 | 全部屋の敵種・順序・座標、新5番B/HP12をassert。共有定数の全値照合はこのassertだけでは不足 |
| R3 | 141,148 | hearts1/2/3→2/3/3、回復1回、0で死亡・遷移なし |
| R4 | 142,132,150 | 境界で列挙14フィールドのfresh一致、generation増加、bot retry時Brain生成数。弾・予兆等の残存を全て実際に仕込む試験ではなく、公開driverの境界反応記憶全項目も不足 |
| R5 | 134,139,141,150 | 境界1秒、途中dash拒否、入場同時刻move、同時入力順。入場同時刻処理の厳密な1回件数assertは不足 |
| B1 | 004,010,090 | B位置・HP・1体、HP6で各3回交互予兆。通常HPと低HPの全時間比較は別途 |
| B2 | 009,014,016 | 両warningの移動後aim固定、active到達、距離0右固定。両攻撃の発動時刻列を対象別出力する必要あり |
| B3 | 002,008,019,020 | 2.4移動、壁clamp、最後の前フレームactive・終了recovery。毎フレーム座標列なし |
| B4 | 005,007,015,016,057 | 発射直後位置/age0、速度3、寿命1、期限優先、早期接触と回復1秒不変。057で全消滅理由。実行本文の対象別表示は未整備 |
| B5 | 013 | 両攻撃、ceil(0.25*fps)で1 tile以上・0.4秒以内、aim不変、hearts3 |
| B6 | 021,022,057 | charge spent/blocked1回・無傷、shot実接触消費・後も無傷。実軌道距離と消費前後列はE2へ |
| B7 | 023,057 | charge保護終了後無傷、次charge通常被弾。shot保護吸収は057。shotの保護終了後・次弾の通常命中の連続条件は不足 |
| B8 | 006,011,012 | 全phase・両攻撃でhp以外のenemy辞書不変、warning文言イベント数、warning致死時新発動なし。致死の全phase条件は網羅していない |
| B9 | 003,024,025 | 両回復で4swipe、接触無傷、回復イベント時差。30 FPSは0.35秒を11/30へ量子化 |
| B10 | 017,018 | 内側・外側・上端のhearts。上端は(2,3)いずれも許容。実横ずれ・移動後距離列なし |
| T1 | 030,054,152 | 残弾消去・cleared1回・2秒freeze。通常部屋の全戦闘辞書比較は152 |
| T2 | 001,031,032,153 | 既発射弾と致死swipeで死亡のみ、生存なら勝利のみ、終端件数 |
| T3 | 033,152 | 2秒stepで時刻等不変、入力拒否。152は通常部屋で全辞書と敵辞書比較。033の比較は全状態ではない |
| T4 | 034,129,132,147,150 | win/dead retryのfresh辞書比較、予約破棄、Brain再生成。129は旧入力時刻5より新試行limit1が先なので未来入力破棄の十分な証明にならない |
| C1 | 141,150 | 入場room_t0、境界room_t凍結、run1秒進行、4遷移。全入場時刻列は未表示 |
| C2 | 026,027,131,135,144,145,150 | warning/保護/dash予約/clearのpause凍結とresume、driver2秒、paused入力拒否。全観測状態の対象別表示が必要 |
| C3 | 028,029,040,143 | unfinishedとoutcome分離、limit同フレームdead/won/clear保存 |
| V1 | 108,119–121,125,128,140,150 | 既存cue・印・文字列等の部分試験。ボス全イベント即時画面・重なり・終端retryの両FPS player対照は不足 |
| V2 | なし | D-021の今回テキスト範囲。実機同等性をheadlessでpassにしない |
| L1 | 048,053 | note先頭1回、現行note抑制対照、保護fixtureで60秒上限。歴史的一致は確認不能 |
| L2 | 053 | 全旧部屋・emptyと両viewでnote対象限定 |
| L3 | なし | 同一入力のlegacy/publicボス表示対照assertは未対応 |
| L4 | なし | manual本文が今回未供給。文書現行照合は未実施、歴史保証部分は確認不能 |
| S1,S2 | 049,057 | 共通連番、lifetime/edge/hit/dash/protectionの各発射1回・消滅1回・理由・回復1秒 |
| S3,S4 | 054 | 2部屋の残弾clearedとretry後S1、直後removed再発なし。勝利時全弾等の全終端ケースは不足 |
| S5 | 056,119,125 | messages_forがIDイベントを非表示、旧文言・吸収無hitの部分確認。実player全文のID非露出検査は不足 |
| O1,O6 | 044 | 生存hearts10000 fixture、両FPS・両view1200秒、周期上限、out.seen=全events。内部捕捉全文はStudio収録されず、中間画面・欠落検査も十分ではない |
| O2 | 047 | 間隔0.5/10で全events・結果・playerメッセージ列一致、trace frame/5対照 |
| O3 | 045 | 現行既定と明示0.5の全文一致。歴史的一致は確認不能 |
| O4 | 051,052 | 全終了・両view summary1回、時刻対照、pause/retry/count検査。全数値の独立再計算は部分的 |
| O5 | 046 | 範囲外/NaN/inf/非数/欠損拒否、境界値受理 |
| 道具 | 043,058,059 | source安定hex、窓選択件数・欠落数・END・不正窓拒否、全ID重複/loader errorなし |

### 5. 保持回帰・旧5番・本文未確認

| 対象 | 試験番号・本文で確認した内容 | 未対応・適用整理 |
|---|---|---|
| combat共有 | 066–075,081–088,091–095,113–118,122,124 | 攻撃、grub、dash、保護、弾等。combat.md本文未供給なのでcombat1〜10/17等への厳密な項目別完全対応は未確認 |
| combat11/18 gap | 076–080 | 4番実配置、強制同時、cue中撃破、cap遅延gap、practice offset。077はgapを検査し一般cap上限5をassertしない |
| combat19 | 066–070,101–105 | brute非中断、kill例外、回復、表示回数/時点。105はdescribe文字列のみで「表示がsimulationを変えない」全対照ではない |
| combat20/21 | 098–100,113–118 | 保護接触消費、後続攻撃、同時弾。ボスはB6/B7へ別対応 |
| combat14/15/16c | 061,064,151 | 独立1〜2walker/dodger条件、独立3/4dash、1〜4FPS損失差。151の時間比較は丸め方法未対応 |
| その他BotsTest | 060,062,063,065 | ログ有無結果一致・状態要素・hurt件数・比較距離・brute方針。063はresultにclearedキーがあることだけで終了理由・停止性を厳密には検査しない |
| step68保持文字列 | 093,094,101–105,125–128 | variantHP/時間/文言/suffix/prefix反応の現行部分。step68本文未供給のためV-a〜e全項目対応は未確定 |
| step72 R3-1 | 090 | 現行全配置。1/2/4保持、3と5は正本の適用整理に従う |
| step72 R3-2〜10 | 089,123ほか候補 | room3全敵死亡条件、初射/cue/静止最大3。正本本文未供給で番号別assert対応は未確定。grub有無のcue比較R3-6専用assertは発見できていない |
| step94 W1/W8 | 120,121,140 | 6方向のshot由来語、player例、public文字列。全8方位境界を網羅しない |
| step94 W3/W4 | 119,127ほか候補 | 吸収時hurtなし、rears back substring反応。119は実player全文での無表示をassertしない。step94本文未供給で全条件対応は未確定 |
| step94 W5/W6 | 096,097 | late swipeの順序・文字列・誤prefix禁止、windup/kill/recovery例外 |
| step94 W2/W7 | 108,123–128ほか候補 | 専用全経路対応は未確定。歴史的一致はD-024で確認不能 |
| 記録比較 | 151 | 40の8行数値を期待値として持つが、play_roomの2桁値にPython roundを適用。指定half-up/未丸め時刻の証明は不足。攻撃数は40由来とはしない |

旧5番依存の現行本文追跡：

- 090は旧brute配置を保持せず、`[("boss",12,4)]` とB/HP12をassertしている。置換先R2/B1。
- CueGapTestの実roomループは4番のみ。旧5番spitter固有の経路は現行assert集合にない。4番とpracticeの共有回帰を保持し、新5番はB2/B4・015/016/057へ置換。ただし歴史的な削除差分を検証したという意味ではない。
- 064は旧13集計を外し、14と3/4の15を保持。061のFPS比較は1〜4のみ。新5番は149だが公開情報条件未適合のため診断値。
- step94 W2の4番/practiceと新5番短射の表示置換を完全に追える専用assertは不足。後続Q6/Q4で確認する。
- 旧5番fixture維持を新しい必須条件にしない。旧集計の適用終了を共有基準の免除へ広げない。

歴史的確認不能はL1、L4保証部分、O3、step68 V-a/V-b過去時点・V-c・V-e未記録bot不変、step94 W3/W4過去全行動列・W7、および補足仕様の未記録範囲。現行内対照・記録比較と別管理する。

### 6. 証拠道具の選択・再現・確認

`emit_rows(target, columns, rows, start=1, stop=None, excluded=())` を後続試験からimportして使用する。選択は試験コード内の引数で固定する。環境変数やtrace枠の任意Python実行は前提としない。

例：

```python
from test_g002_evidence import emit_rows

# 当該試験が先に全rowsの条件・assertを評価した後で呼ぶ。
emit_rows(
    "B3/30/current/fixture",
    ["fps", "frame", "before", "after", "distance", "events"],
    evaluated_rows,
    start=1,
    stop=30,
    excluded=["60 FPS is a separate target"],
)
```

対象名には基準・FPS・証拠区分を入れ、rowsには68§2の実行条件・操作・測定本文を渡す。全集合評価は呼出側の責任で、この関数が成功判定や全判断監査を行うわけではない。source_idだけで本文を置き換えない。

出力はBEGINに列定義・source・総件数・表示件数・窓・前後未表示数・除外、各行に1始まりの元集合連番、ENDに対象・総件数・表示件数を持つ。再実行ではsource・入力・総件数を照合し、異なる結果を接合しない。BEGIN/ENDと予定連番を受信側で照合し、欠落を未確認にする。

058は3行中2番だけを捕捉し、total3/shown1、前後未表示各1、`002 [2]`、END、不正start拒否をassertした。Round 1で成功。ただし確認本文は内部捕捉され、外側にはその5行を再表示していない。

059は全ファイルと全IDを表示した。Round 1はINVENTORY_BEGINからENDまで連番001〜154が収録され、棚卸し部分の未表示はない。一方、その後のSPLIT_C_BOSSとSPLIT_C_PUBLIC付近には明示的に3665文字の切断がある。そこは未確認であり、今回のgreenや棚卸し完全性から補完しない。

道具は行数を限定するが、1行の文字数上限や自動的な1万2千字予算は持たない。後続は短い列と窓を選ぶ必要がある。既存SPLIT_C等の出力を全体として自動抑制する仕組みもない。必要な出力が固定suite内の既存印字と競合する場合は、具体的な変更対象をStudioが許可してから対応する。E0の許可外ファイルを変更していない。

今回の154件は旧152件と道具2件。追加の製品仕様試験を実装したという意味ではない。

### 7. QA配布台帳案

F番号は§2の実在パスへ展開する。全13件を少なくとも1単位へ割当済み、未割当ファイル0。追加試験は今後の各Stepで台帳へ追記する。範囲を跨ぐファイルは重複配布する。

| QA | 配布テストF番号 | 主対象 |
|---|---|---|
| Q1 | 04,07,08,09,12 | 公開情報bot、全判断、4条件、bot共有回帰 |
| Q2 | 01,02,03,06,07 | B1〜B10、弾S1〜S5 |
| Q3 | 03,07,09,10,11,12,13 | 境界、終端、retry、時刻、通常再生 |
| Q4 | 04,05,06,07,08,10 | 識別、注記、長時間、V1、文字列 |
| Q5 | 07,08 | 共有combat、cap/gap、variant、R2 |
| Q6 | 07,08,12 | step72/94、保持bot、記録比較 |

各QAの最大8件@needに頼らず、上記を最初から個別Loadする。製品・正本資料の核は68§9を併用する。Q5/Q6で正本照合後に未対応試験が判明した場合は、実装か直列継続を明記し、既存ファイル配布済みを基準充足と同一視しない。

E1用の個別Load候補は以下。いずれも実在確認済み：

- repo/game.py
- repo/session.py
- repo/play.py
- repo/run_driver.py
- repo/bots.py
- repo/source_id.py
- repo/tests/test_bots_boss.py
- repo/tests/test_split_c.py
- repo/tests/test_g002_evidence.py

これに仕様§6/8、68、60、D-019/D-024、本Handoffを加える。E1の必要本文に新たな不明ファイルはない。

### 8. 残作業・partialの理由

E0の全ID棚卸しと汎用窓出力の初版は保存した。基準対応は暫定であり、共有正本combat/step68/72/94とmanualの本文未供給部分、必要状態本文の出力、欠落検知の追加確認が残る。各基準向けの実測行を作るアダプタは未実装であり、汎用helperだけで後続証拠整備完了とはしない。

これらを既知の直列残作業としてpartialで渡す。Ownerへ供給条件の再質問は不要。StudioはE0棚卸しを採用してE1へ進め、正本の番号別完全対応は該当E4/Q5/Q6へ個別本文とともに引き継げる。E0の追加確認を先に行う場合も同Roleの継続で扱う。

E1以降では特に次を残す：

1. 公開情報境界の全分岐試験とbot修正。
2. boss突進をshot補助文から分離し、無傷接触を含む実距離・消費診断。
3. 新方針の3/2 hearts別FPS再測定、全判断列。
4. 未丸め時刻とhalf-upの記録比較、保持回帰の不足assert。
5. 通常公開入力再生成、全入場・正規敵撃破・player対照、旧未来入力破棄の十分な検証。
6. 長時間観測の開始・中間・終了本文と出力欠落検査。
7. 独立Q1〜Q6、歴史的確認不能の工程判断、Art Verify・Play・Designer判断・Review。

## Decisions already made

- D-019：旧集計を終了し、保持回帰・公開情報限定ボス比較・開始hearts別比較を維持。
- D-021：テキスト・スクリプトとStudio内独立検証で進める。
- D-022：旧経路注記、弾ライフサイクル、長時間観測契約を維持。
- D-023：個別Load、最大8件の一度の追加要求、最大3回の実行、出力最大2万字。存在しない全文保存先を要求しない。
- D-024：現行検証、現行内対照、記録比較、歴史的確認不能を分離。
- 68：E0→E1→E2→E3群→E4群→E5群→独立QAを直列に実施。

## Constraints

製品仕様、戦闘パラメータ、難度、秒数ゲート、Goal範囲を変更しない。今回の実装変更はF07のみ。

60のfailを上書きせず、今回の自己確認を独立QAとして扱わない。収録切断・未表示・本文未確認をpassにしない。旧bot数値と通常ラン時間は診断資料に留める。

歴史的確認不能を後続Reviewまで保持する。実機供給・変更前ビルド・全文保存機構を再要求しない。

## Open questions

- 正本combat/step68/72/94と個別assertの完全対応・未対応は、後続の個別Loadで確定する。
- 汎用helperを使った各対象の状態・判断列と出力予算は、E1以降で具体化する。
- 必要状態行が既存suite印字と競合する場合、どの既存試験出力を変更するかは具体的対象をStudioへ提示する。

E1開始を妨げる新しい仕様質問やOwnerへの質問はない。

## Expected output

Studioは実在13ファイル・154IDと配布台帳を確認してE1をルートする。必要ならE0の道具確認を同Roleへ直列継続する。

E1では公開観測専用データ・記憶・判断境界を実装し、全分岐の許可フィールド対応、内部値差に対する判断不変、履歴不足時の保守的処理、入場/retry初期化を試験する。今回E1へ着手済みとは扱わない。

後続QAへはEngineerの評価を合格根拠として渡さず、担当正本・ソース・テスト本文と再現条件を個別Loadする。新規試験が増えたらsource_idと全試験配布台帳を更新する。

## Build check

The runtime ran `run_tests` (`python3 -m unittest discover -s tests`) on the build exactly as this step wrote it: exit 0 (2.2 s).

```text
public-32", "driver_seconds": 141.0, "execution_stop": "driver limit", "outcome": "unfinished", "processing_seconds": 0.33191144798183814, "source_id": "c12166443a05"}, "trial_count": 1}
SPLIT_C_RETAINED {"results": {"30": {"1": {"attacks": 6, "cleared": true, "dashes": 3, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 6.63}, "2": {"attacks": 8, "cleared": true, "dashes": 10, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 20.73}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.63}, "4": {"attacks": 7, "cleared": true, "dashes": 7, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 18.33}}, "60": {"1": {"attacks": 6, "cleared": true, "dashes": 5, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 9.62}, "2": {"attacks": 8, "cleared": true, "dashes": 14, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 25.07}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.02}, "4": {"attacks": 7, "cleared": true, "dashes": 8, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 16.97}}}, "source": "c12166443a05", "trial_count_per_room_fps": 1}
..........................................................................................................................................................
----------------------------------------------------------------------
Ran 154 tests in 2.901s

OK
```

## Load

- Role: studio/roles/studio.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints
- Project: design/final-boss-and-continuous-run.md
- Project: design/g002-historical-comparison-evidence.md
- Project: repo/source_id.py
- Project: repo/tests/test_g002_evidence.py
- Project: repo/tests/test_boss.py
- Project: repo/tests/test_boss_contract.py
- Project: repo/tests/test_boss_contract_details.py
- Project: repo/tests/test_bots_boss.py
- Project: repo/tests/test_d022_observation.py
- Project: repo/tests/test_d022_shots_and_note.py
- Project: repo/tests/test_game.py
- Project: repo/tests/test_play_run_controls.py
- Project: repo/tests/test_run_driver.py
- Project: repo/tests/test_session.py
- Project: repo/tests/test_split_c.py
- Project: repo/tests/test_terminal.py
- Supporting report: goals/G-002-final-boss/60-qa-to-studio.md
- Supporting plan: goals/G-002-final-boss/68-technical-director-to-studio.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Decisions: decisions/D-023-owner-confirms-verification-supply.md
- Decisions: decisions/D-024-g002-historical-comparison-evidence.md
- Previous handoff: goals/G-002-final-boss/69-studio-to-gameplay-engineer.md
>>>END
