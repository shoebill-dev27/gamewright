---
kind: handoff
goal: G-001
seq: 90
from: qa
to: studio
stage: Verify
outcome: done
---
# 90: qa → studio — Room 4 shot hits and "swiped, still hit" on build 1ac4d04d0e75: no defect; two readability gaps; room 3 timed items (C) stay unverified

## Task

Judge two player-reported experiences (A: room 4 hits, B: "swipe landed, still hit") and make a last attempt at the open room 3 timed items (C). Everything was run at 30 and 60 FPS where noted.

## Context

Goal G-001. Report 88 is the playtest. I used one run round (three trace/play runs of room 4, with reaction rules like the player's). No code or document was changed. I spent the round on A and B, so C was not run (see below).

## Findings

### Verdicts

| Item | Verdict |
|---|---|
| A. Room 4 hits | **No defect found.** The player's three hits were **not reproduced** (script not kept, so my rules differ). Dash invulnerability matches the design. **Readability failure (confirmed in the player view):** a shot hit gives no source and the shot disappears at the hit. |
| B. Swipe landed, still hit | **Matches design.** Reproduced at 30 FPS in room 4. **Readability failure:** no line says why the lunge was not cancelled. |
| C. Room 3 timed items | **Unverified** (no run this round). Goes to Review as a known gap. |

### Scripts (rerunnable; `python3 play.py --view trace|player {script}`)

Room 4, run at `fps 60` and `fps 30` (trace) and `fps 60` (player view):

```text
room 4
fps 60
when text "takes aim" then move aside
when text "rears back" then dash aside
when see * coming within 2 then dash aside
when see g within 1.4 then attack
when see r within 1.4 then attack
when see g within 20 then move toward
when see r within 20 then move toward
when see s within 20 then move toward
```

This follows the player's stated rules, but it is not the player's exact script. Its output was partly cut (the 60 FPS trace between about 14 and 19 s). Anything I say about those parts is not claimed.

### Item A

**What I could not reproduce.** The player's hits at 3.45, 5.38 and 8.55 s did not occur in my runs.
- 60 FPS: no hit in the visible part before about 14 s.
- 30 FPS: the first hit was at 6.300 s.

I tried the player's rules as written, at both rates. Because the exact script was lost, the three specific hits are open, not disproved.

**What the runs do show.**

1. **Dash window is correct.**
   - Every dash in the traces shows `dash_left=0.233` at the first frame (60 FPS) or 0.217 (30 FPS), `invulnerable=True`, and `invulnerable False` at `dash_end` about 0.25 s later.
   - No damage was taken during any dash (design: 0.25 s, `combat.md` Player kit).
   - A hit 0.8 s after a dash is therefore not a defect by itself.

2. **A hit after a wasted dash (30 FPS, 6.300 s, source: grub).**
   - The dash was at 5.467 s and ended at 5.700 s.
   - The grub began its wind-up at 5.667 s, lunged at 6.167 s and hit at 6.300 s, 0.6 s after the dash ended.
   - The dash came too early for that lunge. The cue was shown for the full 0.5 s.

3. **Shot hits in my runs were point-blank.**
   - The 30 FPS hits at 9.800 s and 13.000 s, and the 60 FPS hits at 23.200 s and 25.800 s, happened on the same frame as "a spitter spits".
   - In each, my rules had walked the player next to the spitter: the 30 FPS hits had the player at (15.00, 0.00) and (14.60, 0.00) next to the spitter at (15, 0), and the 60 FPS hits had it at about (14.9, 8.0) next to (15, 8).
   - My rule set has no swipe-at-spitter rule, so this is an artifact of my script, not a finding.
   - The aim line and the `cue:` line were shown for the full 0.6 s before each of these. Pass for readability of the cue.

4. **The hit message gives no source (player view, 60 FPS).**
   - The line is `YOU ARE HIT by a shot — hearts 1/3` at 23.200 s and the same at 25.800 s.
   - It does not say which spitter fired.
   - The frame after the hit shows no shot at the player. In the 23.20 s and 25.80 s frames the `*` marks seen are other shots, far away.
   - By the design, a shot that makes contact is consumed and disappears (`combat.md`, Shot and Blocked contact). So a post-hit frame can never show the shot that hit.
   - Shots take about 1–4 s to cross, so several `*` are on screen, and none of them is marked as the one that hit.

**Hypothesis, not confirmed.** The player's hits at 3.45 s and 8.55 s were 0.8 s and about 0.65 s after the player's dashes ended. Both are consistent with shots already in flight when the dash ended. For example, the first room 4 shot is fired at 1.8 s from the far corner and takes about 3 s to reach the middle of the room, so it can arrive at about 3.4–4 s. A 0.25 s dash only protects the player for the dash itself. I could not match these to a particular shot without the original script.

**Verdict A.** No defect; dash invulnerability matches the design. The player's hits could not be reproduced. The inability to tell which shot hit is a **readability failure** (the build matches the design; the player view does not show the cause).

### Item B

**Reproduced (30 FPS, room 4, trace).**
- The grub's wind-up began at 5.667 s and its lunge at 6.167 s.
- A swipe at 6.267 s hit it (`grub hp 2→1`, `attack hits [('grub','hit')]`), and the player was hit at 6.300 s (hearts 3→2).
- The swipe landed 0.1 s after the lunge began and did not cancel it. The lunge continued and the grub went to recovery at hp 1.
- This matches the late-swipe rule in `combat.md` (a swipe cancels only during wind-up) and the manual ("A swipe that lands after the lunge has begun does not cancel it").
- Cancel does work in wind-up (seen in report 86 at 60 FPS, 7.683 s).

**Reports from the player (derived, not reproduced).**
- Room 2 (swipe 5.92 s, hit 5.95 s): the cue began about 5.42 s (the first swipe at 5.42 s was out of reach), and a 0.5 s wind-up ends at about 5.92 s. The swipe came at or just after the lunge start, and the hit followed one frame later. This is consistent with the boundary.
- Room 3 (swipe 8.12 s, hit 8.25 s): the hit is 0.13 s after the swipe, inside the 0.3 s lunge. This is consistent with a swipe after the lunge started.
- Room 5 brute: by design (`the brute shrugs off the swipe`).

**Messages.** In the player view the order reads as a swipe result ("you swipe: …") followed by "YOU ARE HIT by a grub". In the output I could see, no line says that the lunge had already started or that the swipe was too late. The `cue:` line and the `~` lane also stop at the lunge start (the design allows this). Only the brute has a "shrugs off" line. I did not see the full player-view output of the 6.267 s case, so this is based on the visible player-view lines and the design text.

**Verdict B.** Matches design. **Readability failure:** the player view has no line that says why the swipe did not stop the lunge.

### Item C (unverified)

I did not run any room 3 script this round. I used the round on room 4, and room 3 needs a new deterministic script. Nothing here is a failure.

| C item | Status |
|---|---|
| R3-8 at 60 FPS | **Unverified.** The 30 FPS result stands (2.37 s against 6 s, report 86). At 60 FPS the report 86 rules script was shut off by "dash aside" dashing away from the last spitter. |
| Pure 1-tile sidestep in room 3 | **Unverified in room 3.** Passes in the practice room (report 82, criterion 2). |
| 30 FPS cancel and recovery swipe in room 3 | **Unverified in room 3.** Cancel was seen at 60 FPS, and at 30 FPS only in report 76. |

For whoever picks this up in Review, an untested starting point for R3-8 at 60 FPS is the report 86 rules with a narrower dash trigger and a swipe rule for spitters (`when see * coming within 1.5 then dash aside`, `when see g within 1.4 then attack`, `when see s within 1.4 then attack`, then the two `move toward` rules). It has not been run.

## Decisions already made

D-002, D-003, D-007, D-011, D-012 applied as written. None reopened.

## Constraints

No code or document changed. Claims are limited to what the traces show. The run output was partly cut, and the player's script was not available.

## Open questions

1. **For `game-designer` or Review (readability, not defects):**
   - (a) Should the hit message or post-hit frame identify the source of a shot (which spitter, or where it came from)? Today `YOU ARE HIT by a shot` carries no source and the shot vanishes at the hit.
   - (b) Should the text view say why a swipe did not cancel a lunge that has already begun (for example when a swipe hits a grub in its lunge)?
2. **Review:** record C as a known gap (R3-8 at 60 FPS, the room 3 sidestep, and the 30 FPS cancel and recovery swipe).
3. **Review:** the player's exact room 4 hits (3.45 s and 8.55 s) are not reproduced; a hand-timed playtest of room 4 is the check if this matters.

## Expected output

Studio routes. Nothing goes to `gameplay-engineer`. Readability items 1(a) and 1(b) go to `game-designer` or Review, and the open gaps to Review.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md, studio/skills/verify-change.md
- Project: project.md, repo/manual.md, design/combat.md, design/combat-step72.md, design/combat-cues-visual-spec.md, goals/G-001-combat-monotony/86-qa-to-studio.md
- Decisions: decisions/D-002-contact-edge-graze-accepted.md, decisions/D-003-contact-edge-exact-reach-and-lunge-band.md, decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md, decisions/D-011-variant-named-messages-accepted.md, decisions/D-012-room3-standard-grub-and-closer-spitter.md
- Previous handoff: goals/G-001-combat-monotony/89-studio-to-qa.md
