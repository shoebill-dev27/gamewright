---
kind: handoff
goal: G-001
seq: 17
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 17: studio → gameplay-engineer — Add decision-time state to the bot log; align the walker rate test with criterion 16

## Task

Make two tooling and test changes, with no change to the simulation or to any bot decision:

1. Extend the `log on` output of `bots.py` so QA can compare a bot's decisions at 30 and 60 FPS from the same state.
2. Replace the walker 30/60 `expectedFailure` test in `repo/tests/test_game.py` with tests that match criterion 16 as now written in `design/combat.md`.

## Context

G-001 (combat monotony), build 0.5. The walker bot gives different results at 30 and 60 FPS in rooms 3–5. Criterion 16e says this is a build defect only if the same decision at the same game time (±1 frame) from the same state has a different outcome. QA reproduced the divergence (deterministic) and found no build defect, but cannot close 16e because `log on` prints action names and times only, with no positions. The designer ruled that the walker only has to meet criteria 13 and 14 at each rate, and that the dodger must agree across rates (16c). The old test still describes the walker difference as unexplained.

## Findings

Reproduction scripts (one per rate), run with `python3 bots.py {script}`:

```text
bots walker
rooms 1-5
fps 30        # second script: fps 60
log on
```

QA's baseline results, which must not change (hearts lost per room 1/2/3/4/5, ✓ cleared, ✗ not cleared):

| Rate | Walker | Dodger |
|---|---|---|
| 30 FPS | 3✗ 2✓ 0✓ 1✓ 3✗ (9 lost, 3/5 cleared) | 0 lost, 5/5 cleared; dashes in rooms 3/4/5: 8/7/11 (35 total) |
| 60 FPS | 3✗ 2✓ 2✓ 2✓ 2✓ (11 lost, 4/5 cleared) | 0 lost, 5/5 cleared; dashes in rooms 3/4/5: 10/8/14 (48 total) |

The camper differs between rates too (room 2 cleared at 30, not at 60). Record its output before and after your change.

What QA needs to see (hypotheses, not facts, which the new log should confirm or refute):
- Room 1, ~0.30 s: the 60 FPS walker swings and the 30 FPS walker walks. The walker swings when the nearest grub is closer than 2.5 tiles; the distance may land exactly on 2.5 and fall on opposite sides at the two rates through floating-point accumulation.
- Room 3, 2.10–2.25 s: a shot hits the player at 60 FPS but not at 30 FPS. QA cannot tell whether this is a different decision, or a contact-edge graze that is caught at one rate and missed at the other.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- Designer's rulings (handoff 14), already in `design/combat.md`: criteria 14 and 16 as written there, and the five confirmed spec defaults. No build or bot change follows from them.
- Studio: Decide and Plan are skipped for this Goal.

## Constraints

- **No behavior change.** Do not touch simulation code, bot decision logic, thresholds (including the 2.5 tile threshold and any tie handling), the 0.15 s decision grid, or player-visible output. Changing the walker's numbers would invalidate the criterion 13/14 results the designer ruled on.
- With `log` off, bot output must stay byte-identical to the current output.
- No new input; the build must still play correctly at 30 and 60 FPS.
- Stop and hand back to `studio` (outcome `question`) if meeting the criteria below would need a change to the simulation or a bot decision, or if the existing walker test cannot be replaced without ambiguity. Do not decide spec questions.

## Open questions

None for you. Whether a contact-edge graze that depends on the frame rate is acceptable is the game-designer's decision and is decided only after QA reads your log. If your log makes such a case visible, say so in your notes as an observation, without judging it.

## Expected output

Acceptance criteria:

1. **Decision lines.** With `log on`, each bot decision line keeps its current content and adds: the frame number, the grid decision time and the actual frame time; player position (x, y); hearts; whether the player is stunned (and remaining stun); the nearest enemy's kind, position and distance, where the distance is the exact value the bot compared against its threshold, printed to at least 6 decimals; and the position and velocity of every shot in flight.
2. **Skipped decisions.** When a grid decision is skipped (for example while the player is stunned), a log line says so with the time and the reason.
3. **Heart-loss lines.** Each heart lost produces a line with the time, the frame, the source (grub or shot), the player position and the source's position.
4. **Same results.** For `bots walker`, `bots dodger` and `bots camper`, `rooms 1-5`, at `fps 30` and `fps 60`: hearts lost per room, cleared rooms, action counts and the logged action names and times are identical to the output before your change (the table above plus your recorded camper output).
5. **Tests.** `python3 -m unittest discover -s tests` passes. The walker `expectedFailure` test is replaced by tests of what criterion 16 now requires, expressed with the existing bots and deterministic: the dodger agrees across rates (same cleared set, hearts lost per room within 1), and the walker meets criteria 13 and 14 at each rate separately. Leave the other tests as they are.

Write your build notes as a handoff addressed to `studio` (not to qa). Include: files changed; the run_tests result; before and after output for criterion 4 (walker, dodger, camper, both rates); a sample of the new decision lines for room 1 at 0.15–0.50 s and room 3 at 1.80–2.60 s at both rates. Your Sender assessment is stripped before QA sees the Handoff.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat.md (criteria 13–16), repo/bots.py, repo/game.py, repo/play.py, repo/tests/test_game.py, repo/README.md, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/16-qa-to-studio.md (also relevant: goals/G-001-combat-monotony/14-game-designer-to-studio.md)
