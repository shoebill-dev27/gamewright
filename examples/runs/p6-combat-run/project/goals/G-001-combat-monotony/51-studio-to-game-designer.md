---
kind: handoff
goal: G-001
seq: 51
from: studio
to: game-designer
stage: Diagnose
outcome: routed
---
# 51: studio → game-designer — Diagnose the room-1 play findings

## Task

Diagnose the experience problems a playtester reported from room 1 of the current build. Give causes and solution options in design terms, and say which ones are within your authority and which need a Decision from `game-director`.

## Context

G-001 is "戦闘が単調なので改善したい" (combat feels monotonous). Option A (D-002) reworked existing enemy behavior; the build now has telegraphed, multi-state enemies. A playtester then played the build as a first-time player. They saw room 1 only, because both attempts ended in defeat ("run over — rooms cleared: 0"). The full report is `50-playtester-to-studio.md` (previous handoff).

## Findings

Taken from the report (observations only, not decisions):

- **Loop seen.** Every grub did the same cycle: walk up, "rears back" (`G`), bite about 0.5 s later, "open" (`g`). The tester could not say whether later rooms vary.
- **Pressure.** Room 1 starts with 3 grubs that all approach at once. Several reared back within about 0.03–0.04 s of each other (3.90/3.93 s; 6.43/6.47 s). One safe response (step away or dash) covers only one of them, and the dash recovers slowly. The tester felt pinned rather than skillful.
- **Hearts.** Three hearts were lost quickly (2.5, 4.0 and 4.8 s in attempt 1). The tester felt they were losing from the second hit.
- **Stun on being hit.** The swipe was refused with "(stunned)" at 2.5 s and 7.0 s, just when the tester wanted to hit back, with a second grub already winding up. The tester called this the sharpest frustration.
- **Swipe "(miss)" next to a grub.** Swipes into a grub that was reared back or biting did nothing and showed "(miss)" over the grub's tile (2.1 s, 4.0 s). The tester guessed the grub is not hittable during wind-up or bite and said the manual does not state this.
- **Facing.** The player can turn only by moving. After a dash to the right wall, three swipes (4.7, 5.4, 6.1 s) hit empty air while the grubs were on the left. The tester asked for a way to turn without moving, or a swipe that works behind the player.
- **Dash.** It clearly mattered. A dash through a bite caused no damage. The end point was hard to judge beforehand, and one dash landed next to a grub that reared back on arrival.
- **Best moment.** The clean counter sequence: hit at 2.8 s after a bite, kill at 3.5 s.
- **Display.** When a grub shared the player's tile it was drawn beside the player ("on you"), which was confusing about which side to hit.
- **Not observed.** Rooms 2–5, the spitter, projectile hits and room clear. A second Play session (52) is looking at those; its result comes to the Studio separately.

Caution: the tester played by timed input scripts and could not react within a run, so some failures are probably their own timing. Check the points above with `run_trace` and `run_bots`, and compare them with the spec before treating any of them as a design problem. Separate spec-conforming behavior that is hard to read (a manual or display issue) from behavior that is too harsh (a tuning issue).

## Decisions already made

- D-001: one attack button plus dash; no new input buttons without Owner approval. A "turn without moving" input would conflict with this.
- D-002: respond to combat sameness by reworking existing enemy behavior first (Option A).
- D-003: room mix is across rooms; zero hearts ends the run; room clear heals one heart.
- D-006: enemies may overlap the player but are never hidden.

## Constraints

- Stay within the vision and D-001 (pillars: one-button combat, short runs, readable threats). Prefer changes that reuse existing systems.
- Must play correctly at 30 and 60 FPS.
- Do not change the Goal's scope. If an option changes the facing mechanic, the input scheme or the Option A scope, mark it as needing `game-director` rather than deciding it.

## Open questions

- Which findings are spec-conforming and only unclear to the player (the swipe-miss window, the dash end point, the "on you" display, facing), and which are tuning (room 1 pressure, simultaneous rear-backs, stun on hit)?
- Does room 1 break the intended pace? Check with `run_bots` and `run_trace`, using a still player and a passive bot as reference. Open Review items name "a still player going down in about 5 s".
- Is the monotony itself (the same grub loop) still present, or did these findings replace it with a harshness problem?

## Expected output

A diagnosis with options, in the Findings of your outgoing handoff (`templates/handoff.md`). Group the options by authority: yours (rules, tuning), `game-director` (direction or scope), and `art-director` (display). Recommend one. Do not edit the spec in this step. Address the result to `studio` (`53-game-designer-to-studio.md`).

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/diagnose-experience.md
- Project: project.md#vision, project.md#constraints, project.md#player-profile, design/combat.md, design/combat-visuals.md, manual.md, the build `repo/` (`run_trace`, `run_bots`)
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-response-scope.md, decisions/D-003-run-end-and-room-rules.md, decisions/D-006-overlap-display-and-practice-room-manual.md
- Previous handoff: goals/G-001-combat-monotony/50-playtester-to-studio.md
