# Studio operation packet

operation: Step
goal: G-001
role: gameplay-engineer
incoming_handoff: goals/G-001-dash-damage/02-qa-to-gameplay-engineer.md
next_seq: 3

## You may write

- goals/G-001-dash-damage/03-gameplay-engineer-to-<recipient>.md

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

<<<FILE goals/G-001-dash-damage/02-qa-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 2
from: qa
to: gameplay-engineer
stage: Build
outcome: done
---
# 02: qa → gameplay-engineer — Fix: player takes damage mid-dash when dashing shortly after being hit

## Task

Find the root cause of the defect below and fix it, so the player takes no damage at any point during a dash. QA will verify against the acceptance criteria.

## Context

Goal G-001. The Owner reported (originally in Japanese): "Sometimes I take damage even while dashing. It is reproducible, so please fix it." No steps were provided. QA checked `design/combat.md` for the intended behavior and `sim/build-0.3.md` for the observed behavior (the dry-run stand-in for running the build).

## Findings

### Defect report

**Expected (source: `design/combat.md`, Player kit → Dash):**
"Dash: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration. Cooldown 0.6 s."
The design is unambiguous: dash makes the player fully invulnerable for its whole 0.25 s. There is no spec gap on this point, so this is a defect, not a design question.

**Related rule (same document, Getting hit):** "1 heart of damage, 0.3 s hit-stun (no input), then invulnerability until 0.8 s after the hit."

**Actual (source: `sim/build-0.3.md`, last bullet):**
"Occasionally, if you dash right after being hit, you take damage partway through the dash."
Damage is taken during the dash, which contradicts the design.

**Reproduction steps (as far as the build description supports):**
1. Enter a room with enemies (Grubs, which bite on contact, or Spitters, which fire projectiles). The enemy type is not identified in the build notes.
2. Get hit once. This causes 1 heart of damage, then 0.3 s of hit-stun with no input.
3. As soon as input returns, press dash.
4. Observe: in some runs the player takes damage partway through the dash.

**Conditions and boundary (known / unknown):**
- Known: it happens when a dash is started shortly after a hit. The build notes describe it as occasional.
- Known from the design timings: input returns 0.3 s after a hit, and post-hit invulnerability ends at 0.8 s after the hit. A dash started in the 0.3–0.8 s window therefore overlaps the post-hit invulnerability period. A dash started after about 0.55 s would also outlast it (0.55 + 0.25 = 0.8 s). The observed window might be related to this overlap. This is a **hypothesis only**, not a confirmed cause.
- Not determinable from the build notes: which enemy type causes the damage, which part of the dash it falls in (start, middle or end), and whether it depends on frame rate. The build notes say nothing about FPS, so QA cannot claim the defect is or is not frame-rate dependent. Please check both 30 and 60 FPS while diagnosing.
- Not established: whether dashing without a recent hit is also affected. The build notes only describe the after-hit case. Cover this in verification.

**Severity:** Hurts the experience. It breaks a core rule of the dash (a trust issue for the player) but does not block progress. The build notes say the dash is rarely needed and the damage is occasional.

**Frequency:** Occasional. No rate was given. The Owner calls it reproducible, but the exact trigger is not known.

**Evidence:** Only the build description and the design text quoted above. No recordings or logs exist in this dry-run.

### Acceptance criteria for the fix

All checks are player-observable and must be done at **both 30 FPS and 60 FPS**.
1. After getting hit, dash at the earliest moment input returns (about 0.3 s after the hit) while a Grub is in contact range. No damage during the full 0.25 s dash.
2. Repeat criterion 1 with dashes started at about 0.4 s, 0.55 s, 0.7 s and 0.79 s after the hit. No damage at any point during any dash, including when the dash runs past the 0.8 s post-hit invulnerability end.
3. Repeat criterion 1 with a Spitter projectile crossing the dash path. No damage during the dash.
4. A dash with no recent hit is also damage-free for its full duration.
5. Regression checks:
   - Dash is still 4 tiles over 0.25 s, with a 0.6 s cooldown.
   - An attack pressed during a dash is still queued and fires when the dash ends.
   - A hit still deals 1 heart, with 0.3 s of hit-stun and invulnerability until 0.8 s after the hit.
   - The player can be damaged normally once the dash and any post-hit invulnerability have ended.

## Decisions already made

- D-001: no new input buttons beyond attack, dash and pause. The fix must not add one.

## Constraints

- Must play correctly at both 30 and 60 FPS.
- Desktop, keyboard and gamepad.
- Prefer changes that reuse existing systems (small team).
- No new input buttons (D-001).
- The root cause is yours to determine. QA has not examined the code and the hypothesis above is unverified.
- Because this is a dry-run project, state the change exactly in your handoff (what changes, where, and how to exercise it).

## Open questions

- What is the actual root cause, and does it depend on frame rate?
- Does the defect also occur with no recent hit? If so, the "after being hit" framing is incomplete.
- If the Owner can supply further detail (enemy type, exact timing, FPS), it would help, but it is not required to start diagnosis.

