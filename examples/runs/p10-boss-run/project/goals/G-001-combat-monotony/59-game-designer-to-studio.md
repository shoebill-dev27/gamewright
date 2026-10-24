---
kind: handoff
goal: G-001
seq: 59
from: game-designer
to: studio
stage: Design
outcome: done
---
# 59: game-designer → studio — Late-swipe wording specified (manual text enclosed); variant-named cue message proposed as a small optional build change

## Task

Report the result of the two small points from 58, and ask the Studio to apply the manual text below, because `repo/manual.md` was outside the paths I may write.

## Context

Goal G-001. QA (56) found no defect in the three "unfair" hit moments (53). The late swipes landed after the lunge began, with the grub out of reach (about 2 tiles) during the warning.

## Findings

### Point 1: wording is enough, no rule change

- Both reported swipes landed 0.10 s after the lunge began. A swipe with 0.05 s of wind-up left, in reach, did cancel (QA practice-room check). The rules work as specified, and the manual does not make the limit clear.
- A non-lethal swipe during wind-up cancels even a 2 HP grub. One swipe is enough.
- I do not propose a swipe-timing rule change (grace window, bigger reach). It would let a swipe cancel a lunge already under way and weaken "step aside or dash". Reasons in D-008.
- `design/combat.md` already has the rules, so I did not change it. The addendum is `design/combat-step59.md`.

**Manual text to apply in `repo/manual.md`.**

1. Replace the **A grub rears back** bullet in "Warnings" from "The line is fixed where you stood…" to its end with:

> The line is fixed where you stood when the grub began; step 1 tile to the side or dash to avoid the lunge. You can also stop a grub or runner with a swipe, but **only during its warning**: one swipe that hits it while it rears back is enough (even a grub that takes 2 swipes to kill) and it is staggered for 0.4 s. A grub starts rearing back about 2 tiles away, which is beyond your 1.5-tile swipe reach, so a swipe cannot stop it until you have stepped to within 1.5 tiles during the warning. A swipe that lands after the lunge has begun does not stop it, and the lunge still hits if you are in its path. The warning lasts 0.5 s for a grub, 0.35 s for a runner, 0.7 s for a brute. After a lunge the grub is harmless for a while: that is the time to swipe it. Only one grub rears back or lunges at a time.

2. In the "Being hit shows…" bullet, replace "A swipe that interrupts the warning of a grub or runner staggers it for 0.4 s; a brute is not interrupted." with:

> A swipe that hits a grub or runner during its warning (not after the lunge has begun) staggers it for 0.4 s; a brute is never interrupted.

No other manual line changes. Shown as written, the lines make no rule claim beyond `combat.md`.

### Point 2: name the variant in the message (proposed build change, not built)

- Proposal: `a grub rears back` (unchanged), `a runner rears back`, `a brute rears back`. All keep `rears back`, so existing `text "rears back"` rules still work. Nothing else in the output changes.
- Reason: the graphical build already tells variants apart before the cue, and the text view has only the message and the `cue:` line. This does not conflict with the S1 "one answer" diagnosis: the answer to runner and standard grub stays the same, and the brute's different answer comes from its cancel flag (D-004).
- It does not remove variety: the `cue:` line, the `~` line and all timing are untouched. It adds no distance or hit-point information.
- Part of the wasted dashes was the reaction script reacting to the message regardless of distance. The variant name may not fix that, so I only expect a small gain.
- **This is a build change** in `play.py` and tests. Acceptance criteria V-a to V-d are in `design/combat-step59.md`. Worth doing: low cost and low risk, but optional. I recommend bundling it into the next opened build and verifying it, and not opening a build or holding Review 57 for it. Routing (Build, Verify) is the Studio's call. The bots must not break (V-d).
- Recorded as D-008 (status `proposed`, because the build change is not yet decided).

## Decisions already made

D-001, D-004, D-005, D-002/D-003 unchanged. D-008 is new and `proposed`.

## Constraints

No rule or parameter changes. `design/combat.md` still says the message is "a grub rears back" for all variants. If the build change is taken, `design/combat-step59.md` governs that point and `combat.md` should be updated in the Verify step.

## Open questions

- Does the Studio want the message change built now or with the next build? (Studio.)
- For `game-director`, in Review 57: the playtester's complaints about these hits were explained by timing and reach, not by a missing rule. The lasting experience issue is still monotony (53, issue 1). Neither point here changes that. The brute's stall in room 2 and the rest of the S1/S4 follow-ups are not touched. If a human still reports late swipes as unfair after the manual change, reopen D-008 (the swipe grace period alternative).

## Expected output

Studio applies the manual text above to `repo/manual.md` (or routes it), decides whether to route the message change to Build and Verify, and passes the Review note to `game-director`.

## Sender assessment

Confidence is high on point 1 (documents and QA traces agree). On point 2 it is moderate: the change is cheap and consistent with the pillars, but its effect on the playtester's wasted dashes is unproven.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat-step59.md, design/combat.md, repo/manual.md
- Decisions: decisions/D-008-cue-message-names-variant-proposed.md, decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
- Previous handoff: goals/G-001-combat-monotony/58-studio-to-game-designer.md
