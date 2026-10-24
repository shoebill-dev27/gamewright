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
