---
kind: decision
id: D-012
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-012: Room 3 gets one standard grub at (15,0) and its second spitter moves to (10,6); cap and cue rule unchanged

## Decision

1. Room 3 contents become: spitters at (2,1), (10,6), (2,7) in that order, plus one standard grub at (15,0). Nothing else in room 3 or elsewhere changes.
2. D-004 to D-007 and D-011 stand. The cap, the cue rule, the 0.8 s offset and the 1.8/2.6/3.4 s first-shot schedule are unchanged. The D-007 in-flight bound (up to 2 plus the living spitters) is unchanged.
3. The room 3 purpose line becomes "learn the aim cue first, then answer an aim line and a lunge lane together".
4. If the grub's first wind-up in a still-player trace is earlier than 4.0 s, the grub's position is retuned by the designer without a new spec step.
5. Spec and criteria: `design/combat-step72.md` (R3-1 to R3-10).

## Rationale

- Room 3 has a single ask. A grub gives a second, different ask using an existing enemy and existing systems, inside D-001.
- The grub walks in from the far corner, so its first lunge comes after the spitter cues are taught, with no new spawn system.
- It also pressures a player who stands off to dodge a lone spitter, and the spitters are now closer together, so the last one is a short walk away.
- It touches no spitter timing, so the cue rule and cap need no change and one room 3 change is built and verified once.

## Alternatives considered

- **A runner instead of the standard grub:** the 0.35 s warning on top of 0.6 s aim cues is too harsh for the teaching room, and runners are already in rooms 2 and 4. Not chosen.
- **A brute:** adds a long fight to a teaching room. Not chosen.
- **Replacing a spitter with a grub:** changes the verified 1.8/2.6/3.4 s schedule and the in-flight bound. Not chosen.
- **The 0.2 s cue gap in room 3 (D-007 fallback):** does not give a second ask, and changes a verified room. Not chosen.
- **Reinforcements, a lone-spitter speed-up, healing, or any new enemy:** new systems or enemies, outside this step. Not specified.

## Revisit when

- A playtest still shows a long single-spitter standoff or a flat room 3: try a runner in place of the grub, then a second grub, then a larger room change (D-010 revisit).
- A playtest shows the grub overloads the room while the cue is being taught: move the grub later.
- The bots measured on the Build leave criterion 13 or 15 outside its limits for a reason that is design, not bot policy.
- Any change to the cap, the spitter interval or the room 3 schedule (also a D-007 reopen).
