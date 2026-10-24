---
kind: decision
id: D-030
status: accepted
decided_by: game-director
goal: G-003
date: 2026-10-23
supersedes: none
---
# D-030: G-003 review scope calls: hit-stun display and `(nothing happens)` are out of scope, the public-driver cadence stays as documented

## Decision

1. **Hit-stun display is not part of G-003.** After a hit the field shows a true countdown to the moment dash works again, and the numbers were correct. The success condition asks whether dash is available and when it will be again, and the screen answers both. Showing why dash is unavailable on the field is a separate readability improvement (a proposed Goal). It would change wording only, not rules.
2. **`(nothing happens)` after hits is not part of G-003.** The Playtester's script had no dash rule, so these lines cannot be dash refusals, which now print `dash not ready — …`. They are another readability issue, possibly a defect, and become a proposed Goal.
3. **Public-driver periodic cadence.** The behavior stays as `repo/public-driver.md` documents it: after an event picture, the periodic pictures restart their 0.5 s cadence. Spec 3.5 and Q8(b) of `design/dash-availability.md` ("fixed grid including after dash event pictures") are read as applying to the legacy route, where the grid holds. This is recorded as the build's behavior. No dash value or `dash ready` time depends on it. The spec text is corrected only when a later Goal edits that document.
4. **Unverified items are `skipped`, not passed.** They stay listed as unverified in the Review.

Limits: this does not change dash rules, timing, inputs or any earlier Decision. It does not claim that unit-tested-but-unread criteria, the baseline-dependent parts or the timing-unchanged claim are verified.

## Rationale

The Owner's complaint was missing information about when dash returns. The displayed state and time matched the build in every observed case. Refusals told the exact wait, and `dash ready` arrived at the exact moment. Adding the reason for hit-stun, explaining unrelated no-op lines, or aligning the cadence text would each be new work on something other than the stated complaint. The Goal budget is also used up. None of these makes the player guess when dash returns.

## Alternatives considered

- Ask for an Owner cost escalation to add a hit-stun reason: the field is already truthful, so the Owner request does not need it. A proposed Goal is cheaper and keeps scope clean.
- `goal-not-met` because of the hit-stun look: that would stretch the success condition from "when" to "why".
- Redesign the cadence to a fixed grid in the public driver: it changes output timing with no gain for dash clarity, and it is not needed for the request.

## Revisit when

A human playtest (live or gamepad) finds the hit-stun countdown confusing or reads it as a spent dash. The cadence difference is reported as hiding or delaying a dash state. A pre-change build or output record becomes available. D-029's revisit conditions also still apply; none has been reached.
