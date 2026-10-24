# Studio operation packet

operation: Route
goal: G-002
step_artifacts: goals/G-002-final-boss/58-qa-to-studio.md
next_seq: 59
context_request: allowed once (@need, up to 8 paths)
current_build: repo/ (sha d86d55d41027; run through the project's run commands)
log: last 5 of 31 entries in @log-recent; the full history is goals/G-002-final-boss/log.md

## You may write

- goals/G-002-final-boss/goal.md
- goals/G-002-final-boss/58-qa-to-studio.md (in place: keep kind, goal, seq, from, to and any Sender assessment)
- project.md: only in the Route that closes the Goal, and only its ## Current state (at most 1,500 characters)
- goals/G-002-final-boss/NN-studio-to-<role or owner>.md: up to 3 new artifacts, consecutive NN starting at 59
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
- Verify：open（57で独立QA）。30/60 FPS、連続到達・勝敗・再挑戦、共有戦闘回帰を検証する。その後の限定Art Verifyはテキストplayer viewの二攻撃、予兆と実弾、回復、HP、終端・retryの識別を扱う。実機検証は要求しない。
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
| 7 | Verify | qa | verify-change | open | 57-studio-to-qa.md |
| 8 | Verify | art-director | visual-review | planned | — |
| 9 | Play | playtester | playtest-session | planned | — |
| 9a | Design | game-designer | make-decision, write-design-spec | planned | — |
| 10 | Review | game-director | review-outcome | planned | — |
| 11 | Next | studio | — | planned | — |

逐次実行する。Build後は独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewとする。明白な対処不能・到達不能が判明した場合はDesigner判断を前倒しする。並列Stepは開かない。

## Route changes

56はdone。runtimeの保存ソース04fa2b1c168aで全suite152件OKのため、57で独立QAを開く。Engineerの自己評価を含む56はQAへ渡さず、仕様・受入基準・実行経路を新しいHandoffにまとめる。以後の逐次順序は維持する。

## Next action

QAが57-studio-to-qa.mdから、新しいexecutor contextで保存ビルドを独立検証する。30/60 FPS別の仕様適合・公開経路・回帰結果をStudioへ返す。合格後は限定Art Verifyへ進む。

## Outcome

未完了。56でSplit Cを納品し、runtimeの保存ソース04fa2b1c168aで全suite152件が成功した。通常ランの同一試行計測と独立部屋の回帰資料を保存し、57で独立QAを開始する。報告された通常ラン約1.5〜1.7分とVisionとの差、ボスのFPS間所要時間差は独立結果とともにDesignerへ渡す。独立QA・限定Art Verify・独立Play・Designer判断・Reviewは未完了。D-021の承認内で継続し、Goalはactive、project.mdは変更しない。
>>>END

<<<FILE @log-recent
## 060-route · 2026-10-20

Status: active. Open: 49-studio-to-gameplay-engineer.md.

48でDesignerがV1補完3点を確定（D-022、追加Ownerエスカレーション不要）。49でEngineerがV1実装、46の未実行pause/retry試験を含む全suite実行とsource id記録を一括で行う（6k-b）。その後Split C（6l）。完成資料が未了のため独立QAへはまだ送らない。

## 063-route · 2026-10-21

Status: active. Open: 51-studio-to-gameplay-engineer.md.

50はpartialで変更・実行なし。欠落していたplay.py・session.py・source_id.pyを51のLoadに明記し、同じEngineerへV1実装と全suite実行を継続する。仕様再検討やOwner判断は不要。完了後Split C、続いて独立QAの順序を維持する。

## 065-route · 2026-10-21

Status: active. Open: 53-studio-to-gameplay-engineer.md.

52はpartialで弾ライフサイクルと旧経路注記を納品し、runtime試験は140件OK。53で同じEngineerへ観測間隔・全attempt summary・残る受入試験と最終検証を継続する。連続partialは2回。完成後Split C、独立QAの順序を維持し、次も同じ作業がpartialならTechnical Directorへ再計画を戻す。

## 067-route · 2026-10-21

Status: active. Open: 55-studio-to-gameplay-engineer.md.

54はdone。保存ソース120ca2671495の全suite149件OKと両FPSの長時間観測を確認し、55でSplit Cを開く。pause/retry込み通常ラン計測とdodger独立1〜4の回帰固定を完成後、独立QAへ進む。連続partialの再計画条件は発火しない。

## 070-route · 2026-10-21

Status: active. Open: 57-studio-to-qa.md.

56はdone。runtimeの保存ソース04fa2b1c168aで全suite152件OKのため、57で独立QAを開く。Engineerの自己評価を含む56はQAへ渡さず、仕様・受入基準・実行経路を新しいHandoffにまとめる。以後の逐次順序は維持する。
>>>END

<<<FILE goals/G-002-final-boss/58-qa-to-studio.md
---
kind: handoff
goal: G-002
seq: 58
from: qa
to: studio
stage: Verify
outcome: fail
---
# 58: qa → studio — 実行証拠の独立確認と検証不足の差し戻し

## Task

不足している独立検証を追加でルートする。現時点では全受入基準の合格を確認できないため、限定Art Verify以降への合格ルートには進めない。

## Context

57の依頼に従い、仕様・Decisionと、packetに収録された実行結果を照合した。対象はテキスト・スクリプト方式であり、実機供給は要求しない。

実行枠は残り0回。今回の判定は収録結果の独立評価であり、追加実行、保存ソースやテスト本文の閲覧、コード変更は行っていない。実装者の自己評価・履歴は根拠にしていない。

## Findings

### 判定

**fail：必要な独立検証が未完了。再現済みの製品不具合を断定するものではない。**

152 testsの成功は確認したが、各テストの条件・assert・基準対応はpacketにない。suiteのgreenだけではB1〜B10、境界、共有回帰、表示契約全体を合格にできない。以下では観測できた事実と未確認を分離する。

### 保存ビルド・実行条件

全収録出力の識別は以下で一致する。

- build：`0.6-g002-public-32`
- source_id：`04fa2b1c168a`

これは出力上の識別一致であり、保存ファイルからの独立再算出は未実施。D-021により旧指定shaとの照合は不要。

実行済みコマンド：

| 実行 | 入力・条件 | 件数 |
|---|---|---:|
| `python3 -m unittest discover -s tests` | 152 tests、Exit 0、2.855秒 | suite 1回 |
| `python3 play.py --view trace SCRIPT` | Round 2 boss-30、room 5、30 FPS、limit 12、driver-limit 14、2.2 pause／4.2 resume | 1試行 |
| `python3 play.py --view player SCRIPT` | Round 2 boss-60、上記の60 FPS版 | 1試行 |
| `python3 play.py --view player SCRIPT` | Round 3 retry-30、mode run、limit 20、driver-limit 14、control 6 retry | 2 attempts |
| `python3 play.py --view trace SCRIPT` | Round 3 retry-60、上記の60 FPS版 | 2 attempts |

suiteには公開入力再生、独立部屋dodger、ボスdodgerの構造化結果も含まれる。ただし公開連続スクリプトを両FPS・両viewで個別実行した完全出力、`bots.py`の独立実行結果は収録されていない。

### 通常連続ラン：同一試行の測定

`SPLIT_C_PUBLIC`は各FPSにつき公開入力再生1セッション、3 attempts。`state_injection: false`と記録されている。生成済み入力の再生であり、人間のプレイやcontrolled fixtureの連続到達とは扱わない。

| 項目 | 30 FPS attempt 1 | 60 FPS attempt 1 |
|---|---:|---:|
| 結果 | clear | clear |
| ラン時刻 | 86.966667秒 | 103.533333秒 |
| 部屋1 | 6.633333秒 | 9.616667秒 |
| 部屋2 | 20.733333秒 | 25.066667秒 |
| 部屋3 | 15.633333秒 | 15.016667秒 |
| 部屋4 | 18.333333秒 | 16.966667秒 |
| 部屋5 | 21.633333秒 | 32.866667秒 |
| 遷移4回 | 各1.0秒 | 各1.0秒 |
| ボス初入場hearts | 3 | 3 |
| 攻撃／ボス命中／dash | 41／12／34 | 41／12／45 |
| hurt | 0 | 0 |
| pause | 1回、2秒 | 1回、2秒 |
| attemptのdriver経過 | 120秒 | 120秒 |
| pauseを除くdriver経過 | 118秒 | 118秒 |
| 終端待機 | 31.033333秒 | 14.466667秒 |

部屋時間合計＋遷移4秒はラン時刻と一致する。driver経過はラン時刻＋pause＋終端待機と一致する。これは同一attempt内の照合であり、独立部屋時間の合算ではない。

両FPSともattempt 2は第1部屋で自然死亡。30 FPSは5.1秒、60 FPSは5.033333秒、hurtは各3、攻撃・dashは0。driver経過は各20秒で、終端待機は14.9／14.966667秒。

attempt 3は各1秒、攻撃1、hurt・dash各0、unfinished。セッションはdriver 141秒で停止し、retryは勝利後と死亡後の計2回。最終outcome unfinishedと、過去attemptのclear／deathが区別されている。

summaryとの数値一致はこの構造化証拠の範囲で確認できる。processing_secondsは30 FPSが0.127572、60 FPSが0.328531。headless処理時間であり、人間の所要時間ではない。

### 基準別の確認状況

「部分確認」は基準全体のpassを意味しない。

| 基準 | 30／60 FPSの判定と根拠 |
|---|---|
| R1 | 部分確認。構造化記録は通常連続到達・勝利を支持する。ただし正規敵の全撃破・入場列と両viewの対照が未収録で、B単体を含む全条件の独立確認は未完了。 |
| R2 | 未確認。部屋データ、配置、パラメータを閲覧していない。 |
| R3 | 未確認。通常再生は無傷であり、hearts 1/2/3/0の境界試験の代用にならない。 |
| R4 | 未確認。境界前後の残存状態と反応記憶の全比較がない。 |
| R5 | 部分確認。遷移時間は両FPSとも各1秒。表示中・入場同時刻入力の処理列は不足。 |
| B1 | 部分確認。30 FPS traceの初期Bは(12,4)、HP12、単体。60 FPS playerもHP12・charge開始。各攻撃3回、低HPでの順序維持は未確認。 |
| B2 | 部分確認。30 FPSはcharge 2.033333→2.733333、short shot予兆開始4.266667。60 FPSはcharge 2.016667→2.716667、short shot 4.233333→5.033333。移動後の照準不変・距離0は未確認。 |
| B3 | 部分確認。30 FPSの突進は2.733333→3.033333の0.3秒、x=10.0→7.6の2.4 tilesで、接触後も移動継続。壁試験と60 FPSの位置比較は不足。 |
| B4 | 部分確認。60 FPSは発射5.033333、命中5.05、回復6.033333で、早期消費でも1秒を維持。速度・寿命・未接触・吸収の全条件は未確認。 |
| B5 | 未確認。指定した直交1 tile移動の操作列と両攻撃の無傷証拠がない。 |
| B6 | 未確認。dash回数だけでは実接触・消費・終了後無傷を証明できない。 |
| B7 | 未確認。保護終了を攻撃途中に置く状態・接触証拠がない。 |
| B8 | 未確認。全フェーズの非致死swipe前後と致死時の新発動禁止の証拠がない。 |
| B9 | 部分確認。収録観測の回復はcharge 1.2秒、short shot 1.4秒。開始時から4回の攻撃成立は未確認。 |
| B10 | 未確認。横ずれ・接触距離の帯内外・上端試験がない。 |
| T1 | 未確認。残弾を持つ終端と、その後2秒の状態比較がない。 |
| T2 | 未確認。同フレームの致死swipeと既発射弾による致死接触の証拠がない。 |
| T3 | 部分確認。通常再生には終端待機があり時刻集計は整合。戦闘入力を与えた全状態不変の比較は不足。 |
| T4 | 部分確認。勝利・自然死亡からのretry記録と、初期盤面への復帰がある。完全初期状態比較と旧未来入力破棄の決定的証拠は不足。 |
| C1 | 部分確認。部屋時間＋4遷移がラン時刻と整合。全入場時刻0の列は未収録。 |
| C2 | 部分確認。30 FPS traceでpause／resumeイベントはともにrun 2.2、frame 66。60 FPS playerでも両イベントのrun時刻2.2。2秒pauseを記録。dash・保護・clear表示の全状態比較は不足。 |
| C3 | 部分確認。driver-limitとattempt結果は区別される。game-time limitと勝敗同フレームの優先は未確認。 |
| V1 | 部分確認。60 FPS playerでHP、phase、next、両時刻、予兆方向・危険範囲、発動時の線除去、回復、重なった実弾のactive shots 1を確認。通常ラン勝利・retryを含む両FPS全表示の対照は不足。 |
| V2 | 今回の検証対象外。D-021に従う。実機対応済みとは判定しない。 |

Round 2の診断部屋死亡表示は`you went down`である。通常ラン用retry表示の不具合とは断定しない。診断経路ではretryを拒否する契約があるためである。

Round 3の旧入力はrun時刻7秒にattack／dashを予約するが、新attemptは5.1／5.033333秒で自然死亡する。そのため、入力が現れないことは**旧入力破棄の証明にならない**。該当時刻を越えて生存させるか、破棄された入力列を直接観測する必要がある。

### D-019：bot結果と保持回帰

独立dodgerは各部屋・各FPSにつき1試行、開始3 hearts、limit 60秒。全てclear、終了3 hearts、損失0、被弾源なし。

| 部屋 | 30 FPS：秒／攻撃／dash | 60 FPS：秒／攻撃／dash |
|---|---|---|
| 1 | 6.63／6／3 | 9.62／6／5 |
| 2 | 20.73／8／10 | 25.07／8／14 |
| 3 | 15.63／8／6 | 15.02／8／6 |
| 4 | 18.33／7／7 | 16.97／7／8 |

この結果では16cの独立1〜4比較と15の独立3・4 dash使用を満たす。14のdodger側も満たす。ただしwalker側の独立1〜2損失が未収録なので14全体は未確認。

独立3・4のwalker／camperの結果、被弾源、判断ログが不足する。旧3〜5合計ゲートは適用していない。

ボス対応dodgerは各FPS・開始heartsごと1試行、limit 120秒：

| FPS | 開始→終了hearts | 結果／損失 | 秒 | 攻撃／dash |
|---|---|---|---:|---|
| 30 | 3→3 | clear／0 | 21.63 | 12／8 |
| 60 | 3→3 | clear／0 | 32.87 | 12／12 |
| 30 | 2→2 | clear／0 | 21.63 | 12／8 |
| 60 | 2→2 | clear／0 | 32.87 | 12／12 |

数値上は両hearts対とも同じclear結果・損失差0。ただしD-019の条件付き合格には、同一方針・同一初期状態・観測可能情報のみを使うことの確認が必要。

収録サンプルは「walk to boss」「dash up/down from charge/short shot」「hold off locked charge line」「face and swing」を示す。playerに見える状態に対応する行動は確認できるが、`hit in 0.39 s`等の算出元や全判断経路は未確認。サンプルだけで未表示の将来状態を使用しないと断定できない。判断件数は30 FPS各145、60 FPS各220だが、全文はない。

共有combat基準1〜11、17〜21、step68、step72、step94の保持部分は、suite成功のみでは個別passにしない。特にcap遅延の一般上限と、旧第5部屋からの置換範囲を追跡できる試験証拠が必要。

### D-022

| 基準 | 判定 |
|---|---|
| L1〜L3 | 未確認。旧経路各部屋の実出力・変更前比較がない。 |
| L4 | 文書整合を確認。manualは旧room 5 playerだけの注記と公開経路を明記する。 |
| S1〜S4 | 未確認。Round 2 trace中段は省略され、発射・消滅の全ライフサイクルを追跡できない。 |
| S5 | 60 FPSの収録player出力にshot IDは見られない。全条件・両FPSの確認は未完了。 |
| O1 | suiteの構造化出力では両FPSともplayer 121/121、trace 241/241。行数上限を満たす記録。 |
| O2・O3 | 未確認。間隔変更前後・既定出力の比較列がない。 |
| O4 | 部分確認。収録公開実行のsummaryは各1ブロックで、連続再生の数値も整合。全終了条件と状態の独立対照は不足。 |
| O5 | 未確認。範囲外入力の拒否出力がない。 |
| O6 | suiteは両FPS・両viewでrun 1200.0を記録。ただし長時間出力全体は未収録で、途中切断がないことの独立確認は未完了。 |

### 時間差と後続判断

通常再生の完走は約1.45分／1.73分で、15〜20分Visionより大幅に短い。これはスクリプト再生の1試行ずつの測定であり、人間の体験時間ではない。FPS間の完走差は16.566667秒、独立ボス差は11.24秒。秒数差の追加閾値は置かず、規則違反とも難度合格とも判定しない。

Designerへは入力判断・反撃位置・部屋別時間とともに渡し、独立Play後に追加ゲートや調整の要否を判断してもらう。HPや待機時間を増やす提案は本QAでは行わない。

## Decisions already made

- D-017：二攻撃、境界回復、終端優先、pause・retry・時計の契約。
- D-019：旧集計の適用終了。保持回帰、条件付きbot比較、実測後Designer判断。
- D-021：テキスト・スクリプト方式を承認。実機供給・旧指定sha照合は不要。
- D-022：旧経路注記、弾ライフサイクル、長時間観測の追加契約。

## Constraints

- 製品コード・仕様を変更しない。
- 未確認をpassにしない。suite成功と基準ごとの独立証拠を区別する。
- controlled fixture、生成入力再生、bot、人間の独立Playを区別する。
- 新しい難度・秒数ゲートをQAが設定しない。
- 今回の実行不足を実機供給要求へ戻さない。
- 本報告のReview用時間・期待結果をPlaytester資料へそのまま転記しない。

## Open questions

1. 全基準の追加独立検証に必要な実行枠と、保存ソース・テスト本文・完全ログを次のQA Stepへ供給できるか。
2. R3〜R5、B1〜B10、T1〜T4、C2〜C3、D-022の未確認条件について、両FPSの操作列・状態・イベントを追跡できるか。
3. 公開連続スクリプトを両FPS・両viewで再生し、正規撃破・全入場・終端・retryを状態と対照できるか。
4. 新attemptが旧入力時刻を越える条件で、旧未来入力破棄を確認できるか。
5. walker／camperを含む独立部屋成績と、ボスbotの全判断根拠を確認できるか。

仕様の意図が未定義であることを示す確定所見はなく、今回の主要な障害は証拠不足である。

## Expected output

Studioは未確認項目を独立QAへ再ルートし、両FPSの基準別pass/failと再現可能な証拠を揃える。既知の失敗を修正依頼する段階ではなく、まず検証不足を解消する。

合格後に、限定Art Verify、独立Play、Designerの実測後判断、Game Director Reviewへ進める。時間のVisionとの差とFPS別測定値はDesignerへ引き継ぎ、追加不要の場合も理由を記録する。

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#constraints
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: repo/（保存ソース、tests、manual.md、public-driver.md）
- Project: 今回の@run-resultsと、追加実行の完全ログ・入力列
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Previous handoff: goals/G-002-final-boss/57-studio-to-qa.md
>>>END
