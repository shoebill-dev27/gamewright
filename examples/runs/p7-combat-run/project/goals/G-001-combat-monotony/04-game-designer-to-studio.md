---
kind: handoff
goal: G-001
seq: 4
from: game-designer
to: studio
stage: Route
outcome: done
---
# 04: game-designer → studio — Diagnosis of combat monotony, with options and recommendation

## Task

Route this diagnosis. My recommendation is that no Decide step is needed and the work goes to Design. Two side items need routing: a possible FPS-dependent difference in the bot results (engineering/QA) and a short playtester pass on rooms 4–5.

## Context

Goal G-001: the Owner finds combat monotonous. The playtester's report (02) came from scripted play. I checked it against `design/combat.md` and ran `run_bots` (camper, walker, dodger; rooms 1–5; 30 and 60 FPS). The first runs used a wrong script format and produced nothing, so the usable results are the two full runs. I did not run `run_trace` or `run_tests`, so build behavior is verified only through the bots, not the simulation state.

## Findings

### 1. Evidence summary (bots, rooms 1–5)

| Bot | Result at 60 FPS | Result at 30 FPS |
|---|---|---|
| Walker (walks at enemies, attacks, never dashes) | Cleared 5/5, 1 heart lost in total, 5–13.5 s per room | Same: 5/5, 1 heart lost |
| Dodger (uses dashes) | 4/5, 6 hearts lost, 30 dashes. Room 3 failed. | 5/5, 3 hearts lost, 18 dashes |
| Camper (stands still, attacks what comes near) | 2/5. Cleared the grub rooms with 0 hearts lost; lost rooms 3–5 to shots. | Same |

- In rooms 1–2 no bot lost a heart to a grub, and no grub hit any bot in any room. The only damage anywhere in rooms 3–5 was from shots.
- Grub rooms took 5–7 s with 6–8 attacks and 0 dashes, whichever bot played.

### 2. Symptoms, causes, evidence status

**S1. Grub fights are a repeated loop with no decisions (rooms 1–2 feel identical).**
- Supported: the walker and camper clear both rooms with no damage and no dashes. The playtester's hits do not generalize.
- Cause C1 (supported by `design/combat.md` and the bots): the Grub is a single straight-line behavior with no telegraph and no variation. It dies to two swipes (0.7 s) as it arrives. The best play is "face it and swipe", so there is nothing to read, dodge or space.
- Cause C2 (hypothesis): rooms 1 and 2 differ only in grub count. The design lists "mixed Grubs and Spitters" for 3–6 enemies, but the composition and layout of rooms 1–2 are not documented.
- The playtester's "trading hits" was their script's reaction timing, not build balance. The real problem is the opposite: grubs pose almost no threat.

**S2. Idle approach to the last enemy (about 1.3 s).**
- The clear times (5–7 s for 3–4 grubs) include walking time, so dead time is a large share of the room. This is probably spawn distance and layout (hypothesis); I have not measured it.

**S3. Spitter rooms: dodging with no way to progress.**
- Partly supported. The camper is punished (0 attacks, shots only). The walker simply walks in and clears room 3 losing 1 heart, so "no way to progress" is not general; it came from the playtester's "move aside" rule set.
- Still, the dodger does worse than the walker in every spitter room. The dash and dodging are a dominated strategy: more time, more hearts lost, and a failed room 3 at 60 FPS.
- Cause C3 (supported by `design/combat.md`): the Spitter is stationary and fires on a fixed 2 s timer, aimed at the player, with slow shots. A straight charge crosses the lane quickly and kills it with 2 swipes. Dodging is therefore not rewarded.
- Cause C4 (hypothesis): volleys from several spitters on the same timer overlap into a wall of shots that the playtester could not read. This matches the playtester's account and the bots' damage totals, but I have not traced it.

**S4. The dash is never needed (the playtester only used swipe and dash, the same way each time).**
- Supported: the walker clears 5/5 with 0 dashes.
- Answer to the playtester's question: per `design/combat.md`, the dash makes the player invulnerable for its full 0.25 s duration. Build 0.4 is said to have fixed damage during a dash. The cooldown is 0.6 s, so the hit 0.6 s after the dash at 12.1 s was after the protection ended. It was not a dash failure. The protection is short and cannot be read from the log, which is why the dash felt unreliable. I have not verified in the trace that the build matches the design.

**S5. Always lost, no recovery, 5–15 s runs.**
- Not supported as a general finding. The bots mostly clear with 0–3 hearts lost. This symptom comes from the scripts and should not drive the design.

