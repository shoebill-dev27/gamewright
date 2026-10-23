---
kind: handoff
goal: G-003
seq: 9
from: studio
to: qa
stage: Verify
outcome: routed
---
# 09: studio → qa — Verify the dash availability display (criteria P1–P12, Q1–Q12) at 30 and 60 FPS

## Task

Verify the built change against the acceptance criteria in `design/dash-availability.md` (sections 5 and 6: P1–P12 and Q1–Q12). Run every applicable check at both 30 and 60 FPS. Give a pass/fail verdict per criterion, and an overall verdict. Report any regression.

## Context

Goal G-003: the Owner said it is unclear when dash can be used again. Diagnose and Design are done, and the spec is `design/dash-availability.md` (D-028). Build has now changed the player-facing display. Dash rules, timing, inputs and game results must stay identical (Q8). Verify the build from the spec, the criteria and the running build.

## Findings

Surfaces that changed, to exercise (what, not why it should work):

- **Legacy route, player view:** the `[t s] hearts n/3` line ends with a `— dash: …` field. Event text covers an accepted dash (`you dash <dir> — usable again in …`), a refused dash (`dash not ready — <R> s left`, optionally `(dashing)` or `(hit-stun)`), and `dash ready`. A `dash_ready` event is logged once per dash.
- **Legacy trace view:** the state line gains `dash_cooldown=`.
- **Public driver (`mode run` / `mode room`):** the status line carries the dash field while the state is `combat`, including when paused. A `text "dash ready"` rule is available.
- **`repo/manual.md`:** the Dash line, a `Dash status` section and a `text "dash ready"` example.
- **Tests:** a new `tests/test_dash_display.py`. Do not rely on it as evidence. Verify independently.

Points to confirm or decide on observation, with a verdict for each:

1. **Pictures in the public driver.** Spec 3.3 says the accepted-dash and refusal messages get no extra picture. Check what the public driver prints for these messages, and whether it contradicts the spec. State it plainly as a difference or as conforming.
2. **Quiet refusals.** Check whether `text "not ready"` fires for refusals from scripted presses and whether refusals from held-button reaction rules are silent. Compare this with what the spec and manual promise.
3. **Other ignored inputs.** They should still print `(nothing happens)`.
4. **Open observations, Q3–Q5 (record what you see; do not assume).**
   - Q3: a hit taken during the cooldown.
   - Q4: attack recovery against a dash.
   - Q5: room-transition and room-entry state.
5. **Q7.** The displayed state, the `ready` reading the bots use, and the actual acceptance of a press must agree, including at 30 FPS and under float residue.
6. **Q8.** Compare game results against the old outputs (or a run with the dash field, dash text and `dash ready` lines and pictures stripped). Results must be identical. If no earlier build exists, say so and use the strongest available comparison.

## Decisions already made

- D-001: no new inputs (attack, dash, pause only).
- D-028: the dash indicator is shown on the legacy route too, including room 5.
- D-027: G-002 is stopped, so its unfinished verification is out of scope here.

## Constraints

- Both 30 and 60 FPS apply (project constraint). Timing tolerance is the spec's (about ±1 frame).
- Run the build through the project's commands only: tests `python3 -m unittest discover -s tests`, play `python3 play.py --view player {script}`, trace `python3 play.py --view trace {script}`, bots `python3 bots.py {script}`, all from `repo/`.
- Build under test: `repo/`, sha aa28af2ce710 as stated in the packet. Record the source id your run reports.
- Do not change the game or the spec. A fault goes back as a defect report. Behavior the spec does not define goes back as an open question.

## Open questions

- The behaviors in points 1–2 and the Q3–Q5 observations above need a QA verdict. If the spec is silent or contradictory on any, say so exactly.

## Expected output

A verification report in Findings of your outgoing Handoff: per-criterion pass/fail with the script or command used, FPS, and the evidence, plus regressions and unverified items with the reason. Address the result to `studio`, because the independent Play step follows and the Studio composes its Handoff. Set `outcome` to `pass` or `fail`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/dash-availability.md, repo/manual.md, repo/public-driver.md, project.md#constraints, build in repo/ (run commands in project.md)
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-028-dash-indicator-on-legacy-route.md
- Previous handoff: none (the Build report holds the implementer's reasoning, which QA must not receive)
