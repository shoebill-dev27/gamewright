# Studio operation packet

operation: Step
goal: G-001
role: gameplay-engineer
incoming_handoff: goals/G-001-combat-monotony/18-studio-to-gameplay-engineer.md
next_seq: 20

## You may write

- goals/G-001-combat-monotony/20-gameplay-engineer-to-<recipient>.md

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

<<<FILE goals/G-001-combat-monotony/18-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 18
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 18: studio → gameplay-engineer — Make the hit-stun input behavior observable and consistent with D-003 (verification blocker)

## Task

State exactly how the build handles a dash or attack pressed during hit-stun, so that it is ignored and not buffered (D-003). Make the change if the current behavior differs. Record the result in build notes in player-observable terms. Also report the code-side values listed below. Do not change anything else.

## Context

Goal G-001 (combat monotony). The dash/hit invulnerability fix (handoff 08) is being verified by `qa`. QA's second attempt (handoff 15) found that everything described in `sim/build-0.4.md` is consistent with the six criteria in `05-qa-to-studio.md`. QA could not give a verdict on one case: a dash (or attack) pressed during the 0.3 s hit-stun. `sim/build-0.4.md` says only "behaves as it did in 0.3", and `sim/build-0.3.md` does not describe it. D-003 (decided by the designer) requires such input to be ignored, not buffered. Nothing fires during hit-stun or when it ends.

This is the second `question` from step 4a, but for a different missing input. The first was a missing build file, and the second is a missing build behavior. If QA again hands back for the same missing hit-stun observation, the Studio escalates to the Owner.

## Findings

From QA (handoff 15):
- The hit-stun dash press is undescribed in both builds. Neither is observed to be "ignored" or "buffered".
- `sim/build-0.4.md` has the heading "Simulated build 0.3.1" while the file is named 0.4. The Studio needs to know whether they are the same build.
- Flicker and sound cues around the hit and dash are not mentioned in the build text, so QA could not check them.
- The build files are prose and give no repeat counts or measured boundary timings.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- D-003: input during hit-stun is ignored, not buffered. Hit invulnerability and dash invulnerability are independent timers.
- D-004: Phase 2 technical approach (timestamps on the accumulated game clock, not frame counts). Phase 1 is a separate Build that waits for this fix to pass verification.

## Constraints

- Scope is the hit-stun input handling only. This is not the start of Phase 1; the Phase 1 wave scheduler, marker and room tables are not part of this step.
- The fix must be correct at 30 and 60 FPS. Use timestamps, not frame counts.
- Dry-run project: state the change exactly (what changes, where, how to exercise it). The change then counts as made and the simulator updates `sim/`. If nothing needs to change, say so, and say what the build does, in observable terms.
- If the spec is ambiguous, hand back. Do not decide it yourself.
- No new input buttons.

## Open questions

Answer in your handoff:
1. What does the build do today when dash is pressed during hit-stun, and when attack is pressed? Does anything fire during hit-stun, at its end (buffer), or both?
2. Is `sim/build-0.4.md` (heading "0.3.1") the latest build?
3. Report these code-side values, as the Technical Director and Art Director need them (technical-director handoff 16, task 0, and art-director handoff 17): Grub speed, player speed, projectile speed and range, hearts, room size in tiles, Grub and player hitbox sizes, whether a spawn effect or spawner exists, and where the Flinch is implemented. A value that `sim/repo-notes.md` does not contain should be reported as "not in the code notes".
4. Are there flicker or sound cues for hit invulnerability or dash invulnerability? Describe them in observable terms, so QA can check them.

## Expected output

A handoff with the change (or "no change needed") and the answers above, in observable terms. **Address the result to `studio`**, so that the Studio can compose a clean verification Handoff for `qa` without implementation history. Put your own reasoning only in `## Sender assessment`; it is removed before QA receives the handoff.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat.md; project.md#constraints; sim/repo-notes.md; sim/build-0.4.md; sim/build-0.3.md; goals/G-001-combat-monotony/05-qa-to-studio.md (acceptance criteria)
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-003-input-during-hit-stun.md; decisions/D-004-phase-2-technical-approach.md
- Previous handoff: goals/G-001-combat-monotony/15-qa-to-studio.md
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

### Clarifications (G-001 spec, see `design/g001-combat-escalation.md`)

