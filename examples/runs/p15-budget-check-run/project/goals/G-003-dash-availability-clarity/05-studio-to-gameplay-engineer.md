---
kind: handoff
goal: G-003
seq: 5
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 05: studio → gameplay-engineer — Build the dash availability display (A+B+C) per spec

## Task

Implement `design/dash-availability.md` in `repo/`: the persistent dash status on every live picture (A), the dash messages and the `dash ready` event (B), the trace records, and the manual text (C, spec section 8, applied to `repo/manual.md`). Dash rules, timing and results must not change. Stop and hand back on any ambiguity; do not decide design.

## Context

Goal G-003 (Owner: 「ダッシュがいつまた使えるのか分かりにくい。分かるようにしてほしい」). Diagnose (02) found the cause is missing information: the player view has no dash state, a refused dash prints only `(nothing happens)`, nothing marks the return of dash, and the manual is silent. Design (04) produced the spec with player-observable acceptance criteria in seconds. Build is next; QA and an independent playtest follow.

## Findings

From the Design step (details and wording are in the spec, which is the source of truth):

- The 0.6 s cooldown starts when the dash ends (observed at 60 FPS: a dash at 0.500 is accepted again at 1.350, so 0.85 s start to start).
- A: every live picture ends with `dash: ready`, `dash: active` or `dash: <R> s`; R is the time until dash is usable, rounded UP to a tenth, so ready is never shown early.
- B: an accepted dash prints `you dash <dir> — usable again in 0.9 s`. A refused dash prints `dash not ready — <R> s left`, with `(dashing)` or `(hit-stun)` as the reason where it applies. `dash ready` is printed at the exact ready moment with an event picture, and only after a dash was used.
- Trace records: `dash_start`, `dash_end`, `dash_ready`.
- Wind-ups do not change the cooldown. Whether a hit changes it (Q3) and whether attack recovery blocks dash (Q4) are not confirmed. The display must follow what the build actually does; report what you observe for Q3, Q4 and the room-transition clear (Q5).
- D-028: the indicator also appears on the legacy route including room 5. Per D-027, G-002 is stopped, so rebasing its criterion L1 (ignore the dash field, dash text and `dash ready` lines) affects only historical comparisons; QA compares with those stripped (Q8).
- The periodic grid and `view-every` are unaffected; pictures and results are otherwise unchanged.

## Decisions already made

- D-001: no new input buttons.
- D-022: the legacy route stays limited; only the display is added.
- D-028: dash indicator on the legacy route, including room 5.
- D-027 (context): G-002 is stopped; its unfinished verification is not reopened here.

## Constraints

- No change to dash length, distance, invulnerability, the cooldown value or inputs.
- All timing in seconds; criteria hold at 30 and 60 FPS (±1 frame).
- Reuse the existing text view and message system; no new input.
- Game results must not change. Update existing tests and golden outputs only for the new field and text, and say which you changed. Run the project tests (`python3 -m unittest discover -s tests`) and report the result against the sha you build.
- Out of scope: dash invulnerability display, queued inputs.
- The Findings of 04 are a Designer's report, not a verification.

## Open questions

- Does the extra field or message break reaction-rule parsing, `public-driver.md` use, or bot input? If so, report it and hand back to `game-designer` (outcome `question`).
- If a spec case is ambiguous or contradicts the build (for example a cooldown that differs by situation in a way the spec does not describe), stop and hand back `question`; do not choose.

## Expected output

- The change in `repo/` and `repo/manual.md` with build notes: new sha, files changed, tests run and results, tests or goldens edited, and what you observed for Q3, Q4 and Q5.
- Address the result to `studio` (QA verifies next, then an independent playtest; the Studio composes those Handoffs).
- Write `outcome: done`, or `question` / `partial` as the contract requires.

## Sender assessment

Studio routing note only: the Design handoff reports the spec as complete apart from Q3–Q5, which are deliberately left to observation of the build.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/dash-availability.md, design/combat.md, repo/manual.md, repo/public-driver.md, design/final-boss-and-continuous-run.md#2-ランと入場, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-022-g002-v1-supplements.md, decisions/D-028-dash-indicator-on-legacy-route.md
- Previous handoff: goals/G-003-dash-availability-clarity/04-game-designer-to-studio.md
