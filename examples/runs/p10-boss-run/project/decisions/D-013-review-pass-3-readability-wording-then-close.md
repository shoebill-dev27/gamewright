---
kind: decision
id: D-013
status: accepted
decided_by: game-director
goal: G-001
date: 2026-10-17
supersedes: none
---
# D-013: Review pass 3 — goal not met by one clause; one wording-only Design/Build/Verify round for shot-hit source and late-swipe explanation, then Close; no Owner escalation

## Decision

1. G-001 is **not met** on the current build, because the "player can tell why" half of the success condition has two confirmed holes: a shot hit names no source (A), and a late swipe gives no explanation (B). The variety half is met.
2. The D-009 Owner-escalation condition is **not triggered**. The melee reads as distinct fights (runner, standard grub, brute). No Owner decision is needed.
3. Route one **wording-only** Design step for A and B, then Build, then QA Verify at 30 and 60 FPS. Limits:
   - no rule, number, timing, cap, cue or input change;
   - the substrings `takes aim`, `rears back` and `YOU ARE HIT by` stay;
   - no information beyond what the existing cue and lane lines already show.
4. **Pre-commitment.** If QA passes the wording with the suite green and bots unchanged, Review pass 4 is a paper check of QA's result and the verdict is goal-met. No further playtest, Diagnose or room 3 timed run is required first. If QA fails, the failing item goes back to Design once.
5. **Known gaps accepted:** R3-8 at 60 FPS, the room 3 pure 1-tile sidestep, and the 30 FPS cancel and recovery swipe in room 3. The practice-room evidence covers the same rules, and room 3 changed only in content (D-012). Diagnose stays barred by the loop limit.
6. **Not acted on in this Goal:** grub sameness across rooms, dodge-heavy spitter rooms, and the room 5 brute tail. They become proposed Goals at Close only if a live player reports them. The first lever for the brute tail stays D-004 Option 3.

## Rationale

- Rooms 4–5, the runner/brute distinction and the room 3 second ask meet the variety half of the success condition across passes 2 and 3.
- The two holes sit in the Goal's own words and in the "readable threats" pillar. QA 90 confirmed the build is correct and the text view hides the cause, so the fix is wording and cheap.
- Closing with a confirmed clarity failure would ignore the success condition. Opening a larger round would grow the Goal. A bounded round with a pre-committed verdict does neither.
- The unshown items concern rules already verified in the practice room, and QA's bounded tries are used up.

## Alternatives considered

- **Declare goal-met now and move A and B to a new Goal:** the holes are in the success condition's wording and take one cheap step to close, so splitting them out would only delay the Goal. Rejected.
- **Escalate to the Owner:** no trigger fires. Rejected.
- **Third Diagnose or a new live playtest first:** no new cause, and evidence on the wording needs only QA. Rejected.
- **Add a swipe grace period or change cancel rules for B:** a rule change with no defect behind it (D-011). Rejected.
- **Change the shot (for example, keep it visible after contact) for A:** touches D-005. Rejected; wording first.
- **Act on grub sameness, spitter dodging or the brute tail now:** weak, partly script-caused evidence, and it would grow the Goal. Rejected.

## Revisit when

- QA fails the wording, or a human still cannot tell what hit them: reopen the text-view clarity question once, then consider the graphical build as the real fix.
- A live player reports the room 5 brute standoff, grub sameness or flat spitter rooms: propose a Goal (Option 3 first for the brute).
- A graphical build exists: re-judge hit-source and late-swipe readability against the visual criteria.
- The wording would make the text view easier than the graphical build is meant to be: take that back to Design.