### 3. Things the evidence cannot settle

- **FPS divergence.** The dodger fails room 3 at 60 FPS (19.7 s, 13 dashes, 3 hearts lost) but clears it at 30 FPS (9.5 s, 0 hearts lost, 4 dashes). Room 4 also differs (21.8 s vs 17.8 s). The cause could be the bot's logic or build behavior. The project requires correct play at both 30 and 60 FPS, so this needs a check by technical-director or QA (for example `run_trace` on room 3 at both rates). It is not a design question, and I did not diagnose it.
- Rooms 4–5 (composition, what they add): the bots only show that they are clearable, with damage only from shots. No human has seen them.
- Hand-timed play: whether grub fights feel monotonous when played deliberately is unanswered.
- I have not seen `bots.py`, so I do not know what the bots' strategies assume.

### 4. Solution options

All three options stay within D-001 (no new inputs) and the pillars.

**Option A. Make grubs readable and varied (enemy behavior).**
- Change: give the grub a short telegraphed lunge (a visible wind-up, then a fast dash-bite along a line), and add one variant (for example a slow, tough grub, or a faster one) so the grub rooms differ.
- Addresses: S1, S4. A telegraph makes a sidestep or dash a real answer, a threat you read before it hurts, which supports pillar 3.
- Cost: low to medium. It reuses the grub's walk and contact bite, adding a wind-up state and a lunge. Needs art-director input for the cue.
- Risk: the lunge speed needs tuning, so it is not impossible to dodge at 30 FPS.

**Option B. Make spitter pressure readable and answerable (parameters, rooms).**
- Change: stagger the spitters' fire timers so volleys do not overlap, show a short aim cue before each shot, cap shots in flight, and place spitters so a route to them exists. The aim is for dodging to lead to a counter-attack, not a chore.
- Addresses: S3, S4. It makes the dash a useful tool for getting through a lane.
- Cost: low (parameters, spawn positions). Some cue work.
- Risk: it may make room 3 too easy, because the walker already clears it. The numbers need bot verification.

**Option C. Differentiate rooms (content composition, pacing).**
- Change: rework which enemies appear in rooms 1–2 and where they come from (multiple sides, staggered arrivals, shorter approach), using only existing enemies.
- Addresses: S1, S2.
- Cost: low. It is a data change.
- Risk: by itself it does not change what a grub fight is, and the problem may return.

**Out of my authority, noted only:** a new enemy type, or a healing/recovery system. Both would expand scope and effort, and healing touches difficulty and run length. They need the Director's decision. I do not recommend them now.

### 5. Recommendation

Do A and B together, with C as a light pass. They are changes to rules, tuning and rooms within my role's authority and fit the vision and D-001. The A+B combination addresses the main cause: threats are either trivial or unreadable, and the dash is never needed. The acceptance criteria for Design would be that, in the bots, a walker that never dashes loses clearly more hearts than a dodger that uses the dash well in rooms 3–5, with that result at both 30 and 60 FPS. Within the options there is no real choice of direction or scope and no escalation trigger, so I recommend the Studio routes to Design without Decide.

## Decisions already made

- D-001: one attack button plus dash; no new input without Owner approval. None of the options conflicts with it.

## Constraints

- Pillars: one-button combat, short runs (15–20 min), readable threats. Must play correctly at 30 and 60 FPS. Small team, reuse of existing systems.
- Design should not rely on the playtester's raw losses as balance data. The bot results above are the better basis.

## Open questions

- FPS divergence in the dodger's room 3 and 4 results: build or bot artifact? (technical-director/QA)
- What do rooms 4–5 contain, and does a human experience them differently from the bots? (playtester, optional, in parallel with Design)
- Do grub fights feel monotonous in hand-timed play? (playtester, after Design is built)

## Expected output

The Studio routes to Design for game-designer: a spec for options A and B with a light pass on C (rules, parameters, edge cases, player-observable acceptance criteria using the bot comparison above). Separately: (1) technical-director or QA checks the 30/60 FPS divergence; (2) an optional playtester observation of rooms 4–5, which can run alongside Design.

## Sender assessment

Confidence: high that grubs are trivial and the dash is not needed (several bots agree, the design agrees). Medium on the spitter cause (C4 unverified in the trace). Low on rooms 4–5 and on the FPS question. Unverified: build behavior against the design (invulnerability), since I did not run `run_trace` or `run_tests`.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#constraints, design/combat.md, repo/manual.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/04-game-designer-to-studio.md
