---
kind: handoff
goal: G-001
seq: 22
from: game-designer
to: studio
stage: Verify
outcome: done
---
# 22: game-designer → studio — Graze accepted, cap is on cue starts, walker margin kept, governing documents named; no build change, QA closes the open gaps

## Task

Route to QA to close the remaining checks (below). The verdict can become `pass` if they hold. No Build for `gameplay-engineer` is needed.

## Context

G-001 (combat monotony). Handoff 20 (QA) verified build 0.5 against criteria 1–16 and raised four spec questions. They are ruled here and written into `design/combat.md`. I did not run `play` or `bots`; the rulings use QA's numbers from handoff 20. The one derived figure I rely on (grub lunge band about 0.015 tile) is not yet run and is checked in QA's close-out.

## Findings

### 1. Frame-rate-dependent graze: accepted (D-002)

- **Ruling:** acceptable for the text build. The sampling rule is: contact is a distance check once per frame after that frame's movement, shot reach 0.4 tile, lunge reach 0.6 tile, no swept test.
- **Accepted band:** the path's lateral miss within 0.01 tile inside the reach for shots (QA derived about 0.003) and within 0.03 tile inside the reach for lunges (derived about 0.015). Inside the band, 30 and 60 FPS may differ in hit or miss. Outside the band both must agree and follow the geometry (smaller than reach − tolerance: hit; reach or more: never a hit). Only hit or miss may differ, never timing or cue.
- **Why:** the band is far below what a player can see or aim at, a sidestep margin is 0.3 tile or more, and a swept test would change a verified build with no visible gain.
- **Also applies to grub lunges,** with the wider tolerance above.
- **Spec change:** new Contact sampling rule in the Timing rule, new criterion 17 (edge checks), and 16e now says a difference caused only by the band is not a build defect. 16e therefore passes: QA already showed the walker differences are bot timing.
- **Known, accepted limitation of the text build.** Re-check in a graphical build: if its hitboxes or contact test differ from the text build's, re-run criterion 17 at 30 and 60 FPS and rewrite the tolerances (recorded in D-002 and in the spec's open questions).

### 2. Shot cap: a limit on cue starts (as built)

- A cue may start only if fewer than 3 shots are in flight; otherwise wait 0.2 s. It is not rechecked at the shot. So shots from cues already showing may take the count above 3.
- Hard bound: never more than 2 + the number of living spitters. In every real room (at most 3 spitters) the count stays at 3 or fewer (QA: room 3 over 12 s). Only a practice room with four or more spitters can exceed 3 (QA saw 5).
- Why: the cue is the telegraph. Dropping a shot whose cue is already showing would make a visible warning lie.
- Criterion 11 is reworded: "In rooms 1–5 never more than 3 in flight; in a practice room with four or more spitters the cap is on cue starts, bound 2 + living spitters."
- **Note for the Studio:** `repo/manual.md` says "no more than 3 are in the air at once". That is true for every real room and is not wrong for play, only for practice rooms with four or more spitters. I did not edit the manual (outside my paths). Optional wording fix: "no more than 3 are in the air at once in the five rooms".

### 3. Walker margin at 60 FPS: keep

- Criterion 13's numbers stay (walker 4 lost / 2 cleared at 30 FPS, 6 lost / 3 cleared at 60 FPS, upper limit 6; dodger 0; camper 0).
- Reason: the bots are deterministic, the result is inside the range at both rates, and 6 hearts over 3 rooms (2 per room) still reads as "costly but not hopeless". Retuning the room or the spitters would be a Build with no gain.
- If a later change pushes the walker to 7, that is reported to the designer as a tuning question, not fixed as a defect (written into criterion 13).

### 4. Contradictions: which document governs

| Point | Governs |
|---|---|
| Lunge line | `combat.md` rule: the cue shows the true 1.2-tile lane (0.6 either side, 2.4 long). The "thin line" for grubs is withdrawn (thin is for the spitter only). The look of the lane: visual spec. The text view's one-cell `~` line stays. |
| Spitter glow | Timing and "noticeable from the first frame": `combat.md`. Ramp start level: visual spec (floor of at least 30%). Text view keeps 0%. No timing changes. |
| Grub cue | Visible for the whole wind-up and gone at once on cancel or kill: `combat.md`. Steady tint with a slight pulse (≤ 3 Hz), lane full until lunge start and fading during the lunge: visual spec. The text view removing the line at lunge start is acceptable. |
| Marks `r` / `G` | Text build: `combat.md` and manual, unchanged. Graphical build: silhouette and size per the visual spec. The open question is closed. |

`art-director` has nothing to rework in the visual spec (only its note that the design text says "thin line" is outdated). V12 stays open until a graphical build exists. I did not rule on visual style.

## Decisions already made

- D-001: one attack button plus dash; no new input. Unchanged.
- Handoff 14 rulings on 13–16 and the five spec defaults: unchanged, except the 16e amendment above (with the reason given).
- New: D-002 (contact sampling kept, graze accepted).

## Constraints

- No new enemy type, healing system, input or scope change was needed, so no hand-back to `game-director`.
- Everything stays within D-001 and the vision pillars, and holds at 30 and 60 FPS.

## Open questions

1. Does the grub lunge band stay within 0.03 tile at 30 FPS? QA's close-out run checks it (criterion 17c). If wider, back to the game-designer.
2. Manual wording about the cap (optional, see finding 2).

## Expected output

The build does not change. QA closes the open gaps and gives the verdict:

1. Criterion 5, the two-swipe kill (6) and the variant swipe counts (8) at `fps 30`, with the existing practice-room scripts.
2. The edge case "a defeated spitter does not renumber the others" (not run so far).
3. New criterion 17: the reproduction script from handoff 20 with spitter positions chosen from the trace so that the shot's lateral miss is 0.39 tile or less (hit at both rates) and 0.40 tile or more (no hit at both rates). One grub case on each side of the lunge band (0.57 or less hits at both; 0.60 or more misses at both), and report the measured lunge band at 30 FPS.
4. Criterion 11 in its new wording (room 3 at most 3 in flight; the four-spitter practice room within 2 + living spitters).

If all hold, the verdict is `pass` (16e passes as ruled; V12 stays open). If a criterion fails outside the band, route to `gameplay-engineer`.

## Sender assessment

- No `play` or `bots` run was made. The band sizes are QA's derived values; my tolerances (0.01 and 0.03) include margin over them (about 3× for shots, 2× for lunges), and criterion 17 makes them verifiable.
- Confidence: high on the rulings, since they match the build as QA described it. Medium on the grub lunge band until QA measures it.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md, repo/manual.md, repo/game.py, repo/bots.py, repo/play.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-contact-edge-graze-accepted.md
- Previous handoff: goals/G-001-combat-monotony/20-qa-to-studio.md
