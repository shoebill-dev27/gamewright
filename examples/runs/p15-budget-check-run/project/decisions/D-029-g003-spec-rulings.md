---
kind: decision
id: D-029
status: accepted
decided_by: game-designer
goal: G-003
date: 2026-10-23
supersedes: none
---
# D-029: G-003 spec rulings: 30 FPS quantization, driver pictures, rule-driven refusals, evidence without a baseline

## Decision

1. **30 FPS tolerance.** The ±1 frame tolerance for ready time and start-to-start is measured against the frame-quantized value the build produces, not against the nominal 0.85 s. Expected start-to-start is 0.850 s at 60 FPS and 0.900 s at 30 FPS. The manual says so. Dash length, cooldown and the input set do not change. No build change.
2. **Public-driver pictures.** The event picture after an accepted-dash message or a refusal message in the public driver is accepted, as it is for swipe-miss and `(nothing happens)`. The legacy route prints no picture. Spec 3.3 is amended. No build change.
3. **Rule-driven refusals.** A refused dash prints `dash not ready — …` whatever its source (scripted press, public-driver rule, legacy rule). `text "not ready"` may fire on it. This is a small Build change on the legacy rule path; QA discriminates route from action type.
4. **Evidence without a baseline** (Q8, Q12), following D-024: identity with a build that does not exist is not claimed. Accepted evidence is (a) recorded numbers from earlier handoffs, compared at their recorded precision; (b) checks of the new output against the stated rules, such as the periodic grid and event order; (c) internal consistency within one build. Whatever remains is reported as unverifiable, never as pass. See spec Q8 and Q12.

Q3 (a hit does not change the cooldown) and Q4 (attack recovery does not block dash) are recorded as the build's behavior, and the spec now follows it.

## Rationale

Changing 30 FPS timing would break Q8 and is outside the Goal. The display already agrees with the build, so a wording and criteria change is enough. The public-driver picture is the driver's general pattern, and one picture per press is bounded by the user's or the rule's own press rate (a rule acts at most every 0.15 s). A silent refusal on one route is exactly the kind of invisible dash the Owner complained about. A byte comparison with a missing build cannot be done, and D-024 shows the honest alternative.

## Alternatives considered

- Measure against the nominal 0.85 s and change 30 FPS timing: breaks Q8 and the dash rules; not decided here.
- Suppress the driver's pictures: a new driver rule and code, for no clarity gain.
- Leave legacy rule refusals silent and document it: keeps the manual promise false on the most-used route.
- Treat the missing baseline as pass: rejected, as in D-024.

## Revisit when

A human playtest finds the 0.9 s at 30 FPS confusing. A pre-change build or output record becomes available. Refusal pictures are described as clutter.
