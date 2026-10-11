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
   Write it as observations of the running build (by the project's dry-run convention, this text is
   the build); do not add notes about the simulation itself.
2. The updated repository notes: implementation facts after the change.

Write each file as a file block (<<<FILE <path> ... >>>END) using exactly the paths under
"You may write". Text outside file blocks is discarded.
>>>END

<<<FILE goals/G-001-dash-damage/03-gameplay-engineer-to-qa.md
---
kind: handoff
goal: G-001
seq: 3
from: gameplay-engineer
to: qa
stage: Verify
outcome: done
---
# 03: gameplay-engineer → qa — Verify fix: player takes damage mid-dash when the dash overlaps the end of post-hit invulnerability

## Task

Verify the fix below against the acceptance criteria in handoff 02, at both 30 FPS and 60 FPS. Give a pass or fail verdict.

## Context

Goal G-001. The Owner reported: "Sometimes I take damage even while dashing." QA's defect report (02) established that `design/combat.md` says the dash makes the player invulnerable for its full 0.25 s. It also says a hit is followed by 0.3 s hit-stun and then invulnerability until 0.8 s after the hit. The engineer found the root cause in the player invulnerability code. The change is stated exactly below. It counts as made once stated, per the dry-run rules in `project.md#constraints`.

## Findings

### Root cause

The player has a single invulnerability on/off flag. Two independent timers share it: the dash timer (0.25 s) and the post-hit timer (ends 0.8 s after the hit). Each timer switches the flag off when it ends, without checking whether the other source still needs it.

Consequence for the reported case. A dash started in the window of roughly 0.55 s to 0.8 s after a hit outlives the post-hit timer. At 0.8 s the post-hit timer switches the flag off while the dash is still running. The player is then vulnerable for the rest of the dash, which is the reported damage.

- Example: a hit at t=0 and a dash at t=0.6 s. The post-hit timer clears the flag at t=0.8 s, and the dash runs until t=0.85 s. The last 0.05 s of the dash is unprotected.

The same flaw also affects the reverse order, which the report did not list. A dash started right after hit-stun (0.3 s) ends at 0.55 s. The dash timer then switches the flag off while post-hit invulnerability should still last until 0.8 s. The player becomes vulnerable up to 0.25 s early, which violates the rule "invulnerability until 0.8 s after the hit". QA should check this as part of the regression criteria.

A dash with no recent hit is not affected by this cause, because only one timer is involved.

### Change

Where: the player invulnerability logic (the one on/off flag and its two timers). The enemy controller, hit-stun, dash movement and cooldown are not touched.

What:
1. Remove the shared on/off flag and the two "switch the flag off" timer callbacks.
2. Keep two independent sources of invulnerability:
   - Dash source: the player is invulnerable while the dash state is active. It is read from the dash state itself, not from a separate timer. This covers the whole dash, including the final frame.
   - Post-hit source: on a hit, store `hitInvulnUntil = hitTime + 0.8 s`, using accumulated game time (the sum of delta time). The source is active while `gameTime < hitInvulnUntil`.
3. The player is invulnerable if either source is active: `isInvulnerable = isDashing || gameTime < hitInvulnUntil`.
4. The damage check reads `isInvulnerable` at the moment damage would apply. Nothing writes to a flag any more, so one source ending cannot cancel the other.

Frame rate: both sources compare against accumulated game time or the dash state. No per-frame countdown is decremented, so the result does not depend on the frame rate. Quantization at 30 FPS is at most one frame (about 33 ms) of timing on the end of the 0.8 s window.

Tests added. The project had none for invulnerability. Add unit tests that step the simulation with fixed delta times of 1/30 s and 1/60 s, for these cases:
- A hit at t=0, then a dash at 0.3, 0.4, 0.55, 0.7 and 0.79 s. Assert no damage is applied at any step of the dash.
- No damage during a dash with no prior hit.
- After a dash that ends before 0.8 s, damage is still blocked until 0.8 s after the hit and applies after that.
- A dash and a hit in the same frame.

### How to exercise it (maps to the acceptance criteria in 02)

At both 30 FPS and 60 FPS:
1. Get hit, then dash at about 0.3 s, 0.4 s, 0.55 s, 0.7 s and 0.79 s after the hit, with a Grub in contact range. Expect no damage for the full dash (criteria 1 and 2).
2. Repeat with a Spitter projectile crossing the dash path (criterion 3).
3. Dash with no recent hit and enemies in contact range. Expect no damage (criterion 4).
4. Regression (criterion 5):
   - Dash is still 4 tiles over 0.25 s, with a 0.6 s cooldown.
   - An attack pressed during a dash is still queued and fires when the dash ends.
   - A hit still deals 1 heart with 0.3 s hit-stun.
   - After a dash that ends before 0.8 s after the hit, the player stays invulnerable until 0.8 s after the hit. This is a new check for the reverse-order flaw described above.
   - Once the dash and the post-hit window have both ended, the player takes damage normally.

### Known risks

- Behavior change beyond the report: after an early dash, post-hit invulnerability now correctly lasts until 0.8 s. Previously it could be cut short. This matches the design text, but players may notice slightly more safety right after a hit.
- Damage that lands on the exact frame a dash starts or ends depends on the order of the dash-state update and the damage check within a frame. The fix reads the dash state at the time of the check. QA should include a dash started and a dash ended while an enemy is in contact range.
- The enemy Flinch behavior (an enemy hit by the player gets a 0.2 s Flinch) is untouched. If damage still occurs during a dash after this fix, look at other damage sources.

## Decisions already made

- D-001: no new input buttons beyond attack, dash and pause. This fix adds none.

## Constraints

- Must play correctly at both 30 and 60 FPS.
- Desktop, keyboard and gamepad.
- Reuse existing systems (small team). The fix reuses the existing dash state and hit event.
- No new input buttons (D-001).

## Open questions

None. The design is unambiguous when dash and post-hit invulnerability overlap: both rules apply, so the player is invulnerable until the later of the two ends.

## Expected output

A verification Handoff with outcome `pass` or `fail`, stating the result for each acceptance criterion at 30 FPS and at 60 FPS. A `pass` goes to the next step as the Studio decides. A `fail` goes back to `gameplay-engineer` with the failing conditions.

## Sender assessment

- Root cause: confidence is high, from the implementation notes. The single on/off flag with two timers that each clear it on expiry produces exactly the reported symptom: occasional damage when a dash is started shortly after a hit. The window is the 0.55 s to 0.8 s range from QA's hypothesis, which is consistent with it.
- Frame rate: the cause is not frame-rate dependent by itself. The window is set by the timer arithmetic. A variable delta time only shifts the exact moment of expiry by up to one frame. The fix uses game-time comparison and dash state, so both frame rates should behave the same.
- Self-test: no real build exists in this dry-run. The verdicts are from reasoning about the code path and the described unit tests, not from execution. QA must verify independently.
- Not confirmed: whether any damage during a dash with no prior hit exists. No other mechanism is known from the notes. If QA reproduces damage in criterion 4, the cause is something else, so hand back.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: project.md#constraints, design/combat.md, sim/build-0.3.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-dash-damage/02-qa-to-gameplay-engineer.md
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