- **Invulnerability sources are independent.** Hit invulnerability (until 0.8 s after a hit) and dash
  invulnerability (the full dash duration) are separate timers. The player is invulnerable while
  either is active. A dash can start once hit-stun has ended, even while hit invulnerability is still
  running. A dash ending does not shorten remaining hit invulnerability. A hit cannot land during a
  dash, so hit-stun cannot begin during one.
- **Input during hit-stun is ignored, not buffered.** This covers dash and attack alike. See D-003.

## Enemies

| Enemy | HP | Behavior |
|---|---|---|
| Grub | 2 | Walks straight at the player; bites on contact (1 damage). No telegraph. |
| Spitter | 2 | Stationary; fires a slow projectile at the player every 2 s. |

Proposed Phase 2 variants (Lunge Grub, Fan Spitter) are described in `design/g001-combat-escalation.md`.
They are pending feasibility and telegraph review and are not part of the build until approved.

## Rooms

5 rooms, 3–7 enemies each, mixed Grubs and Spitters. A room ends when all enemies are defeated.
Per-room composition, spawn edges, waves, and Spitter placement are defined in
`design/g001-combat-escalation.md` (Phase 1).

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
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

<<<FILE sim/repo-notes.md
# Simulated repository notes — lantern-depths (build 0.3.1)

Dry-run stand-in for reading the game's code. Implementation facts only — never load this for a Playtester.

- Enemies share one controller with the states Idle, Chase and Attack. Per-type behavior is data (speed, HP, attack type) plus a small per-type attack routine.
- Hit reaction: an enemy hit by the player enters a 0.2 s Flinch state that interrupts whatever it is doing (including Attack), then returns to Chase. Not described in `design/combat.md`.
- Damage: the player's attack is a short arc hitbox in front of the player. Enemies take damage on overlap. There is no concept of blocking or facing yet.
- Player invulnerability: the shared on/off flag and its two timers were removed. The player now has two expiry timestamps on the accumulated game clock (sum of delta times): `hitInvulnUntil` (set to hit time + 0.8 s on a hit) and `dashInvulnUntil` (set to dash start time + 0.25 s on dash start). `isInvulnerable(now)` returns `now < max(hitInvulnUntil, dashInvulnUntil)`. Every damage source (Grub contact, Spitter projectile) calls it. Neither window cancels or shortens the other. Hit-stun remains 0.3 s with no input. Dash distance, duration and 0.6 s cooldown unchanged. Attack queued during a dash still fires on dash end. Dash pressed during hit-stun is handled as before (unspecified).
- No other writers of the old flag were found; no flicker or sound cues for invulnerability are described.
- Movement: simple steering; walls stop movement.
- Tests: unit tests for `isInvulnerable` on a simulated game clock, run at fixed steps of 1/30 s and 1/60 s and with varying delta times. They cover dash only, hit only, dashes started 0.3, 0.5, 0.55, 0.6, 0.79 and 0.8 s after a hit, and damage attempts every step up to 1.2 s after a hit. No tests for enemies.
- Game loop uses variable delta time; 30 and 60 FPS supported.
>>>END

<<<FILE sim/build-0.4.md
# Simulated build 0.3.1 — what playing it looks like

Dry-run stand-in for a real build: a player-observable description only.

- Room 1–2: Grubs crawl toward you. Standing still and pressing attack kills each in two swipes before it reaches you. You take damage only if three arrive at once.
- Room 3: Spitters. Their projectile is slow; a single step sideways avoids it. You walk up and swipe them twice.
- Room 4–5: mixed rooms. The same pattern works: back into a corner, face the Grubs, swipe; step aside from projectiles.
- The dash is rarely needed. Most runs use it only to cross the room faster.
- Every room ends the same way: hold position, swipe until empty. A run feels the same at minute 2 and minute 15.

Dash and hit protection (same at 30 FPS and 60 FPS; only the exact frame at which an edge lands differs):

