---
kind: handoff
goal: G-001
seq: 28
from: studio
to: game-designer
stage: Diagnose
outcome: routed
---
# 28: studio → game-designer — Diagnose the experience issues from the fresh playtest (rooms 1–5)

## Task

Diagnose why a fresh playtester still experienced combat as repetitive after build 0.5, and give solution options in design terms. Address the result to `studio`.

## Context

Goal G-001: the Owner said combat feels monotonous ("戦闘が単調なので改善したい"). A first Diagnose (04) led to a design (14, 22), build 0.5 and QA verification (criteria 1–17 pass at 30 and 60 FPS). Handoff 27 is a fresh playtester's report on the result. This is the second pass through Diagnose, so progress must be concrete: say which observed symptoms the 0.5 changes did and did not address, and keep options small and reusing existing systems.

## Findings

Summary of the playtester's observations (full report: 27). Caveat from the playtester: sessions were input scripts with a fixed ~0.15 s reaction, steadier than a human. Rooms 2 and 3 output was cut off, no brute was ever killed, the practice room was not tried, and each reaction script ran once per room. Treat the points below as single-session observations.

1. **Melee enemies share one answer.** Grub, runner and brute all asked for "sidestep on the warning, then swipe or ignore". Rooms 1 and 2 felt interchangeable apart from enemy count. The runner's short warning never tested the player. The brute (slow, 0.7 s warning) was only dodged, trailed the player for 20+ s lunging into empty space, and gave no reason to fight it. Attention dropped by the second grub in room 1.
2. **The dash was never needed** against melee; a one-tile sidestep always sufficed. A swipe during a warning cancels the lunge and staggers the enemy, which felt good. The playtester asked whether the dash exists only for spitters.
3. **Spitters are the only enemy that changed movement.** The aim line and glow were readable. With one spitter left the loop (line, dodge, shot passes, about every 2.4 s) felt repetitive and drawn out.
4. **Rooms 4–5 crossfire.** Two spitters in opposite corners fire in sync, so aim lines cover most of the room, and slow shots in flight cross. The player was hit by shots already in flight while lined up for another warning, and could not tell which line to avoid. This was the only real threat and felt the least fair. Deaths came at 15.75 s (room 4) and 11.1 s (room 5), both from shots, in room 5 with the brute still alive.
5. A possible defect in room 2 at about 5.9–6.0 s (hit by a grub right after a lunge-cancelling swipe) goes to QA separately (handoff 29). Do not diagnose it here.

Positives to preserve: warnings consistently readable, short fights (room 1 cleared in 4–5 s), the cancel and stagger on swipe, and spitter danger that forces movement.

## Decisions already made

- D-001: attack and dash only; no new input buttons.
- D-002: per-frame contact sampling kept; the contact-edge graze is accepted.
- Studio route decision earlier: no Decide step so far, because all options stayed inside D-001 and the pillars.

## Constraints

- Vision pillars: one-button combat, short runs (15–20 minutes), readable threats.
- Small team: prefer changes that reuse existing systems. Must play correctly at 30 and 60 FPS.
- Out of scope: new input buttons, run length changes, new biomes or unrelated content.
- Step 9b (your handoff 26: exact-reach miss, lunge band record in D-002) is a separate, non-blocking item. Do not reopen it here.

## Open questions

- Which of symptoms 1–4 are design causes and which are artifacts of scripted play (fixed reaction time, one run per room)? Say what a human, hand-timed session would need to confirm.
- Do your options stay inside D-001 and the pillars? If an option needs a new enemy type, a healing system, a new input, or a scope change, name it as such and state that it would need a Decide step with the `game-director`. Do not decide that yourself.

## Expected output

A diagnosis with causes and ranked options in design terms, written in Findings of your Handoff (or in the design documents it names), `to: studio`. State plainly which symptoms you consider the most important for the Goal, and whether you recommend a Decide step.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/diagnose-experience.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, design/combat.md, design/combat-cues-visual-spec.md, repo/manual.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-contact-edge-graze-accepted.md
- Previous handoff: goals/G-001-combat-monotony/27-playtester-to-studio.md (earlier diagnosis for comparison: goals/G-001-combat-monotony/04-game-designer-to-studio.md)
