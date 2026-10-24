# Studio operation packet

operation: Step
goal: G-001
role: gameplay-engineer
incoming_handoff: goals/G-001-damage-during-dash/02-qa-to-gameplay-engineer.md
next_seq: 3

## You may write

- goals/G-001-damage-during-dash/03-gameplay-engineer-to-<recipient>.md

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

<<<FILE goals/G-001-damage-during-dash/02-qa-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 2
from: qa
to: gameplay-engineer
stage: Build
outcome: done
---
# 02: qa → gameplay-engineer — Fix: player takes damage mid-dash after a recent hit (defect report)

## Task

Fix the defect below so the player takes no damage at any point during a dash, as `design/combat.md` specifies. Then hand to Verify with the acceptance criteria below unchanged.

## Context

Goal G-001. The Owner reported (verbatim): 「ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。」 ("I sometimes take damage even while dashing. It's reproducible.")

QA ran the dry-run build (`sim/build-0.3.md`) and compared it with `design/combat.md`. The expected behavior is specified, and the build contradicts it in one reproduced case, so this goes to Build, not Design.

## Findings

### Defect report

**Title:** Player takes damage partway through a dash that is started shortly after being hit.

**Source of "expected":** `design/combat.md`, Player kit, Dash: "The player is invulnerable for the full dash duration" (4 tiles over 0.25 s). It has no exception for dashing soon after a hit. The same document says that after a hit there is 0.3 s hit-stun (no input), then invulnerability until 0.8 s after the hit. That also covers a dash started right after the hit-stun ends.

**Actual (from `sim/build-0.3.md`):** "Occasionally, if you dash right after being hit, you take damage partway through the dash."

**Reproduction steps (as far as the build description supports):**
1. Enter a room with enemies (Grubs and/or Spitters) and let one hit you (1 heart).
2. As soon as input returns after the 0.3 s hit-stun, press dash.
3. Watch for a second heart of damage taken during the dash movement.

**Conditions and boundary:**
- Trigger: dash started soon after taking a hit. The build notes describe it only as "occasionally", so it is intermittent, not every attempt.
- Dash phase: "partway through", meaning the middle of the dash, not the start or end. No finer timing is available.
- Not triggered in the normal flow of dashing without a recent hit. The build notes say the dash is otherwise used to cross rooms.
- **Not established from the packet:**
  - Which enemy or attack deals the damage (Grub contact bite vs. Spitter projectile).
  - Exact timing and positions.
  - Whether it depends on frame rate. The build description has no 30 vs. 60 FPS information, so I could not vary frame rate. The report makes no claim about frame rate, and Verify must check both.
  - Whether the hit-stun, post-hit invulnerability and dash invulnerability windows interact in a way that matters. Engineers should treat this as a hypothesis only. It is not established fact.

**Reproducibility:** Sometimes (intermittent). Reproduced on the dry-run build description only. No logs or recordings exist.

**Severity:** Hurts the experience, not progress-blocking. The player loses a heart in a situation where the design guarantees safety. It is a rare path because the dash is rarely needed, but it breaks the dash's core promise and the Owner can reproduce it.

**Evidence:** `sim/build-0.3.md` last bullet; `design/combat.md` Dash rule. No other artifacts.

### Acceptance criteria (for Verify, at both 30 FPS and 60 FPS)

1. Take a hit, then dash as soon as input returns after hit-stun (about 0.3 s after the hit). Repeat at least 20 times per frame rate, against a Grub contact and against a Spitter projectile. The player takes no damage at any moment from dash start to dash end (0.25 s).
2. Repeat the above, starting the dash at several delays after the hit (immediately after hit-stun, and during the remainder of the 0.8 s post-hit invulnerability window). No damage during the dash in any case.
3. With no recent hit, dashing through a Grub or into a projectile still causes no damage during the dash (no regression).
4. Without dashing, a hit still deals 1 heart, applies 0.3 s hit-stun, and grants invulnerability until 0.8 s after the hit (no regression).
5. Dash distance and duration are unchanged (4 tiles over 0.25 s), cooldown is unchanged (0.6 s), and an attack pressed during a dash still fires when the dash ends.
6. Results are the same at 30 and 60 FPS.

