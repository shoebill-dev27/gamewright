---
kind: handoff
goal: G-003
seq: 13
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 13: studio → gameplay-engineer — Print the refusal for rule-driven dashes on the legacy route and apply the manual text

## Task

Make a refused dash print `dash not ready — …` on the legacy rule path too (and let `text "not ready"` fire on it). Apply the updated manual text from the spec. Do not touch any dash timing or game results.

## Context

Goal G-003: the Owner found it unclear when dash can be used again. A display was specified (design 04) and built (08). QA (10) found the display truthful at 60 FPS but failed it literally at 30 FPS and raised spec questions. The Game Designer settled them (design/dash-availability.md, D-029). The settled rulings only change a small part of the build:

- 30 FPS: the first accepted second dash is 0.90 s after the first one started (27 frames), not 0.85 s. The ±1 frame is measured against the frame-quantized value. The display already agrees with the build. This needs a manual wording change only, not a build change.
- Public-driver pictures: the public driver prints its usual event picture after accepted-dash and refusal messages. The legacy route prints none. Spec 3.3 and 3.5 are amended. No build change, but the manual says so.
- Rule-driven refusals: every refused dash prints `dash not ready — …`, whatever its source (scripted press, public-driver rule, legacy rule). `text "not ready"` may fire on it. This is the build change. It is suspected to be needed only on the legacy rule path.
- Rule-driven attacks that do nothing keep their current `(nothing happens)` behavior.
- Q3/Q4: a hit does not change the cooldown, the first accepted press is max(ready, hit + 0.3 s), and attack recovery does not block a dash. This is already how the build behaves; no change.

## Findings

Designer's report: `12-game-designer-to-studio.md` (previous handoff). The authoritative spec is `design/dash-availability.md`; the manual drop-in text is in it.

## Decisions already made

- D-001: no new inputs.
- D-028: the dash indicator shows on the legacy route too (including room 5).
- D-029: the four G-003 spec rulings above.

## Constraints

- Dash rules and timing unchanged (recovery 0.25 s, cooldown 0.6 s, invulnerability, inputs). Game results must not change.
- Both 30 and 60 FPS must play correctly.
- Prefer reusing existing systems (small team).
- If the legacy rule path cannot report the refusal without changing game results (events, timing, RNG, order), stop. Do not change results: hand back with outcome `question`, stating exactly what blocks it. The Designer will rule.
- Do not make judgments about the experience; report only what you built and observed.
- Budget is tight: one Build round is planned. Keep the change small.

## Open questions

- Can the legacy rule path print the refusal without changing results? Answer by building it or by stating the blocker.
- Report the source id (`repo/source_id.py`) before and after your change. The packet's build sha is `aa28af2ce710`; QA's earlier runs reported source id `b62005468da6`. These are probably two kinds of id; state what each tool reports so the Studio can confirm.

## Expected output

1. The build change and the manual changes:
   - Legacy rule path prints `dash not ready — …` for a refused dash; `text "not ready"` fires on it.
   - `repo/manual.md` carries the four changes from the spec's drop-in text: the 30 FPS dash line ("…0.85 s after the previous one started (60 FPS); at 30 FPS the frames make it 0.9 s"), the statement that rule-driven refusals print too, the note about event pictures in `mode` runs, and `text "not ready"` as usable. Update `repo/public-driver.md` if the spec's drop-in text covers it.
2. Tests for the new behavior: a refused dash from a legacy rule, from a public-driver rule, and from a scripted press. Also that periodic pictures stay on the 0.5 s grid, and that the accepted-dash timing at 30 and 60 FPS is unchanged. Run `python3 -m unittest discover -s tests` and report the count.
3. Same-code evidence for "no result changed": before editing, record trace-view output for a few scripts and bot runs. After editing, compare it. The game events must be identical apart from the new refusal lines. Report the scripts used and the outcome.
4. Report to `studio` (address the result to `studio`, not to QA or the Playtester): what changed, which files, test count, the source ids, and anything you could not do. Use outcome `done`, `question` (blocked as above) or `partial`.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/dash-availability.md, repo/manual.md, repo/public-driver.md, repo/game.py, repo/run_driver.py, repo/session.py, repo/source_id.py, repo/tests/test_dash_display.py, repo/tests/test_run_driver.py, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-028-dash-indicator-on-legacy-route.md, decisions/D-029-g003-spec-rulings.md
- Previous handoff: goals/G-003-dash-availability-clarity/12-game-designer-to-studio.md
