---
kind: handoff
goal: G-001
seq: 33
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 33: studio → game-designer — Specify Options 1 and 2 from your second Diagnose, plus manual wording

## Task

Write the design spec (`write-design-spec`) for the changes your Diagnose (handoff 31) recommended as "do": Option 1 (breathing room in spitter rooms 4–5) and Option 2 (the brute's wind-up swipe does not cancel its lunge). Decide yourself whether Option 3 (room 2 spitter) belongs in this slice. Also settle the manual wording items below.

## Context

G-001 (combat monotony). Build 0.5 passed QA (criteria 1–17). The fresh playtest (27) still found monotony: melee enemies share one answer and rooms 4–5 crossfire feels unfair. Your Diagnose (31) ranked the options; the Studio found no Decide needed because all options stay inside D-001 and the pillars. A parallel QA step (handoff 34) is tracing spitter fire times in rooms 3–4, because the playtest said "in sync" and "opposite corners", which conflicts with the spec. That result arrives after this step.

## Findings

- From 31: S1 (melee share one answer) is the core cause of "monotonous". S4 (rooms 4–5 crossfire) is the most important problem: the next cue locks 0.2 s after the previous one ends, at the position the player dodged to. Options 1 and 2 are independent and can be built together.
- From 32 (QA, room 2): the "grub hit right after a swipe" was not a defect. The swipe landed after the 0.5 s wind-up had ended, so the lunge continued, which conforms to `design/combat.md`. `repo/manual.md` says "swipe it (within 1.5 tiles) to cancel the lunge" without saying this works only during the warning. QA asks whether the manual should say so; this is a wording question, not a rule change.
- Known manual item: "no more than 3 in the air" is true in rooms 1–5 only.
- Runner and brute behavior for a human, and the real crossfire experience, are unconfirmed by scripted evidence; a hand-timed playtest will follow the Build.

## Decisions already made

- D-001: attack and dash only; no new input.
- D-002, D-003: per-frame contact sampling, graze accepted, exactly the reach is inside the band.

## Constraints

- Stay inside D-001 and the pillars (one-button combat, short runs 15–20 min, readable threats); reuse existing systems; correct at 30 and 60 FPS.
- Keep lane geometry identical across variants (visual spec); if a change needs presentation work, name it for the `art-director` rather than styling it.
- Make Option 1 robust whether or not the spitters currently fire together: state the required gap between cue windows as a rule in the spec, with player-observable criteria, and do not depend on the "in sync" claim.
- Every new or changed criterion must be checkable by scripts or bots at 30 and 60 FPS. Say which existing criteria change (for example 6, 8, 13, 14) and re-derive the affected bot expectations, flagging any you cannot verify without running the bots.
- Wording of `repo/manual.md` is player-facing text that ships with the build: give the exact lines to add or change (swipe cancels only during the warning; the brute rule if Option 2 is taken; the "3 in the air" scope). The Build step will apply them.

## Open questions

- Include Option 3 in this slice or defer it? Your call; say why.
- Does the Option 2 change need any signal to the player beyond the manual (for example a cue-text line)? If it does, name it as an item for the `art-director`.
- If you find the changes need a new enemy type, healing, new input, or a scope or priority change, stop and hand back to the Studio for a Decide step.

## Expected output

Update `design/combat.md` (and the visual spec only if needed), then write a handoff addressed to `studio`: the rulings, the changed and new criteria, the exact manual wording, whether Build is needed (expected yes), what QA must verify, and anything the Playtester should be asked to focus on without revealing the expected result. Record a Decision only if a real alternative was rejected.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat.md, design/combat-cues-visual-spec.md, repo/manual.md, project.md#vision, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-contact-edge-graze-accepted.md, decisions/D-003-contact-edge-exact-reach-and-lunge-band.md
- Previous handoff: goals/G-001-combat-monotony/31-game-designer-to-studio.md (also read goals/G-001-combat-monotony/32-qa-to-studio.md for the manual wording question)
