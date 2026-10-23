---
kind: handoff
goal: G-001
seq: 31
from: game-designer
to: studio
stage: Route
outcome: done
---
# 31: game-designer → studio — Second Diagnose: why combat still felt repetitive after build 0.5, with ranked options

## Task

Route this diagnosis. I recommend **no Decide step**. All options below are changes to variant parameters, one per-variant rule flag, per-room spitter timing and room contents. All use existing systems and stay inside D-001 and the pillars. The next step is Design (write-design-spec) for the options marked "do", then Build and QA. Two small side items for QA are listed at the end.

## Context

Goal G-001: the Owner finds combat monotonous. Diagnose 04 led to design 14/22, build 0.5 and QA criteria 1–17 passing. Handoff 27 is a fresh playtester report on rooms 1–5. This is the second Diagnose, so the focus is what 0.5 did and did not fix. I read 27 against `design/combat.md`. I ran no `play` or `bots` this step, because the evidence needed is a hand-timed human session, which scripts cannot give. My claims about timing come from the spec numbers.

## Findings

### 1. What 0.5 fixed and what it left (against 04)

| Symptom in 04 | Status after 0.5 (from 27) |
|---|---|
| Grubs trivial, no telegraph | **Fixed.** Warnings are consistently readable, and cancel and stagger on swipe "felt good". Ignoring the cue now costs hearts (room 1, timed script: three hits in under 3 s). |
| Spitter volleys unreadable | **Partly fixed.** A single aim line and glow are readable. In rooms 4–5, several threats at once are not (symptom 4 below). |
| Dash never needed | **Not fixed** for melee. The dash is still optional there. |
| Rooms 1–2 interchangeable | **Not fixed in play.** Contents differ, but the answer is the same ("sidestep on the warning, then swipe or ignore"). |

The 0.5 changes made threats readable, which was needed for pillar 3. They did not make enemies ask for different answers. Readability turned the grub into "see flash, move, hit".

### 2. Symptoms, causes, and design cause versus script artifact

**S1. Melee enemies share one answer (most important for the Goal).**
- **Design cause (supported by `combat.md`):** grub, runner and brute are one behavior (wind-up, lunge, recovery, same 1.2-tile lane, same 2.4-tile lunge, same cancel rule). The parameter sets change *how long you have* but not *what you do*. The wind-up cancel works the same on all three, and sidestepping the same 1.2-tile lane works the same on all three.
- **Runner: probably partly a script artifact.** The runner's wind-up is 0.35 s. The lane is 0.6 tile either side, so a player needs a sideways move of just over 0.6 tile, about 0.15 s at 4 tiles/s. A script with a fixed 0.15 s reaction finishes at about 0.30 s, just under 0.35 s. A human with 0.25 s reaction plus 0.15 s of movement needs about 0.40 s, which is **over** 0.35 s. For a human the runner is likely a real test, unless the player swipes it in the wind-up, which is a different answer from the standard grub. The playtester's finding "the runner's short warning never tested the player" is therefore not safe to use. It needs a human check.
- **Brute: design cause plus artifact.** The brute asks for the same dodge as the others, only slower, and dodging costs nothing. The playtester dodged for 20+ s and never fought it. The room does not clear until it dies (rule: a room ends when all enemies are defeated), so a human has a reason the scripted player did not apply. A human who tries to clear room 2 will end up fighting it. What the design lacks is a *different way* to fight it. The same swipe-cancel works, so "fight the brute" is "dodge, then swipe", as for any grub. The playtester's open question ("is the brute meant to be attacked?") shows the player was not told by the game that it must die.
- **Attention drop by the second grub (room 1):** a design cause shared with the rest of S1. Three identical grubs in one room mean three repeats of the same loop. It is also helped by the script's perfect play: a human who is hit once will have more variation.

