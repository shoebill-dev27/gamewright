---
kind: handoff
goal: G-001
seq: 2
from: playtester
to: game-designer
stage: Diagnose
outcome: done
---
# 02: playtester → game-designer — Playtest report on combat in the current build

## Task

Diagnose why combat in the current build is experienced as monotonous, using the playtest report and the Owner's original report below. Give causes and solution options in design terms, staying within D-001 and the vision pillars. This is a player-side observation report only; it contains no causes or fixes.

## Context

Goal G-001: the Owner said (verbatim): 「戦闘が単調なので改善したい」 ("Combat is monotonous and I want to improve it"). The success condition is that a player from the project's player profile finds combat varied and engaging rather than repetitive, without new input buttons (D-001), while keeping threats readable and playing correctly at 30 and 60 FPS.

The first playtest of the current prototype (build 0.3), focused on combat, is below. The Playtester did not see the Owner's wording.

The dash-damage behavior the Playtester saw is being checked separately by `qa` (handoff 03, running in parallel). It is not part of your Diagnose scope except where it affects your reading of "dash feels pointless". If QA's result arrives before you finish, the Studio will pass it on. Do not wait for it.

## Findings

### Method

There is no executable. I "played" by reading `sim/build-0.3.md` and following the player-observable description as a player from the profile would (action player, short intense runs, comfortable with dodging and spacing, dislikes combo memorization, gamepad). This is a described walkthrough, not live play, so I could not observe things like feel of controls, timing, animation, audio, or exact damage numbers. I only played the content the description covers (rooms 1–5 and the run as a whole).

### Session summary

I went through rooms 1–5 using the same approach almost every time: stand my ground, press attack, step aside for projectiles. It worked each time with little risk. By the later rooms I was repeating what I did in room 1.

### Moments in sequence

1. **Rooms 1–2 (Grubs).** Grubs crawl toward me. I stood still and pressed attack. Two swipes killed each one before it reached me. I only took damage when three arrived together. Felt: easy, no tension. I did not need to move.
2. **Room 3 (Spitters).** Their projectile is slow, and one step sideways avoided it. I walked up and swiped each twice. Felt: a small new action (the sidestep), but it was trivial. Not a real threat.
3. **Rooms 4–5 (mixed).** I backed into a corner, faced the Grubs, swiped, and stepped aside from projectiles. The same pattern worked again. Felt: nothing new. My attention dropped here.
4. **Dash.** I rarely needed it. I used it mostly to cross the room faster, not to fight. Felt: as if I had a tool I was never asked to use. For a player who likes dodging and spacing, this was a letdown.
5. **Whole run.** Every room ended the same way: hold position, swipe until empty. Minute 2 felt the same as minute 15. I wanted escalation, and none came.

### Issues and impact

- **Combat is the same in every room (high impact).** One approach (hold position, swipe) wins everywhere. Player quote: "I figured out the answer in room 1 and it never stopped being the answer."
- **Little pressure to move or dodge (high impact).** Standing in a corner is safe. Damage only came when three Grubs arrived at once. Spitters needed one step. As a player who wants intense runs, I did not feel intensity.
- **Dash feels pointless in combat (medium–high impact).** I only used it for travel. Player quote: "Why do I have a dash?"
- **No sense of progression within a run (medium–high impact).** Later rooms did not feel harder or different.
- **Enemy variety feels shallow (medium).** Spitters and Grubs mixed together did not change what I did.

### Positives

- Attacks are quick to kill: two swipes per enemy. This is clear and readable.
- Spitter projectiles are easy to read.
- Nothing felt unfair or confusing.

### Behavior that looks plainly broken

- **Dash after being hit:** occasionally, if I dash right after taking a hit, I take damage partway through the dash. As a player it looked like the dash did not protect me, or damage landed late. It was rare, and I could not tell what triggered it. This may be a defect. I am reporting only what I saw. (Routed to `qa` by the Studio, handoff 03.)
- No crashes or stuck states observed.

### Not observed

- Controller feel, hit feedback, sound, visuals, and enemy types beyond Grubs and Spitters.
- Anything past room 5, and the overall length of a run in real time.
- How the damage-during-dash case is triggered.

## Decisions already made

- D-001: Combat uses one attack button plus dash. No new input buttons without Owner approval.

## Constraints

- This report covers only what a player could see and feel. It makes no claims about causes in code or design.
- I have no authority over design decisions.
- Solutions must stay inside D-001 and the pillars: one-button combat, short runs (15–20 minutes), readable threats. They must work at 30 and 60 FPS, and should reuse existing systems where possible (small team).
- If the only viable options need a new button or change a pillar, say so plainly. That triggers an Owner escalation through `game-director`.

## Open questions

- Is the dash meant to protect the player? As a player I expected it to, and it sometimes did not. (Check against `design/combat.md`; QA is checking the build.)
- Are there rooms beyond 5 that change the pattern? I could not tell.

## Expected output

A diagnosis with causes and solution options in design terms (skill `diagnose-experience`). Put it in Findings of your outgoing Handoff. Recommend which options to pursue, and name any option that touches D-001 or a pillar.

Send the outgoing Handoff to `game-director` for the Decide stage if the diagnosis offers a real choice of direction, priority or scope. If the diagnosis shows a single obvious fix inside your own authority (rules, tuning, enemy behavior), say so. The Studio will then route to Design instead.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/diagnose-experience.md
- Project: project.md#vision; project.md#player-profile; project.md#constraints; design/combat.md; sim/build-0.3.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/01-studio-to-playtester.md
