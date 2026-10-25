---
kind: handoff
goal: G-001
seq: 12
from: gameplay-engineer
to: qa
stage: Verify
outcome: partial
---
# 12: gameplay-engineer → qa — reach-mark Build finished in code; unlit-brazier/Gloom rule added; verify checks 14 and 29 and regress the rest

## Task

Verify the Build against the amended spec (sections 3, 4, 9) and checks 13, 14, 26 (and 29 by eye). Run `node --test` first. Checks 27-30 need a human opening `repo/index.html`; no text run can show them.

## Context

G-001. Handoff 11 asked for: old check-14 assertions replaced by the strict form, `--trace` fields moved to the D-002 meaning, the unlit-brazier/Gloom ruling confirmed or implemented, hand-made tests, and real runs. The code and tests are written. I did not run anything with `@run` myself. The runtime's Build check (below) is the only execution of this change, and it covers `node --test` only. The play.js and `--trace` runs and the bot checks 14 and 26 are written as tests inside `node --test`, so they appear in that output and not as separate runs. Hence `partial`.

## Findings

What changed:
- `repo/src/view.js`: confirmed that the old code gave an unlit brazier no reach mark at all (an early return), so the Gloom was never evaluated there. Changed it. For an unlit brazier neighbour tile the hypothetical uses E = min(100, E+60) minus that tile's drain (the rekindle happens before dimming). Stunnable creatures (everything except the Gloom) are skipped there, and the Gloom is still evaluated through `planAction` and `hurtsAt`. Lit braziers, floor tiles and the stairs are unchanged (stairs never marked).
- `repo/src/script.js` (`stepLogged`): damage log entries are now `{src, type, amount, visibleBefore, markedBefore, case}`. `case` is `reach` if the player moved onto a neighbour tile, else `threat`. `markedBefore` is true only if the creature carried the threat mark (threat) or the reach mark on the tile where the player ended the turn (reach) in the previous view. `steppedAdjacent` and `radiusChanged` are removed.
- `repo/src/textview.js`: trace damage line now prints `case=... markedBefore=...`.
- `repo/tests/bots.test.js`: the old check-14 test (which accepted `steppedAdjacent` and `radiusChanged` as excuses) and the old sampled-states test are replaced by one strict test. Any damage not shown and marked per `case` fails it. Check 26 test unchanged. The strict check-14 and sampled-states tests in `tests/reach.test.js` stay. Not edited: `creatures.test.js`, `rules.test.js`, `bot.js`.
- `repo/tests/g001-final.test.js` (new): a gathered Gloom beside an arena brazier (reach mark `G`, step in, hp 12→8); an ungathered Gloom there (no mark, no damage); a crouching hound at distance 2, step toward it (threat and reach mark beforehand, bitten for 3); flare timing with a moth (acts on the third turn counting the lighting turn as the first); trace fields via `stepLogged` and `renderTrace`; `node play.js -` and `node play.js --trace -` run as child processes on `seed 42 / dd.`.
- `repo/manual.md`: flare wording clarified (reading 3, now marked ratified), reading 10 marked ratified, the unlit-brazier sentence reflects the Gloom rule, trace damage fields described.
- No creature behaviour, number, content or scope was changed. `STUN_TURNS` and the bite rule are untouched.

How to exercise:
- `node --test`, and read the diagnostics of the check-14 (strict) and check-26 tests in `bots.test.js`, and of `reach.test.js`.
- `node play.js script.txt` with a script such as `seed 1` plus moves; read the `Danger:` line before each step.
- `node play.js --trace script.txt`; damage lines show `case=` and `markedBefore=`.
- On floor 5, walk toward an arena brazier next to a gathering Gloom and read `Danger:`.
- Checks 27-30: a human opens `repo/index.html`.

Criteria addressed: 13 (timing test), 14 (strict, including hand-made unlit/lit brazier and Gloom cases), 26 (bot test), and 29 (reach marks, code only).

Known gaps:
1. I did not run `node --test` myself, nor any `play.js` script, `--trace` script or bot run outside the test file. The Build check below shows only the `node --test` outcome.
2. Blocked-line-of-sight neighbour case: no scenario written. QA should judge whether that case can occur and whether it is covered.
3. The random-walk check-14 test may rarely meet hounds or the Gloom; those are covered by hand-made scenarios.
4. Page appearance (checks 27-30) not seen.

