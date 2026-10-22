---
kind: handoff
goal: G-001
seq: 9
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 09: studio → gameplay-engineer — Build the combat spec (readable grubs and spitters, room pass) and make the balance bots usable

## Task

Implement `design/combat.md` in `repo/` (build 0.4 → next build): grub phases and cues, Runner and Brute variants, spitter aim cue and staggered volleys, the room changes, the `r` / `G` marks and messages in `repo/manual.md`, and tests. Also update `repo/bots.py` as test tooling (see Findings, part 2). Stop and hand back if the spec is ambiguous, contradictory or missing a case; do not decide design questions.

## Context

Goal G-001: the Owner finds combat monotonous. Diagnosis found grubs trivial and unreadable, spitters unreadable, and the dash never needed. The game-designer wrote the spec (handoff 07). Decide was skipped (only parameter variants of existing enemies, no new input, D-001 holds). QA checked the reported 30/60 FPS divergence of the dodger bot (handoff 08). Plan is skipped: the change reuses the existing enemy update loop and adds timers and states, with no cross-system approach. If you find the plan is not workable (for example, the FPS constraint cannot be met with the existing structure), hand back for a Plan.

## Findings

1. **Spec.** `design/combat.md` is the source of truth; 16 acceptance criteria. Criteria 1–12 are play checks (practice room, both 30 and 60 FPS). Criteria 13–16 are bot comparisons at both rates (walker loses 3–6 hearts over rooms 3–5; a good dodger loses at most half and clears them). The numeric thresholds in 13–15 are initial values and may need one tuning pass after the first bot runs; that is a design matter, so report the bot numbers rather than adjusting the spec yourself.
   - Code-reading note from the designer: every `Enemy` starts with `cooldown = SPIT_INTERVAL`, so all spitters fire in the same frame. The spec requires staggered first shots (1.8 s + 0.8 s per spitter).
2. **Bot tooling (QA report 08).**
   - On build 0.4 the dodger bot gives different results at 30 and 60 FPS in rooms 3–4. At 60 FPS it did not clear room 3 (13 dashes, 3 hearts lost); at 30 FPS it cleared with 4 dashes and 0 hearts lost. The walker and camper agree at both rates.
   - The simulation itself matched within one frame of rounding: spit timing, shot travel, dash distance, hit-stun, hurt-invulnerability, and dash invulnerability in the traced cases. The game is deterministic, and the 14 existing tests pass.
   - QA's hypothesis, not proven: the dodger acts every frame with no reaction delay (`play.py` limits rules to one action per 0.15 s, `bots.py` does not), so a one-frame difference in detecting a shot can change later decisions.
   - Needed: make the dodger frame-rate independent (accumulated-time reaction delay in seconds), and make the bots react to the new cues (wind-up flash and path line, spitter aim cue), so that a "good dodger" for criterion 13 exists. Add per-room decision logging if useful for diagnosis.
   - Do not change build timing to fix the bot discrepancy. If, after the bot is fixed, results still differ between 30 and 60 FPS, treat it as a possible build defect: report it with traces and do not paper over it.
3. **Documentation.** `repo/manual.md` must list the `r` / `G` marks and the new messages (it ships with the build and is what players and playtesters read).
4. **Visuals.** The cues (flash, path line, spitter glow, line against the dark) are specified as player-observable behavior. An art-director visual review follows the build, so implement them as the spec describes and note in the build notes how each cue appears in `run_play` output.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- Studio: Decide skipped; Plan skipped (see Context).

## Constraints

- Pillars: one-button combat, short runs, readable threats.
- Must play correctly at both 30 and 60 FPS: durations in seconds, not frames; per-frame travel stays below contact reach.
- Reuse existing systems; small team.
- Do not alter dash behavior (invulnerable for the full dash duration, per `design/combat.md`) beyond what the spec says.
- Run the project's tests (`python3 -m unittest discover -s tests`) and add tests for the new behavior, including one comparing outcomes at 30 and 60 FPS.

## Open questions

- None blocking. Hand back to the game-designer if the spec is unclear or missing a case; hand back to the technical-director if the approach is unworkable.
- Report the first bot results at both rates for criteria 13–16 in the build notes, even if they miss the thresholds.

## Expected output

Changed `repo/` (game, bots, manual, tests) and build notes: what changed per spec section, how each cue appears in `run_play` output, test results, first bot results at 30 and 60 FPS, and any spec problems found. Address the outgoing Handoff to `studio`, since QA verification (and an art-director review in parallel) follows, and a later playtester Handoff must be composed from permitted information only. Put your self-test verdicts and reasoning under `## Sender assessment`.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat.md, repo/manual.md, repo/README.md, repo/game.py, repo/bots.py, repo/play.py, repo/tests/test_game.py, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/07-game-designer-to-studio.md (also read the QA report: goals/G-001-combat-monotony/08-qa-to-studio.md, without relying on its proposals beyond the bot work described above)