- Dash with no preceding hit: you cannot be damaged for the full 0.25 s of the dash. Damage can land immediately after it ends.
- Getting hit: you cannot be damaged for 0.8 s after the hit. You are stunned with no input for the first 0.3 s. After 0.8 s damage can land again.
- Dash started between 0.3 s and 0.55 s after a hit: no damage during the dash, and none after the dash ends. You stay protected until 0.8 s after the hit, then damage can land again.
- Dash started between 0.55 s and just under 0.8 s after a hit: no damage during the dash. Protection lasts through the end of the dash and at least until 0.8 s after the hit, whichever is later. Damage cannot land partway through the dash.
- Dash started at 0.8 s or later after a hit: the hit protection has ended; the dash gives its own 0.25 s of protection.
- This holds for Grub contact and Spitter projectiles alike, and for dashes toward or away from the damage source.
- Compared with 0.3, a hit followed quickly by a dash now gives more safe time, since the dash ending no longer ends the hit protection early.
- A damage event landing exactly on the 0.8 s or 0.25 s boundary counts as after protection; at 30 FPS versus 60 FPS this can differ by one frame.
- Dash distance, dash duration and the 0.6 s dash cooldown are unchanged. An attack pressed during a dash still fires when the dash ends. A dash pressed during hit-stun behaves as it did in 0.3.
- No other changes to enemies, rooms or attacks.
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

<<<FILE decisions/D-003-input-during-hit-stun.md
---
kind: decision
id: D-003
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-11
supersedes: none
---
# D-003: Input during hit-stun is ignored, not buffered

## Decision

During the 0.3 s hit-stun, a dash or attack press is ignored. It is not buffered and does not fire when hit-stun ends. Hit invulnerability and dash invulnerability are independent timers, and the player is invulnerable while either is active. This is recorded in `design/combat.md`.

## Rationale

- `combat.md` already says hit-stun means no input. This states what that rule implies and answers the open question from QA and engineering.
- Buffering would be a retuning of hit-stun, which D-002 excludes (Option C is not adopted).
- It is the simplest rule to build and to verify. The 0.3 s window is short, so the player loses little.

## Alternatives considered

- **Buffer the dash during hit-stun:** more forgiving, but it weakens the cost of a hit and changes tuning that D-002 keeps out of scope.
- **Leave it unspecified:** QA and engineering would keep guessing.

## Revisit when

Playtests show pad players lose inputs unfairly during hit-stun, or Option C is reconsidered.
>>>END

<<<FILE decisions/D-004-phase-2-technical-approach.md
---
kind: decision
id: D-004
status: accepted
decided_by: technical-director
goal: G-001
date: 2026-10-11
supersedes: none
---
# D-004: Time-parametrized, sub-stepped lunge hit check; Fan Spitter over the repositioning Spitter; Phase 1 as one serial Build

## Decision

1. **Lunge motion and hit check.**
   - Lunge position is a function of elapsed time since a scheduled lunge-start timestamp on the accumulated game clock. It is not accumulated `velocity * dt`.
   - Each frame the Grub advances in sub-steps of at most about 0.25 tile (or a fraction of the smaller hitbox radius, if smaller), using the existing wall-stop movement and the existing overlap and contact test.
   - Each sub-step calls `isInvulnerable(t)` with that sub-step's time.
   - At most one hit per lunge.
   - Wind-up and lunge start on scheduled timestamps (wind-up start + 0.6 s), not on the frame that notices the expiry.
2. **Phase 2 Spitter variant: the Fan Spitter, not the repositioning Spitter.** It reuses the Spitter routine and projectile and needs no movement or pathing. The designer delegated the choice to the cheaper option.
3. **Phase 1 goes to Build as one serial task list with no separate Plan gate and no isolated workspace.** Build's first task reports current values (speeds, hearts, room size, spawner and marker support, hit-stun input behavior). If a spawner rework beyond a small scheduler is needed, it comes back to the technical-director.
4. **Gameplay numbers stay data** (timings, ranges, angles, counts), not code constants, so tuning needs no code change.

Not decided here: how the existing 0.2 s Flinch behaves for Phase 2 states. That is player-facing and goes to the game-designer (handoff 16, Open questions 1 and 2). The technical mechanism will be a per-state flinch-immune flag.

## Rationale

- The lunge moves 0.56 tile per frame at 30 FPS. A time-parametrized path with sub-stepping gives identical distance at 30 and 60 FPS and prevents tunneling, using only existing movement, overlap and invulnerability code.
- The Fan Spitter costs mostly data plus a charge and an aim lock. The repositioning Spitter needs wall selection and movement, and it interacts with the Phase 1 placement rules.
- Phase 1 tasks all touch the same spawner and enemy controller, so they cannot safely run in parallel. The risk is moderate and mostly about timers, which a test on the simulated clock covers.