**S2. The dash was never needed against melee. Low priority; mostly a consequence of S1.**
- Cause: a 1.2-tile lane is cleared by a 1-tile sidestep, which is cheaper than a dash (0.6 s cooldown). That is by design and the dash does its job against shots. I do not recommend forcing the dash into melee. For example, widening a lane to need a dash would break the visual spec ("lane geometry identical"), and would make the cue harder to read. Instead, the dash's job is to be the answer in crossfire (S4). The dash can also close a gap on a recovering enemy (dash toward, queued swipe), which is a valid use that the scripts never tried.
- Answer to the playtester's question: no, the dash is not only for spitters, but only the spitter rooms currently make it better than a sidestep.

**S3. A single spitter loop is repetitive and drawn out. Mostly a script artifact.**
- The scripts chose to dodge on every cue and to approach slowly. Crossing 15 tiles takes about 3.75 s at 4 tiles/s, and the build 0.5 walker in QA's bots takes hearts for charging. In 04, charging was free, so this has changed. A human who rushes the last spitter finishes in a few seconds. A scripted dodge-and-approach loop is long by choice.
- Real design residue: a stationary spitter that fires every 2.4 s at one fixed pattern has no variation. This is acceptable for one spitter and not the first thing to fix.

**S4. Rooms 4–5: crossfire felt unfair (second most important, and the only real threat). Most important to *fairness*.**
- Observed: deaths at 15.75 s (room 4) and 11.1 s (room 5), all from shots, with hits from shots already in flight while lined up for another warning. Stepping out of one line put the player into another.
- Causes (from `combat.md`, to be confirmed in a trace):
  1. **Cue gap is only 0.2 s.** With two spitters, the first shots are at 1.8 s and 2.6 s and each repeats every 2.4 s. Each cue lasts 0.6 s, so cue windows are 1.2–1.8, 2.0–2.6, 3.6–4.2, 4.4–5.0 s. After one cue ends, the next begins 0.2 s later and **locks onto the player's position at that moment**, which is where the player stands after sidestepping the first. A good dodge of line 1 is therefore the aim point of line 2. The playtester's "stepping aside put me in another line" is the same thing. The player has no time to reposition before the next lock.
  2. **Shots live long.** A shot at 3 tiles/s crosses the 16-tile room in about 5 s (its lifetime limit). With two spitters firing every 1.2 s combined, 3–4 shots are in the air most of the time. Slow shots linger, so the playtester dodged a line only to meet a shot already in flight.
  3. Rooms 4–5 also contain grubs (a lunge under fire). In room 5 the brute adds a third source.
- **Discrepancy to flag (for QA, not blocking):** 27 says the spitters are in "opposite corners" and "fire in sync". Per the room table, they are at (15,0) and (15,8): the **same side** (two east corners). Per the spec, they are 0.8 s apart, not in sync. In room 3 a 5.8 s double fire was reported. The cap delay can bring two shots closer together, so this could be real, or a misreading of the printed picture. The conclusions above hold either way, but a trace of room 4 would settle which one it is.
- Not a defect on its face: criterion 13 requires cue-ignoring to cost 3–6 hearts across rooms 3–5, so the room is meant to bite. The problem is that a **cue-reading** player also dies. The scripted dodger bot clears 3/3, so the scripts that read cues in 27 (0.15 s fixed reaction, but diverted by overlapping lines) are not the bot's policy. This is the single clearest place where "hard" turns into "unfair".

### 3. Options

All stay inside D-001 and the pillars (readable threats, short runs).

