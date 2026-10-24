---
kind: handoff
goal: G-003
seq: 5
from: game-designer
to: gameplay-engineer
stage: Build
outcome: done
---
# 05: game-designer → gameplay-engineer — ruling on three spec points; apply the fix list, then address the result to studio

## Task

Apply the fix list below (test bound, hit-stun display, manual text). No dash rule or number changes. Address your result Handoff to `studio` so Verify and Play get clean Handoffs.

## Context

G-003 (Owner: 「ダッシュがいつまた使えるのか分かりにくい。分かるようにしてほしい」). Build check failed on `test_ready_time_is_dash_end_plus_cooldown`: 0.9 s vs 0.85 s at 30 FPS (0.05 s over, delta 1 frame). Rulings are in `design/dash-readiness.md` (updated), `design/combat.md` (Dash line) and D-028.

## Findings

Rulings:
1. **Ready time.** 0.9 s at 30 FPS is NOT a defect. Dash end and recharge end each round up to a frame, so up to 2 frames over the nominal 0.85 s is expected. Bound: `0.85 s ≤ Tready − Tuse ≤ 0.85 s + 2 frames` (60 FPS: ≤ 0.8833 s; 30 FPS: ≤ 0.9167 s). Earlier than 0.85 s, or beyond 2 frames, is a defect. Input before `Tuse + 0.85` is always refused; at or after `Tuse + 0.85 + 2 frames` always accepted; in between follows the real state and must match the header. If you find an off-by-one cause you may fix it (not required); the bound stays.
2. **Hit-stun.** Display must follow "ready iff a dash would be accepted". During the 0.3 s stun: header `dash: recharging R s` (R = max of recharge-based time and stun left, rounded up 0.01 s, never `ready`); a dash input prints `dash not ready: R s left` instead of `(nothing happens)`; `dash_ready_in` in the trace is the same R. The dash timer itself is untouched. The `dash ready` line prints at the first frame the dash is usable after a recharge (if the stun outlasts the recharge, at the stun end); no line when only a stun ends with no recharge pending. Other silent causes (pause, clear screen, terminal, player down, reaction-rule refusals) are unchanged.
3. **Cooldown wording.** Confirmed: 0.6 s counts from the end of the dash (done in `combat.md`). Manual change below.
4. **Build number.** Keep 0.6. No banner test changes.

Criteria changed: DR2, DR4, DR5, DR7 (tolerance), DR13 (manual), DR14 new (hit-stun); DR6 and DR12 now include stun in R. See `design/dash-readiness.md`.

Not run in this step (no runs): nothing here was measured; the ready-time bound is derived from frame rounding, not from a trace.

## Decisions already made

- D-001: one attack button plus dash; no buffering of a too-early dash.
- D-028: the rulings above.
- G-003 Interpretation: no change to dash rules or numbers.

## Constraints

- Works at 30 and 60 FPS; reuse existing systems; do not change 0.25 s, 0.6 s or the hit-stun length.
- Header, messages and manual must agree (never claim ready while a dash is refused, or the reverse).

## Open questions

None for you. If the source shows a rule or number that differs (e.g. recharge not 0.6 s from the dash end), do not change it; report to `studio`.

## Expected output

Fix list:
1. `tests/test_dash_readiness.py::test_ready_time_is_dash_end_plus_cooldown`: replace the `assertAlmostEqual(..., delta=1/fps)` with `0.85 - 1e-6 <= ready - start <= 0.85 + 2/fps + 1e-6` at fps 30 and 60 (keep the message with fps).
2. Header/refusal in `game.py`/`play.py`/`run_driver.py`: include hit-stun in `dash_usable()`, `dash_ready_in()` and the header R, refusal text and `dash_ready_in` in trace, as in ruling 2. Make sure header, refusal and acceptance read the same state.
3. Add tests: hit-stun header and refusal text (DR14); ready bound at 30 and 60 FPS.
4. `repo/manual.md`: Dash bullet → "...so you can dash again about 0.85 s after the start of the last one. You cannot dash during the dash, the recharge or the moment after you are hit, and a dash pressed too early is not saved for later." In "Dash readiness" add: "After you are hit you cannot dash for a moment; the line shows `recharging` for that time too."
5. Run `python3 -m unittest discover -s tests`; report results and what was not run, in a Handoff to `studio` (stage Verify), listing the DR numbers above for QA.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/dash-readiness.md, design/combat.md, repo/manual.md, the build in `repo/` (game.py, play.py, run_driver.py), repo/tests/test_dash_readiness.py
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-028-dash-readiness-rulings.md
- Previous handoff: goals/G-003-dash-readiness/04-studio-to-game-designer.md
