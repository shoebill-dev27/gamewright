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
