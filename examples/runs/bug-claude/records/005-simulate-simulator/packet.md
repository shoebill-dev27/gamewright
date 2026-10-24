# Studio operation packet

operation: Simulate (dry-run harness, not a Studio operation)
goal: G-001

## You may write

- sim/build-0.4.md
- sim/repo-notes.md

## Inputs

<<<FILE simulator-instructions
You are the dry-run build simulator. You are not a Studio Role and make no decisions.

The game does not exist; its build and code are described in text. A change was just implemented.
From the engineer's description of the change, the previous build description and the repository
notes, write two files:

1. The new build description: what a player and a tester can observe when they run the changed
   game, under every condition the project constraints name (for example each supported frame
   rate). Describe what would actually happen given the change as implemented, including any flaw
   the description implies — not what was intended. Player-observable behavior only: no design
   intent, no acceptance-criteria names, no implementation terms. Do not copy HTML comments.
2. The updated repository notes: implementation facts after the change.

Write each file as a file block (<<<FILE <path> ... >>>END) using exactly the paths under
"You may write". Text outside file blocks is discarded.
>>>END

<<<FILE goals/G-001-damage-during-dash/03-gameplay-engineer-to-qa.md
---
kind: handoff
goal: G-001
seq: 3
from: gameplay-engineer
to: qa
stage: Verify
outcome: done
---
# 03: gameplay-engineer → qa — Verify fix: no damage at any point during a dash, including a dash started after a recent hit

## Task

Verify the fix for the G-001 defect (player takes damage partway through a dash started shortly after being hit) against the six acceptance criteria below. Run them at both 30 FPS and 60 FPS. The criteria are unchanged from your defect report (02).

## Context

Goal G-001. The Owner reported that damage sometimes lands during a dash. QA's report (02) reproduced it for a dash started soon after a hit and confirmed that `design/combat.md` requires full-duration dash invulnerability. This step is the Build fix. Verify is next.

## Findings

### What changed and where

- **Player invulnerability** is no longer a single on/off flag switched by two independent timers.
  - The player now tracks two separate sources: dash invulnerability (ends 0.25 s after dash start) and post-hit invulnerability (ends 0.8 s after the hit).
  - The player is invulnerable while either source is still active.
  - A source expiring can no longer end protection that the other source still provides.
- **Unchanged:** dash distance and duration (4 tiles over 0.25 s), dash cooldown (0.6 s), the attack queued during a dash, the hit-stun (0.3 s), the damage (1 heart), and the input set (D-001). Enemy behavior is untouched.
- **Root cause (short):** the old shared flag was cleared by whichever timer expired first, even if the other was still running. Details are in the sender-only notes.
- **Scope of the fix:** it is in the player's shared invulnerability logic. It does not depend on the enemy type, so Grub bites and Spitter projectiles go through the same path.

### How to exercise it

1. Enter a room with Grubs and/or Spitters and take one hit.
2. Dash at different delays after the hit:
   - the moment input returns (about 0.3 s after the hit);
   - about 0.5 s after the hit;
   - about 0.6–0.75 s after the hit;
   - just before 0.8 s after the hit.
3. Keep a Grub touching you, or a projectile arriving, throughout each dash.
4. Confirm no heart is lost from dash start to dash end.
5. Also check that a hit taken without dashing still gives 1 heart of damage, 0.3 s of hit-stun and invulnerability until 0.8 s after the hit.
6. Repeat everything at 30 FPS and at 60 FPS.

Most likely failure window: a dash that starts after roughly 0.55 s and before 0.8 s after the hit, so that the 0.8 s post-hit limit falls during the dash. Test this range with extra repetitions at both frame rates. Also check that the player is still protected for the rest of the 0.8 s window after a dash that began earlier and ended inside it.

### Acceptance criteria (unchanged)

1. Take a hit, then dash as soon as input returns after hit-stun (about 0.3 s after the hit). Repeat at least 20 times per frame rate, against a Grub contact and against a Spitter projectile. The player takes no damage at any moment from dash start to dash end (0.25 s).
2. Repeat the above, starting the dash at several delays after the hit (immediately after hit-stun, and during the remainder of the 0.8 s post-hit invulnerability window). No damage during the dash in any case.
3. With no recent hit, dashing through a Grub or into a projectile still causes no damage during the dash (no regression).
4. Without dashing, a hit still deals 1 heart, applies 0.3 s hit-stun, and grants invulnerability until 0.8 s after the hit (no regression).
5. Dash distance and duration are unchanged (4 tiles over 0.25 s), cooldown is unchanged (0.6 s), and an attack pressed during a dash still fires when the dash ends.
6. Results are the same at 30 and 60 FPS.

### Known risks

- Boundary timing: a dash started within about one frame of the 0.8 s post-hit expiry. At 30 FPS a frame is about 33 ms, so check this edge at both frame rates.
- The repository has no tests for invulnerability or enemies. Verification is manual, by the steps above.

## Decisions already made

- D-001 (one attack button plus dash): no input was added.

## Constraints

- Must play correctly at 30 and 60 FPS.
- No new input buttons beyond attack, dash and pause (D-001).
- Design unchanged: dash invulnerability is as specified in `design/combat.md`.

## Open questions

None for QA. If any criterion fails, or damage appears at a delay not listed above, report the delay, frame rate and enemy type.

## Expected output

A verdict handoff (`pass` or `fail`) against criteria 1–6, with results at 30 and 60 FPS. A failure goes back to `gameplay-engineer` with the exact delay, frame rate and enemy involved.

## Sender assessment

**Root cause (from `sim/repo-notes.md`):**
- Invulnerability is one flag. The dash sets it on and starts a 0.25 s timer. A hit sets it on and starts a timer ending 0.8 s after the hit. Each timer clears the flag when it ends, regardless of the other.
- Dash started at delay d after the hit, where d is at least about 0.3 s because of hit-stun. The post-hit timer clears the flag at 0.8 s after the hit.
  - If 0.55 s < d < 0.8 s, the post-hit timer expires partway through the dash and the player is vulnerable for the rest of it. This is the reported "partway through the dash, occasionally" and is the actual spec violation.
  - If d < 0.55 s, the dash timer clears the flag at d + 0.25 s, before the post-hit window ends. The player loses the remainder of the 0.8 s protection after the dash. The design does not allow this either, though it is not the reported symptom.
- Frame rate is not the cause. It only moves where the boundary falls by up to one frame, so both frame rates need testing.
- The fault is in the shared player invulnerability path, so it is independent of Grub vs. Spitter. I could not confirm from the packet which enemy dealt the damage in the Owner's case, and the fix does not need that.

**Limits of this work, which QA should weigh:**
- The packet contained only the observable build description and implementation notes, no source files and no way to run the game. I could not edit the source or run tests in this operation. The change above is specified from the repo notes (two independent invulnerability sources, invulnerable while either is active).
- No test results exist. I have not verified the fix, and I am not claiming the 30/60 FPS behavior is confirmed.
- Before or alongside Verify, someone with repository access should confirm the change is applied as described. A unit test for the sequence "hit, dash at 0.6 s, check invulnerable through 0.85 s" at both frame rates would cover it, since the repository has none. If the change turns out to be non-local, hand back to `technical-director` (Plan).
- Confidence in the root cause is high from the notes, but the fix is untested.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#constraints, design/combat.md, sim/build-0.3.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-damage-during-dash/02-qa-to-gameplay-engineer.md
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
>>>END
