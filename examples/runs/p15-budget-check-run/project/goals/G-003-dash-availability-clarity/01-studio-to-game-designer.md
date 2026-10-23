---
kind: handoff
goal: G-003
seq: 1
from: studio
to: game-designer
stage: Diagnose
outcome: routed
---
# 01: studio → game-designer — Diagnose why "when dash is usable again" is unclear

## Task

Find out what the build currently tells the player about dash availability and why the player still cannot tell when dash can be used again. Write a diagnosis with options, in player-observable terms (skill `diagnose-experience`).

## Context

The Owner's report (verbatim): 「ダッシュがいつまた使えるのか分かりにくい。分かるようにしてほしい」

Goal G-003: a player using only what the build shows can tell whether dash is available now and, when it is not, when it will be again. The Owner's report is the first-hand observation, so there is no separate Observe step. The cause is not yet known, and the Project Context does not say whether the build shows dash state at all.

The project is a headless text build, played through input scripts. Commands, run from `repo/`:

- Play (player view): `python3 play.py --view player {script}`
- Trace (state view): `python3 play.py --view trace {script}`
- Tests: `python3 -m unittest discover -s tests`

The script format is in `repo/manual.md`. The current build sha is dc0138c2b6d1. The tests have not been re-run at this sha.

## Findings

Nothing yet. This is the first step. The Studio did not open design documents or the repository (Intake loads only the project overview). Establish the facts yourself:

- What the player view and messages show about dash: use, recovery, readiness, and any indicator.
- What `design/combat.md` and `repo/manual.md` say about dash recovery and readiness.
- Whether the player view tells the player the recovery time or the moment of readiness. Compare what the trace view knows with what the player view shows.

## Decisions already made

- D-001: Combat uses one attack button plus dash. No new input buttons beyond attack, dash and pause without Owner approval.

## Constraints

- Work only from player-visible output for the experience finding. The trace view may confirm the cause but is not what the player sees.
- Keep the dash rules as they are (recovery length, invulnerability). If every workable option needs changed dash timing or rules, say so as a direction question for `game-director` and do not choose it yourself.
- No new input buttons (D-001).
- The solution must work at both 30 and 60 FPS, so describe timing in time, not frames.
- Reuse the existing text view and message system where possible (small team).
- Do not edit the build or the design documents in this step.
- No numeric thresholds or acceptance criteria yet. Those belong to Design.
- Record anything unrelated that you notice as a proposed future Goal, not as scope.

## Open questions

- Is the problem missing information, late information, or ambiguous wording or placement?
- Is it the same in every situation (just after a dash, during enemy wind-ups, after a room transition or a hit), or only in some?
- Does the manual explain the dash recovery, and is it consistent with what the player view shows?

## Expected output

A diagnosis, in Findings of your outgoing Handoff:

- The cause or causes of the unclarity, each tied to the player-visible output it comes from.
- Two to three solution options in player-observable terms, with the trade-offs of each.
- Your recommended option.
- Whether any option needs a `game-director` decision. State this explicitly: it determines whether the tentative Decide stage runs.
- Whether you need a first-hand play observation to settle the cause.

Address the result to `studio`, so the Studio can route it.

## Sender assessment

The Studio expects this to be a display or message change, not a rules change. It has not read the repository, so this is a guess; the diagnosis may overturn it.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/diagnose-experience.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, project.md#current-state, design/combat.md, repo/manual.md, repo/public-driver.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: none
