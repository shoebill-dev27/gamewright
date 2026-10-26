---
kind: handoff
goal: G-001
seq: 11
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 11: studio → gameplay-engineer — finish the reach-mark Build: old tests and trace fields, Gloom on unlit braziers, run everything

## Task

Continue the Build (handoff 09 was `partial`; nothing is missing, so the same Role finishes it). You can now see the files the earlier pass could not (see Load). Bring the build into line with the amended spec and D-002, run it, and hand the result to `qa`.

## Context

G-001, first complete playable five-floor run. Reach marks (D-002) are written (09) and the runtime's check passed `node --test` (43 tests, exit 0), but that was the only thing run. The Game Designer has ruled on the open questions (handoff 10, in Load). Budget is tight (10 of 19 used before this Route), so do the whole list in one pass.

## Findings

From 09 (Known gaps): old check-14 assertion and old sampled-states test in `tests/bots.test.js`, `tests/creatures.test.js`, `tests/rules.test.js` or `tests/bot.js` may still use the old rule; `play.js --trace` fields `markedBefore`/`steppedAdjacent`/`radiusChanged` likely keep the old meaning; nothing but `node --test` was executed; no scenario for a creature listed only through a neighbour tile with blocked line of sight.

From 10 (Game Designer rulings, spec and checks amended in place):
- Flare stun: reading A (built) is ratified. The lighting turn's own creature phase is the first skipped action, the next turn the second. The manual may be reworded for clarity.
- Hound bite at lunge distance 1: built reading is ratified. Only a blocked lunge (wall or creature stops the hound before it ends adjacent) means no damage.
- Lit brazier gets reach marks like a floor tile: ratified (resolves 09 gap 4).
- NEW, to confirm in code: an unlit brazier tile gets no reach mark from creatures a flare stuns, but it does get a reach mark from the Gloom if the Gloom would hurt the player there at its next action (the Gloom is not stunned by flares). If the code shows no reach mark at all on unlit braziers, change it: skip stunnable creatures in unlit-brazier hypotheticals, still evaluate the Gloom.

## Decisions already made

- D-001: classic-script UMD modules.
- D-002: threat marks plus reach marks, after-dimming E, strict check 14.

## Constraints

- No creature behaviour, numbers, content or scope changes beyond the rulings above. The 30 checks and numbering are unchanged.
- If a spec case is ambiguous or contradictory, stop and hand back `question`; do not decide.
- Report only what you ran. Keep the strict check-14 test; remove or replace any older, weaker assertion of it rather than leaving two rules.

## Open questions

None for the Owner. Return a `question` only if the spec is silent on a case you meet.

## Expected output

1. Old check-14 assertion and sampled-states tests replaced by the strict form; `play.js --trace` fields updated to the D-002 meaning (document in `repo/manual.md` if trace fields are described there).
2. Unlit-brazier/Gloom rule implemented or confirmed, with hand-made tests: a gathered Gloom beside an arena brazier; a hound at distance 1 after a step toward it (bite, marked beforehand); flare timing (acts on the third turn counting the lighting turn as the first); optionally the blocked-line-of-sight neighbour case.
3. Manual flare wording clarified if needed.
4. Actually run with `@run`: `node --test`, a `node play.js` script, a `--trace` script, and the bots (checks 14 and 26). Fix failures, and put the real output in the handoff.
5. Write the outgoing handoff to `qa` (stage Verify): what changed, how to exercise it (including that checks 27-30 need a human opening `index.html`), remaining gaps. `qa` does not receive your Sender assessment.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/game-spec.md, design/acceptance-criteria.md, repo/manual.md, repo/play.js, repo/src/view.js, repo/src/game.js, repo/src/textview.js, repo/src/page.js, repo/tests/bots.test.js, repo/tests/creatures.test.js, repo/tests/rules.test.js, repo/tests/bot.js, repo/tests/reach.test.js, repo/tests/helpers.js, goals/G-001-first-playable-run/10-game-designer-to-studio.md
- Decisions: decisions/D-001-classic-scripts-shared-rules.md, decisions/D-002-threat-and-reach-marks.md
- Previous handoff: goals/G-001-first-playable-run/09-gameplay-engineer-to-qa.md
