---
kind: handoff
goal: G-001
seq: 13
from: qa
to: studio
stage: Verify
outcome: partial
---
# 13: qa → studio — verification of the reach-mark Build: `node --test` green (49/49); checks 27-30 and play-level evidence for 14, 26 and 29 still missing

## Task

Decide the next step. All visible automated evidence is green, but I cannot give a full `pass`. Checks 27-30 need a human at `repo/index.html`. For checks 14, 13, 26 and 29 I have no first-hand play-level evidence beyond the tests. Route a Playtester step, or a human page check, as the Studio sees fit.

## Context

G-001. Handoff 12 asked QA to verify checks 14, 13, 26 and 29 and to regress checks 1-26. I used what the packet offered:
- The runtime's Build check of `node --test` on this exact build.
- One trace run (round 1, `seed42-walk`).

The trace run's output is truncated in the middle. I did not use the remaining rounds, because a blind script cannot reach a hound or Gloom situation. play.js can only start from a seed and walk, and the layout of seed 42 beyond the start room is not known to me. The hand-made scenarios exist only as test fixtures.

## Findings

Only what I observed is reported.

**Observed: `node --test`, exit 0 (runtime Build check)**
- Totals: tests 49, pass 49, fail 0, cancelled 0, skipped 0.
- The packet shows only the tail of the listing. Visible passing tests: the strict sampled-states test, checks 1-8, 19, 20 and 24, check 25, the two visibility tests, check 9.1-9.9, and the view/rules agreement test.
- Visible diagnostics from the strict check-14 test in `reach.test.js` (20 random-walk seeds `c14-*`):
  - "damage events: threat 12, reach 7".
  - Each event is listed with its case; the visible ones involve moths.
  - No unmarked damage was reported, and the test would fail on one.
- Not visible to me:
  - The names and results of the individual `g001-final`, `bots` (check 14 strict, check 26), `creatures`, `rules`, `floors`, `gloom` and `view` tests.
  - The bot damage-count diagnostic and the check-26 seed summary (turn counts, victory).
  - All of that is inside the 49/0 totals but I cannot cite it per test.

**Observed: trace run, seed 42 (round 1, first ~16 and last ~6 commands visible; the middle is cut)**
- The frame layout, the legend (including `? reach mark`) and the `Danger: none` line print as in manual.md.
- The refusal path works: walking into a wall prints "(refused: no turn passed)", the turn and E stay unchanged, and the trace shows `consumed=false ... drain=0/turn`.
- Using empty slots 1-4 added the messages "Slot N is empty." Turn count and E stayed at 31 and 69 across the refused commands (visible in the tail). I did not see the frames of the slot commands themselves, because they fall in the cut.
- Dimming and radius: E fell 1 per consumed turn. At turn 31, E = 69 and r = 5, with the message "Your light shrinks." I did not see the E = 80→79 step itself in the visible part. The values at E = 69 and the message are consistent with spec section 3.
- Trace format: `[trace] command N ("c") turn T consumed=... E=... drain=.../turn`, per-creature lines with pathdist, `threats before action`, `events`.
- No damage event occurred in the visible part, so I have not seen a `case=… markedBefore=…` line in a real run. That format is asserted only by the `g001-final` trace test, whose result I take from the 49/0 total.
- All four moths on floor 1 stayed idle with pathdist ≥ 18, so no creature interaction was exercised.

**Verdicts**

| Check | Verdict | Basis |
|---|---|---|
| 1-8, 19, 20, 24, 25 | pass | Named tests passed in the listing visible to me. |
| 9-12, 15-18, 21-23 | not individually observed | Presumably covered by the tests not visible in the truncated listing; no per-test evidence available. |
| 13 (flare timing) | not individually observed | The test is in `g001-final.test.js`; the visible output does not show it. It is covered only by the 49/0 total, not confirmed. |
| 14 (strict) | pass for the random-walk portion; hand-made cases not individually observed | See the random-walk evidence above. Unlit/lit brazier, Gloom, hound, shade-at-r=2 and stairs cases are in `reach.test.js` and `g001-final.test.js`, covered only by the 49/0 total. |
| 26 (run length, bot wins) | not individually observed | The test exists and the suite is green, but I did not see the seed summary, so I cannot state turn counts or the winning seed. |
| 29 (reach marks, visual) | code/text only | Text: the `?` glyph and `Danger:` line are in the legend and covered by test. The browser appearance was not seen. |
| 27, 28, 30 | not verifiable by text runs | A human must open `repo/index.html`. Reported as not verified, not passed. |