## Alternatives considered

- **Analytic swept test (segment against hitbox) per frame:** exact and a little cheaper at run time, but it adds a new collision primitive, and wall-stop movement would still need separate handling. It can replace sub-stepping if profiling shows a need.
- **Per-frame velocity integration with an end-of-frame test:** tunnels at 30 FPS and differs between frame rates. Rejected.
- **Repositioning Spitter:** higher cost and more risk, less direct dash purpose. Rejected.
- **A separate Plan gate for Phase 1:** no benefit given the serial, low-risk task list. Rejected.
- **Parallel Phase 2 routines in isolated workspaces:** too small to be worth the merge risk on the shared flinch flag. Rejected.

## Revisit when

- Build's report shows Phase 1 needs more than a small scheduler.
- Profiling shows sub-stepping is too costly (use the analytic swept test).
- The designer changes the lunge speed or distance enough that the sub-step size no longer fits.
- The art-director's telegraph cost makes the Lunge Grub or Fan Spitter more expensive than assessed here.
>>>END

<<<FILE goals/G-001-combat-monotony/15-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 15
from: qa
to: studio
stage: Verify
outcome: question
---
# 15: qa → studio — Dash/hit invulnerability fix: build 0.4 matches most criteria, but dash-in-hit-stun cannot be judged, so no pass

## Task

Route a request to `gameplay-engineer` (via Studio) to make the hit-stun dash behavior in `sim/build-0.4.md` observable and consistent with D-003. Then re-route verification to QA. This step gives no `pass` or `fail`, because one required case cannot be judged from the build.

## Context

Goal G-001 (combat monotony). Handoff 12 asked QA to verify the fix against the six criteria in `05-qa-to-studio.md` at 30 and 60 FPS. This time the build files were supplied (`sim/build-0.4.md`, baseline `sim/build-0.3.md`). The handoff says criterion 2 and 5 must cover a dash pressed during hit-stun, now specified by D-003 as ignored.

## Findings

### Verdict

No verdict. **Blocked on one case.** Nothing observed fails. A `pass` requires every criterion to pass, and one cannot be judged.

### The blocker

`sim/build-0.4.md` says only this about a dash pressed during hit-stun: "behaves as it did in 0.3." `sim/build-0.3.md` does not describe that behavior either. So neither build states whether the press is ignored, buffered or something else. D-003 requires "ignored, not buffered", and the build gives no observation to compare with it. Inferring "ignored" from "same as 0.3" would be inventing evidence. The spec is defined, so this is not a spec gap for `game-designer`. It is a build-observability gap.

### Other limits of the evidence

- The build files are player-observable prose, not run data. They give no repeat counts (criterion 1 needs at least 20 per frame rate) and no measured boundary results. They do not list rooms 1–5 individually. I cannot record "20 of 20 clean" or measured 0.8 s / 0.85 s results with the frame lengths (about 33 ms and 17 ms) in view. I can only compare what the description states against the criteria.
- `sim/build-0.4.md` has the heading "Simulated build 0.3.1". Its file name is 0.4. I assume they are the same build, but please confirm.

### Per-criterion comparison with `sim/build-0.4.md`

The build says its behavior is the same at 30 and 60 FPS, apart from which frame an edge lands on. The 30 and 60 FPS columns are therefore identical, and neither is an independently observed run.

