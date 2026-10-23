---
kind: handoff
goal: G-003
seq: 12
from: game-designer
to: studio
stage: Route (compose the next Handoff: Build for one small change, then QA re-check and Playtest)
outcome: done
---
# 12: game-designer → studio — Rulings on 30 FPS tolerance, driver pictures, rule-driven refusals and baseline-free evidence

## Task

Compose the next Handoff from this report. One small Build change is needed (legacy rule-driven refusals print). Then QA re-checks the listed criteria, and the Playtester gets player-visible information only.

## Context

Goal G-003: the Owner found it unclear when dash can be used again. Design 04 specified the display, Build 08 implemented it, and QA 10 failed it literally at 30 FPS and raised spec questions. I settled those questions in `design/dash-availability.md` and D-029. No dash rule changed (recovery 0.25 s, cooldown 0.6 s, invulnerability, inputs).

## Findings

### Answers

**1. 30 FPS tolerance.**
- The ±1 frame is measured against the frame-quantized value the build produces, not against the nominal 0.85 s.
- Expected start-to-start is 0.850 s at 60 FPS and 0.900 s at 30 FPS. For a dash at 0.6 s, ready is 1.450 s at 60 FPS and 1.500 s at 30 FPS.
- At 30 FPS the first accepted press is 27 frames after the first dash, and a press one frame earlier (1.467) is refused. This is what QA saw.
- The display agrees with the build and never shows ready early. `usable again in 0.9 s` is true at both rates.
- The manual line becomes: "So the next dash can start 0.85 s after the previous one started (60 FPS); at 30 FPS the frames make it 0.9 s."
- I did not decide whether this quantization predates the Goal; no earlier build exists. This Goal changed no timing.
- **Change needed:** manual and criteria only (P6, P7, Q1, Q2 intro). No build change. The Goal needs no timing change, so this does not go to `game-director`.

**2. Public-driver pictures.**
- Amend the spec; do not suppress the pictures.
- The legacy route prints none; the public driver prints its usual event picture after accepted-dash and refusal messages, as after swipe-miss and `(nothing happens)`.
- The cost is accepted: these are event output under Q10, bounded by the press rate (a rule presses at most every 0.15 s, so at most about 6 per second).
- **Change needed:** spec 3.3 and 3.5 (done) and a manual note (done in the drop-in text). No build change.

**3. Rule-driven refusals.**
- Any refused dash prints `dash not ready — …`, whatever its source (scripted press, public-driver rule, legacy rule), and `text "not ready"` may fire on it.
- Reason: the Owner's problem is an invisible dash, and the manual promises the line.
- QA could not separate route from action type. P13 is a new check with the same rule on both routes plus one rule of a different action type.
- If the Build finds that the legacy rule path cannot report the refusal without changing game results, it hands back to the designer; it does not change results.
- Rule-driven attacks that do nothing keep their current `(nothing happens)` behavior.
- **Change needed:** Build (small, legacy rule path only, suspected), manual (drop-in text updated), criteria (P13).

**4. Q8 and Q12 without a baseline (D-024 as precedent).**
- "Identical to before" is not claimed and not byte-compared.
- Q8 accepts:
  - (a) recorded numbers from earlier handoffs at their recorded precision: dodger hearts lost and dash counts per room, normal-run clear times, the 60 FPS dash probe, earlier QA hit times;
  - (b) same-build checks: periodic pictures stay on the 0.5 s grid including after dash event pictures, event order is unchanged, trace game events do not depend on the view;
  - (c) the test suite.
  Whatever is not covered is reported as unverifiable, never as pass.
- Q12 reduces to: the legacy room 5 note line is exact and the field is present; the rest is unverifiable (D-024 item 1; G-002 stopped, D-027).
- **Change needed:** criteria only.

**5. Q3 and Q4.** Recorded as the build's behavior. A hit does not change the cooldown, and the first accepted press is max(ready, hit + 0.3 s). Attack recovery does not block a dash. Spec section 2 now says so. No change.

### Items QA could not verify

