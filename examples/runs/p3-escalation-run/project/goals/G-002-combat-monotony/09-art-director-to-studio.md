---
kind: handoff
goal: G-002
seq: 9
from: art-director
to: studio
stage: Design
outcome: done
---
# 09: art-director → studio — Visual cues for enemy telegraphs, charge lane, block and stun are designed

## Task

Merge this visual design with the Technical Director's plan (step 6a) and write the Build Handoff. Pass the open questions below to `game-designer` and the Technical Director.

## Context

Goal G-002 「戦闘が単調なので改善したい」, Option A (D-002). The Game Designer's spec in `design/combat-enemy-depth.md` left the visual cues undecided (its Q1). Handoff 07 asked for a visual design with player-observable readability criteria. No timings, damage, ranges or rules were changed.

## Findings

The full visual spec is in `design/combat-enemy-visuals.md`. In short:

- **One shared approach** for all four damaging attacks: a threat shape (outline plus fill that is full exactly when damage can begin), a lock change (thin dashed orange outline becomes thick solid red with a 0.1 s white-hot flash, and the locked state persists), and a rim pulse on the attacking enemy. Everything is driven by elapsed seconds, so it reads the same at 30 and 60 FPS.
- **Shapes tell attacks apart even in grayscale:** Grub is a short arrow-rectangle, Spitter is a thin aim line with a reticle, Charger is a 1-tile-wide lane with chevrons and an end-cap bar, Shieldbearer bash is a wedge.
- **Lock moments:** Spitter at 0.4 s of 0.6 s, Charger at 0.5 s of 0.8 s (lane rotates and updates before, fixed after), Shieldbearer bash drawn locked from the start, Grub at the end of the telegraph.
- **Palette rule:** saturated orange/red appears only on active threats. Non-threat information (Shieldbearer guard plate, block cue, stun sparks, guard-down opening) uses cold steel/cyan-white, so "hot = danger, cold = opening".
- **Lantern vs threat:** the lantern is a soft, amber, edge-less glow. Threat shapes are hard-edged, saturated, drawn above the lighting pass (so they show in the dark), and have a dark keyline for lit floor.
- **Room 5:** at most 2 threat shapes at once (D-003). Fills are alpha-capped at 35 %, outlines are opaque, and the Charger lane draws underneath. Waiting and recovering enemies show no orange/red.
- **Block cue:** steel-white spark ring at the contact point plus a plate flash, 0.2 s, with a distinct clank sound. **Stun cue (1.5 s):** tilted low sprite with circling steel sparks that blink faster in the last 0.3 s. **Open recovery (0.8 s):** only a dimmed sprite and a dust puff.
- **Acceptance:** VC1–VC14 (QA checks at both frame rates, including contrast ≥ 3:1, lock timing ±0.05 s, shape matches hit area, no strobing) and VE1–VE5 (experience signals for Review; do not put these in the Playtester's handoff).

## Decisions already made

- D-001: one attack button plus dash; no new buttons.
- D-002 (Owner): enemy-side depth only; no hold-to-charge attack.
- D-003: time-based telegraphs with a 0.4 s floor; at most 2 simultaneous attackers.

## Constraints

- Do not change specified timings, damage, ranges or rules. The questions below ask for confirmation or a change by the owning Role.
- Scope: the 5-room slice only.
- Hit areas and cue geometry must come from the same data (cost flag F7).

## Open questions

1. **For `game-designer` (N1, worth routing before Build):** the Grub's direction locks at the end of its 0.5 s telegraph and the lunge takes 0.15 s, which leaves almost no reaction time after the lock. Is that intended? If not, the lock point should move earlier (for example 0.2 s before the lunge, like the Spitter). The visual works either way.
2. **For `game-designer` / `technical-director` (Q-A, Q-B):** Spitter projectile range, and the real widths and angles of the Grub lunge, the Spitter line and the Shieldbearer bash cone. The visual spec assumes about 1 tile wide for the Grub and about 90° for the cone, and will follow the real hit areas.
3. **For `technical-director` (F1–F7):** check that a shared threat-shape renderer with three masks and a chevron texture is cheap, that an outline/rim effect on enemy silhouettes is available (fallback: pre-baked brighter outline sprites), the draw cost of an 8-tile lane plus 2 shapes plus projectiles at 30 FPS, that cue states come from enemy state and phase time (not animation frames), and that the cue is on screen at least one rendered frame before damage. Also check whether the slice has audio support for the single block "clank" sound; if not, drop only the sound part of VC7.
4. **For the Build step (F6):** check existing enemy sprites for saturated orange/red accents. These would conflict with the reserved-color rule and need a small recolor task.
5. **For the Studio:** link `design/combat-enemy-visuals.md` in the `project.md` Design index next to `design/combat-enemy-depth.md`.

## Expected output

A Build Handoff written by the Studio, combining the Technical Director's plan with `design/combat-enemy-visuals.md`. The Build Handoff should include the acceptance criteria VC1–VC14 for QA. Later, the Art Director's visual review of the build checks VC1–VC14 and VE1–VE5 (the VE items stay out of the Playtester's handoff).

## Sender assessment

Confidence: medium-high that the shared shape + lock + rim approach keeps room 5 readable, because the attack limit of 2 caps the on-screen shapes. Main risks: (a) the Grub lock timing (question 1), which is a rules issue, not a visual one; (b) the colors are proposed values and need a check on real captures for the 3:1 contrast criterion in lit areas; (c) the steel-colored cues might get lost beside the lantern's pale light, which visual review should confirm.

## Load

- Role: none (Studio routing)
- Skills: none
- Project: design/combat-enemy-visuals.md, design/combat-enemy-depth.md, project.md#art-direction
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-enemy-side-combat-depth.md, decisions/D-003-time-based-telegraphs-and-attack-limit.md
- Previous handoff: goals/G-002-combat-monotony/07-studio-to-art-director.md
