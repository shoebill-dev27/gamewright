---
kind: decision
id: D-008
status: proposed
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-008: Text-view wind-up message names the variant (proposed build change); no swipe-timing rule change

## Decision

1. **Swipe timing stays a wording matter.** No rule or parameter change. The manual says that a swipe cancels a grub or runner only during its warning, that a grub starts rearing back about 2 tiles away (beyond the 1.5-tile reach), and that a swipe after the lunge began does not cancel it.
2. **Name the variant in the message** (proposed, not built): `a grub rears back`, `a runner rears back`, `a brute rears back`. All keep the words `rears back`. Nothing else in the output changes. Details and acceptance criteria are in `design/combat-step59.md`.
3. **Routing advice:** not urgent, not part of Review 57. Build it with the next opened build and Verify it. `game-director` need not weigh in unless they think the change moves the Goal.

## Rationale

- The graphical build already tells variants apart before the cue (silhouette, size, cadence). The text view has only the message and the `cue:` line. Naming the variant gives the text-view player the same early information and costs no new pillar-breaking information.
- It does not conflict with the "one answer for melee enemies" diagnosis (S1, 04, 31). The answer to runner and standard grub is the same, and the variant name only says how long the warning is. The brute's different answer comes from the cancel flag (D-004), and its name makes that flag easier to learn.
- Compatibility: the substring `rears back` keeps existing reaction scripts working.
- Wording is enough for the swipe, because both reported hits were swipes after the lunge began with the target out of reach during the warning (QA 56). A grace window or larger reach would let a swipe cancel a started lunge, which weakens "step aside or dash" and is not backed by a defect.

## Alternatives considered

- **Keep one message for all variants** (current, `combat.md` step 35): the `cue:` line already names the variant. Not chosen because the playtester reacts to the message line, and a reaction-rule player has to parse the `cue:` line to tell the variant.
- **Put distance and time left in the message** (for example "a runner rears back, 0.35 s"): the numbers make the message long, repeat the `cue:` line, and risk making the text view easier than the graphical build. Not chosen.
- **A swipe grace period of about 0.1 s after the lunge starts, or a bigger reach during wind-up:** would turn the two "unfair" hits into cancels, but needs a rule change that QA did not find a defect for, and it weakens the sidestep/dash answer. Not chosen; reopen if a human playtest still reports unexplained late swipes after the manual is clear.

## Revisit when

- The next playtest still shows wasted dashes or "I could not tell what it was" after variant naming.
- A human still reports late swipes as unfair after the manual wording is in.
- A graphical build makes the text message irrelevant.
