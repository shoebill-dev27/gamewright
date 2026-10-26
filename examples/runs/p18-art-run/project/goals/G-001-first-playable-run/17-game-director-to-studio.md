---
kind: handoff
goal: G-001
seq: 17
from: game-director
to: studio
stage: Route
outcome: goal-not-met
---
# 17: game-director → studio — Review of G-001: intent only partly met, with the missing evidence named; close the Goal and propose four follow-up Goals

## Task

Close G-001 using the verdict below. Put the "achieved / not achieved" wording from Findings into the Outcome, in Japanese per `owner_language`. Present the proposed Goals and the Owner items to the Owner.

## Context

The Owner asked for a version that can be played from start to finish in the browser. Design (30 checks), Plan, Build, Verify and one Play round are done. The budget is spent except for this Review and the closing Route. I compared the evidence with the success condition in `goal.md`, not with the plan.

## Findings

### Verdict

`goal-not-met`, read as **partly met**. Nothing found contradicts the intent. Several parts of the success condition have no evidence at all, and the key one (a person playing a whole run in the browser) is one of them. I do not declare success because the plan was executed. Stopping here is justified because the budget leaves no stage for more evidence. The missing evidence becomes proposed Goals.

### Success condition against evidence

| Part of the success condition | Status | Basis |
|---|---|---|
| Rules, five floors, seeds, ember, creatures and the Gloom are built and consistent | Likely, verified only by automated tests | `node --test` 49/49 (13). QA saw per-test results for only some checks. |
| `repo/index.html` opens from the file system and is played with keyboard or mouse (checks 27-30) | **Not verified.** | No executor can see the page. The Art Director review was skipped. Only the Owner or a human can check. |
| One whole run from floor 1 to an end state | **Not observed by a player.** | Play reached only floor 1, 16 turns, seed 42. A bot is said to win in check 26, but QA did not see the result. |
| Text means (`play.js`, `--trace`, `manual.md`) | Partly observed | Refused moves, frame layout and the trace format work as the manual says (13, 15). |
| Pillar 1, readable threats | Partly observed, for the moth only | The `?` reach mark, the `Danger:` line and the `!` THREAT line were accurate (15). Check 14 passed on 20 random-walk seeds (threat 12, reach 7 events). Hounds, shades, the Gloom and the hand-made cases are covered only inside the 49/0 total. |
| Pillar 2, light as the resource | **Not observed** | Ember fell 1 per turn. No brazier, item or ember choice was met, so whether the trade-off is felt is unknown. |
| Pillar 3, a 15-30 minute run, seeded variety | **Not observed by a player** | Determinism and layout checks are in the tests. Run length, and whether a new seed feels different, is unobserved. Balance, which Design left open, is unreported. |

### Achieved

- A build exists with all the rules of the spec, shared by the page and the text player (D-001), and an automated suite that is green.
- Threats are marked and reach is marked (D-002), and this works in the one situation a player has seen.
- The team-side means ship and behave as documented.

### Not achieved or unknown

- Any evidence that the browser page works and looks right (checks 27-30).
- Any player-side evidence of floors 2-5, hounds, shades, the Gloom, braziers, items, winning, dying and run length.
- Balance, and whether the ember trade-off feels real.
- QA could not see per-test results for checks 13, 14 (hand-made scenarios) and 26.

### The repeated messages

I checked the design before calling this a defect. Spec section 9 item 8 shows "the last 5 messages", and the manual says "the last five messages … are always printed". So the old arrival line and the moth fight lines stayed in later frames because they were within the last five. That is **intended behavior, not a rule defect**. It is still a legibility weakness that a real player reported (low to medium impact): nothing separates what just happened from what is old. A fix that marks messages from the current turn does not change the spec's rule. I propose it as a small Goal.

### Decisions to revisit

- D-001: the revisit condition (a server or build step allowed) has not occurred.
- D-002: the revisit condition (reach marks cluttering or ignored) has not been reached. The only evidence is one accurate moth case, so it is neither confirmed nor contradicted. Keep the Decision.

No Decision was made in this step, and no Owner escalation trigger fires. The vision and pillars are unchanged.

### Proposed Goals, in order

1. **Browser check of `repo/index.html` (checks 27-30), needs the Owner.** The Owner request was specifically a browser version, and no one has seen the page. It is first because it carries the highest risk and costs the least. Expected result: a short note from the Owner on what works and what looks wrong. If defects turn up, the Studio opens a fix Goal.
2. **QA full-listing verification.** Run `node --test` with per-test output, including diagnostics, on `reach.test.js`, `g001-final.test.js` and `bots.test.js`. This confirms checks 13, 14 (hand-made) and 26, including the bot's turn counts and winning seed. It is small, and it gives the run length figure that pillar 3 needs.
3. **Broad playtest and balance.** Several seeds, floors 2-5, reaching braziers and items, meeting shades and hounds, the Gloom fight, a win and a loss, and run length. It should answer the open questions on the ember trade-off (pillar 2), run length and variety (pillar 3), and whether the numbers are too easy or too hard. Design findings from it go to `game-designer`. Ideally a person does it in the browser, which would also cover parts of Goal 1.
4. **Message legibility.** Mark or separate the messages from the current turn in the text frame and the page, within the existing "last 5" rule. Do it after Goal 3 if Goal 3 shows more presentation issues, so they can be handled together.

### Items that need the Owner

- Open `repo/index.html` and check items 27-30 (grid, ember bar, keys and mouse, brighter visible tiles, distinct marks, the three end screens, starting a new run). Nothing else can replace this.
- Say whether Goals 2-4 are wanted and in what order.

### Wording for the Studio's Outcome

A build with all five floors, the ember, the three creature types, the Gloom and the seeded runs exists, and its automated tests pass (49/49). The text player and the manual work. The browser page has not been seen by anyone, and no one has played a whole run, so the Owner's request is not confirmed as met. The next steps are the Owner's page check, a full test listing, a broad playtest with balance, and a message-log fix.

## Decisions already made

- D-001: shared code is classic-script modules (UMD style). Not changed.
- D-002: threat marks plus reach marks. Not changed.

## Constraints

- The vision, the pillars and the Owner-made Decisions are untouched.
- No new stages in this Goal. The follow-ups are proposals for the Owner.
- Nothing is claimed as verified that no executor observed.

## Open questions

- For the Owner: does the page work (checks 27-30), and which proposed Goals do they want next, in what order?

## Expected output

The Studio's Route closes G-001 with the Outcome above (in Japanese), records the four proposed Goals and the Owner items in `project.md` Current state, and presents them to the Owner. No further handoff is needed from the Game Director.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/review-outcome.md
- Project: project.md (Current state), goals/G-001-first-playable-run/goal.md
- Decisions: decisions/D-001-classic-scripts-shared-rules.md, decisions/D-002-threat-and-reach-marks.md
- Previous handoff: goals/G-001-first-playable-run/16-studio-to-game-director.md