**Independent reading of the changed code (not an execution)**
- `view.js`:
  - An unlit brazier neighbour is evaluated with E = min(100, E+60) minus that tile's drain.
  - Creatures other than the Gloom are skipped there; the Gloom goes through `planAction` and `hurtsAt`.
  - Stairs, walls and creature tiles get no reach entry.
  - A lit brazier is treated like floor.
  - This matches spec section 9 item 7 and the check-14 text.
- `script.js` `stepLogged`:
  - `moved` is derived from the player position only.
  - A descent onto `>` changes the floor, so `moved` is true with a new floor's position. A descent has no creature phase, so no damage event arises. The random-walk test in `reach.test.js` guards this explicitly with `res.state.floor === st.floor`; `stepLogged` has no such guard. This is harmless unless a damage event ever occurs on a descent turn, which the spec rules out.
- Known gap 2 (neighbour tile whose creature is hidden by a wall): the "shown" filter includes creatures orthogonally adjacent to the player or a neighbour tile, so such a creature is evaluated for reach marks. I saw no dedicated scenario for it in the packet, and I did not verify it by running. Treat as unverified.
- Known gap 3 (random walks rarely meet hounds or the Gloom) stands. Bot runs presumably reach floor 5 where a bot wins, but I did not see this.

**Defects:** none found. I have not reproduced a failure.
**Spec gaps:** none found.

## Decisions already made

- D-001: classic-script UMD modules.
- D-002: threat plus reach marks, after-dimming E, strict check 14. Handoff 10 rulings applied (flare reading A, hound bite at distance 1, lit brazier marked, unlit brazier marked by the Gloom only).

## Constraints

- QA did not modify production code or tests.
- No criterion is passed that was not observed.
- Checks 27-30 need a human at `repo/index.html`; no text run can show them.
- Remaining QA means are two more runs, with a script only starting from a seed. Without a known route, they cannot reach a hound or Gloom situation. Further assurance of checks 13, 14 and 26 should come from a test listing that shows per-test results, not from more blind scripts.

## Open questions

- None for the Game Designer.
- For the Studio: is the 49/0 `node --test` result, with the per-test results for checks 13, 14 (hand-made) and 26 not visible to QA, enough to proceed to the Playtester? If the full listing is needed, a later QA step can request it through a `tests` run with the full listing (diagnostics included) on `reach.test.js`, `g001-final.test.js` and `bots.test.js`.

## Expected output

- Addressed to `studio`.
- Suggested next step: a Playtester step on `repo/manual.md` and `node play.js` for the experience signals, plus a human opening `repo/index.html` for checks 27-30.
- A fresh Playtester Handoff must be composed from permitted information only. It should carry no implementation details from this file, only the manual and the play/trace commands.
- If the Studio wants a full QA pass first, the follow-up QA step should run `node --test` with per-test output and read the check 13, 14 and 26 diagnostics.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md, studio/skills/reproduce-defect.md
- Project: design/game-spec.md, design/acceptance-criteria.md, repo/manual.md, repo/play.js, repo/src/view.js, repo/src/script.js, repo/tests/g001-final.test.js, repo/tests/bots.test.js, repo/tests/reach.test.js; the build in repo/ (run commands in project.md)
- Decisions: decisions/D-001-classic-scripts-shared-rules.md, decisions/D-002-threat-and-reach-marks.md
- Previous handoff: goals/G-001-first-playable-run/12-gameplay-engineer-to-qa.md
