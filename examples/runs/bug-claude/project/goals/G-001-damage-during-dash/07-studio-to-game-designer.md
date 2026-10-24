---
kind: handoff
goal: G-001
seq: 7
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 07: studio → game-designer — Rule on the frame-rate tolerance at protection-expiry boundaries (criterion 6)

## Task

Decide what "same results at 30 and 60 FPS" means for the moment protection ends (the end of a dash, or the 0.8 s post-hit mark), and state it as a player-observable rule with a tolerance QA can verify. Record it in `design/combat.md`, and also as a Decision if it constrains work beyond this Goal.

## Context

Goal G-001 (Owner's report): "ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。" The player took damage partway through a dash that started shortly after a hit. `design/combat.md` already says the player is invulnerable for the full dash duration. Build 0.4 fixes the defect. QA verified acceptance criteria 1–6 (from `02-qa-to-gameplay-engineer.md`; the criteria are unchanged). Criteria 1–5 pass at 30 and 60 FPS, including the original reproduction. Criterion 6 ("same results at 30 and 60 FPS") could not be decided, because neither the criterion nor the design gives a tolerance for the case below. QA may not redefine the criterion, so the question comes to you.

## Findings

From QA's report (`06-qa-to-studio.md`):

- The build says behavior is the same at both frame rates apart from one edge-timing difference. Exact wording in `sim/build-0.4.md`: "protection ends on the first frame at or after its end time. At 30 FPS that can be up to about 33 ms late, and at 60 FPS up to about 17 ms late. So a contact landing within one frame of an end time can go either way depending on frame rate. This is not visible in normal play."
- Protection ends late, never early, so it cannot cause damage inside the 0.25 s dash. Criteria 1 and 2 are unaffected.
- The affected case is a contact in the single frame just after a protection end time: the dash end, or the 0.8 s post-hit expiry. The result can differ between 30 and 60 FPS.
- `design/combat.md` gives no frame-rate or tolerance rule for this.

## Decisions already made

- D-001: one attack button plus dash. No new inputs. This is not at stake here.

## Constraints

- Must play correctly at both 30 and 60 FPS (`project.md#constraints`).
- Small team: prefer rules that reuse existing systems.
- Stay within the current dash and damage design (full-duration dash invulnerability, 1 heart per hit, 0.3 s hit-stun, invulnerable until 0.8 s). Changing those rules as a design improvement is out of scope for G-001.
- The vision pillar "Readable threats" and the player-facing intent in `design/combat.md` still apply.

## Open questions

1. Is a one-frame difference at a protection-expiry boundary acceptable under "same results at 30 and 60 FPS"? If yes, state the tolerance in player-observable terms (for example, which direction it may differ and by how much) so QA can verify it against the build. If no, state the intended behavior (for example, whether expiry must be time-exact and independent of frame rate) so the engineer can build to it.
2. Does the answer apply to both expiry boundaries (the dash end and the 0.8 s post-hit mark) and both enemy types, or does it differ?
3. If your answer would change the dash or damage rules, or touches the vision or scope, say so and hand back for `game-director` rather than deciding it.

## Expected output

- A ruling on criterion 6, written into `design/combat.md` as a short rule with a player-observable acceptance criterion, and a Decision if it constrains later work.
- Your outgoing Handoff addressed to `studio` (not directly to `qa` or `gameplay-engineer`), so the Studio can recompose the next step. The outcome should be `done` with the ruling in Findings, or `question` if you hand back.
- The Studio then routes Verify to `qa` for the final verdict if the difference is accepted, or Build to `gameplay-engineer` if expiry must change.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md, studio/skills/make-decision.md
- Project: project.md#constraints, design/combat.md, sim/build-0.4.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-damage-during-dash/06-qa-to-studio.md