| Item | Needs Build? | What is needed |
|---|---|---|
| Q5 room-entry reset | No | Better script (below). |
| Q7 across bot runs | No | Evidence method: use trace `dash_start` and `dash_ready` times of the bot runs instead of bot decision logs. |
| 1-frame-before press at 60 FPS | No | Script: dash at 0.6, press at 1.433 (refused) and at 1.450 (accepted). |
| P12 for dodger bots | No | Run the public replay scripts (`public_script` from `tests/test_split_c.py`, player view) and read the pictures. |
| Q9 gaps (legacy rooms 1, 2, 4; `mode room` rooms 1–4) | No | Optional, cheap player-view scripts if rounds remain. |

**Q5 discrimination script** (also in spec Q5):
- Use `mode run`, trace view, room 1.
- A first run gives the last-kill time k.
- In a second run start a dash at k − 0.25 and queue the killing swipe during it (an attack pressed during a dash fires when the dash ends). The swipe then lands at k with the 0.6 s cooldown just starting.
- Read the trace. If `dash_ready` appears during the clear screen (about k + 0.6), the cooldown runs on the clear screen. It is then always over before entry, so the reset is unobservable. The criterion reduces to "ready at entry, press accepted, no message".
- If `dash_ready` appears only at entry, the cooldown was pending and the reset is confirmed.
- Either result is recorded as a result, not a defect.

### Build identity

I treat QA's findings as applying to source `b62005468da6`. The relation to packet sha `aa28af2ce710` stays unconfirmed. The Studio should confirm it before the Build change.

## Decisions already made

- D-001: no new inputs.
- D-024: precedent for evidence without a baseline.
- D-027: G-002 is stopped.
- D-028: the indicator shows on the legacy route too.
- **D-029 (new, this step):** the four rulings above.

## Constraints

- Both 30 and 60 FPS apply.
- Dash rules unchanged; no timing change.
- Budget is tight (11 of 17 operations used after this Route). Remaining scope: one small Build change, one QA round, then the Playtest.
- The Playtester receives only what a player sees: the manual and the screen. The spec's section 7 (experience signals) and this handoff's rationale stay out. The Playtester must be told that at 30 FPS the second dash comes 0.9 s after the first, as the manual now says.

## Open questions

- Whether a human finds one decimal, the `dash:` words, `dash ready` and the extra pictures clear and not cluttered. This is for the Playtest.
- Whether the legacy rule path can report the refusal without changing results. This is for the Build to check.
- Which sha was meant (`aa28af2ce710` vs `b62005468da6`). This is for the Studio to confirm.

## Expected output

1. **Build** (`engineer`):
   - Make a refused dash print `dash not ready — …` on the legacy rule path as well, and let `text "not ready"` fire on it. If this cannot be done without changing results, hand back to the designer.
   - Apply the manual drop-in text, which now has four changes:
     - the 30 FPS dash line;
     - the rule-driven refusal statement;
     - the note on pictures in `mode` runs;
     - `text "not ready"` as usable.
   - Do not touch timing.
2. **QA re-check**, with trace, play and bots:
   - P6, P7, Q1 and Q2 at 30 FPS against the new values (0.90 s, ready at 1.500).
   - P13 on both routes with both action types.
   - Q5 with the script above.
   - Q7 by trace.
   - The 60 FPS press at 1.433/1.450.
   - P12 for dodger runs via the public replay scripts.
   - Q8 and Q12 under the D-029 evidence rule, reporting unverifiable parts separately (D-024 style).
3. **Playtester**, in parallel or after: player-visible information only; clarity judged at 60 FPS, with 30 FPS timing described as in the manual.
4. **Pass condition for Review:** the Studio lists the unverifiable Q8 and Q12 parts explicitly; they are not a pass.

## Load

- Role: studio/roles/engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/dash-availability.md, repo/manual.md, repo/public-driver.md, project.md#constraints
- Decisions: decisions/D-028-dash-indicator-on-legacy-route.md, decisions/D-029-g003-spec-rulings.md, decisions/D-024-g002-historical-comparison-evidence.md
- Previous handoff: goals/G-003-dash-availability-clarity/11-studio-to-game-designer.md
