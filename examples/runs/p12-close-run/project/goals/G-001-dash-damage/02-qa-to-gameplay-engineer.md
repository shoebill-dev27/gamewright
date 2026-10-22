---
kind: handoff
goal: G-001
seq: 2
from: qa
to: gameplay-engineer
stage: Build
outcome: done
---
# 02: qa → gameplay-engineer — Fix: player takes damage while dashing (dash begun during post-hit invulnerability)

## Task

Fix the reproduced defect below so that the player cannot take damage at any moment of a dash, at both 30 and 60 FPS. The acceptance criteria are in Findings.

## Context

Goal G-001. The Owner reported (ja): 「ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。」 ("I sometimes take damage even while dashing."). QA reproduced it in the practice room with deterministic scripts, at both 30 and 60 FPS. The Studio handoff (01) asked for a defect report. `design/combat.md` defines the intended behavior, so this goes to the engineer.

## Findings

### Summary

Damage can be taken while a dash is still in progress. The conditions seen:

1. The player is still in the post-hit invulnerability window (0.8 s after a hit).
2. The player starts a dash while that window has less time left than the dash duration (0.25 s). In the runs, 0.067 s were left.
3. The post-hit invulnerability ends while the dash is still active (`dash_left` > 0).
4. At that moment the player is vulnerable, and an attack that arrives during the remaining dash time hurts them.

The confirmed case is a Spitter shot. A Grub contact in the same window was not tested to a hit (see "Not established").

### Source of "expected" (quoted from `design/combat.md`)

- "**Dash**: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration."
- "**Getting hit**: 1 heart of damage, 0.3 s hit-stun (no input), then invulnerability until 0.8 s after the hit."

Both rules grant invulnerability. The dash rule says "the full dash duration" without exception. Damage during a dash is therefore a defect against the document, and the spec is not silent. The document does not state how the two invulnerability sources combine. The dash rule alone is enough to decide the cases below, because the dash lasts the full 0.25 s.

### Reproduction script A (Spitter shot), deterministic

```text
room empty
fps 60
end 4
player 8 4
spawn grub 10 4
spawn spitter 14 4
0.2 dash right
1.0 dash left
2.0 dash right
```

Run with `python3 play.py --view player {script}` or `--view trace`. Frequency: 2 of 2 runs, with identical results because the simulation is scripted. The same script with `fps 30` also reproduced it.

**Setup:** the first dash at 0.2 s works. The Grub reaches the player after that dash and hits at about 1.28 s (hearts 3→2). That is expected, because the player is not dashing. The 1.0 s dash is ignored ("dash not ready"), which is also not a defect. The Spitter fires at 2.000 s. The player dashes right at about 2.0 s, which is inside the 0.8 s post-hit window.

**60 FPS trace:**
- t=2.000: `hurt_left=0.083`, `invulnerable=True`, spit.
- t=2.017 (frame 121): dash starts, `dash_left=0.233`, `hurt_left=0.067`.
- t=2.083 (frame 125): `invulnerable {'value': False, 'why': 'hurt timer ended'}`, then `hurt {'source': 'shot', 'hearts': 1}`. At this point `dash_left=0.167`, so the dash is still active.
- The player-view line reads "2.083 YOU ARE HIT by a shot — hearts 1/3". Hearts go 2→1.
- The dash ended at t=2.250.

**30 FPS trace:**
- t=2.033 (frame 61): dash starts, `hurt_left=0.033`.
- t=2.067 (frame 62): `invulnerable False ('hurt timer ended')`, `dash_left=0.183`.
- t=2.100 (frame 63): `hurt {'source': 'shot', 'hearts': 1}`, `dash_left=0.150`. Hit during the dash.
- The dash ended at frame 68.

The defect does **not** depend on frame rate. Only the exact timestamps shift by a frame or two.

### Related observations (trace evidence, no cause asserted)