| # | Criterion | 30 FPS | 60 FPS | Evidence (build 0.4 text) |
|---|---|---|---|---|
| 1 | Earliest dash (~0.3 s after hit): no damage in the 0.25 s dash, ≥20 repeats, Grub and Spitter | consistent; repeats not demonstrated | consistent; repeats not demonstrated | "Dash started between 0.3 s and 0.55 s after a hit: no damage during the dash, and none after… until 0.8 s"; holds for "Grub contact and Spitter projectiles alike". 0.3 had "Occasionally… you take damage partway through the dash"; 0.4 has no such line. |
| 2 | Varied delays: in hit-stun, just before, at and after 0.8 s | **not judgeable for hit-stun**; the other delays are consistent | **not judgeable for hit-stun**; the other delays are consistent | 0.3–0.55 s, 0.55–<0.8 s and ≥0.8 s are each described with no damage during the dash. The hit-stun press is "as it did in 0.3", which is not described. Boundary: a hit exactly on 0.8 s or 0.25 s counts as after protection, and "can differ by one frame". |
| 3 | Directions, rooms 1–5, Grubs and Spitters | consistent; per-room runs not shown | consistent; per-room runs not shown | "toward or away from the damage source"; Grub and Spitter named. Rooms are not mentioned in the dash text, and there are no other room changes. |
| 4 | Dash with no hit: full 0.25 s protection | consistent | consistent | "you cannot be damaged for the full 0.25 s of the dash. Damage can land immediately after it ends." |
| 5 | Existing rules: hit-stun 0.3 s with no input, hit invulnerability to 0.8 s, cooldown 0.6 s, attack queued in a dash fires at its end | partly consistent; hit-stun dash press not judgeable | partly consistent; hit-stun dash press not judgeable | Hit-stun 0.3 s with no input and protection to 0.8 s: stated. Cooldown "unchanged" at 0.6 s. Queued attack "still fires when the dash ends". The hit-stun press is undescribed (see blocker). |
| 6 | Mid-dash damage not delayed to land right after the dash; later damage normal | consistent; not observed directly | consistent; not observed directly | "Damage cannot land partway through the dash." After protection ends, damage lands normally. The text says nothing about damage being held or delayed. |

### Independence of the timers

This matches the `design/combat.md` clarification and D-003. 0.4 gives protection through the later of the dash end and 0.8 s after the hit. A dash ending does not cut short remaining hit protection. In 0.3 a quick dash after a hit could end that protection early. The 0.4 text says this no longer happens, and I found no contradiction with the spec.

### Regressions checked (description level only)

- Dash distance, duration and cooldown: unchanged.
- Enemies, rooms and attacks: "No other changes".
- Flicker and sound cues: **not checked**. The build text does not mention them.

### Undefined behavior and gaps

- The hit-stun dash press is unobserved in both builds (see blocker). The spec itself is defined by D-003.
- The one-frame difference at the 0.8 s and 0.25 s boundaries is stated, but not measured. A difference of more than one frame would be a failure, and it cannot be ruled out from prose.

### Plan once the case is observable

1. Press dash at several delays inside the 0.3 s hit-stun. Confirm that nothing fires then or when hit-stun ends (ignored, not buffered, per D-003). Also test an attack press. Do this at 30 and 60 FPS.
2. Run the matrix from handoff 10: dash delays of 0.3, 0.4, 0.5, 0.55, 0.6, 0.7, 0.79, 0.8 and 0.85 s. Keep a damage source present throughout. Record where damage lands: during the dash, between the dash end and 0.8 s, or after 0.8 s.
3. Repeat the earliest-dash case at least 20 times per frame rate.
4. Cover the no-hit dash, both directions, rooms 1–5 and both enemy types.
5. Record the boundary results at 0.8 s and 0.85 s at both frame rates.
6. Check the cooldown, queued attack and flicker/sound cues.

## Decisions already made

- D-001: Combat uses one attack button plus dash.
- D-003: Input during hit-stun is ignored, not buffered. Hit and dash invulnerability are independent timers.

## Constraints

- Verify from `design/combat.md`, the acceptance criteria and the build. Do not change the spec or the build.
- Must be verified at both 30 and 60 FPS.
- Do not count the fix as verified until the open case is observed.

## Open questions

- For Studio and `gameplay-engineer`: state in the build, in observable terms, what happens when dash or attack is pressed during hit-stun. D-003 requires that it is ignored and not buffered. If the build does something else, that is a failure to route back.
- For Studio: confirm that `sim/build-0.4.md` (heading "0.3.1") is the intended latest build.
- For Studio: if observed run data (repeat counts, boundary timings) can be supplied, include it. If the dry run can only offer prose, say so, and QA will judge the other criteria on the prose with that limit recorded.

## Expected output

Studio routes the open case to `gameplay-engineer` for an observable statement, then re-routes to `qa` with the updated build file. QA returns a `pass` or `fail` verification report. If the case cannot be made observable, Studio should not count the fix as verified.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: none
- Project: design/combat.md; project.md#constraints; sim/build-0.4.md; sim/build-0.3.md
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-003-input-during-hit-stun.md
- Previous handoff: goals/G-001-combat-monotony/12-studio-to-qa.md
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
