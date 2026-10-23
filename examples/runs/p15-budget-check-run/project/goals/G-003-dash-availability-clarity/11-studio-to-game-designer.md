---
kind: handoff
goal: G-003
seq: 11
from: studio
to: game-designer
stage: Design (return from Verify)
outcome: routed
---
# 11: studio → game-designer — Rule on the 30 FPS tolerance, public-driver pictures and rule-driven refusals

## Task

Settle the open spec questions QA found, in `design/dash-availability.md`. For each answer, say whether the build or only the manual and criteria change. Do not change dash rules (recovery length, invulnerability, input set).

## Context

Goal G-003: the Owner said it is unclear when dash can be used again. Design (04) specified a ready/cooldown field and messages. Build (08) implemented them. QA verified (10): the display is truthful, and the 60 FPS timings are within spec. Verify failed on the criteria below because the spec is silent or cannot be met as written.

## Findings

Read the QA report, `10-qa-to-studio.md`, for the evidence. The questions it raises:

1. **30 FPS tolerance (fails P6, P7, Q2 literally).**
   - At 30 FPS the first accepted press after a dash is 0.9 s after the previous start, not 0.85 s. Ready is shown at 1.500, not 1.45.
   - The cause is frame quantization of the dash length and cooldown. The display agrees with the build.
   - The spec's section 2 says the 30 FPS ready time was "not confirmed".
   - Is the ±1 frame tolerance measured against the nominal 0.85 s (which fails), or against the frame-quantized value? What should the manual line "0.85 s after the previous one started" say for 30 FPS?
   - Changing the timing itself would break Q8 and is outside this Goal.
2. **Public-driver pictures.** Spec 3.3 says no extra picture for the accepted-dash and refusal messages. The public driver prints one event picture after each such message, as it does after swipe-miss and `(nothing happens)`. Amend the spec, or require suppression? Note the cost: one picture per refused press counts as event output under Q10.
3. **Rule-driven refusals.**
   - Scripted presses and a public-driver rule print `dash not ready — …`.
   - A legacy held rule (`when nothing within 20 then dash right`) is refused silently, and `text "not ready"` never fired.
   - Two issues are mixed in this observation: legacy vs public, and action type. The spec (3.4) and the manual are silent.
   - Should a rule-driven refusal print, and may `text "not ready"` fire on it?
4. **Q8 and Q12 have no baseline.** There is no earlier build and no strip tool, so "identical to before" cannot be byte-compared. Say what evidence the criterion should accept. D-024 handled the same problem for G-002 and is a precedent to look at, not a rule.
5. **Recorded as observed, no change asked unless you want one:** Q3 (a hit does not change the cooldown) and Q4 (attack recovery does not block dash).

Items QA could not verify (Q5 room-entry reset, Q7 across bot runs, the 1-frame-before press at 60 FPS, P12 for dodger bots) stay open for a later QA round. In your output, say which of them need a Build change and which need only a better script or evidence method.

Build identity: QA's runs report source id `b62005468da6`, and the packet names sha `aa28af2ce710`. `project.md#current-state` also lists a sha and a source id with different values. They are probably two kinds of id, but this is not confirmed. Treat QA's findings as applying to the build QA ran.

## Decisions already made

- D-001: no new inputs.
- D-028: the dash indicator is shown on the legacy route too, including room 5.
- D-027: G-002 is stopped; its verification stays out of scope.

## Constraints

- Both 30 and 60 FPS apply (`project.md#constraints`).
- Dash rules stay as they are (goal.md Interpretation). If the only way to satisfy a criterion is to change dash timing or rules, do not decide it. Hand back to `studio` saying so, and the Studio will route it to `game-director` or the Owner.
- Prefer changes that reuse existing systems. Where a wording or criteria change suffices, choose it over a code change.
- Budget is tight: 11 of 17 operations are used after this Route. Keep the remaining Build and Verify scope to what the Owner request needs.

## Open questions

Questions 1–4 above.

## Expected output

An updated `design/dash-availability.md` and an outgoing Handoff addressed to `studio` (the Studio then composes the next Handoff, including the Playtester's from player-visible information only). The Handoff must contain:

- the answer to each of questions 1–4;
- the list of changes needed in build, in manual, and in criteria;
- the criteria QA must re-check, with a script idea for the Q5 discrimination;
- whether any Decision is needed.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/dash-availability.md, design/combat.md, repo/manual.md, repo/public-driver.md, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-028-dash-indicator-on-legacy-route.md, decisions/D-024-g002-historical-comparison-evidence.md
- Previous handoff: goals/G-003-dash-availability-clarity/10-qa-to-studio.md
