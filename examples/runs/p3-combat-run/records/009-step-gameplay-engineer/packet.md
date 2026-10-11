# Studio operation packet

operation: Step
goal: G-001
role: gameplay-engineer
incoming_handoff: goals/G-001-combat-monotony/06-studio-to-gameplay-engineer.md
next_seq: 8

## You may write

- goals/G-001-combat-monotony/08-gameplay-engineer-to-<recipient>.md

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

<<<FILE goals/G-001-combat-monotony/06-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 6
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 06: studio → gameplay-engineer — Fix damage taken during a dash after being hit (build 0.3)

## Task

Fix the defect so the player takes no damage at any point of a dash, including a dash begun right after being hit. State the change exactly (what changes, where, how to exercise it), as the dry-run project requires. Find and report the trigger (frame rate, timing, damage source).

## Context

Goal G-001 (combat monotony). The Playtester saw the player take damage partway through a dash shortly after being hit. QA reproduced it against `design/combat.md` and confirmed a defect: the design says the dash is invulnerable for its full duration, and hit invulnerability lasts until 0.8 s after the hit. Together they should cover any dash begun after hit-stun. The expected behavior is already specified, so no Design or Plan stage is needed. This step runs in parallel with the Game Director's direction decision (step 3a) because it restores specified behavior and does not depend on that decision.

## Findings

The full defect report is in `05-qa-to-studio.md`. Summary:

- **Expected** (`design/combat.md`): the dash (4 tiles over 0.25 s, cooldown 0.6 s) is invulnerable for its full duration. A hit costs 1 heart, causes 0.3 s of hit-stun with no input, then invulnerability until 0.8 s after the hit.
- **Actual** (`sim/build-0.3.md`): occasionally, a dash right after a hit lets the player take damage partway through the dash.
- **Unknown**: frame rate (30, 60 or both), exact hit-to-dash timing, damage source (Grub contact or Spitter projectile), dash direction, and which half of the dash the damage lands in.
- **Severity**: hurts the experience and undermines trust in the dash. It blocks no progress. Frequency is rare.
- **Unverified hypothesis from QA**: the hit-invulnerability and dash-invulnerability timers interact badly, for example one's expiry or reset clears the other's flag. Confirm or discard this; the root cause is yours to decide.

Acceptance criteria (each must pass at both 30 FPS and 60 FPS):

1. After a hit, a dash at the earliest accepted input (0.3 s after the hit) takes no damage at any point of the 0.25 s dash, even with a Grub in contact or a Spitter projectile arriving mid-dash. Repeat at least 20 times per frame rate.
2. Repeat criterion 1 with dash presses at several delays after the hit, including during hit-stun and just before, at and just after the 0.8 s mark. No damage during an active dash.
3. Repeat criterion 1 with different dash directions (towards and away from the damage source) and in rooms 1–5 with both Grubs and Spitters.
4. A dash with no preceding hit still gives full invulnerability for 0.25 s (no regression).
5. Existing rules still hold: hit-stun 0.3 s with no input, hit invulnerability until 0.8 s after the hit, dash cooldown 0.6 s, and an attack pressed during a dash fires when the dash ends.
6. Damage previously taken mid-dash is not merely delayed to land right after the dash ends while an invulnerability window is still active. A hit landing after all windows have expired is normal.

## Decisions already made

- D-001: Combat uses one attack button plus dash. This fix needs no new input.

## Constraints

- Must play correctly at 30 and 60 FPS. Do not make the fix depend on frame rate.
- Prefer reusing existing systems (small team).
- Do not change the specified values in `design/combat.md`. If the spec turns out to be ambiguous or contradictory, hand back with `question` and do not decide it yourself. The handling of a dash pressed during hit-stun (ignored or buffered) is unspecified. That is a non-blocking clarification for `game-designer`, so do not decide it here.

## Open questions

- Which frame rate(s) and hit-to-dash timings trigger the damage? Find this first and report it.

## Expected output

The change, stated exactly (what, where, how to exercise it), with the trigger you found and your root cause. Write it as an outgoing Handoff **addressed to `studio`**, because the Studio composes the QA verification Handoff from it. Do not self-certify the fix as verified; QA verifies it independently against the criteria above.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat.md; sim/build-0.3.md; sim/repo-notes.md; project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/05-qa-to-studio.md
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

<<<FILE goals/G-001-combat-monotony/05-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 5
from: qa
to: studio
stage: Observe
outcome: done
---
# 05: qa → studio: Dash-damage check in build 0.3 (defect confirmed against design; route to gameplay-engineer)

## Task

Route the defect report below to `gameplay-engineer`. The expected behavior is already specified by `design/combat.md`, so no design decision is needed. The defect is not fully characterised: the trigger and frame-rate dependence are unknown (see Conditions and boundary).

## Context

Goal G-001 (combat monotony). The Playtester reported taking damage partway through a dash shortly after being hit (handoff 02). Handoff 03 asked QA to reproduce it and compare it with the dash and invulnerability rules. This report covers only that behavior. The "dash feels pointless" question is a design matter and is not judged here.

## Findings

### Verdict

**Defect.** The build contradicts a written rule in `design/combat.md`. It is not intended behavior, and it is not a design gap.

### Source of "expected"

