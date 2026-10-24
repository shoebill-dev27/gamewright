---
kind: handoff
goal: G-001
seq: 69
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 69: studio → gameplay-engineer — Build D-011 variant-named messages and the manual wording

## Task

Implement the D-011 message strings and the manual wording from `design/combat-step68.md`, with tests. Do not change any rule, timing, room or hearts value.

## Context

Goal G-001 (combat feels monotonous). Build 0.6.1 passed verification at 30 and 60 FPS. The latest playtest found that the brute and runner wind-up and hit messages read "a grub", so the player could not tell which enemy attacked. Design accepted D-011 to fix this and prepared the exact strings and acceptance criteria. This build is wording only.

## Findings

Strings (text build, everywhere they are printed; only the noun changes):

| Variant | Wind-up message | Hit message |
|---|---|---|
| Standard grub `g` | `a grub rears back` | `YOU ARE HIT by a grub` |
| Runner `r` | `a runner rears back` | `YOU ARE HIT by a runner` |
| Brute `G` | `a brute rears back` | `YOU ARE HIT by a brute` |
| Spitter shot | unchanged | `YOU ARE HIT by a shot` (unchanged) |

- The hit message keeps its suffix (for example `— hearts n/3`). Swipe, kill, shrug and spitter messages stay unchanged.
- A reaction rule `text "rears back"` must still match all three wind-ups. Rules keyed on `a grub rears back` or `by a grub` now match only standard grubs.
- Update the existing tests and bots that key on the old strings. Bot results must not change.
- Manual: apply the late-swipe wording and the in-flight count wording given in `design/combat-step68.md` (wording only, and it supersedes the stale "no more than 3 are in the air at once" sentence in `repo/manual.md`).

Acceptance criteria (player-observable, at 30 and 60 FPS, practice room, one case per variant):
- **V-a.** A wind-up prints the variant's message once per wind-up, at the same moment as the current message (±1 frame).
- **V-b.** A hit by a grub, runner or brute prints the matching hit message on the frame of contact, with the same hearts text as today.
- **V-c.** In the same scripts, every other output line, including the `cue:` line, the `~` line, timings and hearts, is byte-identical to 0.6.1.
- **V-d.** `text "rears back"` reacts to all three variants as before.
- **V-e.** Criteria 1–11 and 17–21 of `design/combat.md` still hold (criterion 11 as amended in `design/combat-step-46-room3-cap.md`), and bot results do not change.

## Decisions already made

- D-001: one-button combat. No new input.
- D-011 (accepted): variant-named wind-up and hit messages. It supersedes D-008.
- D-004 to D-007 stand and are not reopened.

## Constraints

- No change to timings, damage, room layouts, hearts or enemy parameters.
- Do not touch room 3 content. A separate Design step is working on it in parallel and will be built later.
- Must play correctly at 30 and 60 FPS. Reuse the existing message system.
- Stop and hand back if the spec is ambiguous or missing a case. Do not decide it yourself.

## Open questions

None.

## Expected output

A change with tests and build notes: the build identifier or sha, the test run (`run_tests`), and the bot run showing results unchanged. Address the result to `studio`; Verify (QA) and a fresh playtest follow, and neither may receive implementation history.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat-step68.md, design/combat-step59.md, design/combat.md, design/combat-step-46-room3-cap.md, repo/manual.md, repo/README.md, repo/game.py, repo/bots.py, repo/play.py, repo/tests/test_game.py, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-011-variant-named-messages-accepted.md
- Previous handoff: goals/G-001-combat-monotony/68-game-designer-to-studio.md
