---
kind: handoff
goal: G-001
seq: 2
from: game-designer
to: studio
stage: Routing (Plan or Build next)
outcome: done
---
# 02: game-designer → studio — first-playable design spec is ready for routing

## Task

Route the work to Plan or Build. The design spec `design/first-playable.md` is finished and needs an engineer to build it and QA to verify it.

## Context

Goal G-001: the Owner asked (ja) "このコンセプトで、遊べる最初の版を作ってほしい". Handoff 01 asked the game-designer for a player-observable spec of the first playable. This is that spec. `repo/` holds only a README; no build exists yet.

## Findings

**Design index (for the Owner's `project.md`; I did not edit it):**
- `design/first-playable.md`: rules, parameters, edge cases, three nights with solutions, acceptance criteria.
- `decisions/D-001-beam-and-ship-rules.md`: the beam and ship-movement rules.

**Rules in short**
- The board is 7×7. The lighthouse is at (3,3). The coast is row 6, made of harbor and rock tiles.
- Ships are all on the board at turn 0.
- The beam has three aims: LEFT, UP (lights nothing) and RIGHT. Commands are `L`, `R` and `H`, clamped at the ends. Changing sides takes two turns.
- Only row 3 can be lit. A lit ship does not advance; it slides one tile away from the lighthouse. An unlit ship moves one tile south. A lit ship at the map edge stays put.
- Harbor docks a ship. A rock or the lighthouse wrecks it. Any wreck loses the night. The turn limit is 10 (dawn).

**The three nights** (each with a solution that wins on turn 7, plus check scripts that lose)
- Night 1 "First light": 1 ship, solution `L H H H R H H`.
- Night 2 "Both sides": 2 ships, solution `H L R R L H H`.
- Night 3 "Keep it dark": 3 ships, solution `L L R R L H H`.

**Acceptance criteria (verification, AC-1 to AC-15; the full text is in the spec §9)**
- AC-1: the first screen of each night matches the layout.
- AC-2: `L`, `R` and `H` change the aim as specified, and switching sides takes two turns.
- AC-3: lit tiles are drawn `~` correctly.
- AC-4: an unlit ship moves one tile south per turn.
- AC-5: a lit ship slides one tile away from the lighthouse and stays in row 3.
- AC-6: a lit ship at the map edge is pinned, not wrecked.
- AC-7: dock and wreck are reported with the position.
- AC-8: the three solutions win on turn 7 with the tabled positions.
- AC-9: the failure scripts lose as stated.
- AC-10: dawn at turn 10 loses with ships still at sea.
- AC-11: a dock and a wreck on the same turn are both reported, and the night is lost.
- AC-12: the same script gives identical output every run.
- AC-13: an invalid command is reported without advancing the turn, and a script that ends early is reported.
- AC-14: commands after the night ends are ignored and reported.
- AC-15: ship positions can be derived from the screen and the manual, including a correct forecast line.

**Experience signals (E-1 to E-5, playtest and Review only):**
- E-1: a new player can predict how far a held beam pushes the ship in Night 1.
- E-2: a stuck player in Night 2 can name the cause, not luck.
- E-3: after losing Night 3, the player can explain the mistake.
- E-4: a night takes under 5 minutes to decide.
- E-5: players describe the game as planning, not reacting.

**Limits of what I could do:** I had no build, so I could not run `play.py`. I simulated every solution and failure script by hand, turn by turn, in the spec's tables. QA should confirm them against the build.

## Decisions already made

- D-001 (accepted, game-designer): three beam aims, lit ships slide along the beam row, a wreck loses the night at once, and there is a 10-turn limit.

## Constraints

- Python 3 standard library only, text output, deterministic, played through input scripts with no live input.
- The script format and `repo/manual.md` are the build's to define. The manual must tell the player the rules in §3–§4 and the symbols in §2.
- Do not add mechanics beyond the spec. Row and column numbers, the ship list and the forecast line are required screen content (spec §6).

## Open questions

- For `game-director`, non-blocking: do you want mid-night ship arrivals in later nights? This version places every ship on the board at turn 0. Adding arrivals would be a scope question.
- For `game-director`, non-blocking: should a wreck always lose the night at once? The spec follows the vision's "let none hit the rocks".

## Expected output

Route to Build (an engineer builds `repo/` and `repo/manual.md` from `design/first-playable.md`), then QA against AC-1 to AC-15. Plan looks unnecessary: the scope is small, standard-library only, and has no cross-system risk.

## Sender assessment

- The spec is complete for a first playable. All three solutions were hand-simulated and are consistent with the rules.
- Confidence is high on rule consistency and medium on balance, since nothing has been played yet. The experience signals are for the playtest.
- If the engineer finds an ambiguity, it should come back as a spec question to the game-designer.

## Load

- Role: none (Studio routing)
- Skills: none
- Project: design/first-playable.md; project.md#constraints
- Decisions: decisions/D-001-beam-and-ship-rules.md
- Previous handoff: goals/G-001-first-playable/01-studio-to-game-designer.md
