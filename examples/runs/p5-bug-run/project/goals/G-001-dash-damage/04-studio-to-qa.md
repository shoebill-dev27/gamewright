---
kind: handoff
goal: G-001
seq: 4
from: studio
to: qa
stage: Verify
outcome: routed
---
# 04: studio → qa — Verify the fix for damage taken during a dash

## Task

Independently verify, against the acceptance criteria in handoff 02, that the player no longer takes damage at any moment of a dash (including the last dash frame), at both 30 and 60 FPS, and check for regressions.

## Context

Goal G-001. The Owner reported: "ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。" (Player sometimes takes damage while dashing.) You reproduced the defect earlier (damage on the last dash frame at 30 and 60 FPS; see handoff 02). The gameplay engineer has since changed the build (`repo/`, sha 36b3b8f9a16e). Intended behavior is in `design/combat.md`: the dash is invulnerable for its full duration.

## Findings

Observable summary of the change, for deciding what to exercise:

- Dash protection should now cover every frame of the dash, including the final one, for Grub contact and for Spitter projectiles.
- Dash rules (0.25 s, 4 tiles, 0.6 s cooldown), hit rules (1 heart, 0.3 s stun, 0.8 s invulnerability after a hit) and the attack queued during a dash are meant to be unchanged.
- Regression tests were added to `repo/tests/test_game.py`.

Areas worth exercising beyond your original repro script (not yet covered by play scripts):

- Dashing up and down, not only horizontally.
- Rooms 1–5 with several enemies.
- A queued attack combined with contact on the last dash frame.
- First-frame contact and Spitter projectiles on the first and last dash frames.
- Pass-through of a Grub mid-dash.
- A hit's invulnerability timer ending during a dash.
- Damage resuming normally after the dash ends (an enemy still in contact may hurt on the next frame; this is accepted in 02 and is not a defect unless it contradicts `design/combat.md`).

## Decisions already made

D-001: one attack button plus dash; no inputs added.

## Constraints

- Must play correctly at both 30 and 60 FPS.
- No change to documented dash or hit rules; do not judge dash design (distance, cooldown, invulnerability length), only conformance to `design/combat.md`.
- Run the build through the project's run commands: `python3 play.py --view player {script}`, `python3 play.py --view trace {script}`, and `python3 -m unittest discover -s tests` (from `repo/`).

## Open questions

None.

## Expected output

A verification report with a pass/fail verdict per acceptance criterion in handoff 02, with reproduction and trace evidence at 30 and 60 FPS, the result of your own run of the test suite, and any regressions found. Severity and reproducibility for any failure. Address the result to `studio`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#constraints, design/combat.md, manual.md, repo/README.md, repo/play.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-dash-damage/02-qa-to-gameplay-engineer.md
