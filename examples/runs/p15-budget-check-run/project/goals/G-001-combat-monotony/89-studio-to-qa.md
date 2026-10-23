---
kind: handoff
goal: G-001
seq: 89
from: studio
to: qa
stage: Observe
outcome: routed
---
# 89: studio → qa — Check the room 4 hits and the "swipe landed, still hit" cases from a player report; one last bounded try at the 60 FPS timed items

## Task

Find out whether two player-reported experiences hide a defect or a readability failure in build `1ac4d04d0e75` (items A and B). Then make one last bounded attempt at the open room 3 timed items (item C). Run everything at 30 and 60 FPS.

## Context

Goal G-001 (combat feels monotonous). A fresh player session played rooms 1–5 with reaction rules (react to what is on screen, 0.15 s delay) and read the printed `--view player` frames. The session report is `goals/G-001-combat-monotony/88-playtester-to-studio.md`. Your earlier report is `86-qa-to-studio.md` (no defect; R3-8 passes at 30 FPS only; the room 3 sidestep is not observed in room 3). Pillar 3 (readable threats: every threat is visible before it can hurt the player) is what the player-view items touch.

## Findings

What the player reported (observations only; treat them as claims to reproduce, not as conclusions):

**A. Room 4 hits the player could not explain.** Room 4 starts with 2 spitters, a grub and a runner. The player went down at 8.55 s with three hits taken:
- 3.45 s: the player had dashed left at 2.65 s and was still hit. The frame after the hit shows no shot near the player.
- 5.38 s: the player was swiping the runner while standing in a spitter's glowing line at 97% brightness. The player could explain this one.
- 8.55 s: the player had dashed down at 7.65 s and was hit about a second later. Again no shot was visible near the player.

The player's rules in rooms 3–5 were: step aside on "takes aim", dash aside on "rears back", dash aside from nearby shots, swipe when close, otherwise walk toward the enemy. The exact script was not kept.

**B. "I swiped it and still got hit."**
- Room 2 grub: rears back about 2 tiles away. A swipe at 5.42 s missed (out of reach). A swipe at 5.92 s hit, and the player was hit at 5.95 s (2→1 hearts).
- Room 3 grub: swipe at 8.12 s, hit at 8.25 s.
- Room 5 brute: swiped during its wind-up ("shrugs off the swipe"), then hit at 7.05 s. The player understood this one.

The player could not tell from the frames why a swipe sometimes does not stop the lunge.

## Decisions already made

- D-002 and D-003: contact-edge graze and exact-reach rules.
- D-007: room 3 simultaneous cues accepted, in-flight bound.
- D-011: variant-named wind-up and hit messages.
- D-012: room 3 layout.

None is reopened here.

## Constraints

- Verify from the design documents, the acceptance criteria and the build. Do not change code or documents.
- Write reproducible scripts for every claim.
- Judge each item as one of: defect, readability failure (the build matches the design, but the player view does not show the cause), or matches design and is readable.
- A readability failure is not a defect; report it separately so the Studio can route it to Design or Review.

## Open questions

1. **Item A.** For each of the three room 4 hits, find what actually damaged the player.
   - Name the source: which spitter's shot, the runner, or the grub, and at what time.
   - Say whether `--view player` shows that threat (a cue, a shot or a lane) before the hit, and whether the post-hit frame or message identifies the source.
   - Check that dash invulnerability matches the design (`design/combat.md`) in each case. A hit about 0.8 s after a dash is only a defect if the dash window is wrong.
   - Reproduce with reaction rules like the player's. If you cannot reproduce them, say so and say what you tried.
2. **Item B.** Check each case against the late-swipe boundary and lunge rules (your report 56 and 64 found the boundary matches the design).
   - Does the swipe cancel only before the lunge starts, as designed?
   - Do the message lines in the player view make the order, "swipe landed" then "lunge hit", look like a contradiction? If so, is there any line that says why the lunge was not cancelled?
3. **Item C (bounded).** Build deterministic walk-and-swipe scripts from your report 86 traces.
   - Show R3-8 at 60 FPS: time from the previous kill to the room clear, against the 6 s limit.
   - Show a pure 1-tile sidestep within 0.4 s of the grub's cue in room 3, and the 30 FPS cancel and recovery swipe, if reachable.
   - If an item cannot be shown after this round, record it as unverified. **No further QA round will be opened for it**; it goes to Review as a known gap.

## Expected output

A report to `studio` (not to `gameplay-engineer`) with a verdict per item (A, B, C) and the reproduction scripts. A real defect needs a defect report with acceptance criteria. Say separately what is a readability failure.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md, studio/skills/verify-change.md
- Project: project.md, repo/manual.md, design/combat.md, design/combat-step72.md, design/combat-cues-visual-spec.md, the build in repo/ (sha 1ac4d04d0e75), goals/G-001-combat-monotony/86-qa-to-studio.md
- Decisions: decisions/D-002-contact-edge-graze-accepted.md, decisions/D-003-contact-edge-exact-reach-and-lunge-band.md, decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md, decisions/D-011-variant-named-messages-accepted.md, decisions/D-012-room3-standard-grub-and-closer-spitter.md
- Previous handoff: goals/G-001-combat-monotony/88-playtester-to-studio.md
