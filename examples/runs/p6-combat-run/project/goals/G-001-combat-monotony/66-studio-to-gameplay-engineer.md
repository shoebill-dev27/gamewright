---
kind: handoff
goal: G-001
seq: 66
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 66: studio → gameplay-engineer — Build the combat response change set (re-issue of 61, with repo files and the Q1 answer)

## Task

Implement the approved spec in `design/combat.md` (AC-19…AC-28 and the parameters and rules they cover) and `design/combat-visuals.md` (V-9…V-17) on the existing simulation in `repo/`. Add tests, run the suite (`run_tests`), and report build notes.

## Context

G-001 (combat feels monotonous), Option A (D-002, D-004): rework existing enemy behavior as one sequential change set. Build 61 came back as a question (63) for two reasons: its packet had no `repo/` files, and the spec lacked the knockback direction of a grub at distance 0. The designer closed the gap in 65 (rule in D-013, criterion AC-28) and cleaned three passages (dash and walls, Waiting positions, AC-23). This packet names the repo files in Load. Read them directly.

## Findings

From 65, the points that change what you build:

- **Knockback (D-013, AC-28):** the first hit knocks a grub back 1 tile over 0.2 s. A grub 0.05 tile or more from the player is pushed straight away. A grub on the player's tile goes toward its display side (D-006): the side it last approached or struck from, otherwise right, left, above, below. That side needs 1 tile of clear room; if not, use the next side in that order. A push toward an edge is clamped at the edge, like the dash. Knockback does not change state or timers. A grub knocked back from distance 0 ends about 1.0 tile away and keeps its cap slot. A grub hit from 0.5 tile or more ends 1.5 tiles or more away and frees a slot.
- **Swipe result line** stays "you swipe: grub hit (1 left)" for every grub. An on-tile grub's position comes from the `on you:` line (AC-28(e)).
- **Dash and walls:** a dash always lasts 0.25 s with invulnerability for all of it, even when a wall shortens it. It is never cancelled by a wall. AC-25 checks 0.25 s on a 2-tile wall dash.
- **Waiting positions:** a cap-blocked grub holds at 2.0 tiles or more, backs off if the player approaches, follows to stay at about 2.0 tiles, and resumes Approach when a slot frees. A spacing-blocked grub approaches until within 1.25 tiles, then stands still until the window ends. If it is already inside 1.5 tiles, it stands where it is and counts toward the cap of 2.
- **AC-23** is split into (a) on tile at 0.2, (b) 0.4 tile behind, (c) 0.8 tile behind ("(miss) not in front"), with explicit scripts.
- No parameter value changed in this round.
- If the current code differs from any rule above (the on-tile knockback, the Waiting-follow behavior), report it in the build notes. The spec stands.

## Decisions already made

- D-001: no new input buttons.
- D-002, D-004: Option A, one sequential change set.
- D-005, D-007: the Owner places `manual.md` text. Do not edit `manual.md`.
- D-006: overlap display, and the display side used by the on-tile knockback.
- D-009: the `ManualTest` phrase check ignores line wraps.
- D-011: grubs take turns and crowd two deep; hit-stun 0.15 s; body hit; dash sets facing.
- D-012: the `on you:` line and the attacker's position in hit lines.
- D-013: knockback of a grub on the player's tile.

## Constraints

- Must play correctly at 30 and 60 FPS. Timers run on elapsed seconds, including the 0.2 s knockback.
- Prefer changes that reuse existing systems. If the Waiting behavior of a blocked grub is not local to existing systems, stop and report; a Plan step (11) may follow.
- Stop on spec ambiguity and hand back; do not decide.
- `manual.md` is Owner-placed. If `ManualTest` fails only because manual text from 59 or V-15 is not yet placed, report which phrases, and do not edit the manual.

## Open questions

None.

## Expected output

An outgoing Handoff addressed to `studio` (so the Studio can compose the QA and art-director Verify packets), with:

- the code and test changes in `repo/`, and the `run_tests` result;
- build notes: any spec/code mismatches found, the root cause of any defect, and anything you could not verify;
- a Sender assessment, which will be removed before QA receives it.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, design/combat.md, design/combat-visuals.md, manual.md (read only), repo/README.md, repo/game.py, repo/play.py, repo/bots.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-004-option-a-single-change-set.md, decisions/D-006-overlap-display-and-practice-room-manual.md, decisions/D-009-manualtest-phrase-check-ignores-line-wraps.md, decisions/D-011-grub-turns-stun-body-hit-dash-facing.md, decisions/D-012-on-you-line-for-displaced-enemies.md, decisions/D-013-knockback-of-grub-on-players-tile.md
- Previous handoff: goals/G-001-combat-monotony/65-game-designer-to-studio.md
