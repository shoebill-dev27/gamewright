---
kind: handoff
goal: G-001
seq: 5
from: studio
to: qa
stage: Verify
outcome: routed
---
# 05: studio → qa — Verify the dash-damage fix against build 0.4 (description is the build)

## Task

Verify the change for G-001 against acceptance criteria 1–6 from the defect report (`02-qa-to-gameplay-engineer.md`), using `sim/build-0.4.md` as the build under test, and issue a `pass` or `fail` verdict per criterion and overall.

## Context

Goal G-001: the player sometimes took damage partway through a dash, especially a dash started shortly after taking a hit. QA reproduced it (02) and a fix has been built (build 0.4). Your earlier attempt (04) returned a blocker because the build is only a description and not runnable. The Studio has resolved this: this is a dry-run sample project with no repository, and `project.md` states that builds are simulated under `sim/` and that "running the build" means reading the `sim/build-*.md` file, which is the project's player-visible artifact. So `sim/build-0.4.md` is the build. You are not asked to run code.

## Findings

Ruling on your 04 questions:

1. **Exercisable build:** `sim/build-0.4.md` is the build under test. No other build exists or is expected. Treat its player-observable statements as the observed behavior of the build, and check them against each criterion.
2. **Description-only check:** accepted for this project, because it is the project's defined way of running the build. This does not relax independence: judge from the criteria, `design/combat.md` and the build text, not from any explanation of why the fix should work. If the build text is silent or vague on a case a criterion needs (for example a specific delay, enemy type or frame rate), mark that criterion not verifiable from the build and say exactly what is missing, instead of assuming a pass.
3. **Criterion 6 tolerance (one-frame difference at an expiry boundary):** not decided here. Verify first. If the build text shows a difference between 30 and 60 FPS only in the single frame at an expiry boundary, record it as an observation with the exact wording. If you cannot decide criterion 6 from the criteria and `design/combat.md`, hand back with `outcome: question` and state the question precisely; the Studio will route it to `game-designer`. Do not redefine the criteria yourself.

Per-criterion handling reminder (the criteria themselves are in 02 and are unchanged):

- 1: no damage during a dash started right after hit-stun (about 0.3 s), for Grub and Spitter, at both frame rates.
- 2: no damage for dashes started at several delays inside the 0.8 s post-hit window, including the 0.55–0.8 s range.
- 3: regression, dash with no recent hit takes no damage.
- 4: regression, an undashed hit costs 1 heart, 0.3 s hit-stun, invulnerable until 0.8 s.
- 5: regression, dash 4 tiles / 0.25 s, cooldown 0.6 s, attack queued during a dash fires at its end.
- 6: same results at 30 and 60 FPS.

Also re-check the original reproduction (hit, then dash as soon as input returns) against the build text.

## Decisions already made

- D-001 (one attack button plus dash): no new inputs. Flag it if the build text implies any.

## Constraints

- Must play correctly at 30 and 60 FPS.
- No new input buttons beyond attack, dash and pause (D-001).
- Do not modify production code or redefine the acceptance criteria.
- Verify from the spec, the criteria and the build only.

## Open questions

- Criterion 6: is a one-frame difference at an expiry boundary within tolerance? Answer it only if the criteria and `design/combat.md` settle it; otherwise hand back with `question`.

## Expected output

A verification report in Findings with per-criterion status (pass / fail / not verifiable from build, with the exact missing information) at 30 and 60 FPS, plus any regressions. Write it as a Handoff addressed to `studio` (`to: studio`), with `outcome: pass`, `fail` or `question`. For a fail, give the exact delay, frame rate and enemy type, so the Studio can route it to `gameplay-engineer`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md (Constraints; the dry-run note under Current state and `player_visible`), design/combat.md, sim/build-0.4.md, goals/G-001-damage-during-dash/02-qa-to-gameplay-engineer.md (acceptance criteria 1–6)
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-damage-during-dash/04-qa-to-studio.md
