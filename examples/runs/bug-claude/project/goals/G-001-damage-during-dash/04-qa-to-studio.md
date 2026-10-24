---
kind: handoff
goal: G-001
seq: 4
from: qa
to: studio
stage: Verify
outcome: question
---
# 04: qa → studio — Verify blocked: the build cannot be exercised, so no pass/fail verdict on G-001

## Task

Provide something QA can actually exercise (a runnable build, or logs or recordings from one), then re-route Verify. Alternatively, rule that a description-only check is acceptable. QA has not issued `pass` or `fail`, because either verdict would be a guess.

## Context

Goal G-001: the player took damage partway through a dash started shortly after a hit. The defect report (02) set six acceptance criteria, which are unchanged in 03. The Build step has since changed the game, and Verify is the step that follows. The handoff (03) says to report a blocker instead of guessing a verdict if the build cannot be exercised.

## Findings

### Why this is a blocker

- The only build artifact in the packet is `sim/build-0.4.md`. It is a player-observable description, not a runnable build, and has no logs, recordings or test output.
- Its last bullet says: "The fix has not been run or tested in this simulation; the description follows the change as specified." The text therefore restates the intended behavior and is not an observation of it.
- Passing on that basis would amount to relying on the implementer's account of why the fix works. `studio/roles/qa.md` (Independence) and `studio/skills/verify-change.md` (Do not) forbid this.
- Several criteria need observation that a description cannot give:
  - Criterion 1 needs at least 20 repetitions per frame rate, against both a Grub contact and a Spitter projectile.
  - Criterion 2 needs dashes at several delays after the hit, with extra repetitions between about 0.55 s and 0.8 s, at both frame rates.
  - Criterion 6 needs actual 30 vs. 60 FPS runs.
- The known intermittent defect and the boundary-timing risk (a dash within about one frame of the 0.8 s expiry) are exactly the cases a written description cannot establish.

### Per-criterion status

None of the six was observed, so none is marked pass or fail. The third column shows what the description claims, for the record only. It is not evidence.

| # | Criterion | Status | What `sim/build-0.4.md` claims (not evidence) |
|---|---|---|---|
| 1 | No damage during a dash started right after hit-stun (~0.3 s), ≥20 reps per FPS, Grub and Spitter | Not verified (30 FPS: none, 60 FPS: none) | No damage from dash start to dash end, for both enemy types |
| 2 | No damage for dashes at several delays in the 0.8 s window | Not verified (30 FPS: none, 60 FPS: none) | Dash started at 0.6–0.75 s stays protected through the whole dash; early dashes (~0.3 s, ~0.5 s) keep protection to 0.8 s |
| 3 | No-recent-hit dash: no damage (regression) | Not verified (30 FPS: none, 60 FPS: none) | Unchanged |
| 4 | Undashed hit: 1 heart, 0.3 s hit-stun, invulnerable until 0.8 s (regression) | Not verified (30 FPS: none, 60 FPS: none) | Unchanged |
| 5 | Dash 4 tiles / 0.25 s, cooldown 0.6 s, attack queued during a dash fires at its end | Not verified (30 FPS: none, 60 FPS: none) | Unchanged |
| 6 | Same results at 30 and 60 FPS | Not verified | Same, except frame-sized edge differences |

The original reproduction steps from 02 (hit, then dash as soon as input returns) were not re-run, because there was nothing to run.

### Observations from reading the description

These are not verdicts.

- The description says protection ends on the first frame at or after its end time. That can be up to about 33 ms late at 30 FPS and about 17 ms late at 60 FPS. A contact within one frame of an end time "can go either way depending on frame rate".
- Criterion 6 says results must be the same at 30 and 60 FPS. A strict reading could conflict with this edge behavior, even though the described difference is only frame quantization. Once the build is exercisable, QA needs a ruling on the tolerance: is a difference of one frame at an expiry boundary acceptable? If the intended behavior is not defined, the Studio should route that to `game-designer`.
- The description is consistent with the design in `design/combat.md` (full dash invulnerability, 0.3 s hit-stun, invulnerability until 0.8 s after the hit). This is only a consistency check, not a pass.

## Decisions already made

- D-001 (one attack button plus dash): no input was added, and nothing in the description suggests otherwise.

## Constraints

- Must play correctly at 30 and 60 FPS.
- No new input buttons beyond attack, dash and pause (D-001).
- QA must not modify the production code under verification, and must not redefine the acceptance criteria.

## Open questions

1. Can the Studio supply a build QA can run, or recorded output from one? It needs to cover the six criteria at 30 and 60 FPS, including the 0.55–0.8 s dash delays and the one-frame edge at the 0.8 s expiry.
2. If no runnable build exists, will the Studio explicitly accept a description-only check? QA does not recommend this, because the description says the fix was never run.
3. For criterion 6, is a one-frame difference at an expiry boundary within tolerance? If the spec is silent, route to `game-designer`.

## Expected output

The Studio resolves the blocker and re-routes Verify to `qa` with an exercisable build. QA then issues a `pass` or `fail` verdict against criteria 1–6 at 30 and 60 FPS. A failure goes to `gameplay-engineer` with the exact delay, frame rate and enemy type. No failure has been recorded, so the "same criterion fails a second time" escalation is not triggered.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#constraints, design/combat.md, sim/build-0.4.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-damage-during-dash/03-gameplay-engineer-to-qa.md
