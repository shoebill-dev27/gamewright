---
kind: handoff
goal: G-001
seq: 6
from: game-designer
to: studio
stage: Build (gameplay-engineer applies the answer, fixes failing tests, rebuilds)
outcome: done
---
# 06: game-designer → studio — Night 3 first screen draws `~` under the starting aim (option a)

## Task

Route to `gameplay-engineer`: keep `DRAW_LIT_ON_FIRST_SCREEN = True` (option a), fix the 4 failing tests, and rebuild. Then route to `qa`.

## Context

Goal G-001, first playable of Lamplight Keeper. Handoff 05 asked whether the first screen of Night 3 (starting aim RIGHT) shows `~` on (3,4)-(3,6). §8 drew none, while §2, AC-3 and AC-1 conflicted with that drawing.

## Findings

**Decision (one sentence):** The first screen of every night draws `~` on the tiles lit by the starting aim, so Night 3 shows `~` on (3,4)-(3,6).

**Why:** Pillar 2 (readable ahead). The header aim and the drawn lit tiles must never disagree, and option (b) would create exactly that disagreement on the first screen. Option (a) also matches AC-3 and every later screen. It changes no ship movement and adds no mechanic.

**Amended sections of `design/first-playable.md`:**
- **§8 intro:** now says the drawings are first screens, with tiles lit by the starting aim drawn `~`. Nights 1 and 2 start UP and show none.
- **§8 Night 3 drawing:** row 3 is now `3 ...T~~~`. A note below it says no ship stands on those tiles at turn 0 and lit status is judged after the first command.
- **AC-1 final wording:** "Its first screen shows the 7×7 board exactly as in §8: coast row, ships, lighthouse at (3,3), row and column numbers, header, ship list and forecast line. The starting aim is as stated. The tiles lit by the starting aim are drawn `~` on the first screen, as AC-3 requires for every screen: Night 1 and Night 2 (UP) show no `~`, and Night 3 (RIGHT) shows `~` on (3,4)-(3,6). The header aim and the drawn lit tiles always agree."
- **§2 and AC-3:** unchanged. They were already correct and now agree with §8 and AC-1.

**Check for QA:** the first screen of Night 3 must read `3 ...T~~~` with header `Beam: RIGHT`. The build's output already matches this exactly (seen in the Build check). The first screens of Nights 1 and 2 have no `~`.

**Forecast order (not changed):** §6 gives the forecast line only as an example (`L -> LEFT, H -> UP, R -> RIGHT`). The spec does not fix the order, and AC-15 only requires the correct aim for each of `L`, `H`, `R`. The build prints `L, R, H`, and 4 tests expect `L, H, R`. Either order complies. The engineer may fix the tests to match the build, or change the build's order. I left §6 alone because it is outside this contradiction. If the studio wants one fixed order, that is a one-line spec change I can make.

**Not checked:** I ran nothing. I only compared the spec against the Build check output in handoff 04.

## Decisions already made

- D-001: three beam aims, lit ships slide along the beam row, a wreck loses the night at once, 10-turn limit. Not reopened.
- No new Decision record: this is a display clarification inside D-001, not a rule change.

## Constraints

- No mechanics change and no change to the behavior of the other nights.
- The two Review questions (mid-night arrivals, wrecks always losing the night) remain for `game-director`. They are still in §12.

## Open questions

- None blocking.
- For `game-director` at Review, unchanged: mid-night arrivals, and whether wrecks always lose the night.

## Expected output

`gameplay-engineer`:
- Confirms option (a) and removes the "provisional" status of the constant (or the constant itself).
- Makes the failing tests agree with the spec: forecast order as noted above, plus the other failures listed in the Build check.
- Reports a green `run_tests`.

Then the build goes to `qa` against AC-1..AC-15, with the Build handoff minus the Sender assessment.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: none
- Project: design/first-playable.md; repo/lamplight.py; repo/tests/test_game.py; repo/manual.md
- Decisions: decisions/D-001-beam-and-ship-rules.md
- Previous handoff: goals/G-001-first-playable/05-studio-to-game-designer.md