## Decisions already made

None that touch this Goal. D-001 (one attack button plus dash) applies: do not add input buttons.

## Constraints

- Must play correctly at both 30 and 60 FPS.
- No new input buttons beyond attack, dash and pause (D-001).
- Prefer changes that reuse existing systems (small team).
- Do not change the design. Dash invulnerability is as specified.

## Open questions

1. Root cause is the gameplay engineer's call. Confirm which enemy attacks produce the mid-dash damage and whether frame rate matters. The packet had no data on either.
2. If the root cause turns out to be non-local (for example frame-rate-dependent timing, or an interaction across several systems) or the fix is non-obvious, hand back with outcome `question` so the Studio can route to Plan (`technical-director`). If the spec turns out to be ambiguous or missing a case, hand back for Design. Do not decide it yourself.

## Expected output

A fix to the build and a handoff for Verify (`qa`), stating what changed and how to exercise it, so that QA can check the acceptance criteria above at 30 and 60 FPS. Include the root cause you found. Put any implementer self-assessment under `## Sender assessment`, which is stripped before QA sees it.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, design/combat.md, sim/build-0.3.md, sim/repo-notes.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-damage-during-dash/01-studio-to-qa.md
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

<<<FILE goals/G-001-damage-during-dash/01-studio-to-qa.md
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

Reproduce the Owner's report that the player sometimes takes damage while dashing. Write a precise defect report with player-observable acceptance criteria, using the `reproduce-defect` skill.

## Context

The Owner's report, verbatim:

> ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。

(In English: "I sometimes take damage even while dashing. It's reproducible, so please fix it.")

This is Goal G-001. Nobody has reproduced the problem first-hand yet. The project is a dry-run: "running the build" means reading the simulated build file listed under Load. The planned route is Observe (this step) → Build → Verify. Design and Plan are tentative and depend on your report.

## Findings

None yet. This is the first step. Intake did not read the combat design, so it has not confirmed what the design says about dash and damage.

## Decisions already made

None that touch this Goal. D-001 (one attack button plus dash) only limits inputs: no new buttons are to be added.

## Constraints

- The game must play correctly at both 30 and 60 FPS. Check whether the defect depends on frame rate and say so in the report.
- No new input buttons beyond attack, dash and pause (D-001).
- Report observed behavior. Do not propose design changes. Root cause is the gameplay engineer's call.

## Open questions

1. Under what exact conditions does damage land during a dash? Cover which enemy or attack, which phase of the dash (start, middle, end), the positions or timing involved, and whether frame rate matters.
2. What does `design/combat.md` say the intended behavior is for damage during a dash?
   - If it clearly says the player takes no damage during the relevant dash phase, state that and cite it.
   - If it is silent or ambiguous for the reproduced case, or allows the damage, say so plainly. That outcome sends the work to Design (`game-designer`) instead of Build.

## Expected output

A defect report (per the `reproduce-defect` skill) containing:
- Reproduction steps and conditions.
- Observed vs. expected behavior, citing the design document.
- Reproducibility (always, sometimes, or frame-rate dependent) and your severity call.
- Player-observable acceptance criteria that Verify can later check, at both 30 and 60 FPS.

Write it in the Findings of your outgoing Handoff. Set `to` per the route:
- `gameplay-engineer` if the intended behavior is specified and the defect is reproduced.
- `game-designer` if the expected behavior is undefined or contradicts the Owner's expectation.
- `studio` with `outcome: question` if you cannot reproduce it, listing exactly what you tried and what information you need.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: project.md#constraints, design/combat.md, sim/build-0.3.md (the build to run)
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
