---
kind: handoff
goal: G-001
seq: 11
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 11: studio → gameplay-engineer — implement the level 1 opening spec (retry after spec gaps were settled)

## Task

Implement the whole Level 1 opening spec in `design/onboarding.md` for build 0.3 (the next build after 0.2, level 1 only). State the change exactly in your outgoing Handoff: what changes, where, and how to exercise it. Stop and hand back a `question` if you find another gap.

## Context

Goal G-001. Owner request (verbatim): 「最初のパズルで子どもが手を止めてしまう。直したい」. Success condition: children aged 7–10 playing level 1 begin purposeful touch interaction on their own, without a long pause and without an adult explaining.

You held Build earlier (Handoff 09) because the spec did not define a non-pool touch during the intro, the intro's relation to undo, and minor points Q3–Q6. The game-designer has settled all six in `design/onboarding.md` (Handoff 10), and `decisions/D-002-intro-cancel-and-undo.md` records the main ruling. Nothing was built before this step.

## Findings

Settled answers to your questions (the spec text is authoritative; this is a summary):

- **Q1, intro cancelled by a touch on the crab, home or sand:** the pool eases back to its authored start position in a fixed 0.15 s, then the idle pulse starts there. The touched object responds at once (within 0.1 s). The redirect pulse starts when the ease-back ends, 0.15 s after touch-down, so the "within 0.2 s" criterion is unchanged.
  - A touch on the pool during the ease-back cancels it, and the pool follows the finger from its current position.
  - A touch on the pool during the intro cancels the intro, and the pool follows the finger from where it is. The pool's hit area follows its drawn position during the intro.
- **Q2, intro and undo:** the intro is a visual offset only and never enters the undo history. The logical position is the authored start until a real drag is dropped. Undo returns to the authored start.
- **Q3:** the crab flips horizontally to face the pool side, plus the ±8° wiggle. No flip if it already faces that side.
- **Q4:** distance is measured center to center, using the pool's at-rest width. The home glow applies only while the pool is being dragged, so a pool at rest after the intro or ease-back never triggers it.
- **Q5:** touch-down on the pool cancels a running redirect pulse, and the 1.10 lift applies from the current scale.
- **Q6:** "Build 0.3" means the next build after 0.2, level 1 only.
- **Reduced motion:** the spec keeps the static-brightness fallback, and the intro is skipped there, so the intro-cancel case does not arise. Read the OS flag where it exists; add no in-game toggle.
- **Home styling:** your plan (scenery outline style, no idle animation) satisfies rule 4. It is checked on a real capture at Verify.

New or changed QA checks, so you can design for them: check 11 (intro cancelled by a non-pool touch, with timings), check 12 (undo after an intro-cancel returns to the authored start and adds no extra step), and check 7 reworded to the pool-touch cancel case. The spec lists all 12 checks.

## Decisions already made

- D-001: no failure, no timers, every move undoable. Do not add a timer, an inactivity trigger or an irreversible step.
- D-002: intro cancel eases the pool back in 0.15 s; the intro is never in the undo history.
- Idle hint (Option C) is excluded from the spec. Do not add one.

## Constraints

- Level 1 only. Existing sprite sheet only (tint, recolor, flip, scale, rotation, position and brightness changes are allowed).
- Touch only. No mechanic may depend on reading text.
- Dry-run project: `sim/repo-notes.md` stands in for the code. A change counts as made when you state it exactly in your Handoff.
- If the change turns out not to be local to level 1, hand back for Plan (`technical-director`) per the return rules. If you find a further spec gap, hand back `question` to `game-designer`; do not decide it yourself.

## Open questions

- Whether iOS "Reduce Motion" and Android "Remove animations" exist on the target platforms is unconfirmed. This does not block Build. The Studio assigns the check to `qa` at Verify, and the static-brightness fallback works either way.
- Home's current styling needs a real capture at Verify (check 3).

## Expected output

Your outgoing Handoff has `outcome: done` and covers the whole Level 1 spec: every rule, edge case and settled answer above. State exactly what changes, where, and how to exercise each of the 12 checks. Address the result to `studio`, so the Studio can send it to `qa` for Verify without your Sender assessment and then compose a fresh Playtester handoff from permitted information only. If blocked, hand back `question` to the Role that can answer.

## Sender assessment

None (written by the Studio at routing).

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, project.md#art-direction, design/onboarding.md, sim/build-0.2.md, sim/repo-notes.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-002-intro-cancel-and-undo.md
- Previous handoff: goals/G-001-first-puzzle-stall/10-game-designer-to-studio.md
