---
kind: handoff
goal: G-003
seq: 1
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 01: studio → game-designer — specify how the player can tell when dash is available again

## Task

Find out what the player view currently shows about dash availability and what rule governs when dash can be used again. Then specify, in player-observable terms, how the game should make "dash is usable now / usable again at X" clear, with acceptance criteria.

## Context

G-003. Owner request (verbatim): 「ダッシュがいつまた使えるのか分かりにくい。分かるようにしてほしい」. Success: the player can tell from what the game shows whether dash is usable and, if not, when it will be again. This is an experience (readability) problem. No reproduction or playtest has been run. Observe and Decide were skipped, and Plan is skipped unless your spec says otherwise.

## Findings

Nothing found yet. The Project Context does not state the dash rule, so confirm it from `design/combat.md`, `repo/manual.md` (what ships to the player) and, if needed, the build. Run the build with `python3 play.py --view player {script}` or `--view trace {script}` from `repo/`. Look at how the player view, the manual and any messages communicate dash state.

## Decisions already made

- D-001: Combat uses one attack button plus dash. No new input buttons.

## Constraints

- Make the existing rule visible. Do not change dash's rules or numbers unless readability cannot be achieved otherwise. In that case, list it as an option and hand back to the Studio rather than deciding a rule change that alters combat feel.
- Must work correctly at 30 and 60 FPS.
- Small team: reuse existing display and state.
- Threats must stay readable (vision pillar 3). The new cue must not hide or crowd out warnings.
- The build is text-based and played through input scripts. Acceptance criteria must be checkable that way.

## Open questions

- What is the current dash rule (limit, duration, what resets it)? Is the state shown anywhere today?
- If a rule detail (such as a hidden timer or an edge case) is what makes it unclear, is that a display problem or a rule problem?

## Expected output

1. A short diagnosis (what the player sees now and why it is unclear), written in the Findings of your outgoing Handoff.
2. A design spec as a project file, `design/dash-readiness.md`. Write it in player-observable terms. Include the cue wording or format for each state, when each state is shown, the behavior at 30 and 60 FPS, the `repo/manual.md` text changes, and acceptance criteria that QA and a Playtester can check from the script and player views.
3. Name any case that would need a rule change or a direction choice, so the Studio can route Decide.
4. The outgoing Handoff goes to `gameplay-engineer` (Build) when the spec is complete. If it needs a direction choice, hand back to the Studio's route with `to: game-director`, per your contract.
5. Say in the Build step's Expected output that the engineer's result should be addressed to `studio`, so a Playtester can later receive a clean Handoff.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/diagnose-experience.md, studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, design/combat.md, repo/manual.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: none
