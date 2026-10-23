---
kind: handoff
goal: G-001
seq: 23
from: studio
to: qa
stage: Verify
outcome: routed
---
# 23: studio → qa — Close the open checks on build 0.5 against the final criteria 1–17 and give the verdict

## Task

Verify build 0.5 (`repo/`) against the current acceptance criteria in `design/combat.md` (criteria 1–17, plus V12 for the text build). Run the checks listed under Findings, which close the gaps from your previous report (handoff 20), and give a verdict. Check at both 30 and 60 FPS where stated.

## Context

G-001 (combat monotony). You verified criteria 1–16 earlier: 1–15 and 16a–d passed, and you raised spec questions (frame-rate graze, shot cap, walker margin, document conflicts). The game-designer ruled on them and updated `design/combat.md`. The build has not changed. Gaps from your last run: criteria 5, 6 and 8 were only run at 60 FPS, and the edge case "a defeated spitter does not renumber the others" was not run.

## Findings

Rulings now in `design/combat.md` (read the spec for the exact text; this is a summary):

- **Contact sampling (D-002).** Contact is a distance check once per frame after that frame's movement; shot reach 0.4 tile, lunge reach 0.6 tile, no swept test. The accepted band is a lateral miss within 0.01 tile inside the reach for shots and within 0.03 tile inside the reach for lunges. Inside the band, 30 and 60 FPS may differ in hit or miss only (never timing or cue). Outside the band both rates must agree and follow the geometry: smaller than reach minus tolerance hits, reach or more never hits. Criterion 16e now says a difference caused only by this band is not a build defect.
- **Shot cap (criterion 11, reworded).** In rooms 1–5 never more than 3 shots in flight. The cap is on cue starts, so in a practice room with four or more spitters the bound is 2 + the number of living spitters.
- **Walker margin (criterion 13).** The numbers stay: walker 4 lost / 2 cleared at 30 FPS, 6 lost / 3 cleared at 60 FPS, upper limit 6; dodger 0; camper 0. A walker result of 7 would be reported as a tuning question, not a defect.
- **Governing documents.** For text-build behavior, `design/combat.md` and `repo/manual.md` govern. The visual spec governs only the look in a graphical build, so V12 stays open until one exists.

Checks to run:

1. Criterion 5, the two-swipe kill (6) and the variant swipe counts (8) at `fps 30`, using the existing practice-room scripts.
2. The edge case "a defeated spitter does not renumber the others".
3. Criterion 17 (edge checks). Take your reproduction script from handoff 20 and choose spitter positions from the trace:
   - shot lateral miss of 0.39 tile or less: a hit at both rates;
   - shot lateral miss of 0.40 tile or more: no hit at both rates;
   - one grub case on each side of the lunge band: 0.57 or less hits at both rates, 0.60 or more misses at both;
   - measure and report the actual lunge band at 30 FPS. If it is wider than 0.03 tile, report that as an open spec question for the game-designer, not as a pass.
4. Criterion 11 in its new wording: room 3 at most 3 in flight over your usual window; the four-spitter practice room within 2 + living spitters.
5. Re-run the unit tests (`run_tests`) and confirm that nothing else regressed.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- D-002: per-frame contact sampling is kept; the contact-edge graze is an accepted limitation of the text build.

## Constraints

- Must play correctly at 30 and 60 FPS.
- Verify from the spec, the criteria and the build, not from explanations of why it should work.
- Do not change the build or the spec. A failing criterion outside the accepted band goes to Build; a spec question goes to Design.

## Open questions

- Is the grub lunge band within 0.03 tile at 30 FPS (check 3)?
- Optional wording note for the Studio: `repo/manual.md` says "no more than 3 are in the air at once", which holds in rooms 1–5 but not in practice rooms with four or more spitters. Report whether you consider that misleading to a player. Do not edit the manual.

## Expected output

A pass/fail report per criterion (1–17, V12 status) with the figures measured. Verdict `pass` if all hold, with V12 noted as open until a graphical build exists. Address the result to `studio` (the next step is a playtest that must be composed without implementation history).

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md, repo/manual.md, repo/game.py, repo/bots.py, repo/play.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-contact-edge-graze-accepted.md
- Previous handoff: goals/G-001-combat-monotony/20-qa-to-studio.md
