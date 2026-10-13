---
kind: handoff
goal: G-001
seq: 15
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 15: studio → game-designer — settle the spec gap QA found in the level 1 opening (silent sand taps) and the minor spec questions

## Task

Decide, as spec owner, how a sand tap behaves inside the pulse rate-limit window (QA gap G1), and say whether the minor points N1, N2 and N4 need a spec change. Update `design/onboarding.md` (and record a Decision only if the choice constrains later work or rejects a real alternative). Then hand the result to `studio`.

## Context

Goal G-001: children aged 7–10 stalled at the start of level 1 in build 0.2. Your spec (options A + B) was built in build 0.3 (Build 4b). QA verified it (step 5, report `14-qa-to-studio.md`): all 12 checks pass. QA found that the spec leaves one case where a touch can feel ignored. Expected behavior there is undefined, so the return rules send it to Design. The next planned step is a Playtester session on the build. It has not happened yet. A spec change would change the build the Playtester sees, so this is settled first.

## Findings

From QA (verified by reading `sim/build-0.3.md` against the spec, not on a device):

**G1 (low to medium): sand taps can be silent.**
- Rule 5: a sand tap triggers only the pool's redirect pulse. The pulse starts at most once per 1.5 s.
- The sand itself shows nothing.
- A sand tap landing after the previous pulse has finished (about 0.6 s) but before 1.5 s has passed gets no visible response.
- That conflicts with check 4 ("no silent touches") and with the intent that a touch never feels ignored. The child's target group taps repeatedly when nothing happens.
- QA passed check 4 because the build matches the spec as written. QA asks whether sand taps in that window need a minimal response, or whether check 4 should apply only to taps at least 1.5 s apart.

**Minor notes (no check fails):**
- **N1: pulsing rim.** Hit areas are the pool's size at rest (per spec). While the pool pulses larger (up to 6%), a touch on its visible outer rim counts as sand and gives a pulse instead of a grab. A child may feel "I touched the pool and it did not take it".
- **N2: crab flip after an intro-cancel.** The crab flips to face the pool's position at touch-down. If the pool was mid-slide, it then glides to its authored start. If the crab lies between the two positions, it could face away from the pool's final position. The spec does not say which position counts.
- **N3: pool shadow source.** QA could not confirm whether the soft shadow under the lifted pool is an existing sprite or a drawn effect. Please say whether the spec intended a particular source. The constraint is to reuse the existing sprite sheet "where possible", so say whether a drawn effect would be acceptable.
- **N4: pulse precedence.** After an intro-cancel, the redirect pulse and the idle pulse are both due at the end of the ease-back. The spec does not say which is shown. QA assumes the redirect pulse plays and the idle pulse resumes after it.

**Other QA results (for context, no action here):**
- No D-001 issue was found. There is no inactivity-triggered cue, and undo works.
- D-002 holds.
- Levels 2 and 3 are unchanged.
- The platform check for reduced-motion settings could not be confirmed from the packet (target OS versions are not named). Do not act on it here.

## Decisions already made

- D-001: no failure, no timers, every move undoable. Any sand-tap response must be triggered by the touch, never by inactivity.
- D-002: intro cancel eases the pool back over 0.15 s, and the intro is never in undo history. Keep it.
- Option C (idle hint) stays excluded from the spec.

## Constraints

- Stay inside the vision and D-001. Keep changes local to level 1 and use the existing sprite sheet (color, flip, size, rotation, position, brightness changes).
- No mechanic may depend on reading text. Touch only.
- Keep the 0.2 s response criterion unless you have a reason to change it, and say why.
- Keep the purpose of the rate limit (no flicker or spam from rapid tapping) when you choose a minimal response.
- Write the spec so a Playtester-safe handoff can be composed afterward. Do not mention the playtest or any expected result in the project files.

## Open questions

1. G1: what should a sand tap do inside the 1.5 s window? Either specify a minimal touch-triggered response, or narrow check 4 and say why leaving it silent is acceptable.
2. N1: is the rim behavior acceptable (keep), or should the hit area follow the pulse?
3. N2 and N4: specify the intended behavior, or say why no spec is needed.
4. N3: what was the intended source of the shadow, and is a drawn effect acceptable?
5. If anything changes in player-facing behavior, say so explicitly, because Build and Verify must then run again.

## Expected output

- An updated `design/onboarding.md` with player-observable acceptance criteria for any change. Update the check list if checks change.
- A Decision record only if the choice meets the threshold (constrains later work or rejects a real alternative).
- An outgoing Handoff to `studio` (address the result to `studio`, not to a Role) with `outcome: done`. It states in Findings whether player-facing behavior changed, and gives your answers to the open questions.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, project.md#art-direction, design/onboarding.md, sim/build-0.3.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-002-intro-cancel-and-undo.md
- Previous handoff: goals/G-001-first-puzzle-stall/14-qa-to-studio.md
