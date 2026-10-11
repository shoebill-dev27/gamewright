---
kind: goal
id: G-002
project: lantern-depths
status: active
created: 2026-10-10
---
# G-002: Combat feels monotonous

## Owner request

> 戦闘が単調なので改善したい

## Interpretation

Success: in a playtest of the 5-room slice, the player has to make different decisions across rooms
(where to stand, when to dash, which enemy first) instead of repeating one pattern, and the Game
Director judges the monotony addressed on that evidence. Out of scope: new biomes,
meta-progression, run length. Also out of scope (Owner, D-002): a hold-to-charge attack.

## Unknowns

All stages of route pattern 2 are open: the monotony has not been observed or diagnosed, a
direction choice is likely (D-001 limits some options), new behavior will need a spec and a plan,
and it is an experience Goal (Play, Review).

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | playtester | playtest-session | done | 01-studio-to-playtester.md |
| 2 | Diagnose | game-designer | diagnose-experience | done | 02-playtester-to-game-designer.md |
| 3 | Decide | game-director | make-decision, prepare-owner-escalation | done (escalated) | 03-game-designer-to-game-director.md |
| 4 | Decide | owner | — | done (Option A, D-002) | 04-game-director-to-owner.md |
| 5 | Design | game-designer | write-design-spec | done | 05-studio-to-game-designer.md |
| 6a | Plan | technical-director | technical-plan | done | 06-game-designer-to-technical-director.md (result: 08-technical-director-to-studio.md) |
| 6b | Design (visual cues) | art-director | write-design-spec | done | 07-studio-to-art-director.md (result: 09-art-director-to-studio.md) |
| 7 | Design (spec rulings before Build) | game-designer | write-design-spec | done | 10-studio-to-game-designer.md (result: 11-game-designer-to-studio.md) |
| 8 | Design (Grub lock cue update) | art-director | write-design-spec | open | 12-studio-to-art-director.md |
| 9 | Build | gameplay-engineer | implement-change | planned | — |
| 10a | Verify | qa | verify-change | planned | — |
| 10b | Verify (visual) | art-director | visual-review | planned | — |
| 11 | Play | playtester | playtest-session | planned | — |
| 12 | Review | game-director | review-outcome | planned | — |

## Route changes

- After step 3: Option B would change Owner Decision D-001 while the evidence leaves A and B both
  viable → escalation triggers → step 4 (Owner); all later steps paused.
- After step 4: the Owner chose Option A (D-002) with the condition that a hold-to-charge attack is
  not part of this Goal. The remaining route matches Option A's "If chosen" (Design → Plan → Build →
  Verify → Play → Review), so the later steps are unchanged. Goal set back to `active`. The Play
  step must be routed to the Playtester through a fresh Studio-composed Handoff without
  implementation knowledge.
- After step 5: the spec leaves the visual design of telegraph cues, the Charger lane indicator and
  the block/stun cues undecided (Designer's Q1), and these affect what the player sees (pillar 3,
  readable threats). Added step 6b (Design, `art-director`) in parallel with Plan 6a: neither
  consumes the other's output. Because the change affects visuals, Verify gains a parallel visual
  review. Build waits for both 6a and 6b. If the cue designs need timing changes, they go back to
  `game-designer`, not decided by the Art Director.
- After steps 6a and 6b: both done and mutually compatible. The plan fits Option A and the
  constraints (about 17–21 person-days, D-003 revisit trigger not met), so no escalation. Both
  results carried open spec questions that belong to `game-designer` (Flinch SQ1, slot lifetime,
  obstacle stun, waiting behavior, guard reference point, Grub lock N1, widths/angles/range Q-A,
  Q-B). Inserted Design step 7 before Build (return rule: Build with ambiguous spec → Design).
  The TD's F1–F7 feasibility checks and the saturated-color sprite check (F6) stay as first Build
  tasks; if one fails, Build returns to `technical-director` or `art-director`.
- After step 7: the Designer answered all questions (SQ1–SQ5, N1, Q-A, Q-B) and recorded D-005.
  No escalation: the rulings are inside the Designer's authority, D-001–D-004 are unchanged (no new
  input, 0.4 s floor, cap of 2) and the vision is untouched. One ruling changes a cue timing: the
  Grub locks at 0.2 s into the telegraph instead of at the lunge start. As planned in the previous
  route change, step 7's result goes to `art-director` before Build. Inserted step 8 (Art Director
  updates the Grub lock cue in `design/combat-enemy-visuals.md`). It is sequential, because Build
  consumes its result. Later steps renumbered (Build 9, Verify 10a/10b, Play 11, Review 12). If
  the Art Director finds the new timing unreadable, step 8 hands back to `game-designer` (the Art
  Director does not change timings). No TD step is needed: the only plan effect is that T3 uses the
  new Grub timing and the `locked` flag flips at 0.2 s, which the Build Handoff will state.

## Next action

art-director starts step 8 from `12-studio-to-art-director.md` and addresses the result to
`studio`. Then the Route operation writes the Build Handoff for `gameplay-engineer` from:
- `08-technical-director-to-studio.md` (task list T0–T9, D-004, cue interface, test strategy,
  Build A / Build B slicing);
- the updated `design/combat-enemy-visuals.md` and `09-art-director-to-studio.md` (VC1–VC14);
- `design/combat-enemy-depth.md` as updated, `11-game-designer-to-studio.md` (data-table values
  for T3 and others) and D-005.

The Build Handoff must:
- give acceptance checks V1–V14 (V12–V14 are new) and VC1–VC14 for QA;
- state that SQ1–SQ5 are all ruled, so Build need not report SQ defaults;
- state the Grub timing (tracking 0.2 s / locked 0.3 s) and the `locked` flag moment;
- ask for the result to be addressed to `studio`.

Watch items for later steps:
- Review should check that two-swipe Grub kills inside its telegraph (spec edge case 4) do not
  become a new single tactic.
- Retune items (spec Q3) wait for the playtest. The Waiting distances and the Spitter range of 12
  tiles are first values and are cheap to retune.

Pending Studio item: add `design/combat-enemy-depth.md` and `design/combat-enemy-visuals.md` to the
Design index in `project.md` (not writable in this operation; do it in the next operation that can
edit `project.md`).

When Build and Verify are routed, their Handoffs must ask for results addressed to `studio`
(needed to compose the independent Playtester Handoff for the Play step). VE1–VE5 (experience
signals) and spec 7.2 stay out of the Playtester's handoff.

## Outcome

—
