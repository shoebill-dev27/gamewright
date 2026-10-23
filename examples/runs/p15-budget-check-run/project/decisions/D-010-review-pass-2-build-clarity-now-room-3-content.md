---
kind: decision
id: D-010
status: accepted
decided_by: game-director
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-010: Review pass 2 — goal not met yet, no Owner escalation; build the variant message and manual text now; room 3 variety goes to Design

## Decision

1. G-001 is **not met** on build 0.6.1, with moderate confidence. The gap is narrow: room 3 offers a single ask and repeats for about 20 s, and the text-view messages for runner and brute read "a grub". Rooms 4–5 and the brute and spitter asks are varied and engaging in the variant-aware playtest (63).
2. The D-009 Owner-escalation condition is **not triggered**. The brute was told apart from the grub and runner. The slow room 2 brute loop is partly caused by the test scripts, so the D-004 "dodges without fighting" trigger is not confirmed. No Owner decision is needed; nothing touches D-001 or the pillars.
3. **Build now (Build 21):** the D-008 variant-named wind-up message, and the manual late-swipe wording from step 59. D-008 may be treated as accepted when Build 21 is routed. The playtest that needed a stable build is complete, so D-009 item 5's reason to wait has ended. The next playtest must state its build.
4. **Design (room content, inside D-001):** `game-designer` is asked for options to give room 3 a second kind of ask or to avoid the long single-spitter standoff, using existing enemies. It must keep criterion 11 and the aim-cue timing that room 3 teaches. It may combine this with the open room 3 in-flight question (66). Option 3 (a spitter in room 2) stays deferred.
5. No third Diagnose. After Build 21 and the Design answer, one more playtest (live or hand-timed if possible) feeds Review pass 3.

## Rationale

- The variant-aware playtest tested the differences the build was changed to create, and they were found: rooms 4–5 held attention, and the brute and spitters each asked something new. That removes the main reason to suspect the melee redesign failed.
- Variety outside rooms 4–5 is thin, but adding a second ask to one room is cheap content, inside D-001, and does not need the Owner.
- "The player can tell why" is half the success condition and the tester hit the unclear message directly. The fix reuses the message system and keeps `rears back`, so scripts keep working.
- All evidence is scripted. A human check is the proportionate next evidence, not more analysis.

## Alternatives considered

- **Declare the goal met:** room 3 and the message clarity gap are real, and no human has played. Rejected.
- **Escalate to the Owner now:** the condition in D-009 is not met and the cheaper content fix is untried. Rejected.
- **Take Option 3 (room 2 spitter) now:** the brute stall is not confirmed, and it would change room 2 without evidence. Rejected for now.
- **Third Diagnose:** no new cause. Rejected (loop limit).
- **Wait on the message change until after the room 3 change:** needless delay. Build 21 may carry the message and manual text alone.

## Revisit when

- The next playtest still shows the melee reading as one fight, or the brute only kited: apply D-009 item 4 (Owner escalation).
- A human still reports a flat room 3 after the Design change: consider a larger room change or Option 3.
- The new message still leaves the player unable to tell what hit them: reopen the text-view clarity question.
- A graphical build exists: re-judge variant readability.
