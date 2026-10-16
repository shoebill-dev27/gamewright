---
kind: decision
id: D-014
status: accepted
decided_by: game-director
goal: G-001
date: 2026-10-17
supersedes: none
---
# D-014: Review pass 4 — G-001 is met on the text-view build; Close with proposed Goals and one Owner item; no Owner escalation

## Decision

1. G-001 is **met** on the current build (text view). Both halves of the success condition hold:
   - different situations call for noticeably different play (met since passes 2–3);
   - the player can tell why. A damaging shot names the side it came from, and a swipe that was too late to stop a lunge says so (QA 98 and 104).
2. This is a paper check under D-013 item 4: wording passed QA, the suite is green, bots and `bots.py` are unchanged, and no rule, number, timing, cap, cue or input changed.
3. The known gaps are **accepted**: bots not re-run in 104, other W1 directions and 30 FPS only in the suite, W2–W4, W6 and W8 not fully re-run, and the room 3 items from D-013 item 5. They concern text paths that do not depend on frame rate.
4. G-001 is closed with these limits. "Met" is judged on scripted and QA-traced evidence. It is not a live-player confirmation.
5. No Owner escalation. The Owner is shown one item: the stray last line of D-007, which no step may remove.
6. **Proposed Goals (not part of G-001):**
   - visual readability on a graphical build (V1–V12);
   - a live-player confirmation of the new hit-source and late-swipe wording, which can be the first step of the visual Goal;
   - grub sameness, dodge-heavy spitter rooms and the room 5 brute tail, each opened only if a live player reports it (first lever for the brute: D-004 Option 3).
7. The shot hit-source and late-swipe wording is the current text-view standard. A change to it needs Design and must keep the prefixes `YOU ARE HIT by`, `rears back` and `takes aim`, and must not add distance, timing or spitter identity (the text view must not become easier than the graphical build).

## Rationale

- The two holes named in D-013 were in the Goal's own words. QA 98 showed the new text at both frame rates, with ordering and prefixes right. QA 104 closed the only failure (a stray manual marker).
- The change touched no gameplay, so the variety half is not put at risk by this round.
- Another QA round or playtest inside G-001 would grow the Goal. The unshown items are covered by the suite and by the frame-rate-independent way the text is built.
- Honest labelling matters. A live player may still find the build flat or the wording thin, and that belongs in a new Goal with its own evidence.

## Alternatives considered

- **Goal-not-met until a live player confirms:** the success condition asks that the player can tell why, which the text now states. A live session is new evidence for a new Goal, and D-013 pre-committed to closing. Rejected.
- **Another full QA round for the unshown items:** the cause of any miss is already covered by the suite, and the bounded tries were used (D-013 item 5). Rejected.
- **Escalate to the Owner:** no trigger fires. Rejected.
- **Declare partially-met:** no reason to stop short; the gap is closed. Rejected.

## Revisit when

- A live player still cannot tell which side a shot came from, or why a swipe did not cancel a lunge: reopen the text-view clarity question through a new Goal.
- A graphical build exists: re-judge hit-source and late-swipe readability against V1–V12 (D-009, D-011, D-013).
- A live player reports grub sameness, flat spitter rooms or the room 5 brute standoff: open the matching Goal.
- The Owner edits or removes the last line of D-007: nothing here depends on it, but record the change.
