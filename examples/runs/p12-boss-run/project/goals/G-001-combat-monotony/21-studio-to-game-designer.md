---
kind: handoff
goal: G-001
seq: 21
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 21: studio → game-designer — Rule on the frame-rate-dependent graze, the shot cap, the walker margin and the doc contradictions

## Task

Answer four spec questions raised by QA's verification of build 0.5, in a ruling written for the Studio. The main one: is a frame-rate-dependent hit/miss at the contact edge acceptable in the text build? If not, state the rule precisely enough that `gameplay-engineer` can build it and QA can verify it.

## Context

Goal G-001 (combat feels monotonous). Build 0.5 implements your cues, variants and rooms (criteria 1–16). QA verified it independently (handoff 20). Criteria 1–15 and 16a–d pass. For 16e, the walker's 30/60 FPS differences are caused by bot decision timing, which is not a build defect (the exact cause is a float tie at the bot's 2.5 threshold in room 1). QA did find one scripted case where the game itself gives different outcomes at 30 and 60 FPS with identical input. QA does not decide whether that is acceptable, so it is yours. The Timing rule in the spec only guarantees "no tunnelling". The answer decides whether 16e passes as ruled (the verdict becomes pass) or the Build reopens. This is the first failure of criterion 16, so no technical-director re-plan is triggered.

## Findings

All facts below are QA's, from runs it made in step 20. Figures marked "derived" were calculated, not run.

### 1. Frame-rate-dependent graze (the main question)

- Shot reach is 0.4 tile. Contact is a distance check once per frame. A shot moves 0.1 tile per frame at 30 FPS and 0.05 at 60 FPS.
- Reproduction (`python3 play.py --view trace`, run at `fps 30` and at `fps 60`):

```text
room empty
fps 30            # and 60
spawn spitter 1.04 3.70
1.3 move up
1.4 stop
end 5
```

| Spitter position | 30 FPS | 60 FPS |
|---|---|---|
| (1.04, 3.70) | no hit, 3 hearts at 5 s | hit at 4.100 s, 2 hearts |
| (1.00, 3.70) | hit at 4.100 s | hit at 4.117 s |
| (1.00, 3.73) | hit at 4.100 s | hit at 4.117 s |
| (1.00, 3.76) | hit at 4.100 s | hit at 4.117 s |

- Cause: the first shot is locked on the player at (8, 4.0) at the cue start (1.2 s). The player then stands at (8, 3.6). The shot line passes the player at a perpendicular distance of about 0.3996, which is 0.0004 inside the reach. A hit needs a sampled frame within about ±0.017 tile of the closest approach. That window is narrower than the frame step at both rates, so which rate catches it depends on the phase.
- Size (derived): only a lateral miss within about 0.003 tile of the 0.4 reach is affected (the shot's step is 0.1 tile at 30 FPS and 0.05 at 60 FPS). Clearly closer always hits and clearly farther never does, at both rates. Grub lunges (reach 0.6, step up to 0.27 tile at 30 FPS) probably have a wider band, about 0.015 tile at 30 FPS. Grubs were not tested. QA rates severity low. The effect is a hit or a miss only and does not change timing.
- 16e says a build defect is "same decision, same time, same positions, different outcome". Read literally, this matches. QA did not decide.

### 2. Shot cap: limit on cue starts, or on shots in flight?

Criterion 11 says "never more than 3 in flight". In the practice-room trace `cap-four-spitters-60` (four spitters, no real room has this), the cap is checked only when a cue starts. Three spitters start cues at 4.6 s, and each check sees 2 shots in flight. At 5.2 s all three fire while the shots from 2.6 s and 3.4 s are still in flight, so 5 shots are in flight (QA's count; the trace shows hits at 5.3 s and 6.1 s). Room 3 (three spitters) stays ≤ 3 in the test. Which does the spec mean?

### 3. Walker margin in rooms 3–5 at 60 FPS

The walker at 60 FPS loses 2+2+2 = 6 hearts in rooms 3–5, the top of criterion 13's range (3–6). At 30 FPS it loses 0+1+3 = 4 and clears 2. One more heart lost would break 13. The dodger loses 0 and the camper clears 0, at both rates. Keep the margin as it is, or retune? (A tuning change is a Build.)

### 4. Contradictions between design/combat.md and design/combat-cues-visual-spec.md (QA reported them; no ruling yet)

- **Lunge line.** `combat.md` says a thin orange-red line for the lunge path. The visual spec draws a lane 1.2 tiles wide.
- **Spitter glow.** `combat.md` and the text view start the glow at 0%. The visual spec requires a floor of at least 30%.
- **Grub cue behaviour.** `combat.md` says the grub flashes for the whole wind-up. The visual spec says a steady tint with a slight pulse (no strobe, ≤ 3 Hz), and the lane stays at full strength until the lunge starts and fades during it. The text view removes the line when the lunge starts.
- **Text marks.** `combat.md` leaves the `r` / `G` marks open for the graphical build. The visual spec uses silhouette and size, which answers that open question.

These matter for a future graphical build, not for the text build. The visual points V1–V11 are already planned as a proposed new Goal at Close. State which document governs each point, or what the visual spec's author (`art-director`) must reconcile. Do not rule on visual style.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- Your rulings on criteria 13–16 and five spec defaults (handoff 14). Change them only if you say why.

## Constraints

- Stay within D-001, the vision pillars (one-button combat, short runs, readable threats) and the project constraints (30 and 60 FPS must both play correctly; small team, reuse existing systems).
- If a ruling would need a new enemy type, a healing system, a new input, or a scope change, hand back instead of ruling (it goes to `game-director`).
- Do not edit the game. A rule that you add must be checkable by QA at both frame rates, with player-observable acceptance criteria.
- If you accept the graze (question 1), record it as a known, accepted limitation of the text build and say what, if anything, must be re-checked in a graphical build.

## Open questions

1. Is the graze in Finding 1 acceptable? If yes, state it as accepted and name the sampling rule. If no, state the required behaviour (for example a swept contact test between frames, with the tolerance allowed between 30 and 60 FPS) and whether it also applies to grub lunges.
2. Is the cap a limit on cue starts (as built) or on shots in flight?
3. Keep or retune the walker margin at 60 FPS (criterion 13)?
4. Which document governs each contradiction in Finding 4?

## Expected output

A short ruling written into `design/combat.md` where it changes the spec, plus a handoff with `outcome: done`, addressed to `studio`. For each question give the ruling and, where the build must change, the acceptance criteria. Say clearly whether the build must change (Build for `gameplay-engineer`) or not (QA closes the open 30 FPS gaps and the verdict becomes pass).

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat.md, design/combat-cues-visual-spec.md, repo/manual.md, goals/G-001-combat-monotony/14-game-designer-to-studio.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/20-qa-to-studio.md