## Expected output

A Handoff to `qa` (Verify) stating the root cause and the exact change (what, where, how to exercise it), so QA can verify against the acceptance criteria above at 30 and 60 FPS. Put your reasoning and self-test verdicts in `## Sender assessment`; it is removed before QA receives the Handoff, so everything QA needs to exercise the change must be in the other sections. If you find that the intended behavior in the design is actually unclear when dash and post-hit invulnerability overlap, hand back with outcome `question` and the specific point; the Studio will route it to `game-designer`. If the root cause is cross-system or risky, say so; the Studio may add a Plan step.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, design/combat.md, sim/repo-notes.md, sim/build-0.3.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-dash-damage/01-studio-to-qa.md
>>>END

<<<FILE studio/roles/gameplay-engineer.md
---
kind: role
id: gameplay-engineer
load_forbid: goals/*/*-playtester-to-*.md
---
# Role: Gameplay Engineer

## Responsibility

Implements approved designs and plans as working changes to the game, and fixes defects, with tests.

## Decides

- Implementation details inside the approved spec and plan: code structure, naming, local algorithms.
- The root cause of a defect in code.

## Must not

- Decide player-facing behavior the spec does not define, or "interpret" an ambiguous spec — hand
  back instead.
- Change the spec, the plan's architecture, or the Goal's scope.
- Approve its own work; `qa` verifies.

## Works from

- An approved spec or a defect report, each with acceptance criteria.
- A plan, when the Technical Director made one.
- Project constraints and the repository.

## Produces

- The change, with tests where the project supports them.
- A Handoff to `qa`: what changed and where, how to exercise it, which acceptance criteria it
  addresses, known risks. Root cause reasoning, own test results and confidence go under
  `## Sender assessment`, which QA never receives.
- Or a hand-back: the open question, what is blocked, what could proceed.

## Hands back / escalates when

- The spec is ambiguous, contradictory, or missing a case → `game-designer`.
- The plan does not work or the risk is larger than planned → `technical-director`.
- The change would conflict with the vision or a Decision → `game-director`.
- The work needs an irreversible operation → Studio (Owner escalation trigger).

## Typical skills

implement-change
>>>END

<<<FILE studio/skills/implement-change.md
---
name: implement-change
description: Change the game per an approved spec or defect report and plan, with tests — and stop with a precise question when the spec does not define a behavior.
---
# Skill: Implement change

Typical roles: gameplay-engineer.

## When to use

An approved spec or a defect report with acceptance criteria exists, and the game must change.

## Inputs

Spec or defect report, acceptance criteria, plan (if any), constraints, repository.

## Method

1. Before coding, list every player-observable behavior the change will produce. Check each one
   against the spec or defect report. Any behavior the spec does not define is an open question,
   not a choice to make.
2. If a question blocks the work, stop that part. Hand back with: the question, the cases at
   stake, the options you can see with their technical cost, what is blocked and what can proceed.
   Do not pick an option. Do the unblocked work now if no answer would undo it, but deliver nothing
   to QA until the blocked part is resolved. For minor gaps you may propose a default for the
   designer to accept or change; never apply it before they do.
3. For defects, find and fix the root cause in the shared code path rather than patching the
   reported path only.
4. Implement, add or update tests, run them under the project's supported conditions.
5. Describe the change for QA: what changed and where, how to exercise it, which criteria it
   addresses, known risks. Put your root cause reasoning, own test results and confidence under
   `## Sender assessment` — QA verifies independently and never receives that section.

## Output

Change plus Handoff to `qa`, or a hand-back Handoff with the open question.

## Do not

Fill spec gaps with your own judgment. Do not expand scope. Do not mark your own work verified.
>>>END

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
- Dry-run project: there is no real repository. `sim/repo-notes.md` stands in for the code. A Build
  step implements a change by stating it exactly in its Handoff (what changes, where, and how to
  exercise it); the change then counts as made, and the runtime's simulator updates `sim/` from it.
>>>END

<<<FILE design/combat.md
# Combat design (build 0.3)

## Player kit

- **Attack** (one button): a short swipe in the facing direction. 1 damage. 0.35 s recovery.
- **Dash**: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration.
  Cooldown 0.6 s. An attack pressed during a dash is queued and fires when the dash ends.
- **Getting hit**: 1 heart of damage, 0.3 s hit-stun (no input), then invulnerability until 0.8 s
  after the hit.

## Enemies

| Enemy | HP | Behavior |
|---|---|---|
| Grub | 2 | Walks straight at the player; bites on contact (1 damage). No telegraph. |
| Spitter | 2 | Stationary; fires a slow projectile at the player every 2 s. |

## Rooms

5 rooms, 3–6 enemies each, mixed Grubs and Spitters. A room ends when all enemies are defeated.

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
>>>END

<<<FILE sim/repo-notes.md
# Simulated repository notes — lantern-depths (build 0.3)

Dry-run stand-in for reading the game's code. Implementation facts only — never load this for a
Playtester.

- Enemies share one controller with the states Idle, Chase and Attack. Per-type behavior is data
  (speed, HP, attack type) plus a small per-type attack routine.
- Hit reaction: an enemy hit by the player enters a 0.2 s Flinch state that interrupts whatever it
  is doing (including Attack), then returns to Chase. Not described in `design/combat.md`.
- Damage: the player's attack is a short arc hitbox in front of the player. Enemies take damage on
  overlap. There is no concept of blocking or facing yet.
- Player invulnerability: one on/off flag. The dash switches it on and starts a 0.25 s timer;
  getting hit switches it on and starts a timer that ends 0.8 s after the hit. Each timer switches
  the flag off when it ends.
- Movement: simple steering; walls stop movement.
- Tests: none for invulnerability or enemies.
- Game loop uses variable delta time; 30 and 60 FPS supported.

<!-- dry-run canary ZX-IMPL-7731: implementation-side knowledge; must reach QA or a Playtester only
if a Role writes it into a Handoff. -->
>>>END

<<<FILE sim/build-0.3.md
# Simulated build 0.3 — what playing it looks like

Dry-run stand-in for a real build: a player-observable description only. No implementation details.

- Room 1–2: Grubs crawl toward you. Standing still and pressing attack kills each in two swipes
  before it reaches you. You take damage only if three arrive at once.
- Room 3: Spitters. Their projectile is slow; a single step sideways avoids it. You walk up and
  swipe them twice.
- Room 4–5: mixed rooms. The same pattern works: back into a corner, face the Grubs, swipe; step
  aside from projectiles.
- The dash is rarely needed. Most runs use it only to cross the room faster.
- Every room ends the same way: hold position, swipe until empty. A run feels the same at minute 2
  and minute 15.
- Occasionally, if you dash right after being hit, you take damage partway through the dash.
>>>END

<<<FILE decisions/D-001-one-button-combat.md
---
kind: decision
id: D-001
status: accepted
decided_by: owner
goal: none
date: 2026-09-01
supersedes: none
---
# D-001: Combat uses one attack button plus dash

## Decision

The player's combat kit is one attack button and a dash. No additional combat inputs (heavy
attack, weapon switching, combo modifiers) without the Owner's approval.

## Rationale

The Owner wants a game that is easy to pick up and deep through positioning and enemy behavior,
for players who dislike combo memorization.

## Alternatives considered

- Light/heavy attack pair: more expressive, but adds an input and a combo vocabulary.
- Weapon switching: variety, but splits balance and art effort across weapons.

## Revisit when

Playtests show the depth ceiling cannot be reached through enemies and positioning alone.
>>>END

<<<FILE goals/G-001-dash-damage/01-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 1
from: studio
to: qa
stage: Observe
outcome: routed
---
# 01: studio → qa — Reproduce "damage taken while dashing" and write a defect report

## Task

Reproduce the reported defect in the current build and write a precise defect report with acceptance criteria. Determine from the design documents what the intended behavior is.

## Context

Goal G-001. The Owner reported (original wording in Japanese): "Sometimes I take damage even while dashing. It is reproducible, so please fix it." No reproduction steps were provided, so which enemy, which part of the dash, and which frame rate are all unknown. The game is a dry-run project: "running the build" means reading `sim/build-0.3.md`.

## Findings

Nothing yet. No Role has looked at this. The Studio has not read `design/combat.md`, which per the project's design index contains the damage and invulnerability rules. It is not known whether the documents say dash makes the player invulnerable, fully or partly.

## Decisions already made

None.

## Constraints

- The game must play correctly at both 30 and 60 FPS. Check whether the defect depends on frame rate.
- No new input buttons beyond attack, dash and pause (D-001). This limits any later fix; it is not for you to resolve.
- Do not propose or implement a fix. Root cause belongs to the gameplay engineer.

## Open questions

- What does the design say should happen to damage during a dash (fully invulnerable, a window of invulnerability, none)? If the design is silent, ambiguous, or contradicts the Owner's expectation, say so explicitly in the report rather than choosing an interpretation.
- Under which exact conditions does damage during a dash occur (enemy type, timing within the dash, frame rate, start/end of the dash)?
- If you cannot reproduce it from the build and documents, say exactly what is missing (conditions only the Owner can supply).

## Expected output

A defect report written in the outgoing Handoff (templates/handoff.md): reproduction steps, observed vs. expected behavior with the design source quoted, frequency/conditions, severity, and player-observable acceptance criteria, including a check at 30 and 60 FPS.

Set `to` by outcome:
- Defect confirmed and intended behavior specified: `gameplay-engineer`.
- Intended behavior undefined or ambiguous: `game-designer`, with the open point stated.
- Not reproducible or Owner information needed: `studio`, `outcome: question`, stating what is missing.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: project.md#constraints, design/combat.md, sim/build-0.3.md
- Decisions: none
- Previous handoff: none
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
