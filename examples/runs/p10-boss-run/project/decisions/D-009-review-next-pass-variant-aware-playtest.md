---
kind: decision
id: D-009
status: accepted
decided_by: game-director
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-009: After build 0.6.1 the next pass is a variant-aware playtest, not a third Diagnose; no Owner escalation yet

## Decision

1. G-001 is **not met** on build 0.6.1 (handoff 60). The "rooms feel alike" report in playtest 53 is not accepted as a settled design finding, because the scripts used one answer for every lunger and one run had no brute rule at all.
2. The next pass is a fresh playtest of the unchanged build 0.6.1. The player writes separate rules per enemy mark, plays rooms 1–5 including a slow run, and keeps the output short enough not to be truncated. The brief does not describe the design. No third Diagnose is run on the existing scripted evidence.
3. No direction change now. D-001, the pillars, D-004 to D-007 stand. Option 3 (a spitter in room 2) stays deferred but is the first lever if the stall is confirmed.
4. **Owner escalation condition.** If the variant-aware playtest still reports that the melee enemies ask for one answer (runner, standard grub and brute not told apart in play, or the brute only kited), the next Review does not send the Goal to Diagnose. The game-director prepares an Owner escalation (in Japanese) on adding a genuinely different melee behavior or enemy type, healing, or another change that touches D-001 or the pillars. Room content changes such as Option 3 do not need the Owner.
5. The manual wording on late swipes and a per-variant cue message (step 58) are accepted as in scope, as "the player can tell why". Their detail is the designer's. The playtested build must be stated, and a message change should not be mixed into the same pass without saying so.

## Rationale

- A third Diagnose on the same scripted evidence would repeat 04 and 31 without new information. The loop limit exists for this.
- The cheapest explanation that fits the evidence is that the test did not exercise the intended differences: uniform rules per cue, no brute rule in room 2 aggressive, and a "move away" rule that produced the 10 s stall. That has to be ruled out before changing direction.
- Escalating now would ask the Owner to approve new content on evidence that may be an artifact of the test method.
- The one run with a brute-specific choice (room 5 aggressive) was called interesting, and room 3 showed distinct styles. So the direction is plausible and not shown to have failed.

## Alternatives considered

- **Third Diagnose:** no new evidence; rejected.
- **Escalate now for a new enemy type or healing:** premature, and a cost to the Owner on weak evidence; rejected.
- **Declare goal met or partially-met and close:** the tester's report says rooms feel alike and cautious play stalls, and the deciding case is untested; rejected.
- **Take Option 3 (room 2 spitter) now:** would change room 2 before knowing whether the brute rule works for a human, and would make the next result impossible to attribute (this was the reason for deferring it in D-004); rejected for now.
- **Bundle the cue message change with the playtest build:** would confound the result; not chosen.

## Revisit when

- The variant-aware playtest report arrives (next Review).
- The tester still stalls against the brute or kites it with no reason to fight: take Option 3 or a room change.
- The tester cannot tell runner, standard grub and brute apart in play: apply item 4 (Owner escalation).
- Step 58 changes the cue message, so the playtested build changes: state the build and re-check that the comparison is fair.
- A graphical build exists: re-judge variant readability, since silhouettes replace the text message.
