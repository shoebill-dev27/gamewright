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
