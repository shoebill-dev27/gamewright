---
kind: handoff
goal: G-002
seq: 13
from: playtester
to: game-director
stage: Review
outcome: done
---
# 13: playtester → game-director — Observation report, build 0.4

## Task

Review whether G-002's intent is met, using this report and the verification result.

## Context

G-002, Owner request 「戦闘が単調なので改善したい」. Blind playtest of build 0.4 (handoff 12); the
Playtester was not told what changed.

## Findings

Observation report (method: dry-run, read `sim/build-0.4.md` as two runs of play).

- **Room 2:** orange glow before shots; "I keep moving between swipes now."
- **Room 3:** the rushing enemy hit me once; then "glow means move" — dash sideways, free hit while
  it recovers. "My corner trick got me killed here."
- **Room 4:** shielded enemy sparks on frontal hits; I circle behind and pick targets. Hitting it
  during its glow didn't stop the bash — learned to dodge instead.
- **Room 5:** tense and busy, the best room. **Problem:** in the darkest corner near the exit, the
  shielded enemy's orange glow is hard to see against the wall — bashed twice "out of nowhere".
  Impact: medium; felt unfair.
- **Dash:** used constantly in rooms 3–5, mostly to dodge.
- **Power:** still occasionally wish a hit felt heavier, "but much less than last time".
- **Overall:** rooms feel different from each other; would play another run.

## Decisions already made

None known to the Playtester.

## Constraints

Observations only.

## Open questions

None from the Playtester.

## Expected output

Review result to the Studio: goal met or not, next issues.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/review-outcome.md
- Project: project.md, design/enemy-telegraphs.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-enemy-side-combat-depth.md, decisions/D-003-committed-telegraphed-attacks.md
- Previous handoff: goals/G-002-combat-monotony/11-qa-to-studio.md