- **Flag drops mid-dash.** In script B (below, no Spitter), `invulnerable` also becomes False when "hurt timer ended" at t=2.083 with `dash_left=0.067`, and stays False until `dash_end` at 2.150 (frames 125–129). No damage followed because the Grub was about 2 tiles away. This confirms the window exists independently of the Spitter. It also shows a damaging source in that window would hurt.
- **Flag drops after a dash.** In script A at 60 FPS, after the second hit (2.083) the player has `hurt_left=0.800`. At `dash_end` (t=2.250) the trace shows `invulnerable=False` while `hurt_left=0.633` and `stun_left=0.133` remain. The doc says invulnerability lasts until 0.8 s after a hit, so this looks like a second discrepancy. The 30 FPS trace shows the same at frame 68. No damage was observed in that window, because the enemies were far away. It should be checked as part of the fix.
- **Hypothesis only (not verified):** the invulnerable flag appears to be driven by whichever timer ended most recently rather than by the combination of the two sources. The engineer decides the actual cause.

### Script B (Grub only, no damage; evidence of the window)

```text
room empty
fps 60
end 4
player 8 4
spawn grub 10 4
0.2 dash right
1.0 dash left
1.9 dash left
```

Result: the flag drops at 2.083 mid-dash, no hit. The player is hit at 3.400 after the dash, which is expected.

### Boundary

- Hit during the dash is shown when the post-hit invulnerability ends while the dash is active (dash started with `hurt_left` 0.067 at 60 FPS and 0.033 at 30 FPS).
- Dashes started when there was no post-hit invulnerability left, and the first dash at 0.2 s, were invulnerable for the whole dash in all runs (`invulnerable=True, why 'dash'` until `dash_end`).
- QA did not sweep other `hurt_left` values or dash timings.

### Not established (explicitly)

- Whether a Grub contact hit during a dash is reproducible. Script B shows the vulnerable window, but not an actual Grub hit during the dash.
- The full range of start offsets (other `hurt_left` values) that expose the window.
- The `run_tests` result was not obtained. The existing tests were not run, so the baseline test status is unknown.

### Severity and frequency

- **Severity:** hurts the experience. The player loses a heart during an action the rules call invulnerable, and in a one-button game with dash as the only defense this is felt as unfair. It does not block progress.
- **Frequency:** deterministic once the conditions are met. In real play it needs a dash started shortly before the post-hit window ends and an attack arriving in the remaining dash time. That is plausible for "dash out right after being hit", the most common panic response.
- **Reproducibility:** 100% with script A at 30 and 60 FPS.

### Acceptance criteria (player-observable; each at 30 FPS and at 60 FPS)

1. **Script A** (and its `fps 30` variant): no "YOU ARE HIT" line appears between a "you dash" line and the dash's end. Specifically, the shot at about 2.08–2.10 s does not reduce hearts. Hearts stay 2/3 through the dash.
2. A dash started at any point during the post-hit invulnerability window, including with under 0.25 s remaining, is invulnerable for its full 0.25 s. A Spitter shot or Grub contact arriving at any time in that dash does not hurt.
3. Invulnerability lasts until the later of dash end and 0.8 s after the last hit. After the dash ends, if the 0.8 s window has not elapsed, hits are still ignored. In script A the trace at `dash_end` must still report invulnerable while `hurt_left` > 0.
4. Unchanged behavior:
   - A hit while not dashing and not in the post-hit window still costs 1 heart, with 0.3 s hit-stun.
   - The post-hit invulnerability still ends 0.8 s after the hit.
   - A dash with no preceding hit is still invulnerable for exactly 0.25 s.
   - Dash cooldown behavior is unchanged.
5. `python3 -m unittest discover -s tests` passes, with a regression test added for the dash-in-post-hit-window case at both frame rates.

## Decisions already made

- D-001: combat uses one attack button plus dash. No new input buttons. The fix must not add inputs.

## Constraints

- Must play correctly at both 30 and 60 FPS (`project.md`).
- Do not change `design/combat.md`. The intended behavior (invulnerable for the full dash) is already specified.
- Small team: prefer reusing existing systems.
- QA will verify independently from the criteria and the build, not from the engineer's explanation.

## Open questions

- None blocking. For the engineer to decide: whether the "flag drops after a dash" observation (criterion 3) is part of this fix. It follows from the quoted rule "invulnerability until 0.8 s after the hit". If the engineer thinks the design intends otherwise, hand it to `game-designer` rather than deciding it.

## Expected output

A fix in `repo/` that meets all acceptance criteria, with a regression test. Hand back to `qa` for verification (`verify-change`). Include the exact scripts that QA should re-run: script A at 30 and 60 FPS, and script B.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, design/combat.md, manual.md, repo/README.md, repo/game.py, repo/play.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-dash-damage/01-studio-to-qa.md
