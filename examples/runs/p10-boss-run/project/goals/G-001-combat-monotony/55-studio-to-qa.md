---
kind: handoff
goal: G-001
seq: 55
from: studio
to: qa
stage: Observe
outcome: routed
---
# 55: studio → qa — Reproduce three player-reported unfair-feeling hits (late swipe vs lunge; hit with no visible cue)

## Task

Using the build in `repo/`, try to reproduce the three moments below, then decide for each whether the build matches the design documents and manual (not a defect) or contradicts them (defect, with a precise report and acceptance criteria). Also check one wording point (item 4).

## Context

Goal G-001 (combat feels monotonous). A fresh playtester played rooms 2–5 at 60 FPS through the player view with hand-written reaction scripts. They reported three hits that felt unfair or unexplained. An earlier, similar case (a room 2 grub hit after a swipe) was ruled not a defect in step 32; your report should say whether these differ from that case. Experience judgments (monotony, fun) are out of your scope; report only whether behavior matches the documents.

## Findings

Reported by the playtester (observations only, times in seconds of play):

1. **Room 2, late swipe at a rearing grub (about 4.0–4.25 s).** A grub reared back with a 0.5 s warning. The player swiped at the last moment (about 0.05 s left) and was hit anyway at 4.25 s. The manual says a swipe within 1.5 tiles cancels the lunge. Question: should a swipe this late have stopped it? Is "was in range, swipe landed, grub needs more than one swipe" the explanation?
2. **Room 5, swipe at a rearing grub (about 8.35–9.03 s).** A grub reared back (0.5 s warning). The player swiped once at 8.93 s (a hit) and the grub's lunge hit the player at 9.03 s, taking the last heart. The player thought the grub needed two swipes. Question: does the build behave as the documents say, including blocked-contact and lunge rules (see D-005)?
3. **Room 2, hit at about 5.4 s with no cue seen.** A runner was swiped and killed at about 5.0 s, then a grub hit the player at 5.4 s. The player saw no "rears back" line before it. Question: was there a cue (and was it printed in the player view), or did a hit land without the warning the design requires?
4. **Wording.** The line "A grub rears back" was reported as printed for runners and brutes too, distinguishable only from the `cue:` line ("r", "g", "G"). Check what the design documents and manual say the message should be for each enemy; report any mismatch.

Scripts used (play with `python3 play.py --view player {script}`, then `--view trace` to explain; reproduce at 60 FPS and 30 FPS):

Room 2 cautious (items 1 and 3), with `end 16`:
```
room 2
end 16
when see * coming within 1.5 then move aside
when text "rears back" then move aside
when see r within 1.4 then attack
when see g within 1.4 then attack
when see G within 1.4 then attack
when see G within 3 then move away
when see r within 3 then move away
```

Room 5 cautious (item 2), with `end 16`:
```
room 5
end 16
when see * coming within 1.5 then move aside
when text "rears back" then move aside
when text "takes aim" then move aside
when see r within 1.4 then attack
when see g within 1.4 then attack
when see G within 1.4 then attack
when see G within 3 then move away
when see g within 3 then move away
```

If the exact moments do not recur from these scripts, write your own input script that puts the player in the same situation (a swipe in the last 0.1 s of a grub's wind-up) and report what you ran.

## Decisions already made

D-005: a contact blocked by invulnerability consumes the shot and spends the lunge's hit. D-002/D-003: contact-edge sampling and exact-reach rules. Other Decisions in the Load list apply as written.

## Constraints

- Verify against the design documents, manual and Decisions; where they are silent or contradict each other, report the gap as "expected behavior undefined" (goes to Design), do not invent a rule.
- Do not change the build.
- Run `python3 -m unittest discover -s tests` first and report the result.

## Open questions

- Is the hit at about 5.4 s in room 2 preceded by a printed cue? (item 3)
- Does the manual state clearly enough to a player whether a late swipe cancels a lunge, and how many swipes a grub takes? If not, say so; that is a wording question for Design, not a build defect.

## Expected output

A report in the handoff template: for each of items 1–4, reproduced yes/no, what happened (times, hearts, enemy state), the governing document line, and the verdict (matches / defect with severity and acceptance criteria / undefined). Address the result to `studio`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md, design/combat-cues-visual-spec.md, repo/manual.md, the build in repo/ (run commands in project.md)
- Decisions: decisions/D-002-contact-edge-graze-accepted.md, decisions/D-003-contact-edge-exact-reach-and-lunge-band.md, decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Previous handoff: goals/G-001-combat-monotony/53-playtester-to-studio.md (observations only); similar earlier case: goals/G-001-combat-monotony/32-qa-to-studio.md
