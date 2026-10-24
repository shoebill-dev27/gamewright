---
kind: handoff
goal: G-001
seq: 30
from: game-designer
to: studio
stage: Design
outcome: done
---
# 30: game-designer → studio — Both spec rulings made as wording only; no Build and no re-Verify needed

## Task

Report my rulings on the two points from QA's close-out verification (handoff 24, section D) and the files changed. Route onward: the playtest is not affected.

## Context

G-001 (combat monotony). Build 0.5 passed QA against criteria 1–17 at 30 and 60 FPS. The build is unchanged. Handoff 26 asked for two small rulings on the contact-edge graze accepted in D-002.

## Findings

### Ruling 1: a shot at exactly the reach (0.400)

- **A miss of exactly the reach is inside the band.** Either result is accepted at either rate, and 30 and 60 FPS may differ. It is not a guaranteed miss.
- This keeps `distance <= reach` in the build. QA's observation (hit at 30 FPS, miss at 60 FPS for a nominal 0.400) is correct behavior under the clarified spec and is not a failure of 17b.
- The same rule applies to lunges at exactly 0.600.
- Spec wording in `design/combat.md`, with no number changed:
  - The band is now more than reach − tolerance and up to and including the reach: more than 0.39 to 0.40 for shots, more than 0.57 to 0.60 for lunges. This removes the overlap at 0.39 and 0.57 and the gap at the reach.
  - 17a: 0.39 or less hits at both rates (as before).
  - 17b: "more than 0.40" (was "0.40 or more") misses at both rates.
  - 17c: lunge 0.57 or less hits at both rates; more than 0.60 misses at both rates (was "0.60 or more").
  - 17d: the band includes exactly the reach; the sampling rule, 16e and the edge cases are aligned.
- Every case QA verified (shots 0.390 hit and 0.407 miss; lunges 0.570 hit and 0.610 miss) is still covered with the same result. Those criteria remain valid.

### Ruling 2: lunge band width

- The measured figures are recorded: a guaranteed hit up to about 0.585 at 30 FPS, a band of about 0.015 tile at 30 FPS and about 0.004 tile at 60 FPS.
- **Limitation, stated in the files:** five probes only, not a full scan. The rates disagreed only at 0.590. There is no evidence of a band wider than 0.03 tile, which is the threshold that triggers a report back to the designer. The shot figure of about 0.003 tile is derived, not scanned.
- Recorded in `design/combat.md` (sampling rule, replacing "not yet run") and in the new Decision D-003.

### Where it is recorded

- I did not edit D-002, because it is not on my write list for this step. The ruling is a short follow-up Decision, **D-003**, which refines D-002 and does not supersede it. D-002 still says "derived, not yet run" for the lunge band, and D-003 carries the measured figures. Studio: if you want D-002's text brought in line, route that edit separately. It is not needed for correctness.
- Files changed: `design/combat.md` and `decisions/D-003-contact-edge-exact-reach-and-lunge-band.md` (new).

## Decisions already made

- D-001: one attack button plus dash; no new input.
- D-002: per-frame contact sampling is kept; the graze is an accepted limitation.
- D-003 (new): exactly the reach is inside the band; measured lunge band recorded.

## Constraints

- Wording clarifications only. No parameter, tolerance or other criterion was reopened.
- The `manual.md` sentence "no more than 3 are in the air at once" (QA's note in handoff 24, section B) is not a spec matter. Whether to say "in the five rooms" is a text edit for whoever owns the manual, and it does not affect the playtest.

## Open questions

None for the designer. If the Studio wants D-002 itself updated, that needs a role with it on its write list.

## Expected output

- **Build needed: no.** `distance <= reach` is kept.
- **Re-Verify needed: no.** The change is wording only, and every tested value keeps its verified result. The one-off case QA flagged (nominal 0.400) is now in the accepted band, so there is nothing left to re-check.
- The playtest can proceed as planned. Nothing here is for the Playtester's handoff.

## Sender assessment

Confidence is high that no Build or re-Verify is needed. The only residual risk is that a future tester scripts a miss of exactly 0.400 or 0.600 and expects a fixed result. The spec now says explicitly that none is promised.

## Load

- Role: studio/roles/studio-routing.md
- Skills: none
- Project: design/combat.md
- Decisions: decisions/D-002-contact-edge-graze-accepted.md, decisions/D-003-contact-edge-exact-reach-and-lunge-band.md
- Previous handoff: goals/G-001-combat-monotony/26-studio-to-game-designer.md