`design/combat.md`, Player kit:

- **Dash:** 4 tiles over 0.25 s, "The player is invulnerable for the full dash duration." Cooldown 0.6 s.
- **Getting hit:** 1 heart of damage, 0.3 s hit-stun (no input), "then invulnerability until 0.8 s after the hit."

### Why the design rules out the observed damage

Taking the rules at face value, a dash after a hit is covered by invulnerability for its whole length:

- During hit-stun (0–0.3 s after the hit) the player cannot input, so the earliest a dash can begin is 0.3 s after the hit.
- A dash begun at 0.3 s runs to 0.55 s. Hit invulnerability lasts to 0.8 s, so the whole dash is covered by hit invulnerability.
- The dash's own invulnerability also covers the whole dash.
- So there should be no damage at any moment of a dash begun after a hit. Both windows cover it, and either one alone would be enough.

The design does not say how a dash pressed during hit-stun is handled (ignored or buffered). This does not change the verdict, because the expected outcome holds in every case: no damage from the start of the dash to its end. It could be clarified separately, and it is not required to fix this defect.

### Actual (from `sim/build-0.3.md`)

The build description states: "Occasionally, if you dash right after being hit, you take damage partway through the dash." This matches the Playtester's report and contradicts the expected behavior above.

### Reproduction steps (as far as the build description allows)

1. Play build 0.3 in any of rooms 1–5.
2. Take a hit (1 heart of damage).
3. Dash right after the hit.
4. Result: occasionally, the player takes damage partway through the dash.

### Conditions and boundary (not established)

`sim/build-0.3.md` is a player-observable description only. It gives no frame-rate, timing, enemy-type, direction or room information, so I could not vary conditions one at a time as the skill requires. Unknown:

- **Frame rate:** whether it happens at 30 FPS, 60 FPS or both. The project must play correctly at both, so the engineer must test both.
- **Time between the hit and the dash:** exact values; the boundary where it stops.
- **Damage source:** which enemy (Grub contact or Spitter projectile) causes the second hit.
- **Dash direction and position:** not described.
- **Whether the damage lands in the first or second half of the dash:** only "partway" is stated.

Frequency is "occasional/rare" in both the Playtester report and the build description. I could not measure it.

### Severity and frequency

- **Severity:** hurts the experience. The player loses a heart while using a move the design says is safe, and it undermines trust in the dash. It blocks no progress, and no crashes or stuck states were seen.
- **Frequency:** rare (occasional).
- **Impact on G-001:** this makes the dash look unreliable, but it does not explain the monotony and should not be treated as its cause.

### Hypothesis (unverified, not a code-level fact)

Hit invulnerability (0.8 s) and dash invulnerability (0.25 s) may interact badly. For example, one timer's expiry or reset may clear the other's flag. Another possibility is that the dash begins during or just after the hit-stun and a timer is restarted or cancelled. This is a guess for the engineer to confirm or discard.

### Acceptance criteria for the fix

Each check is player-observable and must pass at both **30 FPS and 60 FPS**:

1. After taking a hit, the player dashes at the earliest moment input is accepted (right after hit-stun, 0.3 s after the hit). The player takes no damage at any point of the 0.25 s dash, even with a Grub in contact or a Spitter projectile arriving mid-dash. Repeat at least 20 times per frame rate with no damage.
2. Repeat criterion 1 with dash presses at several delays after the hit, including during hit-stun (pressed early) and just before, at and just after the 0.8 s mark. At no point during an active dash does the player take damage.
3. Repeat criterion 1 with the dash in different directions (including towards and away from the damage source) and in rooms 1–5 with both Grubs and Spitters.
4. A dash that has no preceding hit still gives full invulnerability for 0.25 s (no regression).
5. The existing rules still hold: hit-stun lasts 0.3 s with no input, hit invulnerability lasts until 0.8 s after the hit, the dash cooldown is 0.6 s, and an attack pressed during a dash fires when the dash ends.
6. The damage that was previously taken mid-dash does not appear to be delayed and land right after the dash ends. If a hit lands after the invulnerability windows expire, that is normal behavior.

### Evidence

- The player report and `sim/build-0.3.md` agree on the behavior. No logs or recordings exist in this dry run.
- Frame rate, exact timing and trigger: not recorded, because the build description does not contain them.

## Decisions already made

- D-001: Combat uses one attack button plus dash. The fix needs no new input and does not touch D-001.

## Constraints

- The fix must play correctly at 30 and 60 FPS.
- Prefer reusing existing systems (small team).
- QA does not fix the defect. QA will verify the change against the criteria above after the build.

## Open questions

- Which frame rate(s) and which hit-to-dash timings trigger the damage? The engineer should find this first, because the build description cannot show it.
- Optional, for `game-designer`, not blocking: how should a dash pressed during hit-stun be handled (ignored or buffered)?

## Expected output

Route to `gameplay-engineer`: fix the behavior so the dash is invulnerable for its full duration, including right after a hit. Report the trigger found (frame rate, timing, damage source). Then route to `qa` for verification against the acceptance criteria above. Do not route to `game-designer` for this defect. The buffering question above is a separate, non-blocking clarification.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: none
- Project: design/combat.md; sim/build-0.3.md; project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/03-studio-to-qa.md
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