## Decisions already made

- D-001: classic-script UMD modules.
- D-002: threat plus reach marks, after-dimming E, strict check 14. Handoff 10 rulings applied: flare reading A, hound bite at distance 1, lit brazier marked, unlit brazier marked by the Gloom only.

## Constraints

- Report only what was run. No creature behaviour, numbers, content or scope changes. The 30 checks and numbering are unchanged.

## Open questions

None for the Game Designer. A spec case I met was silent on nothing.

## Expected output

A verdict on checks 14, 13, 26 and 29 plus a regression pass on checks 1-26, with failures routed to `gameplay-engineer`. Checks 27-30 need a human at `index.html`; report them as not verifiable by text runs rather than passed. Run the scripts and `--trace` yourself (`node play.js {script}`), not only `node --test`. Address the result to `studio` (a Playtester step may follow and needs a fresh Handoff composed from permitted information only).

## Sender assessment

Confidence is moderate-high for the view.js change: `hypo` only gained a base-ember override, and the Gloom's plan does not depend on r. The risk is that the strict bot check-14 test may expose a case the old weaker assertions hid (for example a shade whose fear state differs between the hypothetical and the creature phase). If it fails, the failing entry names seed, turn and `case`. I have no execution evidence beyond what the runtime's Build check shows.

## Build check

The runtime ran `run_tests` (`node --test`) on the build exactly as this step wrote it: exit 0 (2.0 s).

```text
8 creature #4 moth
ℹ threat seed c14-15 command 16 creature #2 moth
ℹ reach  seed c14-15 command 76 creature #1 moth
ℹ reach  seed c14-16 command 17 creature #3 moth
ℹ threat seed c14-16 command 18 creature #3 moth
ℹ threat seed c14-16 command 32 creature #1 moth
ℹ threat seed c14-16 command 35 creature #1 moth
ℹ reach  seed c14-18 command 57 creature #1 moth
ℹ damage events: threat 12, reach 7
✔ sampled states: threat flags equal what the planner does with the ember after dimming (70.683791ms)
✔ check 1: a new run shows E=100, r=6, HP 12/12, floor 1/5 (6.702778ms)
✔ check 2: waiting costs 1 E; radius thresholds (2.443146ms)
✔ check 3: move, wait, fight and item use each cost exactly 1 E; refused actions cost 0 and no turn (1.24172ms)
✔ check 4: brazier at E=30 gives 89, at E=80 gives 99; a lit brazier gives nothing later (0.256691ms)
✔ check 5: E reaching 0 ends the run; creatures do not act (0.553231ms)
✔ check 6: messages at E 20, 10, 5 and when r drops (0.488671ms)
✔ check 7: remembered tiles stay; out-of-sight creatures are not listed (1.101622ms)
✔ check 8: oil +30 up to 100 then dim; salve +5 up to 12 (0.201078ms)
✔ check 19: HP 0 gives "You fell on floor N"; HP 0 with E 0 gives ember out (0.367933ms)
✔ check 20: after an end state further commands change nothing (0.32994ms)
✔ check 24: descending keeps E and HP apart from dimming, increments floor, places on < (1.233676ms)
✔ check 25: a full inventory leaves the item on the floor with a message; the move still costs a turn (0.265231ms)
✔ visibility: adjacent tiles and clear distance-2 straight tiles are always visible at r=2 (15.206861ms)
✔ visibility: walls block line of sight; the glow is circular (0.667209ms)
✔ check 9.1-9.9: the text frame shows every item of spec section 9 (1.767172ms)
✔ view and rules agree: marked threats come from the planner (adjacent moth is marked, distant one is not) (0.449317ms)
ℹ tests 49
ℹ suites 0
ℹ pass 49
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 1840.894907
```

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md, studio/skills/reproduce-defect.md
- Project: design/game-spec.md, design/acceptance-criteria.md, repo/manual.md, repo/play.js, repo/src/view.js, repo/src/script.js, repo/tests/g001-final.test.js, repo/tests/bots.test.js, repo/tests/reach.test.js; the build in repo/ (run commands in project.md)
- Decisions: decisions/D-001-classic-scripts-shared-rules.md, decisions/D-002-threat-and-reach-marks.md
- Previous handoff: none