**Option 1: Breathing room in spitter rooms 4–5 (addresses S4, helps S2).** *Do.*
- Change: for rooms 4–5 only, space the two spitters' cues so there is a **gap of at least 0.6 s** between one cue ending and the next starting (for example, a first-shot offset of 1.2 s instead of 0.8 s for the second spitter, with the 2.4 s interval unchanged: cue windows 1.2–1.8, 2.4–3.0, 3.6–4.2…). Optionally also lower the shots-in-flight cap to 2 in those rooms. Room 3 stays exactly as spec'd, so criterion 11 does not change.
- Why: the player gets time to take the sidestep and reposition before the next lock, so each line is a separate decision. The dash then becomes the way to cross a lane for a counter-attack rather than a panic button. This preserves "spitter danger forces movement".
- Cost: low. It is a per-room parameter (stagger, cap) on the existing spitter timing rule, with no new code path beyond a per-room value.
- Risk: criterion 13 (walker 3–6 hearts lost, dodger at most half) may move. The walker is already at the 60 FPS upper limit (6). If the walker drops below 3 total, that is a tuning matter for me, not a build defect, and a re-check of the numbers is part of the spec. Keep the interval unchanged, so run length is unaffected.
- Fit: strengthens pillar 3 (readable threats) and the Positives (spitter danger).

**Option 2: Make the melee variants ask for different answers (addresses S1, S2). *Do.***
- Change: add one per-variant flag to the existing grub rule, "can a swipe in the wind-up cancel the lunge", and use it for the **brute**:
  - **Brute (`G`)**: a swipe during its wind-up still damages it but does **not** cancel the lunge. The answer is "sidestep (or dash through), then punish in its 1.2 s recovery". Four swipes need more than one window, so the player must dodge, hit, and dodge again.
  - **Standard and runner**: unchanged (cancel works), so the runner remains "commit to the swipe or step out quickly" and the standard grub is "either".
- Why: three enemies would then want three different things (swipe-cancel quickly, either, dodge-and-punish). The brute becomes a different fight and gives a reason to learn the cue (swiping into its wind-up now costs a heart). It reuses the existing rule and parameter table, and the cue visuals are unchanged (the lane and tint are the same for all variants).
- Cost: low. It is a flag in the existing wind-up cancel check, plus the manual line (brute swipe does not stop the lunge) and a spec/criterion for it (criterion 6 and 8 need a brute case).
- Risk: it makes the brute harder, which could hurt room 5 (already deadly, deaths at 11 s). The brute's lunge is also dodgeable, so it stays fair. Check that a cue-reading player stays safe. A player who has learned "a swipe cancels" and swipes the brute in the wind-up gets hit, and this is a learning moment that should be signalled: the manual and the message ("a brute rears back, heavy") need a short line. That text is not mine to style; art-director can add presentation.

