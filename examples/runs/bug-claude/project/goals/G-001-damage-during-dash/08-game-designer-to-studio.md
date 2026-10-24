---
kind: handoff
goal: G-001
seq: 8
from: game-designer
to: studio
stage: Verify
outcome: done
---
# 08: game-designer → studio — Criterion 6 ruled: one-frame late-only difference at expiry is accepted

## Task

Route Verify to `qa` for the final overall verdict on G-001, applying the criterion 6 ruling below. Nothing goes to `gameplay-engineer` unless QA finds a failure.

## Context

Goal G-001: the player took damage partway through a dash started shortly after a hit. Build 0.4 fixes it. QA (`06-qa-to-studio.md`) passed criteria 1–5 at 30 and 60 FPS. Criterion 6 ("same results at 30 and 60 FPS") was undecided, because `sim/build-0.4.md` says protection ends on the first frame at or after its end time, up to about 33 ms late at 30 FPS and about 17 ms late at 60 FPS, and the design gave no tolerance.

## Findings

**Ruling (Question 1): the difference is acceptable.** Protection expiry may be late by less than one frame at the running frame rate (under 34 ms at 30 FPS, under 17 ms at 60 FPS). It must never be early. This matches what build 0.4 describes. Time-exact, frame-rate-independent expiry is not required, so no engineering change is needed.

**Scope (Question 2):** the ruling covers both boundaries, the dash end and the 0.8 s post-hit mark, and both enemy types (Grub contact and Spitter projectile). There are no differences between them.

**Escalation (Question 3):** no dash or damage rule changes, and neither vision nor scope is touched. The ruling is within the Game Designer's authority, so there is no hand-back to `game-director`.

**Acceptance criterion for QA (criterion 6)**, at both 30 and 60 FPS, for each boundary and enemy type:
1. Contact at or before the end time: no damage.
2. Contact later than the end time plus one frame (34 ms at 30 FPS, 17 ms at 60 FPS): 1 heart of damage.
3. Contact between those two moments: either result passes. A 30 vs 60 FPS difference here is not a failure.
4. No other difference between frame rates in damage, dash or hit-stun results.

Files written:
- `design/combat.md`: new section "Protection expiry and frame rate" with the rule and the QA criterion.
- `decisions/D-002-protection-expiry-frame-tolerance.md`: records the ruling, because it constrains any future timed protection.

## Decisions already made

- D-001: one attack button plus dash. Not affected.
- D-002 (new): protection expiry may be late by up to one frame, never early.

## Constraints

- Must play correctly at 30 and 60 FPS.
- Dash and damage rules unchanged (full-duration dash invulnerability, 1 heart per hit, 0.3 s hit-stun, invulnerable until 0.8 s).
- QA does not redefine criteria. Criterion 6 is now defined by the design rule above.

## Open questions

None. If QA finds protection ending early at any frame rate, or lasting more than one frame past its end time, that is a criterion 6 failure and goes to `gameplay-engineer`.

## Expected output

QA issues the overall verdict for G-001 against criteria 1–6. Criteria 1–5 are already recorded as pass. With the criterion 6 ruling applied, build 0.4's stated behavior (late by under one frame, never early) meets it, so the expected verdict is `pass`. QA returns the verdict to the Studio.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#constraints, design/combat.md, sim/build-0.4.md, goals/G-001-damage-during-dash/02-qa-to-gameplay-engineer.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-protection-expiry-frame-tolerance.md
- Previous handoff: goals/G-001-damage-during-dash/06-qa-to-studio.md
