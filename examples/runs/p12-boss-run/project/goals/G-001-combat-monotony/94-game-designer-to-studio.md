---
kind: handoff
goal: G-001
seq: 94
from: game-designer
to: studio
stage: Build
outcome: done
---
# 94: game-designer → studio — Wording spec for shot-hit source (A) and late-swipe explanation (B) is ready to build

## Task

Route the spec in `design/combat-step94.md` to Build (gameplay-engineer), then Verify (QA, 30 and 60 FPS), then Review pass 4 as a paper check (D-013).

## Context

Goal G-001, handoff 93. Wording only: no rule, number, timing, cap, cue or input change. No runs were needed.

## Findings

- **(A) Format.** `YOU ARE HIT by a shot from the <direction>`, followed by the existing suffix. `<direction>` is one of eight compass words (north is the top of the drawn room, smaller y). It is the side the shot came from: the reverse of its travel direction, taken from the locked travel vector at the contact frame. The formula and the 22.5° sector boundary are in the spec.
- **(A) Information needed.** Nothing new is carried. The shot's locked travel direction is read at contact, before the shot is removed. The message repeats the direction the `cue:` and `~` lines already showed, with no distance, time or spitter identity. It is identical at 30 and 60 FPS. Absorbed shots still show no message.
- **(B) Format.** One line when a swipe damages, without killing, a grub, runner or brute in its Lunge phase: `the <grub|runner|brute>'s lunge had already started, the swipe was too late to stop it`. It comes before any `YOU ARE HIT by` line of the same frame. It does not contain `rears back`, `takes aim` or `YOU ARE HIT by`. The brute's wind-up line `the brute shrugs off the swipe` is untouched. No line appears in other phases or on a kill.
- **Acceptance criteria W1–W8** are in the spec. They cover the direction words, the prefix and substrings, absorbed shots, the late-swipe line, no line elsewhere, no behavior change (the same traces as before to ±1 frame, `bots.py` unchanged with the suite green) and equality of wording at both rates.
- **W1 placement caveat for QA.** The spitter at (15,7) is a boundary-ish case: the ratio is 3/7 = 0.43, which is above 0.4142, so the diagonal `south-east` is expected. QA checks the traced value against the formula.
- **Files.**
  - New `design/combat-step94.md`.
  - `design/combat.md` gets a pointer paragraph at the top.
  - **I could not edit `repo/manual.md`** (outside my write paths). The exact replacement wording is at the end of the spec; the Build step applies it.
- **Risk for Build.** If `bots.py` or any reaction rule matches the full string `YOU ARE HIT by a shot` with equality instead of a substring, it would break. Build checks this and fixes the tool, not the rule text.

## Decisions already made

D-001, D-005, D-007, D-011, D-013 apply as written. No new Decision: no rejected alternative constrains later work beyond the spec's list.

## Constraints

- Wording only. Keep `takes aim`, `rears back`, `YOU ARE HIT by` and the brute "shrugs off" line.
- Reuse the existing message system.
- Same effect at 30 and 60 FPS.

## Open questions

None.

## Expected output

Build implements the two messages and applies the manual wording. QA verifies W1–W8 at 30 and 60 FPS. Review pass 4 is a paper check of QA's result.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: none
- Project: design/combat-step94.md, design/combat.md, repo/manual.md
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md, decisions/D-011-variant-named-messages-accepted.md, decisions/D-013-review-pass-3-readability-wording-then-close.md
- Previous handoff: goals/G-001-combat-monotony/93-studio-to-game-designer.md