**Option 3: Give the brute a reason to be fought, in room 2 (addresses S1; also S4's single-source problem).** *Do, after 1 and 2 if the team wants a smaller first slice.*
- Change: in room 2, replace the Standard grub at (14,0) with a spitter at (14,0) (existing enemy). Room 2 becomes "runners and a brute under one spitter".
- Why: stalling and dodging the brute for 20 s now costs hearts from shots, so dodging forever is no longer free, and room 2 differs in *kind* from room 1 (no more "same fight, more enemies"). It mixes the two existing enemy classes earlier, as the player profile (comfortable with dodging and spacing) suggests.
- Cost: low (room data).
- Risk: criterion 14 (grub rooms: walker loses at least 1 heart, dodger loses at most 1 and clears both) must be rechecked with a spitter in room 2, and the rooms 1–2 sentence in the spec changes. It brings room 2 closer to 4. Not for a first slice if 1 and 2 already fix the feel.

**Needs a Decide step (named only, not chosen, not recommended now):**
- A **new enemy type** (for example a melee enemy with a genuinely different behavior, like a charger or a shielded enemy), a healing or recovery system, any new input, or a change to run length or the number of rooms. Each would need the `game-director`. I raise one only if a human playtest after Options 1–2 still reports that the melee fights feel the same. At present the evidence is scripted play, so it is premature.

**Ranking:** 1 first (the only real threat and the least fair), 2 second (the main monotony cause), 3 optional third. 1 and 2 are independent and can be built together.

### 4. The most important symptoms for the Goal

1. **S1 (melee shares one answer)** is the Goal's core: it directly produces "monotonous", and rooms 1–2 reading as the same fight.
2. **S4 (crossfire in rooms 4–5)** is the most important *problem*: the only real danger, and the one that feels unfair. A fix here protects the positives. It is also late in a run, where a player decides whether to continue.
3. S2 follows from S1. S3 is mostly a scripted-play artifact.

### 5. What the evidence cannot settle (hand-timed human session needed)

- **Runner:** with a human reaction of 0.2–0.3 s, does the 0.35 s wind-up actually test the player (my estimate says yes) and do they choose swipe or sidestep? A human needs to play room 2 at least twice and say what they did against the runner.
- **Brute:** does a human who must clear room 2 fight the brute at all, and what do they do? Do they notice the room will not clear while it lives? Kill at least one brute (the playtester never did).
- **Rooms 4–5:** is the crossfire unfair for a human, or only for a scripted player who reacts at a fixed 0.15 s? Hand-timed play in rooms 4–5, at least two attempts each, noting cause of each hit (a shot in flight, a new lock, or a line misread). Also whether the two spitters really fire together.
- **Rooms 2 and 3 endings:** the playtester's output was cut off, so the end of those sessions is unknown. Do not treat the 20+ s brute dodging as a finding about clear times.
- **Dash:** whether a human uses it on purpose against shots once Option 1 is in. Experience signal: at least once in a room, not only in panic.

## Decisions already made

- D-001: attack and dash only; no new input. All options comply.
- D-002: per-frame contact sampling and the contact-edge graze stay. Not touched here.
- D-003 (step 30, band wording): not touched.
- Step 9b and the room 2 possible defect (handoff 29) are separate and not diagnosed here.

## Constraints

- Pillars: one-button combat, short runs (15–20 min), readable threats. Play correctly at 30 and 60 FPS. Reuse existing systems.
- Option 1 keeps the 2.4 s interval, so run length is unaffected. Option 2 and 3 are content and rule-flag changes. No run-length change.
- The visual spec says lane geometry is identical for all variants. Option 2 keeps this. Any option that changes lane width per variant would need `art-director` and a spec change, and I do not propose one.

## Open questions

- None that need a Decide step.
- For the Studio: whether to take Options 1 and 2 as one Design step (my recommendation) or 1 first. If a human playtest of the hand-timed kind can run **before** the Design step, it would settle the runner and brute questions above and could change the priority of Option 2. It is not blocking, because Option 1 is justified by the spec numbers alone.

## Expected output

Route to Design for `game-designer` (write-design-spec) for Options 1 and 2, with Option 3 as optional. The spec updates `design/combat.md`: per-room spitter stagger and cap for rooms 4–5, the brute wind-up flag, manual text, and any rewritten criteria (6, 8, 13, 14 if room 2 changes), plus new player-observable criteria (for example: a cue-reading player in rooms 4–5 can name which line to avoid; a brute swipe in its wind-up does not cancel the lunge). Then Build, then QA at 30 and 60 FPS, then a **hand-timed** playtest of rooms 2, 4 and 5 (briefed on the unknowns in Findings 5).

Two side items for QA, not blocking: (a) a trace of room 4 and of room 3 around 5.8 s to confirm spitter fire times and shots in flight against the spec (0.8 s apart, at most 3 in flight), given 27's "in sync" report; (b) handoff 29, the room 2 defect, already routed.

## Sender assessment

Confidence: high that S1 is a design cause (one shared behavior and answer, and the 0.5 changes tuned timing, not the answer). Medium on S4's causes: they come from the spec numbers and the playtester's account, and the "in sync" and "opposite corners" statements conflict with the spec, so a trace is wanted. Medium-low on the runner and brute conclusions: they rest on scripted play and on my reaction-time arithmetic. I ran no `play` or `bots` this step, so I did not verify any build behavior.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#constraints, design/combat.md, design/combat-cues-visual-spec.md, repo/manual.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-contact-edge-graze-accepted.md
- Previous handoff: goals/G-001-combat-monotony/31-game-designer-to-studio.md
