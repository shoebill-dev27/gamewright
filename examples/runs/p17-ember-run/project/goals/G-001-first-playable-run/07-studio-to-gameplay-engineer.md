---
kind: handoff
goal: G-001
seq: 7
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 07: studio → gameplay-engineer — apply the check-14 amendment (reach marks, D-002) and finish the build

## Task

Change `repo/` so that it meets the amended spec section 9.7 and checks 14 and 29 (reach marks, D-002). Then run the tests and scripts and report what you saw.

## Context

G-001: the Owner wants the concept playable from start to finish in the browser. Your first pass (handoff 05) wrote the whole build. Its outcome was `partial`, so the rest of the work comes back to you. The runtime's Build check of that pass: `node --test` exit 0, 34 tests, 0 failed. Nothing else was executed then: bot checks (14, 26), generator success rates, `--trace` output and the page.

While you built, the Game Designer answered the check-14 question (handoff 06): the threat-mark rule was right but the display was incomplete. The spec is amended. Handoff 05 is not sent to `qa`. Verify opens after this step and the parallel Design step 08 are both done.

## Findings

Changes required (from handoff 06, authoritative together with `design/game-spec.md` §9.7, §11 and `design/acceptance-criteria.md` checks 14 and 29):

1. Compute marks with E after this turn's dimming: current E minus 1, or minus 2 near the Gloom. At E = 20 a Wait beside a shade must already show a threat mark, because the creature phase sees r = 2.
2. Add reach marks to `view()` for the four neighbour tiles: for each tile the player could step onto, which visible creatures would hurt the player at their next action if the player ended the turn there. Use `planAction` with a hypothetical player position. Brazier tiles and stairs tiles get none (the flare stuns visible creatures; stairs skip the creature phase). Walls and creature-occupied tiles get none.
3. Always show a creature orthogonally adjacent to the player or to a neighbour tile, even if line of sight is blocked.
4. Show reach marks in both the text frame (for example `Danger: N (m), E (h)`) and the page, from the same `view` data. Define the final format in `manual.md`. The glyphs must be distinct from threat marks (check 29).
5. Replace the check-14 test assertion with the strict form: the damaging creature was visible in the previous output and carried a mark on the tile where the player ended the turn, and the test log names the case (threat or reach). Add the hand-made scenarios the check lists. Update the sampled-states test so marks equal what the planner does.

Still open, owned by the Game Designer (parallel step 08): the flare stun reading (does "next 2 turns" include the lighting turn's creature phase; built: yes) and the hound bite at lunge distance 1 (built: bites for 3). Keep the built readings, with `STUN_TURNS` and the bite rule easy to change. Do not change them yourself. If 08 changes them, the Studio will route that.

Unchanged from handoff 05: checks 27-30 need a human opening `index.html` from `file://`; check 26 is bot-based, so report its result and do not tune numbers or weaken generator rules.

## Decisions already made

- D-001: plain classic-script UMD modules, no ES modules.
- D-002: threat marks plus reach marks on the four neighbour tiles; marks use E after dimming; check 14 is strict.

## Constraints

- Do not change creature behaviour, numbers, content or scope to fit the marks; the marks follow the rules.
- Deterministic; no dependencies, no network; page has no rule logic.
- Report only what you ran or saw. State what you could not show (page appearance, anything unexecuted).

## Open questions

None for you (the two rule questions are with the Game Designer).

## Expected output

The changed build, tests and `manual.md`. Then a Handoff to `qa` (stage Verify) with the changes, how to exercise them, what you ran and its results, and the known gaps. If a test or script shows a rule gap you cannot settle, hand back with the failing check, seed and rule.

## Sender assessment

None (written by the Studio).

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/game-spec.md, design/acceptance-criteria.md, repo/manual.md, project.md#constraints
- Decisions: decisions/D-001-classic-scripts-shared-rules.md, decisions/D-002-threat-and-reach-marks.md
- Previous handoff: goals/G-001-first-playable-run/06-game-designer-to-studio.md
